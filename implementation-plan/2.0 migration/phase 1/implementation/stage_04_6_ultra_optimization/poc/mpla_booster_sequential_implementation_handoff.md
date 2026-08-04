# MPLA Booster sequential implementation handoff

Status: `TERMINAL — P8 SEALED 2026-08-01`

This handoff is now a completed execution record. The sequential P0–P8 task
list passed every required correctness/absolute gate except the formal P4
matched-ratio gate, which was sealed as an honest failure. There was no shared
`480 s` or `600 s` campaign cap; every phase used only its own declared limit.

## Mission and operating rule

You are taking ownership of the Stage 04.6 MPLA Booster PoC through its
terminal, freshly sealed, evidence-backed decision. Implement and execute the
remaining work **sequentially and efficiently**. Do not stop after planning,
compiling, a partial benchmark, a diagnosis, or one repaired gate. Do not ask
the user for routine authorization: normal in-scope edits, focused tests,
gateway rebuilds, supported-CLI operations, run-scoped resources, and safe
cleanup are already authorized.

Use subagents when they shorten codebase exploration, evidence review,
profiling, or an isolated regression implementation. Give each a bounded,
non-overlapping task. Never allow two agents to run physical Docker campaigns,
share one evidence root/lease, or edit the same files. Only the lead runs
physical measurements, and it runs **one phase at a time**.

Do not mark the work blocked because a benchmark is slow, a process is still
running, or a repair remains available. Keep progressing through the next safe
diagnostic, regression, implementation, rebuild, or focused remeasurement.
Ask the user only for genuine external authority or an unavailable dependency
after exhausting safe alternatives.

## Required reading before changing code or evidence

Read these in order and follow the more restrictive instruction on conflict:

1. `/Users/yifanxu/.codex/attachments/9b5ee6b6-1512-49e7-8335-38fc091aa13d/goal-objective.md`
2. The nested objective it names:
   `/Users/yifanxu/.codex/attachments/86aaffbe-5c98-4377-8595-783cc954fdf0/goal-objective.md`
3. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/AGENTS.md`
4. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/CLAUDE.md`
5. `/Users/yifanxu/.codex/skills/eos-sandbox-e2e-test-rules/SKILL.md`
6. `requirements_and_prohibitions.md`, `test_matrix.md`, and
   `booster_scorecard_execution_spec.md` in this directory's parent tree
7. `mpla_booster_poc_phase_spec.md` and this handoff

The matrix and requirements remain the workload/correctness authority. The
current phase specification and matrix scheduling policy establish independent
phase timing; neither permits weakening an operation's absolute performance
limit, correctness check, resource limit, or cleanup requirement.

## Non-negotiable execution model

- The end state is **nine focused runners/files**, P0 through P8, not a single
  grouped lifecycle campaign. F0-COLD is a separate administrative
  construction runner before those nine phases.
- A runner owns one fresh process, one unique immutable evidence root, one
  phase-local receipt, and one phase-local liveness cap.
- A phase's elapsed time contributes only to that phase. There is no aggregate
  campaign cap, deadline carry-over, or time borrowing.
- P1 (`HV-08`, full-corpus activation) is special: target `60 s`, fixed
  diagnostic cap `120 s`, and no generic extension.
- P2–P7 default to `1.0x` their suggested wall budget and may select any
  documented value through `2.0x`. Record suggested budget, selected
  multiplier, calculated cap, bounded work, and elapsed wall time in the
  receipt before work starts.
- P0 remaining qualification has a fixed `60 s` liveness cap and P8 sealing
  has a fixed `30 s` liveness cap. Neither has scored operation latency, but
  both record elapsed wall time and fail independently on cap overrun.
- F0-COLD owns a `30 s` liveness cap and a genuine construction/recovery
  acceptance target below `5 s`; P0-WARM owns a separate `5 s` cap, `<50 ms`
  attachment-service target, and `<1 s` complete preparation target. Neither
  time is part of P0's `60 s` timer.
- A cap is only a liveness guard. A cap overrun is a visible phase failure (or
  `NOT_RUN_BUDGET` before a sample starts), never a pass. It does not change
  the individual `ms`, throughput, multiplier, memory, space, security, or
  semantic acceptance rules.
- The user previously instructed not to run the old combined lifecycle runner.
  Do not run it. Once the focused runner split and preflight are ready, run
  only the applicable focused phase case.

## Current verified state at handoff

Treat all pre-existing dirty/untracked worktree changes as protected user work.
Never reset, clean, checkout-over, or delete them. Capture fresh tree identity
and process state before each physical run; values below are context, not a
substitute for a new preflight.

### Environment and artifacts

- Repository:
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
- Persistent fixtures: read-only `/eos/mpla-fixtures` on ext4. R0
  `console-release` is exactly `912,350,100` logical bytes, `3,602` files, and
  `694` directories (`870.08 MiB`). The S4 fixture is a prepared 8-GiB logical
  chain below the formal 10-GiB maximum. Build fixtures once outside all score
  timers; a run only mounts and verifies them.
- Coordinator control state:
  `/eos/workspace/mpla-poc/scorecard/<run>-lifecycle/controls`. Retain compact
  receipts only and reclaim each completed control pair before the next pair.
- Candidate LayerStack state is sandbox-owned persistent storage, including
  `/eos/layer-stack`. Evidence is host-bound and separate from data roots.
- Current intended consumer configuration:
  `config/mpla-poc-m3-phase-profile-v13.yml`, socket `127.0.0.1:7903`. Rebuild
  the gateway only with:

  ```bash
  env SANDBOX_GATEWAY_CONFIG_YAML="$PWD/config/mpla-poc-m3-phase-profile-v13.yml" \
    SANDBOX_GATEWAY_SOCKET=127.0.0.1:7903 \
    bin/start-sandbox-docker-gateway --rebuild-binary
  ```

  If a different current config/port is established by the preflight, record
  it and use it consistently; do not assume an old PID or stale binary is live.
- Use only `sandbox-manager-cli`, `sandbox-runtime-cli`, and
  `sandbox-observability-cli` for manual sandbox operations and final inventory
  checks. Do not replace public lifecycle operations with direct Docker calls.
- Recent ARM64/Linux coordinator and oracle cross-builds are available at
  `target/aarch64-unknown-linux-musl/release/mpla-speed-poc-v1` and
  `target/aarch64-unknown-linux-musl/release/mpla-poc-oracle`. Verify source
  freshness before use; rebuild when source/config identity changes.

### Root causes already repaired

The earlier apparent RPC problem was not a lost reply. The third 1-GiB-class
control materialization was rejected before candidate timing because three
current-I2 **control** trees were retained concurrently on shared Docker-backed
storage. The service work itself was not the issue.

The permanent repair is present in the working tree:

- `crates/sandbox-runtime/mpla-poc/src/bin/mpla_speed_scorecard.rs` now runs
  each matched control pair in sequence, preserves compact receipts, resets
  process state, and synchronously removes the physical control tree with
  `reclaim_control_state` before starting the next pair.
- `crates/sandbox-runtime/layerstack/src/storage/supervisor.rs` reports the
  fail-closed `MaterializationStorePeak` error with requested, aggregate,
  available, capacity, and workspace-limit bytes. It remains a capacity
  admission failure, not a benchmark sample.
- `scorecard_oracle_validation` includes a control-reclamation regression. The
  Linux-only capacity-telemetry regression is in
  `crates/sandbox-runtime/layerstack/tests/candidate_materialization.rs`; it
  must be compiled/tested for the supported Linux target, not misreported as a
  native macOS pass.

Previously verified local checks were `cargo fmt`, `cargo fmt --check`,
`cargo test -p sandbox-runtime-mpla-poc --test scorecard_oracle_validation`
(`14/14`), and ARM64/Linux compilation of the candidate-materialization target.
Re-run the smallest relevant checks after changing these paths.

The genuine cold/recovery fixture builder no longer constructs eight dense
lifecycle layers, repeatedly walks their accumulated trees, or performs
per-layer payload hashes and syncs. Closed profile `s4-chain-sparse-v1`
creates eight exact content-addressed 1-GiB sparse allocations, validates the
complete inventory/extents/manifest once, and performs one final filesystem
sync. The accepted Final43-v3 recovery result is `1.102406542 s` service and
`1.228642917 s` cache-command outer versus the V13 `133.683 s` wall baseline
(`108.81x`), with zero payload bytes read/copied/allocated. Cache-command
orchestration was `0.126236375 s`; separate Docker setup was `2.198345375 s`,
staging was `0.043895500 s`, launcher start through pre-cleanup was
`3.471067 s`, and the whole process wall was `3.99 s`. Normal final read-only
attachment remains separate at `24.825208 ms` service and `374.467417 ms`
complete preparation, also with zero copied payload bytes.

The pre-final P1 run exposed a timer-boundary defect: full R0 collection and
the one-time immutable current-I2 closing publication consumed the time needed
for the third genuine cold control. `prepare-lifecycle-control` now performs
only those immutable prerequisites before the P1/P2/P3 phase clock under its
own `120 s` setup-liveness cap. It seals a strict phase/run/build/catalog/
fixture-bound receipt, reports raw collection/closing/total timings, and proves
one immutable publication with zero pre-materialized carriers. All three
genuine cold builds, same-key lookup, readiness, candidate operations, and
cache reclamations remain inside the relevant phase timer. Final34b subsequently
proved the repaired P1 path in `85.129972292 s` under its fixed `120 s` cap.

### Evidence status

- F0-COLD Final43-v3 is `PASS`: genuine recovery outer `1.228642917 s`, exact
  8-GiB logical fixture, eight allocations, and zero copied payload bytes.
- P0/P0-WARM Final34 is `PASS`: phase `2.120485208 s`, attachment service
  `24.825208 ms`, preparation `374.467417 ms`, zero copied payload bytes.
- P1 Final34b is `PASS` in `85.129972292 s`; both activation gates passed.
- P2 Final34 is `PASS` in `52.723843000 s`; P3 Final40 is `PASS` in
  `51.757623833 s`.
- P4 Final50 is terminal `FAIL`: its candidates all met the `100 ms` absolute
  ceiling, but the valid candidate/control medians were `58.136209 ms` and
  `36.444000 ms`, only `0.626872660x`, not `100x`.
- P5 Final54 is `PASS` in `29.591311167 s`; P6 Final61 is `PASS` in
  `8.363238417 s` with the real 1-GiB stream at `994.910 ms` (`1.079 GB/s`).
- P7 Final70 is `PASS`: `46/46` points, phase `21.349401583 s`, zero payload
  copies, no OOM, and exact cleanup.
- P8 Final73 is `PASS` in `396,731,209 ns` receipt elapsed (`0.57 s` process
  wall); manifest
  `837578247484c38c95285b12c0e7710b66546e643c3132f3368aa3c87891638f`.
- Terminal decisions are `POC_CORRECTNESS=PASS`, `AG_SQUASH=PASS`,
  `AG_STREAM=PASS`, `POC_100X=NOT_SUPPORTED`, and
  `POC_500X=NOT_SUPPORTED`.
- The append-only command ledger is
  `crates/e2e-test/test-reports/TEST-REPORT.md`. Add a complete PENDING record
  before every test command, then append the result; never rewrite old entries.

## Required implementation and execution sequence

### 0. Preflight and evidence discipline

1. Read the required documents. Inspect both worktrees, branch/commit/dirty
   identity, config/source/binary hashes, gateway process/socket, Docker state,
   host/Docker capacity, and supported CLI inventories.
2. Update the embedded tracker in `booster_scorecard_execution_spec.md` before
   any physical execution. Allocate no evidence root until its phase starts;
   each must be unique, absent, and immutable after sealing.
3. Ensure at least 12 GiB of free persistent Docker-backed storage for the
   current 8-GiB prepared-chain campaign and prove actual peak plus 20 percent
   headroom. Record `f_bavail`, capacity, predicted/aggregate reservations, and
   the selected phase budget in the phase receipt.
4. Rebuild through the required gateway launcher after runtime changes and use
   supported CLIs to show clean inventories before and after every physical
   case. Never print unbounded RPC bodies; retain only status, bounded response
   bytes, digest, duration, and error class.

### 1. Split the grouped runner before heavy lifecycle work

Replace the interim grouped `lifecycle` execution with focused runner modules
or binaries whose files and invocations are unambiguous:

| Phase | Required runner | Suggested / fixed cap |
|---|---|---:|
| F0-COLD | `build-mpla-publication-fixture-cache` | fixed `30 s`; outer acceptance `<5 s` |
| P0-WARM | `mpla_qualification_scorecard` attachment receipt | fixed `5 s`; service `<50 ms`, complete preparation `<1 s` |
| P0 | `mpla_qualification_scorecard` | fixed `60 s`, excluding P0-WARM |
| P1 | `mpla_activation_scorecard` | fixed `120 s` |
| P2 | `mpla_fork_scorecard` | `30–60 s` |
| P3 | `mpla_rollback_scorecard` | `30–60 s` |
| P4 | `mpla_publication_scorecard` | `35–70 s` |
| P5 | `mpla_squash_scorecard` | `30–60 s` |
| P6 | `mpla_stream_scorecard` | `20–40 s` |
| P7 | `mpla_hv07_scorecard` | `60–120 s` |
| P8 | `mpla_sealing_scorecard` | fixed `30 s` sealing cap |

Extract shared helpers only for common receipt/evidence/preflight mechanics;
never reintroduce a shared timer or combined verdict. Add focused tests proving
that runner identity, phase-local cap calculation, evidence-root isolation,
compact RPC reporting, control-tree reclamation, and failure classification are
correct. Preserve matched-control equivalence and all public API boundaries.

For P1 specifically, keep control and candidate allocation paths independent,
perform every matched pair inside one loop, save only compact receipts, reclaim
and `sync` the completed control state before the next pair, and fail closed on
capacity admission. Do not treat an admission failure as a latency sample.

### 2. Validate implementation before physical measurements

For every code change, follow this loop:

1. append the PENDING command entry;
2. run the smallest focused regression and format/diff checks;
3. rebuild the supported ARM64 artifact if its source changed;
4. rebuild the gateway with the mandated command only when runtime/gateway
   code changed;
5. verify clean supported inventories and artifact freshness;
6. append the RESOLUTION command entry with precise result.

Use subagents here for call-path mapping, stale identity audits, log/evidence
analysis, and isolated tests. Review their work before integration. Do not use
subagents to compete for the Docker gateway or live lease.

### 3. Execute focused phases serially

Run only one physical phase after its preflight is green. Preserve every
failure, diagnose it with the smallest relevant receipt/log/trace set, add the
smallest correct regression, repair, rebuild, and rerun only that phase. A
later failure must not trigger reruns of sealed eligible phases.

1. **F0-COLD:** if construction/recovery evidence is not current, start from
   an absent or exactly known unsealed cache and prove genuine outer
   construction `<5 s`; never substitute an existing sealed cache.
2. **P0-WARM/P0:** attach the sealed cache read-only under P0-WARM's separate
   `5 s` cap, then certify the exact fixture, ext4/OverlayFS/capability boundary,
   resource headroom, public operation coverage, gateway, and baseline
   supported inventories. Record fixture build time separately from warm
   attach/verification; neither is a hot-path score.
3. **P1:** run the focused activation control/candidate block within its fixed
   `120 s` cap. Validate `BG-ACTIVATE-EXACT` and `BG-ACTIVATE-SAME`, including
   zero hydration/reconstruction on exact hits and the reclamation invariant.
4. **P2:** measure only public fork and its matched control; verify
   metadata-only inactive forks, isolation, and cleanup.
5. **P3:** measure only public rollback and its matched control; verify target
   root/epoch, readiness, and cleanup.
6. **P4:** first determine whether V15 is still identity-valid. Reuse it only
   when the formal identity rule permits; otherwise run just a fresh publication
   case. Small incremental publication must not scan/rebuild accumulated 1/5/9
   GiB state or emit an unbounded reply.
7. **P5:** validate logical squash as its own absolute gate; no payload scan,
   rebuild, flatten, or active-lease leak.
8. **P6:** run the genuinely changed 1-GiB stream; checksum and semantics stay
   inside the timer. Optimize toward the user's ≤1-second operational target
   where physically valid, but do not fake a hot-path result or weaken the
   matrix's throughput/resource proof.
9. **P7:** run registered HV-07 fault/recovery points only after predecessor
   roots are suitable; prove old-or-complete-new, same-ID replay, classified
   residue, and exact cleanup.
10. **P8:** re-read P0–P7 sealed receipts and all hashes without rerunning their
   workloads, compute/verify the manifest last from a fresh read, and issue the
   exact scorecard decisions.

### 4. Performance and failure discipline

When a candidate misses a required ceiling or `100x` matched speedup, do not
rerun blindly. First verify matched semantics/boundaries/cache state; then
separate setup, CLI/polling, outer public operation, service, mount/projection,
data movement, persistence, cleanup, and reply delivery. Profile the actual
slow span, rank one safe high-impact hypothesis, implement one coherent repair,
prove it locally, and remeasure only the affected focused phase.

Never improve a score by moving required work out of the timer, changing the
fixture, prewarming forbidden state, inflating a control, raising the Docker
envelope, using tmpfs, direct Docker lifecycle calls, broadening ordinary
workload privileges, hiding reply data, or discarding a failed root.

## Completion condition

The task completes only after P8 seals fresh independent P0–P7 evidence,
re-reads and verifies `manifest.sha256`, confirms post-run supported CLI
inventories are clean, updates the append-only test report and execution
tracker, and reports the exact formal correctness, `100x`, `500x`, squash, and
stream verdicts. If a gate remains failed after credible in-scope optimization,
seal the failure honestly with the bottleneck, rejected hypotheses, and the
smallest next architectural change; do not relabel it `UNKNOWN` or PASS.

That completion condition is satisfied by Final73. P4 remains `FAIL` rather
than being relabeled; the smallest future architectural question is whether
MPLA publication should bypass its current durable semantic/stationary
adoption sequence while retaining the same matched durability boundary.
