# Cluster 04 — Durability and lifecycle

## Purpose

This cluster defines crash-safe visibility, fail-closed recovery, and bounded
retirement of whole complete-Version payload closures.

## Reading order

1. [Durability and recovery](01-durability-and-recovery.md) defines
   payload-before-reference ordering, crash-prefix classification, quarantine,
   and bounded startup work.
2. [Retirement and cleanup](02-retirement-and-cleanup.md) uses exact Head/Root
   reachability plus custody and final serialized revalidation before detaching
   a complete payload closure.

## Cluster invariants

- An AcceptedBinding cannot become durably referenceable before its complete
  accepted payload.
- Startup exposes prior truth, complete new truth, or fails closed—never a
  fieldwise hybrid.
- Retirement requires no Head, no Root, and no read custody after final
  revalidation under transition authority.
- Staging, orphan, quarantine, recovery, and cleanup debt are finite.
- Retirement is whole-Version lifecycle management, not Chunk-graph tracing or
  persistent refcount authority.

## Evidence and open choices

The existing primitive family is `SOURCE-VERIFIED`; V2 crash ordering,
recovery, and retirement are `INFERRED`; no V2 crash matrix is
`SPIKE-VERIFIED`. Phase 03 selects exact records, checksums, generations,
qualified fences, supported filesystems, batches, and limits
`OPEN_WITHIN_R0`.

Return `REOPEN_PHASE_01` if no supported local filesystem can provide the
required prior-or-complete-new behavior or bounded exact reachability plus
custody cannot close retirement races.

## Consumers

- [Manager lifecycle API](../../api/manager.md)
- [Observability API](../../api/observability.md)
- [Phase 03 storage contract](../../phases/03-state-store/PRD.md)
- [Read lifetime, recovery, and retirement diagram](../../diagrams/06-read-lifetime-recovery-and-retirement.md)

[Back to package index](../README.md)
