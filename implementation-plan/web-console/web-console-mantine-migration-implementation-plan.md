# EphemeralOS web console Mantine migration implementation plan

| Field | Value |
|---|---|
| Status | P00–P12 complete — release gate approved |
| Plan owner | Codex (active implementation agent) |
| Design reviewer | Unassigned |
| Engineering reviewer | Unassigned |
| Accessibility reviewer | Unassigned |
| Security reviewer | Required for Preview |
| Created | 2026-07-11 |
| Last updated | 2026-07-11 |
| Console root | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/web/console` |
| Design proposal | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/web-console/web-console-ui-ux-design-proposal.md` |
| Earlier technology record | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/web-console/web-console-ui-tech-stack-and-library-options.md` |
| Superseding decision record | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/web-console/web-console-mantine-tdr-amendment.md` |
| Evidence root | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/web-console/evidence/web-console-mantine/` |

## 1. Purpose and required outcome

This is the execution plan for migrating the EphemeralOS web console to one
application-wide Mantine component and visual system. Once approved, it
converts the design proposal into ordered, independently reviewable work
packages with explicit dependencies, acceptance criteria, progress tracking,
rollback boundaries, automated verification, and screenshot evidence.

The required end state is decisive:

- Mantine owns application colors, typography, spacing, radii, shadows, focus,
  breakpoints, overlays, forms, notifications, and ordinary components.
- The console has one `MantineProvider` and one EphemeralOS light theme.
- Local Radix wrappers and direct Radix application usage are removed.
- Tailwind component styling, `@theme` tokens, and Tailwind build integration
  are removed. A counted allowlist may exist only during migration.
- React Router, TanStack Query, CodeMirror, uPlot, Lucide, and TanStack Virtual
  remain. TanStack Table becomes the headless engine for operational tables
  rendered with Mantine components.
- React Aria Components is not added unless a recorded parity test proves that
  a Mantine composition cannot satisfy a required collection accessibility or
  scale behavior.
- No community package is treated as official merely because “Mantine” appears
  in its name.
- Every phase leaves the console buildable and produces approved screenshots.

The migration must preserve the compact, light, calm, high-density
operator-console character and all existing backend, polling, lifecycle,
security, routing, and audit boundaries.

## 2. Fixed product and layout decisions

These decisions are not reopened by routine implementation work:

1. **Canonical logo and theme source.** The visual source is
   `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/web/console/dist/assets/images/logo.png`.
   Phase 1 must register those canonical pixels as a durable source/static
   asset so application source does not depend on generated `dist` output.
   Theme colors are derived from the logo's warm neutral environment and
   eye-blue interaction accent, then completed and contrast-tested as Mantine
   color scales.
2. **Fleet uses Flexbox.** The Fleet collection uses a wrapping Flexbox, not a
   final CSS Grid card layout. Cards do not grow to fill a partial row.
3. **Fleet card bounds.** Below 768px cards are full-width. At 768px and above,
   each card is no wider than 28rem; at every viewport it is no taller than
   22rem. The layout remains start-aligned on wide screens. Essential status
   and actions must not be clipped to satisfy the height bound.
4. **Exceptional Grid is local.** Local CSS Grid modules remain valid for true
   `minmax()` split panes, dense label/value layouts, and waterfall geometry
   that Mantine layout primitives cannot express cleanly.
5. **One scroll owner.** Every route and pane has one intentional scroll owner.
   Mantine `ScrollArea` is not placed around the direct viewports owned by
   TanStack Virtual, CodeMirror, or uPlot.
6. **Desktop-first, responsive fallback.** Dense split panes remain on desktop;
   narrow widths use Drawers and stacked layouts with focus restoration.

## 3. Scope, authority, and non-goals

### 3.1 In scope

- Mantine dependency/compatibility validation and exact-version selection.
- Theme, provider, global-style, and component-default foundation.
- Migration of Shell, navigation, Fleet, Overview, Terminal, Observability,
  Files, and approved Preview controls.
- Migration of all local ordinary primitives and feedback patterns.
- Table, tree, combobox, virtualization, CodeMirror, and uPlot integration.
- Removal of Radix and permanent Tailwind visual architecture.
- Visual, responsive, accessibility, correctness, polling, security, and
  performance verification.
- Evidence capture and progress reporting for every phase.

### 3.2 Out of scope

- Inventing backend fields, richer Fleet metadata, or unsupported correlations.
- Replacing React Router, TanStack Query, CodeMirror, uPlot, Lucide, or
  TanStack Virtual without a separately approved technical finding.
- Treating Mantine as a fix for Preview origin isolation, file CAS, missing
  command history, trace enumeration, or pagination API gaps.
- Redesigning lifecycle semantics or route/deep-link contracts.
- Editing the earlier technology decision record in this plan. It still
  recommends local Tailwind/Radix composition and must be superseded or amended
  by a separately authorized decision-record change.

No console implementation phase may become Ready until that separate change
is authorized and approved. This plan records the dependency but does not
silently rewrite the historical decision.

### 3.3 Source-of-truth order

When implementation details disagree, use this order:

1. Current backend/API contracts and security boundaries.
2. This implementation plan's gates and fixed decisions.
3. The web-console UI/UX design proposal.
4. Current official Mantine documentation for the pinned version.
5. Existing console behavior, unless identified as a correctness defect.
6. The older technology record, which is historical until superseded.

## 4. Delivery governance

### 4.1 Status model

| Status | Meaning |
|---|---|
| Not ready | A dependency, owner, reviewer, fixture, command, decision, or evidence plan is missing. |
| Ready | Entry criteria are complete and implementation may start. |
| In progress | Source changes or fixtures are actively being developed. |
| In review | Implementation and evidence are complete; approval is pending. |
| Blocked | A named external decision or failed gate prevents useful in-scope progress. |
| Complete | All acceptance, automated, screenshot, and sign-off gates pass. |

Screenshot status is tracked separately as `Not started`, `Capturing`,
`Review required`, `Rejected`, or `Approved`. A phase-wide screenshot `N/A` is
not permitted while the console remains runnable. The manifest also records an
artifact mode: standard `triad`, P00 `baseline-only`, or disposable P00
`fixture-only`. Artifact mode does not replace the screenshot review status.

### 4.2 Five progress gates

Every phase advances through the same gates. The tracker records `0/5` through
`5/5`:

- **G1 — Ready:** scope, owner, reviewer, dependency, fixtures, commands,
  acceptance IDs, screenshot cases, and rollback boundary are locked.
- **G2 — Implemented:** the phase deliverables are complete and the console is
  buildable at the phase commit.
- **G3 — Verified:** required automated build, test, accessibility, polling,
  security, and performance evidence passes.
- **G4 — Visually approved:** every required artifact and applicable diff
  exists, review is complete, and the screenshot pack is Approved.
- **G5 — Signed off:** acceptance is `passed/total`, evidence links resolve,
  reviewers and date are recorded, and the next baseline is promoted where
  applicable.

### 4.3 Entry and exit rules

- Phases merge in order. Preparation may run in parallel, but a phase cannot
  merge before its dependency is Complete.
- Use one implementation PR or otherwise reviewable commit range per phase.
- A failed gate leaves the phase In progress or Blocked; attempted work is not
  progress evidence.
- Phase 8 has Files (8A) and Preview (8B) subtracks. An unresolved Preview
  isolation decision blocks only 8B, not Files or earlier migration work.
- Any scope exception records the owner, reason, risk, expiry phase, and removal
  acceptance criterion. No exception may create a permanent second visual
  system.

## 5. Master progress tracker

All phases are initially Not ready because the proposal is awaiting approval
and owners, reviewers, commands, PRs, and evidence packs are unassigned. Update
this table in the same change that advances a phase.

| Phase | Dependency | Status | Gates | Acceptance | Owner / reviewer | Automated evidence | Screenshot evidence | Blocker or decision | Updated |
|---|---|---|---:|---:|---|---|---|---|---|
| P00 — Compatibility and trust gate | Authorized amendment record | Complete | 5/5 | 6/6 | Codex / Codex evidence self-review | [Approved P00 fixture evidence](evidence/web-console-mantine/phase-00/0f7d024867fc/) | [Approved — P00 fixture-only SS01–SS03](evidence/web-console-mantine/phase-00/0f7d024867fc/) | D02 deferred to P08B; resolved in P08B `cfae89ede9` | 2026-07-11 |
| P01 — Theme and tokens | P00 | Complete | 5/5 | 5/5 | Codex / Codex evidence self-review | [Verified P01 implementation evidence](evidence/web-console-mantine/phase-01/0ce628786a83/) | [Approved — P01 fixture SS01–SS03](evidence/web-console-mantine/phase-01/0ce628786a83/) | D05 implemented; final theme consumes it | 2026-07-11 |
| P02 — Provider and globals | P01 | Complete | 5/5 | 5/5 | Codex / Codex evidence self-review | [Verified P02 implementation evidence](evidence/web-console-mantine/phase-02/b042d34ab/) | [Approved — P02 foundation fixture SS01–SS03](evidence/web-console-mantine/phase-02/b042d34ab/) | Historical removal-only allowlist retired in P10; zero styling residue | 2026-07-11 |
| P03 — Primitives | P02 | Complete | 5/5 | 5/5 | Codex / Codex evidence self-review | [Verified P03 implementation evidence](evidence/web-console-mantine/phase-03/aac65f046/) | [Approved — P03 primitive SS01–SS03](evidence/web-console-mantine/phase-03/aac65f046/) | Historical cleanup completed in P09/P10 | 2026-07-11 |
| P04 — Shell and navigation | P03 | Complete | 5/5 | 5/5 | Codex / Codex evidence self-review | [Verified P04 implementation evidence](evidence/web-console-mantine/phase-04/8139d292a/) | [Approved — P04 Shell/navigation SS01–SS03](evidence/web-console-mantine/phase-04/8139d292a/) | D02 deferred to P08B; resolved in P08B `cfae89ede9` | 2026-07-11 |
| P05 — Fleet and Overview | P04 | Complete | 5/5 | 6/6 | Codex / Codex evidence self-review | [Verified P05 implementation evidence](evidence/web-console-mantine/phase-05/0173407bc/) | [Approved — P05 Fleet/Overview SS01–SS04](evidence/web-console-mantine/phase-05/0173407bc/) | D02 deferred to P08B; resolved in P08B `cfae89ede9` | 2026-07-11 |
| P06 — Terminal | P05 | Complete | 5/5 | 6/6 | Codex / Codex evidence self-review | [Verified P06 implementation evidence](evidence/web-console-mantine/phase-06/9bc8d4107/) | [Approved — P06 Terminal SS01–SS03](evidence/web-console-mantine/phase-06/9bc8d4107/) | D02 deferred to P08B; resolved in P08B `cfae89ede9` | 2026-07-11 |
| P07 — Observability | P06 | Complete | 5/5 | 6/6 | Codex / Codex evidence self-review | [Verified P07 implementation evidence](evidence/web-console-mantine/phase-07/91e1b2688/) | [Approved — P07 Observability SS01–SS04](evidence/web-console-mantine/phase-07/91e1b2688/) | D02 deferred to P08B; resolved in P08B `cfae89ede9` | 2026-07-11 |
| P08 — Files and Preview | P07 | Complete | 5/5 | 6/6 | Codex / Codex delegated evidence and security self-review | [P08A Files evidence](evidence/web-console-mantine/phase-08/f1073cd29/); [P08B Preview evidence](evidence/web-console-mantine/phase-08/cfae89ede9/) | [Approved — P08 complete](evidence/web-console-mantine/phase-08/cfae89ede9/) | D02 resolved; verified through P12 | 2026-07-11 |
| P09 — Remove Radix | P08 | Complete | 5/5 | 4/4 | Codex / Codex evidence self-review | [Verified P09 cleanup evidence](evidence/web-console-mantine/phase-09/29c36d2cd/) | [Approved — P09 interaction and route triads](evidence/web-console-mantine/phase-09/29c36d2cd/) | Zero Radix runtime/dependency residue; verified through P12 | 2026-07-11 |
| P10 — Remove Tailwind | P09 | Complete | 5/5 | 4/4 | Codex / Codex evidence self-review | [Verified P10 styling evidence](evidence/web-console-mantine/phase-10/934429874/) | [Approved — P10 four-viewport styling triads](evidence/web-console-mantine/phase-10/934429874/) | Mantine is the sole styling/token system; verified through P12 | 2026-07-11 |
| P11 — Dependency cleanup | P10 | Complete | 5/5 | 4/4 | Codex / Codex evidence self-review | [Verified P11 cleanup evidence](evidence/web-console-mantine/phase-11/30064b91c/) | [Approved — P11 exact P10-to-P11 triads](evidence/web-console-mantine/phase-11/30064b91c/) | Cleanup retained through P12 | 2026-07-11 |
| P12 — Release gate | P11 | Complete | 5/5 | 7/7 | Codex / Codex implementation-agent evidence self-review | [Verified P12 release evidence](evidence/web-console-mantine/phase-12/8f9e7b741/) | [Approved — P12 complete visual, accessibility, performance, polling, and cross-browser report](evidence/web-console-mantine/phase-12/8f9e7b741/) | P00–P12 complete; no failed release gates | 2026-07-11 |

As soon as a pack exists, replace `Not started` with a relative link whose
label is the current screenshot status, such as `[Capturing](...)` or
`[Review required](...)`. Use `[Approved](...)` only after G4 sign-off. Do not
report subjective percentages.

## 6. Screenshot and evidence contract

### 6.1 Evidence-pack structure

Store each immutable pack under:

`evidence/web-console-mantine/phase-XX/<short-console-sha>/`

Except for the P00 `baseline-only` and `fixture-only` artifact modes defined in
section 6.3, each pack contains:

```text
index.md
manifest.json
screenshots/
  pXX__surface__state__viewport__interaction__reference.png
  pXX__surface__state__viewport__interaction__actual.png
  pXX__surface__state__viewport__interaction__diff.png
```

- `index.md` records expected changes, exceptions, automated artifact links,
  reviewer, review date, and approval decision.
- `manifest.json` records phase/evidence IDs, route/query state, fixture and
  schema version, console/document commits, PR, baseline, capture environment,
  interaction sequence, masks, image hashes, diff result, DOM assertions,
  reviewer, and status.
- Raw browser traces, logs, axe output, performance data, and network
  assertions may remain CI artifacts but must be linked from `index.md`.

### 6.2 Standard capture environment

| Viewport | Dimensions | Required purpose |
|---|---:|---|
| Narrow phone | 375 x 812 | Single-column controls, full-width Fleet cards, Drawers, touch/focus containment |
| Tablet boundary | 768 x 1024 | Breakpoint transitions and wrapped toolbars |
| Compact desktop | 1024 x 768 | Split-pane threshold and bounded content |
| Wide desktop | 1440 x 900 | Dense operator layout, partial Fleet rows, overlays, long data |
| Fleet wide proof | 1920 x 1080 | P05 and P12 only; card max-width/max-height and start alignment |

Use production builds except for the disposable P00 spike. Pin Chromium,
operating-system image, fonts, device scale factor 1, zoom 100%, locale, and
timezone. P12 adds representative Firefox and WebKit sentinels.

Use deterministic sanitized fixtures based only on existing API types. Freeze
time and random identifiers where practical. Never capture credentials,
tokens, private command output, or invented fields.

Wait for fonts, initial queries, relevant portals, and layout stabilization.
Use viewport screenshots, not full-page captures, so body overflow and bounded
scroll failures remain visible. Ordinary captures disable incidental animation;
a separate reduced-motion case is required. Focus evidence must be produced by
real keyboard navigation.

### 6.3 Baseline and diff policy

- P00 establishes the pre-migration route atlas. `baseline-only` atlas records
  contain an immutable `reference` image because no earlier actual/diff exists.
  P00 trust corrections require full triads against that baseline; disposable
  spike-only cases may use `fixture-only` mode with an `actual` image and an
  explicit reviewer decision. Both exception modes still receive one of the
  screenshot review statuses defined in section 4.1.
- Each later phase compares unchanged surfaces with the latest approved
  baseline and changed surfaces with an explicitly approved target.
- Preserve reference, actual, and diff originals. Promote an actual only after
  design and engineering approval.
- Start with at most 0.1% changed pixels in unchanged regions. Cleanup phases
  expect exact equivalence; any nonzero diff requires review.
- Numeric tolerance never excuses clipping, overflow, focus loss, unstable
  wrapping, unreadable contrast, content jump, or polling-driven layout shift.
- Nonvisual phases still capture UI sentinels at 375 x 812 and 1440 x 900.
  Screenshots of terminal output or dependency files do not count as UI proof.

Fleet manifests record each visible card's computed width and height, Flexbox
container dimensions, row position, `flex-grow` result, body overflow, and
scroll owner.

## 7. Verification system

Only `npm run build` exists in the console package today. P00 must record the
exact package-manager invocation and establish reviewable commands for every
new verification layer before later phases claim them.

| Layer | Purpose | Required by |
|---|---|---|
| Production build | TypeScript project build plus Vite production bundle | Every phase |
| Unit/contract fixtures | State mappings, absolute times, input dispatch, cache keys, request shaping | P00 onward |
| Component interaction | Forms, Combobox, Tree, Table, overlays, notifications, keyboard behavior | P02 onward |
| Route/browser smoke | Existing routes, redirects, filters, query strings, deep links, scroll owners | P04 onward |
| Accessibility | axe, keyboard scripts, focus trap/restoration, screen-reader manual protocol | Relevant phase and P12 |
| Visual regression | Pinned screenshots and diff manifest | Every phase |
| Polling stability | Focus, selection, scroll, overlay, last-good-data, poller-count assertions | P00 and live surfaces |
| Performance | Production fixtures on recorded reference machine | P05–P08 and P12 |
| Dependency/source audit | Zero-result searches, graph/lockfile review, exact Mantine versions | P00, P09–P12 |
| Security | Preview isolation, notification disclosure, sanitized evidence | P00, P08, P12 |

## 8. Phase work packages

### P00 — Mantine compatibility spike and trust gate

**Objective:** establish a go/no-go version baseline, complete the migration
inventory, and close finite high-priority trust defects before visual work can
hide them.

**Primary work:**

- Pin one compatible version across `@mantine/core`, `@mantine/hooks`,
  `@mantine/form`, and `@mantine/notifications`.
- Spike React/Vite/TypeScript, CSS order, portals, overlays, notifications,
  Tree/virtual tree, Combobox/virtual options, CodeMirror, and uPlot.
- Count Radix wrappers/imports, Tailwind utilities, `@theme` tokens, global
  styles, providers, and cleanup dependencies.
- Correct event absolute-time/Pause behavior, trace-event shape, duplicate
  stdin dispatch, publication rejection display, transcript isolation,
  file-draft preservation, Fleet list generation, and ready-sandbox polling.
- Assign and record the Preview isolation decision owner.

**Acceptance criteria:**

- [x] **P00-AC01:** Exact versions pass React, Vite, TypeScript, production
  build, and stylesheet-order verification; commands and version matrix are
  recorded.
- [x] **P00-AC02:** The disposable integration fixture passes portal, focus,
  restoration, reduced-motion, keyboard, virtualization, CodeMirror, and uPlot
  checks.
- [x] **P00-AC03:** Starting inventories, replacement targets, deletion phases,
  and rollback/removal procedure are recorded.
- [x] **P00-AC04:** All named correctness/trust fixtures pass with network-level
  evidence where screenshots cannot prove semantics. Polling retains the
  current 400ms fast/2s slow cadence, hidden-tab pause, focus catch-up, 15s
  idle decay, and 8s ceiling unless a separately measured change is approved.
- [x] **P00-AC05:** D02 assigns the Security reviewer role as the P08B
  decision/sign-off authority, the test boundary is recorded, and the
  unresolved policy is scoped only to P08B.
- [x] **P00-AC06:** Build/test artifacts and the P00 fixture-only screenshot
  pack are Approved; a failed spike is removed without changing production
  providers.

**Required screenshot evidence:**

- [x] **P00-SS01:** Pre-migration Shell, Fleet, Overview, Terminal, Resources,
  Events, Traces, Layers, Files, and Preview at all four standard viewports.
- [x] **P00-SS02:** Mantine spike at 375 and 1440 showing theme, form validation,
  real keyboard focus, Modal or Drawer, Tooltip, and notification.
- [x] **P00-SS03:** Paused Events, publication rejection, and a file conflict
  with its local draft visibly preserved at 375 and 1440.

**Rollback boundary:** remove all spike-only code and dependencies; retain only
independently reviewed correctness fixes and evidence.

**P00 implementation record (2026-07-11):** `@mantine/core`,
`@mantine/form`, `@mantine/hooks`, and `@mantine/notifications` are pinned to
9.4.1. The npm metadata for `@mantine/core@9.4.1` declares React and React DOM
`^19.2.0` plus `@mantine/hooks` 9.4.1; the tested installation is React and
React DOM 19.2.7, TypeScript 6.0.3, Vite 8.1.3, Node 24.14.0, and Playwright
1.61.1. The inventory records 410 `className` expressions across 39 source
files, two Tailwind directives/tokens, seven direct Radix dependencies, and
five Radix source imports. Replacement/removal ownership remains P02 for the
provider/global styles, P03 for primitives/feedback, P04–P08 for surfaces,
P09 for Radix, P10 for Tailwind, and P11 for dependency removal. The
[provisional fixture pack](evidence/web-console-mantine/phase-00/0f7d024867fc/)
contains the commands and hashes. A deterministic browser route-interception
fixture now verifies actual requests at the 400ms fast cadence and the
window-focus catch-up request; P00-AC04 is complete. The same pack now contains
a 36-image sanitized route atlas covering SS01 at 375, 768, 1024, and 1440,
captured from committed console revision `8153d6f43` with recorded Chromium,
macOS, and font-inventory metadata. The fixture pack was reviewed by Codex at
`2026-07-11T09:11:53Z` after the exact Node 24.14.0 unit, build, and browser
commands were re-run and the 36 SS01 checksums were verified. It is approved
for P00 fixture evidence only, not as a final migrated visual baseline.

The pending Preview boundary, required P00 owners, and the minimum P08B test
contract are recorded in the [P00 review and Preview-isolation decision
record](evidence/web-console-mantine/phase-00/0f7d024867fc/review-decision.md).
It is evidence only: it does not select an isolation approach or grant an
external security authorization. Consistent with the authorized amendment, the
open D02 security decision is a P08B blocker only; it does not block
non-Preview migration work.

### P01 — Logo-led theme and token mapping

**Objective:** define the sole EphemeralOS Mantine theme before migrating
production components.

**Primary work:**

- Register the canonical logo pixels in a durable source/static asset path.
- Build complete, contrast-tested light-theme scales from the logo anchors.
- Map typography/monospace roles, spacing, radii, shadows, focus, breakpoints,
  overlays, z-index, compact sizes, variants, and lifecycle states.
- Mirror breakpoints for CSS Modules and add a theme/static-value drift check.

**Acceptance criteria:**

- [x] **P01-AC01:** The logo source is durable, production-build safe, and
  independent of generated `dist` imports.
- [x] **P01-AC02:** The theme completely owns approved visual tokens and
  breakpoint/z-index behavior.
- [x] **P01-AC03:** Defaults and variants preserve the compact, calm,
  high-density operator-console character rather than default-dashboard styling.
- [x] **P01-AC04:** Contrast, real focus, reduced motion, logo sizing, and
  breakpoint drift pass.
- [x] **P01-AC05:** Theme fixtures and screenshot pack are Approved for P01
  fixture scope; no production-screen visual baseline is implied.

**Required screenshot evidence:**

- [x] **P01-SS01:** Theme specimen at all four viewports with logo, sans/mono
  typography, palette, spacing, radii, shadows, statuses, and focus.
- [x] **P01-SS02:** Hover, selected, disabled, loading, stale, error,
  destructive, and keyboard-focus states at 375 and 1440.
- [x] **P01-SS03:** Reduced-motion and logo/header detail proving no crop,
  distortion, layout shift, or duplicate accessible naming.

**Rollback boundary:** theme fixtures and asset registration only; no production
screen depends on the theme until P02.

**Implementation and review record:** committed console revision
[`0ce628786a83`](evidence/web-console-mantine/phase-01/0ce628786a83/) adds the
durable `public/assets/images/logo.png` asset, complete light Mantine theme,
CSS-module breakpoint mirror, unit drift/contrast checks, and an isolated
fixture. The recorded logo is bit-identical (SHA-256
`42a06f2cdf37becedf0b4436fdcb6fd8cee4e6a93120cfbd4cee727ba84fc81a`) to
historical canonical source `f3bd2ab6451038731b8782906b28d02fd751eca9:asset/logo.png`;
the earlier generated `dist` path is not imported. The
[P01 evidence pack](evidence/web-console-mantine/phase-01/0ce628786a83/) records
the passing tests, build asset checksum, four viewport captures, state captures,
reduced-motion/logo checks, zero-Axe scan, and reviewed reference/actual/diff
triads. Codex explicitly approved this as P01 fixture evidence after inspection;
an external human design reviewer remains unassigned, and this is not a final
production-screen visual approval.

### P02 — Provider and global-style foundation

**Objective:** introduce the single Mantine root without destabilizing legacy
routes.

**Primary work:**

- Add one `MantineProvider` and one Notifications host while retaining Query
  and Router.
- Establish Core/Notifications stylesheet order and minimal global containment.
- Add shared test renderers, jsdom mocks, and browser portal/focus fixtures.
- Freeze and count a temporary Tailwind allowlist; reject new utility styling.

**Acceptance criteria:**

- [x] **P02-AC01:** Exactly one provider/notification host exists and Query/
  Router behavior remains compatible.
- [x] **P02-AC02:** There is no duplicate reset, competing theme, body overflow,
  or typography drift.
- [x] **P02-AC03:** Portal, Modal, Drawer, Tooltip, notification, focus-trap,
  Escape, and restoration fixtures pass.
- [x] **P02-AC04:** Legacy and migrated surfaces coexist buildably; the
  Tailwind allowlist is counted and CI-enforced.
- [x] **P02-AC05:** Production build, automated foundation checks, and
  screenshot pack are Approved.

**Required screenshot evidence:**

- [x] **P02-SS01:** Shell under the shared provider at all four viewports with a
  migrated primitive beside an unchanged legacy surface.
- [x] **P02-SS02:** Notification, Modal, Drawer, and Tooltip at 375 and 1440 with
  trigger, backdrop where applicable, portal stacking, and visible focus.
- [x] **P02-SS03:** Root sizing, typography, scroll ownership, and no-reset-drift
  sentinels.

**Rollback boundary:** root-provider and stylesheet-order commit can be reverted
without removing P01 theme assets or fixtures.

**Implementation and review record:** committed console revision
[`b042d34ab`](evidence/web-console-mantine/phase-02/b042d34ab/) adds the sole
production `MantineProvider` and `Notifications` host in `AppProviders`, while
preserving Query, Router, and temporary legacy feedback providers. Core styles,
Notifications styles, and legacy global styles have asserted import order;
minimal root height containment and four viewport sentinels reject reset,
typography, overflow, and scroll-owner drift. The phase freezes the temporary
Tailwind allowlist at 410 `className` expressions, 431 static parts, five
dynamic expressions, and 259 tokens; the P02 unit contract is removal-only.
The [P02 evidence pack](evidence/web-console-mantine/phase-02/b042d34ab/)
records passing Node 24.14.0 unit tests, production build, 62 browser checks,
zero-Axe P02 fixture scan, portal/focus behavior, screenshot triads, and
checksum manifest. Codex self-reviewed the foundation scope after visual
inspection. External human design, engineering, and accessibility reviewers are
still unassigned; P03 must migrate ordinary primitives before any final
production-screen approval.

### P03 — Ordinary primitive migration

**Objective:** replace shared visual primitives before page migration.

Track independently reviewable subgroups: **3A inputs/forms**, **3B overlays
and navigation**, and **3C feedback/display**.

**Primary work:**

- Migrate Button/ActionIcon, inputs/Textarea, Select/Combobox, Modal, Drawer,
  Popover, Tooltip, Tabs, Menu, notifications, Badge/status, Paper/Card,
  Skeleton/loading/error/empty, Breadcrumbs, and ordinary ScrollArea.
- Preserve product-specific StateBadge, RPC normalization, notification limits,
  dismissal, and durable inline error behavior.
- Allow adapters only for EphemeralOS semantics, never to clone the old Radix
  API.

**Acceptance criteria:**

- [x] **P03-AC01:** Every migration-map primitive is accounted for and subgroup
  counts show migrated versus remaining usage.
- [x] **P03-AC02:** Lifecycle, error, notification, and destructive semantics
  remain correct.
- [x] **P03-AC03:** Keyboard, axe, labels/errors, focus, portal/restoration,
  contrast, and reduced-motion tests pass.
- [x] **P03-AC04:** No new feature imports local Radix; each adapter has a
  documented product-semantic purpose and deletion/retention decision.
- [x] **P03-AC05:** Inventory, automated reports, and screenshot pack are
  Approved.

**Required screenshot evidence:**

- [x] **P03-SS01:** Complete primitive gallery at all four viewports.
- [x] **P03-SS02:** Form validation, Select/Combobox, loading, empty, error,
  status, surface, and Skeleton cases at 375 and 1440.
- [x] **P03-SS03:** Menu, Tabs, Popover, Tooltip, Modal, Drawer, and notification
  stack at 375 and 1440 with real keyboard focus.

**Rollback boundary:** subgroup commits remain separately revertible until the
first consuming page phase merges.

**Implementation and review record:** committed console revision
[`aac65f046`](evidence/web-console-mantine/phase-03/aac65f046/) deletes the
six local shared UI wrappers and migrates all mapped ordinary primitives to
Mantine. The only retained product-semantic components are `ErrorToast`, which
normalizes RPC errors before dispatching to Mantine's shared four-item,
dismissible notification host, and `StateBadge`, which maps the EphemeralOS
status vocabulary onto Mantine `Badge`. The [P03 evidence pack](evidence/web-console-mantine/phase-03/aac65f046/)
records the full Node 24.14.0 unit/build/browser pass, nine dedicated P03
browser checks, zero-Axe gallery scan, keyboard portal/focus restoration,
responsive captures, zero-difference screenshot triads, and checksum manifest.
Codex self-reviewed the primitive scope after visual inspection. External
human design, engineering, and accessibility reviewers remain unassigned; P04
may consume the completed primitive foundation.

### P04 — Shell, routing, and navigation

**Objective:** migrate the stable application frame and route navigation.

**Primary work:**

- Migrate Shell to AppShell/Group/Breadcrumbs and the canonical logo Image.
- Migrate sandbox Tabs and Observability subnavigation.
- Canonicalize Layers under Observability while preserving redirects/deep links.
- Replace unsafe unmodified global numeric shortcuts.
- Enforce one semantic main region and one route scroll owner.

**Acceptance criteria:**

- [x] **P04-AC01:** Shell, header, logo, breadcrumbs, route Tabs, and
  Observability navigation use Mantine and preserve density.
- [x] **P04-AC02:** All routes, redirects, filters, query parameters, and deep
  links resolve with correct active navigation.
- [x] **P04-AC03:** Every viewport has one main region, one route scroll owner,
  no body overflow, and no clipped focus ring.
- [x] **P04-AC04:** Skip/main, narrow navigation, scoped shortcuts, keyboard
  focus, and focus restoration pass.
- [x] **P04-AC05:** Route/deep-link reports and screenshot pack are Approved.

**Required screenshot evidence:**

- [x] **P04-SS01:** Every Shell/navigation route state at all four viewports.
- [x] **P04-SS02:** Narrow navigation Drawer/Menu open at 375 with trigger,
  backdrop, focused item, and restored focus.
- [x] **P04-SS03:** Keyboard focus and bounded route scrolling at 1024 plus
  overflow assertions at all widths.

**Rollback boundary:** page content remains unchanged; Shell/navigation changes
are isolated from Fleet and sandbox feature migrations.

**Implementation and review record (2026-07-11):** committed console revision
[`8139d292a`](evidence/web-console-mantine/phase-04/8139d292a/) replaces the
stable application frame with Mantine AppShell/navigation primitives, preserves
the legacy Layers deep link with search/hash retention, and enforces semantic
main plus bounded route scrolling. The [P04 evidence pack](evidence/web-console-mantine/phase-04/8139d292a/)
records the Node 24.14.0 unit/build/browser pass, 36 route-atlas structural
states across the four standard viewports, legacy redirect coverage, skip/main
and scoped keyboard/scroll coverage, narrow Drawer focus/Escape/restoration,
and 38 zero-difference screenshot triads with checksums. Codex self-reviewed
the committed P04 scope after visual inspection. External human design,
engineering, and accessibility reviewers remain unassigned; P05 may consume
the completed frame. P08B Preview isolation remains a separate security gate.

### P05 — Fleet, creation, WorkspacePicker, and Overview

**Objective:** migrate the primary operational landing experience and prove the
non-stretching Flexbox card model.

**Primary work:**

- Migrate creation, searchable/virtual WorkspacePicker, Fleet summary/toolbar/
  cards, sandbox header, metric strip, and Overview panels.
- Remove Layers/Squash from Fleet and use one list generation.
- Implement deterministic loading, fresh, stale, error, empty, mixed,
  truncated, one-card, full-row, partial-row, and large-list states.

**Acceptance criteria:**

- [x] **P05-AC01:** All named surfaces use Mantine and show only supported API
  fields; Layers/Squash are absent from Fleet.
- [x] **P05-AC02:** Fleet uses wrapping Flexbox; below 768px cards are full
  width, at 768px and above width is at most 28rem, height is always at most
  22rem, partial rows are start-aligned, and cards do not grow.
- [x] **P05-AC03:** Summary/cards share one authoritative generation; polling
  does not reorder a focused card or remove/blur an active control.
- [x] **P05-AC04:** Every defined query/data state passes without layout shift,
  unsupported metadata, or clipped essential actions.
- [x] **P05-AC05:** WorkspacePicker search, keyboard model, virtualization,
  explicit first-500-directory truncation label, draft preservation, and focus
  restoration pass.
- [x] **P05-AC06:** Geometry, polling, accessibility, performance, and
  screenshot evidence are Approved.

**Required screenshot evidence:**

- [x] **P05-SS01:** Fleet and Overview at all four viewports with one-card,
  full-row, and partial-row fixtures.
- [x] **P05-SS02:** Fleet at 1440 and 1920 visibly start-aligned/non-stretched;
  manifest measurements prove every visible card is within 28rem by 22rem.
- [x] **P05-SS03:** Full-width cards below 768, creation, and WorkspacePicker
  open with keyboard focus.
- [x] **P05-SS04:** Loading, fresh, stale, error, empty, mixed, truncated, and
  polling-update states at required narrow/wide widths.

**Rollback boundary:** Fleet/Overview route group can revert while retaining the
shared provider, theme, primitives, and Shell.

**Implementation and review record (2026-07-11):** committed console revision
[`0173407bc`](evidence/web-console-mantine/phase-05/0173407bc/) migrates the
Fleet, creation, virtual WorkspacePicker, sandbox header, and Overview surfaces
to Mantine. Fleet now uses bounded start-aligned Flex rows and one authoritative
slow/fast list generation; it retains the last confirmed list on refresh error.
The Fleet-specific Layers/Squash controls are removed while the sandbox-header
Squash control remains in its separate detail scope. The
[P05 evidence pack](evidence/web-console-mantine/phase-05/0173407bc/) records
the Node 24.14.0 unit/build/browser passes (17 files/34 tests and 125 browser
checks), 16 zero-difference screenshot triads across Fleet, creation,
WorkspacePicker, and Overview, the 10,000-folder virtual-search bound, and
geometry/accessibility checks. Systematic debugging identified and corrected
the nested Escape focus handoff and transient Axe audit timing before approval.
Codex self-reviewed the committed P05 scope after visual inspection. External
human design, engineering, and accessibility reviewers remain unassigned; P06
may consume P05. P08B Preview isolation remains a separate security gate.

### P06 — Terminal workspace

**Objective:** migrate Terminal chrome without weakening transcript, input, or
polling correctness.

**Primary work:**

- Migrate Sessions Drawer/rail, toolbar, composer, CommandCard, transcript
  chrome, stdin controls, and result/publication feedback.
- Preserve TanStack Virtual, pages/offsets, tail pinning, and one transcript
  scroll owner.
- Separate history filtering from execution target and bound/consolidate
  pollers.

**Acceptance criteria:**

- [x] **P06-AC01:** All Terminal chrome uses Mantine while virtualizer identity,
  paging, offsets, tail intent, and the native transcript viewport stay stable.
- [x] **P06-AC02:** Ctrl-C/Ctrl-D sends one RPC; `publish_rejected` and
  `publish_reject_class` drive the authoritative final outcome; unknown or
  expired commands cannot appear as successful empty output; transcript caches
  are sandbox-scoped.
- [x] **P06-AC03:** Timeout errors associate and block submit; history filtering
  is distinct from execution target; desktop/narrow flows are accessible.
- [x] **P06-AC04:** 10,000-line and 10,000-character fixtures have bounded DOM,
  no overlap/jump, and meet Terminal performance targets.
- [x] **P06-AC05:** Poller count is bounded; polling preserves focus, selection,
  scroll intent, tail state, and overlays.
- [x] **P06-AC06:** Correctness, polling, performance, accessibility, and
  screenshot evidence are Approved.

**Required screenshot evidence:**

- [x] **P06-SS01:** Desktop split and narrow Drawer/stack layouts at all four
  viewports with one visible transcript scroll owner.
- [x] **P06-SS02:** Session selection, composer focus, invalid timeout, running,
  stale, failed/completed, and publication-rejection states at 375 and 1440.
- [x] **P06-SS03:** 10,000-line mid-scroll/tail and 10,000-character-line
  containment captures.

**Rollback boundary:** Terminal route group can revert independently; no
transcript/cache schema migration is irreversible.

**Completion record:** Console revision `9bc8d4107` migrates the Terminal
workspace chrome to Mantine while retaining the TanStack Virtual transcript
viewport and page/offset protocol. A route-level provider owns the bounded
transcript poller (maximum four callbacks per round), cache keys remain
sandbox-scoped, and a history selection does not change the command execution
target. The [P06 evidence pack](evidence/web-console-mantine/phase-06/9bc8d4107/)
records the Node 24.14.0 unit/build/browser passes (17 files/34 tests and 134
browser checks), nine dedicated Terminal checks, eight zero-difference
screenshot triads, 10,000-line/character containment, keyboard and Axe
coverage, and the tail/error-rendering fixes found through systematic
debugging. Codex self-reviewed the committed P06 boundary after visual
inspection. External human design, engineering, and accessibility reviewers
remain unassigned; P07 may consume P06. P08B Preview isolation remains a
separate security gate.

### P07 — Observability

**Objective:** migrate Resources, Events, Traces, Layers, and logs while
stabilizing live-table/chart/trace behavior.

**Primary work:**

- Use Mantine surfaces, controls, Tabs, Drawers, and feedback.
- Adopt TanStack Table as the headless Events engine rendered with Mantine
  Table; apply TanStack Virtual only at measured scale.
- Keep uPlot instances stable and expose numerical summaries.
- Virtualize flattened spans when the 2,000-span fixture requires it.

**Acceptance criteria:**

- [x] **P07-AC01:** All observability surfaces use Mantine and retain route/URL
  compatibility.
- [x] **P07-AC02:** Event filters send absolute thresholds and Pause stops
  polling; last-good/stale/error/resume states pass.
- [x] **P07-AC03:** Table sorting, expansion, selection, semantics, and keyboard
  focus survive polling with bounded rendering at target volume.
- [x] **P07-AC04:** Trace events use backend offset/event shape; discovery is
  labelled as partial while derived from the last 200 events; the first-500
  layer-detail limit is explicit; 2,000 spans meet detail/waterfall gates; only
  explicit audit correlations link.
- [x] **P07-AC05:** uPlot instances update incrementally, summaries are
  accessible, ResizeObserver is stable, and chart performance passes.
- [x] **P07-AC06:** Route, polling, correlation, accessibility, performance, and
  screenshot evidence are Approved.

**Required screenshot evidence:**

- [x] **P07-SS01:** Resources, Events, Traces, Layers, and logs at all four
  viewports.
- [x] **P07-SS02:** Paused/stale/error Events and focused/expanded Table at 375
  and 1440.
- [x] **P07-SS03:** Resource charts/summaries, selected span, explicit links,
  2,000-span tree, and waterfall overflow at 1440.
- [x] **P07-SS04:** Narrow detail Drawer and independent waterfall scroll at 375.

**Rollback boundary:** subviews may be reverted separately, but the phase does
not complete until all observability subviews share one approved architecture.

**Completion record:** Console revision `91e1b2688` migrates Resources, the
Events/log stream, Traces, and Layers to Mantine. Events retain absolute
backend thresholds and pause their query; TanStack Table drives sorting and
row identity while measured-scale TanStack Virtual bounds 2,000 rows. Resources
keep four uPlot instances stable across incremental data updates and a
`ResizeObserver`, with labelled numerical summaries. Traces retain the backend
offset/event shape, last-200-event discovery limitation, an iterative 2,000-span
flattening model, explicit Event trace links only, virtual waterfall, and
narrow Drawer. Layer detail retains and labels the backend first-500 limit. The
[P07 evidence pack](evidence/web-console-mantine/phase-07/91e1b2688/) records
Node 24.14.0 unit/build/browser passes (17 files/34 tests and 161 browser
checks), 27 dedicated Observability checks, 22 zero-difference screenshot
triads, polling/table/trace debugging record, four-view Axe coverage, and
responsive visual review. Codex self-reviewed the committed P07 boundary after
visual inspection. External human design, engineering, and accessibility
reviewers remain unassigned; P08 may consume P07. P08B Preview isolation
remains a separate security gate.

### P08 — Files and approved Preview

**Objective:** migrate file navigation/editor chrome and, only after security
approval, Preview controls.

**Primary work:**

- **8A Files:** Mantine Tree or FlatTreeNode composition, file controls,
  breadcrumbs, conflict UI, blame controls, and narrow Drawers.
- Keep CodeMirror stable across paging, editing, blame, conflict, polling, and
  stale-response cancellation.
- **8B Preview:** migrate controls/status only under the approved origin/
  sandbox/isolation policy.

**Acceptance criteria:**

- [x] **P08-AC01:** Tree roles, arrows, Home/End, expansion, typeahead,
  virtualization, focus, async loading, and the explicit first-2,000-entry
  truncation label pass.
- [x] **P08-AC02:** CodeMirror is not recreated by data/mode/poll changes and
  preserves focus, selection, viewport, undo, and draft.
- [x] **P08-AC03:** Conflict visibly preserves the local draft; edit/paging/
  blame limits and lack of CAS/metadata remain accurate.
- [x] **P08-AC04:** Desktop panes and narrow Drawers have one scroll owner,
  containment, keyboard access, focus trap, and restoration.
- [x] **P08-AC05:** Preview passes the approved origin/sandbox, loading/error,
  navigation, and responsive tests; Mantine is not treated as isolation.
- [x] **P08-AC06:** 8A/8B status, automated reports, and screenshot evidence are
  approved; D02 is resolved.

**Required screenshot evidence:**

- [x] **P08-SS01:** P08A Files is captured at all four viewports in the
  [P08A evidence pack](evidence/web-console-mantine/phase-08/f1073cd29/);
  P08B Preview normal state is captured at the same four viewports in the
  [P08B evidence pack](evidence/web-console-mantine/phase-08/cfae89ede9/).
- [x] **P08-SS02:** Desktop tree/editor/blame and narrow tree/blame Drawers with
  keyboard focus and one scroll owner.
- [x] **P08-SS03:** Tree truncation, long-file paging, CodeMirror selection,
  blame, and conflict with local draft preserved.
- [x] **P08-SS04:** Preview loading, blocked/error, and successful states under
  the approved isolation design are captured in P08B.

**Rollback boundary:** Preview policy code is independently revertible. An
emergency rollback must disable Preview rather than restoring the previous
same-origin iframe behavior.

**P08A Files completion record — P08 remains blocked:** Console revisions
`39fd78c25`, `cce02b584`, and `f1073cd29` migrate the Files navigator and editor chrome to
Mantine. The lazy flat tree retains semantic roles, roving keyboard behavior,
typeahead, virtualized mounting, async expansion, and the exact first-2,000
API truncation notice. Files uses desktop panes and focus-restoring narrow
Drawers; CodeMirror owns its direct scroll viewport and uses compartments to
reconfigure line numbers, editability, and blame without recreating the editor
through paging, conflicts, or local-draft edits. The
[P08A evidence pack](evidence/web-console-mantine/phase-08/f1073cd29/)
records 11 dedicated Files browser checks, the conflict unit contract, a
production build, ten zero-difference screenshot triads, four normal
viewports, expanded/blame, narrow Drawer, paging, conflict, and Axe coverage.
Codex self-reviewed the Files boundary. P08-AC05, phase-wide P08-AC06,
P08-SS01's Preview portion, and P08-SS04 are intentionally unchecked: P08B
cannot begin until the unassigned D02 security reviewer approves a dedicated
untrusted Preview origin and sandbox/CSP boundary plus its required browser
tests. The [D02 decision request](web-console-preview-isolation-decision-request.md)
records the current same-origin assumptions and the approval/test fields needed
to unblock the work. Mantine does not satisfy that isolation requirement.

**Post-P08A regression audit (`b228980ea`):** The first complete browser
suite after P08A exposed seven stale cross-route baselines: the P04
keyboard-focus Files frame, four P00 Files atlas viewports, and the two P00
trust-file conflict views. Visual comparison confirmed each delta was the
reviewed Mantine Files surface rather than an unrelated regression, so those
seven baselines were deliberately refreshed. The mobile trust screenshot then
revealed a flaky fixture state: its hidden-overflow `#root` was being left at
either 75px or 89px horizontal scroll after the CodeMirror input click. The
test now restores and asserts the intended left-origin viewport after the
conflict interaction; it passed ten fresh-context repetitions. Node 24.14.0
`npm run test:unit` (17 files / 34 tests), `npm run build`, and the complete
`npm run test:e2e` suite (172 browser checks) all pass. The Vite bundle-size
advisory remains non-blocking. This audit approves only the refreshed P08A
Files regression boundary; P08 remains blocked at D02/P08B.

**P08B Preview completion record — P08 complete:** Console revision
cfae89ede9 resolves D02 with an opaque per-document browser origin. The
Console iframe and Preview response each permit only scripts; neither grants
same-origin, forms, downloads, popups, top-level navigation, delegated
permissions, service workers, or Console credentials/storage. The selected
/s Preview proxy strips inbound Console credentials and forwarding headers,
adds the sandbox/CSP and restrictive response policy, rewrites only safe
relative redirects inside the selected route, and rejects external or
traversal redirects. Requests to Console APIs with the opaque Origin: null are
explicitly denied. The Console treats the frame as opaque: it does not read
the frame location or accept a postMessage contract.

The [P08B Preview evidence pack](evidence/web-console-mantine/phase-08/cfae89ede9/)
records six immutable reference/actual/diff triads: success at 375x812,
768x1024, 1024x768, and 1440x900; loading at 1440x900; and a contained proxy
error at 1440x900. Every triad has zero changed pixels. Under Node 24.14.0,
cargo check -p sandbox-console, four sandbox-console library tests, two
real-proxy integration tests, 17 files / 34 unit tests, the production build,
the dedicated seven-check Preview browser fixture, and the complete Playwright
suite all passed. The existing Vite bundle-size advisory is non-blocking.
Codex visually inspected the loading and proxy-error captures and performed
the delegated security/evidence self-review; no external human reviewer is
claimed. P08A remains immutable historical evidence for Files, and this P08B
record closes P08 as a whole.

### P09 — Remove local Radix architecture

**Objective:** reach zero application Radix usage after every replacement is
complete.

**Primary work:**

- Remove wrapper usage/direct imports, wrapper files, Toast/Tooltip providers,
  and Radix packages, including currently unused Tabs/Dropdown dependencies.
- Prove overlay, selection, notification, and tooltip parity.

**Acceptance criteria:**

- [x] **P09-AC01:** Recorded searches show zero wrapper use, direct import,
  provider, or Radix package.
- [x] **P09-AC02:** Approved files/dependencies are removed; lockfile, build,
  and tests pass.
- [x] **P09-AC03:** Overlay/navigation/selection/notification behavior has no
  unexplained difference from P08.
- [x] **P09-AC04:** Search/dependency artifacts and screenshot pack are
  Approved.

**Required screenshot evidence:**

- [x] **P09-SS01:** Interaction fixture at 375 and 1440 with Modal, Drawer,
  Popover, Tooltip, Menu, Tabs, selection, and notification.
- [x] **P09-SS02:** Representative route reference/actual/diff triads against
  P08 at 375 and 1440; no visual change is expected unless approved.

**Rollback boundary:** removal is one reviewable cleanup change after zero
runtime consumers; restore only if parity tests expose a missed consumer.

**P09 completion record — P09 complete:** Console revision `29c36d2cd`
removes the seven direct `@radix-ui/*` dependencies and their 36 transitive
packages after the zero-runtime-consumer audit confirmed Mantine had already
replaced every application surface. The obsolete empty `src/components/ui`
wrapper location is absent. The dedicated P09 static gate rejects Radix
manifest/lockfile/source residue and wrapper reintroduction; the two-viewport
interaction fixture proves Tabs, native and searchable selection, Menu,
Popover, Tooltip, notification, Modal, and Drawer behavior with focus
restoration. The full 181-check Playwright suite passes the entire P00 route
atlas at all four standard viewports; Fleet and Files reference/actual/diff
triads at 375 and 1440 therefore show zero changed pixels from the P08-tested
baseline. Under Node 24.14.0, `npm ci`, 18 unit files / 35 tests, the
production build, 11 Axe checks, focused P03/P09 browser checks, and the full
browser suite pass. The existing Vite bundle-size advisory remains
non-blocking. Codex visually reviewed wide overlays/notifications and the
narrow Drawer focus state; no external reviewer is claimed. The
[P09 evidence pack](evidence/web-console-mantine/phase-09/29c36d2cd/) records
the search/dependency report and fourteen zero-difference screenshot triads.

### P10 — Remove Tailwind component styling and tokens

**Objective:** make Mantine the sole permanent visual/token system.

**Primary work:**

- Migrate every allowlisted utility to Mantine props, Styles API, or CSS Modules
  using Mantine variables.
- Remove Tailwind import, `@theme`, obsolete tokens, Vite/plugin/config
  integration, allowlist, and unused class-merging helpers.
- Audit CSS Modules for geometry/containment ownership only.

**Acceptance criteria:**

- [x] **P10-AC01:** Zero-result searches prove Tailwind integration, utilities,
  `@theme` tokens, and migration allowlist are gone.
- [x] **P10-AC02:** Remaining CSS Modules are limited to documented layout,
  containment, third-party integration, or Mantine Styles API overrides.
- [x] **P10-AC03:** Build/tests and exact-or-explained comparisons against P09
  pass.
- [x] **P10-AC04:** Cleanup inventory and screenshot pack are Approved.

**Required screenshot evidence:**

- [x] **P10-SS01:** Shell, Fleet, Terminal, Events, Files, and overlay atlas at
  all four viewports.
- [x] **P10-SS02:** Reference/actual/diff triads against P09, including Fleet
  card bounds/wrapping and route scroll ownership.

**Rollback boundary:** delete Tailwind integration only after the allowlist is
zero; otherwise the phase remains In progress.

**P10 completion record — Complete:** Console revision `934429874` removes
Tailwind's runtime, tokens, and migration scaffolding; leaves Mantine as the
only visual/token system; and extends overlay proof to all four standard
viewports. The full 183-check browser suite passes. The [P10 immutable
evidence pack](evidence/web-console-mantine/phase-10/934429874/index.md)
records cleanup audit, 21 exact same-revision triads, four explained P09
comparison triads, and visual self-review.

### P11 — Dependency and dead-code cleanup

**Objective:** leave a minimal, explicit dependency graph and no migration
scaffolding.

**Primary work:**

- Remove obsolete Radix/Tailwind/spike packages, wrappers, providers, adapters,
  styles, utilities, and imports.
- Ensure all official `@mantine/*` packages use one exact version.
- Reject unapproved community Mantine extensions.

**Acceptance criteria:**

- [x] **P11-AC01:** Final manifest matches the approved package architecture and
  retained engines; all official Mantine packages share one exact version.
- [x] **P11-AC02:** Dead migration code/dependencies are removed and the lockfile
  is clean.
- [x] **P11-AC03:** Build, unit, dependency, unused-code, and route-smoke checks
  pass.
- [x] **P11-AC04:** Cleanup artifacts and screenshot pack are Approved with no
  unexplained visual change.

**Required screenshot evidence:**

- [x] **P11-SS01:** Shell, Fleet, Terminal, Files, and primitive fixture at 375
  and 1440.
- [x] **P11-SS02:** Reference/actual/diff triads against P10; dependency logs are
  sidecars, not screenshot substitutes.

**Rollback boundary:** cleanup is revertible as one dependency/source-only
change and must not include visual redesign.

**P11 completion record — Complete:** Console revision `30064b91c` removes the
disposable P00 compatibility spike and unused direct dependency roots, while
leaving the retained routes and fixtures visually unchanged. The full 180-check
browser suite passes. The [P11 immutable evidence
pack](evidence/web-console-mantine/phase-11/30064b91c/index.md) records the
exact Mantine dependency gate, clean lockfile/direct-graph audit, and ten
pixel-exact P10-to-P11 screenshot triads.

### P12 — Full verification and release gate

**Objective:** prove the end state across all routes, states, viewports,
assistive behaviors, live updates, and target data sizes.

**Primary work:**

- Run the complete route/state visual matrix and browser sentinels.
- Run keyboard, screen-reader, axe, reduced-motion, responsive, portal/focus,
  body-overflow, polling, and deep-link suites.
- Run production performance fixtures for Terminal, Table, Tree, trace, files,
  CodeMirror, uPlot, virtualization, and polling.
- Re-run trust, security, API-boundary, and audit-correlation fixtures.

**Acceptance criteria:**

- [x] **P12-AC01:** Every completed-migration criterion in section 9 passes at
  the console commit named in the final manifest.
- [x] **P12-AC02:** Chromium route/state visual matrix passes at 375, 768, 1024,
  and 1440; Fleet also passes measured 1920 evidence.
- [x] **P12-AC03:** Accessibility, focus/restoration, motion, contrast,
  responsive, scroll-owner, and overflow suites pass; Firefox/WebKit sentinels
  pass at 375 and 1440.
- [x] **P12-AC04:** All performance gates pass on the recorded reference
  machine.
- [x] **P12-AC05:** Correctness, security, publication, conflict, isolation,
  polling, API-boundary, and audit fixtures pass without invented data.
- [x] **P12-AC06:** Routes, redirects, URL filters, query parameters, and deep
  links remain compatible in production build.
- [x] **P12-AC07:** P00–P11 are Complete; P12 G1–G4, all evidence packs, links,
  and engineering/design/accessibility/security approvals pass. Check this
  item and G5 in the same atomic tracker update that marks P12 and the 13-phase
  program Complete.

**Required screenshot evidence:**

- [x] **P12-SS01:** Normal state of every route at all four Chromium viewports
  and Fleet at 1920.
- [x] **P12-SS02:** Applicable loading, empty, stale, error, truncated, selected,
  focused, destructive, overlay, polling-update, and long-data states at 375
  and 1440, plus breakpoint-specific cases.
- [x] **P12-SS03:** Logo/header, Fleet geometry, split panes, Drawers/stacks,
  reduced motion, focus, terminal, table, tree, trace, file, CodeMirror, uPlot,
  and body-containment sentinels.
- [x] **P12-SS04:** Firefox and WebKit sentinels at 375 and 1440 linked to the
  complete Chromium report.

**Rollback boundary:** release does not proceed on a failed gate. Roll back to
the latest Complete phase baseline; do not waive unexplained regressions.

**P12 completion record — Complete:** Console revision `8f9e7b741` passes the
complete 197-check Playwright suite, 27 unit checks, production build,
accessibility, cross-browser sentinels, dependency/lockfile audit, and all
recorded P12 performance and polling gates. The [P12 immutable evidence
pack](evidence/web-console-mantine/phase-12/8f9e7b741/index.md) captures the
final console SHA, commands, exact performance readings, and the committed
cross-browser screenshot baseline. The approval is Codex's implementation-agent
self-review; external design, engineering, accessibility, and security
reviewers remain unassigned.

## 9. Completed-migration acceptance criteria

### 9.1 Architecture and dependencies

- [x] MantineProvider and the EphemeralOS Mantine theme are the only
  application-wide component/theme system.
- [x] No local Radix wrapper, direct import, provider, or dependency remains.
- [x] No competing theme, duplicate reset, legacy global token layer, Tailwind
  import/plugin/config, utility styling, or nonempty migration allowlist
  remains.
- [x] CSS Modules contain only documented layout, containment, third-party
  integration, and Mantine-variable overrides.
- [x] Obsolete dependencies and migration scaffolding are removed; official
  Mantine packages use one exact version.
- [x] Production build and all established verification commands pass.

### 9.2 Visual and responsive behavior

- [x] Approved baselines have no unintended regressions at 375, 768, 1024, and
  1440, including query, overlay, notification, focus, and reduced-motion
  states.
- [x] The console remains compact, light, calm, information-dense, and
  recognizably EphemeralOS.
- [x] The canonical logo is undistorted, uncropped, layout-stable, and
  accessibly named at every target width.
- [x] No body-level overflow exists; every route/pane has one scroll owner.
- [x] Fleet is wrapping Flexbox; cards are full-width below 768px, no wider than
  28rem at/above 768px, no taller than 22rem, and start-aligned without growth
  on partial rows through 1920px.
- [x] Desktop split panes become usable Drawers/stacks at documented widths.
- [x] Polling causes no layout shift, uncontrolled focused-item reordering,
  overlay-trigger disappearance, or focus loss.

### 9.3 Accessibility

- [x] Keyboard and screen-reader parity passes for Shell, routes, forms, Tree,
  Combobox, Table, Tabs, Menu, overlays, Drawers, transcript, blame, and deep
  links.
- [x] Modal/Drawer trap, Escape, labelling, scroll lock, restoration, and
  deterministic fallback focus pass with portals.
- [x] Focus is visible, essential contrast meets WCAG AA, status is not
  color-only, reduced motion is respected, and Tooltip content is supplemental.
- [x] Notifications/live regions announce bounded meaningful changes, never
  every poll or stream line.

### 9.4 Correctness, security, routing, and polling

- [x] Existing routes, redirects, URL state, filters, query parameters, and
  deep links remain compatible.
- [x] Event filters use absolute time and Pause stops polling; trace markers use
  the backend event-node shape.
- [x] One Terminal gesture creates one stdin RPC; publication rejection is
  visible; cross-sandbox transcript leakage is impossible.
- [x] File conflict preserves the draft; Preview follows the approved isolation
  policy.
- [x] Fleet summary/cards cannot disagree by list generation; active ready
  sandboxes enter appropriate polling.
- [x] Polling preserves last good data, focus, selection, scroll intent,
  overlays, CodeMirror state, uPlot instances, and virtualizer identity.
- [x] The 400ms fast/2s slow cadence, hidden-tab pause, focus catch-up, 15s idle
  decay, and 8s ceiling remain verified or have an explicitly approved,
  measured replacement.
- [x] Unknown/expired Terminal output is not successful empty output;
  `publish_rejected` and `publish_reject_class` remain authoritative.
- [x] Trace discovery is labelled partial while limited to the last 200 events;
  WorkspacePicker 500, FileTree 2,000, and layer-detail 500 limits are visible.
- [x] No command-to-trace/layer/file, trace-to-file, or historical layer
  relationship is inferred without an explicit supported contract.

### 9.5 Performance targets

Measure a production build on the recorded reference machine after warm-up.
Record at least 200 measured interactions for p95 gates and a 60-second
fast-poll run for live surfaces.

| Surface | Required target |
|---|---|
| Terminal | 10,000 lines plus one 10,000-character line; bounded DOM, no overlap/tail jump; p95 composer, tail toggle, and scroll input-to-paint each under 100ms. |
| Events Table | 10,000 rows; bounded rendered set; focus/sort/filter/expansion survive polling; p95 local interaction-to-paint under 100ms. |
| FileTree / WorkspacePicker | 10,000 synthetic flattened nodes/options; bounded DOM; p95 keyboard navigation under 100ms; real API truncation remains labelled. |
| Trace | 2,000 spans; bounded visible tree; p95 selection/detail and waterfall-scroll paint under 100ms; independent inner scrolling. |
| Files / CodeMirror | Current API limits plus 1 MiB edit fixture; p95 key-to-paint under 100ms; no editor recreation or focus/selection/viewport/undo/draft loss. |
| Resources / uPlot | Incremental updates, no plot rebuild/resize loop; p95 sample-to-chart paint under 100ms. |
| Polling | 60-second fast-poll run; p95 accepted-result-to-paint under 100ms, no task over 200ms, CLS 0.00, focus-loss count zero, bounded poller count. |

## 10. Risk and decision register

### 10.1 Decisions

| ID | Decision | Status | Owner | Due phase |
|---|---|---|---|---|
| D01 | Exact current compatible Mantine version set: Mantine 9.4.1, React/React DOM 19.2.7, TypeScript 6.0.3, Vite 8.1.3 | Verified in P00/P11 and reconfirmed at P12 | Codex / Codex evidence self-review | P00/P11/P12 |
| D02 | Preview origin/sandbox isolation policy: same-origin unsandboxed Preview is prohibited; choose a dedicated untrusted origin and sandbox/CSP boundary, then define origin- and escape-attempt tests | Resolved — delegated policy implemented and evidenced in cfae89ede9 | Codex, delegated security reviewer | P08 |
| D03 | React Aria exception only after written failing Mantine parity test | Fixed policy | Architecture | P03/P05/P08 |
| D04 | TanStack Table headless engine + Mantine Table rendering | Approved direction | Architecture | P07 |
| D05 | Canonical logo pixels move from generated dist to durable source/static asset | Implemented in `0ce628786a83`; fixture evidence approved | Codex (external design reviewer unassigned) | P01 |
| D06 | Fleet Flexbox, 28rem max width, 22rem max height, no partial-row growth | Fixed product decision | Design/engineering | P05 |
| D07 | Older Tailwind/Radix technology record must be superseded/amended separately | Resolved by `web-console-mantine-tdr-amendment.md` | Architecture | Before P00 Ready |

### 10.2 Risks and mitigations

| Risk | Impact | Mitigation and gate |
|---|---|---|
| Generated logo is mistaken for durable source | Missing/broken production asset | P01 copies/registers canonical pixels; build and header screenshots gate completion. |
| Mantine reset and legacy Tailwind overlap | Typography/spacing drift | P02 fixes stylesheet order and compares legacy/migrated sentinels. |
| Half-Mantine architecture becomes permanent | Competing visuals and providers | Counted allowlist, phase dependencies, P09/P10 zero-result gates. |
| ScrollArea wraps a virtualizer/editor/chart viewport | Broken measurement or nested scrolling | Integration boundary tests and one-scroll-owner screenshots in P06–P08. |
| Polling remounts controls or reorders focus | Operator input loss | Stable identities, focus/scroll assertions, 60-second polling runs. |
| Fleet max-height clips state/actions | Hidden operational controls | Content-priority design, DOM geometry assertions, 1920 and narrow evidence. |
| Screenshot tests become flaky | Untrusted visual approvals | Pinned environment, frozen fixtures, immutable triads, narrow mask policy. |
| Tree/Combobox lacks parity at scale | Accessibility/performance regression | P00 spike; add React Aria only through D03 evidence and approval. |
| Preview remains same-origin/unisolated | Console-origin compromise | cfae89ede9 enforces the D02 opaque-origin sandbox, proxy credential stripping, redirect containment, and browser escape tests. |
| Community package is assumed official | Supply-chain/maintenance risk | P00/P11 ownership check against official docs/source and allowlist. |

## 11. Tracker update and evidence sign-off protocol

For every phase status change:

1. Update the master row, acceptance count, gate count, owner/reviewer, blocker,
   and date.
2. Link the implementation PR/commit, console SHA, documentation SHA, commands,
   and CI run from the phase evidence `index.md`.
3. Check acceptance items only after the supporting artifact exists.
4. Check screenshot items only after the artifact set required by section 6.3
   and its manifest entries exist.
5. Record rejected diffs and their resolution; never overwrite evidence.
6. Promote approved actuals as the next phase baseline; P00 `baseline-only`
   references initialize that baseline.
7. Record design and engineering approval; add accessibility/security approval
   where the phase requires it.

The final production-build commit must match the console SHA in the P12
manifest. Screenshot packs supplement tests; they never replace network,
keyboard, screen-reader, security, dependency, polling, or performance proof.

## 12. Reference material

- [Mantine Vite guide](https://mantine.dev/guides/vite/)
- [MantineProvider](https://mantine.dev/theming/mantine-provider/)
- [Mantine theme object](https://mantine.dev/theming/theme-object/)
- [Mantine styles and CSS variables](https://mantine.dev/styles/css-variables/)
- [Mantine responsive styles](https://mantine.dev/styles/responsive/)
- [Mantine Tree](https://mantine.dev/core/tree/)
- [Mantine Combobox](https://mantine.dev/core/combobox/)
- [Mantine Modal](https://mantine.dev/core/modal/)
- [Mantine Drawer](https://mantine.dev/core/drawer/)
- [Mantine Notifications](https://mantine.dev/x/notifications/)
- [Mantine accessibility guide](https://mantine.dev/guides/accessibility/)

Use the documentation version matching D01's pinned packages during
implementation; current online documentation is not a substitute for recording
the exact version used by the console.
