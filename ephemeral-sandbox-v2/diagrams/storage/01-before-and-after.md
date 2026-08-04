# Before and after — legacy LayerStack, selected R0, and proposed CAS+CDC

Date: **2026-08-04**

Status: **current-source comparison plus selected/proposed target views**

> `CURRENT e497 — SOURCE-VERIFIED`: legacy storage and ownership facts.
>
> `SELECTED R0 — LOCKED_PHASE_01`: complete immutable payload and reference semantics.
>
> `PROPOSED`: CAS+CDC cross-Version sharing; not part of selected R0.
>
> `PROPOSED CANDIDATE CONSTRAINT`: backend-agnostic durable and runtime
> Workspace contracts, with ordinary-I/O materialization as the correctness
> profile.

## Question answered

What durable truth is being replaced, what does selected R0 already require,
and which additional CAS+CDC mechanisms discussed for LayerStack-0 still need
a new architecture decision?

This document is subordinate to the product [hard rules](../../PRD.md#hard-rules-must-never-break),
the Phase 00 [measured evidence](../../phases/00-freeze-rules/SPEC.md), the
Phase 01 [selection contract](../../phases/01-choose-design/SPEC.md), and the
selected [architecture](../../architecture_design.md). The broader ownership
comparison remains in [Before and after architecture](../01-before-and-after-architecture.md).

Historical Stage 4.6 evidence is `INCOMPARABLE`. It is not used here as a
speed baseline, a ranking input, or a V2 performance claim.

## Legend

```text
[I]  immutable durable object
[M]  mutable durable reference
[R]  runtime-private object/effect
[O]  unresolved architecture mechanism

---->  reference, selection, or metadata/control flow
====>  payload-byte flow
-X-->  forbidden V2 truth or transition
```

The labels `V1`, `V2`, and `V3` are readable names for Accepted Versions. The
normative typed identifier is `VersionId`; roots and heads carry an
`AcceptedBinding`, not an unchecked raw identifier.

## Panel A — measured legacy selected truth

```text
+-------------------------------------------------------------------------+
| CURRENT e497 -- SOURCE-VERIFIED                                         |
|                                                                         |
|  sandbox-runtime-layerstack                                             |
|                                                                         |
|  manifest.json [M]                                                      |
|       |                                                                 |
|       | ordered LayerRef selection                                      |
|       v                                                                 |
|  +----------+      +----------+      +----------+                       |
|  | layer L1 | ---> | layer L2 | ---> | layer L3 |                       |
|  +----------+      +----------+      +----------+                       |
|       \                 |                 /                              |
|        \                |                /                               |
|         +========== compose/project ==========+                         |
|                                                |                        |
|                                                v                        |
|                                      selected filesystem view           |
|                                                                         |
|  Related current mechanisms:                                            |
|    layers, parent/order/depth, projection, merge, squash, leases         |
|                                                                         |
|  Runtime effects remain separate:                                       |
|    workspace / OverlayFS / namespace / exec / host paths                |
+-------------------------------------------------------------------------+
```

Measured e497 facts relevant to this comparison:

- `sandbox-runtime-layerstack` is the durable history home.
- Current durable selection uses a manifest and ordered layers.
- Current code contains layer projection, depth, squash, merge, and lease
  behavior.
- Current publish may auto-merge compatible directory creation and eligible
  text edits. That is legacy evidence, not permitted V2 stale behavior.
- `sandbox-runtime` primarily owns application ordering and composition.
- Workspace, OverlayFS, namespace, and exec packages own live Linux effects.
- Observability reads diagnostics and is not selected-Version authority.

The current layout is not presented as a V2 candidate. Product hard rule 1
forbids a logical layer chain as selected truth, and hard rule 5 forbids silent
merge or rebase after a stale OCC expectation.

## Panel B — selected R0 replacement

```text
+-------------------------------------------------------------------------+
| SELECTED R0 -- LOCKED_PHASE_01                                          |
|                                                                         |
|  Branch/product selection ----> Head [M] ----+                          |
|                                              | accepted binding          |
|  Checkpoint-to-existing -----> Root [I] -----+                          |
|                                              |                           |
|                                              v                           |
|                                  accepted Version V3 [I]                |
|                                  complete immutable Version             |
|                                  one payload closure                    |
|                                  no parent/depth reconstruction          |
|                                                                         |
|  private Workspace [R]                                                  |
|     upperdir / writable Candidate                                       |
|             |                                                           |
|             | admission may process payload                             |
|             v                                                           |
|     new complete accepted Version V4 [I]                                |
|             |                                                           |
|             '---> one conditional OCC Head transition                  |
|                                                                         |
|  reference-only fork/checkpoint/rollback-to-existing:                   |
|      payload bytes read    = 0                                          |
|      payload bytes written = 0                                          |
|      payload bytes copied  = 0                                          |
+-------------------------------------------------------------------------+
```

Selected R0 changes the durable semantics without moving their owner:

```text
owner continuity:
    crates/sandbox-runtime/layerstack stays the selected-Version owner

truth replacement:
    ordered legacy layers
        -> one complete immutable payload closure per Accepted Version

selection replacement:
    layer-chain manifest selection
        -> small typed Roots and OCC-controlled Heads

write replacement:
    legacy merge/squash/layer publication
        -> private Candidate admission + one strict Head transition
```

R0 does not require an accepted Version to depend on any earlier Version:

```text
Version V3 needs its own complete payload closure.

Version V3 -X-> Version V2 parent for reconstruction
Version V3 -X-> Version V1 parent for reconstruction
```

## Panel C — proposed CAS+CDC extension

The discussed CAS+CDC model keeps the **logical** requirement that every
Version is a complete workspace, but proposes a different **physical**
representation for file bytes.

```text
+-------------------------------------------------------------------------+
| PROPOSED CAS+CDC STORAGE FAMILY -- NOT SELECTED                         |
|                                                                         |
|  Branch agent-a ----> accepted Workspace Version V3 [I]                 |
|                              |                                          |
|                              v                                          |
|                    complete Workspace manifest [I]                      |
|                                                                         |
|                    workspace/                                           |
|                    +-- app/main.py  -> [C01, C02]                       |
|                    +-- data.bin    -> [C03, C07, C08]                   |
|                    '-- README.md   -> [C09]                             |
|                              |                                          |
|                              | complete ordered Chunk references         |
|                              v                                          |
|                    Chunk content-addressed storage [I]                   |
|                    C01 C02 C03 C07 C08 C09                              |
|                              |                                          |
|                              v                                          |
|                    backend-neutral read contract [P]                    |
|                              |                                          |
|                              v                                          |
|                    runtime Workspace adapter [P]                        |
|                              |                                          |
|                    ordinary-I/O WorkspaceBase [R]                       |
|                              |                                          |
|                    current Linux lowerdir [R]                           |
|                              + private upperdir/workdir [R]              |
|                              |                                          |
|                              v                                          |
|                    full merged Workspace [R]                             |
+-------------------------------------------------------------------------+
```

The proposed model must preserve this distinction:

```text
logical completeness:
    V3's manifest directly describes every accepted path and file byte.
    V3 does not apply a delta to V2.

physical sharing:
    V3 may reference immutable Chunks also referenced by V1 or V2.
    Sharing does not make an earlier Version a reconstruction parent.
```

However, this is not a Phase 03 detail inside selected R0. The selected
architecture explicitly did not select an object/Chunk DAG, cross-Version
Chunk deduplication, tracing reclamation, or the backend-neutral CAS+CDC
contracts. The candidate now rules out a custom filesystem or
storage-specific clone feature as a correctness dependency. The
proposed family changes:

- the physical payload and equality model below a complete Version;
- occupied-ID and collision checks at the Chunk boundary;
- publication and recovery across many immutable objects;
- Version and Chunk reachability/retirement;
- backend capability semantics for read/admission/recovery/retirement;
- runtime activation/materialization, cache/read-custody, and resource bounds;
  and possibly
- package, process, filesystem, or privilege boundaries.

It therefore requires Phase 01 reopening before selection or implementation.

## Panel D — local before and after for one edited workspace

```text
CURRENT e497 -- SOURCE-VERIFIED CONCEPT

  previous selected layer composition
              |
              + new writable changes
              |
              v
        publish another layer
              |
              v
      updated ordered manifest
              |
              v
        later depth/squash work
```

```text
SELECTED R0 -- ARCHITECTURE DECISION

  complete accepted Version V3 [I]
              |
              v
       private Workspace [R]
       writes cannot mutate V3
              |
              v
       complete Candidate [T]
              |
              v
  admit/reuse complete payload V4 [I]
              |
              v
  conditional OCC Head transition

  stale expectation -> clean stale; no merge/rebase
```

```text
PROPOSED CAS+CDC PHYSICAL PATH

  changed files in private Workspace
              |
              =====> content-defined chunking
              |
              =====> write only absent immutable Chunks
              |
              -----> complete Workspace manifest for V4
              |
              -----> durable multi-object admission/recovery
              |
              -----> conditional OCC Head transition

  This path is explanatory, not selected or benchmark-proven.
```

## What disappears from the permanent V2 core

| Legacy concept | V2 disposition | Reason |
|---|---|---|
| Ordered durable layer-chain truth | `DELETE V2 CORE` | A selected Version must be complete and parent-independent. |
| Layer parent/depth reconstruction | `DELETE V2 CORE` | Normal reads cannot depend on history depth. |
| Squash as selected-Version maintenance | `DELETE V2 CORE` | Complete Versions need no history compaction to become readable. |
| Silent compatible merge/rebase after stale publication | `DELETE V2 CORE` | One strict OCC transition; stale loses cleanly. |
| Writable committed payload | `FORBIDDEN` | Workspace writes must remain private until new admission. |
| Layer/whiteout facts in portable identity | `FORBIDDEN` | They are runtime/delta mechanics, not the complete portable Version. |
| Observability as storage authority | `FORBIDDEN` | Observability remains a diagnostic reader. |

Temporary legacy decoding may exist only in the separately governed one-way
import path, after legacy writes are fenced. It cannot become a fallback V2
read or write truth.

## What remains at its current owner

| Responsibility | R0 disposition |
|---|---|
| Selected-Version owner | Keep `sandbox-runtime-layerstack`; rewrite its durable model and APIs as LayerStack-0. |
| Application auth, request/revoke ordering, expected-Head capture, orchestration | Keep in `sandbox-runtime` application/operation services. |
| Workspace and writable Candidate custody | Keep in workspace/runtime-effect owners. |
| OverlayFS `lowerdir`/`upperdir`/`workdir`, mounts, namespaces, exec, host paths | Keep runtime-private at existing effect owners. |
| Manager/daemon lifecycle and readiness | Keep at existing lifecycle owners. |
| Observability | Keep read-only and diagnostic. |
| MCTS/rollout/winner policy | Keep in callers/application, outside storage. |

R0 introduces zero new crate, service, process, facade, coordinator, database,
or deployment boundaries. A helper or service cannot be added under the label
“optimization” without proving the exact R0 failure and reopening the joint
ownership/storage decision. No platform-specific copy mechanism may become a
correctness requirement.

## Operation comparison

| Operation or concern | Current e497 evidence | Selected R0 target | Proposed CAS+CDC effect |
|---|---|---|---|
| Selected truth | Ordered manifest/layers | Complete immutable payload closure | Complete manifest plus Chunk closure, only if selected later |
| Fork/Branch reference | No named public fork operation in current inventory | `CreateHeadIfAbsent` for the target Branch Head; zero payload I/O | No additional payload benefit beyond selected zero-payload reference path |
| Checkpoint to accepted content | No named public checkpoint operation in current inventory | `CreateFixedRootIfAbsent` for a typed Checkpoint Root; zero payload I/O | Same fixed-reference semantics; Chunks are not copied |
| Workspace write | Runtime workspace/OverlayFS effects | Private mutable Candidate work | Changed files may be chunked only under proposed family |
| Publish | Current validated layer publication; compatible auto-merge can occur | Complete payload admission, then one OCC Head transition | Multi-object Chunk/manifest admission would need its own recovery proof |
| Rollback to existing | No named public rollback operation in current inventory | Exact `ReplaceHead` for the Branch Head; zero payload I/O | Same Head semantics; no rechunking required |
| Long history | Layer depth creates reconstruction/squash concerns | No parent/depth reconstruction | Version manifests remain complete; shared Chunks must not create ancestry truth |
| Reclamation | Layer leases/objects are current implementation detail | Exact bounded complete-payload retirement with read custody | Version/Chunk graph reachability is a new unselected obligation |
| Performance evidence | Stage 4.6 is historical and `INCOMPARABLE` | No V2 performance claim | Proposed optimization has no matched result |

## Invariants

The following remain mandatory whether or not CAS+CDC is ever selected:

- One accepted Version is one complete immutable portable filesystem value; it requires no parent,
  layer depth, or squash to read.
- Equal complete canonical bytes at one occupied `VersionId` converge on one
  physical payload for that store.
- An occupied `VersionId` requires full canonical-byte comparison; mismatch is a
  collision and fails closed.
- Exact Head create/replace/remove and fixed-Root create/remove read, write,
  and copy zero accepted-reference payload bytes; a Branch is a Head and a
  Checkpoint is a fixed Root.
- One conditional OCC Head transition is the selection linearization point;
  stale changes no Head and triggers no silent merge/rebase.
- Accepted payload is immutable. Agent writes remain in a private Workspace
  and must create or reuse another complete accepted Version before selection.
- MCTS, rollout, authorization, and winner policy remain outside storage.
- Runtime-private OverlayFS, mount, namespace, host-path, process, Workspace,
  and lease facts never enter portable identity.
- Migration has one writable truth and a deletable importer.
- Recovery, readers, staging, retirement, memory, disk, FDs, and worker debt
  remain finite and fail closed when safety cannot be established.

## Selected, proposed, open, and deferred

| Subject | Status | Decision owner or reopening rule |
|---|---|---|
| R0 package/authority shape | `SELECTED R0` | Fixed by Phase 01; later phases cannot move ownership silently. |
| Filesystem-native complete immutable payload closure | `SELECTED R0` | Phase 03 implements and proves this selected family. |
| Roots/Heads, strict OCC, zero-payload references | `SELECTED R0` | Phase 03 proof; Phase 04 application composition. |
| Exact portable fact grammar, codec, digest | `DEFERRED P02` | Must remain complete, bounded, deterministic, portable, and exactly comparable. |
| Exact R0 on-disk spelling, records, fence sequence, limits | `DEFERRED P03` | May vary only inside selected R0. |
| CDC and cross-Version Chunk sharing | `PROPOSED` | Reopen Phase 01; cannot be introduced as a Phase 03 micro-optimization. |
| Complete Workspace manifest as Chunk physical truth | `PROPOSED` | Reopen Phase 01; changes payload, recovery, and retirement family. |
| Backend-agnostic durable and Workspace-adapter contracts | `PROPOSED` | Must select semantic capabilities, owner, dependency/costs, crash behavior, and bounded cleanup. |
| Ordinary-I/O immutable WorkspaceBase materialization | `PROPOSED PROFILE` | Correctness-first cold path; payload I/O is measured separately from reference COW. |
| New service/filesystem/cache/helper boundary | `NOT SELECTED` | Requires exact R0 failure and joint Phase 01 reevaluation. |
| Owner DECs 001/011/017/018 | `OWNER_DEC_OPEN` | This diagram does not close them. |
| Performance evidence and final verdict | `OPEN`; `TARGET_UNSELECTED` | Stage 4.6 remains `INCOMPARABLE`; later matched measurement required. |

## Verification and reopening

Selected R0 must later prove complete immutable payload reads, occupied-ID
full comparison, zero-payload reference operations, one OCC linearization
point, prior-or-complete-new recovery, immutable read custody, bounded
retirement, and one-writable-truth migration through the Phase 02–06 gates.

Reopen Phase 01 before adopting the proposed CAS+CDC family. The reopening must
jointly decide at least:

1. whether complete manifests plus Chunk objects replace the selected
   filesystem-native payload closure as physical truth;
2. where Chunk admission, collision comparison, indexes, recovery, and
   retirement live;
3. which backend-neutral capabilities make a Version readable without changing
   identity, collision, durability, or recovery semantics;
4. how the runtime Workspace adapter and ordinary-I/O materialization profile
   integrate with existing owners, including cache, mount, and reader custody;
5. how all crash prefixes avoid dangling manifests or references;
6. how every resource population and cleanup debt remains bounded; and
7. which source-placeable joint candidate passes all ten product hard rules.

No diagram, naming decision, optimization claim, or Phase 03 local choice may
answer those architecture questions implicitly.

## Related diagrams

- [Storage diagram index](README.md)
- [Workspace Versions and proposed Chunk content-addressed storage](02-workspace-versions-and-chunk-cas.md)
- [Branches, Checkpoints, and rollback](03-branches-checkpoints-and-rollback.md)
- [Proposed backend abstraction and runtime isolation](04-ephcow-runtime-view.md)
- [Publication, OCC, and recovery](05-publication-occ-and-recovery.md)
- [Retention and reclamation](06-retention-and-reclamation.md)
- [Data movement and complexity](07-data-movement-and-complexity.md)
- [CDC boundaries, resynchronization, and reuse](08-cdc-boundaries-resynchronization-and-reuse.md)
- [Selected architecture comparison](../01-before-and-after-architecture.md)

## Evidence

- Current facts: Phase 00 [SPEC](../../phases/00-freeze-rules/SPEC.md) and
  inventories at sealed product source `e4974d1f9aac702b35e052629cb070c897989352`
  — `SOURCE-VERIFIED`.
- R0 ownership/storage selection: root
  [architecture design](../../architecture_design.md) — `SELECTED R0`.
- Version/Branch/EphCoW vocabulary: branding
  [terminology](../../branding/terminology.md) — explanatory vocabulary only.
- CAS+CDC, Chunk manifests, and backend-neutral storage/runtime contracts:
  discussion-derived architecture proposal — `PROPOSED`, not executed or
  selected.
- Scratch spike: **none**. No code or benchmark was needed to explain the
  decision boundary.
