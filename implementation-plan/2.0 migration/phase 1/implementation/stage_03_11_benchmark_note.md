# Phase 1 Stage 03–11 benchmark scorecard

[Implementation index](index.md) ·
[Preparation 01](../prep/01-cdc-cas-space-time-materialization-spec.md) ·
[Preparation 02](../prep/02-storage-solution-examination-review.md) ·
[Preparation 03](../prep/03-seqcdc-cas-and-squash-decision.md) ·
[Preparation 04](../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Status: **PROPOSED / NOT RUN**

This is the common speed, space, memory, and complexity scorecard for
Stages 03–11. Each stage also has a small `benchmark_note.md` containing its
local loop and progress ledger. Preparation 04 is normative; Preparation 01
still governs where it is stricter. Correctness, durability, recovery,
dependency, architecture, and portability failures invalidate performance
results even when they are not repeated in this note.

## 1. How to set numeric targets

The no-op command comparator is fixed even though its measured p50/p95 values
do not exist yet: direct, shell-free `docker exec <container-id> ls`. For each
matched invocation, start a fresh ordinary Docker control container from the
same pinned OCI index/platform digest used to seed the candidate root. Its
visible pristine root and working directory must be byte- and
metadata-equivalent to the candidate view, but it must have no LayerStack-owned
`/eos` root, candidate materialization, lower/upper/work mount, root lease,
session/namespace-holder setup, or public API wrapper. Pull, create, start,
health, and fixture setup are untimed and recorded separately; the control
container is already running before samples begin. The timed control starts
immediately before the Docker exec request and ends only after exit status,
stdout, and stderr are fully drained.

Pair that raw Docker control with public `exec_command(["ls"])` using the same
host, filesystem, root contents, working directory, environment, Docker
CPU/memory allocation, cache class, arm ordering, and output-drain rule. This
is the raw Docker execution-floor comparator, not a bare-host `fork/exec`
baseline. The separately predeclared optimization target is a saving of at
least 80 ms at both p50 and p95. It never substitutes for the Prep regression
cap and is never rebased if the control is faster than 80 ms.

Do not invent absolute baseline values or absolute targets for the other
operations. Freeze each named control on the same environment and corpus,
then calculate every percentile independently:

```text
latency_cap_ms = raw_ms × (1 + allowed_percent) + floor_ms
delta_ms       = candidate_ms - raw_ms
headroom_ms    = latency_cap_ms - candidate_ms
throughput     = candidate_rate / raw_rate
```

Symbolic calculations, not measured values:

| Baseline symbol | Normative candidate cap | Separate optimization interpretation |
| --- | ---: | --- |
| direct `docker exec … ls` in a ready, ordinary, non-LayerStack control container = `B_exec` | `B_exec×1.03+0.5 ms` | separately test `candidate_exec≤B_exec-80 ms`; report a miss/impossibility if `B_exec<80 ms` |
| warm materialization = `B_warm` | `B_warm×1.05+2 ms` | any stricter target is frozen before candidate data |
| small-edit publication p95 = `B_publish` | `B_publish×1.15+5 ms` | report the signed candidate-minus-baseline delta and cap headroom |

The one Prep-authored mandatory speed improvement is integrated SeqCDC publication:
at least 10% over the internal StreamCDC comparator at equal chunk
distribution. Most other time gates are regression ceilings; the command
80 ms saving is an additional predeclared optimization target.

## 2. Progress tracker

Allowed states are `NOT_RUN`, `RUNNING`, `OPEN`, `DIAGNOSTIC_PASS`, `FAIL`,
and `QUALIFIED`. `OPEN` means a required target, sample, or counter is still
missing and blocks arrival. `QUALIFIED` is reserved for Stage 11 after every
cumulative Prep gate passes. A Stage 03–10 local pass is never final
qualification.

Keep the last three columns synchronized from the latest immutable Markdown
report. They intentionally show `—` while no benchmark has run.

| Stage note | Owner outcome | Status | Baseline → candidate actual | Required / optimization target and headroom | Latest report |
| --- | --- | --- | --- | --- | --- |
| [03](stage_03_streaming_seqcdc/benchmark_note.md) | bounded, exact SeqCDC primitive | NOT_RUN | — | — | — |
| [04](stage_04_shadow_cas_ingest/benchmark_note.md) | metadata-only shadow ingest | NOT_RUN | — | — | — |
| [05](stage_05_candidate_materialization/benchmark_note.md) | private cold/warm materialization | NOT_RUN | — | — | — |
| [06](stage_06_strict_candidate_activation/benchmark_note.md) | strict native candidate activation | NOT_RUN | — | — | — |
| [07](stage_07_durable_publication/benchmark_note.md) | durable/OCC candidate publication | NOT_RUN | — | — | — |
| [08](stage_08_retention_gc_packs/benchmark_note.md) | bounded retention, packs, and GC | NOT_RUN | — | — | — |
| [09](stage_09_identity_preserving_squash/benchmark_note.md) | identity-preserving squash | NOT_RUN | — | — | — |
| [10](stage_10_candidate_authority/benchmark_note.md) | candidate authority and soak | NOT_RUN | — | — | — |
| [11](stage_11_qualification_retirement/benchmark_note.md) | complete qualification and retirement decision | NOT_RUN | — | — | — |

## 3. Stage ownership and tiny experiments

| Stage | What this stage must prove | Frozen local experiment | Local exit |
| --- | --- | --- | --- |
| 03 | Exact author-v1 cuts; `O(U+K)=O(U)`; one 32 KiB ring; at most two borrowed slices; zero payload queue; scalar core at most 300 physical non-test Rust lines | Empty, boundary, localized edit, incompressible, small-file, source-like, fragmentation, and depths 1/8/32; exactly 1 warmup + 5 alternating oracle/candidate pairs | Exact oracle equality, monotonic scan, chunk-count bounds, caps, dependency check; no publication, materialization, mount, command/file/PTY, or squash claim because every candidate runtime path is still absent |
| 04 | Normal shadow ingest `O(U+K+C+V_delta)` plus bounded changed-event ordering, `O(B)` memory, and zero candidate payload copies | Separately label `O(R+E)` bootstrap; then same-byte legacy/shadow cells with exactly 1 warmup + 5 counterbalanced pairs; hold `U,C,K` fixed while scaling unchanged prior-tree/history cardinality | Exact candidate metadata/IDs, payload writes and work staging exactly zero, all queue/cache/permit caps, terminal residue; no hidden prior-tree scan or full-tree rewrite |
| 05 | Exact crash-atomic hydration; warm ensure is metadata-only; cold `O(R+E+K)=O(R+E)` | 2 warmup + 6 alternating pairs; force cold generation, verify, then warm ensure; include cancellation and 12 lifecycle observations with 100 ms polling for at most 5 s | Exact tree, warm CAS payload reads zero, candidate peak at most `C_target+5%`, buffers/resources release; 70% throughput is diagnostic here |
| 06 | Candidate route is strict with `fallback_count=0`; clean sessions clone zero payload and use `O(1)` metadata; warm/mount `O(D)`, `D≤64`; command/file/PTY stay native | 2 warmup + 6 pairs alternating cold/warm generations; exercise exec, sequential file I/O, PTY/stdin/control-C/control-D, unsupported PTY operations, and cancellation; separately sweep prebuilt 64/256/1,024 MiB clean workspaces × sessions 1/8/32 | Exact output and semantics, no legacy fallback, clean payload growth zero, metadata is `≤M0+N×m_cap` using workspace-size-independent predeclared caps, warm payload reads zero, hot-path CDC/CAS/manifest/pack work zero, resource caps |
| 07 | Durable idempotent publication, per-branch OCC, `O(U+K+C+V_delta)`, diff/OCC `O(Q log N)`, bounded publication peak | 2 warmup + 6 pairs; retry the same request, run disjoint branches, conflict one branch, and pre-commit cancel; verify each private root; 12 lifecycle observations | Receipt/root identity, exact OCC, scanned/hashed/reused/new-byte accounting, peak `C_capture+≤5%`, no pending transaction |
| 08 | Bounded packs, retention, evacuation, GC, last-locator safety, and terminal ownership | Deterministic ~16 MiB tree, depths 1/8/32, current/pinned/leased/unreachable states, 20% and 5% boundaries; 1 warmup + ≥5 pairs; 3 warmups + 20 long-lived cycles | Exact pack/slice/grace thresholds, unexplained persistent bytes zero, logical release; final amplification/RSS remains Stage 11 |
| 09 | Squash preserves logical/publication identity; build `O(S+E_s)`; frozen work is `O(D+tasks+verified FDs)` and independent of payload bytes; count and serialized-`lowerdir=` admission; depth/benefit policy | ~16 MiB tree; depths 8/47/48/63 and policy-only 64/65; serialized `lowerdir=` at `L_limit-1/L_limit/L_limit+1`; sessions 1/4; benefits 7/8 and selected widths 1/2; fixed-`D` 16/64/256 MiB remount; synchronized command/PTY idle versus squash-builder active; 1 warmup + ≥5 pairs; 3+20 lifecycle cycles | Root/publication unchanged, materialization generation advances, correct count/byte thresholds, zero frozen payload work and command/PTY maintenance critical-path counters, bounded replacement/lease overlap, and build/commit/frozen/remount/evacuation evidence |
| 10 | Exactly one candidate publication authority, strict candidate reads, ordered verified legacy shadow, explicit rollback | ~16 MiB tree, depths 1/8/32, roots 1/8; 1 warmup + ≥5 pairs; authority sentinel 3 warmups + 20 cycles including retry/read/exec/maintenance/rollback | Authority/route exact, shadow caught up, fallback/mismatch zero, bounded recovery and quiescence; no retirement claim |
| 11 | Every cumulative Prep time, throughput, complexity, memory, RSS, space, locality, maintenance, selection, portability, and evidence gate | Run separate frozen time, selection, distribution, locality, RSS, space, maintenance, recovery, dependency, and full compatible host×Ubuntu/Debian/Alpine/minimal-or-distroless/shell-less×variant campaigns | Only `QUALIFIED` when all gates pass, every exact OCI index/platform digest is present, and every required value exists |

Every measured operation must finish in at most 60 seconds and every leaf
cell or final matched invocation in at most five minutes. Aggregate E2E nodes
may use 60–300 s control-plane timeouts only to validate plans,
dispatch/resume leaf run IDs, and validate completed immutable artifacts.
Dispatch success is never a qualification pass.

### Estimated full tiny-cycle duration

These are **ESTIMATED planning values**, not performance evidence. They assume
an already-built daemon/probe, a locally available pinned image, pre-generated
tiny corpus, and no defect/retry. Cold builds, image pulls, and corpus
generation are recorded separately. “Full arrival bundle” includes setup,
warmup, measured work, required lifecycle/recovery sentinel, quiescence,
cleanup, validation, and report writing. It may comprise multiple invocations;
each matched invocation still remains at most five minutes. Each arrival
report replaces the estimate with actual phase times.

| Stage | Core developer loop | Required extension | Estimated full arrival bundle |
| --- | ---: | ---: | ---: |
| 03 | 30–50 s | included opposing-slope/jump, error, and release cells | **30–50 s** |
| 04 | 30–49 s | 30–90 s recovery + two 90–210 s transaction-failpoint shards | **240–559 s** |
| 05 | 31–55 s | 90–220 s recovery + two 80–200 s failpoint shards + 75–150 s lifecycle | **356–825 s** |
| 06 | 31–55 s | 75–180 s fail-closed + 60–150 s lifecycle + 75–180 s clean-space sweep | **241–565 s** |
| 07 | 38–59 s | 75–180 s lifecycle/recovery | **113–239 s** |
| 08 | 38–60 s | 162–424 s lifecycle/recovery + 205–410 s exact cap-boundary extension | **405–894 s** |
| 09 | 30–60 s | 12–24 s frozen-size sweep + 10–25 s lowerdir/isolation/evacuation cells + 35–72 s 20-cycle sentinel | **87–181 s** |
| 10 | 30–60 s | 35–72 s 20-cycle sentinel | **65–135 s** |
| 11 developer tiny | 30–60 s | full qualification below | **30–60 s** |

Run serially, the complete Stage 03–10 arrival bundles are estimated at
**1,537–3,448 seconds (25.6–57.5 minutes)** before defect reruns, builds, image
pulls, corpus generation, or Stage 11 qualification.

Stage 11 full qualification is not the developer tiny cycle. Its current
non-normative local planning estimate is **11–27 runner-hours**, plus the full
required compatible host×image×variant matrix, and remains `OPEN` until the
time-cell sample count, measured corpus throughput, space-history cells,
exact non-Ubuntu image digests, compatible matrix row count, and runner
availability are frozen. The
selection and RSS matrices alone reserve up to 30 minutes per workload and
270 minutes respectively when every allowed five-minute invocation is
consumed; time, space, maintenance, recovery, and platform campaigns are
additional.

## 4. Final time and throughput register

These are Stage 11 gates. Earlier owning stages should draw the same lines as
diagnostic alerts, but cannot claim the percentile result.

| Metric | Exact final gate | Component evidence owner |
| --- | --- | --- |
| warm root resolve/session preparation | p50 and p95 `≤ raw×1.05+2 ms`; zero CAS payload reads | 05–06 |
| OverlayFS mount | p50 and p95 `≤ raw×1.05+2 ms` | 06 |
| squash frozen remount | p50 and p95 `≤ raw×1.05+2 ms` | 09 |
| full squash plan/build/commit | p50 and p95 `≤ raw×1.10+5 ms` | 09 |
| no-op `exec_command(["ls"])` | exact direct shell-free `docker exec <container-id> ls` in the ready ordinary non-LayerStack control defined in §1, with setup excluded and matched root contents/cwd/env/allocation/cache/order/output drain; required p50/p95 `≤control×1.03+0.5 ms`; separately report `control-candidate≥80 ms` at both percentiles and never rebase | 06, final 11 |
| warm workspace-size slope | `S=64/256/1024 MiB`, fixed `D=16`; candidate one-sided 95% upper bound for `β_S` in `latency=α+β_S×log2(S/64MiB)` does not exceed frozen raw-noise ceiling; identical structural counters and zero payload | 05–06, final 11 |
| mount/remount depth slope | `D=1/16/48/64`, fixed `S=256 MiB`; paired-bootstrap one-sided 95% upper bound `β_D,candidate/β_D,raw≤1.10`; invalid raw denominator stays `OPEN` | 06, 09, final 11 |
| command/PTY under maintenance | synchronized idle/active cells for packer, squash builder, and GC; normal latency gates plus every maintenance-owned critical-path counter exactly zero | 08–09, final 11 |
| native command throughput | `≥0.97× raw` | 06 |
| PTY create | p50 and p95 `≤ raw×1.03+1 ms` | 06 |
| PTY drain, supported stdin, control-C/control-D | p50 and p95 `≤ raw×1.03+0.5 ms` | 06 |
| unsupported resize/arbitrary signal/literal EOF | same deterministic unsupported result; do not score as implemented | 06 |
| native sequential file read/write | `≥0.97× raw` | 06 |
| concurrent disjoint publication | `≥0.90× raw` with exact OCC | 07 |
| small-edit publication | p95 `≤ raw×1.15+5 ms`; report scanned/new bytes | 07 |
| cold hydration | `≥0.70×` verified same-filesystem native sequential-copy throughput | 05 |
| cold activation | p95 `≤1.5×` native-copy control + warm-mount allowance | 05–06 |
| SeqCDC selection | median integrated publication advantage `≥0.10`; paired-bootstrap 95% lower bound `≥0.10` | 03–04, final 11 |

Hard failures include warm latency growing with workspace bytes, any warm CAS
payload read, mount/remount depth slope more than 10% worse than raw, storage
maintenance in a command/PTY critical path, superlinear hydration,
monotonically worsening equivalent settled cycles, or any operation over
60 seconds.

Freeze the OLS implementation, percentile estimator, raw slope-noise ceiling,
pairing key, bootstrap method/seed/resample count, measured `N`, and exclusions
before candidate data. Missing inputs leave the row `OPEN`; graphs or post-hoc
statistics cannot close it.

The selection metric is elapsed end-to-end publication, not saved bytes:

```text
seq_ratio    = seqcdc_elapsed / seq_paired_raw_elapsed
stream_ratio = streamcdc_elapsed / stream_paired_raw_elapsed
advantage    = median(1 - seq_ratio / stream_ratio)
```

Large-source localized-edit and mixed-tree workloads each require
`advantage≥0.10`. No-dedup and many-small may regress by at most 3%. Use three
fresh matched invocation sets, at least five interleaved samples per workload
per invocation, counterbalanced order, and the 95% lower-bound rule. Equal
distribution requires the same 8/32 KiB bounds, means within 5%, and
p10/p50/p90 each within 10%. Unique retained payload is a separate gate:
SeqCDC must be `≤1.14×` StreamCDC on every required corpus.

## 5. Complexity and bounded-memory register

| Operation | Required complexity / independence |
| --- | --- |
| SeqCDC | scan/hash `O(U)`, descriptors `O(K)`, combined `O(U+K)=O(U)`; `ceil(U/32KiB)≤K≤ceil(U/8KiB)` |
| first import | `O(R+E)` with bounded memory; labeled and excluded from normal incremental samples |
| incremental publication | `O(U+K+C+V_delta)` plus changed-event ordering up to `O(C log C)`; no scan/rewrite proportional to unchanged tree/history size and no complete tree/history/chunk list in memory |
| warm creation/materialization/mount | `O(D)`, `D≤64`, independent of workspace bytes, zero CAS payload reads |
| clean session creation | `O(D)` plus namespace/mount syscalls; zero lower/workspace payload clone; `O(1)` constant-size directories and lease ref per session, independent of merged workspace bytes |
| cold hydration / activation | `O(R+E)` / `O(R+E+D)`; never superlinear |
| command/file/PTY | existing native cost; no CDC, manifest, pack, or CAS lookup |
| small edit | one-byte edit may still be `O(F)` because OverlayFS copy-up is allowed; record `F`, scanned, and new bytes |
| squash | build `O(S+E_s)`; frozen interval `O(D+tasks+verified FDs)` |
| evacuation / GC / compaction | linear in bytes whose last locator moves / `O(G)` per bounded slice |
| diff/OCC/blame | `O(Q log N)` plus bounded output |
| recovery | pending common transactions plus bounded cursors only; never all history |

Big-O is proven by structure plus counters, not tiny-loop elapsed time. Stage 04
must record prior-tree entries/pages read. With `U,E_changed,K` held fixed,
work that grows with unchanged current-tree/history cardinality does not prove
the claimed incremental bound. Each stage must freeze any numeric work-counter
coefficient before viewing candidate data; an unspecified coefficient is
reported as `OPEN`, not passed.

Hard resource limits:

| Resource | Limit |
| --- | ---: |
| SeqCDC window / per-publication-worker ring | 32 KiB each |
| borrowed payload | one chunk/worker; at most 4 globally |
| storage data-plane/background workers | 4 globally |
| downstream payload queue | 0 bytes |
| metadata queue | 16 descriptors and at most 64 KiB serialized |
| pack-read / hydration-output buffer | 256 KiB per worker each |
| external merge | fan-in 8; 64 KiB reader per run |
| manifest/journal encoding | at most 256 KiB per admitted operation |
| shared index cache | 4,096 × 4 KiB = 16 MiB |
| managed publication memory | at most 4 MiB excluding shared cache |
| global storage-owned semaphore | 64 MiB |
| native lower depth | at most 64 |
| qualification RSS | at most 384 MiB absolute and 128 MiB above idle raw |

The cold RSS matrix is input 64/256/1,024 MiB × history 1/16/64 roots × three
repetitions per point. Adjusted median final and peak RSS may vary at most
16 MiB across the full series; no 4× input or history increase may add more
than 8 MiB. Every point must satisfy both absolute RSS caps.

## 6. Physical-space and maintenance register

Measure allocated physical bytes, never logical file length alone:

```text
T(t)    = L_hot + H_cold + ΣU_active + P_staging + M
D_ideal = C_current + H_unique
amp     = T_settled / D_ideal
```

Settled qualification excludes dirty unpublished sessions. Report clean
upper/work directories separately.

| Metric | Target | Hard failure |
| --- | ---: | ---: |
| clean-session payload growth | exactly 0 bytes across 64/256/1,024 MiB workspaces ×1/8/32 sessions | any lower/workspace payload clone or nonzero payload allocation |
| clean-session metadata | allocated bytes `≤M0+N×m_cap` with predeclared caps and constant directory/lease/journal record counts at every workspace size | any workspace-byte-dependent term or cap breach |
| mixed tree amplification | `≤1.08×D_ideal` | `>1.15×` |
| no-dedup amplification | `≤1.08×D_ideal` | `>1.15×` |
| many-small amplification | `≤1.15×D_ideal` | `>1.25×` |
| avoidable native+pack duplicate | `≤1%` | `>3%` |
| pack dead/slack after compaction | `≤2%` | `>5%` |
| unexplained unreachable/unleased payload | 0 bytes | any persistent bytes |
| native depth | preemptively below 64 | above 64 |
| serialized `lowerdir=` admission | accept exact byte length through `L_limit`; reject `L_limit+1` before mount, independently of layer count | missing boundary evidence or any over-limit mount syscall |

Publication permits one `C_capture` plus staging at most 5% of
`C_capture`. Hydration permits one `C_target` plus at most 5%. Squash permits
one replacement plus leased old carriers. Compaction permits one bounded
source and target. ENOSPC must fail before visibility without deleting
authoritative input.

Metadata is at most 96 B/chunk, 64 B/segment reference, and
256 B + canonical path bytes/changed path. Settled journal/recovery residue is
at most `1 MiB + min(1% retained payload, 64 MiB)` with no pending transaction.

For a CDC-friendly file `F≥16 MiB` and localized change `≤64 KiB`:

```text
new_unique target ≤ changed + 2×32 KiB + measured segment overhead
```

The algorithm hard-fails if the corpus median is over 4× that target or any
sample is at least 25% of `F`.

Maintenance limits are: autosquash enqueue at projected depth `≥48`;
compact/reject before depth would exceed 64; routine squash benefit at least
8 carriers and a manual selected run containing at least 2 lowers; sealed pack at most 64 MiB payload,
100,000 records, and 80 MiB allocation; individual compaction at 20% dead;
aggregate urgent trigger above 5%; one transaction at most 100,000 records or
64 MiB; deletion grace at least one complete durable epoch plus final
root/generation/lease checks.

Mount preflight tests the exact serialized `lowerdir=` value at
`L_limit-1`, `L_limit`, and `L_limit+1`, crossed with independent layer-count
boundaries. Squash reports build, commit, frozen, remount, and evacuation
intervals separately. Evacuation begins when the installed replacement makes
old carriers eligible and ends only after required last locators move, the
cursor is durable, and old carriers are lease-safe for their next state.

The final GC matrix always follows selected-root manifest, metadata, segment,
and chunk references as strong edges. It tests parent/base ancestry
independently under each weak selector—durable lease, pin, active branch,
configured history window, migration frontier, in-flight transaction, and
pending transaction—plus an unselected control. A separate materialization
record retains its required carriers and locators. Remove each sole weak
selector independently and prove collection only after the durable grace
epoch and final root/generation/lease/locator recheck.

## 7. Final corpus and sampling plan

Pre-generate deterministic inputs outside timed intervals:

- mixed tree: at least 512 MiB and 20,000 files;
- large source: at least 256 MiB deterministic line records;
- no-dedup: at least 512 MiB pseudorandom bytes;
- many-small: at least 100,000 files;
- sparse: at least 8 GiB logical with bounded allocated extents;
- repeated small-file and repeated large-file histories.

Freeze the Phase 1 portability matrix across every compatible required host
and exact-digest Ubuntu/Debian glibc, Alpine musl, minimal/distroless, and
shell-less fixture, including normal, read-only-root, and non-root variants.
Normative performance remains on pinned Ubuntu. Any missing required OCI
index, resolved platform manifest, or executed capability leaf is a no-go.

Normative time campaigns require at least three warmups and enough
counterbalanced pairs for stable p50/p95, but the current plan does not define
an exact `N`. Before the first candidate result, freeze the count and exclusion
rule. The recommended, non-normative default is 100 measured matched samples
per latency cell across at least three fresh counterbalanced invocations.
If that cannot fit the five-minute invocation constraint, predeclare a fixed
alternative before observing candidate data; otherwise the cell stays
`OPEN`/unqualified. Report p99 only when `N≥100`, and always report p50, p95,
MAD, `N`, operations/s, and bytes.

Each RSS point gets its own raw and candidate invocation, repeated three
times. Selection uses one raw/StreamCDC invocation and one raw/SeqCDC
invocation; repeat the two-invocation set three times. Stage 11 uses three
settled repetitions for each space cell.

## 8. Required performance report at every stage arrival

A stage is not considered reached merely because its functional tests pass.
Its E2E implementation task must also create:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/
  .benchmark-state/results/<run-id>/
    stage-XX-perf-report.json
    stage-XX-perf-report.md
```

The JSON is the versioned machine-readable authority; Markdown is a generated
human checkpoint. Stages 03–10 may report `DIAGNOSTIC_PASS` or `FAIL`.
Stage 11 is the only report allowed to say `QUALIFIED`.

Use `schema_version="phase1.stageXX.perf-report.v1"`. A pre-arrival draft may
be `OPEN`, but an `OPEN` report never satisfies stage exit. The Markdown
report begins with one human-readable comparison table:

| Metric | Frozen baseline | Required target/cap | Predeclared optimization target | Candidate actual | Delta / ratio | Headroom | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| stage-owned metric | value + unit | formula + computed value | frozen value | measured value | signed values | passing-direction distance | row verdict |

Every comparable metric row contains:

| Field | Meaning |
| --- | --- |
| `baseline_kind` | `raw-layerstack`, `previous-stage`, `native-copy`, `streamcdc`, or a named oracle/control |
| `baseline` | frozen value, unit, revision, environment, cache class, and sample set |
| `required_target` | exact Prep formula and computed value; never a prose-only goal |
| `optimization_target` | value frozen before the candidate run; may be stricter than Prep, otherwise equals `required_target` |
| `candidate` | actual measured value from this stage |
| `delta` / `delta_percent` | signed candidate-minus-baseline change; latency improvement is also shown as `baseline-candidate` |
| `ratio` | candidate/baseline, with direction (`lower`, `higher`, or `exact`) |
| `headroom` | distance from the required cap/floor in the passing direction |
| `statistics` | raw samples, p50/p95, MAD, `N`, throughput/bytes, and CI where applicable |
| `verdict` | `PASS`, `FAIL`, `OPEN`, or `NOT_APPLICABLE`, with exact reason |

The report also contains the full complexity work counters and scale cells,
resource high-waters, RSS, every physical-space term, cleanup/quiescence,
missing-data inventory, and links/digests for raw samples. Where the same
operation exists, include both raw LayerStack and previous-stage comparators so
the report shows the performance obtained on arrival at each stage. Do not
force a comparison between different operations; record it as
`NOT_APPLICABLE`.

After generation, link the report in this scorecard and the stage-local
progress table, and append its verdict to `e2e/test-report.md`. A missing
report, missing baseline, target chosen after candidate data, or untraceable
raw sample blocks stage arrival.

## 9. Conduct and progress recording

For every live invocation:

1. Freeze product/test/docs commits and dirty state, binary digest, config and
   route mode, host/CPU/memory/storage, Docker/guest kernel, filesystem/mount,
   OCI index/platform digest, corpus digest, seed, cache class, and operation
   order.
2. Append the exact command, intended cases, expected evidence, artifact
   custody, and cleanup plan **before running** to
   `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`.
3. Run correctness first, alternate/counterbalance raw and candidate, and do
   not overlap top-level campaigns. The sole overlap exception is a
   predeclared maintenance-isolation leaf synchronizing one named active
   packer, squash builder, or GC actor with its command/PTY probe. Use event
   synchronization rather than arbitrary sleeps and poll defined quiescence
   at 100 ms for at most 5 seconds where the stage loop requires it.
4. Preserve immutable per-sample artifacts under
   `.benchmark-state/runs/<run-id>` and derived results under
   `.benchmark-state/results/<run-id>`.
5. Immediately append `Good` or `Defect`, artifact IDs, exact misses, and
   cleanup evidence. Later append `Fix` and `Rerun`; never erase a failed run
   or silently discard a sample.

Every result records revision/build/profile/config, pair/run/seed/order,
p50/p95/p99/MAD/N/throughput, work bytes, chunk distribution, RSS/resource
high-waters, every physical-space term, duplication/slack/unreachable/trash/
quarantine/lease-blocked bytes, warm/cold state, squash timings, recovery
outcomes, exact command/control context, size/depth slopes and confidence
bounds, lowerdir bytes/mount-syscall count, maintenance active/idle events and
critical-path counters, squash build/commit/frozen/remount/evacuation events,
complete GC selector/root decisions, exact host×image×variant digests,
dependency/platform evidence, and every miss. Each value is labeled
`measured`, `derived`, `estimated`, or `unknown`; missing accounting rejects
the result and is never treated as zero.

Per-stage notes use this append-only tracker. It exposes the achieved
performance without requiring a reader to open raw JSON:

| UTC | State | Run ID | Baseline → candidate actual | Required / optimization target | Delta / ratio / headroom | Report / raw artifacts | Cleanup / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | NOT_RUN | — | — | — | — | — | Freeze the first cell before execution |

## 10. Pre-run blockers

1. The Stage 11 E2E table now defines selection as normalized end-to-end
   publication elapsed-time advantage and lists the `≤1.14×` unique-payload
   envelope separately. Preserve that separation in the runner and both
   reports; collapsing them again blocks qualification.
2. Stage 04 must freeze an unchanged-prior-tree scale sweep and numeric
   work-counter coefficients. Disk-backed external merge proves bounded memory
   but does not by itself prove incremental time.
3. Freeze the Stage 11 time-cell sample count and exclusion/stability rule
   plus OLS/percentile/bootstrap implementation, seed/resamples, pairing key,
   and raw slope-noise ceiling before candidate data. The recommended
   100-sample policy above is not a Prep-authored number.
4. Settled-space fixtures must contain no dirty unpublished upper payload.
5. Freeze exact Debian, Alpine, minimal/distroless, and shell-less OCI index
   and compatible platform-manifest digests and the full required row count.
   Every current `OPEN` digest blocks qualification.
6. Freeze the provider-declared serialized `lowerdir=` byte limit used to
   construct `limit-1/limit/limit+1` cells.
7. No stage may declare overall success until Stage 11 also passes every
   correctness, recovery, dependency, architecture, and required-platform
   prerequisite from Prep 04.
