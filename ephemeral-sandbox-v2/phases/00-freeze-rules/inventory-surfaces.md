# Phase 00 — Surface inventory (from source)

**Status:** pass-2 inventory complete for the requested G1–G6 scope  
**Measured implementation:** `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0` at `e4974d1f9aac702b35e052629cb070c897989352`  
**Primary catalog:** `crates/sandbox-operations/catalog/src/`  
**Primary dispatch:** `crates/sandbox-runtime/operation/src/operations/registry/`

This is an inventory of the measured implementation, not a V2 design. In
particular, current LayerStack publication and current Docker disk layout are
evidence to migrate from; they do not override the product hard rules or close
any decision.

---

## 1. Catalog and dispatch inventory

### 1.1 Public catalog operations

The public operation catalogs contain **26** names: 8 manager, 10 runtime, and
8 observability. The daemon HTTP-only `file_list` capability makes the pinned
current public/tool inventory **27** names. This current count is unrelated to
the appendix's legacy 26-row V2 proposal (§8).

| Domain | Exact catalog names | State / workspace relevance |
|--------|---------------------|-----------------------------|
| Manager (8) | `create_sandbox`, `list_docker_images`, `list_workspace_directories`, `destroy_sandbox`, `list_sandboxes`, `inspect_sandbox`, `squash_layerstacks`, `export_changes` | Fleet lifecycle, discovery, compact, export |
| Runtime (10) | `exec_command`, `write_command_stdin`, `read_command_lines`, `file_read`, `file_write`, `file_edit`, `file_blame`, `create_workspace_session`, `publish_workspace_session`, `destroy_workspace_session` | Commands, file access, live workspaces, publication |
| Observability (8) | `snapshot`, `trace`, `events`, `resources`, `daemon`, `topology`, `cgroup`, `layerstack` | Logically read-only diagnostics; never storage authority. `layerstack` sampling may lazily fill a non-authoritative byte-size sidecar (§4.2). |

Runtime behavior relevant to the V2 boundary:

- `file_read` with `workspace_session_id` reads a live workspace; without it,
  it reads the latest published LayerStack view.
- `file_write` and `file_edit` with a session mutate that live workspace.
  Without a session, current code calls `amend_path` and publishes a layer
  attributed to `operation:<request_id>`. The V2 disposition remains
  **DEC-017 open**.
- `exec_command` without a session creates an automatic session using
  `publish_then_destroy`; an explicit session stays alive until teardown.
- `file_blame` reads the append-only auditability side channel, not the
  LayerStack manifest or V2 portable identity. Its disposition remains
  **DEC-001 open**.
- No public manager operation named checkpoint, fork, or rollback exists in
  this pinned catalog.

### 1.2 HTTP-only and internal runtime operations

| Operation | Visibility | State touch | Source anchor |
|-----------|------------|-------------|---------------|
| `file_list` | Daemon HTTP only; not CLI/MCP catalog | List a snapshot or live-session directory | `catalog/src/internal/runtime.rs`; `daemon/src/http/api.rs`; `file/service/impls/list.rs` |
| `squash_layerstack` | Internal daemon operation | Compact layers and replace the manifest | `catalog/src/internal/runtime.rs`; `operation/src/layerstack/actions/squash.rs` |
| `export_layerstack` | Internal daemon operation | Read and stream published changes above base | `layerstack/service/impls/export.rs` |
| `read_export_chunk` | Internal daemon operation | Read an export spool chunk | same export path |

None of these four internal specs is projected into CLI or MCP tools.

---

## 2. Catalog → CLI → MCP projection

The operation catalog is the semantic source of truth. CLI and MCP are
projections, not independent API ledgers.

| Concern | CLI projection | MCP projection | Measured delta |
|---------|----------------|----------------|----------------|
| Operation names | Exact catalog snake-case names | Exact catalog names | No name mismatch |
| Ordinary argument names | Catalog underscore names rendered as kebab-case flags | Catalog JSON names unchanged | Presentation only |
| Runtime `sandbox_id` | Global `sandbox-runtime-cli --sandbox-id ID` scope selector | Required `sandbox_id` is injected into each runtime tool schema/request | Same routing value, different adapter placement |
| Manager / observability `sandbox_id` | Ordinary per-operation `--sandbox-id` flag | Ordinary catalog JSON argument | No semantic mismatch |
| `exec_command.cmd` | Positional `COMMAND` | JSON string `cmd` | Presentation only |
| `write_command_stdin.stdin` | Positional `TEXT` | JSON string `stdin` | Presentation only |
| `create_sandbox.workspace_root` | `--workspace-bind-root`, with CLI alias `--workspace-root` | JSON `workspace_root` | CLI compatibility alias only |
| `file_edit.edits` | JSON text supplied to `--edits` and parsed by CLI | Native JSON array | Encoding/presentation only |
| Domain selection | Separate manager/runtime/observability CLIs | An MCP server selects one domain and exposes exactly that domain's tools | Deliberate adapter boundary |
| Internal specs | Not projected | Not projected | `file_list` remains daemon HTTP only |

Catalog/adapter integrity tests assert one CLI projection per public route,
exact order/count/argument binding, exact MCP tool names and schemas for the
selected domain, and exclusion of internal specs.

One implementation/catalog mismatch is material: the observability query
handler accepts latent `layer_id` and `limit` fields for a per-layer delta view,
but the public `LAYERSTACK_SPEC` exposes only `sandbox_id`, `workspace_id`, and
`window_ms`. Therefore neither CLI nor MCP can request the delta view. Under
catalog-as-truth, `layer_id`/`limit` are **not public surface** at this commit;
this inventory does not promote them into one.

---

## 3. Manager create/destroy lifecycle and disk layout

This section follows the concrete manager + Docker provider path. The selected
host workspace is copied into a shared base; it is not bind-mounted writable
into the sandbox.

### 3.1 Create path

| Stage | Exact current write / mount | Lifetime and cleanup |
|-------|-----------------------------|----------------------|
| Host shared-base cache | Cache root is `EOS_SHARED_BASE_CACHE`, or `<workspace_root parent>/eos-shared-workspace-base-cache`. `build_shared_workspace_base` builds `<cache>/.building-<pid>-<unique>/base/B000001-base` with staging under `.building-…/staging/B000001-base.staging`, then renames the build atomically to `<cache>/<root_hash>` and fsyncs the cache. | Reused when `<cache>/<root_hash>/base/B000001-base` exists. Failed build removes its temp tree. Final cache entries persist across sandbox destroy. The selected host workspace is read, not changed. |
| Shared Docker volume | `eos-shared-base-<root_hash>` is seeded from host `<cache>/<root_hash>/base` by a transient container, then mounted read-only at `/eos/layer-stack/base`. | Shared across sandboxes with that hash. Not removed by per-sandbox destroy or create rollback. |
| Per-sandbox LayerStack volume | `<sandbox_id>-layer-stack` mounted at configured `runtime.workspace.layer_stack_root` (default `/eos/layer-stack`). | Removed on successful destroy/rollback. A provider error can leave it behind. |
| Per-sandbox workspace scratch volume | `<sandbox_id>-workspace` mounted at configured `runtime.workspace.scratch_root` (default `/eos/workspace`). | Holds `manager.json`, live session scratch trees, and transient export spools under `.export/`. Removed on successful destroy/rollback. |
| Seeded LayerStack files | `/eos/layer-stack/{layers,staging,.layer-metadata}/`; `manifest.json` version 1 pointing `B000001-base` at `base/B000001-base`; `workspace.json`; `.layer-metadata/B000001-base.digest`. | In the per-sandbox LayerStack volume, except that the nested `base` mount is the shared read-only volume. |
| Live workspace mountpoint | Configured container workspace root (default `/workspace`) is created by the seed archive. | The directory itself is in the container writable layer; runtime mounts the live workspace there. |
| Daemon assets/runtime | Daemon binary/config (defaults `/eos/bin/sandbox-daemon`, `/eos/config/daemon.yml`) are uploaded separately. The daemon creates `/eos/runtime/daemon/runtime.sock`, `runtime.pid`, and bounded files under `observability/` (`observability.ndjson`, `resources.ndjson`, rotated/lock siblings, and optional `daemon-diagnostic.json`). | Container writable layer; removed with the container. |
| Runtime side channels | Runtime opens `<layer_stack_root>/../storage/file_auditability` and can preserve bounded failed-holder artifacts under sibling `storage/workspace_recovery` (defaults `/eos/storage/{file_auditability,workspace_recovery}`). | These default paths are outside both named per-sandbox volumes, so they live in the container writable layer and disappear with container removal. That is a measured current layout fact, not a V2 durability choice. |
| Manager registry | If `manager.registry_path` is configured, every create/state/endpoint/remove mutation writes a sorted JSON snapshot to sibling `<registry filename>.tmp`, fsyncs it, then renames it. Without a path, the registry is in memory only. | Host manager state, independent of the sandbox volumes. |
| Manager resource ring | The manager sampler writes one fixed-size `<sandbox_id>.ring` under sibling `observability-resources/` when a registry path exists; otherwise under the platform state directory (`XDG_STATE_HOME`, macOS Application Support, or `$HOME/.local/state`). | Host diagnostics state. Successful destroy removes that sandbox's ring; a failed destroy can retain it with the manager record. |

The create sequence is: build/reuse shared host base → ensure/seed shared
Docker volume → create stopped container plus two per-sandbox volumes → upload
the seed archive → persist manager record → install/start/check daemon → persist
endpoints and `Ready`. Failure after a record exists performs best-effort daemon
stop, runtime destroy, and record removal. Shared cache/volume are intentionally
left reusable.

### 3.2 Destroy path

1. Manager persists `Stopping` and stops the daemon when an endpoint exists.
2. Docker removes the container, then removes
   `<sandbox_id>-layer-stack` and `<sandbox_id>-workspace` sequentially.
3. Manager persists `Stopped`, removes the registry record, and removes the
   resource-ring entry.

Destroy does **not** remove the selected host workspace, the host shared-base
cache, or `eos-shared-base-<root_hash>`. If Docker destruction fails, the
manager retains the record as `Failed`; because container and volume removal is
sequential, partial provider cleanup is possible.

Source anchors: `sandbox-manager/src/management/service/impls/create_sandbox.rs`,
`destroy_sandbox.rs`, `sandbox-manager/src/store.rs`,
`sandbox-manager/src/resource_ring.rs`,
`sandbox-provider-docker/src/{runtime,archive,launch,engine}.rs`, and
`sandbox-runtime/layerstack/src/workspace_base/build.rs`, plus runtime
`operation/src/{workspace_session/service/recovery.rs,layerstack/service/impls/export.rs}`
and daemon/telemetry observability paths.

---

## 4. Durable writer inventory

### 4.1 Logical content and head writers

| Writer path | Production entry/callers at e497 | Durable effect | Convergence point |
|-------------|----------------------------------|----------------|-------------------|
| Validated session publish | Explicit `publish_workspace_session`; automatic `exec_command` finalization | New layer or no-op; manifest/head advance; auditability append after commit | `LayerStackService::publish_changes` → `LayerStack::publish_validated_changes` |
| Sessionless write/edit | `file_write` and `file_edit` only when no session id is supplied | Read/transform/single-path publish under the exclusive writer lock; auditability append | `LayerStackService::amend_path` → `LayerStack::amend_path` |
| Manual squash | Manager `squash_layerstacks` → internal daemon `squash_layerstack` | Replace squashable manifest block, rewrite leases, GC when safe | Operation action → `LayerStack::squash_with_observer` |
| Autosquash | Policy worker after qualifying commits/startup | Same squash mechanism and effects | Same operation action and `squash_with_observer` |
| Runtime base ensure | Runtime service construction/open | Build local base/binding only when missing; validate a provider-seeded binding otherwise | `ensure_workspace_base` |
| Manager shared-base builder | `create_sandbox` | Content-addressed host cache and Docker seed input | `build_shared_workspace_base` |

### 4.2 Durable metadata, audit, and reclamation writers

| Writer | Effect | Truth classification |
|--------|--------|----------------------|
| Workspace persistence | `/eos/workspace/manager.json` plus session scratch/run directories | Live-runtime recovery metadata; not committed portable identity |
| Failed-holder recovery | Bounded copy + manifest under `/eos/storage/workspace_recovery/<artifact-key>` when holder finalization/cleanup requires recovery | Failure artifact side channel; default Docker layout loses it with the container |
| Export pipeline | Runtime creates transient `/eos/workspace/.export/<export-id>.tar.zst`; manager applies the stream to the caller-selected host destination | Explicit export output and scratch, not a second writable head |
| Lease acquire/release/sweep | Lease registry/state and safe reclamation of unreferenced layer directories/sidecars | Reachability/GC metadata; not new logical content |
| Layer metadata sidecars | Publish/base creation writes `.digest` and publish writes `.bytes`; `sample_layerstack` also lazily writes a missing `.layer-metadata/<layer_id>.bytes` after a complete disk walk | Integrity and size cache metadata; neither is a separate head or portable identity |
| File auditability append | `file_auditability_*.ndjson` events after publish/amend | Attribution side channel; not head truth |
| Daemon telemetry / diagnostics | Bounded active/rotated NDJSON logs and an optional diagnostic JSON artifact beside the daemon socket | Container-local diagnostics; not sandbox content |
| Manager registry / resource rings | Optional host JSON snapshot of sandbox records plus per-sandbox fixed-size resource rings | Fleet lifecycle/diagnostics; not sandbox content |

Published-content/head non-writers include `file_read`, `file_list`,
`file_blame`, export reads, and command stdin/stdout by themselves.
Observability queries never mutate the head, but a `layerstack` query may fill
the byte cache and daemon-metric collection may emit a bounded diagnostic
artifact; background telemetry also writes the bounded logs listed above.
`destroy_workspace_session` discards unpublished live state; it does not create
published content.

### 4.3 Pass-2 call-site recheck

The production `src/` tree was re-searched for the required writer symbols:

| Search symbol | Production finding |
|---------------|--------------------|
| `publish_layer(` | Public low-level definition only; no other production `src/` caller. Tests call it directly. |
| `publish_validated_changes(` | Definition plus the single LayerStack service publish caller. |
| `amend_path(` | LayerStack/service definitions plus sessionless `file_write` and `file_edit` callers. |
| `squash_with_observer(` / `squash(` | Manual and autosquash converge in the operation LayerStack action. |
| `ensure_workspace_base(` | Runtime service boot/open plus definition. |
| `build_shared_workspace_base(` | Manager create plus definition. |
| `record_layer_publish(` | Publish and amend append paths plus definition. |
| `write_manifest(` / `write_layer_digest(` / `write_layer_bytes(` | Manifest writes are base build, publish, and squash; digest writes are base build and publish; byte-sidecar writes are publish plus their definitions. |
| `sample_layerstack(` / `write_bytes_sidecar(` | Production sampling is called by the daemon observability adapter and post-squash telemetry. When no valid byte sidecar exists, a complete layer walk writes the cache through the collector-local helper. |
| `preserve_recovery_artifact(` | Failed workspace-holder finalization copies a bounded recovery tree and atomically publishes its manifest under the sibling storage root. |
| `resource_ring.append_if(` / telemetry `Sink::append` | Manager cadence writes host resource rings; daemon observers/resource sampler write bounded container-local logs. These are operational side stores, not published sandbox truth. |
| `export_spool_dir(` / export apply | Runtime export writes and later reaps a scratch spool; manager materializes the validated caller-selected destination. |

**Completeness claim:** production call sites for these named symbols are
complete at e497. Residuals are explicitly bounded to test-only direct callers,
future provider implementations not present at this commit, and new symbols
introduced after the seal.

---

## 5. Publish rejection and OCC matrix

`PublishReject` carries `path`, `reason`, optional `source_conflict`, optional
`protected_drop`, and an internal `message`. The public serializer emits the
snake-case reason and structured optional fields, but always emits
`"message": null`; route-preparation internals are deliberately redacted.

| Internal reason → public class | Symbol / firing site | Exact measured condition | Product-facing envelope |
|--------------------------------|----------------------|--------------------------|-------------------------|
| `InvalidBaseRevision` → `invalid_base_revision` | `plan_publish::validate_base_revision`; `LayerStackService::publish_changes`; synthetic rejection in `publish_session` | Supplied base revision's manifest version/root hash/layer count is inconsistent with its accompanying base manifest, or the captured expected revision does not equal the revision derived from that manifest. | Explicit session publish: `operation_failed` with structured `publish_rejection`. Automatic finalize: terminal command response marks `publish_rejected=true`, class string. |
| `ProtectedPath` → `protected_path` | `publish::route::classify_protected`; protected-drop checks; `explicit_publish_input` | Any component is `.layer-metadata` or starts `.wh.`; top-level `manifest.json`, `workspace.json`, `layers`, `staging`, or `.layer-metadata`; or a protected capture drop is rejected. The core planner permits only `UnsupportedSpecialFile` drops, while explicit session publication rejects any protected drop, including that class. | Same explicit/automatic envelopes. Structured payload may include `protected_drop` with `unsupported_special_file`, `invalid_layer_path`, or `command_scratch_path`. |
| `SourceConflict` → `source_conflict` | `resolve_source_change`; structural OCC validation | Under the writer lock, a source-routed path's active fingerprint differs from the base expectation and is neither an idempotent compatible directory create nor an eligible clean three-way text merge. Structural subtree changes also conflict. | Same envelopes; structured payload includes path plus expected/actual fingerprints. |
| `OpaqueDirProtectedDescendant` → `opaque_dir_protected_descendant` | `plan_opaque_dir` hidden-descendant routing | Opaque-directory expansion finds a hidden protected descendant. | Same envelopes; rejected before publication. |
| `OpaqueDirMixedRoutes` → `opaque_dir_mixed_routes` | `plan_opaque_dir` | Hidden descendants of one opaque directory span source and ignored routes. | Same envelopes; rejected before publication. |
| `OpaqueDirExpansionLimit` → `opaque_dir_expansion_limit` | opaque planning; structural OCC expansion | Hidden-descendant expansion or structural-conflict census exceeds the hard bound of 4096 entries. | Same envelopes; rejected without leaking the enumerated paths. |
| `RoutePreparationFailed` → `route_preparation_failed` | `plan_opaque_dir` around `hidden_descendants` | Preparing the hidden-descendant route returns an error. | Same envelopes; public `message` remains null even though the internal reject stores text. |

Envelope details shared across rows:

- Explicit `publish_workspace_session` returns top-level `operation_failed`,
  message `workspace session publish was rejected`, and details containing
  `stage=publish`, `session_retained=true`, `workspace_session_id`, and the
  structured `publish_rejection` when present.
- Automatic `publish_then_destroy` rejection does not retroactively fault the
  command operation. The terminal command output exposes `publish_rejected`
  and `publish_reject_class`; finalization continues to destroy the automatic
  session.
- Sessionless `file_write`/`file_edit` map LayerStack failures to top-level
  `operation_failed` without the structured `publish_rejection` object.
- `LayerStackError::ManifestConflict { expected, found }` is a separate late
  manifest recheck in `publish_layer_unlocked`. It maps as an unstructured
  LayerStack service `operation_failed`, not a `PublishRejectReason`.

### 5.1 Current concurrency behavior versus the V2 rule

Current `publish_validated_changes` plans against the captured base, acquires
the exclusive writer lock, rereads the active manifest, and resolves changes.
It permits compatible directory creates and attempts a clean three-way merge
for eligible text writes. Therefore current publication can automatically merge
some concurrent text changes.

That behavior is **not** the V2 target. Product hard rule 5 remains: one head
transition at a time under OCC, with no silent merge or rebase. Later V2
fixtures must test the rule, not bless the measured current auto-merge path.

Current sessionless amend is different again: it holds the exclusive writer
lock across latest-head read → transform → resolve → commit, so another logical
writer cannot normally make its base stale inside that operation. Protected
path and I/O failures remain possible; the late manifest-conflict type is still
defensive infrastructure.

---

## 6. Workspace, overlay, exec, and composition owners

| Concern | Package / path | Current role |
|---------|----------------|--------------|
| Workspace create/destroy/remount/capture | `crates/sandbox-runtime/workspace` (`sandbox-runtime-workspace`) | Live mounts, upperdir capture, session persistence |
| Overlay mount helper | `crates/sandbox-runtime/overlay` | Kernel overlay primitives |
| Namespace process holder | `crates/sandbox-runtime/namespace-process` | Process/namespace lifecycle |
| Namespace command execution | `crates/sandbox-runtime/namespace-execution` | Isolated command runner |
| Runtime composition | `crates/sandbox-runtime/operation` | Wires file, LayerStack, workspace-session, command, autosquash |
| Durable LayerStack implementation | `crates/sandbox-runtime/layerstack` | Current manifest/layers/publish/squash/project/lock home |
| Daemon composition | `crates/sandbox-daemon` | RPC/HTTP and runtime/observability dispatch |
| Manager fleet | `crates/sandbox-manager` | Create/destroy/squash/export orchestration |
| Docker effects | `crates/sandbox-provider-docker` | Container, named volume, archive, and daemon installation effects |

These ownership boundaries are current evidence only. Mounts, OverlayFS,
namespaces, workspace run directories, and provider bindings remain
runtime-private and outside V2 portable identity.

---

## 7. `layerstack` observability field inventory

### 7.1 Public request

| Field | Catalog contract |
|-------|------------------|
| `sandbox_id` | Required routing target |
| `workspace_id` | Optional; selects one live workspace view |
| `window_ms` | Optional, catalog default 60,000 ms, maximum 600,000 ms; controls stack trend |

The latent handler-only `layer_id`/`limit` fields are not public (§2).

### 7.2 Default inventory response

| Field | Meaning / source |
|-------|------------------|
| `view` | Literal `layerstack` |
| `manifest_version`, `root_hash` | Live active manifest observation |
| `active_lease_count` | In-process lease registry count |
| `total_bytes`, `total_allocated_bytes` | Logical and allocated totals for active layers |
| `storage_logical_bytes`, `storage_allocated_bytes` | Totals for the complete LayerStack storage root, including obsolete/staging/metadata content |
| `staging_entry_count` | Immediate entry count under `staging/` |
| `layers[]` | Newest-to-base entries with `layer_id`, `bytes`, `allocated_bytes`, `leased_by_workspaces`, and `booked_by` newer leased layers |
| `trend[]` | When a reader and `window_ms` are available: sampler metrics plus `ts`; stack metrics are `layer_count`, `layers_bytes`, `layers_allocated_bytes`, `storage_allocated_bytes`, `staging_entry_count`, and `active_leases` |

Incomplete, malformed, overflowed, or walk-budget-limited disk measurements are
`null`, never forged as zero. Logical sidecars can supply a layer's logical byte
count, but incomplete walks do not populate or claim allocated totals.

### 7.3 Workspace response

With `workspace_id`, the response contains `view`, `workspace`, `mounts[]`, and
`upper_bytes`. Every mount has `layer_id` and `shared_with[]`; `upper_bytes` is
the latest workspace `disk_bytes` telemetry sample and may be null.

The observability view joins live runtime state with a bounded on-disk sampler
and, for trends/upperdir size, telemetry samples. It is diagnostics—not a
portable catalog, migration input, collision oracle, or writable authority.
The sampler can populate a missing `.layer-metadata/<layer_id>.bytes` cache only
after a complete walk; that metadata side effect does not advance the manifest
or make the view authoritative.

For completeness, the non-public layer-delta handler would return `view`,
`layer_id`, `entries[] {path, kind}`, and `truncated`, using a configured default
limit of 500 and maximum 5,000. Recording it here does not make it public.

---

## 8. Legacy 26-row proposal location

The exact legacy document is [system-design/api_methods.md](<../../../implementation-plan/2.0 migration/system-design/api_methods.md>). Its 26 proposal rows are 18 sandbox/session/checkpoint/fork operations plus 8 command/file operations. It is **evidence-only design input**, not the deployed e497 surface and not a Phase 00 decision.

The appendix [public API disposition](../../../implementation-plan/new_2.0_migration_implementation_plan/design/public-api.md) keeps three populations separate: pinned current public/tool names, the legacy 26-row proposal, and a candidate 25-row ledger. The [source-disposition ledger](../../../implementation-plan/new_2.0_migration_implementation_plan/traceability/source-disposition.md) marks the legacy document `EVIDENCE-ONLY` / `OPEN-RETEST`; [DEC-017](../../../implementation-plan/new_2.0_migration_implementation_plan/decisions/README.md) still requires the mapping and owner approval before the final V2 set can close.

---

## 9. Bounded residuals

The pass-2 requested gaps are closed as an inventory at e497. The remaining
items below are scope boundaries, not unfinished pass-2 backlog:

- This records the concrete Docker provider present at the sealed commit; a
  future provider would require a fresh lifecycle/layout inventory.
- Test helpers and fixtures intentionally call lower-level APIs in shapes not
  counted as production writers; selected anchors are mapped in
  [fixture-catalog.md](fixture-catalog.md).
- The latent observability delta is implementation-only until the catalog is
  deliberately changed.
- The final V2 public surface, sessionless write behavior, exact blame contract,
  architecture, and storage algorithm all remain open decisions.

---

Parent: [SPEC.md](SPEC.md) · [PLAN.md](PLAN.md)
