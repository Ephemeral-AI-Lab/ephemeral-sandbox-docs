# Cluster 04 — Operations: writing spec

> Companion to [`../skelenton.md`](../skelenton.md), Cluster 04. This is the
> implementation plan for the five operation-reference and adapter pages. It is
> grounded in the code as of 2026-07-11 and concentrates on three questions:
> **what operations exist, how callers use them, and what each returns.**

**Code root:** `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`. All source
anchors below are relative to that root.

| Abbrev | Expands to |
|---|---|
| `CAT/` | `crates/sandbox-operations/catalog/src/` |
| `CONTRACT/` | `crates/sandbox-operations/contract/src/` |
| `CLIENT/` | `crates/sandbox-operations/client/src/` |
| `MGR/` | `crates/sandbox-manager/src/operations/` |
| `RT/` | `crates/sandbox-runtime/operation/src/` |
| `OBS/` | `crates/sandbox-observability/query/src/` |
| `CLI/` | `crates/sandbox-cli/src/` |
| `MCP/` | `crates/sandbox-mcp/src/` |

---

## 1. Deliverable and writing order

Write the five pages already named in the skeleton, in this order:

| Order | Page | Contract owned by the page |
|---|---|---|
| 1 | `01-management-operations.md` | 8 public management operations and the 3 daemon-internal operations they compose |
| 2 | `02-command-and-file-operations.md` | 7 public runtime operations, 2 internal workspace-session operations, and HTTP-only `file_list` |
| 3 | `03-observability-operations.md` | 5 public observability operations, including both `snapshot` routes and all result variants |
| 4 | `04-cli.md` | How the 20 public operations project into three CLI binaries and how results/errors reach stdout/stderr |
| 5 | `05-mcp.md` | How the same 20 public operations project into MCP schemas and `structuredContent` |

Pages 01–03 are the canonical caller reference. Pages 04–05 explain adapter
projection and link back instead of restating every semantic contract.

## 2. Census and classification

The opening of page 01 must state the arithmetic precisely:

- **20 public operation names** expand to **21 public route rows**, because
  `snapshot` has a system route and a sandbox route.
- **5 internal operation names** have sandbox-scoped daemon routes.
- **1 HTTP-only operation**, `file_list`, has a runtime handler but no catalog route.
- Therefore the implementation has **26 unique operation names** and **27 callable
  route/surface combinations**. Only the 20 public names appear in CLI and MCP.

The catalog integrity tests pin the public and internal sets
(`crates/sandbox-operations/catalog/tests/integrity.rs`); the runtime registry pins the HTTP-only partition
(`RT/operations/registry/file_operations.rs:20-40`).

### Complete inventory

| Operation | Functional cluster | Visibility/surface | Scope | Executes in | Canonical page |
|---|---|---|---|---|---|
| `create_sandbox` | lifecycle | public | system | manager | 01 |
| `destroy_sandbox` | lifecycle | public | system | manager | 01 |
| `list_sandboxes` | discovery | public | system | manager | 01 |
| `inspect_sandbox` | discovery | public | system | manager | 01 |
| `list_docker_images` | discovery | public | system | manager | 01 |
| `list_workspace_directories` | discovery | public | system | manager | 01 |
| `squash_layerstacks` | storage maintenance | public | system | manager, then daemon | 01 |
| `export_changes` | change transfer | public | system | manager, then daemon | 01 |
| `squash_layerstack` | storage maintenance | internal RPC | sandbox | runtime | 01 |
| `export_layerstack` | change transfer | internal RPC | sandbox | runtime | 01 |
| `read_export_chunk` | change transfer | internal RPC | sandbox | runtime | 01 |
| `exec_command` | command lifecycle | public | sandbox | runtime | 02 |
| `write_command_stdin` | command lifecycle | public | sandbox | runtime | 02 |
| `read_command_lines` | command lifecycle | public | sandbox | runtime | 02 |
| `file_read` | file read | public | sandbox | runtime | 02 |
| `file_write` | file mutation | public | sandbox | runtime | 02 |
| `file_edit` | file mutation | public | sandbox | runtime | 02 |
| `file_blame` | file auditability | public | sandbox | runtime | 02 |
| `create_workspace_session` | session lifecycle | internal RPC | sandbox | runtime | 02 |
| `destroy_workspace_session` | session lifecycle | internal RPC | sandbox | runtime | 02 |
| `file_list` | file discovery | daemon HTTP only | daemon identity | runtime | 02 |
| `snapshot` | live state | public, two routes | system or sandbox | manager or observability | 03 |
| `trace` | historical trace | public | sandbox | observability | 03 |
| `events` | historical events | public | sandbox | observability | 03 |
| `cgroup` | resource history | public | sandbox | observability | 03 |
| `layerstack` | storage state/history | public | sandbox | observability | 03 |

The pages should use two classifications together:

1. **Routing classification:** public/internal/HTTP-only, system/sandbox, and
   manager/runtime/observability owner.
2. **User-job classification:** lifecycle, discovery, command interaction, file
   access, storage maintenance/transfer, and observability.

The first explains authority. The second helps a caller find the right operation.

## 3. Contract template for every operation

Every operation subsection in pages 01–03 must use the same compact template:

1. **Purpose and side effects** — one sentence, including whether it is read-only,
   mutates host state, mutates a session, or publishes a layer.
2. **Availability** — public/internal/HTTP-only; scope policy; execution owner;
   CLI binary and MCP set when public.
3. **Usage** — canonical CLI synopsis for public operations, then the logical RPC
   argument object. Internal operations show only the manager→daemon or daemon-HTTP
   invocation path; never imply they are directly public.
4. **Arguments** — table with name, JSON kind, requiredness, default, validation/cap,
   and semantic role. Put scope selectors in a visually separate row because
   `sandbox_id` is removed from `args` for sandbox-scoped requests.
5. **Success output** — one typed JSON skeleton and one representative JSON example.
   Mark fields as **always present**, **nullable**, or **conditionally absent**.
6. **Output variants** — a discriminator or condition for every alternative shape.
7. **Errors** — only operation-specific kinds/details; link to the shared envelope.
8. **Source of truth** — catalog declaration, parser/handler, output assembler, and
   at least one contract test.

Use this notation consistently in typed skeletons:

- `field?: T` means the key can be absent.
- `field: T | null` means the key is always present and its value can be JSON null.
- `T[]` means a JSON array, including an empty array when there are no items.
- Literal unions such as `"running" | "ok"` are exhaustive only when the code has an
  enum or exact-key test that proves them.

Do not call handler-local Rust structs the wire schema. The wire schema is the JSON
assembled immediately before `OperationResponse::ok(...)`, plus any adapter wrapping.

## 4. Shared request and response rules

Pages 01–03 should define these once, then link back from each operation:

```ts
type OperationError = {
  error: {
    kind: string;
    message: string;
    details: object;
  };
};
```

Success payloads are top-level JSON values; there is no `{ result: ... }` wrapper.
Errors use the shape above (`CONTRACT/error.rs:40-47`). `OperationResponse::running`
currently serializes exactly like `ok`; running state is identified by the operation
payload's `status` field (`CONTRACT/response.rs:14-27`).

Scope must be documented separately from arguments:

- Management operations are system-scoped. Their `sandbox_id`, where present, is
  ordinary fleet-operation data.
- Runtime operations require a sandbox scope selector. CLI uses the global
  `--sandbox-id`; MCP injects a required `sandbox_id` tool property; the request builder
  lifts it into `scope` and removes it from `args`.
- Observability `snapshot` selects system scope when `sandbox_id` is absent and sandbox
  scope when present. The other four observability operations require it.

Adapter output rules belong in pages 04–05:

- CLI writes one compact success JSON line to stdout (exit 0) or one error envelope to
  stderr (exit 1); local usage/config errors exit 2 (`CLI/output.rs:11-13,101-128`).
- MCP returns the same JSON as `structuredContent`, leaves textual `content` empty, and
  mirrors envelope presence into `isError` (`MCP/server.rs:66-80`).

## 5. Page 01 — management operations

### Public argument and usage matrix

| Operation | CLI usage | Arguments and constraints |
|---|---|---|
| `create_sandbox` | `sandbox-manager-cli create_sandbox --image IMAGE --workspace-bind-root PATH [--count N]` | `image: string` required/non-empty; `workspace_root: path` required/absolute/picker-allowed; `count: integer = 1`, minimum 1 |
| `list_docker_images` | `sandbox-manager-cli list_docker_images` | none |
| `list_workspace_directories` | `sandbox-manager-cli list_workspace_directories [--path PATH]` | `path?: path`; absent lists picker roots, present lists at most 500 immediate directories |
| `destroy_sandbox` | `sandbox-manager-cli destroy_sandbox --sandbox-id ID` | `sandbox_id: string` required |
| `list_sandboxes` | `sandbox-manager-cli list_sandboxes` | none |
| `inspect_sandbox` | `sandbox-manager-cli inspect_sandbox --sandbox-id ID` | `sandbox_id: string` required |
| `squash_layerstacks` | `sandbox-manager-cli squash_layerstacks --sandbox-id ID` | `sandbox_id: string` required |
| `export_changes` | `sandbox-manager-cli export_changes --sandbox-id ID --dest PATH [--format dir\|tar\|tar-zst]` | `sandbox_id: string`; absolute `dest: path`; `format: string = "dir"` with exact three-value enum |

Catalog anchors: `CAT/manager.rs`. CLI spellings and examples:
`CLI/projection/manager.rs`.

### Required success-shape coverage

Define and reuse this record shape for create/destroy/list/inspect:

```ts
type SandboxRecord = {
  id: string;
  workspace_root: string;
  state: string;
  daemon: { host: string; port: number } | null;
  daemon_http: { host: string; port: number } | null;
  shared_base: {
    source: string;
    target: string;
    root_hash: string;
    readonly: boolean;
  } | null;
};
```

| Operation | Success payload |
|---|---|
| `create_sandbox` | `count == 1` → `SandboxRecord`; `count > 1` → `{ sandboxes: SandboxRecord[] }` |
| `list_docker_images` | `{ images: string[] }` |
| `list_workspace_directories` | `{ path: string \| null, parent: string \| null, truncated: boolean, directories: { name: string, path: string }[] }` |
| `destroy_sandbox` | `SandboxRecord` for the removed/stopped record |
| `list_sandboxes` | `{ sandboxes: SandboxRecord[] }` |
| `inspect_sandbox` | `SandboxRecord` |
| `squash_layerstacks` | `SquashResult` below, passed through from internal `squash_layerstack` |
| `export_changes` | `DirectoryExportResult \| ArchiveExportResult` below |

The polymorphic `create_sandbox` result is mandatory documentation, not an
implementation footnote (`MGR/registry/management_operations.rs:99-112`). Record and
listing assemblers are at `:239-280`.

```ts
type SquashResult = {
  manifest_version: number;
  squashed_blocks: {
    squashed_layer_id: string;
    replaced_layer_ids: string[];
    replaced_layers: "reclaimed" | "leased";
    blocked_reasons?: string[];
  }[];
  faulty_sessions?: {
    session_id: string;
    class_detail: string;
    lease_errors: string[];
  }[];
};

type DirectoryExportResult = {
  manifest_version: number;
  format: "dir";
  layers_exported: string[];
  files_written: number;
  symlinks_written: number;
  deletes_applied: number;
  opaque_clears: number;
  skipped_unchanged: number;
  bytes_written: number;
  live_workspace_sessions?: string[];
};

type ArchiveExportResult = {
  manifest_version: number;
  format: "tar" | "tar-zst";
  layers_exported: string[];
  files_written: number;
  symlinks_written: number;
  whiteouts_emitted: number;
  bytes_written: number;
  live_workspace_sessions?: string[];
};
```

Shape anchors: `RT/layerstack/service/impls/squash.rs:80-149` and
`MGR/management/service/impls/export_changes.rs:417-449`. Exact export keys are pinned
in `crates/sandbox-manager/tests/manager_export.rs`.

### Internal fan-out operations

| Operation | Args | Success payload |
|---|---|---|
| `squash_layerstack` | `{}` | `SquashResult` |
| `export_layerstack` | `{}` | `{ export_id: string, manifest_version: number, layers_exported: string[], entries: { files: number, symlinks: number, whiteouts: number, opaques: number }, spool_bytes: number, live_workspace_sessions?: string[] }` |
| `read_export_chunk` | `{ export_id: string, offset: number, limit?: number }`; limit defaults to and is capped at configured chunk bytes | `{ chunk: string /* base64 */, offset: number, len: number, total: number, eof: boolean }` |

Explain that public plural `squash_layerstacks` is one manager-to-daemon call today;
the plural is API naming, not fleet-wide fan-out. Explain the two-step export protocol
without turning the internal operations into advertised user entry points.

## 6. Page 02 — command, file, and session operations

All seven public operations use sandbox scope. Their CLI prefix is always
`sandbox-runtime-cli --sandbox-id ID` and the scope selector is not part of `args`.

### Public argument and usage matrix

| Operation | Operation-specific usage and arguments |
|---|---|
| `exec_command` | `exec_command [--workspace-session-id ID] [--timeout-ms N] [--yield-time-ms N] COMMAND`; `cmd: string` required, the other three optional |
| `write_command_stdin` | `write_command_stdin --command-session-id ID [--yield-time-ms N] TEXT`; `command_session_id` and `stdin` required |
| `read_command_lines` | `read_command_lines --command-session-id ID [--start-offset N] [--limit N]`; offset default 0, limit default 200/max 1000 |
| `file_read` | `file_read --path FILE [--offset N] [--limit N] [--workspace-session-id ID]`; offset is 1-indexed/default 1, limit default/max 2000 |
| `file_write` | `file_write --path FILE --content TEXT [--workspace-session-id ID]` |
| `file_edit` | `file_edit --path FILE --edits JSON [--workspace-session-id ID]`; edits are ordered `{old_string,new_string,replace_all?}` objects |
| `file_blame` | `file_blame --path FILE`; published snapshot only |

Catalog anchors: `CAT/runtime/{command,file}.rs`. CLI spellings:
`CLI/projection/runtime.rs`.

### Command result shape

All three command operations return the same superset:

```ts
type CommandOutput = {
  status: "running" | "ok" | "error" | "timed_out" | "cancelled";
  exit_code: number | null;
  wall_time_seconds: number;
  command_total_time_seconds: number;
  start_offset: number;
  end_offset: number;
  total_lines: number;
  original_token_count: number;
  output: string;
  command_session_id?: string;
  workspace_session_id?: string;
  publish_rejected?: true;
  publish_reject_class?: string;
};
```

For each command operation, document when IDs are present, whether the returned window
is an initial yield or stable offset read, and what makes the status terminal. The shape
is assembled at `RT/operations/registry/command_operations.rs:95-151`; the status enum
is `RT/command/service/dto.rs:28-50`.

### File result shapes

| Operation | Success payload |
|---|---|
| `file_read` | `{ path: string, content: string, start_line: number, num_lines: number, total_lines: number, bytes_read: number, total_bytes: number, next_offset: number \| null, truncated: boolean }` |
| `file_write` | `{ type: "create" \| "update", path: string, bytes_written: number }` |
| `file_edit` | `{ type: "edit", path: string, edits_applied: number, replacements: number, bytes_written: number }` |
| `file_blame` | `{ path: string, ranges: { start_line: number, line_count: number, owner: string }[] }` |

For read/write/edit, make the two backends explicit: `workspace_session_id` present
means live session access; absent means latest-snapshot read or one-layer atomic publish.
Output assemblers: `RT/operations/registry/file_operations.rs:282-345`.

### Internal and HTTP-only operations

| Operation | Args | Success payload |
|---|---|---|
| `create_workspace_session` | `{ network_profile?: "shared" \| "isolated" }`, default `shared` | `{ workspace_session_id: string, network_profile: "shared" \| "isolated", finalize_policy: "no_op" }` |
| `destroy_workspace_session` | `{ workspace_session_id: string, grace_s?: number }`, grace must be non-negative | `{ workspace_session_id: string, destroyed: true, evicted_upperdir_bytes: number }` |
| `file_list` | HTTP `POST /files/list` body `{ path?: string, workspace_session_id?: string }` | `{ path: string, entries: { name: string, kind: "file" \| "directory" \| "symlink" \| "other", size: number \| null }[], truncated: boolean }` |

Internal session anchors: `RT/operations/registry/workspace_session_operations.rs:36-147`.
HTTP request synthesis: `crates/sandbox-daemon/src/http/api.rs:22-48,88-94`.

The page must distinguish error-envelope rejection from a successful command whose
shell `exit_code` is nonzero. It must also document operation-specific `details` shapes:
`active_command_session_ids`, `command_session_id`, `publish_rejection`, path, and
workspace-session id.

## 7. Page 03 — observability operations

### Argument and usage matrix

| Operation | CLI usage | Logical arguments |
|---|---|---|
| `snapshot` | `sandbox-observability-cli snapshot [--sandbox-id ID]` | optional scope selector only; absent = manager aggregate, present = one daemon |
| `trace` | `... trace --sandbox-id ID [--trace-id TRACE\|last]` | `trace_id: string = "last"` |
| `events` | `... events --sandbox-id ID [--name NAME] [--since-ms MS] [--last-n N]` | exact-name filter, unix-ms lower bound, newest-N cap |
| `cgroup` | `... cgroup --sandbox-id ID [--scope SCOPE] [--window-ms MS]` | `scope: string = "sandbox"`; `window_ms = 60000`, max configured/currently 600000 |
| `layerstack` | `... layerstack --sandbox-id ID [--workspace-id WS] [--window-ms MS]` | `workspace_id?: string`; `window_ms = 60000`, max configured/currently 600000 |

Catalog anchors: `CAT/observability/*.rs`. CLI spellings:
`CLI/projection/observability.rs`.

### Required success-shape coverage

| Operation/variant | Success payload |
|---|---|
| system `snapshot` | `{ sandboxes: SnapshotNode[] }` |
| sandbox `snapshot` | `SnapshotNode` directly, not wrapped in `sandboxes` |
| `trace` | `{ view: "trace", trace: string, spans: SpanTreeNode[] }` |
| `events` | `{ view: "events", events: EventRecord[] }` |
| `cgroup` | `{ view: "cgroup", scope: string, series: SampleDelta[] }` |
| `layerstack` inventory | `{ view: "layerstack", manifest_version: number, root_hash: string, active_lease_count: number, total_bytes: number, layers: { layer_id: string, bytes: number, leased_by_workspaces: number, booked_by: string[] }[], trend?: object[] }` |
| `layerstack` workspace | `{ view: "layerstack", workspace: string, mounts: { layer_id: string, shared_with: string[] }[], upper_bytes: number \| null }` |

At minimum define these reusable fragments:

```ts
type SampleDelta = {
  ts: number;
  sample_delta_ms: number;
  metrics: Record<string, unknown>;
  deltas: Record<string, unknown>;
};

type SnapshotNode = {
  sandbox_id: string;
  lifecycle_state: string;
  availability: "available" | "partial" | "unavailable";
  sampled_at_unix_ms: number | null;
  errors: string[];
  daemon: object;
  resources: { latest: SampleDelta | null, history: SampleDelta[] };
  workspaces: object[];
  stack?: { layer_count: number, layers_bytes: number, active_leases: number };
};
```

Do not flatten span/event/resource records into prose. Show representative nested JSON
and point to telemetry record types. Snapshot and layerstack assemblers are in
`OBS/response.rs`; dispatch and validation are in `OBS/query.rs`.

### Mandatory drift note: hidden layer detail mode

The `layerstack` handler accepts `layer_id` plus optional `limit` and returns:

```ts
{
  view: "layerstack",
  layer_id: string,
  entries: { path: string, kind: "file" | "symlink" | "directory" | "delete" | "opaque_dir" }[],
  truncated: boolean
}
```

Those arguments are absent from `LAYERSTACK_SPEC`, CLI projection, and generated MCP
schema (`CAT/observability/layerstack.rs`; `OBS/query.rs:89-178`). Treat this as an
**implementation-only, non-publicly-generated mode pending maintainer decision**. Do
not silently advertise it as supported public API and do not omit it from the reality
check.

Also call out that a raw RPC omitting catalog defaults can produce a different optional
shape (for example no `trend` on an inventory request), while CLI/MCP builders insert
the catalog default. Public examples must use generated-surface behavior.

## 8. Page 04 — CLI adapter

This page owns invocation mechanics, not operation semantics. It must include:

- One table mapping manager/runtime/observability domain → binary → scope-selector rule
  → public operation count (8/7/5).
- Links to the exact usage matrix in pages 01–03; do not create a second drifting list.
- A request example showing CLI flag/positional conversion into `args` and `scope`.
- A success example, an operation error example, and a local usage error example with
  stdout/stderr and exit code.
- The `create_sandbox --progress` exception: progress frames on stderr, `[Output]`
  delimiter, final JSON on stdout; progress text is not part of the operation result.
- A statement that `--workspace-bind-root` maps to catalog argument
  `workspace_root`; `--workspace-root` is an accepted compatibility alias.
- The Phase 0 fixture boundary and projection-integrity checks.

Primary anchors: `CLI/projection/*.rs`, `CLI/input.rs`, `CLI/output.rs`, and
`crates/sandbox-cli/tests/{projection_integrity,compatibility}.rs`.

## 9. Page 05 — MCP adapter

This page must include:

- One table mapping `--set management|runtime|observability` to the same 8/7/5 public
  operation names.
- JSON-schema mapping for every `ArgKind`, defaults, required arrays, and
  `additionalProperties: false`.
- Runtime `sandbox_id` injection and observability optional/required selector behavior.
- A `tools/list` excerpt and one `tools/call` example for each domain.
- Exact result wrapping: `content: []`, operation JSON in `structuredContent`, and
  `isError` based on the top-level error envelope.
- Streaming suppression (`_stream_logs: false`) and the fact that create progress is
  not returned over MCP.
- A note that the single binary compiles all catalogs; `--set` selects authority at
  runtime rather than at link time.

Primary anchors: `MCP/schema.rs`, `MCP/tools.rs`, `MCP/server.rs`, and
`crates/sandbox-mcp/tests/server.rs` plus tool-list fixtures.

## 10. Corrections and decisions to surface while writing

These are findings, not optional editorial notes:

1. **`create_sandbox` is output-polymorphic.** One sandbox returns a bare record; a
   batch returns `{sandboxes:[...]}`. Decide whether to preserve or normalize it, but
   document current behavior first.
2. **`layerstack` has uncatalogued `layer_id`/`limit` inputs.** Decide whether to add
   them to the public catalog/projections or remove the handler mode.
3. **`file_write` differs below the public builder.** The catalog requires `content`,
   while the runtime parser defaults a missing value to an empty string
   (`RT/operations/registry/file_operations.rs:164-170`). Public docs follow the
   catalog; the correction notes the direct-handler behavior.
4. **Output schemas have no catalog declaration.** They are inferred from handler JSON
   assembly and tests. Every page must label output shapes “current wire shape,” and
   the done-when checks should encourage exact-key contract tests for unpinned results.
5. **System and sandbox `snapshot` intentionally differ at the root.** System scope
   wraps an array; sandbox scope returns a node directly. Manager normalization also
   produces available/partial/unavailable node variants.
6. **Caps have mixed ownership.** Some defaults are catalog literals while maxima come
   from runtime configuration. State both current public value and configuration owner;
   do not imply every number is protocol-frozen.
7. **Internal session operations are real but not public.** Document them as composed
   architecture, pending a decision on whether explicit-session workflows should be
   exposed.

## 11. Verification plan

Before declaring the cluster complete:

1. Re-run the catalog census from `manager::operation_specs`,
   `runtime::operation_specs`, `observability::operation_specs`, internal routes, and
   runtime registry partitions. The documented totals must remain 20/21/5/1.
2. Compare every public argument row against both its `OperationSpec` and CLI
   projection. Compare MCP schemas against the generated tool-list fixtures.
3. Compare every success shape against the handler's JSON assembler and tests. Add a
   representative captured result only when it is deterministic and sanitized.
4. Search all operation declarations and handlers for uncatalogued names/args. Resolve
   or list every mismatch; `layer_id`/`limit` and `file_write.content` are the known
   baseline.
5. Run the focused proofs from the code repo:

```bash
cargo test -p sandbox-operation-catalog --all-features --test integrity
cargo test -p sandbox-cli --all-features --test projection_integrity
cargo test -p sandbox-manager --test manager_core
cargo test -p sandbox-manager --test manager_export
cargo test -p sandbox-runtime --test operation_registry
cargo test -p sandbox-runtime --test exec_command
cargo test -p sandbox-runtime --test file_operations
cargo test -p sandbox-observability-query --test query
cargo test -p sandbox-mcp --test server
```

6. Link-check page navigation and every cross-cluster “internals live in…” reference.
   Cluster 04 documents caller contracts; workspace mechanics remain in cluster 01,
   routing machinery in `00-foundations/03`, wire lifecycle in `00-foundations/02`,
   daemon HTTP in cluster 03, and export hardening in cluster 05.

## 12. Done-when checklist

The cluster is done only when:

- [ ] All 26 unique operation names occur exactly once in the inventory and have one
  canonical detailed subsection or an explicit link to their composing public operation.
- [ ] All 21 public route rows are represented, including both `snapshot` scopes.
- [ ] Every operation has purpose, availability, argument contract, success shape, and
  operation-specific failures.
- [ ] Every optional output key is distinguished from a present-but-null key.
- [ ] Every result variant has a stated selection condition.
- [ ] CLI and MCP pages map all 20 public operations without advertising internal or
  HTTP-only operations.
- [ ] Generated-surface behavior is distinguished from raw/direct-handler behavior.
- [ ] Known contract drift is visible and tied to a maintainer decision.
- [ ] The focused proof suite passes, or failures are recorded with the exact stale
  assumption they invalidate.
