# Agent prompt — multi-agent Phase 02 alignment review

Use this prompt in a new lead-agent session to review the current Phase 02
documentation and algorithm package. This is a read-only design, correctness,
performance, terminology, diagram, link-graph, and extensibility review. Do not
implement product code or silently rewrite the architecture.

## 1. Review context and fixed progress

Phase 01 is finished. Its selected result is fixed:

```text
WINNER: R0 — LayerStack-0 rewrite-in-place filesystem-native complete-Version storage
```

The current work is the overall Phase 02 documentation review. Algorithms,
conceptual APIs, call flows, diagrams, resource models, and demonstration plans
were expanded after the Phase 01 selection. Review whether those additions are
perfectly aligned with the accepted R0 architecture and with one another.

Do not run another architecture tournament. Do not replace R0 with CAS+CDC, a
manifest/Chunk DAG, a parent/layer chain, reflink-backed truth, a database, a
new service, a second writer, or a backend-neutral storage framework. If—and
only if—evidence proves R0 cannot satisfy a hard rule, return
`REOPEN_PHASE_01` with the exact architecture-changing failure.

This is a review, not an editing session:

- do not modify documentation, product code, tests, live state, migration data,
  or the pinned product worktree;
- report exact findings and recommended changes with file-and-line evidence;
- do not accept product-owner decisions on the owner's behalf; and
- do not turn an unimplemented design, complexity argument, or benchmark plan
  into an implementation, qualification, or performance claim.

## 2. Required first-screen result

The final review must begin with exactly one result:

```text
PHASE_02_ALIGNMENT_REVIEW: PASS
```

or:

```text
PHASE_02_ALIGNMENT_REVIEW: PASS_WITH_OPEN_EVIDENCE — <specific unproved but architecture-preserving items>
```

or:

```text
PHASE_02_ALIGNMENT_REVIEW: CHANGES_REQUIRED — <highest-severity documentation or algorithm defect>
```

or:

```text
PHASE_02_ALIGNMENT_REVIEW: REOPEN_PHASE_01 — <specific architecture-changing failure>
```

Use the statuses precisely:

- `PASS` means the documents are internally and externally consistent and every
  required claim is supported at its stated evidence level.
- `PASS_WITH_OPEN_EVIDENCE` means the design is coherent within R0, but named
  implementation, spike, filesystem-qualification, backend-conformance, target,
  or benchmark evidence is still open. This is not a performance pass.
- `CHANGES_REQUIRED` means the problem can be repaired within R0 by correcting
  algorithms, complexity, diagrams, APIs, wording, naming, links, evidence
  labels, or phase-owned details.
- `REOPEN_PHASE_01` is reserved for a proved failure that changes ownership,
  storage family, dependency direction, writer count, crash model, or hard-rule
  satisfiability. Documentation quality problems do not reopen Phase 01.

Also print this compact status block immediately below the result:

```text
architecture:             ALIGNED | REOPEN_PHASE_01
algorithm correctness:    PASS | CHANGES_REQUIRED | OPEN_EVIDENCE
complexity accounting:    PASS | CHANGES_REQUIRED | OPEN_EVIDENCE
diagram/workflow parity:  PASS | CHANGES_REQUIRED
terminology/naming:       PASS | CHANGES_REQUIRED
link graph:               PASS | CHANGES_REQUIRED
backend extensibility:    PASS | CHANGES_REQUIRED | OPEN_EVIDENCE
performance readiness:    QUALIFIED | DESIGN_ONLY | TARGET_UNSELECTED | INCOMPARABLE
product source seal:      CLEAN | BASE_DRIFT
```

## 3. Mandatory multi-agent review orchestration

The lead reviewer must launch multiple independent subagents. Use parallel
waves if concurrency is limited. All subagents are read-only and must return
evidence to the lead reviewer; they may not edit files.

Assign at least these specialist roles:

1. **Architecture and authority auditor**
   - Verify the product PRD hard rules, Phase 01 output, accepted ADRs,
     ownership, dependency direction, and open owner decisions.
   - Decide whether each finding is `OPEN_WITHIN_R0`, a documentation defect,
     or an exact `REOPEN_PHASE_01` condition.

2. **Algorithm and API correctness reviewer**
   - Review identity, admission, complete-Version content addressing, reference
     EphCoW, OCC publication, read custody, materialization, recovery,
     retirement, cleanup, and migration as one composed state machine.
   - Check preconditions, typed outcomes, termination, collision handling,
     concurrency, retry, cancellation, crash prefixes, idempotency,
     linearization, durable visibility, and cleanup.

3. **Complexity and performance analyst**
   - Re-derive worst-case time, CPU, memory, temporary space, persistent space,
     payload I/O, metadata I/O, descriptors, workers, locks, custody, staging,
     recovery work, and cleanup-debt costs.
   - Audit the optimization targets and the Stage 4.6 comparison discipline.

4. **Diagram and workflow auditor**
   - Compare every ASCII or Mermaid flow with the prose algorithms, conceptual
     APIs, ownership map, state transitions, and visibility points.
   - Find missing arrows, reversed dependencies, hidden byte-moving steps,
     duplicated authorities, or diagrams that imply a second Head point.

5. **Terminology and API naming editor**
   - Enforce the locked Version vocabulary, capitalization, type distinctions,
     API responsibility names, evidence labels, and historical-term rules.

6. **Documentation link-graph auditor**
   - Build and validate the complete Markdown document graph, including local
     paths, anchors, indexes, backlinks, algorithm dependencies, phase/design
     authority links, and stale flat-path references.

7. **Runtime-backend extensibility researcher**
   - Audit separation between portable Version semantics, LayerStack-0
     storage/reference authority, and existing runtime-effect owners.
   - Evaluate whether OCI/container, Firecracker, and WASM/WASI activation can
     use the same accepted Version and reference contracts without entering
     identity or requiring a new storage authority.

8. **Evidence and benchmark auditor**
   - Verify source seals, evidence labels, benchmark comparability, workload
     definitions, correctness gates, target provenance, and claim wording.

When capacity is limited, combine adjacent roles but preserve eight separately
reported verdicts. Require each specialist to report:

```text
role:
verdict: PASS | CHANGES_REQUIRED | OPEN_EVIDENCE | REOPEN_PHASE_01
findings:
  - severity: P0 | P1 | P2 | P3
    evidence: <absolute path:line plus concise excerpt/paraphrase>
    violated authority or invariant:
    consequence:
    minimal within-R0 correction:
    verification needed:
open evidence:
```

The lead reviewer must deduplicate findings, resolve disagreements by the
authority order below, and preserve minority concerns when evidence is not
decisive. A majority vote cannot override the product PRD or accepted ADRs.

## 4. Authority order and required reading

Read the following before reaching conclusions. The product PRD and its hard
rules outrank every later document.

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/README.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/PRD.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/PLAN.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/architecture_design.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/branding/terminology.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/README.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/01-ownership-and-boundaries.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/02-state-identity.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/03-state-store.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/04-algorithms-and-call-flows.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/05-concurrency-durability-recovery.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/06-resources-security-observability.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/07-performance-and-optimization.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/08-migration-and-cutover.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/09-source-and-implementation-map.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/10-verification-matrix.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/decisions/README.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/decisions/ADR-001-r0-complete-version-storage.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/decisions/ADR-002-version-id-naming.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/00-freeze-rules/SPEC.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/01-choose-design/SPEC.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/02-state-identity/PRD.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/03-state-store/PRD.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/algorithm/README.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/algorithm/**/*.md
```

Authority rules:

1. Product PRD hard rules.
2. Phase 00 measured e497 evidence.
3. Phase 01 selection input.
4. Accepted Phase 01 output and accepted ADRs.
5. Phase 02 and Phase 03 phase-owned contracts.
6. Detailed design and algorithm documents.
7. Historical implementation-plan material, which is evidence-only and cannot
   override the selected architecture.

Do not use this review prompt or any algorithm document as authority over a
higher-ranked source.

## 5. Product-source seal

The product tree is read-only:

```text
path:            /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
expected branch: codex/new-2.0-storage-core
recorded HEAD:   e4974d1f9aac702b35e052629cb070c897989352
```

Before any command in that tree, read its `AGENTS.md` and `CLAUDE.md`
completely. Then run the Phase 01 seal commands. Do not switch, edit, commit,
reset, clean, build, or run destructive/live-state commands.

If branch, HEAD, tracked status, staged status, or untracked status differs
from the recorded clean base:

- report `product source seal: BASE_DRIFT`;
- mark source-placeability conclusions `OPEN: BASE_DRIFT`; and
- do not substitute conclusions from another branch, commit, or worktree.

## 6. Locked architecture, terminology, and ownership

Use this authority chain everywhere:

```text
Candidate
  -> VersionId
  -> AcceptedVersion
  -> AcceptedBinding
  -> Head + HeadRevision or typed Root
```

Enforce these distinctions:

- `VersionId` is typed, content-derived Candidate identity—not equality,
  existence, admission, reference authority, or an unchecked raw digest.
- `AcceptedVersion` is LayerStack-0-verified durable admission of canonical
  bytes and one complete immutable payload closure.
- `AcceptedBinding` is issued or revalidated only by LayerStack-0 admission.
- Heads and Roots contain AcceptedBindings, never unchecked raw IDs.
- `Head` is mutable selected reference state with monotone `HeadRevision`.
- `Root` is a fixed typed durable reachability reference.
- `Workspace` is mutable runtime-effect-owned state and never Version identity
  or accepted selected truth.
- `EphCoW` means reference-level copy-on-write over AcceptedBindings plus
  runtime-owned isolated writable Workspaces. It is not payload mutation,
  mandatory reflink cloning, a layer reconstruction chain, or a Chunk store.

Historical vocabulary—`StateId`, “state store,” “State Store,”
“selected-state owner,” PMSS, and raw digest references—may occur only when
explicitly labelled historical or in stable legacy folder slugs. New APIs,
types, diagrams, metrics, tests, and prose must use the Version model.

Preserve this ownership:

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
  Workspace, OverlayFS or backend-specific activation,
  mount/namespace/exec and manager/daemon lifecycle

observability -> diagnostic reader only
```

The product-owner decisions `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018`
must remain `OWNER_DEC_OPEN` at their documented application/API seams.

## 7. Algorithmic correctness and API review—the highest-priority gate

Algorithmic correctness and performance are the most important review axes.
For every normative algorithm, independently verify all of the following.

### 7.1 Contract completeness

- Purpose and owning phase are explicit.
- Inputs, outputs, preconditions, typed outcomes, and failure outcomes compose
  with callers and callees.
- Pseudocode is finite, unambiguous, and consistent with prose and diagrams.
- Conceptual APIs express responsibility and type flow without inventing exact
  Rust signatures, codec bytes, filenames, syscalls, or numeric bounds that an
  owning phase has not selected.
- Normal, concurrent, retry, cancellation, crash, unknown-outcome, and cleanup
  behavior is defined.
- Each operation has exactly the appropriate linearization or durable-
  visibility point, or explicitly states why none applies.
- Untrusted paths, facts, identifiers, records, and backend inputs have bounded
  validation and fail-closed behavior.

### 7.2 Global safety invariants

Prove composition around these invariants:

1. One complete immutable Version is truth; no layer reconstruction.
2. Equal canonical bytes under one occupied `VersionId` converge on one
   physical payload closure.
3. Occupancy equality uses full canonical-byte comparison; digest or length
   equality is insufficient and mismatch is collision.
4. Only LayerStack-0 admission creates or revalidates AcceptedBindings.
5. Heads and Roots contain AcceptedBindings, never unchecked IDs.
6. Reference-only Fork, Checkpoint, rollback, Root creation, and same-Version
   movement have payload bytes read/written/copied `0/0/0` and payload opens
   `0` within the reference scope.
7. Head publication has one state-changing OCC linearization point: conditional
   replacement of one complete Head record under the sole transition gate.
8. A stale writer loses without silent merge, rebase, expected-value refresh,
   or retry against a newly observed Head.
9. Accepted payloads cannot be modified by live Workspace writes.
10. Authorization, MCTS/rollout policy, scores, and product ordering remain
    outside LayerStack-0.
11. Runtime-private and backend-specific facts are absent from portable
    identity and accepted reference authority.
12. Migration has at most one writable selected-Version truth, generation
    fences stale work, and temporary compatibility code remains deletable.
13. Staging, memory, temporary/persistent disk, FDs, workers, locks, custody,
    recovery work, retirement work, and cleanup debt are bounded and fail
    closed.

### 7.3 Concurrency, crash, and lifecycle proofs

Construct adversarial schedules and crash-prefix tables for at least:

- equal Candidates admitted concurrently;
- unequal canonical Candidates forced under one occupied `VersionId`;
- two publishers with the same expected binding and `HeadRevision`;
- same-target concurrent publishers;
- lost acknowledgement before or after possible Head replacement;
- cancellation before admission visibility, after admission but before Head
  publication, and after possible publication;
- read-custody capture racing final Root/Head removal and retirement;
- cleanup/recovery racing admission or reference creation;
- process restart with private staging, an accepted orphan, an ambiguous
  control record, or partial private materialization; and
- migration restart and stale-generation legacy/import workers.

For each schedule, identify prior truth, possible new truth, typed result,
resource debt, cleanup owner, and the exact point that orders the race.

Report a P0 finding if any schedule permits:

- two selected truths;
- an incomplete accepted payload;
- unchecked raw-ID reference authority;
- accepted-payload mutation;
- more than one Head linearization point;
- a stale writer to succeed silently;
- deletion of reachable or custodied truth; or
- unbounded work or fail-open recovery.

## 8. Diagram and workflow parity review

Inventory every ASCII and Mermaid diagram in the root, design, phase, cluster,
and algorithm documents. Build a normalized graph for each diagram:

```text
node -> authoritative term/type/owner
edge -> conceptual API, data flow, control flow, or durable transition
annotation -> evidence label, cost scope, or visibility point
```

Then verify:

- every diagram node uses the locked terminology;
- every arrow direction matches the ownership and dependency map;
- the end-to-end flow preserves
  `Candidate -> VersionId -> AcceptedVersion -> AcceptedBinding -> Head/Root`;
- byte-moving Candidate capture, admission, activation, and materialization are
  visually separated from zero-payload reference movement;
- diagrams never imply that observability, runtime effects, OCI, Firecracker,
  WASM, a raw ID, or a Workspace can issue an AcceptedBinding or mutate a Head;
- all Head diagrams show the same single conditional replacement point;
- crash/recovery diagrams show prior, complete-new, or fail-closed outcomes;
- migration diagrams show one writable truth at every generation;
- diagram labels and pseudocode operation names correspond one-to-one or have
  an explicit terminology mapping; and
- every diagram has a nearby link to its authoritative algorithm and every
  algorithm links back to the higher-level flow it refines.

Classify any unexplained diagram/prose mismatch as at least P1. Cosmetic layout
problems are P3 only when they cannot alter interpretation.

## 9. Complexity, speed, time, space, memory, and I/O review

Create one shared symbol table. Detect symbols that change meaning across
files. At minimum reconcile:

```text
B       complete canonical comparison bytes
E       portable filesystem entry count
V       logical bytes in one complete Version payload
P_path  total path-validation/ordering work
M_fs    or Ops_fs: filesystem metadata operations
L_id    occupied-VersionId admission contention/wait
L_gate  sole transition-gate contention/wait
N_h     Head records examined
N_r     Root records examined
N_c     live custody records/tokens examined
D_n     cleanup/recovery debt item count
D_b     cleanup/recovery debt bytes
K       selected bounded batch size
w       bounded workers
b       bounded per-worker buffer bytes
```

For every algorithm, independently derive and compare:

- worst-case CPU/time complexity;
- wall-time terms that include lock wait, durability fences, backend
  activation, and bounded retries where applicable;
- peak heap and fixed metadata memory;
- private staging and persistent space;
- payload bytes read, written, copied, and opened;
- canonical comparison bytes read;
- filesystem metadata operations and durability fences;
- FDs, workers, locks, queues, reservations, and custody;
- recovery, retirement, migration, and cleanup-debt work; and
- best/expected-case notes only after the honest worst case is stated.

The audit must check at least these expected scopes without assuming their
correctness:

- canonicalization includes content/path traversal and deterministic ordering;
- typed-ID derivation is linear in canonical bytes;
- occupied-ID equality is a complete worst-case byte comparison;
- admission includes complete payload construction, validation, fencing, and
  possible staging cleanup;
- reference-only operations are bounded-record operations with payload I/O
  `0/0/0` and open count `0`;
- accepted-only publication is a bounded Head-record operation plus gate and
  durability costs, while Candidate-to-Head publication also includes
  admission costs;
- runtime activation costs are not hidden inside the zero-payload reference
  claim;
- complete private materialization accounts for all source reads, destination
  writes, metadata work, bounded buffers, and destination space;
- recovery/retirement costs include exact reference/custody inspection or the
  Phase 03-selected bounded equivalent; and
- migration cost includes legacy reads, translation, ordinary V2 admission,
  progress fencing, verification, orphan handling, and temporary-code cleanup.

Reject any complexity statement that:

- treats hashing or length equality as full equality;
- calls a reference operation zero-copy while including uncounted activation
  or materialization work in the same scope;
- hides payload construction, fence, lock, metadata, staging, recovery, or
  cleanup costs;
- uses average-case language as a hard bound;
- assumes reflink, page cache, filesystem snapshots, or deduplication for
  correctness;
- permits memory, FDs, workers, staging, queues, custody, or cleanup debt to
  grow without a selected bound and fail-closed response; or
- claims a formal performance guarantee from asymptotic analysis alone.

## 10. Wording and naming-convention review

Review headings, prose, diagrams, pseudocode, APIs, outcomes, variables,
metrics, test names, and links for the following:

- `LayerStack-0`, `EphCoW`, `Version`, `VersionId`, `AcceptedVersion`,
  `AcceptedBinding`, `Head`, `HeadRevision`, `Root`, `Branch`, `Checkpoint`, and
  `Workspace` use one spelling and one meaning.
- “CAS” is qualified as complete-Version content-derived addressing when used
  inside R0; it must not imply a selected cross-Version CAS object store.
- “CDC” appears only as explicitly non-selected comparison or an evidence-based
  Phase 01 reopening gate.
- “CoW” does not imply accepted-payload mutation or a mandatory filesystem
  clone primitive; the selected term is EphCoW.
- “zero-copy” is replaced or scoped precisely as zero **payload** I/O for
  reference-only operations unless kernel/user-copy behavior was actually
  instrumented and proved.
- “backend agnostic” is not used to introduce a backend-neutral storage
  framework. Prefer “runtime-backend-independent Version/reference semantics”
  or “backend-decoupled runtime handoff” where that is the intended claim.
- `SOURCE-VERIFIED`, `SPIKE-VERIFIED`, `INFERRED`, `OPEN`,
  `OPEN_WITHIN_R0`, `OWNER_DEC_OPEN`, `DESIGN_ONLY`, `INCOMPARABLE`, and
  `QUALIFIED` are not conflated.
- “fast,” “optimized,” “better,” “zero cost,” “production-ready,” and similar
  words have a defined scope, metric, target, evidence state, and workload—or
  are removed.

Report terminology drift even when the underlying algorithm is correct,
because naming drift can create a second apparent authority.

## 11. Link-graph audit—the currently highest-risk documentation area

Treat link quality as a graph-integrity problem, not only a broken-file check.

### 11.1 Mechanical validation

Recursively inspect all Markdown under `ephemeral-sandbox-v2`, with a focused
report for `algorithm/`:

- resolve every relative file link from the containing document;
- validate every explicit Markdown anchor against the target heading/anchor;
- identify absolute local paths used where a stable relative link is possible;
- detect stale pre-clustering flat algorithm paths;
- detect case-only filename or anchor mismatches;
- detect links into historical/evidence-only documents that are presented as
  normative authority;
- validate code-fence balance so links are not accidentally hidden in broken
  Markdown; and
- classify external links and verify that any current technical claim uses a
  primary/official source.

### 11.2 Semantic connectivity

Build a directed adjacency table and require:

- root V2 README/PLAN/architecture documents link to the current algorithm
  package where the workflow is delegated;
- the algorithm root README reaches every cluster index and normative
  algorithm file;
- every cluster index links back to the algorithm root and to every child in
  its prescribed reading order;
- every normative algorithm links to its immediate caller, callee, durability,
  lifecycle, resource, demonstration, and authority documents when relevant;
- high-level design flows and detailed algorithms have backlinks rather than
  one-way orphan references;
- comparative or reopening documents link clearly to the selected normative
  algorithm they do **not** replace;
- no normative algorithm is orphaned or reachable only through a search; and
- duplicate definitions identify one authority and use links elsewhere.

For each weak or missing semantic edge, report:

```text
source document and section
missing/incorrect target
relationship: authority | refines | calls | durability | recovery | evidence | comparison
reader consequence
recommended relative link and anchor
```

Produce a small document-graph summary with:

- total Markdown files scanned;
- file links and anchor links checked;
- broken links;
- stale links;
- orphan normative files;
- missing backlinks;
- duplicate-authority risks; and
- links whose normative/evidence status is ambiguous.

Do not declare the link graph `PASS` merely because every target file exists.

## 12. Runtime-backend extensibility: OCI, Firecracker, and WASM

The selected storage architecture remains filesystem-native R0. The required
extensibility is semantic and ownership separation—not a new generic storage
framework.

Audit three planes independently:

```text
portable Version plane
  canonical facts, VersionId, AcceptedVersion meaning
                    |
                    v
LayerStack-0 reference/storage plane
  complete immutable payload, AcceptedBinding, Head/Root, OCC,
  custody, recovery, retirement
                    |
                    v
existing runtime-effect plane
  backend-specific protected activation or private materialization
  OCI/container | Firecracker | WASM/WASI
```

The first two planes must not contain backend identity such as OCI image IDs,
container layer IDs, OverlayFS paths, Firecracker snapshot or block-device
identities, VM mount paths, WASM module IDs, WASI preopen paths, host paths,
kernel namespaces, process IDs, sessions, leases, or runtime custody tokens.

For each backend, produce a conformance row covering:

| Question | OCI/container | Firecracker | WASM/WASI |
|---|---|---|---|
| Same portable Candidate facts and VersionId semantics? | | | |
| Same AcceptedVersion and AcceptedBinding authority? | | | |
| Backend-specific activation/materialization owned below LayerStack-0? | | | |
| Accepted payload kept immutable? | | | |
| Writable Workspace isolated and runtime-owned? | | | |
| Activation/materialization byte and memory costs separately accounted? | | | |
| Cleanup and custody lifecycle mapped to an existing owner? | | | |
| Optional acceleration has a correctness-preserving fallback? | | | |
| Current evidence state: source, spike, inferred, or open? | | | |

OCI being the only currently tested backend is acceptable only when it is
labelled as current evidence rather than a universal proof. Firecracker and
WASM support may remain `OPEN_EVIDENCE`, but the core algorithms and APIs must
not make them impossible or require changes to portable identity, Accepted
Version truth, reference authority, or Head OCC.

Reviewers may consult current official OCI, Firecracker, and WASI/WASM sources
to validate external runtime facts. Cite primary sources and clearly separate
external research from repository authority. Do not select an exact future VM
disk format, WASM runtime, adapter API, or materialization strategy on the
product owner's behalf.

Return `CHANGES_REQUIRED` if the documents accidentally embed OCI-only
assumptions above the runtime-effect boundary. Return `REOPEN_PHASE_01` only if
proved required backend semantics cannot be supported by the accepted complete-
Version owner and direct runtime handoff without changing an architectural hard
rule.

## 13. Optimization targets and Stage 4.6 benchmark discipline

The review must take the optimization goal seriously without inventing proof.
The desired direction is materially better performance than the Stage 4.6 POC,
but Stage 4.6 is currently `INCOMPARABLE`. Historical numbers without a sealed
source closure, matched semantics, and matched rerun provenance cannot rank R0
or establish a V2 target.

First extract every authoritative optimization target from the product PRD,
PLAN, phases, design documents, and accepted decisions. For each target record:

```text
target owner
metric
operation scope
workload/data shape
concurrency
backend
filesystem
durability level
cache state
statistic/percentile
threshold or required improvement factor
resource ceilings
correctness gates
evidence state
```

If “much better than 4.6” has no owner-approved numerical meaning, report:

```text
OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED
```

Do not invent a percentage, multiplier, percentile, dataset, or absolute
latency. Recommend the exact owner decision needed.

Before any comparative claim, require a benchmark closure containing:

- exact source commit and clean/dirty/untracked state;
- build profile, compiler/tool versions, features, and configuration;
- hardware, kernel/OS, filesystem, storage device, runtime backend, and
  resource limits;
- durability semantics and fence policy;
- dataset generator and sealed workload corpus;
- entry/byte/path distributions and adversarial cases;
- cache-cold, cache-warm, and restart protocol where relevant;
- concurrency and scheduling protocol;
- repetitions, exclusions, timeouts, failures, and raw results;
- wall time, CPU time, RSS/peak memory, allocations, bytes read/written/copied,
  metadata operations, disk usage/amplification, FDs, workers, locks, custody,
  staging, recovery, and cleanup debt;
- correctness results for identity equality, collision, zero-payload reference
  I/O, OCC stale behavior, immutability, crash recovery, retirement safety, and
  one-writer migration; and
- statistical summaries with confidence/variance and tail behavior.

Compare only matched operation scopes. In particular:

- do not compare zero-payload reference movement with full runtime
  materialization;
- do not compare weaker durability with stronger durability;
- do not compare different cache states, backend effects, data shapes, failure
  handling, or cleanup accounting;
- do not ignore failed/cancelled attempts, staging, accepted orphans, recovery,
  or debt; and
- invalidate performance qualification when a correctness gate fails.

The final performance verdict must be one of:

```text
QUALIFIED — matched implementation evidence meets an owner-approved target
DESIGN_ONLY — complexity and benchmark plan exist, but no qualified run exists
TARGET_UNSELECTED — “much better” has no authoritative quantitative target
INCOMPARABLE — evidence closures or semantics are not matched
FAILED_TARGET — matched qualified evidence misses the selected target
```

Never translate `DESIGN_ONLY`, `TARGET_UNSELECTED`, or `INCOMPARABLE` into a
benchmark-win or production-performance statement.

## 14. Evidence and severity rules

Use these labels exactly:

- `SOURCE-VERIFIED`: directly supported by the sealed product source or
  authoritative repository documents.
- `SPIKE-VERIFIED`: supported by a reproducible disposable implementation or
  test with sealed inputs and outputs.
- `BENCHMARK-QUALIFIED`: supported by a matched benchmark closure and all
  correctness gates.
- `INFERRED`: a design deduction that is internally reasoned but not yet
  executed or qualified.
- `OPEN`: a missing decision or evidence item.
- `OPEN_WITHIN_R0`: a phase-owned choice isolated without changing R0.
- `OWNER_DEC_OPEN`: one of the four owner decisions that the review may not
  settle.
- `INCOMPARABLE`: evidence cannot support a fair ranking.

Severity:

- `P0`: hard-rule violation, data-loss/corruption path, authority split, second
  writer/Head point, mutable accepted truth, unsafe retirement, fail-open
  recovery, or proved Phase 01 reopening condition.
- `P1`: algorithm/API/diagram/complexity contradiction that can produce an
  incorrect implementation or invalid performance conclusion.
- `P2`: important missing bound, evidence seam, backend abstraction, semantic
  link, or terminology distinction that leaves implementation ambiguous.
- `P3`: localized wording, presentation, or low-risk navigation defect.

Do not inflate severity merely because a detail is open. Do not reduce severity
because several documents repeat the same defect.

## 15. Required final report

Return the report in this order:

1. The required first-screen result and compact status block.
2. Executive verdict: whether Phase 02 can proceed within completed Phase 01.
3. P0/P1 findings, ordered by severity and causal dependency.
4. P2/P3 findings.
5. Algorithm/API correctness matrix.
6. Diagram/workflow parity matrix.
7. Complexity and resource matrix with independently derived formulas.
8. Terminology and naming drift table.
9. Link-graph report, including broken links, missing semantic edges, backlinks,
   and orphans.
10. OCI/Firecracker/WASM conformance matrix with evidence labels.
11. Optimization-target and Stage 4.6 evidence verdict.
12. Cross-file invariant proof summary.
13. Phase-owned `OPEN_WITHIN_R0` items.
14. `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018`, each still open with its
    stable seam.
15. Exact `REOPEN_PHASE_01` conditions, stating whether any is triggered.
16. Prioritized within-R0 correction plan; recommendations only, no edits.
17. Files and sources inspected, commands/checks run, and any audit limitation.

Every actionable finding must include an absolute clickable local path and a
line number. Every nontrivial external fact must cite a current official/primary
source. Clearly label inference.

## 16. Final consistency gates before reporting

Before returning the result, verify all of the following:

- Phase 01 remains finished and R0 remains the selected architecture unless an
  exact hard-rule failure is proved.
- All algorithm, API, prose, and diagram flows use the same authority chain.
- All algorithms terminate or fail closed within finite declared resources.
- Full canonical-byte comparison—not digest/length equality—controls occupied-
  ID equality.
- Reference-only zero-payload scope is not confused with activation or
  materialization.
- One conditional complete Head-record replacement is the sole state-changing
  Head linearization point.
- Every complexity formula defines its variables and includes worst-case time,
  memory, temporary/persistent space, and I/O/resource dimensions.
- Runtime-backend-independent semantics do not become a new storage facade or
  framework.
- OCI-only evidence is not presented as Firecracker/WASM proof.
- All links and anchors resolve, every normative document is reachable, and
  important higher-level/detail relationships are bidirectional.
- Prohibited architecture terms occur only as rejected, comparative,
  historical, optional non-required acceleration, or reopening material.
- All four owner decisions remain open.
- Stage 4.6 remains `INCOMPARABLE` until a matched closure exists.
- “Much better” is quantified by an authoritative target or reported
  `OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED`.
- No benchmark winner, V2 performance guarantee, backend support claim, or
  production-readiness claim exceeds its evidence.
- The pinned product tree and all live/migration data remain unchanged.

The objective is perfect alignment of authority, algorithms, APIs, diagrams,
complexity, naming, links, extensibility, and evidence—not a superficially
positive verdict.
