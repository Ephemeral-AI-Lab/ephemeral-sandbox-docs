---
status: draft
authority: requirements
---

# Design requirements

## Responsibility

This document owns the externally required behavior, safety invariants,
resource ceilings, portability constraints, prohibitions, and success criteria.
It does not select an architecture mechanism or storage algorithm.

## Correctness and identity

- **REQ-COR-001 — Complete immutable state.** A published state is one complete,
  immutable canonical filesystem state identified by `StateId`. V2 has no
  logical layer chain, history-depth lookup, or reconstruction through retained
  state history. The selected root container, envelope, or manifest shape is a
  joint Phase 1A `H_PROFILE` representation decision, not a requirement.
- **REQ-COR-002 — Complete root identity without aliasing.** State identity binds every accepted
  product-visible canonical root fact, including root metadata. Ownership,
  attribution, or provenance participates only if the accepted `DEC-001`
  product contract retains it. Equal qualified facts produce identical canonical
  bytes and therefore the same candidate `StateId`. For accepted/published
  states, the converse is enforced: the same `StateId` must resolve to identical
  complete canonical bytes/facts. A raw digest match is never equality proof.
  On an occupied candidate ID, exact canonical-byte equality coalesces; unequal
  bytes fail before publication as `T03_REJECTION / STATE_ID_COLLISION`. The
  colliding candidate receives no identity, root, head, mapping, index, closure,
  revision, custody, or capacity credit and learns nothing about the incumbent.
  No child-object topology or root wrapper is implied.
- **REQ-COR-003 — Determinism.** Equal qualified filesystem facts produce
  byte-identical selected canonical bytes and the same candidate `StateId`, independent
  of source enumeration order and qualified execution environment. This does
  not require an object graph.
- **REQ-COR-004 — Crash outcome and acknowledgment.** Recovery may expose the
  complete previous state selected by the accepted storage authority or one
  complete durably committed new state; it must never select mixed or dangling
  dependencies. Every
  acknowledged result survives. Commit-before-response may leave a complete new
  state that the caller had not observed; exact replay resolves that uncertainty
  without re-executing the effect.
- **REQ-COR-005 — One head transition.** Publication moves exactly one sandbox
  head under strict optimistic concurrency control. It never implicitly
  rebases, merges, or writes a second head selector.
- **REQ-COR-006 — Stable session actor.** An accepted mutable session freezes one
  internal actor identity used for capture and, if retained by `DEC-001`,
  attribution. Retry must not substitute ambient caller identity.
- **REQ-COR-007 — Exact zero-copy COW for selected-state immutable payload.** Within one
  configured selected-state storage authority/profile, every root that names the
  same already accepted, no-alias immutable `StateId` names exactly one selected-state immutable physical
  dependency closure across that profile. Every **same-`StateId`, reference-only**
  semantic-root creation, move, replacement, or ownership transfer is subject
  to one purpose-independent accounting law. Across the complete selected-state
  authority boundary, the transition's totals are exactly:

  ```text
  total selected-state immutable payload bytes read = 0
  total selected-state immutable payload bytes written = 0
  total selected-state immutable payload bytes copied = 0
  new root-private physical closure bytes = 0
  ```

  The law applies to checkpoint creation, reference-only fork creation,
  rollback to an existing state, `commit_fork` winner transfer, same-state
  no-op publication, and any future operation whose selected-state effect is
  only to create, move, replace, or transfer a reference to an already accepted
  no-alias `StateId`. A candidate digest hit is admission work: it must perform
  exact canonical equality, and its CPU, I/O, bounded scratch, temporary custody,
  cleanup, crash, and replay costs are charged outside this reference-only law.
  It applies on normal, conflict, stale-revision/generation,
  duplicate/replay, cancellation/timeout, process crash, `SIGKILL`, host crash,
  power loss, restart, last-root race, and recovery paths. Naming an access
  “validation,” “integrity verification,”
  “warming,” “prefetch,” “recovery,” or any other purpose cannot exempt it.
  Only separately instrumented, Phase 0-bounded authority, root, retention,
  provenance, control, outcome, custody, framing/rounding, inode/dirent, and
  synchronization metadata I/O is permitted. Rollback replays no delta
  sequence, and no same-state reference transition may materialize or privately
  retain another copy of the selected immutable closure.
  For `N >= 1`, root multiplicity therefore changes only the bounded root term:

  ```text
  D_same_state_root_contribution(N) =
      1 * D_physical_closure(StateId)
    + sum(D_root_reference(i), i = 1..N)

  0 <= D_root_reference(i) <= D_bounded_root_reference
  D_same_state_root_contribution(N)
    <= D_physical_closure(StateId) + N * D_bounded_root_reference

  D_immutable_closure_due_to_root_multiplicity(N)
                  = 1 * D_physical_closure(StateId)

  # forbidden term:
  N * D_base_payload
  ```

  This equation is deliberately scoped to the closure and semantic-root
  contribution. Request outcomes, effect custody, readers, and retirement debt
  use their own cardinalities and lifetimes in the complete capacity equation.

  `D_physical_closure` already includes any separately accepted fixed
  redundancy policy across its failure domains and does not grow because
  another root points at the state. This is an exact `1x` closure law, not a
  “near `1x`” target: physically materializing one base per root and relying on
  later compression or deduplication fails the requirement.
  This is exact zero-copy COW for selected-state immutable payload through
  immutable references, not filesystem clone/reflink/OverlayFS/snapshot
  sharing. Divergent successor content, runtime-owner-private mutable
  workspaces and realizations, staging, and recovery reserve are separate,
  admitted, and fully charged capacity/I/O classes. Runtime-owner-private
  realization may copy or materialize its own non-selected bytes, but it may
  never relabel a
  selected-state immutable payload read, write, or copy as realization work to
  evade the exact counters. Exact zero selected-state immutable payload I/O does
  **not** mean zero metadata I/O: every accepted same-state reference transition
  separately
  charges its bounded root, provenance, control, exact-outcome,
  framing/rounding, inode/dirent, and synchronization costs, and qualification
  instruments those costs independently from selected-state immutable payload
  and closure counters.
- **REQ-COR-008 — Exact retention and last-root transfer.** Semantic roots,
  selected physical dependencies, transient owner custody, and old-reader
  custody are distinct facts. Reclamation must be exact and reader-safe. Every
  root create, reference-only fork, rollback, `commit_fork` winner move, rollout
  prune, checkpoint removal, child/parent deletion, and retirement path races
  against removal of the target state's last other root. The transition must
  either atomically move/create the root inside the owning authority or hold
  durable transfer custody from before the old last root disappears until the
  new root is durable, recoverable, and visible to capacity accounting. A
  `STATE_ID_COLLISION`, including one racing last-root retirement, cannot retire
  old custody, create a second closure, or make capacity visible early.
- **REQ-COR-009 — Custodied environment-effect dispatches.** Every
  system-issued mutating environment-effect dispatch obtains durable,
  crash-discoverable
  `EffectCustody` identity before dispatch. Custody remains unresolved or
  quarantined until the responsible runtime-effect owner proves completion, failure, compensation, or
  synchronized containment; selecting a terminal public `RequestOutcome` does
  not by itself clear custody. Automatic redispatch is permitted only when
  intrinsic idempotence or exact runtime-generation-bound deduplication is proved for that
  dispatch. Downstream effects initiated by arbitrary guest code are outside
  system authority and inherit the enclosing command's uncertainty; they are
  never claimed to be individually identified or idempotent.
- **REQ-COR-010 — Fail closed.** Corrupt, truncated, oversized, unsupported, or
  environmentally unqualified input is rejected before an unsafe effect.
- **REQ-COR-011 — No unbounded decode history.** Repeated same-line or same-unit
  edits may not create an unbounded reconstruction chain.
- **REQ-COR-012 — Exact replay, authorization, and anti-replay.** Once bounded
  replay-query admission accepts an authenticated semantic request binding
  under the authorization policy accepted by `DEC-018`, an outcome still inside
  its declared finite replay horizon returns its atomically recoverable exact
  result. The accepted authorization decision/fence is satisfied before any
  retained outcome, custody status, freshness classification, or conflicting
  prior binding is disclosed. Authorization denial is a typed transient edge
  response, not a durable `RequestOutcome`; it reveals no retained authority
  result, creates no effect custody, and authorizes no dispatch. A bounded service may likewise
  reject before authoritative lookup with a typed transient pre-admission
  overload. That overload cannot replace or prune a retained result. A later
  admitted and currently authorized retry still returns the exact retained
  result. The selected authority must also retain or derive bounded,
  authenticated freshness/anti-replay evidence after exact-result pruning. Its
  atomic prepare-or-return decision distinguishes a genuinely fresh identity
  from an expired or invalid one; an expired identity returns `replay-expired`
  without custody creation or dispatch. Re-execution is not a replay strategy.
- **REQ-COR-013 — Durable rejection and terminal-result visibility.** A
  statically unsupported or semantically invalid result produced after a
  request identity has been admitted as fresh is authority-atomically committed
  as the exact `Rejected` outcome before response and creates no
  `EffectCustody`. Every accepted terminal result becomes replay-visible only
  after all result-specific cleanup, request-work join, capacity-visibility,
  and durable resource-attribution prerequisites have completed. Before that
  barrier, a durable `PendingResponse`/custody disposition blocks redispatch
  and returns only a bounded nonterminal status to a duplicate. The final
  authority transition terminalizes the exact outcome before its first public
  response. When no external or hidden allocation exists, atomic
  reject-or-return may satisfy the barrier and terminalize `Rejected` in one
  step.
- **REQ-COR-014 — Authenticated semantic request binding.** Replay identity is
  never a bare caller-supplied key. One `AcceptedRequestBinding` consists of an
  authenticated security namespace, the caller request/idempotency key, and an
  immutable normalized semantic request descriptor. The descriptor binds the
  operation and compatibility version; target authority identifiers; every
  caller-supplied or acceptance-frozen revision/generation that affects
  semantics; the stable actor where applicable; normalized arguments; and the
  payload or a collision-resistant payload commitment. The exact canonical
  encoding and qualified standard digest remain Phase 1B decisions under
  `DEC-005`/`DEC-010`; this semantic equality law is not optional.

  The first authority-atomic fresh reject-or-return or prepare-or-return
  transition binds the key to that descriptor. Every retained outcome,
  `PendingResponse`, `EffectCustody`, freshness/anti-replay fact, and pruned
  anti-replay remainder refers to the same binding. Every later classification
  bind-or-verifies the incoming descriptor before returning authority state. A
  key reused with a different descriptor returns a bounded typed
  `request-identity-conflict`, creates no custody, performs no dispatch, and
  discloses neither the prior result nor its state. Authenticated security
  namespaces cannot alias; Phase 0 defines their exact product scope and every
  operation's normalized descriptor. Pruning may remove an exact result only
  if sufficient authenticated binding evidence remains to prevent the old key
  from naming different semantics.
- **REQ-COR-015 — Authorization linearization and revocation.** Before Phase 1A,
  `DEC-018` must accept and name the authorization linearization/revocation
  policy and its ordering relative to request binding, authoritative lookup,
  prepare, dispatch, terminalization, and every public disclosure. A snapshot
  policy is valid only if it explicitly makes the accepted authorization point
  authorize completion of that in-flight bound request despite later
  revocation. A revocation-cutoff policy is valid only with a race-safe
  authority revision, lease, or equivalent fence at every required dispatch
  and disclosure barrier; an ordinary check followed by work is not a fence.
  Any per-operation exception requires separate justification and fixtures.
  Until the decision is accepted, no workflow may silently assume either
  policy and no production implementation may proceed beyond Phase 0.
- **REQ-COR-016 — Eligible small-publication critical path.** Joint Phase 1A
  `H_PROFILE` selection must admit
  and test a standard-first small-publication candidate with four explicit
  boundaries: (1) freeze and attest the origin, (2) perform bounded in-process
  source capture, (3) stream, canonicalize, hash, stage, and verify outside the
  final authority gate, and (4) hold only a short origin-revalidation and
  selection gate. The final gate performs no subprocess invocation,
  unmount/remount, selected-state immutable payload read, write, or copy,
  activation, capture, disposal, or other runtime-effect lifecycle work. This is a
  candidate contract, not a selected implementation. Admission and performance
  evidence charge the entire authenticated-request-through-durable-response and
  cleanup path, including all work moved outside the final gate.

## Resource and concurrency bounds

- **REQ-RES-001 — Managed memory.** Storage-managed memory across the selected
  topology has an exact aggregate `8 MiB` ceiling, a normal `4 MiB` target, a
  concurrent claim no greater than `4 MiB` per sandbox, and a heavy-operation
  claim no greater than `2 MiB`. These are claim maxima, never per-sandbox
  reservations. Joint Phase 1A `H_PROFILE` must assign disjoint local caps and
  a shared recovery reserve, or select and price a different owner; the sum must fit the same
  ceiling without double-charging or gaps.
- **REQ-RES-002 — Cgroup memory.** The measured storage containment scope uses
  `memory.high = 64 MiB`, exact `memory.max = 96 MiB` (`100,663,296 B`), and
  swap disabled. The limit covers all concurrent sandbox/session storage work.
  Phase 0 must map that scope to the actual existing process/cgroup topology;
  this requirement does not create a new service or deployable.
- **REQ-RES-003 — Complete accounting.** The sealed admission model accounts
  simultaneously for
  managed memory, workers, queues, descriptors, owner custody, reader custody,
  maintenance reserve, retirement debt, per-sandbox attribution, separately
  bounded untrusted-runtime memory, and every capacity dimension declared by
  the selected-state storage and execution-profile realizations.
  The current Linux profile includes bytes and inodes; neither is hard-coded as
  a universal runtime concept. Each authority charges an exact disjoint slice
  before allocation; cross-authority operations acquire permits in a frozen
  order and release in reverse. No global admission owner is implied.
  Planning records may use `[OPEN:<owner>]` only when the placeholder fixes its
  units/domain, closure procedure, required raw receipt, and blocking gate; an
  open record cannot be scored. Before Phase 1A scoring, every applicable cost
  cell must be either (a) a proved analytical or mechanically enforced finite
  bound, (b) a Phase-0-permitted expected-case empirical statistic with sealed
  scope, raw samples, estimator, uncertainty, dependence treatment, and
  receipts, or (c) proved `N/A` with an executable falsifier. A finite sample,
  sample maximum, timeout, or absence of an observed failure never substitutes
  for a worst-case or amortized bound; those close analytically or through a
  mechanically enforced cap.
- **REQ-RES-004 — Charge before allocation.** Every declared capacity unit,
  including temporary output, allocation rounding, recovery reserve, metadata,
  and side-by-side migration capacity, is charged before first use.
- **REQ-RES-005 — No speculative credit.** Deleting a semantic root grants no
  physical capacity credit. Credit follows exact reachability proof, reader
  drain, unlink, and synchronized parent metadata.
- **REQ-RES-006 — Bounded concurrency.** Every queue, worker pool, cursor,
  reader, owner, file descriptor class, buffer, and retry is finite. Overload
  returns a typed bounded result before operation allocation. A transient
  admission overload is not an accepted operation result and does not supersede
  durable replay state.
- **REQ-RES-007 — No idle residency.** An idle sandbox or session owns no
  worker, buffer, descriptor, reader slot, selected-state cache, cursor, or
  permit.
- **REQ-RES-008 — Aggregate qualification.** Correctness, speed, and resource
  bounds hold under mixed admitted loads of 1, 4, 8, 16, 32, and 64 active
  sessions, including one maintenance epoch and slow/cancelled readers.
- **REQ-RES-009 — Cleanup plateau.** Success, conflict, cancellation, process
  crash, `SIGKILL`, host crash, power loss, restart, and recovery return every
  charged resource to the justified steady plateau after the required join and
  synchronization boundary. Each fault remains a distinct evidence cell.
- **REQ-RES-010 — Separate untrusted-runtime containment.** Independently of
  the selected/current storage-side process limits in `REQ-RES-001` and
  `REQ-RES-002`, every
  untrusted sandbox runtime/process tree must remain inside its own finite
  per-sandbox parent cgroup or a selected execution profile's proved equivalent
  enforceable containment boundary. Before activation, the selected profile
  freezes the parent/child hierarchy, every descendant/helper membership rule,
  reparent/escape behavior, finite memory limits, accounting source, and swap
  policy where applicable. Normal work, overload, cancellation, sandbox or
  supervisor process crash, `SIGKILL`, host crash, power loss, restart,
  recovery, and cleanup must neither escape the boundary nor lose attribution.
  A shared trusted helper must have a separate finite charge
  and cannot act as an uncharged escape path. Evidence for this containment is
  recorded separately from the storage-side cgroup evidence called the “PMSS
  service cgroup” by Stage 4.6; that historical label does not require a new V2
  service, and passing its `64/96 MiB` gate cannot prove this requirement.
- **REQ-RES-011 — Terminal resource closure.** Every operation and maintenance
  workflow executes the single normative registry below as
  `O × T × applicable F`. Representative-operation, representative-terminal,
  or representative-fault sampling is forbidden. Every cell is executed, or
  carries an invariant plus an executable `UNREACHABLE` falsifier. Each cell
  names the concrete join/drain, synchronization, startup/recovery, cache, and
  debt owners; its numeric cleanup/convergence horizon; and its expected
  plateau. A terminal result is not public until its cell reaches that barrier.
  Unresolved custody and cleanup debt remain durably attributed and charged.
- **REQ-RES-012 — Nondurable cache ownership.** Every authority-owned
  nondurable cache, memo, index view, and scheduler hint has a finite byte/entry/
  descriptor/worker/lifetime bound, an explicit invalidation owner, and
  automatic cleanup on every applicable terminal path. Its required inventory
  row records key scope, admission charge, invalidation triggers, expiry/TTL
  rule, reaper owner and finite reaper schedule where expiry is applicable,
  terminal cleanup owner, cleanup-failure behavior, durable/reconstructible debt
  if cleanup cannot complete, restart treatment, numeric cleanup horizon, and
  observed idle plateau. “Expires eventually” without a bounded admitted reaper
  and a faulted cleanup-failure lifecycle is not a bound. Idle per-sandbox/
  session cache residency is exactly zero. A fixed shared idle baseline is
  permitted only when Phase 0 freezes its purpose, numeric bound, process
  ownership, expiry/rebuild behavior, cleanup-failure treatment, and
  measurement procedure.
- **REQ-RES-013 — External exploration policy.** MCTS or any other search/
  rollout scheduler is external policy, never selected-state semantics or a
  storage algorithm. Phase 0 must accept one explicit fork/search product
  contract before any architecture or physical-method candidate may use forks:
  the parent state is immutable; parent/child and sibling mutations are
  isolated; ancestry, policy/configuration identity, fork/request identity, and
  result identity are deterministic under the accepted inputs; stale-parent and
  stale-generation attempts have typed non-rebasing outcomes; winner, child,
  sibling, checkpoint, and losing-workspace retention/deletion fates are closed;
  and `commit_fork` neither merges nor rebases. Search score, tree topology,
  expansion order, and winner policy remain outside selected-state identity and
  storage selection.

  The same Phase 0 contract freezes maximum breadth, depth, inactive roots,
  active mutable realizations, concurrent expansion/evaluation, admission
  ordering, starvation/fairness rule, deadline, and typed overload result. An
  inactive rollout retains only one immutable root reference plus bounded
  scheduler metadata. A mutable realization exists only while active, finite,
  and admitted under the full resource vector. Qualification exercises fanouts
  `1`, `2`, `4`, `16`, `64`, and the accepted maximum with inactive roots, plus
  the maximum admitted active-rollout mix. It tests stale-parent and concurrent
  winner races, deterministic ancestry/results, parent/sibling isolation,
  fairness/overload, duplicate retries, and the complete cleanup matrix.
  `commit_fork` winner transfer is a same-`StateId` ownership transfer governed
  by `REQ-COR-007`: total selected-state immutable payload bytes read, written,
  and copied are each zero and new root-private closure bytes are zero on every
  path, including last-root/recovery races. Pruning synchronously cancels and
  joins work, disposes or durably quarantines the exact realization, removes
  its semantic root when authorized, and releases each charge only after the
  owning cleanup and capacity-visibility boundary.
- **REQ-RES-014 — Max-over-time scratch accounting.** A `2x` scratch factor is
  not inherent. It occurs only where a selected write-new-before-delete-old
  policy overlaps complete old and new material. Streaming, reference-switch,
  and qualified in-place candidates report their own allocation-by-allocation
  maximum over time. External sort remains unselected and receives no generic
  scratch multiplier. Any external-sort candidate must derive its initial runs
  from an exact deterministic whole-record recurrence over per-record resident
  charges and encoded sizes, prove or type-bound the oversized-record path, and
  seal the actual run manifest, merge graph, and persisted event trace. It
  derives passes, byte-I/O, scratch, inode/FD peaks, syncs, and recovery work
  from those artifacts. `ceil(total_encoded_bytes / encoded_run_cap)` is only a
  lower bound absent a packing theorem; substituting a memory budget for the
  encoded run cap is dimensionally invalid.

## Normative terminal and fault registry

This is the package's **only** terminal/fault registry. Other documents must
reference its content hash and IDs; they must not maintain shorter prose copies.
Phase 0 freezes the complete public/internal/maintenance operation set `O`,
expands every parameterized ID below into concrete rows, and seals the resulting
machine-readable registry before any candidate result. Changing `O`, `T`, `B`,
or `F` invalidates all consuming selection and qualification evidence.

`B` is the ordered boundary registry. A candidate may add a boundary but may
not remove an applicable one without an executable equivalence proof:

| ID | Boundary |
|---|---|
| `B00` | before admission/request binding |
| `B01` | after binding, before durable effect custody or authoritative mutation |
| `B02` | after custody/preparation, before external dispatch |
| `B03` | after dispatch or authoritative mutation, before effect resolution |
| `B04` | after resolution, before result-specific cleanup/join/capacity visibility |
| `B05` | after cleanup barrier, before durable terminalization |
| `B06` | after terminalization, before first response |
| `B07` | after first response / replay path |
| `B08(D)` | every candidate-enumerated persisted durability subcut `D`: immediately before and after each durability-relevant record/data write, data sync, rename/replace/selector transition, directory sync, durable cleanup transition, and synchronized capacity-credit transition |

`B08(D)` is not one representative crash point. Each candidate emits the
complete machine-readable `D` set for every applicable operation, terminal
path, recovery action, and cleanup action. An omitted write/sync/selector/
directory transition is a missing test cell, not an implementation detail.

`T` is the terminal/lifecycle-path registry:

| ID | Required path |
|---|---|
| `T00_SUCCESS` | accepted success or accepted no-op |
| `T01_VALIDATION` | typed validation failure |
| `T02_AUTHORIZATION` | typed authorization/revocation failure with no retained-state disclosure |
| `T03_REJECTION` | admitted static or semantic rejection, including terminal replay-safe reason `STATE_ID_COLLISION`; collision adds no new terminal ID |
| `T04_CONFLICT` | OCC or ownership conflict |
| `T05_STALE_REVISION` | stale revision |
| `T06_STALE_GENERATION` | stale fleet/runtime generation |
| `T07_DUPLICATE@B00..B07` | duplicate/retry at every boundary, before and after each outcome cut |
| `T08_TIMEOUT@B00..B07` | deadline expiry at every applicable boundary, distinct from cancel |
| `T09_CANCEL@B00..B07` | caller cancellation at every applicable boundary |
| `T10_ABORT@B00..B07` | internal abort at every applicable boundary |
| `T11_WORKER_PANIC@B00..B07` | task/thread/worker panic at every applicable boundary |
| `T12_PROCESS_CRASH@B00..B08(D)` | storage/application process crash at every durability/capacity boundary and persisted subcut |
| `T13_SIGKILL@B00..B08(D)` | uncatchable storage/application process termination at every durability/capacity boundary and persisted subcut |
| `T14_RESTART@B00..B08(D)` | restart after each persisted pre-crash boundary/subcut |
| `T15_RECOVERY@B00..B08(D)` | recovery and reconciliation, distinct from restart itself |
| `T16_EXPIRY` | lease/session/cursor/cache-lifetime expiry where applicable |
| `T17_ROLLOUT_PRUNE` | rollout cancellation, join, root/workspace disposition, and charge release |
| `T18_ROOT_RETIREMENT` | checkpoint/root/session/reference deletion or replacement |
| `T19_LAST_REFERENCE_RACE` | last-root/reader/transfer-custody race |
| `T20_PARENT_DELETE_PARTIAL` | parent deletion with partial failure |
| `T21_GENERATION_REPLACE_PARTIAL` | parent/generation replacement with partial failure |
| `T22_AMBIGUOUS_EFFECT` | replayable `OutcomeUnknown`, fenced/quarantined unresolved custody |
| `T23_RETRY_EXHAUSTED` | finite retry budget exhausted |
| `T24_OPERATOR_ESCALATION` | finite automatic horizon ends in charged durable operator-owned debt |
| `T25_HOST_CRASH@B08(D)` | qualified host/VM crashes at every persisted durability subcut, independently of storage/application-process survival behavior |
| `T26_POWER_LOSS@B08(D)` | abrupt qualified-substrate power-loss/reset semantics at every persisted durability subcut |

`F` is the nested cleanup/reaper fault registry. `F00_NONE` is executed for
every `O × T` cell. Every other applicable fault is injected at every concrete
cleanup/deletion/reaper cut `C` named by that operation and terminal path:

| ID | Nested fault |
|---|---|
| `F00_NONE` | no nested cleanup fault |
| `F01_CLEANUP_STEP_FAIL@C` | each cleanup/join/drain/unlink/sync/capacity-visibility step fails |
| `F02_CLEANUP_WORKER_PANIC@C` | cleanup worker panics |
| `F03_CLEANUP_WORKER_SIGKILL@C` | cleanup worker/process is killed |
| `F04_REAPER_PANIC@C` | admitted cache/expiry reaper panics |
| `F05_REAPER_SIGKILL@C` | admitted cache/expiry reaper is killed |
| `F06_RESTART_WITH_DEBT@C` | restart with the exact durable cleanup debt outstanding |
| `F07_DELETE_OR_SYNC_FAIL@C` | deletion or durability synchronization fails |
| `F08_HOST_CRASH@C_PERSISTED` | qualified host/VM crashes at every persisted cleanup/reaper durability cut |
| `F09_POWER_LOSS@C_PERSISTED` | abrupt qualified-substrate power-loss/reset semantics at every persisted cleanup/reaper durability cut |

The required evidence product is therefore:

```text
RESOURCE_EVIDENCE = O × T × applicable(F)

for every cell:
  execute(cell)
  or executable_UNREACHABLE_falsifier(cell)
```

`UNREACHABLE` is not `N/A`: its invariant and falsifier must fail the candidate
if the path can be forced. The `T22_AMBIGUOUS_EFFECT` cells name fencing or
quarantine, selected request-outcome authority, restart reconciliation, zero
volatile plateau, charged durable debt, and a finite convergence or
`T24_OPERATOR_ESCALATION` horizon. `F04`/`F05` may be unreachable only when the
candidate proves it has no cache/expiry reaper and no equivalent worker.

`T25`/`T26` and `F08`/`F09` are distinct from process exit, panic, and
`SIGKILL`; replaying `T12` or `T13` does not satisfy them. Where durability
depends on a real filesystem, block device, kernel, hypervisor, or VM boundary,
qualification retains content-addressed receipts from the qualified real
substrate (for example an abrupt VM/host reset or an accepted power-cut rig) at
every applicable `B08(D)`/cleanup cut. A unit-test fault shim is supplementary
unless an independently accepted equivalence proof shows that it reproduces
the qualified substrate's write, cache, ordering, and persistence semantics.

## Portability

- **REQ-PORT-001 — Portable identity.** Canonical identity contains only
  versioned portable filesystem facts. Runtime brand, host paths, handles,
  mounts, device identifiers, provider identifiers, and physical selected-state
  locators are noncanonical.
- **REQ-PORT-002 — No environment-native leakage.** Execution-environment-
  specific paths, mounts, handles, resource identifiers, instances, and
  lifecycle facts do not enter canonical values, selected-state durable values,
  or public lifecycle meaning. Phase 1 must compare direct calls to existing
  runtime-effect owners before introducing an aggregate Backend API, facade,
  port, trait, package, component, service, or process. This is an outcome
  constraint, not a mandated seam.
- **REQ-PORT-003 — Explicit compatibility.** Every qualified execution-profile
  realization declares
  exact fact, execution, isolation, and durability capabilities. Statically
  knowable incompatibility is rejected before hidden allocation. A
  data-dependent incompatibility may be discovered only during bounded hidden
  realization and must be cleaned up synchronously before activation.
- **REQ-PORT-004 — No silent downgrade.** If an environment cannot observe,
  preserve, or reproduce a required canonical fact or requested operation, it
  returns a typed unsupported result before activation or irreversible public
  exposure. A failed hidden realization is never acknowledged as usable and
  leaves no reachable allocation or uncharged residue. Missing metadata is not
  normalized away.
- **REQ-PORT-005 — Cross-profile equality.** Any two qualified execution
  profiles applied to the same complete fact corpus produce
  byte-identical canonical facts and the same candidate `StateId`; publication
  remains subject to the same exact-byte no-alias admission law.
- **REQ-PORT-006 — Future implementations, stable core.** If the accepted
  product semantics can be supported by WASI or Firecracker, support is added
  as a qualified execution-profile realization. It must not change
  accepted canonical semantics, selected-state authority/selection, the core
  public lifecycle schema, or the public consistency model. It may own bounded runtime-private
  durable allocation/effect state, instances, and failure domains behind the
  opaque binding when its substrate requires them. A disposable contract spike
  may instead prove a runtime unsupported; this draft makes no compatibility
  promise before that evidence exists.

## Product behavior

- **REQ-API-001 — Closed use cases.** The public surface exposes authenticated,
  named sandbox/session/checkpoint/fork/rollback/read/export operations, not a
  generic transaction, key/value, locator, pack, or root-selection API.
- **REQ-API-002 — Explicit public result and ordered points.** Every mutating
  public operation has one documented accepted/no-op/conflict/unsupported or
  uncertain result and one unambiguous public outcome/visibility decision
  point. Its proof separately names and orders every selected-state authority,
  dispatch, runtime-effect, and response linearization point; it must not imply an
  atomic commit across independent authorities.
- **REQ-API-003 — Conflict readability.** A publication conflict does not
  silently destroy the losing workspace; retained access and later disposal
  follow the bounded session contract.
- **REQ-API-004 — Blame decision.** Exact `file_blame` remains an open product
  requirement. Phase 0 must accept or remove it explicitly before an
  attribution method is eligible.
- **REQ-API-005 — Total current-surface disposition.** Phase 0 must account for
  every externally reachable current operation and every private/control
  compatibility surface, not only manager/runtime names registered in a shared
  catalog. At pinned e497 the public/tool operation-name subtotal is **at least
  27 distinct names**: the exact 18 manager/runtime catalog names, 8 separate
  observability catalog names (`snapshot`, `trace`, `events`, `cgroup`,
  `resources`, `topology`, `daemon`, `layerstack`), and the catalog-external
  daemon HTTP `POST /files/list` / internal `file_list` exception. The private,
  authenticated `sandbox_daemon_ready` control RPC is inventoried separately.
  So are the unauthenticated host-loopback HTTP control endpoint `GET /health`
  and public routed path families `/forward/shared/{port}/{tail...}` and
  `/forward/isolated={workspace_id}/{port}/{tail...}`; a route family is not an
  operation-name row and is not multiplied by method, workspace, port, or tail.
  Every current operation, endpoint, control RPC, and route family receives an
  explicit retain, promote, reshape, migrate, or remove decision and exact
  caller, authorization, request, result, error, replay, revocation, generation,
  recovery, cancellation, resource, transport, and compatibility dispositions
  before the final V2 surface is frozen. A semantically inapplicable field needs
  a falsifiable `N/A` rationale and conformance test; it cannot be omitted.
  Observability, health, readiness, and forwarding remain diagnostic, liveness,
  private control, or byte-routing surfaces respectively: they may read or route
  bounded facts/effects from existing owners, but they do not select or write
  authoritative state, own storage/replay/effect custody, or become storage,
  lifecycle, repair, or runtime-allocation authorities.
- **REQ-API-006 — Bounded listing if retained.** If `file_list` or a reshaped
  listing operation remains externally reachable, its committed-state and
  workspace-session target semantics, authorization, captured view or mutation
  consistency, deterministic ordering, traversal bound, entry/byte response
  ceilings, truncation/continuation behavior, cancellation, and replay identity
  are explicit. It may not be hidden inside `file_read`, because enumeration
  and bounded byte-range reads have different cardinality, consistency, and
  denial-of-service laws.

## Migration and operations

- **REQ-MIG-001 — Actual-source import.** Migration imports the actual deployed
  legacy schema, metadata, roots, provenance, leases, replay state, and mutable
  session facts. A documentation model is not an import source.
- **REQ-MIG-002 — Total mapping.** Every imported legacy root has a recorded,
  deterministic old-to-new identity mapping and complete root provenance. The
  mapping is written only after exact canonical-byte no-alias admission; an
  unequal same-ID import writes no mapping, head, selection, or partial import.
- **REQ-MIG-003 — Monotone fleet fence.** One fleet-visible generation selects
  the active format. Every legacy and V2 durable-selection authority atomically
  conditions selection on the exact locally installed generation token, binds
  the receipt to it, and suppresses stale acknowledgment. Generations increase
  on every transition and are never restored or reused.
- **REQ-MIG-004 — No writable dual truth.** Migration may compare or import
  read-only state, but it does not acknowledge independent legacy and V2 writes
  for the same authority.
- **REQ-MIG-005 — Rollback and acknowledgment boundaries.** Returning to
  writable legacy state is permitted only before the fleet authority commits
  the irreversible transition to `V2Writable`. That transition occurs while
  ingress remains closed, so it precedes the first possible public V2 operation acknowledgment.
  After it, recovery is V2 roll-forward and legacy remains permanently fenced;
  only after every selector has durably activated and acknowledged that exact
  generation may ingress open and a public V2 operation acknowledgment become possible.
- **REQ-MIG-006 — Delayed destruction.** Legacy data/code deletion occurs only
  after no retention, replay, compatibility, reader, backup, or restore path
  depends on it and an explicit destructive gate is approved.

## Prohibitions

- **REQ-PRO-001.** No LayerStack, logical layer history, parent-applied state
  delta, squash, autosquash, squash-triggered remount, durable publication
  history, or layer-depth garbage collection in V2 steady state. Such concepts
  may appear only in a migration reader. Required per-request outcome/custody
  facts and separately retained immutable roots are not an ordered publication
  log and must not be used to reconstruct state by replaying history.
- **REQ-PRO-002.** No SQLite or other database engine, WAL, MVCC, LSM, generic
  key/value service, arbitrary keyspace, persistent application cache, or
  hidden background maintenance. No repository-sized resident or memory-mapped
  map, index, path/object/task set, queue payload, reverse map, refcount ledger,
  or cache; no full-tree buffer, unbounded queue, or unbounded worker pool.
- **REQ-PRO-003.** No runtime-selectable physical representation, codec,
  selector, or per-workload architecture menu. One version freezes one complete
  winner.
- **REQ-PRO-004.** No second selected-state root, fallback selector,
  writable post-ack legacy fallback, or recovery election among uncommitted
  candidates.
- **REQ-PRO-005.** No environment-effect owner selects `StateId`, canonical
  encoding, physical selected-state representation, lifecycle outcome, or
  selected-state admission decision.
- **REQ-PRO-006.** No reflink use, including an optional fast path. Correctness,
  identity, retention, quota, or recovery must not depend on OverlayFS, a
  Docker snapshotter/storage driver, filesystem or VM snapshots, copy-on-write
  cloning, mutable hard-link sharing, a particular host filesystem, a
  memory-backed workspace, or deduplication hints. A runtime-internal overlay,
  snapshot, or private storage-driver acceleration may exist only when
  invisible to selected-state/public semantics and disabling it preserves every
  fact, result, durability, and resource gate.
- **REQ-PRO-007.** No FUSE or userspace-filesystem process is introduced,
  including as an optional acceleration or portability path.
- **REQ-PRO-008.** No added administrative or storage-management capability,
  including `CAP_SYS_ADMIN`, is permitted. A future runtime implementation
  declares and proves its own least-privilege profile at its existing or
  selected effect boundary while satisfying this prohibition; it cannot
  broaden the core service trust boundary. Ordinary least-privilege workload
  capabilities remain runtime-owner policy, but they cannot
  expose canonical storage, mutate selected-state-authority-owned state, or
  bypass fencing.
- **REQ-PRO-009.** No canonical object is writable, and no writable data is
  shared between workspaces, allocations, selected immutable state, staging areas,
  or selected states through hard links, clone/snapshot sharing, overlay lower
  reuse, or any other mechanism. Hard-link topology that represents one real
  link group inside one private captured filesystem remains a canonical fact
  where supported; realization must keep its writable data private to that
  workspace.
- **REQ-PRO-010.** Filesystem-native or VM snapshot bytes, OCI layers,
  OverlayFS upper directories, and runtime caches are never canonical truth or
  the sole restore representation.
- **REQ-PRO-011.** No candidate passes qualification without a source-to-binary
  audit of every `unsafe` block, FFI boundary, raw syscall, `ioctl`, `mmap`,
  direct-I/O path, filesystem semantic/durability assumption, and helper process.
  Each occurrence is absent, removed, or tied to a named invariant, bounded
  resource/crash model, least-privilege justification, and executable falsifier.
  Unlisted helper processes and implicit filesystem assumptions fail closed.

## Performance classification

- **REQ-PERF-001.** Stage 4.6 measurements are receipt-backed historical
  negative context, not a reproducible Phase 0 comparator and not V2 results.
  Because the dirty source bytes (including untracked inputs), exact host
  publication-scorecard executable bytes, and complete transitive causal
  build/configuration/run closure were not archived, the current comparison
  classification is `R_stage46 = INCOMPARABLE`. Historical medians cannot enter
  a Phase 0 matched statistic. Eligibility requires either a newly attested
  comparator run or reconstruction of the exact dirty source plus a
  content-addressed archive/bundle, toolchain and build configuration,
  executable digest, fixture, command, and environment provenance.
- **REQ-PERF-002.** The `<= 5.8136209 ms` sparse-publication value is an
  unmeasured stress target derived from the matched-first-three candidate ratio
  denominator `58.136209 ms`; `<= 0.36444 ms` is likewise an unmeasured stress
  target derived from the matched-first-three control value `36.444 ms`. Both
  source values are incomparable historical receipt observations. Neither
  derived value is an achieved result, comparator, hard gate, or SLA.
  Only one exact Phase-0-frozen `QG-PERF-001` decision rule may accept or reject a
  candidate. It must use a newly attested matched incumbent and may adopt,
  replace, or reject either historical target before candidate results exist.
- **REQ-PERF-003.** Performance acceptance requires frozen fixtures and timing
  boundaries, cache-state declaration, randomized paired incumbent/V2 runs,
  raw samples, confidence calculations, resource measurements, and falsifiable
  absolute and relative thresholds.
- **REQ-PERF-004.** Isolated microbenchmark gains cannot compensate for a
  correctness, crash, capacity, cgroup, aggregate-load, or migration failure.

## Non-goals

- Inventing novel algorithms.
- Supporting arbitrary object stores, databases, or filesystems through a
  generic persistence trait before such a requirement exists.
- Preserving old internal method names, modules, records, or process boundaries.
- Providing multiple active physical formats for workload tuning.
- Implementing future execution profiles before their product requirements and
  conformance environments exist.
