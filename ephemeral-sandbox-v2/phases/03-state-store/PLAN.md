# Phase 03 — LayerStack-0 durable storage — Plan

**Status:** not started

## Prerequisites

- Root [architecture design](../../architecture_design.md) selects a winner and
  Phase 02 identity has passed  

## Approach

Implement the selected **R0 / LayerStack-0** contract: rewrite the existing
LayerStack ownership home into complete immutable Versions. Delete layer/squash/depth
reconstruction from the core path. Keep identity pure; durable I/O stays in
LayerStack-0. Phase 03 may choose only the bounded details explicitly left open
by [architecture_design.md](../../architecture_design.md).

Apply the detailed-design
[forward-work naming and storage gate](../../design/README.md#forward-work-naming-and-storage-gate)
before implementation. Archived CDC/CAS, PMSS, reflink, pack/catalog, and
object-DAG plans are evidence only and cannot become the physical model through
an “internal optimization” decision.

## Work checklist

- [ ] Map current LayerStack write/read/publish paths in clean tree  
- [ ] Select and document the exact LayerStack-0 root/layout; prove it cannot overlap e497 legacy paths during coexistence  
- [ ] Implement admit/publish using phase 02 identity  
- [ ] Keep `VersionId`, `AcceptedVersion`, and `AcceptedBinding` distinct at API boundaries  
- [ ] Implement `CreateHeadIfAbsent`, `ReplaceHead`, and `RemoveHead` with complete exact expected-state comparison, typed outcomes, durable-success fence, `OUTCOME_UNKNOWN` read-back, retry/idempotency, recovery, custody, and retirement effects  
- [ ] Implement `CreateFixedRootIfAbsent` and `RemoveFixedRoot` through the same reference authority; reject generic Root replacement/retargeting  
- [ ] Map Branch creation to `CreateHeadIfAbsent`, Checkpoint creation to `CreateFixedRootIfAbsent`, and rollback/Branch movement to `ReplaceHead`  
- [ ] Instrument or assert: accepted-reference payload bytes read = written = copied = 0 on all five operations, while recording metadata, coordination, durability-fence, and backend-materialization work separately  
- [ ] Implement recover-on-startup / after kill  
- [ ] Collision path: unequal bytes, same candidate id → reject  
- [ ] Bound caches/queues/FDs; cleanup on failure  
- [ ] Remove or hard-fail layer-history APIs on the new core path  
- [ ] Tests from this phase’s test-perf.md green  
- [ ] Publish the layout/API contract consumed by Phase 05; importer code never writes physical paths directly  
- [ ] Audit changed/new names and records: Version terminology only; Roots/Heads carry `AcceptedBinding`, never unchecked `VersionId`  

## Likely locations

| Area | First guess | Action |
|------|-------------|--------|
| LayerStack-0 engine | `crates/sandbox-runtime/layerstack/src/store/**` plus selected existing storage modules | main rewrite |
| Identity | phase 02 modules | call, don’t fork logic |
| New crate | none by default | only if 01 required it |

## Deliverables

- LayerStack-0 library/path in clean worktree  
- Exact versioned layout and migration-safe namespace contract  
- Test suite for COW + crash + OCC  

## Stop if

- Reference-only EphCoW cannot meet payload I/O `0/0/0` without opening or copying payload  
- Recovery cannot be defined  
- Design forces dual truth  
- A required implementation change introduces chunk/object-DAG truth, layer reconstruction, a new owner/boundary, or another writer; reopen Phase 01  

## Handoff to phase 04

App/workspace code may call LayerStack-0 for publish/read heads; Phase 05 may
call its import/admission APIs. Neither receives direct write authority over
the physical layout; no live cutover yet.

## Effort (rough)

Large — main engineering phase.

---

[PRD.md](PRD.md) · [test-perf.md](test-perf.md)
