# Phase 00 — Freeze rules — Plan

**Status:** done (pass 2 completed 2026-08-04; docs only)

## Prerequisites

- Access to docs package and clean product worktree (read-only is enough)  
- Product [PRD.md](../../PRD.md) read  

## Approach

Read the real tree; write short inventories and plans; do not implement V2 features.

**Agent prompts (copy-paste):**

- [PROMPT.md](PROMPT.md) — pass 1: produce initial `SPEC.md` (done)  
- [PROMPT-continue.md](PROMPT-continue.md) — pass 2: close PARTIAL gaps

## Work checklist

- [x] Verify worktree path, branch, HEAD vs recorded base; note drift if any  
- [x] List public ops / file APIs that touch state or workspace (from source, not memory)  
- [x] List packages/modules that own LayerStack / workspace / publish today  
- [x] Write open decisions table (copy IDs from product PRD; add findings)  
- [x] Draft fixture categories: happy path, corrupt, crash, concurrent, migrate  
- [x] Document Stage 4.6: numbers as history; status `INCOMPARABLE` unless re-proven  
- [x] Propose resource envelopes to refine later (memory/disk/FD) — mark as proposals  
- [x] Link any appendix docs you relied on  

### Pass 2 closure (`PROMPT-continue.md`)

- [x] G1 — trace all publish rejection reasons, firing conditions, and public error projections
- [x] G2 — document concrete Docker create/destroy layout, ownership, persistence, and partial-failure behavior
- [x] G3 — recheck durable-state writers and production call sites from `src/`
- [x] G4 — compare catalog operations with CLI and MCP projections, including internal and latent mismatches
- [x] G5 — link the exact legacy 26-row appendix without adopting it; keep DEC-017 open
- [x] G6 — enumerate public `layerstack` observability inputs, outputs, null semantics, and authority boundary
- [x] G7 — map 1–2 concrete e497 test anchors per fixture category A–G and state the missing V2 oracles
- [x] G8 — audit all ten product hard rules; close no decision and select no design winner

Pass 2 is complete for the pinned e497 source tree. Bounded residuals are
explicitly limited to future providers/commits, test-only callers outside the
production search, and V2 behavior that later phases must implement and prove.

## Likely locations

| Area | Path | Action |
|------|------|--------|
| This phase docs | `ephemeral-sandbox-v2/phases/00-freeze-rules/` | edit |
| Product code | clean worktree | **read only** |
| Appendix | `implementation-plan/new_2.0_migration_implementation_plan/` | read |

## Deliverables

- **[SPEC.md](SPEC.md)** (primary)  
- [inventory-surfaces.md](inventory-surfaces.md)  
- [inventory-packages.md](inventory-packages.md)  
- [fixture-catalog.md](fixture-catalog.md)  
- Checklist items above completed  

## Stop if

- Cannot identify writers of durable sandbox state  
- Worktree base is unknown/dirty and cannot be described  
- Team tries to start store implementation in this phase  

## Handoff to phase 01

Primary handoff: **[SPEC.md](SPEC.md) §12**.  
Give phase 01: inventory summary, open decisions, fixture plan, baseline policy.  
Phase 01 may compare designs against those frozen rules.

## Effort (rough)

Small–medium docs session (hours, not weeks). See SPEC §10 for session breakdown
and later-phase rollup.

---

[PRD.md](PRD.md) · [test-perf.md](test-perf.md) · [SPEC.md](SPEC.md)
