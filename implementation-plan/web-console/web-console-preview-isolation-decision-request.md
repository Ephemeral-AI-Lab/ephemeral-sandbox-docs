# D02 — Preview isolation decision request

**Status:** Pending security approval — this is a request and test contract,
not an authorization to change Preview.

**Owner:** Security reviewer (unassigned)

**Blocks:** P08B Preview, then P09–P12 by the ordered migration plan.

## Decision required

The console currently embeds untrusted sandbox HTTP output through a relative
`/s/<sandbox-id>/...` proxy URL. That makes the embedded document same-origin
with the console, and the current iframe has no `sandbox` attribute. P08B may
not preserve that design.

The security reviewer must approve one complete isolation boundary before P08B
starts. The approval record must name the reviewer and date, and select every
item in the following table rather than relying on a generic sandboxed
description.

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
| `web/console/src/pages/sandbox/preview/PreviewTab.tsx` | `previewUrl` is the relative `/s/<id>/...` route and the iframe has no `sandbox` or Permissions Policy. | The frame is same-origin today; P08B needs an origin and frame-capability change, not only Mantine controls. |
| `PreviewTab.tsx` | `syncFromIframe` reads `frame.contentWindow.location`; the blocked-state probe fetches `previewUrl` and reads response headers. | Both are same-origin assumptions. A cross-origin implementation needs an approved replacement; it cannot silently retain these accesses. |
| `crates/sandbox-console/src/proxy.rs` | The console proxy forwards arbitrary Preview request/response headers, body, query, and WebSocket upgrades. | A dedicated origin requires an explicit backend boundary and header/auth/capability policy; the current pass-through proxy is not an isolation design. |
| `crates/sandbox-console/src/proxy.rs` | The only current Preview routes are console-origin `/s/<id>/shared/...` and `/s/<id>/isolated=<workspace>/...`. | There is no existing approved untrusted-origin service to consume in P08B. |

## Required test contract after approval

P08B must add and pass the following positive and negative cases against the
reviewer-approved policy. The exact URLs, headers, sandbox tokens, and
capability payloads come from the signed decision record.

| Case | Required proof |
|---|---|
| Origin separation | Loaded frame origin differs from the console origin; direct parent DOM/location reads fail; console session credentials are absent from Preview requests. |
| Embedding allowlist | The approved console can embed Preview; an unapproved ancestor is rejected by the response policy. |
| Sandbox/permissions | Every selected capability works; each unselected capability is blocked, including top navigation, popups, downloads, forms, dialogs, and permissions as applicable. |
| Navigation/messaging | In-frame navigation and approved navigation reporting work without cross-origin location access; malformed, wrong-origin, and wrong-source messages are rejected. |
| Proxy/capability scope | Valid Preview capability reaches only its selected sandbox, scope, port, and expiry; altered, expired, cross-sandbox, and API-targeting requests fail. |
| Browser traffic | Required assets, redirects, WebSocket traffic, and CORS behavior work only under the approved policy; unapproved egress/upgrade paths fail. |
| User-visible states | Mantine loading, blocked, timeout, error, success, narrow, keyboard-focus, and reduced-motion states pass at required viewports. |
| Security regression | The test fixture attempts parent access, top-level navigation, popup/download/permission escalation, credentialed console API access, and capability replay. All must fail unless the signed policy expressly permits the action. |

The implementation evidence must include the P08-SS04 loading, blocked/error,
and successful captures under that policy, immutable reference/actual/diff
triads, and the phase’s route, accessibility, visual, security, and build
results. A fixture that merely adds `sandbox` to the current same-origin iframe
is insufficient evidence.

## Approval record to complete

```text
Decision: D02 — Preview origin/sandbox isolation policy
Reviewer: <name and security role>
Approved at: <ISO-8601 timestamp>
Preview origin/site and backend owner: <value>
Capability/auth design and expiry: <value>
iframe sandbox attribute: <literal value>
iframe Permissions Policy allow attribute: <literal value>
Console CSP frame-src: <literal value>
Preview CSP frame-ancestors: <literal value>
Referrer policy: <literal value>
Allowed network/browser capabilities: <value>
Disallowed network/browser capabilities: <value>
Navigation and postMessage contract: <value>
Required positive/negative tests and evidence location: <value>
Rollback owner and procedure: <value>
Approval signature or authoritative record link: <value>
```

Until that record is complete, P08-AC05, phase-wide P08-AC06, the Preview
portion of P08-SS01, and P08-SS04 remain blocked. This request does not change
the current Preview implementation or authorize a same-origin sandboxed
iframe.
