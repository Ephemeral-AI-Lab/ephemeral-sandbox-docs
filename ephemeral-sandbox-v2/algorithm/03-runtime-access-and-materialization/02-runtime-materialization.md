# 03.02 — Runtime activation and bounded materialization

## 1. Purpose and owning phases

**Owners:** Phase 03 LayerStack-0 captures/revalidates an AcceptedBinding and
installs bounded read custody. Existing runtime-effect owners retain ownership
of Workspace, OverlayFS, mount, namespace, exec, and manager/daemon lifecycle.
Phase 06 qualifies resource behavior.  
**Purpose:** Specify how an immutable accepted Version becomes usable by a
runtime through either protected read-only activation or bounded streaming
construction of a runtime-private writable destination.

This algorithm consumes the custody established by
[read custody and runtime handoff](01-read-custody-and-runtime-handoff.md). It
does not create an AcceptedVersion, AcceptedBinding, Head, or Root.

## 2. Evidence status

- `SOURCE-VERIFIED`: the sealed e497 base places mutable Workspace, OverlayFS,
  mount, namespace, exec, and lifecycle effects in existing runtime owners.
- `SPIKE-VERIFIED`: none; no V2 activation/materialization latency, RSS, FD,
  byte-I/O, immutability, or cancellation spike has run.
- `INFERRED`: protected immutable use, streaming private materialization,
  explicit byte accounting, and bounded resource admission preserve R0 and its
  ownership map.
- `OPEN`: Phase 03 selects exact read handle/custody representation, supported
  filesystem profile, traversal, destination readiness, cleanup, limits, and
  optional accelerators. Phase 06 selects qualification workloads/targets.

## 3. Two runtime modes

### Mode A — protected immutable activation

```text
AcceptedBinding
  -> admission-owned revalidation
  -> bounded read custody
  -> immutable accepted-payload access
  -> existing runtime activation
```

There is no eager complete-payload copy inherent in this mode. Runtime reads
that occur during execution are real payload reads and are charged to runtime
activation/use, not to a reference operation.

### Mode B — private writable materialization

```text
AcceptedBinding
  -> admission-owned revalidation
  -> bounded read custody
  -> private bounded destination
  -> validated streaming traversal/copy
  -> runtime-private writable Workspace/view
  -> existing runtime activation
```

The accepted payload remains immutable throughout. The mutable destination is
runtime-effect-owned and is never Version identity or selected truth.

## 4. Contract

Conceptual operation names show type and responsibility flow, not exact APIs,
syscalls, mount flags, path spellings, or filesystem assumptions.

### Inputs

- An admission-issued or admission-revalidated `AcceptedBinding`.
- A LayerStack-0 captured immutable Version read plus bounded custody token.
- Runtime request selecting protected immutable access or private writable
  materialization.
- A capability-scoped runtime destination/activation context.
- Finite payload bytes, entries, metadata operations, sparse allocation,
  memory, buffer, descriptor, worker, mount/namespace, destination-space,
  custody-duration, cancellation, cleanup-debt, and deadline budgets.

### Preconditions

1. Binding and generation revalidation succeeded through admission-owned code.
2. Custody was installed relative to retirement before payload access escaped
   LayerStack-0.
3. The accepted closure passed recovery/readiness checks and cannot be opened
   for mutation through the provided capability.
4. Runtime owners reserved required Workspace/mount/namespace/process resources
   and cleanup headroom.
5. The destination is new/private or proven empty under the selected runtime
   contract; it is not inside the accepted payload, LayerStack-0 control paths,
   another live Workspace, or product/live/migration data.
6. No caller treats activation/materialization output as an AcceptedBinding.

### Outputs and typed outcomes

| Outcome | Meaning |
|---|---|
| `ActivatedImmutable(RuntimeHandle)` | Existing runtime owners activated protected immutable Version access under bounded custody. |
| `MaterializedPrivate(WorkspaceHandle)` | A complete validated runtime-private writable destination became ready; accepted payload stayed unchanged. |
| `InvalidBinding` | Binding/generation/accepted metadata could not be revalidated. |
| `UnsupportedEntry(reason)` | The accepted portable entry cannot be represented safely in the selected runtime profile. |
| `DestinationConflict` | Destination was non-private, nonempty, aliased, escaped, or changed unexpectedly. |
| `ResourceLimit(kind)` | Byte, entry, allocation, memory, FD, worker, mount, custody, time, or debt budget would be exceeded. |
| `CancelledPrivate` | No destination became runtime-visible; private partial work was removed or charged as bounded debt. |
| `ActivationFailed(reason)` | Existing runtime owner could not safely mount/namespace/exec the view; accepted truth remains unchanged. |
| `CleanupDeferred(debt)` | Runtime result is not live; bounded private resources await retryable cleanup. |
| `StoreNotReady` | Recovery, retirement state, generation, corruption, or filesystem qualification blocks custody/access. |

## 5. Protected immutable activation algorithm

```text
activate_immutable(binding, runtime_request, budgets):
    capture := LayerStack0.capture_version_read(binding, budgets.custody)
    if capture failed: return typed capture failure

    immutable_access := capture.payload_capability(read_only = required)
    validate runtime request and reserve mount/namespace/FD/worker resources
    cancellation_checkpoint()

    result := runtime.activate_immutable_version(
        immutable_access, runtime_request, reserved_resources)
    if result failed:
        runtime.unwind_private_effects_bounded()
        LayerStack0.release_read_custody(capture.custody)
        return ActivationFailed(result.reason)

    attach custody lifetime to RuntimeHandle
    return ActivatedImmutable(RuntimeHandle)
```

The runtime handle must not contain a writable capability to the accepted
closure. Any mutable upper/work directories are isolated runtime-owned paths.

## 6. Bounded private materialization algorithm

```text
materialize_private(binding, destination_capability, runtime_request, budgets):
    capture := LayerStack0.capture_version_read(binding, budgets.custody)
    if capture failed: return typed capture failure

    validate destination is private, empty, capability-scoped, and non-aliased
    reserve conservative destination bytes, entries, Mem, FD, workers,
        metadata operations, time, and cleanup headroom
    create recognizable private materialization transaction

    for entry in deterministic safe traversal(capture.immutable_payload):
        cancellation_checkpoint()
        validate relative portable path and entry kind
        charge discovered logical/physical resources before growth

        create parent/entry beneath destination without ambient path traversal
        if regular content:
            stream bounded buffers from immutable source to private destination
            account V_read and V_write; never buffer the complete Version
        if link or metadata:
            validate target/value and apply only selected portable semantics

    verify complete destination projection, entry count, bytes, and metadata
    apply runtime-private readiness operation selected by Phase 03/runtime owner
    hand destination to existing runtime activation owner
    transfer cleanup ownership to WorkspaceHandle
    release source custody when the runtime no longer depends on source reads
    return MaterializedPrivate(WorkspaceHandle)
```

If private materialization is a true complete copy, custody can be released
after source traversal and destination verification. If an optional accelerator
creates continuing source dependency, custody remains for that dependency's
bounded lifetime. It cannot be silently dropped to satisfy a quota.

## 7. Immutability and capability proof

The runtime boundary must enforce:

```text
AcceptedVersion payload capability:
  read/traverse only
  no create, unlink, rename, truncate, write, chmod/chown mutation,
     mutable upper/work use, or destination placement beneath it

Workspace/materialization capability:
  private runtime-effect-owned mutable scope
  not accepted truth
  not addressable through VersionId
  deleted through runtime cleanup, not Version retirement
```

Permission bits alone are not sufficient if a more privileged ambient path can
reopen the accepted payload writable. Phase 03 must combine capability/path
separation, API/module boundaries, qualified mount/access flags where used,
and mutation-trap tests.

## 8. Visibility and linearization

Runtime activation does not change selected-Version truth and adds no Head
linearization point.

- Read safety point: bounded custody is installed relative to retirement before
  immutable access is handed off.
- Immutable activation readiness: the existing runtime owner declares its
  private mount/namespace/runtime handle usable after its selected complete
  setup; this is not durable Version visibility.
- Private materialization readiness: only after every entry and byte is copied,
  validated, and the selected runtime-private readiness operation completes may
  a Workspace handle escape. Exact private rename/fence mechanics are Phase
  03/runtime-owned and are not claimed here.

The sole selected Head point remains conditional complete Head-record
replacement under LayerStack-0 transition authority.

## 9. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal immutable | Install custody, hand read-only access to runtime owner, keep accepted payload immutable, release custody with handle lifecycle. |
| Normal materialization | Stream one complete private destination within budgets, verify, expose it once, and keep accepted truth unchanged. |
| Concurrent readers | Each bounded custody/handle is tracked; aggregate readers, FDs, workers, and mounts remain capped. |
| Concurrent materializations | Independent private destinations and reservations; no shared mutable upper/work or accepted payload mutation. |
| Retry | Allocate/revalidate a new private transaction or resume only from a recognized Phase 03-selected state; never trust an arbitrary partial destination. |
| Cancellation before readiness | Expose no handle; close resources, release custody when safe, remove or debt-charge private work. |
| Cancellation after readiness | Transfer responsibility to the returned runtime handle/lifecycle; do not delete a live Workspace underneath its owner. |
| Crash | Accepted payload remains truth; startup/runtime reconciliation removes or resumes only recognizable private transactions in bounded batches. |
| Cleanup | Existing runtime owners unwind namespace/mount/process effects, delete private materializations, release custody, and report bounded debt. |

## 10. Finite resource accounting and complexity

Let:

- `E` be accepted filesystem entries;
- `V_read` be accepted payload bytes actually read;
- `V_write` be private destination bytes written;
- `V_copy` be separately reported logical/physical copy-offload bytes, if any;
- `Ops_act` be traversal, metadata, mount, namespace, and activation operations;
- `w` be bounded copy workers;
- `b` be each worker's bounded buffer;
- `e_batch` be bounded entry/metadata batch state;
- `M_fixed` be fixed runtime/tool state;
- `S_dest` be conservative destination allocation including metadata/sparse
  policy;
- `L_custody` be bounded custody lifetime/wait effects.

| Path | Worst-case time | Payload I/O | Peak additional resources |
|---|---:|---:|---:|
| Protected activation setup | `O(Ops_act + L_custody)` | eager complete-payload copy `0`; setup may read bounded metadata | `O(M_fixed + e_batch)`, bounded FDs/mounts/workers |
| Runtime use after protected activation | `O(V_read + Ops_runtime)` over actual use | accepted reads `V_read`; private writes separately owned | bounded runtime buffers/custody |
| Full private materialization | `O(E + V_read + V_write + Ops_act + L_custody)` | reads `V_read`, writes `V_write`, reports `V_copy` separately | `O(w*b + e_batch + M_fixed)` memory, `O(S_dest)` disk |
| Failure/cancel cleanup | `O(E_partial + filesystem_reclaim(S_partial))` | no accepted writes; private deletion cost implementation-dependent | bounded cleanup batch/debt |

For a complete byte-for-byte private materialization, `V_read` and `V_write`
are each normally proportional to logical payload `V`, subject to sparse-file,
metadata, compression, and filesystem allocation policy selected and reported by
Phase 03. The algorithm never requires `O(V)` RAM; streaming peak memory is
bounded by `O(w*b + e_batch + M_fixed)`.

Reference-only `0/0/0` does not apply here. Materialization must expose its
nonzero byte terms honestly. All memory, destination space, FDs, workers,
mounts/namespaces, custody, time, and debt are reserved/capped. Exhaustion fails
before runtime readiness and preserves accepted truth.

## 11. Optional optimizations

A qualified filesystem may permit a reflink, clone, copy-offload, cache, or
snapshot-like acceleration only if all of the following hold:

- complete-Version payload remains sole accepted readable truth;
- correctness is identical when the optimization is unavailable or fails;
- no optimization artifact becomes identity, reference authority, or durable
  reconstruction dependency;
- source immutability and private-destination mutation isolation are proven;
- continuing source dependency remains under custody;
- byte/copy-offload/space accounting remains explicit; and
- the supported-filesystem contract and fallback are qualified.

Therefore R0 is not reflink-backed truth and does not claim universal kernel
zero-copy.

## 12. Security and path validation

- Traverse beneath immutable source and private destination capabilities; use
  no caller-composed absolute path and follow no ambient symlink.
- Revalidate relative paths, depth, entry type, links, metadata, sparse extents,
  device/special-file policy, ownership mapping, xattrs, and executable bits
  under the selected portable/runtime profile.
- Prevent source/destination aliasing, hard-link escape, mount crossing, TOCTOU
  replacement, destination prepopulation, and writes through privileged ambient
  handles.
- Apply checked arithmetic to sizes/offsets/allocations; bound decompression,
  sparse expansion, metadata amplification, and error/log contents.
- Keep secrets, file content, and raw paths out of metrics. Runtime owners must
  enforce namespace/exec security separately from Version identity.

## 13. Observability and demonstration seams

Separate scopes must report custody acquire/release/age, activation mode,
entries traversed, `V_read`, `V_write`, `V_copy`, metadata operations, buffer and
RSS high-water marks, destination allocation, FDs, workers, mounts/namespaces,
readiness latency, cancellation side, partial cleanup, and debt.

Required tests include:

- immutable mutation traps through every runtime handle and privileged fallback;
- full tree/content/metadata projection for materialization;
- small-file, large-file, sparse, deep-tree, link, and unsupported-entry cases;
- exact memory-bound validation across `V >> memory_budget`;
- FD/worker/mount/disk/deadline/debt exhaustion and backpressure;
- concurrent readers/materializations and last-custody retirement race;
- cancellation/crash at each entry/buffer/readiness boundary;
- optional-optimization failure followed by correct bounded fallback; and
- counters proving reference operations stay `0/0/0` while this scope reports
  every actual runtime payload byte.

Observers cannot keep a Version alive, create/release custody, make a Workspace
ready, authorize exec, or declare a private destination accepted truth.

## 14. Details owning phases may still select

Phase 03 and runtime owners select exact payload handles, custody lifetime,
traversal order, portable-to-runtime metadata mapping, private transaction and
readiness mechanics, buffer/worker/FD limits, sparse policy, supported
filesystems, cleanup, and optional accelerators. Phase 06 selects workloads,
measurement tools, and targets.

No choice may mutate an accepted payload, make runtime-private facts Version
identity, require an optimization for correctness, add another selected writer,
or hide materialization costs under the reference zero-payload claim.

## 15. `REOPEN_PHASE_01` conditions

Return `REOPEN_PHASE_01 — <specific architecture-changing failure>` if:

- accepted payloads cannot be exposed immutably to existing runtime owners;
- bounded custody cannot close the read/retirement race;
- a required runtime operation necessarily mutates the accepted payload or
  requires it as mutable upper/work state;
- complete private materialization cannot be bounded/fail-closed within a
  selected hard target and no protected activation or within-R0 repair suffices;
- runtime handoff requires a new durable service/writer or different truth; or
- an optional accelerator must become required correctness or durable identity.

Traversal, buffer, mount, metadata-mapping, and optimization choices remain
`OPEN_WITHIN_R0` unless they prove one of these exact failures.
