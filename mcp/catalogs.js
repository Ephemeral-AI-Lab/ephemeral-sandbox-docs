(() => {
  "use strict";

  const field = (type, description, extra = {}) => ({ type, description, ...extra });
  const schema = (properties = {}, required = []) => ({
    type: "object",
    properties,
    required,
    additionalProperties: false
  });
  const sandboxId = () => field("string", "Target sandbox id (selects the daemon to query).");
  const managerSandboxId = () => field("string", "Sandbox id.");

  const sandboxRecord = {
    id: "sbox-example",
    workspace_root: "/host/workspaces/example",
    state: "ready",
    daemon: { host: "127.0.0.1", port: 41001 },
    daemon_http: { host: "127.0.0.1", port: 42001 },
    shared_base: {
      source: "/host/cache/shared-base/rootfs",
      target: "/eos/layer-stack/shared-base",
      root_hash: "sha256:…",
      readonly: true
    }
  };

  const commandOutput = {
    command_session_id: "namespace_execution_42",
    workspace_session_id: "workspace_17",
    status: "running",
    exit_code: null,
    wall_time_seconds: 0.25,
    command_total_time_seconds: 0.25,
    start_offset: 0,
    end_offset: 2,
    total_lines: 2,
    original_token_count: 4,
    output: "building…\n"
  };

  window.MCP_CATALOGS = {
    management: {
      label: "Management",
      eyebrow: "Fleet control",
      server: "ephemeral-os-management",
      command: "sandbox-mcp --set management",
      accent: "management",
      summary: "Host-side discovery, sandbox lifecycle, and delivery of published layer changes.",
      guidance: [
        "Use this catalog when the manager—not an individual sandbox daemon—owns the operation.",
        "Discovery and inspection calls are read-only. Creation, destruction, squash, and export change durable state.",
        "Sandbox identifiers are opaque strings returned by create_sandbox, list_sandboxes, or inspect_sandbox."
      ],
      families: [
        {
          id: "discovery",
          label: "Host discovery",
          description: "Read-only pickers for locally available images and workspace roots.",
          tools: [
            {
              name: "list_docker_images",
              summary: "List local Docker image references",
              risk: "safe",
              description: "List every local Docker image reference, including untagged image IDs that can create a sandbox.",
              manual: [
                "Call before create_sandbox when the caller needs a valid local image reference.",
                "The list may contain tags, digests, and untagged image IDs. Pass the chosen string unchanged as create_sandbox.image.",
                "This is host discovery only; it does not pull an image or create a sandbox."
              ],
              schema: schema(),
              request: {},
              output: { images: ["ubuntu:24.04", "sha256:abc123…"] },
              outputNote: "images is the complete set returned by the configured runtime provider."
            },
            {
              name: "list_workspace_directories",
              summary: "Browse allowed workspace directories",
              risk: "safe",
              description: "List picker-visible workspace roots when path is omitted, or up to 500 immediate local subdirectories of a selected workspace directory.",
              manual: [
                "Omit path to list picker-visible roots, then pass a returned absolute path to browse one level deeper.",
                "Only immediate subdirectories are returned. Continue calling with a selected child path to walk the hierarchy.",
                "Use the selected absolute path as create_sandbox.workspace_root."
              ],
              schema: schema({ path: field("string", "Absolute picker-visible workspace directory to browse. Omit to list roots.") }),
              request: { path: "/host/workspaces" },
              output: {
                path: "/host/workspaces",
                parent: "/host",
                truncated: false,
                directories: [
                  { name: "example", path: "/host/workspaces/example" },
                  { name: "service", path: "/host/workspaces/service" }
                ]
              },
              outputNote: "path and parent may be null at a configured root. truncated becomes true after the browse limit."
            }
          ]
        },
        {
          id: "lifecycle",
          label: "Sandbox lifecycle",
          description: "Create, enumerate, inspect, and remove manager-owned sandbox records.",
          tools: [
            {
              name: "create_sandbox",
              summary: "Create and start one or more sandboxes",
              risk: "danger",
              description: "Create a host-side sandbox record, create the runtime sandbox, and start its daemon.",
              manual: [
                "Choose image with list_docker_images and workspace_root with list_workspace_directories.",
                "The manager builds or reuses a shared read-only workspace base, creates each runtime sandbox, installs daemon assets, waits for readiness, and records endpoints.",
                "count defaults to 1. A failed multi-create batch is rolled back; successful creation changes host and container state."
              ],
              schema: schema({
                image: field("string", "Container image used to create the sandbox."),
                workspace_root: field("string", "Absolute host workspace directory bind-mounted into this sandbox."),
                count: field("integer", "Number of sandboxes to create (minimum 1). Values greater than 1 use a shared read-only workspace base.", { minimum: 0, default: 1 })
              }, ["image", "workspace_root"]),
              request: { image: "ubuntu:24.04", workspace_root: "/host/workspaces/example", count: 1 },
              output: sandboxRecord,
              outputNote: "For count = 1 the structured output is one record. For count > 1 it is { sandboxes: [record, …] }.",
              gaps: ["Schema gap: count advertises minimum 0, but the implementation rejects 0 and requires at least 1."]
            },
            {
              name: "list_sandboxes",
              summary: "List manager-known sandboxes",
              risk: "safe",
              description: "List sandbox records known to the manager, including lifecycle state and configured daemon endpoint metadata.",
              manual: [
                "Use this as the primary read-only way to obtain sandbox_id values and current lifecycle state.",
                "A record can exist without usable daemon metadata while it is creating, stopping, stopped, or failed.",
                "Do not infer daemon reachability from a stored endpoint alone; pair with Observability snapshot when health matters."
              ],
              schema: schema(),
              request: {},
              output: { sandboxes: [sandboxRecord] },
              outputNote: "The array is empty when the manager has no records. A verified safe call returned three ready records."
            },
            {
              name: "inspect_sandbox",
              summary: "Inspect one sandbox record",
              risk: "safe",
              description: "Inspect one sandbox record, including lifecycle state, workspace root, and configured daemon endpoint metadata.",
              manual: [
                "Call with an id from list_sandboxes when a single record and its endpoint metadata are needed.",
                "This reads the manager registry; it does not call the sandbox daemon or prove runtime health.",
                "Treat workspace paths and endpoint fields as operational metadata and avoid displaying them in untrusted logs."
              ],
              schema: schema({ sandbox_id: managerSandboxId() }, ["sandbox_id"]),
              request: { sandbox_id: "sbox-example" },
              output: sandboxRecord,
              outputNote: "Returns one record with nullable daemon, daemon_http, and shared_base fields."
            },
            {
              name: "destroy_sandbox",
              summary: "Stop and remove a sandbox",
              risk: "danger",
              description: "Stop the sandbox daemon, destroy the runtime sandbox, and remove the host-side sandbox record.",
              manual: [
                "Confirm the target with inspect_sandbox before calling; this operation is destructive.",
                "The manager transitions the record to stopping, stops its daemon, destroys the runtime sandbox, marks it stopped, and removes the registry record.",
                "If runtime destruction fails, the record is retained in failed state for operator recovery."
              ],
              schema: schema({ sandbox_id: managerSandboxId() }, ["sandbox_id"]),
              request: { sandbox_id: "sbox-example" },
              output: { ...sandboxRecord, state: "stopped" },
              outputNote: "Success returns the removed record in its final stopped state."
            }
          ]
        },
        {
          id: "delivery",
          label: "Layer delivery",
          description: "Compact published layers or materialize their combined delta on the host.",
          tools: [
            {
              name: "squash_layerstacks",
              summary: "Compact squashable published layers",
              risk: "danger",
              description: "Squash every squashable block of the selected sandbox's published layers into equivalent flattened layers and migrate live workspace sessions onto the compact chains. Forwards one squash_layerstack request to the sandbox daemon.",
              manual: [
                "Use only for operator-directed storage compaction; it changes the active layer manifest.",
                "The daemon plans and commits equivalent flattened layers, then the manager reports migration or lease dispositions for live workspace sessions.",
                "A stale daemon that lacks squash support returns operation_failed and must be recreated with the current daemon binary."
              ],
              schema: schema({ sandbox_id: managerSandboxId() }, ["sandbox_id"]),
              request: { sandbox_id: "sbox-example" },
              output: {
                manifest_version: 5,
                squashed_blocks: [{
                  squashed_layer_id: "layer-flat-5",
                  replaced_layer_ids: ["layer-2", "layer-3"],
                  replaced_layers: "reclaimed"
                }],
                swept_sessions: [{ session_id: "workspace_17", disposition: "migrated" }]
              },
              outputNote: "replaced_layers can be reclaimed or leased. Optional blocked_reasons and faulty_sessions explain incomplete reclamation."
            },
            {
              name: "export_changes",
              summary: "Apply or archive the published delta",
              risk: "danger",
              description: "Fold every published layer above the base (newest-wins, whiteout/opaque aware) into a compressed delta stream, fetch it from the sandbox daemon, and apply it onto --dest or write it as an archive. Forwards export_layerstack and read_export_chunk requests to the sandbox daemon.",
              manual: [
                "Choose dir to apply the delta into a host directory, or tar/tar-zst to atomically write an archive file.",
                "dest must be an absolute host path. The filesystem root, home directory, manager state paths, and .export spool directories are denied.",
                "The manager treats daemon bytes as untrusted, validates the paged stream, and is the only component that writes the host destination."
              ],
              schema: schema({
                sandbox_id: managerSandboxId(),
                dest: field("string", "Absolute host destination: directory for dir format, archive file for tar formats."),
                format: field("string", "Output format: dir, tar, or tar-zst.", { default: "dir" })
              }, ["sandbox_id", "dest"]),
              request: { sandbox_id: "sbox-example", dest: "/host/exports/example.tar.zst", format: "tar-zst" },
              output: {
                manifest_version: 7,
                format: "tar-zst",
                layers_exported: ["layer-6", "layer-7"],
                files_written: 12,
                symlinks_written: 1,
                whiteouts_emitted: 2,
                bytes_written: 48211
              },
              outputNote: "dir output uses deletes_applied, opaque_clears, and skipped_unchanged; archive output uses whiteouts_emitted. live_workspace_sessions is optional.",
              gaps: [
                "Catalog wording gap: --dest is CLI notation. MCP clients send the JSON field dest.",
                "Schema gap: format is a plain string instead of an enum constrained to dir, tar, or tar-zst."
              ]
            }
          ]
        }
      ]
    },

    runtime: {
      label: "Runtime",
      eyebrow: "Inside a sandbox",
      server: "ephemeral-os-runtime",
      command: "sandbox-mcp --set runtime",
      accent: "runtime",
      summary: "Shell command sessions and file operations projected through a sandbox daemon.",
      guidance: [
        "Every tool requires sandbox_id. Use Management list_sandboxes to discover an existing ready target.",
        "Commands without workspace_session_id create an automatic publish_then_destroy session and may publish filesystem changes.",
        "File operations without workspace_session_id target the latest published snapshot; write and edit publish a new layer."
      ],
      families: [
        {
          id: "commands",
          label: "Command sessions",
          description: "Start a shell command, stream its input, and page its stable transcript.",
          tools: [
            {
              name: "exec_command",
              summary: "Start a sandbox shell command",
              risk: "stateful",
              description: "Start a shell command in a workspace session. With workspace_session_id, run inside that existing session. Without it, exec_command creates an automatic session with finalize policy publish_then_destroy: after its last command reaches terminal state, the runtime captures and publishes the session's changes to the layerstack, then destroys the session. Explicitly managed sessions remain alive until internal teardown and discard unpublished changes when torn down. File operations and remounts run under the session's admission gate and neither extend nor trigger the session lifecycle. If the command is still running after the initial wait, the response includes a command_session_id usable with read_command_lines or write_command_stdin; a still-running command stays terminable through write_command_stdin (Ctrl-C or Ctrl-D).",
              manual: [
                "Use workspace_session_id only when an existing managed session is available; otherwise an automatic publish_then_destroy session is created.",
                "If status is running, retain command_session_id and continue with read_command_lines or write_command_stdin.",
                "A terminal automatic command captures and publishes filesystem changes. A read-looking shell command is safe only if the command itself is read-only."
              ],
              schema: schema({
                sandbox_id: sandboxId(),
                workspace_session_id: field("string", "Existing workspace session id to run inside. Omit to create a session with finalize policy publish_then_destroy."),
                cmd: field("string", "Shell command text."),
                timeout_ms: field("integer", "Command timeout in milliseconds.", { minimum: 0 }),
                yield_time_ms: field("integer", "Initial output wait in milliseconds.", { minimum: 0 })
              }, ["sandbox_id", "cmd"]),
              request: { sandbox_id: "sbox-example", cmd: "cargo check", yield_time_ms: 1000 },
              output: commandOutput,
              outputNote: "status is running, ok, error, timed_out, or cancelled. command_session_id appears when the command remains addressable; terminal responses can report publish rejection fields."
            },
            {
              name: "write_command_stdin",
              summary: "Write to a running command",
              risk: "stateful",
              description: "Append text to the stdin stream of a running command session and return a bounded output yield.",
              manual: [
                "Use command_session_id returned by exec_command while its command remains running.",
                "stdin is written exactly as supplied. Include a newline for line-oriented programs; send control characters such as \\u0003 only with deliberate intent.",
                "The response uses the same command-output shape as exec_command and may become terminal after the write."
              ],
              schema: schema({
                sandbox_id: sandboxId(),
                command_session_id: field("string", "Command session id returned by exec_command."),
                stdin: field("string", "Text to write to stdin."),
                yield_time_ms: field("integer", "Output wait after writing stdin.", { minimum: 0 })
              }, ["sandbox_id", "command_session_id", "stdin"]),
              request: { sandbox_id: "sbox-example", command_session_id: "namespace_execution_42", stdin: "yes\n", yield_time_ms: 1000 },
              output: { ...commandOutput, status: "ok", exit_code: 0, end_offset: 4, total_lines: 4, output: "accepted\ndone\n" },
              outputNote: "Uses the shared command output shape and returns only a bounded transcript window."
            },
            {
              name: "read_command_lines",
              summary: "Page a command transcript",
              risk: "safe",
              description: "Read rendered command output for a command session using stable line offsets.",
              manual: [
                "Start with start_offset 0, then continue from the returned end_offset until it reaches total_lines.",
                "The command may still be running; status and offsets are a point-in-time snapshot.",
                "This does not extend or trigger workspace-session lifecycle behavior."
              ],
              schema: schema({
                sandbox_id: sandboxId(),
                command_session_id: field("string", "Command session id returned by exec_command."),
                start_offset: field("integer", "First transcript line offset. Defaults to 0.", { minimum: 0, default: 0 }),
                limit: field("integer", "Maximum transcript rows to return. Defaults to 200; maximum 1000.", { minimum: 0, default: 200 })
              }, ["sandbox_id", "command_session_id"]),
              request: { sandbox_id: "sbox-example", command_session_id: "namespace_execution_42", start_offset: 2, limit: 200 },
              output: { ...commandOutput, status: "ok", exit_code: 0, start_offset: 2, end_offset: 4, total_lines: 4, output: "accepted\ndone\n" },
              outputNote: "original_token_count describes the untruncated source output before rendering bounds.",
              gaps: ["Schema gap: limit says maximum 1000 but does not publish maximum: 1000; minimum 0 may also admit a value the runtime does not use as a meaningful page size."]
            }
          ]
        },
        {
          id: "files",
          label: "Files and attribution",
          description: "Read snapshots, publish exact file mutations, and inspect line ownership.",
          tools: [
            {
              name: "file_read",
              summary: "Read a UTF-8 text window",
              risk: "safe",
              description: "Read a UTF-8 text window from a repository-relative or workspace-root-absolute path. With workspace_session_id the read runs inside that live session's mounted workspace; without it the read projects the latest published snapshot.",
              manual: [
                "Omit workspace_session_id to read the latest published snapshot; include it to read uncommitted content in a live session.",
                "offset is a 1-indexed line number. Follow next_offset while truncated is true to page long files.",
                "Only UTF-8 regular files are supported. This operation is safe for inspecting an existing sandbox."
              ],
              schema: schema({
                sandbox_id: sandboxId(),
                path: field("string", "Repository-relative or workspace-root-absolute path to read."),
                offset: field("integer", "1-indexed line number to start reading from. Defaults to 1.", { minimum: 0, default: 1 }),
                limit: field("integer", "Maximum number of lines to read. Defaults to 2000; must be 1..=2000.", { minimum: 0, default: 2000 }),
                workspace_session_id: field("string", "Existing workspace session id to read inside. Omit to read the snapshot.")
              }, ["sandbox_id", "path"]),
              request: { sandbox_id: "sbox-example", path: "README.md", offset: 1, limit: 40 },
              output: {
                path: "README.md",
                content: "# Example\n\nProject overview…\n",
                start_line: 1,
                num_lines: 3,
                total_lines: 3,
                bytes_read: 31,
                total_bytes: 31,
                next_offset: null,
                truncated: false
              },
              outputNote: "A verified safe call succeeded against an existing sandbox; its real content and identifiers are intentionally omitted here.",
              gaps: ["Schema gap: offset is documented as 1-indexed and limit as 1..=2000, but both schemas publish minimum 0 and omit the useful upper bound for limit."]
            },
            {
              name: "file_write",
              summary: "Create or overwrite a file",
              risk: "danger",
              description: "Write content to a repository-relative or workspace-root-absolute path. With workspace_session_id the write lands in that live session's mounted workspace and is attributed on capture; without it the write publishes one layer attributed to operation:<request_id>.",
              manual: [
                "Use only when overwriting the entire target file is intended.",
                "With workspace_session_id, the write stays in the live session until its lifecycle resolves. Without it, the runtime publishes a durable layer immediately.",
                "The owner recorded for a direct publish is operation:<request_id>."
              ],
              schema: schema({
                sandbox_id: sandboxId(),
                path: field("string", "Repository-relative or workspace-root-absolute path to write."),
                content: field("string", "File content to write."),
                workspace_session_id: field("string", "Existing workspace session id to write inside. Omit to publish a layer.")
              }, ["sandbox_id", "path", "content"]),
              request: { sandbox_id: "sbox-example", path: "notes.txt", content: "new content\n" },
              output: { type: "update", path: "notes.txt", bytes_written: 12 },
              outputNote: "type is create for a new path or update for an existing regular file."
            },
            {
              name: "file_edit",
              summary: "Apply ordered exact replacements",
              risk: "danger",
              description: "Apply an ordered list of exact-string replacements to a repository-relative or workspace-root-absolute path. Each old_string must be found and unique unless replace_all is set. With workspace_session_id the edit runs inside that live session; without it the edit publishes one layer attributed to operation:<request_id>.",
              manual: [
                "Each edit object requires old_string and new_string; replace_all defaults to false. Edits run in array order.",
                "Without replace_all, old_string must occur exactly once. Missing, ambiguous, empty, or no-op edit sets are rejected.",
                "Like file_write, omitting workspace_session_id publishes a durable layer immediately."
              ],
              schema: schema({
                sandbox_id: sandboxId(),
                path: field("string", "Repository-relative or workspace-root-absolute path to edit."),
                edits: field("array", "JSON array of { old_string, new_string, replace_all? } edits, applied in order."),
                workspace_session_id: field("string", "Existing workspace session id to edit inside. Omit to publish a layer.")
              }, ["sandbox_id", "path", "edits"]),
              request: {
                sandbox_id: "sbox-example",
                path: "notes.txt",
                edits: [{ old_string: "draft", new_string: "ready", replace_all: true }]
              },
              output: { type: "edit", path: "notes.txt", edits_applied: 1, replacements: 2, bytes_written: 26 },
              outputNote: "edits_applied counts edit objects; replacements counts individual occurrences changed.",
              gaps: ["Schema gap: edits is only typed as array and publishes no items object schema, so clients cannot discover old_string, new_string, and replace_all structurally."]
            },
            {
              name: "file_blame",
              summary: "Inspect per-line published ownership",
              risk: "safe",
              description: "Return each line's owner for a published path, tiling the whole file from the latest auditability event. The owner is an opaque string (workspace_session:<id> | operation:<id> | original | unknown).",
              manual: [
                "Use for a published repository-relative path after command, write, or edit operations have created auditability events.",
                "Ranges are 1-indexed and tile the latest known file content. Treat owner strings as opaque identifiers.",
                "A missing auditability record returns a not_found error even if unrelated filesystem content exists."
              ],
              schema: schema({ sandbox_id: sandboxId(), path: field("string", "Repository-relative path to blame.") }, ["sandbox_id", "path"]),
              request: { sandbox_id: "sbox-example", path: "notes.txt" },
              output: {
                path: "notes.txt",
                ranges: [
                  { start_line: 1, line_count: 4, owner: "original" },
                  { start_line: 5, line_count: 2, owner: "operation:request-id" }
                ]
              },
              outputNote: "owner can be workspace_session:<id>, operation:<id>, original, or unknown."
            }
          ]
        }
      ]
    },

    observability: {
      label: "Observability",
      eyebrow: "Read-only evidence",
      server: "ephemeral-os-observability",
      command: "sandbox-mcp --set observability",
      accent: "observability",
      summary: "Fleet health, trace history, domain events, resource series, and active layer inventory.",
      guidance: [
        "Every operation is read-only. snapshot can aggregate all ready manager-known sandboxes; the other tools require sandbox_id.",
        "snapshot and layerstack are live views. trace, events, and workspace-scoped cgroup folds read the telemetry log.",
        "Sandbox-scoped cgroup data comes from the host Docker Engine and is kept in manager memory for the lookback window."
      ],
      families: [
        {
          id: "health",
          label: "Fleet health",
          description: "A live, normalized view of sandbox availability and active runtime state.",
          tools: [
            {
              name: "snapshot",
              summary: "Inspect live sandbox health",
              risk: "safe",
              description: "Show current state from the runtime registry for one sandbox, or aggregate ready manager-known sandboxes when --sandbox-id is omitted: sandbox lifecycle state, workspaces (with layer counts), in-flight executions, and the latest resource sample per scope. Served live; does not read the log.",
              manual: [
                "Omit sandbox_id for fleet aggregation, or supply one id to select that manager record.",
                "Each node normalizes availability to available, partial, or unavailable and contains an errors array for partial failures.",
                "Use this first for live health. Follow with trace/events for history or cgroup/layerstack for detail."
              ],
              schema: schema({ sandbox_id: field("string", "Optional target sandbox id. When omitted, the manager queries all ready sandboxes.") }),
              request: {},
              output: {
                sandboxes: [{
                  sandbox_id: "sbox-example",
                  lifecycle_state: "ready",
                  availability: "available",
                  sampled_at_unix_ms: 1784016000000,
                  errors: [],
                  daemon: { daemon_pid: 321, runtime_dir: "/run/ephemeral-os" },
                  resources: { latest: null, history: [] },
                  workspaces: [],
                  stack: { layer_count: 2, layers_bytes: 4096, active_leases: 0 }
                }]
              },
              outputNote: "A verified safe call returned three available sandbox nodes with no sandbox-level errors.",
              gaps: ["Catalog wording gap: --sandbox-id is CLI notation. MCP clients send sandbox_id or omit the field."]
            }
          ]
        },
        {
          id: "telemetry",
          label: "Traces and events",
          description: "Fold the append-only telemetry log into one flow or a filtered fact stream.",
          tools: [
            {
              name: "trace",
              summary: "Render a span waterfall",
              risk: "safe",
              description: "Fold the log into a span waterfall for one trace: spans nested by parent, offset by start, with attached events inline. Use --trace-id last for the most recent root trace.",
              manual: [
                "Use trace_id last (the default) for the most recently started root trace, or supply an exact trace/request id.",
                "spans is a forest. Each node carries the completed span, its offset from trace start, nested children, and attached events.",
                "An unknown trace is not an error; it returns an empty spans array."
              ],
              schema: schema({
                sandbox_id: sandboxId(),
                trace_id: field("string", "Trace id to render, or 'last' for the most recent root trace.", { default: "last" })
              }, ["sandbox_id"]),
              request: { sandbox_id: "sbox-example", trace_id: "last" },
              output: {
                view: "trace",
                trace: "request-uuid",
                spans: [{
                  span: { ts: 1784016000250, trace: "request-uuid", span: "d-0", name: "daemon.dispatch", dur_ms: 250, status: "completed", attrs: { op: "exec_command" } },
                  offset_ms: 0,
                  children: [],
                  events: []
                }]
              },
              outputNote: "Span status is completed, error, cancelled, or timed_out. attrs is operation-specific.",
              gaps: ["Catalog wording gap: --trace-id is CLI notation. MCP clients send trace_id; the MCP default is last."]
            },
            {
              name: "events",
              summary: "Filter cross-trace domain events",
              risk: "safe",
              description: "Fold the log into a flat, cross-trace stream of point-in-time events (lease, errors, …), newest first. Filter by exact name and/or a start timestamp, and cap to the newest N with --last-n.",
              manual: [
                "Filter name by an exact dotted event label such as lease.acquired; use since_ms for an inclusive Unix-millisecond lower bound.",
                "last_n keeps only the newest N matched events. Omit filters to return every retained event in the telemetry log.",
                "Events carry their trace and parent span identifiers so they can be followed into trace."
              ],
              schema: schema({
                sandbox_id: sandboxId(),
                name: field("string", "Filter to events with this exact name (e.g. lease.acquired)."),
                since_ms: field("integer", "Only events at or after this unix-ms timestamp.", { minimum: 0 }),
                last_n: field("integer", "Keep only the N newest matched events.", { minimum: 0 })
              }, ["sandbox_id"]),
              request: { sandbox_id: "sbox-example", name: "lease.acquired", last_n: 20 },
              output: {
                view: "events",
                events: [{ ts: 1784016000120, trace: "request-uuid", parent: "d-1", name: "lease.acquired", attrs: { layer_id: "layer-7" } }]
              },
              outputNote: "attrs is an open domain-fact object and can vary by event name.",
              gaps: ["Catalog wording gap: --last-n is CLI notation. MCP clients send last_n."]
            }
          ]
        },
        {
          id: "resources",
          label: "Resources and layers",
          description: "Inspect time-windowed resource samples and the active layer manifest.",
          tools: [
            {
              name: "cgroup",
              summary: "Read a resource time series",
              risk: "safe",
              description: "Return a read-only resource time series. Sandbox scope reads CPU, memory, and block-I/O counters from the host Docker Engine; workspace scopes retain daemon disk samples.",
              manual: [
                "Use the default sandbox scope for host Docker CPU, memory, and block-I/O counters. Use a workspace id as scope for daemon-recorded workspace samples.",
                "window_ms defaults to 60 seconds and cannot exceed 600000. Deltas appear only when a prior in-window counter sample exists.",
                "The response identifies sandbox metrics with metrics_source: docker_engine."
              ],
              schema: schema({
                sandbox_id: sandboxId(),
                scope: field("string", "Resource scope: 'sandbox' or a workspace id.", { default: "sandbox" }),
                window_ms: field("integer", "Lookback window in milliseconds (max 600000).", { minimum: 0, default: 60000 })
              }, ["sandbox_id"]),
              request: { sandbox_id: "sbox-example", scope: "sandbox", window_ms: 60000 },
              output: {
                view: "cgroup",
                scope: "sandbox",
                series: [{
                  ts: 1784016000000,
                  sample_delta_ms: null,
                  metrics: { metrics_source: "docker_engine", cpu_usec: 912345, mem_cur: 67108864, mem_max: 1073741824, io_rbytes: 4096, io_wbytes: 8192 },
                  deltas: {}
                }]
              },
              outputNote: "The live catalog description reflects the Docker-backed sandbox path; the Phase-0 fixture still carries the retired /sys/fs/cgroup wording.",
              gaps: ["Schema gap: window_ms documents a maximum of 600000 but the JSON Schema does not publish maximum: 600000."]
            },
            {
              name: "layerstack",
              summary: "Inspect the active layer manifest",
              risk: "safe",
              description: "Show the active manifest as a per-layer inventory: disk bytes, how many workspaces lease each layer, and which leased layers book each base. Served live from the runtime; does not read the log.",
              manual: [
                "Omit workspace_id for the full active manifest and an optional stack trend. Include workspace_id for that session's mounted lower layers and private upperdir bytes.",
                "Layers are listed in manifest order. booked_by identifies leased layers above a base; leased_by_workspaces is the direct lease count.",
                "window_ms controls only the optional telemetry trend and cannot exceed 600000."
              ],
              schema: schema({
                sandbox_id: sandboxId(),
                workspace_id: field("string", "Show one workspace's lower layers and private upperdir."),
                window_ms: field("integer", "Lookback window in milliseconds for the stack trend (max 600000).", { minimum: 0, default: 60000 })
              }, ["sandbox_id"]),
              request: { sandbox_id: "sbox-example", window_ms: 60000 },
              output: {
                view: "layerstack",
                manifest_version: 7,
                root_hash: "sha256:…",
                active_lease_count: 1,
                total_bytes: 16384,
                total_allocated_bytes: 20480,
                storage_logical_bytes: 24576,
                storage_allocated_bytes: 28672,
                staging_entry_count: 0,
                layers: [{ layer_id: "layer-7", bytes: 8192, allocated_bytes: 12288, leased_by_workspaces: 1, booked_by: [] }],
                trend: []
              },
              outputNote: "With workspace_id, output changes to { view, workspace, mounts, upper_bytes }.",
              gaps: ["Schema gap: window_ms documents a maximum of 600000 but the JSON Schema does not publish maximum: 600000."]
            }
          ]
        }
      ]
    }
  };
})();
