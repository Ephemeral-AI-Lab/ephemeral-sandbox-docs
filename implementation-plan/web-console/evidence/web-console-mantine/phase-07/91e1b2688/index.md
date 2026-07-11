# P07 approved Observability evidence

This immutable pack is captured from console revision `91e1b2688`. It approves
the P07 Observability migration only: Resources, Events/log stream, Traces,
and Layers. Files/Preview, Radix removal, Tailwind removal, dependency
cleanup, the release gate, and the P08B Preview-isolation decision remain
separate work.

## What passed

- `npm run test`: 17 files and 34 tests passed.
- `npm run build`: TypeScript and the Vite production bundle passed; Vite
  emitted its existing bundle-size advisory only.
- `npx playwright test tests/browser/P07ObservabilityFixture.spec.ts`: 27 P07
  browser checks passed. They cover all four observability surfaces at the
  four standard viewports, paused/error/resume Event polling, TanStack Table
  sorting/selection/expanded attributes, bounded 2,000-event rows, a
  2,000-span virtual waterfall, span detail, a narrow Trace Drawer, numerical
  chart summaries, the explicit first-500 layer-detail limit, and Axe.
- `npm run test:e2e`: all 161 Chromium checks passed without updating
  snapshots. The approved P07 surface refresh promoted the 16 Observability
  Route Atlas baselines; the Trust fixture and the P04 narrow Drawer baseline
  were also regenerated because they embed the migrated Events/Resources UI.

Events retain the API's absolute `sinceMs` threshold and disable their query
when Tail is paused. The table uses TanStack Table for its headless row and
sorting model, remains keyboard-selectable, and virtualizes only above the
200-row measured threshold. Resources retain stable uPlot instances, update
their data incrementally, resize through `ResizeObserver`, and expose latest,
minimum, and maximum summaries. Traces keep the backend `{ offset_ms, event }`
shape, label discovery as a last-200-event inference, iteratively flatten
spans, and use a bounded native waterfall scroll owner. The only correlation
link is the explicit Event trace identifier; no correlation is inferred from
attributes or current selection. Layers state the backend's first-500-entry
limit exactly.

## Debugging record

Systematic debugging resolved three P07 evidence risks before approval:

- A standalone fixture could let the Events and Trace roots grow to the full
  virtual height, defeating viewport measurement. Each root now owns its
  available flex height, so the native inner table/waterfall viewport remains
  bounded.
- In zero-layout test environments TanStack Virtual can initially report no
  virtual rows. The waterfall renders a bounded first-20-row fallback until
  the virtualizer measures, preserving both test visibility and the production
  virtual scroll path.
- The P07 polling assertion sampled its request counter just before Pause
  committed, occasionally including an already queued 400ms interval. It now
  waits for the paused state and the one boundary to settle, then proves no
  subsequent request over the next polling window; five repeated runs passed.

## Immutable screenshot triads

The committed Playwright snapshots below are the approved P07 reference.
Same-commit actual captures are byte-identical; `compare -metric AE` reported
`0 (0)` for every pair. [manifest.json](manifest.json) records hashes,
requirements, timing, and test assertions.

| Requirement | Capture | Reference / actual / diff |
|---|---|---|
| P07-SS01 | Resources, Events/log stream, Traces, and Layers at 375x812, 768x1024, 1024x768, and 1440x900 | [reference](reference/) / [actual](actual/) / [diff](diff/) |
| P07-SS02 | Focused/expanded, paused, stale/error Events at 375x812 and 1440x900 | [375](reference/p07-events-paused-stale-expanded-375x812-darwin.png) / [1440](reference/p07-events-paused-stale-expanded-1440x900-darwin.png) |
| P07-SS03 | Resource chart summaries, span detail, and 2,000-span tree/waterfall at 1440x900 | [resources](reference/p07-resources-1440x900-darwin.png) / [detail](reference/p07-traces-span-detail-1440x900-darwin.png) / [waterfall](reference/p07-traces-2k-mid-1440x900-darwin.png) |
| P07-SS04 | Trace Drawer and independent overflowing waterfall at 375x812 | [Drawer](reference/p07-traces-drawer-375x812-darwin.png) / [overflow](reference/p07-traces-drawer-overflow-375x812-darwin.png) |

## Review decision

At `2026-07-11T19:18:00+08:00`, Codex self-reviewed the committed P07 scope,
the responsive/live-state/large-trace captures, and the complete automated
evidence. P07 is approved for the Observability migration boundary. This is
transparent implementation-agent self-review, not external human design,
engineering, accessibility, or production-screen sign-off; those reviewers
remain unassigned. P08 may consume P07; P08B Preview isolation remains an
independent security gate.
