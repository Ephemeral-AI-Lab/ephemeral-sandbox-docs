# Source and implementation map

**Status:** Phase 01 placement selected; later paths require source verification  
**Evidence base:** `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0`
at `e4974d1f9aac702b35e052629cb070c897989352`  
**Rule:** source coexistence during incremental compilation never permits two
writable runtime truths

## Purpose

Translate R0 into exact package ownership, source disposition, dependency laws,
phase sequencing and deletion boundaries. The Phase 00
[package inventory](../phases/00-freeze-rules/inventory-packages.md) and
[surface inventory](../phases/00-freeze-rules/inventory-surfaces.md) remain the
measured e497 census; this file states the selected V2 disposition.

Internal filenames marked as hypotheses may change without reopening Phase 01.
Changing the package owner, process boundary, dependency direction, storage
family, or writer count may not.

## Selected package graph

```text
crates/sandbox-daemon                      transport/composition
crates/sandbox-manager                     lifecycle/fleet/fence
crates/sandbox-runtime/operation            auth/order/product composition
  -> crates/sandbox-runtime/layerstack      selected-Version owner (R0 rewrite)
       -> identity internal module          pure portable facts/VersionId
       -> store internal modules            payload/root/head/durability
       -> low-level fs/lock/hash/codec libs
  -> crates/sandbox-runtime/workspace       writable workspace effects
  -> crates/sandbox-runtime/overlay         OverlayFS effects
  -> crates/sandbox-runtime/namespace-*     namespace/exec effects

crates/sandbox-observability/*              read-only diagnostic projection
crates/sandbox-provider-docker              provisioning/runtime effects
```

Allowed direction is consumer/application/effect/lifecycle/diagnostic code to
the selected store, and the store to pure identity plus low-level libraries.
Permanent identity/store code must not depend on application policy, runtime
effects, observability, provider code, or temporary import types.

## Permanent selected-Version owner

| Disposition | Product path | Phase | Required result |
|---|---|---:|---|
| `KEEP` | `crates/sandbox-runtime/layerstack/Cargo.toml` | 02–08 | Existing dependency-neutral package remains the LayerStack-0 selected-Version owner; no replacement storage crate. |
| `REWRITE` | `crates/sandbox-runtime/layerstack/src/lib.rs` | 02–04 | Export narrow V2 identity/store types and operations; stop exporting permanent V2 layer/squash/depth truth. |
| `REWRITE` | `crates/sandbox-runtime/layerstack/src/model/**` | 02–03 | Replace legacy manifest/layer DTO authority with portable facts, typed `VersionId`, accepted binding, head revision and typed root/head records. |
| `ADD` | `crates/sandbox-runtime/layerstack/src/identity.rs` or `src/identity/**` | 02 | Pure deterministic identity module; internal module, not a new authority. |
| `ADD` | `crates/sandbox-runtime/layerstack/src/store/**` | 03 | Payload, binding, root/head, admission, publication, read custody, recovery, retirement and cleanup internals. |
| `REWRITE` | `crates/sandbox-runtime/layerstack/src/storage/fs.rs` | 03 | V2 filesystem primitives for bounded private staging, immutable payload admission, atomic records and durability. |
| `REWRITE` | `crates/sandbox-runtime/layerstack/src/storage/lock.rs` | 03 | Exclusive selected-Version transition gate and documented lock ordering. |
| `DELETE` or isolate from V2 | `crates/sandbox-runtime/layerstack/src/stack/**` | 03–08 | No V2 read, write, recovery or fallback may reconstruct truth from parent layers, manifests, changes, merge, squash, depth or layer leases. |
| `DELETE`/`REWRITE` | `crates/sandbox-runtime/layerstack/src/workspace_base/**` | 03–05 | Replace layer-specific base binding with complete-Version admission/materialization or temporary legacy import. |
| `KEEP` only as thin facade if needed | `crates/sandbox-runtime/layerstack/src/service/**` | 03–04 | Must not preserve legacy authority or create another writer; delete if direct owner calls are smaller. |

Phase 02 adds identity incrementally and should not delete legacy APIs merely to
force all consumers to migrate early. Phase 03 establishes offline V2 truth;
Phase 04 rewires consumers; Phases 05–08 remove temporary/legacy paths in a
controlled order.

## Application and public-operation wiring

| Disposition | Product path | Phase | Required result |
|---|---|---:|---|
| `KEEP`/`REWRITE` | `crates/sandbox-runtime/operation/src/layerstack/service/**` | 04 | Retain application orchestration but call accepted V2 store contracts; no legacy manifest/layer authority. |
| `DELETE` from V2 wiring | `crates/sandbox-runtime/operation/src/layerstack/actions/squash.rs` | 04–08 | V2 complete Versions require no squash action. Compatibility-only reachability must be temporary and named. |
| `DELETE` | `crates/sandbox-runtime/operation/src/layerstack/autosquash_engine/**` | 04–08 | No background layer-depth/squash policy in V2. |
| `KEEP`/`REWRITE` | `crates/sandbox-runtime/operation/src/file/**` | 04 | Committed reads resolve captured immutable Versions; live writes/edits target workspace Candidates; preserve open `DEC-001`/`DEC-017` seams. |
| `KEEP`/`REWRITE` | `crates/sandbox-runtime/operation/src/workspace_session/**` | 04 | Session create/publish/destroy retain app ordering and effect ownership; publish uses V2 candidate admission/OCC. |
| `KEEP` | `crates/sandbox-runtime/operation/src/command/**` | 04 | Exec remains a runtime effect; automatic session publication uses the same V2 path. |
| `KEEP`/`REWRITE` | `crates/sandbox-runtime/operation/src/operations/registry/**` | 04 | Preserve catalog ownership; do not silently decide open public-surface DECs. |
| `KEEP`/`REWRITE` | `crates/sandbox-runtime/operation/src/services.rs` | 04 | Compose existing owners; remove autosquash/legacy store initialization only when replacement consumers compile. |
| `KEEP` | `crates/sandbox-operations/catalog`, `contract`, `client` | 04 | Adapter/public vocabulary remains outside storage. Surface changes require the owning product decision. |

The current 26 catalog operations plus daemon HTTP-only `file_list` are measured
legacy/current inventory, not permission to copy an older 26-row proposal or
silently resolve `DEC-017`.

## Runtime-effect owners

| Disposition | Product path | Phase | Required result |
|---|---|---:|---|
| `KEEP`/`REWRITE` | `crates/sandbox-runtime/workspace` | 04 | Own writable sessions, upperdirs, capture, remount and runtime recovery; supply bounded candidate facts without owning portable identity. |
| `KEEP` | `crates/sandbox-runtime/overlay` | 04 | Own OverlayFS operations; no mount/lower/upper/work path enters canonical identity. |
| `KEEP` | `crates/sandbox-runtime/namespace-process` | 04 | Own namespace/process lifetime only. |
| `KEEP` | `crates/sandbox-runtime/namespace-execution` | 04 | Own isolated command effects only. |
| `KEEP`/`REWRITE` | failed-holder recovery paths under workspace operation code | 04/06 | Recovery artifacts remain bounded runtime side effects and cannot become selected truth. |

The store may consume validated portable facts supplied through a narrow call,
but it must not call mount/namespace/exec implementations or acquire their
privileges.

## Lifecycle, provider and observability

| Disposition | Product path | Phase | Required result |
|---|---|---:|---|
| `KEEP`/`REWRITE` | `crates/sandbox-daemon` | 04–07 | Transport/dispatch/readiness only; enforce authorized app calls and cutover readiness without store algorithms. |
| `KEEP`/`REWRITE` | `crates/sandbox-manager` | 04–08 | Fleet lifecycle, create/destroy and generation fencing; no second selected-Version representation. |
| `KEEP`/`REWRITE` | `crates/sandbox-provider-docker` | 04–08 | Provisioning/container/volume effects; consume an accepted Version binding or temporary import inputs, never define portable identity. |
| `KEEP`/`REWRITE` | `crates/sandbox-observability/telemetry` | 04/06 | Emit bounded diagnostics; no selected-Version mutation. |
| `KEEP`/`REWRITE` | `crates/sandbox-observability/query` | 04/06 | Read bounded store projections/counters; legacy layer field compatibility must be temporary or explicitly changed. |
| `KEEP`/`REWRITE` | `crates/sandbox-config` | 02–08 | Own typed finite limits, store root/version/profile and migration modes without importing store authority into config. |
| `KEEP`/`ADD checks` | `xtask` and existing architecture/test tooling | 02–08 | Enforce forbidden dependencies, temporary-code deletion and source invariants. |

Observability may not fill authoritative payload metadata or mutate root/head
truth as a side effect of sampling. Any non-authoritative cache must be bounded,
reconstructible and irrelevant to readiness correctness.

## Temporary migration placement and deletion unit

| Disposition | Path hypothesis | Phase | Constraint |
|---|---|---:|---|
| `ADD`, temporary | `crates/sandbox-runtime/layerstack/src/legacy_import.rs` or `src/legacy_import/**` | 05 | Decode legacy selected views and call ordinary V2 APIs. |
| `ADD`, temporary | existing manager/daemon/application invocation sites | 05 | Fence/invoke/report only; no alternate representation or write path. |
| `ADD`, temporary | migration-only config/progress/test fixtures | 05 | Explicit namespace and deletion manifest; fail closed and restart safely. |
| `DELETE` | all migration-only code/config/callers/dependencies | 08 | Delete as one bounded unit after owner-approved observation; rebuild and requalify clean artifact. |
| `KEEP` | permanent V2 generation/writer law | 08 | Prevent legacy writer resurrection after importer deletion. |

See [migration and cutover](08-migration-and-cutover.md) for the transition
state machine. Legacy data deletion is out of this source deletion unit and
requires separate authorization.

## Phase-by-phase first touch map

| Phase | First source areas | Required stopping boundary |
|---:|---|---|
| 02 | `layerstack/src/lib.rs`, `model/**`, new `identity.rs`/`identity/**`, identity tests | No durable store I/O, consumer rewiring, migration, or new package/service. |
| 03 | new `store/**`, `storage/{fs.rs,lock.rs}`, focused legacy stack/model isolation | Offline store only; no public cutover or app semantics selection. |
| 04 | operation layerstack/file/workspace-session/services, runtime-effect adapters, daemon/manager/provider/observability consumers | No live cutover; preserve open DECs and one store writer. |
| 05 | temporary store-local importer, generation-fence call sites, migration tests/config | No production flip; no dual writes or permanent legacy dependency. |
| 06 | integration/fault/resource/architecture tests and instrumentation | Prove exact artifact offline; no live state change. |
| 07 | existing lifecycle/config/runbook paths needed for authorized fence/cutover | Use only Phase 06-qualified artifact; no migration-code deletion. |
| 08 | migration deletion manifest, compatibility-only call sites/config/tests | Rebuild/reprove/deploy clean artifact; no implicit legacy-data deletion. |

## Required deletion/hard-failure audit

The final V2 production path must have no operational truth dependency on:

- layer manifests, layer refs or layer changes;
- parent chains or depth;
- merge/rebase of stale publication;
- manual or automatic squash;
- whiteout/delta reconstruction as selected truth;
- layer leases as durable selected-Version reachability;
- legacy workspace-base identity;
- raw digest accepted as a store binding;
- direct writes to `versions/`, `roots/` or `heads/` outside the store owner;
- temporary importer/progress/legacy decoder types after Phase 08; or
- diagnostics/cache records as readiness authority.

Temporary legacy code may coexist for compilation and import only while every
runtime writer is fenced. A hidden fallback that reads layers after a V2 error
is a correctness failure, not compatibility.

## Forbidden additions without Phase 01 reopening

Do not add a replacement storage crate, database, helper daemon, RPC boundary,
coordinator, persistent refcount authority, object-DAG/archive truth,
independent GC service, plugin/backend framework, or second writer unless a
specific R0 correctness/privilege/process/recovery/resource failure is proved
and joint selection is reopened.

An internal module, test seam or low-level dependency is not automatically an
architectural boundary. It must still have one owner, bounded resources,
compatible dependency direction and no independent lifecycle/protocol.

## Verification commands and evidence

Later phases should record focused commands rather than silently asserting
source placement. Expected checks include:

```text
cargo metadata --format-version 1
rg for layer/depth/squash/merge/whiteout/manifest truth in V2 paths
rg for identity dependencies on workspace/overlay/namespace/provider/manager
rg for direct writes to payload/root/head paths outside layerstack store
rg for legacy_import references after Phase 08
targeted package tests and architecture/dependency checks
```

Run these against the phase-sealed implementation source and record branch,
HEAD and dirty state. This document itself is design evidence, not proof that
the future source already conforms.

## Reopening conditions

Reopen Phase 01 if the e497 placement assumptions no longer hold and the change
requires another owner, reversed dependency, new process/service/crash domain,
different storage family, runtime-private identity, more than one selected-Version
writer, permanent legacy decoding, or dual writable truth. Ordinary internal
file naming and safe implementation refinement remain with the owning phase.

Related: [ownership](01-ownership-and-boundaries.md) ·
[Version identity](02-state-identity.md) · [LayerStack-0 storage](03-state-store.md) ·
[verification](10-verification-matrix.md)
