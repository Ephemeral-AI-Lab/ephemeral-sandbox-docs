# Stage 04 benchmark note

Status: **NOT_RUN**.

[Stage 04.5](../stage_04_5_materialization_gc_alignment/benchmark_note.md)
supersedes this note for common publication, recovery/resource caps, old-generation
handoff, and peak-overlap qualification.

| Cell | Required measurement | Result |
| --- | --- | --- |
| cold reconstruction by `R,E` | elapsed, throughput, bytes read/written, peak RSS/FD/tasks | `NOT_RUN` |
| warm command/file/PTY | latency/tail and zero forbidden-work counters | `NOT_RUN` |
| activation by depth | plan time and final `D≤64` | `NOT_RUN` |
| already-materialized reuse | metadata-only work and zero payload write | `NOT_RUN` |
| same-key concurrent cold requests | active builds/waiters, duplicate staging bytes, selected generation | `NOT_RUN` |
| concurrent sessions | latency, lease/FD/mapping/upper bounds | `NOT_RUN` |
| shared generation scaling | carrier/page-cache sharing and per-session upper/work/execution bytes | `NOT_RUN` |
| inactive vs active MCTS forks | metadata, payload, materialization, upper bytes | `NOT_RUN` |
| generation switch overlap | current/old/building bytes and exact hold/handoff duration; no Stage 04 deletion | `NOT_RUN` |
| quota pressure | current/pinned keys, staging/upper bytes, rejection/backpressure, zero active eviction | `NOT_RUN` |
| crash matrix | old-or-new selection and residue | `NOT_RUN` |
| target matrix | glibc/musl/minimal/shell-less/read-only/non-root/amd64/arm64 | `NOT_RUN` |
| native backend matrix | Linux Engine/Desktop-VM kernel, filesystem, mount/capability result | `NOT_RUN` |

Use the exact Preparation 04 thresholds. Report command, revision, corpus digest,
environment, raw artifact, sample distribution, measured value, threshold, and
`PASS`/`FAIL`. The design's native route is a requirement, not evidence that it is
fast.
