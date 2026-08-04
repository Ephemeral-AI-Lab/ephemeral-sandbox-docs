# API methods

> Status: **Accepted**

This is the sole authority for the public domain surface: exactly **18
lifecycle methods** and **8 runtime methods**. Signatures use direct typed IDs.
There is no generic `ref`, `target`, backend selector, archive format
selector or public catalog/locator term. Authentication, pagination framing,
request operation IDs and byte-stream transport stay outside the signatures.

## Types and version semantics

| Type | Meaning |
|---|---|
| `sandbox_id` | One live sandbox. |
| `workspace_session_id` | One session, permanently scoped to one sandbox. |
| `checkpoint_id` | One immutable checkpoint, owned by one sandbox. |
| `command_session_id` | One running command. |
| `portable_archive` | The one versioned backend-neutral complete-state stream. |
| `StateId` | Content identity defined only by [Canonical State](components/canonical_state.md#state-and-object-model): `ObjectId(FilesystemRoot)`. |
| `ForkOrigin` | Internal immutable immediate provenance `{parent_id, checkpoint_id}`; it is exposed only through `get_sandbox_parent`. |

IDs are opaque and non-interchangeable. A `portable_archive` is a stream, not
an ID. OCI conversion is a Docker-adapter edge around that one stream.

Every sandbox also has an internal `HeadRevision`. It is not part of
`StateId` and is not a public method parameter. It starts at zero and
prevents ABA:

- every `Published` decision increments it, including publication of
  content-identical `StateId`;
- an actual rollback and a `Committed` fork commit increment it;
- `AlreadyCurrent`, `NoChanges`, `ParentDiverged` and other no-head-change
  outcomes do not increment it.

## Lifecycle methods

### Sandboxes — 5

| # | Method | Result | Contract |
|---:|---|---|---|
| 1 | `create_sandbox(portable_archive?)` | `sandbox_id` | Create the canonical empty state or verify/import one complete archive; expose nothing until objects and the typed catalog effect are durable. |
| 2 | `get_sandbox(sandbox_id)` | `sandbox` | Read current sandbox metadata from one selected root. |
| 3 | `list_sandboxes()` | `sandbox[]` | List accessible live sandboxes through bounded transport pagination. |
| 4 | `destroy_sandbox(sandbox_id)` | `Destroyed` | Logically remove one quiescent sandbox without cascading to children or owned checkpoints. |
| 5 | `export_sandbox(sandbox_id)` | `portable_archive` | Capture and stream one complete committed `StateId`; session changes are excluded. |

Export takes one bounded read slot after capturing the head and does not block
later publication. A destroyed sandbox’s checkpoints and child provenance
remain directly addressable as specified below.

### Workspace sessions — 5

| # | Method | Result | Contract |
|---:|---|---|---|
| 6 | `create_workspace_session(sandbox_id)` | `workspace_session_id` | Register a mutable session from the exact origin pair `(StateId, HeadRevision)`, snapshot the authenticated principal internally, reserve resources and activate one isolated private workspace. |
| 7 | `get_workspace_session(workspace_session_id)` | `workspace_session` | Read its durable mutable or terminal metadata. |
| 8 | `list_workspace_sessions(sandbox_id)` | `workspace_session[]` | List that sandbox’s sessions through bounded transport pagination. |
| 9 | `publish_workspace_session(workspace_session_id)` | `Published \| AlreadyPublished \| PublishConflict` | Fence and capture one workspace; publish one complete candidate only if the current head still equals its exact origin pair. |
| 10 | `destroy_workspace_session(workspace_session_id)` | `Destroyed \| AlreadyClosed` | Durably claim one foreground `OwnerSlot[1..15]/AdapterClose`, then dispose and delete Mutable/`ACTIVE` or Terminal/`CONFLICTED` as `Destroyed`; idempotently dispose and delete Terminal/`PUBLISHED` as `AlreadyClosed`. Row deletion, exact receipt and close-intent clear are one commit. |

Multiple sessions from the same head are supported. Publication never creates
a layer, rebases, merges or retries against a newer head. During capture the
durable row stays Mutable/`ACTIVE`; a transient operation owner and adapter
fence prevent concurrent session work. There is no durable `PUBLISHING`
state. The accepted create request stores its authenticated principal once as
an immutable internal `ActorId[32]`. Capture, changed-metadata ownership and
C3 attribution always use that session-bound value; a publish or retry never
uses the ambient caller. Either Terminal transition drops the actor together
with the origin and reservation. This adds no public parameter, result or
method.

At final commit:

- Store checks the origin before opening the Build-owned sorted selection
  cursor. A mismatch therefore performs bounded row/receipt work, scans none
  of the candidate objects, selects no candidate locator, leaves the head
  unchanged, moves the session to Terminal/`CONFLICTED`, records
  the exact `PublishConflict` receipt, and retains the exact Build nonce for
  synchronous abort;
- on an exact match, Store first revalidates the complete Build-owned disk
  cursor `(ObjectId, REUSE | candidate locator)` against the current Catalog.
  A `REUSE` entry must retain a structurally valid current same-ID row. A
  candidate entry also retains a structurally valid current same-ID row when
  present and otherwise uses its staged locator; an existing Full is therefore
  never replaced by a staged Delta. A newly selected staged Delta must resolve
  its `base_id` to a structurally valid current Full. This gate trusts the
  selected Catalog's structural and locator invariants and performs no payload
  I/O;
- only after the complete revalidation succeeds, Store makes the selection
  pass. Candidate frames are globally ObjectId-ordered, so each pack occupies
  one contiguous cursor interval and needs only one scalar `selected_count`.
  Store installs and synchronizes a candidate pack iff that count is nonzero,
  deletes and directory-synchronizes a zero-selected late-dedup pack, and
  leaves dead frames in a selected mixed pack for ordinary exact maintenance.
  It then deletes/synchronizes the cursor and all non-pack scratch while the
  exact Build nonce remains selected. The same selecting HEAD advances the
  head, increments `HeadRevision` even when `StateId` is unchanged, moves the
  session to Terminal/`PUBLISHED`, records the exact `Published` receipt,
  selects the chosen locators and clears that nonce atomically.

The internal physical `HEAD` mentioned here is exactly
`{type_tag, StoreSequence, ArenaId, committed_arena_length, checksum}`. It
serializes no Catalog-root offset or page identifier. Store requires the
selected committed length to be 16-KiB aligned and at least 16 KiB, derives
`CatalogRoot` only as
`(ArenaId, committed_arena_length - 16 KiB)`, and emits one fresh root as the
last page of every selected S1 commit. A sparse candidate writer starts exactly
at the selected committed length with positional writes; it never discovers
that cursor from file size or append mode, and no selected padding or trailer
follows the fresh root.

No candidate pack is installed before the entire current-root revalidation
succeeds. On the first missing, structurally invalid, or incompatible `REUSE`
row or required Full base, Store leaves the final gate, closes the cursor, and
deletes plus directory-synchronizes the whole cursor, every staged pack, and
every scratch artifact under the same selected Build. The private workspace
remains stably fenced while one complete two-pass recapture runs under that
same Build nonce. A second invalidation performs the same complete cleanup,
exact-aborts the Build, and returns typed transport outcome `RetryLater`; it
never patches one `REUSE` entry to Full, locally rewrites one Delta, or loops.

`Session/Terminal` stores only `{status, allocation}`. `PUBLISHED` derives the
publication outcome `Published`; `CONFLICTED` derives `PublishConflict`. It
has no duplicate result field. A later semantic call on `PUBLISHED` returns
`AlreadyPublished`; replay of the accepted publication returns the exact
original `Published` or `PublishConflict` response from its retained
`Receipt`.

Let `K=|U_candidate|<=N_object_max`, `K_delta<=K`, and Catalog height `H<=8`.
One exact-origin attempt costs
`Theta(KH + K_delta + selected-candidate-pack install/sync work)`; the two
streaming cursor passes change only its constant factor and retain O(1)
per-segment selection memory. Preparation runs at most twice: the initial
two-pass capture plus one whole recapture after the first invalidation. An
origin conflict has no `K`-proportional scan. The admitted maximum and tail
latency must pass the parallel-session qualification profile.

Cleanup is ordered and synchronous. After `Published`, charge transfers to
selected storage, the Build permit is released, and the private allocation is
idempotently disposed and synchronized before normal acknowledgement. After
`PublishConflict`, the operation owner fences/joins the producer, deletes
every fixed-directory file and synchronizes the directory while the exact
Build remains selected, exact-CAS-clears the nonce in a final S2 commit,
releases the charge/permit, and only then acknowledges; the private allocation
remains fenced and read-only. A pre-decision failure uses the same
join/delete/directory-sync/exact-clear/release order, leaves the session
`ACTIVE`, and records any required accepted failure receipt with the clear.

A live pre-HEAD failure that may have installed a pack first runs the exact
installed-pack census against the current selected Catalog, unlinks every
zero-selected installed orphan, and synchronizes `packs/` before it deletes
the fixed staging directory, clears the Build, or releases its charge. Restart
recovery reconstructs every selected Build and charge, keeps all of them
selected while
it performs the exact installed-pack census, and unlinks plus synchronizes
every zero-selected orphan. Only after that census and orphan cleanup may it
empty Build staging, exact-clear the corresponding Build rows, and release
their charges. Recovery never clears a Build before the census that proves
which installed packs are unselected.

A conflicted allocation stays fenced and readable until explicit destruction.
It accepts no command or mutation. V1 admits only an adapter profile that
proves the retained private allocation is self-contained and remains readable
without canonical origin objects; Terminal rows are never semantic roots. An
adapter that cannot prove this profile is unsupported.
`AlreadyPublished` applies to a later semantic call on an already published
session; replay of the original retained operation ID returns its exact
`Published` receipt.

Destroying a session first uses one S2 commit to condition on the exact row and
claim one of the foreground `OwnerSlot[1..15]` lanes as the typed
`AdapterClose` intent
`{session_id, expected_row_digest, request_identity}`. The allocation is
derived only from that exact selected session row, not duplicated in the
intent. The owner then fences and drains work, synchronously disposes and
syncs the allocation, and uses one final S2 commit to delete that exact Mutable
or Terminal row, store the exact destroy receipt and clear the intent.
Recovery fences and idempotently completes any selected close intent. The row
remains selected until the final commit; an unused intent may be cleared only
before irreversible disposal. This is one of the same 15 foreground lanes,
not another namespace or public state. There is no `CLOSED` row
or deletion tombstone. After both the row and retained receipt expire, a fresh
call can only observe `WorkspaceSessionNotFound`.

### Checkpoints and rollback — 5

| # | Method | Result | Contract |
|---:|---|---|---|
| 11 | `create_checkpoint(sandbox_id)` | `checkpoint_id` | Record the sandbox’s complete committed `StateId`; session changes are excluded and sessions may coexist. |
| 12 | `get_checkpoint(checkpoint_id)` | `checkpoint` | Read immutable checkpoint metadata. |
| 13 | `list_sandbox_checkpoints(sandbox_id)` | `checkpoint[]` | List checkpoints owned by that sandbox through bounded transport pagination. |
| 14 | `remove_checkpoint(checkpoint_id)` | `Removed` | Remove an unbound checkpoint; payload is reclaimed only when no semantic or temporary root reaches it. |
| 15 | `rollback_sandbox(sandbox_id, checkpoint_id)` | `RolledBack \| AlreadyCurrent` | Quiescently point the sandbox at its own checkpoint; create no history. |

Checkpoint creation is payload-copy-free but may retain unique bytes. Removal
returns `CheckpointInUse` when a live child’s derived pin exists. An actual
rollback increments `HeadRevision`; `AlreadyCurrent` does not.

### Forks — 3

| # | Method | Result | Contract |
|---:|---|---|---|
| 16 | `fork_sandbox(source_sandbox_id, checkpoint_id?)` | `{ sandbox_id, checkpoint_id }` | From one quiescent source checkpoint, create a detached child at `HeadRevision=0`; when omitted, checkpoint creation, child creation and derived pin are one commit. |
| 17 | `get_sandbox_parent(sandbox_id)` | `{ parent_id, checkpoint_id } \| null` | Return immutable immediate-parent provenance; roots return `null`, and provenance survives parent destruction. |
| 18 | `commit_fork(sandbox_id, checkpoint_id)` | `Committed \| AlreadyCurrent \| NoChanges \| ParentDiverged` | With parent and child quiescent, conditionally point the immediate parent at an explicit checkpoint owned by the child. |

An explicit fork checkpoint must belong to the source. Parent and child remain
operationally independent; forks can nest, and parent mutation is allowed.
Destroy never cascades. Destroying a child removes only the derived
`CheckpointPin`; it never silently deletes the named origin checkpoint.

#### Ordered fork-commit decision

Let `B` be the child’s immutable origin-checkpoint state, `C` the explicit
child-checkpoint state and `P` the immediate parent’s current state. Evaluate
the rows in exactly this order:

| Order | Condition | Result |
|---:|---|---|
| 1 | `P = C` | `AlreadyCurrent` |
| 2 | `C = B` | `NoChanges` |
| 3 | `P = B` | Set parent to `C`, increment its `HeadRevision`, return `Committed` |
| 4 | Otherwise | `ParentDiverged` |

Equality is `StateId` equality. Fork commit never creates a checkpoint,
merges, rebases, deletes a sandbox or changes the child’s origin binding or
pin.

## Runtime methods — 8

Committed views are read-only. Execution and mutation require a mutable active
workspace; its session ID already identifies the sandbox. A conflicted session
permits only metadata inspection, file reads and destruction.

| # | Method | Result | Contract |
|---:|---|---|---|
| 1 | `exec_command(workspace_session_id, command)` | `command_session_id` | Start a command in an active writable session. |
| 2 | `write_command_stdin(command_session_id, input)` | — | Send bounded input to a running command. |
| 3 | `read_command_lines(command_session_id, cursor?)` | `command_lines` | Read bounded command output. |
| 4 | `file_read(sandbox_id, path)` | `file` | Read committed content from one complete state. |
| 5 | `workspace_file_read(workspace_session_id, path)` | `file` | Read an active or conflicted private workspace. |
| 6 | `workspace_file_write(workspace_session_id, path, content)` | — | Stream a file write into an active session. |
| 7 | `workspace_file_edit(workspace_session_id, path, edits)` | — | Apply validated edits to an active session. |
| 8 | `file_blame(sandbox_id, path)` | `attribution` | Read canonical committed attribution. |

The exact adapter mapping is in
[Backend Adapters](components/backend_adapters.md#runtime-method-trace).

## Quiescence and publication ownership

`Session/Mutable` prefix absence is the only durable quiescence proof.
`OPENING` and `ACTIVE` rows block. A session under transient publication
remains `ACTIVE`, so it also blocks; Terminal/`PUBLISHED` and
Terminal/`CONFLICTED` rows do not.

| Operation | Sandboxes that must be quiescent |
|---|---|
| `fork_sandbox` | Source |
| `rollback_sandbox` | Target |
| `destroy_sandbox` | Target |
| `commit_fork` | Child and immediate parent |

The same per-sandbox gate serializes mutable-session registration with the
prefix check. Fork commit acquires gates in ascending `sandbox_id` order.
Failure releases every gate and returns `WorkspaceSessionsActive`; it never
waits or partially changes durable state. See
[Lifecycle](components/lifecycle_engine.md#quiescence-and-gates).

## Exact replay horizon

Authenticated lane, sequence, operation ID and request digest are transport
metadata, not new method parameters. The existing `Receipt` Catalog namespace
has exactly two closed key subtypes; this does not create a ninth namespace:

```text
ReceiptControl(lane) -> next_sequence:u64                 # 16 rows, initially 0
ReceiptSlot(lane, sequence mod 64)
  -> {request_digest[32], bounded_exact_result}           # 1,024 rows
```

The complete canonical framed `ReceiptSlot` value—including the 32-byte
request digest and exact result—is at most 512 bytes. For control value `next`,
the retained sequence range is `[max(0,next-64), next)`. A retry in that range
performs one modulo-slot lookup, verifies `request_digest`, and returns the
original exact result without reevaluating current state. An older sequence
returns transport outcome `ReplayExpired` and **never executes**; a sequence
greater than `next` is a typed transport gap rejection. A new request is
accepted only at sequence `next`, and its one S2 commit atomically writes the
semantic effect if any, the replacement modulo slot, and
`ReceiptControl.next_sequence=next+1`. Receipt slots store no sequence,
generation, low-water mark, or duplicate lane field.

Every post-acceptance semantic outcome—including no-effect errors such as
`CheckpointInUse`—uses that same effect-plus-receipt or receipt-only rule.
Preaccept authentication, malformed-request and admission failures may remain
unstored. All retained rows are disk-resident and cache-off; only the one
bounded control/slot replay working set may be resident. The durable profile
and commit coupling are defined by
[Lifecycle](components/lifecycle_engine.md#exact-bounded-receipts) and
[Durable Store](components/durable_store.md#s2-single-head-commit-and-recovery).

## Typed domain errors

| Error | Meaning |
|---|---|
| `SandboxNotFound(sandbox_id)` | Sandbox is absent or destroyed. |
| `WorkspaceSessionNotFound(workspace_session_id)` | Session is absent. |
| `WorkspaceSessionNotActive(workspace_session_id)` | Mutation/publication targeted a non-active session. |
| `WorkspaceSessionNotReadable(workspace_session_id)` | Session is neither active nor conflicted. |
| `WorkspaceSessionBusy(workspace_session_id)` | A transient publish or close owner holds the session. |
| `CheckpointNotFound(checkpoint_id)` | Checkpoint is absent or removed. |
| `CheckpointNotOwnedBySandbox(checkpoint_id, sandbox_id)` | Rollback used another sandbox’s checkpoint. |
| `CheckpointNotOwnedBySource(checkpoint_id, source_sandbox_id)` | Fork used another sandbox’s checkpoint. |
| `CheckpointNotOwnedByChild(checkpoint_id, sandbox_id)` | Fork commit used a checkpoint not owned by the child. |
| `CheckpointInUse(checkpoint_id)` | A derived live-child pin exists. |
| `NotAFork(sandbox_id)` | Fork commit targeted a root sandbox. |
| `ParentMissing(parent_id)` | Recorded parent was destroyed or unavailable. |
| `WorkspaceSessionsActive(sandbox_ids)` | A required sandbox has a Mutable session row. |
| `InvalidPortableArchive(reason)` | Archive framing, version, identity or content is invalid. |
| `InvalidPath(path)` | Path is invalid, escapes the root or names an unsupported target. |
| `IntegrityFailure(object_id)` | Durable bytes do not match typed identity. |
| `CorruptState(object_id)` | Selected state is missing, unsupported or ambiguous. |
| `ResourceLimitExceeded(resource)` | A hard limit prevents admission; `resource=storage_retention` covers the irreducible live floor. |
| `WorkspaceActivationFailed(workspace_session_id)` | Adapter could not create a verified private workspace. |
| `WorkspaceCaptureFailed(workspace_session_id)` | Adapter could not fence and capture exact stable facts. |
| `DurabilityFailure(operation)` | Required data could not become durable; no public head changed. |

`PublishConflict` and `ParentDiverged` are expected conditional outcomes.
`RetryLater` is a bounded admission/transport outcome outside these domain
result signatures. It may delay a public final commit while the Durable Store
runs one bounded maintenance pass; it does not invent a hidden lifecycle
result. If an operation was already accepted far enough to require replay, the
same receipt-only or effect-plus-receipt S2 rule still applies. See
[System requirements](system_requirements.md#typed-overload). Error details
are bounded.

The 16 durable custody lanes are static:

```text
OwnerSlot[0]     = Empty | Build{owner_nonce}                 # Maintenance only
OwnerSlot[1..15] = Empty | Build{owner_nonce} | AdapterClose  # foreground only
```

`Build` contains only `owner_nonce`; its lane supplies its meaning, so there is
no purpose field. Selecting `Build` in slot 0 is the sole global maintenance
fence and makes every non-maintenance S2 mutation return bounded `RetryLater`
until that exact nonce clears. Foreground work never borrows slot 0 or its
non-borrowable maintenance byte/inode reserve and quota; maintenance never
borrows slots 1 through 15. A foreground claimant selects one Empty foreground
lane or returns `RetryLater`; therefore the 16th simultaneous foreground
operation is bounded rather than admitted. A maintenance claimant likewise
returns `RetryLater` when slot 0 is not Empty. This adds no queue choreography,
dynamic lane assignment, field, namespace, or public API state.

## Deliberate exclusions

There is no `create_rollout`, workspace-session fork, checkpoint export, fork
removal/rebase, freeze/unfreeze, general merge, sandbox history or ancestor-list
method. Rollback and fork commit create no public history record. Physical
Full/Delta locators, Catalog arenas, `HEAD` and GC/repack remain internal.
The separate Lifecycle-facing Store port is also closed at exactly
`open_read`, `stage_objects`, and `commit`; these are internal capabilities,
not additions to the 18 lifecycle or 8 runtime methods above.
