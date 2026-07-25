# Stage 07 E2E plan — qualification and retirement

Status: `NOT_RUN`.

## 0. Imported Stage 03 deferral matrix

The eight `S03-Q07` children transferred in
[`spec.md` §0](spec.md#0-imported-stage-03-deferrals) are mandatory Stage 07
work, not optional context:

| Transfer ID | Exercised by this plan | Required terminal evidence |
| --- | --- | --- |
| `S07-X03-01` | §7 environment matrix | every supported/unsupported cell is explicit; immutable revision/image and effective kernel/filesystem/backend facts; cross-cell ID equality |
| `S07-X03-02` | §3 performance, space and memory | complete Preparation 04 64/256/1024 MiB input/history × 1/16/64-root RSS/resource matrix and bounded-owner counters |
| `S07-X03-03` | §3 and §8 evidence/decision | matched five-minute baseline/candidate campaigns, three valid invocations per selection cell and explicit threshold decision |
| `S07-X03-04` | §§1–4 cumulative/fault/soak/rollback | exhaustive corpus, long soak, restart storm, release variance and exact cleanup/residue evidence |
| `S07-X03-05` | §§1 and 3 | real Stage 04 cold/warm materialization, strict activation, lease/fence and capability replay |
| `S07-X03-06` | §§1–3 and 5 | real Stage 05 common replacement, two-phase root admission, two-cycle GC, singleton retirement, and fault replay |
| `S07-X03-07` | §§4–5 | genuine Stage 06 rollback/re-cutover plus separately approved Stage 07 retirement and candidate-only restart |
| `S07-X03-08` | §§1, 2 and 5 | retained content/attribution/checkpoint proof across every real destructive later-stage transition |

All rows start `OPEN`. Intermediate-stage results are prerequisite inputs; Stage
07 must bind the terminal verdict to the exact release artifact, retained raw
artifacts and cleanup boundary.

## 1. Cumulative correctness

Run all Stage 00–06 suites on the release artifact. Add cross-stage
sequences:

- publish→checkpoint→branch/MCTS→materialize→squash→compact→GC→restart;
- dirty checkpoint→reset→revert→checkpoint deletion→concurrent GC;
- attribution/blame through edit→rename→checkpoint→squash→compact→GC→restart;
- lost publication response followed by another admission and restart;
- authority cutover→candidate writes→rollback→v1 writes→re-cutover;
- retained old checkpoint through carrier evacuation and retirement preparation.
- candidate publication/checkpoint creation across GC fence changes and root-log
  saturation, followed by two complete negative observations and bounded retirement.

Every visible root reconstructs exactly or the operation fails closed before
visibility.

## 2. Fault campaign

Inject process kill, host restart, short write, fsync/rename failure, ENOSPC, corrupt
object/page/pack/locator/ref/state, stale lease, clock jump, missing carrier, GC run
corruption, and response loss at every failure boundary in the canonical contract.

Assert:

- old or complete new visibility only;
- retry returns exact outcome or stable typed expiry/conflict;
- uncertainty retains;
- no ref points to an incomplete graph;
- no last locator/current generation is deleted;
- no broad/recursive recovery deletion;
- `Pending` ambiguity restores exact sources and durable `Deleting` resumes only exact
  recorded destination unlinks;
- no task/permit/FD/mapping/lease/mount/temp-path leak.

## 3. Performance, space, and memory

Execute every Preparation 04 corpus/cell and record:

- first import and repeated small edits at growing tree/history size;
- same/disjoint concurrency, lock waits, retry/progress;
- cold/warm native routes and depth;
- checkpoint/fork/MCTS allocation;
- packs/locators/GC/squash/evacuation;
- Stage 05 `W_gc`, root-log, retirement-ledger, hold, generation, FD, worker, queue, and
  byte-permit caps;
- settled and peak unique/duplicate/staging/metadata/slack/unreachable bytes;
- RSS, queues, workers/tasks, FDs, mappings, caches, operation residue;
- foreground latency under maintenance and long soak.

No full file/tree/history/all-live collection is allowed. Replay the Stage 05 peak
accounting `settled + T_build + H_gen + H_gc + H_trash`, including long-reader,
restart-recovery, and ledger-backpressure cases. Every retained unreachable byte must
name its root/hold/selector/operation/authority/corruption/resource blocker; settled
unexplained unreachable/unleased bytes must be zero.

## 4. Rollout and rollback

- qualify under explicit opt-in before default;
- exercise default cohorts and configured automatic/operator rollback thresholds;
- prove authority rollback produces a writable verified v1 result;
- publish in v1, re-import, and re-cut over;
- run rollback during load, maintenance, session activity, restart, and disk pressure;
- confirm one writer and immutable route per session at all times.

## 5. Retirement rehearsal and execution

Before destructive approval:

- enumerate every v1-dependent root/object/carrier/lease/session/operation;
- evacuate every retained root to verified non-v1 locators;
- prove enumeration is empty with disk-backed/bounded processing;
- page the exact v1 target inventory through fixed buffers and prove target count does
  not create a resident all-target vector/map/set;
- prove candidate-only admission cannot create a new v1 dependency after rollback is
  fenced;
- verify Stage 05 ledger capacity or stop before `candidate-retired`; and
- rehearse retirement without deletion and perform a final rollback.

After explicit approval:

- inject failure before/after candidate-retired `CONTROL`, parent fsync, installation
  of the no-new-v1-dependency admission rule, source-hold release, ledger submission,
  every `Pending` inventory fsync/exact rename/parent fsync, durable `Deleting`, every
  unlink, `Done`, and authorization-operation cleanup;
- require each final ledger predicate to match candidate-retired authority epoch,
  `rollback_allowed=false`, no v1-dependent root/operation/session/selector/hold, and
  verified selected replacement locators;
- prove the authorization operation's exact target inventory is deletion evidence,
  not a logical root/source hold that permanently blocks its own retirement;
- resume candidate-only admissions after the rollback fence without holding an
  authority lock across ledger service; race new publications, checkpoints, GC, and
  restart with physical retirement;
- fill the ledger and prove bounded backpressure leaves candidate authority and exact
  sources/recovery state safe;
- corrupt each authorization/ledger field and prove uncertainty retains;
- assert Stage 07 invokes no direct unlink, creates no trash owner/deletion state
  family, and never targets `/eos/workspace`, `/eos/storage`, or `/eos/runtime`; and
- assert no `refs/legacy`/new legacy directory ever existed.

Restart must recover authority only from `CONTROL`, recover exact physical deletion
only through Stage 05 `Pending`/`Deleting`/`Done`, and never infer targets. Candidate-
only publication/materialization/GC then passes with no migration-only operation work
or v1 path. Unreachable v1 residue must converge to zero or carry an explicit blocker
and keep Stage 07 `OPEN`.

## 6. Phase 2/3 suites

Run branch/checkpoint/MCTS/merge-promotion/conflict/retention/depth suites and portable
provider contract suites. Verify v2 IDs remain readable and v2→v3 import yields an
explicit distinct v3 ID.

## 7. Environment matrix

Run exact pinned glibc, musl, minimal/distroless, shell-less, read-only, non-root,
amd64, and arm64 cells on the qualified Linux backend. Use public file/workspace APIs
when command execution is unavailable. Separately record Linux Engine/Desktop-VM
guest kernel, OverlayFS/mount capabilities, `/eos` backing filesystem, architecture,
and image digest. Prove zero target helper/system-tool dependency. Unmeasured
host/backing-filesystem/image cells remain unsupported; do not infer universal or
percentage compatibility.

## 8. Evidence and decision

The [overall scorecard](../stage_03_07_benchmark_note.md) links every raw artifact,
command, revision, threshold, result, and approval. Missing cells remain `OPEN`.
Qualification, default, and retirement decisions are separate signed/owned entries.
The decision record must name every `S07-X03-*` row and may not collapse the eight
transfers into one inferred pass.
