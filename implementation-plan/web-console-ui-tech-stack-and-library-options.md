# Web Console UI Technology Stack and Library Options

> **Status:** Proposed implementation guidance  
> **Scope:** `ephemeral-sandbox/web/console`  
> **Source snapshot:** 2026-07-11

This note records the web console's as-built UI stack, the constraints that
shape UI-library decisions, and a staged recommendation for future work. It
does not authorize a framework migration by itself.

## Decision summary

Keep the current **React + Tailwind + Radix** foundation. Do not introduce a
second, full visual design system for incremental work.

The first recommended addition is **TanStack Table** for operational tables.
Use **React Aria Components** selectively when an accessible tree, combobox,
table, or virtualized collection would be expensive to build from primitives.
Evaluate a full component suite only through an isolated redesign or prototype.

## Current UI technology stack

The source of truth is `web/console/package.json`; implementation usage is in
`web/console/src/`.

| Concern | As-built technology | Use in the console |
|---|---|---|
| UI runtime | React 19.2.7 + React DOM | All rendered UI |
| Build tooling | Vite 8 + TypeScript 6 | SPA development and production build |
| Styling | Tailwind CSS 4.3.2 via `@tailwindcss/vite` | Utility styling plus the console's custom CSS tokens |
| Accessible primitives | Radix UI | Dialog, popover, select, toast, and tooltip behavior |
| Icons | `lucide-react` | Consistent SVG icon set |
| Routing | React Router 7 | Nested routes, tabs, query-string filters, and deep links |
| Server state | TanStack Query 5 | Cached RPC data and polling |
| Virtualization | TanStack Virtual | Live terminal transcript rendering |
| File viewer | CodeMirror 6 | File content, editor state, commands, and gutters |
| Time-series charts | uPlot | Resource history charts |

### Local component layer

`web/console/src/components/ui/` contains local `Button`, `Input`, `Dialog`,
`Popover`, `Select`, and `Tooltip` wrappers. They combine Tailwind classes
with underlying Radix primitives and the console's own tokens.

This is **shadcn-style composition**, not a `shadcn/ui` package dependency:
the component source is local and owned by the repository. The declared
Radix dropdown-menu and tabs packages currently have no direct import in
`web/console/src/`; keep that distinction when auditing dependencies.

### Design and architecture constraints

- Preserve the compact, light, operator-console visual language: tokenized
  colors, dense data layouts, visible focus states, and minimal elevation.
- Preserve the custom surfaces that define the product: terminal transcript,
  CodeMirror file view, resource charts, trace waterfall, layer-stack view,
  and sparklines.
- Avoid CSS-in-JS and a runtime styling layer.
- Do not replace uPlot or CodeMirror for ordinary component-library work.
- Favor additive, headless behavior libraries over a full-kit migration unless
  the visual system is intentionally being redesigned.

## Current gaps worth solving

### Operational tables

`EventsView` manually sorts event rows and renders a raw HTML table. It has no
shared table abstraction for column visibility, user-driven sorting, paging,
selection, or reusable virtualization. The console already uses TanStack
Virtual for the terminal transcript, so table behavior can share established
performance patterns without changing the visual language.

### Large and keyboard-rich collections

`WorkspacePicker` renders directory entries as buttons and can show the first
500 child folders. Future folder, trace, or fleet collections need reliable
keyboard navigation, selection semantics, typeahead/search, and virtualization
before they grow more complex.

### Catalog-driven forms

`CreateSandboxModal` handles dynamic catalog arguments and validation in local
component state. A form library is not currently required, but it becomes
worth considering if multiple catalog-driven forms or cross-field validation
land.

## Candidate options

| Option | Best fit | Benefits | Cost and risk | Recommendation |
|---|---|---|---|---|
| **TanStack Table** | Events, fleet, and other operational tables | Headless sorting, filtering, pagination, column state, and typed table behavior; pairs naturally with the existing TanStack Virtual package | Requires a local Tailwind table adapter; does not provide visual components | **Adopt first** |
| **React Aria Components** | Accessible trees, comboboxes, tables, and complex collections | Unstyled, Tailwind-compatible patterns with keyboard and ARIA behavior; supports local composition | Overlaps some Radix primitives if used indiscriminately | **Adopt selectively for new complex patterns** |
| **Radix Themes** | A deliberate move to pre-styled components while staying in the Radix ecosystem | Low conceptual migration cost; cohesive theme, layout, and component primitives | Imports its own CSS and visual system; mixing it piecemeal with local Tailwind wrappers risks inconsistent UI | **Prototype only** |
| **Mantine** | A planned, broad admin-console redesign | Large component and hook catalog, forms, navigation, notifications, and rich selects | Adds a provider, global CSS/theme, and a second design language beside Radix/Tailwind | **Use only for an intentional redesign** |
| **PrimeReact** | A genuinely grid-centric product surface | Comprehensive data-grid-oriented component set and unstyled/Tailwind paths | Its official Tailwind theme is not tested with Tailwind v4; high integration cost for this stack | **Defer** |

### Supporting, non-visual additions

These are complementary tools rather than UI-component libraries:

- **React Hook Form + Zod:** evaluate only when catalog-driven forms multiply
  or validation becomes cross-field and asynchronous.
- **ECharts or Visx:** evaluate only if resource/trace views need interactive
  zoom, tooltips, multi-series analysis, or dashboards that uPlot cannot
  express cleanly.

## Recommendation and adoption sequence

### Phase 1 — add a local operational table foundation

1. Add `@tanstack/react-table`.
2. Create a local, Tailwind-styled table adapter; it must use the existing
   token names and dense row rhythm.
3. Migrate `EventsView` first while preserving its URL-backed `name`, `since`,
   and `last` filters.
4. Add row virtualization only when the observed event volume needs it, using
   the existing `@tanstack/react-virtual` dependency.

**Exit criteria:** event sorting/filtering remains URL-restorable, keyboard
navigation works, no layout shift occurs during polling, and the component is
usable without a new global theme provider.

### Phase 2 — improve complex collection accessibility

1. Prototype React Aria Components in `WorkspacePicker` or the next
   high-cardinality collection; do not rewrite existing dialogs or selects.
2. Establish a local wrapper for the accepted pattern so Tailwind tokens,
   focus behavior, empty states, and loading states remain consistent.
3. Validate keyboard navigation, screen-reader labels, and list performance
   with a large directory response.

**Exit criteria:** pointer and keyboard flows select the same item, the focus
ring remains visible, and the wrapper does not introduce a parallel theme.

### Phase 3 — evaluate a full component suite only with a product decision

Before adopting Mantine or Radix Themes, build a throwaway representative
surface covering a dialog, a long-form catalog flow, a data-dense table, and a
dark/light decision if dark mode has become a product requirement. Compare
bundle impact, CSS precedence, accessibility, visual fit, and migration cost.

Do not mix a full suite into individual screens opportunistically.

## Explicit non-decisions

- This note does not commit the console to Mantine, Radix Themes, PrimeReact,
  React Aria Components, React Hook Form, Zod, ECharts, or Visx.
- This note does not change the current light-only visual direction.
- This note does not replace local Radix/Tailwind wrappers with a package.
- This note does not alter the terminal, file editor, or current uPlot chart
  implementation.

## Decision criteria for future UI dependencies

A new dependency must satisfy all applicable criteria:

1. Solves a demonstrated product gap that local code would otherwise repeat.
2. Works with React 19 and Tailwind CSS 4.
3. Preserves accessible keyboard and focus behavior.
4. Does not impose a competing global CSS or theme system without an approved
   redesign decision.
5. Fits dense, polling-driven operator workflows without layout shift.
6. Has a named first integration surface, acceptance criteria, and removal
   path before being added to `package.json`.

## Sources

### Local implementation references

- `web/console/package.json`
- `web/console/src/index.css`
- `web/console/src/components/ui/`
- `web/console/src/pages/sandbox/observability/EventsView.tsx`
- `web/console/src/pages/fleet/WorkspacePicker.tsx`
- `web/console/src/pages/sandbox/terminal/TranscriptViewer.tsx`
- Historical design rationale: `docs/obsidian/ephemeral-os/implementation_plan/web-ui/design.md`

### External documentation

- [TanStack Table](https://tanstack.com/table/latest/docs/framework/react)
- [React Aria Components](https://react-aria.adobe.com/getting-started)
- [Radix Themes](https://www.radix-ui.com/themes/docs/overview/getting-started)
- [Mantine](https://mantine.dev/)
- [PrimeReact Tailwind integration](https://primereact.dev/docs/styled/guides/theming/tailwind)

## Document-registry blocker

This note is not registered with LoopX yet. Neither the source repository nor
this documentation vault has a project-local LoopX registry or an active goal
state, and the available global registry has no Ephemeral Sandbox goal.

After an owner connects this project to LoopX and resolves a stable goal ID,
register this note as `web-console-ui-techstack-spec` with topic
`web-console-ui-techstack` using a redacted source reference. Until then, this
file is the local durable record.
