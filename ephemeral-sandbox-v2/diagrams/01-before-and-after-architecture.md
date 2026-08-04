# Before and after — selected R0 architecture

Date: **2026-08-04**
Status: **`LOCKED_PHASE_01` architecture diagram**
Evidence base: product source at
`e4974d1f9aac702b35e052629cb070c897989352`
Selected result: **R0 — LayerStack-0 rewrite-in-place filesystem-native
complete-Version storage**

## Authority and purpose

This document is a visual companion to the selected root
[architecture design](../architecture_design.md) and the detailed
[ownership contract](../design/01-ownership-and-boundaries.md). It contrasts
the measured e497 ownership shape with the selected R0 target so later phases
can see what remains in place, what is rewritten, and which dependencies are
forbidden.

Authority descends from the product [PRD](../PRD.md), Phase 00
[evidence](../phases/00-freeze-rules/SPEC.md), Phase 01
[selection contract](../phases/01-choose-design/SPEC.md), and the selected root
[architecture](../architecture_design.md). This diagram does not select a new
owner, storage family, codec, digest, disk record, or filesystem fence
sequence. If shorthand here conflicts with those sources, the higher-authority
text wins.

## Legend

```text
[SOURCE-VERIFIED e497]  Measured current package/ownership fact at the sealed base
[SELECTED R0]           Binding Phase 01 architecture decision
[DEFERRED P02/P03]      Exact implementation detail owned by Phase 02 or Phase 03

  A --> B               Allowed call/dependency or responsibility flow
  A ..> B               Read-only, temporary, or non-authoritative flow
  A -X-> B              Forbidden authority/dependency flow
  [KEEP]                Existing responsibility boundary remains
  [REWRITE]             Existing source home remains; its permanent semantics change
  [DELETE V2 CORE]      Legacy concept cannot remain V2 selected truth
  [ADD INTERNAL]        Module inside the existing owner; not a new architecture boundary
```

The left/e497 panels are evidence about the current implementation, not V2
semantics. The right/R0 panels are selected design, not a claim that V2 has
already passed executable qualification.

## Panel A — system architecture before and after

```text
+-------------------------------------------------------------------------+
| CURRENT e497 -- SOURCE-VERIFIED                                         |
|                                                                         |
|  CLI / MCP / manager clients                                            |
|              |                                                          |
|              v                                                          |
|  +---------------------------+                                          |
|  | sandbox-daemon / manager  |                                          |
|  | daemon: auth + dispatch   |                                          |
|  | manager: fleet lifecycle |                                          |
|  +-------------+-------------+                                          |
|                |                                                        |
|                v                                                        |
|  +---------------------------+                                          |
|  | sandbox-runtime           |                                          |
|  | operation composition +   |                                          |
|  | relevant request ordering |                                          |
|  +-------------+-------------+                                          |
|                |                                                        |
|           +----+------------------------------+                         |
|           |                                   |                         |
|           v                                   v                         |
|  +---------------------------+      +-------------------------------+    |
|  | sandbox-runtime-layerstack|      | workspace / overlay /         |    |
|  | durable history home      |      | namespace / execution         |    |
|  | manifest + layers         |      | live Linux effects            |    |
|  | parent/depth/project      |      | mounts and host paths          |    |
|  | publish/merge/squash      |      +-------------------------------+    |
|  | leases + writer lock      |                                           |
|  +---------------------------+                                           |
|                                                                         |
|  observability query/telemetry ..> layerstack diagnostic/read-only      |
|                                                                         |
|  CURRENT FACT: durable history is LayerStack-style.                     |
|  WARNING: current merge/squash/layer behavior is evidence, not V2 law.  |
+-------------------------------------------------------------------------+

                              PHASE 01 R0
                                  |
                                  v

+-------------------------------------------------------------------------+
| SELECTED R0 -- ARCHITECTURE DECISION                                    |
|                                                                         |
|  CLI / MCP / manager clients                                            |
|              |                                                          |
|              v                                                          |
|  +---------------------------+                                          |
|  | daemon / manager [KEEP]   |                                          |
|  | lifecycle + readiness     |                                          |
|  +-------------+-------------+                                          |
|                |                                                        |
|                v                                                        |
|  +---------------------------+                                          |
|  | sandbox-runtime [KEEP]    |                                          |
|  | application authority    |                                          |
|  | auth/order/expected head |                                          |
|  | candidate orchestration  |                                          |
|  +-------------+-------------+                                          |
|                |                                                        |
|           +----+------------------------------+                         |
|           |                                   |                         |
|           v                                   v                         |
|  +---------------------------+      +-------------------------------+    |
|  | LayerStack-0 [REWRITE]    |      | effects [KEEP]                |    |
|  | V2 Version storage        |<-----| portable candidate facts only |    |
|  | Versions + bindings       |      | workspace / overlay / mount   |    |
|  | typed roots + heads       |      | namespace / exec / host paths |    |
|  | one OCC transition gate   |      +-------------------------------+    |
|  | recovery + retirement     |                                           |
|  +-------------+-------------+                                           |
|                |                                                        |
|                v                                                        |
|  +---------------------------+                                          |
|  | identity [ADD INTERNAL]   |                                          |
|  | canonical bytes + VersionId |                                          |
|  +---------------------------+                                          |
|                                                                         |
|  observability [KEEP, READ] ..> layerstack diagnostic/read-only         |
|                                                                         |
|  SELECTED: complete immutable payload truth; roots/heads are references. |
|  DELETE V2 CORE: layer parent/depth/squash/merge/delta truth.            |
|  NEW ARCHITECTURAL BOUNDARIES: zero.                                    |
+-------------------------------------------------------------------------+
```

The package name `sandbox-runtime-layerstack` survives because it is the
existing source-placeable low-level owner. Its LayerStack truth model does not
survive. “Rewrite in place” is ownership continuity plus semantic replacement,
not a compatibility wrapper around layers.

## Panel B — authority split after R0

```text
                      APPLICATION AUTHORITY [KEEP]
             +-------------------------------------------+
             | authorize request                         |
             | order request/revoke                      |
             | capture expected HeadRecord               |
             | (AcceptedBinding, HeadRevision)            |
             | orchestrate candidate and store call      |
             +--------------------+----------------------+
                                  |
                                  | typed request + expected head
                                  v
             +-------------------------------------------+
             | LAYERSTACK-0 VERSION AUTHORITY [REWRITE]  |
             | crates/sandbox-runtime/layerstack         |
             |                                           |
             | admit exact content -> AcceptedBinding    |
             | publish roots/heads under one OCC gate    |
             | recover/read/retire immutable payloads    |
             +--------------------+----------------------+
                                  ^
                                  | complete portable candidate facts
                                  |
             +--------------------+----------------------+
             | RUNTIME-EFFECT AUTHORITY [KEEP]           |
             | workspace / overlay / namespace / exec    |
             | writable generation, mount, capture       |
             | host paths and process-local custody      |
             +-------------------------------------------+

  application -X-> durable payload/root/head path writes
  effects     -X-> portable identity policy or selected head writes
  store       -X-> auth, MCTS, mounts, namespace, exec, workspace mutation
  identity    -X-> store I/O, runtime effects, auth, migration, recovery
  diagnostics -X-> selected-Version publication or truth reconstruction
```

Authorization and OCC are deliberately separate. The application decides
whether an operation may be attempted; the store rereads the expected head
under its exclusive gate and alone decides whether the selected reference
transitions.

## Panel C — source disposition

```text
crates/sandbox-runtime/layerstack/
|
+-- Cargo.toml                         [KEEP owner/dependency position]
+-- src/lib.rs                         [REWRITE narrow V2 API]
+-- src/model/**                       [REWRITE V2 facts/bindings/records]
+-- src/identity.rs or identity/**     [ADD INTERNAL in Phase 02]
+-- src/store/**                       [ADD INTERNAL in Phase 03]
+-- src/storage/{fs.rs,lock.rs}        [REWRITE primitive family]
+-- src/workspace_base/**              [REWRITE or temporary import]
+-- src/stack/**                       [DELETE from permanent V2 path]
    +-- layers / parents / depth       [DELETE V2 CORE]
    +-- merge / squash / delta truth   [DELETE V2 CORE]
    +-- durable layer leases           [DELETE or replace at selected seam]

crates/sandbox-runtime/operation       [KEEP application; REWRITE wiring]
crates/sandbox-runtime/workspace       [KEEP runtime effects]
crates/sandbox-runtime/overlay         [KEEP runtime effects]
crates/sandbox-runtime/namespace-*     [KEEP runtime effects]
crates/sandbox-daemon                  [KEEP composition/lifecycle]
crates/sandbox-manager                 [KEEP lifecycle/cutover fence]
crates/sandbox-observability/*         [KEEP read-only diagnostics]

store-local legacy_import              [ADD TEMPORARILY, then DELETE]
new crate/service/database/coordinator [NOT SELECTED]
```

Temporary legacy source may remain while consumers are migrated, but it cannot
remain writable selected truth beside V2.

## Panel D — one-writer migration boundary

```text
                         lifecycle generation fence
                                      |
                                      v
  legacy writable  --drain/fence-->  legacy READ-ONLY
                                           |
                                           | one selected legacy view
                                           v
                                  .-------------------.
                                  : temporary importer:  [TEMPORARY]
                                  '---------+---------'
                                            |
                                            | normal portable facts +
                                            | ordinary V2 APIs
                                            v
                                  +-------------------+
                                  | R0 store WRITABLE |
                                  | sole V2 truth     |
                                  +-------------------+

  legacy writable  -X-------------------------------> R0 writable
                      no interval with two writable truths
```

The temporary importer decodes legacy input; it does not own a second V2
representation. Permanent identity/store code must not depend on importer
types. `DEC-011` may change when compatibility is deleted, never the one-writer
fence.

## Walkthrough

1. **Current evidence.** At e497, LayerStack is the durable history home;
   `sandbox-runtime` composes product operations; workspace/overlay/namespace/
   exec packages own Linux effects; daemon/manager own lifecycle; observability
   reads diagnostics.
2. **R0 keeps the useful ownership boundaries.** Application authorization and
   ordering, runtime effects, lifecycle, and diagnostics do not move into the
   store.
3. **R0 rewrites the durable owner.** The existing LayerStack package becomes
   the sole V2 selected-Version owner. Layers, depth, merge, and squash cease to
   be permanent selected truth.
4. **Pure identity remains internal.** Phase 02 adds canonicalization and
   `VersionId` derivation under the same package without giving identity durable
   I/O or application authority.
5. **Phase 03 implements storage under one authority.** Candidate preparation
   may be concurrent and outside the final gate, but accepted references and
   final retirement are controlled by the store.
6. **Runtime effects supply candidates, not identity brands.** Workspace and
   Linux owners may supply complete portable facts; host paths, mounts,
   namespaces, and runtime handles never enter canonical identity.
7. **Migration crosses a temporary seam.** The importer calls ordinary V2
   admission after legacy writes are fenced, then is deleted after the
   owner-selected observation window.

## Architecture invariants

- `sandbox-runtime-layerstack` is the only selected-Version truth owner.
- Application services own authorization, request/revoke ordering, expected-
  head capture, and store-call orchestration; they cannot bypass store OCC.
- Workspace, OverlayFS, namespace, and exec owners retain live effects and
  cannot mutate committed payloads or durable references directly.
- Observability and audit projections are diagnostic/side-channel readers, not
  truth or write authority.
- MCTS, rollout, winner choice, API policy, and auth policy stay outside the
  store.
- One Accepted Version at an occupied `VersionId` has one complete immutable payload closure;
  selected reads require no layer reconstruction.
- LayerStack-0 has one process/filesystem-exclusive selected-Version transition
  authority and one head OCC linearization point.
- Portable identity excludes Docker, OCI, OverlayFS, mounts, namespaces, host
  paths, workspaces, sessions, leases, processes, and policy facts.
- Migration never has two writable selected-Version truths and remains deletable.
- R0 adds zero crate/service/process/facade/database/coordinator boundaries.

## Selected versus deferred

| Subject | Status | Owner/constraint |
|---|---|---|
| Selected Version truth owner and dependency direction | `LOCKED_PHASE_01` | Existing `sandbox-runtime-layerstack`, rewritten; consumers depend downward on it. |
| Application/effect/lifecycle/diagnostic boundaries | `LOCKED_PHASE_01` | Existing owners retained as shown above. |
| Complete immutable payload + accepted binding + root/head storage family | `LOCKED_PHASE_01` | Phase 03 implements without choosing another family. |
| One writer/OCC point and no silent merge/rebase | `LOCKED_PHASE_01` | Store-owned final transition. |
| Portable/runtime-private boundary | `LOCKED_PHASE_01` | Phase 02 defines exact portable profile inside this boundary. |
| Exact canonical fact grammar, codec, digest, limits | `SELECT_IN_PHASE_02` | Must be pure, deterministic, complete, bounded, and exactly comparable. |
| Exact on-disk spelling, record format, checksum, lock/fence sequence | `SELECT_IN_PHASE_03` | Must prove payload-before-reference durability and prior-or-complete-new recovery. |
| Read-custody representation and finite store constants | `SELECT_IN_PHASE_03` | Must close last-root/read race and bound all populations. |
| `DEC-001`, `DEC-011`, `DEC-017`, `DEC-018` | `OWNER_DEC_OPEN` | Stable seams are defined; no outcome is accepted here. |
| V2 correctness result; performance verdict | `NOT_RUN`; `TARGET_UNSELECTED` | Stage 4.6 remains `INCOMPARABLE`; Phase 06 owns matched qualification after an owner-approved target exists. |

## Verification mapping

| Architecture claim | Required later evidence |
|---|---|
| Identity is pure and runtime-neutral | Phase 02 I1–I7, forbidden-field/type/dependency audit |
| Complete immutable payload and one equal-Version occupant | Phase 03 F1, F9, F11 plus physical-count and source audits |
| Exact collision handling | Phase 02 forced-ID seam and Phase 03 F10 at every occupied-ID ingress |
| One OCC transition; stale changes no head | Phase 03 F2 and concurrency/linearization histories |
| All five accepted-reference operations perform zero payload I/O | Phase 03 F3–F7 counters/syscall evidence and Phase 06 integration qualification |
| Captured reads and exact retirement are race-safe | Phase 03 C3 and reader/head-move/last-root histories |
| Prior-or-complete-new durability and bounded cleanup | Phase 03 C1, C2, C4 crash-prefix, restart, cancellation, ENOSPC, and resource-bound tests |
| Consumers preserve authority/dependency direction | Phase 04 operation wiring and dependency/source audits |
| Migration has one writable truth and is deletable | Phases 05–08 writer inventory, generation-fence, retry, and no-reference deletion build |
| No new architecture boundary | Phase 02/03 package/dependency checks and review of every proposed addition against an exact R0 failure |

## Reopening conditions

Stop the owning phase and reopen Phase 01 if evidence requires:

- moving selected truth, application authority, or runtime-effect custody to a
  different owner;
- adding a selected-Version writer, OCC point, crate/service/process/database/
  coordinator, independent crash domain, or privilege boundary;
- importing runtime-private facts into identity or making identity depend on
  layer reconstruction;
- replacing complete immutable filesystem closure truth with a layer chain,
  archive-extraction truth, object DAG, database authority, or another storage
  family;
- weakening exact occupied-ID comparison, payload-before-reference durability,
  captured reads, zero-payload-I/O references, or bounded recovery/retirement;
- allowing dual writable legacy/V2 truth or a permanent importer dependency;
  or
- accommodating an owner decision that exceeds its documented stable seam.

Do not reopen for internal module names, a compatible Phase 02 codec/digest,
finite constants, a safe Phase 03 fence refinement, or instrumentation that
preserves all selected boundaries.

## Links

- [Product PRD and hard rules](../PRD.md#hard-rules-must-never-break)
- [Selected architecture](../architecture_design.md)
- [R0 ownership and boundaries](../design/01-ownership-and-boundaries.md)
- [R0 Version identity](../design/02-state-identity.md)
- [LayerStack-0 storage](../design/03-state-store.md)
- [Algorithms and call flows](../design/04-algorithms-and-call-flows.md)
- [Concurrency, durability, and recovery](../design/05-concurrency-durability-recovery.md)
- [Source and implementation map](../design/09-source-and-implementation-map.md)
- [Verification matrix](../design/10-verification-matrix.md)
