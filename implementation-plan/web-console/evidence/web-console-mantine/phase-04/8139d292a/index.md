# P04 approved Shell and navigation evidence

This pack is captured from immutable console revision `8139d292a`. It approves the P04 Shell, routing, and navigation migration only. Fleet/Overview migration, package cleanup, Tailwind removal, and the P08B Preview-isolation decision remain separate work.

## What passed

- `npm run test`: 17 files and 32 tests passed.
- `npm run build`: TypeScript and the Vite production bundle passed; Vite emitted its existing bundle-size advisory only.
- `npm run test:e2e`: all 110 Chromium checks passed. The 39 P04 checks cover 36 route/viewport structural states; legacy Layers redirect query/hash retention; skip-to-main, scoped tab keyboard navigation, bounded route scrolling; and narrow Drawer focus, Escape dismissal, and trigger-focus restoration. Route capture waits for the canonical logo image to decode before screenshotting.

The migration replaces the stable frame with Mantine `AppShell`, `Drawer`, `Burger`, `Breadcrumbs`, `Tabs`, `Anchor`, and `Image`. Every route has one semantic main region and—outside Fleet—one bounded route scroll owner. The legacy `/sandboxes/:sandboxId/layerstack` form redirects to the canonical Observability Layers route while preserving query string and hash.

## Immutable screenshot triads

P04 intentionally changes the application frame, so the committed Playwright snapshots below are the approved P04 reference. Same-commit actual captures are byte-identical. `compare -metric AE` reported `0 (0)` for every pair and the rendered zero-difference image is in `diff/`. The complete capture inventory and SHA-256 record is in [manifest.json](manifest.json). The Route Atlas filenames retain their original `p00-atlas` prefix for longitudinal baseline identity; every image was recaptured from the P04 revision.

| Requirement | Capture | Reference / actual / diff |
|---|---|---|
| P04-SS01 | 36 route-atlas states: Fleet, Overview, Terminal, Files, Resources, Traces, Events, Layers, and Preview at 375x812, 768x1024, 1024x768, and 1440x900 | [reference directory](reference/) / [actual directory](actual/) / [diff directory](diff/) |
| P04-SS02 | 375x812 narrow navigation Drawer with focused active item | [reference](reference/p04-navigation-open-375x812-darwin.png) / [actual](actual/p04-navigation-open-375x812-darwin.png) / [0 pixels](diff/p04-navigation-open-375x812-darwin.png) |
| P04-SS03 | 1024x768 keyboard focus and bounded route scroll | [reference](reference/p04-shell-keyboard-scroll-1024x768-darwin.png) / [actual](actual/p04-shell-keyboard-scroll-1024x768-darwin.png) / [0 pixels](diff/p04-shell-keyboard-scroll-1024x768-darwin.png) |

## Review decision

At `2026-07-11T10:06:09Z`, Codex reviewed the committed P04 boundary, all route-atlas viewport captures, the narrow Drawer, keyboard/scroll capture, and the complete automated evidence. The stable shell, route containment, active navigation, redirect compatibility, and tested keyboard/focus behavior are approved for P04 scope. This is a transparent self-review by the implementation agent, not a claim of external human or final production-screen design approval; external design, engineering, and accessibility reviewers remain unassigned. P08B Preview isolation remains an independent security approval gate.
