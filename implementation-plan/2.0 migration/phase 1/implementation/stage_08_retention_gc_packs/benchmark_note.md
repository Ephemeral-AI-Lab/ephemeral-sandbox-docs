# Stage 08 benchmark note — retention, GC, and packs

[Specification](spec.md) · [E2E plan](e2e_test.md) ·
[Stage 03–11 scorecard](../stage_03_11_benchmark_note.md) ·
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Status: **NOT_RUN**

Preparation 04 gates are normative. The six-cell tiny schedule, the separate
cap-boundary extension, and their wall-clock budgets are benchmark policy
chosen to cover Stage 08 boundaries; they do not qualify final amplification,
RSS, or throughput. Stage 11 alone may report `QUALIFIED`.

Where a latency comparison is made, freeze matched raw LayerStack first:

```text
cap_ms      = raw_ms * (1 + allowed_percent) + floor_ms
delta_ms    = candidate_ms - raw_ms
headroom_ms = cap_ms - candidate_ms
```

Do not invent an absolute millisecond improvement target.

| Required report field | Frozen value before the first candidate sample |
| --- | --- |
| frozen baseline | matched maintenance-disabled control; revision/environment/corpus/order fixed |
| required target/cap | the Prep and Stage 08 limits below |
| predeclared optimization target (recommended, non-normative) | complete core loop `<=45 s`; settled pack dead/slack `<=1%`; native read/write throughput at least `1.00*raw` |
| candidate actual | `NOT_RUN` |
| delta / ratio / headroom | `NOT_RUN`; calculate only from preserved raw values |

## Owned target

| Surface | Required Stage 08 result |
| --- | --- |
| Complexity | Retain selection `O(R)` scan / `O(R log R)` comparisons externally; mark `O(V+E)`; sweep `O(A)`; pack append `O(B)`; evacuation `O(L_p)`; locator work expected `O(Q+U log pages)`. Every total-history structure is paged, externally merged, or cursor-bounded. |
| Pack/slice bounds | Pack at most 64 MiB payload, 100,000 records, 80 MiB allocated; seal before crossing any cap. One GC/compaction transaction at most 100,000 records or 64 MiB. |
| Trigger/grace correctness | Individual compaction at dead ratio `>=20%`; aggregate urgent when dead+slack ratio `>5%`; deletion only after at least one complete later durable epoch plus final root/generation/lease/locator recheck. |
| Local settled result | Focused unexplained persistent unreachable/unleased payload is exactly 0; no last locator or live/pinned/leased/root data is lost; normal command/file/PTY path performs zero CAS/pack lookup. |
| Hard resources | 32 KiB publication ring; one borrowed chunk/worker and at most 4 globally; downstream payload 0; 4 workers; 256 KiB pack-read/hydration buffer; queue 16/64 KiB; merge 8 x 64 KiB; encoder 256 KiB/op; cache 16 MiB; semaphore 64 MiB; native depth at most 64. |
| Local duration/release | Every operation/cell at most 60 s; quiescence polls every 100 ms for at most 5 s; case-owned tasks, buffers, readers, permits, cursors, staging, leases, and FDs return to warmed bounds. |

Stage 08 proves the algorithms and caps with exact byte/record/page/work
counters. Tiny elapsed time alone does not prove a complexity class.

## Tiny experiment/evaluation matrix

Use one pre-generated ~16 MiB mixed tree containing a localized edit,
repeated payload, incompressible payload, and 256 small files; histories
1/8/32; the complete root/transaction fixture below; the pinned OCI
index/platform digest; and identical seed/order/host/filesystem/cache/
configuration. Pair maintenance-disabled legacy control with candidate shadow
maintenance and counterbalance `AB/BA`.

Construct ratios with integer byte checks, avoiding rounded labels:
individual trigger is `dead*100 >= allocated*20`; aggregate urgent is
`(dead+slack)*100 > allocated*5`.

The durable mark fixture is mandatory and records one independent selection
reason per positive seed:

| Fixture node | Required mark behavior |
| --- | --- |
| current root | root is a seed; follow its complete manifest graph |
| root/carrier lease | leased root and the carrier/locator needed by the lease remain |
| explicit pin | pinned root is a seed |
| active branch head | branch root is a seed |
| configured-retention ancestor | ancestor is a seed because policy selects it, not because it is a parent |
| frontier root | frontier root is a seed |
| in-flight publication root | in-flight root is a seed |
| pending transaction roots/objects | every root or object named by a pending publication journal, hydration, materialization, evacuation, or compaction transaction is a direct seed |
| weak ancestry-only parent/base | not a seed; its graph becomes collectible after grace unless another reason above independently selects it |

For every selected root, root → complete tree manifest → metadata/segment/chunk
object references are **strong reconstruction edges**. Parent/base/provenance
IDs are **weak ancestry edges** and never retain history by themselves.
Materialization records separately retain only the carriers and locators
required by active backends.

| Cell | Candidate inventory/event | Repetitions | Raw metrics | Pass/fail |
| --- | --- | ---: | --- | --- |
| Warmup | depth 1, below both triggers | 1 pair, excluded | correctness/counters | exact read/tree and no trigger |
| C1 | depth 1, individual `<20%`, aggregate `<=5%` | 1 pair | selected packs, ratios, work | no compaction/urgent trigger |
| C2 | depth 8, individual exactly `20%`, aggregate `<=5%` | 1 pair | copied/live/dead/slack bytes | async compaction selected |
| C3 | depth 8, every individual `<20%`, aggregate `>5%` | 1 pair | scheduling and cursor work | urgent compaction selected |
| C4 | depth 32, first durable epoch with every positive seed above plus unreachable and weak-ancestry-only controls | 1 pair | seed reason, strong/weak edges, mark/sweep/trash/leases | every positive seed and its strong graph survive; weak ancestry is not implicitly marked; trash allowed but no premature unlink |
| C5 | next complete epoch plus final recheck | 1 pair | deleted/retained/unreachable bytes by seed reason | eligible unreachable and weak-only graph become 0; current/leased/pinned/branch/configured-ancestor/frontier/in-flight/pending roots and objects survive |
| C6 | last-locator evacuation with cancellation/recovery | 1 pair | locators/generations/journal/I/O | reconstructable throughout; caps hold |

Preserve raw ratios and medians; six pairs do not support normative p95. Run
the longer memory/reclamation sentinel separately: 3 warmups followed by 20
measured cycles in one daemon, with the dedicated restart-recovery case
excluded from slope inference.

## Exact cap-boundary extension

Status: **NOT_RUN**. Run these after the core diagnostic loop. Inputs are
pre-generated outside the timed interval. Each row isolates one cap: the other
two pack caps have documented slack, and transaction tests arrange for the
non-target transaction cap to remain below its limit. Preserve the admission
decision and the counters immediately before reservation, projected after
reservation, after sealing/cursor persistence, and after quiescence.

Pack constants are exact bytes:

```text
P_max = 64 MiB = 67,108,864 payload bytes
N_max = 100,000 records
A_max = 80 MiB = 83,886,080 allocated bytes
```

Let `a` be the measured filesystem allocation quantum. The live fixture
records `a`, `st_blocks*512`, and the writer's projected complete-pack
allocation including headers, index, and footer. For a 4 KiB quantum, the
allocation triplet below is exactly 83,881,984 / 83,886,080 / 83,890,176
bytes; for another quantum, use the exact `A_max-a / A_max / A_max+a`
representable triplet and report the numeric expansion.

| Pack case | State before reserving one complete next record | Projected state | Required result |
| --- | --- | --- | --- |
| `P-PAYLOAD-BELOW` | payload `67,108,862`; next payload `1` | `67,108,863` | `Append`; same pack remains ≤ cap |
| `P-PAYLOAD-AT` | payload `67,108,863`; next payload `1` | `67,108,864` | `Append`; exact cap is allowed, and no later positive-payload append may enter this pack |
| `P-PAYLOAD-CROSS` | payload `67,108,863`; next payload `2` | `67,108,865` | `SealBeforeAppend`; old pack stays at `67,108,863`, new pack starts with `2` |
| `P-RECORDS-BELOW` | records `99,998`; next record `1` | `99,999` | `Append` |
| `P-RECORDS-AT` | records `99,999`; next record `1` | `100,000` | `Append`; exact cap is allowed, and no later record may enter this pack |
| `P-RECORDS-CROSS` | records `100,000`; next record `1` | `100,001` | seal before append; new pack starts at one record |
| `P-ALLOC-BELOW` | projected complete allocation `A_max-2a`; next record consumes `a` | `A_max-a` | `Append` |
| `P-ALLOC-AT` | projected complete allocation `A_max-a`; next record consumes `a` | `A_max` | `Append`; exact cap is allowed, and no later allocating append may enter this pack |
| `P-ALLOC-CROSS` | projected complete allocation `A_max-a`; next record consumes `2a` | `A_max+a` | `SealBeforeAppend`; old pack remains `<=A_max`, new pack receives the record |

The live writer must agree with the pure admission oracle and no observed open
or sealed pack may exceed any cap. If a fixture cannot realize the declared
allocation triplet on the measured filesystem, the case is `OPEN`, not
silently rounded or treated as passing.

GC/compaction transaction constants are the same `67,108,864` payload bytes
and `100,000` records, whichever comes first:

| Transaction case | State before reserving next record | Projected state | Required result |
| --- | --- | --- | --- |
| `T-PAYLOAD-BELOW` | payload `67,108,862`; next payload `1` | `67,108,863` | admit into current transaction |
| `T-PAYLOAD-AT` | payload `67,108,863`; next payload `1` | `67,108,864` | admit exact cap and persist terminal cursor |
| `T-PAYLOAD-CROSS` | payload `67,108,863`; next payload `2` | `67,108,865` | persist cursor before the record; next transaction starts with `2` bytes |
| `T-RECORDS-BELOW` | records `99,998`; next record `1` | `99,999` | admit into current transaction |
| `T-RECORDS-AT` | records `99,999`; next record `1` | `100,000` | admit exact cap and persist terminal cursor |
| `T-RECORDS-CROSS` | records `100,000`; next record `1` | `100,001` | persist cursor before the record; next transaction starts at one record |

The record-first fixture uses one-byte payload records so it reaches 100,000
records far below 64 MiB. The payload-first fixture uses fewer than 1,000
records so it reaches 64 MiB far below 100,000 records. Recovery resumes at
the persisted cursor without skipping or revisiting a committed record.

### ESTIMATED wall-clock budget

Assume the binary is built and image is present. Build, image-pull, and
Cargo-lock time are separate. Replace estimates after the first measurement.

| Portion | ESTIMATED time |
| --- | ---: |
| fixture/setup and frozen fingerprints | 3–5 s |
| 1 warmup pair | 3–5 s |
| 6 measured cells | 24–36 s |
| quiescence and run-scoped cleanup | 6–10 s |
| report validation/write | 2–4 s |
| **core diagnostic loop subtotal (30–60 s lane)** | **38–60 s** |
| lifecycle shard A: 3 warmups + measured cycles 1–10, same daemon/run ID | **75–180 s** |
| lifecycle shard B: measured cycles 11–20, same daemon/run ID | **60–180 s** |
| dedicated restart-recovery case, excluded from slope | **27–64 s** |
| **lifecycle/recovery extension subtotal** | **162–424 s (2.7–7.1 min)** |
| **full healthy arrival bundle total** | **200–484 s (3.3–8.1 min)** |
| exact pack-cap invocation: nine `P-*` cases | **120–240 s (2.0–4.0 min)** |
| exact transaction-cap invocation: six `T-*` cases | **75–150 s (1.3–2.5 min)** |
| boundary artifact/schema validation | **10–20 s** |
| **boundary extension subtotal** | **205–410 s (3.4–6.8 min)** |
| **revised full Stage 08 cycle total** | **405–894 s (6.8–14.9 min)** |

These are scheduling estimates, not gates. Every operation/cell remains at
most 60 s and each quiescence wait at most 5 s; do not add arbitrary sleeps.
The core, lifecycle shard A, lifecycle shard B, recovery, exact pack-cap,
exact transaction-cap, and validation rows are separate invocations, each with
a hard five-minute watchdog. Lifecycle shard B must verify the same
run/gateway/daemon identity and the cycle-10 cursor before continuing; an
identity change invalidates the 20-cycle slope result.

## Final Prep gates carried to Stage 11

| Metric | Target | Hard failure |
| --- | ---: | ---: |
| mixed/no-dedup settled amplification | `<=1.08*D_ideal` | `>1.15*D_ideal` |
| many-small settled amplification | `<=1.15*D_ideal` | `>1.25*D_ideal` |
| avoidable native+pack duplicate | `<=1%` | `>3%` |
| settled pack dead/slack | `<=2%` | `>5%` |
| unexplained unreachable/unleased | 0 bytes | any persistent bytes |
| Phase-1 image matrix (Stage 11 only) | every required Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root row has pinned passing evidence | any required row failed or `unverified`; Stage 08 claims no qualification |

Stage 11 also qualifies publication/hydration 5% peak shapes, metadata limits
of 96 B/chunk, 64 B/segment, and 256 B plus path/changed path, RSS at most
384 MiB and 128 MiB above raw idle, and the 64/256/1,024 MiB x 1/16/64 roots
x 3 repetition matrix. Adjusted peak/final RSS spans at most 16 MiB; no 4x
scale step adds more than 8 MiB. Every operation remains at most 60 s and
every matched final invocation at most 5 min.

## Raw evidence and arrival report

Preserve pair/order, elapsed components, `R,V,E,A,B,L_p,Q,U`, boundary case
ID, allocation quantum, before/projected/after payload-record-allocation
counters, admission/seal/cursor decision, records/pages/comparisons/runs,
bytes read/written/scanned/copied/evacuated/deleted, pack payload/allocation/
live/dead/slack, every retention seed reason, strong/weak edge classification,
pending transaction root/object, locator/root/generation/epoch,
`L_hot,H_cold,sum(U_active),P_staging,M,C_current,H_unique,D_ideal`,
amplification/duplication/unreachable/trash/quarantine/lease-blocked bytes,
workers/buffers/queues/permits/cache/FDs, RSS/cgroup source, native route
counters, quiescence, recovery, and cleanup.

Stage 08 has not arrived until the run emits:

- `.benchmark-state/results/<run-id>/stage-08-perf-report.json`
  with `schema_version="phase1.stage08.perf-report.v1"`; and
- `.benchmark-state/results/<run-id>/stage-08-perf-report.md`.

Both reports link raw artifacts and contain frozen baseline, required
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
