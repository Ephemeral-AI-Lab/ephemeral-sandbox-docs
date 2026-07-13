# EphemeralOS E2E Control Room — UI Migration Specification

| Field | Value |
| --- | --- |
| Status | Ready for implementation |
| Implementation prompt | [e2e-test-ui-implementation-prompt.md](e2e-test-ui-implementation-prompt.md) |
| Source UI | `<E2E_SOURCE_ROOT>/web/src` |
| Visual target | [e2e-test-ui-layout-theme.md](e2e-test-ui-layout-theme.md) |
| Interaction target | [e2e-test-ui-design.md](e2e-test-ui-design.md) |
| System contract | [e2e-test-system-spec.md](e2e-test-system-spec.md) |
| Technical contract | [e2e-test-design.md](e2e-test-design.md) |
| Historical reference | `<E2E_SOURCE_ROOT>/web/prototype` |

## 1. Problem

The production React Control Room implements the basic route and API contract,
but its generic dark Mantine presentation is materially different from the
approved historical visual direction and incomplete relative to the rewritten
interaction design.

Repository history contains two separate UI lines: the original product commit
added the static prototype, while the external test repository created the
production React application independently. No commit migrated the prototype's
theme, shell, or route compositions into production. This migration closes that
gap without replacing the working API, reducer, routing, or safety model.

### 1.1 Repository evidence

| Commit | Repository | Evidence |
| --- | --- | --- |
| `54ed152e3` | `ephemeral-sandbox` | Added `e2e/ui-prototype`, including HTML, CSS, and all 11 JPG references. This is the original visual-design commit. |
| `a88e8c9ef` | `ephemeral-sandbox` | Removed the extracted E2E tree from the product repository; it did not supersede the design. |
| `70d9030` | `ephemeral-sandbox-test` | Added the production React Control Room, its API client, CSS, and component tests as a separate implementation. |
| `f549685` | `ephemeral-sandbox-test` | Made the React Control Room runnable end to end; it changed React/API files, not the prototype. |
| `b58d810` | `ephemeral-sandbox-test` | Preserved the historical prototype and screenshots at `e2e/web/prototype` during extraction. |

Use `git show 54ed152e3:e2e/ui-prototype/styles.css` in the product repository
to inspect the original theme at its source. Use the documentation JPGs for
review, because their availability does not depend on retaining the prototype
inside production source.

## 2. Goals

1. Adopt the attached warm editorial Control Room theme and page compositions
   without adopting the prototype's hash-route model.
2. Preserve the four production routes and Health drawer.
3. Preserve generic catalog-driven rendering; no domain, family, feature, test,
   or case gains a frontend-specific component or route.
4. Complete the missing interaction design required for Catalog, Review, Run,
   Runs, Workspaces, and Health.
5. Prove visual behavior at the required viewports and 200% zoom.
6. Preserve truthful state, revision-qualified scope, SSE reconciliation,
   evidence semantics, and server-projected action safety.
7. Deliver in independently reviewable slices with a green test suite after
   every slice.

## 3. Non-goals

- Do not serve, import, or progressively convert the static prototype DOM.
- Do not restore nine hash-routed pages or separate domain pages.
- Do not redesign backend state to fit sample screenshot content.
- Do not fabricate counts, progress, last-run health, paths, or evidence.
- Do not add charts, virtualization, a client state machine, a second component
  library, or a custom design-system package.
- Do not add dark mode during this migration.
- Do not change destructive-action eligibility in the frontend.
- Do not delete the historical prototype until production visual acceptance is
  complete and the reference assets are retained in documentation.

## 4. Constraints

### 4.1 Stack

Keep the existing React, TypeScript, Mantine, React Router, TanStack Query, and
native `EventSource` stack. Use Mantine for accessible behavior and CSS/theme
overrides for the target appearance.

No dependency is added merely to reproduce styling. A browser visual-test
runner is justified because DOM tests cannot prove responsive composition. Reuse
the Playwright and Axe versions/configuration pattern already present in the
workspace rather than designing a new harness.

### 4.2 Contract ownership

- API projections own displayed facts and allowed actions.
- URL search state owns server-backed Catalog filters.
- Query owns server cache; local React state owns only ephemeral presentation
  such as an open drawer or selected visible panel.
- The production UI maps wire enums to semantic presentation but does not rename
  or reinterpret them.
- If a target layout needs a fact the projection does not provide, record a
  contract gap and omit or explicitly mark the section unavailable. Never fill
  it with prototype data.

### 4.3 Prototype-reference boundary

Mimic the prototype's visual design and layout: shell proportions, navigation
placement, color tokens, typography, spacing, cards, tables, status treatments,
content hierarchy, and responsive composition. Reimplement those qualities with
the current React/Mantine components, production projections, semantic markup,
and accessibility behavior.

Keep the existing production navigation contract exactly as-is:

- `/e2e/catalog`;
- `/e2e/runs`;
- `/e2e/runs/:runId`;
- `/e2e/workspaces`;
- Health as a drawer and Review as a Catalog modal.

The prototype's hash targets are composition references, not routes to restore,
redirect, alias, or expose:

| Prototype reference | Production destination |
| --- | --- |
| `#catalog` | `/e2e/catalog` overview composition |
| `#runtime`, `#manager`, `#observability` | Filtered/browsing states of `/e2e/catalog`; preserve the family rail, result rows, and detail composition without domain routes |
| `#test-detail` | Selected-case panel or sheet within `/e2e/catalog` |
| `#compound` | Compound selection state within Catalog and the existing Review modal |
| `#live-run` | `/e2e/runs/:runId`, using the shared live/historical run composition |
| `#runs` | `/e2e/runs` |
| `#workspaces` | `/e2e/workspaces` |

Do not copy prototype navigation URLs, `:target` CSS routing, hard-coded domain
links, sample values, or static interaction semantics. A visual difference is
required when current route ownership, truthful data, safety, responsive
behavior, or WCAG 2.2 AA demands it.

### 4.4 Working tree

The extracted E2E repository may contain unrelated user changes. Each migration
slice must begin with a status/diff inspection and avoid overwriting or
reformatting unrelated work. Migration commits must contain only the intended
UI slice and its tests.

## 5. Current-to-target mapping

| Current production area | Target change | Contract retained |
| --- | --- | --- |
| Dark horizontal header | Warm shell with desktop sidebar and compact mobile navigation | Four routes and Health drawer |
| Generic Mantine defaults | Explicit theme tokens, typography, borders, shadows, statuses | Mantine behavior |
| Catalog topology cards and button cloud | Overview plus rail/results/detail browse composition | Catalog query, facets, pagination |
| Minimal Review modal | Full review hierarchy and mobile full-screen surface | Preview and admission |
| Minimal Run cards | Hero, progress, first/primary failure, execution tree, detail/evidence | One `RunProjection`, SSE reconciliation |
| Four-column Runs table | Complete operational history and selected detail | Runs projection and deep links |
| Minimal Workspaces cards | Capacity, Template, Active, Quarantine, Recent purges | Server-projected safety |
| Three Health groups | Five operator-decision groups and scoped actions | Health projection |

## 6. Implementation strategy

Migrate route by route over a shared visual foundation. Do not begin with a
general component-library rewrite. A component is extracted only when the same
semantic pattern is used by more than one route or extraction makes the current
slice materially easier to review.

Expected primary files are:

- `e2e/web/src/main.tsx` for the Mantine light theme and provider defaults;
- `e2e/web/src/styles.css` for tokens, shell, responsive grids, status surfaces,
  and focus/motion rules;
- `e2e/web/src/App.tsx` for the first structural slices;
- existing `api.ts`, `types.ts`, and state-copy modules only when a named
  projection or type gap is proven;
- existing component tests plus browser interaction/visual tests.

Do not reorganize the entire frontend before changing the first screen. Extract
route modules during the relevant slice only if `App.tsx` becomes an obstacle to
review or testing.

## 7. Migration stages

### M0 — Freeze behavior and evidence

Deliverables:

1. Record current repository status and preserve unrelated changes.
2. Capture deterministic current-production screenshots at 390, 768, 1024, and
   1440px for the four routes and Review.
3. Register the attached historical JPGs as design references, not automated
   pixel baselines.
4. Freeze fixture responses for Catalog overview/browse/detail, Review states,
   live/terminal Run, partial history, Workspaces, and Health.
5. Inventory every target field missing from current projections.

Exit gate:

- existing build and component tests pass;
- each planned visual screen has a deterministic fixture;
- data gaps have an owner and are not hidden by sample values.

### M1 — Theme and shell

Deliverables:

1. Switch Mantine to the light target theme.
2. Add the layout/theme tokens without copying the 2,756-line prototype CSS.
3. Implement desktop sidebar, top context bar, compact tablet navigation, and
   phone icon navigation.
4. Preserve skip link, route-heading focus, Health drawer, active-route state,
   dynamic domain navigation, and reconnect notice.
5. Establish shared surface, button, field, table, status, identity, empty,
   failure, and loading treatments.

Exit gate:

- all routes render inside the target shell;
- navigation works with pointer and keyboard at every required width;
- no route/API behavior changes;
- Axe runs with color contrast enabled and has no applicable serious violation.

Rollback unit: theme and shell commit.

### M2 — Catalog overview and browse

Deliverables:

1. Add the screenshot-informed editorial heading, search, truthful summary strip,
   diagnostics notice, and dynamic domain cards for unfiltered Catalog.
2. Build the 1440px filter rail/results/detail composition.
3. Build the 1024px rail/results layout with detail sheet.
4. Build full-screen filter and detail surfaces below 1024px.
5. Implement all specified filters, removable chips, pagination, debounced
   search with obsolete-read cancellation, and URL restoration.
6. Preserve exact selection across pages and filters, including expression and
   exclusions when supported by the contract.
7. Complete the case detail order from purpose through source/history.

Exit gate:

- overview and browse visual baselines pass at 390, 1024, and 1440px;
- a keyboard-only user can search, filter, select, paginate, open detail, and
  reach Review;
- a fifth-domain fixture renders without component, icon, route, or CSS change;
- no Catalog request exceeds the interaction design's request budget.

Rollback unit: Catalog commit.

### M3 — Review and admission

Deliverables:

1. Implement Scope, Boundaries, Execution, Evidence and cleanup, Inputs, and
   Preflight in the target raised-surface style.
2. Use a desktop dialog and mobile full-screen surface.
3. Render checking, ready, blocked, stale, error, admission pending, conflict,
   and expired-nonce states with exact copy.
4. Place the exact disabled reason adjacent to Start.
5. Preserve one preview request and one admission request; do not add automatic
   mutation retry.

Exit gate:

- every preview/admission fixture has a component and accessibility assertion;
- duplicate Start is impossible;
- successful admission navigates to the returned run;
- visual baselines pass at 390 and 1440px.

Rollback unit: Review commit.

### M4 — Live and historical Run

Deliverables:

1. Implement slate hero, counts/progress strip, timing, stream freshness, and
   workspace/evidence identity.
2. Render first failure and primary error distinctly.
3. Add execution/case tree, selected case detail, validation and cleanup phases,
   evidence, bounded logs, duration, and not-run reason.
4. Render queued, preparing, running, failure-detected, finalizing, terminal,
   disconnected, recovery, evidence-gap, degraded, unavailable, and purged
   states truthfully.
5. Use only server-projected Cancel and retry permissions.
6. Keep live and historical views on the same `RunProjection` and composition.

Exit gate:

- static projection refresh and SSE replay produce the same DOM truth;
- duplicate/gap/recovery fixtures do not duplicate or fabricate state;
- first failure remains visible at every width;
- keyboard users can inspect evidence, cancel when allowed, and invoke permitted
  retry actions;
- visual baselines pass for live, failed, and recovery states at 390 and 1440px.

Rollback unit: Run commit.

### M5 — Runs, Workspaces, and Health

Deliverables:

1. Complete Runs filters, pagination, current-run callout, full row summary, and
   selected detail.
2. Implement partial and unavailable history without rendering false emptiness.
3. Implement Workspaces sections in the specified order.
4. Render Purge only for a server-projected inactive owned leaf and require a
   semantic confirmation that names retained lineage.
5. Complete all five Health decision groups and their scoped actions.
6. Keep root paths read-only, wrapped, and confined to Health.

Exit gate:

- corrupt-record and directory-failure fixtures remain distinct;
- no destructive action is inferred from client state;
- Runs and Workspaces visual baselines pass at 390, 1024, and 1440px;
- keyboard and screen-reader journeys cover Health and Purge confirmation.

Rollback unit: Runs/Workspaces/Health commit.

### M6 — Responsive, accessibility, and load proof

Deliverables:

1. Exercise 375, 390, 768, 1024, and 1440px plus 200% zoom.
2. Run pointer and keyboard primary/failure journeys.
3. Enable color-contrast checks; do not suppress them.
4. Verify focus trap/return, route-heading focus, live-region throttling, touch
   targets, safe areas, reduced motion, and long-value wrapping.
5. Exercise 10,000 server-paged Catalog cases and a 1,000-case admitted Run.
6. Record any measured need before adding virtualization or another dependency.

Exit gate:

- all interaction acceptance criteria in `e2e-test-ui-design.md` pass;
- no applicable WCAG 2.2 AA violation;
- no page-level horizontal overflow;
- screenshot baselines are stable across two clean runs.

Rollback unit: verification and responsive commit.

### M7 — Cutover and reference retirement

Deliverables:

1. Run the production build and live controller smoke journey.
2. Review side-by-side production screenshots against the attached references.
3. Update documentation status from migration target to implemented.
4. Retain the documentation JPGs.
5. Delete `<E2E_SOURCE_ROOT>/web/prototype` only in a separate commit after
   all visual, interaction, and accessibility gates pass.

Exit gate:

- the production routes are the only served UI;
- the old prototype is no longer required to understand or test the design;
- deletion does not remove the historical Git commits or documentation assets.

Rollback unit: prototype-retirement commit only.

## 8. Required fixture and test matrix

| Surface | Minimum fixtures | Required proof |
| --- | --- | --- |
| Shell | healthy, reconnecting, Health unavailable | route navigation, focus, responsive shell |
| Catalog | loading, overview, browse, empty, refreshing, stale last-good, unavailable, incompatible | request budget, URL state, generic domains, screenshots |
| Review | checking, ready, blocked, stale, error, conflict, expired | exact copy, one mutation, focus trap/return |
| Run | queued, preparing, running, failure/finalizing, each terminal result, disconnected, recovery mismatch | projection equivalence, announcements, actions, screenshots |
| Evidence | complete, truncated, gap, degraded, unavailable, invalid, purged | no fabricated zero, readable disclosure |
| Runs | normal, active, partial, unavailable, empty | truthful empty/error distinction, pagination |
| Workspaces | capacity ready/blocked, template absent/ready, active, eligible/ineligible quarantine, purge partial | server-projected safety and confirmation |
| Health | browse/start/boundary/storage/attention combinations | scoped actions, read-only roots |

Use accessible queries (`getByRole`, `getByLabelText`, and visible state copy) in
component tests. Test IDs are reserved for otherwise inaccessible implementation
hooks, not ordinary user controls.

## 9. Visual regression rules

1. Production screenshots come from deterministic fixtures, a fixed timezone,
   stable fonts, disabled animation, and fixed viewport sizes.
2. Baselines cover route composition and critical state, not every catalog
   record permutation.
3. Keep one desktop and one phone baseline for Catalog, Review, and Run; add
   1024px baselines for layouts whose column model changes there.
4. Mask only genuinely nondeterministic values. Prefer deterministic fixture IDs
   and timestamps over broad masks.
5. A threshold must not hide layout movement, text clipping, missing focus, or a
   changed status color. Update a baseline only with a reviewed reason.
6. Historical JPGs are human design references. New production baselines are
   captured from the implemented React UI.

## 10. Network and performance budgets

- Route navigation must not create per-row requests.
- Catalog uses one server request per page/filter state, plus an explicit refresh
  only when requested.
- Review uses one preview and one admission request.
- Run uses one snapshot query plus one route-scoped event stream.
- Runs, Workspaces, and Health each use their combined projection endpoint.
- Decorative images are not loaded by production; the documentation JPGs are
  not application assets.
- CSS and SVG are sufficient for the visual migration. No image-based UI chrome.

## 11. Safety gates

The migration fails review if it:

- exposes an action because a run or workspace merely looks eligible;
- turns a root/path into an editable control;
- makes a terminal pass visible while cleanup remains unresolved;
- collapses first failure into primary error;
- hides evidence degradation, truncation, or purge behind a normal empty state;
- silently updates a revision-qualified selection;
- retries an admission or destructive mutation automatically;
- uses a prototype value when a projection field is absent.

## 12. Commit and review policy

Use the migration stages as commit boundaries. Every commit must include the
smallest tests that prove its changed behavior and must leave the build green.
Do not mix backend contract expansion, broad frontend reorganization, visual
restyling, and prototype deletion in one commit.

Each review includes:

1. files and existing user changes preserved;
2. fixture/contract delta;
3. desktop and phone screenshots for the affected surface;
4. keyboard and accessibility results;
5. request-count and mutation-safety results;
6. explicit list of remaining migration stages.

## 13. Completion criteria

The UI migration is complete when:

1. all routes use the target shell and theme;
2. all route compositions in the layout/theme document are implemented;
3. every async/failure state in the interaction design has truthful rendering;
4. all five target widths and 200% zoom pass;
5. visual baselines, component tests, build, Axe, and live smoke proof pass;
6. no feature-specific frontend registration exists;
7. no unsafe action is inferred by the client;
8. the documentation screenshots remain available after optional prototype
   retirement.
