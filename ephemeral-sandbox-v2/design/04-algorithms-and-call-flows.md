# LayerStack-0 algorithms and call flows

Status: **PHASE 01 ALGORITHM CONTRACT — exact Phase 02/03 mechanics pending**  
Owners: Phase 02 for pure identity steps; Phase 03 for durable store steps  
Authority: product [hard rules](../PRD.md#hard-rules-must-never-break) and the selected
[R0 architecture](../architecture_design.md)

## 1. Purpose and status notation

This document specifies the algorithm families and observable state-machine
behavior that R0 implementations must preserve. It is detailed enough to guide
implementation and tests, but intentionally does not select the exact canonical
codec/hash or filesystem `fsync`/rename sequence.

| Label | Meaning |
|---|---|
| `LOCKED_PHASE_01` | Required semantic algorithm or linearization boundary |
| `SELECT_IN_PHASE_02` | Pure identity grammar, digest, validation, and streaming detail |
| `SELECT_IN_PHASE_03` | Exact filesystem, record, locking, durability, and bounded-limit detail |
| `OWNER_DEC_OPEN` | Product-owner behavior remains open behind the fixed primitive |
| `REOPEN_PHASE_01` | New evidence changes ownership, storage family, writer count, or a hard rule |

The algorithms operate on the conceptual types in
[02-state-identity.md](02-state-identity.md) and
[03-state-store.md](03-state-store.md). Exact Rust names may differ.

## 2. Common invariants

Every algorithm preserves these invariants:

1. Selected Version truth is a complete immutable payload plus valid durable
   roots/heads; private staging is never selected truth.
2. `VersionId` is not an Accepted Version or accepted binding, and digest
   equality is not full canonical equality proof.
3. An occupied ID always triggers full canonical-byte comparison.
4. A root/head can name only a complete durable accepted binding.
5. A committed payload is never edited in place.
6. One store-owned transition gate serializes final selected-reference changes
   and final retirement checks.
7. Head publication has one OCC linearization point and stale never merges or
   rebases.
8. Reference-only operations never open or otherwise touch payload bytes.
9. Runtime effects and application/MCTS/auth policy remain outside storage.
10. Failure leaves prior truth, complete new truth, or bounded recognizable
    private/orphan debt; corruption or ambiguity fails closed.

## 3. Operation classes and authority points

| Operation class | Payload admission point | Selected-reference linearization | Payload I/O allowed? |
|---|---|---|---|
| Validate/canonicalize | None | None | Candidate/canonical bytes only |
| Admit candidate | Atomic accepted-payload visibility selected by Phase 03 | None | Yes, bounded complete candidate; full comparison when occupied |
| Publish candidate | May admit/reuse before final gate | One atomic complete head-record replacement | Yes before gate; head transition is metadata only |
| Accepted-reference lifecycle | Already accepted | One operation-appropriate atomic transition from Head create/exact replace/exact remove or fixed-Root create/exact remove; only a Head can be replaced | **No: read/write/copy = 0** |
| Capture/read | Already accepted | Custody acquisition serialized against retirement | Read-only accepted payload after capture |
| Recover | Revalidates existing accepted population | None; never invents truth | Bounded validation/cleanup as selected by Phase 03 |
| Retire | Already accepted | Final root/custody revalidation plus selected unlink point | No payload content read/copy; metadata/unlink only |
| Import | Calls ordinary admission | Calls the ordinary five-operation Head/fixed-Root authority | Same as ordinary APIs; no alternate path |

“Payload I/O” means bytes of accepted Version or Candidate content, including
hidden extraction, hashing, walking, canonical comparison, private payload
creation, copying, cloning, or materialization. Reference metadata I/O is
accounted separately.

## 4. Conceptual failure classes

Exact Rust enums are phase-local choices, but call sites and tests must be able
to distinguish the following outcomes:

| Class | Meaning and required safety behavior |
|---|---|
| `InvalidCandidate` | Malformed, ambiguous, incomplete, corrupt, or unsupported portable facts; no binding/reference change |
| `IdentityLimit` | Phase 02 finite validation/canonicalization bound exceeded; no partial identity accepted |
| `StoreLimit` | Phase 03 staging/population/custody/recovery bound exceeded; no reference change |
| `Collision` | Occupied `VersionId`, unequal full canonical bytes; no alias or reference change |
| `UnknownBinding` | Raw, missing, forged, wrong-generation, or no-longer-valid binding; cannot use reference path |
| `Stale` | Expected head/root token no longer matches; no merge/rebase or target mutation |
| `Missing` | Requested selector/root/payload is absent |
| `Corrupt` | Integrity, completeness, ID, reference, or durable record invariant failed; fail closed |
| `UnsupportedVersion` | Identity/store/control version cannot be interpreted safely |
| `UnsupportedFilesystem` | Configured filesystem cannot meet selected atomicity/durability assumptions |
| `ResourceExhausted` | Memory, disk/scratch, FD, worker, root, custody, or debt capacity unavailable |
| `IoOrDurability` | Required I/O/fence failed before an acknowledged transition |
| `AmbiguousCommit` | Implementation cannot prove caller-visible acknowledgement around a durable point; explicit recovery/re-resolution required |
| `ActiveReachability` | Retirement target is still rooted or under read custody |
| `StaleGeneration` | Migration/import call does not match the active monotone generation |

An implementation may use more precise variants. It must not collapse
collision into “already exists,” stale into automatic retry/merge, or
corruption into best-effort reconstruction.

## 5. A0 — validate and canonicalize complete candidate

Status: core semantics `LOCKED_PHASE_01`; exact grammar, digest, and constants
`SELECT_IN_PHASE_02`.

```text
function prepare_identity(untrusted_facts, identity_limits, canonical_sink):
    budget = identity_limits.start_accounting()
    validated = validate_complete_structure(untrusted_facts, budget)

    for entry in deterministic_canonical_order(validated, budget):
        reject_forbidden_or_unsupported_facts(entry)
        encoded = encode_unambiguous_versioned_entry(entry, budget)
        canonical_sink.write(encoded)
        digest.update(encoded)

    require_complete_state(validated)
    return CanonicalSummary(
        version_id = typed_domain_separated_digest(digest),
        bounded_counts = budget.final_counts()
    )
```

| Contract field | Requirement |
|---|---|
| Inputs | Untrusted complete portable candidate plus finite identity limits |
| Preconditions | None beyond a supported identity domain request |
| Output | Deterministic canonical stream and typed `VersionId` summary |
| Linearization/durable point | None; pure computation |
| I/O | Caller-supplied bounded canonical source/sink only; no store/mount/workspace I/O policy |
| Resource behavior | Streaming content; bounded ordering metadata, buffers, work, depth, entries, and bytes |
| Failures | Invalid/unsupported fact, ambiguity/duplicate, limit, corrupt input, canonical source/sink failure |
| Idempotency | Same qualified facts and version produce exactly the same bytes and ID |

Phase 02 selects whether deterministic ordering is produced by validated
ordered input, bounded in-memory metadata, a bounded external strategy, or
another pure mechanism. It may not rely on host enumeration order or unbounded
memory.

## 6. A1 — admit candidate

Status: semantics `LOCKED_PHASE_01`; exact transaction/layout/lock/fence steps
`SELECT_IN_PHASE_03`.

```text
function admit_candidate(candidate, identity_limits, store_limits):
    reservation = precharge(candidate, identity_limits, store_limits)
    txn = create_private_bounded_staging(reservation)

    try:
        summary = prepare_identity(candidate, identity_limits, txn.canonical_sink)

        occupant = lookup_accepted_occupant(summary.version_id)
        if occupant exists:
            equality = compare_full_canonical_bytes(txn, occupant, identity_limits)
            if equality == UNEQUAL:
                return Collision(summary.version_id)
            accepted = verify_and_capture_accepted_version(occupant)
            binding = issue_accepted_binding(accepted, active_generation)
            return AdmissionReceipt(accepted, binding, REUSED)

        result = coordinate_id_slot_and_recheck(summary.version_id)
        if result now has occupant:
            equality = compare_full_canonical_bytes(txn, result.occupant, identity_limits)
            if equality == UNEQUAL:
                return Collision(summary.version_id)
            accepted = verify_and_capture_accepted_version(result.occupant)
            binding = issue_accepted_binding(accepted, active_generation)
            return AdmissionReceipt(accepted, binding, REUSED)

        txn.build_complete_payload(candidate, summary)
        txn.validate_private_completeness()
        make_private_payload_complete_and_durable(txn)
        accepted = atomically_expose_one_accepted_version(txn, summary.version_id)
        make_admission_namespace_durable_as_required()
        binding = issue_accepted_binding(accepted, active_generation)
        return AdmissionReceipt(accepted, binding, NEW)
    finally:
        cleanup_private_txn_or_record_bounded_recovery_debt(txn, reservation)
```

`make_*`, `coordinate_*`, and atomic exposure above are obligations, not an
exact filesystem sequence. Phase 03 chooses them and proves their crash
prefixes.

| Contract field | Requirement |
|---|---|
| Inputs | Bounded complete portable candidate; caller does not assert acceptance |
| Preconditions | Ready active store generation and successful resource precharge |
| Output | `AcceptedVersion`, its store-accepted binding, plus `NEW` or `REUSED` |
| Admission visibility point | One atomic accepted-payload namespace transition selected by Phase 03 |
| Selected-reference point | None; admission never changes a root/head |
| Durable point | Complete payload and required metadata durable before accepted binding is returned |
| I/O | Candidate read/canonicalization; new complete payload write; occupied ID requires full canonical-byte reads/comparison |
| Resources | Precharged scratch/disk/memory/FD/work; one bounded transaction; deterministic cleanup |
| Failures | Identity, collision, store limit, ENOSPC/resource, corrupt occupant, unsupported version/profile, I/O/durability |
| Retry | Content-idempotent: equal candidate converges on the same accepted occupant |

### Concurrent admissions

- Equal candidates may both prepare privately, but after serialized ID-slot
  coordination they converge on one accepted payload and both receive that
  binding.
- Unequal canonical candidates forced to the same ID produce collision. A race
  cannot create two physical occupants or let either mismatch mutate a
  reference.
- A process crash may leave private staging or a complete unreferenced accepted
  payload. Both are bounded, recognizable, and safe because no incomplete
  payload can be named.

## 7. A2 — publish candidate with OCC

Status: semantics and sole head linearization `LOCKED_PHASE_01`; exact durable
record protocol `SELECT_IN_PHASE_03`.

```text
function publish_candidate(selector, expected_head, candidate):
    # Application already authorized, ordered, and captured expected_head.
    receipt = admit_candidate(candidate)

    replacement = HeadRecord(
        binding = receipt.binding,
        revision = next_monotone_revision(expected_head.revision)
    )

    with selected_state_transition_gate:
        current = reread_and_validate_complete_head(selector)
        if current != expected_head:
            return Stale(current)       # no merge, rebase, or head mutation

        prepare_complete_replacement_record(replacement)
        atomically_replace_complete_head(selector, replacement)
        satisfy_selected_reference_durability()
        return Published(receipt, replacement)
```

| Contract field | Requirement |
|---|---|
| Inputs | Authorized selector, expected complete `(binding, revision)`, complete candidate |
| Preconditions | Application ordering complete; expected binding is store-valid for the active generation |
| Output | Accepted binding plus new complete head/revision, or typed stale/failure |
| OCC linearization point | Exactly one atomic complete head-record replacement under the transition gate |
| Durable acknowledgement | Target payload already durable; new reference durability complete before success acknowledgement |
| I/O outside gate | Candidate/canonical/payload work, full occupied-ID comparison, staging, payload durability |
| I/O inside final gate | Bounded complete head/control metadata only; no candidate construction or payload comparison |
| Failures | Admission failures, stale, corrupt/unknown head, store limit, I/O/durability, explicit ambiguous commit if unavoidable |
| Retry | Reusing admission is safe; replay with consumed expected revision is stale or an explicitly defined same-Version result |

If admission succeeds but OCC is stale, the accepted payload may be
unreferenced. It becomes bounded retirement/recovery work. It is not rolled
back by mutating or partially deleting content while another admission/read may
use it.

Phase 03 may select whether a same-binding successful head transition advances
the revision or returns a defined no-op result. Either choice must retain
monotone OCC, explicit replay semantics, and zero payload I/O for the
accepted-binding path.

## 8. A3 — apply an exact reference lifecycle operation

Status: `LOCKED_PHASE_01`; exact record encoding remains
`OPEN_WITHIN_R0` in Phase 03. The canonical lifecycle contract is
[Reference EphCoW](../algorithm/02-references-and-publication/01-reference-ephcow.md).
A3 is a facade over that single reference authority, not a generic retargeting
primitive.

```text
function apply_reference_operation(operation):
    require operation in {
        CreateHeadIfAbsent(head_identity, Expected::Absent, new_binding),
        ReplaceHead(head_identity, Expected::Exact(expected_head), new_binding),
        RemoveHead(head_identity, Expected::Exact(expected_head)),
        CreateFixedRootIfAbsent(root_identity, root_kind,
                                Expected::Absent, binding),
        RemoveFixedRoot(root_identity, root_kind,
                        Expected::Exact(expected_root))
    }

    validate_typed_identity_expected_state_and_binding(operation)
    start_operation_io_counters()
    outcome = ReferencePlane.apply(operation)
    assert payload_bytes_read == 0
    assert payload_bytes_written == 0
    assert payload_bytes_copied == 0
    return outcome
```

| Contract field | Requirement |
|---|---|
| Inputs | One typed operation, its complete expected state, and an accepted binding where creation/replacement needs one |
| Mutation policy | Heads support create, exact replace, and exact remove; fixed typed Roots support create and exact remove only |
| Linearization and durability | Exactly the canonical Reference EphCoW operation's metadata commit point; required metadata/namespace fence completes before `APPLIED` |
| Outcomes | `APPLIED`, `ALREADY_EXISTS`, `NOT_FOUND`, `CONFLICT`, `INVALID_BINDING`, `CORRUPT`, `OUTCOME_UNKNOWN`, or `INTERNAL_FAILURE` |
| Retry/read-back | Same request and expectation is idempotent only as defined by the canonical operation; `OUTCOME_UNKNOWN` requires authoritative exact-record read-back before retry |
| Payload I/O | Accepted-reference payload read/write/copy is exactly `0/0/0`; binding validation, coordination, metadata I/O, fences, and later runtime materialization are separately nonzero |
| Custody/retirement | Successful creation adds reachability; successful removal drops one reachability edge and only schedules exact retirement revalidation |

There is no `move_reference` escape hatch and no generic Root update. A Branch
is represented by a Head. A Checkpoint is a fixed typed Root. Rollback replaces
the Branch Head by exact OCC; fork creates a new Branch Head if absent.

## 9. A4 — resolve and capture immutable read

Status: captured-Version semantics `LOCKED_PHASE_01`; custody representation
`SELECT_IN_PHASE_03`.

```text
function capture_read(selector_or_root, custody_limits):
    reserve_custody_capacity(custody_limits)

    with protocol_serialized_against_final_retirement:
        record = reread_and_validate_complete_reference(selector_or_root)
        binding = revalidate_accepted_binding(record.binding)
        custody = acquire_custody(binding)

    return CapturedRead(
        binding = binding,
        revision = record.revision_if_head,
        read_only_payload = open_immutable_payload(binding),
        custody = custody
    )

function release_read(captured):
    close_read_only_payload(captured)
    release_custody_repeat_safely(captured.custody)
```

| Contract field | Requirement |
|---|---|
| Inputs | Typed root/head selector and bounded custody request |
| Output | Captured binding/revision and read-only payload access protected by custody |
| Capture linearization | Custody acquisition protocol point serialized against final retirement |
| I/O | Bounded reference metadata then read-only payload bytes requested by caller |
| Concurrency | Later head moves do not redirect the captured read; retirement sees custody or loses final revalidation |
| Failures | Missing/corrupt/dangling reference, unknown binding/version, custody/resource limit, I/O |
| Retry | A fresh retry resolves a fresh point in time unless caller retains the prior capture |

A read-only path string without custody is insufficient if retirement can
unlink/reuse its namespace. Phase 03 must select a representation that closes
the root-removal/read-acquisition race without an unbounded lease population.

## 10. A5 — recover and establish readiness

Status: fail-closed prior-or-new behavior `LOCKED_PHASE_01`; validation order,
record formats, and bounded batch details `SELECT_IN_PHASE_03`.

```text
function recover_and_open(store_root, supported_profile, store_limits):
    verify_supported_filesystem_profile(supported_profile)
    acquire_exclusive_recovery_or_transition_authority()

    control = validate_store_version_generation_and_integrity(store_root)
    debt_budget = store_limits.start_recovery_accounting()

    for bounded recognizable staging item in recovery_scope(debt_budget):
        classify_staging(item)
        cleanup_or_quarantine_repeat_safely(item, debt_budget)

    for bounded accepted payload/reference population required for readiness:
        validate_versions_integrity_and_completeness(item, debt_budget)

    for each head and root:
        require complete integrity-checked record
        require target is one complete accepted binding in active generation

    if corruption, ambiguity, dangling truth, unsupported version/profile,
       or excessive debt:
        return ReadinessFailed(typed_diagnostic)

    return ReadyStore(active_generation, bounded_diagnostics)
```

| Contract field | Requirement |
|---|---|
| Inputs | Configured store root, supported filesystem profile, finite limits |
| Output | Ready active generation or fail-closed diagnostic |
| Linearization | None; recovery validates rather than inventing selected truth |
| I/O | Bounded metadata/payload-integrity work and recognizable cleanup selected by Phase 03 |
| Permitted truth | Prior valid record or complete new valid record only |
| Cleanup | Repeat-safe; bounded staging/orphan debt; no unbounded scanner or worker pool |
| Failures | Corrupt/torn/dangling/unknown version, collision ambiguity, unsupported filesystem, excessive debt, I/O/resource |
| Retry | Idempotent over the same durable bytes; cleanup/quarantine actions are repeat-safe |

Recovery never selects the “newest-looking” file, repairs a dangling head by
choosing a layer parent, discards a rooted payload silently, or treats metrics
and indexes as truth.

## 11. A6 — retire an unreachable accepted payload

Status: reachability and final-race semantics `LOCKED_PHASE_01`; custody/index
and bounded-scan detail `SELECT_IN_PHASE_03`.

```text
function retire_one(target_binding, retirement_budget):
    require_valid_accepted_binding(target_binding)
    precheck = bounded_reachability_check(target_binding, retirement_budget)
    if precheck.rooted_or_custodied:
        return Retained(ActiveReachability)

    with selected_state_transition_gate:
        exact = exact_revalidate_heads_roots_and_active_custody(
            target_binding,
            retirement_budget
        )
        if exact.rooted_or_custodied:
            return Retained(ActiveReachability)

        atomically_remove_accepted_payload_visibility(target_binding)
        satisfy_selected_retirement_durability()

    cleanup_remaining_private_metadata_repeat_safely()
    return Retired(target_binding)
```

| Contract field | Requirement |
|---|---|
| Inputs | Accepted target or one bounded sweep unit |
| Preconditions | Ready store; finite retirement budget |
| Retirement point | Selected atomic removal/unlink after exact final serialized revalidation |
| I/O | Reachability/custody metadata and unlink; no payload content comparison/copy required |
| Sources of reachability | Heads, typed roots, and active read custody |
| Failures/outcomes | Retained/active, deferred/limit, corrupt reachability, I/O/durability, retired |
| Retry | Repeat-safe; missing after completed retirement is a defined completed/already-retired result |

Persistent refcount/index data may be a reconstructible bounded hint only. It
cannot replace exact final revalidation or become selected truth.

## 12. A7 — temporary one-way legacy import

Status: one-writer/deletable shape `LOCKED_PHASE_01`; legacy decoding and
progress details belong to later migration phases.

```text
function import_selected_legacy_view(legacy_locator, expected_generation):
    require active_generation == expected_generation
    require legacy_mutating_ingress_is_fenced_read_only()

    legacy_view = decode_one_complete_selected_legacy_view(legacy_locator)
    portable_candidate = convert_to_complete_portable_facts(legacy_view)
    receipt = admit_candidate(portable_candidate)

    require active_generation == expected_generation
    reference_result = apply_normal_v2_root_or_head_primitive(receipt.binding)
    record_repeat_safe_migration_progress(reference_result)
    return reference_result
```

| Contract field | Requirement |
|---|---|
| Inputs | Temporary legacy locator, fenced monotone generation, bounded legacy selected view |
| Output | Ordinary V2 accepted binding/root/head outcome |
| Authority | Existing lifecycle owners fence writers; importer never becomes selected-Version authority |
| Linearization/durability | Exactly the ordinary admission/reference points; no migration-specific truth path |
| I/O | Legacy read plus normal complete candidate admission; no dual write |
| Failures | Stale generation, legacy decode, identity, collision, resource, OCC/stale, I/O/durability |
| Retry | Exact admission plus explicit progress/generation is repeat-safe |
| Deletion | Decoder, feature/target, config, tests, progress types, and call sites removed as one unit |

The observation window (`DEC-011`) changes deletion timing only. It never
permits legacy and V2 to remain writable concurrently.

## 13. A8 — failure cleanup

Status: bounded/idempotent semantics `LOCKED_PHASE_01`; exact ownership tables
and batch limits `SELECT_IN_PHASE_03`.

```text
function finish_operation(operation_state, outcome):
    close_owned_descriptors_and_handles(operation_state)
    cancel_and_join_owned_bounded_workers(operation_state)
    release_memory_fd_disk_and_worker_reservations(operation_state)

    if private_staging_is_safe_to_remove:
        remove_repeat_safely(operation_state.staging)
    else:
        record_recognizable_bounded_recovery_debt(operation_state.staging)

    never remove accepted payload based only on caller failure
    never roll back or rewrite a durable head heuristically
    emit bounded diagnostic counters(outcome)
```

Cleanup ownership must cover success, identity rejection, collision, stale OCC,
cancellation, timeout, panic/process kill, ENOSPC, I/O error, recovery error,
and retirement interruption. A process kill may prevent synchronous cleanup;
the persistent form must therefore remain recognizable and bounded for A5.

## 14. Application-to-store call flows

### 14.1 Candidate-bearing publish

```text
Application owner                         Store owner
-----------------                         -----------
authorize and order request
capture expected head/revision
ask runtime owner for complete candidate
                         candidate -----> A0/A1 validate, stage, compare, admit
                                         acquire final transition gate
                                         reread expected head/revision
                         stale <--------- mismatch: no head change
                                         or A2 atomic head replacement
                         result <-------- durable accepted head/revision
```

Authorization success does not bypass store OCC. Store OCC success does not
decide whether the application was authorized. `DEC-018` may refine the
application cutoff but not add another store transition point.

### 14.2 Reference-only branch/checkpoint/rollback/destruction

```text
fork Branch
    -> CreateHeadIfAbsent(new Head, Expected::Absent, accepted binding)
create Checkpoint
    -> CreateFixedRootIfAbsent(new fixed Checkpoint Root, Expected::Absent, binding)
rollback Branch
    -> ReplaceHead(Branch Head, Expected::Exact(captured complete Head), binding)
destroy Branch / remove Checkpoint
    -> RemoveHead / RemoveFixedRoot with the exact complete record

Every path uses A3's one ReferencePlane authority, returns the canonical typed
outcome, and asserts accepted-reference payload I/O `0/0/0`. No path accepts a
raw `VersionId`, retargets a fixed Root, or retries a stale Head against newly
captured state inside the same application request.
```

### 14.3 Committed read versus workspace read

```text
No workspace session:
  application selector -> A4 captured immutable store read

Live workspace session:
  application session -> existing workspace/effect owner
```

The latter may eventually form a complete candidate and call A2. It never
receives permission to mutate the accepted payload used as its base.

## 15. Concurrency outcome matrix

| History | Required outcome |
|---|---|
| Two equal candidate admissions | Exact equality as needed; one physical accepted occupant; both may receive the same binding |
| Unequal candidates forced to same ID | Collision; mismatch cannot alias or change any root/head |
| Two publishers with same expected head | At most one atomic head transition wins; the other returns stale |
| Publisher versus rollback/reference move | Operations serialize at the one transition gate; stale expected token loses cleanly |
| Head move during captured read | Reader stays on captured immutable binding; selector may advance independently |
| Read acquisition versus last-root retirement | Custody acquisition or final retirement wins a defined serialized race; never use-after-retire |
| New root versus retirement | Root transition or exact final retirement revalidation wins under the same authority; no rooted payload unlink |
| Cancellation during staging | No reference change; private state cleaned or bounded for recovery |
| ENOSPC before payload admission | No accepted binding/reference; private bounded cleanup debt only |
| Error after payload admission before head | Complete safe orphan; prior head remains |
| Auth revoke racing store request | Application-defined cutoff remains open; any accepted store call still obeys OCC and immutability |

## 16. Crash-prefix outcome matrix

Phase 03 must expand this matrix with every exact persistent step it selects.

| Crash interval | Required restart observation |
|---|---|
| Before private staging exists | Prior truth; no debt |
| During private candidate construction | Prior truth; recognizable bounded staging cleanup/quarantine |
| After private complete candidate, before accepted visibility | Prior truth; private staging only |
| During accepted-payload visibility transition | Either no accepted occupant or one complete accepted occupant; never partial accepted content |
| After accepted payload is durable, before the selected reference transition | Prior reference plus safe complete unreferenced payload |
| During Head/fixed-Root create, Head replace, or exact removal | Prior operation-appropriate state or complete new record/absence; never mixed/torn accepted truth |
| After durable reference state, before acknowledgement | Complete operation-appropriate new truth; retry semantics must resolve explicitly rather than merge/rebase |
| During retirement before final revalidation | Payload retained |
| During/after accepted-payload unlink | Phase 03 protocol yields retained complete payload or absent proven-unreachable payload; no valid reference dangles |
| During cleanup/recovery | Cleanup is repeat-safe; bounded recognizable debt remains |

## 17. I/O and optimization contract

R0 fixes measurable cost shapes, not a benchmark winner:

| Path | Required/allowed work |
|---|---|
| New Version admission | At least complete Candidate validation/canonicalization; complete payload staging/write; durability work |
| Occupied ID | Full canonical-byte comparison, potentially linear in complete Version size |
| Candidate publication | Expensive work outside final gate; bounded reference metadata inside gate |
| Five accepted-reference operations | `CreateHeadIfAbsent`, `ReplaceHead`, `RemoveHead`, `CreateFixedRootIfAbsent`, and `RemoveFixedRoot` have payload bytes read = written = copied = 0; bounded reference metadata, coordination, and fence work remain nonzero |
| Accepted read | One complete closure; no cost term proportional to layer depth |
| Retirement | Exact bounded reachability/custody metadata plus unlink; no layer GC graph |
| Recovery | Bounded recognized populations/debt; no unbounded reconstruction scan |

Correctness-required full comparison and durability fences cannot be removed to
improve a timing result. Stage 4.6 remains `INCOMPARABLE`; this design makes no
speedup, latency, throughput, memory, or 100x guarantee.

## 18. Phase-local selections

### Phase 02 may select

- portable entry/metadata profile;
- canonical grammar, version/domain, ordering, and path rules;
- digest algorithm/width and typed `VersionId` representation;
- streaming comparison interfaces and validation constants; and
- golden/corrupt/forced-ID test representation.

### Phase 03 may select

- exact durable names/layout within payload/root/head/staging/control roles;
- record encoding, versioning, checksum, and completeness markers;
- ID-slot coordination and accepted-payload visibility primitive;
- supported local filesystem profile;
- exact synchronization/atomic replacement/lock sequence;
- finite staging/population/recovery/custody limits;
- read-custody and non-authoritative index representation;
- same-Version revision/no-op result consistent with monotone OCC; and
- instrumentation and fault-injection mechanisms.

Neither phase may select a new authority, storage family, second writer,
digest-only admission, reference payload work, layer truth, silent merge/rebase,
or dual-write migration.

## 19. Verification trace

| Algorithm | Primary checks |
|---|---|
| A0 identity | Phase 02 I1 deterministic, I2 order, I3 corrupt, I4 limits, I6 forbidden fields |
| A1 admission | Phase 02 I5 seam; Phase 03 F1, F9 one payload, F10 collision, C4 cleanup |
| A2 publish | Phase 03 F1, F2 stale OCC, C1 crash, C2 restart |
| A3 reference lifecycle | Phase 03 F3 Head create/fork, F4 Head replace/rollback, F5 Head remove, F6 fixed-Root create/checkpoint, F7 fixed-Root remove, F8 outcomes/read-back, and F9 sharing; operation I/O counters |
| A4 captured read | Phase 03 concurrent head-move/read, attempted mutation, last-root/read histories |
| A5 recovery | Phase 03 C1 prior-or-new, C2 durable head, corrupt/dangling/unknown-version cases |
| A6 retirement | Phase 03 C3 last-root/read race and bounded debt |
| A7 import | Phases 05–07 generation fence, retry, writer inventory, and deletion proof |
| A8 cleanup | Phase 03 C4 cancel/timeout plus fault/ENOSPC boundary matrix |

## 20. Stop and reopening conditions

Stop and reopen Phase 01 if implementation evidence requires:

- layer, parent, squash, merge, archive-extraction, object-DAG, database, or
  another storage family as selected truth;
- runtime-private facts in portable identity;
- a new crate/service/process/coordinator or a store dependency on application
  or effect policy;
- more than one selected-Version transition authority or OCC point;
- skipping full occupied-ID comparison;
- payload work on a reference-only operation;
- writable accepted payloads;
- crash recovery outside prior-or-complete-new fail-closed behavior;
- unbounded read/retirement/recovery/resource populations; or
- dual writable migration truth.

Do not reopen for the exact codec, digest, record encoding, checksum, directory
name, finite constant, safe filesystem sequence, custody representation, or
internal module split when it preserves every algorithm contract above.

## References

- [Product PRD](../PRD.md)
- [Selected architecture](../architecture_design.md)
- [Phase 01 selection contract](../phases/01-choose-design/SPEC.md)
- [R0 Version identity](02-state-identity.md)
- [LayerStack-0 storage](03-state-store.md)
- [Phase 02 tests](../phases/02-state-identity/test-perf.md)
- [Phase 03 tests](../phases/03-state-store/test-perf.md)
