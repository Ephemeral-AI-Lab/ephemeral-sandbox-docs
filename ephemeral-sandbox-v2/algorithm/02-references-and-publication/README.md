# Cluster 02 — References and publication

## Purpose

This cluster defines reference-level EphCoW and the sole selected-Version
transition. Its operations consume an AcceptedBinding; they never treat a raw
`VersionId` as authority.

```text
AcceptedBinding
  -> typed Root
  -> Head + HeadRevision
```

## Reading order

1. [Reference EphCoW](01-reference-ephcow.md) defines exact Head creation,
   replacement, and removal plus fixed typed Root creation and removal. Fork is
   Head creation, Checkpoint is fixed Root creation, and rollback is Head OCC;
   there is no generic Root retargeting.
2. [OCC publication](02-occ-publication.md) defines the one conditional Head
   replacement and clean stale-writer outcome.
3. [Composed publication pipeline](03-composed-publication-pipeline.md) connects
   Candidate capture, admission, binding issuance, and the OCC transition while
   preserving their separate costs and visibility points.
4. [Zero-payload reference demonstration](04-zero-payload-reference-demonstration.md)
   defines the structural and measured qualification proof for payload I/O
   `0/0/0`.

## Cluster invariants

- Heads and Roots contain AcceptedBindings, never unchecked raw IDs.
- One ReferencePlane authority implements all five lifecycle operations; only
  Heads support replacement and every mutation compares complete expected
  state.
- Reference-only operations cannot open a payload and report payload bytes
  read/written/copied `0/0/0`.
- The only state-changing Head linearization point is conditional replacement
  of one complete Head record under the LayerStack-0 transition gate.
- A stale writer never merges, rebases, refreshes its expectation, or retries
  against a newly observed Head.
- Admission may precede publication, but accepted-payload visibility is not Head
  selection.
- Authorization, request ordering, MCTS/rollout policy, and scores stay with
  application owners.

## Evidence and open choices

The capability split and OCC model are `INFERRED`; the current dependency
direction and existing primitive family are `SOURCE-VERIFIED`. No V2
zero-payload or concurrency test is `SPIKE-VERIFIED`. Phase 03 still selects
record, gate, fence, same-Version, custody, and finite-limit mechanics
`OPEN_WITHIN_R0`; product decisions `DEC-001`, `DEC-011`, `DEC-017`, and
`DEC-018` remain open.

Return `REOPEN_PHASE_01` if one transition authority and one complete-record
conditional replacement cannot close stale-writer behavior, or if a hard rule
requires payload access in a reference-only operation.

## API and workflow consumers

- [Shared API lifecycle map](../../api/README.md#14-api-operation-to-algorithm-navigation)
- [Manager lifecycle, Checkpoint, fork, and rollback callers](../../api/manager.md)
- [Runtime publication callers](../../api/runtime.md)
- [Phase 03 storage contract](../../phases/03-state-store/PRD.md)
- [Fork, Checkpoint, rollback, and CoW diagram](../../diagrams/03-fork-checkpoint-rollback-and-cow.md)
- [Publication/OCC diagram](../../diagrams/04-publish-occ-and-head-cas.md)

[Back to package index](../README.md)
