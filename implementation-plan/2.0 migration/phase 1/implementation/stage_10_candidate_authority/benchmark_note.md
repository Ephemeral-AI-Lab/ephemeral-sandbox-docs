# Stage 10 benchmark note — candidate authority

[Specification](spec.md) · [E2E plan](e2e_test.md) ·
[Overall Stage 03–11 scorecard](../stage_03_11_benchmark_note.md) ·
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Status: **NOT_RUN**

Stage 10 owns the first candidate-authority exercise, ordered legacy shadow,
and explicit verified read rollback. It remains a POC diagnostic stage: it
cannot enable the default, retire legacy state, or qualify final performance.

| Required report field | Value frozen before the first candidate sample |
| --- | --- |
| frozen baseline | matched legacy-authority publication/read route; revisions, corpus, host, cache, authority state, and order fixed |
| required target/cap | exact single-writer authority, ordered shadow parity, verified rollback, native hot path, stage-owned complexity/resources, release, and operation `≤60 s` |
| predeclared optimization target (recommended, non-normative) | native hot-path median `≤raw`, small-edit publish median `≤raw×1.10+2 ms`, and complete local bundle `≤100 s` |
| candidate actual | `NOT_RUN` |
| delta / ratio / headroom | `NOT_RUN`; derive only from preserved matched samples |

## Owned targets

| Area | Required local result |
| --- | --- |
| Authority | Exactly one writer: candidate root-catalog CAS is the publication linearization point; retry returns the same receipt/root generation |
| Normal reads | Candidate strict route only; `fallback_count=0` and `mismatch_count=0`; corrupt or missing candidate data fails closed |
| Legacy shadow | One-way, ordered, generation-correlated apply; cursor reaches current candidate generation and exact tree parity |
| Rollback | Explicit quiesced read-route switch only at verified parity; candidate remains sole publication authority; a publish during rollback is fenced until shadow parity |
| Retention | Candidate and declared legacy shadow bytes remain policy-owned; no legacy code, config, reader, writer, or artifact is retired |
| Complexity | Candidate publication remains `O(U+E+K)` plus bounded external ordering; authority CAS/retry is bounded catalog work; warm activation is `O(D)` with `D≤64`; shadow is linear in declared change/carrier work plus the v1 write; rollback is `O(A×remount)`; recovery is linear in declared journal/catalog work |
| Native hot path | Command/file/PTY/stdin use native carriers with zero CDC/CAS/pack work |
| Bounded resources | 32 KiB ring; 4×256 KiB worker buffers; queue 16 descriptors/64 KiB; encoder ≤256 KiB; cache ≤16 MiB; ≤4 MiB/publication; 64 MiB semaphore |
| Local timing | Every operation/cell ≤60 s; record raw phase times and median only. All p50/p95, RSS-scale, amplification, and release verdicts remain Stage 11 |
| Portability boundary | Stage 10 records the focused pinned-Ubuntu capability result only. Stage 11 must qualify the complete Prep 04 required-host matrix and pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root image cells; an unverified required-release row blocks retirement. |

## Concrete tiny evaluation matrix

Use a deterministic ~16 MiB mixed tree, depths 1/8/32, root counts 1/8, one
active root, and one retained old root. The minimum counterbalanced schedule
is `A,B,C,D,E`: one unscored global warmup and five legacy-control/candidate
pairs. Prefer 3 warmups and ten pairs only if the whole developer loop remains
30–60 seconds. Cell F is an exact fault suite, not a substitute for a pair.

| Cell | Frozen control and candidate | Warmups / measured | Raw metrics | Pass / fail |
| --- | --- | --- | --- | --- |
| A — changed publish | `D=1`, 1 root; legacy authority control versus candidate authority+shadow | global 1 / 1 pair | publication phases, receipt/root/authority generations, scanned/new/reused bytes | one candidate commit and receipt; exact shadow parity |
| B — no-op/retry | `D=8`, 8 roots; repeat request across lost-response/restart boundary | global 1 / 1 pair | CAS attempts/conflicts, IDs, journal terminal state | stable `PublicationId` and root generation; retry adds zero payload |
| C — strict read/maintenance | `D=32`, 8 roots; read/exec, then one bounded pack or materialization maintenance action | global 1 / 1 pair | routes, fallback/mismatch, depth/pack counters, read/exec time | candidate strict, fallback/mismatch 0; Stage 08/09 limits unchanged |
| D — verified rollback | current candidate and caught-up legacy cursor; active session | global 1 / 1 pair | cursor/digest, authority/read epochs, remounts, leases | read route changes only after parity/quiescence; writer stays candidate |
| E — publish during rollback | legacy read route active; issue one changed candidate publication | global 1 / 1 pair | fence time, shadow lag/apply/verify, restored route | publish is ordered; read advancement waits for parity; candidate strict is restored |
| F — fail closed | corrupt/missing candidate object; stale or gapped shadow cursor; restart at authority/shadow transitions | 0 / 1 exact call per fault | error enum, route and authority counters, recovery work | no silent fallback, stale rollback, second writer, or partial visibility |
| G — authority sentinel | one daemon runs publish/no-op, strict read/exec, shadow, periodic squash/pack, selected rollback, destroy | 3 / 20 cycles, with equal-warmup control | 100 ms resource/RSS/space stream, cursor lag, first/last 5-cycle medians and slope | all logical owners release; shadow caught up; candidate route restored; unexplained bytes 0 |

Pre-generate payloads and freeze seed, image/platform, host allocation,
filesystem, cache class, operation order, and config except the route factor.
Poll quiescence every 100 ms for at most 5 s. At settle: no case-owned
session/execution/publication/shadow/maintenance transaction remains; shadow
has zero gaps and current cursor; queues and borrowed chunks are zero; four
workers and the 64 MiB semaphore are within bounds; only declared durable
roots/leases/grace remain.

### Planning wall-clock budget — ESTIMATED, not measured

| Work | Core tiny loop | 20-cycle sentinel | Full local bundle |
| --- | ---: | ---: | ---: |
| fixture/config/setup | 4–7 s | 4–7 s | 8–14 s |
| warmups | 4–8 s | 3–6 s | 7–14 s |
| measured cells/cycles | 17–32 s | 20–40 s | 37–72 s |
| quiescence/cleanup | 2–7 s | 5–13 s | 7–20 s |
| artifact/report write | 3–6 s | 3–6 s | 6–12 s |
| **Total** | **30–60 s** | **35–72 s** | **65–132 s (plan 65–135 s)** |

These are healthy-run scheduling estimates, not relaxed limits. Every
operation/cell remains ≤60 s and any final matched invocation remains ≤5 min.

## Raw evidence and arrival checkpoint

Keep every sample and record:

- capture/chunk/hash/index/write/fsync/root-CAS/activation/shadow/apply/verify/
  rollback-remount/read/exec/maintenance/cleanup times;
- root, publication, receipt, authority, read-route, materialization, and
  shadow-cursor IDs/generations plus exact tree digests;
- CAS retries/conflicts, shadow lag/gaps, fallback/mismatch and route deltas;
- scanned/read/written/copied/reused/new bytes and all logical/allocated
  candidate, legacy, staging, grace, pack, trash, quarantine, and unexplained
  physical categories;
- workers, buffers, queues, permits, leases, transactions, mappings/FDs,
  cache, quiescence latency, RSS source/scope, and first/last slope evidence;
- revisions/dirty state, binary/config digests, host, image/platform,
  filesystem/mount, corpus/seed/order/cache, and
  `measured|derived|estimated|unknown` provenance.

Stage 10 has not arrived until
`.benchmark-state/results/<run-id>/stage-10-perf-report.json` and
`stage-10-perf-report.md` exist with
`schema_version="phase1.stage10.perf-report.v1"` and contain the frozen
baseline actual, required pass target/cap, separately predeclared optimization
target, candidate actual, delta/ratio/headroom, complexity and work counters,
memory/RSS, complete physical-space terms, links between the reports and to
run/raw artifacts, provenance, and verdict. Allowed terminal verdicts are
`DIAGNOSTIC_PASS` or `FAIL`; never `QUALIFIED`.

The first Markdown table must show the frozen baseline actual, required pass
target/cap, separately predeclared optimization target, candidate actual,
delta/ratio, headroom, and verdict for every stage-owned metric.

## Append-only progress

Before each live command, append the exact command, intent, expected authority/
shadow/cleanup evidence, ownership, and rollback to
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`.
Afterward append `Good` or `Defect`, artifact IDs, misses, and cleanup; append
later `Fix` and `Rerun` entries rather than rewriting history. Then update the
overall scorecard and append a row here.

| UTC | State | Run ID | Baseline → candidate actual | Required / optimization target | Delta / ratio / headroom | Report / raw artifacts | Cleanup / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | NOT_RUN | — | — | — | — | — | Freeze the first cell before execution |
