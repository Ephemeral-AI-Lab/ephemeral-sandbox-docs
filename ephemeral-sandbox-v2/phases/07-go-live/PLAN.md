# Phase 07 — Go live — Plan

**Status:** not started

## Prerequisites

- Phase 06 **go** on frozen artifact  
- Owner approval for live change  
- Backups / restore path ready  

## Approach

Follow the rehearsal runbook on production with the **same** artifact. Prefer boring checklists over invention mid-incident.

## Work checklist

- [ ] Confirm artifact hashes match phase 06  
- [ ] Confirm all writers known and fenced  
- [ ] Capacity and monitoring ready  
- [ ] Quiesce / drain  
- [ ] Final import + verify  
- [ ] Barrier: all nodes have inert V2 activation material  
- [ ] Either abort (legacy writer at new gen) or V2 writer mode  
- [ ] Activate writers; only then open ingress  
- [ ] Observe for agreed horizon; log incidents  
- [ ] Explicit decision: proceed to phase 08 or hold  

## Likely locations

| Area | Action |
|------|--------|
| Fleet / deploy | install qualified build |
| Runbooks | execute, don’t redesign |
| This folder | observation log |

## Deliverables

- Cutover record  
- Observation summary  
- Phase 08 entry decision  

## Stop if

- Hash mismatch  
- Unknown writer  
- Incomplete acknowledgements  
- Must-class live failure during observe (hold cleanup)  

## Handoff to phase 08

Only if observation acceptable: permission to remove temp migrator/compat and re-ship.

## Effort (rough)

Ops-critical; calendar time dominated by observation window.

---

[PRD.md](PRD.md) · [test-perf.md](test-perf.md)
