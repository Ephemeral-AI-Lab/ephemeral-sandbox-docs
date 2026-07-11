# EphemeralOS Web Console UI/UX Design Proposal

Status: Design proposal; implementation pending approval
Date: 2026-07-11
Scope: Complete Mantine migration, console information architecture, and operator workflows

This document is a planning artifact. It does not authorize implementation,
dependency installation, source-code changes, or `package.json` changes.

## Evidence base

The audit covered:

- The current console package, `src/index.css`, local UI wrappers, shell, Fleet,
  sandbox pages, API types, polling code, and relevant backend response contracts
  under `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/web/console`.
- The existing technology decision record at
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-docs/implementation-plan/web-console/web-console-ui-tech-stack-and-library-options.md`.
- Current official Mantine 9.4.1 documentation for React compatibility,
  installation, theming, responsive styles, overlays, accessibility, tables,
  trees, comboboxes, scrolling, notifications, and testing.
- The canonical 1024x1024 RGBA console logo at
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/web/console/dist/assets/images/logo.png`,
  used as the visual source for the Mantine theme.

The proposal is intentionally limited to data already supplied by audited
contracts. In particular, Fleet must not imply sandbox owner, creation time,
age, region, TTL, labels, or last activity because `SandboxRecord` does not
provide those fields.

## 1. Executive recommendation

Migrate the entire web console to Mantine as the sole application-wide UI
component and visual system. This is an incremental replacement under one
committed end state, not a permanent coexistence model.

Mantine must own:

- Colors, typography, spacing, radii, shadows, breakpoints, focus treatment,
  reduced-motion behavior, and component variants.
- Ordinary controls, forms, navigation, feedback, panels, tables, trees,
  overlays, drawers, modals, tooltips, and notifications.
- The light-mode operator-console visual language across every route.

The migration must end with:

- No use of the local Radix wrappers or direct Radix imports.
- No competing application theme or global Tailwind token layer.
- No permanent Tailwind component styling. Temporary utilities are allowed
  only on an explicit migration inventory and have a mandatory removal phase.
- One Mantine-owned component vocabulary across Fleet, sandbox detail,
  Terminal, Observability, Files, and Preview.

Retain React 19, React Router, TanStack Query, CodeMirror, uPlot, Lucide, and
TanStack Virtual. Adopt TanStack Table as the headless state engine for
operational tables, rendered entirely with Mantine components. Do not add
React Aria Components now: current Mantine Tree and Combobox APIs provide the
first implementation path and document virtualized integrations. The spike
must prove the complete required keyboard model, including Home, End,
typeahead, and focus continuity for virtualized `FlatTreeNode` rows. React
Aria may be reconsidered only if that prototype proves a specific
accessibility or collection-behavior gap that a local Mantine composition
cannot meet; it must never become a second visual system.

Mantine 9 requires React 19.2 or later. The console currently declares React
19.2.7, so the versions are compatible on paper, but the first implementation
step must still verify the exact registry versions, Vite/TypeScript build,
tests, style ordering, and bundle impact. All `@mantine/*` packages must use
the same exact version.

The product priority remains trust before density:

1. Correct event, trace, polling, terminal, file-conflict, and preview-safety
   defects without conflating those fixes with visual migration.
2. Establish the Mantine provider, theme, component defaults, bounded layouts,
   and one explicit scroll owner per pane.
3. Migrate every route and composition, then remove Radix and Tailwind.
4. Verify correctness, accessibility, responsive behavior, and live-data
   performance before declaring the migration complete.

Mantine adoption must preserve EphemeralOS's character: compact, light, calm,
desktop-first, and information-dense. IDs, commands, paths, hashes, timestamps,
and output remain monospace. Hover states remain stable, surfaces stay quiet,
and operational state is never reduced to generic dashboard decoration.

The cat-in-sandbox logo is the canonical brand anchor. Its warm ivory, sand,
wood, espresso, soft blush, and ice-blue palette should be recognizable in the
theme without turning the artwork into a page background or allowing brand
colors to obscure operational status semantics.

The revised Fleet direction remains:

- Do not show layers anywhere on Fleet.
- Remove the layer count from the Fleet summary.
- Remove Squash and its layer count from `SandboxCard`.
- Keep Squash inside the sandbox's Observability > Layers view.
- Make each card answer, in order: Which sandbox? Is it usable? Is work
  running? What is its current resource signal? What should I do next?

The canonical sandbox navigation remains:

- Overview
- Terminal
- Files
- Observability
- Preview

Layers live only under Observability. The duplicate top-level Layer Stack
route should redirect to the canonical Observability route while preserving
existing deep-link compatibility.

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
contract risk, not migration priority.

| Priority | Surface | User decision and evidence-based problem | Impact / effort / dependency | Work type |
|---|---|---|---|---|
| P0 | Events | The selected time range does not produce the requested backend range; Tail off still polls. | High / S / Low | Frontend correctness |
| P0 | Traces | Attached event markers consume the wrong response shape. | High / S / Low | Frontend contract fix |
| P0 | Terminal controls | A single Ctrl-C or Ctrl-D can produce two stdin writes. | High / S / Low | Frontend correctness |
| P0 | Terminal outcome | Publication rejection and authoritative result metadata are discarded. | High / M / Low | Frontend correctness |
| P0 | Terminal isolation | Transcript cache is keyed only by command ID, which can repeat across sandboxes. | High / S / Low | Frontend correctness |
| P0 | File editing | Conflict mode can replace the local draft with server content. | High / M / Low | Frontend; backend CAS for full safety |
| P0 | Preview | Untrusted app content shares the console origin in an unsandboxed iframe. | High / M-L / High | Frontend mitigation plus backend or deployment decision |
| P1 | Fleet data trust | Fast cached card data can be preferred after fast polling stops while the summary uses the slow list. | High / S / Low | Frontend query |
| P1 | Fleet summary | A prose-like flex row is difficult to scan and currently elevates layers. | High / S / Low | Frontend composition |
| P1 | SandboxCard | Too many equally weighted details and actions; layer maintenance distracts from operational entry. | High / M / Low | Frontend composition |
| P1 | Creation and picker | The directory picker truncates at 500 and lacks search, keyboard collection behavior, and robust dialog bounds. | High / M / Medium | Frontend now; API later |
| P1 | Header and Overview | Identity, endpoints, actions, lifecycle, and resources compete; loading, unavailable, stale, and error are conflated. | High / M / Low | Frontend composition |
| P1 | Snapshot polling | Fast mode can never be selected for ready sandboxes with active work. | High / S / Low | Frontend query |
| P1 | Terminal layout | Fixed sidebar and composer overflow; stale history filter doubles as execution target. | High / M / Low | Frontend composition |
| P1 | Terminal transcript | Wrapped lines violate fixed virtual height; polling errors are silent and scale per expanded command. | High / M / Low | Frontend behavior |
| P1 | Command audit | Ledger is browser-local and an unknown command can look like empty success. | High / M / Medium-High | Mixed |
| P1 | Events table | Missing responsive containment, column state, robust query states, and virtualization. | High / M / Medium | TanStack Table + Mantine Table + existing Virtual |
| P1 | Trace investigation | No complete trace index; sidebar and waterfall do not adapt. | High / M / Medium | Mixed |
| P1 | Layer investigation | Duplicate IA, local trend history, hidden sharing IDs, and unlinked changed paths. | High / M / Low-Medium | Mostly frontend |
| P1 | Files | Fixed tree and non-semantic recursive controls; listing truncates without a cursor. | High / M-L / Medium | Mixed |
| P1 | File viewer | CodeMirror recreation, weak request cancellation, mouse-only blame, and large-file edit inefficiency. | High / M / Low-Medium | Mixed |
| P2 | Resources | uPlot is recreated on polling updates and lacks a numerical accessibility alternative. | Medium-High / M / Low | Frontend behavior |
| P2 | Logs | Forced tail, unbounded rows, and no pause, copy, wrap, or durable history. | Medium / M / Low-High | Mixed |
| P2 | Preview ergonomics | Toolbar and status treatment are weak at narrow widths. | Medium / M / Low | Frontend after security decision |

## 4. Mantine application architecture

### 4.1 Ownership and end-state boundary

Mantine is the only component and theme system. Semantic HTML, local CSS Grid
modules, and non-visual state or rendering engines remain valid integration
boundaries; they do not constitute a competing visual system.

| Layer | End-state decision | Ownership boundary |
|---|---|---|
| Application | React 19, React Router, TanStack Query | Preserve routes, URL state, server-state lifecycles, and cache behavior. |
| Visual system | MantineProvider and one EphemeralOS theme | Own every application token, component default, variant, focus rule, and responsive breakpoint. |
| Ordinary UI | Mantine Core | Inputs, buttons, navigation, feedback, surfaces, overlays, tables, trees, and layout primitives. |
| Forms | Mantine inputs plus `@mantine/form` | Own labels, descriptions, errors, validation state, and submission ergonomics; API mutation behavior remains application code. |
| Notifications | `@mantine/notifications` | One global host; product-specific error normalization and live-region policy remain custom. |
| Operational tables | TanStack Table + Mantine Table | TanStack owns headless row/column/sort/expansion state; Mantine owns semantic rendering and appearance. |
| Long live data | TanStack Virtual | Retain for transcripts and use for measured high-volume table/tree/span collections. |
| Code and charts | CodeMirror and uPlot | Retain their rendering engines; Mantine owns surrounding controls, surfaces, labels, and theme bridges. |
| Icons | Lucide | Retain one icon language; pass icons as Mantine sections or children with semantic labels. |
| Exceptional layout | Local CSS Modules | Only for minmax Grid, virtualizer geometry, and CodeMirror/uPlot containment; values come from Mantine variables. |

### 4.2 Mantine packages and responsibilities

Use the smallest complete first-party package set:

| Package | Responsibility | Decision |
|---|---|---|
| `@mantine/core` | Provider, styles, layout, inputs, navigation, surfaces, feedback, overlays, Table, Tree, ScrollArea, and accessibility primitives | Required |
| `@mantine/hooks` | Disclosure, media/reduced-motion, resize, focus, and interaction utilities where component state needs them | Required |
| `@mantine/form` | Form state, field validation, associated errors, and submit coordination for creation, command, preview, and filter forms | Required |
| `@mantine/notifications` | Global transient notifications and queue/limit behavior | Required |

Build-time CSS tooling is also explicit:

| Package | Provenance | Responsibility | Decision |
|---|---|---|---|
| `postcss` | General third-party build tool, explicitly included by Mantine's Vite guide | Run the CSS transformation pipeline | Required dev dependency if not already direct |
| `postcss-preset-mantine` | Unscoped Mantine preset documented by Mantine; its name alone is not the reason it is trusted | Provide Mantine mixins plus `rem`/`em` helpers for CSS Modules | Required dev dependency |
| `postcss-simple-vars` | General third-party plugin explicitly recommended by Mantine's responsive-style guide | Expose the five static breakpoint values to CSS Module media queries | Required dev dependency |

Do not add `@mantine/charts` because uPlot remains the resource-chart engine.
Do not add `@mantine/code-highlight` because CodeMirror remains the file and
code engine. `@mantine/modals` is unnecessary unless a later audit proves that
a centralized modal manager reduces real product complexity; Core `Modal` and
`Drawer` are sufficient for this proposal.

Official status must be verified from current Mantine documentation and source
ownership, not inferred from an npm scope or the word “Mantine.” The four
runtime packages above are documented first-party Mantine packages. The three
build tools are identified separately because two are general third-party
PostCSS packages and one is an unscoped Mantine preset. Packages such as
`mantine-react-table` and `mantine-datatable` are listed as community
extensions; they are not required or recommended here.

### 4.3 Compatibility and dependency spike

The implementation spike must:

1. Resolve one exact current Mantine 9.4.x version from the registry and pin
   every `@mantine/*` package to that same version. The documentation and
   registry patch number must be reconciled rather than mixed.
2. Confirm React 19.2.7, React DOM 19.2.7, Vite 8, TypeScript 6, Vitest, and the
   production build work together.
3. Import Core styles once and Notifications styles once, in documented order.
4. Render representative Button, input, Modal, Drawer, Tooltip, Table, Tree,
   virtualized `FlatTreeNode`, virtualized Combobox, notification, CodeMirror
   pane, and uPlot panel.
5. Verify the complete Tree and virtualized Tree keyboard model: Up, Down,
   Left, Right, Home, End, typeahead, selection, expansion, roving focus, and
   focus continuity as rows mount and unmount. Record any localized custom
   behavior needed before deciding whether React Aria has a proven role.
6. Verify portal stacking, focus restoration, scroll lock, reduced motion,
   CSS ordering, responsive CSS Modules, and bundle impact.
7. Remove the spike if it fails. Do not leave experimental packages or a
   second provider in the production tree.

### 4.4 MantineProvider, CSS reset, and global-style strategy

Create one root `MantineProvider` around the console. It supplies the single
theme, CSS variables, component defaults, and forced light color scheme. The
existing TanStack Query provider and BrowserRouter remain application
providers; the Radix Toast and Tooltip providers disappear as their consumers
are migrated. Render exactly one `Notifications` host inside MantineProvider.

Provider rules:

- Define the theme outside React render so polling cannot recreate it.
- Use `forceColorScheme="light"` until a separately designed and approved dark
  operator theme exists. Do not expose a nonfunctional color-scheme toggle.
- Keep global classes enabled for responsive visibility helpers.
- Evaluate React 19 inline-style deduplication for repeated responsive style
  props during the spike; do not use responsive inline props inside thousands
  of virtual rows.
- Use `env="test"` only for unit tests that intentionally disable portals and
  transitions. Browser tests must exercise production portal behavior.

CSS order and scope:

1. Import `@mantine/core/styles.css` once at the application root.
2. Import `@mantine/notifications/styles.css` once after Core styles.
3. Load one small application-global stylesheet after Mantine. It may define
   only document/root sizing, body overflow, skip-link placement, and shared
   containment required by CodeMirror, uPlot, virtualizers, and portal roots.
4. Use Mantine props, Styles API, component extensions, and CSS Modules for
   route-specific composition.
5. During migration, keep existing Tailwind utilities only on a checked-in
   route/component allowlist. No new Tailwind component style may be added.
6. After the last route migrates, remove `@import "tailwindcss"`, `@theme`, the
   Tailwind Vite plugin/configuration, obsolete tokens, page utility strings,
   and `cn` if it has no non-Tailwind use.

Mantine Core's global stylesheet and minimal reset become authoritative. Do
not layer a second reset or re-create Mantine component tokens in global CSS.

### 4.5 Theme and token mapping

The theme should translate the current console character and canonical logo
rather than accept Mantine defaults unchanged. The file at
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/web/console/dist/assets/images/logo.png`
is the canonical logo source. Its sampled palette anchors include espresso
`#271f1c`, warm cream `#e7dccc`/`#fefdfc`, sand and wood
`#c7976d`/`#d4b18d`, and eye blue `#68889e`/`#a1c3d7`. These are seeds for
complete Mantine color scales, not untested text or focus tokens; every applied
shade still requires contrast verification.

The existing file is in generated `dist` output. During implementation, the
same canonical pixels must be registered in a durable source/static asset
input so a clean build does not depend on a pre-existing `dist` tree. This
proposal neither moves nor modifies the asset.

| Concern | Current intent | Mantine-owned mapping |
|---|---|---|
| Canvas | `#f7f8fa` app background | Logo-derived warm ivory near the cream family, mapped through the theme and application CSS variable resolver |
| Surface | White cards and panes | Warm white `Paper`, `Card`, overlays, and input surfaces that remain visually distinct from the canvas |
| Hover | Quiet `#f1f3f6` | Light warm-neutral shade; no translation, scale, or saturated card wash |
| Border | `#e3e6eb` | One logo-compatible warm-neutral border used by panels, inputs, tables, and split boundaries |
| Primary text | `#1a1d21` | Espresso family anchored near `#271f1c` for essential text |
| Secondary text | `#57606d` | AA-verified taupe/charcoal for metadata |
| Faint text | `#8a93a2` is too weak in small text | Recalibrate; use only for nonessential decoration, never essential 10–11px labels |
| Accent/running | Blue `#2563eb` | Eye-blue scale derived from the logo; use darker AA-passing shades for links, actions, focus, and running state |
| Brand warm | Not currently explicit | Sand/wood/caramel scale for quiet highlights, selected neutrals, illustrations, and shell details; it is not automatically Warning |
| Brand blush | Not currently explicit | Restrained inner-ear blush for rare decorative emphasis only; it is not Danger or Error |
| Success | Green | Custom accessible green pair plus text/icon label |
| Warning | Amber/orange | Custom accessible amber pair plus text/icon label |
| Danger | Red | Custom accessible red pair for destructive/error states |
| Idle/unknown | Neutral gray | Textual state with neutral Badge/Indicator |
| Sans typography | Inter/system stack, 13.5px base | Theme font family and compact `xs`/`sm` sizes; preserve readable line height |
| Monospace | UI monospace/JetBrains fallback | `fontFamilyMonospace` for IDs, commands, paths, hashes, timestamps, metrics, and output |
| Spacing | Compact 4–24px rhythm | Theme scale centered on 4, 8, 12, 16, and 24px; avoid spacious SaaS defaults |
| Radius | Small, functional | Explicit 4–6px scale and compact default; avoid pill-shaped ordinary controls |
| Shadow | Subtle separation | Minimal overlay/panel shadows; no hover lift |
| Focus | Existing 2px blue outline | `focusRing: auto` plus a consistent 2px high-contrast `:focus-visible` treatment and offset; never `never` |
| Motion | Stable operational surfaces | Set `respectReducedMotion: true`; keep transitions short and non-positional |
| Breakpoints | Base, 768, 1024, 1280, 1440 | `xs: 30em`, `sm: 48em`, `md: 64em`, `lg: 80em`, `xl: 90em` |

Mantine breakpoint values used by responsive component props are runtime theme
values. CSS media queries cannot consume those variables, so the same values
must also be declared in the static PostCSS configuration used by CSS Modules.
A single test should detect drift between the two definitions.

### 4.6 Component defaults and variants

Define application-wide defaults through `theme.components` and component
extensions rather than repeating props on each screen:

- AppShell header and Image: render the canonical logo at a fixed 28–32px
  square with preserved aspect ratio and transparency; pair it with the
  EphemeralOS name without allowing either to crowd route context.
- Button and ActionIcon: compact desktop sizes, clear primary/default/subtle/
  danger hierarchy, no motion on hover, and touch-sized narrow-screen targets.
- Input family: consistent label, description, error, 32px compact desktop
  height, and larger narrow-screen hit area. Monospace is opt-in by content.
- Paper and Card: subtle border by default, restrained shadow, small radius.
- Badge: compact, text-first lifecycle semantics; color never acts alone.
- Tabs and NavLink: visible route selection, `aria-current` where applicable,
  stable widths, and horizontal containment on narrow screens.
- Tooltip: focus triggering enabled for informative tooltips, 300ms open delay,
  no hover-only essential content.
- Skeleton and Loader: reserved final dimensions and reduced-motion behavior.
- Modal and Drawer: semantic title required, focus trap/restoration retained,
  and predictable close policy.
- Table: compact cell padding, sticky header where bounded, tabular numbers,
  and responsive column priorities.

Product-specific components such as `StateBadge`, `CommandCard`, and query
state panels remain local compositions, but their visual parts must be Mantine
components and theme values.

### 4.7 Portals, overlays, notifications, and tooltips

- Use Mantine `Modal` for blocking dialogs and confirmations. Do not replace a
  Radix dialog with Mantine `Dialog`: Mantine documents `Dialog` as unsuitable
  for important accessible content because it lacks the modal behavior needed
  here.
- Use `Drawer` for narrow-screen secondary panes such as Sessions, FileTree,
  and trace selection. Preserve focus trap, Escape behavior, scroll lock,
  semantic title, and return focus.
- Use `Popover` and `Menu` only from semantic button targets. Never enable a
  hover-only Menu.
- Portal overlays to the document body under one theme-owned z-index scale.
  Test nested Popover/Menu content, body scroll lock, and bounded route panes.
- If polling removes the original overlay trigger before close, restore focus
  to the nearest deterministic route heading or region rather than the body.
- Use one `Notifications` host with a bounded visible limit. Preserve current
  RPC error normalization, details, dismissal, and de-duplication semantics.
- Mantine's current 9.4.1 Notification and Notifications documentation does
  not state a default live-region contract. Set and test explicit
  `role="status"` for routine feedback and `role="alert"` only for urgent
  failures. Keep actionable or durable failures inline.
- Do not notify on every poll or stream line. Announce concise completion,
  failure, freshness, connection, and destructive-action outcomes.
- Mantine Tooltip focus events are off by default; enable focus for informative
  tooltips, and keep every target's accessible name independent of the tooltip.

### 4.8 Integration boundaries

| Integration | Decision | Mantine boundary and constraint |
|---|---|---|
| React Router | Retain | Mantine Tabs, NavLink, Anchor, and Breadcrumbs render Router links; URLs, filters, redirects, and deep links remain authoritative. |
| TanStack Query | Retain | Query/mutation state feeds Mantine feedback components; polling must not remount providers, controls, or overlay triggers. |
| TanStack Table | Adopt and retain | Headless sort/filter/visibility/expansion/row state for Events and future operational tables; render with Mantine Table. Do not adopt a community “Mantine table” package. |
| TanStack Virtual | Retain | Own visible-range geometry for transcripts and measured high-volume table/tree/span lists; Mantine owns row content and styling. |
| Mantine Tree | Adopt | Use Tree for normal volume; use `flattenTreeData` + `FlatTreeNode` + TanStack Virtual for large visible trees. Preserve async loading, truncation, path navigation, and API boundaries. |
| Mantine Combobox | Adopt | Use searchable Combobox; use `useVirtualizedCombobox` + TanStack Virtual for WorkspacePicker and high-cardinality options. |
| React Aria Components | Do not add now | Reconsider only after a written failing parity test demonstrates a Mantine accessibility or collection gap. Any exception remains headless under Mantine visuals. |
| CodeMirror | Retain | CodeMirror owns its editor DOM and scroll viewport; Mantine owns toolbar, labels, panels, conflict UI, and theme bridge. Do not wrap it in a second ScrollArea. |
| uPlot | Retain | uPlot owns canvas/plot DOM; Mantine owns panel, legend, summaries, and theme-derived colors. Keep instances stable and update data incrementally. |
| Lucide | Retain | Use one stroke/icon language. Icon-only controls require an accessible label and adequate target. |

### 4.9 Testing and accessibility implications

- Unit-test components through a shared render helper with the production
  EphemeralOS theme. Provide the documented jsdom mocks for `matchMedia`,
  `ResizeObserver`, and `scrollIntoView`.
- `env="test"` may simplify focused unit tests by disabling portals and
  transitions, but it cannot prove production behavior.
- Browser tests must cover real portals, z-index, focus trap/restoration,
  Escape/outside-click policy, scroll lock, reduced motion, and narrow layouts.
- Run axe checks and keyboard scenarios on every migrated primitive and product
  composition. Mantine defaults do not replace application-level semantic,
  labeling, contrast, and live-region testing.
- Capture visual baselines at 375, 768, 1024, and 1440px under stable fixture
  data, including loading, stale, empty, error, active, and overlay states.

## 5. Component migration map

Complexity is L, M, or H and includes behavior migration, not only JSX changes.

| Component or composition | Current implementation | Proposed Mantine replacement or composition | Custom behavior that remains | Complexity | Accessibility or performance concern |
|---|---|---|---|---|---|
| Button | Local Tailwind native-button wrapper with four variants/two sizes | `Button`, `ActionIcon`, and `UnstyledButton` only for specialized semantics; theme-owned defaults/variants | Permission, loading, confirmation, and action semantics | L | Icon controls need labels; disabled/loading must remain perceivable |
| Brand logo | Canonical PNG exists only under generated `dist`; Shell currently has no logo | Mantine `Image` inside `AppShell.Header`, using the canonical logo asset | Durable asset registration, adjacent product name, and responsive route context | L | Fixed intrinsic box prevents layout shift; use meaningful alt when standalone and empty alt beside an equivalent product name |
| Input and textarea | Local compact native Input; ad hoc textareas | `TextInput`, `Textarea`, `NumberInput`, `Input.Wrapper` | API parsing, command/path validation, draft state | L-M | Preserve labels, descriptions, associated errors, and mobile target size |
| Select and combobox | Radix Select wrapper plus manual button lists | `Select` for small static sets; `Combobox`/`useVirtualizedCombobox` for searchable or large sets | URL state, option loading, execution scope, truncation | M | Stable option IDs, active descendant, keyboard selection, bounded DOM |
| Dialog | Local Radix Dialog wrapper | Mantine `Modal`, not Mantine `Dialog` | Confirmation copy, destructive policy, RPC details | M | Focus trap, title/description, Escape, scroll lock, and restoration |
| Drawer | Planned/route-specific custom behavior; no shared Mantine primitive | Mantine `Drawer` | Responsive pane state and selected item | M | Restore focus; avoid nested scroll lock and orphaned triggers |
| Popover | Local Radix Popover wrapper | Mantine `Popover` | Filter/help/content logic | L-M | Semantic trigger, dismissal, portal placement, collision behavior |
| Tooltip | Local Radix Tooltip with 300ms delay | Mantine `Tooltip` with focus events enabled through defaults | Concise supplemental labels | L | Tooltip never sole name; test keyboard and screen reader |
| Tabs | Routed links/manual styling; Radix Tabs dependency unused | Mantine `Tabs` with Router-driven value and link semantics | URL/deep-link ownership and canonical redirects | M | Selection and focus must follow routes; narrow overflow must be operable |
| Menu | Radix dependency unused; ad hoc action clusters | Mantine `Menu` | Destructive/action authorization and confirmations | L-M | No hover-only trigger; keyboard order and labels |
| Toast/notifications | Direct Radix ErrorToast with RPC normalization, cap, duration, dismiss | `@mantine/notifications` plus one host and product notification adapter | Error normalization, de-duplication, durable inline fallback | M | Explicit status/alert semantics; no poll/stream spam |
| Badge/status indicator | Local Tailwind StateBadge mappings and spans | Mantine `Badge`, `Indicator`, `ThemeIcon`, and Text composition | Lifecycle/command-state mapping remains authoritative | M | Never color-only; contrast at compact sizes |
| Card/panel | Raw article/section/div with Tailwind borders | Mantine `Card` or `Paper`, with `Stack`/`Group` | Sandbox hierarchy, operational content, and Fleet dimension bounds | M | Stable geometry during polling; no hover movement or large-screen stretching |
| Skeleton/loading state | Ad hoc pulse blocks, blanks, spinners | `Skeleton`, `Loader`, `Progress`, `Alert`, and the official `@mantine/core` `EmptyState` | Query-state classifier and retry actions | M | Reserve final geometry; give EmptyState titles the correct heading level; respect reduced motion |
| Table | Manual native Events table; no table engine | TanStack Table state rendered with Mantine `Table`; Virtual at measured volume | URL filters, polling, expansion, trace links | H | Semantic headers/sort state, focus stability, sticky/virtual row integration |
| Tree/FileTree | Recursive non-semantic buttons; first 2,000 entries | Mantine `Tree`; large view uses `flattenTreeData`, `FlatTreeNode`, and TanStack Virtual | Async directory loading, truncation, selection, path fetch, plus localized Home/End/typeahead/focus behavior if the spike finds gaps | H | Prove the full keyboard model for normal and virtual trees; stable IDs, virtual focus, cursor gap |
| WorkspacePicker | Radix Dialog with up to 500 directory buttons and no search | Mantine `Modal` + searchable virtualized `Combobox`/Tree composition + `ScrollArea` viewport | Parent navigation, selected path, API limit, permission errors | H | 500-result truncation must be explicit; typeahead and focus restoration |
| Breadcrumbs | Manual Shell/file breadcrumb links | Mantine `Breadcrumbs`, `Anchor`/Router links, `Text` truncation | Route/path derivation and copy-full-path behavior | M | Current item semantics, accessible names, focus after deep link |
| ScrollArea | Ad hoc `overflow-auto` regions | Mantine `ScrollArea` for ordinary bounded lists; native viewport/ref for virtualizers and third-party engines | Tail pinning, x/y policy, scroll restoration | M | One scroll owner only; ScrollArea is not a virtualizer |
| Split-pane layouts | Fixed Flex/Grid columns with Tailwind minmax classes | `Box`/`Paper` plus local CSS Grid module; `Drawer` at narrow widths | Pane sizing, selection, responsive state | M-H | Keep `min-width/min-height: 0`; do not adopt resizable Splitter without keyboard QA |
| Command composer | One-row custom Tailwind form | `Paper`, `Stack`, `Group`, local Grid, `Select`/`Combobox`, `NumberInput`, `TextInput`, `Button` | Command parsing, workspace target, timeout, submit mutation | M | Separate history filter from target; errors associated; no narrow overflow |
| Command card | Custom bordered disclosure and controls | `Card`, `Accordion`/`Collapse`, `Badge`, `Group`, `Menu`, `Code`, `Kbd` | Transcript lifecycle, stdin, result/publication details, links | H | One RPC per key action; expansion/focus stable under polling |
| Transcript viewer | TanStack Virtual, fixed 18px estimate, wrapping rows, custom paging/tail | Mantine `Paper`/toolbar around a native virtualizer viewport | Paging, offsets, tail pinning, 400ms active polling, stdin state | H | Fixed rows cannot wrap; dynamic measurement if wrap enabled; bounded DOM |
| Events table | Manual sticky table and newest-first polling | TanStack Table + Mantine Table + native/Mantine viewport; Virtual when measured | Absolute time filter, Tail/Pause, URL state, trace navigation | H | Do not reorder focused rows; responsive summary; table/virtual semantics |
| Trace detail/waterfall | Recursive span list, fixed split/waterfall, no virtualization | Mantine Tabs/Combobox/Paper/Drawer plus local minmax Grid and virtualized flattened span tree | Trace inference, span selection, time geometry, event markers | H | Minimum inner width with explicit x-scroll; abort stale fetches; no false links |
| File viewer and blame controls | CodeMirror recreated on data/mode changes; ad hoc toolbar and blame gutter | Mantine `Paper`, `Breadcrumbs`, `Group`, `SegmentedControl`/`Switch`, `Drawer`; stable CodeMirror host | Paging, edit/save, draft, conflict, line owners, current-file links | H | Preserve editor instance/focus/undo/viewport; keyboard blame; no nested scroll |

## 6. Layout and responsive blueprints

### Shared frame

Breakpoints are theme-owned:

- Base to 767px: single-column content; secondary panes become Mantine Drawers
  or disclosures.
- 768px to 1023px: primary content remains full width; investigation panes are
  on demand.
- 1024px and above: persistent desktop split-pane workspaces.
- 1280px and above: the Fleet card Flexbox may fit more cards per row, but
  each card remains bounded rather than stretching to fill the viewport.
- 1440px is the widest required visual-regression checkpoint, not a license to
  let lines or panels grow without bounds.

Macro recipe:

- Use Mantine `AppShell` for the 44px header and application main region.
- Place the canonical cat-in-sandbox logo in a fixed 28–32px Mantine `Image`
  box at the start of the header, preserve its square aspect ratio and
  transparency, and keep the adjacent EphemeralOS name visible where space
  permits.
- Constrain the root to `100dvh`; `AppShell.Main` must have zero minimum block
  and inline size and hide document overflow.
- Use `Group` for the header and `Breadcrumbs` with truncating `Text` for the
  current location.
- The active route owns scrolling; the document body has neither horizontal
  nor vertical scrolling.
- Use `Box`/local CSS Grid for exact `auto` and `minmax(0, 1fr)` workspace rows.
- Persistent controls occupy explicit workspace rows, never viewport-fixed
  layers over content.

### 6.1 Fleet overview — revised

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

Do not show layers, storage stack depth, region, owner, age, TTL, labels, or a
synthetic health score.

Composition:

- A `Box` local Grid creates `auto`, `auto`, and `minmax(0, 1fr)` rows for
  summary, toolbar, and cards.
- Use `SimpleGrid` for two base columns, three at 768px, and five at 1280px.
- Each `Paper` summary cell has one label, one value, and reserved loading
  height.
- Summary and cards consume the same authoritative sandbox list generation.

#### Toolbar

- `TextInput` search matches ID and workspace root, both already present in
  `SandboxRecord`.
- State filters are All, Ready, Creating, Stopping, Failed, and Stopped.
- Use `Group` with wrapping for search, filter controls, and the primary New
  Sandbox Button.
- Below 375px, keep the state `SegmentedControl` in one labelled horizontal
  native overflow region rather than shrinking labels.
- Do not add owner, region, age, or tag filters without backend fields.

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
- The Mantine Menu is reserved for destructive or infrequent actions.
- Do not put Destroy as an unlabeled 24px icon in the main action row.

Body:

- Workspace root is a single truncated monospace line with the full value
  available to copy or inspect.
- Activity uses plain language: “2 sessions” and “1 command running.”
- Running command count receives the strongest accent because it is the most
  immediate operational signal.
- CPU activity and memory use a quiet two-column local Grid inside the Card.
- CPU uses the existing activity series rather than inventing a precise
  percentage. Memory may show current `mem_cur` when available.
- Freshness comes from snapshot sampling time when available.

Footer:

- Open is the primary Button.
- Terminal is the single contextual quick action.
- Squash is removed from Fleet.
- Destroy moves to a labelled Menu confirmation path or remains in sandbox
  detail if the menu is not implemented.

Visual and responsive behavior:

- Theme warm-white Mantine Card, theme border, small radius, and restrained
  shadow.
- Hover changes border/shadow only; there is no lift, scale, or movement.
- Active commands may add a narrow accent edge or soft Badge, never a fully
  tinted card.
- The Fleet card collection uses Mantine `Flex` with wrapping, theme gap,
  `align="flex-start"`, and `justify="flex-start"`; it does not use
  `SimpleGrid` or CSS Grid for card placement.
- Below 768px, each card takes the full available row width. At 768px and
  above, each card uses a flexible basis of 22rem, may grow only to a maximum
  inline size of 28rem, and wraps naturally as space permits. Unused space on
  a partial row remains empty instead of stretching its cards.
- Each card has a maximum block size of 22rem and is never stretched to match
  a taller neighbor. Keep essential identity, state, freshness, and actions
  visible within that bound; long progress, error, or diagnostic detail opens
  through View progress or Inspect rather than creating a per-card scroller or
  being clipped.
- Card internals use `Stack`, `Group`, and a small local two-column resource
  Grid. Actions become a two-column full-width Grid at very narrow card widths.
- Reserve predictable internal regions so polling does not make cards jump,
  while allowing shorter lifecycle variants to remain shorter than the
  maximum height.

Card variants and query states remain distinct:

- Ready/idle: neutral card, “No commands running.”
- Ready/active: running count highlighted; transcript/output stays off Fleet.
- Creating: stable Progress block and latest line; details open on demand.
- Stopping: entry actions disabled and transition visible.
- Failed: inline failure explanation, Inspect primary, Destroy secondary.
- Stopped: muted state with only supported Inspect/Destroy actions.
- Snapshot stale/error: retain values and show Stale/Unavailable; never turn
  missing data into zero.
- Initial loading: stable summary/card Skeletons.
- Background refresh: retain cards and show freshness.
- Error with stale data: retain cards plus inline retry Alert.
- First-use empty: explanation plus New Sandbox Button.
- Filtered empty: filter summary plus Clear filters.
- Creation failure: keep the failed progress card visible.

### 6.2 Creation and WorkspacePicker

Creation remains driven by the audited `create_sandbox` operation catalog;
the layout must not introduce fields beyond that catalog.

- Use a labelled Mantine `Modal` with a bounded body and persistent action
  footer. At narrow widths it becomes full-screen rather than overflowing the
  viewport.
- Render catalog fields in a compact `Stack` with `Input.Wrapper`; use
  `Select` for a small Docker-image set and searchable virtualized `Combobox`
  only when measured cardinality warrants it. Image names and paths remain
  monospace.
- Keep validation next to its field and keep Cancel/Create actions in a
  `Group` aligned to the footer. The first invalid field receives focus after
  submit.
- Treat WorkspacePicker as a controlled sibling overlay, not a nested focus
  trap. Opening it preserves the creation draft; closing it restores focus to
  the workspace control.
- While WorkspacePicker is open, it owns the only active focus trap; the
  Creation surface is inert or suspended without unmounting or losing its
  draft.
- WorkspacePicker uses `Modal` on desktop and a full-screen `Drawer` below
  768px. Its header contains Up, Roots, the current path, and search when the
  current API can support it; its one bounded collection viewport contains
  the directory options.
- Parent navigation, current-path selection, loading, unavailable, empty,
  permission error, and the current 500-entry truncation are explicit. Search
  must not imply results beyond the returned page until a backend search or
  cursor contract exists.
- Preserve current streamed creation progress on the Fleet card after submit;
  do not trap the operator in a busy Modal.

### 6.3 Sandbox detail workspace

~~~text
┌ Fleet / sandbox-id                                  Actions ┐
│ sandbox-id  Ready  Reachable  /workspace/root                │
├ [CPU] [Memory] [Workspaces] [Running] [Sampled]             ┤
├ Overview | Terminal | Files | Observability | Preview        ┤
├──────────────────────────────────────────────────────────────┤
│ Active tab: one bounded content region                       │
└──────────────────────────────────────────────────────────────┘
~~~

Layers are absent from top-level stats and navigation. Storage and Layers
remain in Observability where they have the required context.

Composition:

- A `Box` with local Grid owns identity, metrics, Tabs, and
  `minmax(0, 1fr)` content rows.
- Identity uses a local Grid with `minmax(0, 1fr)` content and auto actions at
  768px; it stacks below that width.
- Metrics use `SimpleGrid`: two base, three at 768px, five at 1280px.
- Mantine `Tabs` renders Router links and uses a bounded horizontal overflow
  region on narrow screens.
- Active content has zero minimum inline/block size and owns internal scrolling.
- Overview uses `SimpleGrid` or a local Grid at 1024px for the primary and
  secondary columns; it becomes one scrolling column below 1024px.

Lifecycle, availability, errors, sessions, active executions, CPU, memory, and
sample freshness come first. Raw endpoints and record data belong in a
secondary Details disclosure.

### 6.4 Terminal and command workspace

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

Desktop composition:

- Use a local CSS Grid module because the workspace requires a fixed 15rem
  rail, `minmax(0, 1fr)` content, and `auto/minmax/auto` rows.
- Mantine `Paper`/`Stack` compose the rail; the rail has its own ordinary
  ScrollArea.
- The ledger has zero minimum size and one vertical scroll owner.
- The composer occupies the final Grid row and is not viewport-fixed.
- The transcript has a bounded `clamp(16rem, 42vh, 32rem)` block size and a
  native virtualizer viewport with explicit x/y overflow.
- Preserve non-wrapped fixed virtual rows. If Wrap is enabled, switch to
  dynamic measurement rather than retaining an 18px estimate.

Below 1024px, Sessions opens in a left Mantine Drawer. Below 768px, composer
controls use a two-row local Grid. History filtering and execution target
selection are separate controls.

Collapsed Command Cards show command, actual workspace, status, exit and
publication outcome, duration, and time. Expanded cards add transcript state,
stdin, IDs, Copy, Prefill/Rerun, and only valid contextual links.

### 6.5 Observability and auditability

~~~text
┌ Resources | Traces | Events | Layers                    ┐
├ Scope/filter controls                  Live · updated 2s ┤
├──────────────────────────────────────────────────────────┤
│ Active investigation surface                             │
└──────────────────────────────────────────────────────────┘
~~~

Use Mantine Tabs with Router-owned subroutes, a `Group`/`Flex` toolbar, and a
single bounded content region.

Resources:

- A local two-row Grid keeps the toolbar above `minmax(0, 1fr)` content.
- `SimpleGrid` creates one chart column at base and two at 768px.
- Each `Paper` reserves chart height and provides latest/minimum/maximum text.
- Keep each uPlot instance alive; use `setData`, ResizeObserver, and a theme
  color bridge rather than recreation on every poll.
- Provide a numerical alternative to each chart.

Events:

- Use a Mantine toolbar and bounded semantic Table viewport.
- TanStack Table owns sorting, visibility, expansion, and stable row identity.
- TanStack Virtual handles measured high live row counts.
- Below 768px, prioritize time, event, and trace summary; details expand inline
  or in a Drawer.
- Live polls; Paused actually stops polling.

Traces:

- A local desktop Grid uses a `clamp(14rem, 22vw, 19rem)` selection pane and a
  `minmax(0, 1fr)` detail pane.
- Waterfall content has a minimum inner width and one explicit horizontal
  scroll viewport.
- Below 1024px, trace selection becomes a Drawer or virtualized Combobox.
- Flatten and virtualize visible spans at measured volume.

Layers:

- Canonical home is Observability > Layers.
- At 1280px, a local Grid uses `minmax(0, 1fr)` content plus a 20rem detail
  pane; details stack below at smaller widths.
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

### 6.6 File workspace

~~~text
┌ scope / Files ┐┌ breadcrumb / path ─── Blame · Edit/Save ┐
│ repository    ││ code viewer / editor                    │
│ tree          ││ line │ owner │ content                  │
│ tree scrolls  │├ paging / conflict / status              │
└───────────────┘└──────────────────────────────────────────┘
~~~

Composition:

- Use a local desktop Grid with a `clamp(14rem, 22vw, 20rem)` tree pane and a
  `minmax(0, 1fr)` viewer pane.
- Mantine Tree and CodeMirror each own exactly one scroll viewport.
- A local header Grid gives Breadcrumbs the flexible column and actions the
  auto column.
- Preserve code line geometry by default; Wrap is optional.
- Keep the CodeMirror instance, selection, viewport, undo history, and draft
  stable through paging and blame changes.
- Conflict state uses Mantine Alert/Paper/Tabs or a comparison composition and
  preserves both local draft and server content.

Below 1024px, the Tree moves to a left Drawer. Breadcrumb and current scope
remain visible after the Drawer closes. Blame becomes an optional gutter or
detail Drawer rather than compressing code.

### 6.7 Preview

~~~text
┌ scope ─ port ─ path ───────────── Refresh · Open tab ┐
├ network / security / loading status                  ┤
│                     iframe                           │
└──────────────────────────────────────────────────────┘
~~~

Composition:

- A local Grid creates toolbar, reserved status row, and
  `minmax(0, 1fr)` iframe rows.
- Desktop toolbar uses `Group`/`Flex` with Mantine form controls.
- Below 768px, a local Grid puts scope and port first, full-width path second,
  and actions third.
- Reserve status geometry to prevent layout shift.
- Do not invest heavily in embedded-preview polish before approving the
  isolation model. Mantine does not mitigate same-origin iframe risk.

## 7. Mantine layout primitives versus local CSS Grid

| Region or need | Preferred mechanism | Reason and boundary |
|---|---|---|
| Application shell | Mantine `AppShell`, `Group`, `Box` | Standard header/main chrome with theme spacing and breakpoint behavior |
| Inline headers/status/actions | `Group` or `Flex` | One-dimensional alignment and wrapping |
| Vertical control/panel sequences | `Stack` | Consistent theme spacing |
| Repeated equal cards/metrics/charts | `SimpleGrid` or Mantine `Grid` | Responsive repeated composition without bespoke media rules |
| Fleet summary metrics | `SimpleGrid` | Compact equal summary cells at theme breakpoints |
| Fleet card collection | Mantine `Flex` with wrapping and bounded `Card` items | Natural card counts across wide screens without stretching; cards use a 22rem flexible basis, 28rem maximum inline size, 22rem maximum block size, and start alignment |
| Tabs and action groups | `Tabs`, `Group`, bounded native overflow | Ordered navigation/actions with semantic controls |
| Ordinary bounded list | `ScrollArea` | Styled scrollbars, viewport ref, and overscroll containment |
| Virtualized list/tree/table | Native viewport or proven `ScrollArea` viewport ref + TanStack Virtual | The virtualizer needs the direct stable scroll element; ScrollArea alone does not reduce DOM |
| Terminal workspace | Local CSS Grid module + Mantine surfaces | Requires fixed rail plus `minmax(0, 1fr)` and three explicit rows |
| Trace/File split panes | Local CSS Grid module + `Paper`; `Drawer` narrow | Exact clamp/minmax columns are clearer and safer than nested layout props |
| Optional user-resizable panes | Mantine `Splitter` only after keyboard/a11y spike | Official docs cover the resizable API but do not document keyboard operation; current product does not require resizing, so do not add it speculatively |
| Dense label/value or layer rows | Local CSS Grid module | Repeated two-axis alignment with theme CSS variables |
| Data table | Semantic Mantine `Table` | Preserve table semantics; Grid may surround but not replace table structure |
| CodeMirror/uPlot host | `Box`/`Paper` plus local containment CSS | Third-party engine controls inner DOM, sizing, and scroll behavior |
| Drawer body | `Drawer`, `Stack`, one ScrollArea | Standard focus/overlay behavior with a single scroll body |

Local CSS Modules may use Mantine CSS variables for spacing, colors, radii,
and typography. They may define geometry; they must not define a parallel
token system or recreate Mantine control styles.

## 8. Accessibility, loading, polling, and performance requirements

### 8.1 Focus, keyboard, and semantics

- Add a skip link and one semantic main region.
- Keep Mantine `focusRing: auto` and a visible 2px high-contrast focus-visible
  treatment across controls, links, table interactions, tree nodes, and custom
  split/virtual surfaces. Never suppress outline without an equivalent.
- Use `aria-current` for active navigation/sessions and `aria-expanded` for
  expandable folders, commands, events, spans, and disclosures. Add
  `aria-controls` only when the controlled target has a stable rendered ID;
  never leave it pointing at an unmounted virtual row.
- FileTree supports Up, Down, Left, Right, Home, End, typeahead, and roving
  focus. Normal Tree and virtualized `FlatTreeNode` must pass the same keyboard
  suite. Retain `role="tree"`, stable IDs, and Mantine's documented handlers,
  then add localized custom behavior for any spike-proven Home, End,
  typeahead, or offscreen-focus gap.
- WorkspacePicker supports labelled search, Arrow navigation, typeahead,
  Enter selection, Escape closure, and deterministic focus restoration.
- Deep links move focus as well as scroll.
- Ctrl-C and Ctrl-D produce one RPC each.
- Replace unmodified numeric tab shortcuts with documented modified shortcuts
  that do not fire while editing or conflict with assistive technology.
- Tooltips are supplemental and never the sole accessible name.
- Desktop density does not excuse sub-target controls; narrow layouts use
  touch-sized actions.

### 8.2 Portals, focus traps, and restoration

- Modal and Drawer keep focus trap, Escape, semantic titles, scroll lock, and
  return-focus behavior enabled unless a documented exception is tested.
- Destructive or stateful operations define whether outside click may close
  the overlay; no in-progress draft is silently discarded.
- Portal z-index is theme-owned and tested with nested Menu/Popover content,
  notifications, CodeMirror, uPlot, and the body-overflow-hidden shell.
- If the trigger no longer exists after polling, focus moves to the route
  heading or the nearest stable region.

### 8.3 Reduced motion and contrast

- Set `respectReducedMotion: true`; use `useReducedMotion` for custom chart,
  transcript, progress, and pane behavior outside Mantine transitions.
- No layout-affecting hover animation. Loading pulses become static under
  reduced motion.
- Recalibrate `ink-faint` and status pairs into the Mantine palette. Essential
  normal text and controls meet WCAG AA; state is always reinforced by text or
  icon, not color alone.
- Validate focus-ring contrast against canvas, surface, selected, danger, and
  chart backgrounds.

### 8.4 Loading and live-region model

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

Skeletons reserve final geometry. Background refresh retains the last good
data and exposes freshness; missing data is never coerced to zero. Streamed
lines are not individually announced. A concise, explicit polite live region
announces completion, failure, connection/freshness transitions, and critical
destructive outcomes; urgent failures alone use alert semantics.

### 8.5 ScrollArea and virtualization

- Every pane has one intentional scroll owner. Never nest Mantine ScrollArea
  around CodeMirror, uPlot, or a native virtualizer viewport by default.
- ScrollArea needs an explicit bounded size or maximum size. It customizes
  overflow presentation; it is not a virtualizer.
- When TanStack Virtual uses a ScrollArea, pass the direct viewport ref and
  test sticky headers, keyboard scroll, restoration, and overscan.
- Terminal fixed-height rows do not wrap. Wrap mode uses dynamic measurement.
- Table/tree/span virtualization preserves stable keys, focused item identity,
  semantic roles, and an explicit strategy for offscreen active items.

### 8.6 Polling and rerender control

- Preserve the current 400ms fast/2s slow model, previous-data retention,
  hidden-tab pause, focus catch-up, 15-second idle decay, and 8-second ceiling
  unless a separate performance change is approved.
- Hidden tabs pause or back off; focus performs bounded catch-up.
- Snapshot polling accelerates for actual active work.
- Fleet summary and cards share one authoritative list generation.
- Polling must not remount Mantine providers, controls, or overlays, or
  recreate Tree, CodeMirror, uPlot, or virtualizer instances. Tree identity,
  expansion, selection, and focus remain stable as data updates.
- Do not reorder a row or card under keyboard focus. Defer newest-first movement
  or preserve focused-row placement until focus leaves.
- Replace whole-payload `JSON.stringify` fingerprints for large live data with
  revision fields or surface-specific comparisons.
- Consolidate or schedule per-command pollers and bound the number of expanded
  active transcripts.
- Memoize expensive flattened tree/span/table models by stable data revision.
- Keep uPlot and CodeMirror instances stable and update them incrementally.
- Use ResizeObserver for charts and pane hosts; abort stale file/trace requests.
- Cap or virtualize streamed logs and expose pause, wrap, copy, and truncation.

## 9. Correctness, security, and audit invariants

The component migration does not weaken or defer these findings.

| Finding | Required invariant |
|---|---|
| Event time range | Convert the selected duration to the absolute epoch threshold expected by the backend; Tail off stops polling. |
| Trace attached events | Match backend `EventNode { offset_ms, event }`; markers use backend offsets. |
| Terminal controls | One Ctrl-C/Ctrl-D gesture generates exactly one stdin RPC. |
| Command outcome | Preserve authoritative exit, `publish_rejected`, and `publish_reject_class`; rejection cannot appear successful. |
| Transcript isolation | Cache keys include sandbox identity and command/session identity. |
| File conflict | Never replace the local draft with server content; full safety requires backend CAS/revision support. |
| Preview | Same-origin unsandboxed content is not considered safe; approve iframe restrictions or a dedicated untrusted origin before polish. |
| Fleet list | Summary and cards use one authoritative generation and cannot disagree because fast polling stopped. |
| Snapshot activity | Ready sandboxes with active work enter the intended fast polling mode. |
| Missing command/history | Browser-local ledger remains non-authoritative; unknown/expired commands cannot be presented as empty success. |
| Trace discovery | Continue to label the last-200-event inference as partial until a trace index exists. |
| Files/layers/picker limits | Expose current 2,000 file, 500 layer-detail, and 500 picker truncation rather than implying completeness. |

Supported audit links remain limited to explicit or documented identifiers:

| From | To | Evidence level |
|---|---|---|
| Event trace ID | Trace detail | Explicit contract |
| Event parent span ID | Selected span | Frontend route state |
| Blame operation request owner | Trace | Existing parsing convention, not a structured guarantee |
| Blame workspace session owner | Terminal filter | Existing parsing convention; history may be absent |
| Layer changed path | Current Files path | Frontend convenience; not historical layer content |
| New caller-supplied RPC request ID | Trace | Supported future correlation when the browser sends the ID |

Never infer command-to-trace, command-to-layer, command-to-file,
trace-to-file, or layer-to-operation relationships from arbitrary attributes,
similar IDs, or current selection.

## 10. Full migration sequence

No implementation begins until this proposal is approved. Each phase must
leave the console buildable. A temporary Tailwind inventory names every
remaining legacy route/component and shrinks at each phase; no legacy screen
is accepted as a permanent island.

### Phase 0 — Mantine compatibility spike and trust gate

- Run the exact-version React/Vite/TypeScript/build/test/style/portal spike
  described in section 4.3.
- Inventory all Radix imports/wrappers, direct Tailwind classes, `@theme`
  tokens, global styles, and package/config dependencies.
- In parallel, correct the P0 trust defects that do not depend on visual
  components: event time/pause, trace payload, duplicate stdin, publication
  outcome, transcript isolation, file-draft preservation, Fleet generation,
  and active snapshot polling.
- Record and approve the Preview isolation decision; it may block only Preview
  migration, not the rest of the visual foundation.

Exit: the spike passes or is removed cleanly; the dependency/version plan is
explicit; trust fixtures pass; no experimental provider enters production.

### Phase 1 — Theme and token mapping

- Register the canonical logo pixels in a durable source/static asset input
  and make the header render plan independent of generated `dist` output.
- Define the EphemeralOS light theme, palette, typography, monospace usage,
  spacing, radii, shadows, focus ring, reduced motion, and breakpoints. Derive
  its warm neutrals and eye-blue interaction scale from the logo anchors in
  section 4.5.
- Define component sizes/defaults/variants and the z-index/overlay scale.
- Create visual fixtures for ordinary, hover, selected, disabled, loading,
  stale, error, destructive, and focus states.
- Mirror breakpoints into static PostCSS variables and add a drift check.

Exit: contrast and focus pass; the approved fixtures still look like the
compact operator console, not a default Mantine dashboard.

### Phase 2 — Provider and global-style foundation

- Add one MantineProvider and one Notifications host while preserving Query
  and Router providers.
- Establish Core/Notifications stylesheet order and the minimal app-global
  containment stylesheet.
- Add shared test rendering, jsdom mocks, and browser portal/focus fixtures.
- Establish the Tailwind allowlist and a CI check that prevents new utility
  styling outside it.

Exit: both legacy and migrated screens build under one provider; there is no
new competing theme. Mantine is authoritative on migrated surfaces, while the
frozen Tailwind `@theme` remains migration-only and allowlisted until Phase 10;
global sizing and body overflow remain stable.

### Phase 3 — Primitive migration

- Migrate Button, ActionIcon, input family, Select/Combobox, Modal, Drawer,
  Popover, Tooltip, Menu, Tabs, notifications, Badge, Paper/Card, Skeleton,
  loading/error/empty states, Breadcrumbs, and ordinary ScrollAreas.
- Preserve product behavior such as StateBadge mappings and RPC error details.
- Add adapter components only when they encode EphemeralOS semantics, not to
  reproduce the old Radix API indefinitely.

Exit: no new feature imports a local Radix wrapper; migrated primitives pass
keyboard, axe, focus, portal, reduced-motion, and visual tests.

### Phase 4 — Shell and navigation migration

- Migrate Shell to AppShell/Group/Breadcrumbs, the canonical logo Image, and
  bounded route containment.
- Migrate sandbox route Tabs and Observability subnavigation.
- Canonicalize Layers under Observability while preserving redirects and deep
  links.
- Replace unsafe global numeric shortcuts.

Exit: all routes and URL state still resolve; one semantic main region and one
route scroll owner work at all target widths.

### Phase 5 — Fleet and Overview migration

- Migrate creation, WorkspacePicker, Fleet summary, toolbar, cards, sandbox
  header, metric strip, and Overview panels.
- Remove Layers/Squash from Fleet and use one list generation.
- Implement all loading/fresh/stale/error/empty/truncated states.

Exit: Fleet hierarchy and supported fields match this proposal; cards do not
move on hover or exceed their documented width/height bounds; the Flexbox
wraps without stretching a partial row; picker keyboard/virtualization works;
polling cannot reorder or blur a focused control.

### Phase 6 — Terminal migration

- Migrate Sessions Drawer/rail, command toolbar, composer, CommandCard,
  transcript chrome, stdin controls, and result/publication feedback.
- Preserve TanStack Virtual, paging, offsets, tail pinning, and one transcript
  scroll owner.
- Separate history filtering from execution target and consolidate pollers.

Exit: trust fixtures pass; invalid timeout is associated and blocks submit;
10,000-line/10,000-character fixtures render without overlap; polling does not
lose composer or transcript focus.

### Phase 7 — Observability migration

- Migrate Resources, Events, Traces, Layers, and logs to Mantine surfaces,
  controls, Tabs, Drawers, and feedback.
- Add TanStack Table for Events and preserve TanStack Virtual at measured scale.
- Keep uPlot instances stable and add numerical summaries.
- Virtualize flattened spans where the performance fixture requires it.

Exit: absolute event filters and Pause work; sort/expansion/focus survive
polling; trace markers use the backend shape; charts update without recreation;
only explicit audit links render.

### Phase 8 — Files and Preview migration

- Migrate FileTree to Mantine Tree/FlatTreeNode, File controls to Mantine, and
  narrow tree/blame panes to Drawers.
- Keep CodeMirror stable through paging, edit, blame, and conflict states.
- Migrate Preview controls/status only under the approved isolation policy.

Exit: full tree keyboard model/typeahead works; truncation is visible; file
draft/focus/undo/viewport survive updates; Preview meets the approved security
policy and responsive layout.

### Phase 9 — Remove local Radix wrappers

- Remove all wrapper usage and direct Radix imports.
- Remove unused wrapper files, Toast/Tooltip providers, Radix packages, and the
  already-unused Radix Tabs/Dropdown dependencies.
- Prove overlays, toasts, selection, and tooltips through regression tests.

Exit: repository search and dependency graph contain no application Radix use.

### Phase 10 — Remove Tailwind component styles and tokens

- Migrate every remaining allowed utility string to Mantine props, Styles API,
  or local CSS Modules using Mantine variables.
- Remove `@import "tailwindcss"`, `@theme`, obsolete global tokens, Tailwind
  Vite integration/configuration, and any now-unused class-merging helper.
- Review CSS Modules to ensure they define geometry/containment rather than a
  second component skin.

Exit: the Tailwind allowlist is empty; no permanent Tailwind component styling
or global token system remains.

### Phase 11 — Dependency and dead-code cleanup

- Remove obsolete Radix/Tailwind packages, unused spike packages, wrappers,
  styles, adapters, and imports.
- Ensure all `@mantine/*` packages use the same exact version.
- Verify no community “Mantine” extension slipped into the dependency graph.

Exit: the dependency graph matches section 4.2 plus approved retained engines;
typecheck, unit tests, and production build succeed.

### Phase 12 — Full verification and release gate

- Run visual regression at 375, 768, 1024, and 1440px across route and query
  states.
- Run keyboard, screen-reader, axe, reduced-motion, responsive, portal, focus,
  body-overflow, polling, and deep-link suites.
- Run terminal, table, tree, trace, file, CodeMirror, and uPlot performance
  fixtures in a production build.
- Re-run every trust/security/audit fixture and inspect the final diff for
  Radix/Tailwind residue.

Exit: all completed-migration acceptance criteria below pass.

## 11. Completed-migration acceptance criteria

### Architecture and dependencies

- MantineProvider and the EphemeralOS Mantine theme are the only application
  component/theme system.
- There is no remaining local Radix wrapper usage, direct Radix import, Radix
  provider, or Radix dependency.
- There is no competing application theme, duplicate reset, or legacy global
  token layer.
- There is no permanent Tailwind component styling, Tailwind import/plugin/
  config, or nonempty migration allowlist.
- Local CSS Modules contain only layout, containment, third-party integration,
  and documented component Styles API overrides using Mantine variables.
- Obsolete dependencies, wrappers, styles, helpers, and spike packages are
  removed. All remaining `@mantine/*` packages use one exact version.
- Typecheck, unit tests, and the production build succeed.

### Visual and responsive behavior

- Approved visual baselines have no unintended regressions at 375, 768, 1024,
  and 1440px, including loading, stale, error, empty, active, Drawer, Modal,
  Menu, Tooltip, and notification states.
- The console remains compact, light, calm, information-dense, and recognizably
  EphemeralOS rather than a generic SaaS dashboard.
- No body-level overflow exists, horizontally or vertically. Every route and
  pane has one intentional scroll owner and no clipped focus ring.
- The header renders the canonical cat-in-sandbox logo without distortion,
  cropping, layout shift, or loss of route context at every target width. Its
  accessible name is not duplicated when adjacent product text is present.
- Fleet cards use a wrapping Flexbox and become full-width below 768px. At
  768px and above they stay at or below 28rem inline; at every width they stay
  at or below 22rem block. Partial rows remain start-aligned, and no essential
  status or action is clipped by the height bound.
- Desktop split panes become usable Drawers/stacks at the documented widths.
- Polling changes do not cause card/panel movement, cumulative layout shift,
  uncontrolled reordering under focus, or overlay-trigger disappearance.

### Accessibility

- Keyboard and screen-reader behavior is at least at parity with the approved
  design: skip/main, route state, forms, tree, combobox, table, tabs, menus,
  overlays, drawers, transcript controls, blame, and deep-link focus all pass.
- Modal and Drawer focus trap, Escape, labelling, scroll lock, and restoration
  pass with real portals; deterministic fallback focus works if a trigger is
  removed.
- Focus is visible, contrast meets WCAG AA for essential text/controls, state
  is not color-only, reduced motion is respected, and tooltips are supplemental.
- Notifications/live regions announce concise state changes without announcing
  every stream line or poll.

### Correctness, routing, and polling

- Existing routes, URL filters, redirects, query parameters, and deep links
  remain compatible.
- Last-five-minute event fixtures use the correct absolute threshold; Tail off
  stops polling; trace markers render at backend offsets.
- One terminal control gesture creates one stdin RPC; publication rejection
  cannot appear successful; cross-sandbox transcript leakage is impossible.
- File conflict never destroys the draft; Preview follows the approved
  isolation policy.
- Fleet cards and summary cannot disagree because of list generations; active
  ready sandboxes enter fast polling.
- Polling preserves last good data, freshness, focus, selection, scroll intent,
  open overlays, CodeMirror state, uPlot instances, and virtualizer identity.

### Performance targets

Measure on the agreed reference machine using a production build and stable
synthetic fixtures; these fixtures are frontend verification targets, not new
backend contracts. Record at least 200 measured interactions after warm-up for
each p95 gate and include a 60-second fast-poll run for every live surface.

- Terminal: 10,000 transcript lines plus one 10,000-character line render with
  bounded DOM, no overlap, and no tail jump; p95 composer key-to-paint, tail
  toggle-to-paint, and transcript scroll input-to-paint are each under 100ms.
- Events table: 10,000 rows keep a bounded rendered row set; sort/filter/
  expansion and keyboard focus survive polling; p95 local interaction-to-paint
  is under 100ms.
- FileTree/WorkspacePicker: 10,000 flattened synthetic nodes/options keep a
  bounded DOM and p95 keyboard navigation under 100ms; actual API truncation is
  still labelled.
- Trace: a 2,000-span synthetic trace keeps the visible tree bounded; p95
  span-selection-to-detail-paint and waterfall scroll input-to-paint are each
  under 100ms, and waterfall scrolling remains independent of the body.
- Files: viewing/paging at current API limits and editing a 1 MiB fixture at the
  current edit ceiling keep p95 editor key-to-paint under 100ms and do not
  recreate CodeMirror or lose selection, viewport, undo, draft, or focus;
  stale requests are aborted.
- Resources: polling calls incremental uPlot updates rather than rebuilding
  plots; p95 sample-to-chart-paint is under 100ms, and ResizeObserver changes
  do not create loops or layout shift.
- Polling: during each 60-second fast-poll fixture, p95 accepted-result-to-
  committed-paint is under 100ms, no polling task exceeds 200ms, steady-state
  cumulative layout shift is 0.00, focus-loss count is zero, and poller count
  stays within the documented active-command bound.

## 12. Backend and API gaps or open questions

| Gap | Current evidence | Required decision or contract |
|---|---|---|
| Preview isolation | Same-origin iframe without sandbox | Iframe restrictions versus a dedicated untrusted origin |
| Command history | Browser-local ledger; active snapshot has only execution ID, operation, and lifecycle | Paginated, redacted, authorized history with timestamps and outcomes |
| Missing command | Unknown transcript can appear as empty OK | Explicit not-found or expired response |
| Trace enumeration | UI infers trace IDs from recent events | Trace index with time, duration, root operation, and status |
| Future correlations | Backend accepts caller request ID; browser omits it | Frontend support now; documented durable backend correlations later |
| Command to layer or file | No explicit keys in `CommandOutput` | Add only if required by product investigation goals |
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

## 13. Technology decision record follow-up

The older technology decision record still recommends local Tailwind styling
and local Radix composition, treats Mantine only as a possible intentional
redesign, and rejects a global theme provider. That decision is incompatible
with the requested direction that this proposal recommends and would authorize
if approved.

Do not edit that separate record as part of this documentation-only task. A
follow-up decision record must explicitly supersede or amend it before
implementation begins, recording:

- Mantine as the sole UI and theme system.
- The complete-migration end state and temporary Tailwind deletion gate.
- TanStack Table and Virtual as headless/performance engines.
- The decision not to add React Aria absent a demonstrated gap.
- The verified package-provenance boundary and rejection of unapproved
  community “Mantine” packages.
- The retained React Router, TanStack Query, CodeMirror, uPlot, and Lucide
  boundaries.

## 14. Official Mantine references

Sources verified on 2026-07-11:

- [Getting started and official package list](https://mantine.dev/getting-started/)
- [Vite setup and stylesheet order](https://mantine.dev/guides/vite/)
- [Mantine 8 to 9 migration and React 19.2 requirement](https://mantine.dev/guides/8x-to-9x/)
- [MantineProvider](https://mantine.dev/theming/mantine-provider/)
- [Theme object, focus ring, and reduced motion](https://mantine.dev/theming/theme-object/)
- [Component default props](https://mantine.dev/theming/default-props/)
- [Responsive styles and breakpoint constraints](https://mantine.dev/styles/responsive/)
- [Mantine PostCSS preset](https://mantine.dev/styles/postcss-preset/)
- [Official and community extensions](https://mantine.dev/x/extensions/)
- [Modal](https://mantine.dev/core/modal/), [Drawer](https://mantine.dev/core/drawer/), [Dialog accessibility warning](https://mantine.dev/core/dialog/), and [Portal](https://mantine.dev/core/portal/)
- [Tooltip accessibility](https://mantine.dev/core/tooltip/)
- [Mantine Table](https://mantine.dev/core/table/)
- [Tree and virtualized FlatTreeNode](https://mantine.dev/core/tree/)
- [Combobox and virtualized collections](https://mantine.dev/core/combobox/)
- [EmptyState semantics](https://mantine.dev/core/empty-state/)
- [Splitter API](https://mantine.dev/core/splitter/)
- [ScrollArea](https://mantine.dev/core/scroll-area/)
- [Notifications system](https://mantine.dev/x/notifications/) and [Notification accessibility](https://mantine.dev/core/notification/)
- [Vitest integration](https://mantine.dev/guides/vitest/)
