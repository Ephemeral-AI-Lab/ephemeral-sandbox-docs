# Stage 05 benchmark note — private candidate materialization

[Overall Stage 03–11 scorecard](../stage_03_11_benchmark_note.md) ·
[Specification](spec.md) · [E2E plan](e2e_test.md) ·
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Status: **NOT_RUN**

Stage 05 proves private, crash-atomic candidate hydration while public legacy
authority remains unchanged. It does not prove candidate activation, mount,
native command/file/PTY performance, publication, retention, or final
qualification. Any tree, authority, integrity, atomicity, recovery, or cleanup
failure invalidates performance.

## Stage-owned target and hard caps

- Warm `ensure` is expected `O(1)` / bounded `O(log pages)`, metadata-only,
  with exactly zero CAS payload reads and no allocated-byte growth.
- Cold hydration is `O(R+E+K)=O(R+E)`; streamed tree verification is
  `O(R+E)`; no complete tree/chunk list is resident.
- Read and output buffers are each `<=256 KiB/worker`; there are at most four
  global workers; metadata queue is `<=16` and `<=64 KiB`; encoder is
  `<=256 KiB/operation`.
- Shared cache is `<=16 MiB`; managed memory is `<=4 MiB/operation` excluding
  that cache; global permits are `<=64 MiB`.
- Candidate carrier physical peak is `<=C_target+5%`; no partial carrier is
  visible. RSS is `<=384 MiB` absolute and `<=128 MiB` above idle, with logical
  release mandatory.
- Every operation and the planned tiny invocation are under 60 seconds.

There is no justified absolute “materialization minus 10 ms” target. Compare
against the matched raw control: diagnostic warm cap
`raw*1.05+2 ms`, cold throughput `>=0.70*verified native-copy rate`, and cold
activation p95 `<=1.5*native-copy time + warm allowance`. Six pairs cannot
qualify p95; those latency/throughput lines and the final scale campaign belong
to Stage 11.

| Required report field | Value frozen before the first candidate sample |
| --- | --- |
| frozen baseline | matched legacy-tree oracle and verified native-copy control; revisions, image/platform, corpus, host, cache, and order fixed |
| required target/cap | exact atomic tree/metadata result, `O(R+E+K)=O(R+E)`, warm zero-payload work, carrier/resource/RSS caps, release, and operation `≤60 s` |
| predeclared optimization target (recommended, non-normative) | warm-ensure median `≤raw×1.03+1 ms`, cold hydration `≥0.80×` verified native-copy throughput, and complete tiny cycle `≤45 s` |
| candidate actual | `NOT_RUN` |
| delta / ratio / headroom | `NOT_RUN`; derive only from preserved matched samples |

## Frozen tiny evaluation matrix

Use seed `0x5A05`, the pinned Ubuntu image/platform manifest, one prebuilt
binary, identical host/filesystem/cache protocol, input manifest, and
counterbalanced order. A control derives the exact legacy tree digest and
performs verified same-filesystem native sequential copy. A candidate forces
cold hydration into a fresh run-owned generation, verifies it, then performs
one warm `ensure`. Run exactly **two warmup pairs and six measured alternating
pairs**; one pair is a complete ordered sweep of all cells.

| Cell | Exact corpus | Control / candidate | Required raw metrics | Pass / fail |
| --- | --- | --- | --- | --- |
| `S05-EMPTY-BOUNDARY` | empty root; short file; 8/16/32 KiB boundary files | legacy digest + verified copy / cold hydrate, verify, warm ensure | `R,E,K`, phase times, payload reads, carrier allocation | exact tree; atomic generation; warm payload reads `=0` |
| `S05-LOCAL` | 1 KiB replacement in deterministic 1 MiB file | identical logical tree | cold bytes/time/rate, copy bytes/time/rate, index reads, fsyncs | exact content/metadata; `O(R+E+K)` work ledger |
| `S05-ENTROPY` | deterministic 1 MiB incompressible file | identical bytes | chunks, sequential reads/writes, buffers, elapsed | exact hash/tree; bounded buffers/workers/permits |
| `S05-SMALL-META` | 256 files totaling about 1 MiB; modes `0640`/`0751`; owners `0:0` and `1234:2345`; mtime `1,700,000,005 s + 123,456,789 ns`; raw xattrs `user.phase1=00 01 02 ff` and `user.empty=<zero bytes>`; one two-path hardlink group; one raw-byte symlink target; whiteout/opaque transition inputs; one 1 MiB sparse file with two 4 KiB data extents | legacy oracle / private candidate | entries, content/canonical metadata digest, `(mode,uid,gid,mtime_seconds,mtime_nanoseconds,xattr-name/value,hardlink-group,symlink-target,sparse-extents)` values, queue/cache/FD high-water | exact bytes and every metadata field; hardlink paths share the declared group/native inode; transition inputs produce the exact final tree; no partial visibility |
| `S05-HISTORY` | the frozen payloads at root depths 1, 8, and 32 | matched roots in identical order | depth, index pages, cold and warm phase work | warm work does not grow with payload bytes; zero mismatch |

The core timing invocation contains no injected fault. Cancellation, crash, disk
full, corruption, and transaction-boundary faults run in the separate recovery
invocations below so recovery time cannot contaminate the cold/warm medians.

Run a second lifecycle submatrix after warmup: exactly **12 candidate
lifecycles**, alternating success and that declared cancellation (six each) at
fixed positions. Sample every 100 ms and poll for quiescence for at most
5 seconds after each. Freeze the control noise band as
`max(8 MiB, 4 * control MAD)`.

### Mandatory recovery and failpoint matrix

Use a fresh run-owned generation per injection, poll every 100 ms for at most
5 seconds, restart only where declared, and retry the same
`MaterializationKey` exactly twice. The matrix is untimed correctness/space
evidence:

| Cell | Exact injections | Required result |
| --- | --- | --- |
| `S05-F-CANCEL` | after `ObjectsVerified`, and after `CarrierFsynced` before visibility | no partial carrier/catalog; workers/permits join; restart plus two same-key retries yields exactly one ready generation |
| `S05-F-CRASH` | crash once at `Prepared`, `ObjectsVerified`, `CarrierFsynced`, `Visible`, and `Cataloged` | restart resumes, validates, or reaps only the owned generation; last ready generation remains stable; replay is idempotent |
| `S05-F-CORRUPT` | independently corrupt/truncate one object range, locator/index page, hydration journal, and materialization catalog generation | verification fails closed; only proven corrupt candidate evidence is quarantined; no legacy/shared healthy carrier is deleted |
| `S05-F-ENOSPC` | allocation preflight, mid-carrier write, and after rename before catalog install | no incomplete visibility; journal/staging is bounded and recoverable; retry after restored space converges once |
| `S05-F-VERIFY-FSYNC-RENAME-CATALOG` | the 16 positions below, one failure per fresh generation | exact typed failure and durable pre/post state; restart/retry never creates two visible generations |

The exhaustive 16-position manifest is split into two independent invocations:

1. object read, object hash verification, tree-entry verification, journal
   write, journal fsync, carrier data write, carrier fsync, and carrier-directory
   fsync;
2. carrier rename, rename-parent fsync, catalog-intent write, catalog-intent
   fsync, catalog install, catalog-parent fsync, final verification/compare, and
   cleanup unlink/parent fsync.

## Raw evidence and decision

Each raw record includes revisions/build/image/platform/config/seed/order,
root/generation and legacy/candidate tree digests, mismatch count, `R/E/K`,
`C_target`, copy and hydration bytes/times/rates, phase times for read,
verify, fsync/promotion, compare and warm ensure, CAS payload reads, candidate
payload/staging/journal/carrier allocated bytes, index/cache reads, buffer/
queue/worker/borrow/permit/FD high-waters, idle/peak/settled RSS and attribution,
cancellation/recovery state, quiescence, and cleanup. Missing values are
`unavailable`, never zero.

For `S05-SMALL-META`, preserve expected and actual canonical fields rather than
only an aggregate digest. The dependency record contains canonical before/after
resolved external `(name,version,source,checksum)`, enabled
`(package,feature)`, and direct
`(workspace_package,dependency,features,kind,target)` arrays, plus Python,
system-tool, runtime-service, target-image-helper, and network requirement
deltas. Every symmetric difference and non-Rust delta has exact count `0`;
missing evidence is `OPEN`.

Local pass requires exact trees and metadata, legacy authority, atomic
visibility/recovery, warm payload reads and byte growth `=0`,
`C_peak<=C_target*1.05`, every working-set/RSS cap, and release of active
transactions/workers/tasks/borrows/queue/permits/extra FDs within 5 seconds.
Hydration must be structurally linear; a superlinear work-counter slope,
monotonic settled resource growth outside the frozen noise band, timeout, or
unexplained bytes fails. Warm p50/p95, `>=70%` copy throughput, cold activation,
the 64/256/1,024 MiB by 1/16/64-root RSS matrix, final space, and required hosts
remain diagnostic/deferred to Stage 11.

## Split wall-clock budget

These are **ESTIMATED planning values until measured**, not claimed results.

| Invocation | Included work | Estimated wall time |
| --- | --- | ---: |
| `S05-CORE` | setup, two warmups, six cold/warm corpus pairs, cleanup/report; no injected fault | **31–55 s** |
| `S05-RECOVERY-A` | cancellation, five crash states, four corruption cases, and three ENOSPC points | **90–220 s** |
| `S05-RECOVERY-B` | failpoint positions 1–8 with restart/retry/quiescence | **80–200 s** |
| `S05-RECOVERY-C` | failpoint positions 9–16 with restart/retry/quiescence | **80–200 s** |
| `S05-LIFECYCLE` | 12 alternating success/cancellation cycles and settled-slope report | **75–150 s** |
| **Full healthy arrival bundle, five invocations** | aggregate only; never one runner invocation | **356–825 s** |

Do not add sleeps or restart/trim/purge caches to manufacture settlement.
Every operation remains below 60 seconds and each invocation remains below
5 minutes. Preserve any overrun and split only at a declared failpoint boundary
before the next candidate run; do not omit a recovery state.

## Required arrival report

The run is not a Stage 05 arrival until
`.benchmark-state/results/<run_id>/stage-05-perf-report.json`
(`schema_version="phase1.stage05.perf-report.v1"`) and
`stage-05-perf-report.md` validate. They
must include raw copy/legacy and cold/warm candidate samples, target/cap,
delta/ratio/headroom, `R/E/K` and phase work, memory/RSS, complete carrier and
physical-space accounting, field-by-field metadata equality, every recovery/
failpoint/retry result, exact-zero dependency-delta arrays, provenance,
immutable run/raw links, cleanup, and
a `DIAGNOSTIC_PASS|FAIL|OPEN` verdict. Markdown renders the same JSON truth;
Stage 11 alone may qualify the final gates.

The first Markdown table must show the frozen baseline actual, required pass
target/cap, separately predeclared optimization target, candidate actual,
delta/ratio, headroom, and verdict for every stage-owned metric.

## Append-only progress

Append the exact command, intended cells, artifacts, and cleanup owner to the
shared E2E report before execution, then append the outcome here. Never edit
or remove an older row; append `Defect`, `Fix`, and `Rerun`. `QUALIFIED` is
reserved for Stage 11.

| UTC | State | Run ID | Baseline → candidate actual | Required / optimization target | Delta / ratio / headroom | Report / raw artifacts | Cleanup / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | NOT_RUN | — | — | — | — | — | Freeze metadata/failpoint manifests, then run `S05-CORE`, recovery A/B/C, and lifecycle invocations |
