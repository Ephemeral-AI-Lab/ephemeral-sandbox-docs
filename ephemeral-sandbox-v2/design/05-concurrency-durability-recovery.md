# R0 concurrency, durability, and recovery

**Status:** `LOCKED_PHASE_01` semantics; exact Phase 03 filesystem mechanics
are `SELECT_IN_PHASE_03`

**Selected architecture:** [R0](../architecture_design.md)

**Proof owners:** [Phase 03](../phases/03-state-store/PRD.md), then frozen-artifact
requalification in [Phase 06](../phases/06-prove-offline/PRD.md)

## Purpose and authority

This document expands the selected R0 failure model into implementation and
test obligations. It does not choose another owner, storage family, writer, or
recovery authority. Product [hard rules 1–10](../PRD.md#hard-rules-must-never-break)
and the root [architecture design](../architecture_design.md) remain higher
authority.

The store is a local, in-process library with one process/filesystem-exclusive
selected-Version transition gate. Multi-host active/active writing is not an R0
assumption. If implementation requires a second writer, coordinator, service,
database, or different storage family, Phase 01 must be reopened.

## Fixed safety model

The following are fixed by Phase 01:

- one Accepted Version at an occupied `VersionId` has one complete immutable payload closure;
- a payload becomes referenceable only after complete admission and required
  durability;
- every occupied ID is resolved by full canonical-byte comparison;
- roots and heads name store-accepted bindings, never unchecked digests;
- a complete head-record replacement under the transition gate is the sole OCC
  linearization point;
- a stale expected `(AcceptedBinding, HeadRevision)` changes no Head and never triggers
  merge or rebase;
- a reference-only transition never opens the payload and reports selected
  payload bytes read, written, and copied as zero;
- readers retain bounded custody of the captured immutable Version while a Head
  may advance;
- retirement revalidates durable roots/heads and active read custody before
  unlinking; and
- recovery exposes prior truth, complete new truth, or a fail-closed diagnosis—
  never reconstructed, partial, or dangling selected truth.

## Authority and linearization points

| Action | Authority | Required visibility/linearization rule | Phase 03 choice still open |
|---|---|---|---|
| Candidate validation and canonicalization | LayerStack-0 calling the pure Phase 02 identity module | No selected-Version visibility; failure changes no Root/Head | Buffering, traversal, and bounded streaming details |
| Payload admission | `sandbox-runtime-layerstack` store owner | One atomic accepted-occupancy event must make either no payload or one complete immutable payload visible for an ID | Exact install primitive, record spelling, and durability fence sequence |
| Occupied-ID resolution | Store owner | Full canonical bytes decide equal/reuse versus collision before reference mutation | Exact comparison implementation and instrumentation |
| Head publication | Store owner under the single transition gate | Atomic complete replacement of `(accepted binding, HeadRevision)` is the **sole OCC linearization point** | Exact temporary name, record encoding, checksum, rename/fence sequence |
| Accepted-reference transition | Store owner under the transition gate | `CreateHeadIfAbsent`, `ReplaceHead`, `RemoveHead`, `CreateFixedRootIfAbsent`, and `RemoveFixedRoot` use one reference authority; only `ReplaceHead` retargets a reference, and no operation opens the payload | Same bounded metadata mechanics as selected in Phase 03 |
| Read capture | Store owner | Custody must be acquired so retirement cannot pass final revalidation while the captured payload is in use | Token/guard/registry representation and exact acquisition protocol |
| Retirement | Store owner under transition authority | Final exact roots/heads/custody revalidation precedes unlink; no new root or reader may slip between them | Exact bounded scan/index aid and unlink durability sequence |
| Recovery readiness | Store owner during lifecycle-controlled startup | No mutating ingress before validation and bounded cleanup establish readiness | Startup ordering and quarantine representation |

Payload admission and reference publication are distinct events. Admission may
leave a complete unreferenced payload after a stale publication or crash; that
is bounded cleanup debt, not selected truth. A root/head must never name a
private staging path or an incompletely admitted payload.

## Required concurrency histories

Phase 03 must make these histories deterministic enough to test. Phase 06 must
rerun the applicable tests on the frozen candidate artifact.

| History | Required outcome | Forbidden outcome | Primary proof |
|---|---|---|---|
| Two equal candidates race for an unoccupied ID | Both resolve to the same accepted binding and exactly one physical payload closure | Duplicate accepted payloads or digest-only acceptance | Concurrent admission plus physical-count assertion |
| Equal Candidate races an already accepted equal Version | Full comparison establishes equality and the existing payload is reused | Bypassing comparison because the digest exists | Forced occupied-ID instrumentation |
| Unequal candidate has the same forced ID as accepted bytes | Typed collision; no root/head change and no alias | Last-writer-wins, overwrite, or silent sharing | Forced-collision seam across every candidate ingress |
| Two publishers use the same expected revision | At most one head replacement succeeds; every loser is stale | Both report success, merge, rebase, or overwrite | Barrier-controlled OCC history |
| Publisher races Head rollback/move | `ReplaceHead(Expected::Exact(...))` operations serialize at the same transition gate; only a complete exact expected Head can win | Independent writers, implicit retry, or a reference naming unaccepted content | Mixed-operation history and head/revision assertions |
| Candidate is admitted, then its publisher loses OCC | Winner alone changes the head; loser may leave one bounded complete orphan | Loser mutates the head or triggers silent content merge | OCC test plus recovery/retirement debt accounting |
| Reader captures old head while publisher advances it | Reader completes against the captured immutable old payload; later reads may resolve new head | Reader switches payload mid-read | Barrier-controlled capture/publish history |
| Reader acquisition races last-root retirement | Either custody is established and retirement retains, or retirement wins and capture fails/retries cleanly | Successful reader observes an unlinked/partial payload | Custody/retirement history at the final gate |
| New fixed Root or Head races retirement | Either `CreateFixedRootIfAbsent`/`CreateHeadIfAbsent` becomes durable and prevents unlink, or retirement completes before the operation can accept the binding | Durable reference points to missing payload | Gate-serialized reference/retirement history |
| Cancellation/timeout races staging | No reference changes; private state is removed or remains recognizable bounded debt | Untracked scratch, leaked descriptors/workers, or partial head | Cancellation injection and post-recovery accounting |
| Resource exhaustion/ENOSPC occurs at each persistent step | Operation fails before success acknowledgement; old truth remains or complete new truth is recoverable | Dangling reference, mixed payload, or unbounded retry loop | Fault injection at each store write/fence boundary |
| Recovery races attempted mutating ingress | Lifecycle owner blocks ingress until readiness succeeds | A write runs against unvalidated or partially cleaned state | Startup integration test |

The test oracle is the accepted history and physical effects, not wall-clock
timing. Sleep-based races alone are insufficient; tests should use barriers,
fault hooks, or controlled store primitives.

## Conceptual publication sequence

This order is fixed; the exact syscall sequence is not:

1. application code authorizes/orders the operation and captures the expected
   head and revision;
2. the store validates and canonicalizes bounded complete candidate facts;
3. the store builds recognizable private staging;
4. occupied ID means full canonical-byte comparison: equal reuses, unequal
   fails collision;
5. a new payload, if needed, becomes complete, durable, immutable, and
   atomically accepted;
6. under the one transition gate, the store rereads the expected head/revision;
7. stale fails without head mutation, merge, or rebase;
8. a complete replacement head record is made durable and atomically installed;
9. success is acknowledged only after Phase 03's qualified durability boundary.

The expensive candidate capture, canonicalization, hashing, comparison, and
payload construction should occur outside the final OCC gate where correctness
allows. This is a contention-reduction hypothesis, not permission to split the
authoritative revision check from the head replacement.

## Crash-prefix obligations

Phase 03 must replace the conceptual stages below with its exact persistent
steps and execute a fault/crash matrix on every meaningful prefix. The outcome
column is normative even though the low-level mechanism is deferred.

| Crash/fault cut | Required restart outcome | Permitted bounded debt | Must never happen |
|---|---|---|---|
| Before staging is created | Prior selected truth | None | Any new reference |
| During private staging | Prior selected truth | Recognizable incomplete staging eligible for idempotent cleanup/quarantine | Staging interpreted as accepted payload |
| After staging is complete but before admission | Prior selected truth | Complete private staging | Root/head names the private path |
| During validation, hashing, or occupied-ID comparison | Prior selected truth | Recognizable staging only | Collision mismatch changes accepted content or reference |
| During new payload admission | Recovery sees no accepted payload or one complete immutable accepted payload | Private staging and, if complete, an unreferenced payload | Partial payload accepted under `VersionId` |
| After payload is durable/accepted but before head work | Prior head remains | Complete unreferenced payload | Head points to incomplete payload |
| During head temporary-record construction | Prior head remains | Recognizable private metadata temporary | Partial temporary treated as head |
| During atomic head replacement, before acknowledgement | Recovery exposes one valid prior or complete new head record | Safe temporary/orphan debt | Torn/mixed accepted head or two successful OCC outcomes |
| After head replacement but before its durability boundary | Caller has not received success; restart may expose prior or complete new truth according to the qualified filesystem contract | Recognizable temporary/orphan debt | Success was acknowledged before durability |
| After durable head, before response delivery | Complete new truth may persist; caller has an unknown outcome and retry is resolved by OCC/idempotency rules | No correctness debt beyond normal orphan accounting | Rollback to partial/mixed truth |
| After success acknowledgement | Complete new head and payload survive every supported restart model | Bounded unrelated cleanup debt only | Acknowledged head disappears or dangles |
| During accepted-reference transition | Prior, absent, or complete new small record according to the exact operation; payload counters remain zero | Recognizable metadata temporary | Generic Root retarget, payload opened/copied, or dangling reference |
| During retirement before unlink | Payload remains available | Deferred retirement item | Rooted or custodied payload disappears |
| During/after retirement unlink | Unlink is allowed only after exact final revalidation; recovery must not resurrect a reference | Bounded retirement bookkeeping debt | Any durable reference names removed payload |
| During cleanup or quarantine | Cleanup is idempotent and restartable | Still-recognizable bounded debt | Cleanup invents/deletes selected truth |
| During recovery itself | Next startup repeats validation/cleanup safely | Bounded recovery marker/debt if selected | Recovery requires human inference to choose truth |

For every acknowledged operation, Phase 03 must state which files and
directories have crossed the durability boundary. Merely closing a file or
successfully returning from rename is not assumed to imply durability.

## Recovery and readiness algorithm

Before declaring the store ready, recovery must:

1. validate store generation and control-record version/integrity;
2. validate the supported filesystem/configuration profile;
3. classify all bounded recognized staging and metadata temporaries;
4. validate every accepted payload descriptor and the completeness needed to
   serve it, without reconstructing from legacy layers;
5. validate every head/root record, revision, accepted binding, and target;
6. detect dangling references, unknown versions, checksum/integrity failures,
   digest/byte ambiguity, and unclassifiable store entries;
7. perform only deterministic, idempotent, bounded cleanup or quarantine; and
8. either publish a ready diagnostic generation or fail readiness closed.

Recoverable private debt may be cleaned in bounded batches only if selected
truth is already unambiguous and the configured debt ceiling is not exceeded.
Corrupt/ambiguous selected metadata, dangling roots/heads, unsupported versions,
unsupported durability topology, or excessive debt fail readiness. Recovery
must not repair truth by following parents, squashing layers, choosing the
newest timestamp, or silently deleting an accepted reference.

## Phase 03 filesystem profile decision

Phase 03 must select and document a supported local-filesystem profile rather
than assuming all filesystems share the same crash semantics.

| Question Phase 03 must answer | Required constraint |
|---|---|
| What atomic replacement primitive is supported? | It must expose only a complete prior or complete new record within the selected topology. |
| Are all atomic renames constrained to one filesystem/directory topology? | Cross-filesystem fallback may not silently copy or weaken atomicity. |
| What synchronizes payload file data and metadata? | The acknowledged payload must survive the qualified restart/power-loss model. |
| What synchronizes directory entry creation, replacement, and unlink? | The documented fence sequence must cover the directories whose names carry accepted truth. |
| How is the exclusive transition gate implemented and recovered? | It must cover all selected-Version reference writers and final retirement revalidation without creating another authority. |
| How are complete records integrity-checked and versioned? | Torn, corrupt, and unknown records fail closed. |
| How is immutable payload custody enforced? | Product APIs cannot obtain a writable committed handle; attempted mutation is tested. |
| How is safe candidate traversal performed? | Descriptor/path-resolution mechanics must prevent symlink escape and TOCTOU replacement. |
| Which filesystem/configuration profiles are unsupported? | Readiness must reject them explicitly rather than downgrade guarantees. |

Allowed local choices include record encoding, checksums, temporary names,
directory spellings, lock primitive, safe descriptor traversal, exact
`fsync`/rename order, custody representation, and finite constants. A choice is
valid only after targeted fault and restart tests prove the fixed model.

## Proof matrix

| Obligation | Phase 03 evidence | Phase 06 evidence |
|---|---|---|
| One OCC linearization point | Barrier-controlled concurrent histories and source audit | Must suite rerun on frozen artifact |
| Prior-or-complete-new publication | Exact crash-prefix/fault matrix on supported filesystem profile | Must crash suite rerun |
| Exact collision handling | Forced collision at every candidate ingress | Frozen-artifact integration rerun |
| Reference-only payload I/O zeros | Store counters plus syscall/fixture evidence | Integrated operation rerun with counters |
| Immutable captured reads | Read/head-move and mutation-attempt tests | Integrated regression |
| Last-root/read-custody safety | Barrier-controlled retirement histories | Stress rerun if in qualification set |
| Bounded cleanup and cancellation | Boundary/fault tests with post-run resource accounting | Resource/crash suite rerun |
| Readiness fails closed | Corrupt, dangling, unknown-version, excessive-debt, and unsupported-profile fixtures | Frozen-artifact startup rehearsal |

## Reopening conditions

Reopen Phase 01 rather than weakening R0 if any of these becomes true:

- the supported deployment cannot provide prior-or-complete-new durability for
  payload-before-reference publication;
- more than one selected-Version writer or OCC linearization point is required;
- exact collision comparison cannot be completed within finite resources;
- read custody and exact reachability cannot close the last-root race within a
  bounded model;
- recovery needs a second authority, unbounded scan/population, layer-history
  reconstruction, or human choice between competing truths;
- reference-only transitions require opening or copying payload bytes; or
- a new service, process, database, coordinator, owner, or storage family is
  necessary to satisfy a correctness invariant.

Do not reopen Phase 01 merely because Phase 03 selects a different safe record
encoding, checksum, temporary naming convention, finite constant, or qualified
fence sequence inside these constraints.

## References

- [Product PRD](../PRD.md)
- [Selected architecture](../architecture_design.md)
- [Phase 00 evidence and baseline policy](../phases/00-freeze-rules/SPEC.md)
- [Phase 03 PRD](../phases/03-state-store/PRD.md),
  [plan](../phases/03-state-store/PLAN.md), and
  [test/performance contract](../phases/03-state-store/test-perf.md)
- [Phase 06 qualification contract](../phases/06-prove-offline/test-perf.md)
