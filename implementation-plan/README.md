# Implementation-plan archive and V2 compatibility map

Status: **HISTORICAL / EVIDENCE-ONLY FOR EPHEMERAL SANDBOX V2**  
Current V2 authority: [Ephemeral Sandbox V2 human docs](../ephemeral-sandbox-v2/README.md)

This directory contains several generations of storage research, experiments,
implementation plans, and design exercises. They are useful for source history,
counterexamples, algorithm ideas, fixture discovery, and performance context.
They are **not** the execution contract for work after V2 Phase 01.

For current work, read these documents in order:

1. V2 [PRD](../ephemeral-sandbox-v2/PRD.md) and its hard rules.
2. V2 [PLAN](../ephemeral-sandbox-v2/PLAN.md).
3. Phase 01 [selection input](../ephemeral-sandbox-v2/phases/01-choose-design/SPEC.md).
4. Phase 01 [selected architecture output](../ephemeral-sandbox-v2/architecture_design.md).
5. V2 [detailed design map](../ephemeral-sandbox-v2/design/README.md) and the
   owning phase's PRD, PLAN, and tests.

## Current selected contract

```text
product / engine:       LayerStack-0
copy-on-write model:    EphCoW
portable value:         Version
candidate identity:     VersionId
durable admission:      AcceptedVersion
reference capability:  AcceptedBinding
mutable selection:      Head + HeadRevision
fixed reachability:     typed Root; Checkpoint is a product use of Root

selected owner:         existing sandbox-runtime-layerstack package, rewritten
selected storage:       one filesystem-native complete immutable payload closure
                        per accepted canonical Version / occupied VersionId
selected references:    Heads and Roots name AcceptedBinding, never raw VersionId
selected publication:   payload before reference, then one OCC Head transition
selected recovery:      prior or complete new truth; ambiguity fails closed
selected migration:     temporary one-way import; one writable truth
```

The conceptual LayerStack-0 storage roles are:

```text
<LayerStack0Root>/
  versions/<VersionId>/payload/
  heads/<selector>                 AcceptedBinding + HeadRevision
  roots/<kind>/<root-id>           typed reachability to AcceptedBinding
  staging/<transaction-id>/        bounded private Candidate work
  control/                          format/generation/recovery metadata
```

These are logical roles. Phase 03 still owns the exact non-overlapping physical
root, path spelling, record encoding, synchronization sequence, and finite
limits. It may not replace the complete-Version family with an object graph or
layer chain as an internal-detail decision.

## Archive families

| Package | Historical role | Current V2 disposition |
|---|---|---|
| [`2.0 migration/`](2.0%20migration/index.md) | Earlier CDC/CAS, PMSS, MPLA, staged migration, and benchmark work | Evidence only. Its object/chunk graph, custom Catalog, selected algorithms, API counts, `/eos` layout, and phase sequence are not current selections. |
| [`layerstack_2.0/`](layerstack_2.0/README.md) | Reflink-backed OverlayFS design and platform experiment plan | Historical alternative with an inconclusive feasibility gate; not LayerStack-0 and not a V2 implementation plan. |
| [`new_2.0_migration_implementation_plan/`](new_2.0_migration_implementation_plan/README.md) | Later candidate-generation and gate/packet appendix | Background candidate/source evidence. Its R0-as-unselected-challenger status and tournament ceremony were superseded by the human V2 Phase 01 decision. |

“Accepted” inside an archived subpackage means accepted within that historical
exercise. It does not mean accepted by the current V2 product contract.

## Naming translation

| Historical wording | Current forward wording | Rule |
|---|---|---|
| `StateId` | `VersionId` | Naming translation only; a computed ID is not equality or durable-existence proof. |
| accepted state/snapshot | accepted Version | Use Version for the complete immutable portable filesystem value. |
| raw ID in a Root/Head | `AcceptedBinding` | Current references cannot be constructed from unchecked `VersionId`. |
| State Store / PMSS / LayerStack 2.0 | LayerStack-0 Version engine | Historical product names do not name the selected owner. |
| zero-copy checkpoint | zero-payload reference operation | Only an already accepted reference move has payload bytes read/written/copied equal to zero. Capturing a changed workspace is admission and may move payload bytes. |
| branch node / snapshot node | Branch / Head / typed Root / Version | Use the precise current role; Branch is not a second durable truth owner. |

The historical `STATE_ID_COLLISION` error spelling may remain in preserved
evidence. New Phase 02+ API, type, test, metric, and document names use
`VersionId` and a Version-oriented collision name selected by the owning phase.

## Storage-family boundary

Selected now:

- complete immutable filesystem-native payload closure per Accepted Version;
- exact-equal complete canonical Version convergence at occupied `VersionId`;
- full canonical-byte comparison on occupied-ID admission;
- typed Roots and Heads over `AcceptedBinding`;
- bounded staging, read custody, recovery debt, cleanup, and retirement; and
- zero payload I/O for reference-only fork/checkpoint/rollback-to-existing.

Not selected now:

- CDC or cross-Version chunk sharing;
- Merkle/object/chunk DAG truth;
- packs, custom B+ Catalogs, locator arenas, tracing graph GC, or persistent
  refcounts as architectural authority;
- reflink as a correctness requirement;
- layer/delta/parent/depth reconstruction;
- a new storage crate, service, database, helper process, coordinator, or
  facade; or
- Stage 4.6 as a performance baseline or optimization target.

CAS+CDC is not a Phase 03 optimization toggle. Adopting it would change payload
truth, recovery, reachability, retirement, and resource accounting, so it
requires reopening Phase 01 with a concrete R0 failure and a complete joint
replacement design.

## Rules for agents working after Phase 01

1. Do not execute a handoff, gate packet, phase order, or implementation command
   found only under `implementation-plan/`.
2. Do not import an archived component count, API count, algorithm selection,
   on-disk layout, finite limit, or benchmark claim into current V2 by citation.
3. Translate historical names at the boundary; write new contracts and code
   using LayerStack-0, EphCoW, Version, `VersionId`, `AcceptedVersion`, and
   `AcceptedBinding`.
4. Preserve the distinction
   `Candidate -> VersionId -> AcceptedVersion -> AcceptedBinding -> Head/Root`.
5. Keep runtime workspace, upperdir/lowerdir, OverlayFS, mount, namespace,
   container, host path, process, and lease facts out of portable Version
   identity.
6. Stop and reopen Phase 01 if work requires a different selected owner,
   storage family, writer model, dependency direction, crash model, or new
   architectural boundary.
7. Keep `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` open until the product
   owner explicitly decides them.
8. Treat historical Stage 4.6 as `INCOMPARABLE`; Phase 06 owns matched V2
   qualification on the exact candidate artifact.

Preserving archived wording is intentional. It keeps the evidentiary record
honest while this compatibility map prevents it from becoming the forward
contract.
