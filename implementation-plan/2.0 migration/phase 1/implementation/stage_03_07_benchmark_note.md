# LayerStack Stage 03–07 benchmark scorecard

Overall status: **CUMULATIVE QUALIFICATION OPEN**.

Stage 03 now has a bounded correctness POC PASS with retained artifacts. It did
not make a performance-selection, release-qualification, default, rollout, or
retirement claim. Stages 04–07 remain `NOT_RUN`, and the eight Stage 03
deferrals are explicitly transferred to the
[Stage 07 ledger](stage_07_qualification_retirement/benchmark_note.md#imported-stage-03-deferral-ledger).

Normative thresholds:
[Preparation 04](../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md).

## 1. Active-stage status

| Active stage | Scope | Status | Note |
| --- | --- | --- | --- |
| 03 | v3 identity, incremental publication, refs/OCC/recovery | `POC PASS / S03-Q07 OPEN` | [note](stage_03_incremental_publication/benchmark_note.md) |
| 04 | materialization and strict native activation | `NOT_RUN` | [note](stage_04_candidate_materialization/benchmark_note.md) |
| 05 | packs/locators, retention, GC, squash | `NOT_RUN` | [note](stage_05_retention_gc_packs/benchmark_note.md) |
| 06 | candidate authority and v1 authority rollback | `NOT_RUN` | [note](stage_06_candidate_authority/benchmark_note.md) |
| 07 | qualification/default/retirement | `NOT_RUN` | [note](stage_07_qualification_retirement/benchmark_note.md) |

Stage 03’s POC status does not close any cumulative release row below. The
Stage 07 owner must close `S07-X03-01` through `S07-X03-08` with the release
artifact evidence defined in the Stage 07 spec.

## 2. Correctness and crash scorecard

| Gate | Status | Artifact |
| --- | --- | --- |
| owner-approved v3 bounded Merkle identity; v2 compatibility | `OPEN` | — |
| canonical hostile codec/golden suite | `NOT_RUN` | — |
| incremental publication exactness and structural sharing | `NOT_RUN` | — |
| persistent attribution/blame correctness and content-ID independence | `NOT_RUN` | — |
| conflict-key/OCC/disjoint progress | `NOT_RUN` | — |
| idempotency, lost response, outcome expiry | `NOT_RUN` | — |
| checkpoint/branch/MCTS/checkout/revert/reset semantics | `NOT_RUN` | — |
| exact cold reconstruction and strict no-fallback warm route | `NOT_RUN` | — |
| last-locator/source-protection/restart safety | `NOT_RUN` | — |
| concurrent GC barrier, grace, trash, final recheck | `NOT_RUN` | — |
| same-root squash/checkpoint survival | `NOT_RUN` | — |
| candidate cutover, genuine v1 authority rollback, re-cutover | `NOT_RUN` | — |
| retirement evacuation and candidate-only restart | `NOT_RUN` | — |

## 3. Complexity/performance scorecard

| Gate | Required shape/threshold | Status |
| --- | --- | --- |
| first import | `O(R+E)` trend | `NOT_RUN` |
| later publication | changed input/entries/chunks/touched pages; no total tree/history | `NOT_RUN` |
| attribution update/query | touched attribution pages/query paths only; no operation-history scan | `NOT_RUN` |
| no-op publication | bounded proof; zero new payload | `NOT_RUN` |
| same/disjoint writers | stable conflicts and Preparation 04 progress/throughput | `NOT_RUN` |
| clean checkpoint/fork | `O(1)` metadata, zero payload/native tree | `NOT_RUN` |
| dirty checkpoint | normal publication plus one ref | `NOT_RUN` |
| warm route | native I/O only, `D≤64`, no CDC/object/pack/GC work | `NOT_RUN` |
| cold materialization | streamed `O(R+E+D)` | `NOT_RUN` |
| same-key cold concurrency | one fenced build, bounded waiters/orphan residue | `NOT_RUN` |
| concurrent session sharing | shared immutable carriers, isolated private uppers, stable leases | `NOT_RUN` |
| squash | `O(S+E_s)` build, bounded pointer pause | `NOT_RUN` |
| compaction | selected bytes/records only, bounded merge | `NOT_RUN` |
| GC | `O(V+edges)` disk mark, streamed `O(A)` sweep, bounded RAM | `NOT_RUN` |
| authority rollback | streamed `O(R+E)`, bounded quiesce/pointer pause | `NOT_RUN` |
| foreground tails under maintenance | Preparation 04 limits | `NOT_RUN` |

## 4. Space and bounded-resource scorecard

| Gate | Status |
| --- | --- |
| structural sharing and unique retained history | `NOT_RUN` |
| attribution-page sharing and measured blame metadata | `NOT_RUN` |
| no current full payload duplication outside bounded migration/build overlap | `NOT_RUN` |
| metadata amplification, locator runs, operation outcomes/residue | `NOT_RUN` |
| pack slack, unreachable bytes, mark-run/trash staging | `NOT_RUN` |
| materializations only for active/explicitly pinned roots | `NOT_RUN` |
| materialization/staging/upper quotas and no active lease eviction | `NOT_RUN` |
| exact Preparation 04 RSS/queue/worker/buffer/cache/semaphore caps | `NOT_RUN` |
| bounded FDs, mappings, tasks, iterators, leases, retries, deletion batches | `NOT_RUN` |
| no detached tasks/strong cycles/all-live resident set/refcount deletion | `NOT_RUN` |
| restart residue bounded and measured | `NOT_RUN` |

Each space report separates logical payload, physical payload, duplicate overlap,
metadata, operation staging, GC mark/candidate/trash, native generations, uppers, pack
slack, and unreachable residue. A zero denominator uses a reported absolute metadata
floor rather than a misleading ratio.

## 5. Environment/dependency scorecard

| Cell | Status |
| --- | --- |
| glibc | `NOT_RUN` |
| musl | `NOT_RUN` |
| minimal/distroless | `NOT_RUN` |
| shell-less | `NOT_RUN` |
| read-only target root | `NOT_RUN` |
| non-root | `NOT_RUN` |
| amd64 | `NOT_RUN` |
| arm64 | `NOT_RUN` |
| Linux Docker Engine native backend | `NOT_RUN` |
| supported Docker Desktop Linux-VM backend | `NOT_RUN` |
| qualified `/eos` backing filesystems/providers | `NOT_RUN` |
| bind/translated/remote backing-store rejection or explicit qualification | `NOT_RUN` |
| no target helper/system-tool/dependency use | `NOT_RUN` |
| cross-cell logical ID determinism | `NOT_RUN` |

Exact pinned image digests, effective Linux guest kernel, mount capability profile,
and `/eos` backing filesystem configuration remain `OPEN`. The matrix makes no native
macOS/Windows, universal OCI, or image-percentage claim.

## 6. Phase 2/3 scorecard

| Gate | Status |
| --- | --- |
| branch/checkpoint/MCTS metadata-only clean fork | `NOT_RUN` |
| active-only writable/materialization allocation | `NOT_RUN` |
| deterministic merge/promotion/conflict semantics | `NOT_RUN` |
| GC safety for frontier/checkpoint/promotion refs | `NOT_RUN` |
| bounded native depth independent of logical ancestry | `NOT_RUN` |
| filesystem provider contract suite | `NOT_RUN` |
| alternate deterministic provider contract suite | `NOT_RUN` |
| provider physical data excluded from IDs | `NOT_RUN` |

## 7. Required evidence format

Every populated row records:

- exact command and git revision;
- benchmark/test code revision and configuration;
- corpus/fixture/image digest;
- host, kernel, filesystem/provider, CPU architecture, target image;
- Linux Engine/Desktop-VM backend, mount capability profile, and `/eos` storage kind;
- declared variables (`R,E,U,E_changed,K,P,N,Q,D,V,A,S`);
- raw artifact path and sample distribution;
- peak/settled byte and resource counters;
- threshold, measured value, `PASS`/`FAIL`;
- variance, failure, and retry explanation;
- owner approval for qualification/default/retirement decisions.

No row changes from `NOT_RUN`/`OPEN` based on design inspection.
