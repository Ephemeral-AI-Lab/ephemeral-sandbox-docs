# Stage 07 — qualification, default, and retirement

Status: specification only; all benchmark and environment results are open.

Normative dependencies:

- [implementation index](../index.md)
- [minimal storage contract](../layerstack_storage_contract.md)
- [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)
- [Stage 03 final handoff](../stage_03_incremental_publication/handoff_to_stage_04.md)
- [Stage 03 benchmark note](../stage_03_incremental_publication/benchmark_note.md)
- all Stage 03–06 exit evidence

## 0. Imported Stage 03 deferrals

Stage 03 closed as a bounded correctness POC while its canonical
`S03-Q07` row remained `DEFERRED_STAGE_07`. Stage 07 owns final closure of the
following transferred rows. An owning intermediate stage may supply prerequisite
evidence, but no row becomes `PASS` until Stage 07 replays or validates it against
the exact release artifact and records the required raw artifacts, thresholds,
environment, cleanup, and approval.

| Transfer ID | Stage 03 deferred scope | Required prerequisite | Stage 07 closure evidence | Initial status |
| --- | --- | --- | --- | --- |
| `S07-X03-01` | full host/filesystem/architecture qualification beyond the approved Stage 03 portability cases | Stage 03–06 release candidate and complete environment adapter support | every §8 cell identified by immutable image/revision, guest kernel, backing filesystem/provider, mount/backend capabilities and architecture; cross-cell logical IDs match; unsupported cells fail closed | `OPEN` |
| `S07-X03-02` | full 64/256/1024 MiB × 1/16/64-root RSS matrix | final publication, materialization, pack/locator, GC and authority routes | Preparation 04 matrix with idle/peak/settled RSS, queues, buffers, workers/tasks, FDs/mappings, cache/permit ownership, raw distributions and cap verdicts | `OPEN` |
| `S07-X03-03` | full five-minute matched candidate/baseline allowance and three-invocation selection-advantage decision | qualified baseline/candidate pair on the same release revision, corpus and host cell | matched five-minute campaigns plus at least three valid invocations per decision cell, variance and exclusion accounting, threshold comparison and explicit selection decision | `OPEN` |
| `S07-X03-04` | exhaustive corpus, long-duration soak, restart storm and release-variance matrix | all Stage 03–06 mechanisms and fault seams integrated | corpus manifest/digest, soak duration, restart/fault schedule, per-release distributions, cleanup ledger, unexplained-residue zero and bounded rollback behavior | `OPEN` |
| `S07-X03-05` | real Stage 04 materialization/activation behavior | Stage 04 exit evidence | release-artifact replay of exact cold reconstruction, strict no-fallback warm route, generation fencing/leasing, capability rejection and resource/space bounds | `OPEN` |
| `S07-X03-06` | real Stage 05 packs, locator compaction, GC, squash and destructive retention | Stage 05 exit evidence | release-artifact replay of pack/locator replacement, same-root squash, disk-backed trace/sweep, grace/trash/final recheck, restart and last-location safety | `OPEN` |
| `S07-X03-07` | Stage 06 public authority cutover/fallback plus Stage 07 retirement | Stage 06 reversible cutover/rollback exit evidence | genuine candidate→v1 rollback, verified v1 publication, re-cutover, separate qualification/default/retirement approvals, evacuation proof and candidate-only restart | `OPEN` |
| `S07-X03-08` | end-to-end attribution/checkpoint survival through real later-stage destructive operations | `S07-X03-05` through `S07-X03-07` prerequisites | immutable attribution and retained checkpoint roots survive materialize→squash→compact→GC→restart→cutover/rollback→retirement rehearsal with unchanged content identity and exact blame | `OPEN` |

The source inventory is
[Stage 03 guide §15.4](../stage_03_incremental_publication/implementation_instructions.md#154-explicit-stage-07-deferrals).
Stage 03 campaign correctness evidence is a prerequisite, not a substitute for
these release-qualification rows.

## 1. Outcome

Stage 07 introduces no storage format or runtime mechanism. It performs three ordered,
separately approved gates:

1. **opt-in qualification** while candidate authority remains reversible;
2. **candidate default and soak** with rollback continuously rehearsable;
3. **legacy retirement** only after an explicit destructive approval.

Default does not precede correctness/performance qualification. Retirement is not an
automatic consequence of a successful soak.

## 2. Qualification gate

Qualification requires one coherent artifact set proving:

- v2 fixtures remain readable and v3 identity golden vectors are frozen;
- incremental publication scales with changed input/touched pages, not tree/history;
- OCC conflict semantics and disjoint progress;
- idempotency/lost-response recovery at every commit boundary;
- checkpoint/branch/MCTS semantics and zero-payload clean refs;
- persistent attribution/blame across edit, rename, revert/reset, checkpoint, squash,
  compaction, GC, and restart without content-identity changes;
- exact cold reconstruction and strict warm native routing;
- same-root squash and checkpoint survival;
- locator replacement, concurrent GC barrier, grace/trash/final recheck, conservative
  restart, and last-locator protection;
- genuine candidate→v1 authority rollback and re-cutover;
- safe Rust, bounded resources, no detached tasks/cycles, and no all-live resident set;
- complete Preparation 04 performance/space gates;
- complete environment/dependency matrix;
- Phase 2/3 contract compatibility.

Any missing required row is `OPEN`, not implicitly passed.
That rule includes every `S07-X03-*` transfer row above.

## 3. Candidate default and soak

After qualification approval:

- new installations/default routing select candidate authority;
- v1 reader/writer/artifacts remain available and protected;
- rollback-compatible capability enforcement remains active;
- a bounded rollout cohort and error/latency/space budget are defined;
- long-soak workloads cover publication, checkpoint churn, MCTS forks, materialization,
  squash, compaction, GC, restart, process kill, disk pressure, and authority rollback;
- operator-triggered and automated rollback thresholds are tested;
- every rollback is followed by verified v1 publication and a fresh forward catch-up.

No soak observation may delete the legacy rollback source.

## 4. Retirement prerequisites

Retirement requires all of:

1. a separately recorded owner approval naming release/revision and rollback window;
2. the full qualification and default-soak matrices pass;
3. a recent authority rollback and re-cutover rehearsal pass on the release artifact;
4. every retained root/checkpoint/pin has an independently verified non-v1 last
   locator;
5. no active/prepared operation, lease, materialization, session, locator generation,
   GC cycle, or policy root depends on v1;
6. v2 roots required by compatibility remain readable/importable even if production
   starts at v3;
7. `CONTROL` names candidate authority, the store is quiescent, and the prepared
   retirement operation contains the approval that will atomically mark rollback
   ineligible;
8. exact legacy deletion targets are enumerated and backed up/recoverable according to
   release policy.

If any proof is uncertain, retain legacy.

## 5. Retirement operation

Retirement is one common maintenance operation:

1. fence authority and mutation admissions;
2. recheck all prerequisites and active ownership;
3. record the approval identifier and retirement proof in the operation `STATE`, then
   atomically update top-level `CONTROL` to `{format_version,
   authority=candidate-retired,new_epoch,rollback_allowed=false,
   active_migration_operation_id}`;
4. release ordinary migration/source leases only after every retained root has a
   verified non-v1 locator;
5. hand exact existing v1 `manifest.json`, `workspace.json`, `base`, `layers`,
   `staging`, and `.layer-metadata` targets to Stage 05
   grace/final-recheck deletion;
6. retain the terminal operation only for the declared bounded response/audit window,
   then release its work; there is no retirement receipt/ref family;
7. clear `CONTROL.active_migration_operation_id` after the operation is terminal and
   the same authority epoch still names it;
8. resume candidate-only admissions.

The operation never recursively deletes `/eos`, `/eos/layer-stack`, a workspace root,
or a glob-derived target. Product data removal is exact and recoverable until its
declared final boundary.

After retirement, rollback means candidate checkpoint/head reset/revert; v1 authority
rollback is unavailable and APIs report that explicitly.

## 6. Phase 2 qualification

Contract suites must show:

- clean checkpoint/branch/MCTS frontier retention is `O(1)` metadata and zero payload;
- only active forks allocate private uppers/materializations;
- base/left/right merge and promotion have deterministic conflict keys including
  ancestor/descendant, rename, opaque-directory, and hardlink effects;
- promotion is an atomic head CAS with normal idempotency/recovery;
- squash/materialization bounds native depth without altering roots;
- checkpoint/frontier creation participates in concurrent GC barriers;
- publication transition/blame uses the Phase 1 immutable attribution object graph and
  never becomes a `RootId` identity input or operation-history dependency.

## 7. Phase 3 qualification

Run the logical provider contract against the Phase 1 filesystem adapter and at least
one test/deterministic alternate adapter:

- typed immutable put-if-absent/get/corruption;
- atomic/fenced ref update and lost response;
- bounded iteration and locator lookup;
- missing/corrupt object behavior;
- native materialization;
- capability rejection;
- no provider location/credential/path in logical IDs.

This is a contract audit, not authorization to add a service or dependency in Phase 1.

## 8. Environment, native backend, and dependency matrix

Required cells include:

- glibc and musl;
- minimal/distroless and shell-less;
- read-only target root;
- non-root;
- amd64 and arm64;
- Linux Docker Engine and supported Docker Desktop Linux-VM configurations;
- every supported `/eos` backing filesystem/provider configuration, recorded
  separately from the host UI OS;
- command-capable and file/workspace-API-only verification.

Exact image digests, host/kernel/filesystem, CPU architecture, revision, commands, and
artifacts are recorded. The target requires no helper, shell, libc/coreutils, package
manager, FUSE, reflink, tar, or `cp`. Identity is unchanged across cells.

The qualified claim is capability-based. Phase 1 does not claim native macOS/Windows
activation, unqualified bind/translated/remote filesystem support, universal OCI
compatibility, or a percentage of Docker images. The principal portability boundary
is the Linux kernel/filesystem/mount and metadata capability profile; target userland
is not required to contain support tools.

## 9. Go/no-go rules

`GO` requires every normative row in the
[overall scorecard](../stage_03_07_benchmark_note.md) to pass with reproducible
artifacts. Correctness, crash safety, GC safety, or environment failure cannot be
waived by a favorable average latency. Performance cannot be declared from asymptotic
prose.

`NO-GO` retains the last reversible authority and all uncertain data. Retirement
failure leaves candidate authority intact or stops safely before candidate-only state;
it never guesses that rollback data is disposable.

## 10. Exit

Stage 07 completes only when:

- qualification approval is recorded;
- candidate default soak passes;
- retirement approval is explicit;
- exact legacy evacuation/deletion evidence passes;
- migration-only state is gone;
- candidate-only restart and GC pass;
- documentation, benchmark notes, links, and terminology agree with the one canonical
  storage contract.
