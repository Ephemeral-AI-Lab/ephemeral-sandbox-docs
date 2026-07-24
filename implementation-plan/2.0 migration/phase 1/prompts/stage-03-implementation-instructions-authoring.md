# Stage 03 implementation-instructions authoring prompt

## Mission

Create a complete, implementation-ready instruction document for Stage 03,
“corrected identity and complete private publication.”

Write the resulting document to:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_03_incremental_publication/implementation_instructions.md`

This is a documentation and planning task only. Do not implement Stage 03 product
code, change the Stage 03 specification, change the E2E contract, run live E2E or
benchmark campaigns, or claim that any Stage 03 result passed. Inspect the product,
test, benchmark, and documentation repositories read-only so the instructions name
real integration seams, files, commands, evidence artifacts, and ownership boundaries.

The output must guide a future implementation agent from repository preflight through
implementation, focused verification, the three-minute Stage 03 benchmark E2E
campaign, completion tracking, and final handoff.

## Non-negotiable working method

1. Read every required document below completely, from the first line through EOF.
   Do not rely on headings, snippets, search matches, prior summaries, or the contents
   of this prompt as a substitute.
2. Inspect the current worktrees and repository-local instructions before proposing
   files or commands. Treat the working trees as shared custody. Do not reset, stash,
   clean, switch branches, discard, overwrite, or “restore” existing changes.
3. Reconcile the specification, E2E plan, benchmark note, storage contract,
   Preparation 04 gates, Stage 02 handoff, and actual code/test seams. Do not silently
   resolve a contradiction by weakening a normative requirement.
4. Keep facts, proposed work, measured evidence, and deferred qualification strictly
   separate. A planned test is not evidence. A source inspection is not a benchmark.
5. Create or edit only the requested
   `stage_03_incremental_publication/implementation_instructions.md` document. If a
   source document is inconsistent, record the inconsistency and its blocking owner
   decision in the instruction document instead of rewriting the source.

## Authority order

Use this precedence and state it explicitly in the output:

1. recorded owner decisions, including any Stage 03 v3 amendment approved after this
   prompt was written;
2. the Phase 1 implementation index and minimal storage contract;
3. the Stage 03 specification;
4. the Stage 03 E2E plan;
5. Preparation 04 quantitative acceptance criteria;
6. the Stage 03 benchmark note;
7. the completed Stage 02 handoff and inherited evidence;
8. current repository-local instructions and actual implementation/test seams;
9. the new implementation-instructions document.

The instruction document is an execution guide, not a new authority. If it conflicts
with a higher source, the future implementation agent must stop and reconcile it.

## Required reading before writing

Read these files completely:

### Stage 03 sources

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_03_incremental_publication/spec.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_03_incremental_publication/e2e_test.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_03_incremental_publication/benchmark_note.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_03_incremental_publication/handoff_from_stage_02.md`

### Phase 1 authority and quantitative gates

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/index.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/layerstack_storage_contract.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prep/03-seqcdc-cas-and-squash-decision.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md`

Follow every direct normative link from those files that is necessary to understand a
field, threshold, lifecycle, algorithm, fixture, or unresolved owner decision. Read
each selected linked source completely.

### Stage 02 contract and handoff

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_02_portable_root_contract/spec.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_02_portable_root_contract/e2e_test.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_02_portable_root_contract/implementation_instructions.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_02_portable_root_contract/contract_v2_owner_decision_d2_5.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_02_portable_root_contract/handoff_to_stage_03.md`

Do not treat approved decision `PRC-STAGE02-OWNER-DECISION-D2.5` as approval of
`RootRecordV3`, bounded Merkle pages, or the Stage 03 identity amendment. The recorded
Stage 02 handoff says Stage 03 remains blocked until a separate owner decision freezes
the v3 wire contract and benchmark corpus. Inspect the live documentation for a newer
approval. If none exists, make that the first hard blocker and prohibit v3 golden or
product implementation work.

### Repository-local instructions and current code

Read all applicable `AGENTS.md`, `CLAUDE.md`, maintainer, test-report, and benchmark
instructions by directory ancestry in:

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs`

Inspect, without editing:

- the Stage 02 `layerstack-core` values/codecs/tests and LayerStack adapters;
- current v1 publication, workspace-upper capture, whiteout, fsync, lock, and recovery
  seams;
- current observability/resource counters and public workspace/file APIs;
- E2E catalog, typed declarations, fixtures, helpers, artifact schemas, and append-only
  test report;
- benchmark planner, runner, operation catalog, strict fixtures, presets, verifier,
  recovery, and artifact compatibility tests;
- the exact dependency comparator and frozen baselines.

The output must name real paths found during inspection. Do not invent a module,
command, E2E runner option, benchmark plan, metric, or artifact schema because it
would be convenient.

## Required source reconciliation

Begin the document with a source-status and reconciliation section containing:

- a reading ledger listing every required source, its live status, the relevant
  authority it contributes, and confirmation that it was read through EOF;
- the current v3 owner-decision status;
- the current branch, `HEAD`, upstream, and complete worktree custody of the product,
  test/E2E, benchmark, and documentation repositories;
- inherited Stage 00–02 stable evidence and exact artifacts that can be reused;
- contradictions, stale paths, or stale status statements found across Stage 03
  sources;
- a resolution or explicit owner blocker for every contradiction.

Do not copy stale handoff revisions as if they were the current state. Show both the
recorded handoff state and the live state when they differ.

## Required structure of `implementation_instructions.md`

Use the Stage 02 implementation-instructions document as a structural quality
baseline, but specialize it for the much larger Stage 03 vertical slice. Include at
least the following sections.

### 1. Status, purpose, and exact outcome

State that the document is instructional and that all Stage 03 code, E2E, benchmark,
and completion results remain `NOT_RUN` unless an existing retained artifact proves
otherwise.

Define the complete vertical slice:

- owner-approved v3 bounded Merkle identity with immutable v2 read/import
  compatibility;
- deterministic streaming SeqCDC and typed loose-object put-if-absent;
- bounded changed-path capture, ordering, persistent-page mutation, and structural
  sharing;
- atomic private heads, refs, checkpoints, pins, and leases;
- branch-scoped `PublicationId`, durable operation recovery, exact retry outcomes, and
  crash-gap repair;
- changed-path OCC conflicts and bounded disjoint rebase;
- checkpoint, branch/MCTS fork, checkout, revert, and reset semantics;
- v1 carrier source protection where imported bytes remain in v1;
- optional hidden validation using the same normal publication protocol;
- unchanged public v1 read/write/publication authority.

### 2. Entry gates and hard blockers

Turn every Stage 03 entry condition into a yes/no gate with required evidence. Owner
approval of the complete v3 schema and frozen corpus is a hard gate. Also include
custody, inherited Stage 02 evidence, dependency baseline, environment, available
disk, and benchmark-harness readiness.

No work that freezes v3 goldens or persists v3 state may proceed while the owner gate
is open. Safe read-only inspection and preparation of the instruction document may
continue.

### 3. Scope and non-goals

Separate Stage 03 work from Stages 04–07. Explicitly forbid Stage 03 from creating or
implementing:

- packs except an existing-v1 physical locator when genuinely required;
- native materializations;
- GC authority or `gc/CURRENT`;
- candidate public authority, migration retirement, or public route selection;
- `refs/legacy`, a new `legacy/` directory, shadow-specific roots/receipts/journals,
  full-tree identity manifests, reserved future directories, or empty schema
  scaffolding;
- a new external dependency, system helper, target-image helper, service, network
  dependency, unsafe portable-core path, or alternate E2E/benchmark harness.

### 4. Complete `/eos` structure and ownership map

Reproduce the complete migration-time `/eos` tree from the normative storage contract,
then annotate it for Stage 03. Do not show only the new candidate subtree.

Provide a path-by-path table with:

- exact path or pattern;
- owner;
- pre-existing versus Stage 03-created status;
- creation condition;
- record/object purpose;
- atomic durability protocol;
- recovery owner;
- deletion/retention rule;
- bound and physical-space category;
- workload/public visibility;
- E2E evidence that proves the rule.

At minimum, distinguish:

- existing v1 `manifest.json`, `workspace.json`, `base`, `layers`, `staging`, and
  `.layer-metadata`, which remain in place and authoritative;
- `/eos/workspace/<session>/upper`, the only admitted changed-payload source;
- WorkspaceManager `work`, `executions`, `.export`, and manager state, which
  LayerStack must not ingest or delete;
- `/eos/storage` and `/eos/runtime`, which LayerStack must not scan or collect;
- Stage 03 `.storage-writer.lock`, `CONTROL`, `objects/loose`, conditionally required
  locator files, `refs/{heads,checkpoints,pins,leases}`, and
  `operations/<id>/{STATE,work}`;
- future `objects/packs`, `materializations`, and `gc`, which must remain absent;
- the absence of durable `/eos/legacy`, `refs/legacy`, and new
  `/eos/namespace_execution`.

Directories are created only on first real use. A pattern in the canonical tree does
not authorize an empty directory.

Add explicit `/eos` assertions for setup, active publication, post-commit, restart,
failure recovery, ref deletion, session teardown, and settled/quiescent boundaries.
Workloads must continue to see `/eos` masked.

### 5. Architecture, types, and dependency boundaries

Describe SRP ownership and dependency direction for:

- v3 portable canonical values/codecs and typed IDs;
- LayerStack SHA-256 and persistence adapters;
- SeqCDC streaming reader and typed chunk sink;
- changed-path external ordering/spool;
- loose-object store and typed verification;
- persistent tree/file/segment page mutation and flat diagnostic export;
- atomic refs and the short writer-lock commit seam;
- publication operation state machine and recovery;
- conflict-key extraction/OCC/rebase;
- source locators/leases;
- optional hidden validation;
- observability, benchmark instrumentation, and test-only failpoints.

Include a closed type/record/field table based only on an approved owner decision.
Show identity-bearing versus excluded fields, maximum encoded sizes, validation
errors, atomic record fields, and ownership. If approval is absent, describe the
required decision shape without inventing numeric tags, digest domains, wire bytes, or
goldens.

Keep the portable core safe Rust and independent of filesystem, Docker, OverlayFS,
mount, runtime, async, serde, SHA implementation, host path, and materialization
types, consistent with the approved dependency boundary.

### 6. File-by-file implementation map

After inspecting the repositories, provide separate Product, test/E2E, benchmark,
documentation, fixture, and artifact-schema tables. For every path include:

- add/modify/avoid;
- exact responsibility;
- preserved inherited behavior;
- custody/dirty-file note;
- smallest focused verification;
- rollback boundary.

Do not use placeholder filenames where an existing integration seam can be identified.
Where a new filename is genuinely proposed, label it `proposed` and explain why the
existing structure has no suitable owner.

### 7. Ordered implementation sequence

Use a dependency-aware sequence that starts only after the owner gate:

1. freeze and test v3 codecs and hostile decoder bounds;
2. implement deterministic loose-object put-if-absent and typed verification;
3. implement bounded changed-path capture/order and SeqCDC installation;
4. implement persistent-page mutation, sharing, and derived flat export;
5. implement atomic refs and GC-barrier hook points without adding GC;
6. implement publication operation recovery and lost-response repair;
7. implement OCC conflict keys and bounded disjoint rebase;
8. implement checkpoints, forks, checkout, revert, and reset;
9. add v1 locator/source holds only if import needs them;
10. add optional hidden validation using the normal protocol;
11. add observability, failpoints, E2E declarations, benchmark operations, verifiers,
    and documentation closure.

For each step include files, introduced behavior, invariants preserved, focused tests,
failure cleanup, rollback boundary, prerequisites, and a “proceed only when” gate.
Make expensive capture, hashing, sorting, page construction, and comparison occur
outside the brief writer-lock section.

### 8. Progress tracker

Add one canonical progress table to be maintained during implementation. Give every
row a stable Stage 03 work ID. Use a closed status vocabulary:

`BLOCKED`, `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL`, `DEFERRED_STAGE_07`.

Each row must contain:

- work ID and dependency IDs;
- deliverable;
- current status;
- completion condition;
- exact verification command or typed evidence ID;
- run/artifact path and digest;
- owner/blocker;
- cleanup result;
- last-updated timestamp.

Cover owner approval, custody, every implementation slice, every E2E family, the
three-minute benchmark campaign, dependency proof, `/eos` verification, resource
reclamation, documentation, and final handoff. Initialize statuses from actual
evidence. Do not pre-check future work or use ambiguous percentages.

### 9. Completion checklist

Provide an evidence-backed Markdown checklist. Each item must map to a progress ID and
verification row. It must include:

- entry/custody/owner gates;
- v2 compatibility and approved v3 goldens;
- all publication/ref/OCC/recovery/source-hold behaviors;
- exact `/eos` allowed, conditional, and forbidden paths;
- public-v1 compatibility and `/eos` masking;
- every E2E family in `e2e_test.md`;
- three-minute time/space benchmark evidence;
- bounded memory, queues, tasks, FDs, mappings, retries, and operation residue;
- zero detached tasks/strong cycles and explicit quiescence;
- exact zero dependency/system/helper/service/image delta;
- artifact schema validation and append-only reporting;
- exact run-owned cleanup and retained failed attempts;
- honest deferral of Stage 07-only qualification.

An item may be checked only when the linked command passed and the named artifact
contains all mandatory fields. Missing mandatory data is `BLOCKED` or `FAIL`, never
zero and never an inferred pass.

## E2E and verification design

### Typed E2E catalog

Convert every Stage 03 E2E-plan section into concrete, stable typed cases:

1. v2/v3 identity, codec, hostile decode, and derived-flat-stream cases;
2. publication correctness across all listed file kinds and mutations;
3. ref semantics;
4. two-writer and three-or-more-writer OCC/progress;
5. every publication failpoint and lost-response retry boundary;
6. v1 source safety and validation mode;
7. bounded resources, target-image independence, `/eos` masking, and ownership;
8. exit-evidence completeness.

For each case specify:

- stable ID and title;
- product/API seam;
- preconditions and deterministic fixture digest;
- exact action;
- public behavior oracle;
- allowed outside inspection;
- counters and artifacts;
- time/resource limit;
- cleanup;
- pass/fail rule.

Public workspace/file behavior is the correctness oracle. Private `/eos` inspection is
allowed only for independent layout, allocated-space, permission, durability,
failpoint recovery, and residue evidence. It must not replace public logical-tree
verification.

### Verification traceability matrix

Create a matrix from every Stage 03 spec exit criterion, E2E bullet, benchmark cell,
Preparation 04 Stage 03-applicable gate, and `/eos` invariant to:

- implementation owner/path;
- focused unit/integration test;
- typed E2E ID;
- benchmark operation/cell;
- required artifact field;
- pass threshold;
- completion/progress ID.

No requirement may be represented only by prose or architecture inspection.

### Commands and execution order

Provide exact future commands, based on the live repositories, for:

1. formatting and narrow static checks;
2. v3 core golden/hostile/portability tests;
3. loose-object, tree mutation, refs, operation recovery, OCC, and source-hold tests;
4. safe E2E catalog collection;
5. focused E2E cases feature by feature;
6. benchmark plan validation;
7. the three-minute benchmark E2E campaign;
8. benchmark artifact verification;
9. exact dependency delta comparison;
10. final focused regression and cleanup verification.

Do not run these commands during this authoring task. In the instructions for the
future implementation agent:

- append the exact command, intent, custody, run ID, and cleanup plan to the existing
  test report before execution;
- append/fill `Good`, `Defect`, and `Fix/next action` after execution;
- keep failed attempts and reports append-only;
- rerun only a failed focused case while debugging;
- do not rerun passing cases merely because another case failed;
- use only exact run-owned cleanup and never broad Docker/process cleanup;
- report harness wall time separately from build-lock, image-pull, and unrelated host
  contention;
- run the final required aggregate proof only after focused failures are resolved.

## Three-minute benchmark E2E campaign

The Stage 03 focused benchmark E2E campaign receives a hard aggregate execution
budget of **180 seconds** to obtain better coverage than a tiny diagnostic. This
three-minute campaign is Stage 03 implementation evidence, not the complete Stage 07
release qualification.

The instruction document must define a concrete 180-second plan and the exact runner
clock boundary. Prefer measuring from benchmark-runner campaign start through settled
artifact write and cleanup accounting. Prebuilds, image pulls, and deterministic
fixture generation may be explicit prerequisites only when their time is measured and
reported separately; they may not be silently hidden or charged asymmetrically.
Failed attempts and retries count in the campaign in which they occur.

The 180-second cap does not weaken Preparation 04:

- no individual operation may exceed 60 seconds;
- all correctness gates precede performance claims;
- the normative five-minute candidate/baseline allowance remains an upper bound for
  later matched qualification, not permission to overrun this focused campaign;
- a full Preparation 04 cell that cannot be credibly sampled in 180 seconds remains
  `NOT_RUN` or `DEFERRED_STAGE_07`; it must not be approximated into `PASS`;
- do not compress the full host, architecture, 64/256/1024 MiB × 1/16/64-root RSS,
  three-invocation selection-advantage, or Stage 07 matrix into three minutes.

### Required campaign coverage

Use deterministic pre-generated fixtures and counterbalanced operation order. Design
the most informative campaign that fits 180 seconds and includes, at minimum:

- first import;
- no-op publication;
- repeated 4 KiB middle edits at more than one file/tree scale;
- append, truncate, metadata-only change, delete, and rename;
- clean checkpoint/fork and dirty checkpoint;
- same-path conflict and disjoint two/three-writer progress;
- at least one representative lost-response commit failpoint/restart retry in the
  timed campaign, while the complete failpoint matrix remains a separate correctness
  gate;
- before/peak/settled resource and physical-space samples;
- exact cleanup/quiescence and operation-residue verification.

If all required cells cannot fit, the document must state the deterministic priority
and identify the separately run focused correctness cases. Do not reduce assertions,
omit cleanup, or downsize fixtures below the point where changed-input scaling and
space amplification are observable merely to fit the clock.

Include a budget table whose rows sum to at most 180 seconds. Reserve time for
settling, artifact serialization, and cleanup verification rather than allocating the
whole budget to workload execution.

### Time-performance evidence

For every sampled operation record:

- runner and operation elapsed time;
- warmup count, raw sample count, execution order, p50, p95 when sample count supports
  it, diagnostic p99 when applicable, median absolute deviation, and throughput;
- baseline and candidate values with the exact threshold formula;
- `R,E,U,E_changed,K,P,N,Q`;
- bytes read, hashed, and written;
- object/page read/write counts and bytes;
- unchanged-tree/history scan counters;
- lock-wait time, retry count, conflict count, and disjoint progress ratio;
- cache state, worker limits, host load/context, and variance explanation.

The campaign must test scaling, not just a single elapsed value. Require multiple
problem sizes or repeated tree growth for the 4 KiB edit case and report ratios/slopes
that can expose total-tree or history work. Any nonzero complete-tree/history scan on
a normal incremental publication is a failure.

Do not claim p95 from an inadequately small sample without labeling it diagnostic.
Never report a benchmark pass merely because the implementation is expected to be
incremental.

### Space and resource evidence

Measure allocated physical bytes, not only apparent/logical length. Sample at
pre-operation, peak, post-commit, post-restart where applicable, and settled
quiescence. Attribute bytes to the Stage 03-applicable categories:

- loose logical objects and conditional existing-v1 locator/source holds;
- refs;
- operation `STATE` and work/staging;
- metadata;
- active workspace upper/work, reported separately from retained candidate storage;
- unchanged v1 carriers;
- unreachable/unexplained residue.

Record:

- new unique payload and changed chunk/page bytes;
- shared unchanged payload/pages;
- peak and settled candidate bytes;
- publication staging amplification;
- metadata bytes per chunk, segment, and changed path where applicable;
- process RSS and available cgroup memory;
- storage-owned permits/bytes, worker/task/thread counts, queue depth, open FDs,
  mappings, and lock wait;
- first-to-last settled deltas and quiescence;
- exact operation residue and lease-protected bytes.

For clean checkpoint and clean fork, require exactly zero copied payload and zero
native-tree allocation. For no-op publication, require zero new payload. For
localized edits, calculate the Preparation 04 locality target and report measured new
unique bytes. Missing accounting is a failed artifact, not a zero value.

### Benchmark artifacts and verdict

Require machine-readable raw samples plus a human-readable `benchmark_note.md`
closure. Each result must contain:

- exact command, revision, build, algorithm/profile/format, host/target/image identity,
  `/eos` backing filesystem, seed, corpus/fixture digest, run/pair ID, and sample order;
- every required time, space, memory, task, FD, page/object, lock, retry, and cleanup
  field;
- raw artifact paths and digests;
- threshold, measured value, sample sufficiency, `PASS`/`FAIL`/`NOT_RUN`/
  `DEFERRED_STAGE_07`, and variance or unavailability reason.

The verifier must reject missing mandatory fields and inconsistent totals. It must not
coerce `null`, missing, unsupported, or unavailable data to zero.

## Final completion and handoff format

End the instruction document with:

1. the evidence-backed completion checklist;
2. the canonical progress tracker;
3. a hard-blocker table;
4. checks explicitly deferred to Stage 07;
5. a self-contained final handoff template.

The handoff template must include:

- Stage 03 verdict: `POC PASS`, `POC FAIL / BLOCKED`, or the repository’s established
  equivalent;
- owner decision and v3 format version;
- files changed by repository and pre-existing dirty files preserved;
- focused product results;
- every typed E2E result and run ID;
- three-minute campaign budget/result, sample sufficiency, and raw artifacts;
- time, space, memory, concurrency, failpoint, source-hold, and `/eos` evidence;
- dependency and portability proof;
- exact cleanup/quiescence result and retained failed attempts;
- current Git custody for all repositories;
- skipped, unavailable, `NOT_RUN`, and Stage 07-deferred checks;
- remaining blockers or contradictions.

Do not mark Stage 03 complete because code compiles, because architecture looks
incremental, because one benchmark is favorable, or because a broad suite passes.
Completion requires every mandatory Stage 03 checklist item to have direct retained
evidence and every missing mandatory item to remain visibly open.

## Quality bar for this authoring task

Before finishing the document:

- verify every local link and referenced path;
- verify every proposed command against the current CLI/help or existing test pattern;
- verify progress IDs are unique and every completion item maps to one;
- verify every Stage 03 E2E bullet and benchmark-note cell appears in the traceability
  matrix;
- verify the 180-second budget sums correctly;
- verify the `/eos` table includes the complete ownership tree, the exact Stage 03
  delta, conditional paths, forbidden future paths, and setup/active/restart/settled
  assertions;
- verify no source-inspection statement is mislabeled as executed evidence;
- verify all results remain honestly unchecked or `NOT_RUN` unless backed by an
  existing artifact;
- run only documentation-safe checks such as link/path validation and
  `git diff --check`.

Return a concise summary of the created document, unresolved owner blockers, and the
single output path. Do not implement or execute Stage 03.
