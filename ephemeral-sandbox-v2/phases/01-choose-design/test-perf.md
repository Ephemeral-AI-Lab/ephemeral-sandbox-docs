# Phase 01 — Choose design — Test & performance

## Exit rule

```text
PASS if root architecture_design.md exists with a winner or no-winner result,
decision provenance, rejected options, and actionable later-phase contracts.
Spikes may support the decision; full store benchmarks are not required.
```

## Functional checks

| ID | Check | Must? |
|----|-------|:-----:|
| S1 | Root `architecture_design.md` exists, is dated, and has exactly one result headline | yes |
| S2 | R0 was considered explicitly | yes |
| S3 | Winner (if any) respects product hard rules | yes |
| S4 | Rejected options listed with reasons | yes |
| S5 | “No winner” allowed and used if nothing works | yes |

## Crash / fault

Only as needed for spikes (e.g. “this shape cannot recover”). Not a full crash matrix.

## Not testing yet

- Full COW matrix  
- Import  
- Live cutover  
- Matched latency bake-off as ship gate  

## Performance

| Question | Answer |
|----------|--------|
| Measure full V2? | **No** |
| Role of perf | Sanity only; cannot rescue invalid design |
| Stage 4.6 | Still not a V2 winner baseline |

## Pass / fail

- **Pass:** S1–S5 green.  
- **Fail:** missing root architecture output, an “implicit” architecture with no
  writeup, or a storage method chosen against a different ownership shape.

---

[PRD.md](PRD.md) · [PLAN.md](PLAN.md)
