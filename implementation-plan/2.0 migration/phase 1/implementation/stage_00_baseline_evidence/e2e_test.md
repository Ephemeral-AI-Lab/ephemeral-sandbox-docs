# Stage 00 E2E — Baseline and evidence seams

**POC proof tier.**
[Implementation overview](../index.md) · [Stage 00 specification](spec.md) · [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Product root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
Test root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`

## 1. Stage-local test objective

Implementation execution is blocked unless the product worktree is on the
exact fresh branch `upgrade-2.0-phase-1`, created from the newest approved
immutable product revision, with its base commit, upstream, clean scoped
worktrees, and responsible implementer recorded before any code edit. This
planning stage creates or switches no branch; any mismatch is a hard blocker.

Prove that the packaged feature-off product still uses the legacy v1 writer and reader, that structured evidence can identify that route without log inference, and that bounded lifecycle gauges return to their declared idle state in one long-lived daemon.

Stage 00 is runnable without SeqCDC/CAS because its authority and comparison path are both legacy. The exact seam is `runtime.layerstack.rollout_mode: legacy`, the existing `sandbox-observability-cli snapshot/layerstack` projection, and additive `LayerStackRouteSnapshot`/`LayerStackResourceSnapshot` fields. Candidate artifacts, candidate fallback, CAS timing, full regression, and normative qualification are deferred to their owning stages.

Required now:

1. focused Rust config/observation/v1-golden tests;
2. one packaged public create/write/publish/read/execute/destroy E2E route proof;
3. one tiny legacy benchmark and same-process resource sentinel;
4. exact dependency/environment snapshots.

## 2. Existing assets to reuse

| Asset | Exact path | Reuse |
| --- | --- | --- |
| Typed declarations | `e2e/harness/catalog/declarations.py` | Stable metadata and exactly-once validation checkpoints |
| Gateway custody | `e2e/harness/runner/gateway.py`, `resources.py` | Tracked gateway/sandbox cleanup; no global prune |
| Publication cases | `e2e/runtime/workspace_session/test_publish_workspace_session.py` | Reuse public CLI helpers and `runtime.workspace-session.publish.*` assertions |
| Resource quiescence | `e2e/observability/resource_efficiency/` | Existing manager/session/worker cleanup patterns |
| Operation timing | `.e2e-state/metrics/operation-timing/{latest.json,latest.md}` | Diagnostic client wall time only |
| Runtime samples | `.e2e-state/evidence/runtime/<case-key>.ndjson` | Bounded sample stream with explicit gaps |
| Benchmark runner | `benchmark/backend/benchmark_lab/runner.py` | Sole campaign scheduler |
| Sampling | `benchmark/backend/benchmark_lab/resource_sampling.py` | Allocated/logical disk, public cgroup, filesystem, snapshot/layerstack sources |
| Result schemas | `benchmark/backend/benchmark_lab/artifacts.py` | Run manifest v2, observation v5, report/export v4, evidence v1 |
| Modeled workload source | product `crates/sandbox-runtime/layerstack/tests/occ_merge_bench.rs` | Workload names only; modeled outputs are never called measured |
| Standard library | Python `json`, `pathlib`, and `unittest` | Build one shared canonical dependency-delta verifier without adding a Python package |

Before each live E2E command the implementer appends command and intent to `e2e/test-report.md`; afterward append Good/Defect/Fix and cleanup evidence. Cleanup is limited to tracked IDs and run-owned resources.

## 3. Resulting test tree

```text
ephemeral-sandbox/
├── crates/sandbox-runtime/layerstack/tests/baseline_v1_golden.rs       [add]
├── crates/sandbox-runtime/layerstack/tests/resource_observation.rs     [add]
├── crates/sandbox-runtime/operation/tests/storage_route_observation.rs [add]
└── crates/sandbox-cli/tests/observability.rs                           [modify]

ephemeral-sandbox-test/
├── e2e/runtime/layerstack_baseline/
│   ├── test_baseline_route.py                                          [add]
│   └── SPEC.md                                                         [add]
├── e2e/fixtures/layerstack_phase1/v1/
│   ├── corpus-manifest.json                                            [add]
│   ├── expected-tree.json                                              [add]
│   └── expected-roots.json                                             [add]
├── e2e/schemas/layerstack_phase1/evidence-v1.schema.json               [add]
├── e2e/tools/
│   ├── verify_external_dependency_delta.py                              [add] — stdlib-only canonical comparer
│   └── test_verify_external_dependency_delta.py                         [add] — synthetic exact-delta fixtures
├── benchmark/presets/layerstack-phase1-tiny-baseline.yml               [add]
├── .e2e-state/                                                         [reuse] — mutable run-owned evidence
└── .benchmark-state/                                                   [reuse] — mutable run-owned evidence
```

Runtime boundary snapshots:

```text
BEFORE / AFTER SUCCESS / AFTER FAILURE / AFTER CLEANUP
/eos/layer-stack/
├── .storage-writer.lock         [legacy coordination; one; no RootId]
├── manifest.json                [legacy v1 authority; atomic visibility]
├── workspace.json               [legacy base binding]
├── base/B000001-base/           [legacy native carrier]
├── layers/<committed>/          [legacy truth; success may add one]
├── staging/                     [empty at quiescence; failed private entry must be reaped]
└── .layer-metadata/
    ├── <committed>.digest          [legacy content digest]
    └── <committed>.bytes           [legacy allocated-byte metadata]

/eos/workspace/
├── manager.json                 [recovery catalog survives session cleanup]
├── .export/                     [absent after run cleanup]
└── <session>/                    [present only while active; absent after destroy]
    ├── upper/
    └── work/

/eos/namespace_execution/
└── <execution>/transcript.log   [present only while command owner lives; absent after cleanup]
```

Outside inspection may record allocated bytes, ownership/permissions, and absence of staging residue. Correctness, route, and logical cleanup must be asserted through public manager/runtime/observability CLIs. `/eos` is never exposed to the sandbox workload.

## 4. Typed E2E case catalog

Stage 00 POC rows use only the pinned Ubuntu 24.04 target image. The planned-final row
uses the Stage 07 target-image/native-backend capability matrix; this does not rewrite
the completed Stage 00 baseline result.

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `layerstack.phase1.baseline.legacy-route` | POC; `run-now-focused` | feature-off legacy | fresh tracked sandbox and explicit legacy config | create, write, publish, read, execute, destroy | exact v1 tree, legacy authority, zero candidate activity, complete cleanup | diagnostic component durations | categorized allocated bytes | owners return to idle | environment and zero-delta dependency inventory | `60000` ms | typed validation, runtime NDJSON, CLI JSON, tree digest |
| `layerstack.phase1.baseline.restart-cleanup` | POC; `run-now-focused` | legacy recovery | one permitted pre-visibility failpoint | restart through gateway custody and retry | no partial visibility, deterministic reap, legacy route unchanged | recovery and quiescence durations | residue allocation | no retained transaction, FD, or worker | same pinned platform/image evidence | `60000` ms | failpoint record and before/after inventory |
| `layerstack.phase1.baseline.tiny` | POC; `run-now-tiny-bench` | raw legacy control | fixed tiny corpus and one warmup | public paired lifecycle campaign | exact output digests and clean teardown | at least five alternating raw pairs | logical and allocated subtrees | settled delta and robust slope | complete environment record | `60000` ms | raw observations, report, export |
| `layerstack.phase1.qualification.all` | integration; `planned-final` | cumulative Phase 1 qualification | frozen Stage 07 required-runner, image, architecture, and Linux-backend matrix | full affected regression and qualification campaigns | every Phase 1 invariant and required capability-profile row passes | normative Stage 07 metrics | normative complete envelope | normative repeated-lifecycle matrix | exact image, effective Linux kernel, `/eos` backing filesystem, and architecture evidence | `300000` ms | Stage 07 qualification bundle |

Complete literal declaration metadata for every catalog row:

| Stable ID | Title | Description | Features | Validations | Validation features | Execution surface | Owner ID | Timeout (ms) | Pytest markers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `layerstack.phase1.baseline.legacy-route` | `Legacy LayerStack route and resource baseline is observable` | `Uses public workspace, command, file, and observability CLIs to freeze the feature-off v1 route and prove run-owned cleanup.` | `("workspace-session","layerstack","observability","phase1-baseline")` | `{"route":"The committed publication and subsequent read report legacy_v1 authority with no fallback, shadow comparison, or mismatch.","content":"Published bytes and metadata match the frozen v1 tree digest.","cleanup":"Session, execution, transaction, staging, lease, and tracked sandbox ownership reach the declared quiescent state."}` | `{"route":("layerstack","observability"),"content":("workspace-session","file"),"cleanup":("resource-efficiency",)}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","config")` |
| `layerstack.phase1.baseline.restart-cleanup` | `Legacy recovery preserves visibility and cleanup` | `Restarts at the permitted pre-visibility boundary and proves that retry preserves legacy authority while all run-owned staging is deterministically reclaimed.` | `("workspace-session","layerstack","recovery","phase1-baseline")` | `{"visibility":"No partial manifest or publication becomes visible before the legacy commit boundary.","recovery":"Restart and retry select the one complete legacy result without changing authority.","cleanup":"Staging, transactions, file descriptors, workers, and tracked run ownership return to quiescence."}` | `{"visibility":("layerstack","recovery"),"recovery":("layerstack","workspace-session"),"cleanup":("resource-efficiency","observability")}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","config")` |
| `layerstack.phase1.baseline.tiny` | `Legacy tiny benchmark control is reproducible` | `Runs the fixed legacy-only tiny corpus with alternating measured samples and records correctness, time, allocated disk, and memory-lifecycle evidence without a normative percentile claim.` | `("workspace-session","layerstack","benchmark","phase1-baseline")` | `{"correctness":"Every measured operation returns the frozen output and tree digest.","sampling":"The artifact contains the warmup and at least five alternating raw measured pairs.","cleanup":"Every repetition and the final campaign cleanup return owned resources to the declared settled state."}` | `{"correctness":("layerstack","workspace-session"),"sampling":("benchmark",),"cleanup":("benchmark","resource-efficiency")}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","benchmark","config")` |
| `layerstack.phase1.qualification.all` | `Phase 1 cumulative release qualification` | `Executes the frozen Stage 07 affected regression, correctness, recovery, benchmark, memory, disk, target-image, architecture, and Linux native-backend capability matrix.` | `("layerstack","phase1-qualification","portability","linux-native-backend","resource-efficiency")` | `{"terminal":"All normative Phase 1 gates and every required capability-profile row have passing evidence with exact image, effective Linux kernel, backing filesystem, and architecture; no universal or percentage compatibility is inferred."}` | `{"terminal":("layerstack","phase1-qualification","portability","linux-native-backend","resource-efficiency")}` | `"cli"` | `"layerstack-phase1"` | `300000` | `("runtime","layerstack","serial","release","config")` |

Every validation key above is emitted exactly once as a terminal
`ValidationReporter` result.

## 5. Correctness and failure matrix

| Case | Expected now | Deferred |
| --- | --- | --- |
| Empty/no-op and 1-byte/boundary legacy publication | exact current v1 identity; no new layer for no-op | v2/CDC boundaries Stage 03 |
| 1 MiB deterministic localized edit, incompressible file, 100–1,000 small files | exact legacy tree/export digest | dedup/space Stage 03/07 |
| Mode, symlink, hardlink where supported, whiteout, opaque dir, sparse, xattr/owner | freeze current behavior and known export limitations separately | portable round trip Stage 04/07 |
| Disjoint/conflicting/stale OCC | current behavior frozen | candidate OCC Stage 03 |
| Failure before layer rename / before manifest commit | no partial active manifest; owned staging recovered | candidate failpoints Stage 03/05 |
| Daemon restart and retry | feature-off legacy remains readable | mixed root Stage 06 |
| Command success/cancel plus workspace teardown | transcript owner releases before workspace removal under current roots | scratch move Stage 01 |
| PTY resize/arbitrary signal/literal EOF | deterministic unsupported response preserved | no parity work planned |
| Candidate strict fallback | impossible; candidate absent | Stage 04 strict gate requires zero fallback |
| Scalar/accelerated SeqCDC | absent | scalar Stage 03; acceleration excluded unless separately approved |
| Target-image userland independence | baseline records assumptions only | Stage 04 proves helper-free materialization; Stage 07 executes the declared target-image, architecture, and Linux native-backend capability matrix |

Any difference between frozen expected behavior and actual current behavior is a baseline defect, not silently updated data. The stage owner decides whether the defect blocks migration or receives a versioned, reviewed expectation.

## 6. Tiny correctness and benchmark loop

Preset `layerstack-phase1-tiny-baseline` uses the existing sequential runner and a deterministic seed. Corpus:

- empty/no-op;
- 1 KiB localized edit in a 1 MiB deterministic file;
- 1 MiB deterministic incompressible file;
- 256 small files totaling approximately 1 MiB;
- repeated overwrites at history depths 1, 8, and 32.

Run one warmup and at least five measured legacy/control pairs; prefer three warmups and ten alternating repetitions if every cell and the aggregate stay within the declared 30–60 second developer loop. Pre-generate inputs. Keep filesystem, host, image, cache class, seed, operation order, and config identical. Store every raw sample; report absolute values and ratios, but make no p95 or normative regression claim from an insufficient sample.

Collect elapsed/component time; bytes scanned/read/written; logical and allocated bytes for legacy layers, staging, workspace upper, transcripts, and metadata; layer/file count; tree digest; RSS/cgroup source availability; live/high-water resources; route/fallback/mismatch counters. Every field is labeled `measured`, `derived`, `estimated`, or `unknown`. Planning estimates are never promoted to measurements.

Diagnostic cap: each operation ≤60 seconds, each tiny cell ≤60 seconds, aggregate developer loop target 30–60 seconds. The exact raw distribution becomes the later paired baseline; it is not itself a candidate pass.

## 7. Memory-stability and reclamation test

Stage 00 adds fixed gauges and bounded encoded observations, so it changes a small allocation/ownership path. Use one daemon without restart across 20 cycles after 3 warmups:

```text
idle baseline
  -> warmed idle
  -> create/write/publish/read/exec active peak
  -> cancel-or-injected-failure active peak
  -> explicit destroy and bounded quiescence polling
  -> settled sample
```

Poll every 100 ms for at most 5 seconds. Quiescence requires zero active operation/publication/transaction/staging/permit/lease owners attributable to the case, queues drained, worker count at configured idle, session/execution absent, and terminal registry within its configured cap. A timeout or missing gating gauge fails; no arbitrary sleep, restart, `malloc_trim`, cache purge, or allocator change.

Record process RSS (and anonymous/file-backed split if available), cgroup current/peak, Docker stats fallback, fixed owned/high-water bytes, buffers, tasks, workers, queues, permits, mappings, FDs, caches, registries, leases, transactions, quiescence latency, and per-cycle outcome. Bound raw sampling with the existing stream/ring.

Predeclare the physical rule from an equal-warmup raw control before candidate work: first and last five-cycle settled-window medians, their delta, Theil–Sen or benchmark-standard robust slope, sample count, and raw noise band. Stage pass requires all logical counts return and the short physical series remain inside that frozen diagnostic band. It does not claim the final ≤384 MiB, ≤128 MiB idle-adjusted, scale, or 16/8 MiB gates; those remain Stage 07.

Verdicts use only: `bounded-and-released`, `bounded-retained-by-design`, `allocator-or-page-cache-retained`, `suspected-leak`, `confirmed-leak`, `measurement-unavailable`. Suspected/confirmed leak and unavailable stage-gating data block exit.

## 8. Dependency and portability proof

Capture for every frozen target/feature invocation:

- exact external `(source,name,version,checksum)` set;
- enabled external `(package,feature)` set;
- product-wide direct external manifest-edge multiset;
- workspace manifests and `Cargo.lock` bytes;
- Python/npm manifests/locks;
- image package/helper inventory;
- processes, sockets, services, commands, and runtime downloads on the route;
- license/notice inventory.

Repeat after implementation. Pass only on exact equality; Stage 00 itself adds no crate or edge. The currently observed all-feature host counts (291 resolved, 271 external, 116 direct edges, 490 feature pairs) are sanity checks, not substitutes for sets.

Sole Phase 1 target image recorded on 2026-07-24:

| Fixture | OCI index digest | linux/amd64 manifest | linux/arm64 manifest | Stage 00 status |
| --- | --- | --- | --- | --- |
| `ubuntu:24.04` | `sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` | `sha256:52df9b1ee71626e0088f7d400d5c6b5f7bb916f8f0c82b474289a4ece6cf3faf` | `sha256:7f622ca8766bccb22f04242ecb6f19f770b2f08827dc4b8c707de5e78a6da7ab` | raw index identity verified; arm64 runnable here, not yet qualified |

The same Ubuntu OCI index is used on every applicable required host, and each
run records and verifies the resolved platform manifest. Test-report Iteration
56 records the owner-authorized correction of the earlier transcribed arm64
value to the descriptor contained in the immutable captured raw index. The
index, tag, and historical captures were not changed. Read-only and non-root
runtime variants of this image are allowed. No image is a product dependency
and no target image helper is added. This completed Stage 00 run qualifies only
its pinned baseline cell; Stage 07 owns the declared target-image and Linux
native-backend capability matrix and must leave any unexecuted required cell
unverified.

## 9. Focused and final-stage commands

Run from the stated roots. Commands that create evidence use run-owned paths.

### Product formatting, lint, and focused unit/integration

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-config -p sandbox-runtime-layerstack -p sandbox-runtime -p sandbox-cli --all-targets --all-features -- -D warnings
cargo test -p sandbox-config runtime
cargo test -p sandbox-runtime-layerstack --test baseline_v1_golden --test resource_observation
cargo test -p sandbox-runtime --test storage_route_observation
cargo test -p sandbox-cli observability
```

### Exact zero-external-dependency comparison

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo metadata --locked --all-features --format-version 1 \
  > /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/tmp/<run_id>/metadata-after.json

cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.venv/bin/python e2e/tools/verify_external_dependency_delta.py \
  .e2e-state/evidence/<entry_capture>/stage00-entry-baseline.json \
  .e2e-state/evidence/<post_capture>/stage00-post-baseline.json \
  --output .e2e-state/evidence/<closure_capture>/dependency-delta.json
```

Resolve every placeholder to an explicit run-owned capture. Each capture
contains the complete frozen invocation inventory, and the verifier fails
unless package identities, versions, sources, checksums, feature pairs,
direct-edge multisets, and contract-file records are exact.

### Focused E2E

First live gate—append the required intent block to `e2e/test-report.md` first:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_baseline/test_baseline_route.py \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

For a focused rerun use `E2E_REBUILD_BINARY=0` only after recording that the gateway binary/config identity matches. `E2E_REBUILD_BINARY=1` does not rebuild if an already-responsive gateway is reused; record actual custody evidence.

Catalog validation:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.venv/bin/python e2e/tools/test_verify_external_dependency_delta.py
PYTHONPATH=e2e .venv/bin/python -m harness.catalog.collect \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

### Tiny benchmark validate/run

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
  --plan layerstack-phase1-tiny-baseline \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --plan layerstack-phase1-tiny-baseline \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

The benchmark consumes prebuilt binaries and does not rebuild them.

### Artifact compatibility validation

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.benchmark-state/test-venv/bin/python -m pytest \
  benchmark/backend/tests/compatibility/test_artifacts.py
```

### DO NOT RUN in Stage 00 — Stage 07 affected regression

Stage 07 owns this cumulative selector.

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

### DO NOT RUN in Stage 00 — Stage 07 qualification matrix

The command below preserves the frozen Ubuntu baseline cell. Stage 07 also runs its
declared glibc/musl/minimal/distroless/shell-less, architecture, Linux
Engine/Desktop-VM, and `/eos` backing-filesystem capability cells with exact digests
and environment records.

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

### DO NOT RUN in Stage 00 — Stage 07 full Phase 1 qualification

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

| Metric / field | Definition, source, cadence | Samples / aggregation | Gate and missing-data policy | Artifact |
| --- | --- | --- | --- | --- |
| `route.write_authority`, `route.read_authority` | closed enum from product observation, once per boundary | exact | both `legacy_v1`; missing fails | CLI JSON + validation |
| `fallback_count`, `mismatch_count`, `shadow_completed_count` | monotonic route counters | start/end delta | all zero; missing fails | runtime evidence |
| `operation.elapsed_ns` | client monotonic call wall time | warmup + ≥5 raw pairs; median only | diagnostic; operation <60 s | benchmark observation |
| `disk.<category>.allocated_bytes` | filesystem allocated bytes outside workload | pre/visible/post/cleanup | staging/session residue zero at quiescence | evidence JSON |
| `memory.process_rss_bytes` | daemon scope if identity proven; otherwise unavailable | 100 ms bounded stream | use Docker/cgroup fallback; never zero-fill | runtime NDJSON |
| `memory.cgroup_current_bytes` | public cgroup source | 100 ms | unavailable explicit | benchmark observation |
| `resource.live_*` | product owned-resource snapshot | every boundary + 100 ms polling | expected idle after ≤5 s; missing fails | CLI JSON |
| `settled_delta_bytes`, `settled_slope_bytes_per_cycle` | first/last 5-cycle medians and robust post-warmup slope | 20 cycles | within predeclared raw noise; diagnostic | summary/report |
| `dependency_fingerprint` | hash of canonical exact sets/multisets | before/after | byte-equal; missing fails | dependency snapshot |
| `tree_digest` | frozen exact content/metadata oracle | each correctness boundary | exact expected | fixture/result |

Every record includes commits/dirty states, Docker/Desktop/Engine, OCI index/platform digest, host/guest architecture, CPU/memory/storage allocation, kernel/filesystem/mount/userxattr, toolchains, config/mode, cache state, seed/corpus, source/scope, and measurement classification. The sampler streams or uses a fixed ring; it does not retain an unbounded time series.

## 11. Stage exit verdict

Mandatory:

- all focused Rust/static/golden tests pass;
- two focused live cases pass through public CLIs with legacy authority and zero fallback/mismatch/shadow;
- exact tree/content/metadata fixtures match;
- success and injected-failure cleanup reach quiescence in ≤5 seconds;
- logical resources return to idle and the short physical sentinel stays inside the frozen raw-control diagnostic band;
- dependency/package/feature/direct-edge/system/service/helper evidence is exactly unchanged;
- artifacts validate, are run-owned, and cleanup is proven.

Warnings may note unavailable optional RSS splits or unexecuted required
capability-matrix rows only when an approved independent source covers every
stage-gating value. `measurement-unavailable` for a gating value,
any route ambiguity, silent fallback, corruption/durability error, suspected
leak, unexpected residue, dependency delta, artifact/schema gap, or cross-run
cleanup is a blocker.

Rerun only the failing focused case after a documented fix, using reuse mode when binary identity is proven. Roll back all Stage 00 additive fields/fixtures if feature-off behavior or observation boundedness cannot be preserved. Full SeqCDC/CAS correctness, time/space/RSS matrices, portability, soak, and production status remain deferred to Stages 03–07 and are not passed here.
