# Phase 00 — Fixture catalog (plan only)

> Historical terminology: “state id” below maps to current `VersionId` under
> [ADR-002](../../design/decisions/ADR-002-version-id-naming.md). This catalog
> remains frozen evidence rather than an implementation naming contract.

**Status:** planning catalog for later phases; existing source anchors mapped — **no fixtures implemented here**  
Parent: [SPEC.md](SPEC.md)

Implement fixtures when the named phase owns the code under test. Prefer
recovering bytes from real product tests or attested corpora; do not invent
“pass” numbers in this phase.

---

## Categories and example scenarios

### A. Happy path publish / read / session

| # | Scenario | Later phase |
|---|----------|-------------|
| A1 | Create session → write files in session → publish → `file_read` without session sees published content | 03–04, prove 06 |
| A2 | `file_read` with session sees live generation before publish | 04 |
| A3 | `exec_command` without session auto-publishes then destroys (`publish_then_destroy`) | 04, 06 |
| A4 | Sessionless `file_write` / `file_edit` (today: one layer publish) — **behavior depends on DEC-017** | 04 (after DEC) |
| A5 | Destroy session without publish discards upperdir changes | 04, 06 |

### B. Corrupt / invalid input

| # | Scenario | Later phase |
|---|----------|-------------|
| B1 | Truncated / invalid manifest or index mid-tree | 03, 06 |
| B2 | Layer / payload object missing while referenced | 03, 06 |
| B3 | Invalid path / non-UTF-8 / oversize edit (`max_edit_bytes`) | 04 |
| B4 | Malformed publish changeset / whiteout abuse | 03–04 |
| B5 | `file_edit` non-unique `old_string` without `replace_all` | 04 |

### C. Crash mid-publish / mid-import

| # | Scenario | Later phase |
|---|----------|-------------|
| C1 | Kill process after staging payload, before head commit | 03, 06 |
| C2 | Kill after head write, before reader-visible readiness | 03, 06 |
| C3 | Host crash / power-loss class (if durable model claims it) — keep distinct from process kill | 03, 06 |
| C4 | Crash mid-legacy import / migrator | 05–06 |
| C5 | Crash mid-squash / compact | 03, 06 |

### D. Concurrent OCC / fork

| # | Scenario | Later phase |
|---|----------|-------------|
| D1 | Two publishes race on same head; loser fails cleanly (no silent merge) | 03–04, 06 |
| D2 | Publish while readers hold snapshot leases | 03–04 |
| D3 | Reference fork / checkpoint / rollback-to-existing: **zero** immutable payload copy when same accepted state | 02–04, 06 |
| D4 | Stale base revision publish rejected (`PublishReject` / OCC) | 03–04 |

### E. Migration / legacy shape

| # | Scenario | Later phase |
|---|----------|-------------|
| E1 | Import multi-layer LayerStack with base + N published layers | 05–06 |
| E2 | Import after squash-compacted chain | 05–06 |
| E3 | Import empty / base-only sandbox | 05–06 |
| E4 | Reject dual-writable (legacy write after cutover fence) | 05–07 |
| E5 | Writer generation fence: old binary cannot write after generation bump | 05–07 |

### F. COW: multiple accepted references to one Version (payload must not copy)

| # | Scenario | Later phase |
|---|----------|-------------|
| F1 | Checkpoint root points at existing accepted state; payload bytes read=write=copy=0 for immutable store | 02–03, 06 |
| F2 | Fork creates another Branch Head → same `VersionId`; two accepted references, one physical payload | 02–03, 06 |
| F3 | Rollback-to-existing accepted state; no new private payload | 02–03, 06 |
| F4 | N Heads/fixed Roots (≥3) share one payload; removing one reference does not delete payload while others remain | 03, 06 |

### G. Collision: same id, different bytes

| # | Scenario | Later phase |
|---|----------|-------------|
| G1 | Candidate claims state id already taken; full canonical bytes differ → fail closed | 02–03, 06 |
| G2 | Same id, equal canonical bytes → admit / share (no silent wrong alias of unequal bytes) | 02–03 |
| G3 | Forced-collision qualification seam (test-only) if Phase 01 requires it | 02–03, 06 |

---

## Existing e497 test anchors (inputs, not V2 oracles)

These tests are concrete places to recover setup code, bytes, and legacy shapes
when the owning phase implements the fixtures. A matching category does **not**
mean the existing test proves the V2 rule; the final column calls out the gap.

| Category | Existing test anchors (1–2) | What can be reused / what is still missing |
|----------|-------------------------------|-------------------------------------------|
| A — happy path | `crates/sandbox-runtime/operation/tests/layerstack_publish.rs::implicit_session_completion_publishes_captured_changes_before_destroy`; `crates/sandbox-runtime/operation/tests/file_operations.rs::sessionless_write_create_then_update_with_blame` | Reuse session capture/publish/read and current no-session amend setup. DEC-017 still controls whether the latter remains a V2 product path. |
| B — corrupt/invalid | `crates/sandbox-runtime/layerstack/tests/stack.rs::ensure_workspace_base_rejects_too_new_manifest_schema`; `crates/sandbox-runtime/layerstack/tests/unit/publish.rs::protected_paths_reject` | Reuse malformed manifest and reserved-path inputs. V2 canonical object/index corruption must be added against the selected store. |
| C — crash | `crates/sandbox-runtime/operation/tests/workspace_session_publish.rs::storage_failure_keeps_revision_and_session_then_retry_commits_once`; `crates/sandbox-runtime/layerstack/tests/unit/squash.rs::crash_and_error_paths_around_commit` | Reuse pre/post-commit assertions and retry shapes. Process-kill, host-crash, V2 import, and exact durability cuts remain new fixtures. |
| D — OCC/fork | `crates/sandbox-runtime/layerstack/tests/unit/publish.rs::source_occ_conflict_rejects_without_publishing_ignored_changes`; `crates/sandbox-runtime/layerstack/tests/unit/publish.rs::stale_delete_conflicts_with_concurrently_created_directory` | Reuse stale-base fingerprints and no-partial-publication assertions. Current code can also auto-merge eligible text conflicts; V2 D1 must instead enforce the hard-rule loser outcome with no silent merge/rebase. Fork/reference-only counters are new. |
| E — legacy migration | `crates/sandbox-runtime/layerstack/tests/unit/export_delta.rs::fold_matches_merged_view_over_the_delta_manifest`; `crates/sandbox-runtime/layerstack/tests/unit/export_delta.rs::fold_agrees_with_flatten_on_winner_selection` | Reuse multi-layer, whiteout, opaque, and newest-wins legacy trees. The V2 migrator/import receipt and writer-generation fence remain new. |
| F — COW/reference sharing | `crates/sandbox-runtime/layerstack/tests/unit/observe.rs::observe_reports_leased_and_booked_layers_over_l0_to_l4`; `crates/sandbox-runtime/layerstack/tests/unit/squash.rs::old_layers_not_deleted_until_refcount_zero` | Reuse multi-reader reachability and last-reference setup ideas only. Neither test proves complete-state payload sharing or zero payload I/O; F1–F4 require new V2 counters/oracles. |
| G — identity/collision | `crates/sandbox-runtime/layerstack/tests/cas_fixtures.rs::all_cas_fixtures_match` with `tests/fixtures/cas/cases.json`; `crates/sandbox-runtime/layerstack/tests/unit/publish.rs::digest_deduped_publish_reports_no_op` | Reuse canonical hashing golden bytes and current equal-digest no-op setup. There is no current forced same-id/different-bytes full-compare oracle; G1–G3 must add it and fail closed. |

Only paths and test names are frozen here. Later phases own any copied fixture,
new fault seam, counter, canonical byte format, or pass/fail assertion.

---

## Oracle / measurement notes (not pass criteria yet)

- **Correctness first:** crash and collision fixtures fail closed; never “fast wrong.”
- **COW proof:** measure payload I/O or equivalent store counters on reference-only
  root ops; digest equality alone is **not** proof (product hard rule 4).
- **Stage 4.6:** may supply **fixture ideas** only after re-hash/recover; timings
  are **not** oracles for V2 pass/fail (see SPEC §8).
- **Holdout:** if a fixture corpus is reserved for final proof, mark it and do
  **not** tune store code against it before Phase 06.

---

## Mapping to phases (summary)

| Phase | Fixture classes primarily owned |
|------:|---------------------------------|
| 02 State identity | G, F (identity/equality), partial D |
| 03 State store | A (store-level), B, C, D, F, G |
| 04 Wire product | A, B product paths, D product OCC |
| 05 Migrator | E |
| 06 Prove offline | Full matrix re-run on ship candidate |
| 07 Go live | E4–E5 live observation; not new unit fixtures |
| 08 Clean release | Re-prove without migrator code |

---

Parent: [SPEC.md](SPEC.md)
