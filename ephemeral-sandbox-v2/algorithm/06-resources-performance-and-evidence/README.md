# Cluster 06 — Resources, performance, and evidence

## Purpose

This cluster defines honest worst-case resource costs, finite admission and
cleanup bounds, diagnostic-only observability, and the evidence matrix required
before making speed or memory claims.

## Reading order

1. [Resources, complexity, and observability](01-resources-complexity-and-observability.md)
   defines shared variables, asymptotic bounds, resource ownership, and
   zero-payload counters.
2. [Performance demonstration matrix](02-performance-demonstration-matrix.md)
   defines sealed workloads, measurement scopes, pass/fail gates, and evidence
   states for admission, reference, publication, materialization, recovery,
   retirement, and migration.

## Cluster invariants

- Staging, memory, descriptors, workers, queues, locks, custody, recovery, and
  cleanup debt are finite and fail closed.
- Reference `0/0/0`, admission byte movement, and runtime materialization byte
  movement have disjoint measurement scopes.
- Observability consumes facts and never issues a binding, advances a Head,
  installs custody, declares equality, or authorizes cleanup.
- Asymptotic analysis is not benchmark evidence.
- Stage 4.6 remains `INCOMPARABLE`; no V2 performance winner or production
  guarantee is claimed.

## Evidence and open choices

The e497 branch, commit, and clean-state seal are source metadata rather than
an evidence label. Current source facts and the existence/provenance of the
historical measurement record are `SOURCE-VERIFIED`; that record's comparison
status remains `INCOMPARABLE`. The V2 resource and measurement contracts are
`INFERRED`. No V2 result is `SPIKE-VERIFIED`. Phase 02/03/06 limits, datasets,
targets, tracing mechanism, and qualification environment remain
`OPEN_WITHIN_R0`, with the final performance verdict `TARGET_UNSELECTED`.

Return `REOPEN_PHASE_01` only if a selected hard performance/resource target,
measured comparably against a sealed implementation, proves R0 cannot qualify
without changing storage family or authority.

## Consumers

- [Observability API](../../api/observability.md)
- [Performance design](../../design/07-performance-and-optimization.md)
- [Phase 02 test/performance contract](../../phases/02-state-identity/test-perf.md)
- [Phase 03 test/performance contract](../../phases/03-state-store/test-perf.md)
- [Data movement diagram](../../diagrams/README.md)

[Back to package index](../README.md)
