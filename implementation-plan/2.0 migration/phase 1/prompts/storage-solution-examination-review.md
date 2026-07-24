# Phase 1 — StreamCDC versus SeqCDC decision

Target Codex task: `019f8ad7-3280-7be1-b0e0-c646cd55c72d`

Required StreamCDC reference task:
[`codex://threads/019f91b6-492d-79f0-8a5b-6e106a8c4c24`](codex://threads/019f91b6-492d-79f0-8a5b-6e106a8c4c24)

## Mission

Choose exactly one Phase 1 chunking algorithm:

1. synchronous StreamCDC, using the stable `fastcdc-rs v2020` boundary behavior
   as the reference; or
2. scalar SeqCDC implemented as a genuinely bounded streaming iterator.

This is a decision between these two algorithms. Do not introduce a third
finalist.

The recommendation must provide the best defensible balance of:

1. exact correctness and compatibility with the existing LayerStack;
2. warm materialization, mount, remount, squash, file, command, and PTY speed;
3. honest total physical space efficiency;
4. bounded time and application-memory complexity;
5. universal Docker compatibility with no target-image setup;
6. compatibility with efficient Phase 2 branching, rollout, checkpoint,
   rollback, and MCTS; and
7. implementation simplicity, no external operational dependencies, and low
   maintenance risk.

This is a read-only code and architecture examination. Do not implement either
candidate or modify production code.

Hold the native-carrier, CAS, digest, manifest, pack, index, transaction,
recovery, and collection design constant between the candidates. The decision
must isolate the chunking algorithm rather than rewarding one candidate for a
different storage layout.

Select one algorithm, not a shortlist or hybrid. If neither passes every hard
gate, return `neither is viable` and identify the smallest missing proof or
design change. Do not weaken a hard gate.

## Authority order

When inputs conflict, use this order:

1. this prompt and current user requirements;
2. the Phase 1 migration overview and space/time/materialization specification;
3. actual behavior and tests in the current production LayerStack;
4. reproducible implementation and primary-source evidence;
5. the required StreamCDC reference task; and
6. other secondary descriptions.

The StreamCDC task is a required lead and audit record, not unquestionable
authority. Recheck its important claims against the pinned source it cites.

## Read first

Read each relevant source completely before deciding.

### Migration requirements

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/index.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/index.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prep/01-cdc-cas-space-time-materialization-spec.md`

Use the migration index to judge whether the Phase 1 storage choice forms a
sound foundation for Phase 2. Do not implement SandboxGraph, rollout
scheduling, MCTS, or process-state rollback.

### Current production behavior

Read the applicable code, tests, and local instructions under:

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/AGENTS.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/crates/sandbox-runtime/workspace/src/`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/crates/sandbox-runtime/overlay/src/`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/crates/sandbox-runtime/namespace-execution/src/`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/crates/sandbox-runtime/namespace-process/src/`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/crates/sandbox-runtime/operation/src/`

Trace the actual implementations and tests for LayerStack roots and manifests,
workspace creation, file operations, publication, squash, OverlayFS mount,
live remount, namespace execution, `exec_command`, PTY, `write_stdin`,
cancellation, and child reaping. Use code evidence rather than assumptions
from names or architecture prose.

### StreamCDC reference

Read the complete Codex task:

`codex://threads/019f91b6-492d-79f0-8a5b-6e106a8c4c24`

Then inspect the exact upstream sources cited by that task, including:

- `nlfiedler/fastcdc-rs` version `4.0.1`, commit
  `f76938d8c2d77799852415247c9b3e1fd91b73f3`;
- synchronous `fastcdc::v2020::StreamCDC`;
- synchronous `fastcdc::v2020::FastCDC`;
- conservative `fastcdc::v2016::FastCDC`;
- `puntakana/seqcdc-rs` version `0.1.0`, commit
  `f1d3e33cb29b08daf27c77aca98261d85e48ba65`; and
- the authors' SeqCDC reference implementation identified by that task.

Confirm or reject the following StreamCDC findings:

1. synchronous `v2020` is reliable for conventional even, power-of-two
   parameters;
2. a safe comparison configuration is `4 KiB minimum / 16 KiB average /
   64 KiB maximum`;
3. odd `v2020` size parameters can violate minimum-boundary expectations or
   diverge from `v2016`;
4. the asynchronous implementation has separate mask-rounding and feature
   combination concerns and is unnecessary for the Phase 1 storage path;
5. `StreamCDC` keeps one fixed `max_size` input buffer but returns each chunk in
   an owned `Vec<u8>`;
6. retaining returned chunks or sending them to an unbounded queue changes
   memory from bounded streaming to growth proportional to processed data;
7. immediate hash/write/drop processing keeps retained file state bounded;
8. per-chunk allocation and copying can create allocator churn and elevated
   RSS even without a leak;
9. the SeqCDC scalar core is close to its reference, but the reviewed Rust
   package reads full files, lacks production-strength validation and golden
   vectors, and is not a safe streaming dependency as written; and
10. stable golden boundary fixtures are required so an algorithm or parameter
    upgrade cannot silently change historical roots.

Do not choose an upstream crate merely because it exists. Compare these exact
production forms:

- **StreamCDC candidate:** a minimal internal synchronous implementation with
  `fastcdc-rs v2020 StreamCDC` boundary behavior, fixed validated parameters,
  caller-controlled bounded processing, and no async feature or crate
  dependency.
- **SeqCDC candidate:** a minimal internal scalar implementation matching the
  authors' algorithm, rewritten around a genuine bounded streaming iterator
  with fixed buffers, validation, golden vectors, and no `read_to_end()` or
  crate dependency.

`fastcdc-rs v2016` may be used only as a correctness reference for boundary
edge cases. It is not a third candidate.

Label every important conclusion as `published`, `source-verified`, `inferred`,
or `unknown`.

## Existing LayerStack contract to preserve

First confirm these statements against current code and correct any that are
inaccurate:

- immutable native lower layers are resolved newest first;
- `/workspace` is a complete native OverlayFS view of immutable lowers plus one
  private writable upper and work directory;
- a clean session does not clone the merged workspace payload;
- the first write to a lower-only file may copy the complete resulting file
  into that session's upper;
- repeated edits in one unpublished session reuse that upper file rather than
  creating private historical versions;
- publication captures the private upper rather than rescanning the complete
  merged workspace;
- squash builds and commits a replacement immutable root before the live
  namespace switch;
- live remount uses the existing private upper, a fresh work directory, a
  staged replacement mount, a rollback point, atomic mount moves, verification,
  and fail-closed cleanup; and
- command, file, PTY, stdin, signal, cancellation, and reaping paths operate on
  the native mounted filesystem.

Phase 1 optimizes retained immutable-history storage. It must not remove,
weaken, or reinterpret existing LayerStack, workspace, file, command, squash,
mount, remount, namespace, lease, OCC, blame, recovery, or GC behavior.

## Non-negotiable implementation constraints

The selected solution must:

- be implemented in Rust and embedded in the normal Ephemeral Sandbox binary;
- require no SQLite;
- require no external database, service, host package, target-image package,
  helper binary, sidecar, resident daemon, Docker plugin, kernel module, FUSE,
  reflink, new privilege, or extra Linux capability;
- require no installation or configuration step beyond deploying the normal
  Ephemeral Sandbox binary;
- introduce no third-party runtime dependency;
- avoid adding a new Rust crate when the small required algorithm can be
  implemented and audited directly in the product;
- if source is adapted, record its license and provenance and include only the
  minimal synchronous algorithm needed;
- use no async runtime or async CDC feature merely to chunk a sequential file;
- operate above ordinary Linux directories inside the Docker VM;
- preserve compatibility with arbitrary target-image contents because no
  target-image utility participates;
- qualify initially on one pinned Ubuntu 24.04 Docker image without an image
  matrix;
- keep active workspaces on native OverlayFS;
- perform no CAS reconstruction, manifest lookup, or per-file RPC in
  `exec_command`, normal file I/O, PTY, or `write_stdin` hot paths;
- reconstruct a missing native lower completely, verify it, fsync it, and
  expose it atomically before it becomes executable;
- retain and deterministically reconstruct old leased roots;
- support immutable roots, compare-and-swap publication, idempotent retries,
  bounded disk-backed indexes, journals, and crash recovery;
- keep file blame separate from chunk identity;
- expose stable, immutable, deterministic, versioned root identities for Phase
  2 branches and checkpoints;
- allow inactive branch nodes to remain disk-backed roots and retained content
  rather than resident sandboxes or permanent native materializations;
- use fixed chunk and I/O buffers, bounded workers and queues, bounded
  index-page access, and disk-backed maintenance cursors; and
- remain correct with a cold page cache and after process restart.

Do not claim macOS, Windows, native-Linux, or other-image qualification from
algorithm portability. Analyze the complete storage, transaction,
materialization, recovery, GC, namespace, and mount design and mark unverified
behavior `unknown`.

## Hard rejection gates

Reject a solution before scoring if it:

- loses filesystem bytes or required metadata;
- changes existing command, file, PTY, stdin, namespace, squash, or remount
  semantics;
- can silently lose concurrent writes or invalidate a leased old root;
- derives blame ownership from chunk ownership;
- can expose a partial or corrupt materialization;
- cannot recover publication, hydration, carrier evacuation, compaction,
  squash, remount, or GC idempotently;
- requires an in-memory global index, full-file buffer, full-tree buffer,
  full-file or unbounded mmap, unbounded queue, unbounded cache, unbounded
  worker set, or history-sized resident state;
- collects a large file's returned chunks before processing them;
- relies on allocator behavior to enforce the memory limit;
- permanently stores both a full native current root and a second packed copy
  of the same current content without a narrowly bounded justification;
- moves CDC/CAS work into native execution or the live-remount frozen interval;
- requires SQLite or any external setup, service, dependency, or new privilege;
- requires one resident sandbox, native materialization, or workspace-sized
  copy for every inactive Phase 2 branch;
- is unavailable under a usable open-source license;
- lacks sufficient algorithm and format detail for faithful Rust
  implementation; or
- has no falsifiable advantage over the current raw LayerStack.

Correctness, recovery, leases, OCC, blame, namespace isolation, and
bounded-memory failures are disqualifying. Do not average them into a speed or
space score.

## Required examination

### 1. Establish the current-system boundary

Produce a concise evidence-backed diagram of:

```text
immutable history -> roots + CDC/CAS + manifests + indexes + blame
active workspace  -> native lower carriers + private OverlayFS upper
execution         -> existing namespace, command, file, PTY, and stdin paths
publication       -> bounded streamed capture + transactional immutable root
squash/remount    -> native build before quiesce + namespace switch
retention         -> leases + bounded disk-backed collection/recovery
Phase 2 graph     -> immutable RootIds; only active branches rent sandboxes
```

Distinguish:

- warm root activation from cold hydration;
- active upper copy-up cost from retained-history cost;
- publication cost from native execution cost;
- logical bytes from allocated physical bytes;
- required hot native carriers from unique cold historical content; and
- durable branch nodes from active sandbox processes.

### 2. Compare StreamCDC and SeqCDC

Compare only:

- an internally implemented synchronous StreamCDC-equivalent iterator; and
- an internally implemented genuinely streaming scalar SeqCDC iterator.

Use the current whole-file history behavior only as product context. Use
FastCDC v2016, upstream crate wrappers, SIMD SeqCDC, Gear variants, or other CDC
algorithms only to verify claims; do not score or promote them as finalists.

Hold constant for both candidates:

- input files and edit patterns;
- dominant workload weighting toward repeated edits of a few lines of source
  code, while still considering insertions, offset shifts, append, full
  rewrites, binary files, compressed files, and very large files;
- effective target average chunk size and allowed chunk-size range;
- digest and object identity;
- native-carrier and packed-object policy;
- manifest and segment encoding;
- disk-backed locator/index;
- worker, queue, buffer, and page limits;
- retention and lease set;
- publication, hydration, squash, recovery, and collection semantics; and
- all current LayerStack operations.

If the algorithms cannot use identical boundary parameters, normalize the
comparison by effective average chunk size and explicitly explain the mapping.
Do not let one candidate win by silently producing much larger chunks, less
metadata, or weaker localized-edit reuse.

For each candidate report:

- exact algorithm, parameters, digest, manifest, carrier, pack, and index
  model;
- source status, license, provenance, and CPU requirements;
- exact amount of new internal Rust code and any dependency implication;
- boundary stability and upgrade behavior;
- large-file memory behavior;
- input-buffer, returned-chunk, allocation, and copying behavior;
- required backpressure and queue limits;
- expected localized-edit reuse and metadata overhead;
- expected publication and cold-hydration cost;
- warm activation, squash, and remount impact;
- worst-case full rewrite and compressed-file behavior;
- deterministic old-root reconstruction;
- recovery and collection model;
- Phase 2 branch/checkpoint behavior under the same storage layout; and
- operational and maintenance risk.

### 3. Validate the common storage layout

Do not select a chunker solely from its boundary loop. Define one common
storage layout that preserves native execution while avoiding a permanent
double copy of current data, then judge how each algorithm behaves inside it.

For the common layout state:

- how native immutable carriers act as valid content locations while hot;
- what is packed immediately and what is not;
- how small objects and metadata avoid one-file-per-chunk overhead;
- how the pure-Rust disk-backed locator/index works without SQLite;
- how duplicate puts and locator changes are transactional;
- how a carrier is evacuated to packed cold storage before reclamation;
- how cold content is hydrated back to an atomic native carrier;
- how leases prevent deletion of current, old, and branch roots;
- how manifests, blame, journals, and collection cursors remain bounded and
  disk-backed; and
- how old format versions remain readable after algorithm upgrades.

### 4. Score both candidates after hard gates

Use this 100-point technical score:

| Category | Points |
| --- | ---: |
| Existing LayerStack correctness and integration fit | 25 |
| Warm materialization, mount/remount, squash, command, file, and PTY performance | 27 |
| Honest total physical space efficiency | 18 |
| Bounded memory plus time/space complexity | 10 |
| Portability, embeddability, setup, and dependency simplicity | 10 |
| Phase 2 branch, checkpoint, rollback, rollout, and MCTS compatibility | 5 |
| Recovery, maturity, and implementation risk | 5 |

Apply one evidence-confidence multiplier:

| Confidence | Multiplier |
| --- | ---: |
| Complete, directly applicable, source-verified implementation | `1.00` |
| Maintained source plus credible applicable published evidence | `0.85` |
| Sound source or paper with incomplete LayerStack-specific evidence | `0.70` |
| Theoretical, immature, derivative, or difficult to verify | `0.50` |

Calculate:

```text
adjusted_score = technical_score × evidence_confidence
```

Break close ties in this order:

1. existing LayerStack behavior and correctness;
2. warm materialization, mount/remount, squash, and native runtime speed;
3. bounded-memory confidence for very large files;
4. settled total physical space;
5. implementation, setup, and dependency simplicity;
6. Phase 2 checkpoint and branch-activation efficiency.

Do not promote a more sophisticated algorithm merely for novelty or peak
chunker throughput. End-to-end LayerStack fit is the decision target.

### 5. Select StreamCDC or SeqCDC

Name exactly one recommended algorithm at the level required for
implementation:

- chunking algorithm and fixed parameters;
- streaming buffer ownership and lifetime;
- returned-chunk representation and allocation policy;
- maximum in-flight chunks and backpressure;
- digest and typed object identity;
- segment and manifest encoding;
- native-carrier role;
- packed-object role;
- pure-Rust disk-backed index;
- root, lease, OCC, blame, journal, recovery, and collection relationship;
- hot-to-cold carrier transition;
- cold hydration sequence; and
- format and algorithm upgrade policy.

For StreamCDC, state exactly how the internal form differs from
`fastcdc-rs v2020 StreamCDC`, particularly:

- whether it avoids one fresh owned allocation per chunk;
- how it preserves exact boundaries;
- how it handles short reads and final chunks;
- how it enforces even, power-of-two parameters;
- how it prevents a caller from retaining unbounded chunk payload;
- how it prevents an unbounded downstream queue; and
- how golden vectors lock historical boundary behavior.

For SeqCDC, state exactly how the internal streaming form differs from
`seqcdc-rs`, particularly:

- how it eliminates full-file `read_to_end()`;
- the minimum retained lookbehind/lookahead required by the algorithm;
- how boundary state crosses input-buffer refills;
- how it validates all parameters and short inputs;
- how it prevents a cut point beyond available input;
- how it preserves the authors' scalar boundary semantics;
- how it bounds returned chunks and downstream queues; and
- how differential and golden vectors lock historical behavior.

Explain why the losing algorithm is not selected.

Favor the simpler algorithm unless the more complex one has a strongly
evidenced whole-system advantage in publication speed or localized-edit
storage reuse. Chunking throughput alone is insufficient.

### 6. Map the chosen solution onto current code

For every relevant module and public operation, classify it as:

- `reuse unchanged`;
- `modify internally, preserve interface`;
- `new storage method`; or
- `remove/replace`.

At minimum cover:

| Area | Required operations |
| --- | --- |
| LayerStack roots | create, resolve, verify, lease, publish, read old root |
| Workspaces | create, destroy, capture upper, recover, squash, remount |
| Files | list, stat, read, write, edit, upload, download, metadata, blame |
| Overlay mount | lower resolution, upper/work creation, mount, unmount |
| Namespace execution | `exec_command`, cancellation, stdout/stderr/status |
| PTY/process | create, resize, signal, drain, `write_stdin`, EOF, reaping |
| Publication | stream upper, chunk, digest, manifest, journal, root CAS |
| Concurrency | leases, OCC generation, conflicts, deterministic retry/rebase |
| Materialization | warm resolve, cold hydrate, verify, expose, rollback |
| Squash/remount | plan, build, quiesce, switch, rollback, lease exchange |
| Retention | pack/evacuate, compact, collect, trash, quarantine, disk cursors |

Any existing behavior that cannot be preserved is normally disqualifying
because Phase 1 optimizes storage rather than removing functionality.

### 7. State time, space, and memory complexity

Use:

- `D`: mounted lower-layer depth;
- `U`: captured upper bytes;
- `E`: captured upper entries;
- `K`: generated chunks;
- `R`: bytes missing from a requested native materialization;
- `Q`: changed paths used by diff/OCC/blame;
- `N`: disk index records;
- `G`: objects processed by one collection slice; and
- `C`: configured concurrency.

State expected and worst-case time, temporary disk, settled disk, and
application-memory complexity for:

- clean session creation;
- warm materialization and mount;
- cold hydration;
- file read/write/edit;
- large-file publication;
- root lookup and diff;
- blame transition and query;
- squash;
- live-remount frozen interval;
- old-root activation;
- compaction and collection; and
- crash recovery.

Declare concrete limits for:

- maximum chunk window;
- input and output buffers;
- maximum workers;
- maximum queued chunks and bytes;
- maximum index pages;
- maximum per-publication memory;
- maximum storage-service RSS;
- cancellation cleanup;
- error and panic cleanup; and
- behavior when any limit is reached.

The selected architecture must satisfy:

```text
memory =
    O(fixed_chunk_window
      + fixed_IO_buffers
      + fixed_workers × fixed_worker_buffer
      + fixed_queue_capacity
      + fixed_index_page_budget)
```

After configuration, application memory must remain `O(1)` with file size,
stored bytes, files, chunks, roots, leases, and history depth.

### 8. Account for total physical space

Use:

```text
T(t) =
    L_hot(t)
  + H_cold(t)
  + ΣU_active(t)
  + P_staging(t)
  + M(t)
```

And:

```text
D_ideal = C_current + H_unique

settled_amplification = T_settled / D_ideal
```

Explain expected storage for:

- a clean session;
- the first tiny edit to a large lower-only file;
- repeated edits before one publish;
- repeated small edits across ten publishes;
- multiple modified sessions;
- duplicate files;
- renames;
- sparse files;
- compressed or encrypted rewrites;
- old leased roots;
- branch checkpoints;
- hydration;
- squash; and
- evacuation, compaction, and collection peaks.

Count current native carriers, every active upper, staging, manifests, index,
blame, journals, trash, quarantine, and pack slack. CAS bytes alone are not
total LayerStack storage.

### 9. Check Phase 2 compatibility

Evaluate the selected Phase 1 solution as the storage foundation for
`SandboxGroup` and an immutable checkpoint graph.

Require:

- stable, versioned `RootId` checkpoint identities;
- branch intent from an immutable parent without a complete workspace clone;
- one isolated sandbox and private upper only for each active branch;
- disk-backed inactive branch and rollout nodes;
- warm activation by leasing existing native lower carriers;
- verified cold activation before native execution;
- idempotent checkpoint publication with base root, publisher/branch identity,
  request identity, write set, and expected generation;
- deterministic conflict, merge, promotion, and rejection behavior;
- rollback by releasing the attempt and activating an earlier retained root;
- durable pins for accepted nodes, ancestors, frontier nodes, and in-flight
  rollouts;
- pruning that makes unleased content reclaimable without an in-memory graph;
- bounded active sandbox concurrency independent of durable node count; and
- separate durable rollout, policy, reward, trajectory, evaluation, and
  exactly-once MCTS backpropagation metadata.

For each candidate state the cost of `branch`, `activate`, `checkpoint`,
`rollback`, `merge/promote`, and `prune`; the pressure created by rapid
checkpoint churn; and whether Phase 2 would require a storage-format rewrite.

Phase 2 compatibility is a selection criterion, not authorization to implement
Phase 2. Do not prefer a speculative MCTS-specific optimization that weakens
the current LayerStack or makes Phase 1 harder to deploy.

## Required output

Create exactly one review document:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prep/02-storage-solution-examination-review.md`

Do not edit production code, candidate implementations, shared specifications,
trackers, or this prompt.

The document must contain:

1. **Decision** — `StreamCDC`, `SeqCDC`, or `neither is viable`;
2. **Decision confidence** — high, medium, or low;
3. **Current LayerStack facts** verified against source;
4. **Hot/cold and Phase 2 architecture diagram**;
5. **StreamCDC and SeqCDC source audit** against the required Codex task and
   pinned sources;
6. **Hard-gate table** for both candidates;
7. **Complete technical and adjusted score table**;
8. **Source-verified versus inferred evidence table**;
9. **Why the selected algorithm wins and the other loses**;
10. **Common on-disk and transaction architecture held constant** between the
    two candidates;
11. **Current-code integration map** for all required operations;
12. **Time, temporary-space, settled-space, and memory complexity table**;
13. **Large-file memory and allocation analysis**;
14. **Total-physical-space examples**;
15. **Failure, recovery, lease, OCC, blame, and collection analysis**;
16. **Dependencies, license, portability, setup, and CPU compatibility**;
17. **Phase 2 compatibility** for branch, checkpoint, rollback, rollout, and
    MCTS;
18. **Unproven assumptions and evidence still required**;
19. **Minimal implementation order**;
20. **Risks and falsification criteria**; and
21. **Final recommendation**, including whether Phase 1 implementation can
    proceed or remains blocked.

Place source links and absolute local file references next to the claims they
support.

## Completion condition

The examination is complete only when:

- the StreamCDC and SeqCDC claims are checked against the required task and
  pinned sources;
- StreamCDC and SeqCDC both have explicit hard-gate outcomes;
- each survivor has a complete score and confidence multiplier;
- exactly one of StreamCDC or SeqCDC is recommended unless both are
  disqualified;
- the selected design preserves the current LayerStack operation surface;
- large-file streaming remains bounded without retaining returned chunks;
- no SQLite, external setup, external operational dependency, or new privilege
  is required;
- the selected design has an explicit Phase 2 compatibility judgment;
- time, temporary-space, settled-space, and bounded-memory behavior are
  explicit;
- missing source evidence and contradictions are visible;
- no estimate is presented as a proven result; and
- no product implementation was changed.
