# LayerStack-0 durable Version storage design

Status: **PHASE 01 CONTRACT — exact Phase 03 selections pending**  
Owner: Phase 03, implemented inside `crates/sandbox-runtime/layerstack`  
Prerequisite: Phase 02 identity passes I1–I7  
Authority: product [hard rules](../PRD.md#hard-rules-must-never-break) and the selected
[R0 architecture](../architecture_design.md)

## 1. Purpose and decision boundary

This document defines the offline LayerStack-0 durable-Version contract selected by Phase 01.
It fixes the storage family, owner, write authority, failure semantics, and
required primitives. Phase 03 selects and proves only the bounded filesystem
mechanics left open here.

| Label | Meaning |
|---|---|
| `LOCKED_PHASE_01` | R0 architecture invariant; Phase 03 may not weaken or replace it. |
| `SELECT_IN_PHASE_02` | Pure identity choice consumed by the store and not redefined here. |
| `SELECT_IN_PHASE_03` | Exact durable implementation choice inside the R0 family. |
| `OWNER_DEC_OPEN` | Product-owner decision remains open behind a stable store seam. |
| `REOPEN_PHASE_01` | Evidence would change owner, storage family, writer count, dependency direction, or a hard rule. |

## 2. Selected store in one table

| Concern | R0 decision | Status |
|---|---|---|
| Storage owner | LayerStack-0 in the existing `sandbox-runtime-layerstack` package, rewritten internally | `LOCKED_PHASE_01` |
| Deployment boundary | In-process library under existing application/effect/lifecycle consumers; no RPC/service | `LOCKED_PHASE_01` |
| Payload | One complete immutable filesystem closure per Accepted Version and occupied `VersionId` | `LOCKED_PHASE_01` |
| References | Small typed roots and heads name store-accepted bindings; no payload bytes | `LOCKED_PHASE_01` |
| Candidate work | Bounded private staging, never selected truth | `LOCKED_PHASE_01` |
| ID occupancy | Full canonical-byte comparison; equal reuses one payload, unequal is collision | `LOCKED_PHASE_01` |
| Publication | Durable payload before a reference may name it; one OCC head transition | `LOCKED_PHASE_01` |
| Writer | One process/filesystem-exclusive selected-Version transition gate | `LOCKED_PHASE_01` |
| Read | Capture one immutable accepted binding with bounded read custody | `LOCKED_PHASE_01` |
| Recovery | Prior or complete new truth; bounded recognizable debt; ambiguity/corruption fails closed | `LOCKED_PHASE_01` |
| Retirement | Exact roots/heads/read-custody reachability with serialized final revalidation | `LOCKED_PHASE_01` |
| Migration | Temporary one-way importer through normal V2 APIs under a generation fence | `LOCKED_PHASE_01` |
| Physical mechanics | Local layout spelling, record encoding, fences, lock primitive, custody form, limits | `SELECT_IN_PHASE_03` |

The selected family is not a layer/delta chain, an archive that must be
extracted for normal use, an object/chunk DAG, a database authority, a
persistent refcount truth, or an external Version service.

## 3. Ownership and dependency direction

The store owns:

- immutable payload admission and physical occupancy;
- accepted-binding creation and validation;
- durable roots and heads;
- the single final selected-Version transition gate;
- OCC comparison and head replacement;
- read custody, recovery, retirement, and store-side cleanup; and
- bounded store diagnostics and test counters.

It does not own:

- application authorization, revoke ordering, API policy, retries, audit,
  MCTS, rollout, or winner choice;
- writable workspace construction, OverlayFS, mounts, namespaces, execution,
  or host-path lifecycle;
- portable identity grammar or digest selection, which Phase 02 supplies as a
  pure internal module; or
- daemon/manager lifecycle beyond returning readiness and typed diagnostics.

Allowed dependency direction is:

```text
application / effects / lifecycle / diagnostics
    -> sandbox-runtime-layerstack store
        -> pure internal identity module
        -> low-level filesystem, locking, hashing, serialization primitives
```

The store must not depend upward on application services, workspace effects,
mount/namespace implementations, observability authority, or temporary legacy
types. Temporary import code may depend on permanent V2 APIs; permanent V2
identity/store code must not depend on the importer.

## 4. Conceptual durable model

Names describe logical roles, not an exact Phase 03 disk spelling. In
particular, `versions/` names the accepted Version population; it does not
select CDC, chunks, an object DAG, or a `VersionView` indirection:

```text
<LayerStack0Root>/
  versions/<VersionId>/payload/  one complete immutable accepted payload closure
  heads/<selector>               AcceptedBinding + monotone HeadRevision
  roots/<kind>/<root-id>         typed durable reachability to AcceptedBinding
  staging/<transaction-id>/      bounded private unaccepted candidate
  control/...                    format, generation, lock, and recovery metadata
```

Phase 03 must select the exact physical root and path spelling. If V2 and the
e497 reader coexist during migration, the V2 namespace must not overlap legacy
`manifest.json`, `workspace.json`, `layers/`, `staging/`,
`.layer-metadata/`, or `base/`. The current `/eos/layer-stack` mount is a
placement fact, not an automatic new-format root and not something branding
alone renames. Phase 05 consumes the selected layout through LayerStack-0 APIs;
it must not invent paths or write them directly.

### 4.1 Payload invariants

- A payload is a complete qualified Version. A read never needs a parent,
  changeset, depth walk, merge, squash, or whiteout-as-delta reconstruction.
- The payload preserves or can regenerate the full canonical bytes required for
  exact occupied-ID comparison.
- Equal canonical bytes at an occupied `VersionId` reuse the existing physical
  payload. Concurrent equal admission converges on that one occupant.
- Unequal canonical bytes at an occupied ID fail as collision. No second
  physical occupant, alias, root, or head is created for the mismatch.
- Newly accepted payload content and required descriptor/comparison metadata are
  durable and integrity-checkable before any root/head may name the binding.
- Store custody never exposes an accepted payload as a writable workspace.
- R0 does not guarantee cross-Version file/block deduplication between different
  `VersionId`s. A future optimization must preserve closure completeness and may
  not introduce hidden layer/DAG truth without architecture review.

### 4.2 Reference invariants

- A durable root/head contains a store-accepted binding, not candidate bytes or
  an unchecked raw digest.
- A head additionally contains a monotone `HeadRevision` used by OCC.
- Records are complete, versioned, integrity-checkable, and atomically replaced
  as one logical value.
- Roots and heads do not embed, duplicate, or read payload content during a
  reference-only move.
- A reference can never name private staging, incomplete content, an unknown
  version, or a collision mismatch.

### 4.3 Truth and non-truth

Selected durable truth is the accepted immutable payload population plus valid
roots/heads under the active store generation. The following are not selected
truth:

- staging transactions and recoverable orphan debt;
- observability projections, counters, or indexes;
- caches, persistent optimization hints, or reconstructed refcounts;
- writable workspaces and mounts;
- migration progress outside the active generation fence; and
- legacy layers, parents, depth, squash, merge, or lease records.

## 5. Conceptual types and primitives

Exact Rust representation is `SELECT_IN_PHASE_03`; the separation is fixed.

```text
VersionId           typed Phase 02 identity; candidate-level until admitted
AcceptedVersion     LayerStack-0-owned admitted complete immutable payload
AcceptedBinding     LayerStack-0-issued/revalidated capability naming AcceptedVersion
HeadRevision        monotone OCC token
HeadRecord          selector -> (AcceptedBinding, HeadRevision)
RootRecord          fixed (RootKind, RootId, incarnation) -> AcceptedBinding
ReadCustody         bounded runtime-local protection for a captured binding
AdmissionReceipt    AcceptedVersion/binding + NewPayload | ReusedPayload
StoreGeneration     active writer/migration generation
StoreLimits         finite resource/population limits
StoreError          typed failure; never silent fallback to legacy truth
```

Required store primitives:

| Primitive | Inputs | Result and authority |
|---|---|---|
| Admit candidate | Complete bounded portable candidate | Accepted binding plus new/reused result; no reference change |
| Publish candidate | Selector, expected `(binding, revision)`, candidate | Admission plus exactly one conditional head transition |
| `CreateHeadIfAbsent` | Typed Head identity, `Expected::Absent`, `AcceptedBinding` | Conditional complete-record creation under the sole reference authority |
| `ReplaceHead` | Typed Head identity, `Expected::Exact(expected_head)`, `AcceptedBinding` | The sole metadata-only Head movement/OCC point |
| `RemoveHead` | Typed Head identity, `Expected::Exact(expected_head)` | Conditional complete-record removal under the same authority |
| `CreateFixedRootIfAbsent` | Typed Root identity/kind, `Expected::Absent`, `AcceptedBinding` | Conditional creation of one fixed reachability pin |
| `RemoveFixedRoot` | Typed Root identity/kind, `Expected::Exact(expected_root)` | Conditional removal of that exact fixed pin |
| Resolve/capture read | Typed root/head selector and custody request | Captured binding/revision plus read-only custody |
| Release read | Read custody | Bounded custody release; no truth change |
| Recover/readiness | Store root, version/profile, limits | Ready active generation or typed fail-closed diagnostic |
| Retire | Accepted target or bounded sweep unit | Retained, retired, or retry/deferred after exact revalidation |
| Import | Temporary fenced input | Ordinary admission/reference outcomes only |

Detailed algorithms and error/side-effect contracts are in
[04-algorithms-and-call-flows.md](04-algorithms-and-call-flows.md).
The complete five-operation lifecycle and shared outcomes are normative in
[Reference EphCoW](../algorithm/02-references-and-publication/01-reference-ephcow.md).
No generic Root update/retarget primitive exists. A Branch is a Head; a
Checkpoint is a fixed typed Root.

## 6. Admission and accepted bindings

Admission is separate from reference mutation:

1. validate/canonicalize/hash the complete candidate with Phase 02 APIs;
2. reserve bounded staging resources before materialization;
3. construct private candidate payload and comparison material;
4. inspect occupancy at the derived `VersionId`;
5. if occupied, compare full canonical bytes;
6. reuse on equality or return typed collision on mismatch;
7. if absent, make one complete payload durable, integrity-checkable, and
   immutable, then atomically expose it as accepted; and
8. issue an accepted binding only after the accepted occupant is established.

Admission alone never changes a root or head. An Accepted Version can therefore
become an unreferenced orphan after a later stale publication; this is safe,
bounded cleanup debt, not mixed truth.

An accepted binding must be unforgeable by ordinary API construction or be
revalidated by the store at every ingress. A raw `VersionId`, even one produced
by the pure identity module, is not sufficient to use a reference-only path.

## 7. Publication, OCC, and write authority

The application owns authorization, request/revoke ordering, candidate
orchestration, and capture of an expected head. The store owns the final
authoritative comparison and transition.

Candidate preparation, canonicalization, hashing, staging, exact comparison,
and payload durability should occur outside the final transition gate. Under
the one exclusive gate, the store:

1. rereads the current complete head record;
2. compares it to the caller's expected `(AcceptedBinding, HeadRevision)`;
3. returns typed stale without any head mutation, merge, or rebase on mismatch;
4. prepares/installs one complete replacement head record on match; and
5. acknowledges success only after the selected reference durability boundary.

The logical conditional replacement of the complete Head record is the sole
Head movement/OCC linearization point. Initial Head creation and exact Head
removal use the same reference authority, conditional complete-record
transition family, qualified fence, and read-back seam; they do not create a
second movement/OCC point. Phase 03 selects the filesystem operation and exact
synchronization sequence that implement these semantics on an explicitly
supported local filesystem profile.

Payload admission visibility and OCC head transition are distinct points. A
crash or stale result may leave a complete unreferenced payload, but can never
leave a head naming incomplete content.

## 8. Reference-only zero-payload-I/O contract

Head create/replace/remove, fixed-Root create/remove, fork-to-Branch,
checkpoint-to-existing, rollback-to-existing, and same-Version Head behavior
have a dedicated accepted-binding path. For each operation:

- input contains a store-accepted binding and typed target/reference token;
- validation examines bounded binding/reference metadata only;
- the payload is never opened, mapped, walked, hashed, compared, read, staged,
  materialized, linked as a new private payload, or copied;
- only the small fixed-Root/Head record and required control metadata may
  change; and
- operation-scoped counters report selected payload bytes read = `0`, written =
  `0`, and copied = `0`.

Metadata reads/writes are expected and must be accounted separately. Filesystem
metadata implementation must not disguise payload work—for example, a hidden
archive extraction or full-tree validation cannot be labeled “metadata.”

Candidate bytes, a raw digest, or an unknown binding always use admission,
including full occupied-ID comparison. They cannot receive the reference-only
fast path merely because the candidate is expected to be equal.

## 9. Captured reads and immutability

A committed read:

1. resolves one root/head to a complete captured record;
2. acquires bounded runtime-local custody for the accepted payload;
3. reads/materializes only that immutable closure even if the selector moves;
4. exposes no writable payload handle; and
5. releases custody, allowing later exact retirement revalidation.

Read custody is not portable identity or durable selected truth. Phase 03 may
select its exact bounded representation, but it must close the race among root
removal, reader acquisition, and payload unlink. Time-based lease expiry alone
is not proof that no reader can use the payload.

Workspace/live-session reads and mutations remain with runtime-effect owners.
Committed payloads may be used as read-only bases, but a live write/edit must
create or mutate separate Candidate/Workspace custody and publish a new Version.

## 10. Durability and filesystem qualification

The following outcomes are fixed; exact micro-steps are not:

- no reference is acknowledged before its target payload is durably accepted;
- every durable record is either the prior complete record or the new complete
  record after a crash, never a torn/mixed logical value;
- payload content, payload descriptor, reference record, and containing
  namespace durability are ordered as required by the selected filesystem;
- unsupported filesystem semantics fail configuration/readiness rather than
  weakening the acknowledgement promise;
- cancellation, timeout, I/O error, and ENOSPC before reference commit leave the
  prior selected reference and only bounded private/recoverable debt; and
- an error after a durable linearization point reports an explicit ambiguous or
  recoverable outcome if the implementation cannot prove which acknowledgement
  the caller observed; it must never repeat a non-idempotent transition blindly.

Phase 03 must select and document:

- supported local filesystem profile and assumptions;
- atomic namespace/record replacement primitive;
- payload admission visibility primitive;
- exact file and directory synchronization/fence sequence;
- record version, checksum/integrity, and completeness markers;
- lock/gate primitive and process-crash behavior; and
- acknowledgement and retry semantics for every error boundary.

No exact `fsync`/rename sequence is selected by this document.

## 11. Recovery and readiness

Before declaring the store ready, recovery must validate within finite bounds:

- control/store format and active generation;
- record versions and integrity;
- accepted payload completeness and canonical identity consistency as required;
- every head and root target;
- recognizable private staging;
- complete unreferenced accepted payloads; and
- cleanup/recovery debt against configured limits.

Permitted restart classifications are:

| Durable condition | Required behavior |
|---|---|
| Complete private staging only | Clean or quarantine repeat-safely within a bound; no reference is visible. |
| Incomplete/invalid private staging | Remove/quarantine as bounded debt; never accept it heuristically. |
| Complete accepted payload, no root/head | Safe unreferenced payload; retain or retire by bounded policy. |
| Prior valid Head/fixed-Root record | Serve the prior accepted truth. |
| Complete new valid Head/fixed-Root record or authoritative exact removal | Serve the complete new accepted truth/absence after validating the protocol. |
| Torn, corrupt, dangling, unknown-version, or collision-ambiguous durable truth | Fail readiness/read closed with a typed diagnostic. |
| Debt exceeds the bounded recovery envelope | Fail readiness or enter an explicitly non-serving maintenance state; do not start an unbounded scan. |

Recovery is repeat-safe and never reconstructs selected truth from legacy
layers, filenames alone, observability indexes, or “best effort” guesses.

## 12. Reachability, retirement, and cleanup

Authoritative reachability sources are heads, typed roots, and active read
custody. Retirement:

1. runs as a bounded unit under selected-Version transition authority;
2. computes or verifies exact durable reachability without trusting a
   persistent refcount as truth;
3. performs final serialized revalidation of roots and active custody;
4. unlinks only a complete accepted payload proven unreachable; and
5. returns a repeat-safe retained, retired, or deferred/retry result.

An optional cache/index/refcount hint may improve performance only if it is
bounded, reconstructible, integrity-checked, and non-authoritative. Corruption
of such a hint cannot permit premature unlink or change selected truth.

Every failure path owns its staging, temporary records, descriptors, memory,
workers, and reservations. Synchronous cleanup is preferred; a crash may leave
only recognizable debt inside the selected finite population. Cleanup itself
must be idempotent and cancellable/batch-bounded.

## 13. Resource and security contract

Phase 03 selects finite limits and tests boundary behavior for:

- simultaneous admissions and staging transactions;
- staging bytes, store disk reservation, and minimum free-space policy;
- accepted payload/root/head populations;
- active read custody and concurrent readers;
- open descriptors, locks, workers/tasks, and in-memory indexes/caches;
- selector/root name lengths and counts;
- recovery/orphan/retirement debt per startup and per batch; and
- transition-gate wait/hold and cancellation behavior.

Admission must precharge relevant disk, scratch, memory, and descriptor capacity
before expensive work. Resource exhaustion returns a typed error before a
reference transition and never triggers silent eviction of rooted/custodied
payloads.

Store paths, selectors, and root IDs are untrusted. Phase 03 must use safe
descriptor/path-resolution mechanics so candidate replacement, symlink escape,
path traversal, and time-of-check/time-of-use substitution cannot write outside
store custody or mutate an accepted payload. The exact primitive is
`SELECT_IN_PHASE_03`.

## 14. Diagnostics and test seam

Diagnostics are bounded read-only projections. At minimum, operation-scoped
tests and operational counters must expose:

- candidate bytes consumed and canonical bytes compared;
- selected payload bytes read, written, and copied by operation class;
- new versus reused accepted payloads and physical accepted-payload count;
- head/root metadata bytes and operation outcome;
- OCC success/stale/same-Version outcomes;
- collision outcomes;
- staging bytes/transactions and orphan/recovery debt;
- roots, heads, active read custody, descriptors, workers, and reservations;
- cleanup/retirement results and readiness failures; and
- transition-gate wait and hold time where measurable.

Raw Version IDs, tenant-controlled paths, or selectors must not become unbounded
metric labels. Instrumentation cannot become authority or be required to
reconstruct selected truth.

## 15. Migration seam

The Phase 05 importer is temporary and subordinate to this store:

1. lifecycle owners establish a monotone active store generation;
2. legacy mutating ingress drains and legacy truth becomes read-only;
3. importer decodes one legacy selected view into complete portable facts;
4. it calls normal identity, admission, and exact Head/fixed-Root lifecycle
   primitives, selecting create/replace/remove from the mapped source kind;
5. it never writes an alternate V2 representation or bypasses collision/OCC;
6. retry uses exact admission and explicit generation/progress checks; and
7. importer types, feature/target, config, tests, and call sites are deleted as
   one unit after the owner-selected observation window.

The importer maps a legacy selected view to a complete portable candidate,
then receives the ordinary `VersionId` → `AcceptedVersion` →
`AcceptedBinding` result from LayerStack-0. A migration progress record may
remember that mapping for retry; it is not a user checkpoint, root, or second
truth. Legacy layer IDs, parents, depth, squash records, whiteouts, and runtime
paths are decoder inputs only and never enter Version identity.

`DEC-011` remains open only for observation duration. It cannot authorize dual
writes. Legacy-data deletion remains a separately authorized later action.

## 16. Source disposition for Phase 03

| Source area | Disposition | Store requirement |
|---|---|---|
| `crates/sandbox-runtime/layerstack/Cargo.toml` | `KEEP` | Existing package remains the dependency-neutral owner. |
| `layerstack/src/lib.rs` | `REWRITE` | Export narrow V2 store/identity types and operations. |
| `layerstack/src/model/**` | `REWRITE` | Replace permanent layer DTOs with accepted binding, head revision, roots/heads, and store records. |
| `layerstack/src/store/**` | `ADD` | Admission, payload, root/head, OCC, read, recovery, retirement, cleanup. |
| `layerstack/src/storage/{fs.rs,lock.rs}` | `REWRITE` | Reuse the primitive family under proved V2 durability semantics. |
| `layerstack/src/stack/**` and permanent layer/depth/squash/merge truth | `DELETE` or hard-fail from V2 path | No reconstruction or fallback. |
| `layerstack/src/workspace_base/**` | `REWRITE` | Complete accepted-Version binding or temporary importer; no permanent layer binding. |
| Store-local `legacy_import` | `ADD TEMPORARILY` in Phase 05 | One-way dependency on V2 APIs and deletable unit. |

Phase 03 may preserve legacy source temporarily to keep consumers compiling,
but the offline V2 core and tests must not read or write it as selected truth.

## 17. Phase 03 selections and forbidden substitutions

Phase 03 may select:

- the exact physical root, non-overlapping V2 namespace, on-disk names, and
  hierarchy inside the conceptual roles, documented as an API/layout contract
  consumed by Phase 05;
- record encoding, version, checksum, and completeness representation;
- temporary transaction names and bounded manifest/index aids;
- supported local filesystem profile;
- lock and safe path-resolution primitives;
- exact write/sync/rename/link fence sequence;
- finite store limits and recovery batch sizes;
- read-custody representation;
- retry/idempotency detail consistent with fixed linearization points; and
- internal modules and bounded instrumentation.

Phase 03 may not substitute:

- another owner, crate, service, helper process, database, registry, or
  coordinator;
- a layer/delta chain, archive-extraction truth, or chunk/object DAG;
- persistent refcount authority;
- digest-only equality;
- payload work on reference-only operations;
- multiple head writers or linearization points;
- silent merge/rebase;
- writable committed payloads;
- runtime-private identity; or
- dual writable legacy/V2 truth.

## 18. Verification map

| Phase 03 check | Store proof |
|---|---|
| F1 publish/read | Complete payload facts and identity round-trip |
| F2 stale OCC | Exactly one matching expected revision wins; stale changes no head |
| F3 Head create/fork | `CreateHeadIfAbsent`; accepted-binding path; payload read/write/copy counters all zero |
| F4 Head replace/rollback | `ReplaceHead`; accepted-binding path; payload read/write/copy counters all zero |
| F5 Head remove | `RemoveHead`; exact expected-record behavior and payload read/write/copy counters all zero |
| F6 fixed-Root create/checkpoint | `CreateFixedRootIfAbsent`; accepted-binding path; payload read/write/copy counters all zero |
| F7 fixed-Root remove | `RemoveFixedRoot`; exact expected-record behavior and payload read/write/copy counters all zero |
| F8 lifecycle outcomes | All eight required outcomes remain distinct; `OUTCOME_UNKNOWN` uses authoritative read-back |
| F9 N Heads/fixed Roots, one payload | Physical occupancy count remains one for the equal Accepted Version |
| F10 collision | Forced same ID + unequal canonical bytes rejects with no alias/reference change |
| F11 no layer-depth truth | Source/dependency audit and read/restart behavior need no parent chain |
| F12 migration namespace | Selected V2 physical namespace cannot alias legacy e497 paths during coexistence |
| C1 kill mid-publish | Prior or complete new truth; never mixed/dangling |
| C2 restart | Durable valid head recovers or corruption fails closed |
| C3 last-root race | Root/read-custody revalidation prevents premature unlink and bounded debt remains |
| C4 cancel/timeout | Scratch, FDs, workers, reservations cleaned or bounded/recoverable |

Small publication latency is a target, not a correctness waiver. Stage 4.6 is
`INCOMPARABLE` and cannot select a fence sequence or make a benchmark-winner
claim.

## 19. Stop and reopening conditions

Stop Phase 03 and reopen Phase 01 if evidence shows any of the following cannot
be fixed within R0:

- complete immutable payload closures cannot support normal reads without
  layer reconstruction;
- exact occupied-ID comparison or one physical equal-Version occupant cannot be
  implemented with finite resources;
- reference-only transitions cannot prove zero payload bytes read, written, and
  copied;
- a supported filesystem cannot provide prior-or-complete-new payload and
  reference durability under one OCC transition;
- last-root/read retirement cannot be made race-safe and bounded;
- the existing package cannot own the required transition gate without a
  dependency, process, privilege, or authority violation;
- migration requires dual writes or a permanent alternate truth; or
- a new crate/service/database/process/coordinator or different storage family
  becomes necessary for correctness.

Do not reopen Phase 01 for an exact record format, checksum, directory name,
safe fence refinement, local lock primitive, read-custody representation,
finite constant, or internal module split that satisfies this contract.

## References

- [Product PRD](../PRD.md)
- [Selected architecture](../architecture_design.md)
- [Phase 01 selection contract](../phases/01-choose-design/SPEC.md)
- [Phase 03 PRD](../phases/03-state-store/PRD.md),
  [plan](../phases/03-state-store/PLAN.md), and
  [tests](../phases/03-state-store/test-perf.md)
- [R0 Version identity](02-state-identity.md)
- [R0 algorithms and call flows](04-algorithms-and-call-flows.md)
