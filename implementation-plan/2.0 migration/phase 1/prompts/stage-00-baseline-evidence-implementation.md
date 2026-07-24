# Phase 1 Stage 00 — baseline evidence implementation prompt

Use this prompt in a new Codex task to implement and prove
`stage_00_baseline_evidence`. This is an implementation task, not another
planning pass.

## Mission

Implement Stage 00 completely across the product and external test
repositories:

- freeze the current LayerStack v1 behavior and deterministic golden evidence;
- add a legacy-only rollout selector;
- extend the existing authenticated observability surface with bounded,
  structured storage-route and owned-resource evidence;
- add focused Rust, packaged E2E, restart/recovery, tiny benchmark, and
  same-process reclamation proofs;
- capture reproducible environment and exact dependency baselines for later
  Phase 1 comparisons; and
- stop only when the Stage 00 exit gate is proved or a concrete blocking
  defect is documented with evidence.

Product root:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`

branch: upgrade-2.0-phase-1

Test root:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`

branch: upgrade-2.0-phase-1

Planning root:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1`

Do not implement any later stage.

## Approved repository policy and frozen entry

This task resolves the earlier fresh-branch conflict in favor of the product
repository's local instructions:

- work in the existing product checkout directly on `main`;
- do not create a side branch or another worktree;
- the approved immutable product base is
  `7e8f4562f9079f27dcb5b514f6e4546b87e5aa04`;
- the expected product preflight is clean `main`, synchronized with
  `origin/main`, with one worktree;
- use the existing test checkout on
  `agent/retire-multi-agent-demo` at
  `d594f0c72083c39f95334fac685399bca20193f0`, clean and two commits ahead of
  its upstream;
- do not create or switch branches or worktrees in the test repository; and
- the Codex task executing this prompt is the responsible implementer.

Before editing, verify branch, exact `HEAD`, upstream state, worktrees, and
`git status --short` in both repositories. If either exact base or required
branch differs, if either repository has unexpected changes, or if another
checkout now owns product `main`, do not rebase, pull, reset, switch, stash, or
overwrite anything. Report the mismatch and stop for an updated immutable-base
decision.

Preserve all user and concurrent-agent changes. Never revert unrelated work.

## Authority order

When evidence conflicts, apply this order:

1. this prompt and the current user's instructions;
2. repository-local `AGENTS.md`, `CLAUDE.md`, and applicable maintainer rules;
3. the Phase 1 implementation overview and Stage 00 specification/E2E plan;
4. preparations 03 and 04, with preparation 04 controlling quantitative
   acceptance;
5. current product and test source behavior; and
6. secondary prose.

Do not silently reconcile a contradiction. State the competing requirements,
which authority controls, and the concrete implementation consequence.

## Read and inspect before editing

Read these files completely:

- `ephemeral-sandbox/AGENTS.md`
- `ephemeral-sandbox/CLAUDE.md`
- `ephemeral-sandbox/docs/maintainer-architecture.md`
- `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/index.md`
- `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_00_baseline_evidence/spec.md`
- `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_00_baseline_evidence/e2e_test.md`
- `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prep/03-seqcdc-cas-and-squash-decision.md`
- `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md`

Then inspect the current implementations and callers rather than trusting the
planned paths blindly. At minimum, trace:

- `LayerstackConfig` parsing, validation, defaults, and production/benchmark
  YAML;
- v1 `Manifest`, `manifest_root_hash`, physical `LayerRef` identity, native
  layer write, publication staging/fsync/rename/OCC/manifest commit, boot
  cleanup, leases, substitutions, projection, export, and squash;
- existing LayerStack, operation, ownership, namespace-worker, and
  observability snapshots and CLI JSON compatibility;
- workspace public create/write/publish/read/execute/destroy and
  restart/recovery flows;
- current failpoint facilities around publication visibility boundaries;
- LayerStack integration-test conventions and the existing
  `occ_merge_bench.rs` modeled-result vocabulary;
- E2E typed declarations, gateway and run-resource custody, append-only
  reporting, workspace publication cases, and resource-efficiency cases;
- benchmark runner, models, public observability parser, sampling, schemas,
  presets, and immutable/run-owned artifact conventions; and
- CI, packaging, target configuration, and feature invocations that define
  the actual supported dependency-baseline inventory.

Reuse existing abstractions. If a planned filename or symbol no longer matches
the source, preserve the planned responsibility in the current owner instead
of creating a duplicate layer.

## Hard scope boundary

Stage 00 may add only:

- a closed `StorageRolloutMode` admitting `legacy` only, defaulting compatibly
  to `legacy`, and rejecting unknown values;
- explicit `rollout_mode: legacy` in production and benchmark configuration;
- bounded value snapshots and additive observation fields for route,
  authority, fallback/mismatch/shadow counters, owned-resource
  current/high-water gauges, observation epoch, and quiescence;
- compatibility-preserving public observability projection fields;
- v1 golden fixtures and failure/recovery expectations;
- external E2E fixtures, schema, typed cases, benchmark parsing/model fields,
  and a tiny baseline preset; and
- run-owned dependency, environment, route, resource, disk, timing, and
  cleanup evidence.

Stage 00 must not add or change:

- `RootId` v2, SeqCDC, CAS objects, candidate reads/writes, shadow ingest,
  materialization, retention, packing, GC, migration, squash identity, or
  candidate rollout variants;
- any durable product format or path under `/eos`;
- current v1 manifest bytes, physical identity, publication authority,
  command/file/PTY/stdin behavior, workspace semantics, or native OverlayFS
  hot path;
- a diagnostic daemon, test-only production API, second E2E scheduler, second
  benchmark runner, or unbounded log scraping;
- a product crate or external Rust/Python/npm/system/image/runtime dependency,
  feature activation, service, helper, download, privilege, or target-image
  requirement; or
- broad regression, full host/image qualification, normative percentile,
  full scale/RSS/space campaigns, or a production-go claim. Stage 11 owns
  those.

No field may be labeled by a user path, object ID, chunk ID, or unbounded error
text. Use closed enums, fixed arrays, scalars, and existing capped lists.
Missing optional OS measurements are explicit `None`/`unknown`, never zero.
Counters saturate rather than wrap. Snapshots copy bounded values and retain no
new strong ownership edges.

Keep tests out of production `src/`. Follow the repository's no-inline-comment
rule in production code and its SRP/component-boundary law. Add no background
worker merely to observe existing work.

## Required implementation

### 1. Freeze the entry evidence

Before source changes:

1. record exact product/test commits, branches, dirty state, upstreams, and
   worktrees;
2. discover and record the canonical supported target/feature invocations from
   current CI/build/release source; do not invent or silently narrow them;
3. capture canonical locked dependency records for every frozen invocation:
   exact external `(source,name,version,checksum)` identities, enabled external
   `(package,feature)` pairs, and product-wide direct external manifest-edge
   multiset;
4. hash workspace manifests, `Cargo.lock`, Python/npm manifests and locks;
5. inventory licenses/notices, product-route processes, sockets, services,
   commands, runtime downloads, image packages, and target-image helpers; and
6. record host, Docker/Desktop/Engine, toolchains, image index/platform
   digests, architecture, CPU/memory/storage allocation, guest kernel,
   filesystem/mount/userxattr, config, cache class, and measurement scope.

Use canonical sorted records, not the planning-time counts. Counts are only
sanity checks.

Recheck the pinned Ubuntu OCI index and arm64 platform digest from raw
metadata. A mismatch is an artifact-validation failure; do not silently
resolve the tag to a new fixture.

If the repository does not define an unambiguous supported target/feature
inventory after inspecting CI, packaging, and release source, identify the
exact missing owner decision. Continue safe implementation work, but do not
claim Stage 00 exit until that inventory is approved and captured.

### 2. Add legacy-only configuration

Implement the smallest typed rollout configuration in `sandbox-config`:

- closed snake-case enum with only `legacy`;
- absent value remains backward compatible and resolves to `legacy`;
- unknown values fail validation;
- production and benchmark YAML state `rollout_mode: legacy`; and
- focused tests cover default, explicit legacy, and rejected unknown values.

Do not predeclare later variants.

### 3. Add bounded operational observations

Refactor existing observation construction only where needed, preserving old
behavior and response compatibility. Add bounded route/resource value
snapshots in the correct LayerStack owner and map them through the existing
operation and observability CLI seams.

The structured evidence must make it possible to prove:

- configured mode is legacy;
- read and write authority are `legacy_v1`;
- fallback, mismatch, and shadow-comparison deltas are zero;
- route/resource schema version and observation epoch are present;
- active operations, publications, transactions, staging owners, leases,
  buffers, tasks, workers, queues, byte permits, mappings, file descriptors,
  caches, registries, and owned bytes are represented by bounded
  current/high-water values where the product actually owns or can observe
  them; and
- logical cleanup and bounded quiescence can be decided without parsing logs.

Do not fabricate gauges for resources the product cannot own or measure.
Represent optional outside measurements as unavailable and use the declared
independent sampler where allowed.

Add focused saturation, high-water, mapping, and CLI schema-compatibility
tests. Observation failure must never mutate storage or convert a product
failure into success.

### 4. Freeze v1 behavior

Add deterministic v1 integration goldens for the corpus required by the
Stage 00 spec, including empty/no-op, one-byte/boundary, regular file,
localized edit, deterministic incompressible content, small files, symlink,
mode/owner, ordered multilayer, and supported hardlink, whiteout/opaque,
sparse, and xattr cases.

Freeze exact current manifest/root bytes and tree/export/content/metadata
digests. Record unsupported or currently lossy behavior explicitly rather
than pretending it round-trips.

Exercise current publication failure boundaries around staging fsync, layer
rename, metadata, OCC reread, and manifest replacement. Prove no partial
active-manifest visibility and owned staging recovery.

If observed current behavior differs from the intended fixture, retain it as a
baseline defect and report it. Do not rewrite an expectation merely to obtain
a green run.

### 5. Add external focused proofs

In the external test repository, add:

- `e2e/runtime/layerstack_baseline/test_baseline_route.py`
- `e2e/runtime/layerstack_baseline/SPEC.md`
- versioned v1 corpus/tree/root fixtures under
  `e2e/fixtures/layerstack_phase1/v1/`
- `e2e/schemas/layerstack_phase1/evidence-v1.schema.json`
- typed cases
  `layerstack.phase1.baseline.legacy-route` and
  `layerstack.phase1.baseline.restart-cleanup`
- bounded runtime evidence using the existing harness and public manager,
  runtime, and observability CLIs; and
- run-owned LIFO cleanup only.

The primary case must perform packaged public
create/write/publish/read/execute/destroy and assert exact legacy content,
route authority, zero fallback/mismatch/shadow, and cleanup. The restart case
must inject one allowed pre-visibility failure, recover through existing
gateway custody, retry, and prove no partial manifest or staging residue.

Outside `/eos` inspection may record allocated bytes, permissions, and
residue. It may not replace public correctness, route, or logical-cleanup
assertions, and `/eos` must never be exposed to the workload.

### 6. Add the tiny baseline and reclamation sentinel

Extend the existing benchmark models and observability parser without adding
a scheduler or dependency. Add
`benchmark/presets/layerstack-phase1-tiny-baseline.yml`.

Use a deterministic seed and pre-generated corpus:

- empty/no-op;
- 1 KiB localized edit in a 1 MiB deterministic file;
- 1 MiB deterministic incompressible file;
- 256 small files totaling about 1 MiB; and
- repeated overwrites at history depths 1, 8, and 32.

Run one warmup and at least five measured raw legacy/control pairs. Prefer
three warmups and ten alternating repetitions only if each cell remains below
60 seconds and the aggregate developer loop remains in the planned 30–60
second range. Store all raw samples. Report absolute values and ratios, but do
not make a p95 or normative regression claim from this small sample.

In one daemon without restart, run three warmups followed by 20 cycles:

```text
idle
  -> create/write/publish/read/execute peak
  -> cancellation or injected-failure peak
  -> explicit destroy
  -> poll quiescence every 100 ms for at most 5 seconds
  -> settled sample
```

Require attributable logical owners to return to declared idle, queues and
permits to drain, workers to return to configured idle, sessions/executions to
disappear, and registries to remain within their configured cap. Do not use an
arbitrary sleep, daemon restart, allocator trim, cache purge, or global
cleanup.

Record first/last five-cycle settled medians, delta, a benchmark-standard
robust slope, sample count, and the predeclared raw-control noise band.
Verdicts are limited to:

- `bounded-and-released`
- `bounded-retained-by-design`
- `allocator-or-page-cache-retained`
- `suspected-leak`
- `confirmed-leak`
- `measurement-unavailable`

Suspected/confirmed leak or unavailable stage-gating data blocks exit.

### 7. Prove exact zero dependency delta

After implementation and before declaring success, regenerate every canonical
dependency/environment record independently and compare it with the entry
record.

Pass only when all are exactly equal:

- external packages, versions, sources, and checksums;
- enabled external feature pairs;
- direct external manifest-edge multiset;
- `Cargo.lock` and manifest bytes, except the planned source/config files that
  do not change dependency declarations;
- Python/npm lock and manifest dependency content;
- licenses/notices;
- system tools, image packages, processes, sockets, services, runtime
  downloads, and target-image helpers.

Stage 00 adds no crate or internal dependency edge either. Any unexpected
delta is a blocker.

## Live-test custody

Before every live E2E command, append an intent entry to
`ephemeral-sandbox-test/e2e/test-report.md` containing:

- exact product/test commits and dirty states;
- command, case/node, timeout, image index/platform digest, binary/config
  identity, and expected evidence;
- gateway/sandbox/run ownership and cleanup scope; and
- the reason for rebuild or proven reuse.

Immediately afterward, append Good/Defect/Fix, artifact IDs, measured gaps, and
tracked cleanup evidence. Never erase a failed attempt. Never perform a global
Docker prune or delete resources not owned by the run.

The first packaged gate after product changes must use the repository's normal
gateway rebuild path and `E2E_REBUILD_BINARY=1`. An already-responsive gateway
may still be reused by the harness; record actual custody and binary/config
identity instead of claiming a rebuild that did not happen. Use
`E2E_REBUILD_BINARY=0` only for an unchanged, identity-proven focused rerun.

Rerun only a failing focused case after a documented fix. Do not automatically
expand to a broad suite.

## Required validation

Run formatting and focused product tests from the product root:

```bash
cargo fmt --all
cargo fmt --all -- --check
cargo test -p sandbox-config runtime
cargo test -p sandbox-runtime-layerstack --test baseline_v1_golden --test resource_observation
cargo test -p sandbox-runtime-operation --test storage_route_observation
cargo test -p sandbox-cli observability
cargo metadata --locked --all-features --format-version 1
```

Adapt only test target names that current source proves are different; do not
weaken the test coverage.

Validate the E2E catalog:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
PYTHONPATH=e2e .venv/bin/python -m harness.catalog.collect \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

After appending the required intent entry, run the focused packaged cases:

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

Validate and run the tiny benchmark with the existing prebuilt-binary runner:

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

The benchmark does not rebuild binaries. Prove the binary identity before
using its results.

Do not run the full affected regression, full image/release matrix, cold
27-point RSS matrix, full physical-history campaigns, soak, or Phase 1 final
qualification.

## Stage 00 exit gate

Do not declare Stage 00 complete unless all of the following are true:

- branch/base preflight matches the approved entry;
- focused config, observation, v1 golden, failpoint, and CLI tests pass;
- packaged success and restart/cleanup cases pass through public CLIs;
- read/write authority is always `legacy_v1`, and fallback, mismatch, and
  shadow deltas are zero;
- exact content/tree/metadata fixtures match without silent regeneration;
- success and injected-failure resources quiesce within five seconds with no
  unexpected staging/session/execution residue;
- the 20-cycle same-process sentinel returns logical gauges to idle and stays
  inside the frozen raw physical-noise rule;
- all artifacts validate against the versioned schema and remain under
  run-owned custody;
- independently generated exact dependency/environment snapshots compare
  equal for every supported target/feature invocation;
- no product durable format/path, candidate artifact, branch/worktree,
  external dependency, service, helper, privilege, or target-image
  requirement was added; and
- every Stage 03–11 metric remains explicitly deferred rather than reported as
  passed.

A failing baseline is valid measured evidence but blocks the affected exit
gate. Missing gating data, route ambiguity, silent fallback, corruption,
durability failure, suspected leak, unexpected residue, dependency delta,
schema gap, or cleanup trespass is a blocker, not a warning.

## Final report

Return a concise evidence-backed report containing:

1. outcome: `Stage 00 passed` or `Stage 00 blocked`;
2. exact final Git state of product and test repositories;
3. files changed, grouped by product, E2E, fixtures/schema, and benchmark;
4. focused commands and pass/fail results;
5. route/content/recovery/quiescence evidence and artifact paths/IDs;
6. tiny-loop sample count and non-normative raw summary;
7. 20-cycle logical-release and physical-noise verdict;
8. exact dependency/environment comparison result for each frozen invocation;
9. any retained baseline defect or missing measurement; and
10. confirmation that later-stage work and final qualification were not run.

Do not claim production readiness. Do not proceed to Stage 01 or Stage 02 in
the same task.
