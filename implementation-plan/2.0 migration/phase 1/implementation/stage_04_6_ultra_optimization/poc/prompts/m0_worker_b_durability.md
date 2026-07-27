/goal Implement and verify the M0 permanent allocation, durable ownership, epoch-fenced lease, and stale-token primitives for the Stage 04.6 MPLA PoC, then return a scoped commit and structured handoff.

# M0 Worker B — allocation, ownership, lease, and durability

You are a fresh, phase-bounded Codex task in an isolated git worktree. Your context begins here and ends with a scoped local commit and structured handoff to the persistent lead. Do not create subagents or other Codex tasks.

## Mission

Implement the permanent allocation, durable ownership, epoch-fenced lease, and stale-token primitives required by the lead’s stationary publication path.

Target effort: 45–75 agent minutes after the lead freezes `m0-iface-v1`.

## Read before editing

Read:

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/requirements_and_prohibitions.md`, especially ownership, fencing, durability, and prohibited data motion
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/new_plan.md`, especially allocate/lease/seal/adopt semantics
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/test_matrix.md`, especially SM-02, SM-03, SM-04, SM-11, SM-12, and HV-07
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/implementation_plan.md`, especially §§3–5, 8, and steps 2 and 4
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/progress_tracker.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/AGENTS.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/CLAUDE.md`

Inspect the referenced workspace lifecycle, holder, LayerStack faultpoint, and durable-ref tests before coding.

## Preconditions

Wait for the lead to provide:

- the absolute PoC crate path;
- frozen `m0-iface-v1`;
- exact assigned paths;
- stable shared IDs/errors/evidence interfaces;
- active run ID and permanent arena root.

Do not guess shared contracts.

Pure unit/fault tests may run without the physical execution lease. Request the lead-issued lease before any real Docker, mount, cgroup, or measured filesystem run.

## Exclusive scope

Expected files, subject to lead confirmation:

- `src/allocation.rs`
- `src/durable.rs`
- `src/owner.rs`
- `src/lease.rs`
- `tests/allocation_owner.rs`

Do not edit Cargo manifests, `src/lib.rs`, shared types, publication/execution modules, aggregate suites, the host wrapper, or `progress_tracker.md`.

## Required implementation

Implement:

1. Permanent allocation creation at its final payload-arena path.
2. Stable random `AllocationId` unrelated to paths or canonical identity.
3. Adjacent `upper` and `work` directories on the same filesystem.
4. Explicit owner states and epochs sufficient for:
   - `WorkspaceOwned`;
   - owner-transition intent;
   - conditional `PayloadOwned`;
   - terminal/recovery/error states required by the implementation plan.
5. Epoch-fenced mutable leases and deletion capabilities.
6. Stale writer/deleter rejection before any payload pathname resolution or open.
7. Append-only framed journal records with version, length, operation ID, allocation ID, prior/new owner and epochs, phase, checksum, and terminal outcome.
8. Torn-tail detection.
9. Durable selector replacement using same-directory temp write, file fsync, rename, and parent-directory fsync.
10. Compare-and-adopt semantics that yield exactly one owner under retry or response loss.
11. Idempotent replay receipts.

Use real filesystem durability operations. In-memory state is never authoritative. Do not copy, rename, reflink, or recreate payload bytes during ownership transition.

Coarse allocation-local locking is acceptable. A database or generic transaction framework is not.

## Required tests

Test at minimum:

- allocation path and ID stability;
- legal and illegal owner transitions;
- current versus stale lease epochs;
- stale writer/deleter rejection before payload access;
- conditional owner transition conflict;
- torn journal tail;
- retry and response loss;
- crash/replay immediately before and after selector replacement;
- exactly one owner after replay.

The lead owns process termination, OverlayFS quiescence, and end-to-end publication integration.

## Handoff format

Return the canonical handoff envelope from progress tracker §13, then include:

1. `Durable state and journal format implemented`.
2. `Fsync/rename/parent-fsync ordering`.
3. `Stale-token evidence`.
4. `Crash/replay cases covered`.
5. `Tests unlocked`.

Do not edit the tracker. End after handoff.

## Codex-task checkpoints and commit

Send `STARTED`, `DISCOVERY_COMPLETE`, `FIRST_BUILD`, `FOCUSED_TESTS`, and `HANDOFF_READY` checkpoints. Send `NEEDS_ATTENTION` immediately with one precise lead action when blocked.

Commit only assigned files in your isolated worktree. Do not push. The canonical handoff must contain the commit SHA and base phase-checkpoint SHA/ref.
