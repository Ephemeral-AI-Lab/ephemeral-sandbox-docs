# LayerStack-0 terminology

Date: **2026-08-04**  
Status: **Accepted V2 naming contract**

This guide keeps LayerStack-0 and EphCoW language precise across architecture
documents, code discussions, benchmarks, demos, and product copy. It does not
create new engineering contracts. If a definition conflicts with the product
[PRD](../PRD.md) or selected
[architecture](../architecture_design.md), the higher-authority document wins
and this guide must be corrected.

## 1. Names and capitalization

| Write | Meaning | Do not write or imply |
|---|---|---|
| **Ephemeral Sandbox** | The multi-agent sandbox product | “EphCoW” as the name of the whole product |
| **LayerStack-0** | Public short name for the V2 sandbox Version engine | `LayerStack 0`, `Layer Stack Zero`, or “version zero” |
| **EphCoW** | Ephemeral Copy-on-Write, the LayerStack-0 branch/admit/publish architecture | `ECOW`, `ECoW`, “Eph COW,” or a claim that it is a new reflink syscall |
| `layerstack-0` | Lowercase identifier when a command, metric, file, or machine-readable name requires one | Preferred prose spelling |
| `ephcow` | Lowercase code or metric identifier | Preferred prose spelling |
| **Version** | Named LayerStack-0 concept: one accepted complete immutable portable filesystem value | Every temporary workspace or unaccepted candidate |
| `VersionId` | Exact typed identity spelling selected by ADR-002 | `StateId`, `state ID`, `state hash`, raw digest, or proof of equality |
| **AcceptedVersion** | LayerStack-0-verified durable admission of one `VersionId` and its complete immutable payload closure | A raw or merely computed `VersionId` |
| **AcceptedBinding** | LayerStack-0-issued or LayerStack-0-revalidated capability naming an `AcceptedVersion` | A public constructor or unchecked raw `VersionId` |
| **Head** | Named mutable selected reference | The accepted payload itself |
| **Root** | Named typed durable reachability reference | A filesystem root directory or mutable workspace |

Capitalize **Version**, **Head**, and **Root** when referring to these specific
LayerStack-0 concepts. Lowercase them when using the words generically.

The preferred product category is **sandbox Version engine**, and the concrete
owner is **LayerStack-0**. Preserve “selected-state store” only when quoting a
frozen Phase 00/01 field or historical source; new Phase 02+ prose should say
**selected-Version owner**, **LayerStack-0**, or **Version storage** as
appropriate. Do not use **State Store** as a product or component name.

## 2. The central vocabulary

| Term | Precise meaning |
|---|---|
| **Version** | An accepted complete immutable portable filesystem value identified by a `VersionId` and backed by one admitted payload closure. A Version is not a mount, process, workspace path, or history chain and needs no parent/layer reconstruction. |
| **Candidate** | Bounded complete portable facts offered for validation and admission. A Candidate is unaccepted and is not selected truth. |
| **Portable facts** | The complete validated facts allowed to define Version identity across hosts and runtime realizations: normalized relative paths, accepted entry types and metadata, symlink targets, file content, and schema/domain information selected by Phase 02. |
| **Canonical bytes** | Versioned, domain-separated, deterministic, unambiguous encoding of the complete portable fact set. |
| `VersionId` | Typed, versioned, domain-separated digest derived from the complete canonical byte stream. It may be computed before admission and does not prove equality or durable existence by itself. |
| **AcceptedVersion** | LayerStack-0 admission result proving that the complete canonical bytes and immutable payload closure for a `VersionId` were verified and durably accepted. |
| **AcceptedBinding** | LayerStack-0-created or LayerStack-0-revalidated capability naming an `AcceptedVersion` after admission, including full canonical-byte comparison when its `VersionId` was already occupied. |
| **Payload closure** | One physical complete immutable filesystem representation for accepted canonical bytes in one LayerStack-0 instance. |
| **Selected truth** | Accepted payloads plus valid durable Roots and Heads under the active LayerStack-0 generation. It is never a layer chain, live workspace, or observability projection. |

Use **Candidate** until admission succeeds. Canonicalization may derive a
`VersionId` before admission, but only successful admission creates an
**AcceptedVersion** and permits an accepted binding. After admission, product
prose may use **Version** or **accepted Version**. “Candidate Version” should be
avoided because it blurs this boundary.

Historical Phase 00 and Phase 01 documents may say `StateId`. That spelling is
a compatibility alias for `VersionId` only; ADR-002 changed the name without
changing the complete-content, collision, or admission semantics.

## 3. References and publication

| Term | Precise meaning |
|---|---|
| **Reference** | Small metadata that names an accepted binding without containing or copying payload data. Root and Head records are reference forms. |
| **Root** | Fixed typed durable reachability reference to an accepted binding. A Root is created if absent and removed only by exact comparison; it is never generically retargeted. A Checkpoint is the principal product Root kind. |
| **Head** | Mutable selected reference containing an accepted binding and monotone `HeadRevision`. It identifies the currently selected Version for its selector. |
| `HeadRevision` | Monotone OCC token associated with one Head. It distinguishes Head histories even when a Version repeats. |
| **Selector** | Bounded application-facing name used to identify a particular Head or typed reference target. It is not a host path. |
| **Reference-only transition** | One of Head create/exact replace/exact remove or fixed typed Root create/exact remove over an accepted binding, without opening the payload. Accepted-reference payload bytes read, written, and copied are all zero; metadata, coordination, and fence work is nonzero. |
| **Admission** | Validation, canonicalization, `VersionId` derivation, occupied-ID comparison, staging, and durable installation that turn a Candidate into an accepted immutable Version. Admission alone does not select the Version as Head. |
| **Publication** | Application-authorized operation that may admit a Candidate and then attempts exactly one conditional Head transition. |
| **Head transition** | Atomic replacement of one complete Head record after expected binding/revision validation. It is the sole OCC linearization point. |
| **OCC** | Optimistic concurrency control. A publisher supplies its expected Head and revision; if either is stale, the transition loses cleanly. |
| **Stale** | Typed outcome meaning the expected Head or revision no longer matches. Stale publication changes no Head and triggers no silent merge or rebase. |

Keep **admission** and **publication** distinct. A Candidate may be completely
admitted before its publisher loses OCC. The resulting complete but unreferenced
payload is safe bounded cleanup debt, not a partially published Head.

Do not call the OCC transition “consensus.” LayerStack-0 has one local
process/filesystem-exclusive transition authority; it is not a distributed
consensus protocol.

## 4. Agent and runtime vocabulary

| Term | Precise meaning |
|---|---|
| **Agent** | One application-controlled worker exploring from a selected Version. Agent identity and policy are not portable Version facts. |
| **Branch** | Product exploration context represented durably by exactly one Head, plus isolated temporary writable work and application context. Its Head is the only movable Branch selector and remains under the one LayerStack-0 OCC authority. |
| **Fork** | `CreateHeadIfAbsent` for a new Branch Head from an accepted binding. The accepted-reference portion has payload I/O `0/0/0`; runtime namespace readiness may perform separate metadata, mount, materialization, or effect work. |
| **Writable namespace** | Runtime-owned isolated view in which an agent may change files without modifying an accepted Version or another agent's work. |
| **Workspace** | Runtime-effect-owned live filesystem location/view used for Candidate work. It is mutable and is not selected truth. |
| **Runtime effects** | Workspace, OverlayFS, mount, namespace, execution, file descriptor, lease, process, and host-path facts owned outside portable identity. |
| **Checkpoint** | Fixed typed Root created for an already accepted binding. New Workspace content must first publish through Candidate admission; the subsequent Checkpoint creation remains reference-only and the Root never retargets. |
| **Rollback-to-existing** | `ReplaceHead(Expected::Exact(expected_head), checkpoint_binding)` for a Branch Head. It is not Root retargeting, reverse mutation of a payload, or a silent merge. |
| **Materialization** | Runtime preparation or reading of an immutable Version as a usable filesystem view. Materialization cost is outside the reference-only zero-payload claim. |
| **Rollout** | Application-owned agent exploration from a base Version. LayerStack-0 stores and publishes Versions; it does not choose rollout policy or scores. |
| **Winner** | Candidate selected by application policy for a publication attempt. OCC still decides whether that attempt can change the current Head. |

### Branch is a product concept, not a new truth owner

```text
Branch
  = exactly one durable Head over an accepted binding
  + runtime-owned writable namespace
  + application-owned agent/operation context

Branch is not
  = a mutable accepted Version
  = another durable Version authority
  = a layer chain
  = a Head update that bypasses OCC
```

## 5. EphCoW and zero-copy language

| Term | Precise use |
|---|---|
| **CoW / copy-on-write** | General technique in which an initially shared value is not copied until a write requires divergence. It is an established mechanism, not a newly invented primitive. |
| **EphCoW / Ephemeral Copy-on-Write** | LayerStack-0 architecture: reference-level CoW over complete immutable Versions, paired with isolated runtime-owned writable namespaces, immutable admission, and OCC publication. |
| **Zero-payload reference fork** | Exact selected claim: the reference operation reads, writes, and copies zero payload bytes for an already accepted binding. |
| **Zero-copy** | Shorthand permitted only when the operation and byte class are explicit. Prefer “zero-payload reference fork.” |
| **Isolated writes** | Writes occur in private runtime Candidate work and cannot mutate accepted payloads or another agent's writable namespace. |
| **Immutable outcome** | An accepted Version whose payload cannot be modified in place. It does not mean the Head can never move. |

The approved equation is:

```text
accepted-Version reference fork:
    payload bytes read    = 0
    payload bytes written = 0
    payload bytes copied  = 0
```

The same payload equation applies to all five accepted-reference lifecycle
operations. It does not cover Root/Head metadata, validation, locks, durability
fences, namespace construction, mounts, first read, file writes, Candidate
capture, canonicalization, hashing, admission, or cleanup.

Never use these phrases:

- “zero-copy writes”;
- “zero-I/O storage”;
- “zero-cost fork”;
- “instant sandbox” without a measured end-to-end definition;
- “checkpoint is always zero-copy”; or
- “immutable workspace.”

## 6. Content addressing, CAS, CDC, and sharing

The acronym **CAS** is ambiguous: it can mean **content-addressed storage** or
**compare-and-swap**. Avoid bare “CAS” in architecture and product documents.

| Term | Selected meaning and status |
|---|---|
| **Content addressing** | Selected at the complete-Version boundary: one complete canonical Candidate derives `VersionId`, and equal accepted canonical Versions converge on one occupied payload closure. |
| **Content-addressed storage** | Use only with scope, such as “complete-Version content-addressed storage.” It does not currently imply chunk-level cross-Version deduplication. |
| **Compare-and-swap** | If used, spell it out and tie it to the Head OCC transition. Prefer “conditional OCC Head transition” to avoid CAS ambiguity. |
| **CDC / content-defined chunking** | Proposed technique for finding reusable content ranges across changed files or Versions. It is not part of selected R0. |
| **Chunk** | Proposed sub-Version storage object in a possible CAS+CDC design. It is not a selected LayerStack-0 durable primitive. |
| **Manifest** | Proposed complete logical Version description for an object/chunk design. It is not the selected R0 payload model. |
| **Object DAG** | Proposed graph representation and reachability model. It is not selected and would add recovery and retirement obligations. |
| **Deduplication** | Selected only for exact-equal complete canonical Versions under the same occupied `VersionId`. Cross-Version unchanged-chunk reuse is not selected. |
| **Shared content** | Safe when describing many agents referencing the same accepted base Version. Do not use it to claim that different Versions share chunks or extents. |

The selected/proposed boundary is:

```text
selected now:
  complete immutable payload closure per Accepted Version / occupied VersionId
  equal complete Version -> one occupied payload
  Roots/Heads reuse accepted bindings
  reference transition -> zero payload I/O

not selected now:
  CDC
  cross-Version chunk sharing
  manifest/chunk physical truth
  object DAG or tracing GC
  custom lazy COW filesystem/view
```

CAS+CDC is an architecture family change, not merely a speed optimization. It
requires Phase 01 reopening before becoming a LayerStack-0 implementation or
branding claim.

## 7. Reflink, snapshots, OverlayFS, and legacy layers

| Term | Precise meaning | Relationship to LayerStack-0 |
|---|---|---|
| **Reflink** | Filesystem operation that clones file extents while initially sharing physical blocks. | Comparator and possible filesystem primitive, not the definition of EphCoW. Recursive whole-tree reflink still has tree/file work. |
| **Filesystem snapshot** | Filesystem-native root/subvolume snapshot, such as a native CoW filesystem operation. | Strong raw local-latency comparator; does not by itself provide portable Version identity, Head OCC, or the full Version lifecycle. |
| **Snapshot** | Informal word often overloaded across storage systems. | Prefer **Version**, **Fork**, or **Checkpoint** according to the exact operation. Use “snapshot” only when comparing with a specific filesystem mechanism. |
| **OverlayFS** | Linux runtime union filesystem with lower, upper, work, copy-up, and whiteout behavior. | Runtime effect only; its paths and delta mechanics are forbidden from portable identity. |
| **Copy-up** | Overlay/runtime behavior that creates a writable copy when a lower entry is modified. | Runtime implementation detail, not the selected durable Version representation. |
| **Layer** | Legacy durable delta/history concept or a runtime overlay component. | Never use as V2 complete-Version truth. Qualify it as “legacy layer” or “runtime overlay layer.” |
| **Layer depth** | Number of history/delta layers required to reconstruct a filesystem view. | Required V2 logical value is zero. |
| **Squash** | Legacy operation combining a layer chain to reduce depth. | Not part of the V2 core because a Version is already complete. |
| **Merge/rebase** | Combination or relocation of divergent Version histories. | Never performed silently by LayerStack-0 publication. Application policy may separately request explicit future semantics if product contracts authorize them. |

Use this differentiation sentence:

> **Reflink clones local extents. Legacy LayerStack reconstructs deltas.
> LayerStack-0 branches complete immutable sandbox Versions.**

Do not use “faster than reflink” until a matched benchmark identifies the exact
operation, comparator, hardware, filesystem, data shape, fan-out, cache state,
build, and percentile.

## 8. Durability, recovery, and cleanup

| Term | Precise meaning |
|---|---|
| **Staging** | Private bounded store area used to construct and validate an unaccepted Candidate. It cannot be named by a durable Root or Head. |
| **Payload-before-reference** | Durability rule: a complete accepted payload becomes durable before any new Root or Head may name it. |
| **Transition gate** | LayerStack-0's single process/filesystem-exclusive serialization point for selected-Version reference changes and final retirement checks. Candidate preparation may occur outside it. |
| **Read custody** | Bounded runtime-local protection for a captured immutable Version while it is read or materialized. It prevents premature retirement but is not a portable Version fact. |
| **Orphan payload** | Complete accepted payload currently named by no durable Root or Head and held by no read custody. It may arise when admission succeeds but OCC publication loses. It is cleanup debt, not a corrupt partial payload. |
| **Recovery** | Startup or restart process that validates durable records and exposes prior or complete new truth while cleaning or quarantining recognizable bounded debt. Ambiguity fails closed. |
| **Retirement** | Safe removal of an unrooted accepted payload after exact final Root/Head/read-custody revalidation under transition authority. Prefer this to generic “GC.” |
| **Cleanup debt** | Accounted bounded staging, orphan, or recovery work that can be processed repeatably. It must not grow without an enforced limit. |
| **Fail closed** | Refuse readiness or the requested operation when integrity, reachability, collision, durability, or resource safety cannot be established. |

Avoid **garbage collection** as the primary selected term. R0 selects exact,
bounded retirement over complete payload closures; it does not select an
unbounded object-graph tracing authority.

## 9. Identity boundaries

Portable identity describes the Version, not how one host happens to run it.

```text
portable Version facts                  runtime-private facts
----------------------                  ---------------------
normalized relative paths               host absolute paths
accepted entry types                    Docker/container IDs
accepted portable metadata              OCI runtime descriptors
symlink targets                         OverlayFS lower/upper/work paths
regular-file content                    mount IDs and options
schema/domain version                   namespaces and processes
                                        file descriptors and leases
                                        workspace/session IDs
                                        auth, audit, rollout, or MCTS data
                                        legacy parent/depth history
```

**Namespace isolation** means agents receive separate runtime views. It does not
mean namespace or mount identity becomes part of `VersionId`.

## 10. Migration vocabulary

| Term | Precise meaning |
|---|---|
| **Legacy import** | Temporary one-way decoding and admission of legacy data through normal V2 validation and store paths. |
| **Migration progress record** | Temporary restart aid written only after the corresponding permanent durability point. It is not a Checkpoint, Root, Head, or selected truth. |
| **Generation fence** | Monotone cutover control that ensures exactly one writable selected-Version truth. |
| **One writable truth** | At any migration stage, either legacy or V2 may be authoritative for writes, never both. |
| **Compatibility observation window** | Product-owner-selected period after cutover before compatibility code can be removed. It does not authorize dual writes. |
| **Cutover** | Controlled switch of writable authority to V2 after offline proof and generation fencing. It is not migration execution by the storage branding layer. |

## 11. Marketing metaphors

| Word | Allowed use | Boundary |
|---|---|---|
| **World** | Short public metaphor for a complete sandbox Version | Not an API type, identity field, or stronger durability promise |
| **Branch** | Agent-friendly expression for isolated exploration from a Version | Not proof of a Git-style commit DAG or merge model |
| **Fork** | Branching from an accepted Version | Qualify the zero-copy claim as the durable reference portion |
| **Outcome** | Accepted result of agent work | Becomes durable truth only after admission and successful publication/rooting |
| **History** | Human description of successive Head choices | Not a layer chain or guarantee that every unrooted Candidate is retained |

Recommended public line:

> **Fork the reference. Isolate the work. Publish one outcome.**

## 12. Open product decisions are not terminology

Terminology must not silently resolve these product-owner decisions:

| Decision | Still open | Stable architectural seam |
|---|---|---|
| `DEC-001` | Whether exact `file_blame` remains | Auditability remains an application-owned side channel, not portable Version identity. |
| `DEC-011` | Cutover observation-window duration | Changes compatibility removal timing, never the one-writable-truth rule. |
| `DEC-017` | Sessionless write/edit and exact V2 file-operation/target set, including `file_list` | Application may reject or construct a Candidate; accepted payloads cannot be edited in place. |
| `DEC-018` | Auth/revoke ordering under races | Application owns authorization ordering; store OCC remains independent and mandatory. |

Do not redefine these unresolved behaviors through a convenient word such as
“write,” “checkpoint,” “authorized,” or “compatible.”

## 13. Quick usage guide

| Instead of | Prefer |
|---|---|
| “LayerStack-0 copies a sandbox for each agent.” | “LayerStack-0 gives each agent an isolated Branch from an accepted Version.” |
| “Fork is free.” | “The accepted-Version reference fork copies zero payload bytes.” |
| “The VersionId proves the content is equal.” | “The VersionId addresses the Candidate; occupied IDs require full canonical-byte comparison.” |
| “The workspace is the state.” | “The workspace contains temporary Candidate work; an accepted Version is durable selected truth.” |
| “Publish writes the files into the Head.” | “Admission makes a Version durable; publication conditionally changes the small Head reference.” |
| “Losing agents are merged.” | “A stale publisher loses without Head mutation, merge, or rebase.” |
| “LayerStack-0 uses CAS.” | “LayerStack-0 uses complete-Version content addressing and an OCC Head transition.” |
| “EphCoW deduplicates chunks.” | “Selected EphCoW reuses an Accepted Version binding; cross-Version CDC chunk sharing remains proposed.” |
| “EphCoW is faster than reflink.” | “EphCoW defines accepted-reference payload I/O `0/0/0`; no comparative latency target or matched result has been selected.” |
| “We garbage-collect snapshots.” | “LayerStack-0 retires unrooted Versions after exact reachability and read-custody revalidation.” |
| “A Version is ephemeral.” | “Writable agent work is ephemeral; an accepted rooted Version is durable and immutable.” |

## 14. References

- [Brand landing page](README.md)
- [Architecture innovation narrative](architecture-innovation.md)
- [Selected V2 architecture](../architecture_design.md)
- [ADR-002 — `VersionId` naming](../design/decisions/ADR-002-version-id-naming.md)
- [Version identity design](../design/02-state-identity.md)
- [LayerStack-0 Version storage design](../design/03-state-store.md)
- [Algorithms and call flows](../design/04-algorithms-and-call-flows.md)
- [EphCoW versus reflink analysis](../complexity-analysis/ephcow-vs-reflink-performance-analysis.md)
