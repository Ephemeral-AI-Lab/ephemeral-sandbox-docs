# MPLA Booster PoC — Phased Execution, Acceptance, and Progress Specification

Status: `SEALED`  
Owner: Codex `/root`  
Last updated: `2026-08-01`

This is the operational view of the formal MPLA Booster scorecard. It adds a
phase-oriented tracker to the governing [test matrix](test_matrix.md) and the
[scorecard execution spec](booster_scorecard_execution_spec.md); it does not
relax either document. On conflict, the test matrix wins.

## 1. Scope and verdict model

The seven PoC operations are:

1. materialization/activation;
2. fork;
3. rollback;
4. small publication;
5. squash;
6. real 1-GiB stream;
7. crash recovery.

They execute as one administrative cache-construction phase plus nine visible
scorecard phases: setup, the seven operations, and finalization.
Materialization contains two formal gates: exact activation and same-key
activation.

Only these five gates participate in the aggregate multiplier verdict:
`BG-ACTIVATE-EXACT`, `BG-ACTIVATE-SAME`, `BG-FORK`, `BG-ROLLBACK`, and
`BG-PUBLISH-SMALL`. `AG-SQUASH` and `AG-STREAM` have independent absolute
verdicts. `HV-07` is a mandatory correctness/recovery qualifier. Thus, a fast
publication alone can never establish `POC_100X_SUPPORTED`.

### Independent phase files, timers, and verdicts

Administrative phase F0-COLD and each P0–P8 phase own one focused test
file/runner, one fresh process, one immutable evidence root, and one
phase-local wall-clock safety deadline. Elapsed time contributes **only to that
phase's receipt**. There is no aggregate campaign budget, no deadline carry-over
between phases, and no rule that combines fast phases to offset a slow one. The
final decision is the logical conjunction of independently
sealed phase verdicts; F0-COLD and P0-WARM are setup qualifiers, not Booster
operation latency.

| Phase | Required focused test file / runner | What its time measures |
|---|---|---|
| F0-COLD | `build-mpla-publication-fixture-cache --evidence-file fixture-cache-construction.json` | genuine first-time or recovery construction of the sealed, content-addressed 8-GiB logical fixture cache |
| P0-WARM | `mpla_qualification_scorecard` → root `fixture-cache-attachment.json` | read-only attachment of the already sealed cache plus the complete publication-fixture preparation receipt |
| P0 | `mpla_qualification_scorecard` | remaining environment and security qualification, excluding both F0-COLD and the P0-WARM timer |
| P1 | `mpla_activation_scorecard` | exact and same-key activation only, with its matched controls |
| P2 | `mpla_fork_scorecard` | public fork and matched control only |
| P3 | `mpla_rollback_scorecard` | public rollback and matched control only |
| P4 | `mpla_publication_scorecard` | small publication and matched control only |
| P5 | `mpla_squash_scorecard` | logical squash only |
| P6 | `mpla_stream_scorecard` | real changed-1-GiB stream only |
| P7 | `mpla_hv07_scorecard` | registered crash/recovery sweep only |
| P8 | `mpla_sealing_scorecard` | receipt/hash/decision validation; no scored operation latency |

Every phase-local deadline must be documented beside its runner with the work
it bounds. The acceptance metrics in that phase remain the authoritative
performance limits; a deadline is only a liveness guard, never an alternative
pass criterion. A liveness-cap overrun is a visible phase failure (or
`NOT_RUN_BUDGET` before a sample starts), never a pass and never a reason to
borrow time from another phase.

#### Phase-local wall-budget policy

P1 is the deliberate exception. It is the full-corpus activation/control case:
its matrix target is `60 s` and its **fixed phase-local diagnostic cap is
`120 s`**. P1 must not acquire an additional generic extension beyond that
`120 s` cap.

For P2–P7, the runner's declared liveness cap may be from **1.0× through 2.0×**
of the corresponding suggested matrix wall budget. The runner must record the
suggested budget, selected multiplier, calculated cap, and elapsed wall time
in its receipt before it starts. `1.0×` is the default; a value above `1.0×`
is an explicitly recorded diagnostic allowance, not extra scored-operation
time or an acceptance relaxation. These caps are independent; they do not form
a new cumulative campaign budget.

| Phase | Matrix source | Suggested wall budget | Allowed phase-local cap |
|---|---|---:|---:|
| P0 remaining qualification | qualification runner | `60 s` | fixed `60 s` |
| P1 activation | `HV-08` | `60 s` | fixed `120 s` only |
| P2 fork | `HV-10` | `30 s` | `30–60 s` |
| P3 rollback | `HV-10` | `30 s` | `30–60 s` |
| P4 small publication | `HV-01` | `35 s` | `35–70 s` |
| P5 squash | `HV-10` | `30 s` | `30–60 s` |
| P6 real 1-GiB stream | `HV-02` | `20 s` | `20–40 s` |
| P7 crash/recovery | `HV-07` | `60 s` | `60–120 s` |
| P8 sealing and decision | sealing runner | `30 s` | fixed `30 s` |

F0-COLD has a `<5.0 s` outer cache-command acceptance target and a `30 s`
phase-local liveness cap; `1–3 s` is the stretch range. P0-WARM has a `<50 ms`
service-attachment target, a `<1.0 s` complete in-service preparation target,
and a `5 s` phase-local liveness cap. P0's remaining qualification has a fixed
`60 s` phase-local cap; P8 sealing has a fixed `30 s` phase-local cap. They
have no scored operation latency, but their receipts still record elapsed
wall time and fail visibly on their own cap. None can hide or extend P1–P7
timing.

The current grouped `lifecycle` runner (P1/P2/P3/P5) is migration debt and may
not be used for a final phase-level timing claim after this split is
implemented.

P1–P3 use one phase-specific `prepare-lifecycle-control` prerequisite before
their phase clock starts. That prerequisite may collect/hash R0 and create the
single immutable current-I2 closing publication only. It has an independent
`120 s` setup-liveness cap and must report raw collection, closing-publication,
and total preparation timings. Its authenticated receipt is bound into the
phase result. It must prove exactly one immutable publication and zero
materialized carriers. Every cold activation/fork/rollback carrier build,
same-key lookup, readiness probe, matched candidate operation, and intervening
cache reclamation remains inside the applicable P1/P2/P3 phase-local timer.
This setup cap neither extends nor contributes to any phase cap.

## 2. Global acceptance rules

Every measured phase must meet all applicable items below.

- [ ] Use the supported public gateway and CLI boundary; do not substitute a
      helper or direct Docker operation for the public operation being scored.
- [ ] Keep fixture generation, image pulls, sandbox allocation, cache warming,
      and harness preparation outside the operation timer, while retaining
      separate receipts for them.
- [ ] Use `CLOCK_MONOTONIC_RAW`, record the exact start/stop boundary, retain
      raw samples, median, max, and the exact ratio numerator/denominator.
- [ ] For a multiplier claim, candidate and control must have the same fixture,
      intent, logical input availability, timing boundary, durability boundary,
      clock, and independently allocated arms. A missing or mismatched control
      yields `UNKNOWN`, never a speedup claim.
- [ ] Prove exact semantic oracle equality, durability where applicable,
      capability/authorization boundaries, resource bounds, and cleanup back to
      the pre-run manager and observability inventories.
- [ ] Record compact RPC outcome metadata (status, response bytes, digest,
      duration, and error class). Do not store or print an unbounded reply body.
- [ ] Retain failed or invalidated evidence. A hard timeout, OOM, hidden
      payload copy, partial root, stale-token success, unexplained persistent
      bytes, or cleanup leak is never a pass.

### Fixed envelope and evidence common to all phases

| Item | Required record / limit |
|---|---|
| Environment | Docker Desktop `4 vCPU / 4 GiB`; pinned Ubuntu 24.04 Linux/arm64 image; persistent ext4, never tmpfs/ramfs |
| Resources | application pool `≤8 MiB`; storage `memory.high=96 MiB`, `memory.max=128 MiB`; no OOM; record RSS, cgroup memory, FDs, inodes, and I/O |
| Security | authorized lifecycle process proves `CAP_SYS_ADMIN` bit 21 effective/permitted/bounding; ordinary workload proves denial; real OverlayFS mount and strict unmount |
| Per-case evidence | source/config/binary/image/fixture hashes; allocation/lease/owner identities; raw terminal result, spans, resources, correctness, cleanup, and failure reason |
| Final evidence | `environment.json`, `source.json`, `fixture-manifest.json`, `security-profile.json`, `command-ledger.jsonl`, per-gate case receipts, `correctness.json`, `resources.json`, `cleanup.json`, `scorecard.json`, `decision.json`, `report.md`, and freshly re-read `manifest.sha256` |

### Environment, workspace layout, and quick fixture setup

The prepared fixtures and live workspaces have deliberately different roles.
The **R0 corpus** is the near-1-GiB class input: `console-release`, exactly
`912,350,100` logical bytes (`870.08 MiB`), `3,602` files, and `694`
directories. It must not be confused with the S2 large-stream workload, whose
changed upper is exactly `1 GiB`. The **S4-chain** starts from a 1-GiB base and
uses sequential deltas to reach the current 8-GiB logical depth; its formal
maximum remains below 10 GiB (and the scored small-publication points are 1,
5, and at most 9 GiB).

| Role | Location / backing | Lifetime and contents | Quick-setup rule |
|---|---|---|---|
| Prepared fixtures | builder-only read/write `/eos/mpla-fixtures`; consumer read-only mount on persistent ext4 | Canonical R0 and the verified 8-GiB logical S4-chain, each with a manifest and digest | Build in F0-COLD only. Normal consumers cannot select the builder operation or mutate/recover the cache; P0-WARM only attaches and verifies the sealed fixture. Never reconstruct or copy 1/8 GiB during a hot-path timer. |
| Coordinator control state | `/eos/workspace/mpla-poc/scorecard/<run>-lifecycle/controls` on the coordinator's persistent workspace backing | Current-I2 control carrier/state for one matched pair | Complete cold, same-key, fork, and rollback receipts for one pair, retain compact receipts, then reclaim the pair before creating the next one. No three full control trees may accumulate. |
| Candidate runtime state | sandbox-owned persistent LayerStack storage, including `/eos/layer-stack` | Candidate metadata, upper, projection, and mount state | Allocate only after fixture qualification. The candidate timer starts at the formal public-operation boundary, never at fixture generation or volume attachment. |
| Evidence | immutable host-bound evidence root | JSON receipts, spans, hashes, compact RPC metadata, and final manifest | Persist evidence separately from data roots; no unbounded RPC reply body is printed or retained. |

Quick setup therefore means **reuse plus verification**, not a misleading
8-GiB materialization benchmark. F0-COLD is nevertheless a real performance
gate for construction: it may not be renamed “warm,” bypassed, or satisfied by
an already sealed cache. P0-WARM is the normal attach path and may not rebuild
or mutate the cache. Score neither as publication or activation latency.
Before the campaign, calculate the simultaneously live data from the actual
manifests and require that peak plus 20% headroom. For the current 8-GiB
prepared-chain campaign, provision at least 12 GiB of free persistent
Docker-backed storage as an operating floor, then record the exact
`f_bavail`/capacity result for each attempted reservation.

### F0-COLD and P0-WARM measured baseline

The current closed profile is `s4-chain-sparse-v1`: eight exact
content-addressed allocations expose `8,589,934,592` logical bytes while the
sealed Linux extent proof reports zero allocated payload blocks. It replaces
V13's eight dense lifecycle publications. V13 performed a dense write, sync,
and hash for each layer and repeatedly walked the accumulated semantic/oracle
tree, resulting in about `48 GiB` of cumulative scans plus about `9 GiB` of
explicit payload hashing. The recorded V13 cold result was `129.932 s` service
and `133.683 s` wall.

The accepted Final43-v3 physical recovery measurement for
`s4-chain-sparse-v1` used Docker
Desktop on the fixed macOS-hosted `4 vCPU / 4 GiB` envelope with Ubuntu 24.04
Linux/arm64 containers, pinned image
`ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`,
and a persistent named Docker volume. Raw timings were:

| Receipt | Raw result | Bytes copied / allocated |
|---|---:|---:|
| F0-COLD builder service | `1,102,406,542 ns` (`1.102406542 s`) | `0 / 0` |
| F0-COLD cache-command outer | `1,228,642,917 ns` (`1.228642917 s`) | `0 / 0` |
| Cache-command orchestration overhead | `126,236,375 ns` | n/a |
| Docker sandbox setup, separate platform overhead | `2,198,345,375 ns` | n/a |
| Artifact staging, separate harness overhead | `43,895,500 ns` | n/a |
| Launcher start through pre-cleanup | `3,471,067,000 ns` | `0` payload bytes copied |
| Whole launcher process (`/usr/bin/time`) | `3.99 s` | `0` payload bytes copied |

The genuine recovery removed only the exact unsealed cache roots, rebuilt all
eight allocations, sealed the manifest, and improved outer construction by
`108.81×` versus `133.683 s` (service improvement `117.86×` versus
`129.932 s`). The accepted receipt is
`mpla-final43-f0-v3-20260731t072650z@9490df6403472941b81d00bdd21dc00ebf4df88e42bfb6f58235d0b320f91a5c`.
Corrupt or unknown sealed state remains a
fail-closed error, not an automatic deletion.

Earlier repeat-attachment measurements and the final P0-WARM qualification
against that sealed volume were:

| Run | Attachment service | Complete in-service fixture preparation | Harness outer | Payload bytes copied |
|---|---:|---:|---:|---:|
| `mpla-warm-sparse-v1-a` | `23,010,084 ns` | `529,899,292 ns` | `1,135,584,208 ns` | `0` |
| `mpla-warm-sparse-v1-b` | `19,368,500 ns` | `490,085,667 ns` | `1,113,340,875 ns` | `0` |
| `mpla-final34-p0-20260731t014411z` | `24,825,208 ns` | `374,467,417 ns` | phase `2,120,485,208 ns` | `0` |

All three warm receipts prove operation `attach_mpla_prepared_fixture`, the exact
eight cached allocations, branches `fixture-depth-1`, `fixture-depth-5`, and
`fixture-depth-8`, and zero copied payload bytes. The roughly `0.6 s` excess of
harness outer time over in-service preparation is asynchronous CLI polling;
it is reported separately and is not attachment service time.

## 3. Progress tracker

Use the states `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL_REPAIRING`,
`FAIL_SEALED`, `HARD_BLOCKED`, or `INVALIDATED`. A `PASS` is final only when the relevant
source/config/binary/fixture/image hashes are still current; otherwise mark it
`INVALIDATED` and create a new phase-local run before P8. P8 validates sealed
receipts and never re-runs predecessor workloads.

| ID | Phase / formal gates | Current state | Current evidence or blocker | Next completion event |
|---|---|---|---|---|
| P0 | Setup and qualification | `PASS` | Final34 P0 passed in `2.120485208 s` under its own `60 s` cap. Its independent P0-WARM receipt records `24.825208 ms` attachment service, `374.467417 ms` complete preparation, and zero copied payload bytes. | Complete; sealed manifest `858024156c4b60f44d96198a004ffce6360928f4f1cc0c820532a357a6d80537` |
| P1 | Materialization: `BG-ACTIVATE-EXACT`, `BG-ACTIVATE-SAME` | `PASS` | Final34b passed both gates in `85.129972292 s` under the fixed independent `120 s` cap. | Complete; sealed manifest `0d3e6c79487aabb3fca25048577d72ec2a151f7cc7751589888d2f02ec173d9f` |
| P2 | Fork: `BG-FORK` | `PASS` | Final34 passed the public fork gate in `52.723843000 s` under its independent `60 s` cap. | Complete; sealed manifest `134bb7e53b99d6fe485838135545fe1d54f21ea695c9b1dfb3e6d57cb962dd7b` |
| P3 | Rollback: `BG-ROLLBACK` | `PASS` | Final40 passed the public rollback gate in `51.757623833 s` under its independent `60 s` cap. | Complete; sealed manifest `7571405d1e65919e82e8bc1efed2f3a8b717509f880c2364f8ab0d8e179f48ad` |
| P4 | Publication: `BG-PUBLISH-SMALL` | `FAIL_SEALED` | Final50 completed in `22.881794000 s` under its independent `70 s` cap. All candidates were below `100 ms`, but the valid matched medians were candidate `58.136209 ms` and current-I2 control `36.444000 ms`, only `0.626872660×`; `BG-PUBLISH-SMALL=false` remains an honest formal failure. | Complete; sealed manifest `ca38a57d6a93fd268e2f696a78e234bf73f3dccfdf64e1fd6883ae46438bfc96` |
| P5 | Squash: `AG-SQUASH` | `PASS` | Final54 passed in `29.591311167 s` under its independent `60 s` cap. | Complete; sealed manifest `e443d68c253ace8401b4b0a3e6d4dc82f545ff1ea3c5a793a4f84533432275fc` |
| P6 | Stream: `AG-STREAM` | `PASS` | Final61 passed a real changed-1-GiB stream at `994.910 ms` (`1.079 GB/s`), with phase wall `8.363238417 s` under its independent `40 s` cap. | Complete; sealed manifest `653a56a8fe2dbd17e8648ca18877c1eae75a195218e88ebcb95f6f7be43901e4` |
| P7 | Recovery: `HV-07` | `PASS` | Final70 completed all `46/46` registered points in `21.349401583 s` phase wall (`15.867793590 s` campaign, `14.438988090 s` sweep) under its independent `120 s` cap, with one build and 45 exact reuses, zero payload copies, no OOM, and exact cleanup. | Complete; sealed manifest `3362305560b61d1e827221bcde1e92f53b72bdcb9ec6667020d127a4902349c2` |
| P8 | Final qualification, sealing, decision | `PASS` | Final73 sealed in `396,731,209 ns` (`0.57 s` process wall) under its independent fixed `30 s` cap and rehashed all 14 manifest entries. It preserved Final50 as failed. | Complete; manifest `837578247484c38c95285b12c0e7710b66546e643c3132f3368aa3c87891638f`; `POC_CORRECTNESS=PASS`, `AG_SQUASH=PASS`, `AG_STREAM=PASS`, `POC_100X=NOT_SUPPORTED`, `POC_500X=NOT_SUPPORTED` |

### Attempt ledger template

Append one row after every material attempt; never delete failures.

| UTC | Phase/gate | Run ID and evidence root | Source/config/binary/fixture identity | Samples or fault points | Result / failure reason | Next action |
|---|---|---|---|---|---|---|
| `<UTC>` | `<P# / gate>` | `<unique immutable root>` | `<hashes>` | `<raw values or count>` | `PASS / FAIL_REPAIRING / INVALIDATED` | `<one bounded next action>` |

## 4. Phases F0-COLD and P0 — fixture cache, setup, and qualification

Purpose: construct or recover the sealed fixture once, then prove normal
read-only attachment, the environment, and the public control plane before any
scored work.

Acceptance list:

- [ ] Create a unique, absent evidence root and capture source tree, dirty-state,
      config, executable, image, and fixture identities.
- [ ] Verify the exact R0 path (`console-release`), `912,350,100` logical
      bytes, `3,602` files, and `694` directories; reject its 1.72-GiB parent
      directory.
- [ ] In F0-COLD, build and digest-verify the near-1-GiB R0 corpus and the
      8-GiB logical S4-chain once on persistent ext4. Start with the cache
      absent or an explicitly recoverable unsealed cache; prove `<5.0 s` outer,
      exact eight-allocation identity, the sealed manifest, and zero copied
      payload bytes.
- [ ] In P0-WARM, mount the same cache read-only and write
      `fixture-cache-attachment.json`. Require attachment service `<50 ms`,
      complete in-service preparation `<1.0 s`, the exact three branches and
      eight cached allocations, and zero copied payload bytes. Per-run setup
      may not rebuild or mutate either fixture.
- [ ] Reject stale, partial, symlinked, unknown, or corrupt cache layouts
      before consumer use. Recovery may remove only the exact known unsealed
      roots; a corrupt sealed cache fails closed and requires an explicit
      administrative recovery decision.
- [ ] Prove peak disk plus 20% margin and chain size `<10 GiB` before generation;
      use at least 12 GiB free persistent Docker-backed storage for the current
      8-GiB campaign, then retain the actual calculation.
- [ ] Before every control or candidate materialization, record its predicted reservation,
      aggregate reservations, filesystem available/capacity bytes, and the
      resulting headroom. Fail closed if the candidate cannot fit; never turn a
      storage preflight failure into a benchmark sample.
- [ ] Retain only compact control receipts after each matched pair; synchronously
      reclaim that pair's carrier/state tree before provisioning the next pair.
- [ ] Rebuild the gateway with `bin/start-sandbox-docker-gateway --rebuild-binary`;
      verify readiness and baseline inventories only through supported CLIs.
- [ ] Prove persistent ext4, real OverlayFS mount/strict-unmount, authorized
      capability, and ordinary-workload denial.
- [ ] Confirm public operation catalog coverage and independent candidate/control
      allocation paths; add the append-only `TEST-REPORT` PENDING entry before a
      test command.

| Metric | Required / recorded value | Scored? |
|---|---|---|
| Setup wall time | Record separately from every operation timer | No |
| F0-COLD construction | `fixture-cache-construction.json`; genuine absent/recovery cache; outer `<5.0 s`, stretch `1–3 s`, liveness cap `30 s` | Setup performance gate; not a Booster operation |
| P0-WARM attachment | `fixture-cache-attachment.json`; service `<50 ms`, complete in-service preparation `<1.0 s`, liveness cap `5 s`; exact eight allocations/three branches/zero copy | Setup performance gate; not a Booster operation |
| Disk headroom | Expected peak plus `20%` before generation | Qualification gate |
| Materialization-store headroom | Per-control and per-candidate reservation, aggregate, available and capacity bytes | Qualification gate |
| Environment | `4 vCPU / 4 GiB`, Ubuntu 24.04 Linux/arm64, persistent ext4 | Qualification gate |
| Control plane | CLI calls, polls, bytes returned, and control-plane overhead | Guardrail; no poll storm |

## 5. Phase P1 — materialization and activation

This phase measures a usable workspace session, not host compilation or
fixture preparation. Record compact RPC response metadata and first
`exec_command` readiness separately from the operation timer.

Acceptance list:

- [ ] `BG-ACTIVATE-EXACT`: exact R0 / `HV-08` activation versus `R0-C01`, with
      zero-build `R0-03` precondition, three matched pairs, five cached repeats,
      and projection depths `1/4/8`.
- [ ] Exact hits prove zero hydration, reconstruction, and immutable-payload
      reads; stable allocation; correct S4/S5 state; exact oracle; usable
      public session and first command response.
- [ ] `BG-ACTIVATE-SAME`: first three same-key usable sessions versus `R0-C02`;
      no complete-tree or carrier rebuild.
- [ ] Retain candidate/control raw values, outer/CLI time, service time,
      mount/projection and readiness spans, median/max, and exact ratios.

| Gate / metric | Required acceptance | Preferred acceptance | Timing boundary / notes |
|---|---:|---:|---|
| `BG-ACTIVATE-EXACT` | each candidate `≤min(99.87675338 ms, matched control / 100)` | `≤min(19.975350676 ms, matched control / 500)` | exact activation to usable session; matched control must pass too |
| `BG-ACTIVATE-SAME` | each candidate `≤50 ms`; matched median `≥100×` | each `≤20 ms`; median `≥500×` | same-key activation to usable session |
| First command readiness | record reply delivery, byte count and response digest | lower is better; not a separate multiplier gate | must not require printing a full reply |
| Cold/warm classification | raw samples, median, max, cache state, and depth | n/a | do not call a failed reconstruction a hot measurement |

## 6. Phase P2 — fork

Acceptance list:

- [ ] Measure the public `HV-10` fork operation against a matched physical-copy
      control, retaining the public outer time and selected fork-to-ready time
      separately.
- [ ] Prove fork isolation, correct root/oracle, ownership/authorization, and
      cleanup with no active lease leak.
- [ ] Scale inactive forks at `1`, `64`, and `1,000`; each inactive fork owns
      zero payload bytes, upper, projection, or mount.

| Metric | Required acceptance | Preferred acceptance | Evidence |
|---|---:|---:|---|
| `BG-FORK` candidate time | each `≤10 ms` | each `≤2 ms` | raw candidate/control outer samples |
| Matched speedup | median `≥100×` | median `≥500×` | exact numerator/denominator; matched physical-copy control |
| Inactive-fork slope | metadata-only at `1/64/1,000` | same | payload/upper/projection/mount counters |
| Readiness/isolation | selected fork is usable and isolated | same | public response, oracle, epochs, cleanup |

## 7. Phase P3 — rollback

Acceptance list:

- [ ] Measure public hot rollback against a matched rebuild/reset control.
- [ ] Prove atomic paired-ref outcome, externally usable readiness, correct
      target root/oracle, fresh epoch, and no reconstruction or payload copy on
      an exact hit.
- [ ] Retain outer and service spans separately with candidate/control raw
      samples, median/max, and exact ratio.

| Metric | Required acceptance | Preferred acceptance | Evidence |
|---|---:|---:|---|
| `BG-ROLLBACK` outer operation | each `≤20 ms` | each `≤10 ms` | public operation boundary |
| Service time | each `≤1 ms` | retain and report | service receipt, not inferred from outer time |
| Matched speedup | median `≥100×` | median `≥500×` | matched rebuild/reset control |
| Correctness | correct root, oracle, epoch, and cleanup | same | paired-ref/readiness/zero-copy receipts |

## 8. Phase P4 — small publication

Acceptance list:

- [ ] Publish the identical ordinary approximately `1 MiB` delta across exactly
      ten files on S4-chain branches at `1 GiB`, `5 GiB`, and maximum depth
      within `≤9 GiB`.
- [ ] Run three independently allocated, alternating-order matched current-I2
      closing-control pairs at the 1-GiB point. All five candidate samples are
      retained (three 1-GiB, one 5-GiB, one maximum-depth).
- [ ] Include admission through durable-root commit and session close in the
      timer; fixture preparation stays outside it and is separately receipted.
- [ ] Prove depth-invariant work, zero accumulated immutable-payload reads, no
      second full-size allocation, durability, exact independent merged-tree
      oracle, resource bounds, and exact cleanup.

| Metric | Required acceptance | Preferred acceptance | Evidence |
|---|---:|---:|---|
| `BG-PUBLISH-SMALL` candidates | all five `≤100 ms` | all five `≤20 ms` | raw `CLOCK_MONOTONIC_RAW` ns, median and max |
| Matched speedup at 1 GiB | median `≥100×` | median `≥500×` | three exact matched pairs; uncapped ratio |
| Work independence | no growth with accumulated chain depth | same | immutable-read, scan/hash, bytes, and span receipts |
| Publication outcome | durable closed/ref state and bounded compact reply | same | response metadata, owner/ref/oracle receipts |

The sealed V15 publication calibration (`64.270791 ms` median, `178.867×`)
is useful prior evidence only. It becomes formal only if the final current
closure reproduces the gate.

## 9. Phase P5 — squash

Acceptance list:

- [ ] Measure the public logical squash, not a physical flatten or internal
      helper timing.
- [ ] Preserve canonical identity and attribution, public outcome, epochs,
      mount/FD cleanup, and final physical equation `X_unexplained=0`.
- [ ] Prove no payload scan, rebuild, or flatten and no active lease leak.

| Metric | Required acceptance | Preferred reporting | Evidence |
|---|---:|---:|---|
| `AG-SQUASH` outer operation | each `≤10 ms` | retain the `1–6 ms` band | public outer receipt |
| Service time | each `≤1 ms` | retain raw values | service receipt |
| Multiplier | not applicable | not applicable | this is an independent absolute gate |
| Semantic continuity | exact identity/attribution | same | oracle/epoch/cleanup receipts |

## 10. Phase P6 — real 1-GiB stream

Acceptance list:

- [ ] Use `HV-02`: one genuinely changed 1-GiB upper, represented by four
      dense 256-MiB deterministic files with four 64-MiB extents each.
- [ ] Keep checksum and semantic record-stream hash inside the measured timer;
      compute throughput from integer raw bytes and elapsed nanoseconds, never
      float extrapolation from a 64-MiB probe.
- [ ] Prove real stream/hash/flush, durable exact oracle, bounded `H+O(M)`
      memory, zero immutable reads, no second payload allocation, and cleanup.

| Metric | Required acceptance | Preferred acceptance | Timing boundary / evidence |
|---|---:|---:|---|
| `AG-STREAM` throughput | `≥1 GiB/s` | `≥5 GiB/s` | integer `1 GiB / elapsed_ns` |
| Stream timer | actual changed upper, checksum included | same | storage-stable callback + semantic build spans |
| Resources | within global cgroup and pool bounds | same | RSS, cgroup, I/O, FDs, bytes, inodes |
| Multiplier | not applicable | not applicable | physical-floor throughput gate |

## 11. Phase P7 — crash recovery

Acceptance list:

- [ ] Run a fresh 128-MiB `HV-07` sweep at every registered durable edge:
      fencing, sealing, strict unmount, stability inventory, owner
      selector/receipt, canonical install, locator, paired ref, response loss,
      and successor activation.
- [ ] Each point performs a real mount, fault marker, `SIGKILL`, restart,
      recovery, and same-ID replay. A response-loss retry must reuse the same
      scoped ID/request digest, never make a second operation.
- [ ] Prove only old-or-complete-new root outcomes, exactly one valid owner
      selector, no stale authority or partial locator, exact oracle, classified
      allocation bytes, mount/FD audit, `X_unexplained=0`, and no unreconciled
      debt.

| Metric | Required acceptance | Preferred reporting | Evidence |
|---|---:|---:|---|
| `HV-07` sweep wall time | complete within `60 s` | retain per-point wall times | all registered physical fault points |
| Recovery outcome | old or complete-new only | same | same-ID replay / paired-ref proof |
| Residue | no ambiguous allocation or stale authority | same | allocation, mount, FD, locator, owner receipts |
| Multiplier | not applicable | not applicable | required correctness qualifier |

## 12. Phase P8 — final qualification, seal, and decision

Acceptance list:

- [ ] Validate independently sealed P0–P7 roots; P8 does not re-run their
      workloads or impose a cumulative campaign timeout. Keep host
      build/rebuild duration separate from every phase receipt.
- [ ] Re-read qualification, all seven independent gate receipts, global
      correctness, security, resources, cleanup, CLI/poll accounting, and raw
      metrics without altering any phase result.
- [ ] Compute `manifest.sha256` last and verify it in a fresh read.
- [ ] Publish exact top-level decision strings, never a rounded or inferred
      ratio: `POC_CORRECTNESS_*`, `POC_100X_*`, `POC_500X_*`, `AG_SQUASH_*`,
      and `AG_STREAM_*`.

| Decision / metric | Acceptance condition |
|---|---|
| `POC_CORRECTNESS_PASS` | every ownership, semantic, durability, recovery, space, memory, security, reconciliation, and cleanup requirement passes |
| `POC_100X_SUPPORTED` | all five `BG-*` gates have valid matched controls, median `≥100×`, every sample meets its required absolute ceiling, and correctness passes |
| `POC_500X_SUPPORTED` | all five multiplier gates meet the preferred ceiling and median `≥500×` |
| `POC_500X_PARTIAL` | 100× is supported and one or more, but not all, multiplier gates meet the preferred target |
| `AG-SQUASH` / `AG-STREAM` | independently report `PASS`, `FAIL`, or `UNKNOWN`; do not force a meaningless multiplier |
| Any `UNKNOWN` multiplier gate | `POC_100X_NOT_SUPPORTED`; retain the reason and evidence root |

## 13. Phase-to-runner map

| Phase | Final runner case | Formal artifacts expected |
|---|---|---|
| P0 | `qualification` | qualification result, environment, security, baseline inventories |
| P1 | `activation` | `BG-ACTIVATE-EXACT` and `BG-ACTIVATE-SAME` receipts, activation progress, matched controls |
| P2 | `fork` | `BG-FORK` receipt, scale/isolation/control evidence |
| P3 | `rollback` | `BG-ROLLBACK` receipt, target-root/epoch/control evidence |
| P4 | `publication` | `BG-PUBLISH-SMALL` result, publication progress, candidate/control/oracle/durability receipts |
| P5 | `squash` | `AG-SQUASH` receipt, identity/attribution and cleanup evidence |
| P6 | `stream` | `AG-STREAM` result, raw byte/elapsed throughput and resource receipts |
| P7 | `recovery` | `HV-07` fault-point/replay result and residue audit |
| P8 | `sealing` | re-read scorecard, decision, report, cleanup, and manifest verification |

The focused P0–P8 runner split is complete. P8 consumed the exact sealed
receipts without rerunning P0–P7 and applied only its own fixed `30 s` cap.
No cumulative campaign timeout was used.
