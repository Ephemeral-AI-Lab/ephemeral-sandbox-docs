# MCP adapter: generated tools and structured results

> **Cluster 04 — Operations, page 5 of 5.**
> Previous: [04 — CLI adapter](04-cli.md) ·
> [Architecture skeleton](../skelenton.md)

## Why this page exists

`sandbox-mcp` exposes one operation catalog as one MCP tool set over stdio. It
generates input schemas from the same argument specifications used by the CLI,
uses the same request builder and gateway client, and returns operation JSON as
MCP structured content. This page defines the adapter layer: set selection,
schema generation, scope lifting, JSON-RPC examples, and result/error wrapping.
The operation semantics and current wire shapes remain canonical in:

- [management operations](01-management-operations.md)
- [command and file operations](02-command-and-file-operations.md)
- [observability operations](03-observability-operations.md)

Source anchors are relative to the `ephemeral-sandbox` repository.

## One process exposes exactly one public set

Start the stdio server with one required set:

```sh
sandbox-mcp --set management
sandbox-mcp --set runtime
sandbox-mcp --set observability
```

| `--set` | Tools, in `tools/list` order | Count |
|---|---|---:|
| `management` | `create_sandbox`, `list_docker_images`, `list_workspace_directories`, `destroy_sandbox`, `list_sandboxes`, `inspect_sandbox`, `squash_layerstacks`, `export_changes` | 8 |
| `runtime` | `exec_command`, `write_command_stdin`, `read_command_lines`, `file_read`, `file_write`, `file_edit`, `file_blame` | 7 |
| `observability` | `snapshot`, `trace`, `events`, `cgroup`, `layerstack` | 5 |

These are the same 20 public names as the CLIs. There are no tools for the five
daemon-internal operations or HTTP-only `file_list`. `--set all`, comma-joined
sets, an unknown set, and an omitted `--set` are startup usage errors with exit
2 (`crates/sandbox-mcp/src/config.rs:6-24`;
`crates/sandbox-mcp/tests/server.rs:815-862`). Run separate MCP processes when
one client should receive more than one authority set.

The set is a catalog/discovery boundary, not an assertion about the terminal
execution service. `cgroup` remains in the observability set even though its
current sandbox route is manager-owned: the default operation scope reads
Docker Engine stats in the manager, while other operation scopes currently hit
the forwarding drift described in [the cgroup contract](03-observability-operations.md#cgroup).

The single executable nevertheless compiles all three catalog features
(`crates/sandbox-mcp/Cargo.toml:8-15`). `--set` chooses one decoded catalog at
runtime; it is an authority and discoverability boundary, not a link-time
feature switch (`crates/sandbox-mcp/src/catalog.rs:7-20`). A server can
initialize and answer `tools/list` without contacting the gateway. Gateway I/O
starts only on `tools/call`.

Gateway discovery is shared with the CLI: explicit `--gateway-socket` and
`--gateway-auth-token` normally override `SANDBOX_GATEWAY_SOCKET` and
`SANDBOX_GATEWAY_AUTH_TOKEN`; the endpoint defaults to `127.0.0.1:7878`.
Current discovery eagerly validates an environment token, so an empty or
whitespace-only `SANDBOX_GATEWAY_AUTH_TOKEN` is a startup `config_error` even
when a valid explicit token was supplied. Unlike the repository CLI wrappers,
`sandbox-mcp` itself does not read the gateway token file
(`crates/sandbox-mcp/src/config.rs:19-36`;
`crates/sandbox-operations/client/src/config.rs:35-86`).

## `tools/list`: catalog to JSON Schema

For every selected catalog operation, MCP uses the operation name unchanged,
the full catalog description, and a generated object `inputSchema`. A compact
runtime excerpt is:

```json
{
  "tools": [
    {
      "name": "exec_command",
      "description": "Start a shell command in a workspace session. …",
      "inputSchema": {
        "type": "object",
        "properties": {
          "sandbox_id": {
            "type": "string",
            "description": "Target sandbox id (selects the daemon to query)."
          },
          "workspace_session_id": {"type": "string", "description": "…"},
          "cmd": {"type": "string", "description": "Shell command text."},
          "timeout_ms": {"type": "integer", "minimum": 0, "description": "…"},
          "yield_time_ms": {"type": "integer", "minimum": 0, "description": "…"}
        },
        "required": ["sandbox_id", "cmd"],
        "additionalProperties": false
      }
    }
  ]
}
```

The ellipses abbreviate descriptions only; they are not wire values. The full
descriptions come verbatim from the catalog.

### Complete kind mapping

| Catalog `ArgKind` | MCP property schema | Notes |
|---|---|---|
| `String` | `{"type":"string"}` | No implicit enum or pattern. |
| `Path` | `{"type":"string"}` | No JSON Schema `format`; owner-side path policy remains authoritative. |
| `Integer` | `{"type":"integer","minimum":0}` | Matches the shared builder's unsigned-integer contract. |
| `Float` | `{"type":"number"}` | JSON numbers are used; handler validation still owns semantic range. |
| `JsonArray` | `{"type":"array"}` | Native arrays, not CLI-style JSON strings; item structure is described in help and checked by the handler. |

Every property gets the catalog argument help as `description`. A catalog
default is parsed into its native JSON kind and emitted as `default`; the same
shared builder inserts that value when a caller omits it. Required catalog
arguments appear in `required`, and that array is present even when empty.
Every tool has `additionalProperties:false`
(`crates/sandbox-mcp/src/schema.rs:21-92`). Calls that bypass client-side schema
validation are still checked by the shared builder, so unknown keys, wrong
kinds, and missing required values fail locally before gateway I/O.

The generated schema intentionally does **not** encode all semantic rules. It
does not derive string enums such as `export_changes.format`, operation-specific
minimums such as `create_sandbox.count >= 1`, path absoluteness, configured
caps, detailed `file_edit` item fields, or handler-only output schemas. Those
constraints live in the canonical operation pages and remain enforced by the
operation parser/owner. Output schemas are not declared in the catalog at all;
`tools/list` therefore describes inputs only.

### Scope selectors

Scope is not exposed as an arbitrary MCP property. The adapter accepts only a
catalog-approved `sandbox_id` selector and creates the envelope itself:

| Set | Tool schema behavior | Built request |
|---|---|---|
| Management | Uses catalog arguments unchanged. A management `sandbox_id` is ordinary operation data. | Always `scope:{kind:"system"}`; management args stay in `args`. |
| Runtime | Injects required string property `sandbox_id` before all catalog arguments. | Lifts it to `scope:{kind:"sandbox",sandbox_id:…}` and removes it from `args`. |
| Observability | `sandbox_id` is already in each catalog spec: optional on `snapshot`, required on the other four tools. | Absence on `snapshot` chooses system scope; presence chooses sandbox scope and is removed from `args`. |

The injection is generated in `crates/sandbox-mcp/src/schema.rs:38-69`; route
selection and lifting are in `crates/sandbox-mcp/src/tools.rs:59-139`. Empty or
non-string selectors and missing required selectors become structured
`invalid_request` tool errors. Fields such as `scope`, `request_id`, auth
tokens, daemon endpoints, `view`, `set`, and export tokens are neither schema
properties nor accepted hidden controls
(`crates/sandbox-mcp/tests/server.rs:273-377,649-744`).

## `tools/call`: one example per domain

The following are client-to-MCP JSON-RPC lines. `id` values are examples; the
MCP adapter independently generates the operation request UUID.

### Management

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"create_sandbox","arguments":{"image":"ubuntu:24.04","workspace_root":"/workspace"}}}
```

MCP uses semantic argument names, so this is `workspace_root`, not the CLI-only
flag spelling `--workspace-bind-root`. The outgoing operation request is
system-scoped and has
`args:{"image":"ubuntu:24.04","workspace_root":"/workspace","count":1}`;
the shared builder inserted the catalog default.

### Runtime

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"file_edit","arguments":{"sandbox_id":"eos-x","path":"notes.txt","edits":[{"old_string":"one","new_string":"two"}]}}}
```

`edits` remains a native JSON array. The outgoing envelope is scoped to
`eos-x`; its args are only `path` and `edits`. No caller-provided
`args.sandbox_id` reaches the runtime.

### Observability

```json
{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"snapshot","arguments":{}}}
```

With no selector this uses the public system route and returns the aggregate
snapshot shape. Supplying `{"sandbox_id":"eos-x"}` selects the distinct
sandbox route and node shape. For a default-insertion example, calling `trace`
with only `sandbox_id` removes that selector from args and sends
`args:{"trace_id":"last"}`. These route and native-array behaviors are pinned
in `crates/sandbox-mcp/tests/server.rs:505-647`.

## Exact result wrapping

An operation success payload is still the top-level operation JSON documented
on pages 01–03. There is no operation-level `{result: ...}` wrapper. JSON-RPC
necessarily adds its own outer `result`, and MCP places the operation value in
that result's `structuredContent`:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [],
    "structuredContent": {"sandboxes": []},
    "isError": false
  }
}
```

The adapter always returns an empty textual `content` array, sets no `_meta`,
and mirrors the presence of the operation value's top-level `error` key into
`isError` (`crates/sandbox-mcp/src/server.rs:66-80`). Thus the object at
`result.structuredContent` preserves the parsed operation response's JSON
value semantics; the object at `result` is MCP protocol framing.

For an owner-returned error, local validation error, connection failure, or
gateway protocol failure, `tools/call` still succeeds at the JSON-RPC method
level and returns a tool error:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [],
    "structuredContent": {
      "error": {
        "kind": "operation_failed",
        "message": "publish failed",
        "details": {"phase": "publish", "retryable": false}
      }
    },
    "isError": true
  }
}
```

Gateway operation errors preserve `kind`, `message`, and `details`. Local
builder failures use `invalid_request`; gateway connection failures use
`connection_error`; malformed gateway responses use `protocol_error`
(`crates/sandbox-mcp/src/tools.rs:39-57,142-155`;
`crates/sandbox-mcp/tests/server.rs:746-788`). Unsupported MCP methods are the
different case: prompts, resources, and completion return JSON-RPC
method-not-found rather than a tool result (`crates/sandbox-mcp/src/server.rs:83-115`).

Although the shared operation response type can hold any JSON value,
`sandbox-mcp` currently requires a gateway success response to be a JSON
object. A scalar or array is converted to a `protocol_error`; all current
documented operation outputs are objects. This adapter restriction is explicit
in `crates/sandbox-mcp/src/tools.rs:45-54` and tested with an array response in
`crates/sandbox-mcp/tests/server.rs:768-788`.

## No progress stream over MCP

MCP dispatch calls `GatewayClient::send`, whose fixed behavior is
`send_with_logs(..., false, ...)`. Every gateway request therefore carries
`_stream_logs:false` (`crates/sandbox-operations/client/src/client.rs:31-33,86-109`;
`crates/sandbox-mcp/tests/server.rs:443-453`). In particular,
`create_sandbox` progress frames are not returned as MCP text, notifications,
or structured content. The tool waits for and returns only the final operation
object. Callers needing the current progress side channel must use the
[management CLI progress mode](04-cli.md#management-progress-is-a-side-channel).

## Protocol surface and lifecycle

The server advertises MCP protocol version `2025-06-18` and only the tools
capability. It serves over stdin/stdout until the client closes the transport
(`crates/sandbox-mcp/src/server.rs:42-64`;
`crates/sandbox-mcp/src/lib.rs:17-35`). Prompts, resources, resource templates,
and completion are deliberately unimplemented. Configuration errors happen
before stdio serving and exit 2; later projection/server failures exit 1 and
are diagnostic text on process stderr (`crates/sandbox-mcp/src/main.rs:6-21`).

## Fixture boundary and contract checks

The MCP server tests make two complementary assertions:

1. Generated `tools/list` names exactly match the current 8/7/5 catalog lists,
   every current spec has one tool, and every property kind/default/required
   marker matches its catalog argument.
2. The checked-in tool-list fixtures are the **Phase 0 compatibility floor**.
   The management fixture has the original six tools, so tests require those
   definitions to remain identical while separately allowing and checking the
   newer `list_docker_images` and `list_workspace_directories`. Runtime and
   observability fixtures already cover their current 7/5 sets.

This is additive compatibility, not evidence that a six-tool management
`tools/list` is current (`crates/sandbox-mcp/tests/server.rs:227-428`). Tool-call
tests then compare request building with the shared builder, assert scope and
defaults, preserve native edit arrays, reject hidden operations before network
I/O, and pin exact result wrapping (`crates/sandbox-mcp/tests/server.rs:191-217,443-788`).

## Source-of-truth map

| Concern | Authoritative source and proof |
|---|---|
| Runtime set selection and gateway configuration | `crates/sandbox-mcp/src/{config,catalog}.rs` |
| Tool names, descriptions, and input schemas | `crates/sandbox-mcp/src/schema.rs`; tool-list assertions and fixtures in `crates/sandbox-mcp/tests/` |
| Scope selection, defaults, request construction, transport errors | `crates/sandbox-mcp/src/tools.rs`; shared builder in `crates/sandbox-operations/client/src/request.rs` |
| JSON-RPC/MCP result shape and advertised capability | `crates/sandbox-mcp/src/server.rs` |
| Stdio lifecycle and process errors | `crates/sandbox-mcp/src/{lib,main}.rs` |

The adapter exposes only generated public inputs. Consequently the
implementation-only `layerstack.layer_id`/`limit` mode is absent from MCP, the
runtime parser's missing-`file_write.content` fallback cannot be reached
through a valid generated call, and no internal/session/file-list authority is
accidentally added. Those differences are documented where the operations are
canonical rather than normalized away here.
