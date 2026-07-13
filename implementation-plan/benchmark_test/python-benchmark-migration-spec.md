# EphemeralOS Benchmark Test — Python/TypeScript Migration Specification

| Field | Value |
| --- | --- |
| Status | Draft for implementation |
| Date | 2026-07-13 |
| Current source | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/benchmark` |
| Target source | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark` |
| Mutable state | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.benchmark-state` |
| Product checkout | supplied explicitly as `--product-root` |
| Backend language | Python only |
| Web language | TypeScript/JavaScript only |
| Backend test runner | pytest |
| Web test runners | Vitest and Playwright |

## 1. Decision

Move the benchmark laboratory out of the product repository and rewrite its
backend and runner in Python. Retain the React/TypeScript web application and
the existing `/api/v1` browser contract where practical. The target benchmark
tree must contain **no Rust source, Cargo metadata, Rust build step, or direct
dependency on an EphemeralOS source package**.

This is a contract-preserving rewrite, not a mechanical Rust-to-Python port.
Preserve benchmark semantics, safety, artifacts, and useful web workflows;
delete implementation complexity that exists only because the current runner
is embedded in a Rust workspace.

The target system is:

```text
React/TypeScript web
        |
        | same-origin HTTP + SSE
        v
FastAPI Python service
        |
        +-- plans, scheduling, fixtures, checks, artifacts, reports
        |
        +-- authenticated JSONL over asyncio TCP (timed path)
        |
        +-- prebuilt product executables (lifecycle/catalog only)
        v
isolated sandbox-gateway -> Docker-backed EphemeralOS daemon
```

## 2. Re-examined baseline

The current implementation is substantially larger than a test wrapper:

- the Rust backend has about 37,000 lines under `benchmark/backend/src`;
- the React/TypeScript application and browser tests have about 11,000 lines;
- the largest Rust areas are scheduling, reports, gateway lifecycle, artifacts,
  comparison, resource collection, and recovery;
- the backend directly depends on `sandbox-config`,
  `sandbox-operation-catalog`, `sandbox-operation-client`, and
  `sandbox-operation-contract` through the product Cargo workspace;
- direct product-crate use is concentrated in configuration, plans, fixtures,
  operation definitions, gateway transport, daemon sessions, and startup;
- the backend serves the built web application and `/api/v1` from one loopback
  origin and streams run events with SSE;
- the benchmark owns seven operations across Command, Files, Workspace
  Lifecycle, and LayerStack families;
- plans use deterministic seeds, randomized blocks, warmups, measured trials,
  per-operation timeouts, correctness checks, cleanup, and resource sampling;
- artifacts and append-only journals are a real compatibility surface, not
  disposable debug output;
- the product now has a deterministic offline `sandbox-catalog-export` binary,
  so Python does not need to copy or import the Rust operation catalog;
- the external E2E suite already proves the desired Python product boundary:
  explicit roots, subprocess lifecycle, authenticated raw gateway JSONL, pytest
  fixtures, and owned cleanup.

The E2E patterns should be reused selectively. The benchmark must not be
implemented as a large collection of pytest test functions: it is a benchmark
application with a web control plane, while pytest verifies that application.

## 3. Goals and non-goals

### 3.1 Goals

1. Make `/ephemeral-sandbox-test/benchmark` the only benchmark source tree.
2. Use Python for every backend, runner, report, and lifecycle component.
3. Use TypeScript/JavaScript for the web application.
4. Keep the benchmark independent of product-language packages and Cargo.
5. Preserve real Docker-backed execution through public product boundaries.
6. Preserve statistically meaningful measurements and reproducible plans.
7. Preserve the useful `/api/v1` and web workflows with minimal contract churn.
8. Preserve the ability to read historical Rust-produced artifacts.
9. Make source read-only during a run and keep all mutation under
   `.benchmark-state`.
10. Use pytest for Python unit, contract, integration, recovery, and live smoke
    tests.

### 3.2 Non-goals

- Do not translate every Rust type or abstraction one-for-one.
- Do not expose Python objects as a product integration boundary.
- Do not share an in-process gateway with the E2E suite.
- Do not measure CLI process startup as operation latency.
- Do not add a database, task queue, plugin system, ORM, generated client, or
  generalized executor framework.
- Do not redesign the web UI during the backend migration.
- Do not add distributed or multi-host benchmark execution in this migration.
- Do not make benchmark runs parallel at the campaign level. One active
  campaign remains the safety rule.

## 4. Mandatory language and dependency boundary

### 4.1 Zero-Rust invariant

The final `benchmark/` tree must contain none of the following:

- `*.rs`;
- `Cargo.toml`, `Cargo.lock`, `build.rs`, or `rust-toolchain*`;
- a Rust crate, workspace member, FFI module, PyO3 extension, or compiled Rust
  helper owned by the benchmark;
- a command that runs `cargo`, `rustc`, `rustup`, or `xtask`;
- a path dependency into `<PRODUCT_ROOT>/crates`;
- copied Rust product catalog or configuration source.

The product may itself be implemented in Rust. The benchmark interacts only
with already-built product executables and public network/file contracts, just
as an external client would.

A pytest guard must walk the complete benchmark source tree and fail on the
forbidden file names, suffixes, command tokens, Python imports, or package-path
dependencies. CI must run that guard before live tests.

### 4.2 Product boundary

The Python benchmark may use only:

1. explicit canonical paths supplied by `--product-root` and
   `--product-bin-dir`;
2. prebuilt executables from the product binary directory;
3. the JSON emitted by `sandbox-catalog-export`;
4. the authenticated gateway JSONL socket protocol;
5. documented daemon/gateway observability responses;
6. product version and binary hashes captured as provenance.

It must not:

- add `<PRODUCT_ROOT>` to `sys.path`;
- import product Python or Rust packages;
- parse Rust source to discover operations;
- walk upward from its own location to guess the product checkout;
- build the product during `serve`, `run`, pytest, or a timed campaign;
- silently fall back to a product source directory.

Missing or stale binaries are a preflight failure with a corrective command;
they are never repaired by the benchmark process.

## 5. Target technology stack

### 5.1 Python backend

| Concern | Choice | Reason |
| --- | --- | --- |
| Python | 3.13+ | Modern `asyncio.TaskGroup`, typing, and stable performance |
| HTTP/API | FastAPI | Strict typed requests and small route implementation |
| ASGI server | Uvicorn | Mature loopback server and graceful shutdown |
| Models | Pydantic v2 | Reject unknown fields and render stable JSON contracts |
| YAML | PyYAML | Already used by E2E and sufficient for strict plan data |
| Concurrency | `asyncio` | Raw socket timing and cancellation without thread frameworks |
| Persistence | `pathlib`, `json`, NDJSON, atomic replace | Existing artifact model needs no database |
| Statistics | Python standard library first | Preserves transparent algorithms and avoids native extensions |
| Backend tests | pytest + pytest-asyncio + HTTPX | Unit, async runner, and ASGI contract coverage |

`numpy`, `pandas`, `scipy`, Celery, Redis, SQLAlchemy, and a database are not
initial dependencies. Add NumPy only if a measured report-generation benchmark
shows that the exact 10,000-resample implementation misses an agreed runtime
budget. Measurement code and bootstrap seeds must not change merely to gain
speed.

### 5.2 Web

Keep the current React/TypeScript stack initially:

- React;
- TypeScript;
- Vite;
- Mantine;
- TanStack Query;
- React Router;
- uPlot;
- Vitest and Testing Library;
- Playwright and axe-core.

Do not rewrite the UI or replace these dependencies as part of the backend
migration. Move the web tree, update its real-backend launcher to start Python,
and change API types only when the versioned backend contract changes.

## 6. Repository and state layout

```text
ephemeral-sandbox-test/
├── pyproject.toml                     # existing E2E pytest configuration
├── e2e/
├── benchmark/
│   ├── README.md
│   ├── pyproject.toml                 # installable benchmark Python project
│   ├── defaults/
│   │   ├── standard-local.yml
│   │   ├── gateway.yml
│   │   └── workspace-profiles/
│   ├── presets/
│   ├── backend/
│   │   ├── benchmark_lab/
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py
│   │   │   ├── cli.py
│   │   │   ├── api.py
│   │   │   ├── app.py
│   │   │   ├── paths.py
│   │   │   ├── models.py
│   │   │   ├── catalog.py
│   │   │   ├── plans.py
│   │   │   ├── runner.py
│   │   │   ├── gateway.py
│   │   │   ├── transport.py
│   │   │   ├── operations.py
│   │   │   ├── fixtures.py
│   │   │   ├── checks.py
│   │   │   ├── resources.py
│   │   │   ├── artifacts.py
│   │   │   ├── events.py
│   │   │   ├── recovery.py
│   │   │   ├── statistics.py
│   │   │   ├── reports.py
│   │   │   └── compare.py
│   │   └── tests/
│   │       ├── unit/
│   │       ├── contract/
│   │       ├── integration/
│   │       ├── compatibility/
│   │       └── live/
│   └── web/                           # moved React/TypeScript application
│       ├── src/
│       ├── tests/
│       ├── package.json
│       └── vite.config.ts
└── .benchmark-state/                  # Git-ignored; only mutable benchmark root
    ├── .ownership.json
    ├── fixtures/
    ├── runs/
    ├── results/
    ├── runtime/
    └── tmp/
```

`benchmark_lab` is the Python import name to avoid collisions with generic
packages named `benchmark`.

The module list is a ceiling, not a requirement to create empty files. Begin
with fewer modules and split only when ownership becomes unclear or a file
becomes difficult to test.

## 7. Root and ownership contract

Startup requires exactly these canonical absolute roots:

- `--test-repository-root`;
- `--product-root`;
- `--product-bin-dir`.

Derive, without further overrides:

```text
BENCHMARK_SOURCE_ROOT = <TEST_REPOSITORY_ROOT>/benchmark
BENCHMARK_STATE_ROOT  = <TEST_REPOSITORY_ROOT>/.benchmark-state
```

The test and product repositories must be disjoint and neither may be an
ancestor of the other. The source root is read-only during validation and
execution. Every mutable path must resolve beneath the benchmark state root.

The state marker is exact JSON:

```json
{
  "owner": "ephemeral-sandbox-benchmark",
  "role": "benchmark-state",
  "schema_version": 1
}
```

Deletion is allowed only below an owned role directory after canonical path,
ancestor, symlink, and marker validation. The state root, marker, role
directories, source root, repository roots, and their ancestors are never
deletion targets.

Reuse the E2E root semantics, but do not import E2E runner or fixture modules.
The small benchmark `paths.py` remains independently runnable and has contract
tests that assert the same derived benchmark roots and marker shape as
`e2e/harness/storage/roots.py`.

## 8. Backend runtime design

### 8.1 Command line

Install one console command, `sandbox-benchmark`, with these commands:

```text
sandbox-benchmark serve
sandbox-benchmark validate --plan <path-or-preset>
sandbox-benchmark run --plan <path-or-preset>
sandbox-benchmark compare --reference <run-id> --candidate <run-id>
sandbox-benchmark recover
sandbox-benchmark cleanup --run-id <run-id>
```

`serve` is the normal interactive path and serves the built web assets and API
from one loopback origin. `run` is the non-browser CI path and uses the same
application service functions, not an alternate runner.

All commands accept the same explicit root options. Configuration precedence is
command line, environment, then a state-owned settings file. There is no sibling
workspace guess and no global user settings file.

### 8.2 HTTP and web serving

- Bind only to a loopback address.
- Serve `/api/v1` before the static fallback.
- Serve `benchmark/web/dist` as immutable static content in production.
- Inject a per-process cryptographic nonce into the bootstrap HTML.
- Require the exact same `Origin`, JSON content type, and constant-time nonce
  match for every state-changing request.
- Set `Cache-Control: no-store` for mutable API responses and bootstrap HTML.
- Do not enable CORS.
- Graceful shutdown requests cancellation, waits a bounded cleanup grace period,
  terminalizes the run truthfully, and then closes the server.

FastAPI route handlers validate input and delegate immediately to service
functions. They do not contain scheduling or artifact logic.

### 8.3 Campaign ownership

One process owns at most one active campaign. Admission is guarded by one
`asyncio.Lock`. A campaign uses:

- one immutable intent plan;
- one deterministic expanded plan;
- one cancellation event;
- one append-only event journal;
- one append-only observation journal;
- one owned isolated gateway process;
- a registry of created product resources for cleanup.

Do not introduce a worker queue. The campaign runs in one background asyncio
task owned by the ASGI lifespan. Blocking file and subprocess waits use
`asyncio.to_thread` only where necessary.

### 8.4 Run states

Preserve the current public state vocabulary:

```text
planned -> queued -> preparing -> running -> verifying -> tearing_down
                                                               |
                                                               v
                                                          completed

nonterminal -> cancelling -> cancelled
nonterminal ----------------> failed
```

Terminal states are `completed`, `failed`, and `cancelled`. Cleanup failure has
higher precedence than a passing workload: a run cannot be `completed` unless
all owned resources were removed and the cleanup baseline was restored.

### 8.5 Cancellation

Cancellation is cooperative and checked before every new family, cell, trial,
and request batch. In-flight network operations receive a bounded grace period.
After that period, their tasks are cancelled, but cleanup still executes under
`asyncio.shield` with its own timeout.

The API cancellation endpoint is idempotent. Repeating it cannot append
contradictory state or start a second cleanup path.

## 9. Product integration

### 9.1 Offline catalog

At preflight, invoke the prebuilt `sandbox-catalog-export` executable and parse
its schema-versioned JSON. Validate that every operation required by the selected
plan exists in the exported manager, runtime, or observability catalog.

Store the exact export and its SHA-256 digest in the run's definition snapshot.
The benchmark owns experiment factors and checks; the product catalog owns
product operation identity and request schema.

There is no hand-copied Python product catalog.

### 9.2 Isolated gateway

Do not reuse the E2E session gateway for scientific runs. Each campaign launches
an isolated gateway with:

- a generated loopback port;
- a cryptographically random auth token;
- state-owned PID, log, token, and effective-config paths;
- state-owned run and runtime directories;
- an explicit prebuilt daemon artifact;
- a process group that the Python owner can terminate;
- a readiness probe through the same authenticated public protocol.

The benchmark configuration template lives under `benchmark/defaults`. Python
fills only documented deployment values. The gateway executable performs final
configuration validation. Config failure is a preflight/infrastructure failure,
never a benchmark sample.

The benchmark must never call `bin/start-sandbox-docker-gateway` because that
script builds Cargo packages and manages shared `/tmp` paths. It launches the
prebuilt gateway executable directly with explicit arguments.

### 9.3 Raw timed transport

Use `asyncio.open_connection` and one newline-delimited JSON request per
connection, matching the proven E2E raw gateway contract:

```json
{
  "op": "operation_name",
  "request_id": "benchmark-...",
  "scope": {"kind": "sandbox", "sandbox_id": "..."},
  "args": {},
  "_stream_logs": false,
  "_sandbox_gateway_auth_token": "..."
}
```

Requirements:

- generate a unique request ID for every request;
- encode compact UTF-8 JSON plus one newline;
- require exactly one newline-terminated JSON response;
- enforce request and response size limits;
- redact credentials from errors and artifacts;
- classify product error envelopes separately from transport failures;
- record `time.monotonic_ns()` immediately before the send/read operation and
  immediately after the complete response line;
- keep setup, fixture generation, correctness verification, report generation,
  and teardown outside primary operation latency;
- use CLI subprocesses only for untimed lifecycle or diagnostics when a public
  socket operation is unavailable.

Concurrency is created inside the runner with an asyncio start barrier and
`TaskGroup`. Do not use pytest-xdist to generate request concurrency.

## 10. Experiment and operation model

### 10.1 Preserved families and operations

| Family | Operations |
| --- | --- |
| Command | `exec_command` |
| Files | `file_read`, `file_write`, `file_edit`, `file_blame` |
| Workspace Lifecycle | `create_workspace` |
| LayerStack | `squash_layerstack` |

Preserve the current factor IDs, factor roles, control values, workspace
profiles, session behavior, and operation-specific correctness checks. Closed
identifiers should be Python `StrEnum` values or validated literals, not a
plugin registry.

### 10.2 Plan validation and expansion

Plans and presets remain strict, versioned YAML data. Validation must:

- reject unknown fields and unsupported schema versions;
- reject duplicate operations or factor values;
- require one valid control for each varied factor;
- reject unsafe commands, product routes, paths, or credentials in plan data;
- validate trial counts, timeouts, resource intervals, and value bounds;
- verify required operations against the offline product catalog;
- produce a canonical JSON expanded plan;
- produce identical cell IDs and order for identical plan bytes, catalog digest,
  workspace-profile digests, and seed.

Preserve `randomized_blocks`, warmup/measured separation, `standard-local`, all
existing presets, and the Quick Smoke subset. YAML files may be moved directly
only after golden expansion tests pass.

### 10.3 Trial lifecycle

Every trial has explicit phases:

```text
setup -> operation -> verify -> teardown
```

Record each duration independently. A measured trial is reportable only when:

- the product operation produced a valid response;
- required correctness checks passed;
- no infrastructure failure occurred;
- teardown ran;
- the cleanup baseline was restored.

Warmups exercise exactly the measured path but are excluded from statistical
summaries. Failures remain in observations and reports; they are never silently
discarded as outliers.

## 11. Artifacts, recovery, and compatibility

### 11.1 State roles

- `fixtures/`: content-addressed generated inputs shared safely across runs;
- `runs/`: disposable per-run product workspaces;
- `results/<run-id>/`: authoritative run artifacts;
- `runtime/<run-id>/`: PID, token, config, and sanitized process logs;
- `tmp/`: same-filesystem staging for atomic replacements.

Secrets never enter `results/`. Runtime tokens are mode `0600`, redacted from
logs, and deleted after cleanup.

### 11.2 Artifact set

Preserve these stable names:

- `run-manifest.json`;
- `intent-plan.json`;
- `expanded-plan.json`;
- `definition-snapshot.json`;
- `environment-metadata.json`;
- `events.ndjson`;
- `observations.ndjson`;
- `summary.json`;
- `report.json`;
- `export.json`;
- `export.csv`;
- bounded per-trial evidence under allowlisted paths.

Writes follow these rules:

- immutable JSON: write to `tmp`, flush, fsync, atomic replace;
- append journals: one compact JSON record per line, flush at state boundaries;
- artifact downloads: fixed ID allowlist, never arbitrary paths;
- evidence: size cap, media-type allowlist, SHA-256 digest, secret scan;
- manifests: explicit state transition validation;
- timestamps: wall clock for human provenance, monotonic offsets for durations.

### 11.3 Schema policy

If Python emits byte/field-compatible data, retain the existing schema name and
version. If a field, tag, unit, nullability rule, or meaning changes, increment
the schema version. Never label an incompatible Python document as Rust schema
v1 or v2.

Add a `producer` block to the first new schema version:

```json
{
  "implementation": "python",
  "implementation_version": "...",
  "source_commit": "..."
}
```

Python readers must support the retained Rust artifact fixture versions,
including observation v1/v2 compatibility and partial-tail recovery. The web UI
must be able to open historical completed runs without starting a gateway.

### 11.4 Recovery

On startup, scan nonterminal manifests and validate journals. A single incomplete
final NDJSON record may be quarantined with its digest; corruption before the
final record is fatal and read-only. Recovery may clean only resources whose
run ownership is proved by manifest plus marker.

If complete cleanup cannot be proved, execution remains unavailable while
historical reports and artifacts remain readable. Recovery never changes a run
to `completed`.

## 12. Statistical contract

Port the observable statistical semantics and cover them with golden vectors:

- count, minimum, maximum, mean, sample standard deviation;
- median and median absolute deviation;
- p25, p75, and p95;
- coefficient of variation;
- IQR outlier indices;
- deterministic 95% percentile-bootstrap median interval with 10,000 resamples
  when `n >= 5`;
- explicit confidence-interval omission when `n < 5`;
- exploratory p95 marker when `n < 20`;
- raw distribution points when `n < 30`;
- Freedman-Diaconis histogram with Sturges and single-value fallbacks plus ECDF
  when `n >= 30`;
- bootstrap median-difference intervals for comparisons;
- bootstrap Pearson intervals and explicit omission reasons.

Port the existing deterministic seed derivation and SplitMix64 behavior if exact
historical parity is required. Golden tests must compare exact integer fields,
tags, and omission behavior and use documented floating-point tolerances for
derived values.

Do not substitute `pytest-benchmark`. It measures Python callable performance,
while this laboratory measures an external sandbox product with custom plans,
resource observations, correctness, cleanup, and artifact requirements.

## 13. API contract

Keep the current routes for the initial migration:

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/api/v1/health` | service, execution, recovery, and dependency health |
| GET | `/api/v1/settings` | resolved roots and path health |
| PUT | `/api/v1/settings` | state-owned settings only |
| GET | `/api/v1/definitions` | operations, factors, checks, phases, and presets |
| POST | `/api/v1/plans/validate` | strict validation and deterministic expansion |
| POST | `/api/v1/runs` | admit one campaign |
| GET | `/api/v1/runs` | list retained runs |
| GET | `/api/v1/runs/{run_id}` | current run projection |
| GET | `/api/v1/runs/{run_id}/events` | resumable SSE |
| POST | `/api/v1/runs/{run_id}/cancel` | idempotent cancellation |
| GET | `/api/v1/runs/{run_id}/report` | report projection |
| GET | `/api/v1/runs/{run_id}/artifacts` | allowlisted artifact index |
| GET | `/api/v1/runs/{run_id}/artifacts/{artifact_id}` | bounded artifact download |
| POST | `/api/v1/compare` | compatible-run comparison |

Preserve error envelopes and status codes where the current web relies on them.
Generate no TypeScript client during this migration; keep the existing small
manual client and shared fixture JSON. Contract fixtures are the language
boundary between Python and TypeScript.

SSE records retain ordered sequence IDs. Reconnect with `Last-Event-ID` replays
persisted events after that sequence before subscribing to live events. A slow
or disconnected browser never blocks the benchmark journal writer.

## 14. Web migration

Move `benchmark/web` to the test repository without a redesign. Required work:

1. preserve the current route and component behavior;
2. keep `/api/v1` relative URLs and same-origin credentials;
3. keep the mutation nonce header contract;
4. point the Vite development proxy at the Python server;
5. replace the real-backend Node launcher so it installs/starts the Python
   service and never builds Cargo;
6. replace Rust-specific test setup and diagnostics with Python equivalents;
7. update API types only from accepted contract fixture changes;
8. retain fixture Playwright tests, real-backend Quick Smoke, accessibility
   checks, cancellation, reports, comparison, artifact browsing, and recovery
   visibility.

The production web build is performed before backend startup or in CI. The
Python service does not invoke npm during a run.

## 15. pytest strategy

### 15.1 Recommendation

Use pytest. It is the best fit for the Python rewrite because fixtures and
finalizers express gateway/process/resource cleanup clearly, parametrization
covers operations and schema vectors, and markers separate offline tests from
live Docker tests.

Pytest verifies the benchmark application; it is not the production campaign
scheduler. `sandbox-benchmark run` and the web API call the same Python runner
without going through pytest collection.

### 15.2 Test layers

| Layer | Marker | Product/Docker | Scope |
| --- | --- | --- | --- |
| Unit | none | no | paths, plans, state machine, statistics, checks, redaction |
| Contract | `benchmark_contract` | no | API fixtures, catalogs, artifacts, schemas, web boundary |
| Compatibility | `benchmark_compatibility` | no | Rust-produced artifact golden corpus |
| Integration | `benchmark_integration` | fake process/socket only | cancellation, SSE, recovery, atomic writes |
| Live smoke | `benchmark_live` | yes | isolated real gateway and Quick Smoke |

The default fast command excludes `benchmark_live`. CI runs offline Python
tests and web tests on every change, then one serialized live Quick Smoke gate.

### 15.3 Required failure-injection tests

- gateway exits before readiness;
- gateway becomes unavailable mid-batch;
- malformed, oversized, non-newline, and product-error responses;
- cancellation before admission and in each lifecycle phase;
- one and multiple cleanup failures;
- process crash after each manifest transition;
- partial final journal line and interior journal corruption;
- wrong ownership marker, symlink escape, root alias, and protected deletion;
- secret in logs/evidence;
- stale product catalog or binary digest;
- browser disconnect and SSE resume;
- report generation from historical Rust artifacts without product startup.

## 16. Migration phases

### Phase 0 — Freeze contracts and parity corpus

1. Record current source counts and current Cargo/web commands.
2. Export the current product catalog.
3. Capture sanitized artifacts from successful Quick Smoke and representative
   standard/preset runs.
4. Capture plan-expansion, state-transition, API, event, observation,
   statistics, report, comparison, and recovery golden fixtures.
5. Record current browser contract fixtures and screenshots as orientation,
   not as sole acceptance evidence.

Gate: fixtures are committed in the external test repository, contain no
secrets or machine-specific absolute paths, and are readable without Docker.

### Phase 1 — Python project, roots, models, and guards

1. Create `benchmark/pyproject.toml` and `benchmark_lab`.
2. Implement explicit roots, ownership marker, safe atomic writes, redaction,
   and the zero-Rust pytest guard.
3. Implement strict Pydantic models for plans and public API fixtures.
4. Move defaults, presets, and profiles only after validation fixtures pass.

Gate: offline pytest passes from an unrelated working directory, source remains
unchanged, and forbidden Rust/package-dependency checks pass.

### Phase 2 — Artifact readers, statistics, reports, and comparison

1. Implement schema envelopes and Rust artifact compatibility readers.
2. Port journal recovery and atomic artifact writers.
3. Port statistics against golden vectors.
4. Port report/export/compare behavior needed by the existing web.

Gate: the Python backend opens the complete parity corpus and produces accepted
normalized outputs without product binaries or Docker.

### Phase 3 — Product boundary and isolated lifecycle

1. Consume `sandbox-catalog-export` from the explicit binary directory.
2. Implement authenticated raw JSONL transport.
3. Implement isolated gateway configuration, process ownership, readiness,
   logs, shutdown, and stale-process recovery.
4. Implement the resource registry and aggregated cleanup.

Gate: failure-injection integration tests pass and no test invokes Cargo or
imports product source.

### Phase 4 — Plans, fixtures, operations, and scheduler

Implement in this order:

1. deterministic plan expansion and Quick Smoke;
2. `exec_command`;
3. file read/write/edit/blame;
4. workspace creation;
5. LayerStack squash;
6. resource observations and product phase correlation;
7. cancellation and restart recovery.

Finish one operation end-to-end—setup, timed request, verification, teardown,
artifacts, report, and live test—before starting the next.

Gate: each operation passes its offline tests and one scoped live proof. Do not
rerun already-passing expensive families until the final gate.

### Phase 5 — FastAPI and web cutover

1. Implement the versioned routes and same-origin security.
2. Move the React/TypeScript web application.
3. Update fixtures and the real-backend launcher for Python.
4. Verify run launch, progress/SSE, cancellation, reports, comparison,
   artifacts, settings, accessibility, and browser refresh/reconnect.

Gate: Vitest, fixture Playwright, backend API contract pytest, and real-backend
Quick Smoke pass with no Cargo command.

### Phase 6 — Destructive cutover

1. Stop accepting changes to the old benchmark tree.
2. Run normalized parity and final live proof.
3. Remove `benchmark/backend` from the product Cargo workspace.
4. Delete `<PRODUCT_ROOT>/benchmark` after the external source is committed.
5. Remove old Rust benchmark dependencies, scripts, and CI jobs.
6. Add CI checks that reject a benchmark source reappearing in the product
   repository and reject Rust appearing in the external benchmark.
7. Update E2E documents that currently describe `benchmark/` as optional
   configuration rather than the benchmark application.

Gate: there is one source tree, one state root, no symlink/copy/fallback, no
benchmark Cargo member, and all final checks pass from the external repository.

## 17. Acceptance criteria

The migration is complete only when all statements are true:

1. `/ephemeral-sandbox-test/benchmark` is the only benchmark implementation.
2. The benchmark tree contains Python plus TS/JS/web assets and no Rust or Cargo
   files.
3. No benchmark command, test, or Node launcher invokes Cargo/Rust tooling.
4. Python imports no EphemeralOS product package and adds no product path to
   `sys.path`.
5. Startup works from an unrelated current directory using explicit canonical
   roots and prebuilt binaries.
6. Source remains byte-for-byte unchanged during validate, serve, run, compare,
   recovery, and cleanup.
7. All mutable data remains under the exact owned `.benchmark-state` root.
8. The selected plan is validated against the offline product catalog export.
9. Primary latency uses monotonic raw-socket timing and excludes process startup,
   fixtures, verification, reports, and teardown.
10. Identical inputs and seed produce identical expanded cell identities/order.
11. Warmups never enter measured statistics.
12. A correctness, infrastructure, or cleanup failure cannot yield a completed
    run.
13. Statistics pass the golden vector suite and comparison rejects incompatible
    runs before computing deltas.
14. Historical Rust-produced artifacts remain readable, or an explicit one-time
    migration tool produces lossless versioned replacements.
15. API contract pytest and web fixture tests pass.
16. Vitest, Playwright fixture, accessibility, and real Python-backend Quick
    Smoke pass.
17. Cancellation and injected crash recovery leave no owned sandbox, gateway,
    container, session, mount, or secret-bearing file.
18. The old product benchmark tree and Cargo workspace member are gone, with no
    compatibility copy, symlink, submodule, or runtime fallback.

## 18. Explicitly deferred

The following require a separate measured need and design:

- multiple simultaneous campaigns;
- remote/distributed workers;
- a database-backed run index;
- a generalized plugin/executor SDK;
- user authentication or non-loopback hosting;
- Python-generated TypeScript clients;
- replacing the existing React stack;
- NumPy/scientific-stack acceleration;
- merging the E2E Control Room and benchmark UI.

## 19. Implementation recommendation

Proceed with this Python/TypeScript architecture. Use pytest heavily for the
backend and safety contracts, but keep the actual benchmark runner as a normal
Python application. Preserve the existing web/API contract first, then simplify
only after the Python cutover is proven. The most important sequencing rule is
to build one vertical Quick Smoke path before porting the full scheduler and
report surface; that prevents a second large framework from being recreated in
Python without live evidence.
