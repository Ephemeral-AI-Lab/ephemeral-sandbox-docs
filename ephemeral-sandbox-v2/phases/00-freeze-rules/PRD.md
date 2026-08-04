# Phase 00 — Freeze rules — PRD

**Status:** SPEC drafted (2026-08-04) — see [SPEC.md](SPEC.md)  
**Inherits:** [../../PRD.md](../../PRD.md)

## Goal

Freeze what “correct” means, what we will test later, and what is still open — **before** we optimize or rewrite the store.

## Why this phase exists

If we invent fixtures and baselines after seeing candidate results, we fool ourselves. This phase builds the exam, not the student.

## In scope

- Inventory real product surfaces, writers, and packages from the clean base tree  
- Record open product decisions (blame, no-session write, etc.)  
- Plan fixtures: normal, corrupt, crash, concurrency, migration  
- Name the baseline story (including Stage 4.6 as **historical only**)  
- Resource ceiling **proposals** (not final measured V2 results)  
- COW and identity laws restated as testable intent  

## Out of scope

- Choosing architecture or disk methods  
- Implementing V2 store  
- Live cutover  
- Claiming performance winners  

## Decisions this phase makes

- What must be frozen before coding (fixture plan, decision list, inventory scope)  
- How Stage 4.6 may be used (reference / negative only unless re-sealed)  

## Decisions this phase must NOT make

- Winner architecture  
- Physical storage algorithm  
- Final package graph  

## Inputs

- Clean worktree `ephemeral-sandbox-new-2.0` @ recorded main base  
- Product PRD  
- Optional appendix design docs  

## Outputs for later phases

- **`SPEC.md`** (primary) — see [PROMPT.md](PROMPT.md) for how to produce it  
- Written inventory notes (callers, ops, store-related packages)  
- Open-decision register  
- Fixture / oracle plan  
- Baseline / comparator plan (even if “blocked until re-run”)  
- Effort estimates (this phase + rough later rollup)  
- Clear “do not tune on holdout” rule if a holdout is used  

## Success

A new implementer can start phase 01 without inventing the rules mid-flight, and without treating Stage 4.6 as a free speed guarantee.

---

[PLAN.md](PLAN.md) · [test-perf.md](test-perf.md) · [Index](../../PLAN.md)
