# Agent prompt — Phase 00: write the freeze-rules **spec**

Copy everything below the line into a new agent session.

---

## Goal

Produce a **Phase 00 specification** for Ephemeral Sandbox State Storage V2: concrete
inventories, fixture plan, open decisions, baseline/perf policy, and **effort
estimates** for this phase and a rough rollup for later phases.

Use the existing human docs as the contract. **Do not** implement V2 product code.
**Do not** choose architecture or storage algorithms. **Do not** claim performance winners.

---

## Authorized work

| Allowed | Forbidden |
|---------|-----------|
| Read clean product worktree and appendix docs | Edit product/Rust code (except you may not) |
| Write/update files under `ephemeral-sandbox-v2/phases/00-freeze-rules/` | Live cutover, migrator, store rewrite |
| Add `SPEC.md` (required deliverable) and small supporting inventories | Closing open product decisions without owner input |
| Update phase `PLAN.md` checkboxes / status when done | Treating Stage 4.6 as a V2 guarantee |
| Link to appendix; quote sparingly | Gate/ownership/ceremony rewrite of the whole package |

---

## Paths (verify before trusting)

```text
Human docs package (edit here)
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2

Phase 00 folder
  .../ephemeral-sandbox-v2/phases/00-freeze-rules/

Required reading (in order)
  .../ephemeral-sandbox-v2/README.md
  .../ephemeral-sandbox-v2/PRD.md
  .../ephemeral-sandbox-v2/PLAN.md
  .../ephemeral-sandbox-v2/phases/00-freeze-rules/PRD.md
  .../ephemeral-sandbox-v2/phases/00-freeze-rules/PLAN.md
  .../ephemeral-sandbox-v2/phases/00-freeze-rules/test-perf.md

Clean implementation base (READ ONLY)
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
  expected branch: codex/new-2.0-storage-core
  recorded base:   e4974d1f9aac702b35e052629cb070c897989352

Optional appendix (READ ONLY, for detail)
  .../implementation-plan/new_2.0_migration_implementation_plan/
  .../implementation-plan/2.0 migration/   # Stage 4.6 history
```

On start:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git status -sb
```

Record path, branch, HEAD, dirty state, and any drift from `e497…` in the spec.
If the worktree is missing or wrong, **stop** and report `BASE_DRIFT` / missing tree.

Preserve unrelated dirty docs in the docs repo; do not `git clean` or reset.

---

## What to produce

### Primary deliverable (required)

Create:

```text
ephemeral-sandbox-v2/phases/00-freeze-rules/SPEC.md
```

Human-readable. Prefer tables and checklists. No gate/epoch/acceptor jargon.

### `SPEC.md` required sections

#### 1. Summary
- One paragraph: what Phase 00 freezes and what it deliberately leaves open.
- Exit status target: how this spec satisfies `test-perf.md` D1–D5.

#### 2. Environment seal
| Field | Value |
|-------|--------|
| Docs package path | |
| Worktree path | |
| Branch | |
| HEAD | |
| Dirty? | |
| Matches recorded e497 base? | yes/no + notes |

#### 3. Product rules (pointer + deltas)
- Link product `PRD.md` hard rules.
- List any **clarifications** discovered from source (not new architecture).

#### 4. Surface inventory (from source)
From the clean worktree, inventory (as complete as practical in this pass):

| Class | What to list |
|-------|----------------|
| Runtime/manager ops touching state or workspace | names + crate/module hints |
| File API ops | `file_*`, session publish/create/destroy, blame if present |
| Durable state writers | who can change LayerStack / heads / publish |
| Workspace / overlay / exec owners | package paths |
| Observability names that look storage-like | e.g. layerstack diagnostics — note non-authority |

Use source search (`rg`, catalog modules). Prefer measured lists over memory.
If incomplete, mark `PARTIAL` and list gaps (do not invent).

#### 5. Package / module map (today)
Table: package or directory → role (store history, workspace, app, other) → relevance to V2.

#### 6. Open decisions register
Start from product PRD (`DEC-001`, `DEC-011`, `DEC-017`, `DEC-018`, design opens).
For each:

| ID | Question | Blocks which later phase? | Status | Notes from source |
|----|----------|---------------------------|--------|-------------------|

Do **not** resolve DECs unless the user explicitly decides in-session; record `open`.

#### 7. Fixture plan (for later phases)
Categories with 2–5 example scenarios each:

- Happy path publish / read / session  
- Corrupt / invalid input  
- Crash mid-publish / mid-import  
- Concurrent OCC / fork  
- Migration / legacy shape  
- COW: multi-root same state (payload must not copy)  
- Collision: same id, different bytes  

State which **later phase** should implement each class (02–06 etc.).

#### 8. Baseline and performance policy
- Stage 4.6: historical only; note prior candidate slower than control if citing numbers.
- Label: **not** a sealed V2 comparator until re-run with full provenance.
- What Phase 00 freezes: “how we will measure later,” not V2 results.
- No 100× claim.

#### 9. Resource envelope **proposals**
Propose (mark `PROPOSAL`, not measured V2 fact):

- Store-side memory / FD / disk scratch thinking  
- Untrusted runtime cgroup-style bounds (pointer only)  
- Cleanup expectations (no unbounded caches)

#### 10. Effort estimation

Provide **two layers** of estimate.

**A. This Phase 00 task (writing the spec)**

| Workstream | Estimate (person-hours) | Confidence | Notes |
|------------|------------------------:|------------|-------|
| Env verify + tree skim | 0.5–1 | high | |
| Ops / file API inventory | 2–4 | medium | depends on catalog clarity |
| Writer / package map | 2–4 | medium | |
| Open decisions + appendix skim | 1–2 | high | |
| Fixture + baseline + resources writeup | 1–2 | high | |
| SPEC polish + self-check vs test-perf | 1 | high | |
| **Total Phase 00 spec** | **~8–14 h** | medium | single focused agent pass may land ~6–10 h if inventory is partial |

Break into **agent session sizes** (assume ~2–4 h focused sessions):

| Session | Outcome |
|---------|---------|
| S0a | Env seal + package map draft |
| S0b | Full surface + writer inventory |
| S0c | Fixtures, baseline, DECs, effort rollup; SPEC complete |

**B. Rough rollup after Phase 00 (planning only, not commitment)**

| Phase | Name | Effort band | Notes |
|------:|------|-------------|-------|
| 00 | Freeze rules (this spec) | S | docs |
| 01 | Choose design | S–M | decision + light spikes |
| 02 | State identity | S–M | pure code + tests |
| 03 | State store | **L–XL** | main engineering |
| 04 | Wire product | M–L | integration |
| 05 | Migrator | M | temp code |
| 06 | Prove offline | M–L | test time |
| 07 | Go live | M + calendar | observation window |
| 08 | Clean release | M | delete + requal |

Bands: **S** ~1–3 d · **M** ~3–8 d · **L** ~1–3 w · **XL** multi-week (calendar, one engineer-equivalent; AI-assisted can compress wall time but not zero review).

State assumptions (one engineer + AI, clean worktree, R0-first, no live fleet surprises).

#### 11. Stop conditions and risks
- What would block finishing Phase 00  
- What must not start until SPEC passes Phase 00 test-perf  

#### 12. Handoff to Phase 01
Bullet list: exact files to read; what Phase 01 may assume frozen; what remains open.

---

## Optional supporting files (same folder)

If `SPEC.md` gets long, split:

```text
inventory-surfaces.md
inventory-packages.md
fixture-catalog.md
```

`SPEC.md` must still index them with links.

---

## Process

1. Read required human docs (full).  
2. Verify worktree; record identity.  
3. Inventory from source (rg / read catalogs).  
4. Skim appendix only where needed for Stage 4.6 or decision IDs.  
5. Write `SPEC.md` (and optional splits).  
6. Self-check against `test-perf.md` D1–D5; fix gaps.  
7. Update `PLAN.md` checkboxes and status if accurate.  
8. Short final message: path to SPEC, hours spent vs estimate, gaps left `PARTIAL`.  

Do **not** edit root `PRD.md` / `PLAN.md` unless you find a factual contradiction; prefer notes in SPEC.

---

## Definition of done (Phase 00 agent task)

- [ ] `SPEC.md` exists with all required sections  
- [ ] Env seal filled from real git  
- [ ] Surface + package inventories from source (or explicit PARTIAL + gaps)  
- [ ] Open decisions not silently closed  
- [ ] Fixture plan + baseline policy + resource proposals present  
- [ ] Effort estimates for Phase 00 sessions + rough later-phase rollup  
- [ ] `test-perf.md` D1–D5 satisfiable  
- [ ] No product code changes  
- [ ] No architecture/algorithm winner declared  

---

## Style

- Plain English; tables over essays  
- Paths and command outputs in fences  
- Mark uncertainty `OPEN` / `PARTIAL` / `PROPOSAL`  
- Diagrams optional (Mermaid) if they clarify inventory  

---

## Out of scope reminder

```text
NO store implementation
NO design winner
NO V2 benchmarks as pass/fail
NO live cutover
NO deletion of legacy data
```

When finished, point the user at:

```text
ephemeral-sandbox-v2/phases/00-freeze-rules/SPEC.md
```
