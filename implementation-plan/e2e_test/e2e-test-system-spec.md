# EphemeralOS E2E Control Room — System Specification

| Field | Value |
| --- | --- |
| Status | Rewritten after adversarial review; implementation not started |
| Date | 2026-07-12 |
| Product checkout | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox` |
| Planned test repository | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test` |
| Mutable store | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test-workspace` |
| Technical design | [e2e-test-design.md](e2e-test-design.md) |
| UI design | [e2e-test-ui-design.md](e2e-test-ui-design.md) |
| Delivery plan and review ledger | [e2e-test-implementation-plan.md](e2e-test-implementation-plan.md) |

The words **MUST**, **SHOULD**, and **MAY** are normative. “Current” means
verified in the repository on the date above. “Planned” means specified here but
not implemented. A screen mockup, proposed schema, or document statement is not
implementation evidence.

## 1. Executive verdict and design rule

The architecture is **PASS AFTER REWRITE**. The previous draft had a credible
safety core but surrounded it with duplicate journals, projections, registries,
API resources, telemetry machinery, and recovery records. Those additions made
the system harder to build and harder to trust.

The rewritten system has one ordinary path:

```text
Rust product catalog + one E2E metadata catalog + pytest declarations
  -> complete side-effect-free collection
  -> one atomically published catalog
  -> one preview
  -> one immutable run manifest
  -> one append-only run event journal
  -> one pure run projection
  -> one generic API and UI
```

Every additional subsystem must defend a distinct source of truth, safety
boundary, durability requirement, or measured performance need. V1 does not add
an index, cache, plugin system, workflow engine, compatibility matrix, telemetry
platform, or domain-specific UI.

## 2. Outcomes and scope

### 2.1 Required user outcome

A first-time engineer can:

1. search by product behavior, test purpose, feature, validation, owner, or ID;
2. select an exact mixture of expanded pytest cases without knowing node IDs;
3. review the exact scope, source/product identities, execution boundaries,
   workspace policy, fail-fast policy, evidence policy, and preflight outcome;
4. start once and see queued, running, validation, failure, cleanup, and terminal
   progress without reading raw pytest output;
5. distinguish product verdict from evidence health;
6. reconnect or refresh without duplicate state or false “live” claims;
7. inspect the same frozen truth later, including after explicit evidence purge;
8. retry a visible subset as a new child run.

### 2.2 Required in v1

- side-effect-free collection mode;
- stable test and expanded-case identity;
- one product/E2E metadata merge and one atomic last-good catalog;
- mixed selection, exact preview, serial execution, optional run-wide fail-fast,
  bounded cancellation, and child-run retry;
- immutable run input and source snapshot;
- typed lifecycle, validation, failure, cleanup, evidence, and surface events;
- one append-only run journal and replayable projection;
- exact-bundle restart recovery with scoped, idempotent cleanup;
- structured logs and artifacts with caps and redaction;
- fresh owned workspaces and quarantine on uncertain cleanup;
- catalog, run, history, workspace, and health UI;
- keyboard-complete responsive operation at 375, 390, 768, 1024, and 1440 CSS
  pixels and at 200% zoom;
- offline contract/reducer/UI fixtures before any focused live proof.

### 2.3 Explicitly deferred

The following are not v1 requirements:

- parallel or distributed execution;
- a database, queue, workflow engine, plugin runtime, or general scheduler;
- incremental catalog merging;
- a global history index before directory-scan latency is measured and exceeds
  the budget in §14;
- automatic workspace reuse; every case gets a fresh attempt;
- automatic evidence eviction;
- cross-version recovery; v1 recovery requires the exact admitted controller
  bundle;
- generalized high-rate telemetry, burst profiles, percentile platforms, or
  performance dashboards;
- per-domain routes, pages, icons, colors, API handlers, or state machines;
- browser-authored paths, commands, environment variables, pytest arguments,
  transport endpoints, or execution surfaces;
- arbitrary assertion instrumentation or a second test DSL.

Deferral does not weaken cleanup, containment, evidence health, redaction,
replay, or accessibility.

## 3. Verified baseline

The implementation plan records the detailed evidence. The system depends on
these verified facts:

| Item | Current fact | Consequence |
| --- | --- | --- |
| Test location | Live pytest source is under `<PRODUCT_ROOT>/e2e`; the planned external test repository does not exist. | Migration begins only after stable IDs are recorded. |
| Suite shape | 103 tracked E2E files, 75 Python files, and 264 test functions were observed; existing design material reports 373 expanded cases. | Counts are migration baselines, never UI constants. |
| Collection | Session autouse fixture starts/reuses the gateway. | A separate side-effect-free collector entry point is a hard Phase 0 gate. |
| Cleanup | Several cleanup paths catch and discard exceptions. | Cleanup aggregation must be fixed before a passing verdict is trusted. |
| Source writes | Session summary writes timing artifacts into product documentation. | Collection and controller output move entirely to the external store. |
| Product catalog | Rust `sandbox-operation-catalog` owns declarations; the console exposes `/api/catalog` only while running. | Add a small offline export from the same Rust projection; do not copy vocabulary into Python. |
| Product boundaries | CLI, direct daemon HTTP, raw gateway, and allowlisted direct daemon RPC helpers exist; console `/api/rpc` and proxy routes exist product-side. | Surface proof can wrap real boundaries; the Control Room itself is not implemented. |
| Prototype | `e2e/ui-prototype` is static HTML/CSS plus screenshots. | It is visual direction only and proves no interaction, data, accessibility, or runtime state. |
| Benchmark store | Benchmark currently appends `benchmark/` below a configurable root and owns its own marker. | The fixed store contract must avoid `benchmark/benchmark` and preserve benchmark ownership. |

## 4. Roots, ownership, and source boundaries

Only three roots are configured at controller startup:

- `TEST_REPOSITORY_ROOT`: one Git repository containing `e2e/` and optional
  non-product benchmark configuration;
- `PRODUCT_ROOT`: the EphemeralOS checkout;
- `WORKSPACE_STORE_ROOT`: the external mutable parent.

The controller derives without override:

- `E2E_SOURCE_ROOT=<TEST_REPOSITORY_ROOT>/e2e`;
- `BENCHMARK_SOURCE_ROOT=<TEST_REPOSITORY_ROOT>/benchmark`;
- `E2E_WORKSPACE_ROOT=<WORKSPACE_STORE_ROOT>/e2e`;
- `BENCHMARK_WORKSPACE_ROOT=<WORKSPACE_STORE_ROOT>/benchmark`.

All configured roots MUST be canonical, absolute, pairwise disjoint, and neither
aliases nor ancestors of one another. Source roots are read-only during
collection and execution. Browser requests cannot contain any root or path.

Each mutable child root has its own immutable ownership marker. The E2E
controller never initializes or mutates the benchmark child. Benchmark code
never initializes or mutates the E2E child. Neither owner may delete a child
root, its marker, a direct role directory, either repository, or the store
parent.

## 5. One owner per fact

| Fact | Sole owner | Consumers |
| --- | --- | --- |
| Product domain, family, operation, public route | Rust `sandbox-operation-catalog` | offline export, collector, UI through combined catalog |
| E2E-owned Harness topology, Compound scenario topology/complexity, owners, execution-label definitions, display hints | `<E2E_SOURCE_ROOT>/metadata/catalog.yaml` | collector only |
| Test purpose, stable ID, expanded case ID, validations, feature claims, policies, expected surface | typed declaration beside the pytest test | collector, runner through frozen manifest |
| Current combined catalog | atomically published `catalog/current.json` | API and preview |
| Catalog availability/diagnostics | `catalog/health.json` | health and UI |
| Admitted run inputs | immutable `manifest.json` | runner, reducer, UI |
| Execution and post-terminal purge history | `events.jsonl` | reducer, SSE, and evidence API |
| Current/historical run view | derived `run.json` | API and UI |

There is no separate feature registry, taxonomy registry, catalog event journal,
per-case result authority, recovery-session file, or global run-summary file.
Labels needed for history are frozen into the run manifest. Mutable current
catalog data is never joined into a historical verdict.

## 6. Catalog and contributor model

### 6.1 Collection

Collection MUST use a dedicated command that:

- does not execute session autouse fixtures, gateway startup, Docker calls,
  terminal-summary writers, `atexit` writers, or product runtime preflight;
- loads the offline Rust catalog projection;
- loads one E2E-owned `metadata/catalog.yaml`;
- collects expanded pytest items and their typed declarations;
- reports every independent local error in one attempt;
- publishes no partial catalog;
- writes candidates only below `<E2E_WORKSPACE_ROOT>/tmp`;
- atomically replaces `catalog/current.json` only after complete validation;
- preserves the last-good catalog and updates `catalog/health.json` on failure.

Refresh uses a simple complete input digest and a coalesced watcher. Manual
refresh MAY exist as a controller action, but the ordinary UI receives one
revision notification and performs one catalog refetch. A refresh journal is
not required because refresh attempts are operational diagnostics, not durable
product evidence.

### 6.2 One declaration shape

The declaration API is a thin pytest annotation, not an executor. Every expanded
case has:

- globally stable `test_id` and explicit stable `case_id` (`default` when not
  parameterized);
- title, purpose, owner, source location, and current pytest node ID;
- `kind=product | harness`;
- named validations with stable ID, description, phase, and requiredness;
- references to E2E-wide execution labels categorized as scheduling, cost, or
  risk when applicable;
- workspace policy, evidence policy, resource claims, and timeout;
- for product cases, one taxonomy leaf, at least one direct product feature,
  validation-to-feature mappings, and one expected execution surface;
- for Compound product cases, the same Product claims plus one E2E-owned
  `compound` record containing a complexity ID, at least two subject domains,
  ordered component IDs with `subject | fixture | evidence` roles, and an
  explicit shared-workspace/teardown contract;
- for harness cases, no product taxonomy or coverage claim; an optional surface
  or explicit `product_boundary_claim=not_applicable`.

Parameters are represented only by author-supplied bounded JSON summaries. The
collector never calls arbitrary `repr`, `str`, pickle, or custom serializers.

### 6.3 Stable identity and provenance

`(test_id, case_id)` is the durable identity. File paths and pytest node IDs are
diagnostic selectors only. Moving a file or reordering parameters MUST preserve
identity and history.

Feature provenance is `direct | inherited`. Inheritance may expand a valid
direct claim but never hide the absence of a direct claim. Declaration coverage
and latest execution result are separate UI concepts.

Compound remains metadata, not an execution DSL. Pytest owns its ordered
cross-domain behavior. The collector validates the declared domains, roles,
complexity, shared context, features, validations, and one primary real
execution surface; the generic runner executes the case exactly like any other.

### 6.4 Generic extension contract

| Addition | Expected edits | Forbidden ripple |
| --- | --- | --- |
| Parameterized case or test in an existing group | test declaration | registry, API, or frontend edit |
| New Harness group, scenario, family, or feature | one E2E metadata record plus declarations/tests | Rust, API, route, component, style, or icon edit |
| New Product domain, family, operation, or feature | legitimate Rust catalog edits plus declarations/tests | Harness taxonomy, Python allowlist, or frontend taxonomy edit |
| New Compound scenario or complexity | one E2E metadata record plus declarations/tests | runner, route, reducer, or bespoke scenario UI edit |
| New named validation | declaration and reporter calls | reducer branch or bespoke panel |
| New Harness diagnostic area | Harness metadata plus tests | frontend navigation or color edit |

## 7. Selection, preview, and admission

### 7.1 Selection

The browser stores a revision-qualified `Selection` with only:

- explicit `(test_id, case_id)` entries;
- server query clauses using the same schema as catalog browse;
- explicit exclusions.

Node and feature checkboxes compile to a query clause. There are no separate
node, feature, group, and domain clause languages.

### 7.2 Preview

`POST /api/v1/previews` resolves the complete selection and returns one exact,
ordered preview. V1 caps an admitted run at 1,000 expanded cases; a larger
selection is blocked with an explanation rather than producing an unbounded
response.

A preview freezes:

- catalog and source revision;
- exact case records and validation declarations;
- selected policies and fail-fast mode;
- expected execution surfaces and required preflight checks;
- product binary/probe/image digests where applicable;
- controller and runner bundle digests;
- workspace template identity and disk estimate;
- blockers, warnings, creation time, and expiry.

States are `checking | ready | blocked | stale`. A ready preview expires after
ten minutes; volatile lane ownership and preflight older than 60 seconds are
rechecked at admission.

### 7.3 Admission

`POST /api/v1/runs` accepts only `preview_id`, its one-use token, and an
idempotency key. It cannot accept paths, commands, environment, pytest selectors,
surface overrides, endpoints, or credentials.

Admission atomically:

1. revalidates preview inputs and the single-run lane;
2. copies declared E2E inputs into a run-owned, non-writable source snapshot;
3. verifies the snapshot digest;
4. writes the immutable manifest containing the source-file digest list;
5. creates an empty journal and initial projection;
6. publishes the complete run directory;
7. starts the child only after bundle, product, and source identities match.

Failure before publication creates no run and does not consume the token.
Concurrent reuse of the same idempotency key and digest returns the same run.

## 8. Execution boundaries

The surface is test-owned metadata but driver choice is controller policy:

| Surface | Real boundary | Driver | Current evidence |
| --- | --- | --- | --- |
| `cli` | one product CLI subprocess | subprocess adapter | existing E2E CLI helper |
| `console_rpc` | console `POST /api/rpc` and its streaming response | HTTP/SSE adapter | product route exists; E2E adapter planned |
| `console_http_proxy` | console daemon-HTTP proxy | HTTP adapter | product route exists; E2E adapter planned |
| `gateway_rpc` | authenticated gateway JSON-line RPC | fixed product probe preferred | raw Python helper exists; fixed probe planned |
| `daemon_http` | daemon allowlisted HTTP listener | Python standard-library HTTP | existing helper |
| `direct_daemon_rpc` | authenticated daemon RPC for a fixed allowlist | fixed product probe preferred | Python allowlist helper exists; probe planned |

Every product or surface-declaring harness result records expected and observed
surface, driver, boundary, product binary/probe digest, dispatch outcome, timing,
and redacted transport evidence. Missing, duplicate, mismatched, or unavailable
proof is `error(kind=contract|infrastructure)`; it can never pass. There is no
cross-surface fallback and no automatic operation replay after dispatch may have
occurred.

Console health blocks only console surfaces. A no-surface harness case emits no
surface placeholder and says “Harness diagnostic — no product boundary claimed.”

## 9. Lifecycle and verdict semantics

### 9.1 Execution model

V1 has one controller-wide active run, one serial lane, and one pytest child.
Pytest remains the executor. The controller admits, observes, persists, cancels,
and recovers; it does not interpret a workflow graph.

### 9.2 States

Run states are:

```text
queued | running | cancelling | recovering |
passed | failed | cancelled | error
```

Case states are:

```text
queued | running | passed | failed | skipped | cancelled | error | not_run
```

Phase, validation, and cleanup states are:

```text
pending | running | passed | failed | skipped | cancelled | error | not_run
```

Unknown values under a supported schema are incompatibilities, not neutral
states.

### 9.3 Failures and pass rule

Every failure record includes stable ID, kind, message, causal sequence, entity,
phase/validation/cleanup ID, time, and evidence references. `first_failure_id`
is the earliest causal failure. `primary_failure_id` is the earliest failure in
the verdict-determining severity class, ordered `error > failed > cancelled`.

A case passes only when:

- pytest setup/call/teardown completes successfully;
- all required applicable named validations pass;
- expected surface proof is verified, or the harness no-boundary arm applies;
- all mandatory cleanup actions pass;
- required evidence dependencies are healthy enough for their validation.

Supporting evidence degradation does not change product verdict. It changes
`evidence_health` to `degraded | unavailable`. Cleanup failure is an error and
cannot be swallowed.

### 9.4 Fail-fast, cancellation, and retry

Run-wide fail-fast is opt-in and defaults off. After the first persisted outcome
that makes the active case unable to pass, no new case starts; active teardown,
mandatory cleanup, and evidence finalization continue. Remaining cases become
`not_run(reason=fail_fast, caused_by_seq=...)`.

Cancellation persists the request before signalling. It uses one frozen process
strategy with interrupt, terminate, and cleanup deadlines. Queued cases become
`not_run(reason=user_cancel)`. A run cannot remain cancelling indefinitely.

Retry creates a child preview and new run. The operator explicitly chooses
`failed`, `not_run`, or their union. Passed cases are never silently rerun.

## 10. Durable run model

### 10.1 Authoritative files

Each run has only two semantic authorities:

- `manifest.json`: immutable admitted input and frozen labels;
- `events.jsonl`: append-only execution and post-terminal purge history; it is
  retained permanently with the run record.

`run.json` is an atomically replaced pure projection of manifest plus events. It
is always rebuildable, including after explicit evidence purge. It contains all
case results; there are no duplicate per-case `result.json` files.

### 10.2 Event envelope and vocabulary

Every persisted event has:

```text
schema_version, run_id, seq, at, monotonic_ns, producer,
producer_revision, type, test_id?, case_id?, attempt_id?,
entity_id?, caused_by_seq?, payload
```

The minimal registry is:

- `run.state`, `case.state`, `phase.state`, `validation.state`, `cleanup.state`,
  `retention.state`;
- `failure.recorded`;
- `surface.recorded`;
- `evidence.recorded`, `log.recorded`, `artifact.recorded`;
- `recovery.started`, `recovery.action_started`,
  `recovery.action_finished`.

State events contain `from`, `to`, reason, timing, and applicable verdict data.
Typed entity state avoids separate start/finish/not-run event names without
making transitions ambiguous.

The journal validates schema, identity, correlation, and transition before
allocating a sequence. Persistence and sync happen before reducer update and
SSE broadcast. Invalid input receives no sequence and causes a structured
controller error; the reducer never guesses.

### 10.3 Replay and SSE

`GET /api/v1/runs/:run_id` returns `applied_through_seq=N`. The browser opens one
native EventSource at `/api/v1/events?run_id=<id>&after=N`. Numbered default
events carry the run sequence. Duplicate or old events are ignored; a gap
triggers one projection refetch. Unnumbered named controller notifications are
limited to `catalog.revision` and `stream.heartbeat`; they never enter the run
reducer. A heartbeat every five seconds carries the applied run sequence when a
run is selected. The UI marks the stream stale after 15 seconds and preserves
the last verified projection.

Away from a run, the browser keeps the same `/api/v1/events` connection without
`run_id`. `catalog.revision` causes one catalog refetch. This is the catalog
freshness notification path; no catalog polling or second SSE connection exists.

## 11. Recovery

The controller computes one bundle digest over executable/runtime identity,
locked dependencies, schemas, reducer, and recovery code before it mutates the
store.

`RunProjection.recovery_bundle_match` is `exact_match | mismatch`; there is no
looser compatibility value. On startup, for each nonterminal run:

1. acquire the store writer lock and run lock;
2. compare current and admitted controller bundle digests;
3. on mismatch, mutate nothing, signal nothing, block new admission, and expose
   “Recovery blocked — controller bundle changed” with both digests;
4. on exact match, append `recovery.started` with a stable recovery ID and a
   deterministic list of scoped actions before any side effect;
5. bracket each action with started/finished events and an idempotency key;
6. signal only a process whose persisted PID and process-start identity still
   match; otherwise record manual intervention and do not signal;
7. append one controller-restart failure if absent, finish reachable entities,
   mark unreachable declarations not-run, perform scoped cleanup, quarantine on
   uncertainty, and terminalize the run as error.

If recovery crashes, the next exact-bundle controller folds the same journal,
reconciles an action with a started event but no finished event, and performs
only missing idempotent actions. There is no separate recovery-session registry
or projection. Recovery history survives in `run.json` after purge.

## 12. Evidence, redaction, and retention

### 12.1 V1 evidence contract

V1 collects:

- structured operation results and bounded stdout/stderr;
- lifecycle, validation, surface, cleanup, and timing records;
- artifacts explicitly attached by a test or adapter;
- optional low-rate resource summaries when a provider is available.

Evidence roles are `supporting | validation_bound`. Evidence availability is
`available | partial | unavailable | unsupported | invalid`. Aggregate evidence
health is `complete | degraded | unavailable | invalid`.

There is no generalized channel scheduler or high-rate burst profile in v1.
When a validation depends on evidence, the declaration freezes the minimum
availability/coverage and unsupported behavior. A post-admission loss of
required validation evidence is an error. Missing supporting evidence only
degrades evidence health.

All logs, event JSON, artifacts, and SSE payloads have manifest-frozen byte/count
caps. Caps produce explicit truncation and omitted counts; the system never
fills missing samples with zero.

### 12.2 Secret handling

Known secrets are registered before transport startup. Redaction happens before
persistence and again at storage/SSE sinks. It covers plain, JSON-escaped,
URL-encoded, shell-quoted, and standard/URL-safe base64 forms across chunk
boundaries. Unknown or unscannable binary/archive artifacts are rejected rather
than served.

Artifacts are retrieved only through a run-scoped opaque ID mapped in `run.json`.
Unknown and cross-run IDs return the same 404. Purged evidence returns 410.
Corrupt mapped evidence returns 500 and no bytes. HTML/SVG/script content is
download-only with `nosniff`, `no-store`, and sandboxed content policy.

### 12.3 Explicit purge

There is no automatic evidence eviction. Terminal run purge accepts a semantic
run ID, never a path. It may remove source snapshot payload, logs, artifacts,
and workspace payloads. It retains the manifest, event journal, terminal
`run.json`, and workspace lineage/tombstones. Each deletion is contained,
allowlisted, journaled in `events.jsonl`, and retryable. Active or recovering
runs cannot be purged.

## 13. Workspaces and filesystem tree

V1 always creates a fresh attempt from one verified template. It does not reuse
a retained attempt. Failed, cancelled, errored, or cleanup-uncertain attempts are
quarantined.

The smallest source tree is:

```text
<TEST_REPOSITORY_ROOT>/
├── README.md
├── pyproject.toml
├── package.json                 # only if the web build needs it
├── package-lock.json
├── e2e/
│   ├── metadata/catalog.yaml
│   ├── harness/                 # declaration, collection, runner, adapters
│   ├── tests/
│   │   ├── product/             # single-subject product behavior
│   │   ├── compound/            # cross-domain shared-context scenarios
│   │   └── harness/             # infrastructure/control-plane diagnostics
│   ├── web/                     # generic Control Room
│   └── offline_tests/           # collector/reducer/API/UI contract tests
└── benchmark/                   # optional non-product benchmark config
```

`tests/` may contain domain/family folders for contributor navigation. Paths do
not own taxonomy or identity. There are no `core`, `common`, `shared`, `utils`,
`schemas`, and `control` top-level buckets. Split a harness module only when it
has two real consumers or is independently testable.

The smallest mutable tree is:

```text
<WORKSPACE_STORE_ROOT>/
├── e2e/
│   ├── root.json
│   ├── TEST-REPORT.md           # append-only delivery proof; not run truth
│   ├── catalog/{current.json,health.json}
│   ├── runs/<run-id>/
│   │   ├── manifest.json
│   │   ├── events.jsonl
│   │   ├── run.json
│   │   ├── source/
│   │   └── evidence/
│   ├── workspaces/{template,attempts,quarantine}/
│   ├── tmp/
│   └── tooling/
└── benchmark/
    ├── root.json
    └── {fixtures,runs,results,runtime,tmp}/
```

The E2E root has five direct role directories: `catalog`, `runs`, `workspaces`,
`tmp`, and `tooling`. `TEST-REPORT.md` is an append-only implementation/live-proof
ledger required by the delivery process; it is never a run, catalog, API, or UI
authority. History listing scans the small `run.json` file in each run directory
and paginates deterministically. A disposable index may be introduced only after
a benchmark shows p95 listing above 500 ms at the supported retained run count;
it must remain rebuildable and non-authoritative.

Disk admission requires estimated run bytes plus at least 1 GiB finalization
reserve. At the reserve threshold the controller stops scheduling, completes
active cleanup/finalization, marks queued cases not-run due storage exhaustion,
and ends error. It never silently deletes history.

## 14. API and round-trip budget

All resources are under `/api/v1`, carry a schema version, and return typed
errors. The v1 surface is:

```text
GET  /health
GET  /catalog
GET  /events
POST /previews
POST /runs
GET  /runs
GET  /runs/:run_id
POST /runs/:run_id/cancel
POST /runs/:run_id/purge
GET  /runs/:run_id/evidence/:evidence_id
GET  /workspaces
POST /workspaces/:workspace_id/purge
```

Catalog detail is returned by the same `GET /catalog` query using an exact
identity filter. Feature views are catalog queries, not endpoints. Run case,
validation, cleanup, and evidence summaries are fields of `GET /runs/:run_id`;
large evidence payloads are fetched on demand.

The primary budget is:

| Journey | Budget |
| --- | --- |
| Browse catalog | 1 request per query/page; no taxonomy/feature/validation N+1 |
| Open exact test detail | at most 1 catalog request; 0 when present in the current page |
| Review selection | 1 preview request |
| Start | 1 admission request |
| Live run | 1 snapshot plus 1 SSE connection |
| Open log/artifact | 1 on-demand evidence request |
| Catalog refresh | 1 revision notification plus 1 catalog refetch |

Pagination defaults to 50 and caps at 100 for catalog/history. Event replay caps
each response at 1,000 events. The 1,000-case run limit bounds preview and run
projection payloads.

The loopback API validates Host on every request. Mutations require exact Origin
and a memory-only per-controller nonce. Mutations are never automatically
retried. The server accepts no cross-origin CORS permission.

## 15. Acceptance criteria

### 15.1 Catalog and extension

1. Two unchanged collections produce identical semantic catalog bytes.
2. Duplicate case ID, unknown feature, and unmapped required validation are all
   reported together; the last-good catalog remains and admission is blocked.
3. Collection from an unrelated CWD starts no gateway/Docker resource and leaves
   both repositories byte-identical.
4. A new family, group, feature, validation, and fifth domain flow through
   collection, query, preview, run fixtures, and UI with no frontend/API change.
5. Moving source and reordering parameters preserve `(test_id, case_id)`.

### 15.2 Admission and execution

6. Three mixed cases require one preview and one admission request and freeze the
   same ordered identities.
7. Stale preview, active-run conflict, empty selection, excessive selection,
   insufficient disk, and arbitrary input are typed non-mutating failures.
8. Same idempotency key and digest creates one run; mismatched reuse returns 409.
9. Editing live source after admission cannot affect the run snapshot.
10. All six surfaces prove their actual boundary; missing or mismatched proof
    cannot pass; console-down blocks only console surfaces.

### 15.3 Verdict, failure, and cleanup

11. Five-case fail-fast yields one passed, one failed/error, three causal
    not-run, completed mandatory cleanup, and stable first/primary failures.
12. Assertion followed by teardown failure keeps assertion first and teardown
    primary; terminal severity is error.
13. Failure of the first and third cleanup action still attempts every action,
    records both failures, quarantines the attempt, and prevents pass.
14. Missing required validation never becomes an inferred pass.
15. Cancellation always reaches a terminal state and records every escalation.

### 15.4 Replay, recovery, and history

16. Every valid event prefix folds deterministically; duplicate SSE delivery
    does not duplicate counts or announcements.
17. Gapped, corrupt, truncated, or incompatible journals fail visibly and never
    produce guessed state.
18. Exact-bundle restart performs scoped, idempotent recovery and terminalizes;
    a mismatched bundle mutates and signals nothing and blocks admission.
19. Crash at every recovery action boundary performs each external action at
    most once or records manual intervention.
20. History renders from frozen manifest/projection data without current catalog
    joins; directory-scan listing stays below the 500 ms p95 index threshold at
    the supported retained-run fixture.

### 15.5 Evidence, security, and retention

21. Supporting evidence loss yields passed with degraded evidence; a required
    validation-bound loss yields error.
22. Truncation exposes caps and omitted counts; missing values are never shown as
    zero.
23. Plain and encoded token canaries never appear in durable files, SSE, API, or
    UI fixtures.
24. Cross-run, traversal, purged, and corrupt evidence requests return the exact
    safe 404/410/500 behaviors without leaking bytes.
25. Purge retains manifest, terminal truth, lineage, and deletion provenance;
    it cannot target roots, markers, role directories, source, active work, or
    an arbitrary path.

### 15.6 UI and accessibility

26. A first-time user completes feature search, mixed selection, review, Start,
    first-failure inspection, cleanup review, and retry without pytest knowledge.
27. Loading, empty, stale, blocked, disconnected, recovering, recovery-blocked,
    incompatible, degraded, purged, and failed states use the exact message and
    action matrix in the UI design.
28. Keyboard-only operation and 200% zoom work at all five viewports with no
    page-level horizontal overflow, hidden status, or pointer target below 44 px.
29. First failure is announced once; event/log/timer updates do not flood the
    live region or steal focus.
30. Fixture/demo routes are persistently labeled “Demo data — no runner
    connected” and expose no real Start/Cancel claim.

## 16. Proof status

This document is internally ready for implementation, but the system is not.
The current proof status is:

- **implemented today:** pytest suite, product catalogs, product CLIs, gateway,
  console routes, daemon HTTP, direct daemon helper, benchmark store machinery;
- **visual only:** static E2E UI prototype;
- **specified only:** external test repository, collector, combined catalog,
  controller, journal/reducer, source snapshot, Control Room API/UI, recovery,
  run retention model;
- **not run in this review:** live Docker tests, browser automation, builds, or
  cleanup commands.

Implementation must follow the gates in the delivery plan. A later optimization
may add complexity only with a measurement, a named owner, a deletion plan, and
cross-document reconciliation.
