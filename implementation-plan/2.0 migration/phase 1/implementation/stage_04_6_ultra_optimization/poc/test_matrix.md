# MPLA proof-of-concept test matrix

**Status:** design for performance and correctness falsification; not release qualification  
**Architecture under test:** stationary allocation adoption MPLA  
**Design authority:** `../new_plan.md` and `../requirements_and_prohibitions.md`  
**Performance objective:** demonstrate at least `100×` matched improvement on
eligible post-setup paths; prefer and report `500×` or greater  
**Host envelope:** current Docker Desktop allocation, 4 vCPU and 4 GiB; do not increase it for this PoC  
**Suite envelope:** smoke hard limit 3 minutes; heavy hard limit 10 minutes  
**Fixture envelope:** no heavy fixture or combined layer chain exceeds 10 GiB  
**Bound real-corpus experiment:** [`experiments/ubuntu24_console_release_870mib.md`](experiments/ubuntu24_console_release_870mib.md)

---

## 1. Purpose

The PoC answers six questions:

1. Can a mutable allocation be sealed and adopted without copying or moving its
   path?
2. Do stale workspace leases lose both write and delete authority after
   adoption, including across crashes?
3. Is publication work incremental in the new delta rather than the accumulated
   size of existing roots and layers?
4. Do large files, many small files, and rapid multi-agent publication stay
   within the fixed memory envelope without OOM?
5. Can OCI activation use an exact projection plus a fresh upper while keeping
   canonical Merkle identity independent of OverlayFS and `AllocationId`?
6. On operations that eliminate complete-repository work, does the candidate
   demonstrate at least `100×` matched improvement, preferably `500×` or more,
   without moving work outside the declared boundary?

This is a falsification suite. A failed invariant rejects or changes the design;
the suite must not raise the memory limit, hide fixture time, use a copy
fallback, or weaken correctness to obtain a faster number.

---

## 2. Two execution tiers

| Tier | Use | Runtime | Repetition | Concurrency |
|---|---|---:|---|---|
| Smoke | Fast implementation loop and obvious-regression detection | Design target `≤150 s`; hard stop `<180 s` | One warm-up; cheap cases 3 measured runs; expensive cases once | Up to four active data workers |
| Heavy | Load-bearing proof on large/cardinality/concurrent fixtures | Design target `≤480 s`; hard stop `<600 s` | Cheap cases 3 measured runs; ≥1 GiB, ≥100k-file, crash, and long-chain cases once | Four active workers plus queued logical agents |

Three repetitions do not support a statistically meaningful p95. Report every
sample, median for the cheap cases, and max. Any p95 in a later qualification
campaign requires enough independent samples and must not be inferred from this
PoC.

The PoC therefore reports `POC_MEDIAN_RATIO`, never a qualifying p95 speedup.
It supports the `100×` design objective only when the candidate and control are
semantically matched, the median ratio is at least `100`, every candidate sample
also meets the applicable absolute required ceiling, and all
correctness/space/memory gates pass. It reports the preferred `500×` result only
under the same rule with a median ratio of at least `500` and the preferred
absolute ceiling. Ratios are never capped: a measured `1,700×` remains
`1,700×`.

The suite timer excludes deterministic fixture generation only when the fixture
was built before the timer and is reused unchanged. Every measured operation
still includes its real scan, hash, flush, owner transition, locator selection,
Merkle update, ref durability, mount, and readiness work. Report fixture build
time and bytes separately.

### 2.1 Booster evidence and claim rules

Every candidate performance row has one of these evidence classes:

| Class | Meaning |
|---|---|
| `MATCHED_SPEEDUP` | Candidate and current control use the same fixture, operation intent, logical input-availability contract, start boundary, stop/readiness boundary and required durability. Implementation-specific physical cache/placement states are disclosed and must be the states naturally produced by the same declared setup; no asymmetric hidden warm-up is allowed. |
| `HISTORICAL_EQUIVALENT` | Arithmetic comparison with a preserved historical sample only; useful context, never a matched speedup claim. |
| `ABSOLUTE_GATE_ONLY` | Candidate meets an absolute latency target but no valid matched control completed. |
| `PHYSICAL_FLOOR` | The operation necessarily reads, writes, creates or copies work proportional to bytes or entries; no universal `100×`/`500×` claim applies. |
| `UNKNOWN` | The control, boundary, cache proof or sample data is missing, incompatible or stopped by the suite budget. |

For a matched PoC pair:

```text
POC_MEDIAN_RATIO =
  median(matched current-control samples) /
  median(MPLA candidate samples)

HISTORICAL_EQUIVALENT =
  preserved historical sample /
  median(MPLA candidate samples)
```

Publication may use only a current `I0` or `I2` closing control with the same
admission-through-durable-root/session-closed boundary as the candidate. The
historical `107.024411507 s` first-ingestion sample is not a denominator for an
ordinary small-delta publication. A missing matched control makes the ratio
`UNKNOWN`; it does not turn an absolute result into a `100×` claim.

The preserved cold-materialization sample is `9.987675338 s`, so an exact
stored `870 MiB` activation must be at most `99.87675338 ms` for the historical
`100×`-equivalent ceiling and at most `19.975350676 ms` for the
`500×`-equivalent ceiling. The matched-current divisor must also pass.

### 2.2 Booster scorecard gates

| Gate ID | Eligible operation and qualifying row | Required PoC objective | Preferred result | Work that must be absent from the optimized boundary |
|---|---|---:|---:|---|
| `BG-ACTIVATE-EXACT` | Exact stored `870 MiB` activation: `HV-08` / `R0-04` versus `R0-C01`, with an exact zero-build `R0-03` precondition | `≤min(99.87675338 ms, matched/100)` | `≤min(19.975350676 ms, matched/500)` | Payload reconstruction, hydration, per-object ingestion and a projection build deferred into the immediately preceding activation |
| `BG-ACTIVATE-SAME` | Same-key usable session: first three `R0-04` samples versus `R0-C02` | `≤50 ms` and `≤matched/100` | `≤20 ms` and `≤matched/500` | Complete-tree/carrier rebuild |
| `BG-FORK` | Forked exact-projection activation: `HV-10` | `≤10 ms` and `≤matched/100` | `≤2 ms` and `≤matched/500` | Inactive payload/projection construction and tree copy |
| `BG-ROLLBACK` | Public hot rollback to usable target: `HV-10` | outer `≤20 ms`, service `≤1 ms`, and outer `≤matched/100` | outer `≤10 ms` and `≤matched/500` | Root reconstruction and payload copy on an exact hit |
| `BG-PUBLISH-SMALL` | Ordinary `≈1 MiB`/10-file closing publication: `HV-01` | `≤100 ms` and `≤matched/100` | `≤20 ms` and `≤matched/500` | Accumulated-root scan, loose-object amplification and second payload copy |
| `AG-SQUASH` | Public logical squash: `HV-10` | outer `≤10 ms`, service `≤1 ms` | preserve/report `1–6 ms` | Payload scan, rebuild or physical flatten; no multiplier claim is required |
| `AG-STREAM` | Large CAS/CDC stream: `HV-02` | `≥1 GiB/s` | `≥5 GiB/s` | Avoidable additional complete passes |

The five `BG-*` rows are the complete aggregate `100×`/`500×` multiplier set
for this PoC. Smoke rows are fast diagnostic mirrors and do not create duplicate
votes; `HV-05` proves long-chain stability but does not add a sixth denominator.
The two `AG-*` rows retain independent absolute verdicts.

Cold first ingestion, true empty-worker hydration, genuine creation of many
files and the first ordinary OverlayFS copy-up of a large lower-only file remain
`PHYSICAL_FLOOR` rows. They must be optimized against matched one-pass controls
but never relabeled as `100×` or `500×`.

---

## 3. Prepared fixtures

All fixtures are deterministic and generated offline. Public repositories may
be added as semantic diversity fixtures, but no network fetch belongs inside a
measured run.

| Fixture | Shape | Smoke | Heavy | Purpose | Expected stored footprint before deltas |
|---|---|---:|---:|---|---:|
| `S0-empty` | Empty root plus directory metadata | yes | yes | Fixed overhead, create/activate/close | `<16 MiB` including control data |
| `S1-code` | Mixed source tree, symlinks, executable bits, xattrs where supported | 10k paths / 128 MiB | 100k paths / 1 GiB | Normal repository behavior | payload `≈` logical bytes; metadata reported separately |
| `S2-large` | Four large files with deterministic incompressible and sparse regions | 256 MiB | 1 GiB | Bounded streaming, tiny edit, copy-up truth | payload `≈256 MiB` / `≈1 GiB` |
| `S3-small` | Fan-out tree of 0–4 KiB files, long names, hardlink groups | 20k paths / ≤64 MiB | 250k paths / ≤1 GiB | Many-small-file memory and inode pressure | metadata may dominate; must be reported |
| `S4-chain` | Exact base plus sequential immutable published deltas | 1 GiB base + 16 small deltas | ≤9 GiB base/chain + ≤256 MiB final delta | Existing-size independence and projection depth | combined fixture/layer payload `<10 GiB` |
| `S5-semantics` | Whiteouts, opaque dirs, type changes, renames, hardlinks, sparse files, xattrs, ACL/capability cases allowed by profile | ≤5k paths / 64 MiB | ≤25k paths / 256 MiB | Canonical correctness oracle | `<512 MiB` |
| `R0-console-release` | Preserved compiled Rust release corpus: 3,602 files, 694 directories, 214 files ≥1 MiB, 912,350,100 logical bytes | Deterministic ≈128 MiB path-manifest subset, supplemental only | Full 870.08 MiB corpus | Real near-1-GiB stationary publication, projection construction, activation, small-delta republish, reconstruction and reconciliation | source corpus only; never include its preserved materialized result |

For every fixture record logical bytes, allocated bytes, inodes, sparse/shared
extent facts where observable, generated digest, and build duration. The
10-GiB limit applies to the fixture/layer chain under test, not to unrelated
Docker images already present on the machine.

### 3.1 Bound Ubuntu 24.04 real-corpus experiment

`R0-console-release` uses only:

```text
/Users/yifanxu/Ephemeral-AI-Lab/experiment/materialization-benchmark-20260727/corpus/console-release
```

The parent experiment directory is about 1.7 GiB because it also contains a
preserved materialized-carrier copy. It is never used as the fixture root.

The bound OCI image is Linux/arm64 Ubuntu 24.04 with local immutable image
identity:

```text
sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
```

The evidence record stores the resolved image ID, architecture, OS release,
Docker engine version and graph driver. The mutable tag `ubuntu:24.04` is
convenience only and is never the qualification identity. The external harness
must not rely on a shell or other command inside this image.

Fixture transfer from the macOS host into a prepared Linux Docker volume occurs
before the suite timer and is reported separately. The measured experiment
still includes the real allocation flush, scan, hash, stationary owner
adoption, locator/Merkle durability, projection construction, mount, external
readiness and reconstruction work. The full corpus is the required `HV-08R`
real-corpus subcase. Its samples may satisfy overlapping `HV-08` activation and
`HV-10` reconciliation assertions without rerunning the same physical work.

The corpus supplements rather than replaces `S1`–`S5`: 3,602 files cannot
qualify the 100k/250k cardinality paths, it is not the four-file 1-GiB copy-up
fixture, and compiled artifacts do not exercise the complete semantic oracle.
The deterministic smoke subset likewise supplements rather than replaces the
128-MiB `S1-code` semantic shape.

---

## 4. Required measurement record

Each case emits one machine-readable record containing:

- suite/case id, git revision, image digest, backend qualification digest, and
  Docker Desktop CPU/memory settings;
- compared implementation (`I0`, `I1`, `I2` or `I3`), exact build identity,
  matched-pair id, cache/placement class and evidence class;
- operation boundary and whether fixture generation is excluded;
- wall time plus spans for admission, quiesce, unmount, flush, scan/hash,
  ownership adoption, Merkle build, locator selection, ref fsync, mount, and
  external readiness;
- logical/allocated/unique/shared bytes and inodes before, at peak, and after;
- `AllocationId`, allocation generation, owner epoch, and lease epoch in the
  private test artifact only—never in a canonical root/ref;
- application RSS, whole storage cgroup RSS, `memory.current`,
  `memory.events`, kernel slab where available, open FDs, mounts, worker count,
  queue bytes, and OOM events;
- root/attribution ids, oracle result, locator coverage, stale-token result,
  crash-recovery terminal state, and `X_unexplained`;
- raw control and candidate samples, medians, maxima,
  `POC_MEDIAN_RATIO`, `HISTORICAL_EQUIVALENT`, exact absolute/matched gate
  expressions and verdicts;
- bytes eliminated from the scored boundary: reconstructed, hydrated,
  accumulated-root-scanned, copied and second-payload bytes;
- raw samples. Expected bands below remain `PROJECTED` until measured.

The PoC fails on any OOM, lost update, partial root, writable adopted allocation,
stale-token success, last-locator loss, payload copy during optimized
publication, unexplained persistent bytes, or hard suite-time overrun. It may
still pass correctness while returning `POC_100X_NOT_SUPPORTED`; correctness
success is never relabeled as performance success.

---

## 5. Smoke matrix

The smoke suite is one ordered campaign so fixture and daemon startup are
amortized without excluding operation work.

| ID | Section | Operation / public boundary | Fixture and mutation | What is checked | Projected time | Expected storage/memory |
|---|---|---|---|---|---:|---|
| `SM-01` | Qualification | backend qualify → workspace create | `S0-empty` | Stable allocation handle, adjacent upper/work, OverlayFS semantics, no host workspace payload copy | `1–5 s` once | control-only workspace metadata; no OOM |
| `SM-02` | Lease | create → `exec_command` → close without publish | `S0-empty`, create 10 files | Only current lease can mutate/delete; exact private cleanup | `<1 s` | allocation removed only while workspace-owned |
| `SM-03` | Adoption + publication booster | receipt-hit `seal_publish`, then forced immediate receipt miss as a separate sample | `S1-code`, edit 10 files / ≈1 MiB | Same `AllocationId` and physical path before/after; `WorkspaceOwned→Sealing→PayloadOwned`; matched closing control when it fits the smoke budget | receipt hit absolute `≤100 ms`, prefer `≤20 ms`; support `100×`/prefer `500×` only with matched control; forced miss `≤1.070 s` | no second payload allocation; app pool ≤8 MiB |
| `SM-04` | Stale authority | old workspace write/delete after `SM-03` | adopted allocation | Old lease and teardown token are rejected | `<100 ms` | zero byte/inode change |
| `SM-05` | Activation booster | activate committed root → external readiness; time first `exec_command` separately | `SM-03` root; one warm-up plus three exact-hit samples | Exact projection role is qualified separately; new allocation/lease is fresh; no reconstructed or hydrated bytes | absolute `≤100 ms` each, prefer `≤20 ms`; matched `100×` required for booster support and `500×` preferred | fresh upper initially empty |
| `SM-06` | Incrementality | publish 16 sequential tiny edits; preserve every sample and early/middle/late medians | `S1-code` | Root correctness; valid-receipt publication reads zero accumulated immutable payload; latency and byte work do not grow with prior roots | `<2 s` campaign; each receipt-hit sample `≤100 ms`, prefer `≤20 ms` | growth traces to deltas/metadata only |
| `SM-07` | Large file | edit 4 KiB in an already-upper 256 MiB file, publish | `S2-large` | Bounded reads, no `read_to_end`, honest copy-up/scan span | `<5 s` | no payload twin; RSS soft ≤96 MiB, hard <128 MiB |
| `SM-08` | Many small | create/publish 20k tiny files | `S3-small` | Disk spools/external sort; bounded FDs/tasks/heap | `<20 s` | metadata/inodes reported; no cardinality-sized resident map |
| `SM-09` | Semantics | mutation oracle publish and reconstruct | `S5-semantics` | Reconstructed tree equals final-scan oracle including supported metadata | `<15 s` | zero missing locator/metadata |
| `SM-10` | Multi-agent | four agents lease independent roots and publish at a barrier | four small `S1-code` branches | Isolation, all disjoint results visible, no global serialization around hashing | `<10 s` | four uppers only; queued work owns zero payload |
| `SM-11` | OCC | two disjoint and two conflicting publications | small branch fixture | Disjoint rebase succeeds; same/ancestor overlap returns stable typed conflict | `<5 s` | retained conflict accounted; no deletion |
| `SM-12` | Recovery | kill at lease revoke, owner-journal append, locator select, ref fsync | small fixture; one injection per boundary | Old or complete new root only; exact owner epoch; idempotent same-id retry | `<30 s` total | safe accounted residue only |
| `SM-13` | Reconcile | storage reconcile/status | all smoke artifacts | Physical equation balances and `X_unexplained=0` | `<5 s` | every allocation classified |
| `SM-14` | CLI lifecycle + metadata boosters | create → exec → publish → activate → fork → rollback → squash → close | small fixture; three cheap samples per metadata operation | Public success/error/cancel output maps to durable outcomes; separately time fork metadata, fork-to-ready, rollback service/outer, squash service/outer and first command after ready | `<15 s`; fork activation `≤10 ms`/prefer `≤2 ms`; rollback outer `≤20 ms`/prefer `≤10 ms`; squash outer `≤10 ms`, service `≤1 ms` | inactive fork adds metadata only; all mounts/FDs/leases released |

Smoke execution stops immediately on a correctness, ownership, OOM, or hidden
copy failure. Performance misses continue only long enough to retain diagnostic
spans, provided the 3-minute hard stop is still enforced.

---

## 6. Heavy matrix

| ID | Section | Operation / public boundary | Fixture and mutation | What is checked | Projected time | Expected storage/memory |
|---|---|---|---|---|---:|---|
| `HV-01` | Existing-size independence + publication booster | publish identical ≈1 MiB/10-file delta on short and long chains; run a three-pair matched closing control block at the 1 GiB point | `S4-chain` at 1 GiB, 5 GiB, and ≤9 GiB accumulated sizes | Adoption span is constant; valid-receipt scan/build follows delta, not existing bytes; candidate reads zero accumulated immutable payload | budget `35 s`; candidate `≤100 ms` and matched median `≥100×`, prefer `≤20 ms` and `≥500×` | final fixture/chain `<10 GiB`; no `existing size × publication` twin |
| `HV-02` | Big update + stream floor | publish 1 GiB genuinely changed upper | `S2-large` | Real stream/hash/flush throughput, checksum inside timer and `H+O(M)` peak | budget `20 s`; CAS/CDC `≥1 GiB/s`, prefer `≥5 GiB/s`; publication remains `PHYSICAL_FLOOR` | one changed allocation plus bounded metadata |
| `HV-03` | Large lower copy-up | first 4 KiB write to a 1 GiB lower-only file, then publish | `S2-large` | Separately time kernel copy-up and publication; do not credit MPLA for avoiding copy-up it did not avoid | budget `25 s` | upper may grow ≈1 GiB before publish; no second 1 GiB publication copy |
| `HV-04` | Many-small + memory | publish 250k tiny files while sampling application/cgroup/kernel memory | `S3-small` heavy | External-sort correctness, FD bound, inode/slab pressure, soft/hard reactions | budget `60 s` | app pool ≤8 MiB; storage soft ≤96 MiB/hard <128 MiB or design fails |
| `HV-05` | Long rapid chain | 64 sequential small publications; report every sample plus first/middle/last-eight medians | 5 GiB `S4-chain`, 10 files/≈1 MiB per delta | Every valid-receipt publication reads zero prior immutable payload; publication rate does not decay; locator/catalog and kernel projection depth remain bounded | budget `50 s`; every candidate `≤1.070 s`, median objective `≤100 ms`, prefer `≤20 ms` | accumulated new payload ≈64 MiB plus metadata; no 64-layer kernel lower stack requirement |
| `HV-06` | Multi-agent/OCC/overload | four active publishers with mixed disjoint/overlap work; 12 queued logical agents; cancellation/job-33 probe | independent and same-root `S1-code` branches | Four-worker progress, disjoint rebase, typed conflict, queue-zero-payload, fairness, typed overload | budget `45 s` | four active uppers only; queue ≤64 KiB; no OOM |
| `HV-07` | Crash sweep | process/VM kill at the conditional owner transition, locator selector, and paired-ref durability edges | 128 MiB fixture | Replay produces exact owner and old-or-complete-new root; same-id recovery | budget `60 s` | no ambiguous allocation; safe residue explicitly classified |
| `HV-08` | Activation booster + semantic identity | three-pair current `I2` cold-to-usable and same-key-to-usable control block; exact activation at projection depths 1/4/8; five cached `870 MiB` activation repeats and three candidate same-key usable sessions; semantic reconstruct/compare; run bound `HV-08R` stationary publish/activate/republish sequence | `R0-console-release` full corpus plus `S4-chain` and `S5-semantics` | Cold, same-key and exact-hit labels/boundaries separated; exact hits reconstruct/hydrate zero bytes; stable physical allocation across adoption; no second corpus-sized publication copy; bounded native lowers; roots independent of `AllocationId`/path | target budget `60 s`; exact activation `≤min(99.87675338 ms, matched/100)`, prefer `≤min(19.975350676 ms, matched/500)`; same-key candidate `≤50 ms` and `≥100×`, prefer `≤20 ms` and `≥500×`; diagnostic cap `120 s` | fresh upper only on activation; reconstruction exact; cap overrun consumes diagnostic margin and is a visible performance miss |
| `HV-09` | Evacuation + debt | pack one adopted 1 GiB allocation, hold a reader, then approach configured PoC debt quota | published `S2-large` variants | Honest old+new peak, locator replacement, reader safety, typed backpressure, no silent delete | budget `60 s` | fixture chain stays `<10 GiB`; every source/target counted |
| `HV-10` | Full lifecycle + metadata boosters + reconcile | concurrent create/exec/publish/activate/fork/rollback/squash/close plus response loss and cancellation; create 1/64/1,000 inactive forks and activate only selected samples | mixed prepared fixtures | Fork metadata and payload slopes; matched fork/rollback controls; public outcomes, epochs, mount/FD cleanup, last locator, final physical equation | budget `30 s`; fork activation `≤10 ms` and `≥100×`, prefer `≤2 ms` and `≥500×`; rollback outer `≤20 ms` and `≥100×`, prefer `≤10 ms` and `≥500×`; squash outer `≤10 ms` | inactive forks own zero payload/upper/projection/mount; no leaked active lease; `X_unexplained=0` |

The declared heavy case budgets total 445 seconds. Setup/teardown and report
serialization have a 35-second reserve inside the 480-second design target and
a further 120-second diagnostic margin before the 600-second hard stop.

Matched controls are co-scheduled inside `HV-01`, `HV-08` and `HV-10`; they do
not authorize an additional unbounded campaign. The old 107-second historical
publisher is not rerun merely to create an impressive ratio. If a matched
control cannot complete inside its declared case budget, retain its raw partial
evidence, set the corresponding ratio to `UNKNOWN`, and report
`POC_100X_NOT_SUPPORTED`. The suite may continue for correctness within the
hard limit.

The scheduler may omit a later performance-only cell when the hard 10-minute
budget would be exceeded, but it may not omit the ownership, semantic,
memory/OOM, hidden-copy, or final-reconciliation cells and still report the
heavy suite as passed. A time-budget omission is a visible `NOT_RUN_BUDGET`
result, not a pass.

### 6.1 Required top-level verdicts

The report emits independent verdicts rather than one ambiguous “PoC passed”:

| Verdict | Condition |
|---|---|
| `POC_CORRECTNESS_PASS` | Every ownership, semantic, durability, recovery, space, memory and reconciliation gate passes. |
| `POC_100X_SUPPORTED` | All five `BG-*` gates have `MATCHED_SPEEDUP`, `POC_MEDIAN_RATIO≥100`, every candidate sample meets its required absolute ceiling, and `POC_CORRECTNESS_PASS` holds. |
| `POC_100X_NOT_SUPPORTED` | Any required `BG-*` gate is below `100×`, misses its absolute ceiling, is `UNKNOWN`, or fails a non-performance gate. |
| `POC_500X_SUPPORTED` | All five `BG-*` gates meet the corresponding preferred absolute ceiling and `POC_MEDIAN_RATIO≥500`; report every larger uncapped ratio. |
| `POC_500X_PARTIAL` | `POC_100X_SUPPORTED` holds and at least one but not all five `BG-*` gates reaches the preferred `500×` rule. |
| `POC_500X_NOT_SUPPORTED` | The complete preferred rule is not met and `POC_500X_PARTIAL` does not apply—for example, no eligible row reaches `500×`, the aggregate `100×` objective is unsupported, or correctness fails. |

Logical squash and streaming throughput retain their own absolute verdicts; they
are not forced into a meaningless multiplier. Physical-floor rows can falsify
correctness, boundedness or throughput, but cannot lower or inflate the matched
hot-path speedup.

### 6.2 Time/space-complexity evidence

| Path | Expected PoC shape | Required evidence | Falsifier |
|---|---|---|---|
| Exact activation | `O(D_proj)`, constant in repository bytes/files | Compare prepared 128 MiB, 870 MiB and 1/5/≤9 GiB roots at `D_proj=1/4/8`; zero reconstructed/hydrated payload bytes on an exact hit | Latency or byte work proportional to root size |
| Valid-receipt small publication | `O(ΔB + ΔP·d + K_delta)`, independent of accumulated history | Identical ≈1 MiB/10-file delta at 1/5/≤9 GiB; zero prior immutable payload bytes read | Scan/hash grows with existing immutable size |
| Fork | `O(log R)` metadata and zero inactive payload | Compare 1/64/1,000 inactive forks; record bytes, uppers, projections and mounts | Any payload/projection/upper/mount per inactive fork |
| Hot rollback/squash | Bounded metadata/projection selection | Compare 16/64/1,000-root histories; zero reconstruction/copy | Payload work or linear history traversal |
| Many-small publication | Linear external I/O with bounded resident memory | 20k and 250k entries; fixed application pool, FD/task/queue bounds and RSS gates | Cardinality-sized resident map, unbounded resources or OOM |
| Cold hydration | `Θ(B+F)` one-pass physical work | 128 MiB, 870 MiB and 1 GiB throughput versus matched native floor | Superlinear work or a false hot-path label |
| First large-file copy-up | `Θ(file size)` on ordinary OverlayFS | Separately report kernel copy-up bytes/time from publication | Crediting MPLA with work performed by the kernel or claiming universal `500×` |

---

## 7. CLI and API coverage

The PoC binds to the generated public command catalog before implementation.
The names below describe operations, not permission to invent unsupported
commands:

| Operation boundary | Required CLI/API observation |
|---|---|
| Workspace/session create | Returns session epoch plus opaque workspace handle; `AllocationId` remains diagnostic/private |
| `exec_command` | First command works in the mounted merged workspace; command dispatch/execution is timed separately from activation; long commands hold no storage worker while idle |
| Closing checkpoint / `seal_publish` | Clearly states that the old session is consumed and process state is not preserved |
| Status/query/retry | Same scoped `PublicationId` returns the exact durable outcome; stale/different request bytes reject |
| Activate | Reports exact hit, compatible hit, build, or miss; returns a new session epoch and fresh upper lease; emits the matched-control id and reconstructed/hydrated bytes |
| Fork/branch/freeze | Inactive fork creates metadata only; activation is separately timed through external readiness |
| Rollback/reset/revert | Paired ref update is atomic; service and externally usable readiness spans are explicit |
| Squash/materialization selection | Pointer-only only when an already-ready exact generation exists; service and outer spans are explicit; missing construction is separate |
| Cancel/close/destroy | Phase-aware; only pre-`Sealing` restoration/private cleanup, then `Sealing`-or-later roll-forward; stale deleter cannot remove payload |
| Storage status/reconcile | Reports physical categories, debt, inodes, owner epochs, and `X_unexplained` without exposing locator identity as root truth |

Every command test covers success, typed rejection, cancellation, response loss,
same-id retry, and teardown where applicable. Tests use external readiness
probes and never require `/bin/sh`, `stat`, `ls`, a package manager, or another
helper inside the workload image.

---

## 8. Interpretation

The following outcomes support the design but are not release proof:

- stationary adoption metadata stays small while flush/hash time scales with
  the actual new delta;
- every eligible hot-path row has a valid matched control, reaches at least
  `100×`, and meets its absolute ceiling;
- `500×` is reported per operation as supported, partial or missed, with every
  larger observed ratio retained uncapped;
- a ≤9 GiB accumulated chain does not make a ≈1 MiB valid-receipt publication
  scan the full chain;
- exact cached activation reconstructs/hydrates zero bytes and reaches the
  exact dual historical/matched gate;
- large and many-small workloads stay under the unchanged memory limits.

The following outcomes falsify the current design:

- publication requires rename across mounts, reflink, payload copy, or a
  host-workspace volume copy;
- an old lease can write or delete after `PayloadOwned`;
- `AllocationId` or a path changes canonical root bytes;
- publication time grows with accumulated immutable chain size for a fixed
  valid-receipt delta;
- a `100×`/`500×` ratio uses the historical first-ingest number for a small
  publication, compares different readiness boundaries, omits required work or
  includes a cache/build mismatch;
- any required eligible row is reported as a speedup despite a missing matched
  control;
- a repository-sized heap/task/FD structure or OOM appears;
- the kernel is asked to mount one lower for every historical stack;
- storage cannot reconcile to zero unexplained bytes.

Expected times and memory/storage amounts in this document are hypotheses.
Replace them only with raw-artifact-backed measurements, keeping the original
expectation visible for comparison.
