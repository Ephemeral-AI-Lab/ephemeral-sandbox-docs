# Ephemeral Sandbox V2 — detailed design package

**Status:** selected design contract; implementation/qualification `NOT_RUN` ·
**Selected architecture:** R0  
**Authority:** subordinate to the product [PRD](../PRD.md) and the selected
Phase 01 [architecture design](../architecture_design.md)

## Purpose

This folder turns the Phase 01 R0 decision into scoped contracts that Phases
02–08 can implement and prove. It does not run a second architecture selection,
copy the older appendix tournament, or claim that deferred algorithms and
performance results already exist.

The root [architecture design](../architecture_design.md) is the integrated
Phase 01 baseline. Files here may add exact, phase-owned details only when those
details satisfy that baseline. If a detail would change the selected owner,
dependency direction, storage family, identity boundary, writer count, crash
model, one-writable-truth rule, or need for an architectural boundary, stop and
reopen Phase 01 instead of editing the baseline by implication.

## Authority order

1. Product [PRD](../PRD.md), especially hard rules 1–10.
2. Completed Phase 00 [SPEC](../phases/00-freeze-rules/SPEC.md) and measured
   inventories.
3. Phase 01 [SPEC](../phases/01-choose-design/SPEC.md) and selected
   [architecture design](../architecture_design.md).
4. The owning phase's `PRD.md`, `PLAN.md`, and `test-perf.md`.
5. These scoped design files and accepted records under [decisions/](decisions/).
6. The older implementation-plan appendix as background evidence only.

When two files at the same level appear inconsistent, use the narrower owning
file only if it still satisfies every higher-authority contract. Otherwise
record the conflict and stop the affected phase.

## Status vocabulary

| Label | Meaning |
|---|---|
| `ACCEPTED_PRODUCT_CONTRACT` | Explicit product-owner contract accepted after Phase 01 without changing the selected architecture family. |
| `ACCEPTED_PHASE_01` | Accepted joint architecture decision recorded by Phase 01. |
| `LOCKED_PHASE_01` | Part of the selected R0 ownership/storage architecture; later phases may implement but not change it. |
| `OPEN_WITHIN_R0` | A later phase must select the detail without changing R0's owner, storage family, authority, identity boundary or hard-rule behavior. |
| `SELECT_IN_PHASE_02` | Exact portable-identity detail Phase 02 must select and prove within R0. |
| `SELECT_IN_PHASE_03` | Exact durable-store detail Phase 03 must select and prove within R0. |
| `SELECT_IN_PHASE_05` | Exact temporary migration/fence detail Phase 05 must select and prove within R0. |
| `OWNER_DEC_OPEN` | Product-owner choice remains open; no document or agent may accept it on the owner's behalf. |
| `IMPLEMENTED` | The owning phase has implemented the contract on its sealed source base, but later qualification may remain. |
| `VERIFIED` | The required executable evidence exists and the owning `test-perf.md` passes. |
| `REOPEN_PHASE_01` | New evidence changes an architectural premise; downstream work stops pending a new joint decision. |

`INFERRED`, `SOURCE-VERIFIED`, `SPIKE-VERIFIED`, and `OPEN` retain the evidence
meanings used by the Phase 01 architecture document. Implementation status and
evidence quality are separate dimensions.

## Design map

| File | Scope | Current selection owner |
|---|---|---|
| [01-ownership-and-boundaries.md](01-ownership-and-boundaries.md) | Authorities, dependency direction, process/privilege boundaries, one writer | Phase 01 (`LOCKED_PHASE_01`) |
| [02-state-identity.md](02-state-identity.md) | Version identity: portable facts, canonical bytes, typed `VersionId`, exact comparison | Phase 01 constraints plus ADR-002 naming; Phase 02 exact choices |
| [03-state-store.md](03-state-store.md) | LayerStack-0 Version storage: Versions, Roots/Heads, staging, admission, publication, recovery, retirement | Phase 01 family; Phase 03 exact choices |
| [04-algorithms-and-call-flows.md](04-algorithms-and-call-flows.md) | Transition state machines, linearization, I/O and cleanup contracts | Phase 01 semantics; Phases 02–05 implementation detail |
| [05-concurrency-durability-recovery.md](05-concurrency-durability-recovery.md) | Histories, crash prefixes, filesystem proof obligations | Phase 01 model; Phase 03 exact proof |
| [06-resources-security-observability.md](06-resources-security-observability.md) | Finite accounting, untrusted inputs, diagnostic-only observability | Phases 02–06 |
| [07-performance-and-optimization.md](07-performance-and-optimization.md) | Cost model, hypotheses, matched measurement, result ledger | Phase 01 stance; Phase 06 qualification |
| [08-migration-and-cutover.md](08-migration-and-cutover.md) | One-way import, generation fence, cutover and deletion boundary | Phases 05, 07, and 08; `DEC-011` remains open |
| [09-source-and-implementation-map.md](09-source-and-implementation-map.md) | Exact package placement, `KEEP`/`REWRITE`/`DELETE`/`ADD`, phase ownership | Phase 01 placement; later source verification |
| [10-verification-matrix.md](10-verification-matrix.md) | Hard-rule and architecture-claim traceability to executable evidence | Phases 02–08 |
| [decisions/README.md](decisions/README.md) | Accepted architecture records, delegated choices, open owner decisions | Per-record owner |
| [Architecture diagrams](../diagrams/README.md) | ASCII before/after and operational views of the selected contracts | Explanatory; subordinate to the owning contract above |

## What Phase 01 locked

- `sandbox-runtime-layerstack` remains the selected-Version owner and is rewritten
  for complete immutable V2 Versions.
- Existing application owners retain authorization, request ordering, expected
  head capture, and product orchestration.
- Existing workspace, OverlayFS, namespace, exec, manager, daemon, provider,
  and observability owners retain their effect/lifecycle/diagnostic roles.
- Storage is filesystem-native complete immutable payload closures plus typed
  roots/heads, bounded private staging, one OCC reference transition, exact
  occupied-ID comparison, and fail-closed recovery.
- Layer chains, parent/depth reconstruction, squash/merge truth, runtime-private
  portable identity, silent merge/rebase, and dual writable truth are excluded.
- R0 adds no new crate, service, helper process, protocol, deployment unit,
  authority, or independent resource pool by default.

## Product terminology accepted after Phase 01

[ADR-002](decisions/ADR-002-version-id-naming.md) renames the typed complete
canonical identity from historical `StateId` to `VersionId`. The change is a
product/API naming contract only: it does not alter R0 ownership, storage
family, canonical bytes, occupied-ID comparison, admission, or recovery.
`AcceptedVersion` and `AcceptedBinding` distinguish a computed identifier from
verified durable admission.

The filenames `02-state-identity.md`, `03-state-store.md`, and the corresponding
phase-folder slugs are stable historical routing names, not the forward product
vocabulary. Their headings and all new APIs, types, tests, metrics, and prose
use **Version identity** and **LayerStack-0 Version storage**.

## Forward-work naming and storage gate

Every Phase 02+ task, prompt, plan update, design addition, and implementation
handoff must preserve this chain:

```text
Candidate
  -> VersionId
  -> AcceptedVersion
  -> AcceptedBinding
  -> Head + HeadRevision or typed Root
```

Use **LayerStack-0** for the engine, **EphCoW** for the branch/admit/publish CoW
architecture, **Version** for the complete immutable portable value, and
`VersionId` for its typed candidate identity. A raw `VersionId` is never a
Root/Head capability and never proves equality or durable existence.

The locked storage model is filesystem-native complete-Version storage:

```text
versions/<VersionId>/payload/   one complete immutable accepted closure
heads/<selector>                AcceptedBinding + HeadRevision
roots/<kind>/<root-id>          typed reachability to AcceptedBinding
staging/<transaction-id>/       bounded private Candidate work
control/                        format/generation/recovery roles
```

The names above are conceptual; Phase 03 selects non-overlapping physical path
spellings and records. The family is not conceptual: Phase 03 may not select
CDC, cross-Version chunks, a Merkle/object DAG, pack/catalog authority, a layer
chain, or a new store boundary as an optimization. Any such need is
`REOPEN_PHASE_01`.

Older material under [`implementation-plan/`](../../implementation-plan/README.md)
is evidence-only. Its “Accepted” labels, `StateId`, raw root identifiers,
CDC/CAS/PMSS layouts, component/API counts, custom algorithms, exact limits,
phase sequence, and handoffs do not flow forward automatically.

## What later phases may still select

| Detail | Owner | Constraint |
|---|---|---|
| Portable fact grammar, canonical codec, digest and limits | Phase 02 | Must remain pure, complete, deterministic, bounded, typed, runtime-neutral, and exactly comparable. |
| Disk spellings, record/checksum encoding, local filesystem profile, safe fence sequence, read custody and finite store limits | Phase 03 | Must preserve complete immutable payloads, payload-before-reference durability, one OCC point, zero-payload reference moves and fail-closed recovery. |
| Application operation mapping | Phase 04 plus product owner where required | Must preserve store/effect separation and open decision seams. |
| Import progress/fence encoding | Phase 05 | Must be one-way, use ordinary V2 admission, keep one writable truth, and be deletable. |
| Qualification measurements | Phase 06 | Must use the exact candidate artifact; Stage 4.6 remains incomparable. |
| Observation-window duration | Product owner (`DEC-011`) | Changes removal timing only; never permits dual writes. |

The exact codec, digest, disk encoding, synchronization sequence, resource
constants, benchmark result, and owner decisions are not Phase 01 results.

## Open product decisions

The selected architecture isolates these choices; it does not silently close
them:

| ID | Status | Stable seam |
|---|---|---|
| `DEC-001` — exact `file_blame` | `OWNER_DEC_OPEN` | Application auditability may key non-canonical records by accepted Version/revision/publication. |
| `DEC-011` — observation window | `OWNER_DEC_OPEN` | Affects temporary compatibility removal timing, never writer count. |
| `DEC-017` — operation surface and sessionless writes/edits | `OWNER_DEC_OPEN` | Application rejects the mutation or publishes a bounded candidate through the same OCC path; accepted payloads remain immutable. |
| `DEC-018` — auth/revoke race ordering | `OWNER_DEC_OPEN` | Application owns the cutoff/disclosure rule; store OCC remains independent and mandatory. |

## Document update rule

Every material implementation choice added here must state:

1. owning phase and status;
2. inputs, outputs, invariants and typed failure behavior;
3. resource and cleanup obligations;
4. evidence path or explicitly `NOT_RUN` result;
5. whether it is a local choice or a Phase 01 reopening trigger; and
6. which older statement it supersedes, if any.

Do not publish guessed limits, LOC totals, Stage 4.6 speedups, unrun test
results, or open owner choices as settled facts.

## Current program state

```text
Phase 00: complete after pass 2
Phase 01: complete — R0 selected
Phase 02: next; identity contract fixed, exact local choices not yet selected
Phase 03: not started; store contract fixed, exact filesystem mechanics not yet selected
Performance guarantee: none
Live cutover: not authorized
```

Parent documents: [README](../README.md) · [PRD](../PRD.md) ·
[PLAN](../PLAN.md) · [architecture design](../architecture_design.md)
