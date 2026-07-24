# Stage 11 benchmark note — cumulative qualification and retirement

[Specification](spec.md) · [E2E plan](e2e_test.md) ·
[Overall Stage 03–11 scorecard](../stage_03_11_benchmark_note.md) ·
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Status: **NOT_RUN**

Stage 11 is the only final qualification tier. Candidate default and legacy
retirement are a no-go unless every cumulative Preparation gate is measured
and passes; missing or unavailable required evidence is a failure.

> **Definition guards before timing:** the E2E plan now separates normalized
> end-to-end publication **elapsed-time advantage** from the distinct
> `SeqCDC unique retained ≤1.14× StreamCDC` storage gate. Prep requires enough
> samples for stable p50/p95 but does not freeze an exact time-cell `N`;
> qualification remains `OPEN` until `N` and exclusions are predeclared
> before candidate data.
>
> **Frozen no-op command control:** the baseline operation is direct,
> shell-free `docker exec <container-id> ls` in a fresh ordinary control
> container created for each matched invocation from the pinned OCI/platform
> digest. Its pristine root contents match the candidate view, but it has no
> LayerStack-owned `/eos` root, candidate materialization/mount, root lease,
> session/namespace-holder setup, or public API wrapper. Pull/create/start/
> health/setup are untimed and separately recorded; time the ready control
> only from the Docker exec request through complete exit/status/stdout/stderr
> drain. Pair it with public `exec_command(["ls"])` on matched
> host/filesystem/root contents/cwd/env/Docker allocation/cache class/order/
> output drain. This is raw Docker execution, not bare-host `fork/exec`. The
> Prep gate
> remains independently `candidate≤docker_exec_ls×1.03+0.5 ms` at p50 and
> p95. The separately predeclared stretch target is **at least 80 ms saved**
> at both p50 and p95 and is never rebased or waived if the frozen control is
> faster than 80 ms.

| Required report field | Value frozen before the first candidate sample |
| --- | --- |
| frozen baseline | matched raw LayerStack, StreamCDC, verified native-copy controls, and direct shell-free `docker exec <container-id> ls` in the ready ordinary non-LayerStack control for no-op command; revisions, required host×image rows, corpora, setup exclusion, allocation, cwd/env/stdout drain, cache, order, exclusions, and time-cell `N` fixed |
| required target/cap | every correctness, recovery, dependency, platform, time, selection, distribution, RSS, space, locality, maintenance, resource, and complexity gate in Prep |
| predeclared optimization target (recommended, non-normative) | no-op `exec_command(["ls"])` saves `≥80 ms` versus direct `docker exec <container-id> ls` at both p50 and p95 (never rebase); other latency medians `≤raw`; native throughput `≥1.00×raw`; selection advantage `≥0.15`; mixed/no-dedup settled amplification `≤1.05×D_ideal`; many-small `≤1.10×D_ideal`; RSS overhead `≤96 MiB` while retaining the 384 MiB absolute cap |
| candidate actual | `NOT_RUN` |
| delta / ratio / headroom | `NOT_RUN`; derive only from preserved matched samples |

## Cumulative complexity and resource gates

| Path | Required complexity / bound |
| --- | --- |
| Boundary/chunk/hash | `O(U+K)=O(U)`; fixed count `ceil(U/32KiB)≤K≤ceil(U/8KiB)`; nonempty sub-min file is one actual-length chunk; mean within 5% of 16 KiB |
| Publication | `O(U+E+K)`, external ordering at most `O(E log E)`; ≤4 MiB managed memory/op excluding 16 MiB cache; staging ≤5% of `C_capture` |
| Clean session / warm prepare / mount | clean session `O(D)` plus namespace/mount syscalls and `O(1)` metadata per session; warm prepare/mount `O(D)`, `D≤64`, independent of workspace bytes; zero lower-payload clones and zero CAS payload reads |
| Cold hydrate/activate | `O(R+E)` / `O(R+E+D)`; one target plus ≤5%; never superlinear |
| Squash | build `O(S+E_s)`; frozen interval `O(D+tasks+verified FDs)`; one replacement plus leased old |
| GC/compaction | `O(G)` per bounded slice; one bounded source+target |
| Diff/OCC/blame | `O(Q log N)` plus bounded output |
| Command/file/PTY | Existing native cost; no CDC/CAS/manifest/pack lookup |
| Mount admission | `O(D)` preflight checks both `D≤64` and the exact serialized OverlayFS `lowerdir=` byte limit before any mount syscall |
| Maintenance isolation | packer, squash builder, and GC slice may run concurrently only in the synchronized isolation campaign; command/PTY critical paths have zero maintenance-owned wait/lock/permit/CDC/CAS/manifest/pack work |
| Hard resources | 32 KiB window/ring; ≤2 borrowed slices/chunk and ≤4 chunks global; 4 workers; payload queue 0; metadata queue 16/64 KiB; 256 KiB worker buffers; merge fan-in 8×64 KiB; encoder ≤256 KiB; semaphore 64 MiB |

## Final time and selection gates

All latency bounds apply independently to p50 and p95 against a frozen matched
raw LayerStack baseline.

| Metric | Pass gate |
| --- | --- |
| Warm resolve/session and OverlayFS mount | `candidate≤raw×1.05+2 ms`; zero warm CAS payload reads |
| Frozen remount | `candidate≤raw×1.05+2 ms` |
| Full squash | `candidate≤raw×1.10+5 ms` |
| No-op exec | exact control `docker exec <container-id> ls` in the ready ordinary non-LayerStack container versus public `exec_command(["ls"])`, with setup excluded and matched root contents/cwd/env/allocation/cache/order/output drain; required p50/p95 gate `candidate≤control×1.03+0.5 ms`; separately report stretch target `control-candidate≥80 ms` at both percentiles and never rebase it |
| Native command and sequential file read/write | throughput `≥0.97×raw` |
| PTY create | `candidate≤raw×1.03+1 ms` |
| PTY drain/supported stdin/control-C/control-D | `candidate≤raw×1.03+0.5 ms`; unsupported operations remain deterministically unsupported |
| Concurrent disjoint publication | throughput `≥0.90×raw` with exact OCC |
| Small-edit publication | p95 `≤raw×1.15+5 ms`; record scanned/new bytes |
| Cold hydration / activation | `≥0.70×` native-copy throughput; activation p95 `≤1.5×copy+warm allowance` |

### Frozen scale and maintenance-interference regressions

These cells are normative parts of the Time campaign, not optional plots:

1. **Warm workspace-size independence.** Use prebuilt warm workspaces
   `S∈{64,256,1024} MiB` at fixed `D=16`, one session, identical
   task/verified-FD schedule, image/root, cwd/env, cache class, and zero
   workspace writes. Measure warm resolve/session preparation, mount, and
   no-op exec with at least three excluded warmups and a frozen `N` of
   counterbalanced raw/candidate pairs. For each operation and percentile fit
   the predeclared OLS model
   `latency_ms = α + β_S×log2(S/64MiB)`. Before candidate data, derive and
   freeze the one-sided 95% raw-control slope-noise ceiling from raw
   resamples. The candidate's one-sided 95% upper bound for `β_S` must not
   exceed that ceiling, its structural metadata/syscall/work-counter tuple
   must be identical at all three sizes, and payload reads/copies must be zero.
   Any positive workspace-size term beyond frozen raw noise is a hard failure.
2. **Mount/remount depth slope.** Use `D∈{1,16,48,64}` at fixed warm
   `S=256 MiB`, session count, tasks, verified FDs, mount options, and cache.
   Fit `latency_ms = α + β_D×D` separately to matched raw and candidate p50
   and p95 cell estimates. Use the frozen paired-bootstrap seed, resample
   count, and pairing key to report
   `depth_slope_ratio=β_D,candidate/β_D,raw`; its one-sided 95% upper bound
   must be `≤1.10` for mount and remount. If the raw denominator is
   non-positive or its 95% interval includes zero, the row stays `OPEN`; do
   not substitute a post-hoc statistic.
3. **Maintenance isolation.** For each actor—packer, squash builder outside
   freeze, and one GC slice—prebuild a deterministic backlog, synchronize on
   an explicit `maintenance_active` event, and interleave idle/active no-op
   command and PTY create/drain cells. Use at least three warmups and the same
   predeclared `N`/ordering/exclusions as the matching idle cell. Standard
   command/PTY numeric gates still apply. Additionally, maintenance-owned
   wait, lock, permit, CDC, CAS, manifest, pack, and GC work counters on the
   command/PTY critical path must each be exactly zero.

The raw-control slope-noise ceiling, regression implementation, percentile
estimator, bootstrap method/seed/resamples, `N`, and exclusion policy are
frozen in the plan before any candidate sample. If any is missing, the
corresponding row is `OPEN`, not inferred from a graph.

The normative selection formula is:

```text
seq_ratio_sample    = seqcdc_elapsed / seq_paired_raw_elapsed
stream_ratio_sample = streamcdc_elapsed / stream_paired_raw_elapsed
advantage_sample    = 1 - seq_ratio_sample / stream_ratio_sample
advantage           = median(advantage_sample)
```

Localized-large-source and mixed-tree each require advantage `≥0.10` and a
paired-bootstrap 95% lower bound `≥0.10`. No-dedup and many-small may regress
by at most 3%. Use 3 fresh matched sets, at least 5 interleaved samples per
workload/invocation, and counterbalanced order. Equal distribution means the
same 8/32 KiB min/max, means within 5%, and p10/p50/p90 within 10%.

## Final memory, space, locality, and maintenance gates

| Area | Target / hard gate |
| --- | --- |
| RSS | Every cold point ≤384 MiB absolute and ≤128 MiB above raw idle; matrix 64/256/1,024 MiB × histories 1/16/64 ×3 reps; adjusted final/peak variation ≤16 MiB; no 4× input/history step adds >8 MiB |
| Clean sessions | prebuilt clean workspaces 64/256/1,024 MiB × simultaneous sessions 1/8/32 ×3 repetitions; lower/workspace payload growth and copied payload bytes exactly 0; per-session directories, leases, journals, and their bounded record sizes are constant in workspace bytes; allocated metadata is `≤M0 + N×m_cap` using the same predeclared `M0,m_cap` at all three sizes |
| Settled space | mixed and no-dedup target ≤1.08×`D_ideal`, hard >1.15×; many-small target ≤1.15×, hard >1.25× |
| Duplication/slack | avoidable duplicate target ≤1%, hard >3%; pack dead/slack target ≤2%, hard >5%; persistent unexplained unreachable bytes exactly 0 |
| Metadata/residue | ≤96 B/chunk, ≤64 B/segment reference, ≤256 B+path/changed path; residue ≤`1 MiB+min(1% retained,64 MiB)` and no pending transaction |
| SeqCDC storage | unique retained ≤1.14× StreamCDC on every required corpus |
| Locality | for `F≥16 MiB`, edit ≤64 KiB: target `changed+2×32 KiB+segment overhead`; hard fail if median >4×target or any sample ≥25% of `F` |
| Squash policy | enqueue at projected `D≥48`; compact/reject before `D>64`; routine benefit ≥8; manual selected run contains ≥2 lowers |
| Packs/GC | payload ≤64 MiB, records ≤100,000, allocation ≤80 MiB; compact at ≥20% dead; urgent aggregate >5%; slice ≤100,000 records or 64 MiB; grace ≥1 durable epoch plus final recheck |

No restart, cache purge, `malloc_trim`, allocator swap, sample deletion, or
unreported estimate may manufacture a pass.

## Concrete developer-tiny matrix

This loop is diagnostic only. Use empty/no-op, a localized 1 KiB edit in a
deterministic 1 MiB file, one 1 MiB incompressible file, 256 small files, and
depths 1/8/32. Run one warmup and at least five alternating raw/candidate
samples; `A,B,C,D,A` is the minimum schedule.

| Cell | Control / candidate | Measured samples in minimum | Metrics | Diagnostic pass |
| --- | --- | ---: | --- | --- |
| A — clean/no-op/native | raw versus candidate at `D=1` | 2 pairs | clean-session allocated payload/metadata, warm, mount, exec, file, route, CAS reads | exact behavior; zero lower/workspace payload clone, fallback, or CAS hot read; metadata owner counts constant for the tiny workspace |
| B — localized edit | raw versus candidate, 1 KiB/1 MiB, `D=8` | 1 pair | publish phases, scanned/new bytes, chunks | exact publication and accounting |
| C — incompressible | raw versus candidate, 1 MiB, `D=32` | 1 pair | throughput, peak owned/staging bytes | exact tree and bounded resources |
| D — many-small tiny | raw versus candidate, 256 files, `D=8` | 1 pair | metadata counts/bytes, exec/read, settle | exact metadata and zero leaked owners |

Poll quiescence every 100 ms for at most 5 s. Report raw samples and diagnostic
medians only—never final p95, RSS, space, or selection qualification.

### Developer-tiny wall clock — ESTIMATED, not measured

| Work | Budget |
| --- | ---: |
| fixture/config/setup | 5–8 s |
| warmup | 3–6 s |
| five measured pairs | 14–30 s |
| quiescence/cleanup | 3–8 s |
| artifact/report write | 5–8 s |
| **Total** | **30–60 s** |

## Concrete full-qualification matrix

Pre-generate deterministic inputs outside timed intervals: mixed
≥512 MiB/20,000 files, source ≥256 MiB, no-dedup ≥512 MiB, many-small
≥100,000 files, sparse ≥8 GiB logical, and repeated small/large histories.
Freeze host, image/platform digest, binaries, filesystem, allocation, cache,
corpus/seed/order, background load, and exclusion rules per matched cell.

| Campaign | Controls and cells | Warmups / measured | Required metrics | Pass / fail |
| --- | --- | --- | --- | --- |
| Correctness/recovery | raw/candidate default, rollback, forward restore, mixed-root, target-only restart, failpoints, affected suite, required hosts | 0 / 1 execution per declared deterministic case, failpoint checkpoint, and required-host row | exact tree/metadata, OCC, leases, routes, residue, dependencies/platform | every prerequisite exact before scoring; any missing row fails |
| Time | matched raw/candidate cells for every time/throughput row above; exact ready ordinary non-LayerStack direct `docker exec <container-id> ls` no-op control with setup excluded; warm-size sweep `S=64/256/1024 MiB`; mount/remount depth sweep `D=1/16/48/64`; fixed-`D`, fixed-task/FD frozen-remount cells across prebuilt 16/64/256 MiB targets; synchronized command/PTY under packer/squash-builder/GC activity | ≥3 warmups/cell; exact measured `N` is **OPEN** and frozen before candidate data | every raw sample, p50/p95, MAD, `N`, ops/s, bytes; p99 only at `N≥100`; `β_S`, raw noise ceiling, `β_D`, depth-slope ratio/CI; frozen lower/task/FD counters; critical-path ownership counters | each numeric cap passes; command stretch result reported separately; warm-size term within frozen raw noise; mount/remount slope-ratio upper CI≤1.10; frozen work independent of `S`; every maintenance-owned critical-path counter zero |
| Selection | raw/StreamCDC and raw/SeqCDC; localized source, mixed, no-dedup, many-small | 3 fresh two-invocation matched sets; ≥5 interleaved samples/workload/invocation | elapsed formula, pairing, bootstrap seed/resamples/CI | advantage/guardrail and 95% lower-bound gates pass |
| Distribution | same StreamCDC/SeqCDC matched records | reuse selection samples | min/max/mean/p10/p50/p90/count | exact 8/32 KiB bounds and distribution tolerances |
| Locality | `F≥16 MiB`, edit ≤64 KiB, same matched records | all localized samples retained | changed/new unique/segment overhead/F | target reported; no median or per-sample hard failure |
| RSS | 3 sizes ×3 histories × raw/candidate ×3 independent reps = **54 invocations** | equal warmup per invocation / bounded 100 ms stream | idle/final/peak/slope, logical owners, source/scope | every absolute, adjusted, scale, release, and slope gate |
| Space | required corpora/histories; allocated `L_hot,H_cold,ΣU_active,P_staging,M`; separate prebuilt clean-workspace 64/256/1,024 MiB × session-count 1/8/32 matrix | 3 settled repetitions/cell | pre/peak/visible/settled/restart bytes, `D_ideal`, amp, metadata, residue; clean-session lower reads/copies, payload allocation, directory/lease/journal counts and bytes | every target/hard bound; unexplained bytes 0; clean-session payload growth exactly 0 and metadata is `≤M0+N×m_cap` with the same predeclared caps at every workspace size |
| Maintenance | exact 20%/5%/2%, depth 47/48/63/64/65, routine benefits 7/8, manual selected-run widths 1/2, serialized `lowerdir=` at `L_limit-1/L_limit/L_limit+1`, pack/slice caps, evacuation/grace/restarts, and the complete GC root/selector matrix below | exact boundary case once plus frozen restart and selector-removal variants | depth/carriers/serialized option bytes/mount syscalls, records/allocated/live/dead/leases/epochs, squash build/commit/frozen/remount/**evacuation** time, selector/root decisions | every threshold, byte/count cap, last-locator, selector, evacuation, and grace rule; over-limit lowerdir rejected before mount |
| Portability | every compatible required host × pinned image fixture × runtime variant: Ubuntu glibc, Debian glibc, Alpine musl, minimal/distroless, shell-less; read-only root and non-root variants | one deterministic capability execution per frozen row; each leaf invocation ≤5 min | OCI index and resolved platform manifest, architecture, root/config, mount/xattr/security, writable provider `/eos`, public storage/workspace/file/recovery results, helper/process/download inventory | every required row executed; no target userland dependency; a missing digest, unavailable manifest, or unexecuted compatible row fails |

The Maintenance campaign uses this complete reachability matrix. Strong
manifest edges always retain referenced manifests, metadata, and objects.
Parent/base ancestry is weak and is retained only when selected independently
by each of: durable lease, explicit pin, active branch, configured history
window, migration frontier, in-flight transaction, and pending transaction.
A separate materialization-record row retains its carrier and locator set even
when no weak ancestry selector applies. For every weak selector, first run
with only that selector present, then remove only it and prove collection
occurs only after one complete durable epoch plus final root/generation/lease
recheck. Also run an unselected weak-ancestry control. Missing any selector or
collapsing selectors into one combined case is a failure.

For time cells, the recommended **non-normative** default is at least 100
measured matched samples per cell across at least 3 fresh invocations. If that
cannot fit the invocation constraint, freeze a different fixed `N`, stability
rule, and exclusion policy before candidate data. Otherwise the cell remains
`OPEN` and Stage 11 cannot qualify.

Every operation is ≤60 s. Every matched pair/invocation and every capability
matrix leaf is ≤5 min; each RSS
raw or candidate point has its own ≤5 min invocation. Campaigns are sequential
and samples are never silently dropped, except that the maintenance-isolation
cell intentionally overlaps exactly one named background actor with its
command/PTY probe using event synchronization. No two top-level campaigns
overlap.

### Frozen Phase 1 image matrix

The image manifest is part of qualification, not a post-Phase-1 extension.
Every row must contain an exact OCI index digest and an exact platform manifest
for each compatible required architecture before it can run. `OPEN` below is
an explicit pre-run blocker and is never replaced by a tag-only result.

| Required fixture class | Repository/tag selection | OCI index | linux/amd64 manifest | linux/arm64 manifest | Required variants |
| --- | --- | --- | --- | --- | --- |
| Ubuntu glibc | `ubuntu:24.04` | `sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` | `sha256:52df9b1ee71626e0088f7d400d5c6b5f7bb916f8f0c82b474289a4ece6cf3faf` | `sha256:7f622ca8766bccb22f04242ecb6f19f770b2f08827dc4b8c707de5e78a6da7ab` | normal, read-only root, non-root |
| Debian glibc | `OPEN — release owner selects and freezes exact repository/tag` | `OPEN` | `OPEN` | `OPEN` | normal, read-only root, non-root |
| Alpine musl | `OPEN — release owner selects and freezes exact repository/tag` | `OPEN` | `OPEN` | `OPEN` | normal, read-only root, non-root |
| Minimal/distroless | `OPEN — release owner selects and freezes exact repository/tag` | `OPEN` | `OPEN` | `OPEN` | normal, read-only root, non-root |
| Shell-less | `OPEN — deterministic OCI fixture recipe and repository/tag must be frozen` | `OPEN` | `OPEN` | `OPEN` | no shell/userland helper; read-only root; non-root |

Each cell validates a Linux OCI rootfs/config, supported architecture,
provider mount/xattr/security behavior, and writable provider-owned `/eos`
even when the image root is read-only. The product may not require target
shell, libc, package manager, checksum utility, or any other userland helper.
If a command executable is absent in the minimal or shell-less fixture, that
specific command fails with the documented public error while storage,
workspace, file, publication, mount, and recovery cases still pass.

### Full qualification wall clock — ESTIMATED planning only

Corpus throughput, frozen time-cell `N`, space-history cells, and required-host
runner count prevent a normative fixed total. `OPEN` below is intentional.

| Campaign | Setup | Warmups | Measured work | Quiescence/cleanup | Reporting | Estimated total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Correctness/recovery/default/rollback | 15–30 min | 5–15 min | 30–90 min | 10–30 min | 10–20 min | 70–185 min |
| Time | 15–30 min | **OPEN** with `N` | **OPEN**; `cells×invocations×≤5 min` envelope | 10–30 min | 15–30 min | **OPEN**; provisional 1.5–4 h only after `N` freezes |
| Selection | 15–30 min | 10–30 min | 45–120 min; 24 workload-invocations, timeout envelope ≤120 min | 10–30 min | 10–20 min | 90–230 min |
| Distribution/locality | reused | reused | reused selection samples | 5–10 min | 10–20 min | +15–30 min analysis |
| RSS | 20–40 min | 30–60 min | 135–270 min for 54 invocations | 20–45 min | 20–40 min | 225–455 min |
| Space | 15–30 min after pre-generation | 0–15 min | **OPEN**, provisional 60–240 min | 20–60 min | 15–30 min | **OPEN**, provisional 2–6 h |
| Maintenance | 10–20 min | 5–10 min | 20–60 min | 10–20 min | 10–20 min | 55–130 min |
| Required host×image capability matrix | per runner/fixture | per row | `compatible host×image×variant cells×≤5 min`; row count dependent | per row | 10–30 min aggregate | **OPEN** until every digest, compatible row, and runner is frozen |

A provisional single-runner local aggregate is roughly **11–27 runner-hours**
after inputs are pre-generated, plus the required host×image capability
matrix. This is not a commitment or gate; the authoritative total remains
**OPEN**.

The typed E2E `qualification.time`, `.rss`, and `.space` nodes are bounded
control-plane plan validators/dispatchers, and `qualification.all` is a
bounded completed-artifact validator. Their 60–300 second timeouts cover
schema validation, dispatch/resume acknowledgement, and bundle checks only;
they never execute or await an 11–27-hour campaign inline. The scheduler
persists a run ID for every dispatched leaf, each leaf has its own ≤5-minute
invocation and ≤60-second operation limits, and final qualification reruns the
artifact validators only after all leaf bundles are terminal. Dispatch
success is not a performance pass.

## Raw evidence and arrival checkpoint

Every record carries baseline/candidate revisions and dirty state, binary and
config digests, host/runtime/image/platform, CPU/memory/storage allocation,
kernel/filesystem/mount/xattr, corpus/seed/cache/order, raw values,
`measured|derived|estimated|unknown` provenance, and rejection reason. Preserve
immutable per-sample run/observation artifacts and full resource/physical-space
streams; missing gating data is never zero.

The raw bundle also carries the exact command-control argv/container/root/cwd/
env/cache/stdout-drain tuple; warm-size and depth regression inputs,
coefficients, raw noise ceiling, confidence intervals, and frozen statistical
configuration; maintenance-active event intervals and critical-path owner
counters; serialized-`lowerdir` limit/bytes/preflight/mount-syscall evidence;
every GC root/selector decision; and squash build, commit, frozen, remount, and
evacuation nanoseconds. Evacuation starts at release of the final protecting
old-carrier lease and ends when replacement locators are durable and the
source is grace-eligible, or is exactly zero with a closed no-evacuation
reason.

Stage 11 has not arrived until
`.benchmark-state/results/<run-id>/stage-11-perf-report.json` and
`stage-11-perf-report.md` exist with
`schema_version="phase1.stage11.perf-report.v1"` and adjudicate every Prep
gate: frozen baseline actuals, required pass targets/caps, separately
predeclared optimization targets, candidate actuals, deltas/ratios/headroom,
complexity/work counters, memory/RSS, complete physical-space terms,
correctness/recovery/dependency/platform prerequisites, links between the
reports and to run/raw artifacts, provenance, and one terminal verdict.
`QUALIFIED` is allowed only if every required gate passes; any miss or
unverified row yields `FAIL`. A pre-arrival draft may remain `OPEN`, but
`OPEN` is never an arrival or retirement decision.

The first Markdown table must show the frozen baseline actual, required pass
target/cap, separately predeclared optimization target, candidate actual,
delta/ratio, headroom, and verdict for every Prep metric.

## Append-only progress

Before each live command, append exact command, commits, intended cases,
expected custody/evidence, and cleanup to
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`.
Afterward append `Good` or `Defect`, artifact IDs, exact misses, and cleanup;
append later `Fix` and `Rerun` entries rather than rewriting history. Update
the overall scorecard and append a row here only after immutable reports exist.

| UTC | State | Run ID | Baseline → candidate actual | Required / optimization target | Delta / ratio / headroom | Report / raw artifacts | Cleanup / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | NOT_RUN | — | — | — | — | — | Freeze time-cell `N`, exclusions, and first campaign before execution |
