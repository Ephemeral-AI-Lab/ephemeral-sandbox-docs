# Phase 01 — Choose design — Plan

**Status:** complete — R0 joint ownership/storage design selected on 2026-08-04

## Prerequisites

- Phase 00 complete enough to list rules and inventory  
- Product PRD hard rules accepted as constraints  
- Phase 01 [selection specification](SPEC.md) defines targets, candidate
  quality, and the required architecture output  

## Approach

Start with **R0** (rewrite LayerStack home, zero new framework). Only enlarge design if R0 fails a named product rule. Record evidence; prefer deletion over new boxes.

## Work checklist

- [x] Restate candidates in one page (R0 mandatory; others only if motivated)  
- [x] For each candidate: who owns state truth, who owns mounts/exec, who owns app order  
- [x] Check: portable identity free of OCI/OverlayFS brands?  
- [x] Check: COW shared payload possible under this shape?  
- [x] Check: migrator can stay temporary?  
- [x] Spike only if needed (compile slice / dependency direction); focused source and dependency checks were sufficient, so no spike was created  
- [x] Write decision: **winner** or **no winner** + rejected list  
- [x] List “first code files to touch” for phase 02–03 (hypothesis)  
- [x] Publish the selected whole-program architecture at the V2 package root  

## Likely locations

| Area | Action |
|------|--------|
| This phase `SPEC.md` | input contract for selection; do not rewrite to fit the winner |
| Root `architecture_design.md` | selected Phase 01 output consumed by Phases 02–08 |
| Product code | small spikes only; no full rewrite yet |
| Appendix architecture docs | optional reading |

## Deliverables

- [SPEC.md](SPEC.md), the Phase 01 input/selection contract  
- [PROMPT.md](PROMPT.md), retained as the historical operational runbook and
  not as product or architecture authority  
- [architecture_design.md](../../architecture_design.md), the dated selected
  joint architecture/storage output  
- [design/README.md](../../design/README.md), the scoped ownership, identity,
  store, algorithm, reliability, migration, optimization, and proof contracts  
- Clear `GO` for Phase 02, with Phase 02 and Phase 03 implementation handoffs  

## Stop if

- Every candidate violates a hard product rule  
- Selection would require live production change  
- Team splits architecture and method into conflicting winners  

## Handoff to phase 02

Phase 02 implements identity **for the chosen design** (or does not start if no winner).

## Effort (rough)

Medium; dominated by honest comparison, not code volume.

---

[PRD.md](PRD.md) · [test-perf.md](test-perf.md)
