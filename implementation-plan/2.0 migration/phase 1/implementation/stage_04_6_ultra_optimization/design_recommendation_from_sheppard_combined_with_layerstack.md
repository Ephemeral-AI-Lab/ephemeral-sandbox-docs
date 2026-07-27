# Shepherd live-carrier design combined with LayerStack

Status: **ISOLATED DESIGN RECOMMENDATION — NOT YET ADOPTED**

## Executive decision

Combine the strongest part of Shepherd with the durable LayerStack
architecture:

- use Shepherd-style immutable-upper promotion for fast, live OCI workspace
  fork, checkpoint, rollback, and reactivation;
- retain LayerStack CAS/CDC, `RootId`, `AttributionRootId`, immutable manifests,
  leases, and recovery as the authoritative checkpoint system;
- treat every native carrier as a reconstructible backend cache, never as a
  second checkpoint identity;
- keep the full native carrier as a portable recovery fallback;
- introduce a separate large-file carrier strategy because ordinary OverlayFS
  is file-level, not byte-range, copy-on-write; and
- never require `tmpfs`, reflink, FUSE, a loop device, device mapper, or a
  particular host filesystem for correctness.

This architecture is expected to provide a 100–500× improvement for the hot
operations that dominate parallel agent development: fork, rollback, exact
reactivation, small-edit native publication, and workspace-session creation
from an existing carrier. It does not make an honest 100–500× claim for first
ingestion of previously unread bytes or for a one-byte modification inside a
huge lower file.

## Shepherd evidence and boundary

The recommendation is informed by:

- [Shepherd paper](https://arxiv.org/pdf/2605.10913);
- [`shepherd` commit `d45074e`](https://github.com/shepherd-agents/shepherd/tree/d45074e0099d9ccafeed4a233702ad68ff8a2fa6);
- [`shepherd-experiments` commit `c12ebd1`](https://github.com/shepherd-agents/shepherd-experiments/tree/c12ebd1b774cf12f70ef2b4486e61e7052f3e3ab);
- [kernel OverlayFS carrier](https://github.com/shepherd-agents/shepherd/blob/d45074e0099d9ccafeed4a233702ad68ff8a2fa6/vcs-core/packages/core/src/vcs_core/_kernel_overlay.py);
- [carrier runtime abstraction](https://github.com/shepherd-agents/shepherd/blob/d45074e0099d9ccafeed4a233702ad68ff8a2fa6/vcs-core/packages/core/src/vcs_core/_substrate_runtime.py); and
- [frozen fork/revert benchmark](https://github.com/shepherd-agents/shepherd-experiments/blob/c12ebd1b774cf12f70ef2b4486e61e7052f3e3ab/exp/framework-perf/src/experiment_framework_perf/bench_agent_revert.py).

Shepherd's fast path is:

1. start from an already prepared lower filesystem;
2. run an agent over a writable OverlayFS upper;
3. quiesce and unmount;
4. rename the current upper into an immutable lower layer;
5. create an empty upper and work directory; and
6. remount the new lower vector.

The promotion itself copies no payload. Its cost is dominated by quiescence,
sync, directory metadata, and mount operations.

The reported Shepherd result is not a measurement of LayerStack-style durable
publication. Its initial full `cp -a` into `tmpfs` is outside the fork timer,
and the timed operation does not include CDC, hashing, CAS installation,
immutable root construction, attribution, durable reference advancement, or
cross-host restoration.

This recommendation adopts the promotion mechanism, not Shepherd's `tmpfs`
assumption or benchmark boundary.

## Architecture

```text
                    Backend-neutral checkpoint authority
                RootId + AttributionRootId + immutable tree
                                  │
                    ┌─────────────▼─────────────┐
                    │ LayerStack CAS/CDC store  │
                    │ roots, chunks, manifests │
                    │ leases and recovery      │
                    └─────────────┬─────────────┘
                                  │
                  reconstructible materialization cache
                                  │
                    ┌─────────────▼─────────────┐
                    │ Backend carrier registry │
                    │ keyed by RootId + format │
                    └─────────────┬─────────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             ▼                    ▼                    ▼
      OCI live carrier    Firecracker carrier    WASM/WASI projection
      directory layers    block/guest format     capability-scoped tree
             │
      [delta-N : ... : base]
             │
      per-attempt private upper
```

The authoritative relationship is one-way:

```text
CAS checkpoint ──reconstructs──► backend carrier

backend carrier ──publishes changed semantics──► new CAS checkpoint
```

A carrier may accelerate access to a root. It may never redefine the root.

## Why this is better than the implemented complete-carrier path

The current complete native materialization is approximately:

```text
T_complete =
    T_walk(all entries)
  + T_read(all required chunks)
  + T_write(complete native root)
  + T_verify(complete native root)
  + T_publish_generation
```

Its byte cost is proportional to the repository, even when the new root
contains a small source edit.

The recommended live checkpoint path is:

```text
T_live_checkpoint =
    T_quiesce
  + T_sync(changed upper)
  + T_validate(changed upper)
  + T_promote_metadata
  + T_mount
```

Durable publication remains separate:

```text
T_durable_publish =
    T_normalize(upper operations)
  + T_hash_and_CDC(changed regular-file bytes)
  + T_build_changed Merkle paths
  + T_publish RootId and attribution
  + T_publish carrier generation
```

For ordinary source changes, changed bytes and entries are much smaller than
the complete repository:

```text
changed bytes H << repository bytes R
```

The main speedup comes from avoiding `O(R)` native reconstruction, not from
making hashing or storage hardware unrealistically fast.

## OCI live-carrier topology

Before checkpoint:

```text
                    merged workspace
                           │
                  ┌────────▼────────┐
                  │ writable U2     │
                  ├─────────────────┤
                  │ immutable L1    │
                  ├─────────────────┤
                  │ immutable L0    │
                  └─────────────────┘
```

After checkpoint:

```text
1. quiesce and unmount
2. sync and validate U2
3. publish durable CAS checkpoint
4. rename/adopt U2 as immutable L2
5. create empty U3 and work3
6. remount

                    merged workspace
                           │
                  ┌────────▼────────┐
                  │ writable U3     │
                  ├─────────────────┤
                  │ immutable L2    │
                  ├─────────────────┤
                  │ immutable L1    │
                  ├─────────────────┤
                  │ immutable L0    │
                  └─────────────────┘
```

The `U2` payload moves from active-upper accounting to immutable-carrier
accounting. It must not be copied into a second native directory.

## Multi-agent workspace sessions

One immutable carrier vector is shared by bounded active attempts:

```text
                            RootId B
                               │
                     [L2 : L1 : L0]
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
       Attempt A          Attempt B          Attempt C
       upper-A            upper-B            upper-C
       work-A             work-B             work-C
       mount-ns-A         mount-ns-B         mount-ns-C
       process-A          process-B          process-C
```

Each active attempt owns:

- one writable upper;
- one OverlayFS work directory;
- one mount namespace and merged mount;
- one sandbox/process isolation boundary; and
- one lease over every immutable carrier dependency.

Each inactive MCTS node owns only:

- an immutable root reference;
- parent/edge and evaluation metadata;
- CAS retention required by policy; and
- no private upper, merged mount, process, or mandatory native carrier.

Forking an inactive node is an `O(1)` graph operation. Activating it is:

```text
T_activate =
    T_select_carrier
  + T_lease_dependency_vector
  + T_create_empty_upper_and_work
  + T_mount
```

If the compatible carrier is absent, the backend reconstructs it from CAS
through the bounded complete or delta path.

## Workspace-session operations

### Create from an existing carrier

1. Select a carrier manifest using:

   ```text
   (RootId, backend_kind, backend_format_version, target_profile)
   ```

2. Validate immutable state, generation, manifest digest, and dependency
   fences.
3. Lease the full dependency vector.
4. Create private upper/work directories.
5. Mount the merged view in the attempt's mount namespace.
6. Return workspace readiness.

No root payload is copied.

### Fork

1. Copy the logical root/reference and rollout metadata.
2. Do not create a carrier or upper for an inactive child.
3. On activation, share the selected lower vector and create a new private
   upper/work pair.

### Checkpoint and publish

1. Quiesce execution and prevent further writes to the upper.
2. Capture the exact parent root and carrier dependency fence.
3. Stream and normalize the upper's filesystem operations.
4. Publish changed content and tree paths through the existing CAS authority.
5. Obtain the new immutable `RootId` and `AttributionRootId`.
6. Validate that the frozen upper represents the same logical transition.
7. Publish the upper as an immutable backend carrier generation.
8. If execution continues, create and mount a new private upper.

CAS publication and carrier publication remain two existing authorities with a
defined ordering, not a new cross-authority atomic transaction.

If CAS publication succeeds but carrier publication fails, the root remains
valid and the carrier can be reconstructed. If CAS publication fails, the
upper is not exposed as a carrier for a nonexistent authoritative root.

### Rollback

1. Stop or quiesce the active attempt.
2. discard its uncommitted private upper according to session policy;
3. select and lease the carrier vector for the target `RootId`; and
4. mount a fresh private upper over that vector.

Rollback changes the selected immutable root. It does not reverse external
network or service side effects.

### Reactivate a winner

1. Select the winner's immutable root.
2. Prefer a compatible local carrier from the bounded execution pool.
3. Otherwise reconstruct it from CAS.
4. mount it with a new private upper.

Carrier locality changes latency only. It is not authoritative MCTS state.

## Carrier formats

Use one logical checkpoint model with three replaceable carrier families.

### Directory-delta carrier

Best for:

- source trees;
- ordinary build output;
- package installations with manageable entry counts;
- small and medium changed files; and
- OCI workspace sessions.

Implementation:

- Linux OverlayFS lower vector;
- promoted frozen upper as the newest immutable delta;
- disk-backed by default;
- Linux whiteout and opaque-directory encoding confined to the adapter; and
- complete-copy fallback where OverlayFS mounting is unavailable.

### Large-file carrier

Required for:

- one-byte or small-range edits inside `100 MiB`–`1 GiB` files;
- databases, model weights, disk images, and large generated artifacts; and
- workloads where complete-file OverlayFS copy-up violates space or latency
  budgets.

The logical file remains a backend-neutral chunked CAS object. Candidate
native adapters may include:

- an optional reflink implementation when verified at runtime;
- a block-addressed sparse image with changed-block mapping;
- a chunk-aware lazy file projection; or
- a Firecracker-local block-image delta.

No optional mechanism may become a correctness dependency. Until a portable
large-file adapter qualifies, the directory carrier uses a bounded
complete-file fallback and reports that cost honestly.

Plain OverlayFS must not be advertised as byte-range CoW:

```text
one-byte data edit in a 1 GiB lower file
        ↓
potential 1 GiB copy-up into the upper
```

### Complete carrier

Required for:

- first cold hydration;
- backend-format migration;
- recovery when no compatible dependency vector exists;
- deliberate physical flattening;
- environments where optimized carriers are unavailable; and
- verification qualification.

It is the correctness fallback, not the performance target for normal new
layers.

## Many-small-file handling

Upper promotion itself does not copy the files, but durable publication and
validation remain proportional to changed entries.

For `pip`, `npm`, and generated trees:

- traverse only the frozen upper, not the complete merged repository;
- stream sorted operation records with bounded memory;
- use fixed worker, file-descriptor, queue, and byte-permit limits;
- spill sorting/index state to bounded disk storage instead of holding every
  path in RAM;
- preserve atomic rename, whiteout, opaque-directory, symlink, and executable
  semantics;
- coalesce repeated operations before durable publication when they have not
  already crossed a publication boundary; and
- record logical entries, allocated blocks, inode use, and metadata bytes.

An upper with one million files still has `O(1,000,000)` metadata work.
Promotion can remain fast, but publication cannot truthfully be constant time.

## Space model

Measure physical allocation:

```text
T(t) =
    L_hot(t)
  + H_cold(t)
  + sum(U_active(t))
  + P_staging(t)
  + M(t)

D_ideal = C_current + H_unique
```

The recommended native topology is:

```text
shared immutable base carriers
+ immutable native deltas required by selected carrier vectors
+ active private uppers
+ one bounded staging target when reconstruction is necessary
+ bounded metadata
```

Promotion must satisfy:

```text
payload_before =
    immutable lowers
  + frozen U_active

payload_after =
    immutable lowers
  + promoted immutable delta

additional native payload copy = 0
```

Illustrative native allocation:

| Workload | Complete-copy topology | Recommended topology |
| --- | ---: | ---: |
| `1 GiB` base plus 32 roots with independent `1 MiB` changed files | up to `33 GiB` | approximately `1 GiB + 32 MiB` plus metadata |
| 16 active siblings over a `1 GiB` root | up to `16 GiB` of repeated lowers | one shared lower vector plus private uppers |
| 1,000 inactive forks | up to approximately `1 TiB` if materialized per node | zero additional native payload |
| Promote a frozen `250 MiB` package upper | upper plus another `250 MiB` reconstruction | adopt the existing `250 MiB` payload |
| One-byte edit inside a `1 GiB` lower file | complete root or complete file copy | still up to one complete changed file without a large-file carrier |

Existing amplification gates remain applicable:

- mixed/no-dedup settled target `≤1.08 × D_ideal`;
- many-small settled target `≤1.15 × D_ideal`;
- avoidable duplicate payload target `≤1%`;
- persistent unexplained bytes `0`;
- operational carrier depth target `≤16`; and
- hard carrier depth always below 64.

Stage 04.6 may construct and select a bounded replacement carrier. Retention
and deletion authority remain separate. All lease-protected, staging,
quarantined, and grace-period bytes remain visible in accounting.

## Memory and resource safety

The optimized path must not rely on placing the base repository in `tmpfs`.

Default placement:

```text
CAS and immutable carriers     persistent disk
private active uppers          persistent disk
bounded operation metadata     memory with explicit limits
tmpfs                          optional accelerator only
page cache                     opportunistic, never an acceptance assumption
```

Retain fixed limits for:

- concurrent materialization workers;
- bytes being hydrated or hashed;
- filesystem walkers;
- open files;
- path-record queues;
- retries;
- carrier depth; and
- active execution attempts.

Cancellation and failure must release permits, descriptors, staging
directories, leases, and mount references. No correctness state may exist only
in RAM.

Benchmark reporting includes:

- process RSS;
- cgroup memory;
- tmpfs allocation;
- page-cache observations where available;
- swap activity;
- worker and byte-permit high-water marks;
- queue depth; and
- open-file high-water marks.

## Backend neutrality

The same logical root can have several independent carriers:

| Backend | Carrier recommendation | Root authority |
| --- | --- | --- |
| OCI/Linux | OverlayFS directory vector; optional large-file accelerator | CAS `RootId` |
| Firecracker | guest workspace carrier or block-image delta; VM snapshot as cache only | CAS `RootId` |
| WASM/WASI | capability-scoped logical projection with explicit metadata support | CAS `RootId` |
| Portable fallback | complete native copy | CAS `RootId` |

The following never enter `RootId`:

- native paths;
- inode numbers;
- Linux whiteout or opaque xattrs;
- carrier generations;
- mount-option order;
- block-image identifiers;
- VM snapshot identifiers; and
- WASI handles.

Backend-specific carriers translate the same canonical filesystem semantics.
They do not silently discard unsupported metadata.

## Privilege and portability

The OCI optimized path may use `CAP_SYS_ADMIN` to mount OverlayFS inside a
controlled mount namespace. It must not require broader privilege.

Runtime qualification must detect:

- whether the kernel permits the required mount;
- whether container seccomp or LSM policy blocks it;
- whether the backing filesystem supports the needed OverlayFS semantics; and
- whether whiteout, opaque directory, xattr, hardlink, and rename behavior
  matches the adapter contract.

If qualification fails, use the correct complete-carrier fallback.

Docker images must not need custom filesystem packages or contain the storage
engine. Workspace mounts are managed by the sandbox runtime. On non-Linux
hosts, OCI execution may occur inside a Linux VM, but host-specific identity
must not leak into the checkpoint.

## Carrier manifest

A versioned carrier manifest should contain:

```text
root_id
backend_kind
backend_format_version
target_profile
generation
state
manifest_digest
ordered_dependency_generations[]
dependency_manifest_digests[]
construction_parent_root
whiteout_and_opaque_encoding_version
allocated_byte_accounting
```

`construction_parent_root` explains how the carrier was built. It does not
participate in content identity.

The existing lifecycle remains:

```text
Building → Ready → Published → Terminal
```

`STATE` remains operation truth, `MANIFEST` is immutable, and `CURRENT`
selects a published generation. Large IO and recursive traversal occur outside
the writer lock.

## Verification

Normal delta verification is compositional:

```text
verified dependency vector
+ Merkle equality for unchanged subtrees
+ verified frozen-upper operations and changed bytes
= verified requested RootId
```

Qualification additionally performs complete merged-tree audits. Exact reuse
must validate immutable state and digests without rereading the complete
repository.

The upper-to-CAS normalization must cover:

- regular-file creation and replacement;
- append and truncate;
- directories and directory metadata;
- unlink and whiteout;
- opaque directory;
- file/directory/symlink type replacement;
- relative and absolute symlinks;
- supported hardlinks;
- mode, ownership, timestamps, and xattrs;
- sparse-file promises; and
- rename normalization.

## Expected performance

The preserved Stage 04.6 baseline is:

| Operation | Current measurement |
| --- | ---: |
| Full publication/CDC/CAS ingestion, `870.08 MiB` | `107.024 s` |
| Cold complete native materialization, `870.08 MiB` | `9.988 s` |
| Explicit same-key materializer reuse | `6.362 s` |
| Ordinary warm generation lookup | `0.035375 ms` median |

Recommended targets:

| Operation | Target | Stretch | Basis |
| --- | ---: | ---: | --- |
| Hot workspace fork from existing carrier | `≤100 ms` p95 | `≤20 ms` p95 | No repository copy |
| Small-edit carrier promotion | `≤100 ms` p95 | `≤20 ms` p95 | Rename/adopt existing upper |
| Exact carrier reuse | `≤100 ms` p95 | `≤25 ms` p95 | Immutable metadata validation |
| Rollback to existing carrier | `≤100 ms` p95 | `≤20 ms` p95 | Discard upper and remount |
| Small-source-edit durable publication | `≤1.070 s` p95 | `≤214 ms` p95 | Process changed upper only |
| Logical squash | `≤10 ms` p95 | preserve prior result | No physical flatten |
| First cold complete materialization | improve independently | `2–3 s` diagnostic | Still byte proportional |
| First ingestion of unindexed `870.08 MiB` | establish physical lower bound | no dishonest 500× claim | Must read and hash source bytes |
| Tiny edit inside `1 GiB` file | qualify separate carrier | `≤100 ms` only with true block/chunk CoW | Directory OverlayFS is insufficient |

The 100–500× claim applies only when the operation avoids complete-repository
work. Every result reports:

- time to workspace-ready;
- first file read;
- first full repository scan;
- first write and copy-up;
- durable publication;
- warm reactivation; and
- deferred work.

## Benchmark requirements

Use the existing Stage 04.6 baseline experiment without modifying its
historical results.

Compare:

- current complete carrier;
- pinned legacy/raw-overlay path;
- direct native copy;
- Shepherd-style disk-backed upper promotion;
- durable LayerStack publication from the frozen upper;
- optional large-file carrier;
- Firecracker and WASI adapter prototypes when available.

Required workloads include:

- preserved `870.08 MiB` compiled-Rust corpus;
- `1 GiB` mixed repository;
- at least 20,000, 100,000, and 1,000,000 small entries;
- one-byte, `4 KiB`, and `64 KiB` edits inside `100 MiB` and `1 GiB` files;
- offline `pip` install, upgrade, and uninstall;
- offline `npm` install, update, and removal;
- 32 sibling tiny-edit publications;
- 64 and 1,000 inactive MCTS nodes;
- 1, 4, and 16 genuinely concurrent writable attempts;
- rollback and winner reactivation;
- logical squash and deliberate physical flatten;
- cold worker and locality-hit activation; and
- crash, cancellation, `ENOSPC`, and stale-fence injection.

Fixture preparation, network acquisition, and preservation copies remain
outside product timers. No required publication, verification, or first-read
work may be moved outside a timer to manufacture a speedup.

## Implementation slices

### Slice 1: live-carrier contract

- Add the backend carrier key and versioned manifest.
- Preserve complete-carrier v1 reading and fallback.
- Add dependency-vector leases and exact activation.
- Do not change `RootId`.

### Slice 2: isolated multi-agent activation

- Create one upper/work/mount namespace per active attempt.
- Share immutable lowers.
- Prove sibling isolation and bounded active rollout count.
- Keep inactive nodes payload-free.

### Slice 3: upper promotion

- Quiesce and freeze the upper.
- Publish through existing CAS authority.
- Validate and adopt the upper without copying.
- Rotate to a new upper when execution continues.
- Add crash and cancellation recovery.

### Slice 4: compositional verification

- Verify dependency digests and fences.
- Verify only normalized changed operations and bytes.
- Retain complete audit qualification.
- Remove byte-proportional exact reuse.

### Slice 5: depth and space controls

- Target depth at most 16.
- Reject admission before the hard limit.
- Build a bounded rebase/complete carrier outside the writer lock.
- Account for all old leased generations without deleting them.

### Slice 6: large-file carrier decision

- Benchmark the complete-file copy-up failure mode.
- Prototype block/chunk-aware alternatives under the privilege and portability
  constraints.
- Select an optional accelerator only with a correct fallback.
- Do not claim the large-file target until measured.

### Slice 7: qualification

- Run matched performance, space, memory, correctness, and crash experiments.
- Enable the new carrier format behind a feature gate.
- Make it default only after every hard gate passes.

## Rejection conditions

Reject or revise this design if any of the following is observed:

- a frozen upper must be copied to become a lower;
- active siblings can observe one another's writes;
- inactive nodes acquire native payload proportional to node count;
- carrier depth or mount-option length becomes unbounded;
- exact reuse rereads the complete root;
- first workspace access hides large deferred reconstruction;
- large-file copy-up violates admitted space without a bounded fallback;
- many-small-file publication requires unbounded RAM;
- persistent unexplained bytes remain after failure;
- restart recovery guesses state from directory presence;
- backend carrier identity leaks into `RootId`;
- OverlayFS becomes a required correctness dependency; or
- the optimized path needs more privilege than the admitted runtime permits.

## Final recommendation

Adopt Shepherd-style upper promotion as LayerStack's fast OCI live-carrier
path. Keep CAS/CDC and immutable roots as the durable, deduplicated,
backend-neutral authority.

This combination directly supports:

- cheap multi-agent fork;
- bounded parallel MCTS rollout;
- isolated workspace sessions;
- fast rollback and winner reactivation;
- small-edit publication proportional to changed upper data;
- efficient shared native storage;
- OCI performance without coupling logical identity to Linux; and
- independent Firecracker and WASM/WASI materialization adapters.

Do not use a full repository in `tmpfs` as the default, do not equate carrier
promotion with durable publication, and do not treat directory OverlayFS as
the solution for huge mutable files. The architecture is strongest as a
hybrid with explicit carrier specialization and one canonical LayerStack
checkpoint identity.
