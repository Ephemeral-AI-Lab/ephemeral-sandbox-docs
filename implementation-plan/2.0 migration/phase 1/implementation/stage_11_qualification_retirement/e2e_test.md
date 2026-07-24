# Stage 11 E2E — Cumulative qualification and retirement

**Final integration and qualification tier; not a POC.**
[Implementation overview](../index.md) · [Stage 11 specification](spec.md) · [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Product root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
Test root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`

## 1. Stage-local test objective

Implementation execution is blocked unless the product worktree is on the
exact fresh branch `upgrade-2.0-phase-1`, created from the newest approved
immutable product revision, with its base commit, upstream, clean scoped
worktrees, and responsible implementer recorded before any code edit. This
planning stage creates or switches no branch; any mismatch is a hard blocker.

Produce the sole cumulative go/no-go record for Phase 1. Correctness, recovery,
namespace isolation, OCC, lease safety, atomic visibility, dependency equality,
and portability run before any performance or space score. The qualified
candidate becomes the default only after those gates pass; legacy writers,
readers, and `/eos` artifacts are removed only after a default-mode soak,
rollback proof, complete migration inventory, and a restorable snapshot.

This stage must:

1. promote every focused case from Stages 00–10 and run the affected regression;
2. exercise candidate default, rollback, forward restore, mixed-root migration,
   and target-only restart;
3. execute the complete time, throughput, SeqCDC-selection, locality, memory,
   physical-space, pack, GC, squash, and cleanup matrices;
4. execute every required-release host row using the same sole pinned Ubuntu
   OCI index, verify it, and record the resolved platform manifest;
5. prove the exact external-dependency and runtime-helper delta is zero;
6. emit one immutable, schema-valid qualification bundle whose missing required
   values are failures, never inferred passes.

The tests use public command, file, PTY, stdin, workspace, publish, export,
squash, and structured-observability surfaces. Host-side `/eos` inspection is
an independent durability/space oracle; it does not replace public correctness.
No sandbox workload can observe `/eos`.

## 2. Existing assets to reuse

| Asset | Exact path | Reuse contract |
| --- | --- | --- |
| Typed declarations | `e2e/harness/catalog/declarations.py` | Stable IDs and exactly-once terminal validation checkpoints |
| Gateway/resource custody | `e2e/harness/runner/gateway.py`, `e2e/harness/runner/resources.py` | Track only run-owned gateways, sandboxes, sessions, and cleanup |
| Workspace publication | `e2e/runtime/workspace_session/test_publish_workspace_session.py` | Existing public publish/read behavior |
| Squash/remount | `e2e/runtime/workspace_session/test_squash_remount.py`, `e2e/manager/management/squash/` | Native remount and management behavior |
| Export | `e2e/manager/management/export/` | Existing export compatibility surface |
| Commands and lifecycle | `e2e/runtime/workspace_session/test_workspace_session.py`, `e2e/runtime/workspace_session/test_exec_finalize.py` | Command, cancellation, finalize, and teardown |
| Resource correctness | `e2e/observability/resource_isolation/`, `e2e/observability/resource_efficiency/` | Disk/memory ownership, diagnostics, reclaim, and soak patterns |
| Stress | `e2e/compound/stress/` | Long-lived and concurrency patterns |
| Catalog collection | `e2e/harness/catalog/collect.py` | Declaration/schema validation |
| Benchmark scheduler | `benchmark/backend/benchmark_lab/runner.py` | Sole sequential campaign scheduler |
| Resource sampling | `benchmark/backend/benchmark_lab/resource_sampling.py` | Allocated/logical disk, cgroup, Docker, filesystem, and product sources |
| Immutable artifacts | `benchmark/backend/benchmark_lab/artifacts.py` | Run manifest, observation, evidence, report, and export schemas |
| Existing presets | `benchmark/presets/publication.yml`, `benchmark/presets/squash-only.yml`, `benchmark/presets/squash-remount.yml`, `benchmark/presets/remount-width.yml`, `benchmark/presets/payload-scaling.yml`, `benchmark/presets/workspace-size-count.yml`, `benchmark/presets/concurrency-scaling.yml`, `benchmark/presets/release-comparison.yml` | Operation definitions and controls, not old thresholds |

Before every live E2E invocation, append the exact command, product/test commits,
intended cases, expected custody, and cleanup scope to `e2e/test-report.md`.
Afterward append Good/Defect/Fix, artifact IDs, and tracked cleanup evidence.
`E2E_REBUILD_BINARY=1` may reuse a responsive gateway, so the record states
whether the intended binary was actually built and loaded.

## 3. Resulting test tree

```text
ephemeral-sandbox-test/
├── e2e/runtime/layerstack_phase1/
│   ├── test_candidate_default.py                                  [add]
│   ├── test_mixed_root_migration.py                               [add]
│   ├── test_publication_recovery.py                               [add]
│   ├── test_materialization_recovery.py                           [add]
│   ├── test_retention_gc.py                                       [add]
│   ├── test_squash_identity.py                                    [add]
│   ├── test_target_only_restart.py                                [add]
│   ├── test_portability_matrix.py                                 [add]
│   └── SPEC.md                                                    [add]
├── e2e/runtime/workspace_session/
│   ├── test_publish_workspace_session.py                          [reuse]
│   ├── test_exec_finalize.py                                      [reuse]
│   └── test_squash_remount.py                                     [reuse]
├── e2e/fixtures/layerstack_phase1/
│   ├── corpora/
│   │   ├── tiny/                                                   [add]
│   │   ├── mixed/                                                  [add]
│   │   ├── large-source/                                           [add]
│   │   ├── no-dedup/                                               [add]
│   │   ├── many-small/                                             [add]
│   │   └── sparse/                                                 [add]
│   ├── roots/
│   │   ├── v1/                                                     [add]
│   │   ├── v2/                                                     [add]
│   │   └── mixed/                                                  [add]
│   ├── images/pinned-images.json                                  [add]
│   └── environment/required-release.json                          [add]
├── e2e/schemas/layerstack_phase1/
│   ├── evidence-v1.schema.json                                    [reuse]
│   └── qualification-v1.schema.json                               [add]
├── benchmark/presets/
│   ├── layerstack-phase1-tiny.yml                                 [add]
│   ├── layerstack-phase1-selection.yml                            [add]
│   ├── layerstack-phase1-rss.yml                                  [add]
│   ├── layerstack-phase1-space.yml                                [add]
│   └── layerstack-phase1-qualification.yml                        [add]
├── .e2e-state/                                                    [reuse] — run-owned evidence only
└── .benchmark-state/                                              [reuse] — run-owned evidence only
```

Boundary snapshots are taken before setup, immediately before and after every
durable visibility transition, immediately after each injected failure and
restart, after public success but before release, after explicit release, after
retirement, and after bounded quiescence. A snapshot is invalid if any path is
collapsed, inferred, or omitted.

### B0 — exact tree before each test

This is the pre-retirement Stage 10 authority state. Candidate v2 is public
authority, the legacy tree is a verified rollback shadow, and all transaction
directories shown without a child are empty.

```text
/eos/
├── layer-stack/
│   ├── .storage-writer.lock
│   ├── manifest.json
│   ├── workspace.json
│   ├── base/<legacy_base_id>/
│   ├── layers/<legacy_layer_id>/
│   ├── staging/
│   ├── .layer-metadata/
│   │   ├── <legacy_layer_id>.digest
│   │   └── <legacy_layer_id>.bytes
│   ├── format-v2.json
│   ├── roots/v2/<prefix>/<RootId>.root
│   ├── manifests/v2/<prefix>/<TreeManifestId>.manifest
│   ├── objects/v1/loose/<prefix>/<ObjectId>.obj
│   ├── packs/v1/
│   │   ├── open/
│   │   └── sealed/<PackId>.pack
│   ├── indexes/v1/
│   │   ├── pages/<page>.idx
│   │   └── index.catalog
│   ├── catalogs/v1/
│   │   ├── roots.catalog
│   │   ├── locators.catalog
│   │   ├── materializations.catalog
│   │   ├── leases.catalog
│   │   ├── retention.catalog
│   │   └── legacy-shadow.catalog
│   ├── journals/v1/
│   │   ├── publication/
│   │   ├── hydration/
│   │   ├── squash/
│   │   ├── compaction/
│   │   └── migration/
│   ├── staging/v2/
│   │   ├── publication/
│   │   ├── hydration/
│   │   ├── squash/
│   │   ├── compaction/
│   │   └── migration/
│   ├── leases/v1/
│   ├── retention/v1/
│   │   ├── epochs/<epoch>.epoch
│   │   └── pins.catalog
│   ├── maintenance/v1/
│   │   ├── gc.cursor
│   │   └── compaction.cursor
│   ├── materializations/docker-overlayfs/v1/<MaterializationId>/
│   │   └── carriers/<ordinal>/
│   ├── quarantine/v1/
│   └── trash/v1/
├── namespace_execution/<legacy_id>/transcript.log
├── storage/
│   ├── file_auditability/
│   └── workspace_recovery/
├── workspace/
│   ├── manager.json
│   └── .export/
└── runtime/daemon/
    ├── runtime.sock
    └── runtime.pid
```

### V — exact visibility-boundary additions

Each test copies B0, then introduces exactly one row from the failure roster
below. Before that row's visibility point, the authoritative catalog and public
route are byte-identical to B0; after it, they name the new generation. The
complete active-work tree is B0 plus these literal leaves, with `<family>` and
identifier substitutions fixed by the roster:

```text
/eos/
├── layer-stack/
│   ├── packs/v1/open/<PublicationId>.pack                         publication only
│   ├── journals/v1/<family>/<TxnId>.journal
│   ├── staging/v2/<family>/<TxnId>/
│   ├── leases/v1/<LeaseId>.lease
│   └── trash/v1/<RetentionEpoch>/<opaque_id>/                     trash/compaction only
├── workspace/
│   └── <workspace_session_id>/
│       ├── upper/
│       ├── work/
│       └── executions/<namespace_execution_id>/
│           └── transcript.log
└── runtime/daemon/
    ├── runtime.sock
    └── runtime.pid
```

Directories not selected by the roster remain the empty directories shown in
B0. `packs/v1/open/<PublicationId>.pack` exists only for a publication or pack
writer before sealing. `trash/v1/<RetentionEpoch>/<opaque_id>/` exists only
after the lease/root/generation checks and rename but before grace completion.
No reader may resolve a staging, open-pack, quarantine, or trash locator.

### S — exact success tree before explicit release

After a successful operation, the complete tree is B0 with the new immutable
root/manifest/object or materialization/pack leaves and committed catalog
generation, plus the following still-owned leaves:

```text
/eos/
├── layer-stack/
│   ├── roots/v2/<prefix>/<CommittedRootId>.root
│   ├── manifests/v2/<prefix>/<CommittedTreeManifestId>.manifest
│   ├── objects/v1/loose/<prefix>/<CommittedObjectId>.obj
│   ├── catalogs/v1/
│   │   ├── roots.catalog                                           committed generation visible
│   │   ├── locators.catalog                                        committed locator generation visible
│   │   ├── materializations.catalog                                committed materialization generation visible
│   │   └── leases.catalog                                          active owner still recorded
│   ├── journals/v1/<family>/<TxnId>.journal                        terminal committed state
│   ├── leases/v1/<LeaseId>.lease
│   └── materializations/docker-overlayfs/v1/<MaterializationId>/
│       └── carriers/<ordinal>/
├── workspace/
│   └── <workspace_session_id>/
│       ├── upper/
│       ├── work/
│       └── executions/<namespace_execution_id>/
│           └── transcript.log
└── runtime/daemon/
    ├── runtime.sock
    └── runtime.pid
```

All B0 leaves not replaced above remain present, including the legacy rollback
shadow. Public success is emitted only after the catalog generation and parent
directory are durable; the terminal journal, lease, session, and transcript
remain owned until the explicit-release checkpoint.

### F0/F1 — exact immediate failure trees and complete failpoint roster

Every injected crash is run both immediately before and immediately after each
named durable transition. The immediate post-restart snapshot is exactly one
of two schemas:

```text
F0 — failure before authoritative visibility
/eos/layer-stack/journals/v1/<family>/<TxnId>.journal               last fsynced pre-visibility state
/eos/layer-stack/staging/v2/<family>/<TxnId>/                       private, never reader-visible
/eos/layer-stack/leases/v1/<LeaseId>.lease                          live or fenced for recovery
/eos/layer-stack/packs/v1/open/<PublicationId>.pack                 publication/packing only
/eos/workspace/<workspace_session_id>/upper/                        only if workspace creation started
/eos/workspace/<workspace_session_id>/work/                         only if workspace creation started
/eos/workspace/<workspace_session_id>/executions/<namespace_execution_id>/transcript.log
                                                                     only if command admission started
```

F0 includes every B0 path unchanged and no new reader-visible catalog
generation. Recovery must abort or resume idempotently, fence the lease, and
remove every run-owned leaf above.

```text
F1 — failure after authoritative visibility
/eos/layer-stack/roots/v2/<prefix>/<CommittedRootId>.root           publication/migration when applicable
/eos/layer-stack/manifests/v2/<prefix>/<CommittedTreeManifestId>.manifest
                                                                     publication/migration when applicable
/eos/layer-stack/catalogs/v1/roots.catalog                           new generation when root authority changed
/eos/layer-stack/catalogs/v1/locators.catalog                        new generation when locator authority changed
/eos/layer-stack/catalogs/v1/materializations.catalog                new generation when carrier authority changed
/eos/layer-stack/journals/v1/<family>/<TxnId>.journal               committed or settling state
/eos/layer-stack/staging/v2/<family>/<TxnId>/                       recoverable residue only
/eos/layer-stack/leases/v1/<LeaseId>.lease                          live or fenced for recovery
/eos/layer-stack/trash/v1/<RetentionEpoch>/<opaque_id>/             deletion/evacuation only
```

F1 includes every B0 path not superseded above. Recovery must return the exact
committed receipt/generation, never roll the catalog back or duplicate the
commit, and then remove only run-owned residue after lease/root/generation
rechecks.

| Literal `<family>` | Inject before and after every transition into these states | F0 states | F1 states | Literal journal and staging identifiers |
| --- | --- | --- | --- | --- |
| `publication` | `Prepared`, `Capturing`, `ObjectsDurable`, `RootDurable`, `CommitIntent`, `Committed`, `Settling` | through `CommitIntent` | `Committed`, `Settling` | `<PublicationId>.journal`, `<PublicationId>/` |
| `hydration` | `Prepared`, `ObjectsVerified`, `CarrierFsynced`, `Visible`, `Cataloged` | through `Visible` | `Cataloged` | `<HydrationId>.journal`, `<HydrationId>/` |
| `squash` | `PLANNED`, `BUILDING`, `VERIFIED`, `COMMIT_INTENT`, `INSTALLED`, `REMOUNTING`, `EVACUATING`, `DONE` | through `COMMIT_INTENT` | `INSTALLED` through `DONE` | `<SquashId>.journal`, `<SquashId>/` |
| `compaction` | `Planned`, `Copying`, `TargetDurable`, `LocatorCommitIntent`, `LocatorsInstalled`, `SourceTrashed`, `GraceWaiting`, `Done` | through `LocatorCommitIntent` | `LocatorsInstalled` through `Done` | `<CompactionId>.journal`, `<CompactionId>/` |
| `migration` | `Inventoried`, `Capturing`, `Verified`, `CatalogCommitIntent`, `Mapped`, `Done` | through `CatalogCommitIntent` | `Mapped`, `Done` | `<MigrationId>.journal`, `<MigrationId>/` |
| `trash` | `Marked`, `RenameIntent`, `Renamed`, `DirectoryFsynced`, `GraceWaiting`, `Rechecked`, `Unlinked` | `Marked`, `RenameIntent` | `Renamed` through `Unlinked` | compaction/GC journal ID; `<RetentionEpoch>/<opaque_id>/` |

The failpoint driver names both sides explicitly
(`before_<state>`, `after_<state>`), emits one `eos-failure-<failpoint>.json`
snapshot for every row/state/side, and rejects an unlisted state. Mount, lease
acquire/renew/release/fence, file fsync, directory fsync, atomic rename,
catalog compare-and-swap, locator swap, and final unlink faults are injected
at their owning state as additional named failpoints and use the same F0/F1
classification. Thus every injected failure has one complete B0+F0 or B0+F1
path schema, not a prose-only expectation.

### R — exact post-retirement tree

Retirement is visible only after the migration inventory, soak, rollback,
snapshot restore, no-legacy-lease, and target-only restart gates pass. At this
checkpoint the legacy files and global namespace root are absent:

```text
/eos/
├── layer-stack/
│   ├── .storage-writer.lock
│   ├── format-v2.json
│   ├── roots/v2/<prefix>/<RootId>.root
│   ├── manifests/v2/<prefix>/<TreeManifestId>.manifest
│   ├── objects/v1/loose/<prefix>/<ObjectId>.obj
│   ├── packs/v1/
│   │   ├── open/
│   │   └── sealed/<PackId>.pack
│   ├── indexes/v1/
│   │   ├── pages/<page>.idx
│   │   └── index.catalog
│   ├── catalogs/v1/
│   │   ├── roots.catalog
│   │   ├── locators.catalog
│   │   ├── materializations.catalog
│   │   ├── leases.catalog
│   │   └── retention.catalog
│   ├── journals/v1/
│   │   ├── publication/
│   │   ├── hydration/
│   │   ├── squash/
│   │   ├── compaction/
│   │   └── migration/
│   ├── staging/v2/
│   │   ├── publication/
│   │   ├── hydration/
│   │   ├── squash/
│   │   ├── compaction/
│   │   └── migration/
│   ├── leases/v1/
│   ├── retention/v1/
│   │   ├── epochs/<epoch>.epoch
│   │   └── pins.catalog
│   ├── maintenance/v1/
│   │   ├── gc.cursor
│   │   └── compaction.cursor
│   ├── materializations/docker-overlayfs/v1/<MaterializationId>/
│   │   └── carriers/<ordinal>/
│   ├── quarantine/v1/
│   └── trash/v1/
├── storage/
│   ├── file_auditability/
│   └── workspace_recovery/
├── workspace/
│   ├── manager.json
│   └── .export/
└── runtime/daemon/
    ├── runtime.sock
    └── runtime.pid
```

Specifically absent at R are `manifest.json`, `workspace.json`, `base/`,
`layers/`, legacy `staging/`, `.layer-metadata/`,
`catalogs/v1/legacy-shadow.catalog`, and
`/eos/namespace_execution/`.

### Q — exact bounded-quiescence cleanup tree

Q has the same complete tree as R with retained immutable roots, manifests,
objects, sealed packs, indexes, catalogs, retention epochs/pins, maintenance
cursors, and ready materializations. The following existing directories are
exactly empty, and no other run-owned leaf exists:

```text
/eos/layer-stack/packs/v1/open/
/eos/layer-stack/journals/v1/publication/
/eos/layer-stack/journals/v1/hydration/
/eos/layer-stack/journals/v1/squash/
/eos/layer-stack/journals/v1/compaction/
/eos/layer-stack/journals/v1/migration/
/eos/layer-stack/staging/v2/publication/
/eos/layer-stack/staging/v2/hydration/
/eos/layer-stack/staging/v2/squash/
/eos/layer-stack/staging/v2/compaction/
/eos/layer-stack/staging/v2/migration/
/eos/layer-stack/leases/v1/
/eos/layer-stack/quarantine/v1/
/eos/layer-stack/trash/v1/
/eos/workspace/.export/
```

There is no `/eos/workspace/<workspace_session_id>/`, execution transcript,
live mount, file descriptor, mapping, worker, queue item, borrowed chunk,
permit, or expired catalog lease at Q. `/eos/attempts` is absent in B0, V, S,
every F0/F1 snapshot, R, and Q; its presence is always a hard failure.

## 4. Typed E2E case catalog

Every row below preserves the required host and release-runner coverage while
using only the `ubuntu:24.04` target image pinned to OCI index digest
`sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`.
Cross-image acceptance is deferred beyond Phase 1.

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `layerstack.phase1.qualification.correctness` | final integration; `run-now-focused` | candidate-default public correctness | frozen cumulative public corpus | command, file, PTY, stdin, workspace, publish, export, squash | exact bytes/metadata, native workspace, candidate authority, zero fallback/mismatch | per-operation raw durations | categorized peak/settled allocation | complete owner quiescence | frozen dependency and platform inventory | `60000` ms | validations, roots, route snapshots |
| `layerstack.phase1.qualification.recovery` | final integration; `run-now-focused` | exhaustive declared recovery boundaries | frozen failpoint ledger | inject, restart, retry through public surfaces | old-or-new complete visibility, idempotent recovery, bounded residue | per-fault recovery duration | staging/journal/trash residue | recovery owners return to idle | same pinned environment per pair | `60000` ms | failpoint ledger and inventories |
| `layerstack.phase1.qualification.concurrency` | final integration; `run-now-focused` | OCC, retry, cancellation | disjoint/conflicting/stale/duplicate histories | concurrent public publications and cancellation | linearizable OCC, idempotent retry, no lost update | per-history duration | transaction/staging allocation | permits/leases/workers release | provider-neutral history evidence | `60000` ms | operation histories and generations |
| `layerstack.phase1.qualification.migration-rollback` | final integration; `run-now-focused` | migration, default soak, rollback, restore | v1-only, v2-only, mixed selected roots | migrate, switch, soak, rollback reads, restore | complete mappings, all data readable, authority fencing exact | bounded action and soak series | coexistence/migration allocation | route/session/lease owners quiesce | release environment matrix | `300000` ms | catalog, soak, snapshot/restore records |
| `layerstack.phase1.qualification.target-only` | final integration; `run-now-focused` | retired-legacy target-only runtime | gated deletion slices and cold restart | public regression and recovery after each slice | only target writers/readers/tree remain and behavior is preserved | per-slice operation duration | target-only allocation | no retired owner or service remains | exact zero dependency/system delta | `60000` ms | target inventory and dependency snapshot |
| `layerstack.phase1.qualification.images` | release; `run-now-focused` | single pinned Ubuntu 24.04 target-image profile | same pinned target on each compatible required runner, including non-root/read-only variants | public capability profile | exact helper-independent behavior; cross-image acceptance remains deferred | per-runner case duration | target-image categorized allocation | owners quiesce on every required runner | pinned OCI index/platform digests and runner manifests | `60000` ms | target-image manifest and validations |
| `layerstack.phase1.qualification.hosts` | release; `run-now-focused` | required native host and release-runner triples | frozen macOS/Linux/Windows runners using the pinned Ubuntu 24.04 target where a container workload applies | public capability and identity corpus | identical canonical roots/public behavior and native carriers | per-host case duration | host-specific categorized allocation | owners quiesce on every host | machine/environment manifests plus the same pinned target digest | `60000` ms | host manifests and validations |
| `layerstack.phase1.qualification.selection` | final benchmark; `run-now-focused` | Raw/StreamCDC/SeqCDC selection | frozen matched campaign plans | benchmark scheduler runs matched workloads | statistical selection, distribution, locality gates | paired raw and bootstrap metrics | matched physical envelope | matched lifecycle and RSS evidence | same environment per comparison | `300000` ms | raw observations and paired bootstrap |
| `layerstack.phase1.qualification.time` | final benchmark; `run-now-focused` | warm/cold/command/PTY/publication/squash time | frozen factors and matched order | benchmark scheduler invokes public workloads | every latency and throughput gate | paired p50/p95/throughput | allocation context for samples | owner settle before every sample | pinned environment and dependency record | `60000` ms | raw control/candidate samples |
| `layerstack.phase1.qualification.rss` | final benchmark; `run-now-focused` | scale and history memory matrix | 64 MiB/256 MiB/1 GiB by histories 1/16/64 | cold public lifecycle campaign | logical release and raw physical bounds | bounded sampling duration | allocation context for memory rows | adjusted final/peak and RSS gates | source/scope/availability explicit | `300000` ms | bounded memory samples |
| `layerstack.phase1.qualification.space` | final benchmark; `run-now-focused` | physical space and amplification | required corpora, histories, faults, maintenance | public workload and bounded maintenance | complete accounting and amplification gates | operation durations as context | complete allocated tree categories | cleanup and settled-space lifecycle | filesystem allocation semantics recorded | `60000` ms | allocated tree inventories |
| `layerstack.phase1.qualification.all` | promoted final; `run-now-focused` | cumulative Phase 1 qualification | all frozen Stage 11 plans on required runners with the pinned Ubuntu 24.04 target | dispatch all eleven final drivers above | every normative gate and required row passes; cross-image acceptance is not claimed | complete normative time set | complete physical envelope | complete memory/lifecycle matrix | complete runner, pinned-target, and dependency matrix | `300000` ms | signed qualification bundle |
| `phase1.final.workspace-scratch.qualification` | promoted Stage 01 final; `run-now-focused` | workspace scratch release matrix | frozen command/PTY/restart corpus on required runners with the pinned Ubuntu 24.04 target | correctness, recovery, host, image, time, RSS, space drivers | containment, isolation, rollback, cleanup, portability | matched command/PTY metrics | workspace/global allocation | sustained scratch owner matrix | required-runner rows with one pinned target | `300000` ms | mapped Stage 11 bundle |
| `runtime.layerstack-phase1.portable-root.release-matrix` | promoted Stage 02 final; `run-now-focused` | portable-root release matrix | frozen golden corpus on required runners with the pinned Ubuntu 24.04 target | correctness, hosts, images drivers | identical canonical IDs and compatible behavior | per-row diagnostic duration | encoded and runtime allocation | repeated lifecycle matrix | every required-runner row with one pinned target | `300000` ms | mapped Stage 11 bundle |
| `runtime.layerstack-phase1.seqcdc.selection` | promoted Stage 03 final; `run-now-focused` | SeqCDC selection and portability | frozen matched algorithm corpus on required runners with the pinned Ubuntu 24.04 target | selection, time, RSS, space, host, image drivers | selection/distribution/locality/storage/portability gates | matched selection metrics | complete matched envelope | full scale/repeated lifecycle | frozen required-runner proof with one pinned target | `300000` ms | mapped Stage 11 bundle |
| `runtime.layerstack-phase1.shadow-ingest.qualification` | promoted Stage 04 final; `run-now-focused` | shadow-ingest qualification | frozen recovery/scale corpus on required runners with the pinned Ubuntu 24.04 target | correctness, recovery, selection, time, RSS, space, host, image drivers | v1 authority, exact shadow, zero duplicate payload, all final gates | matched ingest metrics | complete shadow envelope | scale/repeated lifecycle | required-runner rows with one pinned target | `300000` ms | mapped Stage 11 bundle |
| `phase1.final.materialization.qualification` | promoted Stage 05 final; `run-now-focused` | candidate materialization qualification | frozen correctness/fault/scale corpus on required runners with the pinned Ubuntu 24.04 target | correctness, recovery, time, RSS, space, host, image drivers | exact tree, atomic visibility, warm reuse, recovery, portability | matched materialization metrics | complete carrier envelope | scale/sustained lifecycle | required-runner rows with one pinned target | `300000` ms | mapped Stage 11 bundle |
| `phase1.final.strict.qualification` | promoted Stage 06 final; `run-now-focused` | strict activation qualification | frozen route/failure/rollback corpus on all release triples with the pinned Ubuntu 24.04 target | correctness, recovery, migration, time, RSS, hosts, images drivers | actual candidate source, zero fallback, exact rollback and cleanup | matched activation metrics | complete carrier/mount envelope | full history/owner matrix | all release triples with one pinned target | `300000` ms | mapped Stage 11 bundle |
| `phase1.final.publication.qualification` | promoted Stage 07 final; `run-now-focused` | durable publication qualification | frozen OCC/recovery/scale corpus on required runners with the pinned Ubuntu 24.04 target | correctness, recovery, concurrency, migration, time, RSS, space drivers | atomicity, OCC, retry, authority, resource gates | matched publication metrics | complete amplification envelope | full history/soak lifecycle | required-runner matrix with one pinned target | `300000` ms | mapped Stage 11 bundle |
| `layerstack.phase1.retention-gc.qualification` | promoted Stage 08 final; `run-now-focused` | retention, GC, pack qualification | frozen fault/history/scale corpus on required runners with the pinned Ubuntu 24.04 target | recovery, concurrency, time, RSS, space drivers | reachability, leases, pack caps, compaction, recovery gates | matched maintenance metrics | full live/staging/trash/slack envelope | full repeated-cycle owners/RSS | required-runner matrix with one pinned target | `300000` ms | mapped Stage 11 bundle |
| `layerstack.phase1.squash.qualification` | promoted Stage 09 final; `run-now-focused` | identity-preserving squash qualification | frozen identity/remount/depth corpus on required runners with the pinned Ubuntu 24.04 target | correctness, recovery, concurrency, time, RSS, space drivers | identity, lease continuity, recovery, depth, resource gates | matched squash metrics | source/target/settled envelope | scale/repeated remount lifecycle | required-runner matrix with one pinned target | `300000` ms | mapped Stage 11 bundle |
| `layerstack.phase1.authority.qualification` | promoted Stage 10 final; `run-now-focused` | candidate authority and retirement gate | frozen authority/shadow/rollback/retirement corpus on required runners with the pinned Ubuntu 24.04 target | correctness, recovery, concurrency, migration, target-only, hosts, images, time, RSS, space drivers | candidate authority, shadow parity, rollback fencing, retirement gates | matched authority metrics | authoritative peak/settled envelope | full soak and owner lifecycle | complete release-runner matrix with one pinned target | `300000` ms | mapped Stage 11 bundle |

In the mappings below, `hosts` retains every required host and release-runner
row, while `images` denotes the single pinned Ubuntu 24.04 target-image driver
on each compatible required runner. Cross-image coverage is deferred beyond
Phase 1.

The eleven promoted IDs map verbatim to Stage 11 drivers as follows:

- `layerstack.phase1.qualification.all` → all eleven base drivers.
- `phase1.final.workspace-scratch.qualification` → correctness, recovery, hosts, images, time, RSS, and space.
- `runtime.layerstack-phase1.portable-root.release-matrix` → correctness, hosts, and images.
- `runtime.layerstack-phase1.seqcdc.selection` → selection, time, RSS, space, hosts, and images.
- `runtime.layerstack-phase1.shadow-ingest.qualification` → correctness, recovery, selection, time, RSS, space, hosts, and images.
- `phase1.final.materialization.qualification` → correctness, recovery, time, RSS, space, hosts, and images.
- `phase1.final.strict.qualification` → correctness, recovery, migration-rollback, time, RSS, hosts, and images.
- `phase1.final.publication.qualification` → correctness, recovery, concurrency, migration-rollback, time, RSS, and space.
- `layerstack.phase1.retention-gc.qualification` → recovery, concurrency, time, RSS, and space.
- `layerstack.phase1.squash.qualification` → correctness, recovery, concurrency, time, RSS, and space.
- `layerstack.phase1.authority.qualification` → correctness, recovery, concurrency, migration-rollback, target-only, hosts, images, time, RSS, and space.

Complete literal declaration metadata for all 22 executable Stage 11 IDs:

| Stable ID | Title | Description | Features | Validations | Validation features | Execution surface | Owner ID | Timeout (ms) | Pytest markers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `layerstack.phase1.qualification.correctness` | `Phase 1 candidate preserves every public runtime contract` | `Runs cumulative native command, file, PTY, stdin, workspace, publication, export, squash, recovery, and isolation assertions in candidate-default mode.` | `("layerstack","workspace-session","command","file","observability","phase1")` | `{"content":"Bytes, canonical metadata, roots, export, and native workspace behavior match the versioned oracle.","authority":"Every write and read is candidate_v2 with no legacy fallback, mismatch, or unverified route.","lifecycle":"Transactions, workers, queues, permits, leases, mappings, file descriptors, staging, and run-owned resources reach bounded quiescence."}` | `{"content":("layerstack","workspace-session","file"),"authority":("layerstack","observability"),"lifecycle":("resource-efficiency",)}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","config")` |
| `layerstack.phase1.qualification.recovery` | `Phase 1 recovery boundaries are atomic and idempotent` | `Restarts and retries every declared write, fsync, rename, catalog, lease, mount, trash, and cursor boundary through public operations.` | `("layerstack","recovery","workspace-session","phase1")` | `{"terminal":"Each failpoint exposes either the old complete state or the exact committed new state; retry is idempotent; all selected roots reconstruct; residue and recovery owners satisfy their bounds."}` | `{"terminal":("layerstack","recovery","workspace-session","resource-efficiency")}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","hard","config")` |
| `layerstack.phase1.qualification.concurrency` | `Phase 1 publication and maintenance histories are linearizable` | `Executes disjoint, conflicting, stale, duplicate-request, cancellation, lease, publication, GC, and squash histories against one candidate-default daemon.` | `("layerstack","concurrency","publication","maintenance","phase1")` | `{"terminal":"OCC generations are linearizable; retries are identical; no update, root, or last locator is lost; cancellation releases every transaction, permit, worker, and lease."}` | `{"terminal":("layerstack","concurrency","publication","maintenance","resource-efficiency")}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","hard","config")` |
| `layerstack.phase1.qualification.migration-rollback` | `Migration rollback and forward restore preserve every selected root` | `Migrates v1-only and mixed roots, runs the approved candidate-default soak, performs verified legacy-read rollback, and restores candidate reads.` | `("layerstack","migration","candidate-authority","read-rollback","phase1")` | `{"terminal":"Every selected root has a complete v2 mapping; candidate remains sole write authority; rollback fails closed without verified parity and reads every root with verified parity; forward restore is generation-fenced and exact."}` | `{"terminal":("layerstack","migration","candidate-authority","read-rollback","recovery")}` | `"cli"` | `"layerstack-phase1"` | `300000` | `("runtime","layerstack","serial","release","config")` |
| `layerstack.phase1.qualification.target-only` | `Target-only runtime survives cold restart after legacy retirement` | `Applies the approved gated retirement slices, cold-restarts after each slice, and runs affected public behavior and recovery with only the target tree and owners.` | `("layerstack","legacy-retirement","recovery","phase1")` | `{"terminal":"No legacy writer, reader, helper, service, direct dependency edge, or mutable authority remains; every public contract and selected root survives cold restart with complete target-only evidence."}` | `{"terminal":("layerstack","legacy-retirement","recovery","resource-efficiency")}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","release","config")` |
| `layerstack.phase1.qualification.images` | `Pinned Ubuntu 24.04 target-image capability profile is helper-independent` | `Runs the frozen public capability corpus against the same pinned Ubuntu 24.04 target on every compatible required runner, including non-root and read-only variants where prescribed; cross-image acceptance is deferred beyond Phase 1.` | `("layerstack","portability","ubuntu-24.04","phase1")` | `{"terminal":"Every required-runner row passes exact behavior against the same pinned target without invoking a target shell, libc utility, package manager, network fetch, or undeclared helper; OCI index and platform digests are recorded and no cross-image claim is made."}` | `{"terminal":("layerstack","portability","ubuntu-24.04","workspace-session")}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","release","config")` |
| `layerstack.phase1.qualification.hosts` | `Required native host triples preserve portable identity and behavior` | `Runs the frozen identity and public capability corpus on every required macOS, Linux, and Windows release triple with its native provider carrier and the pinned Ubuntu 24.04 target where a container workload applies.` | `("layerstack","portability","host-matrix","ubuntu-24.04","phase1")` | `{"terminal":"Canonical roots and public results are identical across required hosts; each provider uses its declared native carrier; every applicable workload uses the same pinned target; machine, toolchain, filesystem, dependency, and target-digest evidence is complete."}` | `{"terminal":("layerstack","portability","host-matrix","ubuntu-24.04","workspace-session")}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","release","config")` |
| `layerstack.phase1.qualification.selection` | `Matched campaigns select the Phase 1 chunking algorithm` | `Runs frozen Raw versus StreamCDC and Raw versus SeqCDC plans with identical corpus, order, cache state, environment, collectors, and correctness oracle.` | `("layerstack","benchmark","chunking-selection","phase1")` | `{"terminal":"All raw pairs validate; bootstrap and distribution gates are computed from matched samples; locality and physical-space gates pass; the selected algorithm and rejection rationale are persisted."}` | `{"terminal":("layerstack","benchmark","chunking-selection","resource-efficiency")}` | `"cli"` | `"layerstack-phase1"` | `300000` | `("runtime","layerstack","serial","release","benchmark","config")` |
| `layerstack.phase1.qualification.time` | `Candidate time and throughput gates pass on matched workloads` | `Runs frozen warm, cold, command, PTY, publication, hydration, maintenance, and squash workloads through the benchmark scheduler.` | `("layerstack","benchmark","performance","phase1")` | `{"terminal":"Every workload has schema-valid matched raw samples, exact correctness, approved p50 and p95 or throughput gates, bounded per-operation duration, and no competing campaign."}` | `{"terminal":("layerstack","benchmark","performance","workspace-session")}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","release","benchmark","config")` |
| `layerstack.phase1.qualification.rss` | `Candidate logical and physical memory gates pass at scale` | `Runs the cold 64 MiB, 256 MiB, and 1 GiB by history-depth 1, 16, and 64 matrix with repeated lifecycle and explicit sampler provenance.` | `("layerstack","benchmark","memory","resource-efficiency","phase1")` | `{"terminal":"All logical owners return to settled bounds; adjusted final and peak process or cgroup memory passes the frozen gates; unavailable sources are explicit and no required row is unverified."}` | `{"terminal":("layerstack","benchmark","memory","resource-efficiency")}` | `"cli"` | `"layerstack-phase1"` | `300000` | `("runtime","layerstack","serial","release","benchmark","config")` |
| `layerstack.phase1.qualification.space` | `Candidate physical space and amplification gates pass` | `Measures allocated bytes for every required corpus, history, fault residue, carrier, index, journal, pack, trash, quarantine, and maintenance state.` | `("layerstack","benchmark","storage-efficiency","phase1")` | `{"terminal":"Peak and settled categorized allocated bytes reconcile with zero unexplained required residue and satisfy all frozen amplification, slack, staging, and reclamation gates."}` | `{"terminal":("layerstack","benchmark","storage-efficiency","resource-efficiency")}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("runtime","layerstack","serial","release","benchmark","config")` |
| `layerstack.phase1.qualification.all` | `Phase 1 cumulative release qualification` | `Promotes the Stage 00 planned-final ID and dispatches every Stage 11 correctness, recovery, concurrency, migration, target-only, image, host, selection, time, RSS, and space driver across the required runners with only the pinned Ubuntu 24.04 target.` | `("layerstack","phase1-qualification","portability","ubuntu-24.04","resource-efficiency")` | `{"terminal":"All eleven Stage 11 drivers and every required release-runner row execute successfully against the pinned target; the aggregate bundle is schema-valid, internally linked, contains no inferred or missing required observation, and makes no cross-image acceptance claim."}` | `{"terminal":("layerstack","phase1-qualification","portability","ubuntu-24.04","resource-efficiency")}` | `"cli"` | `"layerstack-phase1"` | `300000` | `("runtime","layerstack","serial","release","config")` |
| `phase1.final.workspace-scratch.qualification` | `Final workspace scratch qualification` | `Promotes the Stage 01 planned-final ID into the mapped Stage 11 correctness, recovery, host, image, time, RSS, and space drivers across required runners with only the pinned Ubuntu 24.04 target.` | `("phase1.qualification","runtime.workspace_session","runtime.pty","ubuntu-24.04")` | `{"terminal":"All workspace scratch command, PTY, cancellation, restart, rollback, memory, and required-runner rows execute successfully against the pinned target with complete evidence and no global scratch writes; cross-image acceptance remains deferred."}` | `{"terminal":("phase1.qualification","runtime.workspace_session","runtime.pty","ubuntu-24.04","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `300000` | `("runtime","layerstack","serial","release","config")` |
| `runtime.layerstack-phase1.portable-root.release-matrix` | `Portable root release matrix` | `Promotes the Stage 02 planned-final ID into the mapped Stage 11 correctness, host, and image drivers for canonical portable identities across required runners with only the pinned Ubuntu 24.04 target.` | `("runtime.layerstack-phase1.portable-root","phase1.qualification","portability","ubuntu-24.04")` | `{"terminal":"Every required-runner row against the pinned target produces identical canonical root identifiers and compatible public behavior with complete environment and lifecycle evidence; cross-image acceptance remains deferred."}` | `{"terminal":("runtime.layerstack-phase1.portable-root","phase1.qualification","portability","ubuntu-24.04")}` | `"cli"` | `"e2e-core"` | `300000` | `("runtime","layerstack","serial","release","config")` |
| `runtime.layerstack-phase1.seqcdc.selection` | `SeqCDC final selection and portability qualification` | `Promotes the Stage 03 planned-final ID into the mapped Stage 11 selection, time, RSS, space, host, and image drivers across required runners with only the pinned Ubuntu 24.04 target.` | `("runtime.layerstack-phase1.seqcdc","phase1.qualification","benchmark","portability","ubuntu-24.04")` | `{"terminal":"All final selection, distribution, locality, physical-space, lifecycle-memory, and required-runner gates execute against the pinned target from matched raw evidence; the selected algorithm is recorded without an unverified required row or a cross-image acceptance claim."}` | `{"terminal":("runtime.layerstack-phase1.seqcdc","phase1.qualification","benchmark","portability","ubuntu-24.04")}` | `"cli"` | `"e2e-core"` | `300000` | `("runtime","layerstack","serial","release","benchmark","config")` |
| `runtime.layerstack-phase1.shadow-ingest.qualification` | `Shadow ingest final qualification` | `Promotes the Stage 04 planned-final ID into the mapped Stage 11 correctness, recovery, selection, time, RSS, space, host, and image drivers across required runners with only the pinned Ubuntu 24.04 target.` | `("runtime.layerstack-phase1.shadow-ingest","phase1.qualification","benchmark","portability","ubuntu-24.04")` | `{"terminal":"All final shadow-ingest correctness, zero-duplicate-payload, recovery, time, storage, memory, and required-runner gates execute successfully against the pinned target with complete matched evidence; cross-image acceptance remains deferred."}` | `{"terminal":("runtime.layerstack-phase1.shadow-ingest","phase1.qualification","benchmark","portability","ubuntu-24.04")}` | `"cli"` | `"e2e-core"` | `300000` | `("runtime","layerstack","serial","release","benchmark","config")` |
| `phase1.final.materialization.qualification` | `Final materialization qualification` | `Promotes the Stage 05 planned-final ID into the mapped Stage 11 correctness, recovery, time, RSS, space, host, and image drivers across required runners with only the pinned Ubuntu 24.04 target.` | `("phase1.qualification","storage.materialization","portability","ubuntu-24.04")` | `{"terminal":"All final materialization exactness, atomicity, warm-reuse, corruption, recovery, time, physical-space, memory, and required-runner gates execute successfully against the pinned target with complete evidence; cross-image acceptance remains deferred."}` | `{"terminal":("phase1.qualification","storage.materialization","observability.resource_efficiency","portability","ubuntu-24.04")}` | `"cli"` | `"phase1-storage"` | `300000` | `("runtime","layerstack","serial","release","config")` |
| `phase1.final.strict.qualification` | `Final strict activation qualification` | `Promotes the Stage 06 planned-final ID into the mapped Stage 11 correctness, recovery, migration-rollback, time, RSS, host, and image drivers across every required release triple with only the pinned Ubuntu 24.04 target.` | `("phase1.qualification","storage.candidate_activation","portability","ubuntu-24.04")` | `{"terminal":"All strict activation route, no-fallback, corruption, mount, rollback, correctness, time, space, memory, soak, and required-release-runner gates execute successfully against the pinned target with complete evidence; cross-image acceptance remains deferred."}` | `{"terminal":("phase1.qualification","storage.candidate_activation","observability.resource_efficiency","portability","ubuntu-24.04")}` | `"cli"` | `"phase1-storage"` | `300000` | `("runtime","layerstack","serial","release","config")` |
| `phase1.final.publication.qualification` | `Final durable publication qualification` | `Promotes the Stage 07 planned-final ID into the mapped Stage 11 correctness, recovery, concurrency, migration-rollback, time, RSS, and space drivers across required runners with only the pinned Ubuntu 24.04 target.` | `("phase1.qualification","storage.publication_v2","storage.occ","storage.recovery","portability","ubuntu-24.04")` | `{"terminal":"All final publication atomicity, OCC, retry, recovery, authority, time, amplification, memory, history, soak, and required-runner gates execute successfully against the pinned target with complete evidence; cross-image acceptance remains deferred."}` | `{"terminal":("phase1.qualification","storage.publication_v2","storage.occ","storage.recovery","observability.resource_efficiency","portability","ubuntu-24.04")}` | `"cli"` | `"phase1-storage"` | `300000` | `("runtime","layerstack","serial","release","config")` |
| `layerstack.phase1.retention-gc.qualification` | `Retention GC and pack qualification matrix` | `Promotes the Stage 08 planned-final ID into the mapped Stage 11 recovery, concurrency, time, RSS, and space drivers across required runners with only the pinned Ubuntu 24.04 target.` | `("layerstack","phase1-qualification","retention","garbage-collection","pack","portability","ubuntu-24.04")` | `{"terminal":"All Stage 11 retention, reachability, lease, pack-cap, compaction, recovery, time, space, memory, soak, portability, required-runner, and affected-regression gates execute against the pinned target with no unverified required row; cross-image acceptance remains deferred."}` | `{"terminal":("layerstack","phase1-qualification","retention","resource-efficiency","portability","ubuntu-24.04")}` | `"cli"` | `"layerstack-phase1"` | `300000` | `("runtime","layerstack","serial","release","config")` |
| `layerstack.phase1.squash.qualification` | `Identity-preserving squash release qualification` | `Promotes the Stage 09 planned-final ID into the mapped Stage 11 correctness, recovery, concurrency, time, RSS, and space drivers across required runners with only the pinned Ubuntu 24.04 target.` | `("layerstack","phase1-qualification","squash","materialization","portability","ubuntu-24.04")` | `{"terminal":"Every Stage 11 squash identity, lease-continuity, remount, recovery, depth, latency, space, memory, soak, and required-release-runner gate executes successfully against the pinned target; cross-image acceptance remains deferred."}` | `{"terminal":("layerstack","phase1-qualification","squash","resource-efficiency","portability","ubuntu-24.04")}` | `"cli"` | `"layerstack-phase1"` | `300000` | `("runtime","layerstack","serial","release","config")` |
| `layerstack.phase1.authority.qualification` | `Candidate authority release qualification and legacy retirement gate` | `Promotes the Stage 10 planned-final ID into the mapped Stage 11 correctness, recovery, concurrency, migration-rollback, target-only, host, image, time, RSS, and space drivers across required runners with only the pinned Ubuntu 24.04 target.` | `("layerstack","phase1-qualification","candidate-authority","legacy-shadow","portability","ubuntu-24.04")` | `{"terminal":"All authority, shadow parity, rollback fencing, soak, performance, space, memory, required-runner, affected-regression, default-enable, and legacy-retirement gates execute successfully against the pinned target; cross-image acceptance remains deferred."}` | `{"terminal":("layerstack","phase1-qualification","candidate-authority","resource-efficiency","portability","ubuntu-24.04")}` | `"cli"` | `"layerstack-phase1"` | `300000` | `("runtime","layerstack","serial","release","config")` |

Every declaration has exactly the terminal checkpoints named in `validations`,
and each checkpoint is emitted once. The benchmark scheduler owns all campaign
ordering; pytest never starts a competing benchmark campaign.

## 5. Correctness and failure matrix

| Dimension | Required cases | Pass contract |
| --- | --- | --- |
| Content sizes | empty/no-op; 1 B; 8,191/8,192/8,193 B; 16 KiB; 32,767/32,768/32,769 B; ≥256 MiB | Exact bytes; nonempty `ceil(U/32KiB)≤K≤ceil(U/8KiB)`; sub-min one actual-length chunk |
| Tree metadata | modes; uid/gid mapping; symlink; supported hardlink groups; whiteout; opaque dir; required timestamps/xattrs | Canonical round trip and native materialization without target helpers |
| Path domain | non-UTF-8 Linux byte path, deep tree, long component, normalized separator rejection | Byte identity preserved; invalid/escaping input fails closed |
| Sparse/incompressible | ≥8 GiB logical sparse; ≥512 MiB no-dedup | Extents/bytes exact; bounded memory/disk; no dense accidental copy |
| Publication | no-op, localized edit, many-small, deletes/renames, retry | Immutable objects; one atomic root generation; idempotent `PublicationId` |
| OCC | disjoint, overlapping, stale base, duplicate request | Disjoint merge semantics preserved; conflict is explicit; no lost update |
| Warm activation | depths 1, 16, 48, 64 | `O(D)`, zero CAS payload bytes, native mount |
| Cold activation | complete/partial cache, object miss, corrupt object, disk full | Private verify/fsync/swap; no partial visibility or fallback |
| Commands | success, nonzero exit, no-op, cancel, timeout | Native files; exit behavior and cleanup unchanged |
| PTY/stdin | create, drain, supported stdin, control-C, control-D | Compatible timings/bytes; resize, arbitrary signal, literal EOF remain deterministically unsupported |
| Squash | manual/routine/threshold; concurrent reader/writer; restart in every state | `RootId` and publication generation unchanged; materialization generation advances; leases overlap |
| GC/pack | live/dead/weak ancestry/pin/lease; compaction interruption | Strong data retained; weak unpinned provenance collectible; grace and final recheck |
| Migration | v1-only, v2-only, mixed, interrupted, retry, stale mapping | Complete verified mapping; one authority; idempotent restart |
| Retirement | writer removal, reader removal, artifact deletion as separate checkpoints | Each deletion gate passes and target-only restart succeeds |
| Namespace | two sandboxes and two sessions with same logical paths | No cross-namespace read, locator, lease, transcript, or observation leakage |
| Export | active/historical root and mixed metadata | Existing public export behavior preserved from v2 truth |

For publication, hydration, squash, compaction, migration, and trash, inject a
crash before and after each durable phase boundary. Expected recovery is
enumerated by state, including the squash chain
`PLANNED→BUILDING→VERIFIED→COMMIT_INTENT→INSTALLED→REMOUNTING→EVACUATING→DONE`.
`ABORTED` or `CONFLICT` is legal only before `INSTALLED`. Missing, truncated,
length-mismatched, hash-mismatched, wrong-domain, and stale-generation data
fail closed and enter bounded quarantine where specified.

All correctness/recovery rows must pass before benchmark scoring. A crash,
corruption, partial visibility, silent fallback, lost update, leaked namespace,
or unowned cleanup is a hard failure regardless of timing.

## 6. Tiny correctness and benchmark loop

The developer loop uses `layerstack-phase1-tiny`: empty/no-op, a localized
1 KiB edit in a deterministic 1 MiB file, one 1 MiB incompressible file, 256
small files, history depths 1/8/32, one warmup and at least five alternating
raw/candidate samples. It targets 30–60 seconds and gives diagnostic medians
only; it cannot pass the final p95, selection, RSS, or physical-space gates.

The final scheduler executes these frozen campaigns:

| Campaign | Corpus / ordering | Samples | Gate |
| --- | --- | --- | --- |
| Time | no-op exec, command throughput, PTY/stdin, warm prepare/mount, remount, squash, publish, cold hydrate/activate | ≥3 warmups then enough counterbalanced pairs for stable p50/p95; raw stored | Stage 11 numeric time/throughput contract |
| Selection | localized large source and mixed tree; separate no-dedup/many-small guardrails | 3 fresh matched corpus sets; ≥5 interleaved samples/workload/invocation; counterbalanced | paired-bootstrap 95% lower bound≥0.10 where required |
| Distribution | SeqCDC and StreamCDC with identical min/max and corpus | same matched records | means within 5%; p10/p50/p90 within 10% |
| Locality | source `F≥16MiB`, edit≤64KiB | all raw samples retained | target changed+2×32KiB+segment overhead; hard median>4×target or any≥25%F |
| RSS | inputs 64 MiB/256 MiB/1 GiB × histories 1/16/64, cold | 3 independent repetitions/point, one raw and one candidate invocation each | absolute, idle-adjusted, scale, release, and slope gates |
| Space | mixed≥512 MiB/20k files; no-dedup≥512 MiB; many-small≥100k; sparse≥8 GiB logical; repeated small/large histories | 3 settled repetitions/cell | amplification, duplication, slack, residue, metadata |
| Maintenance | pack, GC, compaction, autosquash at controlled live/dead/depth values | exact threshold boundaries + restart variants | capacity/threshold/grace/slice gates |

Inputs are pre-generated outside timed intervals. A matched cell fixes host,
image, daemon binary, filesystem, CPU/memory allocation, cache class, corpus
digest, seed, operation order, and background load. Raw control and candidate
alternate; no campaign overlaps another. No operation exceeds 60 seconds.
Each matched pair/invocation is at most five minutes. Each RSS point receives
its own five-minute raw invocation and candidate invocation, repeated three
times. Selection uses separate raw/Stream and raw/Seq invocations; the
two-invocation set is repeated three times.

Every sample records absolute values, ratio/difference, warmup status, order,
and rejection reason. No sample is silently dropped. Bootstrap method, seed,
resamples, pairing key, confidence interval, and predeclared exclusion policy
are artifact fields.

## 7. Memory-stability and reclamation test

The test observes one daemon without restart, purge, `malloc_trim`, cache drop,
or allocator swap. For every operation:

```text
idle -> admission -> active/high-water -> success|failure|cancel
     -> explicit handle release -> 100 ms quiescence polling for ≤5 s
     -> settled observation
```

Logical quiescence requires: operation handle complete; transaction-owned bytes
and permits zero; payload queue exactly zero; metadata queue empty; borrowed
chunks zero; temporary leases/mappings/FDs closed; staging/journal terminal;
workers at configured idle count; bounded registries within capacity; no
session/execution/run-owned artifact remains.

| Resource | Required hard bound |
| --- | --- |
| SeqCDC window and publication ring | 32 KiB each |
| Borrowed chunk slices | at most 2 per chunk; ≤4 chunks globally |
| Payload queue | exactly 0 bytes |
| Metadata queue | 16 descriptors and ≤64 KiB |
| Hydration/pack buffer | 256 KiB each per worker |
| Workers | 4 global |
| Merge readers | fan-in 8 ×64 KiB |
| Manifest/journal encoder | ≤256 KiB/operation |
| Index cache | 4096×4 KiB =16 MiB |
| Managed publication memory | ≤4 MiB excluding index cache |
| Storage byte semaphore | 64 MiB |
| Native carrier depth | ≤64 |

Physical RSS passes only when every cold matrix point is ≤384 MiB absolute and
≤128 MiB above its raw idle; adjusted median final and peak values vary by
≤16 MiB across the series, and no 4× input/history increase adds >8 MiB.
The first and last settled-window medians and robust slope must remain within
the frozen raw-control noise band and 16 MiB tolerance. Logical release is an
independent gate. If daemon RSS scope cannot be proven, record it as
`unavailable` and use the predeclared public cgroup/Docker source; never
zero-fill or estimate a gating value.

Every physical checkpoint accounts:

```text
T(t) = L_hot + H_cold + ΣU_active + P_staging + M
D_ideal = C_current + H_unique
```

Mixed/no-dedup settled amplification targets ≤1.08 and fails >1.15;
many-small targets ≤1.15 and fails >1.25; avoidable duplicate bytes target
≤1% and fail >3%; pack dead/slack targets ≤2% and fail >5%; persistent
unexplained unreachable bytes must be zero. Metadata is ≤96 B/chunk,
≤64 B/segment reference, and ≤256 B plus path bytes/changed path. Recovery
residue is ≤1 MiB + min(1% retained payload, 64 MiB) with no pending
transaction.

Publication staging is `C_capture+≤5%`; hydration is `C_target+≤5%`; squash
has one replacement plus leased old carriers; compaction has a bounded source
and target. SeqCDC unique retained bytes are ≤1.14× StreamCDC.

## 8. Dependency and portability proof

For every target/feature invocation, compare before/after canonical inventories:

- exact external `(source,name,version,checksum)` set;
- exact enabled external `(package,feature)` set;
- product-wide direct external manifest-edge multiset;
- workspace manifest and `Cargo.lock` bytes;
- Python/npm manifests and locks;
- image package/helper inventory;
- runtime processes, sockets, services, executed helpers, and downloads;
- license/notice inventory.

Pass requires exact equality: zero new external packages, features, direct
edges, services, sidecars, helpers, target-image prerequisites, or runtime
downloads. The new portable core may use `std` and internal workspace crates;
the adapter reuses existing `sha2` and other already-enabled dependencies.
No database, daemon, FUSE helper, target-image shell, libc, package manager, or
network fetch is permitted. Apache-2.0 SeqCDC provenance and legal approval are
mandatory evidence.

Sole pinned Phase 1 target image:

| Image | OCI index | linux/amd64 manifest | linux/arm64 manifest | Capability case |
| --- | --- | --- | --- | --- |
| `ubuntu:24.04` | `sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` | `sha256:52df9b1ee71626e0088f7d400d5c6b5f7bb916f8f0c82b474289a4ece6cf3faf` | `sha256:7f622ca8766bccb22f04242ecb6f19f770b2f08827d7c5425fb57681140e6efb` | public capability profile plus read-only and non-root runtime variants |

The same OCI index identity is used on every applicable required host. The
index is verified and its host-appropriate resolved platform manifest is
recorded for every run. Required target capability profile
`linux-image-capability-v1` contains a Linux OCI rootfs/config, supported native
architecture, provider-side OverlayFS/mount/xattr capabilities, and writable
provider storage even when the image root is read-only. It contains no
userland requirement. A requested command may fail because its executable is
absent; storage, workspace, file, publication, and recovery must still work.
No second target image supplies Phase 1 evidence. Cross-image portability is
deferred beyond Phase 1 and is neither an acceptance nor a retirement gate.

Required-release matrix:

| Host triple | Frozen runtime | Image/platform | Disposition before execution | Required result |
| --- | --- | --- | --- | --- |
| macOS 26.4 / Darwin 25.4.0 / arm64 | Docker Desktop 4.76.0, Engine 29.5.2, LinuxKit 6.12.76, 4 CPU, ~4.1 GiB | same pinned Ubuntu OCI index; verify and record arm64 manifest | `unverified`; planning host provenance only | required-release; normative performance row |
| Ubuntu 24.04 LTS / amd64 | Docker Engine 29.5.2 | same pinned Ubuntu OCI index; verify and record amd64 manifest | `unverified` | required-release contract row |
| Windows 11 24H2 / amd64, Linux containers | Docker Desktop 4.76.0, Engine 29.5.2 | same pinned Ubuntu OCI index; verify and record amd64 manifest | `unverified` | required-release contract row |

Unavailable or unexecuted required-release rows are no-go. Other Linux
kernel/filesystem/Docker combinations may be `contract-tested` or
`unverified`; they cannot substitute for a required row.

## 9. Focused and final-stage commands

### Product formatting, lint, and focused unit/integration

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked --workspace --all-targets --all-features -- -D warnings
cargo test -p sandbox-runtime-layerstack-core
cargo test -p sandbox-runtime-layerstack
cargo test -p sandbox-runtime-workspace
cargo test -p sandbox-runtime
cargo test -p sandbox-runtime-overlay
cargo test -p sandbox-runtime-namespace-execution
cargo test -p sandbox-runtime-namespace-process
cargo test -p sandbox-cli
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

### Artifact compatibility validation

Catalog validation:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
PYTHONPATH=e2e .venv/bin/python -m harness.catalog.collect \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
.benchmark-state/test-venv/bin/python -m pytest \
  benchmark/backend/tests/compatibility/test_artifacts.py
```

### Focused E2E

After the required `test-report.md` intent entry:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_candidate_default.py \
  e2e/runtime/layerstack_phase1/test_mixed_root_migration.py \
  e2e/runtime/layerstack_phase1/test_publication_recovery.py \
  e2e/runtime/layerstack_phase1/test_materialization_recovery.py \
  e2e/runtime/layerstack_phase1/test_retention_gc.py \
  e2e/runtime/layerstack_phase1/test_squash_identity.py \
  e2e/runtime/layerstack_phase1/test_target_only_restart.py \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

Use `E2E_REBUILD_BINARY=0` only for a recorded, identity-matched focused rerun.

### Stage 11 affected regression

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

### Stage 11 native-host/pinned-Ubuntu-24 matrix

Run this single-image matrix once per applicable required host and record the
actual host row. Pinned Ubuntu 24.04 is the only Phase 1 target image;
cross-image portability is deferred beyond Phase 1 and is not an acceptance
gate. No tag-only result counts.

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

### Tiny benchmark validate/run

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
  --plan layerstack-phase1-tiny \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --plan layerstack-phase1-tiny \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

### Full Phase 1 qualification

The final qualification uses only pinned Ubuntu 24.04:

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

The benchmark consumes prebuilt binaries and never rebuilds them.

After interruption:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark recover \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

Run-owned cleanup:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark cleanup \
  --run-id RUN_ID \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

The runner is sequential. Destructive global Docker cleanup, untracked
sandbox deletion, and concurrent campaign execution are prohibited.

## 10. Metrics and evidence contract

| Metric family | Definition / source | Aggregation | Gate / missing-data rule |
| --- | --- | --- | --- |
| Correctness | versioned byte/metadata/tree/root oracle | exact per checkpoint | exact; missing fails |
| Route | closed enum authority/read/fallback/mismatch counters | start/end deltas per operation | candidate only; all fallback/mismatch zero |
| Warm time | resolve, prepare, mount, frozen remount | paired p50/p95 | ≤raw +5%+2 ms |
| Squash | full build/install/remount | paired p50/p95 | ≤raw +10%+5 ms |
| Command | no-op, native throughput | paired p50/p95 / bytes/s | no-op≤+3%+0.5 ms; throughput≥97% |
| PTY/stdin | create, drain, supported control | paired p50/p95 | create≤+3%+1 ms; rest≤+3%+0.5 ms |
| Native file | sequential read/write | paired throughput | ≥97% |
| Publication | disjoint and localized small edit | throughput / p95 | disjoint≥90%; edit≤+15%+5 ms |
| Cold | hydrate bytes/s and activation p95 | matched native-copy control | hydrate≥70%; activation≤1.5×copy+warm |
| Selection | saved unique bytes ratio | paired bootstrap | required lower CI≥0.10; guardrail regressions≤3% |
| Chunking | count, mean, p10/p50/p90, retained/locality bytes | per corpus and matched algorithm | all fixed gates; missing fails |
| Memory | owned bytes/counts, RSS/cgroup/Docker and scope | 100 ms bounded stream, medians/peaks/slope | all lifecycle/absolute/scale gates |
| Space | allocated bytes in `L_hot,H_cold,ΣU_active,P_staging,M` | pre/visible/settled/restart | all amplification/residue/metadata gates |
| Maintenance | depth, carriers, pack bytes/records/allocation, dead/slack, slice | exact threshold boundary | all squash/pack/GC thresholds |
| Dependencies | canonical exact sets and edge multiset | byte-for-byte before/after | zero delta |

The final numeric time gates are: warm prepare/resolve and mount p50/p95
≤baseline+5%+2 ms with zero CAS payload; remount same; squash
≤baseline+10%+5 ms; no-op exec ≤baseline+3%+0.5 ms; native command, read,
and write ≥97%; PTY create ≤+3%+1 ms; drain/stdin/control-C/control-D
≤+3%+0.5 ms; disjoint publication ≥90%; small-edit publish p95
≤+15%+5 ms; cold hydration ≥70% native copy; cold activation p95
≤1.5× native copy plus warm allowance.

Maintenance gates are: enqueue autosquash at projected depth≥48 and
compact/reject before depth>64; routine squash benefit≥8 carriers and manual
benefit≥2; pack payload≤64 MiB, records≤100,000, allocation≤80 MiB;
individual compaction at≥20% dead; urgent aggregate when>5%, target≤2%;
each slice≤100,000 records or64 MiB; deletion grace≥one complete durable epoch
plus a final lease/root/generation recheck.

Every record includes product/test commit, dirty state, binary digest, config
and rollout mode, host/runtime versions, image index/platform digest,
architecture, CPU/memory/storage allocation, kernel/filesystem/mount/xattr,
toolchains, corpus/seed, cache state, operation order, source/scope, and
`measured|derived|estimated|unknown`. Evidence streams are bounded or written
incrementally. An `unknown` or `unavailable` normative value fails unless an
independent, predeclared source measures the same quantity.

## 11. Stage exit verdict

The qualification verdict is `go` only when:

- all promoted focused and affected-regression cases pass;
- correctness, crash recovery, OCC, idempotency, namespace isolation, lease
  safety, and atomic visibility pass before scoring;
- every required time, throughput, SeqCDC, locality, memory, space, pack, GC,
  squash, and cleanup number passes without a weakened threshold;
- scalar SeqCDC is byte-identical across required triples, safe, and ≤300
  physical non-test Rust lines or has an approved recorded exception;
- exact dependency, feature, manifest-edge, service, helper, download, and
  target-image prerequisite deltas are zero;
- every required-release host row executes successfully using the sole pinned
  Ubuntu OCI index, with the verified resolved platform manifest recorded;
- candidate-default soak has zero legacy authority/fallback/mismatch and
  bounded resources;
- rollback and forward restore preserve all roots and public behavior;
- every legacy root has a verified v2 mapping, no legacy lease is live, a
  restorable pre-retirement snapshot exists, and target-only restart passes;
- artifacts and legal provenance are complete, immutable, schema-valid, and
  retained.

Any unverified required row, missing gating observation, corruption, partial
visibility, unexpected fallback, mismatched root, dependency delta, suspected
leak, unexplained persistent byte, cleanup trespass, or artifact/schema gap is
`no-go`. A result-changing fix invalidates the affected observations and they
are rerun before cumulative sign-off.

Retirement is a sequence, not one deletion: remove legacy writes and rerun;
remove legacy read selection and rerun; remove compatibility code/config and
rerun; rename legacy artifacts into lease-checked recoverable trash, restart,
then delete and rerun target-only recovery. If any slice fails before deletion,
return to Stage 10 authority. After deletion, recovery uses the documented
snapshot plus compatibility-reader restore binary. Phase 1 is complete only
after the post-retirement sentinel and evidence publication pass.
