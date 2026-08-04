# Phase 06 — Prove offline — Test & performance

## Exit rule

```text
PASS if Must suites + both rehearsals pass on one frozen artifact, and go/no-go is written.
```

## Functional / regression

| ID | Check | Must? |
|----|-------|:-----:|
| Q1 | Artifact id frozen before suite run | yes |
| Q2 | Phase 03 Must tests re-pass on artifact | yes |
| Q3 | Phase 04 Must tests re-pass | yes |
| Q4 | Phase 05 Must tests re-pass | yes |
| Q5 | Abort-path rehearsal succeeds in isolation | yes |
| Q6 | V2-path rehearsal succeeds in isolation (no prod) | yes |
| Q7 | Go/no-go document exists | yes |

## Crash / load

Re-run earlier Must crash tests; include multi-session stress if listed in phase 00 plan.

## Not testing yet

- Real production traffic  
- Multi-day observation  
- Post-compat-deletion binary (phase 08)  

## Performance

| Item | Stance |
|------|--------|
| Matched incumbent vs candidate | MUST if comparator available; else **BLOCKED** with reason (not fake pass) |
| Stage 4.6 raw numbers | Context only |
| Small publication | Record; TARGET unless product PRD promotes MUST later |

## Pass / fail

- **Pass:** Q1–Q7 green and no open Must failures.  
- **Fail:** “looks good” without frozen artifact or failed Must re-run.

---

[PRD.md](PRD.md) · [PLAN.md](PLAN.md)
