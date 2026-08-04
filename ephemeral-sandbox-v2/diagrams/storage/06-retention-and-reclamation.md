# Retention and reclamation

> Status boundary: the complete-payload retirement model is **SELECTED R0**.
> The manifest plus cross-Version CDC chunk graph is **PROPOSED**, not selected.
> Adopting that graph would reopen Phase 01 because it changes payload truth,
> recovery, retirement, and resource accounting.

This document explains when immutable workspace content remains live and when
it may be reclaimed. It deliberately separates the selected LayerStack-0 model
from the proposed chunk-sharing extension so the diagram cannot be read as a
silent architecture amendment.

Authoritative context:

- [V2 product hard rules](../../PRD.md)
- [Selected architecture](../../architecture_design.md)
- [Normative terminology](../../branding/terminology.md)
- [Selected read, recovery, and retirement detail](../06-read-lifetime-recovery-and-retirement.md)

## Terms used here

The product-facing word **Version** means one admitted complete immutable
workspace value. Its typed identity is `VersionId`; roots, heads, and readers
hold an `AcceptedBinding` or store-validated equivalent, not a bare ID.

For the selected design, a Branch's accepted binding is implemented through a
mutable **Head**, while a durable Checkpoint is a typed immutable **Root**.
Branch also includes runtime and application context, so Branch itself is not a
second store-owned truth record.

```text
product term                       selected durable primitive
-------------------------------    ---------------------------
Branch.current_version          -> Head(AcceptedBinding, HeadRevision)
Checkpoint                      -> typed Root(AcceptedBinding)
captured Version reader         -> bounded read custody(AcceptedBinding)
complete immutable Version      -> complete payload closure
```

## Selected R0: exact roots plus read custody

Selected LayerStack-0 does not need a tracing object graph. A complete payload
closure may be retired only when no Head, no typed Root, and no active read
custody names it. The last check and retirement commit occur under the store
owner's transition gate.

```text
                    reachability sources

       +----------------+   +----------------+   +----------------+
       | Heads          |   | typed Roots    |   | read custody   |
       | mutable + OCC  |   | checkpoints,   |   | bounded,       |
       |                |   | migration, ... |   | runtime-local  |
       +-------+--------+   +-------+--------+   +-------+--------+
               \                    |                    /
                \                   |                   /
                 +------------------+------------------+
                                    |
                                    v
                        +-------------------------+
                        | accepted Version X      |
                        | complete immutable      |
                        | payload closure         |
                        +------------+------------+
                                     |
                     any exact live reference/custody?
                              /              \
                            yes               no
                             |                 |
                             v                 v
                          retain      final revalidation under
                                      transition gate, then retire
```

The set is exact and bounded by store limits. A persistent reference count is
not selected as independent truth: a counter can drift across crashes or
partial updates. If a count is cached for efficiency, it is derived evidence
and must be revalidated against authoritative Heads, Roots, and custody before
the last unlink.

## Why rollback does not immediately delete anything

Rollback changes one small Head record. It does not synchronously erase the
previous complete Version, and it does not inspect or copy payload bytes.

```text
before rollback                        after rollback commits

Branch B                               Branch B
Head(B) -> V3                          Head(B) -> V1

Root(CP-1) -> V1                       Root(CP-1) -> V1

payload V1  RETAINED                   payload V1  RETAINED
payload V2  maybe rooted/custodied     payload V2  unchanged
payload V3  reachable by Head(B)       payload V3  retirement candidate only

               OCC Head transition: expected V3/rev7 -> V1/rev8
               payload bytes read = written = copied = 0
```

After the exact Head replacement, V3 is eligible for retirement only if the exact
final check finds no other Head, Root, or reader. This separation keeps the
reference operation fast and keeps last-root/read races correct.

## The last-root and reader race

There are two valid winners. There is no valid history where a reader obtains
a Version while retirement simultaneously makes its payload disappear.

```text
case A: reader wins                    case B: retirement wins

reader          transition gate       gate             reader
  |                    |                |                  |
  |-- acquire X ------>|                |-- revalidate X --|
  |<-- custody held ---|                |   no roots/readers|
  |                    |                |-- retire X -------|
  |-- read X safely    |                |                  |
  |                    |                |<-- acquire X -----|
  |-- release X ------>|                |--> NOT_FOUND -----|
  |                    |                |                  |

The same serialization boundary orders custody acquisition against the final
retirement decision.
```

The implementation may optimize preparation outside the gate, but it must not
split the authoritative last-live check from the irreversible retirement
decision in a way that reintroduces this race.

## Crash and orphan handling

A payload can become durable before a Head transition loses OCC. That complete,
accepted, but unreferenced payload is an **orphan payload**: bounded cleanup
debt, not partial truth and not permission to repair the losing Head.

```text
candidate staging
      |
      v
validate + accept complete immutable V4
      |
      v
make V4 durable
      |
      +-----------------------+
      |                       |
      v                       v
Head OCC succeeds       Head OCC is stale
      |                       |
      v                       v
V4 reachable            V4 remains an accepted orphan
                        Head is unchanged
                        bounded recovery/retirement later
```

Recovery must classify recognizable staging, committed payloads, durable
references, and retirement debt. Ambiguous, corrupt, or dangling reference
records fail closed. Recovery does not guess a Head or silently merge/rebase a
stale publish.

## Proposed CAS plus CDC extension

The following model illustrates the requested chunk-sharing idea; it is **not
the selected payload model**. Here a complete workspace manifest names every
path and its ordered chunks. Liveness is transitive:

```text
PROPOSED ONLY

Branches / Checkpoints / leases / transactions
                    |
                    v
          +-------------------+
          | live Version set  |
          +---------+---------+
                    |
                    v
       +----------------------------+
       | complete workspace         |
       | manifests                  |
       +----+------------------+----+
            |                  |
            v                  v
       file metadata      ordered chunk IDs
                               |
                               v
                    +----------------------+
                    | shared immutable     |
                    | chunk content store  |
                    +----------------------+

reclaimable chunk = no live manifest transitively names it
```

Example after several edits and a rollback:

```text
PROPOSED ONLY

V1 manifest: /src/app.rs -> [A, B, C]
V2 manifest: /src/app.rs -> [A, X, C]
V3 manifest: /src/app.rs -> [A, X, D]

Branch main -> V1 after rollback
Checkpoint q -> V2

live manifests  = {V1, V2}
live chunks     = {A, B, C, X}
candidate dead  = {D}

D is not deleted during rollback. A later exact, crash-safe reclamation pass
must prove that no live manifest, in-flight admission, materialized view, or
read lease can still require D.
```

Compared with selected R0, this extension introduces a graph, transitive
reachability, multi-object publication, and shared-object last-reference
races. It therefore needs a proved source of truth for:

- manifest admission and atomic visibility;
- in-flight transaction and reader leases;
- graph traversal bounds and corrupt-edge handling;
- quarantine versus physical deletion;
- crash recovery of partially staged manifests/chunks;
- chunk collision verification using full canonical bytes;
- disk-pressure behavior and finite cleanup debt; and
- concurrent deletion versus new-manifest admission.

Those are architecture obligations, not merely a Phase 03 encoding choice.

## Safe deletion pipeline

Physical deletion should remain distinct from logical unreachability in either
storage family. The selected design can implement a bounded queue or private
retirement record without creating another truth owner.

```text
reference removed
      |
      v
candidate no longer reachable
      |
      v
exact final revalidation under transition gate
      |
      +------ live again / reader active ------> retain
      |
      v
record retirement intent or quarantine
      |
      v
unlink physical payload
      |
      v
durably clear bounded retirement debt
```

The exact write ordering is intentionally deferred to Phase 03, but every
crash prefix must expose either the prior valid truth or the complete new
truth. Retrying cleanup must be idempotent.

## Ownership and resource limits

```text
sandbox-runtime-layerstack (selected store owner)
  owns: Heads, typed Roots, read custody, recovery, retirement
  owns: bounded staging/orphan/retirement debt and observability counters

sandbox-runtime and application owners
  own: branch orchestration, authorization, request ordering, workspace life
  call: direct store APIs; they do not mutate store records independently

workspace / OverlayFS / namespace owners
  own: live upperdir, workdir, mounts, namespace, and process cleanup
  never: become portable Version identity or durable retirement truth
```

The selected implementation must bound scan work, scratch bytes, memory, open
file descriptors, workers, active custody entries, staging debt, orphan debt,
and retirement debt. `ENOSPC`, limit exhaustion, and cleanup failure must be
explicit results; they must not mutate an accepted payload or manufacture a
new reference.

## Invariants

1. An accepted Version is immutable for its entire lifetime.
2. Exact Head create/replace/remove or fixed-Root create/remove never opens
   payload bytes; generic Root update/retarget is not an operation.
3. Retirement cannot win against a previously captured supported reader.
4. Unreferenced does not mean safe to delete until exact final revalidation.
5. Recovery never invents reachability and never repairs stale OCC by merge.
6. Runtime paths, mounts, OverlayFS identities, and namespaces are not durable
   liveness facts.
7. Observability reports liveness and debt; it is not a second authority.
8. Cleanup work and debt are finite and enforce configured limits.

## What remains open

Phase 03 may choose the exact on-disk names, custody record shape, lock
primitive, sync sequence, quarantine mechanism, and bounded scan strategy, as
long as the selected ownership and complete-payload model do not change.

Phase 01 must be reopened before adopting cross-Version Chunks, a manifest DAG,
tracing garbage collection, the backend-neutral CAS+CDC durability/runtime
contracts, or a separate cleanup service. Each changes the selected storage
family or introduces a new architectural boundary. The candidate does not use
a custom filesystem or storage-specific clone feature as a correctness path.

## Related diagrams

- [Storage diagram index](README.md)
- [Branches, checkpoints, fork, and rollback](03-branches-checkpoints-and-rollback.md)
- [Proposed backend abstraction and runtime Workspace isolation](04-ephcow-runtime-view.md)
- [Publication, strict OCC, and recovery](05-publication-occ-and-recovery.md)
- [Data movement and complexity](07-data-movement-and-complexity.md)
- [CDC boundaries, resynchronization, and reuse](08-cdc-boundaries-resynchronization-and-reuse.md)
