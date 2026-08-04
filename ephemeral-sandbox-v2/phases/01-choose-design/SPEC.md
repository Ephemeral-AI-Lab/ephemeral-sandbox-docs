# Phase 01 specification — select the V2 architecture

> **Post-selection terminology note (2026-08-04):** Phase 01 used the
> pre-implementation type name `StateId`. The selected architecture now calls
> it `VersionId` under
> [ADR-002](../../design/decisions/ADR-002-version-id-naming.md). This is a
> terminology decision only; it does not reopen or alter R0's selected owner,
> complete-payload storage family, OCC, collision, or recovery contracts.

Date: **2026-08-04**  
Status: **APPROVED PHASE INPUT**  
Consumes: product contract and completed Phase 00 evidence  
Produces: [`../../architecture_design.md`](../../architecture_design.md)

## 1. Document role

This `SPEC.md` is the **input contract for Phase 01**. It does not select a
winner. It defines:

- what joint architecture decision Phase 01 must make;
- what evidence and candidate quality are required;
- what makes a candidate admissible, implementable, and preferable;
- when Phase 01 must return no winner rather than force a design; and
- what the whole-program `architecture_design.md` output must contain.

The Phase 01 agent consumes this document, evaluates the source-placeable
candidates, and writes the selected architecture—or a bounded no-winner
record—to:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/architecture_design.md
```

The root architecture document is the Phase 01 output consumed by Phases
02–08. Later agents must not rediscover or silently change its ownership or
storage-family decisions.

## 2. Phase goal and result contract

Phase 01 must make one honest, implementable **joint** decision about:

1. where selected-state ownership and all adjacent responsibilities live; and
2. what storage approach that ownership shape implements.

Architecture and storage cannot be selected independently. A package topology
that only works for a different storage method is not a candidate, and a
storage algorithm without a source-placeable owner is not a candidate.

The output must have exactly one first-screen result:

```text
WINNER: <candidate id and short name>
```

or:

```text
NO_WINNER: <specific blocking reason>
```

`NO_WINNER` is required when no candidate closes every architecture-changing
gap. It is preferable to a speculative architecture that pushes ownership,
dependency, storage family, crash behavior, or hard-rule choices into Phase 02
or Phase 03.

## 3. Authority and interpretation

Use sources in descending authority:

1. V2 product [`PRD.md`](../../PRD.md), especially hard rules 1–10.
2. Completed Phase 00 [`SPEC.md`](../00-freeze-rules/SPEC.md) and its measured
   inventories/catalog.
3. This Phase 01 specification, [`PRD.md`](PRD.md), [`PLAN.md`](PLAN.md), and
   [`test-perf.md`](test-perf.md).
4. The pinned e497 product source tree for implementability evidence.
5. Phase 02 and Phase 03 documents for the required handoff boundary.
6. The older implementation-plan appendix as background and counterexample
   evidence only.

When sources conflict, the higher source wins and the output records the
conflict. In particular:

- The human V2 package does not require the appendix's exhaustive tournament,
  gate, epoch, or ownership-ceremony machinery.
- An appendix sketch, topology, algorithm family, open DEC, or proposed package
  count is not an accepted result.
- Historical Stage 4.6 evidence is `INCOMPARABLE` and cannot rank a Phase 01
  candidate.
- Phase 00 measured the current implementation. Legacy behavior is evidence,
  not V2 semantics.
- R0 is the mandatory first candidate and default preference, not a preselected
  winner.
- `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` remain product-owner decisions
  unless explicitly decided by the owner in the session.

## 4. Evidence-base precondition

The product evidence base is:

```text
Path:   /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
Branch: codex/new-2.0-storage-core
HEAD:   e4974d1f9aac702b35e052629cb070c897989352
```

Before using the product tree, the Phase 01 agent must read its `AGENTS.md` and
`CLAUDE.md`, then run:

```bash
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git status --short --branch
```

The output architecture must record path, branch, HEAD, dirty state, and drift.
If the tree is missing, dirty, on the wrong branch, or not at the recorded
commit, stop selection and report `NO_WINNER: BASE_DRIFT ...`. Do not switch,
clean, reset, or edit the product worktree to make the evidence fit.

Read-only focused checks such as `rg`, `cargo metadata`, and existing targeted
tests are allowed. Product-source edits, full V2 implementation, live cutover,
migration execution, and legacy-data deletion are not Phase 01 work. A
disposable scratch spike outside the product tree is allowed only when one
specific architecture-changing question cannot be answered from source.

## 5. Frozen inputs from Phase 00

Phase 01 may rely on these measured facts, with the Phase 00 documents as the
full evidence:

- hard rules 1–10 are frozen product intent;
- current durable history lives in `sandbox-runtime-layerstack`;
- application ordering/composition lives primarily in `sandbox-runtime`, while
  daemon/manager retain lifecycle;
- workspace, OverlayFS, namespace, and exec are runtime effects, not portable
  state identity;
- observability is a diagnostic reader, not selected-state authority;
- current shared catalogs contain 26 operations and daemon HTTP-only
  `file_list` makes a 27-name current public/tool inventory;
- current publish can auto-merge compatible directories or eligible text, but
  V2 stale OCC must lose without silent merge/rebase;
- `file_blame`, sessionless write/edit, `file_list`, auth/revoke ordering, and
  the cutover observation window remain open owner decisions;
- fixture categories A–G are later-phase plans, not executed V2 proof;
- Stage 4.6 is historical and `INCOMPARABLE`; and
- R0 means rewriting the existing LayerStack ownership home for complete
  immutable V2 state, removing layer-history truth, retaining current app and
  Linux-effect owners, and adding no package/framework by default.

Phase 01 should perform focused source rechecks for claims that determine the
winner, but must not redo Phase 00's full inventories.

## 6. The joint selection target

Every admitted candidate must answer all of these questions as one coherent
system.

| Target | Required decision |
|---|---|
| Selected-state truth | Exact package/module/process that owns accepted immutable payloads, roots/heads, and durable transitions |
| Application ordering | Owner of authorization, request/revoke ordering, candidate orchestration, expected-head capture, and OCC call orchestration |
| Runtime effects | Owners of workspace, mount/OverlayFS, namespace, exec, host paths, and writable candidate custody |
| Lifecycle/readers | Manager/daemon lifecycle boundaries and observability/audit read-only authority |
| Storage family | Complete payload representation, accepted-ID admission, roots/heads, candidate staging, publication, OCC, recovery, retirement, and cleanup |
| Identity boundary | Portable facts included in state identity and runtime-private facts explicitly excluded |
| Writer model | One selected-state writer/transition authority and its linearization boundary |
| Migration | Temporary one-way importer placement, one-writable-truth fence, and complete deletion boundary |
| Source disposition | Useful `KEEP`, `REWRITE`, `DELETE`, `MOVE`, and `ADD` map for current packages/modules |
| Dependencies | Allowed and forbidden package/process dependency directions |
| New boundaries | Exact new crate/service/process/facade/helper/registry/coordinator, if any, and why it is necessary |
| Resources | Finite memory, disk/scratch, file-descriptor, worker, root/read, staging, recovery, and cleanup model |
| Handoffs | Exact Phase 02 identity location/contract and Phase 03 store location/contract, including stop/reopen conditions |

A response that chooses only “keep LayerStack,” only “use content-addressed
storage,” or only a publish algorithm does not satisfy the joint target.

## 7. Non-negotiable correctness gates

A winning candidate must structurally support every product hard rule:

| Gate | Required architecture property |
|---:|---|
| 1 | One complete immutable state is truth; reads need no layer-depth/parent reconstruction. |
| 2 | Equal canonical bytes under one accepted `StateId` map to exactly one physical payload. |
| 3 | Checkpoint, fork, rollback-to-existing, and same-state moves update references with payload bytes read = written = copied = 0. |
| 4 | Every occupied digest is checked by full canonical-byte comparison; mismatch is a collision and cannot change a reference. |
| 5 | Head publication has one OCC linearization point; stale loses without silent merge/rebase. |
| 6 | Committed payload cannot be modified by live file write/edit behavior. |
| 7 | MCTS/rollout/application policy remains outside storage. |
| 8 | Portable identity excludes Docker, OCI, OverlayFS, mount, namespace, host-path, process, and lease facts. |
| 9 | Migration preserves one writable truth and all import code is temporary/deletable. |
| 10 | R0 is preferred; every new boundary/package/framework must fix a proved R0 failure. |

The output architecture must map each rule to a design mechanism, current
evidence, later executable proof owner, and `PASS`, `FAIL`, or `OPEN`. Any
`FAIL`, or any `OPEN` that can change ownership, storage family, dependency
direction, writer count, crash semantics, migration truth, or a hard rule,
forces `NO_WINNER`.

## 8. Mandatory candidate R0

R0 must be evaluated first as this joint hypothesis:

```text
ownership:
  existing sandbox-runtime-layerstack package becomes the V2 state-store owner
  existing application owners keep auth, order, and orchestration
  existing workspace/overlay/namespace/exec owners keep runtime effects

storage:
  one complete immutable payload closure per accepted StateId
  roots and heads name accepted states
  one OCC head transition
  staged recoverable durable publication
  full-byte occupied-ID comparison
  no layer-chain truth
  no payload copy/read/write for reference-only moves
```

This is a hypothesis, not a result. The Phase 01 agent must test:

- whether the current package is dependency-neutral enough to remain the owner;
- whether every relevant current consumer can move to neutral accepted-state
  bindings without creating cycles or another authority;
- whether existing low-level lock/filesystem primitives make the storage family
  source-placeable;
- whether current layer/squash/depth/merge concepts can be removed from the V2
  core rather than wrapped;
- whether migration and reader/retirement behavior can remain bounded; and
- whether any current privilege, process, crash, scaling, or resource invariant
  actually requires a new boundary.

## 9. Alternative admission discipline

Admit a serious alternative only if at least one condition holds:

- a named hard rule or source dependency makes R0 invalid;
- a smaller package-deleting fusion is credibly source-placeable;
- a new boundary is required by a concrete ownership, privilege, process,
  recovery, failure-isolation, or resource invariant; or
- a different joint storage family materially simplifies the whole design
  without moving runtime-private facts into identity.

Do not invent candidates to fill a table. For every added crate, service,
process, deployable, trait/facade, helper, registry, database, or coordinator,
the candidate must state:

1. the exact R0 failure it fixes;
2. why an existing owner and direct call cannot fix that failure;
3. the new dependency, protocol, crash, retry, queue, security, resource,
   deployment, latency, cleanup, and operating costs; and
4. evidence that the boundary is required rather than merely tidy.

If no alternative reaches this threshold, the output must record the credible
shapes considered and why they were not admitted. A one-candidate gate is
honest when only one candidate is serious.

## 10. Candidate card

Every admitted candidate must have one complete card:

| Field | Required content |
|---|---|
| Candidate ID/name | Stable short identifier |
| State truth owner | Exact current/proposed package, module, process, or service |
| Application ordering owner | Auth, request/revoke ordering, expected-head capture, and OCC call orchestration |
| Runtime-effect owners | Workspace, mount, namespace, exec, and host-path custody |
| Lifecycle/readers | Manager/daemon and audit/observability authority |
| Storage approach | Complete payload, roots/heads, staging, publish/OCC, recovery, retirement, and cleanup family |
| Identity boundary | Included portable facts and excluded runtime-private facts |
| Writer model | Single selected-state writer and transition/linearization point |
| Migration placement | One-way temporary import, generation fence, and deletion unit |
| Source disposition | `KEEP`/`REWRITE`/`DELETE`/`MOVE`/`ADD` at useful granularity |
| Dependencies | Allowed/forbidden direction and current consumers affected |
| New boundaries | Exact additions and necessity evidence |
| Resources/cleanup | Finite limits, admission/backpressure, crash debt, and cleanup ownership |
| Failure semantics | Collision, stale OCC, crash prefixes, corruption, dangling reference, ENOSPC, reader/retirement races |
| Phase handoff | Concrete Phase 02 and Phase 03 owner, inputs/outputs, proofs, and stop conditions |
| Evidence | Source paths, commands, existing tests, scratch spike, inference, and open gaps |

## 11. What makes a good candidate

Correctness and implementability are gates. Among candidates that pass them, a
good candidate has the following qualities, in order:

### 11.1 Complete hard-rule compliance

The architecture contains an explicit mechanism for all ten rules and does not
depend on a later phase choosing a compatible owner or different storage
family. Performance cannot rescue an invalid candidate.

### 11.2 Source-placeable ownership

The owner exists or has a proved necessity case; dependency direction is
acyclic and respects application/effect boundaries; privileges and process
custody are explicit; current consumers have a credible transition; and no
responsibility is assigned to a package merely because its name sounds tidy.

### 11.3 Coherent storage and failure model

Payload, identity admission, roots/heads, writer/OCC, durability acknowledgement,
recovery, readers, retirement, last-root behavior, ENOSPC, and cleanup work as
one system. The candidate must not combine an ownership diagram from one design
with a storage method whose crash/resource needs require another.

### 11.4 Runtime-neutral identity

Complete portable facts are sufficient without importing workspace paths,
mount handles, OverlayFS/OCI/Docker facts, namespaces, leases, or host-specific
state. Exact occupied-ID comparison is feasible within finite resources.

### 11.5 One-writer, deletable migration

Migration is a consumer of the permanent V2 admission path, never another
truth. Its code, types, config, tests, and call sites form a temporary unit that
can be deleted without permanent V2 references.

### 11.6 Bounded resources and cleanup

Every untrusted or workload-controlled population has a finite cap and an
accounting/backpressure owner. Crashes can leave only bounded recognizable
debt; no unbounded background cache, scanner, worker pool, recovery backlog, or
GC authority is assumed.

### 11.7 Minimal justified change

Prefer deletion and rewrite inside an existing correct boundary. New packages,
services, protocols, databases, indexes, and coordinators are costs, not signs
of architecture quality. A smaller fusion may win only when its dependency and
responsibility map is actually implementable.

### 11.8 Actionable later-phase contract

Phase 02 knows exactly where pure identity belongs, the portable facts it
receives, and what it may still choose. Phase 03 knows exactly where the store
belongs, which primitives and failure semantics it must implement, and what
details remain open. Neither must choose architecture again.

## 12. Evidence quality and blocking gaps

Use these labels consistently:

```text
SOURCE-VERIFIED  measured directly from the sealed product tree
SPIKE-VERIFIED   demonstrated by a bounded disposable spike or existing test
INFERRED         reasoned implementability, with later proof owner named
OPEN             evidence or decision is missing
```

Source placement and current behavior claims require exact package/file anchors
or focused command results. New V2 semantics may be `INFERRED` when the
architecture fixes a coherent mechanism and assigns executable proof to a
later phase.

An `OPEN` blocks a winner when it can change:

- state truth owner or application/effect ownership;
- dependency direction or need for a new authority;
- complete-state versus layer/archive/DAG/database storage family;
- writer/OCC count or linearization point;
- collision, crash recovery, durability acknowledgement, or retirement model;
- migration's one-writable-truth/deletion shape; or
- ability to satisfy a hard rule within finite resources.

An owner DEC may remain open only when every currently stated outcome fits one
stable architecture seam. The output must explain that seam and the condition
that would constitute a new requirement and reopen Phase 01.

## 13. Comparison and selection procedure

1. Read the product, Phase 00, Phase 01, and downstream handoff documents in the
   required order.
2. Seal the product evidence base without changing it.
3. Restate R0 as a complete ownership/storage candidate from measured source.
4. Identify concrete R0 failure hypotheses and trace only the focused source
   paths needed to test them.
5. Admit alternatives only under section 9; document non-admitted credible
   shapes separately from correctness-rejected designs.
6. Complete a candidate card for every admitted candidate.
7. Apply the hard-rule and architecture-changing-open gates before simplicity
   or performance.
8. Compare passing candidates on dependency clarity, failure coherence,
   resource bounds, migration deletability, changes/additions/deletions, and
   evidence quality.
9. Select one joint winner only if later phases need no architecture
   rediscovery. Otherwise select no winner and name the minimum bounded
   unblocker.
10. Produce and self-check the root `architecture_design.md`; update the Phase
    01 plan only when the output passes S1–S5.

Do not use guessed LOC totals, package/component counts, appendix scoreboards,
or historical Stage 4.6 performance to rank candidates. Optional performance
evidence is sanity information only after correctness and implementability.

## 14. Required `architecture_design.md` output

The root architecture document is a whole-program contract, not merely a short
candidate scorecard. It must be human-readable, source-aware, and detailed
enough that Phases 02–08 can proceed without choosing architecture again.

### 14.1 Document control and authority

- Date, status, exactly one `WINNER` or `NO_WINNER` headline, and Phase 02
  `GO`/`STOP` disposition.
- Authority chain from product PRD through this selection specification.
- Environment seal: docs path, product path, branch, HEAD, dirty state, and
  drift.
- Explicit distinction between current-source facts, selected V2 architecture,
  inferred implementability, and later executable proof.
- Change/reopening rule and what later phases may refine without architecture
  review.

### 14.2 Decision provenance

- Candidate set and admission rationale, including R0 first.
- One complete card per admitted candidate and compact comparison.
- Why the winner passes, or the exact no-winner blocker.
- Correctness-rejected options separated from non-admitted unnecessary shapes.
- Conflicts with lower-authority appendix material.
- No Stage 4.6 or benchmark-winner claim.

### 14.3 Architecture drivers and traceability

- One row for each product hard rule 1–10 with selected mechanism, evidence now,
  later proof owner, and result.
- Quality attributes: correctness, portability, durability, consistency,
  bounded resources, security/trust, operability, testability, and deletion.
- Assumptions and explicit non-goals.

### 14.4 System context, authority, and dependencies

- System/component context diagram where it materially helps.
- Exact selected-state, application-ordering, runtime-effect, lifecycle,
  observability/audit, and migration authorities.
- Allowed and forbidden dependency directions.
- Process, privilege, trust, and write-authority boundaries.
- Exact count and necessity case for every new architectural boundary.

### 14.5 Source/package disposition

- Current-to-target map using `KEEP`, `REWRITE`, `DELETE`, `MOVE`, and `ADD`.
- First source/package paths for each owner and downstream phase.
- Legacy layer, squash, depth, merge, lease, delta, or other concepts that must
  disappear or hard-fail in the permanent V2 path.
- Temporary coexistence/deletion rules so source migration cannot become dual
  runtime truth.

### 14.6 Domain and portable identity model

- Conceptual definitions of portable facts, canonical bytes, `StateId`,
  accepted binding, payload, head/revision, typed roots, candidate, and read
  custody.
- Included portable facts and forbidden runtime-private fields.
- Complete-state, physical uniqueness, immutability, and exact-comparison
  invariants.
- Phase 02's permitted choices for exact codec/hash/limits and its stop/reopen
  conditions.

### 14.7 Storage architecture

- Chosen physical storage family and conceptual layout for payloads, staging,
  heads, roots, and recovery/control metadata.
- Payload admission and occupied-ID collision behavior.
- One-writer model, OCC linearization, and clean stale semantics.
- Durability acknowledgement, atomicity assumptions, and supported-filesystem
  obligation.
- Read capture/custody, retirement/last-root, reachability, orphan/staging
  cleanup, and corrupt/dangling fail-closed behavior.
- Explicit reference-only zero-payload-I/O mechanism and observability/test seam.

### 14.8 Interfaces and call flows

- Conceptual inputs, outputs, authority, idempotency, errors, and side effects
  for candidate admission/publish, reference-only moves, reads, recovery,
  retirement, and import.
- Publish, reference-only transition, captured-read, recovery, retirement, and
  migration/cutover flows using prose, tables, or sequence diagrams.
- Separation between application authorization/order and store OCC authority.
- Concurrent equal candidate, forced collision, stale OCC, crash, ENOSPC,
  corruption, reader/head move, and last-root outcomes.

### 14.9 Resource, security, and operations model

- Finite limits and accounting/backpressure ownership for bytes, entries,
  paths/depth, memory, FDs, workers, scratch/disk, roots, readers, staging, and
  recovery debt.
- Untrusted input/path/link validation and denial-of-service boundaries.
- Cleanup ownership, startup readiness, diagnostic observability, and metrics
  required to prove zero payload I/O and bounded debt.
- Performance sanity policy without unproved guarantees.

### 14.10 Migration and evolution

- Temporary importer location and one-way dependency direction.
- Monotone generation fence and one-writable-truth cutover model.
- Retry/idempotency, rollback boundary, observation window seam, and separately
  authorized legacy-data deletion.
- Complete code/config/test/call-site deletion boundary.
- Format/version evolution and reopen conditions when compatibility would
  require a different architecture.

### 14.11 Open decisions and stable seams

- `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` remain open unless explicitly
  decided by the owner.
- For each, show how all currently stated outcomes fit the selected architecture
  and what expanded requirement would reopen Phase 01.
- Appendix DECs remain proposal/open evidence rather than silently accepted
  decisions.

### 14.12 Phase implementation contracts

- Phase 02 identity owner, inputs/outputs, forbidden fields, first files,
  decisions it may make, proof obligations, and stop conditions.
- Phase 03 store owner/dependency direction, primitives, layout, publication,
  recovery, zero-I/O, retirement, cleanup, first files, permitted details, and
  stop conditions.
- Ordered Phase 04–08 responsibility/handoff summary so integration, importer,
  qualification, cutover, and cleanup cannot change the architecture silently.

### 14.13 Verification and reopening

- Trace architecture claims to Phase 02–08 tests/owners.
- Required collision, OCC, crash-prefix, immutability, zero-payload-I/O,
  recovery, resource-bound, migration-fence, and deletion proofs.
- Risks, assumptions, source-drift triggers, failed-proof handling, and exact
  architecture reopening conditions.
- References and a glossary for normative terms whose ambiguity could change
  implementation.

Do not freeze Phase 02's exact canonical codec/hash grammar or Phase 03's exact
micro-optimized fence sequence merely to make the architecture document longer.
The output fixes their constraints, owner, and proof gates while leaving those
bounded details to the correct phase.

## 15. No-winner output

If no candidate qualifies, `architecture_design.md` must not contain a proposed
topology disguised as a selection. It must contain only:

- dated `NO_WINNER` headline and `PHASE_02 = STOP` / `PHASE_03 = STOP`;
- sealed environment/evidence base;
- every admitted/rejected candidate and its exact failing rule or
  architecture-changing gap;
- the minimum missing evidence or owner decision needed to reopen selection;
- a bounded next action tied to one answerable question; and
- why later phases cannot proceed without choosing architecture themselves.

Do not overwrite a previously accepted architecture with a no-winner record
without explicit program-owner authorization; create a review/change proposal
and stop if an existing root architecture is already authoritative.

## 16. Phase exit checks

The Phase 01 agent must map the output directly to `test-perf.md`:

| Check | Passing result |
|---|---|
| S1 | Root `architecture_design.md` exists, is dated, and has exactly one result headline. |
| S2 | R0 was evaluated explicitly as a joint ownership/storage candidate. |
| S3 | A winner, if any, passes all hard rules with no architecture-changing open gap. |
| S4 | Rejected and non-admitted options have concrete reasons. |
| S5 | No winner is used when nothing valid is implementable. |

Phase 01 is complete only when the output is internally consistent, later-phase
handoffs do not require architecture rediscovery, and the Phase 01 plan can be
truthfully checked.

## 17. Authorized scope and exclusions

| Allowed | Forbidden |
|---|---|
| Read/search the sealed product tree | Edit, switch, commit, reset, clean, or push the product worktree |
| Write root `architecture_design.md` and Phase 01 evidence/status docs | Implement identity/store/product wiring |
| Read-only source/dependency checks and targeted existing tests | Full performance bake-off or V2 performance guarantee |
| Bounded external scratch spike for one unresolved placeability question | Product-source spike without separate authorization |
| Recommend owner decisions and show their effects | Accept an owner DEC on the owner's behalf |
| Update Phase 01 plan only after the output passes | Rewrite product/root contracts to match a preferred candidate |

Preserve unrelated dirty/untracked documentation files. Never use destructive
reset, broad checkout, or `git clean`.

## 18. Required reading

Read in this order:

1. `../../README.md`, `../../PRD.md`, `../../PLAN.md`
2. Phase 00 `SPEC.md`, `inventory-surfaces.md`, `inventory-packages.md`, and
   `fixture-catalog.md`
3. This `SPEC.md`, then Phase 01 `PRD.md`, `PLAN.md`, and `test-perf.md`
4. Phase 02 and Phase 03 `PRD.md`, `PLAN.md`, and `test-perf.md`
5. Product worktree `AGENTS.md`, `CLAUDE.md`, maintainer architecture guide,
   and focused e497 source paths
6. Appendix `design/architecture-selection.md`, `architecture.md`,
   `source-layout.md`, `storage-model.md`, `state-store.md`,
   `algorithms/registry.md`, `algorithms/selection-protocol.md`, and
   `decisions/README.md` as lower-authority evidence

The Phase 01 prompt may repeat these instructions to remain standalone, but it
must treat this specification as input and `../../architecture_design.md` as
the output.
