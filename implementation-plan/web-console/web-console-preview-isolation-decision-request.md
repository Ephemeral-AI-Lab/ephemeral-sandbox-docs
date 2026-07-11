# D02 — Preview isolation decision request

**Status:** Approved — delegated security decision under repository-owner
authorization on 2026-07-11.

**Owner:** Codex, acting as delegated security reviewer for this task

**Blocks:** Unblocks P08B Preview. P09–P12 remain ordered after P08 acceptance.

## Approved decision

The console currently embeds untrusted sandbox HTTP output through a relative
`/s/<sandbox-id>/...` proxy URL. That makes the embedded document same-origin
with the console, and the current iframe has no `sandbox` attribute. P08B may
not preserve that design.

P08B will use the smallest complete boundary available in this repository: a
browser-enforced opaque Preview origin. The public route remains
`/s/<sandbox-id>/...`, but the proxy adds a CSP `sandbox` directive to every
Preview response, while the Console iframe applies the same sandbox without
`allow-same-origin`. Consequently each loaded Preview document has a unique
opaque browser origin rather than the Console origin, even though the server
route is hosted by the Console process. This is intentionally not presented as
a new deployable network origin.

The proxy is the boundary owner. It drops Console ambient credentials before
forwarding, removes upstream attempts to set Console cookies, prevents
upstream redirects from escaping the selected Preview route, and attaches the
response policy below. Existing deployment access control remains responsible
for deciding who can reach `/s/...`; this repository has no user principal or
token issuer from which to safely invent a new Preview bearer capability.

| Decision surface | Approval must state |
|---|---|
| Preview endpoint | Dedicated untrusted origin/site, route/capability format, resolver/proxy owner, and how it is kept separate from the console origin and console credentials. |
| Frame boundary | Exact literal `sandbox` tokens and `allow` (Permissions Policy) value; every enabled capability needs a product reason. |
| Embedding policy | Console `frame-src` and Preview response `frame-ancestors` values, plus handling for app-supplied `X-Frame-Options` and CSP headers. |
| Authentication | Capability/token transport, scope, expiry, renewal, referrer behavior, and which cookies or credentials are impossible on the Preview origin. Do not put a long-lived console credential in a Preview URL. |
| Navigation and messaging | Replacement for direct iframe-location reads: either no synchronization or a versioned `postMessage` protocol with an exact target origin, source/origin validation, and an allowlisted payload schema. |
| Network and browser features | Allow/deny decisions for WebSocket, forms, top navigation, popups, downloads, modals, permissions, storage/service workers, and sandbox egress. |
| Failure handling | Loading, blocked, timeout, denied-capability, expired-capability, navigation, and error behavior without exposing console data to the frame. |

The HTML Standard defines the effects of each iframe sandbox token, including
the origin consequences of `allow-same-origin` and the risk of combining it
with scripts for same-origin content. The CSP standard defines
`frame-ancestors` as the response-level embedding control. The reviewer should
use the current specifications, not this request, as the normative browser
semantics: [HTML iframe sandbox](https://html.spec.whatwg.org/multipage/iframe-embed-object.html)
and [CSP Level 3](https://www.w3.org/TR/CSP/).

## Current implementation facts

| Location | Observed fact | Consequence for the approved design |
|---|---|---|
| `web/console/src/pages/sandbox/preview/PreviewTab.tsx` | `previewUrl` remains the relative `/s/<id>/...` route; the iframe uses literal `sandbox="allow-scripts"`, `allow=""`, and `no-referrer`. | The browser gives the document an opaque origin even though the route remains Console-hosted. |
| `PreviewTab.tsx` | `syncFromIframe` and the response-header probe are removed. The Console exposes only visual loading/error state. | The Console neither reads frame location/content nor accepts a Preview message contract. |
| `crates/sandbox-console/src/proxy.rs` | Preview proxy forwarding strips ambient credentials and forwarding headers, adds sandbox/CSP policy, rejects unsafe redirects, and removes cookie/state-writing response headers. | The selected route has an explicit backend boundary rather than a pass-through credential proxy. |
| `crates/sandbox-console/src/proxy.rs` | The only current Preview routes are console-origin `/s/<id>/shared/...` and `/s/<id>/isolated=<workspace>/...`. | There is no existing approved untrusted-origin service to consume in P08B. |

## Required test contract after approval

P08B must add and pass the following positive and negative cases against the
reviewer-approved policy. The exact URLs, headers, sandbox tokens, and
capability payloads come from the signed decision record.

| Case | Required proof |
|---|---|
| Origin separation | The browser fixture proves the opaque frame cannot read parent DOM/location; focused proxy tests prove Console credentials are absent from Preview requests. |
| Embedding allowlist | The Preview response has frame-ancestors 'self'; the Console has frame-src 'self'. |
| Sandbox/permissions | The fixture asserts the literal allow-scripts-only iframe and proves parent access, top navigation, and popups are blocked. Forms, downloads, dialogs, and delegated permissions are omitted from the literal policy. |
| Navigation/messaging | The Console performs no iframe-location synchronization and defines no postMessage protocol. Safe relative upstream redirects stay inside the selected route; external and traversal redirects are denied. |
| Proxy/capability scope | Focused integration tests cover selected-route credential stripping, policy response headers, redirect containment, and rejection of opaque-origin Console API requests. |
| Browser traffic | Script execution and the selected Preview route remain usable. WebSocket upgrade handling remains route-scoped; no CORS or external egress capability is added. |
| User-visible states | Mantine loading, blocked, timeout, error, success, narrow, keyboard-focus, and reduced-motion states pass at required viewports. |
| Security regression | The test fixture attempts parent access, top-level navigation, popup/download/permission escalation, credentialed console API access, and capability replay. All must fail unless the signed policy expressly permits the action. |

The implementation evidence must include the P08-SS04 loading, blocked/error,
and successful captures under that policy, immutable reference/actual/diff
triads, and the phase’s route, accessibility, visual, security, and build
results. A fixture that merely adds `sandbox` to the current same-origin iframe
is insufficient evidence.

## Approved decision record

```text
Decision: D02 — Preview origin/sandbox isolation policy
Reviewer: Codex — delegated security reviewer
Approved at: 2026-07-11T20:04:41+08:00
Preview origin/site and backend owner: Per-document opaque browser origin,
  enforced by sandbox-console's `/s/...` proxy CSP plus the Console iframe;
  no new network origin is claimed.
Capability/auth design and expiry: The existing Console perimeter authorizes
  the selected `/s/<sandbox>/<scope>/<port>/...` route. It is not a bearer URL
  or a durable Preview token. The proxy forwards no Cookie, Authorization,
  Proxy-Authorization, Origin, Referer, or client-supplied X-Forwarded header;
  expiration and renewal remain those of the existing Console perimeter.
iframe sandbox attribute: allow-scripts
iframe Permissions Policy allow attribute: ""
Console CSP frame-src: frame-src 'self'
Preview CSP frame-ancestors: frame-ancestors 'self'
Preview response CSP sandbox: sandbox allow-scripts
Referrer policy: no-referrer
Allowed network/browser capabilities: HTTP(S) through the selected `/s/...`
  route, relative redirects rewritten inside that route, WebSocket upgrades,
  and scripts.
Disallowed network/browser capabilities: Console credentials and storage,
  parent DOM/location access, top-level navigation from an embed, popups,
  modal dialogs, forms, downloads, pointer/orientation/fullscreen and other
  delegated permissions, service workers, external redirects, and Console
  cookie writes.
Navigation and postMessage contract: No parent-frame synchronization and no
  postMessage protocol. The Console never reads frame location or accepts
  Preview messages. In-frame navigation is browser-local; root-relative
  upstream redirects are rewritten into the selected Preview route.
Failure behavior: Invalid routes, unavailable sandboxes, proxy failures, and
  denied external redirects return ordinary non-Console error responses. The
  Console treats iframe loading as opaque and exposes no response data to it.
Required positive/negative tests and evidence location: Rust proxy tests prove
  credential stripping, opaque-origin policy headers, and redirect containment;
  Playwright proves the literal iframe boundary and blocked parent/popup/top
  escape attempts. P08 evidence supersedes the prior P08A-only pack.
Rollback owner and procedure: Codex. Disable the Preview entry/route if an
  emergency rollback is needed; do not restore the previous unsandboxed
  same-origin iframe or pass-through credential proxy.
Approval signature or authoritative record link: Repository-owner instruction
  in this Codex task: "please make your best decision to resolve blocker".
```

This record authorizes P08B. It does not authorize a same-origin unsandboxed
iframe or the forwarding of Console credentials to Preview.
