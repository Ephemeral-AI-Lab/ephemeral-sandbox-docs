# Stage 06 benchmark note — strict candidate activation

[Specification](spec.md) · [E2E plan](e2e_test.md) ·
[Stage 03–11 scorecard](../stage_03_11_benchmark_note.md) ·
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Status: **NOT_RUN**

Preparation 04 numbers are the normative Phase 1 gates. The small sample
counts, cell schedule, and wall-clock budget below are stage-local benchmark
policy: they can find regressions and prove correctness/caps, but cannot
qualify a percentile. Stage 11 alone may report `QUALIFIED`.

The no-op command comparator is frozen exactly as direct
`docker exec <container-id> ls` (no shell). Each matched invocation gets a
fresh ordinary control container from the same pinned OCI index/platform
digest, with byte- and metadata-equivalent pristine root contents but no
LayerStack-owned `/eos` root, candidate materialization, lower/upper/work
mount, root lease, session/namespace-holder setup, or public API wrapper.
Pull/create/start/health/setup are untimed and separately recorded; the
control is already running when timing starts at the Docker exec request and
ends after exit status, stdout, and stderr are fully drained.

Pair that raw Docker execution-floor control—not bare-host `fork/exec`—with
candidate public `exec_command(["ls"])` on matched host/filesystem/root
contents, working directory, environment, Docker CPU/memory allocation, cache
class, arm order, and output-drain protocol. Other surfaces use their matched
raw LayerStack or native-copy control. For each percentile:

```text
cap_ms      = raw_ms * (1 + allowed_percent) + floor_ms
delta_ms    = candidate_ms - raw_ms
headroom_ms = cap_ms - candidate_ms
```

Before any candidate sample, separately freeze the non-normative stretch
target `docker_exec_ls_ms - candidate_exec_ls_ms >= 80 ms` at both p50 and
p95. It never replaces the Prep pass cap. If the frozen Docker control is
under 80 ms, the stretch target is missed/impossible and remains reported as
such; it is never silently rebased. Actuals remain `NOT_RUN` until measured.

| Required report field | Frozen value before the first candidate sample |
| --- | --- |
| frozen baseline | no-op: direct `docker exec <container-id> ls`, no shell, in the ready ordinary non-LayerStack control defined above; other metrics: matched raw LayerStack/native-copy samples; revision/image/root/cwd/env/cache/stdout-drain/corpus/order fixed |
| required target/cap | the Prep formulas in “Final Prep gates” below |
| predeclared optimization target (recommended, non-normative) | no-op exec saves at least 80 ms at both p50 and p95 versus the frozen Docker control; other hot-path p50 no slower than raw; command/file throughput at least `1.00*raw`; cold hydration at least `0.80*` native copy |
| candidate actual | `NOT_RUN` |
| delta / ratio / headroom | `NOT_RUN`; calculate only from preserved raw values |

## Owned target

| Surface | Required Stage 06 result |
| --- | --- |
| Authority/correctness | Explicit strict sessions report `candidate_v2_strict`, the expected root/generation, and `fallback_count=0` on success and failure; no legacy read occurs after route commit. |
| Complexity | Selection `O(1)`; warm prepare `O(1)+O(D)` setup; mount `O(D)`, `D<=64`; cold hydration `O(R+E)` and cold activation `O(R+E+D)`; command/file/PTY retain native cost with zero CDC/CAS/manifest/pack lookup. |
| Warm work | CAS payload reads exactly `0`; no ready carrier is copied per session. |
| Cold/space | Hydration staging is at most `5%` above `C_target`; total allocated bytes remain `L_hot + H_cold + sum(U_active) + P_staging + M`. |
| Clean-session space | At 64/256/1,024 MiB workspace bytes and 1/8/32 concurrent clean sessions, payload allocated growth and carrier-copy bytes are exactly 0; metadata obeys one frozen workspace-size-independent bound `M_delta(size,N) <= M0 + N*m_cap`. |
| Hard resources | 32 KiB ring; one borrowed chunk/worker and at most 4 globally; 4 workers; downstream payload queue 0 bytes; 64 MiB storage semaphore; 16 descriptors/64 KiB metadata queue; 256 KiB hydration buffers; 4,096 x 4 KiB = 16 MiB cache; managed memory at most 4 MiB/op excluding cache; RSS at most 384 MiB and 128 MiB above raw idle. |
| Local duration/release | Each operation at most 60 s; poll every 100 ms for quiescence for at most 5 s; all plans, mounts, guards, hydration owners, permits, tasks, scratch, and extra FDs release. |

Big-O is established by ownership, bounded queues, and work counters, not by a
flat tiny-loop elapsed time.

## Tiny experiment/evaluation matrix

Use seed `0x5A06`, the pinned Ubuntu OCI index and resolved platform manifest
from the E2E plan, pre-generated inputs, one unchanged packaged daemon, and
the same host/filesystem/cache/configuration for both arms. The lifecycle
control is raw legacy LayerStack and the candidate is strict v2 activation.
For the no-op command cell only, the control is direct
`docker exec <container-id> ls` without a shell in the already-running
ordinary non-LayerStack container and the candidate is public
`exec_command(["ls"])`, paired under the frozen protocol above. Container
setup is outside this cell. Alternate arm order `AB/BA` across pairs and
retain timeouts and failures as samples.

Every measured pair runs the empty/no-op, localized 1 KiB edit in deterministic
1 MiB, 1 MiB incompressible, and 256 metadata-rich small-file bundle plus
exec, sequential file I/O, PTY/stdin/control-C/control-D, digest, route, and
cleanup.

| Cell | Candidate state/history | Repetitions | Raw metrics | Pass/fail |
| --- | --- | ---: | --- | --- |
| Warmup | one cold then one warm pair | 2 pairs, excluded | correctness and route only | must pass before measurement |
| C1–C2 | depth 1: forced cold, then warm reuse | 2 measured pairs | phase elapsed, payload/read bytes, throughput, mount depth, route | exact output; fallback 0; warm payload 0 |
| C3–C4 | depth 8: forced cold, then warm reuse | 2 measured pairs | same, plus resource high-waters | same; every cap holds |
| C5–C6 | depth 32: forced cold, then warm reuse | 2 measured pairs | same, plus depth/work slope | same; no hot-path storage work |

The six pairs support raw ratios and medians only, not normative p95. Run the
separate lifecycle sentinel for 12 post-warmup candidate lifecycles: ten
successful cold/warm activations, one cancellation, and one injected mount
failure.

### PTY control and unsupported-operation cells

| Cell | Exact action | Required result |
| --- | --- | --- |
| `S06-PTY-C` | create PTY, write the fixed marker, send one control-C, drain | byte/status behavior exactly matches the frozen legacy control, completes within 5 s, `fallback_count=0`, and CDC/CAS/manifest/pack lookups are 0 |
| `S06-PTY-D` | create PTY, write the fixed marker, send one control-D, drain | byte/status behavior exactly matches the frozen legacy control, completes within 5 s, `fallback_count=0`, and storage hot-path lookups are 0 |
| `S06-PTY-UNSUPPORTED` | invoke resize, arbitrary signal, and literal EOF exactly once each | each returns the exact frozen legacy deterministic unsupported code/status/body with no side effect and no fallback; these are not scored as implemented-operation latency |

### Mandatory fail-closed and recovery cells

Each row runs once after one excluded setup/warmup and must return the declared
strict error, keep `legacy_resolver_calls=0` and `fallback_count=0`, expose no
partial session/carrier, and quiesce all case-owned resources within 5 s.

| Cell | Injection point(s) |
| --- | --- |
| `S06-F-MISSING` | selected root absent; selected materialization absent |
| `S06-F-STALE` | stale catalog generation; expected-root mismatch; quarantined root/materialization |
| `S06-F-CORRUPT` | corrupt/truncated locator or index; corrupt selected object |
| `S06-F-VERIFY` | object/root verification failure after read but before activation visibility |
| `S06-F-HYDRATE` | Stage 05 hydration returns a typed failure before carrier-ready |
| `S06-F-ENOSPC` | preflight admission, mid-hydration write, and after carrier visibility but before catalog commit |
| `S06-F-LIFECYCLE` | cancellation, injected mount failure, and daemon restart with recoverable setup state |

### Clean-session space sweep

Prebuild immutable base/workspace fixtures of exactly 64, 256, and 1,024 MiB
outside the measured interval. For each size, run concurrency 1, 8, and 32:
one excluded setup/warmup, then exactly three measured repetitions of
create → public no-op exec → destroy without a file write (27 measured cells
total). Before the first candidate sample, freeze `M0_bytes` and
`m_cap_bytes` from the existing raw clean-session control and reuse those same
constants for every size and concurrency.

Every cell records allocated blocks by category and must satisfy
`payload_allocated_delta_bytes=0`, `carrier_copy_bytes=0`, and
`M_delta(size,N) <= M0_bytes + N*m_cap_bytes`. The unchanged coefficients,
plus work counters for plans/guards/mounts proportional only to `N`, prove
per-session metadata is `O(1)` and independent of workspace bytes.

### ESTIMATED wall-clock budget

These estimates assume the binary is built and the image is present. Build,
image-pull, and Cargo-lock time are reported separately. Replace `ESTIMATED`
with measured durations after the first run.

| Portion | ESTIMATED time |
| --- | ---: |
| fixture/setup and frozen fingerprints | 3–5 s |
| 2 warmup pairs | 4–8 s |
| 6 measured pairs | 18–30 s |
| quiescence and run-scoped cleanup | 4–8 s |
| report validation/write | 2–4 s |
| **core diagnostic loop subtotal (30–60 s lane)** | **31–55 s** |
| separate fail-closed matrix invocation | **75–180 s** |
| separate 12-lifecycle/recovery invocation | **60–150 s** |
| separate 27-cell clean-space invocation | **75–180 s** |
| **four-invocation healthy arrival bundle total** | **241–565 s** |

The estimates are scheduling aids, not latency gates. The tiny loop target is
at most 60 s; each of the four invocations is separately scheduled and
estimated below 5 min, every individual operation remains at most 60 s, and
quiescence never waits beyond 5 s.

## Final Prep gates carried to Stage 11

| Metric | Normative final gate |
| --- | --- |
| warm resolve/session prepare | p50 and p95 `<= raw*1.05+2 ms`; zero CAS payload reads |
| OverlayFS mount | p50 and p95 `<= raw*1.05+2 ms` |
| no-op exec | against direct no-shell `docker exec <container-id> ls` in the ready ordinary non-LayerStack control, p50 and p95 `<= docker_exec_ls*1.03+0.5 ms`; separately report the frozen non-normative ≥80 ms saving target |
| native command and sequential read/write | throughput at least `0.97*raw` |
| PTY create | p50 and p95 `<= raw*1.03+1 ms` |
| PTY drain/stdin/control-C/control-D | p50 and p95 `<= raw*1.03+0.5 ms` |
| unsupported PTY resize/arbitrary signal/literal EOF | preserve the exact frozen legacy deterministic unsupported response; do not score as implemented-operation latency |
| cold hydration/activation | at least `0.70*` native-copy throughput; activation p95 at most `1.5*` native-copy control plus warm-mount allowance |
| memory scaling | 64/256/1,024 MiB x 1/16/64 roots x 3 reps; adjusted peak/final span at most 16 MiB and no 4x scale step adds more than 8 MiB |
| duration | each operation at most 60 s; each matched final invocation at most 5 min |

The tiny run draws these as diagnostic alert lines; it does not pass their
final sample-size or corpus requirements.

## Raw evidence and arrival report

Preserve every sample's pair/order, exact control/candidate command vectors,
control-container isolation and no-LayerStack proof, untimed
pull/create/start/setup intervals, container/image/root/cwd/env/cache/
stdout-drain protocol, phase times, bytes
read/written/copied,
operations/s, file throughput, CAS/manifest/pack lookups, mount depth, route
and fallback, root/generation/digest, workers/tasks/buffers/queues/permits,
FDs/mounts/guards, RSS/cgroup source and high-water, quiescence latency, and
all five physical-space terms. Include the PTY/fail-closed cell result,
clean-space `size_bytes`, `concurrency`, `M0_bytes`, `m_cap_bytes`, payload and
carrier-copy deltas, and the canonical exact-zero dependency schema:
`resolved_external_package_delta=[]`, `enabled_external_feature_delta=[]`,
`direct_external_edge_delta=[]`, `cargo_lock_delta=[]`,
`python_environment_delta=[]`, `system_tool_delta=[]`,
`runtime_service_delta=[]`, and `target_image_helper_delta=[]`.

Stage 06 has not arrived until the run emits:

- `.benchmark-state/results/<run-id>/stage-06-perf-report.json`
  with `schema_version="phase1.stage06.perf-report.v1"`; and
- `.benchmark-state/results/<run-id>/stage-06-perf-report.md`.

Both reports must link the immutable raw run and contain frozen raw baseline,
required target/cap, predeclared optimization target, candidate actual,
delta/ratio/headroom, complexity/work counters, memory/RSS, physical space,
full provenance, missing values, and a
`DIAGNOSTIC_PASS|FAIL|OPEN` verdict. Then append a new row to this tracker and
append the command plus
`Good`/`Defect`/`Fix`, artifacts, and cleanup to
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`.

The first Markdown table must show the frozen baseline actual, required pass
target/cap, separately predeclared optimization target, candidate actual,
delta/ratio, headroom, and verdict for every stage-owned metric.

## Append-only progress

| UTC | State | Run ID | Baseline → candidate actual | Required / optimization target | Delta / ratio / headroom | Report / raw artifacts | Cleanup / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | NOT_RUN | — | — | — | — | — | Freeze the first pair before execution |
