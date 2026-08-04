/goal Finish Stage 04.6 MPLA PoC implementation and benchmark verification from the sealed M2R terminal decision. Deliver a fresh, evidence-backed adoption decision; do not reopen or alter any sealed run.

# M2R post-Docker takeover — complete PoC implementation and benchmark verification

You are the single lead for the next fresh MPLA physical campaign. The previous
M2R corrective implementation is committed and its first fresh campaign was
sealed as `REVISE`, not as a pass: Docker was unavailable at that time. The
user has now started Docker Desktop and the supported public surface has been
rechecked successfully. Your job is to complete the remaining public lifecycle
implementation, then run and verify the benchmark honestly.

Do not treat the previously sealed `REVISE` as a reason to restart, overwrite,
or relabel historical evidence. It remains a valid record of the earlier
platform outage. Do not claim a physical pass from host tests.

## Read before changing code or evidence

Read completely, in this order:

1. The current Codex `/goal` objective supplied to this task.
2. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/AGENTS.md`
3. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/CLAUDE.md`
4. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/docs/maintainer-architecture.md`
5. `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/requirements_and_prohibitions.md`
6. The sibling `new_plan.md`, `poc/test_matrix.md`, `poc/implementation_plan.md`, and `poc/progress_tracker.md`.
7. This prompt, the prior `poc/prompts/m2_revision_lead.md`, and the sealed
   M2R terminal-decision evidence listed below.

Treat the tracker as authoritative. Preserve all unrelated dirty changes in
both repositories. Do not create hidden subagents; the previous two worker
changes are already integrated.

## Exact resume state

- Source repository: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
- Source branch: `upgrade-2.0-phase-1`
- Current integrated source commit:
  `41888fb9658ac26682af754701ea3b0c6389d877`
  (`fix(mpla): bind storage authority to public runtime`)
- New terminal ref at that commit:
  `refs/heads/mpla-poc/m2r-terminal-20260728T074311p0800`
- Frozen M2R checkpoint ref (do not move it):
  `refs/heads/mpla-poc/m2r-checkpoint-20260728T015724p0800` =
  `06623414b1e0e8875de9434d2fe15ba38cdde5e4`
- Stale, ambiguous custom ref (do not delete, update, or use as the checkpoint):
  `refs/mpla-poc/m2r-checkpoint-20260728T015724p0800` =
  `b75185a8e9b35e77ecfa0023cf8c780006d5cd7e`
- Immutable blocked M2 checkpoint:
  `refs/heads/mpla-poc/m2-blocked-20260728T011331p0800` =
  `d49c44b35eabbb40b98874d907edcdd40decf6e3`
- Frozen M1 manifest SHA-256:
  `fe02d5b960f3e9c1937a3d1c1c745dc2f3f7fd59bee5335d5f4bf33e5939f45c`
- Sealed M2 manifest SHA-256:
  `17ef3fd6c18d68ac2eaeb4e071ee3cb6b385bc801058ed7ea8792145d652e298`

The prior M2R run is immutable:

`/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/m2r-20260728T015724p0800`

It contains a six-file sealed evidence tree with manifest SHA-256:

`4981f725ac2c6af24078415fee5a8152af1b089831cf1a18cfb7d8486d019f10`

Read its `terminal-decision.json`, `environment/public-cli-availability.json`,
and `manifest.sha256`; verify the manifest before proceeding. Do not append to
that root and do not copy any of its files into a later run.

## Docker state now

After the prior seal, the user started Docker Desktop. The required supported
surface was rebuilt and then confirmed:

```bash
SANDBOX_GATEWAY_CONFIG_YAML="$PWD/config/mpla-poc-m2.yml" \
SANDBOX_GATEWAY_LOG=/tmp/mpla-m2r-resume-gateway.log \
  bin/start-sandbox-docker-gateway --rebuild-binary
bin/sandbox-manager-cli list_docker_images
bin/sandbox-manager-cli list_sandboxes
bin/sandbox-observability-cli snapshot
```

`list_docker_images` returned the qualified Ubuntu 24.04 arm64 image
`ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`.
Both sandbox and observability lists were empty. This proves only that Docker
is presently reachable; recheck it through those supported CLIs before issuing
the new physical lease. Do not use Docker commands as qualifying evidence.

## What is already implemented and verified on the host

Commit `41888fb9658ac26682af754701ea3b0c6389d877` integrates the ratified
`SD-04.6-002` authority correction and HV-07 work:

- public typed `mpla_storage_admin` request projection, catalog entry, daemon
  routing, and strict sandbox/session/lease binding;
- fixed helper at
  `/usr/local/libexec/ephemeral-sandbox/mpla-storage-admin-v1`, with no
  arbitrary command or argument surface;
- helper executable/cgroup/mount-namespace checks, capability narrowing,
  no-new-privileges, fixed seccomp BPF, fixed OverlayFS lifecycle, durable
  receipt validation, and negative ordinary-workload isolation tests;
- Docker profile confines `CAP_SETPCAP` to the helper lifecycle path, not
  normal `exec_command`;
- all 46 HV-07 names have operation-specific real-operation source witnesses
  and host verification.

The following host gates have passed on that commit: formatting; complete PoC
crate tests; strict scoped Clippy; Linux/arm64 zigbuild; package and operation
catalog tests; Docker provider and manager tests; runtime, CLI, and projection
tests; and `git diff --check`.

Do not weaken this boundary. `CAP_SYS_ADMIN`, mount, and umount are allowed
only in the authenticated fixed lifecycle helper. General exec, shells,
workloads, and descendants must neither inherit that capability nor mount.

## Remaining implementation gate

Before running the physical benchmark, inspect the actual public lifecycle
path end to end. The generic public workspace-session create operation did not
yet construct the MPLA allocation, lease, control, and session state needed to
form a routed storage-admin request; its generic overlay target may conflict
with the MPLA target. Implement the smallest lead-owned public choreography
that creates the exact allocation/lease/control/session layout, routes the
authenticated storage request, and can be driven entirely through supported
manager/runtime/observability CLIs.

First establish the root cause and add/adjust focused regression coverage.
Do not work around it with direct Docker execution, a generic privileged flag,
mock evidence, an arbitrary helper command, or a weaker resource envelope.
Keep the frozen four-vCPU/four-GiB host, 8-MiB candidate pool, and 96/128-MiB
storage cgroup unchanged.

## New run, lease, and evidence rules

1. Start from `41888fb9658ac26682af754701ea3b0c6389d877` and create a new
   uniquely named checkpoint/ref. Never update the frozen M2R checkpoint or
   stale custom ref.
2. Mint a new run ID and evidence root under
   `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/`.
   The root must not exist before this new campaign begins. Record
   `copied_prior_evidence: false`.
3. Update `poc/progress_tracker.md` with the checkpoint, run identity, exact
   lease owner, and planned serial campaign before physical work.
4. Before every manual sandbox lifecycle operation, rebuild with
   `bin/start-sandbox-docker-gateway --rebuild-binary` and use only
   `sandbox-manager-cli`, `sandbox-runtime-cli`, and
   `sandbox-observability-cli` for qualifying manual operations.
5. Check public sandbox and observability inventory first. Do not touch
   unrelated resources. Use exactly scoped cleanup and prove it afterwards.
6. Hold one exclusive physical lease at a time. Preserve failed, cancelled,
   timeout, and crash evidence before releasing it.

## Required verification and benchmark campaign

Complete the host gate for the public choreography, then run these phases in
order through the supported public interfaces:

1. Scoped authority qualification: prove the authenticated helper's real
   OverlayFS mount, quiesce, strict unmount, and cleanup; capture executable
   hash, full capability sets, seccomp/no-new-privileges state, cgroup,
   namespace, paths, mount options/IDs, timestamps, and durable receipt.
2. Negative qualification: prove ordinary exec and workload descendants lack
   `CAP_SYS_ADMIN` and cannot mount; prove substituted executable/path/
   namespace/run/lease/session and stale/replayed requests fail closed.
3. Create immutable heavy fixtures through the public lifecycle, then execute
   HV-01 through HV-10 serially under their frozen phase-local limits. Do not
   impose an aggregate campaign deadline or carry unused time between phases.
   Run every required HV-07 process-SIGKILL point with a real operation
   witness. If a public restart/recreate API is unavailable, state precisely
   which container-kill subset is `UNKNOWN`; do not simulate it.
4. Verify the exact root/oracle, stationary/no-hidden-copy, ownership,
   recovery old-or-complete-new, performance, resource, OOM, FD/mount/leak,
   reconciliation, and `X_unexplained=0` requirements in the test matrix.
5. Record command, artifact path, duration, maxima, cleanup, and terminal
   result for every required row. A skipped or host-only row is never a
   physical pass.
6. Seal the fresh evidence tree and independently run both the PoC
   `evidence-verify` command and `shasum -a 256 -c manifest.sha256`.

Use an append-only ledger in the tracker. Do not mark the effort blocked merely
because an operation is running; wait and collect its output. If an invariant
is disproven, record `FAIL`. If a required platform/API is genuinely
unavailable, preserve evidence and record the narrow honest `UNKNOWN` or
`REVISE` decision.

## Final handoff requirements

Do not finish until the new evidence root is sealed and the adoption decision
is written to the tracker and terminal decision artifact. Report:

- final commit and every created ref, including exact target SHAs;
- changed files and host-gate commands/results;
- fresh run ID, evidence root, manifest SHA-256, and verification output;
- authority positive/negative results and receipt locations;
- every HV-01–HV-10 status, HV-07 point count, benchmark timings/maxima, and
  root/oracle/no-copy/reconciliation outcomes;
- cleanup proof and remaining failures/unknowns;
- an evidence-backed `ADOPT`, `REVISE`, or `NOT_ADOPTED` recommendation.

Only recommend `ADOPT` when every required physical and benchmark gate passes.
