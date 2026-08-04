# Phase 02 — Version identity — Plan

**Status:** authorized by Phase 01.5 `PASS`; not started  
**Closure trace:** `019fcd32-b832-7750-9eb5-5f544e39c533`

## Prerequisites

- Root [architecture design](../../architecture_design.md) has a winner and
  `Phase 02 = GO` (if it records no winner, this phase does not start)  
- Phase 01.5 [contract-closure SPEC](../01-5-contract-closure/SPEC.md) has been
  executed with `PHASE_01_5: PASS` and `PHASE_02: GO`  

## Approach

Keep identity **pure**: no I/O policy, no mounts. Follow the selected owner and
identity boundary in [architecture_design.md](../../architecture_design.md): an
internal pure module in the existing LayerStack-0 package, not a new service or
crate.

Before changing code, apply the detailed-design
[forward-work naming and storage gate](../../design/README.md#forward-work-naming-and-storage-gate).
New APIs, types, tests, metrics, and documents use Version terminology. The
historical phase-folder slug does not authorize new `StateId` names.

## Work checklist

- [ ] Specify fact set included in one complete portable Version (align with product PRD)  
- [ ] Implement encode → canonical bytes → typed `VersionId`  
- [ ] Implement validators with explicit limits  
- [ ] Add golden vectors (stable `VersionId`s)  
- [ ] Add corrupt / oversized / deep-tree rejects  
- [ ] Add forced-ID and exact-byte comparison capability for Phase 03 collision tests  
- [ ] Prove identity cannot construct `AcceptedVersion` or `AcceptedBinding`; those are LayerStack-0 admission results  
- [ ] Grep for forbidden brands in identity types (path, overlay, docker id)  
- [ ] Document how LayerStack-0 admission will call these APIs  
- [ ] Audit changed/new names: no new `StateId`, State Store/PMSS, raw-ID accepted reference, or runtime-private identity field  

## Likely locations

| Area | Action |
|------|--------|
| Pure identity code | `crates/sandbox-runtime/layerstack/src/identity.rs` or an equivalent internal module selected by the architecture |
| Tests | unit tests beside module |
| This docs folder | update status when done |

## Deliverables

- Code + tests in clean worktree  
- Short “how to compute VersionId” note if not obvious from code  

## Stop if

- Identity requires mount or runtime-private facts  
- Cannot define a complete Version without layer history  
- A proposed identity API can manufacture `AcceptedVersion`/`AcceptedBinding` or put raw `VersionId` into a Root/Head  
- Design winner from 01 is contradicted  

## Handoff to phase 03

LayerStack-0 implements durable Version admission **on top of** these functions;
it must not redefine identity or treat a raw `VersionId` as accepted existence.

## Effort (rough)

Small–medium engineering.

---

[PRD.md](PRD.md) · [test-perf.md](test-perf.md)
