# Phase 05 — Migrator — Plan

**Status:** not started

## Prerequisites

- Phases 03–04 usable in lab  

## Approach

Smallest deletable translator. It reads fenced legacy truth and depends on pure
Version identity plus LayerStack-0 import/admission APIs. It owns **no**
permanent product policy and has no direct physical-layout write authority.

## Work checklist

- [ ] Enumerate legacy selections, explicit restore points, layers, fields, side channels, and live-workspace dispositions  
- [ ] Record the exact `LegacySelectionKey -> complete Candidate -> VersionId -> AcceptedVersion -> AcceptedBinding -> Head/Checkpoint Root` mapping  
- [ ] Prove layer IDs/parents/depth/whiteouts and runtime paths are decoder inputs only, never Version facts  
- [ ] Implement deterministic mapping + provenance  
- [ ] Implement import through LayerStack-0 APIs (idempotent where required); never write physical paths directly  
- [ ] Consume and test Phase 03's non-overlapping V2 namespace/layout contract  
- [ ] Reject corrupt/unsupported with typed errors  
- [ ] Implement generation fence checks on inventoried writers (lab)  
- [ ] Shadow compare harness (read-only)  
- [ ] Name retry artifacts migration progress records/cursors, never Checkpoints  
- [ ] Document how to delete this code in phase 08  
- [ ] Tests from test-perf green  

## Likely locations

| Area | Action |
|------|--------|
| New temp module/tool | add, mark temporary |
| Writer call sites | fence check only |
| LayerStack-0 | consume its admission/reference entrypoints; add only a narrow API if required, never a second algorithm or direct path writer |

## Deliverables

- Migrator + fence + lab shadow results  
- Deletion checklist for phase 08  

## Stop if

- Import needs permanent dual-write  
- Mapping not total for in-scope roots  
- Fence can be bypassed by a known writer  
- Phase 03 has not provided a migration-safe layout/API contract, or the importer must bypass it  
- Migration would require CDC/chunks, a second store, or permanent legacy facts in Version identity  

## Handoff to phase 06

Exact lab artifact (code + config) ready for full offline prove and cutover rehearsal.

## Effort (rough)

Medium.

---

[PRD.md](PRD.md) · [test-perf.md](test-perf.md)
