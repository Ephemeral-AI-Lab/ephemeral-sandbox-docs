# EphemeralOS Live E2E Control Room — Web UI Design

| Field | Value |
|---|---|
| Status | Proposed v1 UI source of truth; ready for adversarial review |
| Date | 2026-07-12 |
| V1 viewport scope | Complete workflows at 375, 390, 768, 1024, and 1440 CSS pixels, plus 200% zoom |
| Configured test repository root (`TEST_REPOSITORY_ROOT`) | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test |
| Derived E2E source root (`E2E_SOURCE_ROOT`) | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e |
| Derived benchmark source/config root (`BENCHMARK_SOURCE_ROOT`) | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark |
| Product UI target | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/web |
| Configured product repository root (`PRODUCT_ROOT`) | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox |
| Existing reviewed prototype | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/e2e/ui-prototype |
| Configured mutable workspace store (`WORKSPACE_STORE_ROOT`) | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test-workspace |
| Derived E2E workspace root (`E2E_WORKSPACE_ROOT`) | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test-workspace/e2e |
| Derived benchmark workspace root (`BENCHMARK_WORKSPACE_ROOT`) | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test-workspace/benchmark |
| System specification | [e2e-test-system-spec.md](e2e-test-system-spec.md) |
| Technical design | [e2e-test-design.md](e2e-test-design.md) |
| Delivery plan | [e2e-test-implementation-plan.md](e2e-test-implementation-plan.md) |

This document is the visual and interaction source of truth for the production
web UI. It specifies information architecture, responsive page composition,
interaction states, content hierarchy, and UI acceptance tests. V1 designs,
implements, and release-gates the complete task flow at 375, 390, 768, 1024,
and 1440 CSS pixels and separately at 200% browser zoom.

The system specification remains authoritative for product behavior and data
meaning. The technical design remains authoritative for controller, storage,
schema, event, and reducer implementation. If older UI prose or the static
prototype conflicts with this document, this document governs page composition
and the system specification governs behavior.

`TEST_REPOSITORY_ROOT`, `PRODUCT_ROOT`, and `WORKSPACE_STORE_ROOT` are the only
configurable filesystem roots. The server derives `E2E_SOURCE_ROOT`,
`BENCHMARK_SOURCE_ROOT`,
`E2E_WORKSPACE_ROOT`, and `BENCHMARK_WORKSPACE_ROOT` as the fixed children shown
above. `e2e/` and `benchmark/` are Git-controlled, read-only runtime inputs.
The external store's `e2e` and `benchmark` leaves are mutable roots whose
destructive operations require ownership markers. The controller returns all
resolved roots for display. The browser cannot supply, browse for, derive, or
override a root path.

The existing prototype is a visual reference only. It is not evidence that the
production UI, controller, workspace roots, or live execution flow exists.

## 1. UI outcome

The Control Room should let a first-time user complete this workflow without
knowing pytest paths, node IDs, markers, or command-line arguments:

~~~mermaid
flowchart LR
    A["Find tests by domain, family, feature, purpose, or validation"] -->
    B["Read the case contract and feature-to-validation claims"] -->
    C["Build a mixed selection"] -->
    D["Review the exact server-expanded run"] -->
    E["Start one admitted run"] -->
    F["Follow in-flight cases, validations, cleanup, and evidence"] -->
    G["Open the first failure and synchronized evidence"] -->
    H["Retry failed or not-run cases through a new preview"]
~~~

The UI succeeds when users can answer three questions quickly:

1. **Before a run:** What will be tested, which features and validations prove
   it, and what resources and workspace will be used?
2. **During a run:** What is happening now, what has passed or failed, what is
   still cleaning up, and is the displayed state live?
3. **After a run:** What caused the result, which validations support it, what
   telemetry and logs exist, and what should be retried?

### 1.1 Design principles

1. **One generic catalog.** Runtime, Manager, Observability, Compound, and any
   future domains are data-driven filters and headings, not separate page
   implementations.
2. **Feature-first discovery is equal to taxonomy discovery.** A user can start
   from a feature ID, label, or description and see its cases and mapped
   validations.
3. **No direct execution from a catalog row.** Selection leads to Review run;
   only a ready preview can lead to Start run.
4. **Purpose before evidence.** Declared purpose and validations appear before
   history or logs.
5. **First failure before raw logs.** The causal failure, its validation, phase,
   time, and evidence interval are pinned ahead of diagnostic output.
6. **Product verdict and evidence health are separate.** A Runtime or Manager
   test can pass while supporting telemetry is degraded.
7. **Unknown is never success.** Missing, stale, unsupported, incompatible,
   partial, and zero are visually and semantically distinct.
8. **Live and history use the same result components.** Completed runs are a
   frozen projection, not a different interpretation.
9. **Critical state never disappears.** At every required width and at
   200% zoom, run state, stream freshness, first failure, cleanup, evidence
   health, and the active action remain visible.
10. **The browser does not invent truth.** Exact expansion, verdicts, counts,
    eligibility, safety, and evidence availability come from server projections.

## 2. Information architecture

### 2.1 Global navigation

The only primary destinations are:

- **Catalog**
- **Runs**
- **Workspaces**

**Runner Health** is a persistent labeled control that opens a drawer. An active
run indicator is also persistent and links to that run.

Runtime, Manager, Observability, Compound, family, group, scenario, complexity,
and feature links all resolve to the generic Catalog route with URL-backed
filters. They never create a new page implementation.

### 2.2 Route map

| Route | Page | Primary task |
|---|---|---|
| /e2e and /e2e/catalog | Catalog | Search, filter, understand, and select cases |
| /e2e/catalog?domain_id=... | Catalog filtered state | Browse any current or future taxonomy node |
| /e2e/catalog?catalog_kind=harness&runnable=true | Runnable Harness-filtered Catalog | Review and select runnable runner diagnostics through normal admission |
| /e2e/features/:featureId | Feature-filtered Catalog | Understand feature coverage claims and select mapped cases |
| /e2e/tests/:testId/cases/:caseId | Test detail | Read one expanded case contract and history |
| /e2e/runs | Runs | Find live and completed runs |
| /e2e/runs/:runId | Run | Follow or review one frozen run projection |
| /e2e/workspaces | Workspaces | Inspect the derived E2E workspace root, its seven direct children, readiness, retention, and eligible marker-owned leaves |

Route segments for test, case, feature, and run IDs are independently URL
encoded and decoded. The UI preserves test_id and case_id as separate fields;
it does not depend on a derived case UID.

Canonical historical deep links use:

~~~text
/e2e/runs/:runId
  ?test_id=:testId
  &case_id=:caseId
  &attempt_id=:attemptId
  &validation_id=:validationId
  &evidence_context_ms=2000
~~~

`validation_id` is omitted only for case-level evidence. The client never puts
an originless monotonic range in the URL. The server resolves the frozen
case/validation identity and displayed context margin into one or more
origin-qualified intervals, so producer clocks are never compared across
origins. Each optional identity field progressively narrows the Run page. A
copied link remains valid against the run's frozen manifest even when the
current catalog changes.

The Runs list and a known-run route have independent availability. Opening
`/e2e/runs/:runId` reads that run's authoritative projection and MUST remain
usable while the global run-summary projection is rebuilding, stale, errored,
or incompatible. The UI never redirects a known-run deep link through the Runs
list query.

### 2.3 Page inventory

| Surface | Form | Main action |
|---|---|---|
| App shell | Persistent | Navigate, inspect active run, open Runner Health |
| Catalog | Route | Add selection clauses and Review run |
| Test detail | Route | Add/remove this case from selection |
| Feature view | Catalog state | Add all matching cases as a feature clause |
| Selection tray | Persistent drawer/tray | Inspect clauses, exclusions, and Review run |
| Run preview | Adaptive drawer/full-screen modal | Start a ready preview |
| Run | Route | Cancel live work, inspect evidence, or review a retry |
| Runs | Route | Find and open a frozen run |
| Workspaces | Route plus detail drawer | Inspect source/workspace separation, prepare or verify testbed content, review from copy, or purge an eligible marker-owned leaf |
| Runner Health | 480 px right drawer | Diagnose readiness and run recovery actions |

### 2.4 Technology stack

The production UI is a dedicated npm/Vite single-page application at
`e2e/web`. It reuses the repository's established web stack and conventions,
but remains separate from the product console because it is served by the E2E
controller and has test-runner mutation authority.

| Layer | V1 choice | Responsibility |
|---|---|---|
| Language and UI | React 19 + TypeScript 6 | Generic catalog, preview, live run, history, workspace, and health components |
| Build | Vite 8 + npm/package-lock | Local development and static production bundle; Node is not a production runtime |
| Component system | Mantine 9 + Mantine Hooks/Notifications | Theme, layout, forms, drawers, dialogs, feedback, and accessible primitives |
| Routing | React Router 7 | `/e2e/...` routes, historical deep links, and URL-owned filters |
| Server state | TanStack Query 5 | HTTP resource cache, refresh, mutation state, and snapshot refetch |
| Dense data | TanStack Table 8 + TanStack Virtual 3 | Sortable tables and bounded DOM rendering for large catalogs, runs, events, and logs |
| Live projection | Native `EventSource` + a pure React reducer | Replayable ordered SSE with duplicate/gap handling; no bidirectional socket protocol |
| Telemetry | uPlot 1.6 | CPU, memory, disk, and cgroup time series with table alternatives |
| Icons | Lucide React | Allowlisted generic icons with visible text labels |
| UI tests | Vitest + Testing Library | Reducers, query/filter state, semantics, and component interactions |
| Browser proof | Playwright + axe | Responsive workflows, reconnect, high volume, keyboard, zoom, and WCAG checks |

The Vite development server proxies `/api/v1`. Production emits static assets
served by the same loopback Python controller as `/api/v1` and replayable SSE,
keeping UI and API same-origin. Mantine theme tokens plus a small amount of
plain CSS/CSS modules own styling.

V1 deliberately adds no Next.js/SSR server, Electron/Tauri shell, Tailwind or
second component system, Redux/Zustand/XState store, GraphQL, WebSocket/Socket.IO
transport, heavyweight data grid, code editor, or shared UI package. React
Router owns shareable URL state; TanStack Query owns server snapshots; a
revision-qualified React context/reducer owns selection and live projection;
component state owns disclosure and focus. A shared package is reconsidered
only after a second production consumer creates demonstrated maintenance cost.

## 3. App shell

### 3.1 Wide composition

At 1200 pixels and wider, use a compact 224-pixel navigation rail. The route
content owns the remaining width. The shell does not contain domain links.

~~~text
┌──────────────────────┬────────────────────────────────────────────────────────────┐
│ EphemeralOS          │ Breadcrumb / page title        Active run     Health: Ready│
│ E2E Control Room     ├────────────────────────────────────────────────────────────┤
│                      │                                                            │
│ ▣ Catalog            │ Route content                                              │
│ ◷ Runs               │                                                            │
│ ◫ Workspaces         │                                                            │
│                      │                                                            │
│ Active run           │                                                            │
│ Running · 7 / 18     │                                                            │
│ Live · 2 s ago       │                                                            │
│                      │                                                            │
│ Catalog rev          │                                                            │
│ 8a4d… · current      │                                                            │
└──────────────────────┴────────────────────────────────────────────────────────────┘
~~~

The active-run block shows state, completed/total **case** count, and connection
freshness. If no run is active, it says “No active run”; it never leaves a stale
completed run looking active. If recovery compatibility is blocked, this block
instead says “Recovery blocked” and “Last persisted state · historical,” links
the run, and contains no live dot, ticking duration, or completed/total progress
claim.

### 3.2 Compact and narrow composition

At 1024–1199 pixels, replace the rail with a compact top application bar and
three labeled navigation controls. Filters and secondary inspectors may use
desktop drawers, but run state, connection freshness, selection count, and the
active action remain visible. At 768 pixels, use a single main column with
labeled filter and selection drawers; the run case list precedes its selected
detail with a sticky “Back to cases” action. At 390 and 375 pixels, use one
column and full-screen filters, selection, preview, and evidence detail. The
primary action bar, connection state, first failure, cleanup, and evidence
health remain reachable without horizontal page scrolling.

### 3.3 Persistent truth banners

Only one highest-severity global banner is expanded at a time; lower-severity
states remain available in Runner Health.

| Condition | Required copy and behavior |
|---|---|
| Demo | “Demo data — no runner connected.” Start, Cancel, safety, and live claims are disabled or clearly qualified as demonstration. |
| Recovery bundle mismatch | “Recovery blocked — controller bundle changed.” Label the persisted state historical, block all new-run admission, and link the affected Run page's identity/decision evidence plus Runner Health; Catalog/history browsing remain available. |
| Incompatible schema/event | “Updates stopped — this UI cannot interpret the runner response.” Preserve the last verified state and link diagnostics. |
| Catalog invalid, no last-good | “Catalog unavailable — collection errors must be fixed.” Do not show an empty catalog. |
| Catalog stale, last-good exists | Show revision and age; browsing/history remain available; new-run admission is disabled. |
| History rebuilding or stale, last-good exists | “Run history rebuilding/stale — showing generation {generation} from {generated_at}.” Keep the last-good rows and filters usable, disclose their age, and link Runner Health. |
| History unavailable or incompatible, no last-good | “Run history unavailable — the run-summary index cannot be served.” Show Retry, Runner Health, and Open known run; never render an empty-history result. |
| Stream stale/offline | Keep the last projection, show “as of” time and Retry; do not claim Live. |

## 4. Visual system

The visual direction reuses the existing prototype's warm neutral operational
language while tightening typography, density, accessibility, and truthful
state presentation.

### 4.1 Core tokens

| Role | Token value | Use |
|---|---|---|
| Canvas | #F5F2ED | Application background |
| Surface | #FFFDF9 | Cards, drawers, content regions |
| Raised surface | #FFFFFF | Dialogs, selected inspector |
| Subtle surface | #F9F6F1 | Group headers, secondary sections |
| Text | #241F1C | Primary copy |
| Muted text | #6C625C | Secondary metadata |
| Faint text | #837970 | Timestamps and tertiary labels; only when AA contrast is retained |
| Border | #E3DDD5 | Cards and row separators |
| Strong border | #D4CABF | Focused grouping and table headings |
| Info | #395F76 | Links, selected state, live informational state |
| Success | #23734C | Passed/ready/complete |
| Warning | #9C5A08 | Degraded/stale/warning |
| Danger | #AF3B3B | Failed/error/blocked |
| Focus | #1769AA | Focus-visible outline |

Semantic colors never encode domain identity. Optional catalog accent_token and
icon_key values are allowlisted hints; missing or unknown hints use a neutral
icon and neutral accent.

### 4.2 Typography and density

- UI text: Fira Sans, then system sans-serif.
- Technical values: Fira Code, then system monospace.
- Page title: 32 pixels; no oversized marketing hero.
- Section title: 20–22 pixels.
- Desktop body/table text: 14–16 pixels.
- IDs, paths, and event payloads wrap or scroll in their own labeled region.
- Spacing uses a 4-pixel base: 4, 8, 12, 16, 24, 32.
- Card radius: 10 pixels; dialog radius: 14 pixels.
- Hover changes border/background only; it never scales or shifts layout.

### 4.3 Status grammar

Every status combines icon or shape, visible text, and accessible text.

| State | Visual grammar |
|---|---|
| Queued / Declared | Hollow circle + “Queued” or “Declared” |
| Running / Checking / Collecting / Finalizing | Spinner or pulsing ring + visible state text |
| Passed / Ready / Complete / Available | Check circle + state text |
| Failed | X circle + “Failed” |
| Error / Invalid / Incompatible | Octagon-alert + exact state text |
| Skipped | Slash circle + “Skipped” and reason |
| Cancelled | Stop square + “Cancelled” |
| Not run | Pause circle + “Not run” and causal reason |
| Partial / Degraded / Stale | Warning triangle + exact state text |
| Unsupported / Unavailable | Minus circle + exact state text and reason |

Failure and error do not share a generic red badge: failure means a product
assertion failed; error means execution, cleanup, recorder, telemetry collector,
or infrastructure could not produce a valid result.

## 5. Page designs

### 5.1 Catalog

The Catalog is the default landing page and primary execution-entry surface. It
supports grouped outline and flat case views from the same query response.

#### Reference composition at 1440 pixels

~~~text
┌─ Test catalog ──────────────────────────────────────────────────────────────┐
│ Find cases by purpose, feature, validation, taxonomy, ID, or source        │
│ [ Search tests, features, validations, IDs…                         ] [⌘K] │
│ Catalog current · rev 8a4d… · 373 cases       [Grouped ▾] [Refresh]        │
├─ Filters 280 ─────┬─ Results, fluid ─────────────────┬─ Selection 320 ─────┤
│ Active filters 3  │ 128 matching cases              │ 3 selection clauses │
│ [Clear filters]   │                                  │ Current-revision     │
│                   │ Runtime / File / Read            │ estimate: 12 cases  │
│ Domain            │ 42 cases · 119 validations      │                      │
│ □ Runtime 226     │ ┌──────────────────────────────┐ │ 1 case               │
│ □ Manager 103     │ │ ◩ [ ] Read windowed content │ │ 1 family clause      │
│ □ Observability 2 │ │ Plain-language description   │ │ 1 feature clause     │
│ □ Compound 31     │ │ runtime.file.read · 1 case   │ │ − 1 explicit exclude │
│                   │ │ direct: file-read             │ │                      │
│ Family / Group    │ │ effective: file-correctness   │ │ Scope is provisional │
│ Complexity        │ │ 4 declared validations        │ │ until preview.       │
│ Scenario          │ │ Latest: Passed · run… · 2h    │ │                      │
│ Feature           │ │ [Open details]                │ │ [Review run]         │
│ Owner             │ └──────────────────────────────┘ │ [Clear selection]    │
│ Validation        │                                  │                      │
│ Catalog kind      │                                  │                      │
│ Runnable          │                                  │                      │
│ Metadata          │ [Load next 50]                   │                      │
│ Execution label   │                                  │                      │
└───────────────────┴──────────────────────────────────┴──────────────────────┘
~~~

Key rules:

- Counts always identify their unit: cases, tests, validations, or features.
- Search shows why a result matched, such as “Matched validation description.”
- Latest result is optional and must show run ID, timestamp, and revision. It is
  not a Catalog result facet; result filtering belongs to Runs.
- Parent checkboxes use unchecked, checked, and partial states. A parent
  selection creates a SelectionExpression clause; it does not expand cases in
  the browser.
- The selection tray shows clauses, exclusions, and a clearly labeled
  current-revision estimate. Only a ready RunPreview may call the scope exact.
- Clear filters and Clear selection are separate controls.
- Select all matching adds the revision-bound query clause, not only loaded rows.
- Cursor pagination loads at most 200 rows per page; long lists are virtualized.
- A `catalog_revision` notification invalidates the one combined Catalog query
  and refetches it once. A newly saved valid annotated pytest case appears
  automatically without restart or UI registration; an invalid case preserves
  the visibly stale last-good list and links to its collection diagnostic.
- The normal flow uses one catalog query, one preview request, one admission
  request, and one live SSE connection. Evidence is fetched on demand; the UI
  never joins taxonomy, features, validations, and cases through per-row calls.

#### Runnable Harness cases

`catalog_kind` is the discriminant for two valid expanded-case shapes; the UI
MUST NOT impose the Product shape on Harness or silently relax Product:

Both arms share stable `test_id`/`case_id`, title, non-empty description,
validated owner, current pytest `nodeid`, source path/line, one or more named
validations with description/phase/requiredness/evidence declarations,
workspace/telemetry/execution-label/resource/exclusivity policies, optional
bounded parameter summary, lifecycle, `metadata_status`, and `runnable`.

| `catalog_kind` | Required case contract | UI proof contract |
|---|---|---|
| `product` | The shared fields plus exactly one Product topology leaf: `group_id` with derived domain/family, or Compound `scenario_id` with derived `complexity_id`; one or more direct Product features and complete validation mappings; and exactly one `execution_surface` from `cli`, `console_rpc`, `console_http_proxy`, `gateway_rpc`, `daemon_http`, or `direct_daemon_rpc`, with its derived driver/privilege and expected boundary-attestation contract. | Catalog/detail/preview show the expected surface proof. Result/history show the matching observed boundary attestation; missing or mismatched attestation is a contract error, never Pass. |
| `harness` | The shared fields, while omitting `domain_id`, `family_id`, `group_id`, `scenario_id`, `complexity_id`, Product feature references, and validation-to-Product-feature mappings. `execution_surface` is optional. | No Product breadcrumb, empty Product section, or feature-coverage claim is fabricated. When surface is absent, `surface_driver`, privilege, boundary attestation, surface-specific preflight, and surface events are also absent; preview, event, result, and history projections carry `product_boundary_claim=not_applicable`, and every user-facing case surface says “Harness diagnostic — no product boundary claimed.” When a Harness case explicitly declares one of the six surfaces, its expected/observed attestation uses the identical Product rendering and verdict rules. |

A collected case with `catalog_kind=harness` and `runnable=true` is executable
in v1 through this same Catalog route, `SelectionExpression`, exact RunPreview,
preflight, and admitted Run flow. `catalog_kind` and `runnable` are server-backed
URL facets; the Runner Health action opens
`/e2e/catalog?catalog_kind=harness&runnable=true` rather than invoking a hidden
executor. The URL restores visible `Harness` and `Runnable` filter chips after
refresh or sharing; the response, not the browser, applies both predicates.

A valid no-surface row renders, for example:

~~~text
[ ] Verify Docker readiness
Harness diagnostic — no product boundary claimed
harness.docker.readiness / default · 1 named validation · Runnable
Owner: e2e-infrastructure · Workspace: none · Telemetry: standard-v1
Excluded from product feature coverage                         [Open details]
~~~

All Harness records remain inspectable from Runner Health. A Harness record
with `runnable=false` shows its exact metadata or admission reason and cannot be
selected. A Product feature reference on Harness is an invalid local collection
diagnostic, not a chip the browser hides. Any Product topology field or
validation-to-Product-feature mapping on Harness fails the same way. Product
feature-coverage queries
exclude all `catalog_kind=harness` records, but execution results, validations,
evidence, consumption, cleanup, retry, and history use the normal contracts. A
mixed Product/Harness selection is valid when its combined preview passes the
ordinary policy and resource checks.

#### Feature-filtered Catalog

The feature route reuses the same page and components. It adds a contextual
header above results:

~~~text
Feature · workspace-lifecycle
Creates, mutates, verifies, and safely releases a workspace.

12 mapped cases · 31 mapped validation claims
9 direct case associations · 3 inherited associations · 2 metadata gaps

[feature:workspace-lifecycle ×] [other active filters…]
~~~

Every result lists the specific validation claims mapped to the selected
feature. Selecting the feature creates one feature clause whose unit remains
expanded cases, not validations. Feature searches and feature-filtered queries
are server-owned Product queries: their request includes
`catalog_kind=product`, their URL restores that visible filter, and a Harness
record can never appear by client-side post-filtering or by silently ignoring
an invalid Harness feature reference.

#### Compound within the generic Catalog

Compound is rendered by the same Catalog route. Filtering domain=compound adds
generic Complexity and Scenario facets from registry data. A scenario row adds
only fields supplied by its contract:

~~~text
[ ] Workspace survives Runtime → Manager → Observability handoff
Compound / Complex / workspace-cross-surface
3 ordered components · shared workspace context · 7 validations
Runtime: create and write
Manager: list and inspect
Observability: correlate lifecycle evidence
[direct: workspace-lifecycle] [direct: cross-surface-consistency]
~~~

Simple, Medium, and Complex are seeded complexity labels, not frontend enums.
A fourth registered complexity uses the same row, filter, selection, preview,
run, and evidence components with neutral display fallbacks.

#### Catalog states

| State | Page treatment |
|---|---|
| Initial load | Reserve header/three-column geometry; show a labeled skeleton after 300 ms |
| Refresh | Keep verified data and selection; show refreshing state and revision |
| Filtered empty | “No cases match these filters” with Clear filters |
| Known node empty | “0 cases registered” with selection disabled |
| Invalid metadata | Show local diagnostic, file/line, recovery; never fabricate a runnable case |
| Stale selection revision | Mark tray stale, show changed/missing clauses, require reconciliation or new preview |

### 5.2 Test detail

The test detail page separates the declared contract from evidence belonging to
a particular run.

#### Desktop

~~~text
Runtime / File / Read
Read windowed content · offset 3, limit 3                 [Add to selection]
runtime.file.read_windowed  /  offset_3_limit_3

Verifies that offset and limit return the exact requested line window.
[direct: file-read] [effective: file-correctness · from Runtime/File]

┌─ Declared contract, 2/3 ───────────────────┬─ Execution metadata, 1/3 ─────┐
│ Parameters                                 │ Owner and topology             │
│ offset 3 · limit 3                         │ Source path and line           │
│                                            │ Diagnostic pytest nodeid       │
│ Declared validations                       │ Execution labels               │
│ ○ window_content_matches · Declared        │ Workspace policy               │
│   Verify · Required                        │ Telemetry: standard-v1         │
│   Proves file-read, file-correctness       │ Resource/exclusive claims      │
│   Expected claim in plain language         │ Runnable / metadata state      │
│                                            │                                │
│ ○ clean_teardown · Declared                │                                │
│   Teardown · Required                      │                                │
│                                            │                                │
│ Latest result                              │                                │
│ ✓ Passed · run 01J… · Jul 12 · 1.24 s      │                                │
│ [Open frozen evidence]                     │                                │
│                                            │                                │
│ Recent results                             │                                │
└────────────────────────────────────────────┴────────────────────────────────┘
~~~

Declared validation rows always say Declared before a run. Passed/failed state,
expected/actual values, duration, failure records, and artifacts appear only
inside a clearly identified active or historical run.

#### Catalog-kind detail variants

A Product detail also shows its frozen Product/Compound topology, direct and
effective product features, validation-to-feature mappings, expected execution
surface, proof label, required boundary-attestation kind, and privilege class.
It never defaults a missing published surface to `cli`; missing Product
topology, direct features/mappings, or surface makes the catalog record invalid
before this page can offer Add to selection.

The six Product execution surfaces have one exact, non-configurable proof label:

| `execution_surface` | Exact UI proof label | A matching boundary attestation proves |
|---|---|---|
| `cli` | `Real CLI → gateway` | The user-facing CLI binary performed parsing, defaults, output/error handling, exit behavior, and gateway dispatch. |
| `console_rpc` | `Console /api/rpc → gateway` | The request crossed the console HTTP/SSE `/api/rpc` boundary and the console proxied it to the gateway. |
| `console_http_proxy` | `Console HTTP proxy → daemon HTTP` | The request crossed the console daemon-HTTP proxy, including its endpoint resolution and HTTP proxy behavior. |
| `gateway_rpc` | `Direct gateway RPC · internal` | The direct gateway protocol/client path worked; the CLI and console were bypassed. |
| `daemon_http` | `Direct daemon HTTP · console bypassed` | The resolved daemon HTTP endpoint worked without the console proxy. |
| `direct_daemon_rpc` | `Privileged daemon RPC · allowlisted` | An allowlisted internal lifecycle RPC crossed the privileged daemon boundary; no public CLI or console surface is claimed. |

Collection assigns `execution_surface`; preview freezes it into the run manifest,
and case events and results retain that value. The label is derived from the
frozen value. Catalog, detail, preview, retry, and Run provide no surface picker,
dropdown, editable label, or override. An observed attestation does not select or
repair a surface. Missing, duplicate, wrong-driver, wrong-boundary, or otherwise
mismatched attestation makes the case `Error · contract`; it is never a valid or
partially valid Pass.

A no-surface Harness detail uses the same layout without fake empty Product
sections:

~~~text
Harness diagnostic
Verify Docker readiness                                  [Add to selection]
harness.docker.readiness / default

Harness diagnostic — no product boundary claimed
Checks that the runner can reach a healthy Docker daemon before product work.

Declared validations                 Execution metadata
○ docker_ping_ready · Declared        Owner: e2e-infrastructure
  Setup · Required                    Source path and line
  Expected claim in plain language   Workspace: none
                                      Telemetry: standard-v1
                                      Resource claims
                                      Runnable / metadata state
~~~

The Product topology, Product feature, feature-mapping, expected surface,
privilege, and attestation sections are omitted rather than rendered as empty,
forbidden, unsupported, or unavailable fields. Surface absence is legitimate
only for `catalog_kind=harness`; it is not Unsupported, Unavailable, a metadata
gap, or a failed validation. Harness named validations neither require nor
permit validation-to-Product-feature mappings. A surfaced Harness detail
instead shows its declared surface and required attestation normally, while
remaining excluded from Product coverage.

### 5.3 Run preview

Review run is the only bridge from selection to admission. It is an 800–900-pixel
right drawer at 1024/1440 and a full-screen dialog at 375/390/768.

#### Reference ready state

~~~text
Review run · Preview Ready                                      [Close]
12 exact expanded cases · 37 declared validations
Catalog rev 8a4d… · generated 12:06:18 · expires 12:16:18

┌─ Exact ordered scope ──────────────────────┬─ Policies ────────────────────┐
│ 1  test_id / case_id                       │ Repository: e2e/ @ 91c…       │
│    Case title · 4 validations              │ Source mode: read-only        │
│    [Real CLI → gateway]                    │ Workspace: fresh attempt      │
│ 2  test_id / case_id                       │ Prepared from: testbed/       │
│    Case title · 3 validations              │ Telemetry: standard-v1        │
│    [Direct daemon HTTP · console bypassed] │ CPU · memory · disk · cgroup  │
│ … page through every exact case            │ Lane: serial                  │
│ Per-case policy deviations are inline.     │ Fail-fast: Off (default)      │
│                                            │ Locks/resource ranges         │
└────────────────────────────────────────────┴────────────────────────────────┘

Preflight · checked 12:06:17
✓ Controller       ✓ Docker          ✓ Gateway
✓ Workspace root   ✓ Testbed         ! Optional metric unsupported
✓ Disk 8.2 GB free ✓ Serial lane     ✓ Source/image revision

Expected cleanup: teardown, telemetry finalization, workspace verification
[Back to selection]                                      [Start run]
~~~

Changing a policy creates a new checking preview. It never mutates a Ready
snapshot in place.

Each check presents both its server-owned, policy-derived `state` (Ready,
Warning, or Blocked) and, when relevant, its observed condition (Degraded,
Unsupported, Unavailable, or Error). Requiredness alone does not determine the
state: `unsupported_policy=block` reads “Blocked · Unsupported,” while `skip`
reads “Warning · Unsupported” and explains whether it skips the whole case
(required validation) or only the optional validation while the case still
executes. Supporting-only unsupported telemetry is a warning/gap. The UI never
reinterprets the condition without the server-provided admission state and
frozen policy.

#### Checking, blocked, and stale

| Preview state | Header | Body | Start control |
|---|---|---|---|
| Checking | “Checking preflight…” | Reserved scope/policy layout plus current named check | Disabled: “Waiting for preflight” |
| Ready | “Preview Ready” | Complete exact ordered cases and current checks | Enabled |
| Blocked | “Run blocked” | Blocker adjacent to policy/check plus recovery action | Disabled with exact reason |
| Stale | “Preview expired or dependencies changed” | Show changed digest inputs | Disabled; Refresh preview |

Admission retains a loading label until the API returns one run or a structured
error. Duplicate clicks are prevented, and an idempotent retry never creates a
second run.

An unfinished run whose direct-run overlay reports
`recovery_compatibility=mismatch` is a controller-owned global admission
block, not a warning on that run alone. Every open or newly requested preview
shows the named recovery blocker, disables Start, and links to the blocked Run
page and Runner Health. Refreshing preflight cannot clear the blocker; Start is
enabled only after a later controller projection says the recovery lock has
been resolved and the serial lane is admissible. The browser never infers
compatibility from matching version strings or offers a generic Retry that
could contend with the retained recovery lock.

Harness-only and mixed Harness/Product previews follow this exact interaction.
Each Harness case remains visibly labeled as diagnostic and excluded from
product coverage; that label does not bypass metadata validation, named
validations, workspace policy, telemetry policy, preflight, cleanup, or
evidence retention. A valid no-surface Harness preview row says “Harness
diagnostic — no product boundary claimed,” freezes the declared absence of an
execution surface as `product_boundary_claim=not_applicable`, and omits
surface-driver, privilege, boundary-attestation, surface-specific preflight,
and surface-event claims. It can become Ready when its declared policies and
applicable checks pass; the UI MUST NOT invent a “missing surface” blocker or
silently add `cli`. A surfaced Harness row and every Product row freeze the
declared surface, proof label, driver/privilege, required attestation, and
surface-specific checks.

Preflight is selection-specific. Console readiness is required only when the
exact scope contains `console_rpc` or `console_http_proxy`. If sandbox-console is
unavailable, those selected cases are Blocked with that named dependency;
`cli`, `gateway_rpc`, `daemon_http`, and `direct_daemon_rpc` cases remain eligible
when their own checks pass. Catalog projection, ordinary CLI execution, and
non-console preview must not acquire a runtime dependency on sandbox-console.

### 5.4 Live and completed run

One Run page renders the same RunProjection live and historically.

#### Wide run composition

~~~text
Run 01J… · Running · 03:42 elapsed · fail-fast On             [Cancel run]
Stream Live · sequence 284 · event 1 s ago · cleanup pending
Catalog 8a4d… · repository source 3fb… · attempt workspace · standard-v1

Queued 8 | Running 1 | Passed 26 | Failed 0 | Skipped 0
Cancelled 0 | Error 0 | Not run 4

┌─ Blocking failure detected · final verdict pending ─────────────────────────┐
│ First failure · Read windowed content › window_content_matches             │
│ Assertion failure · Verify · 12:03:14                                      │
│ Cleanup in progress; terminal Failed/Error count is not final yet.         │
│ [Jump to failure] [Open evidence interval] [Copy stable reference]         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─ Ordered cases, 40% ─────────────┬─ Selected case / validation, 60% ───────┐
│ [Search cases] [State ▾]         │ Read windowed content                   │
│                                  │ Purpose and feature claims              │
│ ✓ Passed · Real CLI → gateway    │ Started 12:03:13 · 842 ms               │
│ ✕ Cannot pass · cleanup 3.1 s    │ Surface: Real CLI → gateway             │
│ ● Running · 4.1 s                │ Setup → Execute → Verify → Teardown     │
│ ○ Not run · caused by fail-fast  │ ✓ setup  120 ms                         │
│ ○ Not run · caused by fail-fast  │ ✓ execute 210 ms                        │
│                                  │ ✕ verify  window_content_matches        │
│ Runtime / File                   │ ● teardown / cleanup in progress         │
│ Manager / Management             │                                        │
│ Compound / Complex               │ Evidence health: Collecting             │
│                                  │ [Overview] [Timeline] [Evidence] [Logs]  │
└──────────────────────────────────┴─────────────────────────────────────────┘
~~~

#### Catalog-kind result truth

Product case results always pair the manifest-frozen expected surface/proof
label with the observed boundary attestation, driver, privilege, time, and
evidence reference. Missing, duplicate, wrong-driver, or wrong-boundary proof
renders `Error · contract` and cannot coexist with Passed.

A valid no-surface Harness case shows “Harness diagnostic — no product boundary
claimed” in the ordered row, inspector, result summary, retry preview, and
history. The frozen preview, every case-scoped event, and the terminal result
carry `product_boundary_claim=not_applicable`; surface lifecycle events and
expected/observed surface-attestation rows are absent. A missing surface is not
rendered as Unsupported, Unavailable, Error, or a feature-coverage gap. A
missing or contradictory `product_boundary_claim` is instead `Error · contract`
because the projection can no longer prove which union arm ran. The verdict
still requires every required named validation plus mandatory cleanup and
telemetry finalization to reach their declared outcomes. If those succeed, the
case may truthfully Pass; the UI attributes that Pass only to the named Harness
diagnostic claims and never to a Product feature or boundary. A surfaced Harness
result uses the normal expected/observed attestation rendering but remains
excluded from Product coverage.

The first failure banner appears before logs and does not steal focus or
automatically scroll the user. It is announced once. If teardown later makes
the run Error, the original assertion remains the first failure and the page
adds:

> Run ended with teardown error. The assertion above was the first failure.

The final severity-determining failure and the first causal failure are both
visible and separately labeled.

#### In-flight fail-fast truth

When a validation reaches a blocking failure but cleanup/telemetry finalization
is still active:

- show “Blocking failure detected · final verdict pending”;
- close scheduler scope and show queued cases as causal Not run;
- keep the active case/run nonterminal;
- show cleanup and evidence finalization progress;
- do not increment final Failed or Error counts prematurely;
- do not enable retry until the parent run is terminal.

After finalization, show the causal explanation:

> Stopped by fail-fast after Test 2 › Validation 3 failed. Cleanup completed.
> Tests 3–5 were not run.

#### Connection and timers

| Stream state | Timer behavior |
|---|---|
| Live | Elapsed values derive from the latest verified monotonic timing and one shared UI clock |
| Connecting/reconnecting under stale threshold | Continue only with a visible “estimating” qualifier |
| Stale/offline | Freeze at the last verified projection and show “as of 12:03:20” |
| Recovery/bundle mismatch | Freeze at the last persisted watermark, label that projection historical, and render the current-controller identity overlay; do not reconnect-loop or imply live work |
| Historical | Use frozen start/completion/duration only |

The UI never presents a locally ticking disconnected timer as verified runtime
state.

#### Controller recovery identity

`recovery_state` is persisted run history; `recovery_compatibility` is the
non-authoritative current-controller overlay returned by the direct-run API.
The only v1 values are `exact_match` and `mismatch`. The UI never merges the
overlay into the frozen projection or rewrites the persisted verdict/state.
When the overlay is `mismatch`, the Run page pins
this blocking panel above the summary:

~~~text
Recovery blocked — controller bundle changed
Last persisted state: Running · historical last valid at sequence 284
No current execution is claimed. New-run admission is blocked.

Admission controller  sha256:…  [Show complete identity] [Copy reference]
Current controller    sha256:…  [Show complete identity] [Copy reference]
Decision              current digest does not equal admitted digest

[Open typed recovery action] [Runner Health]
~~~

“Running” in this panel is subordinate text prefixed by “Last persisted state”
and “historical last valid”; it never uses the live-running icon, live timer,
Live stream label, active-run count, or Cancel affordance. The stream and all
timers freeze at `applied_through_seq` and the last verified timestamp. Retry,
Review retry, Resume, and Start remain unavailable while the recovery lock is
retained.

Both identity disclosures render the complete referenced
`ControllerBundleIdentity@1`: controller revision, packaged-bundle digest, and
executable/runtime and lock identity. Decision details render both digests,
their equality result, typed reason code/message, and the controller-provided
typed recovery action. Long digests wrap or copy without clipping. A version label or Git
commit may appear only as provenance and never replaces this evidence. The UI
renders only the action kind and target returned by the API; it does not build
or execute a shell command from display text.

For an exact-bundle recovery, the page may show “Recovery in progress” while
appended recovery events arrive. Each such event's detail
identifies its actual `producer_revision`. Once terminal, the frozen run and
affected case results expose the complete admission identity and every ordered
recovery-session controller identity plus its compatibility decision evidence.
This survivor provenance
remains available from the same historical Run page after logs, telemetry
samples, screenshots, and other purgeable evidence have been removed; an
`evidence_purged` view must not hide it or replace it with the controller that
happens to be current when history is opened.

#### Recovery-session provenance and a crash during recovery

Recovery itself can be interrupted. `RunProjection` therefore owns an
append-only `recovery_sessions[]` survivor array ordered by persisted
registration sequence, never by a wall clock or browser arrival order. Every
entry has:

- an opaque, run-unique `recovery_id`;
- the complete recovery writer's `ControllerBundleIdentity@1`;
- the admitted/current bundle digests and exact-equality decision used to
  authorize that writer;
- observed prefix digest/sequence, action dispositions, first/last event times,
  and successor reference where applicable; and
- derived `status=superseded | active | manual_intervention | complete`.

The controller and event reducer create and transition these entries; the UI
never reconstructs them from `producer_revision`, timestamps, or logs. A
exact-bundle writer appends and fsyncs `recovery.session_registered` before any
external or lifecycle mutation. External actions use only the write-ahead pair
`recovery.action_started` and `recovery.action_finished`, keyed by stable
`recovery_step_id`. There is no session-finished event: a later registration
derives the previous session as `superseded`; the session whose folded prefix
contains `run.finished` is `complete`; and the last nonterminal registration is
`active` or `manual_intervention` from its folded action state. The original
`run.interrupted(failure_kind=controller_restart)` is appended at most once per
run. A later session references that existing interruption, reconciles prior
write-ahead actions, and appends only missing deterministic steps. Replaying the
journal or reconnecting SSE after any sequence produces the same ordered
session array, run/case counts, and cleanup/telemetry outcomes without duplicate
logical events or repeated announcements.

The Run page labels an `active` entry **Current recovery session** only while
the direct-run overlay proves that entry's full controller/lock identity is the
current writer. If the direct API is unavailable or cannot prove ownership, the
entry reads **Last persisted active recovery session · current ownership
unknown** and receives no Live indicator. A prior `superseded` entry is rendered
as **Superseded · earlier recovery controller stopped**, while retaining the
canonical raw status in its disclosure. A `manual_intervention` entry is pinned
as blocked with its exact action disposition and typed controller action.
Previous entries appear under **Previous recovery sessions** in registration
sequence order with controller, decision, prefix, actions, status, and event
range disclosures. On a terminal historical run, no session is labeled current;
the `complete` entry is labeled **Final recovery session** and all preceding
sessions remain inspectable after evidence purge.

~~~text
Recovery in progress · current session recovery-02 · Active
Controller sha256:… · exact bundle · registered at sequence 311
Original run interruption · sequence 285 · recorded once

Previous recovery sessions (1)                         [Show]
recovery-01 · Superseded · earlier controller stopped · Controller sha256:…
~~~

At every required viewport, the current/unknown ownership statement and the
single original interruption remain visible before the collapsed prior-session
details. Session status uses text and icon, never color alone. The panel does
not offer Resume, retry, or a browser-derived recovery action.

#### Historical parity and retry

Completed history removes stream mutation and Cancel. It retains the frozen
manifest's labels, features, validations, policies, timing, evidence, and
workspace lineage. It offers only applicable child-run preview actions:

- Review failed cases
- Review not-run cases
- Review failed + not-run cases

Every action creates a new preview with parent_run_id and retry_mode. No action
is labeled Resume.

Historical detail also retains the admission controller identity and, when
restart recovery occurred, every ordered recovery session with its complete
controller identity and exact compatibility decision evidence. These are
completion-projection survivors, not optional raw artifacts, and therefore
remain inspectable and copyable after evidence purge. A historical page never
substitutes the current-controller overlay identity for a frozen survivor.

### 5.5 Evidence inspector

Evidence is part of every domain's run detail. Runtime and Manager tests receive
supporting Observability evidence without changing ownership. Observability
tests use the same evidence components.

#### Information order

1. Product verdict and EvidenceHealth.
2. Named validations and selected critical interval.
3. Unified trace/time ruler.
4. Resource summary.
5. Telemetry channels and accessible tables/charts.
6. Structured operation logs.
7. Artifacts.
8. Raw bounded logs.

#### Resource summary

| Resource | Required summary |
|---|---|
| Wall/CPU | Wall duration, CPU total, average, p95, peak, units, aggregation |
| Memory | Current/peak, cgroup peak/limit, provider, coverage |
| Disk I/O | Read/write bytes and operations; never conflated with capacity |
| Disk capacity | Workspace size delta, available/required bytes, retained size |
| Cgroups | Identity, v1/v2/none/unknown, limits, usage, provider |
| Resources | Sandbox/session/container/process lifetimes and counts |
| Evidence | Samples/logs/artifacts recorded, dropped, capped, truncated, redacted |

#### Channel lifecycle

Collection lifecycle and final availability are separate. Every channel's
`collection_state` is exactly `scheduled | collecting | finalizing | finalized`:

| Collection state | UI copy |
|---|---|
| Scheduled before resource identity | “Scheduled · waiting for resource” |
| Collecting before first sample | “Collecting · waiting for first sample” |
| Collecting with samples | “Collecting · last sample 1 s ago” |
| Finalizing | “Finalizing evidence” |
| Finalized | Show available, partial, unsupported, unavailable, error, or invalid |

Missing samples render as gaps, never zero. Charts always have a table
alternative. A selected validation highlights its evidence interval on the
common ruler and exposes Clear interval.

#### Live logs

Raw logs are collapsed by default and provide:

- Pause follow and Resume follow;
- “N new records” when the user scrolls away from the tail;
- text search and level/source/correlation filters;
- visible selected evidence interval and Clear interval;
- cap, truncation, omission, and redaction notices;
- copy for selected bounded text, not an unbounded page dump.

New log records never force-scroll a user who has paused or moved upward.

### 5.6 Runs

Result and evidence filtering belongs here.

#### Desktop

~~~text
Runs
[Search] [Result ▾] [Domain ▾] [Feature ▾] [Evidence ▾] [Revision ▾] [Period]
History ready · generation 42 · indexed 318 runs             [Open known run]

Active run
● Running · 7/18 cases · Live 2 s ago                         [Open]

Created      Scope                 Result / distribution      Duration
             Parent / retry        Evidence / first failure   Revisions
Jul 12 18:10 Runtime / File        ✕ Failed                   01:43
             31 cases              27 passed · 1 failed       catalog 8a4d…
             fail-fast run         3 not run                  repository 3fb…
                                   Evidence degraded           [Open failure]
~~~

Rows use frozen summary data. Filters include result, evidence health,
catalog/repository-source revision, domain, feature, parent run, retry mode, and
retention.
Cursor pagination and virtualization keep DOM size bounded.

The Runs list consumes `HistoryProjectionHealth` from every successful history
response and from controller health:

~~~text
state: ready | rebuilding | stale | error
serving_last_good: boolean
generation?: integer
generated_at?: timestamp
last_success_at?: timestamp
indexed_run_count: integer
discovered_run_count: integer
reason?: { code, message, retryable }
~~~

`incompatible` is a distinct UI/API error view, represented by typed
`history_incompatible` in `reason.code` or the list error response; it is not an
invented fifth value of the projection `state` enum. The page obeys this state
table:

| Projection condition | Runs-page treatment |
|---|---|
| `ready` | Show generation, generated time, indexed count, rows, filters, and pagination. “No runs yet” is allowed only for an unfiltered successful ready response with `indexed_run_count=0`; “No runs match” is allowed only for a successful ready filtered response. |
| `rebuilding` and `serving_last_good=true` | Keep the frozen generation's rows, filtering, and pagination; show a timestamped rebuilding warning and disclose that newer terminal or retention commits may be absent. |
| `rebuilding` and `serving_last_good=false` | Replace the table with “Run history rebuilding,” Retry, Runner Health, and Open known run. Never show “No runs” or a zero count. |
| `stale` and `serving_last_good=true` | Keep the last-good rows usable behind a timestamped stale warning; show `last_success_at`, counts, and the typed reason. |
| `error` with no compatible generation | Replace the table with an explicit unavailable error and safe Retry/diagnostic actions. Never synthesize rows or an empty result. |
| `history_incompatible` | Show “Run history incompatible,” the non-retryable reason and Runner Health; do not retry-loop or call the store empty. |

Open known run accepts a run ID and navigates directly to
`/e2e/runs/:runId`. Existing deep links and the active-run card use the same
direct lookup and remain usable in every history-list condition. A direct
lookup may still return its own typed run-not-found or run-corruption error;
projection unavailability is never substituted for that run-local truth.

### 5.7 Workspaces

The workspace page displays the server-derived
`E2E_WORKSPACE_ROOT=<WORKSPACE_STORE_ROOT>/e2e` and its seven direct
children: `testbed/`, `attempts/`, `quarantine/`, `tmp/`, `runs/`, `catalog/`,
and `tooling/`. It presents `TEST_REPOSITORY_ROOT` as the Git repository and
`WORKSPACE_STORE_ROOT` as the external mutable parent. The derived source roots
`E2E_SOURCE_ROOT=<TEST_REPOSITORY_ROOT>/e2e` and
`BENCHMARK_SOURCE_ROOT=<TEST_REPOSITORY_ROOT>/benchmark` are read-only inputs;
the external workspace roots are the only mutable side of this boundary.

#### Desktop

~~~text
Workspaces
Test repository · Git-controlled
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
e2e/ · E2E implementation · read-only
benchmark/ · benchmark source/config · read-only

Product repository · Git-controlled · read-only product under test
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox

Workspace store · configured · external · non-versioned
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test-workspace

E2E workspace root · server-derived · fixed
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test-workspace/e2e
Root marker: Verified                 No browser path setting or picker

Benchmark workspace root · server-derived · fixed
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test-workspace/benchmark

┌─ testbed/ ──────────────┐ ┌─ attempts/ ─────────────┐ ┌─ quarantine/ ───────────┐
│ Prepared 91c…           │ │ 12 marker-owned leaves  │ │ 2 retained leaves   │
│ Verified 12:05          │ │ 1 active · 11 finalized │ │ Reasons recorded    │
│ [Verify] [Repair]       │ │ [Review attempts]       │ │ [Review quarantine] │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────┘

Direct operational roots
tmp/ · staging clean     runs/ · 318 retained
catalog/ · revision 8a4d…     tooling/ · compatible

Capacity: 42 GB available · 8.1 GB retained                [Review retention]
[Search leaves] [Lifecycle ▾] [Purge eligibility ▾] [Origin ▾] [Age ▾]

Owned leaf          Lineage / source run      Lifecycle / digest       Size
Verified at         Cleanup / test result     Purge decision           Actions
~~~

`TEST_REPOSITORY_ROOT`, `PRODUCT_ROOT`, and `WORKSPACE_STORE_ROOT` are the only configurable roots. The
server derives every source and workspace child; the browser receives the
resolved values for display only. There is no editable path field, filesystem
picker, query parameter, or mutation payload that can replace a root. The page
shows `BENCHMARK_WORKSPACE_ROOT` as a separately owned sibling without listing
or mixing its leaves into E2E retention actions.

Root, testbed, and operational-root readiness precede retained workspace leaves.
“Safe,” “ready,” “verified,” “eligible,” ownership, and digest values appear
only after the corresponding verified projection says so. Source files under
`e2e/` and `benchmark/` never receive mutation controls.

Selecting a workspace opens a detail drawer with:

- immutable source/run/test/case/attempt lineage;
- validated root-relative location, safely wrapped with copy support;
- workspace lifecycle and verification timestamp;
- digest, size, cleanup result, test result, and safety scan;
- reuse state and blockers;
- retention history and purge tombstone;
- ownership-marker evidence and backend-projected purge eligibility;
- contextual Verify, Review run from copy, and confirmed Purge actions only for
  eligible marker-owned leaves.

Retention history is a separate post-completion stream. When a row exposes its
transaction/event identity, it uses the retention `stream_id` plus sequence and
the event's own `producer_instance_id` and `producer_revision`. It never labels
the admission controller, recovery controller, or current page controller as
the purge producer. The immutable terminal admission/recovery provenance stays
in run history while the retention timeline truthfully identifies the
controller revision that performed each purge mutation.

Review run from copy enters the normal RunPreview flow. Purge targets a stable
server-issued leaf identity, not a browser-supplied path. The controller must
re-resolve it below an approved direct child, verify its ownership marker and
inactive/eligible projection, and require explicit confirmation. The E2E and
benchmark workspace roots, all seven E2E child roots, either source root, active
leaves, unmarked entries, unknown entries, and anything outside the derived
workspace root are never purgeable. Generic Workspaces purge is offered only for
eligible leaves projected below `testbed/`, `attempts/`, or `quarantine/`;
`tmp/`, `runs/`, `catalog/`, and `tooling/` expose readiness or their owning
typed retention action, never a generic root purge. A quarantined leaf is
purgeable only when its backend projection explicitly marks that individual
leaf eligible; quarantine membership alone is not permission.

### 5.8 Runner Health

Runner Health opens as an approximately 480-pixel right drawer.

~~~text
Runner health
Degraded · checked 12:06:48                              [Retry all]

Admission
New runs blocked — prepared template is unavailable        [Repair]

Controller and stream
✓ Controller API     Ready · 18 ms
✓ Event stream       Live · seq 284 · 1 s ago

Catalog
✓ Product projection Revision 7b2…
! Combined catalog   Stale · last good 8a4d…              [Refresh]

Run history
! Summary projection Rebuilding · serving generation 42  [View runs]

Dependencies
✓ Docker             Ready
✓ Gateway            Ready
✕ sandbox-console    Unavailable · console surfaces only  [Retry]
✓ Manager CLI        Ready

Repository inputs
✓ TEST_REPOSITORY_ROOT  Git repository
✓ e2e/                  Read-only E2E implementation
✓ benchmark/            Read-only benchmark source/config
✓ PRODUCT_ROOT          Git repository · read-only product under test
✓ WORKSPACE_STORE_ROOT  External · non-versioned · unowned parent
✓ Root separation       Repositories and store are pairwise disjoint

Workspace and capacity
✓ E2E_WORKSPACE_ROOT        Derived · root marker verified
✓ BENCHMARK_WORKSPACE_ROOT  Derived · separate benchmark workspace
✕ testbed/                  Error                         [Repair]
✓ attempts/ · quarantine/   Ready
✓ tmp/ · runs/              Ready
✓ catalog/ · tooling/       Ready
! Disk capacity      Degraded · 8.2 GB free

Surface readiness · selection-specific
✓ Real CLI → gateway
✕ Console /api/rpc → gateway               Console unavailable
✕ Console HTTP proxy → daemon HTTP          Console unavailable
✓ Direct gateway RPC · internal
✓ Direct daemon HTTP · console bypassed
✓ Privileged daemon RPC · allowlisted

Execution and evidence
✓ Serial lane        Available
✓ Telemetry          CPU · memory · disk · cgroup

Harness diagnostics
11 runnable cases · catalog_kind=harness
Excluded from product feature coverage
[Review runnable Harness cases]
~~~

Checks use ready, checking, degraded, unavailable, or error and always show
checked time, diagnostic, and recovery. Unknown never maps to Ready.

The drawer never turns sandbox-console unavailability into a global admission
block. It identifies `console_rpc` and `console_http_proxy` as unavailable and
blocks only previews that selected either surface. The other four surface rows
retain their independently computed readiness, and ordinary Catalog collection
does not require a running console.

Harness/preflight cases are discoverable here and visibly excluded from product
coverage. In v1, Review runnable Harness cases opens the generic Catalog with
`catalog_kind=harness&runnable=true`; selection, exact preview, preflight,
admission, execution, cleanup, evidence, and history then use the same contracts
as every other live case. There is no direct, manual, or Harness-specific
executor. Non-runnable diagnostics remain visible with their local reason.

Runner Health also renders `HistoryProjectionHealth`. Rebuilding/stale health
with `serving_last_good=true` links to the usable timestamped generation.
Rebuilding/error without last-good and `history_incompatible` link to the
explicit unavailable/incompatible Runs view; neither is summarized as zero
runs. Open active run and direct known-run navigation remain enabled.

If an unfinished run has `recovery_compatibility=mismatch`, Runner Health
adds “Recovery blocked — controller bundle changed,” the blocked run ID, both
controller revisions, typed reason, and links to the Run page's complete
identity/decision evidence and typed recovery action. Serial lane and Admission
remain Blocked, not Ready or merely Degraded, until the controller reports the
lock resolved. Catalog and historical browsing remain usable; every preview
Start control stays disabled.

## 6. Interaction contracts

### 6.1 Selection truth

Before preview, the browser stores and displays a revision-qualified
SelectionExpression:

- ordered case, node, query, and feature clauses;
- explicit test_id/case_id exclusions;
- the originating catalog revision;
- a provisional current-revision estimate, if supplied by the controller.

The browser does not expand or truncate the authoritative selection. A ready
preview is the first surface allowed to say “exact ordered cases.”

If the catalog revision changes, the tray becomes stale and shows what changed.
The user must reconcile the expression or request a new preview; the UI never
silently removes cases.

### 6.2 Find by feature and run

~~~mermaid
sequenceDiagram
    actor User
    participant Catalog
    participant Preview
    participant Controller
    participant Run

    User->>Catalog: Search feature label or description
    Catalog-->>User: Matching cases and mapped validation claims
    User->>Catalog: Select feature plus mixed cases/exclusions
    Catalog-->>User: Clauses and provisional scope
    User->>Preview: Review run
    Preview->>Controller: SelectionExpression + policies
    Controller-->>Preview: Checking, then exact Ready or Blocked/Stale
    User->>Controller: Start ready preview
    Controller-->>Run: One admitted immutable run
    Run-->>User: Live projection, first failure, validation and evidence state
~~~

### 6.3 Cancel

Cancel is visible only for a nonterminal live run. After activation:

- the button becomes “Cancelling…” and cannot be submitted twice;
- queued cases show Not run with `reason=user_cancel` and the label “User
  cancelled before start”;
- started work shows Cancelling/Cancelled, never Not run;
- cleanup and telemetry finalization remain visible and mandatory;
- any mutation error appears beside Cancel with safe retry guidance;
- cleanup failure may make the terminal result Error while preserving the
  cancellation request in history.

### 6.4 Reconnect and incompatibility

On an event gap or disconnect, the UI preserves the last verified projection
and focus. It never clears counts, selection, or the selected case.

An unknown optional display field receives a neutral fallback. An unknown
lifecycle state, unsupported schema major, or unknown event semantic is not a
display fallback: the UI stops applying updates, freezes the last verified
projection, and shows an incompatibility error.

### 6.5 Live update behavior

- First failure is announced once without auto-scroll, focus theft, or
  automatic row selection.
- Aggregate progress announcements are throttled; logs, samples, timers, and
  individual events are not individually announced.
- A single shared clock updates visible elapsed values; there is no timer per
  row.
- Live reducer commits are batched without delaying first-failure visibility.
- Background refresh never clears a selection or closes an inspector.

## 7. State model presented in the UI

### 7.1 Execution states

| Entity | States that must remain distinct |
|---|---|
| Preview | checking, ready, blocked, stale |
| Run | queued, running, cancelling, passed, failed, error, cancelled |
| Case | queued, running, passed, failed, skipped, cancelled, error, not run |
| Validation/phase | declared, running, passed, failed, skipped, cancelled, error, not run |
| Cleanup | declared, running, passed, error, not run |
| Stream | connecting, live, reconnecting, stale, offline |
| Recovery | none, recovering, complete, manual intervention |
| Recovery session | superseded, active, manual intervention, complete |
| Current-controller recovery compatibility overlay | compatible, incompatible |

### 7.2 Evidence and workspace states

| Entity | States that must remain distinct |
|---|---|
| Telemetry availability | available, partial, unsupported, unavailable, error, invalid |
| Telemetry collection | scheduled, collecting, finalizing, finalized |
| EvidenceHealth | complete, degraded, unavailable, invalid |
| Workspace | active, finalized, quarantined, purged |
| Reuse | not evaluated, eligible, ineligible |
| Health check | ready, checking, degraded, unavailable, error |
| History projection | ready, rebuilding, stale, error; incompatible is a typed reason/view, not a projection state |

### 7.3 Async state gallery

The UI implementation must ship a fixture gallery for:

- initial loading;
- background refresh;
- known empty and filtered empty;
- invalid catalog with and without last-good data;
- stale catalog and stale selection;
- checking, blocked, stale, and ready preview;
- mutation error and active-run conflict;
- connecting, reconnecting, stale, offline, and recovered stream;
- incompatible schema/event;
- permission or workspace safety rejection;
- scheduled, collecting, finalizing, and finalized telemetry collection;
  nonfinal states show provisional gaps without inventing final availability,
  while finalized fixtures cover available, partial, unsupported, unavailable,
  error, and invalid availability;
- ready history; rebuilding with and without last-good; stale last-good; error
  without a compatible generation; `history_incompatible`; and a working known-
  run deep link while the list is unavailable;
- exact-bundle recovery; mismatched current controller over a
  persisted Running projection; a successor recovering after the first recovery
  writer crashes; and a recovered terminal run after evidence purge;
- demo mode.

Each fixture has truthful copy, a recovery action where safe, and no success-like
fallback.

### 7.4 Catalog-kind fixture suite

One stable fixture record—`test_id=harness.docker.readiness`,
`case_id=default`, `catalog_kind=harness`, `runnable=true`—has title,
description, owner, one required named validation, policies, lifecycle, and
resource claims, but no Product topology, Product feature references,
validation-to-Product-feature mappings, or execution surface. The following
fixtures reuse that exact identity and frozen contract rather than
hand-authoring inconsistent page data:

| Fixture ID | View | Required assertions |
|---|---|---|
| `harness-no-surface.catalog-url` | Shared URL | Loading `/e2e/catalog?catalog_kind=harness&runnable=true` restores visible Harness/Runnable chips, sends both predicates to the server, returns the record, and renders “Harness diagnostic — no product boundary claimed”; refresh and back/forward preserve the same query and selection semantics. |
| `harness-no-surface.catalog-filter` | Catalog filters | Selecting Catalog kind = Harness and Runnable = true updates the shareable URL, replaces rather than client-filters the server result set, exposes the no-surface row, and keeps Product feature facets/coverage absent. |
| `harness-no-surface.detail` | Test detail | Shows purpose, owner, named validation and policies; omits Product topology, feature/mapping, surface, privilege, and attestation sections; treats absent surface as legitimate and shows the exact diagnostic statement. |
| `harness-no-surface.preview` | Ready preview | Freezes `product_boundary_claim=not_applicable`, shows the exact diagnostic statement, runs applicable checks, and has no surface driver, privilege, attestation, surface-specific preflight/event promise, or invented CLI claim. |
| `harness-no-surface.live-result` | Live case, terminal result, retry, and history | Every case event and the terminal result retain `product_boundary_claim=not_applicable`; validation/timing/evidence/cleanup render normally; Pass requires completed required claims; the exact diagnostic statement persists; and expected/observed attestation, surface lifecycle, and Product-coverage claims are absent. |
| `harness-product-contract.invalid` | Catalog diagnostic and Runner Health | A Harness record containing any Product topology field, Product feature reference, or validation-to-Product-feature mapping is rejected locally with source/field detail and is never selectable. |
| `product-contract.invalid` | Catalog diagnostic and Runner Health | A Product record missing topology, direct product features/mappings, or one of the six execution surfaces/attestation contracts is rejected and never defaults to Harness or CLI. |

### 7.5 Controller-recovery fixture suite

The recovery fixtures use one immutable admission
`ControllerBundleIdentity@1`. Current/recovery identities either have the exact
same packaged-bundle digest or a different digest. The direct-run API supplies
the equality decision; the browser does not manufacture it.

| Fixture ID | Input truth | Required assertions |
|---|---|---|
| `controller-recovery.mismatch` | Persisted projection is `running` through sequence 284; current overlay is `mismatch`; admitted/current bundle digests differ; recovery lock and lane remain held. | Run header says “Recovery blocked — controller bundle changed” and “Last persisted state: Running · historical last valid,” freezes timer/watermark, removes live/Cancel claims, exposes both digests, equality result, typed reason/action, and blocks Start on every preview. |
| `controller-recovery.exact-terminal` | The current bundle digest exactly equals the admitted digest, appends recovery events, and terminalizes the run as Error. | Live recovery shows exact-match authorization; terminal detail keeps the admission/recovery identity and decision evidence. |
| `controller-recovery.crash-during-recovery` | `recovery-01` is registered, appends the run's sole `run.interrupted` and one write-ahead `recovery.action_started`, then crashes. The same exact bundle registers `recovery-02`, reconciles the action, appends only missing steps, and terminalizes once. | The live panel labels only `recovery-02` Current, labels `recovery-01` Superseded, and shows the original run interruption once. Replay, reconnect, refresh, and terminal history produce identical state without duplicate mutation. |
| `controller-recovery.purged-survivors` | The compatible terminal fixture is reopened after purgeable artifacts are removed and retention events were produced by a third controller revision. | The same Run route shows typed `evidence_purged` for removed evidence while admission/recovery identities and decision evidence remain inspectable; retention history attributes each mutation to its retention event `stream_id`, sequence, `producer_instance_id`, and `producer_revision`, never to either frozen run identity. |

The fixture implementation records every expected label, disabled action, link,
identity value, and digest in DOM assertions at 375, 390, 768, 1024, and 1440
CSS pixels. It also asserts that an incompatible fixture causes no Start,
Cancel, Resume, or generic Retry request and that history/purge rendering makes
no network request for deleted evidence merely to recover survivor provenance.
The crash-during-recovery fixture schema assertion requires
`recovery_sessions[]` to be sequence-ordered, rejects a duplicate
`recovery_id`, missing full identity/decision/prefix evidence, a derived status
outside `superseded | active | manual_intervention | complete`, more than one
accepted `run.interrupted`, an action finish without its stable write-ahead
start, or conflicting dispositions for one step. It verifies reducer equality
for full replay versus every valid snapshot-plus-reconnect suffix.

## 8. Responsive layout specification

| Width | Shell | Catalog | Run | Overlay behavior |
|---:|---|---|---|---|
| 1440 | 224 px nav rail | 280 px filters + fluid results + 320 px tray | 40/60 split | Preview 800–900 px drawer; Health 480 px drawer |
| 1024 | Compact top navigation | Filter drawer; result + 300 px tray until result would be below 520 px | Two panes with compact header | Tray may become drawer; preview remains large drawer |
| 768 | Compact labeled navigation | One column; filter drawer; sticky 44 px selection summary | Case list then selected detail with sticky Back to cases | Selection and preview use bottom/full-screen drawers |
| 390 | Compact labeled navigation | One column; full-screen filters/selection; wrapping metadata and counts | Summary, first failure, cases, then detail | Filters, preview, and evidence detail are full-screen |
| 375 | Same complete flow as 390, independently tested for minimum-width clipping | No clipped controls, counts, or metadata | No hidden connection, cleanup, or first-failure state | Same as 390 with minimum-width verification |

At every required width:

- there is no page-level horizontal scrolling;
- body text, headings, counts, paths, and actions do not clip;
- every pointer target is at least 44 by 44 CSS pixels;
- long logs/code scroll only inside labeled regions;
- wide evidence tables provide a card/detail alternative;
- selected counts and the active primary action remain reachable;
- status, stream freshness, first failure, cleanup, and evidence health remain
  visible;
- loading regions reserve space to avoid disruptive layout shift.

At 200% browser zoom the same workflows remain operable without lost,
overlapping, clipped, or unreachable content. Internal panels stack using the
same narrow-layout contracts; the page itself never scrolls horizontally.

## 9. Accessibility and keyboard behavior

- A skip link targets the main route content.
- Native links, buttons, checkboxes, headings, lists, tables, details/summary,
  dialogs, and form labels are preferred.
- Search is the first focusable control after the Catalog heading.
- Tab order follows visual order; there is no positive tabindex.
- Drawers/dialogs trap focus while modal, Escape closes when safe, and focus
  returns to the invoking control.
- Tri-state parent selection announces checked, not checked, or mixed and its
  affected clause meaning.
- Every icon-only control has an accessible name.
- Focus-visible indicators achieve at least 3:1 non-text contrast.
- Text meets WCAG 2.2 AA contrast; color is supplementary.
- Charts expose the same values and gaps in a table.
- Loading buttons expose progress and prevent duplicate submission.
- Errors use role=alert. High-frequency progress uses one throttled polite live
  region.
- Reduced-motion preference disables nonessential animation.
- Streaming updates do not move focus, reorder the focused row, or open panels.

## 10. Data-to-view mapping

| Projection or contract | UI owner | Required presentation |
|---|---|---|
| CatalogHealth | AppShell, Catalog, Runner Health | Revision, last-good/current state, checked time, diagnostics, admission eligibility |
| CatalogQuery response | Catalog | Normalized query, cursor, deterministic results, generic facets, explicit units |
| SelectionExpression | Selection tray | Ordered clauses, exclusions, revision, provisional estimate, stale/reconcile state |
| Expanded case contract | CaseRow, Test detail, Preview | Discriminated `catalog_kind`; shared stable identity/purpose/owner/named validations/policies/lifecycle; Product-only topology, feature mappings, and required six-surface proof; optional Harness surface; exact no-surface diagnostic copy plus `product_boundary_claim=not_applicable` |
| ExecutionSurfaceDescriptor and BoundaryAttestation | Catalog, Test detail, Preview, Run, Runs | Immutable manifest-frozen surface; exact derived proof label; expected driver/privilege/boundary; observed attestation and evidence reference; no UI override; mismatch as `Error · contract` |
| RunPreview | Preview dialog | State, exact ordered frozen cases, policies, resources, preflight, blockers including any controller-recovery admission lock, expiry, lineage |
| RunProjection | Run, Runs | Frozen identity, state counts, timing quality, stream watermark, fail-fast/cancel/cleanup/recovery; sequence-ordered append-only `recovery_sessions[]` with full controller identities, decisions, prefixes/actions, and derived canonical statuses; and either expected/observed surface proof or the frozen no-surface Harness boundary claim |
| RecoveryCompatibilityOverlay | Run, Preview, AppShell, Runner Health | Current non-authoritative exact-match/mismatch decision; complete admission/current bundle identity references and digest equality evidence; typed reason/action; historical-last-valid labeling and global admission effect |
| Current recovery overlay | Run, AppShell, Runner Health | Label one derived `active` session Current only when its complete controller/lock identity matches the direct API's verified current writer; otherwise label persisted activity with current ownership absent or unknown and never infer it |
| HistoryProjectionHealth | AppShell, Runs, Runner Health | `state=ready | rebuilding | stale | error`, `serving_last_good`, generation/timestamps/counts/reason, explicit `history_incompatible`, and direct known-run independence |
| Failure record | FirstFailureBanner, Failure panel | First versus primary, kind/reason, phase, correlation, source, causal sequence, evidence refs |
| Validation projection | Validation row/detail | Purpose, mapped features, phase/state, timing, expected/actual/error, evidence interval |
| EvidenceHealth/channel summary | Evidence inspector | Role, `collection_state=scheduled | collecting | finalizing | finalized`, separate final availability, provider, units, coverage, gaps/drops/caps/reason |
| Workspace/retention projection | Workspaces, Run | Server-derived E2E and benchmark workspace roots; fixed direct E2E children `testbed/`, `attempts/`, `quarantine/`, `tmp/`, `runs/`, `catalog/`, and `tooling/`; read-only source roots; leaf lifecycle/lineage; marker verification; digest/size only when verified; cleanup, reuse and purge eligibility; retention mutation identity from its separate stream/sequence and event producer revision |
| Health projection | Runner Health | Named checks, state, checked time, diagnostic, selection-specific admission effect, per-surface readiness including console-only dependency failure, recovery |

The UI uses server-derived timing quality. It does not imply subsecond precision
when clocks cannot be correlated or when only wall-clock time is trustworthy.

## 11. Generic rendering and scale

### 11.1 Genericity boundary

The following additions must render without a frontend source change:

- a case in an existing group;
- a new group or family;
- an E2E-only domain;
- a feature;
- an optional validation using the existing lifecycle;
- a Compound scenario or complexity;
- a runnable `catalog_kind=harness` case with or without an execution surface;
- an unfamiliar optional display token or bounded evidence object.

All taxonomy nodes render through one generic shape:

~~~text
kind + id + label + description + parent breadcrumb +
counts with units + optional display hints + health/runnable state
~~~

Unknown optional icons and accents use neutral fallbacks. Unknown lifecycle,
event, or schema semantics stop projection and display incompatibility.
Conditional fields do not become generic missing-data warnings: the renderer
branches only on the schema-owned `catalog_kind` discriminant. It requires
Product topology/features/mappings/surface proof for Product, forbids Product
topology/features/mappings for Harness, and uses the exact no-boundary copy plus
`product_boundary_claim=not_applicable` for surface-absent Harness records
without adding a Harness-specific page or executor.

### 11.2 Data-volume behavior

- Catalog and Runs fetch no more than 200 rows per cursor page.
- Virtualize list/table bodies above 100 visible records.
- Exact preview scope is complete server-side and browseable page by page; the
  browser never truncates the manifest selection.
- Event and telemetry requests page at no more than 1,000 records.
- The 10,000-case catalog and 100,000-event run fixtures are release tests.
- Timeline rendering uses windowing and level-of-detail summaries before raw
  event expansion.
- Telemetry charts decimate only for display and retain exact table/paged data.
- Log DOM is bounded; follow mode drops rendered nodes only after preserving
  cursor/position and explicit omission information.
- Search typing, Cancel, first-failure navigation, and current status are not
  blocked by background chart or log rendering.

## 12. Component map

| Component | Responsibility |
|---|---|
| AppShell | Navigation, skip link, truth banner, active run, Health trigger |
| CatalogRoute | URL query, generic filters, grouped/flat results |
| CatalogNode | Generic domain/family/group/scenario/complexity display |
| CaseRow | Match reason, case summary, feature provenance, selection |
| FeatureContext | Feature description and validation-claim summary |
| SelectionTray | SelectionExpression clauses/exclusions and preview entry |
| TestDetailRoute | Current case contract plus identified history |
| RunPreviewDialog | Exact scope, policies, preflight, admission |
| RunRoute | Shared live/history projection and actions |
| RunSummary | State/counts/timing/stream/cleanup/evidence overview |
| RecoveryCompatibilityPanel | Historical-last-valid state, complete controller identity disclosures, tuple/fixture decision evidence, typed action, and admission blockade |
| RecoverySessionsPanel | Current-or-ownership-unknown recovery statement, the single original run interruption, and sequence-ordered current/final/previous session provenance |
| FirstFailureBanner | First causal failure and deep-link actions |
| CaseList | Ordered generic cases and reasons |
| CaseInspector | Purpose, phases, validations, failures, timing |
| EvidenceInspector | Trace, metrics, logs, artifacts, critical interval |
| StreamStatus | Connecting/live/reconnecting/stale/offline and age |
| RunsRoute | Frozen run summaries, filters, projection health, last-good/unavailable states, and direct known-run entry |
| WorkspacesRoute | Read-only repository inputs, derived workspace roots, seven direct E2E children, capacity, and retained marker-owned leaves |
| WorkspaceDrawer | Lineage, safety, reuse, contextual actions |
| RunnerHealthDrawer | Readiness groups, history health, admission impact, recovery, and generic Harness Catalog entry |
| StateGallery | Visual fixtures for every truthful async/error state and catalog-kind view contract |

There is no RuntimePage, ManagerPage, ObservabilityPage, CompoundPage,
domain-card registry, domain route map, or validation-type plugin system.

## 13. Prototype disposition

The prototype's screenshots remain useful design references:

- [Catalog screenshot](../../../ephemeral-sandbox/e2e/ui-prototype/screenshots/catalog.jpg)
- [Test detail screenshot](../../../ephemeral-sandbox/e2e/ui-prototype/screenshots/test-detail.jpg)
- [Live run screenshot](../../../ephemeral-sandbox/e2e/ui-prototype/screenshots/live-run.jpg)
- [Runs screenshot](../../../ephemeral-sandbox/e2e/ui-prototype/screenshots/runs.jpg)
- [Workspaces screenshot](../../../ephemeral-sandbox/e2e/ui-prototype/screenshots/workspaces.jpg)

| Prototype element | Decision |
|---|---|
| Warm canvas, restrained blue, white cards, quiet borders | Reuse |
| Feature chips and direct/inherited distinction | Reuse with visible provenance |
| Validation rows and expected/actual layout | Reuse after separating declared contract from run evidence |
| Execution list and selected-case inspector | Reuse as generic Run split view |
| Phase trail and raw-log disclosure | Reuse with exact timing and truthful states |
| Workspace lineage and retained-root emphasis | Reuse |
| Hard-coded domain navigation/pages/counts | Remove |
| Catalog marketing/domain-card landing page | Replace with search/filter/select Catalog |
| Direct “Run” links | Replace with selection → Review run |
| Fabricated Runner ready/Live/Safe claims | Remove; fixture UI gets persistent Demo banner |
| Hidden stream/connection state at required widths | Remove; critical state stays visible |
| 7–11 pixel labels and clipped content | Replace with readable responsive type and wrapping |

The prototype must not be copied into production as a starting information
architecture. Reusing its CSS tokens and small visual primitives is acceptable.

## 14. UI acceptance criteria

### 14.1 Core journeys

1. **Feature discovery and admission**
   - Given a first-time user searches by feature label or description,
   - when three cases are selected across groups with one exclusion,
   - then the UI shows purpose, tag provenance, mapped validations, selection
     clauses, exact preview scope, workspace, telemetry, lane, fail-fast,
     resources, preflight, and cleanup before one Start action admits the run.

2. **Generic extension**
   - Given an unknown fifth domain, new family/group/feature, fourth Compound
     complexity, and unknown display hint in a supported schema,
   - when Catalog, detail, preview, and Run render,
   - then all are navigable with neutral fallbacks and no frontend source change.

3. **Selection revision**
   - Given selection revision A and catalog revision B removes or changes cases,
   - when the tray opens,
   - then it marks scope stale, explains changes, and requires reconciliation
     without silently changing clauses.

4. **Catalog/history truth**
   - Given a latest case result from an older revision,
   - when Catalog shows it,
   - then run ID, time, and revision are visible and it is not a Catalog result
     facet; Runs may filter the result normally.

### 14.2 Live execution and evidence

5. **Fail-fast while cleanup runs**
   - Given five serial cases and case 2 fails validation 3,
   - when cleanup is active,
   - then one case is passed, case 2 is nonterminal/cannot pass, cases 3–5 are
     causally Not run, first failure is pinned, and final verdict is pending.
   - After cleanup, final counts and applicable retry choices are visible.

6. **Additional teardown error**
   - Given an assertion followed by teardown error,
   - when the run terminalizes,
   - then the assertion remains first failure, teardown is an additional error,
     and terminal severity is Error.

7. **Disconnect truth**
   - Given disconnect after sequence N,
   - when the stream becomes stale,
   - then the last projection remains, timing freezes or says estimated/as of,
     focus remains stable, and reconnect resumes after N without duplicate
     counts or repeated first-failure announcements.

8. **Telemetry lifecycle**
   - Given a Runtime test before a cgroup identity exists,
   - then memory says Scheduled · waiting for resource, not Unsupported.
   - During sampling it says Collecting; during grace it says Finalizing; only
     the frozen summary receives a final availability.

9. **Degraded evidence**
   - Given Runtime assertions pass while memory samples become partial and logs
     truncate,
   - then the UI says “Passed · evidence degraded,” shows a gapped chart/table,
     last sample, coverage, omitted counts, and reason, never zero-filled data.

10. **Semantic incompatibility**
    - Given an unknown event semantic or unsupported schema major,
    - then updates stop, the last verified projection remains, an incompatibility
      error appears, and no unknown value maps to a neutral success-like status.

### 14.3 Responsive, accessible, and high-volume operation

11. At exactly 375, 390, 768, 1024, and 1440 CSS pixels, and separately at 200%
    browser zoom, the Catalog-to-preview and Run-to-first-failure journeys have
    no page-level horizontal overflow, clipped critical content, unreachable
    action, hidden stream/first-failure state, or pointer target below 44 by 44
    CSS pixels.
12. A keyboard-only user can search, facet, select mixed cases, review, start,
    locate first failure, inspect evidence, cancel, and review a retry. Focus is
    trapped/returned correctly and live updates never steal focus.
13. First failure is announced once; progress announcements are throttled;
    timers, logs, samples, and every event are not announced individually.
14. Every enabled search, filter, selection, preview, Start, Cancel, retry,
    copy, disclosure, recovery, and navigation control has an automated
    interaction test.
15. With 10,000 catalog cases, 373 selected/run cases, 100,000 events, and
    bounded maximum logs/telemetry, typing, scrolling, selection, Cancel, and
    first-failure navigation remain responsive and DOM growth remains bounded.
16. Count labels never combine cases, tests, validations, and features into an
    unlabeled total.
17. Axe and manual keyboard/zoom checks produce zero applicable WCAG 2.2 AA
    violations at all five required viewports; a tooling false positive has a
    reviewed documented exception and manual proof.

### 14.4 Demo and workspace truth

18. Given fixture data on any route, a persistent “Demo data — no runner
    connected” label is visible and no real Live, Ready, Safe, Start, Cancel, or
    connection claim is made.
19. Given the server is configured with `TEST_REPOSITORY_ROOT`, `PRODUCT_ROOT`,
    and `WORKSPACE_STORE_ROOT`, when Workspaces opens, it shows the exact Git
    repositories; derived read-only `e2e/` and `benchmark/` source roots;
    external derived `e2e` and `benchmark` workspace roots; and direct `testbed/`,
    `attempts/`, `quarantine/`, `tmp/`, `runs/`, `catalog/`, and `tooling/`
    children below the E2E workspace root. No browser setting, picker, URL/query
    parameter, or mutation field can submit, derive, or replace a root.
20. Given purge candidates consisting of either source root, either workspace
    root, each of the seven direct E2E child roots, an active leaf, an
    unmarked/unknown/outside entry, and one inactive marker-owned leaf projected
    as eligible, when Workspaces renders and mutation requests are exercised,
    only the eligible leaf exposes and completes Purge. Every other target is
    rejected by the controller and the adjacent reason remains visible.

### 14.5 V1 completeness and degraded history

21. **Runnable Harness admission**
    - Given `harness.docker.readiness/default` has
      `catalog_kind=harness`, `runnable=true`, the shared identity, owner,
      named-validation, policy, and lifecycle fields, and no Product topology,
      Product feature references, validation-to-Product-feature mappings, or
      execution surface, plus a separate non-runnable Harness diagnostic,
    - when a user activates Review runnable Harness cases in Runner Health or
      selects Catalog kind = Harness and Runnable = true in Catalog,
    - then the generic Catalog opens with shareable `catalog_kind=harness` and
      `runnable=true` filters and visible filter chips, and refresh/back/forward
      restore the server-backed query; its row and detail say “Harness
      diagnostic — no product boundary claimed” without empty Product sections,
      a feature gap, or an Unsupported surface.
    - The case passes through ordinary selection, exact Ready preview,
      preflight, Start, Run, evidence, cleanup, retry, result, and history
      components without a surface-specific check or invented CLI; it may Pass
      only after its required named validation, telemetry finalization, and
      cleanup complete. The preview, every case event, and terminal result carry
      `product_boundary_claim=not_applicable`; no surface driver, privilege,
      attestation, surface-specific preflight, or surface lifecycle event is
      emitted or rendered. The Catalog URL/filter, detail, preview, live result,
      retry, and history fixtures pass at 375, 390, 768, 1024, and 1440 pixels
      without clipping, a hidden status, or a Harness-only component.
    - The non-runnable case remains inspectable in Runner Health with its reason
      but cannot be selected. Product feature coverage excludes both records,
      and the browser contains no Harness-only route, executor, admission
      request, result renderer, or synthetic surface attestation.

22. **Exact telemetry collection lifecycle**
    - Given a channel that has not acquired resource identity, begins sampling,
      stops producers while draining buffered records, and completes its
      summary,
    - when its events and projections are replayed live and historically,
    - then the UI renders, in order, `scheduled`, `collecting`, `finalizing`,
      and `finalized`, never skips `finalizing`, never uses availability as a
      collection state, and shows final availability only with the finalized
      summary.

23. **History projection degradation and direct-run independence**
    - Given ready history, rebuilding history with and without a compatible
      last-good generation, stale last-good history, failed rebuild without a
      generation, and `history_incompatible`,
    - when each state is rendered on Runs, AppShell, Runner Health, and the
      fixture gallery,
    - then last-good rows remain filterable with generation/time warnings;
      unavailable states show Retry/diagnostics/Open known run and never “No
      runs”; incompatible state does not retry-loop; and an existing
      `/e2e/runs/:runId` deep link still renders its run without consulting the
      global history projection.

24. **Catalog-kind union enforcement**
    - Given valid Product fixtures for all six execution surfaces, a Product
      fixture missing topology/features/surface proof, and Harness fixtures
      containing a Product topology field, Product feature reference, or
      validation-to-Product-feature mapping,
    - when collection and every catalog-kind UI fixture run,
    - then valid Product rows/detail/preview/result show the exact expected and
      observed surface proof, mapping `cli` to `Real CLI → gateway`,
      `console_rpc` to `Console /api/rpc → gateway`, `console_http_proxy` to
      `Console HTTP proxy → daemon HTTP`, `gateway_rpc` to
      `Direct gateway RPC · internal`, `daemon_http` to
      `Direct daemon HTTP · console bypassed`, and `direct_daemon_rpc` to
      `Privileged daemon RPC · allowlisted`; each invalid record produces a local
      field/source diagnostic and is not selectable; the UI neither defaults
      Product to CLI nor strips the illegal Harness feature; and no Harness
      result contributes to Product feature coverage.
    - Given missing, duplicate, wrong-driver, or wrong-boundary observed proof,
      when the same fixture is rendered live and historically, then its terminal
      result is `Error · contract`, never Passed. DOM and request assertions show
      no surface picker, editable proof label, override field, or browser rewrite
      between catalog, preview manifest, events, retry, and result.

25. **Controller recovery identity and survivor provenance**
    - Given a direct-run fixture whose persisted projection is `running` through
      sequence 284 and whose current-controller overlay is `mismatch`, with
      complete, different admission/current `ControllerBundleIdentity@1`
      records, unequal bundle digests, typed reason/action, and a retained
      recovery lock,
    - when the Run route, Runner Health, AppShell active-run affordance, and any
      Ready-looking preview render at 375, 390, 768, 1024, and 1440 CSS pixels,
    - then the Run page says “Recovery blocked — controller bundle changed,”
      labels Running only as the historical last-valid state at sequence 284,
      freezes timing, shows no Live/current-running/Cancel/Resume claim, exposes
      both bundle digests and the exact equality-decision evidence, renders only
      the typed recovery action, and every preview Start
      is disabled with a link to the blocker. Automated request assertions prove
      that clicking Refresh or the diagnostic controls emits no Start, Cancel,
      Resume, shell-command, or generic recovery-Retry mutation.
    - Given the corresponding exact-bundle fixture terminalizes
      with recovery events, is then evidence-purged, and its retention events
      carry a third controller revision,
    - when the historical Run and workspace retention detail reopen without the
      purgeable artifacts,
    - then event detail attributes recovery events to their own
      `producer_revision`, the terminal survivor still exposes complete,
      separately labeled admission/recovery identities and the exact decision
      evidence, removed evidence is typed `evidence_purged`, and retention rows
      use their retention stream/sequence and producer identity. DOM/network
      assertions prove the UI neither substitutes the current controller nor
      fetches deleted artifacts to reconstruct survivor provenance.

26. **Console-down surface isolation**
    - Given sandbox-console is unavailable while the CLIs, gateway, daemon HTTP,
      privileged daemon RPC probe, catalog projection, and their own preflight
      checks are healthy,
    - when fixtures for all six surfaces are previewed independently and in a
      mixed selection,
    - then only `console_rpc` and `console_http_proxy` are Blocked with the named
      console dependency. `cli`, `gateway_rpc`, `daemon_http`, and
      `direct_daemon_rpc` remain eligible, their exact proof labels remain
      visible, and Catalog plus ordinary CLI flows issue no console health or
      runtime request. Runner Health calls the failure console-specific rather
      than globally blocking admission.

27. **Crash during recovery is resumable and non-duplicating**
    - Given a persisted journal in which `recovery-01` is registered, emits the
      run's only `run.interrupted` and one `recovery.action_started`, and
      crashes, then a different compatible controller registers `recovery-02`,
      reconciles that action with `recovery.action_finished`, appends only
      missing stable steps, and finishes the run,
    - when the pure reducer is exercised from sequence zero, from a materialized
      snapshot plus every valid event suffix, and with duplicate SSE delivery at
      every boundary, and the Run route renders each projection at 375, 390,
      768, 1024, and 1440 CSS pixels,
    - then every reducer result is byte-equivalent after canonical
      serialization; `recovery_sessions[]` contains exactly `recovery-01` then
      `recovery-02` with complete identities/decisions, with statuses
      `superseded` and `complete`; the result contains exactly one
      `run.interrupted`; validation,
      cleanup, telemetry, case, and run terminal counts are not duplicated; and
      first failure is announced once.
    - Before terminalization, while the verified overlay's full controller/lock
      identity matches the `active` `recovery-02`, only that entry is labeled
      Current. With no provable overlay it is labeled last persisted active with
      ownership unknown; after terminalization it is `complete` and labeled
      Final. `recovery-01` remains visibly `superseded`; prior
      sessions remain inspectable after purge, and DOM/network assertions prove
      no Resume, retry, Start, Cancel, or client-authored recovery mutation is
      offered or sent.
    - A static schema/event fixture accepts only
      `recovery.session_registered`, `recovery.action_started`, and
      `recovery.action_finished` for recovery-session bookkeeping, proves there
      is no session-finished event, and rejects any projection status outside
      `superseded | active | manual_intervention | complete`.

28. **Canonical repository/workspace boundary is static and operable**
    - Given a root projection with exactly `TEST_REPOSITORY_ROOT`, `PRODUCT_ROOT`, `WORKSPACE_STORE_ROOT`,
      `E2E_SOURCE_ROOT`, `BENCHMARK_SOURCE_ROOT`, `E2E_WORKSPACE_ROOT`, and
      `BENCHMARK_WORKSPACE_ROOT` in their canonical roles and paths, with only
      the first three configurable and the other four server-derived,
    - when Workspaces and Runner Health render at every required viewport,
    - then the test repository is visibly a Git repository; `e2e/` and
      `benchmark/` are its direct read-only source children; external store
      `e2e/` and `benchmark/` are its derived mutable roots; and
      E2E operational content occurs below exactly the direct `testbed/`,
      `attempts/`, `quarantine/`, `tmp/`, `runs/`, `catalog/`, or `tooling/`
      child. No path clips or becomes an editable/picker-backed value.
    - Runner Health shows pairwise root separation and marker verification; a
      failed guard blocks workspace initialization and admission instead of
      presenting a merely informational warning.
    - A static contract test parses production TypeScript root keys, root labels,
      configuration types, mutation request types, and route fixtures; it permits
      exactly these six root keys, permits configuration of only the two parent
      roots, and requires the exact six canonical fixture paths from this
      document. It fails on an additional configurable root, a path supplied by
      the browser, a source nested below a workspace root, an extra nested
      workspace layer, or a purge target other than one eligible marker-owned
      leaf.

## 15. Implementation handoff

Production UI work begins only after the catalog, annotation, preview, manifest,
execution-surface descriptor/attestation, event, reducer, telemetry, and
repository/workspace-boundary schemas required by Phase 7 are frozen.

The UI implementation order is:

1. AppShell, semantic tokens, status grammar, and StateGallery.
2. Catalog query, discriminated Product/Harness case rendering, generic nodes,
   and SelectionExpression tray.
3. Test detail, no-surface Harness URL/filter/detail fixture suite, and
   feature-filtered Catalog.
4. RunPreview checking/ready/blocked/stale flow with conditional surface proof.
5. Run summary, catalog-kind result/retry/history fixtures, controller-recovery
   compatibility/session/crash/survivor fixtures, ordered case list, first
   failure, and shared live/history detail.
6. Evidence inspector, synchronized interval, telemetry tables/charts, and logs.
7. Runs history with `HistoryProjectionHealth`, last-good, unavailable, and
   direct known-run states.
8. Workspaces and Runner Health, including source/workspace-root safety,
   surface-specific readiness, and the runnable Harness Catalog entry.
9. Responsive layout, keyboard, accessibility, high-volume, reconnect, and demo proof.

The first implementation review must compare the rendered pages against the
wireframes and acceptance criteria in this document, not against the static
prototype's hard-coded page structure.
