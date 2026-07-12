# EphemeralOS E2E Control Room — Implementation Plan

| Field | Value |
| --- | --- |
| Status | **PASS AFTER REWRITE** — implementation not started |
| Review date | 2026-07-12 |
| System contract | [e2e-test-system-spec.md](e2e-test-system-spec.md) |
| Technical design | [e2e-test-design.md](e2e-test-design.md) |
| UI design | [e2e-test-ui-design.md](e2e-test-ui-design.md) |
| Current product checkout | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox` |
| Planned test repository | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test` |
| Mutable store | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test-workspace` |
| Append-only delivery proof | `<WORKSPACE_STORE_ROOT>/e2e/TEST-REPORT.md` |

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

1. Full catalog collection starts a gateway, daemon, container, or test workload.
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
| The live suite remains in the product repository. | `<PRODUCT_ROOT>/e2e` contains 103 tracked files, 75 Python files, and 264 `def test_` declarations. | Stable identity must be frozen before moving source. |
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
| F07 | P1 Critical | Former system spec §4 maintained separate taxonomy and feature registries. | One owner per fact; ordinary growth is data-driven. | One feature edit touched multiple hand-maintained authorities. | `e2e/metadata/catalog.yaml` owns Harness/Compound metadata; Product hierarchy comes from the Rust projection. | A metadata-only Harness feature appears without controller or UI edits. |
| F08 | P1 Critical | Former system spec §14.3 and design §6 exposed case, feature, tree, detail, validation, and recovery endpoints. | The UI consumes projections. | Per-row joins and resource-specific routes create N+1 calls and API/UI change amplification. | Design §12 exposes twelve generic routes, with run state composed in one projection. | The full UI journey stays within implementation plan §9 round-trip budgets. |
| F09 | P1 Critical | Former system spec §§8.3, 10.5 and design §10 made recovery sessions a second workflow. | One owner per fact; delete before adding. | Session files and recovery projections duplicate journal state and add crash cases. | Recovery is an event-backed action plan on the run; no recovery-session authority exists. | Repeating an action is idempotent and replay yields the same projection. |
| F10 | P1 Critical | Former system spec §11, design §9, and plan Phase 6 proposed a general telemetry platform. | Delete before adding. | High-rate channels and burst profiles dominate implementation before demonstrated user value. | Evidence v1 keeps structured results, bounded logs/artifacts, and optional low-rate resource summaries. | Richer telemetry remains blocked until a named incident cannot be diagnosed with v1 evidence. |
| F11 | P1 Critical | Former system spec §14.2, design §5.4, and plan §10.1 required a global history index. | Future-proof means low change amplification. | Another mutable database must be reconciled after partial writes. | History scans bounded `run.json` headers; a disposable index is allowed only when supported-count scan p95 exceeds 500 ms. | Benchmark at the supported retained-run count before adding an index. |
| F12 | P1 Critical | Former system spec §4.7 and design §3.1 disagreed on `core`, `control`, `schemas`, and UI-specific service trees. | Obvious dependency direction; source is not state. | Ownership changed depending on which document a contributor read. | Both documents use only `metadata`, `harness`, `tests`, `web`, and `offline_tests` under `e2e`. | A tree check rejects unapproved top-level dumping-ground directories. |
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
| Product operation identity and hierarchy | Rust product catalog projection | Collected catalog |
| Harness hierarchy and descriptive metadata | `e2e/metadata/catalog.yaml` | Collected catalog |
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

| # | Extension attack | Exact authoritative edits | Derived path; no hand edit | Maximum hand-edited files/components |
| ---: | --- | --- | --- | ---: |
| 1 | Add a parameterized case to an existing test | Existing test declaration supplies one stable `case_id` and bounded parameter summary. | Collector expands it; current catalog, preview, run fixtures, and generic UI consume it. | 1 |
| 2 | Add a test to an existing group | New test file/declaration only. | The existing group query includes it after refresh. | 1 |
| 3 | Add a Harness group to an existing family | One record in `e2e/metadata/catalog.yaml` plus the new test declaration/file. | Generic topology, facets, selection, and detail render it. | 2 |
| 4 | Add an E2E-only family | One Harness family/group record in `metadata/catalog.yaml` plus tests. | No Rust, controller route, or UI component changes. | 2 or more test files; 0 framework files |
| 5 | Add a Product domain legitimately owned by Rust | Product catalog/implementation/tests plus E2E case declarations. | Offline Rust projection supplies domain meaning; generic collector/UI consume it. | Product change set + test files; 0 E2E taxonomy/UI files |
| 6 | Add a feature and two validations | Product feature in Rust **or** Harness feature in `catalog.yaml`; test declaration names two validations and their mappings; reporter emits generic validation states. | Existing reducer and validation list render both. | 2 authority/declaration files; 0 API/UI files |
| 7 | Add a Compound scenario and a complexity value | One E2E-owned Compound scenario/complexity record in `metadata/catalog.yaml` plus affected Product declarations. | Complexity, subject domains, component roles, and shared context are catalog data; pytest remains the executor. | 2 or more test files; 0 framework files |
| 8 | Rename or move test source without identity change | Move source and update imports only; keep `(test_id, case_id)`. | Catalog source/node diagnostics change; deep links, history, and retry lineage do not. | Moved file + necessary import sites |
| 9 | Add duplicate ID or unknown reference | The intentionally invalid test file only. | Collector aggregates diagnostics, writes health `stale`, preserves current catalog, blocks admission, and UI shows last-good plus error. | 1 invalid file; 0 catalog/UI authority edits |
| 10 | Change Product catalog input while controller runs | Legitimate Rust catalog source edit only. | Watcher coalesces one full recollection, atomic publication, revision notice, and one combined catalog refetch. | Product change set; 0 controller/UI taxonomy files |

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
| `<PRODUCT_ROOT>/e2e` | Current live E2E source | Migrate only after identity and collection safety gates. |
| `<PRODUCT_ROOT>/e2e/ui-prototype` | Visual reference | Keep temporarily; never import as production architecture. |
| `<PRODUCT_ROOT>/benchmark/backend` | Product benchmark code | Keep unless a separate product extraction is approved. |
| `<WORKSPACE_STORE_ROOT>/benchmark` | Current mutable benchmark area | Migrate explicitly; do not let either controller infer ownership. |
| `<WORKSPACE_STORE_ROOT>/e2e` | Planned mutable E2E leaf | Create only with marker and protected-root validation. |
| `<TEST_REPOSITORY_ROOT>` | Absent planned repository | Create in Phase 1 with independent Git identity. |

### 7.2 Final source tree

```text
ephemeral-sandbox-test/
├── README.md
├── pyproject.toml
├── package.json                 # only while the web build needs Node
├── package-lock.json
├── e2e/
│   ├── metadata/
│   │   └── catalog.yaml
│   ├── harness/
│   ├── tests/
│   │   ├── product/
│   │   ├── compound/
│   │   └── harness/
│   ├── web/
│   └── offline_tests/
└── benchmark/                 # non-product benchmark source, if migrated
```

Top-level `core`, `common`, `shared`, `utils`, `schemas`, `control`, and
`services` buckets are prohibited unless a later concrete ownership review shows
that one has a stable purpose. Modules begin beside their consumer and are moved
only after a second real consumer appears.

### 7.3 Final mutable tree

```text
ephemeral-sandbox-test-workspace/
├── e2e/
│   ├── root.json
│   ├── TEST-REPORT.md
│   ├── catalog/
│   │   ├── current.json
│   │   └── health.json
│   ├── runs/<run_id>/
│   │   ├── manifest.json
│   │   ├── events.jsonl
│   │   ├── run.json
│   │   ├── source/
│   │   └── evidence/
│   ├── workspaces/
│   │   ├── template/
│   │   ├── attempts/
│   │   └── quarantine/
│   ├── tooling/
│   └── tmp/
└── benchmark/
    ├── root.json
    ├── fixtures/
    ├── runs/
    ├── results/
    ├── runtime/
    └── tmp/
```

The repository, product checkout, store root, both leaf roots, Git metadata,
markers, catalog directory, and run root are protected targets. Cleanup and purge
operate only on validated descendants selected by recorded ownership.

### 7.4 Directory ownership and purge boundaries

| Directory | Single purpose | Owner | Allowed contents | Purge boundary |
| --- | --- | --- | --- | --- |
| `<TEST_REPOSITORY_ROOT>/e2e` | Versioned E2E source | Test repository maintainers | The five children below plus source configuration | Never runtime-purged |
| `e2e/metadata` | Harness topology, Compound definitions, and shared descriptive definitions | Collector contract maintainers | `catalog.yaml` and its schema fixture only | Never runtime-purged |
| `e2e/harness` | Collection, runner, adapters, reducer, store, and API implementation | Harness maintainers | Cohesive modules named in design §2 | Never runtime-purged |
| `e2e/tests` | Classification root for executable test source | Test contributors | Only `product`, `compound`, and `harness` children | Never runtime-purged |
| `e2e/tests/product` | Single-subject Product behavior tests | Domain test contributors | Tests and local helpers beside first consumer | Never runtime-purged |
| `e2e/tests/compound` | Cross-domain Product scenarios sharing context | Cross-domain test contributors | Scenario tests; component roles stay in declarations | Never runtime-purged |
| `e2e/tests/harness` | Infrastructure and Control Room diagnostics | Harness maintainers | No-coverage or explicit-boundary Harness tests | Never runtime-purged |
| `e2e/web` | Generic Control Room UI | UI maintainers | React source, styles, generated types, UI tests | Build output goes to store/tooling; source never purged |
| `e2e/offline_tests` | Framework contract proofs | Harness/UI maintainers | Collector, reducer, API, storage, and UI fixtures | Never runtime-purged |
| `<TEST_REPOSITORY_ROOT>/benchmark` | Optional non-product benchmark source/config | Benchmark maintainers | Versioned benchmark inputs only | Never E2E-purged |
| `<WORKSPACE_STORE_ROOT>/e2e` | E2E mutable ownership leaf | E2E controller | `root.json`, `TEST-REPORT.md`, and five role directories | Leaf/root/marker/report never purged |
| `e2e/TEST-REPORT.md` | Append-only phase/live-proof ledger | Delivery process | Commands, results, scoped artifact links, limitations | Protected; never an API/run authority |
| `e2e/catalog` | Last-good catalog and health | Collector publisher | `current.json`, `health.json` | Files replace atomically; never user-purged |
| `e2e/runs` | Run records | Run controller/retention writer | Validated run-ID directories | Only payloads in one terminal run; directory, manifest, projection, lineage retained |
| `e2e/workspaces` | Template, attempts, quarantine | Workspace owner | Marker-owned semantic workspace leaves | Only an inactive exact owned descendant |
| `e2e/tmp` | Staged atomic candidates | Owning controller process | Non-published bounded temporary files | Stale exact descendants only; never parent |
| `e2e/tooling` | External build/tool caches | Tooling owner | Digest-addressed controller/web/probe outputs | Exact cache entry after liveness check; never source/product roots |
| `<WORKSPACE_STORE_ROOT>/benchmark` | Benchmark mutable ownership leaf | Benchmark backend | `root.json` and benchmark role directories | Never E2E-purged; benchmark applies its own descendant rules |

There are no unresolved root-level source outliers. The current `ui-prototype`
remains a temporary product-repository visual reference until the production UI
supersedes it; it is not migrated as framework code.

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

Gate:

- full collection is side-effect-free under process, network, and Docker spies;
- every expanded case has a unique explicit stable ID;
- injected cleanup failures are visible and cannot produce pass;
- ordinary current live behavior is unchanged in focused existing tests.

Do not move files in this phase. A safe observer and stable identity must precede
repository extraction.

### Phase 1 — Establish roots and migrate source without changing identity

Deliver:

1. Create `<TEST_REPOSITORY_ROOT>` with independent Git identity and a minimal README.
2. Create only the source tree in §7.2.
3. Move E2E source while preserving stable IDs and import behavior.
4. Add canonical startup arguments for test, product, and store roots.
5. Derive fixed E2E and benchmark children; reject aliases and containment.
6. Initialize the E2E store leaf only after exact marker validation.
7. Specify and fixture-test benchmark root migration, including double nesting.

Gate:

- pre/post migration stable-ID sets are identical;
- imports and offline tests do not depend on CWD, home, or ambient root aliases;
- destructive-path fixtures cannot target protected roots;
- benchmark tests cover old/new path interpretation without mutating live data.

### Phase 2 — Build one offline catalog

Deliver:

1. Deterministic Rust product catalog export with no runtime connection.
2. Typed pytest metadata declarations and one E2E `catalog.yaml` for Harness and
   Compound metadata.
3. Product/Harness ownership and stable-ID validation.
4. Full expanded collection in dedicated catalog mode.
5. Atomic `catalog/current.json` and `catalog/health.json` publication.
6. Last-good preservation when a refresh fails.

Gate:

- identical inputs produce byte-equivalent normalized catalog output;
- duplicate IDs, orphan hierarchy, unknown surfaces, and missing required metadata fail;
- failed refresh changes health but not last-good current catalog;
- adding a representative Harness leaf requires no controller/UI source edit.

### Phase 3 — Implement contracts, reducer, and storage offline

Deliver:

1. Immutable preview, manifest, event, run, retention, and evidence schemas.
2. Canonical serialization and digests.
3. Single-writer append/fsync rules for `events.jsonl`.
4. Pure reducer from manifest + events + retention to `run.json`.
5. Atomic projection replacement and startup replay.
6. Owned workspace attempt and quarantine primitives.

Gate:

- reducer property tests cover duplicates, truncation, reordered rejection, and restart;
- deleting `run.json` and replaying produces the same normalized projection;
- partial final-line recovery never invents success;
- marker, symlink, alias, traversal, and protected-root deletion tests pass.

### Phase 4 — Add preview, admission, runner, boundaries, and recovery

Deliver:

1. Query-clause and explicit-case selection with exclusions.
2. Exact preview membership, policy, preflight, digest, and expiration.
3. Admission by preview ID/digest without recomputation.
4. One active serial pytest runner with cancellation and fail-fast causality.
5. Six explicit surface adapters with attestation.
6. Structured validation, cleanup, failure, log, artifact, and evidence events.
7. Exact-bundle recovery actions reduced into the same run projection.

Gate:

- preview/catalog drift is rejected;
- an admitted manifest contains exactly the previewed ordered case IDs;
- each surface fixture proves the intended boundary and rejects false attestation;
- mismatch recovery is read-only; exact-match actions are idempotent;
- disconnect/restart replay preserves state and first/primary failure semantics.

Run focused live proofs only for the completed surface or lifecycle feature under
test. Do not rerun already passing live suites during feature iteration.

### Phase 5 — Expose the generic API and fixture-driven UI

Deliver:

1. The twelve routes in design §12, including one run snapshot and SSE stream.
2. Catalog browse/search, exact selection, review, and admission flow.
3. One run detail page used for live and historical runs.
4. Workspaces page and Health drawer.
5. The exact in-flight/error copy matrix from UI design §11.
6. Keyboard, focus, responsive, and reduced-motion behavior.

Gate:

- UI contract tests run first against fixtures for every state and transition;
- the primary journey stays within the roundtrip budget in §9;
- keyboard-only and automated accessibility checks pass;
- SSE disconnect, gap, and refresh use one notification plus one snapshot refetch;
- no UI code branches on a product feature or case ID.

### Phase 6 — Migrate the full family metadata

Deliver:

1. Register remaining Product and Harness features against the new contracts.
2. Convert all cases to stable typed declarations.
3. Add structured validation names and evidence roles where they carry meaning.
4. Remove legacy taxonomy and catalog shims only after parity.

Gate:

- stable-ID ledger has no unexplained loss, duplication, or ownership change;
- every registered case is reachable through generic Catalog queries;
- no source family adds controller routes, reducer states, or UI components;
- collection remains side-effect-free for the full suite.

### Phase 7 — Focused live proof and release

Deliver proofs in this order:

1. one representative case for each execution surface;
2. failure, cancellation, fail-fast, and cleanup aggregation;
3. controller disconnect and exact-bundle restart recovery;
4. evidence missing, corrupt, purged, and optional cases;
5. disk admission/finalization reserve and retention behavior;
6. one final full eligible live suite after all focused proofs pass.

Gate:

- each phase appends evidence to the test report;
- passing focused suites are not repeatedly rerun before final proof;
- final proof uses frozen toolchain, catalog, source, and policy digests;
- any remaining limitation names an owner, impact, and explicit non-claim.

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

## 10. In-flight and error-state acceptance matrix

The detailed copy lives in UI design §11. This matrix is the implementation gate.

| State | Required operator truth | Allowed action | Forbidden implication |
| --- | --- | --- | --- |
| Catalog refresh running | Last-good catalog may still be displayed with refresh age | Continue browsing; inspect Health | Never call stale data newly refreshed |
| Catalog refresh failed with last-good | Error and last successful digest/time are visible | Retry refresh; browse last-good | Never clear a usable catalog |
| No usable catalog | Run creation is unavailable | Retry; inspect diagnostics | Never show an empty tree as success |
| Preview expired or catalog drifted | Reviewed membership is no longer admissible | Create a new preview | Never recompute and submit silently |
| Admission rejected | Run was not created; structured reason is shown | Correct cause; retry review | Never navigate to a fictional run |
| Run queued/running | Current phase, elapsed time, cases, and connection state are separate | Cancel when allowed | Never equate stream disconnect with run failure |
| SSE gap/disconnect | View may be stale; controller state is unknown until refetch | Reconnect/refetch | Never infer terminal state from silence |
| Recovery exact match | Same controller bundle may execute listed idempotent actions | Run one explicit action | Never auto-mutate merely on page load |
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
| Product vs E2E metadata authority | §§5–6 | §§3–5 | Catalog in §§4–5 | Phases 0–2 |
| Selection and exact preview | §7 | §§4.3–4.4, 6 | Catalog/Review §§4–6 | Phase 4 |
| Immutable manifest | §§7.3, 10.1 | §§4.5, 6 | Review §6 | Phases 3–4 |
| Event authority and pure projection | §§9–10 | §§4.6–4.7, 7 | Run UI §7 | Phase 3 |
| Failure/cleanup precedence | §§9.3–9.4 | §9 | Run/matrix §§7, 11 | Phases 0, 4, 7 |
| Exact-bundle recovery | §11 | §9.4 | §§7.6, 11 | Phase 4 |
| Evidence v1 | §12 | §10 | §§7.5, 11 | Phases 4, 7 |
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

- [ ] Full expanded collection performs no live infrastructure operation.
- [ ] Pre/post migration stable-ID sets match or every intentional difference is reviewed.
- [ ] Catalog output is deterministic and preserves last-good on failure.
- [ ] Preview admission copies exact ordered membership and frozen policy.
- [ ] Event replay is deterministic after truncation and controller restart.
- [ ] Cleanup errors aggregate and prevent false pass.
- [ ] Every declared execution surface is attested at the real boundary.
- [ ] Exact-bundle mismatch is provably read-only.
- [ ] Evidence health distinguishes available, optional, missing, corrupt, and purged.
- [ ] Purge and cleanup cannot target protected roots or cross ownership boundaries.
- [ ] Primary UI journey meets the network budget and requires no pytest knowledge.
- [ ] All UI in-flight/error states have contract, component, and accessibility tests.
- [ ] No feature/case-specific controller route or UI branch exists.
- [ ] No deferred subsystem was added without its written measurement trigger.
- [ ] Focused live proofs pass before the one final full eligible suite.
- [ ] The four documents pass link, terminology, API, enum, and whitespace checks.

The first implementation change is Phase 0, not the control-room UI. A safe,
stable catalog view of the existing suite is the foundation every later screen and
recovery claim depends on.
