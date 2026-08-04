# LayerStack-0 storage diagrams

Date: **2026-08-04**

Status: **mixed — selected R0 contract plus explicitly proposed storage-family extension**

This folder explains the LayerStack-0 storage model as a short, ordered set of
ASCII views. It starts from the selected R0 architecture and then makes the
discussed CAS+CDC direction visible without presenting it as an accepted
implementation.

The governing sources are the product [PRD](../../PRD.md), the Phase 01
[selection input](../../phases/01-choose-design/SPEC.md), and the selected
[architecture](../../architecture_design.md). The general architecture
[diagram index](../README.md) remains the companion index for ownership,
rollout, and migration views. If any diagram here conflicts with a governing
source, the governing source wins and this folder must be corrected.

**Phase 02/03 implementation path:** read `01`, `03`, and `05`–`07`, using only
panels labeled **SELECTED R0** or **DEFERRED P02/P03**. Files `02`, `04`, and
`08`, plus every **PROPOSED/OPEN** panel, are comparison material—not
implementation input. A Phase 02/03 agent must stop and reopen Phase 01 before
adopting any of them.

## Decision boundary

The selected architecture and the discussed storage extension must remain
visibly separate.

```text
SELECTED R0 -- LOCKED_PHASE_01

  complete immutable payload closure per Accepted Version / occupied VersionId
  equal complete canonical bytes -> one physical payload closure
  Root/Head reference operations -> zero payload bytes read/written/copied
  one strict OCC Head transition; no silent merge or rebase
  private runtime Workspace writes; accepted payload never edited in place
  sandbox-runtime-layerstack remains the selected-Version owner


PROPOSED CAS+CDC EXTENSION -- NOT SELECTED

  complete Workspace manifest
        |
        +--> files represented by ordered CDC Chunk references
        |
        +--> cross-Version Chunk content-addressed storage sharing
        |
        '--> backend-agnostic durable admission/recovery contract


PROPOSED BACKEND/RUNTIME ABSTRACTION

  AcceptedBinding -> Workspace adapter -> isolated mutable Workspace

  correctness-first profile:
    ordinary bounded byte I/O -> immutable WorkspaceBase directory

  current Linux adapter:
    WorkspaceBase lowerdir + private upperdir/workdir/namespace
```

CAS+CDC cross-Version sharing, a manifest/Chunk physical truth model, and a
backend-agnostic durable/runtime adapter contract were not selected by the
current Phase 01 document. They change the selected storage family and add
multi-object recovery, cache/materialization, and graph-retirement obligations.
They require **Phase 01 reopening** before they may be marked selected or
implemented as LayerStack-0 V2.

The candidate must not depend on a custom filesystem, storage-specific clone
operation, or one durable substrate. The existing OverlayFS path is one runtime
adapter profile; it is never portable identity or a durable storage dependency.

Historical Stage 4.6 evidence is `INCOMPARABLE`. This folder contains no
benchmark winner, latency claim, or V2 performance guarantee.

## Reading order

There are **nine files total**: this index and eight focused chapters.

| # | Diagram | Question answered |
|---:|---|---|
| 0 | This `README.md` | What is selected, proposed, open, and where should a reader start? |
| 1 | [Before and after](01-before-and-after.md) | What measured legacy storage truth is replaced by selected R0, and where does proposed CAS+CDC extend R0? |
| 2 | [Proposal only: Workspace Versions and Chunk content-addressed storage](02-workspace-versions-and-chunk-cas.md) | If Phase 01 were reopened, how could a full logical workspace be described while file bytes share CDC Chunks? **Skip for current implementation.** |
| 3 | [Branches, Checkpoints, and rollback](03-branches-checkpoints-and-rollback.md) | How do mutable selection, fixed retention, fork, and rollback relate to accepted Versions? |
| 4 | [Proposal only: backend abstraction and runtime isolation](04-ephcow-runtime-view.md) | If Phase 01 were reopened for CAS+CDC, how could backend-neutral Version reads become isolated Workspaces? **Skip for current implementation.** |
| 5 | [Publication, OCC, and recovery](05-publication-occ-and-recovery.md) | How do Workspace changes become a complete accepted Version before one conditional Head transition? |
| 6 | [Retention and reclamation](06-retention-and-reclamation.md) | Which Roots, Heads, Checkpoints, readers, Workspaces, and transactions protect Versions and proposed Chunks? |
| 7 | [Data movement and complexity](07-data-movement-and-complexity.md) | Which paths are guaranteed to move zero payload bytes, which paths process content, and what must later benchmarks measure? |
| 8 | [CDC boundaries, resynchronization, and reuse](08-cdc-boundaries-resynchronization-and-reuse.md) | How are content-derived cut points selected, how can edits resynchronize, and when must capture fall back to a complete scan? |

The intended narrative is:

```text
legacy layer-chain problem
          |
          v
complete immutable Workspace Version
          |
          v
Branch and Checkpoint references
          |
          v
existing runtime-owner handoff
          |
          +--> correctness-first ordinary-I/O materialization
          `--> current Linux lowerdir + private upperdir profile
          |
          v
admission -> durable Version -> strict OCC Head transition
          |
          v
recovery, reachability, and retirement
          |
          v
CDC boundaries, payload-I/O, and complexity obligations
```

## Architecture at a glance

```text
                    APPLICATION / PRODUCT PLANE

  Branch agent-a                         Checkpoint baseline
  "where this work is selected"          "which Version must remain"
          |                                       |
          +-------------------+-------------------+
                              |
                              v
                  accepted Workspace Version [I]
                  complete immutable portable value
                              |
               +--------------+--------------+
               |                             |
               v                             v
     SELECTED R0 payload closure       PROPOSED representation
     filesystem-native, complete       complete Workspace manifest
     no parent/layer needed            + ordered CDC Chunk references
                                             |
                                             v
                                  shared Chunk content-addressed
                                  storage across different Versions
                                             |
                                             v
                                  proposed backend-neutral read/materialize contract
                                             |
                    +------------------------+
                    |
                    v
             immutable WorkspaceBase [R]
                    |
                    +--> current Linux: lowerdir [R]
                                      + private upperdir/workdir [R]
                                      + isolated namespace [R]
```

The complete Workspace is the user-visible logical target. A proposed Chunk is
only a private physical byte-storage object for file contents; it is not a
Workspace, Version, Branch, Checkpoint, or legacy layer.

## Storage structure under `/eos`

The paths below connect the architecture roles to the sandbox filesystem. They
are a **conceptual placement map**, not a Phase 03 disk-layout decision. The
e497 base currently mounts the per-sandbox LayerStack volume at
`/eos/layer-stack` and workspace scratch at `/eos/workspace`; the Phase 00
[surface inventory](../../phases/00-freeze-rules/inventory-surfaces.md) records
those as current facts. Phase 01 selected the roles and owner but deliberately
left exact V2 directory names, record spellings, and control-file encodings to
Phase 03.

Branding the engine **LayerStack-0** does not by itself rename the existing
`/eos/layer-stack` mount. Reusing that mount is the lowest-change placement
hypothesis, but Phase 03 must choose a V2 namespace under or beside it that
cannot alias legacy e497 paths while the two readers coexist. A path rename
such as `/eos/layerstack-0` needs an explicit configuration/migration decision,
not a diagram assumption.

### Selected R0 role map

```text
/eos/
+-- layer-stack/                         [CURRENT mount; reuse is a hypothesis]
|   |
|   +-- manifest.json                   [LEGACY e497 -- no V2 reuse]
|   +-- workspace.json                  [LEGACY e497 -- no V2 reuse]
|   +-- layers/                         [LEGACY e497 -- no V2 reuse]
|   +-- staging/                        [LEGACY e497 -- no V2 reuse]
|   +-- .layer-metadata/                [LEGACY e497 -- no V2 reuse]
|   +-- base/                           [LEGACY e497 -- no V2 reuse]
|   |
|   `-- <v2-namespace>/                 [DEFERRED P03; MUST NOT alias legacy]
|       +-- versions/                   complete Accepted Versions
|       |   `-- <VersionId>/
|       |       `-- payload/            one immutable payload closure
|       +-- heads/                      mutable selected references
|       |   `-- <selector>              AcceptedBinding + HeadRevision
|       +-- roots/                      fixed typed reachability
|       |   +-- checkpoint/<root-id>    product Checkpoint -> AcceptedBinding
|       |   `-- <other-kind>/<root-id>  explicitly typed product root only
|       +-- staging/                    private, bounded, unaccepted work
|       |   `-- <transaction-id>/       never selectable by Head or Root
|       `-- control/                    format/generation/recovery roles;
|                                       exact encoding deferred to Phase 03
|
+-- workspace/                           [RUNTIME-PRIVATE effect owner]
|   +-- manager metadata                 lifecycle/recovery, not Version truth
|   +-- <WorkspaceId>/
|   |   +-- upper/                       this agent's private writes
|   |   +-- work/                        OverlayFS work area
|   |   `-- merged/                      full sandbox-visible workspace
|   `-- .export/                         transient export scratch
|
+-- runtime/                             daemon sockets, PIDs, diagnostics
+-- bin/                                 runtime binaries
+-- config/                              runtime configuration
`-- storage/                             bounded runtime side artifacts;
                                         not selected-Version authority
```

Only the role names `versions`, `heads`, `roots`, `staging`, and `control` are
the selected architecture's conceptual vocabulary. Even those exact path
spellings remain `DEFERRED P03`. The entries below `control/` explain five
responsibilities; they are not five new services, coordinators, registries, or
truth owners. Phase 03 may encode several roles in one versioned record or use
different filenames while preserving the same failure and ownership model.

The tree separates two kinds of storage:

```text
/eos/layer-stack/<v2-namespace>   durable Accepted Versions and references
/eos/workspace     live mutable upperdir/workdir/merged effects

workspace write -X-> versions/<VersionId>/payload in-place mutation
workspace write ----> private upperdir ----> new Candidate admission
```

An accepted Version is a full logical workspace folder. In selected R0 its
physical truth is one complete filesystem-Version payload closure. A Branch is
the product context whose durable selected binding is a small Head; a
Checkpoint is a fixed typed Root. Neither contains payload bytes.

### Proposed CAS+CDC role map

If Phase 01 is reopened and selects the manifest-plus-Chunk family, the store
portion could instead have this conceptual shape:

```text
/eos/
+-- layer-stack/                         [PROPOSED storage-family replacement]
|   +-- versions/
|   |   `-- <VersionId>/
|   |       `-- workspace.manifest       complete portable workspace tree
|   |
|   +-- chunks/
|   |   `-- <ChunkId>                    immutable file-content bytes shared
|   |                                    across different complete Versions
|   |
|   +-- heads/
|   |   `-- <selector>                   Branch binding + HeadRevision
|   +-- roots/
|   |   `-- checkpoint/<root-id>         fixed Checkpoint binding
|   +-- staging/
|   |   `-- <transaction-id>/            private manifest/Chunk admission
|   `-- control/                         format, generation, coordination,
|                                        recovery, and retirement roles
|
`-- workspace/
    +-- materialized-bases/<VersionId>/     [PROPOSED] derived cache/profile
    `-- <WorkspaceId>/
        +-- lower -> WorkspaceBase        runtime binding; never portable ID
        +-- upper/                        private writes
        +-- work/                         OverlayFS work area
        `-- merged/                       full sandbox-visible workspace
```

This proposal still stores a **complete workspace Version**, not a directory
delta:

```text
Version = complete workspace.manifest
        + transitive closure of every Chunk named by that manifest

Version -X-> parent Version required for reconstruction
Branch  -X-> direct Chunk reference
Checkpoint -X-> direct Chunk reference
```

The proposed `materialized-bases/` location is illustrative, runtime-private,
and not accepted truth. It is the correctness-first ordinary-byte-I/O profile,
not a universal backend layout. Other runtime profiles may realize the same
Workspace adapter contract, but all must preserve the same Version semantics
and conformance tests. Cache ownership, custody, crash cleanup, space, and
limits are part of the Phase 01 reopening question described in the
[proposed backend/runtime chapter](04-ephcow-runtime-view.md).

For the measured legacy `/eos` tree and the transition from layers to complete
Versions, see [Before and after](01-before-and-after.md). For the distinction
between a full workspace and its proposed physical Chunks, see
[Workspace Versions and Chunk content-addressed storage](02-workspace-versions-and-chunk-cas.md).

## Decision-status matrix

| Subject | Status | Meaning |
|---|---|---|
| Complete immutable Version per occupied `VersionId` | `SELECTED R0` | The accepted payload is complete and needs no parent, depth, layer chain, or squash to read. |
| Public product term **Version** | `ACCEPTED PRODUCT CONTRACT` | An admitted complete immutable portable filesystem value; see ADR-002. |
| One physical payload for equal complete canonical bytes | `SELECTED R0` | Equality is at the complete-Version boundary, not selected cross-Version Chunk deduplication. |
| Full-byte comparison for occupied `VersionId` | `SELECTED R0` | A digest match is not proof; mismatch fails closed. |
| Five Head/fixed-Root reference operations | `SELECTED R0` | Head create/exact replace/exact remove and fixed-Root create/exact remove use one authority; for an already accepted binding, payload bytes read, written, and copied are all zero. |
| Branch | `PRODUCT VIEW` | Application/runtime concept for isolated work from an accepted Version; durable selection uses the selected Head contract. |
| Checkpoint to an existing Version | `SELECTED COMPOSITION` | A fixed typed Root create operation with zero payload I/O. Capturing new Workspace contents first requires Candidate admission. |
| Private Workspace `upperdir` and immutable base/lower view | `SELECTED OWNERSHIP/INVARIANT` | Runtime effects remain outside portable identity; exact materialization is a runtime/Phase 03 detail within R0. |
| Content-defined chunking (CDC) | `PROPOSED` | Possible changed-file storage optimization; not part of selected R0. |
| Cross-Version Chunk content-addressed storage sharing | `PROPOSED` | Different Versions may reuse equal Chunks only if Phase 01 selects this different physical storage family. |
| Complete Workspace manifest over ordered Chunk references | `PROPOSED` | A possible complete logical representation; not the selected R0 payload model. |
| Backend-agnostic durable capability contract | `PROPOSED CANDIDATE CONSTRAINT` | CAS+CDC correctness must survive changing qualified durable substrates. |
| Runtime Workspace adapter contract | `PROPOSED CANDIDATE CONSTRAINT` | Runtime activation is separate from reference operations and portable identity. |
| Correctness-first ordinary-I/O materialization profile | `PROPOSED` | Cold materialization may process the complete payload; it is not a zero-copy reference operation. |
| Exact canonical codec and digest | `DEFERRED P02` | Must satisfy the selected identity boundary; not chosen by diagrams. |
| Exact R0 root/namespace, disk spelling, records, locks, and durability sequence | `DEFERRED P03` | Phase 03 must choose a migration-safe non-overlapping namespace inside the selected filesystem-native complete-payload family. |
| Exact CDC algorithm/parameters | `NOT AUTHORIZED YET` | Requires selection of the CAS+CDC family first; a local parameter choice cannot silently introduce it. |
| V2 performance evidence and final verdict | `OPEN`; `TARGET_UNSELECTED` | Stage 4.6 is `INCOMPARABLE`; future matched tests own evidence. |

## Shared legend

Every file in this folder should use these labels and symbols.

```text
[I]  immutable durable object
[M]  mutable durable reference
[R]  runtime-private object or effect
[T]  private publication transaction/candidate
[O]  unresolved architecture mechanism

---->  reference, selection, or metadata/control flow
====>  payload-byte flow
....>  diagnostic, recovery, or temporary flow
-X-->  forbidden transition or dependency

[SOURCE-VERIFIED e497]  measured current-source fact at the sealed e497 base
[SELECTED R0]           binding Phase 01 architecture decision
[PROPOSED]              discussed candidate mechanism; not selected
[OPEN]                  unresolved item that can change architecture
[DEFERRED P02/P03]       bounded implementation choice inside selected R0
```

Do not use bare `CAS` in prose because it can mean content-addressed storage or
compare-and-swap. Write **Chunk content-addressed storage** for the proposed
content backend and **conditional OCC Head transition** for selected reference
publication.

## Shared example identifiers

Use the same identifiers across all eight chapters so the diagrams form one
continuous example.

```text
Accepted Versions:    V1, V2, V3
Normative identity:   VersionId (shown as V1/V2/V3 for readability)
Proposed Chunks:      C01, C02, C03, ...
Branch:               agent-a
Checkpoint:           baseline
Workspace:            W17
Publication:          T42
Head revision:        r12, r13, ...
```

Vocabulary relationship:

```text
Version     complete portable filesystem value before/after admission
Version     admitted complete immutable value, identified by VersionId and named through AcceptedBinding
VersionId   content-derived typed identifier; computable before admission
AcceptedBinding  LayerStack-0-issued/revalidated capability for an Accepted Version
Branch      product/runtime line of isolated work from an accepted Version
Head        mutable durable selected reference with HeadRevision
Checkpoint  product operation; existing-Version case becomes a typed Root
Workspace   mutable runtime view used to prepare Candidate work
```

## Required explanation in every chapter

Each detailed file should state:

1. the question it answers;
2. its authority and design status;
3. the primary ASCII diagram and a plain-English walkthrough;
4. selected invariants, proposed mechanisms, and open/deferred details;
5. relevant failure and cleanup behavior;
6. later proof ownership; and
7. any condition that requires Phase 01 reopening.

The diagrams explain architecture. They do not select an exact codec, hash,
Chunk size, CDC window, disk filename, lock, filesystem fence sequence, cache
policy, benchmark result, or owner decision.

## Update and reopening rule

An implementation choice inside selected R0 should first update its owning
Phase 02/03 design or contract and then update these diagrams. The following
cannot be introduced through a diagram edit:

- Chunk/manifest physical truth or cross-Version Chunk sharing;
- a dependency on a custom filesystem or storage-specific clone feature;
- a new mount/cache/helper process without a concrete necessity case;
- a second selected-Version writer or OCC point;
- a different owner, package, service, database, or coordinator;
- runtime-private facts in portable identity;
- payload-bearing Branch/Checkpoint reference paths;
- layer/parent/depth truth; or
- dual writable legacy and V2 storage.

Those changes require the Phase 01 reopening process in the selected
[architecture](../../architecture_design.md#15-architecture-verification-and-reopening).
