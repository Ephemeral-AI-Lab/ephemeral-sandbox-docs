# Agent prompt — Phase 00 (pass 2): close freeze-rules gaps

Copy everything below the line into a new agent session.

---

## Goal

**Continue Phase 00** for Ephemeral Sandbox State Storage V2. A first-pass
`SPEC.md` already exists. Your job is to **close PARTIAL gaps**, tighten
inventories from the clean worktree, and leave Phase 00 ready to hand off to
Phase 01 — still **docs only**.

Use the existing human docs and the prior SPEC as the contract.

**Do not** implement V2 product code.  
**Do not** choose architecture or storage algorithms.  
**Do not** claim performance winners.  
**Do not** silently close product DECs (`DEC-001`, `DEC-011`, `DEC-017`, `DEC-018`).  
**Do not** treat Stage 4.6 as a sealed V2 comparator.

---

## Authorized work

| Allowed | Forbidden |
|---------|-----------|
| Read clean product worktree and appendix docs | Edit product/Rust code |
| Edit files under `ephemeral-sandbox-v2/phases/00-freeze-rules/` | Live cutover, migrator, store rewrite |
| Update `SPEC.md` + supporting inventories | Closing open product decisions without owner input |
| Add small supporting files if needed (keep SPEC as index) | Architecture/algorithm winner claims |
| Update phase `PLAN.md` checkboxes / status | Gate/ownership/ceremony rewrite of the whole package |
| Link to appendix; quote sparingly | Using Stage 4.6 timings as V2 pass/fail |

---

## Paths (verify before trusting)

```text
Human docs package (edit here)
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2

Phase 00 folder
  .../ephemeral-sandbox-v2/phases/00-freeze-rules/

Already present (read first — do not rewrite from scratch)
  SPEC.md                         ← primary; update in place
  inventory-surfaces.md
  inventory-packages.md
  fixture-catalog.md
  PRD.md / PLAN.md / test-perf.md
  PROMPT.md                       ← original pass-1 prompt (context only)

Required reading (in order)
  .../ephemeral-sandbox-v2/README.md
  .../ephemeral-sandbox-v2/PRD.md
  .../ephemeral-sandbox-v2/PLAN.md
  .../phases/00-freeze-rules/SPEC.md          ← prior agent output
  .../phases/00-freeze-rules/test-perf.md     ← D1–D5 still apply
  .../phases/00-freeze-rules/inventory-*.md
  .../phases/00-freeze-rules/fixture-catalog.md

Clean implementation base (READ ONLY)
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
  expected branch: codex/new-2.0-storage-core
  recorded base:   e4974d1f9aac702b35e052629cb070c897989352

Optional appendix (READ ONLY)
  .../implementation-plan/new_2.0_migration_implementation_plan/
  .../implementation-plan/2.0 migration/   # Stage 4.6 history only
```

On start:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git status -sb
```

Re-seal env in SPEC §2 if anything drifted from `e497…`.  
If worktree missing/wrong → **stop** and report `BASE_DRIFT`.

Preserve unrelated dirty docs in the docs repo; do not `git clean` or reset.

---

## What prior pass already did

Treat as done unless you find factual errors:

- [x] Env seal (was clean match on `e497…`)  
- [x] Public catalog ops inventory (file / session / command / manager / internal)  
- [x] Primary durable writers (publish, amend, squash, base, auditability)  
- [x] Package map (R0 home = `sandbox-runtime-layerstack`)  
- [x] Open decisions register (all **open**)  
- [x] Fixture categories A–G  
- [x] Stage 4.6 historical / `INCOMPARABLE` policy  
- [x] Resource envelope **PROPOSAL**s  
- [x] Effort estimates  

---

## What you must finish (pass-2 backlog)

Prior SPEC §4.5 and inventory-surfaces §7 marked these **PARTIAL**. Close each
from **source** (`rg` / read code), or keep `PARTIAL` with a sharper gap note
(no invention).

### Priority 1 — close or tighten

| ID | Work | Where to put result |
|----|------|---------------------|
| G1 | **Publish reject / OCC matrix** — enumerate `PublishRejectReason` (and related amend/publish errors) with symbol + when it fires + product-facing error class if known | `inventory-surfaces.md` new section + SPEC §4 pointer |
| G2 | **Manager create/destroy disk layout** — paths written under host/workspace/layerstack roots for `create_sandbox` / `destroy_sandbox` (provider-docker + manager service) | `inventory-surfaces.md` or short `inventory-lifecycle-paths.md` |
| G3 | **Re-verify every durable writer** — `rg` for `publish_layer`, `publish_validated`, `amend_path`, `squash`, `ensure_workspace_base`, auditability append; confirm no missed production writers | Update writer table; mark COMPLETE or residual PARTIAL |
| G4 | **CLI / MCP surface delta** — which catalog ops are exposed; any name/flag mismatch vs catalog (catalog remains source of truth) | Short table in `inventory-surfaces.md` |

### Priority 2 — only if time

| ID | Work |
|----|------|
| G5 | Appendix “legacy 26-row” / DEC-017 matrix: locate in appendix if present; **link** only — do not invent a product decision |
| G6 | Observability field-level inventory for `layerstack` op (still non-authority) |
| G7 | Fixture catalog: add 1–2 concrete fixture **names** per category that map to existing tests under `crates/sandbox-runtime/layerstack/tests` or operation tests (paths only; do not implement) |
| G8 | Self-audit SPEC vs product PRD hard rules — fix contradictions only |

### Explicitly out of scope this pass

```text
NO store implementation
NO design winner (that is Phase 01)
NO V2 benchmarks as pass/fail
NO live cutover
NO closing DEC-001 / 011 / 017 / 018 without human owner
NO deletion of legacy data
NO rewrite of root ceremony package
```

---

## Deliverables

1. **Updated** `SPEC.md` (required)
   - Refresh §2 env seal  
   - Update §4.5 gaps: closed items removed or marked COMPLETE; residual PARTIAL only  
   - Keep §6 DECs **open** unless the user decides in-session  
   - Bump handoff §12 if inventories improved  

2. **Updated** supporting inventories as needed:
   - `inventory-surfaces.md` (primary place for G1–G4)
   - `inventory-packages.md` only if package facts were wrong
   - `fixture-catalog.md` only if G7 done

3. **Optional** new file if layout would bloat surfaces:
   ```text
   inventory-lifecycle-paths.md
   inventory-publish-rejects.md
   ```
   SPEC must link them.

4. **Update** phase `PLAN.md` status/checklist if still accurate.

5. **Do not** rewrite root `PRD.md` unless factual contradiction; note in SPEC instead.

---

## Process

1. Read prior `SPEC.md` end-to-end + `test-perf.md` D1–D5.  
2. Re-verify worktree identity.  
3. Work G1 → G4 from source (prefer measured tables).  
4. G5–G8 only if Priority 1 is solid.  
5. Self-check: D1–D5 still green; no winner language; no DEC closed by accident.  
6. Short final message: what closed, what remains PARTIAL, path to SPEC.

---

## Definition of done (pass 2)

- [ ] Env seal still accurate (or drift documented)  
- [ ] G1 publish-reject / OCC matrix present from source  
- [ ] G2 create/destroy path inventory present or explicit PARTIAL with file anchors  
- [ ] G3 writer list re-verified  
- [ ] G4 CLI/MCP vs catalog delta noted  
- [ ] SPEC §4.5 reflects new completeness  
- [ ] DECs still open (unless human closed them)  
- [ ] Stage 4.6 still historical only  
- [ ] No product code changes  
- [ ] No architecture/algorithm winner  

---

## Style

- Plain English; tables over essays  
- Paths and command outputs in fences  
- Mark uncertainty `OPEN` / `PARTIAL` / `PROPOSAL`  
- Prefer editing existing files over sprawl  
- Do not restate entire SPEC; patch and add sections  

---

## Effort band (planning)

| Session | Outcome |
|---------|---------|
| S0d | G1 + G3 (reject matrix + writer re-verify) |
| S0e | G2 + G4 (lifecycle paths + CLI/MCP delta) |
| S0f | SPEC polish, residual PARTIAL list, handoff note |

Estimate: **~3–6 person-hours** if focused on Priority 1 only.

---

## When finished, point the user at

```text
ephemeral-sandbox-v2/phases/00-freeze-rules/SPEC.md
```

and list any remaining `PARTIAL` items in one short table.
