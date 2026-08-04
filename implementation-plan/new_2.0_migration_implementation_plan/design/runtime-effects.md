---
status: draft-challenger-laws
authority: existing-runtime-effect-owner-laws
depends-on:
  - ARCH-BND-003
  - ARCH-BND-004
  - ARCH-BND-006
  - REQ-COR-009
  - REQ-RES-010
  - REQ-PORT-002
  - REQ-PORT-003
  - REQ-PORT-004
---

# Existing runtime-effect owner laws

## No aggregate Backend

R0 adds no `WorkspaceBackend` component, API, trait, facade, package, service,
factory, registry, plugin layer, RPC, sidecar, or deployable. “Backend” is not a
new aggregate authority.

Phase 1 inventories and reuses the current owners of workspace lifecycle and
capture, OverlayFS primitives, namespace/process execution, live-file effects,
containment, disposal, and their local resource debt. Their exact
reason-to-change, effect-authority, component, package, process, call-edge, and
method counts remain `OPEN`. Existing application owners call only the
applicable current effect owner; no universal runtime interface is presumed.

The lack of an aggregate seam does not relax portability. Runtime-native values
remain behind their actual owners and may cross neither into selected identity
nor public/core values. The selected-state writer never calls a runtime-effect
owner, and no runtime-effect owner writes selected-state truth.

## Existing-owner map to verify

| Effect category | Current candidate owner | Required evidence |
|---|---|---|
| workspace allocation, realization, fence, stable capture, conflict retention, disposal | `sandbox-runtime-workspace` plus its existing application calls | generation binding, crash cuts, portable capture, synchronized cleanup |
| mount/filesystem primitive | `sandbox-runtime-overlay` | native containment and cleanup without leaking carrier facts |
| command/process/PTY effect | `sandbox-runtime-namespace-execution` and `sandbox-runtime-namespace-process` | exact generation routing, cancellation, ambiguity, descendants/helpers containment |
| live file effect | current runtime operation/workspace owners found by the Phase 1 call graph | bounded range/mutation behavior, symlink/path containment, partial-effect law |

This table is a search plan, not an accepted owner or component count. Phase 1
must correct it from source and executable traces.

## Required lifecycle effects

The fewest actual calls must prove all applicable effects:

- **RFX-LIFE-001 — hidden allocation.** Static compatibility and quota checks
  precede allocation. Data-dependent checks occur only inside a bounded,
  admitted, unreachable realization.
- **RFX-LIFE-002 — verified realization and activation.** One complete
  generation becomes reachable or none does. Failure is typed and synchronously
  cleaned; restart can determine the result.
- **RFX-LIFE-003 — writer fence and stable capture.** New mutation stops and
  in-flight effects drain or reject under the accepted contract before portable
  facts are captured from one exact generation.
- **RFX-LIFE-004 — conflict readability.** If product semantics retain a losing
  workspace, that exact generation remains bounded and read-only; it cannot
  resume mutation.
- **RFX-LIFE-005 — synchronized disposal.** Disposal is generation-bound and
  idempotent for the exact effect identity, cannot delete a replacement, and
  acknowledges only after process/device/filesystem and required parent-
  metadata cleanup.

Existing owners may fuse allocate/realize/activate or fence/capture calls when
all crash, cancellation, resource, and attestation laws remain provable. This
document selects no typestate, call count, native schema, or source-pass count.

## Values that may cross

Allowed values are bounded portable fact streams; opaque
profile/instance/allocation/generation/effect identities; bounded command/file
streams and cancellation; and typed support, completion, failure, ambiguity,
containment, and synchronized-cleanup evidence.

Forbidden cross-boundary values include selected-state locators, packs,
indices, selectors, physical handles, a runtime-selected `StateId`, native path
as public identity, mount/namespace/device/snapshot/provider identity, WASI or
VM handle, OCI value, and generic plugin objects. Capture emits portable facts,
not layers, whiteouts, native snapshots, host paths, or storage decisions.

## Commands and files

Commands, stdin, output reads, and live file effects target one authorized
active allocation generation, except explicitly accepted read-only access to a
retained conflict generation. Each operation freezes byte/entry bounds,
backpressure, cancellation, partial effect, ambiguity, output retention, and
cleanup.

`file_read` keeps its public name. Omitted `workspace_session_id` reads one
captured committed revision without a runtime effect. Supplied
`workspace_session_id` resolves the exact authorized live allocation generation
and calls its current file-effect owner. No `workspace_file_read` alias or
aggregate Backend dispatch is added. V2 `file_write` and `file_edit` target a
live workspace and never mutate selected immutable state.

## Effect ambiguity and retry

Every system-issued mutation is dispatched only after an accepted durable
owner records custody for the complete authenticated semantic request and exact
runtime generation. Automatic redispatch requires intrinsic idempotence or
exact generation-bound deduplication. Arbitrary command/file mutation is never
silently repeated.

A terminal `OutcomeUnknown` does not close runtime custody: the exact generation
stays fenced, charged, and quarantined until its actual owner proves synchronized
completion, failure, compensation, or containment. Time-based expiry,
retry-until-success, name-only disposal, and reuse of unresolved allocation are
forbidden. Runtime owners do not claim control over downstream external effects
initiated by guest code.

## Resource and containment law

Each runtime-effect owner admits and accounts only its own dimensions and
reconstructs only its own live debt. It sends no claim, census, handle, or debt
to the selected-state writer. Exact aggregate admission placement is open;
allocation cannot occur until all participating finite capacity is held.

Every accepted runtime profile proves a finite parent cgroup or equivalent for
the complete untrusted process tree, including descendants, helpers,
fork/clone/reparent/daemonization, escape prevention, memory/swap, overload,
restart, cancellation, and cleanup. Shared trusted helpers are independently
bounded and attributed. Passing the selected-state `8 MiB` and `64/96 MiB`
storage gates does not prove runtime containment, and vice versa.

An idle session/root holds no runtime allocation, mount, process, VM/WASI
instance, FD, worker, buffer, cache, queue slot, or permit. Cancellation,
failure, conflict, pruning, and restart return resources to the proved
synchronized plateau or retain an explicitly charged quarantine.

## Linux and future runtimes

Linux workspace/OverlayFS/namespace ownership is the first conformance subject.
Mounts, upper/work directories, namespaces, paths, whiteouts, and privileges
remain private. OCI is import/export only. Only a qualified runtime-internal
OverlayFS, native or VM snapshot, private storage-driver acceleration, or
deduplication hint may accelerate a runtime-private realization. Reflinks/clone
ioctls and FUSE remain prohibited in both enabled and disabled modes. Disabling
every eligible acceleration must preserve portable facts, identity, results,
admission, durability, cleanup, privilege, and capability.

WASI and Firecracker remain disposable conformance spikes. A failed spike may
classify the runtime unsupported. A second accepted implementation plus a
measured shared-contract/substitution need may justify changing ownership or
extracting one boundary, but future intent alone cannot add an enum, trait,
facade, plugin, package, service, or deployable.

## External rollout policy and qualification

MCTS/parallel rollout policy is not a runtime-effect scheduler. Existing owners
see only independently admitted active generations and exact effect identities.
Inactive checkpoint/fork roots hold no runtime resources; pruning disposes only
the exact generation and returns its local charges.

Phase 1 qualification covers supported facts/effects, static rejection,
bounded hidden-failure cleanup, fence/capture races, containment, crash/retry
ambiguity, activation/disposal, conflict retention, mixed load, and the idle
plateau. Phase 2 may cut over only the exact qualified artifact, then observe,
retire compatibility, requalify changed `H_RELEASE`, and release.
