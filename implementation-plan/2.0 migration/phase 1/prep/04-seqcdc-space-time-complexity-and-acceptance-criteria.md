# SeqCDC space/time complexity and acceptance criteria

> Quantitative acceptance contract for the gated SeqCDC implementation chosen
> by the
> [SeqCDC/CAS and squash decision](03-seqcdc-cas-and-squash-decision.md).
> This document specializes the broader
> [Phase 1 storage specification](01-cdc-cas-space-time-materialization-spec.md).
> When two quantitative requirements differ, the stricter requirement governs.
> The decision record's identity-preserving squash protocol explicitly
> supersedes the new-logical-root wording in specification §2.4.

| Field | Requirement |
| --- | --- |
| Status | Proposed hard gate for implementation and production enablement |
| Candidate | Internal scalar author-semantic SeqCDC |
| Comparator | Internal synchronous StreamCDC at equal effective chunk distribution |
| Baseline | Current raw LayerStack on identical hardware and filesystem |
| Normative performance environment | Pinned Ubuntu 24.04 Docker image |
| Portability qualification | Frozen supported-host release matrix plus versioned Linux-image capability profile |
| Dependency budget | Exact zero external dependency delta from the frozen product baseline |
| Per candidate/baseline pair | At most five minutes, including setup and settled measurement |
| Correctness policy | No performance or space result can compensate for a correctness failure |

## 1. Purpose and pass semantics

This document states what the selected SeqCDC/CAS implementation is expected
to cost and the measurements it must pass. It covers:

- the SeqCDC boundary loop and streaming adapter;
- checkpoint publication;
- warm and cold native materialization;
- normal native execution;
- identity-preserving squash and remount;
- carrier evacuation, pack compaction, retention, and GC;
- peak and settled physical storage;
- bounded application memory;
- process-resource reclamation and long-lived memory stability;
- a zero-new-external-dependency implementation; and
- Docker-host and Linux-image portability.

Three kinds of number appear:

| Kind | Meaning |
| --- | --- |
| Correctness invariant | Any violation rejects the candidate immediately |
| Target | Expected healthy operating result |
| Hard failure | Production enablement is blocked; only an explicitly algorithm-specific failure triggers StreamCDC fallback |

An outcome between a space target and its hard ceiling requires an explicit
exception plus evidence that the StreamCDC comparator cannot meet the target
without violating a higher-priority correctness or time requirement.

There is no trustworthy absolute latency baseline yet. Relative gates are
evaluated only after freezing the raw LayerStack baseline on the same host,
filesystem, Docker environment, cache state, and corpus.

## 2. Fixed SeqCDC profile

| Parameter | Fixed value |
| --- | ---: |
| Algorithm ID | `seqcdc-scalar-author-v1` |
| Mode | Increasing |
| Minimum chunk | 8,192 bytes |
| Target effective average | 16,384 bytes |
| Maximum chunk/window | 32,768 bytes |
| Consecutive-sequence threshold | 5 |
| Opposing-slope trigger | 50 |
| Jump | 512 bytes |
| Digest | Domain-separated typed SHA-256 |
| Stream representation | One 32 KiB circular window; at most two borrowed slices |

The average is an empirical target, not an input used by the authors' cut
loop. Each root records the exact algorithm and parameters. Any profile change
creates a new format version and never changes an existing root.

For non-empty input of size `U`, the chunk count `K` is bounded approximately
by:

```text
ceil(U / 32 KiB) ≤ K ≤ ceil(U / 8 KiB)
```

The final chunk may be shorter than 8 KiB. A complete file shorter than 8 KiB
is one actual-length chunk, not an 8 KiB padded allocation.

## 3. Complexity notation

| Symbol | Meaning |
| --- | --- |
| `U` | Bytes in the captured unpublished upper being published |
| `E` | Filesystem entries processed by the operation |
| `K` | Chunks generated or consumed |
| `F` | Size of one file visible in the private upper |
| `R` | Bytes missing from a requested native materialization |
| `D` | Native lower-carrier depth |
| `Q` | Changed paths or ranges used by OCC, diff, or blame |
| `N` | Entries in the relevant disk-backed index |
| `S` | Bytes in the carrier interval selected for squash |
| `E_s` | Entries in the carrier interval selected for squash |
| `G` | Objects or bytes admitted to one bounded maintenance slice |
| `B` | Configured storage-owned memory budget |
| `C_capture` | Allocated payload bytes of one immutable captured upper |
| `C_current` | Allocated bytes of one correct current native materialization |
| `C_target` | Allocated bytes of one complete hydration or squash target carrier |
| `H_unique` | Unique retained history absent from `C_current` |

All complexity claims assume format-bounded locator probes and bounded
disk-backed cursors. They do not assume that the complete index, tree,
history, or chunk list is resident in memory.

## 4. Expected time complexity

### 4.1 SeqCDC boundary selection

The scan position only advances. A jump advances it farther; it does not cause
already consumed input to be rescanned.

| Work | Expected/worst time |
| --- | --- |
| Read input | `O(U)` |
| SeqCDC boundary scan | `O(U)` worst case |
| SHA-256 over emitted chunks | `O(U)` |
| Emit `K` descriptors | `O(K)` |
| Combined content path | `O(U + K)`, therefore `O(U)` because `K = O(U)` |

SeqCDC's jumps may reduce the number of byte comparisons on some inputs, but
the production contract assumes linear time. It does not assume the paper's
raw throughput will reproduce in LayerStack.

### 4.2 Publication

| Publication component | Expected/worst time |
| --- | --- |
| Walk captured upper | `O(E)` |
| Read and hash payload | `O(U)` |
| Chunk and emit descriptors | `O(U + K)` |
| Canonical path ordering | Bounded external ordering; up to `O(E log E)` comparison/I/O work when input is not already canonical |
| Format-bounded locator/catalog probes | `O(K)` under fixed on-disk fan-out and page limits |
| Journal, fsync, and root OCC | Bounded fixed transactions plus bytes made durable |

The normal publication expression is:

```text
O(U + E + K)
```

plus bounded external-sort work when canonical input order is unavailable.
Application memory remains `O(B)`.

A one-byte edit to a lower-only file of size `F` may still require `O(F)` read
time because OverlayFS can copy up and expose the complete resulting file.
CDC is expected to reduce new retained history, not make the publication scan
proportional only to the edit.

### 4.3 Materialization and execution

| Operation | Expected/worst time | Payload dependence |
| --- | --- | --- |
| Clean session creation | `O(D)` path/lease resolution and mount | Independent of workspace bytes |
| Warm root materialization | `O(D)`, with `D ≤ 64` | Reads no CAS payload |
| OverlayFS mount | `O(D)` plus kernel mount work | Reads no CAS payload |
| Cold hydration | `O(R + E)` sequential reconstruction and verification | Linear in bytes and entries missing from native storage |
| Cold activation | `O(R + E + D)` | Hydrate, then use the warm path |
| Native command/file/PTY operation | Existing native cost | No CDC, manifest, pack, or CAS lookup |
| Old-root activation | Warm `O(D)` when native; cold `O(R + E + D)` otherwise | Determined by locator availability |

Neither warm nor cold activation runs SeqCDC. Chunk boundaries are already
recorded in the immutable manifest. SeqCDC affects activation only indirectly
through chunk count, reuse, metadata volume, and pack locality.

Warm activation must never become proportional to logical workspace size.
Cold hydration must never have superlinear byte or entry cost.

### 4.4 Squash and maintenance

| Operation | Expected/worst time |
| --- | --- |
| Squash plan | Bounded catalog/lease work plus selected-carrier metadata |
| Squash build and verify | `O(S + E_s)` plus bounded external ordering |
| Squash commit | Short materialization-generation CAS and fsync |
| Live-remount frozen interval | `O(D + tasks + verified FDs)`; no `U`, `R`, `K`, or `S` work |
| Carrier evacuation | Linear in historical bytes whose last locator must move |
| Pack compaction/GC | `O(G)` per resumable slice |
| Root diff/OCC/blame query | `O(Q log N)` plus bounded result output |
| Crash recovery | Linear in pending journals and bounded cursor work, never all history |

Squash may hardlink exact immutable winners and therefore avoid copying their
payload on the same filesystem. It must not rechunk data. Its build occurs
outside the remount frozen interval. A hardlinked target inode must never be
mutated to normalize mode, ownership, xattrs, or timestamps; differing metadata
requires a fresh inode.

## 5. Time and throughput gates

For latency:

```text
allowed(baseline, percent, floor)
    = baseline × (1 + percent) + floor
```

The additive floor prevents sub-millisecond noise from producing a false
failure.

| Operation | Required SeqCDC/CAS result |
| --- | --- |
| Warm root resolve and session preparation | p50 and p95 `≤ baseline + 5% + 2 ms`; zero CAS payload reads |
| OverlayFS mount | p50 and p95 `≤ baseline + 5% + 2 ms` |
| Squash live-remount frozen interval | p50 and p95 `≤ baseline + 5% + 2 ms` |
| Full squash plan/build/commit | p50 and p95 `≤ baseline + 10% + 5 ms` |
| No-op `exec_command` | p50 and p95 `≤ baseline + 3% + 0.5 ms` |
| Native command throughput | At least 97% of raw LayerStack baseline |
| PTY create | p50 and p95 `≤ baseline + 3% + 1 ms` |
| PTY drain, supported `write_stdin`, and control-C/control-D cancellation | p50 and p95 `≤ baseline + 3% + 0.5 ms` |
| PTY resize, arbitrary signal, and literal EOF | Preserve the current deterministic unsupported response; do not score these as implemented operations |
| Native sequential file read/write | At least 97% of baseline throughput |
| Concurrent disjoint publication | At least 90% of baseline throughput while preserving OCC |
| Small-edit publish | p95 `≤ baseline + 15% + 5 ms`; report bytes scanned and newly retained |
| Cold hydration | Verified payload throughput at least 70% of same-filesystem native sequential copy |
| Cold activation end to end | p95 `≤ 1.5 ×` verified native-copy control plus the warm-mount allowance |
| SeqCDC selection advantage | At least 10% repeatable integrated publication improvement over internal StreamCDC at equal effective chunk distribution |

The hard latency gates use p50 and p95. Report p99 when at least 100 samples
exist, plus median absolute deviation, sample count, operations per second, and
bytes processed.

The selection-advantage gate is computed from end-to-end publication elapsed
time, including capture scan, chunking, hashing, manifest/index work, durable
writes, fsync, and root commit:

```text
for each matched (workload, seed, repetition, sample_index):
    seq_ratio_sample    = seqcdc_elapsed / seq_paired_raw_elapsed
    stream_ratio_sample = streamcdc_elapsed / stream_paired_raw_elapsed
    advantage_sample    = 1 - seq_ratio_sample / stream_ratio_sample

advantage = median(advantage_sample)
```

It passes only when:

- the large-source localized-edit and mixed-tree publication workloads each
  have `advantage ≥ 0.10`;
- no-dedup and many-small-file publication do not regress by more than 3%;
- three fresh, matched candidate/baseline-pair invocations independently meet
  those conditions;
- each workload contributes at least five interleaved samples per invocation;
- raw and candidate order is counterbalanced across repetitions; and
- a paired bootstrap over matched normalized samples has a 95% lower
  confidence bound of at least `0.10` for each workload claiming the selection
  advantage.

The profile is "equal effective distribution" only when both chunkers use the
same 8 KiB minimum and 32 KiB maximum, their measured means differ by at most
5%, and their p10, p50, and p90 chunk sizes differ by at most 10% on the same
bytes. If StreamCDC cannot be configured to match this envelope, report the
comparison as invalid rather than retuning SeqCDC or claiming the selection
advantage.

The candidate fails if:

- warm latency grows with workspace bytes;
- a warm path reads payload from CAS;
- mount/remount has a depth slope more than 10% worse than raw LayerStack;
- a background packer, squash builder, or GC slice enters a command/PTY
  critical path;
- cold hydration is superlinear;
- equivalent settled cycles show monotonically worsening latency; or
- one operation exceeds 60 seconds.

## 6. Application-memory complexity and limits

The required application-memory complexity is:

```text
O(B)
```

`B` is a configured constant independent of file size, logical workspace
bytes, entry count, chunk count, number of roots, and history depth.

| Resource | Hard configured limit |
| --- | ---: |
| SeqCDC maximum window | 32 KiB |
| Per publication worker chunk ring | 32 KiB |
| Per worker pack-read buffer | 256 KiB |
| Per worker hydration-output buffer | 256 KiB |
| Storage data-plane/background workers | 4 globally |
| In-flight payload chunks | One borrowed ring-backed chunk per publication worker; at most 4 globally |
| Downstream payload bytes | 0 |
| Downstream metadata queue | 16 descriptors and at most 64 KiB serialized metadata |
| External merge fan-in | 8 runs |
| External merge reader buffer | 64 KiB per run |
| Manifest/journal encoding | At most 256 KiB per admitted operation |
| Shared index cache | 4,096 × 4 KiB pages = 16 MiB |
| Managed memory per publication | At most 4 MiB, excluding shared index cache |
| Global storage-owned byte semaphore | 64 MiB |
| Native lower depth | 64 |
| Qualification RSS | At most 384 MiB absolute and at most 128 MiB above idle raw baseline |

All buffers, queues, manifests, journal encoders, sort readers, page caches,
and worker-local state are charged to explicit permits. Allocator behavior or
eventual garbage collection is not a memory-control mechanism.

When a worker, byte, queue, descriptor, page, or depth limit is reached:

1. apply bounded backpressure;
2. wait only until the operation deadline;
3. return `ResourceExhausted` if admission remains unavailable;
4. expose no new root or carrier; and
5. leave only transaction-owned, journaled cleanup state.

Qualification must include at least 64 MiB, 256 MiB, and 1 GiB inputs and
histories of 1, 16, and 64 roots with a cold page cache. For three repetitions
at each point, subtract the paired idle raw-baseline RSS and compare medians:

- adjusted final RSS and adjusted peak RSS must each vary by at most 16 MiB
  across the full size series; and
- no 4-times increase in input bytes or retained-root count may add more than
  8 MiB to either adjusted median.

The absolute and above-baseline RSS ceilings still apply at every point.
Collecting chunks, retaining borrowed slices, reading a whole large file,
building a whole-tree map, or rebuilding a history-sized index in memory is a
hard failure even when allocator reuse later hides the growth.

### 6.1 Reclamation and long-lived-process stability

The implementation must inventory every buffer, queue, cache, registry,
permit, worker/task, thread, file descriptor, mmap, and strong/weak shared
reference with its owner, hard bound, and normal, error, cancellation, panic,
shutdown, and restart release behavior. Strong ownership cycles, detached
workers, unbounded terminal registries, and cleanup that depends on process
exit are hard failures.

Run repeated publish, materialize, squash, GC, cancellation, timeout, and
injected-failure cycles in one long-lived process. After explicit cleanup,
bounded polling must observe product-defined quiescence: in-flight work is
zero, permits are returned, queues drain to their warmed-idle bounds, workers
are joined or return to their bounded pool, and terminal transaction state is
removed or durably handed to bounded recovery.

Report logical release separately from physical-memory stability. At each
settled sample collect process RSS, cgroup memory when available, live
storage-owned bytes, queue depths, permits, worker/task counts, open file
descriptors, and mappings. The first-to-last adjusted settled RSS delta and a
robust settled-RSS slope must remain inside the frozen raw-control noise band
and the existing 16 MiB flatness tolerance, while every absolute and
above-baseline cap continues to pass. Do not restart the process, call
`malloc_trim`, replace the allocator, purge page cache manually, or use an
arbitrary sleep to manufacture a pass. Rust's lack of tracing garbage
collection is not evidence of reclamation.

## 7. Physical-space model

Measure allocated physical bytes, never only logical or apparent length:

```text
T(t) =
    L_hot(t)
  + H_cold(t)
  + sum(U_active(t))
  + P_staging(t)
  + M(t)
```

Where:

- `L_hot` is every allocated native immutable carrier;
- `H_cold` is every pack plus its slack;
- `U_active` is every active private upper;
- `P_staging` is publication, hydration, squash, compaction, and recovery
  staging; and
- `M` is manifests, indexes, blame, leases, journals, trash, quarantine, and
  other storage metadata.

The ideal retained state is:

```text
D_ideal = C_current + H_unique
settled_amplification = T_settled / D_ideal
```

For settled-amplification qualification, no active session may contain dirty
unpublished payload. Clean constant-size upper/work directories remain in
`T_settled` and are reported separately. A dirty-session experiment is useful
peak accounting, but it is not compared against `D_ideal`; otherwise unrelated
active edits would distort the retained-history ratio.

The target topology is:

```text
one required native current materialization
+ unique retained historical payload
+ bounded metadata and pack slack
```

The system must not settle with one complete native file or carrier per
checkpoint when historical manifests and chunks can represent the differences.

## 8. Peak and settled space criteria

### 8.1 Peak temporary space

| Operation | Allowed temporary shape |
| --- | --- |
| Publication | `C_capture` plus transaction staging no greater than 5% of `C_capture`; metadata in `M` remains separately visible |
| Cold hydration | One complete native target of allocated size `C_target` plus at most 5% of `C_target` while the cold source remains authoritative |
| Squash | One replacement carrier plus old carriers still protected by leases |
| Evacuation/compaction | Live bytes may temporarily exist in one bounded source and target |

An operation must check available space before visibility and abort cleanly on
`ENOSPC`. It must not delete an authoritative source to make room for an
unverified target.

### 8.2 Settled amplification

| Corpus | Target | Hard failure |
| --- | ---: | ---: |
| Mixed tree | `≤ 1.08 × D_ideal` | `> 1.15 × D_ideal` |
| No-dedup binary | `≤ 1.08 × D_ideal` | `> 1.15 × D_ideal` |
| Many-small-file | `≤ 1.15 × D_ideal` | `> 1.25 × D_ideal` |

Additional settled criteria:

| Metric | Target | Hard failure |
| --- | ---: | ---: |
| Avoidable current native-plus-pack duplicate payload divided by `C_current + H_unique` | `≤ 1%` | `> 3%` |
| Allocated pack bytes not occupied by live records, divided by total allocated pack bytes after compaction | `≤ 2%` | `> 5%` |
| Unexplained unreachable, unleased payload | 0 bytes | Any persistent unexplained payload |
| Native lower depth | Preemptively below 64 | Exceeds 64 |

Bytes protected by an active lease, explicit retention policy, quarantine, or
durable grace period remain counted in `T(t)` and must be reported separately.

### 8.3 Metadata budgets

| Record | Amortized budget |
| --- | ---: |
| Chunk pack/footer/index metadata | At most 96 bytes per chunk |
| File segment reference | At most 64 bytes per segment |
| Changed-path record | At most 256 bytes plus canonical path bytes |

Root, tree, blame, journal, lease, and catalog bytes are also included in
`M(t)`. Many-small-file qualification can fail even with perfect payload
deduplication if these structures exceed the total amplification target.

## 9. SeqCDC-specific storage gates

The user's accepted paper result permits SeqCDC's worst cited retained-fraction
ratio of approximately 1.139 times the paper's FCDC baseline. It does not
permit 13.9% of every source file as extra storage and does not replace direct
measurement against internal StreamCDC.

SeqCDC fails selection if, at an equal measured chunk distribution:

- its unique retained payload exceeds 1.14 times internal StreamCDC on a
  required corpus;
- its effective mean is outside 5% of 16 KiB without a separately approved,
  versioned, and requalified profile;
- it fails the localized-edit limits below; or
- the total physical-space gates fail even when the algorithm-only unique
  payload ratio is acceptable.

For an uncompressed, unencrypted, CDC-friendly file with `F ≥ 16 MiB` and a
localized change of at most 64 KiB, define:

```text
locality_target =
    changed_bytes + 2 × 32 KiB + measured_segment_overhead
```

The target is `new_unique_bytes ≤ locality_target`. The algorithm-specific
hard gate fails if the median across the localized-edit corpus exceeds
`4 × locality_target` or any sample retains at least `25% × F` as new unique
payload. Full rewrites and compressed or encrypted content are excluded from
this locality gate because `O(F)` new unique payload is expected; they remain
part of total-space qualification.

Sub-8-KiB files have identical whole-file chunk granularity under both selected
profiles. Ten distinct retained 4 KiB versions require about 40 KiB of unique
payload plus metadata; identical versions share one payload object.

## 10. Squash and history-churn criteria

Squash is a physical materialization compactor:

- `RootId` and publication/OCC generation remain unchanged;
- materialization generation advances;
- live leases pin old carriers rather than divide the logical squash plan;
- the build and all payload work occur outside remount quiescence;
- the target must verify as the same logical root;
- old and replacement leases overlap through the verified switch;
- historical last locators are evacuated before carrier deletion; and
- retention plus GC, not squash, decide whether old checkpoint payload may be
  removed.

Initial scheduling criteria:

| Trigger or limit | Decision |
| --- | --- |
| Depth accounting | Count every mounted native lower carrier, including base |
| Soft asynchronous depth trigger | Enqueue when projected depth is at least 48 |
| Hard admission depth | Compact or reject before projected depth exceeds 64 |
| Routine autosquash minimum benefit | `selected source carriers - replacement carriers ≥ 8` |
| Manual squash | Any run of at least 2 lowers |
| Squash pressure override | Only when the planned squash predicts reduced mounted depth, resident native carriers, or native allocated bytes that moves the state toward the applicable gate |
| Pack or locator pressure | Route pack slack/dead bytes to pack compaction and last-locator debt to evacuation; neither alone triggers squash |
| Mount preflight | Check both layer/kernel limits and the legacy serialized `lowerdir=` byte limit |

Synchronous hard-limit compaction occurs before publication enters its
exclusive writer section. Otherwise publication returns `NeedCompaction`,
compaction runs, and publication retries with fresh OCC validation. It must not
recursively invoke squash while holding the writer lock.

A workload is not settled until:

1. the current mount-ready projection has converged to the shallowest
   materialization that passes the space gates, including subsuming a shadowed
   base when latest-only retention would otherwise preserve avoidable bytes;
2. session and transaction leases explain every retained old carrier;
3. required historical chunks have durable replacement locators;
4. evacuation, GC, and compaction cursors have completed the admitted work;
5. trash, grace, and quarantine remain included in accounting; and
6. all amplification, duplication, slack, and depth gates pass.

Ten writes before one durable publication linearization may be coalesced into
one root. Ten durably committed publications remain ten roots until retention
releases them, even when a client response was lost.

Maintenance controls are also hard configuration:

| Control | Initial bound |
| --- | --- |
| Sealed pack payload | At most 64 MiB |
| Sealed pack records | At most 100,000 |
| Sealed pack total allocation | At most 80 MiB including headers, indexes, and footer |
| Per-pack asynchronous compaction trigger | At least 20% dead bytes |
| Aggregate urgent compaction trigger | More than 5% dead bytes or slack |
| Settled pack target | At most 2% dead bytes or slack |
| GC/compaction transaction | At most 100,000 records or 64 MiB payload, whichever comes first |
| Deletion grace | At least one complete durable grace epoch plus final generation and lease recheck |

Pack writers reserve the next record and seal before crossing any payload,
record-count, or total-allocation limit.

The Phase 1 root's canonical tree manifest is a complete reconstruction graph.
GC follows its manifest, metadata, segment, and chunk references as strong
edges. Parent/base IDs recorded for provenance are weak edges: they are marked
only when a lease, pin, active branch, configured history window, frontier, or
in-flight/pending transaction independently selects them. Materialization
records separately retain the carriers and locators required by active
backends. An ancestry field alone must not keep all history reachable under
latest-only retention.

## 11. Reusable architecture boundary

The universal reusable unit is the platform-neutral checkpoint-storage core,
not the Linux materialization backend:

| Portable core | Backend-specific adapter |
| --- | --- |
| Canonical roots/manifests and typed IDs | Capture from a backend filesystem |
| SeqCDC and immutable content objects | Linux native carriers and OverlayFS |
| Packs, indexes, publication/OCC, and leases | WASM preopened-directory or virtual-FS materialization |
| Retention, GC, journals, and recovery | Firecracker guest filesystem or block-image materialization |

Portable `RootId` input must contain no host path, inode number, OverlayFS
layer ID, mount handle, or backend locator. Backend materializations use:

```text
MaterializationKey =
    (RootId, backend_kind, backend_format_version, target_profile)
```

The canonical manifest carries a versioned capability/feature set for path
bytes, metadata, ownership, xattrs, sparse extents, hardlinks, symlinks, entry
deletion, subtree replacement, and timestamps. A backend must reproduce all
required semantics or reject the root with a capability error; it may not
silently degrade identity-bearing state. Full-tree manifests name the final
logical tree; any transition representation uses backend-neutral
`RemoveEntry` and `ReplaceSubtree` operations. Linux whiteout devices and
opaque-directory xattrs are only that adapter's encoding.

The same logical root can have multiple backend materializations. Backend
locators are outside manifest identity, but a native carrier may still be the
sole authoritative physical CAS location for current payload. It can be
deleted only after every reachable object has a verified replacement locator;
only then is that materialization a rebuildable cache.

### 11.1 Zero-new-external-dependency contract

Freeze the dependency baseline separately for every supported target and
feature invocation. The implementation passes only when all of the following
are true:

- the resolved external package identity/version set is unchanged;
- the enabled external feature set is unchanged;
- the product-wide count and multiset of direct external manifest edges do
  not grow;
- an existing direct external edge is relocated only for a documented
  responsibility move, with its old edge removed and no package, version,
  feature, or total edge-count change; and
- a new workspace crate depends only on the Rust standard library and
  internal workspace crates.

Do not add a CDC, hashing, database, allocator, profiler, benchmark, async
runtime, Python/npm, vendored, C/C++, or FFI library; a system package or
command-line tool; a runtime service, daemon, or sidecar; a target-image
helper; or a build/runtime download. The Python verifier may use the
environment's existing interpreter and standard library, but it must not add
a package. Internal workspace edges may change for a documented SRP/SOLID
split only when they remain cycle-free.

### 11.2 Docker host and Linux-image portability

“Universal” means that the provider-neutral storage core is designed for
every host/architecture supported by the declared Docker Engine or Docker
Desktop release and for every Linux image satisfying one versioned capability
profile. It does not mean that an unexecuted platform is qualified or that an
image can violate Docker and LayerStack prerequisites.

The capability profile must require only a valid OCI rootfs/config, a native
or explicitly emulated compatible architecture, the declared
mount/namespace/filesystem/xattr/security semantics, and writable LayerStack
storage such as the externally supplied `/eos` volume. Storage operations must
not require a shell, libc utility, package manager, helper executable, or
network inside the target image. A read-only, non-root, distroless, or
scratch-style image passes when it satisfies the profile even if it cannot run
an arbitrary command; test its storage behavior through the public
workspace/file API.

The frozen qualification matrix must:

- name exact host OS/version, host architecture, and Docker Engine/Desktop
  versions;
- include every required release triple available to the product, with
  representative Linux-host, macOS, and Windows rows where supported;
- pin both the OCI index digest and resolved platform-manifest digest for
  Ubuntu/Debian glibc, Alpine musl, minimal/distroless, and shell-less
  fixtures;
- cover read-only-base and non-root cases;
- label each row `qualified`, `contract-tested`, `designed-compatible`, or
  `unverified`, and classify it as `required-release` or `informational`; and
- treat every unverified required-release row as a portability and production
  no-go.

Use explicit-width, explicitly byte-ordered persisted fields and deterministic
path-byte ordering. Host-native path rules, word size, endianness, filesystem
enumeration order, and provider locators must not affect a root or object ID.
SeqCDC must always provide the deterministic scalar path. Any optional SIMD
path uses safe runtime feature detection, falls back to scalar, and produces
byte-identical boundaries and identities on x86_64 and AArch64.

Phase 1 implements and performance-qualifies only the Docker/OverlayFS
backend; the Docker host/image release matrix above still applies.
Architecture review must nevertheless prove that the portable core can be
built without importing OverlayFS, namespace, mount, guest-agent, or
WASM-runtime types. WASM and Firecracker receive their own correctness,
cold/warm materialization, time/space, security, and recovery qualification
before production use.

## 12. Correctness gates that precede measurement

Do not record a candidate as passing speed or space if any of these fail:

- every SeqCDC cut matches the pinned authors' increasing-mode oracle;
- each cut is within `1..=available`, deterministic, and independent of `Read`
  fragmentation;
- bytes, sparse extents, hardlink groups, symlinks, xattrs, modes, ownership,
  whiteouts, opaque directories, and required timestamps round-trip exactly;
- root publication is atomic, OCC-safe, and idempotent;
- old leased roots reconstruct exactly;
- blame remains separate from content identity;
- hydration verifies and fsyncs a complete target before atomic exposure;
- squash preserves `RootId`;
- remount remains native, verified, and fail-closed;
- cancellation fences a late commit;
- crash recovery is idempotent at every journal, fsync, rename, catalog,
  locator, lease, mount-move, trash, and deletion boundary; and
- no supported command, file, PTY, `write_stdin`, control-C/control-D
  cancellation, warm mount, or frozen-remount path performs CDC or cold CAS
  reconstruction;
- unsupported PTY resize, arbitrary-signal, and literal-EOF requests preserve
  their existing deterministic response; and
- portable root/object schemas remain independent of every materialization
  backend.

Any failure is disqualifying even if the resulting run is faster or smaller.

## 13. Required qualification corpora

Use deterministic, pre-generated data:

| Corpus | Minimum useful content | Primary purpose |
| --- | --- | --- |
| Mixed tree | At least 512 MiB and 20,000 files | Warm activation, mount, command, metadata, total space |
| Large source file | At least 256 MiB deterministic line records | Tiny edits, insertions, publication scan, boundary locality |
| No-dedup binary | At least 512 MiB deterministic pseudorandom bytes | Representation overhead without reuse |
| Many small files | At least 100,000 files within the time budget | Chunk/index/path/root/pack and native-directory overhead |
| Sparse file | At least 8 GiB logical with bounded allocated extents | Sparse preservation and physical accounting |
| Repeated small-file history | Multiple identical and distinct sub-8-KiB revisions | Publication coalescing, retention, packing, GC |
| Repeated large-file history | Localized edits plus compressed/full rewrites | Locality limits, carrier evacuation, settled convergence |

For the selection-advantage gate, one matched pair is one five-minute
invocation containing interleaved raw LayerStack and candidate runs with the
same workload, seed, repetition, and sample indexes. Run one raw/StreamCDC
invocation and one raw/SeqCDC invocation, then repeat that two-invocation set
three times. Counterbalance which side runs first across repetitions. Each
invocation obeys the 60-second per-operation deadline; there is no ambiguous
five-minute three-way run.

The RSS scale matrix in §6 is an additional qualification, not work packed
inside those selection invocations. Each
`input size × retained-root count × candidate` point receives its own matched
raw/candidate five-minute invocation, repeated three times after pre-generated
setup and cache reset.

Run both candidates with the same:

- effective average and range;
- input bytes and publication sequence;
- baseline reset;
- CPU placement and worker limits;
- filesystem and available disk space;
- cache state;
- retention and lease set;
- settle procedure; and
- accounting code.

Docker/container creation, image pull, and unrelated setup intervals are
reported separately. A candidate may not hide them while charging them to the
other path.

## 14. Required benchmark outputs

The machine-readable result must include:

- exact source revision, algorithm ID, parameters, format version, and build;
- pair/run ID, deterministic seed, and candidate-to-baseline execution order;
- raw LayerStack, internal StreamCDC, and SeqCDC identities;
- p50, p95, diagnostic p99, median absolute deviation, and sample count;
- operations per second and payload throughput;
- bytes read, hashed, reconstructed, newly retained, evacuated, and deleted;
- effective mean, p10, p50, p90, minimum, maximum, and total chunk count;
- peak and final RSS, explicit permit high-water marks, worker count, queue
  depth, page-cache count, and open-file-descriptor high-water mark;
- `L_hot`, `H_cold`, every `U_active`, `P_staging`, and `M`;
- `C_current`, `H_unique`, `D_ideal`, peak `T(t)`, settled `T`, and settled
  amplification;
- native-plus-pack duplication, pack slack/dead bytes, unreachable bytes,
  trash, quarantine, and lease-blocked bytes;
- warm versus cold materialization classification and reconstructed bytes;
- squash depth before/after, physical bytes before/after, build time,
  commit time, frozen time, remount outcomes, and evacuation time;
- crash/failpoint coverage and recovery outcome;
- resolved external package/version, feature, and direct-edge baseline/delta;
- dependency-boundary audit for portable core versus materialization adapters;
- host release-triple and Linux-image capability results, including pinned
  OCI index and platform-manifest digests; and
- exact reason for every target miss, exception, or hard failure.

The verifier must reject a result with missing accounting rather than treating
missing values as zero.

## 15. Final go/no-go rule

Enable SeqCDC in production only when all of the following are true:

1. every correctness and recovery gate passes;
2. logical resources are reclaimed and settled memory remains stable in one
   long-lived process, within all explicit caps and flat with file/history
   growth;
3. warm execution and materialization stay within raw LayerStack latency gates;
4. cold hydration and activation meet their native-copy controls;
5. squash meets full-operation and frozen-interval gates;
6. every total physical-space target passes, or an allowed target-to-ceiling
   exception is documented;
7. SeqCDC stays within the accepted 1.14-times unique-payload envelope against
   internal StreamCDC;
8. SeqCDC demonstrates at least a repeatable 10% integrated publication
   advantage at equal effective distribution;
9. the scalar production core remains within 300 physical non-test Rust lines
   or has an approved exception;
10. each candidate/baseline pair completes within five minutes and no
    individual operation exceeds 60 seconds;
11. the portable root/CAS core remains independent of Linux and runtime
    materialization types;
12. the resolved external package/version and enabled-feature sets are
    unchanged, direct external manifest edges do not grow, and no new build,
    test, system-tool, service, target-image, or download dependency exists;
13. the portable scalar core uses neither SIMD nor `unsafe`; every optional
    accelerated path uses safe runtime detection, scalar fallback, and
    byte-identical output, and any introduced `unsafe` has an approved
    necessity and safety proof;
14. every required-release host/image matrix row passes with pinned evidence;
    and
15. storage operations require no target-image userland, network, new
    privilege, helper, FUSE path, external database, or runtime service.

If items 7, 8, or 9 fail while the common architecture remains correct, revert
to the internal synchronous StreamCDC implementation. If a common
correctness, durability, materialization, memory, total-space, dependency, or
portability gate fails, neither chunker is production-ready until the common
storage design is fixed.
