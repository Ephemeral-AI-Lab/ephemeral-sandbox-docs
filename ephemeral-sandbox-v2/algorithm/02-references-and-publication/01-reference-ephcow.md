# 02.01 — Reference EphCoW and complete reference lifecycle

## 1. Purpose, authority, and owning phase

**Owner:** Phase 03 — the one LayerStack-0 accepted-state and reference
authority. Application, migration, and runtime-effect owners are callers; none
is another record writer.  
**Purpose:** define one semantic transition mechanism for the complete Head and
fixed-Root lifecycle:

```text
CreateHeadIfAbsent(head_identity, Expected::Absent, new_binding)
ReplaceHead(head_identity, Expected::Exact(expected_head), new_binding)
RemoveHead(head_identity, Expected::Exact(expected_head))
CreateFixedRootIfAbsent(root_identity, root_kind, Expected::Absent, binding)
RemoveFixedRoot(root_identity, root_kind, Expected::Exact(expected_root))
```

The names are conceptual contracts, not selected Rust, wire, record, lock,
journal, or filesystem syntax. All five operations use the same LayerStack-0
reference authority, transition gate, complete-record comparison law,
conditional state-transition mechanism, qualified durability fence, and
authoritative read-back seam. Record policy differs: a Branch is represented
by a mutable Head; a Checkpoint is a fixed typed Root. Only a Head supports
replacement. No generic Root retarget/update operation exists, and no
higher-authority mutable Root kind has been proved.

This closure traces finding `019fcd32-b832-7750-9eb5-5f544e39c533` and does not
select the Phase 03 mechanisms that implement the contract.

## 2. Structural zero-payload boundary

Each operation receives only bounded reference metadata and an
admission-owned metadata verifier:

```text
LayerStack0Admission.revalidate_existing_binding_metadata(AcceptedBinding)

ReferencePlane
  read_head_record(TypedHeadIdentity)
  create_head_record_if_absent(Expected::Absent, CompleteHeadRecord)
  replace_head_record_conditionally(Expected::Exact(CompleteHeadRecord),
                                    CompleteHeadRecord)
  remove_head_record_conditionally(Expected::Exact(CompleteHeadRecord))
  read_fixed_root_record(TypedRootIdentity, RootKind)
  create_fixed_root_record_if_absent(Expected::Absent, CompleteFixedRootRecord)
  remove_fixed_root_record_conditionally(
      Expected::Exact(CompleteFixedRootRecord))
  fence_reference_transition()
```

`ReferencePlane` has no payload descriptor, accepted-payload accessor,
directory walker, canonical byte stream, materializer, copier, Workspace
handle, mount request, or runtime adapter. Metadata revalidation checks the
LayerStack-0-issued capability, accepted-record identity, store generation,
and non-retired state without opening accepted payload. Full canonical-byte
comparison belongs to admission.

For every success, conflict, absence, retry, cancellation, crash prefix, and
read-back path in this file:

```text
accepted-reference payload bytes read    = 0
accepted-reference payload bytes written = 0
accepted-reference payload bytes copied  = 0
```

That `0/0/0` claim excludes nonzero complete-record reads/writes, validation,
lock or coordination work, durability fences, custody accounting, retirement
evaluation, Workspace activation, Candidate capture/admission, and runtime
materialization. Those costs are measured separately.

## 3. Shared typed contract

### 3.1 Inputs and complete expected state

| Type | Required meaning |
|---|---|
| `TypedHeadIdentity` | Stable Head identity, namespace/kind, and incarnation information sufficient to prevent stale-name reuse; exact representation is Phase 03-owned. |
| `TypedRootIdentity` + `RootKind` | Stable fixed-Root identity, typed kind, and incarnation information; an unchecked display name or path is insufficient. |
| `AcceptedBinding` | LayerStack-0-issued binding to one complete immutable accepted Version; raw `VersionId` input is rejected. |
| `Expected::Absent` | The complete authoritative record for the typed identity must not exist. |
| `Expected::Exact(expected_head)` | Binding, revision/incarnation, identity, kind/generation, checksum/schema facts, and every field selected as part of the authoritative Head comparison must match. |
| `Expected::Exact(expected_root)` | Binding, identity, fixed kind, incarnation/generation, checksum/schema facts, and every field selected as part of the authoritative Root comparison must match. |

The caller captures an exact record as one value; it must not assemble an
expected state from independently read fields. Phase 03 must select bounded,
ABA-safe record/incarnation semantics. Silent wrap or name reuse that revives a
stale handle is invalid.

### 3.2 Authority and preconditions

1. Application authorization, product ordering, migration generation, and
   writer-class checks have completed where required, but those callers do not
   gain record authority.
2. LayerStack-0 is ready on the active generation, and its bounded debt,
   record, wait, descriptor, memory, and retry budgets permit the operation.
3. Every new target is an `AcceptedBinding` revalidated through the
   admission-owned metadata facet. A missing, retired, forged, or malformed
   binding is rejected without a raw-ID fallback.
4. The operation holds the sole process/filesystem-exclusive LayerStack-0
   transition gate for authoritative comparison and transition.
5. A fixed Root may be created or removed, never retargeted. A desired new
   checkpoint binding requires a distinct Root identity or an explicit exact
   remove followed by a separately authorized create; the intermediate absence
   is real and the pair is not atomic retargeting.

### 3.3 Required semantic outcomes

All callers preserve these distinctions:

| Outcome | Meaning |
|---|---|
| `APPLIED` | The requested complete-record transition linearized and crossed the qualified reference durability fence before acknowledgement. |
| `ALREADY_EXISTS` | An `Expected::Absent` create found a complete record already present. It made no mutation; the permitted response may expose bounded current metadata. |
| `NOT_FOUND` | An exact replace/remove target is absent. It made no mutation. |
| `CONFLICT` | A present complete record does not equal the supplied exact expected record, or a conditional primitive loses after the in-gate comparison. It made no requested mutation. |
| `INVALID_BINDING` | A target binding is forged, dangling, retired, wrong-generation, unavailable, or otherwise not acceptable. |
| `CORRUPT` | An authoritative record, expected record, namespace relation, or binding evidence is torn, malformed, ambiguous, or fails validation. Readiness or the affected operation fails closed. |
| `OUTCOME_UNKNOWN` | The transition may have linearized or crossed its fence, but the caller cannot prove the result because acknowledgement/observation failed. Authoritative read-back is mandatory. |
| `INTERNAL_FAILURE` | A bounded internal, resource, lock, fence, or I/O failure occurred and is not safely classifiable as another outcome. It never authorizes guessing or weakening durability. |

Cancellation before linearization returns `INTERNAL_FAILURE` with a typed
cancelled reason at the API mapping layer; cancellation after a possibly
linearized transition returns `OUTCOME_UNKNOWN` unless success is durably
known. Phase-owned error spellings may be more specific, but they must map
without collapsing the eight semantic distinctions above.

## 4. Shared transition and read-back law

For every operation:

1. validate typed identity, operation kind, expected-state variant, record
   bounds, generation, and caller class;
2. when a new binding is supplied, revalidate it using metadata-only admission
   authority;
3. observe cancellation before entering the transition point;
4. acquire the one LayerStack-0 transition gate;
5. read and validate the complete authoritative record or authoritative
   absence;
6. compare the complete expected state and return the exact non-mutating
   `ALREADY_EXISTS`, `NOT_FOUND`, `CONFLICT`, `INVALID_BINDING`, or `CORRUPT`
   outcome when applicable;
7. invoke exactly one conditional complete-record create, replace, or remove
   primitive under the same authority;
8. treat that successful conditional primitive as the semantic linearization
   point;
9. apply the Phase 03-qualified reference durability fence;
10. release the gate and return `APPLIED` only after the fence succeeds; and
11. on an ambiguous transition/fence/acknowledgement result, return
    `OUTCOME_UNKNOWN` and use a distinct non-mutating authoritative resolver.

The conditional primitive must repeat the complete expected-state comparison;
an in-memory precheck alone is insufficient. Readers observe prior complete
truth or new complete truth, never a fieldwise mix.

Read-back validates the complete current record/absence under the ordinary
read integrity and generation rules. It proves an authoritative postcondition,
not which concurrent caller caused it. Operation/request identity may be part
of the complete record only if a later owning phase selects it within R0; the
contract does not manufacture that mechanism.

## 5. Operation contracts

### 5.1 `CreateHeadIfAbsent`

```text
create_head_if_absent(head_identity, Expected::Absent, new_binding):
    validate identity and Expected::Absent
    target := revalidate_existing_binding_metadata(new_binding)
    if invalid: return INVALID_BINDING
    acquire transition gate
    current := read and validate complete Head or absence
    if corrupt: release; return CORRUPT
    if present: release; return ALREADY_EXISTS(current metadata allowed by policy)
    next := complete initial Head(head_identity, target, initial revision/incarnation)
    conditionally create next requiring authoritative absence
    if conditional conflict: release; return ALREADY_EXISTS or CONFLICT
        according to authoritative read-back; never overwrite
    fence reference transition
    release; return APPLIED(next)
```

- **Linearization:** conditional complete Head create-if-absent.
- **Durable success:** after the reference fence; preparation or rename without
  the fence is not `APPLIED`.
- **Already present:** `ALREADY_EXISTS` whether the occupant names the same or a
  different binding; no implicit idempotent overwrite occurs. A caller may
  separately read and compare the occupant.
- **Retry/idempotency:** before known linearization, a retry with the same
  typed identity and binding is safe because create-if-absent cannot overwrite.
  After `ALREADY_EXISTS`, read the complete Head and decide at the caller seam;
  do not convert the create into replacement.
- **Unknown outcome:** read the exact Head. The intended complete initial record
  proves the desired postcondition; absence proves no durable create; any other
  complete record is `ALREADY_EXISTS`/`CONFLICT`; ambiguity remains fail-closed.
- **Custody/reachability:** `APPLIED` adds one Head reachability edge. A failed
  create adds none. Operation custody protecting the target is released only
  after the decision is safe.
- **Retirement/debt:** a failed create after separate Version admission may
  leave a valid accepted orphan charged to bounded cleanup debt. It never
  publishes merely to avoid that debt.
- **Callers:** sandbox/manager initialization, durable target Branch creation
  during fork, and initial migrated Branch creation.

### 5.2 `ReplaceHead`

```text
replace_head(head_identity, Expected::Exact(expected_head), new_binding):
    validate exact expected Head and target binding
    acquire transition gate
    current := read and validate complete Head or absence
    if corrupt: release; return CORRUPT
    if absent: release; return NOT_FOUND
    if current != expected_head: release; return CONFLICT
    next := complete Head(target binding, checked revision/incarnation successor)
    conditionally replace requiring on-disk current == expected_head
    if conditional mismatch: release; return CONFLICT
    fence reference transition
    release; return APPLIED(next)
```

- **Linearization:** the sole conditional complete Head replacement used by
  publication, rollback, and authorized same-Version transitions.
- **Durable success:** the new Head record must cross the reference fence
  before `APPLIED`.
- **Absent/stale:** absence is `NOT_FOUND`; any mismatch in the complete
  expected record is `CONFLICT`. There is no merge, rebase, expected refresh,
  target recapture, or automatic retry.
- **Retry/idempotency:** a known-success replay with the old expected Head is
  `CONFLICT`; this prevents a double revision advance. After
  `OUTCOME_UNKNOWN`, the caller uses read-back rather than blind replacement.
- **Unknown outcome:** the exact intended successor may establish the desired
  postcondition; expected unchanged establishes no replacement; any other
  record is conflict/indeterminate and never publisher attribution.
- **Custody/reachability:** `APPLIED` atomically adds reachability to the new
  binding and removes this Head's edge to the prior binding. Captured reader
  custody for the prior Version remains valid.
- **Retirement/debt:** the prior binding enters ordinary exact retirement
  evaluation; it is not deleted synchronously. A stale publication can leave
  its separately admitted target as accepted orphan debt.
- **Callers:** new-Version publication, rollback of a Branch to an existing
  accepted Version or fixed Checkpoint binding, rollout Branch advancement,
  and the Phase 03-selected same-Version rule when that rule advances revision.

### 5.3 `RemoveHead`

```text
remove_head(head_identity, Expected::Exact(expected_head)):
    validate exact expected Head
    acquire transition gate
    current := read and validate complete Head or absence
    if corrupt: release; return CORRUPT
    if absent: release; return NOT_FOUND
    if current != expected_head: release; return CONFLICT
    conditionally remove requiring on-disk current == expected_head
    if conditional mismatch: release; return CONFLICT
    fence reference transition
    release; schedule ordinary exact retirement evaluation; return APPLIED
```

- **Linearization:** conditional removal of the exact complete Head.
- **Durable success:** authoritative absence/tombstone semantics selected by
  Phase 03 cross the same reference fence before `APPLIED`.
- **Retry/idempotency:** a retry after known success returns `NOT_FOUND`. That
  is a stable idempotent postcondition, not a second `APPLIED` transition.
- **Unknown outcome:** complete authoritative read-back returns expected record
  (not removed), absence (desired postcondition), another incarnation/record
  (`CONFLICT`), or corruption/fail-closed. Never delete the newly observed
  record as a retry.
- **Custody/reachability:** `APPLIED` removes exactly one Head reachability
  edge; existing reader/operation custody remains authoritative.
- **Retirement/debt:** removal schedules bounded exact revalidation of Heads,
  fixed Roots, custody, and recognizable debt. It never directly unlinks the
  accepted payload and never reports payload cleanup as part of removal.
- **Callers:** sandbox/Branch destruction, fork/rollout loser cleanup, and
  pre-activation migration cleanup where exact owned records were captured.

### 5.4 `CreateFixedRootIfAbsent`

```text
create_fixed_root_if_absent(
    root_identity, root_kind, Expected::Absent, binding):
    validate typed fixed-root identity/kind and Expected::Absent
    target := revalidate_existing_binding_metadata(binding)
    if invalid: return INVALID_BINDING
    acquire transition gate
    current := read and validate complete fixed Root or absence
    if corrupt: release; return CORRUPT
    if present: release; return ALREADY_EXISTS(current metadata allowed by policy)
    next := complete fixed Root(identity, kind, incarnation/generation, target)
    conditionally create next requiring authoritative absence
    if conditional conflict: release; return ALREADY_EXISTS or CONFLICT
        according to authoritative read-back; never overwrite
    fence reference transition
    release; return APPLIED(next)
```

- **Linearization:** conditional complete fixed-Root create-if-absent.
- **Durable success:** after the same qualified reference fence.
- **Already present:** `ALREADY_EXISTS` for any occupant; even an equal binding
  is not silently recreated. A different binding is not retargeted.
- **Retry/idempotency:** a same-request retry converges on the one occupant and
  returns `ALREADY_EXISTS`; the caller may compare the complete record but may
  not turn the create into update.
- **Unknown outcome:** exact Root read-back distinguishes intended occupant,
  absence, a conflicting occupant/incarnation, and corruption.
- **Custody/reachability:** `APPLIED` adds one fixed durable reachability edge.
- **Retirement/debt:** a failed create can leave a separately admitted Version
  unrooted; bounded retirement handles it. No cleanup path retargets the Root.
- **Callers:** checkpoint-to-existing, checkpoint-after-successful admission,
  fixed recovery/retention pins selected by a higher-authority contract, and
  mapped legacy checkpoint/pin creation during migration.

### 5.5 `RemoveFixedRoot`

```text
remove_fixed_root(
    root_identity, root_kind, Expected::Exact(expected_root)):
    validate typed identity/kind and exact complete expected Root
    acquire transition gate
    current := read and validate complete fixed Root or absence
    if corrupt: release; return CORRUPT
    if absent: release; return NOT_FOUND
    if current != expected_root: release; return CONFLICT
    conditionally remove requiring on-disk current == expected_root
    if conditional mismatch: release; return CONFLICT
    fence reference transition
    release; schedule ordinary exact retirement evaluation; return APPLIED
```

- **Linearization:** conditional removal of the exact complete fixed Root.
- **Durable success:** authoritative absence crosses the reference fence before
  `APPLIED`.
- **Retry/idempotency:** a known-success retry returns `NOT_FOUND`; it never
  removes a newly created incarnation that reused a display name.
- **Unknown outcome:** read back the typed identity and complete incarnation.
  Absence proves the desired postcondition; the expected record means not
  removed; any other complete record is `CONFLICT`; corruption fails closed.
- **Custody/reachability:** `APPLIED` removes exactly that Root edge; custody and
  all other Heads/Roots continue to retain the Version.
- **Retirement/debt:** schedule bounded exact retirement evaluation, never
  synchronous payload deletion.
- **Callers:** checkpoint/pin removal, manager destruction of exact owned fixed
  Roots, and pre-activation migration cleanup of exact importer-owned Roots.

## 6. Same-Version Head behavior

Phase 03 may select exactly one of these within-R0 results for a
`ReplaceHead` whose target names the current Accepted Version:

1. conditionally replace the exact Head with a checked revision successor and
   return `APPLIED` after the fence; or
2. perform a comparison-only no-op under the gate and return an API-specific
   replay/no-op result mapped without claiming `APPLIED`.

Either preserves ABA safety, the exact expected comparison, one authority, and
accepted-reference payload `0/0/0`. Callers must not infer the chosen rule from
raw IDs, and fixed Roots have no analogous same-Version move.

## 7. Cancellation, crash, recovery, and cleanup prefixes

| Prefix | Required restart/caller result |
|---|---|
| Before transition gate or before conditional operation | Prior truth remains; bounded private temporary metadata is removable; no authoritative record mutation. |
| Conditional operation definitely rejects | Required non-mutating `ALREADY_EXISTS`, `NOT_FOUND`, or `CONFLICT`; no fence can convert it to success. |
| Conditional operation may have linearized, fence/ack unknown | `OUTCOME_UNKNOWN`; authoritative read-back is required. Never undo or blindly retry. |
| Complete new record/absence visible but fence not provable | Recovery applies the declared filesystem profile and fails closed if durability cannot be established. No early success. |
| Fence complete, acknowledgement lost | Read-back observes the durable postcondition; caller mapping may report recovered success without performing a second mutation. |
| Corrupt/torn/ambiguous authoritative record | `CORRUPT`; quarantine/report exact evidence and do not report ready. |
| Bounded internal failure before known linearization | `INTERNAL_FAILURE`; retain prior truth and recognizable bounded cleanup debt. |

Recovery recognizes protocol artifacts and complete records; it does not guess
authority from filenames, timestamps, metrics, refcounts, or migration
progress. Temporary record fragments and accepted orphans are bounded debt.
Authoritative Heads and fixed Roots are never cleanup hints.

## 8. Payload, metadata, custody, and retirement matrix

| Operation | Accepted payload R/W/C | Nonzero work | Reachability effect | Retirement effect |
|---|---:|---|---|---|
| Create Head | `0/0/0` | record validation/read/write, gate, fence, custody accounting | add one Head edge | failed create may leave admitted orphan debt |
| Replace Head | `0/0/0` | record validation/read/write, gate, OCC compare, fence | add target/remove prior Head edge atomically | evaluate prior binding; stale target may be orphan debt |
| Remove Head | `0/0/0` | record validation/read/remove, gate, fence | remove exact Head edge | schedule exact bounded retirement evaluation |
| Create fixed Root | `0/0/0` | record validation/read/write, gate, fence | add one fixed-Root edge | failed create may leave admitted orphan debt |
| Remove fixed Root | `0/0/0` | record validation/read/remove, gate, fence | remove exact fixed-Root edge | schedule exact bounded retirement evaluation |

Retirement revalidates all supported Heads, fixed Roots, reader/operation
custody, and recognized debt before unlinking. A derived index/refcount may
accelerate that proof but cannot replace authority without a later proof.

## 9. Caller mapping

| Caller intent | Required operation | Selected algorithm boundary |
|---|---|---|
| Initialize sandbox/manager Branch | `CreateHeadIfAbsent(..., Expected::Absent, binding)` | This file, section 5.1 |
| Create durable fork target Branch | `CreateHeadIfAbsent(..., Expected::Absent, binding)` | This file, section 5.1; local `ForkStart` alone is not a durable Branch |
| Publish admitted Candidate | `ReplaceHead(..., Expected::Exact(expected_head), binding)` | [OCC publication](02-occ-publication.md) plus this file, section 5.2 |
| Roll back Branch to accepted Version/checkpoint | Read/revalidate target, then `ReplaceHead` | This file, section 5.2; fixed Root does not move |
| Checkpoint accepted Version | `CreateFixedRootIfAbsent(..., Checkpoint, Expected::Absent, binding)` | This file, section 5.4 |
| Remove checkpoint/pin | capture exact Root, then `RemoveFixedRoot` | This file, section 5.5 |
| Destroy sandbox/Branch | capture exact Head, then `RemoveHead`; remove exact owned fixed Roots separately | This file, sections 5.3 and 5.5 |
| Migration initialization | ordinary `CreateHeadIfAbsent` and/or `CreateFixedRootIfAbsent` according to mapped source kind | This file; migration owns no alternate mutation |
| Pre-activation migration cleanup | ordinary exact `RemoveHead`/`RemoveFixedRoot` | This file; cleanup cannot directly delete records |
| Capture accepted Version for read/runtime | read complete reference, acquire custody, hand off `AcceptedBinding` | [Read custody and runtime handoff](../03-runtime-access-and-materialization/01-read-custody-and-runtime-handoff.md) |

The manager, migrator, application, runtime adapter, and observability code
never write, replace, tombstone, or delete a LayerStack-0 record directly.

## 10. Resource, security, and observability obligations

Record bytes, Root/Head populations, identity lengths, gate wait, retries,
temporary records, operation custody, descriptors, memory, workers, orphan
count/bytes, and retirement debt have finite enforceable ceilings. Exhaustion
returns bounded backpressure/`INTERNAL_FAILURE` without opening payload or
weakening the expected-state/fence law.

Typed identities are mapped through a Phase 03-selected non-overlapping
namespace without unchecked concatenation, traversal, separators, prefixes,
symlink following, or aliasing. Serialized capabilities, generations, schemas,
checksums, and bounds are validated before use. Authorization remains above
LayerStack-0, but LayerStack-0 enforces binding and concurrency integrity even
when a caller is defective.

Required diagnostics separate:

```text
reference_payload_bytes_read_total       # must add 0
reference_payload_bytes_written_total    # must add 0
reference_payload_bytes_copied_total     # must add 0
reference_metadata_bytes_read_total      # may be nonzero
reference_metadata_bytes_written_total   # may be nonzero
reference_gate_wait / fence / recovery   # may be nonzero
accepted_orphan_count / bytes            # may be nonzero and bounded
retirement_debt_count / bytes             # may be nonzero and bounded
```

Observers cannot acquire transition authority, issue a binding, create or
remove a reference, decide readiness, or retain a Version.

## 11. Required proof matrix

Phase 03 tests each operation across normal, already-present/absent/conflict,
invalid binding, corrupt record, bounded internal failure, cancellation before
and after the transition point, response loss, every persistent crash prefix,
concurrent callers, retry, exact read-back, last-reference removal with reader
custody, orphan debt, and recovery restart. Structural tests forbid payload and
materialization imports; injected payload access traps and classified I/O
counters prove `0/0/0` for every semantic outcome.

## 12. Still open within R0

`OPEN_WITHIN_R0`: exact record encoding, identity/incarnation representation,
same-Version rule, filesystem primitive, lock/gate, journal/tombstone strategy,
qualified fence sequence, supported filesystem profile, result correlation,
custody representation, retirement implementation, cleanup batching, finite
limits, metrics, and public/wire spelling.

`OPEN`: V2 implementation, filesystem qualification, crash campaigns, and
executable zero-payload evidence are absent. These gaps do not change the
complete semantic seam.

`OWNER_DEC_OPEN`: `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` remain open.

## 13. `REOPEN_PHASE_01` conditions

Reopen Phase 01 only if reproducible implementation evidence proves that a
required lifecycle operation must traverse accepted payload, needs a second
reference authority or Head/OCC point, requires mutable accepted truth, cannot
use bounded exact expected-state comparison/read-back, cannot fence before
success, or cannot retire safely using bounded Heads, fixed Roots, custody, and
debt. An unselected record/fence mechanism, absent backend evidence, or missing
implementation is not such proof.

## Related contracts

- [Reference/publication cluster index](README.md)
- [OCC publication](02-occ-publication.md)
- [Composed publication pipeline](03-composed-publication-pipeline.md)
- [Zero-payload reference demonstration](04-zero-payload-reference-demonstration.md)
- [State-store design](../../design/03-state-store.md)
- [Manager API](../../api/manager.md)
- [Durability and recovery](../04-durability-and-lifecycle/01-durability-and-recovery.md)
- [Retirement and cleanup](../04-durability-and-lifecycle/02-retirement-and-cleanup.md)
- [Phase 03 contract](../../phases/03-state-store/PRD.md)
