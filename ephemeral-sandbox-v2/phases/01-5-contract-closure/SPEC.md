# Phase 01.5 specification — close architecture contracts before Phase 02

**Status:** passed; documentation-only contract closure complete  
**Date:** 2026-08-04  
**Finding reference:** `019fcd32-b832-7750-9eb5-5f544e39c533`  
**Execution prompt:** [PROMPT.md](PROMPT.md)  
**Consumes:** completed Phase 00 evidence, selected Phase 01 R0 architecture,
and the Phase 02 alignment review  
**Produces:** corrected normative documents and a bounded `GO` or `HOLD` for
formal Phase 02 entry

```text
PHASE_01_5_SPEC: EXECUTED
PHASE_01_5_RESULT: PASS
PHASE_02_FORMAL_ENTRY: GO
REOPEN_PHASE_01: NO
```

---

## 1. Document role

This `SPEC.md` is the input contract for a short, documentation-only
architecture-closure gate between Phase 01 and Phase 02.

Phase 01 selected the R0 LayerStack-0 complete-Version owner and authorized
Phase 02. Finding `019fcd32-b832-7750-9eb5-5f544e39c533` subsequently showed
that the selected architecture remains sound, but several downstream
algorithm, API, diagram, evidence, and navigation contracts are incomplete or
contradictory.

Phase 01.5 closes those contracts without selecting a new architecture. It
must not become a second design tournament, an implementation phase, a backend
selection exercise, or a benchmark qualification exercise.

Identity fixture preparation and read-only Phase 02 research may proceed in
parallel. Formal Phase 02 product-code entry remains on hold until this gate
passes so later work consumes one internally consistent authority set.

## 2. Goal and result contract

Phase 01.5 must make the selected R0 architecture directly consumable by
Phase 02 and later phases by closing six review findings:

1. complete the abstract Head and Root lifecycle contract;
2. resolve Branch-versus-Root workflow ambiguity;
3. make candidate admission-before-reference publication ordering universal;
4. seal the exact architectural input delegated to Phase 02 identity work;
5. normalize evidence and performance vocabulary; and
6. repair broken authority links and navigation.

The execution result must start with exactly one of:

```text
PHASE_01_5: PASS
FINDING_REFERENCE: 019fcd32-b832-7750-9eb5-5f544e39c533
PHASE_02: GO
REOPEN_PHASE_01: NO
```

or:

```text
PHASE_01_5: CHANGES_REQUIRED — <bounded unresolved contract defect>
FINDING_REFERENCE: 019fcd32-b832-7750-9eb5-5f544e39c533
PHASE_02: HOLD
REOPEN_PHASE_01: NO
```

or, only when section 18 is proved:

```text
PHASE_01_5: REOPEN_PHASE_01 — <proved hard-rule incompatibility>
FINDING_REFERENCE: 019fcd32-b832-7750-9eb5-5f544e39c533
PHASE_02: STOP
```

Repeated wording, a missing implementation, or open backend evidence does not
by itself justify `REOPEN_PHASE_01`.

## 3. Authority and interpretation

Use sources in descending authority:

1. product [PRD](../../PRD.md), especially its hard rules and exclusions;
2. completed Phase 00 [SPEC](../00-freeze-rules/SPEC.md) and sealed evidence;
3. completed Phase 01 [SPEC](../01-choose-design/SPEC.md) and selected root
   [architecture](../../architecture_design.md);
4. this Phase 01.5 specification;
5. selected [design documents](../../design/README.md) and accepted ADRs;
6. selected [algorithm contracts](../../algorithm/README.md);
7. public [API contracts](../../api/README.md);
8. selected [diagrams](../../diagrams/README.md);
9. phase PRDs, plans, and test/performance documents; and
10. quarantined proposals and the historical appendix as evidence only.

When lower-authority text conflicts with a higher-authority hard rule, repair
the lower-authority text. Do not weaken the hard rule to preserve an existing
diagram or API sketch.

Finding `019fcd32-b832-7750-9eb5-5f544e39c533` is the review trace for this
closure work. It is not a new product authority and does not supersede the
source order above.

## 4. Evidence-base precondition

The sealed product evidence base remains:

```text
Path:   /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
Branch: codex/new-2.0-storage-core
HEAD:   e4974d1f9aac702b35e052629cb070c897989352
```

Before executing Phase 01.5, record:

```bash
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git status --short --branch
```

If the sealed product tree is missing, dirty, on a different branch, or at a
different commit, report the drift. Do not reset, clean, switch, or edit the
product tree to manufacture the expected evidence.

The documentation repository may contain unrelated pre-existing changes.
Preserve them. Only touch files required by the Phase 01.5 correction manifest
in section 16.

## 5. Finding trace

All correction work must remain traceable to
`019fcd32-b832-7750-9eb5-5f544e39c533`.

| ID | Finding | Severity | Required closure |
|---|---|---:|---|
| F-01 | State-store design and manager APIs require Root lifecycle operations not defined by the reference algorithm. | P1 | Define fixed-Root creation/removal and explicitly dispose of generic Root retargeting. |
| F-02 | Manager creation and migration require initial Head creation; manager destruction also requires Head removal, while OCC specifies replacement of an existing Head only. | P1 | Define Head create/replace/remove under the sole reference transition authority. |
| F-03 | The Phase 03 PRD diagram places Head OCC before durable candidate admission/reference truth. | P1 | Make payload admission-before-reference publication ordering universal. |
| F-04 | Branch movement is shown once as mutable Fork Root retargeting and elsewhere as Head movement. | P1 consequence | Select one semantic model and repair all workflows. |
| F-05 | Evidence, source-seal, decision-state, correctness, and performance-verdict terms are mixed. | P2 | Use the evidence and verdict taxonomies in section 14. |
| F-06 | Five API-to-algorithm Markdown links use obsolete paths. | P2 | Repair all five and validate the full local link graph. |
| F-07 | “Zero-copy” wording is broader than the selected zero-payload reference contract. | P3 | Use scoped payload byte classes and name nonzero control/fence I/O. |
| F-08 | Three prompt/runbook documents have no incoming navigation edge. | P3 | Link them or explicitly mark them intentionally standalone. |

Phase 01.5 passes only when F-01 through F-08 are resolved or, for a genuinely
non-normative P3 artifact, explicitly dispositioned with no semantic ambiguity.

## 6. Non-goals

Phase 01.5 shall not:

- change the selected LayerStack-0 complete-Version owner;
- replace complete immutable Version truth with layer, archive, chunk, Merkle,
  object-DAG, database-row, runtime-image, or VM-disk truth;
- introduce a second accepted-state or reference writer;
- introduce a second Head OCC point;
- choose the exact canonical codec, digest, or validation limits;
- choose a final filesystem layout, lock, journal, or fence primitive;
- choose a Firecracker disk format, kernel, snapshot format, adapter API, or
  materialization strategy;
- choose a WASM runtime, component adapter, preopen topology, or
  materialization strategy;
- generalize the current Docker API into a speculative universal backend API;
- select an optimization threshold, factor, percentile, or workload corpus;
- qualify a benchmark or compare V2 with Stage 4.6;
- implement V2 product code;
- execute migration, cutover, retirement, or legacy deletion; or
- settle `DEC-001`, `DEC-011`, `DEC-017`, or `DEC-018`.

## 7. Hard rules preserved by this closure

### 7.1 Accepted Version truth

A Version is one complete immutable portable filesystem value accepted by the
selected LayerStack-0 owner. It is not a Head, Root, runtime mount, OCI bundle,
VM disk, WASM preopen, session, migration record, or materialized workspace.

### 7.2 Portable identity

Portable Version identity excludes runtime-private configuration, including
container, VM, WASM runtime, mount, OverlayFS, namespace, host-path, process,
lease, cache, and materialization facts.

### 7.3 Exact occupied-ID truth

A matching `VersionId` is not proof of equal content. Occupied admission must
compare complete canonical content within enforceable bounds. Mismatch fails
closed and cannot modify accepted truth or a reference.

### 7.4 Immutable acceptance

An accepted Version is never edited in place. An edit creates a candidate; a
successful admission creates or reuses an immutable accepted Version; a
separate reference transition publishes it.

### 7.5 Reference authority

Heads and Roots are reference-plane records naming complete
`AcceptedBinding`s. LayerStack-0's selected reference transition authority is
their only writer. Manager, runtime, migration, recovery, and cleanup callers
must use that authority rather than writing records directly.

### 7.6 Sole Head OCC point

Every Head create, replacement, and removal uses one transition authority and
one linearization boundary. Initialization and teardown are not exceptions.

### 7.7 Zero-payload reference operations

Creating, moving, or removing an accepted reference performs:

```text
accepted payload bytes read:    0
accepted payload bytes written: 0
accepted payload bytes copied:  0
```

Reference metadata, locks, journals, directory operations, and durability
fences are nonzero work and must be reported separately.

### 7.8 Runtime-effect boundary

Runtime consumption begins after an authoritative reference capture resolves
to an accepted binding and obtains custody or equivalent retirement
protection. Runtime adapters consume truth; they do not define identity,
accept Versions, or publish references.

### 7.9 Safe retirement

An accepted Version cannot be reclaimed while reachable through a Head, Root,
active custody, or an unresolved recovery/migration state that may have
committed.

### 7.10 One-writer migration

Migration is a temporary consumer of permanent admission/reference APIs. It
never becomes another accepted-state or reference authority and never creates
a permanent dual-write period.

## 8. Selected Branch, Head, Checkpoint, and Root semantics

Phase 01.5 closes the ambiguous reference vocabulary as follows:

| Product concept | Selected reference record | Mutability |
|---|---|---|
| Branch | Head | Mutable only through Head OCC |
| Current branch selection | Head binding plus Head revision/incarnation | Conditional replace |
| Checkpoint | Fixed typed Root | Binding does not retarget after creation |
| Other durable pin | Fixed typed Root unless a higher-authority requirement explicitly defines another kind | Create/remove only by default |

Therefore:

- branch movement, rollback, and publication are Head transitions;
- checkpoint creation is fixed-Root creation;
- checkpoint removal is conditional fixed-Root removal;
- a “Fork Root retarget” is not part of the selected contract and must be
  relabeled as a Head transition or removed; and
- generic Root update shall not remain as an implied operation.

If a future sealed requirement needs a mutable `RootKind`, it may remain within
R0 only when its complete conditional-update contract uses the same reference
transition authority, introduces no second Head point, performs no accepted
payload I/O, and preserves the same durability, retry, recovery, custody, and
retirement rules. Do not infer such a kind during Phase 01.5.

## 9. Semantic records and outcomes

The definitions in this section are semantic contracts, not selected Rust or
wire schemas.

### 9.1 `VersionId`

A typed content-derived identifier produced by the Phase 02 canonical identity
function. It does not prove equality, acceptance, durability, or reachability.

### 9.2 `AcceptedBinding`

The complete LayerStack-0-issued binding required to locate and validate an
accepted Version under the selected owner. A raw `VersionId` is not an
`AcceptedBinding`.

### 9.3 `HeadRecord`

Contains the logical Head identity, complete `AcceptedBinding`, and the
revision/incarnation information required for exact conditional transitions.

### 9.4 `RootRecord`

Contains the logical Root identity, fixed Root kind, complete
`AcceptedBinding`, and any record identity/revision needed for safe
conditional removal.

### 9.5 Expected state

Reference operations compare one of:

```text
Expected::Absent
Expected::Exact(complete current record)
```

An API may encode this differently, but it must not weaken absent/exact
semantics or compare only a raw `VersionId`.

### 9.6 Required semantic outcomes

Reference APIs preserve at least these distinctions:

```text
APPLIED
ALREADY_EXISTS
NOT_FOUND
CONFLICT
INVALID_BINDING
CORRUPT
OUTCOME_UNKNOWN
INTERNAL_FAILURE
```

Exact public transport mappings remain `OPEN_WITHIN_R0` under `WIRE-001`.

`OUTCOME_UNKNOWN` is neither success nor failure. The caller must perform
authoritative read-back. A matching current value alone does not prove that a
particular retried request authored that value unless an owner-selected
idempotency mechanism establishes it.

## 10. Complete reference lifecycle contract

All operations below use the same selected reference transition authority.
The exact lock, CAS, transaction, journal, directory primitive, or fence
sequence remains Phase 03-owned.

### 10.1 Common preconditions

Before storing a new binding, the authority must verify that:

1. the complete binding is structurally valid;
2. it names accepted Version truth under the selected owner;
3. the Version is not staging-only, corrupt, or already retired;
4. required admission durability has completed; and
5. the expected reference state is complete and unambiguous.

### 10.2 Create Head if absent

```text
CreateHeadIfAbsent(head_identity, Expected::Absent, new_binding)
```

Required semantics:

1. validate `new_binding` before publication;
2. enter the sole reference transition authority;
3. read the complete current Head state;
4. return `ALREADY_EXISTS` or `CONFLICT` when present;
5. atomically create the complete Head record when absent;
6. establish its initial revision/incarnation under the Phase 03 policy;
7. durably fence the reference result before returning `APPLIED`; and
8. return `OUTCOME_UNKNOWN` when the durable result cannot be determined.

Manager creation and migration initialization must call this operation. They
must not write initial Head storage through a separate path.

### 10.3 Conditional Head replacement

```text
ReplaceHead(Expected::Exact(expected_head), new_binding)
```

Required semantics:

1. the candidate Version is already accepted and durably admissible;
2. validate `new_binding`;
3. enter the sole reference transition authority;
4. compare the complete current Head with `expected_head`;
5. return `CONFLICT` without a Head write when they differ;
6. atomically replace the complete binding and advance revision/incarnation
   when they match;
7. durably fence the result before returning `APPLIED`; and
8. return `OUTCOME_UNKNOWN` when the durable result cannot be determined.

No content merge, silent rebase, or candidate mutation occurs.

### 10.4 Conditional Head removal

```text
RemoveHead(Expected::Exact(expected_head))
```

Required semantics:

1. enter the same transition authority;
2. return `NOT_FOUND` when the Head is absent;
3. return `CONFLICT` when the complete current Head differs;
4. remove or tombstone the expected Head through the selected durable method;
5. fence the result before returning `APPLIED`;
6. invoke or schedule retirement evaluation after the transition; and
7. return `OUTCOME_UNKNOWN` when the durable result cannot be determined.

Removing a Head does not prove that its formerly referenced Version is
reclaimable. Manager destruction and migration cleanup must use this operation.

### 10.5 Create fixed Root if absent

```text
CreateRootIfAbsent(root_identity, root_kind, Expected::Absent, binding)
```

Required semantics:

1. validate the accepted binding;
2. enter the reference transition authority;
3. return `ALREADY_EXISTS` or `CONFLICT` when a Root already exists;
4. atomically create the complete fixed Root when absent;
5. fence the result before returning `APPLIED`;
6. return `OUTCOME_UNKNOWN` when the durable result cannot be determined; and
7. preserve accepted-payload `0/0/0` accounting.

Checkpoint and durable-pin creation use this operation.

### 10.6 Conditional fixed Root removal

```text
RemoveRoot(Expected::Exact(expected_root))
```

Required semantics:

1. enter the same transition authority;
2. return `NOT_FOUND` when absent;
3. return `CONFLICT` when the complete Root differs;
4. remove or tombstone the expected Root through the selected durable method;
5. fence the result before returning `APPLIED`;
6. invoke or schedule retirement evaluation after the transition;
7. return `OUTCOME_UNKNOWN` when the durable result cannot be determined; and
8. preserve accepted-payload `0/0/0` accounting.

Checkpoint removal and manager destruction use this operation. Direct Root
file deletion is forbidden.

## 11. Publication ordering contract

Every normative publication workflow must use this order:

```text
portable candidate facts
  -> canonicalize and derive VersionId
  -> stage candidate privately
  -> validate new or occupied admission
  -> exact canonical compare when VersionId is occupied
  -> make complete Version accepted and durable
  -> produce complete AcceptedBinding
  -> enter reference transition authority
  -> compare expected complete Head
  -> perform one Head replacement
  -> fence reference result
  -> acknowledge publication
```

Candidate admission remains outside the Head transition gate.

On stale OCC:

- return `CONFLICT`;
- do not change the Head;
- do not read, write, or copy accepted payload for the reference operation;
- do not mutate or roll back the accepted candidate;
- account for the candidate as a possible accepted orphan; and
- leave later reclamation to ordinary safe-retirement policy.

No diagram may show the Head naming an unaccepted or not-yet-durable candidate.

## 12. Recovery, custody, and retirement integration

Reference lifecycle operations must connect to the selected recovery and
retirement model:

- success is acknowledged only after the selected durability boundary;
- ambiguous failures return `OUTCOME_UNKNOWN` and require authoritative
  read-back;
- recovery fails closed on corrupt, partial, or dangling records;
- a captured read obtains custody before runtime handoff;
- Root or Head removal never synchronously assumes last reachability;
- retirement checks all Heads, Roots, custody, and unresolved recovery or
  migration state;
- cleanup reports staging, accepted orphan, recovery, and deletion debt; and
- exact batching, lock, journal, fence, and tombstone choices remain
  `OPEN_WITHIN_R0` for Phase 03.

## 13. Phase 02 entry contract

After Phase 01.5 passes, Phase 02 receives these frozen inputs:

```text
one complete immutable portable Version is accepted truth
runtime-private facts are outside Version identity
VersionId is not equality proof or acceptance authority
occupied VersionId requires exact canonical comparison
raw VersionId cannot construct AcceptedVersion or AcceptedBinding
Heads and fixed Roots name complete AcceptedBindings
Branch movement uses Head OCC
checkpoint creation/removal uses fixed Roots
candidate admission completes before reference publication
runtime adapters consume accepted bindings after custody
```

Phase 02 owns these bounded choices:

| ID | Phase 02 decision | Required output |
|---|---|---|
| `ID-001` | Canonical schema and codec | Normative grammar, ordering, normalization, malformed-input behavior, versioning/domain separation, and golden vectors |
| `ID-002` | Digest and typed identifier encoding | Algorithm/encoding plus occupied-ID exact-comparison seam and forced-ID test capability |
| `ID-003` | Enforceable limits | Byte, entry, path/name, depth, memory/batch, and adversarial-input rejection limits |

Phase 02 must produce deterministic canonical vectors, corrupt/over-limit
rejects, forced-collision inequality evidence, bounded resource tests, and a
proof that identity APIs cannot assert durable acceptance.

Phase 02 must stop if implementation requires runtime-private identity,
layer-history reconstruction, mutable accepted truth, a raw-ID reference, a
second owner, or another writer/OCC point.

## 14. Evidence and performance discipline

Use only these evidence labels:

```text
SOURCE-VERIFIED
SPIKE-VERIFIED
BENCHMARK-QUALIFIED
INFERRED
OPEN
OPEN_WITHIN_R0
OWNER_DEC_OPEN
INCOMPARABLE
```

Keep source metadata separate:

```text
evidence: SOURCE-VERIFIED
source commit: e4974d1f9aac702b35e052629cb070c897989352
source state: CLEAN
```

Use these final performance verdicts only:

```text
QUALIFIED
DESIGN_ONLY
TARGET_UNSELECTED
INCOMPARABLE
FAILED_TARGET
```

Rules:

- `BENCHMARK-QUALIFIED` is an evidence label; `QUALIFIED` is a final verdict.
- A correctness failure invalidates qualification.
- `FAILED_TARGET` requires matched semantics, passing correctness gates, a
  complete closure, and an owner-approved target that was missed.
- `DESIGN_ONLY`, `TARGET_UNSELECTED`, and `INCOMPARABLE` are not performance
  wins.
- Stage 4.6 remains `INCOMPARABLE`.
- Phase 02 encode/hash microbenchmarks are diagnostic only unless a later
  owner-approved target and matched closure qualify them.

At Phase 01.5 entry and exit:

```text
OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED
performance readiness: TARGET_UNSELECTED
Stage 4.6: INCOMPARABLE
```

The product owner must later select the metric, matched operation scope,
workload/data shape, concurrency, backend, filesystem, durability, cache
state, statistic/percentile, numerical threshold or improvement factor,
resource ceilings, and correctness gates. Phase 01.5 does not invent them.

## 15. Backend conformance boundary

OCI/Docker is current evidence only, not universal proof.

Firecracker and WASI/WASM may remain at backend-conformance status
`OPEN_EVIDENCE`, with the missing implementation evidence labelled `OPEN`,
when:

- portable identity contains no runtime-specific fields;
- Accepted Version truth remains owned by LayerStack-0;
- direct accepted-binding/custody handoff remains the runtime input;
- the adapter cannot author Heads or Roots;
- Head OCC remains backend-neutral; and
- materialization work is measured separately from reference movement.

Phase 01.5 shall not select an exact future VM disk, WASM runtime, adapter API,
or materialization strategy. Those choices remain below the runtime-effect
boundary and within the later owning phase unless evidence proves a section 18
reopening condition.

## 16. Required correction manifest

Phase 01.5 execution is authorized to make only the following semantic and
navigation corrections.

| Target | Required correction |
|---|---|
| [design/03-state-store.md](../../design/03-state-store.md) | Replace ambiguous generic Root create/update/remove wording with Head create/replace/remove and fixed-Root create/remove, or explicitly specify any higher-authority mutable Root kind. |
| [reference EphCoW algorithm](../../algorithm/02-references-and-publication/01-reference-ephcow.md) | Add fixed-Root removal, complete outcomes, durability/read-back, retirement integration, and the Branch-as-Head rule. |
| [OCC publication algorithm](../../algorithm/02-references-and-publication/02-occ-publication.md) | Add absent-state Head creation and conditional Head removal under the same authority as replacement. |
| [manager API](../../api/manager.md) | Map initialization, publication/rollback, checkpoint, checkpoint removal, destruction, and migration to the complete lifecycle operations; prohibit direct record writes/deletes. |
| [fork/checkpoint/rollback diagram](../../diagrams/03-fork-checkpoint-rollback-and-cow.md) | Replace mutable Fork Root retargeting with Head movement. |
| [Phase 03 PRD](../03-state-store/PRD.md) | Show durable accepted admission before Head OCC and reference acknowledgement. |
| [performance matrix](../../algorithm/06-resources-performance-and-evidence/02-performance-demonstration-matrix.md) | Separate evidence labels, correctness results, source seal, and final performance verdict. |
| [API index](../../api/README.md) | Normalize evidence labels and repair obsolete algorithm links. |
| [runtime API](../../api/runtime.md) | Repair OCC and custody algorithm links. |
| [terminology authority](../../branding/terminology.md) and root [PRD](../../PRD.md) | Scope “zero-copy” to exact operation/byte classes or use “zero-payload accepted-reference” wording. |
| Prompt/runbook navigation | Link the three intentional prompt/runbook documents from the relevant README or mark them standalone. |
| Root [README](../../README.md), [PLAN](../../PLAN.md), and Phase 02 documents | Record Phase 01.5 as the formal entry gate. |

Do not use the correction manifest to refactor unrelated documents or close
phase-owned and owner-owned decisions.

## 17. Verification and exit checks

### 17.1 Contract coverage

The final lifecycle matrix must have no unexplained cell:

| Record | Create | Move/update | Remove |
|---|---|---|---|
| Head | Defined under sole authority | Conditional OCC replace | Conditional removal under same authority |
| Fixed Root | Defined under reference authority | Not permitted | Conditional removal under same authority |
| Accepted Version | Admission only | Never | Safe retirement/reclamation only |
| Runtime materialization | Backend effect only | Ephemeral backend behavior | Backend cleanup; never accepted-truth mutation |

### 17.2 Required checks

| ID | Check | Must? |
|---|---|:---:|
| C1 | Every manager/runtime lifecycle operation links to one selected algorithm. | yes |
| C2 | Initial Head creation uses the same transition authority as Head replacement. | yes |
| C3 | Head removal and fixed-Root removal define exact expected state, durability, read-back, and retirement behavior. | yes |
| C4 | Branch movement is a Head transition in every normative document and diagram. | yes |
| C5 | Checkpoint Root binding is fixed after creation. | yes |
| C6 | Every publication workflow admits/durably accepts the candidate before Head OCC. | yes |
| C7 | Reference-only operations state accepted-payload `0/0/0` and do not call control/fence I/O zero. | yes |
| C8 | Evidence labels and performance verdicts follow section 14. | yes |
| C9 | Internal Markdown file links resolve; the five known obsolete links are gone. | yes |
| C10 | OCI is current evidence; Firecracker and WASI/WASM remain possible and `OPEN`. | yes |
| C11 | No protected owner decision or phase-owned exact mechanism is selected accidentally. | yes |
| C12 | Phase 02 input, owned decisions, stop conditions, and outputs are explicit. | yes |

### 17.3 Passing result

Phase 01.5 passes only when:

```text
P0 findings: 0
P1 findings: 0
broken internal links: 0
API lifecycle operations without selected algorithm: 0
Branch/Root semantic contradictions: 0
publication-order contradictions: 0
backend-specific portable identity fields: 0
alternative Head/reference authorities: 0
invented performance targets: 0
protected owner decisions settled: 0
```

The final status block must be:

```text
architecture: ALIGNED
algorithm correctness: PASS
diagram/workflow parity: PASS
terminology/naming: PASS
link graph: PASS
backend extensibility: OPEN_EVIDENCE
performance readiness: TARGET_UNSELECTED
product source seal: CLEAN
```

## 18. Exact Phase 01 reopening conditions

Return `REOPEN_PHASE_01` only when reproducible evidence proves that required
semantics cannot be supported by the accepted complete-Version owner and
direct runtime handoff without changing a hard rule, including one of:

1. required portable identity necessarily contains runtime-private state;
2. a required backend necessarily owns accepted truth rather than consuming
   it through accepted-binding handoff;
3. required semantics need a second accepted-state or reference authority;
4. required semantics need a second Head/OCC point or content merge;
5. a required reference-only operation must traverse accepted payload;
6. exact occupied-ID comparison cannot be bounded and fail closed;
7. required accepted truth must be mutable;
8. recovery cannot fail closed while preserving fence-before-success;
9. retirement cannot remain safe with bounded Heads, Roots, custody, and debt;
10. migration requires permanent dual writes; or
11. an owner-approved required resource ceiling cannot be met without changing
    the selected owner, truth model, or writer boundary.

No condition is triggered merely because Firecracker/WASM evidence is absent,
a filesystem mechanism is unselected, a benchmark target is unquantified, an
API mapping is open, or documentation is currently inconsistent.

## 19. Protected open decisions and stable seams

These remain `OWNER_DEC_OPEN`:

| Decision | Stable seam |
|---|---|
| `DEC-001` | File blame/audit remains a side channel keyed by accepted/publication facts, outside Version identity and accepted truth. |
| `DEC-011` | Observation window changes deletion timing only; it cannot authorize dual writes or another reference authority. |
| `DEC-017` | Sessionless edits are rejected or flow through candidate/admission/publication; they never mutate an accepted Version. |
| `DEC-018` | Authorization/revocation policy cannot create another OCC path or backend-owned reference authority. |

These remain `OPEN_WITHIN_R0`:

```text
ID-001 canonical codec/schema
ID-002 digest/identifier encoding
ID-003 enforceable identity limits
STORE-001 physical layout
STORE-002 filesystem/fence policy
STORE-003 lock/transition implementation
STORE-004 custody/retirement implementation
STORE-005 resource ceilings and backpressure
WIRE-001 transport mapping
MIG-001 migration journal/fence mechanics
QUAL-001 benchmark corpus, target, closure, and ship result
```

## 20. Authorized scope

| Allowed | Forbidden |
|---|---|
| Correct selected V2 documents listed in section 16 | Change product code |
| Add narrow semantic algorithms/outcomes needed to close F-01 through F-08 | Select exact Phase 02 codec/hash/limits |
| Repair links and navigation | Select exact Phase 03 filesystem/locking/fence implementation |
| Run read-only link, terminology, and consistency checks | Run migration, cutover, or deletion |
| Record source state and evidence labels | Claim Firecracker/WASM implementation support |
| Recommend an owner target record | Invent a performance target or benchmark win |
| Return a bounded `CHANGES_REQUIRED` result | Reopen Phase 01 without section 18 proof |

Preserve unrelated dirty/untracked documentation. Do not reset, clean, switch,
or broadly rewrite either repository.

## 21. Required reading

Read in this order:

1. root [README](../../README.md), [PRD](../../PRD.md), and
   [PLAN](../../PLAN.md);
2. Phase 00 [SPEC](../00-freeze-rules/SPEC.md);
3. Phase 01 [SPEC](../01-choose-design/SPEC.md) and selected
   [architecture](../../architecture_design.md);
4. this Phase 01.5 `SPEC.md`;
5. [design authority/index](../../design/README.md), especially identity,
   state-store, references/publication, runtime, durability, performance, and
   decisions;
6. [algorithm index](../../algorithm/README.md) and all selected algorithms;
7. [API index](../../api/README.md), manager, runtime, and observability APIs;
8. [diagram index](../../diagrams/README.md), selected diagrams, and the
   storage-diagram quarantine notice;
9. Phase 02 [PRD](../02-state-identity/PRD.md),
   [PLAN](../02-state-identity/PLAN.md), and
   [test/performance gate](../02-state-identity/test-perf.md); and
10. Phase 03 [PRD](../03-state-store/PRD.md),
    [PLAN](../03-state-store/PLAN.md), and
    [test/performance gate](../03-state-store/test-perf.md).

## 22. Handoff to Phase 02

After C1–C12 pass, publish the Phase 01.5 result, update root program status,
and permit Phase 02 to implement only the identity contract in section 13.

Phase 02 shall not rediscover Branch/Root semantics, reference lifecycle,
publication ordering, backend authority, or performance evidence rules. It
shall consume them as fixed inputs and stop if implementation evidence triggers
a section 18 condition.

Until then:

```text
Phase 02 research/test-vector scaffolding: allowed
Phase 02 production implementation: hold
Phase 03 implementation: hold
Phase 01 architecture: remains selected; not reopened
```
