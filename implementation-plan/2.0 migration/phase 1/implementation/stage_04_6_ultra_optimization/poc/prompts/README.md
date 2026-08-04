# MPLA PoC Codex task prompt index

The original Q0–M2 prompts are retained as history. The current entrypoint for
formal Booster scorecard testing, repair, and optimization is
`booster_scorecard_qualification_lead.md`. That prompt explicitly authorizes
bounded subagents for research, exploration, profiling, and troubleshooting
while keeping contending physical benchmark work serialized.

| Role and phase | Prompt |
| --- | --- |
| Persistent lead, Q0 through final decision | `lead.md` |
| M0 Worker A, qualification/evidence | `m0_worker_a_qualification.md` |
| M0 Worker B, allocation/durability | `m0_worker_b_durability.md` |
| M1 Worker A, semantics/oracle | `m1_worker_a_semantics.md` |
| M1 Worker B, locator/ref/recovery | `m1_worker_b_recovery.md` |
| M2 Worker A, scale/stream/copy-up | `m2_worker_a_scale.md` |
| M2 Worker B, overload/crash/evacuation | `m2_worker_b_faults.md` |
| M2R takeover lead, scoped storage authority through final rerun | `m2_revision_lead.md` |
| M2R Worker A, public lifecycle security profile | `m2_revision_worker_a_security.md` |
| M2R Worker B, HV-07 real-operation wiring | `m2_revision_worker_b_hv07.md` |
| Booster scorecard qualification, bug repair, and speed optimization | `booster_scorecard_qualification_lead.md` |

Every launchable prompt file begins with `/goal `. When creating a worker task, use the complete file contents unchanged and append the lead assignment capsule. Never place text before `/goal`.

For a new Booster scorecard campaign, launch
`booster_scorecard_qualification_lead.md`. The rotation rules below apply to the
older M2R corrective workflow and are retained as historical operating guidance.

## Rotation rule

For a new takeover, start with `m2_revision_lead.md`. Do not restart with `lead.md`; the original M0/M1 results and the sealed M2 blocker are inputs to the corrective run.

1. The takeover lead verifies blocked checkpoint `d49c44b35eabbb40b98874d907edcdd40decf6e3` and ref `mpla-poc/m2-blocked-20260728T011331p0800`.
2. The lead allocates a fresh corrective run/evidence root, establishes `m2r-iface-v1`, updates `../progress_tracker.md`, and creates a scoped corrective checkpoint plus a named local branch/ref.
3. The lead resolves the saved project with `list_projects`.
4. When Codex task/session tools are available, the lead calls `create_thread` twice using isolated git worktrees based on that branch/ref. If unavailable, the assignments run sequentially with the same scopes, or the operator launches the two prepared worker prompts manually.
5. Each initial request starts with the complete current phase prompt and therefore with `/goal `, then appends a delimited lead assignment capsule with the checkpoint SHA/ref, interface, exclusive paths, run ID, evidence root, blockers, prior handoff capsule, and execution-lease status.
6. The lead records task/thread IDs, host IDs, cursors, and checkpoint SHA/ref in the tracker.
7. Workers edit only assigned files, create scoped local commits, and return structured handoffs with commit SHAs.
8. The lead monitors both tasks with cursor-based `wait_threads`, resolves attention requests, reviews commits, cherry-picks, verifies, and updates the tracker.
9. After integration, the lead archives both completed tasks.
10. The lead integrates both corrective handoffs, performs the public-path security qualification, and then owns the serialized physical campaign and final evidence decision.

Do not reuse the archived M2 worker tasks. The progress tracker, blocked checkpoint, sealed evidence artifacts, and repository state are the context bridge.

Do not use `spawn_agent` or another hidden subagent mechanism for the corrective workers. Use visible Codex tasks when available.
