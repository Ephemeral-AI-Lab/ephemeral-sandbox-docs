# P00 provisional fixture-only evidence

This is a P00 compatibility and trust capture from console `0f7d024867fc` with
a dirty worktree. It is deliberately **not immutable**, not an approved
baseline, and not a completion claim. The machine-readable record is in
[manifest.json](manifest.json).

## What passed

- `npm run test`: 13 files and 22 tests passed. The suite covers the
  Mantine import/render spike and the named Event, trace, stdin, publication,
  transcript, file-conflict, Fleet, ready-polling, and polling-cadence
  contracts.
- `npm run build`: TypeScript and Vite production build passed.
- `npm run test:e2e`: six Chromium checks passed: real keyboard focus and
  portal behavior, an Axe scan with zero violations, deterministic visual
  regression snapshots, and intercepted request proof of the fast polling
  cadence plus window-focus catch-up. The other two checks use the sanitized
  trust fixture to create and capture the visible paused-tail, publication
  rejection, and preserved-draft states at desktop and mobile viewports.

The fixture imports the pinned Mantine 9.4.1 packages and verifies the CSS
order (`@mantine/core/styles.css` before `@mantine/notifications/styles.css`),
Combobox virtualization, Tree, CodeMirror, uPlot, form validation, reduced
motion, Modal focus behavior, Tooltip, and notifications. The P00 fixture is
test-only; production provider work remains in P02.

## P00-SS02: disposable Mantine fixture

All captures below are sanitized. Their status is **Review required**; they
are evidence of a working compatibility spike, not design approval.

| Viewport | State | Artifact |
|---|---|---|
| 1440x900 | idle | [desktop idle](screenshots/p00-ss02-desktop-idle-1440x900.png) |
| 1440x900 | validation, keyboard Tooltip, notification | [desktop interaction](screenshots/p00-ss02-desktop-interaction-1440x900.png) |
| 1440x900 | Modal focus trap | [desktop modal](screenshots/p00-ss02-desktop-modal-1440x900.png) |
| 375x812 | idle | [mobile idle](screenshots/p00-ss02-mobile-idle.png) |
| 375x812 | validation, keyboard Tooltip, notification | [mobile interaction](screenshots/p00-ss02-mobile-interaction.png) |
| 375x812 | Modal focus trap | [mobile modal](screenshots/p00-ss02-mobile-modal.png) |

## P00-SS03: sanitized trust-state fixture

The fixture mounts the real Events, CommandCard, and FileView components with
intercepted deterministic RPC responses. It pauses the Events tail, supplies a
publication-rejected ledger entry, edits a local file draft, and returns a
changed server file on save. No live console route or sandbox metadata is used.

| Viewport | State | Artifact |
|---|---|---|
| 1440x900 | paused tail, rejection, preserved draft | [desktop trust state](screenshots/p00-ss03-trust-1440x900.png) |
| 375x812 | paused tail, rejection, preserved draft | [mobile trust state](screenshots/p00-ss03-trust-375x812.png) |

## Outstanding required evidence

- **P00-SS01:** not captured. The local live route atlas contains a real
  sandbox identifier, so it is excluded. Create deterministic sanitized
  fixtures from existing API types before capture.
- Pin and record the exact Chromium revision, OS image, and fonts; rerun from
  a committed console revision before requesting visual approval or promotion.

## Review decision

No design, engineering, accessibility, or security reviewer has approved this
pack. Screenshot approval, P00 completion, and baseline promotion remain
blocked on the outstanding captures, a committed source revision, and recorded
reviewer decisions.
