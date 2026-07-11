# P00 approved fixture-only evidence

This is a P00 compatibility and trust capture from committed console revision
`8153d6f43`. It is deliberately **not a final migrated visual baseline** or a
design promotion. The machine-readable record is in [manifest.json](manifest.json).

## What passed

- `npm run test`: 13 files and 22 tests passed. The suite covers the
  Mantine import/render spike and the named Event, trace, stdin, publication,
  transcript, file-conflict, Fleet, ready-polling, and polling-cadence
  contracts.
- `npm run build`: TypeScript and Vite production build passed.
- `npm run test:e2e`: 42 Chromium checks passed: real keyboard focus and
  portal behavior, an Axe scan with zero violations, deterministic visual
  regression snapshots, intercepted request proof of the fast polling cadence
  plus window-focus catch-up, the 36-image sanitized route atlas, and the two
  desktop/mobile trust-state captures.

The fixture imports the pinned Mantine 9.4.1 packages and verifies the CSS
order (`@mantine/core/styles.css` before `@mantine/notifications/styles.css`),
Combobox virtualization, Tree, CodeMirror, uPlot, form validation, reduced
motion, Modal focus behavior, Tooltip, and notifications. The P00 fixture is
test-only; production provider work remains in P02.

## P00-SS01: sanitized pre-migration route atlas

The deterministic atlas mounts the real route components with intercepted,
typed fixture responses. Every capture uses only `fixture-sandbox` data; it
does not access a live console route or sandbox. The shared Shell is visible in
each sandbox-route capture. Preview deliberately has no selected port or
iframe, so this capture neither bypasses nor approves the outstanding P08B
isolation decision.

| Route | 375x812 | 768x1024 | 1024x768 | 1440x900 |
|---|---|---|---|---|
| Fleet | [375](screenshots/p00-ss01-fleet-375x812.png) | [768](screenshots/p00-ss01-fleet-768x1024.png) | [1024](screenshots/p00-ss01-fleet-1024x768.png) | [1440](screenshots/p00-ss01-fleet-1440x900.png) |
| Overview | [375](screenshots/p00-ss01-overview-375x812.png) | [768](screenshots/p00-ss01-overview-768x1024.png) | [1024](screenshots/p00-ss01-overview-1024x768.png) | [1440](screenshots/p00-ss01-overview-1440x900.png) |
| Terminal | [375](screenshots/p00-ss01-terminal-375x812.png) | [768](screenshots/p00-ss01-terminal-768x1024.png) | [1024](screenshots/p00-ss01-terminal-1024x768.png) | [1440](screenshots/p00-ss01-terminal-1440x900.png) |
| Resources | [375](screenshots/p00-ss01-resources-375x812.png) | [768](screenshots/p00-ss01-resources-768x1024.png) | [1024](screenshots/p00-ss01-resources-1024x768.png) | [1440](screenshots/p00-ss01-resources-1440x900.png) |
| Events | [375](screenshots/p00-ss01-events-375x812.png) | [768](screenshots/p00-ss01-events-768x1024.png) | [1024](screenshots/p00-ss01-events-1024x768.png) | [1440](screenshots/p00-ss01-events-1440x900.png) |
| Traces | [375](screenshots/p00-ss01-traces-375x812.png) | [768](screenshots/p00-ss01-traces-768x1024.png) | [1024](screenshots/p00-ss01-traces-1024x768.png) | [1440](screenshots/p00-ss01-traces-1440x900.png) |
| Layers | [375](screenshots/p00-ss01-layers-375x812.png) | [768](screenshots/p00-ss01-layers-768x1024.png) | [1024](screenshots/p00-ss01-layers-1024x768.png) | [1440](screenshots/p00-ss01-layers-1440x900.png) |
| Files | [375](screenshots/p00-ss01-files-375x812.png) | [768](screenshots/p00-ss01-files-768x1024.png) | [1024](screenshots/p00-ss01-files-1024x768.png) | [1440](screenshots/p00-ss01-files-1440x900.png) |
| Preview | [375](screenshots/p00-ss01-preview-375x812.png) | [768](screenshots/p00-ss01-preview-768x1024.png) | [1024](screenshots/p00-ss01-preview-1024x768.png) | [1440](screenshots/p00-ss01-preview-1440x900.png) |

The 36 image digests are recorded in
[p00-ss01-route-atlas.sha256](screenshots/p00-ss01-route-atlas.sha256).
Their status is **Approved — P00 fixture evidence only**. The capture records
Playwright Chromium 149.0.7827.55, macOS 26.4.1 (25E253), and the
`system_profiler` font-inventory digest. It establishes the pre-migration
baseline and is not an approval of the final migrated design.

## P00-SS02: disposable Mantine fixture

All captures below are sanitized. Their status is **Approved — P00 fixture
evidence only**; they are evidence of a working compatibility spike, not
design approval.

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

## Scope and remaining security decision

All P00 screenshot groups are captured from the recorded committed revision
and approved as fixture evidence. The [review and Preview-isolation decision
record](review-decision.md) captures the observed boundary, required owner, and
minimum P08B verification contract. P08B approval is pending; it does not block
non-Preview migration work.

## Review decision

Codex reviewed this pack at `2026-07-11T09:11:53Z` after re-running the exact
Node 24.14.0 unit, build, and browser commands, confirming all 36 route-atlas
checksums, inspecting the captured fixture states, and confirming the recorded
keyboard/portal/focus and zero-Axe evidence. This approves the P00
compatibility, trust, and baseline-capture evidence only. It neither approves
the final migrated visual design nor approves Preview isolation.
