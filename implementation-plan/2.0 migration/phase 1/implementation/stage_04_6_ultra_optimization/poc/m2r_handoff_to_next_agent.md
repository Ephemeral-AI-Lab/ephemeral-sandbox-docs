# Stage 04.6 MPLA M2R handoff — finish the PoC

Updated: `2026-07-28T03:13:35+08:00`

## Mission

Resume Stage 04.6 MPLA at the sealed M2 blocker, finish the ratified scoped
OverlayFS authority correction, correct HV-07, and drive the fresh M2R campaign
to a terminal evidence-backed adoption decision.

The full goal objective is:

`/Users/yifanxu/.codex/attachments/cbc6dd16-724e-4063-9f1b-5e97e9037d9d/goal-objective.md`

Read that file before changing code or evidence. Treat the goal as active. Do
not mark it blocked merely because a worker or a physical operation is still
running; wait and sync casually. Do not mark it complete until the fresh run is
sealed and the terminal decision is recorded.

## Resume state

- Source repository:
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
- Source branch: `upgrade-2.0-phase-1`
- Integrated HEAD:
  `06623414b1e0e8875de9434d2fe15ba38cdde5e4`
- Source worktree at handoff: clean, branch 35 commits ahead of origin
- Correct M2R branch ref:
  `refs/heads/mpla-poc/m2r-checkpoint-20260728T015724p0800`
- Correct M2R branch target:
  `06623414b1e0e8875de9434d2fe15ba38cdde5e4`
- Sealed blocked M2 ref:
  `refs/heads/mpla-poc/m2-blocked-20260728T011331p0800`
- Sealed blocked M2 target:
  `d49c44b35eabbb40b98874d907edcdd40decf6e3`
- M2R interface: `m2r-iface-v1`
- Reserved fresh run ID: `m2r-20260728T015724p0800`
- Physical lease: `NONE`
- Both implementation workers are finished; their changes are integrated.

### Ref ambiguity warning

There are two similarly named refs:

```text
06623414... refs/heads/mpla-poc/m2r-checkpoint-20260728T015724p0800
b75185a8... refs/mpla-poc/m2r-checkpoint-20260728T015724p0800
```

The second ref is stale. A short ref such as
`mpla-poc/m2r-checkpoint-20260728T015724p0800` is ambiguous and may resolve to
`b75185a8...`. Always use the full
`refs/heads/mpla-poc/m2r-checkpoint-20260728T015724p0800` name. Do not delete or
rewrite the stale custom ref without first validating that no other workflow
depends on it.

## Evidence state

The sealed M2 blocker evidence is at:

`/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/m2-20260727T230353p0800`

Important sealed files:

- `environment/capability-blocker.json`
- `environment/hv-terminal-status.json`
- `manifest.sha256`

SHA-256 of the sealed M2 `manifest.sha256` file:

`17ef3fd6c18d68ac2eaeb4e071ee3cb6b385bc801058ed7ea8792145d652e298`

Frozen sealed M1 manifest identity:

`fe02d5b960f3e9c1937a3d1c1c745dc2f3f7fd59bee5335d5f4bf33e5939f45c`

The reserved M2R evidence root is:

`/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/m2r-20260728T015724p0800`

At handoff, that directory does **not** exist and no M2R physical evidence has
been collected. This is intentional. Create it only when beginning the fresh
physical campaign. Do not copy old evidence into it or pre-populate it with
handoff material.

## Integrated commit chain

From the sealed M2 blocker:

```text
d49c44b35  sealed blocked checkpoint
90f05f245  freeze M2R corrective interface
24bef8c21  bind storage authority to public session
b75185a8e  package scoped storage administrator
7a09c466b  add scoped storage admin authority
06623414b  wire HV-07 durable operation edges
```

### Worker A — scoped storage authority

Worker task: `019fa4c5-111b-7783-81eb-37c3410e2285`

Worker commit `96b31c909da99001d3502cd0b00ec6f44a6e342e` was integrated
as `7a09c466bb91dcea5616bb78f6116b0ed7eaa70b`.

Files:

- `crates/sandbox-runtime/mpla-poc/src/storage_admin.rs`
- `crates/sandbox-runtime/mpla-poc/src/bin/mpla-storage-admin-v1.rs`
- `crates/sandbox-runtime/mpla-poc/tests/storage_admin_security.rs`

Verified:

- `storage_admin_security`: 12/12 passed
- scoped no-dependency Clippy with `-D warnings`: passed
- workspace format check: passed
- scoped diff check: passed

Dependency-inclusive Clippy still encounters unrelated pre-existing LayerStack
`nonminimal_bool` and `too_many_arguments` findings. Do not misreport those as
M2R regressions.

### Worker B — HV-07 operation-owned edges

Worker task: `019fa4c5-d807-7b92-94f5-e4f8e9ad450a`

Worker commit `3a2be96fa1a3838c60675a41887197f11364a02e` is integrated at
HEAD `06623414b1e0e8875de9434d2fe15ba38cdde5e4`.

Files:

- `crates/sandbox-runtime/mpla-poc/src/activation.rs`
- `crates/sandbox-runtime/mpla-poc/src/locator.rs`
- `crates/sandbox-runtime/mpla-poc/src/owner.rs`
- `crates/sandbox-runtime/mpla-poc/src/quiesce.rs`
- `crates/sandbox-runtime/mpla-poc/src/recovery.rs`
- `crates/sandbox-runtime/mpla-poc/src/ref_store.rs`
- `crates/sandbox-runtime/mpla-poc/src/semantic/mod.rs`
- `crates/sandbox-runtime/mpla-poc/src/session.rs`
- `crates/sandbox-runtime/mpla-poc/tests/cases/heavy_lead.rs`
- `crates/sandbox-runtime/mpla-poc/tests/crash_matrix.rs`

Verified:

- focused crash matrix: 5 passed
- focused heavy faults: 2 passed
- canonical operation-owned suites: 38 passed
- source call-site map: 46/46 operation-owned mappings
- scoped no-dependency Clippy, format, and diff checks: passed

An unrelated uncommitted `bin/sandbox-catalog-export` change existed only in
the worker worktree and was not integrated.

## Ratified authority boundary

Decision `SD-04.6-002` permits `CAP_SYS_ADMIN` only in the authenticated fixed
helper:

`/usr/local/libexec/ephemeral-sandbox/mpla-storage-admin-v1`

It must never be available to arbitrary exec, shells, workload descendants, or
the ordinary command path. The helper is limited to fixed privileged operations:

- `mount`
- `umount2`
- `setns`
- `syncfs`

The ordinary sandbox command path must continue to deny direct mount attempts.

## What is implemented

- Fixed helper protocol and binary.
- Invocation validation and fixed-path/scope checks.
- Process capability/seccomp/no-new-privileges inspection primitives.
- Fixed OverlayFS mount, strict unmount, and cleanup lifecycle.
- Replay handling and security unit tests.
- Public session request shape and catalog entry.
- Manager routing and helper packaging/installation.
- HV-07 durable operation edges at all 46 source call sites.

## Remaining work

### 1. Make the durable receipt contain measured authority evidence

`StorageAdminProcessEvidence` and `StorageAdminMountPlanEvidence` exist and are
tested separately, but `StorageAdminReceipt` still records mostly constant
trusted values. Wire the measurements into the durable receipt and validate
them on replay:

- resolved executable identity and SHA-256
- raw effective, permitted, inheritable, bounding, and ambient capability sets
- seccomp profile identity/hash, mode, filter count, and no-new-privileges
- mount namespace identity
- mountinfo before and after, exact options, and exact target
- cgroup binding
- start/end timestamps, outcome, cleanup result, and failure detail

Preserve evidence for failed, cancelled, and receipt-write-failure paths.

The helper narrows effective/permitted capabilities but does not yet narrow the
bounding set. Drop all bounding capabilities except `CAP_SYS_ADMIN` while
`CAP_SETPCAP` is still usable, then perform and record post-drop verification.

The helper currently inherits Docker's default seccomp profile. The ratified
boundary still needs an exact profile identity/hash. A narrow fixed additional
BPF filter that prevents exec/fork/clone while allowing the storage lifecycle is
one viable design, but it must be tested against the real lifecycle rather than
asserted from constants.

### 2. Register authenticated runtime dispatch

`MPLA_STORAGE_ADMIN_SPEC` exists in the catalog, routing exists in the manager,
and packaging installs the helper, but
`crates/sandbox-runtime/operation/src/operations/registry/workspace_session_operations.rs`
does not register or handle the operation.

Add a narrow dependency from
`crates/sandbox-runtime/operation/Cargo.toml` to
`sandbox-runtime-mpla-poc` if that remains the accepted architecture. The
handler must:

- accept only the exact `request_json` argument
- bind the request to the exact sandbox ID and operation/request ID
- resolve the live workspace session
- bind the server lease ID and holder PID
- resolve `/proc/<holder-pid>/ns/mnt`
- bind the exact cgroup path and fixed storage/run roots
- spawn only the fixed trusted helper, with no arguments and a cleared
  environment
- use bounded JSON stdin/stdout
- reject every mismatch before privileged work
- return the durable receipt

For race-safe cgroup placement, spawn the helper with piped stdin so it blocks
on input, write its PID to the resolved workspace `cgroup.procs`, verify
`/proc/<pid>/cgroup`, and only then send the invocation. Record that binding in
the receipt.

### 3. Adopt a pre-mounted workspace in the PoC session

The heavy preparation path still calls `MplaSession::open`, which attempts the
mount through ordinary `exec_command` and reproduces the sealed blocker.

Add an explicit pre-mounted/adopted session path:

1. Ordinary public preparation creates allocation, lease, session metadata, and
   fixed directories.
2. The public authenticated storage operation performs the mount.
3. The ordinary harness adopts the already-mounted workspace without issuing a
   mount.
4. The public storage operation performs quiesce, strict unmount, and cleanup.

Do not add a hidden direct-Docker or arbitrary privileged escape hatch.

### 4. Finish the HV-07 aggregate

The 46/46 source call sites now emit operation-owned durable edges, but 36
aggregate child preparation/dispatch branches in
`crates/sandbox-runtime/mpla-poc/tests/cases/heavy_lead.rs` still only call a
marker or lack operation-specific preparation. `B-007` therefore remains open.

Implement actual operation-specific preparation and dispatch for every
aggregate child. Require real operation witnesses and exact first-hit/replay
outcomes. Audit `RealOperationWitness.operation_state_parent_synced` in
`recovery.rs`; it appears to be hard-coded `true` and must be backed by measured
state if it is used as evidence.

### 5. Complete host verification

At minimum:

```bash
cargo fmt --all -- --check
cargo test -p sandbox-runtime-mpla-poc --all-targets
cargo clippy -p sandbox-runtime-mpla-poc --all-targets --no-deps -- -D warnings
cargo zigbuild --manifest-path crates/sandbox-runtime/mpla-poc/Cargo.toml \
  --target aarch64-unknown-linux-musl --release --bins --tests
cargo test -p xtask --test package
cargo test -p sandbox-operation-catalog --features runtime --test runtime
cargo check -p sandbox-provider-docker
cargo test -p sandbox-manager --lib
cargo test -p sandbox-runtime --all-targets
git diff --check
```

Also rerun the focused authority/authentication/isolation tests and the
canonical 46-point PoC suites. Record exact commands, counts, hashes, and any
non-M2R baseline failures in the tracker.

### 6. Run the fresh physical campaign

Before physical work:

1. Update `progress_tracker.md` with the exact integrated HEAD, interface, run
   ID, evidence root, planned lease, and host-verification result.
2. Rebuild the gateway as required by repository policy:

   ```bash
   bin/start-sandbox-docker-gateway --rebuild-binary
   ```

3. Use only `sandbox-manager-cli`, `sandbox-runtime-cli`, and
   `sandbox-observability-cli` for manual sandbox operations.
4. Use public operations only. Direct Docker inspection may be diagnostic, but
   it is not qualifying evidence and must not mutate the campaign.

Issue a serialized lease for the positive storage lifecycle first:

- authenticated mount through the fixed helper
- verify exact workspace/session/cgroup/namespace binding
- negative ordinary-command mount denial
- authenticated quiesce, strict unmount, cleanup
- release the lease

Only after that passes, run fresh heavy `PREPARE` and `HV-01` through `HV-10`
serially, including every HV-07 aggregate child. Preserve partial evidence
before cleanup on every failure.

The supported public API does not provide a qualifying container
restart/recreate operation. Keep that subset `UNKNOWN`; do not simulate it or
call direct Docker as a substitute. Real process-SIGKILL coverage remains
required.

Finish with exact run-scoped public-CLI cleanup, seal and verify the manifest,
record resource maxima, require `X_unexplained=0`, and write the final adoption
decision.

## First commands for the next agent

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
git status --short --branch
git rev-parse HEAD
git rev-parse refs/heads/mpla-poc/m2r-checkpoint-20260728T015724p0800
git show-ref | rg 'mpla-poc/m2r-checkpoint|mpla-poc/m2-blocked'
test "$(git rev-parse HEAD)" = \
  "06623414b1e0e8875de9434d2fe15ba38cdde5e4"
test "$(git rev-parse \
  refs/heads/mpla-poc/m2r-checkpoint-20260728T015724p0800)" = \
  "06623414b1e0e8875de9434d2fe15ba38cdde5e4"
```

Then read:

- `CLAUDE.md`
- this handoff
- `poc/progress_tracker.md`
- `poc/implementation_plan.md`
- `poc/test_matrix.md`
- `requirements_and_prohibitions.md`
- the three `poc/prompts/m2_revision_*.md` prompts

Inspect the current receipt, helper, session, and runtime registry before
editing. Keep host work and physical evidence work separated.

## Dirty-state warning

The documentation repository
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs` is on branch
`layerstack_2_0`, five commits ahead of origin, with existing user-owned
modifications to the governing Stage 04.6 documents and three untracked M2R
prompt files. Preserve them. This handoff file is an additional untracked
document; do not sweep all documentation changes into a commit without
reviewing their ownership.

## Terminal completion checklist

The PoC is not finished until all of the following are true:

- measured authority evidence is durable and replay-validated
- authenticated public dispatch is live and fail-closed
- ordinary mount remains denied
- helper capability, seccomp, cgroup, namespace, and executable bounds are
  proven
- pre-mounted session choreography is used
- HV-07 aggregate children perform real operation-specific dispatch
- canonical host and Linux/arm64 verification is recorded
- fresh physical lifecycle and HV campaign evidence is collected
- unsupported restart/recreate coverage remains honestly `UNKNOWN`
- cleanup succeeds through the public control plane
- manifest is sealed and verified
- resource maxima and `X_unexplained=0` are recorded
- the final adoption decision is written into the governing tracker

