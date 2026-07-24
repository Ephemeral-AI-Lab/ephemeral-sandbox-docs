# Stage 01 implementation prompt — workspace-scoped execution scratch

Use this prompt in a new Codex task rooted at:

`/Users/yifanxu/Ephemeral-AI-Lab`

## Mission

Implement Phase 1 Stage 01, **Workspace-scoped execution scratch, POC tier**, by building on the actual Stage 00 outcome and following the Stage 01 specification and E2E contract.

Move command transcripts from the legacy global layout:

`/eos/namespace_execution/<execution>/transcript.log`

to the workspace-scoped layout:

`/eos/workspace/<session>/executions/<execution>/transcript.log`

Route every new transcript through one validated workspace scratch locator. Preserve the existing `/workspace` contract, public CLI and command behavior, LayerStack v1 authority, `manager.json`, `.export`, and the native OverlayFS hot path.

Complete the implementation, focused tests, packaged Stage 01 E2E definitions, tiny benchmark support, evidence validation, and final qualification that can safely be completed. Do not broaden the work into later Phase 1 stages.

## Repository policy and current baseline

Work only in these repositories:

- Product: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
- Test harness: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`
- Read-only design authority: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs`

The intended product and test branch is:

`upgrade-2.0-phase-1`

At Stage 00 closure, the recorded repository identities are:

- Product HEAD: `3a450d052b68daf45588328f723e50662808d266`
- Test HEAD: `100d11c8f00b9774cbb7b509212d11742ae48bf5`

Both heads contain the committed Stage 00 outcome. The current worktrees also
contain in-progress Stage 01 changes; those changes are part of the handoff and
must be preserved.

Before editing:

1. Read all applicable `AGENTS.md`, `CLAUDE.md`, maintainer, and repository-local instruction files.
2. Record branch, HEAD, upstream, status, and the complete initial diff in both repositories.
3. Verify both repositories are on `upgrade-2.0-phase-1`.
4. Reconcile the dirty files with the Stage 00 evidence described below.
5. Preserve all existing changes. Do not stash, reset, discard, overwrite, commit, push, or switch branches unless the user explicitly authorizes that action.
6. If a pre-existing change conflicts with Stage 01 and its ownership cannot be established from the Stage 00 evidence, stop and ask the user before editing that file.

The existing dirty worktree is not permission to rewrite unrelated user work. Make the smallest compatible Stage 01 diff on top of it.

## Authority order

Resolve ambiguity in this order:

1. The user’s current instructions.
2. Repository-local instructions.
3. Stage 01 specification:
   `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_01_workspace_scratch/spec.md`
4. Stage 01 E2E contract:
   `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_01_workspace_scratch/e2e_test.md`
5. The frozen Stage 00 evidence and verified implementation already present in the worktrees.
6. Current product and harness conventions.

Do not blindly copy proposed filenames or APIs from the specification. Inspect the current callers, ownership model, and test topology, then express the specified invariants using the repository’s existing architecture.

## Required reading before implementation

Read these files completely:

- Stage 01 `spec.md`
- Stage 01 `e2e_test.md`
- The Phase 1 implementation index and the Stage 01 preparation material referenced by the spec
- Stage 00 report:
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`
- Stage 00 dependency/environment comparison:
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/evidence/stage00-post-20260724T155849+0800/stage00-dependency-comparison.json`
- Stage 00 shared dependency verifier:
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/tools/verify_external_dependency_delta.py`
- Stage 00 owner-approved closure comparison:
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/evidence/stage00-closure-20260724T191140+0800/dependency-delta-e2e-tool.json`
- Stage 00 post-baseline evidence in:
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/evidence/stage00-post-20260724T155849+0800/`
- Stage 00 final benchmark artifacts in:
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.benchmark-state/results/019f9320-08ea-7d6f-9f8e-f086d972a927/`

Use the Stage 00 report’s final evidence entries, including Iterations 54 and 55, rather than rerunning already-passing Stage 00 suites.

Inspect the current implementation and every relevant caller before choosing the patch shape, especially:

- runtime config defaults and YAML configuration
- workspace manager creation, admission, recovery, destroy, and `manager.json`
- workspace session root ownership and lifecycle
- operation command execution, `CommandExecValue`, teardown, cancellation, and join handling
- namespace execution engine transcript-path plumbing
- existing recovery artifacts and terminal eviction behavior
- product observation/query/daemon/CLI path added in Stage 00
- existing workspace-session E2E helpers and cases
- benchmark catalog, strict schemas/models, scheduler, artifact recovery, and Stage 00 resource sampling

Use `rg` to find the real definitions and callers. Do not assume the planning document’s proposed paths exactly match the current tree.

## Stage 00 handoff that Stage 01 must preserve

The Stage 00 functional baseline is green:

- explicit legacy rollout configuration is present across the five configured YAML profiles
- bounded route and resource observation reaches the product query, daemon, and CLI surfaces
- v1 goldens, failpoints, operation catalog, and resource-lifecycle checks passed
- focused Rust, configuration, query, CLI, and catalog tests passed
- focused external E2E catalog nodes passed
- live packaged Stage 00 cases passed `2/2` in `53.20s`, with successful cleanup
- the final tiny benchmark run passed all six checks in `78.22s`
- that run recorded `1109` timed public requests and `7294` resource observations
- logical resource release completed
- final fixed bookkeeping was `176` bytes with zero active resources
- the physical-memory verdict was `allocator-or-page-cache-retained`, which was explicitly non-blocking
- exact dependency delta was zero across all 16 frozen invocations
- semantic environment inventory delta was zero

The exact Stage 00 comparison evidence included:

- `1143` external package records
- `2179` feature pairs
- `116` direct dependency edges
- comparison SHA-256:
  `5f00ed4ce892f2bb7069f0f9c084dbe5e224a393ea6992275dab08187896d503`
- post-baseline SHA-256:
  `f5cd3c8eb4f06b7360302c6d12b26632197a04de88c8ad3c3ac3181fb4f0f511`

Reuse and extend these Stage 00 observation, schema, catalog, and benchmark mechanisms. Do not create a competing observer, scheduler, resource model, report format, or dependency comparator.

Stage 00’s run-owned staged binaries were identity-checked and removed. Stage 01 must build and stage fresh binaries through the repository’s normal path before the first packaged gate. Never treat a stale or missing `bin/sandbox-gateway` or `bin/sandbox-catalog-export` as valid.

## Stage 00 closure decisions

Stage 00’s former Ubuntu arm64 image-fixture blocker is resolved by the
owner-approved closure recorded in test-report Iteration 56:

- pinned index:
  `sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`
- corrected arm64 descriptor from that immutable raw index:
  `sha256:7f622ca8766bccb22f04242ecb6f19f770b2f08827dc4b8c707de5e78a6da7ab`
- historical transcribed value retained only in the immutable entry/post
  evidence:
  `sha256:7f622ca8766bccb22f04242ecb6f19f770b2f08827d7c5425fb57681140e6efb`

The correction changes no tag, index, image, or historical artifact and makes
no host-qualification claim. Stage 01 packaged gates must use the pinned index,
record the resolved platform descriptor, and preserve the Iteration 56
provenance.

The Stage 00 tiny run’s measured duration remains 78.22 seconds. The owner
waived only its 30–60 second duration requirement; all correctness, route,
quiescence, logical-release, custody, and dependency evidence remains gating.
Do not rerun or optimize Stage 00 merely to change that duration.

## Hard scope

Implement only Stage 01:

- one workspace scratch locator and validated path model
- session admission plumbing
- owner-only directory and transcript creation
- workspace-scoped command transcript routing
- explicit command terminal eviction and release proof
- command teardown ordering
- restart-safe bounded legacy scratch reaping
- legacy configuration deprecation/compatibility
- bounded structured route and resource evidence
- focused product tests
- the two packaged Stage 01 E2E cases
- the Stage 01 tiny benchmark preset and validation
- exact dependency/environment proof against Stage 00

Do not introduce:

- `/eos/attempts`
- transcript payloads in LayerStack or CAS
- a new RootId, CDC, object, publication, materialization, pack, GC, squash, or candidate model
- a public API or CLI behavior change
- a second workspace authority
- a second lifecycle scheduler
- an unbounded metrics label, map, scan, retry loop, queue, or evidence stream
- a new external package, crate, feature edge, Python dependency, system helper, runtime helper, or image helper
- a broad regression run, host matrix, or final Phase 1 qualification; those belong to Stage 07

Keep LayerStack v1 as the sole persistence authority.

## Required product implementation

### 1. Workspace scratch locator

Add one validated locator seam equivalent to the specification’s:

- `WorkspaceScratchLocator`
- `WorkspaceSessionScratch`
- `ExecutionScratchLease`

The exact names may follow repository conventions, but there must be one authority for deriving and validating:

- the session scratch root
- the `executions` root
- the per-execution leaf
- the transcript path

Never reconstruct these paths independently in operation or namespace code.

Validation must reject:

- path separators
- `.` and `..`
- NUL
- non-canonical identifier spellings
- symlink parents
- any path that can escape the configured workspace root

Use canonical session and execution identifiers. Create directories and transcript files owner-only, including mode `0700` for directories and an owner-only transcript mode. Validate modes in focused tests and packaged evidence.

Lease cleanup must be explicit, idempotent, and safe if terminal cleanup is retried.

### 2. Admission and command routing

Resolve the session scratch locator during workspace admission and carry the resolved capability through the current command-execution path.

For every newly admitted command:

1. derive the execution leaf from the admitted workspace session
2. create the leaf through the locator
3. pass the resolved transcript path into the namespace execution engine
4. write no new transcript beneath `/eos/namespace_execution`

The namespace runner may accept a resolved transcript path, but it must not regain authority to select a root.

Preserve public command output, streaming, cancellation, exit status, error behavior, and the existing `/workspace` contract.

### 3. Terminal eviction and teardown proof

Implement the Stage 01 ownership order:

1. command reaches a terminal state
2. command resources are closed
3. terminal command state is evicted from active ownership
4. transcript descriptors and execution scratch leases are released
5. the per-execution leaf is deleted
6. workspace teardown receives a zero-owner release proof
7. the workspace session root is unmounted and deleted

Represent the zero-owner transition with a move-only proof equivalent to `WorkspaceCommandReleaseProof`. Do not encode this invariant only as a comment, boolean convention, or best-effort `Drop`.

Keep cleanup idempotent. Respect the existing command join deadline—currently one second—unless direct evidence demonstrates that Stage 01 requires a different value. If the deadline expires:

- do not delete storage still owned by a live command
- preserve or create the repository’s normal recovery artifact
- expose the bounded cleanup state
- allow restart recovery to finish safely

Add focused tests for normal completion, cancellation, repeated cleanup, teardown ordering, and deadline/recovery behavior.

### 4. Bounded legacy compatibility and reaper

Keep the namespace scratch-root configuration only as deprecated compatibility input. New commands must not write there.

Add a restart-safe, bounded legacy reaper equivalent to `LegacyExecutionScratchReaper`:

- maximum `1024` entries per bounded pass
- maximum traversal depth `3`
- minimum age guard
- weak active-execution ownership input
- no symlink following
- no deletion of active, recent, foreign, ambiguous, malformed, or unsafe entries
- no new writes beneath the legacy global root

Record scanned, deleted, skipped-active, and skipped-unsafe counts through bounded evidence.

Tests must cover old residue deletion, active residue preservation, recent residue preservation, symlink refusal, malformed/foreign entry refusal, and bounded-pass behavior.

### 5. Structured evidence

Extend the existing Stage 00 observation surface. At minimum, expose bounded equivalents of:

- `scratch_layout_version`
- bounded or hashed session and execution identity
- `scratch_route = workspace_scoped | legacy_compat`
- active execution scratch leases
- retained terminal records
- open transcript descriptors
- live and high-water scratch bytes
- teardown join count
- teardown deadline count
- legacy entries scanned
- legacy entries deleted
- legacy entries skipped active
- legacy entries skipped unsafe
- cleanup state
- quiescence state

Do not place raw unbounded identifiers into metric labels. Prefer fixed enums, counters, gauges, bounded snapshots, and existing hashed/bounded identity conventions.

Correctness must be asserted through public CLI/product evidence. Host inspection outside `/eos` is allowed only for placement, permissions, residue, and disk-use evidence.

## Required external E2E implementation

Extend the existing harness and catalog with these stable Stage 01 IDs:

- `phase1.stage01.workspace-scratch.lifecycle`
- `phase1.stage01.workspace-scratch.restart-reap`
- `phase1.stage01.workspace-scratch.tiny`

Do not duplicate existing Stage 00 packaging, artifact, cleanup, observation, or catalog logic.

### Lifecycle case

The packaged lifecycle case must prove:

- a command transcript is created under the admitted session’s `executions` tree
- no new transcript is created under the legacy namespace-execution root
- the command’s public behavior remains correct
- directory and transcript permissions are owner-only
- terminal eviction releases descriptors and leases
- cancellation follows the same ownership order
- execution leaves are removed
- workspace teardown reaches logical quiescence
- run-owned cleanup removes its own residue

### Restart/reap case

The packaged restart/reap case must prove:

- restart recovery does not delete active or unsafe legacy entries
- eligible old legacy residue is reaped
- symlink, recent, malformed, foreign, and active entries are skipped
- each pass remains within the entry and depth bounds
- a teardown deadline preserves recovery state rather than deleting live storage
- a later restart can safely complete cleanup
- no new command writes to the legacy root

Use a fresh build for the first packaged gate with `E2E_REBUILD_BINARY=1`. Reuse a staged binary only after the build gate passed, its identity was recorded, and no relevant source changed.

## Required tiny benchmark

Add and validate the Stage 01 preset:

`workspace-scratch-tiny.yml`

with seed:

`0x5A01`

Use the same revision for both sides:

- control: legacy locator adapter
- candidate: workspace-scoped locator

Do not compare against an old binary.

The run shape is:

- two warmup pairs
- six measured alternating pairs
- twelve measured lifecycles total
- one cancellation
- whole run at most `60s`
- each operation at most `60s`

Evaluate:

- no-op latency diagnostic alert at `+3%` and `+0.5ms`
- throughput at least `97%` of control
- RSS at most `384 MiB`
- RSS at most `128 MiB` above idle
- quiescence polling every `100ms` for at most `5s`
- all logical owner gauges settle
- Theil–Sen slope is not positive outside the control noise band

Do not make a p95 claim from this tiny sample.

Reuse the Stage 00 strict data models and artifact recovery. Missing, malformed, truncated, wrong-run, or contradictory evidence must fail closed.

## Dependency and portability proof

Compare the completed Stage 01 state with the frozen Stage 00 post-baseline using the existing exact comparator for every frozen invocation.

Required result:

- zero external dependency graph delta
- zero feature delta
- zero direct-edge delta
- no `Cargo.lock` dependency change
- no new Cargo, Python, system, runtime, or image helper dependency

Internal use of dependencies already present may change, but the exact external graph and semantic environment inventory must remain equal.

If a manifest or lockfile changes for a non-dependency reason, prove the exact graph remains equal and explain the change.

## Live-test custody and report rules

Follow the repository’s E2E rules for every live Docker, packaged E2E, or benchmark command.

Before each live command, append an intent entry to:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`

After it finishes, append the result with:

- exact command
- start and end time
- duration
- exit status
- stable case or preset ID
- build/reuse decision and binary identity
- run ID
- evidence and artifact paths
- cleanup/custody result
- qualification conclusion

Use run-owned state and cleanup only. Never delete another run’s containers, networks, volumes, evidence, or state.

While debugging, run only the smallest focused command that answers the current question. Do not rerun a passing suite without a source or fixture change that invalidates it. Do not run the broad affected suite, host matrix, or final Phase 1 qualification.

## Validation order

Derive the exact supported commands from the current repositories and Stage 01 E2E contract. The expected focused product sequence is:

1. `cargo fmt --all -- --check`
2. `cargo clippy --locked -p sandbox-runtime-workspace -p sandbox-runtime --all-targets --all-features -- -D warnings`
3. focused workspace scratch tests equivalent to:
   `cargo test -p sandbox-runtime-workspace execution_scratch -- --nocapture`
4. focused runtime integration tests equivalent to:
   `cargo test -p sandbox-runtime workspace_execution_scratch -- --nocapture`
5. focused config, query, CLI, and catalog tests changed by Stage 01
6. exact dependency/environment comparison against the Stage 00 baseline
7. packaged lifecycle case
8. packaged restart/reap case
9. tiny preset validation
10. tiny benchmark run and recovery validation
11. artifact compatibility validation
12. no-helper portability validation

If an expected test filter does not exist, identify the real Stage 01 test target and use the smallest equivalent command. Do not “fix” a missing filter by running an entire broad suite.

The former image-fixture blocker no longer governs steps 7–11. Use the pinned
index and corrected arm64 descriptor from Iteration 56, record the resolved
platform identity for each live run, and do not reinterpret that correction as
host qualification.

## Exit gate

Stage 01 may be reported **passed** only if all of the following are true:

- both repositories remain on `upgrade-2.0-phase-1`
- all pre-existing Stage 00 changes are preserved
- all new transcripts route through the validated workspace locator
- no new transcript writes use the legacy global root
- identifier and symlink escape attempts are rejected
- owner-only modes are proven
- normal completion and cancellation release terminal ownership
- teardown receives an explicit zero-owner proof
- deadline behavior preserves recoverable state
- restart reaping is safe, bounded, and restart-correct
- structured evidence is bounded and reaches the existing public observation surface
- focused Rust and changed-surface tests pass
- both packaged Stage 01 E2E cases pass
- the Stage 01 tiny benchmark passes its logical and physical gates
- artifact recovery and compatibility checks pass
- exact dependency/environment delta is zero
- no-helper portability is proven
- the append-only report contains complete command custody and evidence
- the Stage 00 image-fixture correction and its Iteration 56 provenance are preserved

If any item is unresolved, report **Stage 01 blocked** or **Stage 01 failed** accurately. Distinguish:

- implementation complete but qualification blocked
- implementation/test defect
- infrastructure or immutable-fixture blocker

Do not weaken a gate to obtain a pass.

## Final response

Report:

- concise implementation outcome
- files changed, grouped by product and test repository
- key ownership and teardown design decisions
- focused validation commands and results
- packaged E2E and benchmark run IDs
- dependency/environment comparison result
- evidence and report paths
- cleanup/custody status
- remaining blockers, if any
- final verdict: passed, blocked, or failed

Do not commit or push unless the user explicitly asks.
