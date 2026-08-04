# System requirements

> Status: **Accepted**
> Sole authority: correctness gates, prohibitions, finite resource profile,
> storage-retention accounting, overload behavior and acceptance evidence.

A sandbox points to one complete immutable state; publication builds or reuses
content-addressed objects and conditionally moves that pointer. Exact
reachability maintenance reclaims physical bytes no retained pointer can
reach. Structural sharing is the only logical copy-on-write model: no state
requires a parent layer, and no squash operation exists.

All numeric values below are **requirements**, **analytical bounds** or
**targets**, as labelled. None is an achieved result unless a cited project
measurement says so.

## Hard gates

| Gate | Required result |
|---|---|
| Complete canonical identity | The same supported filesystem and attribution facts produce the same backend-neutral `StateId`, and every `StateId` names one complete state. |
| Integrity | Every object is checked by expected kind, format, canonical length and BLAKE3-256 before use. |
| Atomic visibility | A reader observes the old complete selected state or the new complete selected state, never a mixture. |
| Durability | Every immutable dependency is durable before the one selecting `HEAD` becomes durable and before acknowledgement. |
| Exact replay | A retained authenticated request returns its exact recorded outcome; an expired request never executes. |
| Isolation | Committed views are read-only; each mutable session has one private writable adapter allocation. |
| Concurrency | Exact origin and selected-basis conditions prevent lost updates, ABA and stale maintenance installation. |
| Exact retention | Only the closed semantic-root schema retains canonical content; physical dependency closure cannot lose a live Full base, candidate or reader. |
| Bounded resources | Managed RAM, cgroup memory, workers, queues, FDs, disk, inodes, readers, owners, roots and maintenance space are finite and admitted before use. |
| Portability | Canonical identity and public lifecycle behavior contain no backend locator, runtime layer, mount, snapshot or process state. |
| Fail closed | Missing, corrupt, unsupported, over-limit or ambiguous selected state is not served and is never replaced by an older selection. |

Failure of one gate rejects an implementation regardless of timing or disk
benchmarks.

## Exact architecture and vocabulary

The production design is the **Portable Merkle State Store**. “CAS” is only an
adjective for content-addressed objects. “MPLA” refers only to the historical
Stage 4.6 proof of concept.

| Item | Required count or choice |
|---|---|
| Domain components | **4**: Canonical State, Durable Store, Lifecycle, Backend Adapters |
| Shared services | **1**: Resource Admission, volatile and permit-only |
| Workspace Engine components | **0**; the retained file documents workflows |
| Project-owned custom mechanisms | **6**: C1, C2, C3, S1, S2, S3 |
| Selected Catalog roots | **1** |
| Mandatory selectors | **1** `HEAD` |
| Catalog arenas | **2**: one Selected and one mutually exclusive Auxiliary |
| Logical layers / squash operations | **0 / 0** |
| Persistent application caches | **0** |

The six custom mechanisms are exactly C1 canonical compressed
Patricia/Merkle directory, C2 `ContentTree-v1` bounded content-defined Merkle
sequence, C3 deterministic whole-run attribution tiling, S1
fixed-purpose immutable CoW B+ Catalog, S2 single-`HEAD` dependency-first
commit/fail-closed recovery, and S3 `AlignedSpliceDelta-v1`. Resource
Admission, lifecycle transitions, adapter workflows, external sorting,
GC/repack policy and qualification suites are not additional custom
mechanisms.

The Catalog has exactly these eight compile-time-closed namespaces:
`Sandbox`, `Session/Mutable`, `Session/Terminal`, `Checkpoint`,
`CheckpointPin`, `Receipt`, `OwnerSlot` and `ObjectCatalog`. There is no
separate state, session-registry, history, refcount, live-set, deletion-
tombstone or delta-search namespace.

The 16 `OwnerSlot` keys are statically partitioned, and the key—not a stored
purpose field—selects the grammar and non-borrowable quota. Slot `0` is
maintenance-only: `Empty | Build {owner_nonce}`. Slots `1..15` are
foreground-only: `Empty | Build {owner_nonce} | AdapterClose`. The nonce
prevents slot-reuse ABA; a value or artifact illegal for its lane fails closed.
S2 selects the required empty lane before any file is created. A 16th
simultaneous foreground owner receives bounded `RetryLater`; maintenance never
competes for a dynamically chosen slot or priority queue.

The selected row owns every file subsequently created beneath its fixed
contained directory outside `packs/`, so no pack-list manifest, durable build
reservation, per-pack Catalog mutation or observed-locator pin exists. The
live permit owns the reservation; recovery reconstructs actual allocation and
aborts every Build. Per-file canonical framing plus lane-specific hard
byte/inode quotas replace duplicate manifest fields. Recovery streams each
selected or nonempty slot directory within those quotas, never builds a
resident inventory, and cleans or fails closed before readiness. Maintenance
selects slot `0` **before** capturing `MaintenanceBasis`. While slot `0` is
selected, existing foreground builders may finish private staging, synchronize
and close resources, then wait, but no foreground lane may be granted and no
foreground S2 mutation may finalize. Waiters hold zero managed buffers, FDs or
workers. `AdapterClose` that crossed irreversible disposal completes after the
bounded maintenance fence. Slot `0`'s directory quota/reserve is dedicated and
cannot be borrowed by foreground work.

Only these four version terms are permitted:

| Term | Meaning and advance rule |
|---|---|
| `StateId` | `ObjectId(FilesystemRoot)`; changes only when canonical complete-state bytes differ and is not monotonic. |
| `HeadRevision` | Per-sandbox ABA token, initially `0`; increments on every `Published` decision including identical content, every actual rollback, and every `Committed` fork commit. |
| `StoreSequence` | Global selected Catalog commit sequence; advances for every selected typed, receipt-only or maintenance commit. |
| `ArenaId` | Physical Catalog arena identity; changes only when S2 selects the other arena. |

`AlreadyCurrent`, `NoChanges`, `ParentDiverged` and all other no-head-change
outcomes leave `HeadRevision` unchanged. Overloaded “generation” terminology
is not used.

## Optimization and claim discipline

Each optimization has one primary label:

| Class | Optimizes | Required evidence |
|---|---|---|
| `ARCH` | Authority, coupling and state transitions | Owners, dependencies, durable facts or transitions removed |
| `ALG` | Passes, ordering, lookup and asymptotic work | Worst-case bound and adversarial corpus |
| `TIME` | Latency, throughput, CPU or I/O time | Named workload, matched baseline and percentile/throughput |
| `DISK` | Allocated bytes, staging, writes or inodes | Allocation-rounded byte/write/inode accounting |
| `MEM` | Managed RAM, queues, workers or FDs | Permit peaks plus process/cgroup high-water |

Numbers must be labelled **analytical bound**, **project measurement**,
**external measurement**, **target**, **estimate** or **hypothesis**.
Correctness, durability, portability, replay and resource safety remain hard
gates, never weighted tradeoffs. A cache-on result cannot support the
cache-off baseline.

## Exact prohibitions

- No reflink use, including an optional fast path.
- No FUSE use.
- No added administrative or storage-management capability, including
  `CAP_SYS_ADMIN`. Ordinary least-privilege workload capabilities remain
  runtime policy and cannot expose canonical storage or bypass fencing.
- No SQLite or other database engine; no WAL, MVCC, generic key/value service,
  arbitrary keyspace or hidden background maintenance.
- No logical layer stack, parent-applied state delta, squash, autosquash,
  squash-triggered remount or durable publication history.
- No correctness, identity, retention, quota or recovery dependency on
  OverlayFS, a Docker snapshotter/storage driver, filesystem snapshot, mutable
  hardlink sharing, a particular host filesystem, VM snapshot or memory-backed
  workspace.
- No repository-sized resident map, memory mapping, index, path/object/task
  set, queue payload, reverse map, refcount ledger or cache.
- No writable canonical object or cross-workspace writable sharing.

Permitted runtime-internal overlay or snapshot acceleration is invisible to
the Store and public lifecycle. Disabling it must not change facts, identity,
retention, quota results, publication or recovery. Docker’s private storage
driver may exist as a runtime implementation detail; it is never the Store or
workspace-sharing mechanism.

Hardlinks reproduce one real link group only inside one private workspace.
They never share writable file data with the immutable Store or another
workspace.

## Canonical complete-state requirements

The sole state formula is:

```text
ObjectEnvelope = canonical([versioned_type_tag, payload])
ObjectId       = BLAKE3-256(ObjectEnvelope)
StateId        = ObjectId(FilesystemRoot)
```

The one unsigned `versioned_type_tag` binds kind and format version; the
definite-length two-field envelope and end-of-input check make a separate
payload length redundant. A decoder verifies the expected tag, exact schema,
canonical re-encoding and digest.

Canonical facts include raw relative path bytes, directory/regular/symlink
type, explicit hardlink topology, logical file length, exact DATA/hole extents,
mode, uid, gid, nanosecond mtime, strictly ordered supported xattrs, raw
symlink target, and coalesced attribution for every surviving fact. Host inode,
mount, allocation, backend, OCI layer, process and physical locator facts are
excluded. Unsupported or unrepresentable facts fail before execution or
publication.

Canonical caps are hard:

| Quantity | Requirement |
|---|---:|
| Basename / encoded relative path | `<=255 B / <=4096 B` |
| Payload FastCDC profile | pinned `fastcdc` 4.0.1 `v2020`, normalization 2, original tables/seed 0, min/target/max `8/16/32 KiB` |
| C2 encoded entry / entries per node | `<=64 B / <=512` |
| C2 canonical node payload | `<=16,512 B` |
| C2 root level | `<=7`, eight total levels |
| C2 builder | eight open nodes = `132,096 B`; with one chunk and scratch page = `181,376 B` |
| C3 records per generation/output | `N_C3_record_max = 2,097,152`; before allocation require checked occurrence, fragment-bound and output-bound counts each `<=N_C3_record_max`, and recheck every emission |
| Direct typed child references per canonical object | `<=512`; excess encode/decode fails `CanonicalLimitExceeded` |
| Complete encoded canonical object | `<=65,536 B`; checked before hashing, packing and decoding |

For C3, the one count cap applies independently to checked
`c_old+c_new`, `c_match+s_old` and `c_frag+(c_new-c_match)`. The job reserves
the complete two-generation maximum over 50-, 16- and 48-byte records before
creating scratch and rejects `CanonicalLimitExceeded` before allocation when
any bound exceeds `2^21`. Per-emission counters repeat the check. One cap is
sufficient because the three external sorts reuse the same two generation
files and one control file; separate occurrence/fragment/output knobs are
forbidden redundant configuration.

C2 boundary input, prefixes, empty form, single-child collapse and golden
vectors are normative in
[Canonical State](components/canonical_state.md#frozen-c2-format-profile).
Expected local resynchronization is not a deterministic bound: adversarial
boundary grounding remains `Theta(n)` and must be admitted.

Every public state is:

```text
StateId -> FilesystemRoot -> complete filesystem with integrated per-entry and per-file attribution
```

No parent state is required to interpret it. Unchanged chunks and tree nodes
share identity. S3 may encode one complete canonical DATA object physically
but cannot alter its bytes, `ObjectId`, graph edges or `StateId`.

## Lifecycle and API requirements

The public surface is exactly the
[18 lifecycle and 8 runtime methods](api_methods.md). It has no backend,
archive-format, locator, layer, generic `ref` or generic `target` selector.

- Each mutable session stores one immutable exact origin pair
  `(StateId, HeadRevision)`, one creation-bound authenticated `ActorId[32]`,
  and one private adapter allocation. The accepted
  `create_workspace_session` request snapshots the actor; capture, metadata
  ownership and C3 read only that stored value. Publish retries never consult
  ambient caller identity, and Terminal transition drops the actor with the
  origin/reservation.
- `Session/Mutable` presence, including `OPENING` and `ACTIVE`, is the only
  durable non-quiescence proof. Session insertion and prefix absence use the
  same per-sandbox gate.
- Publication leaves the durable row `ACTIVE` while a transient owner fences
  and captures. There is no durable `PUBLISHING`.
- Exact origin match selects the complete candidate, moves the row to
  Terminal/`PUBLISHED`, increments `HeadRevision` and records the exact
  `Published` receipt. The Terminal status itself fully determines the outcome.
- Origin mismatch selects no candidate locator, leaves the head unchanged,
  moves the row to Terminal/`CONFLICTED` and records the exact
  `PublishConflict` receipt.
  It never rebases, merges or retries against the newer head.
- A conflicted allocation is fenced, read-only and self-contained. V1 admits
  only adapters that prove it remains readable without canonical origin
  objects; an adapter that cannot prove that property is unsupported.
- Checkpoints name committed complete state only. Creating one may coexist
  with active sessions and copies no payload at creation.
- Fork, rollback and sandbox destroy require target quiescence. Fork commit
  requires immediate parent and child quiescence; gates are acquired in
  ascending sandbox-ID order.
- A fork binds immutably to one immediate-parent checkpoint. Its
  `CheckpointPin` is derived membership, not a counter or content edge.
  Parent and child remain writable/detached, nesting is allowed and destroy
  never cascades.
- Rollback creates no history. `AlreadyCurrent` does not advance revision; an
  actual rollback does.
- Fork commit evaluates exactly: `P=C -> AlreadyCurrent`,
  `C=B -> NoChanges`, `P=B -> Committed` with parent revision increment,
  otherwise `ParentDiverged`.

Session destruction is crash-discoverable:

1. one S2 commit conditions on the exact Mutable or Terminal row and claims
   an existing
   `OwnerSlot/AdapterClose {session_id, expected_row_digest,
   request_identity}`; the selected row remains the sole source of its
   allocation handle;
2. Lifecycle fences and drains all admitted adapter work;
3. the adapter idempotently disposes the allocation and synchronizes the
   destructive transition;
4. one final S2 commit rechecks and deletes the exact row, stores
   `Destroyed` or `AlreadyClosed`, and clears the intent.

The row stays selected through irreversible disposal.
Recovery fences and completes every selected close intent. An unused intent
may be cleared only before irreversible disposal. This is one typed variant of
the existing 16 `OwnerSlot` values, not another namespace or mechanism. There
is no `CLOSED` row, tombstone or per-session history.

## Exact replay

The replay profile is fixed:

The existing `Receipt` namespace has two closed key/value subtypes; no ninth
namespace, replay ledger or generation field exists:

```text
ReceiptControl(lane) -> next_sequence:u64                 # exactly 16 rows
ReceiptSlot(lane, sequence mod 64)
  -> {request_digest[32], bounded_exact_result}           # exactly 1,024 rows

16 authenticated lanes
x 64 retained sequence slots per lane
x <=512 B complete canonical framed ReceiptSlot value
= 1,024 exact results
<=512 KiB slot payload before Catalog page overhead
```

Every control row starts at `next_sequence=0`. A new request is accepted only
at exactly `next_sequence`; a future gap is a typed transport rejection. The
retained window is `[max(0,next_sequence-64), next_sequence)`. A retry in that
window addresses exactly one modulo slot, verifies its `request_digest`, and
returns its exact result without reevaluating current state. An older request
returns `ReplayExpired` and never executes. Each S2 commit atomically writes
the semantic effect (if any), the modulo `ReceiptSlot`, and
`ReceiptControl.next_sequence+1`. A slot stores no sequence, generation,
low-water mark or duplicate lane field. Every post-acceptance semantic outcome,
including a no-effect error, follows this rule. Preaccept malformed,
authentication and admission rejections may remain unstored. IDs inside
receipts are inert and never content edges. The 1,024 slots remain durable and
cache-off; only the one consulted control/slot working set may be resident.

## Durable Store and publication

One fixed-purpose immutable CoW B+ Catalog root contains every selected
lifecycle fact and `ObjectCatalog` locator. It is a purpose-built closed index,
not a database. The mandatory checksummed `HEAD` contains exactly
`{type_tag,StoreSequence,ArenaId,committed_arena_length,checksum}`. With
`P=16 KiB`, require the committed length aligned and `>=P`, then derive the
only `CatalogRoot=(ArenaId,committed_arena_length-P)`. Its versioned tag replaces
a separate format file; no serialized root offset, store ID or selected-pack
list exists. Recovery derives dependencies by streaming that root. Exactly one
arena is Selected; Auxiliary is replacement space, never an acknowledged
fallback.

The selected prefix contains only complete S1 pages. Every selectable sparse
or dense build emits children bottom-up and exactly one fresh root as its final
page; no selected trailer, control record, padding, hole or later page follows
it. Child references are P-aligned, name the same arena and lie below the root.
Candidate writes begin at the selected committed length, never physical or
preallocation EOF; `O_APPEND` is forbidden so crash tails can be overwritten.
Every StoreSequence-advancing S2 commit changes Catalog data and emits a fresh
root. Retained replay, preaccept rejection and selector-only recovery do not
advance it. The initial empty Catalog is one valid root page at length `P`.

S1 requirements are 16 KiB pages, half-full non-root occupancy, height
`<=8`, immutable verified pages, sparse sorted path-copy, dense sequential
build and total two-arena physical bytes `<=4C_max`. `C_max` is the configured
full-occupancy byte capacity of one complete admitted Catalog and is never
recomputed downward from current live rows; one half-full-bounded arena is
`<=2C_max`. Cache-off lookup is `Theta(H)`; sparse `K`-record update is
`O(KH)` pages worst case; dense construction is `Theta(N)` ordered I/O.

Every S1 internal-child entry contains a checked `u32
subtree_record_count`. Leaf count equals the exact unique-record count; parent
count equals the checked sum of child counts. Overflow, disagreement, wrong
key/namespace/kind or rank outside the exact range fails closed. For a captured
root, preceding-sibling counts plus the leaf slot define a basis-local ordered
rank. Because `ObjectCatalog` is one contiguous key range, subtracting its
lower-bound rank maps its records bijectively to `[0,N_object)`. This is S1
order-statistic metadata, not a new mechanism, version, refcount or live-set
ledger. Its encoded width is included when internal fanout, the height-eight
capacity proof, `C_max` and `4C_max` are frozen and qualified.
Admission requires `N_catalog_record_max < 2^32` and therefore
`N_object_max < 2^32`; checked arithmetic may be wider, but every stored count
and basis-local rank is `u32`.

Publication’s portable bounded-memory baseline uses two stable fenced source
passes and one disk-backed distinct-object classification:

1. pass 1 reads/describes/hashes at most `B_scan` non-hole source payload
   bytes and emits `U_candidate`;
2. classify every distinct object exactly once into disjoint `U_reuse` and
   `U_missing` streams;
3. pass 2 groups source descriptors by interval and Store reads by locality,
   rereads at most `B_scan` payload bytes, reconstructs and exactly compares
   every reused canonical object once, and emits every missing object once.

Let `C_reuse` be reused canonical comparison bytes, `P_reuse` the actual
physical selected-Store reconstruction reads, and `P_new` physical missing-
object writes including framing. Exact accounting is source reads
`<=2B_scan`, canonical comparisons `=C_reuse`, selected reads `=P_reuse`, and
new physical writes `=P_new`. Neither comparison term is bounded by
`B_scan`: metadata exists for zero-payload trees, and Delta reconstruction may
read its Full anchor. `Delta=C_candidate-C_reuse` is canonical information,
not physical writes. Changed stability tokens, short reads, unsupported facts
and any same-ID kind/length/content mismatch abort before selection.

S2 durability order is exact:

```text
validate complete claim and select one empty OwnerSlot directory
-> write immutable objects within that owned staging directory
-> seal, verify, rename into the installed directory and sync dependencies
-> write immutable Catalog pages
-> sync the arena and every selected dependency
-> write and sync complete HEAD.tmp
-> same-filesystem rename HEAD.tmp to HEAD
-> sync the containing directory
-> acknowledge the recorded exact result
```

The `HEAD` directory synchronization is the commit/acknowledgement point.
Recovery keeps readiness closed and holds every selected Build plus its
reconstructed aggregate allocation charge. It first validates the one
mandatory `HEAD`, derives and validates the final aligned root and its complete
same-arena below-root closure, and validates closed rows; then streams
the complete selected Catalog/installed-pack census, verifies every selected
frame and Full dependency, and synchronously unlinks plus directory-syncs every
installed pack with zero selected rows. Only after that custody proof may it
clean every fixed owner directory, synchronize each deletion, exact-clear the
Build rows, release the reconstructed charges and open readiness. It fences
stale adapters and fails closed on missing, corrupt or ambiguous selected data.
It never elects Auxiliary or an older `StoreSequence`, and it needs no per-pack
manifest.

The storage medium must qualify exclusive ownership, durable file sync,
atomic same-filesystem replacement, durable create/rename/unlink directory
sync, stable reopen, conservative byte/inode allocation rounding and reserve
measurement. Failure keeps the Store unavailable or returns
`UnsupportedEnvironment`.

## Sealed-pack format

One pack has exactly this grammar and no footer:

```text
SegmentHeaderV1 = b"PMSSPK1\0"                            # exactly 8 B
RecordHeaderV1  = ObjectId[32] || stored_len_minus_one:u16 # exactly 34 B
PackSegmentV1   = SegmentHeaderV1 || 1..n (RecordHeaderV1 || payload)
```

Payload length is `stored_len_minus_one+1`, hence `1..65,536` bytes; canonical
envelopes and Delta payloads are nonempty. `ObjectCatalog` is the sole codec
authority: `Full {segment_id,offset:u32,framed_len:u32}` or
`Delta {segment_id,offset:u32,framed_len:u32,base_id}`. The record header stores
no codec, base, canonical length, checksum, kind or locator copy. For every
locator, `offset` starts its record header and `framed_len=34+stored_len`.
Full canonical length equals stored length. A Delta target length is derived
from its verified equal-length Full base and its checked `u16` prefix/suffix
fields; reconstruction must verify canonical DATA framing and target
`ObjectId`.

`P_pack_committed_max=64 MiB` includes the eight-byte header and every frame;
output frames therefore fit in `64 MiB-8 B`.
`P_pack_alloc_max=A(P_pack_committed_max)<2^30`, every offset/end calculation
uses checked `u64`/`u128` arithmetic before narrowing, and a segment has at
least one frame. `SegmentId=BLAKE3(pack-domain || exact entire file bytes)`;
only the filename and locator repeat it. Admission and recovery fstat the exact
length, verify the full hash, then parse from the signature to exact EOF.
Short, trailing-malformed, zero-frame, bad-signature, over-cap, overlapping or
overflowing input fails closed. A trailing syntactically valid frame that no
selected row names is valid dead charged space, not hidden metadata.

## S3 physical encoding requirements

`AlignedSpliceDelta-v1` applies only to canonical DATA objects. Its sole base
candidate is the exact same logical interval in the session origin. If that
origin locator is Delta, the candidate reuses its verified Full anchor.

| Rule | Requirement |
|---|---|
| Target and base canonical lengths | Equal and `<=32 KiB` |
| Dependency | `base_id` resolves through the reader's captured Catalog root to a Full locator; depth exactly one |
| Selection economics | framed Delta `<=floor(framed Full/4)` and saves `>=1 KiB` |
| Decode | Read one Full base plus one Delta at most; verify target kind, length and BLAKE3 |
| Scratch | exactly one 98,304-B slab: 32-KiB base, 32-KiB target, 16-KiB Delta I/O and 16-KiB controls |
| FDs | exactly 3: Catalog, input/base pack and candidate/replacement pack |
| Search state | none: no global search, reverse map, window, chain or cache |

Base selection is identity-bound, not locator-pinned. Hold one bounded
`ReadSlot`, resolve and verify a Full `base_id` through that captured root,
compute and verify the bounded candidate, place only the candidate/output pack
under durable `OwnerSlot` custody, then release the slot. At the final shared
publication/maintenance gate, re-resolve every classified reuse and Delta base
in the current selected root. Commit a Delta only when that root still selects
a structurally valid Full `base_id`; atomically retain that Full row, select
the target Delta and transfer candidate custody in the same S2 commit. The
selected Delta stores `base_id`, never a physical base locator. No payload
read, encoding or bulk verification occurs in the serialized gate.

If any classified `REUSE` object or Delta dependency has vanished, leave the
gate. While the private workspace remains fenced and the same foreground Build
is selected, join all producers/readers; delete and directory-sync the entire
classification cursor, every candidate pack and all scratch; then rerun the
complete two-pass capture against the current Catalog under the same permit and
owner nonce. A local REUSE-to-Full or Delta-to-Full patch is forbidden because
it would use bytes after the classification proof that admitted them was
discarded. One recapture is allowed per request. A second invalidation performs
the ordered abort/clear and returns typed transport `RetryLater`; the session
remains `ACTIVE`. No candidate pack is installed before this revalidation.

Pass-two `MISSING` is also only a captured-root classification. During final
Catalog streaming, look up every candidate ObjectId again. A `REUSE` keeps its
structurally valid current selected row. A candidate locator keeps an already
selected structurally valid exact row when one now exists, otherwise it selects
the staged locator; it never replaces an existing Full row with a staged Delta.
Candidate frames are written in global ObjectId order, so each segment occupies
one contiguous cursor interval and only one `selected_count` is needed for the
current segment. Install and sync a segment only when that count is positive;
delete and directory-sync a zero-selected late-deduplicated segment while the
Build remains selected. A mixed segment may contain dead duplicate frames,
which remain charged for later repack. Here “structurally valid” means a closed,
invariant-valid selected Catalog row whose payload was proved at admission; no
payload I/O is added to the gate.

Abort and supersession first fence/join the producing worker, then unlink every
file while its OwnerSlot directory is still selected, synchronize that
directory, clear the row through S2, and finally release byte/inode charges.
An empty selected directory is valid and crash-recoverable. At successful
selection, only nonempty selected candidate segments are renamed and
synchronized in the installed directory before HEAD; the same S2 root selects
every needed staged locator or already-selected exact row and clears the slot.
A live failure before HEAD must unlink and directory-sync every known newly
installed destination (or stream the complete installed census) before
clearing the Build and returning. A crash before HEAD leaves only
self-verifying unselected installed orphans, which recovery synchronously
unlinks before readiness.

S3 requires equal canonical lengths within a base group, so all corresponding
Full record frames have length `F` and every Delta frame has `D<=F/4`. The only
frame-inefficient shape is a non-logically-live base with one logically-live
Delta target: `F+D>F`. A dead base with `k>=2` targets uses at most
`F+kF/4<kF`; an independently live base is already required. The grouped
`DeltaEdgeV1 {base_id,target_rank:u32}` stream therefore needs only a checked
count, not byte-size fields or a cost solver. Emission already knows the
basis-local target rank. A group resolves `base_id` once and exact-selects each
rank, verifies that row is the unique Delta naming that base, and rejects a
duplicate rank/target. One normalization-mode pass selects
dead-base singletons in key order up to the `64 MiB-8 B` output-frame budget;
other groups retain the anchor.

Completed normalization is no larger than Full-only in **record-frame bytes**.
It makes no per-group filesystem-allocation claim because unrelated frames may
share a pack and one group may span packs. Every real pack allocation remains
charged through exact `PackAlloc`; the separate pack census and physical
repack policies control allocation-rounded bytes.

## Semantic retention and maintenance

The semantic root schema is fixed:

```text
Rsem = every live Sandbox StateId
     U every Checkpoint StateId
     U every Session/Mutable origin StateId
```

Every Terminal field, receipt content, allocation handle, provenance ID and
`CheckpointPin` is inert for content reachability. V1 requires every
conflicted private allocation to be self-contained and readable; there is no
conditional terminal edge. Physical custody barriers are exactly the 16
fixed `OwnerSlot` directories, 64 bounded `ReadSlot` epochs and one
maintenance/retirement epoch; none changes semantic liveness.

Every GC/repack, normalization and dense rebuild first selects
`OwnerSlot[0]=Build {owner_nonce}`. That dedicated row is the global
non-maintenance S2 mutation fence; no purpose field, dynamic owner search,
priority queue, lock namespace, change log, refcount or catch-up structure
exists. Store then captures
`MaintenanceBasis{StoreSequence,ArenaId,committed_arena_length}`. The Store derives
`CatalogRoot=(ArenaId,committed_arena_length-P)` and itself scans
the closed semantic namespaces from an ordered cursor over that exact
that root; callers cannot submit a root list, and root rows and
`ObjectCatalog` locators cannot come from different bases. Logical traversal
closes only canonical objects. A separate physical census classifies every
selected locator, required Full anchor and installed sealed PackSegment.
OwnerSlot staging directories are separately charged and never enter victim
selection. ReadSlots pin selected retirement epochs rather than contributing
object records.

While that exact Build row remains selected, every new foreground-slot grant
and non-maintenance S2 mutation receives bounded `RetryLater`; reads,
materialization and already admitted private edits continue. Foreground
builders already holding slots may finish staging, close/sync resources and
wait without managed memory, FDs or workers. Replacement packs and the complete Auxiliary Catalog
are built, verified and synchronized before the final selector. Store streams the complete
basis/Auxiliary relation in `Theta(N_object)`. Every basis row is classified
exactly once as an identical keep, a trace/census-proven deletion of its exact
old locator, or an exact old-to-verified-new replacement;
extra/unclassified Auxiliary rows are rejected. The resulting bounded proof
summary binds the exact basis, Auxiliary root/length and synchronized
dependencies. The final HEAD/root selector is `O(1)` in repository size, but
the write-side pause explicitly spans trace, two external sorts, optional
rewrite, dense validation and selection: bounded
`Theta(N_object+N_pack+X_live)`. Production must freeze and pass a maximum
pause/fairness gate at `C_max` under 1/4/8/16/32/64 active sessions. A basis
mismatch is impossible without corruption while the fence holds; it aborts
with synchronized cleanup and never blind-rebases or loops.

Accounting is conservative and has no refcount:

- every newly selected physical and Catalog allocation, every unselected
  candidate, and every `OwnerSlot` byte and inode remains charged;
- removing a root gives zero speculative byte or inode credit;
- the only credit point is an exact-basis trace, successful replacement when
  needed, joined cancellation/drain of every old-epoch reader cursor and FD,
  completed unlink, and synchronization of every affected parent directory;
- exact trace is triggered by charged-allocation high-water, semantic-root
  retirement and before a final
  `ResourceLimitExceeded(storage_retention)` decision;
- `RetryLater` is permitted for retention pressure only while a bounded pass
  can still make progress.

### Exact bounded trace

Let `A(x)` be the checked allocation-rounding function. Deployment derives and
admission enforces these finite checked bounds:

```text
N_object <= N_object_max
N_reach  <= N_reach_max <= N_object_max
N_delta  <= N_delta_max <= N_object_max
N_pack <= N_pack_max
N_pack_record = N_object + N_pack
N_pack_record_max =
  N_object_max + N_pack_max
N_roots  <= N_root_max
R_child_max = 512
E_reach_max <= N_root_max + R_child_max * N_reach_max
```

`N_catalog_record_max<2^32`, so `N_object_max<2^32`; record counts and ranks
are `u32`, while products, byte totals and cross-pack sums use checked
`u64`/`u128` arithmetic. Maintenance uses the S1
basis-local dense rank and exactly one fully allocated, non-sparse,
OwnerSlot-charged trace file:

```text
P_s = 4096
d   = 32
P_t = P_s - d = 4064

q_0(n) = ceil(n / (4 * P_t))
q_{j+1}(n) = ceil(q_j(n) / (8 * P_t)) while q_j(n) > 1
Q(n) = sum_j q_j(n)

if n = 0: Q(n) = 0
D_trace(n) = A(P_s * (1 + Q(n)))
D_trace_max = D_trace(N_object_max)
I_trace_max = 1
```

Maintenance reserves `D_trace_max` but allocates only
`D_trace(N_object)` for the captured basis. The file has one header block plus
`Q(N_object)` state/summary blocks. Its canonical header and digest bind the
trace format, exact `MaintenanceBasis`, `N_object`, every level count/offset,
allocated length and current phase. Every remaining block digest binds the
domain, exact basis, `N_object`, phase, level/type, block index,
valid-tail length and its 4,064-byte payload. The checked header geometry must
equal `Q(n)`; swapping blocks, replaying another basis or reinterpreting a
logical block as physical therefore fails. A phase transition rewrites the
header and every block digest before the new state meanings are consumed.
Level zero holds a two-bit state per rank. During logical trace, `00` is
unseen, `01` pending, `10` done/logically-live and `11` invalid.
Valid ranks initialize to `00`, unused state-tail ranks to `11`, and all
summary bits and tails to zero. One summary bit per child block/subtree is one
if and only if it contains a valid `01`.

Fixed-schema roots and newly verified typed children move `00 -> 01`. Pop
follows the summary tree and moves `01 -> 10`; one coordinator recomputes all
affected ancestors. The selected object is then reverified by exact key,
namespace, kind, length, canonical codec and digest before only its closed
typed children are considered. Sharing, duplicate edges and corrupt cycles
cannot expand one rank more than once.

Success requires valid ranks to contain only `00` or `10`, no `01` or `11`,
the unused state tail to remain exactly `11`, and all summary bits/tails to
recompute exactly with every summary bit zero. Only then is `10`
`LogicalLive`. A crash, checksum/summary/state mismatch, corrupt typed edge,
missing object, rank/count overflow, short write or I/O error discards the
whole OwnerSlot scratch and synchronizes its deletion; it is never resumed.
State/summary windows, one
height-`<=8` Catalog path, the streaming decoder and bounded child batch fit
one `<=2 MiB` heavy claim. `mmap`, a resident queue/set and a repository-sized
record stream are forbidden. Bounded dirty windows and explicit
synchronization/drop behavior are required.

The ordered ObjectCatalog sweep consults `LogicalLive`. Each logically live
Delta locator emits one exact `DeltaEdgeV1 {base_id,target_rank:u32}`. A Full anchor
reached only this way is `PhysicalLive`, not `LogicalLive`, so S3 normalization
can distinguish an independently logically-live anchor. Candidate/staging and
current-maintenance outputs remain fully charged OwnerSlot roots outside the
selected victim population. Every ReadSlot pins its captured StoreSequence/
arena epoch; it does not add one record per object.

After logical success, the ordered edge-group merge enters one-way
`PhysicalClosure`: `00=dead`, `10=logical keep`, `11=anchor-only keep`, and
`01=logical Delta selected for normalization`. In a normalization-mode pass a
dead-base singleton changes its target `10->01` if the checked Full frame fits
the remaining `64 MiB-8 B` output-frame budget and leaves its base `00`;
otherwise the base changes `00->11`. Beneficial groups retain a dead base as
`11`; a logical
base stays `10`. Summary bits remain checked zero and no longer interpret
`01` as pending. Exact point lookups verify every base Full and target Delta,
equal canonical lengths, bounded frame header and unique pair. The rewritten
phase-bound digests make these meanings unambiguous without another bitmap,
map or retained record stream.

### Exact physical closure

Physical closure uses only two packed schemas and two sequential external
sorts:

- `DeltaEdgeV1` is exactly 36 bytes:
  `base_id[32], target_rank:u32`.
- `PackCensusV1` is exactly 72 bytes:
  `segment_id[32], offset_or_committed:u32, marked_len:u32,
  object_id_or_zero[32]`.

Bits `31..30` of `marked_len` form one closed enum: `00 DEAD_CATALOG`,
`01 LOGICAL_CATALOG`, `10 ANCHOR_CATALOG`, `11 INVENTORY`. Its low 30 bits
hold exact framed length for a Catalog alternative or allocation-rounded bytes
for inventory. A Catalog alternative carries the exact locator offset,
selected ObjectId and state-derived kind. The one inventory alternative
follows all positive frames for its pack, carries committed EOF in
`offset_or_committed` and a zero ObjectId. Every pack's committed and allocated
length is `<2^30`; code masks the kind bits before arithmetic and uses checked
`u64`/`u128` sums before narrowing. The exact order is
`(segment_id, offset_or_committed, value(marked_len), kind(marked_len),
object_id_or_zero)`. The ObjectId lane lets one physical-order merge compare a
Catalog key with the exact frame header. No tag byte, padding, codec, custody
variant, relocation record, footer or reserved field remains.

Let `R_run=1 MiB`; let `N_delta_max` and `N_pack_max` be the admitted maxima
for Delta locators and installed sealed PackSegments. `N_pack_max` is derived
from the hard pack-directory inode/quota bound. Let `r` be fixed record width
and `n` maximum records:

```text
q_run(r) = floor(R_run / r)
require q_run(r) >= 1
m(r,n) = ceil(n / q_run(r))

G(r,n) = A(r * n + 64 * m(r,n))

N_pack_record_max =
    N_object_max + N_pack_max
D_closure_scratch_max =
    2 * max(G(36, N_delta_max),
            G(72, N_pack_record_max))
    + A(4096)
I_closure_scratch = 3

q_run(36) = 29,127
q_run(72) = 14,563
passes_edge = ceil(log_8(max(1, m(36, N_delta_max))))
passes_pack = ceil(log_8(max(1, m(72, N_pack_record_max))))
```

The first external sort orders 36-byte edges by `(base_id,target_rank)`.
Its grouped merge resolves each base ID once, exact-selects each target by its
basis rank, verifies that the row is a Delta naming that base, rejects duplicate
ranks/targets and records anchor/normalization choices in the trace. The
complete ObjectCatalog sweep then emits a frame alternative
for **every** selected row, including dead rows; state `01` or `10` is logical,
state `11` is anchor-only, and `00` is dead.
Finally, a streaming census of the complete installed sealed-PackSegment
directory verifies containment/type, SegmentId filename, committed length,
allocation and exact-EOF framing and emits one inventory alternative per pack;
directory entries are never accumulated in memory.

The second external sort orders these variants by pack and frame. Its merge
sequentially verifies every selected ObjectId against the exact frame header,
validates the trailing inventory alternative, intervals, duplicate locators,
masked lengths, SegmentIds, committed/allocation bounds, overlaps and custody,
and emits exact
zero-live and inventory-only totals. A pack is current-selected exactly when a
current ObjectCatalog locator names it; therefore a rowless current-selected
pack is impossible and no `PackCatalog` or ninth Catalog namespace exists.
Incomplete artifacts remain outside the installed directory under fixed
OwnerSlot-directory custody. An inventory-only installed pack cannot be
deleted while an old retirement epoch can name it; otherwise it is an
orphan/quarantine candidate for synchronized unlink.

The exact dense Auxiliary keep-set is:

```text
every ObjectCatalog row whose physical-closure trace state is 01, 10, or 11
```

Every captured ObjectCatalog row is exactly `KEEP`, `DELETE` or `REPLACE`.
State `00` rows are omitted, each state-`01` target is replaced by verified
Full, and state `10`/`11` rows remain selected unless the same physical batch
relocates them. Owner-staged candidates do not become Catalog rows. Dense validation proves each exact-locator deletion,
requires each keep identical, validates every exact old-to-new replacement and
rejects extra rows. Every other namespace is byte-identical except removal of
the exact Maintenance Build nonce. Packs omitted by the new root remain
old-epoch custody until every reader cancellation has joined and all old
cursors/FDs are closed.

One `REWRITE_BATCH` engine covers dead repack, emergency repack, all-live
consolidation and Delta-to-Full normalization; these are policies, not four
algorithms. One invocation-wide control header records the single policy; one
checked 4-KiB vector retains at most 64 victims:

```text
VictimV1 = segment_id[32] || allocated:u32 || retained_framed:u32
64 * 40 = 2,560 bytes
```

Both byte fields are exact per-pack values `<2^30`; cross-victim totals use
checked `u64` arithmetic.

Store rescans the captured ObjectCatalog in ObjectId order. A physical-policy
batch copies/verifies state-`10`/`11` rows from selected victims; a
`NORMALIZE` batch reconstructs exactly the state-`01` targets as Full. Each
writes at most one 64-MiB ObjectId-ordered output and policies never mix. After
seal, it rescans replacement record headers sequentially and merges derived
locators with the basis Catalog. Thus replacement ordering needs no relocation
stream, third sort or resident ObjectId list.

Progress uses `V_alloc`, the actual allocation-rounded bytes of source packs
fully retired by the selected commit; `X_live<=64 MiB-8 B`, the verified output
frame bytes; and `X_alloc<=P_pack_alloc_max=A(64 MiB)`, the actual
allocation-rounded sealed output (`0` when empty):

| Policy | Exact eligibility/progress |
|---|---|
| `DEAD_REPACK` | Up to 64 partially/fully dead packs; require `2*X_alloc<=V_alloc`. |
| `EMERGENCY_REPACK` | Only when normal ratio is impossible before retention failure; require `X_alloc<V_alloc`. |
| `CONSOLIDATE` | Up to 64 underfilled all-live packs; require `X_alloc<=V_alloc` and fewer output packs. |
| `NORMALIZE` | Replace at least one state-`01` Delta with Full and strictly reduce Delta count; claim no physical decrease and keep both allocations charged until later physical retirement. |

The requested maintenance mode and frozen policy order select exactly one
policy, with SegmentId tie order. With `p` eligible source packs, physical convergence takes at most
`ceil(p/64)` fresh-basis batches; finite admitted Delta count bounds additional
normalization batches. No policy deletes a semantic root or counts an
unretired shared source pack as reclaimed.

Two fully allocated, non-sparse generation-container files and one checked
4-KiB control file are reused sequentially for the two sorts. Each generation
is preallocated to the largest `G` bound; no later sort starts before the prior
final stream is consumed. Logical runs use 64-byte headers. Checked arithmetic
is mandatory and record counts never grow. Eight logical cursors share bounded
offset reads. Initial-run memory is at most 1 MiB; merge memory is at most
eight 64-KiB input windows, one 64-KiB output window and a fixed eight-key
heap. The complete heavy claim remains at most 2 MiB. Replacement adds one
sequential Catalog pass and, when output exists, one sequential replacement-
header pass; it adds no scratch schema.
There is no object-count-sized RAM table, eight-MiB buffer, or disk term
masquerading as RAM.

### Non-borrowable maintenance and root-control reserve

Let `D_HEAD` be the allocation-rounded maintenance HEAD temporary/control bound, and
`D_root_ctl/I_root_ctl` the separately protected byte/inode
semantic-root-control slice. Because the Auxiliary Catalog, trace,
physical-closure sort, one possible replacement output and root-control slice
can coexist, the simultaneous reservation is:

```text
D_aux_max <= A(2 * C_max)

D_maintenance >= D_aux_max
               + D_trace_max
               + D_closure_scratch_max
               + P_pack_alloc_max
               + D_HEAD
               + D_root_ctl
I_maintenance >= I_aux_max
               + 1                 # trace
               + 3                 # two generation files + one control file
               + 1                 # replacement output
               + I_HEAD
               + I_root_ctl
```

Its inode counterpart includes Auxiliary Catalog files, trace file `1`, sort
files `3`, one replacement pack, maintenance HEAD temporary and all root-
control workflow files. All scratch/output files are fully allocated,
non-sparse and created beneath the already-selected maintenance OwnerSlot
directory. A `max(...)` reservation is not valid for this schedule.

`D_root_ctl/I_root_ctl` cannot be borrowed even by bulk maintenance. It is the
sum of all coexisting byte/inode allocations for S1 sparse path-copy pages, S2
HEAD/control output and framing across the largest complete accepted
semantic-nonexpanding root-control workflow. The derivation covers
`remove_checkpoint` effect, replay and no-effect receipt-only completion;
`destroy_sandbox`; and `destroy_workspace_session` with its selected
`AdapterClose` intermediate plus the final row/root/pin/intent changes and
receipt at every cut. Root-control workflows are serialized. Closed key
placement, value widths, S1 fanout
and worst-case page splits must be frozen before qualification derives this
exact bound; writable readiness is forbidden without it. The slice is
restored only after the complete workflow and selected old-page/control cleanup
and parent-directory synchronization are durably complete. Once any part is
used, normal writable readiness stays closed, and recovery restores the whole
slice before reopening it. Root deletion itself grants zero byte or inode credit.
Creation, publication and bulk maintenance cannot consume this slice.

Before `ResourceLimitExceeded(storage_retention)`, each fenced iteration runs
one `REWRITE_BATCH`, durably retires eligible old files, restores the complete
reserve and then captures a fresh basis. A mixed batch is still one S2 commit.
Finite pack/Delta counts and the strict progress rules above make repeated
progress terminate. `RetryLater` may repeat only while measured progress
exists. The floor is irreducible only when exact trace and all four policies
expose no progress. More-than-50%-live dead bytes and framing are never
relabelled semantic live. No policy changes a canonical object or `StateId`.

Old packs, arenas and anchors retire only after replacement `HEAD` and its
parent directory are durable. They are deleted only after the old bounded
reader epoch drains; deletion and every affected parent directory are synced
before accounting credit. A crash recovers the old selected basis or the
complete replacement, never a hybrid.

There is no automatic history retention or automatic root expiry. Explicitly
named checkpoints and required session origins retain their reachable unique
information until the matching public removal succeeds. Unretained revisions
collect; identical objects deduplicate; intentionally retained differing
states consume their unavoidable information. No squash is required or
permitted.

An optional TTL/last-N controller is policy above the Store: it may invoke only
the existing remove/destroy methods for checkpoint/session identifiers it
created and owns, must skip `CheckpointInUse`, must never remove a manual
checkpoint, and must keep its registry external and finitely bounded with safe
behavior on registry loss. It adds no Store namespace, API, component or
implicit history rule.

## Resource profile

All values in this table are frozen **requirements/analytical bounds** until
qualification:

| Resource | Bound |
|---|---:|
| Storage-managed live memory | `M_managed_hard = 8 MiB`; `M_managed_normal_target = 4 MiB` |
| One sandbox’s concurrent managed claims | `M_sandbox_claim_max <= 4 MiB` |
| One heavy operation | `M_heavy_claim_max <= 2 MiB` |
| Cgroup `memory.high` | `64 MiB` |
| Cgroup `memory.max` | `100,663,296 B`, exactly 96 MiB |
| Cgroup swap / persistent application cache | `0 / 0 B` |
| Storage workers | `4` |
| OwnerSlots | exactly `1` dedicated maintenance lane + `15` foreground lanes |
| Queued heavy descriptors | `16`; aggregate `<=64 KiB`; queued payload `0` |
| Storage-owned FDs | `128` |
| ReadSlots | exactly `64`; `30 s` absolute cancellation deadline, nonrenewable; release only after joined drain |
| Complete PackSegment / contained frames | `<=64 MiB`, including the 8-byte signature / `<=64 MiB-8 B` |
| External run / merge fan-in | `1 MiB / <=8` |
| Fenced maintenance epochs / victim vector | `1 / <=64 SegmentIds (<=4 KiB)` |
| Catalog page / height / arenas | `16 KiB / <=8 / 2` |
| Catalog two-arena physical bound | `<=4C_max` |
| Classified reclaim/retirement debt | soft `128 MiB / 32 inodes`; hard `256 MiB / 64 inodes` |

The 8 MiB managed ceiling is partitioned without double counting:

| Partition | Hard sub-budget |
|---|---:|
| Catalog pages and cursors | `2 MiB` |
| Four worker buffers | `1 MiB` total, `256 KiB` each |
| Coordinators, readers, replay, permits and queue | `1 MiB` |
| Chunk/hash/codec/trace/sort/merge scratch | `3 MiB` |
| Accounting, recovery and allocator headroom | `1 MiB` |

`M_managed_normal_target=4 MiB` is the global normal-operation target inside
the `M_managed_hard=8 MiB` permit ceiling;
`M_sandbox_claim_max=4 MiB` is a separate per-sandbox admission bound. None of
these is process RSS. Thread stacks, allocator arenas, helper processes, page
cache, dentries and inode slab are captured by the outer storage-service
cgroup.

Every grant is a multidimensional claim, not a worker-count promise:

```text
for every managed partition p:
  sum(bytes of all live claims in p) <= partition_cap[p]
sum(bytes of all live managed claims) <= 8 MiB
sum(bytes attributed to one sandbox) <= 4 MiB
active_heavy <= free_workers
```

The maximum simultaneously active heavy-operation count is whatever complete
claim vectors fit all four inequalities and the FD/OwnerSlot/ReadSlot/disk
dimensions—often one or two, never implicitly four. The per-sandbox `4 MiB`
number is a ceiling, not a reservation: at most two sandboxes can hold maximum
claims at once and all other work queues or returns typed `RetryLater` before
any payload, FD, worker or staging allocation.

The exact `96 MiB` `memory.max` applies once to the shared PMSS storage service
and all of its storage helper processes across all sandboxes and sessions; it
is not multiplied per sandbox. This is stricter than a 96-MiB-per-sandbox
storage allowance. One sandbox can attribute at most 4 MiB of the managed
pool. Untrusted runtime/container memory is not storage memory and belongs to
a separate finitely configured per-sandbox parent cgroup that contains all of
that sandbox's session children; no child gets an additive unbounded budget.

`memory.high` is a throttle/qualification target, not a proof. The frozen
deployment must satisfy and measure:

```text
M_service_current =
    RSS_baseline
  + resident_thread_stack_bound
  + allocator_arena_and_fragmentation_bound
  + storage_helper_process_bound
  + M_managed                         # <= 8 MiB
  + charged_page_cache_writeback_bound
  + charged_dentry_inode_bound

M_service_current <= 64 MiB under every qualified workload
M_service_current <  96 MiB at every instant
```

Qualification freezes thread count and stack size, allocator/arena settings,
helper count, I/O/readahead/writeback windows and kernel/filesystem profile.
An implementation that merely survives `memory.max` throttling/OOM does not
pass.

Idle sessions own no storage worker, buffer, FD, read slot or volatile permit.
At the 30-second deadline, a read batch is canceled; wall-clock expiry alone
does not clear its epoch. The slot releases only after cancellation joins and
every old-epoch cursor/FD closes. Supported environments must qualify this
bounded, cancellable I/O; failure blocks retirement and readiness rather than
weakening safety. A higher workflow may acquire a new slot and resume only from
`{StateId, canonical_traversal_key}` after proving that exact StateId remains a
semantic root in the new basis. Otherwise it returns `SnapshotExpired` or
restarts the public operation. This is not renewal and never reuses a physical
locator. Every root-count, terminal-session, object/fact, path, workspace, byte
and inode dimension has a finite configured hard limit.

## Aggregate storage admission

Resource Admission is the sole cross-cutting shared service. It owns only a
fixed volatile vector of counters and issues one all-or-none uniquely tagged
permit. The tag is an implementation token, not a version. Resource Admission
cannot mutate canonical objects, Catalog rows, `HEAD`, sessions, adapter
allocations or retention policy.

Before allocation or dispatch, one claim includes every applicable managed
byte, worker, queue descriptor, FD, OwnerSlot, ReadSlot, disk byte, inode,
workspace, staging, charged-physical, known-debt and maintenance need.
Admission atomically grants the entire vector or grants nothing. Queued work
holds only its already-counted bounded descriptor and no payload, FD, worker
or staging allocation.

Physical capacity admission uses allocation-rounded, non-speculative
accounting:

```text
charged selected physical and Catalog bytes
+ charged owner/staging/orphan bytes
+ charged adapter workspace bytes
+ outstanding byte and inode reservations
+ non-borrowable maintenance reserve, including separate root-control slice
<= qualified physical byte and inode capacity
```

Root retirement does not subtract unreachable estimates. All selected bytes
remain charged until exact trace and completed physical reclaim. Known
reclaim/retirement debt counts only deterministically identified retired
epochs, maintenance orphans/output and other already classified physical
residue. It excludes still-selected potential garbage, selected pack slack and
Catalog arenas (which retain their separate `<=4C_max` bound); it is not a guess
for all unreachable data and is not created retroactively by root removal.
Trace-classified dead frames remain fully charged until durable physical
reclaim.

Every permit has one acyclic owner. Release is idempotent and occurs only when
each charged allocation is absent, transferred to another durable owner or
still conservatively charged. Cancellation joins/drains workers, closes FDs
and synchronously resolves owner state. Independent partial resource
acquisition is forbidden.

### Typed overload

| Condition | Required outcome |
|---|---|
| Worker, queue, managed-memory, FD or transient permit pressure | Bounded `RetryLater` before staging/public change |
| Adapter workspace byte or inode enforcement limit | `QuotaExceeded(bytes|inodes)`; workspace remains intact |
| A finite configured hard count/cap is exceeded | `ResourceLimitExceeded(resource)` before effect |
| Retention pressure with a bounded exact pass able to progress | Bounded `RetryLater` while the exclusive pass runs |
| Exact trace plus S3 normalization and all three repack/consolidation branches prove no allocation-rounded progress | `ResourceLimitExceeded(storage_retention)`; no root is deleted and no reserve is borrowed |
| Required filesystem, durability, containment or quota claim is unavailable | `UnsupportedEnvironment` or the narrower adapter capability error before mutation |
| A selected dependency is missing/corrupt/ambiguous | Fail readiness closed; never fall back to older state |
| Actual usage exceeds a granted claim | Abort before selection, retain exact ownership/accounting, and enter read-only degraded handling if counters cannot be reconciled |

Every post-acceptance semantic result still obeys the exact receipt rule;
`RetryLater` used before semantic acceptance need not consume a receipt.

### Workspace quota truth

`PortableAccounting` means conservative reservation plus measured usage.
`EnforcedQuota` may be claimed only when a qualified unique scope enforces
both bytes and inodes with tested overflow/crash behavior. An arbitrary shared
bind directory never qualifies. Aggregate cgroup accounting, Store capacity
accounting and per-workspace byte/inode enforcement are separate dimensions.

Without reflink, FUSE, privileged mounts or write interception, a private
ordinary-file workspace has the honest general lower bound
`Theta(B_i+F_i)` additional allocation for materialized bytes and facts.
Creation reserves the full materialization upper bound plus admitted growth;
inactive sandboxes, forks and checkpoints create no workspace copy.

## Backend and environment requirements

| Adapter | Required profile |
|---|---|
| Docker OCI | Current full profile: complete private ordinary-file allocation, descriptor-safe realization/capture, full canonical fact preservation and no added administrative capability. OCI conversion is an edge around the one portable archive. |
| WASI | Future reduced preopen/capability profile. Unsupported metadata, links or sparse facts reject; they are never silently lost. |
| Firecracker | Future fixed-block allocation with an authenticated guest agent or qualified offline reader. VM snapshot identity is never `StateId`. |

Every adapter must prove descriptor/capability-relative containment, exact fact
round-trip to the same `StateId`, writer/mapping drain, stable two-pass capture,
idempotent activation/disposal recovery, quota truth and conflicted-workspace
readability. Symlinks are leaf facts and are never followed. A missing
capability rejects the profile or fact before mutation.

Docker layer/snapshotter choices, OCI layer digests and whiteouts are adapter
input/runtime facts, not canonical identity. OCI import applies the ordered
changesets to one complete fact view before canonical build; export converts
one complete canonical state at the edge. WASI and Firecracker expose the same
public lifecycle semantics without adding selectors.

## Honest work bounds and performance labels

Let `B` be non-hole bytes, `F` filesystem facts, `A` attribution facts,
`N` Catalog records and `X` copied live repack bytes:

| Operation | Universal ordinary-path work | Peak managed memory | Additional physical allocation |
|---|---:|---:|---:|
| Materialize workspace | `Theta(B+F)` read/write | Fixed permits | `Theta(B+F)` workspace |
| Portable capture/build | `Theta(B)+O(sort(F+A))`; source reads `<=2B` | Fixed permits | missing objects plus charged runs/framing |
| Export | `Theta(B+F)` | Fixed stream/cursor | selected sink output |
| Checkpoint / fork / rollback / fork commit | `O(H)` typed Catalog path work per changed key | Bounded S1 pages | no payload copy |
| S1 dense rebuild | `Theta(N)` ordered I/O | Fixed builders | one Auxiliary arena, total Catalog `<=4C_max` |
| Bounded repack | exact trace plus `Theta(N_object+N_pack+X_live)` | Fixed trace/sort/codec buffers | `X_alloc<=P_pack_alloc_max=A(64 MiB)` plus replacement Catalog/reserve |

Ordinary-directory publication/materialization has the correctness lower bound
`Omega(B_nonhole+F)`. Only a capability-qualified complete journal may replace
portable discovery with dirty-byte/fact closure; a gap, overflow or incomplete
proof falls back to the full scan.

Performance families remain separate:

| Family | Claim |
|---|---|
| `P4-compat-sparse` | Stage 4.6 P4 median `58.136209 ms` is a **historical project measurement**. `<=5.8136209 ms` is a **10x stretch target** for the comparable sparse fixture. The old formal 100x threshold is `<=0.364440 ms`. |
| `PortableFullScan` | Must report bytes/facts and obey the ordinary-directory lower bound; it has no universal 5.8 ms target. |
| `JournalQualifiedDelta` | Optimization target only after completeness, epoch and fallback qualification; correctness never depends on it. |

## Acceptance evidence

Phase 6 may accept these documents only after the design is internally
consistent and implementation qualification is explicitly left Proposed.
Implementation acceptance later requires at least:

- restricted-CBOR, BLAKE3, C1, both FastCDC profiles, C2 and C3 golden vectors;
- same `StateId` for every claimed adapter round-trip and rejection of every
  unclaimed fact;
- million-entry, deep-tree, huge-directory, sparse, hardlink, raw-name,
  metadata and adversarial C2/C3 corpora;
- exact `U_candidate=U_reuse disjoint-union U_missing`, `C_reuse`, `P_reuse`
  and framed `P_new` accounting, same-ID two-pass verification, and corruption
  injection;
- S1 sparse/dense equivalence, occupancy, height, arena and cache-off tests;
- S2 power cuts at every dependency/`HEAD` barrier, acknowledged-sequence
  retention and fail-closed corruption tests;
- all 1,024 receipt slots, exact replay after restart and
  `ReplayExpired` no-execution tests;
- strict-origin sibling publication, losing-owner cleanup, checkpoint,
  rollback and ordered `P/C/B` fork tests;
- AdapterClose crashes before/after intent, disposal, row deletion and receipt;
- S3 eligibility, base re-resolution, target verification, depth/cycle failure,
  normalization and Full-only comparison;
- exact semantic-root/non-root adversaries, S1 `u32` count/rank corruption,
  admitted `<2^32` record ceilings, every
  two-bit trace state/tail/summary/crash cut, block-swap/replay, duplicate/cyclic edges, the
  two sequential reusable-generation closure sorts (36-byte Delta edge and
  72-byte pack census), replacement-header rescan without relocation scratch,
  anchor-only trace phase, dead-row census, wholly dead packs, OwnerSlot
  candidate custody and ReadSlot epoch retirement;
- charged-allocation high water, every complete root-control workflow,
  maintenance conflicts, simultaneous near-full reserve use and restoration;
- normal dead-byte, emergency high-live, all-live consolidation and separate
  normalization branches, 64-source batching, irreducible-floor convergence,
  reader expiry and synchronized retirement;
- frozen maximum maintenance write pause, fairness, `RetryLater` rate and
  foreground latency at `C_max` with 1/4/8/16/32/64 active sessions;
- workers 1/4, owner lanes 1+15 including 16th-foreground rejection, readers
  64, queue 16/rejection, 128 FDs, disk/inode
  quotas, 8 MiB managed permits and exact 96 MiB cgroup sweeps; and
- cache-off correctness/performance and deterministic cleanup plateaus for
  buffers, tasks, FDs, permits, staging, charged bytes and inodes.

The 8 MiB managed ceiling, 4 MiB target, exact cgroup profile, six mechanisms,
backend profiles, performance targets and every proposed format constant remain
**requirements/targets**, not achieved claims.
