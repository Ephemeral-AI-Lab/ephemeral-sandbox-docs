# Phase 04 — Wire product — Plan

**Status:** not started

## Prerequisites

- Phase 03 store tests green  

## Forward-work gate

Implement against the selected chain
`Candidate -> VersionId -> AcceptedVersion -> AcceptedBinding -> Head + HeadRevision or typed Root`.
Application code owns authorization and call ordering; it may not turn a raw
`VersionId` into a reference, write LayerStack-0 paths directly, or substitute
an archived CAS/CDC, PMSS, reflink, object-DAG, or layer-chain design.

## Approach

Thin wiring: **no new coordinator service**. The application keeps ordering;
LayerStack-0 owns accepted Versions and references; Workspace owners keep
mounts and processes.

## Work checklist

- [ ] Map each in-scope op to: auth → store and/or effects  
- [ ] Implement `file_read` committed vs `workspace_session_id`  
- [ ] Ensure write/edit require live workspace  
- [ ] Publish Workspace Candidate → Accepted Version → conditional Head transition through LayerStack-0  
- [ ] Checkpoint/fork hooks pass `AcceptedBinding` through LayerStack-0 reference-only paths  
- [ ] Explicit error for removed LayerStack-only behaviors  
- [ ] E2E tests from test-perf  
- [ ] Confirm no durable truth in observability-only paths  

## Likely locations

| Area | Action |
|------|--------|
| App / runtime ops | wire calls |
| Workspace crates | keep effect ownership |
| Store | already done; only call sites |

## Deliverables

- Lab-runnable product path  
- E2E test list green  

## Stop if

- Wiring reintroduces layer history as truth  
- Writes mutate an accepted Version  
- New god-object service appears without phase 01 mandate  

## Handoff to phase 05

Migrator can assume store + product path exist; import feeds store, not a third truth.

## Effort (rough)

Medium–large integration.

---

[PRD.md](PRD.md) · [test-perf.md](test-perf.md)
