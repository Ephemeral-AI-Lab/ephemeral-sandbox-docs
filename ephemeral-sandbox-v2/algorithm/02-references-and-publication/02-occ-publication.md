# 02.02 — OCC publication

## 1. Purpose and owning phase

**Owners:** Application owners authorize and order the request; Phase 03
LayerStack-0 admits the Candidate and owns the Head transition.  
**Purpose:** Publish an admitted complete Version to one existing Head through
exactly one optimistic-concurrency-control decision and one conditional
complete Head-record replacement. Initial Head creation and exact Head removal
are lifecycle operations under this same reference transition authority; they
are defined by [Reference EphCoW](01-reference-ephcow.md), not by a second
initializer or cleanup writer.

There is one state-changing Head linearization point in the entire package.
Stale writers lose without silent merge, rebase, expected-Head refresh, or retry
against a newly observed Head.

## 2. Evidence status

- `SOURCE-VERIFIED`: current e497 source places application ordering above the
  existing low-level durable-history owner and contains a writer-lock plus
  atomic-write/durability primitive family. Current auto-merge behavior is
  legacy behavior to remove, not V2 proof.
- `SPIKE-VERIFIED`: none; V2 OCC, same-Version, lost-response, and crash-prefix
  tests have not run.
- `INFERRED`: the expected tuple, sole transition gate, one whole-record
  replacement, and clean stale outcome are selected R0 design contracts.
- `OPEN`: Phase 03 selects record/fence/lock mechanics and same-Version behavior;
  Phase 04 selects API/idempotency integration. `DEC-017` and `DEC-018` remain
  `OWNER_DEC_OPEN`.

## 3. Responsibility split

### Application owners

- identify the typed Head selector;
- capture the expected complete Head value before ordering the mutation;
- decide authorization and the authorization/revoke cutoff;
- decide request order, application idempotency, disclosure, MCTS/rollout
  policy, scores, and whether a stale result should trigger a new user-visible
  attempt;
- capture one complete Candidate from the runtime-owned Workspace; and
- pass the unchanged expected tuple to LayerStack-0.

### LayerStack-0

- validate/admit the Candidate as a complete immutable AcceptedVersion;
- invoke the LayerStack-0 admission boundary to issue or revalidate the target
  AcceptedBinding;
- serialize Head create/replace/remove, fixed-Root create/remove, and
  retirement transitions through the one process/filesystem-exclusive
  transition authority;
- compare the complete expected tuple to the current complete Head;
- make at most one conditional complete Head-record replacement;
- return a typed stale/same/success/error result; and
- account for an accepted payload left unreachable by a losing publication.

LayerStack-0 does not know authorization policy, rollout scores, branch search
strategy, or when the application should start a brand-new attempt.

### Complete Head lifecycle under this authority

| Lifecycle intent | Complete expected state | Semantic operation | Linearization and durable success |
|---|---|---|---|
| Initialize a Branch Head | `Expected::Absent` | `CreateHeadIfAbsent` | conditional complete-record creation; `APPLIED` only after the shared reference fence |
| Publish, advance, or roll back a Branch Head | `Expected::Exact(expected_head)` | `ReplaceHead` | the sole conditional complete-record Head replacement; `APPLIED` only after the shared reference fence |
| Destroy a Branch Head | `Expected::Exact(expected_head)` | `RemoveHead` | conditional removal of the exact complete record; `APPLIED` only after the shared reference fence |

All three run through the same `ReferencePlane`, transition gate, complete
comparison law, conditional transition family, outcome taxonomy, authoritative
read-back, recovery, custody, and retirement integration specified by
[the lifecycle contract](01-reference-ephcow.md#4-shared-transition-and-read-back-law).
Head creation/removal do not create additional OCC points: only replacement is
a Head movement, while the three record-state transitions share one authority.

## 4. Contract

Conceptual names express responsibility and type flow, not selected Rust or
wire signatures.

### Inputs

- `TypedHeadSelector`.
- `ExpectedHead = { AcceptedBinding, HeadRevision }`, captured before the
  application orders the request.
- Either a bounded complete Candidate to be admitted or an AcceptedBinding
  already returned by ordinary admission.
- Optional application attempt correlation used only for existing API
  idempotency/diagnostics; it is not Version truth or another store authority.
- Finite admission, transition-wait, record, custody, and cleanup budgets.

### Preconditions

1. The application has made its currently required authorization and ordering
   decision; exact revoke-race semantics remain `DEC-018`.
2. The expected binding and revision came from one complete captured Head,
   rather than independently assembled fields.
3. A raw digest or `VersionId` is not accepted in place of a binding.
4. LayerStack-0 is ready, on the active store generation, and below all finite
   debt/resource bounds.
5. No caller expects LayerStack-0 to merge, rebase, refresh, score, or choose a
   different target.

### Outputs

One typed publication or read-only resolution result. A successful
state-changing output contains the complete new Head value; a stale output
contains only policy-allowed metadata and never a replacement side effect.

### Semantic outcomes

| Outcome | Publication meaning |
|---|---|
| `APPLIED` | The exact expected Head matched, the complete successor replaced it, and the reference fence completed. The result contains the new Head. |
| `ALREADY_EXISTS` | Reserved for absent-state Head creation; publication replacement does not return it. |
| `NOT_FOUND` | The exact replacement target Head is absent. No mutation occurred. |
| `CONFLICT` | Current Head differs from the complete expected Head, or the conditional replacement loses. No mutation occurred. |
| `INVALID_BINDING` | Admission failed or the admitted target cannot be revalidated; raw-ID fallback is forbidden. |
| `CORRUPT` | A Head, expected record, binding, generation, or transition artifact is invalid or ambiguous. Fail closed. |
| `OUTCOME_UNKNOWN` | Replacement/fence/acknowledgement may have crossed the transition boundary; mandatory authoritative read-back is non-mutating. |
| `INTERNAL_FAILURE` | A bounded cancellation, readiness, resource, lock, fence, or I/O failure not safely classifiable above. No guessing is permitted. |

An API may expose `SameVersion`, desired-postcondition-observed, or
desired-postcondition-not-observed details, but these are result details or
read-back observations rather than replacements for the eight lifecycle
outcome distinctions.

## 5. Composed algorithm

```text
application_publish(selector, expected, workspace, request_context):
    application.capture_expected_as_one_head_record(expected)
    application.authorize_and_order(request_context, expected)
    candidate := runtime.capture_complete_candidate(workspace, finite_budget)

    admitted := LayerStack0.admit_complete_version(candidate)
    if not admitted:
        return INVALID_BINDING or the exact CORRUPT/INTERNAL_FAILURE class

    # A bounded operation-local use guard may retain the binding until the
    # transition decision. Exact representation is Phase 03-owned.
    return LayerStack0.publish_accepted(
        selector, expected, admitted.binding, admitted.operation_guard)
```

```text
publish_accepted(selector, expected, target_binding, operation_guard):
    validate typed selector, expected tuple, revision domain, and request bounds
    cancellation_checkpoint_or_return(INTERNAL_FAILURE(cancelled_before_linearization))

    acquire the single process/filesystem-exclusive LayerStack-0 transition gate
    target := LayerStack0Admission.revalidate_existing_binding_metadata(
                  target_binding, accepted_metadata/custody)
    if target invalid:
        release gate; return INVALID_BINDING

    current := read and validate one complete Head record

    if current.binding != expected.binding
       or current.HeadRevision != expected.HeadRevision:
        release gate
        return CONFLICT(allowed_metadata(current))

    if current.binding names same AcceptedVersion as target.binding:
        apply the one selected same-Version rule:
            revision advance -> one conditional whole-record replacement; or
            no-op -> no record mutation
        release gate
        return APPLIED(next) after fenced revision advance, or the selected
               comparison-only no-op detail without claiming APPLIED

    next := complete checksummed/generation-fenced Head record(
                binding = target.binding,
                HeadRevision = checked_monotone_successor(current.HeadRevision))

    conditionally replace exactly this one complete Head record,
        requiring on-disk current still equals expected
    apply Phase 03-qualified durable-reference fence
    release gate
    return APPLIED(next)
```

Unknown-outcome resolution is a distinct non-mutating seam. It is never an
alternate branch inside `publish_accepted`:

```text
resolve_unknown_publication(selector, expected, target_binding):
    validate typed selector, expected tuple, revision domain, and request bounds
    target := LayerStack0Admission.revalidate_existing_binding_metadata(
                  target_binding)
    if target invalid: return INVALID_BINDING
    current := LayerStack0.read_and_validate_complete_head(selector)
    if current.binding == target.binding
       and current.HeadRevision == checked_successor(expected.HeadRevision):
        return read_back(desired_postcondition_observed, current)
    return read_back(desired_postcondition_not_observed,
                     allowed_metadata(current))
```

`desired_postcondition_observed` proves only that the intended postcondition is
now true.
It cannot attribute the replacement to this caller when concurrent callers had
the same expected tuple and target. A direct retry of `publish_accepted` with
the old expected tuple is stale after any caller wins.

The application may decide after `CONFLICT` to begin a new operation.
That new operation must recapture and reauthorize explicitly; it is not a retry
of the stale transition.

## 6. Visibility and the one Head linearization point

The sole state-changing OCC linearization point is:

```text
conditional complete Head-record replacement while the sole transition gate is held
```

The expected value includes both AcceptedBinding and `HeadRevision`. Comparing
only a revision or only a target ID is invalid. Preparing a record, admitting a
payload, acquiring a lock, validating authorization, or emitting a metric is
not the Head linearization point.

Success is acknowledged only after the Phase 03-qualified reference durability
fence. A crash may therefore produce prior truth, complete new truth, or
fail-closed recovery, never a fieldwise hybrid. A selected same-Version no-op
has no state-changing replacement; its operation point is the successful
expected/current comparison under the gate.

## 7. Stale, retry, and orphan behavior

### Stale writer

On any expected binding/revision mismatch, LayerStack-0:

1. leaves the Head untouched;
2. does not compare Workspace deltas, merge trees, rebase facts, recapture the
   current Head, or update the expected tuple;
3. releases transition and operation custody; and
4. returns one typed stale result.

### Idempotent retry seam

- Admission retry is idempotent through occupied-ID full canonical comparison.
- If publication definitely failed before replacement, the same expected tuple
  may be retried.
- If acknowledgement was lost, the application invokes the distinct read-only
  resolver. The exact intended successor—target binding at
  `expected.HeadRevision + 1`—reports the desired postcondition observed; any
  other Head reports it not observed. Neither result performs a replacement or
  claims which concurrent caller published.
- A direct publication retry with the old expected tuple is stale once any
  caller has advanced the Head. The application must not disguise a new
  expected tuple as the old retry.
- If product APIs require stronger per-request replay or result retention,
  Phase 04 must isolate it at the existing application/API seam. It cannot add
  a second Head authority or durable truth.

### Accepted orphan

Candidate admission may succeed before a stale/cancelled publication. The
complete accepted payload remains valid but may be unreachable by any Head or
Root after bounded operation custody is released. It is charged as orphan
cleanup debt and handled by
[retirement and cleanup](../04-durability-and-lifecycle/02-retirement-and-cleanup.md). A stale writer
never publishes merely to avoid that debt.

## 8. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal | Application authorizes/orders; admission yields a binding; expected tuple matches; one whole Head replacement becomes durable. |
| Concurrent writers | Gate serialization plus conditional expected comparison permits at most one winner for a captured revision. All others are stale. |
| Concurrent same target | One wins and every other state-changing call is stale; read-only resolution may observe the desired Head without attributing the winner. |
| Retry | A direct call reusing an old expected tuple is stale after a winner. Resolve an unknown outcome through the separate read-only seam; never refresh internally. |
| Cancellation before point | No Head mutation; release guard/gate; accepted target may become bounded orphan debt. |
| Cancellation after point | Do not roll back the new Head. Return `APPLIED` if durably known, otherwise `OUTCOME_UNKNOWN` and resolve by complete read-back. |
| Crash | [Recovery](../04-durability-and-lifecycle/01-durability-and-recovery.md) admits prior or complete new Head, quarantines ambiguity, and handles private records/orphans idempotently. |
| Cleanup | Release operation custody; remove record temporaries in bounded recovery; retire unreachable accepted orphans only after exact final revalidation. |

## 9. Finite resource accounting and complexity

Let `A_admit` denote the Candidate admission costs from
[complete Version admission](../01-identity-and-admission/02-complete-version-admission.md), `R_head`
the bounded complete Head-record bytes, `L_gate` the bounded transition wait,
and `O_debt` the finite accepted-orphan allowance.

| Path | Worst-case time | Data I/O | Space/resources |
|---|---:|---:|---:|
| Full Candidate publication | `A_admit + O(1) + L_gate` | Admission byte I/O plus `O(R_head)` reference metadata read/write; no payload I/O inside the Head transition | Admission staging plus one record temp, one gate holder, bounded operation custody |
| Publish already accepted | `O(1) + L_gate` | `O(R_head)` metadata | `O(R_head)` memory/temp, finite descriptors |
| Stale after admission | `A_admit + O(1) + L_gate` | Admission I/O plus Head metadata read; Head write `0` | Up to one accepted orphan charged to `O_debt` |
| Lost-response resolution | `O(1) + L_gate` | One complete Head metadata read; replacement write `0` when exact successor exists | Bounded record buffer |

Lock wait, request size, record size, admission workers, operation custody, and
orphan count/bytes are finite. Exhaustion returns backpressure or a typed error
before unsafe work. Exceeding orphan debt can stop new admission/publication
until bounded cleanup progresses; it cannot weaken OCC.

## 10. Security and validation obligations

- Treat selector, expected record, revision, binding, request correlation, and
  Candidate as untrusted at their respective boundaries.
- Validate typed selector grammar without traversal or namespace aliasing.
- Revalidate both expected and target AcceptedBindings; raw IDs and caller-made
  capability fields are rejected.
- Check revision successor overflow and reject unsupported/corrupt generations.
- Keep the application authorization result outside canonical identity and
  store records. LayerStack-0 cannot compensate for a missing application
  authorization policy, but it always enforces OCC and binding integrity.
- Bound stale-result disclosure and diagnostics according to application policy.
- `DEC-017` does not authorize sessionless mutation here; the owner may reject
  it or route a bounded complete Candidate through this ordinary algorithm.
- `DEC-018` does not pick a revoke-race result here; the owner decides the
  application cutoff while this one OCC point remains mandatory.

## 11. Observability and test seams

Diagnostics include authorization-seam outcome class (without becoming its
authority), admission outcome, expected/current revision relation, gate wait,
replacement attempt count, same-Version outcome, stale count, lost-response
resolution, accepted-orphan bytes/count, cancellation side, and recovery
classification.

Required tests:

- two writers with one expected tuple yield exactly one replacement and one
  stale result;
- expected binding mismatch with matching revision is stale;
- expected revision mismatch with matching binding is stale;
- no merge/rebase/recapture call occurs on stale paths;
- same-Version behavior is exactly the Phase 03-selected rule;
- response loss before and after the replacement resolves without double
  advance;
- admission success plus stale/cancel yields bounded orphan debt;
- corrupt/dangling binding, revision overflow, lock timeout, ENOSPC, and crash at
  every prefix fail closed; and
- reference Head-transition payload byte counters remain `0/0/0`, while
  admission byte costs remain separately visible.

Observers cannot acquire the gate, decide stale/success, advance a Head, retain
an orphan, or authorize a request.

## 12. Details owning phases may still select

Phase 03 selects the exact complete Head record, checksum/generation, lock,
filesystem profile, fence, same-Version rule, operation custody, recovery,
limits, and diagnostics. Phase 04 selects application API and idempotency
spellings and integrates owner decisions without changing OCC.

Neither phase may add automatic stale merge/rebase, a second Head writer, a
second mutation point, a raw-ID Head, or policy/scoring inside LayerStack-0.

## 13. `REOPEN_PHASE_01` conditions

Reopen Phase 01 with the exact failure if:

- the existing application/LayerStack-0 dependency direction cannot keep
  authorization/order outside while enforcing OCC inside;
- a required Head update cannot be expressed as one conditional complete-record
  replacement under one transition authority;
- stale correctness requires automatic merging, rebasing, or multiple durable
  linearization points;
- finite accepted-orphan handling cannot preserve admission/publication
  separation;
- no supported filesystem can expose prior or complete new Head truth; or
- `DEC-017` or `DEC-018` requires accepted-payload mutation, another writer,
  joint durable authorization/storage authority, or another representation.

Record, fence, same-Version, and API details that satisfy the contract remain
`OPEN_WITHIN_R0`.
