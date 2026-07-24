# Stage 01 completion summary and Stage 02 handoff

[Stage 02 specification](spec.md) · [Stage 02 E2E plan](e2e_test.md) · [Stage 01 specification](../stage_01_workspace_scratch/spec.md) · [Phase 1 implementation overview](../index.md)

Prepared: 2026-07-24

Product root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`  
Test root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`  
Documentation root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs`

## 1. Handoff status

Stage 01, **Workspace-scoped execution scratch**, is complete at the POC proof
tier. All 17 Stage 01 completion items are checked, the focused product and
harness gates pass, both packaged E2E cases pass, the tiny benchmark passes,
artifact recovery reports execution available, and the exact external
dependency delta remains zero.

Stage 01 is not a prerequisite for Stage 02. The Stage 02 specification depends
only on Stage 00 and treats Stage 01 as a parallel-world optional layout delta.
Because Stage 01 has now passed, Stage 02 may accept the workspace-scoped
transcript layout as an already-proved checkpoint. Stage 02 must not rerun,
reinterpret, or make this layout part of portable root identity.

This is a working-tree handoff, not a commit handoff. No commit, push, branch
switch, stash, reset, discard, or unrelated cleanup was performed.

## 2. Repository custody

| Repository | Required/current branch | HEAD and upstream | Handoff state |
| --- | --- | --- | --- |
| Product | `upgrade-2.0-phase-1` | `3a450d052b68daf45588328f723e50662808d266`; upstream `origin/upgrade-2.0-phase-1` at the same revision | Dirty Stage 00 plus Stage 01 implementation; tracked and untracked files are intentional. |
| Test | `upgrade-2.0-phase-1` | `100d11c8f00b9774cbb7b509212d11742ae48bf5`; upstream `origin/upgrade-2.0-phase-1` at the same revision | Dirty Stage 00 plus Stage 01 harness/evidence; tracked and untracked files are intentional. |
| Documentation | `layerstack_2_0` | `537938fe7c10a7607c408d2487199ac08a6dba44`; upstream `origin/layerstack_2_0` at the same revision | Existing Phase 1 planning edits, completed Stage 01 checklist, and this handoff document. |

The immutable Stage 00 comparison bases remain product
`7e8f4562f9079f27dcb5b514f6e4546b87e5aa04` and test
`d594f0c72083c39f95334fac685399bca20193f0` as recorded in the Stage 00
evidence. Use the immutable baseline artifacts, not revision names alone, when
constructing a comparator.

The current product and test HEADs do **not** contain the dirty Stage 01
implementation. Do not infer the handoff from `git log`, reset either
repository to HEAD, or overwrite untracked files. Before Stage 02 edits:

1. record all three HEADs, upstreams, and complete `git status --short`;
2. reconcile the Stage 02 clean-scoped-worktree entry requirement with this
   owner-preserved dirty handoff;
3. obtain explicit authorization before committing, stashing, switching,
   resetting, or moving any Stage 01 change; and
4. if work proceeds directly on the dirty tree, record that custody decision
   and isolate every Stage 02 diff from the preserved Stage 00/01 diff.

## 3. What Stage 01 changed

### Product behavior

- Added one validated workspace scratch locator. It alone composes
  `/eos/workspace/<session>/executions/<execution>/transcript.log`, validates
  canonical IDs and containment, rejects separators, dot segments, NUL,
  symlink parents, and out-of-root paths, and creates owner-only directories
  and transcripts.
- Moved all new command transcript writes under the owning workspace session.
  `/eos/namespace_execution` is compatibility residue only; Stage 01 creates no
  new global transcript entry.
- Added move-only execution leases and zero-owner proof. Command teardown
  closes/join resources, evicts terminal ownership, releases the lease, removes
  the exact execution leaf, and only then permits recursive session deletion.
- Bounded terminal draining and terminal retention so no detached task, strong
  ownership cycle, or live-owner session deletion remains.
- Preserved bounded recovery state when an owner join deadline cannot prove
  zero ownership; retry/restart cleanup is idempotent.
- Added a restart-safe legacy reaper bounded to 1,024 entries, depth 3, and the
  declared minimum age. It deletes only eligible old, safe residue and
  preserves active, recent, foreign, malformed, ambiguous, and symlink entries.
- Added bounded structured route, ownership, teardown, reaper, disk, process,
  and cgroup evidence without raw-path or unbounded-label telemetry.
- Added a hidden same-revision legacy route adapter solely for the benchmark
  control. It is not a public runtime default or an alternate production
  authority.

### Preserved behavior

- `/workspace` projection and public command/CLI output are unchanged.
- LayerStack v1, `manifest.json`, `root_hash`, native OverlayFS execution,
  limits, `manager.json`, and `.export` remain authoritative and compatible.
- No `/eos/attempts`, transcript CAS path, v2 root, CAS object, pack, index,
  materialization, publication, GC, or later-stage durable format was added.
- No Cargo, Python, system, service, runtime, target-image, or helper dependency
  was added.

### Principal new files

Product:

- `crates/sandbox-runtime/workspace/src/scratch.rs`
- `crates/sandbox-runtime/workspace/tests/execution_scratch.rs`
- `crates/sandbox-runtime/operation/src/command/terminal_cache.rs`
- `crates/sandbox-runtime/operation/src/workspace_scratch_compat.rs`
- `crates/sandbox-runtime/operation/tests/workspace_execution_scratch.rs`

Test:

- `benchmark/backend/benchmark_lab/workspace_scratch.py`
- `benchmark/backend/tests/unit/test_workspace_scratch.py`
- `benchmark/presets/workspace-scratch-tiny.yml`
- `benchmark/tests/fixtures/golden/layerstack_phase1/workspace_scratch_v1.json`
- `e2e/runtime/workspace_session/test_execution_scratch.py`
- `e2e/tools/verify_external_dependency_delta.py`
- `e2e/tools/test_verify_external_dependency_delta.py`

The complete file inventory remains visible in the product and test worktree
status. Do not use this short list as a substitute for that inventory.

## 4. Stage 01 validation and evidence

### Product checks

The following passed on the final product revision:

- `cargo fmt --all -- --check`;
- exact all-target/all-feature clippy;
- workspace scratch locator: 6/6;
- runtime workspace containment: 2/2;
- compatibility reaper: 4/4;
- command teardown: 3/3;
- affected command/terminal registry: 14/14;
- namespace execution: 69/69;
- workspace destroy/recovery: 15/15;
- daemon observability: 30/30 plus the final focused route checks;
- hidden legacy adapter: 1/1;
- service graph: 8/8; and
- focused configuration, query, CLI, catalog, and registry checks.

The fresh packaged binary identities are:

- gateway:
  `sha256:115763ec9678e4de72107bfafd78911cc6a0a77f1f8e32c697bcb7b7749966e6`;
- catalog exporter:
  `sha256:fb34313543ac3d4ab37a4b0e91bb361e7662c6dfc79bb2782502ed275cda8d88`;
- Linux arm64 daemon:
  `sha256:6647444a82fb61369300479cc834da213bfd2ad6697005bf7c88a54510305390`.

### Packaged E2E

Both declared cases passed with run-owned cleanup:

| Stable ID | Evidence | Result |
| --- | --- | --- |
| `phase1.stage01.workspace-scratch.lifecycle` | `.e2e-state/reports/workspace-session/workspace-session-20260724-202348/phase1.stage01.workspace-scratch.lifecycle/verdict.json`; `sha256:76e29502f281c42282769cb918bd2ba60f4cf4128a07f6c60d079f45c7262d74` | PASS, 1/1, 9.73 s |
| `phase1.stage01.workspace-scratch.restart-reap` | `.e2e-state/reports/workspace-session/workspace-session-20260724-202453/phase1.stage01.workspace-scratch.restart-reap/verdict.json`; `sha256:96c0a717b43d41b7a86d802ba913f9c39b1c62efff35197b0f421921f47dc772` | PASS, 1/1, 12.80 s |

The pinned target is Ubuntu 24.04 manifest
`ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`.
The owner-approved immutable Linux arm64 descriptor is
`sha256:7f622ca8766bccb22f04242ecb6f19f770b2f08827dc4b8c707de5e78a6da7ab`.

### Tiny benchmark

Normal runner qualification passed as run
`019f9430-f031-748b-a29a-42f9542c1ac8`:

- seed `0x5A01` (`23041`);
- two warm-up pairs;
- six alternating measured pairs;
- twelve measured lifecycles;
- one candidate cancellation;
- whole-run time `8,983,323,208` ns, below 60 seconds;
- legacy-control no-op median `23,663,458` ns;
- workspace-candidate no-op median `23,276,500` ns;
- candidate/control latency ratio `0.98364744`;
- throughput ratio `1.0166244`;
- all correctness, route, disk, logical quiescence, memory cap, process/cgroup
  trend, deadline, artifact, and cleanup gates passed; and
- no unsupported p95 or Stage 11 normative claim was made.

Primary artifacts under the test repository:

- `.benchmark-state/results/019f9430-f031-748b-a29a-42f9542c1ac8/summary.json`
  (`sha256:00aadf1c160089ae8eb5a08f76f07e57a31114e00032d643a6a3cb474ba2476c`);
- `.benchmark-state/results/019f9430-f031-748b-a29a-42f9542c1ac8/report.json`
  (`sha256:cc8f0a7d63ac5544769fb697316919b5f1cf63e581b0fb95dc63950b12913e2e`);
- `.benchmark-state/results/019f9430-f031-748b-a29a-42f9542c1ac8/export.json`
  (`sha256:4cd37f77c3b014d6d20331c0deb410b501d941ca3dc0af22709e33d2ec02362c`);
  and
- bounded operation evidence
  `operation-evidence-f5044dc7cdac1b94315b786b5d91b1ddb74789b412a007c54ca399473b21bc2d.json`.

Recovery then returned:

```json
{
  "execution_available": true,
  "issues": [],
  "recovered_run_ids": [],
  "schema_version": 1
}
```

### Final offline closure

- Complete benchmark backend suite: 168/168 passed.
- External-dependency drift suite: 8/8 passed.
- Exact dependency comparison: 16 invocations, 1,143 external packages,
  2,179 external feature pairs, 116 direct external edges, zero differences.
- Dependency artifact:
  `.e2e-state/evidence/stage01-offline/dependency-delta.json`,
  `sha256:3995bdabcc6f732883ee831189e690a60faa0cf58fe9e2a0be95870278a2b945`.
- Focused E2E collection is warning-free and finds exactly the two declared
  Stage 01 cases.
- Side-effect-guarded focused catalog contains exactly those two cases and has
  identical before/after product and E2E source digests.
- `git diff --check` passes in product, test, and documentation repositories.
- No `.workspace-evidence.json` residue or benchmark runtime directory remains.

The authoritative append-only execution record is
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`.
Its final entries explicitly clarify earlier physical insertion order and the
correct `report.json`/`export.json` paths. Never reorder, truncate, or rewrite
that history.

## 5. Known history and cautions

- A broad macOS LayerStack autosquash run has three unrelated pre-existing
  failures. Stage 01 did not rerun it after focused evidence passed. Stage 02
  touches LayerStack, so establish the documented Stage 02 focused baseline
  and distinguish those known failures from new regressions.
- The complete benchmark suite initially exposed a stale API assertion that
  expected eight catalog operations. Stage 01 deliberately adds the ninth
  `workspace_scratch` benchmark operation; the corrected suite passes 168/168.
  Stage 02 catalog additions must update exact-count contracts deliberately.
- The benchmark report contains failed diagnostic attempts as immutable
  evidence. Only run `019f9430-f031-748b-a29a-42f9542c1ac8` is the final
  Stage 01 tiny qualification.
- The Stage 01 E2E sandboxes were destroyed exactly once. Do not use broad
  Docker cleanup or prune when preparing Stage 02.
- Stage 00 evidence is frozen and referenced. Do not rerun a passing live
  Stage 00/01 suite merely to recreate evidence.

## 6. Stage 02 overlap map

Stage 02 should be additive, but these existing dirty seams require special
care:

| Stage 02 area | Preserved Stage 01 state to keep |
| --- | --- |
| LayerStack crate | `stack/ops/publish.rs` and `storage/whiteout.rs` already have dirty handoff edits. Inspect and merge; do not replace the files from HEAD. |
| Runtime workspace/operation | Workspace scratch locator, execution leases, terminal ownership, and session teardown ordering are complete. Portable root values must not import or own them. |
| Operation catalog | Preserve the internal Stage 01 legacy-control adapter and the public/hidden partition. Add Stage 02 feature-off evidence without exposing benchmark-only operations publicly. |
| Daemon observability | Preserve bounded Stage 01 route/ownership/reaper fields. Stage 02 candidate gauges must be additive, closed, bounded, and zero while dormant. |
| Benchmark definitions | The definition catalog has nine operations and a passing exact-count API contract. Stage 02 planning must extend the catalog and update all strict fixtures coherently. |
| E2E catalog | Preserve the two Stage 01 declarations and their marker registration. Stage 02 adds its own declaration; it must not rename or absorb Stage 01 cases. |
| Dependency comparator | Reuse the standard-library exact comparator and immutable Stage 00 baseline. Stage 02 requires zero external package, feature, and direct-edge delta. |
| `/eos` outside tree | Accept the completed Stage 01 `workspace/<session>/executions` delta as pre-existing. Stage 02 must create none of the forbidden v2 storage paths. |

Stage 02's new `sandbox-runtime-layerstack-core` crate remains std-only and
must not depend on workspace scratch, operation, daemon, catalog, OverlayFS,
Docker, serde, or a concrete SHA implementation. The existing LayerStack crate
retains hashing, serde, persistence, and provider adapters.

## 7. Recommended Stage 02 start sequence

1. Read `spec.md` and `e2e_test.md` in full and treat them as authority.
2. Record immutable product/test/doc HEADs, upstreams, full status, and this
   dirty handoff before any edit.
3. Resolve scoped-worktree custody without committing, stashing, switching,
   resetting, or discarding unless the owner explicitly authorizes it.
4. Confirm Stage 00 focused evidence is intact and record that Stage 01's own
   exit passed. Do not make Stage 01 a Stage 02 prerequisite.
5. Confirm no unexpected `/eos` artifact and no forbidden v2 path exists.
6. Reuse the frozen dependency comparator; capture two agreeing Stage 02 entry
   snapshots before adding the internal crate.
7. Add only the std-only core crate and internal workspace edge first. Prove
   the core dependency table is empty before implementing adapters.
8. Implement canonical values, codec, raw Linux path bytes, closed
   capabilities, root/tree records, and narrow ports with exact goldens and
   fail-closed tests.
9. Keep concrete SHA-256, serde, filesystem, publication, and provider behavior
   in existing LayerStack. Do not write any v2 durable artifact.
10. Before every live Docker, E2E, benchmark, or recovery command, append the
    exact intent and custody boundary to `e2e/test-report.md`.
11. Run focused proof before broader suites, use run-owned cleanup only, and do
    not rerun passing live Stage 00/01 cases without a new-revision rationale.
12. On Stage 02 completion, update every Stage 02 completion checklist item and
    append the final evidence/cleanup verdict.

## 8. Stage 02 invariant summary

Stage 02 succeeds only if it produces deterministic, host-independent,
versioned portable root values and exact goldens while changing no system
behavior. Legacy v1 remains the sole read, write, and publication authority;
Stage 01 remains the sole owner of workspace-scoped transcript placement; the
new core has no external dependency; no v2 artifact appears under `/eos`; and
rollback is deletion of the internal crate/edge and its tests only.
