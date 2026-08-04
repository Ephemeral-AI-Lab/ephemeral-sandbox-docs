# 02.04 — Zero-payload reference demonstration

```text
EVIDENCE_LABEL: OPEN
CORRECTNESS_RESULT: NOT_RUN
FINAL_PERFORMANCE_VERDICT: TARGET_UNSELECTED
required correctness result after execution: payload read/write/copy/open = 0/0/0/0
```

## 1. Purpose and owning phases

**Owners:** Phase 03 supplies negative capabilities and scoped
instrumentation; Phase 06 executes qualification against a sealed
implementation and environment.  
**Purpose:** Turn the EphCoW zero-payload claim into a structural proof plus a
repeatable normal/concurrent/retry/cancellation/crash demonstration.

The claim is deliberately scoped:

```text
CreateHeadIfAbsent, ReplaceHead (including publication/rollback), RemoveHead,
CreateFixedRootIfAbsent, RemoveFixedRoot, and non-durable binding handoff

payload bytes read    = 0
payload bytes written = 0
payload bytes copied  = 0
payload opens         = 0
```

It is not a claim that Candidate capture, complete-Version admission, runtime
activation, or private materialization is zero-copy.

## 2. Evidence status

- `SOURCE-VERIFIED`: selected ownership and the e497 source seal are verified;
  no existing behavior proves the V2 counters.
- `SPIKE-VERIFIED`: none; this demonstration has not run. Its correctness
  result is `NOT_RUN` and its evidence label is `OPEN`; `DESIGN_ONLY` is a
  final performance verdict and is not used as a correctness/evidence state.
- `INFERRED`: negative payload capability, forbidden dependency edges, trapped
  access, operation-scoped I/O classification, and tracing together can prove
  the selected reference property.
- `OPEN`: Phase 03 selects capability/API and metric spellings; Phase 06 selects
  tracer, filesystem, workload sizes, repetition/noise policy, and sealed
  qualification environment `OPEN_WITHIN_R0`.

## 3. Structural proof

The reference plane receives only metadata capabilities:

```text
ReferencePlaneCapability
  may access:
    AcceptedBinding verifier metadata
    complete Head records
    complete Root records
    transition-control records
    transition gate

  cannot access:
    versions/<VersionId>/payload/
    Candidate or Workspace content
    runtime materialization destinations
    payload open/read/copy/write interfaces
```

The proof requires all of the following:

1. Reference-plane types expose no payload handle or payload path.
2. Dependency/build checks reject payload/materialization imports into
   reference transition modules.
3. A test payload accessor traps immediately if invoked in reference scope.
4. Scoped accounting classifies payload and reference/control I/O separately.
5. Filesystem/syscall tracing validates allowed path classes independently.
6. Tests cover every outcome, not only successful warm-cache calls.

Counters alone are insufficient because a missing hook could report zero. Type
and dependency exclusion alone are insufficient because an ambient filesystem
open could bypass them. The two proof styles compose.

## 4. Demonstration contract

### Inputs

- A sealed LayerStack-0 implementation, build manifest, and source commit.
- A Phase 03-qualified filesystem and durability configuration.
- At least two complete AcceptedVersions with distinct nonempty payloads and
  admission-issued AcceptedBindings.
- Typed Head/Root fixtures and expected revisions.
- Scoped I/O classifier, trapped payload accessor, filesystem/syscall tracer,
  and bounded event buffers.
- Finite cases, repetitions, concurrency, crash points, time, memory, FDs,
  workers, trace bytes, and temporary-space budgets.

### Preconditions

1. Fixtures were admitted through ordinary LayerStack-0 admission; raw IDs are
   not injected into Head or Root records.
2. At least one payload is large/nontrivial enough that accidental access is
   observable; byte size is not itself a pass criterion.
3. Instrumentation self-tests prove a deliberate payload read/write/copy/open
   increments or traps in an activation/materialization control case.
4. Operation scopes cannot overlap in a way that attributes activation/admission
   bytes to a reference operation.
5. Tracing loss, buffer overflow, unknown path classification, or missing scope
   identity invalidates the run rather than being counted as zero.

### Outputs

A sealed per-case evidence manifest plus exactly one typed suite outcome. The
manifest records functional results, four payload dimensions, trace coverage,
positive controls, resource high-water marks, and source/configuration seals;
it has no product authority.

### Typed outcomes

| Outcome | Meaning |
|---|---|
| `QualifiedZeroPayload(evidence)` | Structural checks passed and every required reference case reported payload `0/0/0/0` with complete trace coverage. |
| `FailedPayloadAccess(case, evidence)` | Any payload open/read/write/copy or forbidden dependency/access occurred. |
| `FailedReferenceSemantics(case, evidence)` | Payload counters were zero but the reference result, OCC behavior, or durable record semantics were wrong. |
| `EvidenceInvalid(reason)` | Instrumentation, scope, trace, fixture, seal, or resource coverage was incomplete. |
| `NotRun` | Design contract exists but no sealed execution occurred; current package state. |

## 5. Demonstration algorithm

```text
qualify_zero_payload_reference(suite, budgets):
    verify source/build/filesystem/configuration seals
    verify forbidden dependency edges are absent
    run instrumentation positive controls in non-reference scope
    if any control is not detected: return EvidenceInvalid

    for case in bounded_required_case_matrix:
        establish isolated admitted fixtures and expected reference truth
        arm trapped payload accessor
        begin operation-scoped counters and independent trace

        execute exactly one reference operation/outcome

        stop scope and require complete trace delivery
        validate functional and durable result
        assert payload_open_count == 0
        assert payload_read_bytes == 0
        assert payload_write_bytes == 0
        assert payload_copy_bytes == 0
        classify every observed path as allowed reference/control

        if any payload access: return FailedPayloadAccess(case, evidence)
        if semantics wrong: return FailedReferenceSemantics(case, evidence)
        if evidence incomplete: return EvidenceInvalid(reason)

    return QualifiedZeroPayload(sealed_aggregate)
```

## 6. Required case matrix

| Operation/outcome | Functional assertion | Payload assertion |
|---|---|---|
| Non-durable binding handoff | Local context refers to same accepted start; no durable Branch exists until Head creation | `0/0/0/0` |
| `CreateHeadIfAbsent` applied/already-present/error/read-back | One complete initial Head or unchanged occupant/absence as required | `0/0/0/0` |
| `RemoveHead` applied/not-found/conflict/error/read-back | Exact Head absence or unchanged authoritative record as required | `0/0/0/0` |
| `CreateFixedRootIfAbsent` applied/already-present/error/read-back | One fixed complete Root or unchanged occupant/absence as required | `0/0/0/0` |
| `RemoveFixedRoot` applied/not-found/conflict/error/read-back | Exact fixed Root absence or unchanged authoritative record as required | `0/0/0/0` |
| Rollback through `ReplaceHead` | One expected exact conditional Head result | `0/0/0/0` |
| Same-Version Head rule | Exactly selected no-op or revision-advance behavior | `0/0/0/0` |
| Accepted-only publication success | One expected Head successor | `0/0/0/0` |
| Stale publication | Head write zero; no merge/rebase/refresh | `0/0/0/0` |
| Concurrent same expectation | Exactly one winner, all state-changing losers stale | each scope `0/0/0/0` |
| Read-only unknown-outcome resolution | Exact successor observed/not observed; no mutation | `0/0/0/0` |
| Cancellation before point | Prior truth remains | `0/0/0/0` |
| Cancellation after possible point | success/unknown classification; no rollback | `0/0/0/0` |
| Injected reference-record error | fail closed; no payload fallback | `0/0/0/0` |
| Crash at each record prefix | prior/complete-new/fail-closed recovery | `0/0/0/0` in reference scope |

Admission and runtime materialization positive controls must show nonzero payload
accounting when bytes actually move, proving the classifier did not simply
disable all payload measurement.

## 7. Visibility and linearization

The demonstration adds no product visibility or linearization point. It
observes the points defined by the underlying algorithms:

- conditional complete-record create/remove visibility for initial Heads and
  fixed Roots; and
- the **single Head movement/OCC point**, conditional replacement of one
  complete Head record under the LayerStack-0 transition gate.

Head create/replace/remove and fixed-Root create/remove all use the one
reference transition authority and qualified fence; create/remove do not add a
second Head movement/OCC point.

Starting/stopping a trace, emitting a counter, trapping an accessor, or declaring
a test passed is never a Head/Root durability point or authority decision.

## 8. Behavior by execution condition

| Condition | Required demonstration behavior |
|---|---|
| Normal | Run all required cases with isolated scopes and validate semantics plus four zero payload dimensions. |
| Concurrent | Preserve per-operation attribution; aggregate zero is insufficient if one scope is missing. |
| Retry | Treat each attempt as a new scope; old expected tuple must become stale after a winner. |
| Cancellation | Require complete trace flush; otherwise return `EvidenceInvalid`, not a pass. |
| Crash | Resume from sealed fixture/evidence state, validate recovery classification, and rerun any case whose trace was incomplete. |
| Cleanup | Remove only demonstration fixtures created in its isolated test root; incomplete cleanup is bounded test debt, never permission to touch live state. |

## 9. Finite resources and complexity

Let `N_case` be cases, `R` repetitions, `C` maximum concurrent operations,
`R_rec` maximum reference record bytes, `S_trace` trace events/bytes, and
`M_tool` measurement-tool working memory.

- Reference algorithm cost remains `O(1) + L_gate` and `O(R_rec)` metadata per
  operation, with payload I/O exactly zero when qualified.
- Demonstration orchestration is `O(N_case * R)` operations plus crash/recovery
  cases.
- Trace processing is `O(S_trace)` time and bounded `O(M_tool)` memory or a
  bounded streaming/spill strategy.
- Peak subjects are bounded by `C`; FDs, workers, fixture bytes, event buffers,
  temporary disk, and wall time have selected caps.

Instrumentation overhead must be reported separately; it cannot be subtracted
to manufacture a latency claim. Budget/trace exhaustion returns
`EvidenceInvalid` and preserves prior truth.

## 10. Security and path validation

- Run only in an isolated qualification root; reject product/live/migration
  paths and validate every configured target beneath that root.
- Treat tracer output, operation IDs, selector values, and injected failures as
  untrusted; redact content and bound cardinality/volume.
- Ensure the trapped payload accessor cannot be disabled by the code under test
  and the tracer cannot follow uncontrolled namespaces.
- Do not expose payload content in evidence. Record byte counts/path classes,
  not file contents or secret paths.
- A diagnostic agent cannot issue/revalidate a binding, acquire transition
  authority, or alter an expected Head to make a test pass.

## 11. Observability and test seams

Conceptual required facts are:

```text
reference_payload_open_count
reference_payload_bytes_read
reference_payload_bytes_written
reference_payload_bytes_copied
reference_record_bytes_read
reference_record_bytes_written
reference_metadata_operations
trace_unknown_path_count
trace_dropped_event_count
```

Exact names are Phase 03-owned. The sealed result must include source/config
identity, operation/outcome, expected/current revision relation, counter values,
trace completeness, forbidden-dependency result, positive-control result,
resource high-water marks, and crash/cancellation classification.

## 12. Details owning phases may still select

Phase 03 selects capability boundaries, module dependencies, counter hooks,
record path classes, and fixture interfaces. Phase 06 selects tracer, sealed
environment, repetitions, concurrency, failure injection, evidence format,
retention, and acceptable measurement overhead.

They may not weaken `0/0/0/0`, omit failure paths, combine admission/runtime
bytes into the reference scope, or accept incomplete tracing as zero.

## 13. `REOPEN_PHASE_01` conditions

Reopen Phase 01 with the exact failure if a correct required reference-only
operation must open/read/write/copy the complete payload, or if the existing
LayerStack-0 boundary cannot structurally exclude payload access without a new
authority/storage family.

An instrumentation bug, missing test, counter spelling, or unqualified tracer
is `OPEN_WITHIN_R0`/`EvidenceInvalid`, not an architecture failure. A failed
functional OCC/Root test is repaired within its owning algorithm unless it
proves that one complete-record reference model cannot satisfy a hard rule.
