# Runtime API — commands, files, and Workspace sessions

Date: **2026-08-04**  
Status: **DESIGN DRAFT — proposed Phase 04 public surface**

The runtime family lets callers execute commands, read selected immutable
Versions, and work inside isolated mutable Workspace sessions. Runtime effects
remain outside portable Version identity; publication is the only path from a
mutable Workspace Candidate to a newly selected accepted Version.

This file is subordinate to the shared [API contract](README.md), the product
[hard rules](../PRD.md#hard-rules-must-never-break), and the selected
[architecture](../architecture_design.md).

## 1. Family boundary

```text
public runtime request
        |
        v
sandbox-runtime application / operation services
  - auth and request/revoke ordering
  - target selection
  - command and file orchestration
  - internally captured expected Head
        |
        +-----------------------> Workspace / mount / namespace / exec owners
        |                           mutable live effects
        |
        `-----------------------> LayerStack-0
                                    immutable accepted Versions
                                    admission + one OCC Head transition

Workspace effect -X-> portable Version identity
file_write/edit  -X-> accepted payload mutation
public caller    -X-> HeadRevision or AcceptedBinding
LayerStack-0     -X-> command policy, auth, or rollout policy
```

## 2. Operation index

| Operation | Evidence label | V2 disposition / decision state | Required operation arguments | Optional arguments | Target/effect |
|---|---|---|---|---|---|
| `exec_command` | `SOURCE-VERIFIED` | retain; rewrite publish semantics | `cmd` | `workspace_session_id`, `timeout_ms`, `yield_time_ms` | Existing or automatic mutable Workspace; command execution |
| `write_command_stdin` | `SOURCE-VERIFIED` | retain | `command_session_id`, `stdin` | `yield_time_ms` | Running command stream |
| `read_command_lines` | `SOURCE-VERIFIED` | retain | `command_session_id` | `start_offset=0`, `limit=200` | Bounded command transcript |
| `file_read` | `SOURCE-VERIFIED` | retain; rewrite Version terminology | `path` | `offset=1`, `limit=2000`, `workspace_session_id` | Selected Version or live Workspace |
| `file_list` | `SOURCE-VERIFIED` for HTTP-only surface | `OWNER_DEC_OPEN` (`DEC-017`) for promotion | — | `path`, `limit=2000`, `workspace_session_id` | Selected Version or live Workspace |
| `file_write` | `SOURCE-VERIFIED` | `OWNER_DEC_OPEN` (`DEC-017`) for no-session form | `path`, `content` | `workspace_session_id` pending `DEC-017` | Live Workspace only in V2 core; optional composed publish remains owner choice |
| `file_edit` | `SOURCE-VERIFIED` | `OWNER_DEC_OPEN` (`DEC-017`) for no-session form | `path`, `edits` | `workspace_session_id` pending `DEC-017` | Live Workspace only in V2 core; optional composed publish remains owner choice |
| `file_blame` | `SOURCE-VERIFIED` | `OWNER_DEC_OPEN` (`DEC-001`) | `path` | — | Application auditability side channel, never Version truth |
| `create_workspace_session` | `SOURCE-VERIFIED` | retain | — | `network_profile=shared` | Create isolated mutable Workspace |
| `publish_workspace_session` | `SOURCE-VERIFIED` | rewrite semantics | `workspace_session_id` | `grace_s` | Candidate admission plus one internal-OCC Head transition |
| `destroy_workspace_session` | `SOURCE-VERIFIED` | retain | `workspace_session_id` | `grace_s` | Discard unpublished live effects |

Source metadata for `SOURCE-VERIFIED` is the clean sealed e497 product tree
recorded by the shared API contract. These labels are not correctness results;
no V2 runtime implementation check or performance qualification was run.

The recommended projection has 11 runtime names if the owner keeps
`file_blame` and promotes `file_list`. `DEC-001` and `DEC-017` control the final
count and mutation schema.

## 3. Runtime routing and CLI projection

The runtime CLI keeps `sandbox_id` as a required global route:

```text
sandbox-runtime-cli --sandbox-id SANDBOX <operation> [arguments]
```

MCP injects the same required `sandbox_id` into each runtime operation schema.
The field is not repeated in the operation tables below.

Examples:

```text
sandbox-runtime-cli --sandbox-id S1 file_read --path src/lib.rs

sandbox-runtime-cli --sandbox-id S1 exec_command \
  --workspace-session-id W1 \
  'cargo test -p sandbox-runtime-layerstack'
```

Catalog/MCP fields use snake case; CLI flags use kebab case. `cmd` and `stdin`
remain CLI positional strings. `file_edit.edits` is a native JSON array in MCP
and JSON text supplied to `--edits` in CLI.

## 4. Target semantics

### 4.1 File target matrix

| Operation | No `workspace_session_id` | With `workspace_session_id` |
|---|---|---|
| `file_read` | Capture the sandbox's selected accepted Version once, acquire read custody, and read that immutable Version | Read that live Workspace generation through runtime-effect custody |
| `file_list` | Same captured selected-Version rule; promotion remains `DEC-017` | List one directory level in that live Workspace |
| `file_write` | `DEC-017`: reject in V2 core, or application-composed temporary Workspace + publish; never edit accepted bytes | Write only into the live Workspace's private writable effects |
| `file_edit` | Same `DEC-017` seam | Read/validate/edit only the live Workspace's private writable effects |

For committed reads, a concurrent Head move does not splice old and new
Versions into one result:

```text
resolve Head -> acquire custody of accepted Version V12 -> read/list V12
                         |
                         +---- concurrent publish may move Head to V13

current request remains entirely on immutable V12, then releases custody.
```

For live-session operations, `workspace_session_id` is a routing/effect fact.
It never enters canonical bytes or `VersionId`.

### 4.2 Path rules

The e497 public file operations accept a repository-relative path or an
absolute path under the configured Workspace root. V2 must normalize either
accepted public spelling to one bounded relative Workspace path before it
reaches identity or storage.

Required behavior:

- reject path traversal, NUL, ambiguous separators/encodings, invalid root
  escape, and paths over finite length/depth bounds;
- never interpret a public path relative to the LayerStack-0 storage root;
- never follow a candidate symlink while resolving a store write target;
- keep host absolute Workspace paths out of portable Version facts; and
- treat the exact accepted absolute-path compatibility form as part of the
  `DEC-017` “file target set” decision.

Checkpoint and `VersionId` selectors are absent from file operations. A caller
that needs to explore a Checkpoint forks/activates an authorized Branch through
the manager workflow instead of reading raw storage.

## 5. Command operations

### 5.1 `exec_command`

```text
sandbox-runtime-cli --sandbox-id SANDBOX exec_command \
  [--workspace-session-id WORKSPACE_SESSION] \
  [--timeout-ms MS] \
  [--yield-time-ms MS] \
  COMMAND
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `workspace_session_id` | no | opaque string | Existing explicit Workspace session. Omit to create an automatic session with publish-then-destroy finalization. |
| `cmd` | yes | string, CLI positional | Shell command text within configured request and audit bounds |
| `timeout_ms` | no | non-negative bounded integer | Maximum command execution time; server configuration supplies default/cap |
| `yield_time_ms` | no | non-negative bounded integer | Initial output wait before returning a running command handle |

With an explicit Workspace session, the command mutates only that Workspace
and does not publish or destroy it. With no session, the application creates an
automatic isolated Workspace and owns this composition:

```text
capture selected accepted base + internal Head revision
        |
activate private automatic Workspace
        |
run command(s)
        |
last command reaches terminal state
        |
freeze/capture complete Candidate
        |
validate + admit complete immutable Version
        |
one conditional Head transition
        +---- success -> close/destroy automatic Workspace
        `---- stale/failure -> no merge/rebase; bounded retained/recovery outcome
```

This replaces e497's compatible-directory/text auto-merge behavior. A stale
automatic publish must be visible in the terminal result, for example
`publish_rejected=true` with error class `conflict`; it may not recapture the
new Head and silently retry.

Initial result includes bounded output, command status, exit information when
terminal, and `command_session_id` when the command is still running. Terminal
automatic-session results additionally include publication outcome and the
accepted `VersionId` on success when disclosure is allowed. They never expose
the internal expected/current Head revision.

`timeout_ms` controls the command, while `yield_time_ms` controls the initial
response wait. A response timeout is not permission to run an unbounded worker
or repeat a publication blindly.

### 5.2 `write_command_stdin`

```text
sandbox-runtime-cli --sandbox-id SANDBOX write_command_stdin \
  --command-session-id COMMAND_SESSION \
  [--yield-time-ms MS] \
  TEXT
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `command_session_id` | yes | opaque string | Running command returned by `exec_command` |
| `stdin` | yes | string, CLI positional | Bounded bytes/text appended to command stdin; control characters may request interrupt/EOF according to existing semantics |
| `yield_time_ms` | no | non-negative bounded integer | Output wait after the write |

This operation interacts with command/runtime effects. It does not itself
publish a Version, replace a Head, create a Checkpoint, or extend the enclosing
Workspace lifetime beyond its defined command/session policy.

The result includes accepted stdin byte count, bounded new output, command
status, and transcript offsets. `not_found` or terminal-command errors must not
be converted into a new command.

### 5.3 `read_command_lines`

```text
sandbox-runtime-cli --sandbox-id SANDBOX read_command_lines \
  --command-session-id COMMAND_SESSION \
  [--start-offset N] \
  [--limit N]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `command_session_id` | yes | opaque string | Command transcript to read |
| `start_offset` | no | integer, default `0`, minimum `0` | First stable transcript line offset |
| `limit` | no | integer, default `200`, maximum `1000` | Maximum transcript rows |

Returns ordered bounded lines, next offset, terminal/running status, and
`truncated`/retention information. Command output retention is bounded; a
caller cannot request an unbounded history scan.

## 6. File operations

### 6.1 `file_read`

```text
sandbox-runtime-cli --sandbox-id SANDBOX file_read \
  --path PATH \
  [--offset LINE] \
  [--limit LINES] \
  [--workspace-session-id WORKSPACE_SESSION]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `path` | yes | path string | Repository-relative or accepted Workspace-root-absolute file path |
| `offset` | no | integer, default `1`, minimum `1` | 1-indexed starting line |
| `limit` | no | integer, default `2000`, range `1..=2000` | Maximum returned lines |
| `workspace_session_id` | no | opaque string | Omit for captured selected Version; supply for live Workspace |

The operation reads UTF-8 text only under the current contract. It returns
normalized public path, requested/effective window, lines/content, total or
continuation information allowed by the bounded implementation, and target
kind (`accepted_version` or `workspace`). A committed read may return
`VersionId` for correlation; a live read may return Workspace generation
diagnostics but never makes that generation portable identity.

Missing paths, directories/non-regular files, invalid UTF-8, and over-limit
content produce typed errors. An Accepted Version is opened only through
read-only custody.

### 6.2 `file_list`

`file_list` exists at e497 as a daemon HTTP-only operation. The proposed V2
surface promotes it to the catalog, CLI, and MCP if the owner selects that
outcome under `DEC-017`.

```text
sandbox-runtime-cli --sandbox-id SANDBOX file_list \
  [--path PATH] \
  [--limit N] \
  [--workspace-session-id WORKSPACE_SESSION]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `path` | no | path string, default Workspace root | Directory whose immediate children are listed |
| `limit` | no | integer, proposed/current configured default `2000`, maximum `2000` | Maximum immediate entries |
| `workspace_session_id` | no | opaque string | Omit for captured selected Version; supply for live Workspace |

Result:

```text
path          normalized public directory path
target        accepted_version | workspace
VersionId     optional committed correlation only
entries[]     bounded { name, kind, size? }
truncated     whether more immediate entries existed
```

Entries are one directory level, not a recursive tree walk. Names are bounded
and returned in a stable documented order. Promotion must add one catalog
definition and parity tests; it must not leave HTTP with different defaults or
target semantics.

### 6.3 `file_write`

```text
sandbox-runtime-cli --sandbox-id SANDBOX file_write \
  --path PATH \
  --content CONTENT \
  [--workspace-session-id WORKSPACE_SESSION]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `path` | yes | path string | Validated Workspace file path |
| `content` | yes | bounded string | Complete replacement content |
| `workspace_session_id` | owner decision | opaque string | With ID: live Workspace target. Omission behavior is `DEC-017`. |

Selected V2 invariant: this operation never receives a writable handle to an
Accepted Version and never changes accepted payload bytes in place.

Allowed `DEC-017` outcomes:

| Owner outcome | No-session behavior | Architecture effect |
|---|---|---|
| Require session | Reject with `invalid_argument` and tell the caller to create a Workspace session | Simplest V2 core; no API composition |
| Keep convenience | Application creates a bounded temporary Workspace from a captured selected Version, applies the write, captures/admit Candidate, then performs one internal-OCC publish | Same selected architecture; must surface stale and cleanup exactly like session publication |
| Break/remove no-session form | Make `workspace_session_id` required in the versioned catalog | Public compatibility break only |

No allowed outcome can call a direct “amend accepted file” store method,
publish a legacy layer, silently merge on stale, or accept a raw Version
selector.

With a live Workspace, result includes normalized path, bytes written, write
kind (created/replaced where useful), Workspace ID, and no durable publication
claim. A later `publish_workspace_session` produces the accepted Version.

### 6.4 `file_edit`

```text
sandbox-runtime-cli --sandbox-id SANDBOX file_edit \
  --path PATH \
  --edits JSON_ARRAY \
  [--workspace-session-id WORKSPACE_SESSION]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `path` | yes | path string | Validated Workspace text-file path |
| `edits` | yes | non-empty bounded JSON array | Ordered `{old_string, new_string, replace_all?}` edits |
| `workspace_session_id` | owner decision | opaque string | With ID: live Workspace target. Omission behavior is `DEC-017`. |

Edits apply in array order. Each `old_string` must be found and unique unless
`replace_all=true`; empty edit arrays, invalid occurrences, non-UTF-8, over-size
results, and limit violations fail before the write effect.

The same no-session outcomes and prohibitions as `file_write` apply. With a
session, the edit is a live Workspace mutation only. The result includes
normalized path, per-edit replacement counts, total replacements, resulting
bounded byte count, and Workspace ID.

### 6.5 `file_blame`

```text
sandbox-runtime-cli --sandbox-id SANDBOX file_blame --path PATH
```

| Argument | Required | Type | Contract |
|---|---:|---|---|
| `path` | yes | path string | Published/selected file to query in the application auditability side channel |

`DEC-001` remains open: the owner may keep exact e497-style per-line blame or
accept a breaking removal. If retained, V2 must key provenance to bounded
publication/accepted-Version correlation while preserving these boundaries:

- provenance is not canonical Version identity or selected-Version truth;
- absence/corruption of provenance cannot change a Head, admit a Version, or
  block an otherwise valid immutable read unless product policy explicitly
  requires a separate audit failure;
- owners remain opaque bounded strings with redaction/cardinality controls;
- `file_blame` is read-only and cannot reconstruct truth from legacy layers;
- live Workspace content is outside committed blame until publication; and
- auth/disclosure follows `DEC-018`.

If removed, delete its catalog/CLI/MCP route and return an explicit versioned
compatibility error during the observation window. Do not leave a command that
returns guessed ownership.

## 7. Workspace-session operations

### 7.1 Workspace lifecycle

```text
selected accepted Version V20
          |
          | capture immutable base/read custody
          v
create_workspace_session -> Workspace W8
                              private writable effects
                                  |
                     exec / file_write / file_edit
                                  |
                    +-------------+-------------+
                    |                           |
          publish_workspace_session    destroy_workspace_session
                    |                           |
                    v                           v
        complete Candidate -> V21      discard unpublished effects
        one conditional Head move       no Version publication
```

### 7.2 `create_workspace_session`

```text
sandbox-runtime-cli --sandbox-id SANDBOX create_workspace_session \
  [--network-profile shared|isolated]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `network_profile` | no | enum `shared` or `isolated`, default `shared` | Runtime networking policy; never portable Version identity |

The application captures one selected accepted Version as the session base and
records the internal expected Head needed for a later publish. Runtime-effect
owners create the isolated mutable Workspace. The result includes
`workspace_session_id`, base `VersionId` correlation, network profile, and
ready/lifecycle state—never the internal base revision or binding.

Session count, scratch, FDs, processes, mounts, memory, and cleanup debt are
finite. Failure cleans or records bounded recoverable runtime effects without
changing the selected Head.

### 7.3 `publish_workspace_session`

```text
sandbox-runtime-cli --sandbox-id SANDBOX publish_workspace_session \
  --workspace-session-id WORKSPACE_SESSION \
  [--grace-s SECONDS]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `workspace_session_id` | yes | opaque string | Explicit Workspace to freeze, capture, publish, and close on success |
| `grace_s` | no | non-negative bounded float seconds | Optional close/drain grace period |

There is no public expected revision. The session already owns the internally
captured base Head record from creation; application ordering decides when the
publish attempt may proceed.

```text
Workspace W8
    |
    | close admission gate; drain/stop mutable activity within grace
    v
freeze one complete view
    |
    | validate portable facts; canonicalize; derive VersionId
    v
LayerStack-0 admission
    | absent -> durable complete immutable payload
    | occupied equal -> full-byte compare then reuse
    | occupied unequal -> collision, fail closed
    v
AcceptedBinding V21
    |
    | ReplaceHead(Head identity,
    |             Expected::Exact(session's complete base Head), V21)
    +---- match -> durable complete Head replacement -> success -> close W8
    `---- stale -> conflict, Head unchanged, no merge/rebase -> retain W8
```

Important outcomes:

| Outcome | Head | Workspace | Accepted payload |
|---|---|---|---|
| `APPLIED` | Head replaces once with the accepted Version binding | Closes after the reference durability fence | Complete and reachable by Head |
| No content change | Phase 03-selected same-Version strict outcome | Closes only after explicit successful outcome | Existing payload reused; reference path remains zero-payload where applicable |
| `CONFLICT` | Unchanged | Retained for explicit caller decision when safely possible | Newly admitted complete Version may remain bounded accepted-orphan debt |
| Collision/integrity failure | Unchanged | Retained or bounded recovery state | Mismatch never aliases or gains a Root/Head |
| Pre-linearization cancellation/I/O/limit | Unchanged | Retained when safe; private debris bounded/cleaned | No incomplete accepted payload |
| `OUTCOME_UNKNOWN` at durability edge | Authoritatively read the exact Head and request correlation before any retry | Do not destroy blindly | Prior or complete new truth only |

The public result includes publication status, selected/attempted `VersionId`
where disclosure is safe, session retention/closure status, typed conflict or
collision class, and bounded cleanup/recovery indication. It never includes a
revision for the caller to use later.

### 7.4 `destroy_workspace_session`

```text
sandbox-runtime-cli --sandbox-id SANDBOX destroy_workspace_session \
  --workspace-session-id WORKSPACE_SESSION \
  [--grace-s SECONDS]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `workspace_session_id` | yes | opaque string | Explicit Workspace session to close |
| `grace_s` | no | non-negative bounded float seconds | Optional command/effect drain grace period |

Destroy discards unpublished Workspace changes and never creates a Version or
applies any Head/fixed-Root lifecycle operation. It is rejected while active commands cannot be
safely drained under the chosen policy. Cleanup is bounded and reports retained
recovery artifacts honestly.

Safe read-back is session inspection through the existing operation/lifecycle
result or a typed `not_found`. Workspace session IDs are not reused in a way
that lets stale commands target a new session.

## 8. Publish then Checkpoint

The user-selected public contract intentionally separates content publication
from reference Checkpoint creation:

```text
# 1. Work privately
W=$(sandbox-runtime-cli --sandbox-id S1 create_workspace_session ...)
sandbox-runtime-cli --sandbox-id S1 file_write \
  --workspace-session-id "$W" --path result.txt --content 'done'

# 2. Admit and select the complete Version
sandbox-runtime-cli --sandbox-id S1 publish_workspace_session \
  --workspace-session-id "$W"

# 3. Create the fixed Root from the selected accepted Version
sandbox-manager-cli create_checkpoint --sandbox-id S1 --name review-ready
```

`create_checkpoint` is not duplicated in the runtime family and never accepts
a Workspace session. This avoids an overloaded “checkpoint” command whose cost
and failure behavior would silently switch between reference-only and
Candidate-admission paths.

## 9. Error and retry rules

| Operation | Important errors | Retry/read-back rule |
|---|---|---|
| `exec_command` | session missing, command limit/timeout, namespace/exec failure, auto-publish conflict | Read retained command/session outcome; never repeat auto-publication blindly |
| command interaction | command missing/terminal, stdin closed, transcript evicted/offset invalid | Re-read status; do not create a replacement command automatically |
| committed read/list | invalid path, not found/type mismatch, integrity/readiness, limit | Retry only after request/store readiness changes; captured read remains one Version |
| live read/write/edit | session missing/closing, path/edit/size limit, command admission conflict | Correct request or wait; no accepted Head changed |
| publish | stale `conflict`, collision, integrity, limit/ENOSPC, busy, outcome unknown | Preserve session when safe; inspect result/Head, then make an explicit new decision |
| destroy session | active command/busy, partial cleanup | Drain command or resolve bounded recovery; no publication occurs |

No adapter converts a stale conflict to success, starts a new Workspace after a
missing one, or falls back from a live-session target to the selected Version.

## 10. Open decisions

### `DEC-001` — `file_blame`

Blocks final presence/schema of one runtime operation. It does not move
provenance into LayerStack-0 truth.

### `DEC-017` — file surface

Blocks:

- whether `file_list` is promoted from HTTP-only to the catalog/CLI/MCP;
- whether `workspace_session_id` becomes required for `file_write` and
  `file_edit`;
- whether a no-session convenience form remains as an explicit
  application-composed temporary Workspace + strict publish; and
- the exact accepted public path target forms.

It cannot permit in-place Accepted-Version mutation, legacy layer publication,
or silent merge/rebase.

### `DEC-018` — auth/revoke races

Controls when a request becomes authorized, how revocation races with admitted
work, which conflict/current-Version facts may be disclosed, and audit event
order. It does not add a second Head transition or make auth fields portable
identity.

`DEC-011` affects compatibility removal timing, not normal runtime parameter
semantics.

## 11. Runtime-to-owner call map

| Public operation | Application owner | Runtime-effect owner | LayerStack-0 owner |
|---|---|---|---|
| `exec_command` with explicit session | Auth/order/result mapping | Namespace/exec in live Workspace | Captured base is read-only; no publish by command alone |
| automatic `exec_command` | Auth/order and finalization orchestration | Temporary Workspace + command | Candidate admission + exactly one internal-OCC publish |
| command stdin/lines | Routing and bounds | Command stream/transcript | None |
| committed `file_read/list` | Select/capture request | Optional materialization/read adapter | Immutable read custody for one accepted Version |
| session `file_read/list/write/edit` | Target and API validation | Live Workspace file effect | No selected-reference mutation |
| no-session write/edit if retained | Full convenience composition | Temporary Workspace effect | Admission + one conditional publish |
| `file_blame` if retained | Auditability side-channel query | None | At most accepted-Version correlation; no authority |
| create/destroy Workspace | Lifecycle/order | Workspace/mount/network/cleanup | Capture/release immutable base custody as needed |
| publish Workspace | Auth/order, freeze/capture, expected Head from session | Drain/freeze/cleanup Workspace | Validate/admit, full compare, one OCC transition |

## 12. Phase 04 acceptance checks

- [ ] Runtime `sandbox_id` routing is identical across CLI/MCP/transport adapters.
- [ ] Committed `file_read` and selected `file_list` capture one immutable Version and survive concurrent Head movement coherently.
- [ ] Live file and command writes affect only an isolated Workspace.
- [ ] No runtime schema exposes a public revision, binding, Root/Head record, payload path, or mutation-target `VersionId`.
- [ ] `publish_workspace_session` has one internal expected Head and one conditional transition; stale does not merge/rebase/retry.
- [ ] Collision paths perform full canonical-byte comparison inside LayerStack-0 and fail closed.
- [ ] Automatic command finalization surfaces publication conflicts and bounds retained/recovery effects.
- [ ] `create_checkpoint` is absent from this family and publish-then-checkpoint is tested end to end.
- [ ] `DEC-001`, `DEC-017`, and `DEC-018` are explicitly resolved before final catalog/security acceptance.
- [ ] `file_list`, if promoted, has catalog/CLI/MCP/HTTP parity and bounded one-level results.
- [ ] Command output, content, edit arrays, paths, sessions, workers, FDs, memory, scratch, and cleanup debt are finite.
- [ ] Tests prove an Accepted Version cannot be opened writable or changed by `file_write`/`file_edit`.

## 13. Source and design anchors

Measured e497 declarations and implementations:

- `crates/sandbox-operations/catalog/src/runtime/command.rs`
- `crates/sandbox-operations/catalog/src/runtime/file.rs`
- `crates/sandbox-operations/catalog/src/runtime/workspace_session.rs`
- `crates/sandbox-operations/catalog/src/internal/runtime.rs`
- `crates/sandbox-daemon/src/http/api.rs`
- `crates/sandbox-runtime/operation/src/file/service/impls/{read,list,write,edit}.rs`
- `crates/sandbox-runtime/operation/src/workspace_session/**`

Design contracts:

- [Shared API contract](README.md)
- [Manager API](manager.md)
- [Ownership and boundaries](../design/01-ownership-and-boundaries.md)
- [Composed publication pipeline](../algorithm/02-references-and-publication/03-composed-publication-pipeline.md)
- [OCC publication algorithm](../algorithm/02-references-and-publication/02-occ-publication.md)
- [Read custody and runtime handoff](../algorithm/03-runtime-access-and-materialization/01-read-custody-and-runtime-handoff.md)
- [Runtime materialization](../algorithm/03-runtime-access-and-materialization/02-runtime-materialization.md)
- [Runtime-cluster backend-evidence boundary](../algorithm/03-runtime-access-and-materialization/README.md#backend-evidence-boundary)
- [Measured e497 surfaces](../phases/00-freeze-rules/inventory-surfaces.md)
