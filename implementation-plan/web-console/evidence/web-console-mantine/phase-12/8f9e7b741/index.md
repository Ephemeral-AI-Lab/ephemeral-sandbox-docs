# P12 approved release-gate evidence

This immutable release pack is captured from Console revision `8f9e7b741`.
It completes the Mantine migration program: the final source revision matches
the production-build, full-browser, accessibility, performance, polling, and
cross-browser evidence recorded here.

## Release decision

P12 is approved on the recorded reference machine. No assertion was weakened
to obtain approval. The one visual-stability correction sets a 202px minimum
height on the centered WorkspacePicker modal, avoiding fractional-pixel text
rasterization while retaining its natural content layout; the two affected
Chromium baselines were intentionally regenerated and then each passed twenty
parallel strict-snapshot repetitions.

This is an implementation-agent self-review by Codex. It does not represent
external human design, engineering, accessibility, or security sign-off.

## Automated evidence

- `npm run test:e2e` — pass: 197 Playwright checks in 14 files. It covers the
  Chromium route/state visual matrix at 375, 768, 1024, and 1440, Fleet at
  1920, deep links, URL state, focus, motion, overflow, security/isolation,
  publication/conflict, API boundaries, polling, and audit fixtures.
- `npm run test` — pass: 14 files / 27 unit checks.
- `npm run build` — pass: TypeScript project build and Vite production bundle.
  The existing bundle-size advisory is non-blocking.
- `npm run test:a11y` — pass: 10 Axe checks, including Shell, Fleet, Terminal,
  Files, and every Observability view.
- `npx playwright test tests/browser/P12CrossBrowserSentinel.spec.ts --browser=firefox --workers=1 --reporter=line`
  — pass: 8 strict visual/overflow sentinels at 375x812 and 1440x900.
- `npx playwright test tests/browser/P12CrossBrowserSentinel.spec.ts --browser=webkit --workers=1 --reporter=line`
  — pass: 8 strict visual/overflow sentinels at 375x812 and 1440x900.
- `npx playwright test --grep 'P12 keeps' --workers=1 --reporter=line` — pass:
  8 measured 200-sample performance gates, all below 100ms p95.
- `npx playwright test tests/browser/PollingFixture.spec.ts --workers=1 --reporter=line`
  — pass: virtual 60-second fast-poll stability (100–150 accepted calls,
  maximum task at most 200ms, CLS 0.00) and 200-sample accepted-result paint
  measurement.
- `npm ci --dry-run`, `npm ls --depth=0`, and `git diff --check` — pass: lock
  plan, direct dependency graph, and patch formatting are clean.

## Performance record

Each interaction below uses 200 samples and a p95 threshold strictly below
100ms. The listed run was made after the final visual-baseline correction.

| Surface | p95 | Result |
|---|---:|---|
| WorkspacePicker 10,000-option filter | 16.9ms | Pass |
| Terminal 10,000-line scroll | 22.0ms | Pass |
| Events Table 10,000-row sort | 74.0ms | Pass |
| Trace 2,000-span waterfall scroll | 51.0ms | Pass |
| uPlot chart resize | 20.0ms | Pass |
| FileTree 10,000-node keyboard navigation | 24.1ms | Pass |
| CodeMirror 1 MiB edit | 9.0ms | Pass |
| Fast-poll accepted result to paint | 6.0ms | Pass |

The virtual 60-second polling proof additionally reports CLS 0.00, no task
over 200ms, bounded poller activity, and no focus-loss assertion failure.

## Visual artifacts

The final Console revision Git-tracks 24 P12 strict screenshot baselines in
`web/console/tests/browser/P12CrossBrowserSentinel.spec.ts-snapshots/`: Fleet,
Terminal, Events, and Files at 375x812 and 1440x900 for Chromium, Firefox, and
WebKit. The complete Chromium route/state baseline is exercised by the
197-check suite and its committed P00–P08 snapshots; it includes all required
375, 768, 1024, 1440, and Fleet 1920 captures. The P12 snapshot spec also
asserts that the document root has no horizontal overflow.

## Acceptance coverage

| Criterion | Evidence |
|---|---|
| P12-AC01, P12-AC05, P12-AC06 | Full 197-check route, trust, security, publication, conflict, isolation, API, polling, and deep-link suite; unit/build and audit gates. |
| P12-AC02, P12-SS01–SS03 | Full Chromium matrix, committed strict snapshots, visual state fixtures, focus/motion/containment assertions, and Fleet 1920 proof. |
| P12-AC03, P12-SS04 | 10 Axe checks plus strict Firefox and WebKit 375/1440 sentinels. |
| P12-AC04 | Eight 200-sample p95 performance gates and the virtual 60-second poller proof. |
| P12-AC07 | P00–P11 evidence packs are complete; this pack and the tracker update complete P12 G1–G5 atomically. |

The exact machine, command, artifact, and review metadata are recorded in
[manifest.json](manifest.json).
