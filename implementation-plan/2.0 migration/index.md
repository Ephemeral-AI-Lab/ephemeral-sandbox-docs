# Ephemeral Sandbox 2.0 migration

> Abstract and dependency order for the public Ephemeral Sandbox **0.2.x**
> roadmap. In this directory, “2.0” is an internal migration name; it does not
> change the public release numbering.

| Field | Decision |
| --- | --- |
| Status | Proposed; evidence-gated |
| Main outcome | A durable checkpoint graph over fast, native sandbox execution |
| Phase 1 | Replace LayerStack history storage with a portable CDC/CAS-backed design |
| Phase 2 | Add branch, checkpoint, rollback, bounded rollout, and MCTS |
| Execution path | Native OCI/Linux filesystem, command, PTY, and stdin behavior |
| Initial qualification | One pinned Ubuntu 24.04 Docker environment |

## 1. The migration in one sentence

Ephemeral Sandbox 2.0 first makes LayerStack checkpoints portable, compact,
recoverable, and independent of a running sandbox; it then uses those
checkpoints as the nodes of a durable branch graph that can activate a bounded
number of isolated sandboxes for multiagent work and MCTS rollouts.

The organizing principle is:

> **Persist checkpoint nodes; rent execution only while work is running.**

## 2. Target product model

```mermaid
flowchart TB
    C["Multiagent, RL, or MCTS controller"] --> G["SandboxGroup"]
    G --> N["Immutable SandboxNodes"]
    N --> S["LayerStack roots"]
    S --> H["Portable history and metadata"]
    S --> A["Native materialization"]
    N --> E["Bounded ExecutionAttempts"]
    E --> O["Separate isolated sandboxes"]
    O --> R["Checkpoint, evaluate, promote, merge, or prune"]
    R --> G
```

The durable graph may be large. Only selected nodes become live sandboxes.
A running container, mount, process tree, or workspace session is an execution
detail, not the durable identity of a branch.

## 3. Core abstractions

| Abstraction | Role in 2.0 |
| --- | --- |
| `RootId` | Stable identity of one immutable LayerStack checkpoint |
| `SandboxGroup` | Owns one checkpoint graph and its canonical accepted node |
| `SandboxNode` | Immutable, selectable branch or checkpoint in the graph |
| `ExecutionAttempt` | Temporary activation of one node in one isolated sandbox |
| `Evaluation` | Versioned tests, review, reward, and evidence for a sealed result |
| `Lease` | Protects roots and active work from reclamation |
| `Checkpoint` | Atomically sealed filesystem state, logical state, and provenance |
| `Promotion` | Explicit compare-and-swap advance of the group’s canonical node |
| `Materialization` | Native worker-local representation used for command execution |
| `Portable history` | CDC/CAS-backed retained history used outside the execution hot path |

Three distinctions are essential:

- A **fork** creates branch intent from an immutable node; it does not clone a
  running process or duplicate the parent workspace payload.
- An **activation** creates a temporary sandbox with its own writable state and
  isolation boundary.
- A **checkpoint** seals the result as a new immutable node. It never mutates
  its parent.

## 4. Two main phases

### Phase 1 — LayerStack 2.0 storage

**Goal:** replace whole-file historical LayerStack retention with a portable,
space-efficient checkpoint store while preserving the current native execution
experience.

Phase 1 introduces:

- portable, versioned LayerStack root identity;
- CDC/CAS-backed retained history;
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

## 5. Dependency order

| Order | Milestone | Depends on | Main proof |
| ---: | --- | --- | --- |
| 0 | Freeze current contracts and baseline | Current runtime | Existing behavior and performance are reproducible |
| 1 | Define portable roots and checkpoint semantics | 0 | Roots are deterministic, versioned, and backend-neutral |
| 2 | Build CDC/CAS history beside the current LayerStack | 1 | New metadata matches existing visible filesystem state |
| 3 | Prove native materialization and storage lifecycle | 2 | Warm execution stays native; old leased roots remain usable |
| 4 | Make 2.0 publication authoritative | 3 | OCC, blame, recovery, and GC pass hard correctness gates |
| 5 | Introduce `SandboxGroup` and immutable nodes | 4 | Branches are durable without resident sandboxes |
| 6 | Activate nodes in separate bounded sandboxes | 5 | Sibling isolation and hot-root reuse hold across containers |
| 7 | Add checkpoint, rollback, merge, and promotion workflows | 6 | No lost updates or ambiguous branch state |
| 8 | Add rollout and MCTS coordination | 7 | Retry-safe evaluation and backpropagation survive failure |
| 9 | Default-on migration and compatibility retirement | 8 | Rollback window and production evidence are complete |

This order creates one hard boundary:

> Phase 2 may design its schema in parallel, but it must not depend on the new
> storage path until Phase 1 has proven immutable roots, leases, OCC, recovery,
> blame, and native-path performance.

## 6. What can run in parallel

| Lane | When it may start | Constraint |
| --- | --- | --- |
| Baseline and benchmark verification | Immediately | Establishes the comparison contract before optimization claims |
| LayerStack storage implementation | After root and compatibility contracts freeze | Rust implementation; no public graph dependency |
| SandboxGraph schema design | During Phase 1 | Design only until Phase 1 semantics stabilize |
| SandboxGraph runtime | After Phase 1 exit | Must consume the proven root, lease, OCC, and recovery contracts |
| MCTS scheduler and evaluator design | Late Phase 1 or early Phase 2 | Runtime integration waits for durable nodes and idempotency |
| MCTS execution | After bounded sandbox activation | Must not create one resident sandbox per durable node |

The benchmark lane should finish before approach results are judged. If an
implementation finishes first, its evaluation clock starts only when the
shared baseline and verifier are ready.

## 7. Storage and performance posture

The product optimizes two different lifecycles:

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

No CDC algorithm is selected by this overview. The algorithm and packed layout
remain versioned and replaceable until identical benchmark evidence identifies
a production winner.

## 8. Migration posture

The migration is additive and evidence-gated:

1. read existing roots through a compatibility path;
2. generate 2.0 metadata beside current publication;
3. compare old and new roots before new reads become authoritative;
4. enable 2.0 publication for opted-in groups;
5. keep the old reader through a rollback window; and
6. retire the compatibility path only after usage and recovery evidence show
   it is safe.

The existing workspace-session API becomes a compatibility execution handle.
New functionality belongs to the graph model so that the compatibility layer
does not become a second architecture.

## 9. Explicit non-goals for this migration

- CRIU or instruction-exact process rollback;
- nested workspace sessions as the public branching model;
- one permanently resident container or VM per durable node;
- FUSE, JuiceFS, a CAS-backed VFS, or per-read CAS reconstruction;
- required reflink, custom kernels, loop devices, or target-image utilities;
- an external database service or SQLite dependency in the storage core;
- automatic semantic conflict resolution;
- distributed or remote CAS in the first implementation;
- production WASI execution in the initial Ubuntu 24.04 qualification; and
- broad host or image matrices before the initial Docker path is proven.

The logical root format should remain backend-neutral so wider OCI and WASI
qualification can be added later without changing checkpoint identity.

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

This index intentionally stops at the abstraction and migration order. The
next documents should separately define:

1. Phase 1 storage and compatibility specification;
2. Phase 1 benchmark and acceptance specification;
3. Phase 2 SandboxGraph and checkpoint specification;
4. Phase 2 bounded sandbox activation specification;
5. Phase 2 rollout and MCTS specification; and
6. production migration, rollback, and observability specification.

No Phase 2 implementation should begin from this overview alone.
