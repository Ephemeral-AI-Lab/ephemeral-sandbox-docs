# EphemeralOS Benchmark Laboratory — Coordinated System Specification

| Field | Value |
|---|---|
| Status | Revised implementation contract |
| Date | 2026-07-12 |
| Product root | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/benchmark` |
| Default test workspace root | Sibling directory `ephemeral-sandbox-test-workspace` |
| UI design | [benchmark-ui-design.md](benchmark-ui-design.md) |
| Backend design | [benchmark-backend-design.md](benchmark-backend-design.md) |
| Architecture review | [system-spec-architecture-review-prompt.md](system-spec-architecture-review-prompt.md) |

## 1. Purpose

The Benchmark Laboratory is a local, reproducible performance-testing system
for EphemeralOS command, file, workspace-session, and LayerStack operations. It
must answer three questions without conflating them:

1. How long does an operation take, both per request and per concurrent batch?
2. What memory, disk, CPU, and block-I/O cost does it impose while it runs and
   after it settles?
3. Did it preserve the operation's correctness contract?

The product consists of a scientific web interface, a trusted loopback runner,
immutable run artifacts, and a report/compare surface. The UI and backend must
use the names, units, count semantics, states, schemas, and statistical rules in
this document. Neither side may invent a second interpretation.

This is a benchmark suite, not the live E2E correctness suite. Existing E2E
tests remain the source of exhaustive failure-path proof. The laboratory uses
representative valid scenarios, checks their invariants, and measures them.

### 1.1 Architecture and dependency direction

V1 uses a **hybrid closed core with registered capabilities** inside a modular
monolith: one trusted local runner, one active campaign, and
first-party operation implementations compiled into the runner. Its intentional
ceiling is compile-time extension. V1 has no runtime plugin loading, arbitrary
code loading, dependency-injection container, service locator, workflow DSL,
generic graph engine, event bus, database, repository abstraction, distributed
worker protocol, or browser-side executor.

The closed core owns lifecycle phases, safety policy, artifact durability,
scientific identity, and comparison. Small compile-time definition tables may
remove repeated metadata for operations, resource metrics, correctness checks,
and phases, but they must use typed identifiers and exhaustive registration.
They must not replace behavior with runtime strings or bypass security review.

Dependencies flow in one direction:

```text
HTTP/UI contract
      ↓
ExperimentPlan + compile-time definitions
      ↓
validator / cell expander → ExpandedPlan
      ↓
common scheduler → operation lifecycle → product clients / host adapters

resource collectors ─┐
correctness checks ──┼→ immutable observations
phase correlation ───┘          ↓
                         statistics / reports / comparison
```

Operation modules never depend on HTTP, UI, report, or artifact-layout types.
Statistics and reports depend on immutable observations, not executors, product
clients, Docker, or the browser. Presets depend only on the public plan schema.

### 1.2 Canonical ownership

| Concern | Canonical owner |
|---|---|
| User intent | Versioned `ExperimentPlan`. |
| Supported capabilities and scientific metadata | Exhaustive compile-time operation, metric, check, and phase definitions; `/definitions.catalog` is their projection. Versioned Default plans and presets are separately owned data in the same response. |
| Exact work, order, effective protocol, and estimates | Validated, immutable `ExpandedPlan`. Execution never reinterprets the intent plan. |
| Trial order, barriers, concurrency, timing, cancellation, and cleanup invocation | Common scheduler. |
| Operation topology, product request construction, and operation-specific verification inputs | Typed operation lifecycle module. |
| Common resource acquisition | Resource collectors selected by the runner, never by an executor. |
| Correctness results | Typed checks selected by an operation; the common runner folds their verdicts and applies cleanup eligibility. |
| Raw evidence | Artifact writer and versioned immutable observation records. |
| Statistics, reports, and compatibility | Pure statistics, report, and comparison modules over persisted artifacts. |
| UI definitions and results | HTTP projections of definition snapshots and backend-derived report models. The UI does not compute competing statistics. |

## 2. Fixed product decisions

1. The benchmark catalog contains seven measured operations in four families.
2. There is one page per family, not one page per operation.
3. There are five primary pages and three shared workflow page types: eight
   route shapes total.
4. A family can run independently. **Run All Locally** runs all enabled
   families in sequence by default so their resource measurements do not
   contaminate one another.
5. Concurrency values default to `1`, `5`, and `20`; their meaning is defined
   per family in section 5.
6. LayerStack executes one `squash_layerstacks` request per trial. It must not
   issue concurrent squash requests because squash is singleflight per root.
7. Remount is measured as the post-commit phase of squash, not presented as a
   separate public operation.
8. The only editable host path in the ordinary UI is **Test workspace root**.
   The runner derives its fixture, work, and result directories below it.
9. The default root is the `ephemeral-sandbox-test-workspace` sibling of the
   discovered `ephemeral-sandbox` checkout. No user-specific absolute path is
   committed.
10. Raw observations are immutable. Failed correctness checks remain visible
    and are never silently included in successful latency distributions.
11. Time uses monotonic clocks for measurement, bytes for stored raw values,
    and explicit units in every display. Wall-clock timestamps are metadata.
12. The MVP has one active campaign per runner. Cross-family parallel stress
    mode, distributed runners, a database, and remote execution are deferred.
13. Every family page opens with a complete, versioned **Default configuration**
    that is valid to review without editing. Customization is optional,
    reversible, and never changes the stored default.
14. The runner uses the fixed isolated gateway mode. Gateway isolation, product
    access allowlists, cleanup policy, and safety caps are not plan options.

## 3. Benchmark catalog

| Family | UI operation | Product route measured | Scope and semantic boundary |
|---|---|---|---|
| Command | `exec_command` | public runtime `exec_command` | Explicit-session mode measures command admission/execution. Automatic-session mode deliberately includes create, publish, and destroy lifecycle. |
| File Operations | `file_read` | public runtime `file_read` | UTF-8 line window from the published snapshot or a live workspace session. |
| File Operations | `file_write` | public runtime `file_write` | Overwrite in a live session, or publish one attributed layer when sessionless. |
| File Operations | `file_edit` | public runtime `file_edit` | Ordered exact-string replacements in a session, or one attributed published layer when sessionless. |
| File Operations | `file_blame` | public runtime `file_blame` | EphemeralOS per-line ownership from publish auditability. This is not Git blame. |
| Workspace Lifecycle | `create_workspace` | internal runtime `create_workspace_session` | Benchmark label for creation of an explicit `no_op` workspace session. It is a test adapter, not a new public catalog operation. |
| LayerStack | `squash_layerstack` | public manager `squash_layerstacks` forwarding one internal `squash_layerstack` | Storage plan/build/commit followed by the bounded live-session remount sweep. |

Out of scope for v1 are sandbox creation/destruction latency, command transcript
polling, stdin, file listing, export, observability query latency, and Git
operations. Sandbox creation is setup for a trial, not its measured operation.

### 3.1 Operation extension contract

`FamilyId` and `OperationId` are closed Rust enums. Each operation has one
exhaustively registered compile-time definition containing all of the following:

- family and operation identity;
- operation semantic revision and typed factor-schema revision;
- count semantics and execution shape;
- trial isolation and cleanup policy;
- one closed product-access choice: a public gateway operation, a daemon HTTP
  action, or the exact allowlisted internal workspace-session adapter;
- supported client cohorts and security classification;
- typed factor metadata and constraints;
- stable correctness-check and optional phase identifiers; and
- comparison-key projection.

An operation cannot be registered without its access allowlist, isolation,
semantic revisions, and comparison identity. `/definitions.catalog` is derived
from these definitions; it is not a runtime handler registry. The response's
`defaults` and `presets` fields are strict versioned plan data validated against
that catalog, not compile-time behavior metadata. The UI owns explicit family
layout and operation-specific controls, but labels, units, factor bounds,
capabilities, and scientific revisions come from the catalog projection.

The operation module—not the metadata definition—owns its tagged plan and
expanded-cell variants plus ordinary typed validation and expansion functions.
Exhaustive matches route those functions. The definition does not store erased
validation callbacks, executor factories, or runtime handler names.

Operation-specific plan, expanded-cell, and evidence data use tagged typed
variants. A normalized factor projection may be derived for generic tables and
exports, but a `Map<String, Value>` is never the authority for validation,
execution, security dispatch, or comparison. Conversely, the system does not
use one giant struct containing nullable factors from unrelated operations.

The common runner calls a phase-aligned, statically dispatched lifecycle with
typed preparation state, invocations, outputs, verification, and teardown.
Adding an operation recompiles the runner and normally changes one operation
module, one typed definition/registration, operation-specific UI controls when
needed, and tests. Shared scheduling, measurement, artifacts, statistics, and
generic reports must remain unchanged. A new family may additionally require
explicit topology and family UI because those changes expose product meaning.
For example, a later Sandbox Lifecycle family may add create and destroy
modules and one explicit family page while retaining the common pipeline. A
concurrent create trial issues C independent product requests with `count=1`;
it must not call one product request with `count=C` and mislabel the product's
internal sequential loop as request concurrency.

Resource metrics, correctness checks, and report views are independent of
operation dispatch:

- a metric definition owns stable id, semantic revision, unit, scope,
  availability, counter/gauge kind, and aggregation rule;
- a check definition owns stable id, revision, bounded-evidence policy, and
  typed verifier function; the common verdict folds its `CheckResult`;
- a semantic phase definition owns stable id, revision, unit, source, and
  correlation rule; unmatched server spans remain diagnostic data; and
- a report view is a pure derivation over observations and never adds executor
  behavior.

The current `exec_command` product contract accepts a shell command in its
`cmd` string and executes it through the product shell path. V1 command cases
are compile-time allowlisted templates that generate an exact, bounded `cmd`;
the plan and browser cannot supply arbitrary shell text or pretend the product
supports an argv/no-shell contract.

A future `file_list` benchmark must use the product's daemon HTTP-only list
path. Directory breadth and depth describe its fixture and target topology. The
product's typed list request accepts `limit: Option<usize>`: zero is rejected
and a positive request is clamped by the fixed `FileRuntimeConfig.max_list_entries`
safety cap. `result_limit` is a valid experimental factor only through that
bounded contract. The expanded plan and manifest record the requested limit,
effective limit, fixed cap, and cap revision; raw evidence records returned
count and truncation.
The safety cap itself is never an ordinary plan option.

## 4. Scientific vocabulary

| Term | Exact meaning |
|---|---|
| Campaign | One user-submitted run containing one or more families. |
| Family run | The portion of a campaign for Command, Files, Workspace, or LayerStack. |
| Factor | A controlled or varied input such as concurrency, payload bytes, or workspace profile. |
| Cell | One unique combination of factor values. |
| Trial | One independent execution of a cell. Warmups are trials flagged `warmup=true` and excluded from summaries. |
| Batch | The requests released together in a trial. |
| Request | One product operation invocation inside a batch. |
| Control | The explicitly starred factor value used as the comparison reference. |
| Fixture | Deterministically generated input state with a manifest and content hash. |
| Sample | One raw timing, resource, correctness, or phase observation. |
| Default configuration | The immutable, versioned complete starting plan for a scope. It is a UX starting point, not a statistical control or resource baseline. |
| Customized configuration | A current canonical portable plan that differs from the versioned Default configuration. Machine-local runner bindings are not part of this equality. |
| Resource baseline | A pre-operation measurement for one named memory or disk scope. It is not the Default configuration. |
| Reference run | The run used as the left-hand comparison reference; it is not a factor control. |
| Preset | An optional, versioned alternative starting plan. It never mutates or silently replaces the Default configuration. |

The UI and backend use three different work counts and never collapse them into
one ambiguous “requests” value:

- **Test combinations**: expanded cells.
- **Trial batches**: the sum of `warmups + measured trials` over all cells.
- **Issued product requests**: trial batches multiplied by concurrent request
  count for Command and File Operations, by workspace count for Workspace
  Lifecycle, and by exactly one for LayerStack regardless of `N`.

LayerStack remount attempts are phase spans and outcome observations inside the
one squash request. They are not counted as additional public product requests.

## 5. Count and concurrency semantics

| Family | UI field | Default values | Meaning in one trial | Primary aggregate |
|---|---|---:|---|---|
| Command | Concurrent requests | `1, 5, 20` | Release that many `exec_command` requests through one barrier. | Request latency plus batch makespan and successful ops/s. |
| File Operations | Concurrent requests | `1, 5, 20` | Release that many calls of the selected file operation, each using a deterministic independent target unless contention mode is explicitly selected. | Request latency plus batch makespan and successful ops/s. |
| Workspace Lifecycle | Workspace count | `1, 5, 20` | Create that many explicit workspace sessions concurrently against one prepared sandbox and workspace fixture. | Create latency plus time until all sessions are ready. |
| LayerStack | Live sessions `N` | `0, 1, 5, 20` | Prepare `N` live sessions that are exposed to the post-commit remount sweep, then issue exactly one squash request. `N` is not the number successfully remounted. `N=0` is the squash-only control. | Total squash, storage phases, sweep wall time, and per-session remount distribution. |

For LayerStack, the runner also records:

- `M`: sessions observed with disposition `Migrated`.
- `I = N - M`: non-migrated sessions, further classified as `Identity`,
  `Leased`, `Faulty`, or `SessionGone`.
- `W`: configured remount sweep width; default `4`.
- `B`: squashable block count.
- `L`: published layer count and layers per block.

`M` is an observation, not blindly copied from the requested migration ratio.

## 6. Default configuration and factor catalog

Each family has an immutable, versioned Default configuration assembled from
the standard values below. The family page renders that resolved plan first,
including the enabled operations, factors, effective per-cell protocol groups,
test-combination count, trial-batch count, issued-request count, duration range,
disk estimate, and current validation state. The primary action is available as
**Review default run**; users do not have to enter a configuration workflow to
run a trustworthy starting study.

**Customize** edits a draft copied from the Default configuration. A changed
field is identified by comparing the backend-canonical current plan with the
immutable default identified by `(id, version, scope)`. Machine-local runner
bindings are outside both plans. `scope` is `all` on the central page and
`command`, `files`, `workspace`, or `layerstack` on a family page. Reset for one
field restores its scoped default value; **Reset all** must reproduce the exact
scoped default canonical plan and clear customized state. Loading a preset
replaces the draft with the preset's visible, complete scoped plan. That plan's
`configuration_base` must exactly match the page's Default configuration, so it
produces a Customized configuration whenever its canonical values differ.
Optional starting-preset provenance is request/manifest authoring metadata
outside the canonical plan; it never changes canonical equality, `plan_hash`,
or the reset target.

The Default configuration is fully explicit; it is not a set of hidden server
fallbacks applied when fields are omitted. The backend is the sole source of its
id, version, and resolved values, and every run manifest stores the full
canonical plan needed for reproduction.

Canonical input factors have role `varied` or `controlled`, one or more typed
values, and exactly one control value when varied. `Derived` values are results,
not editable plan factors. The editor may offer `fixed`, `series`, and `range`
entry modes, but it expands a range to canonical typed values before backend
validation; canonical YAML contains the resolved values so visual and YAML
editing cannot disagree. The backend expands factors and returns exact cells
before a run can start.

### 6.1 Configuration classification

Every configurable or recorded value belongs to exactly one class:

| Class | Meaning | Examples and authority |
|---|---|---|
| Experimental factor | A value intentionally varied or controlled in a study. | Concurrency, workspace profile, payload size, session mode, contention mode, and LayerStack `N`, `W`, `B`, and layer topology. Operation definitions declare valid values and combinations. |
| Protocol | How a valid cell is repeated and observed. | Trials, warmups, cell order, seed, timeout, sampling interval, and the fixed stabilization algorithm. |
| Environment and client cohort | The product/runtime context, not an operation treatment factor. | Plan-selectable image and `direct_client` or `cli_e2e`; machine-local workspace-root binding; resolved product versions; and later a redacted remote endpoint identity. |
| Operation definition | Compile-time product meaning and capability. | Count semantics, execution shape, factor schema, isolation, access allowlist, checks, phases, and semantic revisions. Ordinary plans cannot redefine these. |
| Derived value | Exact work, estimate, or observation computed from other data. | Cells, requests, plan hash, fixture hash, actual materialized cost, LayerStack `M`/`I`, availability, outcomes, and statistics. Derived values are read-only. |
| Safety policy | A fixed boundary ordinary and advanced plans cannot bypass. | One active campaign, sequential families, isolated gateway, exact internal allowlists, path containment, ownership markers, cleanup rules, output caps, and no automatic retry. |

Runner retention and diagnostic logging are administrative settings outside the
portable experiment plan. They do not become experimental factors merely
because machine-local runner configuration can change them. V1 shows their
effective values read-only in the UI; only the workspace root is edited there.

#### 6.1.1 Common protocol

| Protocol field | Standard values | Notes |
|---|---|---|
| Measured trials | Fast cells `30`; destructive cells `10` | Resolved after operation boundary and isolation factors are known. Destructive means automatic-session command, sessionless file mutation, session creation, and squash. |
| Warmups | Fast cells `2`; destructive cells `1` | Resolved after operation boundary and isolation factors are known. Warmup artifacts remain recorded but are excluded from statistics. |
| Seed | `20260712` | Controls fixtures, cell randomization, request target selection, and bootstrap resampling. |
| Cell order | Randomized blocks | Randomize within a family while blocking changes that require gateway restart. |
| Resource interval | `100 ms` raw, `500 ms` live UI | Raw interval is configurable from `20–1000 ms`. |
| Request timeout | `120 s` | LayerStack may override to `600 s`. |

Quick Smoke applies one warmup and five measured trials to its bounded cells.
Publication applies three warmups and 100 measured trials to resolved fast
cells, and two warmups and 30 measured trials to resolved destructive cells.
The UI shows every effective cell protocol before review and the resulting
successful `n` beside every percentile.

Protocol defaults resolve per expanded cell, not once per family. A File
Operations run can therefore show “read, blame, and session mutation: 2 + 30”
beside “publish mutation: 1 + 10.” A family-wide override must be explicit and
must write exact warmup and measured-trial counts into every expanded cell.

The stabilization algorithm and campaign failure policy are fixed in v1. The
expanded plan and manifest record their version and effective timeouts so a
resource result cannot silently use a different settle boundary.

#### 6.1.2 Environment and client cohort

The default image is `ubuntu:24.04`; its resolved digest is recorded. The
portable plan selects a typed `client_cohort`, defaulting to `direct_client`.
`cli_e2e` deliberately includes CLI process behavior and is scientifically
distinct. These cohorts are not comparable unless a future versioned
comparison protocol explicitly defines a valid projection; an ordinary plan
cannot relabel one as the other.

A later `remote_product` cohort is an environment boundary and product-client
implementation, not a new scheduler or distributed-runner design. Endpoint,
TLS, and credential resolution are machine-local. Manifests store only a
redacted endpoint identity and credential-reference identifier; secret values
never enter plans, events, observations, or reports. Gateway mode remains
fixed to `isolated` and appears only as effective manifest state.

### 6.2 Workspace profiles

The simple UI exposes named profiles. Advanced mode may vary their fields
independently. All bytes are genuinely materialized; sparse files do not count
toward the target.

| Profile | Files | Logical bytes | Maximum depth | Standard run |
|---|---:|---:|---:|---|
| Small | 1,000 | 16 MiB | 4 | Included |
| Medium | 10,000 | 256 MiB | 8 | Included |
| Large | 50,000 | 2 GiB | 12 | Opt-in |

The deterministic shape is 80% small text files, 15% medium binary files, and
5% larger binary files adjusted to reach the byte target. The fixture manifest
records requested and actual file count, logical bytes, allocated bytes,
directory count, maximum depth, generator version, seed, and tree hash.

Workspace size and workspace count answer different questions and must be
plotted as separate axes: profile measures metadata/data scale; count measures
concurrent session creation.

Profile definitions are versioned data when the existing generator already
supports their shape. A Metadata Heavy profile with 250,000 tiny files and deep
directories therefore needs only a profile entry and fixture test if directory
breadth, depth, counts, and size distribution are supported. If the generator
cannot express that shape, add one ordinary typed generator branch and increment
its version; do not add a generator plugin interface. The cache key hashes the
complete profile, generator version, and seed. Estimates and manifests keep
requested and actual file/directory counts, depth, logical and allocated bytes,
inode use when available, generation duration, and the materialized tree hash.

### 6.3 Operation-specific factors

| Operation | Primary varied factors | Controlled/default case |
|---|---|---|
| `exec_command` | Concurrent requests; workspace profile; `explicit` vs `automatic` session; command case | `true`, explicit session, Small profile. Additional cases: 64 KiB output, 50 ms CPU, and deterministic filesystem read. |
| `file_read` | Concurrency; returned bytes/lines; snapshot vs session; independent vs same-file contention | Snapshot, independent files, `4 KiB`, `64 KiB`, `256 KiB`; never request beyond configured output/line caps. |
| `file_write` | Concurrency; content bytes; session vs publish; independent vs same path | Independent paths; `4 KiB`, `256 KiB`, `3 MiB`; both session and publish presets. |
| `file_edit` | Concurrency; file bytes; replacement count; match density; session vs publish | Independent paths; one unique replacement; `4 KiB`, `256 KiB`, `3 MiB`. |
| `file_blame` | Concurrency; line count; ownership segments; auditability event count | Published snapshot; `100`, `2,000`, `50,000` lines and `1`, `10`, `1,000` segments. |
| `create_workspace` | Workspace count; workspace profile; network profile | `1`, `5`, `20`; `shared` network; Small/Medium standard, Large opt-in. |
| `squash_layerstack` | Live sessions `N`; requested migration ratio; remount parallelism `W`; squashable blocks `B`; layers per block; layer payload; session activity | `N=0,1,5,20`; ratios `0,0.5,1`; `W=4`; `B=1`; 8 layers/block; 4 KiB payload; idle sessions. `M`, `I`, dispositions, reclaimed bytes, and phase times are results, never inputs. |

The full Cartesian product is never selected implicitly. Presets choose a
bounded design; the UI shows cell, trial, request, duration, and disk estimates
before submission and requires confirmation for a large design.

## 7. Trial isolation rules

| Scenario | Required state policy |
|---|---|
| Read-only command, file read, blame | A verified cell fixture may be reused. Request targets rotate deterministically. |
| Explicit-session write/edit | Create fresh sessions per trial; destroy them after measurement. Session setup and teardown are recorded but excluded. |
| Automatic command or sessionless write/edit | Use a fresh sandbox/layerstack per trial so published layers from an earlier trial cannot bias a later one. |
| Workspace creation | Use one prepared sandbox per cell. Destroy every created session after its trial and verify the session registry returns to baseline. |
| LayerStack | Build a fresh deterministic layer/session topology for every trial. Squash is destructive, so no post-squash fixture is reused. |

Each concurrent request has its own target by default. A same-target contention
case is a separately named factor level and must never be mixed into the
independent-target baseline.

Every warmup and measured trial has four distinct timed phases: setup,
operation, correctness verification, and teardown. Warmup is a trial type, not
a fifth phase. The common scheduler owns the phase clock, trial order, request
barrier, concurrency, timeout, cancellation, sampling coordination, immutable
evidence append, and guaranteed teardown invocation. An operation lifecycle
owns only the typed work that differs:

```text
prepare(cell) → prepared topology
invocations(prepared, cell) → exact measured invocation set
invoke_one(invocation) → typed output
verify(prepared, outputs) → CheckResult records
teardown(prepared) → cleanup result
```

The runner times `prepare` as setup, releases the returned invocations through
one barrier and times them as operation, times `verify`, and finally times
`teardown`. Command, File, and Workspace creation return their concurrent
request set. LayerStack prepares `N` live sessions but returns exactly one
squash invocation. A future destructive lifecycle operation such as
`destroy_workspace` may prepare C sessions before the barrier, return C destroy
invocations for the operation phase, verify registry/cgroup/scratch removal,
and use teardown only for residue. It must not copy the scheduler or
misclassify the measured destroy as teardown.

Sample correctness is the conjunction of product success and every required
operation check. Successful-latency eligibility additionally requires the
cleanup baseline to be restored. Setup, verification, and teardown remain
outside primary operation latency but their observations are never erased.

Failure policy is fixed in v1 and cannot be selected by a plan. An individual
request or correctness failure is recorded and later trials may continue only
after verified cleanup. There is no automatic retry. Fixture integrity,
environment, path-containment, artifact-durability, or cleanup-baseline failure
aborts the campaign after best-effort owned cleanup because later samples would
not be scientifically or operationally safe.

## 8. Measurement contract

### 8.1 Time

| Metric | Definition |
|---|---|
| `request_latency_ns` | Monotonic time from sending one operation request until its final response is decoded. |
| `batch_makespan_ns` | Barrier release until the last request in the batch reaches a terminal response. |
| `throughput_ops_s` | Successful requests divided by batch makespan seconds. |
| `setup_ns`, `verify_ns`, `teardown_ns` | Separately recorded harness phases; excluded from operation latency. |
| `server_span_ns` | Authoritative duration of a matched operation span when available. |
| LayerStack phase times | Plan, flatten/build, commit, remount sweep, and each `workspace_session.remount` span. |

Raw time is integer nanoseconds. Tables display an adaptively chosen unit
(`µs`, `ms`, or `s`) consistently within a chart. Tooltips always show both the
display value and exact raw nanoseconds. No chart may mix units on one axis.

Reportable optional server phases are namespaced `PhaseObservation` records,
not nullable fields added to every trial type. Each carries stable phase id and
semantic revision, source, trial/request correlation, start offset, duration,
unit, and status. Raw unmatched spans may be retained as bounded diagnostics
but are not silently promoted into scientific metrics. Command queue delay, for
example, is available only when `exec_command` emits server-correlated timing
around its actual session gate/admission boundary; the runner must not infer it
by subtracting unrelated timestamps.

### 8.2 Memory

| Metric | Source and interpretation |
|---|---|
| `sandbox_memory_current_bytes` | cgroup `memory.current` sampled during the trial. |
| `sandbox_memory_peak_bytes` | cgroup `memory.peak` when supported; otherwise the maximum sampled current value with `sampled=true`. |
| `daemon_rss_bytes` | Daemon process resident set at baseline, peak, and settle. |
| `runner_rss_bytes` | Host runner resident set, reported separately so harness cost is visible. |
| `memory_delta_bytes` | Peak minus the pre-barrier baseline for the same scope. |

The report must not sum runner and sandbox memory into one number. Missing
kernel counters are `unavailable`, never zero.

### 8.3 CPU and block I/O

| Metric | Source and interpretation |
|---|---|
| `sandbox_cpu_time_ns` | Delta of the sandbox runtime's cumulative CPU-use counter over the named trial window, normalized exactly from its source resolution and never wall-clock CPU percentage. |
| `sandbox_block_read_bytes` | Delta of the cumulative sandbox block-I/O read counter over the named trial window. |
| `sandbox_block_write_bytes` | Delta of the cumulative sandbox block-I/O write counter over the named trial window. |

The product runtime preserves absence of CPU and block-I/O counters with
optional values. Benchmark readings convert this into explicit
`available(value)` or `unavailable(reason, source)` evidence. Missing counters
are never zero. Counter reset or regression invalidates that metric window with
a reason; it does not produce a negative or wrapped delta. Metric definitions
own their unit, scope, counter/gauge kind, aggregation, and semantic revision,
so adding one collector does not change any operation executor.

### 8.4 Disk and space

| Metric | Definition |
|---|---|
| `workspace_logical_bytes` | Sum of file logical sizes in the target workspace. |
| `workspace_allocated_bytes` | Allocated filesystem bytes where the host supports them. |
| `layerstack_bytes` | Allocated bytes below `/eos/layer-stack`, sampled at baseline, peak, post-operation, and settled. |
| `upperdir_bytes` | Private session upperdir bytes by session/sum. |
| `host_free_bytes` | Free bytes on the volume holding the test workspace. |
| `disk_delta_bytes` | Settled minus baseline for the named scope. |
| `peak_disk_delta_bytes` | Maximum sampled scope bytes minus baseline; explicitly labeled sampled. |
| `reclaimed_bytes` | Pre-squash source allocation minus settled retained allocation, with source and retained sets recorded. |
| `write_amplification` | Bytes written or peak additional allocation divided by logical changed bytes, only when both are measurable. |

Logical and allocated bytes must not be interchanged. LayerStack reports show
S0 baseline, S1 sampled peak, S2 post-commit, and S3 post-sweep/settled values.

### 8.5 Correctness

A timing sample enters the successful distribution only when the product
success contract and all required operation-specific checks pass and cleanup
restores the required baseline:

- Command: expected exit status/output and terminal lifecycle state.
- Read: content hash and requested window match.
- Write: final bytes/hash and publication/session attribution match.
- Edit: exact replacement count and final hash match.
- Blame: ranges tile the file with the expected EphemeralOS owners.
- Workspace: every session becomes usable, has the requested network profile,
  and can be destroyed without residue.
- LayerStack: content equivalence, expected manifest reduction, disposition
  accounting, no staging/remount residue, and live-session usability.

Checks compose as stable, namespaced `CheckResult` records with check revision,
verdict, bounded evidence, truncation count/hash when evidence exceeds its cap,
and artifact references. Operation or command-case definitions select only
registered checks; plans cannot inject executable verifier code. The common
runner folds the results into correctness and latency eligibility.

Failures remain in immutable observations, are displayed beside successful
`n`, and are excluded from successful distribution calculations. A report with
any correctness failure is visibly marked **Correctness failure** even if its
timing is fast. Cleanup failure remains separately visible and invalidates the
trial even when all operation checks passed.

## 9. Statistical and visualization rules

For every compatible cell and metric, retain raw values and compute:

- count, failures, minimum, maximum, arithmetic mean, standard deviation;
- median, median absolute deviation, p25, p75, and p95;
- coefficient of variation when the mean is non-zero;
- deterministic 95% percentile-bootstrap confidence interval for the median
  using 10,000 resamples and the run seed;
- Tukey-fence outlier flags without deleting or winsorizing observations.

P95 is marked **exploratory** below 20 successful measured samples. P99 is not shown in v1.
Confidence intervals are omitted when fewer than five successful observations
exist. Control-value or reference-run comparisons report absolute difference, percentage difference,
and a bootstrap 95% interval for the median difference. No default p-value or
claim of significance is produced.

Distribution display rules:

- Fewer than 30 successful measured observations for the selected metric in
  that cell: box plot plus every raw point (beeswarm/jitter).
- 30 or more successful measured observations for the selected metric in that
  cell: histogram plus ECDF; the histogram uses Freedman–Diaconis bin width,
  falling back to Sturges when the interquartile range is zero.
- Factor trends: median line with 95% confidence band and raw points.
- Matrix studies: heatmap with the numeric value in every cell.
- Resource samples: synchronized time-series panels with the operation window
  and phase boundaries.

Every chart includes title, metric definition, unit, `n`, control, confidence
method, and a table alternative. A truncated axis must be explicitly marked.

## 10. Workspace path contract

The UI stores one machine-local setting:

```text
test_workspace_root = /Users/<user>/.../Ephemeral-AI-Lab/ephemeral-sandbox-test-workspace
```

Resolution precedence is:

1. Explicit runner flag.
2. `EPHEMERAL_SANDBOX_TEST_WORKSPACE`.
3. Machine-local persisted setting.
4. The `ephemeral-sandbox-test-workspace` sibling of the discovered checkout.

Derived paths are fixed:

```text
<test_workspace_root>/benchmark/
  .eos-benchmark-root
  fixtures/<profile-id>/<fixture-hash>/
  runs/<run-id>/<cell-id>/<trial-id>/workspace/
  results/<run-id>/
  runtime/<runner-instance-id>/
```

Ordinary run/trial cleanup may delete only marker-owned targets whose canonical
path is a strict descendant of `<test_workspace_root>/benchmark/runs`. Runtime
cleanup may delete the exact active
`<test_workspace_root>/benchmark/runtime/<runner-instance-id>` directory or one
of its strict descendants, but never the `runtime` parent. Both paths also
require matching ownership-ledger identity, device containment, and no symlink
target or traversal. Cleanup never deletes the configured root, `benchmark`,
`fixtures`, `results`, or the `runtime` parent. Fixture eviction is a separate,
explicit operation guarded by fixture markers, content hashes, and run-reference
checks; it is not trial cleanup.

The path setting and recent-path history are not committed. Portable plans and
presets contain no workspace path or placeholder. The runner resolves this
machine-local binding during validation; the `ExpandedPlan` and `RunManifest`
record the effective canonical path and containment identity needed to
reproduce or audit the local run.

## 11. Page and execution contract

### 11.1 Routes

| # | Route | Page |
|---:|---|---|
| 1 | `/benchmark` | Central Benchmark Laboratory |
| 2 | `/benchmark/command` | Command family |
| 3 | `/benchmark/files` | File Operations family |
| 4 | `/benchmark/workspace` | Workspace Lifecycle family |
| 5 | `/benchmark/layerstack` | LayerStack family |
| 6 | `/benchmark/runs/:runId` | Shared live run |
| 7 | `/benchmark/reports/:runId` | Shared scientific report |
| 8 | `/benchmark/compare` | Shared run comparison |

Settings, plan review, and YAML are drawers/modals, not more pages.

### 11.2 Run controls

- Central page: **Review default run**, **Open family**, and **Customize**. The
  default review includes all enabled families and starts them sequentially as
  **Run All Locally**. Quick Smoke is a visibly lower-cost alternate starting
  point, not a hidden replacement for the Default configuration.
- Family page: show the resolved **Default configuration**, then offer **Review
  default run** and the secondary **Customize** action. Customized plans use
  **Review customized run** and always retain **Reset all**.
- File page: one included-operation master list with a persistent detail editor
  for read, write, edit, and blame. Switching operations retains edits. At narrow
  widths the same model becomes an accordion; a second tab set or detached
  family-set popover is forbidden.
- LayerStack page: one squash action grouped as Storage topology, Live-session
  load, Remount policy, and Outcomes to measure. Only `N`, requested migration
  ratio, `W`, `B`, layer count, payload, and activity are editable.
- Every action first sends the plan to backend validation. A run starts only
  from the returned expanded plan hash.
- Run All executes Command → Files → Workspace → LayerStack. Family order is
  fixed and families never overlap in v1; the seed affects cell order only.

The review modal shows operations, test combinations, trial batches, issued
product requests, effective warmups and measured trials per operation,
estimated duration range, estimated peak disk, free-space check, required
gateway restarts, workspace root, destructive fixtures, cleanup policy,
separately labeled artifact-retention policy, and validation warnings. Its
sticky action footer never covers review evidence.

## 12. Canonical plan example

The visual builder and YAML drawer edit the same `ExperimentPlan` model. YAML
is a presentation format; the backend returns canonical JSON and `plan_hash`.

```yaml
schema_version: 1
name: standard-local
configuration_base:
  id: standard-local
  version: 1
  scope: all
seed: 20260712
environment:
  image: ubuntu:24.04
  client_cohort: direct_client
protocol:
  order: randomized_blocks
  resource_interval_ms: 100
  trial_defaults:
    fast: {warmups: 2, measured_trials: 30}
    destructive: {warmups: 1, measured_trials: 10}
  timeout_ms:
    default: 120000
    squash_layerstack: 600000
operations:
  - operation: exec_command
    configuration:
      enabled: true
      factors:
        concurrent_requests: {role: varied, values: [1, 5, 20], control: 1}
        workspace_profile: {role: controlled, values: [small]}
        session_mode: {role: controlled, values: [explicit]}
        command_case: {role: controlled, values: [noop]}
  - operation: file_read
    configuration:
      enabled: true
      factors:
        concurrent_requests: {role: varied, values: [1, 5, 20], control: 1}
        returned_bytes: {role: varied, values: [4096, 65536, 262144], control: 4096}
        source: {role: controlled, values: [snapshot]}
        target_mode: {role: controlled, values: [independent]}
  - operation: file_write
    configuration:
      enabled: true
      factors:
        concurrent_requests: {role: varied, values: [1, 5, 20], control: 1}
        content_bytes: {role: varied, values: [4096, 262144, 3145728], control: 4096}
        destination: {role: controlled, values: [session]}
        target_mode: {role: controlled, values: [independent]}
  - operation: file_edit
    configuration:
      enabled: true
      factors:
        concurrent_requests: {role: varied, values: [1, 5, 20], control: 1}
        file_bytes: {role: varied, values: [4096, 262144, 3145728], control: 4096}
        replacement_count: {role: controlled, values: [1]}
        destination: {role: controlled, values: [session]}
        target_mode: {role: controlled, values: [independent]}
  - operation: file_blame
    configuration:
      enabled: true
      factors:
        concurrent_requests: {role: varied, values: [1, 5, 20], control: 1}
        line_count: {role: varied, values: [100, 2000, 50000], control: 100}
        ownership_segments: {role: controlled, values: [10]}
  - operation: create_workspace
    configuration:
      enabled: true
      factors:
        workspace_count: {role: varied, values: [1, 5, 20], control: 1}
        workspace_profile: {role: varied, values: [small, medium], control: small}
        network_profile: {role: controlled, values: [shared]}
  - operation: squash_layerstack
    configuration:
      enabled: true
      factors:
        live_sessions: {role: varied, values: [0, 1, 5, 20], control: 0}
        requested_migration_ratio: {role: controlled, values: [1.0]}
        remount_parallelism: {role: controlled, values: [4]}
        squashable_blocks: {role: controlled, values: [1]}
        layers_per_block: {role: controlled, values: [8]}
        payload_bytes: {role: controlled, values: [4096]}
        session_activity: {role: controlled, values: [idle]}
```

`operations` is a flat list of Serde-tagged typed operation plans. Each
operation id appears at most once, and its family is derived exclusively from
the compile-time `OperationDefinition`; plans cannot repeat or contradict
family membership. `enabled` remains inside the typed operation configuration
so deselection preserves its edits. Enabled families are derived from enabled
operations. The top-level `seed` is semantically a protocol field despite its
stable wire location.

The backend rejects unknown fields. Byte values in canonical JSON are integers;
the UI may accept `KiB`, `MiB`, and `GiB` and display the resolved byte count.
`command_case` selects a registered template whose resolved bounded product
`cmd` is recorded in the expanded plan and manifest; it is not arbitrary shell
text or an argv supplied by YAML.
`plan_hash` covers the canonical portable plan, non-secret effective environment
including workspace-root identity, definition revisions, exact expanded cells
and execution blocks, and fixed lifecycle policy. Secrets and authoring-only
provenance are excluded. The runner re-expands before starting and rejects the
hash if any effective input changed after validation.
The expanded plan records an exact effective protocol per cell because fast and
destructive boundaries may coexist in one File Operations family run. Editor
entry modes are not serialized; their resolved factor values are. The backend
returns `is_customized` by comparing this canonical plan with the Default
configuration identified by `(configuration_base.id,
configuration_base.version, configuration_base.scope)`. Machine-local runner
bindings are outside both canonical plans. Preset provenance, when present, is
stored outside this canonical plan and is not part of `plan_hash`.

## 13. Run and artifact contract

The backend owns these shared entities:

| Entity | Required identity and contents |
|---|---|
| `ExperimentPlan` | Versioned user intent. It contains typed operation plans, experimental factors, protocol, and portable environment/cohort selections, but no derived cells, secrets, handler names, or safety overrides. |
| `ExpandedPlan` | Exact ordered typed cells, effective per-cell protocol, seeds, resolved machine-local workspace binding, fixture identities, invocation counts, estimates, operation/access/isolation definitions, and `plan_hash`. It is the only execution input. |
| `RunManifest` | Run id, plan hash, source commit/dirty state, image digest, host/kernel/Docker/filesystem and workspace-binding data, redacted client/access identity, effective fixed gateway and safety policy, requested and effective product caps, definition snapshot and revisions, fixture hashes, lifecycle/failure/stabilization versions, timestamps, and terminal state. |
| `TrialSample` | Common cell/trial/request ids, warmup flag, typed operation evidence reference, phase timers, product outcome, and raw-record references. It does not embed a second resource, check, or statistical authority. |
| `ObservationRecord` | A tagged, versioned `Trial`, `Resource`, `Phase`, `Check`, or typed operation-evidence record correlated by run/cell/trial/request ids. |
| `RunSummary` and report model | Regenerable grouped statistics, warnings, failures, compatibility identity, and derived views. They are never raw evidence. |

The intent plan and expanded plan are written atomically before execution.
Observation records and bounded evidence are append-only. The manifest is
atomically replaced for lifecycle state changes and becomes immutable at its
terminal state:

```text
results/<run-id>/
  run-manifest.json
  intent-plan.json
  expanded-plan.json
  events.ndjson
  observations.ndjson
  cells/<cell-id>/trials/<trial-id>/bounded-evidence/...
  summary.json
  report.json
```

`intent-plan.json`, `expanded-plan.json`, `run-manifest.json`,
`observations.ndjson`, and bounded evidence are the immutable authority.
`events.ndjson` is a resumable progress/diagnostic projection, not a competing
scientific record. `summary.json`, `report.json`, exports, and indices may be
deleted and regenerated using only authoritative artifacts; regeneration does
not require executors, product clients, Docker, or the original UI.

Every persisted JSON/NDJSON envelope carries a schema name and version.
Operation semantics, factor schemas, metrics, checks, phases, fixture
generators, comparison protocols, and report derivations carry independent
stable revisions because they do not necessarily evolve together. The reader
keeps explicit decoders for every released v1 artifact version, converts old
records into the current in-memory observation model, and never rewrites old
raw files. Unsupported schemas or versions fail with a precise error rather
than being ignored or interpreted under current semantics. Plans reject unknown
fields for their declared version. Reports use the run's persisted definition
snapshot, not merely the definitions compiled into the current runner.

Secrets, daemon auth tokens, credential values, full environment variables,
and unbounded command output are forbidden. Output stored for correctness is
size-capped and hashed. Partial trailing NDJSON records from a crash are
detected and reported; preceding complete observations remain immutable and
readable.

## 14. Comparability rules

Compatibility is evaluated before deltas. The comparison contract separates
**scientific invariants** from a deliberately changed **treatment identity**.
Every operation definition projects a persisted typed `ComparisonKey`. At a
minimum it contains operation id and semantic revision, factor-schema revision
and canonical typed factors, client cohort and product-access identity, fixture
hash, isolation and effective protocol identity, environment fingerprint, and
the measurement revisions required by the requested view. Changing operation
meaning, phase endpoints, count semantics, or correctness eligibility requires
incrementing the corresponding semantic revision; changing a display label
does not.

The Compare page blocks an aggregate comparison when any of these invariants
differ:

- operation id, semantic revision, factor-schema revision, or typed operation
  factor values;
- client cohort, product-access path, isolation, or effective protocol;
- workspace fixture hash and fixture-generator revision;
- non-treatment image/runtime settings and effective benchmark configuration;
- host architecture, kernel major/minor, Docker engine major, or filesystem;
- required measurement definition, schema, clock, or resource sampling
  interval.

Metric compatibility is view-specific without weakening the core cohort. Two
runs may remain latency-compatible when CPU was unavailable in one run, but a
CPU comparison or CPU-versus-latency correlation requires the same CPU metric
id, semantic revision, scope, unit, and availability semantics. Unavailable
data yields an explicit reason instead of a zero or a silently smaller cohort.

Source commit/diff hash and daemon/gateway binary hashes are treatment identity
fields. The sandbox image digest remains an environment invariant. An ordinary
same-treatment comparison requires the treatment identity to match. A Release
Comparison plan must explicitly declare the allowlisted product treatment
identity fields intended to differ; all other invariants and treatment fields
still have to match. The UI shows that declaration before showing performance
deltas, so a product build change is not mistaken for an environment mismatch.
The reference and candidate must carry identical versioned comparison
declarations—the same protocol id, protocol version, and treatment-field
allowlist—or the pair is incompatible. The backend never unions or broadens
treatment allowlists after execution. Two absent declarations normalize to the
versioned default same-treatment protocol with an empty allowlist; one absent
and one explicit declaration is incompatible.

For compatible cells, absolute change is `candidate - reference`. Percentage
change is `(candidate - reference) / reference × 100` only for ratio-scale
metrics with a positive reference; otherwise it is unavailable with a reason.
Every row states whether lower, higher, or neither direction is ordinarily
preferred, but v1 does not convert direction into a regression verdict. A
verdict requires a future versioned threshold/decision policy.

The user may choose **Show side by side anyway**, but the UI labels the result
**Descriptive only**, suppresses aggregate claims, and does not calculate a
regression verdict. Dirty source trees are allowed but visibly tagged and
include the diff hash in the treatment identity.

## 15. Presets

The versioned `standard-local` plan is the Default configuration on the central
and family pages; the user-facing heading remains **Default configuration** so
“baseline” is not confused with a resource baseline or factor control. It is
not a preset-gallery choice. **Load another preset** is a secondary customization
action. The first implementation supplies these bounded alternatives:

- Quick Smoke
- Publication
- Concurrency Scaling
- Payload Scaling
- Workspace Size × Count
- File Metadata / Blame Scaling
- Squash Only (`N=0` control)
- Squash + Remount (`N=1,5,20`)
- Remount Width (`W=1,2,4,8`)
- Active Session Interruption
- Release Comparison

Each preset file is a strict envelope containing its schema version, id,
version, and one complete `ExperimentPlan`; presets are not overlays and there
is no merge order. Scope has one representation: the embedded plan's
`configuration_base.scope`, which must exactly match the Default for that
scope. Loading one never hides its factors; users see and may edit the complete
values before running. Quick Smoke is the
clearly labeled lowest-cost setup check on the central page. Release Comparison
defines a two-treatment comparison protocol; its name never implies that the result is
automatically a regression.

Preset discovery reads strict versioned data files and passes them through the
same public plan parser, validator, and expander as user plans. A preset may
select only existing operations, factors, protocol, and portable environment
values. It cannot name an executor, product route, internal RPC, verifier
function, cleanup policy, arbitrary command, credential, or safety override.
Adding “High Contention File Writes” from existing capabilities therefore
requires one preset file and a validation/golden test, with no executor, route,
or report code.

## 16. Implementation boundary and release criteria

The backend is a separate trusted loopback service, not an extension of the
general web console. It may invoke test-only internal session lifecycle through
a narrow allowlisted adapter, but it must not expose internal operations as a
general browser RPC. Public operations use the same operation contract and
gateway path as product clients. Daemon HTTP-only operations use their exact
typed HTTP adapter. The internal workspace adapter exposes only typed create
and destroy methods, rejects every other operation before credential or network
access, and operates only on runner-owned sandbox/session identities. Registering
an operation never broadens any of these access paths.

The v1 release is complete only when:

1. All eight routes work at 375, 768, 1,024, and 1,440 px.
2. Each family can validate and run alone; Run All executes sequentially.
3. Count semantics are displayed and enforced exactly as section 5 defines.
4. Workspace root discovery, override, validation, and safe cleanup pass.
5. Raw timing, memory, disk, CPU, block-I/O, phase, and correctness artifacts
   survive runner restart and can regenerate the same summary.
6. LayerStack reports separate storage from remount sweep and include `N`,
   observed `M`, `I`, `W`, `B`, and disposition counts.
7. Charts expose raw points and accessible tables, with no color-only status.
8. Compare refuses incompatible statistical claims.
9. Cancellation stops future trials, terminates owned work, and writes a valid
   cancelled manifest without deleting evidence.
10. Automated unit, integration, live-Docker smoke, accessibility, and visual
    tests pass with no secret or path-escape findings.
11. Every family opens with a runnable Default configuration; customization,
    field reset, and Reset all are deterministic canonical-plan transitions.
12. Test combinations, trial batches, and issued product requests remain
    distinct in validation, review, progress, artifacts, and reports.
13. Every operation definition is in bijection with typed dispatch and product
    access, and all extension acceptance tests in section 17 pass.

## 17. Extension acceptance tests

These tests are release gates. Each is observable and automatable; passing by
manual architectural assertion is insufficient.

| Extension property | Automated proof |
|---|---|
| Registration is exhaustive and safe | Compile-time/all-variants tests prove every `OperationId` has exactly one definition, lifecycle dispatch, closed product-access choice, semantic/factor revisions, and comparison projection; duplicate ids and unregistered handlers fail. |
| Presets are data-only | Add a temporary valid preset using existing capabilities. Discovery, strict parsing, expansion, and golden plan tests pass, and a changed-path assertion permits only the preset and its test fixture. |
| Same-generator fixture profiles are data-only | Add a profile using already supported generator fields. It materializes the declared shape and deterministic hash without operation/executor changes. |
| An operation reuses the common pipeline | A test-only typed fake lifecycle returns C invocations and one failed check. The shared barrier, four phase timers, resource sampling, immutable observations, failure exclusion, statistics, and generic report all run without fake-specific scheduler or report code. |
| LayerStack retains its topology | With `N=20`, spies observe 20 prepared live sessions and exactly one squash product request. `N` is stored as live-session load, never request concurrency. |
| Destructive lifecycle phases are honest | A test destroy-workspace lifecycle prepares C sessions before the barrier, measures C destroys as operation, verifies registry/cgroup/scratch absence, and uses teardown only for residue. No scheduler code is copied. |
| A metric does not change executors | A test collector and metric definition round-trip through availability-aware raw records, summary, export, and generic chart data. Dependency tests prove operation modules do not import collector implementations. |
| Unavailable is not zero | Inject unavailable CPU and block-I/O counters. Raw records and reports contain `unavailable` with source/reason, latency remains usable, and metric-specific comparison/plots refuse the missing data. |
| An operation-specific phase is namespaced | Round-trip `command.queue_delay/v1` for one correlated command request. Its endpoints and revision survive regeneration, and golden serialized samples for unrelated operations do not gain nullable command fields. |
| Correctness checks compose | Enable a filesystem-integrity check for one command case and exceed its evidence cap. The stable check id fails the common verdict, stores truncation count/hash, excludes the latency, and does not run for unselected cases. |
| Old artifacts regenerate | Load every supported released v1 artifact fixture with the current reader. Rebuilt summary/report goldens match, no executor/product client is loaded, and raw fixture bytes remain unchanged. |
| Internal access is closed | Attempt to register or invoke an unregistered internal action. It fails before credential lookup or socket creation, verified by zero-call spies. |
| Cleanup cannot be bypassed | Inject failure/cancellation in every lifecycle phase and simulate leftover state. Teardown is attempted on every reachable path, outside-root sentinels remain untouched, leaked state invalidates the trial, and the campaign aborts. |
| Comparison follows semantics | Two otherwise identical manifests with different operation semantic revisions are rejected with a typed mismatch; changing only a display label remains compatible. |
| Client cohorts remain distinct | Equivalent `direct_client`, `cli_e2e`, and test `remote_product` observations are incompatible by default; the remote manifest contains no secret value and uses the same local scheduler. |
| `file_list` preserves product and safety semantics | Adapter spies show only daemon HTTP access. Zero limit is rejected; a positive requested limit is clamped by the fixed runtime cap; requested/effective limit, result count, and truncation round-trip in evidence. |
| Report views are derivations | Known latency/CPU observations, including correctness failures and unavailable CPU, produce one deterministic backend correlation model used unchanged by API, export, and UI fixtures; no execution module is loaded. |
| Schema handling is deliberate | Unknown fields in a current plan and unsupported future schema versions fail explicitly; every supported old version decodes through its named reader without rewriting raw evidence. |
