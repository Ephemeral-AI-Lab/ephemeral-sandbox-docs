# Stage 04.5 benchmark note — materialization/GC lifecycle alignment

Status: **COMPLETE — PASS WITH OWNER-APPROVED PERFORMANCE EXCEPTIONS**.
Run `019fa006-36da-7f9f-ae82-3b3af89f2bab` completed the one-clock campaign
within `180 s` with sufficient matched p50/p95 samples, zero retries, and green
functional, authority, resource, space, cleanup, and quiescence gates. The raw
strict verdict remains `FAIL`; the unchanged measurements and explicit owner
disposition are recorded in
[the Stage 04.5 handoff](implementation_handoff.md).

Normative sources:

- [Stage 04.5 specification](spec.md)
- [Stage 04 benchmark note](../stage_04_candidate_materialization/benchmark_note.md)
- [Stage 05 benchmark note](../stage_05_retention_gc_packs/benchmark_note.md)
- [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

## 1. Result record schema

Every benchmark row MUST record:

| Field | Required value |
| --- | --- |
| command | exact executable, arguments, environment, and benchmark filter |
| source | revision, dirty-worktree flag/diff artifact, build profile, feature set |
| corpus | generator version, deterministic seed, corpus hash, bytes, entries, roots |
| host | machine, CPU/RAM, architecture, kernel, filesystem/mount options, runtime |
| configuration | `B`, worker/queue/FD/hold/operation/generation/depth caps and disk budget |
| samples | count, p50, p95, diagnostic p99 when `n≥100`, maximum, MAD, ops/s, bytes/s |
| accounting | bytes read/written/synced, RSS, permits, queues, workers, FDs, mappings, disk components |
| comparison | matched baseline revision/configuration/order and allowed threshold |
| artifacts | raw JSON/CSV/log/trace path and checksum |
| decision | measured value, `PASS`, `FAIL`, or `OPEN`, and exact reason |

Missing fields invalidate the result. Do not infer a `PASS` from asymptotic
analysis, unit tests, or an unpaired historical baseline.

## 2. Variables and required complexity

Use:

- `V`: live logical objects;
- `A`: allocated objects or locator records;
- `E`: strong edges/filesystem entries for the stated operation;
- `R`: bytes reconstructed for a root;
- `S`: materialization bytes selected for squash;
- `E_s`: squash reconstruction entries/work;
- `P`: pack count;
- `L`: active locator-run count and encoded bytes;
- `Q`: concurrent foreground requests;
- `B`: configured storage-owned RAM budget;
- `D`: native depth; and
- `G`: active/pinned materialization generations.

| Operation | Required time | Required RAM | Where it runs |
| --- | --- | --- | --- |
| cold private build | `O(R + E + D)` | `O(min(B,64 MiB))` | explicit admitted background/cold operation |
| warm activation | `O(D)`, `D≤64` | fixed bounded plan | foreground |
| common publication | bounded `O(1)` records/fsync | bounded state/selector/root-log entry | brief writer-lock section |
| private squash | `O(S + E_s)` | `O(min(B,64 MiB))` | outside writer lock |
| recovery | `O(64)` records per slice | one bounded page | pre-admission/background slices |
| same-key join | one owner + at most 16 waiters | bounded registry | foreground admission |
| warm command/PTY fast path | native execution cost plus explicitly transferred input/output bytes | bounded per-request buffers and existing runtime caps | foreground; no materialization/GC work |
| warm file operation | native filesystem cost proportional only to explicitly requested bytes/entries | bounded request buffers and existing session caps | foreground; no CAS/locator/materialization scan |

No foreground or writer-lock path may scale with `R`, `S`, `V`, `A`, `P`,
historical `L`, or total history. `P` and active `L` affect only bounded source
lookup; Stage 05 separately caps active locator runs at eight and encoded
`CURRENT` at 64 KiB.

## 3. Exact inherited thresholds

Use Preparation 04's `allowed = baseline × (1 + percent) + floor`.

| Metric | Gate |
| --- | --- |
| warm root resolve/session preparation p50 and p95 | `≤ baseline + 5% + 2 ms`; zero CAS payload reads |
| OverlayFS mount p50 and p95 | `≤ baseline + 5% + 2 ms` |
| squash live-remount frozen interval p50 and p95 | `≤ baseline + 5% + 2 ms` |
| full squash plan/build/commit p50 and p95 | `≤ baseline + 10% + 5 ms` |
| cold hydration throughput | at least 70% of same-filesystem verified native sequential copy |
| cold activation p95 | `≤ 1.5 ×` verified native-copy control plus warm-mount allowance |
| no-op `exec_command(["ls"])` p50 and p95 | `≤` ready ordinary-container direct `docker exec <container-id> ls` baseline `+ 3% + 0.5 ms` |
| native command throughput | at least 97% of raw LayerStack baseline |
| PTY create p50 and p95 | `≤ baseline + 3% + 1 ms` |
| PTY drain, supported `write_stdin`, and control-C/control-D p50 and p95 | `≤ baseline + 3% + 0.5 ms` |
| unsupported PTY resize, arbitrary signal, and literal EOF | preserve the current deterministic unsupported response; never score as implemented |
| native sequential file read/write | at least 97% of baseline throughput |
| small-edit publish p95 | `≤ baseline + 15% + 5 ms`; report bytes scanned and newly retained |
| concurrent disjoint publication | at least 90% of baseline throughput while preserving OCC |
| qualification RSS | at most 384 MiB absolute and 128 MiB above paired idle raw baseline |
| adjusted RSS flatness | peak/final median range ≤16 MiB; no 4× input/root increase adds >8 MiB |
| one operation deadline | no individual measured operation exceeds 60 seconds unless the declared cell is a sliced large-root maintenance campaign |

Stage 04.5 adds these structural performance gates:

| Metric | Gate |
| --- | --- |
| writer-lock forbidden-work counters | zero tree walks, payload verification, history/lease scans, waits, joins, or provider payload I/O |
| publication lock hold | report p50/p95/p99/max; p50/p95 within the warm-root `+5% + 2 ms` allowance against the pre-alignment selector-switch control |
| startup/recovery history scaling | increasing historical directories by 4× adds at most 8 MiB adjusted peak RSS; each slice inspects at most 64 records |
| same-key staging | exactly one target; at most 16 waiters; excess fails by deadline |
| disjoint target staging | at most four `Building`/`Ready` targets and aggregate `sum(T_build)≤W_mat`, where `W_mat=min(4 GiB,10% capacity)` |
| worker ownership | at most four storage workers globally under all tested concurrency |
| mappings | zero on all Stage 04.5 paths |
| native metadata and small/random file operations | matched p50/p95 `≤ baseline + 5% + 2 ms`; report p99/max; warm read-only cases perform zero candidate cold work |
| foreground during maintenance | each command/file/PTY cell continues to pass its own hard gate; report maintenance-off/on deltas and timeout count |
| read-only durable-space delta | zero new LayerStack operation, generation, root/object, pack/locator, or staging bytes after bounded quiescence |
| mutating-operation residue | every upper/work and published byte is attributed; unexpected LayerStack-owned generation/staging/residue is zero after bounded cleanup |

The publication-lock comparison is a matched regression guard, not permission
to put payload work under the lock. A zero forbidden-work counter is required
even if latency happens to pass.

## 4. RAM and scale matrix

Run all combinations that are practical and use a covering pairwise plan only
when the full Cartesian campaign cannot finish; omitted cells stay `OPEN`.

| Dimension | Required values |
| --- | --- |
| configured `B` | 64, 256, and 1024 MiB; effective shared permits remain `min(B,64 MiB)` |
| input/root size | 64 MiB, 256 MiB, and 1 GiB |
| retained roots | 1, 16, and 64 |
| object/entry count | small-object and large-object-count corpora |
| graph | shallow, depth 48, depth 64, and deeply shared |
| concurrency `Q` | 1, 4, 16, and 64 |
| generations `G` | 1, 16, and 64, with long-running readers |
| storage mix | loose-heavy, pack-heavy, and mixed live/dead packs |
| history residue | 0, 64, 4,096, and adversarially many completed directories |
| cache | warm and cold page cache, recorded separately |
| file access | 4-KiB random, 128-KiB and 1-MiB sequential, metadata-only, and many-small-file mutation |
| execution mode | direct no-op command, sustained command batch, PTY lifecycle, and public workspace/file API |

For each `input size × retained roots × candidate` RSS point, use its own
matched raw/candidate invocation and three repetitions as Preparation 04
requires. Record storage-owned live bytes separately from allocator RSS.

## 5. Workload matrix

Use deterministic Preparation 04 corpora plus Stage 04.5 lifecycle variants:

| Workload | Required measurements | Status |
| --- | --- | --- |
| cold materialization by `R,E,D` | elapsed, verified throughput, bytes read/written, RSS, permits, workers, FDs, staging | `OPEN` |
| warm reuse/activation | p50/p95/p99/max, `D`, zero payload/forbidden-work counters | `OPEN` |
| no-op `exec_command(["ls"])` | p50/p95/p99/max, exit/stdout/stderr, setup/drain time, zero cold-work counters | `OPEN` |
| sustained native command batch | commands/s, p50/p95/p99/max, CPU, RSS, FDs, timeouts | `OPEN` |
| PTY create/drain/input/cancel | p50/p95/p99/max per supported operation, bytes, semantics, resources | `OPEN` |
| sequential file read/write | bytes/s at 128-KiB and 1-MiB request sizes, p50/p95/p99/max, CPU, allocated-byte delta | `OPEN` |
| 4-KiB random file read/write | IOPS, p50/p95/p99/max, fsync mode, CPU, allocated-byte delta | `OPEN` |
| file metadata operations | `stat`, `readdir`, create, rename, fsync, and unlink ops/s and p50/p95/p99/max | `OPEN` |
| many-small-file mutation | create/write/fsync/rename/unlink throughput, peak and quiescent upper/work bytes, residue | `OPEN` |
| read-only/no-op space | before/peak/quiescent allocated bytes by owner; durable LayerStack delta must be zero | `OPEN` |
| initial publication | lock wait/hold, fsyncs, selector/state bytes | `OPEN` |
| replacement publication | lock metrics, root-log bytes, exact old-handoff latency, overlap bytes | `OPEN` |
| same-key `Q` | owner/waiter high-water, duplicate bytes, timeout/rejection | `OPEN` |
| disjoint-key `Q` | throughput and foreground latency while sharing four workers/64 MiB | `OPEN` |
| private squash by `S,E_s,D` | plan/build/commit/frozen time, depth, bytes, identity | `OPEN` |
| long-running old readers | old/new/leased bytes, lookup latency, generation cap behavior | `OPEN` |
| recovery by history | startup/slice time, page count, RSS, admission delay, residue | `OPEN` |
| crash/restart storm | time to safe admission, recovery throughput, repeated-work bytes | `OPEN` |
| continuous publication during build | foreground p50/p95/p99/max, build throughput, lock contention | `OPEN` |
| disk pressure/ENOSPC | predicted/actual peak, abort latency, retained source bytes | `OPEN` |
| cancellation/panic churn | settled RSS slope, resources and residue after quiescence | `OPEN` |

The large object-count cells include at least the Preparation 04 mixed tree
(512 MiB/20,000 files), no-dedup binary (512 MiB), many-small-file corpus
(100,000 files), large source file (256 MiB), and sparse file (8 GiB logical
with bounded allocated extents).

## 6. Foreground latency during maintenance

Measure warm root resolve, session preparation, mount, no-op command, sustained
command batch, PTY create/drain/input/cancellation, sequential file read/write,
4-KiB random file read/write, `stat`, `readdir`, create, rename, fsync, unlink,
and concurrent publication while each of the following runs:

- cold build;
- private squash;
- recovery paging;
- continuous replacement publication;
- Stage 05 GC mark/sweep when available; and
- Stage 05 old-generation retirement when available.

Report foreground p50, p95, p99, maximum, timeout count, and throughput, plus
maintenance throughput and pause/lock distribution. Separate same-key blocking
from disjoint-key behavior. Any `O(R)`, `O(S)`, `O(V)`, `O(A)`, or
`O(total history)` foreground/lock trace is a correctness `FAIL`, not merely a
latency regression.

Run file operations through the public workspace/file API and command/PTY
operations through their public runtime APIs. Do not substitute an arbitrary
shell command for storage-path verification. Preserve operation semantics,
exit status, stdout/stderr, PTY byte stream, fsync mode, request size, access
pattern, and cache state between the matched raw and candidate runs.

## 7. Physical-space accounting

Measure allocated physical bytes, not apparent length. Report separately:

- unique logical payload;
- current native materialization;
- old exact leased/pinned generations;
- private replacement target;
- operation staging and metadata;
- loose and packed physical payload;
- locator metadata;
- duplicate old/new overlap;
- v1 rollback-authority bytes;
- abandoned operation residue; and
- unreachable but not yet Stage 05-reclaimed bytes.

Required peak shapes:

| Operation | Allowed temporary shape |
| --- | --- |
| cold build | one complete `C_target` plus at most 5% of `C_target`, with all authoritative sources retained |
| squash/replacement | one complete replacement plus old/current/leased generations |
| crash recovery | the admitted target and exact recorded residue; no duplicate retry target |
| ENOSPC | abort before visibility; never delete a source to make room |

Required command/file space deltas:

| Workload | Required space result |
| --- | --- |
| no-op command, PTY create/drain without writes, file read, `stat`, and `readdir` | after bounded quiescence, zero new durable LayerStack operation, materialization generation, logical object/root, pack/locator, or staging bytes |
| session file create/write/rename/fsync | all allocated growth is attributed to the session upper/work filesystem; no hidden materialization generation or common operation is created |
| session file unlink and teardown | expected filesystem slack is reported against the matched raw baseline; unexpected LayerStack-owned residue is zero |
| explicit publish after mutation | root/object and publication bytes are reported separately from command execution; only the declared publication may create durable logical state |
| command/file operation during maintenance | peak includes the operation's upper/work growth plus all admitted maintenance overlap; aggregate reservations and available-space preflight still pass |

Capture component-level allocated-byte snapshots before the operation, at peak,
after the operation, and after bounded quiescence. Apparent length, page-cache
occupancy, allocator RSS, and physical allocated bytes are reported separately.
A zero-payload or read-only operation cannot hide durable growth inside a later
settle step or an unattributed maintenance directory.

Across concurrent cold/replacement operations, at most four private targets may
exist and their aggregate reservations must remain within `W_mat`. Per-operation
shape and aggregate store shape are both gates.

Before Stage 05, retained old published generations are expected but must be
fully attributed and included in peak/settled totals. Stage 04.5 cannot claim
settled-space `PASS` for that state.

After Stage 05 convergence, the inherited settled gates are:

| Corpus/metric | Target | Hard failure |
| --- | ---: | ---: |
| mixed tree / no-dedup binary | `≤1.08 × D_ideal` | `>1.15 × D_ideal` |
| many-small-file | `≤1.15 × D_ideal` | `>1.25 × D_ideal` |
| avoidable native-plus-pack duplication | `≤1%` | `>3%` |
| settled pack dead bytes/slack | `≤2%` | `>5%` |
| unexplained unreachable, unleased payload | 0 bytes | any persistent unexplained payload |
| native lower depth | preemptively below 64 | exceeds 64 |

Long-running-reader bytes and v1 authority bytes remain in physical accounting
and are reported separately; they cannot be hidden as exclusions.

## 8. Matched campaign table

Populate one row per exact cell:

| Run ID | Baseline / proposal | Command | Revision | Corpus hash | Host/fs | Caps | Samples | Raw artifact | Threshold | Measured | Result |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| _unassigned_ | Stage 04 before / Stage 04.5 aligned | _not run_ | _not recorded_ | _not recorded_ | _not recorded_ | _not recorded_ | 0 | _none_ | see §§3–7 | _none_ | `OPEN` |

Do not replace this table with prose summaries. Keep failed and superseded runs
with their artifact links.

## 9. Go/no-go

Stage 04.5 benchmark status becomes `PASS` only when:

1. every exact Preparation 04 threshold applicable to materialization, squash,
   command, file, and PTY operation passes;
2. matched baseline/proposal campaigns show no unacceptable foreground
   regression;
3. lock instrumentation proves heavy work is absent;
4. memory stays within the absolute, above-baseline, flatness, and explicit
   permit caps;
5. workers, queues, FDs, mappings, operations, waiters, holds, retries, and
   generations stay within hard caps;
6. peak disk overlap is admitted safely and cannot exhaust the store after
   preflight;
7. post-Stage-05 settled space passes the inherited amplification and residue
   gates;
8. crash/restart and cancellation do not create unbounded repeat work or
   unexplained residue; and
9. read-only/no-op operations create zero durable LayerStack-owned bytes and
   every mutating-operation byte is attributed at peak and quiescence; and
10. every `PASS` links a complete raw result.

Until then, speed, memory, peak-space safety, and settled-space efficiency are
`OPEN`.
