/goal Implement, run, and evidence HV-06, HV-07, and HV-09 for overload, complete crash recovery, and pinned-reader evacuation, then return a scoped commit and structured handoff.

# M2 Worker B — overload, crash sweep, and evacuation

You are a fresh M2 Codex task in an isolated git worktree. You inherit no prior worker conversation. Use the M1 → M2 tracker capsule, phase-checkpoint commit, and durable repository/evidence state. Do not create subagents or other Codex tasks.

## Mission

Implement, run, debug, and evidence HV-06, HV-07, and HV-09: bounded overload behavior, complete crash replay, and post-publication evacuation with a pinned reader.

Target phase contribution: finish within the M2 12–20 cumulative elapsed-hour gate.

## Read before editing

Read:

- the M1 → M2 capsule in `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/progress_tracker.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/requirements_and_prohibitions.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/new_plan.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/test_matrix.md`, especially HV-06, HV-07, and HV-09;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/implementation_plan.md`, especially durable state machines, fault injection, resource controls, storage reconciliation, and definition of done;
- repository `AGENTS.md` and `CLAUDE.md`.

Inspect M1 owner/locator/ref journals and smoke crash artifacts before modifying recovery.

## Preconditions

Require:

- M1 `PASS`;
- frozen `m2-iface-v1`;
- exact exclusive files;
- active run ID and evidence directory;
- lead-owned scheduler/resource API;
- the complete named faultpoint registry;
- immutable fixtures.

Do not edit lead-owned scheduler or shared faultpoint definitions. Request changes through the lead.

Every HV-06, HV-07, and HV-09 physical run requires the lead-issued execution lease. Do not overlap crash, storage, or timed measurements with the lead or Worker A. Your artifacts are developmental until the lead verifies the integrated heavy suite.

## Exclusive scope

Expected files:

- `src/recovery.rs`
- `src/evacuation.rs`
- `tests/crash_matrix.rs`
- one lead-approved `tests/cases/heavy_faults.rs` or equivalent file

You may modify M1 Worker B’s locator/ref/OCC files only if the lead explicitly transfers those exact files for M2.

Do not edit manifests, `src/lib.rs`, shared state/resource types, aggregate heavy dispatch, semantic code, or the tracker.

## Required cases

### HV-06: overload and backpressure

- Exercise four active data workers and twelve queued logical agents.
- Prove queued agents own zero payload, upper, mount, and staging allocations.
- Keep coordinator/descriptor memory within the matrix bound.
- Attempt job 33 and require a typed overload response before allocation.
- Prove eventual progress and correct publication for admitted work.
- Consume the lead-owned scheduler API; request changes rather than editing it.

### HV-07: complete crash sweep

Use real process or container termination at every required point:

- command fencing;
- durable `Sealing`;
- holder stop/reap and unmount/quiescence;
- allocation flush;
- ownership intent;
- conditional owner transition;
- owner receipt;
- locator generation selection;
- canonical-object durability;
- ref replacement;
- parent-directory fsync;
- response loss;
- successor activation.

For every point:

- record durable before/after state;
- restart through the real recovery runner;
- require old-or-complete-new selected visibility;
- require exactly one owner;
- require idempotent retry by operation ID;
- prove post-`Sealing` sessions never resume;
- retain failed and cancelled spans;
- classify all temporary or retirement debt.

### HV-09: evacuation with pinned reader

- Start from a stationary adopted 1 GiB allocation.
- Hold a real reader across locator-generation replacement.
- Build the explicit post-publication pack; never call it publication.
- Record the honest old+new physical peak.
- Keep the old generation until the reader pin releases.
- Drain retirement debt and reconcile to zero.
- Require uninterrupted reader correctness, exact locator/owner state, and final `X_unexplained=0`.

## Failure discipline

Do not simulate crashes with in-memory exceptions. Do not skip fsync, reuse a dead session, free a pinned generation, hide temporary pack bytes, or increase limits. Preserve a bundle for every failed crash point.

## Handoff format

Return the canonical handoff envelope from progress tracker §13, then include:

1. HV-06 worker/queue/allocation timeline and verdict.
2. HV-07 table with every faultpoint and recovery verdict.
3. HV-09 reader/locator/pack/debt timeline and verdict.
4. Exact-owner and old-or-complete-new evidence.
5. Final storage/debt reconciliation.
6. Recommended design decision.

Do not edit the tracker. End after handoff.

## Codex-task checkpoints and commit

Send `STARTED`, `DISCOVERY_COMPLETE`, `FIRST_BUILD`, `FOCUSED_TESTS`, and `HANDOFF_READY` checkpoints. Send `NEEDS_ATTENTION` immediately with one precise lead action when blocked.

Commit only assigned files in your isolated worktree. Do not push. The canonical handoff must contain the commit SHA and base phase-checkpoint SHA/ref.
