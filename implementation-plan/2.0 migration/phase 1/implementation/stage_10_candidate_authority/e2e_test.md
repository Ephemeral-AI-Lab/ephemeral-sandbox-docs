# Stage 10 E2E — Candidate authority, legacy shadow, and read rollback

[Implementation overview](../index.md) · [Stage 10 specification](spec.md) · [Benchmark note](benchmark_note.md) · [Preparation 03](../../prep/03-seqcdc-cas-and-squash-decision.md) · [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Product root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
Test root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`

## Performance arrival checkpoint

Stage 10 has not reached its exit until the focused test runner writes versioned
`.benchmark-state/results/<run-id>/stage-10-perf-report.json` and
`stage-10-perf-report.md` with
`schema_version="phase1.stage10.perf-report.v1"`, the frozen baseline actual,
required pass target/cap, separately predeclared optimization target,
candidate actual, delta/ratio/headroom, complexity/work counters,
logical-resource high-water counters, memory/RSS,
complete allocated-space accounting, links between the reports and to
immutable run/raw artifacts, provenance, and a `DIAGNOSTIC_PASS` or `FAIL`
verdict. The first Markdown table exposes those comparison fields per
stage-owned metric. It must then update the append-only
[benchmark tracker](benchmark_note.md) and
[overall scorecard](../stage_03_11_benchmark_note.md), and append the exact
command, outcome, report links, and cleanup to `e2e/test-report.md`.

The full Stage 10 local cycle is **ESTIMATED** at 65–135 s: setup 8–14 s,
warmups 7–14 s, measured work 37–72 s, quiescence/cleanup 7–20 s, and
reporting 6–12 s. Its core developer loop remains 30–60 s. These are planning
numbers; the ≤60 s operation/cell and ≤5 min invocation limits remain hard.

## 1. Stage-local test objective

Implementation execution is blocked unless the product worktree is on the
exact fresh branch `upgrade-2.0-phase-1`, created from the newest approved
immutable product revision, with its base commit, upstream, clean scoped
worktrees, and responsible implementer recorded before any code edit. This
planning stage creates or switches no branch; any mismatch is a hard blocker.

This is the first **POC proof tier** allowed to enable candidate authority, and only in an explicit test configuration. It proves:

- candidate roots-catalog OCC CAS is the sole publication linearization point;
- retry after crash or lost response returns the byte-identical committed receipt and never creates a second root generation;
- candidate strict read is the normal route and has zero silent legacy fallback;
- a one-way legacy shadow consumes committed receipts in order and verifies exact filesystem parity;
- explicit legacy read rollback requires a quiesced authority-epoch change and a verified shadow cursor equal to the current candidate root/generation;
- candidate remains the only publication authority while reads use the legacy rollback route;
- mixed v1/v2 roots and all candidate/shadow/read-route restart boundaries recover deterministically;
- a bounded candidate-authority soak releases resources without retiring any legacy asset or adding a dependency.

This stage does not make candidate mode the default and does not run the full
suite, normative performance/space/RSS matrices, required host/release-runner
and image-capability matrices, or retirement gate. Stage 11 owns all of them,
including the complete Prep 04 image matrix; any unverified required-release
row blocks acceptance and retirement.

## 2. Existing assets to reuse

| Asset | Reuse and constraint |
| --- | --- |
| `e2e/harness/catalog/declarations.py` | Full stable metadata for each live case |
| validation reporter | One terminal post-cleanup validation checkpoint, exact node IDs, flushed/fsynced JSONL |
| run resource controller | Tracked sandbox/session/execution ownership and LIFO cleanup only; never global Docker/host prune |
| `runtime.workspace-session.publish.surface/changed/no-op/active-command/protected-atomic/clean-merge/conflict-retry/binary-conflict/destroy-compat/validation-replay/disposition-race/parallel-disjoint/special-file` | Existing public publication behaviors; select focused representatives and preserve all for Stage 11 regression |
| Stage 06/07 strict-read/publication failpoint fixtures | Candidate missing/corrupt object, OCC CAS, response loss, journal restart, exact root/tree oracle |
| Stage 08 retention/pack/GC cases | No last-locator loss, epoch grace, pack caps, zero unexplained bytes |
| Stage 09 squash/remount cases | Identity-preserving materialization, continuous leases, depth admission |
| resource-efficiency cases (`triggered-diagnostic`, `holder-exit`, `holder-destroy-race`, `manager-resource-quiescence`, `lifecycle-soak`, `workspace-cycle-reclaim`) | Ownership/quiescence patterns; Stage 10 uses a bounded authority-specific soak |
| benchmark runner/sampler | Sole sequential scheduler; monotonic time, logical/allocated bytes, public cgroup/container memory, layerstack observations |
| artifact compatibility tests | Run manifest v2, observation v5, report/summary/export v4, bounded evidence v1 reader contract |

Before a live command, append its exact command, intent, expected authority/shadow/cleanup evidence, ownership scope, and rollback to `e2e/test-report.md`. After execution append Good/Defect/Fix, run/artifact IDs, and cleanup. Planning executes no live test.

## 3. Resulting test tree

```text
ephemeral-sandbox/
├── crates/sandbox-runtime/layerstack-core/tests/authority_state.rs       [add]
├── crates/sandbox-runtime/layerstack/tests/
│   ├── candidate_authority.rs                                           [add]
│   ├── legacy_shadow.rs                                                 [add]
│   └── authority_recovery.rs                                            [add]
├── crates/sandbox-runtime/workspace/tests/authority_route_restart.rs    [add]
└── crates/sandbox-runtime/operation/tests/candidate_authority.rs         [add]

ephemeral-sandbox-test/
├── e2e/runtime/layerstack_candidate_authority/
│   ├── test_candidate_authority.py                                  [add]
│   ├── test_legacy_read_rollback.py                                 [add]
│   ├── test_mixed_root_restart.py                                   [add]
│   └── SPEC.md                                                      [add]
├── benchmark/presets/layerstack-phase1-tiny-authority-soak.yml      [add]
├── .e2e-state/                                                      [reuse] — run-owned artifacts only
└── .benchmark-state/                                                [reuse] — run-owned artifacts only
```

```text
PRE-CUTOVER / LEGACY MODE
/eos/layer-stack/
├── manifest.json                                                       [legacy authority and rollback corpus]
├── workspace.json                                                      [legacy authority and rollback corpus]
├── base/                                                               [legacy authority and rollback corpus]
├── layers/                                                             [legacy authority and rollback corpus]
├── .layer-metadata/                                                    [legacy authority and rollback corpus]
├── roots/v2/                                                           [candidate shadow, verified through Stage09]
├── manifests/v2/                                                       [candidate shadow, verified through Stage09]
├── objects/v1/                                                         [candidate shadow, verified through Stage09]
├── packs/v1/                                                           [candidate shadow, verified through Stage09]
├── catalogs/v1/
│   ├── roots.catalog
│   ├── locators.catalog
│   ├── materializations.catalog
│   ├── leases.catalog
│   └── retention.catalog
├── journals/v1/
│   ├── publication/                                                    [terminal/empty]
│   ├── hydration/                                                      [terminal/empty]
│   ├── squash/                                                         [terminal/empty]
│   ├── compaction/                                                     [terminal/empty]
│   └── migration/                                                      [terminal/empty]
└── no authority.catalog or its mode remains legacy

CANDIDATE COMMIT LINEARIZED, SHADOW PENDING
/eos/layer-stack/
├── roots/v2/<prefix>/<new-RootId>.root                                 [authoritative root]
├── catalogs/v1/roots.catalog                                           [authoritative generation g+1]
├── catalogs/v1/authority.catalog                                       [candidate write/read epoch]
├── journals/v1/publication/<PublicationId>.journal                      [committed receipt/terminal]
├── catalogs/v1/legacy-shadow.catalog                                   [cursor at g, Pending g+1]
├── journals/v1/migration/<id>.journal                                  [ordered shadow application]
├── manifest.json                                                       [still verified g; never silently read]
└── layers/                                                             [still verified g; never silently read]

SHADOW VERIFIED / NORMAL CANDIDATE READ
/eos/layer-stack/
├── catalogs/v1/roots.catalog                                           [candidate root/generation g+1]
├── catalogs/v1/materializations.catalog                                [candidate materialization generation]
├── materializations/docker-overlayfs/v1/<MaterializationId>/carriers/  [candidate native read]
├── manifest.json                                                       [derived v1 shadow g+1]
├── layers/                                                             [derived v1 shadow g+1]
├── .layer-metadata/                                                    [derived v1 shadow g+1]
├── catalogs/v1/legacy-shadow.catalog                                   [same RootId/generation + v1 digest, Verified]
└── catalogs/v1/authority.catalog                                       [write=candidate, read=candidate]

EXPLICIT LEGACY READ ROLLBACK
/eos/layer-stack/
├── catalogs/v1/authority.catalog                                       [new epoch: write=candidate, read=legacy_rollback]
├── catalogs/v1/roots.catalog                                           [candidate remains publication truth]
├── catalogs/v1/legacy-shadow.catalog                                   [Verified cursor exactly equals current root/generation]
├── manifest.json                                                       [selected legacy read state, not publication authority]
└── layers/                                                             [selected native v1 layers, not publication authority]

AFTER RESTART / RETURN TO CANDIDATE / CLEANUP
/eos/layer-stack/
├── catalogs/v1/
│   ├── authority.catalog                                               [generation-consistent]
│   ├── roots.catalog                                                   [generation-consistent]
│   ├── legacy-shadow.catalog                                           [generation-consistent]
│   └── materializations.catalog                                        [generation-consistent]
├── journals/v1/
│   ├── publication/                                                    [terminal bounded/reaped]
│   ├── hydration/                                                      [terminal bounded/reaped]
│   ├── squash/                                                         [terminal bounded/reaped]
│   ├── compaction/                                                     [terminal bounded/reaped]
│   └── migration/                                                      [terminal bounded/reaped]
├── staging/v2/
│   ├── publication/                                                    [empty]
│   ├── hydration/                                                      [empty]
│   ├── squash/                                                         [empty]
│   ├── compaction/                                                     [empty]
│   └── migration/                                                      [empty]
├── manifest.json                                                       [retained through Stage10]
├── workspace.json                                                      [retained through Stage10]
├── base/                                                               [retained through Stage10]
├── layers/                                                             [retained through Stage10]
├── .layer-metadata/                                                    [retained through Stage10]
└── no unexplained unreachable+unleased bytes

/eos/workspace/
├── manager.json                                                        [authority epoch + read route + RootId/M generation]
├── .export/
└── <session>/                                                          [active only; subtree absent after destroy]
    ├── upper/
    ├── work/
    └── executions/<exec>/transcript.log

/eos/namespace_execution/                                               [compatibility-empty, boot-reaped, no new writes]
```

Public manager/runtime/file/workspace/observability operations are the correctness boundary. Outside `/eos` inventory proves generations, allocation categories, staging absence, permissions, and legacy retention. The sandbox image neither sees `/eos` nor supplies a storage helper.

## 4. Typed E2E case catalog

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `layerstack.phase1.authority.candidate-shadow` | medium / `run-now-focused` | candidate-authoritative publication with legacy shadow | candidate-authority config; deterministic workspace; response-loss and shadow failpoints | publish/retry/read via public surfaces; wait for bounded shadow status | one candidate CAS/receipt; retry identical; strict candidate read exact; ordered legacy parity; legacy never publishes; zero fallback | publication/shadow phase durations, diagnostic only | candidate/staging/legacy-shadow categorized allocation | publisher/shadow workers, journals, permits, leases settle | exact zero dependency delta; pinned Ubuntu provider proof | `60000` ms | receipts, authority/cursor observations, tree digests, disk/memory series, logs |
| `layerstack.phase1.authority.legacy-read-rollback` | hard / `run-now-focused` | explicit verified legacy read rollback | lagging, mismatched, and caught-up shadow cursors; active sessions | request route changes; publish while legacy reads; return to candidate | lag/mismatch fail closed; caught-up epoch switch quiesced; candidate remains sole write authority; reads fenced; fallback zero | route/remount durations | route staging and candidate/legacy coexistence | session leases and route coordinator return to warmed idle | no per-read fallback/helper; provider-neutral epoch contract | `60000` ms | epoch/cursor timeline, remount/lease state, receipts, digests, allocation inventory, logs |
| `layerstack.phase1.authority.mixed-root-restart` | hard / `run-now-focused` | mixed v1/v2 restart recovery | retained pre-migration v1 plus migrated/new v2 roots; authority/publication/shadow/materialization failpoints | restart and read every selected root; retry incomplete public operations | one durable authority/root generation; all roots reconstruct; cursor/journal resume idempotently; legacy artifacts remain | recovery duration per failpoint | journal/staging/quarantine/trash/residue allocation | all owners quiesce and no lease/worker/journal leaks | zero dependency delta; v1/v2 format and pinned-environment evidence | `60000` ms | root matrix, authority/catalog snapshots, journal states, digests, disk/memory series, logs |
| `layerstack.phase1.authority.soak-tiny` | bench / `run-now-tiny-bench` | diagnostic authority stability loop | one daemon; warmup; 20 bounded cycles; ≥5 alternating pairs; receipt/shadow/route faults | publish/read/switch/restart/clean up through public surfaces | exact receipt/tree/cursor/authority oracle each cycle; hard resource and zero-fallback invariants | raw phase samples; 30–60 s loop diagnostic target | categorized peak/settled allocation | logical final/high-water gauges plus explicit cgroup/RSS availability | frozen dependency evidence and pinned-environment manifest | `60000` ms | plan/result JSON, raw samples, environment, timelines, disk/memory series, logs |
| `layerstack.phase1.authority.qualification` | release / `planned-final` | cumulative final qualification/default/retirement | Stage 11 regression/soak/performance/space/RSS matrix over required hosts and the complete Prep 04 image-capability matrix | Stage 11 public benchmark, rollback rehearsal, and affected suite | all normative gates/required rows pass before candidate default or legacy retirement | normative paired p50/p95; each matched cell ≤5 min | authoritative full peak/settled envelope | full repeated-cycle/scale/RSS gates | pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root cells; every unverified required-release row blocks | `300000` ms for aggregate artifact validation only; dispatched cells own their timeout | Stage 11 qualification bundle only |

Each live case emits exactly one terminal validation checkpoint after cleanup.

```python
@pytest.mark.medium
@pytest.mark.config
@e2e_test(
    id="layerstack.phase1.authority.candidate-shadow",
    title="Candidate publication is authoritative and legacy is an ordered shadow",
    description="Publishes through candidate OCC with response-loss and shadow failpoints, verifies idempotent receipts and exact candidate reads, and proves the legacy writer only applies committed receipts.",
    features=("workspace-session", "layerstack", "phase1-cas", "candidate-authority", "legacy-shadow"),
    validations={
        "terminal": "Exactly one candidate root generation and receipt commit; retries are identical; candidate strict reads match the oracle with zero fallback; legacy shadow reaches exact verified parity; legacy has no publication authority; cleanup quiesces.",
    },
    validation_features={
        "terminal": ("layerstack", "candidate-authority", "legacy-shadow", "observability", "resource-efficiency"),
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
    id="layerstack.phase1.authority.legacy-read-rollback",
    title="Legacy read rollback is explicit and generation-fenced",
    description="Attempts rollback with lagging, mismatched, and verified shadow cursors, then publishes while the verified legacy read route is active and returns to candidate strict read.",
    features=("workspace-session", "layerstack", "phase1-cas", "candidate-authority", "legacy-shadow", "read-rollback"),
    validations={
        "terminal": "Lagging or mismatched rollback fails closed; verified rollback persists a new read epoch and never changes candidate write authority; reads fence on shadow parity; return to candidate is quiesced and exact; fallback count stays zero.",
    },
    validation_features={
        "terminal": ("layerstack", "candidate-authority", "read-rollback", "recovery", "observability"),
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
    id="layerstack.phase1.authority.mixed-root-restart",
    title="Mixed legacy and candidate roots recover under candidate authority",
    description="Starts from retained v1 roots plus migrated and newly published v2 roots, restarts at authority, publication, shadow, materialization, and read-route boundaries, and verifies every selected root.",
    features=("workspace-session", "layerstack", "phase1-cas", "candidate-authority", "migration", "recovery", "retention"),
    validations={
        "terminal": "Recovery selects one durable authority epoch and root generation; old and new roots reconstruct; journals/cursors resume idempotently; no live root or locator is lost; every legacy artifact remains present; all owners quiesce.",
    },
    validation_features={
        "terminal": ("layerstack", "candidate-authority", "migration", "recovery", "retention", "resource-efficiency"),
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
    id="layerstack.phase1.authority.qualification",
    title="Candidate authority release qualification and legacy retirement gate",
    description="Stage 11-only full affected regression, authority soak, time/space/RSS matrices, required-host and complete Prep 04 image-capability matrices, default enablement, rollback rehearsal, and evidence-gated legacy retirement.",
    features=("layerstack", "phase1-qualification", "candidate-authority", "legacy-shadow", "portability"),
    validations={
        "terminal": "All normative gates and required-release rows execute successfully, candidate default is approved, rollback is rehearsed, and legacy retirement satisfies the explicit Stage 11 deletion gate.",
    },
    validation_features={
        "terminal": ("layerstack", "phase1-qualification", "candidate-authority", "resource-efficiency", "portability"),
    },
    execution_surface="cli",
    owner_id="layerstack-phase1",
    timeout_ms=300_000,  # aggregate artifact validator only; every dispatched cell owns its timeout
)
```

The tiny authority soak is cataloged through the same typed pytest metadata path:

```python
@pytest.mark.bench
@pytest.mark.config
@e2e_test(
    id="layerstack.phase1.authority.soak-tiny",
    title="Tiny candidate-authority stability soak",
    description="Runs a bounded one-daemon authority loop with alternating samples and receipt, shadow, and read-route faults while enforcing exact authority, cursor, and tree oracles.",
    features=("workspace-session", "layerstack", "phase1-cas", "candidate-authority", "legacy-shadow", "benchmark"),
    validations={
        "terminal": "Every cycle preserves one candidate publication authority, exact receipts/tree/cursors, zero silent fallback, hard resource bounds, and complete run-owned cleanup and evidence.",
    },
    validation_features={
        "terminal": ("layerstack", "candidate-authority", "legacy-shadow", "resource-efficiency", "observability", "benchmark"),
    },
    execution_surface="cli",
    owner_id="layerstack-phase1",
    timeout_ms=60_000,
)
```

Plan metadata: existing schema; fixed seed/corpus; factors `route × publication outcome × shadow state × read route`; one warmup plus ≥5 alternating measured pairs and 20 logical cycles when bounded; 60-second cell timeout; exact root/tree/receipt/cursor oracle; filesystem/layerstack/public-memory collectors; run-owned cleanup; disposition `run-now-tiny-bench`.

## 5. Correctness and failure matrix

| Boundary/fault | Required result | Disposition |
| --- | --- | --- |
| candidate no-op publication | no new root generation; deterministic no-op receipt; no shadow layer | `run-now-focused` |
| changed candidate publication | one roots-catalog CAS and receipt; exact read/metadata | `run-now-focused` |
| clean/disjoint OCC and parallel disjoint changes | expected merge/serialization, one generation per commit | `run-now-focused` |
| stale/conflicting/binary OCC | deterministic conflict/no commit; no shadow item | `run-now-focused` |
| crash before root CAS | no commit/receipt/shadow; private state recovered | `run-now-focused` |
| crash or lost response after root CAS | committed receipt recovered; retry returns exact receipt; no second generation | `run-now-focused` |
| shadow crash before/after v1 carrier rename/manifest replace/cursor CAS | candidate remains committed; ordered replay reaches one verified cursor | `run-now-focused` |
| shadow cannot encode or verify metadata | cursor `Degraded`; candidate strict remains authority; Stage 10 blocks; no silent read | `run-now-focused` |
| candidate missing object/corrupt manifest/locator/materialization | candidate read fails closed; injected integrity counter exact; fallback zero | `run-now-focused` |
| automatic exception/fallback attempt | impossible/rejected by route contract | `run-now-focused` |
| rollback request while cursor lags or digest mismatches | quiesced transition aborts, current candidate read route remains durable | `run-now-focused` |
| rollback request with exact cursor | new authority epoch; write=candidate/read=legacy; exact native parity | `run-now-focused` |
| new candidate commit during legacy read rollback | candidate CAS commits; reads fence until shadow catches up, then exact read; no stale value | `run-now-focused` |
| shadow degrades while rollback read active | new reads fail closed within bound; never serve stale generation | `run-now-focused` |
| crash before/after authority epoch persist and session remount | old or new complete read route; manager/catalog generations agree; recovery resumes | `run-now-focused` |
| return from legacy rollback to candidate strict | verified candidate materialization, quiesced epoch/remount, exact reads | `run-now-focused` |
| preexisting v1 current/history plus v2 roots | every retained/pinned/leased root reconstructs; v1 bytes retained | `run-now-focused` |
| retention/GC/pack compaction during authority soak | no live/leased root or last-locator loss; exact caps/grace | `run-now-focused` |
| identity-preserving squash during authority soak | RootId/publication generation unchanged; materialization generation advances | `run-now-focused` |
| active command/file/PTY/stdin | documented quiesce semantics, native carrier, zero CAS/pack hot-path work | `run-now-focused` |
| destroy/disposition race/cancellation | one terminal owner, no leaked session/execution/lease/journal | `run-now-focused` |
| full affected regression and normative matrices | not executed or qualified here | `planned-final` |

Parity fixtures cover empty/no-op, localized edit, incompressible binary, 100–1,000 small files, modes, symlink, supported hardlink/sparse/xattr/ownership, whiteout, opaque directory, conflicts, and restart. Each stores canonical logical tree digest plus candidate/legacy public read digest, not just byte totals.

## 6. Tiny correctness and benchmark loop

Preset `layerstack-phase1-tiny-authority-soak` uses a deterministic ~16 MiB mixed tree, depths 1/8/32, roots 1/8, one active and one retained old root, and candidate operations:

```text
warmed candidate-authority idle
  -> publish changed or no-op with stable PublicationId
  -> read/exec through candidate strict route
  -> apply and verify legacy shadow
  -> periodically squash materialization or compact one bounded pack
  -> on selected cycles request verified legacy read rollback
  -> publish once while rollback reads are active; fence until shadow parity
  -> return to candidate strict
  -> destroy and quiesce
```

Run one warmup and at least five alternating legacy-control/candidate pairs; the authority-specific logical sentinel runs 20 cycles after three warmups when the total developer loop remains 30–60 seconds. Prefer more warmups/10 samples only within that budget. Payloads are pre-generated. Seed, corpus, image, host allocation, operation order, config except route factor, filesystem, and cache class are fixed.

Collect raw publication phases, candidate activation, shadow lag/apply/verify, rollback quiesce/remount, read/exec, maintenance, and cleanup time; root/receipt/cursor generations; exact tree digests; logical/allocated bytes by candidate/legacy/staging/grace; pack/depth counts; bytes scanned/read/written/copied; workers/buffers/queues/permits/leases/transactions/FDs/cache; authority/fallback/mismatch; and declared physical memory source.

Each operation/cell must finish in ≤60 seconds. Report raw samples and median; make no p95 or release-performance conclusion from the POC.

## 7. Memory-stability and reclamation test

Use one daemon and one proven gateway binary/config identity across the measured 20-cycle authority loop. Do not restart between iterations. Dedicated restart failpoint cases are separate from slope inference.

Quiescence within five seconds requires:

- no case-owned workspace/session/execution/publication/shadow/migration/squash/compaction/GC transaction or staging;
- shadow queue has zero gaps and cursor equals current candidate generation;
- candidate strict route restored unless the case explicitly ends in verified rollback;
- all borrowed chunks, buffers, queue descriptors/bytes, permits, temporary mappings, and FDs released;
- durable leases only for declared retained/current roots and active sessions; active test leases zero after destroy;
- four-worker and 64 MiB global bounds respected; shared index cache within 4,096 pages/16 MiB;
- trash contains only declared not-yet-complete grace entries and persistent unexplained unreachable/unleased bytes equal zero;
- legacy shadow and all candidate roots remain policy-owned; legacy retention is not called a leak.

Capture bounded 100 ms samples/ring summaries for process RSS if identity is proven, cgroup current/peak, Docker stats fallback, logical owned/high-water resources, queue/cursor lag, candidate and v1 allocated categories, caches/registries/leases/transactions, quiescence latency, and outcome.

The physical rule is frozen before candidate samples from an equal-warmup control: first/last five-cycle settled medians, delta, robust slope, count, and raw noise band. Logical non-release, repeated physical growth beyond that coarse band, timeout, unexplained bytes, or missing gating data blocks. `measurement-unavailable` is never zero and must use the approved independent fallback. No restart-to-clean, arbitrary sleep, `malloc_trim`, allocator change, or cache purge.

## 8. Dependency and portability proof

Capture and compare exact before/after:

- external Rust `(source,name,version,checksum)` set;
- external `(package,feature)` set per frozen target/invocation;
- direct external manifest-edge multiset product-wide;
- workspace manifests and lockfile bytes;
- Python/npm/vendored/system/image package inventories;
- external commands/helpers/processes/sockets/services/downloads on candidate, shadow, rollback, recovery, and measurement paths;
- internal workspace edge direction and cycle freedom.

Pass requires zero external delta, including no relocated duplicate edge. Candidate/legacy composition uses existing internal crates and std-only core. No `tar`, shell, checksum command, Python, libc-specific utility, package manager, helper binary, FFI library, service, sidecar, or network lookup is added.

The pinned Stage 10 focused fixture is
`ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`;
record its resolved platform manifest plus Docker Desktop/Engine and guest
kernel/filesystem/mount/userxattr. Storage correctness uses public operations,
so the target image need not provide a command. Read-only and non-root runtime
variants are exercised locally where available. This focused row is not the
final host/image qualification. Stage 11 executes every required
host/architecture/Docker release-runner row and pins both OCI index and
resolved platform-manifest digests for Ubuntu/Debian glibc, Alpine musl,
minimal/distroless, and shell-less fixtures, including read-only and
non-root cases. No unexecuted required-release row is qualified; it blocks
default enablement and retirement.

## 9. Focused and final-stage commands

### Product formatting, lint, and focused unit/integration

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack -p sandbox-config -p sandbox-runtime-workspace -p sandbox-runtime --all-targets --all-features -- -D warnings
cargo test -p sandbox-runtime-layerstack-core --test authority_state
cargo test -p sandbox-runtime-layerstack --test candidate_authority --test legacy_shadow --test authority_recovery
cargo test -p sandbox-config candidate_authoritative
cargo test -p sandbox-runtime-workspace --test authority_route_restart
cargo test -p sandbox-runtime --test candidate_authority
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

From the declared test root, first append the required report intent:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_candidate_authority/test_candidate_authority.py \
  e2e/runtime/layerstack_candidate_authority/test_legacy_read_rollback.py \
  e2e/runtime/layerstack_candidate_authority/test_mixed_root_restart.py \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

Use `E2E_REBUILD_BINARY=0` only after recording matching gateway binary/config identity. A responsive gateway may be reused even with `E2E_REBUILD_BINARY=1`; record actual custody.

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
  --plan layerstack-phase1-tiny-authority-soak \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --plan layerstack-phase1-tiny-authority-soak \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

The benchmark consumes prebuilt binaries.

### DO NOT RUN in Stage 10 — Stage 11 affected regression

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

### DO NOT RUN in Stage 10 — Stage 11 host/image capability matrix

The command below is only the already-pinned Ubuntu cell. Stage 11's image
driver must dispatch it once for every entry in the frozen image manifest:
Ubuntu/Debian glibc, Alpine musl, minimal/distroless, and shell-less, plus
read-only and non-root variants. The manifest records each OCI index and
resolved platform digest and labels every host/image row
`qualified|contract-tested|designed-compatible|unverified` and
`required-release|informational`. Do not run or accept this single command as
the Phase 1 matrix.

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

### DO NOT RUN in Stage 10 — Stage 11 full Phase 1 qualification

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

| Metric | Source/cadence | Aggregation | Stage 10 gate |
| --- | --- | --- | --- |
| authority epoch/mode/write/read | public bounded observation at every boundary | exact sequence | candidate/candidate normal; candidate/legacy only explicit verified epoch |
| publication ID/root/generation/receipt digest | candidate journal/catalog/receipt | exact | one commit; retry byte-identical |
| roots-catalog CAS/conflict count | candidate observation | delta | matches expected successful/conflicting calls |
| fallback/mismatch/integrity counters | public route | pre/post delta | fallback zero; success mismatch zero; injected integrity exact and fail-closed |
| shadow candidate/legacy generation, lag, state, digest | shadow catalog/observation after each phase | exact/max lag | contiguous and Verified/zero lag at quiescence |
| exact candidate/legacy tree+metadata digest | public file/workspace APIs | exact | parity with fixture |
| read-route switch epoch/pending sessions | authority/workspace observation | exact | old or new complete route; terminal pending zero |
| candidate hot-path CAS/pack lookups/payload reads | route counters around command/file/PTY/stdin | delta | zero |
| logical/allocated bytes by root/object/pack/materialization/v1 shadow/staging/trash | outside sampler | boundary/settled | every byte owned; unexplained persistent zero |
| elapsed phase ns | monotonic runner | raw + median only | operation/cell ≤60 seconds; normative gates deferred |
| workers/buffers/queues/permits/leases/transactions/FDs/cache | product gauges, boundaries +100 ms | current/high-water | cap adherence and warmed-idle return ≤5 seconds |
| process/cgroup/container memory | declared source, bounded 100 ms | settled windows + robust slope | coarse noise rule only |
| dependency/environment fingerprint | immutable artifact | equality | zero external delta and complete comparability |

Every run records product/test commit+dirty state, Docker Desktop/Engine, OCI index/platform digest, host/guest architecture, CPU/memory/storage allocation, guest kernel/filesystem/mount/userxattr, Rust/Python, config/mode/authority epoch, cache state, seed/corpus, operation order, memory source, and sampler gaps.

Every result value uses exactly one provenance label: `measured`, `derived`, `estimated`, or `unknown`; only `measured`/`derived` support a gate. Separately named model projections are non-gating source conventions, never result provenance. Artifacts are schema-valid, run-owned, bounded/content-addressed where supported, and tied to exact node IDs. Cleanup uses tracked IDs only.

## 11. Stage exit verdict

The only success label is `stage-10-poc-passed`. It requires all focused Rust/live cases and the tiny soak to pass; one candidate publication authority and idempotent receipt; exact candidate reads with zero fallback; ordered verified zero-lag legacy shadow; explicit generation-fenced read rollback with candidate write authority retained; deterministic mixed-root/restart recovery; Stage 08/09 invariants during soak; native hot-path independence; logical quiescence and acceptable coarse memory evidence; zero unexplained bytes; retained legacy inventory/code/config; valid catalog/artifacts/cleanup; and exact zero external dependency/runtime delta.

Block on duplicate/ambiguous commit, silent fallback, stale rollback read, shadow influencing candidate outcome, parity mismatch, corruption, generation/route ambiguity, live-root/locator loss, depth/cap/grace violation, persistent unexplained bytes, missing gating evidence, suspected leak, artifact mismatch, cross-run cleanup, or any external delta.

Passing does **not** mean default enablement, production qualification,
required-host portability, normative performance/space/RSS, or legacy
retirement. Those decisions require Stage 11 evidence over every applicable
required host and every required Prep 04 image-capability cell; all legacy
paths and rollback code remain through the end of Stage 10. Any unverified
required-release host/image row is a production and retirement no-go.
