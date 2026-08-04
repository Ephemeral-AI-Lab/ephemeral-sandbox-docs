# Phase 00 — Freeze rules — Test & performance

## Exit rule

```text
PASS if inventories and plans exist and are consistent with the product PRD.
No V2 code or V2 benchmarks are required.
```

## Functional checks (docs quality)

| ID | Check | Must? |
|----|-------|:-----:|
| D1 | Worktree identity recorded (path, branch, commit, dirty?) | yes |
| D2 | Open decisions listed, none silently closed | yes |
| D3 | Fixture categories listed for later phases | yes |
| D4 | Stage 4.6 labeled historical / not a V2 guarantee | yes |
| D5 | Product hard rules referenced, not contradicted | yes |

## Crash / fault

None for product code (no product change).

## Not testing yet

- Store behavior  
- Import  
- Live fleet  
- Latency  

## Performance

| Question | Answer |
|----------|--------|
| Measure V2 this phase? | **No** |
| Stage 4.6 | History only; prior POC was slower than control; not matched baseline for V2 |
| Complexity | N/A |

## Pass / fail

- **Pass:** all Must docs checks green.  
- **Fail:** missing inventory, or docs claim a performance/architecture winner.

---

[PRD.md](PRD.md) · [PLAN.md](PLAN.md)
