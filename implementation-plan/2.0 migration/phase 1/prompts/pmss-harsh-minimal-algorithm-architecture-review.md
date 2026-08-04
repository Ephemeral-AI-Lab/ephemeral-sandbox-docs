# PMSS harsh minimal-algorithm and architecture review prompt

Use this prompt in a fresh Codex task to review the proposed **Portable Merkle
State Store (PMSS)**. This is a hostile, read-only design audit. Do not protect
the proposal, preserve terminology for politeness, or assume that an existing
algorithm, method, field, namespace, record, cache, index, transition, or
component deserves to survive.

## Mission

Determine whether PMSS is the smallest correct storage architecture that can
meet its durability, concurrency, performance, disk-space, and memory bounds.
Find and remove every redundant concept. Then verify that the surviving
algorithms and pseudocode agree exactly with the accepted architecture and API
contracts.

The desired outcome is not a long list of possible improvements. It is one
decisive design:

1. the minimum number of authorities, components, namespaces, methods, fields,
   durable records, algorithms, indexes, passes, synchronization barriers,
   allocations, FDs, and terms needed for correctness;
2. the best defensible time and physical-space complexity under cold-cache,
   restart, concurrent-session, concurrent-publication, fork, checkpoint,
   rollback, materialization, hot-edit, and exact-GC workloads; and
3. a mechanically checkable mapping from every public API effect to the exact
   architecture authority and algorithm that implements it.

Prefer deletion over abstraction, fusion over duplicated machinery, and a
closed fixed format over a general framework. However, do not delete a safety
mechanism merely because its purpose is rare. Every deletion must preserve
crash consistency, exact reachability, reader safety, quota accounting,
idempotency, and conflict semantics.

## Review stance: less is more

> [!danger] Preservation is not the default
> Treat the current design as evidence, not as an asset that must be protected.
> Sunk implementation cost, document volume, familiar terminology, and prior
> agreement do not justify keeping anything. The burden of proof is on every
> surviving algorithm, method, field, record, state, round trip, pass, lock,
> sync, buffer, index, component, and abstraction boundary.

Be bold. A destructive **proposal** is acceptable—and preferred when it
produces a materially smaller or faster correct system. You may recommend
deleting or replacing whole algorithms, component boundaries, schemas,
physical formats, commit choreography, internal APIs, public method groupings,
or the overall architecture. You may conclude that PMSS itself is the wrong
shape. The audit remains read-only: “destructive” authorizes a design proposal,
not destructive repository, data, or infrastructure actions.

Do not give the incumbent design a compatibility advantage merely because it
is already written. Construct a clean-sheet minimum design that preserves the
required external outcomes and hard safety/resource bounds, then compare PMSS
against it. If the incumbent wins, prove why. If a smaller design wins, say so
directly and recommend replacement rather than disguising it as an incremental
refactor.

Apply these priorities in order:

1. preserve acknowledged-state durability, crash consistency, exact
   reachability, isolation, deterministic conflict semantics, reader safety,
   quota correctness, fail-closed behavior, and the hard memory/space bounds;
2. remove independent authorities, durable states, recovery branches, and
   concurrency interleavings;
3. minimize peak physical bytes, retained physical bytes, inodes, managed
   memory, cgroup memory, FDs, workers, queues, and temporary amplification;
4. minimize critical-path API/service round trips, Store calls, data passes,
   sorts, random reads, checksums, allocations, copies, locks, fsyncs,
   dirsyncs, and reader-drain boundaries; and
5. only then optimize abstractions, naming, extensibility, or code elegance.

Use Pareto reasoning when time, space, and simplicity trade off. A replacement
must either dominate the incumbent or state the exact regression bought by
each improvement. “Cleaner,” “more flexible,” “more modular,” and “future
proof” have zero weight unless they delete measurable state or work. Moving
complexity into a helper, background job, kernel cache, filesystem behavior,
allocator, database, or new abstraction is not a reduction.

For any proposal that changes an accepted contract or public behavior, label
it `AUTHORITY CHANGE` or `BREAKING API CHANGE`; show the complete propagated
architecture/schema/API/pseudocode replacement, compatibility and migration
plan, crash-safe cutover, rollback boundary, before/after complexity, and
benchmark that could falsify the claimed gain. Do not silently violate an
accepted contract. Conversely, do not use “accepted” as a reason to withhold a
superior destructive proposal.

## Repositories and authority

Product repository:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`

Design repository:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs`

Read the local `AGENTS.md` and `CLAUDE.md` files before examining code or
documents.

The accepted design set is exactly these ten files:

1. `implementation-plan/2.0 migration/system-design/index.md`
2. `implementation-plan/2.0 migration/system-design/system_requirements.md`
3. `implementation-plan/2.0 migration/system-design/api_methods.md`
4. `implementation-plan/2.0 migration/system-design/architecture/overall_architecture.md`
5. `implementation-plan/2.0 migration/system-design/architecture/mpla_demonstrations.md`
6. `implementation-plan/2.0 migration/system-design/components/backend_adapters.md`
7. `implementation-plan/2.0 migration/system-design/components/canonical_state.md`
8. `implementation-plan/2.0 migration/system-design/components/durable_store.md`
9. `implementation-plan/2.0 migration/system-design/components/lifecycle_engine.md`
10. `implementation-plan/2.0 migration/system-design/components/workspace_engine.md`

The algorithm workbook is:

`implementation-plan/2.0 migration/pmss_algorithms.md`

Obsidian navigation: [[implementation-plan/2.0 migration/system-design/index|PMSS accepted system design]],
[[implementation-plan/2.0 migration/system-design/api_methods|PMSS API methods]],
and [[implementation-plan/2.0 migration/pmss_algorithms|PMSS algorithm workbook]].

The ten accepted files own normative behavior. The workbook is a
non-normative implementation and qualification aid and must not silently
invent a conflicting requirement. When two accepted files conflict, report a
design defect; do not choose whichever wording is convenient.

Read all eleven files completely. Follow every link needed to verify a claim.
Inspect relevant current product code and Stage 4.6 evidence when a design
claim depends on existing behavior or a benchmark. Distinguish measured facts,
analytical bounds, proposed targets, and hypotheses.

## Non-negotiable requirements

- No LayerStack, logical layer history, squash, autosquash, or history-depth
  lookup in the production design. Legacy layers may exist only at an explicit
  import boundary.
- Treat squash as the model for architectural obsolescence: it was useful only
  because the former layer representation created depth. Search for every
  analogous legacy step, operation, method, state, component, record, mount or
  remount transition whose original cause disappeared after the move to
  complete content-addressed states. Delete it unless a current PMSS invariant
  independently requires it. Moving an obsolete operation to maintenance or
  renaming it does not count as deletion.
- A published state is a complete immutable canonical state identified by
  `StateId`; publication moves one sandbox head with strict optimistic
  concurrency control.
- Fork and checkpoint must not copy payload. Rollback must move a reference,
  not replay historical deltas.
- Same-line and same-chunk hot edits must not create an unbounded decode chain.
- Semantic retention and physical custody must remain separate and exact.
- No persistent refcount, persistent application cache, global resident index,
  repository-sized memory set, full-tree buffer, unbounded queue, unbounded
  worker pool, or hidden database/LSM/WAL machinery.
- Storage-managed memory has a hard `8 MiB` shared-service ceiling, a normal
  target of `4 MiB`, a per-sandbox concurrent claim no greater than `4 MiB`
  (a ceiling, not a reservation), and a heavy-operation claim no greater than
  `2 MiB`. The shared PMSS service has `memory.high=64 MiB`, exact
  `memory.max=96 MiB`, and swap disabled; this one limit covers all concurrent
  sandbox/session storage work and therefore is stricter than multiplying
  96 MiB by sandbox count. Untrusted runtime memory remains separately bounded
  by each sandbox's finite parent cgroup.
- Every byte and inode must be charged before allocation. Root deletion gives
  no speculative capacity credit. Physical credit occurs only after exact
  proof, safe reader drain, unlink, and parent-directory synchronization.
- Multiple sandboxes, workspace sessions, publications, materializations,
  checkpoints, forks, rollbacks, crashes, retries, and GC triggers must be
  safe under the stated finite admission bounds.
- Memory safety and speed must hold under a substantial admitted load of
  parallel active workspace sessions, not only in isolated microbenchmarks.
  There must be no per-session resident Store cache, idle-session buffer/FD,
  unbounded task fanout, allocator-driven limit, head-of-line blocking hidden
  behind a global lock, or maintenance starvation. Aggregate claims must fit
  before dispatch, and overload must return a typed bounded outcome.
- Acknowledged state must never silently roll back during recovery.
- Unsupported or unqualified environmental behavior must fail closed.
- The `<=5.8136209 ms` P4-compatible sparse-publication result is an unmeasured
  10x target relative to the Stage 4.6 candidate, not an existing SLA.

## Mandatory pass/fail gates

These gates override a merely favorable overall assessment. A design that
fails any gate is not minimal and is not production-ready.

### Gate A — architecture-shift deletion sweep

Begin with the explicit deletion of squash. The old raw-file/layer
representation created a depth problem, so it needed squash and remount. PMSS
publishes complete immutable states and does not have that problem. Apply the
same causal test to every surviving step and component: **what current PMSS
invariant—not historical implementation shape—requires it?**

At minimum, issue an individual verdict for:

- LayerStack, parent/version chains, layer lookup, layer-depth state and layer
  GC;
- squash, autosquash, squash-triggered remount, lower-carrier rebuild and any
  renamed physical operation that still has logical squash semantics;
- durable base-locator pins, relocation records/streams, a third relocation
  sort and per-publisher immovability;
- a prepared-locator vector, a second Delta-base/dependency vector, an in-RAM
  publication object set, or any duplicate of the one Build-owned sorted disk
  cursor;
- a second HEAD/root selector, PackCatalog, persistent refcount, tombstone,
  WAL, MVCC, LSM level, persistent cache or recovery-election path;
- separate normalization/repack write engines, or a rewrite invocation that
  mixes policies and therefore needs a second progress/accounting model;
- background cleanup, detached owner disposal, retry/catch-up logs, implicit
  rebase or merge;
- adapter open/close/remount phases, durable session states, internal methods
  and result fields that correspond to no public effect, crash cut or live
  invariant; and
- duplicate terms that name the same identity, root, owner, cursor, selector,
  physical rewrite or semantic-retention concept.

For every item kept, identify the exact invariant and give a concrete failing
execution after deletion. If neither exists, mark it `DELETE`; moving it,
renaming it or hiding it behind an abstraction fails this gate. Report the
before/after count of components, methods, fields, namespaces, algorithms,
passes, scratch files, synchronization barriers, FDs and durable states.

### Gate B — parallel-load memory, speed and storage safety

Prove the aggregate system, not a single happy-path operation. The admission
proof must be multidimensional and simultaneous across managed bytes, workers,
FDs, OwnerSlots, ReadSlots, queue descriptors, disk bytes, inodes, maintenance
reserve and per-sandbox attribution. A worker count is not permission to admit
that many maximum-size heavy claims. In particular, four 2-MiB heavy buffers
cannot coexist with other live managed partitions under an 8-MiB ceiling; show
the actual maximum admitted combination. At most two simultaneous 4-MiB
per-sandbox claims may fit globally, and a 4-MiB sandbox bound is never
pre-reserved for every sandbox.

Measure and enforce:

```text
M_service_current = baseline RSS
                  + thread stacks
                  + allocator arenas and helper/runtime memory
                  + managed buffers
                  + page cache and writeback
                  + dentry and inode slab

M_service_current <= 64 MiB under every qualified workload
M_service_current <  96 MiB at every instant
swap = 0
```

Freeze thread count and stack size, allocator configuration, helper-process
inventory, queue capacity, every buffer/slab, FD class and kernel-memory
charging behavior. Test 1/4/8/16/32/64 active sessions with mixed capture,
publication, materialization, read/export, checkpoint, fork, rollback,
conflict cleanup and one maintenance epoch. Include hot same-line edits,
maximal candidate cursors, slow readers, crashes and overload. For each point,
report publication throughput and p50/p95/p99/max latency, serialized-gate hold
time, queue wait, maintenance pause, fairness, RSS/cgroup peak, managed-byte
peak, FDs, disk/inode high-water, temporary amplification and post-cleanup
plateau. Idle sessions must retain no worker, buffer, FD, slot, cursor, cache or
permit. Cancellation, error, conflict and restart must return every resource to
the justified steady plateau after the required join/sync boundary.

This gate fails if the proof adds per-session caches, repository-sized memory,
unbounded tasks, hidden allocator growth, uncharged page cache, global-lock
head-of-line blocking, maintenance starvation, speculative storage credit, or
if speed is shown only by isolated microbenchmarks. It also fails if the 10x
publication goal is labeled achieved without a comparable measured workload.

### Gate C — algorithm/architecture/API identity

Verify these exact cross-document contracts or provide one fully propagated,
strictly smaller replacement:

- `StateId = ObjectId(FilesystemRoot)`; there is no StateManifest wrapper or
  version chain.
- An accepted session creation freezes one internal `ActorId[32]`; capture,
  metadata ownership and C3 use only that session field, publish retries never
  use the ambient caller, and Terminal rows drop it.
- Candidate handoff is one Build-owned sorted disk cursor containing
  `(ObjectId, REUSE | candidate locator)`; a conflict checks origin before
  opening it, and no locator/base vector survives alongside it.
- `HEAD` stores exactly
  `{type_tag,StoreSequence,ArenaId,committed_arena_length,checksum}`. For
  `P=16 KiB`, `CatalogRoot=(ArenaId,committed_arena_length-P)` is derived after
  checked alignment and lower-bound validation. Every StoreSequence-advancing
  sparse or dense commit emits exactly one fresh root as the last committed
  page; no selected trailer, padding, hole or later page follows it, and new
  writes begin at selected committed length rather than physical EOF.
- The 16 `OwnerSlot` keys are static lanes, not dynamically purposed rows:
  slot `0` is maintenance-only `Empty | Build {owner_nonce}` and slots `1..15`
  are foreground-only `Empty | Build {owner_nonce} | AdapterClose`. Existing
  foreground builders may close staged work during the maintenance fence and
  then wait with zero buffers, FDs and workers; no purpose field or borrowed
  maintenance lane exists.
- Physical closure uses exact `DeltaEdgeV1` 36-byte records
  `{base_id[32],target_rank:u32}`, `PackCensusV1` 72-byte records and
  `VictimV1` 40-byte records. All Catalog/object counts and basis-local ranks
  fit checked `u32`; aggregate byte arithmetic is checked wide. A dead Full
  base with one live Delta target is normalized; a dead base shared by at
  least two live Delta targets remains an anchor when that is frame-space
  beneficial. There is no relocation record, relocation stream or third sort.
- A pack is footerless: an exact eight-byte `SegmentHeaderV1=b"PMSSPK1\0"`
  followed by one or more 34-byte
  `{ObjectId[32],stored_len_minus_one:u16}` headers and nonempty payloads.
  `ObjectCatalog` is the sole Full/Delta codec and locator authority;
  `P_pack_committed_max=64 MiB` includes the signature and frames.
- If final publication finds that a classified REUSE vanished or a Delta Full
  base disappeared, it performs no local repair. It leaves the gate, retains
  the exact Build and workspace fence, joins producers/readers,
  deletes+dirsyncs the complete cursor, candidate packs and scratch, and
  reruns both capture passes once against the latest Catalog. A second
  invalidation aborts in order and returns transport `RetryLater` with the
  session `ACTIVE`.
- Origin-match publication makes one complete validation pass before installing
  any candidate pack, then one sequential late-dedup/install pass. REUSE keeps
  a valid current row; a candidate keeps a valid current exact row or selects
  its staged row; an existing Full is not replaced by a staged Delta. Candidate
  segments occupy contiguous cursor intervals so only one constant selected
  count is needed. No payload I/O occurs in the final gate.
- Selected-state validation already proves hardlink membership. Portable
  materialization is `Theta(B+F)` with no alias sort or scratch map: canonical
  path order plus a same-filesystem hidden control anchor derived from each
  `HardlinkGroup` ObjectId supplies the `O_EXCL` first-occurrence test. Anchors
  are unlinked and their directory synchronized before activation; a crash
  destroys the incomplete allocation.
- Exact replay uses only 16 `ReceiptControl(lane)->next_sequence:u64` rows and
  1,024 modulo `ReceiptSlot(lane,sequence mod 64)` rows containing
  `{request_digest[32],bounded_exact_result}`. A slot stores no sequence,
  generation, low-water mark or repeated lane. The S2 effect, slot and next
  sequence advance atomically.
- Trace block authentication binds format, exact `MaintenanceBasis`,
  `N_object`, phase, level/type, block index, valid-tail length and payload;
  every phase transition rewrites every block digest.
- One `REWRITE_BATCH` invocation selects exactly one of `DEAD_REPACK`,
  `EMERGENCY_REPACK`, `CONSOLIDATE` or `NORMALIZE`; policy mixing is forbidden.
- Maintenance selects its Build before basis capture and fences every
  non-maintenance S2 mutation across trace, sorting, rewrite, dense validation
  and selection. Foreground publication does not CAS unrelated global Catalog
  identity and honestly accounts for candidate-size-dependent gate work.
- Lifecycle faces only `open_read`, `stage_objects` and `commit`; Store owns
  `maintain` and startup `recover`. Recovery keeps all readiness and Build
  charges closed until it validates selected state, performs the complete
  installed-pack census, unlinks+dirsyncs zero-selected orphans, cleans fixed
  directories, and only then exact-clears Builds and releases charges.

A disagreement among architecture, schema, API method contract and pseudocode
fails this gate even if each version would be plausible in isolation.

The current accepted design is the baseline authority, not an untouchable
solution. Audit all public methods and every named contract above for
redundancy too. A strictly smaller replacement may change them only as an
explicit, fully propagated `AUTHORITY CHANGE` or `BREAKING API CHANGE` proposal
with equivalent-or-better external semantics, migration, crash, concurrency,
space, memory, and performance proofs. Until such a proposal is accepted, the
current contract remains normative.

### Gate D — clean-sheet and destructive-replacement challenge

Produce the smallest clean-sheet design that could satisfy the same external
outcomes, safety properties, strict storage bounds, and shared `96 MiB` cgroup
ceiling. It may reuse none, some, or all of PMSS. Compare it mechanically with
the incumbent; do not merely sketch it.

At minimum, challenge whether the system truly needs:

- all four current components and every boundary call between them;
- all six custom mechanisms, or whether a mechanism can be deleted, fused,
  replaced by a simpler primitive, or proved unnecessary;
- every lifecycle/runtime public method as a distinct operation rather than a
  redundant view or composition of another atomic effect;
- all three Store-port operations and each call/return field;
- both sparse and dense mutation paths, every capture/validation pass, every
  sort, every owner/read slot type, and every recovery phase;
- every persistent namespace, row variant, sequence, digest, checksum,
  revision, identifier, and derived locator;
- every fsync/dirsync, lock acquisition, reader drain, retry loop, cleanup
  transition, temporary file, queue hop, and process boundary; and
- every maintenance policy and whether it exists only to compensate for a
  representation choice that should itself be replaced.

For each candidate redesign, provide a **destructive replacement card**:

1. exact current items removed;
2. exact minimal replacement, including on-disk and in-memory state;
3. preserved and intentionally changed external behavior;
4. correctness argument and counterexample search;
5. crash cuts, concurrency interleavings, recovery, GC, and migration path;
6. before/after methods, fields, components, durable states, calls, passes,
   sorts, syncs, locks, bytes, inodes, FDs, workers, and peak memory;
7. worst-case and amortized time, I/O, physical-space, and memory complexity;
8. predicted latency/throughput/storage gain, with source of the gain; and
9. a benchmark or model-check result that would reject the redesign.

Rank destructive candidates by net deletion and demonstrated improvement, not
novelty. Bold does not mean speculative: reject a replacement that merely
trades familiar complexity for more concepts, undocumented filesystem magic,
unbounded memory, probabilistic cleanup, or weaker durability. This gate fails
if the review considers only local edits, assumes all major components must
survive, or refuses to challenge a design solely because it is accepted or
implemented.

## Audit posture

Assume the design is over-engineered until each item proves otherwise. For
every named thing, ask:

1. What exact invariant fails if it is deleted?
2. Can an existing item own the same responsibility without ambiguity?
3. Can the field be derived from already authenticated bytes or a captured
   root instead of stored?
4. Does the field encode logical identity, selected lookup state, temporary
   custody, or merely a cache? Reject mixed roles.
5. Is the mechanism required in the steady state, or only for migration,
   observability, or explanation?
6. Does it reduce total work, or merely move work into background maintenance?
7. Does it create a new concurrency interleaving, recovery state, allocation,
   inode, FD, sort pass, random read, checksum, or synchronization barrier?
8. Is its worst case bounded by a frozen finite constant and admitted before
   use?
9. Is there a standard primitive that provides exactly the needed semantics
   with less custom state?
10. Can two sequential algorithms reuse the same bounded scratch, owner slot,
    cursor, or commit authority without increasing peak resources?
11. How many API/service/Store round trips, passes, sorts, copies, lock
    acquisitions, fsyncs, dirsyncs, and reader drains does it add to each
    affected critical path?
12. Does an abstraction delete a state or transition, or merely give the same
    complexity another name?
13. Is this mechanism repairing a consequence of a representation choice that
    should itself be removed?
14. Would a clean-sheet design invent this item today under the same hard
    bounds?
15. Can the entire containing algorithm, API method, component, or storage
    representation be replaced more cheaply than simplifying this item?

Do not accept “future flexibility,” “clean separation,” “common practice,” or
“may be useful” as justification. Require a concrete invariant, failure mode,
or measured benefit. Do not soften a finding to preserve prior work. Do not
use a new abstraction to conceal a deletion opportunity.

## Required review

### 1. Minimality ledger

Enumerate every:

- component and cross-cutting service;
- public and internal method;
- Catalog namespace and row variant;
- canonical object kind and child edge;
- durable selector, sequence, revision, identity, locator, and ownership field;
- pack signature/record field and physical encoding, plus a proof that no
  footer/trailer/index field survives;
- volatile slot, permit, cursor, queue, worker, buffer, FD class, scratch file,
  arena, and recovery token;
- foreground and maintenance algorithm; and
- user-facing architectural term.

For each item, return exactly one verdict:

- `KEEP — irreducible`: state the invariant that requires it;
- `DERIVE`: identify the authenticated source and delete the stored field;
- `FUSE`: identify the surviving owner/mechanism;
- `INLINE`: remove a method or abstraction boundary with no semantic value;
- `RENAME`: only when the current name causes a logical/physical ambiguity;
- `MIGRATION-ONLY`: remove it from the production steady state; or
- `DELETE`: explain why no invariant depends on it.

Treat a `KEEP` without an explicit counterexample after deletion as a failed
review. Include before/after counts and the estimated code/format/pass/resource
reduction. Flag every field that is duplicated across canonical bytes,
Catalog rows, OwnerSlot custody, pack framing, and API results.

Inventory public methods with the same burden of proof as internal methods. If
two methods share one transition and differ only by client-side composition,
return shape, naming, or a redundant round trip, propose the smaller API. Mark
any change to the accepted public surface as `BREAKING API CHANGE`; specify the
replacement call, preserved linearization semantics, compatibility shim if one
is warranted, and the date or condition on which that shim must be deleted.

Create a separate **obsolete-operation sweep**. Start from the former
LayerStack lifecycle—publish layer, stack lookup, squash, remount, lower-carrier
rebuild, autosquash scheduling, layer-depth metrics, and layer GC—and map each
step to `DELETED`, `LEGACY-IMPORT-ONLY`, or one precisely justified PMSS
replacement. Then repeat the exercise for every current PMSS operation: ask
whether it repairs a property of the old representation rather than a property
of complete immutable states. Report any semantic no-op or duplicated
publication/materialization/maintenance transition.

### 2. Algorithm-by-algorithm hostile review

Review canonical construction, chunking, attribution tiling, sparse Catalog
mutation, dense Catalog build, publication, S3 Delta selection/decode,
materialization, semantic trace, physical closure, normalization, victim
selection, repack, retirement, receipt replay, recovery, checkpoint, fork,
rollback, session close, and root deletion.

For each algorithm:

1. state its exact inputs, outputs, preconditions, invariant, commit point,
   crash state, retry behavior, and owner;
2. give worst-case and amortized time, byte-I/O, memory, disk-scratch, inode,
   FD, synchronization, and pass complexity using defined variables;
3. identify hidden work such as canonical verification, base reconstruction,
   allocation rounding, directory enumeration, dense validation, page copies,
   checksums, fsyncs, and reader drain;
4. test whether one pass, sort, temporary record, file, or durable transition
   can be eliminated;
5. show whether the algorithm is asymptotically optimal or provide a lower
   bound/counterexample;
6. give the smallest correct pseudocode after proposed deletions; and
7. return `KEEP`, `SIMPLIFY`, `REPLACE`, or `DELETE`.

Also ask whether the algorithm should exist at all. Do not optimize a pass,
sort, index, cache, GC phase, or recovery transition before testing whether a
different representation deletes its cause. A `REPLACE` verdict may discard
the current data model and all associated pseudocode when the replacement has
a complete proof and materially improves the Pareto frontier.

Reject pseudocode that refers to an undefined input, an unproduced ordering, a
second authority, a hidden in-memory set, an unbounded directory listing, a
locator captured from a different Catalog root, or a cleanup step that can race
a reader or owner.

### 3. Space-complexity audit

Prove peak simultaneous use, not individual local maxima. Account for:

- selected Catalog and packs;
- both arenas during replacement;
- owner/staging/orphan outputs;
- adapter-private workspaces;
- semantic trace;
- every external-sort generation and control file;
- replacement-header rescans and any proposed relocation metadata (whose
  default verdict is deletion);
- replacement pack and framing/allocation rounding;
- HEAD/root-control output;
- retirement debt and old-reader epochs;
- filesystem metadata and inodes; and
- all memory inside the cgroup, distinguishing managed allocations from RSS,
  stacks, allocator arenas, page cache, dentries, and inode slab.

Construct adversarial storage sequences: one-byte edits to one chunk, edits
that shift chunk boundaries, alternating incompressible/compressible content,
many tiny files, many empty files, sparse files, hard links, metadata-only
edits, checkpoint-per-publish, session-per-state, fork fanout, head ABA,
abandoned candidates, crash before/after every sync boundary, all-live tiny
packs, one live frame per pack, one live Delta target per dead base, many live
Delta targets sharing one base, rapidly changing bases, and old readers during
repack.

For every sequence, give the tight retained canonical-byte, selected physical-
byte, temporary-byte, inode, and managed-memory bounds. If a proposed bound
depends on a symbolic deployment constant, list that constant and the exact
qualification measurement needed before production.

### 4. Time-complexity and latency audit

Separate:

- foreground publication preparation;
- the serialized final commit gate;
- exact read/decode;
- materialization;
- checkpoint/fork/rollback;
- semantic trace;
- closure/census ordering;
- dense Auxiliary validation;
- normalization/repack copy;
- safe reader drain; and
- synchronized physical deletion.

Provide a table with worst-case CPU, random I/O, sequential byte-I/O, sort
passes, fsync/dirsync barriers, lock duration, and concurrency effect. Identify
which work is payload-dependent, changed-object-dependent, object-count-
dependent, pack-count-dependent, or fixed. Do not call `Theta(N)` work
“bounded” without also stating `N` and its admitted maximum.

For every performance target, supply:

- exact workload/fixture;
- baseline and proposed comparator;
- mathematical threshold;
- mechanism expected to create the improvement;
- possible regression mechanism;
- measurement status (`MEASURED`, `ANALYTICAL`, `TARGET`, or `HYPOTHESIS`);
- benchmark method and sample count; and
- reject threshold.

Do not extrapolate the Stage 4.6 sparse fixture to payload-bearing or
metadata-heavy publication. Do not claim a 10x result before measurement.

In addition to single-operation cases, analyze admitted parallel-load matrices
for at least 1, 4, 8, 16, 32, and 64 active workspace sessions, constrained by
the actual worker/OwnerSlot/ReadSlot/queue/FD/memory vector. Mix publication,
materialization, read/list/export, checkpoints, rollbacks, and one maintenance
epoch. For each load level report aggregate managed bytes, complete cgroup RSS,
FDs, runnable/queued tasks, queue wait, throughput, p50/p95/p99/max latency,
final-commit lock hold time, fairness/starvation behavior, and cleanup plateau.
Show that idle sessions consume no worker, buffer, FD, ReadSlot, or Store cache.
Require backpressure before allocation and distinguish expected queueing from a
memory leak or global-lock scalability failure.

Add a **critical-path round-trip ledger** for every public operation. Count, in
execution order, client/service crossings, component calls, Store-port calls,
cursor handoffs, full-data passes, sorts, random lookups, lock acquisitions,
atomic commits, fsyncs, dirsyncs, retries, reader drains, and queue transitions.
Give before/after counts for each recommendation and identify which calls can
be fused, inlined, batched, derived, or deleted without moving the same work to
another phase.

### 5. Architecture and API consistency

Build three bidirectional matrices:

1. public API method -> lifecycle transition -> canonical operation -> Store
   read/write -> adapter operation -> permit/resources -> durable rows changed;
2. durable field/row -> sole owning component -> creating method -> consuming
   method -> deleting/retiring method -> recovery rule; and
3. algorithm/pseudocode step -> accepted normative section -> required input ->
   produced output -> next consumer.

Report any orphan method, unowned field, duplicated authority, algorithm with
no API caller, API effect with no durable transition, pseudocode input that no
prior step produces, or accepted rule missing from the workbook.

Explicitly verify:

- `StateId`, `HeadRevision`, `StoreSequence`, `ArenaId`, `SegmentId`, and
  `ObjectId` are not interchangeable;
- publication, content-identical publication, concurrent publication, receipt
  replay, fork, checkpoint, rollback, session destruction, and checkpoint
  deletion each have one unambiguous linearization point;
- a Delta depends on a Full base without embedding a physical locator that
  repack can invalidate;
- exact GC distinguishes semantic roots, selected physical dependencies,
  owner custody, and old-reader epoch custody;
- dead ObjectCatalog rows are omitted from the dense replacement while exact
  anchor-only Full rows required by selected Deltas remain resolvable;
- materialization creates only adapter-private output and cannot accidentally
  register it as a Store PackSegment;
- ReadSlot expiry cannot clear an epoch while a cursor or FD can still read an
  old pack; and
- no diagram, demonstration, or workbook section creates a fifth component,
  ninth Catalog namespace, PackCatalog, layer, squash path, or fallback HEAD.

### 6. Concurrency, crash, and garbage-collection model checking

For each mutation, enumerate interleavings with:

- a second publication from the same origin;
- publication to another sandbox sharing objects;
- checkpoint creation/deletion;
- fork and rollback;
- materialization/read under an expiring ReadSlot;
- S3 candidate preparation with Build-owned custody and a transient ReadSlot;
- exact trace and Auxiliary construction;
- maintenance final commit;
- pack unlink; and
- process or host crash at every durability boundary.

Prove no execution loses acknowledged state, deletes a semantic or physical
root, publishes a dangling Delta, reuses stale capacity credit, leaks an owner
allocation indefinitely, or permits ABA through equality of content IDs.

Use small executable state-model tests if practical. Keep them temporary unless
the user separately authorizes production test changes.

### 7. Whole-system reduction decision

Compare at least these three outcomes:

1. keep the current architecture;
2. apply the best surgical deletion/fusion set; and
3. adopt the best destructive clean-sheet replacement.

For each, provide exact counts and bounds—not adjectives—for components,
authorities, public/internal methods, persistent fields/rows, algorithms,
recovery states, critical-path round trips, full passes, sort passes, sync
barriers, lock boundaries, peak/steady physical bytes, temporary amplification,
inodes, FDs, managed memory, cgroup peak, throughput, and latency. Include
migration cost and the duration of any dual-format or compatibility state.

Select one outcome. The recommendation must minimize total system complexity
subject to correctness and the hard resource limits; it must not default to
the least disruptive option. If a destructive replacement is best, recommend
it plainly. If it is not best, identify the quantified cost or invariant that
defeats it.

## Required output

Lead with one verdict:

- `ACCEPT AS MINIMAL`;
- `ACCEPT AFTER DELETIONS`;
- `REDESIGN REQUIRED`; or
- `REJECT`.

Then provide, in this order:

1. a ranked `P0/P1/P2` defect list with exact file/line evidence;
2. a one-page minimum-design verdict stating `KEEP CURRENT`,
   `SURGICAL REDUCTION`, or `DESTRUCTIVE REPLACEMENT`;
3. a deletion/fusion/derivation table with before/after counts;
4. ranked destructive replacement cards and the clean-sheet comparison;
5. the smallest corrected authority graph and durable schema;
6. corrected minimal pseudocode for every affected algorithm;
7. complete time, byte-I/O, memory, scratch-disk, inode, FD, pass, sync,
   round-trip, lock, and recovery-state complexity tables;
8. the critical-path round-trip ledger with before/after counts;
9. architecture/API/algorithm consistency matrices;
10. adversarial no-squash storage-growth results;
11. an obsolete-operation deletion map and parallel-workspace load matrix;
12. an expected-performance table separating measurements, analytical bounds,
    targets, hypotheses, and the exact mechanism responsible for each gain;
13. the remaining production-qualification blockers and exact experiments;
14. a final net-reduction scorecard for the three whole-system outcomes; and
15. a final list titled `What we can delete now` containing only safe,
    immediately actionable removals.

Every finding must include a precise repair. Avoid vague advice such as
“simplify,” “optimize,” “consider,” or “add tests.” State what to delete or
change, why it is correct, the resulting complexity, and the evidence needed.
Every recommended addition must identify what larger cost or mechanism it
deletes; otherwise presume the addition is rejected. Every retained item must
pay rent with a named invariant and concrete deletion counterexample.

Do not modify production code or accepted documents during the audit. Put any
suggested rewrite in the report or a separate patch proposal so the owner can
review it. Do not declare production readiness while a format constant,
aggregate FD inventory, peak-disk equation, cgroup measurement, crash cut, or
performance target remains unqualified.
