# Stage 07 benchmark and qualification note

Status: **NOT_RUN / OPEN**.

Stage 07 does not define new thresholds. It closes every required row in:

- [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)
- [overall Stage 03–07 scorecard](../stage_03_07_benchmark_note.md)
- Stage 03–06 benchmark notes.

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
