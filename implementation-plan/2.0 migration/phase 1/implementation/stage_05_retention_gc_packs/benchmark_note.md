# Stage 05 benchmark note

Status: **NOT_RUN / OPEN**. Architecture and asymptotic bounds are not benchmark
evidence. Destructive enablement remains `NO-GO` until every required correctness,
resource, time, and space row has a raw artifact and a passing verdict.

Normative thresholds come unchanged from
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md).
This note adds Stage 05 workload dimensions and accounting; it does not relax those
thresholds.

## 1. Variables and required shapes

- `V`: live logical objects; `A`: allocated objects/locator records; `E`: strong edges.
- `R`: logical root size; `S`: materialization size; `E_s`: squash reconstruction work.
- `P`: pack count; `L`: active locator-run count and encoded size.
- `Q`: concurrent foreground requests; `B`: configured RAM budget.
- `D`: active materialization depth; `G`: active/pinned generations.

| Operation | Required shape | Hard bound or foreground rule |
| --- | --- | --- |
| GC mark | `O(V + E + Sort(V + E))` | disk-backed `O(B)` RAM; no resident all-live set |
| sweep | sequential merge/sliced `O(A + V)` | fixed pages and candidate batches |
| pack creation | selected bytes and records | one admitted target; 64 MiB/100,000 records/80 MiB allocation |
| locator consolidation | selected runs and records | `L≤8`, encoded `CURRENT≤64 KiB`, merge fan-in 8 |
| lookup | deterministic loose lookup or at most `L` indexed probes | no historical-run scan |
| startup/recovery | current selectors plus capped nonterminal recovery pages | no total-history collection |
| squash | streamed `O(S + E_s)` | build outside bounded switch; `D≤64` |
| publication | Stage 03 incremental work plus bounded root-log append/fsync | no `O(V)`, `O(A)`, tree/history/locator scan |

`Sort` is measured external-sort/merge work; this plan does not claim a strictly
linear GC mark.

## 2. Required campaign matrix

Run matched baseline-versus-proposal campaigns. A baseline disables only the Stage 05
maintenance activity being measured while retaining the same revision, corpus,
foreground workload, cache state, limits, filesystem, CPU placement, and available
space.

Cross at least:

| Dimension | Required cells |
| --- | --- |
| configured RAM budget `B` | 64, 256, and 1,024 MiB; Stage 05 remains capped at `min(B,64 MiB)` |
| input/history scale | Preparation 04 64, 256, and 1,024 MiB cells, plus the larger object-count corpora below |
| simultaneously retained roots | 1, 16, and 64 |
| object count | large objects and many-small-object corpus of at least 100,000 files |
| graph | shallow, deeply shared, and high-edge-fanout |
| liveness | mostly live and mostly dead |
| physical layout | loose-heavy, pack-heavy, and mixed live/dead packs |
| readers | none and long-running old locator/materialization holds |
| mutations | idle, concurrent ref/checkpoint creation, and continuous publication |
| materialization | idle and concurrent materialize/squash |
| recovery | clean start, restart storm, corruption, and response loss |
| storage pressure | normal free space and `ENOSPC` at every write/fsync/rename boundary |

Use the deterministic Preparation 04 corpora and hashes. Add generated object-graph
corpora only when the existing corpus cannot express the graph dimension; record their
generator revision, seed, and hash.

## 3. Measurement ledger

| Cell | Inputs and workload | Required measurement | Threshold | Result |
| --- | --- | --- | --- | --- |
| disk-backed mark | `V,E,B`, sharing and live ratio | elapsed/CPU, bytes read/written, runs, merge passes, throughput, RSS, permits, queue, FDs | resource caps; RSS gates; required shape | `OPEN` |
| streamed sweep | `A,V`, loose/pack mix | scan/candidate throughput, slice duration, pause, restart cursor, foreground tails | fixed batches; no foreground scan; no operation over 60 s | `OPEN` |
| two-phase admission | `Q`, root-log fill, GC phase | append/fsync latency, writer-lock hold, retries, GC aborts, publication p50/p95/p99/max | small-edit and concurrency gates from Preparation 04 | `OPEN` |
| pack build | selected bytes/records | payload throughput, CPU, writes, allocation, source/target overlap | 64 MiB/100,000/80 MiB caps; peak-space gate | `OPEN` |
| lookup | loose/pack mix and `L=1..8` | probes, bytes/read amplification, p50/p95/p99/max | bounded by active `L`; warm paths meet Preparation 04 | `OPEN` |
| locator consolidation | selected runs/records | throughput, read/write amplification, merge passes, switch pause, old/new overlap | fan-in/run/encoded-pointer caps; peak-space gate | `OPEN` |
| evacuation | last legacy/external carrier | copied/verified bytes, throughput, source/target overlap, hold delay | source retained until verified selected replacement | `OPEN` |
| Two-cycle GC liveness | candidates across cycles `n,n+1` | cycle intervals, blockers, queue wait, time-to-reclaim, persistent residue | unexplained unreachable/unleased bytes = 0 after settle | `OPEN` |
| retirement ledger | path/byte batch and queue occupancy | rename/unlink throughput, per-slice and total lock pause, recovery time, bytes queued/renamed | 1,024 paths/64 MiB batch; 16-path/64-KiB lock slice; ledger 64/65,536/4 GiB | `OPEN` |
| squash | `S,E_s,D,G` | build throughput, switch/frozen pause, old-reader overlap, command/file/PTY tails | exact Preparation 04 squash/warm gates | `OPEN` |
| startup/recovery | incomplete operations/ledger at each cap | startup time, pages read, RSS, FDs, repair throughput | capped current state, not total history | `OPEN` |
| long-lived ownership | repeated pack/GC/evacuate/squash/cancel cycles | RSS slope, tasks, queues, permits, FDs, mappings, holds, residue | Preparation 04 quiescence/RSS gates; zero leaks | `OPEN` |

Maintenance throughput has no invented threshold. Record it, compare matched
distributions, and keep the result `OPEN` until an owner approves a release threshold.
No large operation may be reported only as “background”; record whether it is
asynchronous, sliced, backpressured, and its foreground p50/p95/p99/maximum effect.

## 4. Time and foreground-latency gates

Apply Preparation 04 exactly:

- warm resolve/session preparation p50 and p95 no worse than
  `baseline + 5% + 2 ms`, with zero CAS payload reads;
- squash frozen interval p50 and p95 no worse than
  `baseline + 5% + 2 ms`;
- full squash p50 and p95 no worse than `baseline + 10% + 5 ms`;
- no-op command p50 and p95 no worse than `baseline + 3% + 0.5 ms`;
- native command and sequential file throughput at least 97% of baseline;
- PTY gates unchanged;
- concurrent disjoint publication throughput at least 90% of baseline; and
- small-edit publication p95 no worse than `baseline + 15% + 5 ms`.

Report diagnostic p99 when at least 100 samples exist, maximum latency, median absolute
deviation, sample count, operations/second, payload throughput, lock wait/hold time,
maintenance slice time, and retry/backpressure counts. A maintenance slice entering a
command/PTY critical path, latency increasing with history, or an operation exceeding
60 seconds is a failure under Preparation 04.

## 5. Memory and resource gates

The complete Stage 05 caps in `spec.md` are assertions, not configuration suggestions.
At minimum record:

- absolute/adjusted peak and settled RSS;
- `min(B,64 MiB)` shared-byte-semaphore high-water mark;
- four-worker global high-water mark;
- metadata queue descriptors/bytes and same-key waiters;
- external-sort fan-in/buffers;
- per-operation/global FDs and zero mappings;
- active holds, operations, terminal records, retry attempts, root-log bytes, `W_gc`,
  retirement batches/paths/bytes, and `G`; and
- quiescent values after success, error, cancellation, panic, timeout, shutdown, and
  restart.

Run every `B=64/256/1,024 MiB × 1/16/64-root` cell and record that Stage 05 ownership
does not expand above `min(B,64 MiB)`. Independently, within each `B` campaign run
Preparation 04's 64/256/1,024 MiB input/history × 1/16/64-root scale cells. For three
repetitions at every input/history-size point, use the matched idle baseline. Adjusted
final and peak RSS must each vary by at most 16 MiB across the size series; no 4×
input/root increase may add more than 8 MiB to either median; every point remains at
most 384 MiB absolute and 128 MiB above idle.

## 6. Space and write-amplification accounting

Record separately:

- unique logical payload;
- loose-object payload and overhead;
- pack payload, slack, dead bytes, footer/index metadata;
- locator runs and selectors;
- duplicate old/new generation overlap;
- active and previous GC mark/root-log/candidate work;
- retirement trash;
- operation/build staging;
- current, pinned, and old-reader materialization generations;
- abandoned-operation residue; and
- unreachable bytes split by an explicit blocking reason.

Let `T_build` be the one admitted replacement, `H_gen` held old locator/
materialization bytes, `H_gc≤W_gc` active plus prior GC work, and `H_trash` the bounded
retirement batch. Measure every term in:

```text
peak <= settled + T_build + H_gen + H_gc + H_trash
```

The inequality and admission rejection are verified at the preflight boundary and at
the observed peak. Test the worst case with long readers, restart recovery, and
`ENOSPC`. No authoritative source may be deleted to make room for an unverified
target.

Preparation 04 settled gates remain exact:

- mixed tree and no-dedup binary target `≤1.08 × D_ideal`, hard failure
  `>1.15 × D_ideal`;
- many-small-file target `≤1.15 × D_ideal`, hard failure
  `>1.25 × D_ideal`;
- avoidable current-native-plus-pack duplication target `≤1%`, hard failure `>3%`;
- settled pack slack/dead bytes target `≤2%`, hard failure `>5%`; and
- persistent unexplained unreachable/unleased payload must be zero;
- native lower depth remains preemptively below 64 and must never exceed 64; and
- metadata remains within the Preparation 04 amortized budgets: at most 96 bytes per
  chunk for pack/footer/index metadata, 64 bytes per file segment reference, and
  256 bytes plus canonical path bytes per changed-path record.

Report bytes read, written, copied, evacuated, renamed, unlinked, and write
amplification for pack, consolidation, evacuation, GC, retirement, recovery, and
squash. Long-reader-protected bytes remain in total physical accounting and must be
explained rather than hidden.

## 7. Raw artifact schema and verdict

Every result row must include:

- exact command and source revision/build;
- corpus/generator ID, hash, seed, and retained-root manifest;
- machine, CPU placement, memory, architecture, OS/kernel, filesystem/mount/provider,
  and available disk;
- full configuration and every applicable cap;
- baseline/proposal pair/run ID and execution order;
- sample count and raw distribution;
- threshold and measured value;
- fault schedule and recovery/cleanup outcome;
- raw artifact path; and
- `PASS`, `FAIL`, or `OPEN`.

The verifier rejects missing accounting instead of treating it as zero. Correctness,
crash-safety, corruption, leak, or cap failures force `FAIL` regardless of favorable
latency or space. Unmeasured cells remain `OPEN`; architectural reasoning never
converts them to `PASS`.
