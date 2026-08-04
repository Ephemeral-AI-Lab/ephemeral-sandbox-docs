# Phase 5 — Writer finalization

> Owner: separate writer  
> Prerequisite: Phase 4 PASS and complete Writer Handoff  
> Allowed writes: the ten design documents and this phase's Handoff record  
> Output: Writer Completion Packet

## Objective

Apply the approved decisions consistently across the existing design set. Do
not reopen architecture decisions, add documents or implement code.

## Allowed files

Edit only:

- ../index.md
- ../system_requirements.md
- ../api_methods.md
- ../architecture/overall_architecture.md
- ../architecture/mpla_demonstrations.md
- ../components/canonical_state.md
- ../components/durable_store.md
- ../components/workspace_engine.md
- ../components/lifecycle_engine.md
- ../components/backend_adapters.md

Do not edit other refine specifications. Only this phase's Handoff record may
change. Preserve unrelated user changes.

## Authority map

| Document | Must own |
|---|---|
| index.md | Selected design, navigation, exact counts and provenance |
| system_requirements.md | Hard gates, prohibitions and resource bounds |
| api_methods.md | Public signatures, outcomes and lifecycle semantics |
| overall_architecture.md | Tournament, final boundaries and dependency graph |
| mpla_demonstrations.md | Visual and comparative evidence |
| canonical_state.md | Identity, canonical facts, tree, chunks and attribution |
| durable_store.md | Objects, catalog, commit, replay, leases and GC |
| workspace_engine.md | Projection, fencing, capture and candidate preparation |
| lifecycle_engine.md | Session, checkpoint, rollback, fork and destroy policy |
| backend_adapters.md | Fact translation and Docker, WASI, Firecracker contracts |

Each definition has one authority. Other documents link to it rather than
redefine it.

## Writing rules

- Lead with the selected storage decision and why it is minimal.
- Keep the API and semantic requirements unchanged.
- Use the exact names and counts from the Writer Handoff.
- Remove obsolete mechanisms and duplicated authority.
- Give every component one responsibility and narrow interface.
- Explain what invariant prevents further reduction.
- State that the catalog is a purpose-built immutable index, not a database.
- Do not introduce database terminology except in rejection comparisons.
- Keep cache absent from the baseline.
- Cite direct primary sources beside supported decisions.
- Be concise: if 50 words are enough, do not use 200.

## Custom mechanism template

For every retained non-trivial custom algorithm or protocol include:

| Field | Required content |
|---|---|
| Purpose | One responsibility |
| Optimization target | ARCH, ALG, TIME, DISK or MEM |
| Inputs and outputs | Typed boundary |
| Preconditions | Required state and permits |
| Invariants | What must always hold |
| Pseudocode | Concise, only when it clarifies behavior |
| Commit point | Linearization or durability point |
| Failure behavior | Crash, corruption and replay |
| Complexity | Worst-case time and I/O |
| Resources | Memory, FDs, disk and inodes |
| Implementation | Adopt, borrow or minimal custom |

Do not add pseudocode for a wrapper, syscall sequence with no policy, or simple
lifecycle getter.

## Required visual evidence

Use the minimum useful Mermaid diagrams for:

- component ownership and dependency direction;
- canonical identity versus physical location;
- durable segment and catalog layout;
- capture and publication dataflow;
- sparse versus dense index update;
- checkpoint, rollback, fork and commit;
- atomic commit and crash recovery;
- aggregate resource admission;
- backend fact-profile boundary.

Every diagram states its conclusion. Remove repeated diagrams.

Use compact tables for:

- architecture and index candidates;
- component deletion and replaceability;
- custom versus adopted mechanisms;
- time, I/O, disk, memory, FD and implementation complexity;
- crash outcomes;
- quota capability levels;
- backend fact profiles;
- optimization targets and evidence.

## Claim discipline

Label every number as:

- analytical bound;
- project measurement;
- external measurement;
- target;
- estimate;
- hypothesis.

Do not present historical proof-of-concept performance as performance of the
new design. Do not claim a cache-on result for the cache-off baseline.

## Status

Keep all ten documents Proposed for review. Only Phase 6 may mark them Accepted.

## Writer Completion Packet

Return:

1. exact files changed;
2. definition-ownership map;
3. final component and custom-mechanism counts;
4. removed, merged and replaced mechanism list;
5. citation summary;
6. diagram and comparison-table inventory;
7. requirements and API traceability confirmation;
8. remaining concerns, if any;
9. writer task path and session ID.

## Pass gate

Phase 5 passes only when:

- only the ten allowed files changed;
- every Writer Handoff decision is implemented;
- no duplicate authoritative definition remains;
- counts agree across documents;
- no prohibited mechanism is selected;
- all resource and crash bounds are explicit;
- all links and diagrams are ready for audit;
- no TODO, TBD or writer-made architecture decision remains.

## Handoff record

> Mutable, append-only execution record. Complete this after gate evaluation.
> On a rerun, append Attempt 2 or later; do not overwrite an earlier attempt.

### Attempt 1

| Field | Value |
|---|---|
| Status | NOT_STARTED |
| Gate | NOT_EVALUATED |
| Owner task path | Not assigned |
| Owner session ID | Not assigned |
| Started | Not recorded |
| Completed | Not recorded |
| Next phase | Phase 6 — Final acceptance audit |
| Next phase may start | NO |

### Subagents

| Writing or verification scope | Task path | Session ID | Result |
|---|---|---|---|
| Not assigned | — | — | — |

### Writing synthesis

- Not started.

### Sources applied

- Not recorded.

### Decisions implemented and results

- Writer Completion Packet: not produced.
- Files finalized: not recorded.
- Final component and mechanism counts: not recorded.
- Definitions centralized or removed: not recorded.
- Diagram and comparison inventory: not recorded.

### Blockers and returned work

- None recorded.

### Files changed

- Not recorded.

### Output for Phase 6

- Auditor task path and session ID: not assigned.
- Claims requiring special verification: not recorded.
- Known residual risks: not recorded.
- Writer Completion Packet reference: not recorded.

### Attempt 2

| Field | Value |
|---|---|
| Status | PASS |
| Gate | PASS — all Phase 5 pass conditions are satisfied |
| Owner task path | `/root/phase5_writer` |
| Owner session ID | `019fc0b8-5c39-7a81-962f-ac4f1c318c74` |
| Started | 2026-08-02 (writer session; exact start instant was not separately recorded) |
| Completed | 2026-08-02T05:58:48Z |
| Next phase | Phase 6 — Final acceptance audit |
| Next phase may start | YES |

### Subagents

| Writing or verification scope | Task path | Session ID | Result |
|---|---|---|---|
| Writer-owned subagents | None | — | Verification completed locally; Phase 4 audit evidence was consumed as upstream input, not delegated writer work |

### Writing synthesis

- Selected the Portable Merkle State Store: content-addressed immutable state,
  one complete `StateId`, structural sharing, and a single mandatory catalog
  `HEAD` without layers, logical deltas, squash, autosquash, or remount.
- Integrated every Phase 4 Attempt 3 correction, including Store-owned root
  discovery, finite root and child bounds, the two-bit mark trace, bounded edge
  sorting, conservative accounting, exact convergence order, root-control
  reserves, and the prohibition on reflink and FUSE in every profile.
- Kept all ten design documents at `Proposed for review`; acceptance remains a
  Phase 6 authority.

### Sources applied

- Phase 4 handoff Attempts 1 through 3 and their exact audit provenance.
- Canonical-state sources: RFC 8949, BLAKE3, FastCDC, compressed Patricia
  tries, POS-Tree/CDMT, Myers difference, and rsync rolling-delta research.
- Durability and lifecycle sources: Bayer and McCreight B-trees, POSIX rename
  and synchronization contracts, ALICE and CrashMonkey crash-consistency
  research, Git pack/repack design, RFC replay guidance, and Linux RCU.
- Adapter and isolation sources: `openat2`, Linux quota and cgroup contracts,
  OCI and Docker specifications, WASI, and Firecracker documentation.
- Stage 4.6 measurements were retained only as historical evidence; no result
  was relabeled as performance of the selected baseline.

### Writer Completion Packet

#### 1. Exact files changed

The writer finalized exactly these ten design files:

1. `index.md`
2. `system_requirements.md`
3. `api_methods.md`
4. `architecture/overall_architecture.md`
5. `architecture/mpla_demonstrations.md`
6. `components/canonical_state.md`
7. `components/durable_store.md`
8. `components/workspace_engine.md`
9. `components/lifecycle_engine.md`
10. `components/backend_adapters.md`

This Attempt 2 record was appended to
`refine/phase_5_writer_finalization.md` as required execution metadata. The
writer did not alter any other refine record or any unrelated dirty file.

#### 2. Definition-ownership map

| Document | Sole authoritative definition |
|---|---|
| `index.md` | Selected design, navigation, exact counts, and provenance |
| `system_requirements.md` | Hard gates, exact analytical formulas, prohibitions, and resource bounds |
| `api_methods.md` | Exact public method set, signatures, results, errors, and API-visible semantics |
| `architecture/overall_architecture.md` | Candidate tournament, final boundaries, and dependency direction |
| `architecture/mpla_demonstrations.md` | Non-normative visual and comparative evidence linked to normative owners |
| `components/canonical_state.md` | Identity, canonical facts, C1 tree, C2 chunks, and C3 attribution |
| `components/durable_store.md` | Object custody, Catalog, S1 index, S2 commit/recovery, S3 delta, replay, and GC |
| `components/workspace_engine.md` | Non-component workflows for projection, fencing, capture, and candidate preparation |
| `components/lifecycle_engine.md` | Session, checkpoint, rollback, fork, destroy, and semantic-root policy |
| `components/backend_adapters.md` | Fact translation, enforcement capability, and Docker/WASI/Firecracker profiles |

#### 3. Final counts

| Item | Final count |
|---|---:|
| Domain components | 4 |
| Shared permit-only mechanisms | 1 (`Resource Admission`) |
| Workspace Engine components | 0 |
| Retained custom mechanisms | 6 (C1–C3 and S1–S3) |
| Catalog namespaces | 8 |
| Catalog roots | 1 |
| Mandatory `HEAD` selectors | 1 |
| Catalog arenas | 2 (`Selected` plus mutually exclusive `Auxiliary`) |
| Lifecycle API methods | 18 |
| Runtime API methods | 8 |

The four domain components are Canonical State, Durable Store, Lifecycle, and
Backend Adapters. The eight namespaces are `Sandbox`, `Session/Mutable`,
`Session/Terminal`, `Checkpoint`, `CheckpointPin`, `Receipt`, `OwnerSlot`, and
`ObjectCatalog`.

#### 4. Removed, merged, and replaced mechanisms

- Removed layers, parent chains, logical deltas, squash, autosquash, remount,
  mutable cache state, database/WAL/MVCC/KV selection, resident live maps,
  persistent reference counts, publishing states, and hidden accounting
  ledgers.
- Rejected reflink and FUSE even as optional backend behavior.
- Merged workspace orchestration into explicit Lifecycle, Durable Store, and
  Backend Adapter workflows; `workspace_engine.md` is therefore a workflow
  description and does not define a fifth component.
- Replaced fixed-fanout canonical trees with C1 compressed Patricia/Merkle
  directories and C2 `ContentTree-v1` content-defined trees.
- Replaced heuristic attribution with C3 deterministic occurrence-rank
  attribution.
- Replaced general storage-index machinery with S1, a fixed-purpose immutable
  copy-on-write B+ Catalog.
- Replaced multi-selector publication and permissive recovery with S2
  single-`HEAD`, dependency-first commit and fail-closed recovery.
- Replaced unrestricted delta behavior with S3 `AlignedSpliceDelta-v1` and
  its exact base-pin sequence.
- Replaced renewable leases and dynamic owner allocation with 16 fixed
  `OwnerSlot` records and nonrenewable 30-second read permits.

#### 5. Citation summary

Primary specifications and research are cited next to the claims they support.
The citation set covers canonical encoding and hashing, content-defined
chunking and ordered Merkle structures, bounded delta construction, immutable
B+ indexing, atomic publication and crash recovery, replay safety, epoch
reclamation, path confinement, quota/cgroup enforcement, container contracts,
WASI, and Firecracker. Comparative and historical material is explicitly
labeled and does not own normative behavior.

#### 6. Diagram and comparison-table inventory

| Document | Mermaid diagrams | Markdown tables |
|---|---:|---:|
| `index.md` | 1 | 6 |
| `system_requirements.md` | 0 | 12 |
| `api_methods.md` | 0 | 9 |
| `architecture/overall_architecture.md` | 6 | 6 |
| `architecture/mpla_demonstrations.md` | 16 | 5 |
| `components/canonical_state.md` | 1 | 8 |
| `components/durable_store.md` | 4 | 14 |
| `components/workspace_engine.md` | 2 | 2 |
| `components/lifecycle_engine.md` | 1 | 5 |
| `components/backend_adapters.md` | 1 | 4 |
| **Total** | **32** | **71** |

Every Mermaid diagram has an immediately following conclusion. All Mermaid
graphs are acyclic where they express dependency or process direction, and all
Markdown fences are balanced.

#### 7. Requirements and API traceability

- The public surface remains exactly 18 lifecycle methods and 8 runtime
  methods; no helper or decision-table row was promoted into an API method.
- The design uses only `StateId`, `HeadRevision`, `StoreSequence`, and
  `ArenaId` as version terms.
- Replay is exactly 16 owners × 64 slots × at most 512 canonical framed bytes:
  1,024 retained results and 512 KiB before framing. `ReplayExpired` never
  executes the operation.
- C1 bounds child records with `R_child_max = 512`; S1 uses 16 KiB nodes,
  half-full occupancy, `H <= 8`, and two arenas bounded by `4C`; S2 owns the
  one-epoch mutation gate; S3 distinguishes logical and physical liveness.
- The Store discovers semantic roots from its own Catalog state. Optional
  finite TTL roots are only external identifiers owned by the Store and cannot
  replace manual or in-use checkpoints.
- The mark trace uses the exact non-sparse two-bit header, checksum, state
  transitions, summaries, and bounded-memory full-scan restart rules.
- Edge sorting uses the exact `q_run`, `m`, `G`, two-work-file, control-file,
  80-byte-record, three-inode, fan-in-eight, and pass-bound formulas.
- Conservative capacity accounting charges selected bytes, every unselected
  candidate, every `OwnerSlot` byte and inode, complete accepted root workflows,
  and the simultaneous maintenance byte and inode reserves.
- Every `StoreSequence`-changing final commit returns `RetryLater` while the
  mutation gate is held. Normal and emergency GC follow the exact convergence
  order and restore writable reserve before admitting ordinary writers.
- Sandbox destroy, checkpoint removal, and all session `AdapterClose` cuts
  have complete `D_root_ctl` and `I_root_ctl` workflow effects, including
  replay and no-effect outcomes.
- Validation found 58 local Markdown links and anchors with zero failures,
  ten exact `Proposed for review` status lines, zero TODO/TBD/FIXME markers,
  balanced fences, and no missing diagram conclusions.

#### 8. Remaining concerns

There is no Phase 5 writing blocker. The remaining work is acceptance and
implementation qualification:

- Phase 6 must independently audit the Attempt 3 trace, edge-sort, admission,
  root-control, and crash-recovery proofs.
- Stage 4.6 historical cgroup measurements did not satisfy the 96 MiB target;
  that is an implementation-qualification risk, not evidence against the
  analytical design bound.
- Exact numerical instantiation of root-control reserves depends on the frozen
  key widths, fanout bounds, and adapter facts used by an implementation. The
  normative formulas and fail-closed admission rule are complete.

#### 9. Provenance

| Role | Task path | Session ID |
|---|---|---|
| Phase 5 writer | `/root/phase5_writer` | `019fc0b8-5c39-7a81-962f-ac4f1c318c74` |
| Phase 4 lead | `/root` | `019fc04c-cc15-7bd0-9f32-15e944d54659` |
| Phase 4 semantic/GC audit | `/root/semantic_gc_algorithm_audit` | `019fc0c5-d6eb-78e0-a26b-56160fb65b1d` |
| Phase 4 trace proof audit | child of semantic/GC audit | `019fc0d5-d5fc-7da1-95e2-6416a4a5c3de` |

### Decisions implemented and results

- Writer Completion Packet: produced in Attempt 2 above.
- Files finalized: all ten authorized design files.
- Final architecture: 4 domain components, 1 shared permit-only mechanism,
  0 Workspace Engine components, and 6 retained custom mechanisms.
- Definitions centralized or removed: complete; each normative definition has
  one owner and comparative documents link back to it.
- Diagram and comparison inventory: 32 Mermaid diagrams and 71 Markdown
  tables, with direct conclusions and balanced fences.
- Gate result: PASS.

### Blockers and returned work

- None.

### Files changed

- The ten design files listed in Writer Completion Packet section 1.
- This append-only Attempt 2 handoff record.
- No unrelated file was touched by the writer.

### Output for Phase 6

- Auditor task path and session ID: not yet assigned by the lead.
- Claims requiring special verification: the exact Attempt 3 two-bit trace,
  edge-sort, maintenance-reserve, root-control, `AdapterClose`, mutation-gate,
  and GC-convergence rules; exact component, mechanism, namespace, and API
  counts; and retained `Proposed for review` status.
- Known residual risks: implementation memory qualification at 96 MiB and
  independent numerical instantiation of admission bounds.
- Writer Completion Packet reference: Phase 5 Attempt 2, sections 1 through 9
  above.
- Phase 6 may start: **YES**.
