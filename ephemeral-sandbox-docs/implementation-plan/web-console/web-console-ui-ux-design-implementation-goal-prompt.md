/goal Implement the complete EphemeralOS web-console UI/UX design and Mantine migration through production-ready verification; do not stop at docs, a prototype, or partial conversion.

Read `ephemeral-sandbox/web/console` and every document in `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-docs/implementation-plan/web-console/`. The proposal and migration plan are authoritative; obtain an authorized superseding/amendment record for the historical Tailwind/Radix decision before P00 is Ready. Verify version-sensitive choices with official Mantine docs.

Complete P00–P12 in order and keep the app buildable. Update each phase’s status, gates, acceptance count, ownership, blockers, commands, commits, and evidence links. Lock fixtures, acceptance IDs, screenshot cases, checks, and rollback before starting; never advance on failure.

Required end state:
- Mantine is the sole app-wide component/theme/token/form/overlay/notification/focus/responsive system, with one MantineProvider and one EphemeralOS light theme.
- Remove all Radix wrappers/imports/providers/dependencies after parity. Remove Tailwind utilities, `@theme`, build integration, allowlist, and obsolete helpers. No mixed architecture.
- Retain Router, TanStack Query/Table/Virtual, CodeMirror, uPlot, and Lucide. Render Table models with Mantine. Add React Aria only after a documented failing Mantine parity test; verify package ownership.
- Register `web/console/dist/assets/images/logo.png` pixels as a durable source/static asset; never import generated `dist` at runtime. Build the contrast-tested theme from its warm neutrals and eye-blue accent.
- Preserve compact, calm, light, high-density operator character; monospace operational data; split panes; narrow Drawers/stacks; visible focus; reduced motion; and bounded scrolling.
- Fleet uses wrapping Flexbox: full-width below 768px; at/above 768px cards are ≤28rem wide; all are ≤22rem high; partial rows stay start-aligned and never grow or clip essential content. Use CSS Grid only for genuine minmax split/waterfall geometry.
- Keep one scroll owner; never wrap Virtual, CodeMirror, or uPlot viewports in another ScrollArea.

Preserve routes, URL/deep-link state, lifecycle/API/polling contracts, and explicit audit relations. Never invent fields or inferred command/trace/layer/file links. Fix and test every P00 trust defect in the plan. Mantine does not solve Preview isolation, file CAS, missing indexes, or pagination. Block only P08B pending approved isolation. Polling must preserve last-good data, focus, selection, scroll/tail intent, overlays, CodeMirror, uPlot, and virtualizer state.

Run all build, contract, component, route, accessibility, visual, polling, performance, dependency, and security checks in the plan; never waive failures. Each phase needs an approved `web-console/evidence/web-console-mantine/phase-XX/<sha>/` pack from pinned, sanitized fixtures. Use immutable reference/actual/diff triads except for the plan's P00 baseline-only and fixture-only evidence modes. Capture normal states at 375x812, 768x1024, 1024x768, and 1440x900; exceptional/focus/overlay states at 375 and 1440; and P05/P12 Fleet at 1920x1080 with measured bounds. Include real focus, reduced motion, overflow, scroll ownership, and polling stability. Screenshots supplement tests.

Finish only when every phase/global architecture, visual, accessibility, correctness, security, performance, route, build, cleanup, screenshot, and sign-off gate passes with no unexplained diff, Radix/Tailwind residue, body overflow, focus loss, layout shift, or undocumented exception. Report changed files, exact commands/results, tracker/evidence locations, backend-only gaps, and genuine blockers; never claim completion with an open gate.
