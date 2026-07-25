# Stage 04 implementation instructions: candidate materialization and strict native activation

Status: **IMPLEMENTATION GUIDE ONLY — STAGE 04 IMPLEMENTATION AND VERIFICATION ARE NOT COMPLETE**

Stage 04 product code, product tests, typed E2E, benchmark cells, portability cells,
and qualification remain `OPEN` or `NOT_RUN`. This document records read-only source
and repository inspection performed on 2026-07-25; it does not convert specification
prose, Stage 03 evidence, a planned command, or source inspection into a Stage 04
`PASS`. The focused benchmark is Stage 04 POC evidence only. Stage 07 release
qualification remains `DEFERRED_STAGE_07`.

## 1. Status, authority, source ledger, and custody

### 1.1 Authority order

Resolve requirements in this order:

1. approved owner decisions and frozen v2/v3 identities;
2. the [LayerStack storage contract](../layerstack_storage_contract.md);
3. the Stage 04 [specification](spec.md) and [typed E2E plan](e2e_test.md);
4. reconciled Stage 03 outgoing and Stage 04 incoming handoff evidence;
5. [Preparation 04 quantitative gates](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md);
6. current implementation details.

Lower-authority implementation details may identify a seam, but may not weaken a
higher-authority invariant. In particular:

- `legacy_v1` remains the sole public read and write authority through Stage 04.
- Strict candidate mode never silently falls back to v1.
- Frozen v2/v3 framing, typed domains, bounds, golden bytes, and `RootId` meaning do
  not change.
- A materialization key includes logical `RootId`, backend kind, backend format
  version, and target profile; physical paths, credentials, hosts, devices, inodes,
  compression, and build inputs never enter logical identity.
- Cold reconstruction is an explicit operation. Command, file, PTY, workspace, and
  warm-session requests never hide it.
- One admitted session leases exactly one
  `{materialization-id,generation,fence}`. Later head or `CURRENT` changes affect
  later admissions only.
- Immutable carriers may be shared. An upper, OverlayFS work directory, execution
  scratch, mount namespace, or live session may not be shared.

### 1.2 Complete reading ledger

Every row below was read from line 1 through EOF. Line count and SHA-256 describe the
bytes inspected while authoring this guide. Recompute them at implementation entry;
any changed authority source is a hard reconciliation gate.

| Source | Role | Lines | SHA-256 |
| --- | --- | ---: | --- |
| `stage_04_candidate_materialization/spec.md` | Stage 04 normative behavior | 167 | `eda5fef5b84b1a5b01b2cfdb50fccd2c3ed1880491c4d4b414a6a0ec9ceb1045` |
| `stage_04_candidate_materialization/e2e_test.md` | Stage 04 typed E2E contract | 86 | `59ed2559548a0a6cf10452401279acea817bba678ef916ff9de27379e140d523` |
| `stage_04_candidate_materialization/handoff_from_stage_03.md` | Stage 04 incoming custody/evidence | 185 | `bd1ed14f590122f53e97f42d74eaf15162e08390297cac457f536fd4cad38e21` |
| `stage_04_candidate_materialization/benchmark_note.md` | Stage 04 initial benchmark status | 24 | `d951e9c33e393501b40edfac969a08c5aedebdf300b0fe26f9e670af28c47aa0` |
| `implementation/index.md` | Phase ordering and cross-stage boundary | 376 | `91b9bb66ef87a68f3fb5537c7bac814584fe34420c1105278a5e7dd380baab54` |
| `implementation/layerstack_storage_contract.md` | Normative `/eos` ownership and durability | 718 | `4319272001aa9f1465f5baf9bd39ec421e200e6a0b5f2310ddf476c887f548d5` |
| `prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md` | Quantitative gates and accounting | 819 | `a02a8280152a59316cdb139299ac22f309bc3737787ffdcc4daebc122518257f` |
| `stage_03_incremental_publication/handoff_to_stage_04.md` | Immutable outgoing handoff | 201 | `471fc5b65a167755b5620f43429e6efc59794fb250f074789c19cf7ef4bf9954` |
| `stage_03_incremental_publication/implementation_instructions.md` | Guide rigor and inherited architecture | 1,514 | `2ea6c4e64416cd1327d18656b811f135c90ce3144d77ffaba73caeb6d472f435` |
| `stage_03_incremental_publication/benchmark_note.md` | Historical Stage 03 benchmark evidence | 134 | `8b775f3ed998132a72b451034b8d8e529fd427cfbfcd7bedd8a06bd84219778f` |
| `stage_03_incremental_publication/stage03_dependency_portability_audit_20260725.md` | Inherited dependency boundary evidence | 105 | `a475ad7a23999ee4a231c08d40677186498bddcaf5b44d4e2fbf8683eaa386f7` |
| `stage_03_incremental_publication/contract_v3_owner_decision_g01_1.md` | Approved/frozen v3 owner decision | 703 | `27264ef96f97960757eeba0b51bb7d2560446466cbf8e6a11c99a881da834e16` |
| `ephemeral-sandbox/AGENTS.md` | Product repository operating rules | 11 | `df940aab9dcd4502ae0bcb7615f97100aedc75955e6eefa7dfcb07aae1730ff9` |
| `ephemeral-sandbox/CLAUDE.md` | Product architecture/development rules | 94 | `f4ebdc0aaa997b673d272c31e2a09e12e4d499f0c1d1cd15000335796086a308` |
| `ephemeral-sandbox/docs/maintainer-architecture.md` | Current subsystem ownership | 189 | `bad6718400572de469516c3c3677e642958b87b99e5d7d4bbb8ecc393dd3b454` |
| `stage_05_retention_gc_packs/spec.md` | Stage 05 non-goals | 186 | `db619550fe87b870635b09a73fa066c278fdf7d3fda60576412fc7e1327dd594` |
| `stage_06_candidate_authority/spec.md` | Stage 06 cutover non-goals | 177 | `e2d482a554cce26f4a4f2644ca9a6461c37484ffe22d7bec8f6f4d3f7d01eed8` |
| `stage_07_qualification_retirement/spec.md` | Stage 07 qualification/retirement deferrals | 215 | `0355244af6581b5576271fc59701631f85f04aed8bc7e2f9798b95ca4ee1ee8e` |

Useful direct links are the Stage 03 [outgoing handoff](../stage_03_incremental_publication/handoff_to_stage_04.md),
[implementation guide](../stage_03_incremental_publication/implementation_instructions.md),
[benchmark note](../stage_03_incremental_publication/benchmark_note.md),
[dependency audit](../stage_03_incremental_publication/stage03_dependency_portability_audit_20260725.md),
and [owner decision](../stage_03_incremental_publication/contract_v3_owner_decision_g01_1.md);
the later boundaries are the Stage 05 [specification](../stage_05_retention_gc_packs/spec.md),
Stage 06 [specification](../stage_06_candidate_authority/spec.md), and Stage 07
[specification](../stage_07_qualification_retirement/spec.md).

### 1.3 Handoff reconciliation

The incoming handoff names the exact outgoing handoff SHA-256
`471fc5b65a167755b5620f43429e6efc59794fb250f074789c19cf7ef4bf9954`,
which equals the inspected outgoing file. Both records agree on:

| Identity | Reconciled value |
| --- | --- |
| owner decision | `27264ef96f97960757eeba0b51bb7d2560446466cbf8e6a11c99a881da834e16` |
| product recorded baseline | `cbe45de873cd24fbf48bb7b3a6c5f9f98980313c` |
| test recorded baseline | `173191e8694515af43797128070dbdfd2d246040` |
| recorded product Stage 03 source-diff | `d5323b27f1dd7b9e19cf53551162e5608624597b1a9b6aaa9f9dcf1d6b8c8823` |
| recorded test/benchmark Stage 03 source-diff | `95adf9fddf75d715a464d095cc7e9192d240d3eaa00597b822795e5756c2ba38` |
| final Stage 03 campaign | `019f977b-752d-7868-927d-170b8d46a078` |
| authority | public read/write `legacy_v1`; candidate private validation only |
| mandatory Stage 03 blockers | none recorded |

There is **no incoming-versus-outgoing handoff contradiction** at authoring time.
If any recorded identity differs at implementation entry, `S04-G02` is `BLOCKED`;
do not choose either record silently.

There is one genuine cross-source contradiction: `implementation/index.md` lines
355–358 still calls the v3 content-Merkle/attribution amendment “unapproved,” while
the higher-authority approved owner decision above freezes it and the outgoing
handoff records no mandatory Stage 03 blocker. Under the authority order, the index
text is stale/superseded, not permission to redesign v3 and not a present handoff
blocker. If the owner decision digest or approval status changes, stop.

The handoff describes Stage 03 custody as uncommitted. The fresh snapshot below finds
those deltas committed one commit ahead of each recorded baseline. That is subsequent
custody state, not a content contradiction. The future agent must preserve both
commits and compare exact trees before relying on recorded diff digests; it must not
force the worktree back to the historical form.

### 1.4 Read-only custody snapshot

Snapshot time: `2026-07-25T05:05:22Z`. It is context, not permission to mutate or
clean anything.

| Repository | Branch / HEAD / upstream | Worktree and custody |
| --- | --- | --- |
| product | `upgrade-2.0-phase-1`; HEAD `487ac4c7fda941711bf9ce15524e425a221b780c`; upstream `origin/upgrade-2.0-phase-1` at `cbe45de873cd24fbf48bb7b3a6c5f9f98980313c`; ahead 1 | clean index/worktree/untracked; local commit `feat(layerstack): implement incremental publication`; preserve it |
| test + benchmark | `upgrade-2.0-phase-1`; HEAD `1b253b2107aa81926839cbd5d8a8cdae746de2cf`; upstream at `173191e8694515af43797128070dbdfd2d246040`; ahead 1 | clean index/worktree/untracked; local commit `test(layerstack): validate stage 03 publication`; preserve it |
| documentation | `layerstack_2_0`; HEAD `4cf4b32f28306d03000b5e2e715f0ffd01a716aa`; upstream `426b6be3284c26a59eb77d39ad6622997e8479c9`; ahead 3 | pre-existing modified Stage/phase docs plus untracked incoming Stage 04 handoff; preserve all; this guide is the only path this task may add |

Ignored historical state is substantial and is not free scratch:
`ephemeral-sandbox-test/.benchmark-state` was about 3,328,300 KiB and
`.e2e-state` about 673,848 KiB. The final Stage 03 result remains under
`.benchmark-state/results/019f977b-752d-7868-927d-170b8d46a078/`. Allocate a new,
run-scoped Stage 04 artifact root; never overwrite or broadly delete retained runs.

Three pre-existing gateway processes/listeners were observed and are not Stage
04-owned: PIDs `14966`, `23296`, and `53713` on `127.0.0.1:17878`,
`127.0.0.1:7878`, and `127.0.0.1:17978`. Eight pre-existing exited containers were
also present. Do not signal, reuse, or remove them. The host is therefore not globally
quiescent; Stage 04 must prove quiescence relative to an exact run ownership ledger
and pre-samples, not by claiming zero host processes.

At every future mutation or run:

1. re-record branch, HEAD, upstream, ahead/behind, staged/unstaged/untracked/ignored
   relevant state, exact diffs, processes, listeners, containers, benchmark roots,
   disk allocation, and UTC time;
2. allocate collision-resistant run IDs, ports, configs, directories, and container
   labels;
3. write ownership before creation and update it as each resource becomes live;
4. touch only exact resources present in that run's ledger; and
5. never recommend or use reset, stash, clean, restore, branch switching, broad
   deletion, or cleanup by ambiguous name/pattern.

## 2. Purpose and exact outcome

Stage 04 is complete only when the candidate can:

1. explicitly reconstruct any supported private frozen v3 `RootId` into a verified,
   immutable, backend-native generation;
2. durably publish a generation manifest, then atomically select it through
   `CURRENT`;
3. reuse an already-valid matching generation without reconstructing it;
4. admit strict candidate command, file, PTY, and workspace operations only from a
   selected, verified native generation;
5. retain one exact fenced generation lease for each admitted session;
6. preserve old admitted sessions across logical head and `CURRENT` changes while
   later admissions select the new exact generation;
7. isolate per-session upper/work/execution state and mount namespaces;
8. fail before workspace/session mutation when a generation is missing, corrupt,
   unsupported, or incapable; and
9. leave public v1 behavior, authority, bytes, and compatibility unchanged.

This outcome is a materialization/activation proof. It is not an authority cutover
and not universal platform qualification.

## 3. Entry gates and hard blockers

| Gate | Required action | Stop condition | Initial status |
| --- | --- | --- | --- |
| `S04-G01` custody | Re-inventory all three repositories and exact external runtime state; record digests and ownership. | Unknown/overlapping custody or an unowned path/resource would be mutated. | `OPEN` |
| `S04-G02` handoff identities | Re-hash incoming/outgoing handoffs, decision, corpus, guide, benchmark note, audit, report, recorded diffs, and retained run manifest. | Any incoming/outgoing disagreement; missing recorded evidence; unexplained tree mismatch. | `OPEN` |
| `S04-G03` authority | Prove config, observation, and public APIs still report `LegacyV1` read/write authority. | Any proposed public authority move or v1 behavior change. | `OPEN` |
| `S04-G04` frozen contracts | Run v2/v3 golden, hostile-decode, host-independence, record-bound, and `RootId` tests before Stage 04 mutation. | Golden byte/ID drift, unapproved schema/domain/bound change, physical input in identity. | `OPEN` |
| `S04-G05` storage contract | Map every path owner and atomicity rule in §5 before adding a path. | Ambiguous owner, non-atomic selector, hidden reconstruction, or forbidden directory. | `OPEN` |
| `S04-G06` environment | Lock product/test revisions, binaries, config, pinned images/platform descriptors, filesystem/backend capabilities, ports, and artifact root. | Mutable image tag, missing identity, unsupported capability represented as success, or non-owned collision. | `OPEN` |
| `S04-G07` report discipline | Append the pre-run entry before any live test, diagnostic, or benchmark. | Missing pre-entry, incomplete custody/identity/ownership fields, or reused run ID. | `OPEN` |
| `S04-G08` correctness before performance | Complete the full product, typed E2E, failpoint, artifact-negative, cleanup, and compatibility matrix separately. | Any correctness failure or cleanup leak; benchmark may not hide/skips failures to meet 180 seconds. | `OPEN` |

Additional hard blockers are: no exact native backend capability contract; no safe
raw-byte path reconstruction; no way to fsync the containing directory; inability to
lease an exact generation before mount; inability to distinguish unsupported from a
measured zero; unbounded worker/buffer/queue/FD/mapping growth; or inability to mask
`/eos` from public workloads.

## 4. Scope and non-goals

### 4.1 In scope

- Linux native materialization and OverlayFS/mount-namespace activation for the
  explicitly qualified backend/profile cells.
- Streamed, bounded reconstruction from existing private v3 typed objects.
- Exact metadata reconstruction: raw-byte names, type, mode, ownership when
  representable, timestamps as contracted, xattrs, hardlinks, symlinks, sparse
  extents, whiteouts/deletions, opaque directories, and device/FIFO nodes only where
  supported and authorized.
- Durable operation state/private work, immutable carriers, manifest validation,
  atomic `CURRENT`, exact leases/fences, reuse, same-key single-flight, recovery,
  grace/final recheck deletion, accounting, backpressure, and strict activation.
- Candidate routing for command, file, PTY, workspace, restart, and concurrency
  cases, while v1 remains public authority.
- Stage 04 product/unit/integration tests, typed E2E, fixtures, schemas, strict
  verifier, focused 180-second campaign, documentation, and Stage 05 handoff.

### 4.2 Explicit non-goals and forbidden shortcuts

- Stage 05: packs, pack rewriting, general locator compaction, production GC, squash,
  retention-policy rollout, or pack/locator/GC directories created for Stage 04.
- Stage 06: public read/write authority cutover, mixed-authority fallback,
  destructive migration, or v1 retirement.
- Stage 07: release qualification, universal host/filesystem/image support, an image
  support percentage, long-duration soak, multi-host selection, destructive
  retirement, or final rollback qualification.
- No `/eos/legacy`, `/eos/layer-stack/refs/legacy`, global
  `/eos/namespace_execution`, benchmark-only durable product layout, or premature
  Stage 05–07 directory.
- No alternate benchmark harness and no benchmark-only product protocol. Extend the
  Stage 03 typed E2E, catalog, strict artifact, preset, runner-owned campaign,
  fixture, schema, and verifier architecture.
- LayerStack cleanup may not remove WorkspaceManager, service-storage, daemon-runtime,
  or another subsystem's paths.

## 5. Complete `/eos` contract

### 5.1 Normative tree

The complete contract is shown, including inherited and later-stage paths so absence
and ownership are testable:

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
└── runtime/daemon/
    ├── runtime.sock
    └── runtime.pid
```

The root is control-plane storage. Public workloads must see `/eos` masked. The
public `/workspace` mount is not another durable `/eos` subtree.

### 5.2 Stage 04 path-by-path ownership and lifecycle

Atomic mutable-record publication means: write a same-directory temporary file,
validate/flush content, `fsync` the file, atomic rename, then `fsync` the containing
directory. “Exact lease” means a durable lease naming materialization ID, generation,
and fence; a root-only or `CURRENT`-only lease is insufficient.

| Path/pattern | Owner; creator/mutator | First use | Durability/atomicity; recovery owner | Lease/fence; deletion preconditions | Accounting bucket | Stage 04 status |
| --- | --- | --- | --- | --- | --- | --- |
| `/eos/layer-stack/` | LayerStack only | Existing v1/Stage 03 initialization | Directory durability per storage contract; LayerStack recovery | Never delete while any LayerStack format is retained | metadata | inherited |
| `.storage-writer.lock` | LayerStack storage writer | First mutating LayerStack open | Advisory/exclusive writer discipline; LayerStack | Release on owner exit; not a GC target | metadata | inherited |
| `CONTROL` | LayerStack format owner | First candidate-format open | Bounded, versioned, validated, atomic mutable record | No deletion during compatibility window | metadata | inherited/required validation |
| `objects/loose/<kind>/<prefix>/<typed-id>` | Candidate object store | Stage 03 object put | Immutable put-if-absent; verify type/domain/digest/length | Retained by logical refs/source holds; Stage 04 may read, not generally collect | logical sources | inherited |
| `objects/packs/<pack-id>.pack` | Stage 05 pack owner | Stage 05 only | Immutable pack protocol | Stage 05 reachability/locator barriers | packs | forbidden |
| `objects/locators/{<run-id>.sst,CURRENT}` | Stage 05 locator owner | Stage 05 only | Immutable run plus atomic selector | Stage 05 fences/barriers | locator metadata | forbidden |
| `refs/heads/<branch-id>` | Candidate ref owner | Stage 03 branch use | Atomic fenced ref `{RootId,AttributionRootId,generation}` | Delete only by exact ref protocol | logical refs | inherited |
| `refs/checkpoints/<checkpoint-id>` | Candidate ref owner | Stage 03 checkpoint | Immutable/atomic as contract says | Delete only after exact ownership/retention checks | logical refs | inherited |
| `refs/pins/<pin-id>` | Candidate retention owner | Stage 03 pin | Durable exact root pair | Explicit unpin; never inferred from session end | logical refs/pins | inherited |
| `refs/leases/<lease-id>` logical/source leases | Candidate lease owner | Existing source/ref hold | Durable, fenced, restart-recoverable | Exact owner release/expiry rules and final recheck | logical leases | inherited |
| `refs/leases/<lease-id>` generation lease | Materialization/session admission | Before exposing/mounting selected generation | Durable exact `{materialization-id,generation,fence,session/owner}`; recover/renew or fail closed | Release after unmount/session retirement; deletion waits grace plus final no-lease recheck | generation leases | required |
| `operations/<operation-id>/STATE` | Candidate operation manager | Before first build mutation | Bounded state machine, atomic/fenced, exact retry terminal result | Delete only after terminal retention/ack/expiry contract and no recovery need | operations/metadata | required |
| `operations/<operation-id>/work/` | Same operation owner | After durable ownership state | Private; every artifact attributable; restart classifies resume/reap | Only exact terminal/recovery owner after no live task/FD/mapping/permit | build staging | required |
| `materializations/<materialization-id>/` | Materialization registry | First explicit materialize/lookup for key | ID derived from the physical materialization key, not logical identity | Remove only when all generations/selectors gone under future policy | metadata | required |
| `materializations/<id>/generations/<generation>/carriers/<carrier-id>/...` | One build operation until commit; then immutable carrier owner | Private build after operation ownership | Build privately; bounded streaming; preserve bytes/metadata; sync all data/dirs before manifest; immutable after publish | No mutation after manifest; delete only when unselected, unpinned, unleased, not the last verified native locator, grace elapsed, final recheck passed, and exact owner is known | `H_cold` carriers; building bytes in `P_staging` until publish | required |
| `materializations/<id>/generations/<generation>/MANIFEST` | Materialization publisher | Only after carrier reconstruction and logical/capability verification | Immutable/versioned; file + parent durability before `CURRENT`; recovery validates or quarantines logically without inventing a new layout | Generation deletion only after lease/pin/current/last-verified-locator checks | manifests/metadata | required |
| `materializations/<id>/CURRENT` | Materialization selector owner | First verified generation selection | Atomic record names exact generation, manifest digest, and fence; never points to private/incomplete work | Change affects later admissions only; old selected generation retained while leased | refs/selectors | required |
| `gc/CURRENT` | Stage 05 GC owner | Stage 05 only | Atomic GC epoch/barrier | Stage 05 contract | GC metadata | forbidden |
| `manifest.json`, `workspace.json` | v1 LayerStack compatibility owner | v1 compatibility use | Preserve existing v1 protocol | No Stage 04 deletion or reinterpretation | v1 compatibility bytes | conditional compatibility |
| `base/<base-id>/...`, `layers/<layer-id>/...` | v1 LayerStack compatibility owner | Existing v1 use | Preserve v1 immutability/durability | Protected through compatibility/leases; no Stage 04 retirement | v1 compatibility bytes | conditional compatibility |
| `staging/<layer-id>.staging/...`, `.layer-metadata/<layer-id>.{digest,bytes}` | v1 publication owner | Existing v1 publication | Existing v1 atomic/recovery rules | Exact v1 cleanup only; candidate cleanup excluded | v1 staging/metadata | conditional compatibility |
| `/eos/workspace/manager.json` | WorkspaceManager | Manager first use | Atomic manager state; WorkspaceManager recovery only | LayerStack never deletes; manager requires no live owned sessions | workspace metadata | inherited |
| `/eos/workspace/.export/<spool-id>` | Workspace export owner | Explicit export | Private bounded spool and exact cleanup | Export owner only after terminal/recovery state | work/execution scratch | inherited/excluded |
| `/eos/workspace/<session>/upper/` | One WorkspaceManager session | Active session creation after exact generation lease | Private writable state; not part of shared carrier; manager recovers | After executions stop, unmount, lease release, exact session retirement | `sum(U_active)` | required integration |
| `/eos/workspace/<session>/work/` | Same session | Overlay activation | Same filesystem as upper, private, never shared | Same exact teardown order as upper | work scratch | required integration |
| `/eos/workspace/<session>/executions/<execution>/transcript.log` | NamespaceExecution under session owner | Execution first use | Existing bounded transcript protocol | Exact execution terminal/retention rules; LayerStack excluded | execution scratch | inherited integration |
| `/eos/storage/file_auditability/...` | service-storage/file auditability | Existing service use | Service contract | LayerStack excluded from mutation/cleanup | service-storage | inherited/excluded |
| `/eos/storage/workspace_recovery/...` | service-storage/workspace recovery | Existing service use | Service contract | LayerStack excluded from mutation/cleanup | service-storage | inherited/excluded |
| `/eos/runtime/daemon/{runtime.sock,runtime.pid}` | daemon runtime | Daemon start | Runtime lifecycle, not LayerStack durability | Daemon owner only; LayerStack excluded | daemon runtime | inherited/excluded |
| `/eos/legacy`, `/eos/layer-stack/refs/legacy` | no owner | never | no protocol | must remain absent | forbidden bytes | forbidden |
| `/eos/namespace_execution` | no owner | never | execution state belongs below session | must remain absent | forbidden bytes | forbidden |
| benchmark-only or premature Stage 05–07 paths | no product owner in Stage 04 | never | no benchmark may manufacture product durability | must remain absent | forbidden/unexplained | forbidden |

### 5.3 Mandatory layout assertions (`S04-L01`–`S04-L13`)

Each assertion retains a sorted raw-byte-safe tree inventory, `lstat` metadata,
mountinfo, allocated-block sample, owning IDs, and SHA-256 digest. Absence is an
observed state, never a fabricated zero.

| ID | Boundary and required assertion |
| --- | --- |
| `S04-L01` | Setup: complete normative roots are classified; forbidden paths absent; unrelated `/eos/storage`, `/eos/runtime`, and WorkspaceManager state unchanged. |
| `S04-L02` | Private build: operation `STATE` owns `work`; incomplete carrier bytes are not reachable by `CURRENT`; no session/upper exists. |
| `S04-L03` | Manifest-before-`CURRENT`: carrier data and directories are synced; immutable `MANIFEST` verifies; old/absent `CURRENT` remains authoritative. |
| `S04-L04` | Selected generation: atomic `CURRENT` names exact generation, manifest digest, and fence; parent directory sync is evidenced. |
| `S04-L05` | Active session: exact generation lease predates mount; carrier is read-only/shared; upper/work/executions/mount namespace are private; workload sees `/eos` masked. |
| `S04-L06` | Generation switch: new `CURRENT` changes later admission only; old admitted session and exact old lease remain stable. |
| `S04-L07` | Crash/restart: operation state classifies private residue; selector is old or complete, never partial; valid sessions recover or fail closed by contract. |
| `S04-L08` | Corruption/unsupported capability: failure occurs before lease/mount/upper/work/execution mutation; `CURRENT` is not silently repaired to v1. |
| `S04-L09` | Lease release: execution stops, unmount completes, session state retires, then exact lease releases; no early carrier deletion. |
| `S04-L10` | Grace/final recheck: deletion candidate survives grace and an immediately preceding selector/pin/lease/fence/last-verified-locator recheck; a new lease or last-locator status cancels deletion. |
| `S04-L11` | Teardown: only exact run/session/build-owned resources are removed; WorkspaceManager/service-storage/daemon/v1/unrelated state remains byte-identical. |
| `S04-L12` | Settled: active owned tasks/workers/queues/permits/FDs/mappings/leases/sessions/uppers are zero; all unavailable metrics remain explicitly unavailable. |
| `S04-L13` | Final cleanup: cleanup ledger is durable, `/eos` layout matches the pre-owned baseline plus intentionally retained immutable generation(s), and unexplained persistent residue is zero. |

## 6. Architecture, types, APIs, owners, and dependency direction

### 6.1 Dependency direction

```text
frozen layerstack-core v2/v3 types
        ↓
candidate logical object reader + verified tree walker
        ↓
bounded native materializer + operation/single-flight registry
        ↓
generation manifest/store + atomic CURRENT + exact lease registry
        ↓
workspace admission (strict prebuilt lookup only)
        ↓
WorkspaceManager private upper/work + native overlay mount
        ↓
command / file / PTY consumers of the already-admitted session
```

The portable core must not import Docker, Tokio runtime behavior, host paths,
mount syscalls, or backend credentials. Backend adapters depend on logical types, not
the reverse. NamespaceExecution consumes an admitted workspace; it never resolves a
root, materializes, selects `CURRENT`, or falls back. Benchmark/E2E code observes the
product; product code never depends on benchmark schema or fixtures.

### 6.2 Required types and invariants

Names below are implementation targets; preserve project naming conventions when
adding them.

| Type/API | Required fields/behavior | Owner |
| --- | --- | --- |
| `MaterializationKey` | `RootId`, backend kind, backend format version, target profile; canonical bounded encoding; physical inputs excluded | LayerStack candidate |
| `MaterializationId` | Typed digest of `MaterializationKey`; not a replacement for `RootId` | LayerStack candidate |
| `GenerationId` / `GenerationFence` | Exact monotonically fenced selection identity; no path-only equality | materialization registry |
| `MaterializationCapabilities` | Explicit file kinds, xattrs, raw-byte paths, ownership/timestamp, hardlink, sparse, whiteout/opaque, read-only/non-root constraints | backend adapter |
| `GenerationManifest` | schema/version, key and IDs, fence, carrier list/digests, logical verification result/root, entry count, logical bytes, allocated bytes/sample method, required/provided capabilities, build operation/identity, completion time | manifest owner |
| `CurrentGeneration` | materialization ID, generation, manifest digest, fence; bounded atomic record | selector owner |
| `GenerationLease` | lease/session/owner IDs plus exact materialization, generation, fence and recovery/expiry fields | admission + lease registry |
| `MaterializeRequest` | explicit request, expected key/capabilities, operation ID/deadline/cancellation, byte permit; never invoked by warm route | materializer service |
| `MaterializeResult` | reused/built disposition, exact manifest/current identity, counters and cleanup ownership | materializer service |
| `StrictCandidateAdmission` | lookup/validate selected manifest, acquire exact lease, allocate private session, mount; transactional rollback before response | workspace admission |
| `NativeRouteCounters` | lookup/validation/admission/mount plus forbidden CDC/object/hash/locator/pack/GC/squash/materialization/fallback counters | observability |
| `OwnedResourceSnapshot` | workers/tasks/queues/bytes/permits/RSS/FDs/mappings/builds/leases/sessions/uppers/staging | materializer + workspace |

### 6.3 State machines and ordering

Build:

```text
Absent → Owned → Building → CarrierSynced → ManifestDurable
       → CurrentDurable → TerminalBuilt
       ↘ Cancelled/Failed → Recovered/Reaped
```

The exact visibility order is operation ownership, private reconstruction, logical
and capability verification, carrier file/directory sync, immutable manifest write
and parent sync, atomic `CURRENT` write/rename/parent sync, terminal result. A lost
response retries by exact operation ID. Recovery may complete a fully durable
boundary or reap private residue; it may not expose a partial generation.

Admission:

```text
resolve CURRENT → validate exact manifest/carriers/capabilities
→ acquire durable exact generation lease
→ allocate private session upper/work/execution owner
→ mount native carrier(s) read-only in private namespace
→ expose admitted session → execute command/file/PTY
```

Every failure unwinds in reverse. Lease release occurs only after execution teardown
and unmount. A selector/head change never remounts an admitted session.

Single-flight is keyed by `MaterializationKey`. One owner builds; waiters have
bounded, cancellable waits and receive the same verified result or typed terminal
failure. Crash races may leave only bounded, attributable operation residue.

### 6.4 Resource ownership and limits

- Hydration buffer: at most 256 KiB per active stream.
- Global storage workers: at most four.
- Explicit byte permits cover buffers, queued/staged bytes, and concurrent build
  admission. Permit exhaustion applies backpressure or a typed failure; never
  allocates optimistically.
- Every operation is at most 60 seconds. Cancellation, timeout, panic, shutdown, and
  restart have an owner and cleanup path.
- RSS is at most 384 MiB absolute and 128 MiB above the measured idle baseline.
- Workers, tasks, queues, FDs, mappings, leases, sessions, uppers, and staging owners
  are bounded and sampled.
- Quiescence requires zero detached tasks, strong ownership cycles, or active
  run-owned resources. Host-global resources may remain only when pre-existing and
  excluded by identity.

## 7. File-by-file implementation map

“Add” means the path does not exist at authoring time and Stage 04 must create it.
“Modify” names a current seam. Keep public protocols unchanged unless the row
explicitly adds a private strict-candidate configuration surface.

### 7.1 Product and product-test map

| Work ID | Path | Action and deliverable | Verification |
| --- | --- | --- | --- |
| `S04-I01` | `crates/sandbox-runtime/layerstack/src/stack/candidate/materialization.rs` | **Add** key/ID, request/result, bounded tree reconstruction coordinator, single-flight, cancellation, and typed failures. | `S04-V05`–`S04-V12` |
| `S04-I02` | `.../candidate/native_backend.rs` | **Add** backend capability contract and Linux native carrier writer using raw-byte-safe, fd-relative/no-follow operations and bounded buffer/permits. | `S04-V05`, `S04-V06`, `S04-V10`, `S04-V31` |
| `S04-I03` | `.../candidate/generation.rs` | **Add** manifest codec/validation, immutable generation store, atomic `CURRENT`, exact generation fence/lease, grace/final recheck. | `S04-V13`–`S04-V18` |
| `S04-I04` | `.../candidate/materialization_operation.rs` | **Add** durable operation state, failpoints, exact retry, recovery/residue ownership. Reuse existing candidate operation primitives; do not fork a second protocol. | `S04-V19`–`S04-V24` |
| `S04-I05` | `.../candidate/mod.rs` | Modify exports and module ownership only. | compile/clippy, `S04-V33` |
| `S04-I06` | `crates/sandbox-runtime/layerstack/src/service/model.rs`, `service/mod.rs`, `service/impls/` | Add private explicit materialize/lookup/lease APIs and typed models. Keep `StorageAuthority::LegacyV1` sole authority. | `S04-V03`, `S04-V13`, `S04-V25` |
| `S04-I07` | `crates/sandbox-runtime/layerstack/src/stack/observation.rs`, `observability.rs` | Add materialization/native-route/resource counters with saturation/availability semantics; preserve v1 observations. | `S04-V27`–`S04-V30` |
| `S04-I08` | `crates/sandbox-config/src/configs/runtime.rs`, `crates/sandbox-daemon/src/serve.rs`, `crates/sandbox-runtime/operation/src/services.rs` | Add an explicit private strict-candidate mode/profile. Reject incompatible/missing config. Never turn it into public authority or fallback. | `S04-V03`, `S04-V25`, `S04-V32` |
| `S04-I09` | `crates/sandbox-runtime/operation/src/workspace_session/service/impls/admission.rs`, `create_workspace_session.rs`, `resolve_session.rs`, recovery/shutdown paths | Route strict admission through prebuilt generation lookup, exact lease-before-mount, and reverse-order rollback; legacy path unchanged. | `S04-V25`–`S04-V28` |
| `S04-I10` | `crates/sandbox-runtime/workspace/src/model.rs`, `lifecycle/create.rs`, `lifecycle/leases.rs`, `lifecycle/destroy.rs`, persistence/recovery | Carry exact materialization/generation/fence beside layer paths, allocate private upper/work, release lease after unmount, persist/recover exact selection. | `S04-V15`–`S04-V18`, `S04-V28` |
| `S04-I11` | `crates/sandbox-runtime/namespace-process/src/runner/setns/mount_overlay.rs`, `runner/mod.rs`; `crates/sandbox-runtime/overlay/src/kernel_mount.rs` | Validate native carrier mount inputs, preserve no-fallback kernel mount/unmount, and prove `/eos` mask. Avoid changing portable logical identity. | `S04-V25`, `S04-V26`, `S04-V31` |
| `S04-I12` | `crates/sandbox-runtime/operation/src/{command,file}/`, `namespace_execution.rs`, `operations/registry/`; existing `tests/{command_execution,command_teardown,file_operations,namespace_execution_registry}.rs` | Do not add hydration. Assert command/file/PTY paths consume an admitted strict session and emit zero forbidden-work counters. Preserve PTY drain/cancellation ordering. | `S04-V25`–`S04-V30` |
| `S04-I13` | `crates/sandbox-runtime/layerstack/tests/candidate_materialization.rs` | **Add** reconstruction, reuse, key/manifest/current/lease, single-flight, failpoint, recovery, quota/resource product integration tests. | `S04-V05`–`S04-V24`, `S04-V29` |
| `S04-I14` | `crates/sandbox-runtime/operation/tests/workspace_session_materialization.rs` | **Add** strict route/admission/restart/current-switch/isolation/no-fallback tests. | `S04-V25`–`S04-V30` |
| `S04-I15` | existing core golden/hostile/host-independence tests and Stage 03 publication/security/resource tests | Modify only to add regression assertions if necessary; never rewrite frozen fixtures. | `S04-V02`–`S04-V04`, `S04-V46` |

Before choosing these filenames, the implementer must confirm no concurrent owner has
introduced equivalent modules. If so, reconcile and extend the real seam instead of
duplicating it.

### 7.2 Test, E2E, fixture, schema, benchmark, and documentation map

| Work ID | Path | Action and deliverable | Verification |
| --- | --- | --- | --- |
| `S04-I16` | `e2e/runtime/layerstack_phase1/test_candidate_materialization.py` | **Add** typed cases declared with existing `e2e_test`, exact run ownership, outside accounting, and strict cleanup. | `S04-V05`–`S04-V32` |
| `S04-I17` | `e2e/runtime/layerstack_phase1/helpers.py`, `conftest.py` | Extend bounded identity, `/eos` inventory, allocated-space, capability, route-counter, failpoint, and quiescence helpers; preserve Stage 03 cases. | `S04-V01`, `S04-V27`, `S04-V35` |
| `S04-I18` | `e2e/fixtures/layerstack_phase1/candidate-materialization-v1/` | **Add** deterministic manifest and generator inputs for every file/tree shape and frozen expected logical/native results. Large bytes are deterministically generated, not checked in redundantly. | `S04-V05`, `S04-V34` |
| `S04-I19` | `e2e/metadata/catalog.yaml` and generated catalog export | Extend only through existing collector/declaration workflow; stable IDs for every typed case. | `S04-V01`, `S04-V32` |
| `S04-I20` | `e2e/schemas/layerstack_phase1/evidence-v1.schema.json`; if incompatible, **add** `evidence-v2.schema.json`; `benchmark/backend/benchmark_lab/{models.py,observability.py,artifacts.py}` | Extend the existing versioned Stage 03 evidence architecture with strict Stage 04 groups, explicit availability, and no implicit defaults. Add v2 only when v1 cannot be extended compatibly; do not create a stage-specific schema fork. | `S04-V34`, `S04-V35` |
| `S04-I21` | `benchmark/backend/benchmark_lab/stage04_materialization.py` | **Add** runner-owned 180-second adapter by reusing Stage 03 ownership/sampling/artifact patterns; no alternate harness. | `S04-V36`–`S04-V42` |
| `S04-I22` | `benchmark/backend/benchmark_lab/{planning.py,runner.py,resource_sampling.py,recovery.py}`, `benchmark/defaults/definition-catalog.json` | Register one frozen `stage04_materialization_campaign` operation and extend the existing runner-owned isolation, sampling, recovery, dispatch, and cleanup paths. | `S04-V34`, `S04-V36` |
| `S04-I23` | `benchmark/presets/layerstack-phase1-stage04-materialization.yml` | **Add** one exact 180/150/60-second plan, pinned digest, deterministic seed, counterbalanced protocol, and resource interval. | `S04-V36` |
| `S04-I24` | `benchmark/tests/fixtures/golden/layerstack_phase1/stage04_materialization_v1.json` | **Add** artifact contract, windows, thresholds, required families, buckets, and environment disposition. | `S04-V34`, `S04-V35` |
| `S04-I25` | `benchmark/backend/tests/contract/test_planning.py`, `integration/{test_runner.py,test_recovery.py}`, `compatibility/test_artifacts.py`; **add** `unit/test_stage04_materialization.py` | Test catalog/plan, clock, ordering, samples, accounting, artifact compatibility, negative cases, interruption/recovery, and cleanup without weakening historical readers. | `S04-V34`–`S04-V36` |
| `S04-I26` | `e2e/test-report.md` | Append-only pre- and post-entry around every future live test/benchmark/diagnostic. Never edit history. | `S04-V43` |
| `S04-I27` | this directory's `benchmark_note.md` and outgoing `handoff_to_stage_05.md` | Update benchmark note only from retained direct evidence; **add** final handoff after all Stage 04 gates. | `S04-V44`, `S04-V47` |
| `S04-D01` | Cargo manifests/lock and Stage 03 dependency comparator outputs | Audit dependency delta and portable-core boundary; new external dependencies need evidence and approval. | `S04-V33` |

## 8. Ordered implementation sequence

Do not skip forward across a stop condition.

1. `S04-G01`–`S04-G07`: reconcile authority, hashes, custody, configs, identities,
   ownership, and report discipline. **Stop** on any mismatch or ambiguous resource.
2. `S04-I18`, `S04-I20`, `S04-I24`: freeze deterministic fixtures, evidence schema,
   and golden verifier contract before product implementation. **Stop** if a required
   metric cannot represent `unavailable` without becoming zero.
3. `S04-I01`–`S04-I05`: implement the private materializer, backend capabilities,
   manifest/current/lease, operation recovery, and single-flight behind no public
   route. Run formatting, core goldens, and product-focused tests. **Stop** on
   identity drift or partial visibility.
4. `S04-I06`–`S04-I08`: expose explicit private service/config/observability seams
   while keeping `LegacyV1` authority. **Stop** if a public legacy request can enter
   materialization or candidate failure can fall back.
5. `S04-I09`–`S04-I12`: integrate strict prebuilt admission and native mount, exact
   lease, private upper/work/execution, restart and reverse teardown. **Stop** unless
   missing/corrupt/unsupported generations fail before mutation.
6. `S04-I13`–`S04-I15`: complete product failpoint, concurrency, pressure, recovery,
   and compatibility tests. Run dependency audit. **Stop** on any leak, unbounded
   resource, or v1 regression.
7. `S04-I16`–`S04-I19`: add typed E2E/catalog/fixtures and run the complete
   correctness matrix with append-only pre/post reporting. **Stop** unless exact
   cleanup and `/eos` lifecycle evidence are durable.
8. `S04-I21`–`S04-I25`: integrate and negative-test the runner-owned benchmark and
   strict verifier. Validate the plan without starting the live campaign. **Stop** if
   the clock can be reset, cleanup can cross 180 seconds and still pass, or unmatched
   arms can compare.
9. Run the complete correctness/failpoint matrix again separately. Only then run the
   focused 180-second campaign. Unsupported or unexecuted cells retain canonical
   status `NOT_RUN`; their evidence records an explicit `unverified` or
   `unsupported` availability/disposition and never implies compatibility.
10. `S04-I27`, `S04-H01`–`S04-H04`: verify final v1 authority, append report, update
    benchmark note, complete traceability, and write the Stage 05 handoff. Keep all
    Stage 07 deferrals explicit.

## 9. Typed Stage 04 E2E catalog

Every case is a separately selectable `e2e_test` declaration with a stable ID under
`runtime.layerstack-phase1.materialization.*`. A family `PASS` requires all of its
mandatory cases, exact retained evidence, and cleanup. An unsupported capability
case passes only when the product returns the expected typed capability failure
before mutation; an unexecuted environment cell is `NOT_RUN`, never a compatibility
pass.

### `S04-E01` exact reconstruction

Use a frozen manifest with raw-byte-safe path encodings, expected typed-object IDs,
entry counts, content digests, metadata, link topology, sparse allocation, final
`RootId`, and capability requirement.

| Case | Shape and proof |
| --- | --- |
| `E01-01` | Empty root and empty directories; exact modes/metadata and zero invented entries. |
| `E01-02` | Deep tree through final admitted depth `D=64`; bounded iterative traversal and exact root. |
| `E01-03` | Wide directory; bounded ordering/fanout and no whole-tree memory growth. |
| `E01-04` | Many tiny files/entries; entry-sensitive `E` scaling and exact content. |
| `E01-05` | Large regular file; byte-sensitive `R` scaling and bounded 256 KiB hydration buffer. |
| `E01-06` | Sparse file; logical length, extents/allocated bytes, content digest, and capability. |
| `E01-07` | Non-UTF-8/raw-byte path components; byte-for-byte names, no lossy conversion. |
| `E01-08` | xattrs including binary values/names where supported; typed fail-before-mutation otherwise. |
| `E01-09` | Hardlink groups; one inode relationship, link counts, content, and metadata. |
| `E01-10` | Symlinks including dangling/relative targets; no follow during reconstruction/verification. |
| `E01-11` | Metadata-only changes; distinct logical root and exact native metadata without content rewrite assumption. |
| `E01-12` | Device/FIFO nodes where authorized/supported; typed pre-mutation capability failure elsewhere. |
| `E01-13` | Deleted/whiteout entries; exact absence and no resurrection from carrier/base. |
| `E01-14` | Opaque directory semantics; lower children hidden exactly. |
| `E01-15` | Renames across directories; exact final tree, hardlink/metadata identity, no stale path. |
| `E01-16` | Mixed corpus combining deep/wide/tiny/large/sparse/raw metadata cases. |
| `E01-17` | Empty-to-mixed and mixed-to-deleted reconstruction produces the expected final root each time. |

For every case, verify the decoded typed object kind/domain/length/checksum, bounded
record limits, declared capability set, reconstructed native tree, and independent
logical re-walk to the frozen final root. Native path or inode identity is evidence,
not an input to `RootId`.

### `S04-E02` validation and fail-before-mutation

- `E02-01`: wrong typed-object domain/kind.
- `E02-02`: truncated, oversized, checksum-invalid, or length-inconsistent record.
- `E02-03`: manifest key/root/carrier/digest/fence mismatch.
- `E02-04`: missing carrier or missing `CURRENT`/generation.
- `E02-05`: corrupt selected generation, carrier byte, or metadata.
- `E02-06`: unsupported backend format/profile or required capability.
- `E02-07`: symlink/path traversal, duplicate raw path, ancestor type collision, or
  hostile device metadata.

Each case retains pre/post filesystem and resource snapshots and proves no new upper,
work, execution, mount, lease, `CURRENT`, carrier, or legacy request occurred before
the typed error.

### `S04-E03` reuse, single-flight, and residue

- `E03-01`: valid existing generation is reused; no carrier bytes rewritten and build
  counters remain zero.
- `E03-02`: concurrent same-key cold requests elect one build owner; all successful
  waiters receive the same generation/fence/manifest.
- `E03-03`: a cancelled waiter does not cancel the build while another owner/waiter
  exists and leaks no permit/task.
- `E03-04`: owner failure delivers one typed terminal outcome to all waiters; retry
  follows exact operation semantics.
- `E03-05`: two process/restart contenders leave at most the contractually bounded,
  attributable private operation residue; selector remains old or complete.
- `E03-06`: delete or corrupt a non-current, non-last orphan; explicit recovery
  classifies, rebuilds, or collects only that exact orphan without disturbing the
  selected generation.
- `E03-07`: delete or corrupt the current or last verified native carrier; strict
  access fails closed, retains logical source/object data and evidence, and rebuilds
  only through a later explicit cold operation.

### `S04-E04` strict native routing

- `E04-01` workspace creation/admission from a valid prebuilt generation.
- `E04-02` command execution and cancellation.
- `E04-03` file list/read/write/edit over the session's private upper.
- `E04-04` PTY creation, input, output drain, cancellation, and terminal response.
- `E04-05` daemon restart followed by valid strict admission/recovery.
- `E04-06` concurrent commands/files/PTYs/sessions on a shared immutable generation.
- `E04-07` missing/corrupt/unsupported strict request returns its candidate error;
  public v1 is never invoked and public authority remains v1.

For every warm request, deltas for CDC bytes/chunks, object reads/writes, hashes,
locator/compaction operations, pack operations, GC, squash, materialization
builds/bytes, and legacy fallback are exactly zero. Lookup, manifest validation,
lease, mount, and session work are reported separately and may be nonzero.

### `S04-E05` all build/sync/publication failpoints

Each failpoint executes before and after daemon restart, then exact retry where
applicable:

| Case | Injected boundary | Expected visibility/recovery |
| --- | --- | --- |
| `E05-01` | before operation `STATE` | no owned mutation |
| `E05-02` | after `STATE`, before private work | owned empty operation only |
| `E05-03` | during carrier file create/write | private attributable residue; no manifest/current |
| `E05-04` | after file data write, before file sync | incomplete private generation rejected/reaped |
| `E05-05` | file sync failure | same; typed I/O error |
| `E05-06` | directory create/metadata/sync failure | same; no partial visibility |
| `E05-07` | after all carrier sync, before logical verification | no manifest/current |
| `E05-08` | verification/capability failure | private failure, no selection |
| `E05-09` | during manifest temporary write | old/absent selection |
| `E05-10` | manifest file sync failure | old/absent selection |
| `E05-11` | after manifest file sync, before manifest rename | old/absent selection |
| `E05-12` | after manifest rename, before generation-dir sync | generation not selectable until recovery proves durability |
| `E05-13` | after durable manifest, before `CURRENT` temp | manifest may be reusable; old selection |
| `E05-14` | during `CURRENT` temp write | old selection |
| `E05-15` | `CURRENT` file sync failure | old selection |
| `E05-16` | after `CURRENT` temp sync, before rename | old selection |
| `E05-17` | after `CURRENT` rename, before parent sync | restart yields old or complete, never partial/mixed |
| `E05-18` | after durable `CURRENT`, before terminal operation state | recovery repairs terminal record to exact selected result |
| `E05-19` | terminal durable, response lost | exact retry returns recorded result without rebuild |

### `S04-E06` admission, mount, unmount, and response-loss failpoints

- `E06-01`: failure resolving/validating `CURRENT`.
- `E06-02`: failure before and after exact lease file sync/rename/parent sync.
- `E06-03`: failure allocating upper/work or persisting WorkspaceManager state.
- `E06-04`: failure before/during/after namespace holder creation.
- `E06-05`: failure before/during/after native overlay mount.
- `E06-06`: mount succeeds, response is lost; exact retry does not duplicate the
  session/lease/mount.
- `E06-07`: command/file/PTY response loss preserves existing idempotency semantics.
- `E06-08`: unmount busy/failure, process cancellation, and retry retain the lease
  until actual unmount.
- `E06-09`: unmount succeeds, failure before lease release; restart completes exact
  release once.
- `E06-10`: lease release durable, response lost; retry is terminal and does not
  delete another generation/session.

### `S04-E07` leases, switching, stability, and isolation

- `E07-01`: lease names exact materialization ID/generation/fence and predates mount.
- `E07-02`: logical head changes after admission; old session remains exact.
- `E07-03`: `CURRENT` switches; old leased session stays stable, new admission uses
  new generation.
- `E07-04`: two sessions share immutable carriers but have distinct upper, work,
  executions, mount namespaces, and writes.
- `E07-05`: old/new/building overlap is accounted without double counting.
- `E07-06`: release then grace/final recheck; reacquisition during grace blocks
  deletion.
- `E07-07`: pins and logical/source leases coexist without being confused with an
  exact generation lease.

### `S04-E08` cancellation and lifecycle cleanup

Run cancellation, injected panic, timeout, graceful shutdown, forced daemon restart,
holder exit, client disconnect, and response loss at build, wait, admission, mounted
session, command, file, PTY, unmount, and lease-release states. Each exact owned
resource has one terminal/recovery owner. At quiescence: zero detached tasks, strong
cycles, active run-owned workers/tasks/queues/permits/FDs/mappings/builds/leases/
sessions/uppers/mounts and zero unexplained persistent residue.

### `S04-E09` pressure and backpressure

- build-count/global-worker pressure (never more than four);
- buffer/byte-permit and queued-byte pressure;
- FD and mapping pressure;
- staging allocated-space pressure, including sparse apparent-versus-allocated
  distinction;
- `CURRENT`/pinned/leased generation overlap pressure;
- per-session upper-space pressure and concurrent-session admission;
- deadline/cancellation while queued.

The product must remain bounded, make deterministic progress or return a typed
backpressure/resource error, and never acquire resources out of the declared order.

### `S04-E10` inactive and active MCTS forks

- Inactive forks create constant-sized logical refs only: no materialization,
  carrier, upper, work, execution, or mount.
- A retained checkpoint or ordinary inactive head alone never forces a native tree;
  an explicit pin may retain/materialize only its named root through the explicit
  cold protocol.
- Activation may share an existing immutable generation but allocates a private
  upper/work/session/mount lease.
- Two active forks share no writable state.
- Deactivation releases session resources while retaining only intended refs/pins.
- Stage 04 does not add merge/promotion or general MCTS retention policy.

### `S04-E11` `/eos` lifecycle

One typed case per `S04-L01`–`S04-L13`, including raw path inventory and workload
masking. The teardown case deliberately seeds unrelated WorkspaceManager,
service-storage, daemon-runtime, and v1 compatibility sentinels and proves LayerStack
cleanup leaves them unchanged.

### `S04-E12` platform and target cells

Record every cell independently:

- Linux backend on Docker Engine/Linux and Docker Desktop Linux VM;
- backing filesystem identity/capability, including Docker-managed Linux volume and
  any explicitly tested bind/translated/remote filesystem;
- `amd64` and `arm64`;
- glibc, musl, minimal/distroless, shell-less, read-only, and non-root target images;
- device/FIFO, xattr, sparse, raw-name, ownership, and overlay capabilities.

Shell-less cells use public workspace/file APIs for verification. Unsupported cells
record a typed capability result. Unexecuted cells are `NOT_RUN` in the artifact and
tracker with a separate `availability: unverified` disposition; never infer
universal compatibility or an image-support percentage.

## 10. Exact future command registry and execution order

These commands are derived from current repository CLIs and Stage 03 paths. Paths
marked “new in Stage 04” are planned deliverables and must exist before the command
runs. Every live command, including a diagnostic rerun, requires an append-only
pre-entry and post-entry in `e2e/test-report.md`.

Set the immutable run identifiers explicitly; do not use command substitution:

```bash
export S04_PRODUCT=/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
export S04_TEST=/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
export S04_RUN_ID=<collision-resistant-stage04-run-id>
export S04_E2E_EVIDENCE="$S04_TEST/.e2e-state/evidence/$S04_RUN_ID"
export E2E_IMAGE='ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90'
export E2E_REBUILD_BINARY=1
export PYTHONPATH=e2e
```

`S04_RUN_ID` is the preallocated report/intent ID for product/E2E commands. The
existing benchmark service generates its own UUIDv7 before the runner starts; the
runner must persist that ID and allocate
`S04_ARTIFACT_ROOT=$S04_TEST/.benchmark-state/results/<runner-generated-run-id>`
before campaign clock start. Record both IDs and their relationship. After
`CMD-B02`, transcribe the exact returned/manifest runner ID as
`S04_RUNNER_RUN_ID` before any targeted cleanup. `<...>` is a required explicit
value, not shell syntax to copy literally. The run owner allocates
`S04_E2E_EVIDENCE` before the first test and retains each command's stdout, stderr,
exit status, start/end time, and SHA-256 as
`$S04_E2E_EVIDENCE/commands/<command-id>.json`; case evidence belongs under
`$S04_E2E_EVIDENCE/cases/<typed-case-id>/`.

### 10.1 Non-live custody and contract commands

`CMD-G01` — capture repository state without mutation:

```bash
git -C "$S04_PRODUCT" status --short --branch
git -C "$S04_PRODUCT" rev-parse HEAD
git -C "$S04_PRODUCT" rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
git -C "$S04_PRODUCT" diff --check
git -C "$S04_TEST" status --short --branch
git -C "$S04_TEST" rev-parse HEAD
git -C "$S04_TEST" rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
git -C "$S04_TEST" diff --check
```

Also retain `git diff --binary`, `git diff --cached --binary`, untracked/ignored
inventories, `ps`, listeners, `docker ps -a --no-trunc`, filesystem/mount identities,
and benchmark directory allocated sizes as separate custody artifacts. Do not pipe
sensitive configs/tokens into artifacts.

`CMD-G02` — frozen product contracts:

```bash
cd "$S04_PRODUCT"
cargo test --locked -p sandbox-runtime-layerstack-core --test canonical_contract
cargo test --locked -p sandbox-runtime-layerstack-core --test hostile_v3_decode
cargo test --locked -p sandbox-runtime-layerstack-core --test host_independence
cargo test --locked -p sandbox-runtime-layerstack --test portable_root_golden
```

### 10.2 Product format, lint, unit, and integration commands

`CMD-P01`:

```bash
cd "$S04_PRODUCT"
cargo fmt --all -- --check
```

`CMD-P02`:

```bash
cd "$S04_PRODUCT"
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack -p sandbox-runtime-workspace -p sandbox-runtime -p sandbox-runtime-overlay -p sandbox-runtime-namespace-execution -p sandbox-runtime-namespace-process --all-targets --all-features -- -D warnings
```

`CMD-P03` — new product materialization suite:

```bash
cd "$S04_PRODUCT"
cargo test --locked -p sandbox-runtime-layerstack --test candidate_materialization
```

`CMD-P04` — new strict workspace suite:

```bash
cd "$S04_PRODUCT"
cargo test --locked -p sandbox-runtime --test workspace_session_materialization
```

`CMD-P05` — inherited compatibility/regression:

```bash
cd "$S04_PRODUCT"
cargo test --locked -p sandbox-runtime-layerstack --test candidate_publication
cargo test --locked -p sandbox-runtime --test workspace_session_publish
cargo test --locked -p sandbox-runtime --test workspace_session_publish_security
cargo test --locked -p sandbox-runtime --test storage_route_observation
cargo test --locked -p sandbox-runtime-namespace-execution
```

New test target names above are exact planned filenames, not claims that they
already exist.

### 10.3 Typed catalog and complete E2E commands

`CMD-E01` — collect and validate the typed catalog through the existing collector:

```bash
cd "$S04_TEST"
PYTHONPATH=e2e .venv/bin/python -m harness.catalog.collect --test-repository-root "$S04_TEST" --product-root "$S04_PRODUCT"
```

`CMD-E02` — collect only the new module's tests without running them:

```bash
cd "$S04_TEST"
PYTHONPATH=e2e .venv/bin/python -m pytest --collect-only -q e2e/runtime/layerstack_phase1/test_candidate_materialization.py --test-repository-root "$S04_TEST" --product-root "$S04_PRODUCT"
```

`CMD-E03` — full Stage 04 correctness/failpoint matrix, outside the benchmark clock:

```bash
cd "$S04_TEST"
E2E_IMAGE="$E2E_IMAGE" E2E_REBUILD_BINARY=1 PYTHONPATH=e2e .venv/bin/python -m pytest -vv e2e/runtime/layerstack_phase1/test_candidate_materialization.py --test-repository-root "$S04_TEST" --product-root "$S04_PRODUCT"
```

Use `-k '<stable typed case expression>'` only for a reported diagnostic or defect
iteration. A focused pass never replaces `CMD-E03`.

### 10.4 Benchmark contract tests and plan validation

`CMD-A01` — strict artifact/verifier positive and negative tests:

```bash
cd "$S04_TEST"
.benchmark-state/test-venv/bin/python -m pytest -q benchmark/backend/tests/compatibility/test_artifacts.py benchmark/backend/tests/unit/test_stage04_materialization.py benchmark/backend/tests/contract/test_planning.py benchmark/backend/tests/integration/test_runner.py
```

`CMD-B01` — validate the new Stage 04 plan without running it:

```bash
cd "$S04_TEST/benchmark"
../.benchmark-state/test-venv/bin/sandbox-benchmark validate --plan layerstack-phase1-stage04-materialization --test-repository-root "$S04_TEST" --product-root "$S04_PRODUCT" --product-bin-dir "$S04_PRODUCT/bin"
```

`CMD-B02` — focused live campaign, only after all correctness gates:

```bash
cd "$S04_TEST/benchmark"
../.benchmark-state/test-venv/bin/sandbox-benchmark run --plan layerstack-phase1-stage04-materialization --test-repository-root "$S04_TEST" --product-root "$S04_PRODUCT" --product-bin-dir "$S04_PRODUCT/bin"
```

`CMD-B03` — bounded recovery of the exact run after interruption:

```bash
cd "$S04_TEST/benchmark"
../.benchmark-state/test-venv/bin/sandbox-benchmark recover --test-repository-root "$S04_TEST" --product-root "$S04_PRODUCT" --product-bin-dir "$S04_PRODUCT/bin"
```

`CMD-B04` — ownership-aware cleanup for that exact run:

```bash
cd "$S04_TEST/benchmark"
../.benchmark-state/test-venv/bin/sandbox-benchmark cleanup --run-id "$S04_RUNNER_RUN_ID" --test-repository-root "$S04_TEST" --product-root "$S04_PRODUCT" --product-bin-dir "$S04_PRODUCT/bin"
```

Recovery and safety cleanup cannot change a missed 180-second campaign into `PASS`.
The current `recover` command scans durable stale-run state rather than accepting a
run ID; inspect its candidate manifests first and append pre/post report entries for
every affected run. Do not invoke cleanup without inspecting the exact runner ID and
its ownership ledger.

### 10.5 Dependency and final documentation validation

`CMD-D01` — reuse the Stage 03 dependency comparator architecture:

```bash
cd "$S04_TEST"
.venv/bin/python e2e/tools/verify_external_dependency_delta.py \
  .e2e-state/evidence/stage00-entry-20260724T134437+0800/stage00-entry-baseline.json \
  --product-root "$S04_PRODUCT" \
  --test-root "$S04_TEST" \
  --output ".e2e-state/tmp/$S04_RUN_ID/dependency-delta-a.json" \
  --require-stdlib-crate sandbox-runtime-layerstack-core \
  --require-exact-external-delta-zero
```

The baseline path and comparator are present at guide authoring. Revalidate both
identities at entry; a missing or changed frozen baseline is a blocker, not permission
to substitute a new one. Repeat the same command with
`dependency-delta-b.json`, require byte-equivalent normalized results, and retain the
final report under the artifact root. One comparator invocation executes all 16
frozen target/feature captures. Also retain a source/process/network/system-helper/
service/image audit; raw `cargo metadata`, package counts, or a glob are not a
substitute.

`CMD-H01`:

```bash
git -C /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs diff --check
```

### 10.6 Required execution order

`CMD-G01` → report pre-entry → `CMD-G02` → `CMD-P01` → `CMD-P02` → `CMD-P03`
→ `CMD-P04` → `CMD-P05` → `CMD-E01` → `CMD-E02` → `CMD-A01` → `CMD-B01`
→ full report pre-entry → `CMD-E03` → full report post-entry → correctness review
→ benchmark report pre-entry → `CMD-B02` → verifier → benchmark report post-entry
→ exact `CMD-B03`/`CMD-B04` only if needed → dependency audit → final v1 regression
→ `CMD-H01`.

No campaign performance verdict is legal before the separate complete correctness
and failpoint matrix succeeds. Every arrowed test, live diagnostic, and benchmark
gets its own append-only pre/post report pair and command-result artifact; the phase
labels above do not authorize one report entry to cover several invocations.

## 11. Focused 180-second benchmark E2E campaign

### 11.1 Verdict boundary

`S04-B01` is one runner-owned monotonic budget of exactly 180 seconds. It is Stage 04
POC evidence, not Stage 07 qualification. The same runner owns the monotonic clock,
resource creation, operation admission, sampling, artifact writes, verification,
cleanup, and durable cleanup ledger.

Prerequisites occur outside the clock: locked builds; exact binary/config/source
digests; pinned image index and selected platform manifest/config; deterministic
fixture generation and digest verification; plan validation; filesystem/backend
capability probe; baseline/candidate topology plan; and empty, uniquely owned artifact
root allocation. Record prerequisite elapsed time separately and apply identical
preparation to baseline and candidate arms. Do not pre-warm only one arm.

Clock rules:

- Start before the first pre-campaign resource **and allocated-space** sample or
  creation of any campaign topology.
- Stop admitting new workload operations at exactly `start + 150s`.
- Reserve `[150s,180s)` solely for settling, final samples, artifact
  serialization/fsync, strict verification, cleanup, quiescence, and durable cleanup
  ledger.
- End only after that ledger is file-synced, atomically installed, and its parent
  directory synced.
- At `start + 180s`, the campaign is `FAIL` if the end boundary is incomplete.
- Failed attempts and retries consume the same clock; it is never reset.
- No single operation may exceed 60 seconds.
- Safety cleanup after overrun is separately timed/reported and cannot convert the
  failed campaign to `PASS`.

### 11.2 Deterministic allocation

The initial allocation is normative unless retained inspection supports a documented
replacement. A replacement must still total 180 seconds, stop admission at 150, own
the last 30 seconds for cleanup, and preserve every family.

| Window | Duration | Required work |
| --- | ---: | --- |
| `0–12s` | 12s | Clock-start pre-samples, ownership controls, valid-generation reuse. |
| `12–47s` | 35s | Cold reconstruction at byte-sensitive `R` and entry-sensitive `E` scales; native-copy controls. |
| `47–77s` | 30s | Warm activation plus command, file, and PTY strict-native samples at controlled depths. |
| `77–102s` | 25s | Same-key concurrent build/waiters and shared-generation isolated sessions. |
| `102–122s` | 20s | Atomic `CURRENT` switch, stable old exact lease/session, old/new/building overlap accounting. |
| `122–137s` | 15s | Inactive/active MCTS and quota/backpressure sentinel. |
| `137–150s` | 13s | Representative deterministic crash/restart recovery; no new admission at boundary. |
| `150–180s` | 30s | Settled samples, artifact serialization/fsync, strict verifier, exact cleanup, quiescence, durable ledger. |
| **Total** | **180s** | Admission interval 150s plus cleanup interval 30s. |

### 11.3 Pairing, ordering, and samples

Use counterbalanced baseline/candidate ordering at the smallest safe block, for
example `A-B-B-A` followed by its balanced complement, with identical fixtures,
deadlines, sampling, filesystems, and client path. Persist the generated deterministic
order and every raw sample. A failed or unmatched arm invalidates that pair; it may
not be replaced outside the same clock.

Inferential p95 requires at least 20 valid raw samples **per compared arm and
workload/depth cell**. If the 180-second campaign cannot supply them, report the
diagnostic order statistic actually computed, the raw count, and
`INSUFFICIENT_SAMPLE` (or `NOT_RUN` if unmeasured). Never label a maximum, interpolated
quantile, combined heterogeneous cell, or fewer than 20 samples as a p95 `PASS`.

### 11.4 Time measurements and gates

All samples use runner-owned monotonic start/end boundaries with queue, setup,
operation, verification, and teardown separated.

| Measurement | Required factors and result |
| --- | --- |
| cold reconstruction throughput | At byte-sensitive scales regress/compare elapsed against reconstructed bytes `R`; at entry-sensitive scales against entries `E`; at least 70% of same-filesystem native-copy control |
| cold activation end to end | Explicit request through verified selected generation and usable session; p95 no more than `1.5 ×` native-copy control plus measured warm allowance |
| warm plan validation | Multiple depths including maximum admitted `D=64`; report depth slope and per-depth raw samples |
| mount/session admission | `CURRENT` lookup, manifest validation, exact lease, private dirs, native mount, response split and combined |
| warm session/root/mount | p50 and p95 no more than baseline plus 5% plus 2 ms |
| no-op command | no more than direct Docker exec plus 3% plus 0.5 ms; native command throughput at least 97% of control |
| file read/write | native-route throughput at least 97% of control with exact content/metadata |
| PTY create/drain | create no more than control plus 3% plus 1 ms; drain no more than control plus 3% plus 0.5 ms; response follows drain |
| cancellation | bounded terminal/cancellation latency with zero detached work |
| already-materialized reuse | no build/hydration and lower than explicit cold path; never compare unmatched fixture/root |
| concurrent build waiters | owner and waiter latency, one build, exact shared result, bounded cancellation |
| concurrent sessions | admission/command/file/PTY latency and isolation at declared concurrency |
| warm forbidden work | zero CDC/object/hash/locator/pack/GC/squash/materialization/fallback deltas for every warm sample |

An unavailable control or insufficient p95 makes that gate `NOT_RUN` or
`INSUFFICIENT_SAMPLE`; it does not become zero or pass by prose.

### 11.5 Physical space measurements

Measure allocated physical blocks/bytes with recorded tool/filesystem semantics, not
apparent file length. Sparse logical length is reported separately. Sample:

1. pre-build;
2. private-build peak;
3. verified manifest before `CURRENT`;
4. immediately after `CURRENT`;
5. concurrent-session peak;
6. old/new/building generation overlap;
7. post-restart;
8. post-lease release and grace/final recheck;
9. settled state; and
10. final cleanup.

Every sample separately reports carriers, logical sources, private uppers,
work/execution scratch, build staging, manifests, refs/leases, operations, metadata,
v1 compatibility bytes, duplicate bytes, lease-blocked bytes, orphan/residue bytes,
and unexplained bytes. Device/inode or shared-extent evidence prevents double
counting; hardlinks and reflinks are not summed as independent allocation without
proof.

Reconcile:

```text
T = L_hot + H_cold + sum(U_active) + P_staging + M
```

`T` is total allocated owned storage; `L_hot` logical/candidate hot storage;
`H_cold` immutable materialized carriers; `U_active` each private active upper;
`P_staging` private build/work/execution staging; `M` manifests, refs, leases,
operations, and other metadata. V1 compatibility and excluded service/runtime bytes
are shown as separate context and must not be smuggled into a smaller component.
Report reconciliation residual as unexplained bytes. Final unexplained persistent
residue must be exactly zero.

Cold peak target is one final cold target plus no more than 5% staging overhead,
classified by actual allocated bytes. Do not claim this threshold if sharing or
allocation cannot be measured.

### 11.6 Resource measurements

Sample baseline, peak, settled, and final:

- process/cgroup RSS and idle baseline;
- active/peak workers (global maximum four), tasks and detached tasks;
- buffer bytes (each hydration buffer at most 256 KiB);
- queue items/bytes and byte permits requested/in-use/peak;
- operation owners, builds, waiters, cancellation and backpressure counts;
- open FDs by class and memory mappings;
- generation/logical leases and pins;
- sessions, private uppers/work dirs, executions, mounts/namespaces;
- strong ownership cycles and join-handle disposition.

Required limits are RSS at most 384 MiB absolute and at most 128 MiB above idle,
bounded workers/tasks/queues/FDs/mappings/leases/sessions/uppers, and at final
quiescence zero active run-owned resources, detached tasks, strong cycles, or
unexplained residue.

## 12. Artifact, verifier, reporting, cleanup, and quiescence

### 12.1 Strict artifact schema (`S04-A01`)

The Stage 04 artifact is versioned, closed (`additionalProperties: false` where
feasible), finite, and JSON-serializable with `allow_nan=false`. It must contain:

The runner owns this exact retained layout under the uniquely allocated artifact
root; these are test evidence paths, never product `/eos` protocol:

```text
$S04_ARTIFACT_ROOT/
└── stage04/
    ├── custody-pre.json
    ├── identities.json
    ├── fixture.json
    ├── correctness/cases.ndjson
    ├── lifecycle/eos-boundaries.ndjson
    ├── samples/time.ndjson
    ├── samples/space.ndjson
    ├── samples/resources.ndjson
    ├── counters/native-route.ndjson
    ├── environment/cells.ndjson
    ├── verdict.json
    ├── cleanup/ledger.json
    ├── stage04-materialization-evidence-v1.json
    └── sha256sums.json
```

Every component is written to a same-directory temporary file, file-synced,
atomically renamed, and parent-directory-synced. The final evidence envelope names
and hashes every component; `sha256sums.json` is generated last before strict
verification, and the cleanup ledger's durable boundary remains inside the campaign
clock.

| Group | Mandatory evidence |
| --- | --- |
| envelope | schema/version, case/campaign ID, completeness flag, run ID, creation UTC, artifact-root identity |
| source identity | product/test commit, upstream, source diff digests, Cargo.lock/dependency digest, config digest, exact command |
| runtime identity | binary digests, image index/platform manifest/config, architecture, kernel, Docker engine/VM, filesystem/mount/capabilities |
| fixture/key | fixture/generator/version/digests, typed `RootId`, materialization key/ID, backend/profile |
| custody | pre-existing processes/listeners/containers/paths, run-owned resource ledger and collision controls |
| clock | prerequisite elapsed, monotonic start, 150s admission stop, 180s deadline, last admission, end, maximum operation, post-overrun cleanup timing |
| correctness | typed-object/length/capability/final-root results, reconstruction cases, route/no-fallback, failpoints, leases, isolation, MCTS |
| generation lifecycle | operation states, carriers, manifest/current digests/fences, lease events, selector/head changes, grace/final recheck |
| raw time samples | arm/order/pair/workload/depth/scale, timestamps, latency components, disposition, invalidation reason |
| space | all ten boundaries, method/availability, allocated/apparent bytes, every accounting bucket, sharing/dedup proof, total and residual |
| resources | all gauges/high-water marks and availability, idle/absolute/delta RSS, permits/backpressure, FDs/mappings, ownership graph |
| route counters | allowed native lookup/validation/mount work and every forbidden warm-work/fallback counter, before/after/delta |
| environment matrix | each required cell with closed status `PASS`, `FAIL`, or `NOT_RUN`, plus a separate supported/unsupported/unverified availability disposition and reason |
| verdict | correctness, deadline, performance gate-by-gate, sample sufficiency, space/resource, cleanup; no universal rollup from missing cells |
| cleanup | exact ordered actions/results, retained intentional objects, pre/post comparison, quiescence, durable ledger path/digest/sync boundary |

Measurements use an explicit record such as
`{"availability":"measured","value":0,"unit":"bytes","method":"..."}` or
`{"availability":"unavailable","reason":"..."}`. Missing/unsupported is never encoded
as numeric zero, `null`, empty string, or absent required field. `—` appears only in
human trackers to mean no artifact exists.

### 12.2 Strict verifier (`S04-A02`)

The verifier rejects, at minimum:

- missing mandatory groups/fields, `null`, NaN/infinity, unknown enum/status, duplicate
  run/sample IDs, invalid digests, or an artifact outside the owned root;
- any unavailable/missing/unsupported measurement coerced to zero;
- inconsistent apparent/allocated units, byte totals, equation components, duplicate
  accounting, negative residual, or nonzero unexplained persistent residue;
- invalid timestamp/sample order, elapsed arithmetic, an admission at/after 150
  seconds, operation over 60 seconds, clock reset, end/cleanup-ledger boundary after
  180 seconds, or retry outside the original clock;
- unmatched fixture, topology, baseline/candidate pair, ordering, scale, depth,
  platform, or control;
- a claimed inferential p95 `PASS` with fewer than 20 valid samples per compared arm,
  or a diagnostic order statistic labeled p95;
- unsupported/unexecuted compatibility represented as pass, universal support, or a
  percentage;
- wrong logical root, typed object/domain/length/capability mismatch, mutable carrier,
  manifest-before-carrier violation, or `CURRENT` before manifest durability;
- missing/exact-lease mismatch, early lease release, old-session drift after selector
  change, shared upper/work/execution/mount namespace, or deletion without
  grace/final recheck;
- any legacy fallback or warm CDC/object/hash/locator/pack/GC/squash/materialization
  work;
- public authority other than `legacy_v1`;
- resource cap/permit/RSS violation, detached task/strong cycle, active run-owned
  resource after quiescence, missing ownership, or cleanup outside the ledger;
- performance `PASS` before separate correctness/failpoint evidence, after a deadline
  failure, with an incomplete cleanup ledger, or from a safety-cleanup recovery.

Negative tests mutate one invariant at a time and assert the specific bounded error;
include every rejection family above. The verifier must accept one complete frozen
golden artifact.

### 12.3 Append-only E2E reporting (`S04-A03`)

Before **and** after every future live test, benchmark, or diagnostic, append to:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md
```

The pre-entry records UTC time, exact command, intent/case IDs, custody snapshot and
owner, product/test commits/diffs, binary/config/image/platform/filesystem identities,
run ID, allocated ports/container labels/directories/processes, artifact root, timeout
and cleanup plan.

The post-entry records monotonic and wall elapsed, exact result/status, passed/failed/
skipped counts, Stage 04 claim actually tested, defect and fix-next, every retained
artifact/digest, owned resources created, exact cleanup actions/results, intentional
retained state, quiescence comparison, and reporter identity. Append a failed/aborted
post-entry even when setup fails. Never rewrite a previous entry.

### 12.4 Cleanup and quiescence (`S04-R01`–`S04-R08`)

| ID | Required proof |
| --- | --- |
| `S04-R01` | Ownership ledger is durable before each resource creation and records process/container/session/build/lease/path/port/config identity. |
| `S04-R02` | Build cancellation/panic/timeout/restart joins tasks, closes FDs/mappings, releases permits, and classifies/reaps only exact private residue. |
| `S04-R03` | Admission rollback unmounts before releasing lease and removes only the exact private session state. |
| `S04-R04` | Normal teardown drains command/PTY, stops executions, unmounts, retires session, releases lease, then evaluates generation eligibility. |
| `S04-R05` | Grace/final recheck sees current selector, pins, logical/source leases, and exact generation leases under the required fence/barrier. |
| `S04-R06` | WorkspaceManager, service-storage, daemon-runtime, v1, pre-existing processes/listeners/containers, and retained evidence are unchanged. |
| `S04-R07` | Final gauges and path/mount/process/container samples prove zero active run-owned resources and zero unexplained residue. |
| `S04-R08` | Cleanup ledger is serialized, file-synced, atomically installed, parent-synced inside the 180-second campaign; post-overrun safety cleanup is separate. |

## 13. Verification traceability matrix

`Current status` is deliberately `NOT_RUN`: no direct Stage 04 execution evidence was
found. Command IDs resolve to the exact registry in §10. An artifact cell uses `—`
only because no Stage 04 artifact exists.

| Verification ID | Requirement/invariant | Test layer and case | Exact future command | Required evidence and counters | Threshold/expected result | Current status | Artifact/digest | Cleanup proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S04-V01` | Typed catalog complete/stable | catalog + `S04-E01`–`E12` collection | `CMD-E01`, `CMD-E02` | stable IDs, case count, catalog digest | every mandatory case collected once | `NOT_RUN` | — | no runtime resources |
| `S04-V02` | Frozen v2/v3 bytes/IDs/bounds/RootId | core golden/hostile/host independence | `CMD-G02` | test logs, corpus/source digests | exact PASS, zero fixture drift | `NOT_RUN` | — | no runtime resources |
| `S04-V03` | `legacy_v1` sole public authority | product route observation + `E04-07` | `CMD-P05`, `CMD-E03` | read/write authority, fallback counters | both `legacy_v1`; fallback 0 | `NOT_RUN` | — | exact E2E ledger |
| `S04-V04` | Stage 03 compatibility retained | inherited publication/security suites | `CMD-P05` | direct new logs; Stage 03 hashes labeled inherited | all selected regressions PASS | `NOT_RUN` | — | test process exit |
| `S04-V05` | Exact empty/deep/wide/tiny reconstruction | product + `E01-01`–`04` | `CMD-P03`, `CMD-E03` | typed IDs, lengths, entries, root, allocations | exact fixture; `D=64`; bounded | `NOT_RUN` | — | `L01`–`L13` |
| `S04-V06` | Large/sparse/raw-byte reconstruction | product + `E01-05`–`07` | `CMD-P03`, `CMD-E03` | content, extents, raw names, root, buffer | exact; buffer ≤256 KiB | `NOT_RUN` | — | exact build cleanup |
| `S04-V07` | xattr/hardlink/symlink | product + `E01-08`–`10` | `CMD-P03`, `CMD-E03` | xattrs, inode/link graph, targets, no-follow | exact or typed pre-mutation unsupported | `NOT_RUN` | — | exact build cleanup |
| `S04-V08` | metadata/device/FIFO | product + `E01-11`–`12` | `CMD-P03`, `CMD-E03` | metadata/capabilities/root | exact supported; typed unsupported | `NOT_RUN` | — | no mutation on failure |
| `S04-V09` | deleted/opaque/renamed/mixed | product + `E01-13`–`17` | `CMD-P03`, `CMD-E03` | final path set, whiteout/opaque/link metadata/root | exact fixture | `NOT_RUN` | — | exact build cleanup |
| `S04-V10` | Typed/capability/hostile failure before mutation | `S04-E02` | `CMD-P03`, `CMD-E03` | pre/post tree/resources, error type | no new lease/mount/upper/current/fallback | `NOT_RUN` | — | baseline restored |
| `S04-V11` | Valid generation reuse | `E03-01`, benchmark 0–12s | `CMD-E03`, `CMD-B02` | generation/fence, build/hydration counter delta | same valid generation; build work 0 | `NOT_RUN` | — | session/build cleanup |
| `S04-V12` | Same-key single-flight, orphan/last-locator recovery, crash residue | `E03-02`–`07` | `CMD-P03`, `CMD-E03` | owner/waiters, result IDs, selected/last-locator state, source holds, residue bytes | one build; bounded attributable residue; orphan exact; current/last fails closed | `NOT_RUN` | — | waiters/tasks/permits 0; exact residue classified |
| `S04-V13` | Manifest after fully synced verified carrier | `E05-03`–`13`, `L02`–`L03` | `CMD-P03`, `CMD-E03` | sync events, manifest/carrier/root/capabilities | no manifest before verified durability | `NOT_RUN` | — | private residue owned |
| `S04-V14` | Atomic `CURRENT` and exact fence | `E05-13`–`19`, `L04` | `CMD-P03`, `CMD-E03` | temp/fsync/rename/parent events, selector bytes | old or complete, never partial | `NOT_RUN` | — | recovery terminal |
| `S04-V15` | Exact generation lease before mount | `E06-01`–`05`, `E07-01`, `L05` | `CMD-P04`, `CMD-E03` | ordered lease/mount events and tuple | exact tuple, lease durable first | `NOT_RUN` | — | unmount then release |
| `S04-V16` | Stable old session over head/current change | `E07-02`–`03`, `L06` | `CMD-P04`, `CMD-E03` | old/new session root/generation/fence | old stable; later admission new | `NOT_RUN` | — | both exact leases released |
| `S04-V17` | Shared carrier, isolated writable/execution state | `E07-04`–`05` | `CMD-P04`, `CMD-E03` | inode/carrier and distinct dirs/ns IDs | only carrier shared | `NOT_RUN` | — | each session exact teardown |
| `S04-V18` | Grace/final recheck deletion | `E07-06`–`07`, `L09`–`L10` | `CMD-P03`, `CMD-E03` | lease/pin/current/last-locator timeline and recheck | no protected deletion; reacquire or last-locator status blocks | `NOT_RUN` | — | eligible only after final check |
| `S04-V19` | Build/state failpoints | `E05-01`–`08` | `CMD-P03`, `CMD-E03` | each failpoint/restart/tree/state | old/absent selection; typed recovery | `NOT_RUN` | — | residue bounded/reaped |
| `S04-V20` | Manifest sync failpoints | `E05-09`–`13` | `CMD-P03`, `CMD-E03` | write/fsync/rename/dir-sync boundaries | no premature selection | `NOT_RUN` | — | exact operation recovery |
| `S04-V21` | `CURRENT`/terminal/response failpoints | `E05-14`–`19` | `CMD-P03`, `CMD-E03` | selector/terminal/retry IDs | old or complete; retry no rebuild | `NOT_RUN` | — | exact operation terminal |
| `S04-V22` | Admission/mount response failpoints | `E06-01`–`07` | `CMD-P04`, `CMD-E03` | state/lease/session/mount/response IDs | no duplicate or partial session | `NOT_RUN` | — | reverse rollback |
| `S04-V23` | Unmount/lease-release failpoints | `E06-08`–`10` | `CMD-P04`, `CMD-E03` | mountinfo, lease state, retry | lease retained until unmount; exact once | `NOT_RUN` | — | mount+lease absent |
| `S04-V24` | Cancel/panic/timeout/shutdown/restart | `S04-E08` | `CMD-P03`, `CMD-P04`, `CMD-E03` | ownership graph, joins, resources | terminal typed result; no leak | `NOT_RUN` | — | `R01`–`R08` |
| `S04-V25` | Strict command/file/PTY/workspace native route | `S04-E04` | `CMD-P04`, `CMD-E03` | route identity, selected tuple, operation results | exact native route; no fallback | `NOT_RUN` | — | session exact teardown |
| `S04-V26` | `/eos` masked and mount native/no fallback | `E04`, `E11`, overlay tests | `CMD-P04`, `CMD-E03` | workload probes, mountinfo, kernel errors | `/eos` invisible; no mount fallback | `NOT_RUN` | — | namespace unmounted |
| `S04-V27` | Warm forbidden work zero | every warm `E04` sample | `CMD-E03`, `CMD-B02` | before/after deltas for CDC/object/hash/locator/compaction/pack/GC/squash/materialization/fallback | each delta exactly 0 | `NOT_RUN` | — | counters settle |
| `S04-V28` | Restart/concurrency routing and isolation | `E04-05`–`06`, `E07` | `CMD-P04`, `CMD-E03` | session/generation/ns/results | stable exact results; bounded | `NOT_RUN` | — | all owned resources 0 |
| `S04-V29` | Quotas/backpressure/resources | `S04-E09` | `CMD-P03`, `CMD-E03` | workers/buffer/permits/RSS/FD/maps/queues | ≤4; ≤256 KiB; RSS caps; bounded | `NOT_RUN` | — | all final gauges 0 |
| `S04-V30` | MCTS inactive/active allocation | `S04-E10` | `CMD-E03`, `CMD-B02` | refs/materializations/uppers/leases deltas | inactive O(1) refs; active private state | `NOT_RUN` | — | active fork teardown |
| `S04-V31` | Linux/backend capability correctness | `S04-E12` supported cells | `CMD-E03` | kernel/backend/fs/capability identities | per-cell direct result only | `NOT_RUN` | — | exact cell resources |
| `S04-V32` | Docker/arch/target matrix | `S04-E12` | `CMD-E03` per selected env | image/platform/arch/target result | unrun `NOT_RUN`; no universal claim | `NOT_RUN` | — | per-cell cleanup |
| `S04-V33` | Dependency/portable-core boundary | Cargo metadata + source audit | `CMD-D01`, `CMD-P02` | dependency graph/delta, unsafe/OS import audit | zero unexplained delta; core portable | `NOT_RUN` | — | no runtime resources |
| `S04-V34` | Plan/schema/golden/runner dispatch | benchmark contract tests | `CMD-A01`, `CMD-B01` | expanded plan, schema/golden digests | exact frozen 180/150/60 contract | `NOT_RUN` | — | no live topology |
| `S04-V35` | Verifier negative cases | artifact compatibility tests | `CMD-A01` | one rejection artifact per §12.2 | every malformed claim rejected | `NOT_RUN` | — | temp test artifacts removed |
| `S04-V36` | One runner-owned monotonic clock | focused campaign | `CMD-B02` | start/stop/deadline/last admission/ledger sync | admission <150s; complete ≤180s | `NOT_RUN` | — | ledger durable inside clock |
| `S04-V37` | Counterbalanced raw timing and sufficiency | focused campaign | `CMD-B02` | order, matched pairs, raw samples/counts | p95 only with ≥20/arm/cell | `NOT_RUN` | — | topology teardown |
| `S04-V38` | Cold throughput/activation gates | 12–47s campaign | `CMD-B02` | `R`, `E`, copy controls, raw timings | ≥70%; p95 ≤1.5×copy+warm | `NOT_RUN` | — | build/session cleanup |
| `S04-V39` | Warm depth/mount/command/file/PTY gates | 47–77s campaign | `CMD-B02` | per-depth samples through `D=64`, counters | Prep 04 gates in §11.4 | `NOT_RUN` | — | sessions/executions 0 |
| `S04-V40` | Concurrent build/session/switch/MCTS | 77–137s campaign | `CMD-B02` | waiter/session/current/lease/MCTS samples | exact/isolation/bounded, matched | `NOT_RUN` | — | owners/resources 0 |
| `S04-V41` | Representative restart recovery | 137–150s campaign | `CMD-B02` | deterministic failpoint/restart outcome | old or complete; no leak | `NOT_RUN` | — | recovered exact run |
| `S04-V42` | Allocated-space equation and residue | all ten samples | `CMD-B02` | buckets, sharing evidence, `T` residual | cold staging ≤5%; unexplained final 0 | `NOT_RUN` | — | final allocation reconciled |
| `S04-V43` | Append-only before/after reporting | report review around every command | exact command being reported | report file digest and entries | complete pair, no history edit | `NOT_RUN` | — | exact cleanup recorded |
| `S04-V44` | Benchmark note evidence honesty | doc review after verifier | `CMD-H01` | links/digests/statuses | missing cells not promoted | `NOT_RUN` | — | references ledger |
| `S04-V45` | Complete `/eos` lifecycle/ownership | `S04-E11`, `L01`–`L13` | `CMD-E03` | inventories/mountinfo/allocated bytes/sentinels | all lifecycle assertions exact | `NOT_RUN` | — | `L11`–`L13` |
| `S04-V46` | Final v1 authority regression | product + public E2E comparison | `CMD-P05`, `CMD-E03` | route/bytes/results/counters | v1 behavior exact; authority v1 | `NOT_RUN` | — | no candidate leak |
| `S04-V47` | Outgoing Stage 05 handoff complete | doc/evidence review | `CMD-H01` | source/run/artifact hashes, blockers/deferrals | no unsupported claim; exact custody | `NOT_RUN` | — | cleanup digest included |

## 14. Canonical progress and completion rules

### 14.1 Closed status vocabulary

The only statuses are:

`OPEN`, `IN_PROGRESS`, `BLOCKED`, `PASS`, `FAIL`, `NOT_RUN`,
`INSUFFICIENT_SAMPLE`, and `DEFERRED_STAGE_07`.

Rules:

1. This table is the only canonical Stage 04 progress record. Narrative and the
   append-only report can support it but cannot silently change status.
2. Only one active owner changes a row from `OPEN` to `IN_PROGRESS`; record UTC,
   custody, and the intended artifact first.
3. `PASS` requires the named direct Stage 04 command/result, retained artifact
   SHA-256, verified threshold, and cleanup proof. A code diff, review, Stage 03
   artifact, source inspection, or “expected” result is not a pass.
4. `FAIL` retains evidence and defect/fix-next. A later retry is a new run/report
   pair; do not rewrite the failed record.
5. `BLOCKED` names an exact contradiction, missing authority decision, custody
   collision, or capability preventing safe progress.
6. `NOT_RUN` means no valid execution. `INSUFFICIENT_SAMPLE` means executed but the
   declared inferential threshold lacks the required matched raw samples.
7. `DEFERRED_STAGE_07` is allowed only for the enumerated qualification/retirement
   work in §16. It may not hide a Stage 04 correctness gate.
8. Artifact paths are absolute or run-root-relative and always include SHA-256.
   `—` means no artifact exists; it never means zero.
9. A runtime row cannot be `PASS` while cleanup is missing, partial, after the
   campaign deadline, or based on broad/unowned cleanup.
10. Recompute checklist coverage after any added/removed requirement. No orphan
    checklist, work, or verification ID is allowed.

### 14.2 Canonical progress tracker

| Work ID | Depends on | Deliverable | Current status | Completion condition / exact verification | Run/artifact path and digest | Owner/blocker | Cleanup result | Last updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S04-G01` | — | fresh custody/ownership inventory | `OPEN` | `S04-V43`; exact pre-entry retained | — | implementation owner; shared custody | — | 2026-07-25 |
| `S04-G02` | `G01` | handoff/decision/corpus/evidence identity reconciliation | `OPEN` | all recorded digests agree; contradiction handled per §1.3 | — | implementation owner | no runtime | 2026-07-25 |
| `S04-G03` | `G02` | authority baseline | `OPEN` | `S04-V03` direct result | — | product owner | exact test cleanup required | 2026-07-25 |
| `S04-G04` | `G02` | frozen contract baseline | `OPEN` | `S04-V02` | — | core owner | no runtime | 2026-07-25 |
| `S04-G05` | `G02` | approved `/eos` owner map | `OPEN` | `S04-V45`; no ambiguous/forbidden path | — | storage owner | no mutation | 2026-07-25 |
| `S04-G06` | `G01`–`G05` | locked environment and artifact root | `OPEN` | identities/capabilities/ports/root retained | — | runner owner | root owned exactly | 2026-07-25 |
| `S04-G07` | `G06` | append-only reporting active | `OPEN` | `S04-V43` pre-entry before first live action | — | test owner | ledger defines cleanup | 2026-07-25 |
| `S04-G08` | product/E2E correctness | correctness-before-performance approval | `OPEN` | `V02`–`V35`, `V45`–`V46` direct pass before `B02` | — | verification owner | all prior runs clean | 2026-07-25 |
| `S04-I01` | `G04`,`G05` | materialization key/coordinator | `OPEN` | `V05`–`V12` | — | LayerStack owner | product tests clean | 2026-07-25 |
| `S04-I02` | `I01` | native capability/writer backend | `OPEN` | `V05`–`V10`,`V31` | — | LayerStack/backend owner | exact private paths | 2026-07-25 |
| `S04-I03` | `I01`,`I02` | generation manifest/current/lease | `OPEN` | `V13`–`V18` | — | LayerStack owner | grace/final recheck | 2026-07-25 |
| `S04-I04` | `I01`–`I03` | durable operations/recovery/failpoints | `OPEN` | `V19`–`V24` | — | LayerStack owner | residue bounded/reaped | 2026-07-25 |
| `S04-I05` | `I01`–`I04` | candidate module integration | `OPEN` | `CMD-P01`,`P02`,`P03` | — | LayerStack owner | no runtime | 2026-07-25 |
| `S04-I06` | `I03`–`I05` | private service APIs/models | `OPEN` | `V03`,`V13`,`V25` | — | LayerStack service owner | service resources 0 | 2026-07-25 |
| `S04-I07` | `I01`–`I06` | route/resource observations | `OPEN` | `V27`–`V30` | — | observability owner | counters settled | 2026-07-25 |
| `S04-I08` | `I06`,`I07` | strict private config/daemon wiring | `OPEN` | `V03`,`V25`,`V32` | — | config/daemon owner | gateways exact | 2026-07-25 |
| `S04-I09` | `I03`,`I06`,`I08` | strict session admission/rollback | `OPEN` | `V15`–`V18`,`V22`–`V28` | — | operation owner | reverse rollback | 2026-07-25 |
| `S04-I10` | `I09` | exact workspace lease/persistence/lifecycle | `OPEN` | `V15`–`V18`,`V23`,`V28` | — | WorkspaceManager owner | session exact | 2026-07-25 |
| `S04-I11` | `I09`,`I10` | native mount and `/eos` masking | `OPEN` | `V25`,`V26`,`V31` | — | namespace/overlay owner | strict unmount | 2026-07-25 |
| `S04-I12` | `I09`–`I11` | command/file/PTY warm-route integration | `OPEN` | `V25`–`V28` | — | operation/execution owner | executions drained | 2026-07-25 |
| `S04-I13` | `I01`–`I07` | product materialization tests | `OPEN` | `CMD-P03`; `V05`–`V24`,`V29` | — | product test owner | tempdirs exact | 2026-07-25 |
| `S04-I14` | `I08`–`I12` | strict workspace tests | `OPEN` | `CMD-P04`; `V15`–`V30` | — | product test owner | sessions/mounts 0 | 2026-07-25 |
| `S04-I15` | `I01`–`I14` | inherited contract/regression tests | `OPEN` | `V02`–`V04`,`V46` | — | product test owner | exact test cleanup | 2026-07-25 |
| `S04-I16` | `I13`–`I15`,`I18` | typed Stage 04 E2E module | `OPEN` | `V01`,`V05`–`V32`,`V45` | — | E2E owner | `R01`–`R08` | 2026-07-25 |
| `S04-I17` | `I16`,`I20` | E2E evidence/accounting helpers | `OPEN` | `V01`,`V27`,`V35`,`V45` | — | E2E owner | helper owns nothing | 2026-07-25 |
| `S04-I18` | `G04` | deterministic materialization fixture | `OPEN` | `V05`–`V10`,`V34` | — | fixture owner | generated run copies exact | 2026-07-25 |
| `S04-I19` | `I16` | catalog declarations/export | `OPEN` | `V01`,`V32` | — | catalog owner | no runtime | 2026-07-25 |
| `S04-I20` | specification | strict evidence schema | `OPEN` | `V34`,`V35` | — | schema owner | no runtime | 2026-07-25 |
| `S04-I21` | `I17`,`I20`,`I24` | runner-owned campaign adapter | `OPEN` | `V36`–`V42` | — | benchmark owner | `R01`–`R08` | 2026-07-25 |
| `S04-I22` | `I21` | planning/runner/catalog dispatch | `OPEN` | `V34`,`V36` | — | benchmark owner | topology exact | 2026-07-25 |
| `S04-I23` | `I21`,`I22` | frozen Stage 04 preset | `OPEN` | `V34`,`V36` | — | benchmark owner | no validation resources | 2026-07-25 |
| `S04-I24` | `I20` | golden artifact/threshold contract | `OPEN` | `V34`,`V35` | — | benchmark schema owner | no runtime | 2026-07-25 |
| `S04-I25` | `I20`–`I24` | unit/planning/runner/verifier tests | `OPEN` | `CMD-A01`; `V34`,`V35` | — | benchmark test owner | temp fixtures removed | 2026-07-25 |
| `S04-I26` | `G07` | append-only report entries | `OPEN` | `V43` for every live command | — | executing owner | per-entry exact | 2026-07-25 |
| `S04-I27` | all completion rows | benchmark note and Stage 05 handoff | `OPEN` | `V44`,`V47` | — | documentation owner | cleanup digest cited | 2026-07-25 |
| `S04-E01`–`S04-E12` | `I16`–`I20` | complete typed E2E families | `NOT_RUN` | `V05`–`V32`,`V45` via `CMD-E03` | — | E2E owner | `R01`–`R08` | 2026-07-25 |
| `S04-L01`–`S04-L13` | `I03`,`I09`–`I11`,`I16` | complete `/eos` lifecycle proof | `NOT_RUN` | `V13`–`V18`,`V26`,`V45` | — | storage/E2E owner | `L11`–`L13` | 2026-07-25 |
| `S04-R01`–`S04-R08` | all runtime work | ownership/resource/quiescence proof | `NOT_RUN` | `V12`,`V17`–`V30`,`V36`,`V42`,`V45` | — | run owner | required result is exact | 2026-07-25 |
| `S04-D01` | product complete | dependency/portability audit | `OPEN` | `V33`; `CMD-D01` plus retained comparator | — | dependency audit owner | no runtime | 2026-07-25 |
| `S04-A01` | `I20`,`I24` | complete strict artifact | `OPEN` | `V34`,`V36`–`V42` | — | artifact owner | ledger embedded | 2026-07-25 |
| `S04-A02` | `A01` | strict verifier/negative tests | `OPEN` | `V35`; `CMD-A01` | — | verifier owner | temp files exact | 2026-07-25 |
| `S04-A03` | `G07`,`I26` | append-only reporting | `OPEN` | `V43` | — | run owner | every post-entry complete | 2026-07-25 |
| `S04-B01` | `G08`,`A01`,`A02` | validated 180-second plan | `NOT_RUN` | `V34`,`V36`; `CMD-B01` then `CMD-B02` | — | benchmark owner | exact run ledger | 2026-07-25 |
| `S04-B02` | `B01` | time/space/resource campaign evidence | `NOT_RUN` | `V36`–`V42` | — | benchmark owner | complete before 180s | 2026-07-25 |
| `S04-B03` | `B02` | honest performance disposition | `NOT_RUN` | each gate direct; insufficient stays insufficient | — | verification owner | durable cleanup required | 2026-07-25 |
| `S04-H01` | all Stage 04 correctness | final v1 authority compatibility | `NOT_RUN` | `V03`,`V04`,`V46` | — | product/E2E owner | no candidate leak | 2026-07-25 |
| `S04-H02` | `H01`,`B03`,`D01` | final artifacts/digests/tracker closure | `OPEN` | `V43`,`V44` and mapping audit | — | verification owner | all cleanup linked | 2026-07-25 |
| `S04-H03` | `H02` | outgoing Stage 05 handoff | `OPEN` | `V47` and template §17 | — | documentation owner | cleanup digest included | 2026-07-25 |
| `S04-H04` | `H03` | docs links/diff validation | `OPEN` | `CMD-H01`, link/mapping/scope checks | — | documentation owner | no runtime | 2026-07-25 |
| `S04-Q07` | Stage 07 | release qualification and retirement | `DEFERRED_STAGE_07` | only Stage 07 may change after its entry gates | — | Stage 07 owner | Stage 07-owned | 2026-07-25 |

### 14.3 Evidence-backed completion checklist

Every item is initially unchecked. The artifact/command column names the minimum
direct evidence; runtime items additionally require the listed cleanup. Checking an
item requires all mapped progress and verification rows to satisfy §14.1. Brace and
`*` notation below describes the required artifact set compactly; the completed
tracker must expand it to every concrete path and SHA-256. An unresolved pattern is
not completion evidence.

| Checklist item | Canonical progress row(s) | Verification ID(s) | Exact retained artifact or command result | Cleanup evidence |
| --- | --- | --- | --- | --- |
| [ ] Custody and inherited Stage 03 compatibility reconciled | `S04-G01`–`S04-G04`,`S04-I15` | `S04-V02`–`S04-V04`,`S04-V43` | `$S04_E2E_EVIDENCE/{custody-pre.json,identities.json,commands/CMD-G02.json,commands/CMD-P05.json}` with digests | no unowned mutation; exact test cleanup |
| [ ] Exact reconstruction and capability failure | `S04-I01`–`S04-I05`,`S04-I13`,`S04-I18`,`S04-E01`,`S04-E02` | `S04-V05`–`S04-V10` | `$S04_E2E_EVIDENCE/{commands/CMD-P03.json,commands/CMD-E03.json,cases/E01-*,cases/E02-*}` | private build/session residue reconciled |
| [ ] Typed catalog and honest platform/capability matrix | `S04-G06`,`S04-I16`,`S04-I17`,`S04-I19`,`S04-E12` | `S04-V01`,`S04-V31`,`S04-V32` | `$S04_E2E_EVIDENCE/{commands/CMD-E01.json,commands/CMD-E02.json,commands/CMD-E03.json,cases/E12-*}` | exact per-cell resources cleaned; unrun cells remain `NOT_RUN` |
| [ ] Reuse and same-key single-flight | `S04-I01`,`S04-I03`,`S04-I04`,`S04-E03` | `S04-V11`,`S04-V12` | `$S04_E2E_EVIDENCE/{commands/CMD-P03.json,commands/CMD-E03.json,cases/E03-*}` | waiters/tasks/permits/residue zero/bounded |
| [ ] Strict no-fallback routing | `S04-I06`,`S04-I08`–`S04-I12`,`S04-E04` | `S04-V03`,`S04-V25`,`S04-V26` | `$S04_E2E_EVIDENCE/{commands/CMD-P04.json,commands/CMD-E03.json,cases/E04-*}` and route snapshots | session/mount/lease teardown |
| [ ] Warm zero-forbidden-work counters | `S04-I07`,`S04-I12`,`S04-E04` | `S04-V27` | `$S04_E2E_EVIDENCE/cases/E04-*/native-route-before-after.json` | counters/resources settled |
| [ ] `CURRENT` atomicity and exact generation leases | `S04-I03`,`S04-I04`,`S04-I09`,`S04-L03`–`S04-L06` | `S04-V13`–`S04-V16`,`S04-V19`–`S04-V23` | `$S04_E2E_EVIDENCE/{cases/E05-*,cases/E06-*,cases/E07-*}` plus `commands/CMD-E03.json` | old/new exact leases released in order |
| [ ] Concurrency, isolation, quotas, and backpressure | `S04-I01`,`S04-I07`,`S04-I09`–`S04-I14`,`S04-E03`,`S04-E07`,`S04-E09` | `S04-V12`,`S04-V17`,`S04-V28`,`S04-V29` | `$S04_E2E_EVIDENCE/{cases/E03-*,cases/E07-*,cases/E09-*}/resources.json` | every owned gauge/path returns to baseline |
| [ ] All recovery boundaries | `S04-I04`,`S04-I09`,`S04-I10`,`S04-E05`,`S04-E06`,`S04-E08` | `S04-V19`–`S04-V24` | `$S04_E2E_EVIDENCE/{cases/E05-*,cases/E06-*,cases/E08-*}` with one boundary record per failpoint | exact recovery/reap ledger |
| [ ] Complete `/eos` lifecycle and workload mask | `S04-G05`,`S04-I03`,`S04-I09`–`S04-I11`,`S04-E11`,`S04-L01`–`S04-L13` | `S04-V13`–`S04-V18`,`S04-V26`,`S04-V45` | `$S04_E2E_EVIDENCE/cases/E11-*/{tree.json,mountinfo.txt,space.json}` | `S04-L11`–`S04-L13`,`S04-R03`–`S04-R07` |
| [ ] Inactive versus active MCTS allocation | `S04-E10` | `S04-V30` | `$S04_E2E_EVIDENCE/cases/E10-*/{refs.json,space.json,resources.json}` | active sessions retired; refs intentional |
| [ ] 180-second time/space/resource campaign | `S04-G08`,`S04-I21`–`S04-I23`,`S04-B01`–`S04-B03`,`S04-A01`,`S04-A02`,`S04-R01`–`S04-R08` | `S04-V36`–`S04-V42` | `$S04_ARTIFACT_ROOT/stage04/{stage04-materialization-evidence-v1.json,verdict.json,sha256sums.json}` and `CMD-B02` result | `$S04_ARTIFACT_ROOT/stage04/cleanup/ledger.json` durable by 180s |
| [ ] Dependency and portable-core boundary audit | `S04-D01` | `S04-V33` | `$S04_TEST/.e2e-state/tmp/$S04_RUN_ID/dependency-delta-{a,b}.json` plus `$S04_E2E_EVIDENCE/dependency/boundary-audit.json` and digests | no runtime resources |
| [ ] Artifact/verifier negative tests | `S04-I20`,`S04-I24`,`S04-I25`,`S04-A01`,`S04-A02` | `S04-V34`,`S04-V35` | `$S04_E2E_EVIDENCE/{commands/CMD-A01.json,commands/CMD-B01.json,artifact-negative-cases.json}` and golden digest | test temp artifacts removed |
| [ ] Append-only E2E reporting | `S04-G07`,`S04-I26`,`S04-A03` | `S04-V43` | exact pre/post entries in `e2e/test-report.md`, report SHA-256, and `$S04_E2E_EVIDENCE/report-entry-index.json` | each entry records exact cleanup |
| [ ] Final v1 authority regression | `S04-G03`,`S04-I15`,`S04-H01` | `S04-V03`,`S04-V04`,`S04-V46` | `$S04_E2E_EVIDENCE/{commands/CMD-P05.json,commands/CMD-E03.json,final-v1-authority.json}` | no candidate/public leak |
| [ ] Cleanup and quiescence | `S04-R01`–`S04-R08`,`S04-L09`–`S04-L13` | `S04-V12`,`S04-V17`–`S04-V30`,`S04-V36`,`S04-V42`,`S04-V45` | `$S04_E2E_EVIDENCE/quiescence-final.json` and `$S04_ARTIFACT_ROOT/stage04/{samples/resources.ndjson,samples/space.ndjson,cleanup/ledger.json}` | exact zero run-owned/unexplained result |
| [ ] Outgoing Stage 05 handoff | `S04-I27`,`S04-H02`–`S04-H04` | `S04-V44`,`S04-V47` | `handoff_to_stage_05.md`, `benchmark_note.md`, `$S04_E2E_EVIDENCE/commands/CMD-H01.json`, and all SHA-256 values | cleanup digest and retained state named |
| [ ] Stage 07 deferrals remain explicit | `S04-Q07`,`S04-H03`,`S04-H04` | `S04-V32`,`S04-V44`,`S04-V47` | `handoff_to_stage_05.md` Stage 07 table plus `$S04_E2E_EVIDENCE/stage07-deferral-audit.json` | no Stage 07 resource created |

## 15. Current blockers and stop conditions

At guide authoring time:

- no direct Stage 04 implementation, E2E, benchmark, portability, or qualification
  evidence exists, so all corresponding work remains open/not run;
- the stale implementation-index statement that v3 is unapproved contradicts the
  higher-authority approved decision as described in §1.3; the hierarchy resolves it
  for planning, but identity/approval must be rechecked at entry;
- the host contains unrelated live gateways/listeners and exited containers, so
  global-zero cleanup claims are invalid; exact baseline and ownership-relative
  quiescence are mandatory;
- the incoming/outgoing handoff pair itself agrees. A future mismatch is a hard
  `S04-G02` blocker.

Stop immediately if any of these occurs:

- authority, v2/v3 golden, bounds, or `RootId` drift;
- a strict error reaches legacy v1 or a warm request materializes;
- no exact durable lease can be acquired before mount or retained through unmount;
- a carrier/manifest/selector can become visible out of order;
- a capability failure occurs after session/workspace mutation;
- an owner cannot safely classify a path, task, process, permit, FD, mapping, mount,
  or container;
- allocated space or unavailable measurements cannot be accounted honestly;
- the full correctness/failpoint matrix has a failure;
- the campaign misses 150/180/60-second boundaries;
- cleanup would touch a shared/unowned/v1/service/runtime path; or
- a Stage 05–07 feature becomes necessary. Escalate the scope/authority decision
  instead of implementing it implicitly.

## 16. `S04-Q07`: explicit Stage 07 deferrals

The following remain `DEFERRED_STAGE_07`, even if a Stage 04 POC cell succeeds:

- release-wide Linux distribution/kernel/Docker/VM/backing-filesystem qualification;
- universal amd64/arm64, glibc/musl, shell-less, minimal/distroless, read-only, and
  non-root support claims;
- any percentage of supported images or environments;
- long-duration soak, fleet/multi-host behavior, upgrade/rollback/recovery campaigns,
  and destructive retention survival;
- statistical performance qualification beyond the direct sample set;
- authority cutover, v1 retirement/deletion, rollback authority, destructive
  retirement, and final evidence sign-off;
- full Stage 05 pack/locator/GC/squash behavior under production retention.

Stage 04 may record a direct per-cell result without generalizing it. `NOT_RUN`,
unsupported, or insufficient cells remain visible in artifacts, the tracker,
benchmark note, and outgoing handoff.

## 17. Outgoing Stage 05 handoff template

Create `handoff_to_stage_05.md` only after all non-deferred Stage 04 checklist items
are complete:

```markdown
# Stage 04 handoff to Stage 05

Verdict: <POC PASS or BLOCKED/FAIL — never release-qualified>
Closed at: <UTC>

## Authority and frozen identities
- owner decision/corpus/v2/v3 digests:
- public read/write authority: legacy_v1
- product/test/docs commits, upstreams, source-diff digests:
- exact Stage 04 manifest/key/backend schema versions:

## Handoff reconciliation
- outgoing Stage 03 digest:
- incoming Stage 04 digest:
- contradictions and resolutions:

## Implemented Stage 04 slice
- materialization key/backend/capabilities:
- manifest/CURRENT/fence/lease:
- strict routes:
- resource and ownership limits:
- explicitly unchanged public/v1 behavior:

## Verification
- product command results/artifacts:
- typed E2E catalog and full correctness/failpoint result:
- /eos lifecycle result:
- dependency/portable-core audit:
- platform cells, including NOT_RUN/unsupported:

## Focused benchmark
- run ID, exact command, artifact root/digests:
- 180/150/60 boundaries:
- raw sample counts and sufficiency:
- time gates:
- all ten allocated-space samples and reconciliation:
- resource caps:
- POC-only limitation:

## Cleanup and custody
- ownership/cleanup ledger path/digest:
- retained immutable generations/evidence:
- pre-existing excluded processes/listeners/containers:
- final run-owned quiescence and unexplained residue:

## Open defects/blockers
- <none or exact item>

## Stage 05 inputs and boundaries
- immutable generation/lease facts Stage 05 may consume:
- no Stage 05 pack/locator/GC/squash code was implemented in Stage 04:
- deletion still requires exact lease/pin/current/grace/final checks:

## Stage 07 deferrals
- all items from S04-Q07, with direct cell statuses unchanged
```

The handoff may say Stage 04 POC `PASS` only if every non-deferred checklist mapping
has direct verified evidence and exact cleanup. It must not say release-qualified.

## 18. Copy-ready prompt for the future Stage 04 implementation agent

```text
Implement and verify Stage 04, candidate materialization and strict native
activation, using:

/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_candidate_materialization/implementation_instructions.md

Proceed autonomously from entry reconciliation through implementation, correctness,
recovery, benchmark evidence, cleanup, documentation, and outgoing handoff. Do not
pause for confirmation, wait for optional approval, ask preference questions, or
stop merely because one slice passes while safe in-scope work remains. Make the most
conservative guide-compliant choice, continue to the next ordered action, diagnose
and fix failures, rerun the exact affected gates, and finish every non-deferred
Stage 04 completion row.

Stop and ask for direction only for an actual blocker that prevents completing the
Stage 04 specification safely: an irreconcilable authority/handoff/frozen-identity
contradiction; shared-custody collision with no non-mutating workaround; missing
required credential, permission, host capability, or external service; a required
owner decision between incompatible contracts; or inability to preserve unrelated
data/resources while proceeding. First exhaust safe read-only checks and in-scope
alternatives, then report the exact evidence, affected work/verification IDs, and
smallest decision or external change needed. An optional or unsupported environment
cell is not by itself a blocker: record it `NOT_RUN` with its truthful disposition
and continue all other work.

Read that guide and every ledgered authority source from line 1 through EOF before
mutation. Recompute source hashes and re-inventory product, test, docs, ignored
runtime state, processes/listeners, containers, filesystems, and benchmark roots.
Preserve shared custody. Do not reset, stash, clean, restore, switch branches, or
broadly delete. Stop on any incoming/outgoing handoff or frozen-identity mismatch.

Implement only the ordered S04-I slices on the real seams. Keep public read/write
authority legacy_v1. Preserve frozen v2/v3 bytes, typed domains, bounds, and RootId.
Physical materialization inputs never enter logical identity. Cold reconstruction is
explicit; command/file/PTY/workspace/warm requests may only use a preverified native
generation and may never fall back to v1. Acquire one durable exact
{materialization-id,generation,fence} lease before mount. CURRENT/head changes affect
later admissions only. Share immutable carriers only; keep upper/work/execution/mount
namespace private.

Use the complete /eos ownership table and lifecycle assertions. Never create
/eos/legacy, refs/legacy, global /eos/namespace_execution, benchmark-only durable
layouts, or Stage 05–07 directories. LayerStack cleanup must not touch
WorkspaceManager, service-storage, daemon-runtime, v1 compatibility, unrelated
resources, or retained evidence.

Add the typed E2E, fixtures, schema, strict verifier, and runner-owned benchmark by
extending the Stage 03 architecture. Append a complete pre-entry and post-entry to
e2e/test-report.md around every live test, diagnostic, and benchmark. Run the full
correctness/failpoint matrix separately before performance. Then, if all correctness
gates pass, run the single monotonic 180-second campaign: stop admission at 150
seconds, reserve the final 30 seconds for artifacts/verifier/cleanup/quiescence, and
fail if the durable cleanup ledger is incomplete at 180 seconds. No operation may
exceed 60 seconds. Retries consume the same clock. Safety cleanup cannot repair the
verdict.

Retain raw counterbalanced samples. Inferential p95 needs at least 20 valid samples
per compared arm/cell; otherwise record INSUFFICIENT_SAMPLE. Measure allocated
physical space at all ten boundaries, reconcile
T = L_hot + H_cold + sum(U_active) + P_staging + M, and never coerce missing or
unsupported data to zero. Enforce the 256 KiB buffer, four-worker, byte-permit,
backpressure, RSS, ownership, cleanup, and zero-unexplained-residue gates.

Update the canonical tracker and checklist only from exact artifacts and digests.
Keep unexecuted platform cells `NOT_RUN` with an explicit `unverified` evidence
disposition and all `S04-Q07` work `DEFERRED_STAGE_07`. Finish with final v1
regression, dependency/portable-core audit,
link/mapping/diff validation, benchmark note, and the outgoing Stage 05 handoff.
Do not claim Stage 04 PASS, portability, benchmark success, or qualification unless
the guide's direct evidence and cleanup conditions are all met. If no actual blocker
exists, do not yield early: continue until the guide's Stage 04 outcome is genuinely
complete.
```

## 19. Final document-validation procedure

Before using or closing this guide:

1. Resolve every Markdown link from this file and require an existing target.
2. Search for `S03-`, `Stage 03`, `stage03`, and copied `S04` IDs. Stage 03 may appear
   only as inherited/history/seam evidence, never as a Stage 04 result.
3. Parse every checklist row and require at least one canonical progress row, one
   verification ID, one exact artifact/command result, and cleanup evidence for
   runtime work.
4. Require every progress verification reference to exist in §13 and every
   verification requirement to map to an E2E/product/artifact/doc case.
5. Sum benchmark windows: `12 + 35 + 30 + 25 + 20 + 15 + 13 + 30 = 180`.
   Require admission stop `150` and cleanup reservation `30`.
6. Cross-check every Stage 04 E2E-plan requirement against `S04-E01`–`E12` and
   `S04-V05`–`V45`, including every build/sync/manifest/`CURRENT`/admission/unmount/
   response-loss failpoint.
7. Compare the complete `/eos` normative tree and table; require ownership exclusions,
   forbidden paths, v1 compatibility, and `S04-L01`–`L13`.
8. Search Stage 05–07 terms and require each to be a non-goal, boundary, outgoing
   input, or `S04-Q07` deferral—not implemented Stage 04 scope.
9. Confirm all current Stage 04 execution cells remain `NOT_RUN` and no prose claims a
   Stage 04 implementation, E2E, benchmark, portability, or qualification pass.
10. Run `git diff --check` in the documentation repository and inspect the diff to
    confirm only this target was edited by this task.
