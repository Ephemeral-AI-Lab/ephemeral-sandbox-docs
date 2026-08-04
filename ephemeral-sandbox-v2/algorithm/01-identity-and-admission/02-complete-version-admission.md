# 01.02 — Complete Version admission

## 1. Purpose and owning phase

**Owner:** Phase 03 — LayerStack-0 durable storage, consuming Phase 02 identity.  
**Purpose:** Turn a validated Candidate into one durable AcceptedVersion backed
by exactly one complete immutable filesystem-native payload closure, then issue
or revalidate an AcceptedBinding.

Admission is the sole boundary between a computed Candidate identity and
durable accepted authority. It does not publish a Head. Publication is the
separate [OCC algorithm](../02-references-and-publication/02-occ-publication.md).

```text
Canonical Candidate + VersionId
             |
             v
LayerStack-0 bounded admission
             |
             v
 AcceptedVersion -> AcceptedBinding
```

## 2. Evidence status

- `SOURCE-VERIFIED`: the selected existing package is the current durable
  history owner and contains a writer-lock plus atomic-write/durability
  primitive family that can be rewritten in place. This is placement evidence,
  not proof of V2 admission semantics.
- `SPIKE-VERIFIED`: none; no V2 admission or crash spike has run.
- `INFERRED`: complete-payload construction, occupied-ID exact comparison,
  convergence, immutable installation, and accepted-capability issuance are R0
  design contracts pending implementation and qualification.
- `OPEN`: Phase 03 must select exact paths, per-Version comparison-material
  representation, staging records, locks, supported filesystems, durability
  fences, limits, and error spellings. They are `OPEN_WITHIN_R0`.

## 3. Contract

Conceptual names below express ownership and type flow; they are not selected
Rust signatures, filenames, or record encodings.

### Inputs

- `CanonicalCandidate` from
  [01-canonical-version-identity.md](01-canonical-version-identity.md): typed
  `VersionId`, complete validated portable facts, exact canonical comparison
  stream, and charged totals.
- `AdmissionBudget`: reserved finite bytes, entries, scratch, memory,
  descriptors, workers, staging slots, and cleanup-debt allowance.
- `StoreGeneration`: a LayerStack-0-validated format/generation context.
- Cancellation/deadline signal checked between bounded units.

### Preconditions

1. The Candidate passed the supported Phase 02 schema and limits.
2. Its canonical stream is complete, sealed, replayable, and integrity-checked.
3. LayerStack-0 is ready on a Phase 03-qualified local filesystem.
4. The requested resources and one private staging slot have been reserved
   before Candidate-sized work begins.
5. No caller-supplied path, digest, or asserted AcceptedBinding is trusted.

### Outputs

Success returns an AcceptedBinding that LayerStack-0 issued or revalidated for
an AcceptedVersion. The AcceptedVersion consists of:

- the complete canonical bytes, or a Phase 03-selected exact per-Version
  comparison representation that preserves byte-for-byte comparison;
- one complete immutable filesystem-native payload closure; and
- integrity/format evidence sufficient for fail-closed revalidation and
  recovery.

Comparison material is per Version, not a cross-Version object graph or a
second truth representation. The complete payload remains readable truth.

### Typed outcomes

| Outcome | Meaning |
|---|---|
| `AcceptedNew(binding)` | A previously absent `VersionId` now names a durable complete AcceptedVersion, and LayerStack-0 issued its binding. |
| `AcceptedExisting(binding)` | An occupied ID had fully equal canonical bytes; the existing complete payload was reused and its binding revalidated. |
| `Collision` | The occupied ID's complete canonical bytes differ. No new binding or reference was issued. |
| `InvalidCandidate` | Candidate evidence, schema, accounting, or replay integrity failed revalidation. |
| `LimitExceeded` | Reservation, staging, disk, memory, FD, worker, entry, time, or debt bound would be exceeded. |
| `UnsupportedStore` | Filesystem or format semantics cannot meet the qualified contract. |
| `AcceptedArtifactCorrupt` | Occupied acceptance evidence or payload is corrupt, ambiguous, or incomplete; admission fails closed and quarantines/alerts within bounds. |
| `AdmissionIoFailed` | Construction, comparison, fencing, or installation failed before a success could be established. |
| `CancelledBeforeAcceptance` | Cancellation was observed before durable acceptance visibility. |
| `OutcomeUnknown` | The caller lost confirmation across a crash or I/O failure near visibility; retry/revalidation must resolve it without assuming acceptance. |

Digest equality or length equality can never produce `AcceptedExisting`.

## 4. Admission algorithm

```text
admit_complete_version(candidate, budget, generation):
    revalidate candidate schema, typed VersionId, totals, and replay integrity
    reserve finite staging bytes, debt capacity, FDs, memory, and worker slot
    tx := create recognizable private staging transaction

    cancellation_checkpoint_or_abort(tx)
    retain exact canonical comparison stream inside tx
    build complete filesystem-native payload from every portable fact:
        validate every relative path again at the write boundary
        create beneath an anchored private staging handle only
        never follow a Candidate-controlled link or cross a mount boundary
        charge metadata and physical/logical bytes before each operation
    verify complete entry/content/accounting closure
    mark tx as payload-complete in the selected recognizable form

    acquire bounded LayerStack-0 VersionId admission reservation
    occupant := inspect accepted slot(candidate.version_id)

    if occupant exists:
        revalidate occupant as one complete AcceptedVersion
        equal := full_canonical_byte_compare(
                     candidate.comparison_stream,
                     occupant.comparison_stream)
        if equal is NotEqual:
            record collision diagnostic without content disclosure
            release reservation
            retire private tx within cleanup bound
            return Collision
        if equal is ComparisonFailed:
            classify bounded comparison/integrity failure
            quarantine/alert accepted evidence if its integrity is suspect
            release reservation
            retire or quarantine private tx within cleanup bound
            return AcceptedArtifactCorrupt or AdmissionIoFailed
        binding := LayerStack0.revalidate_or_issue_binding(occupant)
        release reservation
        retire private tx within cleanup bound
        return AcceptedExisting(binding)

    cancellation_checkpoint_or_abort(tx)
    make complete payload and comparison material immutable
    apply Phase 03-qualified payload durability fence
    atomically install the whole accepted closure into the unoccupied slot
    apply Phase 03-qualified acceptance visibility fence
    require the installed closure revalidates completely
    binding := LayerStack0.issue_binding(installed AcceptedVersion)
    release reservation
    return AcceptedNew(binding)
```

The `VersionId` reservation is internal concurrency control within the sole
LayerStack-0 owner. It is not a service, a new writer, a Head transition, a
durable reference, or a substitute for full comparison.

## 5. Occupancy, equality, and convergence

For every occupied `VersionId`:

1. LayerStack-0 validates that the occupant is a complete accepted closure.
2. It compares the Candidate and occupant canonical streams from their first
   byte through exact simultaneous end-of-stream.
3. Equal bytes converge on the already installed payload; Candidate staging is
   discarded.
4. Any byte or terminal-length difference returns `Collision` and creates no
   binding or reference.
5. Corruption, missing comparison material, unreadability, unsupported schema,
   or an ambiguous crash prefix fails closed; it never falls back to digest,
   length, tree shape, or payload-path equality.

Concurrent equal Candidates may each build private staging, but the bounded
ID-scoped reservation serializes occupancy resolution. At most one installs an
absent slot. Every later contender performs full canonical comparison and
returns the same physical accepted closure. Speculative private staging does
not violate physical uniqueness because it is neither accepted nor reachable
and is bounded cleanup debt.

## 6. Visibility and linearization

Admission has **no Head linearization point**. Its durable acceptance visibility
point is the Phase 03-qualified installation/fence at which recovery can
recognize exactly one complete immutable accepted closure at the `VersionId`
slot after its payload and comparison material are durable.

Before that point, the transaction is private staging and cannot yield an
AcceptedBinding. After that point, cancellation cannot revoke acceptance; the
operation returns success if possible, otherwise `OutcomeUnknown` is resolved
by re-running ordinary occupancy validation and full comparison.

An `AcceptedBinding` may be issued only after the installed or existing closure
has passed complete revalidation. Reference visibility occurs later in
[reference EphCoW](../02-references-and-publication/01-reference-ephcow.md) or
[OCC publication](../02-references-and-publication/02-occ-publication.md).

## 7. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal, absent ID | Build one complete private closure, durably install it, revalidate it, issue a binding, and clean transaction residue. |
| Normal, equal occupied ID | Revalidate occupant, compare every canonical byte, reuse its physical payload, issue/revalidate its binding, and remove private staging. |
| Normal, unequal occupied ID | Return `Collision`; do not overwrite, alias, select, or publish either value. |
| Concurrent equal admission | Bounded private work may overlap; the ID reservation admits one physical closure and all others full-compare then converge. |
| Concurrent collision | The first complete occupant remains; every mismatching contender fails closed as `Collision`. |
| Retry | Before visibility, retry starts or resumes only a recognizable safe state. After visibility or unknown outcome, occupancy validation plus full comparison returns `AcceptedExisting`; retry never creates a second payload. |
| Cancellation | Before acceptance, stop at a bounded checkpoint and schedule/remove private staging. After acceptance, preserve the AcceptedVersion and report/resolve its accepted outcome. |
| Crash | Recovery classifies private, payload-complete, installed-complete, ambiguous, and corrupt prefixes under [durability and recovery](../04-durability-and-lifecycle/01-durability-and-recovery.md). No incomplete slot becomes accepted. |
| Cleanup | Transaction residue and loser staging are removed in bounded batches. Failure is charged as debt and can backpressure new admission. |

If payload construction reaches ENOSPC or another resource failure, the
algorithm leaves the prior accepted namespace unchanged, records bounded
cleanup debt, releases reservations, and fails. It never publishes a reference
to reclaim space.

## 8. Finite resource accounting and complexity

Let:

- `E` = entry count;
- `B` = complete canonical comparison bytes;
- `V` = logical bytes in the complete filesystem-native payload;
- `M_fs` = filesystem metadata operations needed to construct the closure;
- `S_adm` = reserved private staging capacity, including comparison material;
- `F_adm` = descriptor cap; and
- `W_adm` = bounded concurrent admission workers/reservations.

| Path | Worst-case time | Data I/O | Space/resources |
|---|---:|---:|---:|
| New admission | `O(B + V + E + M_fs)` | Reads `O(B + V)` Candidate/replay data as represented; writes `O(B + V)` private and accepted per-Version material plus `O(M_fs)` metadata operations | At most `S_adm`, `F_adm`, one worker/reservation, bounded memory buffers |
| Equal occupied ID | `O(B + V + E + M_fs)` if private closure was built before occupancy resolution; exact comparison itself is `O(B)` | Candidate staging may write `O(B + V)`; full comparison reads up to `2B`; accepted payload bytes copied/written `0` | Existing payload unchanged; loser staging remains within `S_adm` until cleanup |
| Collision | Same worst-case construction plus `O(B)` comparison | Full comparison stops at first mismatch but worst case reads `2B`; accepted payload unchanged | Bounded diagnostic and cleanup debt |
| Revalidation-only binding | `O(1)` record work plus integrity work selected by Phase 03; any full audit cost must be separately bounded/accounted | Metadata/control reads; no payload copy | Bounded buffers and one capability result |

Admission is byte-moving work and is not covered by the reference-only
`0/0/0` claim. Phase 03 may avoid wasted equal-candidate payload construction
only if it can still validate complete Candidate facts, perform full canonical
comparison, preserve collision behavior, and prevent an occupant from being
trusted by raw ID alone.

Reservations are obtained before growth. If the configured disk, staging,
memory, descriptor, worker, lock-wait, or cleanup-debt bound is unavailable,
admission fails or backpressures before unsafe partial work. No queue or debt
population is unbounded.

## 9. Security and path obligations

- Treat all Candidate paths and metadata as untrusted even after Phase 02; the
  storage write boundary validates them again against the selected portable
  grammar and budget.
- Resolve beneath an already opened private staging root using Phase
  03-qualified no-escape primitives. Reject absolute paths, traversal,
  symlink races, mount crossing, device/special nodes outside policy, hard-link
  escape, and type changes.
- Never concatenate an untrusted `VersionId`, selector, transaction ID, Root
  ID, or fact path into a host path without typed grammar validation and
  anchored resolution.
- Do not extract an archive as accepted readable truth. If a transport archive
  is ever used at an input seam, validate and translate its logical portable
  facts into ordinary bounded staging before admission.
- Make the accepted closure non-writable through ownership, handles,
  permissions, and runtime API shape selected by Phase 03. Permission bits
  alone are not proof if a writable handle remains.
- Avoid logging file bytes, link targets, secrets, or raw host paths in
  collision and corruption diagnostics.

## 10. Observability and test seams

LayerStack-0 emits diagnostic facts after decisions; observers cannot approve
or change them. Required seams include:

- admission attempts/outcomes by typed class;
- new versus existing convergence;
- bytes/entries staged and reserved;
- full-comparison bytes and exact-end completion;
- forced-ID collision tests with equal digest/length but differing bytes;
- staging age/debt, cancellation, ENOSPC, and cleanup outcomes;
- accepted-closure revalidation and corruption/quarantine outcomes; and
- proof that no binding is issued before durable acceptance visibility.

Required tests cover absent, equal occupied, forced collision, concurrent equal
admission, concurrent mismatch, crash at every durable prefix, cancellation at
every bounded checkpoint, over-limit/ENOSPC, path escape, corrupt occupant,
lost response/retry, and physical payload-count convergence.

Metric/event spellings and numeric thresholds are Phase 03 choices, but all new
names use AcceptedVersion/AcceptedBinding/Version terminology.

## 11. Details Phase 03 may still select

Phase 03 selects exact storage paths, accepted metadata/comparison placement,
record/version/checksum formats, staging-state encoding, immutability mechanism,
supported filesystem, lock implementation, fence sequence, cleanup batching,
capability representation, limits, and instrumentation.

It may not select partial/layer reconstruction as readable truth,
digest-or-length equality, accepted-payload mutation, raw-ID references, a
cross-Version object graph, a second writer, or a dependency outside the
selected ownership direction.

## 12. `REOPEN_PHASE_01` conditions

Reopen Phase 01 and identify the exact failed hard rule if evidence proves
that:

- a complete immutable filesystem-native closure cannot be built or kept
  readable as sole Version truth;
- equal canonical Candidates cannot converge on one physical payload without a
  different storage family;
- full occupied-ID canonical-byte comparison cannot be finite and fail closed;
- no supported filesystem can provide complete accepted installation after
  payload durability;
- accepted-payload immutability cannot be enforced through the existing owner
  and direct runtime handoff;
- LayerStack-0 cannot remain the sole issuer/revalidator of AcceptedBindings;
  or
- correctness requires a database, new service/process, second writer,
  parent/layer chain, Chunk/CDC or manifest/Merkle graph, archive-as-truth,
  reflink-required truth, persistent refcount authority, or tracing graph GC.

Exact mechanics satisfying this contract remain `OPEN_WITHIN_R0`.
