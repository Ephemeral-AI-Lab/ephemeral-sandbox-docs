# 03.01 — Read custody and runtime handoff

## 1. Purpose and owning phase

**Owners:** Phase 03 LayerStack-0 owns accepted-reference capture, immutable
payload access, and retirement coordination; existing runtime-effect owners own
Workspace, OverlayFS, mount, namespace, exec, and manager/daemon lifecycle.  
**Purpose:** Capture one AcceptedBinding stably, hold bounded runtime-local read
custody so its complete payload cannot retire, then hand immutable access to the
existing runtime owners without moving runtime facts into Version identity.

Reference capture itself remains metadata-only. Runtime activation or
materialization may read/copy payload bytes and is accounted separately from
the reference-only EphCoW claim.

## 2. Evidence status

- `SOURCE-VERIFIED`: the sealed e497 source assigns Workspace/OverlayFS/mount/
  namespace/exec effects to existing runtime packages and manager/daemon
  lifecycle owners; those effects are downstream of the selected low-level
  LayerStack package.
- `SPIKE-VERIFIED`: none; V2 custody, immutable-handle enforcement, retirement
  races, and activation accounting have not been executed.
- `INFERRED`: serialized custody capture plus immutable downstream access closes
  Head-move and last-root races within R0.
- `OPEN`: Phase 03 selects custody representation, payload-handle shape,
  supported filesystem/mount protections, finite reader limits, and crash
  reconciliation. Runtime phases qualify actual activation mechanics.

## 3. Contract

Conceptual names express responsibility and type flow, not selected Rust
signatures, handle types, or mount commands.

### Inputs

- One of:
  - a typed Head selector;
  - a typed Root key; or
  - an AcceptedBinding already in caller custody and permitted at the API seam.
- Requested immutable access purpose and bounded lifetime context.
- Finite custody, descriptor, memory, worker, mount/materialization, and runtime
  lifecycle budgets.

### Preconditions

1. Any application authorization/disclosure check required for the read has
   occurred at the application seam.
2. The reference record and AcceptedBinding are LayerStack-0-readable,
   generation-valid, and within supported limits.
3. The store is ready and retirement/recovery share the same transition
   authority used during capture.
4. The runtime owner can accept an immutable source capability rather than a
   caller-supplied host path.
5. Capacity is reserved for one custody entry and its maximum runtime lifetime.

### Outputs

Success returns `CapturedVersionRead` containing:

- the exact captured AcceptedBinding;
- a bounded, non-forgeable read-custody token visible to retirement authority;
- immutable payload access scoped to that custody; and
- accounting context for all runtime payload reads/materialization.

The token is runtime/local lifecycle state, never portable identity, a Root,
selection truth, or an AcceptedBinding.

### Typed outcomes

| Outcome | Meaning |
|---|---|
| `ReadCaptured(captured)` | Binding revalidated and custody acquired before immutable payload access. |
| `InvalidReference` | Head/Root/binding is malformed, forged, wrong-generation, or unsupported. |
| `DanglingOrRetired` | Binding does not name a currently accepted non-retired closure. |
| `CustodyLimitExceeded` | Reader count, duration, FDs, memory, workers, or reconciliation debt has reached its finite bound. |
| `PayloadUnavailable` | Immutable payload access could not be opened after capture; custody is released and the read fails. |
| `RuntimeActivationFailed` | Runtime owner could not create the isolated Workspace/mount/namespace/exec environment. Accepted payload remains unchanged. |
| `Cancelled` | Cancellation occurred before handoff or during runtime work; cleanup releases effects and custody in order. |
| `StoreNotReady` | Recovery, corruption, filesystem qualification, or migration fencing prevents safe access. |

## 4. Capture algorithm

```text
capture_version_read(reference, purpose, budget):
    validate typed reference and reserve one bounded custody slot
    acquire sole LayerStack-0 transition gate

    resolved_binding := if reference is a typed Head/Root key:
                            read and validate its one complete record;
                            if invalid, release gate/reservation;
                                return InvalidReference
                            use record.binding
                        else:
                            validate supplied AcceptedBinding at its allowed seam
                            if malformed, release gate/reservation;
                                return InvalidReference
                            use supplied binding
    binding := LayerStack0Admission.revalidate_existing_binding_metadata(
                   resolved_binding)
    if binding does not name a complete accepted, non-retiring Version:
        release gate/reservation; return DanglingOrRetired

    custody := install bounded runtime-local custody(binding, purpose, lifetime)
    if installation fails:
        release gate/reservation; return CustodyLimitExceeded
    # This step is serialized with retirement's final revalidation.
    release transition gate

    immutable_access := open accepted closure through read-only payload API
    if open fails:
        release_custody(custody)
        return PayloadUnavailable

    return ReadCaptured(binding, custody, immutable_access, accounting_context)
```

The resolved Head may change immediately after the gate is released. The read
still names the captured binding; it is never redirected to a new Head.
Retirement cannot pass its final no-custody check for this binding until custody
is released.

### Custody release

```text
release_version_read(captured):
    runtime owner stops exec and detaches/destroys mutable Workspace effects
    close immutable payload access
    acquire transition authority or Phase 03-selected equivalent serialization
    remove exactly this custody entry
    release authority
    report cleanup debt if any runtime effect cannot yet be reclaimed
```

Custody is finite and tied to actual lifecycle. It is not a persistent Root and
does not keep a Version reachable after the reader has ended.

## 5. Runtime handoff

```text
activate_workspace(captured, runtime_request, runtime_budget):
    require captured custody is live and binding unchanged
    pass immutable source capability, not identity-bearing host paths,
        to the existing runtime-effect owner

    runtime owner:
        reserve bounded activation/materialization resources
        create isolated mutable Workspace state
        expose accepted source only through enforced read-only access
        if OverlayFS is used, accepted bytes may be a qualified read-only source;
            they are never writable lower data, never upper data, and never work data
        create mount and namespace effects without adding them to Version identity
        execute under manager/daemon lifecycle ownership

    return RuntimeWorkspaceHandle owned by runtime, paired with custody
```

Accepted payloads may never become mutable lower, upper, or work storage. A
runtime may use accepted bytes as a protected read-only source, or materialize a
separate runtime-private copy/view if required. Any mutable data is a separate
isolated Workspace effect. Capturing that Workspace later produces a new
Candidate and follows ordinary identity/admission; it never edits the accepted
source.

## 6. Visibility and linearization

This algorithm does not mutate a Head or Root and has no durable reference
visibility point.

The read-capture linearization point relative to retirement is the successful
installation of custody for the revalidated binding while the shared
transition/retirement authority is held. Before it, retirement may win and the
read returns `DanglingOrRetired`; after it, retirement must observe custody and
defer.

Runtime activation becomes visible only to the runtime owner at its qualified
Workspace/mount lifecycle point. That point is not Version selection,
admission, identity, or Head publication.

## 7. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal | Resolve one complete reference, acquire custody, open immutable access, hand it to existing runtime owners, then release effects and custody in order. |
| Concurrent Head move | Capture sees either the complete prior or complete new binding. Its custody pins exactly what it saw; later Head changes do not redirect it. |
| Concurrent last Root removal/retirement | Capture and final retirement revalidation serialize. Either custody installs first and retirement defers, or retirement wins and capture fails before opening payload. |
| Retry | A failed pre-capture attempt may retry. A successful capture has a unique bounded custody token; duplicated retries must not leak or double-release custody. |
| Cancellation before handoff | Close access if opened and release custody. No Workspace effects remain. |
| Cancellation during runtime | Stop/detach runtime effects, close payload access, then release custody; unresolved runtime cleanup is bounded debt and may keep custody conservatively. |
| Crash | Process/runtime lifecycle death invalidates handles only through the Phase 03-qualified reconciliation protocol. Startup fails closed or conservatively retains custody until manager/daemon effects are proven gone. |
| Cleanup | Runtime effects are reclaimed by their existing owners; LayerStack-0 removes custody only when immutable access can no longer occur. |

Unknown or corrupt custody state is conservative: block retirement/readiness or
quarantine the affected Version within bounds. It must not guess that no reader
exists.

## 8. Finite resource accounting and complexity

Let:

- `R_ref` = bounded reference/acceptance metadata bytes;
- `Q` = active read-custody population, capped by `Q_max`;
- `V_read` = accepted payload bytes actually read by runtime activation/exec;
- `V_copy` = payload bytes materialized into a separate runtime-private view;
- `M_act` = runtime metadata/mount operations;
- `F_read` = descriptors/handles retained by the captured read; and
- `T_read` = maximum custody lifetime or cancellation/reconciliation policy.

| Operation | Time | Data I/O | Space/resources |
|---|---:|---:|---:|
| Capture binding + custody | `O(1)` plus bounded gate wait | `O(R_ref)` metadata; payload bytes `0` | one custody entry, bounded record buffer, finite descriptors |
| Open immutable source | `O(1)` metadata/handle work under qualified filesystem | payload data read `0` until consumed | `F_read`, custody retained |
| Runtime activation/materialization | `O(V_read + V_copy + M_act)` worst case | reads `V_read`; may write/copy `V_copy` only into runtime-private Workspace/view | runtime budget for memory, disk, FDs, workers, mounts/namespaces |
| Release | `O(1)` LayerStack-0 custody work plus runtime-owner cleanup | metadata/cleanup I/O; accepted payload write `0` | releases one custody entry; unresolved effects charged as debt |

Reference-only capture counters remain payload `0/0/0`. Runtime activation
must use different operation scopes/counters so its legitimate payload reads or
copies cannot be hidden by the reference claim.

At `Q_max`, FD/memory/worker/disk limits, or custody-lifetime/reconciliation
bounds, new reads fail or backpressure. Cancellation and cleanup loops operate
in finite batches. A bound is never bypassed by dropping custody early.

## 9. Security and path obligations

- Resolve only typed Head/Root keys and revalidated AcceptedBindings. Reject raw
  IDs, caller paths, stale generations, invalid checksums, and forged custody.
- Acquire payload access from an anchored LayerStack-0 handle after custody;
  never reopen a caller-supplied host path or follow a mutable symlink to find
  the accepted closure.
- Expose no writable handle to accepted payload objects. Deny write, truncate,
  rename, unlink, metadata mutation, writable mapping, or mutable mount access
  through every downstream API.
- Treat the runtime Workspace as untrusted mutable output. Namespace/mount
  confinement and OverlayFS validation remain runtime-owner duties, with
  explicit lower/source read-only checks and private upper/work locations.
- Keep mount IDs, namespace IDs, device/inode allocation, host paths, custody
  tokens, sessions, and process facts outside canonical identity.
- Bound runtime request data, environment, descriptors, worker count, output,
  time, and cleanup. Avoid leaking accepted file contents or host paths in
  diagnostics.

## 10. Observability and test seams

Required diagnostic facts include capture outcome, binding/version-safe label,
custody count/age/purpose class, gate wait, immutable-open outcome, activation
bytes read/copied/written, runtime metadata operations, cleanup duration/debt,
and attempted accepted-payload mutation.

Required tests:

- Head move concurrent with capture yields a stable prior-or-new binding;
- capture races final Root removal/retirement without use-after-retire;
- custody limit, cancellation at each boundary, runtime activation failure, and
  process/manager restart fail closed;
- all payload write/truncate/rename/unlink/mutable-map attempts are rejected;
- accepted source is never used as upper/work or any mutable location;
- capture/reference counters assert payload `0/0/0`;
- activation counters separately show actual reads/copies/materialization; and
- releasing the last custody permits retirement only after exact Head/Root
  revalidation.

Observability cannot synthesize custody, keep a Version reachable, open a
payload, or approve retirement.

## 11. Details owning phases may still select

Phase 03 selects exact custody data structure, process/restart representation,
immutable payload accessor, lock serialization, limits, supported filesystem,
and recovery integration. Runtime phases select qualified Workspace/OverlayFS/
mount/namespace/exec mechanics and activation accounting.

These choices may not make runtime facts portable identity, give runtime owners
AcceptedBinding authority, make accepted payload mutable, or combine runtime
activation byte costs with the zero-payload reference claim.

## 12. `REOPEN_PHASE_01` conditions

Reopen Phase 01 with the exact failure if:

- bounded read custody plus final serialized retirement revalidation cannot
  prevent use-after-retire;
- runtime activation necessarily mutates an accepted payload or requires it as
  writable lower/upper/work storage;
- the existing direct LayerStack-0 to runtime-effect handoff cannot provide
  immutable access without a new authority or process boundary;
- correct Version identity requires mount, namespace, Workspace, host-path,
  session, or custody facts; or
- runtime payload I/O cannot be separated from and prevented on reference-only
  operations.

Custody representation and activation mechanics that preserve these boundaries
remain `OPEN_WITHIN_R0`.
