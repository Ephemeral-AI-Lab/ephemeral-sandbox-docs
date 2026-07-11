# P10 approved Mantine-only styling evidence

This immutable pack is captured from Console revision `934429874`. It closes
P10: Mantine is now the sole permanent visual and token system; Tailwind's
runtime integration, theme tokens, utility allowlist, and class-merging helper
are gone.

## What changed

- Removed Tailwind and its Vite plugin, package graph, `@import`, `@theme`,
  `@source` directives, migration allowlist, and `cn.ts` helper.
- Replaced every allowlisted utility use with Mantine components, props, and
  theme variables. The small global reset in `src/index.css` deliberately
  restores browser-normalized geometry formerly supplied by Tailwind
  preflight; it contains no Tailwind token or utility semantics.
- Reworked the P02 and trust fixtures to use Mantine, and added a static P10
  gate that rejects retired styling integration and residue.
- Extended the P09 overlay fixture from the narrow/wide extremes to all four
  standard viewports, so the final styling evidence exercises the same
  interaction atlas at 375, 768, 1024, and 1440.

## What passed

- Tailwind-residue scan, P10 static gate, deleted-file assertions, and
  `git diff --check` passed. `src` has one stylesheet (`index.css`) and no CSS
  Modules; the remaining global rules are base-document normalization only.
- `npm run test`: 18 files / 35 tests passed.
- `npm run build`: TypeScript and Vite production build passed. The existing
  bundle-size advisory is non-blocking.
- `npm run test:e2e`: all 183 Playwright checks passed, including visual,
  route-atlas, P09 overlay, keyboard-scroll, and Axe coverage.
- The P08 preview fixture was repeated three times with seven workers (21
  checks) after its logo-readiness synchronization; no flaky 375px capture
  recurred.

## Immutable screenshot triads

The `p10-baseline` group contains 21 same-revision render comparisons (63
images); ImageMagick `compare -metric AE` reports zero changed pixels for all
of them. The `p09-comparison` group contains four deliberately nonzero P09 to
P10 comparisons (12 images). They are retained to make the styling transition
auditable, not waived: P10 removes Tailwind's font, colour-token, and cascade
output, while Mantine variables and the reset preserve the tested route
structure, content, card bounds, wrapping, and scroll ownership. Codex
visually reviewed the narrow Fleet card and wide Files split-pane captures.

| Requirement | Capture | Reference / actual / diff |
|---|---|---|
| P10-SS01 | Shell and Fleet at 375x812 | [reference](p10-baseline/reference/p00-atlas-fleet-375x812-darwin.png) / [actual](p10-baseline/actual/p00-atlas-fleet-375x812-darwin.png) / [diff](p10-baseline/diff/p00-atlas-fleet-375x812-darwin.png) |
| P10-SS01 | Shell and Fleet at 768x1024 | [reference](p10-baseline/reference/p00-atlas-fleet-768x1024-darwin.png) / [actual](p10-baseline/actual/p00-atlas-fleet-768x1024-darwin.png) / [diff](p10-baseline/diff/p00-atlas-fleet-768x1024-darwin.png) |
| P10-SS01 | Shell and Fleet at 1024x768 | [reference](p10-baseline/reference/p00-atlas-fleet-1024x768-darwin.png) / [actual](p10-baseline/actual/p00-atlas-fleet-1024x768-darwin.png) / [diff](p10-baseline/diff/p00-atlas-fleet-1024x768-darwin.png) |
| P10-SS01 | Shell and Fleet at 1440x900 | [reference](p10-baseline/reference/p00-atlas-fleet-1440x900-darwin.png) / [actual](p10-baseline/actual/p00-atlas-fleet-1440x900-darwin.png) / [diff](p10-baseline/diff/p00-atlas-fleet-1440x900-darwin.png) |
| P10-SS01 | Terminal at all four standard viewports | [375 triad](p10-baseline/diff/p00-atlas-terminal-375x812-darwin.png), [768 triad](p10-baseline/diff/p00-atlas-terminal-768x1024-darwin.png), [1024 triad](p10-baseline/diff/p00-atlas-terminal-1024x768-darwin.png), [1440 triad](p10-baseline/diff/p00-atlas-terminal-1440x900-darwin.png) |
| P10-SS01 | Events at all four standard viewports | [375 triad](p10-baseline/diff/p00-atlas-events-375x812-darwin.png), [768 triad](p10-baseline/diff/p00-atlas-events-768x1024-darwin.png), [1024 triad](p10-baseline/diff/p00-atlas-events-1024x768-darwin.png), [1440 triad](p10-baseline/diff/p00-atlas-events-1440x900-darwin.png) |
| P10-SS01 | Files at all four standard viewports | [375 triad](p10-baseline/diff/p00-atlas-files-375x812-darwin.png), [768 triad](p10-baseline/diff/p00-atlas-files-768x1024-darwin.png), [1024 triad](p10-baseline/diff/p00-atlas-files-1024x768-darwin.png), [1440 triad](p10-baseline/diff/p00-atlas-files-1440x900-darwin.png) |
| P10-SS01 | Popover and Tooltip overlay atlas at all four standard viewports | [375 triad](p10-baseline/diff/p09-overlays-375x812-darwin.png), [768 triad](p10-baseline/diff/p09-overlays-768x1024-darwin.png), [1024 triad](p10-baseline/diff/p09-overlays-1024x768-darwin.png), [1440 triad](p10-baseline/diff/p09-overlays-1440x900-darwin.png) |
| P10-SS02 | Keyboard tab navigation and route-scroll owner at 1024x768 | [reference](p10-baseline/reference/p04-shell-keyboard-scroll-1024x768-darwin.png) / [actual](p10-baseline/actual/p04-shell-keyboard-scroll-1024x768-darwin.png) / [diff](p10-baseline/diff/p04-shell-keyboard-scroll-1024x768-darwin.png) |
| P10-SS02 | P09 Fleet card bounds/wrapping at 375x812 | [reference](p09-comparison/reference/p00-atlas-fleet-375x812-darwin.png) / [actual](p09-comparison/actual/p00-atlas-fleet-375x812-darwin.png) / [diff](p09-comparison/diff/p00-atlas-fleet-375x812-darwin.png) — 143,131 changed pixels (expected styling transition) |
| P10-SS02 | P09 Fleet card bounds/wrapping at 1440x900 | [reference](p09-comparison/reference/p00-atlas-fleet-1440x900-darwin.png) / [actual](p09-comparison/actual/p00-atlas-fleet-1440x900-darwin.png) / [diff](p09-comparison/diff/p00-atlas-fleet-1440x900-darwin.png) — 1,010,640 changed pixels (expected styling transition) |
| P10-SS02 | P09 Files route at 375x812 | [reference](p09-comparison/reference/p00-atlas-files-375x812-darwin.png) / [actual](p09-comparison/actual/p00-atlas-files-375x812-darwin.png) / [diff](p09-comparison/diff/p00-atlas-files-375x812-darwin.png) — 21,605 changed pixels (expected styling transition) |
| P10-SS02 | P09 Files route at 1440x900 | [reference](p09-comparison/reference/p00-atlas-files-1440x900-darwin.png) / [actual](p09-comparison/actual/p00-atlas-files-1440x900-darwin.png) / [diff](p09-comparison/diff/p00-atlas-files-1440x900-darwin.png) — 70,929 changed pixels (expected styling transition) |

The Terminal, Events, Files, and overlay rows link their zero-diff artifacts;
their matching reference and actual files use the identical filename in the
adjacent `reference` and `actual` directories. The complete pack contains 75
Git-tracked PNG artifacts (3.6 MB).

## Review decision

At 2026-07-11T20:56:00+08:00, Codex completed the delegated implementation,
evidence, and visual self-review. The source/manifest audit, full browser
suite, exact same-revision triads, explained P09 transition triads, and manual
layout review support approval of P10. This is an implementation-agent
self-review, not a claim of external human design, engineering, or
accessibility approval.
