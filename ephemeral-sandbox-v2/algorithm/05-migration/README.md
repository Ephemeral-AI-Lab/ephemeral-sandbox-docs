# Cluster 05 — Migration

## Purpose

This cluster defines one-way translation from fenced legacy values into
ordinary R0 Candidates and admission while maintaining at most one writable
selected-Version truth.

## Reading order

1. [One-way migration](01-one-way-migration.md) defines legacy-read fencing,
   translation, restartable progress, generation cutover, rollback before
   commit, and deletion of compatibility code.

## Cluster invariants

- Legacy facts enter V2 through ordinary Candidate validation and admission.
- Legacy layer IDs, parent/depth, whiteouts, mount paths, and host paths never
  become V2 identity.
- Before cutover, legacy is the only writable selected truth; after committed
  cutover, LayerStack-0 is the only writable selected-Version truth.
- Compatibility code is temporary, isolated, observable, and deletable.

## Evidence and open choices

Legacy boundaries and selected ownership are `SOURCE-VERIFIED`; the one-way
protocol is `INFERRED`; no migration rehearsal is `SPIKE-VERIFIED`. Phase 05
selects progress-record and batch spellings within the Phase 03 generation and
one-writer fences `OPEN_WITHIN_R0`. `DEC-011` remains `OWNER_DEC_OPEN`.

Return `REOPEN_PHASE_01` if migration requires dual writable truth, imports
runtime-private facts into Version identity, or cannot delete its compatibility
path after cutover.

## Consumers

- [Manager lifecycle API](../../api/manager.md)
- [Migration design](../../design/08-migration-and-cutover.md)
- [Migration and cutover diagram](../../diagrams/07-migration-and-cutover.md)

[Back to package index](../README.md)
