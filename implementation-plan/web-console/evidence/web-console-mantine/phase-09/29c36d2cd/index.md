# P09 approved Radix-removal evidence

This immutable pack is captured from Console revision `29c36d2cd`. It closes
P09 without application visual-code changes: Mantine already owned the
remaining component, overlay, selection, and notification surfaces, leaving
the direct Radix manifest and lockfile graph as unused architecture.

## What changed

- Removed the seven direct `@radix-ui/*` dependencies and 36 transitive
  packages.
- Removed the obsolete empty `src/components/ui` wrapper location.
- Added a static regression gate for manifest, lockfile, source-import,
  provider-token, and wrapper-location residue.
- Added a two-viewport Mantine interaction fixture covering Tabs, native and
  searchable selection, Menu, Popover, Tooltip, notifications, Modal, Drawer,
  focus trap, Escape close, and trigger focus restoration.

## What passed

- `npm ci`: 196 packages installed, audit reports zero vulnerabilities.
- P09/P03 static tests: 2 files / 4 tests passed.
- `npm run test`: 18 files / 35 tests passed.
- `npm run build`: TypeScript and Vite production build passed; the pre-existing
  bundle-size advisory is non-blocking.
- `npm run test:a11y`: 11 Axe checks passed.
- Focused P03/P09 Playwright fixtures: 11 checks passed without updating a
  snapshot.
- `npm run test:e2e`: all 181 Playwright checks passed, including the P00 route
  atlas at all four standard viewports and the P09 fixture.
- Source, manifest, lockfile, installed-package, and wrapper-directory
  searches returned zero Radix residue; `git diff --check` passed.

## Immutable screenshot triads

Each reference/actual/diff row is committed. ImageMagick `compare -metric AE`
reported zero changed pixels for all 14 pairs. The P09 interaction references
are the committed P09 Playwright baselines reverified by the focused fixture;
the route references are the P00 atlas baselines that passed unchanged through
the P08 suite and again through P09's complete suite. Actual captures are the
same-commit verified renderings. Codex visually reviewed the wide
overlay/notification capture and narrow Drawer capture.

| Requirement | Capture | Reference / actual / diff |
|---|---|---|
| P09-SS01 | Selection and Tabs at 375x812 | [reference](reference/p09-selection-375x812-darwin.png) / [actual](actual/p09-selection-375x812-darwin.png) / [diff](diff/p09-selection-375x812-darwin.png) |
| P09-SS01 | Selection and Tabs at 1440x900 | [reference](reference/p09-selection-1440x900-darwin.png) / [actual](actual/p09-selection-1440x900-darwin.png) / [diff](diff/p09-selection-1440x900-darwin.png) |
| P09-SS01 | Menu and notification at 375x812 | [reference](reference/p09-menu-375x812-darwin.png) / [actual](actual/p09-menu-375x812-darwin.png) / [diff](diff/p09-menu-375x812-darwin.png) |
| P09-SS01 | Menu and notification at 1440x900 | [reference](reference/p09-menu-1440x900-darwin.png) / [actual](actual/p09-menu-1440x900-darwin.png) / [diff](diff/p09-menu-1440x900-darwin.png) |
| P09-SS01 | Popover and Tooltip at 375x812 | [reference](reference/p09-overlays-375x812-darwin.png) / [actual](actual/p09-overlays-375x812-darwin.png) / [diff](diff/p09-overlays-375x812-darwin.png) |
| P09-SS01 | Popover and Tooltip at 1440x900 | [reference](reference/p09-overlays-1440x900-darwin.png) / [actual](actual/p09-overlays-1440x900-darwin.png) / [diff](diff/p09-overlays-1440x900-darwin.png) |
| P09-SS01 | Modal and focus trap at 375x812 | [reference](reference/p09-modal-375x812-darwin.png) / [actual](actual/p09-modal-375x812-darwin.png) / [diff](diff/p09-modal-375x812-darwin.png) |
| P09-SS01 | Modal and focus trap at 1440x900 | [reference](reference/p09-modal-1440x900-darwin.png) / [actual](actual/p09-modal-1440x900-darwin.png) / [diff](diff/p09-modal-1440x900-darwin.png) |
| P09-SS01 | Drawer and focus trap at 375x812 | [reference](reference/p09-drawer-375x812-darwin.png) / [actual](actual/p09-drawer-375x812-darwin.png) / [diff](diff/p09-drawer-375x812-darwin.png) |
| P09-SS01 | Drawer and focus trap at 1440x900 | [reference](reference/p09-drawer-1440x900-darwin.png) / [actual](actual/p09-drawer-1440x900-darwin.png) / [diff](diff/p09-drawer-1440x900-darwin.png) |
| P09-SS02 | Fleet route at 375x812 | [reference](reference/p00-atlas-fleet-375x812-darwin.png) / [actual](actual/p00-atlas-fleet-375x812-darwin.png) / [diff](diff/p00-atlas-fleet-375x812-darwin.png) |
| P09-SS02 | Fleet route at 1440x900 | [reference](reference/p00-atlas-fleet-1440x900-darwin.png) / [actual](actual/p00-atlas-fleet-1440x900-darwin.png) / [diff](diff/p00-atlas-fleet-1440x900-darwin.png) |
| P09-SS02 | Files route at 375x812 | [reference](reference/p00-atlas-files-375x812-darwin.png) / [actual](actual/p00-atlas-files-375x812-darwin.png) / [diff](diff/p00-atlas-files-375x812-darwin.png) |
| P09-SS02 | Files route at 1440x900 | [reference](reference/p00-atlas-files-1440x900-darwin.png) / [actual](actual/p00-atlas-files-1440x900-darwin.png) / [diff](diff/p00-atlas-files-1440x900-darwin.png) |

## Review decision

At 2026-07-11T20:27:52+08:00, Codex completed the delegated implementation,
evidence, and visual self-review. The zero-residue dependency audit, automated
checks, exact route comparisons, and interaction behavior support approval of
P09. This is an implementation-agent self-review, not a claim of external
human design, engineering, or accessibility approval.
