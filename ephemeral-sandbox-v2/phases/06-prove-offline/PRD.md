# Phase 06 — Prove offline — PRD

**Status:** not started  
**Inherits:** product PRD · phases 00–05 outputs

## Goal

Prove the **exact** candidate build (code + config) you would cut over with — full offline tests and dress rehearsal — **without** changing live production truth.

## Why this phase exists

“Works on my branch” is not enough. Cutover must use the same bytes you qualified.

## In scope

- Freeze candidate artifact identity (commit, binary, config)  
- Re-run full relevant suites on that artifact  
- Rehearse cutover steps in an isolated environment  
- Rehearse abort path (stay on legacy) and V2 path **without** prod  
- Go / no-go note for live phase  

## Out of scope

- Actual production cutover  
- Deleting migrator for real  
- New features  

## Decisions this phase makes

- Go / no-go for phase 07  
- Which artifact hash/build is the cutover candidate  

## Decisions this phase must NOT make

- Live irreversible switch without a new authorization in phase 07  
- Skipping failed Must tests  

## Inputs

- Built product + migrator from 03–05  
- All prior test-perf expectations  

## Outputs

- Qualification record for exact artifact  
- Rehearsal notes  
- Explicit go/no-go  

## Success

You can point at one build and say: offline proof passed; rehearsal passed; ready to ask for live approval.

---

[PLAN.md](PLAN.md) · [test-perf.md](test-perf.md) · [Index](../../PLAN.md)
