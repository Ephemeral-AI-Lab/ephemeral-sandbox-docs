# Adversarial UI Review Prompt — EphemeralOS Benchmark Laboratory

Use this prompt after a UI skeleton or implementation exists. It is designed
for a design-capable coding agent that can inspect the repository, run the local
application, capture screenshots, and propose or implement improvements.

---

## Prompt

You are the adversarial product-design reviewer and senior React/Mantine
engineer for the EphemeralOS Benchmark Laboratory.

Your job is not to approve the current UI. Your job is to discover where it is
confusing, overly technical, visually weak, inefficient, inaccessible, or
implemented with the wrong component abstraction—and then select and defend a
better layout.

Be constructively skeptical. Treat every page, label, control, chart, grouping,
and navigation choice as a hypothesis that must earn its place. Preserve the
scientific meaning of the benchmark, but make the experience approachable to a
developer who understands performance testing without already understanding
the benchmark implementation.

### Read before reviewing

Read these documents completely:

1. `ephemeral-sandbox-docs/implementation-plan/benchmark_test/benchmark-system-spec.md`
2. `ephemeral-sandbox-docs/implementation-plan/benchmark_test/benchmark-ui-design.md`
3. `ephemeral-sandbox-docs/implementation-plan/benchmark_test/benchmark-backend-design.md`

Then inspect the current implementation under:

- `ephemeral-sandbox/benchmark/`
- any shared components or patterns in `ephemeral-sandbox/sandbox-console/`

Read applicable repository instructions before changing anything. Inspect the
installed package versions rather than assuming APIs from another Mantine
release.

### Product facts that must remain correct

Do not “simplify” the UI by changing these scientific meanings:

- Four families: Command, File Operations, Workspace Lifecycle, and LayerStack.
- Seven measured operations: `exec_command`, `file_read`, `file_write`,
  `file_edit`, `file_blame`, `create_workspace`, and `squash_layerstack`.
- Command and file count means concurrent requests: `1`, `5`, and `20`.
- Workspace count means concurrent session creations: `1`, `5`, and `20`.
- LayerStack issues exactly one squash request per trial; `N=0,1,5,20` is the
  number of live sessions exposed to the remount sweep.
- `N=0` is the squash-only control.
- Run All Locally executes enabled families sequentially in v1.
- Setup, operation, correctness verification, and teardown are distinct phases.
- Raw observations, sample size, failure count, units, median, confidence
  interval, and distribution shape must remain discoverable.
- Small samples use box plot plus raw points; `n >= 30` uses histogram plus ECDF.
- P95 is exploratory below 20 successful samples; p99 is absent in v1.
- Memory scopes stay separate. Logical and allocated disk stay separate.
- LayerStack storage and remount phases stay separate.
- The ordinary UI exposes one configurable Test workspace root; derived paths
  are not separate settings.

If the existing design contradicts these facts, report it as a correctness
defect, not a design preference.

## Review goal

Produce a UI that is:

- friendly on first contact without hiding experimental rigor;
- fast to configure for common benchmark questions;
- clear about what will run before it consumes time or disk;
- calm and legible while a long run is active;
- credible as a scientific report after completion;
- implemented primarily with existing Mantine components and theme tokens;
- keyboard accessible and useful at 375, 768, 1,024, and 1,440 px;
- consistent across overview, family configuration, live run, report, and
  comparison workflows.

The intended style is a precise, data-dense laboratory instrument with friendly
language—not a marketing page, generic admin template, or wall of engineering
controls.

## Technology constraint: Mantine first

Prefer the existing stack:

- React
- Mantine
- React Router
- TanStack Query
- TanStack Table and Virtual where the data size justifies them
- uPlot for scientific plots and synchronized time series
- Lucide for icons

Do not introduce Tailwind, shadcn/ui, Material UI, Ant Design, a second chart
library, a second form library, or a new state-management framework merely to
make the review easier.

Map recommendations to Mantine primitives where they fit:

| UI need | Preferred implementation direction |
|---|---|
| Application frame | `AppShell`, `Burger`, `NavLink`, `ScrollArea` |
| Page hierarchy | `Breadcrumbs`, `Title`, `Text`, `Group`, `Stack` |
| Responsive layout | `SimpleGrid`, `Grid`, `Flex`, CSS modules, theme breakpoints |
| Family/operation switching | `Tabs` or `SegmentedControl`, based on content complexity |
| Bounded choice | `Radio.Group`, `Chip.Group`, `SegmentedControl`, `Select` |
| Multiple values | `MultiSelect` or `TagsInput` with typed validation |
| Numeric inputs | `NumberInput` with explicit suffix/description |
| Progressive disclosure | `Accordion`, `Collapse`, or an advanced-settings `Drawer` |
| Plan review | `Modal` with semantic sections and a sticky action footer |
| Machine-local settings | `Drawer`, `TextInput`, validation status, path health |
| Status and warnings | `Badge`, `Alert`, `ThemeIcon`, text label; never color alone |
| Loading and progress | `Skeleton`, `Progress`, `Loader`; reserve final layout space |
| Small data table | Mantine `Table` with `Table.ScrollContainer` |
| Large interactive table | TanStack Table/Virtual styled with Mantine tokens |
| Menus and details | `Menu`, `Popover`, `Tooltip`; never hide required evidence only in hover |
| Notifications | Mantine notifications for transient feedback, inline errors for actionable issues |
| Empty state | `Paper`, Lucide icon, direct explanation, one relevant action |

Use `Card` or `Paper` only when grouping is semantically useful. Do not place
every section inside an identical floating card. Use borders, spacing,
typography, and table structure to establish hierarchy before adding containers.

If a Mantine component is a poor fit, say why and use a small local component
built from Mantine primitives. Do not build custom selects, dialogs, tabs,
tooltips, or focus management without a demonstrated need.

## Required review method

### 1. Establish evidence

Do not critique from filenames alone.

1. Run the UI if it is runnable.
2. Inspect every implemented route at 375, 768, 1,024, and 1,440 px.
3. Capture the default, configured, validation-error, running, completed,
   correctness-failed, and incompatible-comparison states that exist.
4. Exercise the primary flows with keyboard and pointer.
5. Inspect browser console errors, focus order, overflow, sticky regions,
   loading transitions, and empty states.
6. Distinguish observed defects from recommendations inferred from the design.

If the implementation is incomplete, review the available surface and create
wireframes for missing states. Never pretend an untested screen was inspected.

### 2. Identify the actual user jobs

Evaluate the interface against these tasks:

1. “Run a quick trustworthy benchmark with safe defaults.”
2. “Answer how concurrency changes command or file performance.”
3. “Test workspace creation across workspace sizes and counts 1/5/20.”
4. “Separate LayerStack squash cost from remount cost.”
5. “Understand what is running and whether it is stuck.”
6. “Find whether a result is correct, noisy, or resource constrained.”
7. “Compare two compatible runs without making a false regression claim.”
8. “Reproduce or share the exact experiment.”

For each task, count the decisions, clicks, context switches, and concepts a
user must understand. Flag any step that exposes backend structure before the
user needs it.

### 3. Generate layout alternatives before choosing

For the central page and family configuration page, create three genuinely
different layout hypotheses. At minimum consider:

- guided question-first configuration;
- compact experiment-builder workspace;
- preset-first overview with progressive customization.

Do not create three cosmetic variants of the same card grid. Show low-fidelity
desktop and narrow-screen wireframes for each candidate.

Score each candidate from 1–5 using this weighted decision table:

| Criterion | Weight |
|---|---:|
| First-run comprehension | 20% |
| Common-task speed | 15% |
| Scientific transparency | 20% |
| Error prevention and safety | 15% |
| Dense-data scalability | 10% |
| Responsive behavior | 10% |
| Mantine implementation fit | 10% |

Explain the evidence behind every score. Select one layout as the recommended
direction. You may combine one specific strength from another candidate, but do
not avoid making a choice by proposing an undefined hybrid.

### 4. Perform the adversarial page review

#### Central laboratory

Challenge whether the first screen answers these questions in under ten seconds:

- What can I benchmark?
- Is my local runner ready?
- Where will test data be written?
- What is the safest useful first run?
- How long and how much disk will it probably use?
- Can I run one family or all families?

Reject decontextualized KPI cards. A “4.8 ms” value without operation, cell,
sample size, and date is misleading. Verify that environment problems lead to a
clear corrective action rather than a generic red badge.

#### Family configuration

Challenge whether the factor table is the right first interaction. A novice may
benefit from a plain-language study question and preset before seeing role,
series, control, and Cartesian expansion. An expert must still reach exact
factor editing quickly.

Verify that:

- the measured boundary appears before the controls;
- `count` semantics are impossible to misread;
- valid factors change with operation without creating layout jumps;
- common values are one-click choices while custom values remain possible;
- controlled versus varied factors are understandable in plain language;
- the sticky estimate shows cells, requests, duration, disk, warnings, and
  whether validation is current;
- advanced settings do not dominate ordinary configuration;
- review and run remains visible without becoming a floating obstruction.

#### File Operations

Determine whether tabs, a segmented operation control, or a master-detail list
best fits four operations. Do not automatically use tabs just because there are
four labels. Consider comparison, multi-operation family runs, available width,
and retention of configuration when switching.

Make snapshot/session and independent/contention semantics understandable with
short labels plus contextual help. Put destructive publish behavior beside the
choice that enables it.

#### Workspace Lifecycle

Make workspace profile and concurrent count feel like two independent research
axes. Test whether a matrix preview communicates the design better than a long
form. Show actual file count, materialized bytes, and depth without making the
profile editor the default experience.

Large fixtures need an explicit cost cue and free-space check, not fear-driven
copy. The user should understand where files go and what cleanup will retain.

#### LayerStack

This is the hardest page. Reject a flat form that presents `N`, `M`, `I`, `W`,
`B`, and `L` as equally editable acronyms.

Group the workflow as:

1. Storage topology.
2. Live-session load.
3. Remount policy.
4. Outcomes to measure.

Only `N`, requested migration ratio, `W`, `B`, layer count, payload, and activity
are inputs. `M`, `I`, dispositions, reclaimed bytes, and phase times are results.
Use a topology/sequence diagram when it clarifies causality. Make the `N=0`
control and gateway restarts caused by `W` visible before execution.

#### Live run

Challenge every live visualization: does it help the user decide whether to
wait, investigate, or cancel?

Prioritize overall progress, current family/cell/trial, phase, elapsed time,
honest ETA range, failures, resource pressure, and last meaningful event. Avoid
chart animation that makes provisional data appear authoritative. Verify SSE
disconnect and reconnect states are distinct from run failure.

The event log should be secondary until something goes wrong. Cancellation copy
must explain evidence retention and teardown without exposing process internals.

#### Scientific report

Ensure the first report view communicates:

- correctness verdict;
- research question;
- varied and controlled factors;
- primary result with sample size and interval;
- noise/distribution shape;
- resource consequence;
- limitations and comparability.

Do not let seven tabs become a place to hide poor hierarchy. Challenge whether
Summary, Results, Distributions, Resources, Correctness, Methods, and Data are
the right labels and order. Preserve direct access to methods and raw evidence.

For every chart verify metric definition, unit, `n`, failures, control, interval,
raw points, and table alternative. Reject rainbow palettes, dual axes without a
compelling reason, chart legends far from data, and histograms with arbitrary
bins. Keep tooltips supplementary.

#### Compare

Compatibility must be understood before performance deltas. Show which checks
passed, which failed, and why a mismatch matters. “Show side by side anyway”
must visibly change the result to descriptive-only and suppress a regression
verdict.

Challenge whether reference/candidate selection, matched-cell scope, and percent
change direction are obvious. Never rely on red/green alone to mean worse/better.

### 5. Audit friendliness and copy

Replace internal or ambiguous copy with concise user-facing language while
retaining exact technical detail nearby.

Examples of the desired pattern:

| Avoid as primary label | Prefer | Preserve in supporting detail |
|---|---|---|
| `create_workspace_session` | Create workspace | Internal operation name |
| `N` | Live sessions | Symbol `N` in methods/results |
| `W` | Remount parallelism | Effective `remount_sweep_width` |
| `B` | Squashable blocks | Symbol `B` |
| `M` | Migrated sessions | Observed `M`, not requested |
| Cartesian product | Test combinations | Exact cell expansion formula |
| destructive operation | Publishes or replaces test state | Isolation and cleanup policy |

Review button verbs, field descriptions, warnings, empty states, errors, and
completion messages. Prefer “Review 18 test combinations” over “Submit plan.”
Never use “something went wrong” when the system has an actionable cause.

### 6. Audit visual hierarchy

Inspect these failure modes explicitly:

- every region rendered as the same card;
- too many borders or nested surfaces;
- oversized page titles pushing evidence below the fold;
- weak distinction between labels, values, units, and methods notes;
- dense forms without alignment or grouping;
- sticky panels covering content;
- status badges used as decoration;
- monospace used for paragraphs rather than identifiers and values;
- inconsistent column widths across related tables;
- empty whitespace beside an overcrowded control column;
- dashboard-wide color noise competing with correctness failures;
- desktop layout merely scaled down on mobile;
- mobile horizontal scrolling outside deliberate data-table/chart containers.

Use the established visual direction unless evidence supports a specific change:

- light canvas `#F6F7F9`;
- white surfaces `#FFFFFF`;
- primary text `#101828`;
- secondary text `#475467`;
- border `#D0D5DD`;
- instrument navy `#17324D`;
- experimental blue `#2563EB`;
- success `#16845B`;
- warning `#B7791F`;
- failure `#C2413B`;
- Fira Sans for interface text and Fira Code for values/identifiers.

Recommend changes through Mantine theme tokens and component variants rather
than one-off inline colors and spacing.

### 7. Audit accessibility and interaction

Treat these as release blockers when violated:

- keyboard navigation follows visual order;
- focus is always visible;
- form fields have persistent labels and associated errors;
- icon-only actions have accessible names and tooltips;
- touch targets are at least 44 × 44 px;
- normal text contrast reaches 4.5:1;
- status never depends on color alone;
- reduced-motion preference is respected;
- loading controls disable duplicate submission and keep layout stable;
- live announcements are useful but not noisy;
- plots have table alternatives and keyboard-accessible inspection;
- dialogs trap and restore focus correctly;
- drawers and menus close predictably with Escape;
- narrow layouts preserve every scientific value and unit.

Use Mantine’s accessibility behavior instead of recreating focus traps or
keyboard interaction locally.

### 8. Audit implementation quality

Look for UI architecture that will undermine consistency:

- duplicated factor controls across family pages;
- page-local colors, radii, spacing, or status mappings;
- statistics recomputed differently in the browser;
- giant page components mixing queries, state, and rendering;
- needless global state or prop drilling through the entire shell;
- custom CSS that fights Mantine layout primitives;
- custom widgets duplicating Mantine behavior;
- unstable list keys, avoidable rerenders, or unvirtualized large logs;
- charts that resize incorrectly or leak event listeners;
- optimistic run states that disagree with backend state;
- ad hoc unit formatting or missing tabular numerals.

Prefer a small shared set of product components built on Mantine:

- `BenchmarkAppShell`
- `EnvironmentStrip`
- `StudyQuestionPicker`
- `ExperimentBuilder`
- `FactorControl`
- `PlanEstimateBar`
- `PlanReviewModal`
- `WorkspaceRootField`
- `RunProgressMatrix`
- `ScientificTable`
- `DistributionPlot`
- `ResourceTimeline`
- `CompatibilityPanel`

Do not demand abstraction before two real uses. If the current local component
is clearer than a generic framework, keep it.

## Required output

Return the review in this exact order.

### A. Executive verdict

In no more than ten sentences, state:

- whether the current UI is friendly, scientifically credible, and ready;
- the three most consequential problems;
- the single recommended layout direction;
- what should remain unchanged.

### B. Evidence reviewed

List routes, viewport sizes, states, screenshots, flows, and implementation files
actually inspected. State gaps explicitly.

### C. Layout decision

Show the three layout alternatives, desktop and narrow wireframes, weighted
score table, reasoning, and one selected winner.

### D. Prioritized findings

Use this table:

| Priority | Route/component | Evidence | User impact | Recommended change | Mantine implementation |
|---|---|---|---|---|---|

Priorities:

- `P0`: scientific or safety meaning is wrong; blocks release.
- `P1`: primary task is confusing, inaccessible, or error-prone; fix before v1.
- `P2`: meaningful usability, responsive, visual, or maintainability problem.
- `P3`: polish with measurable benefit; never include taste-only churn.

Every finding needs concrete evidence. Do not write “improve spacing” without
naming the region, current consequence, proposed token/layout, and expected
result.

### E. Recommended page system

Provide the final application shell and page-by-page hierarchy for all eight
route shapes. Include Mantine component choices and which information is above
the fold at desktop and mobile sizes.

### F. Component and theme plan

Provide:

- Mantine theme tokens and variants to add or reuse;
- shared product components to create, keep, merge, or delete;
- components that should remain local;
- exact places where TanStack Table/Virtual or uPlot is justified;
- dependencies that should not be added.

### G. Copy improvements

Provide a before/after table for unclear labels, descriptions, warnings, empty
states, errors, and actions. Keep exact scientific terms available through
supporting text and Methods.

### H. Responsive and accessibility acceptance matrix

For 375, 768, 1,024, and 1,440 px, specify navigation, builder, charts, tables,
sticky actions, and overflow behavior. Include keyboard, screen-reader, contrast,
reduced-motion, and chart-table checks.

### I. Implementation sequence

Propose the smallest coherent sequence of changes. Separate:

1. release blockers;
2. structural layout/component work;
3. data visualization and report work;
4. polish.

Name the files likely to change. Do not bundle a new design system, new charting
stack, and unrelated refactor into the same step.

### J. Final validation checklist

End with observable pass/fail criteria that another reviewer can verify from the
running application. Include screenshots, interaction tests, accessibility,
scientific semantics, visual regression, and absence of console errors.

## Review behavior constraints

- Be direct, specific, and evidence-based.
- Do not praise the UI before testing its main flows.
- Do not preserve a layout merely because it is already documented.
- Do not propose a redesign based only on personal taste.
- Do not remove advanced capability; reveal it progressively.
- Do not hide scientific caveats to make the interface look cleaner.
- Do not display backend names as the only user-facing language.
- Do not turn the central page into a grid of generic metric cards.
- Do not use a modal for work that needs side-by-side comparison or persistent
  context.
- Do not add dependencies when Mantine or a small local component already fits.
- Do not use hover-only explanations for required information.
- Do not calculate statistical results independently in the UI.
- Do not report a problem without a feasible implementation direction.
- When evidence is incomplete, label the conclusion as a hypothesis and state
  how to test it.

The final review should make it obvious which layout to build, why it is better
for users, how it preserves scientific rigor, and how to implement it cleanly
with Mantine.

