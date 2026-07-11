# CLI adapter: catalog projection, scope, and process output

> **Cluster 04 — Operations, page 4 of 5.**
> Previous: [03 — Observability operations](03-observability-operations.md) ·
> Next: [05 — MCP adapter](05-mcp.md) ·
> [Architecture skeleton](../skelenton.md)

## Why this page exists

The three operation CLIs are deliberately thin adapters. They do not own the
operation names, requiredness, defaults, or runtime semantics: each binary
loads one semantic catalog, joins it to a hand-written argv projection, builds
the shared request envelope, and sends one newline-delimited request to the
gateway. This page defines that projection boundary and the observable process
contract—especially scope lifting, stdout versus stderr, exit status, and the
management progress stream. Operation arguments and result shapes remain in
the canonical references:

- [management usage matrix](01-management-operations.md#public-operation-matrix)
- [command and file usage matrix](02-command-and-file-operations.md#public-operation-matrix)
- [observability usage matrix](03-observability-operations.md#public-operation-matrix)

Source anchors are relative to the `ephemeral-sandbox` repository.

## Three binaries, three authority sets

| Domain | Binary | Scope selector rule | Public names |
|---|---|---|---:|
| Management | `sandbox-manager-cli` | Every request is system-scoped. An operation's `--sandbox-id`, when present, is ordinary fleet data in `args`, not the request scope. | 8 |
| Runtime | `sandbox-runtime-cli` | Global `--sandbox-id ID` is mandatory for every operation; there is no environment or config fallback. The builder lifts it into sandbox scope. | 7 |
| Observability | `sandbox-observability-cli` | `--sandbox-id ID` is operation-local. It is optional for `snapshot`, selecting system scope when absent and sandbox scope when present; it is required for the other four operations. | 5 |

The binaries are feature-gated independently (`crates/sandbox-cli/Cargo.toml:8-27`)
and each links only its catalog and projection. Their 8 + 7 + 5 commands are
the complete 20-name public set. Internal daemon RPCs and HTTP-only `file_list`
have no CLI projection; the projection-integrity test explicitly rejects their
appearance (`crates/sandbox-cli/tests/projection_integrity.rs:43-85`).

These domains select catalogs and binaries; they do not promise that every
request terminates in a same-named execution service. In particular, `cgroup`
remains an observability CLI command while its current sandbox route is owned
by the manager. The default operation scope reads Docker Engine stats there;
non-sandbox operation scopes currently encounter the forwarding drift recorded
in [the canonical cgroup contract](03-observability-operations.md#cgroup).

Use `help` or `help OPERATION` for generated human-readable help. `help` is a
reserved adapter command, not an operation sent to the gateway
(`crates/sandbox-cli/src/input.rs:108-129`). Invoking a binary with no operation
also renders catalog help. The full operation synopses, constraints, and
examples are linked above rather than duplicated here.

## How argv becomes an operation request

The projection gives every semantic argument exactly one flag or positional
binding, with optional compatibility aliases. At startup, `catalog_document`
requires the catalog and projection to agree on domain, operation count and
order, operation names, argument count and order, and uniqueness of every
binding (`crates/sandbox-cli/src/projection/document.rs:39-49,91-230`). A stale
projection therefore fails locally instead of silently sending a malformed
request.

The conversion rules are:

| Catalog kind | CLI token conversion | Local rejection |
|---|---|---|
| `string` | JSON string, unchanged | missing value or duplicate flag |
| `path` | JSON string, unchanged; semantic path checks happen in the operation owner | missing value or duplicate flag |
| `integer` | unsigned base-10 integer | negative or non-integer token |
| `float` | finite JSON number | parse failure, NaN, or infinity |
| `json_array` | parse the token as JSON and require an array | malformed JSON or any non-array value |

Unknown flags and excess positionals are rejected. Required projected
arguments are checked before I/O; then the shared builder rejects unknown
semantic keys, validates JSON kinds, inserts catalog defaults, generates a UUID
`request_id`, and removes a scope selector from `args`
(`crates/sandbox-cli/src/input.rs:172-299`;
`crates/sandbox-operations/client/src/request.rs:57-94,137-253`).

### Concrete runtime projection

```sh
sandbox-runtime-cli --sandbox-id eos-x \
  exec_command --yield-time-ms 0 "sleep 30"
```

The adapter constructs this semantic envelope:

```json
{
  "op": "exec_command",
  "request_id": "<fresh UUID>",
  "scope": {"kind": "sandbox", "sandbox_id": "eos-x"},
  "args": {"cmd": "sleep 30", "yield_time_ms": 0}
}
```

`cmd` came from the `COMMAND` positional, `yield_time_ms` became a number, and
the global selector became `scope`; `args.sandbox_id` is intentionally absent.
Before sending, `GatewayClient` adds the transport-only auth field when
configured and `_stream_logs:false` (`crates/sandbox-operations/client/src/client.rs:86-109`).
Those transport siblings are not part of `OperationRequest` and are removed at
the gateway.

Management is the important contrast:

```sh
sandbox-manager-cli create_sandbox \
  --image ubuntu:24.04 --workspace-bind-root /testbed
```

`--workspace-bind-root` projects to the catalog key `workspace_root`, the
builder inserts `count: 1`, and the envelope remains system-scoped. The old
`--workspace-root` spelling is still accepted as a compatibility alias
(`crates/sandbox-cli/src/projection/manager.rs:5-13`;
`crates/sandbox-cli/tests/request_builder.rs:93-114`). Both spellings are input
syntax only; neither becomes a wire key.

For observability, `sandbox-observability-cli snapshot` builds system scope and
empty args. Adding `--sandbox-id eos-x` builds sandbox scope and still removes
the selector from args. `trace`, `events`, `cgroup`, and `layerstack` reject a
missing selector before gateway I/O (`crates/sandbox-cli/src/input.rs:132-170`;
`crates/sandbox-cli/tests/observability.rs:52-137`).

## Gateway discovery and launch wrappers

All binaries accept global `--gateway-socket HOST:PORT` and
`--gateway-auth-token TOKEN`. Explicit flags normally override
`SANDBOX_GATEWAY_SOCKET` and `SANDBOX_GATEWAY_AUTH_TOKEN`; the endpoint then
defaults to `127.0.0.1:7878`, while the token has no library default. There is
one current precedence edge case: the library validates an environment token
before it applies an explicit token override, so an empty or whitespace-only
`SANDBOX_GATEWAY_AUTH_TOKEN` is a local `config_error` even when a valid flag
is present. Empty configured endpoints are also `config_error`s
(`crates/sandbox-operations/client/src/config.rs:6-8,35-86`).

The repository's `bin/sandbox-*-cli` shell wrappers add one convenience that
the Rust binaries do not: if the auth-token environment variable is unset or
empty, they read `${SANDBOX_GATEWAY_TOKEN_FILE:-/tmp/eos-gateway.token}`.
Whitespace is not empty to the shell, so it suppresses this fallback and is
then rejected by the Rust validator. A wrapper executes an existing
`target/debug` binary first and otherwise uses
`cargo run` with the corresponding feature (`bin/sandbox-manager-cli:7-18` and
the equivalent runtime/observability wrappers). When diagnosing an apparently
stale catalog, remember that an old executable in `target/debug` wins over a
fresh on-demand build.

## Stdout, stderr, and exit status

For an operation invocation, process output is machine-readable and
newline-terminated. A success is the operation's current wire JSON itself; the
CLI adds no `{result: ...}` wrapper. A top-level `error` key is the universal
failure discriminator.

| Outcome | stdout | stderr | Exit |
|---|---|---|---:|
| Operation success | exactly one compact JSON line | empty, unless progress was requested | 0 |
| Gateway operation error | empty | the returned error-envelope value, compactly reserialized as one JSON line | 1 |
| Connection or response-protocol failure | empty | a locally built `connection_error` or `protocol_error` envelope | 1 |
| CLI parse, projection, scope, or required-argument failure | empty | a local `invalid_request` envelope | 2 |
| Invalid gateway configuration | empty | a local `config_error` envelope | 2 |
| `help`, `help OPERATION`, or `--help` | human-readable help | empty | 0 |

The constants and routing are pinned in
`crates/sandbox-cli/src/output.rs:17-38,83-143,173-194`. In particular, an
operation-level command failure is not automatically a CLI failure. For
example, a valid `exec_command` result may contain a nonzero `exit_code` but
has no top-level error, so the adapter exits 0; callers must inspect the command
payload. Conversely, any response with top-level `error` exits 1.

### Success

```console
$ sandbox-manager-cli list_sandboxes
{"sandboxes":[]}
$ echo $?
0
```

The JSON line is on stdout; stderr is empty. Adapter tests also prove the
outgoing system scope, empty args, nonempty request id, and
`_stream_logs:false` (`crates/sandbox-cli/tests/manager.rs:256-279`).

### Operation or transport failure

```console
$ sandbox-manager-cli list_sandboxes 1>out.json 2>err.json
$ echo $?
1
$ cat out.json
$ cat err.json
{"error":{"kind":"operation_failed","message":"manager refused","details":{"reason":"fixture"}}}
```

Returned error envelopes are preserved field-for-field after JSON parsing.
A connect failure instead produces `kind:"connection_error"`; malformed,
empty, oversized, or non-newline-terminated gateway output produces
`kind:"protocol_error"` (`crates/sandbox-operations/client/src/client.rs:64-80,111-170`;
`crates/sandbox-cli/tests/manager.rs:281-325`).

### Local usage failure

```console
$ sandbox-runtime-cli exec_command pwd 1>out.json 2>err.json
$ echo $?
2
$ cat out.json
$ cat err.json
{"error":{"kind":"invalid_request","message":"runtime operations require --sandbox-id","details":{}}}
```

This request never reaches the gateway. The same local channel covers unknown
operations, flags without values, duplicate flags, malformed JSON arrays,
missing required arguments, and invalid scope selectors.

## Management progress is a side channel

The management binary alone can set `_stream_logs:true`. The preferred form is
the top-level global option before the operation, which currently applies to
**all eight management operations**:

```sh
sandbox-manager-cli --progress create_sandbox \
  --image ubuntu:24.04 --workspace-bind-root /testbed
```

For compatibility, only `create_sandbox` also consumes a trailing
operation-local `--progress` from its argv:

```sh
sandbox-manager-cli create_sandbox \
  --image ubuntu:24.04 --workspace-bind-root /testbed --progress
```

The first form is global; the second is the create-only exception. Runtime and
observability always send `_stream_logs:false`. This exact selection is in
`crates/sandbox-cli/src/manager.rs:24-44,82-136` and is proved both for global
progress on `list_sandboxes` and the legacy create form in
`crates/sandbox-cli/tests/manager.rs:187-235`.

Each gateway `cli_log(<JSON string>)` frame becomes a human line on stderr:

```text
[progress 0.137s] creating sandbox container
[progress 1.804s] daemon is ready
[Output]
```

The elapsed prefix is generated locally. On a successful final response the
CLI writes `[Output]` to stderr, then writes the final compact JSON line to
stdout. On a final error there is no delimiter and the error envelope follows
the progress lines on stderr. Progress messages and `[Output]` are not part of
the operation result and must not be parsed as JSON
(`crates/sandbox-cli/src/output.rs:95-120,180-188`;
`crates/sandbox-operations/client/src/client.rs:128-185`). Redirect stdout when
a script needs only the final payload.

## Compatibility and integrity boundaries

Two test families protect different promises:

1. **Projection integrity is current and exact.** Every public catalog route
   must have exactly one CLI operation projection; all semantic arguments must
   have unique bindings, and internal/HTTP-only operations must remain absent
   (`crates/sandbox-cli/tests/projection_integrity.rs:10-114`). The same checks
   also run when a binary joins its catalog and projection at startup.
2. **The Phase 0 fixture is an additive compatibility floor, not today's
   complete catalog.** `compatibility-catalog.json` pins each original
   operation's family, input specification, help text, examples, and primary
   CLI projection; it omits route/scope metadata and alternate flags. Current
   catalogs may add operations. The fixture therefore contains the original
   six management operations plus all seven runtime and five observability
   operations, while the exact current management count is eight. The
   `--workspace-root` alias is protected separately by `request_builder.rs`;
   unknown-operation stderr and exit 2 are also frozen
   (`crates/sandbox-cli/tests/compatibility.rs:8-112`;
   `crates/sandbox-cli/tests/request_builder.rs:93-114`).

Together these checks permit additive catalog growth while preventing an old
spelling, default, example, or failure channel from changing unnoticed. They
do not declare handler result schemas: current success shapes are still
assembled by operation owners and documented in pages 01–03.

## Source-of-truth map

| Concern | Authoritative source and proof |
|---|---|
| Operation-to-argv mappings | `crates/sandbox-cli/src/projection/{manager,runtime,observability}.rs` |
| Catalog/projection join invariants | `crates/sandbox-cli/src/projection/document.rs`; `crates/sandbox-cli/tests/projection_integrity.rs` |
| argv parsing, scope lifting, typed conversion | `crates/sandbox-cli/src/input.rs`; `crates/sandbox-cli/tests/request_builder.rs` |
| defaults and request envelope | `crates/sandbox-operations/client/src/request.rs` |
| gateway configuration and transport fields | `crates/sandbox-operations/client/src/{config,client}.rs` |
| stream rendering and process exit contract | `crates/sandbox-cli/src/output.rs`; domain adapter tests in `crates/sandbox-cli/tests/` |
| Phase 0 compatibility | `crates/sandbox-cli/tests/compatibility.rs` and `tests/fixtures/` |

## What this adapter intentionally does not expose

The CLI cannot invoke the five daemon-internal operations or HTTP-only
`file_list`; it cannot pass arbitrary envelope fields; and it cannot use the
uncatalogued observability `layerstack` detail inputs `layer_id` and `limit`.
Those are authority and catalog boundaries, not missing flags. See the
[operation census](01-management-operations.md#operation-census), the
[HTTP-only file-list contract](02-command-and-file-operations.md#file_list-http-only),
and the [layerstack drift note](03-observability-operations.md#contract-drift-layer-detail-mode)
for the underlying implementation reality.
