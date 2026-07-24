# Stage 05 E2E — Private candidate materialization

Links: [implementation overview](../index.md) · [stage specification](spec.md) · [benchmark note](benchmark_note.md) · [quantitative contract](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Tier: **POC proof tier**. Run only the smallest packaged `dual_read_verify` case, one corruption/restart case, and one sub-minute tiny benchmark/memory sentinel. Candidate activation and normative qualification do not belong here.

## 1. Stage-local test objective

Implementation execution is blocked unless the product worktree is on the
exact fresh branch `upgrade-2.0-phase-1`, created from the newest approved
immutable product revision, with its base commit, upstream, clean scoped
worktrees, and responsible implementer recorded before any code edit. This
planning stage creates or switches no branch; any mismatch is a hard blocker.

Prove that a real packaged Stage 04 shadow root can be reconstructed privately from typed object identities resolved through verified immutable v1-carrier byte-range locators into an exact Docker/OverlayFS native tree, with bounded resources and crash-atomic visibility, while legacy v1 remains the sole public writer, publisher, and reader. The critical risks are silent content/metadata divergence, use of a partially written carrier, unverified object bytes, public candidate serving, unbounded hydration memory, orphaned transactions, and target-image helper dependence.

Invariants:

1. `write_authority=legacy_v1`, `public_read_source=legacy_v1`, `candidate_served=false`.
2. Every comparison pairs the one committed legacy result with its one derived v2 root; zero competing publication occurs.
3. Cold hydration verifies typed object hashes, reconstructs exact tree/content/metadata, fsyncs, atomically exposes one generation, then catalogs it.
4. Warm hydration returns that generation with zero CAS payload reads.
5. Corruption, cancellation, disk-full, or crash never makes a partial generation catalog-visible; restart deterministically completes or cleans it.
6. `comparison_count` is exact and `mismatch_count=0`; mismatch is never silent.
7. All changed owners, permits, buffers, tasks, FDs, and transactions quiesce; physical caps hold.

This route is runnable before Stage 06 because `dual_read_verify` is architecturally useful packaged shadow work but never mounts the candidate. The public CLI creates/edits/publishes and reads the legacy result; structured operation evidence and approved outside inspection prove candidate work. Strict activation, fallback semantics, candidate publication/OCC/leases, pack/GC, squash/remount, authority cutover, and final matrices remain deferred.

## 2. Existing assets to reuse

| Asset | Path | Use |
| --- | --- | --- |
| Workspace publish cases | `ephemeral-sandbox-test/e2e/runtime/workspace_session/test_publish_workspace_session.py` | public create/edit/publish/read oracle and tracked cleanup |
| Workspace helpers | `e2e/runtime/workspace_session/helpers.py` | exact snapshots, archive/tree digest, gateway custody |
| Manager export cases | `e2e/manager/management/export/` | streaming tree/archive digest and `.export` cleanup patterns |
| Manager squash cases | `e2e/manager/management/squash/` | timing/artifact vocabulary only; no squash gate now |
| Typed test declarations | `e2e/harness/catalog/declarations.py:17-48` | immutable metadata and validation checkpoints |
| Resource samplers | `e2e/observability/resource_isolation/helpers.py`; `e2e/observability/resource_efficiency/helpers.py`; `e2e/observability/resource_efficiency/profile.py`; `e2e/observability/resource_efficiency/test_workspace_reclaim.py` | process/cgroup/FD/allocated-byte and quiescence evidence |
| Benchmark CLI | `benchmark/backend/benchmark_lab/cli.py` | current `validate`, `run`, `compare`, `recover`, `cleanup` scheduler |
| Relevant preset families | `benchmark/presets/publication.yml`; `benchmark/presets/payload-scaling.yml`; `benchmark/presets/workspace-size-count.yml`; `benchmark/presets/quick-smoke.yml` | paired workloads and physical-space categories |
| Stage 02–04 goldens | product `crates/sandbox-runtime/layerstack-core/tests/` and Stage 04 shadow artifacts | frozen `RootId`, SeqCDC, object, manifest, legacy/candidate pairing |
| Append-only report | `e2e/test-report.md` | record plan before each live command and result after |

Outside inspection may read `/eos` tree state and allocated blocks. It must not replace public behavior, structured route authority, or typed comparison results.

## 3. Resulting test tree

```text
ephemeral-sandbox/
├── crates/sandbox-runtime/layerstack-core/tests/
│   └── materialization_contract.rs                                [add] — neutral port/schema and streaming vectors
├── crates/sandbox-runtime/layerstack/tests/
│   ├── materialization_golden.rs                                 [add] — exact file/metadata tree
│   └── materialization_recovery.rs                               [add] — every hydration visibility failpoint
└── crates/sandbox-runtime/operation/tests/dual_read_verify.rs     [add] — legacy authority/candidate comparison

ephemeral-sandbox-test/
├── e2e/runtime/layerstack_phase1/
│   ├── materialization_helpers.py                                [add] — tracked candidate config/tree/resources
│   ├── test_candidate_materialization.py                         [add] — focused cases
│   └── test_spec.md                                              [add] — typed Phase 1 catalog
├── benchmark/presets/candidate-materialization-tiny.yml          [add]
├── benchmark/tests/fixtures/golden/layerstack_phase1/
│   ├── candidate-materialization-tiny.json                       [add] — deterministic corpus manifest
│   └── materialization_result_v1.json                            [add] — result validation fixture
├── .e2e-state/runs/<run-id>/evidence/                            [add] — emitted at run time
│   ├── declaration-results.json                                  [add] — emitted at run time
│   ├── route-comparison.jsonl                                    [add] — emitted at run time
│   ├── eos-before.json                                           [add] — emitted at run time
│   ├── eos-pre-visible.json                                      [add] — emitted at run time
│   ├── eos-success.json                                          [add] — emitted at run time
│   ├── eos-failure-<failpoint>.json                              [add] — emitted at run time
│   ├── eos-cleanup.json                                          [add] — emitted at run time
│   ├── tree-digests.json                                         [add] — emitted at run time
│   ├── resource-summary.json                                     [add] — emitted at run time
│   ├── benchmark-raw.json                                        [add] — emitted at run time
│   ├── dependency-before.json                                    [add] — emitted at run time
│   └── dependency-after.json                                     [add] — emitted at run time
├── .benchmark-state/runs/<benchmark-run-id>/                     [add] — emitted at run time; lab-owned
└── .benchmark-state/results/<benchmark-run-id>/                  [add] — emitted at run time; lab-owned
```

### Full storage tree and state boundaries

```text
/eos/
├── layer-stack/
│   ├── .storage-writer.lock
│   ├── manifest.json                                               legacy v1 sole public authority
│   ├── workspace.json                                              legacy v1 workspace binding
│   ├── base/<base_id>/                                             legacy v1 native base
│   ├── layers/<layer_id>/                                          legacy v1 whole-file layer
│   ├── staging/<layer_id>.staging/                                 legacy v1 publication staging
│   ├── .layer-metadata/
│   │   ├── <layer_id>.digest
│   │   └── <layer_id>.bytes
│   ├── format-v2.json
│   ├── roots/v2/<prefix>/<RootId>.root
│   ├── manifests/v2/<prefix>/<TreeManifestId>.manifest
│   ├── objects/v1/loose/                                              reserved-empty through Stage 06
│   ├── packs/v1/
│   │   ├── open/                                                   reserved until Stage 08
│   │   └── sealed/                                                 reserved until Stage 08
│   ├── indexes/v1/
│   │   ├── pages/<page_id>.idx
│   │   └── index.catalog
│   ├── catalogs/v1/
│   │   ├── roots.catalog
│   │   ├── locators.catalog                                       maps ObjectId to verified immutable v1 carrier range
│   │   ├── materializations.catalog                               maps MaterializationKey=(RootId,backend_kind,backend_format_version,target_profile) to MaterializationId, generation, carriers
│   │   ├── leases.catalog                                        reserved until Stage 07
│   │   └── retention.catalog                                     reserved until Stage 08
│   ├── journals/v1/
│   │   ├── publication/
│   │   ├── hydration/<txn_id>.journal                             hydration active
│   │   ├── squash/                                                 reserved until Stage 09
│   │   ├── compaction/                                             reserved until Stage 08
│   │   └── migration/
│   ├── staging/v2/
│   │   ├── publication/
│   │   ├── hydration/<txn_id>/                                    active; never reader-visible
│   │   ├── squash/                                                 reserved until Stage 09
│   │   ├── compaction/                                             reserved until Stage 08
│   │   └── migration/
│   ├── leases/v1/                                                 reserved Stage 07
│   ├── retention/v1/                                              reserved Stage 08
│   ├── maintenance/v1/                                            reserved Stage 08
│   ├── materializations/docker-overlayfs/v1/<MaterializationId>/
│   │   └── carriers/
│   │       └── <ordinal>/                                         verified rebuildable private lower carrier
│   ├── quarantine/v1/<typed-id>/                                  corrupt evidence, never a read source
│   └── trash/v1/                                                  reserved Stage 08
├── workspace/
│   ├── manager.json
│   ├── .export/<spool_id>
│   └── <workspace_session_id>/
│       ├── upper/
│       ├── work/
│       └── executions/<execution_id>/transcript.log
├── namespace_execution/<legacy>/transcript.log                    compatibility only, no new writes
├── storage/
│   ├── file_auditability/
│   └── workspace_recovery/
└── runtime/daemon/
    ├── runtime.sock
    └── runtime.pid
```

| Boundary | Required state |
| --- | --- |
| Before | Legacy head/layers and exactly paired Stage 04 root/manifest/object-locator records exist; every locator names a verified immutable v1 carrier range; `objects/v1/loose/` is empty; no tracked ready materialization or hydration residue exists. |
| Prepared/object streaming | `hydration/<txn>.journal` and `staging/v2/hydration/<txn>` may exist; catalog has no new generation and the public CLI still reads legacy. |
| Visibility boundary | Only after full typed verification, metadata construction, file/directory fsync, and atomic rename may final carrier exist; only after parent fsync may catalog generation advance. |
| Success | Ready carrier tree/content/metadata digest equals legacy oracle; catalog points to it; warm retry performs zero CAS payload reads; candidate was not mounted. |
| Failure before rename | No final generation/catalog record; staging/journal terminal-aborted or recoverable; all permits/tasks release. |
| Crash after rename/before catalog | Restart verifies the unreferenced final carrier and either catalogs it once or deletes it; never serves it publicly. |
| Corrupt object/index/journal | Typed failure and quarantine evidence; previous catalog generation remains; legacy public behavior succeeds; mismatch/error is structured. |
| Cleanup/rollback | Harness removes tracked session/config; product removes only incomplete staging and a catalog-proven rebuildable carrier when requested; roots/manifests/locators and all legacy state remain. |

## 4. Typed E2E case catalog

Run-now rows below use the stage-local pinned Ubuntu 24.04 target image and do
not qualify portability. Stage 11 must run required hosts/release runners and
the full Prep 04 Phase-1 image matrix: pinned Ubuntu/Debian glibc, Alpine
musl, minimal/distroless, shell-less, read-only, and non-root.

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `phase1.stage05.materialization.compare` | POC; `run-now-focused` | `dual_read_verify`, cold then warm | generated config, Stage 04 shadow, metadata-rich deterministic tree | public edit, publish, read twice | legacy authority, exact private candidate tree, atomic generation, warm zero payload, mismatch zero | diagnostic hydration and comparison phases | complete categorized bytes and bounded peak | buffers/workers/permits/FDs/transactions return | scalar identity unchanged and no target helper | `120000` ms | route, trees, catalog/journal, resources |
| `phase1.stage05.materialization.corruption-restart` | POC; `run-now-focused` | cold integrity failure and recovery | copy-on-write object locator and post-rename failpoint | public publish/read and controlled restart | typed corruption, quarantine, no partial catalog, deterministic recovery, legacy unaffected | failure and recovery phases | staging/orphan allocation before/after | cancellation, joins, recovery owners release | helper-independent proof on the pinned Ubuntu 24.04 target | `120000` ms | failpoint state snapshots |
| `phase1.stage05.materialization.tiny` | POC; `run-now-tiny-bench` | legacy projection versus private candidate | frozen tiny corpus, seed, and order | benchmark lab public publish and compare | exact digests and authority with no silent mismatch | two warmups and six raw pairs | carrier/staging/index/journal bytes | twelve cycles including cancellation | graph before/after | `60000` ms | raw and summary JSON |
| `phase1.stage06.strict.activation` | later; `deferred-to-stage_06` | strict packaged candidate read | Stage 06 explicit opt-in | create and execute on candidate carrier | actual candidate source and zero fallback | diagnostic select/hydrate/mount phases | active carrier allocation | activation owners quiesce | same provider adapter and no target helper | `120000` ms | Stage 06 typed bundle |
| `phase1.final.materialization.qualification` | final; `planned-final` | full materialization matrix | frozen scale/corpus, required runners, and full Prep 04 Phase-1 image matrix | Stage 11 qualification scheduler | normative exactness, performance, space, memory, image, and required-runner gates | final matched metrics | complete physical envelope | full scaling and sustained memory | required runners plus pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root | `300000` ms | Stage 11 qualification bundle |

Complete declaration metadata:

| Stable ID | Title | Description | Features | Validations | Validation features | Execution surface | Owner ID | Timeout (ms) | Pytest markers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `phase1.stage05.materialization.compare` | `Stage 05 private cold and warm materialization comparison` | `Publishes through legacy, hydrates the paired v2 root privately, compares exact trees, and proves an idempotent warm hit.` | `("storage.layerstack_v2","storage.materialization","migration.dual_read_verify")` | `{"legacy-authority":"Every public read and publication remains legacy-authoritative.","cold-tree-equal":"The first private candidate materialization has the exact expected content tree.","metadata-equal":"Modes, links, whiteouts, opaque directories, sparse extents, and timestamps match the oracle.","atomic-visible":"Only one complete durable materialization generation becomes selectable.","warm-zero-payload-read":"The second materialization hit reads zero candidate payload bytes.","zero-mismatch":"The private comparison emits no silent or counted mismatch.","cleanup-complete":"Buffers, workers, permits, file descriptors, transactions, staging, and run-owned paths quiesce."}` | `{"legacy-authority":("migration.dual_read_verify","storage.layerstack_v2"),"cold-tree-equal":("storage.materialization","storage.layerstack_v2"),"metadata-equal":("storage.materialization","storage.layerstack_v2"),"atomic-visible":("storage.materialization",),"warm-zero-payload-read":("storage.materialization","observability.resource_efficiency"),"zero-mismatch":("migration.dual_read_verify",),"cleanup-complete":("storage.materialization","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `120000` | `("smoke","phase1","config")` |
| `phase1.stage05.materialization.corruption-restart` | `Stage 05 materialization corruption and restart recovery` | `Injects hash corruption and the post-rename and pre-catalog crash boundary and proves quarantine and deterministic recovery without public impact.` | `("storage.materialization","storage.integrity","runtime.daemon_restart")` | `{"corruption-detected":"A wrong object hash fails with the declared typed integrity error before visibility.","quarantine-recorded":"The corrupt source and reason are recorded under run-owned quarantine without replacing a good locator.","partial-not-cataloged":"A renamed but uncommitted carrier is never selectable from the materialization catalog.","restart-idempotent":"Restart recovery either installs the one durable complete generation or reaps the orphan, and retry is exact.","legacy-unaffected":"Public legacy publication, read bytes, and authority are unchanged by candidate failure.","logical-release":"Cancellation and restart join all materialization owners and return gauges to settled values."}` | `{"corruption-detected":("storage.integrity","storage.materialization"),"quarantine-recorded":("storage.integrity","storage.materialization"),"partial-not-cataloged":("storage.materialization","runtime.daemon_restart"),"restart-idempotent":("storage.materialization","runtime.daemon_restart"),"legacy-unaffected":("migration.dual_read_verify","storage.layerstack_v2"),"logical-release":("runtime.daemon_restart","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `120000` | `("medium","phase1","config")` |
| `phase1.stage05.materialization.tiny` | `Stage 05 materialization tiny sentinel` | `Alternates the legacy control and private candidate materialization over the frozen tiny corpus and records correctness, time, disk, and memory.` | `("benchmark.materialization","observability.resource_efficiency","migration.dual_read_verify")` | `{"paired-tree-equal":"Every paired control and candidate tree and metadata digest is identical.","all-ops-under-60s":"Every publication, hydration, comparison, and cleanup operation finishes within sixty seconds.","physical-peak-bounded":"Categorized peak allocation satisfies the declared diagnostic carrier and staging bound.","logical-release":"Every repetition releases materialization workers, buffers, permits, transactions, and file descriptors.","memory-cap":"Physical memory remains within the declared diagnostic cap or is explicitly unavailable.","artifact-complete":"Raw pairs, environment, disk, memory, correctness, and cleanup evidence validate against the artifact schema."}` | `{"paired-tree-equal":("benchmark.materialization","migration.dual_read_verify"),"all-ops-under-60s":("benchmark.materialization",),"physical-peak-bounded":("benchmark.materialization","observability.resource_efficiency"),"logical-release":("storage.materialization","observability.resource_efficiency"),"memory-cap":("benchmark.materialization","observability.resource_efficiency"),"artifact-complete":("benchmark.materialization","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `60000` | `("smoke","benchmark","phase1","config")` |
| `phase1.stage06.strict.activation` | `Stage 06 strict cold and warm candidate activation` | `Activates the paired v2 root through public workspace APIs, proves actual candidate bytes and generation, and confirms warm zero-read behavior with unchanged legacy default and publication.` | `("storage.candidate_activation","migration.candidate_read_strict","runtime.workspace_session")` | `{"strict-route":"The opted-in session selects candidate_v2 strict read authority.","candidate-tree-visible":"Public file and command operations observe the exact candidate materialization tree.","fallback-zero":"The strict route never calls or selects a legacy resolver.","warm-zero-payload":"A warm activation reuses the durable carrier without candidate payload reads.","legacy-default-preserved":"Unselected sessions and public publication remain legacy-authoritative.","guard-order":"Carrier and mount guards outlive every dependent session operation.","cleanup-complete":"Sessions, guards, mounts, workers, permits, and file descriptors quiesce."}` | `{"strict-route":("storage.candidate_activation","migration.candidate_read_strict"),"candidate-tree-visible":("storage.candidate_activation","runtime.workspace_session"),"fallback-zero":("migration.candidate_read_strict",),"warm-zero-payload":("storage.candidate_activation","observability.resource_efficiency"),"legacy-default-preserved":("migration.candidate_read_strict","runtime.workspace_session"),"guard-order":("storage.candidate_activation","runtime.workspace_session"),"cleanup-complete":("storage.candidate_activation","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `120000` | `("smoke","phase1","config")` |
| `phase1.final.materialization.qualification` | `Final materialization qualification` | `Executes the frozen Stage 11 correctness, failure, performance, storage, memory, soak, rollback, required host/release-runner, and Prep 04 Phase-1 image matrix.` | `("phase1.qualification","storage.materialization","portability")` | `{"terminal":"All final materialization exactness, atomicity, warm-reuse, corruption, recovery, time, physical-space, memory, required-runner, and pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root gates execute with complete evidence."}` | `{"terminal":("phase1.qualification","storage.materialization","observability.resource_efficiency","portability")}` | `"cli"` | `"phase1-storage"` | `300000` | `("release","phase1","config")` |

Every declared checkpoint emits exactly one terminal `ValidationReporter`
record.

## 5. Correctness and failure matrix

| Scenario | Disposition | Proof |
| --- | --- | --- |
| Empty, sub-chunk short, 8/16/32 KiB boundary, 1 MiB binary | Rust golden + tiny now | deterministic reconstruction and typed hash verification |
| Arbitrary object read splits | Rust property now | identical bytes/tree digest under every split schedule |
| Local insert/delete/replace/rename | tiny now | candidate/legacy exact path/content digest |
| Modes, symlinks, whiteouts, opaque directories, sparse file | focused now | exact canonical metadata/tree comparison |
| 100–1,000 small files and no-dedup binary | tiny now | bounded queue/memory, correct bytes |
| Duplicate object/repeated ensure | focused now | one ready generation; warm zero payload reads |
| Legacy v1 plus paired v2 root | focused now | public v1, private v2; explicit authority fields |
| Missing/truncated/wrong-domain/hash-mismatch object or index | Rust exhaustive; one packaged corruption now | fail closed, quarantine, previous generation stable |
| Crash before journal/object/rename/catalog and after rename | Rust every boundary; packaged representative now | no partial visibility; deterministic cleanup/commit |
| Cancellation/timeout/disk full | Rust now; cancel in tiny; disk-full focused if reliable | staging/journal recoverable, permits/tasks release |
| Fallback permitted/strict | deferred-to-stage_06 | candidate does not serve in Stage 05, so serving fallback is not applicable |
| Concurrent/stale OCC publication | deferred-to-stage_07 | legacy publication remains input authority |
| Lease during GC/compaction; pack faults | deferred-to-stage_08 | absent |
| Squash identity/remount | deferred-to-stage_09 | absent |
| Mixed-root candidate authority/rollback | deferred-to-stage_10 | public v1 only |
| Full scale, required host/release-runner, and Prep 04 Phase-1 image matrix | planned-final | Stage 11: pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root; missing rows stay unverified |

The packaged success must show `candidate_served=false`, exact paired root/generation, `comparison_count=1`, `mismatch_count=0`, and no silent error. A command that merely succeeds through legacy proves only the public oracle, not candidate materialization.

## 6. Tiny correctness and benchmark loop

Preset `candidate-materialization-tiny.yml` uses seed `0x5A05`, the sole
Phase 1 target
`ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`
and its resolved platform manifest, the same filesystem, daemon, cache
protocol, input manifest, and alternating control/candidate schedule. Corpus:
empty root; 1 KiB localized edit in deterministic 1 MiB file; 1 MiB
incompressible file; 256 small files totaling ~1 MiB with
modes/symlink/whiteout/opaque directory; history depths 1, 8, 32.

Run two warmup pairs and six measured alternating pairs. Each control derives the legacy tree digest and verified native copy-control throughput; each candidate forces cold hydration to a new run-scoped generation, verifies it, then performs one warm `ensure`. One candidate cycle cancels after object verification. Write raw per-sample JSON and absolute/ratio summary; six pairs do not support a normative p95.

Exact caps: run ≤60 s; any operation ≤60 s; exact digest/mismatch is hard; read/output buffers 256 KiB each/worker, ≤4 global workers, metadata queue 16/≤64 KiB, global permits ≤64 MiB, shared cache ≤16 MiB, managed memory/op ≤4 MiB excluding cache, RSS ≤384 MiB and ≤128 MiB above idle, carrier physical peak ≤`C_target+5%`. Warm zero payload reads is hard. Final throughput `≥70%` and warm/cold p50/p95 are reported as diagnostic lines but remain deferred-to-final.

## 7. Memory-stability and reclamation test

This stage adds buffers, borrowed views, a bounded queue/cache, workers/tasks/join handles, FDs, byte permits, transactions, and cleanup paths. Use the same long-lived packaged daemon for all measured iterations; do not restart it to obtain a passing memory result.

Collect:

```text
idle baseline -> warmed idle -> cold hydrate peak -> warm lookup
-> cancellation/failure peak -> product-observable quiescence -> settled
```

Run 12 candidate lifecycles after warmup, alternating success and the declared cancellation at fixed positions. Sample every 100 ms into a fixed ring/streamed JSONL. Poll ≤5 s for zero active hydration transactions/workers/tasks/borrowed chunks/queue items/permits/extra FDs and bounded cache/catalog values. A terminal crash fixture is excluded until its explicit restart-recovery case; after recovery it too must quiesce.

Freeze control noise before examining candidate as `max(8 MiB, 4 × control MAD)` for settled delta/slope. Mandatory logical verdict: all changed ephemeral resources `bounded-and-released`; cache only `bounded-retained-by-design`. Mandatory physical verdict: both RSS ceilings, declared working-set caps, carrier/staging peak, and no post-warmup positive settled trend beyond the band. Attribute anonymous/file RSS and filesystem page cache. Missing stage-gating data, suspected/confirmed leak, or flat RSS with growing live gauges blocks. Full scale/history and sustained campaigns are Stage 11.

## 8. Dependency and portability proof

Capture canonical locked/all-feature Cargo metadata immediately before and after. Required equality covers resolved external `(name,version,source,checksum)`, enabled external feature set, and product-wide direct external edge multiset; manifests/lock, Python environment, system tools, runtime services, and target-image helpers have zero additive delta. Internal edges into `sandbox-runtime-layerstack-core` are listed separately. Run existing cycle/forbidden-edge checks; specifically reject core imports of `/eos`, `PathBuf`, Docker, OverlayFS, libc, or operation crates.

Run the frozen scalar SeqCDC/root/object golden once to prove Stage 05 did not
change identity. Acceleration is absent, so scalar/accelerated differential is
not applicable (not silently deferred). Focused adapter proof uses the
stage-local pinned Ubuntu OCI index through public file APIs; process evidence must show no
target-image shell, tar, cp, libc utility, package manager, or helper.
Read-only and non-root runtime variants use that same target identity.
Deterministic host/CPU vectors on the available host are evidence only for that
host. Stage 11 executes the complete amd64/arm64 and required
host/release-runner matrix plus pinned Ubuntu/Debian glibc, Alpine musl,
minimal/distroless, shell-less, read-only, and non-root, recording every
resolved platform manifest. Unavailable required rows remain unverified and
cannot support claims.

## 9. Focused and final-stage commands

Append each intended live command to `e2e/test-report.md` before running it and append outcome/artifacts afterward. First packaged gate rebuilds; unchanged reruns may reuse.

### Product formatting, lint, and focused unit/integration

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack -p sandbox-runtime --all-targets --all-features -- -D warnings
cargo test -p sandbox-runtime-layerstack-core materialization -- --nocapture
cargo test -p sandbox-runtime-layerstack materialization -- --nocapture
cargo test -p sandbox-runtime dual_read_verify -- --nocapture
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
  e2e/runtime/layerstack_phase1/test_candidate_materialization.py::test_private_cold_warm_compare \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox

E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 E2E_REBUILD_BINARY=0 PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_candidate_materialization.py::test_corruption_restart_visibility \
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
  --plan candidate-materialization-tiny
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin \
  --plan candidate-materialization-tiny
# Recover validates all owned journals; its current CLI intentionally has no --plan.
../.benchmark-state/test-venv/bin/sandbox-benchmark recover \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

The planned node/preset paths are stage deliverables. The CLI writes run-owned output beneath `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.benchmark-state/{runs,results}/<run-id>/`; it has no `--output` option. Current CLI options, package names (except the stage-created core crate), rebuild/reuse semantics, and workdirs are verified. Record build-lock wait separately.

### Artifact compatibility validation

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.benchmark-state/test-venv/bin/python -m pytest \
  benchmark/backend/tests/compatibility/test_artifacts.py
```

### DO NOT RUN in Stage 05 — Stage 11 affected regression

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

### DO NOT RUN in Stage 05 — Stage 11 host/image matrix

The command below is the pinned-Ubuntu representative and runs once per
applicable required host. The Stage 11 scheduler must additionally cover
pinned Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only,
and non-root rows; this Stage 05 command alone cannot qualify the matrix.

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

### DO NOT RUN in Stage 05 — Stage 11 full Phase 1 qualification

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

| Field | Definition / source | Sampling / aggregation | Baseline | Target / ceiling | Missing policy / artifact |
| --- | --- | --- | --- | --- | --- |
| `write_authority`, `public_read_source`, `candidate_served` | structured daemon route | every op, exact | legacy mode | `legacy_v1`, `legacy_v1`, false | blocker; route JSONL |
| `comparison_count`, `mismatch_count` | completed paired comparisons/errors | every root; sum | Stage 04 pair count | exactly expected; mismatch 0 | blocker |
| `tree_digest_equal`, `metadata_digest_equal` | normalized stream digests | each materialization | legacy oracle | true | blocker; tree JSON |
| `cas_payload_reads` | verified payload read count | warm/cold separately | warm ready generation | warm 0 | blocker |
| `hydration_elapsed_ns`, `bytes_reconstructed` | monotonic component timer / receipt | 2 warmup, 6 pairs; raw, median, throughput | copy control | op <60 s; final ≥70% deferred | missing blocks correctness timing |
| `allocated_bytes.<category>` | allocated blocks for legacy, objects/packs, index/M, staging/journal, carrier, workspace, residue | before/peak/settled | paired control | carrier peak ≤`C_target+5%`; full envelope reported | unknown blocks disk verdict |
| `buffer_live_bytes`, `workers`, `queue_items/bytes`, `permits_bytes` | product gauges | 100 ms ring + peak/settled | warmed idle | exact caps in §6; zero ephemeral at quiescence | blocker |
| `rss_{total,anon,file}_bytes`, `cgroup_{current,peak}_bytes` | daemon `/proc` and cgroup scopes | 100 ms; peaks/windows/slope | equal warmup | ≤384 MiB and idle +128 MiB | required missing blocks; optional split labeled |
| `quiescence_ms`, `settled_slope` | observation poll / Theil–Sen | each cycle, n=12 | frozen control band | ≤5 s; not above band | blocker |
| `external_graph_delta` | canonical metadata comparator | once | Stage 04 | empty | blocker; dependency JSON |

Metrics label `measured`, `derived`, `estimated`, or `unknown`, preserve numerator/denominator and units, and never mix daemon/cgroup/runner scopes. High-frequency evidence streams to bounded artifacts rather than an in-process unbounded list.

### Performance arrival checkpoint

The tiny runner must write
`.benchmark-state/results/<run_id>/stage-05-perf-report.json` and
`stage-05-perf-report.md` according to
[benchmark_note.md](benchmark_note.md). The JSON schema version is
`phase1.stage05.perf-report.v1`; Markdown is generated from the same values.
Required groups are provenance and immutable run/raw links; raw native-copy/
legacy controls and candidate cold/warm samples; frozen baseline actual;
required pass target/cap; separately predeclared optimization target;
candidate actual; delta, ratio, and headroom; `R/E/K` and phase work;
memory/RSS; allocated carrier/staging/journal and full physical-space
categories; field-by-field mode/uid/gid/mtime/raw-xattr/hardlink/symlink/
sparse equality; every benchmark-note cancellation/crash/corruption/ENOSPC and
16-position verify/fsync/rename/catalog outcome; canonical external
package/version/source/checksum, feature, and direct-edge before/after arrays
with empty symmetric differences plus zero system/runtime/image-helper deltas;
integrity/recovery/cleanup; and a
`DIAGNOSTIC_PASS|FAIL|OPEN` verdict. The first Markdown table exposes those
comparison fields per stage-owned metric. Missing required evidence yields
`OPEN|FAIL`, never zero or pass.

Append Plan/Run to `e2e/test-report.md` before execution. After validation,
append Good/Defect there and append a new benchmark-note tracker row. Stage
exit resolves both report links and checks matching run ID, provenance, and
raw artifacts. Stage 05 reports are **DIAGNOSTIC**; Stage 11 alone can qualify
the normative Prep performance, scale, space, memory, and platform gates.

## 11. Stage exit verdict

Mandatory pass: two focused cases, tiny case, focused Rust/goldens, artifact/schema validation, exact graph equality, current-host no-helper proof, cleanup, and append-only report completion. Candidate tree/content/metadata must equal legacy; warm reads zero payload; every visibility/failure assertion must hold. Logical resources must return; physical memory and carrier peak must stay inside stage caps with no unexplained short-run trend.

The two versioned Stage 05 performance-arrival reports, their immutable
run/raw links, and matching append-only benchmark/E2E ledger rows are also
mandatory; without them the stage remains not reached.

Allowed warnings are attributed allocator/page-cache retention inside the frozen band and explicitly unavailable optional platform counters. Blockers include public candidate serving, wrong authority/root pair, fallback-like behavior, partial visibility, silent mismatch, corruption accepted, recovery ambiguity, operation ≥60 s, cap breach, suspected/confirmed leak, missing stage-gating evidence, new external/system/runtime dependency, target helper, or incomplete cleanup/artifacts.

Cleanup is run-ID/catalog-key scoped and restores generated configuration/gateway custody; it may not delete legacy state or shared candidate source objects. Rebuild after product changes; otherwise rerun only the failed focused node. Roll back to `shadow_write` on a blocker. Stage 06 still must prove strict activation/no fallback; Stages 07–10 own publication, GC, squash, and authority; Stage 11 owns normative performance, scale, memory, portability, regression, soak, and production qualification.
