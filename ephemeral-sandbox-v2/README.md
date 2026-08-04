# Ephemeral Sandbox V2 — human docs

**Start here.** This package is the readable product and implementation guide
for **LayerStack-0**, the Ephemeral Sandbox V2 Version engine. LayerStack-0
replaces legacy LayerStack history reconstruction with complete immutable
Versions and uses **EphCoW** for reference-level copy-on-write branching.

It is **not** the gate/ownership ceremony package. Deep design, evidence, and
old process notes live elsewhere as an appendix.

## Read in this order

1. **[PRD.md](PRD.md)** — what we are building and the hard rules  
2. **[PLAN.md](PLAN.md)** — phase order, folders, and where code may change  
3. **[architecture_design.md](architecture_design.md)** — the selected Phase 01
   ownership/storage architecture consumed by later phases  
4. **[Phase 01.5 SPEC](phases/01-5-contract-closure/SPEC.md)** — the passed
   contract-closure gate authorizing formal Phase 02 entry; its
   [execution prompt](phases/01-5-contract-closure/PROMPT.md) remains the
   historical operational trace  
5. **[design/README.md](design/README.md)** — scoped R0 implementation
   contracts, delegated choices, evidence ownership, and reopening rules  
6. **[benchmark/README.md](benchmark/README.md)** — historical Stage 04.6
   evidence quarantine, open V2 optimization-target register, and qualification
   navigation  
7. **[diagrams/README.md](diagrams/README.md)** — ASCII architecture and
   operation views for storage, branching, publication, rollout, lifetime, and
   migration  
8. **[branding/terminology.md](branding/terminology.md)** — canonical
   LayerStack-0, EphCoW, Version, and `VersionId` vocabulary  
9. Current phase under **[phases/](phases/)** — that folder’s `PRD.md` → `PLAN.md` → `test-perf.md`

## Canonical names

| Name | Meaning |
|---|---|
| **LayerStack-0** | The V2 sandbox Version engine and selected-Version owner. |
| **EphCoW** | Reference-level CoW over accepted immutable Versions plus isolated runtime workspaces. |
| **Version** | One accepted complete immutable portable filesystem value. |
| `VersionId` | Typed content-derived identity of the complete canonical value; not proof of equality or durable existence. |
| **AcceptedVersion** / **AcceptedBinding** | LayerStack-0-issued admission evidence used by Heads and Roots. |
| **Branch** / **Head** | Product exploration context and its mutable OCC-selected reference. |
| **Checkpoint** / **Root** | Fixed durable reachability to an accepted Version. |

`StateId` is the superseded pre-implementation name for `VersionId`; see
[ADR-002](design/decisions/ADR-002-version-id-naming.md). Historical Phase 00
and Phase 01 evidence may retain the old spelling and must be read through that
terminology mapping.

## Layout

```text
ephemeral-sandbox-v2/
  README.md                 ← you are here
  PRD.md                    ← product brief
  PLAN.md                   ← phase index
  architecture_design.md    ← selected whole-program architecture
  benchmark/                ← historical evidence and open V2 target contract
    baseline.md             ← Stage 04.6 evidence; INCOMPARABLE to V2
    target.md               ← QUAL-001 target register; values remain OPEN
  design/                   ← detailed R0 implementation contracts
    README.md               ← authority, status, and document map
    01-...md through 10-...md
    decisions/              ← accepted ADRs and open decision register
  diagrams/                 ← detailed ASCII architecture and workflow views
    storage/                ← LayerStack-0 storage structure and algorithms
  phases/
    NN-name/
      PRD.md                ← what this phase owes
      PLAN.md               ← how we do it
      test-perf.md          ← how we know it is done
    01-5-contract-closure/
      SPEC.md               ← documentary interphase entry gate
```

## Workspaces (code)

| Role | Path |
|------|------|
| Clean implementation base | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0` |
| Expected branch | `codex/new-2.0-storage-core` |
| Recorded base commit | `e4974d1f9aac702b35e052629cb070c897989352` |
| Day-to-day product repo | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox` (do not mix casually) |

Do not implement V2 product code until the relevant phase says so. Prefer the
clean worktree above.

## Conceptual `/eos` storage placement

The selected roles fit under the existing sandbox storage mounts as follows.
This is an ownership and non-overlap map, not Phase 03's final directory-name
decision:

```text
/eos/
  layer-stack/                         durable LayerStack ownership home
    manifest.json                     legacy e497 only
    workspace.json                    legacy e497 only
    layers/                            legacy e497 only
    staging/                           legacy e497 only
    .layer-metadata/                   legacy e497 only
    base/                              legacy e497 only
    <v2-namespace>/                    exact name selected by Phase 03
      versions/<VersionId>/payload/    complete immutable Version closure
      heads/                           mutable OCC-selected references
      roots/                           typed durable reachability
      staging/                         bounded private, unaccepted work
      control/                         format/generation/recovery metadata

  workspace/                           runtime-owned writable workspaces,
                                       upperdirs, workdirs, and mount effects

  storage/
    file_auditability/                 separate provenance side channel;
                                       DEC-001 remains open
    workspace_recovery/                runtime recovery side channel;
                                       not Version identity or selected truth
```

Phase 03 must select the exact LayerStack-0 root and V2 namespace so no V2
record aliases any legacy e497 name. Phase 05 consumes the LayerStack-0 API and
reported layout contract; it never manufactures these paths directly. See the
[storage diagram guide](diagrams/storage/README.md) and selected
[storage contract](design/03-state-store.md).

## Appendix (optional detail)

| Topic | Location |
|-------|----------|
| Archive authority and naming/storage translation | [`../implementation-plan/README.md`](../implementation-plan/README.md) |
| Older deep design proposals | `../implementation-plan/new_2.0_migration_implementation_plan/design/` |
| Older algorithm / method census | `../implementation-plan/new_2.0_migration_implementation_plan/algorithms/` |
| Historical Stage 4.6 | [V2 evidence summary](benchmark/baseline.md); raw historical tree `../implementation-plan/2.0 migration/` |
| Ceremony / gates / packets | `../implementation-plan/new_2.0_migration_implementation_plan/execution/` |

Everything under `implementation-plan/` is historical or evidence-only for
current V2. Do not execute an appendix handoff or import its `StateId`, raw-ID
reference, CDC/chunk/Merkle storage, exact `/eos` layout, component count,
algorithm selection, or phase status into Phase 02+. The archive
[compatibility map](../implementation-plan/README.md) records the translation.

## Status

| Item | Status |
|------|--------|
| Human docs package | Created |
| Phase 00 rules/evidence | Complete after pass 2 |
| Phase 01 | Complete; input contract remains in [Phase 01 SPEC](phases/01-choose-design/SPEC.md) |
| Phase 01.5 | Complete; `PASS` with finding trace `019fcd32-b832-7750-9eb5-5f544e39c533` — see [Phase 01.5 SPEC](phases/01-5-contract-closure/SPEC.md) |
| Phase 02 | Authorized by the Phase 01.5 gate; not started |
| Architecture winner | R0 joint ownership/storage direction; see [architecture_design.md](architecture_design.md) |
| Canonical identity name | `VersionId`; `StateId` is a historical alias only |
| Detailed design package | Created; see [design/README.md](design/README.md) |
| Algorithm contracts | Fixed at the semantic/state-machine level; exact Phase 02 identity and Phase 03 filesystem choices remain deferred |
| Performance readiness | `TARGET_UNSELECTED`; no owner-approved quantitative optimization target or qualified V2 benchmark result exists |
| Benchmark package | Created; Stage 04.6 remains `INCOMPARABLE`, and all V2 target values remain `OPEN` in [target.md](benchmark/target.md) |
| Live cutover | Not authorized |

---

Parent product: [PRD.md](PRD.md) · Index: [PLAN.md](PLAN.md)
