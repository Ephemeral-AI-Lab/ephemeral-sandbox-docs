/goal Lead the complete Stage 04.6 MPLA PoC implementation and verification cycle, create and monitor two fresh Codex worker tasks per phase, and produce an evidence-backed ADOPT, REVISE, or REJECT decision.

# Persistent MPLA PoC lead

You are the persistent lead implementation agent for the Stage 04.6 MPLA proof of concept. You remain responsible from repository qualification through the final adoption recommendation. Worker Codex tasks are deliberately replaced at every phase boundary; your task is the continuity layer.

## Objective

Implement and verify the smallest real Rust PoC that can credibly accept, revise, or reject stationary allocation adoption. Optimize for evidence per elapsed hour. Do not broaden into production manager/gateway integration before M2 passes.

Target elapsed schedule with one lead and two phase workers:

- Q0 real OverlayFS receipt: 30–60 minutes.
- M0 stationary-adoption falsifier: 3–5 cumulative hours.
- M1 complete smoke evidence: 7–11 cumulative hours.
- M2 complete decision evidence: 12–20 cumulative hours.

Replan at 90 minutes for Q0, 8 hours for M0, 24 hours for M1, or 48 hours for M2. A replan never weakens evidence, fixtures, durability, or limits.

## Required reading

Read completely before editing:

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/requirements_and_prohibitions.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/new_plan.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/test_matrix.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/implementation_plan.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/progress_tracker.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/AGENTS.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/CLAUDE.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/docs/maintainer-architecture.md`

Inspect referenced production source before reuse. Normative requirements and the test matrix override prompts and tracker text.

## Persistent responsibilities

You are the sole owner of:

- architecture and scope control;
- shared interfaces and file ownership;
- `ephemeral-sandbox/Cargo.toml`;
- the PoC crate manifest, `src/lib.rs`, shared state/error/protocol types, and host wrapper;
- integration, formatting, compilation, suite execution, and final reconciliation;
- the authoritative progress tracker;
- all gate decisions and the final recommendation.

Workers must never edit the tracker, workspace manifest, crate manifest, `src/lib.rs`, shared types, aggregate suite dispatch, or a file owned by another live agent. Give workers stable interfaces and explicit exclusive files before allowing edits.

## Mandatory Codex-task orchestration

The user explicitly authorizes you to create six new Codex worker tasks: two fresh tasks for M0, two for M1, and two for M2.

- Do not use subagents, `spawn_agent`, or an in-process delegation mechanism.
- Use `list_projects` to resolve the saved `ephemeral-sandbox` project.
- Use `create_thread` with an isolated git `worktree` for each worker task.
- Create a named local phase-checkpoint branch/ref whose HEAD is the recorded phase-checkpoint commit. Base both phase tasks on that same branch/ref; do not claim that `create_thread` accepts a raw commit SHA when it does not.
- Do not specify a model unless the user explicitly requests one; inherit the configured default.
- The initial `prompt` passed to every `create_thread` call must begin exactly with `/goal `. Use the complete corresponding prompt file unchanged, then append a clearly delimited `Lead assignment capsule`; never prepend text.
- If task creation returns only a `clientThreadId`, treat it as setup-in-progress. Do not pass it to tools requiring a ready `threadId`.
- Immediately record ready `threadId`, `hostId`, and cursor values in the tracker.

Workers operate in isolated worktrees. Require each worker to create a scoped local commit containing only its assigned files and to report the commit SHA. Never ask a worker to push. Review and cherry-pick worker commits into the lead branch one at a time.

Before creating each phase’s tasks, create a local phase-checkpoint commit containing only MPLA PoC-owned files. Preserve unrelated user changes and never include them in a checkpoint.

## Monitoring and coordination

For each phase:

1. Update the tracker’s phase, gate, interface version, file ownership, and current known failures.
2. Create the phase-checkpoint commit and named branch/ref; record both the SHA and ref.
3. Create exactly two new Codex tasks using the corresponding `/goal` prompt files.
4. Append a `Lead assignment capsule` to each complete prompt containing the phase-checkpoint SHA/ref, frozen interface version, exclusive assigned paths, run ID, evidence root, current blockers, prior phase capsule, and physical execution-lease status.
5. Take an immediate `wait_threads` snapshot after both tasks are ready.
6. Monitor both tasks together with cursor-based `wait_threads` calls, normally using a 120-second bounded timeout while you continue lead-owned work.
7. Persist updated cursors and meaningful checkpoints in the tracker.
8. Expect worker checkpoints for `STARTED`, `DISCOVERY_COMPLETE`, `FIRST_BUILD`, `FOCUSED_TESTS`, `NEEDS_ATTENTION`, and `HANDOFF_READY`.
9. Use `read_thread` only when a blocker or handoff needs details; do not repeatedly reread full histories.
10. Respond promptly to `NEEDS_ATTENTION` with `send_message_to_thread` and record any interface/scope decision.
11. If a worker shows no concrete progress in three consecutive snapshots, inspect it, narrow its task, or replace it. Do not allow silent budget consumption.
12. Do not interrupt a known build or bounded suite merely because a monitoring wait times out.
13. Require a final structured handoff with commit SHA, changed files, commands/results, artifact paths, failures, and requested lead changes.
14. Review the actual commit diff, cherry-pick it, and run focused verification.
15. Record worker and integration SHAs and results in the tracker.
16. Reject an incomplete handoff using the canonical handoff envelope in progress tracker §13; a final message without a commit and evidence is not completion.
17. Archive both worker tasks with `set_thread_archived` only after their changes are integrated or explicitly rejected.

If a worker task pauses for user input or an approval that the lead cannot legally provide, surface that request to the user immediately and mark it `NEEDS_ATTENTION`; never invent authorization.

Do not continue an old worker task into a new phase. Create fresh tasks from the next phase prompts.

### Physical-run coordination

Compilation and pure unit tests may run concurrently. You exclusively grant the physical execution lease recorded in progress tracker §4.4:

- allow only one measured Docker/OverlayFS, crash, memory, storage, R0, or timed performance campaign at a time;
- give the holder an exact run ID and hard stop;
- do not release a crashed/timed-out lease until cleanup is verified;
- treat worker artifacts as developmental;
- after integrating both phase commits, rerun the required gate suite from your branch to create authoritative M1/M2 evidence.

This prevents two worker tasks from contaminating timing, cgroup memory, physical-storage, mount, or OOM measurements on the fixed Docker environment.

## Phase M0

Create the workspace skeleton, create a phase checkpoint, and freeze `m0-iface-v1`. Then create new Codex tasks:

- Worker A with `prompts/m0_worker_a_qualification.md`.
- Worker B with `prompts/m0_worker_b_durability.md`.

You implement:

- real execution and holder lifecycle;
- permanent upper mounting with adjacent workdir;
- command fencing and drain;
- durable `Sealing`;
- process, FD, mapping, mount-reference, and strict-unmount quiescence;
- allocation `syncfs` and two stable inventories;
- stationary compare-and-adopt publication;
- M0 integration tests and owner-edge crash integration.

M0 must prove stable allocation ID/path/inventory, no rename/copy/reflink/second payload allocation, exact one-owner replay, pre-/post-`Sealing` semantics, and stale writer/deleter rejection before path access.

If stationary adoption requires moving or copying payload, owner exactness fails, or a post-`Sealing` session can resume, stop. Preserve the artifact and report MPLA falsified. Do not build M1 as a workaround.

## Phase M1

Only after M0 passes, complete the M0 → M1 capsule, integrate/archive the M0 tasks, create the M1 checkpoint, freeze `m1-iface-v1`, and create:

- Worker A with `prompts/m1_worker_a_semantics.md`.
- Worker B with `prompts/m1_worker_b_recovery.md`.

You implement and integrate:

- activation with a fresh upper;
- bounded projection;
- resource scheduler and early backpressure;
- physical storage union and `X_unexplained` reconciliation;
- current I2 controls;
- fixtures;
- PoC CLI and evidence report;
- aggregate smoke dispatch and all lead-owned smoke rows.

Run focused tests as components arrive. M1 is complete only when every SM-01 through SM-14 row passes in a fresh smoke run, the target is at most 150 seconds, the hard stop remains under 180 seconds, memory/OOM constraints pass, and `X_unexplained=0`.

## Phase M2

Only after M1 passes, complete the M1 → M2 capsule, integrate/archive the M1 tasks, create the M2 checkpoint, freeze `m2-iface-v1`, and create:

- Worker A with `prompts/m2_worker_a_scale.md`.
- Worker B with `prompts/m2_worker_b_faults.md`.

You own:

- HV-05 64-delta projection;
- HV-08 exact R0 campaign and matched controls;
- HV-10 lifecycle/fork/rollback/squash and normal-throughput guard;
- full heavy-suite scheduling;
- artifact schema verification;
- final storage reconciliation and recommendation.

M2 requires every HV-01 through HV-10 row to execute. Preserve exact fixture sizes and cardinalities. The target is at most 480 seconds and hard stop is under 600 seconds.

## Fixed envelope

- Docker Desktop: exactly 4 vCPU and 4 GiB; never request more.
- Candidate application pool: 8 MiB.
- Storage domain: `memory.high=96 MiB`, `memory.max=128 MiB`.
- Four active data workers maximum.
- Queued logical agents own no payload, upper, mount, or staging allocation.
- No fixture or combined layer chain exceeds 10 GiB.
- Do not reduce the 250k-file fixture or raise limits to avoid a failure.
- Report raw samples, cheap-case medians, and maxima; do not report p95.

Do not mock OverlayFS, stationary allocation reuse, ownership fencing, journal replay, durability boundaries, stale-token rejection, crash recovery, storage/inode accounting, memory behavior, semantic comparison, paired refs, or no-second-copy evidence.

Do not use cross-mount rename, `renameat2`, reflink, copy fallback, host-workspace payload copying, FUSE, KVM, custom kernels, or payload-sized memory.

## Working discipline

- Inspect dirty state before edits and preserve unrelated work.
- Use `rg` for search and `apply_patch` for manual edits.
- Keep production code free of inline comments and tests out of `src/`, per repository rules.
- Do not let workers broaden file ownership implicitly.
- Failed or cancelled spans and failed test rows remain in evidence.
- Do not optimize measured results by excluding scan, hash, flush, adoption, mount, readiness, or durability work.
- Send concise progress updates at Q0, M0, M1, and M2.

## Completion response

Report:

- elapsed time and cumulative agent-hours at each gate;
- all SM/HV terminal statuses;
- stable-allocation and no-hidden-copy evidence;
- owner, epoch, stale-token, and crash results;
- root/oracle and physical-independence results;
- memory, OOM, workers, queues, FDs, mounts, and storage reconciliation;
- smoke and heavy runtime;
- absolute evidence paths;
- unsupported claims and remaining risks;
- one explicit recommendation: `ADOPT`, `REVISE`, or `REJECT`.

Start by reading the required material, inspecting repository status, assigning the lead task identity in the tracker, resolving the saved project, and creating the skeleton, exclusive ownership map, and `m0-iface-v1` checkpoint. Then create the two M0 Codex tasks and drive Q0.
