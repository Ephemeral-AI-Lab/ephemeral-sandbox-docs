# EphemeralOS E2E Control Room — Implementation Plan

| Field | Value |
| --- | --- |
| Status | **PASS AFTER RECONCILIATION** — implementation not started |
| Review date | 2026-07-13 |
| System contract | [e2e-test-system-spec.md](e2e-test-system-spec.md) |
| Technical design | [e2e-test-design.md](e2e-test-design.md) |
| UI design | [e2e-test-ui-design.md](e2e-test-ui-design.md) |
| Current product checkout | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox` |
| Planned test repository | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test` |
| Derived E2E state leaf | `<TEST_REPOSITORY_ROOT>/.e2e-state` (Git-ignored) |
| Derived benchmark state leaf | `<TEST_REPOSITORY_ROOT>/.benchmark-state` (Git-ignored) |
| Append-only delivery proof | `<E2E_STATE_ROOT>/TEST-REPORT.md` |

This plan is the destructive-review ledger and the smallest safe delivery order.
It does not authorize product, test, or Docker mutations. The review that produced
it was documentation-only and ran no live Docker E2E tests.

## 1. Executive verdict and stop/go rule

### 1.1 Verdict

The original proposal was directionally sound but too large to implement safely.
It mixed one necessary control plane with several speculative platforms:

- a catalog journal in addition to a current catalog and health record;
- multiple registries for one taxonomy;
- several projections that duplicated the event journal;
- a recovery-session subsystem separate from the run;
- a generalized telemetry and diagnostic-burst framework;
- UI-specific endpoints and frontend dependencies before measured need.

The rewritten design is **approved to implement only in the phase order below**.
The implementation must stop if a phase gate fails. Later-phase code must not be
used to hide an earlier contract failure.

### 1.2 One-sentence target

Build one catalog-driven path from typed pytest declarations to an immutable run
manifest, append-only event journal, pure run projection, and generic React UI.

### 1.3 Hard stop conditions

Implementation must not proceed past its current phase when any of these is true:

1. Full catalog collection starts a gateway, daemon, container, test workload,
   or writes below either source/product root.
2. Stable case IDs change because a file, class, or function is renamed.
3. A controller-bundle mismatch can cancel, clean, purge, or otherwise mutate a run.
4. Cleanup failures can be swallowed or represented as a passing run.
5. Previewed membership can differ from admitted manifest membership.
6. A purge path can escape an owned marker root or delete a protected root.
7. The UI invents state not present in the generic backend projection.
8. A new stored projection has no measured read-latency reason to exist.

## 2. Evidence and present baseline

The review read all four former documents and inspected source read-only. It found:

| Observation | Evidence | Consequence |
| --- | --- | --- |
| The planned test repository does not exist. | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test` is absent. | Repository extraction is real migration work, not a path rename. |
| The live suite remains in the product repository. | Read-only inventory on 2026-07-13 found 106 tracked `e2e` files, 75 Python files, and 275 `def test_` declarations. | Stable identity must be frozen before moving source; the former 373-expanded-case figure remains unverified migration orientation only. |
| Collection has live side effects today. | Current `e2e/conftest.py:34–47` has session writers and `:154–157` has autouse `gateway_up()` calling `gateway.ensure_up()`. | Phase 0 must make metadata collection provably read-only. |
| Cleanup can disappear. | Current `e2e/conftest.py:168–172` and `:217–225` catch and discard cleanup/harvest exceptions. | Cleanup aggregation is a release blocker. |
| Product catalog authority already exists. | `<PRODUCT_ROOT>/crates/sandbox-operations/catalog` is the authority and `crates/sandbox-console/src/catalog.rs:1` identifies the runtime `/api/catalog` projection. | Extend the existing authority with an offline projection; do not create another product catalog. |
| No offline product catalog export was found. | Source inspection found the runtime catalog path but no supported `--print-catalog` equivalent. | A small product-side offline export is a prerequisite. |
| Product boundaries are already distinct. | CLI, console RPC, console HTTP proxy, gateway RPC, daemon HTTP, and direct daemon RPC helpers exist. | Preserve six explicit surface names; share plumbing, not meaning. |
| The UI is only a visual prototype. | `e2e/ui-prototype/index.html`, CSS, and screenshots contain no controller integration. | Screenshots prove composition only, not behavior or accessibility. |
| The benchmark store contract differs today. | `benchmark/backend/src/config.rs:124–126,182` resolves a configurable root then appends `benchmark/`; `cleanup.rs:11` names `.eos-benchmark-owned`. | The fixed sibling-root contract needs an explicit migration, including double-nesting prevention. |

Counts above are orientation evidence, not acceptance baselines. The first authorized
implementation change must capture reproducible collection counts and stable IDs.

## 3. Prioritized findings and direct document edits

The “former location” column refers to the pre-rewrite documents reviewed on
2026-07-12. Every finding is resolved directly in the four rewritten documents.

| ID | Severity | Evidence | Violated principle | Impact | Rewrite applied | Acceptance proof |
| --- | --- | --- | --- | --- | --- | --- |
| F01 | P0 Blocker | Competing run authorities — former system spec §§14.2–14.3, design §§5.2–5.4, and plan §§4 and 10.1. | One owner per fact. | Per-case results, summaries, and recovery projections can disagree with `events.jsonl` after a crash. | System spec §10 and design §§4.5–4.7, 7, and 11 now make `manifest.json` + one retained `events.jsonl` authoritative and `run.json` the only projection. | Delete `run.json`, replay events, and compare byte-equivalent normalized output. |
| F02 | P0 Blocker | Recovery equality contradicted “compatible” recovery — former system spec §§8.3, 10.5, and acceptance criterion 16b. | Failure stays truthful. | A different controller could mutate an in-flight run under a loose compatibility claim. | All documents require exact controller-bundle digest equality; mismatch is read-only. | A mismatch attempt appends no event, signals no process, and performs no action. |
| F03 | P0 Blocker | Former UI design §7.1 used `compatible/incompatible` while the backend used `exact_match/mismatch`. | One owner per fact; failure stays truthful. | Frontend translation could enable the wrong recovery action. | UI design §§7.6 and 11 use only `exact_match` and `mismatch`, with exact user copy. | Contract fixtures cover both values and disabled controls. |
| F04 | P0 Blocker | Former system spec §§4–5 assumed offline collection; current `e2e/conftest.py:34–47,154–157` has session writers and an autouse live `gateway_up()`. | Source is not state; runtime boundaries stay real. | Catalog refresh could write reports or start infrastructure. | System spec §6.1 and design §5.2 establish a dedicated catalog mode evaluated before live session behavior. | Process, network, filesystem-write, and Docker spies observe zero live operations during full collection. |
| F05 | P0 Blocker | Current `e2e/conftest.py:168–172,217–225` catches and discards cleanup/harvest exceptions. | Failure stays truthful. | A run could appear clean and passing while resources leak. | System spec §§9–10 require structured cleanup events and failure precedence; Phase 0 removes silent handling. | Inject multiple cleanup failures and verify aggregation plus a non-pass terminal state. |
| F06 | P0 Blocker | Former design §§7.2–7.3 could resolve selection once for preview and again for admission. | One owner per fact. | The operator could review one case set and run another after catalog drift. | System spec §7 and design §6 admit by preview ID and digest, copying exact membership into the manifest. | A drifted catalog rejects a stale preview instead of recomputing it. |
| F07 | P1 Critical | Former system spec §4 maintained separate taxonomy and feature registries. | One owner per fact; ordinary growth is data-driven. | One feature edit touched multiple hand-maintained authorities. | `e2e/metadata/catalog.yaml` owns Compound and Harness metadata; Manager, Runtime, and Observability hierarchy comes from Rust. | A metadata-only Compound/Harness family and a Rust-owned Product family each appear without controller or UI edits. |
| F08 | P1 Critical | Former system spec §14.3 and design §6 exposed case, feature, tree, detail, validation, and recovery endpoints. | The UI consumes projections. | Per-row joins and resource-specific routes create N+1 calls and API/UI change amplification. | Design §12 exposes fourteen generic routes, with run state composed in one projection and two bodyless controller actions for catalog refresh/template preparation. | The full UI journey stays within implementation plan §9 round-trip budgets. |
| F09 | P1 Critical | Former system spec §§8.3, 10.5 and design §10 made recovery sessions a second workflow. | One owner per fact; delete before adding. | Session files and recovery projections duplicate journal state and add crash cases. | Recovery is an event-backed action plan on the run; no recovery-session authority exists. | Repeating an action is idempotent and replay yields the same projection. |
| F10 | P1 Critical | Former system spec §11, design §9, and plan Phase 6 proposed a general telemetry platform. | Delete before adding. | High-rate channels and burst profiles dominate implementation before demonstrated user value. | Evidence v1 keeps structured results, bounded logs/artifacts, and optional low-rate resource summaries. | Richer telemetry remains blocked until a named incident cannot be diagnosed with v1 evidence. |
| F11 | P1 Critical | Former system spec §14.2, design §5.4, and plan §10.1 required a global history index. | Future-proof means low change amplification. | Another mutable database must be reconciled after partial writes. | History scans bounded `run.json` headers; a disposable index is allowed only when supported-count scan p95 exceeds 500 ms. | Benchmark at the supported retained-run count before adding an index. |
| F12 | P1 Critical | Former system spec §4.7 and design §3.1 disagreed on `core`, `control`, `schemas`, and UI-specific service trees. | Obvious dependency direction; source is not state. | Ownership changed depending on which document a contributor read. | Both documents use canonical `manager`, `runtime`, `observability`, and `compound` areas beside `metadata`, co-located `harness` implementation/diagnostics, and `web`; no `internal` bucket exists. | A tree/path check rejects unapproved buckets and catalog/path disagreement. |
| F13 | P1 Critical | Former UI design §§7, 9, and 14.5 exposed recovery files, telemetry modes, and storage machinery. | The UI consumes projections. | Operators had to understand backend implementation rather than run truth. | UI design uses Catalog, Runs, and Workspaces navigation plus a Health drawer. | A first-time journey completes without storage or pytest vocabulary. |
| F14 | P1 Critical | Implementation plan §2 verifies `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test` is absent, while the former documents treated it as present. | Source is not state; paths aid navigation. | Migration steps could write into an absent or wrong Git root. | Every document labels the repository planned; Phase 1 creates and validates it before source moves. | Canonical root, Git identity, disjointness, and marker checks pass before migration. |
| F15 | P1 Critical | Current `benchmark/backend/src/config.rs:124–126,182` appends `benchmark/`; `cleanup.rs:11` uses `.eos-benchmark-owned`; the former migration was implicit. | Source is not state; purge containment. | Configuration could create `benchmark/benchmark` or target the wrong marker. | System spec §4 and design §3 isolate benchmark migration from E2E ownership. | Fixtures cover old root, new root, double nesting, aliasing, and marker mismatch. |
| F16 | P2 Major | Former design §3.9 and UI §2.4 selected table, virtualizer, plot, and state libraries without measurements. | Delete before adding. | Dependency weight and competing client state arrive before a proven need. | UI uses React, TypeScript, Mantine, Router, Query, and native `EventSource`. | Add a dependency only with a measured native/component failure. |
| F17 | P2 Major | Former UI introduction and acceptance language treated prototype screenshots as behavioral evidence. | Failure stays truthful. | Static visuals can hide keyboard, stream, state, and responsive failures. | UI design introduction and §16 explicitly limit the prototype to visual reference. | Automated interaction, responsive, and accessibility tests replace screenshot inference. |

## 4. Before and after architecture

### 4.1 Former shape

```text
Rust catalog ─┐
taxonomy.yaml ├─> catalog builds + journal + health
features.yaml ┘                │
pytest collection ─────────────┘
          │
          ├─> preview resolution
          ├─> execution-input manifest
          ├─> manifest
          ├─> events journal
          ├─> per-case result files
          ├─> run projection
          ├─> global run summaries
          ├─> recovery session projection
          └─> generalized telemetry projections
                         │
                 many domain endpoints
                         │
                 dependency-heavy UI
```

This shape amplified every identity, state, retention, and recovery change.

### 4.2 Rewritten shape

```text
Rust Product catalog ──offline export──┐
                                      ├─> side-effect-free full collection
one E2E catalog.yaml ──────────────────┘              │
                                                     v
                                  catalog/current.json + health.json
                                                     │
                                      selection -> immutable preview
                                                     │ exact digest + members
                                                     v
                                            manifest.json
                                                     │
                                       runner -> events.jsonl
                                                     │ pure replay
                                                     v
                                               run.json
                                                     │
                                  generic HTTP/SSE API -> generic React UI
```

### 4.3 Authority table

| Fact | Sole authority | Derived consumer |
| --- | --- | --- |
| Product taxonomy, operation, feature, and route identity | Rust product catalog projection | Collected catalog |
| Compound and Harness hierarchy/descriptive metadata | `e2e/metadata/catalog.yaml` | Collected catalog |
| Case declaration and stable ID | Typed pytest declaration | Collected catalog |
| Current usable catalog | `catalog/current.json` | Preview API and Catalog UI |
| Catalog build health | `catalog/health.json` | Health drawer |
| Admitted membership and policy | `runs/<id>/manifest.json` | Runner and run projection |
| Durable run facts | `runs/<id>/events.jsonl` | Reducer |
| Read-optimized run state | `runs/<id>/run.json` | API/UI; replaceable |
| Retention actions | `runs/<id>/events.jsonl` | Run/evidence availability |
| Evidence bytes | `runs/<id>/evidence/` | Evidence endpoint |

## 5. Simplicity ledger

### 5.1 Keep

| Element | Why it earns its place |
| --- | --- |
| Existing Rust product catalog authority | Prevents product operation identity from drifting into test metadata. |
| One E2E metadata file | Gives Harness and Compound metadata one obvious descriptive authority. |
| Stable explicit case IDs | Survive source moves and refactors. |
| Full collection in a dedicated offline mode | Expands parametrization without importing a second test parser. |
| One immutable manifest | Freezes exactly what the operator approved. |
| One append-only event journal | Gives crash recovery and auditability a single truth. |
| One pure projection | Makes live and historical UI read the same shape. |
| Source snapshot/digests | Explains the exact code and metadata admitted. |
| Exact-bundle recovery | Makes mutation authority unambiguous. |
| Scoped evidence health and retention events | Keeps missing/corrupt/purged evidence truthful. |
| Six explicit execution surfaces | They are different product boundaries, not presentation variants. |
| One serial lane and one active run in v1 | Matches the initial operating model and avoids a scheduler. |

### 5.2 Delete now

| Deleted element | Replacement |
| --- | --- |
| Catalog generation journal | Atomic current catalog plus health record. |
| Separate taxonomy and feature registries | One E2E catalog file plus Rust Product projection. |
| Execution-input manifest | Source digests embedded once in the admitted manifest. |
| Per-case `result.json` files | Case state in the event journal and run projection. |
| Global `run-summaries.json` | Bounded directory scan of run projections. |
| Recovery session files | Recovery actions appended to the run journal. |
| Retention projection and second retention journal | `retention.state` events in the permanently retained `events.jsonl`, reduced into `run.json`. |
| Diagnostic-burst profile and channel framework | On-demand bounded evidence fetch. |
| Case/feature/detail-specific endpoints | Catalog and run resources with generic filters. |
| Separate frontend event/state store | Server projection cached by Query; ephemeral view state stays local. |
| TanStack Table, Virtual, uPlot, charting, and state-machine packages | Mantine primitives, CSS, native lists, and `EventSource`. |

### 5.3 Defer behind measurements

| Deferred capability | Admission trigger |
| --- | --- |
| Derived history index | Run-directory scan p95 is over 500 ms at the supported retained-run count. |
| Row virtualization | Representative low-end browser misses the UI responsiveness budget at 1,000 admitted cases. |
| Charts | A named operator decision cannot be made from values, trends, and status summaries. |
| High-rate resource telemetry | A real incident is not diagnosable from structured results, logs, artifacts, and low-rate summaries. |
| Parallel execution lanes | Serial throughput misses a written operational SLO and isolation is proven. |
| Remote/multi-user service | A concrete deployment and authorization requirement exists. |
| Pluggable executors | A second real executor exists with incompatible lifecycle semantics. |

## 6. Change amplification and auto-loading proof

Predicted touch counts are design budgets. Exceeding one requires an architecture
review before implementation continues.

|   # | Extension attack                                   | Exact authoritative edits                                                                                                                                              | Derived path; no hand edit                                                                                                               |                     Maximum hand-edited files/components |
| --: | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------: |
|   1 | Add a parameterized case to an existing test       | Existing test declaration supplies one stable `case_id` and bounded parameter summary.                                                                                 | Collector expands it; current catalog, preview, run fixtures, and generic UI consume it.                                                 |                                                        1 |
|   2 | Add a test to an existing group                    | New test file/declaration only.                                                                                                                                        | The existing group query includes it after refresh.                                                                                      |                                                        1 |
|   3 | Add a Harness diagnostic to an existing family   | New test declaration/file co-located under `harness/<family>`.                                                                                                         | Generic topology, facets, selection, and detail render it.                                                                               |                                                        1 |
|   4 | Add an E2E-owned Compound/Harness family          | One family record in `metadata/catalog.yaml` plus tests in the matching canonical path.                                                                                | No Rust, controller route, or UI component changes.                                                                                      |                  2 or more test files; 0 framework files |
|   5 | Add a Product domain legitimately owned by Rust    | Product catalog/implementation/tests plus E2E case declarations.                                                                                                       | Offline Rust projection supplies domain meaning; generic collector/UI consume it.                                                        | Product change set + test files; 0 E2E taxonomy/UI files |
|   6 | Add a feature and two validations                  | Product feature in Rust; test declaration names two validations and their mappings; reporter emits generic validation states.                                         | Existing reducer and validation list render both.                                                                                        |            2 authority/declaration files; 0 API/UI files |
|   7 | Add a Compound scenario and a complexity value     | One E2E-owned Compound scenario/complexity record in `metadata/catalog.yaml` plus declarations under `compound/<family>`.                                              | Complexity, subject domains, component roles, and shared context are catalog data; pytest remains the executor.                          |                  2 or more test files; 0 framework files |
|   8 | Rename or move test source without identity change | Move source and update imports only; keep `(test_id, case_id)`.                                                                                                        | Catalog source/node diagnostics change; deep links, history, and retry lineage do not.                                                   |                      Moved file + necessary import sites |
|   9 | Add duplicate ID or unknown reference              | The intentionally invalid test file only.                                                                                                                              | Collector aggregates diagnostics, writes health `stale`, preserves current catalog, blocks admission, and UI shows last-good plus error. |             1 invalid file; 0 catalog/UI authority edits |
|  10 | Change Product catalog input while controller runs | Legitimate Rust catalog source edit only.                                                                                                                              | Watcher coalesces one full recollection, atomic publication, revision notice, and one combined catalog refetch.                          |       Product change set; 0 controller/UI taxonomy files |
|     |                                                    |                                                                                                                                                                        |                                                                                                                                          |                                                          |

For a valid future test, the observable path is:

```text
save declaration
  -> coalesced input notification
  -> one complete side-effect-free collection
  -> validate one candidate
  -> atomically replace catalog/current.json
  -> publish one revision notification
  -> open UI invalidates and refetches its combined catalog query
  -> test appears without restart or frontend registration
```

If collection fails, only `catalog/health.json` changes. The last-good catalog
stays visible and identified by revision; admission is blocked until a matching
ready refresh succeeds. An observable browser contract test must cover both paths.

Any ordinary feature addition that requires a controller switch statement and a
frontend switch statement has failed the metadata-driven design.

## 7. Repository and folder assessment

### 7.1 Current classification

| Path | Classification | Action |
| --- | --- | --- |
| `<PRODUCT_ROOT>/crates/sandbox-operations/catalog` | Product authority | Keep; add a deterministic offline projection entry point. |
| `<PRODUCT_ROOT>/e2e` | Current live E2E source | Migrate every source asset after identity and collection safety gates, then delete this product-owned directory. |
| `<PRODUCT_ROOT>/e2e/ui-prototype` | Visual reference | Move to `<E2E_SOURCE_ROOT>/web/prototype`; never import or serve it as production architecture. |
| `<PRODUCT_ROOT>/benchmark/backend` | Product benchmark code | Keep unless a separate product extraction is approved. |
| `<BENCHMARK_STATE_ROOT>` | Derived mutable benchmark area | Create only with its own marker and protected-root validation; never infer an alternate root. |
| `<E2E_STATE_ROOT>` | Derived mutable E2E leaf | Create only with marker and protected-root validation. |
| `<TEST_REPOSITORY_ROOT>` | Absent planned repository | Create in Phase 1 with independent Git identity. |

### 7.2 Final source tree

```text
ephemeral-sandbox-test/
├── .git/
├── .gitignore                  # ignores .e2e-state/ and .benchmark-state/
├── README.md
├── pyproject.toml
├── package.json                 # only while the web build needs Node
├── package-lock.json
├── e2e/
│   ├── metadata/
│   │   └── catalog.yaml
│   ├── harness/
│   │   ├── catalog/
│   │   ├── runner/
│   │   ├── reducer/
│   │   ├── storage/
│   │   ├── api/
│   │   └── ui/
│   ├── manager/
│   │   └── management/
│   ├── runtime/
│   │   ├── command/
│   │   ├── file/
│   │   ├── daemon_http/
│   │   ├── network_isolation/
│   │   ├── reserved_paths/
│   │   ├── shell_security/
│   │   └── workspace_session/
│   ├── observability/
│   │   ├── snapshot/
│   │   ├── trace/
│   │   ├── events/
│   │   ├── cgroup/
│   │   └── layerstack/
│   ├── compound/
│   │   ├── configuration/
│   │   └── lifecycle/
│   ├── web/
│   │   └── prototype/           # migrated static visual reference; never production UI
│   └── conftest.py
└── benchmark/                 # non-product benchmark source, if migrated
```

Top-level `core`, `common`, `shared`, `utils`, `schemas`, `control`, `internal`, and
`services` buckets are prohibited unless a later concrete ownership review shows
that one has a stable purpose. Modules begin beside their consumer and are moved
only after a second real consumer appears.

Initial migration mapping is explicit:

| Current product-repository source | New test-repository source |
| --- | --- |
| `e2e/manager/management` | `e2e/manager/management` |
| `e2e/runtime/command` | `e2e/runtime/command` |
| `e2e/runtime/file` | `e2e/runtime/file` |
| `e2e/observability/test_observability.py` | split by declared case into `e2e/observability/{snapshot,trace,events,cgroup,layerstack}` |
| `e2e/runtime/{daemon_http,network_isolation,reserved_paths,shell_security,workspace_session}` | `e2e/runtime/<same-family>` |
| `e2e/config` | `e2e/compound/configuration` |
| cross-domain lifecycle cases | `e2e/compound/lifecycle` |
| reusable code in `e2e/core` | cohesive modules in `e2e/harness/<family>` |
| harness contract/diagnostic tests | co-locate beside their owner in `e2e/harness/<family>` |
| `.pytest_cache`, `__pycache__`, `repo`, and `test-reports` | do not migrate as source; regenerate only below `.e2e-state/` |
| `e2e/ui-prototype` | `e2e/web/prototype`; migrated visual reference, never production source |

### 7.3 Final mutable tree

```text
ephemeral-sandbox-test/
├── .e2e-state/
│   ├── root.json
│   ├── TEST-REPORT.md
│   ├── catalog/{current.json,health.json}
│   ├── runs/<run_id>/{manifest.json,events.jsonl,run.json,source/,evidence/}
│   ├── workspaces/{template,attempts,quarantine}/
│   ├── tooling/
│   └── tmp/
└── .benchmark-state/
    ├── root.json
    └── {fixtures,runs,results,runtime,tmp}/
```

The repository, product checkout, Git metadata, both source leaves, both state
leaves, markers, catalog directory, and run root are protected targets. Cleanup
and purge operate only on validated descendants selected by recorded ownership.

### 7.4 Directory ownership and purge boundaries

| Directory | Single purpose | Owner | Allowed contents | Purge boundary |
| --- | --- | --- | --- | --- |
| `<TEST_REPOSITORY_ROOT>/e2e` | Versioned E2E source | Test repository maintainers | Canonical test areas plus metadata, harness, web, and source configuration | Never runtime-purged |
| `e2e/metadata` | Compound topology, Harness diagnostic families, and shared descriptive definitions | Collector contract maintainers | `catalog.yaml` and its schema fixture only | Never runtime-purged |
| `e2e/harness` | Harness implementation plus co-located contract tests and diagnostics | Harness maintainers | `catalog`, `runner`, `reducer`, `storage`, `api`, and `ui` family children | Never runtime-purged |
| `e2e/manager` | Public Manager behavior | Manager test contributors | Rust-catalog family children; initially `management` | Never runtime-purged |
| `e2e/runtime` | Runtime product behavior across declared public and non-public execution surfaces | Runtime test contributors | `command`, `file`, `daemon_http`, `network_isolation`, `reserved_paths`, `shell_security`, `workspace_session` | Never runtime-purged |
| `e2e/observability` | Public Observability behavior | Observability test contributors | `snapshot`, `trace`, `events`, `cgroup`, `layerstack` | Never runtime-purged |
| `e2e/compound` | Cross-domain Product scenarios sharing context | Cross-domain test contributors | E2E-owned scenario-family children | Never runtime-purged |
| `e2e/web` | Generic Control Room UI | UI maintainers | React source, styles, generated types, UI tests | Build output goes to store/tooling; source never purged |
| `<TEST_REPOSITORY_ROOT>/benchmark` | Optional non-product benchmark source/config | Benchmark maintainers | Versioned benchmark inputs only | Never E2E-purged |
| `<E2E_STATE_ROOT>` | E2E mutable ownership leaf | E2E controller | `root.json`, `TEST-REPORT.md`, and five role directories | Leaf/root/marker/report never purged |
| `<E2E_STATE_ROOT>/TEST-REPORT.md` | Append-only phase/live-proof ledger | Delivery process | Commands, results, scoped artifact links, limitations | Protected; never an API/run authority |
| `<E2E_STATE_ROOT>/catalog` | Last-good catalog and health | Collector publisher | `current.json`, `health.json` | Files replace atomically; never user-purged |
| `<E2E_STATE_ROOT>/runs` | Run records | Run controller/retention writer | Validated run-ID directories | Only payloads in one terminal run; directory, manifest, projection, lineage retained |
| `<E2E_STATE_ROOT>/workspaces` | Template, attempts, quarantine | Workspace owner | Marker-owned semantic workspace leaves | Only an inactive exact owned descendant |
| `<E2E_STATE_ROOT>/tmp` | Staged atomic candidates | Owning controller process | Non-published bounded temporary files | Stale exact descendants only; never parent |
| `<E2E_STATE_ROOT>/tooling` | External build/tool caches | Tooling owner | Digest-addressed controller/web/probe outputs | Exact cache entry after liveness check; never source/product roots |
| `<BENCHMARK_STATE_ROOT>` | Benchmark mutable ownership leaf | Benchmark backend | `root.json` and benchmark role directories | Never E2E-purged; benchmark applies its own descendant rules |

There are no unresolved root-level source outliers. The current `ui-prototype`
moves with the suite to `e2e/web/prototype`; it remains visual reference material
only and may be deleted once the production UI supersedes it. No E2E source,
prototype, shim, or symlink remains in the product checkout.

## 8. Smallest ordered implementation sequence

Each phase should be a reviewable change set. No phase may prebuild a later
subsystem “for convenience.” Offline tests run throughout; live proofs are delayed
until their feature is individually complete.

### Phase 0 — Make the current suite safe to observe

Deliver:

1. A stable-ID ledger for every currently collected expanded case.
2. A dedicated catalog collection flag/mode evaluated before live session hooks.
3. Guards proving no gateway/daemon/container startup in that mode.
4. Structured cleanup aggregation replacing broad silent exception handling.
5. A reproducible current catalog/count snapshot used only as migration evidence.
6. A conversion inventory mapping every current expanded case to the required
   `@e2e_test(id, title, description, features, validations)` declaration and
   named `validation(...)` checkpoint reports; Phase 2, not this phase, adds
   those annotations and reports.

Acceptance criteria:

- [x] Full collection from an unrelated CWD produces no process, network,
  Docker, or filesystem write below either source/product root; any candidate
  output is confined to a declared test-owned temporary/state leaf.
- [x] Pre/post collection source-tree digests are byte-identical and no gateway,
  daemon, container, terminal-summary, or `atexit` writer runs.
- [x] Every expanded case has one unique explicit stable ID.
- [x] Injected cleanup failures remain visible and cannot produce a pass.
- [x] Focused existing tests prove ordinary current live behavior is unchanged.

Do not move files in this phase. A safe observer and stable identity must precede
repository extraction.

### Phase 1 — Establish roots and migrate source without changing identity

Deliver:

1. Create `<TEST_REPOSITORY_ROOT>` with independent Git identity and a minimal README.
2. Create only the source tree in §7.2.
3. Move E2E source while preserving stable IDs and import behavior.
4. Add canonical startup arguments for test and product roots only.
5. Derive fixed E2E/benchmark source and state children; reject aliases and containment.
6. Initialize the E2E store leaf only after exact marker validation.
7. Specify and fixture-test benchmark root migration, including double nesting.

Acceptance criteria:

- [x] Pre/post migration stable-ID sets are identical.
- [x] Imports and offline tests do not depend on CWD, home, or ambient root aliases.
- [x] `<PRODUCT_ROOT>/e2e` is absent after the move, with no compatibility link,
  duplicate tree, or product-source path discovery;
- [x] Destructive-path fixtures cannot target protected roots.
- [x] Benchmark tests cover old/new path interpretation without mutating live data.

### Phase 2 — Build one offline catalog

Deliver:

1. Deterministic Rust product catalog export with no runtime connection.
2. Split the Rust Observability catalog's generic family into `snapshot`,
   `trace`, `events`, `cgroup`, and `layerstack`, matching the public CLI.
3. Add the canonical Runtime capability families `command`, `file`,
   `daemon_http`, `network_isolation`, `reserved_paths`, `shell_security`, and
   `workspace_session` to the Rust catalog; each case still declares its actual
   execution surface.
4. The required `@e2e_test(id, title, description, features, validations)`
   declaration on every test and `validation(...)` reporting context for every
   named assertion checkpoint, plus one E2E `catalog.yaml` for Compound and
   Harness metadata.
5. Product/E2E ownership, canonical path, and stable-ID validation.
6. Full expanded collection in dedicated catalog mode.
7. Atomic `catalog/current.json` and `catalog/health.json` publication.
8. Last-good preservation when a refresh fails.

Acceptance criteria:

- [x] Identical inputs produce byte-equivalent normalized catalog output.
- [x] Duplicate IDs, orphan hierarchy, unknown surfaces, and missing required metadata fail.
- [x] An undecorated test, unknown/duplicate checkpoint report, or declared
  checkpoint with no terminal report fails collection;
- [x] Failed refresh changes health but not the last-good current catalog.
- [x] Adding a representative Harness leaf requires no controller/UI source edit.

### Phase 3 — Implement contracts, reducer, and storage offline

Deliver:

1. Immutable preview, manifest, event, run, retention, and evidence schemas.
2. Canonical serialization and digests.
3. Single-writer append/fsync rules for `events.jsonl`.
4. Pure reducer from manifest + events + retention to `run.json`.
5. Atomic projection replacement and startup replay.
6. Owned workspace attempt and quarantine primitives.
7. A regular-file-only source-snapshot copier/validator that rejects links,
   devices, sockets, FIFOs, unsafe modes, size/digest/tree-digest mismatch, and
   publishes an immutable run-owned snapshot.

Acceptance criteria:

- [x] Reducer property tests cover duplicates, truncation, reordered rejection, and restart.
- [x] Deleting `run.json` and replaying produces the same normalized projection.
- [x] Partial final-line recovery never invents success.
- [x] Snapshot fixtures reject links, devices, sockets, FIFOs, unsafe modes, and
  size/digest/tree-digest mismatches; the published snapshot is non-writable.
- [x] Marker, symlink, alias, traversal, and protected-root deletion tests pass.

### Phase 4 — Add preview, admission, runner, boundaries, and recovery

Deliver:

1. Query-clause and explicit-case selection with exclusions.
2. Exact preview membership, policy, preflight, digest, and expiration.
3. Admission transaction accepting only preview ID, one-use token, and
   idempotency key; it validates the lane/preflight/disk, snapshots only
   declared regular files, and publishes no run on a failed transaction.
4. One active serial pytest runner with cancellation and fail-fast causality.
5. Six explicit surface adapters with attestation.
6. Structured validation, cleanup, failure, log, artifact, and evidence events.
7. Child retry previews that resolve only frozen `failed`, `not_run`, or
   `failed_or_not_run` membership from one parent run and record lineage.
8. Exact-bundle recovery at controller startup, reduced into the same run
   projection before any recovery side effect.

Acceptance criteria:

- [x] Preview/catalog drift, stale/lane/empty/excess/disk failures, and arbitrary
  browser input are typed, non-mutating admission failures.
- [x] An admitted manifest contains exactly the previewed ordered case IDs, and
  source edits after admission cannot affect its immutable snapshot.
- [x] Same idempotency key plus digest returns one run; mismatched reuse returns 409.
- [x] Child retry previews include only the permitted frozen parent outcomes,
  never passed cases, and record `parent_run_id` lineage.
- [x] Each surface fixture proves the intended boundary and rejects false attestation.
- [x] On controller startup, an exact-match recovery writes its deterministic
  action plan before effects; a mismatch signals/mutates nothing and blocks
  admission; crashes at each action boundary are at-most-once or manual intervention.
- [x] Disconnect/restart replay preserves state and first/primary failure semantics.

Run focused live proofs only for the completed surface or lifecycle feature under
test. Do not rerun already passing live suites during feature iteration.

### Phase 5 — Expose the generic API and fixture-driven UI

Deliver:

1. The fourteen routes in design §12, including one run snapshot/SSE stream and
   bodyless controller actions for catalog refresh and template preparation.
2. Catalog browse/search, exact selection, review, and admission flow.
3. One run detail page used for live and historical runs.
4. Workspaces page and Health drawer.
5. The exact in-flight/error copy matrix from UI design §11.
6. Keyboard, focus, responsive, and reduced-motion behavior.
7. Automatic catalog-revision loading of a newly discovered valid `e2e/**`
   folder/test, with no UI registration, route, or component edit.

Acceptance criteria:

- [x] UI contract tests run first against fixtures for every state and transition.
- [x] Catalog presents Manager, Runtime, Observability, and Compound as primary
  catalog-derived cards, with Harness Diagnostics as a subordinate card;
- [x] Family navigation is generated from catalog data, including all seven initial
  Runtime families, five initial Observability families, and six Harness
  diagnostic families, with no frontend registry;
- [x] Catalog refresh and template preparation use their bodyless controller
  actions; browser code supplies no filesystem/execution values and does not
  auto-retry a mutation.
- [x] Host, exact Origin, memory-only nonce, no-CORS, artifact authorization,
  traversal, and evidence-safe 404/410/500 behavior have API contract tests.
- [x] Plain and encoded secret canaries are absent from durable evidence, SSE,
  API, and UI fixtures; caps expose omitted counts.
- [x] The primary journey stays within the roundtrip and measurement budget in §9.
- [x] Keyboard-only and automated accessibility checks pass at all five viewports
  and 200% zoom, with no page-level horizontal overflow or pointer target below 44 px.
- [x] SSE disconnect, gap, and refresh use one notification plus one snapshot refetch.
- [x] A new valid test/folder appears through the ordinary catalog refetch without
  a frontend source edit;
- [x] No UI code branches on a product feature or case ID.

### Phase 6 — Migrate the full family metadata

Deliver:

1. Migrate all Runtime-facing tests into `runtime/<family>`, regardless of
   public or non-public execution surface; migrate Manager and Observability
   tests into their catalog family paths; migrate only true shared-context
   cross-domain scenarios into `compound`; co-locate harness diagnostics under
   `harness/<family>`.
2. Convert all cases to stable typed declarations.
3. Add structured validation names and evidence roles where they carry meaning.
4. Remove legacy taxonomy and catalog shims only after parity.

Acceptance criteria:

- [x] Stable-ID ledger has no unexplained loss, duplication, or ownership change.
- [x] Every registered case is reachable through generic Catalog queries.
- [x] Every declaration agrees with its canonical source path.
- [x] No source family adds controller routes, reducer states, or UI components.
- [x] Collection remains side-effect-free for the full suite.

### Phase 7 — Focused live proof and release

Deliver proofs in this order:

1. one representative case for each execution surface;
2. failure, cancellation, fail-fast, and cleanup aggregation;
3. controller disconnect and exact-bundle restart recovery;
4. evidence missing, corrupt, purged, and optional cases;
5. disk admission/finalization reserve and retention behavior;
6. one final full eligible live suite after all focused proofs pass.

Acceptance criteria:

- [x] Each phase appends evidence to the test report.
- [x] Passing focused suites are not repeatedly rerun before final proof.
- [x] Final proof uses frozen toolchain, catalog, source, and policy digests.
- [x] Any remaining limitation names an owner, impact, and explicit non-claim.

## 9. Roundtrip and performance budget

| Operator action | Network budget | Local/render budget |
| --- | ---: | ---: |
| Open or filter Catalog | 1 catalog request per query/page change | Visible response within 100 ms after data arrival |
| Open case detail | 0 additional requests when case is in catalog response | Drawer within 100 ms |
| Review selection | 1 preview request | Exact count and ordered membership shown together |
| Start run | 1 admission request | Immediate admitted/rejected state |
| Follow live run | 1 snapshot request + 1 SSE connection | Event visible within 250 ms of receipt |
| Open evidence | 1 request on demand | Never prefetch all evidence |
| Receive catalog revision | 1 notification on the existing SSE stream + 1 catalog refetch | Open Catalog updates without restart or polling |
| Recover from stream gap | 1 notification + 1 snapshot refetch | No event-by-event repair protocol |
| Browse history | 1 runs request | Server scan p95 ≤ 500 ms at supported count |

The maximum admitted run is 1,000 expanded cases in v1. This bounds exact preview,
run projection, and non-virtualized list behavior. Raising it requires measurements
for reducer time, snapshot size, browser responsiveness, and SSE catch-up.

### 9.1 Measurement protocol

The report records the browser/version, operating-system and CPU/memory profile,
fixture revision, and whether the sample is cold or warm. Each budget is measured
with 5 warm-ups followed by 30 samples and reported as p95. Catalog fixtures contain
10,000 cases served in pages of 50 (never more than the API cap of 100); run fixtures
contain 1,000 admitted cases and an SSE catch-up boundary. Local timing starts when
the response/event is delivered to the client and ends at meaningful visible state;
network timing is reported separately. The five required viewports are 375, 390, 768,
1024, and 1440 CSS pixels, and every responsive proof also runs at 200% zoom.

### 9.2 Performance and accessibility acceptance criteria

- [ ] Catalog/filter and case-detail rendering meet the 100 ms p95 local budget
  against the declared 10,000-case paged fixture.
- [ ] Live event visibility meets the 250 ms p95 local budget against the declared
  1,000-case/SSE catch-up fixture.
- [ ] Retained-run directory scan meets the 500 ms p95 history budget at its
  supported fixture count.
- [ ] All five viewports at 200% zoom have no page-level horizontal overflow,
  hidden critical status, or target below 44 px; keyboard order, focus, reduced
  motion, and live-region behavior are covered by automated tests.

## 10. In-flight and error-state acceptance matrix

The detailed copy lives in UI design §11. This matrix is the implementation gate.

| State | Required operator truth | Allowed action | Forbidden implication |
| --- | --- | --- | --- |
| Catalog refresh running | Last-good catalog may still be displayed with refresh age | Continue browsing; inspect Health | Never call stale data newly refreshed |
| Catalog refresh failed with last-good | Error and last successful digest/time are visible | Request a coalesced refresh; browse last-good | Never clear a usable catalog |
| No usable catalog | Run creation is unavailable | Retry; inspect diagnostics | Never show an empty tree as success |
| Preview expired or catalog drifted | Reviewed membership is no longer admissible | Create a new preview | Never recompute and submit silently |
| Admission rejected | Run was not created; structured reason is shown | Correct cause; retry review | Never navigate to a fictional run |
| Run queued/running | Current phase, elapsed time, cases, and connection state are separate | Cancel when allowed | Never equate stream disconnect with run failure |
| SSE gap/disconnect | View may be stale; controller state is unknown until refetch | Reconnect/refetch | Never infer terminal state from silence |
| Recovery exact match | Controller-startup recovery executes its recorded idempotent action plan; the browser only observes progress | Wait, refresh, inspect | Never mutate merely because a page loads or expose a browser recovery-action route |
| Recovery mismatch | Run is inspectable but mutation is disabled | Start matching controller; inspect | Never offer cancel/cleanup/purge |
| Cleanup failed | Cleanup details and affected resources are visible | Retry eligible cleanup action | Never retain a green terminal badge |
| Evidence missing/corrupt/purged | Availability and reason are explicit | Retry only if producer/action permits | Never render absence as “no issues” |
| Purge in progress/failed | Run metadata remains and purge state is visible | Retry eligible purge | Never make the run disappear midway |
| Workspace quarantined | Reason, owner run, and safe action are visible | Inspect or purge exact descendant | Never offer parent-root cleanup |

## 11. Cross-document consistency proof

| Contract | System spec | Technical design | UI design | This plan |
| --- | --- | --- | --- | --- |
| Verdict and scope | §§1–2 | §§1–2 | §1 | §§1–3 |
| Fixed roots and ownership | §4 | §3 | Health/Workspaces in §§9–10 | §§2, 7, Phase 1 |
| Complete source extraction | §§2.2, 4, 13, 15.1 | §§1, 3, 15 | §1 | §§7, Phase 1, 12 |
| Product vs E2E metadata authority | §§5–6 | §§3–5 | Catalog in §§4–5 | Phases 0–2 |
| Selection and exact preview | §7 | §§4.3–4.4, 6 | Catalog/Review §§4–6 | Phase 4 |
| Immutable manifest | §§7.3, 10.1 | §§4.5, 6 | Review §6 | Phases 3–4 |
| Event authority and pure projection | §§9–10 | §§4.6–4.7, 7 | Run UI §7 | Phase 3 |
| Failure/cleanup precedence | §§9.3–9.4 | §9 | Run/matrix §§7, 11 | Phases 0, 4, 7 |
| Exact-bundle recovery | §11 | §9.4 | §§7.6, 11 | Phase 4 |
| Retry and controller actions | §§6.1, 7.2, 14 | §§4.3–4.5, 12 | §§6–7, 9–11 | Phases 4–5 |
| Snapshot/admission safety | §§7.3, 14–15 | §§4.5, 6, 14 | Review §6 | Phases 3–4 |
| Evidence v1 | §12 | §10 | §§7.5, 11 | Phases 4, 7 |
| Transport security and redaction | §§12, 14–15 | §§10, 12, 14 | §§11, 13, 16 | Phase 5 |
| Minimal API and SSE | §14 | §12 | Journeys §§4, 6–7 | Phase 5 |
| Generic UI and dependencies | §15.6 | §13 | §§2–16 | Phase 5 |
| Retention and purge | §§12.3, 13 | §11 | §§7–9, 11 | Phases 3, 7 |
| Roundtrip budget | §14 | §12 | §§4, 6–7, 15 | §9 |
| Deferred capabilities | §2.3 | §§11.1, 13 | §§3.3, 14 | §5.3 |

Consistency rules:

1. Wire enum names are copied, not translated, across backend fixtures and UI.
2. The API returns the reducer’s run projection; it does not assemble a second model.
3. Live and historical run pages consume the same snapshot shape.
4. The implementation plan may order work but may not weaken a specification invariant.
5. If a contract changes, the authority row, state matrix, phase gate, and fixture must
   change in the same review.

## 12. Release checklist

Release is allowed only when all boxes are evidenced:

- [ ] Full expanded collection performs no live infrastructure or source/product-tree write.
- [ ] Pre/post migration stable-ID sets match or every intentional difference is reviewed.
- [ ] `<PRODUCT_ROOT>/e2e` and all tracked product `e2e/**` paths are absent;
  no symlink, wrapper, duplicate source, or product-source path discovery remains.
- [ ] Catalog output is deterministic and preserves last-good on failure.
- [ ] Preview admission copies exact ordered membership and frozen policy.
- [ ] Admission accepts only preview/token/idempotency, keeps a failed transaction
  unpublished, and runs exclusively from a validated immutable source snapshot.
- [ ] Child retries use frozen failed/not-run membership and retain parent lineage.
- [ ] Event replay is deterministic after truncation and controller restart.
- [ ] Cleanup errors aggregate and prevent false pass.
- [ ] Every declared execution surface is attested at the real boundary.
- [ ] Exact-bundle mismatch is provably read-only.
- [ ] Exact-bundle recovery begins automatically at controller startup with a
  persisted deterministic action plan; page load never triggers mutation.
- [ ] Evidence health distinguishes available, optional, missing, corrupt, and purged.
- [ ] Evidence redaction/cap and Host/Origin/nonce/no-CORS/artifact authorization
  fixtures pass; browser mutations are never automatically retried.
- [ ] Purge and cleanup cannot target protected roots or cross ownership boundaries.
- [ ] Primary UI journey meets the network budget and requires no pytest knowledge.
- [ ] All UI in-flight/error states have contract, component, and accessibility tests.
- [ ] Performance proof records its environment and fixture, meets the 100/250/500 ms
  p95 budgets, and covers 10,000 catalog cases, 1,000 run cases, five viewports,
  and 200% zoom.
- [ ] No feature/case-specific controller route or UI branch exists.
- [ ] No deferred subsystem was added without its written measurement trigger.
- [ ] Focused live proofs pass before the one final full eligible suite.
- [ ] The four documents pass link, terminology, API, enum, and whitespace checks.

The first implementation change is Phase 0, not the control-room UI. A safe,
stable catalog view of the existing suite is the foundation every later screen and
recovery claim depends on.
