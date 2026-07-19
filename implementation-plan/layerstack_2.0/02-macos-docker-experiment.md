# LayerStack 2.0 macOS Docker experiment

Status: **DISCOVERY RECORDED — ACCEPTANCE NOT RUN**

Verdict: **INCONCLUSIVE / BLOCKING**

Platform gate: **A-macOS UNSATISFIED**

Global implementation gate: **NO — A-macOS + A-Windows + A-Linux REQUIRED**

This file is the documentation snapshot. The executable run authority is
`EXPERIMENT.md` on branch `macos_experiment` in
`ephemeral-sandbox-layerstack-2-experiment`. Every receipt records that branch
commit and the raw evidence-bundle SHA-256.

## 1. Question under test

Can a reflink-backed LayerStack 2.0, on an ordinary macOS Docker Desktop
installation and the production sandbox security profile, provide materially
lower allocated storage and lower publish/copy-up latency than vanilla
LayerStack without breaking arbitrary OCI images, file blame, squash,
same-upperdir remount, active execution, or daemon health?

This is an acceptance experiment, not a demo. Empty result cells mean
“unknown,” never zero. Simulated numbers may be used in a separately labelled
capacity model but can never appear in the measured tables or change the
verdict.

## 2. Verdict rules

The final verdict is one of:

- `PASS`: every mandatory gate passes and the evidence bundle is complete;
- `FAIL`: any mandatory compatibility, privilege, correctness, storage,
  latency, blame, or memory gate fails; or
- `INCONCLUSIVE`: the run or evidence is incomplete. This keeps
  implementation blocked.

Only the repository owners may change the status at the top after reviewing
the raw artifact digest and pinned product revision.

## 3. Harness location and two-stage sequencing

Before product code, use a disposable external prototype to prove A-macOS:
Docker-native storage provisioning, production mount-builder compatibility,
real shared extents, and an empty security-profile diff. A-macOS currently has
no qualifying backend. Product implementation remains blocked until A-macOS,
A-Windows, and A-Linux all pass and global Gate A is reviewed.

A-macOS's helper is a standalone reference implementation committed to the test
repository, not a nonexistent product primitive. It uses raw `FICLONE`,
FIEMAP, `mount(2)`, and the exact mount flags/options exported from the current
production builder; its source, binary digest, syscall trace, and cleanup are
evidence. Gate B must repeat every probe through the implemented `layerstore`
primitive and the actual v2 production mount path. A mismatch invalidates Gate
A rather than allowing the reference helper to define product behavior.

The executable harness, platform adapters, and append-only evidence record
belong on this platform branch in the dedicated experiment repository, not in
the runtime or documentation repository. It may invoke a pinned
`ephemeral-sandbox-test` checkout, but must not make that checkout the only
copy of the protocol or results. Add:

```text
ephemeral-sandbox-layerstack-2-experiment/
├── EXPERIMENT.md
├── RUN-REPORT.md
├── harness/
│   ├── probe.py
│   ├── workload.py
│   ├── measure.py
│   ├── test_capability_and_privilege.py
│   ├── test_space_and_latency.py
│   ├── test_blame_and_crash_consistency.py
│   ├── test_squash_remount_quiesce.py
│   └── test_memory_and_soak.py
└── artifacts/                 # ignored locally; sealed bundle published separately
```

Reuse the existing squash case recorder and percentile calculation. Every live
run must append its command, good result, defect, and fix to the append-only
run report before the next command is executed. Preserve raw per-sample JSONL,
daemon logs, inspect output, manifests/database snapshots, mountinfo, FIEMAP
evidence, cgroup memory series, and teardown evidence.

## 4. Pin the environment

Record this table before running either baseline or candidate:

| Field | Required value | Recorded value |
|---|---|---|
| macOS version/build | exact | PENDING |
| host architecture | exact | PENDING |
| Docker Desktop version | exact | PENDING |
| Docker Engine/API version | exact | PENDING |
| LinuxKit kernel | exact | PENDING |
| Docker storage driver/backing FS | exact | PENDING |
| Docker VM CPU/RAM/disk limit | exact | PENDING |
| file-sharing/VMM setting | exact | PENDING |
| `ephemeral-sandbox` commit | full SHA | PENDING |
| `ephemeral-sandbox-test` commit | full SHA | PENDING |
| config and binary SHA-256 | digest | PENDING |
| candidate storage layout/schema | exact version | PENDING |
| image references | immutable digests | PENDING |

Local discovery on 2026-07-19 saw macOS 26.4.1 arm64, Docker Desktop 4.76.0,
Engine 29.5.2, and LinuxKit 6.12.76. This is **not** an acceptance run and does
not fill the table; the complete experiment must capture all fields in one
sealed artifact bundle.

Use at least Alpine, Ubuntu or Debian, and a scratch/distroless-style image
with the experiment helper injected externally. The workload must not depend
on a shell or package manager inside the target image.

## 5. Variants

Run randomized paired samples for all three variants:

| ID | Layout | Transfer path | Purpose |
|---|---|---|---|
| A | current separate volumes | current full copy | vanilla LayerStack baseline |
| B | v2 single storage domain | reflink forced off | isolates topology/metadata effects |
| C | v2 single storage domain | reflink required | candidate |

A comparison of A and C alone is invalid because it attributes volume layout,
metadata, and scheduling changes to reflink. Variant B is mandatory.

All variants use identical image digests, daemon configuration apart from the
declared layout/extent mode, Docker resource limits, test order distribution,
warm-up policy, and cleanup.

## 6. Phase 0: feasibility and privilege proof

### 6.1 Storage-domain proof

On the exact volume used by the runtime:

1. record `statfs`, mount options, `st_dev`, filesystem UUID where available,
   and allocated/free bytes;
2. prove `objects`, `staging`, session `upper`, and session `work` share
   `st_dev`;
3. create deterministic, incompressible, fully allocated source data;
4. clone it using A-macOS's reviewed reference primitive (and, in Gate B, the
   actual product primitive);
5. show shared physical extents with FIEMAP or filesystem-native tooling;
6. overwrite one aligned 4 KiB block in the clone;
7. prove source content is unchanged and only a bounded extent region became
   exclusive; and
8. destroy the test domain and prove no resource remains.

Logical size, `ls -l`, sparse zero files, compression, and `du` alone are
insufficient. Keep the raw extent maps and before/after filesystem allocation.

### 6.2 Real OverlayFS copy-up proof

For A-macOS, mount an OverlayFS with the reference helper using the exact flags
and options exported from the current production mount builder. For Gate B,
repeat through the actual v2 production mount path. Use the immutable source
as a lowerdir and a v2 session upper/work pair. Measure extents and allocation:

1. before opening for write;
2. after opening without modifying, to expose unnecessary copy-up;
3. after one 4 KiB overwrite;
4. after 1,024 scattered 4 KiB overwrites; and
5. after an atomic full-file replacement.

For the tiny overwrite, the copied-up upper file must share extents with the
lower except around dirtied blocks. This proves the kernel clone path, not just
the runtime clone path.

### 6.3 Privilege diff

Capture normalized `docker inspect`, effective capability masks, devices,
device-cgroup rules, seccomp/security options, mount propagation, namespaces,
and helper processes for A, B, and C.

Mandatory gate `PRIV-01`:

```text
normalized_security(B) == normalized_security(A)
normalized_security(C) == normalized_security(A)
```

Only volume names, paths, and the declared v2 configuration may differ. Fail
if C needs privileged mode, an extra capability, `/dev/fuse`, a loop device,
new device rule, host filesystem setup, Docker plugin, helper daemon, socket,
or relaxed seccomp/LSM/no-new-privileges setting.

### 6.4 Feasibility table

| Gate | A | B | C | Required C result | Evidence |
|---|---:|---:|---:|---|---|
| same `st_dev` for lower/upper/work | PENDING | PENDING | PENDING | PASS | PENDING |
| direct clone shares physical extents | N/A | N/A | NOT RUN; default volume disqualified | PASS | D1: ext4, `FICLONE` → errno 95 |
| 4 KiB mutation preserves source | N/A | N/A | PENDING | PASS | PENDING |
| OverlayFS copy-up shares extents | NO | NO | PENDING | PASS | PENDING |
| no security-profile delta | baseline | PENDING | PENDING | PASS | PENDING |
| no host install/helper/plugin/device | baseline | PENDING | PENDING | PASS | PENDING |

D1 is a discovery result that eliminates one backend; it is not a completed C
run because no alternative candidate backend has been selected. Stop after
Phase 0 and record `FAIL` if a selected candidate fails. Do not run performance
tests on a candidate that is not actually reflink-backed.

## 7. Workload matrix

Use deterministic seeded data. Large files must be incompressible and fully
allocated. Each correctness case runs at least once per image; performance
cases use the designated benchmark image.

| ID | Workload | Purpose |
|---|---|---|
| W01 | no-op session over a 1 GiB lower file | branch/setup overhead |
| W02 | one aligned 4 KiB overwrite in a 1 GiB file | best-case CoW |
| W03 | 1,024 scattered 4 KiB overwrites | fragmented CoW |
| W04 | append 4 KiB and truncate | size changes |
| W05 | insert one byte near start through temp+rename | offset/replace worst case |
| W06 | replace with a new 1 GiB random file | no-sharing worst case |
| W07 | 100,000 files of 1–8 KiB; edit 1% | metadata/small-file path |
| W08 | sparse file with data islands | sparse preservation |
| W09 | hardlinks, symlinks, modes, xattrs | metadata equivalence |
| W10 | deletes, whiteouts, opaque directory replacement | Overlay semantics |
| W11 | 100 sequential published versions of W02 | retained-version space |
| W12 | 100 live sessions from one head, then publish | multi-agent/session scale |
| W13 | 1, 10, and 100 concurrent agent processes in one session | shared-container execution |
| W14 | squash an 8-layer and a 100-layer eligible run | compaction |
| W15 | active request service during remount | application pause/continuity |

## 8. Measurement method

- Use five warm-ups and at least 30 measured paired samples for short cases.
- Use at least 10 measured samples for 1 GiB/100,000-file cases when 30 is
  operationally excessive; state the reduced confidence before the run.
- Randomize A/B/C order within each repetition using a recorded seed.
- Report raw values, p50, p95, p99 where sample size supports it, maximum,
  median absolute deviation, and bootstrap 95% confidence intervals for the
  paired median delta.
- Measure wall time with a monotonic clock. Keep setup, correctness checks, and
  teardown outside a named critical interval.
- Report cold and warm-cache series separately. Apply any cache treatment
  equally; never claim a page-cache result as a disk result.
- Capture host/VM noise, CPU time, read/write bytes, IOPS, allocation, anonymous
  RSS, file cache, PSI, open fds, and queue depth.

Named intervals:

| Metric | Start | End |
|---|---|---|
| session create | request sent | usable workspace returned |
| first write | write/open request starts | fsync/close completes |
| capture | capture begins | immutable change set produced |
| publish | staged transfer begins | metadata commit acknowledged |
| squash build | plan released lock | all `S` objects fsynced |
| squash commit | exclusive transaction begins | manifest commit durable |
| remount pause | last confirmed application progress before stop | first confirmed progress after resume |
| frozen interval | first successful `SIGSTOP` | final required `SIGCONT` |
| end-to-end | agent mutation begins | published version acknowledged |

## 9. Storage result tables

Report filesystem-wide allocation deltas and object-exclusive/shared extents.
The values below are intentionally blank.

### 9.1 One 4 KiB edit in a 1 GiB file

| Variant | Lower allocated | Upper delta | Published-layer delta | Total retained delta | Shared extents | Verdict |
|---|---:|---:|---:|---:|---:|---|
| A vanilla | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| B v2 copy | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| C v2 reflink | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |

### 9.2 One hundred versions

| Workload | Variant | Logical GiB | Allocated GiB | Exclusive GiB | Reclaimable GiB | Reduction vs A |
|---|---|---:|---:|---:|---:|---:|
| W02 × 100 | A | PENDING | PENDING | PENDING | PENDING | baseline |
| W02 × 100 | B | PENDING | PENDING | PENDING | PENDING | PENDING |
| W02 × 100 | C | PENDING | PENDING | PENDING | PENDING | PENDING |
| W06 × 100 | A | PENDING | PENDING | PENDING | PENDING | baseline |
| W06 × 100 | B | PENDING | PENDING | PENDING | PENDING | PENDING |
| W06 × 100 | C | PENDING | PENDING | PENDING | PENDING | PENDING |

Mandatory storage gates:

- `SPACE-01`: W02 × 100 C total retained allocation is at least 90% lower than A and
  at least 80% lower than B.
- `SPACE-02`: W03 C allocation tracks dirtied extents rather than full logical
  file size and is at least 70% lower than A.
- `SPACE-03`: W06 is reported honestly; C may not claim savings when content
  shares no blocks, and its overhead must be no more than 5% above B.
- `SPACE-04`: after squash, lease release, and destroy, allocation returns to
  within 1% or 16 MiB (whichever is larger) of the expected retained set.
- `SPACE-05`: logical bytes reconcile exactly. The absolute residual between
  filesystem allocation delta and unique shared-plus-exclusive payload
  accounting is no more than the greater of 1% or 16 MiB; per-file FIEMAP
  accounting differs by no more than one filesystem block per mapped extent.

## 10. Performance result tables

### 10.1 Latency

| Workload/interval | Variant | p50 | p95 | p99 | max | CPU time | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| W02 first write | A | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W02 first write | B | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W02 first write | C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W02 publish | A | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W02 publish | B | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W02 publish | C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W07 end-to-end | A | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W07 end-to-end | B | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W07 end-to-end | C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W14 squash | A | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W14 squash | B | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| W14 squash | C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |

Mandatory latency gates:

- `PERF-01`: for W02, C first-write and publish p50 are each at least 2× faster
  than A, and confidence intervals do not cross no improvement.
- `PERF-02`: C p95 is not more than 5% slower than B for W06, W07, or no-op
  W01; these no-sharing/metadata controls are non-regression tests, not claims
  that reflink must beat B everywhere.
- `PERF-03`: C adds no more than 5% p95 command latency to read-only workloads.
- `PERF-04`: C squash p95 is no slower than A by more than 5%; current hardlink
  squash is already byte-neutral, so no speedup is presumed.
- `PERF-05`: during a 15-minute W13 window at 100 concurrent agents, C
  throughput is at least 90% of B, every agent completes an operation in every
  60-second window after warm-up, bounded queue occupancy never exceeds its
  configured limit, and there are zero unclassified timeouts or overflows.

## 11. File-blame and transaction proof

For every relevant workload, capture normalized `file_blame` responses before
and after publish, squash, remount, daemon restart, and GC. Compare exact
`start_line`, `line_count`, and `owner` tuples—not only owner presence.

| Case | Expected | A | B | C | Evidence |
|---|---|---|---|---|---|
| mixed-owner OCC merge | exact line ranges preserved | PENDING | PENDING | PENDING | PENDING |
| no-op publish | no new blame event | PENDING | PENDING | PENDING | PENDING |
| live unfinalized write | blame remains last published state | PENDING | PENDING | PENDING | PENDING |
| delete and delete→recreate | v1 output preserved exactly | PENDING | PENDING | PENDING | PENDING |
| rename/copy; empty/binary; trailing newline | v1 characterization fixture preserved | PENDING | PENDING | PENDING | PENDING |
| base-only/absent path | current `NotFound` behavior preserved | PENDING | PENDING | PENDING | PENDING |
| huge sparse owner ranges | legacy whole-array response exact; bounded RSS via internal paging/spool | PENDING | PENDING | PENDING | PENDING |
| squash | response byte-identical before/after | PENDING | PENDING | PENDING | PENDING |
| live remount | response byte-identical before/after | PENDING | PENDING | PENDING | PENDING |
| restart | response byte-identical | PENDING | PENDING | PENDING | PENDING |
| crash before visibility commit | neither layer nor blame visible | PENDING | PENDING | PENDING | PENDING |
| crash after visibility commit | both layer and blame visible | PENDING | PENDING | PENDING | PENDING |
| commit succeeded/reply lost/retry | same revision; no duplicate layer/event | PENDING | PENDING | PENDING | PENDING |
| metadata/WAL/checkpoint ENOSPC or I/O failure | old-or-new state; never partial attribution | PENDING | PENDING | PENDING | PENDING |

Mandatory gate `BLAME-01`: every row passes, and no successful v2 publish can
be observed without its matching provenance state. The existing public
`file_blame` status, headers, JSON shape, ordering, and values must remain
compatible; internal paging is not permission to replace or truncate that API.
Any public cursor endpoint is tested only as an additive, separately approved
API.

## 12. Squash, remount, and active-execution proof

Retain the current storage/remount boundary:

- squash plans around lease boundaries, builds lock-free, revalidates
  contiguity, commits storage first, and cannot be rolled back by remount;
- replacement lease acquisition precedes old-lease release;
- the production boot gate proves same-upperdir/fresh-workdir coexistence,
  whiteouts, and opaque directories on the v2 domain;
- quiesce discovers the namespace/cgroup union, stops and rechecks every task,
  and rejects cwd/root/fd/map pins or uncertainty before PONR;
- staged move ordering and faulty post-PONR handling are unchanged; and
- rollback unmount is strict, with no `MNT_DETACH`.

Fault matrix:

| ID | Injection | Required outcome | Result |
|---|---|---|---|
| RM01 | cwd in workspace | clean pre-PONR block; tasks resume; OLD retained | PENDING |
| RM02 | workspace fd open | clean pre-PONR block | PENDING |
| RM03 | workspace mmap | clean pre-PONR block | PENDING |
| RM04 | child mount | clean pre-PONR block | PENDING |
| RM05 | task appears after stop | clean pre-PONR block | PENDING |
| RM06 | first `MS_MOVE` fails | release NEW, keep OLD, resume | PENDING |
| RM07 | second move/verification fails | keep frozen, mark faulty, destroy | PENDING |
| RM08 | rollback unmount returns `EBUSY` | resume on NEW, install NEW handle, park OLD+lease | PENDING |
| RM09 | report missing | compare mount IDs; resume only if unchanged | PENDING |
| RM10 | remount skipped after committed squash | compact manifest remains durable | PENDING |

### Active service benchmark

Run for at least 15 minutes a service outside the workspace cwd that increments a monotonic sequence,
serves requests, and periodically fsyncs/verifies workspace data without
holding a pin during the intended switch window. Drive it continuously from a
separate client.

| Variant | samples | request p50 | request p95 | longest silent gap | frozen p95 | errors/timeouts | sequence gaps |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| B | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |

The published idle baseline—p50 5 ms, p95 6 ms, pooled p99 7.1 ms, max
18 ms across 145 measurements—is context only. It measured the complete
operation for an idle session, not application `SIGSTOP` → `SIGCONT`, and is
not an SLA. The current 500 ms freeze budget and 30 s runner timeout are safety
ceilings, not performance targets.

Mandatory gates:

- `REMOUNT-01`: every fault row has the exact classified outcome;
- `REMOUNT-02`: merged-tree digest and blame are identical across successful
  switch and every clean skip;
- `ACTIVE-01`: zero request errors, timeouts, or sequence gaps;
- `ACTIVE-02`: C frozen p95 and longest silent gap each regress no more than
  10% from A; frozen p95 and the longest silent gap are each at most 500 ms;
  and
- `ACTIVE-03`: every resumed process observes the expected mount generation
  and correct post-resume bytes.

## 13. Memory and daemon-health proof

Measure cgroup `memory.current`, `memory.peak`, `memory.stat` (`anon` and
`file` separately), process RSS/PSS, allocator metrics where available, open
fds, threads, metadata queue depth, WAL/cache bytes, and page faults.

Runs:

1. transfer a 1 GiB and 10 GiB file to prove peak anonymous memory is
   independent of file size;
2. grow to 10,000 historical revisions while keeping the active chain below
   the production bound, query manifests and blame, then restart; separately
   run a clearly test-only 10,000-active-layer diagnostic with a raised bound;
3. create/destroy 10,000 sessions in waves while retaining no leases;
4. issue one million blame updates over a bounded path set, then over a growing
   path set, without an eager heap index;
5. run W13 plus continuous publish/squash/remount for at least 24 hours; and
6. inject repeated clone fallback and recoverable remount blocks to expose
   leaked buffers, guards, tasks, or metrics labels.

| Run | Variant | steady RSS/PSS | peak anon | peak file cache | RSS slope/hour | fd/thread delta | queue/WAL peak | daemon health |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 GiB transfer | A | PENDING | PENDING | PENDING | N/A | PENDING | PENDING | PENDING |
| 1 GiB transfer | B | PENDING | PENDING | PENDING | N/A | PENDING | PENDING | PENDING |
| 1 GiB transfer | C | PENDING | PENDING | PENDING | N/A | PENDING | PENDING | PENDING |
| 10 GiB transfer | A | PENDING | PENDING | PENDING | N/A | PENDING | PENDING | PENDING |
| 10 GiB transfer | B | PENDING | PENDING | PENDING | N/A | PENDING | PENDING | PENDING |
| 10 GiB transfer | C | PENDING | PENDING | PENDING | N/A | PENDING | PENDING | PENDING |
| 10k historical revisions, bounded active head | C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| 10k active layers, test-only diagnostic | C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| 10k sessions | C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| 1m events, bounded path set | C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| 1m events, growing path set | C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| 24 h mixed soak | C | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |

Retained-state and recovery measurements:

| Run | DB bytes start/end | WAL max | checkpoint p95/max | recovery start latency | recovery backlog end | staged/export/lost+found bytes end |
|---|---:|---:|---:|---:|---:|---:|
| 10k historical revisions | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| 10k sessions | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| 1m bounded-path events | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| 1m growing-path events | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| 24 h mixed soak | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |

Use this fixed resource profile for the qualification run so “bounded” is
numerically falsifiable. The backing store must have at least 64 GiB available;
v2 accounting enforces a 64 GiB test-domain quota even when Docker cannot
provide a native per-volume quota.

| Resource | Qualification limit |
|---|---:|
| SQLite page cache | 32 MiB |
| WAL checkpoint target | 64 MiB |
| WAL hard health ceiling | 256 MiB |
| aggregate staging | 12 GiB |
| aggregate export spools | 2 GiB |
| `lost+found` + recovery backlog | 2 GiB |
| all transient pools combined | 16 GiB |
| free space reserved only for recovery | 4 GiB |
| normal visible-state admission high-water | 44 GiB allocated |
| parked remounts | 64 sessions |

The 10 GiB lane proves that the 12 GiB staging limit is usable. Resource-fault
cells use at most 1 GiB per object so their deterministic cleanup/quarantine
fits the recovery profile. Production limits may be sized differently, but
Gate B must pin equally concrete values and repeat the boundary tests.

Mandatory gates:

- `MEM-01`: for B and C separately, 10 GiB transfer peak anonymous memory is
  within 16 MiB of the corresponding 1 GiB transfer after baseline
  subtraction; A/B/C use identical buffer, concurrency, and cache conditions.
- `MEM-02`: no daemon-owned payload cache or data structure scales with file
  bytes; profiler evidence identifies every retained allocation class.
- `MEM-03`: after warm-up and completed cleanup, the Theil–Sen anonymous-RSS
  slope over the final 12 soak hours is no greater than 1 MiB/hour and its
  seeded 95% bootstrap confidence interval includes zero with an upper bound
  no greater than 1 MiB/hour.
- `MEM-04`: fds, tasks, leases, staged objects, parked mounts, and bounded
  queue entries return to their expected steady-state counts.
- `MEM-05`: zero OOM kills, allocator failures, panics, daemon restarts, or
  unexpected health/readiness failures; WAL checkpoints target 64 MiB and WAL
  never exceeds the 256 MiB hard ceiling.
- `MEM-06`: growing blame history increases disk usage but not resident heap
  proportional to total paths/events.
- `MEM-07`: staging, export, recovery, and combined transient allocation never
  exceed the numeric table; one boot sweep returns unreachable transient bytes
  to zero or an explicitly accounted quarantine below its limit.
- `MEM-08`: fill and concurrent-race tests at every high-water reject new work
  before visibility, preserve at least 4 GiB recovery reserve, leave old state
  readable, and recover without bypassing admission or deleting blame.

## 14. Crash, ENOSPC, and recovery

Inject process death and storage failures at every durable boundary:

- during clone/copy;
- after object-tree fsync, promotion rename, and objects-parent fsync;
- during each bounded pending-path/range batch;
- before and during the short visibility transaction WAL/commit;
- after a durable commit but before response, followed by idempotent retry;
- during WAL checkpoint and on WAL/metadata/staging quota exhaustion;
- during squash object promotion and commit;
- during live-session, squash-plan, replacement, and parked-rollback lease
  acquisition, epoch recovery, and release;
- before and after remount PONR; and
- during boot reap/checkpoint.

Run relevant storage/metadata faults against B and C so reflink is isolated
from v2 transaction behavior. After every restart, assert exactly one
old-or-new committed state, correct
blame pairing, no referenced-missing object, no active partial object, no
unpinned live chain, no duplicate result for an uncertain retry, bounded WAL,
and deterministic cleanup/quarantine. A dead epoch alone never authorizes
release of a lease whose mount/session state has not been proven.

## 15. Final gate table

| Gate family | Required | Result | Evidence artifact |
|---|---|---|---|
| FEASIBILITY | all Phase 0 gates pass | **UNSATISFIED** | D1 eliminated the default volume; no candidate selected |
| PRIVILEGE | `PRIV-01` | PENDING | PENDING |
| STORAGE | `SPACE-01` … `SPACE-05` | PENDING | PENDING |
| PERFORMANCE | `PERF-01` … `PERF-05` | PENDING | PENDING |
| BLAME | `BLAME-01` | PENDING | PENDING |
| REMOUNT | `REMOUNT-01`, `REMOUNT-02` | PENDING | PENDING |
| ACTIVE | `ACTIVE-01` … `ACTIVE-03` | PENDING | PENDING |
| MEMORY | `MEM-01` … `MEM-08` | PENDING | PENDING |
| CRASH/RECOVERY | every injected boundary | PENDING | PENDING |
| ARBITRARY IMAGES | every pinned image | PENDING | PENDING |
| TEARDOWN | no experiment-owned residue | PENDING | PENDING |

Final verdict: **INCONCLUSIVE — DEFAULT BACKEND DISQUALIFIED; C NOT RUN**

Evidence bundle SHA-256: `PENDING`

Reviewer and date: `PENDING`

## 16. Host qualification scope

This document's A-macOS verdict applies only to the pinned macOS Docker Desktop
environment and architecture. Apple Silicon does not prove Intel macOS. The
dedicated experiment repository has three peer evidence branches, executed in
this order:

1. `macos_experiment`;
2. `windows_experiment`; and
3. `linux_experiment`.

Global Gate A is the conjunction of A-macOS, A-Windows, and A-Linux across
every declared host/architecture lane. No LayerStack 2.0 product code starts
until that conjunction passes. Gate B then repeats the shared security,
arbitrary-image, correctness, storage, performance, blame, remount, crash, and
memory suite through the integrated runtime on:

- supported native Linux kernels/filesystems;
- Windows Docker Desktop/WSL 2; and
- every other host architecture declared supported by the product.

Each host records whether `required`, `preferred`, or only `disabled` is
available. A copy fallback may preserve correctness and universality, but it
does not pass that lane's reflink gate and cannot support a cross-platform
reflink storage/performance claim. Production configuration must never present
one host's successful probe as another host's capability. Every platform
receipt records its branch commit, shared-protocol commit, exact environment
cell, and evidence-bundle SHA-256.

## Appendix A: discovery run report

This appendix is append-only. Discovery results identify blockers but do not
replace the complete acceptance run above.

### 2026-07-19 D0 — default named-volume clone probe

Command (recorded before execution): create the explicitly named temporary
Docker volume `eos-layerstack2-probe-20260719`, run
`python:3.13-bookworm` with no added capabilities, record the volume
filesystem and `st_dev`, stream 64 MiB of random data, attempt Linux
`FICLONE`, verify source/clone independence if it succeeds, and remove the
test-owned volume.

Good: the default Docker named volume supports real extent cloning without an
added capability, or the probe returns a precise unsupported error and leaves
no residue.

Defect: the probe stopped before `FICLONE`; the parser searched
`/proc/self/status` for a literal escaped tab and raised `IndexError`. The
test-owned volume was removed by the registered cleanup trap.

Fix/next action: parse the `CapEff` line by field prefix and rerun as D1.

### 2026-07-19 D1 — corrected default named-volume clone probe

Command (recorded before execution): repeat D0 on the same explicitly named,
newly created test volume, but parse `CapEff` by splitting the line at `:`.
The cleanup trap remains mandatory.

Good: a complete JSON result identifies filesystem, `st_dev`, effective
capabilities, allocated bytes, and either successful clone independence or a
precise unsupported errno; cleanup removes the volume.

D1 result: Docker's default named volume reported filesystem `ext2/ext3`
(the `statfs` family name for ext4), `st_dev=65025`, and a fully allocated
64 MiB source. `FICLONE` failed with errno 95, `EOPNOTSUPP`. The container had
Docker's ordinary default effective capability mask `00000000a80425fb`; no
capability was added by the command. The cleanup trap removed the test volume.

Raw probe record:

```json
{"cap_eff":"00000000a80425fb","errno":95,"error":"Operation not supported","ficlone":"error","filesystem":"ext2/ext3","source_allocated_bytes":67108864,"source_logical_bytes":67108864,"st_dev":65025}
```

Defect: the default Docker Desktop named-volume backing filesystem cannot
provide reflink. Co-locating v2 directories on an ordinary named volume is
therefore insufficient on this machine.

Fix/next action: keep implementation blocked. A different Docker-native
storage provisioning path must independently pass the no-device/no-helper/no-
extra-privilege gate. D2 quantifies OverlayFS copy-up on the known non-reflink
volume; it is diagnostic, not an attempt to turn this backend into a candidate.

### 2026-07-19 D2 — OverlayFS copy-up diagnostic with only `SYS_ADMIN`

Command (recorded before execution): create a new test-owned named volume; run
`ubuntu:24.04` with all capabilities dropped and only `SYS_ADMIN` added plus
no-new-privileges; create lower, upper, work, and merged directories on that
one volume; write a fully allocated random 64 MiB lower file; mount OverlayFS;
overwrite 4 KiB through the merged mount; report lower/upper logical and
allocated bytes and effective capabilities; strictly unmount; then remove the
volume.

Good: the production-relevant mount authority is sufficient, the result
quantifies whether the upper file is extent-shared or fully allocated, and
strict cleanup leaves no residue.

Defect: `mount(8)` failed before copy-up with `cannot mount overlay
read-only` under this deliberately stripped container profile. The container
exited and the registered cleanup trap removed the test volume. This CLI probe
does not reproduce the product's user/mount-namespace setup or raw production
mount builder, so it is not evidence that the product needs another
capability, nor is it valid copy-up evidence.

Fix/next action: do not weaken the security profile or add an unconfined
override to make a diagnostic pass. The acceptance harness must invoke the
production gate/mount builder with the exact full production HostConfig and
record its classified result. A-macOS remains unsatisfied: D1 disqualified the
default named volume and no alternative candidate has been selected.
