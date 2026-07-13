Implement and verify layerstack autosquash in `/Users/yifanxu/Ephemeral-AI-Lab`. Read the two autosquash design docs, existing layerstack/manual-squash code and tests, and `e2e/runtime`. Preserve unrelated changes.

Implementation:

1. Autosquash is an internal layerstack scheduler, not an operation/API. Add no operation registration, request, response, or endpoint.
2. Add `operation/src/layerstack/autosquash_engine/` with a worker and `policies/squash_at_n_layers.rs`; no trait, registry, factory, or new dependency.
3. Support:

```yaml
runtime:
  layerstack:
    autosquash_policies:
      squash_at_n_layers: 100
```

Ship `100` as the product default. Custom config may override it; omission disables it. Reject values below 3 and unknown fields. Count all active `B`, `L`, and `S` manifest layers; match at `count >= N`.
4. Extract squash orchestration to `layerstack/actions/squash.rs`. Manual and auto callers reuse its plan, flatten, atomic commit, remount, cleanup, leases, and single-flight. Preserve the manual API/result; add cause `manual|autosquash`.
5. Notify without blocking after a real `L` from sessionless write/edit or implicit publish; for finalize, notify after session-destruction is attempted. Exclude no-op/dedup and squash's `S`.
6. Use one worker and a capacity-one/coalescing queue that never delays/fails publish. Read/evaluate the live manifest, acquire the shared gate, then re-read/re-evaluate. Auto waits; manual keeps its in-flight error. No hot retry; reevaluate on real commit/restart.
7. Schedule one background startup evaluation after boot reap/remount sweep and shut down cleanly. Autosquash failure cannot alter an already successful publish response.
8. Trace `autosquash.evaluate -> squash -> {plan,flatten,commit,remount_sweep}` with full `layerstack.*` names. Record trigger, policy, threshold, count, decision, queue delay, and coalescing. Emit one `triggered` + `completed`, or `failed` with error/timing/status. No operation telemetry.

Verification:

Put enabled tests in `e2e/compound/configuration/config/` with exclusive gateway custody. Keep `e2e/runtime` disabled. Add an `autosquash` marker and regenerate stable IDs via catalog tooling.

Correctness: default disabled; config validation; below/exact threshold; finalize ordering; write/edit/no-op; tree/blame equivalence for create/overwrite/delete/mode/symlink/opaque-dir; leases/remount; concurrent coalescing/manual race; startup and interruption recovery; exact telemetry. Reuse manual storage tests. Poll structured evidence, no sleeps; assert no leaks.

Run performance serially with `time.monotonic_ns()`, 5 warmups, >=30 raw samples, p50/p95/max and environment metadata. Exclude setup, polling, checks, and teardown. Gates:

- publish ack: enabled p95 <= disabled +50 ms; max <= disabled +250 ms;
- queue delay: p95 <=100 ms; max <=500 ms;
- small convergence: p95 <=2 s; max <=5 s;
- 100-commit burst: ack p95 <= disabled +100 ms; converge <=10 s after last ack;
- live HTTP/tick silent gap <=1.5 s;
- base +499 layers at N=500 converges <=60 s.

Report correctness, time, and teardown evidence; retain artifacts and never weaken gates.

Run product tests; correctness twice; isolated perf three times; slow perf once; full manual-squash, config, and runtime suites. Report files, decisions, commands/results, distributions, artifacts, and gaps. No completion with skips, leaks, telemetry gaps, or failed gates.
