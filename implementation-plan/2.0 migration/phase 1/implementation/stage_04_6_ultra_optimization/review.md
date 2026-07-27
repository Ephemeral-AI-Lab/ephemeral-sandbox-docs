# Stage 04.6 architecture review: backend-neutral Merkle checkpoints and replaceable projections

Status: **architecture decision and falsifiable implementation proposal**

Date: 2026-07-27

Reviewed inputs:

- [`plan.md`](plan.md)
- [`baseline-experiment/README.md`](baseline-experiment/README.md)
- [`design_recommendation_from_sheppard_combined_with_layerstack.md`](design_recommendation_from_sheppard_combined_with_layerstack.md)
- [`04-seqcdc-space-time-complexity-and-acceptance-criteria.md`](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)
- [the existing LayerStack storage contract](../layerstack_storage_contract.md)
- [the Stage 03 incremental-publication specification](../stage_03_incremental_publication/spec.md)
- [the 2.0 migration index](../../../index.md)
- [the 0.2.0 PRD](../../../../../0.2.0/PRD.md)
- [the Phase 3 plan](../../../phase%203/index.md)
- the current `upgrade-2.0-phase-1` LayerStack, workspace-session, CLI,
  candidate-materialization, and benchmark sources
- the two available Codex sessions named in the review request

## Verdict

**Replace the Stage 04.6 physical architecture.** In the requested verdict
taxonomy, the answer is **replace the architecture**, not “keep but revise.”
This does **not** replace the already-correct Stage 03 logical checkpoint
contract.

CAS-first loose-object publication plus a default directory-native
delta/carrier-vector projection is not the right primary physical
publication/materialization architecture. Keep a much shallower, constrained
directory vector only as the capability-qualified OCI projection and logical
directory reconstruction fallback.

The physical replacement is:

1. one backend-neutral, immutable, persistent Merkle filesystem checkpoint;
2. one backend-neutral attribution checkpoint;
3. an immutable multi-locator payload store;
4. a publication engine that commits changed Merkle pages and payload
   locators, not a new complete tree or a logical layer chain;
5. independent OCI, Firecracker, and WASI projection namespaces whose
   metadata is disposable after any sole-locator payload extents are
   evacuated; and
6. optional range-CoW or lazy accelerators selected by capability probes.

This is a destructive conceptual change, not a destructive data migration.
Existing roots and complete carriers remain readable while the new format is
qualified.

### Stage 04.6 release scope

Stage 04.6 implements, benchmarks, and production-qualifies the OCI/Docker
path. Firecracker and WASI remain Phase 3 consumers. This review therefore
requires a backend-neutral logical format, a frozen replaceable adapter
boundary, canonical conformance fixtures, and a credible projection/recovery
design for both future adapters; it does **not** require working
Firecracker/WASI adapters or their runtime/performance matrices before the
Phase 1 OCI release. Phase 3 performs those implementations and qualifications
without changing or republishing the logical root.

Stage 03 already provides the important logical foundation:
`RootRecordV3 -> TreePage -> FileNode -> SegmentPage -> Chunk`, bounded
persistent pages, complete-root semantics, and the atomic
`{RootId, AttributionRootId}` checkpoint pair. Stage 04.6 must make that model
the operational control plane instead of letting carrier availability or
history determine hot-operation cost. The former plan correctly called CAS
authoritative; the failure is in its physical write/read path, not its stated
identity model.

Keep these parts of the existing design:

- `RootId` and `AttributionRootId` as the sole logical identities;
- immutable manifests, explicit schema versions, OCC, leases, and
  compare-and-swap ref updates;
- bounded queues, workers, memory, active attempts, and projection depth;
- the existing space formula and settled-space gates;
- SeqCDC's insertion-locality benefit, provisionally, inside the payload
  store; and
- the 35.375-microsecond warm lookup path as a non-regression control.

Remove or demote these parts:

- a complete native carrier as the normal representation of every root;
- a directory carrier vector as the default hot projection for each root;
- loose 8--32 KiB chunk files with per-object durability work;
- foreground reconstruction of complete roots;
- foreground full-payload verification on exact-key reuse;
- CAS-first publication followed by a duplicate promoted upper;
- physical flattening conflated with public logical ancestry pruning; and
- any assumption that an OverlayFS upper supplies byte-range CoW.

### Scope of the speed objective

The absolute reference ceilings remain reported for first ingestion,
publication, and activation. First ingestion is scored against both the
`1.070 s` / `214 ms` ceilings and its measured one-pass physical floor;
normal incremental publication and stored-projection activation must meet the
applicable 100x gate. Setup may be excluded only when no product operation
performs it. If the measured read/hash floor disproves universal first-import
100x or 500x, report that result rather than weakening the steady-state gate
or moving setup outside a product timer.

The hard steady-state operations are:

- publish/add a layer;
- create a logical checkpoint;
- fork;
- public logical squash, implemented as an ancestry prune;
- rollback/root switch;
- winner reactivation;
- mount or activate an already-built compatible projection; and
- exact-root reuse.

Physical flattening, projection construction on a projection miss, and the
first complete read of lazily mapped bytes are different operations and have
separate clocks.

## Four conclusions that must not be softened

1. **A byte-for-byte 870.08 MiB checkout cannot be written in 20--100 ms on
   the measured system.** The 100x materialization threshold implies 8.51
   GiB/s of output; the 500x threshold implies 42.54 GiB/s. A 20 ms result can
   only be a root switch, mount, or lazy mapping.
2. **Generic directory OverlayFS is whole-file CoW for data writes.** A
   one-byte write to a 1 GiB lower file copies the file data into the upper
   before the write. `metacopy` delays data copy for metadata-only operations;
   it does not make data writes range-CoW. The Linux kernel documents this
   behavior in its [OverlayFS copy-up description](https://docs.kernel.org/filesystems/overlayfs.html).
3. **The qualified no-extra-device OCI path and universal range-CoW form an
   impossibility triangle.** With no reflink, `/dev/fuse`, `/dev/loop`, NBD,
   device mapper, custom kernel filesystem, or privileged helper, a normal
   POSIX directory cannot transparently serve arbitrary binaries and also
   record authoritative dirty byte ranges. The directory path must be correct
   on every placement it accepts but will lose the large-file range-CoW cell.
   An optional accelerator is the only honest solution.
4. **The new logical ancestry-prune operation should move no payload.** If
   resolving a root requires replaying a layer chain, the logical
   representation is wrong for MCTS. Every committed root should already be a
   complete persistent-tree view. Stage 04.6 changes public
   `squash_layerstacks` to logical ancestry pruning; physical flatten/remount
   becomes separately timed maintenance.

## What the preserved baseline actually proves

The historical result block/artifacts and `baseline.json` remain immutable.
Their values are valid for their recorded component intervals; this README's
future experiment plan may be expanded append-only:

| Recorded interval | Current | 100x threshold | 500x threshold |
| --- | ---: | ---: | ---: |
| Prepared-change-vector CDC/CAS publication | 107.024411507 s | 1.070244115 s | 0.214048823 s |
| Cold complete native carrier construction | 9.987675338 s | 99.876753 ms | 19.975351 ms |
| Explicit same-key materializer reuse | 6.361909169 s | 63.619092 ms | 12.723818 ms |
| Ordinary warm generation lookup, median | 0.035375 ms | preserve | preserve |

The source audit found two important boundary qualifications:

- source traversal, `stat`, ordering, and `LayerChange` construction occur
  before the recorded 107.024-second publication timer; and
- carrier traversal/profiling and actual workspace activation occur after the
  recorded 9.988-second materialization timer.

Therefore future results need both the historical matched component interval
and an outer operation clock. The old numbers must not be relabeled as
source-to-durable-root ingestion or workspace-ready latency.

### Physical lower bounds

For `B = 912,350,100` bytes, even a perfectly overlapped implementation obeys:

```text
T_first_ingest >= max(
    B / measured_read_bandwidth,
    B / measured_hash_and_chunk_bandwidth,
    B / measured_write_bandwidth when bytes cannot be adopted
) + metadata_and_durability
```

| Objective | Required byte rate before metadata and durability |
| --- | ---: |
| 100x first-ingest read floor | 852.47 MB/s = 812.98 MiB/s |
| 500x first-ingest read floor | 4.262 GB/s = 3.970 GiB/s |
| 100x full native reconstruction output | 9.135 GB/s = 8.507 GiB/s |
| 500x full native reconstruction output | 45.674 GB/s = 42.537 GiB/s |

If unseen payload must be read and written serially, aggregate media demand is
at least twice the first two rates. A host whose measured one-pass control is
slower than 1.070 seconds cannot satisfy a universal 100x first-ingest promise.
That is a physical limitation, not permission to omit work from the timer.

### Why the current implementation is unusually slow

The current source explains much of the gap:

- publication SeqCDC-hashes every regular file;
- each new loose chunk is installed through a temporary file, sync, link,
  removal, and parent-directory durability sequence;
- an 870 MiB corpus at a 16 KiB average chunk is about 55,700 objects;
- source verification then rereads source and stored chunks;
- complete materialization opens many small chunks, reconstructs files, syncs
  them, and hashes the resulting native tree; and
- exact-key materializer reuse performs deep carrier verification instead of
  trusting an immutable, durably committed receipt.

Replacing per-chunk files and redundant verification with one-pass sealing,
append-only packs, grouped durability, and immutable receipts can plausibly
remove two orders of magnitude of software overhead. It cannot remove the
physical cost of bytes that truly must be read or written.

## Direct review of the current carrier proposal

### One-byte edit in a 100 MiB or 1 GiB file

The proposed carrier stores the copied-up file. Frozen-upper promotion avoids
copying that upper a second time, but it does not avoid OverlayFS's first
whole-file copy-up. With a 1 GiB base:

```text
qualified directory-path peak before packed evacuation =
    old 1 GiB lower + new 1 GiB upper
```

CAS-first publication then retains another representation of changed content.
Calling the upper `L_hot` rather than `U_active` does not make those bytes
disappear. A settled promoted vector therefore cannot prove either the
`1.08 * D_ideal` gate or the `<=1%` avoidable-duplicate gate without a later
locator evacuation/rebase. Sixteen siblings can temporarily allocate roughly
16 GiB of private uppers after sixteen one-byte writes to the same 1 GiB file.

This alone disproves a directory carrier vector as the universal fast
publication/materialization architecture.

### `pip`/`npm` and 100,000--1,000,000 entries

Promotion avoids a second payload copy, but it does not avoid:

- one native inode/dentry per upper entry;
- directory merge and negative lookup work;
- whiteout, opaque-directory, xattr, and repeated-parent allocation;
- an `O(E_changed)` seal and semantic verification pass; or
- retained inodes for every cached carrier.

Twenty milliseconds is not a credible publication or scan target for one
million previously unindexed entries. The correct goal is one bounded,
batched, entry-linear pass with constant RSS, followed by metadata-bound root
commits and no per-inactive-root projection.

### Filesystem semantics

The proposal needs more than a path diff:

- lower-directory rename is `EXDEV` by default or uses backend-specific
  `redirect_dir` metadata;
- recursive rename/opaque normalization can be `O(subtree entries)`;
- hardlink groups that span changed and unchanged paths may require group-wide
  treatment;
- sparse files require extent-aware capture rather than writing logical zeros;
- chmod, ownership, timestamps, ACLs, file capabilities, and security xattrs
  have different privilege requirements;
- a promoted upper may contain metacopy/origin/index/redirect dependencies on
  its exact lower mount; and
- whiteouts must be represented without assuming `mknod`.

The cost model cannot be collapsed into “number of changed files”:

| Operation/semantic | Minimum honest work on the directory path |
| --- | --- |
| Directory merge / `readdir` | `O(sum visible entries across D lowers)` in the worst case, plus kernel dentry/name-cache allocation |
| Whiteout / opaque directory | `O(changed markers)` when authoritative; ambiguous recursive hiding requires an `O(subtree entries)` normalization walk |
| File rename | `O(1)` namespace records when the recorder is complete; replace/type changes add delete/create semantics |
| Directory rename / redirect | `O(1)` only inside an exact qualified recipe; clean-delta normalization may be `O(subtree entries)` |
| `chmod`, owner, time | `O(1)` metadata per inode, but may trigger metacopy/copy-up and privilege checks |
| Xattrs / ACLs / capabilities | `O(total canonical metadata bytes)`; reproduce admitted key/value bytes and semantics exactly or return a placement capability error |
| Hardlinks | at least `O(hardlink-group size)` when a changed inode aliases multiple names |
| Symlinks | `O(target bytes)` capture with byte-exact relative or absolute targets; targets are never rewritten |
| Sparse files | `O(number of logical extents)` with a proved extent API; a fallback scan is `O(logical file bytes)` and must not materialize holes |

Stage 04.6 qualification must prove that the OCI adapter reproduces every
canonical-v3 requirement advertised by the root on a capable placement.
Missing authority or filesystem support rejects that placement, not logical
publication. Phase 3 applies the same obligation to each future adapter
without changing the root. Silent normalization or per-adapter weakening is a
correctness failure.

### Depth and activation

OverlayFS directory lookup and `readdir` merge work grow with lower depth.
Per-open-directory merged name caches also consume kernel memory that process
RSS does not show. Upstream OverlayFS defines
[`OVL_MAX_STACK = 500`](https://github.com/torvalds/linux/blob/master/fs/overlayfs/params.h):
that is 500 total lower-directory entries, or at most 499 incremental
LayerStack carriers when one mandatory base consumes a lower slot. Docker
Engine's [`overlay2` driver separately documents support for 128 lower image
layers](https://docs.docker.com/engine/storage/drivers/overlayfs-driver/);
that product limit is not the upstream OverlayFS stack constant. Neither
ceiling is an acceptable hot-path target. EphemeralOS should keep the
projection target at `D_proj <=4` (at most five total lowers) and reject a
candidate projection at `D_proj >8` (above nine total lowers), starting
compaction before
`D_proj=4` is crossed. Logical history can contain 500 or 1,000 roots because
it is not replayed as 500 or 1,000 native lowers.

The exact platform ceiling is capability-probed and recorded. EphemeralOS
prefers the raw new mount API with repeated `lowerdir+` when that API is
available, but correctness retains the legacy mount API with one serialized
`lowerdir=` value. Candidate `D_proj=8` fits that fallback under the
qualified path-length bound. Docker Engine `overlay2`'s separate
128-image-lower limit, the kernel stack ceiling, and the legacy serialized
option-length limit must not be confused. The benchmark probes 499, 500, and
501 total workspace lowers only on a pinned host whose capability receipt
supports the new mount API; other hosts record the legacy byte/path ceiling
and still run candidate `D_proj` values through eight.

### Compositional verification and crashes

A child receipt can rely on a trusted parent receipt to prove construction,
but it cannot detect later mutation or bit rot in a privileged writable
carrier. Foreground full rehashing makes reuse slow; never rehashing makes the
claim unsafe.

The right split is:

- immutable construction receipt on the commit path;
- exact manifest and locator validation at activation;
- leases preventing locator deletion;
- optional `fs-verity` where supported;
- bounded scheduled full audits and corruption quarantine; and
- automatic reconstruction from the logical root after projection failure.

### Frozen-upper promotion

Promotion can be useful, but only with this terminal protocol:

1. stop command admission;
2. drain or terminate the complete process tree;
3. prove no writable file descriptor or shared writable mapping remains;
4. unmount every overlay using the upper/work directories;
5. complete data and metadata writeback and durably sync the upper;
6. reject or normalize unsafe overlay-private dependencies;
7. hash stable descriptors/inodes in that frozen epoch;
8. same-filesystem rename into store ownership;
9. durably publish payload locators; and
10. commit the root ref last.

An unmounted directory is not immutable while a writable descriptor survives.
`chattr +i` is not the solution: it requires `CAP_LINUX_IMMUTABLE`, which is
not implied by `CAP_SYS_ADMIN`. Continuation after this terminal freeze
requires a new private upper.
Here immutability is a storage-service ownership and reachability invariant,
not protection against a hostile privileged process that can open the backing
store directly. If untrusted sandbox code can reach that backing directory,
safe promotion is impossible and must be rejected.

A rename plus parent-directory `fsync` does not make dirty file data durable.
The qualified directory-path choices are both costly and must be measured: sync every changed
file/directory in the sealed upper (`O(Delta_e)` sync calls), or await a
grouped `syncfs` whose latency can include unrelated dirt on the same
superblock. If neither can be isolated and bounded, publication must copy the
payload into a journaled pack and sync that pack once. That fallback gives up
zero-copy adoption but preserves correctness.

Even a correctly frozen raw upper is not a generic carrier. With OverlayFS
`index=off`, copy-up of one name in a lower hardlink group can break the
expected cross-name relationship. With `index=on`, origin/file-handle metadata
binds the upper to exact lower filesystem identities. Lower-directory rename
also depends on `redirect_dir` behavior. Therefore the accelerator is an
**exact frozen mount-recipe bundle**, not a raw directory: upper plus required
overlay-private state, exact lower generation/filesystem identities, mount
options, and a capability receipt are all pinned and semantically reprobed. A
raw directory alone is never remounted or rebased as a generic lower. A
reusable projection must normalize the bundle into a clean delta:
canonicalize whiteout/opaque/redirect semantics, reconstruct hardlink groups,
emit a manifest, and complete the durability receipt. Normalization is
`O(E_upper)` metadata work even when same-filesystem payload inodes can be
adopted without copying bytes.

### The CAS-first contradiction

The current plan first writes durable CAS truth and then promotes an upper. It
also claims that promotion adds no second payload. Both cannot be true for new
unique bytes.

There are only three honest choices:

1. retain both copies and fail the duplicate-payload gate;
2. make the sealed carrier a durable physical locator, committing root and
   locator under one recoverable owner; or
3. evacuate unique chunks into packs and delete the redundant carrier before
   declaring the root settled.

The recommendation uses choices 2 and 3. Logical content hashes remain truth;
carrier paths and offsets are replaceable locators.

### CAS and CDC verdict

Do not throw away content addressing; throw away **loose-object CAS as the
foreground physical data path**.

The Stage 03 Merkle root and content digests are what make one checkpoint
backend-neutral, independently verifiable, structurally shared, and portable
across OCI, Firecracker, and WASI. SeqCDC remains useful for insertion-local
history sharing and for evacuating old bytes from a whole-file directory upper.
Neither property requires one filesystem object per chunk or reconstruction
through the chunk store on every activation.

Keep the existing canonical chunk policy during this stage to preserve
identity and golden vectors. Store its bytes in adopted ranges and packs.
Benchmark fixed-block and whole-file physical layouts inside projections;
those layouts may change freely because they are not identity. Replacing the
canonical chunk policy itself is a later schema migration only if matched
deduplication, CPU, metadata, and range-edit evidence beats SeqCDC.

### Assessment of the Shepherd/LayerStack recommendation

The additional
[`design_recommendation_from_sheppard_combined_with_layerstack.md`](design_recommendation_from_sheppard_combined_with_layerstack.md)
gets the central timing boundary right: Shepherd-style upper rotation can make
post-setup branch handoff and exact-recipe remount fast, but it does not include
LayerStack's hashing, durable publication, attribution, or cross-host
recovery. This review retains its strongest idea as the exact frozen
mount-recipe OCI fast path.

It should not be adopted unchanged:

- CAS-first publication plus later upper adoption either duplicates new bytes
  or creates a cross-owner gap;
- a raw upper is not generically reusable across lower recipes because of
  hardlinks, origin/index, redirect, whiteout, and opaque semantics;
- sync and validation must form a measured hash-and-durability receipt;
- an operational `D_proj` of 16 is too high for an ultra-fast lookup/readdir
  path; use target 4 and candidate activation cap 8 even though the upstream
  OverlayFS lowerdir ceiling is 500;
- directory OverlayFS still has whole-file data copy-up; and
- loose chunk objects plus complete-carrier fallback do not solve cold
  projection latency.

The recommended hybrid therefore incorporates zero-payload-copy rotation only
at a branch/projection boundary after strict quiescence, ownership transfer,
durability, and exact-recipe bundle pinning/reprobe. Ordinary logical
publication uses a non-rotating capture epoch. Normalized deltas, packed/adopted
locators, and backend-independent projections handle the cases the isolated
recommendation leaves open.

## Candidate comparison

Notation:

- `B`: all logical payload bytes;
- `E`: all filesystem entries;
- `Delta_b`, `Delta_e`: changed bytes/ranges and entries;
- `F`: size of a changed file;
- `D_proj`: incremental LayerStack delta/carrier lower count above one
  mandatory base (`total_overlay_lowers = 1 + D_proj`);
- `P`: bytes actually touched by the first workload after a lazy activation;
- `H`: retained unique history.

“Ready” means a usable workspace plus a bounded probe, not a complete read.

### Cost and behavior

| Architecture family | First/full ingestion | Incremental publication | Workspace ready | First complete read | Tiny edit in large file | Many-small cost | Fork / rollback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Current complete native carrier | `O(B+E)` CAS plus `O(B+E)` carrier | effectively `O(B+E)` for a new complete carrier | `O(B+E)` on miss | native `O(B)` | `O(F)` copy-up, then complete rebuild | `O(E)` loose objects and native inodes | ref cheap; miss reconstructs |
| 2. Directory-native delta/carrier vector | `O(B+E)` initial | `O(sum F_changed + Delta_e)` | `O(D_proj)` mount, lookup/scan depth-sensitive | `O(B)` plus layer lookup | `O(F)` and retains full changed file | `O(Delta_e)`, inode/whiteout explosion | ref `O(1)`; activation `O(D_proj)` |
| 3. Frozen-upper promotion | `O(B+E)` initial | seal `O(sum F_changed + Delta_e)`; native handoff `O(1)` | `O(D_proj)` | `O(B)` | first write and retained upper remain `O(F)` | seal `O(Delta_e)`, no second native copy | cheap if exact vector is safe/cached |
| 4. Block-level CoW/content-addressed block image | `O(B/blk + E)` | `O(dirty blocks * log B + Delta_e)` | root-map switch/mount `O(1)` to metadata | `O(B)` media-bound | `O(dirty blocks)` | metadata image `O(E)`, packed payload | `O(1)` persistent root |
| 5. Immutable filesystem image | image build `O(B+E)` or metadata-only `O(E)` | usually image/delta build `O(Delta_b+Delta_e)`; tool-dependent | mount `O(1)` | `O(B)` | writable OverlayFS still `O(F)` unless paired with range-CoW | compact metadata, good scans | image ref cheap; rebuild on miss |
| 6. Lazy CAS-backed filesystem | index `O(E)` or persistent root reuse | `O(Delta_b+Delta_e)` with tracked writes | mount/root switch `O(1)` | deferred `O(B)` plus fetch/verify | range-local with authoritative write tracking | lookup/metadata server pressure `O(E)` | `O(1)` roots |
| 7. Hybrid Merkle checkpoint + independent projections | one logical `O(B+E)` pass; projection optional | persistent-path update `O(Delta_b log B + Delta_e log E)` when ranges known; qualified directory fallback `O(sum F_changed)` | stored projection `O(1)`; qualified directory miss `O(B+E)` | `O(B)` and reported | range-local on block/WASI/reflink path; `O(F)` on the qualified OCI directory path | persistent metadata and packs; native projection only for active/hot roots | logical `O(1)`, projection activation separate |
| 8. Whole-file object/hardlink checkout | `O(B+E)` | `O(sum F_changed+Delta_e)` | `O(E)` namespace checkout | `O(B)` | `O(F)` and whole-file history | inode-heavy, metadata-dependent hardlink safety | refs cheap; checkout `O(E)` |

### Operational fit

| Architecture family | Crash recovery / verification | Portability | Privilege or device | Memory | Settled / peak space | Phase 2 | Phase 3 | Delivery and maintenance risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Complete carrier | simple but expensive deep verify; staged full copy | strong OCI fallback | `CAP_SYS_ADMIN` for OverlayFS | bounded streaming | one current full tree plus full reconstruction peak | inactive roots need CAS, cold winners hydrate | weak for Firecracker/WASI | low implementation risk, fails goals |
| Directory delta vector | journal + exact vector leases required; later mutation is dangerous | ordinary Linux directories; host-FS semantics leak into projection | OverlayFS mount; backing FS must support required xattrs/`d_type` | process bounded; kernel dentry cost grows with depth | full-file CoW, inode/depth amplification | good only with strict cache/depth quota | poor as cross-backend primary | medium-high semantic risk |
| Frozen upper | ownership handoff is one recoverable transaction; strict quiescence | same as directory vector; same-FS rename needed for zero-copy | same plus metadata-capability caveats | bounded seal | avoids second native copy, not first copy-up or CAS duplicate | fast tracked publications if carrier locator is pinned | useful OCI optimization only | high crash/TOCTOU risk unless protocol is exact |
| Block CoW image | journaled page/root commit; hierarchical maps | logical format portable, transparent OCI projection is not universally available | OCI generally needs reflink, FUSE, loop/NBD/dm, custom FS, or new-enough file-backed FS | bounded mmap page cache | excellent range sharing; map metadata must be hierarchical | excellent | excellent Firecracker; direct WASI possible | high initial implementation risk |
| Immutable FS image | image digest/fsck plus atomic catalog | image bytes portable only to matching readers; root semantics must remain separate | EROFS/SquashFS kernel/tool and sometimes loop/FUSE; file-backed EROFS is kernel-version-dependent | compact/mmap metadata | compact settled; building may create a full peak image | excellent read sharing | strong Firecracker disk; WASI needs independent reader | medium-high, ecosystem-dependent |
| Lazy CAS filesystem | journaled CAS + mount daemon; verify on demand | semantic format strong; OCI mechanism weak without FUSE/custom runtime | FUSE/device/helper or custom kernel; WASI needs none | cache and request queues require hard caps | excellent until hot cache; account cache explicitly | excellent | natural WASI, possible VM server | high runtime/operations risk |
| Recommended hybrid | single checkpoint/locator journal; projection receipts are disposable | one logical root, qualified OCI directory projection, independently rebuildable adapters | qualified directory path needs no additional device beyond mount authority; accelerators are probed and optional | fixed workers, permits, mmap cache | targets `C_current + H_unique + M`; directory-path large-file peak admitted | strongest fit: roots only, bounded active projections | strongest fit: native OCI, block VM, direct WASI | medium-high migration risk, low long-term coupling |
| Whole-file/hardlink checkout | simple receipts; metadata aliasing must be controlled | filesystem/link constraints | same-FS hardlinks; no reflink required | bounded | no duplicate payload for identical whole files; poor version dedup | acceptable hot cache only | weak VM/WASI primary | medium; insufficient alone |

No candidate satisfies every performance cell on every permitted host. The
hybrid wins because it preserves one backend-neutral truth while allowing the
best available projection, and because its qualified fallback fails
performance honestly rather than correctness silently.

## Recommended architecture

“Backend-neutral” means one logical identity and semantic contract, not one
physical representation forced onto every runtime:

| Layer | Backend-neutral contract | FUSE/KVM dependency |
| --- | --- | --- |
| `RootId`, `AttributionRootId`, checkpoint/ref journal | identical for OCI, Firecracker, and WASI | none |
| `CheckpointStore`, `PayloadStore`, `Publisher`, fork/prune/rollback | storage implementation is replaceable; every locator is outside logical identity | none |
| OCI adapter | consumes the common root and emits a qualified Linux projection; readiness never executes an image binary | qualified directory path requires neither FUSE nor KVM |
| WASI adapter | consumes the same common root through an in-process namespace/extent provider | neither FUSE nor KVM |
| Firecracker adapter | consumes the same common root through an independently built guest filesystem projection | no FUSE; executing Firecracker inherently requires Linux KVM and `/dev/kvm` |
| optional accelerators | must preserve the same root and fall back to the qualified directory path or reject placement | only the selected accelerator's declared capability |

Thus Docker images and host-specific paths never shape checkpoint identity.
The control plane can run above different host operating systems, while each
execution adapter is placed in an environment that actually supports that
runtime. Forbidding KVM globally would remove Firecracker execution, not
change the checkpoint architecture.

The component boundaries below are intentionally few and correspond to
independent replacement or failure domains:

| Component | Owns | Must not own |
| --- | --- | --- |
| `AttemptSealer` | command quiescence, writable-FD/mapping drain, hash-and-durability receipts | logical identity or branch refs |
| `ChangeRecorder` | backend-specific authoritative changes and durable cursors | content truth or projection policy |
| `CheckpointStore` | canonical Merkle objects in immutable packed/page runs, legacy loose-record reads, checkpoint journal, root/ref OCC | Linux paths, mounts, image IDs |
| `PayloadStore` | immutable payload IDs, locators, packs, leases, evacuation | logical namespace semantics |
| `Publisher` | one bounded publication pipeline over the preceding interfaces | backend activation |
| `ProjectionStore` | rebuildable projection keys, generations, receipts, quotas | authoritative checkpoints or sole-locator ownership |
| `OciAdapter` now; frozen future `FirecrackerAdapter` / `WasiAdapter` boundaries | backend capability proof, projection build, activation | `RootId` construction |
| `Verifier` | semantic oracle, receipt validation, audit, quarantine | ref selection |
| optional accelerator plug-ins | proved range-CoW, image, or lazy fast paths | correctness fallback or identity |

An interface is added only where these implementations really vary.
Checkpoint and payload durability share one journal owner so there is no
distributed transaction between two “truths.”

The Stage 04.6 implementation has no SQL or key-value database, embedded
database engine, database server, or database daemon. A “catalog” here is an
immutable sorted run/index plus an atomically selected manifest; the bounded
journal is a file-format protocol, not a database. Readers stream or use
bounded read-only `mmap`. This avoids a hidden second source of truth and is
also enforced by the zero-new-external-dependency gate.

### 1. A complete logical root with structural sharing

Stage 03 already defines a complete logical filesystem through
`RootRecordV3`, persistent `TreePage` nodes, `FileNode`, `SegmentPage`, and
content-addressed chunks. Preserve those canonical encodings and golden
vectors. Conceptually, the existing root participates in:

```text
RootRecordV3 {
    required_capability_bits
    chunk_profile_id
    root_directory_file_node_id
}

CheckpointRecord {
    root_id
    attribution_root_id
    parent_checkpoint          // history only
    created_by
    immutable_receipt
}
```

The exact encoding must be canonical and golden-tested. `RootId` hashes the
logical filesystem state, not the parent path used to reach it. History and
selection refs associate `RootId` and `AttributionRootId` atomically without
putting backend information into either identity.

The existing v3 capability bits and canonical node semantics are the
cross-backend contract; Stage 04.6 does not reduce that contract to suit the
least-capable adapter or insert a field into `RootRecordV3`. Stage 04.6 qualifies
the OCI implementation. Firecracker and WASI consume the same contract and
independently qualify it in Phase 3.

The existing namespace is a bounded, fixed-fanout persistent Merkle tree. A publication
path-copies only pages containing changed directory entries or inode records.
Each root is consequently a complete view without duplicating the complete
manifest and without replaying a logical layer chain.

The existing v3 regular-file encoding has explicit zero/hole/chunk extents in
fixed-fanout `SegmentPage`s; it has no inline-small-file payload form. The
on-disk hierarchy permits bounded traversal, but the current implementation
still materializes root-sized vectors in `FileSnapshotV3::Regular`,
`build_segments`, and `reconstruct_segments`. Stage 04.6 must replace those
publication/materialization call sites with streaming page builders/cursors
while preserving canonical bytes and golden IDs. The current SeqCDC policy
remains the initial deterministic chunker because it localizes insertions. A
different canonical chunking policy requires a new logical schema and
migration evidence; a backend projection may choose any physical block layout
without changing `RootId`.

This representation makes:

```text
fork                  = create ref to existing checkpoint
rollback              = compare-and-swap selected checkpoint ref
logical ancestry prune = external checkpoint-history metadata update
root equality         = RootId equality
namespace update      = O(Delta_e * log E)
range-aware file edit = O(local rechunk halo + changed extent-tree pages)
```

Logical ancestry prune is the ultra-fast **logical squash** semantics.
Stage 04.6 changes public `squash_layerstacks` to this operation: it
atomically creates/selects bounded external checkpoint-history metadata while
preserving exactly the same `{RootId, AttributionRootId}` and moving no
payload. If attribution changes, that is a normal attribution publication
with changed-page cost, not an `O(1)` prune. Physical flatten/remount becomes
separately timed internal maintenance and is excluded from the public squash
response. `checkpoint_refs_v2` gates the semantic migration and retains the
old implementation as rollback through the observation window.

Committed rollback is not public in the current generated catalog. Stage
04.6 is not complete until ProductAccess exposes it and the generated catalog
contains the implemented operation; this review deliberately does not invent
its eventual CLI spelling. Logical ref selection is metadata-only.
Workspace-ready rollback meets the hot target only when a compatible local
projection exists; a cold historical root is separately timed against its
projection-build/acquisition floor.

### 2. Immutable payloads with replaceable locators

A content hash has one logical meaning and one or more physical locators:

```text
PayloadId -> [
    sealed_native_file(file_token, offset, length),
    append_pack(pack_id, offset, length),
    adopted_extent(payload_owner_id, offset, length),
    remote_object(provider_key)
]
```

`PayloadId` is the existing typed v3 `Chunk` ID, not a new digest, identity,
or second content truth.

Locator type and location never enter `RootId`. Locator runs are immutable,
checksummed, generation-selected, and leased. A reachable payload must have at
least one durable, verified locator before its checkpoint ref can commit.
The locator index uses fixed-size persistent pages and range-compressed runs;
a flat chunk/block vector copied per file or root is forbidden. Readers keep a
bounded cursor, not a root-sized in-memory map.

Every physical payload owner also has an immutable, generation-selected
reverse manifest:

```text
PayloadOwnerId -> sorted [
    (owner_offset, length, PayloadId, locator_ordinal)
]
```

Evacuation and retirement use this manifest; they never scan the store hoping
to rediscover references. There is at most one reverse entry per installed
locator range and at most `64` encoded bytes per entry plus half-full
`16 KiB` pages. The `100,000` bound is per immutable manifest **shard**, not
per physical owner. An owner root range-indexes as many non-overlapping shards
as its exact locator count requires, and that fixed-page shard index is
selected atomically with the forward locator generation. A 1 GiB file at the
canonical 8 KiB minimum has at most 131,072 ranges and therefore needs at
most two shards; it is never rejected by a 100,000-owner-entry limit.
Builders create at most 100,000 reverse records per bounded batch under one
ownership group and a bounded cursor. Shard count is derived from exact owner
length/count and the admitted workspace byte/inode quota; there is no flat
per-owner vector. The forward index's 600,000/1,200,000-record maintenance
thresholds apply to unreachable/replacement debt, not live manifest capacity.
Reverse metadata is charged to `M`, and a reverse generation is removed only
after its prior selector and leases retire. Crash and cancellation injection
must bracket every forward/reverse selector boundary.

“Runs” are leaf encodings inside one generation-selected persistent B+tree,
not an LSM stack searched newest-to-oldest. Both payload-locator and canonical
metadata indexes have one selected root, `16 KiB` pages, maximum height 6,
and at most 8 page reads for a point lookup: one selector, at most six tree
pages, and one generation/locator-value page. Internal entries use a fixed
bounded encoding; occupancy proof never relies on hash-key prefix
compression. Foreground split/merge keeps non-root pages at least half full
before selection; a builder that cannot meet the height/occupancy bound
bulk-builds a replacement tree or returns bounded backpressure. A commit
path-copies pages into one new root; it cannot append another lookup level.

One worst-case lookup pins at most `8 * 16 KiB = 128 KiB` of index pages.
Four concurrent storage lookups pin at most `512 KiB`; completion and
cancellation release every pin. Index maintenance uses at most eight
`64 KiB` merge buffers (`512 KiB`). Both amounts consume the declared
mmap/index window and storage byte permits and are already included in the
aggregate memory-domain cap.

A locator value occupies at most one `16 KiB` page and selects at most four
physical locators. One block-image locator may contain at most nine spans for
a maximum-size `32 KiB` canonical chunk; greater fragmentation first
evacuates that chunk to a bounded contiguous pack locator rather than creating
an overflow chain. Underfilled-page, unreachable-index, dead-pack, and
journal-owned replacement debt starts maintenance at `256 MiB`, 600,000
records, or 10 jobs and hard-backpressures at `512 MiB`, 1,200,000 records, or
20 jobs, whichever comes first. Maintenance uses the same worker/byte permits.
Warm-lookup qualification includes maximum-scale history so an unbounded run
chain cannot hide behind a small fixture.

`remote_object` is not an accounting escape hatch. Each remote generation
reconciles canonical live bytes, provider-allocated bytes, billed bytes
(including minimum object size, multipart remnants, and retained versions),
replication policy, and deletion receipts. Local qualification runs set remote
bytes to zero. A remote-enabled profile reports
`T_estate = T + R_remote_allocated` and a policy-adjusted ideal denominator;
unexplained remote bytes or unbounded version/multipart retention fail just
like local leaks.

Only `freeze_for_branch` may use an upper inode as a durable locator. After
quiescence, exact-head validation, irreversible ownership transfer, and
removal from every writable mount, the publisher reads each changed file once,
chunks and hashes it once, and may record new chunk ranges against that frozen
storage-owned file. The same inode may then serve the OCI delta. A continuing
mutable upper is never adopted, hardlinked, reflinked, or otherwise referenced
as immutable payload; its newly reachable bytes must already exist in durable
immutable packs before ref commit.

An arbitrary user-owned initial checkout is not adoptable merely because it
can be opened or hardlinked: the user could still mutate the shared inode.
Unless the source is already storage-owned, immutably sealed, and transferred
under the locator transaction, first ingestion streams it into packs and
charges that write to the operation.

Evacuation later copies only still-needed unique chunks into bounded
append-only packs, publishes the replacement locator run, marks the old
generation `Retiring`, and performs only a bounded lease-drain attempt. A live
lease leaves an accounted but explicitly non-settled, journal-owned retiring
generation. It does not delay the logical ref response, but admission
backpressures at the hard retirement byte/count quotas rather than hiding or
calling it settled. A sealed pack is hard-bounded at
`64 MiB` payload, `100,000` records, and `80 MiB` total allocation. A GC or
compaction transaction handles at most the minimum of `64 MiB`,
`100,000` records, the operation's remaining five-percent payload-staging
headroom, the global byte permits, and available disk admission.
Settled pack dead/slack allocation must remain `<=2%`; exceeding it fails the
release space gate. These are physical format limits, not identity rules.
Pack install performs grouped durability rather than one `fsync` per
8--32 KiB chunk.

Non-adoptable input uses the same one-pass chunker but streams new chunks into
packs. It does not first create loose objects or a hidden full staging tree.

Qualified directory hydration must not leave those same current bytes
permanently in both packs and a native tree. A crash-safe
**hydrate-and-adopt** transaction
therefore:

1. creates each reconstructed regular-file inode directly inside a
   storage-owned immutable generation, streams the canonical chunks once,
   preserves sparse/hardlink/metadata semantics, and durably verifies it;
2. exposes that same storage-owned namespace directly as the lower; no hidden
   storage link is created, and canonical hardlink groups contain exactly
   their workload-visible directory entries;
3. installs a new immutable locator run mapping the file's canonical chunk
   ranges to the verified native inode while every old pack locator remains
   readable;
4. selects the locator generation only after the native bytes and semantic
   receipt are durable, then installs/probes/selects the projection receipt;
   and
5. compacts mixed packs in bounded transactions, copying only history-only
   records that still lack another locator, then retires the now-redundant
   current-root pack records after leases drain.

The journal states are `Building -> BytesDurable -> SemanticsVerified ->
AdoptLocatorsDurable -> ProjectionReady -> CurrentPublished ->
AccountingReady -> SourceLocatorsRetiring -> MaintenanceSettled`. Before `AdoptLocatorsDurable`,
cancellation/recovery may delete the journal-owned build. At and after that
state, the native generation is payload-owned and cannot be
cancellation-deleted: recovery finishes the projection, keeps it as a
payload-only owner, or evacuates it through the ordinary locator protocol.
It never exposes a root without a durable locator.

`AccountingReady` means that every allocation has exactly one ledger owner
and `P_staging` contains only declared in-flight work; it is not a
settled-space pass. `MaintenanceSettled`—called “settled” in every release
table—requires evacuation complete, `P_staging = 0`, the avoidable-duplicate
gate satisfied, and no lease blocking retirement.

Before the first side effect in each bounded ownership phase, the transaction
durably appends and syncs **one umbrella intent** naming the exact owner,
reserved namespace token/range, allocation ceiling, cleanup action, and hash
of an immutable streamed batch manifest. Creates, preallocations, payload
writes, and renames named by that manifest use grouped durability; no WAL
record or sync occurs per file, chunk, or directory entry. Selector
installation and retirement are later ownership phases with their own
umbrella intent and durable completion. There are at most eight durable phase
transitions per operation. The `<=256 KiB` pending record stores manifest
roots and bounds rather than a million-entry list; manifest pages/spool are
journal-owned and charged to `M`. Crash injection brackets every phase
intent, grouped allocation/sync, rename, forward and reverse selector update,
lease transition, and deletion. Recovery follows only bounded pending
journals and owner manifests; it never enumerates the storage namespace.

The native target is the one `C_target` hydration allowance, not a hidden
second native staging copy. During the switch, both old source packs and the
target are charged; after the declared settle deadline, current payload is
charged once through its native locator and only genuinely unique history
remains packed. Failure to reach that shape is a space-gate failure.

Payload packing alone is insufficient. Canonical `FileNode`, `TreePage`,
`SegmentPage`, metadata, hardlink, and attribution records also install as
immutable packed/page-object runs with grouped durability and legacy
loose-record dual-read. Otherwise the current temp/write/fsync/link/unlink/
parent-fsync sequence repeats per record and recreates the many-small-file
storm. Canonical bytes and typed IDs remain unchanged.

This locator layer is not a second source of logical truth. It answers only
where verified bytes can currently be read. If every projection is deleted,
the checkpoint remains valid while its logical payload locators remain.

Files adopted as locators are moved under `PayloadStore` ownership before
commit; they are not owned by `ProjectionStore` merely because a projection
also references their inodes. Likewise, an adopted extent that is the sole
durable locator pins its payload-store allocation even if a projection
namespace references it. Projection eviction must first install an
alternative locator, switch its generation, and drain leases. “Disposable
projection” means rebuildable and logically non-authoritative, not deletable
while it contains the last reachable bytes.

Accordingly, “upper reclaimed” has two distinct outcomes in telemetry: an
unretained session upper is physically deleted, while an upper explicitly
frozen for a branch/projection boundary leaves session ownership and becomes
an inventoried immutable payload owner. The latter is an ownership transfer,
never a deletion claim. Ordinary logical publication does not reclaim,
freeze, or rotate the active upper.

### 3. Immutable capture receipts, then an authoritative change recorder

The fastest post-setup commit cannot be created by moving required work
silently before the API timer. A normal checkpoint copies newly reachable
payload into immutable packs but leaves the active OCI upper mounted and
mutable after commit. `AttemptSealer` continuously converts an idle execution
epoch into a reusable **hash-and-durability receipt**:

```text
RUNNING
  -> QUIESCED_CAPTURING
  -> PAYLOAD_SYNCING
  -> EPOCH_RECEIPT
  -> COMMITTED
```

- entering `RUNNING` immediately invalidates an uncommitted candidate; after
  commit it starts a new recorder epoch in the same upper;
- notification streams are hints that schedule work, never proof of
  completeness;
- the candidate records the exact upper epoch, stable file identities,
  authoritative change cursor, hashes, immutable payload-locator generation,
  dirty bytes written, durability method, and completed sync boundary;
- only a quiesced epoch with no process, writable FD, or shared writable
  mapping can become authoritative; and
- cancellation or a new command abandons the candidate and releases all
  memory, FDs, and permits.

For a continuing mutable upper, a receipt is authoritative only when every
newly reachable payload byte already has a durable immutable pack locator; a
hash of bytes that the next command can mutate is not a receipt. An upper may
serve directly as a locator only after the separate branch/projection
transaction freezes it and transfers it to storage ownership.

A checkpoint with a matching completed receipt can be metadata-bound. Without
one, the public operation synchronously performs and times the missing scan,
hash, writeback, and sync work. Benchmarks report both mutation-to-durable-root
latency and the final checkpoint-call latency, so pre-sealing is an
optimization, not timer fraud.

`ChangeRecorder` is a real replaceable boundary because backends expose
different information:

| Recorder | Information | Publication behavior |
| --- | --- | --- |
| Qualified directory upper | semantic paths and metadata; changed file as a whole | one scan of each changed file; `O(sum F_changed)` |
| Reflink-aware Linux upper, after a proving probe | changed/unshared extents plus semantic paths | bounded range rechunk and path updates |
| Block-CoW workspace | dirty block/range bitmap plus filesystem semantic journal | bounded range rechunk and path updates |
| Firecracker block adapter | backend-owned CoW disk-extent journal plus guest semantic export | dirty extents; adapter validation required |
| WASI provider | exact host calls, ranges, and metadata mutations, only when all mutations are provider-mediated | direct persistent-tree update |

Path-only notification (`inotify`/`fanotify`) is a hint, not an authoritative
range recorder: it does not prove byte ranges for arbitrary writes, mmap,
truncate, or crash recovery. It must never activate the range-fast correctness
path by itself.

The change recorder records durable cursors with bounded disk-backed state.
If its evidence is missing or inconsistent, publication falls back to a
whole-changed-file scan. It never guesses from directory presence.

### 4. One publication owner and one crash state machine

The current split between CAS truth and later carrier adoption creates a
cross-authority gap. The replacement gives checkpoint objects, payload
locators, and root/ref publication to one `CheckpointStore` transaction
owner. Large I/O still happens outside the short ref writer lock.

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

These are logical substates and observability labels, not one WAL sync per
arrow. Adjacent labels sharing an ownership boundary use one umbrella durable
phase, and an operation never exceeds the eight-transition durable-phase cap.

Rules:

- `REF_COMMITTED` is the only visibility point.
- The ref commit is a short OCC compare-and-swap after all required data is
  durable.
- A hot publish may return only after its requested compatible projection is
  selected and probed; a logical checkpoint for an inactive node needs no
  projection at all.
- A crash before `REF_COMMITTED` leaves a journal-owned orphan that recovery
  finishes or reclaims.
- A crash after it always finds a complete logical root and at least one
  locator per reachable payload.
- A projection receipt may commit later; projection failure cannot invalidate
  the logical root.
- If requested activation fails after `REF_COMMITTED`, the public result is
  structured as `checkpoint committed; activation failed`, includes the
  `RootId` and retryability, and never reports publication as rolled back.
- Recovery scans bounded pending journals, not the complete object store.
- Cancellation changes journal ownership and releases all permits, FDs,
  leases, and staging inventory through structured cleanup.

Ordinary post-setup `add layer`/checkpoint publication is therefore a
**non-rotating logical epoch commit**. After `REF_COMMITTED`, the
change-recorder cursor advances atomically and the already-mounted private
upper is immediately ready for the next command. It adds no lower, changes no
mount, and cannot force physical flattening. A pre-ref failure preserves the
prior dirty epoch; post-ref recovery advances or reconstructs the cursor
before admitting work.

Only a request for a branchable native recipe, or attempt close, invokes a
separate `freeze_for_branch` transaction. The quiescent upper must exactly
match the committed head; ownership transfers, each continuing sibling gets a
new private upper, and any resulting `D_proj` growth/compaction is charged to
that fork/projection boundary. A historical or post-head fork uses a cached
compatible projection or the separately timed projection-build path. This
separation is what prevents the 64/1,000 non-closing logical-layer sequence
from paying a periodic full-directory flatten.

### 5. Disposable projections

The projection key remains:

```text
(RootId, backend_kind, backend_format_version, target_profile)
```

It always excludes `AttributionRootId`. If a backend embeds attribution, that
is a separately keyed auxiliary artifact/generation. Attribution is queried
from the logical checkpoint, not inferred from native inodes.

Preserve the useful existing projection-generation discipline:
`Building -> Ready -> Published -> Terminal`, an immutable `MANIFEST`, an
explicit `STATE`, and an atomic `CURRENT` selector. Directory presence never
means ready. Projection generation state remains separate from logical
checkpoint visibility.

#### OCI/Linux qualified no-extra-device projection

Use sealed directory deltas and a complete-directory fallback because they
work on the broadest ordinary Linux filesystem matrix. At a
`freeze_for_branch` or attempt-close boundary, changes have two paths:

1. retain the exact frozen mount-recipe bundle (upper, required overlay state,
   exact lower/filesystem generations, mount options, and capability receipt)
   as a short-lived local accelerator; or
2. normalize it into a clean immutable directory delta before reuse with a
   different lower recipe or across restart assumptions.

The bundle is semantically reprobed before reuse. A raw upper directory alone
is never remounted/rebased as a generic lower, is never the only durable
logical truth, and never receives a backend-neutral identity. Keep:

- operational projection depth `D_proj <=4` (`<=5` total lowers);
- hard activation depth `D_proj <=8` (`<=9` total lowers);
- capability receipt records both the selected mount API and its probed
  platform ceiling: expected 500 total lowers on a qualified new-mount-API
  kernel, where one mandatory base leaves at most 499 LayerStack carriers;
  the correct legacy fallback records its serialized option/path ceiling
  instead;
- one new private upper/work pair for continuation;
- a fixed active-attempt cap and a small quota-controlled idle projection
  cache; and
- packed `PayloadStore`/Merkle hydration as the correct projection-miss
  fallback.

A complete hydrated directory is a quota-controlled projection shared as an
immutable lower by compatible active siblings. It is never retained once per
logical root or copied once per agent. On a qualified directory-projection
miss it is built by the hydrate-and-adopt transaction above, so the finished native
allocation replaces redundant current-root pack locators rather than becoming
a permanent second payload copy. If locator evacuation cannot settle within
the declared byte/time quota, this fallback fails qualification.

A normal logical squash does not invoke this compactor. When depth or storage
debt requires physical normalization, the compactor either retains an exact
immutable lower/locator recipe or performs a separately timed, admitted
evacuation/build. It never creates hidden cross-generation hardlinks:
additional directory links would change workload-visible `st_nlink` and can
couple inode metadata across generations. Every copied allocation is charged
to `P_staging`, and source plus target remain counted until selection and
lease retirement complete.

This path is correct and usually makes post-setup layer activation fast. It is
not claimed to be range-CoW.

#### Optional Linux accelerators

Probe, qualify, and independently gate:

- reflink/clone-aware copy-up plus a proved dirty-extent recorder;
- a content-addressed block-CoW workspace;
- file-backed EROFS metadata/data projections on kernels that support the
  required features;
- composefs-like external-object metadata images;
- FUSE/lazy projections when `/dev/fuse` and an allowed helper are explicitly
  available; and
- loop/NBD/device-mapper projections only when device access and policy permit
  them.

EROFS supports external data blobs and compact immutable metadata. Newer Linux
kernels support [file-backed EROFS mounts without a loop
device](https://erofs.docs.kernel.org/en/latest/features.html), but that is an
optional kernel-version-specific accelerator, not the qualified directory
path.

Each accelerator must reproduce the same logical root and pass the same
semantic oracle. Failed capability detection falls back; it never changes
identity.

#### Firecracker projection

The stock Firecracker fallback constructs a regular file-backed
filesystem image from the logical root; attaching that file does not require a
loop device. Stock Firecracker does not directly consume the proposed
hierarchical extent map. `O(1)` map activation is therefore claimed only for
a separately qualified userspace/custom block backend or conversion layer.
Within that optional layer, a flat map copied per root is forbidden and a
backend-owned CoW block layer may provide changed disk extents. Firecracker's
snapshot dirty tracking is guest-memory tracking and must not be mislabeled as
a virtual-disk dirty bitmap. Image ID, snapshot ID, guest inode numbers,
block-layer journal, and guest-memory bitmap never enter logical identity.

Writable sibling isolation uses one immutable shared base workspace image,
attached read-only to every compatible VM, plus one bounded private writable
guest upper/delta drive per active attempt. A versioned guest kernel mounts
that pair through its qualified union facility; the base is never writable
and stock execution never clones one complete base image per sibling. Private
drives have allocated-byte/inode quotas and admission control; a sparse drive
is allowed only after allocated-block accounting and sparse behavior pass.
Without that capability, the Firecracker placement is rejected rather than
preallocating a complete drive per sibling.

`target_profile` includes workspace filesystem kind, on-disk format version,
block size/features, image-codec/builder version, guest kernel/union profile,
and semantic-normalization version. Construction and readback use a declared
adapter-owned userspace codec or a versioned builder/verification guest;
neither path uses `/dev/loop` or an undeclared host tool. The result receives
a full semantic oracle before its projection receipt commits. A guest change
journal is only an optimization: after a gap or crash, a recovery guest
replays the guest filesystem journal and performs a timed full semantic scan
of the private upper, or rejects publication. It never trusts an incomplete
cursor.

Firecracker itself requires Linux KVM and read/write access to `/dev/kvm`, as
its [official prerequisites](https://github.com/firecracker-microvm/firecracker/blob/main/docs/getting-started.md)
state. `CAP_SYS_ADMIN` alone cannot supply the device or hardware
virtualization.

A stock filesystem image is a correct compatibility projection, but it is not
a free space optimization. Its allocated blocks count in `L_hot` while
retained and in `P_staging` while being built. Unless the image is also a
storage-owned, independently verified payload locator and total unique
allocation still passes the settled-space gates, it must be destroyed when its
active lease drains; it may not remain as a second complete packed-plus-image
copy. A stock-image miss therefore makes no 100x/500x activation claim. The
optional hierarchical block backend is the only proposed persistent
Firecracker projection allowed to claim localized allocation, and it must
qualify independently.

#### WASM/WASI projection

Resolve namespace and content extents directly in-process. The provider can
record exact writes and use the range-fast publisher without a kernel mount
only when every filesystem mutation is capability-mediated by that provider
and no host preopen or other bypass can mutate the backing bytes.
Every identity-bearing namespace, content, and metadata semantic must be
represented exactly or activation is rejected. Runtime capabilities may
differ by adapter; persisted semantics never silently weaken under the same
`RootId`.

### 6. Verification

Separate three questions:

1. **Was this immutable object constructed correctly?** Answered once by the
   commit receipt, canonical hashes, and durable locator transaction.
2. **Is this projection still the one described by its receipt?** Answered
   cheaply at activation using generation, manifest, capability, and immutable
   dependency checks.
3. **Has storage suffered later corruption?** Answered by read-time content
   verification where needed, scheduled bounded audits, optional `fs-verity`,
   and automatic quarantine/rebuild.

Exact-key reuse must not recursively hash 870 MiB. A cheap receipt check is
the expected path; any failed check falls back to a rebuild or a full audit
outside the activation lock.

## Quantitative performance contract

These are pre-measurement targets and hypotheses, not achieved results.
The preserved `baseline.json` has `n=1` for publication, materialization, and
explicit reuse, and `n=5` for warm lookup. Its computed 100x/500x values are
absolute ceilings, not percentile evidence. A speedup label requires matched
current and candidate distributions using the same outer boundary, placement,
and cache state. `p95` claims require at least 20 matched samples; any
sub-millisecond claim requires at least 100.

The 107.024-second reference is retained for absolute threshold continuity,
but a tiny edit must also be compared with the current implementation on the
same tiny edit. A result is not called “500x” until that matched denominator
exists.

The user's clarified 100x/500x objective is the post-setup layerstack path.
Accordingly, “cold” must not conflate a cold page cache with an empty worker.
A worker that already has a compatible immutable projection can activate it
without reconstructing bytes even when its page cache is cold. A genuinely
empty worker with neither projection nor payload must acquire or write the
required bytes; the qualified no-FUSE/no-extra-device directory path cannot guarantee
99.9 ms for 870.08 MiB and makes no such claim. Locality-aware placement,
prepositioning measured as its own product operation, or an independently
qualified lazy/block/image accelerator can change that result, but none may
move acquisition before the cold-placement timer.

| Operation and boundary | Current baseline | 100x threshold | 500x threshold | Recommended target | Expected result | Why physically plausible | Deferred or separately timed work |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Very first source-to-durable-root setup | legacy component: 107.024 s; true outer clock unmeasured | 1.070 s | 214 ms | `<=1.25x` measured one-pass floor; stretch `<=1.070 s` when floor permits | hypothesis after one-pass controls: adoptable 0.35--1.0 s; non-adoptable 0.8--2.5 s | one source read, parallel hash/chunk, no loose-object fsync storm, grouped pack commit | none hidden; walk, hash, install, verify, and durability included |
| Post-setup small layer publication with a matching hash-and-durability receipt, root durable | matched current small-delta baseline required | 1.070 s reference ceiling | 214 ms reference ceiling | `<=20 ms p95` | 2--20 ms p95 hypothesis | changed Merkle pages and locator metadata only; payload is already hashed and durable; grouped journal/ref commit | receipt preparation is separately timed and included in mutation-to-root latency |
| Post-setup small layer publication without a receipt | matched current small-delta baseline required | 1.070 s reference ceiling | 214 ms reference ceiling | one-pass floor plus one durable commit; no unconditional 500x promise | delta-dependent | scan, hash, dirty-byte writeback, and sync are physically required | none; every missing receipt task is inside this clock |
| Defined small mutation through durable root, forcing an immediate-post-command receipt miss | matched current end-to-end baseline required | 1.070 s reference ceiling | 214 ms reference ceiling | `<=1.070 s p95`; `<=214 ms` only when the matched divisor also passes | delta- and durability-dependent | one bounded changed-file/range pass plus grouped root commit; no complete-root scan | none; mutation, invalidation, scan/hash, writeback, sync, and root durability remain inside one clock |
| Sustained 64/1,000 non-closing small logical-layer commits: submission through same-upper next-command ready | matched current same-boundary sequence required | `<=1.070 s p95` and every sample `<=1.070 s` | `<=214 ms p95` only with matched divisor | release: `<=1.070 s p95/max`, no rejection/deferred readiness; preferred `<=214 ms p95`; internal `<=20 ms p95` | receipt hits 2--20 ms; bounded misses follow the measured delta floor | the commit advances a recorder epoch in the existing upper: no lower, remount, projection build, or flatten | asynchronous settlement is reported separately, but all admission/queue/backpressure, synchronous work, and delay induced in the next operation stay timed |
| Tiny-edit publish then `freeze_for_branch`/fork to locally stored child workspace, 64/1,000 sequence | constituent matched baselines required | publication `<=1.070 s`; activation `<=99.9 ms` | publication `<=214 ms`; activation `<=20 ms` | constituents remain separate; outer max `<=1.170 s`, preferred outer p95 `<=234 ms`; no rejection/deferred readiness | metadata-bound receipt/freeze/handoff until a bounded projection compaction is required | exact committed upper becomes an immutable recipe without a payload copy; compaction is pre-admitted and bounded | outer total is reported but never called a combined speedup; forced synchronous compaction is inside it and asynchronous settle must meet `D_settle` |
| Exact frozen-recipe selection/handoff | not measured | 99.9 ms materialization reference | 20.0 ms materialization reference | `<=20 ms p95` after a completed receipt | 1--10 ms hypothesis | select/probe an already durable exact recipe; no payload copy | execution copy-up, hashing, writeback, and sync remain visible in their own spans and the combined clock |
| Raw-upper normalization to reusable clean delta | not measured | no honest threshold before matched control | no honest threshold before matched control | `<=1.25x` matched one-pass upper-entry floor | `O(E_upper)` | each upper entry and overlay-private semantic is interpreted once; payload is adopted only when safe | independently timed; never included in the metadata-bound handoff score |
| One-byte edit in 1 GiB, qualified OCI directory publish | not measured | 1.070 s reference ceiling | 214 ms reference ceiling | `<=1.070 s` only when one-pass control permits | 0.2--1.2 s scan after an execution-time full copy-up | one sequential hash/chunk pass, no second payload write | first write/copy-up and peak 1 GiB upper are explicit; no 500x claim |
| One-byte edit in 1 GiB, range-CoW publisher | not measured | 1.070 s reference ceiling | 214 ms reference ceiling | `<=20 ms p95` publication | 2--20 ms | dirty extent plus bounded CDC halo and `O(log F)` Merkle pages | accelerator availability and the original write latency are separate |
| 100,000 new small entries | not measured | no honest threshold before matched control | no honest threshold before matched control | `<=1.25x` one-pass entry floor; stretch `<=1.070 s` | 0.2--2.0 s, hardware/filesystem dependent | one streamed entry pass, packed small payload, batched tree and journal pages | package execution/decompression excluded from publish but combined clock reported |
| Public `squash_layerstacks` logical ancestry prune after the Stage 04.6 contract switch | current physical command unmeasured; no accepted logical baseline | n/a | n/a | `<=20 ms p95` outer and `<=1 ms p95` service | 0.05--5 ms hypothesis | root and attribution pair remain identical; only external ancestry selection changes | an attribution change is separately published; physical flatten is not part of the response |
| Separate internal physical flatten / legacy public-squash control | unmeasured | not compared with logical squash | not compared with logical squash | throughput/control and settle gate, not sub-ms | `O(E)` metadata and any unavoidable locator evacuation | bounded maintenance outside the public logical-squash response and global writer lock | full old leased view, new metadata, and all evacuation bytes counted |
| Hot rollback/root switch to cached compatible projection | unmeasured | 99.9 ms reference | 20.0 ms reference | `<=20 ms p95` | 1--15 ms | ref CAS plus existing projection mount/root switch | command quiescence and first post-switch access reported |
| Cold rollback to a historical root without a compatible local projection | unmeasured | no honest absolute threshold before a matched physical control | no honest 500x claim | `<=1.25x` matched projection-build/acquisition floor | placement-dependent | logical selection remains metadata-bound, but required bytes or namespace metadata must be made usable | acquisition, projection build, verification, activation, and deferred reads are all timed |
| Cold-page-cache worker with a local stored mountable projection | cold complete carrier: 9.988 s | 99.9 ms | 20.0 ms | preferred `<=20 ms p95`; `<=99.9 ms p95` is the minimum 100x release gate | 3--20 ms p95 hypothesis | mount/metadata mapping, no byte reconstruction | first open, scan, reads, and write are mandatory sibling metrics |
| True cold placement: no local projection or payload | 9.988 s component reference | 99.9 ms | 20.0 ms | no false 100x promise; `<=1.25x` direct native-copy/transfer floor; release as correct fallback, not as a 100x result | roughly 0.3--3 s locally plus any measured transfer | bounded parallel sequential hydrate-and-adopt rather than loose-chunk opens; physical bytes must arrive | acquisition, full construction, locator switch, and settle all timed; optional lazy/block path gets a separate row |
| First 4 KiB access after lazy/image activation | not measured | n/a | n/a | report; local p95 `<=2 ms` hypothesis | 0.05--2 ms local | one metadata lookup and bounded object/page read | remote placement reported separately |
| First byte-reading full repository scan | not measured | n/a | n/a | throughput `>=0.8x` pinned native control | storage-limited, about 0.2--3 s | sequential/prefetched packed extents | all deferred bytes and verification reported |
| Random 4 KiB reads, warm local projection | not measured | n/a | n/a | latency/throughput no worse than `1.25x` native control | control-dependent | bounded page lookup; persistent mmap index | cold and warm distributions separate |
| First write plus fsync/copy-up | not measured | n/a | n/a | range path proportional to dirty allocation; fallback reported | range path 0.1--5 ms; directory large-file path `O(F)` | block/reflink CoW when proved | no publication headline may hide this cost |
| Explicit same-key reuse with a valid receipt | 6.362 s | 63.6 ms | 12.7 ms | `<=1 ms p95` | 0.05--0.5 ms | immutable receipt and catalog lookup, no payload traversal | receipt-hit rate is reported; misses include validation/rebuild work, while scheduled audit stays outside activation |
| Warm generation lookup | 35.375 us median | do not regress | do not regress | matched median and p95 each `<=1.05x` control and `<=control + 2 us` | hypothesis 30--37 us median | same keyed catalog lookup | no added deep verification |

Warm-lookup non-inferiority requires both the relative and absolute limits at
matched median and p95. A cold improvement that damages this path fails.

The historical ceilings alone do not establish a speedup against a changed
workload. For every “100x” label, candidate p95 must be no greater than both
the applicable historical ceiling and `matched_current_p95 / 100`; for every
“500x” label it must be no greater than both the historical ceiling and
`matched_current_p95 / 500`. Publication reports receipt-hit rate per
workload, plus the forced immediate-post-command miss above, so the
metadata-bound cell cannot hide a low hit rate.

## Space contract

Preserve:

```text
T(t) =
    L_hot(t)
  + H_cold(t)
  + sum(U_active(t))
  + P_staging(t)
  + M(t)

D_ideal = C_current + H_unique
```

All terms use unique allocated physical bytes. Hardlinks are deduplicated by
`(device, inode)`, sparse files use allocated blocks, and a reflink path must
obtain shared-extent accounting rather than count logical lengths. `M`
includes inode, directory, xattr, pack slack, locator, Merkle page, manifest,
ref, journal, lease, quarantine, and trash allocation.

Accounting precedence prevents double counting:

- payload-store adopted files and packs count once in `H_cold`;
- projection-only allocation counts in `L_hot`;
- a projection exposing the same storage-owned namespace adds no second
  payload allocation or hidden directory link;
- ownership transfer never counts the same allocation in two terms; and
- a sole-locator adopted extent is not disposable until evacuation installs
  and selects another durable locator.

These are release gates, not aspirational targets with a looser pass band:

| Space signal | Required release gate | Release failure |
| --- | ---: | ---: |
| Mixed/no-dedup settled | `<=1.08 * D_ideal` | `>1.08 * D_ideal` |
| Many-small settled | `<=1.15 * D_ideal` | `>1.15 * D_ideal` |
| Avoidable duplicate payload | `<=1%` | `>1%` |
| Pack dead/slack allocation | `<=2%` | `>2%` |
| Publication transaction staging | captured allocation is transferred once; additional **payload** staging `<=5% * C_capture` and is zero for metadata-only capture; fixed transaction metadata is charged to `M` under the bound below | any hidden second upper/native copy, excess payload, or missed settle deadline |
| Cold hydrate-and-adopt | one native `C_target` while the cold source remains authoritative; additional **payload** staging `<=5% * C_target`; fixed transaction metadata is charged to `M` | a second native target, excess payload, or missed locator-switch/settle deadline |
| Persistent unexplained bytes | `0` | any nonzero persistent value |

The percentage limits apply to allocated payload, not unavoidable fixed
metadata. Each transaction may additionally own at most a `256 KiB` journal
and its share of the already-declared `4 MiB` managed publication budget;
those bytes are explicit `M`. A metadata-only edit therefore has zero payload
staging rather than an impossible zero-metadata allowance.

Maintenance settlement has an enforceable deadline. Before candidate runs, controls freeze
`R_bytes` and `R_entries` as conservative lower 95% confidence bounds for
durable evacuation bytes/s and entries/s on that placement. For `B` remaining
allocated bytes and `E` reverse-manifest entries:

```text
D_calc = 2 s + 1.25 * max(B / R_bytes, E / R_entries)
D_settle = min(D_calc, 60 s)
```

If `D_calc > 60 s`, admission must split or pre-evacuate the work, or reject
it; it cannot silently extend the deadline. If no lease blocks retirement,
eligibility begins at `CurrentPublished`; otherwise it begins at the durably
observed release of the last blocking lease. The journal persists that
eligibility time and derived absolute deadline. Recovery resumes immediately,
and an ambiguous/backward clock after eligibility is treated as expired.
Release campaigns quiesce old leases, so their deadline begins at
publication. Excess duplication or unfinished retirement at expiry fails the
operation/campaign while new allocation remains backpressured. A
pre-eligibility live lease stays within the active-attempt and retirement
byte/count quotas and is never reported as settled.

Logical projection depth does not exist. Qualified OCI candidate
`D_proj` counts incremental LayerStack delta/carrier lowers above one
mandatory base, so it is operationally `<=4` (`<=5` total lowers) and rejected
above `8` (`>9` total lowers). The separate probed OverlayFS
ceiling is 500 total lowers, normally 499 incremental carriers plus one base;
the candidate does not spend that safety margin in routine activation.

The table contains targets, not measurements:

The Firecracker rows are Phase 3 analytical budgets and falsifiers for the
adapter handoff, not measured Stage 04.6 release gates. Stage 04.6 measures
the corresponding OCI rows.

| Workload | Settled allocated bytes | Peak temporary bytes | Metadata growth | Payload amplification | Required interpretation |
| --- | --- | --- | --- | --- | --- |
| Mixed/no-dedup steady root | `C_current + H_unique + M`, `<=1.08 D_ideal` | one bounded journal/pack tail plus active uppers | within existing per-chunk, per-segment, and per-change budgets | `<=1%` avoidable duplicate | a payload owner exposed directly as a lower counts once |
| Many-small steady root | `<=1.15 D_ideal` | bounded streamed path spool and metadata-page run; no second tree | target `<=256 B + path bytes` per change plus filesystem allocation; measure inode/dir/xattr blocks | no complete payload duplicate | 100k and 1M cells may not use an in-memory path set |
| 1,000 clean inactive forks | no per-node/private native projection or payload caused by the fork; shared payload-store allocation and unique logical-history payload count once | no projection construction | target `<=8 KiB` allocated/ref, therefore `<=8 MiB` total, plus shared and uniquely changed Merkle pages | no fork-induced complete copy | any native tree/image per inactive fork fails |
| 16 clean active siblings | one shared lower/projection plus empty private upper/work metadata | `sum(U_active)` as mutations occur | target `<=256 KiB` service metadata/attempt plus measured filesystem directory blocks | only bytes actually allocated by uppers | active-attempt and disk quotas apply; inactive roots remain refs |
| Stock Firecracker image | no retained second complete image unless it is an independently verified payload locator and total allocation still passes the applicable settled gate | every allocated image block is charged to `P_staging`, then `L_hot` while leased; the source locator remains counted | image filesystem metadata measured, never inferred from logical length | normally one temporary complete projection; no 100x/500x miss claim | evict at lease drain; persistent use requires the optional qualified block backend or proof that the image is not avoidable duplicate payload |
| 16 stock Firecracker siblings | one shared read-only base image plus 16 empty/private guest upper drives; never 16 base images | one-image build peak plus allocated blocks of all private drives in `sum(U_active)`; logical sparse drive length is ignored | guest filesystem/union metadata and journal allocation per attempt measured | base payload once; only allocated private changes repeat | no-sparse or no-qualified-guest-union placement rejects; guest/VMM memory is accounted separately |
| Sixteen one-byte/1 GiB edits, qualified OverlayFS path | after winner selection and evacuation: `C_current + H_unique + M` and `<=1.08 D_ideal` | worst case about 16 GiB of active full-file uppers plus shared base; must be admitted or rejected explicitly | bounded per-attempt change journals | temporary full-file copy-up is unavoidable; retained full copies are not | this peak is a disclosed directory-path limitation, never a range-CoW result |
| One-byte/1 GiB edit, range-CoW accelerator | `C_current + localized unique chunks + M` | target at most dirty allocation units plus bounded rechunk halo and journal | `O(log F)` extent pages; at 64 KiB, a flat 1 GiB hash list would already be about 512 KiB, so persistent hierarchy is mandatory | target `<=128 KiB` new payload for a one-byte overwrite, subject to measured chunk resync | a retained 1 GiB delta falsifies the accelerator |
| One-byte/1 GiB edit, qualified directory root after settlement | `C_current + old-only CDC chunks + M`, `<=1.08 D_ideal` | old complete lower plus new complete upper until locator evacuation and leases finish | bounded locator replacement run | new current full file counts as `C_current`; old full file must not remain merely for history | settlement has the deterministic deadline above; missing it is not hidden “background work” |
| Offline pip/npm install | current root payload plus unique prior package chunks and metadata | one active upper, pack tail, and bounded metadata spool | entry-linear, within `1.15 D_ideal` for many-small | no CAS-plus-carrier duplicate after settle | install, upgrade, uninstall, and cancellation each get a space curve |
| Public `squash_layerstacks` logical ancestry prune | unchanged payload allocation | one external history/ref receipt at most | `O(1)` with identical root pair | zero | an attribution change is publication; moving payload is separate physical flattening |
| Physical flatten/rebase maintenance | unchanged payload when an exact existing lower/locator recipe can be retained; otherwise every copied byte is reported | old leased projection plus one admitted new namespace build and any explicitly required evacuation | `O(E)` native metadata | zero only for exact locator/lower reuse; copy-required normalization is separately timed and gated | no hidden cross-generation hardlinks; old generation remains until leases drain; failure leaves a journal-owned orphan |

`P_staging` must return to zero after every successful, failed, or cancelled
operation. Peak accounting includes every byte of a replacement locator while
the old source remains retained, not merely the current pack tail. A settled
result is not recorded until locator evacuation and lease retirement have
completed, `P_staging` is zero, and the avoidable-duplicate gate passes.
Bytes explicitly owned in `H_cold` make a `Retiring` state accountable, but
do not turn it into a settled release result.

## Memory and resource bounds

The architecture does not buy latency with a RAM disk, whole-repository page
cache, or an unbounded index. Preserve the prep document's stricter limits and
add active-attempt inventory:

| Resource | Hard bound for the Stage 04.6 qualification profile |
| --- | ---: |
| Active execution attempts | 16 |
| Pending attempt admissions | 16 descriptors |
| Concurrent publication/projection builders | 4 |
| Global storage data workers | 4 |
| Maintenance coordinators | 1; it consumes one of the same four global data-worker slots and permits, never a fifth worker |
| CDC rolling window/ring | 32 KiB per active chunker |
| In-flight publication chunk | one borrowed ring-backed chunk, `<=32 KiB` per data worker |
| Pack-read buffer | one `<=256 KiB` buffer per data worker |
| Hydration-output buffer | one `<=256 KiB` buffer per data worker |
| Downstream queued payload | 0 bytes; descriptors only |
| Descriptor queue | 16 descriptors and `<=64 KiB` encoded metadata |
| Per-publication managed memory | `<=4 MiB`, excluding shared index |
| Application-managed index window/working set | 16 MiB |
| Global storage-owned byte semaphore | 64 MiB |
| Open pack tails | 4; each `<=64 MiB` payload and `<=80 MiB` allocation |
| Disk-backed sort/change spools | `<=512 MiB` and `<=1,200,000` records per operation; `<=2 GiB` / `4,800,000` records global |
| Pending retirements/evacuations | 20, shared with the admitted-operation journal cap |
| Retiring locator bytes | `<=8 GiB` allocated globally; excess admission backpressures |
| Unleased projection generations | 64, `<=16 GiB` allocated, and `<=4,000,000` inodes globally |
| Merge fan-in | 8 runs with `<=64 KiB` buffer each |
| Manifest/journal encoder | `<=256 KiB` |
| Storage-owned FDs | 512 global, `<=32` per operation |
| Storage-owned mounts | 64 global |
| Active locator/projection leases | 4,096 global; excess backpressures |
| Per-attempt upper allocation | 4 GiB and 1,200,000 inodes in the qualification profile |
| Global active-upper allocation | 32 GiB and 4,000,000 inodes |
| Backend workload-memory reservation | `<=512 MiB` per active attempt and `<=8 GiB` global in the qualification profile; OCI cgroup memory, Firecracker guest/VMM memory, and WASI linear/runtime memory are charged to the same admission ledger |
| Native lower depth | `D_proj` counts incremental LayerStack delta/carrier lowers above one mandatory base; target `D_proj <=4` (`<=5` total), reject `D_proj >8` (`>9` total); capability receipt records the platform ceiling (upstream OverlayFS: 500 total, normally 499 incremental plus one base) |
| Aggregate storage-service process RSS | `<=384 MiB` across all storage-service processes and helpers, and `<=128 MiB` above aggregate idle |
| Aggregate storage-service memory domain | `<=512 MiB` hard: all service anonymous/RSS, resident mmap, attributable page cache, dentry/inode/slab, and helper memory in one cgroup or platform-equivalent domain |

Stage 04.6 enforces and measures the backend workload ledger for OCI. The
Firecracker and WASI reservations are frozen contract defaults and become
operational qualification gates in Phase 3.

Every byte/inode admission is the minimum of its row cap, current free-space
reserve, the operation-specific `P_staging` allowance, retirement/compaction
debt allowance, and the global settled/peak space gate. The 16 GiB projection,
8 GiB retirement, and 2 GiB spool numbers are ceilings, never permission to
violate `1.08 D_ideal`, `1.15 D_ideal`, or the declared hydration peak. Space
is reserved before mutation; failure returns deterministic backpressure.

The byte/inode quotas are deployment-configurable downward but not silently
unbounded upward. The backend workload-memory reservation is distinct from the
storage-service RSS bound; 16 attempts fit only if all 16 reservations fit the
8 GiB ledger. A 16-way large-file or memory test either fits the declared
global quota or receives deterministic bounded `ResourceExhausted`
backpressure; it must not overcommit and hope for disk or RAM.

Indexes and persistent Merkle/extent pages may be memory-mapped, but the
application-managed index window/working set is limited to 16 MiB using
bounded mapped windows plus unmap/`madvise`, or `pread`. Mmap bookkeeping
cannot guarantee total kernel residency. Repository size and inactive-root
count may grow persistent file length without growing the application window.
External sort/spill paths use the same global permits.

The aggregate storage-service domain backpressures before its 512 MiB hard
limit and returns deterministic `ResourceExhausted`; any OOM kill or limit
breach fails qualification. On Linux, one cgroup accounts all service
processes plus resident mmap/file cache and kernel memory; another platform
must provide an equivalent aggregate meter/limit or is unqualified. The
384 MiB RSS limit is aggregate, not per process.

For the Phase 3 accounting contract, Firecracker guest RAM is normally mapped
in VMM address space: the same
physical pages are charged exactly once to the 8 GiB backend ledger, never
once as guest memory and again as VMM RSS. Per-attempt reservation includes
guest RAM, non-guest VMM overhead, and associated cache. OCI cgroup memory and
WASI linear/runtime/cache memory use the same exactly-once rule. These
backend workload domains are separate from the 512 MiB storage-service
domain. No performance claim may depend on an unreported hot page cache.

There is at most one pending journal record per admitted operation, hence at
most 20 with this profile's 16 admissions and four builders. Each record is
`<=256 KiB`; restart scans at most 20 records / 5 MiB and must finish within
one second on the qualification host or reject service readiness. Terminal
records fold immediately into a durable generation/checkpoint snapshot.
Optional diagnostics use a separate oldest-first ring capped at both 20
records and 5 MiB; ten minutes is maximum retention, not a guarantee, and
age/count/bytes may evict sooner. Pending plus diagnostic journal storage is
therefore at most 40 records / 10 MiB. Restart reads only the pending 20-record
half and immutable generation selectors; it does not enumerate every object
or native directory. Rust
ownership is acyclic: managers own tasks and leases, callbacks use weak
references, and cancellation joins tasks before dropping inventory. RAII
guards release byte permits, FDs, mappings, leases, and staging ownership.

## Privilege and portability audit

The logical checkpoint, payload, publication, and rollback contracts are
Docker-image, host-OS, and host-filesystem agnostic and independent of reflink
or a particular kernel minor version. Physical writable execution is
capability-qualified, not universally host-filesystem agnostic. OCI
activation uses an adapter-owned namespace/read readiness probe over a known
fixture path; it never requires `sh`, `true`, or another binary to exist in
the image. The OCI adapter executes inside a qualified Linux environment—on
macOS or Windows this is normally the Docker-managed Linux VM—and that
environment must support a qualified union facility and the declared
metadata profile. Under `CAP_SYS_ADMIN` alone, arbitrary-filesystem writable
isolation with shared lowers and no private full copy is an unsatisfied
requirement; absence of a qualified facility is a placement rejection.

`CAP_SYS_ADMIN` is a ceiling, not a magic substitute for devices or other
capabilities:

| Operation or semantic | Is `CAP_SYS_ADMIN` alone sufficient? | Required behavior |
| --- | --- | --- |
| OverlayFS mount in an allowed mount namespace | generally, if the kernel, LSM, user namespace, and backing FS allow it | probe mount options, xattrs, `d_type`, and semantic oracle |
| No-copy writable OCI siblings when the backing FS rejects OverlayFS | no; `CAP_SYS_ADMIN` cannot manufacture union/CoW semantics | reject that OCI placement or use a separately qualified optional union/range adapter; a complete lower copy per sibling is not an allowed fallback |
| Overlay whiteout without `mknod` | only when a semantic probe proves a supported regular-file/xattr encoding; otherwise no, because character-device whiteouts need `CAP_MKNOD` | reject writable placement when no qualified union encoding exists; never guess |
| Arbitrary uid/gid restoration | no; normally needs `CAP_CHOWN`, or a proved idmapped mapping | capability receipt rejects an unsupported placement |
| chmod/timestamp/POSIX ACL changes on files not owned by the service identity | no; may require `CAP_FOWNER` | use a proved idmapped/service-owned profile or reject |
| Preserve setuid/setgid through writes or ownership changes | no; may require `CAP_FSETID` | reject identity metadata the profile cannot reproduce |
| OCI `config.User` UID transition | no; an adapter doing `setuid` needs `CAP_SETUID` in the relevant namespace | a separately qualified OCI runtime/supervisor establishes credentials, or a proved user-namespace mapping is used; otherwise reject placement |
| OCI primary/supplementary GID transition | no; `setgid`/`setgroups` needs `CAP_SETGID` in the relevant namespace | use the same qualified delegation/mapping rule; otherwise reject placement |
| Terminate processes owned by another uid | no; may require `CAP_KILL` | supervisor/cgroup must own termination or placement is rejected |
| `chroot`-based isolation | no; requires `CAP_SYS_CHROOT` | do not use chroot as the base activation path |
| Device-node creation | no; needs `CAP_MKNOD` and device-cgroup policy | reproduce on a separately capable placement or reject that placement |
| File capability xattrs | no; generally needs `CAP_SETFCAP` and policy | reproduce on a separately capable placement or reject that placement |
| Immutable inode flag | no; needs `CAP_LINUX_IMMUTABLE` | never depend on `chattr +i` |
| Some security/LSM xattrs | no; policy and possibly `CAP_MAC_ADMIN` apply | preserve only in a qualified profile |
| Reflink | capability is irrelevant; filesystem/driver support is required | optional probe plus semantic/extent tests |
| FUSE | no; `/dev/fuse`, device policy, userspace server, and mount permission are required | optional only |
| Loop, NBD, device mapper | no; device nodes, device-cgroup access, drivers, and often helpers are required | optional only |
| File-backed EROFS | mount authority plus a sufficiently new/supporting kernel | optional; fall back on probe failure |
| Firecracker execution | no; Linux KVM, hardware virtualization, and read/write `/dev/kvm` are required | Phase 3 qualified backend, not universal fallback |
| Firecracker regular image attachment | ordinary file permission is enough; no loop device is inherent | open the regular file directly and account every allocated block |
| Firecracker jailer/credential/cgroup setup | not in general; chroot, UID/GID transitions, namespaces, and cgroups have distinct authority | a qualified executor supervisor prepares jail, credentials, delegated cgroup, namespaces, and FDs before dropping privilege; otherwise reject |
| Firecracker tap networking | no; normally needs `/dev/net/tun` and `CAP_NET_ADMIN`, unless a prepared FD is delegated | optional networked profile only |
| Firecracker no-network/vsock profile | no tap or `CAP_NET_ADMIN`; vsock still requires its configured Unix-socket/guest support and policy | the Phase 3 Firecracker base profile uses no network and an adapter-owned vsock/control path, or pre-created networking |
| Guest change journal | not a host capability; it requires a version-matched controlled guest component and durable cursor | an absent/incomplete cursor triggers the timed full private-upper semantic scan or publication rejection |

There is no way to preserve arbitrary device nodes, arbitrary ownership,
file capabilities, every LSM xattr, and Firecracker execution with
`CAP_SYS_ADMIN` alone. Stage 04.6 nevertheless preserves the existing
canonical v3 checkpoint without weakening its semantics. A worker capability
receipt says whether that placement can reproduce a root; missing authority
or filesystem support rejects placement, not publication under a different
identity. Process ownership, signal/termination, jailer, networking, and
runtime devices are execution-placement capabilities. They never enter
checkpoint identity and never cause republishing under a weaker root. OCI is
production-qualified in Stage 04.6; Firecracker and WASI independently
qualify the same contract in Phase 3.

`CAP_SYS_ADMIN` is an executor/storage-service ceiling only. It is never
inherited by an OCI workload, Firecracker guest workload, or WASI module.

### Existing canonical v3 semantic contract

Stage 04.6 keeps the existing canonical records and
`RootRecordV3.required_capability_bits`; it adds no backend or reduced-profile
field to `RootId`. The contract and inherited exact-round-trip gate are:

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
namespaces where the environment admits them, sparse extents, hardlinks
including observable `st_nlink`, whiteouts, opaque directories, FIFO, and
device fixtures. A fixture whose host authority cannot create an entry is an
explicit capability-placement rejection, not a weakened successful
materialization. WASI may retain and enforce metadata through the EphemeralOS
virtual-file provider when its standard host-call surface has no corresponding
field.

The Firecracker and WASI mappings are Phase 3 conformance obligations and
design analysis, not live Stage 04.6 release tests. Phase 1 supplies canonical
root/attribution fixtures and backend-independent adapter contract tests; live
adapter construction, activation, semantic-oracle, and performance campaigns
are deferred to Phase 3.

KVM is not a dependency of the logical checkpoint, payload store, publisher,
rollback, OCI adapter, or WASI adapter. Linux KVM and read/write `/dev/kvm`
are mandatory only when the Firecracker adapter is selected for execution.
Likewise, no POSIX algorithm can provide transparent writable, isolated,
no-copy OCI siblings on every possible host filesystem without some union,
range-CoW, or mediated-filesystem facility. The architecture is independent
of a *particular* filesystem, but the OCI adapter must find one qualified
union capability. On a non-Linux host that capability normally lives inside
the OCI Linux VM. Absence is an explicit placement rejection, not permission
to retain one complete lower per agent.

### Zero-new-external-dependency release gate

Stage 04.6 inherits
[prep §11.1](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md#111-zero-new-external-dependency-contract)
as an exact release gate. Milestone 0 freezes, for every supported target and
feature invocation, lockfile package identities/versions, enabled external
features, and the product-wide multiset of direct external manifest edges.
The final candidate must have zero unexplained delta in all four. A moved
direct edge is allowed only for a documented responsibility move with the old
edge removed and no count, package, version, or feature change.

No new package, CDC/hash/database/allocator/profiler/benchmark/async runtime,
Python/npm dependency, vendored or FFI library, system command/package,
daemon, sidecar, target-image helper, or build/runtime download is permitted.
A new workspace crate may use only the Rust standard library and acyclic
internal workspace edges. Qualification stores `cargo metadata --locked`
feature-resolved manifests plus command/helper/download inventories for
baseline and candidate; any unexplained delta is a release falsifier.

### Mandatory host/image release evidence

Stage 04.6 inherits the frozen matrix in
[prep §11.2](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md#112-docker-host-and-linux-image-portability).
Every row records exact host OS/build and amd64/arm64 architecture, exact
Docker Engine/Desktop build, native or Docker-managed Linux environment,
guest kernel/storage driver/backing filesystem, OCI index and resolved
platform-manifest digests, image class, read-only/non-root configuration,
capability receipt, oracle/performance/resource evidence, and artifact
location. Versions and digests never use wildcards or `latest`.

Required coverage includes supported Linux, macOS/Docker Desktop, and
Windows/Docker Desktop release triples; pinned Ubuntu/Debian glibc, Alpine
musl, minimal/distroless, and scratch/shell-less images; read-only bases;
non-root `config.User` plus supplementary groups; and native versus supported
emulated architecture paths. On macOS and Windows, probes measure the
Docker-managed Linux VM storage domain used by the product, not APFS/NTFS
bind-mount behavior. Readiness uses the adapter-owned workspace/file API and
executes no target-image helper.

Rows are labeled `qualified`, `contract-tested`, `designed-compatible`, or
`unverified`, and `required-release` or `informational`. A missing,
`unverified`, `designed-compatible`, or merely contract-tested
required-release row is a production no-go.

## Benchmark and falsification plan

### Preserve and extend, never rewrite

Keep `baseline.json`, its recorded values, and preserved experiment artifacts
unchanged. Add a new append-only Stage 04.6 result directory and benchmark-lab
preset. Retain the historical inner spans and add outer clocks.

Controls, interleaved on identical fixture copies:

- `I0`: pinned main/raw-overlay control;
- `I1`: direct native `cp -a`-equivalent control;
- `I2`: current CAS complete-carrier implementation; and
- `I3`: recommended architecture, with projection/accelerator mode in the
  sample key.

`I0` is a reproducible control, not a label for an already-warm workspace.
Freeze its exact main commit and dirty-state evidence, OCI index/platform
digest, Docker/kernel/storage-driver/backing-filesystem tuple, OverlayFS
options, and capability receipt. The once-only sandbox/base-workspace setup
may occur outside a post-setup sample, but every sample receives a fresh
private upper/work pair and no artifact or receipt from `I2`/`I3`. Execute the
same product mutation and readiness probe through pinned main. For publication
the outer timer begins before change enumeration/freeze and ends only when the
root is durable and the requested public close/readiness boundary passes; for
activation it begins before root/projection selection and ends after the
adapter probe. Record the raw-OverlayFS mutation/copy-up, pinned-main
publication, sync, response, and settle subspans instead of moving any of them
outside the clock. Product-required network work remains inside the outer
timer and is additionally reported as a subspan.

Use a predeclared balanced four-treatment Williams crossover in complete
blocks, not an ambiguous two-treatment `ABBA`: `I0 I1 I3 I2`,
`I1 I2 I0 I3`, `I2 I3 I1 I0`, and `I3 I0 I2 I1`. Allocate a fresh matched
fixture copy per run. If a platform cannot execute complete four-way blocks,
run and report separately predeclared pairwise `I3`-versus-control ABBA/BAAB
blocks; never pool the two designs silently.

At least 20 matched samples support p50/p95. At least 100 support p99 or the
sub-millisecond warm claims. Fault/stress cells run at least three times but
make no percentile claim.

### Required operation boundaries

| Clock | Starts | Ends |
| --- | --- | --- |
| First ingestion | before source open/walk | root and ref durable/resolvable after all required validation |
| Direct native-copy control (`I1`) | before source open/walk | complete destination namespace, semantic oracle, durability sync, and the same adapter-owned readiness probe all pass |
| Prepared-change publication | at the historical `LayerChange` boundary | historical matched completion |
| Non-closing logical checkpoint/add-layer | before admission and tracker enumeration | root/ref durable, recorder epoch advanced in the same upper, and a next-command probe accepted; no close, freeze, rotation, lower addition, or remount |
| Closing public session publication | before admission and tracker enumeration/freeze | root durable, public response complete, session closed, and its upper either transferred to inventoried immutable ownership or deleted; successor-workspace readiness is a separate clock only when the exported product contract promises one |
| Combined mutation + non-closing logical commit | before mutation | durable root plus same-upper next-command readiness |
| Combined mutation + closing session publication | before mutation | durable root, public response, session close, and upper ownership transfer/deletion; any contractually promised successor is reported separately |
| Raw-upper normalization | before freeze and first upper-entry enumeration | durable normalized delta, semantic receipt, and all overlay-private state either represented or rejected |
| Exact frozen-recipe handoff | before recipe/projection lookup | compatible receipt and generation selected, dependencies pinned, and adapter-owned namespace/read probe passes |
| Projection miss/build | before root resolution and build decision | immutable projection receipt durable; activation to usable/probed namespace is a separate clock |
| Cold activation | before root resolution/adapter activation | usable namespace plus an adapter-owned, image-independent namespace/read probe over a known fixture path |
| Exact-key reuse | immediately before key lookup | immutable generation selected, dependencies pinned, and adapter-owned namespace/read probe passes |
| Winner reactivation | before selected-root resolution and placement | selected root usable and probed; warm-local, cold-local, and remote/cold placement reported separately |
| Public `squash_layerstacks` logical ancestry prune | before ProductAccess/CLI invocation | identical root pair plus new ancestry selection durably visible and public response complete |
| Physical flatten | before freeze/build | new projection durable, live sessions switched/probed, old generation reclaimable |
| Rollback | before selected-root CAS | target usable and probed; hot and cold placement separate |
| Teardown | before public request | response complete and owned mounts, FDs, cgroups, staging, and payload reclaimed or bounded settle reported; transferred payload owners remain inventoried rather than falsely counted as deleted |

For every lazy, image, or block projection, cold activation emits:

1. workspace-ready;
2. first open to first byte;
3. first selected-file complete read;
4. first metadata-only repository walk;
5. first byte-reading full repository scan;
6. deterministic random-read cold and warm distributions;
7. first write plus fsync/copy-up and allocation delta; and
8. steady warm activation.

Every cold deferred-cost metric uses a fresh identical activation and a
declared worker, cache, and remote state. A full scan must not precede a
supposedly cold random read, first-file read, or first write. If cache reset
cannot be proved, label the cell `cache state unknown`, not cold. Random reads
use a versioned seed, declared read count, offsets/alignment, file-size strata,
touched-byte count, checksum, p50/p95 (p99 only for `n>=100`), and throughput.
Full scans compute and verify a checksum inside the timer.

### Corpus and mutation matrix

- preserved `B0`: 870.08 MiB, 3,602 files;
- mixed `B1`: recorded 1 GiB multi-language repository;
- `B2a`: at least 20,000 small files;
- `B2b`: at least 100,000 small files;
- stress-only `B2c`: 1,000,000 entries;
- `B3a`: 100 MiB large file;
- `B3b`: 1 GiB large file;
- `B3c`: a deterministic 1 GiB near-min-cut SeqCDC stream plus a synthetic
  131,072-range reverse-owner-manifest boundary case;
- deterministic offline pip and npm install, upgrade, and uninstall fixtures,
  including normal, 100k-entry, and stress-only 1M-entry shapes;
- 64 and 1,000 inactive nodes;
- 64- and 1,000-operation non-closing logical-layer campaigns, each clocking
  submission before admission/queueing through durable ref and same-upper
  next-command readiness; these must keep `D_proj` unchanged, include forced
  synchronous work and later maintenance-induced backpressure, pass
  `<=1.070 s p95` and `<=1.070 s max`, and never reject or defer readiness;
- separate 64- and 1,000-operation tiny-edit
  publish-then-`freeze_for_branch`/fork/activate campaigns that traverse every
  depth-compaction trigger, keep publication and activation scores separate,
  pass the `1.070 s`/`99.9 ms` constituent gates and `1.170 s` outer maximum,
  report aggregate/max compaction, and reach zero maintenance debt under
  `D_settle`;
- 32 sibling tiny-edit branches;
- 1, 4, and 16 concurrent active attempts;
- candidate `D_proj` 0, 1, 4, and 8; legacy/control total lower count 32, 64,
  128, 499, and 500; capability rejection at 501 total lowers;
- public `squash_layerstacks` logical ancestry prune and separately timed
  internal physical flatten/legacy-control behavior; and
- hot-locality and cold-worker winner reactivation.

Large files receive 1-byte, 4 KiB, and 64 KiB overwrites at deterministic
beginning, middle, and end offsets. Also cover append, truncate, replace-by-
rename, and sparse-range mutation. A one-byte write that leaves a full-file
settled delta disproves range efficiency even when the qualified directory fallback is
expected to have a full-file *temporary* upper.

The semantic matrix includes create, overwrite, append, truncate, unlink,
rename, cross-directory rename, type replacement, recursive removal, whiteout,
opaque directory, chmod, supported ownership/timestamps/xattrs, relative and
absolute symlinks, hardlinks, and sparse files.

### Real product command surface

Discover it on every campaign rather than maintaining an invented list:

```text
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo run --quiet -p sandbox-cli \
  --features manager,runtime,observability \
  --bin sandbox-catalog-export
```

The current public surface is:

- manager: `create_sandbox`, `list_docker_images`,
  `list_workspace_directories`, `destroy_sandbox`, `list_sandboxes`,
  `inspect_sandbox`, `squash_layerstacks`, and `export_changes`;
- runtime: `exec_command`, `write_command_stdin`, `read_command_lines`,
  `file_read`, `file_write`, `file_edit`, `file_blame`,
  `create_workspace_session`, `publish_workspace_session`, and
  `destroy_workspace_session`;
- observability: `snapshot`, `trace`, `events`, `resources`, `daemon`,
  `topology`, `cgroup`, and `layerstack`.

`fork`, committed `checkpoint`, historical-root `materialize/reactivate`,
committed `rollback/reset`, and checkout are not public operations today.
Until the catalog exposes them, benchmark their real component APIs and label
the public cell **blocked**, not passed. Current mappings are:

| Requested lifecycle concept | Current supported operation |
| --- | --- |
| Create sandbox | `create_sandbox`, including count 1/4/16/32 |
| Create active workspace | `create_workspace_session` |
| Execute | explicit-session and implicit `exec_command` |
| Checkpoint/publish | `publish_workspace_session` |
| Discard active work | `destroy_workspace_session` |
| Activate current root | `create_workspace_session`; historical root remains component-only |
| Squash today | `squash_layerstacks`, currently physical flatten/live remount; retained as the legacy control |
| Squash after the Stage 04.6 contract switch | public `squash_layerstacks` logical ancestry prune preserving the exact root pair |
| Fork inactive root | component-only; `create_sandbox --count` is not a substitute |
| Roll back committed root | component-only |
| Teardown | workspace-session and sandbox destroy operations |

Stage 04.6 completion requires the generated ProductAccess catalog to expose
the changed logical `squash_layerstacks` contract and a committed-root
rollback operation. Until then, the rollback public cell is blocked. This
review does not invent a CLI spelling.

Outer CLI wall time starts before process spawn/serialization and ends after
the terminal response and readiness condition. Product IPC stays in the
timer. Inner service spans explain the result but do not replace it.
In particular, `TimedGatewayResponse.latency_ns` is diagnostic only: its
transport clock starts after connection setup, while session helpers perform
inspect/auth/connect before the timed daemon request. The score clock wraps
the caller before CLI or `ProductAccess` invocation.

The next benchmark phase covers all 8 manager and 10 runtime operations, all
three export formats, explicit/implicit command execution, stdin/line
lifecycle, and read/write/edit/blame. The eight observability operations are
non-scored integrity/overhead cells; `snapshot` and `resources` exercise both
system and sandbox routes. The campaign fails coverage validation if catalog
export contains an unclassified public operation-and-route tuple.

Operation-specific outer boundaries are:

| Operation | Readiness boundary and required split |
| --- | --- |
| `create_sandbox` | before CLI spawn through every returned record `Ready` plus direct daemon/workspace probe; split shared-base built/reused and image present/pull, and report first/last ready for count |
| list/inspect operations | complete schema-validated response with expected membership/cardinality |
| `destroy_sandbox` | record, daemon/container, mounts, and owned storage absent; report response and settle separately |
| `squash_layerstacks` after contract switch | identical root pair, new ancestry selection durably visible, public response complete; physical flatten is excluded |
| internal physical flatten / legacy squash control | new projection durable, required sessions switched/probed, old generation reclaimable; all copied allocation and settle latency separate |
| non-closing logical checkpoint/add-layer component, and public route only after catalog exposure | root/ref durable, recorder epoch advanced in the same upper, and next-command probe accepted; no session close, upper rotation, lower addition, or remount |
| `export_changes` | complete verified destination; separate directory, tar, and `tar-zst` rows |
| `create_workspace_session` | response plus probe in that exact explicit session; split shared and isolated network profiles |
| explicit `exec_command` | terminal command result/output; an initial still-running response cannot stop the timer |
| implicit `exec_command` | terminal command plus automatic publication durable, automatic session destruction, and session-upper ownership transfer/deletion; label as combined closing lifecycle. Time successor-workspace readiness separately only if the exported contract promises it; do not assume a new private upper |
| stdin/read-lines | accepted write/yield and validated stable-offset read, including the complete running-command interaction |
| `file_read` | verified returned bytes; separate snapshot and explicit-session variants |
| `file_write` / `file_edit` with session ID | mutation visible in that live session |
| `file_write` / `file_edit` without session ID | automatically published layer durable and read back; a distinct score row |
| `file_blame` | complete correct published-file tiling |
| `publish_workspace_session` | root durable, session closed, and session-upper ownership transferred when adopted or deleted when not retained; report response and physical settle separately. Add a successor-workspace readiness row only if catalog/schema semantics require one |
| `destroy_workspace_session` | session absent and non-adopted upper deleted; adopted payload remains under inventoried `PayloadStore` ownership; active-command rejection is an error-path cell |
| every observability operation and route | complete schema-validated, bounded response; record cardinality and response bytes, and verify no lifecycle, checkpoint, projection, or payload-store mutation |

### Per-sample record

Record:

- implementation, source commit/diff, build, image, host, filesystem, mount
  options, projection key, and accelerator probes;
- baseline/candidate lockfile package, feature, direct-edge, helper/command,
  and runtime-download inventories for the zero-dependency comparison;
- corpus, mutation, root, attribution root, parent, depth, placement, cache
  state, concurrency, and active/inactive counts;
- outer wall and every named phase span;
- bytes discovered, read, hashed, reused, written, reconstructed, and deferred;
- syscalls/faults where observable;
- logical and unique allocated before/peak/settled bytes for every `T(t)` term;
- CAS/pack unique bytes, native delta, staging, metadata, and unexplained bytes;
- current/peak RSS, index/mmap residency, FDs, mounts, workers, queues, permits,
  inodes, and leases; and
- semantic-oracle, crash-recovery, and cleanup verdicts.

### Hard falsifiers

The core recommendation is disproved, not merely “in need of tuning,” by the
qualified-directory-path and invariant failures below. A failure explicitly marked as an
optional-accelerator failure disables that accelerator through its kill
switch; it does not disprove the hybrid when the qualified fallback still
qualifies.

1. a semantic mismatch, sibling leak, nondeterministic logical root, backend-
   dependent `RootId`, wrong rollback target, missing committed root after
   restart, visible uncommitted root, or storage ownership inflating
   workload-visible `st_nlink`;
2. small post-setup publication or the defined combined small
   mutation-to-durable-root cell above `1.070 s p95`;
3. any 100x/500x label whose candidate p95 exceeds the lesser of its
   historical ceiling and `matched_current_p95 / 100` or `/ 500`,
   respectively;
4. first ingestion p95 above `1.25x` its matched one-pass physical-floor
   control, or evidence of an avoidable second complete source-payload pass;
5. `I3` rejecting, truncating, or weakening the required 1 GiB canonical
   file challenge instead of ingesting, reconstructing, activating, editing
   deterministic beginning/middle/end offsets, publishing, rolling back, and
   reactivating it within the declared bounded streaming and resource limits;
6. public logical `squash_layerstacks` or hot cached-projection rollback above
   `20 ms p95` outer or `1 ms p95` service, or either logical operation
   scaling with total root payload/history depth;
7. stored-projection cold-ready p95 above 99.9 ms, or any 500x
   workspace-ready claim above 20 ms;
8. a “complete materialization” headline that omits deferred read, scan,
   random-read, or first-write cells;
9. warm lookup outside its non-inferiority margin;
10. for each predeclared first workload `W`, matched candidate
    activation-start-through-`W`-complete p95 above `1.25x` the pinned control
    under identical corpus, placement, and cache state, or warm random/full-
    read throughput below `0.8x` control; workspace-ready remains separate and
    an already-active control is forbidden. This disables an optional
    lazy/image accelerator when the qualified directory fallback passes;
11. settled mixed/no-dedup above `1.08 D_ideal`, many-small above
    `1.15 D_ideal`, duplicate payload above 1%, unexplained bytes nonzero, or
    any fork causing a per-node/private complete native projection or payload;
12. any operation missing its persisted `D_settle`, or `P_staging` failing to
    return to zero after success, failure, or cancellation;
13. either 64/1,000-operation non-closing logical-layer sequence changing
    `D_proj`, exceeding `1.070 s p95` or `1.070 s max`, rejecting admission,
    returning deferred readiness, or omitting admission/queue/backpressure or
    forced synchronous work; or either separate branch-projection sequence
    exceeding a `1.070 s` publication constituent, a `99.9 ms` locally stored
    activation constituent, a `1.170 s` outer maximum, or `D_proj>8`,
    rejecting/deferring readiness, hiding compaction tails or
    maintenance-induced later delay, or retaining debt past `D_settle`;
14. a 1-byte/1 GiB range-accelerated edit retaining approximately 1 GiB
    disables that accelerator; a qualified directory edit retaining both full
    versions past `D_settle` disproves the core space architecture;
15. any queue, worker, byte, RSS, FD, mount, inode, lease, depth, or active-
    attempt cap exceeded; unbounded growth at 1M entries; or cancellation that
    does not return inventory;
16. a required OCI correctness path that secretly needs reflink, `/dev/fuse`,
    `/dev/loop`, NBD, device mapper, DAX, a module, an undeclared privileged
    helper, a specific host filesystem, or a particular kernel minor version;
17. large I/O under the global ref writer lock, serialized disjoint
    publications, unsafe upper mutation after seal, irrecoverable forward/
    reverse-locator/ref disagreement, or teardown leaks;
18. benchmark work moved before the timer, required product network work
    excluded, RAM/page-cache speedup left unreported, nonidentical controls,
    or one-shot results reported as percentiles;
19. a “metadata-bound” checkpoint whose matching hash-and-durability receipt
    was incomplete, whose workload receipt-hit rate was omitted, or whose
    forced immediate-post-command miss omitted scan, dirty writeback, sync,
    or `syncfs` interference from the combined clock; or
20. any unexplained delta in the frozen external-package/version/feature,
    direct-edge, helper/command, target-image-helper, or build/runtime-download
    inventory.

## Where the claimed speedup comes from

The design does not depend on a faster hash or wishful storage throughput. It
deletes foreground work:

| Legacy work | Recommended steady-state work | Saved mechanism |
| --- | --- | --- |
| Read/hash the complete root | read only authoritative changed files/ranges; reuse completed receipt | bytes and hashes reused |
| About 55,700 loose chunk installs for the baseline corpus | append bounded pack runs, or adopt ranges only after `freeze_for_branch` transfers immutable ownership | object opens, links, unlinks, and per-object syncs avoided |
| Loose canonical metadata/Merkle record installs | immutable packed/page-object runs with grouped durability | per-record temp/write/fsync/link/unlink/parent-fsync avoided |
| Reconstruct every file for a complete carrier | select/mount an existing projection or exact frozen recipe bundle | output bytes and syscalls avoided |
| Deep-hash an exact-key carrier on reuse | validate immutable generation and receipt | payload reads avoided |
| Replay a chain for ancestry prune/rollback | update external history or an existing complete-root checkpoint ref | payload and namespace work avoided |
| Build one native tree per inactive branch | retain a checkpoint record and shared Merkle pages | payload and inode allocation avoided |
| Preserve packed bytes and a duplicate frozen native upper | at `freeze_for_branch`, transfer the no-longer-writable upper as a temporary locator, then evacuate once | one payload copy avoided at the branch boundary; never applies to a continuing mutable upper |

For a small post-setup edit with a ready receipt, the foreground path is a
bounded journal append, a few persistent-page writes, locator/generation
selection, one short ref CAS, and (when requested) an already-built projection
switch. That is the only path on which a 500x result is physically plausible.
For first ingestion, a million entries, or a receipt miss, the one-pass floor
remains visible.

## Phase 2 parallel-MCTS compatibility

The recommendation is a stronger fit for Phase 2 than a vector-centered hot
projection:

- an inactive MCTS node owns only its checkpoint/ref and unique logical
  history; a fork creates no per-node/private native repository projection or
  payload, while shared payload-store allocations are counted once;
- fork is a new ref to the same `{RootId, AttributionRootId}` and does not
  mount or copy;
- the scheduler admits at most 16 active attempts and accounts their private
  uppers, inodes, mounts, memory permits, and leases before activation;
- 32 sibling publications update disjoint paths concurrently; only their
  final branch-head CAS is serialized, and a losing CAS never invalidates its
  immutable root;
- winner selection is a ref operation; hot winner activation selects an
  existing projection, while cold placement builds or mounts a projection
  under a separate clock;
- public `squash_layerstacks` rewrites only external history selection while
  preserving the exact root pair; physical flatten/remount is separately
  timed, quota-controlled internal maintenance;
- rollback selects an older complete checkpoint and does not reconstruct
  logical state from descendants; and
- deletion of a subtree decrements reachability asynchronously under leases,
  with bounded GC work and no fork-induced per-node/private native payload.

The Phase 2 qualification run must hold 1,000 inactive nodes, fan out 32
siblings, execute 1/4/16 attempts, cancel half during publication, choose a
winner, apply public logical squash, reactivate it on warm and cold workers,
and reclaim the losers. The 64- and 1,000-operation non-closing logical-layer
campaigns must keep `D_proj` unchanged, include submission/admission through
same-upper next-command readiness, pass `<=1.070 s p95` and `<=1.070 s max`,
and never reject or defer. Separate
publish-then-`freeze_for_branch`/fork/activate campaigns must traverse every
compaction trigger, remain at `D_proj <=8`, keep publication and activation
scores separate, pass the `1.070 s`/`99.9 ms` constituent gates and
`1.170 s` outer maximum, and report p95/max and aggregate compaction work.
Both reach zero maintenance debt within `D_settle`; any later delay induced
by maintenance remains in the next submission's timer. Failure to return all
loser `U_active`, staging, mounts, leases, and memory inventory is a release
blocker.

## Phase 3 and backend compatibility

This section is the Stage 04.6 **design handoff**, not a Phase 1
implementation or release-test requirement. Stage 04.6 ships the OCI adapter,
the logical format, the adapter contract, and canonical fixtures. Phase 3
implements and qualifies Firecracker and WASI.

The adapter contract consumes the same immutable logical checkpoint and
produces a rebuildable backend projection namespace. Namespace/cache metadata
is disposable; any sole-locator adopted payload is separately owned and
pinned until evacuated:

| Backend | Projection | Fast change evidence | Correct backend fallback | Backend-only state excluded from identity |
| --- | --- | --- | --- | --- |
| OCI/Linux | shallow normalized directory delta, complete directory, or optional image/lazy mount | sealed upper as whole files; proved reflink/block recorder for ranges | reconstruct the logical directory, then activate only through a qualified union facility; otherwise reject placement | paths, inodes, xattrs used as overlay encoding, mount and carrier generations |
| Firecracker | stock: regular file-backed filesystem image; optional qualified block backend: hierarchical extent map; optional VM snapshot | backend-owned CoW disk-extent journal plus guest semantic journal | construct a regular filesystem image from the Merkle checkpoint | block/image IDs, guest inode numbers, block journal, memory bitmap and snapshot ID |
| WASM/WASI | direct namespace and extent provider | exact provider-mediated host-call range and metadata journal; no writable bypass | direct Merkle traversal/content read | WASI handles, host paths, cache IDs |
| Future adapter | adapter-owned projection selected by capability receipt | adapter evidence accepted only after semantic qualification | logical checkpoint reader | every physical locator or accelerator identifier |

Every root admitted by Stage 04.6 retains the existing canonical v3 semantics
and passes the OCI oracle on a capable qualified placement. Phase 3 requires
Firecracker and WASI to pass the same oracle and activate the same canonical
fixtures exactly; failure rejects that adapter implementation or worker
placement, not the already-published root's meaning. No adapter weakens,
rewrites, or republishes the root to fit its host. A projection
namespace/cache can be destroyed after any sole-locator payload extents are
evacuated without destroying a checkpoint.

Phase 3 must not force OCI's directory encoding into Firecracker, or VM block
layout into WASI. Conversely, changed disk extents from a backend-owned CoW
layer are evidence only after guest filesystem semantics are exported and
validated; raw dirty blocks alone cannot explain rename, unlink, hardlink, or
attribution. Firecracker's guest-memory dirty tracking is not disk-change
evidence.

## Phased implementation, gates, and rollback points

All feature flags below are proposed implementation gates, not existing CLI
names. Old readers and complete carriers remain available until the final
removal milestone. No milestone rewrites Git history or user data in place.

| Stage 04.6 milestone | Deliverable | Entry/exit evidence | Feature gate and rollback |
| --- | --- | --- | --- |
| 0. Repair measurement | append-only benchmark preset, exact raw-overlay/native-copy/current-CAS controls, outer clocks, allocation/RSS/sync telemetry, semantic/fault oracle, frozen OCI host/image matrix, frozen dependency manifests and helper/download inventories | historical JSON unchanged; all catalogued commands classified; one-pass floors measured; every required OCI row pinned; zero-dependency baseline reproducible | no product behavior change |
| 1. Remove loose-object storm | bounded append-pack payload locators, atomic forward/reverse manifests, immutable packed/page runs for canonical metadata/Merkle records, grouped durability, leases, WAL, and recovery | byte-for-byte roots remain identical; no per-record durability/link storm at 100k/1M entries; bounded RSS/spool; hydrate-and-adopt exposes one storage namespace with exact `st_nlink`; first ingestion approaches `<=1.25x` one-pass floor; crash/fault tests pass | `payload_pack_v1`; disable new writes and dual-read legacy loose chunks/records |
| 2. Seal attempts honestly | `AttemptSealer`, durable recorder cursor, invalidation epochs, dirty-byte and sync accounting | no stale receipt accepted under exec/mmap/crash races; no-receipt path includes all work | `attempt_receipt_v1`; disable to synchronously rescan |
| 3. Make the existing v3 checkpoint the control plane | multi-locator store, bounded streaming v3 page builder/cursor, immutable checkpoint journal, shadow publication against current path | shadow `RootId`/`AttributionRootId` equality and semantic oracle across corpus; 1 GiB build/reconstruct stays within RSS bounds; space inventory reconciles | `checkpoint_publisher_v2`; dual-read/single-selected-write rollback |
| 4. Replace complete carriers for the hot OCI path | exact-parent frozen mount-recipe bundle, normalized clean delta, shallow projection catalog, receipt-based reuse | full canonical-v3 OCI oracle, including overlap-time hardlink identity/`st_nlink`, rename, full mode/ownership, absolute symlink, sparse, xattr/ACL/capability, whiteout/opaque, FIFO/device or explicit placement errors; publish/activate/depth/leak gates | `oci_projection_v2`; legacy reader/rebuild fallback under strict hot projection count/byte/inode quotas; never one complete carrier per logical root |
| 5. Switch public graph operations and MCTS refs | O(1) fork, public `squash_layerstacks` logical prune, ProductAccess rollback, winner selection, bounded active pool and GC | generated catalog exposes squash and rollback; both pass outer/service gates; 1,000 inactive, 32 siblings, 16 active, fault/cancel campaign; 64/1,000 non-closing same-upper campaigns pass `1.070 s p95/max` without changing `D_proj`; separate branch-projection campaigns pass their `1.070 s` publication, `99.9 ms` activation, `1.170 s` outer-max, `D_proj<=8`, and `D_settle` gates | `checkpoint_refs_v2`; branch-level rollback to old selection service |
| 6. Optional range/image accelerators | first proved reflink/block/EROFS/lazy plug-in, never part of correctness | one-byte 1 GiB localized allocation and latency gates plus the canonical semantic oracle | one independent capability gate per accelerator; probe failure falls back |
| 7. Retire legacy writes | stop new loose-object and complete-carrier creation after observation window | no fallback use, all Stage 04.6 OCI gates green, migration/rebuild drill succeeds | retain legacy readers and rebuild-by-root rollback for at least one release |

Each milestone has a kill switch that selects a previously qualified reader or
projection without changing checkpoint identity. Rollback never points a
committed ref at data readable only by the disabled implementation. Schema
additions use new tagged records and generation selectors; destructive
in-place format mutation is forbidden.

Shadow publication is restricted to isolated qualification fixtures or a
strict byte-capped production sample. Both legacy and candidate allocations
are charged to `P_staging`, reported as migration peak, and reclaimed after
comparison. A dual-write interval is never presented as a settled-space pass.

After Stage 04.6, Phase 3 implements the stock Firecracker image adapter and
WASI direct provider, then runs cross-backend golden-root, behavior-oracle,
resource, recovery, and cold/warm campaigns under independent adapter feature
gates. The optional hierarchical Firecracker block backend remains a separate
accelerator. None of that work changes the logical store or blocks the
preceding OCI release.

The release decision is based on medians/tails and correctness, not the best
sample. Milestone 4 is not enabled by default unless post-setup small
publication and the combined immediate-receipt-miss cell are at most
1.070 seconds p95, stored-projection ready is at most 99.9 ms p95, warm
lookup remains non-inferior, and every space/recovery gate passes. Milestone 5
also requires public logical squash and cached-projection rollback at
`<=20 ms p95` outer and `<=1 ms p95` service; 64/1,000 non-closing
logical-layer campaigns at `<=1.070 s p95/max`, unchanged `D_proj`, and no
rejection/deferred readiness; separate branch-projection campaigns at
`<=1.070 s` publication, `<=99.9 ms` activation, `<=1.170 s` outer maximum,
and `D_proj<=8`; both campaign types settled by `D_settle`; and zero
unexplained external-dependency delta. A 500x label is used only when the
complete declared boundary is at
most 214 ms for publication or 20 ms for workspace-ready activation **and**
does not exceed `matched_current_p95 / 500`.

## Final architectural decision

Do not build CAS-first loose-object publication plus directory-carrier vectors
as the primary physical publication/materialization architecture.
Preserve the Stage 03 v3 Merkle checkpoint and SeqCDC identity semantics,
replace loose-object CAS with a packed/adoptable multi-locator payload store,
make hash-and-durability receipts explicit, and treat every native/block/lazy
representation as a replaceable projection.

Frozen-upper promotion survives only in two constrained roles: a short-lived
exact-parent OCI accelerator, and a byte-source for a normalized delta or
payload locator. It is neither backend-neutral identity nor sufficient
durability by itself.

This is the strongest buildable design under the stated constraints. With a
valid completed receipt it can make the final layer-root commit
metadata-bound; public logical squash is payload-free; cached-projection
rollback/reactivation is metadata- and mount-bound. Receipt misses and cold
historical roots retain their measured physical work. The design keeps the
already-fast lookup, avoids native copies for inactive MCTS nodes, admits the
qualified directory path's large-file limitation, and lets Phase 3 use block
and direct providers without contaminating logical roots.
