# P08A approved Files evidence — P08B remains blocked

This immutable pack is captured from console revision `f1073cd29` (the Files
implementation begins at `39fd78c25`). It approves **P08A Files only**:
virtualized file navigation, breadcrumbs and scope controls, a stable
CodeMirror editor, paging, edit/conflict state, blame controls, and narrow
Drawers. It does not approve P08 as a whole and it does not change Preview.

## What passed

- `npx playwright test tests/browser/P08FilesFixture.spec.ts`: 11 Files
  browser checks passed. They cover Files at 375x812, 768x1024, 1024x768, and
  1440x900; virtual-tree roles and keyboard behavior; the explicit API
  first-2,000-entry label; CodeMirror identity through paging/blame/conflict;
  local-draft preservation; narrow Drawer focus restoration; and Axe.
- `npx vitest run tests/trust/FileView.test.tsx`: the FileView conflict
  contract passed.
- `npm run build`: TypeScript and the Vite production build passed. Vite
  emitted only its existing bundle-size advisory.

The tree is a lazy flat composition backed by TanStack Virtual. It uses tree
roles, roving focus, Arrow/Home/End, expansion, and typeahead without mounting
the 2,000-entry response at once. The root label states that the API returned
only its first 2,000 entries. FileView retains a selected-file CodeMirror
instance: loading another page dispatches an append transaction, while
line-number, editability, and blame changes use CodeMirror compartments rather
than reconstructing the editor. Its direct CodeMirror scroller is the editor
pane's only scroll owner.

## P08B blocker

No Preview control, iframe, origin, sandbox, CSP, or proxy behavior changed in
this revision. Decision D02 remains open: a named security reviewer must select
and approve a dedicated untrusted Preview origin and sandbox/CSP boundary, then
define positive and negative origin/escape tests. The current same-origin,
unsandboxed Preview is prohibited by the implementation plan, and Mantine is
not an isolation control. Consequently P08-AC05, P08-AC06, P08-SS01 as a full
Files-and-Preview capture, and P08-SS04 remain incomplete.

## Immutable screenshot triads

The committed Files snapshots below are the approved P08A reference. Same
commit actual captures are byte-identical; ImageMagick `compare -metric AE`
reported `0 (0)` for each of the nine pairs. The
[manifest.json](manifest.json) records hashes, commands, coverage, and the
P08B block.

| Requirement | Capture | Reference / actual / diff |
|---|---|---|
| P08A portion of SS01 | Files normal state at 375x812, 768x1024, 1024x768, and 1440x900 | [reference](reference/) / [actual](actual/) / [diff](diff/) |
| P08-SS02 | Expanded desktop tree with blame; narrow navigator and blame Drawers | [desktop](reference/p08-files-tree-blame-1440x900-darwin.png) / [navigator](reference/p08-files-navigator-drawer-375x812-darwin.png) / [blame](reference/p08-files-blame-drawer-375x812-darwin.png) |
| P08-SS03 | End of a 4,000-line paged file with CodeMirror selection; explicit preserved local-draft conflict | [paging](reference/p08-files-paged-1440x900-darwin.png) / [selection](reference/p08-files-paged-selection-1440x900-darwin.png) / [conflict](reference/p08-files-conflict-1440x900-darwin.png) |
| P08-SS04 | Preview loading/blocked/error/success under an approved isolation design | **Blocked pending D02; no artifact may be substituted.** |

## Review decision

At `2026-07-11T19:34:00+08:00`, Codex self-reviewed the committed P08A Files
scope, the responsive/interactive/large-file captures, and the recorded
automated evidence. P08A is approved for the Files boundary. This is an
implementation-agent self-review, not external human design, engineering,
accessibility, or security approval. P08 remains blocked at P08B until the
named D02 security owner supplies the approved Preview isolation policy and
its required tests and evidence.
