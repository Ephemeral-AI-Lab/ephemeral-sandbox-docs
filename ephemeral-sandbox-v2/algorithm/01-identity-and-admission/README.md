# Cluster 01 — Identity and admission

## Purpose

This cluster defines how bounded portable Candidate facts become canonical
bytes, a typed `VersionId`, one complete immutable AcceptedVersion, and an
AcceptedBinding. It owns no Head or Root transition.

```text
Candidate
  -> VersionId
  -> AcceptedVersion
  -> AcceptedBinding
```

## Reading order

1. [Canonical Version identity](01-canonical-version-identity.md) constrains
   portable facts, canonical bytes, domain separation, and Candidate identity.
2. [Complete Version admission](02-complete-version-admission.md) constructs and
   durably admits one complete filesystem-native payload closure.
3. [Complete-Version content addressing](03-complete-version-content-addressing.md)
   demonstrates occupied-address convergence and collision handling without
   introducing an object-store authority.
4. [CDC non-selection and reopening gate](04-cdc-non-selection-and-reopen-gate.md)
   records why cross-Version content-defined chunking is outside R0 and what
   exact evidence would require reopening Phase 01.

## Cluster invariants

- `VersionId` is typed content-derived Candidate identity, not equality,
  existence, admission, or reference authority.
- Equality at an occupied `VersionId` requires full canonical-byte comparison.
- Equal canonical bytes converge on one complete physical payload closure.
- A full-byte mismatch is a collision error; the occupant remains unchanged.
- Only LayerStack-0 admission creates or revalidates an AcceptedBinding.
- Accepted truth is one complete immutable Version; no Chunk, manifest, parent,
  layer, or depth reconstruction is required.

## Evidence and open choices

The selected complete-Version family is `INFERRED` from the accepted R0
architecture and its source-placeable ownership is `SOURCE-VERIFIED` against
the sealed e497 base. No V2 admission or performance spike is
`SPIKE-VERIFIED`. Codec, digest, exact limits, paths, records, fences, and
filesystem qualification remain `OPEN_WITHIN_R0` for Phases 02 and 03.

Return `REOPEN_PHASE_01` only if bounded canonical identity, full-byte
convergence, or complete immutable payload admission cannot satisfy a hard
rule without changing storage family or authority.

## Consumers

- [Shared API contract](../../api/README.md)
- [Runtime publication API](../../api/runtime.md)
- [Phase 02 identity contract](../../phases/02-state-identity/PRD.md)
- [Phase 03 admission contract](../../phases/03-state-store/PRD.md)
- [Publication/OCC diagram](../../diagrams/04-publish-occ-and-head-cas.md)

[Back to package index](../README.md)
