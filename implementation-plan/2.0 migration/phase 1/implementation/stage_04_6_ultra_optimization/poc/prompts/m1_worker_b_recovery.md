/goal Implement and verify locator generations, paired atomic refs, OCC, and durable smoke recovery for the Stage 04.6 MPLA M1 milestone, then return a scoped commit and structured handoff.

# M1 Worker B — locators, paired refs, OCC, and smoke recovery

You are a fresh M1 Codex task in an isolated git worktree. You inherit no M0 conversation. Use the M0 → M1 tracker capsule, phase-checkpoint commit, evidence, and repository state. Do not create subagents or other Codex tasks.

## Mission

Implement durable locator generations, paired atomic refs, OCC, and recovery replay required to make stationary adoption externally publishable and crash-correct.

Target phase contribution: finish within the M1 7–11 cumulative elapsed-hour gate.

## Read before editing

Read:

- the M0 → M1 capsule in `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/progress_tracker.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/requirements_and_prohibitions.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/new_plan.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/test_matrix.md`, especially SM-03, SM-06, SM-10 through SM-13, and HV-07;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/implementation_plan.md`, especially §§3–5, 8, and steps 7 and 11;
- repository `AGENTS.md` and `CLAUDE.md`.

Inspect existing LayerStack refs/failpoint tests and workspace recovery behavior named by the plan.

## Preconditions

Wait for:

- M0 `PASS` and evidence root;
- frozen `m1-iface-v1`;
- owner-journal and canonical-object durability interfaces;
- exact assigned paths;
- named faultpoint API owned by the lead.

Do not edit shared interfaces to make them fit.

Pure unit tests may run concurrently. Obtain the lead-issued physical execution lease before real process/container kills, Docker, mount, storage, or timed recovery runs. Your artifacts are developmental until the lead reruns the integrated smoke suite.

## Exclusive scope

Expected files:

- `src/locator.rs`
- `src/ref_store.rs`
- `src/occ.rs`
- `src/recovery.rs`
- `tests/locator_ref_recovery.rs`
- one lead-approved M1 recovery/OCC integration-test file

Do not edit owner/lease/publication modules, canonical scanner files, manifests, `src/lib.rs`, aggregate smoke dispatch, shared faultpoint definitions, or the tracker.

## Required implementation

Implement:

1. Immutable forward and reverse locator generations.
2. Durable generation selectors.
3. Locator entries that resolve payload roots to AllocationIds without making physical data canonical identity.
4. Paired root and attribution-root ref commits.
5. Same-directory temp write, file fsync, rename, and parent-directory fsync.
6. Ref commit only after canonical objects and selected locator generation are durable.
7. Branch OCC with:
   - expected-parent validation;
   - disjoint rebase/convergence;
   - typed overlap conflict;
   - retained, owned, and accounted conflict allocation.
8. Replay using durable state, never in-memory state.
9. Response-loss idempotency by stable operation ID.
10. Old-or-complete-new visibility and exactly one owner.

Support deterministic crashes around:

- ownership intent;
- conditional owner transition;
- owner receipt;
- locator generation selection;
- canonical-object durability;
- ref replacement;
- parent-directory fsync;
- response loss.

Command fence, durable `Sealing`, unmount, and allocation flush faultpoints are lead-owned but your recovery must consume their durable outcomes.

Coarse branch locks and flat immutable files are acceptable. SQL or a general transaction service is unnecessary.

## Required verification

Support:

- completion of SM-03 publication durability;
- SM-06 locator/ref progression;
- SM-10 four disjoint publishers;
- SM-11 disjoint rebase and overlapping typed conflict;
- SM-12 smoke crash matrix;
- SM-13 exact ownership/debt inputs to reconciliation.

Every selected ref must resolve durable canonical and locator state. No replay may produce two owners or a selected incomplete generation.

## Handoff format

Return the canonical handoff envelope from progress tracker §13, then include:

1. `Locator and ref disk ordering`.
2. `Publication linearization point used`.
3. `OCC cases implemented`.
4. `Faultpoints and replay decisions covered`.
5. `SM rows unlocked and status`.
6. `Exact-owner/old-or-new evidence`.

Do not edit the tracker. End after handoff.

## Codex-task checkpoints and commit

Send `STARTED`, `DISCOVERY_COMPLETE`, `FIRST_BUILD`, `FOCUSED_TESTS`, and `HANDOFF_READY` checkpoints. Send `NEEDS_ATTENTION` immediately with one precise lead action when blocked.

Commit only assigned files in your isolated worktree. Do not push. The canonical handoff must contain the commit SHA and base phase-checkpoint SHA/ref.
