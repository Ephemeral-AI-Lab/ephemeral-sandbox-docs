# Benchmark evidence and target contract

```text
PACKAGE_ROLE: PERFORMANCE_EVIDENCE_NAVIGATION
CURRENT_V2_EVIDENCE: OPEN
CURRENT_V2_CORRECTNESS_RESULT: NOT_RUN
OPTIMIZATION_TARGET: OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED
FINAL_PERFORMANCE_VERDICT: TARGET_UNSELECTED
STAGE_4_6_EVIDENCE: INCOMPARABLE
QUALIFICATION_DECISION: QUAL-001 — OPEN_WITHIN_R0
```

This package keeps historical observations, future target selection, and final
qualification in separate records. It does not declare a benchmark winner or
performance guarantee.

## Read in this order

1. **[baseline.md](baseline.md)** — quarantined Stage 04.6 MPLA Booster POC
   observations, provenance, and permitted use.
2. **[target.md](target.md)** — the unquantified V2 target register and the
   approval contract that must be completed before a qualifying run.
3. **[Performance demonstration matrix](../algorithm/06-resources-performance-and-evidence/02-performance-demonstration-matrix.md)**
   — the selected benchmark protocol, evidence seal, metrics, correctness
   gates, and final-verdict rules.

The filename `baseline.md` is navigational. The document is not a comparable V2
baseline. Stage 04.6 remains historical evidence with classification
`INCOMPARABLE`.

## Why the records are separate

| Record | Question it answers | May it set V2 acceptance? |
|---|---|---|
| Historical baseline | What did the Stage 04.6 POC report, under what historical scope, and with what provenance limitations? | No. It may inform fixtures, measurement dimensions, and hypotheses only. |
| Target register | What operation, workload, environment, statistic, threshold, resource ceiling, and correctness prerequisites will the owner approve before results exist? | Yes, after every required field is frozen; no value is approved now. |
| Qualification report | Did a sealed, correctness-passing, comparable V2 campaign meet the predeclared targets? | Yes, when Phase 06 produces the required evidence. No such report exists now. |

Correctness, evidence quality, and performance verdict are independent fields.
A historical correctness pass does not qualify V2 performance. A
`BENCHMARK-QUALIFIED` evidence label would not by itself imply final verdict
`QUALIFIED`.

## Selected measurement boundaries

Publication and runtime work are measured separately because they answer
different product questions:

```text
full publication
  authorized Candidate publication request
  -> capture, validation, canonicalization, VersionId derivation
  -> durable complete-Version admission and AcceptedBinding
  -> exact Head OCC, qualified fence, terminal caller outcome

runtime readiness
  authorized runtime request and captured AcceptedBinding
  -> custody
  -> backend-qualified direct activation or private materialization
  -> runtime-ready result
```

Diagnostic rows further isolate admission, accepted-only reference transition,
protected activation, complete private materialization, recovery, retirement,
migration, and resource/debt behavior. No single aggregate multiplier may hide
a regression in correctness, publication, durability, materialization, tail
latency, memory, cleanup, or operating behavior.

Accepted-reference payload movement `read/write/copy = 0/0/0` is a structural
correctness invariant for the five selected Head/fixed-Root lifecycle
operations. It is not a latency target and does not mean zero total I/O:
reference metadata, coordination, durability fences, telemetry, and backend
activation or materialization remain separately measured work.

## Authority and current state

This package consumes, in order:

- the [product performance stance](../PRD.md#performance-stance-product-level);
- the [Phase 00 Stage 04.6 evidence policy](../phases/00-freeze-rules/SPEC.md#8-baseline-and-performance-policy);
- the [Phase 01.5 evidence taxonomy and target rules](../phases/01-5-contract-closure/SPEC.md#14-evidence-and-performance-discipline);
- the selected [performance and optimization design](../design/07-performance-and-optimization.md);
- the [QUAL-001 decision record](../design/decisions/README.md#delegated-implementation-decisions); and
- the [Phase 06 qualification contract](../phases/06-prove-offline/test-perf.md).

Historical documents are evidence only. They cannot override the selected R0
architecture, complete immutable Version truth, one LayerStack-0 authority,
one Head OCC point, direct AcceptedBinding runtime handoff, one-writer
migration, or safe retirement.

## State transitions for this package

1. Keep every numeric target `OPEN` while
   `OPTIMIZATION_TARGET_NOT_QUANTIFIED` is unresolved.
2. Before observing candidate results, the authorized owner completes and
   approves every target tuple in [target.md](target.md).
3. Phase 06 freezes the candidate/control source, configuration, fixture,
   commands, environment, durability/cache state, order/seed, and raw-result
   destinations.
4. Correctness runs first. A correctness failure makes associated speed numbers
   invalid for qualification.
5. Only matched, sealed results are evaluated against the predeclared targets.
6. The qualification report records one allowed final performance verdict:
   `QUALIFIED`, `DESIGN_ONLY`, `TARGET_UNSELECTED`, `INCOMPARABLE`, or
   `FAILED_TARGET`.

Until steps 2–5 occur, the current V2 final performance verdict remains
`TARGET_UNSELECTED`.
