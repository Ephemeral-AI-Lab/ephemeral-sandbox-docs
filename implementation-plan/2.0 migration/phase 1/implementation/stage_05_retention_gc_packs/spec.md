# Stage 05 — retention, physical compaction, GC, and squash

Status: specification only.

Normative dependencies:

- [implementation index](../index.md)
- [minimal storage contract](../layerstack_storage_contract.md)
- [Stage 04](../stage_04_candidate_materialization/spec.md)
- [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

## 1. Outcome

Stage 05 is the first stage authorized to remove logical objects or physical carriers.
It delivers one physical-lifecycle system for:

- named-ref/pin/lease/operation/materialization retention;
- immutable packs and bounded locator-run consolidation;
- disk-backed strong-edge tracing;
- concurrent-ref barrier and conservative restart;
- grace, final recheck, and bounded exact deletion;
- same-`RootId` native squash/materialization replacement;
- evacuation of legacy/external last locators.

No reference count is deletion authority. No resident all-live set is allowed.

## 2. Retention roots and strong edges

The mark seed stream is typed:

- `ContentRoot(RootId)` and `AttributionRoot(AttributionRootId)` from
  branch/checkpoint/pin/lease/policy refs;
- content/attribution roots and direct `Object(ObjectId)` from prepared/committing
  operations;
- `ContentRoot(RootId)` plus `MaterializationGeneration` from active/pinned
  materializations; attribution is retained by history-bearing refs rather than the
  native carrier;
- physical locator generations and source-protection leases required by active
  readers/builds;
- roots/proof named by the active migration operation and ordinary fenced holds on
  existing v1 sources until evacuation/retirement.

Strong object edges are the canonical v3 root/tree/file/segment/chunk graph and the
separate attribution-root/page graph. Parent/base/publication ancestry does not retain
history. Attribution pages persist the current blame snapshot directly; they do not
depend on retaining publication operations. Terminal outcomes retain their result
only for the explicit retry/ack window and do not become an unbounded history policy.

Checkpoint deletion removes one seed; it never synchronously deletes payload.

## 3. Packs and locators

Loose objects are found by typed ID and need no locator record. A locator run maps only
objects stored in a pack or approved external carrier to verified physical extents.

Packing:

1. selects a bounded streamed set without changing logical IDs;
2. reads/verifies each source through a protected locator;
3. writes and fsyncs an immutable pack;
4. externally sorts and fsyncs one immutable locator run using bounded readers;
5. under the brief writer lock installs a new locator `CURRENT`;
6. retains source locations through active leases, at least one later complete durable
   grace boundary, and final recheck.

`CURRENT` has a fixed maximum run count and encoded-byte size set before implementation.
Crossing either limit triggers deterministic bounded consolidation; admission applies
backpressure if consolidation cannot keep up. Lookup/startup may never load all
historical locator records or runs into memory. A mixed live/dead pack is never deleted
wholesale while any live object lacks another selected locator.

## 4. GC barrier and mark

Only one GC operation is active, named by `gc/CURRENT`.

1. Under the writer lock install the active GC operation and durable root-log state.
2. Snapshot typed content/attribution seeds to disk and traverse object edges in
   bounded pages.
3. External-sort/deduplicate mark runs with Preparation 04 fan-in/buffer limits.
4. Every head/checkpoint/pin/lease/materialization/authority visibility mutation takes
   the same closure lock, observes `gc/CURRENT`, appends/fsyncs its root/subject to the
   active root log, and only then makes the mutation visible.
5. The collector closes admission under that same lock, drains to a fixed point, and
   records the closed generation. A generation change or ambiguous registration aborts
   deletion conservatively.

Mark runs and root logs are operation staging and count in peak/settled residue. They
are not hidden as generic metadata.

## 5. Grace and deletion

Sweep externally merge-joins allocated objects/locators against disk mark runs and
records bounded deletion candidates. Candidate bytes stay at their normal readable
paths throughout grace, so a valid newly created ref can retain them.

After at least one complete later durable GC boundary:

1. take the mutation closure lock;
2. final-recheck every ref class, prepared/committing operation, lease/fence, active
   materialization generation, locator `CURRENT`, active migration operation/ordinary
   v1 source-protection lease, and policy root;
3. verify a candidate is not a last locator and its graph cannot be selected by a
   newly admitted validated ref;
4. rename only one bounded exact batch into this GC operation's private `work/trash`,
   fsync, and durably record `deleting`;
5. release the lock and unlink exact recorded paths.

Ref creation validates the selected root graph before visibility and cannot select a
now-missing object. On restart, ambiguous trash not covered by durable `deleting` state
is restored before ref mutations are admitted. Durable exact deletion resumes.
Uncertainty, corrupt mark data, missing cursor, clock ambiguity, expired-but-unfenced
lease, or I/O error retains bytes.

No recursive deletion target may be derived from an unresolved environment variable,
glob, broad root, mtime, count hint, or reference count.

## 6. Squash and materialization replacement

Squash is not a logical publication or a separate transaction family. It invokes the
Stage 04 generation build for an existing `RootId` with a flatter carrier plan:

1. protect the root, source locators, and active generation;
2. build/verify/fsync a private replacement generation;
3. participate in the GC barrier and atomically replace materialization `CURRENT`;
4. admit new sessions on the replacement while old sessions keep old leases;
5. retire the old generation only through the same grace/final-recheck protocol.

The `materialization-id` remains derived from root/backend/profile; only generation
changes. Checkpoint, branch, MCTS, and logical root IDs are unchanged. Manual,
depth-triggered, fragmentation-triggered, evacuation, and repair squash share this
mechanism.

Each admitted session keeps its exact old generation lease and private
`/eos/workspace/<session>` tree. The `CURRENT` switch affects only new sessions.
LayerStack GC may remove eligible old materialization generations but must never scan
or delete WorkspaceManager-owned `upper`, `work`, or `executions` paths.

## 7. Recovery

| Boundary | Restart rule |
| --- | --- |
| pack incomplete | source remains selected; reap/resume exact operation |
| pack/run durable, `CURRENT` old | old locations win; new output is orphan/resumable |
| locator `CURRENT` new | new locations usable; sources stay grace protected |
| GC mark/root log incomplete | resume cursor or abandon and retain |
| barrier closure ambiguous | reopen/abort; retain |
| candidates recorded during grace | bytes remain readable at normal paths |
| trash rename ambiguous | restore before admitting refs |
| durable `deleting` batch | resume exact unlink after validation |
| squash pre-`CURRENT` | old generation active |
| squash post-`CURRENT` | new generation active; old lease/grace protected |

## 8. Bounds and complexity

- pack/compaction: proportional to selected bytes/records, bounded streaming memory;
- locator lookup/startup: bounded by fixed current-run count/bytes, not history;
- GC mark: `O(V_content+V_attribution+strong_edges)` time, proportional temporary
  disk, `O(B)` RAM;
- sweep: streamed/sliced `O(A)` with fixed candidate/delete batch;
- squash: streamed `O(S+E_s)` outside the short pointer section;
- no task-owned 100k-record `Vec`, replacement slice, full locator map, or all-live set;
- run fan-in, buffers, tasks/workers, FDs, mappings, deletion batch, cycle wall slice,
  trash bytes, and operation residue have explicit caps/backpressure;
- no detached tasks, ownership cycles, or reference-count-only deletion.
- GC roots and candidate inventories are confined to `/eos/layer-stack`; other
  top-level `/eos` owners are outside its allocation and deletion namespace.

All duplicate bytes, locator amplification, run count, pack slack, mark-run space,
trash overlap, materialization overlap, and settled residue are measured against
Preparation 04. Nothing here claims a passing result.

## 9. Exit criteria

- [E2E plan](e2e_test.md) passes concurrent ref/checkpoint/MCTS/materialization
  creation at every GC phase;
- last-locator, reader lease, restart uncertainty, trash restoration, and mixed-pack
  cases pass;
- squash preserves exact logical `RootId` and checkpoint accessibility;
- checkpoint blame/attribution remains queryable after squash, compaction, GC, and
  restart;
- [benchmark note](benchmark_note.md) records all Preparation 04 maintenance/space
  results;
- safe-Rust/bounded ownership audit passes;
- no legacy carrier is evacuated until an independently verified selected locator is
  durable;
- public authority remains v1.
