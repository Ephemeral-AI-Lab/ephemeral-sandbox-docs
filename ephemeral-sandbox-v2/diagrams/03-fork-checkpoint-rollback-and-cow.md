# R0 fork, checkpoint, rollback, and logical COW

**Status:** selected Phase 01 semantics; Phase 03 implementation and executable
proof are `NOT_RUN`
**Architecture:** [R0 LayerStack-0 Version storage](../architecture_design.md)
**Primary proof owners:** Phase 03, then Phase 06 qualification

## Authority and purpose

This document visualizes hard rules 1–4 and 6 for the selected R0 architecture:
complete immutable accepted Versions, one physical payload for an equal
accepted Version, metadata-only reference lifecycle, exact collision handling, and no
in-place mutation of committed content.

It is subordinate to the product [PRD](../PRD.md), the Phase 01
[selection contract](../phases/01-choose-design/SPEC.md), and the selected
[architecture design](../architecture_design.md). The detailed
[identity](../design/02-state-identity.md),
[store](../design/03-state-store.md), and
[algorithm](../design/04-algorithms-and-call-flows.md) contracts define the
normative behavior when a visual is abbreviated.

The diagrams describe selected semantics, not an implemented or measured
result. Stage 4.6 remains `INCOMPARABLE` and provides no COW performance proof.

## Legend

```text
[Sx]       one complete immutable accepted payload closure
(binding)  LayerStack-0-issued/revalidated AcceptedBinding for [Sx]
H:name     mutable head record: accepted binding + HeadRevision
R:type/id  typed durable root record naming an accepted binding
W:name     writable runtime-owned workspace/candidate; never accepted truth
---->      authoritative reference or call
....>      temporary/runtime-only derivation; not portable selected truth
===        one physical accepted payload shared by references
X          forbidden path or failed transition

Payload I/O counters are operation-scoped:
  R = selected immutable payload bytes read
  W = selected immutable payload bytes written
  C = selected immutable payload bytes copied

Candidate bytes consumed, canonical bytes compared, and private staging bytes
are accounted separately on admission paths.
```

## 1. The selected meaning of COW

R0 uses **reference-level copy-on-write over complete Versions**:

```text
                   one physical accepted payload
                              |
                              v
                        +-----------+
                        |   [S0]    |
                        | complete  |
                        | immutable |
                        +-----------+
                          ^    ^    ^
                          |    |    |
                 +--------+    |    +---------+
                 |             |              |
          H:main@r7       R:checkpoint/c1   H:agent-b@r1
          -> binding(S0)  -> binding(S0)    -> binding(S0)

Physical accepted payload count for S0: 1
Number of durable references to S0:      3
Reference operation payload I/O:        R=0, W=0, C=0
```

The “copy” is avoided because the five accepted-reference lifecycle operations
act only on small `AcceptedBinding` reference metadata. Checkpoint creation
installs a fixed typed Root; fork creation installs a new Branch Head;
rollback and a same-Version publication use exact Head OCC. None creates a
second private payload for the same Version or opens the existing payload.

This is not a selection of a lower-level block/file sharing technique:

| Technique or interpretation | R0 status |
|---|---|
| Multiple roots/heads name one already accepted complete payload | **Selected and required** |
| Payload bytes read/written/copied during a reference-only move | **Required to be `0/0/0`** |
| Filesystem-specific cloning or block-level COW | Not selected or required |
| Hard-link construction between different Versions | Not selected or required |
| Chunk/blob object DAG across different Versions | Not selected; would change the storage family if made truth |
| Custom lazy filesystem | Not selected or required |
| Archive extraction presented as “COW” | Not selected; normal R0 payload is a complete filesystem closure |
| Cross-Version sharing of unchanged files/blocks between different `VersionId`s | No R0 guarantee |

R0 guarantees one physical payload for the **same accepted canonical Version**.
It does not claim that two different Versions which share most files occupy only
their byte-level difference.

## 2. Focused current-to-V2 truth comparison

The e497 source inventory verifies a current LayerStack chain/history model.
It does not verify current public checkpoint, fork, or rollback operations;
Phase 00 explicitly found no such named public operations. Therefore this
comparison is limited to the supported change in durable truth model:

```text
CURRENT e497 -- SOURCE-VERIFIED               SELECTED R0 -- ARCHITECTURE DECISION
--------------------------------               ------------------------------------

  [base layer]                                  H:main@r7
       |                                           |
       v                                           v
  [layer 1]                                     binding(S0)
       |                                           |
       v                                           v
  [layer 2 / head]                              [S0 complete]

Read truth may depend on parent/depth.      Read truth needs no parent/depth.
Squash/merge maintains layer history.       No squash/layer reconstruction.

No claim is made here about how a           V2 checkpoint/fork/rollback-to-
nonexistent current fork API would copy.    existing is a metadata reference.
```

Legacy behavior is evidence, not V2 semantics. This diagram does not convert
the old appendix’s proposed operations into measured current product facts.

## 3. Reference-only checkpoint

Checkpointing an already accepted Version creates a fixed typed durable Root.
It never changes an existing Root:

```text
Before
------

  H:main@r7 -----------------------> binding(S0) ===> [S0]

Operation
---------

  CreateFixedRootIfAbsent(root_identity=R:checkpoint/c1,
                          root_kind=Checkpoint,
                          expected=Expected::Absent,
                          binding=binding(S0))
                 |
                 v
       validate bounded reference metadata
       under the selected-Version transition gate
                 |
                 v
       atomically install one small root record
                 |
                 v
       assert payload I/O R=0, W=0, C=0

After
-----

  H:main@r7 -----------------------> binding(S0) ===> [S0]
                                                          ^
  R:checkpoint/c1 -----------------> binding(S0) ----------+

Accepted payload count for S0 remains 1.
```

The input must be a LayerStack-0-accepted binding. A Candidate or raw `VersionId`
cannot enter this path because LayerStack-0 would then be unable to prove that the
ID has passed full occupied-ID equality comparison.

## 4. Reference-only fork

A fork creates a new independently movable Branch Head to the same accepted
Version:

```text
Before fork
-----------

  H:main@r7 ------------> binding(S0) ===> [S0]

Fork transition (metadata only)
-------------------------------

  CreateHeadIfAbsent(H:agent-b, Expected::Absent, binding(S0))
       |
       +----> validate accepted-binding metadata
       +----> one atomic complete Head-record creation
       `----> payload counters R=0, W=0, C=0

After fork
----------

  H:main@r7 ------------> binding(S0) ===> [S0]
                                                   ^
  H:agent-b@r1 ----------> binding(S0) -------------+

No payload was read to “verify the fork.”
No payload was copied to create the fork.
No new private payload exists for S0.
```

The fork primitive contains no MCTS or rollout policy. An application may
decide why to create the Branch, but storage only performs the typed Head
creation. Later Branch movement uses exact `ReplaceHead`; it never retargets a
Root.

## 5. Write after fork: new Candidate, new complete Version

Logical COW does not mean an accepted payload becomes writable. A write after
fork goes through runtime-owned writable custody and normal candidate
admission/publication:

```text
STEP 0 — shared immutable starting point
----------------------------------------

  H:main@r7 ---------> binding(S0) ===> [S0 complete, immutable]
                                               ^
  H:agent-b@r1 -----> binding(S0) -------------+


STEP 1 — runtime owner creates writable candidate custody
---------------------------------------------------------

  H:agent-b@r1 -----> binding(S0) ===> [S0 immutable]
                                               |
                                               | read-only base/materialization
                                               | (runtime-private detail)
                                               v
                                         W:agent-b
                                         writable workspace

  W:agent-b contains runtime-private path/mount/session facts.
  Those facts do not enter VersionId.


STEP 2 — write/edit changes only the workspace candidate
--------------------------------------------------------

  [S0 immutable]                  W:agent-b
       |                          +--------------------+
       |                          | portable facts of  |
       X  no in-place write       | Candidate S1         |
                                  +--------------------+


STEP 3 — normal complete candidate admission
--------------------------------------------

  W:agent-b portable complete facts
       |
       v
  validate + canonicalize + derive VersionId S1
       |
       v
  occupied S1? -- yes --> full canonical-byte compare
       |                         | equal: reuse binding(S1)
       no                        ` unequal: collision, fail closed
       |
       v
  bounded staging -> complete durable immutable [S1]

  This is candidate-bearing work. Payload I/O is expected and bounded;
  the reference-only 0/0/0 rule does not apply to admitting S1.


STEP 4 — conditionally replace the Branch Head with accepted S1
----------------------------------------------------------------

  Before branch move                         After branch move

  H:main@r7 -----> [S0]                      H:main@r7 -----> [S0]
  H:agent-b@r1 --> [S0]       ReplaceHead under one GATE     H:agent-b@r2 --> [S1]
                              + Expected::Exact(r1) -------->

  [S0] remains complete and immutable.        [S1] is a second complete
  Existing Checkpoint/main references           immutable accepted Version.
  still observe S0.
```

The depicted operation is the ordinary Branch-Head OCC transition using
`binding(S1)` plus the exact complete expected Head. Stale OCC leaves H:agent-b
at S0 while S1 remains complete accepted orphan debt until rooted or safely
retired. There is no alternate Root-movement call flow, storage shortcut that
edits S0, or record of “only the delta from S0” as V2 truth.

## 6. Rollback to an existing accepted Version

Assume the selected head advanced from S0 to S1 while a checkpoint retains S0:

```text
Before rollback
---------------

  H:main@r8 -----------------------> binding(S1) ===> [S1]
  R:checkpoint/c1 -----------------> binding(S0) ===> [S0]

Rollback-to-existing input
--------------------------

  selector       = H:main
  expected       = (binding(S1), revision r8)
  target         = binding(S0)       # already store accepted

                 bounded metadata only
                          |
                          v
              +-------------------------+
              | transition gate         |
              | re-read H:main@r8       |
              | expected matches        |
              | replace complete record |  <-- one reference linearization
              +-------------------------+
                          |
                          v
              payload I/O R=0, W=0, C=0

After rollback
--------------

  H:main@r9 -----------------------> binding(S0) ===> [S0]
  R:checkpoint/c1 -----------------> binding(S0) -----^

  [S1] may remain reachable elsewhere or become bounded retirement work.
```

Rollback does not reconstruct S0, reverse S1, follow a parent, copy checkpoint
content, or silently merge changes. If the expected head is stale, the rollback
fails cleanly and changes no head.

## 7. Same-Version Head outcomes

A Head replacement that already targets the requested accepted binding still
uses exact OCC. Fixed Roots have no same-Version move; creation against an
occupied identity returns `ALREADY_EXISTS` only when the exact required record
already exists, otherwise `CONFLICT`:

```text
  expected metadata + binding(S0)
             |
             v
  defined Phase 03 same-Version result
    - monotone revision transition, or
    - explicit no-op result

  In either allowed case:
    payload opened?        no
    payload bytes read?    0
    payload bytes written? 0
    payload bytes copied?  0
```

Phase 03 may choose the exact revision/no-op result, but it must document replay
semantics, preserve OCC monotonicity, and never admit payload as a side effect.

## 8. Reader and last-root safety

Reference sharing is safe only if retirement cannot unlink a Version still being
read:

```text
Read path                                  Retirement path
---------                                  ---------------

resolve root/head
      |                                    precheck reachability
      v                                             |
acquire bounded custody                              v
serialized against final retirement  <---->  transition authority
      |                                             |
      v                                             v
read captured immutable [S0]                 exact final revalidation
      |                                      of heads + roots + custody
      v                                             |
release custody                       rooted/custodied? -- yes --> retain
                                                    |
                                                    no
                                                    v
                                              unlink accepted payload
```

The race has a defined winner: custody/root becomes visible and retirement
retains, or retirement completes first and a later capture/root operation
fails or retries cleanly. A durable root must never name an absent payload.

## 9. Fixed invariants and deferred mechanics

| Subject | Status |
|---|---|
| Complete immutable payload per accepted Version | `LOCKED_PHASE_01` |
| Roots/heads name accepted bindings only | `LOCKED_PHASE_01` |
| Head create/replace/remove and fixed typed Root create/remove payload I/O `0/0/0` | `LOCKED_PHASE_01` |
| One physical payload for equal canonical bytes at an occupied `VersionId` | `LOCKED_PHASE_01` |
| Full canonical comparison on occupied ID | `LOCKED_PHASE_01` |
| Writable work occurs outside committed payload custody | `LOCKED_PHASE_01` |
| MCTS/rollout policy outside storage | `LOCKED_PHASE_01` |
| Exact canonical codec, digest, and limits | `SELECT_IN_PHASE_02` |
| Exact reference record format and atomic filesystem primitive | `SELECT_IN_PHASE_03` |
| Exact read-custody representation | `SELECT_IN_PHASE_03` |
| Same-Version revision/no-op result | `SELECT_IN_PHASE_03` |
| Filesystem-specific clone, block COW, hard-link, custom filesystem, or chunk/DAG mechanism | Not selected or required |

## 10. Verification mapping

| Claim in the diagrams | Required executable evidence |
|---|---|
| Fork performs no payload work | Phase 03 F3: operation counters plus independent syscall/fixture evidence |
| Checkpoint performs no payload work | Phase 03 F6: counters plus independent evidence |
| Rollback-to-existing performs no payload work | Phase 03 F4: counters plus independent evidence |
| Head and fixed-Root removals perform no payload work and preserve retirement safety | Phase 03 F5 and F7 plus C3 exact-removal/retirement races |
| N Heads/fixed Roots share one physical payload | Phase 03 F9: sequential/concurrent reference creation and physical-count assertion |
| Collision never aliases | Phase 02 forced-ID seam plus Phase 03 F10 at every candidate ingress |
| Committed S0 is not mutated by write-after-fork | Mutation-attempt and workspace/public wiring tests in Phases 03–04 |
| Captured reader survives root/head move | Barrier-controlled capture/move history |
| Last root/read race is safe and bounded | Phase 03 C3 plus exact custody/reachability accounting |
| Integrated operations preserve the model | Phase 06 rerun on the exact frozen artifact |

Timing alone cannot prove payload I/O zeros. Store counters must cover every
helper in the operation scope and be cross-checked with an independent
syscall/fixture or physical-effect oracle.

## 11. Reopening conditions

Reopen Phase 01 instead of weakening this design if evidence requires:

- copying, reading, hashing, walking, extracting, or staging payload content to
  create or move an existing accepted reference;
- multiple physical accepted payloads for equal canonical bytes at the same
  occupied `VersionId`;
- editing a committed payload in place after fork;
- layer/parent/delta reconstruction as selected truth;
- runtime-private workspace/mount facts in `VersionId`;
- storage-owned MCTS/rollout policy;
- an unbounded root/custody/retirement model;
- a new owner, writer, crate, service, database, coordinator, or object-DAG
  storage family for correctness; or
- a rollback/reference operation that bypasses accepted-binding validation or
  silently merges/rebases.

Do not reopen merely because Phase 02 chooses a codec/digest or Phase 03 chooses
a safe record spelling, atomic filesystem primitive, finite limit, same-Version
outcome, or custody representation inside these fixed semantics.

## References

- [Product PRD](../PRD.md)
- [Phase 00 evidence](../phases/00-freeze-rules/SPEC.md)
- [Phase 01 selection contract](../phases/01-choose-design/SPEC.md)
- [Selected architecture](../architecture_design.md)
- [Version identity design](../design/02-state-identity.md)
- [LayerStack-0 storage design](../design/03-state-store.md)
- [Algorithms and call flows](../design/04-algorithms-and-call-flows.md)
- [Concurrency, durability, and recovery](../design/05-concurrency-durability-recovery.md)
- [Phase 03 tests](../phases/03-state-store/test-perf.md)
- [Publish, OCC, and conceptual head CAS](04-publish-occ-and-head-cas.md)
- [Diagrams index and conventions](README.md)
