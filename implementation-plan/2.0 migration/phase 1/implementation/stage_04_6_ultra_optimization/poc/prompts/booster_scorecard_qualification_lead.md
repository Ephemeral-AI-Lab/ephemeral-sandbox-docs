/goal Execute the formal MPLA Booster scorecard end to end. Run the exact test-matrix campaign, fix correctness and harness bugs, optimize any gate that misses its minimum, and produce a fresh sealed evidence-backed 100x/500x decision. Continue autonomously until the objective is achieved or a genuinely external hard blocker is proven.

# MPLA Booster scorecard qualification lead

You are the persistent implementation, test, debugging, and performance lead
for the formal Stage 04.6 MPLA Booster scorecard. Do not stop after planning,
compiling, diagnosing a failure, or producing a partial benchmark. Own the full
loop:

1. prepare the exact qualified environment;
2. make the public lifecycle surface and focused runner work;
3. execute every formal scorecard gate with matched controls;
4. repair product, harness, and environment defects;
5. optimize gates that miss their required minimum;
6. rerun only invalidated or failed focused cases;
7. run one final focused qualification campaign;
8. seal and independently verify the evidence;
9. publish the exact formal verdict.

Use your best technical judgment. Within the existing repository, Docker,
filesystem, and process permissions, you are authorized to make normal
in-scope decisions, edit the implementation and tests, rebuild binaries, start
and operate the supported gateway, create run-scoped resources, perform
run-scoped cleanup, and iterate on performance. Do not pause to ask the user to
approve routine, reversible, or clearly in-scope work.

Do not bypass a security boundary, destroy unrelated state, rewrite sealed
evidence, or expand the mission into an unrelated architectural rewrite. If a
step truly requires new external authority or an unavailable external
dependency, exhaust safe alternatives, preserve precise evidence, continue
every other unblocked workstream, and ask one narrow question only when no
meaningful progress remains. Never sit idle waiting for authorization that the
current scope and permissions already provide.

There is no blocker-resolution hour limit. Continue while there is a concrete
diagnostic, repair, optimization, or verification action available. Each
focused phase's own test-matrix liveness cap remains a validity requirement;
there is no aggregate campaign ceiling and no deadline carry-over between
phases. Phase caps are not limits on how long you may spend fixing the system.

## Read completely before acting

Read these in order:

1. `/Users/yifanxu/.codex/attachments/86aaffbe-5c98-4377-8595-783cc954fdf0/goal-objective.md`
2. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/AGENTS.md`
3. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/CLAUDE.md`
4. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/docs/maintainer-architecture.md`
5. The mandatory Codex skill
   `/Users/yifanxu/.codex/skills/eos-sandbox-e2e-test-rules/SKILL.md`
6. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/requirements_and_prohibitions.md`
7. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/test_matrix.md`
8. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/baseline-experiment/README.md`
9. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/booster_scorecard_execution_spec.md`
10. The current implementation plan, progress tracker, relevant prior prompts,
    and only the sealed evidence roots referenced by the execution spec.

Treat `test_matrix.md` as the formal contract and
`booster_scorecard_execution_spec.md` as the working handoff and progress
tracker. If they conflict, obey the matrix and record the discrepancy.

## Start from evidence, not assumptions

Before editing or testing:

- inspect both dirty worktrees;
- capture branch, commit, tree, porcelain status, diff identity, config hashes,
  and relevant binary hashes;
- preserve every pre-existing modification and untracked file;
- do not reset, clean, discard, or overwrite user work;
- inspect current processes, Docker state, gateway port, supported CLI
  inventories, disk capacity, and prior exact-run leftovers;
- allocate a unique UTC run ID and a fresh evidence root that does not already
  exist;
- update the embedded tracker in
  `booster_scorecard_execution_spec.md` before physical execution.

The previously sealed `760.228406789519x` matched publication result is valuable
calibration, not proof that the entire Booster scorecard passed. Verify its
manifest before citing it, never alter its evidence root, and keep
`BG-PUBLISH-SMALL` formally `UNKNOWN` until exact HV-01 conformance is proven.

The prior 1.72 GiB lifecycle campaign is diagnostic only. Do not rerun it as
the Booster campaign and do not use its wrong fixture parent, legacy mode,
unmatched timings, 4 KiB publication, or 64 MiB stream as formal gate evidence.

## Exact environment requirements

These are mandatory:

- Do not use tmpfs or ramfs.
- Use persistent ext4 backing for the measured fixture/workspace inside the
  Docker environment.
- Use a persistent host-bound evidence path.
- Enable `CAP_SYS_ADMIN` for the dedicated authenticated lifecycle/storage
  helper and qualified benchmark coordinator. It is required for real
  OverlayFS mount and unmount.
- Verify capability bit 21 in effective, permitted, and bounding sets from
  inside the measured process.
- Exercise and record a real OverlayFS mount and unmount.
- Keep ordinary untrusted workloads and their descendants without broad
  `CAP_SYS_ADMIN`.
- Use the pinned Ubuntu image digest from the execution spec.
- Keep Docker Desktop at the frozen `4 vCPU / 4 GiB` envelope.
- Keep the fixture/chain under the matrix limit.
- Fail preflight rather than silently weakening or changing any condition.

The only exact R0 source is:

`/Users/yifanxu/Ephemeral-AI-Lab/experiment/materialization-benchmark-20260727/corpus/console-release`

It must resolve to:

- `912,350,100` logical bytes
- `3,602` files
- approximately `870.08 MiB`

Reject its approximately 1.72 GiB parent directory.

Rebuild the gateway as required by repository policy:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
export PATH="$PWD/bin:$PATH"
env SANDBOX_GATEWAY_CONFIG_YAML="$PWD/config/mpla-poc-m3.yml" \
  bin/start-sandbox-docker-gateway --rebuild-binary
```

Use only these supported CLIs for qualifying manual lifecycle operations:

- `sandbox-manager-cli`
- `sandbox-runtime-cli`
- `sandbox-observability-cli`

Do not substitute direct Docker lifecycle commands, an ad hoc privileged
container, mocks, or host-only timings for the public live Docker path.

## Use subagents deliberately

You are explicitly encouraged to use subagents when they speed up research,
codebase exploration, evidence review, profiling, or troubleshooting.

Good parallel assignments include:

- map the public activation/fork/rollback/publish/squash call paths;
- audit the heavy harness for hard-coded run, lease, branch, fixture, config,
  and evidence identities;
- compare each test-matrix gate with existing test coverage;
- inspect a failed case's scoped logs, events, traces, and resource evidence;
- profile a slow code path and rank optimization hypotheses;
- independently verify candidate/control comparability and arithmetic;
- review security, capability, mount, cleanup, and no-hidden-copy evidence.

Give each subagent a concrete bounded question or exclusive file ownership.
Tell code-editing agents they are not alone in the worktree, must preserve
others' changes, and must not revert unrelated work. Ask them to return concise
evidence, file/line references, commands, and a recommended next action.

The lead owns integration, decisions, the tracker, and final evidence. Do not
allow multiple agents to run competing heavy Docker campaigns, mutate the same
evidence root, share one execution lease, or edit overlapping files
concurrently. Parallelize research and isolated implementation; serialize
physical measurements that would contend for Docker, CPU, memory, storage, a
gateway, or a lease.

Reuse a knowledgeable subagent for follow-up questions instead of repeatedly
starting context-free investigations. Independently review all proposed code
changes before integration.

## Required scorecard

Execute the exact matrix contracts for:

- `BG-ACTIVATE-EXACT`
- `BG-ACTIVATE-SAME`
- `BG-FORK`
- `BG-ROLLBACK`
- `BG-PUBLISH-SMALL`
- `AG-SQUASH`
- `AG-STREAM`

All five Booster gates require matched candidate/control evidence. Historical
baselines are context only and cannot replace a matched control arm.

The minimum aggregate condition is:

- every one of the five Booster gates has matched speedup `>=100x`;
- every candidate sample satisfies its gate's absolute ceiling;
- every required correctness, durability, isolation, ownership, security,
  space, memory, reconciliation, and cleanup check passes.

The preferred condition is the exact `500x` scorecard described by the matrix.
Report both the required and preferred decisions honestly.

For the usual three measured heavy samples, report raw values, median, and max.
Do not invent p95 for `n=3`. Preserve exact numerators and denominators so the
speedup can be independently recomputed.

## Debug-and-repair loop

For every failure:

1. Preserve the failed attempt and update the append-only attempt ledger.
2. Determine whether the defect is product behavior, public API choreography,
   benchmark harness, fixture identity, matched-arm comparability, Docker
   environment, resource contention, build contention, timeout/polling, or
   evidence interpretation.
3. Read the smallest relevant artifact set first: summary, failed case stdout,
   lifecycle/runtime logs, then scoped events/traces; use audit SQLite only when
   JSONL is insufficient.
4. Establish a root-cause hypothesis supported by evidence.
5. Add or adjust the smallest focused regression coverage.
6. Implement the smallest correct fix without weakening security, correctness,
   the resource envelope, or the measured workload.
7. Rebuild through the supported path.
8. Rerun only the failed or invalidated focused case.
9. Update the tracker with the result and next action.

Do not repeatedly rerun a failure without changing a hypothesis, input, or
diagnostic. Do not rerun passing heavy cases merely because a later case failed.
Run one final full focused proof only after all focused failures are resolved.

Before every test command, append the required `Command`, `Good`, `Defect`, and
`Fix` entry to the repository's E2E `TEST-REPORT.md`. Complete that entry when
the command finishes. Keep the report append-only.

## Performance optimization loop

If any required absolute ceiling or `100x` matched-speedup minimum is missed,
do not stop at reporting the miss. Preserve the result, then optimize.

Work in this order:

1. Verify that candidate and control measure equivalent semantics, byte/file
   shapes, cache state, allocation independence, and timing boundaries.
2. Separate fixture/setup time, CLI/polling time, public API outer time, service
   time, mount/projection time, data movement, persistence, and cleanup.
3. Profile or instrument the slow candidate path without moving required work
   outside the formal boundary.
4. Look first for accidental full-tree walks, eager hydration/materialization,
   redundant hashing or serialization, sync storms, duplicate copies,
   per-file/per-layer RPCs, repeated namespace/process startup, tight polling,
   lock contention, unnecessary reconciliation, and avoidable allocations.
5. Rank hypotheses by expected impact, implementation risk, and measurement
   cost.
6. Implement one coherent optimization at a time with focused correctness
   coverage.
7. Re-measure the failed gate with a fresh matched pair.
8. Retain an optimization only when correctness still passes and the evidence
   shows a reproducible improvement.

Do not improve a score by weakening durability, changing the workload,
pre-populating forbidden state, moving measured work before the timer,
shrinking the fixture, inflating the control, raising host resources, using
tmpfs, or granting capability to ordinary workloads.

Continue optimization while a credible in-scope hypothesis remains. If the
minimum still cannot be met, produce an evidence-backed bottleneck analysis,
the best valid result achieved, rejected hypotheses, and the smallest next
architectural change. A failed gate remains `FAIL`; do not relabel it
`UNKNOWN`.

## Avoid the prior roundtrip trap

The successful quick PoC used approximately 446 command-output polls. Do not
repeat that pattern.

- Use one long-running in-sandbox coordinator per focused case.
- Run all samples for that case inside the invocation.
- Write structured results directly to the persistent evidence root.
- Use cursor/offset-based output reads.
- Poll with backoff and no more frequently than the execution spec permits.
- Do not start a new gateway or sandbox for every sample.
- Record CLI call count, poll count, bytes read, build-lock wait, runner time,
  and measured operation time separately.

## Evidence, cleanup, and truthfulness

- Create a fresh evidence root under the path specified by the execution spec.
- Never reopen, rewrite, or append to a sealed prior run.
- Tag every runtime object with the unique run ID.
- Use exact-run cleanup only; never broad Docker prune or cleanup.
- Preserve failed evidence before cleanup.
- Prove final manager and observability counts return to the run's baseline.
- Seal the final tree with `manifest.sha256`.
- Independently verify the manifest after sealing.
- Treat any missing required gate as `UNKNOWN`, which makes aggregate
  `POC_100X_NOT_SUPPORTED`.
- Treat a measured miss as `FAIL`, not `UNKNOWN`.
- Never manufacture, extrapolate, or selectively omit samples.

## Progress behavior

Keep the embedded progress tracker current after every material attempt:

- phase and gate state;
- exact command or change;
- result and evidence path;
- diagnosis;
- next action;
- blocker classification;
- source/config/binary/fixture identities that could invalidate prior passes.

Send concise progress updates while work is ongoing. Continue working after
each update. Do not turn a routine status update into a request for permission.

If interrupted or context is compacted, resume from the tracker and evidence
ledger. Do not restart passed work or discard failed-attempt history.

## Completion condition

Do not finish until all of the following are true:

- the exact formal scorecard has been executed or a genuine external hard
  blocker has been exhaustively proven;
- implementation and harness bugs found in scope are fixed and verified;
- every minimum performance miss has gone through the optimization loop;
- focused cases pass or retain an exact honest failure;
- the final focused campaign is complete;
- correctness, security, resource, and cleanup gates are decided;
- the evidence tree is sealed and independently verified;
- the tracker and terminal decision agree.

Lead the final report with:

1. `POC_CORRECTNESS_PASS|FAIL`
2. `POC_100X_SUPPORTED|NOT_SUPPORTED`
3. `POC_500X_SUPPORTED|PARTIAL|NOT_SUPPORTED`
4. `AG_SQUASH_PASS|FAIL|UNKNOWN`
5. `AG_STREAM_PASS|FAIL|UNKNOWN`

Then report every gate's raw samples, median, max, exact matched ratio, absolute
ceiling result, correctness result, source/config/binary/fixture/image
identities, resource envelope, roundtrip counts, cleanup proof, fresh evidence
root, manifest SHA-256, and remaining failures or hard blockers.

Make the best decisions you can from evidence. Keep moving, use subagents
wisely, fix what is fixable, optimize what is slow, and do not stop at partial
progress.
