# Agent prompt — implement the Phase 01.5 contract-closure gate

Copy everything below the line into a new lead-agent session.

---

## 1. Mission

Execute the documentation-only Phase 01.5 contract-closure gate for Ephemeral
Sandbox V2.

The normative input is [SPEC.md](SPEC.md):

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/01-5-contract-closure/SPEC.md
```

Implement every correction required by that specification, prove its C1–C12
exit checks, and publish an honest `GO`, `HOLD`, or narrowly proved Phase 01
reopening result.

Finding reference:

```text
019fcd32-b832-7750-9eb5-5f544e39c533
```

Use that identifier as the trace for the closure work. It is not product
authority and cannot override the product PRD, completed Phase 00 evidence,
the accepted Phase 01 architecture, or accepted ADRs.

This phase corrects documentation contracts. Do not implement V2 product code,
run migration or cutover, modify live state, select an exact future backend
mechanism, or manufacture benchmark evidence.

## 2. Required first-screen result

The final response must begin with exactly one of:

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

or, only when an exact reopening condition in the specification is proved:

```text
PHASE_01_5: REOPEN_PHASE_01 — <proved hard-rule incompatibility>
FINDING_REFERENCE: 019fcd32-b832-7750-9eb5-5f544e39c533
PHASE_02: STOP
```

Immediately follow it with:

```text
architecture:             ALIGNED | REOPEN_PHASE_01
algorithm correctness:    PASS | CHANGES_REQUIRED
diagram/workflow parity:  PASS | CHANGES_REQUIRED
terminology/naming:       PASS | CHANGES_REQUIRED
link graph:               PASS | CHANGES_REQUIRED
backend extensibility:    PASS | CHANGES_REQUIRED | OPEN_EVIDENCE
performance readiness:    QUALIFIED | DESIGN_ONLY | TARGET_UNSELECTED | INCOMPARABLE | FAILED_TARGET
product source seal:      CLEAN | BASE_DRIFT
```

Do not return `PASS` because edits were made. Return it only when every Phase
01.5 exit condition has been checked against the resulting repository state.

## 3. Document lifecycle and authority

| Document | Role |
|---|---|
| Phase 01.5 `SPEC.md` | Normative input and acceptance contract |
| This `PROMPT.md` | Operational instructions; never authority over the specification |
| Files in the specification's correction manifest | Normative outputs to repair |
| Root `README.md` and `PLAN.md` | Durable program status and Phase 02 gate |
| Final agent response | Execution report, evidence ledger, and final verdict |

Do not rewrite the specification's hard rules, finding definitions, acceptance
criteria, or reopening conditions to make the work pass. A status-only update
to its opening status block is allowed after the result is proved. If the
result is `CHANGES_REQUIRED`, keep formal Phase 02 entry on hold.

Use repository sources in this descending order:

1. root product `PRD.md`, especially its hard rules and exclusions;
2. completed Phase 00 `SPEC.md` and sealed source evidence;
3. completed Phase 01 `SPEC.md`, selected `architecture_design.md`, and
   accepted ADRs;
4. Phase 01.5 `SPEC.md`;
5. selected design documents;
6. selected algorithm contracts;
7. public conceptual API contracts;
8. selected diagrams;
9. phase PRDs, plans, and test/performance documents; and
10. quarantined proposals and historical appendices as evidence only.

When a lower-authority document conflicts with a higher-authority invariant,
correct the lower-authority document. Do not weaken the higher authority to
preserve existing wording, a diagram, or an API sketch.

The following remain protected:

```text
WINNER: R0 — LayerStack-0 rewrite-in-place filesystem-native complete-Version storage
one complete immutable portable Version as accepted truth
one LayerStack-0 accepted-state/reference authority
one Head OCC point
Candidate -> VersionId -> AcceptedVersion -> AcceptedBinding -> reference
runtime adapters consume truth below the runtime-effect boundary
one-writer migration
safe retirement
```

`DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` remain `OWNER_DEC_OPEN`.

## 4. Paths and repository safety

```text
Documentation repository
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs

V2 documentation package
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2

Phase 01.5 folder
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/01-5-contract-closure

Product evidence tree — read only
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
  expected branch: codex/new-2.0-storage-core
  recorded HEAD:   e4974d1f9aac702b35e052629cb070c897989352

Historical appendix — read only and non-normative
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan
```

Both repositories may be visible to multiple agents. Preserve all unrelated
tracked, staged, and untracked work. Never reset, clean, broadly check out,
stash, switch, or rewrite files merely to obtain a clean diff.

Before editing:

1. discover and read every applicable `AGENTS.md` and `CLAUDE.md` completely;
2. record documentation-repository branch, HEAD, and full dirty/untracked
   state;
3. record the product evidence tree's branch, HEAD, and full dirty/untracked
   state; and
4. build an exact list of files this execution is allowed to change.

Run these read-only source-seal commands in the product evidence tree:

```bash
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git status --short --branch
```

Do not alter the product evidence tree. If it is missing, dirty, on a different
branch, or at a different commit, stop before semantic edits and return:

```text
PHASE_01_5: CHANGES_REQUIRED — BASE_DRIFT <exact drift>
PHASE_02: HOLD
REOPEN_PHASE_01: NO
```

Base drift is not evidence that Phase 01 must be reopened.

## 5. Required reading

The lead agent must read the following completely before approving edits.
Specialists must read the Phase 01.5 specification plus every authority and
target relevant to their assigned workstream.

### 5.1 Program and completed gates

```text
.../ephemeral-sandbox-v2/README.md
.../ephemeral-sandbox-v2/PRD.md
.../ephemeral-sandbox-v2/PLAN.md
.../ephemeral-sandbox-v2/architecture_design.md
.../ephemeral-sandbox-v2/phases/00-freeze-rules/SPEC.md
.../ephemeral-sandbox-v2/phases/01-choose-design/SPEC.md
.../ephemeral-sandbox-v2/phases/01-5-contract-closure/SPEC.md
```

### 5.2 Selected design and decisions

```text
.../ephemeral-sandbox-v2/design/README.md
.../ephemeral-sandbox-v2/design/01-ownership-and-boundaries.md
.../ephemeral-sandbox-v2/design/02-state-identity.md
.../ephemeral-sandbox-v2/design/03-state-store.md
.../ephemeral-sandbox-v2/design/04-algorithms-and-call-flows.md
.../ephemeral-sandbox-v2/design/05-concurrency-durability-recovery.md
.../ephemeral-sandbox-v2/design/06-resources-security-observability.md
.../ephemeral-sandbox-v2/design/07-performance-and-optimization.md
.../ephemeral-sandbox-v2/design/08-migration-and-cutover.md
.../ephemeral-sandbox-v2/design/09-source-and-implementation-map.md
.../ephemeral-sandbox-v2/design/10-verification-matrix.md
.../ephemeral-sandbox-v2/design/decisions/README.md
.../ephemeral-sandbox-v2/design/decisions/ADR-001-r0-complete-version-storage.md
.../ephemeral-sandbox-v2/design/decisions/ADR-002-version-id-naming.md
```

### 5.3 Algorithms, APIs, diagrams, terminology, and phase consumers

Read every Markdown document under these selected indexes, not only the files
named in a finding:

```text
.../ephemeral-sandbox-v2/algorithm/README.md
.../ephemeral-sandbox-v2/api/README.md
.../ephemeral-sandbox-v2/diagrams/README.md
.../ephemeral-sandbox-v2/branding/terminology.md
.../ephemeral-sandbox-v2/phases/02-state-identity/{PRD.md,PLAN.md,test-perf.md}
.../ephemeral-sandbox-v2/phases/03-state-store/{PRD.md,PLAN.md,test-perf.md}
```

Read linked semantic dependencies needed to determine lifecycle, recovery,
custody, retirement, migration, resource, or evidence correctness. Do not use
archived or quarantined designs as forward implementation authority.

## 6. Multi-agent execution model

Use multiple agents. The lead remains accountable for authority resolution,
the integrated edits, final verification, and the verdict.

Concurrency may be limited, so run specialists in waves. Use at least four
separately reported specialist workstreams and one independent post-edit
verification pass. A single subagent may cover two adjacent specialties when
capacity is constrained, but the final report must preserve separate verdicts.

### 6.1 Editing discipline

The safest default is:

- specialists inspect read-only and return evidence plus proposed corrections;
- the lead applies the integrated patches; and
- a specialist that proposed a correction does not provide the only final
  verification of that correction.

The lead may delegate edits only when it assigns an explicit, non-overlapping
file ownership list. Every editing agent must be told:

```text
You are not alone in the repository. Modify only your assigned files. Do not
revert, overwrite, format, or clean work belonging to another agent or the
user. Re-read shared dependencies before editing and report every changed file.
```

Do not let two agents edit the same file concurrently. Root `README.md`, root
`PLAN.md`, the Phase 01.5 `SPEC.md`, and final status publication belong to the
lead unless explicitly reassigned after all semantic edits are integrated.

### 6.2 Specialist workstreams

Assign at least these workstreams.

#### A. Reference lifecycle and API correctness

Inspect and propose or implement the closure of F-01 and F-02:

- Head create-if-absent, exact conditional replace, and exact conditional
  removal;
- fixed typed Root creation and exact conditional removal;
- explicit rejection of generic Root retargeting unless a higher-authority
  mutable kind is proved;
- complete outcomes, linearization, fence-before-success, outcome-unknown
  read-back, retry/idempotency, recovery, custody, and retirement integration;
- manager initialization, publication, rollback, checkpoint, destruction, and
  migration mappings; and
- no second writer, direct record mutation, raw-`VersionId` reference, or
  payload traversal by reference-only operations.

Primary targets:

```text
design/03-state-store.md
algorithm/02-references-and-publication/01-reference-ephcow.md
algorithm/02-references-and-publication/02-occ-publication.md
api/manager.md
```

#### B. Workflow, diagram, and publication-order parity

Inspect and propose or implement the closure of F-03 and F-04:

- Branch is represented by a Head everywhere;
- Checkpoint is a fixed typed Root;
- rollback and branch movement use Head OCC;
- no normative workflow retargets a Fork Root;
- candidate construction and durable admission complete before Head OCC;
- stale OCC preserves accepted immutable truth and accounts for an accepted
  orphan; and
- diagrams match prose visibility, authority, custody, and acknowledgement
  boundaries.

Primary targets:

```text
diagrams/03-fork-checkpoint-rollback-and-cow.md
phases/03-state-store/PRD.md
design/04-algorithms-and-call-flows.md
all diagrams or phases that repeat the affected workflows
```

#### C. Evidence, optimization, backend boundary, and terminology

Inspect and propose or implement the closure of F-05 and F-07:

- separate evidence label, source metadata, correctness result, and final
  performance verdict;
- keep Stage 4.6 `INCOMPARABLE`;
- retain `OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED` unless an owner-approved
  quantitative target exists;
- do not infer a benchmark win from complexity or a plan;
- scope accepted-reference payload movement as read/write/copy `0/0/0` while
  naming nonzero metadata, coordination, fence, and backend materialization
  work separately;
- describe OCI/Docker as current evidence rather than universal proof;
- keep Firecracker and WASI/WASM at backend status `OPEN_EVIDENCE`, with absent
  implementation evidence labelled `OPEN`; and
- preserve portable identity, Accepted Version truth, direct accepted-binding
  handoff, reference authority, and Head OCC above the runtime-effect boundary.

Primary targets:

```text
algorithm/06-resources-performance-and-evidence/02-performance-demonstration-matrix.md
api/README.md
api/runtime.md
branding/terminology.md
PRD.md
design/07-performance-and-optimization.md
runtime-related design, algorithm, API, and diagram consumers
```

Official OCI, Firecracker, and WASI/WASM primary sources may be consulted only
to validate current external runtime facts. Clearly separate external research
from repository authority and cite every nontrivial external fact. Do not
select an exact VM disk format, WASM runtime, adapter API, or materialization
strategy on the product owner's behalf.

#### D. Link graph, navigation, and orphan closure

Inspect and propose or implement the closure of F-06 and F-08:

- validate every local Markdown file link and local anchor in the complete V2
  corpus;
- repair all five known obsolete API-to-algorithm paths;
- check semantic edges from every API operation to its selected algorithm;
- check backlinks from algorithms to their API, design, phase, and diagram
  consumers where navigation requires them;
- link the three prompt/runbook documents from an appropriate index or label
  them intentionally standalone; and
- ensure the root program index, Phase 01.5 gate, and Phase 02 prerequisites
  agree.

Do not treat a path-only link pass as semantic-link parity. Report broken
paths, broken anchors, missing semantic edges, missing backlinks, and orphans
separately.

#### E. Independent final verifier

After integration, assign a fresh read-only pass to challenge the resulting
documents against:

- all F-01–F-08 closures;
- C1–C12;
- the no-P0/no-P1 exit rule;
- the lifecycle matrix;
- authority and terminology consistency;
- backend-neutral portable contracts;
- evidence and performance discipline;
- the link graph; and
- exact Phase 01 reopening conditions.

The verifier must attempt to falsify `PASS`, not merely confirm that expected
phrases exist.

### 6.3 Specialist return contract

Each specialist returns:

```text
workstream:
files inspected:
files changed: <none for read-only work>
verdict: PASS | CHANGES_REQUIRED | OPEN_EVIDENCE | REOPEN_PHASE_01
findings:
  - severity: P0 | P1 | P2 | P3
    evidence: <absolute clickable path and line>
    violated authority or invariant:
    consequence:
    minimal within-R0 correction:
    verification:
open evidence:
disagreements or assumptions:
```

The lead must deduplicate reports and resolve conflicts by authority, not by
majority vote. Preserve a minority concern when the evidence remains
indeterminate.

## 7. Required semantic implementation

The resulting documents must agree on these semantic operations. Names below
are conceptual; do not prematurely select Rust or wire syntax.

```text
CreateHeadIfAbsent(head_identity, Expected::Absent, new_binding)
ReplaceHead(Expected::Exact(expected_head), new_binding)
RemoveHead(Expected::Exact(expected_head))
CreateFixedRootIfAbsent(root_identity, root_kind, Expected::Absent, binding)
RemoveFixedRoot(Expected::Exact(expected_root))
```

Every operation must define:

1. typed inputs and the complete expected-state comparison;
2. authority and preconditions;
3. semantic linearization point;
4. durable-success boundary;
5. exact stale/absent/already-present behavior;
6. retry and idempotency behavior;
7. cancellation and crash prefixes;
8. `OUTCOME_UNKNOWN` and authoritative read-back;
9. payload and metadata I/O classes;
10. custody/reachability effects;
11. retirement and cleanup-debt effects; and
12. caller mapping.

Preserve at least these outcome distinctions:

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

Do not create two conceptually different transition mechanisms merely because
Head and Root records have different mutation policies. The single reference
authority governs them; only Head supports replacement in the selected model.

## 8. Integration order

Apply corrections in causal order:

1. freeze the source seal, allowed file list, and pre-existing docs state;
2. resolve lifecycle semantics and normative vocabulary;
3. correct the reference and OCC algorithms;
4. correct manager/runtime API mappings;
5. correct workflows and diagrams;
6. correct recovery, custody, retirement, and migration links;
7. normalize evidence, performance, backend, and zero-payload wording;
8. repair physical and semantic link-graph defects;
9. run the independent verification wave;
10. publish program status only after the verdict is known.

When a correction reveals another consumer with the same contradiction, add
that consumer to the allowed file list and record why it was necessary. Do not
turn that rule into permission for broad stylistic rewriting.

## 9. Evidence and decision-state rules

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

Use only these final performance verdicts:

```text
QUALIFIED
DESIGN_ONLY
TARGET_UNSELECTED
INCOMPARABLE
FAILED_TARGET
```

Do not conflate:

- source branch/commit/clean state with an evidence label;
- `BENCHMARK-QUALIFIED` evidence with the final `QUALIFIED` verdict;
- a correctness result with performance qualification;
- backend status `OPEN_EVIDENCE` with the evidence label `OPEN`; or
- `OPEN_WITHIN_R0` with `OWNER_DEC_OPEN`.

No current qualified benchmark run is required to pass Phase 01.5. Honest
`TARGET_UNSELECTED` and `OPEN_EVIDENCE` states may remain when they are isolated
behind the stable architecture seams. Never invent a target, workload,
percentile, comparison factor, or production-performance claim.

## 10. Verification requirements

Run all checks needed to prove the Phase 01.5 specification's C1–C12. At a
minimum:

1. validate every Markdown file link and local anchor in the V2 corpus;
2. enumerate every Head and Root lifecycle operation and its algorithm link;
3. search every normative file for Branch, Fork Root, Root retarget/update,
   checkpoint, rollback, Head creation/removal, and publication-order language;
4. compare every affected diagram with the corrected algorithms and APIs;
5. search for stale `StateId`, generic “state,” mutable accepted truth,
   raw-ID authority, second writer/OCC, and legacy storage-family language;
6. search for unsupported “zero-copy,” “constant time,” benchmark-win, and
   production-performance language;
7. enumerate evidence labels, decision states, source seals, correctness
   results, and final performance verdicts by category;
8. verify OCI-specific mechanics do not appear above the runtime-effect
   boundary;
9. verify `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` remain open;
10. verify Phase 02 owns only `ID-001`, `ID-002`, and `ID-003` within the frozen
    architectural input;
11. verify the resulting changed-file list contains no product source, live
    state, migration data, or unrelated documentation; and
12. rerun source-seal and repository-status checks before the verdict.

Text search is discovery, not proof. Inspect every hit in context. A term may
be valid in a historical/quarantine notice and invalid in a normative flow.

No product build, Docker gateway rebuild, sandbox operation, runtime test, or
benchmark is required for this documentation-only gate. Do not use an unneeded
runtime command as ceremony. If execution unexpectedly requires product-code
or live-runtime changes, stop and report the scope conflict.

## 11. Pass, hold, and reopening discipline

Return `PASS` only when the resulting repository proves:

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

Open implementation, filesystem, backend, or benchmark evidence is compatible
with `PASS` only when the design/API seam is complete, the evidence gap is
explicit, and no Phase 02 architectural input depends on choosing it.

Return `CHANGES_REQUIRED` for any repairable within-R0 contradiction, missing
semantic link, incomplete lifecycle algorithm, invalid diagram, broken link,
taxonomy drift, or accidental backend-specific assumption above the
runtime-effect boundary.

Return `REOPEN_PHASE_01` only when reproducible evidence proves that required
semantics cannot be supported by the accepted complete-Version owner and
direct runtime handoff without changing one of the architecture's hard rules.
Quote the exact reopening condition from the Phase 01.5 specification and
provide the proof. Missing evidence, incomplete documents, or a difficult
implementation is not that proof.

## 12. Status publication

After all checks:

### If `PASS`

- update the Phase 01.5 opening status to passed without changing its
  normative acceptance criteria;
- update root `README.md` and `PLAN.md` to record Phase 01.5 complete;
- change Phase 02 from held to authorized/not-started as appropriate;
- keep Phase 03 and later phases governed by their stated dependencies;
- keep backend evidence and optimization target states honest; and
- include the finding reference in the durable status update.

### If `CHANGES_REQUIRED`

- keep Phase 02 formal implementation on hold;
- do not mark Phase 01.5 complete;
- record exactly what remains, where, and how it can be verified; and
- preserve all completed corrections that are internally consistent.

### If `REOPEN_PHASE_01`

- do not silently replace R0;
- do not continue downstream corrections whose assumptions are invalidated;
- keep Phase 02 stopped; and
- report the smallest exact architecture question that must be reopened.

## 13. Required final report

After the first-screen result and compact status block, return:

1. executive verdict and whether formal Phase 02 may begin;
2. source seal and repository-state evidence;
3. multi-agent workstream roster, ownership, and verdicts;
4. F-01–F-08 closure matrix with absolute clickable file-and-line evidence;
5. Head/Root lifecycle matrix and API-to-algorithm mapping;
6. publication-order and diagram parity result;
7. evidence, performance, and backend-boundary result;
8. link-graph results: paths, anchors, semantic edges, backlinks, and orphans;
9. C1–C12 verification matrix;
10. remaining `OPEN_WITHIN_R0`, `OPEN`, and `OWNER_DEC_OPEN` items;
11. exact Phase 01 reopening-condition assessment;
12. changed-file manifest with one-line purpose per file;
13. commands and checks run, including failures and reruns; and
14. limitations or evidence that was unavailable.

Every actionable unresolved finding must have a severity, absolute clickable
local path, line number, violated invariant, consequence, minimal correction,
and verification step. Every nontrivial external fact must cite a current
official or primary source and be labelled separately from repository
authority.

Do not stage, commit, push, open a pull request, modify product code, or proceed
into Phase 02 unless the user separately requests that action.
