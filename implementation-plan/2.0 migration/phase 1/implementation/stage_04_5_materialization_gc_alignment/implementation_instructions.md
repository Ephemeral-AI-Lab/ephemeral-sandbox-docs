# Stage 04.5 implementation instructions — materialization/GC lifecycle alignment

Status: `OPEN` / implementation and direct evidence `NOT_RUN`

Document purpose: implementation instruction only. This document does not implement
Stage 04.5, execute tests, amend the four Stage 04.5 source documents, or promote any
gate to `PASS`.

## A. Status, source authority, ledger, and custody

### A.1 Working status

Stage 04.5 starts `OPEN`. Every checklist item in this guide is intentionally unchecked.
Every Stage 04.5 E2E, benchmark, diagnostic, cleanup, and final-validation result starts
`NOT_RUN`. Architecture inspection and inherited Stage 04 evidence establish context,
not Stage 04.5 proof.

The exact unresolved implementation contradiction is:

> The current product source exposes and calls
> `begin_generation_retirement`, `finish_generation_retirement`, and
> `GenerationStore::remove_generation`, which recursively removes a published
> generation. Stage 04.5 expressly has no generation-retirement, GC, unlink, or
> deletion authority. These production entry points must be removed or made
> structurally unreachable before Stage 04.5 can pass.

This is an implementation blocker, not a documentation-authoring blocker. There is no
known external-decision blocker.

### A.2 Normative source order

When two documents differ, apply the first applicable source in this order:

1. `stage_04_5_materialization_gc_alignment/spec.md`;
2. `stage_04_5_materialization_gc_alignment/e2e_test.md`;
3. `stage_04_5_materialization_gc_alignment/benchmark_note.md`;
4. `stage_04_5_materialization_gc_alignment/handoff_from_stage_04.md`;
5. `implementation/layerstack_storage_contract.md`;
6. Preparation 04;
7. Stage 04, Stage 05, and Stage 06 specifications, in the ownership area of each
   stage;
8. `implementation/index.md`;
9. this guide.

Repository-level `AGENTS.md`, `CLAUDE.md`, and the maintainer architecture remain
mandatory implementation constraints. In particular:

- Rust stays at the repository's Rust 1.85 / edition 2021 baseline.
- `layerstack` owns portable identity, logical objects, refs, physical locations,
  exact leases, and materializations.
- `operation` owns public service orchestration.
- `workspace` owns private upper/work/execution state and session lifecycle.
- `namespace` owns command/PTY execution.
- `overlay` remains the mount primitive.
- Production source receives no test-only code and no explanatory inline comments.
- Any `unsafe` addition needs a local `SAFETY` justification and explicit inventory.
- Docker gateway work uses `bin/start-sandbox-docker-gateway --rebuild-binary`.
- Manual product probing uses the supported manager/runtime/observability CLIs.

The Stage 04.5 sources are mutually consistent. The implementation index contains
older progress text; it cannot downgrade the later Stage 04 handoff or override the
Stage 04.5 specification.

### A.3 Frozen incoming Stage 04 evidence

Inherited evidence is prerequisite evidence only. Never relabel it as Stage 04.5
direct evidence.

| Item | Frozen value |
| --- | --- |
| Stage 04 outcome | POC `PASS`; Stage 04.5 remains `OPEN` |
| product base named by handoff | `a400863b9` plus retained Stage 04 changes |
| test base named by handoff | `152d37acf` plus append-only reporting |
| official Stage 04 run | `019f9aef-8059-7524-8cd8-d569c9c3d3d2` |
| image | `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` |
| candidate oracle SHA-256 | `8f41d104464733295bb6074e2cb9c12294fa1872b9340636a077d1ca86312d83` |
| workspace oracle SHA-256 | `5bbc4524a8d9e34ecc0263867172b28c291d038e8eeb63956ebb4ae6f3d4704f` |
| catalog exporter SHA-256 | `46fefcd77e08d008c6b076c43f2277be5af1dfa42dd0d11091427079ec75bdda` |
| public authority | `legacy_v1` |

Retain and verify these artifacts before implementation:

| Artifact | SHA-256 | Inherited disposition |
| --- | --- | --- |
| `.benchmark-state/results/019f9aef-8059-7524-8cd8-d569c9c3d3d2/stage04/stage04-materialization-evidence-v1.json` | `9116f77b9f327b3d0e1aacf2d59b7286e21e00395c15347f178090d5cd625434` | Stage 04 `PASS` |
| `.e2e-state/evidence/stage04-019f97c8-38c6-7352-9a4f-84f40f227588/commands/CMD-E03-FINAL-D210.json` | `05bae8e7b06c1a02559c65ed94a96c6400fe5ec2654b871d168ca1338a097de9` | 128/128 Stage 04 typed cases |
| `.e2e-state/evidence/stage04-019f97c8-38c6-7352-9a4f-84f40f227588/commands/CMD-P05-FINAL-V1-RETRY-D209.json` | `14c8a83f4b479560e485d3a29520b2240c0302cd157ece45ed5097f9460b411a` | v1 regressions `PASS` |
| `.e2e-state/evidence/stage04-019f97c8-38c6-7352-9a4f-84f40f227588/commands/CMD-OFFICIAL-ACCEPTANCE-D204.json` | `171c2aa834af079e01c70066814e2779e8733ad693fd546559fabb66b6663d09` | Stage 04 acceptance `PASS` |
| `.e2e-state/evidence/stage04-019f97c8-38c6-7352-9a4f-84f40f227588/commands/CMD-DEPENDENCY-BOUNDARY-AUDIT-D207.json` | `5041aa3298518ff6276b0ce32b4dc3947546149db65b20d3168c6397fd4d3ce3` | boundary audit `PASS` |
| `.e2e-state/evidence/stage04-019f97c8-38c6-7352-9a4f-84f40f227588/final-v1-authority.json` | `22eac843a5f44b6aeb8d5054089d7d2d16928c69eb0c78f1d13761158cac0073` | `legacy_v1` |
| `.e2e-state/evidence/stage04-019f97c8-38c6-7352-9a4f-84f40f227588/stage07-deferral-audit.json` | `7f4173df64a8e37e427efcd26e2158707505af18a9eeac6c810d9e61b4fb0e6c` | explicit deferrals |
| `.benchmark-state/results/019f9aef-8059-7524-8cd8-d569c9c3d3d2/stage04/cleanup/ledger.json` | `74e4638c8cc65a78ba8394369d745cbdb6fd451a66bf0287731ccfeb661b7908` | durable, quiescent, zero unexplained residue |

### A.4 Current repository custody

This guide was authored against this read-only custody snapshot:

| Repository | Branch | HEAD/upstream | State before this document |
| --- | --- | --- | --- |
| `ephemeral-sandbox` | `upgrade-2.0-phase-1` | `68c6e2bdeb490c2e7a24f3791dba865c38d9e737` | clean |
| `ephemeral-sandbox-test` | `upgrade-2.0-phase-1` | `47d634d88db005f81b3e2c1ed66a8b4a4bc3d80b` | clean |
| `ephemeral-sandbox-docs` | `layerstack_2_0` | `8b8c7eb4301b4c50740d8ae33dda392566393bfb` | pre-existing untracked `implementation_instructions_prompt.md` |

The implementer must capture a new custody record with exact revisions, upstreams,
dirty flags, and diff hashes before the first edit and before every evidence campaign.
Do not clean, overwrite, or absorb unrelated work.

### A.5 Append-only command ledger

`ephemeral-sandbox-test/e2e/test-report.md` is the canonical command ledger.
Before every future live E2E, benchmark, diagnostic, build used as evidence, or cleanup
command:

1. append one pending entry;
2. include the exact expanded command, working directory, environment, revisions,
   image digest, owner/run ID, intended artifact path, and `Good / Defect / Fix`;
3. execute only that command;
4. fill only that pending entry with exit status, start/end monotonic times, raw
   artifact paths and SHA-256 values, observations, result, and cleanup;
5. never rewrite or delete an older entry.

A command without a prior pending entry is diagnostic-only and cannot support `PASS`.
An interrupted command keeps its entry and records the interruption.

### A.6 Complete reading ledger

This is the complete source set inspected for this guide. Counts and hashes identify
the read-only snapshot; future implementation must re-hash every row and stop on
unexplained drift.

| Relative path | Why it is authoritative or informative | Lines | SHA-256 |
| --- | --- | ---: | --- |
| `ephemeral-sandbox/AGENTS.md` | repository execution and change rules | 11 | `df940aab9dcd4502ae0bcb7615f97100aedc75955e6eefa7dfcb07aae1730ff9` |
| `ephemeral-sandbox/CLAUDE.md` | product build, test, gateway, and Rust constraints | 94 | `f4ebdc0aaa997b673d272c31e2a09e12e4d499f0c1d1cd15000335796086a308` |
| `ephemeral-sandbox/docs/maintainer-architecture.md` | crate ownership and dependency boundaries | 189 | `bad6718400572de469516c3c3677e642958b87b99e5d7d4bbb8ecc393dd3b454` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_5_materialization_gc_alignment/spec.md` | primary Stage 04.5 requirements and exit gates | 568 | `c741de5b251f63351f8ed6919963b13cc4812aa45783c313c7346a30a7ab2425` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_5_materialization_gc_alignment/e2e_test.md` | normative typed E2E coverage and dispositions | 312 | `cefc7c78c765b7be8e391db6c09a59d98249729602a92fb4ac915a3ca984132f` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_5_materialization_gc_alignment/benchmark_note.md` | normative 180-second campaign and thresholds | 292 | `4e537e22f46d9bd5b58ee3ba3a478da1dea0d69f5a58ea67e42108d1d56b1bc1` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_5_materialization_gc_alignment/handoff_from_stage_04.md` | frozen incoming evidence, authority, and custody | 110 | `7f6e846880f083434314700c6b80a49c0548dd2c92d3c5618dde3653d0ea8f65` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/index.md` | phase ordering and document index | 407 | `7ff4b5078a0e96822d956b532942e0a12ecf654319c3d95d5ccd750080272df9` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/layerstack_storage_contract.md` | durable paths, authority, identity, and sync contract | 740 | `d0d8405b8f590d4ad6ed671391e2387619454c5938e24d873628b2d53c5734b6` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/preparation_04_layerstack_storage_foundation/implementation_instructions.md` | common storage-foundation predecessor | 819 | `a02a8280152a59316cdb139299ac22f309bc3737787ffdcc4daebc122518257f` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_candidate_materialization/spec.md` | Stage 04 producer and native-behavior contract | 179 | `37806e99d1c6db7d63e89350211d97ab0b24154331152cbcf3e3d0aeda06083a` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_candidate_materialization/e2e_test.md` | inherited Stage 04 typed cases | 114 | `ece6bfafed573fd381587ad334d5d38d7f1d794d01ebbfd69c0f8c16c9620a40` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_candidate_materialization/benchmark_note.md` | inherited Stage 04 performance protocol | 53 | `e542e0a4ec8d0c437e910a01fa0f61b365a4bbcc7b425f9987da39ca324dcb53` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_candidate_materialization/implementation_instructions.md` | current Stage 04 implementation map and evidence rules | 1620 | `0f1429c71bf5acc4de82ae5edbe8839687d581809813908b564936fb79236464` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_candidate_materialization/handoff_to_stage_04_5.md` | Stage 04 completion facts handed to this stage | 99 | `00a17fb923bbb6cc78fd4046f082ad82f9ca0a287830b0253aeac893d73d98a4` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_05_candidate_gc_and_compaction/spec.md` | next-stage GC, deletion, pack, and locator authority | 647 | `4abe52434ea5cbf99c7a3791db0df0baf4f8110dda7082e930402ee9a556a7cd` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_05_candidate_gc_and_compaction/e2e_test.md` | downstream barrier/handoff expectations | 234 | `84750c01adbda20b6f731864b7bac0781bc28de49c5c22e13b5820cb8abe422f` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_05_candidate_gc_and_compaction/benchmark_note.md` | downstream settled-space gates | 196 | `c632177758c4807aee6fb96cc1a7a30555e201456ed1e6c5c2707da107f8303b` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_06_migration_and_rollback/spec.md` | later public authority switch and rollback boundary | 215 | `44f826f236435f33d0e9e0e5dbb7337e927650db769a90c6b926e9c61d74ecb3` |
| `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_03_incremental_publication/implementation_instructions.md` | prior common publication, OCC, and identity patterns | 1514 | `2ea6c4e64416cd1327d18656b811f135c90ce3144d77ffaba73caeb6d472f435` |

## B. Exact outcome, gates, and scope

### B.1 Required outcome

Implement exactly this producer/consumer boundary:

```text
bounded private build
    -> complete verification and sync
        -> typed immutable Ready generation
            -> bounded common publication
                -> exact old-generation handoff
```

The stage passes only when all of the following are direct, artifact-backed facts:

- private reconstruction, repair, and squash are invisible until common publication;
- the only authoritative lifecycle is `Building -> Ready -> Published -> Terminal`;
- all payload work finishes outside the storage writer lock;
- every replacement publication either admits the exact root to the active Stage 05
  GC barrier or leaves the old selector authoritative;
- admitted readers remain on their exact generation and fence;
- old published generations remain retained until Stage 05 owns retirement;
- recovery is bounded by current admitted work, not total history;
- every owner, waiter, byte, buffer, queue entry, worker, FD, hold, operation,
  generation, retry, and disk target is governed and observable;
- Stage 04 strict native command/file/PTY behavior stays exact, with no silent
  fallback;
- v1 remains public read/write authority;
- all correctness, crash, resource, space, and matched performance gates pass;
- final cleanup is durable, quiescent, and has zero unexplained residue.

### B.2 In scope

- Refactor Stage 04 materialization into the common operation lifecycle.
- Add supervisor-owned bounded storage admission and recovery dispatch needed by
  materialization.
- Add typed root, source, prior-generation, session, and operation protection.
- Add the non-destructive Stage 05 root-admission and exact old-subject handoff
  interfaces.
- Make replacement publication unavailable when that handoff owner is disabled.
- Remove or production-fence Stage 04 retirement/deletion APIs.
- Replace history-sized allocation, verification, lease, and recovery scans.
- Add observability, failpoints, strict decoders, resource accounting, direct unit
  tests, typed E2E cases, and the focused benchmark campaign.
- Preserve all Stage 03/04 identities and public behavior.

### B.3 Out of scope and forbidden

- No logical or physical deletion by Stage 04.5.
- No generation retirement, grace-period policy, trash owner, or maintenance daemon.
- No GC mark/sweep implementation.
- No object unlink, generation unlink, pack unlink, locator unlink, or v1 unlink.
- No pack writer/compactor or locator-run publication.
- No public candidate authority or fallback authority.
- No migration `CONTROL` switch and no v1-retirement authority.
- No new top-level directory, second selector, `NEXT`, allocator pointer, journal,
  receipt, grace ticket, or per-materialization trash hierarchy.
- No repair by maximum generation, mtime, directory age, or searching history.
- No unbounded collection/sort, process-global ownerless pool, memory mapping, or
  input-sized queue.
- No waits, tree walks, hashes, payload verification, provider payload I/O, permit
  acquisition, worker joins, generation scans, or lease scans under the writer lock.
- No implementation change to the four Stage 04.5 source documents as part of this
  guide's execution.

The only Stage 04.5 cleanup authority is exact incomplete private work named by one
valid common `STATE` record and proven, by component-wise path validation, to be below
that operation's `work/`. Published generations and uncertain data are retained.

### B.4 Gate semantics

Use only:

- `OPEN`
- `IN_PROGRESS`
- `BLOCKED`
- `PASS`
- `FAIL`
- `NOT_RUN`
- `INSUFFICIENT_SAMPLE`

Use a narrow named deferral only where the specification explicitly assigns the cell
to a later stage, for example `DEFERRED_STAGE_07`. Never turn unavailable, omitted,
historical, inspected, or inferred evidence into `PASS`.

### B.5 Entry gates, hard blockers, and later-stage boundaries

Entry requires a reconciled custody snapshot, matching retained Stage 04 hashes, the
pinned image/corpus identities, a clean ownership inventory, and a fresh run owner.
Any unexplained revision/diff, missing inherited artifact, mutable image tag, active
conflicting run, or inability to distinguish run-owned resources is a hard stop.

The implementation hard blockers are: reachable retirement/deletion; a fifth
authoritative lifecycle state; replacement publication without an available Stage 05
admission/handoff owner; payload or unbounded work under the writer lock; unbounded
recovery/history scans; ownerless resources; ambiguous corruption repair; public
candidate/fallback authority; or inability to produce raw, digest-addressed evidence.

Stage boundaries are strict:

- Stage 04.5 defines the non-destructive root-admission and exact old-subject handoff
  seam, but Stage 05 alone implements mark/sweep, retirement, unlink, pack/locator
  publication, and settled-space reclamation.
- Stage 06 alone may change public read/write authority or exercise migration
  `CONTROL`; Stage 04.5 must leave `legacy_v1` authoritative.
- Stage 07 alone may perform irreversible v1 retirement. Environment or authority
  preconditions not available now remain explicitly `DEFERRED_STAGE_07`.

## C. `/eos` tree, ownership, identities, and lifecycle

### C.1 Complete Phase 1 ownership tree

Stage 04.5 must preserve this complete tree. A path is created only when its owning
feature first persists a child.

```text
/eos/
├── layer-stack/                                      LayerStack durable owner
│   ├── .storage-writer.lock                          brief cross-process commit fence
│   ├── CONTROL                                       authority/migration fence; untouched here
│   ├── objects/
│   │   ├── loose/<kind>/<digest-prefix>/<typed-id>   immutable logical bytes
│   │   ├── packs/<pack-id>.pack                      Stage 05 physical output
│   │   └── locators/
│   │       ├── <run-id>.sst                          Stage 05 immutable location map
│   │       └── CURRENT                               Stage 05 selected run set
│   ├── refs/
│   │   ├── heads/<branch-id>                         Stage 03 visibility/OCC
│   │   ├── checkpoints/<checkpoint-id>               named snapshot retention
│   │   ├── pins/<pin-id>                             explicit typed retention
│   │   └── leases/<lease-id>                         exact restart-visible protection
│   ├── operations/<operation-id>/
│   │   ├── STATE                                     sole recovery/idempotency record
│   │   └── work/                                     exact bounded private work
│   ├── materializations/<materialization-id>/
│   │   ├── CURRENT                                   sole native-generation selector
│   │   └── generations/<generation>/
│   │       ├── MANIFEST                              immutable verified description
│   │       └── carriers/<carrier-id>/...             immutable backend-native carrier
│   ├── gc/
│   │   └── CURRENT                                   Stage 05 active-GC pointer
│   ├── manifest.json                                 existing v1 compatibility state
│   ├── workspace.json                                existing v1 compatibility state
│   ├── base/<base-id>/...                            existing v1 compatibility bytes
│   ├── layers/<layer-id>/...                         existing v1 compatibility bytes
│   ├── staging/<layer-id>.staging/...                existing v1 compatibility bytes
│   └── .layer-metadata/<layer-id>.{digest,bytes}     existing v1 compatibility metadata
├── workspace/                                        WorkspaceManager runtime owner
│   ├── manager.json                                  restart recovery catalog
│   ├── .export/<spool-id>                            bounded export scratch
│   └── <workspace-session-id>/
│       ├── upper/                                    unpublished session writes
│       ├── work/                                     OverlayFS kernel work
│       └── executions/<execution-id>/
│           └── transcript.log                        command/PTY scratch
├── storage/                                          non-LayerStack service storage
│   ├── file_auditability/...                         audit service owner
│   └── workspace_recovery/...                        failed-cleanup recovery owner
└── runtime/                                          daemon lifecycle owner
    └── daemon/
        ├── runtime.sock
        └── runtime.pid
```

Stage 04.5 itself may persist only this existing subset:

```text
/eos/layer-stack/.storage-writer.lock
/eos/layer-stack/operations/<operation-id>/{STATE,work/...}
/eos/layer-stack/materializations/<materialization-id>/CURRENT
/eos/layer-stack/materializations/<materialization-id>/generations/<generation>/MANIFEST
/eos/layer-stack/materializations/<materialization-id>/generations/<generation>/carriers/<carrier-id>/...
/eos/layer-stack/refs/leases/<lease-id>
```

It may interact with Stage 05's existing `gc/CURRENT` and exact operation-owned
root-admission/handoff interface, but it does not create a parallel GC hierarchy.
There is no `/eos/legacy`, `/eos/layer-stack/refs/legacy`,
`/eos/namespace_execution`, or durable `/workspace`.

### C.2 Ownership rules

| State/resource | Sole owner | Release/visibility rule |
| --- | --- | --- |
| logical objects and roots | LayerStack portable core | immutable; Stage 04.5 reads, never deletes |
| private reconstruction/squash | one common operation | invisible; exact work cleanup only after terminal fencing |
| buffers, queues, workers, FDs, byte/disk permits | storage supervisor | borrowed RAII permits; returned on every exit |
| verified target before publication | `Ready` common operation | immutable, synced, not selected |
| `CURRENT` switch | common publisher under writer lock | atomic replace plus parent fsync |
| active-GC root admission | Stage 05 barrier | invoked inside bounded publication section |
| old exact selector after switch | Stage 05 typed hold/handoff | handed off durably after lock |
| admitted reader generation | exact session lease | reader never follows a later `CURRENT` |
| workspace `upper/work/executions` | WorkspaceManager/session | teardown only after tasks, mounts, FDs, lease release |
| public v1 data | existing v1 authority | retained and writable until Stage 06/07 |

### C.3 Identity derivation

| Identity | Derivation/fields | Prohibited inputs |
| --- | --- | --- |
| `RootId` | typed digest of canonical portable root bytes | host path, carrier, generation, provider, compression |
| `AttributionRootId` | separate typed attribution identity selected beside content | host uid/gid, physical location |
| materialization ID | `(RootId, backend-kind, backend-format-version, target-profile)` | current generation, time, path |
| operation ID | caller/publication idempotency scope plus fenced common-operation identity | mtime, process address |
| generation/fence tuple | exact old selector plus fenced common operation | directory maximum, listing order, wall time |
| carrier ID | verified immutable backend carrier identity | mutable installation path |
| lease ID | exact session owner identity; record names materialization, generation, fence | inferred current selector |
| old-subject handoff | exact `{materialization-id, generation, fence}` from old selector | store-wide search |

Overflow, collision, an existing ambiguous target, or inconsistent identity fails
closed and retains existing data.

### C.4 Authoritative lifecycle

```text
Building
  no new visibility; exact root/source/prior-generation holds and private work durable
    |
    | complete streamed build + verification + sync
    v
Ready
  immutable target and MANIFEST; CURRENT unchanged
    |
    | common bounded publication
    v
Published
  new CURRENT durable; exact old selector recorded; active GC admitted root
    |
    | exact old-subject handoff, or no old selector
    v
Terminal
  durable outcome/response witness; bounded acknowledgement retention
```

`Building -> Terminal` and `Ready -> Terminal` are failure/cancellation paths that
retain old `CURRENT`. `Published -> Terminal` treats the new selector as committed and
must finish the exact handoff. Carrier creation/sync/install checkpoints may be bounded
fields inside `Building`; they are not phases or visibility authority.

For an initial materialization without an old selector, publication can finish without
retirement handoff. For replacement, repair, or squash, disable admission when the
Stage 05 handoff owner is unavailable. A disabled Stage 05 may leave a bounded private
`Ready` target explained by `STATE`; it may not change `CURRENT`.

### C.5 Path-by-path durability and deletion authority

“Retain” below means Stage 04.5 has no deletion authority. Atomic replacement always
means same-directory temporary file, file fsync, rename, and parent-directory fsync;
uncertain sync results fail closed and retain both possible owners.

| Exact path or pattern | Creator / mutator | First use and lifecycle | Durability, recovery, and protection | Deletion authority / preconditions | Space bucket | Stage 04.5 action | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `/eos/layer-stack/` | LayerStack storage initialization | before any LayerStack child | durable directory; parent sync when first created | none in 04.5 | metadata | reuse; no parallel root | `S045-V01` |
| `/eos/layer-stack/.storage-writer.lock` | storage adapter; lock primitive mutates kernel lock state | bounded publication/GC metadata commit | cross-process fence; rank after permits/flight, before metadata mutation | no routine unlink | metadata | reuse and instrument | `S045-V04` |
| `/eos/layer-stack/CONTROL` | migration authority, not 04.5 | Stage 06 authority work | sole migration/authority fence | Stage 06/07 only | metadata | read only if needed; never mutate | `S045-V18` |
| `/eos/layer-stack/objects/loose/<kind>/<digest-prefix>/<typed-id>` | portable object store | logical object persistence | immutable, typed digest verified; exact root/source holds protect it | Stage 05 only after reachability/lease barriers | loose payload | read and hold; never unlink | `S045-V02` |
| `/eos/layer-stack/objects/packs/<pack-id>.pack` | Stage 05 pack writer | Stage 05 compaction | immutable pack plus locator witnesses | Stage 05 only after locator/fence rules | packed payload | observe/account only | `S045-V02` |
| `/eos/layer-stack/objects/locators/<run-id>.sst` | Stage 05 locator publisher | Stage 05 lookup publication | immutable run; selected only through locator `CURRENT` | Stage 05 only | locator metadata | observe/account only | `S045-V02` |
| `/eos/layer-stack/objects/locators/CURRENT` | Stage 05 locator publisher | Stage 05 location-set switch | sole locator selector; atomic replace and parent fsync | Stage 05 only | locator metadata | do not mutate | `S045-V02` |
| `/eos/layer-stack/refs/heads/<branch-id>` | Stage 03/common publisher | logical publication/OCC | atomic typed ref; exact expected-old comparison | Stage 05 reachability rules, never 04.5 | metadata | preserve identity/OCC | `S045-V17` |
| `/eos/layer-stack/refs/checkpoints/<checkpoint-id>` | checkpoint owner | named retention | restart-visible exact root protection | owning later workflow after proof | metadata + retained payload | preserve | `S045-V02` |
| `/eos/layer-stack/refs/pins/<pin-id>` | pin owner | explicit retention | typed restart-visible hold | pin owner after exact release | metadata + retained payload | preserve | `S045-V02` |
| `/eos/layer-stack/refs/leases/<lease-id>` | session lifecycle | before first reader use through teardown | exact materialization/generation/fence; durable-before-use; renewal does not change subject | lease owner may remove exact lease only after tasks/mounts/FDs stop; never generation data | metadata + leased old generation | keep exact subject and order | `S045-V09` |
| `/eos/layer-stack/operations/<operation-id>/STATE` | common operation store | before private source work; through bounded terminal acknowledgement | sole operation/recovery truth; canonical `<=256 KiB`; atomic replace; checksum/fence | common operation owner only after durable Terminal/ack policy; uncertainty retained | operation metadata | converge materialization here | `S045-V03`, `S045-V10` |
| `/eos/layer-stack/operations/<operation-id>/work/**` | one fenced common operation | Building only | component-validated descendant; exact owner in `STATE`; never public | 04.5 may remove only exact incomplete private work after Terminal fence and proof it is beneath this `work/` | private target/staging | stream bounded build here | `S045-V03`, `S045-V16` |
| `/eos/layer-stack/materializations/<materialization-id>/CURRENT` | common publisher | only after immutable Ready | sole native selector; checked expected-old; atomic replace and parent fsync; leases protect exact subject | no deletion in 04.5 | metadata | bounded switch only | `S045-V05` |
| `/eos/layer-stack/materializations/<materialization-id>/generations/<generation>/MANIFEST` | private builder/common operation | complete before Ready | immutable, canonical `<=256 KiB`, checksum/identity/sync witness | Stage 05 only after exact retention barriers | current/old native generation | verify and never mutate after Ready | `S045-V03` |
| `/eos/layer-stack/materializations/<materialization-id>/generations/<generation>/carriers/<carrier-id>/**` | private native builder | Building; selected only after Ready publication | immutable carrier verified and synced before Ready; source/prior holds remain exact | Stage 05 only; 04.5 never calls recursive removal | current/old/private native target | build, verify, sync, retain | `S045-V02`, `S045-V03` |
| `/eos/layer-stack/gc/CURRENT` | Stage 05 GC coordinator | active-cycle discovery at publication | exact active-cycle pointer under writer lock; root admission must be durable before visibility | Stage 05 only | GC metadata | interact through typed bridge only | `S045-V06` |
| `/eos/layer-stack/{manifest.json,workspace.json,base/**,layers/**,staging/**,.layer-metadata/**}` | legacy v1 services | existing public v1 reads/writes | existing v1 durability/recovery contract | Stage 06/07 authority only | v1 rollback bytes | preserve public read/write | `S045-V18` |
| `/eos/workspace/manager.json` | WorkspaceManager | session admission/recovery | restart catalog; exact session owner | WorkspaceManager after session recovery rules | workspace metadata | preserve | `S045-V09` |
| `/eos/workspace/.export/<spool-id>` | export owner | bounded export | exact spool owner and cleanup ledger | export owner after close | export scratch | do not absorb into LayerStack | `S045-V16` |
| `/eos/workspace/<workspace-session-id>/{upper,work,executions/**}` | WorkspaceManager/session/namespace | mount and command/PTY lifecycle | session ownership; tasks, mounts, FDs, transcript and lease ordering | WorkspaceManager after task/mount/FD quiescence | workspace upper/work | preserve routing and attribution | `S045-V09`, `S045-V15` |
| `/eos/storage/{file_auditability,workspace_recovery}/**` | named non-LayerStack services | their service lifecycle | service-specific exact owner/recovery | named service only | other service | exclude from LayerStack cleanup | `S045-V16` |
| `/eos/runtime/daemon/{runtime.sock,runtime.pid}` | daemon lifecycle | daemon start/stop | process identity and supported runtime CLI | daemon owner on exact shutdown | runtime metadata | observe via supported CLI | `S045-V16` |

### C.6 Canonical lifecycle work items

| Work ID | Transition or boundary | Required durable/observable result | Forbidden result | Verification |
| --- | --- | --- | --- | --- |
| `S045-L01` | admission to `Building` | all predicted byte/worker/FD/disk/operation/target permits, exact holds/fence, and `STATE` durable before source work | uncharged read/allocation or discoverable target | `S045-V03`, `S045-V07` |
| `S045-L02` | `Building` private reconstruction | streamed work only below validated operation `work/`; bounded checkpoints | second target, mapping, unbounded buffer/history scan | `S045-V03`, `S045-V07` |
| `S045-L03` | `Building -> Ready` | carrier and manifest fully verified/synced; immutable Ready identity durable | `CURRENT` change or mutable manifest | `S045-V03` |
| `S045-L04` | initial `Ready -> Published` | exact Ready subject becomes sole `CURRENT`; no old handoff required | visibility before Ready | `S045-V05` |
| `S045-L05` | replacement preflight | disabled/missing Stage 05 handoff rejects before writer lock/visibility | switch followed by “best effort” handoff | `S045-V06` |
| `S045-L06` | active-GC publication | exact root admission and its fsync precede `CURRENT` replacement inside bounded lock section | visible unadmitted root | `S045-V06` |
| `S045-L07` | `Published -> Terminal` replacement | new selector stays committed and exact old `{materialization,generation,fence}` is durably handed off | old-subject search or 04.5 deletion | `S045-V06`, `S045-V09` |
| `S045-L08` | pre-publication failure/cancel | old selector remains; exact private work is recovered or safely reaped | partial visibility or source deletion | `S045-V08`, `S045-V10` |
| `S045-L09` | crash/response loss | recover from `STATE`/exact selector only; return same durable outcome without duplicate target | mtime/max-generation repair | `S045-V08`, `S045-V10` |
| `S045-L10` | reader admission/release | reader holds exact generation/fence; release never authorizes generation deletion | following later `CURRENT`, ABA substitution | `S045-V09` |
| `S045-L11` | recovery scheduling | deterministic opaque cursor, at most 64 records/slice, retry count at most 8, fair common-kind dispatch | collect/sort total history | `S045-V10` |
| `S045-L12` | shutdown/cleanup | owner fenced, waiters wake once, workers join, permits return, exact private/run resources only removed, durable ledger | orphan pool, broad cleanup, unexplained residue | `S045-V07`, `S045-V16` |

## D. Architecture, APIs, states, locks, and hard caps

### D.1 Target component graph

```text
service request
  -> bounded request decoder
  -> StorageSupervisor admission
       -> permits(bytes, worker, FD, disk, operation, target)
       -> bounded per-key flight owner/join
  -> CommonOperation<Building>
       -> root/source/prior-generation holds durable
       -> NativeBuilder streams into operations/<id>/work
       -> complete verify + sync
  -> CommonOperation<Ready>
  -> CommonPublisher
       -> preflight outside lock
       -> writer lock
       -> bounded fence/selector/digest checks
       -> optional active-GC root admission
       -> CURRENT atomic replace + parent fsync
       -> Published state witness
       -> unlock
       -> exact old-subject handoff
  -> CommonOperation<Terminal>
  -> service selection/lease response
```

The portable LayerStack core remains safe and filesystem-independent. Filesystem,
native reconstruction, locks, sync, and carrier operations remain in backend/storage
adapters rather than leaking into portable identity types.

### D.2 Required typed model

Use typed values rather than boolean combinations. Exact names may follow repository
conventions, but the semantics and impossible-state guarantees are mandatory.

```rust
enum CommonOperationPhase {
    Building(BuildingState),
    Ready(ReadyState),
    Published(PublishedState),
    Terminal(TerminalState),
}

struct BuildingState {
    operation_id: OperationId,
    request_digest: RequestDigest,
    materialization: MaterializationKey,
    old_selector: Option<GenerationSubject>,
    root_hold: RootHold,
    source_holds: BoundedSourceHolds,
    prior_generation_hold: Option<GenerationHold>,
    work_relative_path: ValidatedWorkPath,
    reservations: ReservationWitness,
    checkpoint: BoundedBuildCheckpoint,
    fence: OperationFence,
}

struct ReadyState {
    building: BuildingIdentity,
    subject: GenerationSubject,
    manifest_digest: ManifestDigest,
    logical_identity: RootId,
    counts: VerifiedCounts,
    allocated_bytes: u64,
    capability_witness: CapabilityWitness,
    sync_witness: SyncWitness,
}

struct PublishedState {
    ready: ReadyIdentity,
    new_selector: GenerationSubject,
    old_selector: Option<GenerationSubject>,
    root_admission: RootAdmissionWitness,
    selector_sync: SyncWitness,
}

struct TerminalState {
    outcome: TerminalOutcome,
    selected: Option<GenerationSubject>,
    old_handoff: OldSubjectHandoffWitness,
    response_digest: ResponseDigest,
    residue: BoundedResidueRecord,
}
```

The encoded `STATE` is the only durable operation and recovery truth. It needs magic,
version, declared length, checksum, kind, idempotency scope, request digest, phase,
exact subjects/holds/fence, bounded checkpoint, terminal outcome/error, retry count,
and response witness. Reject unknown required fields, duplicates, non-canonical
encoding, oversize, checksum mismatch, truncation, overflow, path escape, or ambiguous
subject.

The immutable `MANIFEST` must carry magic/version/length/checksum, exact materialization
key, generation/fence, root identity, backend kind/version/profile, carrier identities,
canonical counts/lengths/extents, allocated-byte witness, capability plan, and sync
witness. Once `Ready` is durable, never mutate it.

### D.3 Required internal APIs

Keep public service behavior stable. Introduce or reshape internal interfaces around
these responsibilities:

```rust
trait StorageGovernor {
    fn admit(&self, request: &AdmissionRequest, deadline: Deadline)
        -> Result<StoragePermits, AdmissionError>;
    fn join_or_own(&self, key: &MaterializationKey, deadline: Deadline)
        -> Result<FlightRole, AdmissionError>;
}

trait CommonOperationStore {
    fn create_building(&self, state: &BuildingState) -> Result<(), OperationError>;
    fn transition_ready(&self, ready: &ReadyState) -> Result<(), OperationError>;
    fn transition_published(&self, published: &PublishedState)
        -> Result<(), OperationError>;
    fn transition_terminal(&self, terminal: &TerminalState)
        -> Result<(), OperationError>;
    fn recover_page(&self, cursor: RecoveryCursor, limit: PageLimit<64>)
        -> Result<RecoveryPage, OperationError>;
}

trait MaterializationBuilder {
    fn build_private(
        &self,
        operation: &BuildingOperation,
        permits: &StoragePermits,
        cancellation: &CancellationFence,
    ) -> Result<ReadyGeneration, MaterializationError>;
}

trait GcPublicationBridge {
    fn preflight_replacement(&self, old: Option<&GenerationSubject>)
        -> Result<PublicationMode, PublicationError>;
    fn admit_root_while_locked(
        &self,
        root: &RootId,
        lock: &StorageWriterLockGuard,
    ) -> Result<RootAdmissionWitness, PublicationError>;
    fn handoff_old_subject(
        &self,
        subject: &GenerationSubject,
        operation: &OperationFence,
    ) -> Result<OldSubjectHandoffWitness, PublicationError>;
}

trait CommonPublisher {
    fn publish(
        &self,
        ready: ReadyGeneration,
        permits: PublicationPermits,
        cancellation: &CancellationFence,
    ) -> Result<PublishedGeneration, PublicationError>;
}
```

The bridge is an interface and durable witness boundary, not Stage 05 GC,
retirement, or deletion. Use a typed disabled mode: initial publication may proceed;
replacement must fail before visibility.

### D.4 Private build protocol

Before reading any logical graph or physical source:

1. Decode and validate all request lengths/counts/depths/capabilities.
2. Predict target and peak allocated bytes with checked arithmetic.
3. Acquire byte, worker, FD, disk, operation, and target permits.
4. Join or own the bounded same-key flight.
5. Resolve old selector exactly.
6. Persist `Building` with exact root/source/prior-generation holds and fence.
7. Stream canonical reconstruction only under `operations/<id>/work/`.
8. Check every offset, extent, segment, entry, object ID, checksum, count, and
   capability before allocation/access.
9. Verify logical identity, native metadata, allocated size, carrier shape, and
   capabilities with bounded buffers.
10. Sync carrier content, manifest, and every required parent in the documented order.
11. Persist immutable `Ready`.

The owner publishes one target. Waiters observe the owner's typed terminal result;
they never build a duplicate. Owner panic/cancellation fences the flight, wakes all
waiters exactly once, returns permits, and leaves a recoverable durable record.

### D.5 Publication protocol and linearization

Outside the writer lock:

- verify `Ready` type and bounded encoding;
- revalidate cancellation, operation fence, expected old selector, manifest digest,
  publication permits, disk reservation, and bridge availability;
- open/prepare only the bounded metadata handles needed by commit.

Inside the writer lock, and only inside it:

1. re-read bounded `CURRENT` and active-GC metadata;
2. compare expected old selector/fence/digest;
3. append and fsync the exact logical root when active GC requires admission;
4. atomically replace `CURRENT`;
5. fsync the materialization parent;
6. persist the bounded published selector/old-subject witness in `STATE`;
7. release the lock.

After the lock:

1. hand the exact old subject to Stage 05 durably;
2. only after the handoff witness is durable, release the operation's old-generation
   hold;
3. persist `Terminal`;
4. wake waiters with the durable selection;
5. return all permits.

If failure is before selector replace, the old selector wins. If selector replacement
is durable, the new selector wins and recovery completes the old handoff. Lost response
is answered idempotently from the durable result.

### D.6 Lock order and assertions

The only permitted acquisition order is:

```text
byte / worker / FD / disk / operation / target permits
    -> optional bounded per-key single-flight ownership
        -> storage writer lock
```

The flight-registry mutex is held only to insert, inspect, update, or remove one
bounded entry. Never hold it while waiting, building, joining, doing I/O, or holding
the writer lock. Code with the writer lock cannot acquire a permit or wait.

Add debug/test lock-rank assertions and production counters for every forbidden
writer-lock class:

- tree walk;
- payload/content hash or carrier verification;
- generation/history/lease scan;
- permit/queue/flight wait;
- worker join;
- provider payload I/O;
- reconstruction/squash work.

Every counter must be zero in final evidence even if timing passes.

### D.7 Hard caps

The tighter existing limit may remain. Raising any cap requires amending the
specification and benchmark plan.

| Resource | Hard cap |
| --- | ---: |
| shared storage-owned byte permits | `min(B, 64 MiB)` |
| storage data/background workers | 4 globally |
| materialization `Building`/`Ready` targets | 4 globally |
| aggregate build reservation `W_mat` | `min(4 GiB, 10% LayerStack capacity)` |
| nonterminal common operations | 64 across all kinds |
| same-key waiters | 16 |
| metadata queue | 16 descriptors and 64 KiB encoded |
| hydration output buffer | 256 KiB per worker |
| `STATE` encoding | 256 KiB |
| `MANIFEST` encoding | 256 KiB; a stricter valid cap may remain |
| open FDs | 16 per operation, 64 storage-global |
| Stage 04.5 mappings | 0 |
| active typed holds | 4,096 |
| active/pinned materialization generations | 64 |
| native depth | 64 |
| operation retries | 8 and caller/maintenance deadline |
| recovery page | 64 common operation records |

Admission failure is typed, bounded, observable, and deadline-aware. It must not
allocate first, spin, silently queue, create a target, or trigger deletion.

### D.8 Recovery and corruption

Run common recovery before materialization mutation admission. A slice processes at
most 64 records and returns an opaque deterministic cursor; never collect or sort all
paths before truncation. Ensure fairness between operation kinds and cap each record's
retry count at eight.

| Observation | Required action |
| --- | --- |
| `Building`, target incomplete | retain old selector; resume bounded checkpoint or terminally abandon exact private work |
| `Ready`, old selector still current | publish through common publisher or retain/terminally abandon without visibility |
| `Published`, new selector current, handoff absent | retain every generation; complete exact handoff |
| terminal pre-publication failure | old selector remains; exact validated private work may be reaped |
| new selector, response absent | return durable result idempotently |
| corrupt/missing `CURRENT` | fail closed; never search generation history |
| corrupt/truncated/oversized/ambiguous `STATE` | expose no private target; retain all possibly owned bytes and report residue |
| old and new both appear authoritative | stop mutation, retain both, require exact-witness repair |
| `ENOSPC` before selector replace | retain old selector and all sources |
| `ENOSPC` after selector replace | retain new selector and old generation until handoff completes |

The generation allocator must not use a sorted generation vector or maximum directory
name. Derive the exact generation/fence from durable old selector plus operation fence,
use no-replace installation, and fail closed on collision.

### D.9 Cancellation, panic, and shutdown

- Cancellation is checked before admission, between bounded build chunks, before
  `Ready`, before lock acquisition, and immediately before selector replace.
- Do not roll back a durable selector replace.
- Catch panics only at an ownership boundary that can fence the operation, wake
  waiters, join/stop borrowed tasks, and return permits.
- The storage supervisor owns worker startup, bounded queue, stop signal, and join.
- Shutdown admits no new work, fences existing operations, allows bounded settle,
  joins exactly its workers, and leaves durable recovery truth.
- No detached or process-global ownerless pool survives supervisor shutdown.

## E. File-by-file implementation maps

Line numbers below identify the inspected baseline and may move after edits. Function
names and responsibilities are the stable anchors.

### E.1 Product repository

| File | Baseline finding | Required Stage 04.5 change | Verification IDs |
| --- | --- | --- | --- |
| `crates/sandbox-runtime/layerstack/src/stack/candidate/materialization.rs` | `begin_generation_retirement` at ~254, `finish_generation_retirement` at ~294, removal call at ~325; multiple writer-lock sections at ~488/516/538/556; `lookup_verified` and history/lease scans | delete or production-fence retirement APIs; split owner into private builder and common publisher; make all heavy verification pre-lock; remove history/lease scans from foreground; bridge exact Stage 05 admission/handoff | `S045-U01`, `E04-*`, `E05-*`, `E07-*` |
| `.../candidate/generation.rs` | `MAX_MANIFEST_BYTES=64 KiB`; `next_generation` ~310; `generation_numbers` ~487; `remove_generation` ~598; recursive `remove_owned_tree` ~821 | retain strict bounded decoder; derive exact fenced generation without enumeration; remove deletion API from production; expose no tree-removal helper for published generations; immutable `Ready` install/no-replace | `S045-U02`, `E02-*`, `E08-*` |
| `.../candidate/materialization_operation.rs` | materialization-specific phases `Owned` through `CurrentDurable` | replace with common four-state record; encode bounded typed checkpoints inside `Building`; add exact holds, witnesses, retry, response, residue; one strict 256-KiB decoder | `S045-U03`, `E03-*`, `E06-*` |
| `.../candidate/native_backend.rs` | bounded native reconstruction and verification primitives exist | accept supervisor-owned buffers/workers/FD permits; keep streaming and depth/entry/segment checks; write only validated work path; expose complete verify/sync witness; no private pool/mapping | `S045-U04`, `E02-*`, `E07-*`, benchmark cold/space cells |
| `.../candidate/mod.rs` | exports Stage 04 candidate modules | export only aligned internal surface; do not expose deletion/retirement | `S045-S01` |
| `.../candidate/operation.rs` | existing common-operation/recovery concepts for publication | converge record codec, paging, dispatcher, and idempotency rather than create a second journal | `S045-U05`, `E06-*` |
| `.../candidate/publication.rs` | existing common writer-lock publication and GC-barrier patterns | reuse/refactor common publisher and root-admission seam; add exact materialization selector subject and old-subject handoff | `S045-U06`, `E04-*` |
| `.../candidate/refs.rs`, `ref_ops.rs` | roots/refs and typed subjects | add/reuse exact root and generation hold types; bounded direct identity lookup only | `S045-U07`, `E04-*`, `E05-*` |
| `.../candidate/squash.rs` and `.../squash/flatten.rs` | squash has its own construction/publication path | make squash a private `Building -> Ready` producer preserving `RootId` and `AttributionRootId`; common publisher owns selection | `S045-U08`, `E03-*`, squash benchmark cells |
| `.../storage/lock.rs` | storage writer lock primitive exists | add lock-rank/forbidden-work instrumentation without expanding critical section | `S045-U09`, `E07-*` |
| `.../storage/mod.rs` plus new focused storage modules if needed | no complete shared governor/dispatcher for Stage 04.5 caps | add supervisor, permits, bounded queue/pool, flight registry, recovery pager, and typed shutdown ownership; prefer small cohesive modules | `S045-U10`, `E06-*`, `E07-*`, `E08-*` |
| `.../service/impls/candidate_materialization.rs` | service owns worker gate/single-flight orchestration | inject shared supervisor; cap owners and 16 waiters/key; map typed admission/recovery errors; keep strict behavior | `S045-U11`, `E07-*` |
| `.../service/model.rs` | candidate request/selection/lease API model | keep public contract stable; add internal typed witnesses only where required; no public authority claim | `S045-U12`, `E11-*` |
| `.../service/support.rs` | service construction/support | construct one owned supervisor and join it at shutdown; no global pool | `S045-U13`, `E07-*`, `E10-*` |
| `.../observability.rs` | Stage 04 counters are narrow | add phase, admission, high-water, bytes, worker, queue, FD, hold, generation, recovery page/retry/residue, lock wait/hold, and forbidden-work counters | `S045-U14`, all E2E/benchmark |
| `.../stack/observation.rs` | runtime observation surface | expose bounded snapshots and exact owner IDs without scanning history; preserve current fields | `S045-U15`, `E01-*`, `E07-*`, `E10-*` |
| `.../layerstack/src/lib.rs`, `.../stack/mod.rs` | service/stack construction boundaries | thread governor/bridge dependencies explicitly; avoid public deletion exports | `S045-S02` |
| `crates/sandbox-runtime/operation/src/services.rs` | strict candidate service config, admission TTLs | construct/inject aligned storage dependencies; preserve public `legacy_v1` routing | `S045-U16`, `E11-*` |
| `crates/sandbox-runtime/workspace/src/service/impls/create_workspace.rs` | resolves candidate and acquires exact v1 snapshot before manager open | keep strict candidate selection and exact generation lease; no silent fallback; maintain rollback order | `S045-U17`, `E05-*`, `E09-*` |
| `.../workspace/src/lifecycle/create.rs` | persists admission, mounts, renews/finalizes lease | preserve durable-before-use lease and cleanup order; ensure exact generation/fence survives selector switch | `S045-U18`, `E05-*`, `E09-*` |
| `.../workspace/src/lifecycle/destroy.rs` | teardown releases exact candidate lease | preserve task/mount/FD-before-lease ordering; Stage 04.5 does not use lease release as generation deletion authority | `S045-U19`, `E05-*`, `E10-*` |
| `.../workspace/src/lifecycle/persistence.rs`, `.../session/state.rs` | restart-visible session lease identity | decode exact generation/fence, fail closed on ambiguity, and retain bounded recovery behavior | `S045-U20`, `E05-*`, `E06-*` |
| `layerstack/tests/candidate_materialization.rs` | Stage 04 private materialization tests | add focused lifecycle, deletion-unreachable, cap, codec, paging, collision, crash, and lock tests; retain Stage 04 tests | `S045-U01..U15` |
| `operation/tests/workspace_session_materialization.rs` | Stage 04 strict workspace/session tests | add exact old/new reader, response-loss, replacement-disabled, public authority, command/file/PTY regressions | `S045-U16..U20` |

Do not create a generic framework beyond the common storage responsibilities already
required by Stages 03–05. Keep portable core dependencies within the maintainer
architecture constraints.

### E.2 Test and benchmark repository

| File | Action | Required content |
| --- | --- | --- |
| `e2e/runtime/layerstack_phase1/test_materialization_gc_alignment.py` | add | typed Stage 04.5 declarations and direct oracles listed in §G |
| `e2e/runtime/layerstack_phase1/helpers.py` | extend narrowly | frozen Stage 04.5 fixture identity, owner inventory, allocated-byte snapshots, quiescence and exact cleanup helpers |
| `e2e/test-report.md` | append only | pending-before-run entries and immutable outcomes |
| `benchmark/backend/benchmark_lab/stage04_5_materialization_gc_alignment.py` | add | one runner-owned 180-second campaign, artifact schema, raw samplers, strict verifier, cleanup |
| `benchmark/backend/benchmark_lab/runner.py` | extend | register one campaign operation and serialize its artifact |
| `benchmark/backend/benchmark_lab/planning.py` | extend | frozen plan shape; reject protocol drift |
| `benchmark/backend/benchmark_lab/recovery.py` | extend | exact run-owned recovery/cleanup only |
| `benchmark/defaults/definition-catalog.json` | extend | operation `stage04_5_materialization_gc_alignment_campaign` |
| `benchmark/presets/layerstack-phase1-stage04-5-materialization-gc-alignment.yml` | add | pinned image, deterministic seed, 180/150/60 clocks, ABBA/complement protocol, caps |
| `benchmark/backend/tests/unit/test_stage04_5_materialization_gc_alignment.py` | add | clock, gate, statistics, schema, space/resource, cleanup, retry tests |
| `benchmark/backend/tests/contract/test_planning.py` | extend | exact one-cell expansion and protocol-drift rejection |
| `benchmark/backend/tests/integration/test_runner.py` | extend | dispatch/artifact/failure/cleanup integration |
| `benchmark/backend/tests/compatibility/test_artifacts.py` | extend | strict schema/golden compatibility |
| `benchmark/tests/fixtures/golden/layerstack_phase1/stage04_5_materialization_gc_alignment_v1.json` | add | deterministic schema golden; never fabricated measured PASS data |

### E.3 Documentation repository at implementation close

Only after direct evidence exists:

- append the exact Stage 04.5 rows to `benchmark_note.md`;
- update `e2e_test.md` statuses with raw artifact links;
- update `spec.md` exit criteria and stage status;
- update `handoff_from_stage_04.md` only if correcting an explicitly identified
  inherited fact, never to rewrite Stage 04 evidence;
- update `implementation/index.md`;
- create a Stage 04.5 handoff to Stage 05 with identities, artifacts, failures,
  cleanup, authority, deferrals, and exact remaining blockers.

Those future documentation edits are implementation-close work, not authorized by
the current documentation-only task.

### E.4 Canonical implementation work map

The following four tables are the canonical file map. Earlier shorthand explains the
baseline; these stable rows control execution and progress.

#### Product code and product tests

| Work ID | Exact current path(s) | Action | Precise deliverable | Depends on | Requirements | Verification | Stop condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S045-I01` | `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/materialization.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/generation.rs` | CHANGE/REMOVE | remove or structurally fence retirement, `remove_generation`, and recursive published-tree removal; replace history-derived generation selection | `S045-G01` | no 04.5 deletion; exact identity | `S045-V02` | any production caller can unlink/retire published data |
| `S045-I02` | `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/materialization_operation.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/operation.rs` | CHANGE | one strict common `Building/Ready/Published/Terminal` state/codec, exact witnesses, 256-KiB bound, response idempotency | `S045-I01` | lifecycle/recovery truth | `S045-V03`, `S045-V10` | fifth phase, second journal, mutable Ready, or unbounded decode |
| `S045-I03` | `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/storage/mod.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/storage/lock.rs` | CHANGE; ADD focused child modules only if needed | injected supervisor, ranked permits/lock, bounded pool/queue/flights/recovery pager, typed shutdown | `S045-I02` | caps and lock contract | `S045-V04`, `S045-V07`, `S045-V10` | ownerless pool, missing charge, lock inversion, or total-history allocation |
| `S045-I04` | `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/native_backend.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/materialization.rs` | CHANGE | streamed validated private build under operation `work/`, full verify/sync, immutable Ready, no mappings | `S045-I02`, `S045-I03` | private build/capability shapes | `S045-V03`, `S045-V07`, `S045-V13` | private visibility, duplicate target, mapping, or unverified Ready |
| `S045-I05` | `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/publication.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/refs.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/ref_ops.rs` | CHANGE | bounded common publisher, active-GC root admission, exact old-subject handoff, expected-old fencing | `S045-I02`, `S045-I03`, `S045-I04` | publication/Stage 05 seam | `S045-V05`, `S045-V06` | forbidden lock work, visible unadmitted root, or searched handoff subject |
| `S045-I06` | `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/squash.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/candidate/squash/flatten.rs` | CHANGE | squash becomes private Ready producer and uses the same publisher while preserving both root identities | `S045-I04`, `S045-I05` | producer convergence | `S045-V03`, `S045-V14` | squash owns selector switch or changes identity |
| `S045-I07` | `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/service/impls/candidate_materialization.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/service/support.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/observability.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/observation.rs` | CHANGE | inject supervisor/bridge, bounded snapshots, all cap/phase/owner/lock/recovery counters, exact shutdown join | `S045-I03`, `S045-I05` | service ownership/observability | `S045-V07`, `S045-V12`, `S045-V16` | missing owner/counter is interpreted as zero |
| `S045-I08` | `ephemeral-sandbox/crates/sandbox-runtime/operation/src/services.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/service/model.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/lib.rs`; `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/mod.rs` | CHANGE | explicit dependency wiring, stable public model, `legacy_v1` routing, no public deletion export/fallback | `S045-I05`, `S045-I07` | architecture/authority | `S045-V17`, `S045-V18` | dependency inversion or candidate authority |
| `S045-I09` | `ephemeral-sandbox/crates/sandbox-runtime/workspace/src/service/impls/create_workspace.rs`; `ephemeral-sandbox/crates/sandbox-runtime/workspace/src/lifecycle/create.rs`; `ephemeral-sandbox/crates/sandbox-runtime/workspace/src/lifecycle/destroy.rs`; `ephemeral-sandbox/crates/sandbox-runtime/workspace/src/lifecycle/persistence.rs`; `ephemeral-sandbox/crates/sandbox-runtime/workspace/src/session/state.rs` | CHANGE | exact generation/fence lease survives switch/restart; teardown releases lease after tasks/mounts/FDs and never deletes generation | `S045-I05`, `S045-I08` | reader/session exactness | `S045-V09`, `S045-V15` | reader follows CURRENT, ABA substitution, fallback, or teardown reordering |
| `S045-I10` | `ephemeral-sandbox/crates/sandbox-runtime/layerstack/tests/candidate_materialization.rs`; `ephemeral-sandbox/crates/sandbox-runtime/operation/tests/workspace_session_materialization.rs` | CHANGE | focused structural, codec, model, crash, cap, reader, authority, and strict command/file/PTY product proofs | `S045-I01` through `S045-I09` | all product gates | `S045-V02` through `S045-V18` | test-only production hook or broad suite masks smallest failure |

#### E2E, fixtures, catalog, schema, and helpers

| Work ID | Exact current path(s) | Action | Precise deliverable | Depends on | Requirements | Verification | Stop condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S045-I11` | `ephemeral-sandbox-test/e2e/runtime/layerstack_phase1/test_materialization_gc_alignment.py` | ADD | typed declarations for every §G case with stable ID, deadline, setup/schedule, direct oracle, artifact, and cleanup | `S045-I10` | full E2E catalog | `S045-V01` through `S045-V18` | any normative E2E bullet lacks an individual case |
| `S045-I12` | `ephemeral-sandbox-test/e2e/runtime/layerstack_phase1/helpers.py`; `ephemeral-sandbox-test/e2e/fixtures/layerstack_phase1/candidate-materialization-v1/manifest.json`; `ephemeral-sandbox-test/e2e/fixtures/layerstack_phase1/candidate-materialization-v1/generate.py` | CHANGE | frozen shapes/capabilities, failpoint schedules, owner inventory, allocated-byte snapshots, deadlines, quiescence, exact cleanup | `S045-I11` | deterministic evidence | `S045-V03`, `S045-V08`, `S045-V11`, `S045-V12`, `S045-V16` | fixture identity drifts or helper mutates non-owned state |
| `S045-I13` | `ephemeral-sandbox-test/e2e/metadata/catalog.yaml`; `ephemeral-sandbox-test/e2e/harness/catalog/collect.py`; `ephemeral-sandbox-test/e2e/harness/schema.py` | CHANGE | schema-valid stable case metadata and side-effect-free catalog generation with digest | `S045-I11` | catalog completeness | `S045-V11`, `S045-V19` | duplicate/missing case ID or collection has live side effects |
| `S045-I14` | `ephemeral-sandbox-test/e2e/test-report.md` | APPEND ONLY | pending-before-command ledger and immutable results/failures/supersessions | every future live command | evidence custody | `S045-V19` | an evidence command runs before its pending row |

#### Benchmark plan, runner, artifact, verifier, and negative tests

| Work ID | Exact current path(s) | Action | Precise deliverable | Depends on | Requirements | Verification | Stop condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S045-I15` | `ephemeral-sandbox-test/benchmark/backend/benchmark_lab/stage04_5_materialization_gc_alignment.py` | ADD | one monotonic campaign operation, raw time/space/resource/lifecycle streams, versioned artifact and strict recomputation | `S045-I10`, `S045-I12` | campaign/artifact | `S045-V20` through `S045-V28` | benchmark-only product protocol, reset clock, or summary-only evidence |
| `S045-I16` | `ephemeral-sandbox-test/benchmark/backend/benchmark_lab/runner.py`; `ephemeral-sandbox-test/benchmark/backend/benchmark_lab/planning.py`; `ephemeral-sandbox-test/benchmark/backend/benchmark_lab/recovery.py`; `ephemeral-sandbox-test/benchmark/defaults/definition-catalog.json`; `ephemeral-sandbox-test/benchmark/presets/layerstack-phase1-stage04-5-materialization-gc-alignment.yml` | CHANGE/ADD preset | register exact operation/plan, reject drift, allocate unique root, recover/clean exact owner, enforce 180/150/60 clocks | `S045-I15` | runner ownership | `S045-V20`, `S045-V27`, `S045-V28` | prerequisite enters clock, late closeout passes, or broad cleanup |
| `S045-I17` | `ephemeral-sandbox-test/benchmark/backend/tests/unit/test_stage04_5_materialization_gc_alignment.py`; `ephemeral-sandbox-test/benchmark/backend/tests/contract/test_planning.py`; `ephemeral-sandbox-test/benchmark/backend/tests/integration/test_runner.py`; `ephemeral-sandbox-test/benchmark/backend/tests/compatibility/test_artifacts.py`; `ephemeral-sandbox-test/benchmark/tests/fixtures/golden/layerstack_phase1/stage04_5_materialization_gc_alignment_v1.json` | ADD/CHANGE | clock/gate/schema/statistics/space/recovery tests and negative rejection of missing, unmatched, insufficient, late, unowned, falsely-zero, non-quiescent evidence | `S045-I15`, `S045-I16` | verifier soundness | `S045-V20` through `S045-V28` | fabricated measured PASS in golden or negative case accepted |

#### Documentation, reporting, cleanup, and handoff

| Work ID | Exact current path(s) | Action | Precise deliverable | Depends on | Requirements | Verification | Stop condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S045-I18` | `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_5_materialization_gc_alignment/spec.md`; `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_5_materialization_gc_alignment/e2e_test.md`; `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_5_materialization_gc_alignment/benchmark_note.md` | CHANGE AT CLOSE | reconcile only direct results, raw paths/digests, exact thresholds, failures, insufficiency, and cleanup | `S045-I11` through `S045-I17` | authoritative closure | `S045-V19`, `S045-V29` | prose or inherited evidence promoted to PASS |
| `S045-I19` | `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_5_materialization_gc_alignment/handoff_from_stage_04.md`; `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/index.md` | PRESERVE first; CHANGE index at close | preserve frozen handoff; update index only with reconciled direct status and remaining boundary | `S045-I18` | custody/stage order | `S045-V01`, `S045-V29` | inherited evidence rewritten |
| `S045-I20` | `ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/stage_04_5_materialization_gc_alignment/handoff_to_stage_05.md` | ADD AT CLOSE | identities, direct artifacts/digests, exact bridge, failures/deferrals, authority, cleanup ledger, and next blocker | `S045-I18`, `S045-I19` | handoff | `S045-V29` | handoff claims deletion authority or lacks cleanup/quiescence |

## F. Ordered implementation sequence

Each step has a stop condition. Do not run the focused campaign while an earlier
structural gate is open.

### F01 — Freeze custody and retained evidence

- [ ] Record repository revisions, upstreams, worktree status, diffs, toolchain,
  platform, filesystem, Docker, image digest, and artifact checksums.
- [ ] Verify all inherited Stage 04 artifacts in §A.3.
- [ ] Allocate a fresh Stage 04.5 owner/run ID and artifact root.
- [ ] Record unrelated resources that cleanup must not touch.

Stop on checksum drift, dirty-worktree ambiguity, missing evidence, unpinned image, or
unresolved ownership.

### F02 — Add red structural tests

- [ ] Add compile/static tests proving the retirement/deletion APIs are absent or
  production-unreachable.
- [ ] Add red tests for the four-state codec, 256-KiB limits, generation collision,
  path escape, corrupt selectors, no-history repair, and 64-record paging.
- [ ] Add lock-rank, forbidden-work, cap, cancellation, panic, and shutdown tests.
- [ ] Append a pending report entry before executing any test command.

Stop until tests fail for the intended missing behavior, not fixture/harness defects.

### F03 — Remove deletion authority

- [ ] Remove `begin_generation_retirement`, `finish_generation_retirement`,
  `remove_generation`, and published-generation recursive removal from production
  reachability.
- [ ] Remove time/grace-based generation deletion outcomes and observations.
- [ ] Ensure ordinary session lease release cannot invoke Stage 04.5 generation
  deletion.
- [ ] Add static inventory proving no Stage 04.5 unlink of logical/published state.

Stop if any production call path can delete a generation or treat expiry/absence as
deletion authority.

### F04 — Implement common state and strict codecs

- [ ] Converge materialization on `Building`, `Ready`, `Published`, `Terminal`.
- [ ] Persist exact root/source/prior-generation holds, selector subjects, fences,
  manifest/sync witnesses, outcomes, response digest, retry, and residue.
- [ ] Enforce bounded canonical decoders and atomic sync/replace ordering.
- [ ] Keep resumable build details as bounded `Building` checkpoints.

Stop on a fifth authoritative phase, second journal, mutable `Ready` manifest, or
unbounded decode/allocation.

### F05 — Implement the shared storage supervisor

- [ ] Own global byte, worker, queue, FD, operation, hold, generation, target, and
  disk reservations in one injected supervisor.
- [ ] Own exactly one four-worker global pool and bounded queue.
- [ ] Bound same-key owners and waiters; reject waiter 17 by typed deadline result.
- [ ] Add RAII return, panic fencing, shutdown stop/join, and high-water metrics.

Stop on any ownerless worker/pool, uncharged target/buffer/FD, unbounded queue/map, or
resource leak after cancellation.

### F06 — Make build private and produce immutable `Ready`

- [ ] Acquire all admission and exact protections before source reads.
- [ ] Stream into the exact operation work directory.
- [ ] Preserve canonical reconstruction, RootId, AttributionRootId, metadata,
  capabilities, and strict native behavior.
- [ ] Fully verify and sync before `Ready`.
- [ ] Make repair and squash use the same producer boundary.

Stop if a private target is discoverable through `CURRENT`, a duplicate target is
created for same-key waiters, or verification relies on full history.

### F07 — Implement bounded common publication

- [ ] Add Stage 05 bridge preflight, active-GC root admission, and exact old-subject
  handoff.
- [ ] Keep all heavy work outside the writer lock.
- [ ] Atomically replace `CURRENT`, sync parent, and record exact old/new subjects.
- [ ] Disable replacement when Stage 05 handoff is disabled.
- [ ] Return committed selection idempotently after response loss.

Stop unless every forbidden-work counter is zero and every crash point has one
deterministic old/new outcome.

### F08 — Implement bounded common recovery

- [ ] Page at most 64 operation records with opaque deterministic cursor.
- [ ] Dispatch every operation kind fairly; do not skip recognized materialization.
- [ ] Cap retries at eight and retain/report uncertainty.
- [ ] Derive selection only from old `CURRENT`, exact operation subject, or fail
  closed.
- [ ] Reap only exact validated private work.

Stop on collect-then-truncate, sorting total history, maximum/mtime repair, lease scan,
or unexplained residue.

### F09 — Preserve session/public behavior

- [ ] Prove old sessions keep exact old generation/fence across replacement.
- [ ] Prove new sessions select and lease the new exact generation.
- [ ] Preserve strict native command/file/PTY behavior and deterministic unsupported
  PTY responses.
- [ ] Preserve v1 public read/write authority and zero candidate fallback authority.
- [ ] Preserve workspace teardown ordering and private upper/work ownership.

Stop on selector-following readers, ABA substitution, fallback, public candidate
authority, or hidden durable state from read-only commands.

### F10 — Complete unit, model, and hostile-input verification

- [ ] Run formatting, focused unit tests, codec/property/fuzz tests, concurrency model
  tests, supported Miri/Loom/sanitizer cells, and repository checks.
- [ ] Record unsupported cells explicitly without claiming `PASS`.
- [ ] Verify dependency and unsafe inventories.

Stop on a failure, missing raw artifact, unlogged command, or unsupported generalized
claim.

### F11 — Run typed E2E

- [ ] Export and verify the typed Stage 04.5 catalog.
- [ ] Execute §G in the pinned Linux/arm64 environment through supported surfaces.
- [ ] Retain one raw record per stable case ID.
- [ ] Run Stage 03, Stage 04, v1, boundary, and authority regressions.

Stop unless every required supported case passes and cleanup is exact.

### F12 — Run the focused matched campaign

- [ ] Validate the frozen plan.
- [ ] Run the single 180-second campaign in §I.
- [ ] Do not restart the campaign clock for retries.
- [ ] Verify sample sufficiency, raw statistics, gates, space buckets, resources,
  cleanup, quiescence, and artifact hashes.

Stop on overrun, missing complement order, insufficient required samples, threshold
failure, forbidden lock work, residue, or missing accounting.

### F13 — Reconcile and hand off

- [ ] Populate §K only from direct raw evidence.
- [ ] Complete §L and §M.
- [ ] Re-run final custody/authority/dependency/cleanup verification.
- [ ] Update authoritative docs and produce the Stage 05 handoff.

`PASS` is permitted only when no required work remains.

### F.14 Step execution contract

The table makes the smallest safe loop explicit. A suite named under “do not rerun”
is retained from the same revision/configuration while a later, unrelated failure is
debugged; it is rerun once in the final complete proof.

| Step | Prerequisites | Smallest focused test | Retain | Cleanup proof | Exact stop | Already-passing suites not rerun |
| --- | --- | --- | --- | --- | --- | --- |
| `F01` | none | hash/custody checker | custody JSON, hashes, owner inventory | no resources created | any drift/ambiguity | all runtime suites |
| `F02` | `F01` | one structural/codec test | failing output and intended reason | test temp root absent | harness failure or wrong red reason | Stage 03/04 E2E |
| `F03` | `F02` | deletion symbol/callgraph test | inventory and compiler result | build temp only | reachable delete/retire | unrelated codec/model tests |
| `F04` | `F03` | one state transition/decoder case | encoded vectors, crash point | temp operation root exact | fifth state/second journal/unbounded decode | deletion inventory |
| `F05` | `F04` | one permit/waiter/panic case | cap trace, thread/permit snapshot | zero live workers/permits | ownerless/unbounded/leaked owner | lifecycle codec tests |
| `F06` | `F05` | private Ready pause case | tree/digest/sync witness | exact private temp owner | visibility/duplicate/unverified carrier | governor unit family |
| `F07` | `F06` | one GC interleaving/failpoint | lock/root/selector/handoff trace | exact operation resources | unadmitted visibility/forbidden work | private-build family |
| `F08` | `F07` | one 65-record page/restart case | cursors, slices, residue | dispatcher quiescent | history collect/sort or uncertainty deleted | publication interleavings |
| `F09` | `F08` | old-reader/new-reader switch | lease/route/content tuples | tasks/mounts/FDs then lease | ABA/fallback/deletion | recovery family |
| `F10` | `F09` | exact failing tool/input cell | corpus/tool output | tool-owned temp removed | unsupported generalized or missing raw output | passing product families |
| `F11` | `F10`, catalog hash | exact `S045-E##` case, then family | per-case JSON/log/digest | case owner ledger/quiescence | any required supported case non-PASS | every unaffected passing E2E family |
| `F12` | all correctness/resource/cleanup gates | benchmark contract test, then plan validate | plan/hash/raw campaign/verifier | ledger durable before 180 s | insufficiency/threshold/clock/residue | passing correctness E2E |
| `F13` | verified raw evidence | link/ID/status validator | final matrix, diffs, hashes | zero run-owned resources | orphan claim/link or authority drift | all suites except one final complete proof |

## G. Typed E2E catalog

### G.1 Declaration contract

Add stable IDs under:

```text
runtime.layerstack-phase1.materialization-gc-alignment.<family>-<index>-<slug>
```

Every declaration records owner, execution surface, exact claim, oracle, timeout,
availability, fixture/corpus identity, required counters, expected space delta, and
cleanup. Dynamic generation is acceptable only when the exported catalog contains a
distinct stable record and direct result for each row.

### G.2 Required case families

All rows start `NOT_RUN`. Each individual row combines its direct oracle and
observations with this mandatory family contract, so every case has an explicit
setup/schedule, logical and physical oracle, counters, artifact, deadline, cleanup,
and verification ID.

| Family ID | Setup / schedule and retained-state oracle | Raw artifact / deadline / cleanup | Verification |
| --- | --- | --- | --- |
| `S045-E01` | frozen source/build inventories; published and v1 data untouched | `commands/<case-id>.json`; 30 s; no live owner | `S045-V01`, `S045-V02`, `S045-V17`, `S045-V18` |
| `S045-E02` | pinned tree/capability; pause named phase; old/missing selector until common publish; sources/old/one private target retained | `cases/<case-id>/result.json`; 60 s; exact operation/private root | `S045-V03`, `S045-V05`, `S045-V13` |
| `S045-E03` | deterministic GC/publication barrier or I/O failpoint; exact old or admitted-new result; old/source/private copies retained to witnessed handoff | `cases/<case-id>/{lock,root,selector}.json`; 60 s; operation plus test GC fixture | `S045-V04`, `S045-V05`, `S045-V06`, `S045-V08` |
| `S045-E04` | old/new session schedule; each reader keeps exact generation/fence; old/new generations retained | `cases/<case-id>/{lease,tree}.json`; 60 s; tasks/mounts/FDs then lease | `S045-V02`, `S045-V07`, `S045-V09` |
| `S045-E05` | one crash/short-write/torn/`EIO`/response-loss/ENOSPC boundary; only exact old/new authority and all uncertain copies retained | `cases/<case-id>/durability.json`; 60 s; recover then exact private/run owner | `S045-V08`, `S045-V10`, `S045-V16`, `S045-V25` |
| `S045-E06` | histories `>64`, mixed kinds, deterministic cursor; ≤64 records/slice and no directory-derived selection | `cases/<case-id>/recovery.json`; 60 s; dispatcher idle and owners reconciled | `S045-V10`, `S045-V12`, `S045-V24` |
| `S045-E07` | declared owner/waiter/queue/lock schedule; rejected work creates no target; every permit remains owned | `cases/<case-id>/concurrency.json`; 60 s; fence/join/wake/return all | `S045-V04`, `S045-V07`, `S045-V16` |
| `S045-E08` | frozen hostile corpus or supported tool cell; reject before prohibited allocation/access; uncertainty retained | `cases/<case-id>/{corpus,tool}.json`; 60 s; tool/corpus temp root | `S045-V07`, `S045-V11`, `S045-V12` |
| `S045-E09` | supported manager/runtime API on exact lease; strict route; reads leave zero durable growth; mutations are owned | `cases/<case-id>/{route,space}.json`; 60 s; supported session teardown | `S045-V13`, `S045-V15`, `S045-V22`, `S045-V23`, `S045-V25` |
| `S045-E10` | deterministic churn/restart/settle; zero live run owner/residue; expected generations attributed | `cases/<case-id>/stability.json`; 60 s/operation; durable owner ledger | `S045-V12`, `S045-V16` |
| `S045-E11` | current-revision compatibility/authority probes; Stage 03/04 retained, Stage 05 bridge only, v1 public, Stage 07 deferred | `cases/<case-id>/compatibility.json`; 60 s; exact run owner | `S045-V06`, `S045-V17`, `S045-V18` |

| Stable family/cases | Direct oracle | Required observations |
| --- | --- | --- |
| `S045-E01-C01-deletion-apis-unreachable` | production symbol/callgraph inventory has no Stage 04.5 retirement/deletion path | symbols, callers, feature set, artifact SHA |
| `S045-E01-C02-unsafe-dependency-inventory` | portable/core boundary and unsafe inventory match approved baseline | dependencies, unsafe blocks, mappings=0 |
| `S045-E01-C03-v1-authority-static` | default authority remains `legacy_v1` | public/candidate/fallback flags |
| `S045-E02-C01-private-build-invisible` | pause during build; old/missing `CURRENT` remains the only selection | phase, selector, tree inventory |
| `S045-E02-C02-ready-invisible-immutable` | pause at `Ready`; manifest verifies and cannot change; selector unchanged | manifest digest, fsync witness |
| `S045-E02-C03-initial-common-publish` | initial publish selects exact Ready subject and reaches Terminal | old=None, new subject, lock counters |
| `S045-E02-C04-replacement-disabled` | Stage 05 bridge disabled rejects replacement before visibility | old selector retained, target attributed |
| `S045-E02-C05-repair-and-squash-common-publisher` | both producers reach the same Ready/publisher path and preserve identities | RootId, AttributionRootId, subject |
| `S045-E02-C06-required-tree-capability-shapes` | every required regular/sparse/symlink/hardlink/xattr/metadata/depth/capability shape uses the private Ready boundary | shape ID, capability witness, tree digest, bounded resources |
| `S045-E03-C01-gc-starts-before-ready` | active GC admits exact root before selector visibility | GC fence/root log/CURRENT ordering |
| `S045-E03-C02-gc-starts-at-publish` | lock serializes GC start and publication; root visible implies admitted | lock trace, root witness |
| `S045-E03-C03-gc-stops-at-publish` | either admission commits or publication retains old selector | exact old/new state |
| `S045-E03-C04-root-admission-fsync-failure` | failed root-log fsync prevents selector replacement | retained old selector/data |
| `S045-E03-C05-handoff-failure-after-publish` | new selector remains; exact old generation stays protected and recovery completes handoff | Published state, hold, retry |
| `S045-E04-C01-old-reader-survives-switch` | existing reader continues exact old generation/fence | lease and content identity |
| `S045-E04-C02-new-reader-uses-new` | post-switch reader leases exact new generation | selector/lease tuple |
| `S045-E04-C03-reader-release-no-stage045-delete` | lease release never deletes old generation | before/after allocated tree |
| `S045-E04-C04-aba-fence-rejected` | stale lease/fence cannot substitute same-number generation | typed error and retained data |
| `S045-E04-C05-generation-cap` | 65th active/pinned generation fails admission, not retention | high-water=64, no deletion |
| `S045-E05-C01-crash-building` | each Building failpoint retains old selector and recoverable/exact private work | STATE, work owner, retry |
| `S045-E05-C02-crash-ready` | Ready crash either later publishes through common publisher or remains invisible | exact state transition |
| `S045-E05-C03-crash-root-admission` | uncertain admission retains all data and fails closed | root log and selector |
| `S045-E05-C04-crash-current-replace` | atomic old/new result; no history repair | selector checksum, state |
| `S045-E05-C05-crash-parent-fsync` | recovery uses exact durable witnesses and retains uncertainty | fsync witness |
| `S045-E05-C06-crash-published-before-handoff` | new selector kept; exact old hold persists until handoff | Published recovery |
| `S045-E05-C07-response-loss-idempotency` | retry returns the same durable selection without duplicate target | response digest, target count |
| `S045-E05-C08-enospc-before-publish` | old selector and every source retained | allocated buckets, no unlink |
| `S045-E05-C09-enospc-after-publish` | new selector retained and old generation protected | exact old/new inventory |
| `S045-E05-C10-corrupt-current` | fail closed without generation scan/substitute | scan counters=0 |
| `S045-E05-C11-corrupt-state` | no private visibility; all possible owner bytes retained/reported | residue record |
| `S045-E05-C12-restart-storm-bounded` | retries≤8, each slice≤64, no duplicate target | repeated-work bytes |
| `S045-E05-C13-state-short-write` | short `STATE` write never creates an authoritative partial transition | phase witness, private owner, decoder result |
| `S045-E05-C14-manifest-torn-metadata` | torn/truncated/checksum-invalid MANIFEST is never Ready or visible | selector unchanged, all possible bytes retained |
| `S045-E05-C15-current-write-eio` | `EIO` before selector rename preserves exact old authority | I/O boundary, selector digest, unlink=0 |
| `S045-E05-C16-parent-fsync-eio` | uncertain selector durability fails closed and protects both possible exact subjects | fsync witness, holds, restart result |
| `S045-E06-C01-recovery-page-64` | adversarial history processes no more than 64 records/slice | page/slice counters |
| `S045-E06-C02-recovery-fairness` | materialization and other common kinds make bounded progress | per-kind cursor/progress |
| `S045-E06-C03-history-no-collect-sort` | 4× history does not create history-sized allocation | adjusted RSS and scan trace |
| `S045-E06-C04-ownerless-residue-dispatched` | recognized operation is terminal or retained/explained | reason/bytes/retries |
| `S045-E07-C01-same-key-16-waiters` | one owner/target and 16 bounded waiters receive one result | owner/waiter/target highs |
| `S045-E07-C02-same-key-waiter-17` | excess waiter fails by deadline without target or leak | typed error, cleanup |
| `S045-E07-C03-disjoint-four-targets` | at most four targets/workers and `sum(T_build)≤W_mat` | permits and disk reservations |
| `S045-E07-C04-global-operation-64` | 65th nonterminal operation fails admission | operation high-water |
| `S045-E07-C05-lock-order` | ranked assertions survive adversarial interleavings | lock trace |
| `S045-E07-C06-no-forbidden-lock-work` | every forbidden-work counter is zero | counter snapshot |
| `S045-E07-C07-cancel-owner-wakes-waiters` | one fenced outcome, all waiters wake, all permits return | wake count, residue |
| `S045-E07-C08-panic-owner-wakes-waiters` | panic boundary has same ownership guarantees | join/permit/flight state |
| `S045-E07-C09-supervisor-shutdown-joins` | no worker/queue/flight remains after shutdown | thread/process inventory |
| `S045-E07-C10-distinct-owner-65` | 64 distinct nonterminal owners cause distinct owner 65 to fail admission without eviction | owner/operation/target high-water, retained owners |
| `S045-E07-C11-queue-q1` | `Q=1` completes with bounded descriptor/byte ownership | queue high-water, progress, waits |
| `S045-E07-C12-queue-q4` | `Q=4` completes with bounded descriptor/byte ownership | queue high-water, progress, waits |
| `S045-E07-C13-queue-q16` | `Q=16` reaches but never exceeds 16 descriptors/64 KiB | descriptor/encoded-byte high-water |
| `S045-E07-C14-queue-q64-rejected` | requested `Q=64` is clamped or rejected before oversized allocation | requested/admitted Q, allocation, typed error |
| `S045-E08-C01-state-hostile-decode` | corrupt/truncated/oversize/noncanonical inputs fail before allocation | fuzz corpus and peak allocation |
| `S045-E08-C02-manifest-hostile-decode` | same for MANIFEST | fuzz corpus and peak allocation |
| `S045-E08-C03-path-escape` | work path/symlink/component escapes rejected; no external change | exact tree delta |
| `S045-E08-C04-offset-extent-overflow` | checked arithmetic rejects hostile native extents | typed error |
| `S045-E08-C05-depth-64-and-65` | depth 64 works; >64 fails before target | depth counters |
| `S045-E08-C06-resource-cap-matrix` | bytes/workers/targets/queue/FDs/holds/generations/retries stay capped | all high-water fields |
| `S045-E08-C07-zero-mappings` | `/proc`/instrumentation shows no Stage 04.5 mappings | mappings=0 |
| `S045-E08-C08-miri-loom-sanitizer` | supported scoped cells pass; unsupported exact cells stay explicit | tool versions/artifacts |
| `S045-E09-C01-noop-command-old-new` | exact exit/stdout/stderr on both leased generations; zero cold work | route counters |
| `S045-E09-C02-sustained-command` | strict native route, no fallback, bounded resources | throughput/semantics |
| `S045-E09-C03-pty-supported-lifecycle` | create/drain/write/C/D semantics exact | byte stream/status |
| `S045-E09-C04-pty-unsupported-deterministic` | resize/arbitrary signal/literal EOF remain deterministically unsupported | response/error |
| `S045-E09-C05-file-read-metadata` | public API read/stat/readdir exact, zero durable LayerStack growth | before/quiescent buckets |
| `S045-E09-C06-file-write-rename-fsync` | growth only in session upper/work until explicit publish | owner attribution |
| `S045-E09-C07-file-unlink-teardown` | expected filesystem slack only; no LayerStack residue | matched raw delta |
| `S045-E09-C08-explicit-publish-separation` | publication bytes separate from command/file operation | operation IDs/buckets |
| `S045-E10-C01-long-quiescence` | after churn, all resources return and residue is zero/explained | time series and final snapshot |
| `S045-E10-C02-cancel-panic-churn` | flat settled RSS and no flight/permit/FD leaks | RSS slope/high-water |
| `S045-E10-C03-exact-cleanup` | only run-owned resources removed; cleanup ledger durable | owner inventory/hash |
| `S045-E11-C01-stage03-root-regression` | RootId/AttributionRootId and OCC unchanged | frozen vectors |
| `S045-E11-C02-stage04-strict-regression` | retained 128-case behavior still passes | direct regression artifact |
| `S045-E11-C03-stage05-bridge-contract` | exact admission/handoff interface matches Stage 05; no deletion executed | typed contract artifact |
| `S045-E11-C04-stage06-authority` | public read/write remains v1; candidate/fallback false | public route probes |
| `S045-E11-C05-stage07-deferrals` | environment and irreversible-retirement claims remain explicit | deferral audit |

### G.3 Exit-code and disposition rules

- Test assertion or product defect: nonzero, `FAIL`.
- Required environment unexpectedly unavailable: nonzero, `BLOCKED` or `FAIL` with
  exact reason; never silently skip.
- Explicitly unsupported tool/platform cell: stable record with exact availability
  reason and the narrow prescribed deferral/`NOT_RUN`.
- Sample shortfall: `INSUFFICIENT_SAMPLE`, not `PASS`.
- Timeout: `FAIL`, unless runner proves admission stopped and only bounded cleanup
  consumed the reserved closeout window.
- Cleanup uncertainty or unexplained residue: `FAIL`.

## H. Exact future command registry

### H.1 Execution variables

Run commands from the workspace root after assigning one fresh ID. The ledger must
contain the fully expanded command and values, not just variable names.

```bash
export S045_ROOT='/Users/yifanxu/Ephemeral-AI-Lab'
export S045_PRODUCT='/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox'
export S045_TEST='/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test'
export S045_DOCS='/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs'
export S045_IMAGE='ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90'
export S045_PLAN='layerstack-phase1-stage04-5-materialization-gc-alignment'
export S045_RUN_ID='<fresh-owner-id-recorded-before-any-live-command>'
```

`S045_RUN_ID` is the only intentional future value. Resolve it once before appending
the first pending entry, then record the literal value in every command/artifact.

### H.2 Registry

Every command ID below is future and `NOT_RUN`.

| ID | Working directory | Exact command after variable expansion | Purpose |
| --- | --- | --- | --- |
| `CMD-S045-001` | root | `git -C "$S045_PRODUCT" status --short --branch` | product custody |
| `CMD-S045-002` | root | `git -C "$S045_TEST" status --short --branch` | test custody |
| `CMD-S045-003` | root | `git -C "$S045_DOCS" status --short --branch` | docs custody |
| `CMD-S045-004` | product | `rg -n 'begin_generation_retirement|finish_generation_retirement|remove_generation|remove_owned_tree' crates/sandbox-runtime/layerstack/src` | static deletion/callgraph inventory; expected zero reachable production paths |
| `CMD-S045-005` | product | `cargo fmt --all -- --check` | format |
| `CMD-S045-006` | product | `cargo clippy -p sandbox-runtime-layerstack -p sandbox-runtime -p sandbox-runtime-workspace --all-targets --all-features -- -D warnings` | focused lint with verified package names |
| `CMD-S045-007` | product | `cargo test --no-run -p sandbox-runtime-layerstack -p sandbox-runtime -p sandbox-runtime-workspace --all-features` | focused compile |
| `CMD-S045-008` | product | `cargo test -p sandbox-runtime-layerstack --test candidate_materialization --all-features -- --nocapture` | focused LayerStack tests |
| `CMD-S045-009` | product | `cargo test -p sandbox-runtime --test workspace_session_materialization --all-features -- --nocapture` | workspace/session integration |
| `CMD-S045-010` | product | `cargo test --workspace --all-features` | final product regression, not a debug loop |
| `CMD-S045-011` | product | `cargo build -p sandbox-cli --bin sandbox-catalog-export` | offline product catalog exporter |
| `CMD-S045-012` | test | `PYTHONPATH=e2e .venv/bin/python e2e/harness/catalog/collect.py --test-repository-root "$S045_TEST" --product-root "$S045_PRODUCT" --product-catalog-command "$S045_PRODUCT/target/debug/sandbox-catalog-export"` | typed catalog collection |
| `CMD-S045-013` | test | `PYTHONPATH=e2e .venv/bin/python -m pytest --collect-only -q e2e/runtime/layerstack_phase1/test_materialization_gc_alignment.py --test-repository-root "$S045_TEST" --product-root "$S045_PRODUCT"` | typed declaration inventory |
| `CMD-S045-014` | test | `E2E_IMAGE="$S045_IMAGE" E2E_REBUILD_BINARY=1 PYTHONPATH=e2e .venv/bin/python -m pytest -vv e2e/runtime/layerstack_phase1/test_materialization_gc_alignment.py -k 'S045_E05_C01' --test-repository-root "$S045_TEST" --product-root "$S045_PRODUCT"` | example exact-case debug command; substitute only another catalog node and allocate a new command ID |
| `CMD-S045-015` | test | `E2E_IMAGE="$S045_IMAGE" E2E_REBUILD_BINARY=0 PYTHONPATH=e2e .venv/bin/python -m pytest -vv e2e/runtime/layerstack_phase1/test_materialization_gc_alignment.py -k 'S045_E05_' --test-repository-root "$S045_TEST" --product-root "$S045_PRODUCT"` | example one-family rerun after rebuilt gateway |
| `CMD-S045-016` | test | `E2E_IMAGE="$S045_IMAGE" E2E_REBUILD_BINARY=1 PYTHONPATH=e2e .venv/bin/python -m pytest -vv e2e/runtime/layerstack_phase1/test_materialization_gc_alignment.py --test-repository-root "$S045_TEST" --product-root "$S045_PRODUCT"` | final complete typed correctness proof |
| `CMD-S045-017` | test | `E2E_IMAGE="$S045_IMAGE" E2E_REBUILD_BINARY=1 PYTHONPATH=e2e .venv/bin/python -m pytest -vv e2e/runtime/layerstack_phase1/test_candidate_materialization.py --test-repository-root "$S045_TEST" --product-root "$S045_PRODUCT"` | current-revision Stage 04 regression |
| `CMD-S045-018` | test | `.benchmark-state/test-venv/bin/python -m pytest -q benchmark/backend/tests/unit/test_stage04_5_materialization_gc_alignment.py` | benchmark unit/negative verifier tests |
| `CMD-S045-019` | test | `.benchmark-state/test-venv/bin/python -m pytest -q benchmark/backend/tests/contract/test_planning.py` | benchmark contract |
| `CMD-S045-020` | test | `.benchmark-state/test-venv/bin/python -m pytest -q benchmark/backend/tests/integration/test_runner.py benchmark/backend/tests/compatibility/test_artifacts.py` | benchmark integration/artifact compatibility |
| `CMD-S045-021` | test | `.benchmark-state/test-venv/bin/sandbox-benchmark validate --plan "$S045_PLAN" --test-repository-root "$S045_TEST" --product-root "$S045_PRODUCT" --product-bin-dir "$S045_PRODUCT/bin"` | frozen plan validation |
| `CMD-S045-022` | product | `bin/start-sandbox-docker-gateway --rebuild-binary` | required rebuilt live gateway |
| `CMD-S045-023` | test | `E2E_IMAGE="$S045_IMAGE" .benchmark-state/test-venv/bin/sandbox-benchmark run --plan "$S045_PLAN" --test-repository-root "$S045_TEST" --product-root "$S045_PRODUCT" --product-bin-dir "$S045_PRODUCT/bin"` | official focused 180-second campaign |
| `CMD-S045-024` | test | `.benchmark-state/test-venv/bin/python -m benchmark_lab.stage04_5_materialization_gc_alignment --verify "$S045_TEST/.benchmark-state/results/$S045_RUN_ID/stage04_5/stage04_5-materialization-gc-alignment-v1.json"` | strict raw-artifact verifier interface delivered by `S045-I15` |
| `CMD-S045-025` | test | `.benchmark-state/test-venv/bin/sandbox-benchmark recover --test-repository-root "$S045_TEST" --product-root "$S045_PRODUCT" --product-bin-dir "$S045_PRODUCT/bin"` | exact registered-run recovery |
| `CMD-S045-026` | test | `.benchmark-state/test-venv/bin/sandbox-benchmark cleanup --run-id "$S045_RUN_ID" --test-repository-root "$S045_TEST" --product-root "$S045_PRODUCT" --product-bin-dir "$S045_PRODUCT/bin"` | exact run-owned cleanup |
| `CMD-S045-027` | product | `cargo tree -p sandbox-runtime-layerstack --edges normal` | dependency-boundary input |
| `CMD-S045-028` | product | `rg -n 'legacy_v1|candidate|fallback|CONTROL' crates/sandbox-runtime/operation/src/services.rs crates/sandbox-runtime/layerstack/src/service/model.rs` | authority audit input |
| `CMD-S045-029` | docs | `git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs diff --check` | final documentation whitespace validation |

Before using any command, verify the package names and supported CLI syntax against
the checked-out repository. If the actual supported syntax differs, do not improvise:
append a new command ID and pending entry containing the corrected exact command,
preserve this row as `NOT_RUN`, and explain the correction.

### H.3 Live discipline and supported manual surfaces

The registry syntax was checked against the present Cargo manifests,
`benchmark_lab.cli`, and `e2e/harness/catalog/collect.py`; commands targeting new
Stage 04.5 files become runnable only after their `ADD` rows land. Miri, Loom,
sanitizer, fuzz, and any narrower diagnostic receive a fresh `CMD-S045-NNN` row before
execution; never reuse an ID for changed arguments, revision, configuration, or
corpus.

After `CMD-S045-022`, any manual probe must use only:

```bash
"$S045_PRODUCT/bin/sandbox-manager-cli" list_sandboxes
"$S045_PRODUCT/bin/sandbox-runtime-cli" --sandbox-id '<run-owned-sandbox-id>' exec_command ls
"$S045_PRODUCT/bin/sandbox-observability-cli" layerstack --sandbox-id '<run-owned-sandbox-id>' --window-ms 60000
```

Replace the run-owned sandbox ID with the literal ID in the pending ledger entry.
Private `/eos` mutation is never a supported probe. Debug one case, then its family,
and run `CMD-S045-016` once at the end; do not rerun an unaffected passing family.

## I. Focused 180-second benchmark campaign

### I.1 One runner-owned clock

The official operation ID is:

```text
stage04_5_materialization_gc_alignment_campaign
```

Locked builds, fixture generation, fixture/image/corpus digest checks, capability
probes, plan validation, conflict/owner checks, and allocation of the unique artifact
root occur outside the clock and are applied identically to both arms. A failure in
any prerequisite prevents admission. The runner then takes its monotonic start
timestamp immediately before the first campaign topology creation or pre-sample and
owns one 180-second deadline:

```text
t0       campaign clock starts
t0..150  topology/pre-sample, warmups, ABBA/complement measured admissions, sampling
t=150    stop every new admission exactly
t=150..180
         settle already-admitted work; final samples; serialize+fsync artifact;
         strict verifier; exact cleanup; quiescence; durable cleanup ledger
t=180    anything still required or executing => FAIL
```

Each individual operation has a 60-second deadline. A retry inherits the original
campaign and operation start/deadline; it never restarts either clock. Cleanup after
180 seconds may protect the host but cannot convert the run to `PASS`; record
`post_overrun_cleanup_ns`.

The final artifact records `campaign_start_ns`, `admission_stop_ns`,
`last_admission_ns`, `deadline_ns`, `campaign_end_ns`, maximum operation duration,
cleanup-ledger durable time, and post-overrun cleanup.

### I.2 Deterministic 180-second window allocation

The half-open windows total exactly 180 seconds. The runner uses a frozen seed and
smallest safe ABBA plus BAAB blocks within each measurement window. Work that cannot
complete within its window is stopped from further admission; an already-admitted
operation may settle only before its 60-second operation deadline and the campaign
deadline. This schedule prioritizes coverage, not fictitious sufficiency: a cell with
fewer than 20 valid samples per arm remains `INSUFFICIENT_SAMPLE`, and p99 with fewer
than 100 remains diagnostic-only.

| Benchmark ID | Window | Seconds | Admissions allowed | Deterministic work |
| --- | --- | ---: | --- | --- |
| `S045-B01` | `[0,5)` | 5 | topology only | create matched topology, idle/resource/allocated-byte pre-sample |
| `S045-B02` | `[5,25)` | 20 | yes | matched publication lock wait/hold and zero forbidden-work blocks |
| `S045-B03` | `[25,45)` | 20 | yes | warm resolve/session/mount, no-op and sustained command blocks |
| `S045-B04` | `[45,62)` | 17 | yes | PTY create/drain/input/control-C/control-D semantic/latency blocks |
| `S045-B05` | `[62,82)` | 20 | yes | public sequential, 4-KiB random, metadata, and many-small-file blocks |
| `S045-B06` | `[82,102)` | 20 | yes | cold private build and squash throughput/peak-space sentinels |
| `S045-B07` | `[102,118)` | 16 | yes | same-key waiter and disjoint-key target/cap sentinels |
| `S045-B08` | `[118,132)` | 14 | yes | 64-record paging, 4× history, crash/restart sentinels |
| `S045-B09` | `[132,150)` | 18 | yes | foreground command/file/PTY blocks while maintenance is active |
| `S045-B10` | `[150,156)` | 6 | no | settle only already-admitted work within original deadlines |
| `S045-B11` | `[156,162)` | 6 | no | final space/resource/route/lock/lifecycle samples |
| `S045-B12` | `[162,168)` | 6 | no | serialize raw artifact and SHA manifest; fsync files/parents |
| `S045-B13` | `[168,173)` | 5 | no | strict recomputation/verifier and negative-presence checks |
| `S045-B14` | `[173,178)` | 5 | no | exact run-owned cleanup through supported runner ownership |
| `S045-B15` | `[178,180)` | 2 | no | quiescence sample and durable cleanup-ledger file/parent fsync |

### I.3 Pairing and sufficiency

- Use deterministic randomized blocks containing ABBA and its complement BAAB.
- Match baseline/proposal source, image, host, filesystem, caps, corpus, cache state,
  request semantics, setup, verification, cleanup, and order.
- Record warmups separately and exclude them from inferential samples.
- Required p50/p95 cells have at least 20 valid raw samples per arm per cell.
- Report p99 only when `n >= 100`; otherwise label p99 `INSUFFICIENT_SAMPLE`.
- A required p50/p95 cell with fewer than 20 valid samples per arm is
  `INSUFFICIENT_SAMPLE`, not `PASS`.
- Other matrix cells that cannot fit the focused campaign remain `OPEN`; do not infer
  them from a covering cell.
- Preserve every rejection, timeout, outlier classification, failed/superseded run,
  and raw sample.

### I.4 Required time gates

For additive latency gates, calculate and store:

```text
allowed_ns = baseline_stat_ns * (1 + percent) + floor_ns
```

Record baseline statistic, percent, floor, computed threshold, proposal statistic,
delta, sample counts, MAD, maximum, ops/s or bytes/s, and decision.

| Cell | Required gate |
| --- | --- |
| warm root resolve/session preparation p50/p95 | `baseline + 5% + 2 ms`; zero CAS payload reads |
| OverlayFS mount p50/p95 | `baseline + 5% + 2 ms` |
| squash frozen interval p50/p95 | `baseline + 5% + 2 ms` |
| full squash plan/build/commit p50/p95 | `baseline + 10% + 5 ms` |
| cold hydration throughput | `>=70%` verified same-filesystem native sequential copy |
| cold activation p95 | `<=1.5x` verified native-copy control plus warm-mount allowance |
| no-op `exec_command(["ls"])` p50/p95 | direct ready `docker exec <id> ls` baseline `+3% +0.5 ms` |
| sustained native command throughput | `>=97%` raw LayerStack baseline |
| PTY create p50/p95 | `baseline +3% +1 ms` |
| PTY drain/write/control-C/control-D p50/p95 | `baseline +3% +0.5 ms` |
| unsupported PTY operations | exact current deterministic unsupported response |
| native sequential file read/write | `>=97%` baseline throughput |
| small-edit publish p95 | `baseline +15% +5 ms`; report scanned/newly retained bytes |
| disjoint publication | `>=90%` baseline throughput with OCC preserved |
| metadata/small/random file p50/p95 | `baseline +5% +2 ms`; report p99/max |
| publication lock p50/p95 | pre-alignment selector switch `+5% +2 ms`; also report p99/max |
| foreground during maintenance | each operation retains its own hard gate; report off/on delta/timeouts |
| operation duration | `<=60 s` |

All writer-lock forbidden-work counters must be zero.

### I.5 Resource and scale gates

Record time series and high-water values for:

- total and adjusted RSS, paired idle RSS, storage-owned live bytes, allocator RSS;
- byte/disk reservations and materialization target bytes;
- workers active/queued/joined;
- queue descriptors and encoded bytes;
- per-operation/global FDs;
- mappings;
- flight owners and waiters by key;
- common operations by phase/kind;
- root/source/generation/session/operation holds;
- active/pinned generations;
- recovery pages, records, retries, and residue;
- writer-lock wait/hold and forbidden-work events.

Gates:

- qualification RSS `<=384 MiB` absolute and `<=128 MiB` above paired idle;
- adjusted peak/final median range `<=16 MiB`;
- a 4x input/root increase adds `<=8 MiB` adjusted RSS;
- a 4x historical-directory increase adds `<=8 MiB` adjusted peak RSS;
- recovery slice `<=64` records;
- workers `<=4`, targets `<=4`, mappings `=0`;
- same-key waiters `<=16`;
- `sum(T_build) <= W_mat = min(4 GiB, 10% capacity)`;
- all §D.7 caps hold continuously.

### I.6 Physical allocated-byte accounting

Use allocated physical bytes, not apparent length. Snapshot before, at peak, after
operation, and after bounded quiescence. Separate:

1. unique logical payload;
2. current native materialization;
3. old exact leased/pinned generations;
4. private replacement target;
5. operation staging and metadata;
6. loose payload;
7. packed payload;
8. locator metadata;
9. duplicate old/new overlap;
10. v1 rollback-authority bytes;
11. abandoned operation residue;
12. unreachable but not Stage 05-reclaimed bytes;
13. workspace upper/work bytes;
14. allocator RSS and page-cache occupancy, outside disk totals.

Required shapes:

- cold build: one complete target plus at most 5% target overhead, all sources
  retained;
- replacement/squash: one replacement plus old/current/leased generations;
- crash recovery: admitted target plus exact recorded residue, no duplicate retry
  target;
- ENOSPC: abort before visibility when pre-switch and never delete a source;
- read-only/no-op command, PTY without writes, file read, `stat`, and `readdir`:
  zero new durable LayerStack operation/generation/root/object/pack/locator/staging
  bytes after quiescence;
- mutation: every byte attributed to session upper/work or explicit publication;
- unexpected LayerStack-owned quiescent residue: zero.

Before Stage 05 convergence, retained old published generations are expected and fully
attributed, but settled-space efficiency stays `OPEN`. After Stage 05 convergence:

| Metric | Target | Hard failure |
| --- | ---: | ---: |
| mixed/no-dedup | `<=1.08 * D_ideal` | `>1.15 * D_ideal` |
| many-small-file | `<=1.15 * D_ideal` | `>1.25 * D_ideal` |
| avoidable native-plus-pack duplication | `<=1%` | `>3%` |
| settled pack dead bytes/slack | `<=2%` | `>5%` |
| unexplained unreachable/unleased payload | 0 | any persistent byte |
| native depth | preemptively below 64 | exceeds 64 |

### I.7 Strict artifact

The official JSON artifact includes:

- schema name/version and campaign/run/owner IDs;
- expanded command and environment;
- all source/build/runtime/corpus/host/filesystem identities;
- full cap configuration;
- clock fields;
- ordered raw sample records;
- raw time, space, resource, route, lock, lifecycle, and cleanup streams;
- formula inputs and computed thresholds;
- per-cell counts and sufficiency;
- case/corpus hashes;
- every verdict with exact reason;
- exact artifact paths and SHA-256 manifest;
- durable cleanup ledger and quiescence proof.

The strict verifier recomputes statistics, thresholds, high-water values, allocated
space, clock compliance, sample sufficiency, and checksums from raw records. A summary
that cannot be recomputed is invalid.

## J. Requirement-to-proof traceability

### J.1 Closed requirement and evidence registers

These IDs group the normative clauses without weakening them; each group is closed by
the exact verification rows below.

| Register | Concrete gate |
| --- | --- |
| `S045-G01` | source/custody reconciled and no 04.5 deletion/retirement authority |
| `S045-G02` | sole four-state common lifecycle, private build, immutable Ready |
| `S045-G03` | bounded common publication, sole selector, GC admission, exact handoff |
| `S045-G04` | shared bounded governor, lock order, all hard caps, owned shutdown |
| `S045-G05` | bounded fair recovery, strict corruption, no history-derived choice |
| `S045-G06` | exact reader/session generation and fence across switch |
| `S045-G07` | crash/short-write/torn/`EIO`/response-loss/ENOSPC safety |
| `S045-G08` | Stage 03/04 identities and strict command/file/PTY behavior |
| `S045-G09` | matched 180-second time/space/resource campaign and sufficiency |
| `S045-G10` | v1 authority, evidence custody, exact cleanup, docs, handoff |
| `S045-R01` | byte/disk/worker/target/queue/FD/hold/generation/operation/retry/page caps |
| `S045-R02` | RSS/live-byte/history scaling and zero mappings |
| `S045-R03` | allocated-byte buckets, read-only zero growth, mutation attribution |
| `S045-R04` | writer-lock wait/hold and zero forbidden work |
| `S045-R05` | cancellation/panic/restart/shutdown cleanup and quiescence |
| `S045-A01` | prerequisite/custody/catalog/plan identity manifest |
| `S045-A02` | versioned raw campaign artifact and SHA-256 manifest |
| `S045-A03` | strict recomputing verifier plus negative rejection suite |
| `S045-A04` | durable exact-owner cleanup ledger and final quiescence sample |
| `S045-D01` | dependency, portable-core, `unsafe`, mapping, decoder, owner inventories |
| `S045-D02` | `legacy_v1` public R/W; candidate/fallback/CONTROL unchanged |
| `S045-D03` | Stage 05/06/07 authority boundaries and explicit deferrals |
| `S045-H01` | evidence-backed Stage 04.5 handoff to Stage 05 |

### J.2 Verification matrix

`—` means no artifact exists. Every row is initially honest; direct Stage 04.5
execution is required before `PASS`.

| Verification ID | Requirement/invariant | Layer and exact case/work | Command ID | Required artifact/counters | Exact threshold/result | Initial | Artifact/digest | Cleanup proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S045-V01` | reading, custody, hashes, owners | `S045-G01`, `S045-A01`, `S045-E01-C02-unsafe-dependency-inventory` | `CMD-S045-001`, `CMD-S045-002`, `CMD-S045-003` | custody JSON, all §A.6 hashes, dirty flags | exact match or explained diff; no owner ambiguity | `NOT_RUN` | — | no live resource |
| `S045-V02` | no deletion/retirement; layout retention | `S045-I01`, `S045-E01-C01-deletion-apis-unreachable`, `S045-E04-C03-reader-release-no-stage045-delete` | `CMD-S045-004`, `CMD-S045-008`, `CMD-S045-016` | symbols/callers, unlink counters, allocated tree | zero reachable production delete/retire and zero 04.5 published unlink | `OPEN` | — | exact test roots only |
| `S045-V03` | `STATE` sole truth; four states; private/immutable Ready | `S045-I02`, `S045-I04`, `S045-L01`, `S045-L02`, `S045-L03`, `S045-E02` | `CMD-S045-008`, `CMD-S045-016` | codec vectors, phase/tree/sync/manifest digest | only four phases; encodings ≤256 KiB; CURRENT unchanged before publish | `OPEN` | — | operation-owned work reconciled |
| `S045-V04` | lock order and bounded critical section | `S045-I03`, `S045-L06`, `S045-E03-C02-gc-starts-at-publish`, `S045-E07-C05-lock-order`, `S045-R04` | `CMD-S045-008`, `CMD-S045-016`, `CMD-S045-023` | rank trace, wait/hold, forbidden counters | every forbidden-work counter=0; no inversion | `OPEN` | — | all lock owners released |
| `S045-V05` | sole atomic selector and private visibility | `S045-I05`, `S045-L04`, `S045-E02-C01-private-build-invisible`, `S045-E02-C02-ready-invisible-immutable`, `S045-E02-C03-initial-common-publish` | `CMD-S045-008`, `CMD-S045-016` | selector digests, parent-fsync witness, target count | exact old before switch and exact Ready after; one selector/target | `OPEN` | — | exact operation cleanup |
| `S045-V06` | active-GC admission and exact old handoff | `S045-I05`, `S045-L05`, `S045-L06`, `S045-L07`, `S045-E03`, `S045-E11-C03-stage05-bridge-contract` | `CMD-S045-016` | root-log/selector ordering, handoff subject/fence/retry | admission durable before visibility; disabled replacement does not switch; exact old handoff | `OPEN` | — | GC fixture and operation reconciled |
| `S045-V07` | shared owner and every hard cap | `S045-I03`, `S045-I07`, `S045-R01`, `S045-E07`, `S045-E08-C06-resource-cap-matrix` | `CMD-S045-008`, `CMD-S045-016`, `CMD-S045-023` | all §D.7 time-series highs/rejections | caps exactly §D.7; mappings excluded to V12; rejected request creates no owner | `OPEN` | — | workers joined, permits returned |
| `S045-V08` | durability faults and ENOSPC fail closed | `S045-G07`, `S045-L08`, `S045-L09`, `S045-E05` | `CMD-S045-014`, `CMD-S045-015`, `CMD-S045-016` | per-failpoint old/new digests, I/O boundary, retained inventory | exact old/new only; no substitute/delete/duplicate target | `NOT_RUN` | — | recovery then exact owner cleanup |
| `S045-V09` | exact reader generation/fence | `S045-I09`, `S045-L10`, `S045-E04` | `CMD-S045-009`, `CMD-S045-016` | lease/selector/content/fence tuples | old reader stays old; new reader exact new; ABA rejected; release no delete | `OPEN` | — | tasks/mounts/FDs then lease |
| `S045-V10` | bounded fair recovery | `S045-I02`, `S045-I03`, `S045-L11`, `S045-E06`, `S045-E05-C13-state-short-write` | `CMD-S045-008`, `CMD-S045-016` | cursors/pages/kinds/retries/scans/residue | ≤64 records/page; retries≤8; no total collect/sort/max/mtime repair | `OPEN` | — | dispatcher idle; residue explained |
| `S045-V11` | strict hostile decode and memory safety tools | `S045-D01`, `S045-E08-C01-state-hostile-decode`, `S045-E08-C02-manifest-hostile-decode`, `S045-E08-C03-path-escape`, `S045-E08-C04-offset-extent-overflow`, `S045-E08-C05-depth-64-and-65`, `S045-E08-C08-miri-loom-sanitizer` | `CMD-S045-008`, `CMD-S045-016` | corpus/tool versions/findings/allocation peaks | typed rejection before allocation/access; depth 64 yes/65 no; unsupported cell `NOT_RUN` | `OPEN` | — | tool temp removed |
| `S045-V12` | RSS, resource stability, zero mappings | `S045-R02`, `S045-E06-C03-history-no-collect-sort`, `S045-E08-C07-zero-mappings`, `S045-E10` | `CMD-S045-016`, `CMD-S045-023` | raw RSS/live bytes/mappings/resource series | RSS ≤384 MiB and ≤128 MiB over idle; range ≤16 MiB; 4× deltas ≤8 MiB; mappings=0 | `NOT_RUN` | — | V16 quiescence |
| `S045-V13` | strict native tree/command/file/PTY correctness | `S045-G08`, `S045-E02-C06-required-tree-capability-shapes`, `S045-E09` | `CMD-S045-009`, `CMD-S045-016`, `CMD-S045-017` | route counters, exit/bytes/status/tree/capability digests | exact baseline semantics; candidate fallback=0; unsupported PTY remains exact | `OPEN` | — | supported session teardown |
| `S045-V14` | squash producer convergence/identity | `S045-I06`, `S045-E02-C05-repair-and-squash-common-publisher`, `S045-B06` | `CMD-S045-008`, `CMD-S045-016`, `CMD-S045-023` | RootId/AttributionRootId, route, peak space | same private Ready/common publisher; identities unchanged | `OPEN` | — | exact squash operation |
| `S045-V15` | read-only zero growth and mutation ownership | `S045-R03`, `S045-E09-C01-noop-command-old-new`, `S045-E09-C05-file-read-metadata`, `S045-E09-C06-file-write-rename-fsync`, `S045-E09-C07-file-unlink-teardown`, `S045-E09-C08-explicit-publish-separation` | `CMD-S045-016`, `CMD-S045-023` | before/peak/after/quiescent allocated buckets | read-only durable LayerStack delta=0; every mutating byte session/publish-owned | `NOT_RUN` | — | final buckets after exact teardown |
| `S045-V16` | exact cleanup/quiescence | `S045-L12`, `S045-R05`, `S045-A04`, `S045-E10-C03-exact-cleanup`, `S045-B14`, `S045-B15` | `CMD-S045-016`, `CMD-S045-025`, `CMD-S045-026` | before/after owner inventory, durable ledger, residue | zero run-owned live resources and zero unexplained residue; unrelated sentinels unchanged | `NOT_RUN` | — | this row is cleanup proof |
| `S045-V17` | dependencies and Stage 03/04 regression | `S045-D01`, `S045-E11-C01-stage03-root-regression`, `S045-E11-C02-stage04-strict-regression` | `CMD-S045-017`, `CMD-S045-027` | tree/delta/unsafe inventory, direct regression records | approved boundaries; exact identities/OCC; complete current-revision Stage 04 proof | `NOT_RUN` | — | exact test owners |
| `S045-V18` | v1 and later-stage authority | `S045-D02`, `S045-D03`, `S045-E01-C03-v1-authority-static`, `S045-E11-C04-stage06-authority`, `S045-E11-C05-stage07-deferrals` | `CMD-S045-016`, `CMD-S045-028` | route/CONTROL/candidate/fallback/deferral record | v1 public R/W; candidate/fallback false; CONTROL unchanged; no Stage 05/07 authority | `OPEN` | — | no authority residue |
| `S045-V19` | append-only ledger and complete catalog | `S045-I11`, `S045-I13`, `S045-I14`, `S045-A01` | `CMD-S045-011`, `CMD-S045-012`, `CMD-S045-013`, `CMD-S045-016` | catalog/result IDs+hashes, pending-before-run entries | no duplicate/missing result; every live command prelogged | `OPEN` | — | catalog is side-effect-free |
| `S045-V20` | exact 180/150/60 clock | `S045-G09`, `S045-B01`, `S045-B10`, `S045-B15` | `CMD-S045-018`, `CMD-S045-021`, `CMD-S045-023`, `CMD-S045-024` | monotonic clock fields and window records | duration≤180 s; admission stop=150 s; operation≤60 s; no clock reset | `NOT_RUN` | — | V16 before deadline |
| `S045-V21` | warm resolve/session/mount latency | `S045-B03` | `CMD-S045-023`, `CMD-S045-024` | matched raw samples/stats/formula | p50/p95≤baseline×1.05+2 ms; zero CAS payload reads | `NOT_RUN` | — | V16 |
| `S045-V22` | command performance | `S045-B03`, `S045-B09`, `S045-E09-C02-sustained-command` | `CMD-S045-023`, `CMD-S045-024` | no-op/sustained raw samples, routes | no-op p50/p95≤baseline×1.03+0.5 ms; sustained≥97%; op≤60 s | `NOT_RUN` | — | V16 |
| `S045-V23` | PTY performance/semantics | `S045-B04`, `S045-B09`, `S045-E09-C03-pty-supported-lifecycle`, `S045-E09-C04-pty-unsupported-deterministic` | `CMD-S045-023`, `CMD-S045-024` | raw PTY samples/byte/status records | create≤baseline×1.03+1 ms; drain/input/C/D≤baseline×1.03+0.5 ms | `NOT_RUN` | — | V16 |
| `S045-V24` | cold build, squash, recovery/history performance/resources | `S045-B06`, `S045-B08`, `S045-R02` | `CMD-S045-023`, `CMD-S045-024` | throughput/activation/RSS/page raw series | hydration≥70%; activation p95≤1.5×control+warm allowance; recovery≤64; 4× history RSS≤8 MiB | `NOT_RUN` | — | V16 |
| `S045-V25` | file and physical-space gates | `S045-B05`, `S045-R03`, `S045-E05-C08-enospc-before-publish`, `S045-E05-C09-enospc-after-publish` | `CMD-S045-023`, `CMD-S045-024` | allocated buckets and file raw samples | file throughput≥97%; metadata p50/p95≤baseline×1.05+2 ms; §I.6 shapes; unexplained bytes=0 | `NOT_RUN` | — | V16 |
| `S045-V26` | publication/squash/maintenance time gates | `S045-B02`, `S045-B06`, `S045-B09`, `S045-R04` | `CMD-S045-023`, `CMD-S045-024` | lock/squash/small-edit/disjoint/interference samples | exact §I.4 thresholds including squash 5%/2 ms and 10%/5 ms, small edit 15%/5 ms, disjoint≥90% | `NOT_RUN` | — | V16 |
| `S045-V27` | matching and sample sufficiency | `S045-B02`, `S045-B03`, `S045-B04`, `S045-B05`, `S045-B06`, `S045-B07`, `S045-B08`, `S045-B09` | `CMD-S045-021`, `CMD-S045-023`, `CMD-S045-024` | ABBA/BAAB blocks, counts, MAD/max/formulas | p50/p95 n≥20/arm/cell; p99 only n≥100; otherwise exact insufficiency/open | `NOT_RUN` | — | V16 |
| `S045-V28` | strict artifact/verifier soundness | `S045-I15`, `S045-I16`, `S045-I17`, `S045-A02`, `S045-A03`, `S045-B12`, `S045-B13` | `CMD-S045-018`, `CMD-S045-019`, `CMD-S045-020`, `CMD-S045-024` | schema/raw streams/SHA manifest/negative results | raw recomputation exact; reject missing/unmatched/insufficient/late/unowned/false-zero/non-quiescent | `OPEN` | — | V16 referenced and verified |
| `S045-V29` | docs, checklist, status, and handoff closure | `S045-I18`, `S045-I19`, `S045-I20`, `S045-H01`, `S045-G10` | `CMD-S045-029` | link/ID/status audit, final diffs, handoff | no orphan/duplicate ID, no authority drift, every PASS has command+raw SHA+threshold+cleanup | `OPEN` | — | V16 artifact linked |

No row becomes `PASS` from code inspection, a diff, unit tests alone, inherited Stage
04 proof, or a missing counter interpreted as zero.

## K. Canonical progress tracker

This is the single progress authority. Only these rows change status. Preserve failed,
interrupted, insufficient, and superseded artifacts. `PASS` requires a direct Stage
04.5 command result, retained raw artifact, SHA-256, exact threshold/result, and
cleanup proof. Inspection, a diff, prose, or inherited evidence cannot pass a runtime
row; missing accounting is `OPEN`, never zero; `—` means no artifact exists. Cleanup
after 180 seconds cannot satisfy a campaign row, and no runtime row passes with a live
run-owned resource or unexplained residue.

For compactness, “condition” cites the exact verification row, which contains the
command, result, threshold, artifact, and cleanup contract. Individual E2E child rows
follow the core tracker and are equally canonical.

| Work ID | Depends on | Deliverable | Initial status | Completion condition / verification | Run/artifact + digest | Owner/blocker | Cleanup result | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S045-G01` | `S045-A01`, `S045-D01` | reconciled source/custody and no deletion | `OPEN` | `S045-V01`, `S045-V02` | — | product+evidence owner | — | 2026-07-26 |
| `S045-G02` | `S045-I02`, `S045-I04` | four-state private-build lifecycle | `OPEN` | `S045-V03`, `S045-V05` | — | LayerStack | — | 2026-07-26 |
| `S045-G03` | `S045-I05` | common publication/GC/handoff | `OPEN` | `S045-V04`, `S045-V05`, `S045-V06` | — | LayerStack/Stage 05 bridge | — | 2026-07-26 |
| `S045-G04` | `S045-I03`, `S045-I07` | bounded governor/lock/ownership | `OPEN` | `S045-V04`, `S045-V07` | — | storage supervisor | — | 2026-07-26 |
| `S045-G05` | `S045-I02`, `S045-I03` | bounded fair recovery | `OPEN` | `S045-V10` | — | recovery dispatcher | — | 2026-07-26 |
| `S045-G06` | `S045-I09` | exact reader/session generation | `OPEN` | `S045-V09` | — | WorkspaceManager | — | 2026-07-26 |
| `S045-G07` | `S045-I02`, `S045-I05` | all durability faults safe | `OPEN` | `S045-V08` | — | operation/publisher | — | 2026-07-26 |
| `S045-G08` | `S045-I06`, `S045-I08`, `S045-I09` | identities and strict public behavior | `OPEN` | `S045-V13`, `S045-V14`, `S045-V17` | — | runtime/workspace | — | 2026-07-26 |
| `S045-G09` | `S045-I15`, `S045-I16`, `S045-I17` | matched 180-second proof | `OPEN` | `S045-V20` through `S045-V28` | — | benchmark runner | — | 2026-07-26 |
| `S045-G10` | all other gate rows | authority/evidence/cleanup/docs/handoff closure | `OPEN` | `S045-V16`, `S045-V18`, `S045-V19`, `S045-V29` | — | stage owner | — | 2026-07-26 |
| `S045-I01` | `S045-G01` | deletion/history-selection removal | `OPEN` | `S045-V02` | — | LayerStack | — | 2026-07-26 |
| `S045-I02` | `S045-I01` | common state/codec | `OPEN` | `S045-V03`, `S045-V10` | — | LayerStack | — | 2026-07-26 |
| `S045-I03` | `S045-I02` | shared governor/lock/recovery ownership | `OPEN` | `S045-V04`, `S045-V07`, `S045-V10` | — | storage | — | 2026-07-26 |
| `S045-I04` | `S045-I02`, `S045-I03` | private streamed Ready producer | `OPEN` | `S045-V03`, `S045-V07` | — | native backend | — | 2026-07-26 |
| `S045-I05` | `S045-I03`, `S045-I04` | common publisher and Stage 05 seam | `OPEN` | `S045-V05`, `S045-V06` | — | publisher | — | 2026-07-26 |
| `S045-I06` | `S045-I04`, `S045-I05` | squash convergence | `OPEN` | `S045-V14` | — | squash owner | — | 2026-07-26 |
| `S045-I07` | `S045-I03`, `S045-I05` | service ownership/observability | `OPEN` | `S045-V07`, `S045-V12`, `S045-V16` | — | service | — | 2026-07-26 |
| `S045-I08` | `S045-I05`, `S045-I07` | dependency wiring/public model | `OPEN` | `S045-V17`, `S045-V18` | — | operation service | — | 2026-07-26 |
| `S045-I09` | `S045-I05`, `S045-I08` | exact session/lease lifecycle | `OPEN` | `S045-V09`, `S045-V15` | — | workspace | — | 2026-07-26 |
| `S045-I10` | `S045-I01`, `S045-I02`, `S045-I03`, `S045-I04`, `S045-I05`, `S045-I06`, `S045-I07`, `S045-I08`, `S045-I09` | focused product proof | `OPEN` | `S045-V02` through `S045-V18` | — | product tests | — | 2026-07-26 |
| `S045-I11` | `S045-I10` | typed E2E declarations | `OPEN` | `S045-V19` and every E child | — | E2E | — | 2026-07-26 |
| `S045-I12` | `S045-I11` | fixtures/helpers/failpoints | `OPEN` | `S045-V03`, `S045-V08`, `S045-V16` | — | E2E | — | 2026-07-26 |
| `S045-I13` | `S045-I11` | catalog/schema | `OPEN` | `S045-V19` | — | E2E catalog | — | 2026-07-26 |
| `S045-I14` | every live command | append-only report | `OPEN` | `S045-V19` | — | evidence ledger | — | 2026-07-26 |
| `S045-I15` | `S045-I10`, `S045-I12` | campaign/artifact/verifier module | `OPEN` | `S045-V20`, `S045-V21`, `S045-V22`, `S045-V23`, `S045-V24`, `S045-V25`, `S045-V26`, `S045-V27`, `S045-V28` | — | benchmark | — | 2026-07-26 |
| `S045-I16` | `S045-I15` | runner/plan/recovery registration | `OPEN` | `S045-V20`, `S045-V28` | — | benchmark | — | 2026-07-26 |
| `S045-I17` | `S045-I15`, `S045-I16` | contract/unit/integration/negative tests | `OPEN` | `S045-V28` | — | benchmark tests | — | 2026-07-26 |
| `S045-I18` | all direct proof | authoritative docs reconciliation | `OPEN` | `S045-V29` | — | docs owner | — | 2026-07-26 |
| `S045-I19` | `S045-I18` | index/frozen handoff custody | `OPEN` | `S045-V01`, `S045-V29` | — | docs owner | — | 2026-07-26 |
| `S045-I20` | `S045-I18`, `S045-I19` | Stage 05 handoff | `OPEN` | `S045-V29` | — | docs owner | — | 2026-07-26 |
| `S045-L01` | `S045-I03` | admission to Building | `OPEN` | `S045-V03`, `S045-V07` | — | operation | — | 2026-07-26 |
| `S045-L02` | `S045-L01` | private reconstruction | `OPEN` | `S045-V03`, `S045-V07` | — | operation | — | 2026-07-26 |
| `S045-L03` | `S045-L02` | immutable Ready | `OPEN` | `S045-V03` | — | operation | — | 2026-07-26 |
| `S045-L04` | `S045-L03` | initial publish | `OPEN` | `S045-V05` | — | publisher | — | 2026-07-26 |
| `S045-L05` | `S045-L03` | replacement preflight | `OPEN` | `S045-V06` | — | bridge | — | 2026-07-26 |
| `S045-L06` | `S045-L05` | active-GC publication | `OPEN` | `S045-V04`, `S045-V06` | — | publisher/GC | — | 2026-07-26 |
| `S045-L07` | `S045-L06` | old-subject handoff | `OPEN` | `S045-V06`, `S045-V09` | — | bridge | — | 2026-07-26 |
| `S045-L08` | `S045-L01` | pre-publish failure/cancel | `OPEN` | `S045-V08`, `S045-V10` | — | operation | — | 2026-07-26 |
| `S045-L09` | `S045-L03` | crash/response loss | `OPEN` | `S045-V08`, `S045-V10` | — | recovery | — | 2026-07-26 |
| `S045-L10` | `S045-L04`, `S045-L07` | reader admission/release | `OPEN` | `S045-V09` | — | workspace | — | 2026-07-26 |
| `S045-L11` | `S045-I03` | bounded recovery schedule | `OPEN` | `S045-V10` | — | recovery | — | 2026-07-26 |
| `S045-L12` | all lifecycle rows | shutdown/cleanup | `OPEN` | `S045-V07`, `S045-V16` | — | supervisor | — | 2026-07-26 |
| `S045-R01` | `S045-I03`, `S045-I07` | all hard caps | `OPEN` | `S045-V07` | — | supervisor | — | 2026-07-26 |
| `S045-R02` | `S045-I07` | RSS/history/mappings | `NOT_RUN` | `S045-V12`, `S045-V24` | — | benchmark | — | 2026-07-26 |
| `S045-R03` | `S045-I12`, `S045-I15` | allocated space/attribution | `NOT_RUN` | `S045-V15`, `S045-V25` | — | E2E/benchmark | — | 2026-07-26 |
| `S045-R04` | `S045-I03`, `S045-I05` | writer-lock proof | `OPEN` | `S045-V04`, `S045-V26` | — | publisher | — | 2026-07-26 |
| `S045-R05` | `S045-I03`, `S045-I07` | cancel/restart/shutdown quiescence | `OPEN` | `S045-V16` | — | supervisor/runner | — | 2026-07-26 |
| `S045-A01` | `S045-I13`, `S045-I14` | prerequisite/custody/catalog manifest | `OPEN` | `S045-V01`, `S045-V19` | — | evidence owner | — | 2026-07-26 |
| `S045-A02` | `S045-I15` | versioned raw artifact/SHA manifest | `OPEN` | `S045-V28` | — | benchmark | — | 2026-07-26 |
| `S045-A03` | `S045-I17` | strict verifier/negative suite | `OPEN` | `S045-V28` | — | benchmark | — | 2026-07-26 |
| `S045-A04` | `S045-I16`, `S045-R05` | durable cleanup ledger/quiescence | `NOT_RUN` | `S045-V16` | — | runner | — | 2026-07-26 |
| `S045-B01` | `S045-A01` | topology/pre-sample `[0,5)` | `NOT_RUN` | `S045-V20` | — | runner | — | 2026-07-26 |
| `S045-B02` | `S045-B01` | lock `[5,25)` | `NOT_RUN` | `S045-V26`, `S045-V27` | — | runner | — | 2026-07-26 |
| `S045-B03` | `S045-B01` | warm command `[25,45)` | `NOT_RUN` | `S045-V21`, `S045-V22`, `S045-V27` | — | runner | — | 2026-07-26 |
| `S045-B04` | `S045-B01` | PTY `[45,62)` | `NOT_RUN` | `S045-V23`, `S045-V27` | — | runner | — | 2026-07-26 |
| `S045-B05` | `S045-B01` | file `[62,82)` | `NOT_RUN` | `S045-V25`, `S045-V27` | — | runner | — | 2026-07-26 |
| `S045-B06` | `S045-B01` | cold/squash `[82,102)` | `NOT_RUN` | `S045-V14`, `S045-V24`, `S045-V26`, `S045-V27` | — | runner | — | 2026-07-26 |
| `S045-B07` | `S045-B01` | concurrency `[102,118)` | `NOT_RUN` | `S045-V07`, `S045-V27` | — | runner | — | 2026-07-26 |
| `S045-B08` | `S045-B01` | recovery `[118,132)` | `NOT_RUN` | `S045-V24`, `S045-V27` | — | runner | — | 2026-07-26 |
| `S045-B09` | `S045-B01` | interference `[132,150)` | `NOT_RUN` | `S045-V22`, `S045-V23`, `S045-V26`, `S045-V27` | — | runner | — | 2026-07-26 |
| `S045-B10` | `S045-B09` | settle `[150,156)` | `NOT_RUN` | `S045-V20` | — | runner | — | 2026-07-26 |
| `S045-B11` | `S045-B10` | final samples `[156,162)` | `NOT_RUN` | `S045-V12`, `S045-V15`, `S045-V20` | — | runner | — | 2026-07-26 |
| `S045-B12` | `S045-B11` | serialize/fsync `[162,168)` | `NOT_RUN` | `S045-V28` | — | runner | — | 2026-07-26 |
| `S045-B13` | `S045-B12` | verify `[168,173)` | `NOT_RUN` | `S045-V28` | — | runner | — | 2026-07-26 |
| `S045-B14` | `S045-B13` | cleanup `[173,178)` | `NOT_RUN` | `S045-V16` | — | runner | — | 2026-07-26 |
| `S045-B15` | `S045-B14` | quiesce/ledger `[178,180)` | `NOT_RUN` | `S045-V16`, `S045-V20` | — | runner | — | 2026-07-26 |
| `S045-D01` | `S045-A01` | dependency/unsafe/mapping/owner audit | `OPEN` | `S045-V11`, `S045-V17` | — | architecture owner | — | 2026-07-26 |
| `S045-D02` | `S045-I08` | v1 public authority | `OPEN` | `S045-V18` | — | operation service | — | 2026-07-26 |
| `S045-D03` | `S045-I05`, `S045-D02` | Stage 05/06/07 boundaries | `OPEN` | `S045-V06`, `S045-V18` | — | stage owner | — | 2026-07-26 |
| `S045-H01` | `S045-I18`, `S045-I19`, `S045-I20`, `S045-A04` | Stage 05 handoff | `OPEN` | `S045-V29` | — | docs/stage owner | — | 2026-07-26 |

### K.1 Canonical E2E child tracker

Every exact §G case is a child row. The family contract supplies owner/deadline and
cleanup; completion additionally requires the individual raw result and SHA. The
artifact column remains `—` and updated date is 2026-07-26 for every authoring-time
row.

| Work ID | Depends on | Deliverable | Initial | Verification | Artifact+digest | Owner/blocker | Cleanup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S045-E01-C01-deletion-apis-unreachable` | `S045-I01`, `S045-I11` | direct static result | `NOT_RUN` | `S045-V02` | — | E2E | — |
| `S045-E01-C02-unsafe-dependency-inventory` | `S045-I11`, `S045-D01` | direct inventory result | `NOT_RUN` | `S045-V01`, `S045-V11`, `S045-V17` | — | E2E | — |
| `S045-E01-C03-v1-authority-static` | `S045-I08`, `S045-I11` | direct authority result | `NOT_RUN` | `S045-V18` | — | E2E | — |
| `S045-E02-C01-private-build-invisible` | `S045-I04`, `S045-I11` | direct phase/tree result | `NOT_RUN` | `S045-V03`, `S045-V05` | — | E2E | — |
| `S045-E02-C02-ready-invisible-immutable` | `S045-I04`, `S045-I11` | direct Ready result | `NOT_RUN` | `S045-V03`, `S045-V05` | — | E2E | — |
| `S045-E02-C03-initial-common-publish` | `S045-I05`, `S045-I11` | direct initial publish result | `NOT_RUN` | `S045-V05` | — | E2E | — |
| `S045-E02-C04-replacement-disabled` | `S045-I05`, `S045-I11` | direct disabled result | `NOT_RUN` | `S045-V06` | — | E2E | — |
| `S045-E02-C05-repair-and-squash-common-publisher` | `S045-I06`, `S045-I11` | direct producer result | `NOT_RUN` | `S045-V03`, `S045-V14` | — | E2E | — |
| `S045-E02-C06-required-tree-capability-shapes` | `S045-I04`, `S045-I12` | every shape result | `NOT_RUN` | `S045-V03`, `S045-V13` | — | E2E | — |
| `S045-E03-C01-gc-starts-before-ready` | `S045-I05`, `S045-I11` | direct schedule result | `NOT_RUN` | `S045-V06` | — | E2E | — |
| `S045-E03-C02-gc-starts-at-publish` | `S045-I05`, `S045-I11` | direct schedule result | `NOT_RUN` | `S045-V04`, `S045-V06` | — | E2E | — |
| `S045-E03-C03-gc-stops-at-publish` | `S045-I05`, `S045-I11` | direct schedule result | `NOT_RUN` | `S045-V06` | — | E2E | — |
| `S045-E03-C04-root-admission-fsync-failure` | `S045-I05`, `S045-I11` | direct failure result | `NOT_RUN` | `S045-V06`, `S045-V08` | — | E2E | — |
| `S045-E03-C05-handoff-failure-after-publish` | `S045-I05`, `S045-I11` | direct handoff result | `NOT_RUN` | `S045-V06`, `S045-V10` | — | E2E | — |
| `S045-E04-C01-old-reader-survives-switch` | `S045-I09`, `S045-I11` | direct lease/content result | `NOT_RUN` | `S045-V09` | — | E2E | — |
| `S045-E04-C02-new-reader-uses-new` | `S045-I09`, `S045-I11` | direct lease/content result | `NOT_RUN` | `S045-V09` | — | E2E | — |
| `S045-E04-C03-reader-release-no-stage045-delete` | `S045-I09`, `S045-I11` | direct release/tree result | `NOT_RUN` | `S045-V02`, `S045-V09` | — | E2E | — |
| `S045-E04-C04-aba-fence-rejected` | `S045-I09`, `S045-I11` | direct ABA result | `NOT_RUN` | `S045-V09` | — | E2E | — |
| `S045-E04-C05-generation-cap` | `S045-I03`, `S045-I11` | direct cap result | `NOT_RUN` | `S045-V07`, `S045-V09` | — | E2E | — |
| `S045-E05-C01-crash-building` | `S045-I02`, `S045-I11` | direct crash result | `NOT_RUN` | `S045-V08`, `S045-V10` | — | E2E | — |
| `S045-E05-C02-crash-ready` | `S045-I02`, `S045-I11` | direct crash result | `NOT_RUN` | `S045-V08` | — | E2E | — |
| `S045-E05-C03-crash-root-admission` | `S045-I05`, `S045-I11` | direct crash result | `NOT_RUN` | `S045-V08` | — | E2E | — |
| `S045-E05-C04-crash-current-replace` | `S045-I05`, `S045-I11` | direct crash result | `NOT_RUN` | `S045-V08` | — | E2E | — |
| `S045-E05-C05-crash-parent-fsync` | `S045-I05`, `S045-I11` | direct crash result | `NOT_RUN` | `S045-V08` | — | E2E | — |
| `S045-E05-C06-crash-published-before-handoff` | `S045-I05`, `S045-I11` | direct crash result | `NOT_RUN` | `S045-V08`, `S045-V10` | — | E2E | — |
| `S045-E05-C07-response-loss-idempotency` | `S045-I02`, `S045-I11` | direct retry result | `NOT_RUN` | `S045-V08`, `S045-V10` | — | E2E | — |
| `S045-E05-C08-enospc-before-publish` | `S045-I04`, `S045-I11` | direct ENOSPC result | `NOT_RUN` | `S045-V08`, `S045-V25` | — | E2E | — |
| `S045-E05-C09-enospc-after-publish` | `S045-I05`, `S045-I11` | direct ENOSPC result | `NOT_RUN` | `S045-V08`, `S045-V25` | — | E2E | — |
| `S045-E05-C10-corrupt-current` | `S045-I02`, `S045-I11` | direct corrupt-selector result | `NOT_RUN` | `S045-V08`, `S045-V11` | — | E2E | — |
| `S045-E05-C11-corrupt-state` | `S045-I02`, `S045-I11` | direct corrupt-state result | `NOT_RUN` | `S045-V08`, `S045-V11` | — | E2E | — |
| `S045-E05-C12-restart-storm-bounded` | `S045-I03`, `S045-I11` | direct restart result | `NOT_RUN` | `S045-V10` | — | E2E | — |
| `S045-E05-C13-state-short-write` | `S045-I02`, `S045-I11` | direct short-write result | `NOT_RUN` | `S045-V08`, `S045-V10` | — | E2E | — |
| `S045-E05-C14-manifest-torn-metadata` | `S045-I04`, `S045-I11` | direct torn result | `NOT_RUN` | `S045-V08`, `S045-V11` | — | E2E | — |
| `S045-E05-C15-current-write-eio` | `S045-I05`, `S045-I11` | direct EIO result | `NOT_RUN` | `S045-V08` | — | E2E | — |
| `S045-E05-C16-parent-fsync-eio` | `S045-I05`, `S045-I11` | direct EIO result | `NOT_RUN` | `S045-V08` | — | E2E | — |
| `S045-E06-C01-recovery-page-64` | `S045-I03`, `S045-I11` | direct page result | `NOT_RUN` | `S045-V10` | — | E2E | — |
| `S045-E06-C02-recovery-fairness` | `S045-I03`, `S045-I11` | direct fairness result | `NOT_RUN` | `S045-V10` | — | E2E | — |
| `S045-E06-C03-history-no-collect-sort` | `S045-I03`, `S045-I11` | direct scaling result | `NOT_RUN` | `S045-V10`, `S045-V24` | — | E2E | — |
| `S045-E06-C04-ownerless-residue-dispatched` | `S045-I03`, `S045-I11` | direct residue result | `NOT_RUN` | `S045-V10`, `S045-V16` | — | E2E | — |
| `S045-E07-C01-same-key-16-waiters` | `S045-I03`, `S045-I11` | direct concurrency result | `NOT_RUN` | `S045-V07` | — | E2E | — |
| `S045-E07-C02-same-key-waiter-17` | `S045-I03`, `S045-I11` | direct rejection result | `NOT_RUN` | `S045-V07` | — | E2E | — |
| `S045-E07-C03-disjoint-four-targets` | `S045-I03`, `S045-I11` | direct concurrency result | `NOT_RUN` | `S045-V07` | — | E2E | — |
| `S045-E07-C04-global-operation-64` | `S045-I03`, `S045-I11` | direct cap result | `NOT_RUN` | `S045-V07` | — | E2E | — |
| `S045-E07-C05-lock-order` | `S045-I03`, `S045-I11` | direct lock result | `NOT_RUN` | `S045-V04` | — | E2E | — |
| `S045-E07-C06-no-forbidden-lock-work` | `S045-I05`, `S045-I11` | direct counter result | `NOT_RUN` | `S045-V04` | — | E2E | — |
| `S045-E07-C07-cancel-owner-wakes-waiters` | `S045-I03`, `S045-I11` | direct cancel result | `NOT_RUN` | `S045-V07`, `S045-V16` | — | E2E | — |
| `S045-E07-C08-panic-owner-wakes-waiters` | `S045-I03`, `S045-I11` | direct panic result | `NOT_RUN` | `S045-V07`, `S045-V16` | — | E2E | — |
| `S045-E07-C09-supervisor-shutdown-joins` | `S045-I03`, `S045-I11` | direct shutdown result | `NOT_RUN` | `S045-V07`, `S045-V16` | — | E2E | — |
| `S045-E07-C10-distinct-owner-65` | `S045-I03`, `S045-I11` | direct owner-cap result | `NOT_RUN` | `S045-V07` | — | E2E | — |
| `S045-E07-C11-queue-q1` | `S045-I03`, `S045-I11` | direct queue result | `NOT_RUN` | `S045-V07` | — | E2E | — |
| `S045-E07-C12-queue-q4` | `S045-I03`, `S045-I11` | direct queue result | `NOT_RUN` | `S045-V07` | — | E2E | — |
| `S045-E07-C13-queue-q16` | `S045-I03`, `S045-I11` | direct queue result | `NOT_RUN` | `S045-V07` | — | E2E | — |
| `S045-E07-C14-queue-q64-rejected` | `S045-I03`, `S045-I11` | direct queue rejection | `NOT_RUN` | `S045-V07`, `S045-V11` | — | E2E | — |
| `S045-E08-C01-state-hostile-decode` | `S045-I02`, `S045-I11` | direct hostile result | `NOT_RUN` | `S045-V11` | — | E2E | — |
| `S045-E08-C02-manifest-hostile-decode` | `S045-I04`, `S045-I11` | direct hostile result | `NOT_RUN` | `S045-V11` | — | E2E | — |
| `S045-E08-C03-path-escape` | `S045-I04`, `S045-I11` | direct hostile result | `NOT_RUN` | `S045-V11` | — | E2E | — |
| `S045-E08-C04-offset-extent-overflow` | `S045-I04`, `S045-I11` | direct hostile result | `NOT_RUN` | `S045-V11` | — | E2E | — |
| `S045-E08-C05-depth-64-and-65` | `S045-I04`, `S045-I11` | direct depth result | `NOT_RUN` | `S045-V11`, `S045-V12` | — | E2E | — |
| `S045-E08-C06-resource-cap-matrix` | `S045-I03`, `S045-I11` | every cap result | `NOT_RUN` | `S045-V07`, `S045-V12` | — | E2E | — |
| `S045-E08-C07-zero-mappings` | `S045-I07`, `S045-I11` | direct mapping result | `NOT_RUN` | `S045-V12` | — | E2E | — |
| `S045-E08-C08-miri-loom-sanitizer` | `S045-I10`, `S045-I11` | tool/fuzz matrix | `NOT_RUN` | `S045-V11` | — | tool availability | — |
| `S045-E09-C01-noop-command-old-new` | `S045-I09`, `S045-I11` | direct command result | `NOT_RUN` | `S045-V13`, `S045-V15` | — | E2E | — |
| `S045-E09-C02-sustained-command` | `S045-I09`, `S045-I11` | direct command result | `NOT_RUN` | `S045-V13`, `S045-V22` | — | E2E | — |
| `S045-E09-C03-pty-supported-lifecycle` | `S045-I09`, `S045-I11` | direct PTY result | `NOT_RUN` | `S045-V13`, `S045-V23` | — | E2E | — |
| `S045-E09-C04-pty-unsupported-deterministic` | `S045-I09`, `S045-I11` | direct unsupported result | `NOT_RUN` | `S045-V13` | — | E2E | — |
| `S045-E09-C05-file-read-metadata` | `S045-I09`, `S045-I11` | direct read result | `NOT_RUN` | `S045-V13`, `S045-V15` | — | E2E | — |
| `S045-E09-C06-file-write-rename-fsync` | `S045-I09`, `S045-I11` | direct mutation result | `NOT_RUN` | `S045-V15`, `S045-V25` | — | E2E | — |
| `S045-E09-C07-file-unlink-teardown` | `S045-I09`, `S045-I11` | direct teardown result | `NOT_RUN` | `S045-V15`, `S045-V25` | — | E2E | — |
| `S045-E09-C08-explicit-publish-separation` | `S045-I09`, `S045-I11` | direct attribution result | `NOT_RUN` | `S045-V15`, `S045-V25` | — | E2E | — |
| `S045-E10-C01-long-quiescence` | `S045-I07`, `S045-I11` | direct stability result | `NOT_RUN` | `S045-V12`, `S045-V16` | — | E2E | — |
| `S045-E10-C02-cancel-panic-churn` | `S045-I03`, `S045-I11` | direct churn result | `NOT_RUN` | `S045-V12`, `S045-V16` | — | E2E | — |
| `S045-E10-C03-exact-cleanup` | `S045-I11`, `S045-A04` | direct cleanup result | `NOT_RUN` | `S045-V16` | — | E2E | — |
| `S045-E11-C01-stage03-root-regression` | `S045-I10`, `S045-I11` | direct Stage 03 result | `NOT_RUN` | `S045-V17` | — | E2E | — |
| `S045-E11-C02-stage04-strict-regression` | `S045-I10`, `S045-I11` | direct Stage 04 result | `NOT_RUN` | `S045-V17` | — | E2E | — |
| `S045-E11-C03-stage05-bridge-contract` | `S045-I05`, `S045-I11` | direct Stage 05 seam result | `NOT_RUN` | `S045-V06`, `S045-V17` | — | E2E | — |
| `S045-E11-C04-stage06-authority` | `S045-I08`, `S045-I11` | direct authority result | `NOT_RUN` | `S045-V18` | — | E2E | — |
| `S045-E11-C05-stage07-deferrals` | `S045-D03`, `S045-I11` | direct deferral audit | `NOT_RUN` | `S045-V18` | — | E2E | — |

## L. Evidence checklist

### L.1 Source and architecture

- [ ] Exact revisions, diffs, toolchains, image, host, and filesystem recorded.
- [ ] Retained Stage 04 hashes match.
- [ ] Deletion/retirement callgraph is absent or production-unreachable.
- [ ] Dependency and unsafe inventories are reviewed.
- [ ] No memory mapping or ownerless worker pool exists.
- [ ] Public authority remains `legacy_v1`.

### L.2 Persistence and lifecycle

- [ ] `STATE` is the sole operation/recovery record.
- [ ] `CURRENT` is the sole materialization selector.
- [ ] `MANIFEST` is immutable after `Ready`.
- [ ] Only four authoritative phases exist.
- [ ] Initial and replacement publication have distinct typed admission rules.
- [ ] Exact old subject is held and handed off after publication.
- [ ] Corruption retains uncertainty and fails closed.

### L.3 Boundedness and locking

- [ ] Every cap in §D.7 has admission, high-water observation, and rejection proof.
- [ ] Recovery pages at most 64 without total-history collection/sort.
- [ ] Same-key work has one target and at most 16 waiters.
- [ ] Four disjoint targets remain within `W_mat`.
- [ ] Lock rank is enforced.
- [ ] Every writer-lock forbidden-work counter is zero.
- [ ] Cancellation, panic, and shutdown return/join exact ownership.

### L.4 Correctness

- [ ] Ready target is invisible before common publication.
- [ ] Active-GC interleavings never expose an unadmitted root.
- [ ] Every crash point resolves to exact old/new authority.
- [ ] Response loss is idempotent.
- [ ] Old readers keep old generation; new readers lease new generation.
- [ ] Strict native routing has no fallback.
- [ ] Command, file, and PTY semantics match baselines.
- [ ] Unsupported PTY actions remain deterministic and are not called implemented.
- [ ] Stage 03/04 identities and regressions pass directly.

### L.5 Performance, resources, and space

- [ ] One 180-second runner clock starts before prerequisites/pre-samples.
- [ ] Admission stops exactly at 150 seconds.
- [ ] The final 30 seconds contain only permitted closeout work.
- [ ] No operation exceeds 60 seconds.
- [ ] ABBA and complement orders are present.
- [ ] Required p50/p95 cells have at least 20 samples per arm.
- [ ] p99 is reported only at `n>=100`.
- [ ] Raw statistics and threshold formulas recompute exactly.
- [ ] RSS, resources, workers, FDs, queues, holds, retries, and mappings meet gates.
- [ ] Physical allocated-byte buckets reconcile at before/peak/after/quiescence.
- [ ] Read-only durable LayerStack delta is zero.
- [ ] Mutation bytes are fully attributed.
- [ ] Unexpected quiescent residue is zero.
- [ ] Pre-Stage-05 retained generations are reported without settled-space `PASS`.
- [ ] Post-Stage-05 settled gates have direct evidence before they pass.

### L.6 Evidence and cleanup

- [ ] Every live command had a prior pending report entry.
- [ ] Each result points to raw artifacts and SHA-256 values.
- [ ] Failed, interrupted, insufficient, and superseded runs remain visible.
- [ ] Cleanup targets only exact run-owned resources.
- [ ] Cleanup ledger is durable before the 180-second deadline.
- [ ] Final state is quiescent with zero unexplained residue.
- [ ] No claim relies only on inspection, diff, unit tests, or inherited proof.

## M. Handoff template and final validation

### M.1 Stage 04.5 to Stage 05 handoff template

```markdown
# Stage 04.5 handoff to Stage 05

Verdict: <OPEN|BLOCKED|PASS|FAIL>
Created: <UTC timestamp>

## Frozen identities

- product revision/diff SHA:
- test revision/diff SHA:
- docs revision/diff SHA:
- Rust/build profile/features:
- host/kernel/architecture/filesystem:
- Docker/runtime:
- pinned image:
- Stage 04.5 run/owner ID:
- catalog SHA-256:
- product oracle SHA-256 values:
- public authority:

## Implemented boundary

- private build:
- Ready immutability:
- common publication:
- GC root-admission bridge:
- exact old-subject handoff:
- common recovery:
- deletion/retirement production reachability:

## Direct evidence

| Gate | Status | Artifact | SHA-256 | Exact reason |
| --- | --- | --- | --- | --- |

## Performance and resources

- official command:
- campaign clock:
- sample sufficiency:
- raw time statistics/formulas:
- lock wait/hold and forbidden-work:
- RSS/resources/high-water:
- physical allocated-byte buckets:
- pre-/post-Stage-05 space disposition:

## Failures, insufficient samples, and deferrals

| Cell | Disposition | Reason | Artifact |
| --- | --- | --- | --- |

## Custody and cleanup

- owner inventory:
- cleanup command:
- cleanup ledger path/SHA:
- quiescence:
- unexplained residue:
- unrelated resources preserved:

## Remaining authority boundary

- public v1 read/write:
- candidate/fallback authority:
- Stage 05 deletion/retirement authority:
- Stage 06 authority switch:
- Stage 07 irreversible retirement:

## Exact blockers or next action

<one concrete statement>
```

### M.2 Final validation procedure

Before proposing `PASS`:

1. Re-read the four Stage 04.5 source documents and diff them against the revisions
   used to design the implementation.
2. Recompute all source, binary, catalog, corpus, raw artifact, summary, and cleanup
   hashes.
3. Re-run the strict artifact verifier from raw records.
4. Confirm every §K row has a direct artifact or remains honestly non-PASS.
5. Confirm every §L box is backed by evidence, not prose.
6. Confirm the product exposes no Stage 04.5 generation deletion/retirement path.
7. Confirm `legacy_v1` remains public read/write authority.
8. Confirm the writer-lock forbidden-work counters and mapping count are zero.
9. Confirm no history-sized recovery/allocation/lease scan exists in exercised paths.
10. Confirm exact owner cleanup and durable quiescence.
11. Capture final repository status/diff and preserve unrelated work.
12. Append the final validation command result to the report; never rewrite history.

### M.3 Current handoff state

This instruction document hands implementation forward with:

- overall Stage 04.5 status: `OPEN`;
- live test/benchmark status: `NOT_RUN`;
- public authority: `legacy_v1`;
- exact unresolved contradiction: current production retirement/deletion entry points
  conflict with Stage 04.5's no-deletion authority;
- external decision blocker: none identified;
- implementation performed while authoring this guide: none;
- live tests or benchmarks performed while authoring this guide: none.
