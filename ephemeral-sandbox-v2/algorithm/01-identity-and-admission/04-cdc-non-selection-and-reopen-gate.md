# 01.04 — CDC non-selection and Phase 01 reopening gate

```text
CDC_ALGORITHM: NOT_SELECTED_IN_R0
```

## 1. Purpose and owning phase

**Owner:** Phase 01 owns the architecture decision and any reopening. Phase 06
may produce comparable evidence but cannot change the decision.  
**Purpose:** Make the absence of content-defined chunking explicit, prevent CDC
from entering Phase 02/03 as an “implementation detail,” and define the exact
evidence gate for reopening rather than silently designing a different system.

R0 addresses and admits one complete canonical Version and stores one complete
filesystem-native immutable payload closure. Cross-Version CDC would add a new
durable representation and lifecycle. This file documents that boundary; it is
not a CDC implementation plan.

## 2. Evidence status

- `SOURCE-VERIFIED`: Stage 4.6 remains `INCOMPARABLE`; historical measurements
  do not establish a matched benchmark winner. The selected output is R0.
- `SPIKE-VERIFIED`: none; no matched R0-versus-CDC V2 spike exists.
- `INFERRED`: CDC would change admission, readable truth, recovery,
  reachability, retirement, security, and resource accounting rather than only
  a local copy loop.
- `OPEN`: future qualification may select workloads and hard targets. CDC is
  not `OPEN_WITHIN_R0`; it becomes discussable as a replacement only after an
  exact R0 hard-rule failure triggers `REOPEN_PHASE_01`.

## 3. What CDC would change

Content-defined chunking would partition content using rolling boundaries and
address chunks for reuse across Versions. Making those chunks durable truth
would require at least some combination of:

- a chunk address grammar and collision policy;
- cross-Version Chunk storage and admission;
- a manifest or object graph describing complete Versions;
- reconstruction/read ordering and missing-object behavior;
- graph/reference reachability or persistent refcount authority;
- multi-object crash ordering, partial installation, and recovery;
- amplification and adversarial-boundary controls;
- migration from complete payloads to object graphs; and
- cleanup coordination for shared objects.

Those are precisely the durable primitives R0 did not select. An optional,
disposable transfer optimization that does not become identity, readable truth,
acceptance, reference authority, or required correctness is a separate later
optimization question; it cannot change this package's algorithms or claims.

## 4. Decision-gate contract

### Inputs

- A named product hard rule or selected hard performance/resource target.
- A sealed R0 implementation/source closure and qualified filesystem profile.
- Reproducible, matched workload and environment evidence.
- A specific observed R0 failure, including resource and crash behavior.
- A proposed architecture-changing repair with complete ownership, dependency,
  durability, recovery, migration, security, and operating-cost analysis.

### Preconditions

1. Exact Phase 02/03 R0 choices are implemented or isolated enough that the
   measured failure is architectural rather than an unselected constant,
   codec, fence, traversal, batching, or instrumentation detail.
2. The target is genuinely hard and accepted by the proper owner; a preference
   for deduplication or a synthetic average is insufficient.
3. Workloads, cache state, hardware/filesystem, concurrency, durability level,
   source commits, configuration, and measurement tools are sealed and matched.
4. R0 has been tested with bounded streaming, backpressure, cleanup, and direct
   ownership intact.
5. The proposal states why existing LayerStack-0 and direct runtime calls cannot
   repair the failure without changing storage family or authority.

### Outputs

One typed design-governance classification with the exact evidence provenance,
failure or gap, responsible phase, and—only when warranted—the specific
architecture-changing R0 failure that requires Phase 01 reopening. The gate
creates no Candidate, VersionId, AcceptedVersion, AcceptedBinding, Head,
HeadRevision, Root, product state, or storage state.

### Typed outcomes

| Outcome | Meaning |
|---|---|
| `RemainAlignedWithR0` | No architecture-changing hard-rule failure was proved; CDC remains non-selected. |
| `OpenWithinR0(details)` | Evidence identifies a Phase 02/03/06 choice or tuning/qualification gap that preserves R0. |
| `EvidenceInvalid(reason)` | Source, workloads, environment, metrics, or target are unmatched, incomplete, or non-authoritative. |
| `REOPEN_PHASE_01(exact_failure)` | A specific hard-rule failure cannot be repaired inside the current owner/storage family; architecture comparison may resume. |

This gate writes no product or storage state. Its output is design-governance
status, not an AcceptedBinding, Head, Root, or migration control record.

## 5. Reopening decision algorithm

```text
classify_r0_failure(evidence, target, proposed_repair):
    validate target is selected and architecture-relevant
    validate sealed source, environment, workload, and measurement provenance
    if validation fails:
        return EvidenceInvalid(exact_reason)

    reproduce the failure against the selected R0 mechanics and finite budgets
    if failure is not reproducible or target is met:
        return RemainAlignedWithR0

    enumerate repairs that preserve:
        one complete immutable Version truth
        existing LayerStack-0 ownership and direct calls
        one writer and one Head OCC point
        bounded fail-closed resources/recovery/cleanup

    if any evidenced repair stays within those constraints:
        return OpenWithinR0(repair_and_owning_phase)

    require proposed replacement to state:
        exact R0 failure repaired
        why current owner/direct call cannot repair it
        new durable primitives and authorities
        dependency, crash, recovery, resource, security, migration,
            cleanup, and operating costs
        matched evidence that it meets the hard target

    if any required field or evidence is absent:
        return EvidenceInvalid(exact_gap)

    return REOPEN_PHASE_01(exact_architecture_changing_failure)
```

There is no automatic “choose CDC” branch. Reopening restores architecture
evaluation; it does not preselect the proposed replacement.

## 6. Comparative hypothesis model—not a selected algorithm

For evidence planning only, let `V` be input bytes, `K` discovered chunks,
`W_roll` rolling-boundary state, `I` index operations, `G` reachable graph
objects, and `M_manifest` manifest bytes.

| Hypothetical CDC concern | Lower-bound or honest worst-case term |
|---|---:|
| Boundary scan | `O(V)` time and `O(W_roll)` streaming state |
| Chunk hashing | `O(V)` byte processing |
| Chunk lookup/admission | `O(K * I)` plus collision verification |
| Manifest construction | `O(K)` entries and `O(M_manifest)` bytes |
| Complete read/reconstruction | `O(K + V_read)` plus missing/corrupt-object checks |
| Crash recovery | proportional to incomplete chunks, manifests, indexes, and visibility edges |
| Retirement | `O(G)` tracing or equivalent authoritative refcount/update work |
| Adversarial inputs | potentially very small/large chunk distributions within selected caps |

Potential reuse is workload-dependent and is not a complexity guarantee. These
terms are `INFERRED`, comparative, and non-selected. No implementation may cite
this table as permission to create Chunks, manifests, or an object index.

## 7. Execution-condition behavior

| Condition | Gate behavior |
|---|---|
| Normal review | Validate evidence and return remain-R0, open-within-R0, invalid, or explicit reopening. |
| Concurrent proposals | Evaluate against one sealed decision record and target set; no proposal mutates product state or gains priority through timing. |
| Retry | Same sealed inputs must produce the same classification; changed evidence is a new review with new provenance. |
| Cancellation | Preserve prior Phase 01 decision; partial analysis has no authority. |
| Crash/tool loss | Preserve prior decision; resume from sealed artifacts, never infer reopening from missing telemetry. |
| Cleanup | Retain bounded decision evidence according to documentation policy; delete disposable benchmark work without touching product/live data. |

The decision's visibility point is acceptance of an explicit Phase 01 reopening
record by the architecture authority. A benchmark completion, metric emission,
or this document is not that point.

## 8. Finite resources and complexity

Evidence collection must bound dataset bytes, cases, repetitions, concurrency,
wall time, trace volume, memory, FDs, workers, temporary disk, and retained
artifacts. Exhaustion returns `EvidenceInvalid` or an incomplete result; it does
not weaken a target or silently reopen Phase 01.

For `N` sealed cases and `R` repetitions, decision aggregation is `O(N*R)` over
bounded summary records, excluding the cost of the systems measured. Temporary
evidence space is `O(S_evidence)` under a selected cap; peak analysis memory is
`O(M_analysis)` under a selected cap. The hypothetical CDC terms above are not
R0 runtime costs.

## 9. Security and validation obligations

- Treat datasets, paths, configurations, trace output, benchmark scripts, and
  claimed targets as untrusted evidence inputs.
- Seal source commits and hash/configure artifacts without turning raw digests
  into Version references.
- Redact secrets and payload content; bound label cardinality and trace volume.
- Prevent benchmark paths from touching product worktrees, live state, or
  migration data.
- Reject cherry-picked cache states, unmatched durability, silent errors,
  incomplete outputs, and arithmetic overflow in rate/percentile calculations.
- Require owner acceptance for a hard target; observability and benchmark tools
  cannot create product policy.

## 10. Observability and test seams

The gate records source closure, configuration, workload identity, environment,
filesystem, cache protocol, durability mode, repetitions, exclusions, raw and
summary artifact locations, failure classification, within-R0 repairs tried,
and reviewer/owner decision status.

Tests must prove that:

- a preference, unmatched benchmark, or missing owner target cannot reopen;
- a codec/constant/batching issue returns `OpenWithinR0`;
- an exact architecture-changing failure names the violated hard rule;
- every replacement cost category is required before reopening;
- cancellation/crash leaves R0 selected; and
- Stage 4.6 remains `INCOMPARABLE` until a qualified matched run exists.

Observability is a diagnostic reader and cannot cast the architecture decision.

## 11. Details owning phases may still select

Phase 06 may select datasets, target statistics, run counts, environment seal,
measurement tools, noise/outlier policy, and evidence-retention limits. Product
owners may select hard performance/resource targets. None of those choices may
install CDC inside R0 or call a non-comparable result a winner.

## 12. `REOPEN_PHASE_01` conditions

The only valid result is:

```text
REOPEN_PHASE_01 — <specific architecture-changing failure>
```

Examples of qualifying failure classes, only when evidenced, are:

- one complete immutable payload cannot satisfy a selected hard storage,
  admission, recovery, or activation bound;
- bounded full-byte equality cannot satisfy a selected hard latency/resource
  bound and no within-R0 repair exists;
- a required workload cannot be represented/read without cross-Version objects;
  or
- whole-Version recovery/retirement cannot remain finite without a different
  durable reachability model.

The report must explain why the current LayerStack-0 owner and direct calls
cannot repair the failure and must enumerate all new costs. Until then,
`ALGORITHM_PACKAGE: ALIGNED_WITH_R0` and `CDC_ALGORITHM: NOT_SELECTED_IN_R0`
remain the coherent result.
