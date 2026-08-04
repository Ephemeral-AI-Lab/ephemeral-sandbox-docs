# R0 ownership and boundaries

Date: **2026-08-04**  
Status: **`LOCKED_PHASE_01`**  
Decision: [ADR-001 — R0 LayerStack-0 Version storage](decisions/ADR-001-r0-complete-version-storage.md)

## Purpose and authority

This document turns the selected ownership portion of the root
[architecture design](../architecture_design.md) into an implementation-facing
contract. It does not perform another architecture selection. The selected
result is R0: rewrite the existing `sandbox-runtime-layerstack` ownership home
as LayerStack-0 filesystem-native immutable complete-Version storage while retaining the
current application, effect, lifecycle, and diagnostic owners.

Authority descends from the product [PRD](../PRD.md), completed Phase 00
[SPEC](../phases/00-freeze-rules/SPEC.md), Phase 01
[selection contract](../phases/01-choose-design/SPEC.md), and the selected root
[architecture](../architecture_design.md). This file is subordinate to those
sources. A conflict is resolved in favor of the higher-authority source and is
not repaired by silently changing R0 here.

The ownership map, dependency direction, one-writer model, portable/runtime
boundary, and zero-new-boundary decision are `LOCKED_PHASE_01`. Exact internal
module names may move inside the selected package without changing authority.
The exact codec/hash and disk/fence details remain bounded Phase 02 and Phase
03 decisions respectively.

## Selected authority map

| Responsibility | Selected owner and source home | Authority it holds | Authority it must not hold |
|---|---|---|---|
| Portable Version identity | Pure internal module at `crates/sandbox-runtime/layerstack/src/identity.rs` or `src/identity/**` | Validate complete portable facts, produce canonical bytes and typed `VersionId`, support exact comparison | Durable publication, auth, runtime paths, mounts, migration policy, application retries |
| Selected-Version truth | Existing `crates/sandbox-runtime/layerstack` package (`sandbox-runtime-layerstack`), rewritten as LayerStack-0 | Accepted immutable payloads, `AcceptedBinding` values, typed Roots/Heads, OCC transition, reads, recovery, retirement, cleanup | User authorization, public operation semantics, writable Workspace ownership, command execution, MCTS/rollout policy |
| Store implementation | Internal `crates/sandbox-runtime/layerstack/src/store/**`; existing `src/storage/{fs.rs,lock.rs}` rewritten where useful | Candidate admission, exact occupied-ID comparison, payload-before-reference durability, exclusive transition gate | A second public authority, service protocol, application orchestration, runtime-effect implementation |
| Application authorization and ordering | Existing `crates/sandbox-runtime/operation` services in `sandbox-runtime` | Auth/revoke and request ordering, expected-head capture, candidate orchestration, typed error/API mapping, store-call orchestration | Direct writes to store-owned payload/root/head paths, collision acceptance, bypass of store OCC |
| Writable Workspace custody | `crates/sandbox-runtime/workspace` and workspace-manager owners | Candidate upperdir/live generation, bounded capture, Workspace lifecycle effects | Portable identity policy, selected durable Head, accepted-payload mutation |
| OverlayFS and mount effects | `crates/sandbox-runtime/overlay` and current Workspace integration | Runtime materialization/mount effects and host-local paths | Portable identity or durable selected-Version authority |
| Namespace and execution effects | `crates/sandbox-runtime/namespace-process`, `crates/sandbox-runtime/namespace-execution`, and current exec owners | Runtime namespace/process/command effects | Portable identity, durable root/head writes, rollout policy inside storage |
| Sandbox/process lifecycle | Existing `sandbox-daemon` and `sandbox-manager` owners | Process composition, readiness integration, provisioning, shutdown, cutover fencing | A second Version representation or writer |
| Diagnostics and audit projections | `crates/sandbox-observability/query`, `crates/sandbox-observability/telemetry`, and the application-owned auditability side channel under `crates/sandbox-runtime/operation/src/file/` | Read-only diagnostics, counters, audit projections | Selected-Version publication, identity admission, truth reconstruction |
| Legacy import | Temporary store-local `legacy_import` module/feature/target, invoked through existing `crates/sandbox-manager`, `crates/sandbox-daemon`, and `crates/sandbox-provider-docker` lifecycle/provisioning paths as needed | Decode one fenced legacy selected view and call ordinary V2 admission/reference APIs | Permanent V2 dependency, alternate V2 format, dual writes, unfenced legacy mutation |

The first source disposition is maintained in the root architecture's
[source placement table](../architecture_design.md#4-source-placement-and-disposition).
Phase 00's full measured package census remains in
[inventory-packages.md](../phases/00-freeze-rules/inventory-packages.md); this
document repeats only boundaries needed to implement R0.

## Selected-Version truth

Selected truth consists of:

- one complete immutable payload closure per accepted canonical Version and
  `VersionId`;
- valid durable heads containing an accepted binding and monotone
  `HeadRevision`;
- valid typed roots naming accepted bindings; and
- the active store generation that grants write authority.

Selected truth does **not** include a logical layer chain, parent pointer,
depth, squash result, merge result, writable workspace, runtime mount, audit
projection, observability cache, migration progress record, or raw digest
supplied by a caller.

The application may decide that an authorized operation should be attempted.
It cannot declare a payload accepted or make a root/head durable. Runtime-effect
owners may construct and capture a candidate. They cannot write the store's
accepted payload, root, or head namespaces directly.

## Single-writer and linearization rule

There is exactly one selected-Version transition authority: the rewritten
`sandbox-runtime-layerstack` store.

Candidate validation, canonicalization, hashing, and private staging may run
outside the final transition gate and may be concurrent subject to finite
limits. Physical acceptance of an occupied/new identity and every durable
root/head change are store operations. The store's process/filesystem-exclusive
gate serializes final selected-reference validation and change.

For a head publication:

1. the application authorizes and orders the request;
2. the application captures the expected `(AcceptedBinding, HeadRevision)` and calls
   the store;
3. the store admits or reuses an exact candidate payload before publication;
4. under its exclusive transition gate, the store rereads the expected head;
5. a mismatch returns stale without merge or rebase; and
6. one atomic complete head-record replacement is the sole OCC linearization
   point.

No application, workspace, manager, daemon, provider, migrator, or
observability component may bypass that transition. A store-created or
store-revalidated accepted binding is the capability admitted to a
reference-only operation; an unchecked raw digest is not.

The writer model assumes one local process/filesystem-exclusive transition
gate. A requirement for multi-host active/active writers, a separately
privileged Version writer, or an independent store crash domain is not an
internal Phase 03 detail—it reopens Phase 01.

## Dependency direction

The allowed architectural direction is:

```text
daemon / manager / API adapters
             |
             v
sandbox-runtime application and operation services
      |                         |
      v                         v
sandbox-runtime-layerstack   workspace / overlay / namespace / exec owners
      |
      v
pure internal identity module + low-level filesystem/lock/hash/codec libraries
```

The following directions are forbidden:

- store → application auth, API policy, audit policy, or rollout/MCTS policy;
- store → workspace, OverlayFS, namespace, or exec implementation;
- identity → store, workspace, manager, provider, observability, mount, or
  host-runtime adapter;
- runtime-effect owner → direct durable payload/root/head mutation;
- observability/audit → selected-Version write or identity authority;
- permanent identity/store code → temporary legacy-import types;
- one application package → another application package merely to reach the
  store; and
- a second crate/service/database/coordinator → selected truth without a new
  joint architecture decision.

Direct consumers may continue to depend on the existing low-level LayerStack
package while its public model is incrementally rewritten. Temporary source
coexistence needed to keep e497 consumers compiling does not permit two
writable runtime truths.

## Process, privilege, and trust boundaries

### Process boundary

The store remains an in-process low-level library. R0 adds no daemon, helper
process, RPC protocol, deployment unit, queue, independent retry loop, or
independent crash domain. Manager and daemon lifecycle owners compose the
library as they do other runtime capabilities.

### Privilege boundary

Existing workspace, mount, namespace, and execution owners retain their
runtime privileges. Persisting portable facts does not grant the store mount,
namespace, container, or command-execution authority. The store operates on
its configured local store root using Phase 03-qualified filesystem
primitives.

If safe capture requires a runtime owner to supply descriptors or validated
facts, that is a typed input boundary rather than permission for the store to
adopt the runtime effect or for host paths to enter identity.

### Trust boundary

The following are untrusted until validated by their selected owner:

- candidate facts and contents;
- paths, entry types, metadata, link targets, sizes, and counts;
- caller selectors and root identifiers;
- raw Version IDs;
- legacy import input; and
- persistent bytes read during startup/recovery.

The store alone promotes validated exact content to an accepted binding.
Corrupt, dangling, ambiguous, unsupported-version, over-limit, or
excessive-recovery-debt input fails closed.

### Diagnostic boundary

Observability receives bounded read-only projections and counters. It may
report payload I/O, admissions, stale outcomes, collisions, roots/heads,
custody, staging, debt, and readiness failures, but these projections are not
inputs to selected-Version correctness. Missing diagnostic data cannot be
interpreted as store truth.

## Portable identity versus runtime-private effects

The identity module receives complete portable filesystem facts. Phase 02
selects their exact schema, but the boundary is already fixed.

Portable identity must exclude:

- Docker images and container identifiers;
- OCI descriptors or runtime configuration;
- OverlayFS lower, upper, work, or merged paths;
- mount identifiers, options, or handles;
- namespaces, process IDs, cgroups, file descriptors, and local handles;
- host absolute paths, store paths, workspace/session IDs, and provider
  bindings;
- leases, active read custody, auth, audit, rollout, or policy data; and
- legacy layer IDs, parents, depth, squash, merge, or whiteout-as-delta facts.

Read custody, materialized read-only paths, live workspace paths, mounts, and
execution handles remain runtime-local effects. None can change the canonical
meaning of an accepted Version.

## Package and module disposition

| Disposition | Path | Ownership consequence |
|---|---|---|
| `KEEP` | `crates/sandbox-runtime/layerstack/Cargo.toml` | Retain the dependency-neutral package as the sole store owner. |
| `REWRITE` | `crates/sandbox-runtime/layerstack/src/lib.rs` | Export narrow V2 identity/store operations and retire permanent layer semantics. |
| `REWRITE` | `crates/sandbox-runtime/layerstack/src/model/**` | Replace layer DTOs with portable facts, typed identity, accepted binding, roots, heads, and revisions. |
| `ADD` internal | `crates/sandbox-runtime/layerstack/src/identity.rs` or `src/identity/**` | Pure identity module; no new authority or package boundary. |
| `ADD` internal | `crates/sandbox-runtime/layerstack/src/store/**` | Store mechanics under the existing authority. |
| `REWRITE` | `crates/sandbox-runtime/layerstack/src/storage/{fs.rs,lock.rs}` | Reuse/adapt the current primitive family to prove V2 durability and exclusivity. |
| `DELETE` from permanent V2 path | `src/stack/**`, layer manifests/refs/changes, parent chains, depth, merge, squash, delta/whiteout truth, and durable layer leases | Prevent legacy reconstruction or a hidden second truth. |
| `DELETE`/`REWRITE` | `src/workspace_base/**` | Replace layer-specific binding with complete-Version admission or temporary import. |
| `KEEP`/`REWRITE` | `crates/sandbox-runtime/operation` | Retain application authority; remove autosquash, silent merge/rebase, and layer-depth policy from V2 wiring. |
| `KEEP`/`MOVE` | Workspace/workspace-manager packages | Retain effects; move durable selected-Version decisions and legacy layer leases to the LayerStack-0/application seam. |
| `KEEP`/`REWRITE` | Manager, provider-Docker, and observability consumers | Consume accepted bindings or temporary import APIs; never own V2 truth. |
| `ADD`, temporary | Store-local `legacy_import` module/feature/target | One-way importer, removable with all migration-only callers/config/tests/types. |

`ADD internal` does not mean a new architectural boundary. The selected count
of new crates, services, processes, facades, registries, coordinators,
databases, or separately governed resource/lifecycle domains is **zero**.

## Open product decisions and stable seams

No product-owner decision is accepted by this document.

| Decision | Status | Stable R0 seam | Expansion that reopens Phase 01 |
|---|---|---|---|
| `DEC-001` — keep exact `file_blame` or accept a break | **`OWNER_DEC_OPEN`** | Application-owned auditability may key side-channel records by accepted Version/revision/publication; provenance is not canonical selected truth. | Requiring provenance/audit history to become canonical payload identity or selected-Version truth. |
| `DEC-011` — cutover observation duration | **`OWNER_DEC_OPEN`** | Changes only when temporary import compatibility is deleted; it never permits two writable truths. | Requiring legacy and V2 to remain writable together or permanent legacy decoding in the store core. |
| `DEC-017` — no-session write/edit and exact V2 file-operation/target set | **`OWNER_DEC_OPEN`** | The application may reject a sessionless mutation or build a bounded candidate and call ordinary publish/OCC; accepted payloads are never edited. | Requiring direct in-place mutation of accepted payloads or another writer/representation. |
| `DEC-018` — auth/revoke ordering under races | **`OWNER_DEC_OPEN`** | Application owns the accepted-request/revocation cutoff and disclosure policy; the store always applies independent OCC. | Requiring joint durable auth/store authority or another store linearization/writer. |

The complete register is in [decisions/README.md](decisions/README.md). Older
appendix DECs remain proposal/open evidence and are not accepted by reference.

## Boundary-change test

A proposed implementation change stays inside R0 only if all answers below are
“no”:

1. Does it move selected-Version truth out of `sandbox-runtime-layerstack`?
2. Does it move auth/order into the store or durable truth into an effect owner?
3. Does it add a store writer, linearization point, process, service, database,
   crate-level authority, or independent lifecycle/resource domain?
4. Does it move runtime-private facts into portable identity?
5. Does it replace complete immutable payload truth with a layer, archive,
   object-DAG, database, or other storage family?
6. Does it change prior-or-complete-new crash behavior, exact occupied-ID
   comparison, reference-only zero-payload-I/O, or the one-writable-truth
   migration model?

If any answer is “yes,” stop implementation and reopen Phase 01 with the exact
R0 failure and the costs of the proposed boundary.

Ordinary internal module naming, codec/hash selection within the portable
contract, safe filesystem step refinement, finite constant selection,
instrumentation, and test seams do not reopen architecture when they preserve
all selected invariants.

## Reopening conditions

Phase 01 must be reopened if evidence shows any of the following:

- product/source drift changes package dependencies, write ownership,
  privilege custody, lock semantics, or source placeability;
- complete bounded portable identity requires runtime-private or layer-history
  facts;
- the selected filesystem family cannot prove payload-before-reference
  durability, exact occupied-ID comparison, one OCC point, reference-only
  zero-payload-I/O, captured reads, or bounded last-root retirement;
- a safe design requires multi-host active/active writers, a privileged helper,
  new service/database/coordinator, or a different recovery authority;
- migration requires dual writes, permanent legacy dependency, or making
  legacy writable after V2 becomes authoritative; or
- an owner decision expands authority beyond its stable seam above.

Until a reopening condition is proved, Phases 02–08 implement and verify this
ownership map rather than selecting another one.

## References

- [Product PRD and hard rules](../PRD.md#hard-rules-must-never-break)
- [Selected whole-program architecture](../architecture_design.md)
- [Phase 00 evidence](../phases/00-freeze-rules/SPEC.md)
- [Phase 01 selection contract](../phases/01-choose-design/SPEC.md)
- [Phase 01 completed plan](../phases/01-choose-design/PLAN.md)
- [ADR-001](decisions/ADR-001-r0-complete-version-storage.md)
