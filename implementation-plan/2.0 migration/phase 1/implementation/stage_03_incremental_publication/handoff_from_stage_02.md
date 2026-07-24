# Stage 02→03 documentation and implementation handoff

Status: architecture/specification handoff only. No Stage 03 product code has been
implemented.

Branch: `layerstack_2_0`. Keep Stage 03 specification and implementation work on the
2.0 migration branch; do not apply it directly to `main`.

Normative inputs:

- [implementation index](../index.md)
- [minimal storage contract](../layerstack_storage_contract.md)
- [Stage 03 specification](spec.md)
- [Stage 03 E2E plan](e2e_test.md)
- [Stage 03 benchmark note](benchmark_note.md)
- [Stage 02 portable-root contract](../stage_02_portable_root_contract/spec.md)
- [Preparation 04 gates](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

## 1. What the architecture review completed

The review reduced the former Stages 03–11 to five durable risk gates, Stages 03–07.
Old Stage 04 shadow ingest and old Stage 07 durable publication are part of this
complete Stage 03 vertical slice. The old stage directories are removed rather than
kept as mapping stubs.

The canonical contract now fixes:

- the complete `/eos` ownership tree and the boundary between LayerStack durable state,
  WorkspaceManager session scratch, other service storage, and daemon runtime files;
- bounded-page v3 Merkle identity as the only design compatible with changed-input
  publication;
- one small ref family, one sparse common operation format, one materialization
  generation pointer, and one optional locator-run pointer;
- no `refs/legacy`, legacy folder, receipt family, journal family, transaction family,
  shadow catalog, flat full-tree identity manifest, or reserved future directory;
- ordinary fenced locator/source leases for imported bytes that remain in existing v1
  carriers;
- branch-scoped `PublicationId` recovery, head commit witnessing, changed-path OCC,
  and GC barrier participation;
- clean checkpoint/branch/MCTS fork as one `RootId` ref with zero copied payload or
  native tree;
- distinct checkout, revert, reset, and later authority-rollback semantics;
- safe-Rust, bounded-memory/resource, dependency, and environment constraints.

All performance results remain `NOT_RUN`. Architecture review is not benchmark
evidence.

## 2. Blocking owner decision

Do not implement Stage 03 until the portable-root owner approves the v3 identity
amendment.

Stage 02's frozen v2 `TreeManifestId` hashes the complete canonical flat tree stream.
That remains immutable and readable, but a middle edit cannot update it without
rehashing the complete tree. Stage 03 therefore requires:

1. `RootRecordV3` containing a typed bounded-page `TreeNodeId`;
2. frozen canonical codecs and maximum encoded sizes for tree pages, file nodes,
   segment pages, chunks, symlink/special nodes, and required capability bits;
3. v2 read/import compatibility with a distinct v3 `RootId`;
4. a derived flat export/validation stream that is never a publication identity input.

If the owner requires v2 and v3 IDs to be identical, Stage 03 is blocked because that
requirement conflicts with later-publication proportionality.

## 3. Exact Stage 03 durable scope

Stage 03 may create only paths needed by a real private publication:

```text
/eos/layer-stack/
├── .storage-writer.lock
├── CONTROL
├── objects/
│   ├── loose/<kind>/<digest-prefix>/<typed-id>
│   └── locators/{<run-id>.sst,CURRENT}        only if imported bytes stay in v1
├── refs/
│   ├── heads/<branch-id>
│   ├── checkpoints/<checkpoint-id>            only when created
│   ├── pins/<pin-id>                          only when created
│   └── leases/<lease-id>                      only while protection is required
└── operations/<operation-id>/
    ├── STATE
    └── work/                                  only while recovery/retention requires it
```

Do not create `packs`, `materializations`, or `gc` for future stages. Do not move
existing v1 `manifest.json`, `workspace.json`, `base`, `layers`, `staging`, or
`.layer-metadata` into a new folder. Public v1 authority and paths remain unchanged in
Stage 03.

Workspace changed input comes from the admitted session's
`/eos/workspace/<session>/upper`. Never ingest OverlayFS `work`, execution transcripts,
other service-owned `/eos/storage`, or daemon `/eos/runtime` state.

## 4. Required implementation order

1. Freeze and test v3 canonical codecs and hostile decoder bounds.
2. Implement deterministic loose-object put-if-absent and typed verification.
3. Implement bounded changed-path capture/order and SeqCDC chunk installation.
4. Implement persistent-page mutation with structural sharing and derived flat export.
5. Implement atomic heads and ref primitives with GC-barrier hook points.
6. Implement the branch-scoped publication operation and crash-gap repair.
7. Implement changed-path OCC conflict keys and bounded disjoint rebase.
8. Add checkpoints, clean branch/MCTS fork, checkout, revert, and reset using the same
   primitives.
9. Add existing-v1 source locators/leases only if import does not evacuate payload to
   deterministic loose objects.
10. Add optional hidden validation by invoking the normal publication path; add no
    shadow-specific state.

Expensive capture, hashing, sorting, and page construction occur outside the brief
writer-lock commit section.

## 5. Recovery and ownership checklist

- A visible head names only a fully durable verified graph.
- `head.publication_id` repairs a crash after head rename and before terminal `STATE`.
- Same scoped ID plus different request digest is `IdempotencyMismatch`.
- Expired/acknowledged outcomes return `OutcomeExpired`; they never republish.
- Terminal operation state/work is bounded and later released to GC.
- No operation task is detached; cancellation/shutdown joins all owned tasks.
- Registries, changed-path runs, buffers, queues, workers, FDs, mappings, retry loops,
  and terminal outcomes have declared caps.
- No full file/tree/history/all-live collection and no reference-count deletion
  authority exists.
- Imported payload is not called durable until its last locator is independently
  durable or protected by an ordinary fenced lease.
- LayerStack never deletes WorkspaceManager-owned session trees.

## 6. Evidence required before Stage 04

Run the Stage 03 E2E and benchmark documents exactly. The release evidence must include:

- immutable v2 and new v3 golden vectors on amd64 and arm64;
- changed-path read/write counters proving no total-tree/history pass;
- exact crash/failpoint outcomes and lost-response retries;
- same-path/ancestor/rename/opaque/hardlink conflicts and disjoint progress;
- clean checkpoint/fork zero-payload/native-tree allocation;
- bounded RSS/tasks/workers/queues/FDs/mappings/operation residue;
- settled/peak object, metadata, source-hold, and staging bytes;
- exact commands, revision, corpus hashes, environment, raw artifacts, thresholds, and
  `PASS`/`FAIL`.

Stage 04 must not start merely because the code looks incremental. Every required
Stage 03 result remains open until measured.
