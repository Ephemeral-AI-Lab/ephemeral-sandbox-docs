# Web Console UI architecture decision amendment

| Field | Value |
|---|---|
| Status | Authorized implementation direction; engineering verification in progress |
| Authority | Active user-provided Web Console UI/UX implementation objective |
| Decision date | 2026-07-11 |
| Applies to | `ephemeral-sandbox/web/console` |
| Supersedes | `web-console-ui-tech-stack-and-library-options.md` only where that note prescribes Tailwind/Radix as the target UI architecture |
| Governing execution record | `web-console-mantine-migration-implementation-plan.md` |

## Decision

The EphemeralOS web console will migrate completely to Mantine 9.4.1 as its
sole application-wide component, theme, token, form, overlay, notification,
focus, and responsive-layout system. This is a finite migration, not a
permanent mixed architecture.

The final console has exactly one `MantineProvider` and one EphemeralOS light
theme. It removes every local Radix wrapper, direct Radix import, Radix
provider, Radix package, Tailwind utility style, `@theme` token, Tailwind
build integration, migration allowlist, and obsolete helper after parity is
proved.

## Retained boundaries

- React 19, React Router, and TanStack Query retain routing, URL state, server
  state, and polling ownership.
- TanStack Table is the headless state engine for operational tables; Mantine
  renders those tables.
- TanStack Virtual remains the performance engine for proven high-volume
  collections.
- CodeMirror, uPlot, and Lucide remain their respective rendering/icon
  engines; Mantine owns their surrounding application chrome.
- Local CSS Modules may express documented `minmax()` geometry, containment,
  and third-party integration using Mantine variables only.

## Dependency and accessibility boundary

The approved first-party runtime package set is `@mantine/core`,
`@mantine/hooks`, `@mantine/form`, and `@mantine/notifications`, pinned to one
exact version. Their ownership and compatibility must be reverified against
official Mantine documentation and the npm registry in P00 and P11.

React Aria Components are not approved at this point. They may be introduced
only after a recorded, reproducible Mantine parity failure shows a necessary
collection accessibility or scale gap; the exception needs package-ownership
verification, an explicit removal/retention decision, and Mantine-owned
visuals.

## Migration controls

1. P00 establishes the package/version matrix, correctness fixes, frozen
   fixtures, commands, evidence protocol, and temporary Tailwind allowlist.
2. Every later phase follows the ordered P00–P12 migration plan and must be
   buildable with its immutable evidence pack.
3. Preview isolation remains a security decision for P08B only. It does not
   authorize an unsafe iframe or block non-Preview migration work.
4. The canonical logo pixels must be copied from their validated source into a
   durable source/static input before generated `dist` is cleared; generated
   output is never imported at runtime.

## Historical record treatment

The earlier technology-options note remains an accurate snapshot of its former
recommendation. It is not rewritten. This amendment supersedes its conflicting
Tailwind/Radix end-state recommendation for this console and makes the Mantine
migration plan authoritative for implementation.
