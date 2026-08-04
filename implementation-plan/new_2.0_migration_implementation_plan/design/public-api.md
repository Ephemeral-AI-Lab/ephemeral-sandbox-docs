---
status: draft-disposition
authority: public-api
depends-on:
  - REQ-API-001
  - REQ-API-002
  - REQ-API-005
  - REQ-API-006
---

# Public API behavior and disposition

## Responsibility

This file owns observable operation names/semantics, authorization order,
result classes, idempotency/replay, linearization requirements, and explicit
compatibility questions. It owns no storage format, pack, locator, cursor,
selector, replay encoding, GC method, crash protocol, runtime-effect call
count, or trait shape.

The mapping below is behavioral, not architectural. R0 tests whether existing
application owners can call the repurposed selected-state owner and applicable
current runtime-effect owners without adding an API family or aggregate seam.
`DEC-012` may reject R0. Every exact responsibility, call-edge, authority,
module, package, component, and process count remains open.

## Transport-aware populations that must remain distinct

1. `[MEASURED:e497-source]` The pinned public manager/runtime catalogs at
   `e4974d1f9aac702b35e052629cb070c897989352` expose **18** distinct operation
   names.
2. `[MEASURED:e497-observability-source]` The separate public observability
   catalog exposes **8** more distinct operation names through the CLI and MCP
   projections; sandbox-scoped requests reach the daemon observability
   dispatcher.
3. `[MEASURED:e497-http-source]` Daemon HTTP additionally exposes
   `POST /files/list`, internally `file_list`, outside those public catalogs.
   The public/tool operation-name subtotal is therefore **at least 27 names =
   18 manager/runtime + 8 observability + 1 HTTP-only exception**. It is not a
   27-row catalog.
4. `[MEASURED:e497-control-source]` The authenticated, sandbox-scoped private
   control RPC name `sandbox_daemon_ready` is inventoried separately from that
   27-name subtotal.
5. `[MEASURED:e497-http-source]` `GET /health` and the two `/forward/...` path
   families are HTTP endpoint/routing surfaces, not operation-name rows. They
   are inventoried separately below.
6. `[MEASURED:legacy-design-source]` The older migration workbook proposes
   **26** rows. It is design input, not deployed behavior.
7. `[CANDIDATE]` The earlier consolidated V2 ledger contains **25** rows: 14
   current names/reshapes proposed for retention, 10 unapproved legacy-only
   additions, and the separate `file_blame` decision.

The final V2 operation-name, endpoint, and route-family counts each remain
`[OPEN]`. A row in the 25-row ledger is not a product requirement. Every
current operation, endpoint, private control RPC, and routed path family needs
an explicit total disposition before retain/promote/reshape/migrate/remove is
accepted; every addition needs demonstrated callers and an approved product
decision.

## Pinned current inventory

| Operation-name population | Exact operation names | Count | Current projection/transport classification |
|---|---|---:|---|
| manager public catalog | `create_sandbox`, `list_docker_images`, `list_workspace_directories`, `destroy_sandbox`, `list_sandboxes`, `inspect_sandbox`, `squash_layerstacks`, `export_changes` | 8 | public catalog projected through current gateway clients |
| runtime public catalog | `exec_command`, `write_command_stdin`, `read_command_lines`, `file_blame`, `file_read`, `file_write`, `file_edit`, `create_workspace_session`, `publish_workspace_session`, `destroy_workspace_session` | 10 | public catalog projected through current gateway clients and routed to sandbox daemon RPC when sandbox-scoped |
| observability public catalog | `snapshot`, `trace`, `events`, `cgroup`, `resources`, `topology`, `daemon`, `layerstack` | 8 | public read/diagnostic catalog projected through observability CLI and MCP; sandbox-scoped requests dispatch in the daemon |
| HTTP-only internal operation name | `file_list`, reached as `POST /files/list` | 1 | public, unauthenticated host-loopback daemon HTTP exception; not a public-catalog row |

The pinned minimum public/tool operation-name subtotal is **27**. The following current
surfaces are counted separately so transport routes do not inflate that subtotal
and private control does not masquerade as a public catalog operation:

| Current surface | Current classification at e497 | Count treatment | Required Phase 0 disposition |
|---|---|---|---|
| `GET /health` | control surface, externally reachable on the unauthenticated host-loopback daemon HTTP listener but not a public operation-catalog row; reports liveness/telemetry | one HTTP endpoint, not an operation-name row | `OPEN`: retain as bounded control, promote, reshape, migrate, or remove; complete every mandatory field below |
| `/forward/shared/{port}/{tail...}` | public routed data-plane HTTP family on the unauthenticated host-loopback listener; proxies to a shared-workspace process target | one route family, not one row per path/method | `OPEN`: retain, promote, reshape, migrate, or remove; complete every mandatory field below |
| `/forward/isolated={workspace_id}/{port}/{tail...}` | public routed data-plane HTTP family on the unauthenticated host-loopback listener; resolves an isolated workspace target before proxying | one route family, not one row per workspace/path/method | `OPEN`: retain, promote, reshape, migrate, or remove; complete every mandatory field below |
| `sandbox_daemon_ready` | private authenticated sandbox-scoped control RPC used by the Docker daemon installer | one private control operation name, outside the 27-name public/tool subtotal | `OPEN`: retain as private control, promote, reshape, migrate, or remove; complete every mandatory field below |

The inventory comes from the pinned operation catalog and source hashes in
[the source manifest](../evidence/source-manifest.md).

### Mandatory total-surface disposition record

Every retained current row above, every retained manager/runtime/observability
operation, and `file_list` must carry all of the following fields. “Not
applicable” is a disposition requiring a falsifiable rationale and conformance
test; omission is not a disposition.

| Mandatory field | Required evidence before retention |
|---|---|
| callers | exact human, CLI, MCP, manager, provider, probe, proxy, and automation callers plus unused-surface evidence |
| authorization | actor, credential, scope, denial order, listener exposure, and information-disclosure boundary |
| request | exact method/name, transport framing, normalized inputs, size/cardinality bounds, and validation order |
| result | exact success/no-op/conflict/unsupported/uncertain or routed-response shape and visibility point |
| error | typed error/status vocabulary, partial-response law, and disclosure bounds |
| replay | idempotency key or request identity, duplicate law, retry horizon, and an executable `N/A` proof for streaming/pass-through traffic |
| revocation | accepted snapshot or race-safe cutoff and ordering relative to lookup, dispatch, streaming, and disclosure |
| generation | exact sandbox/workspace/allocation generation binding and stale-target behavior, or an executable `N/A` proof |
| recovery | restart/crash behavior, retained custody, ambiguity, cleanup, and operator path |
| cancellation | disconnect, timeout, shutdown, child-task join, and post-cancellation effect/result behavior |
| resource | admission order plus byte, entry, memory, process, socket, duration, concurrency, and cleanup ceilings |
| transport | CLI/MCP/RPC/HTTP mapping, method/path family, authentication placement, framing, and upgrade/stream behavior |
| compatibility | current caller migration, version/removal window, shim owner/telemetry, and retirement gate |

### Non-authority law for diagnostic and control surfaces

Observability operations may read bounded diagnostic projections from existing
owners; they do not select `StateId`, write an authoritative head, own request
outcomes/effect custody, allocate a runtime generation, or become a storage
authority. `GET /health` and `sandbox_daemon_ready` report bounded liveness,
telemetry, identity, and readiness facts only. The `/forward/...` handler may
route bytes to an already selected runtime process target, but it owns neither
the upstream effect nor replay, storage, lifecycle, or selected-state truth.
Retaining or reshaping any of these surfaces cannot turn it into a selected-state
writer, selector, repair authority, or independent source of durable truth.

These current questions remain open and cannot be erased by a target table:

- `list_docker_images` and `list_workspace_directories`: retain as
  discovery/administration, reshape, or remove only after caller and transport
  inventory.
- `squash_layerstacks`: V2 steady state cannot implement logical squash;
  decide compatibility failure/removal timing and migration-only behavior.
- `inspect_sandbox` versus proposed `get_sandbox`: semantic/signature/result
  equivalence or an explicit compatibility migration is unproved.
- `export_changes` versus proposed `export_sandbox`: source scope and output
  compatibility are unproved.
- `file_blame`: `DEC-001` must retain exact attribution or approve a breaking
  removal.
- no-session `file_write`/`file_edit`: current e497 behavior publishes a legacy
  layer; the V2 compatibility result is unresolved and cannot recreate layers.
- HTTP-only `file_list`: retain as exception, promote, reshape, or remove under
  `DEC-017`; it is not silently absorbed by another method.
- the eight observability names, including storage-adjacent `layerstack`: retain
  as bounded diagnostics, reshape, migrate, or remove only with caller,
  authorization, result/error, replay/revocation, resource, and compatibility
  evidence; no diagnostic projection becomes storage authority.
- `GET /health`, both `/forward/...` families, and `sandbox_daemon_ready`: close
  their separate public/private/control dispositions and mandatory records;
  listener reachability or path routing is not permission to omit them.

## HTTP-only `file_list`

`[MEASURED:e497-http-source]` Current `POST /files/list` accepts optional
`path`, `workspace_session_id`, and `limit`; `limit >= 1` is clamped to the
daemon safety maximum. It returns normalized path, bounded entries containing
`name`, `kind`, and `size`, plus `truncated`. The daemon currently creates the
internal request ID.

Its disposition remains `OPEN — DEC-017`. If retained, Phase 0 freezes
authorization, deterministic order, continuation/truncation, captured committed
view versus live-session mutation semantics, traversal and byte/entry ceilings,
cancellation, replay identity, transport compatibility, and callers. Listing
is not `file_read`: enumeration and bounded range reads have different
cardinality, consistency, and denial-of-service laws.

## One `file_{verb}` family

The V2 public namespace has one `file_{verb}` family. It does **not** add
`workspace_file_read`, `workspace_file_write`, `workspace_file_edit`,
`workspace_file_list`, or any other workspace-prefixed alias. Compatibility is
handled at the existing names and edge, not by doubling the method surface.

### `file_read`

`file_read` has one request with optional `workspace_session_id`:

```text
FileReadRequest {
  sandbox_id,
  workspace_session_id: Option<WorkspaceSessionId>,
  path,
  offset,
  limit
}

FileReadTarget =
  | Committed { sandbox_id, captured_head_revision }
  | Workspace { sandbox_id, workspace_session_id, allocation_generation }
```

- Omitted `workspace_session_id` means exactly one captured committed revision.
  The accepted selected-state owner captures the authoritative head once; the
  entire bounded read uses that immutable view even if publication occurs
  concurrently.
- Supplied `workspace_session_id` means the named live workspace session. The
  server proves it belongs to the authorized sandbox and resolves its exact
  opaque allocation generation before calling the current live-file owner.
- The edge normalizes to one closed target, never both branches. Public
  framing, normalized path/range validation, byte bounds, cancellation, and
  typed errors are shared; authority, custody, calls, and costs remain
  branch-specific.
- `FileReadTarget` is an internal closed value, not a public alias, runtime
  enum, new operation, or storage interface.

### `file_write` and `file_edit`

A committed V2 state is immutable. The V2 semantic core therefore requires an
explicit live workspace session for `file_write` and `file_edit`; selected
truth is never mutated in place. The current omitted-session behavior
must receive an accepted `DEC-017` compatibility disposition after caller
inventory. The implementation must not silently create a hidden session,
publish a layer, mutate a committed root, or add workspace-prefixed aliases.

### `file_list` and `file_blame`

If retained, `file_list` stays in the same naming family and receives its own
bounded listing contract. `file_blame` remains the existing name if `DEC-001`
retains exact attribution; removing attribution removes the method through an
approved compatibility decision rather than adding a replacement name.

## Candidate target ledger, still unapproved

The table preserves the existing 25-row proposal so none of its behavior is
silently accepted or lost. `PROPOSED ADD` remains a product question.

| # | Candidate operation and current status | Existing application-owner role | Selected-state behavior | Current runtime-effect behavior / open proof |
|---:|---|---|---|---|
| 1 | `create_sandbox` — e497, proposed retain | authenticate, validate import, map result | create one authoritative head/revision and exact outcome | none unless current product truly requires immediate realization; import/durability proof open |
| 2 | `get_sandbox` — proposed reshape of `inspect_sandbox` | authorize and translate only if compatibility accepted | read one bounded authoritative aggregate | none; exact current equivalence open |
| 3 | `list_sandboxes` — e497, proposed retain | authorize and bound pagination | one bounded ordered query | none; pagination consistency/limits open |
| 4 | `destroy_sandbox` — e497, proposed retain | enforce quiescence and closed result | remove semantic head with no speculative capacity credit | dispose only an explicitly owned live allocation; cascade/replay/retention open |
| 5 | `export_sandbox` — proposed reshape of `export_changes` | authorize and stream | capture/read one committed root view | none for committed export; exact source/output compatibility open |
| 6 | `create_workspace_session` — e497, proposed retain | reserve, prepare, realize, activate, terminalize | bind origin/revision, frozen actor, request/effect custody, opaque allocation binding | hidden allocate/realize/attest/activate; all crash cuts open |
| 7 | `get_workspace_session` — legacy-only, `PROPOSED ADD` | authorize/map | bounded session query | optional live status only if required; caller need and private-state leakage open |
| 8 | `list_workspace_sessions` — legacy-only, `PROPOSED ADD` | authorize/bound pagination | bounded per-sandbox query | none; caller need/consistency/limits open |
| 9 | `publish_workspace_session` — e497, proposed retain | fence, capture, coordinate OCC and result | verify exact origin; select one complete state/outcome or conflict | stable portable capture; retain exact conflict generation read-only or dispose per accepted result |
| 10 | `destroy_workspace_session` — e497, proposed retain | prepare, fence/drain, dispatch disposal, terminalize | durable custody and semantic close/delete at accepted point | generation-bound synchronized disposal; replacement safety open |
| 11 | `create_checkpoint` — legacy-only, `PROPOSED ADD` | authorize named-root request | metadata-only retained-root transition | none; caller need and zero-payload-copy proof open |
| 12 | `get_checkpoint` — legacy-only, `PROPOSED ADD` | authorize/map | bounded immutable-root query | none; caller need/ownership open |
| 13 | `list_sandbox_checkpoints` — legacy-only, `PROPOSED ADD` | authorize/bound pagination | bounded ownership query | none; caller need/consistency open |
| 14 | `remove_checkpoint` — legacy-only, `PROPOSED ADD` | authorize/map in-use result | remove semantic root only when allowed; no early credit | none; exact reachability/reader safety open |
| 15 | `rollback_sandbox` — legacy-only, `PROPOSED ADD` | authorize/quiesce target | OCC head-reference move or exact no-op; no delta replay | only if accepted product requires live realization; caller need open |
| 16 | `fork_sandbox` — legacy-only, `PROPOSED ADD` | deterministic ordering and closed result | atomically create bounded child/root/provenance references with zero selected-state immutable payload copy | none unless separately accepted immediate realization; caller need open |
| 17 | `get_sandbox_parent` — legacy-only, `PROPOSED ADD` | authorize/map | read immutable immediate provenance | none; caller need and parent-destruction behavior open |
| 18 | `commit_fork` — legacy-only, `PROPOSED ADD` | ordered gates and decision | atomically evaluate accepted parent/child/root preconditions and OCC-move target head | none; caller need and stale-parent/sibling semantics open |
| 19 | `exec_command` — e497, proposed retain | authorize exact session, prepare custody, dispatch, map ambiguity | durable custody before dispatch plus exact outcome | generation-bound command effect; no silent retry and containment open |
| 20 | `write_command_stdin` — e497, proposed retain | authorize/bound/sequence accepted input | durable binding/custody and exact accepted result as required by stream contract | bounded delivery to exact command generation; ordering/partial acceptance open |
| 21 | `read_command_lines` — e497, proposed retain | authorize/bound cursor/result | durable transcript only if current contract requires it | bounded output read; cursor/restart/retention compatibility open |
| 22 | `file_read` — e497, proposed retain | normalize one optional-session target | omitted session: capture/read one committed revision; supplied: resolve exact opaque binding | omitted: none; supplied: bounded read from named live generation |
| 23 | `file_write` — e497, proposed reshape | require explicit session in V2 core; own ambiguity policy | durable custody before dispatch plus exact outcome | bounded mutation of exact live generation; no-session compatibility open |
| 24 | `file_edit` — e497, proposed reshape | require explicit session; validate edits/ambiguity | durable custody before dispatch plus exact outcome | bounded mutation of exact live generation; atomic/partial/no-session behavior open |
| 25 | `file_blame` — e497, `OPEN — DEC-001` | authorize/map or execute approved removal | selected canonical attribution only if retained | none; caller/product decision and exact method open |

The three unmatched manager/runtime catalog operations, eight observability
operations, separate HTTP-only `file_list`, private readiness control RPC, and
three HTTP endpoint/route surfaces remain outside these 25 rows until their
dispositions close. The route families are not candidate operation rows. The
table does not invent methods for MCTS: if checkpoint/fork operations are
accepted, an external policy caller composes them; the selected-state owner
exposes no rollout scheduler, search, scoring, or backpropagation API.

The zero-copy fast path applies only after collision-safe admission has proved
an **accepted, no-alias `StateId` binding**. A digest computed from canonical
bytes is only a candidate identifier. If that digest is already occupied, the
selected-state owner compares the exact canonical bytes: equal bytes coalesce;
unequal bytes terminate as `T03_REJECTION / STATE_ID_COLLISION`. A collision
must not create an alias, head, root, mapping, index entry, revision, custody
claim, or capacity credit, and must not enter the reference-only fast path.

For every same-accepted-`StateId` checkpoint creation, reference-only fork,
rollback-to-existing, `commit_fork` winner transfer, same-state no-op
publication, and future reference move/ownership transfer, the complete
operation—not merely a step labelled “copy”—must satisfy:

```text
total selected-state immutable payload bytes read = 0
total selected-state immutable payload bytes written = 0
total selected-state immutable payload bytes copied = 0
new root-private physical closure bytes = 0
```

Bounded root/provenance metadata I/O is measured separately. Validation,
warming, prefetch, recovery, and retry labels cannot evade the selected-state
immutable payload boundary measurement. A runtime-owner-private mutable
realization is separately admitted
and charged. Its private materialization does not change these selected-state
counters, but any actual selected-state immutable payload read, write, or copy
remains selected-state work and cannot be relabeled as runtime realization.
Collision admission, exact-byte comparison, bounded quarantine/cleanup, and its
terminal replay result are charged separately from the accepted-state COW
operation. Recovery and index rebuild fail readiness closed if an occupied
candidate digest cannot be proved to name exactly one canonical byte string.

## Cross-effect proof

Every retained operation touching both selected state and a mutable runtime
effect must record:

1. authorization plus the frozen acquisition order for each disjoint owner's
   local permits;
2. one public outcome/visibility point and every ordered selected-state call,
   custody point, runtime dispatch/effect point, cleanup barrier, and response;
3. distinct RequestOutcome, EffectCustody, and opaque allocation-binding
   lifetimes;
4. all cancellation and persisted durability cuts, with process crash,
   `SIGKILL`, host crash, and power loss tested as distinct faults including
   commit-before-response, plus the normative real-substrate receipts where
   applicable;
5. safe retry, real compensation, terminal `OutcomeUnknown`, unresolved
   quarantine, and operator resolution;
6. exact response/replay law; and
7. retention/cleanup convergence and resource plateau.

The selected-state writer never calls a mutable runtime-effect owner. A
runtime-effect owner never writes selected truth. Existing application owners
order the calls and create no new durable truth. R0 creates no global admission
ledger: every owner charges local capacity first, while Phase 1 compares any
proved aggregate placement. The exact total graph remains open, and this
section is replaced if `DEC-012` selects another architecture.

## Result, replay, and authorization laws

- Every uniquely accepted fresh mutation eventually has one exact closed
  accepted/no-op/conflict/rejected/unsupported/uncertain result. A duplicate
  during non-visible `PendingResponse` or open custody receives bounded
  nonterminal status and is not a new mutation.
- Transport retry cannot re-execute a durably accepted effect inside the finite
  replay horizon. Commit-before-response may expose complete new truth; exact
  replay returns it without redispatch.
- Content identity is not head revision. Conflict exposes no physical locator,
  runtime handle, selector, or repair hook and changes no head.
- Pre-admission overload and current authorization denial are transient edge
  results, not durable outcomes, do not replace retained state, and authorize
  no dispatch.
- After accepted authorization and bounded admission, the accepted durable
  owner bind-or-verifies authenticated namespace, key, and immutable normalized
  descriptor. Mismatch returns only `request-identity-conflict`, creates no
  custody/dispatch, and reveals no prior state.
- Outcome pruning never makes an old identity fresh. Bounded authenticated
  evidence returns `replay-expired` before custody/dispatch; absence is never
  freshness.
- Fresh static/semantic rejection is authority-atomically recorded as exact
  `Rejected` without EffectCustody before response.
- No terminal result is public or replay-visible before result-specific
  cleanup, request-work join, capacity visibility, and durable resource
  attribution cross one barrier. The accepted durable owner terminalizes it
  before first response.
- An unknowable runtime effect is neither converted to success nor silently
  retried. `OutcomeUnknown` may replay while custody remains open and the exact
  generation remains fenced, charged, and quarantined.
- Every operation names the accepted `DEC-018` snapshot or race-safe
  revocation-cutoff policy and its order relative to binding, lookup, prepare,
  dispatch, terminalization, and disclosure. Check-then-wait is not a fence.

## Compatibility and quiescence

V2 preserves current observable behavior unless an approved decision says
otherwise. A shim translates only accepted API shape; it cannot restore layers,
squash, writable dual truth, a second selector, runtime brands, physical
locators, client transactions, hidden sessions, or workspace-prefixed file
aliases. Every shim has telemetry, an owner, and a Phase 2C retirement gate plus
fresh Phase 2D proof in the requalified `H_RELEASE` artifact. Any
destructive legacy-data deletion is a separately signed post-release action.

Phase 0 identifies operations requiring per-sandbox quiescence versus a captured
immutable revision. Multi-sandbox gates use deterministic order and release on
failure; they never wait while holding an unrelated authority or partially
change durable truth.

No selected-state or runtime-effect method signature is accepted until the
complete current and proposed operation matrix, `DEC-001`, `DEC-017`,
`DEC-018`, and `DEC-012` are closed.
