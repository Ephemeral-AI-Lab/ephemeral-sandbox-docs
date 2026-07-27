/goal Implement, run, and evidence HV-01 through HV-04 for existing-size independence, one-GiB streaming, honest OverlayFS copy-up, and the exact 250k-file workload, then return a scoped commit and structured handoff.

# M2 Worker A — existing-size, streaming, copy-up, and file-count scale

You are a fresh M2 Codex task in an isolated git worktree. You inherit no M1 conversation. The M1 → M2 tracker capsule, phase-checkpoint commit, evidence, and repository state are authoritative. Do not create subagents or other Codex tasks.

## Mission

Implement, run, debug, and evidence HV-01 through HV-04 without weakening workload size, operation boundaries, durability, or memory limits.

Target phase contribution: finish within the M2 12–20 cumulative elapsed-hour gate.

## Read before editing

Read:

- the M1 → M2 capsule in `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/progress_tracker.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/requirements_and_prohibitions.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/new_plan.md`;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/test_matrix.md`, HV-01 through HV-04;
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/implementation_plan.md`, especially test mapping, measurement, runtime, memory/storage, risks, and definition of done;
- repository `AGENTS.md` and `CLAUDE.md`.

Inspect the accepted M1 semantic/oracle code and its raw smoke evidence before modification.

## Preconditions

Require:

- M1 `PASS`;
- frozen `m2-iface-v1`;
- exact exclusive paths;
- immutable heavy fixtures or fixture-generation commands;
- evidence run ID and directory;
- lead-provided current I2 control interface.

If the current control is incompatible, report `UNKNOWN`; do not invent or use a historical denominator.

Every HV-01 through HV-04 physical run requires the lead-issued execution lease. Do not overlap large fixtures or timed measurements with the lead or Worker B. Your artifacts are developmental until the lead verifies the integrated heavy suite.

## Exclusive scope

You retain phase-exclusive ownership of:

- `src/semantic/**`
- `src/oracle_scan.rs`
- `src/oracle_record.rs`
- `src/bin/mpla-poc-oracle.rs`
- semantic/oracle tests
- one lead-approved `tests/cases/heavy_scale.rs` or equivalent file

Do not edit aggregate `heavy.rs`, manifests, `src/lib.rs`, shared resource types, control implementation, recovery modules, or the tracker.

## Required cases

### HV-01: existing-size independence

- Use 1 GiB, 5 GiB, and no-more-than-9 GiB existing states.
- Add the same approximately 1 MiB new delta.
- Use three matched current I2 controls.
- Include the full `Tpub` boundary.
- Prove no old payload scan/copy, no size-dependent slope, and peak `H+O(M)`.
- Apply required and preferred absolute/ratio gates exactly as written.

### HV-02: one-GiB upper stream

- Stream a real 1 GiB changed upper.
- Include scan, hash, flush, adoption, locator, and ref work.
- Run three interleaved candidate/comparator pairs.
- Keep the candidate pool exactly 8 MiB.
- Enforce storage-domain 96/128 MiB limits.
- Report raw throughput, medians for eligible repeated cases, and maxima.
- Require correct oracle result and no second 1 GiB payload.

### HV-03: honest lower copy-up

- Start with a lower-only 1 GiB file.
- Time from immediately before the first 4 KiB write through publication response.
- Include real kernel copy-up.
- Accept honest approximately 1 GiB upper growth.
- Prove publication creates no additional payload-sized twin.

### HV-04: 250k files

- Use exactly 250,000 files; never reduce cardinality.
- Include complete scan/sort/hash/adoption.
- Track process/cgroup memory, kernel slab where available, FDs, spool, queues, allocated blocks, inodes, and OOM events.
- Enforce the 8 MiB pool and 96/128 MiB storage-domain limits.
- Compare every semantic entry through the independent oracle.

## Failure discipline

Do not raise limits, shrink fixtures, remove fsync, exclude copy-up, mmap the fixture, or add unbounded workers. A failure under the required envelope is evidence.

When a case fails, preserve its raw artifact, isolate the phase/subsystem, make only changes within your assigned files, and rerun the smallest dependent case.

## Handoff format

Return the canonical handoff envelope from progress tracker §13, then include:

1. One result block for each HV-01 through HV-04.
2. Exact fixture sizes and counts.
3. Timed boundaries and phase spans.
4. Raw samples, medians where permitted, and maxima.
5. Peak pool, RSS, cgroup memory, slab, FDs, spool, blocks, inodes, and OOM events.
6. Root/oracle results.
7. No-second-copy evidence.
8. Recommended design decision.

Do not edit the tracker. End after handoff.

## Codex-task checkpoints and commit

Send `STARTED`, `DISCOVERY_COMPLETE`, `FIRST_BUILD`, `FOCUSED_TESTS`, and `HANDOFF_READY` checkpoints. Send `NEEDS_ATTENTION` immediately with one precise lead action when blocked.

Commit only assigned files in your isolated worktree. Do not push. The canonical handoff must contain the commit SHA and base phase-checkpoint SHA.
