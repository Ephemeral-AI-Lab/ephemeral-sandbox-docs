# P08B approved Preview evidence — P08 complete

This immutable pack is captured from Console revision cfae89ede9. Together
with the immutable P08A Files pack at f1073cd29, it closes P08. This pack
approves only the Preview isolation policy, Preview UI, and their evidence; it
does not rewrite or replace the P08A Files history.

## Approved D02 policy

Preview remains reachable through the selected Console /s route, but its
document receives an opaque browser origin. Both the Console iframe and the
Preview response use a literal sandbox allowing scripts only. The frame has no
same-origin capability, no form or download capability, no delegated browser
permissions, no popup or top-level-navigation escape, and no parent-frame
coordination.

The Preview proxy strips Cookie, Authorization, Proxy-Authorization, Origin,
Referer, and client-supplied forwarding headers before proxying. It denies
Preview cookie/state-writing response headers, rewrites only safe relative
redirects inside the already-selected Preview route, and rejects external,
scheme-relative, traversal, and encoded-bypass redirect targets. The Console
also rejects an opaque Origin: null request to an /api route, so a script in
the framed Preview cannot call the Console API surface.

## What passed

- cargo check -p sandbox-console
- cargo test -p sandbox-console --lib: four tests passed.
- cargo test -p sandbox-console --test proxy_security: two real-proxy
  integration tests passed.
- npm run test: 17 files and 34 tests passed.
- npm run build: TypeScript and the Vite production build passed; only the
  existing bundle-size advisory was emitted.
- Dedicated P08 Preview Playwright fixture: seven checks passed without a
  snapshot update. It covers the literal iframe boundary, script execution,
  blocked parent DOM/top navigation/popup attempts, blocked opaque-origin API
  access, normal success at four viewport sizes, loading, and proxy error.
- The complete Playwright suite passed under Node 24.14.0.

The aggregate cargo test -p sandbox-console --test console target was not used
as a P08 gate because its pre-existing test harness requires missing phase-0
documentation fixtures. The focused proxy integration test above exercises
the Preview boundary directly and passes.

## Immutable screenshot triads

Reference, actual, and diff files are committed for every row. ImageMagick
compare reported zero changed pixels for each pair. The actual captures were
visually reviewed: loading provides explicit status without inspecting frame
contents, and a proxy failure remains contained inside the Preview frame.

| Requirement | Capture | Reference / actual / diff |
|---|---|---|
| P08-SS01 | Preview success at 375x812 | [reference](reference/p08-preview-success-375x812-darwin.png) / [actual](actual/p08-preview-success-375x812-darwin.png) / [diff](diff/p08-preview-success-375x812-darwin.png) |
| P08-SS01 | Preview success at 768x1024 | [reference](reference/p08-preview-success-768x1024-darwin.png) / [actual](actual/p08-preview-success-768x1024-darwin.png) / [diff](diff/p08-preview-success-768x1024-darwin.png) |
| P08-SS01 | Preview success at 1024x768 | [reference](reference/p08-preview-success-1024x768-darwin.png) / [actual](actual/p08-preview-success-1024x768-darwin.png) / [diff](diff/p08-preview-success-1024x768-darwin.png) |
| P08-SS01 | Preview success at 1440x900 | [reference](reference/p08-preview-success-1440x900-darwin.png) / [actual](actual/p08-preview-success-1440x900-darwin.png) / [diff](diff/p08-preview-success-1440x900-darwin.png) |
| P08-SS04 | Preview loading at 1440x900 | [reference](reference/p08-preview-loading-1440x900-darwin.png) / [actual](actual/p08-preview-loading-1440x900-darwin.png) / [diff](diff/p08-preview-loading-1440x900-darwin.png) |
| P08-SS04 | Preview proxy error at 1440x900 | [reference](reference/p08-preview-error-1440x900-darwin.png) / [actual](actual/p08-preview-error-1440x900-darwin.png) / [diff](diff/p08-preview-error-1440x900-darwin.png) |

## Review decision

At 2026-07-11T20:04:41+08:00, Codex acted as the delegated security reviewer
authorized by the repository-owner instruction recorded in the D02 decision.
The implementation, tests, screenshot triads, and manual visual review support
approval of P08B and completion of P08. This is an implementation-agent
self-review, not a claim of external human design, engineering, accessibility,
or security approval.
