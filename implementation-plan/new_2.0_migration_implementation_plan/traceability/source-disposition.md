# Legacy-source disposition

Status: **DRAFT TRACE — DEPLOYED REALITY STILL REQUIRES PHASE 0**

## Vocabulary

- `RETAIN-RESULT`: preserve an externally required invariant after deployed
  verification; do not inherit its old mechanism.
- `REFRAME`: keep the need but move it to one SRP owner or express it as a law.
- `OPEN-RETEST`: unselected candidate under the frozen judge.
- `MIGRATION-ONLY`: temporary compatibility path obeying the one explicit
  dependency graph in `design/migration-cutover.md`.
- `REMOVE`: absent from V2 unless a later ADR proves necessity.
- `EVIDENCE-ONLY`: provenance, counterexample, or measurement with no design
  authority.

## Requested source files

Paths are relative to old `implementation-plan/2.0 migration/`; exact hashes
are in `evidence/source-manifest.md`.

| Source | Disposition | Current owner/use |
|---|---|---|
| `system-design/index.md` | `REFRAME` | authority map and three operational envelopes with 11 causal gates |
| `system-design/system_requirements.md` | `RETAIN-RESULT` plus prohibition audit | `design/requirements.md`; mechanisms remain open |
| `system-design/api_methods.md` | `EVIDENCE-ONLY` legacy 26-row proposal; every change `OPEN-RETEST` | `design/public-api.md` keeps the pinned minimum 27 public/tool operation names (18 manager/runtime + 8 observability + HTTP-only `file_list`), separately classified health/forward/readiness surfaces, the legacy 26-row proposal, the candidate 25-row ledger, and the final open population distinct |
| `system-design/architecture/overall_architecture.md` | `OPEN-RETEST` | Phase 1A tournament/`DEC-012`; zero-addition R0 in-place reuse is the first challenger, not a winner or theorem |
| `system-design/architecture/mpla_demonstrations.md` | `EVIDENCE-ONLY` | fixtures/falsifiers only; never production scaffold |
| `system-design/components/backend_adapters.md` | `REFRAME` | runtime-native effect privacy and conformance laws; R0 reuses current owners and adds no aggregate seam |
| `system-design/components/canonical_state.md` | `RETAIN-RESULT`, organization and methods open | deterministic portable facts/identity behavior; no mandatory named module/package/component |
| `system-design/components/durable_store.md` | `OPEN-RETEST`/`REFRAME` | repurpose the existing selected-storage ownership home first; no generic repository, port, plugin, or new Store seam by default |
| `system-design/components/lifecycle_engine.md` | `OPEN-RETEST` | existing application decision-owner roles; no new component or durable truth by default |
| `system-design/components/workspace_engine.md` | `OPEN-RETEST`/`REFRAME` | current Linux effects remain with existing workspace/overlay/namespace owners unless Phase 1A proves a new unit |
| `pmss_algorithms.md` | `EVIDENCE-ONLY`/`OPEN-RETEST` | six historical custom mechanisms have zero winner status; joint Phase 1A evaluates standard-first complete topology × method profiles |
| `system-design/refine/index.md` | `EVIDENCE-ONLY` | provenance and review input |
| `system-design/refine/phase_1_architecture_review.md` | `EVIDENCE-ONLY`/`OPEN-RETEST` | candidate/falsifier record |
| `system-design/refine/phase_2_primary_source_research.md` | `EVIDENCE-ONLY` | verify sources in Phase 0; no method acceptance |
| `system-design/refine/phase_3_resource_scale_review.md` | `RETAIN-RESULT` for falsifiable limits; methods open | resource requirements/gates and P4 provenance warning |
| `system-design/refine/phase_4_review_handoff.md` | `EVIDENCE-ONLY` | provenance and unresolved risks |
| `system-design/refine/phase_5_writer_finalization.md` | `OPEN-RETEST` | actual-writer and fleet-fence inventory |
| `system-design/refine/phase_6_acceptance_audit.md` | `EVIDENCE-ONLY` | counterexamples and hard-gate design |

## Architecture deletion disposition

| Historical/worked claim | Aggressive disposition | Proof still required |
|---|---|---|
| four domain components plus Admission service | **comparison evidence only; production count `OPEN`** | Phase 1A inventories every existing/new unit and justifies each retained boundary by deletion counterexample |
| exactly two new V2 components/authorities | **falsified** | enumerate semantic reasons to change, then count writers, effects, decisions, migrations, edges, packages, components, and processes independently |
| Canonical State as separate component | **remove mandatory component/module** | keep deterministic pure behavior; retain/extract organization only after compile, consumer, dependency, and deletion evidence |
| durable Store behind generic repository/port | **remove new abstraction by default** | rewrite the existing ownership home; add one boundary only after R0 fails a named invariant and the added graph wins its full ledger |
| one new `WorkspaceBackend` component | **remove** | existing workspace/overlay/namespace/execution/file owners remain visible; add no aggregate runtime seam without a concrete deletion counterexample |
| stateful Lifecycle authority | **retest; use existing application roles first** | inventory authorization/order/retry/recovery/reconciliation decision ownership without inventing durable truth |
| volatile Admission/Governor service or global ledger | **remove; reopen placement** | each owner charges local debt first; any aggregate placement must be proved from the actual acquisition graph |
| multiple adapter/facade/plugin families | **remove** | reuse, narrow, or fuse the actual existing effect calls first; the exact call graph remains open and each abstraction needs an incompatible independent consumer or conformance requirement |
| separate state-service process | **remove by default** | `DEC-002` requires measured privilege/fault/scaling benefit including protocol, queue, retry, cgroup, latency, and operations cost |
| OCI-named core and future-runtime compatibility by interface assertion | **remove** | state meaning stays portable; Linux details stay private; disposable WASI/Firecracker spikes may falsify semantics |
| historical `crates/sandbox-runtime/layerstack-core` as a mandatory canonical boundary | **do not project into the current graph** | clean e497 contains no such package; any proposal to create an equivalent package is a new-boundary candidate and must win compile, consumer, dependency, placement, and deletion-counterexample tests |
| fixed traits, calls, records, fields, indexes, caches, workers | **open/delete/derive** | exact caller, transaction, crash, recovery, migration, resource, and cleanup evidence must justify each |

Current production counts are not fixed. R0 proposes zero mandatory additions:
rewrite the existing selected-storage ownership home and call current
runtime-effect owners from existing application owners. All exact semantic,
edge, authority, module, package, component, process, deployable, and method
counts remain open until Phase 0 inventory and Phase 1A `DEC-012` acceptance.
Clean e497 instead makes actual-source transformations mandatory: generate
package-disposition and placement variants only for packages, normal/build
edges, source sites, and consumers that the pinned tree proves exist. Historical
`layerstack-core` and MPLA material may motivate a signed challenger, but it
creates neither a current package nor a deletion obligation. Adding any
equivalent boundary is a candidate, not a conclusion.

## Method and storage disposition

| Old mechanism/result | Disposition | Reason |
|---|---|---|
| `C1/C2/C3/S1/S3` algorithms plus `S2` crash protocol | `OPEN-RETEST`; zero winners | six historical custom mechanisms, no frozen V2 selection |
| owner-prompted 21-family hostile census | `EVIDENCE-ONLY` checklist | mixes results, transitions, methods, and conditional work; not an algorithm count |
| `R`, FastCDC, fixed `HEAD`/Catalog/arena, branch counts | `OPEN-RETEST` or `REMOVE` | representation-dependent or unsupported winner assumptions |
| complete-state identity and deterministic canonicalization | `RETAIN-RESULT`; encoding/digest open | semantic law independently vectored and verified |
| exact zero-copy checkpoint COW | `RETAIN-RESULT` | after exact canonical-byte equality establishes an accepted no-alias binding, one selected-state immutable dependency closure serves any root multiplicity; every whole reference transition has exactly zero selected-state immutable payload read, write, and copy, while runtime-private realization remains separately and fully charged; unequal bytes under one candidate digest fail closed before binding |
| generic `2x` disk/memory claim | `REMOVE` | only measured simultaneous write-new-before-delete-old overlap may approach 2x; streaming/reference-switch/in-place remain candidates |
| layers/squash/autosquash/remount in steady state | `REMOVE`; readers `MIGRATION-ONLY` | V2 complete state has no logical layer history; final publication gate cannot carry runtime-effect lifecycle work |
| persistent refcount/cache, hidden DB/WAL, generic plugin/merge engine | `REMOVE` | added truth/state/dependency is unproved; reopen only by explicit requirement and ADR |
| reflink/clone-ioctl or FUSE use in any role | `REMOVE`/forbidden, including private or optional acceleration | source-to-binary evidence rejects reflink-specific ioctls/libraries and FUSE dependencies, mounts, helpers, and processes; exact COW is semantic |
| private acceleration and hard-link boundary | `OPEN-RETEST` only for runtime-internal OverlayFS, native or VM snapshots, private storage-driver acceleration, and deduplication hints | disabling every acceleration preserves all semantic/durability/admission/cleanup/resource gates and enabling it adds no privilege; hard links only preserve one real link group inside one private captured filesystem and never accelerate copying or share writable bytes |
| Stage 4.6 as implementation base/winner/reproducible comparator/aggregate 100x pass | `EVIDENCE-ONLY` negative context | retained dirty receipts commit to identities but omit patch bytes/source archive/executable; matched `R_stage46` is incomparable until attested rerun/reconstruction |

## Remaining Phase 0 work

Before any type, schema, cache, worker, or method freezes, complete the deployed
field/writer/caller/authority/process ledger; public API matrix; live-writer and
fleet-fence map; exact MCTS contract; Cartesian terminal-resource matrix; unsafe
and system-boundary audit; P4 evidence gap and attested comparator plan; and
independent oracle. Missing facts block Phase 1. Historical prose never fills
them in.
