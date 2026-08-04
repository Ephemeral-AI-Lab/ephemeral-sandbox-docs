# 04.01 — Durability and recovery

## 1. Purpose and owning phase

**Owner:** Phase 03 — LayerStack-0 durable storage.  
**Purpose:** Define ordering, semantic staging states, crash-prefix outcomes,
fail-closed startup, quarantine, idempotent repair, and bounded recovery without
prematurely selecting a filesystem or exact syscall/fence sequence.

The governing partial orders are:

```text
admission:
complete payload + exact comparison material durable
        before AcceptedVersion visibility
        before AcceptedBinding issuance/revalidation
        before admission success acknowledgement

reference operation:
revalidated AcceptedBinding naming a durable AcceptedVersion
        before complete Head/Root record visibility
        before reference durability acknowledgement
```

Thus every durable reference follows its accepted payload, while ordinary
admission may successfully return an AcceptedBinding before any Head or Root
names it. Admission acknowledgement and reference acknowledgement are distinct
operation boundaries.

Heads and Roots are installed only as complete records. Recovery must expose
the prior truth, the complete new truth, or no readiness; it must never invent
a mixed truth.

## 2. Evidence status

- `SOURCE-VERIFIED`: e497 source contains an existing writer lock and
  atomic-write/fsync-style durability primitive family in the selected package.
  This is an implementation starting point, not proof that any current syscall
  sequence meets V2 crash semantics.
- `SPIKE-VERIFIED`: none; no filesystem-qualification or V2 kill-prefix matrix
  has run.
- `INFERRED`: payload-before-reference order, complete record replacement,
  recognizable staging, generation/checksum validation, and fail-closed
  recovery compose within R0.
- `OPEN`: Phase 03 selects the supported local filesystem profile, exact paths,
  state/record encoding, checksum, generation fence, lock, durable fence
  sequence, quarantine representation, recovery batches, and numeric bounds.

## 3. Contract

Names are semantic roles, not selected filenames, exact records, syscalls, or
Rust APIs.

### Inputs

- A Phase 03-qualified `<LayerStack0Root>` and current control generation.
- Bounded admission/reference transactions from the other algorithms.
- Startup/recovery mode with process/filesystem-exclusive transition authority.
- Finite scan, time, bytes, entries, memory, descriptors, workers, quarantine,
  staging, orphan, and cleanup-debt budgets.

### Preconditions

1. The product-source/store generation is not concurrently writable by another
   LayerStack-0 instance.
2. The local filesystem has passed the exact Phase 03 qualification suite for
   atomic complete-record replacement and required durability fences.
3. Store paths are non-overlapping and resolved through trusted anchored
   handles; no legacy/V2 alias exists.
4. All persisted records are treated as untrusted until bounded parse,
   checksum, schema, generation, and referential validation succeed.
5. New operations are blocked until recovery declares the store ready.

### Outputs

One validated readiness/progress/quarantine/error result plus bounded,
recoverable cleanup debt when explicitly classified. Recovery never fabricates
an AcceptedBinding, Head, Root, or accepted payload from ambiguous evidence.

### Typed outcomes

| Outcome | Meaning |
|---|---|
| `Ready(generation)` | All authoritative control, accepted closures, Heads, Roots, staging, custody, and bounded debt needed for safe operation have been reconciled. |
| `ReadyWithBoundedDebt(generation, debt)` | Only classified non-authoritative cleanup remains and is within enforced limits. |
| `RecoveryProgress(cursor)` | A bounded batch completed but readiness is still withheld. |
| `Quarantined(items)` | Ambiguous/corrupt artifacts were isolated diagnostically; affected truth is not exposed. Readiness may remain withheld. |
| `UnsupportedFilesystem` | The required qualified semantics are unavailable. |
| `UnsupportedFormatOrGeneration` | Control/record schema or generation cannot be safely interpreted. |
| `CorruptOrDanglingReference` | A complete Head/Root fails checksum/generation/binding/reachability validation. |
| `AmbiguousCrashPrefix` | Recovery cannot prove prior or complete new truth from bounded evidence. |
| `RecoveryLimitExceeded` | Inventory, bytes, time, memory, FDs, workers, quarantine, or debt exceeds the finite recovery envelope. |
| `RecoveryIoFailed` | Safe reconciliation could not complete; startup remains fail closed. |
| `Cancelled` | A bounded recovery batch stopped; restart resumes from validated state and readiness remains withheld. |

## 4. Semantic staging states

Every private transaction must be recognizable as exactly one supported
semantic state or as corrupt/unknown. Phase 03 selects the concrete encoding.

| Semantic state | Meaning | Reachable as truth? |
|---|---|---|
| `AllocatedPrivate` | Transaction identity and resource reservation exist; no complete Candidate evidence. | No |
| `CandidateValidatedPrivate` | Complete canonical Candidate and accounting are available privately. | No |
| `PayloadBuildingPrivate` | Filesystem-native closure is incomplete. | No |
| `PayloadCompletePrivate` | Payload and exact comparison material are complete and locally validated but not accepted-visible. | No |
| `AcceptanceInstalling` | Installation/fence may have started; recovery must validate the accepted slot and transaction rather than infer outcome from a flag alone. | Only if complete accepted visibility is proved |
| `AcceptedVisible` | One complete immutable accepted closure is recoverably visible and revalidates. | Yes, as AcceptedVersion; not selected without a reference |
| `ReferencePreparedPrivate` | One complete proposed Head/fixed-Root create record, Head replacement record, or operation-specific exact-removal artifact exists privately. | No |
| `ReferenceVisible` | One operation-appropriate Head/fixed-Root create, Head replace, or exact removal crossed its qualified durable-visibility point. | Yes |
| `CleanupPending` | Only classified non-authoritative residue remains. | No |

State markers, if used, are not sole proof. Recovery cross-checks the complete
closure/record, checksum, schema, generation, and required fence evidence. A
torn, duplicated, unsupported, or contradictory state fails closed.

## 5. Durability protocol constraints

Phase 03 must instantiate a qualified protocol satisfying these partial-order
constraints:

1. Create bounded private staging under a unique typed transaction identity.
2. Write and validate all canonical comparison material and every filesystem
   entry/content byte needed by the complete payload.
3. Prevent future mutation through handles/API/ownership and apply the selected
   payload durability fences.
4. Install one complete accepted closure into the unoccupied `VersionId` slot,
   or full-compare and converge on an existing closure.
5. Apply the selected acceptance-visibility fence and revalidate acceptance.
6. Only then prepare either a complete checksummed, schema-versioned,
   generation-fenced Head/fixed-Root record containing an `AcceptedBinding`, or
   the selected operation-specific artifact for exact conditional removal of a
   fully captured existing record.
7. Under the sole transition gate, apply exactly one of Head create, Head exact
   replace, Head exact remove, fixed-Root create, or fixed-Root exact remove,
   then apply the selected reference durability fence. Only a Head is replaced.
8. Acknowledge success only after the required point is recoverable.
9. Classify remaining private fragments as bounded cleanup debt.

This contract intentionally does **not** name `rename`, `fsync`, directory
syncs, flags, temporary suffixes, or a specific syscall order. Phase 03 must
choose and prove the exact sequence for each supported filesystem; generic
POSIX assumptions are insufficient.

## 6. Crash-prefix classification

| Crash prefix | Recoverable interpretation | Required action |
|---|---|---|
| Before private allocation | No operation exists. | None. |
| `AllocatedPrivate` / partial Candidate | No accepted truth. | Delete/quarantine private residue in a bounded batch. |
| Partial payload build | No accepted truth. | Never expose it; delete/quarantine and charge debt. |
| Complete private payload before installation | No accepted truth yet. | Revalidate then safely discard or resume only under the selected idempotent protocol. |
| Installation started; accepted slot absent | No AcceptedVersion. | Remove private residue; retain no binding. |
| Installation started; one complete accepted slot validates | AcceptedVersion exists. | Converge transaction state on that closure; clean private residue. |
| Both private and accepted complete, same canonical bytes | One accepted closure exists. | Keep accepted closure, remove duplicate private work. |
| Accepted slot and private evidence conflict or cannot be classified | No safe assumption. | Quarantine affected artifacts, block bindings/references/readiness as needed. |
| AcceptedVersion visible, no new Head/fixed-Root edge installed | Valid unreferenced accepted orphan. | Preserve temporarily as bounded debt; retirement handles it exactly. |
| Private reference-transition artifact before the selected operation | Prior complete record or required absence remains truth. | Remove/quarantine the private artifact. |
| Reference transition started, complete prior record or required absence still visible | Prior reference state remains truth. | Clean private residue; caller retry may proceed with the original expectation. |
| Complete new record visible and binding validates, or exact removed record is authoritatively absent | The operation-appropriate new reference state is truth. | Finish bounded residue cleanup; lost response resolves by authoritative read-back. |
| Torn, checksum-invalid, wrong-generation, dangling, or fieldwise mixed record | Truth cannot be proven. | Fail startup/affected access closed and quarantine/alert; never select fields. |
| Crash during cleanup/retirement | Last previously completed authoritative state remains. | Resume idempotent bounded cleanup after exact revalidation. |

Collision ambiguity is never “repaired” by choosing one digest occupant.
Canonical mismatch remains a collision; corrupt equality evidence remains a
fail-closed condition.

## 7. Startup recovery algorithm

```text
recover_layerstack0(root, recovery_budget):
    acquire process/filesystem-exclusive recovery and transition authority
    block admission, references, reads, retirement, and migration writes

    control := bounded_parse_and_validate_control(root)
    require supported format, monotone generation, and qualified filesystem

    inventory in bounded deterministic batches:
        accepted Version slots and per-Version comparison evidence
        complete Heads and typed Roots
        private staging transactions and reference temporaries
        custody/runtime reconciliation facts
        quarantine and cleanup/orphan debt

    if any population or byte bound is exceeded:
        persist only validated bounded progress if protocol permits
        remain not-ready
        return RecoveryLimitExceeded or RecoveryProgress

    for each item:
        classify by complete content, checksum, schema, generation, and relation
        apply only idempotent safe action from the crash-prefix table
        quarantine ambiguity within a finite allowance

    validate through the LayerStack-0 admission-owned verifier that every
        visible Head/Root contains a revalidated AcceptedBinding
    validate no accepted closure is mutable or structurally incomplete
    validate staging/debt/custody populations remain within readiness limits

    publish ready generation through the selected complete control-record fence
    release recovery authority while retaining normal transition authority rules
    return Ready or ReadyWithBoundedDebt
```

Repeating recovery after a crash at any recovery step yields the same or a more
fully cleaned valid state. It never converts untrusted residue into authority
merely because it is old, uniquely named, or digest-matching.

## 8. Visibility and linearization points

- AcceptedVersion durable visibility is the qualified complete accepted-closure
  installation/fence defined in
  [complete Version admission](../01-identity-and-admission/02-complete-version-admission.md).
- A Head state change linearizes only at its conditional complete-record
  replacement under the transition gate, as defined in
  [OCC publication](../02-references-and-publication/02-occ-publication.md).
- Root creation/removal becomes visible at its one complete-record operation;
  it does not add a Head point.
- Recovery readiness becomes visible at the complete generation/control state
  chosen by Phase 03 only after all required classifications pass. It is a
  readiness gate, not Version selection.

Control and staging markers cannot move any of those points earlier.

## 9. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal | Enforce payload-before-acceptance-before-reference order and acknowledge only after qualified fences. |
| Concurrent | Normal mutations are excluded during startup recovery. During operation, the sole transition gate serializes reference/recovery/retirement authority; bounded admissions coordinate occupied slots. |
| Retry | Admission converges through full comparison; reference retry resolves prior/new complete record; recovery actions are idempotent. |
| Cancellation | Before an authoritative visibility point, leave prior truth and classified private debt. After a point, preserve new truth and resolve outcome. Recovery cancellation never enables readiness early. |
| Crash | Classify the exact durable prefix using the table; expose prior, complete new, or no readiness. |
| Cleanup | Operate in finite batches after authoritative truth is established; cleanup failure increases bounded debt and may block readiness/new work. |

## 10. Finite resource accounting and complexity

Let:

- `N_v`, `N_h`, `N_r`, `N_t`, `N_q`, `N_d` = bounded counts of AcceptedVersions,
  Heads, Roots, staging transactions, custody entries, and debt/quarantine items;
- `B_ctl` = total bytes of control/reference/staging metadata inspected;
- `B_verify` = payload/comparison bytes required by the selected integrity
  validation policy for this recovery pass;
- `M_rec`, `F_rec`, `W_rec` = finite recovery memory, descriptor, and worker
  budgets; and
- `K_rec` = maximum items/bytes processed in one recovery batch.

| Operation | Worst-case time/I/O | Space/resources |
|---|---:|---:|
| Full bounded inventory | `O(N_v + N_h + N_r + N_t + N_q + N_d + B_ctl)` metadata work | `O(M_rec)`, `F_rec`, `W_rec`, one exclusive recovery authority |
| Integrity verification | `O(B_verify)` byte reads; no payload writes except safe quarantine/retirement mechanics | bounded streaming buffers; never load an unbounded closure |
| One recovery batch | `O(min(total, K_rec))` classified work | finite progress/control record and debt budget |
| Complete recovery | Linear in all admitted bounded artifacts and bytes selected for verification | total work is finite because store populations/debt were bounded at admission |

If the inventory exceeds its guaranteed bound, recovery does not continue
unbounded or declare ready from a sample. It processes validated finite batches
where safe and remains not-ready until the full required set is reconciled, or
returns `RecoveryLimitExceeded` for operator action. Quarantine itself has a
finite item/byte cap; exceeding it is fail-closed.

## 11. Security and path obligations

- Treat every post-crash filename, directory entry, record length, checksum,
  generation, and type as attacker-controlled/corrupt until validated.
- Enumerate only beneath anchored, non-overlapping LayerStack-0 namespaces.
  Reject symlinks, traversal, hard-link escape, unexpected mount crossing,
  special nodes, aliasing, and unknown entries rather than following them.
- Parse bounded headers before allocation and verify full record length,
  checksum, schema, generation, typed key, and binding capability.
- Quarantine by safe anchored movement/marking selected by Phase 03; quarantine
  is diagnostic isolation, not accepted truth or a hidden second store.
- Never invoke archive extraction, runtime mounts, OverlayFS, or Workspace
  activation during authoritative recovery.
- Prevent stale-generation temporary/control records from replaying after
  migration or restart.
- Keep corrupt content and host paths out of logs; expose bounded identifiers and
  reason classes.

## 12. Observability and test seams

Required facts include startup readiness, format/generation, filesystem
qualification, inventory populations/bytes, crash-prefix class, prior/new
resolution, quarantine count/bytes, dangling/corrupt references, staging/orphan
age, cleanup debt, recovery batch/cursor, limit failures, and time by bounded
stage.

Required Phase 03 qualification and fault tests:

- kill/fault injection before and after every candidate durability boundary;
- prior-or-complete-new Head and Root results with no fieldwise mix;
- payload never referenced before its complete accepted fence;
- checksum, generation, truncated/extended record, stale temp, and dangling
  binding corruption;
- concurrent-instance/recovery lock exclusion;
- unsupported filesystem and fence failure;
- recovery crash/restart at every cleanup/quarantine step;
- excessive staging/debt/quarantine/reader populations fail readiness closed;
- accepted-orphan and reference-temp cleanup is idempotent; and
- no recovery event or metric acts as authority.

Stage 4.6 remains `INCOMPARABLE`; recovery costs are not benchmark guarantees.

## 13. Details Phase 03 may still select

Phase 03 selects exact paths, record schemas/checksums/generations, semantic
state encoding, supported filesystem, transition/recovery lock, qualified
atomic replacement and durability-fence syscall sequence, readiness control,
quarantine mechanics, validation depth, batches, limits, and instrumentation.

It may not acknowledge a reference before payload durability, trust partial or
checksum-invalid records, run unbounded startup work, weaken guarantees on an
unsupported filesystem, or add another writer/recovery authority.

## 14. `REOPEN_PHASE_01` conditions

Reopen Phase 01 with the precise failure if:

- no supported local filesystem can provide the required prior-or-complete-new
  reference outcome after qualified fences;
- complete payload durability cannot precede accepted/reference visibility;
- recognizable bounded staging and idempotent recovery cannot be expressed in
  the selected complete-payload family;
- one LayerStack-0 transition/recovery authority cannot prevent concurrent
  conflicting truth;
- safe startup requires unbounded work or accepting ambiguous/corrupt truth; or
- correctness requires a database, new service/helper process, second writer,
  archive-as-readable-truth, or another storage family.

Exact qualified mechanics that meet the partial order remain
`OPEN_WITHIN_R0`.
