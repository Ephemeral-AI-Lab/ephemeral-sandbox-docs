# MPLA Booster Scorecard Qualification — Next-Agent Execution Spec

Status: `IN_PROGRESS`

Overall formal verdict at handoff: `POC_100X_NOT_SUPPORTED`

Reason: a strong matched publication calibration exists, but the complete Booster
scorecard has not been executed under the exact `test_matrix.md` contracts. An
unmeasured gate is `UNKNOWN`; `UNKNOWN` cannot be treated as a pass.

This is an additive execution and progress-tracking document. It does not replace
the historical `progress_tracker.md`, rewrite sealed evidence, or relax any
requirement in `test_matrix.md`.

## 1. Mission

Execute the minimum focused qualification campaign needed to decide the formal
MPLA Booster scorecard:

- `BG-ACTIVATE-EXACT`
- `BG-ACTIVATE-SAME`
- `BG-FORK`
- `BG-ROLLBACK`
- `BG-PUBLISH-SMALL`
- absolute gates `AG-SQUASH` and `AG-STREAM`
- all correctness, durability, isolation, security, space, memory, ownership,
  reconciliation, and cleanup gates required by those cases

The terminal decision must be exact:

- `POC_100X_SUPPORTED` only when all five Booster gates pass at `>=100x`,
  every candidate sample meets its absolute ceiling, and all required correctness
  gates pass.
- `POC_100X_NOT_SUPPORTED` otherwise, including any `UNKNOWN`.
- Report `POC_500X_SUPPORTED`, `POC_500X_PARTIAL`, or
  `POC_500X_NOT_SUPPORTED` separately. Do not substitute the preferred `500x`
  target for the required `100x` decision.
- Report `AG_SQUASH_PASS|FAIL|UNKNOWN` and
  `AG_STREAM_PASS|FAIL|UNKNOWN` separately.

Do not stop merely because a blocker takes time. Continue resolving any
in-scope, technically resolvable blocker. Escalate only a genuine hard blocker
that requires new authority, an unavailable external dependency, or a material
user decision. The old one-hour blocker-resolution rule is superseded. Every
focused phase uses only its matrix-defined phase-local cap; there is no
aggregate campaign validity ceiling.

## 2. Governing sources and precedence

Read these before changing code or running a test:

1. Repository `AGENTS.md`
2. Repository `CLAUDE.md`
3. `docs/maintainer-architecture.md`
4. Codex skill `eos-sandbox-e2e-test-rules`
5. `poc/test_matrix.md`
6. `baseline-experiment/README.md`
7. This document

If this document conflicts with a higher-ranked source, follow the higher-ranked
source and record the discrepancy in the progress ledger.

Authoritative matrix:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/test_matrix.md`

Historical baseline context:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/baseline-experiment/README.md`

The historical baseline is context, not a denominator that may be substituted
for a missing matched control arm.

## 3. Handoff state verified before this spec

These observations have already been checked. Re-capture mutable environment
facts in the new run; do not assume they remain current.

### 3.1 Source state

Source repository:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`

Observed source identity:

- branch: `upgrade-2.0-phase-1`
- commit: `82255cd4f96a5478f856a3e9f46769a5412600b1`
- tree: `a517a27fa0e71a4eb2634c1bcc3f5348880d22dd`

The source and documentation repositories are dirty. Existing modifications and
untracked files belong to ongoing work. Do not reset, clean, discard, or
overwrite them. Capture commit, tree, status, and a diff hash before the next
run.

Important source changes present at handoff include:

- `config/mpla-poc-m3.yml`
- `config/materialization-lifecycle-benchmark.yml` (untracked)
- runtime namespace/operation changes
- `crates/sandbox-runtime/mpla-poc/src/bin/mpla-speed-poc-v1.rs` (untracked)
- `crates/sandbox-runtime/mpla-poc/tests/tree_usage.rs` (untracked)
- `crates/sandbox-runtime/mpla-poc/tests/heavy_scale.rs`
- `crates/sandbox-runtime/mpla-poc/tests/heavy_campaign.rs`

Inspect the current worktree rather than assuming this list is exhaustive.

### 3.2 Exact R0 fixture

The only valid R0 source path is:

`/Users/yifanxu/Ephemeral-AI-Lab/experiment/materialization-benchmark-20260727/corpus/console-release`

Verified profile:

- logical bytes: `912,350,100`
- files: `3,602`
- approximate size: `870.08 MiB`

Never use its parent as R0:

`/Users/yifanxu/Ephemeral-AI-Lab/experiment/materialization-benchmark-20260727`

That parent also contains a materialized carrier and is approximately `1.72 GiB`.
Using it changes the experiment and invalidates an R0 claim.

Pinned image:

`ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`

Platform:

- Linux/arm64
- Ubuntu 24.04

### 3.3 Sealed matched publication calibration

Sealed evidence:

`/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-speed-primary-20260728T223700Z`

Manifest verification succeeded for all ten listed files.

Manifest file SHA-256:

`0b6acfca18dbe11658bca7393ad83a8909530642454994b58ae9c859fef9e905`

Recorded decision:

- `CONCEPT_VERIFIED_500X`
- matched median speedup: `760.228406789519x`
- exact ratio: `51648176274 / 67937709`
- candidate samples, ns:
  `[62481833, 60469417, 67937709, 87828500, 68193000]`
- candidate median: `67,937,709 ns`
- candidate max: `87,828,500 ns`
- matched control samples, ns:
  `[47815802688, 51648176274, 48375731688, 63883792738, 53763431816]`
- control median: `51,648,176,274 ns`
- recorded correctness failures: none

The run also recorded:

- no tmpfs
- persistent `/eos/workspace` ext4 backing
- real OverlayFS mount and unmount
- effective, permitted, and bounding `CAP_SYS_ADMIN` bit 21
- command security profile `mpla_benchmark_qualification`
- pinned image digest
- zero final manager and observability object counts
- no second full-size copy
- exact oracle match
- zero immutable payload reads on the candidate path

Classification for this scorecard:

`PRIOR_MATCHED_CALIBRATION_ONLY`

Do not mark `BG-PUBLISH-SMALL` as formally passed from this result alone. The
formal HV-01 contract requires the S4 chain at depths `1`, `5`, and the maximum
chain within `<=9 GiB`, the same approximately `1 MiB / 10-file` delta, and
three matched pairs at the 1 GiB point. The sealed run remains valuable evidence,
but it is not a substitute for an exact HV-01 conformance run or a documented
proof that every HV-01 condition was met.

### 3.4 Prior 1.72 GiB lifecycle diagnostic

Evidence:

`/Users/yifanxu/Ephemeral-AI-Lab/experiment/materialization-lifecycle-benchmark-20260729/evidence/primary-1.72g-v1`

It passed its own 25/25 diagnostic cases, but it is not Booster scorecard
evidence because:

- it used the wrong 1.72 GiB fixture root;
- `configured_mode` was `legacy`;
- it had no matched baseline arm;
- session creation was measured in place of exact MPLA activation;
- the small publish shape was 4 KiB rather than approximately 1 MiB/10 files;
- the large stream case was 64 MiB rather than the required real 1 GiB stream.

Useful diagnostic observations only:

- closest session-create medians: approximately `80–89 ms`
- 4 KiB small-publish median: `152.655 ms`
- 64 MiB stream throughput: approximately `95.24 MiB/s`
  (`0.093 GiB/s`)

Metrics SHA-256:

`35a50b8f5765186637a28e27d75602093efce2fd529da5da5d6f012a7aa7f5db`

### 3.5 Known harness traps

At handoff, existing heavy harness files contain hard-coded old identities:

- interface: `m2r-iface-v1`
- run ID: `m2r-20260728T015724p0800`
- lease and branch prefixes derived from that run

Known locations include:

- `crates/sandbox-runtime/mpla-poc/tests/heavy_scale.rs`
- `crates/sandbox-runtime/mpla-poc/tests/cases/heavy_lead.rs`

Do not reuse an old run ID or write into sealed evidence. Make run ID, evidence
root, lease prefix, branch prefix, interface, config, fixture, and image explicit
inputs before qualification.

The prior quick-PoC catalog binding exposed publication and squash operations but
did not expose public activation, fork, and rollback operations:

- `publish_workspace_session: true`
- `squash_layerstacks: true`
- `activate_workspace_session: false`
- `fork_workspace_session: false`
- `rollback_workspace_session: false`

Before claiming those Booster gates, expose and test the actual supported public
lifecycle operations, or record a precise blocker explaining why the tested
surface cannot satisfy the matrix. Do not silently substitute internal helper
timings for public operation timings.

## 4. Non-negotiable environment contract

### 4.1 Storage and mount

- Do not use tmpfs or ramfs.
- Fixture and workspace backing must be persistent ext4 inside the Docker
  environment.
- Host evidence must be written to a persistent host path bound into Docker.
- Fail preflight if the measured fixture/workspace path is tmpfs, ramfs, or an
  unintended volatile overlay root.
- Exercise a real OverlayFS mount and unmount during preflight.

### 4.2 Capability and security

- `CAP_SYS_ADMIN` is required and must be enabled for the dedicated
  storage/projection lifecycle process and qualified benchmark coordinator.
- Verify effective, permitted, and bounding capability bit 21 from inside the
  measured process.
- Verify required mount syscalls are allowed.
- Absence of `CAP_SYS_ADMIN` is a preflight failure, not a reason to downgrade
  the experiment.
- The ordinary untrusted workload must still not receive broad
  `CAP_SYS_ADMIN`. Record the boundary between the lifecycle process and ordinary
  workload.
- Do not replace the supported gateway path with an ad hoc privileged Docker
  invocation.

### 4.3 Resource envelope

- Docker Desktop: fixed `4 vCPU / 4 GiB`.
- Do not raise the envelope to make a gate pass.
- Combined fixture/chain under test must remain `<10 GiB`.
- Before generation, calculate expected peak disk consumption plus 20% margin
  and fail early if unavailable.
- Reuse immutable prepared fixtures where allowed; do not make accidental
  full-size copies.
- F0-COLD cache construction owns
  `fixture-cache-construction.json`, created with the builder's
  `--evidence-file` option, a genuine first-time/recovery `<5.0 s` outer
  acceptance target, a `1–3 s` stretch range, and a `30 s` liveness cap.
- P0-WARM attachment owns `fixture-cache-attachment.json`, a `<50 ms`
  attachment-service target, a `<1.0 s` complete in-service preparation target,
  and a `5 s` liveness cap.
- All Booster and absolute operations use only their own matrix-defined
  phase-local budgets. There is no aggregate campaign target or hard limit.
- The focused P0–P8 runners use only their declared phase-local ceilings:
  qualification `60 s`, activation `120 s`, fork `60 s`, rollback `60 s`,
  publication `70 s`, squash `60 s`, stream `40 s`, recovery `120 s`, and
  sealing `30 s`. Publication fixture preparation is a separate `5 s`
  P0-WARM phase. No grouped lifecycle timer, elapsed time, or unused allowance
  carries between phases.

### 4.4 Supported control plane

For all manual sandbox operations use only:

- `sandbox-manager-cli`
- `sandbox-runtime-cli`
- `sandbox-observability-cli`

Rebuild/start the gateway exactly through:

```bash
export PATH="$PWD/bin:$PATH"
env SANDBOX_GATEWAY_CONFIG_YAML="$PWD/config/mpla-poc-m3.yml" \
  bin/start-sandbox-docker-gateway --rebuild-binary
```

Keep the gateway process alive in its own PTY/session and wait for readiness
before creating a sandbox.

Do not run direct Docker lifecycle commands as a replacement for the supported
CLIs. Read-only Docker diagnostics such as `docker info`, `docker context show`,
and narrowly scoped inspection are acceptable.

## 5. Required evidence layout

Create a new immutable run root:

`/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/booster-scorecard-<UTC>`

Never reuse or modify a prior run directory. The new root must contain at least:

```text
booster-scorecard-<UTC>/
├── environment.json
├── source.json
├── fixture-manifest.json
├── security-profile.json
├── command-ledger.jsonl
├── cases/
│   ├── BG-ACTIVATE-EXACT/
│   ├── BG-ACTIVATE-SAME/
│   ├── BG-FORK/
│   ├── BG-ROLLBACK/
│   ├── BG-PUBLISH-SMALL/
│   ├── AG-SQUASH/
│   └── AG-STREAM/
├── correctness.json
├── resources.json
├── cleanup.json
├── scorecard.json
├── decision.json
├── report.md
└── manifest.sha256
```

Each case must emit machine-readable records containing:

- run/case/sample identity
- source commit, tree, and dirty-state hash
- config and binary hashes
- image digest and platform
- fixture identity, logical bytes, file count, and manifest hash
- candidate/control allocation identities
- exact timing boundary and clock
- raw sample values
- median and max
- exact speedup numerator and denominator
- absolute ceiling and result
- bytes, inodes, memory, and immutable-read accounting
- security/capability evidence
- correctness/durability/isolation results
- cleanup result
- exact verdict and failure reasons

Compute `manifest.sha256` only after all other artifacts are finalized, then
verify it in a fresh read.

## 6. Preflight checklist

Complete all items before the first measured sample:

- [ ] Read governing sources listed in section 2.
- [ ] Capture `git rev-parse HEAD`, tree, branch, porcelain status, and a hash of
      the current diff/untracked-input manifest.
- [ ] Confirm existing worktree changes remain untouched.
- [ ] Check Docker daemon, context, resource allocation, relevant processes,
      gateway port `7881`, and supported CLI snapshots before rebuilding.
- [ ] Create a unique UTC run ID and a new evidence root.
- [ ] Confirm free disk exceeds estimated peak plus 20%.
- [ ] Verify the exact R0 path, `912,350,100` logical bytes, `3,602` files, and
      manifest hash. Reject the parent directory.
- [ ] Verify pinned image digest and linux/arm64 platform.
- [ ] Rebuild the gateway using
      `bin/start-sandbox-docker-gateway --rebuild-binary`.
- [ ] Verify gateway readiness through the supported CLI path.
- [ ] Verify persistent ext4 backing and explicitly reject tmpfs/ramfs.
- [ ] Verify real OverlayFS mount/unmount.
- [ ] Verify `CAP_SYS_ADMIN` bit 21 effective/permitted/bounding in the lifecycle
      process and record the ordinary-workload denial boundary.
- [ ] Confirm measured lifecycle operations are public supported operations.
- [ ] Confirm all hard-coded old run/lease/branch/evidence identities are removed
      or overridden by explicit inputs.
- [ ] Confirm candidate and control arms can be independently allocated and
      cleaned without broad Docker cleanup.
- [ ] Append a `TEST-REPORT` start entry immediately before every test command,
      as required by the E2E skill.

If preflight fails, repair and repeat only the failed preflight component. Do not
start the measured campaign with a known invalid environment.

## 7. Implementation work before qualification

### 7.1 Make the runner generic

The focused runner must accept explicit values for:

- run ID
- evidence root
- interface/catalog binding
- config path
- pinned image digest
- exact R0 fixture path
- lease/branch/sandbox prefixes
- case selection
- sample count
- command timeout

It must refuse:

- a pre-existing evidence root;
- the historical hard-coded run ID;
- an R0 path whose identity/profile does not match;
- missing `CAP_SYS_ADMIN`;
- tmpfs/ramfs backing;
- an unpinned image;
- a candidate arm without its required matched control;
- a timing record without exact boundaries and allocation identities.

### 7.2 Expose the required lifecycle surface

Verify or implement the supported public path for:

- exact activation
- same-key activation
- fork
- rollback
- small publish
- squash
- real changed-upper streaming

Keep public API timing distinct from internal service timing. Rollback and squash
require both outer-operation and service timing where specified.

### 7.3 Keep setup outside the measured interval

Fixture generation, image pulls, sandbox allocation, warm-up, and harness setup
must occur outside the measured operation interval but remain reported. Preserve
the matched arm order and ensure candidate/control allocations are independent.

## 8. Focused execution order

Run focused cases in this order so early failures are cheap and diagnostic:

1. Compile and list the focused runner without executing heavy cases.
2. Run capability, mount, fixture, API-surface, and cleanup smoke checks.
3. Run `BG-ACTIVATE-EXACT`.
4. Run `BG-ACTIVATE-SAME`.
5. Run `BG-FORK`.
6. Run `BG-ROLLBACK`.
7. Run `BG-PUBLISH-SMALL`.
8. Run `AG-SQUASH`.
9. Run `AG-STREAM`.
10. Run only the missing correctness/isolation/ownership/reconciliation cases
    needed for the top-level verdict.
11. Run the full focused Booster qualification once after all focused failures
    pass.
12. Seal evidence, verify hashes, and compute the final decision.

Do not rerun a passing heavy case unless its relevant source/config/fixture/input
hash changed or its evidence was invalidated. Record the reason for every rerun.

## 9. Gate contracts

Use raw samples and exact arithmetic. For three measured samples report raw
values, median, and max. Do not report p95 for `n=3`.

### 9.1 BG-ACTIVATE-EXACT

Source:

- HV-08 / R0-04 candidate
- R0-C01 matched control
- exact R0 fixture
- zero-build R0-03 precondition

Required:

`candidate <= min(99.87675338 ms, matched_control / 100)`

Preferred:

`candidate <= min(19.975350676 ms, matched_control / 500)`

Also prove:

- five cached exact-fixture repeats
- zero hydration/reconstruction
- zero immutable payload reads
- stable allocation
- correct S4/S5 state
- three matched control pairs

### 9.2 BG-ACTIVATE-SAME

Source:

- first three same-key R0-04 candidate sessions
- R0-C02 matched controls

Required:

- every candidate sample `<=50 ms`
- matched median speedup `>=100x`

Preferred:

- every candidate sample `<=20 ms`
- matched median speedup `>=500x`

### 9.3 BG-FORK

Source:

- HV-10 public fork operation
- matched physical-copy control

Required:

- every candidate sample `<=10 ms`
- matched median speedup `>=100x`

Preferred:

- every candidate sample `<=2 ms`
- matched median speedup `>=500x`

Include inactive-fork scale checks at `1`, `64`, and `1000`.

### 9.4 BG-ROLLBACK

Source:

- HV-10 public rollback operation
- matched rebuild/reset control

Required:

- every outer-operation sample `<=20 ms`
- service time `<=1 ms`
- matched median speedup `>=100x`

Preferred:

- every outer-operation sample `<=10 ms`
- matched median speedup `>=500x`

### 9.5 BG-PUBLISH-SMALL

Source:

- HV-01
- ordinary approximately `1 MiB / 10-file` delta
- S4 chain at depths `1`, `5`, and maximum depth within `<=9 GiB`
- three matched candidate/control pairs at the 1 GiB point

Required:

- every candidate sample `<=100 ms`
- matched median speedup `>=100x`

Preferred:

- every candidate sample `<=20 ms`
- matched median speedup `>=500x`

Prove constant-work behavior across chain depth, zero prior immutable payload
reads, durability, exact oracle equality, and no second full-size copy.

### 9.6 AG-SQUASH

Required:

- outer operation `<=10 ms`
- service time `<=1 ms`

Report independently from the five Booster ratio gates.

### 9.7 AG-STREAM

Use HV-02 with a real `1 GiB` changed upper stream.

Required:

- throughput `>=1 GiB/s`

Preferred:

- throughput `>=5 GiB/s`

Do not extrapolate from the 64 MiB legacy diagnostic.

## 10. Correctness and resource qualification

At minimum, the final result must prove:

- exact file/content/mode/ownership oracle equality
- immutable layer immutability
- publish durability across teardown/restart as required
- rollback correctness
- fork isolation
- branch/session ownership and authorization boundaries
- lease and reconciliation correctness
- collision and recovery behavior
- no stale mounts, namespaces, sessions, branches, leases, or observability rows
- no hidden second full-size copy
- fixture/chain `<10 GiB`
- memory and inode bounds from `test_matrix.md`
- lifecycle process has required capability while ordinary workload remains
  constrained
- final manager and observability counts return to their exact-run baseline

Reuse prior correctness evidence only when the relevant source, config, image,
fixture, interface, and test-contract hashes match. Otherwise rerun the focused
case. Record every reuse decision and its hash comparison.

## 11. Roundtrip and polling controls

The successful quick PoC made 454 CLI calls, approximately 446 of which were
`read_command_lines` polls. Each poll cost roughly `40–55 ms`. That pattern is a
major avoidable control-plane roundtrip trap.

For this campaign:

- Use one long-running in-sandbox coordinator invocation per focused case.
- Execute all samples for a case inside that invocation and write results to the
  persistent bound evidence root.
- Do not create a new gateway or sandbox for every sample.
- Preserve independent candidate/control allocations and matched ordering within
  the case.
- Poll at `1, 2, 4, 5, 5...` seconds or no more often than every 2 seconds after
  startup.
- Use a returned output offset/cursor; do not reread the full command log.
- Default maximum: 60 polls per heavy case. Exceed only with a recorded reason.
- Set command timeout at or above the case validity budget; do not mistake a
  client poll timeout for benchmark failure.
- Record CLI call count, poll count, bytes returned, and elapsed control-plane
  overhead in `command-ledger.jsonl`.
- Prefer a single final artifact read over hundreds of progress reads.

The agent itself should send concise progress updates while work is ongoing, but
must not inject frequent CLI polling into measured timings.

## 12. Cleanup rules

- Tag every created object with the unique run ID.
- Cleanup only exact-run objects.
- Never use broad Docker prune, broad kill, or repository cleanup.
- Capture pre-run and post-run manager/observability snapshots.
- A case is not passed until cleanup and zero-leak checks pass.
- Preserve failed-case evidence before cleanup.
- Preserve the final evidence root; cleanup runtime objects, not evidence.

## 13. Progress tracker

Update this section in place after every material attempt. Use UTC timestamps.
Link evidence rather than pasting large logs.

### 13.1 Terminal run header

| Field | Value |
|---|---|
| Owner | Codex `/root` |
| Current status | `TERMINAL_SEALED`; Final73 authenticated F0-COLD and the exact P0–P7 roots without rerunning a sealed predecessor. P4 remains the honest required-gate failure. |
| Run ID | `mpla-final73-p8-20260801t085647z` |
| Evidence root | `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final73-p8-20260801t085647z` |
| Source commit/tree | `99290631750430cf267b5c9329f2ac5d281def05 / ae1eac3747de54de749bd3290c7555f4988be8aa`; sealed tracked-diff SHA-256 `390906e0a19da1389c2695b8ac1a15e16e88405c803ee56735177b1844190c85`; porcelain SHA-256 `08b26860499fe3533e0e281c6229c292e1a891d90bfa7663c7da3fc5bdf659ef` |
| Documentation state | Terminal reconciliation completed after the physical seal; historical attempts below remain preserved as evidence rather than active instructions. |
| Config | `config/mpla-poc-m3-phase-profile-v13.yml`; fixed macOS-hosted Docker Desktop `4 vCPU / 4 GiB`, Ubuntu 24.04 Linux/arm64 pinned container image |
| Sealed P7/P8 artifact hashes | Coordinator `929432bfea64e91c8f2c52834b47018755c5c0b6e87d1490f1dd0f8aa2a7e99b`; oracle `42b5e24cfff981058d0908f45abf0a98e71e7cae95342b1394eefa4feb96972a`; HV-07 harness `f9f5726c01a69d73811506754447313ee49adf4d42645ba949bc513130109cf7` |
| Final manifest hash | `837578247484c38c95285b12c0e7710b66546e643c3132f3368aa3c87891638f`; all 14 entries independently rehashed |
| Final update UTC | `2026-08-01T08:56:47Z` |
| Hard blocker | `none` |

### 13.2 Work phases

| ID | Phase | State | Evidence / next action |
|---|---|---|---|
| P0 | Qualification and warm fixture attachment | `PASS` | Final34 phase `2.120485208 s` under `60 s`; warm service `24.825208 ms`, complete preparation `374.467417 ms`, zero copied payload bytes |
| P1 | Exact and same-key activation | `PASS` | Final34b `85.129972292 s` under fixed `120 s`; both activation gates true |
| P2 | Fork | `PASS` | Final34 `52.723843000 s` under `60 s`; `BG-FORK=true` |
| P3 | Rollback | `PASS` | Final40 `51.757623833 s` under `60 s`; `BG-ROLLBACK=true` |
| P4 | Small publication | `FAIL_SEALED` | Final50 `22.881794000 s` under `70 s`; all candidates below `100 ms`, but matched ratio `0.626872660x`, so `BG-PUBLISH-SMALL=false` |
| P5 | Squash | `PASS` | Final54 `29.591311167 s` under `60 s`; `AG-SQUASH=true` |
| P6 | Real changed-1-GiB stream | `PASS` | Final61 `8.363238417 s` under `40 s`; `994.910 ms` at `1.079 GB/s`, `AG-STREAM=true` |
| P7 | Crash/recovery sweep | `PASS` | Final70 `21.349401583 s` under `120 s`; `46/46`, zero payload copies, no OOM, exact cleanup |
| P8 | Final validation and decision | `PASS` | Final73 `396,731,209 ns` under fixed `30 s`; exact inputs and 14 manifest entries authenticated |

Allowed phase states:

`NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL_REPAIRING`, `FAIL_SEALED`,
`HARD_BLOCKED`, `INVALIDATED`

### 13.3 Scorecard

| Gate | Formal state | Absolute result | Matched ratio | Correctness | Notes |
|---|---|---:|---:|---|---|
| BG-ACTIVATE-EXACT | `PASS` | Final34b phase `85.129972292 s` | Passed formal ratio | `PASS` | Exact activation gate authenticated by Final73 |
| BG-ACTIVATE-SAME | `PASS` | Final34b phase `85.129972292 s` | Passed formal ratio | `PASS` | Same-key activation gate authenticated by Final73 |
| BG-FORK | `PASS` | Final34 phase `52.723843000 s` | Passed formal ratio | `PASS` | Focused public fork evidence |
| BG-ROLLBACK | `PASS` | Final40 phase `51.757623833 s` | Passed formal ratio | `PASS` | Focused public rollback evidence |
| BG-PUBLISH-SMALL | `FAIL_SEALED` | candidates `58.136209`, `57.915167`, `62.567625`, `63.389209`, `65.937250 ms` | `0.626872660x` | `PASS` | Absolute `100 ms` ceiling and all correctness predicates passed; required `100x` matched ratio did not |
| AG-SQUASH | `PASS` | Final54 phase `29.591311167 s` | n/a | `PASS` | Absolute squash gate passed |
| AG-STREAM | `PASS` | changed 1 GiB in `994.910 ms` (`1.079 GB/s`) | n/a | `PASS` | Real required workload passed |

Current aggregate:

- `POC_CORRECTNESS=PASS`
- `POC_100X=NOT_SUPPORTED`
- `POC_500X=NOT_SUPPORTED`
- `AG_SQUASH=PASS`
- `AG_STREAM=PASS`

These are the terminal evidence-backed decisions. `NOT_SUPPORTED` is not a
claim that a future implementation can never meet the multiplier targets.

### 13.4 Attempt ledger

Add one row per material attempt. Do not erase failed attempts.

| UTC | Phase/case | Change or command | Result | Evidence | Next action |
|---|---|---|---|---|---|
| `2026-07-29T00:32:01Z` | `P0` | Completed ordered authority read; verified sealed calibration manifest; captured both worktrees, exact Docker 4-vCPU/~4-GiB Linux/arm64 platform, config, processes, ports, disk, and historical residue without mutation | `PASS` | Calibration `manifest.sha256` SHA-256 `0b6acfca18dbe11658bca7393ad83a8909530642454994b58ae9c859fef9e905`; run header above | Finish public-surface and harness audits, then parameterize the focused runner |
| `2026-07-29T00:33:00Z`–`2026-07-29T04:32:07Z` | `P1/P2` | Repaired the public MPLA lifecycle, external stationary-publication ownership/recovery boundary, storage-helper choreography, stable allocation cleanup, cgroup enrollment/release, and focused destroy safety; rebuilt only through `bin/start-sandbox-docker-gateway --rebuild-binary`; ran focused regressions after each repair | `PASS` for focused correctness; formal performance still pending | Append-only authoritative attempt details and exact commands are in `crates/e2e-test/test-reports/TEST-REPORT.md`; latest focused suites passed `external_publication` 7/7 and ratified-Sealing destroy guard 1/1 | Re-measure only the invalidated public gate and retain the repairs if correctness remains green |
| `2026-07-29T04:43:21Z` | `BG-PUBLISH-SMALL` diagnostic | Fresh pinned-image/exact-R0 4-CPU/4-GiB public lifecycle with ten files totaling exactly 1,048,576 bytes; exact-ID cleanup and empty manager/observability proof | `PASS_DIAGNOSTIC`; public service `89,721,458 ns`, below the 100-ms absolute ceiling | `TEST-REPORT.md` entry “natural-helper-exit exact small-publish diagnostic”; launch daemon SHA-256 `7f07ac1e68e0be47b999c45dbd515a3c7cf97f476e14e0f6cd79b0cb0f0154a4`, helper `029c473f1a8a5c52bb7d106ca205233b40d19b351d1d9292e1bb64ed951ff530` | Do not promote one sample to a gate result; run three exact HV-01 pairs at depths 1/5/max with independent controls |
| `2026-07-29T04:54:51Z` | `P1` | Plain `cargo build` of the three Linux/arm64 supported CLIs reached link and failed because macOS `cc` rejected GNU ELF `--as-needed` | `FAIL_REPAIRING` | `TEST-REPORT.md` “Linux arm64 qualification CLI build” | Use the repository-supported zigbuild linker without changing target/features |
| `2026-07-29T04:55:56Z` | `P1` | Cross-built manager/runtime/observability CLIs with `cargo zigbuild --target aarch64-unknown-linux-musl` and exact feature sets | `PASS` | CLI hashes in run header and `TEST-REPORT.md` | Stage only these hashed artifacts in the qualification coordinator |
| `2026-07-29T04:56:47Z`–`2026-07-29T04:59:55Z` | `P1/P2` | Iterated the in-sandbox coordinator connectivity smoke: replaced unsafe temporary cleanup with recoverable Trash move, retained response details, corrected the pre-session shared-base path, then invoked the Linux manager CLI from the pinned sandbox against `host.docker.internal:7881` | `PASS` | `TEST-REPORT.md` entries “in-sandbox supported-CLI gateway connectivity smoke” through “shared-base in-sandbox gateway connectivity”; exact-ID cleanup returned both inventories empty | Use `/eos/layer-stack/base/B000001-base/tools`, one long-running invocation, sparse cursor polling, and supported CLIs for the formal cases |
| `2026-07-29T05:06:24Z` | `P1` | Bound matrix controls to existing audited `run_current_i2_closing` and `run_current_i2_materialization` implementations; confirmed R0-C01/C02 cold/same-key cache validation and HV-10 fork/rollback intent coverage | `PASS_REVIEW`; no physical measurement | Source review of `crates/sandbox-runtime/mpla-poc/src/controls.rs`, `tests/cases/heavy_lead.rs`, and normative matrix sections | Repair formal coordinator orchestration; do not duplicate or approximate matched-control semantics |
| `2026-07-29T14:01:39Z` | `P1/P2/HV-07` | Repaired frozen qualified-command selection to admit only `mpla-speed-poc-v1 scorecard-case --case recovery` in addition to existing fixed cases; added measured coordinator/child CAP_SYS_ADMIN E/P/B receipts; rebuilt the supported gateway and ARM64 campaign artifact | `PASS` focused regression; fresh physical rerun pending | `TEST-REPORT.md` “qualified recovery coordinator regression”; gateway listener restarted on `127.0.0.1:7881` | Run one fresh recovery-only HV-07 campaign, retain the failed predecessor, and optimize only if its 60-second budget misses |
| `2026-07-29T14:12:00Z` | `HV-07` | Fresh qualified recovery campaign completed all 46 physical points with real mount, SIGKILL, recovery, replay, E/P/B capability receipts, and a verified sealed manifest; only the aggregate hard-stop failed at `61,269,082,737 ns` | `FAIL_REPAIRING` (budget only) | `evidence/mpla-booster-20260729T140139Z`; `TEST-REPORT.md` “qualified-coordinator HV-07 recovery campaign” | Reuse one canonical semantic receipt only for the identical immutable 128 MiB fixture inside the measured loop; retain independent allocations and all physical recovery work, then run a fresh sweep |
| `2026-07-29T14:12:00Z` | `HV-07` | Implemented explicit in-window semantic-receipt reuse for the fixed HV-07 fixture; host regressions and exact ARM64 campaign cross-build passed | `PASS` build/regression; physical rerun pending | `TEST-REPORT.md` “HV-07 shared semantic-receipt regression” and “ARM64 HV-07 campaign artifact build” | Stage and execute one new full recovery-only campaign; judge only its sealed receipt |
| `2026-07-29T14:12:42Z` | `HV-07` | Fresh qualified recovery-only campaign completed all 46 registered physical points using the exact 128 MiB fixture; each retained a distinct allocation/operation ID and real mount, SIGKILL, same-ID recovery/replay, and E/P/B capability proof. One canonical semantic build plus 45 explicitly recorded identical-input reuses stayed inside the measurement. | `PASS` — `43,691,821,353 ns` against the `60,000,000,000 ns` hard stop | Sealed and verified `evidence/mpla-booster-20260729T141100Z/manifest.sha256`; `fresh_sweep.passed=true`, physical points `46/46` | Preserve this receipt; advance to the remaining formal gates and complete whole-campaign correctness/security/resource evidence |
| `2026-07-29T14:18:00Z`–`2026-07-29T14:45:00Z` | `P1/P4/P5/P6` | Bound BG-FORK to public-operation timing, made publication candidate/control fixture comparability receipt-backed, and replaced AG-STREAM floating-point qualification with exact raw-byte/elapsed-nanosecond arithmetic. | `PASS` host regression | Append-only entries in `crates/e2e-test/test-reports/TEST-REPORT.md`: lifecycle public-fork binding, publication fixture-comparability retry, full-fixture receipt, and AG-STREAM exact-throughput arithmetic | Implement and run focused receipts for the remaining campaign correctness, security, and resource decisions before broad physical gates |
| `2026-07-29T16:54:40Z`–`2026-07-29T17:07:20Z` | `P2/P7` | Investigated the sealed partial campaign `evidence/mpla-booster-20260729T165343Z`. The candidate base build ran in old gateway PID `28028` while `bin/start-sandbox-docker-gateway --rebuild-binary` was still completing; the script then stopped that PID before launching replacement PID `44907`, which closed the in-flight authenticated connection. Supported manager/observability snapshots against PID `44907` are empty; the 863 MiB `.building-28028-6` orphan was moved recoverably to Trash. | `PASS` diagnosis/preflight; prior campaign remains `FAIL` and is not promoted | Prior partial evidence plus current PID/socket/readiness and inventory checks | Run exactly one fresh full campaign on already-ready PID `44907`; prohibit gateway rebuild/restart until it seals |
| `2026-07-29T17:07:20Z`–`2026-07-29T17:17:27Z` | `P4/P7` | Fresh full campaign on already-ready PID `44907` passed qualification and four lifecycle gates, recorded a real rollback miss, then sealed `BG-PUBLISH-SMALL` partial evidence after its coordinator reached the hard `600.044286689 s` ceiling. Source review established that the runner built the 1/5/8 GiB `S4-chain` inside the timed publication coordinator, contrary to the matrix's prepared-fixture boundary. | `FAIL_REPAIRING` (publication harness boundary; rollback performance) | `evidence/mpla-booster-20260729T170720Z/manifest.sha256`, publication error/terminal receipts, cleanup evidence, and `TEST-REPORT.md` | Add receipted same-sandbox `S4-chain` setup outside the measured publication interval plus durable stage progress; rerun publication only, then repair/remeasure rollback and finish stream/aggregate evidence |
| `2026-07-29T17:37:42Z` | `BG-PUBLISH-SMALL` preflight | ARM64 coordinator/HV-07 artifact cross-build and required gateway rebuild completed, but the first host inventory commands used their default socket rather than the qualified `127.0.0.1:7881` endpoint. No physical case began. | `FAIL_REPAIRING` (preflight invocation only) | `TEST-REPORT.md` “qualified prepared-S4 publication rerun preflight command”; replacement gateway PID `67860` listened on `127.0.0.1:7881` | Load the gateway token and set the endpoint explicitly; supported inventories have subsequently returned empty. |
| `2026-07-29T17:41:00Z` | `BG-PUBLISH-SMALL` preflight | The alternate token-loading command sourced a helper that treats this zsh context as direct invocation and exited with usage. No physical scorecard action began and no sandbox state changed. | `FAIL_REPAIRING` (preflight invocation only) | `TEST-REPORT.md` “corrected qualified prepared-S4 publication rerun token-loading preflight” | Use only the helper's documented `read` subcommand, keeping the private value out of records. |
| `2026-07-29T17:42:00Z` | `BG-PUBLISH-SMALL` | Fresh run `mpla-booster-20260729T173742Z` reached the coordinator immediately but clap rejected `prepare-publication-fixture` because it incorrectly inherited a required `--case` field. The runner sealed partial evidence and cleaned all resources. | `FAIL_REPAIRING` (CLI schema only) | `evidence/mpla-booster-20260729T173742Z`; `TEST-REPORT.md` “qualified prepared-S4 publication rerun CLI-schema defect” | Give fixture preparation its own fixed no-case grammar, direct-test it, cross-build, then run a new focused root. |
| `2026-07-29T17:41:57Z` | `BG-PUBLISH-SMALL` | The fresh corrected-grammar run `mpla-booster-20260729T174157Z` passed parser/security/harness regressions and empty supported-CLI preflight, then built the S4 chain through 3 GiB/depth 3 before its separate preparation coordinator timed out at `600.030843983 s`. The measured small-delta publication never began; cleanup and independent manifest verification passed. | `FAIL_REPAIRING` (preparation observability/budget) | `evidence/mpla-booster-20260729T174157Z/manifest.sha256`; durable progress receipt, terminal timeout receipt, and empty final inventories | Add durable per-operation preparation timing receipts; run one fresh focused diagnostic preparation to locate the exact blocking operation before altering fixture topology or any timeout. |
| `2026-07-29T17:59:22Z` | `BG-PUBLISH-SMALL` preparation diagnostic | Fresh run `mpla-booster-20260729T175922Z` passed runner regressions `13/13`, exact ARM64/musl campaign cross-build, and supported-CLI preflight. It proved layers 1/2 fully published and layer 3 activation plus the 1-GiB write/hash completed. The third `publish_mpla_workspace_session` began at `127,273,814,017 ns` and remained unresolved until the preparation coordinator hard-capped at `600.0373409 s`; the measured small-delta publication did not start. Cleanup, empty post-run supported inventories, and independent manifest verification passed. | `FAIL_REPAIRING` (third incremental public publication) | `evidence/mpla-booster-20260729T175922Z/manifest.sha256`; `fixture-preparation-progress.json`, terminal timeout, cleanup and inventory receipts | Trace publication internals with one focused diagnostic; do not alter timeout or fixture topology until the blocking subphase is evidenced. |
| `2026-07-29T18:24:34Z` | `BG-PUBLISH-SMALL` phase-trace preparation | Added candidate-side `mpla_publication.checkpoint` events spanning operation lock, parent/affected-path discovery, sealing, storage inventory, parallel adoption/semantic/destroy work, ref commit, and outcome persistence. The harness now extracts the latest started publish request ID from durable coordinator progress and preserves both its candidate trace and raw checkpoints when preparation fails. | `PASS` local validation; physical attempt pending | `cargo fmt --check`, `cargo check -p sandbox-runtime`, runner tests `14/14`; append-only `TEST-REPORT.md` entry “corrected candidate publication phase-trace instrumentation validation” | Rebuild through the required gateway command, preflight the reserved root with supported CLIs, and execute one unchanged publication-only diagnostic. |
| `2026-07-29T18:53:44Z` | `BG-PUBLISH-SMALL` response-boundary preparation | Candidate trace review proved `daemon.dispatch` completed at `62.332 s`, excluding service teardown and response-value construction. Added post-dispatch daemon encode/write/shutdown checkpoints (including frame byte count) and scoped observer emission to nonblocking best-effort telemetry; direct concurrent sink appends retain their durable lock behavior. | `PASS` local validation; physical attempt pending | `cargo fmt --check`; daemon/runtime check; observer `12/12`; sink `14/14`; append-only `TEST-REPORT.md` entry “scoped best-effort observer emission validation” | Rebuild through the required gateway command, preflight the reserved fresh root, then execute one unchanged publication-only diagnostic. |
| `2026-07-29T19:54:39Z` | `P3` staged durability verification | Reserved fresh root `mpla-booster-20260730T035800Z` for one serialized publication-only diagnostic after semantic focused tests `7/7` and the required isolated gateway rebuild. The target is the actual third 1-GiB publication duration; telemetry records only timing, response byte count, hash, and status—not response payload contents. | `IN_PROGRESS` | `TEST-REPORT.md` staged semantic regression and isolated-rebuild entries; daemon SHA-256 `09da4ddc32043c910fb09f800629e10ce091d892017d96ad64ca3f4fb67e231e` | Historical instruction at the time: preflight with supported CLIs, then run this one focused diagnostic under the then-configured 600-second validity cap. That cap is retired and superseded by the current phase-local budget policy. |
| `2026-07-30T03:58:00Z` | `P3` staged durability diagnostic | Fresh run `mpla-booster-20260730T035800Z` sealed and independently verified every artifact (manifest SHA-256 `96b770d84a9248899fd2b666d106fcbab5df2634e36d1b689340d251f141a462`). All seven heavyweight publications returned compact 20,762–28,201-byte replies. The stage repair removed the historical missing-reply symptom, but did not meet the one-second engineering target: depth 2–8 1-GiB publications were 30.05–47.50 seconds, including 10.3–10.7 seconds of duplicate full-content stability inventory and 16.3–33.2 seconds of V1 32-KiB incremental trie mutation. | `FAIL_REPAIRING` (performance only; no response loss) | Sealed diagnostic evidence, compact timing/size/hash/status records, and independent manifest verification | Introduce an explicitly metadata-only stationary pair after strict unmount/empty-cgroup proof, preserve canonical content identity through the semantic scan, then replace V1 per-mutation trie rewrites with a bounded bulk-update representation before rerunning the focused diagnostic. |
| `2026-07-30T07:04:00Z` | `BG-PUBLISH-SMALL` | Fresh run `mpla-booster-20260730T065800Z` passed fixture, oracle, durability, and zero-immutable-read receipts. Its three matched samples were 123.921 ms, 235.780 ms, and 99.364 ms against an 11.579 s control; the median was 93.44x, below the 100x gate. Phase receipts isolated a 107.460 ms tail difference in `incremental-staged-commit` for otherwise identical 72-object / 56,028-byte work. | `FAIL_REPAIRING` (timing only) | Sealed `evidence/mpla-booster-20260730T065800Z` and append-only test report | Identify the commit-tail barrier before any further broad scorecard work. |
| `2026-07-30T07:13:00Z` | `P3/BG-PUBLISH-SMALL` focused repair | Made the private reachable-object sort spool explicitly ephemeral: it retains bounded sorting and flush/close semantics but omits only its three scratch `sync_all` calls. The change is limited to `commit_incremental_roots`; canonical object `syncfs`, directory syncs, and root-manifest durability remain unchanged. The exact one-MiB/ten-file semantic-equivalence test passed. | `PASS` focused regression; fresh physical timing pending | `TEST-REPORT.md` “verified ephemeral reachable-spool durability isolation” | Rebuild through the required gateway command and run one fresh isolated publication case with a new evidence root. |
| `2026-07-30T08:44:00Z` | `P3/BG-PUBLISH-SMALL` bounded-pack measurement | Fresh sealed run `mpla-booster-20260730T083700Z` passed exact oracle, fixture comparability, durability, zero immutable-payload reads, no-copy, resource, cleanup, and manifest verification. The matched small-publish median improved to 84.436125 ms against 11,874.089630 ms control (140.62x), but depth-1/depth-8 tails were 126.652333/136.867041 ms and the dense 8-GiB preparation still took 341.439262114 s. Depth-8 semantic work was 13.048198589 s validate/apply plus 10.583713630 s committing 72,404 staged objects / 25,720,484 B as loose files. | `FAIL_REPAIRING` (metadata staging/commit architecture; not RPC or output loss) | Sealed evidence `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/booster-scorecard-20260730T083700Z`, manifest SHA-256 `a0399c12d74ff3454c51d131a341946aad1286deb285347b09b4ebe5e58f54a3`, and append-only `TEST-REPORT.md` | Replace per-object staging and large loose-object fallback with bounded disk-backed staged and permanent segments; retain real dense input and durability, qualify focused semantic tests, then measure one fresh preparation diagnostic. |
| `2026-07-30T11:02:00Z` | `P3` persistent dense fixture warm | Identified the separate setup bottleneck as `dd` zero streaming plus rehashing for each 1-GiB layer, rather than publication or reply transfer. Replaced it with real allocated unwritten zero extents, preserved a complete SHA-256 read and explicit `stat` allocation receipt, moved verification buffers off the stack, passed focused regressions 4/4, and built the exact Linux/ARM64 artifact. The outer watchdog is 800 seconds by explicit authorization, while acceptance remains under 30 seconds. | `IN_PROGRESS` | `TEST-REPORT.md` entries “allocated-extents dense-fixture feasibility probe”, “heap-buffer dense allocated-extent fixture writer tests”, and “Linux ARM64 dense-fixture cache-builder artifact” | Rebuild the dedicated writable builder gateway, then execute exactly one serialized cache warm and retain only a sealed receipt with real allocation facts and elapsed time. |
| `2026-07-30T11:04:00Z` | `P3` fresh persistent fixture cache | The first optimized-warm invocation safely refused to overwrite the already sealed v1 volume in 5.85 seconds. Retained v1 unchanged and switched only the named Docker volume to fresh `eos-mpla-prepared-s4-chain-v2`; guest mount target, fixed `s4-chain-v1` profile, fixture path, artifact, workload, and timing semantics are unchanged. | `IN_PROGRESS` | `TEST-REPORT.md` “persistent allocated-extent S4 fixture warm” | Rebuild the dedicated builder gateway with the v2 writable mount and perform exactly one optimized warm; on seal, use v2 read-only in the normal profile. |
| `2026-07-30T05:01:00Z` | `P3` cross-run semantic lineage | The old split-prior/output proposal was rejected before execution because it would create mixed semantic leaves. `CanonicalDurabilityReceipt` now carries immutable semantic attribution; full builds seed it and incremental lifecycle use reuses it. The new semantic regression and exact capability grammar passed. The v1 cache remains sealed and will not be decoded under the new receipt schema; a distinct closed `s4-chain-v2` cache will be built. | `PASS` focused repair | `TEST-REPORT.md` “cross-run prepared-fixture semantic-lineage regression” | Exercise 1 MiB/ref/parser regressions, rebuild, and run one serialized v2 cache warm before the next physical publication. |
| `2026-07-30T05:15:33Z` | `P3/BG-PUBLISH-SMALL` | Allocated fresh run `mpla-booster-20260730T051533Z` and persistent evidence root, confirmed it is absent, rebuilt/started the normal gateway on the v2 read-only fixture configuration, and recorded the exact runner contract. | `IN_PROGRESS` | Header identifiers and `TEST-REPORT.md` pending entry “v2 cache consumption and sub-50-ms publication measurement” | Execute one serialized publication-only case; use its preparation receipt as the cache-consumption proof and optimize only a measured remaining durable publication phase. |
| `2026-07-30T05:15:40Z` | `P3/BG-PUBLISH-SMALL` | Publication-only run sealed partial evidence after the preparation executable returned `127` from the empty fixture volume in 25.912 ms. It did not prepare the fixture or begin a timed publication. Source review proved the cache warmer had used the final fixture root for bootstrap instead of its normal staged workspace root. | `FAIL_REPAIRING` (cache-warmer path only) | `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/booster-scorecard-20260730T051533Z`; terminal receipt and manifest verification | Regression-test the separated paths, rebuild/start the writable builder configuration, and warm exactly once before another read-only scorecard attempt. |
| `2026-07-30T05:16:00Z` | `P3` cache-warmer path repair | The separated bootstrap/final-root regression passed 3/3 in 0.017 s. The next physical command is the required rebuild of the isolated writable builder gateway; no normal scorecard will run while that profile has write access. | `IN_PROGRESS` | `TEST-REPORT.md` “cache-warmer bootstrap-root regression” | Start the writable builder profile and perform one serialized cache warm with a bounded receipt. |
| `2026-07-30T05:16:25Z` | `P3` builder gateway handoff | The required builder-profile rebuild did not begin a cache warm because a distinct PID file left the normal scorecard gateway owning `127.0.0.1:7881`; the builder exited during startup, normal gateway stayed healthy, and no fixture changed. | `FAIL_REPAIRING` (launcher handoff only) | `TEST-REPORT.md` “builder gateway handoff preflight” | Relaunch through the same dedicated scorecard PID file, which causes supported exact replacement of the normal profile. |
| `2026-07-30T05:20:36Z` | `P3` builder-profile handoff | Required supported rebuild and handoff passed: builder PID `41859` is the sole dedicated scorecard gateway on `127.0.0.1:7881`, using the writable v2 configuration. | `IN_PROGRESS` | `TEST-REPORT.md` “corrected v2 writable builder gateway handoff” | Execute one serialized v2 cache warm with an 800-second outer watchdog and preserve its bounded result. |
| `2026-07-30T05:29:31Z` | `P3` persistent shared-base repair | A supported-CLI mount probe proved that the builder can execute the staged tool only at `/eos/mpla-fixtures/s4-chain-v2/layer-stack/base/...`; the final normal consumer cannot see it because Docker had mounted that base as a nested, ephemeral named volume. Added a fail-closed builder-only materialization mode: the provider archives the immutable base into the writable persistent volume and omits the nested shared-base bind. Provider and configuration regressions passed; formatting and diff checks pass. | `PASS` local repair; live warm pending | `TEST-REPORT.md` materialized-builder archive/mount-shape/configuration entries | Rebuild the dedicated writable builder profile and perform exactly one serialized v2 cache warm; do not invoke the normal read-only scorecard until a sealed cache receipt exists. |
| `2026-07-30T05:36:27Z` | `P3` materialized v2 cache verification | The cache warmer safely found an already sealed v2 volume rather than overwriting it. A supported builder-profile sandbox then proved the sealed manifest and executable staged tool survive at the persistent base path after builder lifecycle cleanup. Replaced global freshness scanning in the cache warmer and normal scorecard with Cargo-metadata-derived local dependency closures; focused cache tests 4/4 and scorecard tests 19/19 passed. | `PASS` | `TEST-REPORT.md` entries “sealed v2 fixture topology probe” and dependency-scoped freshness suites | Handoff to normal read-only profile and run one fresh publication-only scorecard at the reserved evidence root. |
| `2026-07-30T05:46:10Z` | `P3/BG-PUBLISH-SMALL` sealed-fixture reader repair | Run `mpla-booster-20260730T053627Z` sealed partial evidence in 43.308167 ms before timing publication: `refs/LOCK` was opened with write access under the intended read-only fixture mount. A test first reproduced the failure; then shared locks were changed to read-only opens while exclusive locks remain writable. The new regression and full paired-ref/locator target passed 8/8; Linux/ARM64 coordinator SHA-256 is `b26f0d12b83858599c1340526b9521adfbdfbb690508b8fff8ba7f1f73275de4`. | `PASS` focused repair; fresh live evidence pending | Partial evidence `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/booster-scorecard-20260730T053627Z`; append-only `TEST-REPORT.md` | Rebuild the normal read-only gateway, perform one fresh publication-only case at `mpla-booster-20260730T054610Z`, and optimize only from a complete measured receipt. |
| `2026-07-30T05:47:00Z` | `P3/BG-PUBLISH-SMALL` normal gateway deployment | The required normal-profile launcher rebuilt and replaced the scorecard gateway; PID `52614` now owns `127.0.0.1:7881`. The supported manager CLI returned `{"sandboxes":[]}`. This is a deployment/preflight only, not a benchmark sample. | `PASS` deployment preflight | Append-only `TEST-REPORT.md` “normal read-only gateway shared-lock rebuild” and “normal gateway inventory preflight after shared-lock rebuild” | Execute exactly one serialized `publication` case at the header's fresh evidence root; preserve partial or complete receipt and optimize only measured publication work. |
| `2026-07-30T05:47:10Z` | `P3/BG-PUBLISH-SMALL` canonical-source lookup | Fresh run `mpla-booster-20260730T054610Z` attached the sealed read-only fixture and completed fixture preparation in `526,524,042 ns`, proving the shared-lock repair. Before a timed sample, incremental semantic validation tried to read prior root `3b4cbd5a...` only from the new run-local `canonical-objects` directory and failed `ENOENT`; the prior manifest points to the sealed fixture source. | `FAIL_REPAIRING` (cross-run immutable canonical-source lookup; no latency sample) | Partial evidence `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/booster-scorecard-20260730T054610Z`; coordinator terminal/error and preparation receipts | Add a read-only, digest-verified prior-object source chain for incremental validation and mutation, prove it with separate fixture/output directories, rebuild the normal gateway, then execute one fresh serialized publication-only case. |
| `2026-07-30T06:07:05Z` | `P3/BG-PUBLISH-SMALL` artifact freshness preflight | The runner sealed partial root `mpla-booster-20260730T060500Z` in 1.684 seconds and correctly refused to create a sandbox or start the case: its dependency-scoped freshness guard found the sealed fixture's Linux/arm64 coordinator and oracle older than the new semantic source-chain implementation. | `FAIL_REPAIRING` (artifact freshness only; no measured publication) | `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/booster-scorecard-20260730T060500Z`; runner terminal receipt | Cross-build only `mpla-speed-poc-v1` and `mpla-poc-oracle`, record hashes, reserve a new root, and retry the publication-only case. |
| `2026-07-30T06:29:00Z` | `P3/BG-PUBLISH-SMALL` current hot-path measurement | Fresh run `mpla-booster-20260730T062900Z` sealed partial evidence and correctly rejected its first sample: public service completed in `92.891166 ms`, but publication preserved fixture attribution `fixture-s4-chain-v2` while the independent oracle produced a different attribution root. Root metadata matched; semantic root IDs did not, so no performance score is eligible. Its unqualified phase receipt identifies `43.038083 ms` storage sequence and `36.729375 ms` semantic total. | `FAIL_REPAIRING` (oracle-attribution comparability) | `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/booster-scorecard-20260730T062900Z`; append-only resolution “current hot-path publication measurement” | Pass the exact immutable fixture attribution descriptor to the independent oracle; add focused oracle/incremental equivalence coverage, rebuild, and rerun once from a fresh root. |
| `2026-07-30T06:40:02Z` | `P3/BG-PUBLISH-SMALL` audit correction | Review of the sealed partial receipt found a second, separate validity failure: the physical depth-one mount had exactly one lower allocation, yet the candidate semantic receipt reported `32,831` entries/root `1ccc…` while the independent merged-tree oracle reported `4,248`/`70d9…`. The oracle also incorrectly used the transient run ID rather than the durable attribution descriptor. | `FAIL_REPAIRING` (semantic/physical cache identity plus oracle-attribution harness defect) | The retained `mpla-booster-20260730T062900Z` partial evidence and source command at `mpla_speed_scorecard.rs` | Add a bounded read-only cache-ref/projection inspection receipt to locate the divergence, repair the exact source boundary, and separately parameterize the oracle with the receipt attribution before any fresh timing. |
| `2026-07-30T06:44:22Z` | `P3/BG-PUBLISH-SMALL` cache-boundary inspection preparation | Added a closed no-argument inspector for the sealed v2 cache. Its parser regression passed 1/1 and the normal-root-only security grammar passed 3/3; the command returns only manifest/ref/projection/locator identity metadata and accepts no caller path, branch, or mutation input. | `IN_PROGRESS` | Append-only `TEST-REPORT.md` cache-inspection parser and command-security entries | Cross-build only the changed coordinator, rebuild the normal gateway through the required entrypoint, then take one supported read-only inspection receipt. That receipt determines whether v2 construction or run-local attachment introduced the semantic/physical divergence; no timing claim will be made first. |
| `2026-07-30T06:48:30Z` | `P3/BG-PUBLISH-SMALL` isolated cache-consumer reload | The required normal M3 rebuild started a fresh default listener at `127.0.0.1:7878`, but the qualified v2 consumer intentionally uses its own `127.0.0.1:7881` PID/configuration and remains old. The host binary is already rebuilt, so only that consumer needs a supported restart with no repeated build. | `IN_PROGRESS` | `TEST-REPORT.md` normal-M3 rebuild resolution; PIDs `70080` default and `58039` isolated consumer | Restart only the fixed v2 read-only consumer through the supported launcher, prove the manager inventory is empty, then take one read-only cache inspection receipt. |
| `2026-07-30T06:49:13Z` | `P3/BG-PUBLISH-SMALL` isolated cache-consumer reload | The supported launcher replaced only the intended v2 consumer: PID `58039` stopped and PID `70303` now owns `127.0.0.1:7881` with the fixed read-only v2 configuration. | `IN_PROGRESS` | Process/listener receipt and `TEST-REPORT.md` v2 cache-consumer reload resolution | Query both supported inventories; if empty, create one inspection-only sandbox, invoke the closed inspector once, collect its receipt, then perform exact-ID cleanup. |
| `2026-07-30T06:49:18Z` | `P3/BG-PUBLISH-SMALL` cache-boundary live receipt | Both supported inventories are empty. A one-sandbox disposable public-runtime inspection is authorized: it stages only the freshly hashed `mpla-speed-poc-v1` into a temporary workspace, invokes exactly `inspect-prepared-fixture-cache` with no args, and will destroy that exact sandbox after its terminal receipt. It is explicitly non-timed and cannot produce a scorecard result. | `IN_PROGRESS` | `TEST-REPORT.md` inventory preflight results; coordinator SHA-256 `c142285f…` | If the cache ref/projection already disagree with physical depth, create a distinct v3 cache rather than mutate v2. If they agree, inspect run-local attachment next. |
| `2026-07-30T06:50:05Z` | `P3/BG-PUBLISH-SMALL` cache-boundary live receipt | The one-shot public inspection completed and the exact sandbox was destroyed. The sealed `fixture-depth-1` ref/canonical receipt already contains root `3b4cbd5a…` and attribution `1da56bc0…`, while the read-only projection contains exactly the one expected lower allocation `1b829279…`. The fresh failing candidate's `1ccc…` root is thus its ten-file delta from a bad cached parent; it is not introduced by the run-local attachment or by the reply path. | `FAIL_REPAIRING` (sealed cache-construction semantic/physical divergence) | Terminal public receipt for sandbox `eos-59294cf1-19c6-4685-bf6b-ea7e4f314a04`, branch ref/projection/locator identity, and `TEST-REPORT.md` inspection entry | Verify exact-ID cleanup, then trace cache construction's semantic parent selection. Build a distinct v3 cache only after a focused regression proves the depth-one semantic root describes its one-lower OverlayFS tree; v2 remains immutable. |
| `2026-07-30T07:03:00Z` | `P3/BG-PUBLISH-SMALL` v3 merged-tree repair | Proved the branch refs are immutable; the actual defect is that an initial publication semantically scanned only its writable `upper_dir` after strict unmount, while the exact oracle scans the merged OverlayFS projection. Initial publication now captures the sealed, empty-cgroup-proven merged workspace before unmount; incrementals retain their bounded affected-upper hot path. The old cache is untouched and a distinct `s4-chain-v3` profile/control root/Docker volume is introduced. Focused lifecycle 18/18, CLI 3/3, command security 3/3, and ARM64 cross-build passed. | `PASS` local repair; physical v3 cache pending | `TEST-REPORT.md`; ARM64 coordinator SHA-256 `c79d36aefac27a9d40adf279631532e6bfe8afeecfd15eaf47799ce6dbee0d69` | Rebuild the required gateway, create one v3 cache through the writable builder, validate depth-one semantic root against the exact merged oracle, then take fresh sub-50-ms publication samples. |
| `2026-07-30T07:05:00Z` | `P3/BG-PUBLISH-SMALL` v3 builder deployment | Required generic M3 gateway rebuild completed with fresh PID `75771`. The next material attempt is a separate supported launcher instance at `127.0.0.1:7882`, using only the writable `eos-mpla-prepared-s4-phase-profile-v3` volume. It will be preflighted through manager and observability CLIs before the one serialized warm; the sealed v2 consumer remains untouched on `:7881`. | `IN_PROGRESS` | `TEST-REPORT.md` required rebuild receipt | Start builder, verify empty inventories, then create/retain exactly one immutable v3 cache generation. |
| `2026-07-30T07:10:00Z` | `P3/BG-PUBLISH-SMALL` v3 isolated coordinator routing | The v3 coordinator had a hard-coded `host.docker.internal:7881` client endpoint, which would have sent the writable v3 cache warm to the sealed v2 gateway. It now accepts only `host.docker.internal:7881-7889` through a strict configuration variable forwarded by the namespace runner; v3 builder and consumer configs select only `:7882` and `:7883`. Focused routing 8/8, namespace target 10/10, and dense/sparse semantic 1/1 passed. Fresh static ARM64 coordinator SHA-256 is `0ebdee61b6b25e968a40e4cd41709a649f49add71a72772bda46ad9bb3c94b83`. | `PASS` local repair; deployment pending | `TEST-REPORT.md` entries 07:07–07:10 | Rebuild the required gateway and restart only the isolated v3 builder, then execute one serialized cache warm through `:7882`. |
| `2026-07-30T07:11:00Z` | `P3/BG-PUBLISH-SMALL` rebuilt v3 routing deployment | The required generic M3 rebuild completed and replaced only its `127.0.0.1:7878` listener with PID `79671`. The builder process remains separately bound to `:7882` and must be reloaded to inherit the closed configuration endpoint. | `IN_PROGRESS` | `TEST-REPORT.md` required rebuild receipt | Reload only the v3 builder listener, verify inventories, then perform exactly one serialized v3 cache warm. |
| `2026-07-30T07:12:00Z` | `P3/BG-PUBLISH-SMALL` v3 builder reload | Supported launcher stopped only prior v3 builder PID `75930` and started PID `79845` at `127.0.0.1:7882` under the strict builder config. The next operation is inventory-only; no fixture construction has started. | `IN_PROGRESS` | `TEST-REPORT.md` builder reload receipt | Verify empty supported inventories, then warm the distinct v3 volume exactly once through `:7882`. |
| `2026-07-30T07:13:00Z` | `P3/BG-PUBLISH-SMALL` v3 builder preflight | The supported manager and observability inventories both returned empty against `127.0.0.1:7882`; the writable v3 volume has no live owner. | `PASS` | `TEST-REPORT.md` refreshed-builder inventory receipt | Create only the two required run-scoped sandboxes and issue the closed cache-builder command once. |
| `2026-07-30T07:14:00Z` | `P3/BG-PUBLISH-SMALL` v3 persistent fixture warm | A fresh immutable stage contains the freshly hashed ARM64 coordinator, runtime client, catalog exporter, catalog, and gateway token. The only physical work about to start is the serialized administrative cache warm through the isolated `:7882` endpoint; it is not a measured publication sample. | `IN_PROGRESS` | `TEST-REPORT.md` staged cache-warm entry | Await one bounded compact seal receipt, clean up exact IDs, prove the depth-one merged-tree semantic identity, then run the read-only v3 publication measurement. |
| `2026-07-30T07:14:34Z` | `P3/BG-PUBLISH-SMALL` v3 initial-publication qualification | The single warm attempt did not seal. Its first one-GiB initial publication completed durable metadata work but failed only `semantic_input_matches=false`: affected paths `1/1`, immutable payload `0/0`, stable logical bytes `1,073,741,824/1,073,741,824`, roots match. The compact command receipt reported `8.630798962 s` command work / `34.266791641 s` outer. This is a semantic-input qualification defect, not a public reply loss or a valid timing sample. | `FAIL_REPAIRING` | `TEST-REPORT.md` serialized v3 cache-warm result; exact candidate/coordinator/session IDs retained for bounded inspection | Preserve the failed v3 cache generation. Trace only the initial merged-tree scan / qualification boundary; prove its correction locally before allocating a fresh immutable v4 fixture identity. |
| `2026-07-30T07:15:00Z` | `P3/BG-PUBLISH-SMALL` allocated-zero qualification repair | The focused coordinator regression passed: an initial dense zero file can have a complete semantic entry and stable 1-GiB logical receipt with zero physical semantic reads when OverlayFS reports it as a hole-only extent. Missing semantic entry or a read count beyond the closed logical size still fails. | `PASS` focused repair | `cargo fmt --check`; `mpla-speed-poc-v1` unit 1/1; append-only `TEST-REPORT.md` | Retain failed v3 untouched; advance only the server-owned fixture identity/configuration to v4, cross-build, then execute one new serialized v4 warm. |
| `2026-07-30T07:16:00Z` | `P3/BG-PUBLISH-SMALL` v4 source/grammar qualification | The v4 closed cache identity is tested and the prior v3 volume is unreferenced: coordinator unit 12/12, fixture CLI 3/3, command-security 3/3, and workspace publication lifecycle 18/18 all pass. | `PASS` | `TEST-REPORT.md` v4 identity suite | Cross-build the ARM64 coordinator and rebuild the required host gateway, then start a new isolated writable v4 builder on its own listener. |

### 13.5 Blocker and decision ledger

| UTC | Type | Description | Checks exhausted | Resolution / owner |
|---|---|---|---|---|
| — | — | No current hard blocker | — | Continue with P0 |
| `2026-07-29T17:17:27Z` | Resolvable harness defect | Publication used its 600-second measurement coordinator to construct the heavy prepared chain; the case cannot produce the matrix's bounded small-delta result this way. | Fresh sealed timeout, source review, historical timing comparison, and matrix fixture/timer requirements. | `FAIL_REPAIRING`; separate preparation from measured operation with durable receipts, then run a fresh publication-only case. |

For a resolvable failure, record `FAIL_REPAIRING`, the root cause, and the next
focused check. Use `HARD_BLOCKED` only after safe in-scope options are exhausted
and progress needs an external decision or state change.

## 14. Final report requirements

The final report must lead with:

1. `POC_CORRECTNESS_PASS|FAIL`
2. `POC_100X_SUPPORTED|NOT_SUPPORTED`
3. `POC_500X_SUPPORTED|PARTIAL|NOT_SUPPORTED`
4. `AG_SQUASH_PASS|FAIL|UNKNOWN`
5. `AG_STREAM_PASS|FAIL|UNKNOWN`

Then include:

- raw samples, median, max, exact ratios, and absolute ceilings for every gate
- a candidate/control comparability table
- correctness and security gate results
- source/config/binary/fixture/image identities
- resource envelope and wall-clock result
- poll/CLI roundtrip counts
- cleanup and leak results
- invalidated or reused evidence with reasons
- exact failure reasons for every non-pass
- verified manifest hash and evidence root

Do not describe `760x` as the Booster scorecard result unless the new formal
scorecard independently produces that result. Until then, call it the sealed
matched publication calibration.

## 15. Next-agent launch capsule

Start with these actions:

1. Read the governing files in section 2 and inspect the dirty worktrees.
2. Assign a unique UTC run ID and create, but do not overwrite, the new evidence
   root.
3. Replace or parameterize every hard-coded old run/lease/branch/evidence
   identity in the focused harness.
4. Verify the public activation/fork/rollback surface before timing it.
5. Run the preflight through the supported gateway and CLIs, with
   `CAP_SYS_ADMIN` bit 21 enabled for the lifecycle process and no tmpfs.
6. Execute one focused gate at a time, beginning with
   `BG-ACTIVATE-EXACT`.
7. Update the tracker and append-only evidence after every attempt.
8. Run the full focused campaign only after each focused gate passes.

| `2026-07-30T07:17:30Z` | `P3/BG-PUBLISH-SMALL` v4 coordinator and host deployment | The static AArch64 v4 coordinator was freshly cross-built (SHA-256 `c565a30e88f4c1aff51f5bdb51938bde9aa8e429e5e0854c258a116fd89bc87d`) and embeds the v4 fixed fixture path. The required generic M3 rebuild completed and replaced only its `127.0.0.1:7878` listener with PID `84061`; packaged daemon SHA-256 `e26bc58892b5707b3ba3fe2f234fb8862fd715592c0611636e1252b83d0bec9f`. v2 and failed v3 listeners/volumes remain untouched. | `PASS` deployment qualification | `TEST-REPORT.md` v4 artifact/gateway receipt | Start a fresh v4-only writable builder on `:7884`; require empty manager and observability inventories before allocating any new resource. |
| `2026-07-30T07:18:00Z` | `P3/BG-PUBLISH-SMALL` v4 builder preflight/cache warm | A distinct writable v4 builder is authorized only at `127.0.0.1:7884`, using Docker volume `eos-mpla-prepared-s4-phase-profile-v4`. It has no shared control root or listener with v2/v3. The first physical action is supported inventory preflight; no run-scoped sandbox exists yet. | `IN_PROGRESS` | Fresh coordinator SHA-256 `c565a30e…`; append-only `TEST-REPORT.md` PENDING entry | Start the dedicated builder, require empty manager/observability inventories, then issue exactly one serialized administrative cache warm. |
| `2026-07-30T07:20:00Z` | `P3/BG-PUBLISH-SMALL` v4 serialized cache warm | Supported preflight returned empty manager and observability inventories. Exactly two run-scoped builder sandboxes now exist: candidate `eos-7733ae94-e238-45d6-ac4b-d041ccc87b7b` and coordinator `eos-60d1c53d-2b73-4973-b813-db093ffb2fb5`, with coordinator session `00000118c700b315be1a6e`. One closed cache-warm command is authorized against only the v4 tool root and `:7884`. It is administrative, not timed publication work. | `IN_PROGRESS` | `TEST-REPORT.md` exact command/PENDING receipt | Await one bounded terminal seal receipt. Do not create a second warm or touch the v2/v3 volumes. |
| `2026-07-30T07:32:37Z` | `P3/BG-PUBLISH-SMALL` v4 failed-warm diagnosis | The sole v4 warm completed no later than depth five and returned exit `2` after `18.808` seconds, with no terminal line. The candidate has `8,614,850,560` bytes allocated. One supported, read-only `df`/`stat` receipt against that retained failed candidate is authorized to discriminate capacity exhaustion from a dense-write/terminal defect; it cannot publish, build, or resume. | `IN_PROGRESS` | Append-only `TEST-REPORT.md` diagnosis PENDING; exact candidate/session IDs | Record the compact state result, retain v4 unchanged, then repair/prove a new fixture identity only if the fault is confirmed. |
| `2026-07-30T07:35:00Z` | `P3/BG-PUBLISH-SMALL` v4 failed-warm root cause | The supported diagnostic itself failed before its shell began: namespace scratch creation returned `ENOSPC`. Observability and Docker accounting show the v4 persistent fixture volume at `9.747GB` / `8,614,850,560` allocated bytes while the host has about `347GiB` free; Docker Desktop's backing store contains `122.4GB` of local volumes (`78.78GB` reclaimable). The true fixed chain is `9GiB + 5MiB` logical, below the matrix 10GiB limit but not viable without working headroom. | `FAIL_REPAIRING` (Docker ext4 capacity preflight/storage provisioning) | Resolved append-only diagnostic in `TEST-REPORT.md`; no second warm | Implement and test a fail-fast closed capacity preflight; preserve v4. Resume only with a new immutable generation on an ext4 Docker store that proves full-chain-plus-headroom capacity. |
| `2026-07-30T07:39:00Z` | `P3/BG-PUBLISH-SMALL` fixture-builder capacity contract | The closed fixture policy now requires `12GiB + 6MiB` available ext4 space before first write: the fixed `9GiB + 5MiB` chain, independently retained `1GiB + 1MiB` control source, and `2GiB` working headroom; it also requires 4,096 available inodes. The builder records an exact `statvfs` receipt on success and fails before any fixture payload write when either requirement is absent. Formatting, parser/policy tests `4/4`, and coordinator tests `12/12` pass. | `PASS` local permanent repair; physical provisioning pending | Resolved append-only `TEST-REPORT.md` capacity-contract entry | Retain v4 unchanged. Establish a new immutable cache only after proving capacity on the intended Docker ext4 store, then return to the sub-50-ms publication measurement. |
| `2026-07-30T07:57:07Z` | `P3/BG-PUBLISH-SMALL` Docker capacity provisioning | Read-only inspection confirmed Docker Desktop is persistently capped at `147,456 MiB` (144 GiB) while its overlay store contains the retained fixtures and needs a fresh `12 GiB + 6 MiB` generation. Host free space is sufficient. A non-destructive increase of the VM disk ceiling to `204,800 MiB` (200 GiB), followed by one controlled Docker Desktop restart, is authorized; no image, container, volume, cache, or retained v4 artifact will be removed. | `IN_PROGRESS` | Docker settings receipt and existing capacity diagnosis | Verify the new ext4 capacity with the closed v5 builder preflight before any payload write, then take exactly one serialized new-generation warm. |
| `2026-07-30T08:08:30Z` | `P3/BG-PUBLISH-SMALL` v5 isolated builder preflight | The fresh v5 orchestration path is closed and tested: all builder artifacts target `s4-chain-v5`, the builder defaults to `:7886`, and the scorecard consumer is closed to v5 at `:7887`. The next physical action is restricted to starting the dedicated v5 builder and querying only its supported manager/observability inventories; neither action writes a fixture payload. | `IN_PROGRESS` | `TEST-REPORT.md` v5 closure `23/23`; current ARM64 coordinator/oracle build | Start only the dedicated v5 builder on `:7886`; require empty inventories and the builder's `12 GiB + 6 MiB` capacity receipt before authorizing one serialized cache warm. |
| `2026-07-30T08:09:00Z` | `P3/BG-PUBLISH-SMALL` v5 serialized cache warm | The supported isolated v5 builder has PID `94848` at `127.0.0.1:7886`; manager and observability inventories are both empty. A single administrative warm is authorized through this builder only. It may create exactly a candidate/coordinator pair and must fail before payload write unless the new Docker ext4 store proves the fixed `12 GiB + 6 MiB` and inode requirement. | `IN_PROGRESS` | `TEST-REPORT.md` preflight PENDING; v5 gateway PID/empty inventory receipt | Await one bounded result, then destroy exactly the created builder sandboxes. Preserve v2/v3/v4 and use the v5 manifest only after its immutable seal and semantic identity check pass. |
| `2026-07-30T08:10:00Z` | `P3/BG-PUBLISH-SMALL` v5 fixture warm result / read-only consumer | Exactly one v5 warm sealed the fixed 8-layer, `9,668,919,296`-logical-byte chain and returned `42.082 s` outer / `38.765 s` builder elapsed. The fixture is valid for read-only inspection but its administrative setup is still above the desired 30-second target; layer 1/5 durability-semantic spans are isolated for a later non-hot-path repair. The next physical step starts a separate read-only v5 consumer at `:7887` and checks empty inventories only. | `PASS` fixture seal; setup optimization open | Compact terminal builder receipt and `TEST-REPORT.md` resolved warm entry | Start only the v5 read-only consumer, require empty inventories, then take one disposable merged-manifest/semantic inspection before timing any small publication. |
| `2026-07-30T08:10:20Z` | `P3/BG-PUBLISH-SMALL` v5 manifest/semantic inspection | The v5 read-only consumer is running at `127.0.0.1:7887` (PID `95509`) and both supported inventories are empty. One new temporary inspection sandbox is authorized to invoke only `inspect-prepared-fixture-cache` with the current staged coordinator. The fixture volume is mounted read-only and no publication/cache-build grammar is issued. | `IN_PROGRESS` | `TEST-REPORT.md` PENDING inspection command and consumer inventory receipt | Record its bounded manifest/depth/semantic result and destroy the exact sandbox. Permit the hot publication probe only if the v5 fixture is fully valid. |
| `2026-07-30T08:10:30Z` | `P3/BG-PUBLISH-SMALL` v5 manifest/semantic inspection result | The sole read-only inspection passed in `34.700 ms`. Fixed v5 identity is present and branch depths `1`, `5`, and `8` exactly match their projected/canonical semantic roots and attributions and their `1`/`5`/`8` lower allocation counts. Disposable sandbox `eos-91ea364b-d462-4635-852e-14b8189adb12` was destroyed. | `PASS` immutable fixture qualification | Compact terminal inspection receipt and destroy receipt | Verify both inventories are empty, then stage current artifacts and take one bounded publication-only probe. |
| `2026-07-30T08:11:00Z` | `P3/BG-PUBLISH-SMALL` v5 focused scorecard measurement | Exact-ID inspection cleanup was confirmed by empty manager and observability inventories. One fresh evidence root `mpla-booster-p3-v5-20260730T081100Z` was authorized for only the formal `publication` case through the read-only v5 consumer. Its then-configured 600-second case ceiling was a validity guard; that ceiling is retired and superseded by the current independent publication-phase cap. The desired measured small-delta end-to-end latency remained below `50 ms` with unchanged semantic/durability/allocation gates. | `IN_PROGRESS` | `TEST-REPORT.md` focused-probe PENDING entry; qualified v5 manifest inspection | Historical instruction at the time: await compact sealed case verdict/evidence identity. If any valid sample is >=50 ms, diagnose only its dominant measured phase and retry under a new run identity. |
| `2026-07-30T08:12:25Z` | `P3/BG-PUBLISH-SMALL` v5 attach service repair/deployment | The first v5 focused run was invalidated before publication: its v5 attachment was rejected by stale v4 literals in the runtime operation registry and frozen command-security path. The repair centrally derives both from `PREPARED_FIXTURE_PROFILE`; command-security `3/3` and service-graph `8/8` pass. The required generic M3 rebuild is authorized next, followed by a v5 consumer-only restart and fresh-run retry. | `FAIL_REPAIRING` (deployment closure) | Partial evidence `mpla-booster-p3-v5-20260730T081100Z`; local focused suites | Rebuild the required gateway/daemon, restart only `:7887`, verify empty inventories, then rerun only BG-PUBLISH-SMALL under a new evidence root. |
| `2026-07-30T08:13:35Z` | `P3/BG-PUBLISH-SMALL` v5 repaired-consumer reload | The required generic rebuild packaged repaired daemon SHA-256 `902807f6…e31be` and replaced the default listener only. The next physical action restarts only the isolated v5 read-only consumer at `:7887` and queries its inventories. No fixture/cache/publish operation is authorized until that consumer proves empty state. | `IN_PROGRESS` | Generic rebuild receipt / `TEST-REPORT.md` PENDING | Reload only `:7887`; require empty manager and observability responses, then run a fresh publication-only evidence root. |
| `2026-07-30T08:14:00Z` | `P3/BG-PUBLISH-SMALL` v5 focused scorecard retry | The repaired v5 consumer is live as PID `98598` at `:7887`; its manager and observability inventories are empty. A fresh `mpla-booster-p3-v5-20260730T081400Z` evidence root is authorized for only the publication case. Its goal remains sub-50-ms small-delta end-to-end latency under all original correctness/durability/allocation gates. | `IN_PROGRESS` | Consumer reload receipt and fresh root PENDING | Await its sealed verdict. Do not reuse the invalidated pre-attach-repair root. |
| `2026-07-30T08:14:25Z` | `P3/BG-PUBLISH-SMALL` compact-sequence destroy validation | The fresh v5 retry passed the repaired attachment boundary but safety-sealed partial evidence when destroy authority could not locate the new compact immutable sequence header for the cleanup receipt. The coordinator command ended at `12.627205923 s`; no latency sample is valid or promoted. | `FAIL_REPAIRING` (compact journal / destroy-authority compatibility) | `evidence/runs/mpla-booster-p3-v5-20260730T081400Z`; exact operation error and cleanup receipts | Trace the persisted cleanup identity and `ATTEMPTS.json` location, prove the smallest corrective regression locally, then rebuild/reload only the v5 consumer and issue a new publication-only root. |
| `2026-07-30T08:16:20Z` | `P3/BG-PUBLISH-SMALL` compact/legacy destroy-authority repair | Source confirmation found a supported legacy per-operation `ATTEMPT.json` path alongside the newer compact sequence header. Destroy validation had required the compact file unconditionally, so a valid legacy cleanup authority failed closed before the receipt could be checked. The repair is header-first and fail-closed: a present compact header is always strictly validated; only an absent header permits strict validation of the exact legacy cleanup marker. Local durable-journal regression matrix is 4/4, including tamper rejection and no fallback from malformed compact metadata. | `PASS_LOCAL_REBUILD_PENDING` | Append-only local regression receipt; invalid partial v5 evidence retained | Rebuild using the mandatory launcher, reload only `:7887`, verify empty inventories, then issue one new publication-only v5 run. |
| `2026-07-30T08:18:00Z` | `P3/BG-PUBLISH-SMALL` repaired compact/legacy Linux deployment | The mandatory package rebuild and the isolated v5-consumer reload both completed. The live consumer at `:7887` replaced its prior listener and packages daemon `82de6d417943…220864d4d` plus storage helper `ff544d935018…8549742698`; supported manager and observability inventories are empty. Exactly one fresh v5 publication-only root is now authorized. | `IN_PROGRESS` | `TEST-REPORT.md` package/reload receipt; 4/4 local compact/legacy validator matrix | Run only `mpla-booster-p3-v5-20260730T081800Z`. Seal and report all phase gates; do not promote a timing if any gate fails. |
| `2026-07-30T08:18:05Z` | `P3/BG-PUBLISH-SMALL` artifact freshness preflight | The newly authorized runner sealed a partial root before candidate creation because its staged ARM64 coordinator and oracle predate the repaired shared storage-admin source. This is an artifact-deployment preflight, not a publication latency or service failure. | `FAIL_REPAIRING` (staged coordinator/oracle freshness) | Partial root `mpla-booster-p3-v5-20260730T081800Z`; exact runner freshness rejection | Cross-build only `mpla-speed-poc-v1` and `mpla-poc-oracle` for `aarch64-unknown-linux-musl`, verify identities, then create a new publication-only root. |
| `2026-07-30T08:19:20Z` | `P3/BG-PUBLISH-SMALL` fresh ARM64 staged-artifact retry | The coordinator and oracle were cross-built against the repaired library: `mpla-speed-poc-v1` SHA-256 `6f960a62aff7…d2dfd191`; `mpla-poc-oracle` SHA-256 `cd2aa0c32a41…90cb7415`. The live v5 consumer remains the newly packaged isolated listener. The next physical invocation begins with supported empty-inventory checks and has exactly one fresh publication-only root. | `IN_PROGRESS` | Cross-build identity receipt; append-only PENDING test record | Require empty inventories, then run only `mpla-booster-p3-v5-20260730T081920Z`; report a latency only if the full sealed gate set passes. |
| `2026-07-30T08:19:25Z` | `P3/BG-PUBLISH-SMALL` coordinator freshness recheck | Supported inventories were still empty, but the runner correctly rejected the coordinator executable alone as older than its exact Cargo-input set and sealed before candidate creation. The oracle is fresh; the predecessor command did not leave a completed/relinked coordinator artifact. | `FAIL_REPAIRING` (coordinator artifact relink) | Partial root `mpla-booster-p3-v5-20260730T081920Z`; exact runner freshness error | Complete and verify a coordinator-only ARM64 release build before granting a new publication root. |
| `2026-07-30T08:19:40Z` | `P3/BG-PUBLISH-SMALL` post-relink publication retry | A completed coordinator-only ARM64 release build preserved SHA-256 `6f960a62aff7…d2dfd191` but advanced the artifact mtime to `1785400213`, beyond every repaired source input (latest `1785399962`). The oracle remains fresh, and no sandbox state changed after the last empty-inventory proof. Exactly one new publication-only root is authorized. | `IN_PROGRESS` | Verified coordinator artifact identity/mtime; prior supported empty-inventory receipt | Run only `mpla-booster-p3-v5-20260730T081940Z` and promote a result only after all sealed gates pass. |
| `2026-07-30T08:20:45Z` | `P3/BG-PUBLISH-SMALL` V5 semantic-oracle mismatch | The repaired-path V5 publication completed service work but was correctly rejected as non-promotable: its initial full-tree semantic receipt had `61` entries / `5,737` bytes while the independent holder-view oracle observed `27,808` entries / `910,163,968` bytes. Root cause: the service process scanned its own namespace rather than the holder mount namespace that contains the live OverlayFS merge. | `FAIL_REPAIRING` (fixture semantic provenance) | Preserved partial root `mpla-booster-p3-v5-20260730T081940Z`; compact oracle/semantic receipts | Reject V5 permanently. Add a typed holder-namespace semantic snapshot, bind it to a new V6 manifest, then rebuild the gateway before any new cache build or timed publication. |
| `2026-07-30T08:35:10Z` | `P3/BG-PUBLISH-SMALL` V6 holder-namespace snapshot local qualification | The V6 repair uses the authenticated storage helper to enter the attested holder namespace and run a single-process full-tree scan under the existing no-process-creation seccomp profile. Local regressions pass: serial and threaded scans agree exactly on canonical roots/records across nested sparse and hard-linked files; fixed wire rejects injected scanner paths; V6 fixture CLI/manifest tests pass `4/4`. This is setup-only; bounded incremental P3 publication remains unchanged. | `PASS_LOCAL_REBUILD_PENDING` | `TEST-REPORT.md` resolved focused tests; source scoped to semantic/storage-admin/lifecycle/fixture builder | Rebuild with the mandatory launcher, verify empty supported inventories, then build exactly one persistent V6 fixture and require independent oracle agreement before timing the sub-50-ms P3 publication path. |
| `2026-07-30T09:12:30Z` | `P3/BG-PUBLISH-SMALL` V6 confined-trie completion / builder reload | The first real V6 holder snapshot proved the mount-namespace binding and then failed closed because the trie stage still spawned one attribution worker after seccomp denied process creation. The storage helper now uses an equivalent serial trie reducer only for initial holder attestation; focused full-tree semantic equivalence passed. Fresh arm64 coordinator/oracle binaries and daemon/helper packages were built, and only the isolated V6 builder at `127.0.0.1:7888` was reloaded. | `IN_PROGRESS` | `TEST-REPORT.md` confined-reducer regression; packaged daemon `9ae728693ad0db18aa8ec611fd9544e9aea185a0397588389932090891c005e9`, helper `c65a5bf64980c9dd9674ad03e853e1a79b10b427b351660dbbb7e318e318ea8d` | Issue exactly one V6 persistent cache build. Require independent holder-view oracle agreement before starting the read-only consumer or timing P3. |
| `2026-07-30T09:13:40Z` | `P3/BG-PUBLISH-SMALL` V6 cache-root rejection | The V6 builder rejected the request before sandbox creation because its earlier failed attestation had left an unsealed `control-source` directory at the fixed root. That proves the cache validator refuses partial state; it is not a semantic or timing sample. The partial volume/root is retained unmodified. | `FAIL_REPAIRING` (generation hygiene only) | Exact bounded builder error and resolved append-only test report entry | Use a new V7 profile/root/named volume and do not delete, reuse, or mount the V6 cache for timed work. |
| `2026-07-30T09:15:15Z` | `P3/BG-PUBLISH-SMALL` V7 fresh-generation qualification | All closed V7 identities were locally verified: Rust fixed-profile/root tests `2/2`, host builder/runner harness tests `23/23`, new root `s4-chain-v7`, fresh persistent volume, and isolated builder/consumer sockets `7890`/`7891`. The then-configured 600-second case ceiling is retired and superseded by the current phase-local budget policy. | `IN_PROGRESS` | Resolved `TEST-REPORT.md` V7 closure entry | Historical instruction at the time: cross-build/repackage V7 artifacts, start only the V7 builder, then issue one V7 cache warm and independently attest its holder-view semantics before P3 timing. |
| `2026-07-30T09:21:00Z` | `P3/BG-PUBLISH-SMALL` V8 endpoint-preflight permanence | V7 failed before its first session because the closed callback allowlist omitted its builder endpoint, but the builder had already created `control-source`. The permanent correction validates the fixed authenticated `RuntimeClient` before any cache write; V8 is isolated at root `s4-chain-v8`, named volume `eos-mpla-prepared-s4-phase-profile-v8`, builder/consumer `:7892`/`:7893`. Formatter, fixed-endpoint `1/1`, profile parser `1/1`, and host harness `23/23` pass. | `IN_PROGRESS` | Resolved `TEST-REPORT.md` V8 closure entry | Cross-build/repackage, start only the V8 builder, then make one 800-second-bounded cache warm. Start the V8 consumer/P3 publication only after full holder-view seal. |
| `2026-07-30T09:37:09Z` | `P3/BG-PUBLISH-SMALL` V9 holder-tree semantic scope | V8 correctly failed closed before sealing: its initial holder receipt covered `32,928` entries / `1,078,326,871` bytes but the qualifier compared those full-tree fields to a one-path delta. The permanent repair uses an independent holder oracle for the bootstrap full-tree entry count and byte ceiling; incremental checks separately require the complete post-apply entry count, exact `affected_record_count`, affected-stream accounting, roots, durability, stationary invariants, and freshness. Focused regressions `7/7`, V9 endpoint `1/1`, parser `1/1`, and harness `23/23` pass. | `IN_PROGRESS` | Resolved `TEST-REPORT.md` V8 diagnosis and V9 closure entries; V8 root preserved immutable | Cross-build/repackage once, build exactly one V9 cache with builder `:7894` and an 800-second outer watchdog; start the read-only V9 consumer/P3 only after its independent holder oracle seals the cache. |
| `2026-07-30T09:45:15Z` | `P3/BG-PUBLISH-SMALL` V9 staged-oracle diagnosis / V10 repair | V9's single cache warm stopped before timing or sealing with a bounded `ENOENT`: the new bootstrap holder-tree attestation called `mpla-poc-oracle`, but fixture staging contained only the coordinator and omitted that oracle. V9 residue is preserved. V10 permanently stages the oracle, requires it in the pre-write campaign-tool preflight, resolves it from the coordinator's approved tool root, and has fresh root/volume plus builder/consumer `:7896`/`:7897`. Local endpoint, oracle-command, fixed-profile, and host-harness regressions pass `1/1`, `1/1`, `1/1`, `24/24`. | `IN_PROGRESS` | V9 resolved append-only report; V10 local regression receipt | Cross-build/repackage V10, start only the V10 builder, require empty inventory, then issue exactly one 800-second-bounded cache warm; start P3 only after its independent holder-view seal. |
| `2026-07-30T09:57:10Z` | `P3/BG-PUBLISH-SMALL` V10 persisted-allocation root-cause check | V10's one warm is preserved after its initial holder/oracle comparison disagreed (`1,078,326,871` holder bytes versus three zero-payload reactivated entries). Source tracing identifies a concrete invariant gap: an initial external MPLA overlay with `projection=None` leaves `lower_dirs_newest_first` unset, so workspace creation substitutes the ordinary LayerStack lower; reactivation uses only persisted allocation uppers. One disposable, supported-CLI, read-only allocation-tree inspection is authorized to confirm the retained bytes before the permanent explicit-empty-lower repair. | `IN_PROGRESS` | Append-only PENDING report; V10 retained root | Read only the V10 allocation tree, destroy the exact diagnostic resources, then land and locally test the explicit initial empty-lower repair. |
| `2026-07-30T10:03:00Z` | `P3/BG-PUBLISH-SMALL` V10 lower-stack provenance repair | The supported read-only inspection proved V10's `upper/layer-000.bin` remains exactly `1,073,741,824` bytes; earlier `evicted_upperdir_bytes` was an accounting metric, not deletion. The permanent repair removes the optional external-overlay lower stack: the API now requires an exact nonempty vector; fresh MPLA creation persists a private empty lower beside its upper/work, and reactivation passes its exact allocation uppers. Focused initial and reactivation tests plus formatter pass. | `PASS_LOCAL_REBUILD_PENDING` | Resolved append-only V10 diagnosis and focused local test receipt | Preserve V10. Close fresh V11 root/volume/endpoints, then cross-build/rebuild and take one holder/oracle-attested cache warm before P3 timing. |
| `2026-07-30T10:06:00Z` | `P3/BG-PUBLISH-SMALL` V11 immutable-generation closure | V11 is a new closed profile, root, volume, stage root, builder `:7898`, and read-only consumer `:7899`; the active coordinator/oracle and parser harnesses have been advanced together. It is the only generation eligible to validate the repaired lower-stack provenance; V10 remains retained and never retried. | `IN_PROGRESS` | Append-only V11 local-test PENDING receipt | Pass the focused V11 closed-identity/fixture parser/harness tests, then cross-build/repackage and start only the V11 builder. |
| `2026-07-30T10:08:30Z` | `P3/BG-PUBLISH-SMALL` V11 rebuilt builder / one warm authorized | V11 local closure passed: formatter; root `1/1`; endpoints `1/1`; fixture parser `1/1`; host harness `24/24`. Fresh ARM64 coordinator/oracle hashes are `8b095380…6aef99` and `cd2aa0c…cb7415`. The mandatory launcher rebuilt and started only the V11 builder at `:7898` (PID `35897`, daemon `e137e909…ffcd185`); supported manager inventory is empty. | `IN_PROGRESS` | Resolved deployment record and V11 warm PENDING report | Run exactly one 800-second administrative V11 warm. Proceed to consumer/P3 only if initial/incremental holder oracle attestation seals. |
| `2026-07-30T10:11:18Z` | `P3/BG-PUBLISH-SMALL` V11 reactivation-view diagnosis | The only V11 warm failed closed before any P3 measurement: its initial holder attestation saw the 1-GiB input while the reactivated holder saw three metadata entries and zero payload bytes. The failure output is bounded and V11 is retained unchanged. One disposable, supported-CLI read-only inspection is authorized to establish that the persisted allocation upper is intact before altering the remount path. | `FAIL_REPAIRING` (fixture qualification only) | Resolved V11 warm / PENDING read-only diagnosis in `TEST-REPORT.md` | Read V11 allocation tree, clean up exactly, then correct the remaining remount-provenance defect and create a new identity only after local regression passes. |
| `2026-07-30T10:34:00Z` | `P3/BG-PUBLISH-SMALL` V12 shared FIEMAP oracle repair / fresh closure | V11's retained mount receipts prove reactivation selected the exact persisted 1-GiB upper. The actual divergence was allocation classification: the publisher treated full FIEMAP coverage as data before `SEEK_DATA`; the independent oracle used `SEEK_DATA` alone, which reports the correct dense OverlayFS lower as all-hole. V12 centralizes the FIEMAP probe, retains independently ordered oracle traversal/reduction with bounded 256-KiB transfers and four readers, and closes a new root/volume/staging root with builder/consumer `:7896`/`:7897`. Formatter, oracle `1/1`, identity `2/2`, fixture parser `4/4`, and harness `24/24` pass; the ARM64 package build passes through Zig. V11 remains immutable and is never retried. | `PASS_LOCAL_REBUILD_PENDING` | `TEST-REPORT.md` resolved FIEMAP, package, and V12 closure receipts | Repackage the post-V12 sources, rebuild only the V12 gateway with the mandatory launcher, require empty inventories, then make one 800-second-bounded V12 cache warm. Continue to P3 only after the reactivated-holder oracle seal. |
| `2026-07-30T10:42:00Z` | `P3/BG-PUBLISH-SMALL` V12 endpoint collision correction | The first V12 launcher rebuild packaged normally but could not start because V10 legitimately owns `:7896` (PID `30071`). No V12 cache command, sandbox, or persistent write occurred. V12 is now closed to unbound `:7900`/`:7901`; its narrow authenticated endpoint allowlist, builder/consumer configs, source tests `2/2`, harness tests `24/24`, and fresh ARM64 package are synchronized. V10 is retained untouched. | `PASS_LOCAL_REBUILD_PENDING` | `TEST-REPORT.md` V12 endpoint failure and closure receipts | Start only the V12 builder at `:7900` through the mandatory launcher; require empty supported inventories, then issue one 800-second-bounded V12 cache warm. |
| `2026-07-30T10:44:00Z` | `P3/BG-PUBLISH-SMALL` V12 fresh builder preflight | The mandatory launcher rebuilt and started only V12 at `127.0.0.1:7900` (PID `45918`); supported manager inventory is empty and supported fleet resources returns an empty sandbox map. The rejected `list_resources` spelling occurred before the correct `resources` inventory and made no state change. | `IN_PROGRESS` | `TEST-REPORT.md` resolved V12 deployment/preflight receipt | Issue exactly one V12 administrative cache warm through the builder with the 800-second setup watchdog. It is outside P3 timing; start the V12 read-only consumer only after its reactivated-holder oracle seal. |
| `2026-07-30T10:50:00Z` | `P3/BG-PUBLISH-SMALL` V12 exact artifact-freshness repair | The post-gateway `cargo zigbuild` completed, but the package-wide freshness approximation falsely rejected the oracle because an unrelated scorecard binary was newer. The permanent guard now reads Cargo's per-artifact `.d` dependency manifest: focused fixture-cache tests pass `6/6`, retain the stale-listed-source rejection, and prove a newer unlisted source does not invalidate the oracle. V12 itself remains empty; no cache write or second warm occurred. | `IN_PROGRESS` | `TEST-REPORT.md` fresh-artifact and focused-regression receipts | Issue exactly one serialized V12 builder cache warm at `:7900` with the 800-second setup watchdog, then require reactivated holder/oracle agreement before P3. |
| `2026-07-30T10:51:00Z` | `P3/BG-PUBLISH-SMALL` V12 cache-warm semantic-count diagnosis | The one physical V12 warm performed layer-one work and failed closed before any P3 timing. All nonsemantic gates for the dense 4-GiB layer were correct, including exact affected bytes, logical bytes, roots, freshness, durability, and cleanup. The qualifier's `32,772 + 1` expected-entry arithmetic was wrong: a chunked dense file contributes `131,073` semantic records, making the observed full-tree count `163,845` exactly correct. V12 is retained immutable and not retried. | `FAIL_REPAIRING` (fixture-layer semantic expectation) | Resolved bounded V12 warm receipt and empty post-cleanup inventories in `TEST-REPORT.md` | Add a local regression for a chunked dense full-tree receipt; qualify each fixture layer against independent holder-oracle semantics; then close a fresh V13 root/volume/endpoints and warm only that generation. |
| `2026-07-30T11:02:00Z` | `P3/BG-PUBLISH-SMALL` V13 isolated builder deployment | The permanent fixture-layer repair is locally qualified: full-tree holder-oracle matcher `17/17`, oracle cross-check `1/1`, fixture/profile CLI `4/4`, host harness `25/25`. New V13 identity is root `s4-chain-v13`, named volume `eos-mpla-prepared-s4-phase-profile-v13`, builder/consumer `:7902`/`:7903`; ARM64 coordinator SHA-256 is `97b7af0f…825417`, oracle SHA-256 `d756ed47…b49f2fbe`. V12 is retained and not mounted. | `IN_PROGRESS` | `TEST-REPORT.md` local/package receipts | Rebuild only the V13 builder through the mandatory launcher, query only supported empty inventories, then permit one V13 warm under the 800-second setup watchdog. |
| `2026-07-30T11:04:00Z` | `P3/BG-PUBLISH-SMALL` V13 serialized cache warm | Mandatory V13 package rebuild is live at builder `:7902` (PID `51045`, daemon `e4e24f4f…51715151`, helper `05cb34a5…6b18a8e9`); supported manager and fleet resource inventories are empty. One administrative cache warm is authorized against V13 only, bounded by the user-approved 800-second setup watchdog. | `IN_PROGRESS` | `TEST-REPORT.md` deployment/preflight PENDING receipt | Await one compact cache seal. It must use independent holder-oracle qualification on every fixture layer before P3 consumer setup is allowed. |
| `2026-07-30T10:56:01Z` | `P3/BG-PUBLISH-SMALL` V13 sealed persistent fixture | The sole V13 cache warm sealed a real `9,668,919,296`-byte logical chain in `133,683 ms` (`129,932,087,351 ns` builder time). Every fixture layer passed holder-oracle qualification, including the chunked dense 4-GiB full-tree layer; the exact builder manager and resource inventories are empty afterwards. This administrative cost is excluded from P3 hot publication latency, although its 7.03-s/16.79-s dense semantic phases remain a separately measured setup concern. | `PASS` cache qualification; P3 timing pending | Sealed `PREPARED-FIXTURE.json`, bounded builder receipt, `TEST-REPORT.md`, empty supported inventories | Start a separate V13 read-only consumer at `:7903`, preflight its empty inventory, then take one formal publication-only run. |
| `2026-07-30T10:56:01Z` | `P3/BG-PUBLISH-SMALL` V13 consumer preflight | The mandated consumer rebuild started PID `54818` at `:7903`. An initial connection-refused observation raced its asynchronous startup; the subsequent supported manager and fleet-resource inventories are both empty. The sealed cache is mounted read-only, and no P3 resource or evidence root exists yet. | `IN_PROGRESS` | `TEST-REPORT.md` consumer deployment receipt; empty supported consumer inventories | Execute only fresh `mpla-booster-p3-v13-20260730T105601Z` against the fixed V13 consumer, then decide from its sealed matched samples whether sub-50-ms optimization remains necessary. |
| `2026-07-30T10:56:01Z` | `P3/BG-PUBLISH-SMALL` V13 staged-coordinator rejection | The fresh P3 runner sealed partial evidence and cleaned up before timing any candidate: its preparation command failed in `26.316 ms` because the staged coordinator's CLI accepts only `s4-chain-v9`, rejecting required `s4-chain-v13`. The V13 fixture is read-only and unchanged. This is stale staged-artifact provenance, not a P3 publication result or latency miss. | `FAIL_REPAIRING` (deployment provenance) | Retained `mpla-booster-p3-v13-20260730T105601Z` partial root and resolved report receipt | Read only the current host/staged coordinator identity and paths; add a fail-closed V13 artifact-profile preflight, rebuild/repackage only after it passes, then allocate a distinct fresh P3 run. |
| `2026-07-30T10:56:01Z` | `P3/BG-PUBLISH-SMALL` V13 parser provenance repair | Root cause is a duplicated `clap` profile literal: runtime/cache constants were V13 but `PublicationPreparationArgs` still allowed V9. A strengthened CLI regression failed first, then passes `5/5` after binding the parser to `PREPARED_FIXTURE_PROFILE`; it now accepts V13 into application validation and rejects V9. Fresh ARM64 coordinator SHA-256 `19617587…0abd88` contains only V13 profile literals. The mandatory launcher replaced only the read-only consumer (PID `58075`); supported consumer inventories are empty. | `IN_PROGRESS` | `TEST-REPORT.md` focused regression, ARM64 package, and consumer deployment receipts | Execute only fresh `mpla-booster-p3-v13-20260730T105900Z`; it is the first repaired run eligible for timed publication samples. |
| `2026-07-30T10:56:01Z` | `P3/BG-PUBLISH-SMALL` runner freshness false rejection | The first repaired P3 root sealed partial evidence before staging: the runner falsely declared unchanged `mpla-poc-oracle` stale because the coordinator parser source is newer. This is the same broad source-mtime provenance defect already repaired in the cache builder, not a new artifact or P3 behavior; cache and consumer remain unchanged. | `FAIL_REPAIRING` (runner artifact provenance) | Retained `mpla-booster-p3-v13-20260730T105900Z` partial root and resolved report receipt | Port the per-artifact Cargo `.d` closure rule to the runner with a focused unrelated-newer-source regression; then rebuild/repackage and allocate a distinct P3 root. |

Do not begin by rerunning the 1.72 GiB legacy diagnostic. It already answered a
different question and will not close a Booster scorecard gate.

## 16. Append-only execution ledger

| Timestamp | Scope | Result | Status | Evidence | Next action |
|---|---|---|---|---|---|
| `2026-07-30T11:06:52Z` | `P3/BG-PUBLISH-SMALL` runner artifact-provenance repair | The runner copied the cache builder's former broad package-mtime approximation, causing P3 to falsely reject the unchanged oracle when the coordinator-only CLI parser changed. It now parses Cargo's per-artifact `.d` dependency manifest and checks coordinator and oracle independently; a stale listed source still fails closed, while a newer unlisted source does not invalidate either binary. The paired host-only builder/runner regression set passes `26/26` in `0.503 s`. Only the host runner changed: the already cross-built coordinator (`19617587…0abd88`), oracle (`d756ed47…b49f2fbe`), V13 cache, and consumer remain unchanged. | `PASS_LOCAL_REBUILD_NOT_REQUIRED` | Resolved `TEST-REPORT.md` provenance entries; no Docker state or new evidence root | Query supported empty consumer inventories, then run exactly one distinct V13 P3 publication-only measurement targeting the sub-50-ms goal. |
| `2026-07-30T11:18:00Z` | `P3/BG-PUBLISH-SMALL` staged coordinator dispatch repair | The V13 P3 partial root proved that the runner SHA-staged the current coordinator but then invoked a retired V9 executable baked into the immutable cache. The runner now dispatches only `/workspace/_campaign-tools/mpla-speed-poc-v1`; the coordinator resolves its sibling oracle from that same exact allowlisted root. Runner regression passes `21/21`; targeted root-allowlist tests pass `3/3`; ARM64 artifacts were rebuilt and the required V13 consumer launcher reload is live with supported empty inventories. The sealed V13 fixture remains unmodified. | `PASS_LOCAL_DEPLOYED` | Resolved `TEST-REPORT.md` staged-dispatch, formatting, ARM64, and launcher entries; invalid P3 root `mpla-booster-p3-v13-20260730T110800Z` retained | Run exactly one fresh V13 `publication` case under a new evidence root. Promote timing only if all correctness/durability/allocation gates seal; target candidate median <50 ms. |
| `2026-07-30T11:23:00Z` | `P3/BG-PUBLISH-SMALL` staged qualification-profile deployment | The physical V13 staged dispatch entered the daemon in `33.192 ms` but was assigned the capless standard profile because the frozen command allowlist omitted the exact new staged coordinator root. The permanent, narrowly scoped repair admits only `/workspace/_campaign-tools/mpla-speed-poc-v1`, retaining the existing fixed preparation/scorecard grammar; staged authority use and sibling paths remain standard. The profile-derived V13 regression passes `3/3`, Rustfmt is clean, and the required V13 consumer rebuild is live with empty supported inventories. The fixture and prior partial evidence remain immutable. | `PASS_LOCAL_DEPLOYED` | Resolved `TEST-REPORT.md` staged-profile regression and consumer-reload receipt; invalid P3 root `mpla-booster-p3-v13-20260730T111600Z` retained | Run exactly one fresh V13 `publication` case from a new evidence root. The first required outcome is a full capability preflight pass; promote only sealed candidate timing and target median under `50 ms`. |
| `2026-07-30T11:31:36Z` | `P3/BG-PUBLISH-SMALL` incremental semantic-reply repair | The next V13 root passed its capability, immutable-payload, roots, allocation, freshness, and durability gates, but correctly stopped before timing promotion: service-owned incremental scope contained `32,831` total records while the scorecard incorrectly expected “prior + ten paths,” and the RPC response had dropped the internally computed affected-record/stream counters. The durable outcome, replay result, and public reply now preserve that counter; the scorecard instead requires total-tree growth plus the returned counter at least equal to the ten affected paths, matching stream bytes, and all existing independent oracle/exact-payload gates. Focused reply tests pass `3/3`; focused scorecard regressions pass `2/2`; fresh ARM64 coordinator/oracle build and required V13 consumer rebuild are live. Supported consumer manager and resource inventories are empty. | `PASS_LOCAL_DEPLOYED` | Partial root `mpla-booster-p3-v13-20260730T112100Z` retained; append-only `TEST-REPORT.md`; deployed daemon package SHA-256 `8116dee95f08c3ecc735b9f9859ba6115fcaab94fcfe389b0400a5bb7173768b` | Run exactly one new V13 `publication` root. Promote timing only if the full candidate matrix, independent oracle, and cleanup all seal; target candidate median `<50 ms`. |
| `2026-07-30T11:36:27Z` | `P3/BG-PUBLISH-SMALL` candidate-side independent-oracle path repair | The preceding V13 partial root proved the runner atomically staged `mpla-poc-oracle`; the failure was not a missing artifact. The coordinator resolved `/workspace/_campaign-tools/mpla-poc-oracle` before activation and reused it after activation replaced `/workspace` with the candidate MPLA workspace. A narrow candidate-only resolver now selects the candidate-visible read-only shared-base path `/eos/layer-stack/base/B000001-base/_campaign-tools/mpla-poc-oracle`; the coordinator preflight remains dynamically rooted in its staged `/workspace` path. The red/green regression establishes that contract; the scoped ARM64 coordinator/oracle rebuild passes in `35.76 s`. No runtime daemon source changed, so the live V13 consumer remains the required rebuilt deployment; supported inventories are empty. | `PASS_LOCAL_DEPLOYED` | Prior partial root `mpla-booster-p3-v13-20260730T113136Z` retained; append-only `TEST-REPORT.md`; sealed V13 fixture unmodified | Run exactly one distinct V13 `publication` root. Promote timing only after full independent-oracle, correctness/durability, matrix, and cleanup sealing; candidate median target `<50 ms`. |
| `2026-07-30T12:03:10Z` | `P3/BG-PUBLISH-SMALL` sub-50-ms durable incremental publication retry | The physical candidate now removes only a redundant incremental filesystem-wide flush and duplicate locator directory flush, pre-creates the manifest parent before the existing root barrier, and stages small deltas in a bounded in-memory format with the existing verified spill fallback. Full semantic regression (`10/10`), locator recovery (`8/8`), large spill (`1/1`), and exact 1-MiB/ten-file delta (`1/1`) pass. The mandatory V13 consumer rebuild is live at `127.0.0.1:7903` (PID `76195`); supported manager and observability inventories are empty. | `IN_PROGRESS` | `TEST-REPORT.md` append-only local regression/rebuild receipts; fresh evidence root `mpla-booster-p3-v13-20260730T120310Z` is absent before allocation | Execute exactly one fresh V13 `publication` matrix. Retain and diagnose any result at or above `50 ms`; promote timing only after all independent-oracle, durability, no-copy, allocation, and exact cleanup gates seal. |
| `2026-07-30T12:03:11Z` | `P3/BG-PUBLISH-SMALL` current-artifact provenance guard | The newly allocated root `mpla-booster-p3-v13-20260730T120310Z` sealed partial evidence before candidate allocation: the runner correctly detected that the staged ARM64 coordinator predates the semantic source changes. This preserves the fixture, consumer, and latency evidence; no sample is eligible. | `FAIL_REPAIRING` (artifact freshness) | Partial root retained; runner exit `1` after `0.739 s` | Cross-build only `mpla-speed-poc-v1` and `mpla-poc-oracle` for ARM64, rerun the runner's built-in freshness preflight, then use a new evidence root. |
| `2026-07-30T12:05:22Z` | `P3/BG-PUBLISH-SMALL` optimized-artifact deployment/preflight | The required current ARM64 coordinator/oracle build completed in `71 s` with coordinator SHA-256 `d1ceff821937a58805b2a9a83205eca25b7641e4e25bbbebcfd65cfa3f00ed2a` and oracle SHA-256 `d756ed47288b40d9a8626ba66bef4482d8130fc156fded1a403e8103b49f2fbe`. The V13 consumer remains the mandatory post-runtime-change deployment at `:7903`; supported manager and observability inventories are both empty. | `IN_PROGRESS` | Append-only build/preflight receipts; fresh root `mpla-booster-p3-v13-20260730T120522Z` was verified absent | Run exactly one V13 `publication` matrix from this new root, retaining all samples and promoting timing only after full seal. |
| `2026-07-30T12:06:52Z` | `P3/BG-PUBLISH-SMALL` durable optimized physical measurement | The complete publication-only V13 matrix sealed and its manifest verified (`18689ca954fc3199bd9767dc9359d203f904dc40999d09c1554c621d406c9b0a`). All per-candidate fixture, durability, no-copy, allocation, and independent-oracle predicates pass; exact cleanup returned both supported inventories empty. The measured candidate samples are `75.098125`, `81.647833`, `79.828959`, `123.639583`, and `148.897000 ms`; matched median `79.828959 ms`, max `148.897000 ms`, control median `11,433.845089 ms`, exact matched ratio `11,433,845,089 / 79,828,959 = 143.228…x`. | `FAIL_REPAIRING` (absolute latency ceiling) | Sealed root `mpla-booster-p3-v13-20260730T120522Z`; `BG-PUBLISH-SMALL` predicate false solely because the candidate is above `50 ms` target and the required `100 ms` max ceiling | Preserve all samples. Audit the 36–38-ms storage sequence, 27–33-ms semantic build/adoption, and 6–9-ms ref commit for a new safe dependency/barrier optimization before any retry. |
| `2026-07-30T12:23:00Z` | `P3/BG-PUBLISH-SMALL` bounded daemon immutable-object cache | Added a fixed 1-MiB, digest-keyed LRU of already digest-verified immutable semantic object bytes to the long-lived gateway process. Mutable staged objects retain precedence; misses retain the normal validated on-disk path; the fixed cache is included in the 8-MiB semantic managed-memory bound. The isolated LRU and normal one-MiB/ten-file incremental equivalence regression pass. Required runtime rebuild completed; V13 consumer was replaced on `:7903` and supported manager/observability inventories are empty. Fresh ARM64 coordinator SHA-256 `97b4a5ba520ffd2ae803c1783ab2ce9187bd8120abddb796d63e4c908cc71119`; oracle SHA-256 remains `d756ed47288b40d9a8626ba66bef4482d8130fc156fded1a403e8103b49f2fbe`. | `IN_PROGRESS` | Append-only `TEST-REPORT.md`; V13 consumer PID `82466`; no new evidence root yet | Allocate one unique publication-only root and execute the sealed matrix. It must use ordinary public lifecycles only—no cache prewarm outside the timed contract—and must retain all correctness, durability, no-copy, oracle, and cleanup gates. |
| `2026-07-30T12:25:30Z` | `P3/BG-PUBLISH-SMALL` daemon-cache physical measurement | The distinct normal-lifecycle root `mpla-booster-p3-v13-20260730T122114Z` sealed; its manifest verifies as `0f9c7c837ffa3ada5e390478aedcf17b16aab3b096a1e1c53d871b4d5d319d1a`. All publication correctness, durability, fixture/control, no-copy, independent-oracle, resource, and exact cleanup predicates pass. The cache acts only after the first ordinary request: prior-node reads are `195,024`, `0`, and `0` across the three matched pairs. Matched candidate samples are `81.343167`, `62.171208`, `68.736000 ms`; matched median is `68.736000 ms`, a `13.9%` improvement over the preceding `79.828959 ms`, and the exact matched ratio is `167.33...x`. | `FAIL_REPAIRING` (absolute latency ceiling) | Sealed root `mpla-booster-p3-v13-20260730T122114Z`; full candidate sequence `81.343167`, `62.171208`, `68.736000`, `125.113792`, `141.026208 ms` | Preserve this root. No target-compliant retry is justified until a dependency audit identifies a safe permanent reduction in the warm critical path: ~`30.061 ms` storage, `19.873 ms` semantic/adoption, `8.413 ms` ref commit, and `4.117 ms` pre-storage for the 62-ms matched pair. |
| `2026-07-30T12:56:00Z` | `P3/BG-PUBLISH-SMALL` bounded immutable pack-catalog cache | The only new dependency reduction caches a successfully validated immutable source pack catalog in a 768-KiB identity-keyed LRU, offset by a matching reduction in the existing page-cache budget. Mutable staged state is never cached; changed catalog metadata falls back to normal validation. Focused cache and exact 1-MiB/ten-file regressions pass. The required gateway package rebuild (`23e2291b…db7191b`) is deployed to the V13 consumer, and current ARM64 coordinator/oracle hashes are `2b8f7aa4…e4d317` / `d756ed47…f2fbe`; supported consumer inventories are empty. | `IN_PROGRESS` | Append-only `TEST-REPORT.md`; consumer PID `88855`; root `mpla-booster-p3-v13-20260730T203800Z` verified absent | Run exactly one fresh normal-lifecycle `publication` matrix. Preserve all samples; promote only if every correctness, durability, no-copy, oracle, resource, cleanup, and absolute-latency predicate seals. |
| `2026-07-30T12:58:00Z` | `P3/BG-PUBLISH-SMALL` immutable pack-catalog physical measurement | The unique normal-lifecycle V13 P3 root `mpla-booster-p3-v13-20260730T203800Z` sealed and its manifest verifies as `27bb0bbc504985553ccb5e32ebef653553697aa8e0d1b4ea4a223acbea7a0100`. All P3 candidate fixture, durability, independent-oracle, no-copy, allocation/resource, and exact-cleanup predicates pass; supported inventories are empty after the run. Matched samples are `77.710292`, `71.737792`, and `83.221666 ms`, with matched median `77.710292 ms`; all retained candidates are `77.710292`, `71.737792`, `83.221666`, `132.242042`, and `140.777791 ms`. The cache reduced warmed source-store lookup (about `3.8–4.2 ms` to `0.9–1.3 ms`) but no longer controls the durable critical path. | `FAIL_REPAIRING` (absolute latency ceiling) | Sealed root and resolved `TEST-REPORT.md`; fixture construction is outside the timer (`483.850708 ms`) | Before any new root, apply and locally prove only a strict, crash-safe dependency reduction: remove the just-written pack's redundant self-validation scan while retaining sync/install/catalog and overlap independent projection-recipe persistence with locator installation before the ref journal remains last. |
| `2026-07-30T12:51:22Z` | `P3/BG-PUBLISH-SMALL` post-dependency-reduction deployment | The incremental pack writer now returns its already verified writer-owned metadata rather than rescanning the pack it just wrote; normal reopen validation, checksum pass, syncs, immutable no-replace install, and catalog publication remain intact. The independently derived projection recipe is persisted concurrently with locator CAS installation, while the paired ref journal remains last. Focused writer and 1-MiB/ten-file semantic regressions passed; the required gateway rebuild and V13 consumer restart are live at `127.0.0.1:7903`, with supported manager and observability inventories empty. | `IN_PROGRESS` | Resolved append-only `TEST-REPORT.md` focused-regression/rebuild/preflight receipts; ARM64 coordinator/oracle hashes remain `2b8f7aa4…e4d317` / `d756ed47…f2fbe`; fresh root `mpla-booster-p3-v14-20260730T125141Z` verified absent | Run exactly one fresh normal-lifecycle `publication` matrix. Retain every candidate and promote only on full fixture, durability, no-copy, independent-oracle, resource, cleanup, and `<50 ms` latency compliance. |
| `2026-07-30T12:51:41Z` | `P3/BG-PUBLISH-SMALL` V14 dependency-reduction physical measurement | The fresh normal-lifecycle V13 matrix sealed and independently verified (`bf780cec04481bca74a6c62850289bab11b4cd90884ecdaa1425a247afeaab97`). Fixture preparation was a separately receipted `531.485542 ms`; every P3 fixture/control, independent-oracle, no-copy, durability, resource, and exact-cleanup predicate passed, and both supported final inventories are empty. The formal candidate denominator is `68.506125 ms`; all-candidate median/max are `80.256083` / `142.715250 ms`. Matched control median is `11,490.409756 ms`, yielding `11,490,409,756 / 68,506,125 = 167.726...x`. | `FAIL_REPAIRING` (absolute `<50 ms` latency target) | Sealed `mpla-booster-p3-v14-20260730T125141Z`; `summary.json`, manifest verification, append-only test ledger | Do not repeat the matrix. Prove one receipt-preserving critical-path reduction first: the current storage transaction serializes `~3.6–3.8 ms` cleanup/cgroup release before `~8.4–9.5 ms` stable double inventory and repeats `~2.4 ms` mount-plan preparation per quiesce/unmount action. |
| `2026-07-30T13:06:29Z` | `P3/BG-PUBLISH-SMALL` helper-only overlap and exact mount-authority repair | After strict unmount, the storage sequence proves that the workload cgroup contains exactly its authenticated helper before the helper performs target-only cleanup concurrently with the independent stable allocation inventory; it still proves the cgroup empty after helper exit and before publishing a checkpoint. The sequence now loads the immutable, exact mount-receipt attestation once only after exact binding equality, while every quiesce/unmount/cleanup action still derives fresh mount-plan and mount-table evidence, validates live state, and commits its own durable receipt. Focused cgroup, mount-authority, and caller-boundary tests pass (`1/1`, `2/2`, `1/1`). | `PASS_LOCAL_REBUILD_PENDING` | `TEST-REPORT.md` resolved local regressions; no new physical evidence or sample | Rebuild via the mandatory launcher, reload the isolated V13 consumer at `:7903`, require supported empty inventories, then run exactly one fresh normal-lifecycle publication matrix under a new evidence root. |
| `2026-07-30T13:10:41Z` | `P3/BG-PUBLISH-SMALL` V15 helper-overlap physical measurement | The generic and isolated V13 consumer rebuilds are complete; V13 at `:7903` has empty supported manager/resource inventories. Fresh coordinator/oracle artifacts have SHA-256 `623ceb8b…c6e62` / `d756ed47…f2fbe` and current dependency mtimes. A unique absent root `mpla-booster-p3-v15-20260730T131041Z` is authorized only for the ordinary `publication` case. | `IN_PROGRESS` | `TEST-REPORT.md` PENDING V15 entry; sealed V14 root remains retained | Historical action at the time: execute the full P3 publication matrix under the runner's then-configured 600-second case ceiling. This is retained as attempt history and is superseded by the current phase-local budget policy. |
| `2026-07-30T13:12:10Z` | `P3/BG-PUBLISH-SMALL` V15 helper-overlap physical result | The normal-lifecycle publication matrix sealed and manifest verified (`71cbf9b372302dee170ae963c54a0886adbb720dcd10685dba9c781745ad3a5f`). Fixture preparation stayed outside the timer (`550.695042 ms`); every publication fixture/control, durability, independent-oracle, no-copy, resource, and exact-cleanup predicate passed. Matched candidates were `74.305167`, `60.385209`, and `64.270791 ms`; all candidates were `74.305167`, `60.385209`, `64.270791`, `122.935500`, and `139.016291 ms`; matched control median was `11,495.687714 ms`, ratio `178.867...x`. | `FAIL_REPAIRING` (absolute `<50 ms` latency target) | Sealed V15 root, publication-local gates, and final empty supported inventories | Preserve V15. Do not repeat the matrix. Audit the now-dominant `20.862041`/`22.115625-ms` durable stationary-adoption phase for one proven dependency reduction; retain all current receipt, recovery, and commit-last semantics. |
| `2026-07-30T13:27:46Z` | `P3/BG-PUBLISH-SMALL` accepted PoC publication baseline and full-scorecard transition | The user accepted the sealed V15 matched publication median of `64.270791 ms` as sufficient for this PoC. The formal matrix minimum remains `<=100 ms` per eligible candidate and `>=100x` matched speedup; the superseded `<50 ms` stretch target is not a reason to discard V15. V15 remains publication-local evidence only and does not establish the other six formal gates or a whole-campaign verdict. | `PASS_LOCAL_GATE_PENDING_FULL_CAMPAIGN` | V15 manifest `71cbf9b372302dee170ae963c54a0886adbb720dcd10685dba9c781745ad3a5f`; no sealed evidence modified | Rebuild the required V13 gateway, verify the exact supported-CLI inventories and artifact freshness, then execute the remaining focused qualification cases with fresh evidence. Re-run publication only if the final full campaign invalidates it by source or environment change. |
| `2026-07-30T13:31:00Z` | Final focused campaign, lifecycle diagnostic failure | The required V13 gateway rebuild and a clean supported-CLI preflight completed, then the fresh full root `mpla-booster-final-20260730T132800Z` sealed partial evidence. Qualification completed; lifecycle stopped after `119.315399262 s` inside the coordinator with `materialize hidden candidate failed: native reconstruction failed: invalid native materialization: reconstructed carrier summary differs from verified carrier`. The launcher cleanup receipts prove both supported manager and observability inventories empty. | `FAIL_REPAIRING` | Retained sealed partial root `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-booster-final-20260730T132800Z`; append-only `TEST-REPORT.md` resolution | Trace the native reconstruction and post-sync verification summaries, add a focused regression, then apply the smallest integrity-preserving repair and rerun only lifecycle. |
| `2026-07-30T13:50:00Z` | Native-carrier post-sync telemetry repair | The fresh lifecycle diagnostic proved candidate digest `e84c…a400`, entry count `4296`, and logical bytes `912350100` match exactly. Only `stat.st_blocks*512` allocation changed from `926887936` to `926846976` after durability synchronization. A portable red/green regression confirms that allocation is telemetry rather than carrier identity; reconstruction and selection validation now compare only digest/count/logical bytes, while the manifest records the post-sync verified allocation value. Linux fixture assertions no longer make a false exact-allocation claim. | `PASS_LOCAL_DEPLOYMENT_PENDING` | Live diagnostic root `mpla-booster-lifecycle-diagnostic-20260730T134000Z`; append-only test ledger; focused library regression | Rebuild the required V13 gateway and ARM64 coordinator/oracle closure, then run only fresh lifecycle evidence before returning to the remaining scorecard matrix. |
| `2026-07-30T15:28:00Z` | `F0-COLD` sparse fixture-cache construction | Replaced V13's eight dense lifecycle publications and repeated accumulated-tree scans with closed profile `s4-chain-sparse-v1`: eight exact hole-only content-addressed allocations, bounded per-receipt qualification, one final exact inventory/extent/manifest validation, and one filesystem sync. A genuine unsealed recovery completed in `1.256996668 s` service and `1.403286 s` cache-command outer versus V13 `129.932 s` service / `133.683 s` wall (`95.27×` outer improvement). Docker setup was separately `0.871039292 s`, staging `0.040230666 s`, and launcher start through pre-cleanup `2.314714375 s`. | `PASS` | Logical fixture `8,589,934,592` bytes; exact allocations `8`; allocated payload bytes `0`; payload bytes read/copied `0`; exact known recovery roots only; sealed manifest; Docker Desktop fixed macOS-hosted 4-vCPU/4-GiB envelope, Ubuntu 24.04 Linux/arm64 pinned image | Preserve builder-only mutation authority and corrupt-sealed fail-closed behavior; use only P0-WARM for normal runs. |
| `2026-07-30T15:28:20Z` | `P0-WARM` repeat read-only attachment | Two independent normal consumer preparations attached the same sealed sparse cache. Attachment service was `23.010084 ms` and `19.368500 ms`; complete in-service preparation was `529.899292 ms` and `490.085667 ms`; harness outer was `1.135584208 s` and `1.113340875 s`. Both receipts prove operation `attach_mpla_prepared_fixture`, exact eight cached allocations, branches depth 1/5/8, and zero copied payload bytes. | `PASS` | Runs `mpla-warm-sparse-v1-a` and `mpla-warm-sparse-v1-b`; evidence roots `/tmp/mpla-warm-attach-20260730-a` and `/tmp/mpla-warm-attach-20260730-b`; consumer volume is read-only | Keep `<50 ms` as attachment-service acceptance and `<1.0 s` as complete preparation acceptance; never apply either target to genuine cold construction. |
| `2026-07-31T07:26:50Z` | `F0-COLD` accepted Final43-v3 recovery construction | A fresh genuine recovery of `s4-chain-sparse-v1` completed in `1.102406542 s` builder service and `1.228642917 s` cache-command outer. Orchestration was `0.126236375 s`; Docker setup `2.198345375 s`; artifact staging `0.043895500 s`; launcher start through pre-cleanup `3.471067 s`; whole process wall `3.99 s`. The builder created the exact eight content-addressed sparse allocations representing `8,589,934,592` logical bytes, with zero allocated, read, or copied payload bytes. | `PASS` | Receipt `mpla-final43-f0-v3-20260731t072650z@9490df6403472941b81d00bdd21dc00ebf4df88e42bfb6f58235d0b320f91a5c`; `108.81×` outer improvement from the `133.683 s` V13 wall baseline | This supersedes the earlier recovery timing for terminal sealing. Keep the builder mutation authority unavailable to warm consumers and retain corrupt-sealed fail-closed behavior. |
| `2026-08-01T08:56:47Z` | `P8` terminal Final73 sealing | The single sealing process authenticated Final43-v3 plus the eight exact P0–P7 roots, preserved Final50 publication as an honest required-gate failure, and completed in `396,731,209 ns` receipt elapsed (`0.57 s` process wall) under P8's independent fixed `30 s` cap. Independent verification rehashed all 14 manifest entries and terminal supported inventories were exact empty. | `PASS` | Root `mpla-final73-p8-20260801t085647z`; manifest `837578247484c38c95285b12c0e7710b66546e643c3132f3368aa3c87891638f` | Terminal decision: `POC_CORRECTNESS=PASS`, `AG_SQUASH=PASS`, `AG_STREAM=PASS`, `POC_100X=NOT_SUPPORTED`, `POC_500X=NOT_SUPPORTED`. |

### 13.5 Terminal focused execution checklist

This is the active task list for the freshly sealed decision. It supersedes
legacy grouped-run handoffs while preserving their attempt history. Execute
one row at a time in the order shown. Every row owns its declared phase-local
cap; there is no 480-second or 600-second campaign deadline, shared allowance,
deadline carry-over, or time borrowing.

| Order | Phase / runner | Phase-local cap | Sealed result |
|---:|---|---:|---|
| 0 | F0-COLD / `build-mpla-publication-fixture-cache` | `30 s` | `PASS` — genuine recovery outer `1.228642917 s`; service `1.102406542 s`; zero copied bytes |
| 1 | P0-WARM / `mpla_qualification_scorecard` attachment | `5 s` | `PASS` — service `24.825208 ms`; complete preparation `374.467417 ms`; zero copied bytes |
| 2 | P0 / `mpla_qualification_scorecard` | `60 s` | `PASS` — `2.120485208 s` |
| 3 | P1 / `mpla_activation_scorecard` | fixed `120 s` | `PASS` — `85.129972292 s`; both activation gates true |
| 4 | P2 / `mpla_fork_scorecard` | `60 s` | `PASS` — `52.723843000 s` |
| 5 | P3 / `mpla_rollback_scorecard` | `60 s` | `PASS` — `51.757623833 s` |
| 6 | P4 / `mpla_publication_scorecard` | `70 s` | `FAIL` — `22.881794000 s`; candidate absolute ceiling passed, matched ratio only `0.626872660×` |
| 7 | P5 / `mpla_squash_scorecard` | `60 s` | `PASS` — `29.591311167 s` |
| 8 | P6 / `mpla_stream_scorecard` | `40 s` | `PASS` — `8.363238417 s`; 1-GiB stream `994.910 ms` |
| 9 | P7 / `mpla_hv07_scorecard` | `120 s` | `PASS` — `21.349401583 s`; `46/46` fault points |
| 10 | P8 / `mpla_sealing_scorecard` | fixed `30 s` | `PASS` — `396,731,209 ns`; consumes only the eight exact sealed P0–P7 roots |

The rows were executed in this order with no parallel physical work. Each row
used only its declared cap; the retired grouped campaign limits were not used.
Final73 is terminal and did not rerun any sealed predecessor phase.
