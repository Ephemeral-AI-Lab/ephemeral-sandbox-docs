Implement the EphemeralOS E2E Control Room UI migration in
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/web`.

VISUAL AUTHORITY

Inspect `/Users/yifanxu/Ephemeral-AI-Lab/tmp/e2e-ui-prototype-reference-54ed152e3/`
(`index.html`, `styles.css`, JPGs), `docs/e2e/DESIGN.md`, and the layout/theme
and migration specs under `ephemeral-sandbox-docs/implementation-plan/e2e_test/`.
Match its shell, hierarchy, density, components, and responsive composition—not
its HTML, hash routes, hard-coded content, or fake state. Keep current routes/APIs.

VISUAL CONTRACT

- Style: a warm editorial engineering report and calm, data-dense control room;
  large headings and spacious sections frame compact operational data.
- Palette: canvas `#f5f2ed`; nav `#eee9e2`; warm surface `#fffdf9`; raised card
  `#fff`; inset `#f9f6f1`; selection `#f0f5f8`; ink `#241f1c`; secondary
  `#6c625c`; faint `#928881`; borders `#e3ddd5`/`#d4cabf`; slate `#395f76`;
  dark slate `#29495d`. Use the spec's green/amber/red/violet semantic pairs.
- Typography: Inter/system sans; monospace only for IDs, paths, hashes, timings,
  and evidence. Titles use `clamp(30px,3.2vw,45px)` with tight leading/tracking.
- Shape: 7px controls, 11px cards, 16px features, warm 1px borders, subtle
  brown-gray shadows, 120–180ms feedback, and reduced-motion support.
- Use one outlined SVG icon family. No emoji, gradients, glassmorphism,
  decorative charts, image chrome, or dark mode.

RESPONSIVE SHELL

- Above 1180px: fixed 236px sidebar, 58px context bar, max-width 1660px content,
  24–50px padding; sidebar holds brand, four route links, counts, runner summary.
- 901–1180px: 210px sidebar, two-column grids, stacked secondary panels.
- 681–900px: 59px horizontal nav, sticky context bar, 18px content padding;
  stack run tree/detail.
- 375–680px: icon-plus-name nav, one-column cards, full-width actions, full-screen
  filters/details/dialogs, safe-area sticky actions, no page-level overflow.

ROUTE COMPOSITIONS

1. Catalog `/e2e/catalog`: follow `#catalog`—eyebrow, purpose heading,
   search/action, truthful metrics, warning, domain cards. Treat `#runtime`,
   `#manager`, `#observability`, and `#test-detail` as visual states: filter rail,
   dense rows, selected detail, validations, evidence, metadata, selection bar.
   Show rail/results/detail at 1440px, detail sheet at 1024px, and full-screen
   filter/detail below. `#compound` informs Review, never routing.
2. Review: raised desktop dialog/mobile screen. Order Scope, Boundaries,
   Execution, Evidence/cleanup, Inputs, Preflight. One Start action with reason.
3. Run `/e2e/runs/:runId`: follow `#live-run`—dark-slate hero, progress/freshness,
   evidence identity, first failure, narrow tree, wide evidence/log detail. Reuse
   for live/history. Mobile: hero, failure, progress, actions, tree, detail, logs.
4. Runs `/e2e/runs`: editorial heading/filters, operational table, selected
   detail; convert rows to complete cards on narrow screens.
5. Workspaces `/e2e/workspaces`: Capacity/store safety, Template, lifecycle,
   Active, Quarantine, Recent purges. Health is a desktop drawer/mobile screen.

IMPLEMENTATION AND ACCEPTANCE

Use Mantine and focused theme/CSS overrides; add no framework or abstraction.
Render only server facts/actions. Unify empty, loading, stale, error, recovery,
evidence-gap, and destructive states. Status uses label, icon, color. Controls are
44px minimum; focus is visible; dialogs manage focus; WCAG 2.2 AA wins.

Build shell/theme, Catalog, Review, Run, Runs, then Workspaces/Health. Preserve
unrelated changes; run relevant tests/builds. Capture deterministic 390, 1024, and
1440px screenshots and compare with the reference. Verify keyboard use, 200% zoom,
long IDs, reduced motion, contrast, and overflow. Report changes, tests, images,
justified deviations, and remaining work. Do not commit/delete the prototype.
