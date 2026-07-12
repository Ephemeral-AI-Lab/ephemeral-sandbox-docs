# Adversarial Review and Rewrite Prompt — E2E Architecture and Control Room UX

You are a staff-plus software architect, test-infrastructure engineer, and
product UX reviewer. Review the EphemeralOS E2E architecture and Test Control
Room as if you will own it for the next five years.

Your task is not to defend the existing design. Your task is to find the
cleanest, smallest, most understandable architecture that preserves the
required product behavior and gives users a trustworthy way to discover, run,
and understand tests.

Be bold. You are explicitly authorized to rewrite the four design documents
destructively. You may delete sections, collapse abstractions, rename concepts,
replace folder trees, change APIs, change UI flows, reorder implementation
phases, and reject requirements proposed by the current documents. Do not
preserve an idea merely because it is detailed or repeated across multiple
documents.

Prefer simplicity over compatibility with the draft. Prefer a small number of
stable seams over speculative frameworks. Prefer one authoritative model over
several synchronized representations. A more future-proof design is one where
ordinary additions remain ordinary—not one with an abstraction for every
hypothetical extension.

Do not weaken safety, stable identity, truthful verdicts, cleanup containment,
or immutable historical evidence merely to reduce line count. Simplify how
those guarantees are achieved.

This authorization applies to documentation only. Do not modify product code,
test code, repositories, workspaces, Docker state, or retained evidence. Do not
run live Docker E2E tests. Read-only inspection and offline structural checks
are allowed.

## Source material

Read all four documents completely before editing:

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/e2e_test/e2e-test-system-spec.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/e2e_test/e2e-test-design.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/e2e_test/e2e-test-ui-design.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/e2e_test/e2e-test-implementation-plan.md`

Inspect the relevant source trees and implemented code read-only when they
exist. Do not infer implementation from a specification, screenshot, or static
prototype.

The current configured roots are design inputs, not untouchable architecture:

```text
TEST_REPOSITORY_ROOT=/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
PRODUCT_ROOT=/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
WORKSPACE_STORE_ROOT=/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test-workspace
```

The existing prototype under
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/e2e/ui-prototype` is visual
evidence only. It does not prove that a workflow is usable or implemented.

## Governing review principles

Apply these principles in order:

1. **One owner per fact.** Taxonomy, test identity, feature meaning, validation
   intent, execution status, and historical result must each have one canonical
   owner.
2. **Obvious dependency direction.** Product, test definitions, collection,
   execution, persistence, API projection, and UI must form a readable flow
   without cycles.
3. **Source is not state.** Generated catalogs, build outputs, reports, logs,
   screenshots, attempts, caches, and workspaces must not pollute tracked test
   source.
4. **Paths aid navigation; IDs preserve identity.** Moving a test file must not
   destroy history, retry lineage, or deep links.
5. **The UI consumes projections.** It must not understand pytest paths, scan
   files, join several registries per row, control Docker directly, or recreate
   backend rules.
6. **Runtime boundaries stay real.** E2E execution should exercise CLI, HTTP,
   SSE, gateway RPC, or explicitly allowlisted daemon RPC boundaries. E2E
   source and workspace code must not import product application handlers or
   use cross-repository Cargo path dependencies. Product-owned binaries and a
   product-side probe may compile against product crates and be invoked as
   subprocesses.
7. **Ordinary growth is data-driven.** A valid new annotated test or expanded
   case should appear in the UI after collection succeeds, without a new route,
   card, switch branch, icon mapping, or frontend registration.
8. **Failure stays truthful.** Stale catalogs, disconnected streams, cleanup
   work, degraded evidence, cancellation, and recovery blockers must never be
   presented as healthy, live, or complete.
9. **Future-proof means low change amplification.** Optimize for the number of
   owners and files that must change, not for the number of extension points.
10. **Delete before adding.** Before proposing a new layer, explain why a typed
    record, function, pytest hook, subprocess, filesystem record, or existing UI
    component is insufficient.

## Part 1 — Attack architecture cleanness and simplicity

### 1.1 Reconstruct the architecture

Before trusting any diagram in the documents, reconstruct the actual proposed
system. Identify:

- canonical product-operation authority;
- taxonomy, ownership, feature, and validation authorities;
- test declaration and expanded-case identity;
- collection, validation, and catalog publication;
- selection, preview, admission, execution, and cancellation;
- run journal, reducer, current projection, history, and retry lineage;
- workspace preparation, attempt isolation, cleanup, retention, and purge;
- API projections and UI query ownership;
- product binaries, protocol boundaries, and build caches;
- every configured and derived root, including who may write or purge it.

Produce a dependency diagram. Flag competing owners, circular dependencies,
reverse dependencies, duplicated schemas, and concepts that exist only because
another unnecessary concept was introduced.

### 1.2 Run a simplicity audit

Challenge every registry, schema layer, adapter hierarchy, state machine,
event type, compatibility mechanism, cache, index, background worker, API
endpoint, and UI query.

For each, ask:

- What present requirement requires it?
- Is there one real consumer or several?
- What breaks if it is deleted?
- Can an existing record or module own the behavior?
- Is it solving demonstrated scale or hypothetical scale?
- Does it reduce change amplification, or merely relocate complexity?
- Can a new contributor explain it without reading all four documents?

Recommend `keep`, `merge`, `simplify`, `defer`, or `delete`. When proposing a
replacement, specify the smaller end-to-end flow rather than adding another
facade around the old one.

Pay special attention to:

- duplicate Rust, Python, controller, and frontend taxonomy;
- partial/incremental catalog merging versus atomic recollection;
- multiple configuration roots or aliases for derived paths;
- compatibility matrices for versions that do not yet need compatibility;
- both event journals and databases storing the same authority;
- per-row UI joins and N+1 API calls;
- UI-specific endpoints where one generic projection would work;
- speculative plugin systems, workflow DSLs, and dependency injection;
- excessive versioned types that always change together;
- abstractions with only one implementation.

### 1.3 Audit files and folders

Inspect the current and proposed trees. Do not reward visual symmetry. Require
each folder to have one clear purpose and each file to have a predictable home.

At minimum, classify:

- product-domain tests;
- Compound scenarios;
- harness/infrastructure tests;
- shared test support;
- controller/API code;
- metadata and schemas;
- web UI;
- offline framework tests;
- benchmark source/configuration;
- catalogs, reports, runs, attempts, evidence, build caches, and temporary data.

Attack these failure modes:

- test files mixed with framework implementation;
- root-level outliers with no ownership class;
- generic junk drawers such as `utils`, `common`, or `misc`;
- helpers promoted globally before demonstrated reuse;
- features encoded in both paths and metadata;
- folder names treated as stable identity;
- mutable state written beside source;
- benchmark state nested ambiguously under E2E state;
- multiple roots that can alias or contain each other;
- purge rules that operate on a shared parent;
- CWD, home-directory, `TMPDIR`, or environment-dependent resolution;
- workspace directories that import product crates or application handlers.

Propose the smallest clean source tree and a separate mutable-state tree. State
the purpose, owner, and purge boundary of every top-level directory. If the
current layout is already better than an alternative, keep it and explain why.

### 1.4 Measure change amplification

Trace the exact files and components touched by each change:

1. Add a parameterized case to an existing test.
2. Add a test to an existing group.
3. Add a group to an existing family.
4. Add an E2E-only family.
5. Add a new product domain legitimately owned by the Rust product catalog.
6. Add a feature and two named validations.
7. Add a Compound scenario and a new complexity value.
8. Rename or move a test source file without changing its stable identity.
9. Add an invalid test with a duplicate ID or unknown metadata reference.
10. Change a product catalog input while the controller is running.

The target behavior for a valid new annotated test is:

```text
save source
→ controller detects the input change
→ one debounced full collection
→ validate one complete candidate
→ atomically publish one catalog revision
→ notify the UI
→ invalidate and refetch one combined catalog query
→ test appears without restart or frontend registration
```

If the architecture cannot achieve this simply, redesign it. If it claims to
achieve it, require an observable acceptance test.

### 1.5 Audit round trips

Count network calls for the primary flow. Treat avoidable browser joins as an
architecture defect.

The design should justify any departure from this budget:

```text
browse catalog:       1 combined query
review exact scope:   1 preview request
start run:            1 admission request
follow live run:      1 snapshot plus 1 SSE connection
open evidence:        on demand
catalog changed:      1 notification plus 1 combined-query refetch
```

Do not optimize call count by returning an unbounded payload or combining
unrelated mutation semantics. The goal is a cohesive projection, not one giant
endpoint.

## Part 2 — Attack the user-facing Test Control Room

Review the UI as an operational product, not an internal schema browser. A
first-time user should be able to find the right behavior, understand what will
run, start it safely, follow progress, and understand the result without reading
implementation documentation or raw logs first.

### 2.1 Labels, tags, and information hierarchy

Verify that the UI makes these concepts visibly distinct:

| Concept | User question |
|---|---|
| Domain / family / group / scenario | Where does this test belong? |
| Test / expanded case | What exact behavior and parameters will run? |
| Feature tag | What capability or contract is covered? |
| Direct / inherited feature | Why is this feature associated with the case? |
| Named validation | What observable check proves the claim? |
| Required / optional validation | Can the test pass when this check is absent? |
| Execution surface | Which real product boundary is exercised? |
| Execution label | What scheduling, cost, or risk property applies? |
| Status / verdict | What is happening or what happened? |
| Evidence health | How complete is the supporting diagnostic data? |

Find and eliminate “chip soup”: badges with different meanings but identical
appearance, color-only distinctions, tooltip-only explanations, raw IDs where
human labels are needed, and large tag clouds that bury the test purpose.

Require:

- a plain-language title and purpose before internal IDs and paths;
- searchable feature labels and descriptions;
- visible direct/inherited provenance;
- named validations attached to the feature claims they prove;
- explicit units for every count;
- consistent labels across catalog, preview, live run, history, and retry;
- accessible names, keyboard operation, stable focus, and usable zoom;
- honest empty, unavailable, deprecated, invalid, and stale states.

### 2.2 Review the complete run journey

Attempt these tasks without relying on documentation:

1. Find a test by behavior or feature rather than source path.
2. Understand why the result matched the search.
3. Compare cases and inspect feature/validation coverage.
4. Select a mixture of cases and catalog groups.
5. Review the exact server-expanded scope.
6. Understand workspace, resource, execution-surface, telemetry, and fail-fast
   policies.
7. Resolve blockers and warnings correctly.
8. Start exactly one run without duplicate admission.
9. Follow the current case, phase, validation, elapsed time, and evidence.
10. Distinguish first failure, primary verdict, cleanup failure, cancellation,
    fail-fast `Not run`, and degraded evidence.
11. Reopen history and create a new retry preview without confusing Retry with
    Resume.

Remove steps, screens, confirmations, and fields that do not improve safety or
understanding. Add a step only when omitting it can cause the wrong scope to run
or cause the user to misunderstand system truth.

### 2.3 Require good in-flight messages

A spinner and “Running” are not sufficient. For every meaningful state, the UI
must answer:

- What is happening now?
- Why is it happening?
- Which run, case, validation, or subsystem owns the work?
- Is the displayed state live, reconnecting, stale, or historical?
- What can the user safely do now?
- What must complete before the next transition or final verdict?

Review or rewrite the exact visible copy for at least these states:

| State | Minimum message content |
|---|---|
| Catalog refreshing | Inputs changed; recollection is running; old data is identified as stale |
| Catalog invalid | Last-good revision is preserved; exact diagnostic and blocked action are visible |
| Preview checking | Current preflight check and why Start is unavailable |
| Preview ready | Scope is exact and frozen; expiry and Start action are clear |
| Preview blocked | Specific blocker, affected scope, and safe recovery action |
| Admission pending | One request is in flight; duplicate Start is prevented |
| Active-run conflict | Which run owns the lane and what the user can do |
| Preparing | Workspace/environment action currently running |
| Case running | Case, phase, elapsed time, validation, and evidence freshness |
| Failure detected | First causal failure is visible while finalization remains pending |
| Fail-fast applied | Causal failure and which remaining cases became `Not run` |
| Cleaning up | Mandatory cleanup is active; terminal completion is not claimed |
| Evidence finalizing | Product work ended but evidence is not final |
| Reconnecting | Last verified sequence/time and reconnect behavior |
| Stream stale | No Live claim; timer freezes and an “as of” time is visible |
| Cancelling | What stops, what continues, and why cleanup still runs |
| Recovery blocked | Exact incompatibility and authorized next action |
| Terminal | Verdict, causal failure, cleanup, and evidence health are separate |

Messages must be causal, stable, and actionable. Do not announce every log line,
telemetry sample, timer tick, or low-level event. Announce meaningful state
changes once. Never steal focus or force-scroll logs when a failure arrives.

### 2.4 Adversarial UX scenarios

Walk through these scenarios and identify the first misleading or confusing
moment:

1. A user searches by feature phrase but does not know the taxonomy.
2. A valid new test appears while the Catalog page is already open.
3. A new test is invalid and a last-good catalog exists.
4. Filters change after the user has created a durable mixed selection.
5. A required dependency is unavailable while optional telemetry is degraded.
6. Another run acquires the serial lane immediately before Start.
7. One validation fails, fail-fast skips later cases, and cleanup continues.
8. An assertion fails and teardown later raises a more severe error.
9. Product validations pass while evidence is incomplete or truncated.
10. The SSE stream disconnects, becomes stale, and later replays events.
11. The user cancels while one case is active and others are queued.
12. A controller restart encounters a run admitted by a different bundle.
13. A historical run has purged raw evidence but retained its result projection.
14. A large catalog and high-volume live run stress scrolling, filtering,
    focus, and announcement behavior.

Static mockups cannot pass interaction-dependent scenarios. Mark them
`Specified only` or `Not provable` when executable evidence is absent.

## Part 3 — Rewrite authority and method

After the adversarial review, edit the four documents directly when the current
architecture is not the best answer. Do not merely append a list of objections
to contradictory text.

When rewriting:

1. Choose one architecture and propagate it through all four documents.
2. Delete obsolete alternatives, duplicated explanations, stale paths, unused
   types, and superseded phases.
3. Keep the system specification normative and outcome-focused.
4. Keep the technical design concrete about ownership, data flow, boundaries,
   storage, APIs, and failure behavior.
5. Keep the UI document focused on user journeys, exact labels/messages,
   accessibility, responsive behavior, and observable states.
6. Keep the implementation plan dependency-ordered, testable, and free of work
   for abstractions that were deleted.
7. Use the same names, enums, roots, state transitions, and API semantics in all
   four documents.
8. Prefer replacing a section cleanly over layering exceptions onto it.
9. Preserve important rationale briefly; do not preserve the history of every
   rejected draft decision.
10. Add acceptance criteria for every critical architecture or UX claim.

You may conclude that the current architecture is already the simplest valid
one, but only after attempting a smaller alternative and showing why it fails a
real guarantee.

## Evidence and severity

Every finding must include:

- exact file and line or section;
- the violated principle;
- concrete maintenance cost or user harm;
- the simpler replacement;
- an observable acceptance proof.

Use these severities:

- `P0 Blocker`: can run the wrong scope, corrupt or lose truth, mutate/purge an
  unsafe path, or falsely claim live/complete state.
- `P1 Critical`: competing authority, circular dependency, unusable primary
  workflow, manual frontend registration for ordinary test growth, or hidden
  cleanup/failure state.
- `P2 Major`: substantial avoidable complexity, change amplification, unclear
  folder ownership, misleading labels/tags, poor recovery guidance, or
  accessibility failure.
- `P3 Minor`: local naming, wording, hierarchy, or visual issue with concrete
  impact.

Do not write vague findings such as “simplify architecture,” “improve
hierarchy,” or “add better loading states.” Name the component, duplicated
authority, user state, exact message, and smallest corrective change.

## Required deliverables

Return these sections in order:

### 1. Executive verdict

Choose exactly one:

- `PASS`
- `PASS AFTER REWRITE`
- `FAIL — IMPLEMENTATION SHOULD NOT START`

State the chosen architecture and the three largest remaining risks.

### 2. Architecture before and after

Include a compact dependency diagram, canonical ownership table, and source/
mutable-state trees. Explain what was deleted, merged, or moved.

### 3. Simplicity ledger

| Component or concept | Present need | Simpler form | Decision | Proof |
|---|---|---|---|---|

### 4. Change-amplification and auto-loading proof

Show the exact files/components changed for the ten extension attacks. Explicitly
answer whether a valid future test automatically appears in an already-open UI
and what happens when collection fails.

### 5. Round-trip budget

List calls for catalog browsing, preview, admission, live following, catalog
refresh, and evidence. Identify and remove N+1 behavior.

### 6. File and folder verdict

List every top-level directory, its single purpose, owner, allowed contents,
and purge boundary. Identify unresolved outliers or junk drawers.

### 7. UI journey and label/tag verdict

Show whether a first-time user can find, understand, select, preview, run,
follow, diagnose, and retry tests. Include concrete corrections to confusing
labels or badge systems.

### 8. In-flight message matrix

| State | Exact headline | Supporting explanation | Freshness | Safe action | Forbidden claim |
|---|---|---|---|---|---|

Cover every state in §2.3 with proposed user-facing copy.

### 9. Prioritized findings and edits made

| ID | Severity | Evidence | Impact | Rewrite applied | Acceptance proof |
|---|---|---|---|---|---|

Distinguish changes actually made to the documents from recommendations that
remain open.

### 10. Cross-document consistency proof

After editing, search all four documents for stale roots, enums, APIs,
component names, recovery semantics, and superseded architecture. Check
Markdown structure, whitespace, and local links. Report every skipped check.

### 11. Smallest implementation sequence

End with the shortest dependency-ordered implementation plan that proves the
architecture incrementally. Do not preserve phases whose only purpose was to
build deleted complexity.

## Final pass criteria

Do not pass the design unless all of the following are true:

- a contributor can explain the architecture and dependency direction from one
  diagram and one ownership table;
- every top-level folder has one purpose and mutable state is outside source;
- source/workspace code does not import product application handlers or use
  cross-repository Cargo path dependencies;
- one canonical owner exists for taxonomy, identity, features, validations,
  run truth, and history;
- moving a file does not change stable test/case identity;
- a valid new annotated test automatically reaches the open UI through one
  atomic catalog refresh and one combined-query refetch;
- invalid catalog input preserves last-good truth and blocks unsafe admission;
- ordinary extensions do not require domain-specific API or frontend code;
- the primary run flow stays within an explicit, justified round-trip budget;
- users can distinguish taxonomy, feature tags, validations, execution
  surfaces, statuses, and evidence health;
- exact scope and blockers are visible before Start;
- in-flight messages say what is happening, why, how fresh it is, what remains,
  and what action is safe;
- disconnect, cleanup, cancellation, recovery, and evidence degradation cannot
  produce a false Live, Passed, or Complete claim;
- the four documents describe one architecture without stale alternatives;
- every critical claim has an observable acceptance test.
