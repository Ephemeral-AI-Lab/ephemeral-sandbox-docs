# Ephemeral Sandbox V2 decision register

Date: **2026-08-04**  
Status: **ACTIVE — subordinate to the selected architecture**

## Purpose and authority

This is the compact decision register for implementation of the selected R0
architecture. It is not an architecture tournament and does not import the
older appendix decision ceremony.

Authority descends from the product [PRD](../../PRD.md), Phase 00
[SPEC](../../phases/00-freeze-rules/SPEC.md), Phase 01
[selection contract](../../phases/01-choose-design/SPEC.md), and the selected
[architecture](../../architecture_design.md). The design package and this
register elaborate that result. They cannot weaken a hard rule or accept a
product-owner decision.

## Status vocabulary

| Status | Meaning |
|---|---|
| `ACCEPTED_PRODUCT_CONTRACT` | Explicit product-owner contract accepted after Phase 01 that preserves the selected architecture family. |
| `ACCEPTED_PHASE_01` | Part of the selected R0 ownership/storage architecture; later phases implement rather than reselect it. |
| `OPEN_WITHIN_R0` | A named later phase may choose the detail while preserving R0's owner, storage family, identity boundary, writer/crash model, and hard rules. |
| `OWNER_DEC_OPEN` | Only the product owner may decide; this register records the stable architecture seam but does not select an outcome. |
| `PROPOSAL_EVIDENCE` | Historical or appendix idea available for evaluation; not accepted by reference. |
| `REJECTED_PHASE_01` | Conflicts with a hard rule or lacks a necessity case under R0. |
| `VERIFIED` | The owning phase has selected and passed its required executable proof; a link to evidence is required. |
| `SUPERSEDED` | Replaced by an explicitly authorized decision without erasing its history. |

`OPEN_WITHIN_R0` is not an architecture gap. If resolving an item would change
ownership, dependency direction, storage family, writer/OCC count, crash
behavior, portable/runtime boundary, migration truth, or require a new
architectural boundary, the item stops being local and Phase 01 must reopen.

## Accepted architecture decisions

| ID | Decision | Status | Record | Proof owner |
|---|---|---|---|---|
| `ADR-001` | Select R0: existing LayerStack package rewritten as LayerStack-0 filesystem-native complete-Version storage, with existing application/effect/lifecycle owners retained | `ACCEPTED_PHASE_01` | [ADR-001-r0-complete-version-storage.md](ADR-001-r0-complete-version-storage.md) | Phases 02–08 according to the architecture verification matrix |
| `ADR-002` | Rename the canonical complete-content identifier from historical `StateId` to `VersionId`; distinguish computed identity from accepted existence | `ACCEPTED_PRODUCT_CONTRACT` | [ADR-002-version-id-naming.md](ADR-002-version-id-naming.md) | Phase 02 API/types and all later consumers |

ADR-001 includes the complete joint decision. No separate “ownership winner”
or “storage winner” may override half of it.

## Delegated implementation decisions

IDs below are register handles, not accepted outcomes. The owning phase must
record the exact selection and evidence before changing the status to
`VERIFIED`.

| ID | Question | Owner | Status | Fixed boundary |
|---|---|---|---|---|
| `ID-001` | Exact canonical portable fact schema, grammar/codec, ordering, domain and version | Phase 02 | `OPEN_WITHIN_R0` | Complete, deterministic, portable, bounded canonical bytes; no runtime-private facts |
| `ID-002` | Exact typed digest algorithm, width, serialization, and `VersionId` representation | Phase 02 | `OPEN_WITHIN_R0` | ADR-002 fixes the name; digest covers the complete canonical stream; a raw ID proves neither equality nor existence; occupied ID always triggers full canonical-byte comparison |
| `ID-003` | Exact validation limits and streaming/comparison interfaces | Phase 02 | `OPEN_WITHIN_R0` | Every input/population finite; order-independent; forced-collision seam; no store I/O in pure identity |
| `STORE-001` | Exact on-disk paths, record encoding, versions, checksums, and temporary names | Phase 03 | `OPEN_WITHIN_R0` | One complete immutable payload closure plus small typed roots/heads and bounded private staging |
| `STORE-002` | Supported local-filesystem profile and exact fsync/atomic-replacement fence sequence | Phase 03 | `OPEN_WITHIN_R0` | Payload durable before reference; one atomic OCC head replacement; prior or complete new truth; unsupported profile fails readiness |
| `STORE-003` | Transition lock primitive and exact internal admission concurrency | Phase 03 | `OPEN_WITHIN_R0` | One process/filesystem-exclusive selected-Version transition authority; no second writer or silent merge/rebase |
| `STORE-004` | Read-custody representation and bounded last-root retirement implementation | Phase 03 | `OPEN_WITHIN_R0` | Captured immutable read survives head move; exact serialized final revalidation closes last-root/read race |
| `STORE-005` | Exact finite store limits, cleanup batches, instrumentation, and recovery debt caps | Phase 03 | `OPEN_WITHIN_R0` | Precharged resources, bounded recognizable debt, idempotent cleanup, fail-closed readiness |
| `WIRE-001` | Exact public/API wiring compatible with owner decisions | Phase 04 | `OPEN_WITHIN_R0` | Application retains auth/order; accepted payloads immutable; store OCC cannot be bypassed |
| `MIG-001` | Import progress record and restart-safe implementation details | Phase 05 | `OPEN_WITHIN_R0` | One-way importer under a monotone generation fence; normal V2 APIs; no dual writes; complete deletion unit |
| `QUAL-001` | Exact matched V2 performance qualification protocol and ship-candidate result | Phase 06 | `OPEN_WITHIN_R0` | Correctness first; Stage 4.6 remains `INCOMPARABLE`; no result or guarantee is predeclared |

## Product-owner decisions

All four decisions remain open. The current architecture is intentionally
stable across the presently stated outcomes.

| ID | Product question | Status | Stable R0 seam | Reopen if the owner requires… |
|---|---|---|---|---|
| `DEC-001` | Keep exact `file_blame` or accept a break? | **`OWNER_DEC_OPEN`** | Application-owned auditability side channel may key records by accepted Version/revision/publication; it is not canonical selected truth. | Provenance/audit history as canonical portable identity or selected-Version authority. |
| `DEC-011` | How long to observe after cutover before stripping compatibility? | **`OWNER_DEC_OPEN`** | The outcome controls temporary importer/compat deletion timing, never the one-writable-truth fence. | Dual writable legacy/V2 truth or permanent legacy dependencies in the V2 core. |
| `DEC-017` | What are no-session write/edit semantics and the exact V2 file-operation/target set, including `file_list` disposition? | **`OWNER_DEC_OPEN`** | Application may reject sessionless mutation or build a bounded candidate and use normal admission/publish/OCC. | Direct accepted-payload mutation, unchecked reference movement, or another writer/storage representation. |
| `DEC-018` | What is auth/revoke ordering under races? | **`OWNER_DEC_OPEN`** | Application defines authorization cutoff/disclosure; store OCC remains independent and mandatory. | Joint durable auth/store authority or another store linearization point/writer. |

An implementation or document may recommend an owner outcome and show its
effects, but it must not change `OWNER_DEC_OPEN` to accepted without explicit
product-owner action.

## Appendix decisions and proposals

The older appendix
[decision ledger](../../../implementation-plan/new_2.0_migration_implementation_plan/decisions/README.md)
is lower-authority background. Its design DECs—including `DEC-002`–`DEC-010`
and `DEC-012`–`DEC-016` referenced by Phase 00—remain
`PROPOSAL_EVIDENCE` unless the owning V2 phase independently selects a
compatible detail and records current proof here.

Appendix topology, component counts, algorithm families, physical profiles,
gate/epoch protocols, scorecards, or unrun selections are not accepted by a
link. A compatible idea may inform a Phase 02/03 decision; an incompatible idea
cannot override the product PRD, ADR-001, or the root architecture.

Historical Stage 4.6 is likewise evidence only and remains `INCOMPARABLE`. It
cannot select an implementation decision, reject R0, or establish a V2
performance guarantee.

## Phase 01 rejected decisions

| Family | Status | Reason |
|---|---|---|
| Layer/delta/parent-depth truth | `REJECTED_PHASE_01` | Violates complete immutable-Version truth. |
| Per-reference payload copies | `REJECTED_PHASE_01` | Violates zero-payload-I/O reference operations and shared payload. |
| Digest-only deduplication | `REJECTED_PHASE_01` | Violates exact occupied-ID comparison. |
| Silent stale merge/rebase | `REJECTED_PHASE_01` | Violates the one-point OCC rule. |
| Writable committed payloads | `REJECTED_PHASE_01` | Violates accepted-Version immutability. |
| Store-owned MCTS/auth/application policy | `REJECTED_PHASE_01` | Violates authority separation. |
| Dual-write migration | `REJECTED_PHASE_01` | Violates one writable truth. |
| New store crate/service/database/object DAG/archive/refcount authority by default | `REJECTED_PHASE_01` as proposed default | No evidenced R0 failure justifies the new boundary/failure/resource model. |

The last row may be reconsidered only through Phase 01 reopening with a
specific R0 failure and a joint replacement design. It is not a blanket ban on
all future research.

## Recording a later decision

A later phase should keep the update compact:

1. Name the register ID and exact selected outcome.
2. Link the governing phase PRD/SPEC and executable evidence.
3. Explain why the choice stays within ADR-001.
4. Record rejected local alternatives and material tradeoffs.
5. Mark `VERIFIED` only after the required proof passes.
6. If it crosses the boundary-change test in
   [01-ownership-and-boundaries.md](../01-ownership-and-boundaries.md#boundary-change-test),
   stop and reopen Phase 01 instead of recording a local choice.

This register does not require one ADR per constant or internal filename. Use
an ADR when a decision is durable, cross-component, expensive to reverse, or
needed to explain why an architecture boundary remains valid.

## References

- [Product hard rules](../../PRD.md#hard-rules-must-never-break)
- [Selected architecture](../../architecture_design.md)
- [Ownership and boundaries](../01-ownership-and-boundaries.md)
- [Phase 01 completed plan](../../phases/01-choose-design/PLAN.md)
- [ADR-001](ADR-001-r0-complete-version-storage.md)
- [ADR-002](ADR-002-version-id-naming.md)
