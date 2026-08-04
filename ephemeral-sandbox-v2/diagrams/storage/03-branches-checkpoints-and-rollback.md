# Branches, checkpoints, fork, and rollback

**Status:** selected R0 reference semantics; implementation proof is `NOT_RUN`

**Authority:** [V2 PRD](../../PRD.md) -> approved Phase 01
[input and selection contract](../../phases/01-choose-design/SPEC.md) -> selected
Phase 01 [architecture output](../../architecture_design.md)

**Purpose:** define the durable reference vocabulary and show why fork,
checkpoint-to-existing, rollback-to-existing, and same-Version moves do not
copy, read, or rewrite accepted payload bytes.

This chapter uses **Branch** for the product-facing mutable reference backed by
the selected store's revisioned **Head** record. A product Branch may also own
an isolated runtime Workspace, but that Workspace and its upperdir are not part
of durable selected-Version authority. A **Checkpoint** is a fixed durable
**Root** reference. These names do not introduce a registry, coordinator, or
second writer.

Content-defined chunking (CDC), Chunk content-addressed storage, durable
backend profiles, and runtime-Workspace adapters are not invoked by the
reference operations shown here. CAS+CDC remains unselected under the current
Phase 01 document.

## Question answered

How can multiple agents start from one immutable Workspace Version, evolve in
isolation, checkpoint or fork it, and move back to an existing Version without
copying the Version's payload?

```text
 immutable Workspace Version       small durable references
 +-------------------------+       +------------------------------+
 | Version V7              |<------| Branch agent-a: V7, rev 18  | mutable by OCC
 | complete payload closure|<------| Branch agent-b: V7, rev 3   | mutable by OCC
 +-------------------------+<------| Checkpoint baseline: V7      | fixed

 Accepted-reference payload bytes read/written/copied are 0/0/0 for the exact
 Head create/replace/remove and fixed-Root create/remove operations. Reference
 metadata, coordination, and durability-fence work are nonzero. Ordinary reads,
 Candidate capture/admission, and runtime materialization are outside the claim.
```

## Legend

```text
[V]     accepted immutable Workspace Version and its complete payload closure
[B]     Branch: mutable OCC-controlled selected reference, stored as a Head
[C]     Checkpoint: fixed durable Root reference
[W]     isolated mutable runtime Workspace; not portable selected-Version truth
---->   reference names a Version
===>    successful durable reference transition
-X->    rejected transition

Payload-I/O counters count accepted immutable payload bytes only:
  P.read     accepted payload bytes read by the reference operation
  P.written  accepted payload bytes written by the reference operation
  P.copied   accepted payload bytes copied by the reference operation

Small reference records, validation metadata, and durability bookkeeping are
metadata I/O and are intentionally not called zero-I/O.
```

## Reference model

```text
 SELECTED DURABLE TRUTH

 versions/
   V1  [V] complete immutable payload closure
   V2  [V] complete immutable payload closure
   V3  [V] complete immutable payload closure

 heads/                         roots/
   agent-a [B]                  checkpoints/
     binding = V3                 baseline [C]
     revision = 12                  binding = V1

                    names                         names
 [B agent-a, V3, r12] -----------> [V3]   [C baseline, V1] ------> [V1]

 Only the store owner (`sandbox-runtime-layerstack`, rewritten for V2) may
 accept a Version or durably transition these references. App owners perform
 auth, request ordering, and call orchestration; they do not become another
 reference writer.
```

`Version` means an admitted complete immutable portable value plus its typed
`VersionId` and `AcceptedBinding`. A Branch does not contain a delta chain. A
Checkpoint does not freeze an upperdir or mount. Both references name accepted
Versions.

### Branch versus checkpoint

| Property | Branch | Checkpoint |
|---|---|---|
| Durable storage form | Mutable Head record | Fixed typed Root record |
| Target | One accepted Version binding | One accepted Version binding |
| Mutation rule | Strict OCC over `(binding, revision)` | Not retargeted; create a new checkpoint instead |
| Primary use | Agent/session line of work | Named durable restore/fork point |
| Writable files | Separate runtime Workspace/upperdir | None |
| Selected-Version authority | The Head record under the one LayerStack-0 writer | The Root record under the one LayerStack-0 writer |
| Payload identity | Never defined by branch name or revision | Never defined by checkpoint name |
| Deletion effect | Removes the Branch Head after exact OCC validation | Removes that fixed Root explicitly |

If product language treats a Branch as the combined app context, Workspace,
and selected binding, the diagram's `[B]` is specifically its durable storage
component. The runtime Workspace remains with the existing workspace/mount
owner.

## Fork from an accepted Version

Fork creates another mutable Branch reference to the same immutable Version.
It does not clone a directory tree or allocate another accepted payload.

```text
 BEFORE

 [B agent-a, V3, r12] ------------------------------> [V3]


 FORK branch agent-b FROM agent-a's captured V3

 1. app resolves and authorizes the source binding V3
 2. store verifies V3 is an accepted complete binding
 3. store creates a new Head for agent-b at revision 1


 AFTER

 [B agent-a, V3, r12] -------------------+
                                          +-----------> [V3]
 [B agent-b, V3, r1 ] ===================+

 accepted payload bytes for the fork reference operation:
   P.read    = 0
   P.written = 0
   P.copied  = 0

 metadata effect:
   one new complete Branch/Head record
```

The runtime may subsequently create an isolated Workspace for `agent-b`, with
its own private writable effects and an immutable V3 base supplied through the
runtime adapter. That later activation is not part of portable identity and is
not part of the zero-payload fork operation. A cold activation may materialize
the complete Version with nonzero payload I/O; a warm adapter may reuse an
existing validated base. Both paths are accounted separately in
[the EphCoW runtime chapter](04-ephcow-runtime-view.md).

## Create a checkpoint of an accepted Version

A reference-only checkpoint fixes a name to an already accepted Version.

```text
 BEFORE

 [B agent-a, V3, r12] ------------------------------> [V3]


 CHECKPOINT accepted binding V3 AS review-ready

 AFTER

 [B agent-a, V3, r12] -------------------+
                                          +-----------> [V3]
 [C review-ready, V3] ===================+

 accepted payload bytes for the reference operation:
   P.read    = 0
   P.written = 0
   P.copied  = 0

 metadata effect:
   one new complete fixed Root record
```

The Checkpoint never retargets. If a caller wants `review-ready` to mean a
different Version later, the API must create a distinct checkpoint identity or
perform an explicit delete-and-create protocol; it must not silently mutate a
fixed Root.

### Checkpoint an existing Version versus capture current Workspace

```text
 EXISTING VERSION                           MUTABLE WORKSPACE

 accepted binding V3                       [W private upperdir]
        |                                           |
        | create fixed Root                         | first build, validate,
        v                                           | canonicalize, and admit
 checkpoint C3                                     v
 P.read/written/copied = 0                 accepted Version V4
                                                    |
                                                    | then create fixed Root
                                                    v
                                             checkpoint C4
```

Only the left-hand operation has the mandatory zero-payload-I/O property.
"Checkpoint my current Workspace" is a product-level composition: if the
Workspace differs from every accepted Version, candidate creation and
admission must first read Workspace content and may write a new complete
payload. Once V4 is accepted, creation of its fixed Checkpoint reference is
again reference-only.

## Roll back a Branch to an existing checkpoint

Rollback is a strict OCC transition of one Branch. It neither edits the old
Version nor reconstructs a delta path between the two Versions.

```text
 BEFORE

 [C baseline, V1] ----------------------------------> [V1]

 [B agent-a, V3, r12] ------------------------------> [V3]


 REQUEST

 rollback branch agent-a to checkpoint baseline
   expected = (binding V3, revision 12)
   desired  = binding V1


 LINEARIZATION

 store transition gate:
   reread exact Branch/Head
   compare expected (V3, r12)
   durably replace complete Head with (V1, r13)  <=== one OCC point


 AFTER

 [C baseline, V1] -----------------------+
                                          +-----------> [V1]
 [B agent-a, V1, r13] ===================+

 [V3] remains immutable and may remain reachable from other roots/custody.

 accepted payload bytes for rollback-to-existing:
   P.read    = 0
   P.written = 0
   P.copied  = 0
```

A stale expected value loses cleanly. The store does not merge the caller's
old Branch with the current Branch, rebase it, or retry using a newly observed
revision.

## Revision prevents ABA

Comparing only the Version binding is insufficient because a Branch may move
away from V1 and then back to V1. The monotonically changing Branch revision
preserves that intervening history.

```text
 time       Branch value             event
 ----       ------------             -----
 t0         (V1, revision 10)         client A captures expected value

 t1         (V2, revision 11)         client B publishes V2

 t2         (V1, revision 12)         client B rolls back to V1

 t3         expected (V1, rev 10)     client A tries to publish V4
            actual   (V1, rev 12)
                         ^
                         +------------ revision mismatch; reject stale OCC

 binding-only comparison would incorrectly accept the t3 write.
```

The exact revision encoding, wraparound policy, stable Branch identifier, and
record format are Phase 03 decisions. The selected design requires an ABA-safe
expected-value check; a finite revision field that can silently wrap is not
acceptable.

## Same-Version move

Even when the desired Version equals the current Version, an authorized Branch
transition may need to advance the revision so ordering and idempotency remain
unambiguous.

```text
 expected (V3, r12) + desired V3
              |
              v
      [B agent-a, V3, r13]

 accepted payload bytes:
   P.read = P.written = P.copied = 0
```

Phase 03 may choose a precisely specified idempotent no-op result instead, but
it must preserve strict OCC and ABA safety. It may not make the outcome depend
on payload copying or layer reconstruction.

## Delete and recycle semantics

Deleting a Branch removes its Head; deleting a Checkpoint removes its fixed
Root. Neither directly deletes the referenced Version or mutates its payload.

```text
 BEFORE DELETE

 [B agent-a, V3, r12] -----+
                            +-------------------------> [V3]
 [C review-ready, V3] -----+
 [reader custody V3] ------+


 delete Branch agent-a with expected revision 12
             |
             v
 [B agent-a] removed; Checkpoint and reader still retain V3


 delete Checkpoint review-ready
             |
             v
 no durable root remains, but reader custody still retains V3


 reader releases custody
             |
             v
 exact root/head/custody revalidation
             |
             v
 Version V3 becomes retirement-eligible; bounded cleanup may retire it
```

Deletion rules:

1. Branch deletion is an OCC-controlled transition. A stale delete cannot
   remove a newer Branch value.
2. Checkpoint deletion names the exact fixed checkpoint identity. It cannot
   mean "delete whichever checkpoint now has this display name."
3. Reference deletion changes reachability only. It is not an immediate
   payload/chunk deletion command.
4. Retirement waits for exact revalidation of all supported roots, Heads, and
   reader custody. Derived refcounts or indexes may accelerate that check but
   cannot replace authority without proof.
5. Reuse of a human-readable Branch or Checkpoint name must not revive stale
   handles. The exact stable-id/incarnation scheme is deferred to Phase 03/04.
6. Under selected R0 there is no authoritative chunk graph to recycle. If a
   future CDC/chunk store is selected after reopening Phase 01, it must add a
   proved manifest/chunk reachability and reclamation protocol; these reference
   semantics alone are not that protocol.

See [read lifetime, recovery, and retirement](../06-read-lifetime-recovery-and-retirement.md)
for the complete reader-versus-last-root race.

## Public API and owner-decision seam

The storage primitives are selected; the full public operation catalog is not
silently decided here.

| Seam | Locked storage behavior | Still open outside this diagram |
|---|---|---|
| Fork existing accepted Version | Create another Branch/Head reference; payload counters are `0/0/0` | Public operation name, authorization surface, and app response shape |
| Checkpoint existing accepted Version | Create a fixed Root; payload counters are `0/0/0` | Public checkpoint naming/name-reuse policy, retention UX, and catalog placement; fixed-Root replacement is forbidden |
| Checkpoint current Workspace | Admit a complete candidate first when needed, then create the fixed Root | Whether and how public/sessionless file flows expose this composition; `DEC-017` remains open |
| Rollback Branch to existing Version | Strict OCC Head transition; payload counters are `0/0/0` | Public operation naming and application-level policy |
| Sessionless write/edit | Cannot bypass the one writer or mutate an accepted Version | Accept, adapt, or reject and exact V2 target/API remain open in `DEC-017` |
| Auth/revoke race | Store OCC stays mandatory regardless of policy | Application cutoff/ordering policy remains open in `DEC-018` |

The pinned e497 public catalog does not itself prove a final V2 public
fork/checkpoint/rollback surface. Phase 04 must wire the selected primitives
without turning application policy into storage authority. No open owner DEC is
accepted on the owner's behalf here.

## Selected invariants and delegated mechanics

| Topic | Status | Constraint |
|---|---|---|
| Branch is a mutable revisioned selected reference | **SELECTED R0** | Durable form is the store-owned Head; exactly one OCC transition point |
| Checkpoint is a fixed durable reference | **SELECTED R0** | Durable form is a typed Root; it never mutates an accepted payload |
| Reference-only fork/checkpoint/rollback-to-existing | **SELECTED R0** | Accepted payload bytes read, written, and copied are each zero |
| Revision-based ABA prevention | **SELECTED R0** | Expected check includes a changing revision/incarnation, not binding alone |
| Complete immutable Version target | **SELECTED R0** | No layer-chain truth or layer-depth reconstruction |
| Branch/checkpoint record spelling and revision representation | **DEFERRED PHASE 03** | Must be complete, durable, checksummed/validated, ABA-safe, and bounded |
| Public operation names and policies | `OWNER_DEC_OPEN` where governed by `DEC-017`; otherwise deferred Phase 04 | Must preserve the selected storage semantics |
| CDC/Chunk physical sharing and backend/runtime contracts | **PROPOSED ONLY** | Adoption changes the storage family and requires Phase 01 reopening |

## Verification mapping

| Claim | Evidence now | Later proof owner |
|---|---|---|
| The selected owner can represent roots/Heads beside complete accepted payloads | `INFERRED` from selected R0 and source placement | Phase 03 layout and restart tests |
| Fork/checkpoint/rollback-to-existing need no accepted payload I/O | `INFERRED` from reference indirection | Phase 03 payload-I/O counters and deterministic tests |
| Strict OCC rejects stale and ABA writes | `INFERRED` required outcome; exact mechanics deferred | Phase 03 two-publisher and ABA histories |
| Checkpoint of a changed live Workspace may require candidate admission | `INFERRED` consequence of complete immutable truth | Phase 02/03 admission tests and Phase 04 composition tests |
| Deletion cannot race reader custody or last-root retirement | `INFERRED` mechanism family | Phase 03 custody/retirement races |
| Public API shape and sessionless semantics are final | `OPEN`; deliberately not claimed | Product owner and Phase 04 |

No spike or benchmark was used. Historical Stage 4.6 results remain
`INCOMPARABLE` and cannot prove these semantics.

## Reopening conditions

Reopen Phase 01 if implementation evidence shows that:

- a Branch or Checkpoint must name a mutable/layer-derived payload rather than
  an accepted complete immutable Version;
- rollback-to-existing or fork requires payload copy or layer reconstruction;
- selected references require a new registry, service, helper process, or
  writer outside the selected store owner;
- ABA safety cannot be implemented with one bounded revisioned Head protocol;
  or
- CDC/Chunk physical truth or new durable backend/runtime adapter semantics
  become required rather than an optional future storage-family proposal.

## Related documents

- [Architecture design](../../architecture_design.md)
- [LayerStack-0 Version-storage design](../../design/03-state-store.md)
- [Algorithms and call flows](../../design/04-algorithms-and-call-flows.md)
- [Selected storage model](../02-storage-model-and-content-addressing.md)
- [Proposed backend abstraction and runtime isolation](04-ephcow-runtime-view.md)
- [CDC boundaries, resynchronization, and reuse](08-cdc-boundaries-resynchronization-and-reuse.md)
- [Existing fork/checkpoint/rollback view](../03-fork-checkpoint-rollback-and-cow.md)
- [Publication, strict OCC, and recovery](05-publication-occ-and-recovery.md)
- [Read lifetime, recovery, and retirement](../06-read-lifetime-recovery-and-retirement.md)
- [Terminology](../../branding/terminology.md)
