# 06.01 — Resources, complexity, and observability

## 1. Purpose and owning phases

**Owners:** Phase 02 owns identity limits; Phase 03 owns LayerStack-0 storage,
recovery, custody, cleanup, and instrumentation limits; later integration,
migration, qualification, and operations phases measure their own effects.  
**Purpose:** State honest worst-case costs, enforce finite resource admission,
separate reference I/O from byte-moving work, and define diagnostic proof seams
without turning observability into authority.

This file provides shared variables and accounting rules for every package
algorithm. Numeric values and exact metric names remain phase-owned.

## 2. Evidence status

- `SOURCE-VERIFIED`: Phase 00 measured the sealed e497 base and verified current
  owners/package direction. Existing measurements describe current artifacts,
  not V2 performance.
- `SPIKE-VERIFIED`: none; no V2 resource, scale, cleanup, or performance spike
  has run for this package.
- `INFERRED`: finite reservations, incremental charging, backpressure, bounded
  cleanup, and scope-separated counters are required for the selected R0
  algorithms to fail closed.
- `OPEN`: Phases 02/03 select numeric limits, reservation implementation,
  filesystem accounting model, queue/batch policy, telemetry names, cardinality
  controls, and operational targets after evidence.

Stage 4.6 remains `INCOMPARABLE`. Its historical samples lack a matched source
closure and rerun provenance. Nothing in this package says R0 won a benchmark,
meets a latency/throughput/storage target, or is production-ready.

## 3. Shared variables

All variables denote validated finite totals, not caller assertions.

| Variable | Meaning |
|---|---|
| `E` | Portable entry count in one Candidate/Version. |
| `B` | Complete canonical-byte length, including content encoded by Phase 02. |
| `P_path` | Aggregate portable path bytes; `D_path` is maximum path depth. |
| `V` | Logical bytes in one complete filesystem-native payload closure. |
| `C` | Canonical bytes examined by one equality comparison; `C <= max(B_left, B_right)` per stream and worst-case both complete streams are read. |
| `Ops_fs` | Filesystem metadata operations for construction, fencing, activation, or reclamation. |
| `R_rec` | Maximum bytes in one complete Head/Root/control/staging record. |
| `N_v`, `H`, `R` | AcceptedVersion, Head, and typed Root populations. |
| `Q` | Active bounded read/operation/migration/recovery custody population. |
| `T`, `S_tx` | Active staging transactions and maximum reserved bytes per transaction. |
| `D_n`, `D_b` | Cleanup/quarantine/recovery debt items and bytes. |
| `L`, `N_l` | Legacy bytes and import-unit count processed by migration. |
| `A_read`, `A_write`, `A_copy` | Payload bytes read, written, or copied by runtime activation/materialization—not by reference operations. |
| `B_ctl`, `B_verify` | Control/reference metadata bytes and payload/comparison bytes inspected by recovery. |
| `Mem`, `FD`, `W` | Per-operation or global memory, descriptor/handle, and worker budgets. |
| `L_gate`, `L_id` | Bounded wait for the sole transition gate and an internal VersionId admission reservation. |
| `K` | Maximum items/bytes/time processed in one cleanup, recovery, or migration batch. |

Every population and total has both a per-operation and store/process-wide cap,
with checked arithmetic. Physical disk accounting may conservatively exceed
logical bytes to cover metadata, allocation units, comparison material,
temporaries, and incomplete cleanup.

## 4. Resource admission contract

Conceptual names express responsibility, not a selected API.

### Inputs

- Typed operation class and validated preliminary size/count estimates.
- Current authoritative resource reservations and cleanup debt maintained by the
  owning LayerStack-0/runtime/application component.
- Finite per-operation, per-tenant/application where applicable, process, store,
  filesystem, and time budgets.
- Cancellation/deadline and operation scope for diagnostic accounting.

### Preconditions

1. Untrusted lengths/counts are parsed with checked arithmetic before allocation.
2. Expensive discovery proceeds incrementally and charges before resource
   growth when exact totals are not known initially.
3. Resource accounting is owned by the component that allocates the resource;
   diagnostic exporters are not consulted for correctness.
4. Debt caps reserve enough capacity to clean already admitted work.
5. The sole Head transition gate remains distinct from resource-budget locks;
   lock order is fixed and bounded.

### Typed outcomes

| Outcome | Meaning |
|---|---|
| `ResourcesReserved(token)` | Finite capacity is atomically charged for the bounded operation. |
| `Backpressured(retry_class)` | Capacity may become available after bounded cleanup/release; no unsafe partial work begins. |
| `LimitExceeded(kind)` | Input or existing population exceeds a hard bound. |
| `DiskReserveUnavailable` | Safe staging plus cleanup headroom cannot be reserved. |
| `DeadlineOrLockLimit` | Bounded worker/queue/lock-wait policy rejected the operation. |
| `Cancelled` | Reservation/work stopped at a safe checkpoint; resources are released or charged as cleanup debt. |
| `AccountingCorrupt` | Overflow, negative/inconsistent totals, or missing authoritative reservation state; owner fails closed. |

### Outputs

A reservation token scopes authoritative charges to one operation. It may be
converted at an underlying durable point from staging usage to accepted payload
or cleanup-debt usage, then released only when the actual resource is gone. It
is not a VersionId, AcceptedBinding, Root, Head, custody token, or selection
authority.

## 5. Bounded accounting algorithm

```text
begin_bounded_operation(kind, estimates, limits):
    validate kind and checked estimates
    compute conservative bytes, entries, Mem, FD, W, queue, and debt headroom
    atomically reserve within the owning component's finite budget
    if unavailable: return Backpressured or LimitExceeded
    return ResourcesReserved(token)

run_bounded_operation(token, work):
    for each bounded unit:
        cancellation_checkpoint()
        discover next logical/physical charge
        checked_add and reserve before allocation/read expansion/write growth
        if charge unavailable:
            stop before the next authoritative visibility point where possible
            preserve prior truth; classify private work as bounded debt
            return typed resource failure
        perform work and record authoritative accounting

    at underlying algorithm's visibility point:
        atomically convert reservation category as required
        # e.g. staging -> AcceptedVersion, or reference temp -> Head record

    emit best-effort bounded diagnostic facts after the decision
    release only resources actually reclaimed
```

Metrics may mirror charges but never replace the authoritative in-process/
on-disk resource ledger needed to prevent overcommit. Loss, delay, duplication,
or corruption of telemetry cannot create capacity or change an algorithm
outcome.

## 6. Worst-case algorithm costs

The table states required honest upper-order accounting. Filesystem constants,
allocation behavior, cache effects, and exact codec choices may change factors
but not erase required byte terms.

| Algorithm/path | Worst-case time | Required data I/O and metadata |
|---|---:|---|
| Canonical validation/order | `O(B + P_path + E log E)` for comparison sorting; selected streaming/external ordering may alter the sort implementation | Read all portable facts/content; emit/retain `O(B)` canonical data; `O(E)` logical metadata |
| Typed `VersionId` derivation | `O(B)` | Consume every canonical byte; fixed digest state plus bounded buffers |
| Full occupied-ID equality | First mismatch may stop early; worst case `O(C)` with `C = B` for equal streams | Read up to both complete canonical streams, worst-case `2B`; digest/length equality never short-circuits success |
| New complete admission | `O(B + V + E + Ops_fs)` plus canonical ordering | Read Candidate/canonical data; write `O(B + V)` per-Version comparison/payload staging and accepted material; metadata/fence operations charged |
| Equal occupied admission | New-admission staging worst case plus `O(B)` full comparison | May write private `O(B + V)` before convergence; reads up to `2B` comparison bytes; accepted payload bytes written/copied `0/0` |
| Collision | Same construction worst case plus comparison to last differing byte | Up to `2B` comparison reads; accepted occupant unchanged; private cleanup charged |
| Five accepted-reference operations | `O(1) + L_gate` for bounded fixed-size records | `CreateHeadIfAbsent`, `ReplaceHead`, `RemoveHead`, `CreateFixedRootIfAbsent`, and `RemoveFixedRoot` use `O(R_rec)` reference metadata; accepted-reference payload read/write/copy exactly `0/0/0` |
| Head publication of AcceptedBinding | `O(1) + L_gate` | One complete Head read and at most one complete Head write/fence; Head-transition payload `0/0/0` |
| Candidate admission + publication | Admission cost plus `O(1) + L_gate` | Admission byte I/O plus bounded Head metadata; stale may leave one charged accepted orphan |
| Read capture/custody | `O(1) + L_gate` | Bounded reference/custody metadata; payload `0/0/0` before runtime consumption |
| Runtime activation/materialization | `O(A_read + A_write + A_copy + Ops_fs)` | All actual accepted payload reads and runtime-private writes/copies are charged in the activation scope |
| Recovery | `O(N_v + H + R + T + Q + D_n + B_ctl + B_verify)` for a complete bounded pass | Reads all required metadata and selected integrity bytes; quarantine/cleanup writes charged separately |
| Retirement decision | `O(H + R + Q)` | Exact reference/custody metadata scan; payload content `0/0/0` for decision/detach |
| Physical whole-closure reclamation | `O(E + filesystem_reclaim(V))` | Filesystem metadata/reclamation proportional to closure; no need to read/copy content, but physical cost is implementation-dependent |
| Complete migration | `O(L + B + V + E log E + N_l * R_rec)` plus verification/retry | Reads stable legacy values, writes ordinary V2 complete payloads, and records bounded progress/references |

`O(1)` refers only to bounded record-sized control work. It does not mean zero
syscalls, zero record bytes, zero lock wait, or zero durability cost.

## 7. Resource dimensions and failure behavior

| Resource | Owner and bound | Exhaustion behavior |
|---|---|---|
| Canonical/payload/staging bytes | Phase 02 validates logical totals; LayerStack-0 reserves physical staging plus cleanup headroom | Reject/backpressure before growth; leave no accepted partial closure |
| Entries, path bytes/depth, metadata/link populations | Phase 02 portable-fact limits; revalidated at storage/import boundaries | `InvalidPortableFact` or `LimitExceeded`; never truncate or skip |
| Store AcceptedVersions/Heads/Roots | LayerStack-0 finite store limits | Reject new admission/reference; preserve existing truth |
| Memory | Allocating owner, per-operation and global | Stream/spill only within selected bounds or fail closed |
| FDs/handles/mounts/namespaces | LayerStack-0 or runtime-effect owner | Reserve before open/create; close in reverse lifecycle order; fail/backpressure at cap |
| Workers/queues | Owning component with bounded queue and worker pool | Reject/backpressure; no unbounded task spawn |
| Transition lock | One LayerStack-0 process/filesystem-exclusive authority | Bounded wait/timeout outcome; never bypass or add a second writer |
| VersionId admission reservation | LayerStack-0 bounded internal concurrency | Serialize an occupied slot; bounded wait; never substitute for equality |
| Read/operation custody | LayerStack-0 with `Q_max` and lifecycle/reconciliation bounds | Reject new capture/use; never drop custody to satisfy quota |
| Recovery/migration batches | Phase 03/05 `K` and progress bounds | Make validated bounded progress while readiness/writer fence remains closed |
| Staging/orphan/quarantine/cleanup debt | LayerStack-0 `D_n`/`D_b`, age and batch caps | Backpressure new debt, possibly fail readiness, preserve authoritative truth |
| Observability events/cardinality | Diagnostic owner with finite buffers/labels | Drop/coalesce diagnostics according to policy; never change correctness state |

Cleanup capacity is reserved when work is admitted. A cleanup failure converts
the exact resource to bounded debt; it does not release accounting early.
Integer overflow, underflow, inconsistent generations, or missing accounting
evidence is `AccountingCorrupt` and fails closed.

## 8. Reference zero-payload-I/O proof counters

Each reference-only operation has a scoped I/O classifier below the payload
access layer. Exact names are Phase 03-owned; new names must use Version
vocabulary. The conceptual counters are:

```text
layerstack0_version_reference_payload_bytes_read_total
layerstack0_version_reference_payload_bytes_written_total
layerstack0_version_reference_payload_bytes_copied_total

layerstack0_version_reference_record_bytes_read_total
layerstack0_version_reference_record_bytes_written_total
layerstack0_version_reference_metadata_operations_total
```

For `CreateHeadIfAbsent`, `ReplaceHead`, `RemoveHead`,
`CreateFixedRootIfAbsent`, and `RemoveFixedRoot`, including retry, conflict,
not-found, lost-response/read-back, and cleanup paths, tests must report:

```text
payload bytes read    = 0
payload bytes written = 0
payload bytes copied  = 0
```

Proof requires more than dashboards:

1. the ReferencePlane type has no payload accessor;
2. build/dependency checks reject payload/materialization imports;
3. an injected payload accessor traps if called;
4. operation-scoped I/O classification distinguishes payload from
   reference/control paths;
5. syscall/filesystem tracing in qualification confirms allowed path classes;
6. counters are asserted for normal, stale/conflict, retry, cancellation,
   injected failure, and crash-prefix outcomes; and
7. admission and runtime activation use separate scopes whose nonzero byte costs
   remain visible.

A missing metric sample cannot authorize or invalidate a reference after the
fact. It fails the proof/qualification gate and is repaired as instrumentation,
while authoritative types and negative capabilities preserve runtime safety.

## 9. Visibility and linearization

Resource reservation has an internal budget-admission point but no Version,
Head, Root, or migration-truth authority. Converting a reservation follows the
underlying algorithm's already defined point:

- Candidate completion: no durable point;
- AcceptedVersion: complete accepted-closure visibility;
- Head: one conditional complete Head-record replacement;
- Root: one complete Root-record operation;
- read: custody installation relative to retirement;
- retirement: complete accepted-slot detach after final revalidation; and
- migration: complete generation/control cutover for writable truth.

Emitting a counter, log, trace, alert, or dashboard update is never a
linearization or durability point.

## 10. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal | Reserve conservatively, charge incrementally, convert at the underlying durable point, emit bounded facts, and release after actual cleanup. |
| Concurrent | Atomic budget reservations prevent aggregate overcommit; finite workers/queues and fixed lock order prevent unbounded contention. |
| Retry | Charge each actual attempt; reuse/release only validated reservations; idempotent outcomes do not hide prior staging or comparison cost. |
| Cancellation | Stop at bounded checkpoints, preserve underlying truth, release reclaimed resources, and charge remaining private work as debt. |
| Crash | Recovery rebuilds/validates authoritative accounting from bounded accepted/control/staging facts; missing or inconsistent accounting blocks readiness. |
| Cleanup | Work in `K`-bounded batches, retain debt until actual reclamation, and backpressure before exceeding `D_n`/`D_b`. |

## 11. Security obligations

- Parse and combine untrusted sizes/counts using checked arithmetic; reject
  overflow, decompression bombs, sparse/allocated-size surprises outside the
  selected policy, deep paths, and metadata amplification.
- Charge logical and conservative physical bytes before allocation/write;
  filesystem-reported free space is not a sole correctness guarantee.
- Bound labels, reason strings, IDs, trace payloads, queue cardinality, and log
  rate. Never use raw paths, file contents, secrets, arbitrary metadata, or
  high-cardinality request values as diagnostic labels.
- Keep resource tokens and custody unforgeable and generation-scoped. Diagnostic
  counter values cannot be replayed as tokens.
- Avoid deadlocks by selecting and testing one lock order; timeouts return typed
  failures without acquiring a second writer path.
- Treat accounting/control corruption as fail-closed and quarantine evidence
  without letting cleanup delete authoritative truth.

## 12. Observability and test seams

Beyond the zero-I/O counters, required facts include:

- canonical/candidate bytes, entries, paths/depth, compare bytes and exact-end;
- staging/accepted/orphan/quarantine/cleanup bytes and item counts;
- admission new/existing/collision outcomes;
- Head expected/current/same/stale and gate wait;
- active custody count/age and retirement deferral;
- recovery inventory, batches, readiness, corruption, and debt;
- migration mode/generation, active writer kind, progress, and fence rejection;
- memory/FD/worker/queue reservations and high-water marks; and
- runtime activation payload read/write/copy bytes in a separate scope.

Required tests include exact-limit boundary values, checked-integer overflow,
aggregate concurrent reservation, queue/worker/FD exhaustion, ENOSPC and
metadata exhaustion, cancellation/crash resource reconciliation, debt
saturation/backpressure, high-cardinality/redaction checks, and instrumentation
loss/corruption proving it cannot change authority.

Observability is a diagnostic reader only. It may not issue/revalidate an
AcceptedBinding, choose an equality result, advance a Head, create a Root,
install custody, decide retirement, mark import progress, enable a writer, or
declare recovery safe.

## 13. Details owning phases may still select

Phase 02 selects identity-related numerical limits and streaming/scratch
strategy. Phase 03 selects physical accounting, store populations, staging/
debt quotas, memory/FD/worker/lock/custody limits, batches, record sizes, and
metric/event spellings. Later phases select deployment budgets and evidence-
based targets without weakening correctness.

No phase may claim constant byte cost for complete identity/admission, hide
runtime activation under the reference `0/0/0` scope, run unbounded recovery or
cleanup, or turn diagnostics into correctness authority.

## 14. `REOPEN_PHASE_01` conditions

Reopen Phase 01 with the exact architecture-changing failure if:

- complete canonicalization, occupied-ID comparison, admission, exact
  reachability, custody, recovery, migration, or cleanup cannot be given finite
  fail-closed bounds within R0;
- the single owner/process cannot enforce aggregate resources without a proved
  new service or failure-domain requirement;
- zero-payload reference behavior cannot be enforced structurally and measured
  separately from activation/admission;
- exact recovery or retirement necessarily requires unbounded object-graph
  tracing or persistent refcount authority; or
- a hard product performance/resource target, once actually selected and
  comparably measured, proves the complete-payload storage family cannot
  qualify.

Numeric tuning, metric names, batches, and evidence-based targets remain
`OPEN_WITHIN_R0` until such a proof exists.
