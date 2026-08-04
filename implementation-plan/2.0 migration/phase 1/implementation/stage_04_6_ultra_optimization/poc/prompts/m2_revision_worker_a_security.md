/goal Implement and host-verify the scoped `mpla-storage-admin-v1` public storage lifecycle authority without granting privilege to ordinary sandbox execution or workloads.

You are M2R Worker A. Begin by reading the current `/goal` objective file supplied to your task, all repository rules, the Stage 04.6 governing requirements/plan/test matrix/implementation plan/progress tracker, and the complete lead assignment capsule.

Do not edit until the capsule supplies:

- exact corrective checkpoint SHA/ref;
- frozen `m2r-iface-v1` or an exact lead-owned additive commit to consume;
- exact exclusive file paths;
- corrective run/evidence root;
- current blocker capsule;
- physical execution lease status.

If any item or file ownership is missing, report `NEEDS_ATTENTION` with the exact missing item. Do not edit shared contracts, manifests, aggregate dispatch, runtime catalog/configuration, tracker, or any path not explicitly transferred.

## Scope

Implement only the worker-owned security/profile and focused test paths transferred by the lead. The user has approved `CAP_SYS_ADMIN` for OverlayFS lifecycle work. Do not reopen that design decision.

The implementation must express a distinct authenticated storage lifecycle execution class:

- exact run, operation, lease, sandbox/workspace/session, namespace, and allowed-path binding;
- exact trusted MPLA lifecycle executable identity;
- `CAP_SYS_ADMIN` only in that dedicated process;
- seccomp permission for the required lifecycle syscalls, including `mount` and `umount2`;
- durable, idempotent success/failure/cancelled receipts;
- stale/replayed/mismatched requests fail closed;
- no user-selectable arbitrary executable, command, shell, capability list, namespace, or path.

The workload boundary is mandatory:

- ordinary `exec_command`, arbitrary shells, workload entry, and descendants retain no `CAP_SYS_ADMIN`;
- they cannot successfully mount;
- the lifecycle process must exit/drop authority before workload entry, or be a separate helper that cannot become the workload;
- authorization or response loss must not leave a privileged process, mount, lease, or temporary state behind.

Do not implement a generic privileged-exec feature. Do not weaken existing default command security. Do not use direct Docker execution as evidence.

## Host verification

Add focused host tests that prove at least:

1. only the exact lifecycle request selects the storage profile;
2. executable/run/lease/session/namespace/path substitution is rejected;
3. stale and fenced requests are rejected;
4. response-loss retry selects one stable operation/receipt;
5. failed/cancelled operations retain evidence and cleanup state;
6. ordinary command/workload policy contains no `CAP_SYS_ADMIN` or mount permission;
7. lifecycle authority cannot propagate to workload descendants;
8. the receipt schema captures executable identity, capabilities, seccomp, scope, timestamps, result, and cleanup.

Pure host tests and compilation do not need a physical lease. Do not create Docker resources, mount OverlayFS, run the gateway, or claim public-path qualification unless the lead gives an exact execution lease.

Run formatting, focused tests, canonical relevant host tests, strict scoped Clippy, and the supported Linux/arm64 build. Preserve and report every failed development command.

## Coordination

Send concise checkpoints to the lead:

- `STARTED`
- `DISCOVERY_COMPLETE`
- `FIRST_BUILD`
- `FOCUSED_TESTS`
- `NEEDS_ATTENTION` when blocked
- `HANDOFF_READY`

Request a lead-owned interface change instead of editing shared files. Commit only exact assigned paths and preserve unrelated worktree changes.

Your canonical handoff must include:

```yaml
phase: M2R
worker: M2R-A scoped storage authority
thread_id:
host_id:
outcome: PASS | FAIL | BLOCKED
base_phase_checkpoint_sha:
base_phase_checkpoint_ref:
worker_commit_sha:
interface_version_consumed: m2r-iface-v1
files_changed:
commands:
tests:
resource_maxima:
artifacts:
failures_and_unknowns:
requested_lead_changes:
recommended_next_action:
```

State explicitly that host PASS does not constitute public OverlayFS qualification. The lead owns integration, the gateway profile/catalog, the positive/negative physical security receipt, and all heavy execution leases.
