# Stage 04.6 Ultra-Optimization Requirements and Prohibitions

Status: normative Stage 04.6 contract<br>
Scope: materialization, workspace activation, mutation capture, checkpoint
publication, rollback, squash, and their storage-service resource model<br>
Out of scope: Stage 5–7 implementation<br>
Ratified specification decisions: `SD-04.6-001` (closing portable canonical
checkpoint, 2026-07-27)

This document defines what an acceptable Stage 04.6 implementation must
achieve and what it must not do. It is intentionally independent of any single
implementation proposal. The selected architecture is
[`new_plan.md`](new_plan.md). `plan.md`, `review.md`,
`portable_split_cow.md`, and the design recommendation are historical inputs,
not authorities that can weaken this contract.

The words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, and **MAY** are
normative. A requirement may be changed only through an explicit specification
decision that records the reason, benchmark evidence, and affected acceptance
gates.

## 1. Priority and objective

The design priority is:

1. canonical filesystem correctness and checkpoint identity;
2. crash safety and bounded resource behavior;
3. portability across the required execution environments;
4. space proportional to unique payload and active changes;
5. maximum activation and publication performance; and
6. maintainability, modularity, and replaceable backend accelerators.

Stage 04.6 MUST optimize repeated workspace activation, fork, rollback, and
ordinary incremental publication by at least `100x` at the declared target
bound where a matched baseline exists. `500x` is the stretch objective.
Results that do not have a matched baseline MUST be labeled absolute targets,
not speedups.

The implementation MAY be a destructive redesign and MAY replace CAS, CDC,
carrier, index, or materialization components. It MUST preserve every
correctness, portability, resource, space, and backend-neutrality requirement
in this document.

## 2. Required portability

`PORT-001` The required architecture MUST be host-OS agnostic. The same
canonical storage and checkpoint model must work when the OCI runtime is
hosted on Linux, macOS, or Windows.

`PORT-002` The required OCI path MUST be container-image agnostic. It MUST NOT
require language runtimes, filesystem daemons, helper packages, or modified
libraries inside the user image.

`PORT-003` `CAP_SYS_ADMIN` is the maximum additional container privilege the
required path may assume.

`PORT-004` The required path MUST NOT depend on:

- reflink or a CoW host filesystem;
- FUSE;
- KVM;
- ublk, NBD, device mapper, or a custom block device;
- a custom kernel or kernel module;
- `tmpfs` for workspace payload;
- a host-specific snapshot API; or
- a package installed into the user image.

`PORT-005` Reflink, FUSE, Firecracker block snapshots, ublk, and similar
mechanisms MAY be optional accelerators. Disabling an accelerator MUST preserve
filesystem semantics, canonical identity, recovery behavior, and the required
portable path.

`PORT-006` OCI, Firecracker, and WASI representations MUST resolve to the same
backend-neutral `RootId`. Backend-specific mounts, carriers, images, block
maps, and VM snapshots are disposable caches and MUST NOT become checkpoint
identity.

## 3. Filesystem and identity invariants

`SEM-001` Publication MUST preserve the complete semantic oracle, including:

- file creation, replacement, overwrite, append, and truncate;
- file and directory deletion;
- rename within and across directories;
- whiteouts and opaque directories;
- file/directory/symlink type changes;
- hardlinks and symlinks;
- mode, ownership, timestamps, and supported xattrs; and
- sparse ranges and special metadata where the backend supports them.

`SEM-002` The canonical `RootId` MUST be derived from normalized content and
filesystem metadata. It MUST NOT depend on inode number, physical path, mount
identity, backend, host OS, carrier generation, pack location, or storage
locator.

`SEM-003` Every published root MUST be immutable. A root becomes visible only
after every reachable new payload range has a durable locator and all
canonical metadata has been durably committed.

`SEM-004` Root publication and ref update MUST be distinct. The final ref
update MUST use optimistic concurrency control and MUST NOT expose a partial
root.

`SEM-005` Rollback and logical squash MUST preserve canonical identity.
Squashing representation metadata MUST NOT silently change filesystem
semantics or attribution.

`SEM-006` `pip install`, `npm install`, builds, generated artifacts, and
ordinary edits MUST use the same generic mutation and publication pipeline.
The storage design MUST NOT infer semantic importance from a package manager,
lockfile, filename, directory, language, framework, or command name.

### 3.1 Ratified specification decision SD-04.6-001

**Status: RATIFIED — 2026-07-27.** This decision is normative and supersedes
any proposal or benchmark passage that treats a same-upper, non-closing
canonical checkpoint as a Stage 04.6 candidate acceptance requirement.

On the required portable path, publishing a new canonical root from an active
workspace is a **closing filesystem checkpoint**:

1. admission atomically fences every new command, execution, and mutation for
   the exact session epoch;
2. tracked active commands drain within the bounded pre-close interval, or
   publication returns `RejectedBeforeAdoption`/`WorkspaceBusy` with the
   session untouched;
3. the durable `Sealing` record makes the old session terminal and commits the
   same operation identity to forward-only recovery;
4. thereafter, every process that can hold the workspace mount namespace,
   writable file descriptor, mapping, or current working directory is stopped
   and reaped. Inability to prove quiescence MUST return durable
   `RecoveryRequired` and roll forward, never unfence or report a resumable
   pre-adoption rejection;
5. the upper is synchronized, unmounted, and made permanently unavailable to
   the old session;
6. ownership of the same upper allocation may then transfer from workspace
   ownership to immutable payload ownership;
7. durable payload locators and canonical metadata precede the final
   optimistic ref replacement; and
8. the final ref replacement remains the publication linearization point.

The published upper MUST NOT resume accepting mutation. If continuation is
requested, it MUST begin only after the ref commit in a successor session with
a fresh upper/work pair. Successor activation has its own readiness boundary.
Failure to activate that successor after ref commit MUST return a typed
“checkpoint committed; activation failed” outcome and MUST NOT roll back or
misreport the committed checkpoint.

`PublicationOperationId` and any requested `ActivationOperationId` MUST be
distinct. The activation identity and intent MUST be fixed and durable before
the ref commit. That commit creates an immutable `PublicationCommitted` fact;
successor activation is a separate idempotent operation whose result cannot
rewrite, repeat, or roll back publication. A combined response MAY project both
facts, including `CommittedActivationFailed`.

The benchmark-evidence record for this decision is explicit: the immutable
historical `baseline-experiment/baseline.json` measurements describe the old
implementation and do not qualify the closing contract; the non-closing
`I0`/`I2` campaigns, when run, remain compatibility evidence only. No
qualifying closing-`I3` performance, space, or fault campaign existed at
ratification, so that evidence is recorded as `PENDING` and all affected
release gates remain disabled.

On `I3` and every accepted production or public path, a live mutation receipt
or diagnostic observation MAY describe a still-active upper, but it is not a
canonical checkpoint and MUST NOT publish a new durable `RootId` or update a
canonical ref. Optional reflink, snapshot, FUSE, or range-CoW accelerators MAY
reduce internal work only while preserving the same closing external contract;
a separately named experimental live-snapshot capability is outside required
Stage 04.6 qualification.

The preserved 64- and 1,000-operation same-upper non-closing campaigns exercise
the retired behavior **only as pinned `I0`/`I2` compatibility controls and
physical evidence**. When that compatibility evidence is reported, the
campaign rows remain required and must be labeled honestly; running or
reporting them is not a prerequisite for `I3` release qualification. They MUST
NOT be used as an `I3` candidate pass/fail gate, pooled with closing
publication, labeled equivalent to `seal_publish`, or allowed to block release
qualification. The candidate publication boundary is closing seal-and-publish;
when continuation is requested, post-commit restart is separately measured.

This decision preserves `SEM-003`, `SPACE-006`, and `SPACE-007`: keeping the
only durable allocation writable would violate root immutability, while
creating an isolated copy or snapshot would introduce a forbidden dependency
or a second payload-sized publication term.

## 4. Multiagent, rollout, and workspace requirements

`MULTI-001` Multiagent support means that independent external clients create
and operate workspace sessions through CLI or MCP requests. Agents are not
assumed to run inside the sandbox.

`MULTI-002` Logical rollout-node creation MUST be metadata-only until a
workspace is activated. A clean logical child MUST NOT allocate a native
checkout, carrier, private upper, or repository-sized payload.

`MULTI-003` At least 16 simultaneously active sibling workspace sessions MUST
share one immutable lower representation while retaining isolated private
changes.

`MULTI-004` Creating 1,000 clean inactive forks MUST allocate zero
repository-sized native payload and only `O(1)` durable metadata per fork.

`MULTI-005` Active physical workspace storage MUST scale with actual private
changes, not with the number of external clients or logical MCTS nodes.

`MULTI-006` Parallel rollouts MUST publish independent immutable roots.
One rollout MUST NOT mutate another rollout's lower, upper, ref, or
operation-owned staging.

`MULTI-007` A winning root MUST be activatable on another qualified backend.
Losing runtime state may be discarded without deleting canonical shared
payload.

`MULTI-008` A long-running `exec_command` belongs to the execution/workspace
resource ledger. It MUST NOT retain a heavy-storage-job coordinator or data
worker merely because the command continues to run.

## 5. Complexity notation

All performance and space claims MUST use the following terms:

| Symbol | Meaning |
| --- | --- |
| `B` | logical payload bytes reachable from the complete root |
| `F` | paths/inodes reachable from the complete root |
| `R` | immutable roots, refs, checkpoints, and logical rollout nodes |
| `A` | activated workspace sessions |
| `DeltaP` | normalized changed-path operations in one checkpoint |
| `DeltaB` | genuinely new durable payload after reuse and deduplication |
| `H` | physical payload bytes allocated in the private upper |
| `H_scan` | upper bytes without valid pre-sealing or dirty-range evidence |
| `S_f` | size of a lower file receiving its first portable write |
| `K` | total chunks or payload extents |
| `K_delta` | chunks or extents affected by one checkpoint |
| `d` | persistent path/Merkle index depth, normally `O(log F)` |
| `X` | bytes requested by a read |

`H` and `DeltaB` MUST be reported separately. On the required portable path, a
one-byte first write to a `1 GiB` lower file may create approximately `1 GiB`
of upper payload because OverlayFS copy-up is `Theta(S_f)`, even when later CDC
finds very little new durable content.

## 6. Required time complexity

| Operation | REQUIRED total-work complexity | MUST NOT perform |
| --- | --- | --- |
| create logical fork | `O(log R)` metadata; `O(1)` payload | `Theta(B)` copy or `Theta(F)` traversal |
| activate existing exact carrier | `O(1)` in `B` and `F` | complete materialization or root traversal |
| activate private upper | `O(1)` in `B` and `F` | eager lower copy |
| rollback to existing root | `O(log R)` metadata | root reconstruction |
| logical squash | independent of `B` and `F` | payload copy, CDC, or root traversal |
| read `X` unchanged bytes | `Theta(X)` plus touched-extent lookup | unrelated payload scan/materialization |
| write file already in upper | `Theta(bytes written)` | complete-root work |
| first portable write to lower file | worst case `Theta(S_f)` | claim `Theta(edit size)` without a qualified range-CoW accelerator |
| first CAS/CDC ingestion | `Theta(B + F)` | claim sublinear first ingestion |
| first cold carrier construction | `Theta(B + F)` | include it in warm activation timing |
| incremental checkpoint | `O(H_scan + DeltaP * d + K_delta)` | ordinary `Theta(B + F)` scan/reconstruction |
| finalization after valid pre-sealing | `O(DeltaP * d + K_delta)` | claim pre-sealing work was eliminated |
| genuinely create `DeltaP` small files | at least `Theta(DeltaP + DeltaB)` | constant-time or universal 500x claim |
| dedup lookup | expected `O(1)` or `O(log K)` per lookup | linear scan of stored chunks |

`TIME-001` These are total CPU and IO bounds, not merely user-visible
blocking. Pre-sealing MAY move `H_scan` before the final checkpoint boundary,
but benchmarks MUST include that work in total publication work.

`TIME-002` Ordinary incremental checkpoint work MUST NOT become proportional
to `B` or `F` when `H_scan`, `DeltaP`, and `K_delta` remain fixed.

`TIME-003` A first portable write to a lower file MAY remain
`Theta(S_f)`. That limitation MUST be measured and reported, not hidden behind
later CDC reuse or publication timing.

## 7. Quantitative performance gates

The preserved `870.08 MiB` baseline is:

| Operation | Recorded baseline |
| --- | ---: |
| first publication / CDC / CAS ingestion | `107.024 s`, `8.13 MiB/s` |
| cold complete native materialization | `9.988 s`, `87.12 MiB/s` |
| explicit same-key materializer call | `6.362 s` |
| ordinary warm generation lookup | `0.035375 ms` |
| logical squash | approximately `1–6 ms` |

Acceptance targets:

| Operation | REQUIRED acceptance target | Stretch target |
| --- | ---: | ---: |
| activate stored `870 MiB` root from existing carrier | `≤100 ms` p95 | `≤20 ms` p95 |
| explicit same-key usable session | `≤50 ms` p95 | `≤20 ms` p95 |
| activate forked workspace from existing carrier | `≤10 ms` p95 | `≤2 ms` p95 |
| rollback to existing carrier | `≤50 ms` p95 | `≤10 ms` p95 |
| logical squash | `≤10 ms` p95 | preserve measured `1–6 ms` |
| publish approximately `1 MiB` across 10 ordinary files | `≤100 ms` p95 | `≤20 ms` p95 |
| large-input CAS/CDC streaming | `≥1 GiB/s` | `≥5 GiB/s` |
| scan/hash changed `1 GiB` file without dirty ranges | `≤1.0 s` | `≤0.2 s` |

`PERF-001` A `100x` result is REQUIRED for stored-carrier activation against
the preserved cold-materialization baseline. The `500x` result is a stretch
target and MUST be reported honestly whether achieved or missed.

`PERF-002` Sustained command and ordinary filesystem throughput MUST regress
by no more than `5%` unless a separately approved exception names the workload
and reason.

`PERF-003` Enforcing the lean memory profile MUST regress normal
materialization and publication throughput by no more than `5%` compared with
the fastest qualified bounded-memory configuration.

`PERF-004` A cold complete-read/materialization regression of up to `48%` is an
accepted exception only when hot-path targets, correctness, and space gates
pass and no obvious defect remains.

`PERF-005` The `100–500x` objective applies to repeated activation, fork,
rollback, and ordinary incremental publication that avoid complete-root work.
It MUST NOT be applied to first ingestion, first cold carrier construction,
genuine creation of hundreds of thousands of files, or first portable copy-up
of a large lower file.

## 8. Required persistent-space complexity

Physical storage MUST be accounted as:

```text
T_physical(t) =
    P_unique(t)
  + C_cache_only(t)
  + sum(H_active_private[i], t)
  + P_bounded_staging(t)
  + M_metadata(t)
```

Where:

- `P_unique` counts the physical union of canonical CAS and promoted payload
  once;
- `C_cache_only` is bounded reconstructible carrier content not already
  counted in `P_unique`;
- `H_active_private` is actual active private-upper payload;
- `P_bounded_staging` is bounded metadata staging and streaming scratch; and
- `M_metadata` is manifest, index, journal, root, lease, and locator metadata.

The required asymptotic bound is:

```text
T_physical =
    O(P_unique + sum(H_active_private[i]) + C_cache_only + M_metadata)
```

`SPACE-001` Physical payload MUST NOT contain a `Theta(A * B)` term. An
inactive fork adds no payload. A clean active workspace shares the immutable
lower. A changed active workspace adds its actual upper `H_i`.

`SPACE-002` Multiple roots, carrier entries, and CAS locators referencing the
same physical inode or range MUST count those payload bytes once.

`SPACE-003` The main payload and delta representation MUST NOT be materially
inflated to gain speed. Bounded metadata MAY be traded for time only when its
size and performance benefit are measured.

`SPACE-004` Carrier caches MUST declare and enforce byte, inode, generation,
and physical-depth quotas.

`SPACE-005` Stage 04.6 MUST NOT acquire undeclared root-retirement, deletion,
retention, or general GC authority. It may remove only exact
operation-owned private or staging state under a proven ownership record.

## 9. Promotion-first publication space

For upper payload `H`, required optimized publication peak is:

```text
P_publish_peak(H) =
    H_promoted_once
  + M_publish
  + B_streaming_scratch
  = H + O(M)
```

`SPACE-006` Ownership promotion or adoption MUST count changed payload once.
The optimized path MUST NOT produce:

```text
H_private_upper + H_complete_CAS_copy + O(M)
```

`SPACE-007` No copy-based or reconstruction-based fallback that introduces a
second payload-sized term may be used to pass the optimized publication gate.

`SPACE-008` Publication staging may scale with changed metadata:

```text
P_bounded_staging =
    O(DeltaP records + bounded merge pages)

queued_payload_bytes = 0
B_streaming_scratch <= 3 MiB application-wide
```

It MUST NOT contain another complete `H`, one loose temporary object per
payload chunk, or an unbounded descriptor, FD, task, mount, or payload queue.

## 10. Metadata-space requirements

Metadata may have the structural complexity:

```text
M_metadata =
    O(total_encoded_path_bytes + F + K + R + DeltaP_journal)
```

It MUST NOT contain a second payload-sized term.

| Metadata category | REQUIRED target |
| --- | ---: |
| fixed path/index metadata | `≤256 bytes/path`, excluding encoded pathname and xattrs |
| chunk or extent descriptor | `≤96 bytes/chunk` |
| root, ref, or logical-fork record | `≤1 KiB/root` |
| fixed change-journal record | `≤256 bytes/change`, excluding encoded paths |
| payload-dominated corpus metadata | `≤2%` of unique payload |
| application-resident index window | `≤2 MiB` |

`META-001` Empty-file and tiny-file repositories MUST be evaluated using
encoded path bytes, fixed bytes per path, bytes per root/chunk, total metadata,
backing-object count, and inode count. A payload percentage alone is invalid
when payload is near zero.

`META-002` Variable pathnames, xattrs, and user metadata MUST be charged at
their actual encoded size and MUST NOT be hidden in fixed-record figures.

`META-003` Small payload and metadata records SHOULD be packed or inlined.
The design MUST NOT create one loose backing object per small file, record, or
chunk when a bounded packed representation can preserve semantics.

## 11. Memory requirements

The design is disk-backed and memory-bounded, not memory-resident:

```text
M_application = O(1) with respect to B, F, H, K, R, and A
M_application <= 8 MiB
```

Required resource profile:

| Resource | REQUIRED bound |
| --- | ---: |
| storage data workers | 4 |
| admitted heavy-storage-job coordinators | 16 |
| pending heavy-storage-job queue | 16 descriptors; `≤64 KiB` encoded metadata |
| non-resident IO byte credits | `64 MiB` |
| total application-owned resident storage working set | `≤8 MiB` |
| resident index window, included in total | `≤2 MiB` |
| four worker buffers, included in total | `≤256 KiB` each; `≤1 MiB` total |
| coordinator and pending-queue state, included in total | `≤1 MiB` |
| CDC/hash/encoding/merge scratch, included in total | `≤3 MiB` |
| allocator/accounting/emergency headroom, included in total | `≤1 MiB` |
| queued payload | 0 bytes |
| storage-service RSS | `≤min(96 MiB, paired idle RSS + 32 MiB)` |
| aggregate memory-domain soft watermark | `≤96 MiB` |
| aggregate memory-domain hard ceiling | `≤128 MiB` |

`MEM-001` The `8 MiB` figure is one non-double-counted global resident permit
domain. Subcategories are partitions, not additional allowances.

`MEM-002` The `64 MiB` IO-credit window describes borrowed or streamed disk
ranges. It MUST NOT authorize an equivalent resident allocation.

`MEM-003` The service MUST acquire resident permits before allocation and use
fallible reservation. Permit exhaustion MUST produce typed retryable
backpressure before OOM.

`MEM-004` The aggregate memory domain includes service RSS, resident mappings,
attributable page cache, dentries, inodes, filesystem slab, and storage helper
processes.

`MEM-005` At the soft watermark, the service MUST stop optional prefetch,
release one-pass mappings/cache where supported, and reduce admission. It MUST
reject new heavy work before the hard ceiling can trigger an OOM kill.

`MEM-006` The required implementation MUST NOT allocate:

- a repository-sized checkout or index in memory;
- a resident path or chunk record for the complete repository;
- a file-sized application mapping;
- a flat in-memory path/chunk vector;
- an unbounded task, descriptor, or payload queue; or
- a `tmpfs` workspace payload.

`MEM-007` The service MUST NOT use `read_to_end` or equivalent unbounded reads
for repository payload.

## 12. Concurrency and overload policy

`LOAD-001` Four shared storage workers perform bounded hydration, hash, CDC,
encoding, merge, and publication data work.

`LOAD-002` Up to 16 lightweight coordinators may own bounded heavy-job state.
Up to 16 additional admissions may wait as descriptors without payload,
mounts, private uppers, or repository-sized metadata.

`LOAD-003` Additional heavy jobs MUST receive deterministic typed retryable
backpressure. High load increases waiting/retry latency, not resident memory.

`LOAD-004` Lightweight status and control-plane operations MUST use a
separately bounded path and MUST NOT queue behind bulk hydration/publication.

`LOAD-005` Scheduling MUST be fair enough to prevent starvation. Cancellation
MUST join workers and release buffers, permits, leases, FDs, mounts,
coordinator slots, queue descriptors, and operation-owned staging.

`LOAD-006` Overload MUST NOT cause OOM, unbounded filesystem cache growth,
unbounded mounts/FDs, silent request loss, or partial checkpoint publication.

## 13. Failure, cancellation, and recovery

`FAIL-001` Carrier lifecycle MUST have explicit durable states equivalent to:

```text
Building -> Ready -> Published -> Terminal
```

`FAIL-002` Promotion ownership MUST have explicit durable states equivalent to:

```text
WorkspaceOwned -> Sealing -> PayloadOwned -> LocatorReady -> PublicationCommitted
```

`FAIL-003` Recovery MUST resume or roll forward from the last durable ownership
state. It MUST NOT guess whether an inode, upper, range, locator, or staging
object is safe to discard.

`FAIL-004` A sole durable locator MUST remain pinned until an alternative
durable locator exists and all dependent leases have drained.

`FAIL-005` Carrier registration, locator installation, root publication, and
ref update MUST be idempotent.

`FAIL-006` Large traversal, hashing, hydration, and IO MUST occur outside the
root/ref writer lock.

`FAIL-007` Ambiguous publication state MUST fail closed. Cancellation or crash
MUST NOT produce a visible partial root or backend-specific identity.

## 14. Benchmark and evidence policy

The preserved
[`baseline-experiment/README.md`](baseline-experiment/README.md) protocol is
the matched baseline authority.

Under ratified `SD-04.6-001`, candidate canonical-publication measurements use
the closing seal-and-publish boundary. Any requested successor restart is a
separate post-commit operation and combined outer measurement. Any non-closing
same-upper rows in the preserved protocol are `I0`/`I2` compatibility controls
only; they are not candidate acceptance gates or candidate speedup
denominators.

Every qualified run MUST record:

- `B`, `F`, `R`, `A`, `DeltaP`, `DeltaB`, `H`, `H_scan`, `K`, `K_delta`,
  and index depth `d`;
- cache state and exact timing boundaries;
- p50, p95, p99, elapsed time, CPU time, and sustained throughput;
- logical, allocated, unique, shared, staging, and unexplained bytes;
- bytes read, scanned, hashed, written, reused, and transferred;
- fixed and variable metadata per path, chunk, root, and journal record;
- RSS, paired idle RSS, aggregate memory-domain peak, and settled memory;
- page cache and kernel metadata where observable;
- workers, coordinators, queues, permits, FDs, mounts, leases, and inodes;
- exact publication/ref-operation and activation identities, their separate
  durable outcomes, the composed response, attempt/success/failure counts,
  success rate, retry count, and ref-update count;
- first mount-ready, first access, first write/copy-up, checkpoint,
  durable-publication, and deferred-work durations; and
- cancellation/recovery residue and final quiescence.

Latency percentiles over successful activations MAY be reported as diagnostics,
but failures MUST NOT disappear from qualification. Any activation failure
fails a success-required activation or combined-lifecycle cell; publication
remains a successful publication sample when its exact
`PublicationCommitted` fact is durable.

The following work-amplification ratios MUST be reported:

```text
scan_amplification =
    bytes_scanned / max(H_scan, 1)

path_amplification =
    paths_visited / max(DeltaP, 1)

publication_payload_amplification =
    peak_payload_bytes / max(H, 1)
```

Required benchmark workloads include:

- preserved `870.08 MiB` baseline corpus;
- `1 GiB` file: unchanged, append, truncate, and one-byte writes at
  start/middle/end;
- mixed large-file repository;
- 100k and 1M small-file repositories;
- offline fake `pip install` and `npm install`;
- directory rename, delete, opaque, whiteout, type-change, link, and metadata
  operations;
- 16 active sibling workspaces;
- 1,000 inactive clean forks;
- deep checkpoint history, rollback, and logical squash;
- small and large upper promotion;
- cancellation/crash injection at every ownership and visibility boundary;
- memory-profile sweeps under 1, 4, 16, queued, and rejected heavy jobs; and
- canonical-root equivalence across OCI, Firecracker, and WASI adapters.

`BENCH-001` Network time MUST be excluded from package-installation benchmarks.
Use generated archives or local caches.

`BENCH-002` Publication throughput MUST NOT be labeled materialization
throughput. Warm metadata lookup MUST NOT be labeled usable workspace
activation.

`BENCH-003` User-visible blocking and actual total work MUST be reported
separately. Work moved into pre-sealing is not work eliminated.

`BENCH-004` Every ratio MUST name its matched implementation, corpus, hardware,
cache state, concurrency, timing boundary, and sample count.

## 15. Explicit prohibitions

An accepted Stage 04.6 implementation MUST NOT:

1. require reflink, FUSE, KVM, ublk, a custom kernel, or host-specific storage;
2. require changes or packages inside the user container image;
3. use memory-backed workspace payload or repository-sized resident state;
4. eagerly materialize logical forks;
5. create one complete workspace copy per active session;
6. reconstruct or scan the complete repository for ordinary warm activation;
7. scan `B` or `F` for an ordinary checkpoint whose change terms remain fixed;
8. retain both a complete changed upper and a second complete CAS payload copy
   during optimized publication;
9. hide copy-based publication in a fallback or temporary space term;
10. treat an inode, mount, carrier, pack, VM snapshot, or block map as
    canonical identity;
11. infer optimization behavior from lockfiles, filenames, directories,
    package managers, languages, or commands;
12. queue payload bytes or allocate unbounded tasks, buffers, descriptors,
    mounts, FDs, paths, chunks, or operations;
13. use OOM or process termination as normal overload control;
14. expose partial roots or guess storage ownership during recovery;
15. acquire undeclared GC, root-retirement, or published-payload deletion
    authority;
16. inflate primary payload or delta size materially to improve latency;
17. claim `100x`, `500x`, or `5 GiB/s` without matched measurements;
18. combine speedups from unrelated operations by multiplying their ratios;
19. report deferred, asynchronous, or pre-sealing work as eliminated;
20. weaken a hard gate silently because a benchmark fails; or
21. publish a new canonical root while the old workspace or published upper
    continues accepting mutation.

## 16. Permitted architectural freedom

Subject to every requirement above, an implementation MAY:

- replace CAS/CDC, indexing, carrier, publication, or storage internals;
- introduce a new backend-neutral storage representation;
- spend bounded metadata for lower latency;
- batch, pack, inline, stream, pre-seal, and adopt stable ranges;
- use optional reflink, FUSE, VM, or block accelerators;
- change internal module boundaries and algorithms;
- retain reconstructible bounded carrier caches; and
- reject excess work through typed retryable admission control.

No current component is protected merely because it already exists. The
contract protects semantics, identity, portability, bounded resources,
space/time complexity, and measured results.

## 17. Acceptance checklist

Stage 04.6 is complete only when:

1. all semantic-oracle and canonical-identity tests pass;
2. required OCI operation needs no forbidden accelerator or image package;
3. stored-carrier activation meets the `100x` p95 target;
4. the `500x` stretch result is reported honestly;
5. ordinary incremental work satisfies
   `O(H_scan + DeltaP * d + K_delta)`;
6. publication peak satisfies `H + O(M)` with no second payload copy;
7. active storage has no `Theta(A * B)` payload term;
8. inactive forks add no payload;
9. fixed metadata and memory ceilings pass;
10. normal throughput regression remains within `5%`;
11. overload returns bounded retryable backpressure before OOM;
12. crash/cancellation tests leave no ambiguous ownership or partial root;
13. OCI, Firecracker, and WASI produce the same canonical `RootId`;
14. large-file copy-up and many-small-file lower bounds are reported honestly;
15. every claimed speedup has a matched baseline;
16. no forbidden action in Section 15 occurs; and
17. every candidate canonical checkpoint follows the ratified closing
    seal-and-publish boundary, any requested restart is a separately identified
    post-commit operation, and non-closing same-upper campaigns remain unpooled
    `I0`/`I2` controls only.
