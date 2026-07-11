# P06 approved Terminal evidence

This immutable pack is captured from console revision `9bc8d4107`. It
approves the P06 Terminal workspace migration only: Sessions rail/Drawer,
toolbar and composer, command ledger cards, transcript chrome and stdin
controls. Observability, Files/Preview, package cleanup, Tailwind removal, and
the P08B Preview-isolation decision remain separate work.

## What passed

- `npm run test`: 17 files and 34 tests passed.
- `npm run build`: TypeScript and the Vite production bundle passed; Vite
  emitted its existing bundle-size advisory only.
- `npx playwright test tests/browser/P06TerminalFixture.spec.ts`: nine P06
  browser checks passed. They cover the four responsive navigation layouts,
  history filtering versus execution target, timeout blocking, Ctrl-C/Ctrl-D
  de-duplication, an authoritative publication rejection, stale transcript
  feedback, 10,000-line virtualization, a 10,000-character line, and Axe.
- `npm run test:e2e`: all 134 Chromium checks passed. The four Terminal Route
  Atlas baselines and the two Trust fixture baselines were regenerated because
  the approved Mantine `CommandCard` is rendered by those fixtures.

The implementation keeps TanStack Virtual's page/offset model and its native
transcript viewport. `TranscriptPollProvider` owns one route-level timer,
round-robins at most four active running transcript callbacks per tick, slows
while the document is hidden, and nudges on focus/visibility changes. Cache
records remain keyed by sandbox and command; history filtering never changes
the selected workspace execution target.

## Debugging record

Systematic debugging corrected three observable P06 risks before approval:

- A tail request could be mistaken for an intermediate virtualizer scroll and
  clear tail intent. The viewer now settles programmatic scroll events for
  48 ms before treating a scroll as user intent.
- A transcript refresh failure was written into the cache but did not trigger a
  render. The failure path now increments the viewer version so the visible
  alert is authoritative.
- Collapsed cards could retain dormant polling work. Explicit expanded guards
  plus an unmounted Mantine `Collapse` ensure only visible running cards
  register with the provider.

The large-output test initially used an estimated virtual offset that could
race dynamic row measurement. It now anchors to the measured long row, freezes
fixture time, and asserts that fewer than 128 virtual rows are mounted, the
10,000-character row is visible and contained, and the tail remains reachable.

## Immutable screenshot triads

The committed Playwright snapshots below are the approved P06 reference.
Same-commit actual captures are byte-identical; `compare -metric AE` reported
`0 (0)` for every pair. [manifest.json](manifest.json) records hashes,
requirements, timing, and test assertions.

| Requirement | Capture | Reference / actual / diff |
|---|---|---|
| P06-SS01 | Session rail on desktop and Drawer/stack at 375x812, 768x1024, 1024x768, 1440x900 | [reference](reference/) / [actual](actual/) / [diff](diff/) |
| P06-SS02 | Invalid timeout at 375x812; stale transcript error and authoritative publication rejection at 1440x900 | [timeout](reference/p06-terminal-invalid-timeout-375x812-darwin.png) / [rejection](reference/p06-terminal-stale-rejected-1440x900-darwin.png) |
| P06-SS03 | 10,000-line mid-scroll/tail and a 10,000-character row at 1440x900 | [mid-scroll](reference/p06-terminal-10k-mid-1440x900-darwin.png) / [tail](reference/p06-terminal-10k-tail-1440x900-darwin.png) |

## Review decision

At `2026-07-11T18:58:00+08:00`, Codex self-reviewed the committed P06 scope,
the responsive, stale/rejection, and large-output captures, and the complete
automated evidence. P06 is approved for the Terminal migration boundary. This
is transparent implementation-agent self-review, not external human design,
engineering, accessibility, or production-screen sign-off; those reviewers
remain unassigned. P08B Preview isolation remains an independent security
gate.
