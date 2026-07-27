# Portable Split-CoW architecture

Status: **PROPOSED STAGE 04.6 ARCHITECTURE**

This document defines the required portable copy-on-write architecture for
EphemeralOS workspace sessions. It is intentionally independent of
[`plan.md`](plan.md). It refines, but does not replace, the carrier ideas in
[`design_recommendation_from_sheppard_combined_with_layerstack.md`](design_recommendation_from_sheppard_combined_with_layerstack.md).

The decision is to use one backend-neutral checkpoint identity with three
different CoW granularities:

1. runtime file-level CoW for fast, isolated workspace sessions requested by
   independent external clients;
2. checkpoint path-level CoW for fast fork, rollback, and logical graph
   operations; and
3. durable chunk-level CoW for deduplicated publication and storage.

These are not three filesystems, three checkpoint identities, or three full
copies of a repository. They are one pipeline in which each layer avoids a
different category of unnecessary work.

## Executive decision

Portable Split-CoW is the required architecture.

The required correctness path must not depend on reflink, FUSE, KVM, ublk,
device mapper, a custom kernel, host-installed packages, or a particular host
filesystem. It uses:

- a normal disk-backed directory carrier;
- stock OverlayFS where it qualifies inside the Linux OCI environment;
- one private disk-backed upper per active workspace session;
- promotion-first sealing, in which the current upper becomes an immutable
  backend-local carrier delta and execution receives a fresh upper;
- LayerStack path deltas and immutable `RootId` checkpoints; and
- CAS/CDC file recipes and chunks for durable storage, with sealed file ranges
  permitted as immutable physical payload locators.

Promotion-first is the required normal post-checkpoint path, not an optional
accelerator. A qualified ordinary checkpoint must not publish a root and then
reconstruct its complete native carrier. Complete carrier construction is
reserved for a true cold miss, an incompatible carrier, or a correctly
reported portable fallback.

Optional backends may provide finer-grained CoW when their capabilities are
available. They are accelerators, not sources of truth. A checkpoint created
through any accelerator must resolve to the same canonical `RootId` as the
portable path.

The architecture is host-OS agnostic in the deployable OCI sense: it works on
Linux hosts and on macOS or Windows hosts that provide a qualified Linux OCI
environment. It does not claim that one Linux mount implementation natively
supports Windows containers. A native Windows-container adapter would be a
separate projection backend over the same `RootId`.

## Goals

- Make workspace activation, fork, rollback, and normal incremental
  publication independent of total repository size.
- Deliver at least a 100x improvement for normal repeated materialization and
  publication operations; 500x is the stretch objective.
- Keep active workspace sessions isolated while sharing immutable repository
  payload.
- Preserve efficient CAS/CDC deduplication without requiring a complete
  checkout to be rebuilt for every new root.
- Make every ordinary newly published root immediately reusable as a runtime
  carrier without duplicating its changed payload.
- Support repositories with large files, millions of small files, offline
  package-install simulations, and many concurrent CLI/MCP clients and
  workspace sessions.
- Keep storage-service memory bounded and independent of repository size.
- Add only bounded metadata and cache space relative to the current
  OverlayFS + CAS/CDC design.
- Preserve backend-neutral identity for OCI, Firecracker, and WASI.
- Keep rollback, parallel rollout, and MCTS branching metadata-cheap.

## Non-goals

- Implement a universal transparent sub-file CoW filesystem without an OS
  integration point.
- Eliminate the first mandatory read of an arbitrary, previously unindexed
  repository.
- Claim range-CoW for the portable OverlayFS path.
- Make a one-byte edit inside a large lower file space-efficient in the active
  upper on every host.
- Put repository payload in `tmpfs`.
- Make process or VM state part of filesystem `RootId`.
- Make a backend-specific carrier authoritative.
- Transparently hot-switch the layer stack beneath processes that retain open
  files, mappings, or working directories. The portable path seals at a
  quiescent session boundary.
- Introduce physical deletion or GC authority into Stage 04.6.

## Why the split is necessary

No single portable mechanism is optimal at every point:

| Layer | Granularity | Work it avoids | Required mechanism |
| --- | --- | --- | --- |
| Runtime CoW | files and directories | copying the complete repository for each active workspace session | shared immutable lower plus private OverlayFS upper |
| Checkpoint CoW | changed paths and namespace operations | walking and rebuilding every path for fork, checkpoint, rollback, and squash | persistent LayerStack tree/path deltas |
| Storage CoW | chunks and file recipes | storing and transferring complete changed files or repositories | CAS/CDC chunks, recipes, and Merkle objects |

The three improvements are not multiplied together. Each removes work at a
different boundary:

```text
sandbox command execution
      │
      ▼
runtime file-CoW
      │ changed upper
      ▼
checkpoint path-CoW
      │ changed paths and operations
      ▼
storage chunk-CoW
      │ changed chunks and Merkle paths
      ▼
canonical RootId
```

The resulting complexity target is:

```text
create/fork workspace:  O(mount and session metadata)
checkpoint namespace:   O(changed paths)
durable payload:         O(changed bytes or scanned changed files)
logical rollback/squash: O(root metadata)
```

The current complete-carrier path is approximately:

```text
O(all repository paths + all repository bytes)
```

## Authority and identity

`RootId` is the sole canonical filesystem-content identity. It is derived from
canonical LayerStack objects and is independent of execution history and
backend representation.

`AttributionRootId` remains separate. It does not alter filesystem-content
identity or prevent carrier sharing.

Backend carriers are reconstructible caches keyed by:

```text
(RootId, backend_kind, backend_format_version, target_profile)
```

The following never enter `RootId`:

- host paths;
- inode numbers;
- OverlayFS upper or work paths;
- whiteout device or xattr encoding;
- opaque-directory xattrs;
- mount IDs or mount-option order;
- carrier generation numbers;
- reflink or shared-extent identities;
- FUSE, ublk, device-mapper, or block-map IDs;
- Firecracker image and snapshot IDs;
- WASI handles; and
- process-template IDs.

The authority flow is one-way:

```text
RootId + CAS objects ──reconstruct──► backend carrier

frozen workspace upper ──normalize and publish──► new RootId
```

A carrier can accelerate access to a root. It cannot redefine or silently
modify that root.

## Architecture

```text
                         backend-neutral authority
                  RootId + AttributionRootId + refs
                                      │
                         ┌────────────▼────────────┐
                         │ LayerStack checkpoint   │
                         │ path pages + CAS/CDC    │
                         │ chunks + file recipes   │
                         └────────────┬────────────┘
                                      │
                       reconstructible carrier cache
                                      │
                         ┌────────────▼────────────┐
                         │ immutable lower carrier │
                         │ shared by active sessions│
                         └────────────┬────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
      session A upper         session B upper        session N upper
       + Overlay mount          + Overlay mount        + Overlay mount
              │                       │                       │
              └────────────── frozen changed uppers ─────────┘
                                      │
                         ┌────────────▼────────────┐
                         │ WorkspaceSealer freezes  │
                         │ and transfers ownership  │
                         └────────────┬────────────┘
                                      │
                  ┌───────────────────┼───────────────────┐
                  │                   │                   │
                  ▼                   ▼                   ▼
          exact local carrier   sealed-range CAS   changed-path
               delta               locators         normalization
                  │                   │                   │
                  └───────────────────┼───────────────────┘
                                      ▼
                         canonical checkpoint commit
                                      │
                                  new RootId
                                      │
                          fresh private runtime upper
```

### Required components

| Component | Responsibility |
| --- | --- |
| `CheckpointStore` | canonical tree, file, segment, chunk, root, and ref objects |
| `PayloadStore` | ownership of sealed payload, immutable range/pack/remote locators, recipes, and bounded reads/writes |
| `CarrierRegistry` | immutable backend carrier generations keyed by `RootId` and profile |
| `WorkspaceActivator` | per-session upper/work allocation, mount, lease, and teardown |
| `WorkspaceSealer` | session quiescence, writable-FD/mapping drain, durability receipt, and upper ownership transfer |
| `ChangeRecorder` | bounded changed-path and optional dirty-range evidence |
| `UpperNormalizer` | conversion from backend-private upper semantics to canonical operations |
| `Publisher` | changed-path update, CAS/CDC publication, root commit, and ref OCC |
| `ProjectionAdapter` | OCI, Firecracker, WASI, or optional accelerator projection |
| `Verifier` | semantic equivalence, receipts, bounded audits, and quarantine |

The component boundaries must remain concrete. A generic filesystem framework
or a second checkpoint identity is not required.

## Promotion-first refinement

Promotion-first changes the post-checkpoint dataflow from copy-and-rebuild to
freeze-and-reuse:

```text
copy-and-rebuild:
    mutable upper
      -> scan/hash
      -> copy payload into CAS
      -> commit RootId
      -> construct another native carrier
      -> activate

promotion-first:
    mutable upper
      -> quiesce, sync, and transfer ownership
      -> exact immutable carrier delta
      -> sealed-range CAS locators
      -> changed-path RootId commit
      -> activate with a fresh upper
```

The required safe sequence is:

1. stop admission of new writes for the workspace session;
2. reach a declared quiescent boundary;
3. drain writable file descriptors, writable mappings, and incomplete
   filesystem operations;
4. sync changed files, directory entries, and operation metadata;
5. detach the upper from all writable use;
6. transfer its files to `PayloadStore` ownership;
7. install an immutable exact-carrier manifest and leases;
8. compute or validate canonical CDC recipes and changed Merkle paths;
9. install sealed-range locators and commit the new `RootId`; and
10. activate continued execution over the promoted carrier vector with a new
    private upper.

There is exactly one owner:

```text
PayloadStore owns the promoted files
CarrierRegistry leases the exact native view
workspace sessions receive read-only access
```

A promoted file that is the sole durable locator for reachable chunks is
pinned payload, not disposable carrier cache. It becomes independently
evictable only after another durable locator is installed and all applicable
leases drain. Stage 04.6 records and enforces this rule but does not acquire
physical deletion or GC authority.

Promotion is portable because it uses ordinary disk files, ownership,
bounded streaming, manifests, and mounts. Transparent replacement of a live
mount underneath open FDs is deliberately excluded. Stock OverlayFS
continuation uses a new mount or remount at the quiescent boundary. A
DeltaFS-like custom-kernel adapter may later optimize that boundary without
changing the portable contract.

## Runtime file-CoW

The normal OCI/Linux path presents an ordinary POSIX workspace to the
container:

```text
lowerdir = immutable carrier for selected RootId
upperdir = private disk-backed directory owned by one workspace session
workdir  = private disk-backed OverlayFS work directory
merged   = workspace path visible to the container
```

The container image does not need LayerStack, FUSE, a shell, package
installation, or filesystem-specific libraries. The sandbox supervisor
prepares the mount externally. The workload sees a normal `/workspace`.

Clean files remain in the shared lower. A newly activated workspace session
pays for mount and session metadata, not a copy of every repository byte.
Modified paths appear in the private upper.

The merged workspace and its upper are writable only for the owning workspace
session. After promotion, the former upper is never writable again. A workload
that must retain live writable descriptors or mappings across a checkpoint
cannot use portable promotion at that instant; it must reach quiescence,
restart from the new session boundary, or use a separately qualified
live-switch accelerator.

The portable fast path requires a qualified OverlayFS environment. The
capability probe must validate:

- mount permission within the intended namespace;
- backing-filesystem compatibility;
- whiteout and opaque-directory behavior;
- file, directory, symlink, hardlink, and rename behavior;
- supported ownership, mode, timestamp, xattr, and sparse-file semantics; and
- the exact mount options used by the adapter.

If qualification fails, the correct fallback is a complete native directory
projection. The fallback preserves correctness and identity but does not meet
the hot 100x objective. It must be reported as a fallback, never as the
optimized path.

## Checkpoint path-CoW

LayerStack represents a new root by copying only changed fixed-fanout Merkle
paths. Fork and rollback select immutable roots without moving payload.

The normalized mutation vocabulary includes:

| Workspace mutation | Canonical checkpoint operation |
| --- | --- |
| create or replace regular file | file node plus content recipe |
| append, overwrite, or truncate | replacement file recipe, reusing unchanged chunks |
| create directory | directory node and metadata |
| unlink | deletion of the named entry |
| OverlayFS whiteout | canonical unlink; overlay encoding is discarded |
| opaque directory | replace/hide inherited children according to canonical tree semantics |
| file/directory/symlink type change | delete old type and create new typed node |
| rename | canonical remove plus insert with preserved identity semantics where supported |
| symlink | canonical link target and metadata |
| hardlink | canonical hardlink-group semantics |
| chmod/chown/timestamps/xattrs | supported canonical metadata update |

OverlayFS-private artifacts are input evidence, not checkpoint identity.
Normalization must reject ambiguous or unsupported semantics instead of
silently publishing a different tree.

For a repository with `N` paths and `D` changed paths:

```text
complete checkpoint work ≈ O(N)
path-CoW checkpoint work  ≈ O(D * tree depth)
```

Examples:

| Repository | Changed paths | Approximate metadata-work reduction |
| ---: | ---: | ---: |
| 100,000 paths | 10 | 10,000x fewer path visits |
| 500,000 paths | 100 | 5,000x fewer path visits |
| 1,000,000 paths | 10,000 | 100x fewer path visits |

These ratios describe avoided traversal work, not guaranteed end-to-end
latency.

## Durable chunk-CoW

The publisher processes only files named by the normalized path delta. For
each changed regular file it:

1. reads a bounded stream;
2. computes the canonical CDC/chunk boundaries;
3. reuses chunks already present in the parent recipe or CAS;
4. installs only new payload identity and at least one durable locator;
5. builds changed segment, file, and tree pages; and
6. atomically publishes the resulting `RootId`.

Physical payload location is independent of chunk identity:

```text
ChunkId -> [
    SealedFileRange(storage_file_id, offset, length),
    PackRange(pack_id, offset, length),
    RemoteObject(provider_key),
    LegacyLooseObject(object_id)
]
```

The normal post-checkpoint path first adopts immutable ranges from the
storage-owned promoted upper. It must not copy those bytes into another native
tree or pack merely to commit the root. Pack creation is required for new
non-adoptable input and may later migrate adopted ranges through a bounded,
journaled operation without changing `ChunkId` or `RootId`.

The immutable-locator index is paged and cursor-driven. It must not create a
root-sized in-memory vector. Queues carry descriptors, not unbounded payload
bytes. When packs are required, they are bounded append-only packs rather than
one loose filesystem object per chunk.

Dirty-range evidence is optional:

- with trusted exact dirty ranges, hash only affected chunks plus the required
  CDC resynchronization halo;
- without dirty ranges, scan the complete changed file but store and transfer
  only new chunks.

This distinction is essential. A tiny edit in a `1 GiB` file can still require
a `1 GiB` scan on the portable path, but durable new data should remain near
the changed chunk range.

## Workspace-session lifecycle

### Create from an existing root

1. Resolve and lease the requested `RootId`.
2. Resolve a compatible immutable carrier generation.
3. Build the carrier once on a true cache miss; concurrent requests join the
   same bounded single flight.
4. Allocate a private disk-backed upper and work directory.
5. Mount the merged workspace and run a constant-size readiness probe.
6. Return the workspace session.

Steps 4–6 are independent of repository bytes. Step 3 remains byte
proportional on a true cold carrier miss.

### Fork

A fork creates a new logical child reference over the same immutable carrier
vector. A clean inactive fork creates no native payload. Activating that child
as a workspace session creates bounded metadata, a private upper/work
directory, a mount, and leases.

### Checkpoint and publish

1. Quiesce the workspace session, drain writable FDs/mappings, and obtain a stable
   durability receipt.
2. Freeze and transfer storage ownership of its upper.
3. Register an exact immutable carrier delta bound to its parent dependencies
   and capability receipt.
4. Normalize upper-private operations.
5. Compute canonical chunk identities and install sealed-range locators for
   adoptable payload.
6. Publish changed Merkle paths.
7. Commit the new `RootId` and attribution root.
8. Activate continued execution with a fresh private upper.

The optimized path must not construct another complete merged tree or copy
adoptable changed payload between steps 2 and 8.

Hashing and normalization may begin speculatively while the external client is
not mutating the workspace session. A later write invalidates the affected
receipt. Only work revalidated against the final seal may participate in the
commit. Benchmarks report actual background work separately from the final
user-visible checkpoint boundary.

### Add a new layer

A published delta is appended to the immutable carrier dependency vector.
Existing lower payload is reused. New sessions mount the updated vector
without reconstructing the complete root.

Operational carrier depth should remain at or below 4, should be compacted
before it grows materially, and must reject activation above a hard depth of
8. Logical LayerStack ancestry can be deeper because logical ancestry and
physical mount depth are different concerns.

### Exact and normalized carriers

Promotion creates an exact backend-local carrier:

```text
exact parent generations
+ promoted immutable upper
+ exact mount options
+ semantic capability receipt
```

This is the fastest reuse format, but its OverlayFS-private metadata and lower
identities are not assumed portable across hosts.

A normalized portable carrier is a canonical directory delta or complete
directory projection reconstructed from `RootId`. It may be built
asynchronously when cross-environment reuse or depth compaction justifies the
cost. The exact carrier and normalized carrier are caches for the same root;
neither is checkpoint authority.

### Rollback

Rollback selects a prior `RootId`, discards or detaches the current private
upper, and activates an existing compatible carrier. It does not reverse-copy
payload.

### Squash

Logical squash changes graph topology or root references without flattening
payload. The accepted p95 budget is `10 ms`; the existing `1–6 ms` result is
already sufficient and should not be over-optimized.

Physical carrier compaction is a separate, bounded cache-construction
operation. It must not be hidden inside logical squash latency.

## Large-file behavior

The portable path has an explicit limitation:

```text
one-byte write to a 1 GiB lower file
    → OverlayFS may copy the complete 1 GiB file into the private upper
```

Portable Split-CoW does not make this worse than the current OverlayFS
solution, and it must not claim to solve it.

After publication:

- the changed path is represented once in LayerStack;
- CAS/CDC can retain approximately `64 KiB–1 MiB` of new chunks, depending on
  chunking and resynchronization;
- network transfer can be limited to those new chunks; and
- the temporary complete-file upper becomes reclaimable after all required
  ownership, leases, and recovery rules allow it.

Without exact dirty-range evidence, publication may still scan the complete
file. At an achieved scan/hash rate of `1–5 GiB/s`, scanning `1 GiB` would take
approximately `0.2–1.0 s`, excluding durability and metadata commit.

Range-CoW acceleration for this case requires an optional integration such as
reflink, FUSE Chunk-CoW, a block backend, or a VM-specific CoW device. No
portable transparent sub-file CoW exists for arbitrary unmodified programs
when all filesystem, block-device, kernel, and VM integration points are
excluded.

## Many-small-file behavior

Package installation can create or mutate hundreds of thousands of paths.
That is genuine changed work and cannot be reduced to constant time.

The storage architecture must not recognize package managers, lockfiles,
manifests, directory names, commands, or development tools as special
optimization references. An installation is an ordinary filesystem delta:

```text
parent RootId
    + normalized creates, replacements, metadata changes, and deletions
    + promoted immutable upper
    = new RootId
```

The new layer logically shadows the parent through normal LayerStack
semantics. It does not mutate the immutable parent or require a
package-specific cache key.

The implementation must nevertheless avoid amplification:

- enumerate only the promoted upper and its normalized operations, never the
  complete merged repository;
- stream directory enumeration into a bounded disk-backed spool;
- sort and merge path records with bounded fan-in;
- batch fixed-fanout directory/Merkle pages and durability;
- pack or inline small payload records;
- reuse unchanged parent nodes, file recipes, and existing chunks;
- avoid one temporary file and one fsync per CAS object;
- avoid a second complete native tree;
- cap open file descriptors, workers, queue descriptors, and pending bytes;
- apply deterministic admission backpressure; and
- make cancellation release every spool, descriptor, permit, lease, and
  staging owner.

Offline `pip install` and `npm install` simulations should use pre-generated
archives or local package caches so the benchmark measures filesystem
mutation, checkpoint, and publication rather than network latency.

For `100,000` genuinely new files, path-CoW still processes approximately
`100,000` changes. Packing can reduce backing-store object creation by
`100–1,000x`; realistic end-to-end publication improvement is expected to be
closer to `3–20x` than `500x` relative to the current loose/per-record or
complete-tree publication behavior. A matched baseline is required before
claiming that ratio.

## Complexity notation

Space and time claims in this specification use the following symbols:

| Symbol | Meaning |
| --- | --- |
| `B` | logical payload bytes reachable from the complete repository root |
| `F` | paths/inodes reachable from the complete repository root |
| `R` | immutable roots, refs, checkpoints, and logical rollout nodes |
| `A` | activated workspace sessions |
| `DeltaP` | normalized changed-path operations in one checkpoint |
| `DeltaB` | genuinely new durable payload bytes after reuse and deduplication |
| `H` | physical payload bytes allocated in the private workspace upper |
| `H_scan` | upper payload bytes lacking valid pre-sealing or dirty-range evidence and therefore requiring scan/hash work |
| `S_f` | size of a lower file receiving its first write on the required portable path |
| `K` | total payload chunks or storage extents |
| `K_delta` | chunks or extents affected by one checkpoint |
| `d` | persistent path/Merkle index depth, normally `O(log F)` |
| `X` | bytes requested by one read |
| `W` | global storage data workers, fixed at 4 |

`H` and `DeltaB` are deliberately different. Without reflink, FUSE, or
block-range CoW, a one-byte first write to a `1 GiB` lower file may create
approximately `1 GiB` of upper payload, so `H` can approach `S_f` even when
CDC later finds very little genuinely new durable content. Every benchmark
must report both values rather than describing `DeltaB` alone as the mutation
cost.

## Space model

Portable Split-CoW counts physical payload bytes once, even when the same
storage-owned bytes are exposed through both carrier and CAS locators. Its
physical model is:

```text
T_physical(t) =
    P_unique(t)
  + C_cache_only(t)
  + sum(U_active_private(t))
  + P_bounded_staging(t)
  + M_metadata(t)
```

Where:

- `P_unique` is the physical union of canonical CAS payload and
  promotion-owned carrier payload, with shared bytes counted exactly once;
- `C_cache_only` is bounded, reconstructible carrier content not already
  included in `P_unique`;
- `U_active_private` is changed data and metadata still owned by active private
  uppers;
- `P_bounded_staging` is explicitly owned, capped metadata and streaming
  scratch and must not contain another complete copy of changed payload; and
- `M_metadata` is manifests, indexes, journals, and leases.

The required persistent-space complexity is:

```text
T_physical =
    O(P_unique + sum(H_active[i]) + C_cache_only + M_metadata)
```

An inactive logical fork contributes `O(1)` durable metadata and zero payload.
An active clean workspace shares its immutable lower and adds no
repository-sized payload. An active changed workspace contributes its actual
private upper `H_i`. Multiple locators or roots referencing the same physical
payload do not multiply `P_unique`. No `Theta(A * B)` payload term is
permitted.

Relative to the current OverlayFS + CAS/CDC design:

| Space category | Expected difference |
| --- | --- |
| CAS chunks and recipes | approximately unchanged |
| shared immutable carrier | approximately unchanged in content; retained longer as a hot cache |
| active OverlayFS uppers | unchanged per mutation, but lowers are shared among workspace sessions |
| LayerStack path manifests | small additional metadata |
| dirty-path/range journals | small additional metadata |
| complete per-session workspace copies | reduced or eliminated on the optimized path |
| large-file first-write copy-up | unchanged portable worst case |

Expected persistent metadata overhead is `0.1–2%` of repository payload,
depending primarily on path count and chunk size. This is a target to measure,
not a presumption.

Metadata has the unavoidable structural complexity:

```text
M_metadata =
    O(total_encoded_path_bytes + F + K + R + DeltaP_journal)
```

It must not contain a payload-sized term. The following are qualification
ceilings:

| Metadata category | Required target |
| --- | ---: |
| fixed path/index metadata | `≤256 bytes/path`, excluding encoded pathname and xattrs |
| chunk or extent descriptor | `≤96 bytes/chunk` |
| root, ref, or logical-fork record | `≤1 KiB/root` |
| fixed change-journal record | `≤256 bytes/change`, excluding encoded paths |
| payload-dominated corpus metadata | `≤2%` of unique payload |
| application-resident index window | `≤2 MiB`, independent of on-disk index length |

The percentage target is not meaningful by itself for a repository dominated
by empty or tiny files. The 100k- and 1M-file qualifications must therefore
report encoded path bytes, fixed bytes per path, bytes per chunk, bytes per
root, total metadata bytes, backing object count, and inode count separately.
Variable-length pathnames, xattrs, and user metadata are charged at their
actual encoded size and may not be hidden in the fixed-record figures.

Promotion-first makes the adopted changed payload the storage-owned payload.
The promoted inode is counted once even when `CarrierRegistry` leases it as a
native view and `PayloadStore` exposes ranges from it as CAS locators.

For changed payload size `H`:

```text
P_publish_peak(H) =
    H_promoted_once
  + M_publish
  + B_streaming_scratch
  = H + O(M)
```

`M_publish` is locator, manifest, journal, and index metadata.
`B_streaming_scratch` is bounded independently of `H`. The required
promotion-first path has no second payload-sized term: a publication run that
copies or reconstructs another complete `H` does not satisfy this equation and
cannot pass the Stage 04.6 optimized-path space gate.

Publication staging may grow with changed metadata, but not changed payload:

```text
P_bounded_staging =
    O(DeltaP records + bounded merge pages)

queued_payload_bytes = 0
B_streaming_scratch <= 3 MiB application-wide
```

External sorting uses bounded fan-in and a fixed number of open runs. No
staging phase may contain another complete `H`, use one loose temporary object
per payload chunk, or retain an unbounded descriptor, FD, task, mount, or
payload queue.

The carrier may still coexist with other CAS payload for the unchanged base.
This is a bounded performance cache, not another canonical checkpoint. The
current design already constructs a comparable filesystem-form
materialization; Split-CoW changes its sharing, reuse, and lifetime rather than
inventing a third content truth.

Illustrative active space:

| Workload | Complete per-session copies | Portable Split-CoW |
| --- | ---: | ---: |
| `1 GiB` base, 100 active workspace sessions, `10 MiB` unique changes each | approximately `100 GiB` | approximately `1 GiB` shared lower + `1 GiB` uppers, plus CAS/cache metadata |
| `1 GiB` base, 1,000 clean inactive forks | up to approximately `1 TiB` if eagerly materialized | no new native payload; bounded graph metadata only |
| `1 GiB` base, 16 one-byte edits inside the same large file | implementation-dependent complete copies | portable worst case can still approach `16 GiB` of temporary uppers |
| Promote a `250 MiB` generated upper | up to `250 MiB` upper plus `250 MiB` new CAS payload | approximately `250 MiB` storage-owned payload plus metadata |

The carrier cache must have explicit byte, inode, generation, and depth
quotas. Reclamation remains owned by the appropriate later retention/GC
authority; Stage 04.6 must not silently acquire deletion authority.

## Memory model

The design is disk-backed and memory-bounded, not literally memory-free.

It requires no:

- repository-sized in-memory checkout;
- `tmpfs` workspace;
- repository-sized chunk table in application memory;
- unbounded path set;
- unbounded payload queue; or
- process-template population.

Unavoidable memory includes process state, bounded hashing and IO buffers,
mount metadata, the kernel page cache, dentries, inodes, and filesystem slab.
Page cache is reclaimable but must still be observed under the service cgroup;
it cannot be ignored when claiming memory safety.

Stage 04.6 must use the following lean qualification profile:

| Resource | Required bound |
| --- | ---: |
| global storage data workers | 4 |
| admitted heavy storage-job coordinators | 16 |
| pending heavy storage-job admission queue | 16 descriptors and `≤64 KiB` encoded metadata |
| non-resident storage IO byte credits | `64 MiB` |
| total application-owned resident storage working set | `≤8 MiB` |
| resident index window, included in the `8 MiB` total | `≤2 MiB` |
| hydration/hash buffer, included in the `8 MiB` total | `≤256 KiB` per data worker; `≤1 MiB` total |
| all coordinator and pending-queue state, included in the `8 MiB` total | `≤1 MiB` |
| CDC/hash/encoding/merge scratch, included in the `8 MiB` total | `≤3 MiB` |
| allocator, accounting, and emergency headroom, included in the `8 MiB` total | `≤1 MiB` |
| queued payload bytes | 0; payload is borrowed or streamed |
| storage-service RSS qualification target | `≤min(96 MiB, paired idle RSS + 32 MiB)` |
| aggregate storage memory-domain soft watermark | `≤96 MiB` |
| aggregate storage memory-domain hard ceiling | `≤128 MiB` |

The `8 MiB` resident bound is one global, non-double-counted budget. Its
subrows describe the intended partition rather than independent allowances.
Unused capacity in one partition may be borrowed by another only through the
same global resident-memory permit pool. An implementation must acquire a
resident permit before allocation and return it when the allocation becomes
unreachable.

With bounded admission, application-owned storage memory has constant
repository complexity:

```text
M_application = O(1) with respect to B, F, H, K, R, and A
M_application <= 8 MiB
W = 4
admitted_coordinators = 16
pending_descriptor_only_jobs = 16
```

Durable registries may grow on disk with `R` and `A`, but are accessed through
the bounded index window. Increasing repositories, workspace sessions, or
clients must not create a resident record per path, chunk, root, or session.

The `64 MiB` IO-credit window is not a memory-allocation allowance. It limits
the logical disk ranges concurrently borrowed or streamed so that the four
workers can retain IO parallelism. Payload charged as an IO credit must remain
on disk, be processed through a permitted bounded buffer, and never be copied
into a credit-sized resident allocation. This separation preserves the
four-worker throughput path while reducing the former effective
`64 MiB + 16 MiB` application-managed envelope by approximately ten times.

The aggregate memory domain includes service RSS, resident mappings,
attributable page cache, dentries, inodes, filesystem slab, and storage helper
processes. Reclaimable kernel cache is excluded from the `8 MiB`
application-owned budget but included in the aggregate watermarks. At the
`96 MiB` soft watermark, the service must stop optional prefetch, release
one-pass mappings and cache where supported, and apply admission backpressure.
It must reject new heavy work with typed, retryable `ResourceExhausted` before
the `128 MiB` hard ceiling can cause an OOM kill.

The RSS target must be checked against a release-build paired idle
measurement. If release idle RSS itself prevents the `96 MiB` absolute bound,
the implementation does not silently weaken the gate: it must report the idle
components and reduce the process/runtime footprint or obtain an explicit
specification change.

In this table, a **heavy storage job** is an internal, request-scoped
materialization, hydration, checkpoint-publication, carrier-construction,
CAS/CDC, pack, or storage-maintenance job initiated by a CLI/MCP operation.
The coordinator owns only bounded operation state and schedules bounded data
tasks on the four shared storage workers.

External agents remain outside the sandbox and orchestrate workspace sessions
through CLI/MCP requests; they are not deployed into, represented by, or
counted as storage workers or storage jobs.

The 16-job bound is not a limit on external agents, CLI/MCP clients, logical
branches, workspace sessions, ordinary control-plane requests, or commands
running inside a sandbox. A long-running `exec_command` uses the separate
backend execution and workspace-session resource ledgers. Its ordinary
filesystem reads and writes go through the mounted filesystem and private
upper; it does not retain a heavy-storage-job coordinator or data worker merely
because the command is running. A checkpoint request for that same workspace
may wait for quiescence or return a typed `WorkspaceBusy`.

When all 16 heavy-storage-job coordinators are occupied, at most 16 additional
descriptor-only admissions may wait. Further heavy storage jobs receive
deterministic, retryable backpressure. Pending admissions allocate no payload,
private upper, mount, or repository-sized metadata. Lightweight metadata and
status operations use a separately bounded control path and must not queue
behind bulk hydration or publication.

Repository size may increase persistent index length on disk, but it must not
increase the bounded application-managed working set. Large manifests, path
sets, publication journals, and coordinator spools remain disk-backed and are
read through bounded cursors or page windows.

Sealed-range adoption adds locator descriptors and leases, not file-sized
memory. Hashing a `1 GiB`, `10 GiB`, or larger adopted file uses the same
bounded streaming buffers. The storage service must not use `read_to_end`, a
file-sized mapping, an in-memory record per repository path, or a flat
in-memory chunk vector. Allocations use fallible reservation; an allocation
that cannot obtain resident permits returns typed backpressure rather than
attempting an unbounded allocation.

### Cost of the lean memory profile

The lean profile trades cache capacity and overload latency, not correctness,
large-file capacity, or backend-neutral identity:

| Source of cost | Expected effect before measurement | Required response |
| --- | --- | --- |
| `8 MiB` application-owned resident bound | `0–5%` normal throughput loss when four-way streaming remains effective | retain four workers and tune bounded windows; do not restore unbounded buffers |
| `2 MiB` resident index window | additional index-page reads; metadata-heavy 100k/1M-file workloads may be more sensitive | benchmark bounded window sizes and optimize page locality |
| `128 MiB` aggregate ceiling | less warm page, dentry, and inode cache; cold or repeated large directory walks can have higher tail latency | measure reclaim and cache-miss rates; adjust only the aggregate reclaimable-cache allowance if required |
| disk-backed coordinator and path state | small additional metadata IO | batch bounded records and preserve crash-safe journals |
| more than four data-heavy jobs | queueing latency grows while aggregate throughput remains bounded by four workers | descriptor-only admission and fair scheduling |
| exhausted coordinator/queue/memory permits | excess heavy jobs do not start immediately | deterministic typed retry/backoff; never OOM or partially publish |

These percentages are design estimates, not results. Qualification must sweep
bounded resident configurations while holding four workers and `256 KiB`
worker buffers constant. The `8 MiB` configuration passes only if normal
materialization and publication throughput is within `5%` of the fastest
bounded configuration and all semantic, recovery, and space gates pass.

A literal tenfold reduction of the complete former `512 MiB` aggregate-domain
ceiling to approximately `51 MiB` is not the default architecture. That would
also remove useful reclaimable filesystem cache and can create cache thrash or
cgroup OOM risk on many-small-file workloads. It may be reported as an
experimental ultra-lean profile only when release idle RSS fits, overload is
rejected before OOM, and the same throughput and semantic gates pass.

High request load is handled by bounded concurrency rather than resident
growth. Four workers perform data work, up to 16 lightweight coordinators own
bounded job state, and up to 16 descriptor-only admissions may wait. Further
heavy jobs receive retryable backpressure. Long-running sandbox commands
remain on their separate execution/workspace ledgers and do not consume these
storage slots merely by continuing to run.

## Time-complexity requirements

The required portable path must satisfy the following bounds:

| Operation | Required total-work complexity | Forbidden hidden work |
| --- | --- | --- |
| create a logical fork | `O(log R)` durable metadata and `O(1)` payload | `Theta(B)` copy or `Theta(F)` traversal |
| activate an existing exact carrier | `O(1)` in `B` and `F`; bounded mount/setup work | complete materialization or repository traversal |
| activate a private workspace upper | `O(1)` in `B` and `F` | eager lower copy |
| roll back to an existing root | `O(log R)` metadata | reconstruction of the selected root |
| logical squash | independent of `B` and `F`; bounded LayerStack/ref metadata | payload copy, CDC, or complete-root traversal |
| read `X` unchanged bytes | `Theta(X)` payload IO plus touched-extent lookup | materialization or scan of unrelated bytes |
| write a file already present in the upper | `Theta(bytes written)` | complete-root work |
| first portable write to a lower file | worst case `Theta(S_f)` copy-up | claiming `Theta(edit size)` without a qualified range-CoW accelerator |
| first CAS/CDC ingestion | `Theta(B + F)` | sublinear first-ingestion claim |
| first cold carrier construction | `Theta(B + F)` | inclusion in warm activation timing |
| incremental checkpoint total work | `O(H_scan + DeltaP * d + K_delta)` | `Theta(B + F)` root scan or reconstruction |
| durable finalization after valid pre-sealing | `O(DeltaP * d + K_delta)` | reporting pre-sealing work as eliminated |
| `DeltaP` genuinely new small files | at least `Theta(DeltaP + DeltaB)` | constant-time or universal 500x claim |
| chunk/extent dedup lookup | expected `O(1)` or `O(log K)` per lookup | linear scan of stored chunks |

The bounds apply to total CPU and IO work, not only user-visible blocking.
Pre-sealing may move `H_scan` before the checkpoint boundary, but the benchmark
must still include it in actual checkpoint work. An implementation fails the
incremental gate if ordinary publication performs work proportional to `B` or
`F` when `H_scan`, `DeltaP`, and `K_delta` remain fixed.

## Expected performance

The recorded `870.08 MiB` results below are the current
CAS/CDC/materialization comparison baseline for the proposed Portable
Split-CoW architecture:

| Operation | Measured baseline |
| --- | ---: |
| first publication / CDC / CAS ingestion | `107.024 s`, `8.13 MiB/s` |
| cold complete native materialization | `9.988 s`, `87.12 MiB/s` |
| explicit same-key materializer call | `6.362 s` |
| ordinary warm generation lookup | `0.035375 ms` |
| logical squash | approximately `1–6 ms` |

The following are design targets, not measured results. Ratios in the final
column compare the complete proposed architecture with the current measured
implementation or the explicitly named current copy-based behavior. A row
without a matched current measurement is an absolute target, not a measured
speedup:

| Operation | Acceptance target | Stretch target | Comparison with current implementation |
| --- | ---: | ---: | ---: |
| activate a stored `870 MiB` root from an existing carrier | `≤100 ms` p95 | `≤20 ms` p95 | approximately `100x`; stretch approximately `500x` versus `9.988 s` |
| explicit same-key usable session | `≤50 ms` p95 | `≤20 ms` p95 | approximately `127x`; stretch approximately `318x` versus `6.362 s` |
| activate a forked workspace session from an existing carrier | `≤10 ms` p95 | `≤2 ms` p95 | absolute target; matched current baseline pending |
| rollback to an existing carrier | `≤50 ms` p95 | `≤10 ms` p95 | absolute target; matched current baseline pending |
| logical squash | `≤10 ms` p95 | preserve current result | current `1–6 ms` is already accepted |
| incremental publish, approximately `1 MiB` across 10 ordinary files | `≤100 ms` p95 | `≤20 ms` p95 | absolute target; matched current workload required before claiming a ratio |
| CAS/CDC streaming throughput on large input | `≥1 GiB/s` | `≥5 GiB/s` | approximately `126x`; stretch approximately `630x` versus `8.13 MiB/s` |
| scan a changed `1 GiB` file without dirty ranges | `≤1.0 s` | `≤0.2 s` | absolute `1–5 GiB/s` scan/hash target; matched scan baseline pending |
| tiny edit in `1 GiB` file, durable new payload | `≤1 MiB` typical | `≤128 KiB` with range accelerator | approximately `1,000–8,000x` less durable payload than retaining a complete changed file; latency must be measured separately |
| first cold complete carrier construction | improve independently | `2–3 s` diagnostic | absolute diagnostic; remains byte proportional |

For small deltas, upper-only enumeration and Merkle path-CoW reduce internal
path work from approximately `N` repository paths to `D` changed paths times
tree depth. The resulting `N/D` work ratio is not an end-to-end latency claim.
For an installation or any other operation that genuinely creates `100,000`
paths, all `100,000` changes are processed once; packing, batching, bounded
parallelism, and removal of duplicate payload/carrier writes provide the
expected `3–20x` improvement against the current publication path.

Promotion-first adds the following incremental targets over a minimal
Portable Split-CoW implementation:

| Operation | Minimal Split-CoW | Promotion-first | Incremental improvement |
| --- | ---: | ---: | ---: |
| existing-carrier activation | `20–100 ms` | `10–50 ms` | approximately `1–2x` |
| newly published root if no reusable carrier was registered | possible `2–10 s` fallback | `20–100 ms` | approximately `20–500x` |
| newly published root when promotion already succeeds | `20–100 ms` | `10–50 ms` | approximately `1–2x` |
| activate a forked workspace session | `2–10 ms` | `1–5 ms` | approximately `2x` |
| rollback | `10–50 ms` | `5–20 ms` | approximately `2–5x` |
| small-edit final publication boundary | `20–100 ms` | `5–30 ms` with valid pre-sealing | approximately `2–10x` perceived |
| actual small-edit publication work | `20–100 ms` | `10–50 ms` | approximately `1.5–3x` |
| large generated upper publication | hash plus CAS payload copy | hash plus locator commit | approximately `1.5–3x` |
| changed-payload peak allocation | approximately `2H` | approximately `H` plus metadata | up to approximately `2x` better |

These are engineering estimates, not measured evidence. Pre-sealing can reduce
user-visible blocking without reducing total CPU or IO work, so both values
are mandatory results. Promotion-first does not improve the first ingestion of
an arbitrary unindexed repository, the first portable copy-up of a huge lower
file, or a complete changed-file scan without dirty-range evidence.

The 100–500x objective applies to repeated activation, fork, rollback, and
ordinary incremental publication that avoid complete-repository work. It does
not apply honestly to:

- the first read and hash of an arbitrary unindexed repository;
- a package installation that genuinely creates hundreds of thousands of
  files; or
- the first portable OverlayFS write to a huge lower file.

Throughput improvements require a real parallel CDC/hash pipeline, bounded
streaming, batched durability, packed objects, and removal of per-record
filesystem transactions. Split-CoW determines which bytes need work; it does
not by itself make hashing run at `5 GiB/s`.

Improvements at the three layers must not be multiplied together because they
refer to different operations.

## Performance tolerance

- Sustained command and ordinary filesystem throughput may regress by at most
  `5%` unless a separately accepted exception is recorded.
- Logical squash at or below `10 ms` is accepted.
- A cold complete-read/materialization regression up to the previously
  accepted `48%` may be tolerated only when hot-path gains, correctness, and
  space gates pass and there is no obvious implementation defect.
- Every benchmark must report mount-ready time, first access, complete scan,
  first write/copy-up, checkpoint, durable publication, and deferred work
  separately.
- Publication throughput must never be labeled materialization throughput.
- Warm metadata lookup must never be labeled a usable workspace activation.

## Multi-agent and MCTS behavior

An MCTS node stores logical references:

```text
node_id
parent_node_id
RootId
AttributionRootId
optional execution-state cache key
```

Creating a clean child node does not create a native projection. Native state
is created lazily only when a client activates a workspace session for that
node.

Parallel rollouts:

- share immutable lower carriers and CAS payload;
- receive separate private uppers and mount namespaces;
- publish independent immutable roots;
- update shared refs only through optimistic concurrency control;
- cannot mutate another rollout's lower or upper;
- can roll back by selecting a prior root;
- can discard losing runtime state without deleting canonical payload; and
- can reactivate a winning root on another backend.

The architecture therefore scales active physical state with the number of
active, changed workspace projections rather than the total number of logical
tree nodes or external clients.

## Backend adapters

| Backend | Required/optional representation | Canonical authority |
| --- | --- | --- |
| OCI/Linux | required shared directory carrier plus qualified OverlayFS upper; promotion-first exact carrier; complete-directory fallback | `RootId` |
| Firecracker | optional filesystem image and block/VM CoW accelerator | `RootId` |
| WASI | namespace/extent provider with capability-mediated mutations | `RootId` |
| reflink | optional native payload/copy-up accelerator | `RootId` |
| FUSE Chunk-CoW | optional range-CoW workspace projection | `RootId` |
| ublk/device mapper/NBD | optional Linux block accelerator | `RootId` |

Backend-specific process templates, VM memory snapshots, and block maps are
disposable execution caches. Filesystem publication always produces canonical
LayerStack semantics before a root becomes backend-neutral.

## Failure and recovery

Carrier and publication state uses:

```text
Building -> Ready -> Published -> Terminal
```

Promotion also has a journaled ownership transaction:

```text
AttemptOwned -> Sealing -> PayloadOwned -> LocatorReady -> RootPublished
```

- `STATE` is operation and recovery truth.
- `MANIFEST` is immutable after `Ready`.
- `CURRENT` selects the published carrier generation.
- Private work is never discoverable through `CURRENT`.
- Before `RootPublished`, a promoted upper is private journal-owned payload,
  not a public checkpoint or a generally evictable carrier.
- `PayloadOwned` records the sole owner, stable storage identity, durability
  receipt, and recovery action before the publication operation can relinquish
  ownership.
- A root becomes visible only after every reachable new chunk has at least one
  durable locator and the locator index has been durably committed.
- If an adopted range is the only durable locator, its storage file remains
  pinned until another durable locator is installed and all dependent leases
  drain.
- Recovery resumes or rolls forward from the last durable ownership state. It
  never guesses whether an upper is workspace-owned, publication-owned,
  payload-owned, or safe to discard.
- Exact-carrier publication, locator installation, root publication, and ref
  update are idempotent. The ref update remains the final OCC-controlled
  visibility step.
- Large IO, hashing, traversal, hydration, and cleanup occur outside the
  writer lock.
- Publication is idempotent and fails closed on ambiguous state.
- Cancellation joins workers and releases all mounts, FDs, buffers, permits,
  leases, queues, and operation-owned staging.
- A failed carrier is rebuildable from `RootId`; a failed carrier never
  corrupts checkpoint authority.

Stage 04.6 may clean exact operation-owned private work. It does not retire,
delete, or garbage-collect published roots or generations.

## Benchmark matrix

Use the preserved
[`baseline-experiment/README.md`](baseline-experiment/README.md) protocol and
add matched runs for:

| Corpus/workload | Required observations |
| --- | --- |
| preserved `870.08 MiB` corpus | cold carrier miss, stored-carrier activation, fork, read, write, checkpoint, publication |
| `1 GiB` single file | no change, append, truncate, one-byte overwrite at start/middle/end |
| mixed large-file repository | changed-file scan rate and durable chunk reuse |
| 100k and 1M small files | activation, mutation walk, path spool, pack count, inode and FD peaks |
| offline fake `pip install` | same generic mutation pipeline; created/modified paths, checkpoint and publish time, space peak |
| offline fake `npm install` | same generic mutation pipeline; many-small-file and symlink behavior, checkpoint and publish time |
| directory operation suite | whiteout, opaque directory, rename, type change, hardlink, symlink, metadata |
| 16 active siblings | fork latency, mount count, shared lower bytes, private upper bytes |
| 1,000 clean inactive forks | logical latency and metadata only; no native payload |
| deep checkpoint history | activation depth, compaction trigger, rollback, logical squash |
| promotion of small and large uppers | quiescence, ownership transfer, bytes copied, locator install, immediate activation, peak allocated bytes |
| sealed-range adoption and later packing | stable `ChunkId`/`RootId`, sole-locator pin, lease drain, bounded migration, no mandatory duplicate payload |
| pre-sealing with subsequent writes | receipt invalidation, revalidation, actual total work, final user-visible blocking |
| cancellation and crash injection | every sealing, ownership, locator, root, and ref boundary; bounded residue, deterministic recovery, lease and mount release |
| OCI/Firecracker/WASI equivalence | identical semantic oracle and canonical `RootId` |

Every run records:

- `B`, `F`, `R`, `A`, `DeltaP`, `DeltaB`, `H`, `H_scan`, `K`, `K_delta`,
  and index depth `d`;
- logical and allocated bytes;
- unique, shared, staging, and unexplained bytes;
- inode and object counts;
- fixed and variable metadata bytes per path, chunk, root, and journal record;
- process RSS and cgroup memory;
- page cache where observable;
- elapsed and CPU time;
- bytes read, hashed, written, reused, and transferred;
- work amplification ratios
  `bytes_scanned / max(H_scan, 1)`,
  `paths_visited / max(DeltaP, 1)`, and
  `peak_payload_bytes / max(H, 1)`;
- workers, queues, FDs, mounts, leases, and permits;
- carrier depth and fallback reason; and
- final quiescence and owned cleanup.

## Acceptance gates

Portable Split-CoW is accepted only when:

1. stored-carrier activation meets the 100x p95 target on the preserved corpus;
2. an ordinary newly published root is immediately reusable through its
   promoted carrier without complete native reconstruction;
3. adopted changed payload satisfies
   `P_publish_peak(H) = H + O(M)`: it is counted once and is not copied into a
   second payload-sized allocation merely to commit the root;
4. the 500x stretch result is reported honestly, whether achieved or missed;
5. ordinary incremental publication is proportional to changed paths and
   changed payload rather than repository size;
6. actual checkpoint work and inference-masked user-visible blocking are
   reported separately;
7. the published root matches a complete semantic oracle;
8. 16 active siblings share one immutable lower and retain isolated uppers;
9. 1,000 clean inactive forks allocate no repository-sized native payload;
10. permanent metadata overhead is measured and remains within its declared
   target;
11. no repository-sized memory structure, `tmpfs` dependency, or unbounded
   queue exists;
12. large-file copy-up and many-small-file limitations are visible rather than
   hidden;
13. the portable path requires no reflink, FUSE, KVM, ublk, custom kernel, or
    container-image package;
14. optional accelerators produce the same `RootId` and fail back safely;
15. OCI, Firecracker, and WASI adapters preserve the qualified semantic
    profile;
16. all resource, cancellation, recovery, ownership, locator, lease, and space
    accounting gates pass;
17. every reported speedup names a matched current
    CAS/CDC/materialization baseline or is labeled an unmeasured absolute
    target;
18. installation benchmarks use the same generic delta path as every other
    mutation and introduce no package-, filename-, command-, or
    directory-specific storage behavior;
19. Stage 04.6 acquires no forbidden deletion, retirement, or GC authority;
20. application-owned resident storage memory remains within one
    non-double-counted `8 MiB` permit domain while four storage data workers
    remain enabled;
21. storage-service RSS satisfies
    `≤min(96 MiB, paired idle RSS + 32 MiB)`, and aggregate storage-domain
    memory remains below the `96 MiB` soft watermark during steady operation
    and the `128 MiB` hard ceiling under qualified peak load;
22. overload produces bounded queueing or typed retryable backpressure before
    OOM, without partial root publication or checkpoint-identity divergence;
23. inactive forks add `O(1)` metadata and zero payload, active storage scales
    with `sum(H_active)` rather than `A * B`, and application-owned storage
    memory remains `O(1)` in repository and history size;
24. ordinary incremental checkpoint work is
    `O(H_scan + DeltaP * d + K_delta)` and never silently becomes
    `Theta(B + F)`;
25. publication peak payload satisfies `H + O(M)` with no second
    payload-sized staging or CAS-copy term;
26. fixed metadata records satisfy the declared per-path, per-chunk, per-root,
    and per-change ceilings, with variable path and xattr bytes reported
    separately; and
27. first ingestion, first cold carrier construction, large-file portable
    copy-up, and genuine many-file creation are reported with their unavoidable
    byte/path-proportional complexity rather than included in warm or
    incremental speedup claims.

## Implementation order

### Slice 1: contracts and measurement

- Freeze timing boundaries and the semantic oracle.
- Add carrier, change-recorder, and publisher interfaces.
- Record byte, inode, memory, queue, FD, mount, and lease accounting.
- Split resident-memory permits from non-resident IO credits and prove that
  every resident allocation is charged exactly once.
- Record paired idle, peak, and settled RSS plus aggregate-domain memory for
  1, 4, 16, and overloaded heavy-storage-job workloads.
- Preserve the historical baseline unchanged.

### Slice 2: shared carrier activation

- Build and register immutable carriers by `RootId`.
- Activate private disk-backed uppers over a shared lower.
- Add bounded single-flight construction and exact-key reuse.
- Prove 16-sibling isolation and carrier sharing.

### Slice 3: promotion-first sealing

- Drain writable FDs and mappings at a declared quiescent boundary.
- Sync, detach, and transfer upper ownership to `PayloadStore`.
- Register exact backend-local carrier manifests and dependency leases.
- Activate continued execution with a fresh private upper.
- Prove that no ordinary promoted root falls back to complete reconstruction.

Retain the current CAS copy path for durability until the promotion lifecycle,
recovery, and semantic probes pass.

### Slice 4: upper normalization

- Implement the canonical mutation vocabulary.
- Validate whiteout, opaque directory, rename, type-change, hardlink, symlink,
  metadata, and sparse-file behavior.
- Reject unsupported semantics before publication.

### Slice 5: sealed-range adoption and changed-work publisher

- Stream changed paths through bounded spools.
- Install immutable sealed-file-range locators behind an explicit feature
  gate.
- Pin sole-locator adopted files through ownership and leases.
- Add packed CAS writes and grouped durability.
- Reuse parent file recipes and unchanged chunks.
- Replace root-sized in-memory vectors with bounded page builders/cursors.
- Prove crash recovery at every ownership, locator, and root-commit boundary.

### Slice 6: pre-sealing, carrier reuse, and depth

- Pre-hash and normalize stable upper content while waiting for inference.
- Invalidate speculative receipts after subsequent writes.
- Enforce dependency receipts and depth limits.
- Keep logical squash separate from physical carrier compaction.

### Slice 7: qualification

- Run the complete corpus, mutation, package-install, multi-agent, recovery,
  space, and backend-neutrality matrix.
- Compare matched medians and tails against current and main-branch controls.
- Report missed targets without weakening correctness or architecture.

Optional range-CoW backends follow only after the portable pipeline is correct
and measured.

## Rejection conditions

Reject or redesign an implementation that:

- rebuilds the complete repository for normal workspace creation;
- publishes an ordinary root and then constructs its complete carrier instead
  of promoting the sealed upper;
- scans every repository path for an ordinary small checkpoint;
- writes all payload into a new native tree before publishing;
- copies adoptable promoted payload into a new CAS allocation on the critical
  path without a measured and documented necessity;
- keeps three canonical payload copies for the three CoW layers;
- requires repository-sized RAM or `tmpfs`;
- retains writable access to a promoted upper;
- treats sole-locator adopted payload as disposable carrier cache;
- silently converts an OverlayFS upper into canonical identity;
- treats a carrier, mount, inode, VM snapshot, or block map as `RootId`;
- silently falls back to a complete copy while claiming 100x activation;
- hides first-access, copy-up, publication, or deferred work outside the
  reported latency;
- claims `5 GiB/s` without measured end-to-end byte accounting;
- makes clean forks allocate repository-sized payload;
- leaves unbounded carrier depth, staging, queues, or retirement state;
- breaks rollback or OCC under parallel rollouts;
- requires packages inside arbitrary Docker images; or
- makes an optional accelerator necessary for correctness.

## Final recommendation

Implement Portable Split-CoW as a pipeline:

```text
shared disk-backed runtime carrier
    + isolated per-session file-CoW upper
    + promotion-first immutable upper ownership transfer
    + LayerStack changed-path checkpoint
    + sealed-range or packed CAS/CDC payload locators
    + one backend-neutral RootId
```

This preserves the strongest properties of the current OverlayFS + CAS/CDC
design while removing complete-repository work from the operations that
dominate externally orchestrated multi-agent development: create, fork,
checkpoint, rollback, reactivate, and logical squash.

Promotion-first is the required normal path. It makes a newly published root
immediately usable, avoids rebuilding a complete carrier, and requires peak
changed-payload allocation of `H + O(M)`, with `H` counted exactly once.
Pre-sealing may reduce the final user-visible boundary, but actual work remains
measured.

The permanent space increase over the current design should be limited to
small bounded metadata. The main carrier-cache copy already corresponds to
the filesystem-form materialization required by the current runtime and is
shared rather than repeated. Memory remains bounded and disk-backed. The
portable large-file copy-up limitation stays explicit, while environments
with stronger capabilities may opt into range-CoW accelerators without
changing checkpoint identity or application behavior.
