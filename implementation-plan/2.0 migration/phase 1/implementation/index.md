# LayerStack Phase 1 implementation plan

Status: Stage 02 portable-root v2 codec, fixture, and source contract **POC PASS**. Later-stage architecture work remains separate and does not affect this Stage 02 verdict.

Phase 1 uses **five contiguous implementation stages after Stage 02**, not nine.
The merged stage directories are removed; the active sequence is Stage 03 through
Stage 07.

The normative storage and failure contract is
[LayerStack Phase 1 minimal storage contract](layerstack_storage_contract.md).
Preparation 04 remains the normative performance, space, memory, and environment gate:
[SeqCDC space/time complexity and acceptance criteria](../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md).

## 1. Architectural conclusion

The prior simplified design was still over-engineered. The durable core is:

1. bounded-page immutable Merkle objects;
2. small atomic refs;
3. one recoverable operation protocol;
4. immutable native generations selected by one pointer;
5. optional immutable locator runs selected by one pointer;
6. disk-backed tracing GC with a ref-creation barrier;
7. one authority fence plus temporary common-operation migration proof.

Separate root files, receipt and control families, lock directories, per-operation
journal types, separate squash state, permanent quarantine/trash, and Stage 04 shadow
storage are deleted. Values that follow from typed IDs, refs, or immutable manifests
are derived.

This redesign stays close to the Stage 00–02 `/eos` model: one LayerStack-owned
directory with ordinary files/directories and atomic replacement. Candidate state is
added only when a concrete capability needs it. Existing v1 paths remain
rollback-capable until retirement; no new `legacy/` directory or legacy ref class is
created.

### Complete `/eos` structure

The normative fields, lifecycle, and justification are in
[§4 of the storage contract](layerstack_storage_contract.md#4-complete-eos-ownership-and-storage-tree).
The complete migration-time ownership tree is shown here as an implementation
orientation map:

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
│   │   └── work/...
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
│       └── executions/<execution-id>/
│           └── transcript.log
├── storage/
│   ├── file_auditability/...
│   └── workspace_recovery/...
└── runtime/
    └── daemon/
        ├── runtime.sock
        └── runtime.pid
```

The v1 entries directly under `layer-stack/` exist only during the rollback window;
Stage 07 removes exact evacuated targets after approval. Optional 2.0 directories are
created only on first use. The target tree has no global
`/eos/namespace_execution`; `/workspace` is a per-session mount, not a durable `/eos`
path. LayerStack GC never owns `/eos/workspace`, `/eos/storage`, or `/eos/runtime`.

## 2. Blocking prerequisite

Stage 02 freezes a flat `TreeManifestId` as the SHA-256 of the complete canonical tree
stream (`stage_02_portable_root_contract/spec.md:314-324` and
`stage_02_portable_root_contract/contract_v2_owner_decision_d2_5.md:257-263`).
That cannot satisfy later-publication proportionality because a middle edit requires
rehashing the complete stream. Streaming at Stage 02 `spec.md:366` bounds memory, not
work.

Before Stage 03 implementation, an owner amendment must:

- preserve v2 fixture bytes/IDs as immutable and readable;
- define `RootRecordV3` over a typed bounded-page Merkle `TreeNodeId`;
- freeze exact directory, file, segment-page, and chunk codecs;
- treat flat manifests as derived export/validation only;
- permit one `O(R+E)` v1/v2→v3 import with a new v3 `RootId`.

If identical v2 and v3 `RootId` values are required, the requirements are inconsistent
and implementation must not start. Stage 02 writes no candidate state
(`stage_02_portable_root_contract/spec.md:89-97,183-188,386`), so this is the cheapest
safe point to correct the format.

## 3. Requirements trace

| Required capability | Mechanism | Delivered / proved |
| --- | --- | --- |
| portable immutable `RootId` | typed v3 root and bounded Merkle objects | Stage 03 / Stage 07 |
| incremental publication | changed-path capture, persistent-page rewrite, shared objects | Stage 03 / Stage 07 |
| branch heads and OCC | atomic head `{root,generation,publication}` and changed-path three-way compare | Stage 03 / Stage 07 |
| automatic recovery/idempotency | publication-keyed common operation plus head commit witness | Stage 03 / Stage 07 |
| named checkpoint, clean fork | one root ref/head; no payload copy | Stage 03 / Stage 07 |
| dirty checkpoint | ordinary publication then one checkpoint ref | Stage 03 / Stage 07 |
| checkout/revert/reset | session selection / new publication / head move | Stage 03 / Stage 07 |
| warm native execution | preverified materialization `CURRENT`; native-only route | Stage 04 / Stage 07 |
| cold reconstruction/on-demand materialization | bounded streamed generation build | Stage 04 / Stage 07 |
| bounded MCTS native depth | inactive refs only; active private uppers; materialization flattening | Stage 04 / Phase 2 suites |
| compaction without identity change | pack/locator pointer replacement | Stage 05 / Stage 07 |
| checkpoint survival across squash | squash is materialization generation replacement | Stage 05 / Stage 07 |
| concurrent GC safety | disk mark runs, root barrier, grace, final recheck | Stage 05 / Stage 07 |
| migration and authority rollback | one authority state; verified on-demand reverse materialization | Stage 06 / Stage 07 |
| Phase 3 backend portability | provider-neutral objects/refs; physical adapters only | contract / provider contract suites |
| environment/dependency constraints | safe internal Rust and existing mandatory dependencies only | every stage / Stage 07 matrix |

## 4. Reduced stage plan

### Stage 03 — corrected identity and complete private publication

Documents:

- [spec](stage_03_incremental_publication/spec.md)
- [E2E plan](stage_03_incremental_publication/e2e_test.md)
- [benchmark note](stage_03_incremental_publication/benchmark_note.md)
- [Stage 02→03 implementation handoff](stage_03_incremental_publication/handoff_from_stage_02.md)

This is a vertical slice, not an algorithm-only experiment. It includes:

- the owner-approved v3 codecs and bounded Merkle pages;
- streaming SeqCDC and deterministic typed chunks;
- changed-path incremental tree updates;
- loose immutable object installation;
- common operation recovery/idempotency;
- private branch heads, checkpoints, pins, clean/dirty checkpoint;
- checkout, revert, reset, clean branch/MCTS fork;
- same-path/ancestor conflict rules and disjoint OCC rebase;
- source protection for any imported v1 carrier;
- optional hidden candidate-vs-v1 comparison using the final protocol.

Exit requires durable crash/failpoint evidence and changed-input scaling. No public read
or write route changes.

### Stage 04 — materialization and strict native activation

Documents:

- [spec](stage_04_candidate_materialization/spec.md)
- [E2E plan](stage_04_candidate_materialization/e2e_test.md)
- [benchmark note](stage_04_candidate_materialization/benchmark_note.md)

This stage adds on-demand cold materialization, immutable native generations, exact
session leases, same-key single-flight builds, one `CURRENT` pointer, bounded mount
depth, per-session private uppers, and an explicit no-fallback candidate activation
mode. Multiple sessions may share one read-only generation; a head or `CURRENT`
change never mutates an admitted session. Strict routing is an exit gate in this
stage, not another stage.

### Stage 05 — retention, physical compaction, GC, and squash

Documents:

- [spec](stage_05_retention_gc_packs/spec.md)
- [E2E plan](stage_05_retention_gc_packs/e2e_test.md)
- [benchmark note](stage_05_retention_gc_packs/benchmark_note.md)

This stage adds pack/locator maintenance, disk-backed tracing GC, the ref-creation
barrier, grace/final recheck, policy retention, and identity-preserving squash through
the existing materialization-generation switch.

### Stage 06 — reversible candidate authority

Documents:

- [spec](stage_06_candidate_authority/spec.md)
- [E2E plan](stage_06_candidate_authority/e2e_test.md)
- [benchmark note](stage_06_candidate_authority/benchmark_note.md)

Candidate authority is enabled only after verified catch-up. Authority rollback is
real write-and-read rollback: quiesce/fence publications, materialize and verify the
selected candidate root into private v1 staging, atomically publish v1, switch the one
authority state, and resume v1 writes. A continuous legacy-shadow architecture is not
required.

### Stage 07 — qualification, default, and retirement

Documents:

- [spec](stage_07_qualification_retirement/spec.md)
- [E2E plan](stage_07_qualification_retirement/e2e_test.md)
- [benchmark note](stage_07_qualification_retirement/benchmark_note.md)

Stage 07 adds no storage mechanism. It runs the complete crash, concurrency,
performance, space, memory, image, architecture, rollback, and long-soak matrices.
Candidate default occurs only after opt-in qualification passes. Legacy retirement is
a separate destructive approval after rollback rehearsal and evacuation proof.

## 5. Old-stage-to-new-stage mapping

| Old stage | New disposition | Why |
| --- | --- | --- |
| 03 streaming SeqCDC | expanded into active Stage 03 | Chunking alone does not prove publication architecture. |
| 04 shadow CAS ingest | **merged into new Stage 03** as optional validation mode | A “durable” root cannot rely on unprotected v1 carriers, and shadow-specific state would be removed soon afterward. |
| 05 candidate materialization | **renumbered new Stage 04** | Native generations are a real independent risk boundary. |
| 06 strict candidate activation | **merged into new Stage 04** as its exit gate | Strict routing adds no persisted representation. |
| 07 durable publication | **merged into Stage 03** | The first durable root already needs recovery, refs, source protection, and idempotency. |
| 08 retention/GC/packs | **renumbered new Stage 05** | Physical deletion and concurrent reachability are a distinct high-risk boundary. |
| 09 identity-preserving squash | **merged into new Stage 05** | Squash is the same verified-generation build and pointer switch as materialization. |
| 10 candidate authority | **renumbered redesigned Stage 06** | Public authority and reversible migration are a distinct rollout risk. |
| 11 qualification/retirement | **renumbered Stage 07 gate** | Qualification and destructive retirement must remain separately approved. |

Thus there are five active stages: **03, 04, 05, 06, and 07**. There are no mapping
stubs or reserved empty stage directories.

## 6. Former Stage 04 “shadow” decision

“Shadow” previously mixed three meanings:

1. candidate bytes persisted privately;
2. candidate results compared with v1;
3. a migration cursor that could eventually support authority.

Those are not one consistency domain. The old Stage 04 could declare a root durable
while its final payload location was a v1 carrier not protected by a durable source
hold, and it committed v1 before candidate recovery intent. It therefore offered
neither durable candidate recovery nor safe last-locator lifetime.

The former shadow-ingest stage is deleted. “Shadow” now means only an optional
validation mode in Stage 03: the normal final candidate publication protocol advances
a hidden validation head, durably protects any source locator, materializes it when
requested, and correlates the result with the v1 publication. V1 remains authority.
Comparison output is bounded telemetry/evidence, not another catalog, receipt, or
transaction schema.

Stage 06 migration does not reuse this word. It has explicit catch-up, parity,
authority, and rollback phases. `CONTROL` stores only the atomic authority fence;
detailed migration progress and proof remain in the common migration operation.

## 7. Stage-boundary risk argument

| Boundary | Measurable risk retired | Why it remains separate |
| --- | --- | --- |
| 02→03 | canonical identity and incremental/crash-safe logical publication | Format errors contaminate every later root. |
| 03→04 | logical correctness before native reconstruction/routing | A native bug must not obscure an object/ref bug. |
| 04→05 | verified reads before physical deletion/compaction | GC introduces irreversible risk. |
| 05→06 | private durability before public authority | Migration failure must not become public corruption. |
| 06→07 | reversible authority before default/retirement | Rollout evidence and irreversible removal need separate approval. |

The deleted boundaries retired no lasting risk: they created intermediate state
machines or storage formats that the next stage immediately replaced.

## 8. Delivery rules shared by every stage

- The canonical storage contract is not duplicated in a stage document.
- No product code is authorized by this documentation review.
- No stage creates an empty directory for a later stage.
- New logical storage/GC code is safe Rust; no detached tasks or strong ownership
  cycles; all queues, caches, workers, buffers, iterators, registries, FDs, mappings,
  leases, and retries are bounded.
- No all-live resident set or reference-count-only deletion.
- No SQLite, embedded database, sidecar, target-image helper, new dependency, shell,
  libc/coreutils helper, package manager, FUSE, reflink, tar, or `cp`.
- No host/environment value contributes to identity.
- Expensive work occurs outside brief mutable-pointer critical sections.
- Requirement prose is never recorded as a benchmark pass. Each note remains
  `NOT_RUN` until it contains reproducible commands, artifacts, exact environment,
  counters, result, and comparison with the Preparation 04 threshold.
- Each stage runs Markdown-link validation, stale-term search, and `git diff --check`.

## 9. Performance and space gates

Preparation 04 is preserved without relaxation:

- first import may be `O(R+E)`;
- later publication is proportional to changed input, changed entries/chunks, and
  touched persistent pages—not total tree or history;
- warm execution performs native I/O only and final mount depth is at most 64;
- clean branch/checkpoint stores no payload or complete native tree;
- historical roots structurally share unchanged bytes/pages;
- materializations exist only for active or explicitly pinned roots;
- cold reconstruction is streamed and bounded;
- metadata, operation residue, locator amplification, packs, duplicate bytes, mark
  runs, and trash overlap are measured;
- all Preparation 04 queue, worker, buffer, merge-fan-in, encoder, cache,
  per-publication, global semaphore, depth, RSS, and space limits remain normative.

The overall status is recorded in
[the Stage 03–07 benchmark scorecard](stage_03_07_benchmark_note.md). No architecture
review result changes `NOT_RUN` to `PASS`.

## 10. Phase 2/3 and environment audit

Phase 2 uses heads/checkpoints/pins over the same roots. Active MCTS forks allocate
private writable state; inactive nodes retain refs only. Merge/promotion must define
base/left/right roots, ancestor/descendant/rename/hardlink conflict keys, promotion
CAS, retry identity, and retention. Blame/transition metadata, if retained as a Phase
2 requirement, is a separate immutable publication transition and never a `RootId`
input.

Phase 3 logical providers supply typed immutable get/put-if-absent, atomic/fenced ref
update, bounded iteration, and physical locator lookup. Native materialization and
activation are separate OS/backend adapters. A provider or backend that cannot meet
atomic, fencing, metadata-preservation, or activation capabilities fails closed.
Provider URLs, credentials, paths, buckets/keys, inode/device data, and backend
compression never enter identity.

Phase 1 qualifies the Linux materializer plus OverlayFS/mount-namespace activator.
Docker Engine on Linux uses it directly; macOS/Windows hosts use the Linux VM backend,
not native host filesystem semantics. A Docker-managed Linux volume is preferred.
Bind-mounted, translated, remote, and other backing filesystems require explicit
qualification. The target-image matrix includes glibc, musl, minimal/distroless,
shell-less, read-only, non-root, amd64, and arm64. Where a target cannot execute a
shell, public workspace/file APIs supply verification. Compatibility is capability
based; no universal or “95% of images” claim is made. All cells remain open until
measured.

## 11. Unresolved gates

1. **Correctness:** the v3 Merkle identity amendment is unapproved.
2. **Correctness:** exact conflict-key semantics for ancestor/descendant, rename,
   opaque-directory, and hardlink mutations need frozen vectors.
3. **Correctness:** idempotency needs an API retention/ack contract. Outcomes are
   retained within a bounded advertised window; after expiry retry must return
   `OutcomeExpired`, never republish.
4. **Correctness:** ref creation, materialization activation, and authority switch must
   participate in the same GC barrier before visibility.
5. **Performance:** bounded-page fanout, write amplification, global metadata-lock
   contention, locator-run caps, and GC external-run costs are unmeasured.
6. **Space:** imported v1 payload needs a durable source hold until evacuation; no
   candidate root may be called durable before its last locator is protected.
7. **Performance/space:** same-key single-flight behavior, materialization disk quotas,
   and shared-generation/private-upper scaling are not measured.
8. **Portability:** the complete image/architecture/backend/backing-filesystem matrix
   is not run.

These are exit blockers, not reasons to add more storage families or stages.
