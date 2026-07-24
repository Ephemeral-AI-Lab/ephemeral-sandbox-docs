# Stage 06 benchmark note

Status: **NOT_RUN**.

| Cell | Required measurement | Result |
| --- | --- | --- |
| forward import/cutover | `R,E`, build/verify time, quiesce and pointer pause | `NOT_RUN` |
| candidate public publication | Preparation 04 incremental/throughput/tail gates | `NOT_RUN` |
| cold authority rollback | `R,E`, throughput, quiesce, v1 build/verify time | `NOT_RUN` |
| rollback peak space | candidate, v1, staging, materialization, metadata bytes | `NOT_RUN` |
| cutover/rollback failpoints | old-or-new authority and exact retry | `NOT_RUN` |
| session/authority race | request tails, drain time, fence retries | `NOT_RUN` |
| re-cutover after v1 writes | catch-up cost and parity evidence | `NOT_RUN` |
| environment/backend matrix | exact images, effective Linux kernels, `/eos` backing filesystems, architectures, and route results | `NOT_RUN` |

Use [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)
without relaxation. Report commands, revision, corpus/images, raw artifacts,
distributions, threshold, measured value, and `PASS`/`FAIL`. On-demand rollback's
`O(R+E)` requirement is not a promise that it completes within a fixed wall time for
unbounded roots.
