# LayerStack 2.0 macOS Docker experiment

Status: **UNVERIFIED DISCOVERY CONTEXT — ACCEPTANCE NOT RUN**

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

Gate A-macOS receives one feasibility verdict:

- `PASS`: every Phase-0 same-domain, direct-clone/CoW, production-option
  OverlayFS copy-up, security-diff, and teardown gate passes with a sealed
  evidence bundle;
- `FAIL`: any mandatory Phase-0 gate fails on a required stock environment; or
- `INCONCLUSIVE`: a Phase-0 run, required cell, or evidence receipt is
  incomplete. This keeps implementation blocked.

Storage, performance, image, blame, remount, crash, and memory verdicts belong
to post-implementation Gate B. They cannot be prerequisites for Gate A and
remain `BLOCKED_NOT_RUN` until global Gate A authorizes product work.

Only the repository owners may change the status at the top after reviewing
the raw artifact digest and pinned product revision.

## 3. Harness location and two-stage sequencing

Before product code, use a disposable external prototype to prove A-macOS:
same-domain Docker-native storage, numeric direct reflink and CoW behavior,
real OverlayFS copy-up with exported production options, an empty security
profile diff, and complete teardown. A-macOS currently has no qualifying
receipt. Product implementation remains blocked until A-macOS, A-Windows, and
A-Linux all pass and global Gate A is reviewed.

A-macOS's helper is a standalone reference implementation committed to the test
repository, not a nonexistent product primitive. It uses raw `FICLONE`,
FIEMAP, `mount(2)`, and the exact mount flags/options exported from the current
production builder; its source, binary digest, syscall trace, and cleanup are
evidence. Gate B must repeat every probe through the implemented `layerstore`
primitive and the actual v2 production mount path. A mismatch blocks Gate B,
requires a classified discrepancy review and rerun, and may motivate a new
Gate A receipt; it never rewrites the historical evidence-addressed receipt.

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
| product support-matrix/corpus revision | full commit/digest | PENDING |
| image references | immutable digests | PENDING |

Unverified imported notes dated 2026-07-19 mention macOS 26.4.1 arm64, Docker
Desktop 4.76.0, Engine 29.5.2, and LinuxKit 6.12.76. They have no sealed receipt
or evidence digest, do not fill this table, and cannot affect a verdict.

Gate B runs every image in the complete product supported-image corpus pinned
above, not a selected subset. It additionally includes Alpine, Ubuntu or
Debian, and a scratch/distroless-style semantic extreme with the experiment
helper injected externally. The workload must not depend on a shell, package
manager, library, hook, or helper inside the target image.

## 5. Gate B benchmark variants

This section, Sections 7–14, and Section 15.2 are a preregistered Gate B
protocol. They are not executable before global Gate A and do not contribute
to A-macOS.

Run randomized paired samples for all three variants:

| ID | Layout | Transfer path | Purpose |
|---|---|---|---|
| A | current separate volumes | current full copy | vanilla LayerStack baseline |
| B | v2 single storage domain | runtime publish/squash clone disabled | runtime-transfer control |
| C | v2 single storage domain | reflink required | candidate |

A comparison of A and C alone includes topology, metadata, kernel copy-up, and
runtime transfer. Variant B is mandatory when isolating the runtime transfer,
but it cannot disable OverlayFS's kernel copy-up clone attempt. Measure and
report kernel copy-up sharing in B and C; never prescribe or prefill it.

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
3. create at least 1 GiB of deterministic seeded, incompressible, fully
   allocated source data and record its seed and cryptographic hash;
4. clone it using A-macOS's reviewed reference primitive (and, in Gate B, the
   actual product primitive);
5. show with FIEMAP or filesystem-native tooling that at least 99% of allocated
   payload bytes are shared, allowing reconciliation error of at most one
   filesystem block per mapped extent;
6. overwrite one aligned 4 KiB block in the clone;
7. prove the source hash is unchanged, at most two new exclusive extent
   intervals appear, and both shared-byte loss and exclusive-byte growth are no
   more than `max(128 KiB, 32 × filesystem block size)`; and
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

For the tiny overwrite, at least 99% of the unchanged allocated payload must
remain physically shared between lower and upper, with at most one filesystem
block per mapped extent of reconciliation error. The source hash must remain
unchanged and the same mutation-growth bound from Section 6.1 applies. This
proves the kernel clone path, not just the runtime clone path.

### 6.3 Privilege diff

Capture raw and canonical `docker inspect`, effective capability masks,
devices, device-cgroup rules, seccomp/security options, mount propagation,
namespaces, Docker/VM settings, host changes, and helper processes for the
production baseline and Gate A candidate. Repeat for A/B/C in Gate B.

Mandatory gate `PRIV-01`:

```text
canonical_security(gate_a_candidate) == canonical_security(production_baseline)
canonical_security(B) == canonical_security(A)
canonical_security(C) == canonical_security(A)
```

The versioned canonicalizer may normalize only timestamps, runtime-generated
IDs, semantically irrelevant ordering, and declared experiment path tokens. It
must never normalize capabilities, privileged state, devices/device rules,
seccomp, LSM, no-new-privileges, namespaces, propagation, helper processes,
Docker/VM settings, or host changes. Retain raw snapshots, canonical snapshots,
both diffs, and the canonicalizer source/binary SHA-256. Fail if the candidate
needs privileged mode, an extra capability, `/dev/fuse`, a loop device, new
device rule, host filesystem setup, Docker plugin, helper daemon, socket, or a
relaxed security setting.

### 6.4 Feasibility table

| Gate | Production baseline | Gate A reference candidate | Required result | Evidence |
|---|---:|---:|---|---|
| one `st_dev` for objects/staging/lower/upper/work | reference only | PENDING | PASS | PENDING |
| direct clone shared allocated payload | N/A | PENDING | at least 99% | PENDING |
| aligned 4 KiB CoW isolation | N/A | PENDING | source hash exact; growth within bound | PENDING |
| OverlayFS unchanged payload remains shared | reference only; sharing unprescribed | PENDING | at least 99% | PENDING |
| raw/canonical security delta | reference snapshot required | PENDING | empty outside declared paths | PENDING |
| no host install/helper/plugin/device | reference snapshot required | PENDING | PASS | PENDING |
| strict teardown | reference inventory required | PENDING | no experiment-owned residue | PENDING |

The imported D0–D2 notes have no sealed receipt and do not fill this table.
Stop after Phase 0 and record `FAIL` if a selected candidate fails. If it
passes, seal A-macOS and stop: product benchmarks remain blocked until global
Gate A has passed and implementation exists.

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
| W16 | external helper: sequentially hash/read a 1 GiB lower file, walk/stat the W07 tree, and perform 10,000 seeded 4 KiB random `pread`s | read-only data/metadata non-regression |

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
Every delta subtracts the quiescent pre-run domain allocation measured after
the common warm-up. The values below are intentionally blank.

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
- `SPACE-04`: before execution, write the exact retained object IDs and policy
  to the run manifest. Define the expected retained set as the union of unique
  allocated extents belonging to pre-existing pinned bases/control metadata,
  objects reachable from the declared retained revisions after squash, the
  checkpointed SQLite DB/WAL/SHM, and explicitly listed quarantine objects.
  Sessions, staging, export spools, released-lease objects, and unreachable
  objects are excluded. After squash, lease release, destroy, checkpoint, and
  one recovery sweep, filesystem allocation must be within 1% or 16 MiB
  (whichever is larger) of that unique-extent inventory.
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
- `PERF-03`: for each W16 command separately, both cold and warm series satisfy
  `p95(C) <= 1.05 × p95(B)`. The named interval begins immediately before the
  helper's first read/stat/pread and ends immediately after its last operation
  completes. Sequential hashing is itself the W16 read workload and remains
  inside that interval; setup, cache treatment, and correctness verification
  stay outside it and are identical for B and C.
- `PERF-04`: C squash p95 is no slower than A by more than 5%; current hardlink
  squash is already byte-neutral, so no speedup is presumed.
- `PERF-05`: during a 15-minute W13 window at 100 concurrent agents, C
  throughput is at least 90% of B, every agent completes an operation in every
  60-second window after warm-up, bounded queue occupancy never exceeds its
  configured limit, and there are zero unclassified timeouts or overflows.

## 11. File-blame and transaction proof

Before implementation, freeze raw v1 `file_blame` status, headers, and response
body fixtures. For every relevant workload, capture them before and after
publish, squash, remount, daemon restart, and GC. Compare bytes and exact
`start_line`, `line_count`, and `owner` tuples—not only owner presence. The
explicit comparison allowlist may ignore only `Date` and request-ID header
values; header presence, every other header/value, JSON encoding, ordering, and
body bytes remain exact.

| Case | Expected | A | B | C | Evidence |
|---|---|---|---|---|---|
| mixed-owner OCC merge | exact line ranges preserved | PENDING | PENDING | PENDING | PENDING |
| no-op publish | no new blame event | PENDING | PENDING | PENDING | PENDING |
| live unfinalized write | blame remains last published state | PENDING | PENDING | PENDING | PENDING |
| delete and delete→recreate | v1 output preserved exactly | PENDING | PENDING | PENDING | PENDING |
| rename/copy; empty/binary; trailing newline | v1 characterization fixture preserved | PENDING | PENDING | PENDING | PENDING |
| base-only/absent path | current `NotFound` behavior preserved | PENDING | PENDING | PENDING | PENDING |
| one million sparse owner ranges; 64–256 MiB serialized v1 body | byte-exact whole-array response; spool ≤ body + 16 MiB; anon RSS/PSS delta ≤ 64 MiB | PENDING | PENDING | PENDING | PENDING |
| squash | response byte-identical before/after | PENDING | PENDING | PENDING | PENDING |
| live remount | response byte-identical before/after | PENDING | PENDING | PENDING | PENDING |
| restart | response byte-identical | PENDING | PENDING | PENDING | PENDING |
| crash before visibility commit | neither layer nor blame visible | PENDING | PENDING | PENDING | PENDING |
| crash after visibility commit | both layer and blame visible | PENDING | PENDING | PENDING | PENDING |
| commit succeeded/reply lost/retry | same revision; no duplicate layer/event | PENDING | PENDING | PENDING | PENDING |
| metadata/WAL/checkpoint ENOSPC or I/O failure | old-or-new state; never partial attribution | PENDING | PENDING | PENDING | PENDING |

Mandatory gate `BLAME-01`: every row passes, and no successful v2 publish can
be observed without its matching provenance state. Except for the two allowed
volatile header values, the existing public `file_blame` status, headers, and
body must remain byte-for-byte identical. Internal paging is not permission to
replace or truncate that API. The huge fixture's spool allocation and
baseline-subtracted daemon anonymous RSS/PSS must meet the numeric row. Any
public cursor endpoint is tested only as an additive, separately approved API.

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

No historical idle number is accepted without an environment receipt, raw
samples, command interval, commit, and artifact digest. The current 500 ms
freeze budget and 30 s runner timeout are safety ceilings, not performance
targets.

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
- `MEM-02`: profiler evidence identifies every retained allocation class. From
  1 GiB to 10 GiB, no daemon-retained class outside the declared fixed pools
  may grow by more than 16 MiB, and every request-owned allocation must return
  to zero or its recorded warm baseline within 60 seconds of completion or
  cancellation.
- `MEM-03`: after warm-up and completed cleanup, the Theil–Sen anonymous-RSS
  slope over the final 12 soak hours has a seeded one-sided 95% bootstrap upper
  confidence bound no greater than 1 MiB/hour. Candidate steady anonymous
  RSS/PSS p95 is also no greater than
  `max(A steady p95 + 64 MiB, 1.10 × A steady p95)`.
- `MEM-04`: within 60 seconds of normal cleanup and within five minutes after
  an injected recovery, live leases, staged objects, parked mounts, and queue
  entries return to zero; fds and tasks return to within two of their recorded
  warm baseline and stay there for five minutes.
- `MEM-05`: zero OOM kills, allocator failures, panics, daemon restarts, or
  unexpected health/readiness failures; WAL checkpoints target 64 MiB and WAL
  never exceeds the 256 MiB hard ceiling.
- `MEM-06`: comparing 100,000 with one million events under the same active
  query load, baseline-subtracted steady anonymous RSS/PSS p95 may increase by
  at most 16 MiB for both bounded and growing path sets. Query-owned memory
  returns to the warm baseline plus 16 MiB within 60 seconds; durable DB growth
  is reported separately.
- `MEM-07`: staging, export, recovery, and combined transient allocation never
  exceed the numeric table; one boot sweep returns unreachable transient bytes
  to zero or an explicitly accounted quarantine below its limit.
- `MEM-08`: fill and concurrent-race tests at every high-water reject new work
  before visibility, preserve at least 4 GiB recovery reserve, leave old state
  readable, and recover without bypassing admission or deleting blame. A short
  fault drains rejected/private work and restores its pre-run counters within
  60 seconds; after an ENOSPC injection is removed, recovery completes within
  five minutes. Neither path permits manual DB edits or broad deletion.

## 14. Crash, ENOSPC, and recovery

The committed harness owns a versioned `failpoints-v1.json` registry. Its file
digest is part of every receipt, IDs are immutable, and each row records the
operation/state transition, whether injection occurs immediately before or
after its flushed durable marker, injected failure, required old-or-new state,
content/blame oracle, cleanup owner, and deadline. Every durability transition
listed below must have distinct before/after IDs; an unregistered “during” test
does not count as coverage.

Inject process death and storage failures at every registered durable boundary:

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

Mandatory `RECOVERY-01`: every registry ID has one reviewed receipt. At most
one idempotent client retry is allowed after an uncertain commit. Short
kill/I/O cases must reach their registered invariant within 60 seconds of
restart; ENOSPC cases must do so within five minutes after the injection is
removed and the reserved recovery space is available. Timeout, unbounded retry,
manual metadata editing, or broad deletion fails the gate.

## 15. Gate tables

### 15.1 A-macOS feasibility

| Gate family | Required | Result | Evidence artifact |
|---|---|---|---|
| DOMAIN | one production storage domain and exact production mount options | NOT RUN | PENDING |
| DIRECT CLONE | at least 99% allocated payload shared | NOT RUN | PENDING |
| COW ISOLATION | exact source hash and mutation growth within bound | NOT RUN | PENDING |
| OVERLAY COPY-UP | at least 99% of unchanged allocated payload shared | NOT RUN | PENDING |
| PRIVILEGE/SECURITY | `PRIV-01`; raw and canonical diff empty | NOT RUN | PENDING |
| TEARDOWN | no experiment-owned residue | NOT RUN | PENDING |

A-macOS verdict: **INCONCLUSIVE — NO SEALED PHASE-0 RECEIPT**

### 15.2 Gate B integrated product acceptance

Gate B status: **BLOCKED_NOT_RUN — GLOBAL GATE A AND PRODUCT REQUIRED**

| Gate family | Required | Result | Evidence artifact |
|---|---|---|---|
| REPEATED FEASIBILITY | Phase 0 through integrated `layerstore` and mount builder | BLOCKED_NOT_RUN | PENDING |
| STORAGE | `SPACE-01` … `SPACE-05` | BLOCKED_NOT_RUN | PENDING |
| PERFORMANCE | `PERF-01` … `PERF-05` | BLOCKED_NOT_RUN | PENDING |
| BLAME | `BLAME-01` | BLOCKED_NOT_RUN | PENDING |
| REMOUNT | `REMOUNT-01`, `REMOUNT-02` | BLOCKED_NOT_RUN | PENDING |
| ACTIVE | `ACTIVE-01` … `ACTIVE-03` | BLOCKED_NOT_RUN | PENDING |
| MEMORY | `MEM-01` … `MEM-08` | BLOCKED_NOT_RUN | PENDING |
| CRASH/RECOVERY | `RECOVERY-01` registry complete | BLOCKED_NOT_RUN | PENDING |
| SUPPORTED IMAGES | complete pinned product corpus plus extremes | BLOCKED_NOT_RUN | PENDING |
| TEARDOWN | no experiment-owned residue | BLOCKED_NOT_RUN | PENDING |

Evidence bundle SHA-256: `PENDING`

Reviewer and date: `PENDING`

## 16. Host qualification scope

This document's A-macOS verdict applies only to the pinned macOS Docker Desktop
environment and architecture. Apple Silicon does not prove Intel macOS. The
dedicated experiment repository has three independently owned peer evidence
branches—`macos_experiment`, `windows_experiment`, and `linux_experiment`—which
may execute in parallel and cannot inherit one another's verdict.

Global Gate A is the conjunction of A-macOS, A-Windows, and A-Linux across
every declared host/architecture lane. No LayerStack 2.0 product code starts
until that conjunction passes. Gate B then repeats the shared security,
arbitrary-image, correctness, storage, performance, blame, remount, crash, and
memory suite through the integrated runtime on:

- supported native Linux kernels/filesystems;
- stock Windows Docker Desktop's WSL 2 Linux-container backend; and
- every other host architecture declared supported by the product.

Each host records whether `required`, `preferred`, or only `disabled` is
available. A copy fallback may preserve correctness and universality, but it
does not pass that lane's reflink gate and cannot support a cross-platform
reflink storage/performance claim. Production configuration must never present
one host's successful probe as another host's capability. Every platform
receipt records its branch commit, shared-protocol commit, exact environment
cell, and evidence-bundle SHA-256.

## Appendix A: unverified imported discovery context

The notes below were copied without the branch commit, raw artifact bundle, or
sealed SHA-256 required by this protocol. They are not authoritative results,
do not fill a table, and cannot support `PASS` or `FAIL`. Preserve them only as
leads for a fresh, preregistered Phase-0 run; once a receipt exists, append a new
verified entry rather than converting these notes in place.

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

Imported D1 claim: Docker's default named volume reportedly used filesystem
`ext2/ext3`
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
