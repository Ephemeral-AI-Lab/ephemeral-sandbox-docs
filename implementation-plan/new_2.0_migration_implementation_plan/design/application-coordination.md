---
status: draft-challenger
authority: application-contract-after-dec-012
depends-on:
  - ARCH-BND-001
  - ARCH-BND-004
  - ARCH-BND-006
  - REQ-API-001
  - REQ-COR-009
  - REQ-COR-012
  - REQ-COR-014
  - REQ-COR-015
---

# Existing application coordination

## No new coordinator

R0 keeps coordination in the existing manager/runtime application owners. It
does not introduce a V2 coordinator component, facade, package, service,
deployable, journal, authoritative cache, background workflow, or generic
transaction layer.

The exact number of current authorization, request-binding, fleet-fence,
operation, cleanup, and result-decision owners is `OPEN`. Phase 1 must map the
actual code and call graph. The word “coordination” is a behavior description,
not a component or authority count.

R0 also adds no `StateStore` API and no aggregate `WorkspaceBackend` API by
assumption. Existing application code calls the repurposed selected-state owner
and the applicable existing workspace/execution/file-effect owners through the
narrowest compile-valid calls. Exact call edges and method counts remain
selection outputs. A trait, port, wrapper, registry, RPC, or new interface is
eligible only when deleting it produces a concrete failing execution and its
total cost is lower than direct use.

## Complete operation proof

Phase 1 inventories every pinned manager/runtime and observability operation
name, HTTP route, RPC control operation, legacy proposal, and current caller/
signature/result/error. Public/private/control classification changes the
compatibility contract; it never permits omission. A design row does not
authorize a method or turn observability/control into selected-state authority.

Every retained operation records:

1. caller, authentication, authorization/fence, target, normalized immutable
   request binding, and disclosure rule;
2. every actual selected-state and runtime-effect call in order;
3. the resource owner and pre-allocation charge for each byte, inode, worker,
   FD, queue entry, slot, and external allocation;
4. durable custody before an irreversible system-issued runtime effect;
5. one public outcome/visibility point;
6. cancellation, timeout, crash, retry, compensation, uncertainty,
   quarantine, and operator-resolution behavior;
7. restart behavior at each cross-owner cut; and
8. compatibility owner, telemetry, and deletion condition.

Calls are fused whenever one owner can preserve the same linearization,
durability, and failure semantics. No generic prepare/commit choreography or
saga is accepted merely because this document describes an ordering.

## Semantic order for a mutating runtime effect

```text
authorize and cross the accepted race-safe fence
normalize and bind the complete semantic request
precharge every participating owner's finite local resources
if any charge fails:
  release acquired capacity in stable reverse order
  return typed overload before durable mutation or external effect
classify exact replay/conflict/expiry/freshness at the durable owner
if a fresh external mutation is required:
  durably record effect custody
  dispatch to the exact existing generation-bound effect owner
  resolve completion/failure or preserve charged quarantine
finish result-specific cleanup and join request-scoped work
make capacity release and durable attribution visible
durably terminalize one exact outcome
respond
```

This is a semantic partial order. Phase 1 selects the fewest actual calls,
records, barriers, and syncs that implement it. The selected-state writer never
invokes runtime effects, and runtime-effect owners never write selected-state
truth.

## Replay, ambiguity, and disclosure

Response loss is not evidence that an effect did not occur. After accepted
authorization and capacity admission, the durable owner atomically binds or
verifies the authenticated namespace, caller key, and immutable semantic
descriptor before revealing outcome, custody, pending, freshness, or conflict
state. Descriptor mismatch reveals none of those facts. Pruned exact results do
not become fresh requests; bounded authenticated evidence returns
`replay-expired` before dispatch.

A fresh static rejection is durably bound as `Rejected` without effect custody.
Every system-issued mutating runtime dispatch has durable custody first.
Automatic redispatch requires intrinsic idempotence or exact generation-bound
deduplication. Arbitrary command and mutable-file effects may finish as
`OutcomeUnknown` and are never silently repeated.

No terminal result is public or replay-visible until result cleanup,
request-work join, capacity visibility, and durable attribution have completed.
An unresolved effect keeps its exact generation fenced, charged, and
quarantined until synchronized completion, failure, compensation, or
containment proves that no further controlled local effect can occur.

## Recovery

Each durable/resource owner starts closed, reconstructs only its own truth and
debt, and reports readiness. Existing application owners reconcile durable
pending/custody facts with opaque generation-bound runtime evidence. They
resume only effects whose contracts prove safe replay; otherwise they complete
a real compensation or expose the exact terminal/unknown result while
preserving quarantine and charges.

Admission opens only after all required owners are ready and reconciliation,
cleanup, attribution, and reserve proof pass. No volatile continuation is
authoritative, and no owner imports another owner's physical census or debt.

## File operations

The public surface remains `file_{verb}`. For `file_read`:

- without `workspace_session_id`, the existing application owner captures one
  committed head revision and the bounded read stays on that immutable view;
- with `workspace_session_id`, it proves sandbox/session ownership and resolves
  the exact live allocation generation before calling its existing file-effect
  owner.

The two branches share public validation and bounds but not internal authority.
No `workspace_file_read` or other workspace-prefixed alias is introduced.
Committed state is immutable, so V2 `file_write` and `file_edit` target an
accepted live workspace session rather than mutating a selected root.

## Checkpoints, forks, and external rollouts

If checkpoint/fork/rollback/`commit_fork` are accepted, existing application
owners compose bounded selected-state root/reference and OCC effects. For every
same-accepted-`StateId` reference creation, move, transfer, no-op, deletion,
crash, and recovery path, the complete operation performs zero selected
immutable payload reads, writes, or copies and creates zero root-private closure
bytes. Bounded metadata I/O is counted separately. The accepted binding is
available only after the selected-state owner has compared exact canonical
bytes for any occupied candidate digest. Unequal bytes are the terminal
`T03_REJECTION / STATE_ID_COLLISION`; that path creates no alias, reference,
mapping, revision, custody, or capacity fact and cannot invoke the COW fast
path. Collision admission and bounded cleanup are separately charged.

MCTS and parallel rollout selection, expansion, simulation, scoring,
backpropagation, scheduling, and pruning remain external product policy. They
are not selected-state operations, durable records, caches, or runtime-owner
responsibilities. An inactive root retains no mutable allocation, worker, FD,
permit, or cache; every active realization is independently admitted and
contained.

## Phase contract

Phase 0 freezes the judge. Phase 1 selects, implements, and qualifies exact
non-live `H_PRECUTOVER` in order. Phase 2 cuts over that artifact, observes it,
retires compatibility, requalifies changed `H_RELEASE`, and releases. No Phase
1 path may acknowledge live V2 state.
