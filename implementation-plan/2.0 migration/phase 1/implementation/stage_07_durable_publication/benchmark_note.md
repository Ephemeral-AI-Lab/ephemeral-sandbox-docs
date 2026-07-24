# Stage 07 benchmark note — durable candidate publication

[Specification](spec.md) · [E2E plan](e2e_test.md) ·
[Stage 03–11 scorecard](../stage_03_11_benchmark_note.md) ·
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Status: **NOT_RUN**

Preparation 04 gates are normative. The tiny sample count, cell schedule, and
wall-clock budget are stage-local benchmark policy and do not qualify p95.
Stage 11 alone may report `QUALIFIED`.

Freeze a matched raw LayerStack baseline before candidate data and calculate
each latency cap independently:

```text
cap_ms      = raw_ms * (1 + allowed_percent) + floor_ms
delta_ms    = candidate_ms - raw_ms
headroom_ms = cap_ms - candidate_ms
```

No absolute “minus N ms” target is justified until measured baseline and
candidate values exist.

| Required report field | Frozen value before the first candidate sample |
| --- | --- |
| frozen baseline | matched legacy-publication samples; revision/environment/corpus/order fixed |
| required target/cap | the Prep formulas in “Final Prep gates” below |
| predeclared optimization target (recommended, non-normative) | small-edit p95 `<=raw*1.10+2 ms`; disjoint throughput `>=0.95*raw`; staging `<=3%` of `C_capture` |
| candidate actual | `NOT_RUN` |
| delta / ratio / headroom | `NOT_RUN`; calculate only from preserved raw values |

## Owned target

| Surface | Required Stage 07 result |
| --- | --- |
| Authority/correctness | The public legacy result is unchanged; a distinct private branch commits one atomic root/head. Stable-request retry returns the exact receipt; disjoint writers merge, conflicts/stale generations reject, and recovery is deterministic. |
| Complexity | Capture/chunk/durabilize `O(U+E+K)`, with `ceil(U/32 KiB)<=K<=ceil(U/8 KiB)`; OCC/root diff `O(Q log N)` plus bounded result output; head swap `O(1)`; lost-response retry is metadata-only; no whole capture/tree/history is retained in memory. A full-root or full-index sequential scan is not an accepted Stage 07 alternative. |
| Peak/settled space | One capture only; transaction staging at most `5%` of `C_capture`. Terminal journal residue at most `1 MiB + min(1% retained payload, 64 MiB)` and no pending transaction. |
| Hard resources | 32 KiB ring; at most 4 workers/borrowed chunks; downstream payload 0; queue 16/64 KiB; merge 8 x 64 KiB; encoder 256 KiB/op; cache 16 MiB; semaphore 64 MiB; managed memory at most 4 MiB/publication excluding cache; RSS at most 384 MiB and 128 MiB above raw idle. |
| Local duration/release | Each operation at most 60 s; quiescence polls every 100 ms for at most 5 s; no transaction, worker, queue, permit, capture handle, staging, pending journal, or extra FD remains. |

Record `U,E,K,Q,N`, OCC index-page probes/comparisons, bounded result records
and bytes, manifest-merge comparisons/runs, bytes scanned/hashed/reused/newly
retained, and retries. Structural bounds plus these counters must demonstrate
`O(Q log N)` OCC work independently from any bounded external ordering used to
construct the manifest.

## Tiny experiment/evaluation matrix

Use seed `0x5A07`, pinned OCI index/platform digest, pre-generated inputs, one
unchanged packaged daemon, and matched host/filesystem/cache/configuration.
The control is legacy publication only; the candidate is the same admitted
frozen stream plus `candidate_publish_private`. Counterbalance `AB/BA`. Every
candidate arm uses a unique stable request, immediately retries it, and
materializes/compares the committed private root.

| Cell | Corpus/history and required event | Repetitions | Raw metrics | Pass/fail |
| --- | --- | ---: | --- | --- |
| Warmup | no-op then localized edit | 2 pairs, excluded | correctness/receipt only | both authorities exact |
| C1 | empty/no-op, depth 1, stable retry | 1 pair | elapsed components, pages, receipt | retry is exact and metadata-only |
| C2 | 1 KiB edit in deterministic 1 MiB, depth 1, disjoint writers | 1 pair | scanned/new bytes, throughput, OCC | merge exact; no lost update |
| C3 | 1 MiB incompressible, depth 8, conflict | 1 pair | `U/E/K/Q/N`, I/O, conflict work | typed conflict; no head mutation |
| C4 | 256 small files (~1 MiB), depth 8, pre-commit cancellation | 1 pair | metadata/queue/journal/resources | no visibility; recovery terminal |
| C5 | localized edit, depth 32, lost-response retry | 1 pair | phase times, reuse, receipt lookup | one root and identical receipt |
| C6 | full deterministic bundle, depth 32 | 1 pair | memory/space/resource high-waters | exact tree; every cap holds |

Six measured pairs support raw ratios/medians only. The separate stability
sentinel runs 12 post-warmup candidate lifecycles containing successes,
retries, a disjoint pair, a conflict, and a cancellation.

### ESTIMATED wall-clock budget

Assume the binary is built and pinned image is local; report build, image
pull, and Cargo-lock wait separately. Replace estimates after the first run.

| Portion | ESTIMATED time |
| --- | ---: |
| fixture/setup and frozen fingerprints | 3–5 s |
| 2 warmup pairs | 5–8 s |
| 6 measured pairs | 24–34 s |
| quiescence and run-scoped cleanup | 4–8 s |
| report validation/write | 2–4 s |
| **core diagnostic loop subtotal (30–60 s lane)** | **38–59 s** |
| separate 12-lifecycle/recovery extension | **75–180 s** |
| **full healthy arrival bundle total** | **113–239 s** |

The estimates are not acceptance thresholds. The tiny loop target and every
operation are at most 60 s; each quiescence poll stops at 5 s.

## Final Prep gates carried to Stage 11

| Metric | Normative final gate |
| --- | --- |
| small-edit publication | p95 `<= raw*1.15+5 ms`; scanned and newly retained bytes reported |
| concurrent disjoint publication | throughput at least `0.90*raw` with exact OCC |
| publication peak | `C_capture + P_staging <= 1.05*C_capture` |
| metadata | at most 96 B/chunk, 64 B/segment, and 256 B plus path bytes/changed path |
| memory scaling | 64/256/1,024 MiB x 1/16/64 roots x 3 reps; adjusted peak/final span at most 16 MiB and no 4x scale step adds more than 8 MiB |
| strict-read regression | all Stage 06 warm/mount/exec/file/PTY/native-route gates still pass |
| duration | each operation at most 60 s; each matched final invocation at most 5 min |
| portability (Stage 11 only) | every required-release host/image row passes with pinned evidence across Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root fixtures; Stage 07 claims no matrix qualification |

The local small-edit and 90% lines are diagnostics; final percentile,
throughput, scale, and corpus qualification stays in Stage 11.

## Raw evidence and arrival report

Preserve every pair/order and raw phase time; request/branch/publication/root/
generation/receipt; OCC attempts/outcome; `U,E,K,Q,N`; bytes
captured/scanned/hashed/reused/written/newly retained; operations/s; pages,
merge runs/comparisons, journals/leases; worker/queue/buffer/permit/cache/FD
high-waters; RSS/cgroup source; `L_hot,H_cold,sum(U_active),P_staging,M`;
authority, digest, recovery, quiescence, and cleanup.

Stage 07 has not arrived until the run emits:

- `.benchmark-state/results/<run-id>/stage-07-perf-report.json`
  with `schema_version="phase1.stage07.perf-report.v1"`; and
- `.benchmark-state/results/<run-id>/stage-07-perf-report.md`.

Both reports link raw artifacts and include the frozen baseline, required
target/cap, predeclared optimization target, candidate actual,
delta/ratio/headroom, work counters, memory/RSS, physical space, provenance,
missing values, and a `DIAGNOSTIC_PASS|FAIL|OPEN` verdict. Update this tracker and
append the exact command plus `Good`/`Defect`/`Fix`, artifact custody, and
run-scoped cleanup to
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`.

The first Markdown table must show the frozen baseline actual, required pass
target/cap, separately predeclared optimization target, candidate actual,
delta/ratio, headroom, and verdict for every stage-owned metric.

## Append-only progress

| UTC | State | Run ID | Baseline → candidate actual | Required / optimization target | Delta / ratio / headroom | Report / raw artifacts | Cleanup / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | NOT_RUN | — | — | — | — | — | Freeze the first pair before execution |
