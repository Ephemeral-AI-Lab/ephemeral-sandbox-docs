# LayerStack-0 / EphCoW versus Reflink: Complexity and Performance Analysis

**Date:** 2026-08-04  
**Status:** non-normative hypothesis; correctness result `NOT_RUN`; evidence
`OPEN`; final performance verdict `TARGET_UNSELECTED`  
**Working product name:** LayerStack-0  
**Working COW mechanism name:** Ephemeral CoW (`EphCoW`, code identifier `ephcow`)

## 1. Executive conclusion

No owner-approved quantitative performance target exists. A useful research
comparison is not “a faster implementation of `FICLONE`”; it compares precisely
matched operations while keeping native file cloning and LayerStack-0's broader
contract scopes distinct.

The LayerStack-0 research question is at a different boundary:

> **Research question:** can accepted-reference branching at the scope of a
> complete portable immutable Version qualify against an owner-selected matched
> comparator while also preserving namespace isolation, content identity,
> atomic publication, and OCC?

For a directory tree, recursive file-by-file reflink work grows with the number of
files and extents. A logical EphCoW fork can instead create one new namespace or
reference to an existing immutable Version, independent of the Version's byte and
file counts. This suggests a hypothesis for high-fan-out agent workloads,
especially for large or metadata-heavy sandboxes that are forked many times and
modified sparsely; it is neither a selected target nor evidence of a win.

This is a prediction, not a measured result. No matched benchmark has run. Historical
Stage 4.6 evidence remains `INCOMPARABLE` and must not be used to claim an EphCoW
win, a V2 performance guarantee, or a service-level objective.

There is also an architectural qualification: the currently selected R0 design
stores one complete immutable payload closure per `VersionId` and deliberately does
not select cross-Version chunk/object sharing, reflink payload trees, or a custom COW
workspace. A CAS+CDC extension to EphCoW would therefore be a storage-family change, not a
minor optimization to the selected R0. It requires a Phase 01 reopening unless the
term EphCoW is restricted to R0's already-selected metadata-only reference moves.

## 2. Decision boundary: selected R0 versus a proposed CAS+CDC extension

This note must not blur two materially different designs.

| Concern | Selected R0 contract today | Proposed CAS+CDC extension | Consequence |
|---|---|---|---|
| Logical truth | One complete immutable filesystem Version identified by `VersionId` | One complete immutable logical Version identified by `VersionId` | Compatible at the semantic level |
| Physical payload | One complete immutable payload closure per Accepted Version at an occupied `VersionId` | Immutable files/chunks/manifests shared across different versions | Changes the selected storage family |
| Reuse | Equal canonical bytes at one occupied `VersionId` reuse one physical payload | Unchanged content may be reused across different `VersionId`s | New identity, collision, retirement, and recovery obligations |
| Reference fork | Metadata-only reference update with payload bytes read, written, and copied equal to zero | Same | Compatible and already required by R0 |
| Writable workspace | Owned by existing runtime/workspace effect components | Potential custom lazy COW namespace backed by the immutable CAS | May change ownership and dependency direction |
| CDC | Not selected | Used to detect and store new unique content ranges | New CPU, memory, canonicalization, and resource behavior |
| Object/chunk DAG | Explicitly not selected | Likely required for sub-file cross-version sharing | Requires Phase 01 reopening |
| Performance status | Architecture selected; implementation and matched performance not proved | Proposal only | No winner claim is permitted |

The current authority is documented in:

- [Architecture decision](../architecture_design.md)
- [LayerStack-0 Version-storage design](../design/03-state-store.md)
- [Performance and optimization](../design/07-performance-and-optimization.md)

Accordingly, this analysis uses two meanings carefully:

1. **R0 reference COW:** checkpoint, fork, rollback-to-existing, and same-Version
   moves update references without reading, writing, or copying payload bytes. This
   is part of the selected design.
2. **Proposed CAS+CDC extension:** cross-Version physical sharing plus a lazy, isolated writable
   namespace. This is an architecture proposal whose benefit must be demonstrated
   and whose ownership must be selected jointly with its storage model.

The names “LayerStack-0” and “EphCoW” are working brands. They do not override the
product PRD or the Phase 01 architecture decision.

## 3. What is being compared

### 3.1 Full copy

A conventional recursive copy creates a new directory tree and copies file payload
bytes. It is portable but its fork cost generally grows with total files, metadata,
and bytes.

### 3.2 Recursive file-by-file reflink

Linux `FICLONE` makes two files share filesystem storage and turns later writes into
copy-on-write operations. It applies to a file, requires filesystem support, and
normally requires source and destination to reside on the same filesystem. A whole
sandbox tree therefore needs a directory walk, destination metadata creation, and
one clone or equivalent action per regular file.

This avoids copying payload bytes during the initial clone, but it does not make the
directory-tree operation constant-time. It also does not by itself supply portable
content identity, namespace/head semantics, OCC, publication recovery, or agent
authorization.

### 3.3 Filesystem-native snapshot

A Btrfs subvolume snapshot shares tree roots and extents through filesystem COW. It
is the strongest local-filesystem comparator because its snapshot operation can be
effectively instant after required dirty data has been flushed. It may therefore
beat or tie a logical EphCoW reference fork in raw local snapshot latency.

It is not an honest substitute for all LayerStack-0 obligations. A native snapshot
is tied to a filesystem and host implementation, nested subvolumes have distinct
snapshot behavior, and deferred deletion can carry substantial cleanup work.

### 3.4 Selected R0 reference move

When the destination already refers to an accepted immutable `VersionId`, R0 changes
only the relevant root or head binding. Payload I/O for that accepted binding path
must be:

```text
payload bytes read    = 0
payload bytes written = 0
payload bytes copied  = 0
```

This is an O(1)-shaped metadata operation with respect to the Version's byte and file
counts, subject to the chosen reference backend and durability protocol.

### 3.5 Proposed CAS+CDC extension

The stronger proposal combines:

- immutable content-addressed objects;
- content-defined chunking (CDC) for sub-file reuse;
- immutable manifests that define complete logical filesystem versions;
- constant-size roots, heads, and agent namespace bindings;
- a private writable view that reads unchanged content lazily and records changes;
- one OCC transition for publication; and
- bounded recovery, retirement, cache, scratch, FD, and worker behavior.

This could avoid recursive materialization at fork time and avoid rewriting unchanged
content at checkpoint time. However, it adds data structures, collision checks,
garbage-collection reachability, write tracking, and hot-path risks that do not exist
in the selected complete-payload R0 family.

## 4. Complexity model

Let:

| Symbol | Meaning |
|---|---|
| `S` | Total logical payload bytes in a sandbox version |
| `F` | Number of filesystem entries |
| `E` | Number of filesystem extents or equivalent clone units |
| `D` | Logical bytes changed since the base version |
| `M` | Metadata changed since the base version |
| `C` | Chunks inspected by CDC during publication |
| `U` | New unique content bytes admitted after deduplication |
| `N` | Concurrent or sequential agent forks from the same base |
| `R` | Number of reference/root/head records changed by an operation |
| `Q` | Recovery or retirement work left by interrupted operations |

The table gives target asymptotic shapes, not implementation guarantees:

| Operation | Full copy | Recursive reflink | Native subvolume snapshot | Selected R0 reference move | Proposed CAS+CDC extension |
|---|---:|---:|---:|---:|---:|
| Fork one existing version | `O(F + S)` | `O(F + E)` | Approximately one tree-root operation after flush | `O(R)`, normally `O(1)` | `O(R)`, normally `O(1)` |
| Fork same base to `N` agents | `O(N(F + S))` | `O(N(F + E))` | `O(N)` root operations plus filesystem work | `O(NR)` | `O(NR)` |
| Payload bytes copied at fork | `O(S)` | `0` | `0` | `0` | `0` |
| First modification | Usually direct private write | Filesystem COW of affected extents | Filesystem COW of affected nodes/extents | Runtime-workspace dependent | Intended to be proportional to affected private data, not the complete file |
| Publish an entirely new Version | `O(F + S)` | Not a Version-publication protocol | Filesystem-specific | R0 may inspect/process/write a complete canonical payload | Target `O(M + C)` work and approximately `O(U)` new physical bytes |
| Publish no content change | Usually still needs comparison or copy avoidance | N/A | New snapshot/Root metadata | Same-Version reference move must be zero payload I/O | Same; manifest/Root reuse should avoid CDC and payload I/O |
| Retire a version | Delete copied tree: `O(F + S)` physical cleanup shape | Metadata traversal and extent-ref updates | Logical delete may be fast; cleanup is asynchronous | Selected Phase 03 recovery/retirement family | Root removal plus bounded reachability/ref accounting; physical reclamation may be deferred |

Two caveats matter:

1. `O(1)` logical fork does not imply `O(1)` **execution readiness**. Opening a
   namespace, mounting or constructing a runtime view, starting a process, and
   faulting in data may add costs.
2. `D` alone is not automatically the CDC cost. If the implementation rescans every
   file or every payload byte on each checkpoint, the CPU/read complexity remains
   `O(S)` even when only a few bytes changed. Reaching changed-data-proportional work
   requires complete mutation tracking and safe reuse of unchanged canonical
   structures.

## 5. Expected performance ranking

These are engineering hypotheses to test.

### 5.1 Fork or branch-reference creation

Expected ordering for a metadata-heavy directory tree:

```text
native filesystem snapshot ~= R0/EphCoW reference fork
                               < recursive reflink
                               < full recursive copy
```

The first two should be treated as peers until measured. A native snapshot may win
the single-operation microbenchmark because it runs entirely inside a mature
filesystem. R0/EphCoW can win the product-level comparison when the measurement also
requires portable identity, agent namespace bindings, OCC-ready heads, and operation
observability.

### 5.2 High-fan-out multi-agent branching

EphCoW has its clearest potential advantage when many agents branch from one base:

```text
one immutable base
  + N small namespace/reference records
  + private changes only
```

Recursive reflink repeats the directory walk and destination inode/dentry creation
for every agent. A logical reference fork grows with agent count, but not with
`N * F` or `N * S`. As `F` and `N` grow, this difference should become more visible.

### 5.3 Steady-state reads

Native reflink or filesystem snapshots will probably win or tie. They remain on the
normal kernel filesystem path and benefit from the page cache, readahead, mature
extent mapping, and direct VFS integration.

A userspace EphCoW mapping can lose through:

- extra manifest and chunk lookups;
- context switches or FUSE-like request handling;
- fragmented reads across chunk boundaries;
- duplicated caching between kernel and userspace;
- decompression or verification on the read path; and
- cold CAS index access.

Therefore the design should not claim “faster than reflink” for generic reads.

### 5.4 Hot random writes

Native reflink will probably win ordinary random-write latency because the
filesystem owns extent COW directly. EphCoW can be competitive only if writes land
in a normal private writable file or efficient scratch representation and do not
run CDC, hashing, compression, or remote CAS work synchronously per syscall.

### 5.5 Tiny edits to very large files

This is a potential EphCoW win over a whole-file `copy_up` design such as a basic
OverlayFS lower-to-upper transition. Linux OverlayFS documents that copying up a
lower regular file creates the upper object and copies file data before modification.
If EphCoW tracks dirty ranges and republishes only locally affected chunks, a tiny
edit to a multi-gigabyte file could require far less read/write work.

This advantage disappears if EphCoW first materializes the complete file into
private scratch or rescans the entire file at every checkpoint. The benchmark must
measure the actual bytes read and written, not infer efficiency from wall time.

### 5.6 Checkpoint and publication

Selected R0 optimizes already-accepted same-Version movement, but admission of a new
unique complete Version can still process a complete canonical payload. CAS+CDC
EphCoW could improve sparse-change checkpointing by reusing unchanged content across
different `VersionId`s.

The expected benefit is strongest when:

- complete write tracking identifies exactly which files/ranges changed;
- unchanged manifest subtrees can be reused safely;
- CDC resynchronizes locally after insertions or deletions;
- new-object admission is batched;
- canonicalization and collision validation remain correct; and
- retirement does not impose unbounded synchronous garbage collection.

## 6. Proposed CAS+CDC extension execution shape

If Phase 01 is reopened and the CAS+CDC extension is selected, the implementation should
separate its control and data planes.

```text
CONTROL PLANE

  namespace/ref ----> immutable version root ----> manifest root
       |                       |
       |                       +---- VersionId / canonical identity
       |
       +---- head + expected generation ---- OCC ---- durable publication


DATA PLANE

  agent process
       |
       v
  private writable view
       |\
       | +---- changed metadata / dirty-range journal
       |
       +------ lazy reads of immutable base objects
                         |
                         v
                    shared read cache

  checkpoint:
    journal + changed private bytes
      -> canonicalize affected structures
      -> CDC changed regions/files
      -> hash and compare occupied identities by full bytes
      -> batch-admit new unique objects
      -> build immutable version root
      -> OCC head transition
```

The architecture must preserve current V2 responsibility boundaries unless Phase 01
explicitly changes them:

- portable immutable identity and durable selected-Version truth belong to the
  selected storage owner;
- authorization, request ordering, and orchestration remain application concerns;
- workspace, mount, namespace, and execution facts remain runtime-private effects;
- MCTS and rollout policy remain outside storage; and
- observability reads diagnostics but is not selected-Version authority.

If EphCoW itself owns the writable namespace or mounts, that is a new ownership
boundary and cannot be introduced as a private Phase 03 implementation detail.

## 7. Optimization rules for a credible implementation

### 7.1 Never CDC the immutable base during fork

Fork must bind a new agent namespace to an existing version root. It must not walk,
hash, chunk, or materialize the base payload.

### 7.2 Keep CDC off the syscall write path

Writes should go to a private writable representation and append bounded mutation
metadata. Chunking, hashing, and compression should occur at an explicit checkpoint
or background preparation stage, never as mandatory work for every small write.

### 7.3 Track every mutation path

Changed-data-proportional checkpointing is correct only if writes, truncation,
rename, unlink, link, symlink, chmod, ownership changes, timestamps, sparse-hole
changes, xattrs, and every supported sessionless edit path are either captured or
cause a safe full validation fallback.

Missing one mutation path is a correctness failure, not a performance bug.

### 7.4 Use local CDC resynchronization

An insertion near the beginning of a large file should not shift every subsequent
fixed-size chunk. CDC should allow boundaries to resynchronize within a bounded
window. The exact chunking grammar, min/target/max sizes, hash, and rolling-fingerprint
algorithm require separate identity and store design plus benchmarks.

### 7.5 Batch immutable-object operations

Batch existence checks, writes, durability barriers, and manifest construction.
Per-chunk syscalls and globally serialized index updates can erase the theoretical
fan-out advantage.

### 7.6 Share immutable caches, isolate mutable Workspace data

Agents may share verified immutable content and indexes. Dirty pages, scratch files,
mutation journals, open writable descriptors, and unpublished objects must remain
isolated per writable namespace or transaction.

### 7.7 Bound all deferred work

The design needs explicit caps and backpressure for:

- memory and index cache entries;
- open FDs;
- chunking and hashing workers;
- unpublished scratch bytes;
- in-flight object admissions;
- recovery records;
- retirement scans; and
- deletion/garbage-collection debt.

Fast foreground deletion that creates unbounded asynchronous cleanup is not an
end-to-end performance win.

### 7.8 Preserve the single publication point

Expensive preparation should occur outside the OCC critical section, but the head
transition must have one linearization point. A stale expected head loses cleanly;
there is no silent merge or rebase. Failed OCC must not leak an authoritative root,
and orphan cleanup must be bounded and recoverable.

## 8. Benchmark plan

### 8.1 Required comparators

Use at least these four implementations on the same machine and storage device:

| ID | Comparator | Purpose |
|---|---|---|
| A | Recursive full copy | Portable byte-copy baseline |
| B | Recursive file-by-file reflink | File-level COW baseline |
| C | Btrfs or another explicitly identified native snapshot | Filesystem-root COW baseline |
| D | LayerStack-0 selected mechanism or EphCoW prototype | System under test |

Comparator C must not be mislabeled as recursive reflink. They have different
algorithmic shapes. Unsupported filesystem/configuration results must be reported,
not silently removed.

### 8.2 Workload matrix

| Dimension | Required points |
|---|---|
| Logical Version size | 100 MiB, 1 GiB, 10 GiB; larger if practical |
| File count | 1,000; 100,000; 1,000,000 where practical |
| Agent fan-out | 1, 10, 100, 1,000 where resource limits permit |
| Changed fraction | 0%, 0.01%, 1%, 10%, 100% |
| File shapes | Few large, many small, mixed source repository, sparse files |
| Metadata shapes | Deep trees, symlinks, hard links, modes, xattrs if supported |
| Edit shapes | Append, overwrite, insert near start, truncate, rename, delete |
| Reuse shapes | Same exact Version, small delta, unrelated Version, duplicated content in unrelated paths |
| Cache state | Cold, warm metadata, warm data |
| Failure state | Crash before payload durable, before root durable, before/after OCC, during cleanup |

### 8.3 Measure phases separately

One “fork latency” number hides the relevant tradeoffs. Record:

1. logical reference or clone creation;
2. namespace/workspace ready;
3. first `stat`;
4. first byte read;
5. first private write durable enough for the runtime contract;
6. process/exec ready;
7. steady sequential and random read;
8. steady sequential and random write;
9. checkpoint preparation;
10. immutable payload admission;
11. OCC head publication;
12. stale-OCC rejection and cleanup;
13. namespace discard;
14. last-root retirement;
15. crash recovery to a clean writable truth.

### 8.4 Required measurements

For each phase collect:

- median, p95, p99, and maximum wall time;
- CPU time and CPU utilization;
- payload bytes read, written, and copied;
- metadata operations and syscalls where available;
- CDC bytes scanned and chunks emitted;
- hash/full-byte comparison work;
- CAS lookups, hits, misses, and admitted unique bytes;
- peak and steady memory;
- peak FDs and worker count;
- scratch bytes and unpublished-object count;
- recovery records and cleanup debt;
- physical allocation before, during, and after retirement; and
- correctness outcome for collision, stale OCC, crash, and mutation-isolation tests.

Report hardware, kernel, filesystem, mount options, cache state, compiler/profile,
dataset generator, and exact commit. Without these, the result is not reproducible.

### 8.5 Primary hypotheses

| Hypothesis | Pass evidence | Failure meaning |
|---|---|---|
| H1: reference fork is Version-size independent | Flat latency and zero payload I/O as `S` and `F` grow | Fork path is walking or materializing a Version |
| H2: fan-out work is not `N * F` | Near-linear growth in small per-agent records, not tree walks | Namespace creation repeats filesystem materialization |
| H3: sparse checkpoint work tracks change | Bytes processed/written move with `D + M`, not `S` | Mutation tracking or representation reuse is ineffective |
| H4: tiny edit avoids whole-file copy-up | Physical and logical I/O remain near affected regions | Writable path materializes or rescans full files |
| H5: cleanup is bounded | Stable limits and convergence after stress/failures | Foreground speed is borrowing unbounded recovery debt |
| H6: steady I/O regression is acceptable | Explicit threshold against native comparator | Custom namespace overhead undermines product value |

The project must set numeric acceptance thresholds before using these hypotheses as
release gates. This note intentionally does not invent them.

## 9. Performance claims that are and are not supportable

### Supportable now

- A selected R0 reference-only move is designed to perform zero payload-byte I/O.
- Recursive file-level reflink must process a directory tree at file granularity,
  whereas a logical version-root fork can be independent of file and byte counts.
- The CAS+CDC extension has a plausible asymptotic advantage for sparse checkpoints and
  high-fan-out branching if complete mutation tracking and structural reuse work.
- Native reflink/snapshot likely retains a hot-path advantage for ordinary local I/O.

### Not supportable until measured

- “EphCoW is faster than reflink.”
- “Fork is constant-time” as an end-to-end namespace/exec readiness statement.
- “Checkpoint cost is proportional to changed bytes.”
- Any latency, throughput, CPU, memory, storage-ratio, or agent-count SLA.
- Any comparison derived from historical Stage 4.6 results.
- Any claim that a custom userspace COW path beats native kernel COW for generic I/O.

A precise future message, if matched measurements support it, would be:

> **Reflink is optimized for cloning local file extents. EphCoW is optimized for
> branching portable, immutable multi-agent sandbox worlds.**

An operation-scoped brand line is:

> **Zero-payload accepted-reference branches for parallel agents.**

Both are positioning statements. Published performance wording must identify the
operation, comparator, hardware, filesystem, data shape, fan-out, cache state, and
percentile.

## 10. Architecture reopening required for the CAS+CDC extension

Before the CAS+CDC extension can become the V2 implementation plan, a reopened Phase 01
decision must resolve these questions jointly:

1. **Truth owner:** Does the existing `sandbox-runtime-layerstack` package own the
   manifest/chunk graph, or is another boundary strictly necessary?
2. **Writable view owner:** Does the existing runtime workspace owner construct the
   EphCoW view through direct calls, or does the selected-Version owner acquire runtime
   mount/namespace responsibilities?
3. **Storage family:** Are manifests and chunks the authoritative physical payload,
   and how does that preserve one complete immutable logical truth?
4. **Identity:** Which facts are canonical, which object identities exist below
   `VersionId`, and where full-byte collision comparison occurs?
5. **Publication:** Which objects become durable before root creation, and what is
   the single OCC linearization point?
6. **Recovery:** How are incomplete objects, complete-but-unpublished roots, and
   accepted heads distinguished after a crash?
7. **Retirement:** Is reachability, refcounting, tracing, or another bounded method
   authoritative, and how is last-root deletion proved safe?
8. **Migration:** How is there exactly one writable truth during cutover, and where
   does temporary migration code live and get deleted?
9. **Resource bounds:** What limits cache, FDs, workers, scratch, object admission,
   recovery records, and GC debt?
10. **Necessity evidence:** Which measured R0 failure cannot be corrected inside its
    existing complete-payload family and therefore justifies the added object graph
    and possibly a new runtime boundary?

Until these are answered, the honest status is:

```text
R0_REFERENCE_ZERO_PAYLOAD_IO = REQUIRED_NOT_YET_PROVED
CAS_CDC_EPHCOW_ARCHITECTURE  = PROPOSED_NOT_SELECTED
CORRECTNESS_RESULT           = NOT_RUN
MATCHED_PERFORMANCE_EVIDENCE = OPEN
FINAL_PERFORMANCE_VERDICT    = TARGET_UNSELECTED
STAGE_4_6_COMPARATOR         = INCOMPARABLE
V2_PERFORMANCE_GUARANTEE     = NONE
```

## 11. Sources and evidence classification

### Current V2 design authority (authority links, not evidence labels)

- [Architecture decision](../architecture_design.md) — accepted Phase 01 output
- [LayerStack-0 Version-storage design](../design/03-state-store.md) — selected design contract
- [Performance and optimization](../design/07-performance-and-optimization.md) — selected evidence discipline
- [Phase 01 specification](../phases/01-choose-design/SPEC.md) — completed selection input

### External mechanism references

- [Linux `FICLONE`/`FICLONERANGE` manual](https://www.man7.org/linux/man-pages/man2/ioctl_ficlone.2.html) — file-level extent sharing and COW semantics; `SOURCE-VERIFIED`
- [Btrfs subvolume documentation](https://btrfs.readthedocs.io/en/latest/btrfs-subvolume.html) — snapshot root behavior, nested-subvolume qualification, and asynchronous deletion; `SOURCE-VERIFIED`
- [Btrfs design documentation](https://btrfs.readthedocs.io/en/stable/dev/dev-btrfs-design.html) — shared roots/extents and filesystem COW; `SOURCE-VERIFIED`
- [Linux OverlayFS documentation](https://docs.kernel.org/filesystems/overlayfs.html) — lower-to-upper `copy_up` behavior; `SOURCE-VERIFIED`

### Inferences and missing evidence

- Expected operation rankings are `INFERRED` from mechanism shape and must be tested.
- CAS+CDC changed-data-proportional checkpoint complexity is `INFERRED` and depends
  on complete mutation tracking and reusable canonical structures.
- No EphCoW scratch spike was needed to state the hypotheses. No code was written.
- No matched benchmark was run. Every quantitative performance result remains `OPEN`.
