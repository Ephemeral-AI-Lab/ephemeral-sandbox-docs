# EphemeralOS Web Console UI/UX Design Proposal

Status: Design proposal; implementation pending approval  
Date: 2026-07-11  
Scope: React + Tailwind web console design and information architecture  

This document is a planning artifact. It does not authorize implementation,
dependency changes, or package.json changes.

## Evidence base

The initially requested nested decision-record path did not exist during the
audit. The decision record that was read was:

- /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/web-console-ui-tech-stack-and-library-options.md

The audit also covered the console package, tokens, local UI primitives, shell,
Fleet, sandbox Overview, Terminal, Observability, Files, Preview, API types,
frontend polling, and relevant backend response contracts.

The design is intentionally limited to data already supplied by those
contracts. In particular, the Fleet must not imply sandbox owner, creation
time, region, TTL, labels, or last activity because SandboxRecord does not
provide those fields.

## 1. Executive recommendation

Retain the current React 19, Tailwind CSS v4, local Radix wrapper, Lucide,
React Router, TanStack Query, TanStack Virtual, CodeMirror, and uPlot
architecture.

The design priority is trust before density:

1. Correct event, trace, polling, terminal, file-conflict, and preview-safety
   issues.
2. Establish bounded page layouts and one explicit scroll owner per pane.
3. Redesign the Fleet and sandbox workspace around operator decisions.
4. Add TanStack Table for dense operational tables only after approval.
5. Add React Aria Components selectively for high-cardinality pickers and
   semantic trees only after approval.

The revised Fleet direction is:

- Do not show layers anywhere on Fleet.
- Remove the layer count from the Fleet summary.
- Remove Squash and its layer count from SandboxCard.
- Keep Squash inside the sandbox's Observability > Layers view.
- Make each card answer, in order: Which sandbox? Is it usable? Is work
  running? What is its current resource signal? What should I do next?

The canonical sandbox navigation should be:

- Overview
- Terminal
- Files
- Observability
- Preview

Layers should live only under Observability. The duplicate top-level Layer
Stack route should redirect to the Observability route.

Before visual polish, correct these trust-critical defects:

- Event range durations are sent where the backend expects absolute time.
- Trace attached-event data is typed differently from the backend payload.
- Terminal Ctrl-C and Ctrl-D can be written twice.
- Publication rejection can appear as success.
- Transcript caches can collide across sandboxes.
- File conflict handling can lose the operator's draft.
- Preview content is same-origin and loaded in an unsandboxed iframe.
- Fleet cards can remain stale while the summary refreshes.
- Ready sandboxes with active work never enter fast snapshot polling.

## 2. Current UI surface map

| Surface | Operator task | Current evidence and limitation |
|---|---|---|
| Shell | Move between Fleet and a sandbox | Compact header and breadcrumbs exist, but child pages create competing scroll regions. |
| FleetBoard | Find and open a sandbox | Slow and conditional fast lists can disagree; initial loading can look blank. |
| FleetSummaryBar | Understand Fleet state | Currently a wrapped sentence with total, lifecycle states, commands, memory, and layers. Layers must be removed. |
| SandboxCard | Decide which sandbox to enter | Identity, workspace, activity, sparklines, Squash, Open, and Destroy compete inside the same card. |
| Creation | Choose image/workspace and follow progress | Catalog-driven form and streamed progress exist. |
| WorkspacePicker | Select a host directory | Browses up to 500 child directories with no search, typeahead, or collection semantics. |
| SandboxHeader | Confirm identity, lifecycle, health, and actions | Identity, endpoints, metadata, and actions share one wrapping row. |
| OverviewTab | Assess readiness and active work | Raw record, resources, sessions, and in-flight panels exist, but query states are not distinct. |
| TerminalTab | Launch and investigate commands | Browser-local history, per-command polling, fixed sidebar, and a one-row composer. |
| Resources | Diagnose CPU, memory, I/O, and disk | Four uPlot charts; plot recreation and incomplete loading/accessibility treatment. |
| Events | Filter operational events | Manual live table; incorrect time semantics; pause does not pause. |
| Traces | Find the slow or failing span | Trace list is inferred from 200 recent events; fixed-width waterfall layout. |
| Layers | Investigate stack, leases, mounts, and paths | Appears in two navigation locations; no canonical route. |
| Files | Navigate and read/edit files | Fixed tree, CodeMirror, windowed reads, and opaque line-owner blame. |
| Preview | View an HTTP service | Manual scope, port, and path; same-origin iframe security decision unresolved. |

## 3. Prioritized UX opportunity matrix

Effort uses S, M, and L. Dependency risk describes new-package or backend
contract risk.

| Priority | Surface | User decision and evidence-based problem | Impact / effort / dependency | Work type |
|---|---|---|---|---|
| P0 | Events | The selected time range does not produce the requested backend range; Tail off still polls. | High / S / Low | Frontend |
| P0 | Traces | Attached event markers consume the wrong response shape. | High / S / Low | Frontend contract fix |
| P0 | Terminal controls | A single Ctrl-C or Ctrl-D can produce two stdin writes. | High / S / Low | Frontend |
| P0 | Terminal outcome | Publication rejection and authoritative result metadata are discarded. | High / M / Low | Frontend |
| P0 | Terminal isolation | Transcript cache is keyed only by command ID, which can repeat across sandboxes. | High / S / Low | Frontend |
| P0 | File editing | Conflict mode can replace the local draft with server content. | High / M / Low | Frontend; backend CAS for full safety |
| P0 | Preview | Untrusted app content shares the console origin in an unsandboxed iframe. | High / M-L / High | Frontend mitigation plus backend or deployment decision |
| P1 | Fleet data trust | Fast cached card data can be preferred after fast polling stops while the summary uses the slow list. | High / S / Low | Frontend query |
| P1 | Fleet summary | A prose-like flex row is difficult to scan and currently elevates layers. | High / S / Low | Frontend |
| P1 | SandboxCard | Too many equally weighted details and actions; layer maintenance distracts from operational entry. | High / M / Low | Frontend |
| P1 | Creation and picker | The directory picker truncates at 500 and lacks search, keyboard collection behavior, and robust dialog bounds. | High / M / Medium | Frontend now; package/API later |
| P1 | Header and Overview | Identity, endpoints, actions, lifecycle, and resources compete; loading, unavailable, stale, and error are conflated. | High / M / Low | Frontend |
| P1 | Snapshot polling | Fast mode can never be selected for ready sandboxes with active work. | High / S / Low | Frontend query |
| P1 | Terminal layout | Fixed sidebar and composer overflow; stale history filter doubles as execution target. | High / M / Low | Frontend |
| P1 | Terminal transcript | Wrapped lines violate fixed virtual height; polling errors are silent and scale per expanded command. | High / M / Low | Frontend |
| P1 | Command audit | Ledger is browser-local and an unknown command can look like empty success. | High / M / Medium-High | Mixed |
| P1 | Events table | Missing responsive containment, column state, robust query states, and virtualization. | High / M / Medium | TanStack Table plus existing Virtual |
| P1 | Trace investigation | No complete trace index; sidebar and waterfall do not adapt. | High / M / Medium | Mixed |
| P1 | Layer investigation | Duplicate IA, local trend history, hidden sharing IDs, and unlinked changed paths. | High / M / Low-Medium | Mostly frontend |
| P1 | Files | Fixed tree and non-semantic recursive controls; listing truncates without a cursor. | High / M-L / Medium | Mixed |
| P1 | File viewer | CodeMirror recreation, weak request cancellation, mouse-only blame, and large-file edit inefficiency. | High / M / Low-Medium | Mixed |
| P2 | Resources | uPlot is recreated on polling updates and lacks a numerical accessibility alternative. | Medium-High / M / Low | Frontend |
| P2 | Logs | Forced tail, unbounded rows, and no pause, copy, wrap, or durable history. | Medium / M / Low-High | Mixed |
| P2 | Preview ergonomics | Toolbar and status treatment are weak at narrow widths. | Medium / M / Low | Frontend after security decision |

## 4. Recommended UI technology combination

Use one coherent combination:

### Component policy

- **TanStack Table for operational tables.** Use it for dense, stateful data
  surfaces that need sorting, column visibility, expansion, and stable row
  behavior during polling. Events is the first adoption target.
- **React Aria Components for complex accessible collections.** Use it
  selectively for collection behavior such as the WorkspacePicker and
  FileTree, including keyboard navigation, focus management, selection,
  typeahead, and accessible semantics.
- **TanStack Virtual for long live data.** Retain it for terminal transcripts
  and use it for high-volume event rows or flattened visible tree nodes when
  measured volume warrants virtualization.

Tailwind CSS and the existing local Radix wrappers continue to own all visual
styling and ordinary controls. These three libraries supply specialized
behavior; they do not introduce a second component theme.

| Layer | Recommendation | Boundary |
|---|---|---|
| Application | React 19, React Router, TanStack Query | Retain current route and query architecture. |
| Styling | Tailwind CSS v4 and existing tokens | No CSS-in-JS, new reset, or competing theme provider. |
| Primitives | Existing local Radix wrappers | Continue local buttons, dialogs, selects, tabs, popovers, tooltips, and toasts. |
| Operational tables | TanStack Table | Use for dense operational tables; Events is the first justified adoption. Dependency installation remains implementation-gated. |
| Complex accessible collections | React Aria Components | Use selectively for WorkspacePicker and FileTree-class collections. Dependency installation remains implementation-gated. |
| Long live data | TanStack Virtual | Retain for Terminal and use for Events or flattened visible tree nodes when measured volume warrants it. |
| Code and charts | CodeMirror and uPlot | Keep; stabilize instance lifetime, resizing, and data updates. |
| Icons | Lucide | Preserve the current icon language. |

These behavior libraries must remain visually headless:

- TanStack Table owns column, sort, and row state, not presentation.
- React Aria must not install a global visual theme.
- Existing local wrappers remain the only visual component vocabulary.
- Do not add a shadcn/ui package dependency; the repository already uses
  shadcn-style local composition.

Do not adopt Mantine, PrimeReact, Radix Themes, or individual controls from a
full component suite. Each would create a second visual system with different
spacing, focus, state, and theme behavior.

The UI/UX design review reinforced stable hover treatment, focus visibility,
responsive containment, reserved loading space, reduced motion, and keyboard
navigation. Generic palette, typography, horizontal-journey, and marketing
patterns were rejected because they conflict with the existing compact,
light, operator-console language.

## 5. Layout and responsive blueprints

### Shared frame

Breakpoints:

- Below 768px: single-column content; secondary panes become drawers or accordions.
- 768px to 1023px: primary content remains full width; secondary investigation panes are on demand.
- 1024px and above: persistent split-pane workspaces.
- 1280px and above: three-column Fleet cards and optional detail panels.

Macro recipe:

- Shell: <code>grid h-dvh min-h-0 grid-rows-[2.75rem_minmax(0,1fr)] overflow-hidden</code>
- Header: Flex with <code>min-w-0</code> and breadcrumb truncation.
- Main: <code>min-h-0 min-w-0 overflow-hidden</code>.
- The active route owns scrolling; the document body does not.
- Fixed viewport toolbars are avoided. Persistent controls occupy explicit
  grid rows within the workspace.

### 5.1 Fleet overview — revised

Fleet must not show layers, layer counts, or Squash actions.

~~~text
┌ EphemeralOS / Fleet ─────────────────────────────────────────┐
├ [Total] [Ready] [Transitioning] [Running commands] [Memory]  ┤
├ Search ID or workspace   All Ready Creating Failed    New    ┤
├───────────────────────────────────────────────────────────────┤
│ ┌ sandbox-alpha ─────────── Ready • reachable ─────────── ⋯ ┐ │
│ │ /Users/team/project-alpha                                 │ │
│ │                                                           │ │
│ │  2 sessions              1 command running                │ │
│ │  CPU activity  ▁▂▅▃      Memory  742 MiB  ▁▂▂▃            │ │
│ │                                                           │ │
│ │  Updated 3s ago                     Open       Terminal    │ │
│ └───────────────────────────────────────────────────────────┘ │
│                                                               │
│ ┌ sandbox-beta ─────────── Creating ────────────────────────┐ │
│ │ /Users/team/project-beta                                  │ │
│ │ Creating runtime…                                         │ │
│ │ latest progress line                                      │ │
│ │                                             View progress  │ │
│ └───────────────────────────────────────────────────────────┘ │
│                  card region scrolls                         │
└───────────────────────────────────────────────────────────────┘
~~~

#### Summary

Use supported, actionable values only:

- Total sandboxes
- Ready
- Transitioning, derived from creating plus stopping
- Running commands
- Aggregate current memory

Do not show:

- Layers
- Storage stack depth
- Region, owner, age, TTL, or labels
- A synthetic health score

Recipe:

- Root: <code>grid h-full min-h-0 grid-rows-[auto_auto_minmax(0,1fr)]</code>.
- Summary: <code>grid grid-cols-2 gap-px md:grid-cols-3 xl:grid-cols-5</code>.
- Each summary cell has one label, one value, and reserved loading height.
- The summary and cards use the same authoritative sandbox list generation.

#### Toolbar

- Search matches ID and workspace root, both already present in SandboxRecord.
- State filters: All, Ready, Creating, Stopping, Failed, Stopped.
- Keep the primary New Sandbox action at the end.
- Do not add owner, region, age, or tag filters without backend fields.

Recipe:

- <code>flex min-w-0 flex-wrap items-center gap-2</code>.
- Search: <code>w-full sm:w-80</code>.
- State filters use a horizontally scrollable segmented row below 375px rather
  than shrinking labels.

#### Redesigned SandboxCard

The card hierarchy is:

1. Identity and lifecycle state.
2. Workspace context.
3. Active operational work.
4. Current CPU and memory signal.
5. Freshness.
6. Open and Terminal actions.

Header:

- Sandbox ID is the heading and main deep link.
- State and reachability remain textual; color is secondary.
- The overflow menu is reserved for destructive or infrequent actions.
- Do not put Destroy as an unlabeled 24px icon in the main action row.

Body:

- Workspace root is a single truncated mono line with full value available to
  copy or inspect.
- Activity uses plain language: “2 sessions” and “1 command running.”
- Running command count receives the strongest accent because it is the most
  immediate operational signal.
- CPU activity and memory occupy a quiet two-column resource strip.
- CPU uses the existing activity series rather than inventing a precise
  percentage. Memory may show the current mem_cur value when available.
- Freshness comes from the snapshot sampling time when available.

Footer:

- Open is the primary action.
- Terminal is the single contextual quick action.
- Squash is removed from Fleet.
- Destroy moves to a labelled overflow/menu confirmation path, or remains in
  sandbox detail if an overflow pattern is not implemented.

Visual behavior:

- White surface, existing border and tokens.
- No lift, scale, or positional movement on hover.
- Hover changes border and subtle shadow only.
- Active commands may add a narrow accent edge or soft status chip, never a
  fully tinted card.
- Card heights remain consistent within a row.

Responsive recipe:

- Card region: <code>grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3</code>.
- Card: <code>grid min-w-0 grid-rows-[auto_auto_1fr_auto]</code>.
- Resource strip: <code>grid grid-cols-2 gap-2</code>.
- Footer: Flex on desktop; at very narrow card widths use a two-column Grid for
  full-width actions.

Card variants:

- Ready and idle: neutral card, “No commands running.”
- Ready and active: running count highlighted; transcript/output is not shown
  on Fleet.
- Creating: replace resources with a stable progress block and the latest
  progress line; detailed logs open on demand.
- Stopping: disable entry actions and show current transition.
- Failed: inline failure explanation, Inspect primary, Destroy secondary.
- Stopped: muted state with Inspect or Destroy only, according to supported actions.
- Snapshot stale/error: keep last values, add “Stale” or “Unavailable”; never
  turn missing values into zero.

Fleet states:

- Initial loading: summary and card skeletons with stable height.
- Background refresh: retain cards and show updating or stale state.
- Error with stale data: retain cards plus an inline retry banner.
- First-use empty: creation explanation and New Sandbox action.
- Filtered empty: active filter summary and Clear filters.
- Creation failure: keep the failed progress card visible.

### 5.2 Sandbox detail workspace

~~~text
┌ Fleet / sandbox-id                                  Actions ┐
│ sandbox-id  Ready  Reachable  /workspace/root                │
├ [CPU] [Memory] [Workspaces] [Running] [Sampled]             ┤
├ Overview | Terminal | Files | Observability | Preview        ┤
├──────────────────────────────────────────────────────────────┤
│ Active tab: one bounded content region                       │
└──────────────────────────────────────────────────────────────┘
~~~

Layers are intentionally absent from the top-level stats and navigation.
Storage and Layers remain in Observability where they can be investigated with
the proper context.

Recipe:

- <code>grid h-full min-h-0 grid-rows-[auto_auto_auto_minmax(0,1fr)]</code>.
- Identity header:
  <code>grid min-w-0 gap-2 md:grid-cols-[minmax(0,1fr)_auto]</code>.
- Stat strip: <code>grid grid-cols-2 gap-2 sm:grid-cols-3 xl:grid-cols-5</code>.
- Tabs: Flex with <code>overflow-x-auto</code>.
- Content: <code>min-h-0 min-w-0 overflow-hidden</code>.
- Overview:
  <code>grid gap-3 overflow-y-auto lg:grid-cols-[minmax(0,1.1fr)_minmax(20rem,.9fr)]</code>.

Lifecycle, availability, errors, sessions, active executions, CPU, memory, and
sample freshness come first. Raw endpoints and record data belong in a
secondary Details disclosure.

### 5.3 Terminal and command workspace

~~~text
┌ Sessions 15rem ┬ Scope/status · 2 running · updated now ┐
│ All commands   ├─────────────────────────────────────────┤
│ workspace-a    │ Command ledger — this region scrolls    │
│ workspace-b    │ command / target / outcome / duration   │
│                │ ┌ transcript, bounded x/y scroll ┐      │
│ rail scrolls   │ └ stdin · status · jump latest ──┘      │
│                ├─────────────────────────────────────────┤
│                │ target / timeout                        │
│                │ $ command…                         Run  │
└────────────────┴─────────────────────────────────────────┘
~~~

Desktop recipe:

- <code>grid h-full min-h-0 min-w-0 lg:grid-cols-[15rem_minmax(0,1fr)] lg:grid-rows-[auto_minmax(0,1fr)_auto]</code>.
- Sidebar: hidden below lg, otherwise spans all three rows.
- Ledger: <code>min-h-0 min-w-0 overflow-y-auto overscroll-contain</code>.
- Composer occupies the final grid row and is not viewport-fixed.
- Transcript:
  <code>h-[clamp(16rem,42vh,32rem)] min-w-0 overflow-auto</code>.
- Fixed virtual rows use preserved, non-wrapped line geometry. Optional
  wrapping requires dynamic measurement.

Below lg, Sessions opens in a left Radix drawer. Below md, composer controls
use a two-row Grid. History filtering and execution target selection are
separate controls.

Collapsed command rows show command, actual workspace, status, exit and
publication outcome, duration, and time. Expanded rows add transcript state,
stdin, IDs, Copy, Prefill or Rerun, and only valid contextual links.

### 5.4 Observability and auditability

~~~text
┌ Resources | Traces | Events | Layers                    ┐
├ Scope/filter controls                  Live · updated 2s ┤
├──────────────────────────────────────────────────────────┤
│ Active investigation surface                             │
└──────────────────────────────────────────────────────────┘
~~~

Resources:

- <code>grid h-full min-h-0 grid-rows-[auto_minmax(0,1fr)]</code>.
- Charts: <code>grid min-w-0 gap-3 md:grid-cols-2</code>.
- Add latest, minimum, and maximum text summaries.
- Retain chart height during loading.
- Keep uPlot instances and update data with setData.

Events:

- Use a toolbar plus bounded table viewport.
- TanStack Table owns sorting, column visibility, and expansion.
- TanStack Virtual handles high live row counts.
- Under md, show time, event, and trace as a compact summary; details open
  below or in a drawer.
- Live polls; Paused stops polling.

Traces:

- Desktop:
  <code>grid h-full min-h-0 grid-cols-[clamp(14rem,22vw,19rem)_minmax(0,1fr)]</code>.
- Waterfall content uses a minimum inner width and explicit horizontal scroll.
- Under lg, trace selection becomes a drawer or combobox.
- Virtualize the flattened visible span tree.

Layers:

- Canonical home is Observability > Layers.
- Desktop:
  <code>grid min-h-0 grid-cols-1 gap-3 xl:grid-cols-[minmax(0,1fr)_20rem]</code>.
- Details stack below at smaller widths.
- Display available shared workspace IDs.
- Changed file paths may link to the current Files view with explicit “current
  file” wording.
- Do not expose Layers on Fleet.

Supported investigation links:

| From | To | Status |
|---|---|---|
| Event trace ID | Trace | Explicit |
| Event parent span ID | Selected span | Frontend-only route state |
| Blame operation request ID | Trace | Existing owner convention |
| Blame workspace session ID | Terminal filter | Existing convention; history may be absent |
| Layer changed file path | Current Files path | Frontend-only; not historical layer content |
| New caller-supplied RPC request ID | Trace | Frontend can support future actions |

Do not imply command-to-trace, command-to-layer, trace-to-file, or
layer-to-operation relationships unless an explicit key is present.

### 5.5 File workspace

~~~text
┌ scope / Files ┐┌ breadcrumb / path ─── Blame · Edit/Save ┐
│ repository    ││ code viewer / editor                    │
│ tree          ││ line │ owner │ content                  │
│ tree scrolls  │├ paging / conflict / status              │
└───────────────┘└──────────────────────────────────────────┘
~~~

Recipe:

- Desktop:
  <code>grid h-full min-h-0 grid-cols-[clamp(14rem,22vw,20rem)_minmax(0,1fr)]</code>.
- Tree and viewer each use <code>min-h-0 min-w-0</code>.
- CodeMirror and the tree are the scroll owners.
- Viewer header:
  <code>grid grid-cols-[minmax(0,1fr)_auto]</code>.
- Preserve code line geometry by default; Wrap is optional.
- Keep the CodeMirror instance, selection, viewport, undo history, and draft
  stable through paging and blame changes.
- Conflict state preserves both local draft and server content.

Below lg, the tree moves to a left drawer. Breadcrumb and current scope remain
visible after the drawer closes. Blame becomes an optional gutter or detail
drawer rather than compressing code.

### 5.6 Preview

~~~text
┌ scope ─ port ─ path ───────────── Refresh · Open tab ┐
├ network / security / loading status                  ┤
│                     iframe                           │
└──────────────────────────────────────────────────────┘
~~~

Recipe:

- <code>grid h-full min-h-0 grid-rows-[auto_auto_minmax(0,1fr)]</code>.
- Desktop toolbar uses Flex.
- Below md, use Grid with scope and port first, full-width path second, and
  actions third.
- Reserve the status row to avoid layout shift.
- Do not invest heavily in embedded-preview polish before approving the
  preview isolation model.

## 6. Flexbox versus Grid decisions

| Region | Layout | Reason |
|---|---|---|
| Application shell | Grid | Fixed header plus bounded content |
| Fleet summary | Grid | Repeated aligned stats |
| Fleet card region | Grid | Responsive repeated cards |
| SandboxCard internal sections | Grid | Stable header, body, resources, and footer |
| Headers and status rows | Flex | One-dimensional inline alignment |
| Toolbars and filters | Flex with wrapping | Natural control grouping |
| Metric strips | Grid | Comparable repeated values |
| Tabs | Flex | Ordered one-dimensional navigation |
| Terminal workspace | Grid | Sidebar, status, ledger, and composer |
| Command metadata | Flex | Inline state and action alignment |
| Resource dashboard | Grid | Two-axis chart composition |
| Trace and file split panes | Grid | Stable minmax-based columns |
| Layer operational rows | Grid | Repeated field alignment |
| Button groups | Flex | Ordered actions |
| Data table | Semantic table | Preserve semantics; Grid surrounds it |
| Drawers | Flex column | Header, scroll body, and footer |

## 7. Accessibility, keyboard, loading, polling, and performance

Accessibility:

- Add a skip link and semantic main region.
- Preserve visible focus and remove outline suppression.
- Use aria-current for active navigation and sessions.
- Use aria-expanded and aria-controls for folders, commands, events, and spans.
- FileTree supports Up, Down, Left, Right, Home, End, typeahead, and roving focus.
- Deep links move focus as well as scroll.
- Ctrl-C and Ctrl-D produce one RPC.
- Streamed lines are not individually announced; completion and failure are.
- Tooltips are never the sole accessible name.
- Narrow controls use touch-sized targets.
- Respect prefers-reduced-motion.
- Replace unmodified numeric tab shortcuts with documented modified shortcuts.

Contrast:

- Existing ink-faint is too weak for much of the current 10px and 11px
  essential text.
- Several status foreground and soft-background pairs also need review for
  normal-text WCAG AA.
- Preserve token names and the existing visual language, but recalibrate
  values or stop using faint/status colors for essential small text.

Every live surface distinguishes:

- Initial loading
- Fresh data
- Background refresh
- Paused
- Stale or retrying
- Error with retained data
- Error without data
- True empty
- Truncated or partial data

Polling and performance:

- Preserve the last good data and expose freshness.
- Do not reorder rows under keyboard focus.
- Hidden tabs pause or back off; focus performs bounded catch-up.
- Snapshot polling accelerates for actual active work.
- Fleet summary and cards share one authoritative list generation.
- Replace whole-payload JSON serialization fingerprints for large live data
  with revisions or surface-specific comparison.
- Consolidate or schedule per-command pollers.
- Virtualize only measured high-volume collections.
- Stable uPlot and CodeMirror instances receive incremental updates.
- Use ResizeObserver for charts and split panes.
- Abort stale file and trace requests.
- Cap or virtualize stream logs.
- Verify no body-level horizontal overflow at 375, 768, 1024, and 1440px.

## 8. Phased implementation plan and acceptance criteria

No implementation begins until this proposal is approved.

### Phase 0 — DESIGN.md and trust corrections

Create a repository DESIGN.md after approval containing the adopted tokens,
breakpoints, scroll rules, query states, drawer convention, table and tree
patterns, and component ownership.

Then fix without new dependencies:

- Event time and pause semantics.
- Trace attached-event shape.
- Duplicate terminal controls.
- Publication result metadata.
- Transcript cache isolation.
- File draft preservation.
- Fleet list consistency and snapshot polling.
- Preview isolation decision.

Acceptance:

- Last-five-minute fixtures use the correct absolute threshold.
- Trace markers render at backend offsets.
- One control gesture creates one stdin RPC.
- Publication rejection cannot appear successful.
- Cross-sandbox transcript leakage is impossible.
- File conflict never destroys the draft.
- Fleet cards and summary cannot disagree because of different list versions.
- Preview security has an approved policy.

### Phase 1 — Layout foundation and revised Fleet

- Convert Shell and sandbox workspace to bounded Grid.
- Canonicalize Layers under Observability.
- Add shared query states and freshness.
- Implement the revised Fleet summary and SandboxCard hierarchy.
- Remove Layers and Squash from Fleet.
- Establish the responsive drawer pattern.

Acceptance:

- Fleet summary contains Total, Ready, Transitioning, Running commands, and Memory only.
- SandboxCard contains no layer count or Squash action.
- A card answers identity, state, active work, resources, freshness, and next action in one scan.
- No card moves position on hover.
- Loading, stale, creating, failed, stopped, and filtered-empty states are distinct.
- No body overflow at target widths.
- Every active page has one intentional primary scroll owner.
- Full keyboard navigation and visible focus work without a pointer.

### Phase 2 — Frequent operator workflows

- Improve creation and WorkspacePicker ergonomics.
- Rebalance SandboxHeader and Overview.
- Implement responsive Terminal, resilient transcript, serialized stdin, and
  history privacy controls.
- Implement responsive Files, stable CodeMirror, and accessible blame.
- Stabilize resource charts.

Acceptance:

- Stale history filters cannot become command targets.
- Invalid timeout blocks submission with an associated error.
- Ten thousand lines and a ten-thousand-character line render without overlap.
- Failed stdin remains recoverable.
- File paging and blame preserve editor focus and viewport.
- Chart polling updates data without recreating plots.

### Phase 3 — Dependency-gated collections

Only after explicit package approval:

- Add TanStack Table and migrate Events.
- Retain TanStack Virtual for high-volume rows.
- Prototype React Aria in WorkspacePicker.
- Apply semantic React Aria tree behavior to a flattened FileTree if the
  prototype meets style and performance requirements.

Acceptance:

- No global theme or CSS system is introduced.
- Existing URL event filters remain shareable.
- Sorting, expansion, focus, and column state survive polling.
- Tree has full keyboard navigation and typeahead.
- New controls visually match local primitives.
- Bundle and runtime effects satisfy the decision-record thresholds.

### Phase 4 — Audit and backend-enabled capability

- Generate and store request IDs for new browser actions.
- Add event-to-span and layer-path-to-current-file navigation.
- Implement trace index, durable command history, atomic file save, pagination,
  and structured logs when backend contracts exist.

Acceptance:

- Links render only from explicit identifiers.
- Expired targets explain absence.
- Unknown command IDs cannot appear successful.
- Atomic save rejects stale revisions without losing the draft.

## 9. Backend and API gaps or open questions

| Gap | Current evidence | Required decision or contract |
|---|---|---|
| Preview isolation | Same-origin iframe without sandbox | Iframe restrictions versus a dedicated untrusted origin |
| Command history | Browser-local ledger; active snapshot has only execution ID, operation, and lifecycle | Paginated, redacted, authorized history with timestamps and outcomes |
| Missing command | Unknown transcript can appear as empty OK | Explicit not-found or expired response |
| Trace enumeration | UI infers trace IDs from recent events | Trace index with time, duration, root operation, and status |
| Future correlations | Backend accepts caller request ID; browser omits it | Frontend support now; documented durable backend correlations later |
| Command to layer or file | No explicit keys in CommandOutput | Add only if required by product investigation goals |
| Atomic file write | No revision, hash, or ETag precondition | CAS token and conflict response |
| Directory and layer pagination | Truncated flag but no cursor | Cursor and optional search |
| File metadata | Name, kind, size; blame range and opaque owner only | Add mtime, mode, revision, timestamp, or layer only if required |
| Durable logs | Current operation logs are client-held text | Structured history with time, severity, request ID, paging, and retention |
| Retention | Links may point to absent trace or log data | Document retention and return expired state |
| Port discovery | No listening-port inventory | Optional endpoint if manual entry proves costly |
| Rich Fleet filtering | No owner, age, TTL, region, or labels | Do not design these filters without a product requirement and API |
| Layer trend and sharing | Backend data exists but frontend omits or reduces it | Frontend type and presentation correction |

Until those contracts exist, the UI must not imply:

- An existing command has a trace.
- A layer belongs to a particular command or operation.
- Current file content is historical content from a selected layer.
- Blame includes timestamp, revision, layer, or structured actor.
- Arbitrary trace and event attributes form a stable relationship schema.
