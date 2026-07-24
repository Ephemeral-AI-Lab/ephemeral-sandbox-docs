# Stage 03 benchmark note — streaming scalar SeqCDC

[Overall Stage 03–11 scorecard](../stage_03_11_benchmark_note.md) ·
[Specification](spec.md) · [E2E plan](e2e_test.md) ·
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Status: **NOT_RUN**

This note tests only the Stage 03 primitive. It cannot qualify publication,
materialization, mount, command, file I/O, PTY, squash/remount, final space,
RSS, selection, or host portability. At this stage the primitive is dormant:
there is no candidate capture route, durable CAS root, materializer, native
carrier, mount, execution path, or squash path to time. Running those cells
would measure the unchanged legacy route and could not attribute a result to
SeqCDC. Their first mature component owners are Stage 05 (materialization),
Stage 06 (mount/command/file/PTY), and Stage 09 (squash/remount); Stage 11 owns
their statistically qualified end-to-end comparisons.

Correctness is a prerequisite: a fast sample with a cut, ID, ownership,
dependency, or cleanup mismatch is a failure.

## Stage-owned target

- Time is `O(U+K)=O(U)`: reading, scanning, and hashing are `O(U)`;
  callbacks are `O(K)`; jumps never rescan consumed input.
- For non-empty input,
  `ceil(U/32 KiB) <= K <= ceil(U/8 KiB)`; the final chunk may be shorter.
- Application memory is `O(B)`: exactly one ring of at most 32 KiB, one
  borrowed chunk with at most two slices, at most one live descriptor, and
  zero queued or copied downstream payload bytes.
- The scalar production cut core is at most 300 physical non-test Rust lines,
  safe and standard-library-only. The external package/version/feature/direct
  edge delta is exactly zero.
- Every operation is under 60 seconds and the complete tiny cycle targets
  30–60 seconds.

### Frozen identity and oracle

The benchmark is invalid unless the following literals are written to the run
manifest **before** the first candidate sample:

| Field | Exact frozen value |
| --- | --- |
| algorithm / mode | `seqcdc-scalar-author-v1` / `increasing` |
| profile | min `8,192`, target `16,384` (measurement target, not a cut-loop input), max/window `32,768`, sequence threshold `5`, opposing trigger `50`, jump `512` bytes |
| digest | domain-separated typed SHA-256 |
| chunk-object domain / format | ASCII `EOS-LS2\0`, one-byte `ObjectKind::ChunkPayload=3`, two-byte big-endian `ROOT_FORMAT_V2=2`, then the canonical big-endian payload length and exact payload bytes |
| author oracle | `UWASL/dedup-bench@8e2697cbf6332ac5da6dc615bfab82a720e820e4`, `dedup/src/chunking/seq_chunking.cpp` SHA-256 `d19548ac340a54edd5d6ac5f445f0d1fd7a31dbbdce4f6e243e115c81933cc9b` |
| author profile source | `build/config_16kb_middleware24/seqcdc_16kb.conf` SHA-256 `8dc85094530b052fb1a9b2f7e7510f8670e5473628b43c168fb4c759c319f6c0` |
| fixture authority | reviewed oracle output checked into append-only `cases.json`; candidate output can never create or update expected cuts or IDs |

The source and configuration digests are digests of the raw files at that
immutable revision. The report also records the checked-in fixture-manifest
digest; until that artifact exists its value is `NOT_RUN/OPEN`, never inferred
from candidate output.

The Prep latency gates are not owned here. Record raw elapsed time and
throughput, but do not claim an absolute “minus N ms” improvement. Where a
later raw-relative cap is shown diagnostically, calculate it as
`allowed = raw * (1 + p) + floor`; Stage 11 owns the normative percentile and
selection decisions.

| Required report field | Value frozen before the first candidate sample |
| --- | --- |
| frozen baseline | contiguous pinned-author oracle; revision, profile, corpus, host, cache, and order fixed |
| required target/cap | exact cut/ID equality, `O(U+K)=O(U)`, resource/code/dependency caps, and operation `≤60 s` |
| predeclared optimization target (recommended, non-normative) | candidate median throughput `≥0.95×` oracle and complete tiny cycle `≤45 s` |
| candidate actual | `NOT_RUN` |
| delta / ratio / headroom | `NOT_RUN`; derive only from preserved samples |

## Frozen tiny evaluation matrix

Use seed `0x5A03`, one prebuilt binary, one thread, the same host/cache/filesystem
state, and the same case order. A control feeds identical bytes contiguously
through the frozen author oracle. A candidate feeds them through the scalar
streaming scanner using the frozen fragmented-read schedules. One pair is one
complete ordered sweep of every cell. Run exactly **one warmup pair and five
counterbalanced measured pairs**; preserve all samples.

| Cell | Exact corpus | Control / candidate | Required raw metrics | Pass / fail |
| --- | --- | --- | --- | --- |
| `S03-BOUNDARY` | empty plus literal lengths 1, 8,191/8,192/8,193, 16,383/16,384/16,385, and 32,767/32,768/32,769 bytes | contiguous oracle / all small split points for literals, then repeated fragment vector `1,7,511,512,513,8191,8192,32768` | ordered cuts, IDs, byte coverage, comparisons, jumps, wraps | cuts/IDs exactly equal; offsets monotonic; no rescan; chunk-count bound holds |
| `S03-LOCAL` | deterministic 1 MiB base and a 1 KiB localized replacement | same bytes, contiguous / fragmented | input/scanned/hashed bytes, chunks, elapsed, bytes/s | exact oracle equality; scanned/hashed bytes equal input; all caps hold |
| `S03-ENTROPY` | deterministic 1 MiB incompressible bytes | contiguous / fragmented schedule generated by `0x5A03`, fragments in `1..=32,768` | elapsed, bytes/s, cuts, size distribution | exact equality and bounded memory; throughput is diagnostic only |
| `S03-TREE` | 256 files totaling about 1 MiB; source-like, mixed, and repeated bytes | concatenate each frozen file independently in canonical fixture order / same files and fragmentation | per-file and aggregate cut/ID digests, min/mean/p10/p50/p90/max sizes | exact equality; no cross-file state leakage |
| `S03-HISTORY` | overwrite depths 1, 8, and 32 using the same deterministic payloads | oracle / scanner at every depth | depth, bytes, chunks, cuts, owner/resource high-water | output is depth-independent for equal bytes; no retained owner |
| `S03-OPPOSING-JUMP` | exactly 9,000 bytes initialized to `0x00`; set byte 8,191 to `255`, bytes 8,192…8,241 to `254…205`, bytes 8,242…8,753 remain `0`, and bytes 8,754…8,758 to `1…5` | pinned contiguous author routine / whole, byte-at-a-time, and repeated fragment vector | comparison offsets, opposing counter, jump source/destination, first cut, ordered cuts/IDs | exactly 50 opposing comparisons trigger one jump from scan position 8,242 to 8,754; five increasing comparisons after the jump produce the pinned author cutpoint `8,758`; `jump_count=1`; candidate cuts/typed IDs are exact |

Inject `Interrupted`, source error, and visitor error once after the measured
matrix. They are unscored correctness cells: retry only `Interrupted`; every
terminal error stops further reads/callbacks and releases the ring and borrow.

## Raw evidence and decision

Each raw JSON record must include revision/build digest, literal algorithm/mode,
digest/domain/object-kind/format fields, pinned oracle revision/source/config/
fixture digests, profile parameters `8,192/16,384/32,768`, threshold `5`,
opposing threshold `50`, jump `512`, case/generator/seed/schedule/order, `U`,
`K`, cut and typed-ID digests, bytes
read/scanned/hashed, comparisons/jumps/wraps, elapsed nanoseconds, bytes/s,
ring/slice/descriptor/payload high-waters, error, and quiescence result.
Also preserve the code-line audit, dependency/feature/direct-edge inventory,
and source-boundary audit.

Local pass requires exact oracle identity in every sample, the complexity work
counters above, ring `<=32 KiB`, slices `<=2`, descriptor current `<=1`,
payload queue/copies `=0`, no introduced worker/task/thread/channel, and all
owners released. Distribution and throughput misses are retained diagnostics,
not a Stage 03 rejection of SeqCDC. Final mean/distribution, integrated
SeqCDC advantage `>=10%`, unique-payload `<=1.14x`, RSS/space, and required
platform rows are deferred to Stage 11.

## Full-cycle wall-clock budget

These are **ESTIMATED planning values until measured**, not claimed results.

| Phase | Estimated wall time |
| --- | ---: |
| Setup, fixture verification, binary/profile/dependency capture | 3–5 s |
| One full-corpus warmup pair | 3–5 s |
| Five measured full-corpus pairs, deterministic opposing/jump cell, and injected error cells | 20–32 s |
| Quiescence polling and exact run-owned cleanup | 2–4 s |
| JSON validation, summary, and append-only reporting | 2–4 s |
| **Complete tiny cycle** | **30–50 s** |

Do not add sleeps to reach 30 seconds. Any operation over 60 seconds fails.
The complete-cycle range is a scheduling estimate, not an acceptance band:
record a miss and revise the estimate; resize deterministic work only when
coverage is inadequate or an individual operation would breach its limit.

## Required arrival report

The run is not a Stage 03 arrival until
`.benchmark-state/results/<run_id>/stage-03-perf-report.json`
(`schema_version="phase1.stage03.perf-report.v1"`) and
`stage-03-perf-report.md` validate. They
must carry raw control/candidate samples, target/cap, delta/ratio/headroom,
work counters, memory/RSS, physical space, provenance, immutable run/raw
links, cleanup, and a `DIAGNOSTIC_PASS|FAIL|OPEN` verdict. The Markdown must
render the same JSON truth. This is diagnostic evidence, not final
qualification.

The first Markdown table must show the frozen baseline actual, required pass
target/cap, separately predeclared optimization target, candidate actual,
delta/ratio, headroom, and verdict for every stage-owned metric.

## Append-only progress

Before execution, append the exact command and artifact path to the shared E2E
report. Afterward, append the outcome here. Never edit or delete an older row;
append `Defect`, `Fix`, and `Rerun` rows so failed evidence remains visible.
`QUALIFIED` is reserved for Stage 11.

| UTC | State | Run ID | Baseline → candidate actual | Required / optimization target | Delta / ratio / headroom | Report / raw artifacts | Cleanup / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | NOT_RUN | — | — | — | — | — | Freeze oracle/fixture digests, then run `S03-BOUNDARY` through `S03-OPPOSING-JUMP` |
