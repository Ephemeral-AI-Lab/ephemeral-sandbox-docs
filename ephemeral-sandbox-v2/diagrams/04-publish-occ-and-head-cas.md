# R0 publish, OCC, and conceptual head CAS

**Status:** selected Phase 01 semantics; exact Phase 03 filesystem protocol and
executable proof are `NOT_RUN`
**Architecture:** [R0 LayerStack-0 Version storage](../architecture_design.md)
**Primary proof owners:** Phase 02 identity, Phase 03 store, Phase 06 exact-artifact qualification

## Authority and purpose

This document visualizes the complete R0 publication protocol. Its central
distinction is:

```text
content-addressed admission answers:
  "Which complete immutable payload does this candidate exactly equal?"

head OCC / conceptual compare-and-swap answers:
  "May this authorized request replace this selector's expected head now?"
```

They are different decisions, have different authority points, and must not be
collapsed. An admitted payload does not automatically become selected, and a
head update cannot create or validate a payload by trusting a digest.

This document is subordinate to the product [PRD](../PRD.md), Phase 00
[evidence](../phases/00-freeze-rules/SPEC.md), the Phase 01
[selection contract](../phases/01-choose-design/SPEC.md), and the selected
[architecture](../architecture_design.md). The detailed
[identity](../design/02-state-identity.md),
[store](../design/03-state-store.md),
[algorithm](../design/04-algorithms-and-call-flows.md), and
[durability](../design/05-concurrency-durability-recovery.md) contracts are
normative where an ASCII diagram abbreviates a detail.

## Legend

```text
C          unaccepted complete portable candidate facts
canon(C)   complete canonical byte stream
Sx         typed VersionId derived from canon(C)
[Sx]       complete immutable physically accepted payload closure
Bx         LayerStack-0-issued/revalidated AcceptedBinding for [Sx]
H@r        complete durable head record: (accepted binding, HeadRevision r)
T          bounded private staging transaction; never selected truth
GATE       one process/filesystem-exclusive selected-Version transition gate
LP         sole OCC head linearization point
ORPHAN     complete accepted payload currently named by no durable root/head
X          rejected or forbidden transition

---->      operation/data flow
====>      durable authoritative reference
....>      private or non-authoritative work
```

“Head CAS” is conceptual. R0 does not require a CPU CAS instruction or a
lock-free algorithm. It requires one authoritative comparison of the complete
expected head/revision under the store transition gate followed by one atomic
complete head-record replacement.

## 1. Two separate state machines

### 1.1 Content-addressed admission

```text
              complete candidate C
                       |
                       v
          validate + canonicalize + hash
                       |
                 canon(C), VersionId S1
                       |
                       v
              is VersionId S1 occupied?
                    /             \
                  no               yes
                  |                 |
                  |                 v
                  |       full canon(C) versus full
                  |       accepted canonical bytes
                  |              /         \
                  |           equal       unequal
                  |             |             |
                  v             v             v
          build bounded T   reuse [S1]     COLLISION
          complete/durable   return B1      fail closed
                  |                          no binding
                  v                          no ref change
          atomically expose one
          immutable accepted [S1]
                  |
                  v
              return B1

Admission result: an accepted binding.
Admission side effect on head: none.
```

Digest equality selects an occupied slot for exact comparison; it is not proof
that the candidate equals the occupant. A full canonical-byte mismatch is a
typed collision even if the production digest is believed cryptographically
strong.

### 1.2 Head OCC / conceptual compare-and-swap

```text
Inputs:
  selector        H:main
  expected        (B0, revision r7)
  replacement     B1, already accepted

                         acquire GATE
                              |
                              v
                  reread complete H:main record
                              |
                 current == expected (B0,r7)?
                         /               \
                       no                 yes
                       |                   |
                       v                   v
                  STALE result     prepare complete H=(B1,r8)
                  no head change           |
                  no merge/rebase           v
                                    atomic complete record
                                    replacement  <--- LP
                                             |
                                             v
                                    reference durability
                                             |
                                             v
                                       acknowledge success

OCC result: a selected-head transition or clean stale failure.
OCC payload admission: none inside the final gate.
```

The expected value includes the accepted binding and monotone Head revision. Exact
record representation and revision encoding are Phase 03 details, but no
implementation may split the final authoritative comparison from the one head
replacement so another writer can interleave.

## 2. Full publish sequence

The full candidate-bearing publish composes admission and head OCC:

```text
APPLICATION / EFFECT OWNERS             R0 STORE OWNER
---------------------------             ---------------

 1. authorize and order request
 2. capture expected H=(B0,r7)
 3. obtain complete portable candidate C
               |
               +----------------------> 4. precharge bounded resources
                                         5. validate/canonicalize/hash C
                                            -> canon(C), VersionId S1
                                         6. inspect S1 occupancy
                                            occupied -> full-byte compare
                                              equal   -> reuse B1
                                              unequal -> COLLISION, stop
                                            absent -> bounded private staging
                                                      complete/durable [S1]
                                                      accept and issue B1

                    OUTSIDE FINAL GATE  ================================
                    candidate and payload work is permitted here

                                         7. construct intended H'=(B1,r8)
                                         8. acquire the one GATE
                                         9. reread complete current H
                                        10. compare current with (B0,r7)

                    INSIDE FINAL GATE   ================================
                    bounded head/control metadata only

                       if mismatch <--- 11a. return STALE
                                           H remains unchanged
                                           no merge/rebase

                       if match:          11b. prepare complete H' record
                                        12. atomically replace H with H'  <-- LP
                                        13. satisfy reference durability
             success <---------------- 14. acknowledge after durability
```

The target payload must become complete, durable, immutable, and accepted
before step 12. The exact file/directory synchronization sequence behind steps
6, 12, and 13 is deliberately `SELECT_IN_PHASE_03`.

## 3. Outside versus inside the final transition gate

The gate protects selected-Version authority, not all publication computation:

```text
OUTSIDE GATE — bounded but potentially payload-scale
----------------------------------------------------
  candidate capture by runtime owner
  validation
  deterministic canonicalization
  digest derivation
  private staging
  complete payload construction
  occupied-ID full canonical comparison
  new payload durability and accepted occupancy

                                |
                                v

INSIDE ONE FINAL GATE — bounded selected metadata
-------------------------------------------------
  re-read current complete head record
  compare expected (binding, revision)
  decide stale or success
  install one complete replacement head record  <-- sole OCC LP
  satisfy selected reference durability

FORBIDDEN INSIDE FINAL GATE AS NORMAL WORK
------------------------------------------
  workspace mutation
  complete candidate construction
  MCTS/winner policy
  full payload copy
  layer reconstruction/squash
  silent merge/rebase
```

Moving expensive work outside the gate is a contention-reduction hypothesis,
not a benchmark result and not permission to move the authoritative expected-
head reread outside the gate.

## 4. Why admission is not selection

An accepted payload can exist without becoming the head:

```text
Initial selected truth
----------------------

  H:main@r7 =============================> B0 ===> [S0]

Candidate admission succeeds
----------------------------

  accepted occupancy:                     B1 ===> [S1]
  selected head:       H:main@r7 =========> B0 ===> [S0]

No root/head names B1 yet. [S1] is complete and safe but unselected.

Final OCC attempt discovers stale expected r7
---------------------------------------------

  another publisher already installed:
  H:main@r8 =============================> B2 ===> [S2]

  losing publisher asks: expected (B0,r7) -> replacement B1
  current is (B2,r8)
                     |
                     v
                    STALE
                     |
                     +-- no change to H:main@r8
                     +-- no merge/rebase of S1 with S2
                     `-- [S1] may be an ORPHAN

  bounded recovery/retirement later proves [S1] unreachable before unlink.
```

The orphan possibility is an intentional consequence of preparing durable
content before entering the short final gate. It is not dangling selected
truth. Staging/orphan population and cleanup debt must have finite limits,
accounting, and repeat-safe recovery.

## 5. Two publishers with one expected revision

```text
Starting head:
  H:main@r7 =============================> B0 ===> [S0]

Publisher A                                  Publisher B
-----------                                  -----------
admit/reuse B1 for [S1]                      admit/reuse B2 for [S2]
expected (B0,r7)                             expected (B0,r7)
         |                                            |
         +-------------------+    +-------------------+
                             v    v
                           one GATE
                              |
               A enters first in this example
                              |
                reread H == (B0,r7): yes
                atomic H=(B1,r8) replacement  <-- only winning LP
                acknowledge A
                              |
                         B enters next
                              |
                reread H == (B0,r7): no, current=(B1,r8)
                return STALE to B

Final selected head:
  H:main@r8 =============================> B1 ===> [S1]

Required history:
  successful head transitions: 1
  stale outcomes:               1
  merges/rebases:               0
  head overwrites by loser:     0
  possible complete orphan:     [S2]
```

Swapping arrival order may select B instead. It may not produce two successful
replacements for the same expected revision.

## 6. Equal candidates and head OCC are still separate

Even when two publishers submit canonically equal candidates, admission
convergence does not grant both head transitions:

```text
Publisher A candidate Cx                  Publisher B candidate Cx
             |                                         |
             v                                         v
      derive VersionId Sx                          derive VersionId Sx
             |                                         |
             +------------ exact equality -------------+
                              |
                              v
                   one accepted payload [Sx]
                   one accepted binding Bx

Both expected H=(B0,r7)
             |
             v
one head transition may install H=(Bx,r8)
the other sees stale or a documented same-Version/replay outcome

Physical payload convergence does not create two OCC winners.
```

Phase 03 selects the exact same-Version replay/no-op result, while preserving one
linearization point, monotone revision semantics, and no payload work on an
accepted-binding-only retry.

## 7. Collision stops before head mutation

```text
candidate canon(Cbad) -> forced/derived VersionId S1
                                      |
                                      v
                           accepted slot S1 occupied
                                      |
                                      v
                  full canon(Cbad) versus accepted canon(S1)
                                      |
                                   UNEQUAL
                                      |
                                      v
                                 COLLISION

Effects:
  accepted occupant overwritten?   no
  accepted binding issued to Cbad? no
  transition gate/head CAS run?    no
  root/head changed?               no
  silent alias?                    no
```

Length checks, secondary digests, byte samples, or cryptographic probability
cannot replace the full comparison.

## 8. Crash and acknowledgement boundaries

The exact persistent steps are deferred, but the outcome envelope is fixed:

```text
TIME ---------------------------------------------------------------------->

 private      payload accepted      GATE: expected check    head LP    ACK
 staging      complete/durable              |                 |         |
    |                 |                      |                 |         |
    v                 v                      v                 v         v
 [ T ] ...........> [S1]/B1 .............> match? ........> H'=B1 ...> success

Crash before accepted payload:
  prior head + recognizable bounded private staging

Crash after accepted payload, before head LP:
  prior head + complete unreferenced accepted payload

Crash at head replacement:
  prior complete head or complete new head; never torn/mixed accepted truth

Crash after durable head, before response:
  complete new truth may persist; caller resolves explicit unknown/retry by
  head revision and idempotency, never by repeating a merge

Success acknowledgement:
  occurs only after the Phase 03-qualified payload and reference durability
  obligations have completed
```

Unsupported filesystem atomicity/durability behavior fails configuration or
readiness. It does not weaken acknowledgement semantics.

## 9. Focused legacy-versus-V2 conflict behavior

Phase 00 source verification found that the current e497
`publish_validated_changes` path can auto-accept compatible directory creates
and can cleanly three-way-merge eligible text writes. That is measured legacy
behavior, not V2 permission.

```text
CURRENT e497 -- SOURCE-VERIFIED               SELECTED R0 -- ARCHITECTURE DECISION
--------------------------------               ------------------------------------

publisher base becomes stale                 expected (B0,r7) becomes stale
            |                                            |
            v                                            v
eligible conflict class?                     under one GATE, reread head
       /          \                                      |
 compatible      incompatible               current == expected?
     |                |                            /           \
     v                v                          yes            no
may auto-merge/     reject                        |              |
compose eligible                                 v              v
directory/text work                         atomic replace     STALE
                                                                  |
                                                        no merge or rebase
```

V2 application code may construct a fresh candidate in a separately authorized
new request, but storage must not transform a stale publication into success by
silently merging or rebasing it. The old appendix or Stage 4.6 cannot override
this product hard rule.

## 10. Publication results by failure point

| Failure/outcome | Payload state | Head state | Required cleanup/retry behavior |
|---|---|---|---|
| Invalid/over-limit candidate | No accepted new payload | Unchanged | Release reservations/private input |
| Occupied ID, unequal bytes | Existing occupant unchanged; candidate rejected | Unchanged | Typed collision; clean staging |
| Resource/ENOSPC before admission | No accepted new payload | Unchanged | Clean or bounded recognizable private debt |
| Crash during accepted-payload visibility | None or one complete accepted payload | Unchanged | Recovery validates; never accept partial content |
| Payload accepted, expected head stale | Complete reused/new accepted payload; may be orphan | Current winner unchanged | Typed stale; bounded retirement later |
| I/O failure before head LP | Target payload may be accepted | Prior head | No success acknowledgement; bounded metadata cleanup |
| Atomic head replacement succeeds | Complete accepted target | Complete new head | Satisfy reference durability before success |
| Response lost after durable head | Complete accepted target | Complete new head | Explicit unknown/re-resolve by revision; no blind merge/rebase |
| Corrupt/dangling head on recovery | Do not guess | Do not serve ambiguous truth | Fail readiness closed |

## 11. Fixed invariants and deferred mechanics

| Subject | Status |
|---|---|
| Complete canonical identity and typed `VersionId` | `LOCKED_PHASE_01` semantic boundary |
| Full canonical comparison on every occupied ID | `LOCKED_PHASE_01` |
| Payload durable/immutable before reference may name it | `LOCKED_PHASE_01` |
| Admission changes no head by itself | `LOCKED_PHASE_01` |
| One LayerStack-0-owned selected-Version transition gate | `LOCKED_PHASE_01` |
| Complete expected `(binding, revision)` reread under gate | `LOCKED_PHASE_01` |
| Atomic complete head replacement is sole OCC linearization | `LOCKED_PHASE_01` |
| Stale changes no head and never silently merges/rebases | `LOCKED_PHASE_01` |
| Complete unreferenced orphan is bounded cleanup debt | `LOCKED_PHASE_01` |
| Exact canonical codec, digest, ordering, and identity limits | `SELECT_IN_PHASE_02` |
| Exact payload/record spelling, checksums, and completeness markers | `SELECT_IN_PHASE_03` |
| Exact ID-slot coordination and atomic admission primitive | `SELECT_IN_PHASE_03` |
| Exact lock, temporary name, sync/fence/rename sequence, filesystem profile | `SELECT_IN_PHASE_03` |
| Exact finite staging/orphan/recovery limits | `SELECT_IN_PHASE_03` |
| Same-Version retry/no-op revision behavior | `SELECT_IN_PHASE_03` |

No exact hash, codec, hardware CAS, lock-free algorithm, record encoding, or
`fsync` sequence is selected by this diagram.

## 12. Verification mapping

| Diagram claim | Required proof |
|---|---|
| Same facts produce the same ID | Phase 02 I1/I2 golden and permutation tests |
| Occupied ID never trusts digest alone | Phase 02 I5 seam plus Phase 03 F10 forced-collision tests at every ingress |
| Equal concurrent admission creates one payload | Phase 03 F9 physical-count and barrier-controlled histories |
| Stale OCC changes no head | Phase 03 F2 dual-publisher and mixed-operation histories |
| Exactly one head linearization point | Source audit, barrier histories, and fault injection around the selected record replacement |
| Payload precedes reference | Phase 03 C1 crash/fault at every exact selected filesystem step |
| Restart recovers durable head or fails closed | Phase 03 C2 plus corrupt/dangling/unknown-version fixtures |
| Stale loser may leave only bounded orphan debt | Resource accounting, recovery, cancellation, and retirement tests |
| Final gate contains bounded metadata work | Operation instrumentation/source audit; gate wait/hold measurement is sanity evidence |
| No V2 auto-merge/rebase | Source audit and stale directory/text conflict fixtures |
| Exact artifact still satisfies all outcomes | Phase 06 frozen-artifact rerun |

Wall-clock timing cannot prove OCC correctness, collision handling, or crash
durability. Tests need barriers, forced IDs, fault hooks, physical-count/I/O
oracles, restart evidence, and exact artifact provenance.

## 13. Open owner decisions and stable seams

- `DEC-017` may reject sessionless mutation or route it through ordinary
  complete candidate construction and this publish/OCC sequence. It cannot edit
  an accepted Version or bypass OCC.
- `DEC-018` determines the application authorization/revocation cutoff. It does
  not add a second head writer or change the store's expected-head comparison.
- `DEC-001` audit/blame remains outside canonical selected truth and Head OCC.
- `DEC-011` changes migration compatibility deletion timing, not publication
  truth or writer count.

Any owner outcome requiring direct committed mutation, canonical auth/audit
facts, silent stale merge, or joint application/store durable authority would
reopen Phase 01.

## 14. Reopening conditions

Reopen Phase 01 rather than weakening R0 if implementation evidence requires:

- digest-only admission or inability to perform bounded full canonical-byte
  comparison;
- a head naming private, incomplete, or non-durable payload content;
- more than one selected-Version writer, gate, or OCC linearization point;
- candidate/payload work that must occur inside a long authoritative gate
  because the selected owner/storage family cannot separate it safely;
- silent merge/rebase or more than one success for one expected revision;
- recovery outside prior-or-complete-new or fail-closed behavior;
- unbounded staging/orphan/recovery debt;
- runtime-private identity, layer reconstruction, or writable accepted Version;
- a new owner, service, process, database, coordinator, object DAG, archive
  truth, or persistent refcount authority for correctness; or
- a supported deployment filesystem that cannot implement the fixed payload-
  before-reference and atomic-head durability model.

Do not reopen for a safe exact codec/digest, record format, checksum, atomic
filesystem primitive, lock, finite limit, same-Version replay rule, or fence
sequence that preserves the selected points and outcomes.

## References

- [Product PRD](../PRD.md)
- [Phase 00 source evidence and baseline policy](../phases/00-freeze-rules/SPEC.md)
- [Phase 01 selection contract](../phases/01-choose-design/SPEC.md)
- [Selected architecture](../architecture_design.md)
- [Version identity design](../design/02-state-identity.md)
- [LayerStack-0 storage design](../design/03-state-store.md)
- [Algorithms and call flows](../design/04-algorithms-and-call-flows.md)
- [Concurrency, durability, and recovery](../design/05-concurrency-durability-recovery.md)
- [Phase 02 tests](../phases/02-state-identity/test-perf.md)
- [Phase 03 tests](../phases/03-state-store/test-perf.md)
- [Fork, checkpoint, rollback, and logical COW](03-fork-checkpoint-rollback-and-cow.md)
- [Diagrams index and conventions](README.md)
