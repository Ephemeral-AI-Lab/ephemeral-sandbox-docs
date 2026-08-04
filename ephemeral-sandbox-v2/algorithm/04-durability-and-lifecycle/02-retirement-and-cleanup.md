# 04.02 — Retirement and cleanup

## 1. Purpose and owning phase

**Owner:** Phase 03 — LayerStack-0 durable storage; runtime owners clean their
own Workspace/mount/namespace/exec effects.  
**Purpose:** Retire one complete accepted payload closure only after exact
Head/Root reachability and active read/operation custody are absent and the
result is revalidated under transition authority; clean private staging,
OCC-loser orphans, cancellations, and crash residue within finite debt.

Retirement operates on whole Versions. It does not trace or collect a graph of
cross-Version objects, reconstruct layers, or use persistent refcounts as
authority.

## 2. Evidence status

- `SOURCE-VERIFIED`: the selected package is source-placeable as durable owner,
  while manager/daemon/runtime packages retain lifecycle-effect cleanup.
- `SPIKE-VERIFIED`: none; V2 last-root/read races, detach/restart behavior, and
  cleanup-debt tests have not run.
- `INFERRED`: exact bounded Head/Root scan plus custody, ID reservation, and
  final transition-gated revalidation safely identifies a whole closure for
  retirement.
- `OPEN`: Phase 03 selects the retirement marker/detach mechanism, lock order,
  grace policy, exact custody representation, record scan/index mechanics,
  quarantine, batching, restart protocol, and finite constants.

## 3. Authoritative liveness model

An AcceptedVersion is not retirement-eligible if any of these exact authorities
names or protects it:

1. any valid complete Head record contains an AcceptedBinding to it;
2. any valid complete typed Root contains an AcceptedBinding to it;
3. any active bounded read custody protects it;
4. any bounded in-flight operation custody/reservation protects its use while a
   binding is being handed to publication or runtime; or
5. migration/recovery holds an explicit bounded custody/fence that Phase 03/05
   defines within the same authority.

The first two are durable reachability. Custody is runtime/recovery lifecycle
state serialized against final retirement. An AcceptedBinding copied into
untracked application memory is not a durable Root; it must be revalidated and
may become unavailable after retirement.

Candidate lists, age queues, metrics, cached reverse maps, approximate counts,
reference counts, and “last used” timestamps may prioritize scans but are never
retirement authority. Every deletion decision performs the exact final check.

## 4. Contract

Conceptual names express responsibility and type flow, not exact API or disk
spellings.

### Inputs

- A revalidated or scheduled AcceptedVersion candidate.
- Complete bounded Head and typed Root namespaces for the active generation.
- Active read and operation custody populations.
- Recognizable staging/orphan/retirement/debt inventory from recovery.
- Finite scan, lock-wait, batch, bytes, entries, memory, FDs, workers, elapsed,
  and debt budgets.

### Preconditions

1. LayerStack-0 is ready and owns the only writer/recovery/retirement authority.
2. All Head/Root/custody populations were admitted under finite global limits.
3. The target resolves beneath the typed accepted namespace and revalidates as
   one complete immutable AcceptedVersion.
4. A fixed Phase 03-selected acquisition order prevents deadlock between the
   target `VersionId` admission reservation and the transition authority.
5. Corrupt/unknown records block a destructive decision; absence is never
   inferred from a failed read or partial scan.

### Outputs

One typed retain/defer/detach/error result and, after a proven detach, a bounded
whole-Version reclamation task or completed reclamation result. No per-object
reachability graph is produced.

### Typed outcomes

| Outcome | Meaning |
|---|---|
| `RetiredDetached` | Final exact checks found no reachability/custody, and the complete closure became unavailable as accepted truth at one retirement visibility point. Physical reclamation may continue as bounded debt. |
| `RetainedReachable(refs)` | At least one exact valid Head or Root names the Version. Nothing was detached. |
| `RetainedInCustody` | Active read/operation/migration/recovery custody exists. Nothing was detached. |
| `AlreadyRetired` | Target is already in a recognized retirement/cleanup state; idempotent cleanup may continue. |
| `DeferredBusy` | The target reservation, transition gate, runtime cleanup, or bounded batch was unavailable. |
| `LimitExceeded` | Exact scan or cleanup cannot finish within the configured finite envelope. Nothing is destructively inferred. |
| `CorruptReachability` | A Head/Root/binding/custody/target record is invalid or ambiguous; retirement fails closed and may quarantine. |
| `CancelledBeforeDetach` | Cancellation occurred before retirement visibility. Accepted truth remains. |
| `OutcomeUnknown` | A crash/I/O failure occurred around detach; recovery must classify before access or deletion continues. |

## 5. Whole-Version retirement algorithm

```text
retire_if_unreachable(version, budget):
    validate typed VersionId only as lookup key; revalidate AcceptedVersion
    reserve one bounded retirement/debt slot

    acquire target VersionId admission reservation in fixed Phase 03 order
    acquire sole LayerStack-0 transition gate

    target := revalidate complete accepted closure and active generation
    if already retiring/retired:
        release authorities; return AlreadyRetired

    heads := exact bounded scan of every complete Head record
    roots := exact bounded scan of every complete typed Root record
    if any record is corrupt/unknown/incomplete:
        release authorities; return CorruptReachability
    if any binding names target:
        release authorities; return RetainedReachable

    custody := exact bounded inspection of active read, operation,
               migration, and recovery custody
    if custody protects target:
        release authorities; return RetainedInCustody

    # Final check is still under both exclusion authorities.
    revalidate no new Head, Root, custody, or accepted-slot transition appeared
    make the entire accepted closure unavailable through the Phase 03-selected
        recognizable atomic detach/retirement transition
    apply qualified retirement visibility fence

    release transition gate and VersionId reservation
    enqueue the detached whole closure as bounded physical-cleanup debt
    return RetiredDetached
```

The exact scan may use a validated bounded index to locate records, but the
index cannot be the authority unless Phase 03 proves it is itself exactly and
transactionally the Head/Root namespace—not a persistent refcount or tracing
summary. The simplest valid R0 algorithm scans all bounded complete records.

### Physical reclamation

```text
reclaim_detached_closure(item, cleanup_budget):
    require item is recognizably detached in the active/retired generation
    require accepted-binding revalidation can no longer return it
    remove the complete closure beneath anchored retirement scope in bounded work
    persist/validate cleanup progress only as Phase 03 permits
    on failure retain classified debt; never re-expose a partial closure
```

Detachment makes the Version unavailable; deletion may take longer. Reclamation
never edits a still-accepted closure in place.

## 6. Staging, orphan, and cancellation cleanup

### Private staging

Recognizable states from
[durability and recovery](01-durability-and-recovery.md) are handled as
follows:

- partial/private Candidate or payload: delete or quarantine after proving it
  never became accepted;
- complete private duplicate equal to an accepted closure: retain the accepted
  closure and remove only private staging;
- installation-ambiguous or mismatching evidence: quarantine and fail closed;
- private reference record before replacement: preserve prior authoritative
  reference and remove the temporary; and
- cleanup interrupted by crash: resume the same classified action
  idempotently.

### OCC-loser orphan

An admitted target left unreachable after stale/cancelled publication is an
ordinary AcceptedVersion, not corrupt staging. After any Phase 03-selected
minimum safety/grace requirement, it becomes a retirement candidate and must
pass the same exact Head/Root/custody final algorithm. A queue entry or “OCC
loser” label never authorizes deletion.

### Cancellation

- Before detachment, cancellation leaves accepted truth unchanged and releases
  reservations.
- After detachment crosses retirement visibility, cancellation does not
  reattach the Version. It leaves classified whole-closure cleanup debt for
  idempotent restart.
- Runtime cleanup may conservatively retain custody if immutable access cannot
  yet be proved closed.

## 7. Visibility and linearization

The retirement visibility point is the Phase 03-qualified complete transition
that makes the accepted slot unavailable to AcceptedBinding revalidation while
the target reservation and transition gate are held, after the final exact
Head/Root/custody check.

This is not a Head linearization point. It does not mutate a Head. The only
state-changing Head point remains the conditional complete Head-record
replacement in [OCC publication](../02-references-and-publication/02-occ-publication.md).

Physical unlink/reclamation after detachment is cleanup, not the authority
point. A crash before detach preserves the AcceptedVersion; a crash after
detach keeps it unavailable and recovery resumes whole-closure cleanup, unless
the qualified protocol cannot classify the prefix—in which case startup fails
closed.

## 8. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal reachable | Exact scan finds a Head/Root; return retained without touching payload. |
| Normal custody | Exact custody inspection finds a reader/operation; defer without touching payload. |
| Normal unreachable | Final revalidation under both authorities passes; detach whole closure once; reclaim in bounded batches. |
| Concurrent Root/Head creation | Shared transition authority orders the operations. Either reference wins and retirement retains, or retirement wins and binding revalidation fails before reference creation. |
| Concurrent read capture | Shared transition authority orders custody installation and final check. Either custody wins and retirement defers, or detach wins and capture fails. |
| Concurrent equal admission | Target ID reservation prevents install/reuse from racing the final detach; retry sees accepted, retiring, or absent state and follows ordinary admission safely. |
| Retry | Re-running before detach repeats exact checks; after detach recognizes the same retirement item and continues cleanup without double authority. |
| Cancellation | Before detach preserves truth; after detach preserves unavailability and charges cleanup debt. |
| Crash/restart | Recovery classifies accepted, detaching, detached, partially reclaimed, and ambiguous states; actions are idempotent and bounded. |
| Cleanup failure | Retain classified debt, apply backpressure/readiness policy, and never delete reachable/custodied truth to meet a quota. |

## 9. Finite resource accounting and complexity

Let:

- `H` = bounded Head count;
- `R` = bounded typed Root count;
- `Q` = bounded active custody count;
- `E_v` = entries in the retired complete payload;
- `V` = its logical/allocated bytes relevant to filesystem reclamation;
- `T` = bounded staging transaction count;
- `D_n`, `D_b` = cleanup-debt item and byte totals;
- `K_clean` = maximum items/bytes per cleanup batch; and
- `M_ret`, `F_ret`, `W_ret` = retirement memory, FD, and worker caps.

| Operation | Worst-case time | I/O | Space/resources |
|---|---:|---:|---:|
| Exact final reachability | `O(H + R + Q)` | Reads all bounded reference/custody metadata; accepted payload bytes read `0` | streaming record buffer within `M_ret`, `F_ret`, one authority holder |
| Detach complete closure | `O(1)` conceptual namespace/control transition plus qualified fence | Bounded metadata writes; payload content read/write/copy `0/0/0` | one retirement record/temp as selected |
| Physical reclamation | `O(E_v + filesystem_reclaim(V))` | Metadata updates and physical reclamation are filesystem-dependent; content need not be read or copied | bounded FDs/workers and `K_clean` batch |
| Staging/debt scan | `O(T + D_n)` plus artifact bytes needed for safe classification | bounded metadata/integrity reads; deletion work proportional to staged entries/bytes | `M_ret`, `F_ret`, `W_ret`, finite quarantine/debt |

`H`, `R`, `Q`, `T`, `D_n`, `D_b`, worker queues, retries, and batch time are
hard-bounded. If exact validation cannot finish inside the admitted envelope,
retirement returns `LimitExceeded` and preserves the closure. Debt saturation
backpressures new staging/admission and may block readiness; it never converts
approximate liveness into authority.

## 10. Security and path obligations

- Validate every typed Version lookup, Head selector, Root key, custody token,
  transaction, and retirement item against schema/generation/bounds.
- Resolve accepted, staging, and retirement items beneath distinct anchored
  namespaces; reject symlinks, traversal, hard-link escape, mount crossing,
  special nodes, aliases, and unknown entries.
- Treat missing/unreadable/corrupt Head/Root/custody state as “cannot prove
  unreachable,” not as absence.
- Do not recursively remove a path derived from untrusted text. The selected
  deletion primitive must remain anchored to one validated transaction or
  detached closure and never broaden to the store root.
- Do not expose payload contents or host paths in metrics/quarantine logs.
- Prevent cleanup workers from becoming reference writers, AcceptedBinding
  issuers, or runtime-effect owners.

## 11. Observability and test seams

Required diagnostic facts include retirement candidates/outcomes, exact
Head/Root/custody records examined, scan/gate/reservation time, detached
count/bytes, physical reclaim progress, staging/orphan count/age/bytes,
cancellation side, quarantine, cleanup retries, debt high-water marks, and
backpressure/readiness consequences.

Required tests:

- each single Head, Root, and custody form independently prevents retirement;
- concurrent final Root removal/create and concurrent read capture have no
  use-after-retire or missed reachability;
- concurrent equal admission cannot reuse a closure during/after unsafe detach;
- corrupt/unreadable/over-limit reference or custody fails deletion closed;
- OCC-loser orphan passes the same exact final check;
- cancellation and crash at every detach/reclaim boundary are idempotent;
- cleanup saturation blocks new debt rather than deleting live truth;
- restart recognizes detached and partially reclaimed whole closures; and
- diagnostic hints/cached counts are corrupted in tests and never authorize
  deletion.

Observability may report candidates and debt but cannot mark unreachable,
detach, reclaim, create custody, or keep a Version alive.

## 12. Details Phase 03 may still select

Phase 03 selects exact record enumeration/indexing, target-reservation and gate
order, retirement marker/detach/fence, grace policy, custody forms, quarantine,
cleanup progress, batching, limits, backpressure, and diagnostics.

It may not replace exact final Head/Root/custody validation with persistent
refcount authority, approximate age, or tracing object-graph GC; it may not
delete sub-Version shared objects or mutate an accepted closure in place.

## 13. `REOPEN_PHASE_01` conditions

Reopen Phase 01 with the exact failed rule if:

- exact bounded Head/Root reachability plus custody cannot determine safe
  whole-Version retirement;
- one transition authority and target reservation cannot close reference,
  admission, and last-reader races;
- safe retirement requires persistent refcount authority, a tracing object
  graph, sub-Version shared-object collection, or another writer/service;
- cleanup/recovery debt cannot be bounded without deleting authoritative truth;
  or
- the complete payload family cannot be detached/reclaimed without mutating
  still-accepted data.

Exact retirement mechanics that preserve this model remain `OPEN_WITHIN_R0`.
