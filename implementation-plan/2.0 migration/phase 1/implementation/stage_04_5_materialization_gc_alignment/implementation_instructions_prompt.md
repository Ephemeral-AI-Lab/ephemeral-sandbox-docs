# Prompt for the Stage 04.5 implementation-instructions author

You are authoring the implementation instruction document for Stage 04.5 of the
EphemeralOS LayerStack 2.0 migration.

## Mission

Create this file:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_5_materialization_gc_alignment/implementation_instructions.md
```

The result must be a self-contained, execution-ready guide for a future
implementation agent. It must translate every Stage 04.5 specification, E2E,
benchmark, `/eos`, handoff, resource, recovery, authority, evidence, and cleanup
requirement into:

- concrete work items against the current repositories;
- an ordered implementation sequence with stop conditions;
- typed E2E cases;
- exact future commands;
- a focused 180-second benchmark E2E campaign;
- a verification traceability matrix;
- a canonical progress tracker; and
- an evidence-backed completion checklist.

This task is documentation-only. Inspect the repositories read-only, then create
or update only `implementation_instructions.md`. Do not implement product or test
code, run live E2E/benchmark campaigns, change the four Stage 04.5 source
documents, or promote any Stage 04.5 result to `PASS`.

## Repositories and authoritative locations

Use these exact roots:

```text
Docs:
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs

Product:
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox

Test and benchmark:
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test

Stage 04.5:
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_5_materialization_gc_alignment
```

Read and obey the product repository's `AGENTS.md`, `CLAUDE.md`, and
`docs/maintainer-architecture.md` before mapping files or commands. In
particular, preserve crate boundaries, keep production code free of test
helpers, use the repository's supported Docker gateway and CLIs for future live
operations, and do not invent an alternate product or E2E harness.

## 1. Read the documents fully before writing

Do not skim, rely on search excerpts, or start drafting after reading only
headings. Read every required document from beginning to end. Record a reading
ledger in the output with the relative path, purpose, line count, and current
SHA-256. If a required document changes while you work, reread it and refresh
the ledger.

Read these Stage 04.5 documents first and especially carefully:

1. `stage_04_5_materialization_gc_alignment/spec.md`
2. `stage_04_5_materialization_gc_alignment/e2e_test.md`
3. `stage_04_5_materialization_gc_alignment/benchmark_note.md`
4. `stage_04_5_materialization_gc_alignment/handoff_from_stage_04.md`

Then read the normative and structural dependencies in full:

1. `implementation/index.md`
2. `implementation/layerstack_storage_contract.md`
3. `prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md`
4. `stage_04_candidate_materialization/spec.md`
5. `stage_04_candidate_materialization/e2e_test.md`
6. `stage_04_candidate_materialization/benchmark_note.md`
7. `stage_04_candidate_materialization/implementation_instructions.md`
8. `stage_04_candidate_materialization/handoff_to_stage_05.md`
9. `stage_05_retention_gc_packs/spec.md`
10. `stage_05_retention_gc_packs/e2e_test.md`
11. `stage_05_retention_gc_packs/benchmark_note.md`
12. `stage_06_candidate_authority/spec.md`

Use the Stage 03 and Stage 04 implementation-instruction documents as rigor and
format precedents, not as authority for Stage 04.5 behavior or evidence. Stage
04's direct artifacts are inherited baselines and custody evidence only. They
do not make a Stage 04.5-specific gate pass.

Use this reconciliation order:

1. Stage 04.5 specification and its explicit authority boundary;
2. Stage 04.5 E2E and benchmark evidence rules;
3. the minimal storage contract and Preparation 04 quantitative gates;
4. the Stage 04/05/06 boundary specifications;
5. the Stage 04 handoff for frozen incoming identities and evidence;
6. prior implementation guides for structure only; and
7. current source code as evidence of the implementation shape, never as a
   reason to weaken a normative requirement.

If two normative requirements genuinely conflict, record the exact passages,
impact, and required owner decision as a blocker. Do not silently choose one.

## 2. Inspect the current implementation and test architecture

Inspect the complete relevant call graph and read every source file you cite in
the file-by-file plan. At minimum, start from:

- `crates/sandbox-runtime/layerstack/src/stack/candidate/`
  `materialization.rs`, `generation.rs`, `materialization_operation.rs`,
  `operation.rs`, `publication.rs`, `refs.rs`, `ref_ops.rs`,
  `native_backend.rs`, and `mod.rs`;
- the LayerStack storage-writer lock, common operation/recovery, resource
  observation, squash, service, and public API paths reached from those files;
- workspace-session admission, persistence, recovery, teardown, mount,
  command, file, and PTY routes;
- existing product tests under
  `crates/sandbox-runtime/layerstack/tests/` and the relevant operation,
  workspace, namespace, and overlay tests;
- `ephemeral-sandbox-test/e2e/runtime/layerstack_phase1/`;
- the LayerStack Phase 1 fixtures, catalog declarations, schemas, helpers, and
  `e2e/test-report.md`;
- `benchmark/backend/benchmark_lab/stage04_materialization.py` and the runner,
  planning, artifact, model, observation, and verifier paths it uses;
- the Stage 04 benchmark preset, goldens, contract tests, integration tests,
  and retained Stage 04 artifact/handoff identities.

Use `rg`/`rg --files` to discover actual paths and symbols. Trace all production
callers of:

- `begin_generation_retirement`;
- `finish_generation_retirement`;
- `remove_generation`;
- materialization-specific authoritative phases;
- generation enumeration/allocation;
- recovery directory collection/sorting;
- lease scans;
- single-flight registries and waiter admission;
- private worker pools/gates;
- `CURRENT` repair/selection; and
- every `unsafe` block or memory mapping reachable from a Stage 04.5 path.

Do not guess filenames, APIs, CLI flags, test filters, or benchmark plan IDs.
Every path and future command in the document must be verified against the
current repositories. Do not invent a `crates/e2e-test` or `e2e-runner` workflow
if it is not present here; extend the existing Docker-backed typed Python E2E
and benchmark architecture.

Capture a read-only authoring snapshot for all three repositories: branch, HEAD,
upstream, staged/unstaged/untracked paths, and relevant retained artifact
digests. Preserve unrelated or concurrent changes.

## 3. Required document structure

The final `implementation_instructions.md` must contain, at minimum, the
following sections.

### A. Status, authority, reading ledger, reconciliation, and custody

- State that Stage 04.5 implementation and direct evidence are initially
  `OPEN`/`NOT_RUN`.
- Record the complete reading ledger and authoring-time custody snapshot.
- Reconcile the handoff's frozen Stage 04 identities with current repository
  identities without rewriting history.
- State plainly that v1 remains public read/write authority.
- State that Stage 04.5 has no logical or physical deletion, GC, unlink,
  retirement, pack/locator, public-authority, or v1-retirement authority.

### B. Exact outcome, entry gates, scope, non-goals, and blockers

Translate the required flow exactly:

```text
bounded private build
-> complete verification and sync
-> typed immutable Ready generation
-> bounded common publication
-> exact old-generation handoff
```

List all entry gates and hard blockers. Preserve Stage 04 strict native
activation, exact leases, immutable generations, per-session isolation, no
silent fallback, and `legacy_v1` authority. Separate Stage 05, Stage 06, and
Stage 07 work explicitly; a deferral must never hide a Stage 04.5 exit gate.

### C. Complete `/eos` structure, ownership, and lifecycle

Reproduce and reconcile the complete migration-time `/eos` tree from the
storage contract, not only the Stage 04.5 subset. Then provide a path-by-path
table with:

- exact path or pattern;
- sole owner and creator/mutator;
- first-use and lifecycle phase;
- durability, atomicity, and recovery owner;
- exact lease/hold/fence;
- deletion authority and preconditions;
- allocated-space accounting bucket;
- Stage 04.5 action: inherited, changed, asserted, excluded, or forbidden; and
- verification IDs.

The Stage 04.5 persisted subset must remain:

```text
/eos/layer-stack/
├── .storage-writer.lock
├── operations/<operation-id>/
│   ├── STATE
│   └── work/
├── materializations/<materialization-id>/
│   ├── CURRENT
│   └── generations/<generation>/
│       ├── MANIFEST
│       └── carriers/<carrier-id>/...
└── refs/leases/<lease-id>
```

Stage 04.5 adds no new top-level directory or atomic pointer. `STATE` is the
only durable operation/recovery record, `CURRENT` is the only selector, and the
manifest is immutable after `Ready`.

Create concrete `/eos` lifecycle IDs such as `S045-L01`, `S045-L02`, etc. Cover
at least: pre-entry inventory, `Building`, `Ready`, initial publication,
replacement with/without Stage 05 handoff, exact old/new readers,
crash/recovery, corruption/ambiguity, cancellation, session teardown,
quiescence, final cleanup, forbidden paths, `/eos` workload masking, and proof
that WorkspaceManager, service-storage, runtime, v1, and unrelated state remain
unchanged.

### D. Architecture, APIs, state machines, locks, owners, and caps

Define the required types and API seams for:

- private builder output;
- typed verified `Ready` subject;
- common four-state lifecycle
  `Building -> Ready -> Published -> Terminal`;
- bounded common publisher;
- deterministic Stage 05 root-admission and exact old-subject handoff hooks;
- exact session generation leases;
- shared storage governor, worker pool, byte/FD/disk admission, operation
  registry, and recovery dispatcher;
- bounded paginated recovery; and
- instrumentation for forbidden writer-lock work, resources, routes, space,
  and quiescence.

Show dependency direction and sequence/state diagrams where they clarify
ownership. Make the lock order explicit:

```text
byte/worker/FD/disk permits
-> optional per-key single-flight ownership
-> storage writer lock
```

No permit wait, join, payload verification, tree/history/lease scan, provider
payload I/O, or other heavy work may occur under the writer lock.

Carry every hard cap from the specification into one ownership ledger,
including:

- `min(B, 64 MiB)` shared storage-owned byte permits;
- four global storage workers;
- four `Building`/`Ready` materialization targets;
- aggregate `sum(T_build) <= W_mat`, where
  `W_mat = min(4 GiB, 10% LayerStack capacity)`;
- 64 nonterminal common operations;
- 16 same-key waiters;
- 16 descriptors / 64 KiB downstream metadata;
- 256 KiB hydration buffer per worker;
- 16 FDs per operation / 64 global;
- zero Stage 04.5 mappings;
- 4,096 typed holds;
- 64 active or pinned generations;
- native depth 64;
- eight retries;
- 256 KiB operation-state/manifest limits; and
- 64 records per recovery page.

For every owner, specify normal, error, cancellation, timeout, panic, restart,
and shutdown cleanup.

### E. File-by-file implementation map

Create stable work IDs using the `S045-` prefix. Include separate tables for:

1. product code and product tests;
2. E2E, fixtures, catalog, schema, and helpers;
3. benchmark plan, runner integration, artifacts, verifier, and negative tests;
4. documentation, reporting, cleanup, and handoff.

Each row must contain: work ID, exact current path, add/change/remove action,
precise deliverable, dependency, relevant requirement IDs, verification IDs,
and stop condition. If a new path is truly required, label it `ADD`; otherwise
name the existing path to modify. Do not use `...` as the only file
identification in the canonical tracker.

The plan must explicitly remove or make structurally unreachable all Stage 04
generation-deletion/retirement entry points, collapse the duplicate
materialization state machine into the common lifecycle, move work into shared
bounded ownership, paginate before allocation, and prevent directory-derived
selection or allocation.

### F. Ordered implementation sequence and stop conditions

Order the work feature by feature. A good sequence begins with custody and
static inventories, then types/lifecycle, deletion removal, shared governor,
private build/common publication split, Stage 05 hooks, bounded recovery,
reader/session preservation, instrumentation, product tests, typed E2E,
artifact/verifier, benchmark plan, focused live proof, documentation, and
handoff.

At every step name:

- prerequisites;
- smallest focused test;
- exact stop/fail boundary;
- artifacts to retain;
- cleanup proof; and
- which already-passing suites must not be rerun while debugging a later
  failure.

Correctness, crash safety, resource ownership, and cleanup must pass before any
performance verdict can pass.

### G. Typed E2E catalog

Turn every section and bullet of `e2e_test.md` into concrete typed cases with
stable `S045-E##` family IDs and individual case IDs. Cover all of:

- static deletion, `unsafe`, mapping, owner, decoder, and call-graph checks;
- private build and visibility across every required file/tree/capability shape;
- deterministic GC-admission interleavings;
- exact readers and generation switching;
- all crash, short-write, torn metadata, `EIO`, response-loss, and `ENOSPC`
  durability boundaries;
- paginated and fair recovery, including histories much larger than 64;
- concurrency, lock order, same-key waiter 17, distinct-owner 65, and
  `Q = 1,4,16,64`;
- every resource cap and malformed-input/overflow/allocation-bomb boundary;
- supported Miri/Loom/sanitizer/fuzz campaigns, with unsupported cells explicit;
- command, PTY, and public file-API correctness and space attribution;
- read-only zero-durable-growth and mutating-byte ownership;
- long-running cancellation/restart/quiescence stability; and
- Stage 03/04/05/06 compatibility and authority boundaries.

Map each case to setup, failpoint or concurrency schedule, expected logical
state, retained physical copies and owners, resource counters, raw artifact,
deadline, cleanup, and verification ID. Unit tests alone cannot satisfy the
Stage 04.5 E2E exit gate.

### H. Exact future command registry and live E2E discipline

Verify and provide copy-ready future commands for:

- custody/static inventories;
- format, lint, compile, focused product tests, and relevant regressions;
- typed catalog collection;
- one E2E family or exact case at a time while debugging;
- the final complete typed correctness proof;
- benchmark contract/unit/integration tests;
- benchmark plan validation;
- the focused live 180-second benchmark campaign;
- strict artifact verification and negative tests;
- exact run recovery and cleanup;
- dependency/boundary and authority audits; and
- final documentation validation.

Use the existing Docker-backed repository paths and tools. Future live sandbox
work must rebuild the gateway with
`bin/start-sandbox-docker-gateway --rebuild-binary` when required by
`AGENTS.md`, and manual operations must use the supported
`sandbox-manager-cli`, `sandbox-runtime-cli`, and
`sandbox-observability-cli`.

Before every future live E2E, benchmark, or diagnostic command, append a pending
entry to:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md
```

The entry must include the exact command plus `Good`, `Defect`, and `Fix`
fields. After completion, fill only that pending entry with result counts, wall
time, artifacts/digests, failure class, next smallest action, exact owned
cleanup, and quiescence. Keep the report append-only. Preserve failed and
superseded attempts.

Debug feature by feature. Do not rerun a passing family merely because a later
family failed. Inspect the failed case's scoped logs/artifacts first, repair or
rerun only that case/family, then perform one final complete proof. Use run-ID
scoped cleanup only; never disrupt another agent's containers, processes,
ports, mounts, or artifact roots.

### I. Focused 180-second benchmark E2E campaign

Design a single runner-owned monotonic campaign of exactly 180 seconds for
better time, space, and interference coverage. Reuse and extend the existing
Stage 04 benchmark architecture; do not create an ad hoc script or a
benchmark-only product protocol.

The campaign contract must be explicit:

- prerequisites such as locked builds, fixture generation, digest checks,
  capability probes, plan validation, and uniquely owned artifact-root
  allocation occur outside the clock and are applied identically to both arms;
- the clock starts before the first campaign topology creation or pre-sample;
- stop admitting new workload operations at exactly 150 seconds;
- reserve `[150s,180s)` only for bounded settling, final space/resource samples,
  artifact serialization and fsync, strict verification, exact cleanup,
  quiescence, and a durable cleanup ledger;
- no individual operation may exceed 60 seconds;
- failed attempts and retries consume the original clock;
- the clock is never reset;
- cleanup/verifier completion after 180 seconds is `FAIL`; separately timed
  safety cleanup cannot turn it into `PASS`; and
- a missing or invalid cleanup ledger prevents a performance `PASS`.

Provide a deterministic second-by-second window table that covers as much of
the Stage 04.5 workload matrix as can be validly measured, prioritizing:

1. matched publication lock wait/hold and zero forbidden-work counters;
2. warm resolve/session/mount plus no-op and sustained command cells;
3. PTY create/drain/input/cancel semantics and latency;
4. public file-API sequential, 4-KiB random, metadata, and many-small-file
   cells;
5. cold build and private squash throughput/peak-space sentinels;
6. same-key and disjoint-key concurrency/cap sentinels;
7. 64-record recovery/history-scaling and crash/restart sentinels; and
8. foreground command/file/PTY latency while maintenance is active.

Use deterministic matched baseline/proposal inputs and counterbalanced order at
the smallest safe block, such as `A-B-B-A` plus its balanced complement.
Preserve semantics, corpus, cache state, filesystem, request sizes, fsync mode,
deadlines, and topology between arms.

Do not overclaim what fits in three minutes. A p95 gate requires at least 20
valid matched samples per arm and exact cell. Diagnostic p99 requires `n >=
100`. Otherwise report the actual statistic and
`INSUFFICIENT_SAMPLE`/`NOT_RUN`; omitted Cartesian cells remain `OPEN`. A
focused 180-second campaign does not make the full Stage 04.5 benchmark note
pass if required cells remain unproved.

For time, record raw per-arm samples, count, p50, p95, diagnostic p99 when
valid, maximum, MAD, ops/s or bytes/s, queue/setup/operation/verification/
teardown splits, timeouts, and exact threshold calculation:

```text
allowed = baseline * (1 + percent) + floor
```

Carry every exact threshold from `benchmark_note.md`; do not paraphrase away
the numeric gates.

For space, measure allocated physical bytes, not apparent length. Take
component-level samples before, at peak, after, after bounded quiescence, and
after exact cleanup. Attribute separately:

- logical payload;
- current materialization;
- exact old leased/pinned generations;
- private replacement target;
- operation staging/metadata;
- session upper/work allocation;
- loose/packed payload and locator metadata;
- old/new duplicate overlap;
- v1 rollback-authority bytes;
- abandoned operation residue; and
- unreachable but not-yet-Stage-05-reclaimed bytes.

Read-only/no-op commands, PTY without writes, reads, `stat`, and `readdir` must
leave zero new durable LayerStack operation, generation, root/object,
pack/locator, or staging bytes after bounded quiescence. Every mutating byte
must be attributed to session upper/work or an explicit publication.

For resources, sample idle, peak, settled, and final RSS, storage-owned live
bytes, workers, tasks, queues, permits, owners, waiters, FDs, mappings, holds,
leases, generations, mounts, operations, retries, and private paths. Report
runner wall time separately from build or lock wait.

Define a strict, versioned artifact layout and schema under a unique Stage 04.5
test evidence root. It is test evidence, never a product `/eos` layout. Include
raw time/space/resource samples, lifecycle and route/lock counters, source/host/
config/corpus identity, matched comparison records, verdicts, SHA-256 manifest,
and durable cleanup ledger. Define verifier rejection cases for missing,
unmatched, insufficient, late, non-quiescent, unowned, unexplained, or falsely
zero data.

### J. Verification traceability matrix

Create stable `S045-V##` verification IDs. Use columns equivalent to:

| Verification ID | Requirement/invariant | Test layer and case | Exact command ID | Required artifact/counters | Exact threshold/expected result | Initial status | Artifact/digest | Cleanup proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Every Stage 04.5 `MUST`, E2E bullet, benchmark gate, `/eos` lifecycle assertion,
resource cap, authority boundary, and exit criterion must map to at least one
verification row. Every work, E2E, layout, benchmark, artifact, resource,
cleanup, and handoff ID must map back to verification. No orphan IDs or broad
unresolved ranges are allowed.

Initial statuses must be honest. Use `NOT_RUN` where no direct Stage 04.5
execution exists and `OPEN` for unimplemented/unresolved work. An inherited
Stage 04 artifact may be named as a baseline or custody input, but not as direct
Stage 04.5 pass evidence.

### K. Canonical progress tracker and status rules

Define a closed status vocabulary, at minimum:

```text
OPEN
IN_PROGRESS
BLOCKED
PASS
FAIL
NOT_RUN
INSUFFICIENT_SAMPLE
```

Add narrowly named cross-stage deferral statuses only where the normative
documents explicitly defer work; never use one to hide a Stage 04.5 gate.

Create one canonical progress table with columns equivalent to:

| Work ID | Depends on | Deliverable | Initial status | Completion condition / exact verification | Run/artifact path and digest | Owner/blocker | Cleanup result | Last updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Populate it with every concrete gate/work (`G`), implementation (`I`), E2E
(`E`), `/eos` lifecycle (`L`), resource/cleanup (`R`), artifact/verifier (`A`),
benchmark (`B`), dependency/authority (`D`), and handoff (`H`) row. Do not leave
the table as an empty template.

Rules must state:

- only the canonical tracker changes progress;
- `PASS` requires a direct Stage 04.5 command result, retained raw artifact,
  SHA-256, exact threshold, and cleanup proof;
- code inspection, a diff, an inherited artifact, or prose is not a runtime
  pass;
- failed/superseded attempts remain retained;
- missing accounting is `OPEN`, not zero;
- `—` means no artifact exists;
- cleanup after the deadline cannot satisfy the campaign; and
- no runtime row passes with active run-owned resources or unexplained residue.

### L. Evidence-backed completion checklist

Provide a fully populated checklist table using unchecked `[ ]` items at
authoring time. Each row must map:

| Checklist item | Canonical progress row(s) | Verification ID(s) | Exact future retained artifact/command result | Cleanup evidence |
| --- | --- | --- | --- | --- |

Include separate completion items for at least:

- custody, reading, and authority reconciliation;
- complete `/eos` ownership/lifecycle/masking;
- deletion and retirement paths structurally unreachable;
- common four-state lifecycle and private-build/common-publish split;
- Stage 05 root-admission and exact old-subject handoff seam;
- writer-lock forbidden-work proof;
- shared bounded governor and every cap;
- bounded fair recovery and no history-derived selection;
- exact reader/session behavior across generation switch;
- crash/corruption/response-loss/`ENOSPC` safety;
- malformed input, memory safety, and supported tooling;
- command/file/PTY semantics and zero forbidden cold work;
- read-only zero durable growth and mutation byte attribution;
- long-running quiescence and exact cleanup;
- complete typed E2E proof;
- 180-second time/space/resource campaign and strict verifier;
- matched benchmark-note disposition with unproved cells left open;
- v1 authority and cross-stage compatibility; and
- outgoing Stage 05 handoff and final documentation validation.

No checklist box may be checked merely because this instruction document was
written.

### M. Outgoing handoff template and final validation

Include a self-contained Stage 04.5-to-Stage 05 handoff template covering:

- exact source/test/docs identities and dirty-state digests;
- implemented slice;
- production-deletion reachability audit;
- correctness/E2E results;
- benchmark time/space/resource results;
- `/eos` lifecycle and authority result;
- artifacts and SHA-256 values;
- cleanup/quiescence/custody;
- blockers, failed/insufficient/open cells;
- exact old-generation handoff contract; and
- Stage 05/06/07 boundaries.

End the document with a validation procedure that:

1. checks every required source was read and linked;
2. checks every relative link and cited repository path exists;
3. checks every specification exit criterion and E2E/benchmark requirement has
   work, test, verification, tracker, artifact, and cleanup coverage;
4. detects duplicate or orphan `S045-*` IDs;
5. verifies every future command against the current CLI/test architecture;
6. verifies all runtime rows remain `OPEN`/`NOT_RUN` without direct evidence;
7. verifies no Stage 04.5 text claims deletion, GC, public authority, or Stage
   05/06/07 ownership;
8. verifies the 180-second windows total exactly 180 seconds, admission ends at
   150 seconds, and cleanup/verifier/ledger fit in the last 30 seconds;
9. verifies physical-space and time thresholds are copied exactly; and
10. runs:

```bash
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs diff --check
```

## Quality bar

Be concrete enough that a future implementation agent can work without
re-deriving scope, paths, ordering, tests, thresholds, evidence, or cleanup.
Prefer tables and exact IDs where they improve traceability. Do not pad the
document with generic engineering advice.

The final guide must:

- match the actual current product/test repository structure;
- preserve the complete `/eos` ownership contract;
- cover every Stage 04.5 E2E and benchmark requirement;
- treat the three-minute benchmark as a strict monotonic evidence campaign;
- measure both time and allocated physical space carefully;
- preserve raw evidence and failed attempts;
- keep unsupported, insufficient, and unexecuted results explicit; and
- never claim `GO` until every Stage 04.5 exit criterion has direct evidence.

After writing, report only:

- the output file path;
- its line count and SHA-256;
- the major sections created;
- any exact unresolved contradiction/blocker; and
- confirmation that no implementation or live tests were performed.
