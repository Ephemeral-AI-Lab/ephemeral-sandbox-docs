---
status: draft-gate-contract
authority: qualification
---

# Qualification gates

## Evidence-state discipline

Every gate report uses exactly one status:

- `NOT_RUN` — no evidence at this scope;
- `PARTIAL(scope)` — a model, lab, package, runtime profile, shadow, rehearsal, or live
  subset passed, with missing scope explicit;
- `PASS` — all evidence required for the named phase/scope passed;
- `FAIL` — at least one rejection condition occurred; or
- `BLOCKED(reason)` — required evidence cannot currently be produced.

A model/lab result cannot be promoted to an implementation result, and a Phase
or artifact result cannot be promoted to different bytes. `H_PRECUTOVER` names
the exact content-addressed integrated source/build/config/executable/
migration-tool artifact that passes the complete pre-live suite and rehearsal;
live cutover/observation must run those exact bytes. `H_RELEASE` names the
changed content-addressed artifact after compatibility/migration-code
retirement, total gate disposition, exact-artifact qualification, and fleet
rebinding at a new release epoch. `H_PRECUTOVER` evidence and receipts cannot
qualify or activate `H_RELEASE`. Every report names the exact commit/tree,
artifact/config, environment, corpus, and gate version.

## Gate schedule

| Gate | Phase 0 — Independent judge and evidence seal | Phase 1 — Non-live selection, implementation, and qualification | Phase 2 — Irreversible cutover, observation, retirement, and release |
|---|---|---|---|
| `QG-PROV-001` provenance | seal inputs and rules | every artifact from joint `H_PROFILE` through byte-identical `Hqual(H_PRECUTOVER)` | exact `H_PRECUTOVER` at 2A–2B; exact changed `H_RELEASE`, total disposition, and new release receipts at 2C–2D; optional destruction has its own record |
| `QG-DES-001` boundaries | seal comparison and deletion rules | joint result `1A H_PROFILE`; enforce it through 1B–1F | enforce at 2A–2C; total exact-artifact disposition and live topology attestation at 2D |
| `QG-SEM-001` semantics | seal oracle and total operation map | joint model/lab at 1A, then exact production scopes 1B–1F | exact `H_PRECUTOVER` at 2A–2B; disposition-bound exact `H_RELEASE` scope at 2D |
| `QG-FMT-001` format | seal fact corpus and limits | joint model/lab at 1A, `1B H_FMT`, and every consumer through 1F | exact-artifact scope at 2A and disposition-bound scope at 2D |
| `QG-CRASH-001` crash/effects | seal process-death and host-power-loss cuts | joint authority/method model at 1A, then 1C–1F production cuts | exact live cuts at 2A–2B; changed-artifact qualification and new-release-epoch fleet cuts at 2D |
| `QG-RES-001` resources | seal limits, loads, and measurement | joint model/lab at 1A and all applicable 1B–1F scopes | exact live scope at 2A–2B; disposition-bound and live-release scope at 2D |
| `QG-SYS-001` unsafe/substrate | seal inventory and falsifiers | joint spikes/candidates at 1A and exact production artifacts 1B–1F | exact deployed bytes at 2A–2B and changed bytes/live process inventory at 2D |
| `QG-ADP-001` runtime-effect conformance | seal spike scenarios and laws | joint spikes at 1A; current Linux at 1D; exact `H_PRECUTOVER` at 1F | exact live scope at 2A–2B; disposition-bound changed-artifact scope at 2D |
| `QG-MIG-001` migration | seal source and fence model | joint model at 1A; importer/fence and exact artifact at 1E–1F | fleet barrier at 2A; observation at 2B; no-reference proof, new release epoch, and complete fleet rebind at 2C–2D |
| `QG-PERF-001` performance | **seal the sole numeric/statistical contract** | selection/holdout at 1A and exact implementation scopes through 1F | exact observed `H_PRECUTOVER` at 2A–2B; total-disposition `H_RELEASE` scope at 2D |
| `QG-OPS-001` operations | seal runbook and monitor contract | rehearsal against byte-identical `H_PRECUTOVER` at 1F | exact cutover/observation at 2A–2B; exact release-epoch upgrade and live attestation at 2D |
| `QG-RET-001` retirement | seal target and policy schema | no retirement result | retire/build `H_RELEASE` and total QG disposition at 2C; exact qualification, fleet deployment, old-process drain, and live release at 2D; destruction requires distinct post-release approval |

Phase numbers indicate when evidence first exists, not permission to waive later
scopes. For changed bytes, every QG ID must be rerun or carry the accepted
complete-closure non-impact proof defined below; omission never transfers a
pass.

The only ordering vocabulary is: Phase-0 judge seal → joint `1A
H_PROFILE/NO_WINNER` → `1B H_FMT` → `1C Hstore` → `1D Hpermanent` → `1E`
exact `H_PRECUTOVER` → `1F Hqual` naming byte-identical `H_PRECUTOVER` → `2A`
exact-artifact cutover plus durable fleet barrier → `2B`
bounded observation → `2C` compatibility retirement and `H_RELEASE` build →
`2D` total exact-artifact qualification, new-release-epoch fleet rebind, old-
process drain, live attestation, and release. Optional destructive
legacy deletion is separately signed outside this DAG.

## `QG-PROV-001` — Evidence provenance

Pass requires exact Git commit and tree, tracked/untracked/ignored declaration,
dependency lock, compiler, binary/config/image, kernel, filesystem/mount,
runtime, allocator, CPU, memory, cgroup, descriptor, corpus, and runner identity.
Preserve commands, exit codes, monotonic timings, order/seed IDs, expected and
actual results, raw logs, and content-addressed artifacts with a strict path set.
An independent reviewer reproduces the manifest and key assertions without
trusting report prose.

Reject mixed commits, overwritten runs, mutable fixtures, omitted failures,
untracked inputs represented only by a Git SHA, or a report whose numbers do not
resolve to raw artifacts.

For every complete joint Phase 1A topology × physical-profile card, the
provenance bundle is incomplete unless it also contains exact typed inputs,
outputs, preconditions, and postconditions; I/O-complete pseudocode for every
branch; each linearization/commit point; inductively preserved invariants;
progress, fairness, cancellation, and finite retry/exhaustion rules; every
persisted crash cut with exact visible state and custody owner; and complete
`COST_RECORD` instances. It must include executable model checking, property,
differential, and fuzz commands and raw results against an independently
implemented oracle, with seed/trace/input and a mechanically minimized,
one-command counterexample for every failure. Evidence covers the complete
`O × T × applicable F` space from the
[normative terminal and fault registry](../design/requirements.md#normative-terminal-and-fault-registry),
including nested cleanup/reaper faults. A prose promise, candidate-derived
oracle, missing branch, or missing artifact rejects the card before scoring.

The evidence verifier applies one machine-checkable closure predicate before a
card becomes eligible. Every applicable operation, target, semantic branch,
payload bucket, authority, terminal, and fault cell—and every applicable cost
dimension within it—must resolve to a proved analytical or mechanically
enforced bound; a measured statistic only where the schema explicitly permits
expected/empirical performance and binds the sealed procedure, uncertainty,
and raw receipts; or proved `N/A` with an executable reachability/deletion
falsifier. Any remaining `OPEN`, `TO_MEASURE`, blank, or finite measurement used
as a worst-case or amortized bound rejects the whole joint profile before
scoring.

## `QG-DES-001` — Responsibilities and dependencies

**Pre-`DEC-012` joint-selection scope is outcome-neutral.** Pass requires one
owner/reason-to-change per invariant, explicit managed authority classes,
logical scopes and physical instances, commit/failure domains, cross-authority
state machines, dependency direction, package/process consequences, exact
API/field mapping, deletion falsifiers, and a compile-valid Rust graph. Pure
canonical identity performs no I/O; durable storage mechanisms contain no
concrete runtime brand; every existing path that orders selected-state work
with external effects is explicit. The gate does not require four boxes, a stateless application, two
ports, a named component pattern, or any preselected count.

Each candidate is one complete compile-valid topology × physical profile with
its actual Cargo/call/writer/package/process/helper/unsafe/resource/recovery
graph. Reject any candidate with a runtime brand in canonical/storage identity,
hidden truth or undeclared ordering authority, duplicate policy owner,
unexplained trait/package/process,
Cargo cycle, or test-only graph presented as production evidence. A physical
method cannot be projected onto a topology selected earlier, and performance
cannot rescue an invalid topology. `DEC-012` records one joint `H_PROFILE` and
its exact boundary laws, or `NO_WINNER`.

**Post-`DEC-012` implementation scopes enforce only the accepted graph, not any
worked draft.** Machine-check its exact `ARCH-BND-*` laws, authority ownership,
dependency directions, cross-effect ordering path, and runtime-neutrality
rules before production work. In every case, tests/fakes/candidates stay outside
production `src/`, and a generic plugin crate, grouping-directory facade, or
multiple selectable production physical profiles fail unless the accepted ADR
explicitly proves the exception. A role name is not a component, service, port,
or gate mechanism; only the accepted architecture may create one.

## `QG-SEM-001` — Product semantics

Run incumbent and candidate from equivalent independent pre-states against the
Phase 0 oracle. Cover every finally accepted operation and every mapped current/
legacy/proposed row, plus every accepted result/error,
authorization, pagination, root metadata/provenance, arbitrary byte names,
links, sparse data, conflicts, replay, checkpoints/forks/rollback, deletion,
retained conflict workspaces, cancellation, and exact attribution if retained.
Exercise current HTTP-only `file_list` independently until `DEC-017` gives it a
final disposition: committed and workspace targets, deterministic order,
directory mutation races, truncation/continuation, traversal and response
ceilings, deadlines, cancellation, allocation-generation replacement, and the
current server-generated internal request-ID behavior.
Exercise the eight current observability operation names (`snapshot`, `trace`,
`events`, `cgroup`, `resources`, `topology`, `daemon`, and `layerstack`),
`GET /health`, both `/forward/shared/...` and `/forward/isolated=...` route
families, and private authenticated `sandbox_daemon_ready` independently. For
each of the 27 public/tool operation names and every separately classified
endpoint, route family, and private control RPC, verify a total disposition and
the complete mandatory record: callers, authorization, request, result, error,
replay, revocation, generation, recovery, cancellation, resource, transport,
and compatibility. An executable `N/A` proof is required where a field cannot
apply. Diagnostics/control never acquire selected-state authority; forwarding
never acquires upstream effect, replay, lifecycle, or storage authority.
For every idempotent/replayable operation, reuse one caller key with a different
operation, target/revision/generation, actor, normalized argument, payload, and
authenticated security namespace across sequential, concurrent, crash/restart,
and exact-outcome-pruning cuts. Only the winning exact
`AcceptedRequestBinding` may replay or dispatch; every conflicting descriptor
returns the bounded non-disclosing conflict and creates no custody. Under the
accepted `DEC-018` policy, inject authorization revocation at every ordered cut
from initial check through bind/lookup, prepare, dispatch, terminalization, and
response disclosure. Snapshot semantics must reproduce the named point;
revocation-cutoff semantics must exercise the actual race-safe fence.
Revoke current target/outcome authorization after an exact result is retained:
an authenticated retry must reveal no result, custody, pending, or freshness
state until authorization is restored. Change a runtime capability after an
admitted static rejection: the same identity must still replay exact
`Rejected`, never dispatch.

Pass requires exact observable equivalence unless an accepted breaking decision
names the difference. Reject silent normalization, ambient-actor substitution,
replay by re-execution, payload copies for reference operations, implicit
rebase/merge, enumeration/runtime-dependent results, or an unmapped method.

Phase 0 semantic acceptance also freezes the complete fork contract used by any
external MCTS/search policy: an immutable parent; parent/child and sibling
isolation; deterministic ancestry/provenance, policy/configuration, fork/
request, and result IDs; typed stale-parent and stale-generation behavior;
explicit winner, winning-child, losing-child/sibling, checkpoint, root, and
workspace fates; and no merge or rebase. Search scoring, tree topology,
expansion order, and winner policy remain outside `StateId`, selected-state
authority, recovery election, and physical-method selection. Exercise the
contract sequentially, concurrently, across duplicate retries, and across
crash/restart before allowing Phase 1 selection.

## `QG-FMT-001` — Canonical format

Pass requires independent golden vectors, permutation/property distinct-fact
checks, corrupt/truncated/oversized/deep/duplicate/nonminimal/unsupported cases,
and enforced CPU/memory/depth/object/byte decoder bounds. All qualified backends
produce byte-identical identity for a commonly supported portable fact corpus;
statically unsupported facts reject before hidden allocation, while
data-dependent incompatibility discovered during bounded hidden realization
must leave no activated or acknowledged allocation after synchronized cleanup.

Any native path/handle, runtime brand, mount/device/provider identity, OCI/VM
snapshot value, physical locator, or environment-dependent normalization in
canonical bytes fails.

## `QG-CRASH-001` — Durability and external effects

Enumerate executable state machines and inject failure before/after every write,
sync, replace, parent-directory sync, authoritative revision, external dispatch,
runtime-effect linearization, response, custody transition, retirement, and cleanup.
Include torn/truncated/corrupt/ENOSPC variants admitted by the selected local
profile.

For every persisted boundary, run **distinct** process-death/SIGKILL and
host-crash/power-loss cells. A same-host process restart cannot qualify a
durability claim because dirty page-cache state may survive it. Host-power-loss
evidence must exercise the accepted real filesystem/storage substrate and
verify post-boot election from synchronized bytes; mock-only cuts are useful
model evidence but are not qualifying receipts. If a physical test fixture
cannot safely remove power, use an independently accepted substrate mechanism
whose documented failure semantics are equivalent and retain the exact
receipt; otherwise the durability gate remains `BLOCKED`.

Selected-state-authority recovery exposes one complete previous or durably
committed-new state per sandbox head/generation; never mixed/dangling truth. Every
acknowledged result survives. Commit-before-response is returned by exact replay
without re-executing effects. Each system-issued mutating runtime-effect dispatch has
durable custody before dispatch and proves deduplication, intrinsic idempotence,
safe retry cuts, or an explicit terminal request-uncertainty path. Exercise a
crash after a replayable `OutcomeUnknown` while custody remains unresolved: the
allocation stays fenced, quarantined, charged, and restart-routable until
synchronized completion, failure, compensation, or containment. Arbitrary
ambiguous commands/mutations are never silently retried, and the test does not
claim control of downstream effects initiated by guest code.

Inject cuts before and after fresh-identity static rejection, durable
`PendingResponse`, every result-specific cleanup and capacity-visibility step,
request-work join, durable attribution, terminal-visibility commit, and first
response. Race a duplicate identity at every cut. Before terminalization it may
observe only bounded pending/custody state and must never redispatch or reveal
the hidden candidate result; after terminalization it must replay the exact
result and all public-result prerequisites must already be complete. The
no-allocation rejection path must commit exact `Rejected` authority-atomically
before response and remain rejected across capability/profile changes. Exercise
current-authorization denial against retained outcome, custody, pending, and
expired identities: denial is transient, discloses none of those states, and
causes no dispatch or durable outcome replacement.

Repeat recovery/cleanup to convergence and resource plateau. Mock-only fault
injection cannot qualify filesystem or runtime durability assumptions.

## `QG-RES-001` — Capacity, memory, and concurrency

Before first allocation, prove simultaneous inequalities for selected,
temporary, recovery-reserve, reader, owner, backup/restore, import/shadow,
maintenance, and retirement capacity plus descriptors, workers, queues, and
managed memory.
Runtime-effect-specific profiles add their enforceable dimensions without changing
canonical identity. Run the complete normative terminal/fault matrix under
mixed 1, 4, 8, 16, 32, and 64 active sessions, one maintenance epoch, and
admitted reader/cursor pressure.

The same gate directly tests exact zero-I/O COW. For a frozen nontrivial
accepted `StateId` and its exact canonical bytes, measure allocated bytes/inodes
after `1`, `2`, `4`, `16`, `64`, and the accepted maximum number of
heads/checkpoints/forks reference that exact state. Attribute the
dependency-closure namespace, root/reference/provenance
metadata, and control/outcome/custody metadata separately rather than inferring
one from a total-allocation delta. At each root count, the selected immutable
physical dependency-closure contribution remains byte-for-byte exactly one
copy. The root-cardinality term contains only Phase 0-bounded reference/
retention/provenance metadata and its stated allocation rounding; request/
outcome/custody growth is measured under its own cardinalities and lifetimes.

At the selected-state authority's lowest complete access boundary, separately
instrument logical immutable-payload bytes read, bytes written, bytes copied,
new root-private physical-closure bytes, and every permitted metadata I/O class;
cache/page-cache hits and helper calls do not bypass the logical counters. For
checkpoint creation, reference-only fork, rollback to an existing state,
`commit_fork` winner transfer, same-state no-op publication, and every future
accepted no-alias reference-only create/move/ownership transfer, pass requires:

```text
total selected-state immutable payload bytes read    = 0
total selected-state immutable payload bytes written = 0
total selected-state immutable payload bytes copied  = 0
new root-private physical closure bytes               = 0
```

The four zeroes are purpose-independent. “Validation,” “integrity,” “warming,”
“prefetch,” “recovery,” or any other label cannot exempt an access. Prove them
for every applicable `O × T × applicable F` cell in the normative registry.
Only separately instrumented bounded metadata I/O and sync work may be nonzero.
If an operation separately realizes or changes a live runtime workspace, charge
and measure that runtime-owner-private payload work outside the selected-state
counters. Repeat across backup pinning, read-view custody, reference removal,
and reclamation. Separately measure divergent successors, workspaces, staging,
and reserve so the one-copy claim cannot hide their cost.

Separately force a candidate-`StateId` collision in qualification. Exercise
publication, import, recovery, index rebuild, reference-API ingress, and
last-root races with unequal canonical bytes under the same candidate digest.
Every path must return `T03_REJECTION / STATE_ID_COLLISION` before creating an
alias, head, root, mapping, index entry, closure, revision, custody item, or
capacity claim; bounded cleanup/quarantine converges and retry remains
terminal. Candidate-bearing reference requests are rejected or routed to
admission before fast-path entry; the accepted reference-only path consumes a
previously admitted authorized binding and never rereads immutable payload.
Raw digest equality alone must never enter that zero-payload fast path. The
forced seam is qualification infrastructure, not a product identity
fallback, algorithm, API, field, index, or second store.

Phase 0 must seal the physical attribution procedure before any candidate runs:
shared allocation units, packed root/control metadata, allocation rounding,
inodes/dirents, delayed allocation, capacity-visibility lag, and any selected
cross-state reuse are attributed by one reproducible rule. A candidate may not
move bytes between labels after observing results. Race **every accepted
no-alias root creation, root move, and ownership transfer** against removal and
retirement of the target closure's last other semantic root. The executable
matrix must include checkpoint creation, reference-only fork, rollback versus
target-checkpoint removal, `commit_fork` winner transfer, same-state no-op
publication, and a generic future reference move versus rollout prune or
child/parent deletion. Crash immediately before and after every authorization/
validation, metadata pin or retention acquisition, revalidation, bind/move/
commit, sync, recovery, root removal, reclamation, release, and capacity-
visibility cut. Pass requires either one authority-local atomic root-and-
closure-retention transfer or explicit durable closure-transfer custody in the
selected topology, established before the old last root may disappear and
released only after the new root is durable and capacity-visible. No head,
child, parent, checkpoint, or rollout may resolve to a missing closure; no
capacity credit may appear early; and no recovery/retry path may materialize a
second closure for the same accepted `StateId` and identical canonical bytes or
perform selected-state payload I/O for an accepted no-alias reference-only
transition.

Do not copy or shorten the terminal/fault taxonomy here. Instantiate and
fault-inject `O × T × applicable F` exactly from the sole
[normative terminal and fault registry](../design/requirements.md#normative-terminal-and-fault-registry).
Every applicable terminal cell nests cleanup-worker and reaper faults. Recovery
is tested separately from restart; stale revision separately from stale
generation; and a duplicate identity before and after every named boundary.
Each cell is executed or marked `UNREACHABLE` with an invariant plus an
executable falsifier that fails if it becomes reachable.

Every cell names its concrete join/drain, synchronization, custody, startup,
recovery, cleanup, reaper, and capacity-visibility owners; expected durable
debt; affected cache inventory rows; numeric convergence horizon; and expected
plateau. Repeat cleanup and recovery to convergence. Process exit, destructor
execution, timeout, or “the system” is not an owner.

Inventory every authority-owned nondurable cache, memo, rebuilt index view,
negative lookup, and scheduler hint. Every inventory row must record cache ID,
authority/process owner, purpose/key scope, byte/entry/descriptor/worker/
lifetime caps and precharge, invalidation triggers, expiry/TTL, reaper owner and
finite admitted schedule where expiry applies, cleanup owner for each applicable
`O × T × applicable F` cell, cleanup-failure debt/retry/escalation horizon,
restart behavior, and measured idle plateau. Fault the reaper and every cleanup
step; “eventual expiry” without an admitted bounded reaper and cleanup-failure
lifecycle fails.
Per-sandbox/session idle residency must be zero. A nonzero fixed shared baseline
passes only with a Phase 0 purpose, numeric cap, process attribution,
measurement method, expiry/rebuild/failure lifecycle, and proof that it is not
truth or required recovery state.

If external MCTS/search policy exists, test it outside storage semantics:
an immutable parent; parent/child and sibling isolation; deterministic ancestry,
policy/configuration, fork/request, and result IDs; typed stale-parent/
generation outcomes; explicit winner/child/sibling/checkpoint/workspace fates;
and no merge/rebase. Freeze numeric breadth, depth, inactive-root and active-
realization maxima, expansion/evaluation concurrency, admission order,
starvation/fairness, deadline, and typed overload. Exercise inactive fanouts
`1`, `2`, `4`, `16`, `64`, and the accepted maximum plus the maximum admitted
active-rollout mix under every applicable normative `O × T × F` cell. Inactive
rollouts retain only one immutable root reference plus bounded metadata;
mutable realizations are finite, active, and fully admitted; prune cancels and
joins work, disposes or durably quarantines the exact generation, removes
authorized roots, and withholds credit until synchronization/capacity
visibility. `commit_fork`
winner transfer must pass the four exact zero counters and atomic last-root
transfer law above. Search topology, scores, expansion policy, and winner policy
must not alter `StateId`, selected-state authority, recovery election, or
physical-method selection.

Report scratch as allocation-by-allocation maximum over time. A `2x` overlap is
accepted only for a proved write-new-before-delete-old interval; streaming,
reference-switch, and qualified in-place paths pay their own measured/proved
overlap. External sort remains an unselected candidate and receives no generic
multiplier.

For the frozen storage-side process/cgroup profile, every observation must remain at or below
`memory.high = 67,108,864 B`, strictly below `memory.max = 100,663,296 B`, swap
zero, and zero `high`, `max`, `oom`, and `oom_kill` events, together with the
managed-memory claims in `REQ-RES-001`. Phase 0 freezes sample count, polling,
confidence band, cleanup horizon, and failure rule before candidates run.

Independently, qualify `REQ-RES-010` for every selected runtime profile. Before
activation, prove that each untrusted sandbox runtime/process tree is enclosed
by its own finite parent cgroup or a runtime-equivalent
enforceable boundary. Freeze and observe its numeric memory limits, accounting
source, swap policy, hierarchy, every descendant/helper membership rule,
clone/fork/reparent/daemonization and escape behavior, supervisor/reaper
failure handling, and typed overload/termination result. Exercise normal work,
limit pressure, attempted escape, cancellation, sandbox and supervisor
crash/restart, orphan discovery, and cleanup-to-plateau. A shared trusted helper
must remain separately bounded and charged. Store these artifacts separately
from the storage-side cgroup evidence called the “PMSS service cgroup” by
Stage 4.6; that historical label does not require a new V2 service, and neither
gate result implies the other. Reject one unbounded runtime tree, unattributed helper allocation,
membership escape, missing descendant after restart, or loss of enforcement
during cleanup.

Reject one hard breach, uncharged allocation, speculative capacity credit,
unreported kernel memory, changing process profile, or failure to return to the
accepted idle plateau.

## `QG-SYS-001` — Unsafe, FFI, syscall, and substrate audit

Pass requires a sealed source-to-binary inventory of every `unsafe` block,
function, or trait implementation; FFI declaration/call and transitive native
dependency; raw syscall and `ioctl`; `mmap` and direct-I/O path; filesystem,
mount, atomicity, durability, allocation, and capacity-visibility assumption;
and subprocess/helper executable. For each occurrence record its caller,
necessity, accepted invariant, input/resource bound, privilege/capability,
kernel/filesystem/version assumption, cancellation/crash cuts, fallback, and
executable negative fixture. Reconcile the built artifact plus observed runtime
process/syscall inventory to the source record.

The same closure supplies explicit negative source-to-binary evidence for the
reflink and FUSE prohibitions. The production source, generated source, enabled
features, build scripts, complete transitive dependency graph, native linkage,
packaged files, helper launch paths, and built binaries must contain no reachable
reflink-specific wrapper/library or `FICLONE`/`FICLONERANGE` (or equivalent
clone/reflink ioctl) path and no FUSE-specific dependency, `/dev/fuse` access,
FUSE mount, mount helper, daemon, or child process. Reconcile that static closure
with syscall, mount-namespace, open-file/device, and process inventories before,
during, and after every applicable operation. Executable guard fixtures turn an
attempted forbidden ioctl, `/dev/fuse` open, FUSE mount, helper launch, or daemon
spawn into a hard failure; a finite trace with no observed use is not sufficient
without the static and negative-fixture closure. Test/oracle code may name or
trap a forbidden primitive but must remain outside the production artifact.

Reject an unlisted helper/native dependency, undocumented syscall or filesystem
promise, writable canonical mapping, reachable reflink-specific ioctl/library,
FUSE dependency/device/mount/helper/process, unsafe path without a smaller safe
alternative analysis, direct-I/O alignment/resource gap, privilege drift, or
mock-only evidence for a kernel/filesystem claim. Documenting a mechanism does
not select it; every candidate still competes under the standard-first method
protocol.

## `QG-ADP-001` — Runtime-effect conformance

Phase 1A joint-profile spikes test laws, not product compatibility. Phase 1D
applies the common suite to the permanent current-Linux integration, Phase 1F
reruns it against byte-identical `H_PRECUTOVER`, and Phase 2A–2B repeat the
required live scope against those exact bytes. Verify profile and per-
allocation attestation; static rejection before allocation; bounded hidden
realization with typed cleanup on data-dependent incompatibility; activation;
generation-bound fencing; stable portable capture; supported command/file
effects; retained reads; synchronized disposal; and cancellation/crash/retry
around every system-issued mutating runtime-effect dispatch.

Pass requires no unsupported allocation to activate or become publicly usable,
mandatory custody before every mutating runtime-effect dispatch, and no runtime
owner choice of canonical identity, selected-state representation/selection, or
public lifecycle result. A runtime implementation may use bounded private
durable coordination behind its opaque binding. Reflinks/clone ioctls and FUSE
are prohibited even as private, optional, portability, or fallback
accelerators. The only eligible acceleration classes are runtime-internal
OverlayFS, native or VM snapshots, private storage-driver acceleration, and
deduplication hints. An eligible acceleration may change cost only: enabling it
adds no privilege or capability, and disabling all of them must preserve the
full semantic, durability, admission, cleanup, and capacity suite. Hard links
may preserve one real link group inside one private captured filesystem, but
may not accelerate copying, share writable bytes, or cross workspace or
selected-state boundaries. Every applicable gate cell supplies separate
enabled-configuration and all-accelerations-disabled `COST_RECORD` vectors;
neither mode may borrow fields or samples from the other. Future compatibility
requires its own implementation and conformance phase; Linux tests cannot
establish it.

## `QG-MIG-001` — Actual-source import and monotone fleet cutover

Import byte-identifiable samples of actual deployed schema/state. Require total
old-root-to-`StateId` mapping with provenance, semantic equality, deterministic
repeat import, side-by-side capacity, backup/restore, and fail-closed corrupt or
unsupported handling.

The only legal generation transitions are:

```text
LegacyWritable(g)
  -> QuiescedForImport(g+1)
       -> LegacyWritable(g+2)   # pre-V2 abort; prove no V2 selection/operation acknowledgment was possible
       -> V2Writable(g+2)       # irreversible; generation-bound ingress remains closed
```

The selected fleet-fence protocol advances only after proving every inventoried
writer authority is generation-bound and quiescent. While ingress remains
closed, every selector first durably installs exact `g+2` in an inactive slot
and proves restart reconstruction. The global compare-and-transition from
`QuiescedForImport(g+1)` to `V2Writable(g+2)` is then atomic and is the
irreversible writable-legacy rollback boundary; it does **not** open ingress or
permit a public V2 operation acknowledgment.

Still with ingress closed, every selector atomically activates its exact durable
`g+2` slot. The system persists and can reconstruct the complete generation-
bound activation-acknowledgment set, then durably records fleet completion for
exact `g+2`. Installation and activation acknowledgments are control-plane
receipts, not public V2 operation acknowledgments. Only after fleet completion
is durable may generation-bound ingress open; that opening is the first point
at which a public V2 operation can be selected and acknowledged. Every such
selection validates the active local `g+2` token atomically. This does not
preselect a controller, broadcast, lease topology, or one receipt per process.
Stale writers and missing, ambiguous, or restarted selectors fail closed.
Generation values never move backward or reuse `g`/`g+1`; at or after the
global `V2Writable(g+2)` transition, only V2 roll-forward/restore is legal even
while ingress remains closed.

Reject dual public acknowledgments, unknown writer, incomplete or
non-reconstructible activation receipts, ingress before durable fleet
completion, public acknowledgment before ingress opens, unmapped root,
stale-token write, non-atomic local activation/fence, or any post-boundary
writable-legacy plan.

## `QG-PERF-001` — Matched performance

Phase 0 alone freezes the operation set, comparable artifacts, workload and
cache distributions, timing/setup/cleanup boundary, absolute and relative
thresholds, statistic, confidence construction, multiplicity, power/sample,
stopping, invalid-run, and holdout rules before any candidate result. That exact
Phase-0-frozen contract is the **sole** performance pass/fail rule. Changing any
part after results invalidates the affected evidence.

The current sparse-publication proposal—20 untimed warmups, 1,000 randomized
incumbent/V2 pairs per cold/warm profile, 100,000 seeded resamples, and one-sided
95% upper endpoints of `5.8136209 ms` for V2 p50 and `0.1` for
`exp(median(log(V2_i/incumbent_i)))`—is neither an SLA, an achieved result, nor
a second gate. Phase 0 may freeze it, replace it, or reject it before execution.
The legacy-control 100x claim and its derived `0.36444 ms` value are nonbinding
historical stress falsifiers only: a miss falsifies a claim to that historical
target, but neither value passes or fails V2 unless Phase 0 explicitly includes
it in the sole frozen contract before results.

The eligible standard-first small-publication arm must expose and time four
separate boundaries: (1) freeze and attest the origin, (2) bounded in-process
capture, (3) stream/canonicalize/hash/stage/verify outside the final authority
gate, and (4) a short origin-revalidation-and-selection gate. The final gate
must perform absolutely no subprocess launch or wait, unmount/remount,
selected-state immutable payload read/write/copy, or runtime-effect lifecycle work. A fast final gate
does not by itself pass: charge and report every end-to-end byte, allocation,
I/O, CPU interval, wait, cleanup action, and elapsed interval from authenticated
submission through durable exact response, including all work moved before or
after the gate.

Timing spans authenticated submission through durable exact response with
identical correctness, durability, setup, and cleanup boundaries. Report raw
p50/p95/p99/max, paired samples/order, phase traces, bytes/capacity/I/O/CPU/
memory/descriptors, and invalid-sample reasons. Other workloads require their
own Phase 0 effect-size, power, sample, and stopping contract.

Reject semantic/durability mismatch, incomparable boundaries, any breach of the
sole Phase-0-frozen endpoint rule, resource/capacity event, missing raw artifact,
hidden work outside the timed interval, or per-workload strategy cherry-picking.

The pinned Stage 4.6 P4 receipt commits to source commit
`ac5c0686807ab40ee7e4ef3ff0f8488b66292221`, tree
`918b4c0fad8ac37c5e2916d10b9b18d44cfeac55`, tracked-diff size `496505 B` and
claimed SHA-256 `1580ae28b40dee88177bfde575e16ffdf6daf2cff21d2007732b8aaaa2f4b132`, and
one P4 `mpla_lifecycle.rs` SHA-256
`72d42529d54a77db6ebfd8df82b6c0a2bdbde7920495aa25da133d51d0996cf9`.
The receipt bytes preserve those identity commitments, not the claimed dirty
patch bytes or a causal/reconstructible source closure. Untracked source bytes,
the exact executable, and the complete
toolchain/build/config/fixture/command/environment closure are not retained in
the reviewed receipt/evidence bundle. Its matched-first-three candidate median
and ratio denominator is `58.136209 ms`; its all-five candidate median is
`62.567625 ms`; its all-five candidate maximum is `65.937250 ms`; and its
control median is `36.444 ms` (the recorded matched-subset comparison is about
`1.595x` slower). These are negative historical context only. They cannot enter
a Phase 0 matched
distribution, baseline, effect estimate, or pass/fail result:

```text
R_stage46 = INCOMPARABLE
```

Stage 4.6 becomes comparator-eligible only through either a newly attested run
under the accepted protocol or reconstruction of the exact dirty source,
including every untracked input, with a content-addressed source archive or Git
bundle plus dirty/untracked archive, dependency lock, toolchain/build
configuration, executable digest, exact fixture, command, environment, and raw
result artifacts. The separate P1 activation receipt likewise preserves only
its recorded identity commitments and `102,543,360 B` historical observation;
it does not make its dirty source or executable reproducible. The `5.8136209 ms`
figure remains unmeasured, and the legacy/100 `0.36444 ms` figure remains a
nonbinding derived historical stress falsifier only. The later P6/P7 992906-era code hash
`9735e17471edc6076cb218a99204ab7aa062f1eabd2e7fce8f605c94c3ce0f65`
cannot causally own or repair the missing P4 provenance.

## `QG-OPS-001` — Operations and observation

Exercise exact cutover, abort, V2 roll-forward, monitor, alert, incident,
backup, and restore runbooks in shadow, rehearsal, and live scopes. Metrics must
expose integrity/semantic failures, stale writers, effect custody/uncertainty,
cleanup, queues, capacity/debt, cgroup/resource use, recovery, and performance.

Pass requires named owners, numerical envelopes, tested alerts, complete writer
coverage, and the accepted `DEC-011` observation horizon. Stable observation
never authorizes code or data deletion.

## `QG-RET-001` — Retirement release and optional post-release destruction

Remove only the migration/compatibility targets accepted by the frozen source
and dependency ledger, in reverse dependency order, and build the changed
artifact as `H_RELEASE`. Evidence from `H_PRECUTOVER` is input context only; it
cannot qualify changed bytes.

Before scoring or release, a machine-readable disposition map must have exactly
the following key set and no omissions:

```text
{QG-PROV-001, QG-DES-001, QG-SEM-001, QG-FMT-001,
 QG-CRASH-001, QG-RES-001, QG-SYS-001, QG-ADP-001,
 QG-MIG-001, QG-PERF-001, QG-OPS-001, QG-RET-001}
```

Every value is exactly one of:

- `RERUN(H_RELEASE, scope, receipts)`, completed against the exact changed
  source/build/config/executable closure; or
- `UNCHANGED_PROOF(H_RELEASE, closure_hash, acceptor, falsifier)`, where the
  closure is the complete transitive source, dependency, feature, linker,
  allocator, build, configuration, schema, and runtime influence graph and the
  independent executable falsifier fails if any influence was omitted.

Missing rows fail. A binary, dependency, feature, linker, allocator,
configuration, schema, process-topology, or runtime change defaults to `RERUN`;
proximity or an “unaffected” assertion is not a proof. Pass the static
retirement check only when no source, build, schema, configuration, reader,
replay, client, backup, restore, audit, legal, or operational path references
the removed compatibility surface.

`H_RELEASE` is not released merely because this map and its exact-artifact
checks pass. Use a new release epoch `r+1`, distinct from migration generation
`g+2`: freeze the expected selector/process set; install exact `H_RELEASE`
inertly everywhere; durably collect install/synchronization receipts; prove
their reconstruction after process death and host power loss; quiesce ingress;
atomically activate `r+1`; durably collect the complete activation set; drain
every old process; run the map's live scopes against the active bytes; durably
record fleet completion; then reopen ingress. Before activation, abort may
return to the already-qualified V2 `H_PRECUTOVER`. At or after activation, only
roll-forward to a qualified `H_RELEASE` is legal. Missing/restarted selectors,
receipt ambiguity, old-process traffic, or ingress before durable fleet
completion fails release.

Retirement completes only after that `H_RELEASE` qualification and fleet
release with legacy
bytes retained. Data destruction is an optional **POST-RELEASE ACTION** outside
the mandatory phase DAG, not an `H_RELEASE` subgate or completion condition.
It requires a second signed decision after release qualification and lists exact
targets, backup/recovery implications, retention/legal approvals, commands,
evidence, and post-action inventory. Reject inherited `H_PRECUTOVER` qualification,
`H_RELEASE` approval presented as deletion authority, ambiguous targets, or
deletion justified only by elapsed time. Withholding destructive approval does
not fail or reopen `H_RELEASE`.

## Minimum Phase 0 fixture classes

- empty/small/deep/wide trees; million-entry and dense large-file scale;
- real-payload sparse files, hard links, arbitrary byte names, symbolic links,
  metadata/provenance, duplicate/moved content, and repeated same-line edits;
- corrupt/truncated/oversized/nonminimal objects and unsupported facts;
- every operation in the total current/legacy/proposed/final API map, including
  all 27 current public/tool operation names—among them the eight observability
  names and HTTP-only `file_list`—plus `GET /health`, both `/forward/...` route
  families, and private authenticated `sandbox_daemon_ready`; every surface
  covers the full
  caller/authorization/request/result/error/replay/revocation/generation/
  recovery/cancellation/resource/transport/compatibility record; also cover OCC
  conflicts, retry/replay wrap, same-key/different-descriptor conflict,
  cross-security-namespace key reuse, actor substitution, ambiguous dispatch,
  cancellation, slow readers, and max concurrency;
- low capacity, descriptor/worker/queue pressure, maintenance/retirement debt,
  recovery reserve, and side-by-side import;
- every selected-state component and runtime-effect durability/effect cut;
  and
- actual legacy schemas/roots/sessions/leases/replay/provenance, all writers,
  pre-ack abort, post-ack roll-forward, backup, and restore.

Candidate-specific adversarial fixtures run against every eligible candidate
whose contract admits them; they cannot be used only against a disfavored one.
