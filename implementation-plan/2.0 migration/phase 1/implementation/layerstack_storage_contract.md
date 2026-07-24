# Simplified LayerStack storage contract

This document is the normative filesystem, durability, checkpoint, branch,
materialization, and reclamation contract for implementation Stages 03–11.
The stage specifications own when each capability is enabled; this document
owns the common shape and invariants.

It supersedes earlier implementation sketches that proposed separate root,
locator, materialization, lease, and retention catalogs; separate publication,
hydration, squash, compaction, and migration journals; matching staging
families; a flat complete-tree manifest per root; or empty directories reserved
for later stages.

## Design decision

LayerStack uses ordinary files, immutable content-addressed objects, atomic
rename, directory `fsync`, and short file locks. It does **not** use SQLite, an
embedded database, a write-ahead-log library, or a second metadata service.

The storage model has six ideas:

1. immutable typed objects form the logical root graph;
2. small atomic ref files name live roots;
3. one transaction directory shape covers every multi-step mutation;
4. one locator LSM maps object IDs to non-deterministic physical locations;
5. one `CURRENT` file selects a verified materialization generation; and
6. reachability GC starts from durable refs and uses disk-backed mark runs.

## Canonical filesystem layout

The smallest complete target layout is:

```text
/eos/layer-stack/
├── .storage-writer.lock
├── format-v2.json
├── objects/
│   ├── loose/<prefix>/<ObjectId>.obj
│   ├── packs/<PackId>.pack
│   └── locators/
│       ├── tables/<TableId>.sst
│       └── CURRENT
├── roots/<prefix>/<RootId>.root
├── refs/
│   ├── heads/<BranchId>.ref
│   ├── checkpoints/<CheckpointId>.ref
│   ├── pins/<PinId>.ref
│   ├── leases/<LeaseId>.ref
│   └── legacy/<LegacyCheckpointId>.ref
├── receipts/<prefix>/<PublicationId>.receipt
├── materializations/<BackendKey>/<RootId>/
│   ├── generations/<Generation>/
│   │   ├── manifest
│   │   └── carriers/
│   └── CURRENT
├── control/
│   ├── authority
│   └── legacy-shadow
├── transactions/<TransactionId>/
│   ├── intent
│   ├── ready
│   └── work/
├── gc/
│   ├── ACTIVE
│   └── epochs/<Epoch>/
│       ├── state
│       ├── mark-runs/
│       └── barrier-roots/
├── trash/<Epoch>/
├── quarantine/
└── locks/
    ├── heads/<prefix>/<BranchId>.lock
    ├── locators.lock
    ├── materializations.lock
    ├── authority.lock
    └── gc.lock
```

`BackendKey` canonically encodes backend kind, backend format version, and
target profile. `locks/` contains coordination only and is never durable
truth. A stage creates a directory only when it first writes that class of
state; absent future directories are valid.

All paths are beneath a pre-opened LayerStack directory, use contained relative
components, and are owner-only and workload-masked. State files use a bounded,
versioned, checksummed canonical encoding. No correctness decision depends on
directory enumeration order, timestamps, inode numbers, or provider paths.

## 2. Logical object graph

`RootId` names an immutable `RootRecord`. A root is complete because its strong
edge reaches a persistent tree, not because publication rewrites a flat record
for every current path.

```text
RootRecord
└── strong: TreeNode
    ├── strong: TreeNode
    ├── strong: FileNode
    │   └── strong: SegmentPage
    │       ├── strong: SegmentPage
    │       └── strong: Chunk
    └── strong: symlink/device/whiteout metadata object when applicable
```

The immutable object kinds are:

| Kind | Required content | Rule |
| --- | --- | --- |
| `RootRecord` | schema/profile/features, complete `tree_id`, publication identity, optional parent/base provenance | `tree_id` is strong; provenance is weak for retention unless separately pinned |
| `TreeNode` | canonical raw-byte path radix, directory metadata, sorted child edges | updating a path rewrites only nodes on affected radix paths |
| `FileNode` | file metadata, size, sparse layout, first segment-page ID | unchanged file identity is reused |
| `SegmentPage` | bounded ordered chunk descriptors and next/child page edges | boundaries are deterministic/content-defined over the descriptor stream, so local file edits share unchanged pages |
| `Chunk` | immutable payload bytes | ID is typed, domain-separated SHA-256 over canonical bytes |

Xattrs, whiteouts, opaque directories, sparse extents, device metadata, and
symlink targets use explicit canonical fields or typed objects. Canonical paths
are raw bytes; lossy UTF-8 conversion is forbidden.

Every typed ID is domain-separated. Locator, pack, host, native carrier,
materialization generation, permissions, and timestamps that are not logical
filesystem metadata are excluded from `RootId`.

The first import of a legacy tree may cost `O(R+E)`. A later publication with
`U` upper bytes, `K` chunk descriptors, and `C` changed paths reads only the
frozen change stream and touched persistent-tree/segment nodes. It must not
scan or rewrite all `E` entries merely to produce a complete root.

## 3. Object placement and locators

A loose object has a deterministic path and needs no mutable locator record.
Immutable packs reduce inode and metadata overhead. Locator SSTs are required
only for packed objects and external carriers such as Stage 04 verified v1
ranges.

`objects/locators/CURRENT` names an ordered, bounded list of immutable SSTs.
Lookup checks the bounded page cache and newest-to-oldest tables. Compaction:

1. writes and verifies a new immutable pack and SST;
2. `fsync`s both files and their directories;
3. atomically installs a new `CURRENT`;
4. waits for readers/leases and a complete grace epoch; then
5. moves superseded packs/tables to `trash/`.

There is never an in-place pack rewrite. A carrier containing the last locator
for a reachable object cannot be removed until a replacement location is
durable and the replacement `CURRENT` is installed.

During Stage 04, new chunk payload remains in the already committed immutable
v1 carrier. The shadow writer stores:

- persistent tree/file/segment metadata as small loose objects;
- one immutable locator SST mapping each referenced chunk to its verified v1
  carrier byte range; and
- no duplicate candidate chunk payload.

Stage 08 may evacuate the last v1-backed locations into immutable packs. Until
then, legacy carrier deletion must obey the locator source-hold/lease rule.

## 4. Refs, publication, and recovery

Refs are independent atomic files, not rows in a global root catalog.

| Ref | Purpose | Strong retention seed |
| --- | --- | --- |
| `heads/<BranchId>.ref` | mutable branch head and publication generation | yes |
| `checkpoints/<CheckpointId>.ref` | named user/agent milestone | yes |
| `pins/<PinId>.ref` | policy/search/qualification retention | yes |
| `leases/<LeaseId>.ref` | active root/carrier/transaction protection with fence/expiry | yes while valid or recovery-uncertain |
| `legacy/<LegacyCheckpointId>.ref` | temporary v1-to-v2 compatibility mapping | yes until retirement gate |

A head file contains at least branch ID, root ID, publication generation,
publication ID, transaction ID, and checksum. Compare-and-swap holds only that
branch's short lock, re-reads the generation, atomically renames the new file,
and `fsync`s the parent. Publications to different branches do not share a
global root lock.

Every multi-step operation uses the same transaction shape:

```text
transactions/<TransactionId>/
├── intent       # operation, request ID, expected refs/generations, budgets
├── ready        # verified immutable outputs and proposed commit pointer
└── work/        # private temporary files; never reader-visible
```

The durable facts are deliberately small:

1. `intent` exists: the operation was admitted;
2. `ready` exists: immutable outputs were verified and made durable; and
3. the operation's commit pointer names the transaction.

Recovery derives the result:

- no `ready` and no commit pointer: abort and reap `work/`;
- `ready` but no commit pointer: retry the declared CAS if its expectation
  still matches, otherwise record the typed conflict and abort;
- commit pointer present: the operation committed, so recreate any missing
  receipt idempotently and reap `work/`;
- commit pointer present but `ready` or named immutable output is invalid:
  fail closed and quarantine; never guess or fall back.

`receipts/<PublicationId>.receipt` makes retries exact after a branch advances.
It may be rebuilt from a still-current commit pointer only during the narrow
post-CAS recovery window; after that it is retained according to the explicit
idempotency policy. The receipt and in-flight transaction are GC seeds while
required.

Hydration, publication, squash, pack compaction, and legacy migration differ in
their typed `intent`, verified output, and commit pointer, not in filesystem
machinery. This replaces the separate journal and staging families.

## 5. Checkpoint, branch, rollback, and MCTS

Successful publication always creates an immutable root and receipt. Agents do
not call a low-level save function to make ordinary work recoverable.

`save_checkpoint(name)` is a convenience operation for long-lived retention:

1. if the workspace is dirty, run normal publication;
2. if it is clean, reuse the current branch root; and
3. atomically create `refs/checkpoints/<CheckpointId>.ref`.

A clean checkpoint is `O(1)` metadata and stores no payload or copied manifest.
A dirty checkpoint has normal incremental publication cost. Deleting a
checkpoint removes only its ref; GC decides when unreferenced objects are safe
to reclaim.

Rollback has three explicit forms:

| Operation | Behavior | Head effect |
| --- | --- | --- |
| checkout | start a new workspace from the checkpoint root | none |
| revert | publish a new root whose complete tree is the checkpoint tree and whose provenance records the current head | advances head; payload and tree objects structurally share |
| reset | CAS the branch head directly to the checkpoint root | rewinds head; rejected on stale generation |

Squash cannot invalidate a checkpoint: it creates and verifies a new
materialization generation, atomically changes only materialization `CURRENT`,
and retires the old generation after leases and grace. `RootId`, checkpoint
refs, branch history, and publication generation do not change.

A clean branch/MCTS fork writes one bounded graph record outside LayerStack
plus one head or pin ref to the selected `RootId`. It is `O(1)` in parent
payload and allocates zero parent payload. Each active rollout gets:

- one selected immutable root;
- one independent flat native mount with `D≤64` lowers;
- one private upper/work pair; and
- one bounded lease.

It never mounts over a live parent workspace and never maps search depth to
native lower depth. Inactive nodes retain refs/pins and evaluation records, not
permanent materializations. OverlayFS remains file-granular: a one-byte first
write to a lower-only `F`-byte file may still scan/copy up `O(F)` bytes.

## 6. Materializations

Logical history is CAS; normal execution is a native filesystem. A
materialization manifest names ordered native carriers for exactly one
`(RootId, BackendKey)`.

Warm activation validates `CURRENT`, acquires a lease, and mounts the named
native carriers. A compatible current v1 stack may be referenced directly
during migration; LayerStack does not duplicate it merely to obtain a v2
directory name.

Cold activation reconstructs one private generation under
`transactions/<id>/work/`, verifies metadata/content, `fsync`s it, renames it
under `generations/<Generation>/`, then atomically advances `CURRENT`.
Incomplete generations are never returned.

Only active or policy-pinned roots require native materializations. Historical
checkpoints can remain CAS-only and hydrate on demand. This prevents
`number-of-checkpoints × full-tree-size` native storage.

## 7. GC, concurrent mutation, and deletion safety

GC traces only strong reconstruction edges. Parent/provenance edges do not
retain ancestry by themselves.

The root set includes:

- branch heads, checkpoints, pins, valid or recovery-uncertain leases;
- current authority and legacy compatibility roots;
- retained idempotency receipts; and
- admitted transactions and their verified outputs.

Marking uses sorted disk-backed pending/mark runs beneath the epoch directory.
It never builds an all-live `HashSet`, a whole-tree vector, or a whole-history
index in memory.

`gc/ACTIVE` is a durable write barrier. While it exists, any transaction that
will make a new strong ref visible must first create and `fsync`
`epochs/<Epoch>/barrier-roots/<RootId>`. GC repeatedly drains barrier roots and
closes the epoch only after it holds the GC lock, observes no undrained barrier,
and prevents a ref commit from crossing that close without joining the next
epoch.

Unmarked candidates are moved to `trash/<Epoch>/` in bounded batches and the
parent directory is `fsync`ed. Physical unlink is allowed only after a later
complete epoch and a final check of refs, leases, materialization `CURRENT`,
locator `CURRENT`, and active transactions. Restart treats uncertain state as
live. Reference counting alone is never deletion authority.

## 8. Memory and resource safety

The portable core and storage orchestration use safe Rust. Provider code may
retain existing audited OS-specific `unsafe`; no new `unsafe` is allowed in
the object graph, transaction, ref, locator, materialization, or GC code.

Required bounds:

| Resource | Bound |
| --- | --- |
| SeqCDC rolling window and input ring | one 32 KiB window plus one 32 KiB ring per admitted file |
| payload queue | zero; borrowed slices are consumed synchronously |
| storage workers | at most 4 globally |
| metadata queue | 16 items or 64 KiB, whichever is reached first |
| read/write buffers | 256 KiB per admitted worker |
| external merge | fan-in 8 with 64 KiB per run |
| shared locator/index cache | at most 16 MiB |
| publication managed memory | at most 4 MiB per operation, excluding shared cache |
| global storage byte permits | 64 MiB |
| GC memory | bounded buffers/cache only; mark/pending sets are disk-backed |

One supervisor owns every worker `JoinHandle`. Cancellation stops admission,
closes queues, joins workers, then releases permits and source leases. There
are no detached tasks. Registries and caches are capacity-bounded. Observation
back-references use IDs or `Weak`; a session/transaction must not participate
in a strong `Arc` cycle. FDs, memory maps, directory iterators, temporary
paths, permits, and leases have explicit owners and are released on success,
error, cancellation, panic containment, and shutdown recovery.

## 9. Performance and space contract

These are design requirements, not passed benchmark claims:

| Operation | Expected work |
| --- | --- |
| clean checkpoint | `O(1)` metadata; zero payload |
| clean branch/MCTS fork | `O(1)` metadata; zero parent payload |
| incremental publication | `O(U + K + changed Merkle/segment nodes)` after initial import |
| warm activate/checkpoint checkout | `O(D)`, `D≤64`; zero CAS payload reads |
| cold activate/rollback | `O(R+E)` reconstruction |
| head reset | `O(1)` CAS metadata |
| revert | `O(1)` logical tree reuse plus normal receipt/ref durability; hydrate only if later activated cold |
| squash | `O(R+E)` native rebuild; zero logical-object rewrite |
| GC | `O(reachable objects + bounded candidate scan)` with bounded RAM |

The native command, file, PTY, and stdin path does no CDC, CAS lookup,
materialization, pack, or GC work.

At average 16 KiB chunks, a 96-byte locator plus 64-byte segment descriptor is
approximately `160/16384 = 0.98%` of unique payload. This is not the complete
space result: small-file nodes, path/tree nodes, xattrs, pack headers, indexes,
refs, receipts, evaluation records, filesystem allocation, temporary
transactions, leased old generations, and slack remain in measured physical
accounting.

Settled storage is one current native working tree (plus explicitly active or
pinned materializations), unique reachable historical chunks, shared metadata,
and bounded index/pack slack. It is not one complete manifest or one native
tree per checkpoint.

Stage 11 must measure and pass the existing Preparation 04 gates before any
performance statement becomes qualified.

## Stage ownership

| Stage | New durable capability |
| --- | --- |
| 03 | No `/eos` change. Produce bounded deterministic chunk/object descriptors through an object-sink contract. |
| 04 | Add format marker, immutable roots and metadata objects, v1-carrier locator SSTs/`CURRENT`, receipts, and shadow transactions. Roots are shadow observations; legacy remains authority. Do not create future refs/materialization/GC/control directories. |
| 05 | Add on-demand materialization generations/`CURRENT`; reuse compatible warm v1 carriers and hydrate cold roots privately. |
| 06 | Add strict opt-in routing and active guards; no new durable storage family. |
| 07 | Add candidate-private branch heads, automatic immutable publication roots, named checkpoint refs, durable leases, receipts, per-branch CAS, and recovery through the common transaction shape. |
| 08 | Add packs, pins, locator compaction, GC epochs/write barriers, trash, quarantine, and last-locator evacuation. |
| 09 | Add same-root squash by writing a materialization generation and swapping only `CURRENT`. |
| 10 | Add atomic `control/authority` and `control/legacy-shadow`; candidate is authoritative only for the approved cohort and legacy rollback remains parity-gated. |
| 11 | Qualify every gate, prove every retained checkpoint reconstructs without a v1-only locator, then retire legacy state and compatibility refs. |

Stage 04 roots are not promised as indefinitely retained user checkpoints while
their last payload locations are v1 carriers. The public retained-checkpoint
guarantee begins when Stage 07 refs and Stage 08 retention/evacuation are
active. If an earlier checkpoint guarantee becomes a requirement, Stage 04
must create durable source holds that legacy deletion and squash obey.

## 11. Non-negotiable validation

Implementation is blocked unless tests prove:

- canonical root/object IDs are identical across input fragmentation and host
  enumeration order;
- repeat publication returns the exact receipt;
- stale same-path publication conflicts while disjoint branches progress;
- a clean branch/checkpoint allocates zero parent payload;
- checkpoint checkout, revert, and reset have distinct tested semantics;
- checkpoints remain readable before, during, and after squash;
- crash recovery at every `intent`/`ready`/commit boundary is deterministic;
- no ref commit can race past the active GC barrier;
- no reachable last locator, leased generation, or current materialization is
  unlinked;
- repeated success, error, cancellation, restart, compaction, and GC return
  queues, permits, workers, tasks, FDs, mappings, and transaction memory to
  their declared bounds; and
- no SQLite file, SQLite dependency, database process, or unbounded resident
  live-set is introduced.
