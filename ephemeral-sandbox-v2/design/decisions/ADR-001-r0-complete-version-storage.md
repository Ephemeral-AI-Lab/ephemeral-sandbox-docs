# ADR-001 — R0 / LayerStack-0 rewrite-in-place complete-Version storage

Date: **2026-08-04**  
Status: **`ACCEPTED_PHASE_01`**  
Scope: **Joint selected-Version ownership and storage-family decision**  
Phase 02 disposition: **`GO`**

## Decision statement

Ephemeral Sandbox V2 selects **R0**:

> Rewrite the existing `crates/sandbox-runtime/layerstack` package as the
> LayerStack-0 filesystem-native complete-Version storage. Keep authorization and
> application ordering in existing `sandbox-runtime` operation services; keep
> workspace, OverlayFS, namespace, and execution effects at their current
> owners; keep lifecycle in the existing daemon/manager owners; and add no new
> architectural boundary.

The selected storage family is part of the same decision:

- one complete immutable filesystem payload closure per Accepted Version at an
  occupied `VersionId`;
- typed roots and heads name already accepted bindings;
- bounded private staging and exact full-canonical-byte comparison whenever a
  candidate ID is occupied;
- a durable payload before any reference can name it;
- one process/filesystem-exclusive selected-Version transition gate and one
  atomic OCC head replacement;
- captured immutable reads, exact bounded retirement, bounded cleanup, and
  fail-closed recovery; and
- a temporary one-way legacy importer under a monotone generation fence, with
  no dual writable truth.

R0 is recorded in the selected whole-program
[architecture design](../../architecture_design.md). This ADR is its compact
decision record, not a replacement for that contract.

## Context

The product [hard rules](../../PRD.md#hard-rules-must-never-break) require
complete immutable filesystem values, physical reuse for equal accepted
canonical values,
reference-only operations with zero payload I/O, exact collision comparison,
one OCC Head transition, accepted-Version immutability, application-owned
MCTS/policy, runtime-neutral identity, one writable migration truth, and R0
preference unless a real failure requires expansion.

Phase 00 measured the e497 implementation and found:

- durable history currently lives in `sandbox-runtime-layerstack`;
- application ordering/composition lives primarily in `sandbox-runtime`;
- workspace, OverlayFS, namespace, and execution are runtime effects;
- manager/daemon own lifecycle;
- observability is a diagnostic reader, not authority; and
- current layer/squash/depth/merge behavior is legacy evidence, not V2
  semantics.

The Phase 01 evidence seal was the clean product worktree at:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
branch: codex/new-2.0-storage-core
HEAD:   e4974d1f9aac702b35e052629cb070c897989352
dirty:  no
drift:  none
```

Focused source checks found the current LayerStack package to be a
dependency-neutral low-level library already consumed by the relevant
application, effect, lifecycle, and diagnostic paths. It also owns the current
process/filesystem writer-lock and atomic-write/fsync primitive family. Those
placement facts are `SOURCE-VERIFIED`; the V2 algorithms and failure state
machine remain implementation hypotheses until Phases 02–03 prove them.

## Decision drivers

1. Satisfy all ten hard rules without relying on a later architecture choice.
2. Keep selected truth, application policy, and runtime effects at coherent,
   acyclic boundaries.
3. Eliminate layer-chain reconstruction, depth, squash, and merge from V2
   selected truth rather than wrapping them.
4. Make collision, stale publication, crash, recovery, reader/retirement, and
   ENOSPC behavior one coherent storage system.
5. Keep identity portable and independent of current Linux/OCI effects.
6. Preserve one writer and make migration temporary and deletable.
7. Bound scratch, memory, FDs, workers, roots/readers, recovery debt, and
   cleanup.
8. Prefer the smallest source-placeable change and require evidence before
   adding a package, process, protocol, database, or authority.

Historical Stage 4.6 was not a driver for ranking. It remains
`INCOMPARABLE` and provides no V2 performance guarantee.

## Ownership consequences

| Responsibility | Decision |
|---|---|
| Selected Version truth | `sandbox-runtime-layerstack`, rewritten |
| Pure identity | Internal `layerstack/src/identity.rs` or `identity/**` |
| Durable store | Internal `layerstack/src/store/**`, with existing filesystem/lock primitives rewritten as appropriate |
| Auth/order/OCC call orchestration | Existing `sandbox-runtime` application/operation services |
| Workspace/mount/namespace/exec | Existing runtime-effect owners |
| Lifecycle/readiness/cutover fence | Existing manager/daemon owners |
| Diagnostics/audit | Read-only observability and application-owned side channel |
| Migration decode | Temporary store-local importer calling normal V2 APIs |

The full authority and dependency rules are in
[01-ownership-and-boundaries.md](../01-ownership-and-boundaries.md).

## Storage consequences

The conceptual roles are:

```text
<LayerStack0Root>/
  versions/<VersionId>/payload/  complete immutable Accepted Version
  heads/<selector>               AcceptedBinding + HeadRevision
  roots/<kind>/<root-id>         typed durable reachability to AcceptedBinding
  staging/<transaction-id>/      bounded private unaccepted candidate
  control/...                    format, lock, generation, recovery metadata
```

The names are not a frozen Phase 03 disk spelling. Their invariants are fixed:

- reads need no parent/depth/layer reconstruction;
- roots and heads never contain or copy payload bytes;
- exact Head create/replace/remove and fixed-Root create/remove do not open the
  payload and report accepted-reference payload bytes read/written/copied as
  zero; Branch is a Head, Checkpoint is a fixed Root, and generic Root retarget
  is excluded;
- digest occupancy always causes full canonical-byte comparison;
- equal canonical bytes converge to one physical accepted payload;
- an unequal occupied ID fails as a typed collision before reference change;
- a payload is complete, durable, and immutable before it becomes reachable;
- stale expected head/revision fails without merge or rebase;
- recovery yields prior truth, complete new truth, or fail-closed readiness;
  and
- heads, roots, and bounded active read custody are the reachability sources
  for exact retirement.

## Why R0 was accepted

R0 was the mandatory first candidate and the default preference, but not a
preselected winner. It was accepted because:

- every hard rule has an architecture-level mechanism and later executable
  proof owner;
- the existing package has the required low-level dependency position and
  writer/filesystem primitive family;
- current consumers can move to neutral accepted bindings without moving
  portable truth into application or runtime-effect packages;
- no current privilege, process, recovery, resource, or scaling invariant was
  found that requires a new authority;
- the complete-Version storage family fits the same owner and removes, rather
  than preserves, legacy layer truth;
- one-way migration can call ordinary V2 admission under lifecycle fencing and
  be deleted as a unit; and
- no architecture-changing evidence gap remained open.

R0 did **not** win because of guessed LOC, package count, an appendix
scoreboard, or Stage 4.6 performance.

## Alternatives considered but not admitted

These shapes did not fix an evidenced R0 failure, so Phase 01 did not promote
them to joint candidates:

| Shape | Reason not admitted |
|---|---|
| Fuse the store into application operation code | Mixes durable truth with auth/API policy and forces neutral consumers through an application dependency. |
| Fuse the store into workspace/workspace-manager | Pulls host paths, mounts, and effect lifecycle toward portable selected truth. |
| New `sandbox-state-store` crate or facade | Adds package/API migration cost for naming cleanliness despite a suitable existing owner. |
| Store service/helper/coordinator | Adds protocol, auth, retries, queues, deployment, crash ambiguity, latency, and resource pools without a proved process/privilege need. |
| SQLite/KV metadata authority | Adds a second durability/recovery model without an evidenced transaction or indexing requirement. |
| Canonical archive requiring extraction | Adds materialization, scratch, and custody cost without fixing a hard-rule gap. |
| Chunk/object DAG | Adds graph reachability, indexing, multi-object recovery, and GC without a hard-rule need. |

These are rejected for unnecessary boundary/failure/resource cost, not merely
because R0 was the default. A future necessity case must identify the exact R0
failure and rerun the joint architecture decision.

## Correctness-rejected options

The following conflict directly with the product contract:

- layer/delta/parent-depth truth;
- per-reference payload copies;
- digest-only deduplication;
- silent stale merge or rebase;
- writable committed payloads;
- store-owned MCTS, authorization, or application policy; and
- dual-write migration or an importer that becomes permanent truth.

No performance result or implementation convenience may revive one of these
inside R0.

## Positive consequences

- Selected truth has one existing, source-placeable owner.
- Application policy and Linux runtime effects remain separated from durable
  portable Version facts.
- Reads and recovery do not depend on layer depth.
- Reference-only branches and moves have an explicit, measurable zero-payload-
  I/O path.
- One short final transition gate provides a clear OCC linearization point.
- Equal canonical Versions share one accepted physical payload after exact comparison.
- Migration reuses permanent V2 admission and has a complete deletion seam.
- No new crate, service, database, protocol, deployment, independent resource
  pool, or crash domain is introduced.

## Negative consequences and tradeoffs

- `sandbox-runtime-layerstack` is retained in name while its internal model is
  substantially rewritten; the name may be historically awkward.
- A new unique Version requires complete validation, canonicalization, hashing,
  staging, and durability; R0 does not claim delta-publication cost.
- Occupied-ID admission may require reading/comparing the complete canonical
  Version because correctness forbids digest-only reuse.
- Complete closures do not guarantee cross-Version block or file deduplication;
  two different `VersionId`s may duplicate unchanged bytes.
- Current consumers need an incremental compatibility rewrite before legacy
  layer APIs can be deleted.
- Correct local-filesystem durability, read custody, retirement, bounded
  recovery, and resource limits still require substantial Phase 03 proof.
- The selected architecture has no measured performance guarantee.

These are accepted costs of the simplest architecture that meets the frozen
correctness rules. They are not permission to weaken exact comparison,
durability, immutability, or zero-payload-I/O reference transitions.

## Deferred decisions within R0

Phase 02 selects:

- exact portable fact acceptance/rejection;
- canonical version/domain, grammar/codec, and deterministic ordering;
- digest algorithm, width, and typed `VersionId` representation;
- streaming/comparison interfaces and validation limits; and
- golden vectors and forced-collision seams.

Phase 03 selects:

- exact disk path spelling and record/checksum/version encoding;
- supported local-filesystem profile;
- safe fsync/atomic-replacement sequence;
- exact lock and internal admission-concurrency mechanics;
- finite store limits, read-custody representation, cleanup batches, and
  instrumentation.

These choices remain local only while they preserve ADR-001. The active
register is [README.md](README.md).

## Open product-owner decisions

`DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` remain
**`OWNER_DEC_OPEN`**. ADR-001 does not accept outcomes for `file_blame`, the
cutover observation duration, sessionless write/edit and related surface
semantics, or auth/revoke race ordering.

Their currently stated outcomes fit the stable seams in
[01-ownership-and-boundaries.md](../01-ownership-and-boundaries.md#open-product-decisions-and-stable-seams).
An owner requirement that moves provenance into canonical truth, permits dual
writes or in-place committed mutation, or creates joint auth/store authority
reopens Phase 01.

## Implementation constraints

- Phase 02 adds pure identity inside the existing LayerStack package and does
  not perform store I/O or product rewiring.
- Phase 03 implements the store in the same package only after Phase 02 passes.
- Later wiring cannot bypass accepted binding, exact admission, store OCC, or
  immutable read custody.
- Legacy source may coexist temporarily for compilation, but runtime writer
  fencing always preserves one writable truth.
- Every resource-controlled population has a finite owner, admission rule,
  typed failure, and deterministic/idempotent cleanup.
- Unsupported filesystem semantics, corruption, dangling truth, ambiguity, or
  excessive recovery debt fail closed.
- The new architectural-boundary count remains **zero**.

## Reopening conditions

Reopen Phase 01 instead of locally mutating ADR-001 when evidence requires a
change to:

- the selected Version owner, application/effect ownership, or dependency
  direction;
- the complete-Version filesystem storage family or portable/runtime boundary;
- the number of selected-Version writers or OCC linearization points;
- occupied-ID collision, durability, crash recovery, reader/retirement, or
  cleanup semantics;
- the one-writable-truth migration/deletion model; or
- the zero-new-boundary decision.

Concrete triggers include source drift that invalidates the placement,
inability to define bounded portable facts, inability to prove the filesystem
durability or last-root/read race on a supported profile, a real multi-host or
privilege requirement, or an owner decision that exceeds its stable seam.

Internal file naming, a compatible codec/hash, finite constants, safe fence
refinement, and test instrumentation do not reopen architecture.

## References

- [Product PRD](../../PRD.md)
- [Phase 00 evidence](../../phases/00-freeze-rules/SPEC.md)
- [Phase 01 selection contract](../../phases/01-choose-design/SPEC.md)
- [Phase 01 completed plan](../../phases/01-choose-design/PLAN.md)
- [Selected architecture](../../architecture_design.md)
- [Ownership and boundaries](../01-ownership-and-boundaries.md)
- [Decision register](README.md)
