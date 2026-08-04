# 05.01 — One-way migration

## 1. Purpose and owning phases

**Primary owner:** Phase 05 importer/migration integration.  
**Supporting owners:** Phase 03 supplies ordinary LayerStack-0 admission,
references, recovery, and generation controls; Phase 07 performs authorized
cutover; Phase 08 removes temporary compatibility code after the owner-selected
observation window.  
**Purpose:** Translate fenced legacy complete filesystem meaning into ordinary
V2 Candidates, admit them through LayerStack-0, establish V2 references, and
cross one irreversible writable-truth cutover without allowing dual writable
truth.

Migration is one-way at the semantic boundary:

```text
fenced legacy readable value
        -> complete portable Candidate facts
        -> ordinary V2 canonicalization/admission
        -> AcceptedBinding
        -> Head/typed Root through ordinary LayerStack-0 transitions
```

Legacy representation is temporary input. It never becomes V2 identity or the
permanent V2 storage family.

## 2. Evidence status

- `SOURCE-VERIFIED`: e497 legacy layer/squash/depth/merge behavior and source
  locations are frozen Phase 00 evidence; application and runtime owners expose
  seams where temporary importer/routing code can be isolated.
- `SPIKE-VERIFIED`: none; no V2 legacy import, generation-fence, restart, or
  cutover drill has run.
- `INFERRED`: fenced read-only translation plus ordinary R0 admission and a
  monotone one-writer generation can preserve one writable truth and make
  compatibility deletable.
- `OPEN`: Phase 05/07 select exact legacy inventory/mapping, progress/control
  records, generation/fence mechanics, cutover procedure, rollback runbook,
  batches, and limits. `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` remain
  `OWNER_DEC_OPEN`.

## 3. Migration modes and one-writer invariant

The names below are semantic states; exact persisted spellings are phase-owned.

| Mode | Legacy writes | V2 import/artifact writes | V2 product Head writes | Meaning |
|---|---:|---:|---:|---|
| `LEGACY_WRITABLE` | enabled | disabled | disabled | Pre-migration truth. |
| `DRAINING_FENCING` | rejecting new work and draining accepted old work | disabled | disabled | Establish a stable boundary. |
| `LEGACY_READ_ONLY` | disabled | disabled | disabled | Fence proved; legacy is stable input. |
| `IMPORTING_V2` | disabled | one bounded importer through ordinary LayerStack-0 | disabled | Imported AcceptedVersions/Roots/initial Heads are built, but product V2 mutation remains fenced. |
| `V2_VERIFIED` | disabled | retry/verification only | disabled | Required imports and equivalence checks passed. |
| `V2_WRITABLE_LEGACY_READ_ONLY` | disabled permanently | ordinary V2 work only | enabled | Irreversible writable-truth cutover committed. |
| `OBSERVING` | disabled permanently | ordinary V2 work only | enabled | Temporary read/diagnostic compatibility remains for an owner-selected duration. |
| `COMPAT_REMOVABLE` | disabled permanently | ordinary V2 work only | enabled | Temporary importer/routing code is eligible for deletion. |

At no point are legacy and V2 selected-Version writers both enabled. During
`IMPORTING_V2`, the bounded importer may create V2 artifacts only because the
legacy writer is fenced and V2 product publication is disabled. Every import
uses LayerStack-0's existing sole writer/transition authority; the importer is
not a second durable owner.

## 4. Contract

Conceptual names express responsibility and type flow, not selected commands,
wire APIs, Rust signatures, or control filenames.

### Inputs

- A validated migration mode/generation and exclusive migration authority.
- A finite legacy inventory captured behind the legacy write fence.
- Legacy decoder access sufficient to produce one stable complete logical
  filesystem value per import unit.
- Mapping policy for legacy product references to typed V2 Head/Root seams,
  without importing legacy IDs as authority.
- Phase 02/03 limits plus finite migration bytes, entries, scratch, memory, FDs,
  workers, batches, retry, quarantine, and debt budgets.

### Preconditions

1. Product source/store seals and migration generation match the authorized
   run; stale workers fail their fence checks.
2. Legacy writes are disabled and drained before any V2 import artifact becomes
   authoritative.
3. V2 product Head writes remain disabled until the irreversible cutover
   commit.
4. Legacy and V2 namespaces are physically non-overlapping.
5. The importer can read a stable complete legacy meaning; partial/delta facts
   are reconstructed only at the temporary legacy decoder seam.
6. LayerStack-0 is ready and all translated data passes ordinary Candidate
   validation and admission.

### Outputs

One typed per-unit import, progress, cutover, rollback, cancellation, or error
result. Successful import outputs contain ordinary LayerStack-0-issued
AcceptedBindings and typed V2 references, never legacy identity authority.

### Typed outcomes

| Outcome | Meaning |
|---|---|
| `ImportUnitCommitted(binding, progress)` | One legacy unit became an ordinary AcceptedVersion, required V2 reference work became durable, and restartable progress advanced. |
| `ImportUnitAlreadyCommitted(binding)` | Retry found the same canonical bytes/reference result and converged without duplicate payload. |
| `LegacyFenceChanged` | Legacy generation or stable-read proof changed; discard private work and stop. |
| `LegacyValueInvalidOrIncomplete` | A complete portable logical value cannot be reconstructed safely from the legacy unit. |
| `V2ValidationOrAdmissionFailed(reason)` | Ordinary Phase 02/03 validation, collision, resource, filesystem, or durability rule failed. |
| `EquivalenceFailed` | Imported portable facts do not match the qualified legacy logical value under the selected verification. |
| `MigrationLimitExceeded` | Finite inventory, bytes, entries, scratch, workers, time, quarantine, or debt bound would be exceeded. |
| `RollbackCompletedPreCommit` | Before the irreversible cutover, V2 product writes remained disabled and legacy writer was safely re-enabled under a new fence. |
| `CutoverCommitted(generation)` | One durable generation/control transition permanently enabled V2 product writes and kept legacy writes disabled. |
| `PostCommitRollbackForbidden` | The cutover commit was crossed; legacy writable rollback is prohibited. |
| `Cancelled` / `OutcomeUnknown` | Stop at a bounded checkpoint or resolve a durability-edge result through generation/progress/reference revalidation. |

## 5. Fenced import algorithm

```text
begin_migration(expected_generation):
    require mode == LEGACY_WRITABLE
    enter DRAINING_FENCING through existing application control seam
    reject new legacy mutations and drain all earlier accepted writers
    verify no live legacy writer can commit under the next generation
    durably enter LEGACY_READ_ONLY
    enable one bounded importer; keep V2 product publication disabled
    enter IMPORTING_V2
```

```text
import_unit(legacy_key, expected_generation, progress):
    validate generation/mode before allocating or reading
    require legacy writes remain fenced and V2 product writes disabled

    legacy_view := legacy_decoder.capture_complete_stable_value(
                       legacy_key, finite_budget, expected_generation)
    if generation changed: discard private work; return LegacyFenceChanged

    portable_facts := translate logical complete filesystem facts only
        do not copy legacy identity/history/runtime fields

    candidate := Phase02.canonicalize_candidate(portable_facts, finite_budget)
    if candidate failed: return V2ValidationOrAdmissionFailed(candidate.reason)
    if generation/mode changed:
        discard private Candidate work; return LegacyFenceChanged

    admitted := LayerStack0.admit_complete_version(candidate)
    if admission failed: return V2ValidationOrAdmissionFailed(admitted.reason)
    binding := admitted.AcceptedBinding

    if generation/mode changed:
        release operation custody; classify accepted orphan for ordinary cleanup
        return LegacyFenceChanged

    if target is a branch/head:
        CreateHeadIfAbsent(head_identity, Expected::Absent, binding)
    else if target is an explicit restore point:
        CreateFixedRootIfAbsent(root_identity, Checkpoint,
                                Expected::Absent, binding)
    else:
        return InvalidMigrationTarget
    use the ordinary LayerStack-0 binding revalidation, transition authority,
        complete-record durability boundary, outcomes, and read-back protocol
    if reference work failed:
        release operation custody; classify any accepted orphan; return failure
    verify imported portable value/reference mapping under bounded policy
    if equivalence failed: stop progress and return EquivalenceFailed

    durably advance checksummed/generation-fenced progress only after all
        authoritative V2 outcomes for this unit are recoverable
    return ImportUnitCommitted(binding, progress)
```

If a unit is retried before progress advancement, ordinary admission performs
full occupied-ID canonical comparison and converges on one physical payload.
Exact same-record `CreateFixedRootIfAbsent` and `CreateHeadIfAbsent` read-back is
idempotent. `ALREADY_EXISTS` with a nonidentical record, a conflicting mapping,
or canonical mismatch fails closed; progress never skips it. An
`OUTCOME_UNKNOWN` result is resolved by authoritative reference read-back
before retry or progress advancement.

## 6. Legacy translation boundary

The temporary legacy decoder may understand layer IDs, parents, depths,
whiteouts, squash/merge records, archives, mount paths, or host paths only to
derive the final complete logical filesystem value. Translation emits portable
complete-Version facts and discards the representation history.

The following may not enter V2 canonical bytes, `VersionId`, AcceptedBinding,
Head, or Root authority:

- legacy layer, parent, depth, squash, merge, or delta IDs;
- whiteout encoding or OverlayFS implementation artifacts;
- archive offsets/order/compression or extraction paths;
- mount, namespace, OverlayFS lower/upper/work, Docker/OCI, device/inode, or
  host absolute paths;
- legacy writer generations except as temporary migration control;
- sessions, leases, authorization decisions, scores, provenance side channels,
  and process/worker facts.

If a legacy value cannot be reduced to one valid complete portable Version, the
unit blocks cutover. The importer cannot preserve it by adding legacy history to
V2 identity.

## 7. Restartable progress and generation fencing

- Every importer worker validates the expected monotone generation before a
  batch, before authoritative reference work, and before progress advancement.
- Progress records are complete, checksummed, generation-fenced, bounded, and
  monotone. Exact encoding and storage location are Phase 05 choices.
- Progress describes completed import units; it is not Version truth and cannot
  issue/revalidate a binding.
- Progress advances only after the AcceptedVersion and required Root/Head record
  are durable and revalidated.
- A crash after admission but before progress may leave a valid orphan or
  already-created reference. Retry full-compares and resolves the ordinary
  result before advancing once.
- A crash after progress never permits the corresponding authoritative V2
  result to be missing; a dangling progress/result pair blocks migration closed.
- Work is finite per batch, and a restart resumes from validated progress rather
  than scanning or trusting unbounded caller state.

## 8. Cutover and rollback

### Verification before cutover

`IMPORTING_V2 -> V2_VERIFIED` requires:

1. all required inventory units classified and within bounds;
2. each imported AcceptedVersion/reference revalidated;
3. qualified semantic equivalence evidence for all required values;
4. no collision, corrupt/dangling reference, unbounded debt, stale generation,
   or unsupported filesystem;
5. legacy writes still fenced and V2 product writes still disabled; and
6. application/runtime integration and rollback/cutover drills passing their
   later-phase gates.

### Irreversible cutover

```text
commit_cutover(expected_generation):
    require mode == V2_VERIFIED
    require all readiness/equivalence/resource gates still pass
    acquire existing application migration control and LayerStack-0 transition authority
    revalidate legacy writer disabled and no stale generation can commit
    install one complete next-generation control state:
        V2 product Head writes enabled
        legacy writes disabled permanently
    apply qualified durability fence
    release authorities
    enter V2_WRITABLE_LEGACY_READ_ONLY
```

The durable generation/control replacement is the writable-truth cutover point,
not a second Head mutation point. Any initial/migrated Head creation uses the
same ordinary conditional complete Head-record operation defined in
[OCC publication](../02-references-and-publication/02-occ-publication.md).

### Rollback boundary

- Before `CutoverCommitted`, rollback may stop import, remove/quarantine private
  staging, remove temporary Branch Heads only with
  `RemoveHead(Expected::Exact(expected_head))`, remove temporary fixed Roots
  only with `RemoveFixedRoot(Expected::Exact(expected_root))`, leave unreachable
  AcceptedVersions for ordinary exact retirement, verify V2 product writes
  never became enabled, advance a fence, and only then re-enable the legacy
  writer. `OUTCOME_UNKNOWN` removals require authoritative read-back; no direct
  record deletion is a migration shortcut.
- At every step, zero or one writer is enabled. Rollback cannot briefly enable
  both.
- After `CutoverCommitted`, legacy writable rollback is forbidden. Operational
  response may stop V2 writes or serve read-only while repairing V2, but it may
  not make legacy writable truth again.
- Deleting legacy data is a separate explicitly authorized operation after
  compatibility-code deletion gates; it is not implied by cutover.

## 9. Temporary compatibility deletion

After entering `OBSERVING`, the duration remains `DEC-011 OWNER_DEC_OPEN`.
When its selected exit gates pass, Phase 08 deletes as one auditable unit:

- legacy decoders/importers and representation translators;
- legacy/V2 routing, dual-read comparison, feature flags, and migration-only
  generation/progress branches;
- temporary configs, commands, tests/fixtures used only for compatibility;
- permanent V2 call-site dependencies on legacy layer/depth/squash/merge/
  whiteout semantics; and
- obsolete documentation claiming legacy behavior is V2 truth.

Deletion must be verified by source/dependency searches and tests. Keeping
compatibility permanently because an observation duration is undecided is not
an accepted outcome. `DEC-001` audit/provenance handling remains an application
side channel; its resolution cannot keep legacy storage as Version truth.

## 10. Visibility and linearization points

- Each imported AcceptedVersion uses the ordinary admission durable-visibility
  point from [complete Version admission](../01-identity-and-admission/02-complete-version-admission.md).
- Each imported Root/Head uses the ordinary complete-reference operation; every
  Head state change uses the package's one conditional Head-record replacement.
- Import progress becomes durable only after those points and has no authority
  over them.
- The writable-truth cutover linearizes at one complete generation/control
  replacement that disables legacy writes and enables V2 product writes under
  the qualified fence.
- Pre-commit rollback linearizes at a later fenced mode transition only after it
  proves V2 product writes remained disabled. Post-commit legacy writable
  rollback has no valid transition.

## 11. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal | Fence legacy, translate complete portable facts, use ordinary admission/references, verify, cut over once, observe, and delete compatibility. |
| Concurrent legacy request | Generation/mode rejects work not ordered before the drain boundary; no stale legacy worker can commit after the fence. |
| Concurrent importer workers | Bounded workers claim non-overlapping units; duplicate work converges through canonical full comparison and idempotent reference/progress rules. |
| Retry | Revalidate generation and durable outcomes; never trust progress alone or create duplicate payloads. |
| Cancellation | Stop between bounded units, preserve last durable progress/reference truth, clean private staging, and keep current writer mode unchanged. |
| Crash | Recovery validates mode, generation, progress, accepted artifacts, and references; it resumes or fails closed without enabling both writers. |
| Cleanup | Private work and orphans use ordinary bounded cleanup; temporary code/config/tests are removed after authorized observation gates. |
| Rollback | Permitted only before cutover commit and only through a fence that proves V2 product writes stayed disabled. |

## 12. Finite resource accounting and complexity

Let:

- `N_l` = legacy import unit count;
- `L` = legacy bytes read to reconstruct complete values;
- `E` = total portable entries translated;
- `B` = total V2 canonical bytes;
- `V` = total complete V2 payload bytes written;
- `R_m` = migration mapping/progress/reference metadata bytes;
- `S_m` = migration staging/scratch cap;
- `F_m`, `W_m` = descriptor and worker caps;
- `K_m` = maximum units/bytes per batch; and
- `D_m` = migration orphan/quarantine/cleanup-debt cap.

| Operation | Worst-case time | Data I/O | Space/resources |
|---|---:|---:|---:|
| Legacy capture/translation | `O(L + E log E)` subject to selected ordering | Reads `O(L)` legacy truth; emits `O(B)` portable/canonical data | `S_m`, `F_m`, `W_m`, finite path/entry/content limits |
| V2 admission | `O(B + V + E)` plus ordering/metadata costs from [complete Version admission](../01-identity-and-admission/02-complete-version-admission.md) | Reads canonical/source bytes, writes one complete payload; retry may full-read up to `2B` comparison bytes | ordinary bounded LayerStack-0 staging |
| Reference/progress | `O(1)` per bounded record/unit plus fence wait | bounded Head/Root/control/progress metadata | record buffers and one transition authority |
| Complete migration | `O(L + B + V + E log E + R_m)` | linear in all qualified imported bytes plus bounded metadata/retries | bounded batches; total accepted store sized by admission quotas |

If any inventory, unit, value, path, scratch, memory, FD, worker, runtime,
quarantine, or debt bound is exceeded, migration stops closed at its last
validated generation/progress point. It does not skip the unit, silently
truncate facts, enable both writers, or weaken canonical comparison.

Stage 4.6 is `INCOMPARABLE`; these are asymptotic obligations, not a migration
duration or performance guarantee.

## 13. Security and path obligations

- Treat legacy inventory, records, filenames, link targets, archives, and
  metadata as untrusted. Validate lengths/counts before allocation or
  decompression and charge logical output bytes.
- Use anchored read-only legacy access after the fence. Reject traversal,
  symlink/hard-link escape, mount crossing, special nodes outside the portable
  profile, archive path escape, duplicate normalized paths, and changing input.
- Never write through a legacy path during import and never let a legacy path
  choose a V2 storage path.
- Validate typed migration keys, generations, progress, Head/Root mappings, and
  AcceptedBindings. Raw legacy IDs and raw V2 digests cannot become references.
- Keep importer privileges within existing application/LayerStack-0/runtime
  seams; it is not a daemon, service, helper writer, or storage facade.
- Bound diagnostics and redact file contents, secrets, legacy host paths, and
  authorization data.

## 14. Observability and test seams

Required diagnostic facts include current mode/generation, active writer kind,
drain status, inventory/progress totals, legacy/canonical/payload bytes,
per-unit outcome/retry, equality/collision, mapping/equivalence status,
staging/orphan/quarantine debt, stale worker rejection, cutover/rollback point,
observation state, and compatibility-deletion checklist.

Required tests/drills:

- stale legacy writers and stale importer generations cannot commit;
- every mode has zero or one enabled writer as specified;
- legacy layers/parents/depth/whiteouts/mount/host facts affect decoding only and
  never canonical bytes;
- crash before/after admission, reference, progress, verification, cutover, and
  rollback fences resumes idempotently;
- duplicate imports converge on one physical payload through full comparison;
- forced collision blocks progress/cutover;
- corrupt/incomplete/over-limit legacy values fail closed;
- pre-commit rollback never overlaps writers; post-commit legacy writable
  rollback is rejected;
- all imported Heads/Roots contain revalidated AcceptedBindings;
- compatibility code/config/tests/call sites are absent after Phase 08; and
- observability corruption cannot advance progress, verify equivalence, enable a
  writer, commit cutover, or authorize deletion.

## 15. Details owning phases may still select

Phase 05 selects exact inventory, mapping, progress, generation, importer API,
batching, verification, and limits. Phase 07 selects the authorized operational
cutover/runbook inside the one-writer protocol. Phase 08 selects the exact
source/config/test deletion checklist after the owner-decided observation seam.

No phase may import legacy representation into V2 identity, bypass ordinary
admission, permit dual writable truth, re-enable legacy writes after cutover, or
make compatibility permanent.

## 16. Open owner decisions

- `DEC-001`: exact `file_blame` fidelity/acceptable break remains an
  application-owned provenance side channel.
- `DEC-011`: exact observation duration remains open; it cannot weaken the
  one-writer fence or eliminate eventual code deletion.
- `DEC-017`: exact operation surface/sessionless writes remains at the API seam;
  any permitted mutation uses ordinary Candidate admission/publication.
- `DEC-018`: authorization/revoke ordering remains at the application seam and
  cannot add a second store authority or writer.

## 17. `REOPEN_PHASE_01` conditions

Reopen Phase 01 with the specific failure if:

- legacy truth cannot be translated into bounded complete portable Version
  facts without making legacy/runtime-private representation canonical;
- migration cannot maintain zero or one writable selected-Version truth across
  drain, import, rollback, and cutover;
- imported data cannot use ordinary LayerStack-0 validation, full comparison,
  admission, bindings, and reference operations;
- generation fencing cannot prevent stale legacy or V2 writers through existing
  owner seams;
- compatibility/import code cannot be isolated and deleted after cutover; or
- an owner decision requires permanent dual truth, legacy history as Version
  identity, a second writer, or a new service/storage family.

Exact progress, generation, batching, and runbook mechanics that preserve these
laws remain `OPEN_WITHIN_R0`.
