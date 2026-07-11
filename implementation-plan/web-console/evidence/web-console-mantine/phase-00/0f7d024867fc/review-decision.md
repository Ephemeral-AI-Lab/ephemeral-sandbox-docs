# P00 Review and Preview-Isolation Decision Record

Status: P00 test boundary recorded; P08B security approval remains pending. This
record is evidence of the current boundary and a review template; it is not an
approval or an architecture decision.

## Observed Preview boundary

- The console builds Preview URLs as same-origin relative paths in `web/console/src/pages/sandbox/preview/PreviewTab.tsx`: `/s/{sandboxId}/{scope}/{port}/{path}`.
- The Preview iframe has no `sandbox` attribute. The console reads its `contentWindow.location` when synchronizing navigation, which is possible only because the current Preview is same-origin.
- The console backend routes `/s/*` to the general proxy in `crates/sandbox-console/src/router.rs`. `crates/sandbox-console/src/proxy.rs` forwards methods, headers, query strings, streamed bodies, WebSocket upgrades, and response headers, but does not establish a separate origin or response-isolation policy.

This means an application served in Preview currently shares the console origin
and is not constrained by iframe sandboxing. P08B is the only phase that may
change this boundary. The authorized amendment expressly permits P00 and all
non-Preview migration work to proceed while P08B approval is pending; Preview
controls/status are not migrated before security sign-off on the chosen
boundary.

## P00 boundary and P08B authority

P00 records the test boundary below. The implementation plan assigns the
security-reviewer role to D02; a named person and an approved policy are
required before P08B, not before non-Preview work.

| Responsibility | Authority | Required decision |
| --- | --- | --- |
| Preview-isolation decision owner | Security reviewer (D02; appointment pending) | Select the approved isolation approach and its product constraints before P08B. |
| Security sign-off authority | Security reviewer (D02; appointment pending) | Approve the threat model and test boundary before P08B. |
| P00 test boundary | This record | Preserve the minimum checks below in the P08B acceptance suite. |

## Decision options to review

The appointed decision owner and security authority must choose one of these
approaches, record the rationale, and assign the corresponding P08B acceptance
tests. This record does not choose between them.

1. **Dedicated untrusted Preview origin.** Serve Preview content from a distinct origin with no ambient console credentials or same-origin access. P08B must specify the host-routing, authentication/session scope, CSP, and allowed embed behavior.
2. **Sandboxed Preview iframe.** Use an iframe sandbox that does not preserve the console origin, granting only the permissions required by the approved Preview use cases. P08B must document the required permissions, any expected breakage, navigation behavior, and the interaction with the proxy.

## Minimum P08B verification boundary

- A Preview document cannot read console DOM, storage, or `contentWindow` state as a same-origin peer.
- A Preview document cannot make authenticated console API/RPC requests using ambient console credentials.
- Navigation, popups, forms, downloads, and permissions follow the approved policy; disallowed behavior is blocked by a browser test.
- Preview application assets, WebSockets, and approved navigation continue to work under the selected boundary.
- The browser suite contains one positive and one negative test for every permission explicitly granted to Preview.

## P00 screenshot-pack review

SS01–SS03 are available through [the evidence index](index.md). The
fixture-scoped Codex review is recorded below; a later external design,
engineering, accessibility, or security reviewer may supersede it with a named
decision, UTC timestamp, and notes. The missing P08B decision does not block
non-Preview migration.

## P00 fixture-evidence decision

At `2026-07-11T09:11:53Z`, Codex reviewed the P00 fixture-only pack and
approved it for its limited evidence purpose:

- **Design coverage:** SS01 records every planned route/viewport as a
  pre-migration baseline; SS02 and SS03 are intentionally disposable fixtures,
  not proposed final designs.
- **Engineering:** Node 24.14.0 re-runs passed `npm run test` (13 files, 22
  tests), `npm run build`, and `npm run test:e2e` (42 browser tests).
- **Accessibility:** the browser suite passed its zero-Axe scan and its real
  keyboard, portal, and focus assertions.
- **Security:** screenshots use only sanitized deterministic fixture data; this
  is not a Preview-isolation approval.

This P00 review is an evidence decision by the active implementation agent,
not an external security authorization. Preview isolation remains an explicit
P08B decision.
