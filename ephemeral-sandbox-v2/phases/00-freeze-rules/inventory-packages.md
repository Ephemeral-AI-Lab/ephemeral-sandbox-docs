# Phase 00 — Package / module map (today)

**Status:** measured from clean worktree  
**Source root:** `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0` @ `e4974d1f9aac702b35e052629cb070c897989352`

V2 package graph remains **OPEN** (product PRD design decision). This map is
**today’s** layout for R0 orientation only.

---

## Workspace members (Cargo)

| Package name | Path | Role | V2 relevance |
|--------------|------|------|--------------|
| `sandbox-runtime-layerstack` | `crates/sandbox-runtime/layerstack` | **Store history home** — manifest, layers CAS-ish layout, publish, squash, project, leases, locks, workspace base | **R0 primary rewrite target** for immutable state store |
| `sandbox-runtime-workspace` | `crates/sandbox-runtime/workspace` | Live workspace / overlay upperdirs / capture / remount | Workspace effects; must not own portable identity |
| `sandbox-runtime-overlay` | `crates/sandbox-runtime/overlay` | OverlayFS mount helper | Runtime-private |
| `sandbox-runtime-namespace-process` | `crates/sandbox-runtime/namespace-process` | Namespace process holder | Runtime-private |
| `sandbox-runtime-namespace-execution` | `crates/sandbox-runtime/namespace-execution` | Isolated command execution | Runtime-private |
| `sandbox-runtime` | `crates/sandbox-runtime/operation` | Runtime app composition: file API, workspace sessions, layerstack service facade, command ops, autosquash | Keep app ordering; wire V2 store later |
| `sandbox-daemon` | `crates/sandbox-daemon` | Authenticated RPC + HTTP allowlist + dispatch | Composition root; no store algorithms |
| `sandbox-manager` | `crates/sandbox-manager` | Fleet create/destroy/list/inspect/squash/export | Lifecycle + compact/export; not portable identity |
| `sandbox-operation-catalog` | `crates/sandbox-operations/catalog` | Public/internal op names, args, routes | DEC-017 surface freeze source |
| `sandbox-operation-contract` | `crates/sandbox-operations/contract` | Adapter-neutral op vocabulary | Shared types only |
| `sandbox-operation-client` | `crates/sandbox-operations/client` | Client request build | Callers |
| `sandbox-cli` | `crates/sandbox-cli` | CLI projection + bins | Product surface |
| `sandbox-mcp` | `crates/sandbox-mcp` | MCP adapter | Product surface |
| `sandbox-gateway` | `crates/sandbox-gateway` | Gateway | Transport |
| `sandbox-protocol` | `crates/sandbox-protocol` | Wire codec / framing / auth fields | No store |
| `sandbox-config` | `crates/sandbox-config` | Typed config (incl. `runtime.layerstack`, cgroup, file caps) | Resource envelope knobs |
| `sandbox-provider-docker` | `crates/sandbox-provider-docker` | Docker provider | Provisioning only |
| `sandbox-observability-telemetry` | `crates/sandbox-observability/telemetry` | Emit/collect | Non-authority |
| `sandbox-observability-query` | `crates/sandbox-observability/query` | Query views (incl. layerstack diagnostics) | Non-authority |
| `xtask` | `xtask` | Packaging / architecture checks | Dev tooling |

Namespace group dirs without root `Cargo.toml` (grouping only, per product
conventions): `crates/sandbox-operations/`, `crates/sandbox-runtime/`,
`crates/sandbox-observability/`.

---

## Layerstack internal modules (store home detail)

| Module path | Role |
|-------------|------|
| `layerstack/src/stack/` | `LayerStack` core: open, manifest, publish, squash, project, leases |
| `layerstack/src/stack/ops/publish.rs` | `publish_layer` / `publish_validated_changes` |
| `layerstack/src/stack/publish/` | Merge + publish models / reject reasons |
| `layerstack/src/stack/file_read.rs` | Classified read + `amend_path` (sessionless write path) |
| `layerstack/src/stack/squash.rs` | Squash phases / outcome |
| `layerstack/src/storage/` | FS, exclusive lock, whiteout helpers |
| `layerstack/src/model/` | `Manifest`, `LayerRef`, `LayerChange`, digests |
| `layerstack/src/workspace_base/` | Shared workspace base layer construction |
| `layerstack/src/service/` | Thin service facades (snapshot lease helpers) |
| Constants | `LAYERS_DIR`, `STAGING_DIR`, `ACTIVE_MANIFEST_FILE` (`manifest.json`), `LAYER_METADATA_DIR` |

On-disk names and layer-chain semantics are **legacy truth model** — V2 replaces
the model; path reuse is a Phase 01 design question, not decided here.

---

## Runtime operation façade modules

| Module path | Role |
|-------------|------|
| `operation/src/layerstack/service/` | `LayerStackService` (publish, amend, read, export, observe) |
| `operation/src/layerstack/actions/squash.rs` | Squash action + telemetry observer |
| `operation/src/layerstack/autosquash_engine/` | Background squash trigger |
| `operation/src/file/` | `FileService` + auditability store + read/write/edit/list/blame |
| `operation/src/workspace_session/` | Session create/publish/destroy/finalize/remount |
| `operation/src/command/` | Exec / stdin / lines |
| `operation/src/operations/registry/` | Dispatch tables for public / internal / HTTP-only ops |
| `operation/src/services.rs` | Boot composition: open layerstack, file auditability, workspace, autosquash |

---

## Config knobs relevant to resources (today)

| Config area | Examples | Notes |
|-------------|----------|-------|
| `runtime.file` | `max_output_bytes` (256 KiB), `max_edit_bytes` (4 MiB), `max_list_entries` (2000), read line defaults | Request-bounded file API |
| `runtime.command` | `max_active` (32) | Concurrent commands |
| `runtime.layerstack` | `remount_sweep_width`, `export_chunk_bytes`, `spool_zstd_level`, `autosquash_policies.squash_at_n_layers` | Store-adjacent tuning |
| `runtime.workspace` | `layer_stack_root`, `workspace_root`, `scratch_root`, resource caps | Paths + workspace bounds |
| Workload cgroup | `memory_high_bytes`, `memory_max_bytes`, `pids_max`, nano CPUs | Untrusted runtime bounds (manager/daemon inject) |
| Daemon server | connection / request byte caps | Transport, not store |

These are **today’s** product knobs, not sealed V2 envelopes (see SPEC §9).

---

## Hypothesis alignment with human PLAN

Root [PLAN.md](../../PLAN.md) “likely code touch map” matches source:

| PLAN guess | Source confirmation |
|------------|---------------------|
| LayerStack home first (R0) | `sandbox-runtime-layerstack` is the durable history owner |
| Workspace / overlay / exec stay separate | Distinct crates as above |
| App ordering in manager/runtime | `sandbox-manager` + `sandbox-runtime` + `sandbox-daemon` |
| No new packages by default | Current tree has no V2 store package |

Exact future crate edges remain **OPEN** until Phase 01.

---

Parent: [SPEC.md](SPEC.md) · [PLAN.md](PLAN.md)
