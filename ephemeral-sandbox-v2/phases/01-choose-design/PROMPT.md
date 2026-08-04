# Agent prompt — Phase 01: select and publish the V2 architecture

> **Historical prompt note (2026-08-04):** this execution input uses the old
> `StateId` spelling. Current V2 output uses `VersionId` per
> [ADR-002](../../design/decisions/ADR-002-version-id-naming.md); do not rerun
> Phase 01 merely for that rename.

Copy everything below the line into a new agent session.

---

## Goal

Execute **Phase 01 — Choose design** for Ephemeral Sandbox State Storage V2.

The Phase 01 [`SPEC.md`](SPEC.md) is an **input**, not the result. Read it as the
selection contract: it defines what must be selected, what makes a candidate
good enough, the evidence threshold, and the required contents of the output.

Produce the whole-program architecture output at:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/architecture_design.md
```

Make one honest, implementable **joint** decision about:

1. where selected-state ownership and related responsibilities live; and
2. what storage approach that ownership shape implements.

The architecture output must begin with exactly one result:

```text
WINNER: <candidate id and short name>
```

or:

```text
NO_WINNER: <specific blocking reason>
```

Do not choose architecture separately from storage. Do not force a winner so
Phase 02 can start. When nothing satisfies the specification without later
architecture rediscovery, `NO_WINNER` is the correct result.

This is Phase 01 design work. **Do not implement V2 product code.**

## Document lifecycle

| Document | Role |
|---|---|
| `phases/01-choose-design/SPEC.md` | Normative Phase 01 input: targets, candidate gates, evidence rules, output contract |
| `phases/01-choose-design/PRD.md` | Short phase product intent |
| `phases/01-choose-design/PLAN.md` | Execution checklist/status |
| `phases/01-choose-design/test-perf.md` | S1–S5 exit gate |
| Root `architecture_design.md` | Selected Phase 01 output and architecture contract consumed by Phases 02–08 |

Do not rewrite `SPEC.md` to match a preferred result. If the selection contract
is impossible or contradictory, stop and report the exact conflict.

## Authority and interpretation

Use sources in descending authority:

1. V2 product `PRD.md`, especially hard rules 1–10.
2. Completed Phase 00 `SPEC.md` and measured inventories.
3. Phase 01 `SPEC.md`, then its `PRD.md`, `PLAN.md`, and `test-perf.md`.
4. The sealed e497 product source tree for implementability evidence.
5. Phase 02 and Phase 03 documents for handoff requirements.
6. The older implementation-plan appendix as background/counterexample evidence
   only.

If sources conflict, follow the higher-authority source and record the conflict
in `architecture_design.md`.

In particular:

- Do not recreate the appendix's exhaustive tournament, gate, epoch, or
  ownership ceremony.
- An appendix topology, algorithm family, package count, open DEC, or unrun
  selection is not accepted architecture.
- Historical Stage 4.6 evidence is `INCOMPARABLE`; it cannot select or reject a
  Phase 01 candidate.
- Current e497 behavior is evidence, not V2 semantics.
- R0 is the required first candidate and default preference, not a preselected
  winner.
- `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` remain open unless the product
  owner explicitly decides them in the session.

## Authorized work

| Allowed | Forbidden |
|---|---|
| Read and search the sealed product worktree | Edit, switch, commit, push, reset, clean, or otherwise change the product worktree |
| Create/update root `architecture_design.md` | Implement identity, state store, product wiring, importer, or cutover code |
| Add a small Phase 01 evidence note if genuinely useful | Change Phase 01 `SPEC.md` merely to fit a candidate |
| Run read-only `rg`, `cargo metadata`, and focused existing tests | Full performance bake-off or V2 performance guarantee |
| Use a disposable scratch spike outside product source for one unresolved architecture question | Modify product source for a spike without separate authorization |
| Update Phase 01 `PLAN.md` after the output actually passes S1–S5 | Change root product contracts or accept owner decisions on the owner's behalf |

Preserve unrelated dirty/untracked documentation files. Never run `git clean`,
destructive reset, or broad checkout commands.

## Paths and evidence seal

```text
Human V2 package
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2

Phase 01 input folder
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/01-choose-design

Required architecture output
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/architecture_design.md

Product evidence tree — READ ONLY
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
  expected branch: codex/new-2.0-storage-core
  recorded HEAD:   e4974d1f9aac702b35e052629cb070c897989352

Older appendix — READ ONLY, non-normative
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/new_2.0_migration_implementation_plan
```

Before any product-tree command, read the product worktree's `AGENTS.md` and
`CLAUDE.md`. Then run:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git status --short --branch
```

Record path, branch, HEAD, dirty state, and drift in `architecture_design.md`.
Do not change the tree to match. If it is missing, dirty, on the wrong branch,
or not at the recorded commit, stop with:

```text
NO_WINNER: BASE_DRIFT <exact drift>
```

## Required reading — full, in order

### Program contract

```text
.../ephemeral-sandbox-v2/README.md
.../ephemeral-sandbox-v2/PRD.md
.../ephemeral-sandbox-v2/PLAN.md
```

### Phase 00 evidence

```text
.../phases/00-freeze-rules/SPEC.md
.../phases/00-freeze-rules/inventory-surfaces.md
.../phases/00-freeze-rules/inventory-packages.md
.../phases/00-freeze-rules/fixture-catalog.md
```

### Phase 01 input and gate

```text
.../phases/01-choose-design/SPEC.md
.../phases/01-choose-design/PRD.md
.../phases/01-choose-design/PLAN.md
.../phases/01-choose-design/test-perf.md
```

Read `SPEC.md` before evaluating a candidate. It is the complete target,
candidate-quality, evidence, and architecture-output contract.

### Downstream consumers

```text
.../phases/02-state-identity/PRD.md
.../phases/02-state-identity/PLAN.md
.../phases/02-state-identity/test-perf.md
.../phases/03-state-store/PRD.md
.../phases/03-state-store/PLAN.md
.../phases/03-state-store/test-perf.md
```

### Focused appendix, after human docs

```text
.../design/architecture-selection.md
.../design/architecture.md
.../design/source-layout.md
.../design/storage-model.md
.../design/state-store.md
.../algorithms/registry.md
.../algorithms/selection-protocol.md
.../decisions/README.md
```

Use appendix material only to identify candidate families, counterexamples, and
required concerns. Do not claim its unrun selection ran or make its package and
algorithm proposals normative.

## Selection target

Every serious candidate must jointly fix:

- selected-state truth owner;
- application auth/order/OCC-call orchestration owner;
- workspace/mount/namespace/exec/lifecycle/observability responsibilities;
- complete immutable payload and accepted-`StateId` model;
- roots/heads and reference-only zero-payload-I/O behavior;
- candidate staging, occupied-ID full-byte comparison, publication, and one OCC
  linearization point;
- crash recovery, reads, retirement, last-root behavior, and cleanup;
- portable identity boundary and forbidden runtime facts;
- one selected-state writer and temporary/deletable migration;
- source/package `KEEP`/`REWRITE`/`DELETE`/`MOVE`/`ADD` disposition;
- dependency direction and every new boundary's necessity; and
- finite resources plus actionable Phase 02/03 contracts.

The architecture must support all product hard rules 1–10. Any failing rule or
architecture-changing open gap prevents a winner.

## Mandatory R0 candidate

Evaluate R0 first as a joint candidate:

```text
ownership:
  existing sandbox-runtime-layerstack becomes the selected-state store owner
  existing app owners keep auth, ordering, and orchestration
  existing workspace/overlay/namespace/exec owners keep runtime effects

storage:
  one complete immutable payload closure per accepted StateId
  roots/heads name accepted states
  exact occupied-ID comparison
  one OCC head transition
  staged recoverable durable publication
  no layer-chain truth
  no payload I/O on reference-only moves
```

Prove it internally coherent and source-placeable. Do not preserve current
LayerStack semantics merely because the package remains.

## Alternative discipline

Admit a serious alternative only when it fixes a named R0 failure, provides a
credible smaller source-placeable fusion, is required by a concrete
privilege/process/recovery/resource invariant, or materially simplifies the
joint storage approach without contaminating portable identity.

For every new crate, service, process, facade, helper, registry, database, or
coordinator, show:

1. exact R0 failure fixed;
2. why an existing owner/direct call cannot fix it;
3. dependency, protocol, crash, retry, resource, deployment, cleanup, and
   operating costs; and
4. necessity evidence.

Do not invent straw candidates. If no alternative is serious, record the
credible shapes considered and why they were not admitted.

## Evidence labels

```text
SOURCE-VERIFIED  direct sealed-tree evidence
SPIKE-VERIFIED   bounded disposable demonstration or existing test
INFERRED         coherent implementability with a named later proof owner
OPEN             missing evidence or decision
```

An `OPEN` blocks selection when it could change ownership, dependency direction,
storage family, writer/OCC count, crash behavior, migration truth, resource
feasibility, or hard-rule compliance. An owner DEC may remain open only when
all currently stated outcomes fit one stable architecture seam.

## Required architecture output

Follow Phase 01 `SPEC.md` section 14 in full. At minimum, root
`architecture_design.md` must contain:

1. document status, authority, environment seal, one result, and Phase 02
   disposition;
2. decision provenance, admitted candidates, comparison, and rejected versus
   non-admitted options;
3. hard-rule 1–10 traceability and quality-attribute assumptions;
4. system context, exact authorities, component/dependency/trust boundaries,
   and necessity of additions;
5. source/package disposition and legacy deletion/hard-fail map;
6. portable domain/identity concepts and forbidden runtime-private facts;
7. complete-state payload, staging, roots/heads, publication/OCC, recovery,
   reads, retirement, and cleanup architecture;
8. conceptual interfaces and publish/reference/read/recovery/retirement/import
   flows, including failure and concurrency outcomes;
9. finite resource, security, validation, observability, and operations model;
10. one-writer migration, importer deletion, compatibility, and evolution model;
11. stable seams for `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018`;
12. actionable Phase 02–08 implementation contracts and first source anchors;
13. verification ownership, risks, assumptions, and architecture reopening
    conditions; and
14. references and definitions needed to prevent semantic drift.

Do not prematurely freeze Phase 02's exact canonical codec/hash grammar or
Phase 03's micro-optimized durable fence sequence. Fix their owner, boundaries,
constraints, and proof obligations.

If no candidate qualifies, write only the bounded no-winner record required by
`SPEC.md` section 15. State `PHASE_02 = STOP` and `PHASE_03 = STOP`; do not
publish a proposed architecture disguised as a result.

## Practical process

1. Read all required documents in order.
2. Seal the product evidence tree and stop on drift.
3. Restate R0 from Phase 00 facts and focused e497 source anchors.
4. Test concrete R0 failure hypotheses with focused source/dependency checks.
5. Admit alternatives only under the Phase 01 specification.
6. Complete candidate cards and apply hard rules before simplicity/performance.
7. Select one joint winner only with no architecture-changing open gap;
   otherwise select no winner with one bounded unblocker.
8. Write root `architecture_design.md` as the whole-program architecture output.
9. Self-check S1–S5 and every required architecture component.
10. Update Phase 01 `PLAN.md` status/checkmarks only when truthful.
11. Return a short report: result, architecture path, files changed, checks run,
    source seal, and remaining owner decisions.

## Definition of done

- [ ] Root `architecture_design.md` exists and is dated.
- [ ] It has exactly one `WINNER` or `NO_WINNER` headline.
- [ ] Product worktree is sealed at the recorded clean e497 base.
- [ ] R0 is evaluated first as a joint ownership/storage candidate.
- [ ] Alternatives are evidence-motivated rather than strawmen.
- [ ] Winner, if any, closes all architecture-changing gaps and maps hard rules
      1–10 to mechanisms and later proof.
- [ ] Architecture includes exact authorities, dependency direction, storage
      family, failure model, resources, migration, source disposition, and
      Phase 02–08 contracts.
- [ ] Open owner decisions remain open behind stable seams.
- [ ] Rejected and non-admitted options have concrete reasons.
- [ ] Stage 4.6 and guessed performance/LOC do not select the winner.
- [ ] `NO_WINNER` stops later phases and names a bounded unblocker when required.
- [ ] Phase 01 S1–S5 pass.
- [ ] No product code, live state, migration, cutover, or legacy data changed.

## Style

- Plain English and compact tables; use diagrams only for material relationships.
- Keep e497 facts distinct from selected V2 architecture.
- Mark evidence `SOURCE-VERIFIED`, `SPIKE-VERIFIED`, `INFERRED`, or `OPEN`.
- Use exact package/module paths for implementability claims.
- Make the result and Phase 02 disposition visible in the first screen.
- Keep the root architecture useful as a durable whole-program contract, not a
  transcript of the selection process.

## Out of scope

```text
NO product implementation
NO architecture-only or storage-only winner
NO forced winner
NO silent owner-DEC closure
NO Stage 4.6 performance claim
NO live cutover or migration execution
NO legacy-data deletion
NO new package/framework without a proved necessity
```

When finished, point the user at:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/architecture_design.md
```
