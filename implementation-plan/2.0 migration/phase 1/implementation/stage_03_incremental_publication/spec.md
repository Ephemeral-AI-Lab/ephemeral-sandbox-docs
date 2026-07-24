# Stage 03 — corrected identity and complete private publication

Status: specification only; implementation is blocked on the Stage 02 v3 owner
amendment.

Normative dependencies:

- [implementation index](../index.md)
- [minimal storage contract](../layerstack_storage_contract.md)
- [Preparation 04 acceptance criteria](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)
- [Stage 02 contract](../stage_02_portable_root_contract/spec.md)
- [Stage 02→03 implementation handoff](handoff_from_stage_02.md)

## 1. Outcome

Stage 03 delivers the first complete private LayerStack v3 vertical slice. It does not
alter public v1 reads or writes.

The stage is complete only when one normal publication path provides:

- owner-approved bounded Merkle identity;
- deterministic streaming SeqCDC and typed chunk installation;
- persistent changed-path tree updates with unchanged structural sharing;
- private branch heads, named checkpoints, pins, checkout/revert/reset, and clean
  branch/MCTS forks;
- idempotent durable recovery keyed by `PublicationId`;
- same-path OCC conflict and disjoint-path rebase;
- durable source protection for imported v1 carrier locations;
- optional hidden v1/candidate comparison using this exact final protocol.

An algorithm-only CDC result is insufficient.

## 2. Entry conditions

1. Stages 00–02 pass.
2. Stage 02 owner approval defines `RootRecordV3`, bounded `TreePage`, `FileNode`,
   `SegmentPage`, and `Chunk` codecs and preserves v2 read compatibility.
3. Preparation 04 gates and benchmark corpus are frozen.
4. Public authority remains v1.

## 3. Identity and storage

The canonical layout and record fields are defined only in
`../layerstack_storage_contract.md`. Stage 03 creates only:

- `.storage-writer.lock` and top-level `CONTROL`;
- deterministic loose logical objects;
- private heads/checkpoints/pins;
- publication operations and bounded work;
- ordinary locator-generation/source leases only when imported payload remains in an
  existing v1 carrier.

It does not create pack, locator-run, materialization, GC, or migration-authority
directories unless a real Stage 03 imported carrier needs one physical locator and
source hold. It never creates empty future directories.

The full `/eos` tree and ownership boundaries are normative in
[the storage contract](../layerstack_storage_contract.md#4-complete-eos-ownership-and-storage-tree).
Publication captures changed input from
`/eos/workspace/<session>/upper`; it never treats WorkspaceManager scratch, command
transcripts, `/eos/storage`, or daemon runtime files as logical payload.

`RootRecordV3` identity covers logical format/capabilities/chunk profile and the Merkle
tree root. Publication ID, branch, generation, parent/base, author, timestamp, backend,
and carrier location are excluded.

## 4. Publication input and canonical mutation semantics

Capture produces a bounded stream of final logical mutations over raw validated Linux
path bytes. Whiteouts and opaque directories are translated before identity into:

- remove entry/subtree;
- create or replace directory metadata;
- create or replace file/symlink/special node;
- rename as source removal plus destination replacement with one conflict group;
- hardlink-group updates as one conflict group.

The changed-path spool is externally ordered and deduplicated with Preparation 04
buffers/fan-in. It never becomes an in-memory complete path set.

Conflict keys include:

- the exact path;
- all affected ancestors whose child map or directory metadata changes;
- rename source and destination;
- an opaque-directory subtree boundary;
- every member of an affected hardlink group.

Two publications conflict when base→current changes intersect those keys semantically,
not merely when identical path bytes occur.

## 5. Streaming SeqCDC and tree construction

SeqCDC uses the Preparation 03 selected scalar algorithm/profile and existing SHA-256
dependency. The implementation:

- reads through fixed 32 KiB windows/rings;
- emits chunk descriptors without queueing payload chunks;
- installs a typed chunk with put-if-absent semantics;
- uses no target-image helper or environment input;
- produces identical chunk boundaries/IDs across supported host architectures;
- applies explicit sparse/zero, xattr, hardlink, symlink, device, and FIFO rules;
- rejects unsupported required capabilities.

File segment lists and directory child maps use bounded pages. Updating `P` logical
paths rewrites only the affected file/segment/directory pages and ancestors. A complete
flat manifest may be streamed for diagnostics but is never read or written by normal
publication.

## 6. Publication protocol

1. Scope the stable caller `PublicationId` to the branch and derive the common
   operation ID from `(publication-kind,BranchId,PublicationId)`. Create/open it and
   compare its request digest. Reuse on another branch is an independent operation.
2. If terminal within the advertised retry window, return the exact recorded outcome.
   If the ID was reused with different input, return `IdempotencyMismatch`. If an
   acknowledged/expired outcome is no longer retained, return `OutcomeExpired`; never
   perform a new publication under that ID.
3. Read the branch `{base_root,base_generation}` and persist preparing state.
4. Capture, chunk, build pages, and install immutable objects outside the writer lock.
   Persist prepared result root, input digest, changed-path run, and base.
5. Enter the brief writer-lock commit section.
6. Before changing a visible ref, participate in any active GC root barrier.
7. If the head still equals the base, atomically install
   `{result_root,base_generation+1,PublicationId}`.
8. If it advanced, leave the lock and compare only the spooled conflict keys in base
   and current roots. Return a stable conflict on overlap. For disjoint changes, rebase
   on current, rebuild touched pages, and retry within fixed count/time limits.
9. While still excluding a later head advance, persist the terminal operation outcome.
   A crash between head visibility and terminal persistence is repaired from
   `head.publication_id` and the prepared operation before another update may commit.
10. Release operation resources and retain the bounded terminal outcome per the
    advertised retry/ack policy.

Expensive work never occurs under the writer lock. The global short commit section is
accepted only if the Preparation 04 disjoint-progress throughput gate passes.

## 7. Ref semantics

| Operation | Logical effect | Required cost |
| --- | --- | --- |
| clean checkpoint | create named checkpoint ref to current root | `O(1)` metadata, zero payload |
| dirty checkpoint | ordinary incremental publication, then checkpoint ref | publication cost plus `O(1)` |
| checkpoint delete | remove only the ref | `O(1)`; no immediate payload deletion |
| clean branch/MCTS fork | new head to existing root, generation zero | `O(1)` metadata, zero payload/native tree |
| checkout | select a session head/root | no head mutation |
| revert | publish a new event selecting the historical tree | ordinary publication; generation advances and the historical `RootId` may be reused |
| reset | move a head to an existing root with new generation | `O(1)` metadata; explicit reset outcome |

Checkpoint and branch names are policy names, not identity inputs. Inactive MCTS nodes
use a head only when independently writable; otherwise a pin is sufficient. No node
requires both by default.

## 8. Recovery and lifetime

At boot, inspect bounded nonterminal operation directories:

- pre-prepared private work can be reaped by exact owner;
- prepared operations are resumed or stably conflicted;
- a head naming an operation lacking a terminal outcome repairs that outcome before the
  branch advances;
- loose orphan objects remain safe and are reclaimed only after Stage 05 GC exists;
- any root that locates payload in a legacy carrier has a durable fenced source hold
  before its head/ref can become visible;
- missing or corrupt last locators fail closed; the root is not called durable.

Operation registries, retry tables, changed-path spools, task sets, workers, FDs,
buffers, and encoders obey Preparation 04 caps. Tasks are owned, cancelled, and joined.
New logical storage code is safe Rust.

## 9. Optional validation mode (absorbed former shadow-ingest work)

V1 remains public authority. A correlated v1 publication may invoke the normal Stage
03 protocol against a hidden candidate validation head and compare logical/materialized
results. The candidate intent is durable before its result is called recoverable.
Imported source bytes are held before the hidden head becomes visible.

No `refs/legacy` mapping is created. Temporary v1↔v3 correlation used by validation is
bounded operation evidence; durable lifetime comes from the normal root, locator, and
lease mechanisms.

Comparison is bounded evidence. There is no shadow-specific root format, observation
record, receipt family, control file, transaction family, or authority claim. Turning
validation off stops new hidden publications; normal ref/GC rules retire its data.

## 10. Complexity and resource requirements

- first import: `O(R+E)`, bounded resident memory;
- later publication: `O(U+E_changed+K+P log_B N)` plus bounded changed-event ordering;
- OCC attempt: `O(Q log_B N)`, fixed retry/time cap;
- no full-file buffering, total-tree/hash, history scan, or all-path set;
- clean ref operations: `O(1)` metadata and zero payload;
- object/tree sharing preserves unchanged history;
- settled and peak object, operation, source-hold, and metadata bytes are measured.

No statement above is a benchmark result.

## 11. Exit criteria

- all [Stage 03 E2E cases](e2e_test.md) pass, including crash boundaries and
  ancestor/rename/hardlink conflicts;
- the [benchmark note](benchmark_note.md) contains measured results and every required
  Stage 03 Preparation 04 cell passes;
- repeated small edits show no total-tree/history reads or writes;
- clean checkpoint/fork counters show zero payload and native-tree allocation;
- lost-response retry returns the original result after every commit failpoint;
- disjoint writers meet the required progress/throughput gate;
- imported last-locator source holds survive restart and legacy cleanup attempts;
- public v1 behavior and `/eos` exposure remain unchanged.
