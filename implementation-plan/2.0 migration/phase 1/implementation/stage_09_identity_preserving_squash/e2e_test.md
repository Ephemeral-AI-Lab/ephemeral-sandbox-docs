# Stage 09 E2E — Identity-preserving squash

[Implementation overview](../index.md) · [Stage 09 specification](spec.md) · [Preparation 03](../../prep/03-seqcdc-cas-and-squash-decision.md) · [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Product root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
Test root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`

## 1. Stage-local test objective

Implementation execution is blocked unless the product worktree is on the
exact fresh branch `upgrade-2.0-phase-1`, created from the newest approved
immutable product revision, with its base commit, upstream, clean scoped
worktrees, and responsible implementer recorded before any code edit. This
planning stage creates or switches no branch; any mismatch is a hard blocker.

This **POC proof tier** proves one sharp invariant: squash replaces only the physical Docker materialization. It does not republish, rename, or regenerate the logical checkpoint.

At the focused exit boundary:

- `RootId`, root-record bytes/digest, `PublicationId`, and publication/OCC generation are identical before and after squash and restart;
- `MaterializationId` changes and materialization generation strictly advances;
- exact file/tree/metadata behavior survives target build, catalog CAS, live remount, old/new lease overlap, cancellation, and crash recovery;
- projected depth and carrier-benefit rules are enforced and pack/locator pressure is routed to Stage 08;
- legacy v1 authority and rollback artifacts remain byte-stable;
- native command/file/PTY/stdin paths never consult CDC/CAS/packs;
- all case-owned logical resources release in one long-lived daemon with zero external dependency delta.

The stage runs focused cases and one tiny loop only. Final p50/p95, space
amplification, memory/RSS scale, full soak/regression, and required
host/release-runner qualification using the sole pinned Ubuntu target remain
Stage 11. Cross-image portability is outside Phase 1 and is not a gate.

## 2. Existing assets to reuse

| Asset | How Stage 09 uses it |
| --- | --- |
| `e2e/harness/catalog/declarations.py` | Complete stable typed metadata for every live case |
| validation reporter | One terminal validation checkpoint after cleanup, fsynced JSONL, exact manifest node IDs |
| run resource controller | Tracked sandbox/session/execution ownership and LIFO cleanup; no global prune |
| workspace publication cases | Public publish/read/OCC/tree/content/metadata oracles |
| existing squash fixture catalogs (`SMK-*`, `MED-*`, `HRD-*`, `LOAD-499`) | Source workload vocabulary and edge semantics; not evidence for candidate identity until rerun on v2 |
| autosquash cases (`autosquash.cor.01..10`, `autosquash.perf.01..06`) | Existing queue/trigger/remount coverage to preserve; new typed cases isolate 48/64/benefit routing |
| `benchmark` preset `squash-remount` | Existing factor vocabulary; Stage 09 adds a separate small candidate-v2 plan rather than changing historical results |
| resource sampler | Monotonic timing, logical/allocated filesystem, public cgroup/container sources, layerstack observations |
| artifact store/readers | Run manifest v2, observations v5, report/summary/export v4, bounded evidence v1 |
| Stage 08 maintenance tests | Carrier grace, locator safety, bounded worker/buffer/permit and no-unexplained-byte invariants |

Before every live command, append intent, exact command, expected identity/lease evidence, ownership scope, and cleanup to `e2e/test-report.md`; append Good/Defect/Fix and artifact IDs afterward. This document authorizes no test execution.

## 3. Resulting test tree

```text
ephemeral-sandbox/
├── crates/sandbox-runtime/layerstack-core/tests/squash_plan.rs          [add]
├── crates/sandbox-runtime/layerstack/tests/squash_identity.rs           [add]
├── crates/sandbox-runtime/layerstack/tests/squash_recovery.rs           [add]
├── crates/sandbox-runtime/workspace/tests/materialization_remount.rs    [add]
└── crates/sandbox-runtime/operation/tests/identity_preserving_squash.rs [add]

ephemeral-sandbox-test/
├── e2e/runtime/layerstack_squash_v2/
│   ├── test_identity_preserving_squash.py                            [add]
│   ├── test_squash_remount_recovery.py                               [add]
│   └── SPEC.md                                                       [add]
├── benchmark/presets/layerstack-phase1-tiny-squash-v2.yml            [add]
├── .e2e-state/                                                       [reuse] — run-owned artifacts only
└── .benchmark-state/                                                 [reuse] — run-owned artifacts only
```

```text
BEFORE SQUASH
/eos/layer-stack/
├── manifest.json                                                         [legacy authority; frozen inventory]
├── workspace.json                                                        [legacy authority; frozen inventory]
├── base/                                                                 [legacy authority; frozen inventory]
├── layers/                                                               [legacy authority; frozen inventory]
├── .layer-metadata/                                                      [legacy authority; frozen inventory]
├── roots/v2/<prefix>/<RootId>.root                                       [logical identity R]
├── manifests/v2/                                                         [R reconstruction graph]
├── objects/v1/                                                           [R reconstruction graph]
├── packs/v1/                                                             [R reconstruction graph]
├── indexes/v1/                                                           [R reconstruction graph]
├── catalogs/v1/roots.catalog                                             [PublicationId + publication generation P]
├── catalogs/v1/materializations.catalog                                  [MaterializationKey=(RootId,backend_kind,backend_format_version,target_profile) -> old MaterializationId/generation/carriers, depth D including base]
├── catalogs/v1/locators.catalog
├── catalogs/v1/leases.catalog
├── catalogs/v1/retention.catalog
├── materializations/docker-overlayfs/v1/<old-MaterializationId>/carriers/<ordinal>/ [source lowers]
├── journals/v1/
│   ├── publication/                                                      [terminal/empty]
│   ├── hydration/                                                        [terminal/empty]
│   ├── compaction/                                                       [terminal/empty]
│   └── migration/                                                        [terminal/empty]
└── staging/v2/
    ├── publication/                                                      [empty]
    ├── hydration/                                                        [empty]
    ├── compaction/                                                       [empty]
    └── migration/                                                        [empty]

AFTER TARGET VERIFIED, BEFORE CATALOG CAS
/eos/layer-stack/
├── roots/v2/<prefix>/<RootId>.root                                       [same bytes R]
├── catalogs/v1/roots.catalog                                             [same P]
├── catalogs/v1/materializations.catalog                                  [MaterializationKey=(RootId,backend_kind,backend_format_version,target_profile) still maps to old MaterializationId/generation/carriers]
├── journals/v1/squash/<txn>.journal                                      [TargetVerified/CommitIntent, fsynced]
└── staging/v2/squash/<txn>/                                              [private verified replacement M'; not activatable]

AFTER CATALOG CAS / DURING REMOUNT
/eos/layer-stack/
├── roots/v2/<prefix>/<RootId>.root                                       [same bytes R]
├── catalogs/v1/roots.catalog                                             [same P]
├── catalogs/v1/materializations.catalog                                  [MaterializationKey=(RootId,backend_kind,backend_format_version,target_profile) -> new MaterializationId/generation/carriers]
├── leases/v1/
│   ├── <old-lease>.lease                                                 [overlaps new lease until switched]
│   └── <new-lease>.lease                                                 [overlaps old lease; never a gap]
├── materializations/docker-overlayfs/v1/
│   ├── <old-MaterializationId>/carriers/<ordinal>/                       [leased by unswitched sessions]
│   └── <new-MaterializationId>/carriers/<ordinal>/                       [new activations/switched sessions]
└── journals/v1/squash/<txn>.journal                                      [MaterializationInstalled/Remounting]

AFTER SUCCESS / RESTART RECOVERY / CLEANUP
/eos/layer-stack/
├── roots/v2/<prefix>/<RootId>.root                                       [R byte-identical]
├── catalogs/v1/roots.catalog                                             [P byte-identical]
├── catalogs/v1/materializations.catalog                                  [MaterializationKey=(RootId,backend_kind,backend_format_version,target_profile) -> durable new MaterializationId/generation/carriers]
├── journals/v1/squash/                                                   [terminal bounded/reaped]
├── staging/v2/squash/                                                    [empty]
├── materializations/docker-overlayfs/v1/<old-MaterializationId>/         [only if a valid lease/grace owns it, else reclaimed]
├── materializations/docker-overlayfs/v1/<new-MaterializationId>/         [active verified carrier]
└── no unexplained unreachable+unleased candidate bytes

/eos/workspace/
├── manager.json                                                           [session -> M/generation recovery handles]
├── .export/
└── <session>/
    ├── upper/
    ├── work/
    └── executions/<exec>/transcript.log                                  [no global scratch writes]

/eos/namespace_execution/                                                  [compatibility-empty; boot-reaped; Stage11 removal]
```

All correctness and authority assertions use public CLIs/observability. Outside inventory supplies allocation, legacy immutability, and staging/grace evidence. Nothing inside the target image reads `/eos` or runs a helper.

## 4. Typed E2E case catalog

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `layerstack.phase1.squash.identity-preserving` | medium / `run-now-focused` | candidate-shadow identity-preserving squash | deterministic committed root and base-inclusive carrier depth | request squash; read/execute before and after; restart | `RootId`, root record, `PublicationId`, OCC generation, tree/content/metadata unchanged; `MaterializationId` changes and generation advances | phase durations, diagnostic only | old/replacement/staging/grace allocated bytes | workers, permits, leases, remount state return to warmed idle | zero dependency delta; pinned Ubuntu provider proof | `60000` ms | receipts, identity tuples, tree digests, materialization catalogs, disk series, logs |
| `layerstack.phase1.squash.remount-lease-recovery` | hard / `run-now-focused` | remount/lease crash recovery | active sessions and commands; failpoints before/after target durability, catalog CAS, and session persistence | squash, concurrently execute/read, cancel/restart/remount | every session has old-or-new valid carrier and continuous lease; failed switch remains old; source reclaim waits for lease+grace | per-boundary recovery/remount duration | target/source/mount staging/residue | old/new lease overlap bounded; all session and worker owners quiesce | no target-image helper; provider adapter boundary evidence | `60000` ms | lease generations, remount timeline, manager state, journals, allocation inventory, logs |
| `layerstack.phase1.squash.depth-admission` | medium / `run-now-focused` | autosquash admission policy | projected depths 47/48/63/64/65; routine benefit 7/8; manual 1/2; pack/locator pressure | publish/request manual squash and inspect bounded public maintenance state | enqueue at 48; prevent >64; exact benefit boundaries; pack/locator pressure never enqueues squash | decision/queue latency | no unexpected target/staging allocation on rejection | queue/permit/operation gauges return to baseline | pure portable-plan evidence plus zero graph delta | `60000` ms | admission observations, operation receipts, disk diff, gauges, logs |
| `layerstack.phase1.squash.tiny` | bench / `run-now-tiny-bench` | diagnostic squash loop | fixed ~16 MiB carriers/depths; one warmup; ≥5 alternating legacy/candidate pairs | public publish, squash, read/execute, clean up | exact tree and identity receipt on every repetition; hard depth/resource invariants | raw paired phases and diagnostic threshold | peak source+target and settled categorized allocation | logical final/high-water gauges and explicit cgroup/RSS availability | frozen dependency evidence and pinned-environment manifest | `60000` ms | plan/result JSON, raw samples, environment, disk/memory series, logs |
| `layerstack.phase1.squash.qualification` | release / `planned-final` | cumulative final squash qualification | Stage 11 scale/time/RSS/space/soak/required-host matrix using the sole pinned Ubuntu 24.04 target image | Stage 11 public benchmark and affected suite | all normative identity, latency, space, memory, restart, and required-runner gates | paired p50/p95 and ≤5 min pair | full peak/settled envelope | full scale and repeated-cycle stability | required release runners use the pinned Ubuntu 24.04 target; cross-image acceptance is deferred beyond Phase 1 | `300000` ms | Stage 11 qualification bundle only |

Each live case emits exactly one terminal validation checkpoint after tracked cleanup.

```python
@pytest.mark.medium
@pytest.mark.config
@e2e_test(
    id="layerstack.phase1.squash.identity-preserving",
    title="Squash preserves logical root and publication identity",
    description="Builds and installs a replacement Docker materialization for a committed candidate-shadow root, then proves byte-identical RootId/root record/publication generation and a strictly advanced materialization generation.",
    features=("workspace-session", "layerstack", "phase1-cas", "materialization", "squash"),
    validations={
        "terminal": "RootId, root record, PublicationId, and publication generation are unchanged; MaterializationId changes, materialization generation advances, exact content/metadata remains readable, legacy remains authoritative, and cleanup quiesces.",
    },
    validation_features={
        "terminal": ("layerstack", "materialization", "squash", "observability", "resource-efficiency"),
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
    id="layerstack.phase1.squash.remount-lease-recovery",
    title="Squash remount recovery keeps continuous carrier leases",
    description="Restarts or cancels at target durability, materialization CAS, and per-session remount boundaries while old and new sessions execute on native carriers.",
    features=("workspace-session", "layerstack", "phase1-cas", "materialization", "squash", "recovery", "leases"),
    validations={
        "terminal": "Recovery chooses the cataloged materialization, every session has an old-or-new valid lease with no gap, failed remounts stay on old carriers, exact reads/execs succeed, and source reclamation waits for lease plus grace.",
    },
    validation_features={
        "terminal": ("layerstack", "squash", "recovery", "leases", "resource-efficiency"),
    },
    execution_surface="cli",
    owner_id="layerstack-phase1",
    timeout_ms=60_000,
)
```

```python
@pytest.mark.medium
@pytest.mark.config
@e2e_test(
    id="layerstack.phase1.squash.depth-admission",
    title="Projected depth and squash benefit admission are exact",
    description="Exercises base-inclusive projected-depth, routine/manual benefit, hard admission, and pressure-source boundaries through public publication and bounded maintenance observations.",
    features=("workspace-session", "layerstack", "phase1-cas", "squash", "autosquash", "admission-control"),
    validations={
        "terminal": "Projected D at 48 enqueues, work prevents D above 64, routine benefit 8 and manual range 2 are exact boundaries, pack or locator pressure never enqueues squash, and all rejected/admitted operations clean up.",
    },
    validation_features={
        "terminal": ("layerstack", "squash", "autosquash", "admission-control", "observability"),
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
    id="layerstack.phase1.squash.qualification",
    title="Identity-preserving squash release qualification",
    description="Stage 11-only cumulative matrix for normative squash timing, peak/settled space, memory, restart soak, regression, and required release runners using the sole pinned Ubuntu 24.04 target image; cross-image acceptance is deferred beyond Phase 1.",
    features=("layerstack", "phase1-qualification", "squash", "materialization", "portability"),
    validations={
        "terminal": "Every Stage 11 normative gate and required-release row has executed evidence while identity and lease invariants remain exact.",
    },
    validation_features={
        "terminal": ("layerstack", "phase1-qualification", "squash", "resource-efficiency", "portability"),
    },
    execution_surface="cli",
    owner_id="layerstack-phase1",
    timeout_ms=300_000,
)
```

The tiny benchmark is cataloged through the same typed pytest metadata path:

```python
@pytest.mark.bench
@pytest.mark.config
@e2e_test(
    id="layerstack.phase1.squash.tiny",
    title="Tiny identity-preserving squash diagnostic loop",
    description="Runs a fixed bounded squash plan across carrier depths and active-session counts with alternating control/candidate samples and an exact identity/tree oracle.",
    features=("workspace-session", "layerstack", "phase1-cas", "materialization", "squash", "benchmark"),
    validations={
        "terminal": "Every repetition preserves logical/publication identity and exact tree bytes, advances materialization identity, holds hard resource bounds, and emits complete run-owned raw evidence.",
    },
    validation_features={
        "terminal": ("layerstack", "squash", "materialization", "resource-efficiency", "observability", "benchmark"),
    },
    execution_surface="cli",
    owner_id="layerstack-phase1",
    timeout_ms=60_000,
)
```

Plan metadata: existing plan schema; fixed seed/corpus; factors `route × depth × active-session-count`; one warmup; ≥5 alternating measured pairs; 60-second cell cap; exact `tree_digest` and identity receipt oracle; filesystem/layerstack/public-memory collectors; tracked cleanup; disposition `run-now-tiny-bench`.

## 5. Correctness and failure matrix

| Case/fault boundary | Required result | Disposition |
| --- | --- | --- |
| empty/no-op materialization or no qualifying source | `NotNeeded`; no journal/target/generation change | `run-now-focused` |
| routine benefit 7/8 carriers | reject at 7; eligible at 8 | `run-now-focused` |
| manual source 1/2 lowers | reject at 1; accept 2 only if depth decreases | `run-now-focused` |
| base-inclusive projected D 47/48 | no async depth trigger / enqueue at 48 | `run-now-focused` |
| projected D 64/65 | 64 admitted; 65 requires completed compaction or publication rejects | `run-now-focused` |
| pack dead/slack or last-locator debt, low native pressure | Stage 08 compaction/evacuation counter advances; squash counter does not | `run-now-focused` |
| crash/cancel during private target build | target absent/quarantined; catalog remains old `M@g` | `run-now-focused` |
| crash after target fsync, before commit intent/CAS | same logical root and old materialization active; private target reaped | `run-now-focused` |
| unknown CAS outcome | recovery reads materialization generation; never guesses or republishes | `run-now-focused` |
| crash after CAS before first/remid/last remount | new activations use new generation; unswitched sessions remain on leased old carriers; recovery resumes | `run-now-focused` |
| remount prepare/quiesce/mount/persist failure | affected session stays valid on old materialization; no lease gap | `run-now-focused` |
| session destroy races remount | ownership has one terminal path; old/new leases both release | `run-now-focused` |
| publication/OCC races squash | either materialization CAS fences and conflicts or same root completes; publication identity never overwritten | `run-now-focused` |
| retained old root shares carriers | Stage 08 graph/lease rules retain required carriers | `run-now-focused` |
| corruption in replacement tree/metadata | verification rejects before CAS; legacy and old candidate carrier readable | `run-now-focused` |
| mode/symlink/hardlink/sparse/xattr/whiteout/opaque/ownership fixture | exact supported semantics before/after | `run-now-focused` |
| active command/file/PTY/stdin during switch | documented quiesce semantics; native operations only, no CAS lookup | `run-now-focused` |
| restart after terminal before journal reap | idempotent no-op plus bounded reap | `run-now-focused` |
| normative time/space/RSS and required-host matrix using the sole pinned Ubuntu target | no Stage 09 qualification claim | `planned-final` |

Every row records root and root-record digests, publication/materialization generations, carrier/lease sets, manager generation, journal phase, exact tree digest, authority/fallback counters, and ownership cleanup.

## 6. Tiny correctness and benchmark loop

Preset `layerstack-phase1-tiny-squash-v2` uses:

- a deterministic ~16 MiB mixed tree with localized edit, incompressible file, repeated object, 256 small files, and supported metadata edge fixtures;
- depths 8, 47, 48, and 63 plus synthetic pure-policy tests for 64/65;
- one and four active sessions; one command remains quiesce-safe during the remount case;
- routine source reductions 7 and 8 and one valid manual two-lower reduction;
- one warmup and at least five alternating legacy-control/candidate-shadow pairs; prefer 3–5 warmups and 10 samples only inside the total 30–60 second developer loop.

Per pair: publish fixture → snapshot identity/generations → create sessions/read/exec → trigger squash → exact before/after oracle → destroy → poll quiescence. Inputs, seed, operation order, image, config, filesystem, cache class, and host allocation are identical.

Capture raw plan/build/verify/fsync/CAS/frozen-remount/end-to-end time, but with this sample count report no p95 claim. Capture source/target/grace logical+allocated bytes, depth/carrier counts, metadata/object/pack bytes, bytes read/written, session remount and lease counts, resource gauges, route counters, and explicit memory-source availability. Every operation/cell must finish in ≤60 seconds.

The loop proves identity and boundedness. It does not pass the final `baseline+5%+2ms` remount or `baseline+10%+5ms` full squash percentile gates.

## 7. Memory-stability and reclamation test

Keep one daemon alive for 20 measured cycles after three warmups:

```text
warmed idle
  -> publish fixed candidate-shadow root
  -> create four sessions and native reads/execs
  -> build one replacement carrier
  -> catalog CAS and old/new lease-overlap remount
  -> destroy sessions; release transaction lease
  -> complete Stage08 grace/recheck for old carrier
  -> poll quiescence ≤5 seconds
  -> settled sample
```

No daemon restart occurs between measured cycles. Dedicated crash-recovery runs are excluded from slope inference. Quiescence requires zero case-owned transaction/journal-staging/session/execution/remount/borrowed buffer/queue/permit/lease/FD owners, old carrier absent unless a declared retained root/grace owns it, and worker/cache values at their configured warmed baseline.

Sample at 100 ms into a bounded stream/ring: process RSS if PID identity is proven, cgroup current/peak, Docker stats fallback, source/target/grace allocated bytes, logical owned/high-water bytes, buffers/workers/tasks/queues/permits, old/new leases, remount pending, mappings/FDs/cache, and quiescence latency. Missing daemon RSS is explicit, never zero.

Use the equal-warmup control's first/last five-cycle settled medians, delta, robust slope, count, and raw noise band. Logical non-release, unexplained bytes, timeout, missing gating data, or repeated physical growth outside that coarse band blocks. Restart-to-clean, arbitrary sleeps, allocator changes, `malloc_trim`, and cache purge are forbidden.

## 8. Dependency and portability proof

Re-capture before/after canonical external package identities/checksums, external feature pairs, direct external manifest-edge multiset, workspace manifests/lockfile, Python/npm/vendor inventories, image packages/helpers, and external route processes/sockets/services/commands/downloads. Pass only on exact equality. Internal workspace edges may expose the already-designed narrow materialization port but must point operation/workspace → layerstack → core and remain cycle-free.

No target-image shell, libc, `tar`, coreutils, checksum program, Python, package manager, static helper, sidecar, or network service may build or verify the target. Docker/OverlayFS adapter code performs native carrier work outside the image. Core golden plans must be independent of path separator, inode, host order, endianness, word size, time, locale, CPU feature, Docker VM path, and provider locator.

The focused environment uses the sole Phase 1 target,
`ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`,
and records the resolved platform manifest. This is POC evidence for one
required-host row only. Read-only and non-root runtime variants use the same
image identity. Stage 11 executes every required host/architecture/Docker
release-runner row using this same OCI index and records the resolved platform
manifest; unexecuted required rows remain unverified. Cross-image portability
is deferred beyond Phase 1 and is neither an acceptance nor a retirement gate.

## 9. Focused and final-stage commands

### Product formatting, lint, and focused unit/integration

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack -p sandbox-runtime-workspace -p sandbox-runtime --all-targets --all-features -- -D warnings
cargo test -p sandbox-runtime-layerstack-core --test squash_plan
cargo test -p sandbox-runtime-layerstack --test squash_identity --test squash_recovery
cargo test -p sandbox-runtime-workspace --test materialization_remount
cargo test -p sandbox-runtime --test identity_preserving_squash
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

From the declared test root, append `e2e/test-report.md` intent first:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_squash_v2/test_identity_preserving_squash.py \
  e2e/runtime/layerstack_squash_v2/test_squash_remount_recovery.py \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

Use `E2E_REBUILD_BINARY=0` only after recording matching gateway binary/config identity; a responsive gateway can be reused even when `E2E_REBUILD_BINARY=1`, so record custody rather than assuming rebuild.

### Artifact compatibility validation

Catalog and artifact compatibility:

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
  --plan layerstack-phase1-tiny-squash-v2 \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --plan layerstack-phase1-tiny-squash-v2 \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

The benchmark uses prebuilt binaries.

### DO NOT RUN in Stage 09 — Stage 11 affected regression

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

### DO NOT RUN in Stage 09 — Stage 11 native-host/pinned-Ubuntu-24 matrix

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

### DO NOT RUN in Stage 09 — Stage 11 full Phase 1 qualification

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

| Metric | Source/cadence | Stage 09 gate |
| --- | --- | --- |
| `root_id`, root-record digest, `publication_id/generation` before/after/restart | product receipt + raw committed record evidence | exact equality |
| `materialization_id/generation` | catalog/observation at each boundary | ID changes; generation strictly increases |
| exact tree/content/metadata digest | public API before/after/each recovery | exact equality |
| legacy inventory/authority/fallback/mismatch | outside digest + public route | byte-stable; legacy/legacy; zero/zero |
| depth/projected depth/carrier reduction/reason | policy/action observation | 48/64 and 8/2 boundaries exact; no pack-pressure squash |
| old/new carrier leases and remount state | catalog/manager/observation per session boundary | no lease gap; terminal pending zero |
| source/target/grace allocated bytes | filesystem allocated inventory | at most one replacement shape; every byte has owner |
| native hot-path CAS/pack lookup/read | bounded route counter before/after command/file/PTY/stdin | zero |
| plan/build/verify/fsync/CAS/frozen/full elapsed ns | monotonic clock, raw each iteration | ≤60 seconds POC; normative percentiles deferred |
| workers/buffers/queues/permits/tasks/transactions/FDs/cache | product gauges at boundary + 100 ms | fixed caps and warmed-idle return ≤5 s |
| process/cgroup/container memory | declared source, 100 ms bounded | coarse control-band sentinel; unavailable explicit |
| dependency/environment fingerprint | exact immutable artifacts | zero external delta; all comparability fields present |

Environment includes exact product/test commits and dirty state, Docker Desktop/Engine, OCI index/platform digest, host/guest architecture, CPU/memory/storage allocation, guest kernel/filesystem/mount/userxattr, Rust/Python, config/rollout mode, cache classification, seed/corpus, and memory source. Every result uses exactly one provenance label—`measured`, `derived`, `estimated`, or `unknown`; only `measured`/`derived` support a gate. Separately named model projections are non-gating source conventions, never result provenance.

Artifacts remain run-owned, bounded, schema-valid, and tied to exact test node IDs. Cleanup uses tracked IDs only and never prunes unrelated Docker or host state.

## 11. Stage exit verdict

The only passing label is `stage-09-poc-passed`. It requires all focused Rust/live cases and the tiny plan to complete; exact logical/publication identity equality; strictly advanced materialization identity/generation; exact filesystem behavior; continuous old/new leases; idempotent recovery at every boundary; exact depth/benefit/pressure routing; no legacy mutation or candidate authority; zero hot-path CAS/pack work; bounded logical release and acceptable coarse memory sentinel; artifact/catalog validity; tracked cleanup; and exact zero external dependency/runtime delta.

Block on any root/publication change, ambiguous generation, lease gap, source deletion while owned, remount data loss, depth >64, wrong pressure route, corruption, fallback/authority ambiguity, persistent unexplained bytes, missing gating evidence, suspected leak, artifact mismatch, cross-run cleanup, or dependency delta.

This verdict does not authorize candidate authority, default enablement, legacy retirement, or final time/space/RSS/portability claims. Stage 10 owns the first candidate authority; Stage 11 owns qualification and retirement.
