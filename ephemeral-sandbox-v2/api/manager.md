# Manager API — lifecycle, Checkpoints, fork, and rollback

Date: **2026-08-04**  
Status: **DESIGN DRAFT — proposed Phase 04 public surface**

The manager family owns product-level sandbox lifecycle and discovery. For V2
it also orchestrates Checkpoint, fork, and rollback workflows while leaving
selected-Version truth and the sole conditional Head transition inside
LayerStack-0.

This file is subordinate to the shared [API contract](README.md), the product
[hard rules](../PRD.md#hard-rules-must-never-break), and the selected
[architecture](../architecture_design.md).

## 1. Family boundary

```text
caller / CLI / MCP
        |
        v
sandbox-manager application owner
  - authentication and authorization
  - lifecycle and request ordering
  - public ID resolution and response mapping
  - runtime provisioning / teardown
        |
        +-----------------------> provider/runtime lifecycle effects
        |
        `-----------------------> existing operation service
                                      |
                                      v
                                  LayerStack-0
                                  - accepted bindings
                                  - fixed Checkpoint Roots
                                  - sandbox/Branch Heads
                                  - one internal OCC transition

manager -X-> direct writes to versions/, roots/, heads/, or store control data
caller  -X-> raw VersionId, AcceptedBinding, HeadRevision, or payload path
```

The manager may compose store and runtime calls. It does not become a second
Version writer, perform full-byte collision acceptance itself, or make
observability authoritative.

## 2. Operation index

| Operation | Evidence label | V2 disposition | Required arguments | Optional arguments | Primary effect |
|---|---|---|---|---|---|
| `create_sandbox` | `SOURCE-VERIFIED` | rewrite internals | `image`, `workspace_root` | `count=1` | Provision sandbox and establish its initial selected accepted Version |
| `destroy_sandbox` | `SOURCE-VERIFIED` | retain with exact reference lifecycle | `sandbox_id` | — | Stop runtime and remove sandbox-owned references/resources safely |
| `inspect_sandbox` | `SOURCE-VERIFIED` | rewrite result | `sandbox_id` | — | Read lifecycle and bounded selected-Version summary |
| `list_sandboxes` | `SOURCE-VERIFIED` | rewrite result | — | — | List bounded manager records |
| `fork_sandbox` | `OPEN` | proposed public; guarded by `API-D09` | source `sandbox_id` | `checkpoint_id` | Create another logical sandbox/Branch Head from an accepted Version |
| `rollback_sandbox` | `OPEN` | proposed public | target `sandbox_id`, `checkpoint_id` | — | Strict internal-OCC Branch Head replacement to an existing Checkpoint binding |
| `create_checkpoint` | `OPEN` | proposed public; owner-directed shape | `sandbox_id` | `name` | Create a fixed typed Root for the currently selected accepted Version |
| `inspect_checkpoint` | `OPEN` | proposed public | `sandbox_id`, `checkpoint_id` | — | Read one fixed Checkpoint's metadata |
| `list_checkpoints` | `OPEN` | proposed public | `sandbox_id` | `limit=100`, `cursor` | List fixed Checkpoints in bounded pages |
| `remove_checkpoint` | `OPEN` | proposed public | `sandbox_id`, `checkpoint_id` | — | Exactly remove one fixed Root; payload retirement remains internal |
| `list_docker_images` | `SOURCE-VERIFIED` | current OCI/Docker discovery only | — | — | Discover current Docker creation inputs |
| `list_workspace_directories` | `SOURCE-VERIFIED` | current manager-host discovery | — | `path` | Browse bounded host workspace inputs |
| `export_changes` | `SOURCE-VERIFIED` | rewrite semantics | `sandbox_id`, `dest` | `format=dir` | Export a captured complete-Version difference without layer-chain truth |

For every `SOURCE-VERIFIED` row, source metadata is the sealed product tree on
branch `codex/new-2.0-storage-core` at
`e4974d1f9aac702b35e052629cb070c897989352`; the label is not a V2 correctness
result. Proposed rows remain `OPEN`. This table states no performance verdict.

The proposed family has 13 operations. Public/internal
`squash_layerstack(s)` is removed and is not counted.

## 3. Shared manager conventions

### CLI spelling

```text
sandbox-manager-cli <operation> [arguments]
```

Catalog and MCP arguments use snake case. CLI flags use kebab case. Examples:

```text
checkpoint_id  <->  --checkpoint-id
workspace_root <->  --workspace-bind-root
```

The existing `--workspace-root` alias may remain for compatibility, but the
catalog/MCP field remains `workspace_root`.

### Selector rules

- `sandbox_id` selects the product sandbox/Branch context.
- `checkpoint_id` is the only public accepted-Version selector for fork and
  rollback.
- `VersionId` may be returned but is never accepted as a mutation input.
- No operation accepts a public revision, expected Head, Root record, store
  generation, force flag, collision override, or filesystem path to storage.
- A Checkpoint ID is immutable and non-retargetable. `name` is display metadata
  and cannot replace the stable ID in a mutation.

### Internal OCC rule

No manager command accepts `expected_revision`. For every Head-changing
operation, the application captures one current expected Head internally after
the request enters its authorization/order boundary, then submits exactly one
conditional transition. Stale returns `conflict`; it never triggers internal
recapture, merge, or rebase.

## 4. Sandbox lifecycle

### 4.1 `create_sandbox`

Create one or more sandbox records and runtime sandboxes from the selected
image and host Workspace source.

```text
sandbox-manager-cli create_sandbox \
  --image IMAGE \
  --workspace-bind-root ABSOLUTE_PATH \
  [--count N]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `image` | yes | string | Container image reference accepted by the configured provider |
| `workspace_root` | yes | absolute host path | Source Workspace directory selected for provisioning; V2 portable identity never includes this host path |
| `count` | no | integer, default `1`, minimum `1` | Number of sandboxes to create within configured fleet/resource limits |

V2 composition:

1. authorize and validate the host/provider inputs;
2. provision bounded lifecycle resources using existing manager/provider owners;
3. capture complete portable facts for the initial Workspace through the
   selected Phase 02/03 path;
4. admit one complete immutable Version in each applicable LayerStack-0 store;
5. call `CreateHeadIfAbsent(head_identity, Expected::Absent, new_binding)` and
   any required `CreateFixedRootIfAbsent(...)`, and durably establish those
   references before declaring that
   sandbox ready; and
6. return manager records only after lifecycle and store readiness agree.

The exact provider sequence is Phase 04/05 implementation work. `count > 1`
does not imply cross-store payload deduplication: hard rule 2 is scoped to one
LayerStack-0 instance. Host caches, Docker volumes, mounts, and image IDs are
runtime/private provisioning facts, never Version identity.

Successful result fields should include:

| Field | Meaning |
|---|---|
| `sandboxes[]` | Created sandbox records, each with opaque `sandbox_id` and lifecycle state |
| `VersionId` | Optional accepted initial-Version correlation per sandbox; not a capability |
| `ready` | Whether both runtime and LayerStack-0 readiness gates passed |
| `warnings[]` | Bounded partial/provider notices that do not conceal failure |

If a multi-create partially succeeds, the response must enumerate each
sandbox outcome. It must not report an all-or-nothing success unless rollback
of every created lifecycle/store reference is proved. Cleanup remains bounded;
external source workspaces and shared caches are not deleted as rollback.

Safe read-back: `list_sandboxes` and `inspect_sandbox`.

### 4.2 `inspect_sandbox`

```text
sandbox-manager-cli inspect_sandbox --sandbox-id SANDBOX
```

| Argument | Required | Type | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox to inspect |

The result may include lifecycle state, image/provider summary, configured
Workspace source display data, daemon endpoint state, current accepted
`VersionId` correlation, Checkpoint count, active Workspace count, and
readiness. It must not expose `AcceptedBinding`, `HeadRevision`, store paths,
mount paths as portable facts, auth secrets, or raw integrity records.

Inspection captures a coherent bounded summary. It is not a lock or mutation
precondition and its Version may be stale immediately after return.

### 4.3 `list_sandboxes`

```text
sandbox-manager-cli list_sandboxes
```

No arguments. It returns the bounded manager-known sandbox records. The e497
surface has no pagination argument; Phase 04 must either prove the configured
fleet bound makes one result safe or version the operation with bounded
pagination. It must not silently truncate without a `truncated` indication.

### 4.4 `destroy_sandbox`

```text
sandbox-manager-cli destroy_sandbox --sandbox-id SANDBOX
```

| Argument | Required | Type | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox incarnation to stop and remove |

Required behavior:

1. authorize destruction and enter a manager-owned stopping state;
2. reject or drain new application mutations under the selected lifecycle
   protocol;
3. stop commands, Workspaces, daemon, and provider effects using existing
   owners;
4. read the exact complete records, then use
   `RemoveHead(Expected::Exact(expected_head))` and
   `RemoveFixedRoot(Expected::Exact(expected_root))` through LayerStack-0;
5. let exact internal reachability/custody checks decide whether any accepted
   payload becomes retirement-eligible; and
6. persist the terminal manager outcome without claiming cleanup that failed.

Destroying a reference is not a direct payload deletion request. A Version
shared by another Head, Checkpoint, or active read custody remains. The command
does not delete the caller's host Workspace, shared base cache, migration data,
or legacy data unless a separately authorized lifecycle contract says so.

Safe read-back: `inspect_sandbox` or `list_sandboxes`. `not_found` after an
unknown transport result can satisfy the intended postcondition when sandbox
IDs are never reused.

## 5. Checkpoint operations

### 5.1 Checkpoint model

```text
Sandbox/Branch Head                     fixed Checkpoint Root
  selected Version V8                         checkpoint C42
         |                                          |
         +--------------------+---------------------+
                              v
                  one Accepted Version V8

create_checkpoint changes reference metadata only:
  accepted payload bytes read    = 0
  accepted payload bytes written = 0
  accepted payload bytes copied  = 0
```

A Checkpoint is a fixed Root to an already accepted Version. It is not a
Workspace freeze request, archive, directory copy, layer, mutable label, or raw
digest. Creating a new Checkpoint for live changes is deliberately a two-step
public workflow:

```text
publish_workspace_session(workspace_session_id)
    -> selected accepted Version V9
create_checkpoint(sandbox_id, name?)
    -> fixed Checkpoint Root C43 -> V9
```

### 5.2 `create_checkpoint`

```text
sandbox-manager-cli create_checkpoint \
  --sandbox-id SANDBOX \
  [--name DISPLAY_NAME]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox whose selected accepted Version is captured |
| `name` | no | bounded UTF-8 display string | Non-authoritative display metadata; need not be globally unique |

Forbidden parameters include `workspace_session_id`, `VersionId`, a Checkpoint
target, public revision, filesystem path, and `force`.

The application authorizes the request, captures the selected accepted binding
once, allocates a non-reusable opaque `checkpoint_id`, and calls
`CreateFixedRootIfAbsent(root_identity, Checkpoint, Expected::Absent,
binding)`. LayerStack-0 validates accepted-binding metadata and writes only
bounded Root metadata; it never opens or copies payload bytes. A Root already
present under that identity returns `ALREADY_EXISTS`; retry after
`OUTCOME_UNKNOWN` first reads that exact Root authoritatively.

Result:

| Field | Meaning |
|---|---|
| `checkpoint_id` | Stable immutable Checkpoint identity |
| `sandbox_id` | Owning/authorization scope |
| `name` | Display metadata, if supplied |
| `VersionId` | Accepted Version correlation, not a mutation capability |
| `created_at` | Application/record timestamp for display and ordering; not portable Version identity |

Safe read-back: `inspect_checkpoint` or `list_checkpoints`. If a response is
lost after Root creation, read-back must identify the allocated ID through the
operation's internal request correlation; the application must not create
unbounded duplicate Checkpoints on blind retry.

### 5.3 `inspect_checkpoint`

```text
sandbox-manager-cli inspect_checkpoint \
  --sandbox-id SANDBOX \
  --checkpoint-id CHECKPOINT
```

| Argument | Required | Type | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Authorization and store scope |
| `checkpoint_id` | yes | opaque string | Exact fixed Checkpoint identity |

Returns the public fields of the Checkpoint plus availability/readiness state.
It does not expose the Root record, accepted binding, Head revision, physical
payload location, or canonical bytes.

### 5.4 `list_checkpoints`

```text
sandbox-manager-cli list_checkpoints \
  --sandbox-id SANDBOX \
  [--limit N] \
  [--cursor OPAQUE]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Authorization and store scope |
| `limit` | no | integer, proposed default `100`, maximum `1000` | Maximum returned Checkpoints |
| `cursor` | no | opaque string | Continuation from a prior result under the same scope/order |

The selected default and maximum are proposed and carry evidence label `OPEN`;
they are not e497 source facts.
Phase 04 may tighten them under configured finite limits. Ordering must be
stable and explicit, for example creation order plus stable ID. The result
contains `checkpoints[]`, optional `next_cursor`, and `truncated`.

### 5.5 `remove_checkpoint`

```text
sandbox-manager-cli remove_checkpoint \
  --sandbox-id SANDBOX \
  --checkpoint-id CHECKPOINT
```

| Argument | Required | Type | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Authorization and store scope |
| `checkpoint_id` | yes | opaque string | Exact fixed Checkpoint to remove |

Removal reads the complete Root and calls
`RemoveFixedRoot(root_identity, Checkpoint,
Expected::Exact(expected_root))` under LayerStack-0's transition authority. It
does not retarget the Checkpoint, delete a Version directly, scan/copy payload,
or expose a GC command. Internal exact revalidation of Heads, other Roots, and
read custody determines later retirement eligibility.

Result includes the removed `checkpoint_id`, its public `VersionId`
correlation when disclosure is allowed, and `retirement_scheduled` as a
non-authoritative hint at most. It must never claim `payload_deleted=true`
without the internal retirement outcome and must not make synchronous payload
deletion part of the public contract.

Safe read-back: `inspect_checkpoint`; `not_found` can establish the intended
postcondition because Checkpoint IDs are not reused.

## 6. Fork and rollback

### 6.1 `fork_sandbox`

```text
sandbox-manager-cli fork_sandbox \
  --sandbox-id SOURCE_SANDBOX \
  [--checkpoint-id CHECKPOINT]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Source sandbox/Branch context |
| `checkpoint_id` | no | opaque string | Only optional Version selector. Omit to capture the source's currently selected accepted Version; supply to fork from that fixed Checkpoint. |

There is no public `VersionId`, revision, destination ID, image, Workspace
session, payload mode, or backend selector. The manager allocates the target
sandbox identity and inherits the source's authorized runtime configuration
according to product policy.

Conceptual reference path:

```text
source selector
  checkpoint supplied? ---- yes ---> resolve fixed Checkpoint binding
          |
          no
          v
  capture source Head binding once
          |
          v
  CreateHeadIfAbsent(target Head, Expected::Absent, source binding)
          |
          +--> payload read/write/copy = 0/0/0
          |
          v
  manager creates target product record
          |
          v
  runtime activation (separate; may materialize/read payload)
```

The result includes new `sandbox_id`, source sandbox ID, optional source
Checkpoint ID, selected `VersionId` correlation, lifecycle/activation state,
and whether the **reference step** reported payload bytes `0/0/0` through the
qualified store instrumentation.

#### Mandatory architecture guard

The hard-rule fork is a same-store reference operation. The sealed e497
deployment currently gives sandboxes per-sandbox runtime/storage custody; the
selected architecture does not automatically prove a new independently
provisioned sandbox can share the source store's accepted payload.

Before implementing this public name, Phase 04 must select and prove one of
these coherent meanings without adding an unreviewed authority:

1. `fork_sandbox` creates another product Branch/Head inside the same
   LayerStack-0 instance and runtime activation remains a separate effect; or
2. the product renames/narrows the reference operation to `fork_branch`, while
   independent sandbox provisioning is documented as a potentially
   byte-moving operation.

If product requirements instead demand independent per-sandbox stores **and**
zero-payload sharing between them, Phase 01 must be reopened with the required
shared ownership/topology. Copying/exporting/importing the Version into another
store and reporting it as a zero-payload fork is forbidden.

Safe read-back: `list_sandboxes` and `inspect_sandbox` using internal request
correlation for an outcome-unknown create.

### 6.2 `rollback_sandbox`

```text
sandbox-manager-cli rollback_sandbox \
  --sandbox-id TARGET_SANDBOX \
  --checkpoint-id CHECKPOINT
```

| Argument | Required | Type | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox/Branch Head to move |
| `checkpoint_id` | yes | opaque string | Only permitted Version target; must resolve to an authorized fixed Checkpoint in the same LayerStack-0 store |

Rollback deliberately has no omitted-target default. “Latest Checkpoint” is
ambiguous under concurrency, and “current Version” is a no-op rather than a
rollback. It accepts neither `VersionId` nor a public expected revision.

Conceptual flow:

```text
authorize target sandbox + checkpoint
        |
resolve Checkpoint -> store-validated accepted binding
        |
capture target Head (binding, revision) internally exactly once
        |
LayerStack-0 `ReplaceHead(Expected::Exact(captured complete Head), binding)`
  - revalidate checkpoint binding metadata
  - reread complete current Head
  - compare internal expected tuple
  - replace complete Head or return stale
        |
success: reference metadata only, payload 0/0/0
stale:   no Head change, no merge/rebase, no hidden retry
```

Runtime treatment of a live Workspace is application/effect policy: Phase 04
must either reject rollback while a live Workspace can conflict, or close/fence
that Workspace under an explicit authorized protocol. Rollback may not mutate
the Workspace or Accepted Version behind another owner's back. `DEC-018`
controls authorization/revoke ordering, not the store transition.

Result includes sandbox ID, Checkpoint ID, selected `VersionId`, transition
outcome, and reference-path byte counters when exposed. It never returns the
Head revision as a new caller token.

Safe read-back: `inspect_sandbox`. A stale result requires an explicit new
request after inspection; the server never retries against a newly captured
Head within the original request.

## 7. Discovery operations

### 7.1 `list_docker_images`

```text
sandbox-manager-cli list_docker_images
```

No arguments. Returns bounded local Docker image references available to
`create_sandbox`, including the e497-compatible untagged image-ID form where
supported. Docker is a current provider capability, not a LayerStack-0 identity
field or permanent backend requirement.

### 7.2 `list_workspace_directories`

```text
sandbox-manager-cli list_workspace_directories [--path ABSOLUTE_PATH]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `path` | no | absolute host path | Omit to list picker-visible roots; supply to list immediate subdirectories |

The e497 implementation caps a selected directory browse at 500 immediate
subdirectories. Results are manager-host discovery only. A returned path never
becomes a portable Version fact, Checkpoint ID, or store path.

## 8. `export_changes`

```text
sandbox-manager-cli export_changes \
  --sandbox-id SANDBOX \
  --dest ABSOLUTE_HOST_DESTINATION \
  [--format dir|tar|tar-zst]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox whose selected accepted Version is captured for export |
| `dest` | yes | absolute host path | Manager-owned output destination; never portable Version identity |
| `format` | no | enum `dir`, `tar`, `tar-zst`; default `dir` | Output representation |

The operation name is retained, but the e497 “fold every published layer above
base” implementation is not V2 semantics. The V2 operation must:

1. capture one selected accepted Version with read custody;
2. compare/project it against the sandbox's immutable creation-base Root or
   another product-selected fixed baseline that is not supplied as a raw ID;
3. derive the output from complete Version facts, including deletions, without
   reconstructing parents, layer depth, whiteout history, or squash state;
4. write through bounded scratch and safe manager destination handling; and
5. release custody and clean/recover bounded spool debt.

The exact complete-Version differ and destination-atomicity contract is
`OPEN_WITHIN_R0` for Phase 04. If the product wants full-Workspace export
rather than changes from the immutable creation base, it should version or
rename the public operation; it must not preserve a misleading layer-based
meaning.

Result includes captured `VersionId`, baseline kind, format, destination,
bounded entry/byte totals, and truncation/error status. Export is read-only with
respect to selected-Version truth.

## 9. Removed manager operation

### `squash_layerstacks` — remove from V2

```text
e497 public:  squash_layerstacks --sandbox-id SANDBOX
e497 internal: squash_layerstack
V2:            no operation and no replacement
```

Complete immutable Versions have logical layer depth zero. Keeping a public
squash command would falsely preserve layer-chain truth or create an
unnecessary physical-rewrite control surface. Physical cleanup is internal
bounded retirement/recovery, not a user compaction command.

Compatibility behavior should return a stable removed/unsupported error during
the migration window, emit bounded diagnostics if useful, and delete the route,
handler, tests, configuration, and legacy concepts after the owner-selected
`DEC-011` window. It must never silently translate squash into payload rewrite.

## 10. Manager-to-LayerStack-0 call map

Conceptual names are internal responsibilities, not public Rust signatures.

| Public operation | Application/lifecycle work | LayerStack-0 work | Runtime/provider work |
|---|---|---|---|
| `create_sandbox` | Auth, allocate record, order readiness | Admit initial Candidate; `CreateHeadIfAbsent`; create any required fixed Roots | Provision image, volumes/effects, daemon |
| `destroy_sandbox` | Fence ingress, persist lifecycle | `RemoveHead` and `RemoveFixedRoot` with exact expected records; later exact retirement | Stop Workspaces/commands/daemon/provider resources |
| `inspect_sandbox` | Join bounded public summary | Resolve captured Head metadata | Read lifecycle/readiness summaries |
| `fork_sandbox` | Resolve public selector, allocate target | `CreateHeadIfAbsent` if same store | Activate isolated target Workspace/runtime separately |
| `rollback_sandbox` | Auth, resolve Checkpoint, capture expected Head | `ReplaceHead(Expected::Exact(...))`; conflict/no merge | Fence/reconcile live Workspace per product policy |
| `create_checkpoint` | Allocate ID/display metadata, capture selected binding | `CreateFixedRootIfAbsent`, payload `0/0/0` | None |
| inspect/list Checkpoints | Auth, pagination/result mapping | Read bounded Root metadata | None |
| `remove_checkpoint` | Auth, public outcome mapping | `RemoveFixedRoot(Expected::Exact(...))`; exact retirement later | None |
| `export_changes` | Destination policy and stream orchestration | Captured immutable read/custody | Bounded host-output and spool effects |

## 11. Errors, retries, and read-back

| Operation class | Important errors | Safe resolution |
|---|---|---|
| Create sandbox/fork | `limit_exceeded`, `not_ready`, provider failure, `outcome_unknown` | List/inspect using request correlation; never create another target blindly |
| Checkpoint creation | `conflict`, `limit_exceeded`, `outcome_unknown` | Inspect/list by allocated ID/request correlation |
| Rollback | `not_found`, `conflict`, `busy`, `outcome_unknown` | Inspect sandbox and Checkpoint; issue a new authorized request if desired |
| Remove/destroy | `busy`, lifecycle conflict, partial cleanup, `outcome_unknown` | Inspect/list exact non-reused ID; retry only unfinished idempotent cleanup |
| Export | invalid destination/format, I/O/ENOSPC, limit, cancellation | Prior selected Version is unchanged; inspect destination and operation result before retry |

LayerStack-0's complete semantic outcome set is `APPLIED`, `ALREADY_EXISTS`,
`NOT_FOUND`, `CONFLICT`, `INVALID_BINDING`, `CORRUPT`, `OUTCOME_UNKNOWN`, and
`INTERNAL_FAILURE`. The application may map these to stable public errors, but
must not collapse `OUTCOME_UNKNOWN` into failure or success. It first performs
authoritative exact-record read-back using the non-reused public identity and
its internal request correlation.

Auth and integrity errors must be redacted. A conflict may disclose the current
public `VersionId` only if `DEC-018` policy permits it; it never discloses the
internal expected/current Head revision.

## 12. Phase 04 acceptance checks

- [ ] All 13 proposed names have one catalog definition and matching CLI/MCP projections.
- [ ] `fork_sandbox` resolves `API-D09`; no cross-store copy is called zero-payload fork.
- [ ] `rollback_sandbox` accepts only explicit `checkpoint_id` as its Version target.
- [ ] `create_checkpoint` accepts no Workspace/session/Version/revision target.
- [ ] Public schemas contain no expected revision or AcceptedBinding.
- [ ] Checkpoint IDs are fixed, non-retargetable, bounded, and not reused.
- [ ] Fork/checkpoint/rollback-to-existing reference counters prove payload `0/0/0` where the architecture permits that claim.
- [ ] Stale Head operations make no change and perform no hidden recapture/merge/rebase.
- [ ] Export reads complete Versions and contains no parent/layer/depth/squash reconstruction.
- [ ] Public/internal squash operations are absent from the permanent V2 route graph.
- [ ] Destroy/remove close reference and read-custody races without direct public payload deletion.
- [ ] Limits, outcome-unknown read-back, redaction, and adapter parity are tested.

## 13. Source and design anchors

Measured e497 catalog declarations:

- `crates/sandbox-operations/catalog/src/manager/management.rs`
- `crates/sandbox-manager/src/management/service/impls/create_sandbox.rs`
- `crates/sandbox-manager/src/management/service/impls/destroy_sandbox.rs`
- `crates/sandbox-runtime/operation/src/layerstack/actions/squash.rs`
- `crates/sandbox-runtime/operation/src/layerstack/service/impls/export.rs`

Design contracts:

- [Shared API contract](README.md)
- [Runtime API](runtime.md)
- [Selected durable Version store](../design/03-state-store.md)
- [Reference EphCoW lifecycle algorithm](../algorithm/02-references-and-publication/01-reference-ephcow.md)
- [Strict OCC publication algorithm](../algorithm/02-references-and-publication/02-occ-publication.md)
- [Fork, Checkpoint, rollback, and CoW diagram](../diagrams/03-fork-checkpoint-rollback-and-cow.md)
- [Measured e497 surfaces](../phases/00-freeze-rules/inventory-surfaces.md)
