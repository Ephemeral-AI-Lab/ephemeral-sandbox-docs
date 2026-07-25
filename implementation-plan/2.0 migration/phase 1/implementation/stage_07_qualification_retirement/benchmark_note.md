# Stage 07 benchmark and qualification note

Status: **NOT_RUN / OPEN**.

Stage 07 does not define new thresholds. It closes every required row in:

- [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)
- [overall Stage 03–07 scorecard](../stage_03_07_benchmark_note.md)
- Stage 03–06 benchmark notes.

In particular, the release artifact must replay the exact
[Stage 05 campaign matrix and artifact schema](../stage_05_retention_gc_packs/benchmark_note.md).
Stage 07 does not replace that campaign with an architectural review or a smaller
smoke test.

## Imported Stage 03 deferral ledger

Stage 03 completed its correctness POC, but the canonical `S03-Q07` release
qualification row did not pass. Its children are tracked here until Stage 07
binds them to the exact release artifact:

| Transfer ID | Required result | Artifact/decision | Status |
| --- | --- | --- | --- |
| `S07-X03-01` | host/filesystem/architecture qualification matrix | — | `OPEN` |
| `S07-X03-02` | Preparation 04 64/256/1024 MiB input/history × 1/16/64-root RSS/resource matrix | — | `OPEN` |
| `S07-X03-03` | matched five-minute baseline/candidate campaigns and three-invocation selection decision | — | `OPEN` |
| `S07-X03-04` | exhaustive corpus, long soak, restart storm and release variance | — | `OPEN` |
| `S07-X03-05` | release replay of real Stage 04 materialization/activation | — | `OPEN` |
| `S07-X03-06` | release replay of real Stage 05 common replacement, two-phase admission, two-cycle GC, singleton retirement, and squash | — | `OPEN` |
| `S07-X03-07` | Stage 06 rollback/re-cutover plus separately approved retirement | — | `OPEN` |
| `S07-X03-08` | attribution/checkpoint survival through all real destructive transitions | — | `OPEN` |

The exact acceptance criteria and prerequisite mapping are normative in
[`spec.md` §0](spec.md#0-imported-stage-03-deferrals). Do not change an
intermediate Stage 04–06 result directly to a Stage 07 pass without release
artifact replay and the terminal evidence named there.

## Decision ledger

| Decision | Required evidence | Status |
| --- | --- | --- |
| opt-in qualification | all correctness/crash/perf/space/memory/environment rows pass | `OPEN` |
| candidate default | qualification approval plus bounded cohort/rollback soak | `OPEN` |
| legacy retirement | recent rollback rehearsal, evacuation proof, explicit destructive approval | `OPEN` |

## Stage 05/retirement release replay

The `S07-X03-06` and retirement decisions require all of:

| Evidence | Required release-artifact result | Status |
| --- | --- | --- |
| resource scale | complete `B=64/256/1,024 MiB × 1/16/64-root` matrix and separate Preparation 04 64/256/1,024 MiB input/history scale cells, including all Stage 05 caps and long-lived quiescence | `OPEN` |
| lookup/startup | fixed active locator runs/bytes and capped recovery state, with no historical-state slope | `OPEN` |
| foreground maintenance impact | matched p50/p95/p99/maximum for pack, locator merge, mark, sweep, retirement, evacuation, and squash | `OPEN` |
| maintenance throughput | bytes/records/edges per second and slice/pause distributions for every large operation | `OPEN` |
| peak space | measured `settled + T_build + H_gen + H_gc + H_trash`, including long readers, restart, and `ENOSPC` | `OPEN` |
| settled space | exact Preparation 04 amplification, duplication, pack-slack, metadata, and zero unexplained unreachable/unleased bytes | `OPEN` |
| GC liveness | candidate cycle IDs, blockers, queue time, and convergence after roots/holds/uncertainty clear | `OPEN` |
| retirement protocol | exact Stage 07 approval/authority fence plus Stage 05 `Pending`/`Deleting`/`Done` recovery and ledger backpressure | `OPEN` |
| ownership safety | tasks, permits, queues, buffers, FDs, mappings, holds, retries, operation residue, cancellation/panic cleanup | `OPEN` |

Legacy-retirement space is not passed merely because deleting v1 lowers settled bytes.
Report pre-retirement settled bytes, candidate-retired peak while v1/ledger trash and
held generations overlap, post-settle bytes, bytes written/renamed/unlinked, recovery
overlap, and time to explained convergence. Stage 07 performs no direct unlink and has
no separate trash/deletion accounting family.

Exact release revision, image digests, effective Linux
Engine/Desktop-VM kernel, `/eos` backing filesystem, mount/backend capability profile,
CPU architecture, corpus hashes, commands, raw artifact paths, thresholds,
distributions, and owner approvals must be attached. Architecture review is not
benchmark evidence and cannot support a universal or image-percentage compatibility
claim. Each cell records `PASS`, `FAIL`, or `OPEN`; missing accounting is `OPEN`, while
any correctness, corruption, leak, cap, or unexplained-residue failure forces `FAIL`.
