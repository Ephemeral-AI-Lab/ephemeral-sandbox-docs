# Recovered design documents — provenance index

> **Cluster 01 — Workspace runtime & storage, supporting material.**
> These files were recovered verbatim from the `ephemeral-sandbox` git history on
> 2026-07-11. Each carries a one-line provenance header naming its original path and
> the commit that deleted it. **They are historical design records, not ground truth**:
> file paths and code anchors inside predate the current crate layout. Where a
> recovered document and shipped code disagree, the code wins; the cluster pages
> (`../0*.md`) carry the verified anchors.

## Why these exist

The code still cites its deleted specs — `§2.3`, `C1`–`C6`, `F1`/`F5`/`F10`,
`G1`–`G3`, `spec §13`, "spec decision" — but the documents those references resolve
into were removed from the repository (mostly by `0f7d02486`, 2026-07-11, *"chore:
remove obsolete docs and polish fleet cards"*). This folder restores the referents so
the cluster pages can quote them with provenance instead of paraphrasing from memory.

## The three specs the code actually cites

| File | Original path | What resolves into it |
|---|---|---|
| [`squash-spec.md`](squash-spec.md) | `docs/obsidian/ephemeral-os/implementation_plan/squash/spec.md` | **C1**–**C6**, **G1**–**G3**, the invariant list, the lock discipline — cited throughout layerstack/workspace/namespace-execution code. Page 08 is written against it. 1,420 lines; C1 sweep tree @756, C2 swimlanes @801, C3 staged switch @838, C4 /proc inspection map @905, C5 failure policy @942, C6 PTY physics @963. |
| [`finalize-policy-spec.md`](finalize-policy-spec.md) | `docs/obsidian/ephemeral-os/implementation_plan/finalize-policy/spec.md` | **§2.1–§2.7** and the **F-rules** — every `§2.3` (admission/completion protocol), `§2.4` (deleted/relocated), `§2.5` (failure semantics), `§2.6` (destroy-under-live-command exception), `§2.7` (known limits) and `F1`/`F5`/`F10` citation in the workspace-session and command code. Pages 04, 05 and 07 quote it. |
| [`occ-merge-publish-c3-spec.md`](occ-merge-publish-c3-spec.md) | `docs/occ_merge_publish/c3_spec.md` | The **"C3 spec"** cited by the file domain: `§7`/`§7.1` stores, `§9` attribution, `§10` event schema, `§11`/`§11.1` blame, `§13` resolver/merge/commit path. Page 06 quotes it. |

> **Numbering collision, stated once and loudly:** the file domain's "C3 spec
> §7/§9/§11/§13" citations (`operation/src/file/audit.rs:1`,
> `operation/src/file/service/store.rs:1`, `operation/src/file/service/impls/blame.rs:1`)
> refer to `occ-merge-publish-c3-spec.md` — **phase C3 of the OCC-merge-publish plan**
> — *not* to remount step **C3** (the staged switch) of `squash-spec.md`. Pages 06 and
> 08 restate this where the citations appear.

## Squash family (same folder as the main spec, same deleting commit)

| File | Lines | Content |
|---|---|---|
| [`squash-test-case.md`](squash-test-case.md) | 785 | E2E catalog source — the `E*`/`X*`/`B*`/`G*` test ids the live e2e mirror (`e2e/manager/management/squash/test_spec.md`) descends from. |
| [`squash-acceptance-criteria.md`](squash-acceptance-criteria.md) | 254 | Acceptance criteria for the squash/remount feature. |
| [`squash-impl-plan-tracker.md`](squash-impl-plan-tracker.md) | 940 | Implementation plan & progress tracker. |
| [`squash-iteration-report.md`](squash-iteration-report.md) | 1,354 | Iteration report. |
| [`squash-simplicity-review.md`](squash-simplicity-review.md) | 1,022 | Simplicity review results. |

## Remount rework series (why live remount exists in its current shape)

| File | Content |
|---|---|
| [`remount-rework-01-remount-removal.md`](remount-rework-01-remount-removal.md) | Removal of the previous remount mechanism. |
| [`remount-rework-02-remount-mechanism.md`](remount-rework-02-remount-mechanism.md) | The replacement mechanism design. |
| [`remount-rework-03-command-crate-removal.md`](remount-rework-03-command-crate-removal.md) | Removal of the old command crate. |

## Predecessor generation (historical context only)

| File | Original path | Note |
|---|---|---|
| [`predecessor-workspace-session-spec.md`](predecessor-workspace-session-spec.md) | `docs/daemon/workspace_migration/operation_service_workspace_session_SPEC.md` | Pre-finalize-policy session design (deleted earlier, by `2c1beb16c`). Does **not** contain the §2.x numbering the code cites — that is `finalize-policy-spec.md`. |
| [`predecessor-remount-structure-spec.md`](predecessor-remount-structure-spec.md) | `docs/daemon/workspace_migration/phase-operation_service_workspace_session/phase_3_workspace_session_remount_structure_SPEC.md` | Pre-rework remount structure (deleted by `2c1beb16c`). |

## Enumerated but not imported

The full `git log --diff-filter=D --name-only -- docs/` sweep (2026-07-11) also
surfaced, for other clusters' recovery if wanted:

- **Observability spec** → `docs/observability-rework/` (README, `crate-core-impl.md`,
  `layerstack-observability.md`, CLI examples) — cluster 07's concern.
- **OCC siblings** → `docs/occ_merge_publish/{README,c3_phase1_status,experiment,experiment_report}.md`.
- **File-operations family** → `docs/obsidian/ephemeral-os/implementation_plan/file_operations/`
  (spec, fix_spec, test-case, acceptance criteria, live smoke evidence) — the
  generation *before* the C3 spec for the file domain.
- **Oldest layerstack specs** (deleted by `4afcedc26`):
  `docs/layerstack-command-lease-live-remount_SPEC.md`,
  `docs/layerstack-leased-squash-gap-compaction_SPEC.md`,
  `docs/layerstack-squash-policy_SPEC.md`.
- `docs/daemon/squash_remount/live-run-remount-during-squash_IMPLEMENTATION_REPORT.md`.

Recovery command pattern:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
git log --diff-filter=D --format='%h %ad %s' --date=short -1 -- <path>   # find deleting commit
git show '<commit>^:<path>'                                              # read the content
```
