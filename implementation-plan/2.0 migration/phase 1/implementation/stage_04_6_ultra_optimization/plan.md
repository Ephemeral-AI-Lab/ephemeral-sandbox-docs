# Stage 04.6 checkpoint and projection optimization plan

Status: **PROPOSED — REPLACEMENT ARCHITECTURE, TARGETS NOT YET MEASURED**

Decision record: [`review.md`](review.md)

This plan replaces the former CAS-first loose-object publication and default
complete-carrier/carrier-vector physical path. It retains a constrained
shallow directory projection for the qualified no-extra-device OCI/Linux
path. It preserves the Stage 03
backend-neutral logical checkpoint:

```text
RootRecordV3 -> TreePage -> FileNode -> SegmentPage -> Chunk
```

and the atomic logical identity pair:

```text
{ RootId, AttributionRootId }
```

It changes the physical publication and materialization architecture:

- loose per-chunk files cease to be the primary payload store;
- complete native carriers cease to be the normal result of publication;
- raw OverlayFS upper directories are not a general durable delta format;
- payload bytes may have replaceable, leased physical locators;
- logical checkpoints are authoritative and complete;
- OCI, Firecracker, and WASI projection namespaces are independent,
  rebuildable caches; sole-locator adopted payload remains pinned until
  evacuated; and
- block/range-CoW, immutable-image, and lazy mechanisms are optional
  accelerators, never correctness requirements.

This is an architectural replacement, not an in-place destructive migration.
Legacy roots and carriers remain readable until qualification and rollback
windows finish.

## Stage 04.6 release scope

Phase 1 Stage 04.6 implements, benchmarks, and production-qualifies the
OCI/Docker adapter. Firecracker and WASI are Phase 3 consumers, not Stage 04.6
release dependencies. This stage freezes their adapter boundary, keeps every
backend-specific identifier out of logical identity, supplies canonical
golden fixtures, and documents how each can project the same root. It does not
build those adapters or require live Firecracker/WASI conformance and
performance campaigns before the OCI path ships.

## Performance scope

The absolute 100x/500x reference ceilings are reported for first ingestion,
publication, and activation. First ingestion is scored against those ceilings
and its measured one-pass physical floor. Normal incremental publication and
stored-projection activation must meet the applicable 100x gate; setup is
excluded only when no product operation performs it. The critical
steady-state operations are:

- publish/add a layer;
- checkpoint;
- fork;
- public logical squash, implemented as an ancestry prune;
- rollback/root switch;
- winner reactivation;
- activate an already-built compatible projection; and
- exact-root reuse.

First ingestion remains measured as a separate one-time operation. It is
optimized toward its measured one-pass physical floor, but a system that must
read and hash every unseen byte does not promise an impossible 500x result.

“Cold” is not one bucket. A **cold-page-cache worker with a locally stored,
compatible projection** is the post-setup activation case and must meet the
100x gate. A **true empty worker with neither projection nor payload** must
acquire/build the physical bytes and is scored against the matched direct
copy/transfer floor; it must not be advertised as a 100x or 500x
materialization. Product-required network acquisition remains inside the
outer placement timer and is also reported as a separate subspan; fixture
preparation that is not product work is timed separately.

The preserved references remain:

| Historical component interval | Current | 100x | 500x |
| --- | ---: | ---: | ---: |
| Prepared-change CDC/CAS publication | `107.024411507 s` | `1.070244115 s` | `214.048823 ms` |
| Cold complete native carrier construction | `9.987675338 s` | `99.876753 ms` | `19.975351 ms` |
| Explicit same-key materializer reuse | `6.361909169 s` | `63.619092 ms` | `12.723818 ms` |
| Ordinary warm generation lookup | `35.375 us` median | preserve | preserve |

The old timers omitted work on their boundaries. New campaigns preserve those
inner spans for continuity and add an outer source/action-to-ready clock.

## Required outcomes

| Post-setup operation | 100x-equivalent ceiling / release gate | 500x-equivalent ceiling / preferred gate | Aggressive internal target |
| --- | ---: | ---: | ---: |
| Small-layer root commit with completed hash-and-durability receipt | `<=1.070 s p95` | `<=214 ms p95` | `<=20 ms p95` |
| Small-layer root commit without a receipt | `<=1.070 s p95` when its matched one-pass floor permits | `<=214 ms` only when measured, never assumed | one-pass delta floor |
| Defined small mutation through durable root, including an immediate-post-command receipt miss | `<=1.070 s p95` | `<=214 ms p95` only if matched | receipt-hit rate reported, no omitted hash/sync |
| Sustained 64/1,000 non-closing small logical-layer commits, submission to same-upper ready | `<=1.070 s p95` **and every sample `<=1.070 s`**; rejection or deferred readiness fails | `<=214 ms p95` when its matched divisor also passes | `<=20 ms p95`; `D_proj` unchanged |
| Cold-page-cache worker with locally stored compatible projection to workspace-ready | `<=99.9 ms p95` | `<=20 ms p95` | `1--10 ms` hypothesis |
| True empty-worker placement with no local projection or payload | no false 100x claim; `<=1.25x` matched direct copy/transfer floor | no false 500x claim | bounded hydrate-and-adopt; acquisition separate |
| Exact frozen-recipe handoff | `<=99.9 ms p95` | `<=20 ms p95` | metadata-bound selection/reprobe |
| Raw-upper normalization | matched one-pass entry control | no unconditional 500x claim | `O(E_upper)`, separately timed |
| Public hot rollback to a locally compatible projection | `<=99.9 ms p95` | **required `<=20 ms p95` outer operation** | ref-selection service `<=1 ms p95` |
| Cold rollback without a compatible projection | physical build/acquisition floor, reported separately | no false 500x claim | logical ref selection remains `<=1 ms p95` |
| Public logical squash (`squash_layerstacks`) | `<=99.9 ms p95` | **required `<=20 ms p95` outer operation** | ancestry-prune service `<=1 ms p95`, no payload work |
| Exact-key reuse | `<=63.6 ms p95` | `<=12.7 ms p95` | `<=1 ms p95`, no payload traversal |
| Warm generation lookup | preserve baseline | preserve baseline | matched median and p95 each `<=1.05x` control and `<=control + 2 us` |

A result is called 100x or 500x only against a matched operation with the same
start and readiness boundary. Publication and materialization remain separate
scores. Formally, a 100x-labelled result must satisfy
`candidate <= min(historical_absolute_ceiling, matched_current / 100)`; a
500x label substitutes `/500`. Meeting only the historical ceiling is
reported as “within the historical 100x-equivalent ceiling,” not as a matched
100x speedup. Rows without a matched current operation are engineering gates;
the column names describe equivalent ceilings, not automatic speedup labels.

For the sustained-commit row, each sample starts before admission, queueing,
or backpressure and ends only after the root/ref are durable and the same
mounted private upper accepts and passes the next-command probe. All forced
synchronous maintenance is inside that clock. Asynchronous maintenance is
separately timed to `D_settle`, but any delay it causes to a later submission
is charged to that later sample.

For mount, image, block, or lazy activation, always report:

1. workspace-ready;
2. first open/first byte;
3. first selected-file full read;
4. metadata-only repository walk;
5. first byte-reading full repository scan;
6. deterministic random reads, cold and warm;
7. first write plus fsync/copy-up/allocation; and
8. steady-state warm activation.

## Non-negotiable correctness

- `RootId` and `AttributionRootId` contain no backend path, inode, whiteout
  encoding, carrier generation, block-image ID, VM snapshot ID, or WASI
  handle.
- A logical root is a complete immutable view. No logical operation replays a
  native layer chain.
- Every checkpoint preserves all identity-bearing source semantics supported
  by the existing canonical v3 contract. Stage 04.6 qualifies OCI against
  those semantics: a worker reproduces every requirement named by the root
  and its capability receipt or rejects placement. It does not republish a
  weaker root. Firecracker and WASI consume the same contract in Phase 3 and
  may likewise reject an unsupported placement without changing the
  checkpoint.
- At least one durable verified payload locator exists before a root ref
  becomes visible.
- Logical root/ref state is authoritative; projection namespace/cache metadata
  is disposable after any sole-locator adopted payload is evacuated.
- No large I/O occurs under the global ref writer lock.
- Every durability/ownership phase transition is journaled,
  restart-deterministic, idempotent, and bounded. In-memory logical substates
  need not each force a WAL record.
- Presence of a directory or file never substitutes for a committed selector
  and receipt.
- Cancellation and failure return all memory, descriptors, mounts, leases,
  staging, and active-upper inventory.

## Architectural shape

```text
ExecutionAttempt
  -> AttemptSealer + ChangeRecorder
  -> Publisher
       -> CheckpointStore (existing canonical v3 Merkle objects)
       -> PayloadStore (immutable IDs, replaceable physical locators)
  -> durable {RootId, AttributionRootId}
  -> ProjectionStore
       -> OciAdapter
       -> FirecrackerAdapter
       -> WasiAdapter
       -> optional qualified accelerators
```

There is one logical truth and several rebuildable physical views.

Stage 04.6 uses no SQL or key-value database, embedded database engine,
database server, or database daemon. “Catalog” means immutable sorted
run/index files plus an atomically selected manifest; “journal” means the
bounded file protocol specified below. Readers use bounded streaming or
read-only `mmap`, so a database is neither a correctness dependency nor a
hidden second source of truth.

### Component boundaries

| Component | Ownership |
| --- | --- |
| `AttemptSealer` | quiescence, writable-FD/mapping drain, stable execution epoch, completed hash-and-durability receipt |
| `ChangeRecorder` | backend-specific authoritative changed paths/ranges and durable cursors |
| `CheckpointStore` | canonical v3 Merkle objects in immutable packed/page runs, legacy loose-record reads, checkpoint transaction journal, OCC ref updates |
| `PayloadStore` | payload IDs, immutable locator runs, packs, leases, evacuation, reachability inventory |
| `Publisher` | bounded orchestration of seal evidence, path-copy updates, locator installation, and root commit |
| `ProjectionStore` | backend projection generations, receipts, leases, quotas, and rebuild |
| backend adapters | capability proof, build, semantic validation, activation, teardown |
| `Verifier` | construction receipts, semantic oracle, scheduled audit, corruption quarantine |

These are real replacement and failure boundaries. No generic storage
framework or speculative adapter hierarchy is introduced beyond them.

Minimal interface responsibilities are:

```text
CheckpointStore:
  resolve_root
  install_immutable_pages
  commit_checkpoint
  compare_and_swap_ref

PayloadStore:
  resolve_payload
  install_locator_run
  lease_locator_generation
  evacuate_locator

AttemptSealer:
  finish_epoch
  validate_receipt
  invalidate_on_execution

ChangeRecorder:
  changes_since
  validate_cursor

ProjectionAdapter:
  capability_profile
  ensure_projection
  activate
  verify_probe
  teardown
```

## Logical checkpoint and payload representation

Keep the Stage 03 canonical v3 root, tree, file, segment, and chunk encodings.
Keep SeqCDC provisionally as the canonical content segmentation policy because
it provides insertion locality. Do not couple it to loose chunk files.

The existing v3 regular-file format already has explicit zero/hole/chunk
extents in fixed-fanout `SegmentPage`s and no inline-small-file payload form.
Replace the root-sized vectors currently built by
`FileSnapshotV3::Regular`, `build_segments`, and `reconstruct_segments` with
streaming page builders/cursors while preserving byte-identical canonical
objects and golden IDs. A 1 GiB build/reconstruct must stay within the declared
RSS/working-set bounds.

Publication path-copies only changed fixed-fanout tree/segment pages. Parent
checkpoint history remains outside `RootId`; two histories reaching identical
filesystem content have the same root.

Payload identity maps to one or more physical locators:

```text
PayloadId -> [
    SealedFileRange(file_token, offset, length),
    PackRange(pack_id, offset, length),
    AdoptedExtent(payload_owner_id, offset, length),
    RemoteObject(provider_key)
]
```

`PayloadId` is the existing typed v3 `Chunk` ID, not a new digest, identity,
or second content truth.

Locator generations are immutable, checksummed, leased, and selected
explicitly. Their paths and IDs do not enter logical identity. The locator
index is a fixed-page persistent hierarchy with compressed consecutive ranges;
a flat chunk/block vector copied per file or root is forbidden, and readers
hold only a bounded cursor.

Every physical owner also has an immutable, generation-selected reverse
manifest:

```text
PayloadOwnerId -> sorted [(owner_offset, length, PayloadId, locator_ordinal)]
```

This is the bounded source of truth for evacuation; retirement never scans
the store hoping to rediscover references. There is at most one reverse entry
per installed locator range and at most `64` encoded bytes per entry plus
half-full `16 KiB` pages. The `100,000` limit applies to one immutable
manifest **shard**, not to one physical owner. An owner root range-indexes as
many non-overlapping shards as its exact locator count requires; the shard
index is itself a fixed-page hierarchy selected atomically with the forward
locator generation. Thus a 1 GiB file at the canonical 8 KiB minimum has at
most 131,072 ranges and uses at most two shards rather than being rejected.
Builders create at most 100,000 reverse records per bounded batch under one
ownership group and a bounded cursor. Shard count is derived from the exact
owner length/count and the admitted workspace byte/inode quota; there is no
flat per-owner vector or arbitrary 100,000-range correctness limit. The
600,000/1,200,000-record thresholds apply to unreachable/replacement
maintenance debt, not live manifest capacity. Reverse metadata is charged to
`M` and removed only after the old selector and leases retire. Recovery and
cancellation tests interrupt every forward/reverse-selector boundary.

The hierarchy is one generation-selected persistent B+tree, not an
ever-deepening LSM/run chain. Pages are `16 KiB`; internal entries have a
fixed bounded encoding; no occupancy claim relies on hash prefix compression.
Tree height is capped at 6, and a point lookup performs at most eight page
reads: selector, up to six tree pages, and one locator-value page. Non-root
pages must be at least half full before selection or the builder bulk-builds a
replacement tree/returns bounded backpressure.

One worst-case lookup therefore pins at most `8 * 16 KiB = 128 KiB` of index
pages. Four concurrent storage lookups pin at most `512 KiB`; they use the
declared mmap/index window and release pins on completion or cancellation.
Index maintenance uses at most eight `64 KiB` merge buffers (`512 KiB`) and
the normal storage byte permits. These bounds are included in, not additional
to, the aggregate storage-memory limits.

A locator value is at most one page and selects at most four physical
locators. A block-image locator may encode at most nine spans for one
maximum-size `32 KiB` chunk; greater fragmentation first evacuates that chunk
to a contiguous pack locator and never appends an overflow chain.
Locator-maintenance starts at `256 MiB`, 600,000 records, or 10 jobs and
hard-backpressures at `512 MiB`, 1,200,000 records, or 20 jobs, whichever
comes first, until a bounded merge/evacuation transaction retires debt.

The initial implementation supports:

1. storage-owned sealed native file ranges for zero-copy adoption of
   already-written private-upper bytes;
2. bounded append-only packs: at most `64 MiB` payload, `100,000` records, and
   `80 MiB` total allocation; and
3. legacy loose chunks as a read-only migration locator.

New non-adoptable bytes stream once into packs. Do not create loose objects or
a hidden full staging checkout first. An arbitrary user-owned initial
workspace is non-adoptable because a hardlink would remain mutable through the
user's inode; it must stream into packs unless ownership and immutability are
proved and transferred.

When a complete native projection is required, a crash-safe
**hydrate-and-adopt** transaction reconstructs each file directly into a
storage-owned immutable generation. The finished allocation is itself exposed
as the lower through that same storage-owned namespace; no storage-internal
hardlink and no second native checkout is created. Logical hardlink groups
have exactly their canonical directory links, including while generations
overlap, so storage ownership cannot inflate observable `st_nlink`.
Native sealed-range locators are installed while source pack locators remain
valid. The locator selector changes only after byte durability and semantic
verification; the projection is then installed, probed, and selected; only
then may duplicated pack records be compacted. The journal states are:

```text
Building
  -> BytesDurable
  -> SemanticsVerified
  -> AdoptLocatorsDurable
  -> ProjectionReady
  -> CurrentPublished
  -> AccountingReady
  -> SourceLocatorsRetiring
  -> MaintenanceSettled
```

Before `AdoptLocatorsDurable`, cancellation or recovery may delete the
journal-owned build. At and after it, the native generation is payload-owned
and cannot be cancellation-deleted: recovery finishes its projection, keeps
it as a payload-only owner, or evacuates it through the normal locator
protocol. Peak source plus target allocation is reported, and settlement is
incomplete while avoidable native-plus-pack duplication remains above the
gate.

`AccountingReady` means every allocated byte has exactly one ledger owner and
`P_staging` contains only declared in-flight work; it is not a settled-space
pass. `MaintenanceSettled`—called “settled” everywhere in the release
tables—requires evacuation complete, `P_staging = 0`, the avoidable-duplicate
gate satisfied, and no lease blocking retirement.

Before the first side effect in each bounded ownership phase, the transaction
durably appends and syncs **one umbrella intent** naming the exact owner,
reserved namespace token/range, allocation ceiling, cleanup action, and hash
of an immutable streamed batch manifest. Creates, preallocations, payload
writes, and renames listed by that manifest use grouped durability; they do
not append or sync one WAL record per file, chunk, or directory entry.
Selector installation and retirement are later ownership phases, each with
its own umbrella intent and durable completion. There are at most eight
durable phase transitions per operation. The `<=256 KiB` pending record
contains manifest roots and bounds, never a million-entry list; the manifest
pages/spool are journal-owned and charged to `M`. Crash injection brackets
every phase intent, grouped allocation/sync, rename, forward/reverse selector
update, lease transition, and deletion. Bounded recovery follows pending
journals and owner manifests; it never enumerates the storage namespace.

Later locator evacuation copies only
still-reachable unique ranges into packs, switches the locator generation,
marks the old generation `Retiring`, and makes only a bounded lease-drain
attempt. A live lease leaves an accounted but explicitly non-settled
journal-owned retirement; it does not delay the logical ref response, but
admission backpressures at the hard byte/count quotas instead of hiding or
calling it settled.

Each GC/compaction transaction handles at most the minimum of `64 MiB`,
`100,000` records, the operation's remaining five-percent payload-staging
headroom, the global byte permits, and available disk admission. Settled pack
dead/slack must remain `<=2%`; exceeding it fails the release space gate.

Canonical `FileNode`, `TreePage`, `SegmentPage`, metadata, hardlink, and
attribution records also install in immutable packed/page-object runs with
grouped durability and legacy loose-record dual-read. Payload packing alone
does not remove the current per-record temp/write/fsync/link/unlink/
parent-fsync storm. Canonical bytes and typed IDs remain unchanged.

A `RemoteObject` locator additionally records and reconciles canonical bytes,
provider-allocated bytes, billed/compressed bytes, replicas, incomplete
multipart uploads, retained versions, and deletion receipts. Local
qualification sets remote bytes to zero. A remote-enabled profile reports
`T_estate = T + R_remote_allocated`; remote storage is never omitted from the
space denominator or cleanup proof.

Only an upper explicitly frozen for a branch/projection boundary may be
adopted. An adopted file is transferred to `PayloadStore` ownership and exposed
through its storage-owned projection namespace without an extra directory
link. Projection eviction does not delete the payload. If an adopted extent
is the sole durable locator, that payload allocation is
pinned until evacuation installs and selects an alternative locator and all
leases drain. “Disposable” never means deleting the last reachable bytes.

## Honest capture receipts

The checkpoint call can be metadata-bound only when the expensive work is
already complete and reported. A normal logical checkpoint captures an
immutable payload copy into packs but does **not** freeze or rotate the active
OCI upper. `AttemptSealer` uses:

```text
RUNNING
  -> QUIESCED_CAPTURING
  -> PAYLOAD_SYNCING
  -> EPOCH_RECEIPT
  -> COMMITTED
```

Any admitted command, writable descriptor, or shared writable mapping
invalidates an uncommitted candidate. After commit, a new recorder epoch
starts in the same active upper. Notifications may schedule work but never
prove completeness.

A valid receipt binds:

- execution/upper epoch;
- authoritative change-recorder cursor;
- stable file identities and canonical hashes;
- data and metadata writeback completion;
- durability method and sync boundary;
- dirty bytes written and sync/fsync counts;
- semantic normalization status; and
- all memory/FD/lease ownership needed to finish publication.

For a non-frozen continuation, the receipt must name immutable durable pack
locators for every newly reachable payload byte; a hash of a still-mutable
upper is insufficient. A genuinely frozen, storage-owned upper may instead be
adopted by the separate branch/projection transaction.

A raw rename and parent `fsync` do not make dirty file contents durable.
Qualified directory implementations must either:

- sync the changed files and directories;
- await and measure a grouped `syncfs`, including unrelated-superblock
  interference; or
- write the payload into a journaled pack and sync it once.

Benchmark both final checkpoint-call latency and combined
mutation-to-durable-root latency. A receipt is a latency-overlap technique, not
permission to move required work outside measurement.

## Publication state machine

One journal owner coordinates logical objects, payload locators, and refs:

```text
OPEN
  -> QUIESCING
  -> CAPTURING
  -> RECEIPT_READY
  -> PAYLOAD_LOCATORS_DURABLE
  -> LOGICAL_ROOT_DURABLE
  -> REF_COMMITTED
  -> CONTINUATION_EPOCH_READY
  -> OPTIONAL_PROJECTION_READY
  -> RECLAIMABLE
```

These names describe logical substates and observability, not a requirement
for one WAL sync per arrow. Adjacent substates that share one ownership
boundary are covered by one umbrella durable phase; no operation may exceed
the eight-transition durable-phase cap.

`REF_COMMITTED` is the only logical visibility point. Before it, recovery
finishes or reclaims a bounded journal-owned orphan. After it, the logical root
and at least one payload locator are complete. Projection failure never
invalidates the root. If requested activation then fails, return a structured
`checkpoint committed; activation failed` result containing the `RootId` and
retryability; never report publication as rolled back.

Large scans, hashing, packing, and projection builds happen before the short
ref CAS. Disjoint publications run concurrently. A losing branch-head CAS
retains a valid immutable root and returns a normal OCC result.

### Three publication paths

**Post-setup receipt hit**

1. validate the quiesced capture epoch, immutable payload locators, and
   recorder cursor;
2. install changed payload locator/page runs;
3. install the canonical logical root and attribution root;
4. commit the selected ref;
5. atomically advance the change-recorder epoch in the same private upper; and
6. optionally select/probe a compatible projection only when the caller
   requested a different workspace.

Foreground cost is metadata-bound. This is the primary 500x candidate.
It is never reported as the generic OCI publication latency. Qualification
reports receipt-hit rate by workload and includes a primary small-edit cell in
which the final write occurs immediately before command exit, forcing the
receipt-miss path.

**Post-setup receipt miss**

1. stop command admission and drain the process tree;
2. enumerate authoritative changes;
3. scan/hash all required changed files or ranges;
4. complete writeback and durability;
5. follow the normal root commit; and
6. report the full synchronous cost.

This path remains correct and bounded. It makes no false 500x promise.
For the defined small-edit corpus it must still pass the combined
mutation-to-durable-root 100x-equivalent ceiling; larger files/package trees
are scored against their matched one-pass byte/entry floor.

**Very first import**

Walk, read, chunk/hash, install payload locators, install canonical pages,
verify, sync, and publish exactly once. Target `<=1.25x` the measured
read/hash/write/metadata lower bound. First import is never combined with
post-setup activation to flatter either result.

### Non-rotating active continuation

Ordinary post-setup `add layer`/checkpoint publication is a logical epoch
commit, not a native-layer promotion. Once immutable pack locators and the
root/ref are durable, the already-mounted private upper remains the active
workspace and a new change-recorder epoch begins in it. No lower is added, no
mount changes, and no directory flatten is required for same-workspace
readiness. Failure before the ref commit preserves the previous dirty epoch;
failure after it recovers the committed root and either advances or rebuilds
the recorder cursor before admitting another command.

A physical upper is frozen and continuation rotated only when a caller needs
a branchable native recipe—for example, an immediate OCI fork from the
quiescent head—or when the active attempt is closed. That separate
`freeze_for_branch` transaction requires the upper to match the committed
head exactly, transfers ownership, and gives every continuing sibling a new
private upper. It may increase `D_proj` and therefore owns all projection
compaction cost; normal layer publication never does. A historical or
post-head fork uses an already-compatible projection or the separately timed
projection-build path.

## Logical operations

Every checkpoint already names a complete persistent view:

```text
fork             = create a ref to an existing checkpoint
rollback         = OCC-select an older checkpoint
ancestry prune   = update external checkpoint-history selection
root equality    = compare RootId
```

Stage 04.6 deliberately changes public `squash_layerstacks` into this logical
ancestry prune. It must preserve exactly the same
`{RootId, AttributionRootId}`, atomically select bounded external history
metadata, move no payload, build no projection, and leave already-active
sessions on the same complete root. If attribution changes, that is a normal
attribution publication with changed-page cost, not an `O(1)` squash.
Physical flatten/remount becomes separately named, timed internal maintenance;
it is not on the public squash response boundary. The migration is gated by
`checkpoint_refs_v2`, keeps the old implementation as rollback until its
observation window closes, and updates the catalog/readiness contract before
enablement.

The repository currently has no public committed rollback operation. Stage
04.6 is not complete until ProductAccess exposes logical rollback and the
generated catalog contains the implemented operation. This plan does not
invent its eventual CLI spelling: the benchmark consumes the generated
catalog. A rollback response selects the old root; workspace-ready is a
separate required subspan and meets the 20 ms hot gate only with a compatible
local projection. A cold historical root without one is honestly timed
against its physical projection-build/acquisition floor.

An inactive node owns only bounded ref/checkpoint metadata, its unique logical
history, and shared Merkle/payload-store allocation counted once. A fork
causes no per-node/private native projection or payload and owns no upper,
complete carrier, image, or mount.

## Projection architecture

Projection key:

```text
(RootId, backend_kind, backend_format_version, target_profile)
```

`AttributionRootId` is never included. If attribution is physically embedded,
it is a separately keyed auxiliary artifact/generation. Attribution remains
independently queryable.

Retain the existing explicit projection lifecycle:

```text
Building -> Ready -> Published -> Terminal
```

`STATE` is operation truth, `MANIFEST` is immutable, and `CURRENT` selects one
published generation atomically. Directory presence is never readiness.

### Qualified no-extra-device OCI/Linux path

The logical checkpoint/publication architecture is host-OS and Docker-image
agnostic. Physical writable execution is necessarily capability-qualified.
OCI readiness uses an adapter-owned namespace/read probe over a known fixture
path and never assumes that the image contains `sh`, `true`, or any other
binary. The base OCI path executes in a qualified Linux environment and uses
ordinary storage-owned directories plus a proved union facility, normally
OverlayFS; on a non-Linux host that environment lives inside the product's
declared OCI Linux VM. Stage 04.6 adds no reflink, FUSE, loop, NBD,
device-mapper, DAX, kernel module, privileged sidecar, or target-image helper
requirement.

A raw OverlayFS upper is not a generic reusable carrier:

- correct lower hardlink behavior may require `index=on`;
- origin/file-handle metadata then binds it to exact lower identities;
- lower-directory rename depends on `redirect_dir`; and
- whiteout, opaque, metacopy, xattr, sparse, ownership, and hardlink semantics
  require explicit normalization.

Therefore:

- the accelerator is an exact frozen mount-recipe bundle: upper, required
  overlay-private state, exact lower generation/filesystem identities, mount
  options, and capability receipt are pinned and semantically reprobed; a raw
  directory alone is never remounted/rebased as a generic lower; and
- a reusable OCI projection is a normalized clean directory delta or complete
  directory produced under a semantic oracle.

Normalization is `O(E_upper)` metadata work. It never adds a
storage-internal hardlink: those links would change workload-visible
`st_nlink`, especially while old and new generations overlap. The semantic
oracle checks link counts with concurrent generation leases. Payload is reused
only by retaining the storage-owned source namespace as a selected lower or
locator. If exact normalization would require copying payload, the hot
publication/handoff path does not perform that copy and does not call the
result zero-copy. It retains the exact recipe or schedules a
separately timed, admission-controlled evacuation/physical-flatten
transaction. That transaction reports source-plus-target peak allocation,
charges every byte to `P_staging`, switches locators only after the target is
durable and verified, and deletes the source only after leases drain. If its
declared peak or settle deadline cannot fit, normalization is rejected.

Projection depth:

- `D_proj` counts incremental LayerStack delta/carrier lowers above one
  mandatory base (`total_overlay_lowers = 1 + D_proj`);
- operational target `D_proj <=4` (`<=5` total lowers);
- candidate activation rejects `D_proj >8` (`>9` total lowers); and
- the capability receipt records the selected mount API and its separate
  platform ceiling: upstream OverlayFS permits 500 total lower directories
  on a qualified new-mount-API path, normally 499 incremental LayerStack
  carriers when one mandatory base consumes a slot; the correct legacy mount
  fallback records its serialized `lowerdir=` option/path ceiling.

Compaction starts before `D_proj=4` is crossed. It retains existing
storage-owned lowers or builds a separately accounted projection; it never
adds hidden cross-generation hardlinks to reuse payload. Complete
directory hydration uses the hydrate-and-adopt transaction and is timed as
construction, not mount-ready materialization. It is a correct read-only
projection fallback. Writable sibling activation additionally requires a
qualified union/CoW facility; if none is present, placement rejects rather
than creating one complete private lower per sibling.

Generic OverlayFS performs whole-file data copy-up. A one-byte write to a
1 GiB lower file may allocate a complete 1 GiB upper. The qualified
directory path
reports that write, peak, scan, and evacuation cost and does not claim
range-CoW.

### Optional Linux accelerators

Each accelerator has an independent capability probe, semantics
qualification, feature flag, and fallback to the qualified OCI path:

- proved reflink/clone-aware copy-up plus dirty-extent evidence;
- content-addressed block-CoW workspace;
- file-backed EROFS or composefs-like immutable projection;
- FUSE/lazy CAS projection only when `/dev/fuse` and policy allow it; and
- loop/NBD/device-mapper only when devices and policy explicitly allow them.

A one-byte 1 GiB accelerated edit must settle with localized new payload. A
retained full-file delta disproves that accelerator.

### Firecracker

The stock path constructs one regular file-backed, immutable workspace image;
attaching it to Firecracker does not itself require a loop device. Stock
Firecracker does not directly consume the hierarchical extent map. `O(1)` map
activation requires a separately qualified userspace/custom block backend or
conversion layer. In that optional layer, a flat per-root block map is
forbidden. A backend-owned CoW block layer may provide changed disk extents,
which are combined with a guest semantic journal; raw dirty blocks cannot
describe rename, unlink, hardlinks, or attribution. Firecracker's snapshot
dirty tracking covers guest memory, not virtual-disk blocks.

Active siblings attach that one base image read-only and each receive one
bounded private writable guest upper/delta drive. A version-pinned guest
controller mounts them through a semantically qualified guest union. The
adapter must never copy the base image once per VM. Sparse private drives are
an allocation optimization only after physical blocks are measured; if the
guest filesystem, union semantics, or allocated-space accounting does not
qualify, that worker rejects placement.

The Firecracker `target_profile` binds the projection format version,
filesystem kind/version/block size/features, image-builder version, guest
kernel/controller version, and normalization profile. These are projection
inputs, never `RootId` inputs. Image creation and readback use either an
adapter-owned userspace filesystem codec or a pinned builder/verification
microVM that consumes the regular file directly. The correctness path does
not assume `/dev/loop` or an undeclared host command. A version-matched durable
guest semantic journal may accelerate publication, but a missing, gapped, or
crash-uncertain cursor triggers the fully timed semantic scan; raw dirty
blocks alone are never sufficient evidence.

Firecracker image, guest inode, backend block-journal, guest-memory bitmap, and
snapshot IDs remain projection-local. KVM and read/write `/dev/kvm` are
requirements only for executing the Firecracker adapter in Phase 3;
they are not dependencies of checkpoint storage, publication, rollback, OCI,
or WASI. `CAP_SYS_ADMIN` alone cannot provide KVM.

### WASM/WASI

Use an in-process namespace/extent provider over the logical checkpoint. It
records exact host-call mutations and ranges, so it can use the range-fast
publisher without a kernel mount only when every filesystem mutation is
capability-mediated by that provider and no writable host preopen or other
bypass exists. Identity-bearing namespace/content/metadata semantics must be
reproduced exactly or activation is rejected. Runtime capabilities may differ
by adapter; persisted semantics cannot weaken under the same `RootId`.

## Verification and recovery

Separate:

1. construction correctness, proved once by canonical hashes and commit
   receipt;
2. projection identity, checked cheaply through immutable generation,
   manifest, capability, and dependency receipts; and
3. later corruption, handled by verified reads, scheduled bounded audits,
   optional `fs-verity`, quarantine, and projection rebuild.

Exact-key reuse never recursively hashes the repository. A receipt mismatch
triggers rebuild/audit outside the activation lock.

There is at most one pending journal record per admitted operation: at most 20
for 16 admissions plus four builders, each `<=256 KiB`. Restart scans at most
20 records / 5 MiB and must finish within one second on the qualification
host or reject readiness. A terminal record is immediately folded into the
durable generation/checkpoint snapshot; optional diagnostics use a separate
oldest-first ring capped at both 20 records and 5 MiB. Ten minutes is its
maximum retention, not a promise: age, count, or bytes may evict it sooner.
Pending plus diagnostic journal storage is therefore at most 40 records /
10 MiB, and restart scans only the pending half. Recovery does not enumerate
every object or directory. Leases prevent locator/projection reclamation
while in use. All cleanup is ownership-driven and idempotent.

## Space contract

Use allocated unique physical bytes:

```text
T(t) =
    L_hot(t)
  + H_cold(t)
  + sum(U_active(t))
  + P_staging(t)
  + M(t)

D_ideal = C_current + H_unique

T_estate = T + R_remote_allocated
```

Accounting precedence is fixed: adopted files/packs count once in `H_cold`;
projection-only allocation counts in `L_hot`; a projection exposing the same
storage-owned inode adds no payload allocation; ownership transfer never
double-counts; and a sole-locator
adopted extent is not disposable until evacuated.

| Space signal | Required release gate | Release failure |
| --- | ---: | ---: |
| Mixed/no-dedup settled | `<=1.08 * D_ideal` | `>1.08 * D_ideal` |
| Many-small settled | `<=1.15 * D_ideal` | `>1.15 * D_ideal` |
| Avoidable duplicate payload | `<=1%` | `>1%` |
| Pack dead/slack | `<=2%` | `>2%` |
| Incremental publication staging | captured allocation is transferred once; additional **payload** staging `<=5% * C_capture` and is zero for metadata-only capture; fixed transaction metadata is charged to `M` under the bounds below | hidden second upper/native copy, excess payload, or missed settle deadline |
| Cold hydrate-and-adopt staging | one native `C_target` while source locators remain valid; additional **payload** staging `<=5% * C_target`; fixed transaction metadata is charged to `M` | a second native target, excess payload, or missed locator-switch/settle deadline |
| Persistent unexplained bytes | `0` | any persistent nonzero value |

`P_staging` returns to zero after success, failure, and cancellation. Native
candidate `D_proj` targets `<=4` and rejects above `8`; that performance bound
must not be mislabeled as the OverlayFS maximum. On a pinned host whose
capability receipt supports the new mount API, the test probes 499, 500, and
rejection at 501 total lowers. Correctness otherwise uses the legacy mount API
with a single serialized `lowerdir=` value; candidate `D_proj=8` must fit its
qualified option/path limit. Docker Engine `overlay2`'s separate image-layer
limit is recorded independently.

The percentage limits apply to allocated payload, not unavoidable fixed
metadata. Each transaction may additionally own at most a `256 KiB` journal
and its share of the already-declared `4 MiB` managed publication budget;
those bytes are explicit `M`, not hidden payload staging. A zero-byte
metadata-only edit therefore has a zero payload-staging allowance rather than
an impossible zero-metadata allowance.

Maintenance settlement has an enforceable deadline. Before candidate runs, controls freeze
`R_bytes` and `R_entries` as conservative lower 95% confidence bounds for
durable evacuation bytes/s and entries/s on that placement. For `B` remaining
allocated bytes and `E` reverse-manifest entries:

```text
D_calc = 2 s + 1.25 * max(B / R_bytes, E / R_entries)
D_settle = min(D_calc, 60 s)
```

If `D_calc > 60 s`, admission must split/pre-evacuate the work or reject it;
it may not silently extend the deadline. If no lease blocks retirement,
eligibility begins at `CurrentPublished`; otherwise it begins at the durably
observed release of the last blocking lease. The journal persists that
eligibility time and its derived absolute deadline. Recovery resumes
immediately, and an ambiguous/backward clock after eligibility is treated as
expired. Release campaigns quiesce old leases, so their deadline begins at
publication. At expiry, any excess duplication or retirement work is a failed
operation/qualification cell and new allocation remains backpressured until
deterministic recovery finishes or rejects it. A pre-eligibility live lease is
bounded by the active-attempt and retirement byte/count quotas and is never
reported as settled.

Disk admission uses the minimum remaining headroom across the operation's row
quota, filesystem free bytes minus the emergency reserve, the global
`P_staging` budget, locator-maintenance debt, and both settled and peak space
gates. Actual allocated bytes are reconciled during the transaction; an
underestimate pauses admission before more allocation rather than overrunning
a bound.

Specific gates:

The Firecracker rows are Phase 3 analytical budgets and falsifiers for the
adapter handoff, not measured Stage 04.6 release gates. Stage 04.6 measures
the corresponding OCI rows.

| Topology | Required physical result |
| --- | --- |
| 1,000 clean inactive forks | no per-node/private native projection or payload caused by fork; target `<=8 KiB` allocated metadata/ref; shared store and unique history count once |
| 16 clean active siblings | one shared lower/projection plus private upper/work metadata |
| 16 one-byte edits to one 1 GiB file, qualified directory path | admitted worst-case temporary upper payload can approach 16 GiB; after winner/evacuation settled gates still pass |
| One-byte/1 GiB range accelerator | target `<=128 KiB` new payload plus bounded metadata/rechunk halo |
| 100k/1M small files | streaming metadata pages/spools; no second native tree and no in-memory path set |
| Stock Firecracker projection | no retained second complete image unless it becomes an independently verified payload locator and total allocation still passes the settled gate; every image block is charged while present |
| 16 stock Firecracker siblings | one shared read-only base image plus 16 empty/private guest uppers; never 16 base images; allocated upper blocks count in `sum(U_active)` |
| Public logical ancestry prune | zero payload movement |
| Physical flatten | old leased view plus one bounded new metadata/projection build; all copied payload explicit |

A sealed native owner serving simultaneously as locator and projection counts
as one allocation and has no hidden directory link. Sparse and shared extents require actual
allocated/shared-block accounting, not logical lengths. Peak space includes
all replacement-locator bytes while the old source is retained. A live lease
may leave an accounted `Retiring` generation, but only within the hard
count/byte quotas. It may not block the logical publication response, but the
generation remains non-settled and cannot pass a `D_settle`/settled-space
gate; retirement's deadline begins when the last blocking lease drains.

## Memory and resource bounds

Qualification hard limits:

| Resource | Bound |
| --- | ---: |
| Active execution attempts | 16 |
| Pending admissions | 16 |
| Publication/projection builder coordinators | 4; they schedule the same global data workers |
| Global storage data workers | 4 |
| Maintenance coordinators | 1; consumes one of the same four data-worker slots and permits, never a fifth |
| CDC ring | `32 KiB` per chunker |
| In-flight publication chunk | one borrowed ring-backed chunk, `<=32 KiB` per data worker |
| Pack-read buffer | one `<=256 KiB` buffer per data worker |
| Hydration-output buffer | one `<=256 KiB` buffer per data worker |
| Queued payload bytes | `0`; descriptors only |
| Descriptor queue | 16 and `<=64 KiB` encoded metadata |
| Per-publication managed memory | `<=4 MiB` excluding shared index |
| Application-managed index window/working set | `16 MiB` |
| Global storage byte permits | `64 MiB` |
| Open pack tails | 4; each `<=64 MiB` payload and `<=80 MiB` allocation |
| Disk-backed sort/change spools | `<=512 MiB` and `<=1,200,000` records per operation; `<=2 GiB` / `4,800,000` records global |
| Pending retirements/evacuations | 20, shared with admitted-operation journal cap |
| Retiring locator bytes | `<=8 GiB` allocated globally |
| Unleased projection generations | 64, `<=16 GiB` allocated, `<=4,000,000` inodes |
| Merge fan-in | 8 with `<=64 KiB` each |
| Storage-owned FDs | 512 global, `<=32` per operation |
| Storage-owned mounts | 64 |
| Active leases | 4,096 |
| Per-attempt upper quota | 4 GiB and 1,200,000 inodes |
| Global active-upper quota | 32 GiB and 4,000,000 inodes |
| Backend workload-memory reservation | `<=512 MiB` per active attempt and `<=8 GiB` global; OCI cgroup, Firecracker guest/VMM, and WASI linear/runtime memory share the admission ledger |
| Aggregate storage-service RSS | `<=384 MiB` absolute and `<=128 MiB` above idle across the control plane and all builder/helper processes, excluding separately admitted backend workload processes |
| Aggregate attributable storage-service memory domain | `<=512 MiB`, measured by the qualification cgroup/domain and including RSS, mmap residency/page cache, dentry, inode, slab, and builder/helper charges without double counting |

Excess work receives deterministic backpressure. Persistent index length may
scale with repository metadata, but bounded mapped windows plus
unmap/`madvise`, or `pread`, enforce the 16 MiB application-managed working
set. Mmap bookkeeping cannot cap kernel residency, so attributable cgroup
page cache, dentry, inode, and slab memory are separately measured and gated.
The backend workload ledger is separate from storage-service RSS; all 16
attempts are admitted only when their reservations fit the 8 GiB bound.
Firecracker guest RAM mapped into the VMM is charged exactly once to that
backend reservation, not again as storage-service RSS; OCI cgroup memory and
WASI linear/runtime memory follow the same exactly-once rule. Exceeding any
hard memory bound returns deterministic `ResourceExhausted`; an OOM kill is a
qualification failure.
Stage 04.6 measures the OCI workload ledger. The Firecracker/WASI entries
freeze the Phase 3 accounting contract and are qualified when those adapters
are implemented.
Cancellation joins tasks and releases every memory reservation, permit,
mapping, FD, lease, and staging owner.

## Privilege and portability rules

`CAP_SYS_ADMIN` is the maximum capability, not a guarantee that every semantic
or backend is possible:

- changing to an OCI `config.User` UID/GID generally needs `CAP_SETUID` and
  `CAP_SETGID` in the relevant namespace unless a proved user-namespace
  mapping or the existing qualified executor establishes credentials;
- arbitrary ownership normally needs `CAP_CHOWN`;
- chmod/timestamps/POSIX ACLs on non-owned files may need `CAP_FOWNER`;
- preserving setuid/setgid through writes/chown may need `CAP_FSETID`;
- terminating another uid may need `CAP_KILL` unless the supervisor/cgroup
  owns the process;
- `chroot` needs `CAP_SYS_CHROOT` and is not the base activation path;
- device nodes need `CAP_MKNOD`;
- file capabilities need `CAP_SETFCAP`;
- immutable inode flags need `CAP_LINUX_IMMUTABLE`;
- some security xattrs need additional LSM policy/capabilities;
- FUSE needs `/dev/fuse`;
- loop/NBD/device mapper need their devices, drivers, and policy; and
- Firecracker needs KVM and `/dev/kvm`.

Firecracker jailer setup also has distinct chroot, UID/GID, namespace, and
cgroup requirements. Tap networking normally needs `/dev/net/tun` and
`CAP_NET_ADMIN`; the base qualification instead uses a no-network profile and
an adapter-owned vsock/control path where supported. A separately qualified
executor must prepare the jail, credentials, delegated cgroup, namespaces,
and file descriptors before dropping privilege, or placement rejects. A guest
change journal requires a pinned guest component and durable cursor and is
only an accelerator.

The storage service may receive `CAP_SYS_ADMIN` at most. It never grants that
capability to an OCI workload, Firecracker guest, or WASI module. Process
credentials, signals, networking, KVM, and jail setup are placement
capabilities; they never enter checkpoint identity or cause a root to be
republished with weaker semantics.

Stage 04.6 does not reduce canonical v3 semantics to suit the least-capable
adapter. It production-qualifies OCI; Firecracker and WASI qualify their
implementations in Phase 3. The root retains exact
mode, ownership, timestamp, xattr, sparse, hardlink, symlink, and supported
entry-type state. A worker capability receipt says which roots that placement
can reproduce. Missing authority or filesystem support rejects that
placement, not logical publication, and no adapter changes a root to fit the
host. This is the necessary distinction between a backend-neutral checkpoint
and a universally capable worker.
Overlay whiteouts may use a regular-file/xattr encoding only after a semantic
probe; otherwise the character-device encoding needs `CAP_MKNOD` and writable
OCI placement is rejected.

`CAP_SYS_ADMIN` also cannot create union/CoW semantics on a backing filesystem
that OverlayFS rejects. There is no portable POSIX-only way to give arbitrary
OCI programs isolated writable siblings with shared payload and no full
per-agent copy. The OCI adapter must find a qualified union facility (normally
inside the Linux OCI host/VM), select a separately qualified optional adapter,
or reject placement. It must not silently fall back to one complete lower copy
per sibling.

### Existing canonical v3 semantic contract

Stage 04.6 keeps the existing canonical records and
`RootRecordV3.required_capability_bits`; it adds no backend or profile field to
`RootId`. The contract and inherited exact-round-trip gate are:

| Semantic | Canonical checkpoint | Adapter obligation |
| --- | --- | --- |
| Paths | case-sensitive raw byte segments under the existing canonical-path limits | reproduce bytes exactly; reject a lossy or case-folding placement |
| Entry types | regular file, directory, symlink, FIFO, and device as represented by v3 | reproduce accepted types exactly; sockets remain outside the existing v3 tree schema |
| File content | exact bytes and canonical data/hole extents | exact reads and extent semantics; stored zero bytes are not silently changed into holes or conversely |
| Mode and owner | full v3 mode bits (`0000..7777`) plus canonical `u32` UID/GID | restore exactly or reject placement for missing ownership/setid authority |
| Time | canonical identity-bearing `mtime_sec`/`mtime_nsec` | exact set/read round trip |
| Symlinks | raw-byte target, relative or absolute | exact create/readlink behavior; never rewrite a target |
| Hardlinks | explicit canonical hardlink-group identity | preserve alias identity, mutation behavior, and observable link count |
| Sparse files | canonical hole extents | preserve the extent map and qualified hole behavior |
| Xattrs, ACLs, capabilities | exact canonical xattr key/value bytes; ACLs and file capabilities remain identity-bearing when encoded as xattrs | restore bytes and semantics exactly or reject placement for missing authority/policy |
| Rename/delete | complete final namespace plus backend-neutral remove/replace transitions | reproduce the final tree and same-root mutation semantics; whiteout/opaque encodings remain adapter-local |

The OCI semantic oracle includes relative and absolute symlinks, mixed
ownership, setid/sticky modes, supported xattrs including ACL/capability
namespaces where the environment admits them, sparse extents, hardlinks,
whiteouts, opaque directories, FIFO, and device fixtures. A fixture whose
host authority cannot create an entry is an explicit capability-placement
rejection, not a weakened successful materialization. WASI may retain and
enforce metadata through the EphemeralOS virtual-file provider when the
standard host-call surface has no corresponding field.

The Firecracker/WASI cells above are design and conformance requirements
carried into Phase 3, not live Stage 04.6 release tests. Phase 1 supplies
canonical root/attribution golden fixtures and adapter contract tests that do
not require either runtime.

### Zero-new-external-dependency release gate

Stage 04.6 inherits [prep §11.1](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md#111-zero-new-external-dependency-contract)
as an exact release gate. Milestone 0 freezes, per supported target and feature
invocation, the lockfile package identities/versions, enabled external
features, and the product-wide multiset of direct external manifest edges.
The final build must have zero delta in all four. A moved direct edge is
allowed only for a documented responsibility move with the old edge removed
and no count, package, version, or feature change.

No new package, CDC/hash/database/allocator/profiler/benchmark/async runtime,
Python/npm dependency, vendored or FFI library, system command/package,
daemon, sidecar, target-image helper, or build/runtime download is permitted.
A new workspace crate may use only the Rust standard library and acyclic
internal workspace edges. Qualification stores `cargo metadata --locked`
feature-resolved manifests and command/helper/download inventories for
baseline and candidate; any unexplained delta is a release falsifier.

### Mandatory host and image qualification evidence

Stage 04.6 milestone 0 freezes the release matrix required by
[`prep §11.2`](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md#112-docker-host-and-linux-image-portability).
Every row records the exact host OS/version/build and architecture, Docker
Engine/Desktop version, Linux VM/kernel/storage-driver/backing-filesystem
domain, native or named emulation path, OCI index and resolved platform
digests, `config.User`/groups/read-only state, capability receipt, semantic
oracle, time/space/memory evidence, and one classification:
`qualified`, `contract-tested`, `designed-compatible`, or `unverified`.

Required coverage includes every declared supported Linux, macOS/Docker
Desktop, and Windows/Docker Desktop release on supported amd64/arm64 paths;
pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless, and
scratch/shell-less fixtures; non-root and read-only-base cases; and native
versus supported emulated paths separately. On macOS and Windows the probe
qualifies the Docker-managed Linux VM storage domain, not APFS/NTFS or a host
bind mount by proxy. Readiness uses the adapter-owned workspace/file API and
executes no target-image helper.

Each row is also `required-release` or `informational`. A missing,
`designed-compatible`, `unverified`, or merely contract-tested
required-release row is a production portability no-go. A backend-specific
failure rejects placement and never modifies the logical checkpoint.

## Stage 04.6 milestones and rollback

### Stage 04.6 milestone 0: fix measurement before behavior

- preserve `baseline.json` and historical README results unchanged;
- add outer clocks and direct native-copy/raw-overlay/current-CAS controls;
- record read/hash/write/metadata/durability one-pass floors;
- add allocated-space, sync, dirty-byte, RSS, FD, mount, queue, inode, lease,
  and cleanup telemetry;
- discover the real CLI catalog on every campaign; and
- add crash injection and a common filesystem semantic oracle; and
- freeze the exact zero-new-external-dependency manifests and inventories;
  and
- freeze and execute the exact required-release host/image matrix, with
  missing or unqualified required rows treated as no-go.

Exit: historical cells reproduce, all real commands are classified, and no
future timer can omit required product work. The canonical v3 semantic oracle,
zero-dependency baseline, and every required-release host/image row have
pinned expected results.

Rollback: none; observability only.

### Stage 04.6 milestone 1: packed payload locator

- add immutable append packs and locator runs beside legacy chunks;
- install canonical metadata/Merkle records in immutable packed/page runs so
  neither payload nor record publication performs a per-object
  temp/write/fsync/link/unlink/parent-fsync storm;
- use grouped durability and bounded workers/buffers;
- implement the capped persistent B+tree locator index and debt
  backpressure;
- add leases, checksum receipts, recovery, and evacuation;
- implement and crash-test hydrate-and-adopt without a second native target;
- dual-read legacy payloads/records and packed runs; and
- shadow-verify canonical roots.

Exit: root equality, corruption/fault tests, bounded RSS/spool use at 100k and
1M entries, no per-record durability/link storm, zero leaks, and first
ingestion `<=1.25x` the matched one-pass floor.

Gate: `payload_pack_v1`. Rollback writes legacy format and retains pack reader.

### Stage 04.6 milestone 2: hash-and-durability receipts

- implement `AttemptSealer` epochs and command invalidation;
- connect backend change recorder with a durable cursor;
- prove writable FD/mmap/process-tree drain;
- record hashing, dirty writeback, fsync/syncfs, and interference; and
- retain synchronous full fallback.

Exit: race/fault model finds no stale accepted receipt; checkpoint-call and
mutation-to-root clocks reconcile.

Gate: `attempt_receipt_v1`. Rollback synchronously rescans.

### Stage 04.6 milestone 3: checkpoint control-plane publisher

- add multi-locator payload resolution;
- implement the single publication journal and ref-last commit;
- path-copy existing v3 tree/segment pages through streaming builders and
  cursors rather than root-sized segment vectors;
- publish in shadow against the current implementation;
- preserve exact `RootId`/`AttributionRootId`; and
- reconcile allocated-space inventory.

Exit: all corpus roots and semantics match, crash recovery is deterministic,
disjoint publications do not serialize large I/O, and a 1 GiB regular file
build/reconstruct preserves golden IDs within the declared RSS/working-set
limits.

Gate: `checkpoint_publisher_v2`. Rollback selects the legacy writer; both
readers stay available.

Shadow writes run only on isolated fixtures or under a strict byte cap. Their
duplicate allocation is charged to `P_staging`, drained after comparison, and
never used as a settled-space result.

### Stage 04.6 milestone 4: OCI projection v2

- implement the exact-parent frozen mount-recipe bundle with strict pinning,
  capability receipt, and semantic reprobe;
- implement normalized clean deltas and receipts;
- implement shallow activation and depth compaction;
- switch exact reuse to receipt validation; and
- retain a legacy reader/rebuild fallback under strict hot-projection
  count/byte/inode quotas; never retain one complete carrier per logical root.

Exit: all canonical-v3 OCI oracle cells—hardlinks including `st_nlink` during
generation overlap, rename, full mode/ownership, relative and absolute
symlinks, sparse extents, admitted xattrs/ACL/capabilities, whiteouts, opaque
directories, FIFO/devices, rebase, crash, and cancellation—either reproduce
exactly on a capable placement or return the expected explicit placement
capability error. Small publish and stored-ready meet 100x gates; warm lookup
is non-inferior; all space gates pass.

Gate: `oci_projection_v2`. Rollback resolves the same root through legacy
readers or a quota-controlled rebuild. Migration rollback allocation is
charged as peak/staging and cannot qualify as settled space.

### Stage 04.6 milestone 5: public metadata-only graph operations

- route fork, public `squash_layerstacks` logical ancestry prune, ProductAccess
  rollback, and winner selection through complete checkpoint refs;
- keep physical flatten as separately timed internal maintenance, outside the
  logical-squash response;
- cap active attempts and projections;
- implement bounded reachability/locator reclamation;
- add 64- and 1,000-operation non-closing logical-layer commit campaigns that
  exercise admission, queueing, debt, and backpressure while keeping the same
  upper and unchanged `D_proj`; and
- add separate 64- and 1,000-operation
  publish-then-`freeze_for_branch`/fork/activate campaigns that traverse every
  projection-depth compaction trigger.

Exit: 1,000 inactive nodes incur no per-node/private native projection or
payload from the fork, 32 sibling branches and 16 active attempts pass
isolation/backpressure, and cancelled losers leave zero inventory. Shared
payload-store allocation and unique logical-history payload count once.
Public logical squash and hot rollback each pass `<=20 ms p95` outer and
`<=1 ms p95` service gates; the generated ProductAccess catalog exposes both
implemented semantics. In the non-closing logical-layer campaigns every
sample includes admission through same-upper next-command readiness, passes
`<=1.070 s p95` **and `<=1.070 s max`**, and is neither rejected nor returned
with deferred readiness; `<=214 ms p95` is the preferred gate. In the separate
branch campaigns, each sample includes admission and all forced synchronous
maintenance through child readiness, reports publication and activation
independently, passes `<=1.070 s` publication and `<=99.9 ms` locally stored
projection activation gates, and has an outer maximum of `<=1.170 s`; the
preferred constituent p95 gates are `<=214 ms` and `<=20 ms`, with
`<=234 ms p95` outer reported but never used as a combined speedup claim.
Every branch campaign stays at `D_proj <=8`, reports aggregate compaction
work, and both campaign types reach zero maintenance debt within `D_settle`.
Any admission rejection or readiness deferral fails these single-client
sequential campaigns. Later backpressure caused by asynchronous maintenance
is inside the next operation's clock.

Gate: `checkpoint_refs_v2`. Rollback uses the previous ref selection service,
without changing identity.

### Stage 04.6 milestone 6: optional accelerator

Implement only the best measured range/image/lazy candidate after milestone 4
profiles identify the limiting workload. It must use the same logical roots,
semantic oracle, resource contracts, and fallback.

Exit: localized 1 GiB edits, first reads/scans/random reads/writes, peak space,
and recovery beat the qualified directory path without hidden privilege or cache
assumptions.

Each accelerator has its own gate. Probe failure or disablement falls back to
OCI projection v2.

### Stage 04.6 milestone 7: retire legacy writes

Stop new loose-object/complete-carrier writes only after a full observation
window with no required fallback. Retain readers and rebuild-by-root rollback
for at least one release.

No milestone mutates user data or existing records in place.

### Deferred Phase 3 adapter program (not a Stage 04.6 release gate)

Stage 04.6 delivers the frozen `ProjectionAdapter` contract, canonical
root/attribution fixtures, backend-neutral semantic profile, and the
Firecracker/WASI design requirements in this plan. Phase 3 will:

- implement the stock regular file-backed Firecracker image projection as one
  immutable shared base plus bounded private guest uppers, with pinned
  `target_profile`, guest-union semantic proof, userspace/builder-VM
  construction, and full-scan recovery;
- qualify a hierarchical block backend only as a separate optional
  accelerator; and
- implement the WASI direct namespace/extent projection.

Phase 3—not Stage 04.6—runs cross-backend golden-root, behavior-oracle,
16-sibling, image readback, journal-gap, allocated-space, memory, and
cold/warm activation campaigns. Its gates are adapter-specific and never
change logical identity or require an OCI checkpoint rewrite.

## Benchmark and falsification

The authoritative matrix and hard falsifiers are in
[`review.md`](review.md#benchmark-and-falsification-plan). The baseline README
defines the executable experiment.

Required workloads include:

- preserved 870.08 MiB corpus and a 1 GiB mixed corpus;
- 20k and 100k regular small files, with directories/symlinks counted
  separately, plus a stress-only 1M-entry corpus;
- 100 MiB and 1 GiB localized edits;
- offline/fake pip install/upgrade/uninstall;
- offline/fake npm install/update/removal;
- 32 sibling edits;
- 64 and 1,000 inactive nodes;
- 1, 4, and 16 active attempts;
- adversarial 1 GiB near-min-cut SeqCDC input plus a synthetic 131,072-range
  reverse-owner-manifest case;
- candidate `D_proj` 0/1/4/8; legacy/control total lower count
  32/64/128/499/500; capability rejection at 501 total lowers;
- 64 and 1,000 non-closing logical-layer commits, timed from submission through
  durable ref and same-upper next-command readiness, including admission,
  queueing, backpressure, forced synchronous work, p50/p95/max, and later
  maintenance-induced delay;
- separate 64 and 1,000 publish-then-`freeze_for_branch`/fork/activate
  operations including every depth-compaction trigger, independently reported
  publication/activation spans, outer p50/p95/max, and aggregate maintenance
  work;
- public logical `squash_layerstacks` versus separately timed physical
  flatten;
- rollback and winner reactivation on warm and cold workers; and
- crash, cancellation, corruption, `ENOSPC`, and restart at every commit
  boundary.

Discover the public surface using:

```text
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo run --quiet -p sandbox-cli \
  --features manager,runtime,observability \
  --bin sandbox-catalog-export
```

Benchmark every exported public operation-and-route tuple across manager,
runtime, and observability. Observability gets integrity/overhead cells,
including both currently exported routes for `snapshot` and `resources`, and
must prove it does not mutate lifecycle or storage state. At the
pre-Stage-04.6 baseline, fork, committed checkpoint, historical-root
materialize/reactivate, and committed rollback are component-only; label
public CLI cells blocked until the catalog exposes them. Stage 04.6 release
requires the rollback ProductAccess cell and changed logical
`squash_layerstacks` contract in the generated catalog. Do not invent command
names or substitute
`create_sandbox --count` for fork.

The architecture is disproved if any correctness/root/backend invariant fails,
if small post-setup publication or the defined combined small
mutation-to-root cell exceeds `1.070 s p95`, if stored-projection readiness
exceeds `99.9 ms p95`, if first ingestion exceeds `1.25x` its
matched one-pass floor or performs an avoidable extra complete payload pass,
or if a speedup label fails its matched-current divisor. It is also disproved
if public logical squash or hot rollback exceeds `20 ms p95`, if hot logical
operations scale with root size/depth, if either non-closing sequence exceeds
`1.070 s p95` or `1.070 s max`, changes `D_proj`, rejects a submission, or
returns before same-upper readiness, or if either branch sequence exceeds its
`1.070 s` publication, `99.9 ms` local activation, or `1.170 s` outer maximum
gate, exceeds `D_proj=8`, rejects/defers readiness, or misses `D_settle`.
It is likewise disproved if forced work or maintenance-induced backpressure
is omitted, deferred lazy costs are hidden, warm lookup regresses, settled
space gates fail, a bound leaks, or a required correctness path depends on an
undeclared device/filesystem/kernel feature.

## Phase 2 and Phase 3 acceptance

For Phase 2 parallel MCTS:

- inactive forks add refs/unique logical history but no per-node native
  projection or payload;
- fork, rollback, and public logical squash are payload-free;
- active siblings share immutable lowers and have isolated private writes;
- final branch-head CAS is the only serialized selection step;
- winner activation is projection selection/build, not logical
  reconstruction; and
- loser cancellation returns all inventory.

For the Phase 3 handoff (design contract only in Stage 04.6):

| Adapter | Physical view | Change evidence | Correct fallback |
| --- | --- | --- | --- |
| OCI | normalized directory delta, complete directory, optional image/lazy projection | sealed whole files; optional proved extents | hydrate-and-adopt, then activate only through a qualified union facility; otherwise reject writable placement |
| Firecracker | one stock regular file-backed read-only base plus bounded private guest upper per active VM; optional qualified hierarchical block backend; optional VM snapshot | backend-owned CoW disk extents plus guest semantic journal, with full semantic scan after a gap/crash | construct and verify regular image from logical root; reject execution without KVM/qualified guest union |
| WASI | in-process namespace and extent provider | exact provider-mediated host-call mutations/ranges; no writable bypass | direct logical traversal |

The logical checkpoint and attribution identities remain identical across all
three.

## Completion rule

Stage 04.6 is ready only when:

1. historical evidence is preserved and expanded controls are sound;
2. first ingestion reports the absolute 100x/500x comparison and meets
   `<=1.25x` its matched one-pass read/hash/write/metadata/durability floor;
   the one-time setup is not a steady-state speedup gate when that floor makes
   the absolute ceiling physically impossible;
3. root and attribution golden vectors remain unchanged;
4. post-setup small publication and cold-page-cache activation of a locally
   stored compatible projection meet at least the 100x gates with complete
   boundaries; true empty-worker placement is reported separately against its
   direct copy/transfer floor; the small combined mutation-to-root and
   immediate receipt-miss cells also pass;
5. any 500x claim meets `<=214 ms` publication or `<=20 ms`
   workspace-ready and the `matched_current/500` rule;
6. exact reuse is metadata-bound and warm lookup is non-inferior;
7. deferred access, scan, random-read, and first-write costs are reported;
8. every settled/peak space and resource bound passes;
9. crash/cancellation/restart and semantics qualification pass;
10. Phase 2's 1,000-node/32-sibling/16-active campaign passes;
11. every required-release OCI host/image evidence row is qualified; and
12. every admitted Stage 04.6 root passes the OCI semantic oracle, contains no
    backend-specific identity, and matches frozen backend-independent golden
    fixtures. Phase 3 must demonstrate that each adapter consumes those
    fixtures without schema or identity migration;
13. public logical `squash_layerstacks` and hot rollback each meet
    `<=20 ms p95` outer and `<=1 ms p95` service gates, while cold rollback is reported
    separately against its physical floor;
14. the 64- and 1,000-operation non-closing logical-layer campaigns keep
    `D_proj` unchanged, include admission through same-upper readiness, pass
    `<=1.070 s p95` and `<=1.070 s max`, and never reject/defer; the separate
    branch-projection campaigns include compaction tails, stay at
    `D_proj <=8`, pass their `1.070 s` publication, `99.9 ms` activation, and
    `1.170 s` outer-maximum gates, and both campaign types settle by
    `D_settle`; and
15. the zero-new-external-dependency manifest/feature/edge/helper/download
    comparison has exactly zero unexplained delta.

Missing an optional 500x stretch target is reported honestly. A correctness
error, hidden deferred cost, unbounded path, unexplained retained byte, or
architecture-specific logical identity is a release blocker.
