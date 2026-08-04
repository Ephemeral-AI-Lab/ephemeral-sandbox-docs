# Next-agent prompt: redraft as a phase-based implementation plan

Status: **EXECUTION PROMPT — REDRAFT DOCUMENTATION ONLY; DO NOT IMPLEMENT V2**

Copy this complete prompt into a fresh Codex task. The current three-phase
model is an incumbent to challenge, not a conclusion to preserve. This prompt
authorizes edits only to the documentation package named below. It does not
authorize product-code changes, Phase 0 execution, candidate selection,
benchmark execution against live sandboxes, cutover, release, or deletion.

---

/goal Redraft the State Storage V2 migration package into a genuinely
**phase-based implementation plan** that a succession of implementation agents
can execute and hand off safely.

The current plan calls three very broad permission/risk envelopes “phases” and
places 11 causal gates inside them. That is useful for authority control but is
not sufficiently useful as an implementation-phase plan: one current phase
contains architecture/method selection, canonical format work, storage-core
implementation, permanent integration, migration preparation, and complete
qualification. Do not defend that decomposition merely because it is already
written.

Derive the implementation phases from work, dependencies, artifacts, feedback
latency, rollback boundaries, and reviewable size. Preserve authorization and
risk separation as a distinct overlay. Do not assume that the answer is three,
ten, eleven, or any other preferred number. Compare credible decompositions,
select the smallest decomposition that remains practically executable, and
justify every phase and every ordering edge.

## 1. Scope and workspaces

The only package you may redraft is:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/new_2.0_migration_implementation_plan
```

Use these locations read-only when the plan needs source or historical
evidence:

```text
reserved implementation worktree
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
  expected branch: codex/new-2.0-storage-core
  recorded base: e4974d1f9aac702b35e052629cb070c897989352

current product repository
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox

historical design and Stage 4.6 evidence
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration
```

Verify actual branch, HEAD, tree, upstream relationship, and dirty state before
relying on these recorded values. The intended implementation base is the
reserved worktree created from current `main`; the existing upgrade-migration
2.0 work and Stage 4.6 POC are references and possible baselines, not the code
base to extend. If `origin/main` has advanced beyond the reserved base, report
`BASE_DRIFT` and the exact commits. Do not merge, rebase, switch, reset, clean,
stage, commit, push, or alter either product worktree as part of this redraft.
Do not silently rewrite the recorded base.

The docs repository already contains unrelated owner changes and this package
may be untracked. Preserve all unrelated changes. Use `apply_patch` for manual
edits. Read and obey every applicable `AGENTS.md` and `CLAUDE.md` before acting.

## 2. Required conceptual correction

Use four different terms consistently:

1. **Implementation phase** — a bounded, coherent, independently reviewable
   body of work that ends in usable exact artifacts and a clear handoff.
2. **Acceptance gate** — a content-addressed predicate that decides whether
   exact phase output is allowed to feed later work.
3. **Authorization epoch** — a permission/risk ceiling controlling who may
   seal the judge, create only non-live artifacts, or mutate live truth.
4. **Artifact packet** — the exact specification, decisions, experiments,
   algorithms, benchmarks, verification, manifest, acceptance, and handoff
   evidence for one phase or gate.

Do not call an authorization epoch a phase. Do not make every gate a phase by
renaming it. Some gates may terminate one implementation phase; other gates
may be checks inside a phase. The redraft must expose both mappings explicitly.

The current three permission/risk envelopes may survive as authorization
epochs if they remain justified:

```text
Epoch A: candidate-blind judge/evidence preparation and sealing
Epoch B: reversible non-live selection, implementation, and qualification
Epoch C: separately authorized live mutation, observation, retirement, and release
```

They are not automatically the implementation-phase count. Preserve these two
safety boundaries unless a rigorously evidenced challenger replaces them:

- candidate authors must not tune or rewrite the judge that evaluates them;
- non-live implementation authority must not preauthorize irreversible live
  cutover before the exact qualifying artifact exists.

## 3. What makes an acceptable implementation phase

Every selected phase must satisfy all of the following or state a concrete,
reviewable exception:

- one dominant outcome and one coherent reason to change;
- a bounded owner/collaborator set and an explicit authorization epoch;
- exact predecessor artifacts it consumes;
- exact artifacts it produces for the next phase;
- an implementation surface that can be reviewed without understanding an
  unrelated future subsystem;
- early executable feedback rather than deferring all integration failures to
  the end;
- explicit non-goals and forbidden actions;
- clear failure, rollback, invalidation, and stop behavior;
- a realistic effort estimate and a bounded agent handoff;
- tests, proofs, benchmarks, and acceptance criteria proportionate to its risk;
- no premature product method, architecture, component, API, or field choice;
  and
- no phase whose only purpose is ceremonial promotion or duplicating evidence.

A phase is too large when it combines independently failing implementation
surfaces, cannot produce a meaningful intermediate artifact, has unrelated
owners/reasons to change, requires multiple major design choices before useful
feedback, or cannot be handed to one primary implementation owner with a
bounded review cycle. A phase is too small when it merely renames a document,
hash, approval, test command, or substep and produces no independently useful
artifact.

Do not equate “one phase” with “one Codex turn.” For each phase, estimate:

- specification/research effort;
- production implementation effort;
- test/model/benchmark effort;
- hostile-review effort;
- expected files/packages or responsibility regions touched, while keeping
  exact counts `OPEN` until the joint architecture result exists;
- safe parallel lanes and their merge point; and
- whether one normal Codex task is plausible or whether the phase requires a
  coordinated sequence of tasks.

Use qualitative ranges with explicit assumptions if trustworthy numerical
estimates are unavailable. Do not invent lines-of-code or duration precision.

## 4. Derive the phase count; do not guess it

Construct and compare at least three complete decompositions:

1. the current coarse three-phase incumbent;
2. a medium-grained implementation decomposition; and
3. a finer decomposition that closely follows independently testable
   artifacts or the current 11-gate chain.

You may construct additional challengers. Score them against at least:

- causal correctness and inability to run work before its inputs exist;
- architecture and algorithm decision timing;
- feedback latency;
- phase size and handoff clarity;
- storage-core isolation and testability;
- runtime neutrality;
- migration/cutover risk isolation;
- exact-artifact qualification;
- invalidation blast radius;
- safe parallelism;
- documentation/staleness cost; and
- ceremony or fragmentation cost.

Select one decomposition only after the comparison. The selected count must be
a consequence of the boundaries, not a target. Report explicitly:

```text
selected implementation-phase count = N
authorization-epoch count            = M
acceptance-gate count                 = G
```

Do not claim `N` is a global mathematical minimum. State what challenger would
falsify it and what evidence could cause a later split or merge.

At minimum, test whether the work below deserves independent phases. This is a
work inventory, not a mandated decomposition or order:

- source/baseline inventory, matched incumbent, independent oracle, holdout,
  resource model, and benchmark/judge seal;
- joint architecture-topology × physical-method tournament, including a
  zero-addition challenger and `NO_WINNER`;
- canonical state grammar, collision-safe identity, decoder limits, golden
  vectors, and API semantic decisions;
- immutable selected-state storage core and zero-copy root/checkpoint/fork
  operations;
- workspace/session integration and selected-state/application coordination;
- current Linux runtime-effect integration through runtime-neutral contracts;
- future WASI and Firecracker conformance seams and spikes, without pretending
  those runtimes have already qualified;
- importer, dual-read/shadow comparison if selected, fencing, recovery, and
  exact migration rehearsal;
- exact pre-cutover artifact construction and complete non-live qualification;
- separately authorized fleet cutover and the irreversible transition;
- bounded observation and incident/rollback behavior;
- compatibility retirement, changed release build, requalification, fleet
  rebind, old-process drain, and release; and
- separately authorized destructive legacy-byte deletion, if ever performed.

For every selected edge `Phase n -> Phase n+1`, provide:

- the exact output from `n` consumed by `n+1`;
- the invariant that would be unproved if `n+1` ran first;
- a concrete failure or rework mode caused by reordering;
- whether any subset may run in parallel;
- what change invalidates the edge; and
- why the edge is a phase boundary rather than merely an internal gate.

Use a dependency DAG where causality permits parallel work. Do not force a
linear chain for presentation convenience, but identify the single canonical
join/handoff point after parallel lanes.

## 5. Progressive specification, not stale preplanning

Predefine stable contracts for every phase, but do not fabricate detailed
future implementation choices before their predecessors select them.

For all phases, freeze only:

- objective and non-goals;
- required inputs and output artifact types;
- authority epoch;
- decision questions and selection/stop rules;
- invariant and qualification families;
- invalidation owner;
- entry/exit/handoff contract; and
- what future details remain intentionally `OPEN`.

Fully instantiate only the current preparation packet and the next executable
phase packet authorized by accepted predecessors. A future phase must remain a
template/skeleton where its concrete files, packages, algorithms, topology, or
benchmarks depend on an earlier result. Use explicit tokens such as
`OPEN_PENDING_<ARTIFACT>` rather than plausible-looking invented details.

Later phase specifications must consume the exact accepted manifest and
acceptance digests from earlier phases. If an upstream decision changes, the
owning phase and every transitive consumer are invalidated; do not silently
edit an accepted packet in place.

## 6. Required phase document contract

Create a reusable phase template and one numbered Markdown file for every
selected implementation phase. Avoid a proliferation of loosely synchronized
notes. Prefer the existing simplified three-file persistent packet model when
it can carry the required semantics:

```text
packet.md       integrated phase specification and result sections
manifest.json   exact controlled artifact/evidence identity
acceptance.json independent acceptance of one exact manifest
```

Within `packet.md`, preserve exact, machine-detectable sections for:

- phase specification;
- decisions and unresolved questions;
- architecture/component consequences;
- algorithm candidates and any selected/produced algorithm;
- experiments;
- benchmarks and performance evidence;
- implementation notes;
- verification and adversarial tests;
- resource/memory/storage accounting;
- invalidation and rollback;
- outputs and next-phase handoff; and
- evidence custody/provenance.

Do not create separate persistent `spec.md`, `algorithm_note.md`,
`experiment_note.md`, `benchmark_note.md`, `decision_note.md`, and
`handoff_note.md` files unless the redraft proves that independent writers,
lifecycles, access control, or invalidation boundaries require them. Logical
sections are not software components or services.

Every phase file or packet must state at its top:

```text
phase number and stable ID
primary category: PREPARATION | SELECTION | IMPLEMENTATION | INTEGRATION |
                  VERIFICATION | ROLLOUT | CLEANUP
secondary categories, if any
authorization epoch
status
entry artifacts and hashes
produced artifacts
architecture winner count
physical-method winner count
new algorithms selected or produced in this phase
allowed product mutation
forbidden actions
```

Every phase must then contain:

1. objective and why this is a separate phase;
2. prerequisites and exact consumed artifacts;
3. scope, non-goals, and open decisions;
4. responsibilities/components affected, without turning role names or
   diagram boxes into component counts;
5. candidate algorithms/methods and selection status;
6. ordered implementation work;
7. tests, model checking, differential/property/fuzz coverage, and fault cuts;
8. time, I/O, memory, persistent-space, concurrency, and cleanup budgets;
9. benchmark cells and comparability requirements;
10. outputs and content-addressed evidence;
11. exit gate and independent acceptor;
12. rollback, reopening, and transitive invalidation;
13. allowed parallel lanes;
14. effort/size estimate with assumptions; and
15. exact handoff to later phases.

## 7. Non-negotiable architecture and storage constraints

The redraft must not select an architecture merely to make the phase table
look concrete. Joint architecture × physical-method selection remains a real
early decision because physical methods can change ownership, package, helper,
unsafe, recovery, and resource graphs. A method may not be projected onto a
topology selected independently beforehand. The tournament must admit
`NO_WINNER`.

Keep exact component, responsibility, call-edge, package, process, deployable,
trait, API, field, and algorithm counts `OPEN` until measured from the selected
compile-valid graph. The zero-addition R0 topology is a challenger, not a
winner or lower-bound theorem. Every component or abstraction must have one
reason to change and a named failing execution that prevents deletion or
fusion.

The storage layer is the core. Its canonical identity and immutable storage
semantics must not depend on OCI, Docker, OverlayFS, a mount path, a native
handle, a VM snapshot ID, or any runtime brand. OCI/Linux, WASI, and
Firecracker are runtime-effect adapters/conformance targets around the core,
not the core data model. Do not add a speculative generic plugin framework or
one facade per future runtime. Introduce a seam only where a currently named
semantic variation and executable conformance test require it.

Preserve the exact immutable-base zero-copy COW law. For any number of roots
naming one accepted immutable `StateId`, the accepted physical dependency
closure exists once. A no-alias checkpoint, reference-only fork, rollback to an
existing state, winner/root transfer, same-state publication, or ownership
transfer must perform:

```text
selected-state immutable payload bytes read    = 0
selected-state immutable payload bytes written = 0
selected-state immutable payload bytes copied  = 0
new root-private physical closure bytes         = 0
```

Only bounded root/provenance/control metadata may change. Divergent mutable
workspace data and newly published immutable content are charged separately.
Do not describe COW as “approximately one copy” or use ordinary copying as an
implementation fallback for these reference operations.

The phase plan must make ownership, hard bounds, and deterministic cleanup
explicit for every cache, buffer, pin, reader, cursor, mapping, queue, worker,
task, descriptor, scratch file, temporary object, outcome, request, and
rollout. Inactive roots retain no mutable runtime allocation. Cover success,
error, timeout, cancellation, conflict, crash, restart, recovery, rejection,
prune, deletion, and last-root races. Memory safety is an enforced resource and
lifecycle property, not a Rust slogan.

Fork/MCTS/parallel rollout begins from an immutable checkpoint/`StateId` and
shares its immutable closure once. Storage owns checkpoint/root/fork/OCC and
resource-lifecycle semantics only. Search policy, expansion, scheduling,
scoring, backpropagation, and pruning policy remain outside storage.

Preserve the public `file_{verb}` naming. `file_read` without a workspace
session ID captures one committed revision and reads its immutable view;
`file_read` with a valid `workspace_session_id` authorizes and reads that exact
live workspace-session generation through its runtime-effect owner. Writes and
edits require a live workspace and never mutate committed immutable state.

## 8. Correctness, algorithm, and performance discipline

At redraft start and completion, report these counts separately:

```text
algorithm families inventoried
tournament candidate families
algorithms mandated by the plan
algorithms proved
algorithms selected
new algorithms produced
architecture/topology winners
physical-method winners
```

An inventory family, state transition, result type, or test technique is not a
new algorithm. Do not turn the historical 21-family audit census or eight
tournament families into a produced-algorithm count. Until selection runs, the
expected selected/produced count remains zero.

Do not promise that V2 is faster than Stage 4.6, 100x faster, or guaranteed to
dominate any baseline before comparable exact-artifact evidence exists. The
retained Stage 4.6 P4 evidence currently lacks a complete reconstructible
source/build/executable closure, so retain `R_stage46 = INCOMPARABLE` unless
new evidence actually closes it. Do not combine the separate P1 memory receipt
with P4 timing.

Phase 0 or its redrafted equivalent must freeze one candidate-independent
numeric/statistical performance contract before candidate results. It must
bind exact operations, semantics, artifacts, hosts, filesystems, durability,
corpora, cache states, concurrency, setup boundaries, statistics, confidence,
resource ceilings, retry/stopping rules, and rejection behavior. Small
publication is a red-alert falsifier because the historical evidence shows it
regressed; aggregate speedups may not hide it. A candidate that fails a hard
correctness, crash, resource, containment, or per-cell performance conjunct
cannot win through a geometric mean.

For every eventual algorithm or physical method require:

- complete inputs, outputs, preconditions, and postconditions;
- linearization/commit points;
- preserved invariants;
- concurrency, cancellation, retry, exhaustion, and fairness behavior;
- every persisted crash cut and recovery owner;
- worst-case or explicitly qualified amortized/expected time, I/O, memory,
  persistent-space, synchronization, and cleanup bounds;
- model/property/differential/fuzz tests against an independent oracle; and
- mechanically reproducible counterexamples for rejected candidates.

## 9. Migration and release safety

Keep non-live construction and qualification separate from live mutation. The
exact artifact qualified before cutover must be the exact artifact activated.
Define the one-way transition and fleet barrier without preselecting a
controller, database, RPC mechanism, or runtime brand.

After irreversible V2 activation, recovery may roll forward or restore V2; it
must not silently reopen writable legacy state. Bounded observation must
precede compatibility retirement. Retirement changes bytes, so the changed
release artifact requires total gate disposition, exact-artifact
requalification, a new release epoch, complete fleet rebind, old-process
drain, and live attestation before release.

Destructive deletion of legacy stored bytes is not an ordinary implementation
phase and is never implicit in release. Model it as an optional, separately
signed post-release action with its own target, evidence, dry run, recovery
story, and owner authorization.

## 10. Required files and consistency edits

At minimum, produce or update:

- `phases/README.md` — selected implementation-phase index, categories,
  status, effort, epoch, entry/exit artifacts, and gate mapping;
- one numbered file in `phases/` for every selected implementation phase;
- `phases/phase-isolation-and-ordering.md` — dependency DAG, every edge proof,
  safe parallelism, reopening, and decomposition comparison;
- `README.md` — concise plan summary and three separate counts for phases,
  epochs, and gates;
- `HANDOFF.md` — exact current authorization, next allowed work, read order,
  and next-agent action;
- `traceability.md` and `traceability/source-disposition.md` — source and
  requirement coverage;
- the execution artifact contract, templates, schemas, catalog, state, active
  preparation packet, and validator where the selected phase model changes
  their semantics;
- the hostile-review prompt so it contests the newly selected decomposition;
  and
- `evidence/review-record.md` and `evidence/draft-manifest.md` only after the
  redraft is internally consistent and validation succeeds.

Remove or archive obsolete numbered phase files so two incompatible phase
taxonomies cannot both appear authoritative. Do not preserve stale “three
phases,” “five phases,” “ten phases,” phase IDs, paths, transition rules, schema
enums, packet paths, or counts in prose, JSON, examples, validator assertions,
or review instructions. Use repository-wide searches to prove consistency.

Provide an explicit old-to-new disposition table covering every current phase
and all 11 current gates:

```text
old item | new phase/gate/epoch | retained/split/merged/removed | justification
```

Nothing may disappear merely because it no longer has a top-level file. Also
provide a deletion/simplification ledger:

```text
removed | simplified | improved | unchanged | intentionally open
```

Count files and persistent packet artifacts before and after. Prefer fewer
authoritative documents and generated projections over duplicated hand-edited
tables.

## 11. Known unresolved validator issue that must not be hidden

The phase redraft is not permission to declare the package sealed while an
unrelated lifecycle/security defect remains open. Independently verify the
authority-verifier runner's one-process claim.

Linux `RLIMIT_NPROC=1` is not enforced for initial real UID 0 or callers with
applicable `CAP_SYS_ADMIN`/`CAP_SYS_RESOURCE`. The current repair rejects
obviously privileged/root dispatch and terminates/reaps the verifier process
group on normal and exceptional parent paths. Do not assume that checking only
namespace-visible UIDs and `/proc/self/status` capability masks proves the
kernel's real-UID exception cannot apply through nested user namespaces or
credential mappings. Inspect the exact kernel semantics, construct real Linux
reproductions where possible, and either:

- prove the fail-closed eligibility predicate and cleanup contract completely;
- strengthen it with the smallest runtime-neutral mechanism; or
- weaken the claimed threat model honestly and mark protected validation
  `BLOCKED` where the required containment authority is unavailable.

Do not import Docker/OCI daemon dependence into the storage/core plan to solve
this local validator problem. V1 intentionally supports a bounded process tree
using an externally managed PIDs cgroup and process supervision; it did not
prove one process with `RLIMIT_NPROC`. If the new runner needs a kernel PIDs
boundary, model it as an explicit Linux containment requirement/adapter and
justify its authority, lifecycle, cleanup, WASI/Firecracker mapping, and
failure behavior rather than smuggling it into a generic phase.

## 12. Work protocol and drift control

Start with a written plan and keep exactly one step `in_progress`. Before
editing, inventory all regular package files and read every authoritative file
from byte 1 to EOF, including Markdown, JSON, schemas, packet instances, and
`execution/validate.py`. Read historical material only as evidence; do not copy
its conclusions.

Maintain these invariants throughout the redraft:

- product worktrees remain read-only and unchanged;
- no architecture, physical method, algorithm, component count, performance
  result, or phase count becomes accepted by being written in a draft;
- only one phase taxonomy is authoritative at completion;
- every moved requirement appears in the old-to-new disposition table;
- all current open states remain open unless this task actually produces the
  missing evidence;
- package changes are inspected after every substantial edit group;
- unrelated owner changes are preserved; and
- no manifest or seal is refreshed silently.

After your own detailed review and fixes, freeze an exact candidate digest and
launch fresh hostile subagents **from the start**, with isolated context. At
minimum use three independent reviewers:

1. **Phase/dependency hostile reviewer** — tries to split, merge, reorder, or
   delete every selected phase; checks bounded effort, handoff quality,
   progressive specification, and every ordering edge.
2. **Architecture/storage hostile reviewer** — tries to delete components and
   abstractions; checks SOLID/SRP, storage-core isolation, exact zero-copy COW,
   OCI/WASI/Firecracker neutrality, API ownership, and migration boundaries.
3. **Algorithm/performance/lifecycle hostile reviewer** — attacks algorithm
   correctness, time/I/O/memory/persistent-space bounds, cache cleanup,
   checkpoint-rooted fan-out, small publication, benchmark comparability,
   validator privilege/process cleanup, and crash/recovery behavior.

Each reviewer must read the complete frozen corpus, record opening and closing
digests, make no edits, treat all desired conclusions as hypotheses, and
return findings ranked `P0`, `P1`, or `P2` with exact evidence. Fix every P0/P1,
reseal, and repeat a fresh hostile round until the exact reviewed candidate has
no P0/P1. Do not reuse a favorable verdict from different bytes.

## 13. Validation and completion conditions

At minimum, run from the package root:

```bash
python3 -B execution/validate.py

awk '/^```text$/{inside=1;next} inside && /^```$/{exit} inside{print}' \
  evidence/draft-manifest.md | shasum -a 256 -c -

find . -type f \
  ! -path './evidence/draft-manifest.md' \
  ! -path './evidence/review-record.md' -print0 | \
  LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256

find . -type f -print0 | \
  LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256
```

Also verify:

- manifest coverage equals the complete regular-file inventory except the
  manifest itself;
- no symlinks, special files, `__pycache__`, or generated junk entered the
  package;
- every JSON instance validates against its schema;
- all Markdown links and referenced phase paths resolve;
- the phase count, IDs, names, categories, epochs, gate mappings, and states
  agree across every authoritative and executable artifact;
- no future phase packet is instantiated before its exact predecessor and
  separate authorization;
- the product implementation worktree remains clean and unchanged; and
- the final hostile verdicts apply to the exact final substantive digest.

The redraft is complete only when all of the following are true:

1. implementation phases are practical execution units, not renamed
   permission envelopes;
2. the selected count is comparison-derived and every phase/edge is justified;
3. authorization epochs and acceptance gates remain explicit and separate;
4. every phase has an artifact, verification, effort, invalidation, and handoff
   contract;
5. later details remain honestly parameterized by earlier selections;
6. no architecture or method is prematurely selected;
7. the full package has one consistent taxonomy and passes validation;
8. exact manifest and aggregate digests are recorded;
9. the final exact bytes have no hostile-review P0/P1; and
10. no product code or live state changed.

## 14. Required final response

Lead with the result. Report:

- selected implementation-phase count, authorization-epoch count, and gate
  count;
- one compact table of phase number, name, category, dominant deliverable,
  effort band, epoch, and exit gate;
- why the selected decomposition beat the coarse and fine challengers;
- what was removed, simplified, improved, retained, and left open;
- current component/architecture/method/algorithm counts without conflating
  inventories with selections;
- exact files created, changed, removed, or intentionally deferred;
- validator, manifest, digest, Git/worktree, and hostile-review results;
- every remaining P2/open/blocker and the exact next allowed action; and
- an explicit statement that the redraft changed documentation only and did
  not execute any phase or select an architecture/method.

Use clickable absolute paths. Do not call the plan complete merely because the
documents are long or internally confident.

