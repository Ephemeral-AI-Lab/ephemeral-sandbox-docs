/goal Implement and verify the bounded semantic scanner, Merkle and attribution builders, and independent final-tree oracle required for the Stage 04.6 MPLA M1 smoke milestone, then return a scoped commit and structured handoff.

# M1 Worker A — bounded semantics and independent oracle

You are a fresh M1 Codex task in an isolated git worktree. You have no conversational context from M0. The M0 → M1 capsule, phase-checkpoint commit, evidence, and repository state are your only handoff. Do not create subagents or other Codex tasks.

## Mission

Implement the complete bounded `mpla-poc-semantic-v1` scanner, Merkle/attribution builder, and separately compiled independent final-tree oracle needed for the smoke matrix.

Target phase contribution: finish within the M1 7–11 cumulative elapsed-hour gate.

## Read before editing

Read:

- the completed M0 → M1 capsule in `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/progress_tracker.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/requirements_and_prohibitions.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/new_plan.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/test_matrix.md`, especially SM-03 and SM-06 through SM-09;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/implementation_plan.md`, especially §§1, 3, 6–7, 10 and steps 5–6;
- repository `AGENTS.md` and `CLAUDE.md`.

Inspect LayerStack v3 semantic vocabulary and existing bounded CDC/spool tests identified in the plan. The PoC format is not LayerStack v3 compatibility proof.

## Preconditions

Wait for the lead to supply:

- the M0 evidence root and `PASS` verdict;
- frozen `m1-iface-v1`;
- exact exclusive paths;
- candidate semantic input/output interfaces;
- memory-pool, spool, evidence, and fixture interfaces.

Report missing inputs instead of recreating shared types.

Pure unit tests may run concurrently. Obtain the lead-issued physical execution lease before any real Docker, large-fixture, memory, storage, or timed run. Your artifacts are developmental until the lead reruns the integrated smoke suite.

## Exclusive scope

Expected files:

- `src/semantic/mod.rs`
- `src/semantic/record.rs`
- `src/semantic/scan.rs`
- `src/semantic/chunk.rs`
- `src/semantic/spool.rs`
- `src/semantic/trie.rs`
- `src/semantic/attribution.rs`
- `src/oracle_scan.rs`
- `src/oracle_record.rs`
- `src/bin/mpla-poc-oracle.rs`
- `tests/semantic_vectors.rs`
- `tests/spool_bounds.rs`
- `tests/oracle_crosscheck.rs`
- one lead-approved M1 semantic integration-test file

Do not edit manifests, `src/lib.rs`, shared types, aggregate smoke dispatch, locator/ref modules, or the tracker.

## Required implementation

Candidate builder:

1. Stream complete normalized filesystem semantics required by the matrix:
   regular content, directories, symlinks, hardlinks, sparse layout, mode, uid/gid, mtime policy, xattrs, whiteouts, opaque directories, and type changes.
2. Exclude AllocationId, paths to storage roots, physical locators, inode identities, mount IDs, and OverlayFS details from RootId and AttributionRootId.
3. Use bounded buffers and an 8 MiB application pool.
4. Use bounded external sort/spool for high cardinality; no fixture-sized mmap and no unbounded task creation.
5. Emit deterministic semantic records, canonical root, attribution root, bytes read, entry count, spool runs, FD use, and phase spans.
6. Support receipt-hit incremental behavior without scanning old payload history.

Independent oracle:

1. Compile as a separate binary.
2. Do not import candidate scanner, traversal, record encoder, or crate library entry point.
3. Scan an explicitly reconstructed final tree.
4. Emit independently encoded sorted records plus roots.
5. Compare decoded record streams, not only final hashes.
6. Prove identical roots after test-only physical allocation/path/inode/locator substitution.

Fixed-size 1 MiB streaming chunks are acceptable only if the plan’s semantics and performance gates remain valid. Do not silently claim LayerStack v3 format compatibility.

## Required verification

Unlock and support:

- SM-03 forced-miss scan/hash;
- SM-06 sixteen sequential tiny deltas;
- SM-07 256 MiB already-upper file with 4 KiB change;
- SM-08 20k-file bounded-memory publication;
- SM-09 full semantic mutation matrix and physical substitution.

Verify raw memory, bytes-read, spool, FD, record-stream, root, and attribution artifacts. The lead owns suite aggregation and locator/ref integration.

## Handoff format

Return the canonical handoff envelope from progress tracker §13, then include:

1. `Semantic-v1 coverage`.
2. `Fields explicitly excluded from identity`.
3. `Bounded-memory/spool design and observed maxima`.
4. `Oracle independence boundary`.
5. `Record/root comparisons`.
6. `SM rows unlocked and their status`.
7. `Known semantic differences from LayerStack v3`.

Do not edit the tracker. End after handoff.

## Codex-task checkpoints and commit

Send `STARTED`, `DISCOVERY_COMPLETE`, `FIRST_BUILD`, `FOCUSED_TESTS`, and `HANDOFF_READY` checkpoints. Send `NEEDS_ATTENTION` immediately with one precise lead action when blocked.

Commit only assigned files in your isolated worktree. Do not push. The canonical handoff must contain the commit SHA and base phase-checkpoint SHA.
