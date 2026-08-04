# Complete Workspace Versions and proposed chunk content-addressed storage

Date: **2026-08-04**

Design status: **`PROPOSED` architecture family — not selected by Phase 01**

Backend/runtime contract: **`PROPOSED CANDIDATE CONSTRAINT` — see
[proposed backend abstraction and runtime isolation](04-ephcow-runtime-view.md)**

## Question answered

If LayerStack-0 were extended with content-defined chunking (CDC) and
chunk-level content-addressed storage, what would be stored, and how would it
still represent a **complete workspace folder** rather than a chain of deltas
or a loose collection of chunks?

The short answer is:

```text
Branch or Checkpoint
        |
        v
complete Workspace Version
        |
        +-- complete portable directory-tree manifest
        `-- transitive closure of immutable file-content chunks
```

The **Workspace Version is the product object**. Chunks would be a private
physical representation for regular-file content. Agents, references, and
runtime workspaces do not point directly to chunks.

## Authority and status

This document is an explanatory proposal subordinate to the product
[hard rules](../../PRD.md#hard-rules-must-never-break), the selected
[R0 architecture](../../architecture_design.md), the Phase 03
[store contract](../../design/03-state-store.md), and the
[terminology guide](../../branding/terminology.md).

The selected R0 architecture currently requires one complete immutable payload
closure per Accepted Version at an occupied `VersionId`. It explicitly does
**not** select:

- CDC;
- cross-Version chunk sharing;
- manifest/chunk physical truth;
- a chunk or object DAG;
- tracing reclamation over that DAG; or
- a backend-agnostic durable capability and runtime-Workspace adapter contract.

Consequently, the diagrams below are not Phase 03 implementation permission.
Selecting this physical family would change storage, recovery, retirement,
resource, and runtime-view obligations and therefore requires **reopening
Phase 01**. The selected complete-Version, immutability, collision, OCC, and
runtime-neutrality requirements remain constraints on any reopened candidate.

## Legend

```text
[I]   immutable durable object
[M]   mutable durable reference
[R]   runtime-private object
[P]   proposed object or mechanism; not selected R0
[O]   open architecture-changing mechanism

----> reference, selection, or logical relationship
====> file-content byte flow
....> derived, validation, or non-authoritative relationship
-X->  forbidden relationship
```

The shared examples in this folder use:

```text
Versions:    V1, V2, V3
Chunks:      C01, C02, C03, ...
Branch:      agent-a
Checkpoint:  baseline
Workspace:   W17
```

`V1` is a readable example label. Normative identity is the typed `VersionId`
selected by ADR-002; accepted references use `AcceptedBinding`.

## 1. The target is the full workspace

The logical accepted object is the entire qualified portable workspace tree:

```text
Workspace Version V1 [I]

workspace/
+-- app/
|   +-- main.py
|   +-- config.json
|   `-- model.bin
+-- data/
|   `-- input.json
+-- scripts/
|   `-- run.sh
`-- README.md
```

A Version includes all portable facts Phase 02 accepts for that tree:

- normalized relative paths and directory structure;
- explicitly accepted entry kinds;
- explicitly accepted portable metadata;
- symlink targets, without following them during admission; and
- every regular file's complete contents.

It excludes host paths, OverlayFS lower/upper/work paths, mounts, namespaces,
containers, processes, leases, workspace/session identity, rollout policy, and
legacy layer ancestry.

The following mental model is wrong:

```text
Version V1 = Chunk C01 + Chunk C02 + Chunk C03
```

It omits paths, directories, entry kinds, metadata, empty files, symlinks, and
the ordering needed to rebuild each file. The complete model is:

```text
Version V1
  = complete canonical workspace-tree description
  + complete ordered content for every regular file
```

## 2. Proposed physical representation

In a CDC/chunk family, one complete Version manifest would describe the whole
workspace while immutable chunks would hold file-content bytes:

```text
versions/V1/workspace.manifest [I, P]

/
+-- app/                              directory entry
|   +-- main.py                       [C01, C02]
|   +-- config.json                   [C03]
|   `-- model.bin                     [C04, C05, C06, C07]
+-- data/
|   `-- input.json                    [C08]
+-- scripts/
|   `-- run.sh                        [C09]
`-- README.md                         [C10]
                 |
                 | complete ordered ChunkId sequences
                 v
content/chunks/ [I, P]
+-- C01
+-- C02
+-- C03
+-- C04
+-- C05
+-- C06
+-- C07
+-- C08
+-- C09
`-- C10
```

The proposed durable relationship is therefore:

```text
Branch agent-a [M]
        |
        | selects accepted binding for V1
        v
Workspace Version V1 [I, P]
        |
        +-- complete manifest: all portable tree facts
        |
        `-- complete chunk closure: all file-content bytes
```

The Branch never names a chunk. A Checkpoint never names a chunk. A runtime
Workspace never treats the chunk namespace as its visible folder. They name or
open a complete accepted Version.

The paths above are conceptual proposal names, not selected Phase 03 disk
spellings.

## 3. Logical completeness versus physical sharing

Two statements must remain true at the same time:

```text
Logical statement:
  Every Version completely describes its workspace without consulting a
  parent Version.

Physical statement, if this proposal is selected:
  Different complete Versions may reference equal immutable chunks.
```

Example:

```text
V1.manifest
  /app/main.py   -> [C01, C02]
  /app/data.bin  -> [C03, C04, C05]
  /README.md     -> [C06]

V2.manifest
  /app/main.py   -> [C01, C02]       unchanged content
  /app/data.bin  -> [C03, C07, C05]  changed middle range
  /README.md     -> [C06]            unchanged content
```

The physical sharing is:

```text
                    +--> C01 [I] <--+
                    +--> C02 [I] <--+
V1 [I, P] ----------+--> C03 [I] <--+---------- V2 [I, P]
                    +--> C04 [I]    +--> C07 [I]
                    +--> C05 [I] <--+
                    `--> C06 [I] <--+
```

Yet V2 is not expressed as:

```text
parent = V1
replace C04 with C07
```

V2 directly contains the complete path-to-content mapping. To read V2, the
engine needs:

```text
V2.manifest + C01 + C02 + C03 + C07 + C05 + C06
```

It does not need `V1.manifest`. That is how the proposal could provide
delta-efficient physical storage without restoring layer-depth truth.

## 4. Multiple edits to the same file

Assume CDC divides one large file by byte-content boundaries.

```text
V1 /data/model.bin

+-----+-----+-----+-----+
| C01 | C02 | C03 | C04 |
+-----+-----+-----+-----+
```

The first edit changes a middle region. After rechunking and boundary
resynchronization, the complete file sequence may be:

```text
V2 /data/model.bin

+-----+-----+-----+-----+-----+
| C01 | C02 | C05 | C06 | C04 |
+-----+-----+-----+-----+-----+
```

A later edit changes the beginning while retaining part of the V2 result:

```text
V3 /data/model.bin

+-----+-----+-----+-----+-----+
| C07 | C08 | C05 | C06 | C04 |
+-----+-----+-----+-----+-----+
```

Each Version manifest holds a complete sequence:

```text
V1 -> [C01, C02, C03, C04]
V2 -> [C01, C02, C05, C06, C04]
V3 -> [C07, C08, C05, C06, C04]
```

The proposed chunk-content store contains one immutable occupant per equal
chunk byte sequence:

```text
content/chunks/
+-- C01   referenced by V1 and V2
+-- C02   referenced by V1 and V2
+-- C03   referenced by V1 only
+-- C04   referenced by V1, V2, and V3
+-- C05   referenced by V2 and V3
+-- C06   referenced by V2 and V3
+-- C07   referenced by V3 only
`-- C08   referenced by V3 only
```

No edit overwrites a chunk. New bytes produce a new candidate chunk identity;
equal existing bytes reuse the existing immutable occupant.

CDC usually localizes boundary disturbance after an insertion or deletion, but
this is an optimization expectation, not a correctness guarantee. A small
edit can still require rechunking or writing much of a changed file. Exact
windowing, minimum/target/maximum sizes, and algorithms remain deliberately
unselected.

## 5. Proposed chunk admission

If chunk-level content addressing were selected, chunk admission would need a
collision rule as strong in spirit as complete-Version admission:

```text
changed regular-file byte stream
                |
                v
        proposed CDC chunker [P]
                |
                v
        candidate chunk bytes
                |
                v
      derive candidate ChunkId
                |
                v
      { is ChunkId occupied? }
              /       \
             no       yes
             |         |
             v         v
       durably write   compare FULL chunk bytes
       one immutable       /              \
       occupant          equal           unequal
                          |                |
                          v                v
                         reuse        COLLISION
                                      fail closed
```

Digest equality alone is not byte equality. If a candidate `ChunkId` is
occupied, the existing and candidate chunk bytes must be fully compared;
mismatch must not alias two byte sequences.

This does not replace the product's complete-Version collision rule:

```text
occupied VersionId
        |
        v
compare FULL canonical bytes for the complete Workspace Version
        |
        +-- equal   -> reuse the one accepted complete payload closure
        `-- unequal -> collision; no accepted binding or reference change
```

Chunk equality would be an internal physical concern. Complete canonical bytes
remain the identity and admission boundary required by the product.

## 6. Proposed publish data path

The proposal's data path could reuse unchanged manifest entries and process
changed files, but the result must still be one complete Candidate:

```text
Workspace W17 [R]
  lowerdir = accepted Version V1 view
  upperdir = private changes
                |
                v
resolve complete portable merged tree
                |
       +--------+----------------+------------------+
       |                         |                  |
       v                         v                  v
unchanged path             changed file        deletion/metadata
reuse complete entry       ==== CDC ====        update complete tree
                                 |
                                 v
                         put missing chunks [P]
       |                         |                  |
       +-------------------------+------------------+
                                 |
                                 v
                  complete Candidate manifest V2 [P]
                                 |
                                 v
          normal VersionId derivation + complete occupied-ID comparison
                                 |
                                 v
                  accepted immutable Version V2
```

The engine may use trusted reuse evidence to avoid rereading unchanged payload
only if Phase 02/03 proofs show that the complete canonical identity and
occupied-ID comparison remain correct. An upperdir is not itself a complete
Candidate and cannot become durable truth by relabeling its delta entries.

## 7. What this proposal does not solve by itself

A manifest plus Chunk objects is a durable representation, not automatically a
live agent Workspace. The design needs two backend-neutral seams:

```text
Version manifest + complete Chunk closure
             |
             v
   durable backend capability contract
             |
             v
       AcceptedBinding
             |
             v
   runtime Workspace adapter contract
             |
             +--> correctness-first ordinary-I/O materialization
             `--> current Linux immutable lowerdir + private upperdir profile
```

The ordinary-I/O profile may read and write the complete Version during a cold
materialization. That cost is separate from metadata-only reference COW. Other
qualified backend and runtime profiles may change cost, but they must preserve
the same identity, admission, recovery, isolation, and cleanup behavior.

The candidate does not introduce a custom filesystem or require a
storage-specific clone operation. Backend capabilities, materialization cache,
crash cleanup, reader custody, and retirement are nevertheless architecture
obligations rather than local Chunker details. See
[04-ephcow-runtime-view.md](04-ephcow-runtime-view.md).

## 8. Required invariants for any reopened candidate

- A Version is the complete logical portable workspace, not a chunk list by
  itself and not a parent-relative delta.
- A Version can be interpreted without another Version manifest or legacy
  layer chain.
- The complete manifest plus transitive chunk closure is immutable after
  acceptance.
- No Branch, Checkpoint, Root, or Head points directly to a chunk.
- Complete `VersionId` occupancy invokes full canonical-byte comparison.
- Proposed chunk identity occupancy also fails closed on full-byte mismatch.
- Chunks are never overwritten in place or reassigned to different bytes.
- Reference-only fork, checkpoint, rollback-to-existing, and same-Version
  moves do not traverse manifests or chunks and report payload I/O `0/0/0`.
- Runtime-private base/cache paths, lowerdirs, upperdirs, mounts, leases, and
  cache locations do not enter portable identity.
- Candidate construction is bounded in bytes, entries, chunks, memory, file
  descriptors, scratch, workers, and recovery debt.
- An accepted reference can never name a manifest with a missing chunk.
- Retirement cannot delete a chunk used by a reachable or custodied Version.

## 9. Selected, proposed, and open decisions

| Item | Status | Decision owner or consequence |
|---|---|---|
| Complete immutable workspace Version per occupied `VersionId` | `SELECTED R0` | Phase 02/03 must prove it. |
| Equal complete canonical Version converges on one payload closure | `SELECTED R0` | Product hard rule 2. |
| Reference-only operations have payload I/O `0/0/0` | `SELECTED R0` | Product hard rule 3. |
| CDC over changed regular-file contents | `PROPOSED` | Requires Phase 01 reopening before implementation. |
| Cross-Version immutable chunk sharing | `PROPOSED` | Changes the selected physical storage family. |
| Complete Version manifest over chunks | `PROPOSED` | Adds multi-object completeness, recovery, and retirement obligations. |
| Exact codec, digest, and portable fact grammar | `DEFERRED PHASE 02` | Must remain deterministic, complete, versioned, and bounded. |
| Chunker family and chunk-size limits | `UNSELECTED` | Cannot be chosen as a Phase 03 local optimization under current R0. |
| Chunk identity algorithm and layout | `UNSELECTED` | Would belong to an accepted reopened architecture and later detailed design. |
| Backend-agnostic durable capability contract | `PROPOSED` | Must define immutable admission, comparison, durability, OCC, recovery, custody, and retirement semantics before a backend profile. |
| Runtime Workspace adapter and ordinary-I/O materialization profile | `PROPOSED` | Keeps runtime effects outside identity and provides a correctness-first activation path. |
| Cross-object retirement algorithm/index | `OPEN` | Must be bounded, reader-safe, recoverable, and non-authoritative where required. |
| Historical Stage 4.6 performance | `INCOMPARABLE` | Supplies no selection or speed proof. |

## 10. Reopening question and proof burden

The bounded question to reopen Phase 01 is:

> Can one source-placeable design inside the existing LayerStack-0 ownership
> boundary make a complete manifest plus immutable Chunks durable and make an
> Accepted Version available through a backend-neutral Workspace adapter, with
> bounded resources and crash-safe publication/retirement, without introducing
> another selected-Version authority or platform-specific correctness dependency?

A reopened winner would need to select **together**:

1. manifest/chunk admission and complete-Version durability;
2. the durable backend capability contract and qualified backend profiles;
3. publication and one OCC Head transition;
4. runtime-Workspace activation/materialization and reader custody;
5. chunk/manifest reachability and last-reference retirement;
6. bounded cache, scratch, worker, FD, and recovery behavior; and
7. exact ownership/dependency additions, if any, with a proved necessity case.

If that joint proof cannot be established, CAS+CDC must remain research and
the selected filesystem-native complete-payload R0 family remains authoritative.

## Related diagrams and contracts

- [Storage diagrams index](README.md)
- [Proposed backend abstraction and runtime isolation](04-ephcow-runtime-view.md)
- [CDC boundaries, resynchronization, and reuse](08-cdc-boundaries-resynchronization-and-reuse.md)
- [Selected R0 storage model](../02-storage-model-and-content-addressing.md)
- [Selected fork/checkpoint/rollback semantics](../03-fork-checkpoint-rollback-and-cow.md)
- [Product hard rules](../../PRD.md#hard-rules-must-never-break)
- [Selected architecture](../../architecture_design.md)
- [Phase 03 store contract](../../design/03-state-store.md)
- [LayerStack-0 terminology](../../branding/terminology.md)
