# Phase 1 — Read-only architecture review

> Owner: lead reviewer  
> Prerequisite: none  
> Design-document writes: forbidden; this phase's Handoff record is writable  
> Output: Architecture Review Packet

## Objective

Reconstruct the smallest storage architecture that satisfies the locked
requirements and API. Do not assume the current five-component decomposition,
27 mechanism names, or CoW B+ proposal is correct.

## Required inputs

- [Refinement index](index.md)
- ../system_requirements.md
- ../api_methods.md
- ../index.md
- all architecture and component documents
- goal-objective.md identified in the refinement index
- proof-of-concept code only where it supplies evidence

Record the initial Git status. Do not overwrite unrelated work.

## Review work

### 1. Reconstruct invariants

Build a trace from every hard requirement and API method to:

- durable facts;
- owning authority;
- linearization point;
- quiescence rule;
- crash result;
- replay result;
- bounded resources.

Flag competing definitions of identity, ownership or state.

### 2. Run the architecture tournament

Compare at least:

1. simplified current design;
2. clean-slate minimum design;
3. algorithm and data-structure redesign;
4. portability and failure-model design.

Each candidate must show:

- component and authority graph;
- durable and transient structures;
- publication sequence;
- state machine;
- barriers and roundtrips;
- memory, FD and disk bounds;
- crash outcomes;
- backend boundary;
- parts removed from the current proposal.

Reject a candidate immediately if it violates a hard gate.

### 3. Run the physical-index tournament

Compare:

- adaptive immutable CoW B+;
- append-only sorted tables;
- immutable SSTables or bounded LSM-like designs;
- persistent radix or hash structures;
- extendible hashing;
- packed flat indexes;
- static FST-like indexes.

Do not select or wrap a database. Any winning index must be a fixed-purpose
immutable file format with typed operations.

### 4. Minimize component boundaries

For every proposed component, state:

- its one responsibility;
- durable facts it owns;
- inbound and outbound interfaces;
- deletion verdict;
- merge verdict;
- independent replacement proof;
- invariant lost if removed.

The graph must be acyclic. Every durable fact has one owner.

### 5. Reclassify mechanisms

Map every current name to:

- Keep;
- Merge;
- Replace;
- Reclassify;
- Remove.

Then classify each retained item using the categories in index.md. Ordinary
workflows, syscalls and library operations do not count as custom algorithms.

### 6. Identify research questions

List only questions whose answers can change a design decision. Each question
must identify:

- candidate affected;
- hard gate or optimization target;
- evidence needed;
- decision that the evidence will select.

## Required decision matrix

At minimum compare:

| Criterion | Current | Simplified | Clean-slate | Selected candidate |
|---|---|---|---|---|
| Components and authorities | | | | |
| Durable structures | | | | |
| Publication barriers | | | | |
| Payload copies | | | | |
| Metadata scans | | | | |
| Sparse update cost | | | | |
| Dense rebuild cost | | | | |
| Peak application memory | | | | |
| Peak disk and inodes | | | | |
| Crash states | | | | |
| Recovery complexity | | | | |
| Backend coupling | | | | |
| Dependency risk | | | | |
| Implementation effort | | | | |
| Parts removed | | | | |

## Architecture Review Packet

Return one structured packet containing:

1. invariant and API traceability matrix;
2. architecture candidates and tournament matrix;
3. provisional selected architecture;
4. component deletion, merge and replaceability matrix;
5. mechanism disposition and classification table;
6. physical-index shortlist;
7. contradictions and hard blockers;
8. Phase 2 research questions;
9. task paths and session IDs for every reviewer and subagent.

Do not edit the design documents to store this packet. Hand it directly to the
Phase 2 lead and the parent coordinator.

## Pass gate

Phase 1 passes only when:

- every hard requirement and API method is traced;
- every durable fact has one provisional owner;
- at least three viable architectures were compared;
- the index winner remains provisional pending research;
- every current mechanism has a disposition;
- research questions are finite and decision-relevant;
- no database candidate remains selectable;
- unresolved contradictions are explicit.

## Handoff record

> Mutable, append-only execution record. Complete this after gate evaluation.
> On a rerun, append Attempt 2 or later; do not overwrite an earlier attempt.

### Attempt 1

| Field | Value |
|---|---|
| Status | PASS |
| Gate | PASS — every hard requirement and all 26 API methods are traced; four independent candidates were compared; the catalog remains provisional for Phase 2 |
| Owner task path | `/root` |
| Owner session ID | `019fbff4-d312-7e43-bde1-11a3a66fd36f` |
| Started | 2026-08-02T00:57:26Z |
| Completed | 2026-08-02T01:28:21Z |
| Next phase | Phase 2 — Primary-source research |
| Next phase may start | YES |

### Subagents

| Scope | Task path | Session ID | Contribution |
|---|---|---|---|
| Simplified current design | `/root/simplified_current` | `019fbff6-7ef2-7863-90fd-211e7e86660a` | Proposed a two-component one-core/B+ design, one typed root and single `HEAD`; conditionally passed but retained a durable `PUBLISHING` transition and mixed identity, lifecycle and persistence. |
| Clean-slate minimum | `/root/clean_slate_minimum` | `019fbff6-9e69-75b0-9600-360f0bd99dfa` | Proposed a two-component one-core/Patricia design with alternating superblocks; exposed the smallest monolith and migration plan, but mixed responsibilities and permitted an unsafe older-slot fallback. |
| Algorithm and data-structure redesign | `/root/algorithm_redesign` | `019fbff6-be63-7fe0-9421-31faca547d3d` | Proposed three domain components, one permit service, a typed immutable radix forest, bundle-then-`CURRENT`, transient publication phases and a complete physical-index tournament. |
| Portability and failure model | `/root/portability_failure` | `019fc008-2100-7cc3-b454-adadf1973b22` | Proposed the selected four-component/one-service authority graph, proved the dual-slot/no-rollback contradiction, defined fail-closed single-`HEAD`, backend fact profiles and quota capability levels. |

### Synthesis

#### Architecture Review Packet

The provisional winner is the **Portable Single-Root Store**: four in-process
domain components, one permit-only shared service, immutable packed objects,
one fixed-purpose typed immutable catalog root, and one mandatory atomically
replaced `HEAD`. The current Workspace Engine is not a durable authority and
is removed as a component; its projection/capture/publication orchestration
moves to Lifecycle while physical realization remains in Backend Adapters.

```text
Public API -> Lifecycle
Lifecycle -> {Canonical State, Durable Store, Backend Adapters, Resource Admission}
Durable Store -> {Canonical State verifier, Resource Admission}
Backend Adapters -> {Canonical fact contract, Resource Admission}
Canonical State and Resource Admission -> no project component
```

The dependency graph is acyclic. Lifecycle is the sole public mutation and
semantic-transition authority. Durable Store is the sole physical-location,
root-selection, durability, recovery and reclamation authority. Canonical
State alone defines identity. Adapters never own identity, locators or
lifecycle truth. Resource Admission owns only bounded volatile counters and
permits; durable reservations remain records of the initiating Lifecycle or
Store operation.

The two-component candidates are viable deployment shapes, but not selected:
they reduce the visible count by hiding identity definition, lifecycle policy,
physical persistence, recovery, GC and admission inside one mixed-responsibility
core. The selected graph keeps the same single durable commit authority while
allowing the canonical format, physical store and backend implementations to
be replaced independently.

#### Hard-requirement trace

| Invariant or hard gate | Durable fact and provisional owner | Linearization / quiescence | Crash, replay and bound |
|---|---|---|---|
| One backend-neutral identity and exact attribution | Canonical State defines the only typed envelope, `ObjectId`, `StateManifest`, `StateId = ObjectId(StateManifest)`, Merkle directory and attribution rules; Durable Store owns selected object bytes | Pure construction has no linearization; a `StateId` becomes public only with `HEAD` | Every object is type/length/hash verified; unsupported facts fail before selection; construction is streamed or externally sorted under permits |
| Immutable content, logical CoW and structural sharing | Durable Store owns sealed segments and `ObjectId -> locator`; Canonical State determines equal objects | Existing IDs are reused; new segment dependencies are durable before `HEAD` | Partial/unselected packs are charged orphans; no payload copy for already-present objects; no per-object files |
| One physical catalog and one selecting authority | Durable Store owns one closed typed catalog root and mandatory `HEAD` | Same-filesystem `HEAD.tmp -> HEAD` replacement plus containing-directory sync | Before acknowledgement: old or complete new; after acknowledgement: selected new; invalid selected state fails closed, never falls back |
| Strict concurrent session publication | Lifecycle owns session origin `(StateId, head_token)`, current token, status and terminal receipt | The expected token is checked under the single writer and the head/status/receipt delta is selected by the same `HEAD` | Crash before selection leaves `ACTIVE`; lost reply replays receipt; mismatch selects terminal `CONFLICTED`; fixed gates and permits bound fanout |
| Checkpoint semantics | Lifecycle owns immutable checkpoint ID, sandbox owner and pinned committed `StateId` | One typed catalog commit; creation observes a selected head; removal checks exact pins | Old or new complete metadata; exact receipt or `ReplayExpired`; no session content is included |
| Fork, rollback and fork commit | Lifecycle owns immutable immediate-parent/origin-checkpoint binding and exact origin pin; no history | Quiescence gates and the same `HEAD` commit; fork commit uses the locked ordered `P/C/B` table | Metadata-only old/new result; no implicit merge, rebase, history, cascade or reconstruction chain |
| Read-only consumer isolation | Adapters own only disposable private projections/handles; Lifecycle owns allocation/session meaning | Workspace exposure follows verified materialization; publication fences only the publishing workspace | On restart adapters are fenced before readiness; canonical store is never writable by a consumer; idle sessions retain no service worker/buffer/FD |
| Bounded capture, streaming and listing | Initiating Lifecycle/Store record owns durable reservation; Resource Admission owns volatile permit | All-or-none fixed vector is acquired before FDs, buffers, staging or workspace allocation | Large sets stay disk-backed; queues contain bounded descriptors and zero payload; overload is typed denial before expensive work |
| Bounded replay | Lifecycle owns authenticated request epoch/sequence, retained exact receipt and low-water mark | Effect and receipt are in the same catalog root selected by `HEAD` | Retained ID returns exact result; expired authenticated ID returns `ReplayExpired` without execution; no forever history |
| Exact GC and near-full recovery | Durable Store owns selected roots, segment retirement and finite reader/recovery slots | Replacement catalog/locators are selected before old bytes are unlinked | Trace/external-sort/merge/repack is bounded composed work; maintenance reserve is admitted first; crashes leave selected data plus reclaimable excess |
| Portability | Canonical State owns fact meanings; each Adapter owns a versioned qualification result; Durable Store owns storage-medium qualification | Writable activation requires every capability before session creation | Docker works from private ordinary files; WASI/Firecracker reject unrepresentable facts; OverlayFS/snapshots/reflinks/FUSE/privilege/cache never supply correctness |
| Byte, inode and runtime enforcement | Lifecycle owns requested policy; Adapter owns proof for its runtime/workspace; Resource Admission accounts aggregates | `EnforcedQuota` activation occurs only after proven byte, inode and runtime controls | Arbitrary bind directories offer `PortableAccounting` only; missing enforcement is fail-closed, never described as a hard quota |

#### Complete API trace

| Methods | Owner and durable facts | Commit, quiescence and bounded behavior |
|---|---|---|
| `create_sandbox`, `destroy_sandbox` | Lifecycle owns sandbox status/head/token and receipt | One `HEAD` commit; destroy is quiescent and non-cascading; import streams under a full reservation |
| `get_sandbox`, `list_sandboxes` | Lifecycle schema read through a Durable Store root lease | No mutation; one selected-root snapshot; bounded pagination and finite cursor/lease |
| `export_sandbox` | Lifecycle captures one committed `StateId`; Canonical State and Store stream it | Sessions excluded; no linearization; bounded reachability sort/stream and sink backpressure |
| `create_workspace_session` | Lifecycle owns durable `OPENING`, then `ACTIVE`, origin/token, reservation and opaque adapter allocation | `OPENING` counts for quiescence; each transition is one `HEAD` commit; materialization is `Theta(B+F)` and fully reserved |
| `get_workspace_session`, `list_workspace_sessions` | Lifecycle session records | Selected-root read, bounded pagination; no per-session resident registry |
| `publish_workspace_session` | Lifecycle owns strict-origin decision, terminal status and receipt; Store owns new objects/locators and commit | Only the publishing workspace is fenced; durable state may remain `ACTIVE` during transient capture; one final `HEAD` selects locators, head/token, status and receipt |
| `destroy_workspace_session` | Lifecycle owns terminal close and cleanup ownership | One `HEAD` commit; cleanup is idempotent and remains charged until complete |
| `create_checkpoint`, `get_checkpoint`, `list_sandbox_checkpoints`, `remove_checkpoint` | Lifecycle owns checkpoint records and origin pins | Create may coexist with sessions; reads paginate; removal rejects a bound checkpoint; metadata-only `HEAD` commits |
| `rollback_sandbox` | Lifecycle owns sandbox head/token and receipt | Sandbox must have zero mutable sessions; selected checkpoint must belong to it; one `HEAD` commit yields `RolledBack` or `AlreadyCurrent` |
| `fork_sandbox` | Lifecycle owns child, returned checkpoint, immutable parent/origin binding and pin | Source quiescent; optional checkpoint creation and child creation are one commit; child is operationally detached |
| `get_sandbox_parent` | Lifecycle immediate-parent/origin record | Bounded selected-root read; roots return `null`; no ancestor/history API |
| `commit_fork` | Lifecycle owns parent head/token and ordered result receipt | Parent and child quiescent; mandatory checkpoint; gates acquired in stable ID order; exact `AlreadyCurrent`, `NoChanges`, `Committed`, `ParentDiverged` table |
| `exec_command`, `write_command_stdin`, `read_command_lines` | Adapter owns bounded runtime process/stream state; Lifecycle owns the active-session authorization | No canonical commit; bounded command/line windows and adapter sequence receipts; crash loses only unpublished runtime state |
| `file_read`, `file_blame` | Lifecycle resolves one committed state; Store/Canonical State verify and stream content/attribution | Selected-root lease for the stream; no writable handle; fixed buffers/FD permits |
| `workspace_file_read`, `workspace_file_write`, `workspace_file_edit` | Adapter owns private workspace bytes; Lifecycle authorizes `ACTIVE` or allowed read-only `CONFLICTED` state | Adapter operation boundary, not `HEAD`; writes are unpublished and admitted; publication remains the sole canonical transition |

All **18 lifecycle methods and 8 runtime methods** are present above. No public
signature, generic ref/target/backend selector, checkpoint rule, fork rule or
four-result fork-commit decision changes.

#### Architecture tournament

| Criterion | Current draft | Simplified current | Clean-slate minimum | Provisional selected design |
|---|---|---|---|---|
| Components and authorities | 5 domain + 1 service; Workspace and Adapter duties overlap | 2 components, 0 services; one mixed Core | 2 components, 0 services; one mixed Core | 4 domain + 1 permit service; identity, physical store, lifecycle and adapter duties distinct |
| Durable structures | Segments, two CoW B+ roots, dual slots, fences, lifecycle/workspace records | Segments, one typed B+, single `HEAD`, staging | Segments, one Patricia root, alternating superblocks | Segments, one typed catalog arena/root, single `HEAD`, typed lifecycle records |
| Transient structures | Bounded streams/sort, several component gates | Bounded streams/sort, core gates | Bounded streams/sort, reader epochs | Bounded streams/sort, fixed lifecycle gates, finite leases and fixed-vector permits |
| Publication barriers | Object, catalog and dual-slot/selector sequences; exact count obscured | Durable `PUBLISHING`, object group, final catalog/`HEAD` | Object, directory, catalog, inactive superblock | Immutable dependencies, catalog, `HEAD` file and `HEAD` directory; no durable `PUBLISHING` |
| Public/process roundtrips | Multiple internal component calls and phase-shaped handoffs | One client request, one adapter stream, internal core calls | One client request and adapter stream | One client request, one adapter stream, one typed Store commit; in-process ports |
| Payload copies | Missing payload packed; full ordinary-file projection/capture | Same | Same | Same; unchanged payload stationary, no unlawful zero-copy claim |
| Metadata scans | Full capture plus B+ paths and GC scans | Full capture plus B+ paths | Full capture plus Patricia paths | Full capture; bounded sorted batch lookup; exact streaming GC |
| Sparse update | `O(KH)` across two maps | `O(KH)` one B+ | `O(KD)` radix bound | Phase 2 chooses one B+ or typed radix; one root only |
| Dense rebuild | Streamed bulk rebuild of two roots | One streamed B+ rebuild | One streamed Patricia build | One streamed sorted merge/bulk build |
| Peak application memory | 8 MiB stated target, formulas not reconciled | Fixed; 8 MiB target | Fixed; 8 MiB target | Fixed permit formula; numeric target remains unachieved until Phase 3 |
| Peak disk/inodes | Bounded in prose; dual generations and GC reserve | Live + staging + obsolete + GC reserve | Same | Explicit live + workspaces + staging + obsolete + one admitted replacement; finite file generations |
| Crash states | Dual-slot fallback can silently roll back acknowledged corruption | Single-`HEAD` old/new/fail-closed | Older-slot fallback ambiguity | Single mandatory `HEAD`: old/new before ack, new after ack, corruption fail-closed |
| Recovery complexity | Two slots, generation fences, tail/reconciliation rules | Validate one `HEAD`; bounded cleanup | Elect greatest valid slot | Validate one `HEAD` and root; bounded owned cleanup only |
| Backend coupling | Storage qualification is incorrectly under adapters | Adapter port is narrow | Adapter port is narrow | Store qualifies medium; adapters qualify fact/runtimes; no backend fact in identity |
| Dependency risk | Custom SeqCDC and two custom page maps are under-researched | Custom SeqCDC/B+ | Custom CDC/Patricia | Phase 2 must justify hash/codec/index; fixed chunks are simpler default |
| Implementation effort | 28–40 engineer-week estimate in draft | Agent hypothesis 22–32 weeks | High disruptive migration | Lower structure count; no numeric claim until evidence; one-shot migration |
| Parts removed | Baseline | Four visible boundaries, one root/slot | Four boundaries, B+ invariants | Workspace authority, one catalog root, one descriptor slot, fence arrays, durable publishing phase, generic transaction vocabulary, duplicate counters |

Tournament verdicts: the current design is correctable but rejected for
complexity; simplified-current and clean-slate pass conditionally but are not
selected because their one Core hides mixed responsibility; the radix bundle
candidate passes conditionally and supplies the leading index; the
portability/failure candidate wins the component and single-`HEAD` decisions.

#### Component deletion, merge and replacement matrix

| Proposed component/service | One responsibility and owned facts | Narrow ports | Delete/merge/replace verdict and lost invariant |
|---|---|---|---|
| Canonical State | Define canonical facts, object envelope, Merkle identity and attribution; owns definitions, not locations | `build(fact_stream)`, `decode`, `verify`, typed object stream | **Keep.** Do not merge with Store or Adapter. Removing it loses backend-neutral identity; a new format can replace it only through explicit versioned migration. |
| Durable Store | Own immutable bytes, locators, catalog pages/arena, sole `HEAD`, physical recovery, leases and retirement | typed object read/install, selected snapshot, named typed lifecycle commit, exact trace/rebuild | **Keep.** Merging Lifecycle mixes semantic policy with storage format; replacing B+/radix/segments behind this port does not alter API or adapters. Removing it loses durability and location authority. |
| Lifecycle | Own public mutation semantics and lifecycle records: heads/tokens, sessions/origins/status, checkpoints/pins, parent binding, receipts/horizon and durable reservations | public API, Adapter allocation/fence/capture/dispose, Canonical build, typed Store delta | **Keep; merge Workspace orchestration here.** Removing it duplicates mutation rules in API/Store/Adapters; replacing implementation preserves Store/Adapter contracts. |
| Backend Adapters | Realize, fence, capture and dispose private workspaces; own disposable runtime artifacts and qualification evidence only | canonical fact stream plus opaque allocation handle; no Store path or locator | **Keep.** Removing leaks Docker into core; implementations replace independently; merging breaks backend portability/isolation. |
| Workspace Engine | No unique durable fact; only composes projection/capture/publication | Its useful operations already cross Lifecycle and Adapter ports | **Remove as component; retain `workspace_engine.md` as workflow authority.** No invariant is lost. |
| Resource Admission | Atomically grant one fixed volatile resource vector; owns no durable fact | `admit(vector) -> permit`, release/reconstruct bounded counters | **Keep as one shared permit-only service.** Merging into Lifecycle creates reverse dependencies for Store GC and Adapter runtime work; replacement changes no durable format. |

#### Durable-fact ownership

| Fact | One authority |
|---|---|
| Canonical fact schema, object envelope, `ObjectId`, `StateManifest`, `StateId`, attribution rule | Canonical State |
| Packed object bytes, segment trailer, object locator, catalog physical pages, `HEAD`, storage capability proof, physical leases/retirement | Durable Store |
| Sandbox status/head/token; session origin/status/allocation association; checkpoints; origin pins; immediate parent binding; lifecycle receipt/low-water mark; durable operation/workspace reservations | Lifecycle (persisted opaquely by Durable Store) |
| Workspace files, runtime handles/fences, adapter fact-profile and runtime/quota qualification | Backend Adapter; these artifacts are disposable and never canonical authority |
| Volatile permit counters | Resource Admission; no durable facts |

#### Current-mechanism disposition and preliminary classification

| Current item | Disposition | Preliminary final classification |
|---|---|---|
| `CS-1 Canonical Filesystem Encoding` | Keep, but test adoption of deterministic typed encoding | Candidate custom algorithm or adopted standard operation; Phase 2 decides |
| `CS-2 Canonical Merkle Radix Directory` | Keep and simplify | Self-implemented algorithm |
| `CS-3 Streamed SeqCDC File Encoding` | Replace; fixed-size chunks are the simplicity default | Adopted standard/library operation unless frozen CDC evidence reverses it |
| `CS-4 Canonical Attribution Tiling` | Keep | Self-implemented algorithm |
| `CS-5 Bounded External Canonical Build` | Reclassify | Composed workflow using bounded streaming/external sort |
| `DS-1 Sealed Segment Installation` | Merge into publication | Composed durability workflow using hash/checksum/sync/rename |
| `DS-2 CoW B+ Physical Catalog` | Replace with one selected typed B+ or radix catalog | One self-implemented fixed-purpose index algorithm |
| `DS-3 Dual-Slot Root Commit and Recovery` | Replace | One self-implemented single-`HEAD` crash/durability protocol |
| `DS-4 Snapshot Lease` | Reclassify | Adopted bounded epoch/lease operation |
| `DS-5 Streaming Trace-Repack GC` | Reclassify and simplify | Composed trace, external-sort, merge, repack and root-publication workflow |
| `DS-6 Bounded Receipt Replay` | Merge into root commit | Lifecycle receipt policy plus crash-protocol substep |
| `WS-1 Reserved Full Projection` | Merge into Lifecycle/Adapter | Composed workflow |
| `WS-2 Quiesced Stable Capture` | Merge into Lifecycle/Adapter | Composed workflow and adapter contract |
| `WS-3 Payload-Stationary Strict Publish` | Merge into Lifecycle/Store commit | Composed workflow plus lifecycle transition |
| `WS-4 Bounded Stream Pipeline` | Reclassify | Adopted bounded channels/backpressure/external sort |
| `LC-1 Linearizable Session Gate` | Reclassify | Lifecycle transition and standard fixed-shard synchronization |
| `LC-2 Checkpoint Pin and Removal` | Reclassify | Lifecycle transitions |
| `LC-3 Checkpoint-Bound Fork` | Reclassify | Lifecycle transition/composed workflow |
| `LC-4 Quiescent Root Rollback` | Reclassify | Lifecycle transition |
| `LC-5 Strict Fork Commit` | Reclassify | Lifecycle transition with fixed decision table |
| `LC-6 Non-Cascading Destroy` | Reclassify | Lifecycle transition |
| `BA-1 Storage Capability Qualification` | Move to Durable Store | Qualification/test procedure |
| `BA-2 Descriptor-Relative Safe Projection` | Reclassify | Adapter workflow using adopted OS primitives |
| `BA-3 Exact Capture Contract` | Reclassify | Adapter contract/composed workflow |
| `BA-4 Portable Archive Stream` | Reclassify | Adopted encoding plus composed streaming workflow |
| `BA-5 Adapter Identity Equivalence Gate` | Reclassify | Qualification/test procedure |
| `RG-1 Atomic Multi-Resource Admission` | Keep service, remove algorithm label | Policy using standard synchronization; not a storage algorithm |

The preliminary custom registry has **at most five** items pending Phase 2:
canonical typed encoding, canonical Merkle directory construction, exact
attribution tiling, the fixed-purpose immutable catalog update algorithm and
the single-`HEAD` commit/recovery protocol. Fixed-size chunking would reduce
this to four if deterministic typed encoding is adopted rather than invented.

#### Physical-index shortlist

| Candidate | Phase 1 result |
|---|---|
| Adaptive immutable CoW B+ | **Runner-up.** Short cache-off paths and excellent sorted-batch/scan behavior; split/fill/rebalance and page-layout complexity require evidence. |
| Append-only sorted tables | Dense-builder only; sparse lifecycle updates otherwise rewrite `Theta(N)` or accumulate generations. |
| Immutable SST/bounded LSM | Reject: precedence, tombstones, filters and levels recreate forbidden database machinery. |
| Persistent typed radix | **Leading challenger.** Key-length-bounded paths, no rotations/free list and exact prefix scans; cold-page and page-amplification costs require evidence. |
| Extendible hash | Reject: unordered traversal, directory doubling/overflow and weak worst-case rebuild behavior. |
| Packed flat index | Leaf/dense-migration artifact only; reject as sparse root due `Theta(N)` rewrite. |
| Static FST-like index | Reject as primary: sparse locator changes force broad rebuild and random digests compress poorly. |

No database candidate remains selectable. Phase 2 must select persistent typed
radix or fixed-purpose immutable CoW B+; the authority graph and single-`HEAD`
protocol do not depend on that choice.

### Evidence used

- Complete goal objective, refinement index and all six phase specifications.
- All ten authoritative design documents, including the 18 lifecycle and 8
  runtime methods and the current 27-name registry.
- Stage 4.6 proof-of-concept documentation and source references as evidence
  only: owner/locator/projection/phase/recovery authorities, OverlayFS and
  capability assumptions, roundtrip ledger, sealed-generation measurements
  and current migration history.
- Initial implementation worktree: branch `upgrade-2.0-phase-1`, pre-existing
  untracked `mpla_demonstrations.md` and `tmp/`; unchanged.
- Initial documentation worktree: branch `layerstack_2_0`, five commits ahead,
  pre-existing Stage 4.6 modifications/untracked files and the untracked
  `system-design/` tree; unrelated work preserved.
- Independent subagent reports identified in the Subagents table. Primary web
  evidence is intentionally deferred to Phase 2.

### Decisions and results

- Architecture Review Packet: produced in this Handoff record.
- Provisional architecture: Portable Single-Root Store, **4 domain components
  + 1 permit-only shared service**.
- Root protocol: one mandatory checksummed atomically replaced `HEAD`; after
  acknowledged corruption, fail closed rather than elect an older generation.
- Publication phase: `OPENING` is durable; capture/publication may remain
  transient while the durable session is `ACTIVE`; the final root selects
  locators, head/token, terminal session result and replay receipt together.
- Physical index: typed radix leads and CoW B+ remains the runner-up; Phase 2
  must select one with primary evidence.
- Chunking: fixed-size is the simpler provisional baseline; FastCDC/CDC may win
  only with a frozen complete profile, golden vectors and material evidence.
- Component and mechanism dispositions: complete above; Workspace Engine is
  removed as an authority and all 27 current names have a disposition.
- Migration: one-shot, read-only legacy source, streamed fact/attribution
  rebuild, reference verification, atomic routing switch and bounded read-only
  rollback retention; never dual-write or retain a permanent compatibility
  fast path.

#### Contradictions and hard blockers exposed

1. `StateId` is restated inconsistently in Lifecycle; only
   `StateId = ObjectId(StateManifest)` may remain normative.
2. Durable Store physically persists lifecycle bytes while Lifecycle claims
   semantic ownership; the final docs must distinguish custody from authority.
3. Forever same-request replay contradicts bounded metadata. Use an
   authenticated bounded replay horizon and deterministic `ReplayExpired`
   without execution.
4. Dual-slot fallback contradicts acknowledged-generation no-rollback because
   recovery cannot distinguish a pre-ack torn latest slot from later corruption
   of an acknowledged latest slot.
5. Workspace Engine claims publication/reclamation duties also claimed by
   Lifecycle/Store; it owns no unique durable fact and must cease being a
   component.
6. Storage-medium qualification is under Backend Adapters, improperly mixing
   runtime adaptation with durability authority; move it to Durable Store.
7. Two catalog roots and generic transaction vocabulary are unnecessary; one
   closed typed root must select locator and lifecycle changes together.
8. SeqCDC is underspecified and unsupported; fixed chunks are the default until
   primary evidence justifies a frozen CDC profile.
9. An arbitrary bind-mounted directory cannot honestly promise hostile-process
   hard byte/inode limits; separate `PortableAccounting` and `EnforcedQuota`.
10. The 8 MiB pool is a target, not an achieved measurement, and must include
    page, codec, sort, emergency and reader buffers; page cache/RSS/runtime
    memory require separate accounting.
11. Durable `PUBLISHING`, duplicate active/pin counters, generation-fence arrays
    and semantic projection manifests add states or authorities without a
    demonstrated invariant.

These are Phase 2/3 decision inputs, not unresolved Phase 1 omissions.

### Blockers and returned work

- No Phase 1 blocker. Architecture and descriptor choices remain provisional
  exactly where primary evidence or adversarial resource proof is required.

### Files changed

- `refine/phase_1_architecture_review.md` — this Handoff record only. No
  authoritative design document or production source changed.

### Output for Phase 2

- Research questions and selecting decisions:
  1. Radix versus immutable CoW B+: primary papers/formats, cold point and
     page-aware batch reads, sparse amplification, dense build, scan, corruption,
     bounded RAM/FD and maintenance effort; select exactly one.
  2. Single `HEAD` versus A/B descriptors: official file/directory sync and
     crash-consistency evidence plus fault cuts; select the minimum protocol
     that cannot silently roll back acknowledged state.
  3. Deterministic typed encoding: determine whether an adopted standard/Rust
     codec can supply one canonical byte sequence and stable schema evolution;
     otherwise justify the minimal custom envelope.
  4. BLAKE3: verify specification, Rust maintenance/license/platforms, streaming
     memory and same-ID validation obligations.
  5. Fixed-size versus FastCDC: quantify deduplication benefit, deterministic
     profile/version/gear table/parameters/golden vectors and dependency risk;
     choose fixed size when evidence is not decisive.
  6. Segment/trailer layout: identify primary format evidence, checksum and
     bounded recovery rules without per-object durability or a second index.
  7. Reader epochs and GC: prove bounded transient leases suffice after process
     fencing, and derive exact trace/repack safety without a durable reader log.
  8. Replay: prove information requirements and define authenticated sequence,
     horizon, exact receipt and low-water behavior without changing public
     method signatures or creating history.
  9. Docker/WASI/Firecracker and descriptor-relative traversal: establish
     universal, capability-qualified and impossible fact/durability profiles.
  10. Quotas/cgroups: identify exact byte, inode, process and memory enforcement
      capabilities; prohibit accounting from being described as enforcement.
  11. Migration: decide whether existing canonical bytes/`StateId`s can remain;
      if not, require one-shot fact-equivalent re-encoding and complete reference
      rewrite with no permanent ID map.
  12. Dependency and license review: adopt only narrow hash/codec/sort/syscall
      support; reject every database, database-like engine and hidden cache.
- Decisions Phase 2 must validate: four-component/one-service graph; one typed
  root; single mandatory `HEAD`; transient publication phase; fixed-size chunk
  default; preliminary custom registry; fail-closed backend capability contract.
- Required source areas: original index/tree/chunking/hash papers and specs;
  official Rust projects; official Linux/filesystem/OCI/Docker/WASI/Firecracker
  documentation; original crash-consistency research.
- Transcript/packet reference: this Attempt 1 plus the four task/session reports
  in the Subagents table.
