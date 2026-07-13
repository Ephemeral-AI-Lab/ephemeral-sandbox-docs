# Autosquash Engine E2E Verification Plan

Status: Proposed

## 1. Objective

Prove that autosquash preserves layerstack contents, history semantics, live-session safety, recovery, and observability while adding negligible latency to the layer-publication critical path.

Correctness and performance are separate verdicts:

- Correctness tests poll for eventual convergence and validate exact state.
- Performance tests measure explicitly defined intervals and enforce hard numeric gates.
- A correctness timeout is a safety bound, not a performance measurement.

## 2. Test ownership and resulting structure

Autosquash-enabled E2E tests belong to the configuration gateway-custody family because they require a daemon started with custom YAML and use the family's fixed gateway/socket lifecycle.

```text
ephemeral-sandbox-test/e2e/
├── compound/
│   └── configuration/
│       └── config/
│           ├── autosquash_helpers.py
│           ├── test_autosquash_correctness.py
│           └── test_autosquash_perf.py
├── manager/
│   └── management/
│       └── squash/
│           └── ... existing manual squash regression suite
├── runtime/
│   └── ... existing explicitly-disabled regression suites
├── metadata/
│   └── stable-id-ledger.json
└── pytest.ini
```

Required catalog changes:

- Add an `autosquash` pytest marker.
- Mark long cap and live-continuity cases with the repository's existing slow/hard-test convention.
- Regenerate `metadata/stable-id-ledger.json` with the catalog collector; do not hand-edit generated IDs.
- Add the new cases to the existing test-spec/catalog workflow.

Keep autosquash explicitly omitted from the baseline E2E configuration. Many tests under `e2e/runtime` assert exact version or layer deltas, and explicit-disable compatibility is part of the feature contract. Separately verify that the shipped product configuration sets the threshold to `100`.

## 3. Shared test harness

`autosquash_helpers.py` should reuse the configuration family's daemon lifecycle, gateway custody, client, structured telemetry, and cleanup helpers. It should add only autosquash-specific helpers:

- render a minimal config with policy disabled or threshold `N`;
- start an isolated daemon/gateway and wait for readiness;
- read the active layer manifest and classify `B`, `L`, and `S` layers;
- wait for a structured autosquash event by trace/sandbox identity;
- wait until a manifest satisfies a predicate, using bounded polling rather than fixed sleeps;
- capture monotonic client-ack intervals;
- export raw timing samples and the relevant telemetry fields into run artifacts;
- assert that staging/remount residue and test-owned processes are absent at teardown.

Each assertion must select records by stable identifiers such as sandbox, trace, operation, or event name. It must not depend on unrelated global event order.

## 4. Evidence required from every case

Each case reports three axes:

| Axis | Evidence |
|---|---|
| Correctness | manifest state, merged filesystem reads/digest, blame/history where relevant, session/lease state, structured events and spans |
| Time | either the named performance metric or only the stated convergence safety timeout |
| Teardown | sandbox/session destroyed, no test-owned process/container leak, no active staging/remount residue, final observability consistent with cleanup |

Timing artifacts must include raw samples, warm-up count, measured count, threshold, product revision, config, and available host/runner identity. A summary without raw samples is insufficient for a performance verdict.

## 5. Correctness matrix

Unless specified otherwise, eventual checks use bounded polling with a 30-second safety timeout. They must not use arbitrary sleeps.

### AS-COR-01 — Explicit omission disables autosquash

Setup: start the baseline daemon with no `autosquash_policies`, then publish enough independent layers to exceed a representative threshold.

Assertions:

- The active manifest retains all published `L` layers.
- No autosquash evaluation/lifecycle records exist.
- Manual `squash_layerstack` still compacts the stack and returns its existing response shape.
- All files remain readable before and after manual squash.

### AS-COR-02 — Configuration validation

Setup: start the daemon separately with thresholds `0`, `1`, `2`, and `3`, plus an unknown policy key.

Assertions:

- `0`, `1`, and `2` are rejected with a field-specific configuration error.
- `3` starts successfully.
- The shipped product configuration resolves `squash_at_n_layers` to `100`.
- An unknown policy is rejected rather than silently ignored.
- Failed starts leave no gateway/process residue.

### AS-COR-03 — Below and exactly at the threshold

Setup: configure `N=3`. Start from `B`; publish `L1`, then `L2` as two distinct real changes.

Assertions:

- At `B + L1`, evaluation decides `below_threshold`, no `S` layer is created, and content is correct.
- At `B + L1 + L2`, exactly one successful autosquash lifecycle occurs.
- The converged manifest contains the expected compacted result and has fewer than three active layers.
- Both files and their contents are unchanged.
- A following manual squash is a clean no-op under the existing contract.

### AS-COR-04 — Implicit-session finalization ordering

Setup: reach the threshold using a command path that creates and finalizes an implicit session.

Assertions:

- The command receives a successful publish/finalize acknowledgement before autosquash completion is required.
- Autosquash sees the newly published layer.
- The finalized session's lease is released before normal planning, or a failed destruction remains lease-safe and excludes that boundary.
- The command output and published filesystem change remain correct.

### AS-COR-05 — Sessionless write/edit and no-op behavior

Setup: reach the threshold through sessionless file-write and file-edit paths, including one request that produces no new layer.

Assertions:

- Real write and edit commits notify and eventually trigger at the threshold.
- A no-op/deduplicated publish does not emit a second trigger.
- Autosquash's own `S` commit does not recursively trigger another evaluation.
- File contents and representative blame attribution survive compaction.

### AS-COR-06 — Squash semantic equivalence

Setup: in one compact workload, create and overwrite files, delete an entry, replace/opaque a directory where supported, change a mode, and create a symlink. Capture the merged-tree digest and representative blame/history before the trigger.

Assertions:

- The merged-tree digest is identical after autosquash.
- Reads, absence checks, mode, symlink target, and directory behavior match the pre-squash view.
- Representative blame/history follows the same semantics as manual squash.
- The committed block/result is compatible with the existing manual squash planner.

This case is a cross-path equivalence check. It does not duplicate every storage edge case already owned by the manual squash suite.

### AS-COR-07 — Live lease and remount safety

Setup: keep a session/process mounted at an older snapshot while newer commits reach the threshold.

Assertions:

- Planning respects the live lease boundary.
- The active process and its filesystem view remain valid throughout the automatic action.
- Eligible mounts are remounted using the existing sweep semantics.
- After releasing the lease and publishing one more real layer, another evaluation can converge and reclaim the formerly protected block.
- No active source layer is deleted early.

### AS-COR-08 — Burst coalescing and manual race

Setup: issue concurrent sessionless commits with a small threshold and race one manual squash request against the automatic worker.

Assertions:

- Every acknowledged write is visible in the final tree.
- Notifications are observably coalesced during the burst.
- A final live-manifest evaluation occurs after the burst; no above-threshold state is stranded.
- Only one shared squash action executes at a time.
- The manual call either receives the existing in-flight error or runs afterward and reports a clean no-op, according to gate timing.
- The final active count is below `N` when no lease blocks convergence.

### AS-COR-09 — Startup catch-up and interruption recovery

Setup A: create an over-threshold stack with autosquash disabled, stop it cleanly, and restart against the same state with autosquash enabled.

Setup B: interrupt the daemon after `triggered` but before `completed`, then restart it.

Assertions:

- Startup evaluation detects and compacts the restored over-threshold stack.
- After interruption, the active manifest is readable and contains either the old atomic state or the committed new state, never a partial manifest.
- Boot cleanup removes or safely ignores abandoned staging data.
- Startup re-evaluation eventually converges.
- First and last workload files remain readable.

### AS-COR-10 — Observability contract

Setup: run one below-threshold evaluation, one successful automatic action, and one coalesced burst.

Assertions:

- Autosquash has no operation catalog/dispatch/request/response record.
- `layerstack.autosquash.evaluate` contains the specified policy, threshold, observed count, decision, queue delay, trigger reason, and coalesced count.
- The reused `layerstack.squash` span has `cause=autosquash` and is a child of, or correctly linked to, the evaluation trace.
- Existing plan, flatten, commit, and remount-sweep phase spans appear beneath the reused squash span.
- Each successful attempt has exactly one `triggered` and one `completed` event.
- The manual regression leg has `cause=manual` and retains its existing operation trace.

Failure payload/status exactness belongs in a deterministic Rust integration test if live E2E fault injection cannot target the action safely. The E2E interruption case remains responsible for crash safety and restart convergence; it must not use an artificial test-only production endpoint.

## 6. Performance methodology

### 6.1 Measurement rules

- Use `time.monotonic_ns()` for client-side intervals.
- Measure only the interval named by each case; exclude fixture setup, sandbox creation, polling, content verification, artifact upload, and teardown.
- Use five warm-up samples and at least 30 measured samples for small-operation distributions.
- Alternate A/B samples where a disabled baseline is required, rather than completing all A samples before B.
- Run performance cases serially on an otherwise idle autosquash-owned daemon/gateway. Do not run them beside other gateway-custody families or pytest workers.
- Report p50, p95, maximum, sample count, and raw values.
- A test fails on a hard gate even if correctness passes. Runner noise is diagnosed from raw artifacts; the assertion is not silently weakened.

### 6.2 Metrics

| Metric | Start | End |
|---|---|---|
| Publish acknowledgement | Immediately before client sends a layer-producing request | Client receives successful response |
| Queue delay | Producer enqueues accepted signal | Evaluation worker begins evaluation |
| Squash duration | Reused squash action begins | Reused squash action completes |
| Total convergence | Accepted threshold-crossing notification is enqueued | `layerstack.autosquash.completed` is emitted |
| HTTP silent gap | Last tick received before remount window | First subsequent tick received |

Telemetry-provided `queue_delay_ms`, squash duration, and total convergence must be used when they define the server interval more precisely than client polling.

## 7. Performance matrix and hard gates

### AS-PERF-01 — Publish critical-path overhead

Setup: run equivalent tiny sessionless writes against two otherwise identical daemons/sandboxes: autosquash omitted (A) and autosquash enabled with `N=3` (B). Alternate A/B samples. The measured call ends at publish acknowledgement; do not wait for automatic completion inside it.

Hard gates:

- `B p95 <= A p95 + 50 ms`.
- `B max <= A max + 250 ms`.

Correctness gate: every acknowledged sample is eventually readable, and B converges after threshold crossings.

### AS-PERF-02 — Engine pickup latency

Setup: produce at least 30 independent threshold crossings on a small stack, resetting through successful convergence between samples. Read `queue_delay_ms` from structured telemetry.

Hard gates:

- p95 queue delay `<= 100 ms`.
- maximum queue delay `<= 500 ms`.

### AS-PERF-03 — Small-stack convergence

Setup: trigger a squashable two-`L` block with no live sessions, at least 30 times. Measure notification-to-completed using server telemetry.

Hard gates:

- p95 total convergence `<= 2,000 ms`.
- maximum total convergence `<= 5,000 ms`.

Record squash duration separately so scheduler delay and storage cost can be diagnosed independently.

### AS-PERF-04 — Burst backpressure and convergence

Setup: issue 100 concurrent sessionless commits with `N=8` and unique paths. Run an equivalent disabled-baseline burst for acknowledgement comparison.

Hard gates:

- Enabled publish-ack p95 `<= disabled p95 + 100 ms`.
- Convergence completes within `10,000 ms` after the last publish acknowledgement.
- Notification queue occupancy never exceeds its effective capacity of one.

Correctness gates:

- At least one evaluation reports `coalesced_notifications > 0`.
- All 100 writes are present.
- The final active layer count is below `N` when no live lease blocks it.
- No producer fails because the scheduler queue is full.

### AS-PERF-05 — Live-service continuity during autosquash

Setup: keep the existing persistent tick/HTTP workload live while commits trigger autosquash and remount sweep. Reuse the manual squash continuity collector and budget.

Hard gate:

- Maximum HTTP/tick silent gap `<= 1,500 ms`.

Correctness gates:

- No tick is duplicated or lost under the existing workload semantics.
- The live service remains reachable and the post-squash filesystem is correct.

### AS-PERF-06 — Layer-cap boundary

Setup: configure `N=500`, reuse the existing synthetic layer publisher to create 499 tiny `L` layers above the base, and let the threshold crossing schedule autosquash.

Hard gate:

- Total convergence `<= 60,000 ms`.

Correctness gates:

- The final active count is below 500 when no lease blocks the plan.
- The first and last published paths remain readable.
- No staging or source-layer cleanup leak is present.

This case is slow/hard and runs in the final performance proof, not on every local edit.

## 8. Lower-level verification required before E2E

E2E is not the only safety layer. Before running the live matrix, product tests should cover:

- shipped default `100`, explicit omission, deserialization, lower-bound validation, and unknown-field rejection;
- `squash_at_n_layers` comparisons around `N-1`, `N`, and `N+1`;
- bounded channel/coalescing and the guarantee of a later evaluation;
- recheck after action-gate acquisition;
- no notification for no-op publish or squash-created `S` layer;
- notifier placement after implicit-session destruction attempt;
- manual/automatic callers mapping the same `SquashActionResult`;
- exact failed event fields and error span status through deterministic fault injection;
- worker shutdown and startup evaluation.

The existing layerstack squash unit/integration suite remains the authority for planner, flatten, atomic commit, cleanup, and lease-boundary edge cases.

## 9. Execution phases

### Phase 1 — Focused correctness

Run all `AS-COR-*` cases with the configuration family in exclusive gateway custody. Fix one failing feature at a time and preserve its artifacts before rerun.

### Phase 2 — Isolated fast performance

Run `AS-PERF-01` through `AS-PERF-04` serially on an idle runner. Inspect raw samples and telemetry if a gate fails; do not classify a functional pass as a performance pass.

### Phase 3 — Slow/hard performance

Run live continuity and the 500-layer boundary alone. Retain manifest, telemetry, resource, and timing artifacts.

### Phase 4 — Regression

- Run the existing `e2e/runtime` tree with autosquash omitted to prove default compatibility.
- Run the complete existing manual squash family to prove the extracted shared action has not changed behavior.
- Run the configuration family to prove gateway custody and cleanup remain sound.

### Phase 5 — Release proof

Release evidence requires:

- two consecutive all-pass correctness runs;
- three consecutive isolated performance runs in which every hard gate passes;
- one all-pass slow/hard performance run;
- one all-pass `e2e/runtime` run;
- one all-pass manual squash suite run;
- no skipped autosquash cases, weakened assertions, leaked resources, or unexplained telemetry gaps.

## 10. Suggested commands

From `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e`:

```bash
python3 -m pytest compound/configuration/config/test_autosquash_correctness.py -m autosquash
python3 -m pytest compound/configuration/config/test_autosquash_perf.py -m "autosquash and not slow"
python3 -m pytest compound/configuration/config/test_autosquash_perf.py -m autosquash
python3 -m pytest runtime
python3 -m pytest manager/management/squash
python3 -m pytest compound/configuration/config
```

Use the repository's normal run-owned reporter and artifact directory for final proof runs. Preserve the reporter's operation/resource evidence plus the autosquash timing JSON; do not write run artifacts into the source tree.

## 11. Exit criteria

The feature is verified only when:

1. Every acceptance criterion in the feature specification maps to a passing product or E2E test.
2. Autosquash produces the same filesystem and lease-safe result as manual squash for equivalent state.
3. Publish acknowledgement overhead, scheduler pickup, convergence, burst handling, live continuity, and cap-boundary gates all pass.
4. Explicitly-disabled runtime and existing manual squash regressions pass unchanged.
5. Structured evidence is sufficient to identify whether any failure occurred in scheduling, storage squash, remount, client critical path, or teardown.
