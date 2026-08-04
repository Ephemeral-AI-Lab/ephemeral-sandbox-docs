# 06.02 — Performance and resource demonstration matrix

```text
EVIDENCE_LABEL: INFERRED
SOURCE_METADATA: sealed e497 branch/commit/clean state recorded in algorithm/README.md
CORRECTNESS_RESULT: NOT_RUN
OPTIMIZATION_TARGET: OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED
FINAL_PERFORMANCE_VERDICT: TARGET_UNSELECTED
STAGE_4_6_EVIDENCE: INCOMPARABLE
V2_BENCHMARK_WINNER: NOT_CLAIMED
PRODUCTION_PERFORMANCE_GUARANTEE: NOT_CLAIMED
```

## 1. Purpose and owning phases

**Owners:** Phases 02 and 03 instrument and bound their algorithms. Phase 05
supplies migration cases. Phase 06 owns matched qualification and evidence
classification. Product owners select any hard target.  
**Purpose:** Define the demonstration needed to turn asymptotic and structural
claims into comparable speed, time, memory, I/O, filesystem-operation, and debt
evidence without making premature performance claims.

This document consumes the analytical model in
[resources, complexity, and observability](01-resources-complexity-and-observability.md).
It is a qualification contract, not a benchmark result.

The durable benchmark navigation package keeps the quarantined
[Stage 04.6 historical observations](../../benchmark/baseline.md) separate from
the open [V2 optimization target register](../../benchmark/target.md).

## 2. Evidence and result taxonomy

Every report records separate categories; values never migrate between
columns merely because work was planned or source was inspected.

| Category | Allowed values relevant here | Current value |
|---|---|---|
| Evidence label | `SOURCE-VERIFIED`, `SPIKE-VERIFIED`, `BENCHMARK-QUALIFIED`, `INFERRED`, `OPEN`, `OPEN_WITHIN_R0`, `OWNER_DEC_OPEN`, `INCOMPARABLE` | Matrix design `INFERRED`; exact target and run inputs `OPEN`; Stage 4.6 `INCOMPARABLE` |
| Source metadata | repository path, branch, commit, full dirty state, build/configuration seal | e497 seal recorded in the package index; no frozen V2 implementation artifact |
| Correctness result | `PASS`, `FAIL`, `NOT_RUN`, or `INVALID` within the sealed campaign record | `NOT_RUN` |
| Final performance verdict | `QUALIFIED`, `DESIGN_ONLY`, `TARGET_UNSELECTED`, `INCOMPARABLE`, `FAILED_TARGET` | `TARGET_UNSELECTED` |

`BENCHMARK-QUALIFIED` is an evidence label and does not itself set final verdict
`QUALIFIED`; correctness must pass and every predeclared target and
comparability gate must also pass. Conversely, a correctness result does not
qualify performance. No latency, throughput, RSS, storage-efficiency, or
benchmark-winner statement is supported by the current record.

## 3. Variables and predicted worst-case terms

All counts are validated finite values:

| Variable | Meaning |
|---|---|
| `E` | portable filesystem entry count |
| `B` | complete canonical-byte length |
| `P_path`, `D_path` | aggregate path bytes and maximum depth |
| `V` | complete logical payload bytes |
| `Ops_fs` | filesystem metadata/durability operations |
| `R_rec` | maximum complete reference/control record bytes |
| `N_w` | concurrent publication writers sharing one expected Head |
| `N_r` | concurrent runtime readers |
| `T` | staging transactions |
| `Q` | custody population |
| `D_n`, `D_b` | cleanup/recovery debt items and bytes |
| `V_read`, `V_write`, `V_copy` | materialization/activation byte scopes |
| `w`, `b` | bounded workers and per-worker streaming buffer |
| `e_batch`, `M_fixed` | bounded metadata batch and fixed memory |
| `L_gate`, `L_id` | transition-gate and VersionId-reservation waits |
| `L`, `N_l` | migration legacy bytes and import units |

Expected analytical terms to validate rather than assume:

| Algorithm | Honest worst-case model |
|---|---|
| Canonical validation/order | `O(B + P_path + E log E)` for comparison sorting; selected streaming/external sort may refine implementation |
| `VersionId` derivation | `O(B)` time, fixed digest state plus bounded buffers |
| Occupied exact equality | `O(B)` worst-case and up to `2B` canonical-byte reads |
| New complete admission | `O(B + V + E + Ops_fs + L_id)` plus selected ordering/fences |
| Reference EphCoW | `O(1) + L_gate`, `O(R_rec)` metadata, payload `0/0/0` |
| Accepted-only publication | `O(1) + L_gate + fence`, `O(R_rec)` metadata, payload `0/0/0` |
| Full Candidate publication | capture + admission terms + accepted-only transition |
| Protected activation setup | `O(Ops_act + custody effects)`, no required eager complete-payload copy |
| Full private materialization | `O(E + V_read + V_write + Ops_act)`, peak memory `O(w*b + e_batch + M_fixed)` |
| Recovery | proportional to the finite inventory and verification bytes selected for one bounded pass/batch |
| Retirement | decision `O(H + R + Q)`; complete-closure reclamation `O(E + filesystem_reclaim(V))` |
| Migration | `O(L + B + V + E log E + N_l*R_rec)` plus verification/retry |

Asymptotic fit is necessary but not sufficient. Durability fences, allocation,
small-file metadata, cache, scheduling, contention, sparse policy, and cleanup
may dominate constants and tails.

## 4. Evidence-seal contract

### Inputs

- Exact product/docs/source commits and dirty-state seals.
- Phase 02/03 format, filesystem, durability, limits, and configuration seal.
- Hardware/virtualization, kernel/OS, filesystem/mount, storage device, CPU,
  memory, runtime, and power/thermal profile.
- Versioned datasets/workload generator with validated expected totals.
- Cache protocol, warmup, run order/randomization, repetitions, concurrency, and
  failure-injection schedule.
- Correctness oracle and scoped byte/metadata/resource instrumentation.
- Finite benchmark wall time, CPU, memory, FDs, workers, trace, temporary disk,
  retained artifact, and cleanup budgets.
- Owner-selected targets, if any, recorded before viewing results.

### Preconditions

1. Every measured operation first passes its functional, crash, security, and
   invariant checks; an incorrect fast result has correctness `FAIL` and no
   qualifying performance verdict.
2. Comparison candidates use matched semantics, durability, inputs, error
   handling, cache state, resource caps, and evidence tools.
3. Calibration and positive controls prove byte, RSS, syscall/metadata, fence,
   failure, and trace instrumentation detects known work.
4. No run touches product worktrees, live state, or migration data; all fixtures
   live beneath a validated disposable qualification root.
5. Outlier/noise/exclusion policy is fixed before results are inspected.
6. Stage 4.6 historical artifacts remain separate and `INCOMPARABLE` unless
   their missing closure/provenance is independently repaired.

### Outputs

A sealed matrix containing every required case, functional/correctness result,
resource and performance measurements, evidence state, exclusions, and raw
artifact manifest. It is diagnostic evidence only and cannot change Version,
Head, Root, custody, migration, or authorization truth.

### Typed outcomes

| Outcome | Meaning |
|---|---|
| `Qualified(matrix, seal)` | Every required correctness/resource gate and selected hard target passed with `BENCHMARK-QUALIFIED` evidence; final verdict may then be `QUALIFIED`. |
| `SpikeVerified(property, seal)` | A bounded exploratory result supports only the named property and configuration. |
| `Failed(gate, evidence)` | Correctly measured behavior violated an invariant, bound, or predeclared target; a failed target yields final verdict `FAILED_TARGET`. |
| `Incomparable(reason)` | Semantics, durability, source, environment, workload, or instrumentation do not match. |
| `EvidenceInvalid(reason)` | Trace loss, tool/control failure, arithmetic error, fixture corruption, resource exhaustion, or missing artifacts invalidate conclusions. |
| `Cancelled` | No conclusion is promoted; completed sealed subcases may remain evidence at their prior scope. |

## 5. Workload dimensions

The matrix must include boundary and adversarial cases, not only average
production-like examples.

### Candidate and payload shape

- empty/minimal, exact-limit, and over-limit Candidates;
- tiny, medium, and maximum qualified `B`/`V`;
- few large files, many tiny files, and mixed distributions;
- deep/wide trees, long path aggregates, ordering-reversed inputs;
- duplicate/equal and unique content ratios;
- portable metadata, links, sparse extents, and unsupported-entry rejection;
- incompressible and compressible data where underlying storage behavior could
  differ, without changing Version semantics.

### Admission occupancy

- new unoccupied `VersionId`;
- occupied exactly equal bytes;
- first-byte, middle-byte, last-byte, and exact-end mismatch;
- forced digest/length collision hook selected by Phase 02;
- simultaneous equal and unequal contenders;
- cancellation/crash before/after each recognized staging/accepted prefix;
- staging, FD, worker, disk, reservation-wait, and debt saturation.

### References and publication

- Fork, Root/Checkpoint, rollback, same-Version, and accepted-only publication;
- two through selected-maximum `N_w` writers sharing one expected Head;
- same target versus different targets;
- stale expected binding, stale revision, and both stale;
- response loss before/after conditional replacement;
- lock wait/timeout, cancellation, reference-record failures, and crash prefixes;
- payload sizes varied independently to demonstrate reference cost independence
  and payload `0/0/0` rather than infer it from small fixtures.

### Runtime access/materialization

- protected immutable setup and demand reads;
- complete private materialization across all payload shapes;
- cold and warm cache as separately reported cases;
- `V` much larger than memory budget to validate streaming peak RSS;
- varied bounded `w`, `b`, and FD caps;
- concurrent `N_r` readers/materializers and long custody;
- destination space/metadata exhaustion, cancellation, crash, and cleanup;
- optional acceleration enabled, unavailable, failed, and correct fallback—if
  Phase 03 selects an optional qualified accelerator.

### Recovery, retirement, migration

- recognized staging/Head/Root/control crash prefixes and corruption;
- bounded clean, orphan, quarantine, custody, and cleanup debt populations;
- retirement with each individual reachability/custody blocker and last-race;
- legacy data shapes, restart points, batches, writer fencing, cutover, and
  rollback-before-commit;
- startup and bounded-batch behavior at exact selected maxima.

## 6. Measurement algorithm

```text
run_qualification(matrix, seal, budgets):
    validate all source/config/environment/workload seals
    run instrumentation positive controls and correctness oracle self-tests
    if any fail: return EvidenceInvalid

    for case in predeclared bounded run order:
        provision isolated fixture and verify expected logical totals
        establish requested cache and failure state
        begin disjoint operation scopes:
            identity/canonicalization
            admission
            reference/Head transition
            runtime activation/materialization
            recovery/cleanup/migration

        execute case under fixed resource caps
        collect complete raw counters/traces and functional outcome
        verify crash/durability/reference/immutability/OCC invariants first
        if invariant fails: record correctness FAIL; do not publish speed as valid
        require complete telemetry and calibration coverage
        compute predeclared statistics with checked arithmetic
        clean isolated fixture or charge bounded qualification cleanup debt

    aggregate only comparable cases
    classify every missing/unmatched case explicitly
    evaluate predeclared hard targets, if any
    emit sealed matrix and raw-artifact manifest
```

## 7. Required metrics

Metrics must be recorded per operation scope and as bounded process/store
high-water marks where relevant:

- wall-clock latency distribution and throughput under stated concurrency;
- CPU user/system time, scheduling/wait time, and transition/reservation waits;
- peak and time-series RSS, allocator bytes if available, and bounded scratch;
- logical and physical bytes read/written/copied/offloaded by path class;
- canonical comparison bytes per side and exact-end result;
- filesystem metadata operations, syscalls where qualified, and fence latency;
- staging/destination/accepted/orphan/quarantine/cleanup bytes and item counts;
- FDs/handles, workers/tasks, queues, locks, mounts/namespaces, and custody
  high-water marks/age;
- cancellation/crash side, recovery batches/work, and cleanup debt/age;
- functional outcome, Head replacement count, stale/same/winner count, and
  read-only resolution outcome; and
- trace drops, unknown path class, counter overflow, calibration status, and
  instrumentation overhead.

No raw path, content, secret, unbounded ID, or high-cardinality user value may
become a metric label.

## 8. Correctness and resource pass gates

### Complete-Version addressing/admission

```text
computed VersionId alone never reports accepted/equal/existing
occupied success requires full canonical-byte comparison to exact end
full mismatch returns VersionIdCollision
equal bytes converge to exactly one complete physical payload closure
no accepted incomplete closure after failure/crash
all selected resource high-water marks remain within configured caps
```

### Reference EphCoW

For every normal/failure/concurrent/crash case:

```text
payload_open_count    == 0
payload_read_bytes    == 0
payload_write_bytes   == 0
payload_copy_bytes    == 0
unknown_path_count    == 0
trace_dropped_events  == 0
```

### OCC publication

```text
for one expected Head state:
  state-changing winners == 1 at most
  every state-changing loser == StaleExpectedHead
  loser Head writes == 0
  no implicit expected refresh, merge, rebase, or retry
  only Head point == one conditional complete-record replacement
```

### Runtime materialization

```text
accepted payload mutations == 0
complete private projection == expected portable Version projection
peak memory <= selected bound modeled by w*b + e_batch + M_fixed + tolerance
FDs/workers/mounts/custody/destination/debt <= selected caps
all actual V_read/V_write/V_copy reported outside reference scope
no partial destination becomes runtime-ready
```

### Recovery, retirement, migration

```text
startup == prior truth OR complete new truth OR fail closed
recovery/cleanup work <= selected batch/debt bounds
retirement requires no Head, no Root, no custody after final revalidation
migration writable selected truths <= 1 at every generation
post-cutover compatibility code remains deletable
```

Failure of any correctness gate invalidates associated speed numbers as a
qualification claim.

## 9. Performance target evaluation

Targets are not invented here. A product owner may predeclare hard thresholds
for latency, throughput, RSS, disk amplification, activation time, recovery
time, or cleanup debt. The sealed report then states pass/fail per exact
workload and percentile/statistic.

The required target tuple and currently empty target rows are maintained in
[the V2 optimization target register](../../benchmark/target.md). Publication,
accepted-only reference transition, protected activation, complete private
materialization, and end-to-end runtime readiness remain separate scopes.

No owner-approved quantitative target exists now, so the durable marker remains
`OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED` and the final verdict remains
`TARGET_UNSELECTED`. Without a predeclared target, results are descriptive evidence only. Faster
median time does not override worse correctness, tail, durability, memory,
cleanup, or operating behavior. A comparison is `INCOMPARABLE` if any of those
semantics differ materially.

Complexity validation should inspect scaling curves, not merely single points:

- vary one of `B`, `E`, `V`, `N_w`, `N_r`, `D_n`, or `L` while holding others
  controlled where feasible;
- report normalized time/bytes/RSS and residuals without claiming a formal
  proof from curve fit;
- identify constant/tail changes at cache, memory, FD, worker, and filesystem
  boundaries; and
- compare observed high-water marks to selected finite resource models.

## 10. Visibility and linearization

Qualification creates no Version, reference, or application authority outside
its isolated fixture. Measurement hooks and evidence classification are not
durability or linearization points.

The harness must verify, not redefine:

- AcceptedVersion complete-slot visibility;
- complete Root-record visibility;
- custody installation relative to retirement;
- private runtime materialization readiness; and
- the single Head linearization point: conditional complete Head-record
  replacement under the one LayerStack-0 transition gate.

## 11. Behavior by execution condition

| Condition | Required harness behavior |
|---|---|
| Normal | Run predeclared cases/repetitions, validate correctness first, then report complete metrics and evidence state. |
| Concurrent | Synchronize only as declared; preserve per-operation scopes and outcome attribution; report coordination overhead. |
| Retry | Record every actual attempt and its resources; do not collapse failed staging/comparison or stale costs. |
| Cancellation | Flush/validate complete evidence or classify the case cancelled/invalid; never extrapolate a pass. |
| Crash | Preserve sealed artifacts, classify product recovery, rerun incomplete measurement cases, and never treat missing data as zero. |
| Cleanup | Operate only in the disposable root, bound cleanup work/debt, and report leaked fixtures without touching live/product data. |

## 12. Finite harness resources and analysis complexity

Let `N_case` be cases, `R` repetitions, `S_event` raw events, `S_artifact`
retained artifact bytes, and `M_analysis` bounded analysis memory.

- Orchestration performs `O(N_case * R)` subject operations.
- Streaming event validation is `O(S_event)` time and
  `O(M_analysis)` memory or bounded external spill.
- Summary storage is `O(N_case * R * metrics)` under a selected finite schema;
  raw artifacts are capped by `S_artifact`.
- Subject resources use the algorithm-specific terms above; harness CPU/RSS/I/O
  and instrumentation overhead are measured separately.

Before every case the harness reserves wall time, temporary/retained disk,
trace buffers, memory, FDs, workers, and cleanup headroom. Exhaustion yields
`EvidenceInvalid`/`Cancelled`, not a truncated “fast” result.

## 13. Security and path validation

- Validate the disposable root by capability and identity; reject `/`, home,
  workspace roots, product trees, live state, and migration locations.
- Treat datasets/generators/configuration/traces as untrusted. Bound sizes,
  decompression, sparse allocation, path depth, labels, logs, and artifact
  retention with checked arithmetic.
- Redact payload contents, secrets, raw host paths, tokens, and user identifiers.
- Pin privileges and environment; report virtualization/noisy-neighbor effects.
- Prevent measurement agents and observability from issuing/revalidating
  bindings, advancing Heads, changing authorization, installing custody, or
  declaring cleanup safe.
- Record failed commands and partial artifacts; do not silently exclude errors
  or cherry-pick successful runs.

## 14. Observability and test seams

The qualification harness itself requires tests for positive/negative byte
controls, counter overflow, trace loss, time-source consistency, RSS high-water
capture, cache protocol, failure injection, fixture identity, source/config
seal mismatch, run-order reproducibility, checked statistic arithmetic,
artifact truncation, cleanup bounds, and secret/cardinality redaction.

The final evidence manifest must list every required case as passed, failed,
invalid, cancelled, or not run. Missing rows are not allowed. Raw artifacts and
summaries must be traceable to the exact seal without turning artifact hashes
into Version reference authority.

## 15. Details owning phases may still select

Phases 02/03 select exact instrumentation points and numerical resource limits.
Phase 05 selects migration datasets/progress mechanics. Phase 06 selects
qualification hardware/filesystem matrix, tools, workloads, repetitions,
statistics, tolerances, artifact format/retention, and noise policy. Product
owners select any hard target.

No phase may hide nonzero admission/materialization I/O, call missing telemetry
zero, weaken correctness for speed, compare mismatched durability, or promote a
design/spike result to a production guarantee.

## 16. `REOPEN_PHASE_01` conditions

Return `REOPEN_PHASE_01 — <specific architecture-changing failure>` only when a
sealed comparable `FAILED_TARGET` result proves that an accepted hard product rule or
hard performance/resource target cannot be met by any repair that preserves:

- one complete immutable Version truth;
- existing LayerStack-0 and runtime ownership/direct calls;
- one writer and one Head OCC point;
- full occupied-ID canonical-byte equality;
- zero-payload reference operations; and
- bounded fail-closed staging, memory, FDs, workers, custody, recovery, and debt.

The reopening report must identify within-R0 repairs attempted and explain why
they fail, then enumerate replacement dependency, crash, recovery, resource,
security, migration, cleanup, and operating costs. Until such evidence exists,
Stage 4.6 remains `INCOMPARABLE` and this package makes no benchmark-winner or
V2 performance-guarantee claim.
