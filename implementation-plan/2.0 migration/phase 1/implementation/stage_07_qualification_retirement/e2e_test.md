# Stage 07 E2E plan — qualification and retirement

Status: `NOT_RUN`.

## 0. Imported Stage 03 deferral matrix

The eight `S03-Q07` children transferred in
[`spec.md` §0](spec.md#0-imported-stage-03-deferrals) are mandatory Stage 07
work, not optional context:

| Transfer ID | Exercised by this plan | Required terminal evidence |
| --- | --- | --- |
| `S07-X03-01` | §7 environment matrix | every supported/unsupported cell is explicit; immutable revision/image and effective kernel/filesystem/backend facts; cross-cell ID equality |
| `S07-X03-02` | §3 performance, space and memory | complete 64/256/1024 MiB × 1/16/64-root RSS/resource matrix and bounded-owner counters |
| `S07-X03-03` | §3 and §8 evidence/decision | matched five-minute baseline/candidate campaigns, three valid invocations per selection cell and explicit threshold decision |
| `S07-X03-04` | §§1–4 cumulative/fault/soak/rollback | exhaustive corpus, long soak, restart storm, release variance and exact cleanup/residue evidence |
| `S07-X03-05` | §§1 and 3 | real Stage 04 cold/warm materialization, strict activation, lease/fence and capability replay |
| `S07-X03-06` | §§1–3 and 5 | real Stage 05 pack/locator/GC/squash/destructive-retention replay and fault campaign |
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
- no task/permit/FD/mapping/lease/mount/temp-path leak.

## 3. Performance, space, and memory

Execute every Preparation 04 corpus/cell and record:

- first import and repeated small edits at growing tree/history size;
- same/disjoint concurrency, lock waits, retry/progress;
- cold/warm native routes and depth;
- checkpoint/fork/MCTS allocation;
- packs/locators/GC/squash/evacuation;
- settled and peak unique/duplicate/staging/metadata/slack/unreachable bytes;
- RSS, queues, workers/tasks, FDs, mappings, caches, operation residue;
- foreground latency under maintenance and long soak.

No full file/tree/history/all-live collection is allowed.

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
- rehearse retirement without deletion and perform a final rollback.

After explicit approval, inject failure before/after candidate-retired `CONTROL`,
ordinary source-lease release, each exact existing-v1 deletion batch, and operation
cleanup. Assert no `refs/legacy`/new legacy directory ever existed. Restart must retain
or resume exact state. Candidate-only publication/materialization/GC then passes with
no migration-only operation work or v1 path.

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
