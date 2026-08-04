# V2 optimization target register

```text
DOCUMENT_ROLE: FORWARD_QUALIFICATION_CONTRACT
DECISION: QUAL-001
DECISION_STATE: OPEN_WITHIN_R0
TARGET_CONTRACT_EVIDENCE: INFERRED
TARGET_VALUES: OPEN
SOURCE_METADATA: no frozen V2 benchmark candidate or result
CORRECTNESS_RESULT: NOT_RUN
OPTIMIZATION_TARGET: OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED
FINAL_PERFORMANCE_VERDICT: TARGET_UNSELECTED
STAGE_4_6_EVIDENCE: INCOMPARABLE
```

This document defines how an owner-approved Ephemeral Sandbox V2 optimization
target will be written before benchmark results exist. It intentionally selects
no numeric threshold, percentile, workload, backend, filesystem, adapter,
materialization mechanism, comparison factor, or production guarantee.

## 1. What is the optimization target?

The optimization target is not one vague instruction to "make storage fast."
It is the complete, predeclared acceptance tuple for a particular product
operation:

```text
target = operation and exact timed boundary
       + semantic/correctness contract
       + workload and fixture shape
       + concurrency and repetition protocol
       + backend, filesystem, durability, and cache state
       + statistic or percentile
       + numeric ceiling, floor, or matched factor
       + resource/debt ceilings
       + approved owner and frozen version
```

Until that tuple is complete and approved before candidate results are
observed, measurements are descriptive only and the final V2 performance
verdict remains `TARGET_UNSELECTED`.

## 2. What should V2 optimize?

V2 should measure and optimize both publication and runtime
readiness/materialization, but as separate target families. Improving one must
not hide a regression in the other.

| Target ID | Product question | Exact boundary to freeze before a run | Current quantitative target |
|---|---|---|---|
| `T-PUB-E2E` | How long until a caller knows a new Candidate was durably accepted and its Head transition reached a terminal outcome? | Authorized full-publication request -> capture/validate/canonicalize/derive `VersionId` -> occupied-ID exact comparison or new complete-Version admission -> `AcceptedVersion`/`AcceptedBinding` -> exact Head OCC -> qualified fence -> terminal caller outcome | `OPEN` |
| `T-ADM` | What does durable complete-Version admission cost independent of Head contention? | Validated canonical Candidate enters admission -> exact occupied-ID handling or new immutable slot reaches the selected durable-success boundary -> `AcceptedVersion`/`AcceptedBinding` issued | `OPEN` |
| `T-REF` | How expensive is an already-admitted Head/fixed-Root transition? | Typed request with `AcceptedBinding` and complete expected state -> sole reference authority comparison/transition -> qualified fence -> terminal outcome | `OPEN` |
| `T-ACT` | How quickly can a backend consume accepted truth when direct protected activation is supported? | Authorized runtime request plus captured `AcceptedBinding` -> custody installed -> backend-qualified protected activation -> runtime-visible ready result | `OPEN` |
| `T-MAT` | How long and how many resources are required to build a complete private runtime representation when it is required? | Captured `AcceptedBinding` plus custody -> backend-private complete materialization -> validated runtime-private readiness | `OPEN` |
| `T-READY` | What is the user-visible time to a runnable sandbox? | Authorized runtime request -> authoritative accepted-binding capture/custody -> selected activation or materialization path -> runtime-ready acknowledgement | `OPEN` |
| `T-REC` | How long until prior truth or complete new truth is available after a declared failure? | Qualified restart/recovery trigger -> bounded inventory/validation/repair -> prior truth or complete new truth available, or fail closed | `OPEN` |
| `T-RET` | Can retirement and cleanup remain bounded without deleting reachable truth? | Retirement eligibility signal -> exact Head/Root/custody revalidation -> safe detach/reclaim or explicit bounded debt record | `OPEN` |
| `T-MIG` | Can the one-writer migration complete within bounded time and resources while preserving cutover/rollback rules? | Declared migration unit/campaign boundary -> verified V2 admission/reference work -> selected cutover or rollback terminal state | `OPEN` |
| `T-RES` | Are memory, disk, FDs, workers, mounts, staging, orphan, custody, and cleanup debt bounded across all qualifying operations? | Per-target and campaign high-water/debt accounting under the same sealed run | `OPEN` |

`T-PUB-E2E` and `T-READY` are the headline product-facing rows. The other rows
are diagnostic boundaries that make the result actionable. A future owner may
approve only the rows required by the product release contract, but omitted
rows must be labelled non-gating rather than silently treated as passed.

## 3. Invariants no target may trade away

Every target is subordinate to these correctness rules:

- one accepted complete immutable portable Version is truth;
- `VersionId` is typed content-derived identity, not durable-existence or
  equality proof;
- occupied-ID handling performs exact canonical equality before reuse;
- only LayerStack-0 issues `AcceptedVersion` and `AcceptedBinding`;
- the only accepted publication order is Candidate construction and durable
  admission before exact Head OCC and fence-before-success acknowledgement;
- there is one reference authority and one Head OCC point;
- Branch is a Head; Checkpoint is a fixed typed Root;
- accepted-reference operations preserve payload
  `read/write/copy = 0/0/0`, while metadata, coordination, fence, and telemetry
  work remain explicitly nonzero;
- runtime adapters consume accepted truth below the runtime-effect boundary and
  do not redefine portable identity or reference authority;
- migration remains one-writer; and
- retirement never reclaims a Version still reachable by Head, fixed Root, or
  custody.

A faster result that violates any invariant is a correctness failure, not an
optimization.

## 4. Operation boundary details

### 4.1 Full publication

`T-PUB-E2E` includes the complete user-visible publication path. The report must
also expose, rather than subtract, at least:

- Candidate capture and validation;
- canonical ordering/encoding and `VersionId` derivation;
- occupied-ID exact comparison or new-slot admission;
- durable complete-Version admission and `AcceptedBinding` creation;
- Head transition-gate wait and hold time;
- complete expected-record comparison and OCC result;
- durability-fence time;
- outcome-unknown authoritative read-back, if exercised;
- accepted-orphan/staging/cleanup-debt effects; and
- end-to-end caller latency.

Stale OCC preserves accepted immutable truth and accounts for any accepted
orphan. It is not benchmark cleanup success and its cost may not be erased from
the campaign.

### 4.2 Accepted-only reference transition

`T-REF` covers each of the five selected operations separately:

```text
CreateHeadIfAbsent
ReplaceHead
RemoveHead
CreateFixedRootIfAbsent
RemoveFixedRoot
```

For each operation and outcome, payload movement must be recorded as
`read/write/copy = 0/0/0`. The report separately records reference/control
metadata bytes, filesystem operations, coordination wait/hold, fence latency,
read-back, telemetry, custody/reachability changes, and scheduled retirement or
cleanup debt. The structural `0/0/0` rule is not a speed threshold.

### 4.3 Protected activation and full materialization

`T-ACT` and `T-MAT` are not interchangeable:

- protected activation measures direct consumption of captured accepted truth
  when a qualified backend can provide a runtime-private view without eager
  complete-payload copying; and
- full materialization measures the complete payload reads, private writes,
  metadata work, validation, memory, scratch space, and readiness latency when
  a backend-private representation is required.

No target may assume every backend supports direct activation or every backend
requires full materialization. OCI/Docker is current implementation evidence,
not universal proof. Firecracker and WASI/WASM remain backend status
`OPEN_EVIDENCE`, with implementation evidence `OPEN`. This target register does
not select a VM disk format, WASM runtime, adapter API, caching model, or
materialization strategy.

### 4.4 End-to-end runtime readiness

`T-READY` includes accepted-binding capture, custody, the selected backend path,
and runtime-ready acknowledgement. The report must break out `T-ACT` or `T-MAT`
so a cache hit, direct handoff, or setup shortcut cannot disguise full cold-path
cost. Cold, warm, and same-Version reuse are separate cases, not pooled samples.

## 5. Required target tuple

Copy one row per target ID. Every field is mandatory unless the row explicitly
states why it is non-applicable.

| Field | Required declaration | Current value |
|---|---|---|
| Target ID and version | Stable identifier plus revision | `OPEN` |
| Owner and approval timestamp | Product owner authorized to set the release target | `OPEN` |
| Gating status | Hard gate, diagnostic, or non-gating observation | `OPEN` |
| Operation | One target family and exact API/caller operation | `OPEN` |
| Start boundary | Observable event and included setup | `OPEN` |
| Stop boundary | Observable event, durability/readiness state, and acknowledgement rule | `OPEN` |
| Correctness prerequisites | Exact oracles, outcomes, crash/retry behavior, and invalidation rules | `OPEN` |
| Candidate identity | Repository, branch, commit, full dirty/untracked state, binary/build/config seal | `OPEN` |
| Comparator identity | Matched implementation identity or explicit no-comparator design | `OPEN` |
| Workload/fixture | Exact bytes/hash, logical bytes, file/dir count, depth/delta/sparsity, case mix | `OPEN` |
| Concurrency | Writers/readers, arrival shape, synchronization, and contention case | `OPEN` |
| Backend and adapter | Backend status, adapter identity, and capability profile | `OPEN` |
| Filesystem/storage | OS/kernel, filesystem/mount, device/storage profile, namespace/layout version | `OPEN` |
| Durability boundary | Required fences and what is stable at stop | `OPEN` |
| Cache state | Cold/warm/reuse definition and preparation proof | `OPEN` |
| Repetitions/order | Warmups, measured count, randomization, seed, outlier policy | `OPEN` |
| Statistic | Median, percentile, maximum, throughput, rate, or matched factor | `OPEN` |
| Numeric target | Exact ceiling, floor, or factor with units and direction | `OPEN` |
| Resource ceilings | RSS/cgroup, CPU, disk/scratch, I/O, FDs, workers, mounts, debt | `OPEN` |
| Telemetry requirements | Required operation/outcome attribution and dropped-event policy | `OPEN` |
| Evidence paths | Commands, raw samples, logs, manifests, and independent verification output | `OPEN` |
| Freeze proof | Target file hash/commit showing approval occurred before candidate results | `OPEN` |

Editing a target after inspecting results creates a new target version and
invalidates those observed results for qualification against that version.

## 6. Required metrics

Each measured case records both result and cost:

| Category | Required fields |
|---|---|
| Outcome | semantic result, correctness result, retry count, cancellation/crash classification, authoritative read-back result |
| Time | end-to-end latency; stage latencies; gate/fence wait and hold; throughput with exact numerator and denominator |
| CPU/scheduling | CPU time, wait time, worker saturation, declared host contention |
| Memory | process RSS/high-water, cgroup peak/limits, bounded buffers, allocator or cache scope if reported |
| Payload I/O | logical and physical bytes read/written/copied, separated by Candidate, admitted Version, runtime-private representation, and comparator |
| Metadata/durability | reference/control bytes, comparison bytes, filesystem operations, sync/fence counts and latency |
| Storage/debt | staging bytes, immutable bytes, scratch/amplification, accepted orphans, cleanup/recovery debt, reclaimed bytes |
| Resources | FDs, workers, mounts, custody population, concurrent readers/writers |
| Evidence health | missing samples, dropped telemetry, manifest verification, environment drift, comparability classification |

Ratios always name numerator and denominator. Phase-wall time and
single-operation latency are separate metrics. A maximum from a small sample is
not relabelled p95.

## 7. Minimum workload families

The owner chooses exact cases and values later; the protocol must cover the
selected release risks:

| Dimension | Cases to predeclare |
|---|---|
| Payload size | empty/small, representative, large, and selected maximum |
| Entry shape | few-large, many-small, deep paths, maximum path bytes/depth |
| Change shape | no-op/same Version, small delta, large delta, full replacement |
| Reference state | absent, exact expected, stale, already present, removed, corrupt/unknown read-back cases |
| Concurrency | uncontended, competing Head writers, readers plus publication, retirement/custody race |
| Cache/runtime | cold, warm, same-Version reuse; direct activation and complete materialization where backend-qualified |
| Failure | retry, cancellation, crash prefixes, lost acknowledgement, recovery, cleanup debt |
| Migration | representative and maximum units, cutover and rollback cases, one-writer proof |

Case names do not select a fixture, maximum, or numerical target. Those remain
`OPEN` until owner approval.

## 8. Comparator and evidence rules

- Prefer a matched comparator when one can implement the same semantics and
  timing/durability boundary.
- If a comparator differs materially in correctness, admitted truth,
  durability, cache preparation, backend effect, resource profile, or cleanup,
  classify the comparison `INCOMPARABLE` with the exact reason.
- Stage 04.6 is not a V2 comparator. Its values may not enter matched samples,
  target thresholds, factors, confidence calculations, or pass/fail decisions.
- Complexity models and design plans are `INFERRED` evidence. They do not prove
  a benchmark win.
- A candidate must retain complete source, dirty/untracked state, build,
  executable, dependency/toolchain, configuration, fixture, environment,
  command, order/seed, raw-result, and manifest closure.
- Correctness is evaluated before performance. Any failed correctness gate
  invalidates associated speed numbers for qualification.

## 9. Verdict algorithm

| Condition | Final performance verdict |
|---|---|
| No owner-approved complete target tuple exists | `TARGET_UNSELECTED` |
| Architecture/cost model only, with no qualifying measurement | `DESIGN_ONLY` when that is the report's declared scope |
| Candidate and comparator or campaign boundaries differ materially | `INCOMPARABLE` |
| Correctness passes; evidence is complete and comparable; every required predeclared target passes | `QUALIFIED` |
| Correctness passes; evidence and comparison closure are complete; an owner-approved predeclared target is missed | `FAILED_TARGET` |

`BENCHMARK-QUALIFIED` is an evidence label, not an automatic final verdict.
Missing evidence is not converted into a pass or `FAILED_TARGET`.

## 10. Architecture reopening boundary

A disappointing number does not reopen Phase 01. First attempt bounded
implementation, filesystem, batching, caching, scheduling, fencing, and adapter
optimizations inside R0 without weakening correctness. Performance can support
reopening only after sealed comparable `FAILED_TARGET` evidence proves that the
required semantics cannot be supported by the accepted complete-Version owner
and direct runtime handoff without changing an architecture hard rule, and the
exact Phase 01.5 reopening condition is satisfied.

## 11. Approval record

No approval has been given. When an owner selects the first target set, replace
the fields below in a reviewable revision before running or exposing candidate
results:

```text
TARGET_SET_ID: OPEN
TARGET_SET_VERSION: OPEN
OWNER: OPEN
APPROVED_AT: OPEN
GATING_TARGET_IDS: OPEN
NON_GATING_TARGET_IDS: OPEN
TARGET_FILE_DIGEST_OR_COMMIT: OPEN
RESULTS_OBSERVED_BEFORE_APPROVAL: MUST_BE_FALSE
```

Until that record is complete:

```text
OPTIMIZATION_TARGET: OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED
CORRECTNESS_RESULT: NOT_RUN
FINAL_PERFORMANCE_VERDICT: TARGET_UNSELECTED
```
