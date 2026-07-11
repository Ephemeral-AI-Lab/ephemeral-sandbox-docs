# Adversarial Architecture Review Prompt — Benchmark System Specification

Use this prompt to review and strengthen
`benchmark-system-spec.md` before backend implementation or when expanding the
benchmark catalog.

---

## Prompt

You are the adversarial architecture reviewer for the EphemeralOS Benchmark
Laboratory. Review this specification:

`ephemeral-sandbox-docs/implementation-plan/benchmark_test/benchmark-system-spec.md`

Also read these coordinated designs so recommendations remain implementable:

1. `ephemeral-sandbox-docs/implementation-plan/benchmark_test/benchmark-backend-design.md`
2. `ephemeral-sandbox-docs/implementation-plan/benchmark_test/benchmark-ui-design.md`
3. Applicable repository instructions and the existing operation/client APIs
   under `ephemeral-sandbox/`.

Your job is to determine whether the architecture is simultaneously:

1. simple and clean for the seven benchmarks we need now;
2. customizable through explicit, safe configuration;
3. easy to extend when we add operations, benchmark families, factors,
   fixtures, measurements, correctness checks, presets, and report views;
4. resistant to a “generic benchmark framework” that adds abstraction without
   reducing real change cost.

Do not approve the design because the document is detailed. Detail can conceal
coupling, duplicated concepts, unclear ownership, and speculative machinery.
Trace the actual change paths and identify the minimum architecture that keeps
future work local.

## Core review principle

Extensibility does not mean dynamic plugins, reflection, arbitrary code loading,
or making every value configurable. In v1, “plug in” should normally mean:

- add a small compile-time implementation;
- register a typed definition in one obvious place;
- inherit shared planning, scheduling, measurement, artifact, statistics, and
  reporting behavior;
- add operation-specific setup, execution, and correctness logic;
- expose only the configuration that has a real experimental meaning;
- require explicit security review for new privileged behavior.

Prefer boring Rust modules, enums, traits only where multiple implementations
exist, Serde schemas, existing workspace libraries, plain files, and existing
React/Mantine components. Reject a plugin SDK, dependency-injection container,
event bus, workflow DSL, database, distributed worker abstraction, or generic
graph engine unless a demonstrated requirement cannot be met more simply.

The target is a modular monolith: one local runner, clear internal boundaries,
compile-time operation registration, and versioned data contracts.

## Facts that must remain correct

Do not simplify away these product or scientific boundaries:

- Four current families and seven current operations.
- One active campaign per runner and sequential family execution in v1.
- Count semantics differ by family.
- LayerStack performs one squash request and varies live-session load.
- Setup, operation, verification, and teardown remain separately timed.
- Destructive benchmarks require fresh state according to their isolation rule.
- Raw observations are immutable and reports can be regenerated from them.
- Correctness failures remain visible and are excluded from successful latency
  distributions without being erased.
- Memory scopes and logical/allocated disk scopes remain separate.
- Public operations use product paths; the internal workspace-session adapter
  remains narrow and allowlisted.
- Test workspace path containment, ownership markers, and safe cleanup remain
  trust-boundary requirements.
- Comparisons reject incompatible scientific cohorts.

If simplicity conflicts with safety, correctness, reproducibility, or data
integrity, retain the protective mechanism and simplify its implementation.

## Questions the review must answer

### 1. Is the architecture understandable?

Can a new engineer explain the complete system in one diagram and answer:

- Which component owns the canonical experiment plan?
- Which component expands factors into cells?
- Which component schedules trials and concurrent requests?
- Which component performs operation-specific work?
- Which component collects common measurements?
- Which component decides whether a sample is correct?
- Which component persists raw evidence?
- Which component computes statistics and comparison compatibility?
- Which component exposes definitions and results to the UI?

Flag shared responsibilities, circular dependencies, and concepts represented
differently in the UI, API, executor, or artifact schema.

### 2. Is the common pipeline genuinely common?

Trace this lifecycle for every current operation:

```text
definition
  → plan validation
  → cell expansion
  → fixture/topology preparation
  → trial isolation
  → concurrent execution
  → resource measurement
  → correctness verification
  → teardown
  → immutable samples
  → statistics
  → report and comparison
```

Identify where family-specific branches enter the shared pipeline. Decide
whether each branch reflects real semantics or accidental code structure.

The common runner should own orchestration and evidence. Operation code should
own only what differs. However, do not force operations with fundamentally
different topology—especially LayerStack—through a tiny interface that hides
important lifecycle phases or pushes type checks everywhere.

### 3. Are customization boundaries explicit?

Classify every configurable value as one of:

| Class | Meaning |
|---|---|
| Experimental factor | A value intentionally varied or controlled in a study |
| Protocol | Trials, warmups, order, seed, timeout, sampling interval |
| Environment | Image, workspace root, isolated runtime configuration |
| Operation definition | Compile-time behavior, capabilities, valid factors |
| Derived value | Cell count, requests, estimates, observed outcomes |
| Safety policy | Fixed cap or allowlist that ordinary plans cannot bypass |

Find values placed in the wrong class. In particular, reject configurations
that expose implementation accidents, permit invalid combinations, duplicate
the product’s runtime config, or turn fixed safety limits into user options.

The UI and YAML should customize experiments, not assemble arbitrary executor
graphs.

### 4. Does the schema evolve cleanly?

Review the boundaries among:

- `ExperimentPlan` — user intent;
- `ExpandedPlan` — exact validated work;
- operation/family definitions — supported capabilities;
- `RunManifest` — effective environment and lifecycle;
- `TrialSample` and resource records — immutable evidence;
- `RunSummary` and report model — derived data.

Check whether adding one factor forces unrelated schemas to change, whether
operation-specific data is typed and namespaced, and whether unknown fields are
handled deliberately. Recommend the smallest versioning/migration policy that
can still read old reports and regenerate summaries.

Do not recommend one untyped `Map<String, Value>` for everything merely because
it is easy to extend. Do not recommend a giant closed struct with every factor
from every operation either. Find a typed middle ground and explain its tradeoff.

## Required extension drills

Do not discuss extensibility abstractly. Trace each scenario through UI
definitions, plan/schema, validation, cell expansion, setup, execution,
measurement, correctness, artifacts, statistics, report, comparison, tests,
and security.

### Drill A — Add an operation to an existing family

Add `file_list` to File Operations with factors for directory breadth, depth,
and result limit.

Answer:

- Which files/modules/contracts change?
- Can shared concurrency, timing, resource sampling, artifacts, statistics, and
  reports work unchanged?
- Where is the operation registered and allowlisted?
- Can the existing Files page render its common controls while adding only the
  operation-specific controls?
- Does comparison automatically include the new semantic boundary?

### Drill B — Add a lifecycle operation with different isolation

Add `destroy_workspace` to Workspace Lifecycle. It measures concurrent teardown
of prepared sessions, so setup occurs before the barrier and correctness checks
resource/registry removal afterward.

Determine whether the trial lifecycle supports a different measured phase
without copying the scheduler or misclassifying setup/teardown.

### Drill C — Add a new family

Add Sandbox Lifecycle with `create_sandbox` and `destroy_sandbox`.

Determine what should be reused and what deserves a new family page. A new
family may legitimately require explicit UI and topology logic; “zero files
changed outside one plugin” is not a sensible goal if it hides product meaning.

### Drill D — Add a new metric collector

Add sandbox CPU time and block I/O counters, which may be unavailable on some
platforms.

Determine whether collection, availability, raw records, summaries, units,
charts, exports, and comparison compatibility can be extended without changing
every executor.

### Drill E — Add an operation-specific phase

Add command queue delay as a server-correlated phase available only for
`exec_command`.

Determine whether optional phase observations are namespaced and reportable
without adding nullable command fields to every sample type.

### Drill F — Add a fixture profile and generator

Add a “Metadata Heavy” workspace containing 250,000 tiny files and deep
directories.

Determine whether it is a plan-only profile, a generator extension, or both;
how its real materialized cost is estimated; and whether it can reuse fixture
hashing, manifests, validation, and cache behavior.

### Drill G — Add a correctness verifier

Add a post-command filesystem-integrity verifier used only by selected command
cases.

Determine whether checks compose cleanly, retain stable check IDs, contribute
to the correctness verdict, and emit bounded evidence without executor-specific
report code.

### Drill H — Add a preset without code

Add “High Contention File Writes” using existing operations and factors.

This should require a versioned preset plan plus validation/tests, not a new
executor, route, or report component. If it requires code, identify the coupling.

### Drill I — Add a client path

Add a remote product client cohort later, while retaining `direct_client` and
`cli_e2e` as scientifically distinct cohorts.

Determine whether client path is an operation adapter, environment boundary,
or generic executor concern. Preserve credentials and comparability rules.
Do not design distributed scheduling now.

### Drill J — Add a report feature

Add a CPU-versus-latency correlation plot using already collected data.

Determine whether this is a report-model extension or requires raw-data/schema
changes. The UI must not independently invent different statistics.

## Change-surface budget

Use these targets as diagnostic guidance, not inflexible rules:

| Addition | Healthy expected change surface |
|---|---|
| New preset using existing capabilities | One preset file plus validation test |
| New factor value | Plan/preset data only when already supported |
| New workspace profile using the same generator | One definition/preset entry plus fixture test |
| New operation in an existing family | One executor module, one typed definition/registration, operation-specific UI controls if needed, and tests |
| New correctness check | One verifier implementation/registration plus tests; shared verdict/report unchanged |
| New resource metric | One collector/schema/report registration plus tests; executors unchanged |
| New family | New executors/topology and explicit family UI; shared pipeline/artifacts/statistics unchanged |
| New report derived view | Report derivation and UI plot; raw execution unchanged |

If a drill crosses many unrelated modules, name the coupling. If meeting the
budget requires a complex registry or erases type safety, reject the budget and
explain the smaller honest design.

## Simplicity audit

Search for these architecture smells in the specification and proposed design:

- a second representation of the same operation, factor, unit, state, or metric;
- a generic abstraction with one current implementation and no drill that needs
  a second;
- a registry that replaces ordinary Rust matching with runtime strings;
- dynamic plugin loading for a local first-party tool;
- operation-specific scheduling duplicated outside the common runner;
- one giant executor interface with optional methods for unrelated families;
- a tiny executor interface that forces downcasts or `if operation == ...` in
  shared code;
- family names hard-coded independently in the backend, UI, presets, reports,
  and comparison logic;
- UI-generated or executor-generated statistics that compete with the report
  builder;
- a universal event bus where direct function calls are clearer;
- storage hidden behind repositories despite one filesystem implementation;
- factories, dependency injection, or service locators without replacement
  needs in tests or current operations;
- configuration for fixed values that have no valid experimental alternative;
- broad internal RPC exposure to make future operations “easy”;
- a plan DSL powerful enough to express invalid or unsafe workflows;
- schema flexibility that discards type safety or reproducibility;
- premature distributed-runner concepts leaking into local MVP types;
- duplicated setup/teardown code that makes cleanup inconsistent;
- extension points that bypass security, correctness, or comparability checks.

Also search for the opposite problem: hard-coded branching that is simple for
seven operations but makes the same concept change in five places. Recommend a
shared definition only where at least two current operations or one concrete
extension drill proves its value.

## Architecture options to compare

Compare at least these three approaches instead of assuming the most abstract
one is best:

### Option 1 — Explicit enums and match statements

Operations and families are closed typed enums. The scheduler calls explicit
modules. This is easy to read and secure but may concentrate changes in a few
match statements.

### Option 2 — Compile-time definition registry

Each operation supplies a typed definition and executor registration. Common
planning/report metadata derives from the registry. This localizes additions
but can become a framework or stringly typed registry.

### Option 3 — Hybrid closed core with registered capabilities

Core lifecycle, safety, artifacts, and family semantics stay explicit. Repeated
metadata, metrics, checks, presets, and compatible operation handlers use small
compile-time registries or trait objects only where multiple implementations
exist.

Score each option using:

| Criterion | Weight |
|---|---:|
| Readability and debuggability now | 20% |
| Amount of code/indirection | 15% |
| Type safety and invalid-state prevention | 15% |
| Extension-drill change locality | 20% |
| Scientific consistency | 10% |
| Security and cleanup containment | 10% |
| Testability | 10% |

Select one architecture. Do not answer “it depends” without selecting the v1
default and defining the measured condition that would justify changing it.

## Ownership and dependency rules to test

Evaluate whether the following dependency direction is sufficient and clean:

```text
HTTP/UI contract
      ↓
plan model and definitions
      ↓
validator / expander / scheduler
      ↓
operation lifecycle implementations
      ↓
product clients and host adapters

resource collectors ─┐
correctness checks ──┼→ immutable observation/artifact model
event projection ────┘                  ↓
                              statistics / reports / compare
```

The runner may coordinate these components; operation modules should not depend
on HTTP or UI types. Statistics should depend on observations, not executors.
Reports should be rebuildable without product clients or Docker. Presets should
depend on the public plan schema, not internal Rust implementation details.

If this direction is wrong, replace it with a smaller diagram and explain why.

## Required output

Return the review in this exact order.

### A. Executive verdict

In ten sentences or fewer, state:

- whether the current specification is simple enough;
- whether its extension seams are sufficient;
- the three largest coupling or over-engineering risks;
- the architecture option selected for v1;
- which proposed future machinery should explicitly remain deferred.

### B. Current architecture map

Draw one component/dependency diagram and one experiment lifecycle sequence.
Mark unclear ownership, duplicate representations, and trust boundaries.

### C. Simplicity ledger

Use this table:

| Component/concept | Why it exists now | Simplest viable form | Evidence for abstraction | Keep, simplify, defer, or delete |
|---|---|---|---|---|

Do not label safety, correctness, accessibility, or artifact durability as
over-engineering merely because they require code.

### D. Extension-drill matrix

For drills A–J, provide:

| Drill | Modules/contracts touched | Reused pipeline | New code genuinely required | Coupling exposed | Verdict |
|---|---|---|---|---|---|

Classify each verdict as:

- `Clean`: change is local and follows an obvious pattern.
- `Acceptable`: several intentional boundaries change for a valid reason.
- `Coupled`: unrelated modules must change or concepts are duplicated.
- `Over-generalized`: the current abstraction is more complex than the drill.

### E. Architecture option decision

Score the three options with the weighted criteria, show reasoning, select one,
and state what evidence would justify moving to a more dynamic design later.

### F. Prioritized findings

Use:

| Priority | Spec section | Finding | Concrete failure scenario | Smallest corrective change |
|---|---|---|---|---|

Priorities:

- `P0`: breaks safety, correctness, reproducibility, or artifact integrity.
- `P1`: creates a foundational coupling or blocks a required extension drill.
- `P2`: avoidable complexity, duplication, or unclear ownership.
- `P3`: documentation/terminology improvement with implementation value.

Every finding must cite a section and demonstrate a present operation or one of
the required drills. Do not propose abstractions “for future operations” without
naming a drill they simplify.

### G. Recommended minimal extension model

Define the smallest necessary contracts for:

- operation identity and definition;
- valid factor schema and cell expansion;
- operation lifecycle/executor behavior;
- fixture/topology preparation;
- resource metric collection;
- correctness checks;
- raw observation extensions and optional phase data;
- report derivations and comparison identity;
- presets.

For each contract, state whether it should be an enum, struct, trait, function,
compile-time registry, versioned data file, or ordinary module. Include a short
Rust-like sketch only when it makes ownership clearer. Avoid a complete
framework implementation.

Explicitly show the new-operation path from registration through UI definition
and report. Make security allowlisting and comparison identity mandatory parts
of registration rather than optional conventions.

### H. Customization matrix

List what users may configure, what advanced users may configure, what is
derived, and what remains fixed by safety policy. Identify any current option
that should move categories.

### I. Proposed specification edits

Provide exact, concise text or a patch outline for
`benchmark-system-spec.md`. At minimum consider whether it needs sections for:

- architectural principles and dependency direction;
- operation extension contract;
- capability/definition ownership;
- configuration classification;
- schema/version evolution;
- extension acceptance tests.

Do not rewrite unrelated measurement or UI content. Prefer a small number of
high-leverage additions and removals.

### J. Extension acceptance tests

End with tests that prove the architecture stays extensible, such as:

- a fixture/preset-only addition requires no executable code changes;
- a fake operation can reuse scheduling, measurement, artifacts, and reports;
- a new metric requires no executor edits;
- an operation-specific phase round-trips without changing unrelated samples;
- reports regenerate from an older supported artifact schema;
- an unregistered internal operation cannot be invoked;
- cleanup and correctness policies cannot be bypassed by an extension;
- compatibility identity changes when operation semantics change.

Make every test observable and automatable.

## Review constraints

- Read the whole specification and trace the real code boundaries before
  recommending changes.
- Prefer deletion, reuse, enums, functions, and existing workspace dependencies
  before new traits or registries.
- A trait must have at least two real implementations, a test replacement that
  materially helps, or a required extension drill that proves the seam.
- A registry must reduce duplicated metadata without making behavior stringly
  typed or bypassing compile-time exhaustiveness where it matters.
- Do not design dynamic third-party plugins in v1.
- Do not make the browser an execution engine.
- Do not move statistics or comparison decisions into operation executors.
- Do not let presets execute arbitrary code.
- Do not turn safety allowlists or cleanup policy into ordinary configuration.
- Do not claim a design is extensible without completing drills A–J.
- Do not claim a design is simple merely because it has few files; count
  concepts, representations, branches, and change sites.
- Do not use “future-proof” as evidence.
- Select a concrete v1 architecture and name its intentional ceiling.

The final review should leave the team with a smaller, clearer architecture and
a repeatable path for adding real benchmark capabilities without copying the
pipeline or building a speculative plugin platform.

