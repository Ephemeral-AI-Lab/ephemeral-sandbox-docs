# R0 performance and optimization

**Evidence label:** `INFERRED` for the cost model; `OPEN` for measurements

**Source metadata:** sealed product branch/commit/clean state is recorded in
the algorithm package; it is not an evidence label

**Correctness result:** `NOT_RUN`

**Historical comparator:** Stage 4.6 `INCOMPARABLE`

**Performance guarantee/SLA:** **none**

**Optimization target:** `OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED`

**Final performance verdict:** `TARGET_UNSELECTED`

## Decision stance

R0 was selected for correctness, implementability, bounded recovery, and
ownership fit—not because it won a benchmark. Product [hard rules](../PRD.md#hard-rules-must-never-break)
cannot be waived by a faster result. The selected [architecture](../architecture_design.md)
fixes measurable cost properties and optimization opportunities, while Phases
03 and 06 must produce executable evidence.

This document keeps four different statements separate:

| Statement class | Current status |
|---|---|
| Required correctness cost property | Selected where stated below |
| Optimization mechanism/hypothesis | Plausible but unproved until implemented and measured |
| Historical Stage 4.6 observation | Context only; `INCOMPARABLE` |
| R0 benchmark evidence | None; no `BENCHMARK-QUALIFIED` result |
| Correctness result | `NOT_RUN` |
| Final performance verdict | `TARGET_UNSELECTED` |

## Historical Stage 4.6 evidence

Phase 00 records the only permissible summary:

| Historical item | Recorded value/status |
|---|---|
| Role | Historical POC/campaign evidence |
| Matched classification | `R_stage46 = INCOMPARABLE` |
| Matched-first-three candidate median | approximately `58.1 ms` |
| Matched-first-three control median | approximately `36.4 ms` |
| Directional ratio | candidate/control approximately `1.6×`; candidate was slower |
| V2 baseline seal | No |
| Reason | Missing complete dirty/untracked source closure and matched rerun provenance |
| Allowed use | Fixture, timing-boundary, setup/cleanup, and bottleneck hypotheses after re-verification |
| Forbidden use | Selecting/rejecting R0, a V2 pass/fail gate, an SLA, or a “100×” claim |

The separate historical materialization observation and historical memory peaks
are also incomparable. Measurements made under different timing scopes,
fixtures, cgroups, builds, or durability boundaries cannot be combined into a
V2 cost claim. Derived per-operation figures from divided campaign totals are
not measurements.

Reference: [Phase 00 baseline policy](../phases/00-freeze-rules/SPEC.md#8-baseline-and-performance-policy).

## Selected operation cost model

The table states required cost drivers and observability. It does not promise a
time complexity unsupported by the Phase 02 codec or Phase 03 layout.

| Operation | Required payload behavior | Expected dominant work | Required measurement/proof |
|---|---|---|---|
| Admit a new unique complete Version | Read/process the complete Candidate; may write one complete immutable payload | Validation, canonicalization, hashing, staged construction, durability | Candidate/payload bytes, metadata operations, sync calls, CPU, memory, scratch, FDs, end-to-end latency |
| Admit candidate for occupied ID | Read/process candidate and perform full canonical-byte comparison | Canonicalization/hash plus exact comparison; equal may reuse, unequal collides | Compared bytes, equal/collision outcome, no reference mutation on collision |
| Publish candidate | Admission work plus one small OCC head replacement | Candidate work outside final gate; short authoritative reread/replace inside gate | End-to-end latency separated from gate wait/hold and durability time |
| Checkpoint to accepted Version | **Selected payload read = write = copy = 0** | Validate accepted binding and update small typed reference metadata | Complete operation-scoped payload counters at zero plus syscall/fixture evidence |
| Fork to accepted Version | **Selected payload read = write = copy = 0** | Same as checkpoint | Same zero-byte proof |
| Rollback-to-existing | **Selected accepted-reference payload read = write = copy = 0** | Exact expected-Head validation and one small Head replacement; fixed Roots never retarget | Same zero-byte proof plus OCC history |
| Same-Version Head move | **Selected payload read = write = copy = 0** | Small metadata transition or explicitly defined no-op | Same zero-byte proof and revision semantics |
| Resolve/capture read | Read one complete immutable closure after small reference lookup | Payload bytes requested/materialized; no layer-depth reconstruction | Bytes, lookup/read latency, custody use, and depth-independence fixture |
| Reuse one equal accepted Version for N Roots | No new payload per Root | One exact admission result plus N small references | One physical payload count and reference metadata bytes |
| Retire an unrooted Version | May inspect bounded reachability/custody metadata; unlink selected payload only after exact final validation | Bounded scan/index aid, gate revalidation, unlink | Population size, work per batch, gate hold, retained/retired result |
| Recover/readiness | No speculative selected-Version rewrite | Validate bounded records/populations and clean/quarantine recognized private debt | Population/debt size, work/time, cleanup, memory/FD peaks, readiness outcome |

“Accepted-reference payload I/O `0/0/0`” is a correctness invariant for
`CreateHeadIfAbsent`, `ReplaceHead`, `RemoveHead`,
`CreateFixedRootIfAbsent`, and `RemoveFixedRoot`,
not shorthand for “fast enough” or filesystem copy-on-write. Passing a raw
digest or candidate bytes is not the reference-only API and must undergo normal
admission, including occupied-ID full-byte comparison.

These operations still perform nonzero binding validation, coordination,
reference/control metadata I/O, durability fences, and cleanup-debt accounting.
Runtime activation or materialization is a later effect and may read, write, or
copy payload bytes; it is outside the reference counter scope.

## Expected tradeoffs

R0 deliberately accepts costs required by its safety model:

- first publication of a large unique Version must consume and durably admit
  the complete Candidate rather than only a logical delta;
- occupied-ID admission requires full canonical-byte comparison even if the
  digest matches;
- different `VersionId`s are not guaranteed to share unchanged files or blocks;
  R0 selects equality-level reuse, not a chunk/object DAG;
- payload-before-reference durability requires qualified synchronization work;
- fail-closed startup and exact retirement require bounded validation rather
  than heuristic cleanup; and
- resource precharge may reject work that could appear to fit if failure debt
  and concurrency were ignored.

These costs may not be removed by digest-only deduplication, writable committed
payloads, skipped durability, silent OCC merge/rebase, unbounded caching, or a
reference path that opens payload data.

## Optimization hypotheses

The following are the authorized optimization directions inside R0. Each must
preserve the fixed semantics and be measured before being described as a gain.

| Mechanism | Hypothesis | Required guardrail/evidence |
|---|---|---|
| Remove layer/parent/depth reconstruction | Accepted-Version read cost no longer grows with history depth | Source audit plus matched reads across constructed depth histories |
| Remove squash/automerge from V2 core | Avoid layer maintenance and unpredictable compaction work | Verify no fallback path; do not silently rebase stale writes |
| Separate accepted-binding reference API | Checkpoint/fork/rollback become metadata-scale operations | Payload read/write/copy counters exactly zero for the complete operation |
| Prepare candidate outside final OCC gate | Reduce serialized gate hold and improve concurrent publisher progress | Measure gate wait/hold separately; final reread and replacement remain indivisible |
| Reuse equal occupied payload | Avoid a second physical payload for exactly equal canonical Version bytes | Full-byte comparison plus physical-count test under concurrency |
| Stream canonicalization and payload construction | Bound memory relative to input size | Peak memory/FD/scratch evidence on large, wide, and adversarial fixtures |
| Batch bounded cleanup/retirement | Prevent cleanup from monopolizing startup or transition authority | Configured batch/debt ceiling, convergence, and no correctness gap |
| Keep store in-process in the existing package | Avoid RPC, helper-process, external database, and second recovery-domain overhead | Dependency/process audit; this is not a latency claim by itself |
| Avoid archive-required materialization and object-DAG traversal | Keep normal accepted reads as one complete closure | Source/layout audit and representative read/materialization measurement |
| Use bounded caching/index aids, if justified | Reduce repeated metadata work without making the aid authoritative | Explicit capacity, invalidation/reconstruction proof, cold/warm results |
| Refine safe fence sequence | Remove redundant synchronization only if crash safety is unchanged | Exact supported-filesystem crash-prefix suite; no benchmark-only approval |

FUSE, reflink, hard-link tricks, archive extraction, database indexes, object
graphs, persistent refcounts, services, and new frameworks are not selected R0
optimizations. A local internal optimization may be considered only if it does
not change truth, ownership, dependency direction, immutable closure semantics,
or the zero-payload-I/O definition. Architecture-changing additions require a
Phase 01 reopening and a concrete R0 failure case.

## Measurement boundaries

Every reported sample must name what is inside and outside the timed interval.
At minimum, report these separately when applicable:

| Boundary | Begins | Ends |
|---|---|---|
| End-to-end application operation | Authorized request accepted by the measured entrypoint | Caller receives terminal success/failure |
| Store candidate admission | Store accepts bounded candidate input | Accepted binding or terminal admission error returned |
| Final OCC transition | Waiting for/entering authoritative transition gate, reported as separate wait and hold measures | Durable head result or stale/error exits gate |
| Reference-only store operation | Accepted binding and target accepted by store API | Durable small-reference result returned |
| Read/materialization | Captured binding/custody request starts | Requested read/materialization completes and custody is released as defined |
| Recovery/readiness | Frozen artifact process starts recovery against a prepared store | Ready or typed fail-closed result |
| Cleanup/retirement batch | Bounded unit begins | Unit completes/deferred/fails with debt counters updated |

Setup, fixture creation, process launch, cache conditioning, migration, cleanup,
and durability fences must be included or excluded identically for candidate
and comparator. If a measure excludes an important product cost, report that
cost separately and do not call the partial interval end-to-end.

## Matched measurement protocol

A comparator is valid only when the qualification record seals the following:

1. exact repository path, commit, dirty/untracked closure, build inputs/flags,
   toolchain, binary hashes, feature flags, and configuration for each build;
2. one machine/VM profile, OS/kernel, filesystem and mount options, storage
   device/topology, cgroup/resource limits, and relevant background-load policy;
3. identical semantic operation, fixture bytes, seed/order, request path,
   validation, durability acknowledgement, setup, cleanup, and timing boundary;
4. explicit cold/warm/cache-conditioning protocol without cross-candidate
   contamination;
5. randomized or counterbalanced candidate/control order and enough repetitions
   to report the chosen distribution honestly;
6. raw per-sample evidence stored at a named path, including errors, timeouts,
   outliers, and environment metadata—no silent sample deletion;
7. payload and metadata bytes/I/O, CPU, memory, scratch/disk, inodes, FDs,
   workers/tasks, gate wait/hold, cleanup debt, and correctness results where
   relevant; and
8. a written comparability judgment before computing a candidate/control ratio.

Report sample count, p50, p95, p99 when supported by the sample size, maximum,
dispersion, errors, and confidence/uncertainty. Do not overstate percentiles
from too few samples. Throughput tests must also report concurrency and queue
depth. Resource peaks must come from the same scope as the operation they are
used to judge.

Phase 03 may collect targets and sanity/regression measurements while building
the harness. [Phase 06](../phases/06-prove-offline/test-perf.md) freezes one
candidate artifact before qualification, reruns all Must suites, and performs a
matched incumbent comparison if a comparator is available. If it is not
available, that comparison is `INCOMPARABLE` with a specific reason; without an
owner-approved target the overall final verdict remains `TARGET_UNSELECTED`.
Neither state is a Phase 01 architecture failure by itself.

## Workload matrix

At minimum, later measurement should separate:

| Dimension | Required classes |
|---|---|
| Operation | Unique admission, equal reuse, collision reject, candidate publish, stale publish, checkpoint, fork, rollback-to-existing, read, retire, recover |
| Version size/shape | Small, medium, large; deep paths; wide directories; many small files; fewer large files; accepted symlink/metadata classes |
| LayerStack-0 population | Empty/new, occupied equal ID, populated Roots/Heads, bounded orphan/debt populations |
| Concurrency | One request, equal admission race, conflicting publisher race, readers plus head movement, custody plus retirement |
| Cache | Declared cold and warm conditions |
| Outcome | Success, stale, collision, limit rejection, ENOSPC/I/O error, cancellation, crash/recovery |

Holdout fixtures reserved for Phase 06 qualification must not be used to tune
implementation earlier. Historical Stage 4.6 artifacts may inspire a fixture
only after the content and semantic oracle are re-established.

## Result record

Until executable evidence exists, the authoritative result is:

```text
R0_ARCHITECTURE = SELECTED
R0_IMPLEMENTATION = NOT_IMPLEMENTED_OR_NOT_QUALIFIED
EVIDENCE_LABEL = INFERRED
CORRECTNESS_RESULT = NOT_RUN
OPTIMIZATION_TARGET = OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED
FINAL_PERFORMANCE_VERDICT = TARGET_UNSELECTED
R0_VS_MATCHED_INCUMBENT = INCOMPARABLE
STAGE_4_6_COMPARATOR = INCOMPARABLE
V2_PERFORMANCE_GUARANTEE = NONE
V2_LATENCY_OR_THROUGHPUT_SLA = NONE
REFERENCE_ONLY_ZERO_PAYLOAD_IO = REQUIRED_NOT_YET_PROVED
```

Later result additions must include the frozen artifact ID, raw-evidence paths,
protocol version, comparability decision, Must-test status, and any variance
from the selected resource envelopes. Never overwrite the historical status to
make a new result appear comparable; append a new qualified campaign record.

## Optimization acceptance rules

An optimization may be accepted only when:

- every affected hard-rule and crash/concurrency/resource test remains green;
- it preserves complete immutable payload and exact occupied-ID comparison;
- reference-only payload counters remain exactly zero;
- it does not widen store authority or introduce a second writer/truth;
- its resources, cleanup, and failure modes are finite and instrumented;
- the measured boundary and artifact are sealed; and
- the reported gain is scoped to the measured operation/fixture/environment.

A statistically faster result cannot rescue a correctness failure. A slower
correct implementation may continue to later tuning only if all phase Must
gates pass and no separately authorized product performance gate has been
failed.

## Reopening conditions

Reopen Phase 01 if a performance/resource requirement proves implementable only
by changing selected-Version ownership, storage family, dependency direction,
writer count, identity boundary, complete immutable truth, or by adding a
required service/database/coordinator/object graph/layer truth. Do not make the
change under the label “optimization.”

Do not reopen Phase 01 for an ordinary implementation optimization inside R0,
a revised finite constant, a better bounded streaming implementation, a safe
fence refinement that passes the crash matrix, or a Stage 4.6 comparison that
remains incomparable.

## References

- [Product PRD and performance stance](../PRD.md#performance-stance-product-level)
- [Selected architecture](../architecture_design.md)
- [Phase 00 baseline policy](../phases/00-freeze-rules/SPEC.md#8-baseline-and-performance-policy)
- [Phase 03 store tests and performance](../phases/03-state-store/test-perf.md)
- [Phase 06 frozen-artifact qualification](../phases/06-prove-offline/PRD.md) and
  [test/performance contract](../phases/06-prove-offline/test-perf.md)
- [Concurrency, durability, and recovery](05-concurrency-durability-recovery.md)
- [Resources, security, and observability](06-resources-security-observability.md)
