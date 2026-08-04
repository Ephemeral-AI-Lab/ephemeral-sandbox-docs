# Ephemeral Sandbox 2.0 migration

> **Historical plan — not the Phase 01+ execution contract.** This package's
> selected CDC/CAS history, object/ref layout, phase sequence, API model, and
> `/eos` tree predate and conflict with the current LayerStack-0 R0 selection.
> Use the V2 [selected architecture](../../ephemeral-sandbox-v2/architecture_design.md)
> and [compatibility map](../README.md). Preserve this package as evidence; do
> not implement from it or translate its “Phase 1” into current V2 Phase 01.
>
> Abstract and dependency order for the public Ephemeral Sandbox **0.2.x**
> roadmap. In this directory, “2.0” is an internal migration name; it does not
> change the public release numbering.

| Field | Decision |
| --- | --- |
| Status | Proposed; evidence-gated |
| Main outcome | A durable checkpoint graph over fast, native sandbox execution |
| Phase 1 | Replace LayerStack history storage with a portable CDC/CAS-backed design |
| Phase 2 | Add branch, checkpoint, rollback, bounded rollout, and MCTS |
| Phase 3 | Reuse the same state plane through Firecracker and WASI execution adapters |
| Execution path | Backend adapters: native OCI/Linux, Firecracker microVM, or capability-scoped WASI |
| Phase 1 qualification | One pinned Ubuntu 24.04 Docker environment |

## 1. The migration in one sentence

Ephemeral Sandbox 2.0 first makes LayerStack checkpoints portable, compact,
recoverable, and independent of a running sandbox; it then uses those
checkpoints as the nodes of a durable branch graph that can activate a bounded
number of isolated sandboxes for multiagent work and MCTS rollouts; finally, it
reuses the same state and graph planes through OCI/Linux, Firecracker, and WASI
execution adapters.

The organizing principle is:

> **Persist checkpoint nodes; rent execution only while work is running.**

## 2. Target product model

```mermaid
flowchart TB
    C["Multiagent, RL, or MCTS controller"] --> G["SandboxGroup"]
    G --> N["Immutable SandboxNodes"]
    N --> S["LayerStack roots"]
    S --> H["Portable history and metadata"]
    S --> A["Backend-local workspace projection"]
    N --> E["Bounded ExecutionAttempts"]
    E --> O["OCI/Linux · Firecracker · WASI adapters"]
    O --> R["Checkpoint, evaluate, promote, merge, or prune"]
    R --> G
```

The durable graph may be large. Only selected nodes become live sandboxes.
A running container, mount, process tree, or workspace session is an execution
detail, not the durable identity of a branch.

## 3. Core abstractions

| Abstraction | Role in 2.0 |
| --- | --- |
| `RootId` | Portable identity of one immutable logical filesystem tree |
| `AttributionRootId` | Separate portable blame snapshot selected atomically beside a content root |
| `SandboxGroup` | Owns one checkpoint graph and its canonical accepted node |
| `SandboxNode` | Immutable, selectable branch or checkpoint in the graph |
| `ExecutionAttempt` | Temporary activation of one node in one isolated sandbox |
| `Evaluation` | Versioned tests, review, reward, and evidence for a sealed result |
| `Lease` | Protects roots and active work from reclamation |
| `Checkpoint` | Atomically sealed filesystem state, logical state, and provenance |
| `Promotion` | Explicit compare-and-swap advance of the group’s canonical node |
| `Workspace projection` | Verified backend-local representation used for one execution attempt |
| `Portable history` | CDC/CAS-backed retained history used outside the execution hot path |

Three distinctions are essential:

- A **fork** creates branch intent from an immutable node; it does not clone a
  running process or duplicate the parent workspace payload.
- An **activation** creates a temporary sandbox with its own writable state and
  isolation boundary.
- A **checkpoint** seals the result as a new immutable node. It never mutates
  its parent.

## 4. Three main phases

### Phase 1 — LayerStack 2.0 storage

**Goal:** replace whole-file historical LayerStack retention with a portable,
space-efficient checkpoint store while preserving the current native execution
experience.

Phase 1 introduces:

- portable, versioned content and attribution identities;
- CDC/CAS-backed retained history;
- small atomic refs and one common recoverable-operation protocol;
- verified native materialization for active OCI/Linux workspaces;
- immutable publication with OCC and idempotent recovery;
- durable leases, blame, provenance, retention, and garbage collection;
- compatibility with existing LayerStack roots and workspace-session APIs; and
- a unified baseline that measures materialization, mount/remount, squash,
  command, PTY, publication, recovery, memory, and total physical space.

Phase 1 preserves:

- ordinary native files under `/workspace`;
- the current OverlayFS-based OCI/Linux command path;
- existing namespace, command, PTY, stdin, cancellation, and child-reaping
  behavior;
- one private writable upper per active execution; and
- no target-image helper, FUSE filesystem, external database service, or
  required reflink capability.

CDC/CAS is a history and checkpoint representation. It does not replace
OverlayFS, and it does not reconstruct chunks during ordinary command or PTY
I/O.

**Phase 1 exit:** an old or new immutable root can be published, leased,
recovered, garbage-collected, and materialized correctly; warm native execution
remains close to the existing LayerStack baseline; and the storage design has
bounded memory and no correctness dependence on cached state.

#### Complete Phase 1 `/eos` tree

This is the full migration-time ownership structure, not only the LayerStack
subtree. Directories are created only on first use. Bracketed v1 entries remain in
their existing locations through the rollback window; they are not a new legacy
namespace. The canonical field, durability, and deletion rules are in the
[Phase 1 storage contract](phase%201/implementation/layerstack_storage_contract.md#4-complete-eos-ownership-and-storage-tree).

```text
/eos/
├── layer-stack/                                      LayerStack durable owner
│   ├── .storage-writer.lock                          brief cross-process commit fence
│   ├── CONTROL                                       format/authority/retirement fence
│   ├── objects/
│   │   ├── loose/<kind>/<digest-prefix>/<typed-id>   canonical immutable logical bytes
│   │   ├── packs/<pack-id>.pack                      optional immutable compaction output
│   │   └── locators/
│   │       ├── <run-id>.sst                          immutable non-loose location map
│   │       └── CURRENT                               selected locator-run set
│   ├── refs/
│   │   ├── heads/<branch-id>                         mutable branch visibility + OCC
│   │   ├── checkpoints/<checkpoint-id>               named immutable-snapshot retention
│   │   ├── pins/<pin-id>                             explicit policy retention
│   │   └── leases/<lease-id>                         active snapshot/location/generation protection
│   ├── operations/<operation-id>/
│   │   ├── STATE                                     sole recovery/idempotency record
│   │   └── work/                                     bounded private spill/build/mark/trash
│   ├── materializations/<materialization-id>/
│   │   ├── CURRENT                                   selected immutable native generation
│   │   └── generations/<generation>/
│   │       ├── MANIFEST                              verified generation description
│   │       └── carriers/<carrier-id>/...             backend-native immutable tree/carrier
│   ├── gc/
│   │   └── CURRENT                                   active GC operation pointer
│   ├── manifest.json                                 [v1 compatibility window only]
│   ├── workspace.json                                [v1 compatibility window only]
│   ├── base/<base-id>/...                            [v1 compatibility window only]
│   ├── layers/<layer-id>/...                         [v1 compatibility window only]
│   ├── staging/<layer-id>.staging/...                [v1 compatibility window only]
│   └── .layer-metadata/<layer-id>.{digest,bytes}     [v1 compatibility window only]
├── workspace/                                        WorkspaceManager runtime owner
│   ├── manager.json                                  restart recovery catalog
│   ├── .export/<spool-id>                            bounded export scratch
│   └── <workspace-session-id>/
│       ├── upper/                                    unpublished session writes
│       ├── work/                                     OverlayFS kernel work directory
│       └── executions/<execution-id>/
│           └── transcript.log                        command/PTY session scratch
├── storage/                                          non-LayerStack service storage
│   ├── file_auditability/...                         audit service owner
│   └── workspace_recovery/...                        failed-cleanup recovery artifacts
└── runtime/                                          daemon runtime owner
    └── daemon/
        ├── runtime.sock                              local IPC
        └── runtime.pid                               daemon lifecycle
```

There is no durable `/eos/legacy`, `/eos/layer-stack/refs/legacy`, or
`/eos/namespace_execution`. `/workspace` is a per-session mount, not durable `/eos`
storage. LayerStack GC owns only `/eos/layer-stack`.

### Phase 2 — SandboxGraph, checkpointing, and MCTS

**Goal:** make immutable LayerStack checkpoints the durable branching model for
multiagent development, parallel rollouts, and MCTS.

Phase 2 introduces:

- durable groups, nodes, execution attempts, evaluations, and artifacts;
- branch, checkpoint, activate, retry, rollback, merge, promote, and prune
  workflows;
- one separate isolated sandbox for each active branch;
- a bounded, preferably prewarmed sandbox pool;
- locality-aware reuse of hot LayerStack materializations;
- durable rollout, frontier, policy, reward, and trajectory records; and
- idempotent evaluation and exactly-once accepted MCTS backpropagation.

For MCTS, the durable tree is not a tree of resident containers. Inactive nodes
remain checkpoint records on disk. The scheduler activates only the frontier
allowed by the configured concurrency and resource limits.

Rollback means abandoning or releasing the current attempt and activating a
chosen immutable node. Exact process-memory time travel is not part of the
portable 2.0 core.

**Phase 2 exit:** a large durable graph can run through a fixed-size sandbox
pool; siblings remain isolated; stale promotion cannot overwrite newer work;
retries cannot double-count evaluation or reward; and recovery preserves
frontier leases and selectable nodes.

### Phase 3 — Firecracker and WASI execution

**Goal:** run the same immutable roots and SandboxGraph attempts through
Firecracker microVMs and WebAssembly/WASI without creating backend-specific
storage or checkpoint truth.

Phase 3 reuses without modification:

- the selected CDC/CAS design and versioned root identity;
- typed immutable content/attribution objects, refs, native materializations, packs,
  and physical locators;
- publication, OCC, leases, attribution, common operations, recovery, and garbage
  collection; and
- SandboxGroup, node, attempt, evaluation, promotion, and rollout semantics.

Phase 3 replaces only the execution-facing adapters:

- the current OCI/Linux OverlayFS workspace projection;
- Linux namespace process execution; and
- their mount, process, stream, cancellation, and lifecycle implementations.

The Firecracker adapter prepares an isolated microVM-local workspace and
executes through a guest-control channel. Firecracker memory snapshots may be
worker-local startup accelerators, but never become LayerStack checkpoint
identity or replace filesystem publication.

The WASI adapter exposes a capability-scoped workspace and command/component
execution. It preserves unsupported Linux metadata in LayerStack and reports
backend capability limits explicitly rather than silently claiming Linux,
signal, or PTY parity.

**Phase 3 exit:** one content/attribution snapshot can be activated, changed, checkpointed,
recovered, and rolled back through OCI/Linux, Firecracker, or WASI; the same
durable operation and retention rules apply; backend-local failure cannot
corrupt or advance a root; and inactive nodes require no resident executor.

See the [Phase 3 overview](phase%203/index.md).

## 5. Dependency order

| Order | Milestone | Depends on | Main proof |
| ---: | --- | --- | --- |
| 0 | Phase 1 Stages 00–02: baseline, scratch ownership, v2 evidence | Current runtime | Existing behavior is reproducible and accepted v2 bytes remain readable |
| 1 | Phase 1 Stage 03: corrected identity and private publication | 0 plus owner amendment | Bounded content/attribution graphs, refs, OCC, and recovery work end to end |
| 2 | Phase 1 Stage 04: materialization and strict activation | 1 | Cold reconstruction and exact-generation session leases are correct |
| 3 | Phase 1 Stage 05: retention, packs, GC, and squash | 2 | Physical maintenance and deletion are safe under concurrency |
| 4 | Phase 1 Stage 06: reversible candidate authority | 3 | Exactly one public writer can cut over and roll back |
| 5 | Phase 1 Stage 07: qualification/default/retirement | 4 | Default and destructive v1 retirement have separate evidence gates |
| 6 | Introduce `SandboxGroup` and immutable nodes | 5 | Branches are durable without resident sandboxes |
| 7 | Activate nodes in separate bounded sandboxes | 6 | Sibling isolation and hot-root reuse hold across containers |
| 8 | Add checkpoint, rollback, merge, and promotion workflows | 7 | No lost updates or ambiguous branch state |
| 9 | Add rollout and MCTS coordination | 8 | Retry-safe evaluation and backpropagation survive failure |
| 10 | Freeze backend-neutral workspace and execution contracts | 9 | Existing OCI/Linux behavior fits behind adapters without changing roots |
| 11 | Add the Firecracker adapter | 10 | The same root executes and checkpoints through a microVM |
| 12 | Add the WASI adapter | 10 | The same root executes and checkpoints through declared capabilities |
| 13 | Prove cross-backend equivalence and routing | 11, 12 | Backend changes preserve durable truth and schedule only compatible work |

This order creates one hard boundary:

> Phase 2 may design its schema in parallel, but it must not depend on the new
> storage path until Phase 1 has proven immutable roots, leases, OCC, recovery,
> blame, and native-path performance.

Phase 3 has the same boundary: adapter design may begin earlier, but Firecracker
and WASI runtime integration must not fork the LayerStack format or bypass the
proven Phase 1 and Phase 2 contracts.

## 6. What can run in parallel

| Lane | When it may start | Constraint |
| --- | --- | --- |
| Baseline and benchmark verification | Immediately | Establishes the comparison contract before optimization claims |
| LayerStack storage implementation | After root and compatibility contracts freeze | Rust implementation; no public graph dependency |
| SandboxGraph schema design | During Phase 1 | Design only until Phase 1 semantics stabilize |
| SandboxGraph runtime | After Phase 1 exit | Must consume the proven root, lease, OCC, and recovery contracts |
| MCTS scheduler and evaluator design | Late Phase 1 or early Phase 2 | Runtime integration waits for durable nodes and idempotency |
| MCTS execution | After bounded sandbox activation | Must not create one resident sandbox per durable node |
| Backend adapter contract | During late Phase 2 | Design only until root, attempt, evaluation, and recovery semantics freeze |
| Firecracker adapter | After the backend contract freezes | Reuses the state plane; requires a KVM-capable Linux worker |
| WASI adapter | After the backend contract freezes | Reuses the state plane; capability differences must be explicit |
| Cross-backend routing | After both adapters reach conformance | Must preserve root identity and reject unsupported workloads |

The benchmark lane should finish before approach results are judged. If an
implementation finishes first, its evaluation clock starts only when the
shared baseline and verifier are ready.

## 7. Storage and performance posture

The product optimizes two different lifecycles across every executor:

- **Hot execution:** keep current, active, recently used, and frontier roots in
  native mount-ready form.
- **Cold history:** retain reusable content and metadata compactly, and
  materialize it only when a cold node becomes active.

Total storage must include native hot roots, retained history, every live
private upper, staging, and metadata. CAS bytes alone are never the total.
Near-one-current-copy storage is a settled target after squash, lease release,
and garbage collection—not a promise during active parallel edits or
publication.

Priority order for evaluation:

1. correctness, isolation, OCC, leases, blame, and recovery;
2. materialization, mount/remount, squash, command, and PTY speed;
3. total physical storage;
4. bounded memory and operational simplicity;
5. portability expansion.

No execution backend may select a different CDC algorithm or packed layout.
The Phase 1 choice remains versioned and shared by OCI/Linux, Firecracker, and
WASI.

## 8. Migration posture

The migration is additive and evidence-gated:

1. read existing roots through a compatibility path;
2. publish complete private 2.0 content/attribution snapshots through the final
   operation/ref protocol while v1 remains authoritative;
3. optionally compare v1 with a hidden candidate head without a shadow-specific
   storage format;
4. qualify strict candidate materialization, retention, GC, and rollback;
5. enable one fenced 2.0 publication authority for opted-in groups;
6. keep complete v1 read/write rollback through the compatibility window; and
7. retire exact v1 paths only after usage, evacuation, and recovery evidence show
   it is safe.

The existing workspace-session API becomes a compatibility execution handle.
New functionality belongs to the graph model so that the compatibility layer
does not become a second architecture.

## 9. Explicit non-goals for this migration

- CRIU or instruction-exact process rollback;
- nested workspace sessions as the public branching model;
- one permanently resident container or VM per durable node;
- FUSE, JuiceFS, a CAS-backed VFS, or per-read CAS reconstruction;
- required reflink, host-kernel customization, loop devices, or target-image
  utilities in the shared LayerStack path;
- an external database service or SQLite dependency in the storage core;
- automatic semantic conflict resolution;
- distributed or remote CAS in the first implementation;
- Firecracker VM-memory snapshots as LayerStack checkpoint truth;
- instruction-exact process migration between OCI, Firecracker, and WASI;
- implicit Linux PTY, signal, namespace, or syscall parity on WASI;
- production Firecracker or WASI execution in the initial Ubuntu 24.04
  qualification; and
- broad host or image matrices before the initial Docker path is proven.

The logical root format remains backend-neutral so Firecracker and WASI
qualification can be added without changing checkpoint identity.

## 10. Source authority and superseded direction

The current source of product intent is the public roadmap:

- [Overview](https://ephemeral-sandbox.com/roadmap)
- [System design](https://ephemeral-sandbox.com/roadmap/system-design)
- [CDC storage](https://ephemeral-sandbox.com/roadmap/content-defined-chunking)
- [Product specification](https://ephemeral-sandbox.com/roadmap/product-spec)
- [Delivery plan](https://ephemeral-sandbox.com/roadmap/delivery-plan)

The local [0.2.0 PRD](../../0.2.0/PRD.md) remains useful supporting context.
Where its release slicing differs from the newer public roadmap, the public
roadmap’s dependency order wins.

The older [reflink-backed LayerStack 2.0 proposal](../layerstack_2.0/README.md)
is not the implementation authority for this migration. It is retained as
historical research and may inform correctness or recovery work, but required
reflink behavior and SQLite-backed design do not define the new portable
storage foundation.

## 11. Follow-on specifications

This index intentionally stops at the abstraction and migration order. Phase 1 is
defined by its [overview](phase%201/index.md),
[implementation plan](phase%201/implementation/index.md), and
[canonical storage contract](phase%201/implementation/layerstack_storage_contract.md).
The remaining follow-on documents separately define:

1. Phase 2 SandboxGraph and checkpoint specification;
2. Phase 2 bounded sandbox activation specification;
3. Phase 2 rollout and MCTS specification;
4. [Phase 3 portable execution overview](phase%203/index.md);
5. Phase 3 backend-neutral adapter and filesystem-semantics specification;
6. Phase 3 Firecracker adapter specification;
7. Phase 3 WASI adapter specification; and
8. production migration, rollback, and observability specification.

No Phase 2 or Phase 3 implementation should begin from this overview alone.
