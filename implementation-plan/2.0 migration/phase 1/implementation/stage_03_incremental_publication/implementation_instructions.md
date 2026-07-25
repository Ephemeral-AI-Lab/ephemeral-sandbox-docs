# Stage 03 implementation instructions — corrected identity and complete private publication

> **Instruction status:** Stage 03 implementation and mandatory evidence are
> complete; final verdict is **POC PASS**.
>
> **Closure:** `S03-G01–S03-G10`, `S03-I01–S03-I11`, `S03-E01–S03-E08`,
> `S03-B01`, `S03-D01`, `S03-L01`, `S03-R01`, `S03-A01`, `S03-DOC01`, and
> `S03-H01` are `PASS`. The approved
> [`PRC-STAGE03-OWNER-DECISION-G01.1`](contract_v3_owner_decision_g01_1.md) and
> immutable [`stage03_v3_owner_corpus_v1.json`](stage03_v3_owner_corpus_v1.json)
> freeze the complete v3 wire contract and corpus. See the final
> [Stage 04 handoff](handoff_to_stage_04.md), final
> [benchmark note](benchmark_note.md), and
> [dependency/portability audit](stage03_dependency_portability_audit_20260725.md).
>
> This document remains the canonical execution guide and tracker. It does not
> amend the approved format or grant later-stage authority. Retained Stage 00–02
> evidence remains valid only for the claims made by those stages.

## 0. Source status and reconciliation

### 0.1 Authority order

Apply these sources in this order. A future implementation agent must stop and
reconcile any conflict instead of weakening the higher source:

1. recorded owner decisions, including a Stage 03 v3 amendment approved after this
   guide;
2. the Phase 1 [implementation index](../index.md) and
   [minimal storage contract](../layerstack_storage_contract.md);
3. the Stage 03 [specification](spec.md);
4. the Stage 03 [E2E plan](e2e_test.md);
5. [Preparation 04 quantitative acceptance criteria](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md);
6. the Stage 03 [benchmark note](benchmark_note.md);
7. the completed Stage 02
   [handoff to Stage 03](../stage_02_portable_root_contract/handoff_to_stage_03.md)
   and inherited evidence;
8. current repository-local instructions and actual product, test, and benchmark seams;
9. this implementation guide.

### 0.2 Reading ledger

“Read” means inspected from the first line through EOF during authoring. “Missing”
means the requested path was checked and did not exist; it is not represented as read.

| Source | Live status | Authority contributed | EOF status |
| --- | --- | --- | --- |
| [`spec.md`](spec.md) | Present; status says specification only and blocked on the v3 amendment | Stage outcome, entry conditions, identity exclusions, publication/ref/recovery protocol, complexity, exit criteria | Read through EOF |
| [`e2e_test.md`](e2e_test.md) | Present; `NOT_RUN` | Mandatory correctness, failpoint, resource, exposure, and exit-evidence cases | Read through EOF |
| [`benchmark_note.md`](benchmark_note.md) | Present; initial `NOT_RUN` history plus final bounded POC result | Required Stage 03 benchmark cells, final campaign identity, honest sample sufficiency and report fields | Read through EOF before implementation; final result appended at closure |
| `stage_03_incremental_publication/handoff_from_stage_02.md` | **Missing from the current branch**; retained at `origin/layerstack_2_0` | Historical architecture/specification handoff; it repeats the v3 owner blocker and grants no implementation authority | Current absence and retained remote-ref contents verified |
| [`../index.md`](../index.md) | Present | Stage DAG, invariants, authority boundary, physical accounting, stage ownership | Read through EOF |
| [`../layerstack_storage_contract.md`](../layerstack_storage_contract.md) | Present and locally modified before this guide was written | Canonical `/eos` layout, record ownership, atomicity, lifetime, allowed and forbidden paths | Read through EOF, including the live dirty change |
| [`../../index.md`](../../index.md) | Present | Phase-level intent and links | Read through EOF |
| [`../../prep/01-cdc-cas-space-time-materialization-spec.md`](../../prep/01-cdc-cas-space-time-materialization-spec.md) | Present | Original workload, storage, identity, and materialization problem statement | Read through EOF |
| [`../../prep/02-storage-solution-examination-review.md`](../../prep/02-storage-solution-examination-review.md) | Present | Reviewed alternatives and rejected designs | Read through EOF |
| [`../../prep/03-seqcdc-cas-and-squash-decision.md`](../../prep/03-seqcdc-cas-and-squash-decision.md) | Present | Selected scalar SeqCDC semantics/profile and CAS/squash direction | Read through EOF |
| [`../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md`](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md) | Present | Quantitative resource, locality, concurrency, latency, and qualification gates | Read through EOF |
| [`../stage_02_portable_root_contract/spec.md`](../stage_02_portable_root_contract/spec.md) | Present; Stage 02 contract | Immutable v2 identity/codec boundary and v1 authority constraint | Read through EOF |
| [`../stage_02_portable_root_contract/e2e_test.md`](../stage_02_portable_root_contract/e2e_test.md) | Present; contains retained Stage 02 results | PRC evidence and artifact contract | Read through EOF |
| [`../stage_02_portable_root_contract/implementation_instructions.md`](../stage_02_portable_root_contract/implementation_instructions.md) | Present | Structural baseline, live command patterns, dependency comparator and reporting rules | Read through EOF |
| [`../stage_02_portable_root_contract/contract_v2_owner_decision_d2_5.md`](../stage_02_portable_root_contract/contract_v2_owner_decision_d2_5.md) | Present; approved for v2 only | `PRC-STAGE02-OWNER-DECISION-D2.5`; explicitly not v3 approval | Read through EOF |
| [`../stage_02_portable_root_contract/handoff_to_stage_03.md`](../stage_02_portable_root_contract/handoff_to_stage_03.md) | Present; actual completed handoff | Live Stage 02 artifacts, custody at handoff, and explicit v3 owner blocker | Read through EOF |
| [`contract_v3_owner_decision_g01_1.md`](contract_v3_owner_decision_g01_1.md) | Present; approved on 2026-07-25 | `PRC-STAGE03-OWNER-DECISION-G01.1`; complete v3 framing, records, identities, bounds, errors, compatibility and corpus freeze | Read through EOF |
| [`stage03_v3_owner_corpus_v1.json`](stage03_v3_owner_corpus_v1.json) | Present; immutable manifest SHA-256 `7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be` | Fourteen exact byte/ID goldens plus qualification, focused and hostile corpus inventory | Parsed and every golden length/digest independently verified |
| [`gate_resolution_approval_20260725_04.md`](gate_resolution_approval_20260725_04.md) | Present; `PASS` | User approval mapping and complete §5.2 non-drift closure audit | Read through EOF |
| [`stage03_dependency_portability_audit_20260725.md`](stage03_dependency_portability_audit_20260725.md) | Present; `PASS` | Final exact dependency, helper/service/image/network and portable-core closure | Created from retained final evidence |
| [`handoff_to_stage_04.md`](handoff_to_stage_04.md) | Present; `POC PASS` | Final custody, implementation, verification, cleanup, deferral and Stage 04 boundary | Created at closure |
| Product `AGENTS.md`, `CLAUDE.md`, `docs/maintainer-architecture.md` | Present | Repository working rules and core → LayerStack → workspace/provider dependency boundary | Read through EOF |
| Test/docs ancestry instructions | No `AGENTS.md` or `CLAUDE.md` found below their repository roots | No additional local override | Search completed |
| Test `e2e/test-report.md` and benchmark `README.md` | Present | Append-only execution record; one scheduler/runner and run-state ownership | Relevant report history inspected; benchmark README read through EOF |

The Stage 00/01 stable contracts are inherited through the implementation index,
Stage 02 instructions, and Stage 02 handoff. Before implementation begins, the agent
must also re-read any source above that changed after the custody snapshot in §0.4.

### 0.3 Owner-decision status

`PRC-STAGE03-OWNER-DECISION-G01.1` is the current approved Stage 03 decision. It
freezes every record and identity listed in §5.2, numeric record and digest domains,
canonical encoding and ordering, all maximum bounds and typed errors, v2
coexistence/import, and the immutable corpus manifest with SHA-256
`7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be`.
The approval and spec-conformance audit are retained in
[`gate_resolution_approval_20260725_04.md`](gate_resolution_approval_20260725_04.md),
SHA-256 `49ea0a740462ce2652d5a4c4f21f595a44a56af25c0b7222dff3149a63a5f849`.

Therefore `S03-G01` is `PASS`. D2.5 remains immutable and v2-only; the new decision
adds a side-by-side v3 contract and grants no authority to alter public v1 behavior
or pull Stage 04–07 work into Stage 03.

### 0.4 Live repository custody at authoring time

Captured on 2026-07-25 in shared worktrees. Re-run the exact custody commands before
future work and record any drift; do not reset, stash, clean, restore, switch branches,
or overwrite another owner’s changes.

| Area | Repository/branch | `HEAD` and upstream | Complete live worktree custody |
| --- | --- | --- | --- |
| Product | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`, `upgrade-2.0-phase-1` | `cbe45de873cd24fbf48bb7b3a6c5f9f98980313c`; `origin/upgrade-2.0-phase-1` at the same commit | Clean |
| Test/E2E | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`, `upgrade-2.0-phase-1` | `173191e8694515af43797128070dbdfd2d246040`; `origin/upgrade-2.0-phase-1` at the same commit | Clean |
| Benchmark | `ephemeral-sandbox-test/benchmark` | Same Git repository, branch, commit, and upstream as Test/E2E; **not a fourth repository** | Clean as part of Test/E2E |
| Documentation | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs`, `layerstack_2_0` | `606cba03fc2db135b512c7d8951d12d37da7f92d`; `origin/layerstack_2_0` at `426b6be3284c26a59eb77d39ad6622997e8479c9` (local ahead 1) | Pre-existing `M implementation-plan/2.0 migration/phase 1/implementation/layerstack_storage_contract.md`; pre-existing `M implementation-plan/2.0 migration/phase 1/prompts/stage-03-implementation-instructions-authoring.md`; this guide is the only authoring-task addition |

The live storage-contract modification adds `workspace.json` to the v1
compatibility-path listing. It agrees with the canonical tree and is incorporated
here, but ownership of that edit is unknown: preserve it and do not fold it into a
Stage 03 commit without explicit custody.

Use these read-only preflight commands:

```bash
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox status --short --branch
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox rev-parse HEAD
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox rev-parse '@{upstream}'
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test status --short --branch
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test rev-parse HEAD
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test rev-parse '@{upstream}'
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs status --short --branch
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs rev-parse HEAD
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs rev-parse '@{upstream}'
```

### 0.5 Retained Stage 00–02 evidence available for reuse

These are inherited facts, not Stage 03 passes. Verify each retained path and digest
before citing it in a new run:

| Evidence | Retained identity |
| --- | --- |
| v2 binary golden | `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/contract-v2.bin`; 1,289 bytes; SHA-256 `760236a658433c1d385adb7b96db1f1429d74d66b1023e6a6553f8696fb0505f` |
| v2 diagnostic JSON | `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/contract-v2.json`; 4,377 bytes; SHA-256 `8e3cee4013021f236630c3c3182a3f40df0b1fc1ca02c210dca28a942a7bfda8` |
| PRC-R08 fixture | `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/portable-root-r08-v1.bin`; SHA-256 `dbdca20a50da366b037a9adeecc688bdce32cd4e0840630b31babb6018055c60` |
| v2 typed identities | tree `sha256:4d95…`; root `sha256:601c…`; use the complete values from the retained contract, never these display abbreviations in machine evidence |
| External expected contract | `e2e/fixtures/layerstack_phase1/portable-root-v2/expected-contract.json`; SHA-256 `242f…`; verify and record its complete live digest before reuse |
| PRC-01 live run | `20260724T181645.820036Z-96797`; summary SHA-256 `c4646eb0b87f9d876077ebd1b11784c9456b6257cbeaaa44dde4638b2390c81d`; cleanup SHA-256 `7494b60e4e20519a9fcc01479ed98a02217b71de98110365306a1175a80a9e1c` |
| Passing tiny benchmark | run `019f9583-82ff-717e-8247-c1162b0d536e`; aggregate 35.609 s; manifest SHA-256 `d9366bbefb84658e7a1b052bcf853523b2ab845debb051515a77f148f7b8526f`; summary SHA-256 `1b7afbcf0cf7aa6b2d4548738633bd2babaaed3bf0192e866d63e5e0fc224a98` |
| Retained failed PRC-R08 attempt | run `019f956a-3d46-77de-8115-98232c99d4bd`; summary SHA-256 begins `30ac548e…`; retain it and obtain the complete digest from the artifact/report before citation |
| Dependency entry/final evidence | entry-capture SHA-256 begins `3995…`; final JSON SHA-256 `1c77ccb2048f4c7383b0bbe6b45f5c999a88e79bcd2ef86ac2650d503e52be1d`; counts 1,143 packages / 2,179 features / 116 direct edges across 16 invocations |

Abbreviated values above are navigation aids only. A completion artifact must contain
full digests read from the retained artifact and must confirm that the bytes still
match. Stage 03 must re-run the immutable v2 vectors unchanged and compare the exact
external dependency multiset; the existence of retained Stage 02 evidence does not
replace those Stage 03 regression checks.

### 0.6 Contradictions and resolutions

| ID | Conflict/stale statement | Resolution or blocker |
| --- | --- | --- |
| `S03-C01` | The authoring prompt requires `stage_03_incremental_publication/handoff_from_stage_02.md`, but that file does not exist on the current branch. A historical copy remains at `origin/layerstack_2_0`. | Use the live, normative Stage 02 [`handoff_to_stage_03.md`](../stage_02_portable_root_contract/handoff_to_stage_03.md). The remote-ref copy was inspected and also says not to implement before owner approval; it is blocker evidence, not authority or permission to restore/fabricate history. |
| `S03-C02` | D2.5 is an approved owner decision, while Stage 03 needs v3 approval. | D2.5 remains v2-only. `PRC-STAGE03-OWNER-DECISION-G01.1` separately freezes the complete v3 amendment and corpus, so `S03-G01` is `PASS`. |
| `S03-C03` | The Stage 02 handoff and §0.4 record earlier revisions/custody; the live worktrees have advanced. | Preserve both as historical evidence. The fresh clean pre-mutation custody is retained in [`gate_resolution_20260725.md`](gate_resolution_20260725.md); re-capture again before implementation. |
| `S03-C04` | The complete canonical tree contains future pack/materialization/GC paths, but Stage 03 authorizes only its actual delta. | A tree pattern is not creation authority. Future directories must remain absent until their owning stage first uses them. |
| `S03-C05` | Stage 03 exit text mentions attribution surviving later squash, compaction, and GC, whose implementations belong to Stages 05–07. | Stage 03 proves its records are retained and restart-stable, plus focused compatibility hooks; destructive later-stage lifecycle qualification remains `DEFERRED_STAGE_07` until those owners exist. Do not claim the full cross-stage result in Stage 03. |
| `S03-C06` | Preparation 04 permits a later matched candidate/baseline allowance up to five minutes, while this task requires a 180-second focused campaign. | Use the 180-second campaign in §13 for Stage 03 POC evidence. Full corpus/host/RSS/selection qualification remains deferred; the shorter run cannot weaken or approximate it. |
| `S03-C07` | Existing `LayerStack::open` creates v1 `layers`/`staging` and holds the storage lock for the open lifetime, while Stage 03 requires a brief private commit section. | Preserve v1 behavior. Introduce a distinct private publication commit seam whose expensive work is outside its short exclusive section; do not silently change the v1 lock/lifecycle contract. |
| `S03-C08` | Current workspace capture materializes UTF-8/in-memory changes, but Stage 03 requires raw Linux bytes and external bounded ordering. | Replace only the candidate input path with a bounded raw-byte stream/spool. Preserve the public v1 capture contract until compatible integration is proven. |
| `S03-C09` | Benchmark CLI has no `plan` or `list` subcommand. | Use only the verified `validate`, `run`, `compare`, `recover`, and `cleanup` surfaces. Commands in §12 use `validate`/`run`; `recover` has no `--plan`. |
| `S03-C10` | Stage 03 allows a conditional locator/source lease for a last v1 carrier, but forbids general locator runs/packs. | Create only the minimum ordinary locator generation and fenced lease when an imported root would otherwise lose its last payload location. Absence is required when all chunks are loose. |

## 1. Status, purpose, and exact outcome

Stage 03 implementation, product regressions, the complete typed E2E catalog,
the runner-owned canonical campaign, dependency closure, portability/layout
audits, artifact verification, and cleanup are complete with direct retained
evidence. Performance selection remains honestly
`NOT_RUN/INSUFFICIENT_SAMPLE`, and full release qualification remains
`DEFERRED_STAGE_07`.

With `S03-G01` closed, Stage 03 must deliver one complete **private** v3 vertical
slice:

- owner-approved bounded Merkle content identity, with immutable v2 read/import
  compatibility;
- separate bounded persistent attribution identity using stable logical `ActorId`;
- deterministic scalar SeqCDC over bounded windows and typed loose-chunk
  put-if-absent;
- bounded raw-byte changed-path capture, external ordering/deduplication,
  persistent-page mutation, and unchanged structural sharing;
- atomic private heads, checkpoints, pins, and conditional source leases;
- branch-scoped `(publication-kind, BranchId, PublicationId)` durable operations,
  exact retry outcomes, and head/terminal crash-gap repair;
- semantic changed-path OCC conflict detection and bounded disjoint rebase;
- clean/dirty checkpoint, branch/MCTS fork, checkout, revert, reset, and ref-deletion
  semantics;
- v1 carrier source protection only where imported bytes still depend on v1;
- optional hidden v1/candidate comparison through the same normal publication
  protocol;
- unchanged public v1 read, write, publication, route, and `/eos` exposure authority.

An algorithm-only SeqCDC demonstration, codec-only result, favorable source review, or
single benchmark is not this outcome.

## 2. Entry gates and hard blockers

Every row is yes/no. A missing artifact is not “probably yes.”

| Gate | Current status | Required evidence | Stop rule |
| --- | --- | --- | --- |
| `S03-G01` complete v3 owner amendment and frozen corpus | `PASS` | Approved decision covering every §5.2 row, complete wire version/tags/domains/bounds/compatibility, immutable golden corpus and digest | Decision `PRC-STAGE03-OWNER-DECISION-G01.1`; manifest SHA-256 `7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be` |
| `S03-G02` Stages 00–02 pass and artifacts retained | `PASS` | Verify retained files/full digests in §0.5 and append the verification record | Record `stage03_entry_evidence_20260725.md`, SHA-256 `a7daa2be2bdca8605f35eb405b8bd43b800d18febecf46f9cf9b4c0f28075329` |
| `S03-G03` public v1 remains sole authority | `PASS` | Retained PRC-01 plus a fresh Stage 03 public-route regression | Fresh run `20260724T221647.648307Z-52067`, 1/1 PASS; summary SHA-256 `de5fee5ea1d5f2a25ca324d48df45815cfe4fdbc9a7f2458f19ef7efde6447d6` |
| `S03-G04` shared-worktree custody accepted | `PASS` | Fresh branch/HEAD/upstream/full status for all three Git repositories; explicit owners for overlapping dirty files | Custody accepted; all current dirty paths are task-owned and recorded |
| `S03-G05` exact dependency baseline frozen | `PASS` | Full 16-invocation baseline identities and two agreeing entry captures | Both captures SHA-256 `1c77ccb2048f4c7383b0bbe6b45f5c999a88e79bcd2ef86ac2650d503e52be1d`; exact external delta zero |
| `S03-G06` required product/test/benchmark tools ready | `PASS` | Rust toolchain/locked metadata, test `.venv`, benchmark venv/CLI `--help`, catalog collection, no network install | Rust/Cargo and both Python environments ready; safe catalog collects 643 tests |
| `S03-G07` environment and image pinned | `PASS` for implementation entry; per-run binary identity remains mandatory | Exact host/target, filesystem, kernel/cgroup, image digest, product binary/config identity | Entry identity record retained; every measured run must retain its newly built binary/config identity |
| `S03-G08` available disk and cgroup headroom | `PASS` for implementation entry; recheck immediately before campaign | Allocated-byte baseline, free bytes/inodes, 384 MiB RSS cap and at least 128 MiB-over-idle headroom demonstrably available | Observable 384 MiB cgroup-v2 cap and environment headroom retained; warmed-idle campaign check remains mandatory |
| `S03-G09` benchmark plan/verifier ready | `PASS` | Canonical preset validates; focused runner/strict-artifact/dispatch tests pass 22/22; runner clock and 180 s deadline are encoded | Final runner-owned run `019f977b-752d-7868-927d-170b8d46a078` completed in 137.27 s |
| `S03-G10` append-only reporting/run-owned cleanup ready | `PASS` | Planned report entry, run ID, exact owned resources, artifact roots, cleanup/quiescence oracle | Iterations 001–003 demonstrate pre-entry, exact ownership, immutable evidence, and exact cleanup |

## 3. Scope and non-goals

### 3.1 Stage 03 owns

Stage 03 owns only private loose logical/attribution objects; candidate refs;
publication operations and bounded work; candidate publication/OCC/recovery/ref
behavior; necessary v1 source protection; hidden comparison; focused observability,
tests, and benchmark evidence.

### 3.2 Explicit non-goals

Do not add, precreate, or claim:

- pack writing/compaction or general locator runs; the sole exception is the minimum
  existing-v1 physical locator plus lease genuinely required to protect a last carrier;
- native materializations or activation (Stage 04);
- GC authority, `gc/CURRENT`, mark/sweep, retention deletion, pack/locator compaction,
  or squash ownership (Stage 05);
- candidate public authority, cutover, fallback routing, or migration retirement
  (Stages 06–07);
- `refs/legacy`, `/eos/legacy`, a new durable `/eos/namespace_execution`,
  shadow-specific roots/receipts/journals/transactions, full-tree identity manifests,
  empty schema scaffolding, or reserved future directories;
- a new external crate/package, system command/helper, target-image helper, service,
  sidecar, daemon, network dependency, unsafe portable-core path, or alternate
  E2E/benchmark scheduler;
- `seqcdc-rs`, SIMD, async in the portable core, host/environment identity, or
  materialization/carrier fields in content identity;
- full Stage 07 host/architecture/RSS/corpus/repeated-selection qualification.

## 4. Complete `/eos` structure and ownership

### 4.1 Canonical migration-time tree

This is the complete canonical tree, not a list of directories Stage 03 may create:

```text
/eos/
├── layer-stack/
│   ├── .storage-writer.lock
│   ├── CONTROL
│   ├── objects/
│   │   ├── loose/<kind>/<digest-prefix>/<typed-id>
│   │   ├── packs/<pack-id>.pack
│   │   └── locators/
│   │       ├── <run-id>.sst
│   │       └── CURRENT
│   ├── refs/
│   │   ├── heads/<branch-id>
│   │   ├── checkpoints/<checkpoint-id>
│   │   ├── pins/<pin-id>
│   │   └── leases/<lease-id>
│   ├── operations/<operation-id>/
│   │   ├── STATE
│   │   └── work/
│   ├── materializations/<materialization-id>/
│   │   ├── CURRENT
│   │   └── generations/<generation>/
│   │       ├── MANIFEST
│   │       └── carriers/<carrier-id>/...
│   ├── gc/CURRENT
│   ├── manifest.json
│   ├── workspace.json
│   ├── base/<base-id>/...
│   ├── layers/<layer-id>/...
│   ├── staging/<layer-id>.staging/...
│   └── .layer-metadata/<layer-id>.{digest,bytes}
├── workspace/
│   ├── manager.json
│   ├── .export/<spool-id>
│   └── <workspace-session-id>/
│       ├── upper/
│       ├── work/
│       └── executions/<execution-id>/transcript.log
├── storage/
│   ├── file_auditability/...
│   └── workspace_recovery/...
└── runtime/
    └── daemon/
        ├── runtime.sock
        └── runtime.pid
```

No `/eos/legacy`, `refs/legacy`, or new `/eos/namespace_execution` exists. A pattern
above is not authorization to precreate a directory; create directories only on first
real use by their owning stage.

### 4.2 Path-by-path Stage 03 map

Atomic file replacement means: create a same-filesystem run-owned temporary file,
write and validate bounded bytes, `fsync` the file, rename atomically, then `fsync`
the parent directory. Immutable object installation additionally uses
put-if-absent/no-replace semantics and verifies an existing object’s typed identity.

| Path/pattern | Owner; Stage 03 status and creation condition | Purpose; durability and recovery | Retention/bound/physical category | Visibility; proving evidence |
| --- | --- | --- | --- | --- |
| `/eos/layer-stack/.storage-writer.lock` | LayerStack; pre-existing v1 seam, reused only for the brief private commit section | Cross-process serialization for visible ref/terminal transitions; lock owner recovers, never payload-builds under it | One bounded metadata file, `M`; retain while storage exists | Masked; lock-wait/hold counters and `S03-E2E-OCC-*` |
| `/eos/layer-stack/CONTROL` | LayerStack; Stage 03 creates on first real candidate use after owner gate | Approved storage version/capabilities only; atomic replace and fail-closed decode; LayerStack boot recovery | One owner-bounded record, `M`; never a migration-authority claim | Masked; `S03-E2E-LAYOUT-01`, restart/hostile-record case |
| `objects/loose/<kind>/<prefix>/<typed-id>` | LayerStack; Stage 03 creates parent prefixes lazily when installing a real object | Immutable typed content/attribution object; temp-write, file fsync, typed put-if-absent, parent fsync; recovery verifies or fails closed | `Lhot`; object/page and metadata budgets; orphan deletion deferred to Stage 05 GC | Masked; identity/publication/resource cases |
| `objects/packs/<pack-id>.pack` | Stage 05; **must remain absent** in Stage 03 | Future immutable pack | Not part of Stage 03 accounting except forbidden-path zero | Masked; layout assertions at every boundary |
| `objects/locators/{<run-id>.sst,CURRENT}` | Stage 05 normally; Stage 03 conditional only when a v1 carrier is the last physical location | Minimal ordinary immutable locator run then atomic `CURRENT`; recovery validates generation/checksum and fails closed | Conditional `M` plus referenced carrier bytes; no empty/general runs | Masked; `S03-E2E-SOURCE-01`; absence when all-loose |
| `refs/heads/<branch-id>` | LayerStack Stage 03; first real private branch | Atomic `{root, attribution_root, generation, publication_id}` approved record; repaired with operation journal before next advance | One bounded ref per admitted branch, `M`; retained by policy | Hidden/private; public API behavior plus allowed crash inspection |
| `refs/checkpoints/<checkpoint-id>` | LayerStack Stage 03; on named checkpoint | Atomic content/attribution pair and approved metadata; recovery validates typed references | `O(1)` `M`; deletion removes ref only | Hidden/private; ref E2E and zero-payload counters |
| `refs/pins/<pin-id>` | LayerStack Stage 03; only when a root must remain live without independently writable head | Atomic bounded pin to content/attribution pair | `O(1)` `M`; explicit owner releases | Hidden/private; fork/MCTS lifetime case |
| `refs/leases/<lease-id>` | LayerStack Stage 03 only for imported last-v1-carrier protection | Durable fenced locator-generation/source lease before any dependent ref is visible; boot validates fence | Bounded active leases, `M`; release only after no dependent root; protected bytes reported | Hidden/private; restart and legacy-delete attempt |
| `operations/<operation-id>/STATE` | LayerStack Stage 03; first request for `(kind, BranchId, PublicationId)` | Atomic bounded request digest/base/prepared/terminal record per approved schema; branch recovery repairs head/terminal gap | One bounded active/retained outcome, `M`; expiry returns `OutcomeExpired`, never republishes | Hidden/private; all idempotency/failpoint cases |
| `operations/<operation-id>/work/` | LayerStack Stage 03; only when actual bounded spill/build work is needed | Externally sorted changed-path runs and private temp state owned by exact operation | `Pstaging`; ≤5% captured payload, ≤4 MiB/pub metadata, exact reap/join; no unexplained residue | Hidden/private; failpoint/resource/cleanup artifacts |
| `materializations/**` | Stage 04; **must remain absent** | Future native materialization/activation generations | Forbidden Stage 03 bytes | Masked; layout assertions |
| `gc/CURRENT` | Stage 05; **must remain absent** | Future GC generation/authority | Forbidden Stage 03 bytes | Masked; layout assertions |
| `manifest.json` | v1 LayerStack; pre-existing and authoritative | Existing v1 atomic manifest protocol and recovery unchanged | Existing v1 metadata, reported separately in `M` | Public behavior through existing APIs; v1 regression |
| `workspace.json` | v1 compatibility/workspace binding; pre-existing | Existing v1 state unchanged | Existing v1 metadata | Masked; compatibility/layout regression |
| `base/<base-id>/**` | v1 LayerStack; pre-existing authoritative carrier | Existing base payload | Existing carrier category in physical equation; candidate must not copy/delete it | Public logical behavior; outside allocated-byte accounting |
| `layers/<layer-id>/**` | v1 LayerStack; pre-existing authoritative carriers | Existing published v1 layers | Existing carrier category; protect a last location before candidate visibility | Public v1 regression/source-hold case |
| `staging/<layer-id>.staging/**` | v1 LayerStack; pre-existing v1 publication scratch | Existing v1 fsync/rename path unchanged | Existing v1 `Pstaging`; not candidate operation work | Public v1 regression; no candidate scanner |
| `.layer-metadata/<layer-id>.{digest,bytes}` | v1 LayerStack; pre-existing | Existing v1 integrity/accounting records | Existing v1 `M` | Public v1 and storage-shape regression |
| `/eos/workspace/manager.json` | WorkspaceManager; pre-existing | Session-manager state; LayerStack never ingests/deletes it | WorkspaceManager `M`, outside retained candidate bytes | Masked; ownership E2E |
| `/eos/workspace/.export/<spool-id>` | WorkspaceManager; only its export lifecycle creates it | Export scratch; never logical publication input | WorkspaceManager staging, separately reported | Masked; negative scan/deletion assertion |
| `/eos/workspace/<session>/upper/**` | WorkspaceManager owns; admitted session supplies read-only capture view | **Only** changed-payload source for Stage 03; candidate reads bounded raw Linux bytes without taking ownership | `ΣUactive`, separately reported; session owner deletes | Masked; publication/ownership E2E |
| `/eos/workspace/<session>/work/**` | WorkspaceManager/OverlayFS; pre-existing per session | Overlay workdir; never ingest, hash, copy, or delete | `ΣUactive`, separate | Masked; negative input assertion |
| `/eos/workspace/<session>/executions/**` | WorkspaceManager/operation; pre-existing per command | Execution transcript/scratch; never candidate payload | Workspace/session accounting, separate | Masked; negative input assertion |
| `/eos/storage/**` | storage services | Audit/recovery state outside LayerStack | Separate owner/accounting | Masked; prove no scan/collect/delete |
| `/eos/runtime/daemon/**` | runtime daemon | Socket/PID runtime state | Separate owner/accounting | Masked; prove no scan/collect/delete |
| `/eos/legacy`, `/eos/layer-stack/refs/legacy`, `/eos/namespace_execution` | No Stage 03 owner; **must remain absent** | No durable compatibility mapping/schema is authorized | Exactly zero bytes | Masked; forbidden-path evidence at every boundary |

Use the canonical physical equation without double counting:

`T = Lhot + Hcold + ΣUactive + Pstaging + M`.

Report allocated filesystem blocks, not only apparent length. Existing v1 carriers and
active workspace upper/work remain separate categories; do not label unchanged v1
bytes as newly created candidate storage.

### 4.3 Boundary assertions

| Boundary | Required `/eos` assertion |
| --- | --- |
| Setup before first candidate use | Existing v1/workspace/storage/runtime paths match owners; no candidate/future/forbidden path exists |
| Active publication | Only the exact operation work, lazy loose-object prefixes, and conditional source hold may appear; `upper` is the sole input; workload namespace still masks `/eos` |
| Post-commit | Head and terminal state agree; immutable objects are typed/durable; no temp rename residue; v1 manifest/route unchanged |
| Restart | `CONTROL`, refs, operation states, locators/leases decode within bounds; head/terminal gap is repaired before branch advance |
| Injected failure | Head is old or names the one complete result; run-owned work is resumed/reaped; loose orphans are safe and not broadly deleted |
| Ref/checkpoint deletion | Only the ref disappears; no synchronous payload deletion; unrelated refs/leases unchanged |
| Session teardown | WorkspaceManager removes only its session resources; LayerStack does not delete manager/export/storage/runtime state |
| Settled/quiescent | Zero active operation workers/tasks/payload queue, no detached tasks/strong cycles, no unowned work/temp files, exact retained terminal/lease residue, future and forbidden paths absent |

## 5. Architecture, types, and dependency boundaries

### 5.1 Ownership and dependency direction

```text
public workspace/file APIs
        │
        ▼
workspace raw-byte capture stream ──► LayerStack candidate publication coordinator
                                           │
              ┌────────────────────────────┼─────────────────────────────┐
              ▼                            ▼                             ▼
      changed-path spool             SeqCDC/object store          refs/operation/OCC
              │                            │                             │
              └──────────────► portable layerstack-core ◄───────────────┘
                                   values/codecs/ports only
```

- `layerstack-core` owns safe, std-only portable values, validation, canonical
  codecs, typed IDs, and sink/source ports. It does not hash, touch a filesystem,
  spawn work, inspect a host, or know v1 carriers/materializations.
- LayerStack owns the existing `sha2` digest adapter, bounded readers, storage paths,
  fsync/rename/locks, immutable installation, refs, operations, recovery, locators,
  leases, resource permits, observability, and test-only failpoints.
- Workspace owns session admission and the `upper` capture source. It exposes bounded
  raw-byte events; it does not own Merkle identity or candidate persistence.
- Operation/public services invoke the normal publication protocol and preserve the
  current v1 response/authority contract. Hidden validation is additive and bounded.
- E2E and benchmark code consume authenticated/public observations and outside
  allocated-space inspection; product code never depends on either harness.

Portable core remains `#![forbid(unsafe_code)]` and independent of filesystem,
Docker, OverlayFS, mount/runtime/async/serde/SHA implementation, host paths, uid/gid
identity, environment, and materialization types. Reuse the existing `sha2` edge in
LayerStack; the exact external dependency delta must be zero.

### 5.2 Approved owner-decision shape

`PRC-STAGE03-OWNER-DECISION-G01.1` closes every row below without weakening the
higher-authority identity requirements or exclusions. Exact tags, domains, wire
fields, bounds, errors and compatibility rules are normative in the decision; exact
goldens and corpus inventories are normative in its immutable manifest.

| Record/type | Identity-bearing content required by higher authority | Explicitly excluded | Approved closure |
| --- | --- | --- | --- |
| `RootRecordV3` / `RootId` | logical format, required capabilities, approved chunk profile, Merkle tree root | publication/branch/generation/parent/base, actor/attribution, timestamp, backend, carrier/locator/materialization | Decision §§4, 16 and 21 |
| `TreePage` / typed page ID | canonically ordered bounded directory entries/child references and approved logical metadata | host inode/path encoding artifacts, backend/carrier/history | Decision §§5–6, 16 and 21 |
| `FileNode` / typed ID | approved logical metadata, size/sparse semantics, segment root/list reference | source path/FD/carrier, actor/history | Decision §§7–8, 16 and 21 |
| `SegmentPage` / typed ID | ordered bounded chunk/zero/sparse descriptors | queued payload/source location | Decision §§9, 16 and 21 |
| `Chunk` / typed ID | exact logical payload bytes under approved typed domain | file path, offset, carrier, author | Decision §§10, 16 and 21; SeqCDC remains Prep 03 |
| `AttributionRoot` / `AttributionRootId` | approved attribution format/capabilities and bounded attribution page root | content-irrelevant host identity, operation-history scan | Decision §§11, 16 and 21 |
| `AttributionPage` / typed ID | canonically ordered path/range attribution to stable logical actor/publication facts | content identity, host uid/gid, environment identity | Decision §§11, 16 and 21 |
| `BranchId`, `PublicationId`, checkpoint/pin/lease IDs | approved stable logical identifiers | host/time randomness unless explicitly normalized outside identity | Decision §12 |
| Head record | `{root, attribution_root, generation, publication_id}` plus only approved framing | names as content inputs | Decision §13 |
| Operation `STATE` | kind/branch/publication scope, request digest, base triple, phase, prepared result, terminal exact outcome/retention facts required by protocol | payload queue, complete tree/history | Decision §14 |
| Locator/source lease | physical typed object → existing v1 location and fenced locator generation/lease facts | mapping in content identity | Decision §15 |

Approved maximum encoded sizes must be at or below the Preparation 04 memory and
metadata budgets and must be enforced before allocation. Decoder errors must be typed
for at least wrong kind/version/domain, trailing bytes, unsorted/duplicate entries,
oversized count/length/page/depth, dangling edge, invalid sparse range, unknown
required capability, checksum/corruption, and arithmetic overflow.

### 5.3 Stage 03 resource and algorithm invariants

- scalar SeqCDC uses the Prep 03 semantics: 8/16/32 KiB min/target/max, threshold 5,
  trigger 50, jump 512, fixed 32 KiB window/ring, and borrowed two-slice input at wrap;
- at most four storage workers globally; global owned-storage semaphore 64 MiB;
- no payload queue; descriptor buffering at most 16 descriptors / 64 KiB;
- external ordering fan-in 8; lower traversal depth 64; reader 64 KiB;
  encoder scratch 256 KiB; index cache 16 MiB;
- per-publication owned metadata/work at most 4 MiB; publication staging at most 5%
  of captured payload;
- metadata budgets: chunk at most 96 B, segment at most 64 B, changed path at most
  256 B plus path bytes;
- process RSS at most 384 MiB and at most 128 MiB over measured idle;
- normal incremental publication has zero complete-tree/history scans and no
  all-path/all-live resident set;
- localized-write target is changed unique content plus 64 KiB plus one segment page;
  hard failure is median amplification above 4× or any sample at least `25% × F`;
- disjoint concurrent throughput is at least 90% of matched raw baseline; small-edit
  p95 is at most `baseline_p95 × 1.15 + 5 ms`; each operation is below 60 s.

## 6. File-by-file implementation map

All “Add” rows are **proposed** filenames because the current tree has no owner for
that concern. The implementation agent may choose a different new name only after
showing the existing owner is unsuitable and updating this guide/tracker without
changing the normative contract.

At the authoring snapshot, every mapped product and test/benchmark source path was
clean and unowned by another worktree change. The documentation exceptions are
called out in §0.4 and §6.5. Recheck all three complete statuses before editing;
“clean at snapshot” is evidence of custody, not permission to overwrite a later edit.

### 6.1 Product

| Path | Action and responsibility | Preserved behavior/custody | Smallest verification; rollback boundary |
| --- | --- | --- | --- |
| `crates/sandbox-runtime/layerstack-core/src/identity.rs` | Modify after gate: add owner-approved v3 typed IDs/domains | Preserve all v2 types/values; clean at snapshot | Focused v2+v3 identity tests; remove only v3 additions |
| `crates/sandbox-runtime/layerstack-core/src/codec.rs` | Modify: side-by-side bounded v3 framing/decoding; hostile pre-allocation checks | Preserve `EOS-LS2\0`, v2 bytes and decode; never repurpose v2 tags | `canonical_v3`, `hostile_v3_decode`, existing `canonical_contract`; revert v3 branches only |
| `crates/sandbox-runtime/layerstack-core/src/root.rs` | Modify: approved `RootRecordV3` and validation | Preserve `RootRecordV2` fields/identity | v2 goldens plus v3 mutation/exclusion table |
| `crates/sandbox-runtime/layerstack-core/src/tree.rs` | Modify: approved tree/file/segment pages and bounded validation | Preserve flat v2 `TreeManifest`; flat v3 is derived stream only | page golden/hostile/share tests; remove v3 types |
| `crates/sandbox-runtime/layerstack-core/src/attribution.rs` | **Add (proposed):** attribution root/page/actor values and query ports | No current attribution owner exists; std-only/safe | attribution codec/sharing tests; delete module/export |
| `crates/sandbox-runtime/layerstack-core/src/port.rs` | Modify: portable object/page stream and digest callback ports | Preserve `CanonicalSink/Source` and v2 call sites | compile and fake-port tests; remove new traits |
| `crates/sandbox-runtime/layerstack-core/src/error.rs`; `crates/sandbox-runtime/layerstack-core/src/lib.rs` | Modify: typed v3 validation errors/exports | Preserve unsafe forbid and public v2 exports | core clippy/tests; remove v3 exports/errors |
| `crates/sandbox-runtime/layerstack/src/model/portable.rs` | Modify: map approved v3 digest domains to existing `sha2`; diagnostic flat export | Preserve v2 hashing/JSON and two-slice v2 seam | LayerStack v2 golden and v3 adapter tests; remove v3 adapter |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/mod.rs` | **Add (proposed):** private candidate composition root only | No current private-v3 owner; do not alter public routing | module-level integration test; delete module and call edge |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/object_store.rs` | **Add (proposed):** loose typed put-if-absent/verify using `storage/fs.rs` | Preserve v1 layer/staging layout | temp/existing/corrupt/crash tests; remove candidate objects after exact test cleanup |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/seqcdc.rs` | **Add (proposed):** Prep 03 scalar streaming chunker, borrowed ring slices, descriptor sink | Reuse `sha2`; no dependency/SIMD/unsafe/async | fixed vectors/read-fragmentation/resource bounds; delete module |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/spool.rs` | **Add (proposed):** bounded raw-byte mutation/conflict-key runs, merge fan-in 8 | Never replace v1 capture before compatibility proof | ordering/dedup/bounds/crash cleanup; delete module/work |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/tree.rs` | **Add (proposed):** persistent content/attribution page update/share and derived flat export | No normal-path flat read/write | localized page-read/write unit tests; delete candidate objects |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/refs.rs` | **Add (proposed):** heads/checkpoints/pins/leases, short commit lock, GC-barrier no-op hook | Preserve lifetime-held v1 lock behavior; no GC implementation | atomic/crash/ref-cost tests; remove private refs |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/operation.rs` | **Add (proposed):** branch-scoped journal, exact retry/expiry, boot recovery/head repair | Existing in-memory v1 lease registry is not a durable journal | phase/failpoint/restart tests; delete run-owned operation dirs |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/occ.rs` | **Add (proposed):** semantic conflict keys and bounded disjoint rebase | Reuse lessons, not in-memory complete sets, from `crates/sandbox-runtime/layerstack/src/stack/publish/*` | exact/ancestor/rename/opaque/hardlink/disjoint tests; remove candidate coordinator |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/source.rs` | **Add (proposed):** conditional v1 locator/fenced source lease | No general locator compaction or `refs/legacy` | last-location/restart/delete-attempt test; remove exact lease/run |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/publication.rs` | **Add (proposed):** ten-step normal private protocol; expensive work outside lock | Preserve `crates/sandbox-runtime/layerstack/src/stack/ops/publish.rs` v1 public path | end-to-end LayerStack integration and lock-hold counters; disconnect candidate invocation |
| `crates/sandbox-runtime/layerstack/src/observability.rs`; `crates/sandbox-runtime/layerstack/src/service/model.rs`; `crates/sandbox-runtime/layerstack/src/service/support.rs`; `crates/sandbox-runtime/layerstack/src/stack/observation.rs` | Modify: bounded additive private counters/state; hidden validation mode | Preserve `StorageAuthority::LegacyV1`, existing fields and zero/off behavior | serialization/backward/default-zero tests; remove additive fields/mode |
| `crates/sandbox-runtime/layerstack/src/stack/ops/publish.rs` | Modify only at final integration: invoke candidate privately/correlate without delaying or changing v1 outcome | Current v1 publication, fsync, OCC, manifest replace and failpoints remain authoritative | existing publish tests + hidden on/off; remove hook |
| `crates/sandbox-runtime/workspace/src/overlay/capture.rs`; `crates/sandbox-runtime/workspace/src/service/impls/capture_changes.rs` | Modify/add bounded candidate stream with raw `OsStrExt` bytes and only admitted `upper` | Preserve public v1 `Change` behavior until all regressions pass | raw-byte/whiteout/opaque/hardlink/bounds tests; remove candidate stream |
| `crates/sandbox-runtime/operation/src/layerstack/service/impls/publish_changes.rs`; `crates/sandbox-runtime/operation/src/workspace_session/service/impls/publish_session.rs` | Modify only for private invocation/correlation and stable `PublicationId` plumbing | Public response and v1 audit/manifest semantics unchanged | existing `workspace_session_publish*` tests; remove private plumbing |
| `crates/sandbox-runtime/layerstack/Cargo.toml`, workspace `Cargo.toml`, `Cargo.lock` | **Avoid external changes**; no new package | Existing external graph and Stage 02 core edge frozen | exact dependency comparator; any external delta is rollback trigger |
| `crates/sandbox-runtime/layerstack/src/storage/{fs.rs,lock.rs,whiteout.rs}` and `crates/sandbox-runtime/layerstack/src/stack/publish/*` | Reuse/modify only with focused compatibility proof | Shared critical seams; clean at snapshot | existing unit suites plus new candidate cases; revert isolated candidate helper |

### 6.2 Product tests

| Path | Action and responsibility | Preserved behavior/custody | Smallest verification; rollback |
| --- | --- | --- | --- |
| `crates/sandbox-runtime/layerstack-core/tests/{canonical_contract.rs,host_independence.rs}` | Modify additively for v3 after approval | Immutable v2 assertions unchanged; clean at snapshot | exact test binaries; remove only v3 cases |
| `crates/sandbox-runtime/layerstack-core/tests/hostile_v3_decode.rs` | **Add (proposed):** complete hostile/bounds matrix | No current dedicated hostile-v3 owner; absent at clean snapshot | one test target; delete file |
| `crates/sandbox-runtime/layerstack/tests/portable_root_golden.rs` | Modify additively for LayerStack v3 adapter | Existing v2 fixture bytes/IDs unchanged; clean at snapshot | focused test target; remove v3 rows |
| `crates/sandbox-runtime/layerstack/tests/candidate_publication.rs` | **Add (proposed):** object/tree/ref/operation/OCC/source integration | Keep public v1 tests separate; absent at clean snapshot | focused target; delete file and exact temp roots |
| `crates/sandbox-runtime/workspace/tests/unit/overlay_capture.rs` | Modify: raw-byte candidate stream and ownership negatives | Existing v1 capture cases unchanged; clean at snapshot | focused unit filter; remove new cases |
| `crates/sandbox-runtime/operation/tests/workspace_session_publish.rs`; `crates/sandbox-runtime/operation/tests/workspace_session_publish_security.rs` | Modify: v1 compatibility and hidden candidate independence | Current public API/security oracles unchanged; clean at snapshot | focused targets; remove new cases |

### 6.3 Test/E2E

| Path | Action and responsibility | Preserved behavior/custody | Smallest verification; rollback |
| --- | --- | --- | --- |
| `e2e/runtime/layerstack_phase1/helpers.py` | Modify: public logical oracle, authenticated counters, exact outside-layout/accounting projection | Preserve Stage 02 helper behavior; clean at snapshot | helper unit/catalog collection; remove Stage 03 helpers |
| `e2e/runtime/layerstack_phase1/conftest.py` | Modify only for run-owned Stage 03 fixtures and exact cleanup | Preserve existing shared fixture scopes; clean at snapshot | collection + one fixture unit; remove fixture |
| `e2e/runtime/layerstack_phase1/test_incremental_publication.py` | **Add (proposed):** typed cases in §10 | Existing family is the suitable owner; no alternate harness; absent at clean snapshot | catalog collection then one node; delete declarations |
| `e2e/tools/verify_external_dependency_delta.py`; `e2e/tools/test_verify_external_dependency_delta.py` | Reuse unchanged unless a proven comparator defect exists | Frozen exact comparator and tests; clean at snapshot | comparator fixture tests; no fork |

### 6.4 Fixtures

| Path | Action and responsibility | Preserved behavior/custody | Smallest verification; rollback |
| --- | --- | --- | --- |
| `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v3/**` | **Add (proposed) only after owner gate:** immutable approved bytes, JSON and digest manifest | Never rewrite `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/**`; v3 path absent at clean snapshot | digest manifest and golden tests; delete the unapproved/exact v3 fixture set |
| `e2e/fixtures/layerstack_phase1/incremental-publication-v3/**` | **Add (proposed) only after owner gate:** deterministic approved corpus and digest manifest | Preserve `e2e/fixtures/layerstack_phase1/portable-root-v2/**`; new path absent at clean snapshot | fixture digest verifier; delete exact v3 fixture |
| `benchmark/tests/fixtures/golden/layerstack_phase1/stage03_publication_v1.json` | **Add (proposed):** strict plan/artifact-shape fixture, never performance result goldens | Preserve existing portable-root/workspace-scratch fixtures; new file absent at clean snapshot | strict positive/negative fixture tests; delete file |

### 6.5 Artifact schemas, verification, and reporting

| Path | Action and responsibility | Preserved behavior/custody | Smallest verification; rollback |
| --- | --- | --- | --- |
| `e2e/schemas/layerstack_phase1/evidence-v1.schema.json` | Modify additively only if the existing version can truthfully express Stage 03 evidence | Never weaken Stage 02 mandatory fields or coerce null to zero; clean at snapshot | schema positive/negative fixtures; revert additive fields |
| `e2e/schemas/layerstack_phase1/evidence-v2.schema.json` | **Add (proposed) only if v1 cannot be extended compatibly:** strict Stage 03 evidence envelope | No current separate Stage 03 schema owner; absent at clean snapshot | version-selection plus positive/negative fixtures; delete schema and selector |
| `benchmark/backend/benchmark_lab/{models.py,observability.py,artifacts.py}` | Modify additively for versioned Stage 03 operation evidence, mandatory-field validation and retained digests | Preserve all existing read versions, migrations and artifact caps; clean at snapshot | compatibility tests including historical fixtures; remove only new version/fields |
| `benchmark/backend/tests/compatibility/test_artifacts.py` | Modify additively to reject missing, null or inconsistent mandatory Stage 03 fields while retaining old-reader cases | Existing artifact compatibility remains green; clean at snapshot | focused compatibility pytest; revert Stage 03 cases |
| `e2e/test-report.md` | Append only during future execution | Retain all passing and failed attempts; clean at authoring snapshot | tail/readback plus artifact digests; never roll back history |
| `.benchmark-state/**` | Runtime artifact root only; **avoid as source** | Runner-owned exact run/pair IDs; not present as a source edit at snapshot | strict manifest/verifier plus digest inventory; clean only the exact owned run |

### 6.6 Benchmark

| Path | Action and responsibility | Preserved behavior/custody | Smallest verification; rollback |
| --- | --- | --- | --- |
| `benchmark/backend/benchmark_lab/stage03_publication.py` | **Add (proposed):** strict operation adapter, campaign clock, samples/counters/accounting | Existing runner owns scheduling/state; no subprocess per sample if the current prebuilt pattern suffices; absent at clean snapshot | new adapter unit tests; delete operation |
| `benchmark/backend/benchmark_lab/{planning.py,runner.py}` | Modify minimally: register/dispatch Stage 03 operation and enforce the 180 s campaign deadline | Preserve all existing operation IDs/counts and interruption semantics; clean at snapshot | planning/runner focused tests; unregister operation |
| `benchmark/backend/benchmark_lab/resource_sampling.py` | Modify additively: collect allocated-space, process and cgroup samples needed by §13 | Preserve sampling behavior for all other operations; clean at snapshot | resource-sampling unit/integration tests; remove Stage 03 sampler fields |
| `benchmark/backend/benchmark_lab/recovery.py` | Modify only as required for runner-owned interrupted Stage 03 recovery and exact run reconciliation | Preserve existing recovery and interruption semantics; never create an alternate resume path; clean at snapshot | `benchmark/backend/tests/integration/test_recovery.py`; remove Stage 03 recovery case |
| `benchmark/defaults/definition-catalog.json` | Modify: one deliberate hidden operation definition | Preserve exact existing definitions; update strict counts coherently; clean at snapshot | catalog contract tests; remove entry |
| `benchmark/presets/layerstack-phase1-stage03-publication.yml` | **Add (proposed):** deterministic 180 s plan from §13 | Existing presets unchanged; absent at clean snapshot | CLI `validate`; delete preset |
| `benchmark/backend/tests/contract/{test_catalog.py,test_planning.py}`; `benchmark/backend/tests/integration/{test_runner.py,test_recovery.py}` | Modify additively for catalog, planner, runner clock, interruption and recovery | Preserve earlier operation counts and semantics; clean at snapshot | focused pytest nodes; revert Stage 03 cases |

### 6.7 Documentation

| Path | Action and responsibility | Preserved behavior/custody | Smallest verification; rollback |
| --- | --- | --- | --- |
| `implementation-plan/2.0 migration/phase 1/implementation/stage_03_incremental_publication/implementation_instructions.md` | Maintain tracker/checklist/commands without changing authority | This authoring task’s sole file; new at authoring snapshot; preserve concurrent docs edits | links/IDs/diff check; revert unsupported claims only |
| `implementation-plan/2.0 migration/phase 1/implementation/stage_03_incremental_publication/benchmark_note.md` | Future closure: replace `NOT_RUN` cells only with retained evidence | Do not prefill/pass from expectations; clean at snapshot | cross-check artifact digests; revert unsupported result |
| `implementation-plan/2.0 migration/phase 1/implementation/stage_02_portable_root_contract/handoff_to_stage_03.md`; `implementation-plan/2.0 migration/phase 1/implementation/stage_02_portable_root_contract/contract_v2_owner_decision_d2_5.md` | Read-only historical evidence | Never rewrite; clean at snapshot | digest/read check; no change |
| `implementation-plan/2.0 migration/phase 1/implementation/layerstack_storage_contract.md` | Authority; modify only through separate owner-controlled contract change | Pre-existing dirty edit must be preserved | link/diff review; do not absorb |
| `docs/maintainer-architecture.md` in the product repository | Future additive ownership documentation after code exists | Preserve current core boundary; clean at snapshot | doc link/source audit; revert Stage 03 section |

## 7. Ordered implementation sequence

No implementation row begins until `S03-G01`, `S03-G04`, and all of its dependency
rows are closed. G01 and G04 are now closed; each row still waits for its other
declared dependencies.
Each row is a separately reviewable/rollbackable change. After any failure, remove
only exact run-owned scratch, preserve artifacts/report history, and leave immutable
loose orphans for the later GC owner unless the test root itself is wholly run-owned.

| Step / progress ID | Prerequisites; files | Introduced behavior and preserved invariants | Focused proof; failure cleanup/rollback | Proceed only when |
| --- | --- | --- | --- | --- |
| 1 / `S03-I01` v3 codecs | `G01,G04`; core identity/codec/root/tree/attribution/error tests and approved fixtures | Closed approved types, canonical bytes, hostile pre-allocation bounds, v2 side-by-side import | Core `canonical_v3`, `hostile_v3_decode`, host independence, all v2 goldens; remove v3 exports/fixtures only | Every approved golden/tag/domain/bound matches and all v2 bytes remain exact |
| 2 / `S03-I02` loose object store | `I01`; candidate `object_store.rs`, `storage/fs.rs`, portable adapter | Deterministic typed SHA-256 put-if-absent, existing-object verification, durable lazy prefixes | Focused install/existing/collision/corrupt/fsync crash tests; delete only exact run-owned object root | No partial object can be observed; no external dependency delta |
| 3 / `S03-I03` capture/order/SeqCDC | `I01,I02`; workspace capture, candidate `spool.rs`, `seqcdc.rs` | Raw-byte final mutations, external dedup ordering, Prep 03 boundaries, no payload queue | Fixed CDC vectors, fragmented reads, whiteout/opaque/rename/hardlink cases, cap counters; reap exact operation work and join tasks | 32 KiB ring, fan-in 8, four global workers, permits/FD/queue caps are asserted |
| 4 / `S03-I04` persistent pages | `I01–I03`; candidate tree, portable adapter | Changed file/segment/tree/attribution page mutation, unchanged sharing, derived flat stream | Small/large tree edits and attribution queries with page counters; remove exact run-owned candidate root | Zero normal flat/complete-tree/history scans and exact reconstruction after restart |
| 5 / `S03-I05` refs/commit seam | `I02,I04`; candidate refs, lock/fs helpers | Atomic heads/checkpoints/pins/leases and a GC-barrier hook point that is inert when GC is absent | Atomic rename/fsync/crash tests, clean ref zero-payload tests, lock-hold timing; remove exact run-owned refs | Expensive capture/hash/sort/page/compare work is observably outside the short lock |
| 6 / `S03-I06` operation recovery | `I02,I04,I05`; operation/publication modules | Branch-scoped ID, request digest, prepared/terminal states, exact retry/expiry, head-gap repair | Nine focused failpoints plus restart/lost response; retain failed artifacts, reap only owned work | Head is old or one complete result and cannot advance past missing terminal |
| 7 / `S03-I07` OCC/rebase | `I03,I04,I06`; spool/occ/publication and existing publish logic as reference | Exact/ancestor/rename/opaque/hardlink semantic conflicts; disjoint bounded rebase | Two/three-writer focused tests with retries, lock wait, conflict keys and progress counters | No complete path set; typed bounded contention; both disjoint results visible |
| 8 / `S03-I08` ref operations | `I05–I07`; refs/publication/service models | Clean/dirty checkpoint, fork/pin choice, checkout, revert, reset, checkpoint delete | Cost/correctness/restart tests; delete only exact test refs | Generation/attribution semantics and zero-payload rules match §4/Stage 03 table |
| 9 / `S03-I09` v1 source holds | `I02,I05,I06`; source/refs/object store | Only when needed, fenced last-v1-locator lease before dependent ref visibility | Import, restart, attempted v1 cleanup, corrupt/missing locator fail-closed; release exact test lease | Candidate reconstructs after restart/delete attempt; no `refs/legacy`; all-loose case creates none |
| 10 / `S03-I10` hidden validation | `I01–I09`; LayerStack public hook, observations, operation service | Normal Stage 03 protocol on hidden head, bounded correlation/mismatch evidence | On/off/restart/backpressure tests; stop new hidden work and reap owned operation work | v1 outcome/latency contract and public authority remain unchanged |
| 11 / `S03-I11` evidence closure | `I01–I10`; observations/failpoints, E2E, benchmark, schemas, docs | Strict typed cases, 180 s plan/verifier, dependency/layout/resource evidence and handoff | Execute §12 only after report pre-entry; runner-owned cleanup; source rollback per §6 | Every mandatory tracker/checklist row has direct retained evidence; missing fields remain open |

The commit-loop structure for steps 5–7 is mandatory:

1. outside the exclusive lock, open/idempotency-check the operation, capture/spill,
   chunk/hash/install, build content and attribution pages, and persist prepared state;
2. under the brief lock, read/validate head, participate in an active GC barrier hook,
   atomically install head and terminal outcome when base matches;
3. on head advance, leave the lock, compare the spooled semantic keys, rebuild touched
   pages against current for a disjoint change, and retry within fixed approved
   count/time caps;
4. after commit, release permits/FDs/tasks/work and retain only the bounded outcome.

## 8. Canonical progress tracking rules

The one canonical tracker is §15.2 so the document ends in the required closure order.
Use only:

`BLOCKED`, `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL`,
`DEFERRED_STAGE_07`.

Do not use percentages or infer a pass from code review. Update a row only with the
exact command/evidence ID, retained artifact path and SHA-256, exact cleanup outcome,
and UTC timestamp. A failed attempt remains in `e2e/test-report.md`; later success
does not erase it.

## 9. Completion-checklist rules

The evidence-backed checklist is §15.1. An item may be checked only when its progress
row is `PASS`, the named command passed, and the named artifact contains every
mandatory field. Missing, `null`, unsupported, inconsistent, or unavailable data is
`BLOCKED`/`FAIL`/`NOT_RUN` as appropriate, never zero.

## 10. Typed E2E catalog

### 10.1 Declaration contract and common rules

Implement each stable case with the existing
`e2e.harness.catalog.declarations.e2e_test` decorator fields:
`id`, `title`, `description`, `features`, `validations`,
`validation_features`, `execution_surface`, `owner_id`, and `timeout_ms`.
Use product family `runtime.layerstack-phase1`; give every validation exactly-once
semantics. Proposed function names below are part of the execution contract.

Common preconditions for every live case are `S03-G01–G10`, a pinned product
binary/config/image, a fresh run-owned sandbox/workspace/session, and fixture
manifest verification. `V3_FIXTURE_SHA256` means the full owner-approved digest,
`7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be`;
a test must refuse to run rather than substitute a mutable fixture. Public
workspace/file behavior is the logical correctness oracle.
Outside private inspection is allowed only for layout, allocated space, permissions,
durability/failpoint state, and residue; it never substitutes for public
reconstruction. Every case:

- writes raw samples/verdict/cleanup under the harness-owned report root;
- caps any single operation below 60 s and uses the tighter `timeout_ms` named below;
- cleans only exact run-owned sandbox/workspace/operation/process-group resources;
- waits for explicit zero-task/worker/queue/permit quiescence and records retained
  terminal/lease state;
- fails on a missing mandatory counter/artifact field.

### 10.2 Concrete cases

The “evidence” column names mandatory case-specific fields in addition to the common
revision/build/host/target/image/fixture/run ID, elapsed, resource peaks, artifact
digests, and cleanup fields.

| Stable ID / proposed test function / title | Seam, fixture and exact action | Oracle and allowed inspection | Evidence, limit, cleanup and pass rule |
| --- | --- | --- | --- |
| `runtime.layerstack-phase1.incremental.i01-v2-immutable` / `test_s03_i01_v2_immutable` / **S03-I01 v2 vectors remain immutable** | Core/LayerStack codec plus packaged public runtime; retained v2 three-fixture digests; re-run encode/decode/import and one public v1 publication | Exact retained bytes/typed IDs and unchanged public v1 tree/revision behavior; outside digest/layout only | Full fixture digests, bytes/IDs, authority; 30 s; pass only exact match and no candidate path from v2-only action |
| `runtime.layerstack-phase1.incremental.i02-v3-goldens` / `test_s03_i02_v3_goldens` / **S03-I02 approved v3 typed goldens** | Approved v3 fixture; encode/decode root/tree/file/segment/chunk/attribution root/page | Exact approved bytes/typed IDs and independent logical reconstruction | Each type’s full bytes digest/ID/encoded length; 30 s; pass only approved exact match |
| `runtime.layerstack-phase1.incremental.i03-hostile-codec` / `test_s03_i03_hostile_codec` / **S03-I03 hostile v3 decode is bounded** | Approved hostile fixture; wrong kind, trailing bytes, unsorted/duplicate, oversized, dangling, sparse-invalid, unknown-required inputs | Typed errors, no panic, no oversized allocation | Error code per vector, peak allocation/RSS; 30 s; every vector exact and within owner bound |
| `runtime.layerstack-phase1.incremental.i04-derived-flat` / `test_s03_i04_derived_flat` / **S03-I04 flat export is derived** | Approved multi-page fixture; stream flat diagnostic and reconstruct | Same logical tree; normal publication counters show zero flat input/output/root computation | page/flat/root counters; 30 s; equality plus zero normal-path flat use |
| `runtime.layerstack-phase1.incremental.i05-portability` / `test_s03_i05_portability` / **S03-I05 v3 IDs are host independent** | Same approved bytes/fragmentation matrix on amd64/arm64 and supported filesystems | Exact root/page/chunk/attribution IDs | Host/target/fs matrix and IDs; 60 s per invocation; all required matrix entries agree or remain visibly `NOT_RUN` |
| `runtime.layerstack-phase1.incremental.p01-empty-nested` / `test_s03_p01_empty_nested` / **S03-P01 empty and nested publication** | Public workspace/file API; approved empty/nested corpus; publish private candidate and restart | Independent public file/list/metadata tree equals expected before/after restart | changed paths/ancestors, object/page sharing and scans; 45 s; exact equality and bounded work |
| `runtime.layerstack-phase1.incremental.p02-file-shapes` / `test_s03_p02_file_shapes` / **S03-P02 tiny, large, sparse and zero files** | Public writes for tiny/large and explicit sparse/zero corpus; publish/restart | Exact bytes, holes/zero rules, unchanged IDs shared | SeqCDC boundaries/IDs, bytes read/hashed/written, page deltas; 45 s; no full buffering/scan |
| `runtime.layerstack-phase1.incremental.p03-linux-kinds` / `test_s03_p03_linux_kinds` / **S03-P03 raw paths and Linux node kinds** | Public APIs/approved setup for raw byte paths, xattrs, hardlinks, symlinks, devices/FIFOs where supported | Independent logical metadata/content comparison; unsupported required capability is typed, never silently dropped | Capability matrix, raw path bytes, link groups, page IDs; 45 s; every supported kind exact and unsupported status explicit |
| `runtime.layerstack-phase1.incremental.p04-mutations` / `test_s03_p04_mutations` / **S03-P04 final mutation semantics** | Deterministic deletion, opaque directory, rename, truncate, append, metadata-only cases | Exact final tree after publish/restart; rename/hardlink groups atomic | Per-variant mutation/conflict keys/read-write deltas; 45 s; changed paths/ancestors only |
| `runtime.layerstack-phase1.incremental.p05-attribution` / `test_s03_p05_attribution` / **S03-P05 attribution is separate and bounded** | Same content by two actors plus edit/rename/restart and blame query | Content IDs equal where content equal; attribution IDs differ; correct actor/ranges; no history scan | content/attribution page sharing, query pages/output, history-scan zero; 45 s |
| `runtime.layerstack-phase1.incremental.r01-clean-refs` / `test_s03_r01_clean_refs` / **S03-R01 clean checkpoint and fork** | Normal ref APIs; checkpoint and branch/MCTS fork current pair | Refs select same content/attribution; generation zero for fork | Exactly one ref/head each, zero payload/native tree; 30 s |
| `runtime.layerstack-phase1.incremental.r02-dirty-delete` / `test_s03_r02_dirty_delete` / **S03-R02 dirty checkpoint and delete** | Edit, dirty checkpoint, then delete checkpoint | Delta equals ordinary publication plus one ref; deletion preserves payload/other refs | Object/page/ref delta and allocated bytes; 30 s |
| `runtime.layerstack-phase1.incremental.r03-checkout` / `test_s03_r03_checkout` / **S03-R03 checkout selects only** | Create two heads, checkout session selection | Public reads change selection; no head record mutates | Before/after head digests and selection; 20 s |
| `runtime.layerstack-phase1.incremental.r04-revert` / `test_s03_r04_revert` / **S03-R04 revert is a publication** | Edit then revert historical tree as new publication | Generation advances; historical content root may be reused; reverted ranges attributed to reverting actor | root/attribution/generation/publication and delta; 30 s |
| `runtime.layerstack-phase1.incremental.r05-reset` / `test_s03_r05_reset` / **S03-R05 reset moves an existing pair** | Reset head to historical content/attribution pair | Public tree matches target and explicit reset outcome | Zero new logical/attribution objects, new generation/ref; 30 s |
| `runtime.layerstack-phase1.incremental.r06-retention` / `test_s03_r06_retention` / **S03-R06 checkpoint lifetime** | Restart and Stage 03-compatible simulated later-owner traversal; later real compaction/squash/GC matrix when available | Checkpoint content/attribution reconstructs; delete has no synchronous payload effect | Restart proof now; real later-stage run IDs remain `DEFERRED_STAGE_07`; never pass absent owners |
| `runtime.layerstack-phase1.incremental.o01-conflicts` / `test_s03_o01_conflicts` / **S03-O01 semantic conflicts** | Two writers for identical path/directory metadata, ancestor-remove/descendant, rename overlap, opaque/descendant, hardlink overlap | One stable conflict and one complete permitted result per variant | Spool keys, bounded pages/retries/time, no all-path set; 45 s |
| `runtime.layerstack-phase1.incremental.o02-disjoint-two` / `test_s03_o02_disjoint_two` / **S03-O02 two disjoint writers rebase** | Barrier-start two writers on disjoint paths | Both results visible after bounded rebase/restart | Throughput/lock wait/retries/progress ratio; 45 s; Preparation 04 threshold |
| `runtime.layerstack-phase1.incremental.o03-disjoint-three` / `test_s03_o03_disjoint_three` / **S03-O03 three-plus writers progress** | Barrier-start at least three disjoint writers plus bounded contention arm | All disjoint results visible; typed contention rather than hang/starvation | Per-writer progress/fairness/retries; 45 s; ≥90% matched raw baseline and operation <60 s |
| `runtime.layerstack-phase1.incremental.f01-before-state` / `test_s03_f01_before_state` / **S03-F01 death before operation state** | Kill/fail before durable `STATE`, restart, retry same ID | Old head or one exact result; no unowned work | Phase/head/outcome/residue; 30 s |
| `runtime.layerstack-phase1.incremental.f02-during-spill` / `test_s03_f02_during_spill` / **S03-F02 death during changed-path spill** | Kill/fail mid-run write, restart/retry | Partial run ignored/reaped; exact outcome | Run ownership/digests/residue; 30 s |
| `runtime.layerstack-phase1.incremental.f03-object-install` / `test_s03_f03_object_install` / **S03-F03 death during chunk/page install** | Kill/fail at temp/write/fsync/rename points, restart/retry | No corrupt visible object; put-if-absent idempotent | Object temp/final typed verification; 40 s |
| `runtime.layerstack-phase1.incremental.f04-objects-durable` / `test_s03_f04_objects_durable` / **S03-F04 death after roots durable** | Kill after immutable result before prepared state, restart/retry | Old head or same complete result; orphan safe | Root reachability/state/residue; 30 s |
| `runtime.layerstack-phase1.incremental.f05-after-prepared` / `test_s03_f05_after_prepared` / **S03-F05 death after prepared** | Kill after prepared fsync, restart | Resume or stable conflict from recorded base/input | Exact prepared fields/outcome; 30 s |
| `runtime.layerstack-phase1.incremental.f06-gc-barrier` / `test_s03_f06_gc_barrier` / **S03-F06 failure during active GC-barrier registration** | Simulate active barrier hook and fail/kill registration, without implementing GC | No ref becomes visible without participation; retry exact | Barrier/ref/state ordering; 30 s |
| `runtime.layerstack-phase1.incremental.f07-before-head` / `test_s03_f07_before_head` / **S03-F07 death before head rename** | Kill after prepared/commit admission before rename | Head remains old; retry exact | File/dir fsync and head digest; 30 s |
| `runtime.layerstack-phase1.incremental.f08-head-before-terminal` / `test_s03_f08_head_before_terminal` / **S03-F08 head-visible terminal gap repair** | Kill after head rename before terminal, restart then competing update/retry | Boot repairs exact terminal before branch advances | Head publication ID, repaired result, blocked competitor; 40 s |
| `runtime.layerstack-phase1.incremental.f09-terminal-before-response` / `test_s03_f09_terminal_before_response` / **S03-F09 lost response returns original** | Drop response after terminal fsync, restart/retry same ID; reuse different input; ack/expire arm | Same ID returns byte-for-byte outcome; mismatch typed; expired returns `OutcomeExpired` and never publishes | Outcome digest, generations/object deltas; 40 s |
| `runtime.layerstack-phase1.incremental.s01-v1-source` / `test_s03_s01_v1_source` / **S03-S01 last v1 carrier remains protected** | Import root whose last payload is v1, crash/restart, attempt legacy squash/delete | Candidate reconstructs; fenced locator/lease predates ref visibility; corrupt/missing locator fails closed | Locator generation/lease/protected bytes/order; no `refs/legacy`; 45 s |
| `runtime.layerstack-phase1.incremental.s02-validation` / `test_s03_s02_validation` / **S03-S02 hidden validation uses normal protocol** | Toggle hidden comparison on/off repeatedly, publish matched/mismatch corpus, restart | Bounded correlated evidence; public v1 authority/outcome unchanged and within admission/backpressure contract | Correlation IDs/mismatch cap/v1 latency/route; no new schema; 45 s |
| `runtime.layerstack-phase1.incremental.b01-resource-caps` / `test_s03_b01_resource_caps` / **S03-B01 largest corpus is bounded** | Largest frozen Prep 04 corpus under authenticated resource sampling | Exact public tree; no total-tree/history/all-live set | RSS/permits/bytes/workers/tasks/threads/queue/FD/mappings/encoder/cache; 60 s; every §5.3 cap |
| `runtime.layerstack-phase1.incremental.b02-ownership-mask` / `test_s03_b02_ownership_mask` / **S03-B02 `/eos` ownership and masking** | Inspect setup/active/commit/restart/failure/ref-delete/teardown/settled while public workload probes masking | `/eos` masked; only allowed lazy paths; only session `upper` read | Path snapshots/read-source audit/allocated bytes; forbidden zero; 45 s |
| `runtime.layerstack-phase1.incremental.b03-portable-deps` / `test_s03_b03_portable_deps` / **S03-B03 target independent with zero dependency delta** | Shell-less/read-only/non-root public cases plus invocation audit | Public behavior succeeds or typed policy rejection; no helper/network/new dependency/target image call | 16 dependency comparisons, process/network/helper/image ledger; 45 s per host invocation |
| `runtime.layerstack-phase1.incremental.b04-exit-artifact` / `test_s03_b04_exit_artifact` / **S03-B04 evidence is complete** | Run strict schema/verifier over all Stage 03 case/benchmark manifests | Missing/null/inconsistent fields reject; all referenced digests resolve | Traceability coverage, artifact paths/digests, cleanup ledger; 30 s; exact completeness |

## 11. Verification traceability matrix

Abbreviations: `core` is `layerstack-core`; `cand` is
`layerstack/src/stack/candidate`; `pub` is the public workspace/operation seam.
`A.*` fields are the strict evidence fields defined in §13.4. A row cannot close from
source inspection.

### 11.1 Identity, publication, refs, OCC, and recovery

| Requirement | Implementation / focused test | Typed E2E | Benchmark cell / mandatory artifact | Threshold | Progress |
| --- | --- | --- | --- | --- | --- |
| Immutable v2 read/import | core codec/root + portable adapter / existing v2 golden tests | I01 | host determinism / exact bytes, IDs, fixture digests | exact equality | `S03-V01` |
| v3 root/tree/file/segment/chunk/attribution goldens | core identity/codec/tree/attribution / v3 golden tests | I02 | host determinism / type bytes, IDs, bounds | approved exact values | `S03-V02` |
| amd64/arm64/filesystem determinism | core ports + SeqCDC / host-independence vectors | I05 | host/architecture determinism / matrix IDs | all required IDs equal | `S03-V03` |
| wrong kind; trailing; unsorted/duplicate; oversized; dangling; sparse; required capabilities | core codec/validation / `hostile_v3_decode` vector per defect | I03 | resource cell / error, allocation peak | exact typed error; within bound | `S03-V04` |
| derived flat export, never root input | cand tree / flat round trip and zero-counter integration | I04 | 4 KiB edit / flat read-write counters | equality; counters zero | `S03-V05` |
| empty/nested trees | cand publication/tree / candidate publication integration | P01 | first import / tree digest/page counts | exact tree before/after restart | `S03-V06` |
| tiny/large/sparse/zero | capture+SeqCDC+tree / per-shape integration | P02 | first import, 4 KiB edit / `R,E,U,K,P` | exact bytes/metadata; bounded | `S03-V07` |
| raw paths/xattrs/hardlinks/symlinks/devices/FIFOs | workspace capture+core types / capability matrix | P03 | first import / capability and node fields | exact or typed unsupported | `S03-V08` |
| deletion/opaque/rename/truncate/append/metadata | spool/tree/OCC / per-mutation integration | P04 | mutation cells / touched paths/pages | exact final tree; changed-only | `S03-V09` |
| unchanged content/page sharing and changed ancestors only | cand tree / localized update counters | P01–P04 | 4 KiB + mutations / read-write IDs/bytes/scans | unchanged IDs equal; full scans zero | `S03-V10` |
| separate stable attribution and bounded blame | attribution/tree / actor/content/query tests | P05 | attribution cell / content+attribution IDs/query pages | content independent; history scans zero | `S03-V11` |
| clean checkpoint/fork | refs / zero-allocation tests | R01 | clean checkpoint/fork / payload/native-tree bytes | exactly zero | `S03-V12` |
| dirty checkpoint plus one ref; delete ref only | refs/publication / delta tests | R02 | dirty checkpoint / object/page/ref deltas | publication delta + one ref | `S03-V13` |
| checkout no head mutation | refs/session / selection test | R03 | ref diagnostic / head digests | exact no mutation | `S03-V14` |
| revert publication/generation/actor | refs/publication/attribution / revert test | R04 | mutation/ref diagnostic / roots/generation | exact specified semantics | `S03-V15` |
| reset existing pair, no objects | refs / reset test | R05 | ref diagnostic / object deltas | zero new objects; generation advances | `S03-V16` |
| content and attribution survive checkpoint restart; later squash/compaction/GC/delete lifecycle remains explicit | refs / Stage 03 restart test plus later-owner traversal tests | R06 | settled space / both roots and retained reachability | Stage 03 restart exact; real later owners `DEFERRED_STAGE_07` | `S03-V17` |
| exact and directory metadata conflicts | spool/OCC / conflict variants | O01 | same-path conflict / key/work fields | stable conflict, bounded | `S03-V18` |
| ancestor removal vs descendant | spool/OCC / ancestor variant | O01 | same-path conflict / ancestor keys | stable conflict | `S03-V19` |
| rename source/destination overlap | spool/OCC / rename variant | O01 | same-path conflict / group keys | stable conflict | `S03-V20` |
| opaque subtree vs descendant | spool/OCC / opaque variant | O01 | same-path conflict / boundary keys | stable conflict | `S03-V21` |
| hardlink group overlap | spool/OCC / hardlink variant | O01 | same-path conflict / group membership | stable conflict | `S03-V22` |
| disjoint two writers | OCC/rebase / barrier integration | O02 | 2-writer cell / throughput, progress, wait | ≥90% raw; both visible | `S03-V23` |
| disjoint three+ and bounded contention | OCC/rebase / barrier integration | O03 | 3+-writer cell / per-writer retries/time | no starvation; typed bound; <60 s | `S03-V24` |
| branch-scoped ID, mismatch, expiry | operation / journal identity tests | F09 | lost-response matrix / request/outcome digests | exact retry; typed mismatch/expired | `S03-V25` |
| failpoints before state, spill, install, durable roots, prepared | operation/object/spool / phase tests | F01–F05 | failpoint matrix / state/head/residue | old or one result; bounded cleanup | `S03-V26` |
| GC hook, before head, head-terminal gap, lost response | refs/operation / phase tests | F06–F09 | failpoint matrix / ordering/repair/outcome | exact repair/result | `S03-V27` |
| v1 locator/source hold | source/refs / last-location tests | S01 | v1 source-protection cell / lease/fence/protected bytes | durable before ref; survives restart | `S03-V28` |
| hidden comparison, no authority/latency change | publication/observability / on-off tests | S02 | validation diagnostic / route, latency, mismatch | legacy authority; bounded contract | `S03-V29` |

### 11.2 Complexity, resources, `/eos`, benchmark cells, and exit evidence

| Requirement | Implementation / focused test | Typed E2E | Benchmark cell / mandatory artifact | Threshold | Progress |
| --- | --- | --- | --- | --- | --- |
| first import `O(R+E)` bounded | capture/SeqCDC/tree / multi-size trend | P01–P03,B01 | first import / sizes, trend, RSS | credible trend; §5.3 caps | `S03-V30` |
| later `O(U+E_changed+K+P log_B N)` | spool/tree / growing-tree edits | P04,B01 | 4 KiB edit / two+ scales, slopes | no total-tree/history scan; locality gate | `S03-V31` |
| OCC `O(Q log_B N)` fixed cap | OCC / query-size variants | O01–O03 | conflict/disjoint / `Q`, pages, retries | configured count/time bound | `S03-V32` |
| attribution update/query `O(P log_B N)` | attribution / growth/query variants | P05 | attribution / `P,Q`, sharing/query pages | no history scan; bounded output | `S03-V33` |
| no-op zero payload | publication / no-op integration | P01 | no-op / new payload/object deltas | exactly zero new payload | `S03-V34` |
| append/truncate/metadata/delete/rename | tree/publication / per-variant tests | P04 | named mutation cells / inputs/pages | exact and bounded each | `S03-V35` |
| memory/FD/tasks/queues | resource permits/observability / cap tests | B01 | memory/FD/tasks / every peak | §5.3 maxima; zero detached | `S03-V36` |
| settled/peak physical space | storage accounting / accounting fixtures | B01,B02 | settled/peak space / `T` components | totals consistent; missing fails | `S03-V37` |
| staging/locality/metadata budgets | spool/object/tree / size assertions | P02,P04,B01 | edits/space / amplification and per-unit bytes | ≤5%; ≤96/64/256+path; locality rule | `S03-V38` |
| small-edit latency | publication / repeated counterbalanced edits | P04 | 4 KiB edit / raw samples p50/p95/MAD | p95 ≤ baseline×1.15+5 ms with sufficient n | `S03-V39` |
| allowed lazy candidate paths only | all persistence / path-boundary tests | B02 | space/layout / per-boundary path manifest | exact allowed/conditional set | `S03-V40` |
| packs/materializations/gc absent | object/ref storage / negative path tests | B02 | layout / forbidden paths | exactly absent | `S03-V41` |
| legacy/ref-legacy/namespace_execution absent | storage / negative path tests | S01,B02 | layout / forbidden paths | exactly absent | `S03-V42` |
| v1 manifest/workspace/base/layers/staging/metadata authoritative | v1 path / public regression | I01,S02 | compatibility / v1 digests/route | unchanged | `S03-V43` |
| only session `upper` ingested | workspace capture / source-audit tests | B02 | ownership / opened-path ledger | no work/executions/export/storage/runtime read | `S03-V44` |
| `/eos` masked and shell-less/read-only/non-root | public service/security / existing+new tests | B02,B03 | exposure / mount/API observations | masked; exact public behavior | `S03-V45` |
| zero dependency/helper/service/image/network delta | manifests/comparator / graph/source/process audit | B03 | dependency proof / 16 invocation comparisons | exact zero | `S03-V46` |
| complete failpoint matrix | operation / all nine focused tests | F01–F09 | lost-response cell / nine result references | every case passes; representative timed | `S03-V47` |
| every required benchmark cell represented | benchmark adapter/verifier / strict fixtures | B04 | all 14 benchmark-note cells / result status | each `PASS` or honest `NOT_RUN`/deferred | `S03-V48` |
| exact cleanup/quiescence/residue | owners/observability / teardown tests | every case,B04 | settled space / cleanup ledger | zero unowned active state | `S03-V49` |
| required report/artifact fields and append-only history | schema/reporter/verifier / positive+negative fixtures | B04 | all cells / §13.4 | missing/null/inconsistent rejects | `S03-V50` |
| public v1 and `/eos` unchanged | public hook + storage / regression | I01,S02,B02 | compatibility/layout / route/path snapshots | exact unchanged | `S03-V51` |

The benchmark-note cells map as follows: first import `V30`; 4 KiB edit `V31,V39`;
append/truncate/metadata/delete/rename `V35`; no-op `V34`; attribution `V33`;
clean checkpoint/fork `V12`; dirty checkpoint `V13`; same-path conflict `V18`;
2/3+ writers `V23,V24`; failpoint matrix `V26,V27,V47`; v1 source lease `V28`;
memory/FD/tasks `V36`; settled/peak space `V37`; host determinism `V03`.

## 12. Exact future commands and execution order

These commands were checked against the live repository/CLI patterns but were **not
run during authoring**. Commands naming proposed Stage 03 files become runnable only
after those files exist. Before **every** live command, append to
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`:
UTC timestamp, current custody, exact command/intent, run ID, image/binary/config
identity, owned resource IDs/artifact root, and exact cleanup plan. After the command,
append `Run`, `Good`, `Defect`, `Fix/next action`, elapsed times (separating harness
wall time from build lock/image pull/unrelated host contention), artifact digests, and
cleanup/quiescence. Never rewrite a failed attempt. Debug only the failed focused
case; do not rerun passing cases because another failed.

### 12.1 Formatting and narrow static checks

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked \
  -p sandbox-runtime-layerstack-core \
  -p sandbox-runtime-layerstack \
  -p sandbox-runtime-workspace \
  -p sandbox-runtime \
  --all-targets --all-features -- -D warnings
```

### 12.2 Core v2/v3 goldens, hostile decoding, and portability

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo test --locked -p sandbox-runtime-layerstack-core --test canonical_contract
cargo test --locked -p sandbox-runtime-layerstack-core --test canonical_contract canonical_v3
cargo test --locked -p sandbox-runtime-layerstack-core --test hostile_v3_decode
cargo test --locked -p sandbox-runtime-layerstack-core --test host_independence
cargo test --locked -p sandbox-runtime-layerstack --test portable_root_golden
```

`S03-G01` has passed; create `canonical_v3` only from the approved corpus and verify
its manifest digest before use. Architecture matrix invocations must use the exact
owner-approved target/filesystem list and record each invocation separately; do not
substitute cross-compilation for execution.

### 12.3 Focused product slices

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo test --locked -p sandbox-runtime-layerstack --test candidate_publication object_store
cargo test --locked -p sandbox-runtime-layerstack --test candidate_publication seqcdc
cargo test --locked -p sandbox-runtime-workspace --test unit overlay_capture
cargo test --locked -p sandbox-runtime-layerstack --test candidate_publication tree_mutation
cargo test --locked -p sandbox-runtime-layerstack --test candidate_publication refs
cargo test --locked -p sandbox-runtime-layerstack --test candidate_publication operation_recovery
cargo test --locked -p sandbox-runtime-layerstack --test candidate_publication occ
cargo test --locked -p sandbox-runtime-layerstack --test candidate_publication source_hold
cargo test --locked -p sandbox-runtime --test workspace_session_publish
cargo test --locked -p sandbox-runtime --test workspace_session_publish_security
```

Use distinct Rust test-name filters exactly as implemented; a zero-test result is
failure. Never replace a missing focused filter with an all-workspace pass.

### 12.4 Safe typed-catalog collection

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
PYTHONPATH=e2e \
.venv/bin/python -m harness.catalog.collect \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

Collection must show every §10 ID exactly once and every referenced product feature
registered. If retained, output belongs below `.e2e-state/tmp/<run-id>/`. Do not use
the stale README `--ledger` form.

### 12.5 Focused E2E, family by family

Use the pinned image digest from the owner-approved run record. The current inherited
image is shown only as a preflight default and must be reverified:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_incremental_publication.py \
  -k 'test_s03_i' \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

Repeat the same exact command with `-k 'test_s03_p'`, then `test_s03_r`,
`test_s03_o`, each single failed `test_s03_fNN` node, `test_s03_s`, and
`test_s03_b`. Record a distinct run ID/artifact root for each invocation. Request a
rebuild for the first run after product change; reuse only the exact recorded binary
when debugging a failed node. Run the final full Stage 03 module only after every
focused failure is closed.

### 12.6 Benchmark plan validation

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
  --plan layerstack-phase1-stage03-publication \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

### 12.7 Three-minute campaign

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --plan layerstack-phase1-stage03-publication \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

Do not wrap this in a second scheduler. If interrupted, record the attempt before:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark recover \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

`recover` has no `--plan`. Failed attempts/retries consume the campaign in which they
occur. Run exact cleanup only for the owned run ID and only after retention rules:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark cleanup \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin \
  --run-id <exact-run-id>
```

Never use broad Docker/process/filesystem cleanup.

### 12.8 Artifact compatibility/verifier

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.benchmark-state/test-venv/bin/python -m pytest \
  benchmark/backend/tests/compatibility/test_artifacts.py
```

The new strict Stage 03 negative fixtures must prove that missing, `null`,
unsupported, contradictory, or arithmetically inconsistent fields reject.

### 12.9 Exact dependency delta

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.venv/bin/python e2e/tools/verify_external_dependency_delta.py \
  .e2e-state/evidence/stage00-entry-20260724T134437+0800/stage00-entry-baseline.json \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --test-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --output .e2e-state/tmp/<exact-run-id>/dependency-delta-a.json \
  --require-stdlib-crate sandbox-runtime-layerstack-core \
  --require-exact-external-delta-zero
```

Resolve the run-ID placeholder before execution, then repeat the same dynamic capture
to `dependency-delta-b.json`. The live comparator reads the baseline’s complete 16
frozen target/feature invocations and captures each one with locked `cargo tree`; one
invocation of the comparator therefore covers all 16 and must report their identities,
packages, versions, sources, checksums, feature pairs and direct edges. The two
canonical reports must agree exactly. Do not replace them with raw `cargo metadata`,
a glob, or counts alone. At final closure run it again into the retained final
artifact. Separately retain the source/process/network/system-helper/service/image
audit required by `S03-V46`.

### 12.10 Final focused regression and cleanup proof

After focused failures are resolved, run:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo test --locked -p sandbox-runtime-layerstack-core
cargo test --locked -p sandbox-runtime-layerstack
cargo test --locked -p sandbox-runtime-workspace --test unit
cargo test --locked -p sandbox-runtime --test workspace_session_publish
cargo test --locked -p sandbox-runtime --test workspace_session_publish_security

cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=0 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_incremental_publication.py \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

The final artifact must enumerate exact run-owned cleanup, settled observations,
operation/lease residue, retained failed attempts, and all passing focused run IDs.
Do not run a broad Stage 07 matrix as Stage 03 evidence.

## 13. Three-minute focused benchmark E2E campaign

This is implementation evidence, not Stage 07 release qualification. All focused
correctness cases needed by a sampled operation, the complete failpoint matrix, plan
validation, binary/fixture verification, and resource readiness must pass before a
performance verdict is allowed.

### 13.1 Runner boundary and prerequisites

Use one runner-owned monotonic campaign clock:

- prerequisites outside the clock: locked release/prebuilt product and adapter
  binaries; pinned image already present; deterministic approved fixtures already
  generated and digest-verified; benchmark plan validated; run-owned root allocated;
  host load and cache policy recorded;
- separately report the wall time of build locks, builds, image inspection/pull, and
  fixture generation. Candidate and baseline must use the same build/input/cache
  treatment; hidden time may not be charged asymmetrically;
- start `campaign_elapsed_ns` immediately **before** the runner takes the first
  pre-campaign resource/allocated-space sample;
- end it only **after** final settled sampling, strict result/manifest serialization
  and fsync, exact cleanup accounting, quiescence polling, and cleanup-ledger fsync;
- at 150 s stop admitting workload operations and reserve 30 s for settle,
  serialization, cleanup and verification; at 180 s the campaign is `FAIL` if the
  end boundary has not completed. Safety cleanup after a hard overrun is recorded
  separately and cannot convert the campaign to pass;
- every retry/failed attempt after the start consumes this same budget. No individual
  operation receives more than 60 s or more than its cell subdeadline.

The matched baseline is the frozen raw/public-v1 operation already represented by the
live LayerStack Phase 1 baseline adapter/catalog. The candidate performs the same
public workspace mutation/public v1 publication with hidden Stage 03 validation
enabled so the normal private protocol runs while v1 remains the public authority.
The adapter must verify matching logical input/result and must record both operation
IDs; do not add a benchmark-only product protocol.

### 13.2 Deterministic order, samples, and 180-second budget

Fixture sizes and seeds come from the owner-frozen corpus. At minimum the edit arm has
two observably different scales (for example, the corpus’s small and growing-tree
sizes); do not choose substitute numeric sizes before the corpus decision. Use a
seeded counterbalanced `ABBA`/Latin order across baseline (`B`) and candidate (`C`),
with scale order reversed on alternating blocks. One unmeasured warmup per arm is
allowed inside its row budget.

| Deadline window | Budget | Required work and minimum useful samples |
| --- | ---: | --- |
| pre-sample + first import | 20 s | before sample; one warmup then at least 3 measured matched imports at the frozen first-import scale; exact public tree and `O(R+E)` counters |
| no-op | 8 s | at least 1 warmup + 9 measured alternating operations; zero new payload |
| repeated 4 KiB middle edits, two+ scales | 34 s | at least 1 warmup per arm; target 20 measured samples per baseline/candidate/scale for an inferential p95; preserve every raw sample and scale order |
| append/truncate/metadata/delete/rename + attribution | 24 s | every mutation once per arm in counterbalanced order, plus repeated attribution update/query as remaining budget permits |
| clean checkpoint/fork + dirty checkpoint | 16 s | at least 3 repetitions of each clean operation and 3 dirty checkpoint pairs; exact zero/delta accounting |
| same-path conflict + disjoint 2/3-writer progress | 28 s | at least 3 same-path trials, 3 two-writer and 3 three-writer barrier trials, matched raw throughput/control samples |
| representative lost-response restart/retry | 20 s | `F09` head-visible/terminal or terminal-before-response boundary chosen deterministically in preset; restart and exact same-ID result |
| final post-restart/peak/settled samples, artifact fsync, cleanup/quiescence | 30 s | stop admission at 150 s; reconcile `T`, serialize/verify artifacts, exact cleanup and zero-active-state ledger |
| **Total** | **180 s** | hard cap |

The priority on a cell deadline is: retain assertions and cleanup; retain at least one
correctness execution of every mandatory operation; retain two-scale edit evidence;
then maximize counterbalanced repetitions. Never drop an assertion, omit cleanup, or
downsize below observable changed-input/locality behavior to manufacture a pass.
When minimum statistical samples are missed, keep raw results but mark the affected
performance gate `NOT_RUN`/`INSUFFICIENT_SAMPLE` in the artifact; the campaign may
still supply correctness/diagnostic evidence but cannot close that gate.

P95 is inferential only with at least 20 valid measured samples in each compared arm
at a scale. Smaller samples may report a clearly labeled diagnostic order statistic,
not a p95 pass. P99 is always diagnostic in this campaign unless the approved corpus
and sample count independently justify it.

### 13.3 Time, scaling, space, and resource calculations

For every operation/sample record:

- runner and operation monotonic elapsed times, warmup/measured flag, sequence index,
  seed, arm, scale, cache state, worker limits, host load/context;
- raw samples, valid/rejected sample counts, p50, sufficiently sampled p95,
  diagnostic p99 where applicable, median absolute deviation, and throughput;
- baseline and candidate values and literal formulas:
  `candidate_small_edit_p95 <= baseline_p95 * 1.15 + 5 ms` and
  `candidate_disjoint_throughput / raw_baseline_throughput >= 0.90`;
- `R,E,U,E_changed,K,P,N,Q`; bytes read, hashed, written; content/attribution
  object/page read/write counts and bytes; complete-tree/history/flat scan counters;
- lock wait/hold, retry/conflict counts, per-writer completions and progress ratio.

For the two-scale 4 KiB arm, report input-size ratios and elapsed/read/hash/write/page
ratios or fitted slopes with raw points. Any nonzero complete-tree/history scan during
normal incremental publication is immediate failure. Source review cannot replace
these counters.

Sample allocated physical bytes at pre-operation, peak, post-commit, post-restart
where applicable, and settled quiescence. Reconcile:

- loose logical content/attribution objects and conditional last-v1 locator/lease;
- refs;
- operation `STATE` and work/staging;
- LayerStack metadata;
- active workspace `upper` and `work`, reported separately;
- unchanged v1 carriers, reported separately;
- unreachable/unexplained residue;
- `T = Lhot + Hcold + ΣUactive + Pstaging + M`, with no double counting.

Also record new unique payload, changed chunk/page bytes, shared unchanged
payload/pages, peak/settled candidate bytes, staging amplification, bytes per
chunk/segment/changed path, process idle/peak RSS and cgroup available memory,
storage-owned permit bytes, workers/tasks/threads, queue depth, FDs, mappings, lock
wait, first-to-last settled delta, exact operation residue, and lease-protected bytes.
Missing accounting fails the artifact; it is never interpreted as zero.

Required numeric verdicts include:

- ring/window ≤32 KiB; workers ≤4; no payload queue; descriptors ≤16 and ≤64 KiB;
  fan-in ≤8; reader ≤64 KiB; encoder ≤256 KiB; index cache ≤16 MiB; lower depth ≤64;
- per-publication owned metadata/work ≤4 MiB; global owned-storage permits ≤64 MiB;
  RSS ≤384 MiB and ≤128 MiB above measured idle;
- staging ≤5% of captured payload; chunk metadata ≤96 B; segment metadata ≤64 B;
  changed-path metadata ≤256 B plus path bytes;
- clean checkpoint and fork: exactly zero copied payload and zero native-tree
  allocation; no-op: exactly zero new payload;
- localized edit target: changed unique content +64 KiB + one segment page; hard fail
  if median amplification >4× or any sample is `>= 25% × F`;
- zero active workers/tasks/queues/permits and no detached task/strong cycle after
  quiescence; all individual operations <60 s.

### 13.4 Machine artifact and human verdict

The strict machine-readable run must contain, without null-to-zero coercion:

| Artifact group | Mandatory fields |
| --- | --- |
| Identity | exact command, product/test revisions and dirty custody, build/binary/config, algorithm/profile/format and owner-decision ID, host/target/kernel/cgroup, image digest, `/eos` backing filesystem, seed, corpus/fixture digests, run/pair IDs, counterbalanced sample order |
| Clock | prerequisite wall times separately, campaign start/end monotonic values, aggregate elapsed, admission-stop value, per-cell deadlines/elapsed, per-operation elapsed and timeout |
| Time/scaling | warmups/raw sample counts and values, valid/rejected reasons, p50/p95/p99 labels, MAD, throughput, baseline/candidate/formula, scale ratios/slopes, `R,E,U,E_changed,K,P,N,Q` |
| I/O/structure | bytes read/hashed/written, object/page counts and bytes by content/attribution, shared IDs/bytes, complete-tree/history/flat counters |
| Concurrency | lock wait/hold, retries/conflicts, writer count, per-writer completions, progress ratio, raw/candidate throughput |
| Space | allocated pre/peak/post/restart/settled snapshots, every `T` component, unique/shared/staging/metadata/ref/operation/lease/v1/workspace/residue bytes, amplification and locality formulas |
| Resources | idle/peak RSS, cgroup available memory, permits/owned bytes, workers/tasks/threads/queues, FDs, mappings, encoders/cache, detached/strong-cycle/quiescence fields |
| Recovery/cleanup | failpoint ID, state/head/outcome digests, restart result, exact owned resource IDs, cleanup actions/results, retained terminal/lease/orphan facts, unexplained residue |
| Verdict | threshold, measured value, sample sufficiency, `PASS`/`FAIL`/`NOT_RUN`/`DEFERRED_STAGE_07`, variance or unavailability reason, raw artifact paths and SHA-256 digests |

The verifier must reject absent mandatory fields, unresolved fixture digests,
inconsistent component totals, invalid sample ordering, mismatched public input/result,
unsupported values presented as zero, a cleanup boundary after 180 s, or a performance
pass without sample sufficiency.

After verification, update [`benchmark_note.md`](benchmark_note.md) with the exact
command/revision/profile/corpus/host, raw artifact paths/digests, sample summaries,
complexity variables, counters/accounting, thresholds, verdicts, and variance.
Unmeasured required cells remain `NOT_RUN`; later qualification remains
`DEFERRED_STAGE_07`. Do not overwrite its initial history or call expected
incrementality a result.

## 14. Copy-ready prompt for the future implementation agent

Use the following prompt only after handing the agent the three live repositories.
It intentionally delegates no authority to invent the v3 contract:

```text
# Mission: implement and verify the full Stage 03 private-publication slice

Implement Stage 03, “corrected identity and complete private publication,” by
following this execution guide from first line through EOF:

/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_03_incremental_publication/implementation_instructions.md

Work in:
- product: /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
- test/E2E and benchmark: /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
- docs: /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs

Required working method:

1. Read the guide and every source in its reading ledger through EOF. Re-run the
   custody/preflight commands and preserve every pre-existing dirty/untracked change.
   Do not reset, stash, clean, restore, switch branches, or absorb another owner's
   edits.
2. Apply the authority order in §0.1. First resolve `S03-G01`: locate a recorded,
   approved owner amendment that closes every v3 record/type/field/tag/domain/bound,
   ActorId, compatibility rule, and benchmark-corpus item in §5.2. D2.5 is v2-only.
   If no complete approval exists, stop product/v3/golden/persistence work, mark the
   tracker `BLOCKED`, and return the exact owner-decision request. Never invent or
   infer wire values.
3. Once all entry gates pass, implement §7 in dependency order and use the real file
   seams in §6. Keep layerstack-core safe/std-only and preserve v2 bytes/import.
   Reuse LayerStack's existing SHA-256 and durable filesystem helpers. Add no external
   dependency, system/target helper, service, network dependency, unsafe path,
   alternate harness, public candidate authority, pack/materialization/GC feature,
   legacy mapping, or empty future directory.
4. Preserve public v1 read/write/publication authority. The private candidate must use
   the normal branch-scoped idempotent protocol. Capture only the admitted session's
   `upper`; keep expensive capture/hash/sort/page/conflict work outside the short
   writer-lock commit section. Enforce every resource, locality, latency,
   concurrency, operation and physical-accounting bound in §§5 and 13.
5. Before every live test/benchmark command, append the planned command, intent,
   custody, image/binary/config, run ID, owned resources/artifact root and cleanup
   plan to e2e/test-report.md. Afterward append Run/Good/Defect/Fix-next, elapsed,
   artifacts/digests and cleanup. Reports are append-only. Rerun only failed focused
   cases while debugging; retain failed attempts; never use broad cleanup.
6. Execute the exact focused order in §12: format/static checks; core v2/v3/hostile/
   portability tests; each product slice; safe typed-catalog collection; each typed
   E2E family and all nine failpoints; benchmark plan validation; the §13 runner-owned
   180-second campaign; strict artifact verification; all 16 exact dependency
   comparisons; final focused regression and cleanup/quiescence proof.
7. Public workspace/file behavior is the correctness oracle. Inspect private `/eos`
   only for independent layout, allocated-space, durability, failpoint and residue
   evidence. Do not convert inspection, planned tests, missing/null counters, or
   inadequate samples into a pass.
8. Maintain only the canonical tracker in §15.2 using its closed vocabulary. Update
   each row with the exact command/evidence ID, run/artifact path and SHA-256, owner/
   blocker, cleanup, and UTC timestamp. Check §15.1 only when the linked verification
   row and mandatory artifact directly pass.
9. Complete every mandatory Stage 03 implementation, typed E2E, `/eos`, recovery,
   resource, dependency, artifact and three-minute campaign item. Leave the explicit
   Stage 07 matrix deferred; do not weaken or approximate it.
10. Finish by filling the §15.5 handoff template. Report `POC PASS` only if every
    mandatory non-deferred Stage 03 row has retained direct evidence. Otherwise
    report `POC FAIL / BLOCKED` with exact open rows and artifacts. Do not call Stage
    03 complete because it compiles, looks incremental, has one favorable benchmark,
    or passes a broad suite.

Continue until the full authorized Stage 03 slice is implemented and verified or a
genuine owner/external blocker is reached. Do not implement beyond Stage 03 scope.
```

## 15. Completion and handoff

### 15.1 Evidence-backed completion checklist

Every unchecked item is open. The parenthetical references name the canonical
progress row and verification row(s).

- [x] Complete v3 owner amendment and frozen corpus are approved; current custody,
  environment, disk, harness, cleanup and dependency entry gates pass
  (`S03-G01–S03-G10`; `S03-V01–V05`).
- [x] Immutable v2 read/import bytes and all owner-approved v3 typed goldens,
  host-independence and hostile decoder bounds pass (`S03-E01`; `S03-V01–V05`).
- [x] Deterministic scalar SeqCDC, typed loose put-if-absent, bounded raw-byte
  capture/order, persistent page mutation and structural sharing pass
  (`S03-I02–S03-I04`, `S03-E02`; `S03-V06–V11,V30–V35`).
- [x] Private refs, clean/dirty checkpoints, fork/pin, checkout, revert, reset and
  checkpoint deletion meet exact cost and attribution semantics
  (`S03-I05,S03-I08,S03-E03`; `S03-V12–V17`).
- [x] Branch-scoped operations, exact retry/mismatch/expiry, all nine crash boundaries,
  head/terminal repair and bounded residue pass (`S03-I06,S03-E05`;
  `S03-V25–V27,V47,V49`).
- [x] Exact/ancestor/rename/opaque/hardlink conflicts and bounded two/three-writer
  disjoint rebase/progress pass (`S03-I07,S03-E04`; `S03-V18–V24,V32`).
- [x] Conditional last-v1-carrier locator/source hold and hidden normal-protocol
  validation pass without `refs/legacy` or public-authority change
  (`S03-I09,S03-I10,S03-E06`; `S03-V28,V29,V42,V51`).
- [x] The complete `/eos` allowed/conditional/forbidden map passes at setup, active,
  post-commit, restart, failure, ref deletion, teardown and settled boundaries;
  workloads see `/eos` masked and only admitted `upper` is captured
  (`S03-L01,S03-E07`; `S03-V40–V45,V51`).
- [x] First import, no-op, two-scale 4 KiB edits, every required mutation,
  attribution, refs, conflict/disjoint writers, one lost-response restart, and
  before/peak/settled/cleanup cells complete inside the runner-owned 180 s campaign
  with honest sample sufficiency (`S03-B01`; `S03-V30–V39,V47–V50`).
- [x] RSS, permits/owned bytes, workers/tasks/threads, queues, FDs, mappings,
  readers/encoders/cache, retries, staging, metadata and operation-residue bounds pass;
  quiescence proves zero detached tasks/strong cycles (`S03-R01`; `S03-V36–V38,V49`).
- [x] Exact external dependency/feature/edge, system/helper/service/image/network delta
  is zero across all frozen invocations and portable core remains safe/std-only
  (`S03-D01`; `S03-V03,V46`).
- [x] Strict artifact schema/verifier rejects missing/null/inconsistent fields;
  append-only report contains planned and actual commands, retained failures, exact
  artifacts/digests and run-owned cleanup (`S03-A01`; `S03-V48–V50`).
- [x] Focused final v1 compatibility/public-authority regression passes and all
  mandatory non-deferred tracker rows contain direct retained evidence
  (`S03-E08,S03-H01`; `S03-V43,V45,V50,V51`).
- [x] Stage 07-only qualification remains explicitly deferred rather than compressed
  into Stage 03 (`S03-Q07`; `S03-V17,V48`).

### 15.2 Canonical progress tracker

Initialize and maintain this table in place. `—` means no Stage 03 artifact exists,
not a zero-valued result. Timestamps are UTC.

| Work ID | Depends on | Deliverable | Current status | Completion condition / exact verification | Run/artifact path and digest | Owner/blocker | Cleanup result | Last updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S03-G01` | — | Complete owner-approved v3 amendment and frozen corpus | `PASS` | Approved decision closes every §5.2 row; decision ID and fixture manifest SHA-256 retained | [`contract_v3_owner_decision_g01_1.md`](contract_v3_owner_decision_g01_1.md), decision `PRC-STAGE03-OWNER-DECISION-G01.1`, SHA-256 `27264ef96f97960757eeba0b51bb7d2560446466cbf8e6a11c99a881da834e16`; [`stage03_v3_owner_corpus_v1.json`](stage03_v3_owner_corpus_v1.json), SHA-256 `7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be`; [`gate_resolution_approval_20260725_04.md`](gate_resolution_approval_20260725_04.md), SHA-256 `49ea0a740462ce2652d5a4c4f21f595a44a56af25c0b7222dff3149a63a5f849`; earlier blocker audits retained | User approval mapped without Stage 03 spec drift | N/A | 2026-07-24T22:04:16Z |
| `S03-G02` | — | Verify retained Stage 00–02 evidence | `PASS` | Recompute every complete §0.5 digest and reconcile report/artifact references | [`stage03_entry_evidence_20260725.md`](stage03_entry_evidence_20260725.md), SHA-256 `a7daa2be2bdca8605f35eb405b8bd43b800d18febecf46f9cf9b4c0f28075329` | All mandatory retained identities verified | N/A | 2026-07-24T22:16:53Z |
| `S03-G03` | G02 | Fresh public-v1 sole-authority baseline | `PASS` | Fresh packaged PRC-01 route/layout evidence before implementation | Run `20260724T221647.648307Z-52067`; summary SHA-256 `de5fee5ea1d5f2a25ca324d48df45815cfe4fdbc9a7f2458f19ef7efde6447d6`; [`stage03_entry_environment_20260725.md`](stage03_entry_environment_20260725.md), SHA-256 `934956160f9016c741622d17e901ebbb028ba575684dfb04c10cea8ae16c96aa` | Public v1 sole authority; candidate state absent/zero | Exact registered sandbox destroyed; immutable bundle retained | 2026-07-24T22:16:53Z |
| `S03-G04` | — | Accept live shared-worktree custody | `PASS` | §0.4 commands; explicit owner for every overlapping dirty file | [`gate_resolution_20260725.md`](gate_resolution_20260725.md), SHA-256 `c4951f4599bb92383c877ec6b634b2b1f6f455f64ef89462f1faae062fa906c5`; refreshed in [`stage03_entry_environment_20260725.md`](stage03_entry_environment_20260725.md), SHA-256 `934956160f9016c741622d17e901ebbb028ba575684dfb04c10cea8ae16c96aa` | All dirty paths are task-owned; product/test remain at recorded upstreams | N/A | 2026-07-24T22:16:53Z |
| `S03-G05` | G02,G04 | Freeze exact dependency entry | `PASS` | Two agreeing captures for all 16 invocation IDs | Entry captures A/B, each SHA-256 `1c77ccb2048f4c7383b0bbe6b45f5c999a88e79bcd2ef86ac2650d503e52be1d`; environment record SHA-256 `934956160f9016c741622d17e901ebbb028ba575684dfb04c10cea8ae16c96aa` | Exact zero external dependency delta | Exact temp captures retained until final comparison | 2026-07-24T22:16:53Z |
| `S03-G06` | G04 | Toolchain/E2E/benchmark harness readiness | `PASS` | Locked tools, catalog collection and CLI help/validation without network install | [`stage03_entry_environment_20260725.md`](stage03_entry_environment_20260725.md), SHA-256 `934956160f9016c741622d17e901ebbb028ba575684dfb04c10cea8ae16c96aa` | Rust/Cargo, test/benchmark venvs, 643-case catalog ready | No runtime resource created | 2026-07-24T22:16:53Z |
| `S03-G07` | G04 | Pin host/target/fs/cgroup/image/binary/config | `PASS` | Identity manifest retained; per-run measured identities remain mandatory | [`stage03_entry_environment_20260725.md`](stage03_entry_environment_20260725.md), SHA-256 `934956160f9016c741622d17e901ebbb028ba575684dfb04c10cea8ae16c96aa` | Entry implementation identity fixed; rebuild/hash again for measured runs | N/A | 2026-07-24T22:16:53Z |
| `S03-G08` | G07 | Disk/inode/RSS headroom | `PASS` | Allocated/free/cgroup baseline proves safe observable limits; warmed-idle recheck before campaign | [`stage03_entry_environment_20260725.md`](stage03_entry_environment_20260725.md), SHA-256 `934956160f9016c741622d17e901ebbb028ba575684dfb04c10cea8ae16c96aa` | 384 MiB cap observable; environment headroom exceeds 128 MiB | N/A | 2026-07-24T22:16:53Z |
| `S03-G09` | G01,G06–G08 | Strict benchmark plan/verifier ready | `PASS` | §12.6 validate + strict positive/negative tests | Canonical validation PASS; focused runner/strict-artifact/dispatch 22/22 PASS; plan SHA-256 `5511812675ab2f6784b39b701a333200391e51d6e87e870906d0c454d308d8d6`; final run `019f977b-752d-7868-927d-170b8d46a078` | No blocker | Runner-owned final campaign completed under 180 s | 2026-07-25T04:27:25Z |
| `S03-G10` | G04,G06 | Append-only report and exact cleanup plan ready | `PASS` | Pre-run report entry and run-owned IDs/artifact root exist | `e2e/test-report.md` through terminal closure; environment record SHA-256 `934956160f9016c741622d17e901ebbb028ba575684dfb04c10cea8ae16c96aa` | Append-only discipline preserved every failed attempt and fix | Exact comparator temp dirs and generated product binaries removed after final evidence retention | 2026-07-25T04:27:25Z |
| `S03-I01` | G01,G04,G05 | Approved v3 codecs and hostile bounds | `PASS` | §12.2; V01–V05 | Product tests: `canonical_contract` 9/9, focused `canonical_v3` 2/2, `hostile_v3_decode` 3/3, `host_independence` 3/3, `portable_root_golden` 3 passed/1 benchmark ignored; `e2e/test-report.md` Stage 03 Iterations 004–007; approved corpus SHA-256 `7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be` | Exact 16-record corpus, typed domains/errors, hostile bounds, SHA-256 adapter, and v1 compatibility green | No runtime resource created; only ordinary Cargo cache | 2026-07-24T22:43:53Z |
| `S03-I02` | I01 | Typed loose object store | `PASS` | §12.3 object-store filter; V02,V04 | Product `candidate_publication object_store` 3/3 PASS and canonical four-package clippy PASS; `e2e/test-report.md` Stage 03 Iterations 008–009 | Deterministic typed put-if-absent, bounded verified reuse/collision rejection, lazy durable prefixes, and six crash-boundary retries green | All exact temporary object roots removed; only ordinary Cargo cache remains | 2026-07-24T22:49:55Z |
| `S03-I03` | I01,I02 | Bounded capture/order/SeqCDC | `PASS` | §12.3 SeqCDC/capture filters; V07–V10,V30,V31 | Product `candidate_publication seqcdc` 5/5 PASS, workspace `unit overlay_capture` 6/6 PASS on the pinned host with Linux-only raw/xattr cases retained, and canonical four-package clippy PASS; `e2e/test-report.md` Stage 03 Iterations 010–015; Prep-03 oracle `8e2697cbf6332ac5da6dc615bfab82a720e820e4` | Exact author boundaries, 32 KiB/two-slice ring, direct typed CAS delivery, raw candidate stream, hardlink/kind evidence, external last-writer dedup, fan-in 8, and cap counters green | All exact object/spool/workspace roots removed; only ordinary Cargo cache remains | 2026-07-24T23:07:40Z |
| `S03-I04` | I01–I03 | Persistent content/attribution pages and flat export | `PASS` | §12.3 tree filter; V05–V11,V31,V33 | Product `candidate_publication tree_mutation` 3/3 PASS and canonical four-package clippy PASS; exact approved eight-object corpus IDs; `e2e/test-report.md` Stage 03 Iterations 016–018 | Multi-page content/segment/attribution persistence, changed-leaf-and-ancestor COW sharing, restart reconstruction, separate bounded blame, and diagnostic-only flat export green; normal complete-tree/flat/history counters zero | All exact temporary loose-object roots removed; only ordinary Cargo cache remains | 2026-07-24T23:22:35Z |
| `S03-I05` | I02,I04 | Atomic refs/short commit/GC hook | `PASS` | §12.3 refs filter; V12–V17 | Product `candidate_publication refs` 3/3 PASS after bounded lease-read augmentation and canonical four-package clippy PASS; `e2e/test-report.md` Stage 03 Iterations 019–025 | Checksummed atomic heads, exact generation fencing, O(1) checkpoint/fork/pin/lease refs, restart reconstruction, preparation outside the lock, GC barrier before visibility, and zero payload/native writes green | All exact temporary ref/object roots removed; only ordinary Cargo cache remains | 2026-07-24T23:38:36Z |
| `S03-I06` | I02,I04,I05 | Durable operation/recovery/exact retry | `PASS` | §12.3 recovery filter; V25–V27 | Product `candidate_publication operation_recovery` 3/3 PASS and canonical four-package clippy PASS; exact approved 301-byte operation-state golden; `e2e/test-report.md` Stage 03 Iterations 026–028 | Branch-scoped IDs, request-digest fencing, bounded prepared/terminal states, all F01–F09 old-or-complete boundaries, F08 restart repair, F09 exact lost-response retry, permanent expiry/ack tombstones, 1024-state recovery batches, and eight-attempt/60-second typed bounds green | All exact operation/ref/object and 1025-directory batch roots removed; only ordinary Cargo cache remains | 2026-07-24T23:52:14Z |
| `S03-I07` | I03,I04,I06 | Semantic OCC and bounded rebase | `PASS` | §12.3 OCC filter; V18–V24,V32 | Product `candidate_publication occ` 4/4 PASS after the typed `CommitRequest` arity correction and canonical four-package clippy PASS; `e2e/test-report.md` Stage 03 Iterations 029–031 | Exact/metadata/ancestor/remove/rename/opaque/hardlink overlaps, stable terminal conflict, bounded base/current path-prefix probes, two- and three-writer merged visibility, and typed terminal attempt-nine contention green; one key buffered and zero flat/full-tree scans | All exact temporary object/ref/operation/spool roots removed; only ordinary Cargo cache remains | 2026-07-25T00:03:35Z |
| `S03-I08` | I05–I07 | Complete ref operations | `PASS` | refs/publication focused tests; V12–V17 | Product `candidate_publication ref_operations` 4/4 PASS and canonical four-package clippy PASS; `e2e/test-report.md` Stage 03 Iterations 032–033 | Clean checkpoint and explicit fork/pin choice are constant metadata; checkout preserves head bytes; dirty checkpoint is publication plus one ref with exact retry; revert proves bounded actor attribution; reset returns its typed outcome and advances generation with zero objects; delete/restart preserve both roots | All exact temporary object/ref/operation roots removed; only ordinary Cargo cache remains | 2026-07-25T00:11:35Z |
| `S03-I09` | I02,I05,I06 | Conditional v1 source protection | `PASS` | §12.3 source-hold filter; V28 | Product `candidate_publication source_hold` 3/3 PASS and canonical four-package clippy PASS; `e2e/test-report.md` Stage 03 Iterations 034–036 | Stable catalog-ID lookup verifies raw and typed identity; fenced durable lease survives restart, blocks cleanup with exact bytes, fails closed on locator/catalog drift, releases exactly; all-loose creates none | All exact temporary carrier/locator/lease/object roots removed; only ordinary Cargo cache remains | 2026-07-25T00:23:00Z |
| `S03-I10` | I01–I09 | Hidden normal-protocol validation | `PASS` | hidden on/off product tests; V29,V51 | Product `workspace_session_publish` focused S03-S02 1/1 PASS, canonical target 16/16 PASS after ledger-synchronized test cleanup, and canonical four-package clippy PASS; `e2e/test-report.md` Stage 03 Iterations 037–042 | Normal private branch-scoped publication advances a durable head; bounded matched/mismatch correlation, queue-saturation fallback, restart/off-mode, source-lease, zero-resource, unchanged v1 bytes/authority, and non-blocking public publish assertions green | Exact temporary roots removed; owned workers joined; source leases, tasks, queue bytes/items, and permits drained; only ordinary Cargo cache remains | 2026-07-25T00:50:36Z |
| `S03-I11` | I01–I10 | Observability/failpoints/E2E/benchmark/docs closure | `PASS` | §12.4–12.10; V36–V51 | Full typed E2E 34/34; runner surface 22/22; canonical run `019f977b-752d-7868-927d-170b8d46a078`; artifact compatibility 22/22; dependency/audit/docs evidence retained | No blocker | Zero campaign-owned live resources; exact final local cleanup PASS | 2026-07-25T04:27:25Z |
| `S03-E01` | I01,I11 | Identity/codec/flat/portability typed family | `PASS` | §12.5 `test_s03_i`; IDs I01–I05; V01–V05 | I01–I05 5/5 within complete 34/34 typed E2E run; `e2e/test-report.md` Iteration 175 | No blocker | Exact case-owned sandboxes destroyed | 2026-07-25T04:27:25Z |
| `S03-E02` | I02–I04,I11 | Publication/file-kind/attribution typed family | `PASS` | §12.5 `test_s03_p`; P01–P05; V06–V11 | P01–P05 5/5 within complete 34/34 typed E2E run; `e2e/test-report.md` Iteration 175 | No blocker | Exact case-owned sandboxes destroyed | 2026-07-25T04:27:25Z |
| `S03-E03` | I05,I08,I11 | Ref-semantics typed family | `PASS` | §12.5 `test_s03_r`; R01–R06; V12–V17 | R01–R06 6/6 within complete 34/34 typed E2E run; `e2e/test-report.md` Iteration 175 | No blocker | Exact case-owned sandboxes destroyed | 2026-07-25T04:27:25Z |
| `S03-E04` | I07,I11 | OCC/progress typed family | `PASS` | §12.5 `test_s03_o`; O01–O03; V18–V24 | O01–O03 3/3 within complete 34/34 typed E2E run; private probe retains typed conflict and two-/three-writer progress | No blocker | Exact case-owned sandboxes destroyed | 2026-07-25T04:27:25Z |
| `S03-E05` | I06,I11 | Nine failpoint/idempotency typed cases | `PASS` | Each §10 F01–F09 node; V25–V27,V47 | F01–F09 9/9 within complete 34/34 typed E2E run; private probe recovery result old-or-one-complete | No blocker | Temporary artifacts reaped; exact case-owned sandboxes destroyed | 2026-07-25T04:27:25Z |
| `S03-E06` | I09,I10,I11 | v1 source safety/validation family | `PASS` | §12.5 `test_s03_s`; S01–S02; V28,V29 | S01–S02 2/2 within complete 34/34 typed E2E run; settled active workers zero | No blocker | Source leases/tasks/queues/permits drained; sandboxes destroyed | 2026-07-25T04:27:25Z |
| `S03-E07` | I11 | Resource/exposure/ownership typed family | `PASS` | §12.5 `test_s03_b`; B01–B03; V36–V46 | B01–B03 3/3 within complete 34/34 typed E2E run; dependency/portability audit SHA-256 `a475ad7a23999ee4a231c08d40677186498bddcaf5b44d4e2fbf8683eaa386f7` | No blocker | Zero owned live residue; unrelated gateways untouched | 2026-07-25T04:27:25Z |
| `S03-E08` | E01–E07,B01,D01,L01,R01,A01 | Exit-evidence completeness and final focused regression | `PASS` | B04 plus §12.10; V48–V51 | B04 1/1 in complete E2E run; final product regressions PASS; artifact compatibility 22/22; final strict artifact SHA-256 `e8d7426a22ae22680f0c1597d8dcbfd5d9814539e33aa85287efe23be44ff334` | No blocker | Final exact generated-binary/temp-capture cleanup PASS | 2026-07-25T04:27:25Z |
| `S03-B01` | G09,E01–E07 | Runner-owned 180 s campaign | `PASS` | §12.7 and §13; strict campaign artifact | Run `019f977b-752d-7868-927d-170b8d46a078`; 137.27 s; overall/correctness PASS; strict evidence SHA-256 `e8d7426a22ae22680f0c1597d8dcbfd5d9814539e33aa85287efe23be44ff334`; [`benchmark_note.md`](benchmark_note.md) SHA-256 `8b775f3ed998132a72b451034b8d8e529fd427cfbfcd7bedd8a06bd84219778f` | Performance remains honestly `NOT_RUN/INSUFFICIENT_SAMPLE`, not a Stage 03 blocker | All four arms destroyed/retired/closed; zero live campaign resource | 2026-07-25T04:27:25Z |
| `S03-D01` | G05,I11 | Zero dependency/helper/service/image/network delta | `PASS` | §12.9 all 16 invocations + audit; V46 | Six byte-identical captures SHA-256 `1c77ccb2048f4c7383b0bbe6b45f5c999a88e79bcd2ef86ac2650d503e52be1d`; [`stage03_dependency_portability_audit_20260725.md`](stage03_dependency_portability_audit_20260725.md) SHA-256 `a475ad7a23999ee4a231c08d40677186498bddcaf5b44d4e2fbf8683eaa386f7` | No blocker; approved internal manifest delta only | Exact temporary captures removed after retention | 2026-07-25T04:27:25Z |
| `S03-L01` | I02,I05,I06,I09,E07 | Complete `/eos` boundary proof | `PASS` | B02 path manifests; V40–V45,V51 | Typed B02/B03/B04 all PASS within complete E2E run; setup/active/commit/restart/failure/delete/teardown/settled and public masking retained | No blocker | All exact case roots removed; future-stage paths absent | 2026-07-25T04:27:25Z |
| `S03-R01` | I03–I11,E07,B01 | Resource reclamation/quiescence | `PASS` | B01/B04/campaign cleanup; V36–V38,V49 | Strict artifact reports zero active owned resources, detached tasks, strong cycles, route failures, and unexplained residue; cleanup ledger SHA-256 `7cf3607f4a9fb329651ef577393507130c74ba6103cb9a32aa8e1a26069d2059` | No blocker | Independent process/container/listener/runtime inventory clean | 2026-07-25T04:27:25Z |
| `S03-A01` | I11,E01–E07,B01 | Strict schemas/artifact verification/append-only report | `PASS` | §12.8 + B04; V48–V50 | Focused runner/strict fixtures 22/22; full artifact compatibility 22/22; final report SHA-256 `fd919bddc80e50f5c45a26b5b22b476b14aea77e9346df9c76c27ffeffd2ae53`; append-only test report through terminal closure | No blocker | Immutable result bundle retained; transient owned resources removed | 2026-07-25T04:27:25Z |
| `S03-DOC01` | — | This implementation guide and closure documents | `PASS` | Final whitespace, checklist/tracker, link, fence, artifact and immutable-document digest checks | This guide (external SHA-256 recorded after final write); benchmark note SHA-256 `8b775f3ed998132a72b451034b8d8e529fd427cfbfcd7bedd8a06bd84219778f`; audit SHA-256 `a475ad7a23999ee4a231c08d40677186498bddcaf5b44d4e2fbf8683eaa386f7`; handoff SHA-256 `471fc5b65a167755b5620f43429e6efc59794fb250f074789c19cf7ef4bf9954` | No blocker | Documentation checks create no runtime resource | 2026-07-25T04:27:25Z |
| `S03-Q07` | — | Full release qualification matrix | `DEFERRED_STAGE_07` | §15.4 only; no Stage 03 pass claim | — | Stage 07 owner | N/A | 2026-07-25 |
| `S03-H01` | E08,B01,D01,L01,R01,A01 | Final evidence-backed handoff | `PASS` | §15.5 and Stage 04 handoff contain every authority/run/custody/evidence/cleanup/deferral fact | Final §15.5 record; [`handoff_to_stage_04.md`](handoff_to_stage_04.md) SHA-256 `471fc5b65a167755b5620f43429e6efc59794fb250f074789c19cf7ef4bf9954`; prior blocked audits retained as history | No open mandatory Stage 03 row | No owned live resource; exact final local cleanup PASS | 2026-07-25T04:27:25Z |

### 15.3 Hard blockers

| Blocker | Affected work | Exact resolution required | Owner/status |
| --- | --- | --- | --- |
| Resolved owner gate (`S03-G01`) | No remaining blocked work | Decision `PRC-STAGE03-OWNER-DECISION-G01.1` closes §5.2 and freezes immutable corpus SHA-256 `7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be` | User-approved; `PASS` |
| Requested Stage 03 incoming handoff path is missing from the current branch (`S03-C01`) | Source ledger only | Use the live Stage 02 outgoing handoff; retained remote-ref incoming handoff was inspected and also blocks implementation | Docs owner; stale path reconciled |
| Guide-authoring custody differs from fresh repository custody | Contract/prompt custody | Fresh complete custody captured in the gate artifact; no pre-existing dirty/untracked files found | Repository owners; `PASS` |
| Later compaction/squash/GC/materialization owners do not exist in Stage 03 | Cross-stage survival qualification | Run the real retained-root matrix when Stages 04–07 implementations exist | Stage 04–07 owners; `DEFERRED_STAGE_07` |

### 15.4 Explicit Stage 07 deferrals

These do not excuse any focused Stage 03 gate:

- the full required host/filesystem/architecture qualification beyond Stage 03’s
  approved portability cases;
- the full 64/256/1024 MiB × 1/16/64-root RSS matrix;
- the full five-minute matched candidate/baseline allowance and three-invocation
  selection-advantage decision;
- exhaustive corpus, long-duration soak, restart storm and release variance matrix;
- real Stage 04 materialization/activation behavior;
- real Stage 05 packs, locator compaction, GC, squash and destructive retention;
- Stage 06 public authority/cutover/fallback and Stage 07 retirement;
- end-to-end attribution/checkpoint survival through those real later-stage
  destructive operations.

Keep these rows `DEFERRED_STAGE_07`, not `PASS`, until their owning implementations
and retained artifacts exist.

### 15.5 Self-contained final handoff

```text
# Retained interim Stage 03 handoff (superseded by the final record below)

Historical verdict: POC FAIL / BLOCKED
Interim state at (UTC): 2026-07-24T22:04:16Z

## Authority and scope
- Owner decision ID / approval artifact / SHA-256:
  PRC-STAGE03-OWNER-DECISION-G01.1 /
  contract_v3_owner_decision_g01_1.md /
  27264ef96f97960757eeba0b51bb7d2560446466cbf8e6a11c99a881da834e16.
- Approval mapping artifact / SHA-256:
  gate_resolution_approval_20260725_04.md /
  49ea0a740462ce2652d5a4c4f21f595a44a56af25c0b7222dff3149a63a5f849.
- v3 format version and complete approved corpus manifest SHA-256: 3 /
  7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be.
- Confirmation D2.5 remained v2-only: YES. PRC-STAGE02-OWNER-DECISION-D2.5 was
  inspected and grants no v3 authority.
- Public authority: LegacyV1. This is the retained authority state; no fresh live
  Stage 03 regression was authorized or run.
- Stage 07 qualification status: DEFERRED_STAGE_07.

## Git custody
- Product branch / HEAD / upstream / complete status: upgrade-2.0-phase-1 /
  cbe45de873cd24fbf48bb7b3a6c5f9f98980313c / same / clean.
- Test+benchmark branch / HEAD / upstream / complete status:
  upgrade-2.0-phase-1 / 173191e8694515af43797128070dbdfd2d246040 / same /
  clean.
- Docs branch / HEAD / upstream / complete status: layerstack_2_0 /
  901d6d2181d0795eaaf174a23636a38019aab9a1 /
  426b6be3284c26a59eb77d39ad6622997e8479c9 / ahead 2; task changes are
  this guide, the three retained blocker audits, the approved decision, immutable
  corpus manifest, and gate-resolution approval audit.
- Files changed by repository: product NONE; test+benchmark NONE; docs
  implementation_instructions.md plus the gate/decision/corpus artifacts above.
- Pre-existing dirty/untracked files preserved and owner: NONE found at fresh
  pre-mutation custody capture.

## Focused product evidence
- S03-I01 ... S03-I11 command/result/artifact/SHA-256: NOT_RUN while remaining
  entry gates are closed and dependencies are captured.
- Immutable v2 bytes/IDs and approved v3 bytes/IDs: retained v2 evidence was not
  mutated; fourteen approved v3 byte/ID goldens are frozen in the corpus manifest.
- Portable-core safe/std-only and dependency direction: repository instructions were
  inspected; no Stage 03 implementation exists to verify.

## Typed E2E evidence
- S03-E01 IDs I01–I05 / run IDs / verdicts / artifacts: BLOCKED; none run.
- S03-E02 IDs P01–P05 / run IDs / verdicts / artifacts: BLOCKED; none run.
- S03-E03 IDs R01–R06 / run IDs / verdicts / artifacts: BLOCKED; none run.
- S03-E04 IDs O01–O03 / run IDs / verdicts / artifacts: BLOCKED; none run.
- S03-E05 IDs F01–F09 / run IDs / verdicts / artifacts: BLOCKED; none run.
- S03-E06 IDs S01–S02 / run IDs / verdicts / artifacts: BLOCKED; none run.
- S03-E07 IDs B01–B03 / run IDs / verdicts / artifacts: BLOCKED; none run.
- S03-E08 ID B04/final regression / run IDs / verdict/artifacts: BLOCKED; none run.

## Three-minute campaign
- Exact command / run and pair IDs: NOT_RUN; candidate implementation does not yet
  exist.
- Runner clock start/end / aggregate seconds (must be <=180): NOT_RUN.
- Budget rows actual seconds: NOT_RUN.
- Fixture/seed/order are frozen in the approved corpus; prerequisite times are
  NOT_RUN.
- Baseline/candidate samples and sufficiency: NOT_RUN.
- Time/scaling/locality verdicts: BLOCKED.
- Raw artifact paths and SHA-256: NONE.

## Required evidence summaries
- Time and R,E,U,E_changed,K,P,N,Q: NOT_RUN.
- Space and reconciled T components: NOT_RUN.
- RSS/permits/workers/tasks/threads/queues/FDs/mappings: NOT_RUN.
- Concurrency/lock/retry/conflict/progress: NOT_RUN.
- Failpoint/restart/exact retry: NOT_RUN.
- V1 locator/source hold and protected bytes: NOT_RUN; no candidate paths created.
- /eos setup/active/commit/restart/failure/delete/teardown/settled: NOT_RUN.
- Public-v1 behavior, authority and masking: retained LegacyV1 authority; fresh
  behavior/masking evidence NOT_RUN.
- Exact external dependency/feature/edge delta: NOT_RUN; no implementation delta.
- System/helper/service/image/network and portability proof: NOT_RUN.

## Artifacts, cleanup, and history
- Strict schema/verifier result: NOT_RUN; the Stage 03 corpus is approved.
- Append-only test-report entry references: NONE; the report was not changed because
  no live test/benchmark command has run since approval.
- Exact cleanup/quiescence result: no Docker/E2E/benchmark/product runtime resources
  were created; runtime cleanup and quiescence were therefore not exercised.
- Retained terminal/lease/orphan facts: no Stage 03 terminal, lease, or orphan state
  was created.
- Retained failed attempt IDs/artifacts: no execution attempt; retain the gate audit
  and both refreshed-ref re-audits identified above. Two initial read-only search
  wrappers in re-audit 02 had shell/flag syntax errors; they were disregarded and
  corrected searches completed successfully.

## Open/deferred
- BLOCKED/FAIL tracker rows and exact next action: S03-E01–E08, S03-B01, S03-D01,
  S03-L01, S03-R01, S03-A01, and S03-H01 wait for their declared product and entry
  prerequisites. G02–G10 and I01–I11 are the active not-started work queue.
- NOT_RUN/unavailable checks and reason: all gated product, typed E2E, benchmark,
  dependency-delta, layout, reclamation, artifact-verifier, and final-regression
  checks; remaining entry/dependency rows have not yet completed.
- DEFERRED_STAGE_07 checks: every item in §15.4 remains DEFERRED_STAGE_07.
- Remaining source contradictions: the requested incoming handoff is absent from the
  current branch but retained on origin/layerstack_2_0; the current Stage 02 outgoing
  handoff is the live normative handoff.

Completion assertion:
POC FAIL / BLOCKED at this interim checkpoint because mandatory non-deferred
implementation and evidence rows are not yet complete. S03-G01 is PASS and no longer
an external blocker. No approved corpus, source inspection, or retained earlier-stage
result is being inferred as Stage 03 implementation completion.
```

Final closure record:

```text
# Stage 03 final handoff

Verdict: POC PASS
Closed at (UTC): 2026-07-25T04:27:25Z

## Authority and scope
- Owner decision: PRC-STAGE03-OWNER-DECISION-G01.1;
  contract_v3_owner_decision_g01_1.md SHA-256
  27264ef96f97960757eeba0b51bb7d2560446466cbf8e6a11c99a881da834e16.
- Approval mapping: gate_resolution_approval_20260725_04.md SHA-256
  49ea0a740462ce2652d5a4c4f21f595a44a56af25c0b7222dff3149a63a5f849.
- v3 format/corpus: version 3; SHA-256
  7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be.
- D2.5 remains v2-only. Public authority remains legacy_v1.
- Stage 04–07 authority was not pulled into Stage 03.

## Git custody
- Product: upgrade-2.0-phase-1; baseline/upstream
  cbe45de873cd24fbf48bb7b3a6c5f9f98980313c; task-owned dirty source;
  final campaign source-diff SHA-256
  d5323b27f1dd7b9e19cf53551162e5608624597b1a9b6aaa9f9dcf1d6b8c8823.
- Test+benchmark: upgrade-2.0-phase-1; baseline/upstream
  173191e8694515af43797128070dbdfd2d246040; task-owned dirty source/report;
  final campaign source-diff SHA-256
  95adf9fddf75d715a464d095cc7e9192d240d3eaa00597b822795e5756c2ba38.
- Docs: layerstack_2_0; HEAD
  901d6d2181d0795eaaf174a23636a38019aab9a1; upstream
  426b6be3284c26a59eb77d39ad6622997e8479c9; Stage 03 guide/decision/corpus/
  gate/entry/audit/benchmark/handoff changes retained.
- No reset, stash, clean, branch switch, or unrelated-resource mutation occurred.

## Implementation and product verification
- S03-I01–S03-I11 PASS: bounded v3 codec/identities, scalar SeqCDC, typed loose
  CAS, raw capture/order, persistent content+attribution pages, private refs,
  durable operations/recovery, semantic OCC, full ref operations, conditional
  v1 source protection, normal-protocol hidden validation, observations and
  terminal PTY output-drain synchronization.
- cargo fmt PASS; portable core 15 non-ignored PASS (one benchmark ignored);
  candidate_publication 28/28 PASS; workspace unit 34/34 PASS;
  workspace_session_publish 18/18 PASS; security 1/1 PASS;
  namespace-execution 68 non-ignored PASS.
- A package-wide invocation also observed 26 unrelated Stage 05 squash/flatten
  cases hit the pre-existing explicit macOS Linux-only guard. The Stage 03
  target in that package passed 28/28; Stage 03 did not modify that guard.

## Typed E2E
- Complete module: 34/34 PASS in 77.56 s.
- IDs: I01–I05 5/5; P01–P05 5/5; R01–R06 6/6; O01–O03 3/3;
  F01–F09 9/9; S01–S02 2/2; B01–B04 4/4.
- Focused runner/strict-artifact/dispatch surface: 22/22 PASS.
- Final artifact compatibility: 22/22 PASS.
- All exact case-owned sandboxes/resources were destroyed/retired.

## Final 180-second campaign
- Run: 019f977b-752d-7868-927d-170b8d46a078.
- Plan SHA-256:
  5511812675ab2f6784b39b701a333200391e51d6e87e870906d0c454d308d8d6.
- Cell: sha256:e71292adeb408b5c8629e6ea9a32aa133cf1be8d427f9eb74dabd07e6b7ac371.
- Runner elapsed: 137.27 s; measured campaign boundary: 136.568017333 s.
- State completed; failures 0; warnings 0; report ready.
- Overall PASS; correctness PASS; performance NOT_RUN/INSUFFICIENT_SAMPLE.
- Strict evidence SHA-256:
  e8d7426a22ae22680f0c1597d8dcbfd5d9814539e33aa85287efe23be44ff334.
- Report SHA-256:
  fd919bddc80e50f5c45a26b5b22b476b14aea77e9346df9c76c27ffeffd2ae53.
- Summary SHA-256:
  728d3c0d805ccfdc7146e9c3482838adad8b394c23e79702dc1d2c8009a7b464.
- Cleanup ledger/result boundary SHA-256:
  7cf3607f4a9fb329651ef577393507130c74ba6103cb9a32aa8e1a26069d2059 /
  f5657907f7c00f6bce6970a7c798c450c929866c31584b7ae13cb3623d86a7e5.
- Both public ABBA pairs match; public mismatches, route failures, fallbacks,
  active resources after quiescence and unexplained residue are zero.
- Private probe: 16 valid samples; checkpoint, OCC, F01–F09, exact retry,
  restart and cleanup assertions PASS.

## Dependency, portability, layout and cleanup
- Six entry/earlier-exit/final dependency captures were byte-identical:
  SHA-256 1c77ccb2048f4c7383b0bbe6b45f5c999a88e79bcd2ef86ac2650d503e52be1d;
  16 invocations, 1,143 external packages, 2,179 feature pairs, 116 direct
  edges, exact zero external delta, std-only portable core PASS.
- Dependency/portability audit SHA-256:
  a475ad7a23999ee4a231c08d40677186498bddcaf5b44d4e2fbf8683eaa386f7.
- Pinned local arm64 image:
  ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90.
- B02/B03/B04 prove the Stage 03 /eos map, workload masking, capture exclusion,
  restart/failure/delete/teardown boundaries and settled state.
- Final exact cleanup removed only generated catalog/gateway/daemon binaries
  and the three temporary comparator directories after retaining their
  identities. Results, fixture, ledger, result boundary, source and ordinary
  Cargo cache/private probe remain.
- No Stage 03 container, runtime entry, process or listener remains. Three
  unrelated pre-existing gateways on 7878/17878/17978 were untouched.

## Retained documents and deferrals
- benchmark_note.md SHA-256:
  8b775f3ed998132a72b451034b8d8e529fd427cfbfcd7bedd8a06bd84219778f.
- handoff_to_stage_04.md SHA-256:
  471fc5b65a167755b5620f43429e6efc59794fb250f074789c19cf7ef4bf9954.
- Full performance selection, multi-host/filesystem qualification, later-stage
  destructive-retention survival and public cutover remain DEFERRED_STAGE_07.

Completion assertion:
All mandatory non-deferred Stage 03 rows have direct retained evidence and
are PASS. There is no open Stage 03 blocker. The bounded result is a POC PASS,
not a Stage 07 performance-selection or release-qualification claim.
```
