# Phase 06 — Prove offline — Plan

**Status:** not started

## Prerequisites

- Phases 03–05 complete in lab  

## Approach

Do **not** rebuild mid-qualification. Record artifact id first; run suites against it; rehearse runbooks in isolation.

## Work checklist

- [ ] Record exact commit, build flags, config, binary hashes  
- [ ] Run store + wire + migrator suites on that artifact  
- [ ] Run crash/resource suites deemed Must in earlier phases  
- [ ] Isolated rehearsal: quiesce → import → abort-to-legacy  
- [ ] Isolated rehearsal: quiesce → import → V2 mode with ingress still “lab closed”  
- [ ] Matched perf sample if comparator available; else mark blocked  
- [ ] Write go/no-go with failures listed  
- [ ] Tag/branch the candidate clearly  

## Likely locations

| Area | Action |
|------|--------|
| CI / local test commands | run, capture logs |
| This folder | store qualification notes |
| Product code | bugfix only if fail; then re-qualify |

## Deliverables

- Qualification note + artifact ids  
- Go/no-go for phase 07  

## Stop if

- Any Must test fails  
- Artifact changed during run without restarting qual  
- Rehearsal cannot complete fence  

## Handoff to phase 07

Only the **qualified** artifact + runbooks + go decision.

## Effort (rough)

Medium–large (mostly test time).

---

[PRD.md](PRD.md) · [test-perf.md](test-perf.md)
