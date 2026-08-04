ALGORITHM_PACKAGE: ALIGNED_WITH_R0

# LayerStack-0 algorithm package

**Date:** 2026-08-04  
**Selected architecture:** R0 — LayerStack-0 rewrite-in-place,
filesystem-native complete-Version storage  
**Document status:** design contract; specified but not implemented,
benchmarked, qualified, or production-ready

This package fixes how the selected Phase 01 architecture composes. It does not
repeat architecture selection. No source evidence reviewed for this package
invalidates an R0 hard rule, so Phase 01 remains closed.

## 1. Authority order

Conflicts are resolved in this order:

1. The product [PRD](../PRD.md), especially its hard rules.
2. Measured e497 evidence frozen by [Phase 00](../phases/00-freeze-rules/SPEC.md).
3. The Phase 01 [selection input](../phases/01-choose-design/SPEC.md).
4. The accepted [architecture output](../architecture_design.md) and accepted
   [ADR register](../design/decisions/README.md).
5. The Phase 02 [Version identity PRD](../phases/02-state-identity/PRD.md) and
   Phase 03 [LayerStack-0 storage PRD](../phases/03-state-store/PRD.md).
6. The detailed [design package](../design/README.md).

The `implementation-plan/` tree is historical or evidentiary only. It cannot
override the product PRD, the selected architecture, or accepted ADRs.

## 2. Product-source seal

The product worktree was inspected read-only after its `AGENTS.md` and
`CLAUDE.md` were read. The Phase 01 seal commands returned:

```text
path:   /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
branch: codex/new-2.0-storage-core
HEAD:   e4974d1f9aac702b35e052629cb070c897989352
status: ## codex/new-2.0-storage-core...origin/main
dirty:  no
drift:  none
```

The expected branch and recorded HEAD match, and `git status --short --branch`
reported no changed or untracked product files. Source-placeability conclusions
therefore do not carry `OPEN: BASE_DRIFT`.

## 3. Evidence ledger

| Label | Package use |
|---|---|
| `SOURCE-VERIFIED` | The e497 source seal, current package placement and dependency direction, current ownership boundaries, and the presence of an existing writer-lock plus atomic-write/durability primitive family are source-backed Phase 00/01 evidence. |
| `SPIKE-VERIFIED` | None. No disposable spike was needed or run for this algorithm package. |
| `INFERRED` | The V2 identity, admission, reference, OCC, custody, recovery, retirement, migration, and bounded-resource algorithms are design deductions from the selected R0 contract. They still require Phase 02/03 implementation and proof. |
| `OPEN` | Exact Phase 02 codec/hash/limits and exact Phase 03 filesystem mechanics/bounds remain `OPEN_WITHIN_R0`; the four product-owner decisions remain `OWNER_DEC_OPEN`. |

Stage 4.6 remains `INCOMPARABLE`. Historical measurements lack a comparable
source closure and matched rerun provenance; this package makes no benchmark
winner or V2 latency, throughput, storage-efficiency, or production-performance
claim.

The zero-payload correctness demonstration has correctness result `NOT_RUN`.
The performance demonstration has final verdict `TARGET_UNSELECTED`: it
defines an executable proof matrix, but no owner-approved quantitative target
or qualified run exists. Only structural requirements are `INFERRED`; no
numerical result is promoted to `SPIKE-VERIFIED` or `BENCHMARK-QUALIFIED`.

## 4. Locked terminology and authority chain

```text
Candidate
  -> VersionId
  -> AcceptedVersion
  -> AcceptedBinding
  -> Head + HeadRevision or typed Root
```

| Term | Normative meaning |
|---|---|
| **LayerStack-0** | The V2 sandbox Version engine and sole selected-Version owner, implemented by rewriting `sandbox-runtime-layerstack`. |
| **EphCoW** | Reference-level copy-on-write over AcceptedBindings plus runtime-owned isolated writable Workspaces. |
| **Version** | One accepted complete immutable portable filesystem value. |
| `VersionId` | Typed content-derived Candidate identity only; never equality, existence, durable admission, or reference authority by itself. |
| **AcceptedVersion** | LayerStack-0-verified durable admission of canonical bytes and exactly one complete immutable payload closure. |
| **AcceptedBinding** | A LayerStack-0-issued or revalidated capability naming an AcceptedVersion. |
| **Head** | Mutable selected reference containing an AcceptedBinding and a monotone `HeadRevision`. |
| **Root** | Fixed typed durable reachability reference containing an AcceptedBinding. |
| **Branch** | Product exploration context: accepted starting binding, application context, and runtime-owned isolated Workspace. |
| **Checkpoint** | Product restore point represented by a typed Root. |
| **Workspace** | Mutable runtime-effect-owned filesystem view; never Version identity or selected truth. |

Historical terms such as `StateId`, “state store,” “State Store,”
“selected-state owner,” PMSS, or raw digest references do not name new V2
types, APIs, metrics, tests, or authorities. Stable historical folder slugs may
remain in links.

## 5. Ownership map

```text
application owners
  authorization, request ordering, expected Head capture,
  rollout/MCTS policy, scores, product orchestration
                    |
                    v direct calls
LayerStack-0: sandbox-runtime-layerstack
  canonical admission boundary, complete immutable payloads,
  AcceptedBindings, Roots, Heads, one OCC transition,
  recovery, retirement, bounded cleanup
                    |
                    v accepted Version / runtime request
existing runtime-effect owners
  Workspace, OverlayFS, mount, namespace, exec, manager/daemon lifecycle

observability -> diagnostic reader only
```

Application owners decide whether and when an operation is authorized. They
capture the expected Head and order requests. LayerStack-0 alone validates
durable admission, creates or revalidates AcceptedBindings, and serializes the
single Head transition. Runtime owners alone create mutable Workspaces and
perform activation effects. Observability consumes emitted facts and never
participates in a correctness decision.

## 6. Conceptual storage family

```text
<LayerStack0Root>/
  versions/<VersionId>/payload/     complete immutable accepted closure
  heads/<selector>                  AcceptedBinding + HeadRevision
  roots/<kind>/<root-id>            typed reachability to AcceptedBinding
  staging/<transaction-id>/         bounded private Candidate work
  control/                          format/generation/recovery roles
```

The spellings are conceptual, not selected disk names. Phase 03 must choose
non-overlapping paths, record encodings, checksums, durability fences,
supported-filesystem requirements, and finite constants without changing this
storage family.

Cross-Version Chunk/CDC storage, a manifest or Merkle object graph, a
parent/layer/depth reconstruction chain, archive extraction as readable truth,
required reflink or filesystem-snapshot correctness, a database, a new service,
a helper process, a storage facade, a second writer, persistent refcount
authority, and tracing object-graph GC are rejected primitives—not hidden Phase
03 options.

## 7. Algorithm file index

The normative documents are clustered by responsibility and execution boundary.
This organization supersedes the original flat-path presentation by explicit
owner direction; it changes no architecture, authority, invariant, or phase
ownership. Each cluster README is a navigation index, not a competing
specification.

The package-generation [prompt](PROMPT.md) and independent-review
[runbook](REVIEW_PROMPT.md) are intentionally linked here for reproducibility.
They are operational/historical aids, not product or algorithm authority.

### Cluster 01 — Identity and admission

| File | Owner | Contract |
|---|---|---|
| [Cluster index](01-identity-and-admission/README.md) | Phases 02–03 | Reading order and identity/admission invariants. |
| [Canonical Version identity](01-identity-and-admission/01-canonical-version-identity.md) | Phase 02 | Bounded portable facts, deterministic canonical bytes, typed Candidate identity, and full-byte equality. |
| [Complete Version admission](01-identity-and-admission/02-complete-version-admission.md) | Phase 03, consuming Phase 02 | Bounded staging, complete payload installation, occupied-ID comparison, AcceptedVersion, and AcceptedBinding. |
| [Complete-Version content addressing](01-identity-and-admission/03-complete-version-content-addressing.md) | Phases 02–03 | Complete-value address convergence and collision handling; explicitly not a cross-Version CAS object store. |
| [CDC non-selection and reopening gate](01-identity-and-admission/04-cdc-non-selection-and-reopen-gate.md) | Phase 01; evidence from Phase 06 | `CDC_ALGORITHM: NOT_SELECTED_IN_R0`; exact evidence required before architecture reopening. |

### Cluster 02 — References and publication

| File | Owner | Contract |
|---|---|---|
| [Cluster index](02-references-and-publication/README.md) | Phases 03–04 | Reading order and reference/publication invariants. |
| [Reference EphCoW](02-references-and-publication/01-reference-ephcow.md) | Phase 03 | Exact Head create/replace/remove and fixed-Root create/remove through one authority, with payload I/O `0/0/0`. |
| [OCC publication](02-references-and-publication/02-occ-publication.md) | Phase 03, consumed by Phase 04 | Application ordering, admission-before-publication, and one conditional Head replacement. |
| [Composed publication pipeline](02-references-and-publication/03-composed-publication-pipeline.md) | Phases 02–04 and existing runtime owners | Candidate capture through admission to the sole Head transition, with distinct costs and points. |
| [Zero-payload reference demonstration](02-references-and-publication/04-zero-payload-reference-demonstration.md) | Phase 03, qualified by Phase 06 | Structural negative-capability proof plus executable `0/0/0/0` case matrix. |

### Cluster 03 — Runtime access and materialization

| File | Owner | Contract |
|---|---|---|
| [Cluster index](03-runtime-access-and-materialization/README.md) | Phase 03 and existing runtime owners | Reading order and immutable/runtime-private boundary. |
| [Read custody and runtime handoff](03-runtime-access-and-materialization/01-read-custody-and-runtime-handoff.md) | Phase 03 | Stable read capture, bounded custody, immutable access, and runtime-effect handoff. |
| [Runtime activation and materialization](03-runtime-access-and-materialization/02-runtime-materialization.md) | Phase 03 and existing runtime owners | Protected immutable activation and bounded streaming construction of a runtime-private writable destination. |

### Cluster 04 — Durability and lifecycle

| File | Owner | Contract |
|---|---|---|
| [Cluster index](04-durability-and-lifecycle/README.md) | Phase 03 | Reading order and crash/lifecycle invariants. |
| [Durability and recovery](04-durability-and-lifecycle/01-durability-and-recovery.md) | Phase 03 | Payload-before-reference durability, crash-prefix classification, fail-closed recovery, and quarantine. |
| [Retirement and cleanup](04-durability-and-lifecycle/02-retirement-and-cleanup.md) | Phase 03 | Exact reachability plus custody, serialized retirement, staging/orphan cleanup, and bounded debt. |

### Cluster 05 — Migration

| File | Owner | Contract |
|---|---|---|
| [Cluster index](05-migration/README.md) | Phase 05 | Reading order and one-writable-truth migration invariant. |
| [One-way migration](05-migration/01-one-way-migration.md) | Phase 05, constrained by Phase 03 | Fenced legacy translation, ordinary admission, one writable truth, cutover, rollback boundary, and deletion. |

### Cluster 06 — Resources, performance, and evidence

| File | Owner | Contract |
|---|---|---|
| [Cluster index](06-resources-performance-and-evidence/README.md) | Phases 02–06 | Reading order, finite-resource rules, and evidence discipline. |
| [Resources, complexity, and observability](06-resources-performance-and-evidence/01-resources-complexity-and-observability.md) | Phases 02–03; qualified in Phase 06 | Shared variables, worst-case costs, resource budgets, zero-I/O proof counters, and diagnostic-only observability. |
| [Performance demonstration matrix](06-resources-performance-and-evidence/02-performance-demonstration-matrix.md) | Phase 06, consuming all algorithms | Sealed workloads, speed/time/memory/I/O metrics, correctness gates, and evidence states; currently final verdict `TARGET_UNSELECTED`, with historical Stage 4.6 `INCOMPARABLE`. |

## 8. End-to-end composition

```text
application authorizes and captures Expected(HeadRevision, AcceptedBinding)
       |
       +--> runtime-owned isolated Workspace performs mutable work
       |
       +--> capture complete portable Candidate facts
                    |
                    v
          validate + canonicalize (Phase 02 constraints)
                    |
                    v
           typed VersionId (Candidate only)
                    |
                    v
       LayerStack-0 private bounded staging
          | build complete payload closure
          | compare all canonical bytes if VersionId occupied
          | make payload durable and immutable
                    |
                    v
              AcceptedVersion
                    |
                    v
        issue/revalidate AcceptedBinding
                    |
                    v
       acquire sole LayerStack-0 transition gate
          | revalidate Expected tuple and candidate binding
          | conditionally replace one complete Head record
                    |
         +----------+-----------+
         |                      |
       stale                 success
   no merge/rebase      one OCC linearization
         |                      |
         v                      v
 bounded orphan cleanup   new HeadRevision + binding
                                |
                 +--------------+--------------+
                 |                             |
       exact reference operation         capture read custody
          payload I/O 0/0/0                     |
                                               v
                                immutable access -> existing runtime owners
                                      |                     |
                                      v                     v
                           protected activation    private materialization
                           demand reads charged    reads/writes/copies charged
                                      |                     |
                                      +----------+----------+
                                                 v
                                     isolated writable Workspace
                                     (never accepted Version truth)
```

Admission makes an AcceptedVersion durable but does not select it. The only
Head OCC linearization point is the conditional replacement of one complete
Head record while the sole transition gate is held. Reference creation has its
own complete-record visibility point but does not add another Head
linearization point.

## 9. Hard-rule crosswalk

| Product hard rule | Mechanism | Primary specification |
|---|---|---|
| Complete immutable truth; no reconstruction chain | Admission installs one complete filesystem-native payload closure and accepted payloads are never edited. | [Admission](01-identity-and-admission/02-complete-version-admission.md), [runtime boundary](03-runtime-access-and-materialization/01-read-custody-and-runtime-handoff.md) |
| Equal canonical bytes share one physical payload | The occupied slot is reserved; full canonical-byte equality converges on the existing closure. | [Identity](01-identity-and-admission/01-canonical-version-identity.md), [content-address convergence](01-identity-and-admission/03-complete-version-content-addressing.md) |
| Reference operations perform payload I/O `0/0/0` | Reference algorithms receive metadata capabilities only; payload handles and namespaces are absent from their call graph; qualification requires zero opens too. | [EphCoW](02-references-and-publication/01-reference-ephcow.md), [zero-payload demonstration](02-references-and-publication/04-zero-payload-reference-demonstration.md) |
| Digest identity is not equality or existence | `VersionId` names a Candidate; occupancy invokes full canonical comparison and only admission yields accepted evidence. | [Identity](01-identity-and-admission/01-canonical-version-identity.md), [admission](01-identity-and-admission/02-complete-version-admission.md) |
| One OCC point; stale loses cleanly | One complete Head-record conditional replacement under one transition authority; no implicit retry, merge, or rebase. | [OCC](02-references-and-publication/02-occ-publication.md), [composed publication](02-references-and-publication/03-composed-publication-pipeline.md) |
| Accepted payload immutability | Runtime receives immutable access under custody; mutable upper/work data belongs to isolated Workspace owners. | [Read custody](03-runtime-access-and-materialization/01-read-custody-and-runtime-handoff.md), [materialization](03-runtime-access-and-materialization/02-runtime-materialization.md) |
| MCTS/rollout policy outside storage | Application authorizes/orders requests and supplies the expected Head; LayerStack-0 knows no score or rollout policy. | [OCC](02-references-and-publication/02-occ-publication.md) |
| Runtime-private facts excluded from identity | Canonical input contains qualified portable filesystem facts only. | [Identity](01-identity-and-admission/01-canonical-version-identity.md), [migration](05-migration/01-one-way-migration.md) |
| One writable migration truth; deletable compatibility | Generation fencing enables exactly one writer and cutover makes legacy writable rollback impossible. | [Migration](05-migration/01-one-way-migration.md) |
| Speed/time/memory claims require evidence | Complexity terms, measurement scopes, correctness gates, and sealed qualification states prevent unsupported performance claims. | [Resource model](06-resources-performance-and-evidence/01-resources-complexity-and-observability.md), [demonstration matrix](06-resources-performance-and-evidence/02-performance-demonstration-matrix.md) |
| Prefer R0 and existing boundaries | All algorithms are direct in-process responsibilities of the existing LayerStack-0, application, and runtime-effect owners. | This package and the selected [architecture](../architecture_design.md) |

## 10. Cross-file invariants

All files use and preserve these invariants:

1. One complete immutable Version is truth; no layer reconstruction is needed
   to read it.
2. Equal canonical bytes under one occupied `VersionId` map to one physical
   payload closure.
3. Occupancy equality uses full canonical-byte comparison; a mismatch is a
   collision error even if digest and length match.
4. Only LayerStack-0 admission creates or revalidates an AcceptedBinding.
5. Heads and typed Roots contain AcceptedBindings, never unchecked raw IDs.
6. `CreateHeadIfAbsent`, `ReplaceHead`, `RemoveHead`,
   `CreateFixedRootIfAbsent`, and `RemoveFixedRoot` report accepted-reference
   payload bytes read/written/copied `0/0/0`; Branch is a Head, Checkpoint is a
   fixed Root, and no generic Root retarget operation exists.
7. Head publication has one OCC linearization point; stale loses without a
   silent merge, rebase, or retry against a newly observed Head.
8. Live Workspace writes cannot modify an accepted payload.
9. Authorization, request ordering, rollout/MCTS policy, and scores remain
   outside LayerStack-0.
10. Portable identity excludes all runtime-private platform, mount, process,
    session, and host facts.
11. Migration has at most one writable selected-Version truth, and its
    compatibility code is temporary and deletable.
12. Staging, memory, descriptors, workers, recovery, custody, and cleanup debt
    are finite, backpressured, and fail closed.

### Composition proof

- [Identity](01-identity-and-admission/01-canonical-version-identity.md)
  produces only a bounded Candidate identity plus exact canonical comparison
  material; it cannot confer durable authority.
- [Admission](01-identity-and-admission/02-complete-version-admission.md)
  consumes that material and is the only producer of an AcceptedVersion and
  AcceptedBinding. The focused
  [content-addressing proof](01-identity-and-admission/03-complete-version-content-addressing.md)
  shows full-byte equal convergence without a cross-Version object authority;
  [CDC remains non-selected](01-identity-and-admission/04-cdc-non-selection-and-reopen-gate.md).
- [Reference operations](02-references-and-publication/01-reference-ephcow.md),
  [OCC publication](02-references-and-publication/02-occ-publication.md), and
  [read capture](03-runtime-access-and-materialization/01-read-custody-and-runtime-handoff.md)
  accept only bindings that LayerStack-0 admission issued or its
  admission-owned verifier revalidated.
- [Composed publication](02-references-and-publication/03-composed-publication-pipeline.md)
  keeps Candidate/admission byte costs separate from the one constant-record
  Head transition, and the
  [zero-payload demonstration](02-references-and-publication/04-zero-payload-reference-demonstration.md)
  requires structural exclusion plus measured `0/0/0/0` on every outcome.
- [Runtime materialization](03-runtime-access-and-materialization/02-runtime-materialization.md)
  may move complete payload bytes only under runtime-owned scopes and can never
  mutate or replace accepted Version truth.
- [Durability](04-durability-and-lifecycle/01-durability-and-recovery.md)
  ensures payload acceptance precedes reference visibility;
  [retirement](04-durability-and-lifecycle/02-retirement-and-cleanup.md) removes
  a closure only after Heads, Roots, and custody are exactly revalidated under
  the same transition authority.
- [Migration](05-migration/01-one-way-migration.md) cannot bypass these paths;
  translated legacy facts enter as ordinary Candidates.
- [Resource accounting](06-resources-performance-and-evidence/01-resources-complexity-and-observability.md)
  supplies shared finite bounds, while the
  [performance matrix](06-resources-performance-and-evidence/02-performance-demonstration-matrix.md)
  defines the evidence required before speed/time/memory claims. Neither
  acquires authority.

## 11. Open phase-owned choices

The following are `OPEN_WITHIN_R0`, not architecture gaps.

### Phase 02 — Version identity

- Exact portable fact schema and rejection profile.
- Exact canonical codec/grammar, ordering, format version, and domain/schema
  separation bytes.
- Exact digest algorithm, width, serialized form, and typed `VersionId`
  representation.
- Exact finite limits for bytes, entries, paths, depth, metadata, links, and
  comparison scratch.
- Streaming interfaces, golden/corrupt vectors, independent-style checks, and
  forced-collision test mechanics.

Phase 02 may not turn a computed ID into equality, existence, admission, or
reference authority, and it may not admit runtime-private facts.

### Phase 03 — LayerStack-0 durability

- Exact non-overlapping V2 root and path spellings.
- Exact record formats, schema versions, checksums, generations, temporary
  names, and staging-state encodings.
- Exact supported local-filesystem profile and qualified durability-fence
  sequence.
- Exact transition-lock primitive and internal admission concurrency.
- Exact read-custody and last-root/read-race implementation.
- Exact finite limits, cleanup/recovery batch sizes, and metric spellings.
- Whether an expected same-Version publication advances `HeadRevision` or is a
  defined no-op, provided the result is monotone, replayable, and zero-payload.

Phase 03 may refine mechanics but not the storage family, ownership, single
writer, single Head OCC point, payload-before-reference order, or fail-closed
guarantees.

### Later phases

Phase 04 selects application/API integration details without moving policy into
LayerStack-0. Phase 05 selects importer progress and cutover record spellings
within the one-writable-truth protocol. Phases 06–08 qualify, cut over, observe,
and delete compatibility code without changing the accepted architecture.

## 12. Product-owner decisions

All remain `OWNER_DEC_OPEN`; this package accepts none on the owner's behalf.

| Decision | Stable seam | Architecture-changing reopening trigger |
|---|---|---|
| `DEC-001` — exact `file_blame` fidelity or accepted break | Application-owned audit/provenance side channel may key facts by accepted Version, revision, or publication; it is not canonical Version truth. | Provenance/history must become portable Version identity or selected-Version authority. |
| `DEC-011` — observation-window duration | Changes only how long temporary compatibility/import code remains after cutover. | Requires dual writable truth or a permanent legacy dependency in the V2 core. |
| `DEC-017` — operation surface, sessionless writes/edits, and `file_list` | Application rejects the operation or creates a bounded Candidate and invokes ordinary admission/publication. | Requires accepted-payload mutation, unchecked reference motion, another writer, or another storage representation. |
| `DEC-018` — authorization/revoke race ordering | Application owns the authorization cutoff and disclosure; LayerStack-0 OCC remains mandatory and independent. | Requires a joint durable authorization/storage authority, a second writer, or a second Head linearization point. |

## 13. Package outcome and reopening conditions

No reopening condition is currently triggered. Return
`REOPEN_PHASE_01 — <specific architecture-changing failure>` if later evidence
proves any of the following:

- `sandbox-runtime-layerstack` or the selected dependency direction is not
  source-placeable on the required base.
- A bounded, complete, deterministic portable Version cannot be identified
  without runtime-private facts.
- Complete filesystem-native immutable payloads cannot satisfy a product hard
  rule.
- No supported local filesystem can provide prior-or-complete-new reference
  durability under a qualified fence.
- One LayerStack-0 transition authority and one conditional Head replacement
  cannot close stale-writer behavior.
- Occupied-ID full canonical-byte comparison cannot be made finite and fail
  closed.
- Bounded read custody plus final serialized reachability revalidation cannot
  close the last-root/read race.
- Migration cannot maintain exactly one writable truth or its compatibility
  code cannot be deleted.
- A proved multi-host, privilege, process-isolation, scaling, or failure-domain
  requirement necessitates a new architectural boundary.
- An owner decision exceeds its stable seam, source drift invalidates the e497
  placement evidence, or product semantics require a non-content-derived or
  second independent complete-value identity.

Exact codec bytes, digest selection, filenames, record syntax, checksums,
filesystem qualification, syscall fences, numeric bounds, custody
representation, batching, and diagnostic names remain phase-owned. They do not
reopen Phase 01 unless their proof fails in an architecture-changing way.
