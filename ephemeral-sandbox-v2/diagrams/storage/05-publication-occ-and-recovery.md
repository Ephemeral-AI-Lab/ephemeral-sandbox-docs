# Publication, strict OCC, and recovery

**Status:** selected R0 publication/recovery semantics; implementation proof is
`NOT_RUN`

**Authority:** [V2 PRD](../../PRD.md) -> approved Phase 01
[input and selection contract](../../phases/01-choose-design/SPEC.md) -> selected
Phase 01 [architecture output](../../architecture_design.md)

**Purpose:** follow private upperdir changes through a complete portable
Workspace candidate, identity/admission, durable payload placement, and the one
strict OCC Branch transition; then classify every conceptual crash outcome and
its bounded cleanup obligation.

The selected R0 physical truth is a filesystem-native complete immutable
payload closure per Accepted Version at an occupied `VersionId`. A CDC/chunk content-addressed storage
placement is shown only as a **PROPOSED** alternative. It was not selected by
Phase 01 and cannot replace the R0 placement without reopening Phase 01.

## Question answered

How does an agent publish isolated Workspace changes so that another publisher
cannot be silently overwritten, a digest collision cannot alias different
bytes, and restart exposes either the prior complete Branch value or the
complete new value?

```text
 [private upperdir changes]
             |
             v
 [complete portable Workspace Candidate]
             |
             v
 [validate + canonicalize + typed VersionId]
             |
             v
 [durable immutable accepted Version]
             |
             v
 [strict OCC Branch/Head transition]  <=== sole publication linearization
```

The input is a **Candidate**, not a Version, until identity validation,
occupied-ID comparison, and durable LayerStack-0 admission have succeeded.

## Legend

```text
[RUNTIME]     runtime-private effect or mutable Workspace artifact
[PRIVATE]     operation-private candidate/staging; never selectable
[DURABLE]     durable accepted Version or complete authoritative record
[BRANCH]      product-facing mutable reference backed by a revisioned Head
---->         ordinary data/control flow
===>          durable authoritative transition
-X->          rejected transition; selected Branch is unchanged
- - ->        cleanup/diagnostic path; never selected-Version authority

OCC           optimistic concurrency control over expected Branch binding and
              revision; this document does not use bare "CAS" for OCC
CDC/CAS       content-defined chunking plus chunk content-addressed storage;
              PROPOSED physical placement only, not selected R0
```

## Ownership boundary

```text
 APPLICATION / DAEMON OWNERS                  SELECTED STORE OWNER
                                               sandbox-runtime-layerstack
 +------------------------------+              (rewritten in place)
 | authenticate / authorize     |                           |
 | order request and revoke     |                           |
 | resolve expected Branch rev  |---- publish request ----->|
 | choose product response      |                           |
 +------------------------------+                           |
                                                            |
 RUNTIME-EFFECT OWNERS                                      |
                                                            |
 +------------------------------+                           |
 | Workspace / OverlayFS /      |-- complete portable ----->|
 | namespace / exec custody     |   candidate input         |
 | private upperdir changes     |                           |
 +------------------------------+                           |
                                                            v
                                                +------------------------+
                                                | identity + store       |
                                                | admission + one writer |
                                                | durable OCC transition |
                                                +------------------------+
```

The application owns policy and orchestration. Runtime packages own mounts and
mutable effects. Neither may write accepted payloads or authoritative
Branch/Head records independently. MCTS/rollout policy remains above this
boundary and cannot enter portable identity or storage admission.

## End-to-end selected publication flow

```text
 RUNTIME WORKSPACE W17

 immutable projected base V3
          +
 private upperdir changes
          |
          | runtime owner resolves directory structure, files, symlinks,
          | metadata, deletions, and policy-relevant portable facts
          v
 [PRIVATE complete portable Workspace Candidate C4]
          |
          | pure identity boundary (exact grammar selected in Phase 02)
          |   validate finite limits and portable facts
          |   canonicalize complete Candidate
          |   derive typed VersionId S4
          v
 [PRIVATE canonical bytes + S4]
          |
          | selected R0 admission in one store owner
          |   inspect S4 occupancy
          |   compare full canonical bytes when occupied
          |   stage one complete payload closure when new
          |   make the accepted binding durable and immutable
          v
 [DURABLE accepted Version binding B4 = (S4, store proof)]
          |
          | enter short transition gate only after candidate admission
          | reread Branch agent-a
          | expected = (B3, revision 12)
          v
    +-----------------------+
    | expected still exact? |
    +----------+------------+
               |
          +----+----+
          |         |
         no        yes
          |         |
          v         v
 stale OCC      durably replace complete Branch/Head record
 reject         (B3, r12) ===> (B4, r13)
          |                        ^
          |                        |
          |                        +--- sole publication linearization point
          v
 Branch remains (Bcurrent, rcurrent)
 B4 may be an accepted unrooted payload; bounded retirement handles it
```

The transition never performs a silent merge, text merge, directory merge,
rebase, or retry against a newly observed revision. The caller may make a new
explicit request after re-reading current state; the failed request itself
does not change meaning.

## Physical placement: selected R0 versus proposed CDC plus Chunk storage

The logical invariant is one complete portable Version per `VersionId`. The
physical model is not interchangeable without an architecture decision.

```text
                         complete canonical Candidate C4 / VersionId S4
                                           |
                +--------------------------+--------------------------+
                |                                                     |
                v                                                     v
 SELECTED R0 PLACEMENT                                  PROPOSED CDC/CAS PLACEMENT

 +----------------------------------+                   +--------------------------+
 | versions/S4/                     |                   | manifests/S4             |
 |   complete immutable filesystem  |                   | complete Workspace map:  |
 |   payload closure                |                   | path -> chunk refs/meta   |
 |   no parent/layer reconstruction |                   +------------+-------------+
 +----------------+-----------------+                                |
                  |                                                  v
                  |                                      +--------------------------+
                  |                                      | chunks/<chunk-id>        |
                  |                                      | CDC chunk content-       |
                  |                                      | addressed storage        |
                  |                                      +--------------------------+
                  |                                                  |
                  v                                                  v
       accepted binding B4                                accepted binding B4
       then strict OCC Head move                          then strict OCC Head move

       LOCKED CURRENT FAMILY                              NOT SELECTED
                                                         requires Phase 01 reopen,
                                                         backend/read contract, GC,
                                                         crash protocol, resource
                                                         proof, and new cost case
```

Even the proposed manifest would have to describe a complete Workspace
Version, not a parent/delta chain. But that logical compatibility is not enough
to adopt it: Chunk admission, manifest/Chunk crash ordering, backend-neutral
reads, runtime activation/materialization, garbage collection,
file-descriptor/memory bounds, and migration all add architecture-changing
obligations. This chapter makes no performance claim for that proposal.

## Occupied VersionId and collision handling

A digest lookup alone never proves equality.

```text
 candidate canonical bytes C
 typed VersionId S = identity(C)
              |
              v
      is S already occupied?
           /          \
         no            yes
         |              |
         |              v
         |       read/compare the complete canonical bytes
         |              |
         |        +-----+------+
         |        |            |
         |      equal       different
         |        |            |
         v        v            v
 stage one     reuse the      COLLISION
 complete      one physical   reject candidate -X-> no reference mutation
 payload       payload
         |        |
         +----+---+
              v
        accepted binding
```

Required outcomes:

1. Equal full canonical bytes at the same occupied `VersionId` reuse exactly
   one physical accepted payload.
2. Different full canonical bytes under an occupied `VersionId` are a collision,
   not an alternate Version, branch, or overwrite.
3. Collision rejection occurs before the Branch transition and leaves all
   roots/Heads unchanged.
4. Full-byte comparison responsibility spans Phase 02 identity representation
   and Phase 03 admission. Neither phase may replace it with digest equality.
5. Exact codec, digest family, byte stream, and comparison implementation are
   deferred to Phase 02/03; the outcomes above are not deferred.

## Two concurrent publishers

Both publishers may prepare durable candidates concurrently. The short store
transition gate serializes only the authoritative Branch/Head replacement.

```text
 publisher A                     Branch agent-a                 publisher B
 -----------                     --------------                 -----------
 capture expected (B3, r12)      (B3, r12)                     capture expected (B3, r12)
 admit durable B4                                              admit durable B5
        |                              |                              |
        | transition expected B3/r12   |                              |
        +----------------------------->|                              |
        |                              ===> (B4, r13)                 |
        |<---------------- success     |                              |
        |                              | expected B3/r12 transition   |
        |                              |<-----------------------------+
        |                              | actual B4/r13                 |
        |                              +----------------------------->|
        |                              |                    stale OCC reject

 legal result:
   Branch = (B4, r13)
   B5 is accepted but unrooted until bounded cleanup/retirement

 illegal result:
   automatic merge(B4, B5), rebase B5 on B4, last-writer-wins overwrite,
   or retrying B with expected B4/r13 without a new caller decision
```

Candidate preparation may be expensive; the final transition gate must remain
short and bounded. Resource admission must cap concurrent staging bytes,
memory, descriptors, workers, and recovery debt before work begins.

## Durability order and the fixed crash envelope

The exact marker names, checksum records, temporary directory names,
`fsync`/rename calls, and platform-specific sequence are Phase 03 work. The
ordering relation is already selected:

```text
 1. operation-private candidate/staging
              |
              v
 2. validate identity and occupied-ID full-byte equality
              |
              v
 3. make complete accepted payload + binding durable and immutable
              |
              v
 4. enter transition gate; reread and validate expected Branch revision
              |
              v
 5. durably replace one complete Branch/Head record  <=== linearization
              |
              v
 6. release gate; report result; schedule bounded cleanup when needed

 forbidden ordering:
   Branch/Head names private, incomplete, missing, or merely staged payload
```

Phase 03 must declare a supported filesystem profile and prove that every
tested crash prefix exposes either the prior complete Branch record or the
complete new Branch record. Unsupported atomic-replace or durability behavior
fails closed; it is not papered over with a best-effort repair.

## Conceptual recovery-state classification

These labels describe semantic classes, not selected filenames or on-disk
markers.

```text
 +----------------------+  validate/admit  +--------------------------+
 | PRIVATE_INCOMPLETE   | ---------------->| PRIVATE_COMPLETE         |
 | untrusted staging    |                  | validated, not authority |
 +----------+-----------+                  +------------+-------------+
            |                                           |
            | crash                                     | payload durable
            v                                           v
 bounded remove or                           +--------------------------+
 quarantine                                 | PAYLOAD_DURABLE_UNSELECTED|
                                            | accepted, no Branch Head  |
                                            +------------+-------------+
                                                         |
                                                         | OCC Head replacement
                                                         v
                                            +--------------------------+
                                            | REFERENCE_DURABLE        |
                                            | complete Branch -> payload|
                                            +------------+-------------+
                                                         |
                                                         v
                                            +--------------------------+
                                            | CLEANUP_COMPLETE         |
                                            | no operation-private debt |
                                            +--------------------------+

 Any class whose bytes/records cannot be authenticated as one of these
 recognizable states is CORRUPT_OR_AMBIGUOUS and prevents readiness.
```

`PAYLOAD_DURABLE_UNSELECTED` is not partial selected truth. It is a complete
accepted but unrooted Version, possible after stale OCC or a crash before Head
replacement. It is subject to bounded recovery/retirement and must never be
guessed into a Branch based on timestamps or names.

## Failure and cleanup matrix

| Failure point or observation | Legal selected truth after recovery | Cleanup obligation | Fail-closed condition |
|---|---|---|---|
| Validation or private staging fails | Prior Branch only | Remove/quarantine recognizable private artifacts within limits | Unknown artifact can influence authority, or debt exceeds limits |
| ENOSPC/I/O error before accepted payload is durable | Prior Branch only | Bound and remove incomplete private staging | Incomplete bytes appear accepted or referenced |
| Crash after complete payload is durable, before OCC | Prior Branch Head only; new Version may be accepted/unreferenced | Retain safely or retire after exact fixed-Root/Head/custody revalidation | Recovery guesses the unreferenced Version should be selected |
| OCC expected value is stale | Current winning Branch Head only | Treat candidate as accepted/unreferenced; bounded retirement if no accepted reference | Silent merge/rebase/retry or mutation of current Branch |
| Crash during Branch record replacement | Either prior complete Branch or complete new Branch | Validate complete record and bounded protocol debt | Torn, ambiguous, dangling, or unparseable authoritative record |
| Crash after durable Branch transition but before response | Complete new Branch | Caller re-resolves exact Branch/revision; no blind replay | Reporting/repair assumes failure and overwrites newer truth |
| Occupied-ID bytes differ | Branch unchanged | Preserve collision evidence within bounded diagnostics policy | Reuse, overwrite, truncate, or compare only the digest |
| Payload appears writable after acceptance | Never legal | Quarantine/report exact evidence | Service must not become ready with mutable accepted truth |
| Retirement sees last root disappear while reader has custody | Payload remains available to reader | Defer; revalidate after custody release | Unlink before custody-safe revalidation |
| Recovery work/items/bytes exceed configured ceiling | No guessed readiness | Report exact exhausted limit and stop | Unbounded scan or best-effort continuation |

Observability may expose each class, counter, reason, and cleanup outcome. It is
a diagnostic reader, not selected-Version authority and not an independent
repair writer.

## Failure cleanup flow

```text
 startup / explicit recovery
             |
             v
 establish finite item / byte / work / time ceilings
             |
             v
 enumerate authoritative fixed Roots + Branch Heads + accepted bindings
 and only recognizable private/staging/retirement artifacts
             |
             v
 validate complete records, binding targets, canonical-byte equality,
 immutability, and lifecycle relations
             |
       +-----+-------------------+
       |                         |
       v                         v
 bounded + recognizable         corrupt / dangling / ambiguous /
 crash prefix                   unknown / excessive debt
       |                         |
       v                         v
 finish safe prefix,            quarantine/report exact evidence
 remove private debris,         and FAIL CLOSED
 or retain prior truth          service NOT READY
       |
       v
 exact invariant recheck ===> READY
```

Recovery does not scan arbitrary host paths and infer a Branch from whichever
payload looks newest. It cannot merge or rebase candidates, accept a dangling
reference, or delete an accepted payload still reachable through a root, Head,
or supported reader custody.

## Open product-decision seams

The publication/storage family supports the remaining product-owner outcomes
without selecting them silently.

| Open decision | Isolated storage seam |
|---|---|
| `DEC-001` — `file_blame` V2 semantics | Audit/provenance may consume accepted publication facts but cannot become identity or selected-Version authority |
| `DEC-011` — cutover observation window | Changes migration/retirement timing, not the single-writer publish or OCC mechanism |
| `DEC-017` — sessionless write/edit and exact V2 file target/API, including `file_list` | App layer must either supply an authorized Workspace candidate or reject/adapt the request; it cannot mutate an accepted payload or bypass OCC |
| `DEC-018` — auth/revoke race ordering | App layer decides authorization cutoff; any admitted publish still requires the same exact OCC transition |

Checkpoint-current-Workspace composition and public fork/checkpoint/rollback
naming remain Phase 04/API work as explained in
[branches, checkpoints, fork, and rollback](03-branches-checkpoints-and-rollback.md).

## Selected outcomes, deferred mechanics, and proposals

| Topic | Status | Boundary |
|---|---|---|
| Complete immutable Version is truth | **SELECTED R0** | No layer-depth reconstruction, mutable accepted payload, or parent-chain truth |
| Filesystem-native complete payload closure | **SELECTED R0 family** | One physical payload per equal canonical bytes/VersionId |
| Full-byte occupied-ID collision check | **SELECTED outcome** | Exact codec/comparison mechanics deferred to Phase 02/03 |
| Payload durable before reference | **SELECTED outcome** | Head never names private or incomplete bytes |
| One strict OCC Branch/Head transition | **SELECTED outcome** | Sole publication linearization; no silent merge/rebase |
| Prior-or-complete-new recovery | **SELECTED outcome** | Corrupt/dangling/ambiguous states fail closed |
| Bounded staging, cleanup, custody, and recovery | **SELECTED requirement** | Finite constants and exact representation deferred to Phase 03 |
| Exact canonical codec/hash/validation grammar | **DEFERRED PHASE 02** | Must preserve portability, typed identity, collision comparison, and finite limits |
| Exact layout, records, checksums, locks, markers, sync/rename sequence | **DEFERRED PHASE 03** | Must prove the selected crash envelope on a declared filesystem profile |
| CDC/Chunk content-addressed storage placement | **PROPOSED, NOT SELECTED** | Requires Phase 01 reopening and complete backend-read/runtime-adapter/GC/recovery proof |
| Backend-neutral durable and Workspace contracts | **PROPOSED, NOT SELECTED** | Correctness cannot depend on a custom filesystem, clone feature, or one durable substrate |

## Verification mapping

| Claim | Evidence now | Later proof owner |
|---|---|---|
| Existing owners can place identity/store code in the rewritten LayerStack home | `SOURCE-VERIFIED` placement plus Phase 01 selection | Phase 02/03 implementation and dependency checks |
| Complete candidate can be admitted before a short Head transition | `INFERRED` implementable under R0 | Phase 03 deterministic publish tests |
| Equal full bytes reuse and mismatching occupied ID rejects | `INFERRED` required outcome | Phase 02 vectors and Phase 03 injected-collision test |
| Two publishers have one OCC winner without merge/rebase | `INFERRED` required outcome; mechanics deferred | Phase 03 concurrent history tests |
| Crash exposes prior or complete new Branch plus bounded debt | `INFERRED` from selected family | Phase 03 crash-point matrix on declared filesystem profile |
| Recovery fails closed on corrupt/dangling/ambiguous/excessive state | `INFERRED` required outcome | Phase 03 corruption and resource fixtures |
| CDC/Chunk placement is faster or smaller than selected R0/e497 | `OPEN`; not claimed and not selection evidence | Requires a separately admitted design and comparable benchmark methodology |

No scratch spike was needed to draw the selected semantic flow. No benchmark
winner is claimed. Historical Stage 4.6 results remain `INCOMPARABLE`.

## Reopening conditions

Reopen Phase 01 if implementation evidence shows that:

- the durable owner cannot admit complete immutable payloads and perform the
  one Head transition within the rewritten existing package;
- safe publication requires a database, service, registry, helper process, or
  second selected-Version writer;
- selected reads require parent/layer reconstruction or mutable accepted
  payloads;
- the supported filesystem cannot prove prior-or-complete-new publication and
  no coherent in-place filesystem-native mechanism satisfies the rules;
- recovery must guess authority or perform unbounded work before readiness; or
- CDC/Chunk physical truth or the backend-neutral durable/runtime contracts
  become required for the product rather than remaining a proposal.

## Related documents

- [Architecture design](../../architecture_design.md)
- [LayerStack-0 Version-storage design](../../design/03-state-store.md)
- [Algorithms and call flows](../../design/04-algorithms-and-call-flows.md)
- [Concurrency, durability, and recovery](../../design/05-concurrency-durability-recovery.md)
- [Branches, checkpoints, fork, and rollback](03-branches-checkpoints-and-rollback.md)
- [Proposed backend abstraction and runtime isolation](04-ephcow-runtime-view.md)
- [CDC boundaries, resynchronization, and reuse](08-cdc-boundaries-resynchronization-and-reuse.md)
- [Existing publish/OCC view](../04-publish-occ-and-head-cas.md)
- [Read lifetime, recovery, and retirement](../06-read-lifetime-recovery-and-retirement.md)
- [Phase 00 source facts](../../phases/00-freeze-rules/SPEC.md)
