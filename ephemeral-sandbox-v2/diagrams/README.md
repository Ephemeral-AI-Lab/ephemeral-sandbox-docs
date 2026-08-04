# Ephemeral Sandbox V2 architecture diagrams

**Status:** selected R0 views plus explicitly separated CAS+CDC alternative
research

The diagrams in this folder explain the architecture through its durable
objects and important operation workflows. They do not replace the governing
[product requirements](../PRD.md), the Phase 01
[selection input contract](../phases/01-choose-design/SPEC.md), or the selected
[architecture output](../architecture_design.md). If a diagram conflicts with
a higher-authority contract, the higher-authority contract wins and the
diagram must be corrected.

ASCII is the primary diagram format. It keeps the views readable in terminals,
code review, and plain-text exports without requiring a renderer. Exported
images may be added later, but they are never the sole or normative source.

## Reading order

| # | View | Architectural question |
|---|---|---|
| 1 | [Before and after architecture](01-before-and-after-architecture.md) | What ownership and selected-truth model changes under R0, and what remains at its current owner? |
| 2 | [Storage model and content addressing](02-storage-model-and-content-addressing.md) | What objects are authoritative, how does a complete Candidate become an Accepted Version, and how are equal/colliding IDs handled? |
| 3 | [Fork, checkpoint, rollback, and COW](03-fork-checkpoint-rollback-and-cow.md) | How do Branch Heads and fixed Checkpoint Roots share immutable Versions, where do writes occur, and what does COW mean in R0? |
| 4 | [Publish, OCC, and head CAS](04-publish-occ-and-head-cas.md) | How are payload admission and selected-head publication separated, and where does OCC linearize? |
| 5 | [Rollout and branch orchestration](05-rollout-and-branch-orchestration.md) | How do MCTS or agent rollouts compose generic store primitives while policy remains outside storage? |
| 6 | [Read lifetime, recovery, and retirement](06-read-lifetime-recovery-and-retirement.md) | How do captured reads, custody, crashes, cleanup, and last-root retirement remain safe? |
| 7 | [Migration and cutover](07-migration-and-cutover.md) | How does writer authority move once from legacy truth to V2 truth without a dual-writer interval? |

The root [product diagrams](../PRD.md#diagram--product-context) and
[program diagrams](../PLAN.md#diagram--phase-order) remain short orientation
views. This folder owns the detailed architectural and operational
explanations.

The [storage-diagram package](storage/README.md) extends these selected R0
views with the proposed manifest/Chunk CAS+CDC family. It does not silently
change the current Phase 01 decision or redefine EphCoW. The alternative's
candidate constraint is backend-agnostic: no custom filesystem or
storage-specific clone feature is a correctness dependency. See the focused
[CDC boundaries and resynchronization diagram](storage/08-cdc-boundaries-resynchronization-and-reuse.md)
for the missing Chunk-boundary algorithm view.

## Comparison labels

Before/after panels must identify what kind of statement they make. A diagram
must not present a rejected alternative as historical behavior or present an
unimplemented R0 mechanism as source-verified.

| Label | Meaning |
|---|---|
| `CURRENT e497 — SOURCE-VERIFIED` | A focused fact measured or traced in the pinned current implementation and Phase 00 inventory. |
| `SELECTED R0 — ARCHITECTURE DECISION` | A Phase 01 ownership/storage rule that later implementation must preserve. |
| `FORBIDDEN ALTERNATIVE — NOT HISTORICAL` | A boundary or behavior shown only to explain what the selected architecture rejects. |
| `DEFERRED PHASE 02/03/05 DETAIL` | An exact codec, hash, disk, synchronization, resource-limit, or migration-record choice delegated within R0. |

Historical Stage 4.6 evidence remains `INCOMPARABLE`. No diagram may use it as
a V2 latency baseline, benchmark winner, performance guarantee, or numerical
before/after result.

## ASCII conventions

The diagrams use text labels rather than color so they retain their meaning in
every renderer.

```text
+----------------------+    permanent component or authoritative object
|                      |
+----------------------+

[temporary/private]         staging, custody, migration, or cleanup state

---->                      permanent call, dependency, or state transition
- - ->                     temporary, diagnostic, or non-authoritative edge
===>                       authoritative publication or writer-mode transition
-X->                       forbidden transition or dependency
```

Each arrow must be labeled when its authority or payload behavior is not
obvious. Diagrams that show reference-only operations state payload bytes read,
written, and copied explicitly; the phrase "zero-copy" alone is insufficient.

## Terms that must remain distinct

| Term | Meaning in these diagrams |
|---|---|
| Content-addressed admission | Derive a typed `VersionId` from the complete canonical portable value, inspect occupancy, and admit/reuse/reject by full canonical-byte comparison. |
| Head compare-and-swap / OCC | Replace one complete head record only when current `(AcceptedBinding, HeadRevision)` equals the expected record. |
| Logical COW | Fork/checkpoint initially share an accepted binding; mutation occurs in a separate Workspace Candidate and publishes a new immutable complete Version. |
| AcceptedBinding | LayerStack-0-issued or LayerStack-0-revalidated evidence that an exact payload has completed occupied-ID admission; it is not a raw digest. |
| Rollout | Caller-owned MCTS/agent branch policy composed from Branch Heads, fixed Roots, Workspaces, execution, admission, reads, and Head OCC transitions. |

R0 does not select or require filesystem-specific cloning, block-level COW,
hard-link payload trees, chunk deduplication, an object DAG, a database, or
rollout-aware Version storage.

## Required explanation around every diagram

Every detailed view records:

1. its authority and purpose;
2. a legend for local symbols;
3. a plain-English walkthrough;
4. the invariants the implementation must preserve;
5. selected architecture versus delegated implementation details;
6. verification ownership in later phases; and
7. conditions that would reopen Phase 01.

The diagrams describe conceptual roles and outcomes. They do not prematurely
select Phase 02's canonical grammar or digest, Phase 03's exact on-disk names,
record encodings, locking and durability sequence, or Phase 05's exact
migration progress records.

## Update rule

When an implementation decision is accepted inside R0, update the owning
design/API/algorithm document first, then update every affected diagram. A new
service, package-level authority, selected-Version writer, storage family,
runtime-private identity fact, payload-bearing reference path, layer truth, or
dual-write migration is not a diagram correction: it requires the Phase 01
reopening process described by [architecture_design.md](../architecture_design.md#15-architecture-verification-and-reopening).
