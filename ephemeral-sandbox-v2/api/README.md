# LayerStack-0 public API design

Date: **2026-08-04**  
Status: **DESIGN DRAFT — Phase 04 API input; not implementation evidence**

This folder defines the proposed public operation surface for Ephemeral
Sandbox V2. It translates the selected LayerStack-0 architecture into
manager, runtime, and observability operations without exposing storage
internals as product APIs.

The package is intentionally four files:

| File | Responsibility |
|---|---|
| [manager.md](manager.md) | Sandbox lifecycle, checkpoints, fork, rollback, discovery, and export |
| [runtime.md](runtime.md) | Commands, files, and writable Workspace sessions |
| [observability.md](observability.md) | Read-only fleet, runtime, and LayerStack-0 diagnostics |
| This file | Shared identifiers, projection rules, errors, concurrency boundary, and compatibility ledger |

The selected architecture remains authoritative. These API documents do not
change the storage owner, introduce another writer, select a chunk/CDC store,
or prove that V2 has been implemented.

## 1. Authority, evidence, and disposition

Read this package under the following authority order:

1. product [PRD and hard rules](../PRD.md#hard-rules-must-never-break);
2. selected [architecture design](../architecture_design.md);
3. accepted [LayerStack-0 terminology](../branding/terminology.md);
4. Phase 00 [measured public-surface inventory](../phases/00-freeze-rules/inventory-surfaces.md);
5. the family files in this folder.

If an API statement conflicts with a higher-authority source, the API
statement is invalid and must be corrected. Current e497 behavior is evidence
to migrate from, not V2 semantics.

Evidence, source metadata, correctness, disposition, and performance are
different fields:

| Category | Allowed values used by this package | Meaning |
|---|---|---|
| Evidence label | `SOURCE-VERIFIED`, `INFERRED`, `OPEN`, `OPEN_WITHIN_R0`, `OWNER_DEC_OPEN` | Provenance or unresolved-evidence class only |
| Source metadata | branch `codex/new-2.0-storage-core`, commit `e4974d1f9aac702b35e052629cb070c897989352`, clean seal | Identifies the measured product source; it is not an evidence label |
| Correctness result | `NOT_RUN` until implementation checks execute | Does not follow from source presence or design completeness |
| V2 disposition | retain, rewrite, add, or remove | Migration treatment, not evidence |
| Final performance verdict | `TARGET_UNSELECTED` | No owner-approved quantitative optimization target or qualified run exists |

Only the evidence labels defined by the program evidence taxonomy are used as
labels. “Owner-directed input,” “locked by R0,” and “proposed public” below are
decision provenance or document disposition, not new evidence labels.

## 2. Public API decisions

The following decisions shape all three families.

| ID | Decision | Status and consequence |
|---|---|---|
| `API-D01` | No public operation accepts `expected_revision`, `HeadRevision`, or another caller-selected OCC token. | Owner-directed input. The application captures the expected Head internally and LayerStack-0 still performs one strict conditional Head transition. Removing the public parameter does **not** remove OCC. |
| `API-D02` | `fork_sandbox` accepts `checkpoint_id` as its only optional Version-selection argument. | Owner-directed input. Omission means the source sandbox's currently selected accepted Version is captured once; a supplied checkpoint fixes the source binding. Raw `VersionId` is never accepted. |
| `API-D03` | `rollback_sandbox` targets an explicit `checkpoint_id`; no raw Version selector exists. | Owner-directed input. `checkpoint_id` is the only permitted rollback target selector and is required, because silently choosing “latest” would be race-prone and choosing the current Version would make rollback meaningless. |
| `API-D04` | `create_checkpoint` records the sandbox's currently selected accepted Version. | Owner-directed input. It does not accept `VersionId`, a Head token, or a Workspace target. |
| `API-D05` | `create_checkpoint` never accepts `workspace_session_id`. | Owner-directed input. To checkpoint live changes, publish the Workspace first, then create a Checkpoint from the newly selected accepted Version. |
| `API-D06` | `VersionId` may be returned for correlation and diagnostics but is not a public mutation selector or equality proof. | Locked by R0. Every candidate admission and occupied-ID comparison stays inside LayerStack-0. |
| `API-D07` | Root, Head, AcceptedBinding, admission, recovery, retirement, payload paths, and physical storage objects remain internal. | Locked by R0. Public users manipulate Sandboxes, Checkpoints, Workspaces, commands, and files. |
| `API-D08` | The operation catalog remains the semantic source; CLI and MCP are projections. | `SOURCE-VERIFIED` direction retained for V2. CLI flags use kebab case while catalog/MCP fields use snake case. |
| `API-D09` | A public fork may claim accepted-reference payload I/O `0/0/0` only when source and destination references remain inside one LayerStack-0 store instance. | Locked by R0. If `fork_sandbox` means provisioning an independent per-sandbox store/volume, the public name cannot inherit the hard-rule-3 reference claim without a proved same-store topology; Phase 04 must resolve this product mapping. |

These decisions do not silently close `DEC-001`, `DEC-011`, `DEC-017`, or
`DEC-018`.

## 3. Recommended operation catalog

The target projection has **32 names** when the recommended outcomes for the
two catalog-affecting open decisions are included: 13 manager, 11 runtime, and
8 observability operations. Because `file_blame` and promotion of `file_list`
remain owner decisions, 32 is a design target, not a frozen owner-approved
count.

| Family | Proposed names | Count |
|---|---|---:|
| Manager | `create_sandbox`, `destroy_sandbox`, `inspect_sandbox`, `list_sandboxes`, `fork_sandbox`, `rollback_sandbox`, `create_checkpoint`, `inspect_checkpoint`, `list_checkpoints`, `remove_checkpoint`, `list_docker_images`, `list_workspace_directories`, `export_changes` | 13 |
| Runtime | `exec_command`, `write_command_stdin`, `read_command_lines`, `file_read`, `file_list`, `file_write`, `file_edit`, `file_blame`, `create_workspace_session`, `publish_workspace_session`, `destroy_workspace_session` | 11 |
| Observability | `snapshot`, `trace`, `events`, `resources`, `daemon`, `topology`, `cgroup`, `layerstack` | 8 |

### Catalog delta from e497

| Change | Operations | Reason |
|---|---|---|
| Retain name and general role | Manager lifecycle/discovery operations; command operations; `file_read`; Workspace-session operations; seven general observability names | They remain valid product capabilities after their storage wording is updated. |
| Add | `fork_sandbox`, `rollback_sandbox`, `create_checkpoint`, `inspect_checkpoint`, `list_checkpoints`, `remove_checkpoint` | Product-level access to selected reference primitives. Evidence remains `OPEN`; fork mapping has the `API-D09` guard. |
| Promote, pending owner decision | `file_list` | e497 already implements it as daemon HTTP-only; `DEC-017` decides catalog/CLI/MCP promotion. |
| Retain only if owner accepts | `file_blame` | `DEC-001`; provenance remains an application-owned side channel, never Version identity. |
| Rewrite semantics/result | `publish_workspace_session`, `export_changes`, observability `snapshot`, and `layerstack` | Remove legacy auto-merge, layer-chain, squash, depth, and per-layer-truth assumptions. |
| Remove | public `squash_layerstacks` and internal `squash_layerstack` | Complete immutable Versions have no durable layer chain to squash. No replacement operation is created. |
| Rewrite or remove internal legacy transport | `export_layerstack`, `read_export_chunk` | Export may keep bounded transport helpers, but permanent helpers must read complete Versions and must not imply layer truth. |

## 4. Catalog, CLI, MCP, and HTTP projection

One operation has one semantic contract. Adapters may change presentation but
must not create different targeting, concurrency, or authorization semantics.

| Concern | Catalog / MCP | CLI | Rule |
|---|---|---|---|
| Operation name | snake case, for example `create_checkpoint` | same operation token | No aliases that change meaning |
| Ordinary argument | snake case, for example `checkpoint_id` | kebab-case flag, for example `--checkpoint-id` | Presentation only |
| Runtime sandbox scope | required `sandbox_id` in MCP request | global `sandbox-runtime-cli --sandbox-id ID` | Same required routing value |
| Manager/observability sandbox scope | ordinary field | per-operation `--sandbox-id` | Same semantic field |
| Command text | JSON string `cmd` | positional `COMMAND` | Same bytes after adapter decoding |
| Stdin text | JSON string `stdin` | positional `TEXT` | Same bytes after adapter decoding |
| File edits | native JSON array | JSON text supplied to `--edits` | Same validated ordered edit list |
| Errors | typed semantic code and structured details | structured output plus non-zero exit | No adapter may retry a stale mutation silently |

The catalog remains the operation ledger. CLI-schema tests and MCP-schema
tests must compare names, requiredness, defaults, bounds, and routing against
the same catalog definitions. HTTP-only exceptions must be explicit; the V2
goal is to eliminate the current accidental `file_list` transport split if
`DEC-017` selects promotion.

## 5. Shared public identifiers

All identifiers are opaque typed strings at the public boundary. Callers may
store and compare exact identifier strings but must not parse paths, hashes,
revisions, generations, or topology from them.

| Identifier | Public role | May select mutation target? | Reuse rule |
|---|---|---|---|
| `sandbox_id` | Routes lifecycle, runtime, and diagnostics to one product sandbox/Branch context | Yes, for the named sandbox operation | Must not be reused while stale handles could alias a new sandbox incarnation |
| `checkpoint_id` | Names one immutable fixed Checkpoint Root | Yes, only where the operation explicitly accepts a Checkpoint | Stable and non-retargetable; a removed ID must not later name another Checkpoint |
| `workspace_session_id` | Routes to one live mutable Workspace session | Yes, for live runtime operations only | Runtime-scoped; never a portable Version fact |
| `command_session_id` | Routes stdin/output to one running or retained command | Yes, for command interaction only | Runtime-scoped and bounded |
| `VersionId` | Correlation/result identity of canonical complete Version bytes | **No** public mutation selector | Typed/versioned; not equality or durable-existence proof |
| `request_id` | Correlates application, audit, and diagnostic records | No | Unique enough for the configured observation window; not selected truth |
| `cursor` | Opaque bounded-list continuation token | No | Scoped to operation/filter contract; malformed/stale cursors fail explicitly |

The public API never accepts `AcceptedBinding`, `RootId`, `HeadRevision`, a
digest, an on-disk payload path, a store generation, or a legacy layer ID.

## 6. Target model

The same file operation name can target either the selected immutable Version
or a live Workspace, but that choice is always explicit and finite:

```text
                         sandbox_id
                             |
          +------------------+------------------+
          |                                     |
          | no workspace_session_id             | workspace_session_id
          v                                     v
 captured selected accepted Version      live isolated Workspace
 read-only file_read/file_list            read/write/edit/exec

 create_checkpoint never enters the right-hand path.
 publish_workspace_session first admits a complete Candidate and then
 conditionally moves the internally captured Head.
```

Checkpoint selectors are deliberately narrow:

- `fork_sandbox`: optional `checkpoint_id`; omission captures the current
  selected accepted Version;
- `rollback_sandbox`: explicit `checkpoint_id` required;
- `create_checkpoint`: no target selector; captures the current selected
  accepted Version; and
- file and command operations: no Checkpoint or raw Version selector.

## 7. Public concurrency boundary

Public simplicity does not weaken storage correctness. The caller does not
send a revision. The existing application owner captures it exactly once and
the store compares it at the sole linearization point.

```text
public caller       application / operation service       LayerStack-0
     |                            |                              |
     | rollback(checkpoint C)     |                              |
     |--------------------------->| authorize + resolve C        |
     |                            | capture current Head (V7,r9) |
     |                            |----------------------------->|
     |                            | move(C.binding, expect V7,r9)|
     |                            |----------------------------->|
     |                            |                     one gate:|
     |                            |                 reread/compare|
     |                            |                 replace or stale
     |                            |<-----------------------------|
     | success or conflict       |                              |
     |<---------------------------|                              |

No public revision field. No silent expected-Head recapture. No merge/rebase.
```

Rules:

1. Authorization and `DEC-018` race policy remain application-owned.
2. The application captures one expected `(AcceptedBinding, HeadRevision)` for
   a state-changing request or uses the Workspace session's already captured
   base record.
3. LayerStack-0 rereads the complete current Head under its one transition
   authority and conditionally replaces it once.
4. Stale returns `conflict`; the application does not recapture and retry
   inside the same request.
5. A client may explicitly inspect and issue a new request. That is a new
   authorization/order decision, not a hidden storage retry.
6. A completed admission followed by stale OCC may leave one complete
   unreferenced Accepted Version as bounded retirement debt; it never creates a
   dangling Head.

## 8. Common semantic response envelope

The exact transport wrapper remains `OPEN_WITHIN_R0`; each adapter must convey
the following semantic information without loss:

```text
success:
  operation        exact catalog operation name
  request_id       correlation identifier
  result           operation-specific bounded value
  warnings[]       optional non-fatal, non-authoritative notices

failure:
  operation        exact catalog operation name
  request_id       correlation identifier
  error.code       stable machine-readable class
  error.message    bounded redacted explanation
  error.details    typed bounded fields allowed by disclosure policy
  retryable        explicit transport/application guidance
```

`VersionId` may appear in a successful checkpoint, publish, inspect, or
diagnostic result. Its presence means “this accepted result correlates to this
typed Version identity,” not “the digest alone was trusted.” Internal bindings,
revisions, paths, filesystem errors containing host paths, auth internals, and
collision comparison bytes are redacted.

### Common error classes

| Code | Meaning | Retry guidance |
|---|---|---|
| `invalid_argument` | Type, range, path, edit, enum, or identifier validation failed | Correct request; do not retry unchanged |
| `unauthenticated` / `forbidden` | Identity missing or policy denied | Re-authenticate or change authority; `DEC-018` refines race ordering |
| `not_found` | Sandbox, Checkpoint, Workspace, command, or path does not exist in the authorized scope | Re-inspect; do not guess another target |
| `conflict` | Strict OCC lost, fixed Checkpoint ID conflicts, or target lifecycle conflicts | No automatic retry; issue a new request after explicit inspection |
| `collision` | Occupied `VersionId` had unequal canonical bytes | Fail closed; operator/integrity path, never retry as alias |
| `integrity_failed` | Corrupt, dangling, unknown-format, or unverifiable durable record | Fail/readiness closed; operator action required |
| `limit_exceeded` | Finite bytes, entries, roots, sessions, FDs, workers, debt, or response bound reached | Reduce scope or wait for bounded cleanup |
| `busy` | Lifecycle/session command activity prevents the requested transition | Retry only after the reported activity ends |
| `not_ready` | Store/runtime is recovering, fenced, unsupported, or unavailable | Retry only when readiness changes |
| `unsupported` | Requested format/profile/behavior is not selected or supported | Change request/configuration |
| `outcome_unknown` | Failure occurred at an acknowledgement boundary and the server cannot safely assert prior versus new result | Resolve through inspect/list/read-back; never repeat a mutation blindly |
| `internal` | Bounded redacted unexpected failure | Follow server retry guidance and preserve request correlation |

Transport timeout is not proof that a mutation did not linearize. Each
mutation section states the safe read-back operation.

## 9. Bounds, pagination, and resource rules

- Every string, path, array, content body, response, timeout, list population,
  session, worker, descriptor, and recovery population has a configured finite
  bound.
- Defaults and maxima already fixed by e497 are preserved in the family files
  unless a later phase deliberately versions the contract.
- Lists with potentially growing populations use `limit` and opaque `cursor`;
  the cursor is not a file path, offset into mutable storage, or authorization
  capability.
- `file_read` and command output use their existing bounded window forms.
- A limit error cannot bypass validation, mutate an Accepted Version, weaken
  durability, or convert a stale operation into success.
- Metric labels never contain unbounded raw paths, command strings, tenant
  labels, `VersionId`s, or Checkpoint IDs.

## 10. Public versus internal API

The public API is intentionally smaller than LayerStack-0's internal semantic
surface.

| Internal responsibility | Why it stays private |
|---|---|
| Candidate validation, canonicalization, and `VersionId` derivation | Phase 02 pure identity; callers must not choose codec/hash grammar or bypass validation |
| Candidate admission and occupied-ID full comparison | Only LayerStack-0 can issue/revalidate an AcceptedBinding and prove one physical payload |
| Head capture, `HeadRevision`, and conditional replacement | Prevents callers bypassing or weakening the sole OCC point |
| Root/Head record CRUD | Public fixed Checkpoints and sandbox workflows impose authorization, type, and lifecycle policy |
| Read custody and payload materialization | Runtime-effect and store safety mechanism, not portable public identity |
| Recovery, readiness, generation fencing, retirement, and cleanup | Store/lifecycle authority; public mutation would create a second control plane |
| Physical payload paths, complete-Version layout, or future backend objects | Phase 03 internal detail; public paths would freeze a backend and allow authority bypass |
| CDC, Chunks, manifests, object DAGs, or reflink/FUSE controls | Not selected by current R0 and never required public semantics; CAS+CDC would reopen Phase 01 |
| Rollout/MCTS score and winner policy | Application-owned by hard rule 7 |

There is no public “repair,” “force,” “skip collision check,” “disable OCC,”
“write Head,” “delete payload,” “run recovery,” or “run retirement now” command.

## 11. Open product-owner decisions

| Decision | API effect | Stable architecture seam | Blocks this design package? |
|---|---|---|---|
| `DEC-001` — exact `file_blame` | Keep the operation with rewritten Version/publication correlation or remove it as a breaking change | Provenance remains an application-owned side channel and never enters canonical Version identity | Blocks final runtime catalog count and schema, not LayerStack-0 architecture |
| `DEC-011` — observation window | May affect compatibility diagnostics and removal timing after cutover | Cannot authorize dual writes or permanent legacy compatibility | Does not block ordinary API shape |
| `DEC-017` — `file_list`, sessionless write/edit, exact file targets | Determines promotion of `file_list` and whether no-session mutations reject or use an application-composed Candidate/publish path | Accepted Versions remain immutable; all publication uses the same internal OCC path | Blocks final runtime mutation/transport contract |
| `DEC-018` — auth/revoke race ordering | Determines authorization cutoff, response disclosure, and audit event order | Application owns auth; store OCC remains mandatory and independent | Blocks security acceptance tests, not parameter lists |

Until the owner closes a row, implementations must preserve all allowed
outcomes behind the stated seam and must not choose by accident.

## 12. Phase 04 implementation checklist

- [ ] Re-seal implementation branch, HEAD, and dirty state before modifying the catalog.
- [ ] Define every public operation once in the catalog and project it to CLI/MCP consistently.
- [ ] Confirm no public schema contains `expected_revision`, `HeadRevision`, `AcceptedBinding`, raw Root/Head fields, or mutation-target `VersionId`.
- [ ] Resolve `API-D09` before claiming `fork_sandbox` is a zero-payload operation.
- [ ] Keep `create_checkpoint` free of `workspace_session_id`; verify publish-then-checkpoint composition.
- [ ] Remove public/internal squash routes from the permanent V2 path.
- [ ] Prove stale publication/rollback never auto-recaptures, merges, or rebases.
- [ ] Apply the four open owner decisions explicitly and record the selected catalog count.
- [ ] Keep observability read-only with respect to selected-Version authority.
- [ ] Run catalog/CLI/MCP parity, authorization, bounds, conflict, redaction, and compatibility tests.

## 13. Related design contracts

- [Architecture decision](../architecture_design.md)
- [Ownership and boundaries](../design/01-ownership-and-boundaries.md)
- [Version identity](../design/02-state-identity.md)
- [Durable Version storage](../design/03-state-store.md)
- [Algorithms and call flows](../design/04-algorithms-and-call-flows.md)
- [Reference EphCoW](../algorithm/02-references-and-publication/01-reference-ephcow.md)
- [OCC publication](../algorithm/02-references-and-publication/02-occ-publication.md)
- [Branches, Checkpoints, fork, and rollback](../diagrams/03-fork-checkpoint-rollback-and-cow.md)
- [Read custody and runtime handoff](../algorithm/03-runtime-access-and-materialization/01-read-custody-and-runtime-handoff.md)
- [Durability and recovery](../algorithm/04-durability-and-lifecycle/01-durability-and-recovery.md)

## 14. API operation-to-algorithm navigation

| API operation class | Selected algorithm contract |
|---|---|
| Candidate-bearing publication (`publish_workspace_session`, automatic command/file publication) | [Composed publication pipeline](../algorithm/02-references-and-publication/03-composed-publication-pipeline.md) and [strict OCC publication](../algorithm/02-references-and-publication/02-occ-publication.md) |
| Head/Root lifecycle (`fork_sandbox`, rollback, Checkpoint create/remove, destroy) | [Reference EphCoW](../algorithm/02-references-and-publication/01-reference-ephcow.md) |
| Committed reads and export capture | [Read custody and runtime handoff](../algorithm/03-runtime-access-and-materialization/01-read-custody-and-runtime-handoff.md) |
| Runtime activation/materialization | [Runtime materialization](../algorithm/03-runtime-access-and-materialization/02-runtime-materialization.md) |
| Recovery/retirement diagnostics | [Durability and recovery](../algorithm/04-durability-and-lifecycle/01-durability-and-recovery.md) and [retirement](../algorithm/04-durability-and-lifecycle/02-retirement-and-cleanup.md) |

The family files provide caller mapping; the algorithms remain authoritative
for storage semantics. No API operation directly mutates a record, traverses
payload for a reference-only operation, or treats raw `VersionId` as authority.
- [Terminology](../branding/terminology.md)
- [Measured e497 surface inventory](../phases/00-freeze-rules/inventory-surfaces.md)
