# Phase 07 — Go live — Test & performance

## Exit rule

```text
PASS if cutover Must checks pass and observation window completes without Must-class open incidents
(or explicit hold is recorded).
```

## Functional / ops checks

| ID | Check | Must? |
|----|-------|:-----:|
| L1 | Live artifact == phase 06 artifact | yes |
| L2 | All writers fenced | yes |
| L3 | No dual writable truth at any committed step | yes |
| L4 | After V2 writer mode, legacy writes fail closed | yes |
| L5 | Ingress opens only after fleet consistent | yes |
| L6 | Observation window completed or hold documented | yes |

## Crash / incident

| ID | Check | Must? |
|----|-------|:-----:|
| LI1 | Restart during cutover recovers from durable facts | yes |
| LI2 | Incident path does not re-enable writable legacy after V2 mode | yes |

## Not testing yet

- Binary with migrator deleted (phase 08)  
- Optional data destruction  

## Performance

| Item | Stance |
|------|--------|
| Live latency/error rate | monitor vs pre-agreed envelopes |
| Alert | Must-class regression → hold phase 08 |
| Stage 4.6 | still not a live SLO by itself |

## Pass / fail

- **Pass:** L1–L6, LI1–LI2 green.  
- **Fail:** wrong binary, dual write, or unacknowledged fleet member.

---

[PRD.md](PRD.md) · [PLAN.md](PLAN.md)
