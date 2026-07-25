# Stage 06 benchmark note

Status: **NOT_RUN / OPEN**.

Use [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)
without relaxation and reuse the
[Stage 05 campaign and artifact schema](../stage_05_retention_gc_packs/benchmark_note.md).
Stage 06 adds authority/parity dimensions; it does not add a second GC, retirement,
worker, memory, or lock budget.

## Required measurements

| Cell | Required inputs and measurement | Threshold | Result |
| --- | --- | --- | --- |
| forward import | `R,E`; bytes read/written/reused, build/verify/parity throughput, RSS, staging | streamed `O(R+E)` and Preparation 04 caps | `OPEN` |
| forward authority switch | GC idle/`Marking`/`Closing`; root-log append/fsync, GC-fence retry, writer-lock wait/hold, `CONTROL` pause | bounded metadata only under lock; no graph/parity scan | `OPEN` |
| full root log | log at cap during cutover/rollback | GC abort/backpressure latency, typed result, retained bytes | no skipped admission; bounded `ResourceExhausted` | `OPEN` |
| candidate public publication | 1/16/64 roots and foreground concurrency | Preparation 04 incremental throughput and p50/p95/p99/max tails | exact Stage 03/Preparation 04 gates | `OPEN` |
| cold authority rollback | `R,E`; v1 build/verify/publish, quiesce, switch pause | streamed `O(R+E)`; bounded switch section | `OPEN` |
| rollback peak space | candidate, v1, staging, materialization, metadata, source holds | Preparation 04 peak accounting; authoritative sources retained | `OPEN` |
| cutover/rollback failpoints | every root-log, fsync, rename, `CONTROL`, response boundary | complete old/new authority and exact retry | correctness prerequisite | `OPEN` |
| session/authority/retirement race | `Q`, long sessions, Stage 05 final rename | request tails, drain time, lock wait, fence retries, deadlock evidence | foreground gates; bounded quiesce; no deadlock | `OPEN` |
| re-cutover after v1 writes | changed bytes/paths, import and attribution reuse | catch-up cost and exact parity | required shape and space gates | `OPEN` |
| long-lived ownership | repeated cutover/rollback/cancel/restart | RSS slope; tasks, permits, FDs, mappings, holds, operation residue | Stage 05/Preparation 04 caps and quiescence | `OPEN` |
| environment/backend matrix | exact images, kernels, `/eos` filesystems, architectures, routes | supported cells pass; unsupported fail closed | `OPEN` |

## Campaign rules

- Compare GC-idle authority switching with the same foreground workload during
  `Marking`, `Closing`, and a bounded Stage 05 retirement rename.
- Cross 64/256/1,024 MiB inputs with 1/16/64 retained roots where authority work can
  vary with root size or retention.
- Run at least three matched repetitions per cell with the same revision, corpus,
  cache state, CPU placement, filesystem, limits, and available space.
- Report foreground p50/p95, diagnostic p99 when at least 100 samples exist, maximum,
  median absolute deviation, sample count, operations/second, and maintenance
  interference.
- Inject corruption, response loss, restart storms, cancellation, and `ENOSPC` at
  every authority/root-admission persistence boundary. Favorable timing never offsets
  a safety or cleanup failure.

Each result records the exact command, revision/build, corpus hash/seed, machine,
kernel, filesystem/provider, architecture, full configuration and caps, pair/run ID,
raw distribution, threshold, measured value, raw artifact path, cleanup result, and
`PASS`/`FAIL`/`OPEN`.

On-demand rollback's `O(R+E)` requirement is not a fixed wall-time promise for
unbounded roots. Missing evidence remains `OPEN`; no Stage 06 row may claim speed or
space safety from architecture alone.
