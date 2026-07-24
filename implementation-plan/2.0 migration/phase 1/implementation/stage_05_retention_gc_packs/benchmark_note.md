# Stage 05 benchmark note

Status: **NOT_RUN**.

| Cell | Required measurement | Result |
| --- | --- | --- |
| disk-backed mark at growing `V` | time, temporary disk, RSS, run fan-in/FDs | `NOT_RUN` |
| streamed sweep at growing `A` | time slice, candidate/delete batch, request tail impact | `NOT_RUN` |
| concurrent mutation barrier | registrations, abort/restart count, mutation latency | `NOT_RUN` |
| pack build/lookup | throughput, run count/bytes, lookup reads/tail | `NOT_RUN` |
| locator consolidation | input/output bytes, write amplification, old/new overlap | `NOT_RUN` |
| last-locator evacuation | source/replacement overlap and final safety proof | `NOT_RUN` |
| trash/grace | candidate/trash bytes, grace duration, restore/resume residue | `NOT_RUN` |
| squash by `S,E_s` | build time/bytes, pointer pause, same-root proof | `NOT_RUN` |
| active-session squash | lease overlap and command/file/PTY latency tails | `NOT_RUN` |
| settled space | unique retained history, metadata, pack slack, unreachable residue | `NOT_RUN` |
| bounded ownership | RSS/tasks/workers/queues/FDs/mappings and zero detach/cycles | `NOT_RUN` |

Use [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)
thresholds exactly. Count mark runs and deletion candidates as staging; count locator
runs, outcomes, refs, operations, and directory overhead as metadata. Report the
absolute metadata floor separately when a ratio denominator is zero.

Every row requires commands, revision, corpus, environment, raw artifacts, threshold,
measured result, and `PASS`/`FAIL`. Bounded memory is not proof of incremental time.
