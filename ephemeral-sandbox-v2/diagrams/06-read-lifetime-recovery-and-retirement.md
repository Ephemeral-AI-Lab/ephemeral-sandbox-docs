# Read lifetime, recovery, and retirement

**Status:** explanatory view of the selected R0 architecture

**Authority:** [V2 PRD](../PRD.md) -> Phase 01 [selection input contract](../phases/01-choose-design/SPEC.md) -> selected [architecture output](../architecture_design.md)

**Purpose:** contrast the source-grounded e497 history representation with the
selected complete-Version read model, then show reader custody, retirement, crash
outcomes, and bounded fail-closed recovery.

The current-system panel records representation facts only. It does not import
legacy behavior into V2 semantics. Exact custody tokens, record encodings,
durability syscalls, filesystem profile, and recovery limits remain Phase 03
choices within the locked R0 outcomes.

## Legend

```text
+----------------------+   permanent owner or authoritative durable object
[private/staging]          incomplete or operation-private state
[custody]                  bounded proof that a captured reader may use payload
---->                      ordinary call, read, or state transition
- - ->                     diagnostic/cleanup edge; not authority
===>                       authoritative publication or lifecycle transition
-X->                       illegal edge or state

CURRENT e497                SOURCE-VERIFIED current representation
SELECTED R0                 locked V2 architecture decision
LEGAL                       restart may expose this state
ILLEGAL                     recovery must fail closed; never report ready
```

## Current history-oriented read versus selected complete-Version read

```text
CURRENT e497 -- SOURCE-VERIFIED REPRESENTATION
(legacy evidence, not V2 semantics)

 +--------------------+
 | manifest / current |
 | history position   |
 +---------+----------+
           |
           v
 +--------------------+    parent    +--------------------+    parent
 | newest layer       | -----------> | earlier layer      | -----------> ...
 +--------------------+              +--------------------+
           |
           +---- project/reconstruct ordered history ----> readable result

 Durable truth is history/layer oriented in the pinned e497 source. The exact
 current source anchors are summarized by Phase 00; this panel does not claim
 that every public read follows one identical code path.


SELECTED R0 -- ARCHITECTURE DECISION

 +--------------------+       capture       +------------------------+
 | root or head       | ------------------> | accepted binding       |
 | complete record    |                     | VersionId + store proof  |
 +--------------------+                     +-----------+------------+
                                                     |
                                             acquire | bounded custody
                                                     v
                                             +-------+--------+
                                             | one complete   |
                                             | immutable      |
                                             | payload closure|
                                             +-------+--------+
                                                     |
                                                     v
                                                reader result

 No parent-layer walk, layer-depth reconstruction, squash, or reference-path
 payload copy participates in V2 selected truth.
```

A read of a live session Workspace remains a runtime-effect read and can expose
private mutable files under the workspace owner's rules. It is not a read of an
accepted immutable V2 Version and cannot redefine `VersionId` or selected truth.

## Reader versus head-move race

```text
 time       reader R                 store / selected head          publisher P
 -----      --------                 ---------------------          -----------
 t0                                  head = (binding X, rev 8)

 t1         capture complete
            head record X/rev8
            and acquire custody X
            under store protocol

 t2                                  head X/rev8                    request move
                                      |                             expected X/rev8
                                      +---------------------------- winner Y

 t3                                  atomic replacement
                                    ===> head = (binding Y, rev 9)
                                         OCC linearization

 t4         read immutable payload X
            using already acquired
            custody; result remains X

 t5         release custody X

 t6         a new reader captures head Y/rev9 and reads payload Y
```

The legal history is deliberately simple: the first reader returns the Version
it captured, while a later reader returns the newly selected Version. A Head move
does not invalidate an acquired reader and does not mutate payload X.

An exact lock, lease, file descriptor, in-memory epoch, or durable custody
representation is **deferred**. Phase 03 must select one that proves the same
history across process and daemon boundaries actually supported by the
product; it may not assume a process-local counter is sufficient without that
proof.

## Last-root, custody, and retirement race

There are two legal winners. There is no legal history in which retirement
unlinks a payload after a reader has successfully acquired custody but before
that reader finishes.

```text
CASE A -- READER ACQUIRES CUSTODY FIRST

 reader                         transition/retirement gate
   |                                       |
   | capture binding X                     |
   | acquire custody X ------------------->| record/validate custody
   |<-------------------------- success    |
   |                                       |
   |                              remove last durable Head/fixed-Root edge X
   |                              revalidate exact roots/heads
   |                              observe custody X > 0
   |                              retain payload X; defer retirement
   |
   | read X; release custody ------------->|
   |                                       | revalidate again
   |                                       | no roots/heads/custody
   |                                       ===> retire/unlink X


CASE B -- RETIREMENT COMMITS FIRST

 retirement gate               reader
       |                          |
       | prove no exact root/head|
       | and no custody for X     |
       ===> retire/unlink X       |
       |                          | attempt capture/acquire X
       |<-------------------------|
       | return missing/retry ---->|  (never a dangling successful read)
```

The authority test uses exact durable roots/heads plus the selected custody
mechanism. A persistent refcount, reachability cache, or diagnostic gauge may
accelerate work, but it cannot be the sole truth unless Phase 03 proves it is
transactionally equivalent to exact roots/heads and custody under all required
crash histories.

## Accepted-payload lifecycle

```text
 [private stage]
       |
       | validate portable input; canonicalize; derive typed VersionId
       | inspect occupied ID; compare full canonical bytes
       | make complete payload durable and immutable
       v
 +------------------------+
 | ACCEPTED, UNROOTED     |  valid accepted binding; no durable Head/fixed Root yet
 +-----------+------------+
             |
             | complete root/head record names binding
             v
 +------------------------+
 | ROOTED / SELECTED      |<-----------------------------+
 +-----------+------------+                              |
             |                                           |
             | Head replace/remove or fixed-Root remove  | new Head/fixed Root
             v                                           |
 +------------------------+                              |
 | UNROOTED, CUSTODY > 0  | -----------------------------+
 | or retirement pending  |  (if a durable root is added)
 +-----------+------------+
             |
             | last custody released; exact revalidation
             v
 +------------------------+
 | RETIREMENT ELIGIBLE    |
 +-----------+------------+
             |
             | bounded cleanup commits unlink/retirement
             v
 +------------------------+
 | RETIRED                |
 +------------------------+

 [private stage] -X-> root/head
 RETIRED        -X-> successful custody/read without a fresh accepted admission
```

An occupied VersionId with equal full canonical bytes reuses the one physical
payload. An occupied VersionId with different canonical bytes is a collision and
is rejected; it is never another branch of this lifecycle.

## Crash prefixes: legal and illegal restart states

```text
LEGAL RESTART-OBSERVABLE OUTCOMES

 L1  old payload X durable; head X complete
     -> publish did not linearize; X remains selected

 L2  payload Y durable and accepted; head X complete
     -> Y is an accepted orphan/unrooted payload; bounded recovery/retirement

 L3  payload Y durable and accepted; head Y complete
     -> publish linearized; Y is selected

 L4  recognizable private staging or retirement debt
     -> bounded recovery can validate, finish, quarantine, or remove it


ILLEGAL / FAIL-CLOSED CONDITIONS

 I1  head/root names a missing, incomplete, or unvalidated payload
 I2  torn, ambiguous, or unparseable authoritative head/root record
 I3  payload is mutable after it became accepted
 I4  occupied VersionId bytes differ but are treated as equal/reused
 I5  unknown artifact can affect selection or is guessed into acceptance
 I6  recognizable debt exceeds configured recovery work/byte/item limits
 I7  retirement state cannot establish whether a live reader still has custody

 Any I-state => NOT READY. Recovery reports/quarantines exact evidence and
 performs no best-effort guess, silent repair, merge, or rebase.
```

## Bounded fail-closed recovery

```text
 startup / explicit recover
          |
          v
 +-------------------------+
 | establish finite limits |
 | items, bytes, work/time  |
 +------------+------------+
              |
              v
 +-------------------------+
 | scan authoritative roots|
 | heads, accepted records, |
 | recognizable private    |
 | staging/retirement debt |
 +------------+------------+
              |
              v
 +-------------------------+
 | validate exact bindings |
 | complete bytes, records,|
 | and lifecycle relations |
 +------------+------------+
              |
       +------+--------------------+
       |                           |
       v                           v
 recognizable, bounded,        corrupt / dangling /
 unambiguous prefix            ambiguous / unknown /
       |                       excessive debt
       |                           |
       v                           v
 finish safe prefix,           quarantine/report exact
 remove private debris,        evidence and FAIL CLOSED
 or leave prior truth          (service not ready)
       |                           |
       v                           X
 verify invariants ----------> READY
```

Recovery recognizes protocol facts; it does not scan arbitrary files and infer
selected truth from names or timestamps. The Phase 03 filesystem profile must
state which same-filesystem rename, atomic replacement, file and directory
durability, unlink, permissions, and restart guarantees are assumed. An
unsupported filesystem or violated assumption is a fail-closed condition.

## Invariants

1. A V2 accepted payload is a complete immutable Version; captured reads never
   reconstruct selected truth by walking a layer chain.
2. A reader returns either the complete binding captured before a concurrent
   Head move or the complete binding after it. It never mixes Versions.
3. A successful custody acquisition prevents retirement for the lifetime of
   that reader.
4. Retirement occurs only after exact revalidation proves no durable root/head
   and no supported reader custody remains.
5. Accepted payload bytes cannot be modified by live file writes or edits.
6. A root/head cannot name private staging or an incomplete payload.
7. Every publish crash prefix exposes either the prior complete head or the
   complete new head, with at most recognizable bounded private/orphan debt.
8. Dangling references, torn authoritative records, ambiguous collisions,
   unknown authority-affecting artifacts, unsupported filesystem behavior, and
   excessive recovery debt fail closed.
9. Observability may read and report recovery/custody/retirement state but
   cannot certify readiness or mutate selected authority independently.
10. Recovery, staging, reader custody, retirement work, memory, descriptors,
    and workers all have finite enforceable ceilings.

## Selected architecture versus delegated details

| Topic | Status | Boundary |
|---|---|---|
| Complete-Version captured read | **SELECTED R0** | No layer-depth reconstruction in selected truth. |
| Immutable accepted payload | **SELECTED R0** | Live workspace writes produce candidates, never in-place committed mutation. |
| Reader/Head-move history | **SELECTED R0** | Reader returns the captured complete Version; new readers may observe the new Head. |
| Exact-root plus custody retirement safety | **SELECTED R0** | No last-root deletion while a supported reader remains. |
| Prior-or-complete-new crash outcome and fail-closed corruption | **SELECTED R0** | Required publish/recovery family. |
| Canonical grammar and validation limits | **DEFERRED PHASE 02** | Must support full-byte equality and portable complete-Version closure. |
| Custody representation and cross-process protocol | **DEFERRED PHASE 03** | Must match actual reader/process lifetime; bounded and crash-safe. |
| Exact layout, record checksums, fsync/rename order, locks | **DEFERRED PHASE 03** | Must declare and test the supported filesystem profile. |
| Recovery item/byte/work limits and quarantine format | **DEFERRED PHASE 03** | Finite values are required before production use. |
| Retirement scheduling and safe acceleration indexes | **DEFERRED PHASE 03** | Exact roots/heads/custody remain authoritative. |
| `file_blame` public semantics (`DEC-001`) | `OWNER_DEC_OPEN`, isolated | May affect API/history availability, not the selected store family or read safety. |

## Verification mapping

| Claim in this view | Evidence now | Later proof owner |
|---|---|---|
| e497 durable history is LayerStack/layer oriented | `SOURCE-VERIFIED` by [Phase 00 inventories](../phases/00-freeze-rules/SPEC.md) | No V2 proof; current-source context only |
| Read captures one complete Version across concurrent Head move | `INFERRED` implementable under R0 | Phase 03 deterministic reader/Head histories |
| Last-root retirement respects active custody | `INFERRED` mechanism family selected | Phase 03 race tests and Phase 06 offline stress |
| Equal bytes reuse; mismatching occupied ID rejects | `INFERRED` required outcome; exact mechanics deferred | Phase 02 vectors plus Phase 03 collision/admission tests |
| Crash produces prior or complete new head only | `INFERRED` from selected publication family | Phase 03 crash-point matrix on declared filesystem profile |
| Recovery fails closed on dangling/corrupt/ambiguous state | `INFERRED` required outcome | Phase 03 corruption fixtures and restart tests |
| Recovery and cleanup remain bounded | `INFERRED` requirement; finite constants `OPEN_WITHIN_R0` | Phase 03 resource tests and Phase 06 load/crash replay |
| Public read routing preserves live Workspace versus Accepted-Version distinction | Current distinction source-grounded; V2 routing not implemented | Phase 04 wiring tests |

No benchmark comparison is part of this proof. Historical Stage 4.6 results
remain `INCOMPARABLE`.

## Reopening conditions

Reopen Phase 01 if implementation evidence shows that any of these is required:

- selected-Version reads must reconstruct a parent/layer chain or depend on
  layer depth;
- accepted payloads must remain writable after publication;
- safe reads require moving selected-Version authority to a new package, service,
  database, registry, or helper process;
- retirement cannot be made safe using exact roots/heads plus a bounded custody
  protocol within the selected owner;
- the supported filesystem cannot provide a tested prior-or-complete-new
  publication family and no equally coherent in-place family exists;
- recovery must guess selected truth, accept dangling references, or perform
  unbounded work before readiness; or
- a persistent refcount or diagnostic index must replace roots/heads as truth
  rather than remain a derived optimization.

## Related documents

- [Architecture design](../architecture_design.md)
- [LayerStack-0 Version-storage design](../design/03-state-store.md)
- [Algorithms and call flows](../design/04-algorithms-and-call-flows.md)
- [Concurrency, durability, and recovery](../design/05-concurrency-durability-recovery.md)
- [Resources, security, and observability](../design/06-resources-security-observability.md)
- [Source and implementation map](../design/09-source-and-implementation-map.md)
- [Phase 00 frozen source facts](../phases/00-freeze-rules/SPEC.md)
- [Phase 01 selection input contract](../phases/01-choose-design/SPEC.md)
- [Storage-model diagram](02-storage-model-and-content-addressing.md)
- [Publish/OCC diagram](04-publish-occ-and-head-cas.md)
