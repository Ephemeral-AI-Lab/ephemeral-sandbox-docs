# Stage 07 benchmark and qualification note

Status: **NOT_RUN / OPEN**.

Stage 07 does not define new thresholds. It closes every required row in:

- [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)
- [overall Stage 03–07 scorecard](../stage_03_07_benchmark_note.md)
- Stage 03–06 benchmark notes.

## Imported Stage 03 deferral ledger

Stage 03 completed its correctness POC, but the canonical `S03-Q07` release
qualification row did not pass. Its children are tracked here until Stage 07
binds them to the exact release artifact:

| Transfer ID | Required result | Artifact/decision | Status |
| --- | --- | --- | --- |
| `S07-X03-01` | host/filesystem/architecture qualification matrix | — | `OPEN` |
| `S07-X03-02` | 64/256/1024 MiB × 1/16/64-root RSS/resource matrix | — | `OPEN` |
| `S07-X03-03` | matched five-minute baseline/candidate campaigns and three-invocation selection decision | — | `OPEN` |
| `S07-X03-04` | exhaustive corpus, long soak, restart storm and release variance | — | `OPEN` |
| `S07-X03-05` | release replay of real Stage 04 materialization/activation | — | `OPEN` |
| `S07-X03-06` | release replay of real Stage 05 packs/locators/GC/squash/destructive retention | — | `OPEN` |
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

Exact release revision, image digests, effective Linux
Engine/Desktop-VM kernel, `/eos` backing filesystem, mount/backend capability profile,
CPU architecture, corpus hashes, commands, raw artifact paths, thresholds,
distributions, and owner approvals must be attached. Architecture review is not
benchmark evidence and cannot support a universal or image-percentage compatibility
claim.
