# P01 approved theme-fixture evidence

This pack is captured from immutable console revision `0ce628786a83`. It
approves the P01 logo, token, and fixture acceptance criteria only. It does not
promote a production-screen visual baseline, alter the P08B Preview-isolation
decision, or replace the P02 provider/global-style gate.

## What passed

- `npm run test`: 14 files and 26 tests passed, including the durable logo
  checksum, complete color-scale, contrast, z-index, and CSS-module breakpoint
  drift contracts.
- `npm run build`: TypeScript and Vite production build passed; the emitted
  `dist/assets/images/logo.png` SHA-256 equals the durable public source asset.
- `npx playwright test tests/browser/P01ThemeFixture.spec.ts`: 9 Chromium
  checks passed: four viewport snapshots, state/focus snapshots at 375 and
  1440, reduced-motion/logo checks at both widths, no horizontal overflow, and
  Axe with zero violations.

The durable source asset is
`web/console/public/assets/images/logo.png` (SHA-256
`42a06f2cdf37becedf0b4436fdcb6fd8cee4e6a93120cfbd4cee727ba84fc81a`). It
preserves the exact pixels from historical canonical source
`f3bd2ab6451038731b8782906b28d02fd751eca9:asset/logo.png`; no application
source imports a generated `dist` asset.

## Immutable screenshot triads

This is a new P01 fixture, so its committed Playwright snapshots are the
approved reference and the same-commit actual captures. Each pair is
byte-identical. `compare -metric AE` reported `0 (0)` for all eight pairs; the
corresponding rendered zero-difference image lives in `diff/`. The complete
machine-readable checksum record is in [manifest.json](manifest.json).

| Requirement | Capture | Reference | Actual | Diff |
|---|---|---|---|---|
| P01-SS01 | 375x812 normal | [reference](reference/p01-theme-375x812-darwin.png) | [actual](actual/p01-theme-375x812-darwin.png) | [0 pixels](diff/p01-theme-375x812-darwin.png) |
| P01-SS01 | 768x1024 normal | [reference](reference/p01-theme-768x1024-darwin.png) | [actual](actual/p01-theme-768x1024-darwin.png) | [0 pixels](diff/p01-theme-768x1024-darwin.png) |
| P01-SS01 | 1024x768 normal | [reference](reference/p01-theme-1024x768-darwin.png) | [actual](actual/p01-theme-1024x768-darwin.png) | [0 pixels](diff/p01-theme-1024x768-darwin.png) |
| P01-SS01 | 1440x900 normal | [reference](reference/p01-theme-1440x900-darwin.png) | [actual](actual/p01-theme-1440x900-darwin.png) | [0 pixels](diff/p01-theme-1440x900-darwin.png) |
| P01-SS02 | 375x812 states/focus | [reference](reference/p01-theme-states-375x812-darwin.png) | [actual](actual/p01-theme-states-375x812-darwin.png) | [0 pixels](diff/p01-theme-states-375x812-darwin.png) |
| P01-SS02 | 1440x900 states/focus | [reference](reference/p01-theme-states-1440x900-darwin.png) | [actual](actual/p01-theme-states-1440x900-darwin.png) | [0 pixels](diff/p01-theme-states-1440x900-darwin.png) |
| P01-SS03 | 375x812 reduced motion/logo | [reference](reference/p01-theme-reduced-375x812-darwin.png) | [actual](actual/p01-theme-reduced-375x812-darwin.png) | [0 pixels](diff/p01-theme-reduced-375x812-darwin.png) |
| P01-SS03 | 1440x900 reduced motion/logo | [reference](reference/p01-theme-reduced-1440x900-darwin.png) | [actual](actual/p01-theme-reduced-1440x900-darwin.png) | [0 pixels](diff/p01-theme-reduced-1440x900-darwin.png) |

## Review decision

At `2026-07-11T09:23:18Z`, Codex reviewed the committed source, the 1440px
normal specimen, the 375px keyboard-focus state specimen, and the complete
automated evidence above. The compact layout, warm-neutral/eye-blue palette,
visible keyboard focus, textual lifecycle labels, and uncropped decorative logo
are approved for P01 fixture scope. This is a transparent self-review by the
implementation agent, not a claim of external-human or final production-screen
design approval; the external design reviewer remains unassigned.
