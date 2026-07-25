# Stage 05 E2E plan — retention, verified replacement, and retirement

Status: `NOT_RUN / OPEN`. No row is a pass until it runs against the implemented
revision and links the raw artifact.

Normative dependencies:

- [Stage 05 specification](spec.md)
- [LayerStack storage contract](../layerstack_storage_contract.md)
- [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

## 1. Harness and evidence contract

Run each applicable case with process kill, restart, short write, failed write/fsync/
rename/parent-fsync, response loss, corruption, cancellation, panic, timeout, and
`ENOSPC`. A case record contains the exact command, revision, deterministic corpus
hash, seed, failpoint, machine/kernel/filesystem/architecture, configuration and hard
caps, expected and observed durable state, resource high-water marks, cleanup result,
raw artifact path, and `PASS`/`FAIL`/`OPEN`.

Fault injection must identify every persistence boundary in:

- common `Building → Ready → Published → Terminal` replacement;
- GC `Marking ↔ Closing → Complete` and abort;
- retirement `Pending → Deleting → Done`;
- locator and materialization `CURRENT`;
- root-log append and drain; and
- operation recovery/cleanup.

Unknown, corrupt, missing, truncated, overflowed, or checksum-invalid evidence must
retain. Tests must never use mtime, directory contents, clock movement, or lease expiry
alone as deletion authority.

## 2. Retention roots and strong edges

Construct content/attribution roots retained independently by heads, checkpoints,
pins, exact holds, prepared/committing operations, active materializations, migration
operations, and existing-v1 source protection. Remove each seed in every order.

Assert:

- content and attribution graphs are both traversed;
- manifest/page/segment/chunk edges are strong;
- parent/base/provenance ancestry, carrier membership, and locator generation are not
  logical strong edges;
- an object remains readable until its last real root is removed, it is absent from
  two consecutive complete GC observations, and its final typed predicate passes;
- checkpoint attribution/blame survives packing, evacuation, GC, squash, and restart;
- clean checkpoint/branch/frontier refs copy no payload; and
- no `refs/legacy` class exists.

## 3. Two-phase root admission and concurrent GC

For heads, checkpoints, pins, prepared/committing operations, materializations, and a
simulated Stage 06 authority root, inject at:

1. before provisional registration;
2. after the provisional root-log fsync but before graph validation;
3. during bounded graph validation;
4. after validation while the GC fence changes;
5. after registration with the new fence but before visible ref/`CURRENT`/`CONTROL`;
6. after visibility but before response; and
7. while GC is `Closing` and while retirement holds the writer lock.

Assert that visibility occurs only after durable registration with the GC active at
the final commit. An abandoned provisional root causes conservative retention only.
A mutation racing `Closing` either returns the cycle to `Marking` or observes the
durably completed cycle. Ref deletion during mark may retain extra bytes but cannot
remove a newly reachable object.

Fill the 64 MiB root log. Admission must abort that GC under the writer lock and retain
its candidates before the mutation becomes visible; after the bounded deadline, an
unavailable admission resource returns `ResourceExhausted`. Test fence reuse and
restart so a stale generation cannot pass as the same active GC.

## 4. Disk-backed mark, sweep, and liveness

Use shallow, deeply shared, cyclic-invalid, mostly-live, and mostly-dead graphs whose
live set is larger than every tested RAM budget.

Assert:

- no resident all-live `HashSet`, map, vector, or queue;
- traversal is bounded and all typed edges are either marked or conservatively retain;
- external run fan-in, buffers, FDs, tasks, root log, candidate pages, and `W_gc` stay
  within their specified caps;
- cycle `n` records candidates but cannot delete them;
- only cycle `n+1`, complete after `n`, may submit an object absent from both marks;
- corrupt or incomplete mark/candidate/prior-cycle data cannot authorize retirement;
- sweep is paginated/sliced across `A` and restart resumes a checked cursor or aborts;
- objects blocked by roots, holds, selectors, operations, authority, corruption, or
  resource pressure report that exact reason; and
- after every legitimate blocker clears, bounded GC and ledger service reclaim the
  object and unexplained unreachable/unleased residue reaches zero.

Run overlapping holds across multiple GC cycles. Wall-clock reversal, long process
pause, stale lease evidence, or expiry without a fencing/recheck proof must not delete.

## 5. Common verified replacement, packs, and locators

Exercise packing, locator consolidation, and evacuation through the one common build
protocol:

- deterministic loose lookup without a locator entry;
- pack with mixed live/dead objects;
- crash before/after pack fsync, run fsync, `Ready`, locator `CURRENT`, `Published`,
  retirement handoff, and terminal cleanup;
- reader holding the exact old locator generation across `CURRENT`;
- fixed active-run count/encoded-byte cap and same-key waiter cap;
- corrupt/missing replacement with the old selector and source still usable;
- source evacuation when it is the only legacy/external locator;
- ABA attempt using a stale locator fence/generation; and
- cancellation/panic at every permit, buffer, FD, and output-ownership boundary.

A mixed pack is never retired while any live object lacks another selected usable
locator. A current or held locator generation retains every pack/run it names. Pack
build/consolidation does not add a second pointer or state family.

## 6. Singleton retirement ledger

Test loose objects, packs, locator runs, materialization generations, and approved
non-authoritative external carriers through the same ledger.

For each batch, inject before/after inventory fsync, every exact rename, both parent
fsyncs, durable `Deleting`, every unlink, destination-parent fsync, and `Done`.

| Durable state and observed paths | Required recovery |
| --- | --- |
| `Pending`; source present, destination absent | retain source; retry or withdraw eligibility |
| `Pending`; source absent, destination present | restore the exact destination to source and fsync |
| `Pending`; both present or both absent | stop deletion, retain what exists, report corruption |
| `Deleting`; destination present | resume only the recorded destination unlink |
| `Deleting`; destination absent | record `Done`; do not remove a reinstalled source |
| corrupt state or path outside allowed owner root | stop deletion; never infer a target |

Also assert:

- final recheck covers roots, operations, selectors, typed holds, active root log,
  authority/migration fence, and last-usable-carrier status;
- inventory is durable before the first rename;
- paths are normalized relative paths under pre-opened LayerStack directories;
- empty, `.`, `..`, symlink-following, glob, broad, and recursive targets are rejected;
- one batch is at most 1,024 paths/64 MiB and the ledger is at most 64 batches,
  65,536 paths, and 4 GiB renamed bytes;
- each writer-lock slice is at most 16 paths/64 KiB encoded inventory, rechecks
  eligibility after every intervening mutation, and adds no durable sub-state;
- a full ledger backpressures or returns `ResourceExhausted` without losing eligibility
  evidence;
- withdrawn eligibility leaves/restores the source; and
- LayerStack never scans or deletes `/eos/workspace`, `/eos/storage`, or
  `/eos/runtime`.

## 7. Materialization and squash retirement

Stage 04 builds and verifies the replacement; Stage 05 only applies generic holds and
retirement:

- run manual, depth, fragmentation, evacuation, and repair squash;
- prove the same `RootId`, logical tree, checkpoint, and attribution after restart;
- crash before/after generation fsync, materialization `CURRENT`, retirement handoff,
  and cleanup;
- keep old sessions on their exact leased generation while new sessions select the
  replacement;
- attempt stale-generation/ABA selection and reject it;
- enforce `G≤64` active/pinned generations and backpressure further admission; and
- prove no squash-specific Stage 05 state machine or worker exists.

## 8. Stage 06 and Stage 07 overlap

Simulate Stage 06 preparation, candidate cutover, rollback preparation, and `CONTROL`
switch during GC `Marking`, `Closing`, root-log saturation, final retirement recheck,
and restart. These mutations use the same two-phase admission and writer lock.
Stage 05 must retain every v1 source while rollback policy or a typed migration/source
hold requires it.

Simulate Stage 07 retirement authorization. Before `CONTROL` is durably
`candidate-retired` with `rollback_allowed=false`, every v1 path is ineligible. After
approval, Stage 07 may submit exact eligible subjects, but only the singleton Stage 05
ledger may rename/unlink them.

## 9. Rust memory safety and bounded ownership

Inventory every Stage 05 task, thread, worker, queue, channel, vector, map, set, cache,
permit, buffer, FD, mapping, lock, hold, cursor, retry, and temporary path. Assert the
specification caps and record high-water marks. The expected Stage 05 mapping and
`unsafe` inventory is zero.

Required validation:

- Miri-capable unit tests for parsers, ownership, and cancellation paths;
- Loom or deterministic models for writer-lock/root-admission/selector/retirement
  interleavings;
- supported address/thread/leak sanitizers;
- fuzzing of object, pack, locator, operation, GC-run, and retirement decoders;
- checked arithmetic and pre-allocation caps for every count, length, offset, and
  `offset + length`;
- forced panic/cancellation while holding each owned permit/buffer/FD/lock/hold;
- shutdown that stops admission, cancels, joins, and returns to bounded quiescence; and
- a long-lived repeated pack/GC/evacuation/squash/cancel/restart stress run with no
  detached task, `Arc` cycle, permit/FD/mapping/hold leak, or growing terminal registry.

## 10. Critical-scenario ledger

Each row must record visible logical state, retained physical copies, in-memory owners,
locks/holds, admission result, recovery action, maximum RAM/disk overlap, safety
reason, and eventual-reclamation result.

| ID | Scenario | Required result |
| --- | --- | --- |
| `S05-E01` | checkpoint during mark | registered before visibility; reachable graph retained |
| `S05-E02` | checkpoint between complete cycles | second observation/final recheck retains it |
| `S05-E03` | ref during final retirement rename | serializes on writer lock; missing graph cannot become visible |
| `S05-E04` | crash around locator `CURRENT` | complete old or complete new selector |
| `S05-E05` | corrupt locator replacement | reject replacement; source remains |
| `S05-E06` | mixed live/dead pack | no wholesale deletion without replacement |
| `S05-E07` | reader holds old locator | exact generation and carriers remain |
| `S05-E08` | evacuate only legacy locator | verified selected replacement precedes retirement |
| `S05-E09` | corrupt/incomplete mark data | cycle aborts and retains |
| `S05-E10` | crash around exact trash rename | `Pending` restores or `Deleting` resumes |
| `S05-E11` | squash with old sessions | old hold remains; new admissions use replacement |
| `S05-E12` | Stage 06 cutover preparation during GC | same admission fence; v1 remains protected |
| `S05-E13` | several incomplete operations on restart | paginated bounded recovery; no history-sized collection |
| `S05-E14` | disk full at every persistence boundary | old authority/source remains; bounded exact residue |
| `S05-E15` | holds overlap several GC cycles | no expiry-only deletion; reclaim after fenced release |
| `S05-E16` | cancellation/panic with owned resources | unwind releases or durably hands off every resource |
| `S05-E17` | malformed metadata requests allocation | reject before allocation/overflow |
| `S05-E18` | long churn across pack/GC/squash | caps hold; settled unexplained residue is zero |

## 11. Exit

All rows remain `OPEN` until implemented and executed. Destructive Stage 05 enablement
is `NO-GO` unless every safety scenario passes, every resource remains within its hard
cap, every crash/corruption case fails closed, liveness converges after blockers clear,
and the matched benchmark campaign records the required time and space passes.
