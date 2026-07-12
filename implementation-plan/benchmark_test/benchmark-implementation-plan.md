# EphemeralOS Benchmark Laboratory — Implementation Plan

| Field | Value |
|---|---|
| Status | Draft — all phases not started |
| Date | 2026-07-12 |
| Product root | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/benchmark` |
| Primary contracts | [System specification](benchmark-system-spec.md), [backend design](benchmark-backend-design.md), [UI design](benchmark-ui-design.md) |
| Delivery rule | A phase may start only after its predecessor is accepted. Phase 6 is the release gate. |

## 1. Goal and operating rules

Deliver the local Benchmark Laboratory as a separate trusted loopback service
with a same-origin React/Mantine UI. The release covers the four benchmark
families and seven operations specified in the coordinated contract:

| Family | Operations |
|---|---|
| Command | `exec_command` |
| File Operations | `file_read`, `file_write`, `file_edit`, `file_blame` |
| Workspace Lifecycle | `create_workspace` |
| LayerStack | `squash_layerstack` |

The following rules apply to every phase:

1. Keep the runner a modular monolith with closed, exhaustively registered Rust
   operation definitions. Do not introduce runtime plugins, a browser-side
   executor, generic workflow engine, database, or internal-RPC proxy.
2. Treat the versioned `ExperimentPlan`, validated `ExpandedPlan`, immutable
   observations, and stored definition snapshot as the respective authorities.
   The browser renders backend-derived estimates, reports, and compatibility;
   it does not calculate competing scientific results.
3. Preserve the distinct meanings of test combinations, trial batches, and
   issued product requests throughout validation, UI, progress, artifacts, and
   reports.
4. Implement each capability with unit and fake-adapter integration coverage as
   it is added. Do not defer all tests to the final phase.
5. A phase is complete only when its acceptance evidence is linked in the
   tracker and all scoped checks pass. “Implemented” without evidence is not
   complete.

### Declared source and test layout

The backend package and binary stay named `sandbox-benchmark`, but its Cargo
workspace member path is `ephemeral-sandbox/benchmark/backend/`.

```text
ephemeral-sandbox/
  benchmark/
    README.md
    defaults/                 # Versioned Default configuration data
    presets/                  # Strict, data-only versioned plans
    web/
      src/
        api/                  # Typed API client, query hooks, SSE hook
        components/           # Shared presentation/interaction regions
        pages/                # Explicit Overview, family, run, report, compare pages
        plots/                # Accessible backend-authored plot renderers
        lib/                  # Formatting and UI-only helpers
        routes.tsx
        theme.ts
      tests/
        fixtures/             # Stable typed API/report/definition fixtures
        unit/                 # Route, component, and UI contract tests
        browser/
          fixture/            # Screenshot and accessibility tests using fixtures
          real-backend/       # Production UI → real runner → Docker gate
    backend/
      Cargo.toml
      src/
        executors/
          mod.rs
          command.rs
          files.rs
          workspace.rs
          layerstack.rs
        main.rs
        api.rs
        app.rs
        config.rs
        model.rs
        definitions.rs
        plan.rs
        scheduler.rs
        events.rs
        artifacts.rs
        fixtures.rs
        resources.rs
        checks.rs
        statistics.rs
        report.rs
        compare.rs
        cleanup.rs
        gateway.rs
        daemon_session.rs
      tests/
        fixtures/{plans,artifacts,definitions}/
        contract/
        integration/
        live_docker/
        security/
```

Runtime artifacts are intentionally not stored in the repository. They remain
under `<test-workspace-root>/benchmark/{fixtures,runs,results,runtime}`. The
`real-backend` browser tests and `live_docker` runner tests are the only suites
that may satisfy the final release gate; they must run release-built assets
against the real loopback runner, isolated gateway, and Docker backend without
mocked requests, fake adapters, or DOM-state injection.

## 2. Progress tracker

Status values: `Not started` → `In progress` → `Blocked` or `Accepted`.
`Accepted` means the listed acceptance criteria passed and evidence is recorded.

| Phase | Status | Scope | Entry condition | Exit evidence | Progress |
|---|---|---|---|---|---|
| 0. Contract and skeleton | Not started | Crate/app skeleton, schemas, safety boundary, test harness | None | Build, typecheck, schema and security test output | 0% |
| 1. Command vertical slice | Not started | One real command study from default plan to report | Phase 0 accepted | Command run artifact and report regeneration output | 0% |
| 2. File Operations | Not started | Read/write/edit/blame and File UI | Phase 1 accepted | Per-operation traceable run artifacts and tests | 0% |
| 3. Workspace Lifecycle | Not started | Narrow session adapter and matrix study | Phase 2 accepted | Adapter-closure and create/teardown evidence | 0% |
| 4. LayerStack | Not started | Squash/remount topology and phase evidence | Phase 3 accepted | `N=0`/`N>0` results with reconciled dispositions | 0% |
| 5. Reports, compare, and hardening | Not started | All report surfaces, compare, recovery, accessibility and security | Phase 4 accepted | Release-candidate test bundle and artifact fixtures | 0% |
| 6. Final real UI + real backend proof | Not started | Non-mocked end-to-end release verification | Phase 5 accepted | Signed test report with browser, runner, gateway, Docker, and artifact evidence | 0% |

## 3. Phase 0 — Contract, safety boundary, and skeleton

### Scope

- Create the `sandbox-benchmark` Rust crate and `benchmark/web` application;
  integrate them with the workspace build and the established console React /
  Mantine conventions.
- Create the declared source/test directories and keep unit/fixture coverage
  distinct from the non-mocked `live_docker` and browser `real-backend` suites.
- Define versioned plan, expanded-plan, manifest, observation, definition,
  report, comparison, error, and SSE DTO schemas.
- Implement the closed `FamilyId` / `OperationId` model, compile-time
  definitions, typed operation-plan/cell/evidence variants, and exhaustive
  dispatch seams. Definitions must include access choice, isolation policy,
  semantic/factor revisions, count semantics, checks, phases, and comparison
  projection.
- Implement runner startup/readiness, machine-local workspace-root resolution,
  ownership markers, safe-delete guards, artifact layout, JSON API envelope,
  nonce/origin/host validation, and one-active-campaign admission control.
- Add the benchmark test scaffolding: Rust unit/integration targets, TypeScript
  route/component test setup, contract fixtures, and browser-test project.

### Acceptance criteria

- `sandbox-benchmark serve` binds only to loopback, reports execution readiness
  separately from report-browsing availability, and never commits a user-local
  absolute workspace root.
- `/api/v1/health`, `/settings`, `/definitions`, `/plans/validate`, and the run
  admission endpoints follow the documented versioned DTO/error contract.
- A supplied complete Default command plan validates to a canonical plan,
  stable hash, expanded cells, and all three distinct work counts.
- Every production operation identifier has exactly one definition, access
  choice, typed dispatch arm, semantic revision, and comparison projection;
  missing or duplicate registration fails automated tests.
- Plans cannot carry credentials, gateway mode, cleanup policy, allowlists, or
  safety-cap overrides. Invalid origin/host/nonce, unknown fields, unsupported
  future schema, path escape, symlink escape, and unknown artifact IDs are
  rejected.
- Artifact writes and ownership-ledger deletion guards have deterministic unit
  coverage, including a sentinel outside the benchmark root that remains
  untouched.
- Rust format/lint/build, web typecheck/lint, schema contract tests, and the
  scoped security tests pass.

### Progress checklist

- [ ] Crate, web app, workspace commands, and CI test targets exist.
- [ ] Versioned schemas and checked TypeScript bindings exist.
- [ ] Root discovery, marker, ownership ledger, and safe deletion are tested.
- [ ] Definition registration and plan validation are exhaustively tested.
- [ ] Loopback API security and error-envelope tests pass.
- [ ] Phase evidence is linked in the tracker and Phase 0 is marked `Accepted`.

## 4. Phase 1 — Command vertical slice

### Scope

- Implement the common scheduler, static lifecycle driver, barriers, timeout /
  cancellation ledger, event persistence/replay, fixture manager, resource
  collection, correctness folding, immutable observations, statistics, and
  report regeneration.
- Implement the Small fixture and one allowlisted `exec_command` direct-client
  case at concurrency `1`, `5`, and `20`; generate the exact bounded shell
  `cmd` on the backend.
- Implement the first real pages: Overview, Command, plan review, live run,
  and report. Include Default → Customize → Reset behavior and matching-hash
  submission.
- Record latency, runner/daemon/sandbox memory, logical/allocated disk,
  correctness, and available/unavailable resource states with explicit units
  and scopes.

### Acceptance criteria

- A browser user can open the server-authored Default command plan, review its
  exact allowed command and three work counts, submit its matching hash, follow
  the run through SSE, and open the resulting report after reload.
- Concurrent command requests share the common barrier; warmups are excluded
  from summaries; failed correctness results remain visible and are excluded
  from successful-latency distributions.
- Raw observations, events, expanded plan, manifest, and definition snapshot
  persist under the owned result directory. Regenerating the report from those
  artifacts produces deterministic golden output without a product client.
- Cancel, timeout, reconnect/replay, and partial-failure paths write a valid
  terminal manifest, retain evidence, and invoke owned cleanup without touching
  an outside-root sentinel.
- Command text, shell metacharacters, and argv-shaped input cannot be supplied
  by the plan or UI; only registered case IDs and bounded typed parameters are
  accepted.
- Unit, fake-adapter integration, API contract, and Command route/browser
  fixture tests pass.

### Progress checklist

- [ ] Scheduler, lifecycle driver, event ledger, and cancellation are covered.
- [ ] Command fixture, adapter, correctness check, and collectors are covered.
- [ ] Overview/Command/review/run/report pages use only typed API data.
- [ ] Artifact regeneration and correctness-exclusion goldens pass.
- [ ] Default/reset/hash/SSE/reconnect UI tests pass.
- [ ] One real command run is archived as Phase 1 evidence; phase is `Accepted`.

## 5. Phase 2 — File Operations

### Scope

- Add typed lifecycle modules and factor controls for `file_read`, `file_write`,
  `file_edit`, and `file_blame`.
- Add deterministic payload and metadata-heavy fixtures, fixture manifests and
  content hashes, fresh-state policies, and operation-specific correctness /
  attribution evidence.
- Implement the File Operations family page using the designed master-detail
  editor on desktop and accessible operation accordions on narrow screens.
- Extend generic report data with file-operation distributions, raw evidence,
  and family selection while retaining the common scheduler/report pipeline.

### Acceptance criteria

- Each file operation validates and runs independently and as an enabled part
  of the Files family; its count semantics and isolation policy are displayed
  accurately.
- Read uses the intended published/live boundary; write and edit preserve their
  sessionless versus explicit-session publication rules; blame reports
  EphemeralOS ownership rather than Git blame.
- Fresh-state, independent, and contention execution paths create no cross-cell
  mutation contamination. Attribution and content checks link each report row
  to raw operation evidence and its deterministic fixture hash.
- The File page has no arbitrary file-operation or generic-factor escape hatch;
  operation controls remain exhaustive and typed.
- File route tests cover default, customized, invalid, publish-warning, reset,
  keyboard, and responsive states. Per-operation unit/integration tests and
  artifact/report goldens pass.

### Progress checklist

- [ ] Four typed lifecycle modules and their check/evidence variants are done.
- [ ] Deterministic fixtures and fresh-state policies are tested.
- [ ] File page and typed operation-control switch are implemented/tested.
- [ ] Report/raw-artifact traceability passes for all four operations.
- [ ] File family accepts a representative run and has archived evidence.
- [ ] Phase evidence is linked and Phase 2 is `Accepted`.

## 6. Phase 3 — Workspace Lifecycle

### Scope

- Add the narrow, typed `create_workspace_session` adapter and its paired
  runner-owned destroy/teardown path. No general browser-facing internal RPC is
  added.
- Materialize deterministic Small, Medium, and Large workspace profiles;
  capture actual fixture totals and free-space estimates.
- Implement concurrent-create barrier semantics, registry-baseline verification,
  cleanup invalidation, and the profile × count matrix report.
- Implement the Workspace Lifecycle page, including Large-space warning and
  mobile matrix representation.

### Acceptance criteria

- The adapter exposes only typed create/destroy actions for runner-owned
  identities. An unregistered internal action fails before any credential lookup
  or socket/network operation, proven with spies.
- A concurrent creation cell issues exactly the documented number of independent
  product requests, all released from the shared barrier; it does not relabel a
  product-internal sequential loop as concurrency.
- Small/Medium/Large profiles are deterministically materialized, actual totals
  match manifests, and insufficient disk is blocked before a run starts.
- Registry, cgroup, and scratch cleanup return to the captured baseline. Any
  residue invalidates the trial, aborts the campaign, retains evidence, and
  leaves paths outside the owned root unchanged.
- The size × count UI and report display requested cost, result counts, and
  cleanup outcome with correct units and accessible small-screen layout.
- Adapter-closure, barrier, fixture, cleanup, matrix route, and report tests
  pass.

### Progress checklist

- [ ] Allowlisted adapter and zero-call rejection tests exist.
- [ ] Profile generation, space estimation, and baseline cleanup are tested.
- [ ] Concurrent-create measurement and verification evidence is persisted.
- [ ] Matrix page/report pass desktop and mobile fixture tests.
- [ ] Representative count `1` and `5` runs are archived.
- [ ] Phase evidence is linked and Phase 3 is `Accepted`.

## 7. Phase 4 — LayerStack

### Scope

- Add isolated gateway configuration management and the `squash_layerstack`
  lifecycle with deterministic layer/session topology.
- Implement exactly-one-squash-per-trial semantics; `N` represents prepared
  live-session load, not request concurrency. Support `N=0`, `1`, `5`, and
  `20`, including configured restart blocks `W`.
- Record storage/build/commit and remount-sweep phases, the S0–S3 resource
  samples, observed `M`, `I`, `W`, `B`, and every remount disposition.
- Implement the LayerStack topology/causal-group page, live phase progress, and
  report sections that keep storage cost and remount cost separate.

### Acceptance criteria

- With `N=20`, instrumentation proves twenty live sessions are prepared and
  exactly one squash product request is issued. `N=0` is accepted and shown as
  the squash-only control.
- Storage-phase timings are never merged with remount-sweep timings. Phase
  samples, disposition counts, `M`/`I`/`W`/`B`, and S0–S3 resource boundaries
  round-trip from raw observations to report/export.
- The sum of remount dispositions reconciles with the observed session set;
  unexpected residue or unreconciled counts makes the trial ineligible and
  preserves diagnostic evidence.
- Gateway runtime credentials/configuration remain owner-only, live only under
  the active runtime directory, and are never included in results, browser
  responses, exports, or logs.
- LayerStack route, phase-correlation, topology, resource, correctness, and
  report tests pass, including `N=0` and `N=1` representative runs.

### Progress checklist

- [ ] Isolated gateway lifecycle and redaction controls are tested.
- [ ] One-request / `N`-load topology is asserted with spies.
- [ ] Phase and disposition raw schemas/report projections are golden-tested.
- [ ] LayerStack page supports control and restart-block states responsively.
- [ ] `N=0` and nonzero real run evidence is archived.
- [ ] Phase evidence is linked and Phase 4 is `Accepted`.

## 8. Phase 5 — Reports, comparison, and release hardening

### Scope

- Complete the five-destination scientific report, raw/artifact index and
  bounded exports, CSV/export policy, and compatibility-first comparison.
- Add all versioned defaults/presets, old-artifact readers and regeneration
  fixtures, recovery/reconciliation, and Release Comparison protocol support.
- Complete every remaining route shape, responsive behavior, keyboard/focus
  behavior, screen-reader announcements, reduced motion, chart/table
  equivalence, empty/loading/error states, and deterministic screenshot suite.
- Complete security, durability, extension-acceptance, performance-cap, and
  release documentation checks.

### Acceptance criteria

- All eight route shapes render their documented default, configured, running,
  error, historical, and comparison states at 375, 768, 1,024, and 1,440 px;
  charts expose equivalent accessible tables and never use color as the only
  status signal.
- Compare checks typed compatibility before showing deltas. Semantic, cohort,
  metric-availability, or treatment mismatches produce explicit reasons; a
  descriptive override cannot claim an aggregate or regression verdict.
- Stored artifacts from every supported schema version regenerate the same
  current report without rewriting raw evidence or loading an executor/product
  client. Unknown future schemas fail explicitly.
- Cancellation, restart reconciliation, browser reconnect, event replay, slow
  event consumers, unavailable CPU/I/O, partial correctness failure, and
  cleanup residue are truthful and evidence-preserving.
- All extension acceptance tests in system-spec section 17 pass: data-only
  preset/profile additions, fake lifecycle reuse, metric independence,
  operation-scoped phases, closed internal access, and semantic comparison.
- Full unit, integration-with-fakes, contract/security, accessibility, visual,
  and performance-cap suites pass with clean browser console sentinels.

### Progress checklist

- [ ] All defaults/presets and historical artifact fixtures are checked in.
- [ ] Report/export/compare DTOs and UI bind to stored definition snapshots.
- [ ] Eight route shapes pass responsive, accessibility, and visual coverage.
- [ ] Recovery, security, comparison, and extension gates pass.
- [ ] Release-candidate test outputs and known limitations are recorded.
- [ ] Phase evidence is linked and Phase 5 is `Accepted`.

## 9. Phase 6 — Final proof against the real UI and real backend

This is deliberately a separate release gate. It must exercise the compiled
benchmark UI and the real `sandbox-benchmark` process over their actual
same-origin loopback HTTP/SSE connection, through the isolated gateway and real
Docker-backed EphemeralOS backend. API fixtures, mocked `fetch`, fake operation
adapters, fake clocks, DOM-state injection, static screenshots, and direct
artifact fabrication are forbidden for the acceptance flows below. They remain
valuable earlier in the plan, but cannot satisfy this phase.

### Scope

- Build production web assets and start `sandbox-benchmark serve` with a fresh,
  writable, dedicated test workspace root and real Docker prerequisites.
- Drive the product with a browser automation suite using normal user actions
  only: navigate, inspect readiness, review, submit, observe live SSE progress,
  cancel where required, reload, and inspect reports/compare.
- Run one bounded Quick Smoke campaign per family against the real isolated
  gateway: Command at concurrency `1` and `5`; one File read and one
  explicit-session mutation; Workspace creation at counts `1` and `5`; and
  LayerStack at `N=0` and `N=1`.
- Run a real active-trial cancellation flow and verify real cleanup/evidence;
  run a real cross-run comparison flow using two persisted completed runs.
- Retain sanitized test artifacts, browser trace/video/screenshots where
  configured, runner logs, Docker/gateway readiness data, manifests,
  observations, reports, and the generated test report as release evidence.

### Acceptance criteria

- The browser reaches the built, production-served UI from the runner’s actual
  loopback URL; every required API call and SSE stream succeeds against the
  real runner. Tests fail if a request is intercepted, mock service worker is
  active, a fake adapter is selected, or a required browser console error,
  uncaught page error, React-key warning, or network failure occurs.
- Each family’s bounded real run completes with a terminal manifest, immutable
  observations, definition snapshot, and report produced by the real backend.
  The artifacts prove the documented request/count semantics, including one
  LayerStack squash per trial and `N=0` as a control.
- The real run page displays setup/operation/completion progress from persisted
  SSE events; a browser reload reconnects with `Last-Event-ID` and does not
  alter the run’s persisted state.
- The real cancellation flow stops future trials, terminates owned work,
  attempts cleanup, retains partial evidence, and produces a valid cancelled
  manifest. The outside-root sentinel and unrelated Docker resources remain
  unchanged.
- The real LayerStack run reports storage and remount evidence separately, with
  observed disposition counts that reconcile. The real Workspace run restores
  registry/cgroup/scratch baseline or fails transparently with retained
  diagnostics.
- Two real persisted reports can be selected in the UI and compared. The UI
  shows the backend compatibility decision before deltas and does not invent
  local statistics.
- The final report includes exact commands and versions, test-workspace path
  redacted as appropriate, source commit/dirty state, Docker/image identity,
  browser/version, test timestamps, run IDs, artifact hashes, screenshots at
  the four supported breakpoints, and links to all retained evidence. No secret
  is present in any captured output.

### Progress checklist

- [ ] Fresh dedicated workspace root and real Docker readiness are verified.
- [ ] Production assets and real loopback runner are started by the test harness.
- [ ] Browser tests prove no mocks/intercepts/fake adapters are used.
- [ ] Command, Files, Workspace, and LayerStack Quick Smoke flows pass.
- [ ] Real SSE reload/replay, cancellation/cleanup, and comparison flows pass.
- [ ] Artifacts, traces, screenshots, logs, and sanitized report are retained.
- [ ] Release owner reviews evidence and marks Phase 6 `Accepted`.

## 10. Release decision

Release is permitted only when every tracker row is `Accepted`, the Phase 6
report is complete, and no critical correctness, isolation, cleanup, security,
or data-integrity issue remains open. A skipped real-backend or real-browser
flow is a release blocker, not a waiver.
