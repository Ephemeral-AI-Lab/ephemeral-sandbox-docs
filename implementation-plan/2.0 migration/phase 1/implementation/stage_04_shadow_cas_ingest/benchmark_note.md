# Stage 04 benchmark note — metadata-only shadow CAS ingest

[Overall Stage 03–11 scorecard](../stage_03_11_benchmark_note.md) ·
[Simplified storage contract](../layerstack_storage_contract.md) ·
[Specification](spec.md) · [E2E plan](e2e_test.md) ·
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Status: **NOT_RUN**

Stage 04 adds durable candidate metadata and native-carrier locators after the
authoritative v1 commit. It must not add a candidate reader, public authority,
or copied payload. Correctness, v1 authority, recovery, and cleanup failures
invalidate all performance samples.

## Stage-owned target and hard caps

- Normal capture plus shadow ingest is `O(U+K+C+V_delta)` plus bounded
  changed-event ordering, with `O(B)` application memory and no scan/rewrite
  proportional to unchanged tree or history size. A separately labeled first
  bootstrap may be `O(C_current+E_current+K_current)` and is never included in
  normal latency.
- SeqCDC remains `O(U+K)=O(U)` with one 32 KiB ring per active worker and no
  payload copy.
- Exactly four global workers; one borrowed chunk per worker, at most four
  globally and at most two slices per chunk; downstream payload queue `=0`.
- Metadata queue `<=16` items and `<=64 KiB`; encoder `<=256 KiB` per admitted
  operation; external merge fan-in `<=8` with `64 KiB` per run reader.
- Shared cache `<=4,096 * 4 KiB = 16 MiB`; managed memory
  `<=4 MiB/publication` excluding that cache; global permits `<=64 MiB`.
- Encoded metadata is `<=96 B/chunk`, `<=64 B/segment`, and
  `<=256 B + canonical path bytes/changed path`.
- Candidate payload writes, payload copies, payload staging, loose-object
  bytes, pack bytes, and `H_cold` are each exactly **zero**.
- At every publication boundary record allocated bytes, not logical file
  lengths: `C_capture + P_staging <= 1.05 * C_capture` (equivalently
  `P_staging <= 0.05 * C_capture`). `C_capture` is the immutable captured
  payload denominator; `P_staging` includes every publication/recovery staging
  allocation. Metadata remains separately visible in `M` and may not be hidden
  by changing the denominator.
- At clean settle there is no pending transaction or completed `work/` child;
  common-transaction residue is at most
  `1 MiB + min(1% of retained bytes, 64 MiB)`.
- Every operation is under 60 seconds; the tiny loop targets 30–60 seconds.

Command goals such as “exec minus 80 ms” are outside Stage 04 ownership.
Stage 06 and Stage 11 use the exact direct `docker exec … ls` control. Local
Stage 04 small-edit publication diagnostics use
`allowed = raw * (1 + p) + floor` and `raw*1.15+5 ms`. Five local pairs
cannot establish p95; Stage 11 owns normative latency, selection, RSS,
total-space, and portability gates.

| Required report field | Value frozen before the first candidate sample |
| --- | --- |
| frozen baseline | matched legacy-publication control; revision, profile, corpus, host, cache, and order fixed |
| required target/cap | exact v1 authority and candidate metadata, all payload-zero fields, `O(U+K+C+V_delta)` normal work, prior-tree scale coefficients, resource/space caps, and operation `≤60 s` |
| predeclared optimization target (recommended, non-normative) | small-edit shadow median `≤raw×1.10+2 ms` and complete tiny cycle `≤45 s` |
| candidate actual | `NOT_RUN` |
| delta / ratio / headroom | `NOT_RUN`; derive only from preserved matched samples |

## Frozen tiny evaluation matrix

Use seed `0x5A04`, one prebuilt binary, identical host/filesystem/cache/config
apart from rollout mode, and run-owned storage. Control is legacy publication;
candidate is the same v1 publication followed by `shadow_write`. First run one
labeled bootstrap per mode and exclude it. Then run exactly **one warmup pair
and five counterbalanced measured pairs**; one pair is a complete ordered
sweep of the cells below.

| Cell | Exact corpus/action | Control / candidate | Required raw metrics | Pass / fail |
| --- | --- | --- | --- | --- |
| `S04-NOOP` | pre-generated empty/no-op publish | legacy / `shadow_write` | elapsed, revision, root/txn deltas, skipped counter, physical delta | v1 unchanged; no candidate root/txn/allocation; skipped `+1` |
| `S04-LOCAL` | 1 KiB replacement in deterministic 1 MiB file | identical commit bytes | `U,C,K,V_delta`, scanned/hashed bytes, metadata/locator/fsync work, elapsed | exact candidate root/locators; work ledger complete; v1 remains sole authority |
| `S04-ENTROPY` | deterministic 1 MiB incompressible file | identical commit bytes | chunks, unique/reused/new locators, source and metadata bytes | exact IDs/ranges; every locator verifies against the v1 carrier |
| `S04-SMALL` | 256 files totaling about 1 MiB | identical canonical entries | entries/runs/merge records/pages, queue/cache/memory high-waters | exact root; bounded external ordering and every cap holds |
| `S04-HISTORY` | alternating 4 KiB edit and 64 KiB append at depths 1, 8, and 32 | identical history and operation order | depth, prior/current work, transactions/work, physical categories | normal samples exclude bootstrap; no history scan hidden in an unlabeled counter |

Every candidate sample must additionally report payload writes/copies/staging,
loose bytes, pack bytes, and `H_cold`; any nonzero value fails immediately.

### Required unchanged-prior-tree scale sweep

This structural sweep is separate from latency pairs and must run before a
complexity pass is claimed. Pre-generate candidate predecessors containing
exactly **1,024, 8,192, and 65,536 entries**. At each size, exclude one labeled
bootstrap, then apply the same 1 KiB replacement in the same deterministic
1 MiB file (`U`, changed entries, and resulting `K` fixed). Run **one warmup
plus three measured incrementals per size** in counterbalanced size order.

Freeze these local coefficients before candidate results:

```text
records_at_65536 <= 2 * records_at_1024 + 64
pages_at_65536   <= 2 * pages_at_1024 + 8
records_at_N     < N / 4  for every N
```

Record prior-tree records/pages/bytes read, current-event records, index
probes, merge passes, and elapsed time. These coefficients are a focused
sentinel for independence, not a new Prep percentile. Linear growth with
unchanged prior-tree cardinality, a full prior-tree scan, a missing counter,
or relabeling that work outside `V_delta` is **FAIL/OPEN**, not proof of
`O(U+K+C+V_delta)`. Disk-backed spill proves bounded memory but not
incremental time.

### Mandatory failure and recovery invocations

These cells are correctness/space gates and are not mixed into the latency
median. Each fault uses a fresh run-owned transaction, preserves the committed
v1 result, polls quiescence every 100 ms for at most 5 seconds, and retries the
same stable transaction/publication key exactly twice after recovery.

| Cell | Exact injection schedule | Required result and evidence |
| --- | --- | --- |
| `S04-F-CANCEL` | cancel at three positions: immediately after v1 commit before candidate admission; after `intent`; after `ready` before receipt install | request callback is fenced; v1 result is unchanged; candidate is absent or recovery-owned; two same-key retries converge to exactly one candidate root/receipt observation |
| `S04-F-ENOSPC` | fail allocation at metadata preflight, then fail one write after `intent` is durable and before visibility | typed shadow failure; no candidate visibility; v1 source is never removed; accounted residue is absent or bounded/recovery-owned |
| `S04-F-BACKPRESSURE` | hold both the 16-item/64 KiB descriptor queue and 64 MiB permit pool at capacity; freeze `backpressure_deadline_ms` from the candidate config in `1..=5,000` before the run | no unbounded producer work; typed `ResourceExhausted` occurs at the frozen deadline (record observed wait and headroom); all queue bytes/items and permits return to zero |
| `S04-F-IDEMPOTENT` | lose the response after durable completion, restart once, then submit the same stable key twice | every replay returns the same root/observation; root, locator `CURRENT`, receipt, and committed transaction each have multiplicity one; physical delta on the second retry is zero |
| `S04-F-CRASH-A` | crash once at each object, locator-SST, root, and `ready` durability boundary | restart replays or reaps exactly that transaction, never scans full history, and the two same-key retries converge once |
| `S04-F-CRASH-B` | crash once before/after locator `CURRENT`, `ready`, receipt rename, receipt parent `fsync`, and transaction cleanup | restart is idempotent, never double-installs a locator generation/root/receipt, and clean settle has no completed `work/` child |

The crash rows are driven by an exhaustive **18-position transaction boundary
manifest**, split into two independent invocations of nine positions:

1. intent write, intent fsync, metadata-object write, metadata-object fsync,
   metadata-object rename, locator-SST write, locator-SST fsync,
   locator-SST rename, and root write;
2. root fsync, root rename, locator `CURRENT` install, `CURRENT` parent fsync,
   `ready` write/fsync, receipt rename, receipt parent fsync, transaction
   cleanup/unlink, and cleanup parent fsync.

At each position, inject the operation failure once, capture the pre/post
durable state, restart when the boundary is durable, and run the two same-key
retries. A missing boundary, broad deletion, retry multiplicity above one,
unexplained allocation, or legacy mutation is `FAIL`.

## Raw evidence and decision

Each raw record includes revisions/build/config/seed/order, bootstrap flag,
v1 revision/hash, candidate root/status, `U/C/K/V_delta`, source read/scanned/hashed
bytes, cut/locator counts, prior/current tree records/pages/bytes, merge
runs/passes/fan-in, metadata/object/SST/transaction/ref bytes and fsyncs, elapsed
nanoseconds, all payload-zero fields, `L_hot/H_cold/U_active/P_staging/M`,
quarantine/unreachable/residue bytes, workers/tasks/queues/borrows/permits/FDs,
cache and managed-memory high-waters, quiescence, and cleanup.

The space record must preserve `C_capture`, `P_staging`, their allocated-byte
sources, numerator, denominator, ratio, and headroom to `1.05*C_capture` at
before/peak/settled boundaries. The dependency record must contain canonical
before/after arrays for resolved external `(name,version,source,checksum)`,
enabled external `(package,feature)`, and direct external
`(workspace_package,dependency,features,kind,target)` edges, plus Python,
system-tool, runtime-service, target-image-helper, and network requirements.
Every symmetric-difference array and every non-Rust requirement delta must be
present and have exact count `0`; missing evidence is `OPEN`, not zero.

Local pass requires exact v1 authority and candidate metadata, all zero-payload
invariants, the scale-sweep coefficients, every numeric resource/metadata
cap, no pending clean transaction, and explained bounded residue. Diagnostic
small-edit and raw-relative timings are reported without a p95 claim. Final
`>=10%` SeqCDC integrated advantage, total amplification/duplication/locality,
scale RSS, native read/hydration, and required-platform qualification are
deferred to Stage 11 (with hydration implemented first in Stage 05).

## Split wall-clock budget

These are **ESTIMATED planning values until measured**, not claimed results.
The scale fixtures are pre-generated outside timed publication intervals, but
their validation and labeled bootstraps are included here.

| Invocation | Included work | Estimated wall time |
| --- | ---: |
| `S04-CORE` | setup/bootstrap, warmup, five corpus pairs, three measurements at each prior-tree scale, cleanup/report | **30–49 s** |
| `S04-RECOVERY` | three cancellation points, two ENOSPC points, backpressure deadline, response loss, restart, and same-key retries | **30–90 s** |
| `S04-TXN-A` | transaction failpoints 1–9, restart/retry/quiescence per point | **90–210 s** |
| `S04-TXN-B` | transaction failpoints 10–18, restart/retry/quiescence per point | **90–210 s** |
| **Full healthy arrival bundle, four invocations** | aggregate only; never one runner invocation | **240–559 s** |

Do not add sleeps. Every operation remains below 60 seconds and each listed
invocation remains below 5 minutes. The ranges are scheduling estimates, not
acceptance bands: preserve an overrun and split only at the declared boundary
manifest before collecting new candidate data; never drop the 65,536-entry
structural point or a failpoint merely to hide a slope/overrun.

## Required arrival report

The run is not a Stage 04 arrival until
`.benchmark-state/results/<run_id>/stage-04-perf-report.json`
(`schema_version="phase1.stage04.perf-report.v1"`) and
`stage-04-perf-report.md` validate. They
must contain raw legacy/shadow samples, target/cap, delta/ratio/headroom,
`U/C/K/V_delta` and prior-tree work, memory/RSS, all physical categories, explicit
payload-zero fields, `C_capture+P_staging` numerator/denominator/headroom,
every failure/recovery/failpoint/retry cell, exact-zero dependency-delta arrays,
provenance, immutable run/raw links, cleanup, and a
`DIAGNOSTIC_PASS|FAIL|OPEN` verdict. Markdown renders the same JSON truth; this
does not qualify final Prep gates.

The first Markdown table must show the frozen baseline actual, required pass
target/cap, separately predeclared optimization target, candidate actual,
delta/ratio, headroom, and verdict for every stage-owned metric.

## Append-only progress

Append the exact command, intended cells, artifacts, and cleanup owner to the
shared E2E report before execution, then append the outcome here. Never replace
or delete prior rows. `QUALIFIED` is reserved for Stage 11.

| UTC | State | Run ID | Baseline → candidate actual | Required / optimization target | Delta / ratio / headroom | Report / raw artifacts | Cleanup / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | NOT_RUN | — | — | — | — | — | Freeze counters/deadline/failpoint manifest, then run `S04-CORE`, `S04-RECOVERY`, `S04-TXN-A`, and `S04-TXN-B` |
