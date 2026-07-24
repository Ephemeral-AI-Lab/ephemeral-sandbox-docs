# Stage 06 E2E — Strict candidate activation

Links: [implementation overview](../index.md) · [stage specification](spec.md) · [quantitative contract](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Tier: **POC proof tier**. The mandatory live set is one warm/cold strict activation case, one no-fallback corruption/rollback case, and one sub-minute tiny benchmark/memory sentinel.

## 1. Stage-local test objective

Implementation execution is blocked unless the product worktree is on the
exact fresh branch `upgrade-2.0-phase-1`, created from the newest approved
immutable product revision, with its base commit, upstream, clean scoped
worktrees, and responsible implementer recorded before any code edit. This
planning stage creates or switches no branch; any mismatch is a hard blocker.

Prove through the packaged public route that an explicitly opted-in workspace is actually served from the verified v2 materialization, not from a successful legacy fallback, while the non-opted-in default and all publication remain legacy. The tests target route ambiguity, fallback hidden in error handling, an unverified/partial carrier mount, carrier deletion while mounted, cleanup ordering, and activation overhead/resource retention.

Invariants:

1. Strict selection is explicit and immutable before workspace creation.
2. Success reports `selected_read_source=candidate_v2_strict`, the expected `RootId` and generation, and `fallback_count=0`.
3. Candidate content/metadata is observable through ordinary public command/file APIs; outside inspection only corroborates the carrier.
4. Warm activation reads zero CAS payload; cold activation uses the Stage 05 transaction and becomes visible only after verify/fsync/rename/catalog.
5. Missing/corrupt/unsupported candidate, mount failure, cancellation, and disk full fail the public create/activation; none retries legacy.
6. Default sessions still report legacy and legacy publication remains the sole writer.
7. Destroy joins commands, unmounts, then releases the carrier guard; logical and physical resource gates hold.

The route is runnable now because Stage 05 supplies real packaged candidate carriers and current workspace/namespace execution consumes native lower directories. The exact feature seam is generated typed configuration/allowlist for `candidate_read_strict` plus existing public workspace create/execute/destroy and structured activation observation. Candidate publication/OCC/durable leases, pack/GC, candidate squash, mixed-root authority, default enablement, soak, and full qualification are deferred.

## 2. Existing assets to reuse

| Asset | Exact path | Use |
| --- | --- | --- |
| Workspace create/execute/destroy | `ephemeral-sandbox-test/e2e/runtime/workspace_session/test_workspace_session.py` | public session and native command assertions |
| Finalize/cancel lifecycle | `e2e/runtime/workspace_session/test_exec_finalize.py` | command owner teardown and terminal retention |
| Publish/session cases | `e2e/runtime/workspace_session/test_publish_workspace_session.py` | legacy publication input and public tree oracle |
| Workspace helpers | `e2e/runtime/workspace_session/helpers.py` | snapshots, tree digest, tracked cleanup |
| Typed declarations | `e2e/harness/catalog/declarations.py:17-48` | stable IDs, full metadata, validation reporter |
| Gateway custody/config | `e2e/harness/runner/config.py`; `e2e/harness/runner/gateway.py` | generated config, fresh/reuse binary, safe restoration |
| Resource samplers | `e2e/observability/resource_isolation/helpers.py`; `e2e/observability/resource_efficiency/helpers.py`; `e2e/observability/resource_efficiency/profile.py`; `e2e/observability/resource_efficiency/test_workspace_reclaim.py` | process/cgroup/FD/mount/allocated-byte evidence |
| Benchmark CLI/presets | `benchmark/backend/benchmark_lab/cli.py`; `benchmark/presets/active-session.yml`; `benchmark/presets/publication.yml`; `benchmark/presets/quick-smoke.yml` | existing scheduler and paired operation vocabulary |
| Stage 05 artifacts | `.e2e-state/runs/<stage05-run-id>/evidence/`; `.benchmark-state/results/<stage05-benchmark-run-id>/` | exact root/generation/tree digest and hydration control |
| Append-only report | `e2e/test-report.md` | feature-by-feature plan/result log |

Use public file APIs to prove helper independence on the pinned Ubuntu 24.04 target. No executable is added to the target image merely to inspect its filesystem.

## 3. Resulting test tree

```text
ephemeral-sandbox/
├── crates/sandbox-runtime/layerstack/tests/strict_activation.rs         [add]
├── crates/sandbox-runtime/operation/tests/strict_candidate_activation.rs [add]
└── crates/sandbox-runtime/workspace/tests/candidate_base_lifecycle.rs   [add]

ephemeral-sandbox-test/
├── e2e/runtime/layerstack_phase1/
│   ├── activation_helpers.py                                           [add] — config/route/carrier custody
│   ├── test_strict_candidate_activation.py                            [add]
│   └── test_spec.md                                                    [modify] — typed Phase 1 catalog
├── benchmark/presets/strict-activation-tiny.yml                        [add]
├── benchmark/tests/fixtures/golden/layerstack_phase1/
│   ├── strict-activation-tiny.json                                     [add] — deterministic corpus manifest
│   └── activation_result_v1.json                                       [add] — result validation fixture
├── .e2e-state/runs/<run-id>/evidence/                                 [add] — emitted at run time
│   ├── declaration-results.json                                        [add] — emitted at run time
│   ├── activation-routes.jsonl                                         [add] — emitted at run time
│   ├── eos-before.json                                                 [add] — emitted at run time
│   ├── eos-pre-visible.json                                            [add] — emitted at run time
│   ├── eos-success.json                                                [add] — emitted at run time
│   ├── eos-failure.json                                                [add] — emitted at run time
│   ├── eos-cleanup.json                                                [add] — emitted at run time
│   ├── public-tree-digests.json                                        [add] — emitted at run time
│   ├── mount-carrier-proof.json                                        [add] — emitted at run time
│   ├── resource-summary.json                                           [add] — emitted at run time
│   ├── benchmark-raw.json                                              [add] — emitted at run time
│   ├── dependency-before.json                                          [add] — emitted at run time
│   └── dependency-after.json                                           [add] — emitted at run time
├── .benchmark-state/runs/<benchmark-run-id>/                           [add] — emitted at run time; lab-owned
└── .benchmark-state/results/<benchmark-run-id>/                        [add] — emitted at run time; lab-owned
```

### Full `/eos` state and visibility boundaries

```text
/eos/
├── layer-stack/
│   ├── .storage-writer.lock
│   ├── manifest.json                                                   legacy v1 publication/default read authority
│   ├── workspace.json                                                  legacy v1 workspace binding
│   ├── base/<base_id>/
│   ├── layers/<layer_id>/
│   ├── staging/<layer_id>.staging/
│   ├── .layer-metadata/
│   │   ├── <layer_id>.digest
│   │   └── <layer_id>.bytes
│   ├── format-v2.json
│   ├── roots/v2/<prefix>/<RootId>.root
│   ├── manifests/v2/<prefix>/<TreeManifestId>.manifest
│   ├── objects/v1/loose/                                               reserved-empty through Stage 06
│   ├── packs/v1/
│   │   ├── open/                                                       reserved Stage 08
│   │   └── sealed/                                                     reserved Stage 08
│   ├── indexes/v1/
│   │   ├── pages/<page_id>.idx
│   │   └── index.catalog
│   ├── catalogs/v1/
│   │   ├── roots.catalog
│   │   ├── locators.catalog                                            maps ObjectId to verified immutable v1 carrier range
│   │   ├── materializations.catalog                                   active; maps MaterializationKey=(RootId,backend_kind,backend_format_version,target_profile) to MaterializationId, generation, carriers
│   │   ├── leases.catalog                                              reserved Stage 07
│   │   └── retention.catalog                                          reserved Stage 08
│   ├── journals/v1/
│   │   ├── publication/
│   │   ├── hydration/<txn_id>.journal
│   │   ├── squash/
│   │   ├── compaction/
│   │   └── migration/
│   ├── staging/v2/
│   │   ├── publication/
│   │   ├── hydration/<txn_id>/
│   │   ├── squash/
│   │   ├── compaction/
│   │   └── migration/
│   ├── leases/v1/                                                     reserved Stage 07
│   ├── retention/v1/                                                  reserved Stage 08
│   ├── maintenance/v1/                                                reserved Stage 08
│   ├── materializations/docker-overlayfs/v1/<MaterializationId>/
│   │   └── carriers/<ordinal>/                                        strict selected lower carrier
│   ├── quarantine/v1/<typed-id>/                                      never selectable
│   └── trash/v1/                                                      reserved Stage 08
├── workspace/
│   ├── manager.json
│   ├── .export/<spool_id>
│   └── <workspace_session_id>/
│       ├── upper/
│       ├── work/
│       └── executions/<execution_id>/transcript.log
├── namespace_execution/<legacy>/transcript.log                        compatibility only; no new writes
├── storage/
│   ├── file_auditability/
│   └── workspace_recovery/
└── runtime/daemon/
    ├── runtime.sock
    └── runtime.pid
```

| Boundary | Required state |
| --- | --- |
| Before | Legacy head and paired ready v2 root exist; strict generation either absent (cold case) or catalog-ready (warm case); no tracked session/guard/mount. |
| Cold pre-visible | Stage 05 hydration journal/staging may exist, but catalog and mount do not refer to it; public strict workspace is not created. |
| Activation visibility | Catalog-ready verified generation → immutable plan → guard acquired → mount succeeds; structured route is emitted with root/generation and zero fallback. |
| Success | Public command/file/metadata digest equals candidate golden; mount lower resolves to expected carrier; legacy head is unchanged; warm retry has zero CAS payload reads. |
| Failure | Corrupt/missing candidate or injected mount error produces public strict failure, no legacy mount/read, `fallback_count=0`, no leaked session/mount/guard. |
| Active destroy | Carrier remains while command/mount exists; command owners reach zero, then unmount, then guard release; another session remains intact. |
| Rollback/cleanup | Generated opt-in removed; a new default session is legacy; tracked sessions/mounts/uppers/transcripts gone; candidate source/carrier and legacy state retained. |

Outside inspection proves the final lower carrier, allocated bytes, and absence of partial/foreign paths. Only public APIs prove what the workload saw and how errors surfaced.

## 4. Typed E2E case catalog

Every row below uses only the Phase 1 pinned Ubuntu 24.04 target image.
Required host and release-runner coverage remains mandatory at each row's
listed disposition, while cross-image acceptance is deferred beyond Phase 1.

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `phase1.stage06.strict.activation` | POC; `run-now-focused` | strict v2 cold/warm plus legacy default control | paired Stage 05 root, generated allowlist, candidate-distinguishing metadata | public create, execute, file, destroy in strict/default sessions | actual candidate source/root/generation, fallback zero, legacy default preserved, warm zero payload | diagnostic select/hydrate/prepare/mount/execute/destroy phases | all categories with no per-session carrier copy | guards, mounts, FDs, tasks, permits quiesce | scalar identity and helper-independence proof on pinned Ubuntu 24.04 | `120000` ms | route, tree, mount, resource evidence |
| `phase1.stage06.strict.no-fallback` | POC; `run-now-focused` | strict corruption/mount failure and rollback | corrupt copy-on-write locator/object and mount failpoint | public strict create, remove opt-in, create default | strict typed failure, legacy resolver never called, fallback zero, rollback affects only new sessions | diagnostic failure and rollback phases | no visible partial or new legacy bytes | no leaked session, guard, mount, hydration owner | no target-image helper | `120000` ms | failure call trace and trees |
| `phase1.stage06.strict.tiny` | POC; `run-now-tiny-bench` | legacy control versus strict candidate | frozen tiny corpus, warm/cold labels, one daemon | benchmark lab public lifecycle, command, PTY sentinel | exact output, metadata, route, and zero strict fallback | two warmups and six raw pairs | complete envelope and carrier reuse | twelve cycles including cancellation | graph snapshots | `60000` ms | raw and summary JSON |
| `phase1.final.strict.qualification` | final; `planned-final` | release candidate full matrix | frozen Stage 11 corpus and required runners using one pinned Ubuntu 24.04 target image | affected regression and qualification | all strict route, failure, rollback, resource, and required-runner cases | normative matched metrics | complete physical envelope | full memory/history matrix | every required release runner, one pinned target image; cross-image deferred beyond Phase 1 | `300000` ms | Stage 11 qualification bundle |

Complete `@e2e_test` metadata:

| Stable ID | Title | Description | Features | Validations | Validation features | Execution surface | Owner ID | Timeout (ms) | Pytest markers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `phase1.stage06.strict.activation` | `Stage 06 strict cold and warm candidate activation` | `Activates the paired v2 root through public workspace APIs, proves actual candidate bytes and generation, and confirms warm zero-read behavior with unchanged legacy default and publication.` | `("storage.candidate_activation","migration.candidate_read_strict","runtime.workspace_session")` | `{"strict-route":"The opted-in session selects candidate_v2 strict read authority.","candidate-tree-visible":"Public file, command, and PTY operations observe the exact candidate materialization tree and generation.","fallback-zero":"The strict route never calls or selects a legacy resolver.","warm-zero-payload":"A warm activation reuses the durable carrier without candidate payload reads.","legacy-default-preserved":"Unselected sessions and public publication remain legacy-authoritative.","guard-order":"Carrier and mount guards outlive every dependent session operation.","cleanup-complete":"Sessions, guards, mounts, workers, permits, tasks, and file descriptors quiesce."}` | `{"strict-route":("storage.candidate_activation","migration.candidate_read_strict"),"candidate-tree-visible":("storage.candidate_activation","runtime.workspace_session"),"fallback-zero":("migration.candidate_read_strict",),"warm-zero-payload":("storage.candidate_activation","observability.resource_efficiency"),"legacy-default-preserved":("migration.candidate_read_strict","runtime.workspace_session"),"guard-order":("storage.candidate_activation","runtime.workspace_session"),"cleanup-complete":("storage.candidate_activation","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `120000` | `("smoke","phase1","config")` |
| `phase1.stage06.strict.no-fallback` | `Stage 06 strict failure has no legacy fallback` | `Injects candidate integrity and mount failures, proves the legacy resolver is never invoked, and verifies configuration rollback for later sessions.` | `("storage.candidate_activation","storage.integrity","migration.rollback")` | `{"strict-failure":"Candidate corruption and mount faults return the declared strict typed error.","legacy-call-count-zero":"The legacy resolver call count remains exactly zero for every strict failure.","fallback-zero":"No route or diagnostic records a fallback attempt or completion.","partial-not-mounted":"No partial candidate carrier becomes mounted or visible.","rollback-new-session-legacy":"Removing opt-in changes only later sessions, which return to explicit legacy authority.","logical-release":"Failed and rolled-back sessions release guards, mounts, hydration owners, tasks, and file descriptors."}` | `{"strict-failure":("storage.candidate_activation","storage.integrity"),"legacy-call-count-zero":("migration.candidate_read_strict","migration.rollback"),"fallback-zero":("migration.candidate_read_strict",),"partial-not-mounted":("storage.candidate_activation","storage.integrity"),"rollback-new-session-legacy":("migration.rollback","runtime.workspace_session"),"logical-release":("storage.candidate_activation","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `120000` | `("medium","phase1","config")` |
| `phase1.stage06.strict.tiny` | `Stage 06 strict activation tiny sentinel` | `Alternates legacy and strict public lifecycles over the deterministic tiny corpus and records route, time, disk, and memory evidence.` | `("benchmark.activation","observability.resource_efficiency","migration.candidate_read_strict")` | `{"paired-result-equal":"Every legacy control and strict candidate pair returns identical output and metadata.","strict-fallback-zero":"Every strict sample reports candidate_v2 authority and zero fallback calls.","all-ops-under-60s":"Every lifecycle, command, PTY, and cleanup operation finishes within sixty seconds.","logical-release":"Sessions, guards, mounts, workers, permits, and tasks return to settled values after every repetition.","memory-cap":"Physical memory remains within the declared diagnostic cap or is explicitly unavailable.","artifact-complete":"Raw pairs, route, disk, memory, environment, correctness, and cleanup evidence validate."}` | `{"paired-result-equal":("benchmark.activation","migration.candidate_read_strict"),"strict-fallback-zero":("migration.candidate_read_strict",),"all-ops-under-60s":("benchmark.activation",),"logical-release":("storage.candidate_activation","observability.resource_efficiency"),"memory-cap":("benchmark.activation","observability.resource_efficiency"),"artifact-complete":("benchmark.activation","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `60000` | `("smoke","benchmark","phase1","config")` |
| `phase1.final.strict.qualification` | `Final strict activation qualification` | `Executes the frozen full correctness, failure, performance, memory, soak, rollback, and required host/release-runner matrix using the one pinned Ubuntu 24.04 target image in Stage 11; cross-image qualification is deferred beyond Phase 1.` | `("phase1.qualification","storage.candidate_activation","portability","ubuntu-24.04")` | `{"terminal":"All strict activation route, no-fallback, corruption, mount, rollback, correctness, time, space, memory, soak, and required-runner gates execute successfully against the pinned Ubuntu 24.04 target image with complete evidence; no cross-image acceptance is claimed."}` | `{"terminal":("phase1.qualification","storage.candidate_activation","observability.resource_efficiency","portability","ubuntu-24.04")}` | `"cli"` | `"phase1-storage"` | `300000` | `("release","phase1","config")` |

Every declared checkpoint emits exactly one terminal `ValidationReporter`
record.

## 5. Correctness and failure matrix

| Scenario | Disposition | Required proof |
| --- | --- | --- |
| Empty, 1 KiB edit, 1 MiB incompressible, 256 small files | tiny now | public candidate output/tree/metadata exact; route/root/generation explicit |
| Insert/delete/replace/rename, modes, symlink, whiteout, opaque directory, sparse | focused now | candidate-distinguishing tree visible through public API |
| Cold versus warm | focused now | cold uses Stage 05 transaction; warm same generation and zero payload reads |
| Non-opted legacy control | focused now | public legacy source and unchanged publication head |
| Missing/truncated/corrupt/wrong-root/wrong-generation/quarantined candidate | Rust exhaustive; one packaged now | strict public failure, legacy call 0, fallback 0 |
| Mount failure after guard / workspace creation | packaged now | rollback unmount/delete/release, no partial public session |
| Cancellation/timeout/disk full | Rust plus cancellation tiny now | no fallback, joined cleanup; deterministic recovery |
| Daemon restart with active/recoverable workspace | focused representative or Rust now | no plan reconstructed from alternate source; recovery cleanup |
| Concurrent strict sessions same carrier | focused now | one carrier, independent upper/work/transcripts, bounded guard count |
| Active guard while cleanup requested | focused now | carrier not deleted until unmount/release |
| Candidate publish/OCC/conflicts/durable leases | deferred-to-stage_07 | absent |
| Pack/GC lease interactions | deferred-to-stage_08 | absent |
| Squash build/commit/remount | deferred-to-stage_09 | absent |
| Mixed roots/authority/default/soak | deferred-to-stage_10 and planned-final | not current authority |
| Full required host/release-runner matrix using the sole pinned Ubuntu target | planned-final | Stage 11; unavailable required rows are unverified |

No generic successful command is accepted. Every strict assertion needs structured route, root/generation, actual candidate-distinguishing bytes, and `fallback_count=0`.

## 6. Tiny correctness and benchmark loop

`strict-activation-tiny.yml` uses seed `0x5A06`, the sole Phase 1 target
`ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`
and its resolved platform manifest, the same
daemon/filesystem/cache protocol/corpus for control and candidate, and
alternating order. Corpus: empty/no-op; 1 KiB edit in deterministic 1 MiB;
1 MiB incompressible; 256 metadata-rich small files (~1 MiB); histories
1/8/32. Include a short PTY create/write/read/control-D path and a cancellation
path.

Use two warmup pairs and six measured alternating pairs. Candidate cycles alternate one forced cold generation and warm reuse; every pair records route and digest. Preserve raw samples and ratios; do not claim normative p95.

Hard/candidate diagnostics: whole loop ≤60 s; every operation ≤60 s; fallback 0; warm CAS payload reads 0; lower depth ≤64; exact output/metadata; Stage 05 buffers/workers/queue/64 MiB semaphore/shared 16 MiB cache; managed ≤4 MiB/op excluding cache; RSS ≤384 MiB and ≤128 MiB above idle. Alert lines use root/session and mount `baseline+5%+2 ms`, no-op `+3%+0.5 ms`, throughput ≥97%, PTY create `+3%+1 ms`, other PTY actions `+3%+0.5 ms`, cold ≥70% copy and `1.5× copy + warm allowance`. The focused route/caps are gates; normative sample-size p50/p95 remains Stage 11.

## 7. Memory-stability and reclamation test

Stage 06 adds activation plans, carrier guards/registry entries, mount descriptors, route records, setup rollback, and composes Stage 05 hydration resources. The tiny loop runs in one long-lived packaged daemon without restart between samples.

Measure:

```text
idle -> warmed idle -> plan/hydrate/mount active peak -> command peak
-> command join -> unmount -> guard release -> scratch cleanup -> settled
```

Run 12 post-warmup candidate lifecycles: ten successful warm/cold activations, one cancelled hydration/setup, and one injected mount failure. Sample every 100 ms through a fixed ring and streamed artifact; poll observable quiescence ≤5 s. Destroyed session requires zero commands, plans, guards, registry refs, mounts, hydration transactions/workers/borrowed chunks/queue/permits, extra FDs, and scratch; cache may remain only under 4,096/16 MiB.

Freeze physical noise from equal-order control before candidate as `max(8 MiB,4×control MAD)`. Mandatory logical result is ephemeral resources `bounded-and-released`; cache is `bounded-retained-by-design`. Mandatory physical result is both RSS ceilings and no unexplained positive settled slope/delta outside band. Attribute anonymous/file RSS/page cache. Restart/purge/allocator substitution is prohibited. Missing gate data, suspected/confirmed leak, or growing live gauges blocks. Full scale/history/sustained matrix is Stage 11.

## 8. Dependency and portability proof

Canonical before/after `cargo metadata --locked --all-features --format-version 1` must have identical resolved external package/version/source/checksum set, enabled external features, and product-wide direct external edge multiset. `Cargo.lock`, all manifests, Python environment, system tools, runtime services, and target-image helpers add nothing. List internal activation module edges separately; run cycle/forbidden-edge checks and reject portable core references to native paths or Docker.

Re-run one scalar SeqCDC/root/object golden to prove identity stability;
acceleration is explicitly absent, so its differential is not applicable.
Focused portability uses public file/command APIs with the sole pinned Ubuntu
OCI index and proves no target shell, libc utility, tar, cp, package manager,
or helper invocation. Read-only and non-root runtime variants use that same
target identity. Current host/CPU evidence qualifies only that row. Stage 11
executes every required arm64/amd64 host/release-runner row using the same OCI
index and records the resolved platform manifest; unavailable required final
rows remain unverified/no-go. Cross-image portability is deferred beyond
Phase 1 and is neither an acceptance nor a retirement gate.

## 9. Focused and final-stage commands

Follow append-only `e2e/test-report.md` discipline. The first packaged case rebuilds; reuse only an unchanged binary after it passes.

### Product formatting, lint, and focused unit/integration

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack -p sandbox-runtime-workspace -p sandbox-runtime --all-targets --all-features -- -D warnings
cargo test -p sandbox-runtime-layerstack strict_activation -- --nocapture
cargo test -p sandbox-runtime-workspace candidate_base_lifecycle -- --nocapture
cargo test -p sandbox-runtime strict_candidate_activation -- --nocapture
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

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 E2E_REBUILD_BINARY=1 PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_strict_candidate_activation.py::test_strict_cold_warm_activation \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox

E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 E2E_REBUILD_BINARY=0 PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_strict_candidate_activation.py::test_strict_failure_never_falls_back \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

### Tiny benchmark validate/run

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin \
  --plan strict-activation-tiny
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin \
  --plan strict-activation-tiny
# Recover validates all owned journals; its current CLI intentionally has no --plan.
../.benchmark-state/test-venv/bin/sandbox-benchmark recover \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

Planned test/preset files are stage deliverables. The CLI writes run-owned output beneath `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.benchmark-state/{runs,results}/<run-id>/`; it has no `--output` option. Current CLI options/package names (except stage-created core), flags, and workdirs were inspected. Record build-lock wait separately.

### Artifact compatibility validation

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.benchmark-state/test-venv/bin/python -m pytest \
  benchmark/backend/tests/compatibility/test_artifacts.py
```

### DO NOT RUN in Stage 06 — Stage 11 affected regression

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

### DO NOT RUN in Stage 06 — Stage 11 native-host/pinned-Ubuntu-24 matrix

Stage 11 runs this command once per applicable required host. Pinned Ubuntu
24.04 is the only Phase 1 target image; cross-image portability is deferred
beyond Phase 1 and is not an acceptance gate.

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

### DO NOT RUN in Stage 06 — Stage 11 full Phase 1 qualification

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

| Field | Definition / source | Sampling / aggregation | Control | Target / hard ceiling | Missing policy / artifact |
| --- | --- | --- | --- | --- | --- |
| `selected_read_source` | immutable route chosen before setup | structured result each session | legacy control | strict=`candidate_v2_strict` | blocker; routes JSONL |
| `fallback_count`, `legacy_resolver_calls` | alternate-source attempts | resolver counters each success/failure | 0 | exactly 0 | blocker |
| `root_id`, `materialization_generation` | selected candidate identity/carrier | result + catalog cross-check | Stage 05 expected | exact | blocker |
| `public_tree_digest_equal` | public candidate view vs golden | file APIs/tree digest | paired legacy/candidate | true | blocker |
| `activation_component_ns` | selection/hydrate/prepare/mount/unmount | monotonic timer, raw per pair | legacy same host/order | each <60 s; diagnostics §6 | absent blocks |
| `cas_payload_reads` | verified payload reads | per activation | warm candidate | warm 0 | blocker |
| `allocated_bytes.<category>` | full filesystem allocated blocks | boundaries/peak/settled | control | no per-session carrier duplication; full envelope | unknown blocks |
| `active_plans/guards/mounts/fds/tasks/permits` | product live gauges | 100 ms ring, peaks/settled | warmed idle | zero for destroyed session; inherited caps | blocker |
| `rss_total/anon/file`, `cgroup_current/peak` | daemon/cgroup scopes | 100 ms; peak/windows/slope | equal warmup | ≤384 MiB, idle +128 MiB | required missing blocks |
| `quiescence_ms`, `settled_slope` | poll to all idle / Theil–Sen | each cycle, n=12 | frozen band | ≤5 s, not beyond band | blocker |
| `external_graph_delta` | canonical graph/features/edges symmetric diff | once | Stage 05 | empty | blocker |

All values include units, numerator/denominator where ratios exist, scope, and `measured|derived|estimated|unknown`. Raw high-frequency samples stream to bounded artifacts; the test retains only fixed windows/reservoir summaries.

## 11. Stage exit verdict

Pass requires all three run-now cases, focused Rust/static/golden checks,
artifacts, exact graph equality, current-host single-image/no-helper proof, and
cleanup. Every strict success and failure must have the intended v2
root/source and fallback/legacy-call counts of zero. Candidate public view must
be exact; default/publication must remain legacy. Logical resources must
release in order and physical caps/trend must pass.

Only attributed allocator/page-cache retention within the frozen band or optional unavailable split counters are warnings. Wrong/ambiguous route, fallback, accepted corruption, partial mount, carrier deletion while active, setup residue, legacy publication change, op ≥60 s, memory/worker/depth cap breach, suspected/confirmed leak, missing gate evidence, dependency/runtime/helper delta, or incomplete artifact/cleanup is disqualifying.

Cleanup is run-ID/session scoped, restores config and gateway custody, and retains roots/objects/ready carrier plus all legacy state. Rebuild on product changes and rerun only the failed focused node after diagnosis. A disqualifier triggers opt-in disablement for future sessions; active sessions are explicitly drained. Stage 07 owns candidate-private publication/durable leases; Stage 08 packs/GC; Stage 09 squash; Stage 10 authority; Stage 11 final regression/performance/memory/portability/soak/rollback qualification.
