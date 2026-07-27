# MPLA PoC Codex task prompt index

Use one persistent lead Codex task and newly created worker Codex tasks at each phase boundary. Do not use subagents.

| Role and phase | Prompt |
| --- | --- |
| Persistent lead, Q0 through final decision | `lead.md` |
| M0 Worker A, qualification/evidence | `m0_worker_a_qualification.md` |
| M0 Worker B, allocation/durability | `m0_worker_b_durability.md` |
| M1 Worker A, semantics/oracle | `m1_worker_a_semantics.md` |
| M1 Worker B, locator/ref/recovery | `m1_worker_b_recovery.md` |
| M2 Worker A, scale/stream/copy-up | `m2_worker_a_scale.md` |
| M2 Worker B, overload/crash/evacuation | `m2_worker_b_faults.md` |

Every prompt file begins with `/goal `. When creating a worker task, send the file contents as the initial request without placing any text before `/goal`.

## Rotation rule

1. Start the lead with `lead.md`.
2. The lead establishes the phase interface, updates `../progress_tracker.md`, and creates a scoped phase-checkpoint commit.
3. The lead resolves the saved project with `list_projects`.
4. The lead calls `create_thread` twice using isolated git worktrees based on that checkpoint.
5. Each initial request is the exact current phase prompt and starts with `/goal `.
6. The lead records task/thread IDs, host IDs, cursors, and checkpoint SHA in the tracker.
7. Workers edit only assigned files, create scoped local commits, and return structured handoffs with commit SHAs.
8. The lead monitors both tasks with cursor-based `wait_threads`, resolves attention requests, reviews commits, cherry-picks, verifies, and updates the tracker.
9. After integration, the lead archives both completed tasks.
10. The lead creates two new tasks from the next phase prompts.

Do not carry a worker task between M0, M1, and M2. The progress tracker, checkpoint commit, evidence artifacts, and repository state are the only context bridge.

Do not use `spawn_agent` or any subagent mechanism. The user explicitly requires visible, fresh Codex tasks.
