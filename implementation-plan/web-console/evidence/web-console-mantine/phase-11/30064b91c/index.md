# P11 approved dependency and dead-code cleanup evidence

This immutable pack is captured from Console revision `30064b91c`. It closes
P11 without a visual redesign: the disposable P00 compatibility spike and its
now-unused dependency roots are removed, leaving an explicit production and
test dependency graph.

## What changed

- Removed the P00-only Mantine compatibility component, CSS, entry page,
  browser fixture, unit smoke/render probes, and its three screenshots.
- Removed `@mantine/form`, which was used only by that disposable fixture.
- Removed unused direct PostCSS roots and direct `axe-core`; Vite and
  `@axe-core/playwright` retain their required transitive dependencies.
- Added a P11 static gate that fixes the approved direct Mantine set at
  `@mantine/core`, `@mantine/hooks`, and `@mantine/notifications`, each exactly
  `9.4.1`, and rejects the deleted fixture roots.
- Changed Playwright's fixture-server health URL from the deleted spike root to
  the retained `atlas.html`; this prevents a 404 health probe from attempting a
  second server on port 4173.

## What passed

- P11 static gate: 1 file / 2 tests passed.
- `npm run test`: 14 files / 27 tests passed.
- `npm run build`: TypeScript and Vite production build passed. The existing
  bundle-size advisory is non-blocking.
- `npm ci --dry-run`, `npm ls --depth=0`, manifest/lockfile audit, and
  `git diff --check` passed. The direct graph contains only the three approved
  Mantine packages, all pinned to `9.4.1`.
- `npm run test:e2e`: all 180 Playwright checks passed. This is the 183-check
  P10 suite less the three intentionally deleted disposable-spike checks.

## Immutable screenshot triads

The P11 diff is dependency and fixture cleanup only. All ten P10 reference to
P11 actual triads below have zero changed pixels under ImageMagick
`compare -metric AE`; the committed browser snapshot files are unchanged
between P10 `934429874` and P11 `30064b91c`. The 30 PNG artifacts are
Git-tracked in this pack (1.4 MB).

| Requirement | Capture | Reference / actual / diff |
|---|---|---|
| P11-SS01, P11-SS02 | Shell at 375x812 | [reference](reference/p02-shell-375x812-darwin.png) / [actual](actual/p02-shell-375x812-darwin.png) / [diff](diff/p02-shell-375x812-darwin.png) |
| P11-SS01, P11-SS02 | Shell at 1440x900 | [reference](reference/p02-shell-1440x900-darwin.png) / [actual](actual/p02-shell-1440x900-darwin.png) / [diff](diff/p02-shell-1440x900-darwin.png) |
| P11-SS01, P11-SS02 | Fleet at 375x812 | [reference](reference/p00-atlas-fleet-375x812-darwin.png) / [actual](actual/p00-atlas-fleet-375x812-darwin.png) / [diff](diff/p00-atlas-fleet-375x812-darwin.png) |
| P11-SS01, P11-SS02 | Fleet at 1440x900 | [reference](reference/p00-atlas-fleet-1440x900-darwin.png) / [actual](actual/p00-atlas-fleet-1440x900-darwin.png) / [diff](diff/p00-atlas-fleet-1440x900-darwin.png) |
| P11-SS01, P11-SS02 | Terminal at 375x812 | [reference](reference/p00-atlas-terminal-375x812-darwin.png) / [actual](actual/p00-atlas-terminal-375x812-darwin.png) / [diff](diff/p00-atlas-terminal-375x812-darwin.png) |
| P11-SS01, P11-SS02 | Terminal at 1440x900 | [reference](reference/p00-atlas-terminal-1440x900-darwin.png) / [actual](actual/p00-atlas-terminal-1440x900-darwin.png) / [diff](diff/p00-atlas-terminal-1440x900-darwin.png) |
| P11-SS01, P11-SS02 | Files at 375x812 | [reference](reference/p00-atlas-files-375x812-darwin.png) / [actual](actual/p00-atlas-files-375x812-darwin.png) / [diff](diff/p00-atlas-files-375x812-darwin.png) |
| P11-SS01, P11-SS02 | Files at 1440x900 | [reference](reference/p00-atlas-files-1440x900-darwin.png) / [actual](actual/p00-atlas-files-1440x900-darwin.png) / [diff](diff/p00-atlas-files-1440x900-darwin.png) |
| P11-SS01, P11-SS02 | Primitive fixture at 375x812 | [reference](reference/p03-primitives-375x812-darwin.png) / [actual](actual/p03-primitives-375x812-darwin.png) / [diff](diff/p03-primitives-375x812-darwin.png) |
| P11-SS01, P11-SS02 | Primitive fixture at 1440x900 | [reference](reference/p03-primitives-1440x900-darwin.png) / [actual](actual/p03-primitives-1440x900-darwin.png) / [diff](diff/p03-primitives-1440x900-darwin.png) |

## Review decision

At 2026-07-11T21:00:00+08:00, Codex completed the delegated cleanup,
dependency audit, evidence, and visual self-review. The precise dependency
gate, clean lockfile verification, full route/browser suite, and exact P10 to
P11 visual triads support approval of P11. This is an implementation-agent
self-review, not a claim of external human design, engineering, or
accessibility approval.
