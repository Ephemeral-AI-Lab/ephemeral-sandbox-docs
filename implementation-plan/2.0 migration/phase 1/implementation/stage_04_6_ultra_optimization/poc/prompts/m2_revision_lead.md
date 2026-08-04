/goal Take over Stage 04.6 MPLA at the sealed M2 blocker checkpoint, implement the ratified scoped OverlayFS authority, correct HV-07, and drive the PoC to an evidence-backed terminal decision.

You are the corrective M2R lead. Do not restart the PoC, weaken its gates, or overwrite prior evidence. Continue from:

- repository: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
- blocked checkpoint SHA: `d49c44b35eabbb40b98874d907edcdd40decf6e3`
- blocked checkpoint ref: `mpla-poc/m2-blocked-20260728T011331p0800`
- docs root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization`
- sealed blocker run: `m2-20260727T230353p0800`
- sealed M1 manifest SHA-256: `fe02d5b960f3e9c1937a3d1c1c745dc2f3f7fd59bee5335d5f4bf33e5939f45c`

First read the current `/goal` objective file supplied to your Codex task. Then read completely:

1. `ephemeral-sandbox/AGENTS.md`
2. `ephemeral-sandbox/CLAUDE.md`
3. `ephemeral-sandbox/docs/maintainer-architecture.md`
4. `requirements_and_prohibitions.md`
5. `new_plan.md`
6. `poc/test_matrix.md`
7. `poc/implementation_plan.md`
8. `poc/progress_tracker.md`
9. this prompt and both `m2_revision_worker_*.md` prompts

The user has already made the design decision. Do not ask whether `CAP_SYS_ADMIN` is allowed. Ratified decision `SD-04.6-002` permits it for the authenticated dedicated `mpla-storage-admin-v1` storage/projection lifecycle process. That process may call the required mount-namespace, `mount`, and `umount2` operations. This is not permission to add `CAP_SYS_ADMIN` to arbitrary `exec_command`, a general shell, the sandbox workload, or workload descendants.

The earlier architecture did not prohibit the capability: it assumed a privileged dedicated runner. The M2 integration mistake was placing `MplaSession::open` and OverlayFS mount work in the hardened ordinary command child, whose capability/seccomp profile intentionally denies it. Correct the process boundary, not the stationary-publication design.

## Immediate takeover protocol

1. Verify the repository and named ref both resolve to the exact blocked checkpoint. Inspect `git status` and preserve every unrelated user change.
2. Verify the sealed M1 and M2 blocker manifests before changing code. Never write new artifacts into the sealed M2 run.
3. Mint:
   - a fresh corrective checkpoint/ref;
   - interface marker `m2r-iface-v1`;
   - a fresh corrective run ID;
   - a fresh evidence root.
4. Update the progress tracker with these exact identities before any physical work.
5. Freeze the smallest additive public lifecycle interface needed for:
   - exact authenticated operation, run, lease, sandbox/workspace, namespace, and allowed-path binding;
   - trusted lifecycle executable identity;
   - exact capability/seccomp profile;
   - durable success/failure/cancelled receipt;
   - negative ordinary-exec/workload isolation evidence;
   - faultpoint-to-real-operation witnesses for all `NamedFaultPoint::ALL`.
6. Keep shared contracts, security-profile schema, trusted executable allowlist, runtime/catalog configuration, aggregate dispatch, manifest sealing, tracker updates, and execution leases lead-owned.

## Multi-task execution

If Codex task/session management tools are available, create two fresh visible top-level tasks in isolated git worktrees at the same corrective checkpoint:

- Worker A: complete `m2_revision_worker_a_security.md`.
- Worker B: complete `m2_revision_worker_b_hv07.md`.

Do not use hidden subagents. Append a lead assignment capsule to each complete prompt containing:

- corrective checkpoint SHA/ref;
- `m2r-iface-v1`;
- exact exclusive file paths;
- corrective run/evidence root;
- current blockers;
- prior M2 capsule;
- execution lease `NONE`;
- any lead-owned additive commit they must consume.

Record task IDs, host IDs, cursors, ownership, and status in the tracker. Monitor both tasks while continuing lead-owned integration. If task/session management is unavailable, execute the two assignments sequentially under the same non-overlapping scopes, or leave the worker prompts ready for the operator to launch manually; do not broaden file ownership to save time.

## Required implementation boundary

The supported public path must provide a dedicated storage lifecycle execution class, not a privileged form of general command execution.

Required positive behavior:

- an authenticated/lease-bound public runtime lifecycle request selects only the trusted MPLA lifecycle executable;
- its dedicated process receives `CAP_SYS_ADMIN` and a seccomp profile permitting only the required lifecycle syscalls, including `mount` and `umount2`;
- the process operates only on the exact authorized mount namespace and declared payload/control/work paths;
- OverlayFS mount, quiesce, strict unmount, and cleanup succeed through the supported public manager/runtime/observability CLI path;
- the receipt records executable identity, run/lease/session binding, namespaces/paths, capability sets, seccomp identity/mode, mount identity/options, timestamps, result, and cleanup.

Required negative behavior:

- ordinary `exec_command`, arbitrary shells, workloads, and descendants do not receive `CAP_SYS_ADMIN`;
- those processes cannot call a successful mount;
- callers cannot substitute a different executable, path, namespace, run ID, lease, or operation;
- response loss/retry remains idempotent, stale/fenced requests fail closed, and failed/cancelled requests retain evidence;
- capability is dropped before any workload entry, or the lifecycle helper is a separate process that cannot become the workload.

`NoNewPrivs=1` may remain where compatible; it is not a substitute for the exact capability and seccomp evidence.

Do not:

- add a generic `--privileged`, `--cap-add`, or privileged-exec flag;
- use direct Docker execution as qualifying evidence;
- weaken the fixed four-vCPU/four-GiB host, 8-MiB candidate pool, or 96/128-MiB storage cgroup;
- relabel developmental or marker-only tests as physical PASS;
- omit failed, cancelled, timeout, crash, or cleanup evidence.

## HV-07 correction

All 46 frozen named faultpoints must occur inside their corresponding real allocation, lease, owner, semantic, locator, ref, activation, projection, evacuation, or retirement operation. A marker call by itself is not a real-operation witness. The physical sweep may begin only after host/source evidence proves 46/46 mappings, exact fault hits, replay outcomes, and physical-complete rejection when any witness is missing.

If public lifecycle restart/recreate remains unsupported, report the container-kill subset `UNKNOWN` with the exact missing API. Do not simulate it. Process-SIGKILL coverage must still be real.

## Integration and verification

Review and cherry-pick one scoped worker commit at a time. Reject unassigned paths, hidden failures, contract drift, or missing evidence. Independently run:

- formatting;
- focused profile/auth/isolation tests;
- 46-point real-operation host/fault tests;
- the canonical all-target PoC suite;
- strict scoped Clippy;
- supported Linux/arm64 build;
- diff and manifest checks.

Fix lead-owned aggregate dispatch only after worker interfaces are accepted.

Before any manual/physical sandbox operation, run:

`bin/start-sandbox-docker-gateway --rebuild-binary`

Use only:

- `sandbox-manager-cli`
- `sandbox-runtime-cli`
- `sandbox-observability-cli`

for authoritative manual sandbox lifecycle operations.

## Physical campaign

Initial physical execution lease is `NONE`. After host integration:

1. issue one exclusive serial lease for scoped-profile qualification;
2. prove the positive lifecycle mount/unmount and the negative ordinary-workload denial;
3. release and clean that lease;
4. prepare immutable heavy fixtures under a new run ID;
5. issue exact serial leases for HV-01 through HV-10, including every HV-07 point;
6. enforce each frozen phase-local hard stop independently, with no aggregate
   campaign hard stop or deadline carry-over;
7. preserve partial evidence before cleanup on every failure, timeout, cancellation, or crash;
8. audit and destroy only exact run-scoped resources through the public CLIs;
9. seal and independently verify the new manifest.

Never overlap measured physical campaigns.

## Progress reporting and terminal result

Keep `poc/progress_tracker.md` authoritative. Record checkpoint identities, interface, assignments, command results, artifacts, resource maxima, lease transitions, failures, cleanup, and gate decisions as they occur.

Return a final outcome only after the evidence exists:

- `PASS` only if the scoped profile positive/negative gates, all required HV rows, root/oracle checks, real crash convergence, no-hidden-copy gates, fixed resource envelope, cleanup, and `X_unexplained=0` pass;
- `FAIL` when a hard invariant is disproven;
- `BLOCKED` or `UNKNOWN` when the named evidence remains unavailable.

Your final handoff must include the final checkpoint/ref, exact changed files, worker commits and integration SHAs, every verification command and result, run/evidence identities, manifest hashes, physical results, maxima, failures/unknowns, cleanup proof, and the evidence-backed adoption recommendation.
