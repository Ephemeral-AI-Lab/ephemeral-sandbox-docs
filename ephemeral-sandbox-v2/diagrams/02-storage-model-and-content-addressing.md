# LayerStack-0 storage model and content-addressed admission

Date: **2026-08-04**
Status: **`LOCKED_PHASE_01` conceptual storage diagram; exact Phase 02/03
encodings pending**
Evidence base: product source at
`e4974d1f9aac702b35e052629cb070c897989352`

## Authority and purpose

This document visualizes the selected R0 storage family, its logical objects,
conceptual physical roles, and the exact content-addressed admission decision.
It is subordinate to the product [PRD](../PRD.md), selected
[architecture](../architecture_design.md), Phase 02
[identity contract](../design/02-state-identity.md), and Phase 03
[store contract](../design/03-state-store.md).

The diagrams fix semantic separation and required outcomes. They intentionally
do not select Phase 02's exact portable fact profile, canonical codec, digest,
or limits, nor Phase 03's exact directory names, record encodings, checksum,
lock primitive, filesystem profile, or fsync/atomic-replacement sequence.

## Legend

```text
[SOURCE-VERIFIED e497]  Measured current implementation fact at the sealed base
[SELECTED R0]           Binding Phase 01 storage invariant
[DEFERRED P02]          Exact pure identity choice owned by Phase 02
[DEFERRED P03]          Exact durable-store choice owned by Phase 03

  -->                   Data/control flow
  ==>                   Promotion into an accepted durable Version
  ..>                   Read-only, temporary, or non-authoritative relation
  -X->                  Forbidden flow or authority
  { decision? }         Branch whose outcomes are all fixed
  [object]              Logical or conceptual physical role
```

“Content-addressed” here means a candidate `VersionId` is derived from complete
canonical bytes and selects an occupied physical slot. It does **not** mean the
digest proves equality, that raw IDs are accepted capabilities, or that R0 is a
chunk/object DAG.

## Panel A — measured current model versus selected R0 model

```text
+------------------------- SOURCE-VERIFIED e497 --------------------------+
|                                                                         |
|  sandbox-runtime-layerstack owns durable history                        |
|                                                                         |
|      active manifest / refs                                             |
|                 |                                                       |
|                 v                                                       |
|      layer --> parent layer --> ... --> base                            |
|        |             |                    |                              |
|        +---- project / reconstruct -----+                               |
|                 |                                                       |
|                 +---- merge / squash / depth / leases                   |
|                                                                         |
|  This is the measured legacy truth model. It is not accepted V2 truth.  |
+-------------------------------------------------------------------------+

                                  |
                                  | R0 semantic replacement in same owner
                                  v

+---------------------------- SELECTED R0 -------------------------------+
|                                                                         |
|  [head selector] ----+                                                  |
|                      |                                                  |
|  [typed root A] -----+----> [AcceptedBinding X] ----> [payload X]       |
|                      |                              complete             |
|  [typed root B] -----+                              immutable            |
|                                                     closure              |
|                                                                         |
|  payload X has no parent/depth/layer reconstruction dependency.         |
|  roots/heads contain references, not payload bytes.                     |
|                                                                         |
|  [private staging] ==> [accepted payload] ==> [root/head may name it]    |
|       bounded             durable + immutable      small metadata        |
+-------------------------------------------------------------------------+
```

Current LayerStack mechanics are `SOURCE-VERIFIED` placement evidence and
legacy behavior. The complete-payload/root/head model is `SELECTED R0` design
pending executable Phase 02/03 proof.

## Panel B — logical object model

```text
RUNTIME / APPLICATION SIDE                    PURE IDENTITY SIDE

[writable workspace or import view]
                |
                | capture complete portable facts
                | (no host path/mount/namespace identity)
                v
        [UntrustedPortableFacts]
                |
                v
       [ValidatedPortableVersion] ----------> [CanonicalBytes]
                                                    |
                                                    | typed digest over
                                                    | complete byte stream
                                                    v
                                                [VersionId]

STORE SIDE

[VersionId] + [canonical comparison source] + [candidate payload]
                |
                | exact admission
                v
        [AcceptedVersion] --------------------------+
                |                                  |
                |                                  v
                |                           [immutable payload closure]
                |
                v
        [AcceptedBinding] --------------------------+
                |
          +-----+----------------------+--------------------+
          |                            |                    |
          v                            v                    v
 [HeadRecord]                    [RootRecord]          [ReadCustody]
 selector -> binding + revision  kind/id -> binding    runtime-local guard

 [VersionId] -X-> [AcceptedVersion] or [AcceptedBinding] by cast or
                    public constructor
 raw digest -X-> reference-only root/head mutation
 runtime handle -X-> CanonicalBytes or VersionId derivation
```

The identity module proves deterministic bytes and derives a candidate ID. The
store establishes occupancy and exact equality before it issues an
`AcceptedVersion`; reference validation then yields or revalidates an
`AcceptedBinding`. `HeadRevision`, root identity, read custody, and local
payload paths refer to a Version but never contribute to its canonical
identity.

## Panel C — content-addressed admission decision

```text
 [complete bounded portable candidate]
                    |
                    v
 [validate + canonicalize + derive typed VersionId]          [DEFERRED P02 form]
                    |
                    v
 [reserve bounded resources + build private staging]       [SELECTED R0]
                    |
                    v
       { is versions/<VersionId> occupied? }                    conceptual slot
                   / \
                 no   yes
                 /     \
                v       v
       +------------------+       +----------------------------------+
       | EMPTY SLOT       |       | OCCUPIED SLOT                    |
       |                  |       |                                  |
       | finish complete  |       | obtain immutable accepted        |
       | payload + exact  |       | canonical comparison source      |
       | comparison data  |       |              |                   |
       |        |         |       |              v                   |
       |        v         |       | compare FULL canonical bytes     |
       | make durable and |       |        /                 \       |
       | integrity-check  |       |      equal              unequal  |
       |        |         |       |       |                    |     |
       |        v         |       |       v                    v     |
       | atomically expose|       | reuse existing       typed       |
       | one immutable    |       | physical payload     COLLISION   |
       | occupant         |       |       |              no alias    |
       +--------+---------+       |       |              no ref move |
                |                 +-------+--------------------+-----+
                |                         |                    |
                +-----------+-------------+                    |
                            |                                  |
                            v                                  v
                  [AcceptedVersion]                  [cleanup private
                  NewPayload or ReusedPayload         staging or bounded debt]
                            |
                            | validate/reference to form AcceptedBinding;
                            | admission alone never changes a root/head
                            v
                  [AcceptedBinding] --> [caller may separately request
                                         reference publication]
```

The occupied branch must compare the entire canonical byte streams. A matching
digest, length, secondary digest, descriptor, sample, or cryptographic
assumption cannot replace that comparison. Early exit on the first unequal
canonical byte is permitted if validation and corruption handling still fail
safely within the selected limits.

Concurrent candidates obey the same outcomes:

```text
equal canonical candidates, same ID   --> converge on one physical occupant
unequal canonical candidates, same ID --> collision; never two occupants/alias
two publishers, one expected revision --> at most one head transition wins
```

## Panel D — conceptual physical roles

```text
<LayerStack0Root>/                               exact root/name [DEFERRED P03]
|
+-- versions/
|   +-- <VersionId>/                               [accepted Version slot]
|       +-- payload/                               [immutable payload closure]
|       |   +-- complete portable filesystem value
|       +-- canonical descriptor/comparison material as selected
|       +-- version/integrity/completeness data as selected
|
+-- heads/
|   +-- <selector>                               [AcceptedBinding + Revision]
|
+-- roots/
|   +-- <kind>/
|       +-- <root-id>                            [AcceptedBinding]
|
+-- staging/
|   +-- <transaction-id>/                        [private, bounded, unaccepted]
|
+-- control/                                     [store version/generation/
                                                  lock/recovery metadata]

Selected roles: versions, heads, roots, staging, control.
Deferred details: exact spelling, encoding, checksums, markers, temp names,
                  indexes/hints, lock primitive, path-resolution primitive,
                  fsync/link/rename sequence, supported filesystem profile.
```

An exact Phase 03 layout need not use these literal names, but it must preserve
the roles and invariants. Its selected physical root and V2 namespace must not
alias the e497 legacy names `manifest.json`, `workspace.json`, `layers/`,
`staging/`, `.layer-metadata/`, or `base/`; Phase 05 must consume only the
Phase 03 store API and reported layout contract. A bounded index, cache, or
refcount hint may exist only as reconstructible non-authoritative metadata. It
cannot decide truth or permit premature retirement.

## Panel E — shared references and zero payload I/O

```text
                    small durable metadata

 [head main, rev 7] --------+
                            |
 [checkpoint root] ---------+------> [AcceptedBinding X]
                            |                  |
 [branch head agent-42] ----+                  v
                                      +------------------+
                                      | payload X        |
                                      | complete         |
                                      | immutable        |
                                      | one occupant     |
                                      +------------------+

 fixed-checkpoint creation / Branch-Head creation / Head rollback or move:

   validate accepted binding + expected reference metadata
       --> atomically create a fixed Root or conditionally create/replace a Head
       --> selected payload bytes read    = 0
       --> selected payload bytes written = 0
       --> selected payload bytes copied  = 0

 candidate bytes or raw VersionId -X-> this reference-only path
```

This is reference sharing, not filesystem copying and not a promise of
cross-Version block deduplication. Different `VersionId`s may have complete payload
closures containing duplicate unchanged files. Any later physical optimization
must preserve closure independence and cannot introduce hidden layer/DAG truth
without architecture review.

## Panel F — publication order after admission

```text
application                            store
    |                                    |
    | authorize/order                    |
    | capture expected head/revision     |
    |                                    |
    | candidate + expected record ------>|
    |                                    | validate/canonicalize/stage
    |                                    | exact occupancy decision
    |                                    | durable immutable payload
    |                                    |          |
    |                                    |          v
    |                                    | enter one transition gate
    |                                    | reread expected head/revision
    |                                    |    /                 \
    |                                    | stale                match
    |                                    |   |                    |
    |<---------- clean stale ------------|   |                    v
    |                                    |            atomic complete head
    |                                    |            record replacement
    |                                    |                    |
    |<---------- success after selected reference durability -+

  payload durability happens before reference publication.
  head replacement is the sole OCC linearization point.
  stale performs no merge, rebase, or head mutation.
```

The exact persistent micro-steps and acknowledgement behavior around
filesystem errors are `SELECT_IN_PHASE_03`; the ordering and possible outcomes
are `LOCKED_PHASE_01`.

## Walkthrough

1. A runtime owner or temporary importer produces one complete bounded
   candidate in portable facts. Host paths and runtime handles remain outside
   the fact set.
2. The pure Phase 02 module validates those facts, emits deterministic
   canonical bytes, and derives a typed digest over the complete stream.
3. The Phase 03 store reserves bounded private resources and checks the
   conceptual physical slot selected by `VersionId`.
4. If the slot is empty, the store establishes one complete durable immutable
   occupant before issuing an accepted binding.
5. If occupied, the store compares full canonical bytes. Equality reuses the
   occupant; inequality is a typed collision with no alias or reference change.
6. Admission is separate from publication. A complete unreferenced occupant
   after stale OCC is safe bounded orphan debt, not mixed selected truth.
7. Publication rereads the expected head/revision under the one transition
   gate. One atomic record replacement is the OCC point; stale loses cleanly.
8. Roots and heads use only accepted bindings. Moving an existing reference
   never opens or copies the selected payload.
9. Captured reads acquire bounded runtime-local custody for an immutable
   payload; retirement revalidates heads, roots, and active custody before
   unlinking.
10. Recovery validates payload completeness and every durable reference; it
    never guesses truth from staging, filenames, layers, or diagnostic indexes.

## Storage and content-addressing invariants

- One `VersionId` derives from the complete versioned canonical byte stream of
  one qualified portable Version value.
- `VersionId` is an address/index, not equality proof or an accepted capability.
- Every occupied ID invokes complete canonical-byte comparison.
- Equal canonical bytes reuse one physical accepted payload; concurrent equal
  admissions converge on that occupant.
- Unequal canonical bytes at an occupied ID fail closed as collision and
  cannot create an alias, accepted binding, root, or head.
- A payload closure is complete, immutable, integrity-checkable, and durable
  before any reference can name it.
- Roots/heads contain accepted bindings and small metadata, never candidate or
  payload bytes.
- Reference-only operations perform zero selected-payload bytes read, written,
  and copied.
- Publication has one OCC head replacement; stale performs no merge/rebase.
- Accepted payloads are never exposed as writable live workspace custody.
- Heads, typed roots, and active read custody are the authoritative
  reachability sources; persistent refcount truth is not selected.
- Staging and orphan payloads are bounded recognizable debt, not selected
  truth.
- Recovery yields prior truth, complete new truth, or fail-closed diagnostics.
- R0 is not a layer chain, archive-extraction truth, object/chunk DAG,
  database authority, persistent refcount authority, or external service.

## Selected versus deferred

| Subject | Status | Constraint |
|---|---|---|
| Complete immutable payload, accepted binding, roots/heads, staging, one writer/OCC, recovery/retirement family | `LOCKED_PHASE_01` | Phase 03 implements this family in `sandbox-runtime-layerstack`. |
| Portable identity excludes runtime-private facts | `LOCKED_PHASE_01` | Phase 02 must not import host/runtime facts. |
| Full comparison for every occupied ID | `LOCKED_PHASE_01` | No digest-only/probabilistic shortcut. |
| Equal occupant reuse and unequal collision | `LOCKED_PHASE_01` | One physical equal-Version occupant; mismatch changes no reference. |
| Exact portable fact/metadata profile | `SELECT_IN_PHASE_02` | Complete for a qualified product Version; unsupported facts fail closed. |
| Canonical codec, ordering, domain/version, digest algorithm/width | `SELECT_IN_PHASE_02` | Deterministic, unambiguous, bounded, independently reproducible. |
| Exact disk hierarchy and payload/comparison representation | `SELECT_IN_PHASE_03` | Must preserve complete closure, exact comparison, immutability, and one occupancy. |
| Record/checksum/completeness encoding | `SELECT_IN_PHASE_03` | Versioned, integrity-checkable, prior-or-complete-new behavior. |
| Filesystem profile, lock, safe path primitive, fsync/rename/link sequence | `SELECT_IN_PHASE_03` | Unsupported semantics fail readiness; payload durable before references. |
| Read custody, limits, cleanup batches, bounded hints/instrumentation | `SELECT_IN_PHASE_03` | Exact last-root safety, finite populations, non-authoritative diagnostics. |
| Cross-Version file/block deduplication | `NOT SELECTED` | No guarantee; cannot introduce hidden DAG/layer truth as a local optimization. |
| Stage 4.6 performance comparison | `INCOMPARABLE` | No V2 speedup or guarantee is claimed. |

## Verification mapping

| Invariant | Required proof |
|---|---|
| Same facts produce same bytes/ID; input order irrelevant | Phase 02 I1–I2 golden vectors and permutations |
| Corrupt/ambiguous/over-limit facts fail closed | Phase 02 I3–I4 and selected limit boundary cases |
| No runtime-private identity fields | Phase 02 I6 type/source audit |
| Forced occupied ID + unequal bytes rejects | Phase 02 test seam plus Phase 03 F10 across every admission ingress |
| Publish/read round-trip represents one complete Version | Phase 03 F1 and restart/source audits |
| Stale OCC changes no head and exactly one expected revision wins | Phase 03 F2 concurrency histories |
| All five accepted-reference operations perform zero payload I/O | Phase 03 F3–F7 operation counters plus syscall/fixture evidence |
| N Heads/fixed Roots share one accepted physical payload | Phase 03 F9 physical occupancy count |
| No layer-depth truth or reconstruction | Phase 03 F11 source/dependency and read/restart audit |
| Crash/restart produces prior or complete new truth | Phase 03 C1–C2 crash-prefix and corruption/readiness tests |
| Last-root/read race and cleanup stay safe/bounded | Phase 03 C3–C4 custody, cancellation, debt, FD/worker/reservation tests |
| Integrated public paths cannot bypass admission/OCC | Phase 04 wiring audit and Phase 06 offline qualification |

Timing cannot substitute for the byte counters, physical occupancy count,
collision seam, crash histories, or source/dependency audits above.

## Reopening conditions

Stop implementation and reopen Phase 01 if evidence shows R0 cannot provide:

- complete qualified Version without layer/parent reconstruction or
  runtime-private identity;
- bounded deterministic canonicalization and full occupied-ID byte comparison;
- one physical occupant for equal accepted canonical Versions;
- reference-only operations with selected payload bytes read/written/copied
  all zero;
- durable immutable payload-before-reference publication and one OCC point on
  a supported filesystem;
- captured reads and race-safe bounded last-root retirement;
- bounded staging/orphan/recovery debt and fail-closed corruption handling;
- one writable migration truth in the existing owner; or
- the design without a newly necessary crate, service, process, database,
  coordinator, different writer authority, or different storage family.

Do not reopen for a compatible exact codec/digest, directory spelling, record
encoding, checksum, finite constant, read-custody representation, or safe
filesystem fence sequence selected and proved by its owning phase.

## Links

- [Product PRD and hard rules](../PRD.md#hard-rules-must-never-break)
- [Selected architecture](../architecture_design.md)
- [Phase 00 current-source evidence](../phases/00-freeze-rules/SPEC.md)
- [Phase 01 selection contract](../phases/01-choose-design/SPEC.md)
- [R0 Version identity](../design/02-state-identity.md)
- [LayerStack-0 storage](../design/03-state-store.md)
- [Algorithms and call flows](../design/04-algorithms-and-call-flows.md)
- [Concurrency, durability, and recovery](../design/05-concurrency-durability-recovery.md)
- [Resources, security, and observability](../design/06-resources-security-observability.md)
- [Performance and optimization](../design/07-performance-and-optimization.md)
- [Verification matrix](../design/10-verification-matrix.md)
