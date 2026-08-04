# Phase 08 — Clean release — Test & performance

## Exit rule

```text
PASS if migrator is gone, Must re-tests pass on the new artifact, and clean build is live-smoked.
```

## Functional checks

| ID | Check | Must? |
|----|-------|:-----:|
| R1 | No production reference to deleted migrator paths | yes |
| R2 | Store + wire Must tests pass on **new** artifact | yes |
| R3 | Fence/V2 writer laws still hold | yes |
| R4 | Deploy clean build; old processes drained | yes |
| R5 | Live smoke: read/publish basic path | yes |
| R6 | Legacy data retention explicitly documented | yes |

## Crash / regression

Re-run critical crash tests from phase 03 on the clean artifact (at least publish/recover).

## Not testing

- Optional physical deletion of legacy data (separate project)  
- Unrelated feature work  

## Performance

| Item | Stance |
|------|--------|
| Compare clean vs pre-clean | TARGET — should not regress Must envelopes |
| Full matched study | as needed; don’t claim Stage 4.6 100× |

## Pass / fail

- **Pass:** R1–R6 green.  
- **Fail:** cleanup without re-test, or live still loading migrator code.

---

[PRD.md](PRD.md) · [PLAN.md](PLAN.md)
