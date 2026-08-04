---
status: draft-challenger-law
authority: unique-selected-state-writer-law
candidate: R0-in-place-reuse
depends-on:
  - ARCH-BND-001
  - ARCH-BND-006
  - REQ-COR-004
  - REQ-COR-005
  - REQ-COR-007
  - REQ-COR-008
  - REQ-COR-009
  - REQ-COR-012
  - REQ-COR-013
  - REQ-COR-014
  - REQ-COR-015
  - REQ-RES-001
  - REQ-RES-003
  - REQ-MIG-003
---

# Unique selected-state writer laws

> **HISTORICAL CHALLENGER LAW.** Current terminology is LayerStack-0,
> Candidate, `VersionId`, AcceptedVersion, AcceptedBinding, Head/HeadRevision,
> and typed Root. Current storage is the selected filesystem-native
> complete-Version family; use the current
> [architecture](../../../ephemeral-sandbox-v2/architecture_design.md) and
> [archive compatibility map](../../README.md) before Phase 02+ work.

## Functional label, not a new component

This file defines the behavior often abbreviated “StateStore.” It does not
mandate a `StateStore` type, trait, API, module, package, component, service,
process, or deployable.

R0 tests a zero-addition source change: repurpose the existing
`sandbox-runtime-layerstack` ownership unit/package as the only V2
selected-state writer. The implementation keeps none of the LayerStack model.
If R0 fails, Phase 1 may select another complete architecture or `NO_WINNER`.
The final writer's methods, call edges, source shape, physical schema, and
component/package/process counts remain `OPEN`.

Exactly one selected-state writer owns authoritative V2 heads, revisions,
retained roots, and selection of immutable custody. This does not imply that
authorization, public result policy, runtime effects, or migration have the
same owner. Phase 1 maps every durable/effect authority separately.

## Minimum semantic truths

These are required outcomes, not preselected rows or fields. The winning method
must derive and fuse every redundant representation.

| Truth | Why it survives | Minimum law |
|---|---|---|
| selected sandbox head and revision | content identity alone cannot express which root is selected or prevent ABA | one writer and one authoritative revision path; no fallback selector |
| retained named root | checkpoint/fork retention is product ownership, not content | one bounded reference form; no history chain |
| immutable custody and selected lookup facts | reads and exact retirement must find every selected dependency | representation-specific and exact; no persistent refcount or resident repository index |
| workspace origin and opaque generation binding | publication OCC and crash recovery must bind the exact mutable source | retain only facts not derivable from selected state or runtime attestation |
| request binding/outcome/effect custody, if accepted | commit-before-response and ambiguous effects must not redispatch silently | exact owner and bounded replay law selected in Phase 1; no generic workflow engine |
| legacy mapping | cutover needs deterministic old-to-new identity/provenance evidence | migration-only and deletable after release/no-reference proof |

No table, prefix, record, manifest, graph, pack, catalog, selector, digest,
replay window, GC method, recovery protocol, or sync sequence is selected here.

## Complete immutable state

A published `StateId` is one collision-safe binding to complete immutable
canonical filesystem bytes/facts, not a layer, delta history, mutable checkout,
or manifest/version chain. Equal facts deterministically derive equal candidate
IDs. An occupied candidate ID is accepted only after exact canonical-byte
equality; equal bytes coalesce and unequal bytes fail closed as
`T03_REJECTION / STATE_ID_COLLISION` without aliasing or disclosure. The
selected-state writer never calls a runtime-effect owner and never stores a
runtime-native path, mount, namespace, device, snapshot, provider identity,
WASI/VM handle, or OCI value as selected identity.

V2 steady state has no LayerStack, parent-applied lookup, squash/autosquash,
depth state, squash remount, lower-carrier rebuild, layer GC, or rollback replay.
Legacy forms may exist only behind the inventoried read-only legacy adapter
called by the temporary migration unit. Permanent V2 code cannot depend on
either.

## Exact zero-copy COW

Within one selected authority/profile, every root naming the same already
accepted no-alias `StateId`
shares exactly one stored immutable physical dependency closure:

```text
D_same_state(N) = D_closure(StateId) + sum(D_bounded_root_metadata(i), i=1..N)
D_immutable_closure_due_to_root_count(N) = D_closure(StateId)
```

For checkpoint creation, reference-only fork, rollback-to-existing,
`commit_fork` winner transfer, same-state no-op publication, and every present
or future same-`StateId` reference creation, move, ownership transfer, or
deletion, the **complete operation** has:

```text
selected-state immutable payload bytes read         = 0
selected-state immutable payload bytes written      = 0
total selected-state immutable payload bytes copied = 0
new root-private physical closure bytes              = 0
```

This law begins only after collision-safe admission. A raw digest hit during
candidate publication, import, recovery, or index reconstruction must compare
complete canonical bytes with bounded streaming work; that CPU, I/O, scratch,
temporary custody, cleanup, and replay cost is charged to admission, never
hidden in the reference-only fast path. The reference law is purpose-independent and covers success, no-op, duplicate,
conflict, stale parent, cancellation, timeout, crash/restart, recovery,
root/checkpoint deletion, last-reference races, and cleanup. Bounded
root/provenance/OCC/outcome/custody/framing/inode/synchronization metadata I/O
is precharged and measured separately. Validation, closure scan, verification,
warming, prefetch, recovery, or retry cannot conceal payload I/O.

Fixed configured replication/erasure redundancy is part of the one selected
closure and is independent of root count. A separately admitted
runtime-owner-private realization is outside the selected-state counters but
inside the complete workflow's resource, I/O, and latency accounting. Unique
divergent successor payload, staging, mutable runtime workspaces, readers,
retirement debt, outcomes, and recovery reserve are separately charged; none
weakens the same-state law.
Reflinks/clone ioctls and FUSE are prohibited even as runtime-owner-private,
optional, portability, or fallback accelerators. The only eligible private
acceleration classes are runtime-internal OverlayFS, native or VM snapshots,
private storage-driver acceleration, and deduplication hints. Each must remain
invisible to selected-state identity and public semantics; disabling it must
preserve every fact, result, durability, admission, cleanup, and resource gate,
and enabling it must not add privilege or capability. Hard links may represent
one real link group inside one private captured filesystem, but may not be used
as an acceleration, writable-sharing mechanism, or cross-workspace/cross-state
copy substitute.

## Selection, OCC, and durability

- Recovery selects exactly one complete authoritative revision or fails closed.
- Every immutable dependency is durable before a head/root can select it.
- A crash before durable selection exposes the previous complete state; after
  selection it may expose the complete new state even if the response was lost.
- Every acknowledged state and exact retained result survives restart.
- Publication moves one head using strict OCC on frozen
  `(StateId, HeadRevision)`; conflict changes no head and performs no implicit
  merge/rebase.
- Content identity and authoritative revision are distinct, so equal content
  cannot create ABA.
- One format version has one production physical method. Callers cannot select
  strategies per request or workload.

Physical EOF, newest-generation election, a raw digest hit, an uncommitted candidate, a second
head, and writable legacy fallback are never authority.

Recovery or rebuild that observes two unequal durable candidates for one ID
fails readiness closed and never chooses or aliases one. Import writes no
old-to-new mapping until the same no-alias comparison succeeds. Collision
rejection is durable and replay-terminal when the operation has a request
binding; temporary candidate bytes converge through existing bounded
cleanup/quarantine custody, including last-root retirement races.

## Replay and external-effect custody

If an accepted operation can cause a system-issued mutable runtime effect, its
authenticated semantic request is durably bound before disclosure or dispatch,
and effect custody is durable before the irreversible call. Descriptor mismatch
reveals no prior outcome/custody/freshness. Exact-result pruning cannot make an
old request fresh; bounded authenticated evidence returns `replay-expired`.

Automatic redispatch is allowed only for intrinsic idempotence or exact
generation-bound deduplication. Time never clears custody. Unresolved custody
keeps the exact runtime generation fenced, charged, and quarantined. A public
`OutcomeUnknown` may replay exactly while custody remains open. Result cleanup,
work join, capacity visibility, and durable attribution complete before one
terminal visibility point.

The exact record layout and whether outcome/custody share physical bytes remain
method decisions. The selected-state writer does not authorize users, decide
public workflow, or invoke runtime effects.

## Reads and retirement

A committed read captures one authoritative revision once and traverses that
immutable view. A `file_read` with `workspace_session_id` instead targets the
exact authorized live runtime generation and does not read selected mutable
state. The public name remains `file_read` in both cases.

Semantic roots, selected physical dependencies, transient staging custody,
open effect custody, and old-reader custody are distinct. Root deletion grants
no speculative credit. Physical credit follows exact reachability and selected
dependency proof, owner/custody proof, reader close/drain, unlink, and required
parent synchronization. Idle sandboxes/sessions retain no read slot, cursor,
FD, worker, buffer, cache, or permit.

Persistent refcounts, persistent application caches, global resident indices,
repository-sized memory, unbounded queues/pools, hidden databases/LSMs/WALs,
and unbounded background cleanup are forbidden.

## Resource and cleanup law

Before its first allocation, the selected-state owner obtains/records finite
capacity for only its own managed bytes, workers, queues, FDs, custody slots,
scratch, storage bytes/inodes, maintenance, recovery, and retirement debt. It
does not import a runtime owner's dimensions, handles, census, allocation, or
recovery debt. Exact admission placement and call shape remain open.

The accepted implementation must enforce the storage-managed `8 MiB` ceiling,
normal `4 MiB` target, per-sandbox concurrent claim at most `4 MiB`, heavy-
operation claim at most `2 MiB`, `memory.high=64 MiB`, exact
`memory.max=96 MiB`, and swap disabled. These are whole-service constraints,
not per-session reservations.

Every cache is optional, bounded, reconstructible, non-authoritative, charged
before insertion, evicted by a finite policy, and cleared on idle/expiry,
cancellation, error, conflict, restart, and owner teardown. Qualification must
show the synchronized post-cleanup plateau under mixed 1/4/8/16/32/64-session
load, including maintenance and slow/cancelled readers. Overload is typed and
occurs before allocation or effect.

## Recovery and migration

Startup remains closed while the selected-state owner validates authoritative
roots and dependencies, reconciles actual owned allocation, removes only proved
orphans, performs required synchronization, reconstructs only local debt, and
resolves/enumerates retained pending/custody work. Runtime-effect owners recover
independently; existing application owners reconcile their opaque results.

Migration uses one monotone fleet generation and the temporary dependency graph
defined in `migration-cutover.md`: migration code may call a read-only legacy
adapter and the narrow selected-state import command, while permanent V2 code
never calls migration code.
Every imported candidate passes exact no-alias admission before its mapping or
root becomes authoritative; collision leaves no partial mapping or selection.
Writable legacy rollback ends at the global `V2Writable` transition while
ingress is still closed. The first possible public V2 operation acknowledgment
occurs only after complete selector activation, durable fleet completion, and
ingress opening. The importer and compatibility path are removed only in changed `H_RELEASE` after
live observation and no-reference proof; destructive legacy-byte deletion is a
separate post-release action.

## External rollout policy

MCTS, parallel rollout, branching, scoring, selection, pruning, scheduling, and
backpropagation are external policy. The selected-state writer offers only
accepted bounded root/checkpoint/fork/OCC/cleanup effects. It owns no search
tree, scheduler, task fanout, score, or rollout cache. Inactive roots add only
bounded metadata; active mutable realizations belong to separately admitted
runtime owners.

## Gate

No writable V2 truth is accepted until Phase 1 selects the architecture and
physical method, compiles the permanent implementation, seals exact
`H_PRECUTOVER`, and qualifies its correctness, crash, resource, COW, recovery,
migration, and operation-cost contracts. `NO_WINNER` closes the gate.
