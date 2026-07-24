# Stage 08 E2E — Retention, GC, packs, compaction, and evacuation

[Implementation overview](../index.md) · [Stage 08 specification](spec.md) · [Preparation 03](../../prep/03-seqcdc-cas-and-squash-decision.md) · [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Product root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
Test root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`

## 1. Stage-local test objective

Implementation execution is blocked unless the product worktree is on the
exact fresh branch `upgrade-2.0-phase-1`, created from the newest approved
immutable product revision, with its base commit, upstream, clean scoped
worktrees, and responsible implementer recorded before any code edit. This
planning stage creates or switches no branch; any mismatch is a hard blocker.

This is a **POC proof tier**, not Phase 1 qualification. It proves, before candidate authority exists, that focused candidate maintenance is bounded and recoverable while legacy publication/read authority remains untouched.

Exit evidence must show:

- a current, retained, pinned, leased, branched/frontier, or in-flight root is never collected;
- an unreachable and unleased candidate object becomes invisible only after a complete durable grace epoch and final generation/lease recheck;
- open/sealed packs and maintenance transactions obey every fixed cap;
- compaction/evacuation commits replacement locators before source deletion and never loses the last locator;
- crashes at each journal/catalog/fsync boundary recover without corrupting a root;
- normal command, file, PTY, and stdin paths still use native files with zero CAS/pack lookup;
- candidate work releases logical resources in one long-lived daemon and creates no new external dependency.

Full suites, final 64 MiB/256 MiB/1 GiB × 1/16/64-root matrices, normative
percentiles, RSS limits, settled-space claims, and required-host qualification
using the sole pinned Ubuntu target are owned by Stage 11 and must not run
here. Cross-image portability is outside Phase 1 and is not a gate.

## 2. Existing assets to reuse

| Asset | Reuse |
| --- | --- |
| `e2e/harness/catalog/declarations.py` | Required `@e2e_test` declaration with stable ID, title, description, features, validations, validation-feature mapping, execution surface, owner, and timeout |
| `e2e/harness/runner/reporter.py` | Flush/fsync JSONL evidence and exact manifest node IDs; one terminal validation checkpoint/case |
| `e2e/harness/runner/resources.py` | Run-scoped ownership, LIFO cleanup, tracked sandbox/session/execution IDs; never global prune |
| publication live cases under `e2e/runtime/workspace_session/` | Public create/write/publish/read/restart/OCC actions; do not duplicate their scheduler |
| squash/autosquash catalogs (`SMK-*`, `MED-*`, `HRD-*`, `LOAD-499`, `autosquash.cor.*`, `autosquash.perf.*`) | Workload/correctness vocabulary only; Stage 08 must not route pack pressure to squash |
| `benchmark/backend/benchmark_lab/resource_sampling.py` | Monotonic time, logical/allocated filesystem bytes, public cgroup memory/CPU/block I/O, layerstack snapshots, host free space |
| `benchmark/backend/benchmark_lab/artifacts.py` | Run manifest v2, observation v5, report/summary/export v4, bounded evidence v1 (content-addressed, ≤1 MiB) |
| `benchmark/backend/tests/compatibility/test_artifacts.py` | Actual reader/schema compatibility validation for generated artifact families |
| Stage 00 route/resource observation | Authority, fallback/mismatch, workers, buffers, queues, permits, leases, transactions, quiescence |
| Stage 07 publication/recovery fixtures | Committed candidate shadow roots, loose locators, journal failpoints, exact logical tree oracle |

Before any live command, append the command, intent, feature, expected evidence, ownership scope, and cleanup plan to `e2e/test-report.md`. After it finishes, append Good/Defect/Fix, artifact IDs, and cleanup evidence. This planning stage executes nothing.

## 3. Resulting test tree

```text
ephemeral-sandbox/
├── crates/sandbox-runtime/layerstack-core/tests/
│   ├── pack_limits.rs                                              [add]
│   ├── retention_graph.rs                                          [add]
│   └── evacuation_plan.rs                                          [add]
├── crates/sandbox-runtime/layerstack/tests/
│   ├── pack_bounds.rs                                              [add]
│   ├── retention_gc.rs                                             [add]
│   └── maintenance_recovery.rs                                     [add]
└── crates/sandbox-runtime/operation/tests/layerstack_maintenance.rs [add]

ephemeral-sandbox-test/
├── e2e/runtime/layerstack_retention_gc/
│   ├── test_retention_gc.py                                       [add]
│   ├── test_pack_recovery.py                                      [add]
│   └── SPEC.md                                                    [add]
├── benchmark/presets/layerstack-phase1-tiny-retention-gc.yml      [add]
├── .e2e-state/                                                    [reuse] — run-owned evidence only
└── .benchmark-state/                                              [reuse] — run-owned evidence only
```

Runtime boundary inventory:

```text
BEFORE
/eos/layer-stack/
├── manifest.json                                                       [legacy authority, immutable to candidate maintenance]
├── workspace.json                                                      [legacy authority, immutable to candidate maintenance]
├── base/                                                               [legacy authority, immutable to candidate maintenance]
├── layers/                                                             [legacy authority, immutable to candidate maintenance]
├── .layer-metadata/                                                    [legacy authority, immutable to candidate maintenance]
├── roots/v2/                                                           [Stage07 candidate shadow]
├── manifests/v2/                                                       [Stage07 candidate shadow]
├── objects/v1/loose/                                                   [Stage07 candidate shadow]
├── catalogs/v1/
│   ├── roots.catalog                                                   [committed generation]
│   ├── locators.catalog                                                [committed generation]
│   ├── materializations.catalog                                        [committed generation]
│   └── leases.catalog                                                  [committed generation]
├── journals/v1/
│   ├── publication/                                                    [terminal/empty]
│   ├── hydration/                                                      [terminal/empty]
│   └── migration/                                                      [terminal/empty]
├── leases/v1/                                                          [fixture leases as declared]
├── packs/v1/                                                           [absent or empty]
├── retention/v1/                                                       [absent or empty]
├── maintenance/v1/                                                     [absent or empty]
└── trash/v1/                                                           [absent or empty]

AFTER COMMIT
/eos/layer-stack/
├── packs/v1/sealed/<PackId>.pack                                      [≤64MiB payload, ≤100k records, ≤80MiB allocation]
├── indexes/v1/
│   ├── pages/                                                          [replacement locator generation committed]
│   └── index.catalog                                                   [replacement locator generation committed]
├── catalogs/v1/
│   ├── locators.catalog                                                [generation-consistent]
│   └── retention.catalog                                               [generation-consistent]
├── retention/v1/epochs/<N>.epoch                                      [complete durable epoch]
├── maintenance/v1/
│   ├── gc.cursor                                                       [terminal/reset]
│   └── compaction.cursor                                               [terminal/reset]
└── trash/v1/<N>/                                                      [only grace-wait sources]

AFTER INJECTED FAILURE / RESTART
/eos/layer-stack/
├── journals/v1/compaction/<id>.journal                                [replayed to a terminal state]
├── staging/v2/compaction/<id>/                                        [installed or absent, never ambiguous]
├── packs/v1/
│   ├── open/                                                           [no partial committed reader-visible pack]
│   └── sealed/                                                         [only complete reader-visible packs]
└── catalogs/v1/locators.catalog                                       [old or new complete generation]

AFTER CLEANUP / QUIESCENCE
/eos/layer-stack/
├── legacy entries                                                     [byte/inode/content inventory unchanged]
├── staging/v2/
│   ├── publication/                                                    [empty]
│   ├── hydration/                                                      [empty]
│   ├── squash/                                                         [empty]
│   ├── compaction/                                                     [empty]
│   └── migration/                                                      [empty]
├── journals/v1/*/                                                     [terminal records bounded/reaped]
├── trash/v1/                                                          [only entries younger than one complete epoch]
└── no unexplained unreachable+unleased bytes

/eos/workspace/
├── manager.json
├── .export/
└── <session>/                                                          [active only; session subtree absent after destroy]
    ├── upper/
    ├── work/
    └── executions/<exec>/transcript.log

/eos/namespace_execution/                                              [compatibility-empty; boot-reaped; no new writes]
```

Correctness is asserted through public manager/runtime/file/workspace/observability operations. Outside `/eos` inspection supplies allocated-byte, permissions, and absence/residue evidence; it is not a second product API and never runs inside the target image.

## 4. Typed E2E case catalog

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `layerstack.phase1.retention-gc.retain-leased-root` | medium / `run-now-focused` | candidate-shadow retention and GC | current/history/pinned/leased/in-flight/unselected roots | publish/read roots; acquire/release lease; request bounded maintenance | every selected root reconstructs; only unreachable unleased state passes trash, durable grace, and final recheck | phase durations, diagnostic only | allocated bytes by live/staging/trash/unexplained | owner gauges return to warmed idle after cleanup | zero dependency delta; pinned Ubuntu public APIs; outside `/eos` evidence only | `60000` ms | catalog JSON, receipts, tree digests, epoch/lease snapshots, allocated-byte inventory, logs |
| `layerstack.phase1.retention-gc.pack-bounds-recovery` | hard / `run-now-focused` | pack caps and crash recovery | records at next-record payload/count/allocation boundaries; failpoints around journal/seal/locator/trash | publish fixtures; request maintenance; restart daemon; reread roots | reserve-before-cap; no pack exceeds 64 MiB/100,000/80 MiB; old-or-new complete generation; retry idempotent | phase/failpoint recovery durations | open/sealed/staging/trash allocated bytes and residue | buffers/permits/journals settle after every fault | graph/lock equality and target-image tool independence | `60000` ms | pack/index summaries, journal states, root digests, recovery timeline, logs |
| `layerstack.phase1.retention-gc.evacuation-locator-swap` | hard / `run-now-focused` | compaction, locators, reader leases | one/two-locator objects; reader lease; ≥20% dead selected pack and >5% aggregate pressure | read while requesting evacuation; cancel/restart; release lease | replacement durable first; last locator never removed; source survives lease plus complete epoch; content exact | evacuation phases and lease overlap | source/target/trash/dead/slack allocation | locator/read leases and permits quiesce; no detached worker | zero new helpers/services; portable core/provider boundary evidence | `60000` ms | locator generations, lease snapshots, pack inventory, tree digests, logs |
| `layerstack.phase1.retention-gc.tiny` | bench / `run-now-tiny-bench` | diagnostic retention/GC loop | fixed ~16 MiB mixed corpus; depths 1/8/32; one warmup; ≥5 alternating pairs | publish, read, retain, sweep, compact, clean up through public surfaces | every repetition matches tree/object oracle and cap invariants; no normative percentile claim | raw paired durations and diagnostic threshold | peak/settled categorized allocated bytes | logical final/high-water gauges plus explicit cgroup/RSS availability | frozen dependency evidence and pinned-environment manifest | `60000` ms | plan/result JSON, raw samples, environment, disk series, memory series, logs |
| `layerstack.phase1.retention-gc.qualification` | release / `planned-final` | cumulative final qualification | Stage 11 scale/history/required-host matrix using the sole pinned Ubuntu 24.04 target image | Stage 11 public regression, soak, and benchmark routes | all normative space/RSS/time/soak/portability rows and affected regressions pass | normative paired p50/p95 and ≤5 min pair | full settled/peak envelope | full repeated-cycle adjusted final/peak and RSS gates | required release runners use the pinned Ubuntu 24.04 target; cross-image acceptance is deferred beyond Phase 1 | `300000` ms | Stage 11 qualification bundle only |

The three live cases each emit exactly one terminal validation checkpoint after cleanup. Complete declarations:

```python
@pytest.mark.medium
@pytest.mark.config
@e2e_test(
    id="layerstack.phase1.retention-gc.retain-leased-root",
    title="Retention and GC preserve every selected or leased root",
    description="Publishes a deterministic candidate-shadow root graph, closes durable retention epochs, and proves that only unreachable unleased state passes trash, grace, and final recheck while legacy remains authoritative.",
    features=("workspace-session", "layerstack", "phase1-cas", "retention", "garbage-collection"),
    validations={
        "terminal": "All selected, pinned, leased, frontier, and in-flight roots reconstruct exactly; unreachable unleased state is deleted only after a complete durable grace epoch; cleanup and authority invariants hold.",
    },
    validation_features={
        "terminal": ("layerstack", "retention", "resource-efficiency", "observability"),
    },
    execution_surface="cli",
    owner_id="layerstack-phase1",
    timeout_ms=60_000,
)
```

```python
@pytest.mark.hard
@pytest.mark.config
@e2e_test(
    id="layerstack.phase1.retention-gc.pack-bounds-recovery",
    title="Pack caps and maintenance recovery are atomic",
    description="Exercises the exact next-record pack boundaries and restarts at every pack, journal, locator-catalog, and trash visibility boundary.",
    features=("workspace-session", "layerstack", "phase1-cas", "pack", "recovery"),
    validations={
        "terminal": "No pack crosses payload, record, or allocation caps; recovery selects an old-or-new complete locator generation; every committed root reconstructs and private state is reaped.",
    },
    validation_features={
        "terminal": ("layerstack", "pack", "recovery", "resource-efficiency"),
    },
    execution_surface="cli",
    owner_id="layerstack-phase1",
    timeout_ms=60_000,
)
```

```python
@pytest.mark.hard
@pytest.mark.config
@e2e_test(
    id="layerstack.phase1.retention-gc.evacuation-locator-swap",
    title="Evacuation preserves the last locator and reader leases",
    description="Compacts a synthetic dead-byte pack while a bounded reader lease overlaps locator replacement, durable grace, cancellation, and restart.",
    features=("workspace-session", "layerstack", "phase1-cas", "pack", "evacuation", "leases"),
    validations={
        "terminal": "Replacement locators become durable before source removal; a last locator or leased carrier is never deleted; native execution remains CAS-free and all owned resources quiesce.",
    },
    validation_features={
        "terminal": ("layerstack", "evacuation", "leases", "resource-efficiency", "observability"),
    },
    execution_surface="cli",
    owner_id="layerstack-phase1",
    timeout_ms=60_000,
)
```

```python
@pytest.mark.release
@pytest.mark.config
@e2e_test(
    id="layerstack.phase1.retention-gc.qualification",
    title="Retention GC and pack qualification matrix",
    description="Stage 11-only cumulative release matrix for settled space, memory, time, recovery, required-host coverage using the sole pinned Ubuntu 24.04 target image, and regression; cross-image acceptance is deferred beyond Phase 1 and the declaration is cataloged but not selected in Stage 08.",
    features=("layerstack", "phase1-qualification", "retention", "garbage-collection", "pack", "portability"),
    validations={
        "terminal": "All Stage 11 normative gates and required-release matrix rows have executed evidence and no unverified required row.",
    },
    validation_features={
        "terminal": ("layerstack", "phase1-qualification", "resource-efficiency", "portability"),
    },
    execution_surface="cli",
    owner_id="layerstack-phase1",
    timeout_ms=300_000,
)
```

The tiny benchmark is also cataloged as a typed pytest wrapper so artifact and terminal-validation semantics remain identical:

```python
@pytest.mark.bench
@pytest.mark.config
@e2e_test(
    id="layerstack.phase1.retention-gc.tiny",
    title="Tiny retention GC diagnostic loop",
    description="Runs the fixed bounded retention, sweep, and compaction plan with alternating control/candidate samples while requiring an exact tree oracle and complete lifecycle evidence.",
    features=("workspace-session", "layerstack", "phase1-cas", "retention", "garbage-collection", "benchmark"),
    validations={
        "terminal": "Every repetition reconstructs exactly, hard pack/GC bounds hold, run-owned cleanup completes, and raw time, allocated-disk, and memory-lifecycle series are schema-valid.",
    },
    validation_features={
        "terminal": ("layerstack", "retention", "resource-efficiency", "observability", "benchmark"),
    },
    execution_surface="cli",
    owner_id="layerstack-phase1",
    timeout_ms=60_000,
)
```

Its plan metadata is: existing schema/version; factors `route × history-depth × maintenance-state`; fixed seed/corpus; one warmup; minimum five alternating repetitions; per-cell 60-second timeout; correctness oracle `tree_digest`; collectors `filesystem`, `layerstack`, `public-cgroup-or-explicit-unavailable`; cleanup `tracked-run-owned`; disposition `run-now-tiny-bench`.

## 5. Correctness and failure matrix

| Boundary / fault | Required assertion | Disposition |
| --- | --- | --- |
| root is current, retained-history, pinned, branch, frontier, leased, or in-flight | strong graph and required materialization/object locators remain | `run-now-focused` |
| provenance-only parent/base is not independently selected | weak edge does not retain its graph | `run-now-focused` |
| object is unreachable and unleased in epoch `N` | rename to trash may occur; unlink may not | `run-now-focused` |
| epoch `N+1` incomplete, lease/catalog generation changes, or final check unavailable | conservative keep/replan | `run-now-focused` |
| epoch `N+1` complete and all final generations match | unlink + parent fsync; root reconstruction unaffected | `run-now-focused` |
| next record would cross exactly one of 64 MiB payload, 100,000 records, 80 MiB allocation | current pack seals before append; record starts a new pack | `run-now-focused` |
| crash before pack/footer fsync | target private/unreadable; old locator active | `run-now-focused` |
| crash after target fsync but before locator CAS | orphan target reaped/quarantined; old locator active | `run-now-focused` |
| crash with unknown locator CAS result | recovery reads generation; never guesses; old or new complete set | `run-now-focused` |
| crash after locator CAS but before source trash | new locators active; recovery resumes trash | `run-now-focused` |
| cancellation at any state | current atomic phase completes, cursor persists, permits/FDs release | `run-now-focused` |
| one-locator object selected for evacuation | replacement must be durable/committed before removal; otherwise reject | `run-now-focused` |
| overlapping carrier/object lease | source remains through release plus grace/recheck | `run-now-focused` |
| sealed pack dead ratio just below/at 20%; aggregate just below/above 5% | deterministic no-trigger/async trigger and normal/urgent scheduling | `run-now-focused` |
| corruption in pack/footer/index/journal | candidate fails closed/quarantines; legacy stays readable | `run-now-focused` |
| pack pressure while native depth is low | compaction/evacuation only; squash queue unchanged | `run-now-focused` |
| command/file/PTY/stdin during/after maintenance | exact bytes/semantics on native carrier; zero CAS/pack lookup | `run-now-focused` |
| full space/time/RSS and required-host matrix using the sole pinned Ubuntu target | no Stage 08 claim | `planned-final` in Stage 11 |

Fixture oracles include typed IDs, canonical logical tree/metadata digest, selected-root reasons, strong/weak edge list, locator generations, epoch records, pack record offsets/lengths/checksums, legacy inventory digest, and expected terminal state.

## 6. Tiny correctness and benchmark loop

Preset `layerstack-phase1-tiny-retention-gc` is deliberately smaller than qualification:

- one deterministic ~16 MiB mixed tree with a localized edit, repeated object, incompressible object, and 256 small files;
- history depths 1, 8, and 32;
- pack states below/at the 20% individual trigger and below/above the 5% aggregate urgent trigger;
- one current, one pinned, one leased, and one unreachable root;
- one warmup and at least five alternating `legacy control / candidate-shadow maintenance` pairs; prefer 3–5 warmups and 10 samples only if the entire developer loop stays within 30–60 seconds;
- pre-generated payloads, identical seed/order/image/config/cache class, and no concurrent campaign.

Each cell performs publish → exact read/tree digest → maintenance → exact read/exec → destroy → quiescence. Record raw samples only: elapsed/components, bytes read/written/scanned/copied, logical/allocated bytes by candidate category, pack live/dead/slack, trash and staging, object/locator/root counts, catalog generations, workers/buffers/queues/permits/leases/FDs, cgroup/process-source availability, and authority/fallback/mismatch.

An operation or cell over 60 seconds fails the POC. With fewer than enough independent samples, report median/raw spread only—never p95. The tiny loop may prove cap adherence and logical release; it cannot pass final amplification, RSS, or throughput gates.

## 7. Memory-stability and reclamation test

Use one already-built daemon and one gateway identity without restart for 20 measured cycles after three warmups:

```text
warmed idle
  -> create/publish candidate shadow
  -> acquire pin + root/object/carrier leases
  -> pack + mark + sweep + compaction/evacuation
  -> injected cancellation or restart-recovery phase (without replacing measured daemon except the dedicated recovery case)
  -> release owners; close next durable epoch; final recheck
  -> destroy session; poll quiescence ≤5 seconds
  -> settled sample
```

The ordinary sentinel does not restart the daemon between iterations; the separate recovery case is not included in slope inference. Quiescence requires all case-owned sessions/executions/publications/maintenance transactions/staging/borrowed chunks/pack buffers/merge readers/permits/leases/FDs at warmed idle, queues drained, four-worker global bound respected, and only policy-retained roots plus valid grace trash remaining.

Record 100 ms bounded samples or fixed-ring summaries for RSS source, cgroup current/peak, Docker stats fallback, logical owned/high-water bytes, cache entries/bytes, workers/tasks/buffers/queues/permits, journals/cursors/leases, pack/trash/staging allocated bytes, and quiescence latency. Daemon RSS unavailable due to PID identity is explicit `measurement-unavailable`, never zero; Docker/cgroup is the independent fallback.

Physical decision uses the equal-warmup control's first/last five-cycle settled medians, delta, robust slope, and raw noise band. Logical non-release, growth in unexplained bytes, timeout, missing gating gauge, or repeated growth outside the frozen coarse band blocks. No arbitrary sleep, restart-to-clean, `malloc_trim`, allocator switch, cache purge, or RSS-only leak conclusion.

## 8. Dependency and portability proof

Before and after, capture exact:

- resolved external `(source,name,version,checksum)` set;
- enabled external `(package,feature)` set for each frozen target/invocation;
- product-wide direct external manifest-edge multiset;
- workspace manifests/`Cargo.lock`, Python/npm manifests/locks, vendored inventory;
- image packages/helpers and external processes/sockets/services/commands/downloads on the route;
- internal workspace graph and cycle check.

Pass requires byte/set/multiset equality for every external surface. Stage 08 may add only the already-planned internal inward edge to `sandbox-runtime-layerstack-core`; it may not add a crate from crates.io, Python package, native/FFI library, system tool, helper, sidecar, service, shell command, or target-image executable.

The focused run uses the sole Phase 1 target,
`ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`,
and records the resolved platform manifest. This is one required-host row, not
the final cross-host qualification. All storage inspection is outside the
sandbox; the test performs no `sh`, `tar`, `find`, checksum utility,
libc-specific tool, or package install inside the image. Read-only and
non-root runtime variants use the same image identity. Stage 11 executes every
required host/architecture/Docker release-runner row using this same OCI index
and records the resolved platform manifest; no unexecuted required row is
called qualified. Cross-image portability is deferred beyond Phase 1 and is
neither an acceptance nor a retirement gate.

## 9. Focused and final-stage commands

### Product formatting, lint, and focused unit/integration

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack -p sandbox-runtime --all-targets --all-features -- -D warnings
cargo test -p sandbox-runtime-layerstack-core --test pack_limits --test retention_graph --test evacuation_plan
cargo test -p sandbox-runtime-layerstack --test pack_bounds --test retention_gc --test maintenance_recovery
cargo test -p sandbox-runtime --test layerstack_maintenance
```

### Exact zero-external-dependency comparison

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo metadata --locked --all-features --format-version 1 \
  > /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/tmp/<run_id>/metadata-after.json

cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.venv/bin/python e2e/tools/verify_external_dependency_delta.py \
  --baseline .e2e-state/baselines/layerstack-phase1/<invocation_id> \
  --candidate .e2e-state/tmp/<run_id>/metadata-after.json \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --require-stdlib-crate sandbox-runtime-layerstack-core \
  --require-exact-external-delta-zero
```

### Focused E2E

From the declared test root, first append the intent block to `e2e/test-report.md`, then run:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_retention_gc/test_retention_gc.py \
  e2e/runtime/layerstack_retention_gc/test_pack_recovery.py \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

Use `E2E_REBUILD_BINARY=0` only after the report records matching gateway binary/config identity. `E2E_REBUILD_BINARY=1` may reuse an already-responsive gateway; record actual custody evidence.

### Artifact compatibility validation

Catalog and artifact-reader validation:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
PYTHONPATH=e2e .venv/bin/python -m harness.catalog.collect \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
.benchmark-state/test-venv/bin/python -m pytest \
  benchmark/backend/tests/compatibility/test_artifacts.py
```

### Tiny benchmark validate/run

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
  --plan layerstack-phase1-tiny-retention-gc \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --plan layerstack-phase1-tiny-retention-gc \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

The benchmark consumes prebuilt binaries and does not rebuild.

### DO NOT RUN in Stage 08 — Stage 11 affected regression

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1 \
  e2e/runtime/workspace_session \
  e2e/manager/management/squash \
  e2e/manager/management/export \
  e2e/observability/resource_isolation \
  e2e/observability/resource_efficiency \
  e2e/compound/stress \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

### DO NOT RUN in Stage 08 — Stage 11 native-host/pinned-Ubuntu-24 matrix

Stage 11 runs this single-image matrix once per applicable required host.
Pinned Ubuntu 24.04 is the only Phase 1 target image; cross-image portability
is deferred beyond Phase 1 and is not an acceptance gate.

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_portability_matrix.py \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

### DO NOT RUN in Stage 08 — Stage 11 full Phase 1 qualification

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
for PHASE1_PLAN in \
  layerstack-phase1-selection \
  layerstack-phase1-rss \
  layerstack-phase1-space \
  layerstack-phase1-qualification
do
  E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
  ../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
    --plan "$PHASE1_PLAN" \
    --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
    --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
    --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
  E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
  ../.benchmark-state/test-venv/bin/sandbox-benchmark run \
    --plan "$PHASE1_PLAN" \
    --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
    --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
    --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
done
```

## 10. Metrics and evidence contract

| Metric | Source/cadence | Aggregation | Stage 08 gate |
| --- | --- | --- | --- |
| logical tree/content/metadata digest | public file/workspace operations each boundary | exact | unchanged for every retained root |
| legacy inventory digest and route authority | outside inventory + public observation pre/post | exact/delta | legacy bytes unchanged; read/write `legacy_v1`; fallback/mismatch zero |
| pack payload/records/allocation | pack observation on reserve/seal/recovery | max/exact | ≤64 MiB/100k/80 MiB and seal-before-cross |
| GC transaction records/payload | journal observation per transaction | max | ≤100k or 64 MiB, whichever first |
| retention/lease/locator/materialization generations | public bounded observation at mark/trash/final recheck | exact sequence | consistent snapshot and repeated final check |
| live/dead/slack/trash/unexplained bytes | allocated filesystem inventory | boundary and settled | trigger semantics exact; unexplained persistent bytes zero |
| last-locator risk/rejected deletion | product counters and fixture locator set | exact | zero committed last-locator losses |
| elapsed/component ns | monotonic runner | raw + median, no unsupported p95 | each operation/cell ≤60 s; diagnostic otherwise |
| logical owned resources | product gauges every boundary/100 ms | high-water + settled | all case-owned values return to warmed idle ≤5 s |
| RSS/cgroup/container memory | declared independent source, 100 ms bounded | first/last windows + robust slope | coarse noise sentinel only; unavailable explicit |
| filesystem I/O | public cgroup/block source plus allocated bytes | deltas | source disclosed; no target-image helper |
| dependency/system fingerprint | exact canonical artifacts before/after | equality | zero delta |
| environment | commits/dirty, Docker/Desktop/Engine, OCI/platform digest, host/guest arch/kernel/fs/mount/userxattr, Rust/Python, config/mode/cache/seed | one immutable manifest/run | missing comparability field blocks benchmark verdict |

Every result value uses exactly one provenance label: `measured`, `derived`, `estimated`, or `unknown`; only `measured` and `derived` may support a gate. A benchmark model may emit separate non-gating projections under its source convention, but those projections are never result provenance. Evidence is run-owned, content-addressed where supported, schema-valid, size-bounded, and tied to exact node IDs. Cleanup is limited to tracked IDs—never host-wide or Docker-global prune.

## 11. Stage exit verdict

Pass Stage 08 only when all focused Rust and three live cases pass; the tiny plan validates and completes; every retained/leased root reconstructs; unreachable unleased state obeys grace and final recheck; pack and transaction caps never cross; all failpoints recover old-or-new complete locators; last-locator loss is zero; legacy inventory/authority are unchanged; native hot paths have zero CAS/pack lookups; logical resources quiesce; the physical sentinel stays within its predeclared coarse rule; schemas/catalog validate; cleanup is proven; and external dependency/runtime surface delta is exactly zero.

Block on corruption, ambiguous catalog generation, early deletion, persistent unexplained bytes, cap violation, route ambiguity/fallback, legacy mutation, missing gating evidence, cross-run cleanup, suspected leak, or external delta. A warning may cover only an optional physical source when an approved independent fallback supplies the gate.

This verdict is only `stage-08-poc-passed`. It is not production readiness, default enablement, final performance/space/RSS/portability qualification, or permission to retire legacy. Those remain Stage 11.
