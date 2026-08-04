# LayerStack-0 architecture innovation

Date: **2026-08-04**  
Brand: **LayerStack-0, powered by EphCoW**  
Status: **Architecture-aligned working narrative**

> **Ephemeral branches. Immutable outcomes.**

LayerStack-0 is the sandbox Version engine for Ephemeral Sandbox. Its EphCoW
architecture lets parallel agents branch from one accepted immutable sandbox
Version without copying the accepted payload, work in isolated writable
namespaces, and attempt publication through one strict optimistic-concurrency
transition.

The innovation is not a new spelling of filesystem reflink, OverlayFS, CAS, or
OCC. It is the architecture that composes complete portable Version identity,
immutable payload admission, reference-only branching, runtime isolation, and
conflict-safe publication into one multi-agent sandbox lifecycle.

This is an explanatory brand narrative. The normative engineering contract is
[architecture_design.md](../architecture_design.md). In particular, CAS+CDC
cross-Version sharing is not part of the currently selected R0 storage family.

## 1. The problem: one world, many agents

An agent system often wants many workers to explore from the same starting
sandbox:

```text
                         shared starting world
                                  |
                   +--------------+--------------+
                   |              |              |
                Agent A        Agent B        Agent C
               tries plan 1   tries plan 2   tries plan 3
                   |              |              |
               result A       result B       result C
```

Giving each agent a recursive physical copy is simple, but branch work grows
with the starting world's files and bytes. Keeping a growing stack of deltas can
make branching cheap, but it turns the meaning of the current Version into a history
reconstruction problem. Letting agents write the same accepted filesystem
violates isolation. Allowing stale results to merge during publication makes the
selected outcome ambiguous.

LayerStack-0 starts from a different premise:

> A new agent does not need another durable copy of its starting Version. It needs
> a reference to a complete immutable Version and an isolated place to make
> temporary changes.

## 2. Why the name is LayerStack-0

Legacy LayerStack represents durable history through layers, parentage, depth,
merge, and squash behavior. That representation is evidence about the current
product, not the V2 definition of a Version.

LayerStack-0 resets the Version model:

```text
BEFORE: LAYER-CHAIN TRUTH                AFTER: COMPLETE-VERSION TRUTH

base                                    Version V17
  \                                        complete
   layer 1                                 immutable
      \                                    independently meaningful
       layer 2
          \
           layer 3  -> current filesystem view

read meaning:                            read meaning:
reconstruct base + ordered deltas        resolve one accepted Version

cost and risk may follow depth           required layer depth = 0
merge/squash affect value meaning        no layer merge/squash in V2 truth
runtime representation leaks inward      portable identity, runtime effects out
```

The zero therefore has a concrete architectural meaning:

> **Zero required layer-chain depth.**

It does not mean zero metadata, zero checkpoint work, zero durability work, or
zero runtime setup.

## 3. What EphCoW means

**EphCoW** expands to **Ephemeral Copy-on-Write**. In the selected architecture,
it names a lifecycle with three deliberately separated planes:

```text
                  LAYERSTACK-0 / EPHCOW

   APPLICATION PLANE        VERSION PLANE          RUNTIME-EFFECT PLANE
  +------------------+    +------------------+    +---------------------+
  | authorization    |    | VersionId identity |    | writable workspace  |
  | request ordering |--->| immutable Versions|<---| OverlayFS/mounts     |
  | expected Head    |    | roots and Heads  |    | namespaces          |
  | rollout policy   |    | OCC publication  |    | process execution   |
  +------------------+    | recovery/retire  |    +---------------------+
                          +------------------+

  decides what may run    owns selected truth     owns temporary effects
  and what to publish     never owns MCTS         never defines identity
```

The version plane remains in the existing `sandbox-runtime-layerstack` package,
rewritten for V2. Application services retain authorization, orchestration, and
expected-Head capture. Existing workspace, OverlayFS, namespace, and execution
owners retain Linux effects.

No new service, database, coordinator, helper process, or package boundary is
required by the selected architecture.

### The durable CoW boundary

For an already accepted Version, Branch creation uses Head create-if-absent,
rollback/Branch movement uses exact Head OCC replacement, Checkpoint creation
uses fixed-Root create-if-absent, and removal uses an exact expected record.
These operations change only a small Root or Head record and do not open or
duplicate the payload:

```text
payload bytes read    = 0
payload bytes written = 0
payload bytes copied  = 0
```

That is the selected and testable accepted-reference zero-payload boundary. Creating a runtime
namespace, executing commands, changing files, checkpointing a new Version,
hashing canonical Version facts, admitting a new payload, synchronizing durability, and
cleaning resources are outside this zero-payload claim.

### The ephemeral boundary

“Ephemeral” describes the agent's temporary writable work and the ability to
discard unsuccessful exploration. It does not describe accepted Versions:

```text
temporary                              durable
---------                              -------
agent namespace                        Accepted Version
writable workspace                     VersionId and AcceptedBinding
candidate scratch                      root and Head records
mount/process details                  publication and recovery truth
abandoned rollout                      retained immutable payload
```

An agent may come and go. An accepted Version remains immutable for as long as
it is durably rooted or held under read custody.

## 4. The multi-agent lifecycle

```text
                       HEAD = VERSION V17
                     complete and immutable
                               |
             durable reference fork: payload copy = 0
              +----------------+----------------+
              |                |                |
              v                v                v
        +-----------+    +-----------+    +-----------+
        | Agent A   |    | Agent B   |    | Agent C   |
        | branch A  |    | branch B  |    | branch C  |
        | private W |    | private W |    | private W |
        +-----+-----+    +-----+-----+    +-----+-----+
              |                |                |
         checkpoint         abandon        checkpoint
              |                                 |
              v                                 v
         Candidate A                      Candidate C
       complete but unaccepted          complete but unaccepted
              |                                 |
              +---------- application ----------+
                            selects
                               |
                   expected (V17, revision 42)
                               |
                       one OCC transition
                      /                   \
                     /                     \
          winner: HEAD = candidate       stale: no change,
                 revision 43             no merge/rebase
```

The store does not choose which agent is best. MCTS, rollout scoring, policy,
and authorization stay in the application plane. LayerStack-0 makes the chosen
publication attempt safe and unambiguous.

### Step 1: resolve

The application resolves a typed Root or Head to an accepted
`(AcceptedBinding, HeadRevision)` and captures bounded read custody. A raw
`VersionId` cannot enter this reference-only path.

### Step 2: branch

The durable branch/reference operation reuses the accepted binding. It performs
zero payload-byte I/O with respect to the accepted Version. Runtime owners then
prepare an isolated writable environment without changing portable identity.

### Step 3: explore

The agent reads the accepted base and records private effects in its writable
workspace. The accepted payload remains immutable, and one agent's writes cannot
become another agent's selected truth.

### Step 4: checkpoint and admit

A successful branch supplies a bounded complete candidate. LayerStack-0
validates and canonicalizes it, derives a typed `VersionId`, and stages its
complete payload.

If that `VersionId` is already occupied, LayerStack-0 compares the full canonical
bytes:

```text
same VersionId + equal canonical bytes     -> reuse accepted payload
same VersionId + unequal canonical bytes   -> collision; reject
```

A digest is an address, not proof of equality.

### Step 5: publish

The store admits and makes any new payload durable before a reference may name
it. Under its exclusive transition gate, it rereads the expected Head and
revision. One atomic Head replacement is the OCC linearization point.

```text
expected Head still current  -> publish complete new Head
expected Head is stale       -> no Head change, no merge, no rebase
```

### Step 6: recover and retire

Recovery sees either the prior durable truth or a complete new truth. Incomplete
staging, complete-but-unreferenced payloads, corrupt records, and active reads
have explicit handling. Cleanup is bounded and repeatable; an ambiguous or
unsafe durable condition fails closed.

## 5. The selected storage model

The selected R0 family is deliberately direct:

```text
<LayerStack0Root>/
  versions/<VersionId>/payload/  one complete immutable payload closure
  heads/<selector>               AcceptedBinding + HeadRevision
  roots/<kind>/<root-id>         durable reachability to AcceptedBinding
  staging/<transaction-id>/      private bounded candidate work
  control/...                    format, generation, and recovery metadata
```

Its defining properties are:

- one Accepted Version at an occupied `VersionId` has one complete immutable filesystem closure;
- no parent, layer depth, squash, or delta reconstruction is required;
- roots and Heads contain references, not payload copies;
- equal canonical Version bytes converge on the same occupied `VersionId` payload;
- occupied identifiers require full canonical-byte comparison;
- accepted payloads are never exposed as writable live workspaces;
- payload durability precedes reference publication;
- one OCC transition changes the selected Head; and
- roots, Heads, and bounded read custody govern safe retirement.

This is content-addressed at the complete-Version boundary. It does **not**
currently mean that chunks are deduplicated across different `VersionId`s.

## 6. What is architecturally new

None of the individual ingredients is claimed as a new computer-science
primitive. The architectural contribution is their composition at the sandbox
Version boundary.

| Ingredient | What LayerStack-0 changes for multi-agent sandboxes |
|---|---|
| Complete immutable Version | Every accepted outcome is independently meaningful; history depth cannot change its meaning. |
| Reference-level CoW | Branching an accepted Version changes references without copying its payload. |
| Split durable/runtime ownership | Portable truth stays out of mounts, containers, namespaces, and host paths; writable effects stay out of durable identity. |
| Multi-agent isolation | Many agents may explore one base without mutating the accepted Version or each other. |
| Exact content admission | A digest collision cannot alias two unequal Versions because occupied IDs require full-byte comparison. |
| Strict OCC publication | Concurrent exploration may be broad, while selected-Head mutation remains one explicit linearization point. |
| Recoverable lifecycle | Admission, reference publication, read custody, retirement, and cleanup form one coherent failure model. |
| Rewrite in place | The existing low-level owner is transformed without adding an unnecessary service or abstraction boundary. |

The result is a version engine built around the operation an agent system cares
about: fork one known world into many isolated attempts, then publish exactly one
accepted outcome without corrupting or ambiguously rewriting shared history.

## 7. EphCoW versus neighboring mechanisms

### Compared with full copy

Full copy duplicates a directory tree and its payload. LayerStack-0's durable
fork reuses an already accepted Version binding and copies zero payload bytes.
The comparison applies to the durable branch/reference operation, not to every
runtime or checkpoint step.

### Compared with file reflink

Reflink is a filesystem operation that makes files share physical extents until
a later write. A whole-tree recursive reflink still walks entries and creates
destination metadata, and it depends on local filesystem support.

EphCoW operates at a different boundary:

```text
REFLINK                                 EPHCOW

clones local file extents               branches an accepted sandbox Version
filesystem-specific                     portable logical identity
CoW on extent modification              isolated runtime-owned agent writes
no selected-Head protocol               one strict OCC Head transition
no content collision contract           full-byte occupied-ID comparison
clone primitive                         branch/admit/publish/recover lifecycle
```

Native reflink or a filesystem-native snapshot may beat or tie LayerStack-0 for
raw local clone/snapshot and hot-path filesystem operations. LayerStack-0 is
designed for the broader product operation: branching portable immutable
sandbox Versions for parallel agents and safely publishing one result.

The architecture-safe positioning is qualitative:

> **EphCoW defines complete sandbox-Version branching with portable identity,
> agent isolation, immutable admission, recovery, and OCC publication.**

No owner-approved quantitative comparison target or matched benchmark result
exists. Reflink latency remains a possible future comparison workload, not a
selected product target or an inferred win.

### Compared with OverlayFS or layer stacks

OverlayFS is a runtime-effect mechanism. It can construct a writable view, but
its lower/upper/work paths, whiteouts, mounts, and host details are not portable
Version identity.

Legacy layer stacks make ordered deltas part of durable truth. LayerStack-0
allows runtime owners to use appropriate Linux effects while ensuring that the
accepted result is a complete portable Version with zero required layer depth.

### Compared with a plain CAS

A CAS addresses content. It does not by itself define:

- which filesystem facts are portable;
- how an agent gets an isolated writable namespace;
- when a candidate becomes immutable and accepted;
- how an occupied digest is verified;
- which concurrent Head transition wins;
- what recovery exposes after a crash; or
- when an unrooted Version may be retired.

LayerStack-0 provides that complete lifecycle at the sandbox-Version boundary.

## 8. The CAS+CDC boundary

A stronger EphCoW proposal could represent complete logical Versions with
immutable manifests and content-defined chunks, share unchanged chunks across
different Versions, and expose a custom lazy writable view. That could improve
sparse checkpoint storage and high-fan-out workflows.

It is **not** a selected LayerStack-0 feature today:

```text
SELECTED R0                              PROPOSED CAS+CDC EXTENSION

complete logical Version                complete logical Version
complete payload per VersionId            manifest/chunk physical representation
zero-payload reference moves            zero-payload reference moves
existing runtime-effect owners          possible custom lazy COW view
equal-Version payload convergence       cross-Version chunk sharing
no object DAG                           object reachability and GC obligations
```

CAS+CDC changes physical truth, identity substructure, collision handling,
publication ordering, recovery, retirement, resource bounds, and possibly
writable-view ownership. It therefore requires a reopened Phase 01 joint
ownership/storage decision. Branding must not announce it merely as an
optimization of the already selected store.

If that architecture is later selected and proved, this document should be
updated to distinguish:

- the stable EphCoW product semantics: complete immutable Versions,
  reference-only forks, isolated writes, and OCC publication; from
- a possible future CAS+CDC data plane: chunking, manifests, lazy reads, write
  tracking, admission, and retirement.

## 9. Claim boundaries

The branding stays credible by attaching “zero-copy” to the exact operation it
describes.

### Safe architecture language

- **Zero-payload reference forks.**
- **Complete immutable Versions with zero required layer depth.**
- **One accepted Version, many isolated agent branches.**
- **A stale publish loses cleanly—no silent merge or rebase.**
- **Portable identity separated from runtime-private effects.**
- **Content-addressed complete-Version admission with exact collision checks.**
- **Designed for high-fan-out multi-agent sandbox exploration.**

### Language that requires later proof or reselection

- “EphCoW is faster than reflink.”
- “End-to-end fork is constant-time.”
- “Writes and checkpoints are zero-copy.”
- “Checkpoint cost is proportional only to changed bytes.”
- “Versions share CDC chunks.”
- “LayerStack-0 implements a custom filesystem.”
- “Unlimited agents” or any unbounded-resource claim.
- Any latency, throughput, storage-ratio, or agent-count guarantee.
- Any V2 performance conclusion derived from historical Stage 4.6 evidence,
  which is `INCOMPARABLE`.

## 10. Reusable brand copy

### Five words

> **Immutable worlds for parallel agents.**

### Technical line

> **Zero-payload forks. Isolated writes. Strict publication.**

### Product line

> **Fork the reference. Isolate the work. Publish one outcome.**

### Short description

> LayerStack-0 gives every agent an isolated branch from one accepted immutable
> sandbox Version without duplicating that Version's payload during the durable
> fork.

### Technical description

> LayerStack-0 replaces layer-chain truth with complete immutable sandbox
> Versions. EphCoW makes accepted-Version forks reference-only, keeps writable
> agent effects in isolated runtime namespaces, admits complete candidates by
> exact content identity, and publishes through one OCC Head transition.

### Differentiation line

> **Reflink clones local extents. Legacy LayerStack reconstructs deltas.
> LayerStack-0 branches complete immutable sandbox Versions.**

## 11. Architecture references

- [Selected V2 architecture](../architecture_design.md)
- [R0 architecture decision](../design/decisions/ADR-001-r0-complete-version-storage.md)
- [Storage design](../design/03-state-store.md)
- [Algorithms and call flows](../design/04-algorithms-and-call-flows.md)
- [Performance and optimization](../design/07-performance-and-optimization.md)
- [EphCoW versus reflink analysis](../complexity-analysis/ephcow-vs-reflink-performance-analysis.md)
- [Architecture diagrams](../diagrams/README.md)
