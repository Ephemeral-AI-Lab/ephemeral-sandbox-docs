# P03 approved shared-primitive evidence

This pack is captured from immutable console revision `aac65f046`. It approves
the P03 shared-primitive migration only: it does not claim final
production-screen visual parity, delete the remaining package dependencies
(P09), remove Tailwind (P10), or alter the P08B Preview-isolation decision.

## What passed

- `npm run test`: 17 files and 32 tests passed. The P03 contracts prove that
  no source imports a deleted local UI wrapper or Radix, RPC errors retain
  their normalization, and a normalized error is rendered by the shared,
  dismissible Mantine notification host.
- `npm run build`: TypeScript and Vite production build passed. Vite emitted
  its existing bundle-size advisory only; it is not a P03 failure.
- `npm run test:e2e`: 71 Chromium checks passed, including nine P03 fixture
  checks covering responsive gallery and form captures, Select and custom
  Combobox behavior, notification limit/stack, Menu, Popover, Tooltip, Modal,
  Drawer, portal placement, focus trapping/restoration, no horizontal
  overflow, and zero Axe violations. The existing P01 reduced-motion captures
  also remain green in this full run.

The migration accounts for all P03 primitives. 3A replaces buttons/actions,
inputs, Textarea, Select, and Combobox; 3B replaces Modal, Drawer, Popover,
Tooltip, Tabs, Menu, Breadcrumbs, and ordinary ScrollArea; 3C replaces the
notification host, badges/status, Paper/Card, and loading, empty, and error
states. `ErrorToast` remains a small EphemeralOS semantic adapter solely for
RPC normalization; Mantine owns notification rendering, four-item limiting,
and dismissal. `StateBadge` remains the product status vocabulary, now
rendered directly through Mantine `Badge`.

## Immutable screenshot triads

P03 intentionally changes visual controls. Its committed Playwright snapshots
are therefore the approved P03 reference; same-commit actual captures are
byte-identical. `compare -metric AE` reported `0 (0)` for every pair, and the
rendered zero-difference image is in `diff/`. The complete checksum record is
in [manifest.json](manifest.json).

| Requirement | Capture | Reference | Actual | Diff |
|---|---|---|---|---|
| P03-SS01 | 375x812 primitive gallery | [reference](reference/p03-primitives-375x812-darwin.png) | [actual](actual/p03-primitives-375x812-darwin.png) | [0 pixels](diff/p03-primitives-375x812-darwin.png) |
| P03-SS01 | 768x1024 primitive gallery | [reference](reference/p03-primitives-768x1024-darwin.png) | [actual](actual/p03-primitives-768x1024-darwin.png) | [0 pixels](diff/p03-primitives-768x1024-darwin.png) |
| P03-SS01 | 1024x768 primitive gallery | [reference](reference/p03-primitives-1024x768-darwin.png) | [actual](actual/p03-primitives-1024x768-darwin.png) | [0 pixels](diff/p03-primitives-1024x768-darwin.png) |
| P03-SS01 | 1440x900 primitive gallery | [reference](reference/p03-primitives-1440x900-darwin.png) | [actual](actual/p03-primitives-1440x900-darwin.png) | [0 pixels](diff/p03-primitives-1440x900-darwin.png) |
| P03-SS02 | 375x812 form, Select/Combobox, and state surfaces | [reference](reference/p03-form-states-375x812-darwin.png) | [actual](actual/p03-form-states-375x812-darwin.png) | [0 pixels](diff/p03-form-states-375x812-darwin.png) |
| P03-SS02 | 1440x900 form, Select/Combobox, and state surfaces | [reference](reference/p03-form-states-1440x900-darwin.png) | [actual](actual/p03-form-states-1440x900-darwin.png) | [0 pixels](diff/p03-form-states-1440x900-darwin.png) |
| P03-SS03 | 375x812 overlay and notification stack | [reference](reference/p03-overlays-375x812-darwin.png) | [actual](actual/p03-overlays-375x812-darwin.png) | [0 pixels](diff/p03-overlays-375x812-darwin.png) |
| P03-SS03 | 1440x900 overlay and notification stack | [reference](reference/p03-overlays-1440x900-darwin.png) | [actual](actual/p03-overlays-1440x900-darwin.png) | [0 pixels](diff/p03-overlays-1440x900-darwin.png) |
| P03-SS03 | 375x812 Menu | [reference](reference/p03-menu-375x812-darwin.png) | [actual](actual/p03-menu-375x812-darwin.png) | [0 pixels](diff/p03-menu-375x812-darwin.png) |
| P03-SS03 | 1440x900 Menu | [reference](reference/p03-menu-1440x900-darwin.png) | [actual](actual/p03-menu-1440x900-darwin.png) | [0 pixels](diff/p03-menu-1440x900-darwin.png) |
| P03-SS03 | 375x812 Modal | [reference](reference/p03-modal-375x812-darwin.png) | [actual](actual/p03-modal-375x812-darwin.png) | [0 pixels](diff/p03-modal-375x812-darwin.png) |
| P03-SS03 | 1440x900 Modal | [reference](reference/p03-modal-1440x900-darwin.png) | [actual](actual/p03-modal-1440x900-darwin.png) | [0 pixels](diff/p03-modal-1440x900-darwin.png) |
| P03-SS03 | 375x812 Drawer | [reference](reference/p03-drawer-375x812-darwin.png) | [actual](actual/p03-drawer-375x812-darwin.png) | [0 pixels](diff/p03-drawer-375x812-darwin.png) |
| P03-SS03 | 1440x900 Drawer | [reference](reference/p03-drawer-1440x900-darwin.png) | [actual](actual/p03-drawer-1440x900-darwin.png) | [0 pixels](diff/p03-drawer-1440x900-darwin.png) |

## Review decision

At `2026-07-11T09:50:20Z`, Codex reviewed the committed P03 boundary, the
1440px gallery/forms/overlays, the 375px gallery/forms/overlays, and the
complete automated evidence. The compact mobile layout, keyboard focus,
portal layering, focus restoration, error/status semantics, notification
stack, and zero-Axe gallery scan are approved for P03 scope. This is a
transparent self-review by the implementation agent, not a claim of external
human or final production-screen design approval; external design,
engineering, and accessibility reviewers remain unassigned.
