# P05 approved Fleet and Overview evidence

This pack is captured from immutable console revision `0173407bc`. It approves
the P05 Fleet, creation, WorkspacePicker, sandbox-header, and Overview
migration only. Terminal/Observability migration, package cleanup, Tailwind
removal, and the P08B Preview-isolation decision remain separate work.

## What passed

- `npm run test`: 17 files and 34 tests passed.
- `npm run build`: TypeScript and the Vite production bundle passed; Vite
  emitted its existing bundle-size advisory only.
- `npm run test:e2e`: all 125 Chromium checks passed. The dedicated P05 suite
  has 15 checks: five Fleet viewport captures (including 1920x1080), four
  geometry checks, loading/stale/empty/error states, creation and picker
  keyboard focus, a 10,000-directory virtual-search flow, and Axe audits.

The implementation uses Mantine `Flex`, `Card`, `Modal`, `Combobox`, inputs,
and layout primitives. Fleet renders a single stable slow/fast generation,
keeps last-confirmed cards on refresh failure, and removes its Layers/Squash
content. WorkspacePicker uses the existing TanStack virtualizer: fewer than 64
folder options render for a 10,000-directory source and the targeted result
appears within one second. Systematic debugging fixed the nested Escape-focus
handoff and made the Axe audit wait for the dialog transition, so the approved
checks cover the actual visible/focused state rather than a transient one.

## Immutable screenshot triads

The committed Playwright snapshots below are the approved P05 reference.
Same-commit actual captures are byte-identical. `compare -metric AE` reported
`0 (0)` for all 16 reference/actual pairs, with the corresponding rendered
zero-difference image in `diff/`. [manifest.json](manifest.json) records
checksums, geometry assertions, and the complete capture inventory.

| Requirement | Capture | Reference / actual / diff |
|---|---|---|
| P05-SS01 | Mixed Fleet at 375x812, 768x1024, 1024x768, and 1440x900; Overview at the same four viewports | [reference](reference/) / [actual](actual/) / [diff](diff/) |
| P05-SS02 | Start-aligned, non-stretched 1440x900 and 1920x1080 Fleet rows | [1440 reference](reference/p05-fleet-mixed-1440x900-darwin.png) / [1920 reference](reference/p05-fleet-mixed-1920x1080-darwin.png) / [0 pixels](diff/p05-fleet-mixed-1920x1080-darwin.png) |
| P05-SS03 | Full-width 375 Fleet cards, Create sandbox modal, and WorkspacePicker with keyboard focus | [Fleet](reference/p05-fleet-mixed-375x812-darwin.png) / [Create](reference/p05-create-375x812-darwin.png) / [Picker](reference/p05-workspace-picker-375x812-darwin.png) |
| P05-SS04 | Loading, fresh/mixed, stale, error, empty, truncated, and refresh-update behavior | [state references](reference/) / [state actuals](actual/) / [0-pixel diffs](diff/) |

## Geometry and behavior record

The dedicated geometry test inspected every one of seven cards at 375x812,
768x1024, 1440x900, and 1920x1080. It confirms no horizontal body overflow,
`flex-grow: 0`, a maximum card height of 308px (22rem), full collection width
below 768px, a maximum card width of 392px (28rem) at and above 768px, and a
partial row whose first card shares the collection start x-position. The test
also preserves prior card order across refreshed data; the source unit tests
cover active-workspace fast polling and the stable-order helper.

## Review decision

At `2026-07-11T10:28:17Z`, Codex reviewed the committed P05 boundary, direct
Fleet/creation/WorkspacePicker captures, the four Overview captures, and the
complete automated evidence. The Mantine migration, state behavior, geometry,
virtualization, keyboard focus, and accessibility evidence are approved for P05
scope. This is a transparent implementation-agent self-review, not external
human or final production-screen design approval; external design, engineering,
and accessibility reviewers remain unassigned. P08B Preview isolation remains
an independent security approval gate.
