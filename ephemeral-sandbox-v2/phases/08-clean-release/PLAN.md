# Phase 08 — Clean release — Plan

**Status:** not started

## Prerequisites

- Phase 07 observation accepted  
- No Must-class open live incidents  

## Approach

Remove temp code in dependency order (callers first, then dead modules). Build once; re-qualify; deploy as a normal careful release.

## Work checklist

- [ ] Confirm no caller still requires migrator entrypoints  
- [ ] Delete temp entrypoints → migrator modules → dead compat  
- [ ] Keep V2 fence and store laws  
- [ ] Build clean artifact; record new ids  
- [ ] Re-run Must suites (see test-perf)  
- [ ] Deploy clean build; drain old processes  
- [ ] Smoke live  
- [ ] Document leftover legacy **data** retention  
- [ ] Optional: separate approval path for data deletion (not this checklist’s default)  

## Likely locations

| Area | Action |
|------|--------|
| Temp migrator module | delete |
| Call sites | remove branches |
| CI | re-run suites |
| Fleet | rolling/clean deploy |

## Deliverables

- Clean tree + qualified artifact  
- Deploy record  

## Stop if

- Something still references migrator  
- Re-test fails  
- Live smoke fails  

## Handoff

Program complete for storage migration **code**. Data deletion is optional and separate.

## Effort (rough)

Medium engineering + re-test + deploy.

---

[PRD.md](PRD.md) · [test-perf.md](test-perf.md)
