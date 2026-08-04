# Proposed backend abstraction and runtime Workspace isolation

Date: **2026-08-04**

Status: **`PROPOSED` CAS+CDC companion — not Phase 02/03 implementation input**

This chapter preserves a proposed backend-neutral CAS+CDC alternative and its
runtime handoff for comparison. It does **not** define selected LayerStack-0
storage and does not define EphCoW. Under selected R0, LayerStack-0 uses a
qualified local filesystem-native complete-Version payload closure and calls
the existing runtime-effect owners directly. EphCoW is the selected
reference-level CoW behavior over AcceptedBindings and isolated Workspaces.

The alternative described below is backend-agnostic: its correctness would not
depend on a custom filesystem, a filesystem-specific clone operation, or one
particular durable substrate. That extra abstraction is not currently
selected.

The current Linux sandbox can continue to use OverlayFS as one runtime adapter.
OverlayFS paths, copy-up behavior, whiteouts, mounts, and namespaces remain
runtime-private effects in both designs. They never become portable Version
identity or selected LayerStack-0 truth.

The governing sources remain the product [PRD](../../PRD.md), selected
[architecture](../../architecture_design.md), Phase 01
[selection contract](../../phases/01-choose-design/SPEC.md), and Phase 00
[source inventories](../../phases/00-freeze-rules/SPEC.md). Everything beyond
the selected invariants listed next remains a candidate that requires Phase 01
reopening unless a higher-authority decision document changes that status.

Selected invariants carried into the comparison are limited to:

- Accepted Versions are complete and immutable;
- Heads and Roots use AcceptedBindings;
- reference-only EphCoW moves perform payload I/O `0/0/0`;
- runtime effects remain at existing owners and outside Version identity; and
- publication has one strict OCC Head transition.

The generic `DurableBackend`, manifest/Chunk representation, materialization
cache, and generic `WorkspaceAdapter` below are proposals, not accepted APIs or
new boundaries.

## Question answered

How can one accepted immutable Version serve many isolated agent Workspaces
without making the durable storage design depend on the runtime filesystem?

The proposed answer uses two explicit contracts:

```text
PROPOSED BACKEND CONTRACT [P]                  PROPOSED WORKSPACE CONTRACT [P]

AcceptedBinding                               activate(binding)
      |                                             |
      v                                             v
AcceptedVersion                               immutable WorkspaceBase
      |                                             +
      +-- complete manifest                         private writable effects
      `-- complete Chunk closure                    |
                                                    v
                                               agent namespace

storage backend -X-> mount path in Version identity
runtime adapter -X-> direct authority over Branch Heads or Checkpoints
```

The storage owner proves that an `AcceptedBinding` names one complete immutable
Version. The runtime adapter proves that a live Workspace begins from that
Version, isolates its writes, and can freeze a complete view for later capture.

## Legend

```text
[I]  immutable durable Version or Chunk
[M]  durable reference metadata: replaceable Head or fixed Root
[R]  runtime-private Workspace object or effect
[T]  private bounded transaction or staging object
[P]  proposed CAS+CDC mechanism

----> metadata, reference, or control flow
====> payload-byte flow
....> optional hint or derived cache relation
-X--> forbidden dependency or authority flow
```

## 1. Proposed backend-agnostic split

```text
                    PRODUCT / APPLICATION OWNERS

       auth, Branch policy, request ordering, rollout policy
                              |
                              v
                 proposed backend-neutral reference API [P]
                              |
                              v
+------------------------------------------------------------------+
| PROPOSED CAS+CDC DURABLE CORE [P]                                |
|                                                                  |
| AcceptedVersion                                                  |
|   +-- complete portable manifest                                 |
|   `-- complete transitive Chunk closure                          |
|                                                                  |
| Head / Root / Checkpoint records                                 |
| admission, full-byte collision checks, OCC, recovery, retirement |
+-----------------------------+------------------------------------+
                              |
                 AcceptedBinding / read custody
                              |
                              v
+------------------------------------------------------------------+
| RUNTIME WORKSPACE ADAPTER                                        |
|                                                                  |
| activate -> isolate -> execute -> freeze -> teardown              |
|                                                                  |
| current Linux profile: immutable directory + private OverlayFS   |
| another profile:         same semantic contract, different means |
+------------------------------------------------------------------+
```

The selected authority separation does not require a new package or process.
R0 uses direct calls between existing owners. The generic interfaces shown in
this proposal are not authorized additions. A new
service, helper, registry, or coordinator would require a concrete necessity
case and a reopened architecture decision.

## 2. Proposed durable-backend capability contract

The proposed CAS+CDC core must express semantics before choosing a local
filesystem, object store, database, or other durable substrate.

```text
DurableBackend capability family [P]

  stage_immutable(bytes, bounds) -> StagedObject
  inspect_occupant(typed_id)     -> Vacant | Occupied(ReadHandle)
  compare_full(ReadHandle, bytes)-> Equal | Mismatch
  admit_staged(StagedObject)     -> DurableOccupant
  admit_complete_version(...)    -> AcceptedBinding
  acquire_read_custody(binding)  -> VersionRead
  read_chunk(VersionRead, id)    -> bounded byte stream
  replace_head(expected, next)   -> Published | Stale
  enumerate_recovery(bounds)     -> bounded recovery page
  retire_unreachable(bounds)     -> bounded cleanup result
```

These are conceptual obligations, not a fixed public API. A backend profile
may implement them with different primitives, but it must preserve:

- immutable admitted bytes;
- full-byte comparison for occupied typed identifiers;
- Chunk durability before complete-Version visibility;
- complete-Version durability before Root/Head durability;
- exactly one strict OCC Head linearization point;
- prior-or-complete-new recovery;
- reader-safe retirement; and
- finite staging, queues, scans, workers, memory, descriptors, and cleanup debt.

An optional acceleration can change costs. It cannot change these outcomes,
identifier meanings, or failure behavior.

## 3. Proposed generic Workspace-adapter contract

```text
WorkspaceAdapter

  activate(AcceptedBinding, limits) -> Workspace
  execute(Workspace, process_spec)  -> runtime result
  freeze(Workspace)                 -> FrozenWorkspace
  change_hints(FrozenWorkspace)     -> optional hints
  close(Workspace)                  -> bounded cleanup result
```

Required semantics:

| Operation | Required result |
|---|---|
| `activate` | The Workspace begins from the complete accepted Version and has private writable effects. |
| `execute` | One agent cannot observe or mutate another agent's private Workspace effects. |
| `freeze` | Publication receives a stable complete filesystem view, not merely a directory delta. |
| `change_hints` | Hints may reduce scanning but are never correctness evidence by themselves. |
| `close` | Mounts, scratch, handles, workers, and custody are released or recorded as bounded cleanup debt. |

The core publisher remains correct if the adapter provides no byte-range hints:

```text
trusted byte-range hints available? ---- yes ----> localized capture candidate
              |
              no
              v
trusted changed-path hints available? -- yes ----> scan complete changed files
              |
              no
              v
scan complete frozen Workspace
```

Every accelerated path must validate to the same complete Candidate as the
fallback path.

## 4. Correctness-first materialization profile

One portable runtime profile constructs an immutable directory using ordinary,
bounded byte I/O. It does not require a special filesystem operation.

```text
AcceptedBinding
      |
      v
revalidate binding + acquire Version read custody
      |
      v
reserve bounded staging and cache budget
      |
      v
read complete manifest in canonical order
      |
      +---- directory ------------> create safely below staging root
      +---- symlink --------------> validate and create without traversal
      `---- regular file ---------> stream ordered Chunks to file
                                         |
                                         v
                               verify length/content/metadata
      |
      v
final complete-tree validation
      |
      v
atomically expose immutable WorkspaceBase
      |
      v
release staging; retain read/cache custody while active
```

The cache is derived runtime data, never accepted truth:

```text
AcceptedVersion ----> may derive ----> WorkspaceBase cache

WorkspaceBase cache -X-> define VersionId
WorkspaceBase cache -X-> accept a Branch Head
WorkspaceBase cache -X-> survive after its Version loses all required custody
```

Concurrent requests for the same Version may share one completed base or build
private staging attempts that converge on one validated cache entry. They must
not expose a partially constructed tree.

Cold materialization can read and write the complete Version payload. Warm
activation may reuse a validated base. Neither cost is part of the zero-payload
reference-operation proof.

## 5. Current Linux OverlayFS adapter profile

```text
                         Accepted Version V1 [I]
                                  |
                     ordinary materialization profile
                                  |
                                  v
                     immutable WorkspaceBase(V1) [R]
                                  |
                     shared read-only runtime base
              +-------------------+-------------------+
              |                                       |
              v                                       v
       agent-a Workspace W17                   agent-b Workspace W18

       lower = WorkspaceBase(V1)               lower = WorkspaceBase(V1)
       upper = W17/upper                       upper = W18/upper
       work  = W17/work                        work  = W18/work
       merged= W17/merged                      merged= W18/merged
       ns    = namespace A                     ns    = namespace B
```

The two agents share only the immutable base. Their upperdirs, workdirs,
merged mounts, processes, and namespaces are distinct.

### Read, write, and delete

```text
READ /src/lib.rs

  private upper entry exists? -- yes --> read private entry
             |
             no
             v
       read immutable WorkspaceBase


WRITE /src/lib.rs

  adapter performs its normal private-write behavior
             |
             v
  modify only W17 private effects
             |
             `----> Accepted Version V1 remains immutable


DELETE /assets/icon.png

  record runtime-private deletion in W17
             |
             `----> base entry remains immutable
```

For the current OverlayFS profile, the first write can copy up an entire file
and a deletion can be represented by a whiteout. Those are measured runtime
costs and effects, not portable facts and not Chunk-level EphCoW guarantees.

## 6. Reference COW versus Workspace activation

```text
REFERENCE-ONLY OPERATION                 RUNTIME ACTIVATION

fork / checkpoint / rollback            open agent Workspace
        |                                        |
        v                                        v
validate AcceptedBinding                 obtain read custody
        |                                        |
        v                                        v
write small Head/Root metadata            obtain/build WorkspaceBase
        |                                        |
        v                                        v
payload I/O = 0 / 0 / 0                  start private runtime adapter

operation ends here                       payload I/O may be nonzero
```

The zero-payload EphCoW claim is therefore limited to the five exact
accepted-reference transitions: payload read/write/copy is `0/0/0`, while
reference metadata, coordination, and durability-fence work remains nonzero.
End-to-end Workspace startup must report cold and warm materialization, mount,
metadata, and private-allocation costs separately.

## 7. Freeze and publication flow

```text
private Workspace W17
        |
        v
freeze stable complete view
        |
        +.... optional changed-path/range hints
        |
        v
canonical portable tree walk
        |
        +---- unchanged proven content ----> reuse accepted ChunkIds [P]
        `---- changed/unknown content =====> CDC + Chunk admission [P]
                                              |
                                              v
                                   complete Version manifest
                                              |
                                              v
                                     Version admission
                                              |
                                              v
                               one conditional OCC Head transition
```

Runtime whiteouts or opaque-directory markers are interpreted while resolving
the frozen complete tree. They are never copied into portable Version identity
as storage-layer instructions.

## 8. Failure, custody, and cleanup

```text
AcceptedVersion custody -----------------------------+
                                                     |
active WorkspaceBase custody ------------------------+--> Version remains readable
                                                     |
active Workspace custody ----------------------------+

last durable Root removed
        |
        v
active read/base/workspace custody remains? -- yes --> defer retirement
        |
        no
        v
exact revalidation -> bounded Version/Chunk retirement
```

| Failure | Required response |
|---|---|
| Binding disappears or fails validation before activation | Fail closed; do not build a base from unaccepted objects. |
| Missing/corrupt Chunk during materialization | Fail closed, quarantine/report according to backend profile, never expose partial base. |
| Crash during materialization | Ignore/remove private incomplete staging through bounded recovery. |
| Concurrent equal materialization | Reuse one validated base or discard losing private staging safely. |
| Adapter activation failure | Release mounts, scratch, handles, and custody or record bounded cleanup debt. |
| Sandbox crash | Runtime owner tears down namespace and private effects; durable Version remains immutable. |
| Cache eviction racing active Workspace | Active custody wins; eviction is deferred. |

## 9. Portable identity boundary

```text
PORTABLE VERSION FACTS                    RUNTIME/BACKEND-PRIVATE FACTS

normalized relative path                  durable object key/path
accepted entry kind                       staging directory
accepted portable metadata                cache key and cache path
symlink target                            inode, mount, namespace
complete regular-file bytes               lower/upper/work/merged paths
canonical format version                  process/container identity
                                           backend transaction token
```

No fact in the right column may affect `VersionId` or full canonical equality.
Changing durable backend or runtime adapter must not change Version identity.

## 10. Complexity and observability

Let:

```text
N = total payload bytes in the accepted Version
E = number of portable filesystem entries
C = number of Chunks in the Version
D = payload bytes changed in a live Workspace
S = bytes scanned during capture
K = unique new Chunk bytes admitted
A = number of concurrently active Workspaces
```

| Operation | Payload movement | Expected time | Worst case |
|---|---:|---:|---:|
| Reference-only fork/checkpoint/rollback | `0/0/0` | bounded metadata | bounded metadata |
| Cold ordinary-I/O materialization | read/write up to `N` | `O(N + E + C)` | `O(N + E + C)` |
| Warm validated-base activation | no required complete payload copy | adapter/cache dependent | may rematerialize `O(N + E + C)` |
| Current Linux first write | adapter dependent | workload dependent | may copy complete changed file |
| CDC publication | read `S`, write `K` plus metadata | localized when evidence and resynchronization hold | `S = O(N)` |
| Multi-agent immutable-base sharing | one base plus private effects | approximately `O(A)` runtime metadata | bounded by configured Workspace limits |

Required counters include:

```text
reference_payload_bytes_read/written/copied
materialization_payload_bytes_read/written
materialization_cache_hit/miss
workspace_private_bytes_written
workspace_activation_failures
active_bases / active_workspaces / active_mounts
staging_bytes / cleanup_debt
capture_bytes_scanned / unique_chunk_bytes_written
```

No existing benchmark establishes these values. Historical Stage 4.6 evidence
remains `INCOMPARABLE`.

## 11. Decision status and reopening boundary

| Concern | Status | Meaning |
|---|---|---|
| Complete immutable Version and zero-payload accepted-reference transitions | `SELECTED R0` | Required regardless of physical backend. |
| Existing workspace/mount/namespace owners retain runtime effects | `SELECTED R0` | The durable store does not absorb execution policy. |
| Current Linux OverlayFS runtime profile | `CURRENT IMPLEMENTATION DIRECTION` | Adapter-specific; never portable identity or durable truth. |
| Backend-agnostic CAS+CDC capability contract | `PROPOSED CANDIDATE CONSTRAINT` | Must be selected jointly with the CAS+CDC physical family. |
| Complete manifest plus transitive immutable Chunks | `PROPOSED` | Requires Phase 01 reopening under current documents. |
| Correctness-first ordinary-I/O materialization profile | `PROPOSED` | Provides a portable runtime path without a storage-specific clone dependency. |
| Exact backend profiles, cache policy, Chunker, codec, and limits | `OPEN/DEFERRED` | Later choices only after the architecture family is selected. |

Reopen Phase 01 before implementing CAS+CDC as accepted truth. The joint
candidate must prove:

1. source-placeable ownership inside the existing LayerStack-0 home;
2. backend capabilities sufficient for collision-safe admission, durability,
   OCC, recovery, custody, and bounded retirement;
3. a runtime adapter seam that keeps runtime-private facts out of identity;
4. a correctness-first activation/materialization path using ordinary bounded
   byte I/O;
5. no new service, process, registry, or coordinator unless a concrete R0
   failure makes it necessary; and
6. honest separation of reference, activation, live-write, capture, and
   publication costs.

## Related diagrams

- [Complete Versions and Chunk content-addressed storage](02-workspace-versions-and-chunk-cas.md)
- [Branches, checkpoints, fork, and rollback](03-branches-checkpoints-and-rollback.md)
- [Publication, OCC, and recovery](05-publication-occ-and-recovery.md)
- [Data movement and complexity](07-data-movement-and-complexity.md)
- [Storage diagram index](README.md)
