# P02 approved provider-foundation evidence

This pack is captured from immutable console revision `b042d34ab`. It approves
the P02 application-provider and global-style foundation only. It does not
claim that the remaining Radix/Tailwind components have been migrated, approve
final production-screen visual parity, or alter the P08B Preview-isolation
decision.

## What passed

- `npm run test`: 16 files and 29 tests passed, including exactly-one-host,
  stylesheet-order, provider/router rendering, notification-host, root-style,
  and removal-only Tailwind allowlist contracts.
- `npm run build`: TypeScript and Vite production build passed. Vite emitted
  its existing bundle-size advisory only; it is not a P02 failure.
- `npm run test:e2e`: 62 Chromium checks passed. The dedicated P02 fixture has
  11 checks for four responsive shell captures; notification/tooltip,
  Modal, and Drawer captures at 375 and 1440; portal placement; focus trap;
  backdrop and Escape dismissal; focus restoration; overflow/root sentinels;
  and Axe with zero violations.
- `tests/p02/tailwind-allowlist.json` freezes 410 `className` expressions,
  431 static expression parts, five dynamic expressions, and 259 utility
  tokens. The CI contract permits only removals and rejects new tokens or
  additional expressions until P10 deletes the migration allowlist.

The sole production `MantineProvider` and `Notifications` host live in
`web/console/src/AppProviders.tsx`; the existing Query, Router, and temporary
Radix providers remain nested inside it. `web/console/src/main.tsx` imports
Core styles, then Notifications styles, then the legacy stylesheet. Minimal
`html`, `body`, and `#root` sizing containment prevents reset and ownership
drift while the old Tailwind shell is still present.

## Immutable screenshot triads

This is a new P02 fixture, so its committed Playwright snapshots are the
approved reference and same-commit actual captures. Each pair is
byte-identical. `compare -metric AE` reported `0 (0)` for all ten pairs; the
corresponding rendered zero-difference image lives in `diff/`. The complete
machine-readable checksum record is in [manifest.json](manifest.json).

| Requirement | Capture | Reference | Actual | Diff |
|---|---|---|---|---|
| P02-SS01 / P02-SS03 | 375x812 shared Shell, legacy/Mantine coexistence, root sentinel | [reference](reference/p02-foundation-375x812-darwin.png) | [actual](actual/p02-foundation-375x812-darwin.png) | [0 pixels](diff/p02-foundation-375x812-darwin.png) |
| P02-SS01 / P02-SS03 | 768x1024 shared Shell, legacy/Mantine coexistence, root sentinel | [reference](reference/p02-foundation-768x1024-darwin.png) | [actual](actual/p02-foundation-768x1024-darwin.png) | [0 pixels](diff/p02-foundation-768x1024-darwin.png) |
| P02-SS01 / P02-SS03 | 1024x768 shared Shell, legacy/Mantine coexistence, root sentinel | [reference](reference/p02-foundation-1024x768-darwin.png) | [actual](actual/p02-foundation-1024x768-darwin.png) | [0 pixels](diff/p02-foundation-1024x768-darwin.png) |
| P02-SS01 / P02-SS03 | 1440x900 shared Shell, legacy/Mantine coexistence, root sentinel | [reference](reference/p02-foundation-1440x900-darwin.png) | [actual](actual/p02-foundation-1440x900-darwin.png) | [0 pixels](diff/p02-foundation-1440x900-darwin.png) |
| P02-SS02 | 375x812 notification and Tooltip portal | [reference](reference/p02-tooltip-notification-375x812-darwin.png) | [actual](actual/p02-tooltip-notification-375x812-darwin.png) | [0 pixels](diff/p02-tooltip-notification-375x812-darwin.png) |
| P02-SS02 | 1440x900 notification and Tooltip portal | [reference](reference/p02-tooltip-notification-1440x900-darwin.png) | [actual](actual/p02-tooltip-notification-1440x900-darwin.png) | [0 pixels](diff/p02-tooltip-notification-1440x900-darwin.png) |
| P02-SS02 | 375x812 Modal portal, backdrop, and keyboard focus | [reference](reference/p02-modal-375x812-darwin.png) | [actual](actual/p02-modal-375x812-darwin.png) | [0 pixels](diff/p02-modal-375x812-darwin.png) |
| P02-SS02 | 1440x900 Modal portal, backdrop, and keyboard focus | [reference](reference/p02-modal-1440x900-darwin.png) | [actual](actual/p02-modal-1440x900-darwin.png) | [0 pixels](diff/p02-modal-1440x900-darwin.png) |
| P02-SS02 | 375x812 Drawer portal and keyboard focus | [reference](reference/p02-drawer-375x812-darwin.png) | [actual](actual/p02-drawer-375x812-darwin.png) | [0 pixels](diff/p02-drawer-375x812-darwin.png) |
| P02-SS02 | 1440x900 Drawer portal and keyboard focus | [reference](reference/p02-drawer-1440x900-darwin.png) | [actual](actual/p02-drawer-1440x900-darwin.png) | [0 pixels](diff/p02-drawer-1440x900-darwin.png) |

## Review decision

At `2026-07-11T09:32:00Z`, Codex reviewed the committed provider boundary, the
1440px shared-Shell and Modal captures, the 375px shared-Shell and
notification/Tooltip captures, and the complete automated evidence above. The
stylesheet order, compact legacy/Mantine coexistence, visible focus, portal
stacking, and no-reset-drift sentinels are approved for P02 foundation scope.
This is a transparent self-review by the implementation agent, not a claim of
external-human or final production-screen design approval; external design,
engineering, and accessibility reviewers remain unassigned.
