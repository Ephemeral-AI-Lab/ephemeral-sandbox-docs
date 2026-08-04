# Phase 04 — Wire product — Test & performance

## Exit rule

```text
PASS if core file/session E2E Must checks pass against lab store.
```

## Functional checks

| ID | Check | Must? |
|----|-------|:-----:|
| W1 | Session write + publish → committed read sees result | yes |
| W2 | `file_read` without session does not see uncommitted dirty | yes |
| W3 | `file_read` with session sees live generation | yes |
| W4 | Write without live workspace rejected | yes |
| W5 | Fork after publish does not copy payload | yes |
| W6 | Unsupported legacy ops fail explicitly | yes |

## Crash / fault

| ID | Check | Must? |
|----|-------|:-----:|
| X1 | Kill around publish: no dual truth; cleanup bounded | yes |
| X2 | Effect failure does not corrupt store head | yes |

## Not testing yet

- Full fleet fence  
- Shadow import of all legacy roots  
- Production observation window  

## Performance

| Item | Stance |
|------|--------|
| End-to-end publish | TARGET measure in lab |
| Compare Stage 4.6 | optional context only |
| MUST | correctness of W* / X* |

## Pass / fail

- **Pass:** W1–W6 and X1–X2 green.  
- **Fail:** committed mutation or silent legacy behavior.

---

[PRD.md](PRD.md) · [PLAN.md](PLAN.md)
