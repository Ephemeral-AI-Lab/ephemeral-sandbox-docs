# Observability operations: five views, six routes

> **Cluster 04 — Operations, page 3 of 5.**
> Previous: [02 — Command and file operations](02-command-and-file-operations.md) ·
> Next: [04 — CLI adapter](04-cli.md) ·
> [Architecture skeleton](../skelenton.md)

The observability catalog exposes five public names. They expand to six routes
because `snapshot` is the catalog's only `SystemOrSandbox` operation: an absent
`sandbox_id` selects a manager-owned fleet aggregate, while a present selector
selects one daemon-owned sandbox view. The other four operations always require
sandbox scope. `trace`, `events`, and `layerstack` are observability-owned;
`cgroup` is manager-owned and splits again inside its handler: the exact
`"sandbox"` resource scope is served from Docker, while other resource scopes
are forwarded toward the daemon.

This page is the caller contract: selection, defaults, current JSON shapes, and
operation errors. The NDJSON writer, rotation, trace propagation, sampling
pipeline, and record-folding implementation belong in the
[planned Cluster 07 observability page](../skelenton.md) rather than here.
Source anchors below are relative to the `ephemeral-sandbox` repository and
describe the implementation as of 2026-07-11.

## Public operation matrix

| Operation route | User job | Scope and execution owner | Public surfaces | Generated `args` when optional inputs are omitted |
|---|---|---|---|---|
| `snapshot` (fleet) | Live state plus latest resource facts | system → manager | `sandbox-observability-cli`; MCP set `observability` | `{}` |
| `snapshot` (one sandbox) | Live state plus latest resource facts | sandbox → observability query | same | `{}` |
| `trace` | One historical request flow | sandbox → observability query | same | `{"trace_id":"last"}` |
| `events` | Historical point-in-time facts across traces | sandbox → observability query | same | `{}` |
| `cgroup` | Live-sampled resource series for the sandbox; historical daemon series for other resource scopes | sandbox → manager; non-`"sandbox"` resource scopes are explicitly forwarded toward observability | same | `{"scope":"sandbox","window_ms":60000}` |
| `layerstack` | Live storage inventory or workspace sharing, optionally enriched from samples | sandbox → observability query | same | `{"window_ms":60000}` |

All five operations are public and logically read-only: none changes a
sandbox lifecycle, workspace, lease, or published layer. There are two
implementation-local cache effects. Each successful manager-side Docker stats
read—from exact-sandbox `cgroup` or fleet `snapshot`—appends a sample to
process-local memory. The live layer-byte sampler used by sandbox `snapshot`
and the `layerstack` inventory can create a missing
`.layer-metadata/<layer-id>.bytes` sidecar after a budgeted directory walk
(`crates/sandbox-observability/telemetry/src/collect/layerstack.rs:35-96`).

Catalog census and routing are declared in
`crates/sandbox-operations/catalog/src/observability.rs:21-56`; route expansion
is pinned by `crates/sandbox-operations/catalog/tests/integrity.rs` and
`crates/sandbox-observability/query/tests/query.rs:98-132`.

## Shared request and response contract

The CLI flag and MCP property named `sandbox_id` are **scope selectors**, not
operation arguments, for this domain. The shared builder lifts a selector into
the request envelope and removes any `args.sandbox_id` copy:

```ts
type ObservabilityRequest = {
  op: "snapshot" | "trace" | "events" | "cgroup" | "layerstack";
  request_id: string;
  scope:
    | { kind: "system" }
    | { kind: "sandbox"; sandbox_id: string };
  args: Record<string, unknown>;
};
```

For `snapshot`, no selector produces `{kind:"system"}` and a non-empty
selector produces sandbox scope. For the other operations, a missing or
whitespace-only selector is rejected locally before gateway I/O. The public
builder validates JSON kinds, rejects unknown keys, and inserts catalog
defaults (`crates/sandbox-operations/client/src/request.rs:57-94,107-204`).
Integer arguments are unsigned JSON integers. A forwarded sandbox id must also
pass the manager's current identifier grammar: non-empty ASCII alphanumeric,
`-`, `_`, or `.` (`crates/sandbox-manager/src/model.rs:8-24`).

Publicly generated requests therefore have these exact semantic fragments:

```json
{"op":"snapshot","scope":{"kind":"system"},"args":{}}
{"op":"snapshot","scope":{"kind":"sandbox","sandbox_id":"eos-a"},"args":{}}
{"op":"trace","scope":{"kind":"sandbox","sandbox_id":"eos-a"},"args":{"trace_id":"last"}}
{"op":"events","scope":{"kind":"sandbox","sandbox_id":"eos-a"},"args":{}}
{"op":"cgroup","scope":{"kind":"sandbox","sandbox_id":"eos-a"},"args":{"scope":"sandbox","window_ms":60000}}
{"op":"layerstack","scope":{"kind":"sandbox","sandbox_id":"eos-a"},"args":{"window_ms":60000}}
```

`request_id` is omitted above only to keep the fragments readable. CLI request
generation is pinned end to end in
`crates/sandbox-cli/tests/observability.rs:53-112`; generated MCP schemas are
pinned in
`crates/sandbox-mcp/tests/fixtures/observability-tools-list.json`.

A successful result is the operation payload itself—there is no shared
`result` wrapper. A failed operation uses the shared envelope, and current
observability handlers populate `details` with an empty object:

```ts
type OperationError = {
  error: {
    kind: string;
    message: string;
    details: Record<string, unknown>; // {} for errors described on this page
  };
};
```

The envelope is assembled by
`crates/sandbox-operations/contract/src/error.rs:7-48` and
`crates/sandbox-operations/contract/src/response.rs:38-51`. The CLI prints a
success payload on stdout and an error envelope on stderr; MCP exposes the same
value as structured content. Adapter mechanics live in [04 — CLI](04-cli.md)
and [05 — MCP](05-mcp.md).

Every sandbox request first reaches the manager router. For `snapshot`,
`trace`, `events`, and `layerstack`, the generic sandbox route forwards to the
daemon. The manager-owned `cgroup` route instead invokes a local handler. That
handler serves exact resource scope `"sandbox"` directly through the runtime;
it calls the normal manager forwarding helper only when the resource-scope
string is anything else.

The usual forwarding gates—a registry record in Ready state with a daemon
endpoint—therefore apply to the four observability-owned routes and to the
non-sandbox `cgroup` branch, but not to exact-sandbox `cgroup`. An invalid id,
missing record, non-Ready record, or missing endpoint is `invalid_request`; a
manager task/store/forwarding failure is `internal_error`. A daemon can return
`unknown_op` unchanged. Public builders reject a missing selector, unknown
argument, or wrong JSON kind locally as `invalid_request`, with the same empty
`details` object.

Typed skeletons below are labeled **current wire shape** because output schemas
are assembled in handlers rather than declared in the operation catalog. In
those skeletons, `field?: T` means the key can be absent, `field: T | null`
means the key is always present but nullable, and `T[]` is always an array
(possibly empty).

## What the views actually read

Daemon telemetry sampling is request-triggered, not periodic. A completed
runtime daemon RPC schedules a best-effort collection afterward; idle
sandboxes do not emit resource or stack samples. The observability RPC
dispatcher itself does not schedule another collection, so those daemon query
views normally see samples from earlier completed work
(`crates/sandbox-daemon/src/rpc/dispatch.rs:49-105`). Exact-sandbox `cgroup` and
fleet `snapshot` are different: each request takes one Docker Engine stats
sample for every locally served sandbox and records it in manager memory before
returning.

| View | Live inputs | Log inputs | Important limit |
|---|---|---|---|
| sandbox `snapshot` | runtime registry, in-flight executions, active stack | latest `sandbox` and per-workspace samples | resource `history` is currently always `[]` |
| fleet `snapshot` | manager Ready records, each daemon's sandbox snapshot, then one-shot host Docker Engine stats | daemon result unless a successful host sample replaces its resource bundle; manager process-local history receives that sample | default fan-out 8; per-daemon timeout 1,500 ms |
| `trace` | none | spans and their attached events | retained primary plus one rotated NDJSON file |
| `events` | none | events | no result-count cap unless `last_n` is supplied |
| `cgroup`, exact `"sandbox"` scope | one-shot host Docker Engine stats | process-local manager history, including the new sample | fixed 600,000 ms retention and request cap |
| `cgroup`, other scope (intended daemon path) | none | daemon samples for the named scope | currently rejected as `unknown_op` before the query handler |
| `layerstack` inventory | manifest, leases, cached/measured layer bytes | stack trend when a window and reader are available | configured lookback maximum on inventory mode |
| `layerstack` workspace | workspace lower layers and sharing | latest workspace `disk_bytes` | `window_ms` is currently ignored in this mode |

This corrects two catalog descriptions. Sandbox `snapshot` reads the log for
its `resources.latest`; fleet `snapshot` initially receives that daemon bundle
but replaces it after a successful host sample, preserving it only when host
sampling fails. The default public `layerstack` inventory reads the log for
`trend`. Their primary state is live, but these results are hybrid.

## Reusable current wire shapes

These records recur across the operation outputs:

```ts
type EventRecord = {
  ts: number;                         // unix milliseconds
  trace: string;
  parent?: string;                    // absent at a trace root
  name: string;
  attrs: Record<string, unknown>;
};

type SpanRecord = {
  ts: number;                         // completion time, unix milliseconds
  trace: string;
  span: string;
  parent?: string;
  name: string;
  dur_ms: number;
  status: "completed" | "error" | "cancelled" | "timed_out";
  attrs: Record<string, unknown>;
};

type SpanTreeNode = {
  span: SpanRecord;
  offset_ms: number;                  // span start minus trace start
  children: SpanTreeNode[];
  events: { offset_ms: number; event: EventRecord }[];
};

type SampleDelta = {
  ts: number;
  sample_delta_ms: number | null;     // null for the first in-window sample
  metrics: Record<string, unknown>;
  deltas: Record<string, unknown>;
};

type ResourceBundle = {
  latest: SampleDelta | null;
  history: SampleDelta[];             // currently always [] in snapshot
};
```

`parent` is conditionally absent, while `sample_delta_ms` is always present and
nullable. The telemetry types and ordering rules are in
`crates/sandbox-observability/telemetry/src/record.rs:93-172` and
`crates/sandbox-observability/telemetry/src/reader.rs:32-65,92-155`.

## `snapshot`

**Purpose and side effects.** Return current runtime state for one Ready
sandbox, or aggregate every Ready manager record that has a daemon endpoint.
The sandbox route is read-only apart from the missing layer-byte sidecar cache
write described above. The fleet route additionally attempts one host Docker
stats read per selected record and appends each successful sample to the
manager's process-local resource history.

**Availability.** Public; system → manager or sandbox → observability query;
`sandbox-observability-cli` and MCP set `observability`.

**Usage and request.**

```text
sandbox-observability-cli snapshot [--sandbox-id ID]
```

The logical `args` object is `{}` on both routes. Omitting `--sandbox-id`
creates system scope; supplying it creates sandbox scope. There is no operation
argument named `sandbox_id` after request construction.

**Arguments.**

| Input | JSON kind | Required | Default | Validation/cap | Meaning |
|---|---|---:|---|---|---|
| scope selector `sandbox_id` | string | no | absent → system scope | non-empty; manager grammar on forwarding | one sandbox when present, fleet aggregate when absent |

**Success output — current wire shape.** The two routes intentionally differ at
the root:

```ts
type SnapshotResult = SnapshotNode;                 // sandbox scope
type FleetSnapshotResult = { sandboxes: SnapshotNode[] }; // system scope

type SnapshotNode = {
  sandbox_id: string;
  lifecycle_state: "ready";
  availability: "available" | "partial" | "unavailable";
  sampled_at_unix_ms: number | null;
  errors: string[];
  daemon:
    | { daemon_pid: number; runtime_dir: string }
    | { host: string | null; port: number | null;
        daemon_pid: null; runtime_dir: null };
  resources: ResourceBundle;
  workspaces: WorkspaceSnapshot[];
  stack?: {
    layer_count: number;
    layers_bytes: number;
    active_leases: number;
  };
};

type WorkspaceSnapshot = {
  workspace_id: string;
  lifecycle_state: "active";
  network_profile: "shared" | "isolated";
  finalize_policy: "no_op" | "publish_then_destroy";
  layers: {
    base_root_hash: string | null;
    layer_count: number | null;
  };
  namespace_fd_count: number | null;
  resources: ResourceBundle;
  active_namespace_executions: {
    namespace_execution_id: string;
    operation: string;
    lifecycle_state: "running";
  }[];
};
```

A representative sandbox-scoped result, including the nested resource and
execution records, is:

```json
{
  "sandbox_id": "eos-a",
  "lifecycle_state": "ready",
  "availability": "available",
  "sampled_at_unix_ms": 1783760400100,
  "errors": [],
  "daemon": {"daemon_pid": 42, "runtime_dir": "/run/eos/eos-a"},
  "resources": {
    "latest": {
      "ts": 1783760400000,
      "sample_delta_ms": null,
      "metrics": {"cpu_usec": 1200, "mem_cur": 67108864},
      "deltas": {}
    },
    "history": []
  },
  "workspaces": [
    {
      "workspace_id": "ws-7",
      "lifecycle_state": "active",
      "network_profile": "isolated",
      "finalize_policy": "no_op",
      "layers": {"base_root_hash": "sha256:abc", "layer_count": 3},
      "namespace_fd_count": 5,
      "resources": {"latest": null, "history": []},
      "active_namespace_executions": [
        {
          "namespace_execution_id": "np-9",
          "operation": "exec_command",
          "lifecycle_state": "running"
        }
      ]
    }
  ],
  "stack": {"layer_count": 3, "layers_bytes": 8192, "active_leases": 1}
}
```

The system root wraps nodes. After each daemon result, the manager independently
attempts a host resource read. On success it replaces that node's entire
`resources` bundle with the new Docker sample and `history:[]`; on failure it
silently preserves the daemon-provided bundle (or the synthesized empty bundle
for an unavailable node). A daemon failure is data, not a top-level operation
failure, and a successful host read can therefore coexist with
`availability:"unavailable"`:

```json
{
  "sandboxes": [
    {
      "sandbox_id": "eos-a",
      "lifecycle_state": "ready",
      "availability": "available",
      "sampled_at_unix_ms": 1783760400100,
      "errors": [],
      "daemon": {"daemon_pid": 42, "runtime_dir": "/run/eos/eos-a"},
      "resources": {
        "latest": {
          "ts": 1783760400200,
          "sample_delta_ms": null,
          "metrics": {
            "metrics_source": "docker_engine",
            "cpu_usec": 1200,
            "mem_cur": 67108864,
            "mem_max": 536870912,
            "io_rbytes": 4096,
            "io_wbytes": 2048
          },
          "deltas": {}
        },
        "history": []
      },
      "workspaces": [],
      "stack": {"layer_count": 0, "layers_bytes": 0, "active_leases": 0}
    },
    {
      "sandbox_id": "eos-b",
      "lifecycle_state": "ready",
      "availability": "unavailable",
      "sampled_at_unix_ms": null,
      "errors": ["daemon request timed out"],
      "daemon": {
        "host": "127.0.0.1",
        "port": 4318,
        "daemon_pid": null,
        "runtime_dir": null
      },
      "resources": {
        "latest": {
          "ts": 1783760400210,
          "sample_delta_ms": null,
          "metrics": {
            "metrics_source": "docker_engine",
            "cpu_usec": 900,
            "io_rbytes": 0,
            "io_wbytes": 0
          },
          "deltas": {}
        },
        "history": []
      },
      "workspaces": []
    }
  ]
}
```

**Output variants.** A daemon result is `available` when runtime snapshotting
reported no partial errors and `partial` when `errors` is non-empty. `stack` is
conditionally absent when live stack observation fails; that failure does not
fail the snapshot. The manager synthesizes `unavailable` nodes for daemon
errors, malformed responses, timeouts, and worker panics. It bounds each such
error string to 4,096 bytes and keeps the fleet request successful. The manager
queries only Ready records with daemon endpoints, in waves bounded by
`manager.observability_snapshot.max_concurrent_requests` (default 8), with
`timeout_ms` per daemon (default 1,500 ms). Host sampling does not change
`availability` or add an error: success is visible through
`metrics_source:"docker_engine"`; failure is visible only because the original
daemon/empty resource bundle remains. Repeated fleet snapshots can make the
host sample's `sample_delta_ms` and counter `deltas` non-empty because they
share history with manager-served `cgroup`.

**Errors.** A sandbox-scoped request can return `invalid_request` for an invalid,
missing, non-Ready, or daemon-less sandbox during manager forwarding, and
`internal_error` for forwarding/task failures. A direct daemon snapshot returns
`internal_error` with `daemon observability is not configured` when it has no
reader context. A fleet registry failure is a top-level `internal_error`; a
single daemon failure is instead an `unavailable` node as above.

**Source of truth.** Catalog:
`crates/sandbox-operations/catalog/src/observability/snapshot.rs:5-29`;
CLI projection: `crates/sandbox-cli/src/projection/observability.rs:5-6,32-42`;
daemon handler/assembler:
`crates/sandbox-observability/query/src/query.rs:9-24` and
`crates/sandbox-observability/query/src/response.rs:14-47,173-223`; manager aggregate:
`crates/sandbox-manager/src/operations/management/service/impls/observability_snapshot.rs`;
manager host sample/assembler:
`crates/sandbox-manager/src/operations/management/service/impls/resource_metrics.rs:61-89,125-176`;
contracts: `crates/sandbox-observability/query/tests/query.rs:135-185`,
`crates/sandbox-manager/tests/manager_core.rs:719-879`, and
`crates/sandbox-manager/tests/manager_router.rs:231-280`.

## `trace`

**Purpose and side effects.** Fold completed telemetry records for one trace
into a read-only span forest with directly attached events.

**Availability.** Public; sandbox → observability query;
`sandbox-observability-cli` and MCP set `observability`.

**Usage and request.**

```text
sandbox-observability-cli trace --sandbox-id ID [--trace-id TRACE|last]
```

The public default produces `args = {"trace_id":"last"}`. `last` resolves to
the root span with the latest start time, not the record appended last.

**Arguments.**

| Input | JSON kind | Required | Default | Validation/cap | Meaning |
|---|---|---:|---|---|---|
| scope selector `sandbox_id` | string | yes | none | non-empty; manager grammar | daemon whose log is read |
| `trace_id` | string | no | `"last"` | trimmed value must be non-empty in handler; no length cap here | exact trace id or latest-root sentinel |

**Success output — current wire shape.**

```ts
type TraceResult = {
  view: "trace";
  trace: string;
  spans: SpanTreeNode[];
};
```

```json
{
  "view": "trace",
  "trace": "req-7f3",
  "spans": [
    {
      "span": {
        "ts": 1783760400250,
        "trace": "req-7f3",
        "span": "d-1",
        "name": "daemon.dispatch",
        "dur_ms": 250.0,
        "status": "completed",
        "attrs": {"op": "exec_command"}
      },
      "offset_ms": 0.0,
      "children": [
        {
          "span": {
            "ts": 1783760400200,
            "trace": "req-7f3",
            "span": "np-1",
            "parent": "d-1",
            "name": "namespace.exec.run_shell",
            "dur_ms": 180.0,
            "status": "completed",
            "attrs": {"exit_code": 0}
          },
          "offset_ms": 20.0,
          "children": [],
          "events": []
        }
      ],
      "events": [
        {
          "offset_ms": 15.0,
          "event": {
            "ts": 1783760400015,
            "trace": "req-7f3",
            "parent": "d-1",
            "name": "lease.acquired",
            "attrs": {"layer_id": "layer-a"}
          }
        }
      ]
    }
  ]
}
```

**Output variants.** Roots and sibling spans are ordered by start time
(`ts - dur_ms`); events attached to a span are ordered by event `ts`. A span
whose named parent is absent from the selected trace is re-rooted rather than
dropped. An unknown explicit trace id succeeds with `spans:[]`. If `last` finds
no root span, the result is `{view:"trace",trace:"last",spans:[]}`. Only events
whose `parent` names a returned span are attached to the tree.

**Errors.** `internal_error` when daemon observability is not configured;
`invalid_request` when a raw request omits `trace_id`, supplies an empty value,
or supplies the wrong JSON kind. Public CLI/MCP callers do not hit the omission
case because the builder inserts `"last"`.

**Source of truth.** Catalog:
`crates/sandbox-operations/catalog/src/observability/trace.rs:6-27`; projection:
`crates/sandbox-cli/src/projection/observability.rs:8-11,43-52`; handler:
`crates/sandbox-observability/query/src/query.rs:75-102`; tree model/fold:
`crates/sandbox-observability/telemetry/src/reader.rs:32-49,92-124,239-320`;
contract: `crates/sandbox-observability/query/tests/query.rs:187-334`.

## `events`

**Purpose and side effects.** Read a flat cross-trace stream of point-in-time
domain facts, optionally filtered and tail-limited; it does not mutate runtime
or telemetry state.

**Availability.** Public; sandbox → observability query;
`sandbox-observability-cli` and MCP set `observability`.

**Usage and request.**

```text
sandbox-observability-cli events --sandbox-id ID [--name NAME] [--since-ms MS] [--last-n N]
```

With no filters, generated public `args` is `{}`.

**Arguments.**

| Input | JSON kind | Required | Default | Validation/cap | Meaning |
|---|---|---:|---|---|---|
| scope selector `sandbox_id` | string | yes | none | non-empty; manager grammar | daemon whose log is read |
| `name` | string | no | no filter | trimmed; empty/whitespace becomes no filter | exact event-name match |
| `since_ms` | unsigned integer | no | `0` in the handler | no explicit cap; values above signed range clamp to `i64::MAX` | inclusive unix-ms lower bound |
| `last_n` | unsigned integer | no | no result cap | no configured maximum; `0` returns no events | retain the newest N matches |

**Success output — current wire shape.**

```ts
type EventsResult = {
  view: "events";
  events: EventRecord[];
};
```

```json
{
  "view": "events",
  "events": [
    {
      "ts": 1783760400015,
      "trace": "req-1",
      "parent": "d-1",
      "name": "lease.acquired",
      "attrs": {"layer_id": "layer-a"}
    },
    {
      "ts": 1783760400210,
      "trace": "req-2",
      "name": "lease.released",
      "attrs": {"layer_id": "layer-a"}
    }
  ]
}
```

**Output variants.** No matches is the successful `events:[]` case. Current
wire order is **oldest to newest** by `ts`. `last_n` removes older matches but
preserves ascending order among the retained newest N. This differs from the
catalog description's “newest first” wording; callers must follow current
wire behavior until that drift is resolved.

**Errors.** `internal_error` when daemon observability is not configured;
`invalid_request` for a wrong argument JSON kind. An unknown event name, a
future `since_ms`, and `last_n:0` are successful empty queries.

**Source of truth.** Catalog:
`crates/sandbox-operations/catalog/src/observability/events.rs:6-40`; projection:
`crates/sandbox-cli/src/projection/observability.rs:13-18,53-63`; handler:
`crates/sandbox-observability/query/src/query.rs:49-73,213-236`; ordering fold:
`crates/sandbox-observability/telemetry/src/reader.rs:74-90,144-155`;
contract: `crates/sandbox-observability/query/tests/query.rs:187-334`.

## `cgroup`

**Purpose and side effects.** Read a window of resource samples and derive
counter deltas. Exact resource scope `"sandbox"` takes a new Docker Engine
sample on every successful call and appends it to manager memory. Other scope
strings retain the older daemon-log query design. Neither branch changes
sandbox state, but the manager history is an ephemeral cache side effect.

**Availability.** Public; sandbox envelope → manager;
`sandbox-observability-cli` and MCP set `observability`. The local handler
serves resource scope `"sandbox"`; it attempts normal daemon forwarding for
every other resource-scope string. That second branch is currently broken at
the daemon routing boundary, as detailed below.

**Usage and request.**

```text
sandbox-observability-cli cgroup --sandbox-id ID [--scope SCOPE] [--window-ms MS]
```

Public omission produces
`args = {"scope":"sandbox","window_ms":60000}`.

**Arguments.**

| Input | JSON kind | Required | Default | Validation/cap | Meaning |
|---|---|---:|---|---|---|
| scope selector `sandbox_id` | string | yes | none | non-empty; manager grammar | sandbox/container to sample or daemon to forward to |
| `scope` | string | no | `"sandbox"` | exact string comparison; no trimming or membership validation | `"sandbox"` selects the manager/Docker branch; every other string selects forwarding |
| `window_ms` | unsigned integer | no | public builder and raw manager omission: `60000` | exact-sandbox branch: fixed maximum `600000`; `0` is accepted | manager-history lookback; intended daemon branch uses its configured lookback |

The manager checks `scope` before `window_ms`, so the fixed cap is applied only
to exact `"sandbox"`. A raw system-scope request is rejected on that local
branch; the public catalog generates only sandbox envelopes.

**Success output — reachable manager/Docker wire shape.**

```ts
type CgroupResult = {
  view: "cgroup";
  scope: "sandbox";
  series: SampleDelta[];
};
```

```json
{
  "view": "cgroup",
  "scope": "sandbox",
  "series": [
    {
      "ts": 1783760400000,
      "sample_delta_ms": null,
      "metrics": {
        "metrics_source": "docker_engine",
        "cpu_usec": 1200,
        "mem_cur": 67108864,
        "mem_max": 536870912,
        "io_rbytes": 4096,
        "io_wbytes": 2048
      },
      "deltas": {}
    },
    {
      "ts": 1783760401000,
      "sample_delta_ms": 1000,
      "metrics": {
        "metrics_source": "docker_engine",
        "cpu_usec": 1450,
        "mem_cur": 68157440,
        "mem_max": 536870912,
        "io_rbytes": 4608,
        "io_wbytes": 3072
      },
      "deltas": {"cpu_usec": 250, "io_rbytes": 512, "io_wbytes": 1024}
    }
  ]
}
```

**Manager/Docker output variants.** A successful call always returns at least
the sample it just recorded, including for `window_ms:0`. Fleet `snapshot`
host reads feed the same per-sandbox history, so earlier samples can come from
either public operation. History is held in a process-local `HashMap` and
disappears on manager restart. Each insert prunes samples older than 600,000
ms, then the response selects samples inside the requested window. Results
retain stored insertion order. The first selected
sample always has `sample_delta_ms:null` and `{}` deltas. Later samples contain
saturating deltas for exactly `cpu_usec`, `io_rbytes`, and `io_wbytes`.
Pruning occurs only when that sandbox is sampled again; destroy does not remove
its history entry, so an inactive id remains allocated until manager restart.

`metrics_source`, `cpu_usec`, `io_rbytes`, and `io_wbytes` are always present.
`mem_cur` and `mem_max` are independently absent when Docker omits usage or
limit. Docker's cumulative CPU nanoseconds are divided by 1,000. Block-I/O
read/write totals come from recursive service-byte entries, with Docker
storage-stat sizes as a fallback when both totals are zero.

**Intended daemon/workspace output.** The observability query crate still has
the historical scope handler and its open metric vocabulary. If invoked
directly, it returns the same `{view, scope, series}` root, can successfully
return `series:[]`, and reads the daemon-configured lookback maximum. Its
sandbox samples can include CPU, memory, cgroup availability, and errors;
workspace samples can include `disk_bytes`, `files`, and `disk_truncated`.
Only daemon metrics tagged as counters receive deltas; the current emitter tags
`cpu_usec`, not I/O.

That historical shape is **not currently reachable through the public
manager-to-daemon path**. The catalog now marks the only `cgroup` route as
manager-owned. The manager forwards non-`"sandbox"` scopes unchanged, but the
daemon recognizes a public observability request only when its catalog route
is observability-owned. It therefore sends forwarded `cgroup` to the runtime
dispatcher, which returns `unknown_op`, before the query handler can read a
workspace series.

**Errors.** On exact-sandbox scope, a wrong JSON kind, invalid sandbox id,
system envelope, or `window_ms > 600000` is `invalid_request`; a Docker/runtime
stats failure is `internal_error`. This branch does not require a manager store
record, Ready state, daemon endpoint, or configured daemon observability. On
other scope strings, normal forwarding-gate errors apply; after a successful
forward, the current daemon returns `unknown_op`. The intended daemon handler
would instead reject an oversized configured window as `invalid_request` and
missing observability configuration as `internal_error`.

**Source of truth.** Catalog:
`crates/sandbox-operations/catalog/src/observability/cgroup.rs:6-34`; projection:
`crates/sandbox-cli/src/projection/observability.rs:20-24,64-73`; manager
dispatch, validation, and output:
`crates/sandbox-manager/src/operations/management/service/impls/resource_metrics.rs:13-151`;
manager history: `crates/sandbox-manager/src/operations/services.rs:10-52`;
Docker input and conversion:
`crates/sandbox-provider-docker/src/engine.rs:282-306,519-555`; daemon routing
gate: `crates/sandbox-daemon/src/rpc/dispatch.rs:49-70,120-128`; retained daemon
query shape: `crates/sandbox-observability/query/src/query.rs:26-47,238-252`
and `crates/sandbox-observability/query/src/response.rs:49-57,184-191`.

## `layerstack`

**Purpose and side effects.** Return either the live active-layer inventory or
one workspace's lower-layer sharing, enriched with historical metrics when
available; inventory byte measurement may populate missing byte sidecars but
does not change the manifest, leases, or workspace.

**Availability.** Public; sandbox → observability query;
`sandbox-observability-cli` and MCP set `observability`. The handler also has an
implementation-only layer-detail variant documented separately below.

**Usage and request.**

```text
sandbox-observability-cli layerstack --sandbox-id ID [--workspace-id WS] [--window-ms MS]
```

Public omission produces `args = {"window_ms":60000}`. A non-empty
`workspace_id` selects workspace mode; absent or whitespace-only selects
inventory mode.

**Arguments.**

| Input | JSON kind | Required | Default | Validation/cap | Meaning |
|---|---|---:|---|---|---|
| scope selector `sandbox_id` | string | yes | none | non-empty; manager grammar | daemon whose runtime is queried |
| `workspace_id` | string | no | inventory mode | trimmed; unknown id is rejected | select workspace-sharing mode |
| `window_ms` | unsigned integer | no | public builder: `60000` | inventory: configured maximum, currently `600000`; workspace: currently ignored and not cap-checked | stack-trend lookback in inventory mode |

**Success output — current wire shape.** Public callers can receive two root
variants:

```ts
type LayerstackInventory = {
  view: "layerstack";
  manifest_version: number;
  root_hash: string;
  active_lease_count: number;
  total_bytes: number;
  layers: {
    layer_id: string;
    bytes: number;
    leased_by_workspaces: number;
    booked_by: string[];
  }[];
  trend?: {
    ts: number;
    [metric: string]: unknown;
  }[];
};

type WorkspaceLayerstack = {
  view: "layerstack";
  workspace: string;
  mounts: {
    layer_id: string;
    shared_with: string[];
  }[];
  upper_bytes: number | null;
};
```

Generated inventory requests normally include `trend` when daemon
observability is configured, even when there are no samples:

```json
{
  "view": "layerstack",
  "manifest_version": 7,
  "root_hash": "sha256:abc",
  "active_lease_count": 2,
  "total_bytes": 12288,
  "layers": [
    {
      "layer_id": "layer-new",
      "bytes": 4096,
      "leased_by_workspaces": 1,
      "booked_by": []
    },
    {
      "layer_id": "layer-base",
      "bytes": 8192,
      "leased_by_workspaces": 0,
      "booked_by": ["layer-new"]
    }
  ],
  "trend": [
    {
      "ts": 1783760400000,
      "layer_count": 2,
      "layers_bytes": 12288,
      "active_leases": 2
    }
  ]
}
```

```json
{
  "view": "layerstack",
  "workspace": "ws-7",
  "mounts": [
    {"layer_id": "layer-new", "shared_with": []},
    {"layer_id": "layer-base", "shared_with": ["ws-8"]}
  ],
  "upper_bytes": 4096
}
```

**Output variants.** Inventory `layers` follow manifest observation order.
`booked_by` contains leased **layer ids above the current layer**, not workspace
ids. A layer missing from the byte observation gets `bytes:0`; `total_bytes` is
the byte sampler's total. `trend` contains raw stack metrics plus `ts`, not
`SampleDelta` records—there is no `sample_delta_ms` or `deltas` key.

`trend` is conditionally absent. A raw RPC that omits the catalog default has
no trend, and an unconfigured daemon has no reader with which to add one. The
live inventory can still succeed in the latter case. Workspace mode never has
`trend`; `upper_bytes` is always present and is null when no latest workspace
`disk_bytes` sample exists. A raw `window_ms` value, including one above the
configured cap, is currently ignored in workspace mode.

**Errors.** Inventory returns `invalid_request` when `window_ms` exceeds the
configured maximum and `internal_error` when live stack observation fails.
Workspace mode returns `invalid_request` for an unknown workspace. Wrong JSON
kinds are `invalid_request`. Like manager-served exact-sandbox `cgroup`, the
live layerstack variants can succeed when observability logging is not
configured; `snapshot`, `trace`, and `events` cannot.

**Source of truth.** Catalog:
`crates/sandbox-operations/catalog/src/observability/layerstack.rs:6-34`;
projection: `crates/sandbox-cli/src/projection/observability.rs:26-30,74-83`;
dispatch/validation: `crates/sandbox-observability/query/src/query.rs:104-152,188-200`;
assemblers: `crates/sandbox-observability/query/src/response.rs:59-171`;
contracts: `crates/sandbox-observability/query/tests/query.rs:336-479` and
`crates/sandbox-observability/query/tests/query.rs:481-499`.

## Contract drift: layer detail mode

The `layerstack` handler accepts a third, implementation-only variant selected
by `layer_id`, with an optional `limit`:

```ts
type LayerDetail = {
  view: "layerstack";
  layer_id: string;
  entries: {
    path: string;
    kind: "file" | "symlink" | "directory" | "delete" | "opaque_dir";
  }[];
  truncated: boolean;
};
```

```json
{
  "view": "layerstack",
  "layer_id": "layer-new",
  "entries": [
    {"path": "app/config.json", "kind": "file"},
    {"path": "tmp/old", "kind": "delete"},
    {"path": "var/cache", "kind": "opaque_dir"}
  ],
  "truncated": false
}
```

The direct-handler inputs are:

| Input | JSON kind | Required | Default | Validation/cap | Meaning |
|---|---|---:|---|---|---|
| `layer_id` | string | yes for this mode | none | trimmed, non-empty, must name an observed layer | select a layer delta |
| `limit` | unsigned integer | no | configured `layer_delta_default_limit`, currently `500` | configured `layer_delta_max_limit`, currently `5000`; `0` is accepted | maximum returned entries |

`workspace_id` and `layer_id` together are `invalid_request`. An unknown layer
is `invalid_request`; stack-observation and delta-inspection failures are
`internal_error`. `truncated` says the layer contains more entries than the
applied limit. `window_ms`, if present on this raw mode, is ignored.

This is **not a publicly generated contract**. `layer_id` and `limit` are absent
from `LAYERSTACK_SPEC`, the CLI projection, and the generated MCP schema. The
shared public request builder therefore rejects either key as unknown; only a
caller bypassing catalog construction can reach the handler mode. Maintainers
must either add both inputs and this result variant to the catalog/projections,
or remove the handler path. Until that decision, callers must not rely on it as
supported CLI or MCP API.

The drift is visible by comparing
`crates/sandbox-operations/catalog/src/observability/layerstack.rs:11-33` with
`crates/sandbox-observability/query/src/query.rs:104-125,154-186,254-268` and
is covered at the handler layer by
`crates/sandbox-observability/query/tests/query.rs:425-479`.

## Current route and compatibility drift

The caller shapes above follow executable behavior. As of 2026-07-11, the
manager/Docker `cgroup` delta has not been propagated through every ownership
and compatibility check:

1. Catalog integrity still expects `cgroup` owner `Observability`, while the
   route now declares `Manager`.
2. The observability query registry still registers its retained `cgroup`
   handler, but its bijection test derives an owner-filtered route set that no
   longer contains `cgroup`.
3. The daemon's focused concrete-cgroup test now receives `unknown_op` rather
   than a series because the daemon dispatch gate rejects manager-owned routes
   as observability queries.
4. CLI Phase-0 compatibility and MCP tools-list fixture tests retain the old
   public `cgroup` description. The source description changed, so both exact
   compatibility checks fail. Refreshing those fixtures would redefine a
   compatibility baseline; it is not a documentation-only repair.

The first three failures expose the current non-sandbox forwarding gap, rather
than invalidating the retained direct query-handler shape documented above.
The fourth requires an explicit compatibility decision: restore the Phase-0
description or deliberately version/update the baseline.

Coverage is also asymmetric. Manager router tests prove the default branch
returns `view:"cgroup"`, `scope:"sandbox"`, and
`metrics_source:"docker_engine"`, and prove a non-sandbox scope invokes a fake
daemon client. They do not exercise a real manager-to-daemon dispatch, exact
metric/delta/history shapes, fixed-cap and runtime errors, missing or non-Ready
records on the local branch, or optional memory. The Docker provider currently
has no unit tests for CPU conversion, block-I/O aggregation/fallback, or stats
errors. One manager-core test proves that fleet `snapshot` replaces
`resources.latest` with three representative host fields; it does not pin the
full bundle, Docker-failure preservation, or the independent combination of an
unavailable daemon node with a successful host sample.

The failing assertions are located in
`crates/sandbox-operations/catalog/tests/integrity.rs:203-209`,
`crates/sandbox-observability/query/tests/query.rs:97-110`,
`crates/sandbox-daemon/tests/unit/observability.rs:166-196`,
`crates/sandbox-cli/tests/compatibility.rs:8-61`, and
`crates/sandbox-mcp/tests/server.rs:227-269`.

Separately, four catalog descriptions should not be mistaken for current wire
guarantees:

1. `events` catalog prose says “newest first”; the reader sorts by `ts`
   ascending, and `last_n` preserves ascending order among the retained tail.
2. `snapshot` says “does not read the log”; its live result reads the latest
   sandbox and workspace resource samples.
3. `layerstack` says “does not read the log”; a generated inventory request
   asks for a 60-second stack trend, and workspace mode reads latest upperdir
   bytes.
4. `cgroup`'s combined summary says CPU, memory, I/O, and disk. The reachable
   manager/Docker branch emits CPU, optional memory, and I/O but no workspace
   disk; the retained daemon branch emits CPU, memory, and workspace disk but
   no I/O.

The uncatalogued layer-detail mode is the structural drift requiring a public
API decision. The other items require either catalog wording changes or code
changes plus contract tests. In every case, a raw RPC can also differ from a
CLI/MCP call because raw requests bypass catalog-default insertion: missing
`trace_id` errors, missing manager `cgroup` `window_ms` uses its hard-coded
60,000 ms default, a directly invoked retained daemon `cgroup` handler uses its
configured maximum, and missing inventory `window_ms` omits `trend`.

## Navigation

[Architecture skeleton](../skelenton.md) ·
[01 — Management operations](01-management-operations.md) ·
[02 — Command and file operations](02-command-and-file-operations.md) ·
**03 — Observability operations** ·
[04 — CLI adapter](04-cli.md) ·
[05 — MCP adapter](05-mcp.md)
