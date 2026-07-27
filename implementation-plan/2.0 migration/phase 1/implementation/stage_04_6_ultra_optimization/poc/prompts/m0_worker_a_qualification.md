/goal Implement and verify the M0 Docker, OverlayFS, resource, and evidence qualification slice for the Stage 04.6 MPLA PoC, then return a scoped commit and structured handoff to the persistent lead.

# M0 Worker A — qualification and evidence

You are a fresh, phase-bounded Codex task running in an isolated git worktree. You do not retain context from any earlier worker. Your task ends with one scoped local commit and a structured handoff to the persistent lead. Do not create subagents or additional Codex tasks.

## Mission

Implement the smallest real qualification and evidence slice that proves the Docker Desktop Linux environment can exercise stationary OverlayFS allocation. Produce evidence infrastructure usable by the lead’s M0 publication path.

Target effort: 30–60 agent minutes after the lead freezes `m0-iface-v1`.

## Read before editing

Read:

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/requirements_and_prohibitions.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/new_plan.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/test_matrix.md`, especially SM-01, SM-03, SM-13, and the environment envelope
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/implementation_plan.md`, especially §§1–3, 6, 7, 9–10, and steps 0–1
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/progress_tracker.md`, especially current phase, M0 ownership, interface freeze, and blockers
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/AGENTS.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/CLAUDE.md`

Inspect the existing overlay, cgroup, disk, and Docker-provider code named by the implementation plan before reusing it.

## Preconditions

Do not edit until the lead has supplied:

- the absolute PoC crate path;
- the frozen `m0-iface-v1` types and signatures;
- your exact exclusive file list;
- the active run ID;
- the expected evidence directory.

If any precondition is missing, report it to the lead instead of guessing or editing shared files.

Real Docker/OverlayFS qualification requires the lead-issued physical execution lease from progress tracker §4.4. Do not start it concurrently with another measured physical run.

## Exclusive scope

Expected files, subject to the lead’s assignment:

- `src/evidence.rs`
- `src/qualify.rs`
- `src/docker_protocol.rs`
- one lead-approved M0 qualification integration-test file

Do not edit:

- either Cargo manifest;
- `src/lib.rs`, `src/config.rs`, or shared ID/state/error/protocol types;
- `bin/mpla-poc`;
- aggregate smoke/heavy dispatch;
- `progress_tracker.md`;
- Worker B or lead-owned files.

Request shared-interface changes in the handoff.

## Required implementation

Implement:

1. Schema-versioned, atomic JSON evidence writes with explicit failed/cancelled records.
2. Qualification probes for:
   - exactly 4 vCPU and 4 GiB Docker Desktop allocation;
   - required Ubuntu 24.04 Linux/arm64 image digest;
   - real OverlayFS mount, write, whiteout, opaque-dir, xattr, and strict unmount;
   - permanent upper and adjacent workdir;
   - distinct payload and control mount IDs;
   - cgroup v2, `pidfd`, `syncfs`, memory, OOM, CPU, I/O, and mountinfo availability;
   - filesystem type, mount options, architecture, kernel, free bytes, and free inodes.
3. Before/after physical snapshots containing path, AllocationId supplied by the lead, `st_dev`, representative `(dev, ino)`, logical bytes, `st_blocks*512`, and inode/file counts.
4. A qualification result that fails closed when a mandatory feature is absent.
5. SM-01’s real qualification slice and durable receipt.

Use real Linux and filesystem interfaces. Do not mock OverlayFS, mount IDs, blocks, inodes, cgroups, or xattrs.

Fanotify may be optional only as allowed by the implementation plan. If unavailable, record it explicitly; do not weaken the mandatory physical union evidence.

## Validation

Run formatting and the narrowest lead-approved tests. Do not run destructive cleanup outside the exact PoC run ID. Do not change Docker resource allocation.

Completion requires:

- a real OverlayFS qualification receipt;
- payload/control mount separation;
- stable permanent-upper sentinel evidence;
- schema-valid JSON;
- focused tests passing;
- no edits outside your assigned files.

## Handoff format

Return the canonical handoff envelope from progress tracker §13, then include these role-specific fields:

1. `Behavior implemented`.
2. `Observed environment`, including CPU, memory, kernel, architecture, filesystem, and mount IDs.
3. `Qualification probes passed and failed`.
4. `Tests unlocked`.

Do not edit the progress tracker. End your task after the handoff.

## Codex-task checkpoints and commit

Send concise progress checkpoints in your task at:

- `STARTED`: required reading and interface preconditions confirmed;
- `DISCOVERY_COMPLETE`: reuse decisions and exact files confirmed;
- `FIRST_BUILD`: first compile result;
- `FOCUSED_TESTS`: commands, results, and artifact path;
- `NEEDS_ATTENTION`: immediately when blocked, with one precise lead action;
- `HANDOFF_READY`: scoped commit SHA ready for lead review.

Commit only assigned files in your isolated worktree. Do not push. The canonical handoff must contain the commit SHA and base phase-checkpoint SHA.
