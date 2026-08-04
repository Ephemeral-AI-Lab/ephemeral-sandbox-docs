# 02.03 — Composed Candidate-to-Head publication pipeline

## 1. Purpose and owning phases

**Owners:** Application owners authorize and order publication and capture the
expected Head. Existing runtime-effect owners capture a complete Candidate from
an isolated Workspace. Phase 02 constrains identity. Phase 03 LayerStack-0 owns
admission, AcceptedBindings, and the one OCC Head transition. Phase 04 owns the
application/API seam.  
**Purpose:** Demonstrate the complete publication flow while keeping Candidate
capture, complete-Version admission, and constant-sized Head selection as
separate authority, visibility, failure, and cost scopes.

This file composes, but does not replace,
[complete Version admission](../01-identity-and-admission/02-complete-version-admission.md)
and [OCC publication](02-occ-publication.md).

## 2. Evidence status

- `SOURCE-VERIFIED`: the sealed e497 source supports the selected ownership and
  dependency direction; current product behavior is not a V2 publication proof.
- `SPIKE-VERIFIED`: none; no V2 end-to-end publication, contention, or
  lost-acknowledgement test has run.
- `INFERRED`: the two publication modes, admission-before-selection ordering,
  unchanged expected tuple, single transition gate, and orphan handling are R0
  design contracts.
- `OPEN`: Phase 02 selects exact identity mechanics; Phase 03 selects records,
  fences, gate, same-Version semantics, custody, and bounds; Phase 04 selects
  API/idempotency spelling. `DEC-017` and `DEC-018` remain `OWNER_DEC_OPEN`.

## 3. End-to-end authority flow

```text
application authorizes and captures ExpectedHead
  {AcceptedBinding, HeadRevision}
        |
        v
runtime-owned isolated Workspace
        |
        | capture complete portable Candidate
        v
Candidate -> VersionId -> AcceptedVersion -> AcceptedBinding
        |          LayerStack-0 admission
        v
single LayerStack-0 transition gate
        |
        | compare complete ExpectedHead
        | conditionally replace one complete Head record
        v
Head {AcceptedBinding, monotone HeadRevision}
```

There are two valid modes:

```text
MODE A — accepted-only publication
  AcceptedBinding -> OCC Head transition

MODE B — full Candidate publication
  Workspace -> Candidate -> admission -> AcceptedBinding -> OCC Head transition
```

Mode A moves no payload bytes. Mode B may read/write a complete Candidate and
payload during capture/admission, but its final Head transition still moves no
payload bytes. Reporting must not merge those scopes.

## 4. Contract

Conceptual names express responsibilities and typed flow, not exact APIs.

### Inputs

- `TypedHeadSelector`.
- `ExpectedHead = { AcceptedBinding, HeadRevision }` captured as one complete
  Head before application ordering.
- Either:
  - an admission-issued/revalidated `AcceptedBinding`; or
  - a runtime-owned isolated Workspace from which a bounded complete Candidate
    can be captured.
- Application authorization/order context and optional correlation identifier.
- Finite Candidate, admission, transition-wait, record, custody, staging,
  orphan-debt, memory, FD, worker, deadline, and cleanup budgets.

### Preconditions

1. Application authorization and request ordering have run at the existing
   seam; the owner has not delegated policy or MCTS scoring to LayerStack-0.
2. `ExpectedHead` fields were captured together and remain unchanged throughout
   this attempt.
3. A raw digest or computed `VersionId` cannot substitute for either binding.
4. Workspace capture is complete and isolated from concurrent mutation under
   the runtime owner's selected contract.
5. LayerStack-0 is ready on the active generation and below finite debt limits.
6. The caller does not request merge, rebase, expected-Head refresh, or
   accepted-payload mutation.

### Outputs and typed outcomes

| Outcome | Meaning |
|---|---|
| `Published(new_head, admitted_or_existing)` | Target was accepted, expected Head matched, and one complete successor Head became durably visible. |
| `SameVersion(result)` | Expected matched and target names the same AcceptedVersion; Phase 03's selected no-op or revision-advance rule applied. |
| `StaleExpectedHead(metadata)` | Binding, revision, or both did not match; Head write count is zero. |
| `CandidateCaptureFailed(reason)` | No complete Candidate was produced; admission and Head remain unchanged. |
| `AdmissionFailed(reason)` | Candidate did not yield an AcceptedBinding; Head remains unchanged. |
| `TargetUnavailable` | Existing/admitted binding failed transition-time revalidation. |
| `CancelledBeforeHeadPoint` | Cancellation occurred before the Head replacement; an admitted target may become bounded orphan debt. |
| `OutcomeUnknown` | Head replacement may have crossed its point but acknowledgement was lost; invoke the separate read-only resolver. |
| `DesiredHeadObserved(head)` | Read-only resolution found exactly `(target binding, expected revision + 1)`; it does not attribute the winner. |
| `DesiredHeadNotObserved(metadata)` | Read-only resolution did not find the exact intended successor and mutated nothing. |
| `StoreNotReady` | Recovery, migration fence, corruption, unsupported filesystem, or resource/debt limit prevents safe work. |

## 5. Composed algorithm

```text
publish_from_workspace(selector, expected, workspace, context, budgets):
    application.capture_expected_as_one_complete_head(expected)
    application.authorize_and_order(context, expected)

    candidate := runtime.capture_complete_candidate(workspace, budgets.capture)
    if candidate failed:
        return CandidateCaptureFailed(candidate.reason)

    admitted := LayerStack0.admit_complete_version(candidate, budgets.admission)
    if admitted failed:
        return AdmissionFailed(admitted.reason)

    return publish_accepted_target(
        selector, expected, admitted.binding,
        admitted.operation_guard, budgets.transition)
```

```text
publish_existing_binding(selector, expected, target_binding, context, budgets):
    application.capture_expected_as_one_complete_head(expected)
    application.authorize_and_order(context, expected)
    return publish_accepted_target(
        selector, expected, target_binding,
        bounded_operation_guard, budgets.transition)
```

```text
publish_accepted_target(selector, expected, target, guard, transition_budget):
    validate selector, complete expected tuple, target binding, and bounds
    cancellation_checkpoint_or_return(CancelledBeforeHeadPoint)

    acquire the single process/filesystem-exclusive LayerStack-0 transition gate
    revalidate target through the admission-owned verifier
    read and validate one complete current Head record

    if current.binding != expected.binding
       or current.HeadRevision != expected.HeadRevision:
        release gate and guard
        charge admitted unreachable target as bounded orphan debt if applicable
        return StaleExpectedHead(allowed_metadata(current))

    if current and target name the same AcceptedVersion:
        execute exactly the Phase 03-selected same-Version rule
        release gate and guard
        return SameVersion(result)

    next := complete Head(target, checked_successor(current.HeadRevision))
    conditionally replace exactly one complete Head record,
        requiring on-disk current still equals expected
    apply the Phase 03-qualified reference durability fence
    release gate and guard
    return Published(next)
```

Unknown-outcome resolution is separate and non-mutating:

```text
resolve_publication(selector, expected, target):
    validate/revalidate typed inputs
    current := read and validate one complete Head
    if current.binding == target
       and current.HeadRevision == checked_successor(expected.HeadRevision):
        return DesiredHeadObserved(current)
    return DesiredHeadNotObserved(allowed_metadata(current))
```

The resolver never retries publication, refreshes `expected`, or claims which
of several identical concurrent callers performed the replacement.

## 6. Visibility and the single Head linearization point

The pipeline has distinct points:

1. Candidate capture completion: runtime-private, not accepted or selected.
2. AcceptedVersion visibility: one complete payload closure is durably admitted.
3. AcceptedBinding issuance/revalidation: admission-owned capability evidence.
4. **The sole Head OCC linearization point:** conditional replacement of one
   complete Head record while the one transition gate is held.
5. Success acknowledgement: after the Phase 03-qualified Head durability fence.

Only point 4 changes selected Head truth. Admission success does not select the
Version. A Root operation has its own complete-record visibility but is not
another Head point. A same-Version no-op has no state-changing replacement.

## 7. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal accepted-only | Revalidate binding, compare expected Head, replace one record, return success; payload I/O is `0/0/0`. |
| Normal full Candidate | Capture and admit a complete Version, then perform the same accepted-only transition; costs stay scope-separated. |
| Concurrent writers | For one expected Head state, at most one state-changing caller wins; every later gate holder is stale. |
| Concurrent same target | One caller wins; others are stale. A resolver may observe the desired Head without publisher attribution. |
| Retry before known replacement | Reusing the unchanged expectation is valid; it becomes stale if another call already won. |
| Lost response | Invoke read-only resolution. Never publish internally with a refreshed expectation. |
| Cancellation before admission | Release private capture/staging; no accepted or Head effect. |
| Cancellation after admission, before Head point | Head stays unchanged; release guard and charge unreachable accepted target as bounded orphan debt. |
| Cancellation after possible Head point | Never roll back blindly; return success if known, otherwise unknown and classify through complete read-back. |
| Crash | Recovery exposes the prior complete Head or the complete replacement, or fails startup closed. An accepted-but-unpublished Version remains bounded orphan debt; no recovery path silently merges, rebases, or refreshes the expected tuple. |
| Cleanup | Remove private staging and retire accepted orphans only after exact Head/Root/custody revalidation under transition authority. |

No stale or cancelled path publishes merely to avoid orphan debt.

## 8. Finite resources and complexity

Let `A_capture` be bounded Candidate capture cost; `A_admit` be complete-Version
admission cost; `R_head` be the maximum complete Head-record bytes; `L_gate` be
bounded transition wait; `O_debt` be finite orphan count/bytes; and use `B`,
`E`, `V`, `P_path`, and `Ops_fs` as defined in the resource model.

| Scope/path | Worst-case time | Payload/data I/O | Peak resources |
|---|---:|---:|---:|
| Accepted-only publication | `O(1) + L_gate + fence` | Head metadata `O(R_head)`; payload `0/0/0` | one gate holder, `O(R_head)` memory/temp, bounded custody/FDs |
| Full Candidate publication | `A_capture + A_admit + O(1) + L_gate + fence` | capture/admission may read/write `O(B + V)`; Head scope payload `0/0/0` | bounded capture/admission staging, memory, FDs, workers, guard |
| Concrete canonical model | `O(B + P_path + E log E + V + Ops_fs + L_id + L_gate)` | complete Candidate/payload byte terms plus `O(R_head)` metadata | `O(S_tx + M_order + w*b + R_head)` under selected caps |
| Stale accepted-only | `O(1) + L_gate` | one Head metadata read; Head/payload writes `0/0` | bounded record/custody only |
| Stale after new admission | `A_capture + A_admit + O(1) + L_gate` | admission I/O applies; Head write and Head-scope payload I/O `0` | at most one charged accepted orphan per attempt |
| Read-only resolution | `O(1)` plus bounded access wait | one complete Head metadata read; writes `0` | `O(R_head)` |

`O(1)` means bounded record work, not zero syscalls, wait, or durability cost.
All queues, waits, staging, memory, descriptors, workers, operation custody, and
orphan debt have per-operation and global caps. Exhaustion returns typed
backpressure/failure before unsafe visibility and never bypasses OCC.

## 9. Security and path validation

- Validate selector grammar, complete expected tuple, revision successor,
  generation, binding integrity, Candidate paths/facts, and all checked sizes.
- Capture the Workspace through a capability-scoped runtime interface; prevent
  path traversal, ambient symlink following, concurrent mutation, special-file
  abuse, and host/runtime-private facts entering canonical identity.
- Revalidate target bindings only through LayerStack-0 admission-owned code.
- Bound application error disclosure, correlation cardinality, stale metadata,
  logs, and traces; do not expose paths or contents.
- Keep authorization and revoke-race decisions at the application seam.
  `DEC-017` and `DEC-018` remain open; neither permits bypassing admission/OCC.

## 10. Observability and demonstration seams

Emit separate operation scopes for capture, canonicalization, admission,
binding, gate wait, Head read/replace/fence, resolution, custody release, and
orphan cleanup. Required facts include:

- expected/current/target relation without raw secrets;
- capture/canonical/payload bytes and entries;
- admission new/equal/collision outcome;
- accepted-only versus full-Candidate mode;
- gate wait, replacement attempts, Head record bytes, stale/same/published;
- reference-scope payload read/write/copy counters `0/0/0`;
- cancellation side, unknown-outcome resolution, and orphan debt; and
- bounded memory, FD, worker, staging, and queue high-water marks.

Required tests include normal paths for both modes; target/expected corruption;
two and many writer contention; same-target contention; same-Version selected
behavior; cancellation/crash at every boundary; lost acknowledgement before and
after replacement; admission success followed by stale; resource exhaustion;
and a call-graph/tracing assertion that Head transition cannot open payload.

Observers cannot authorize, issue/revalidate a binding, hold the transition
gate, advance a Head, resolve equality, or delete an orphan.

## 11. Details owning phases may still select

Phase 02 selects Candidate/canonical mechanics. Phase 03 selects record, gate,
fence, same-Version, custody, staging, orphan, recovery, and finite-limit
mechanics. Phase 04 selects API/idempotency/correlation spelling and integrates
owner decisions at existing seams.

No owning phase may collapse Candidate identity into reference authority, add a
second Head mutation, hide admission byte I/O under reference `0/0/0`, mutate an
accepted payload, or silently merge/rebase a stale writer.

## 12. `REOPEN_PHASE_01` conditions

Reopen with the exact architecture-changing failure if:

- Candidate capture cannot produce bounded complete portable facts without
  making runtime-private state Version identity;
- admission and publication cannot remain separate under the existing direct
  ownership direction;
- one conditional complete Head replacement under one transition authority
  cannot implement required stale-writer semantics;
- finite orphan handling cannot preserve clean stale/cancellation behavior;
- a product hard rule requires accepted-payload mutation or automatic
  merge/rebase in LayerStack-0; or
- a selected, qualified hard performance/resource target proves this composed
  R0 path cannot qualify without another writer, service, or storage family.
