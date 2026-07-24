# Stage 05 E2E plan — physical lifecycle

Status: `NOT_RUN`.

## 1. Retention graph

Construct roots retained independently by heads, checkpoints, pins, leases, prepared
operations, active materializations, the active migration operation, and ordinary
existing-v1 source holds. Remove each seed in every order and prove objects remain
until the last real seed plus grace/final recheck. Parent/base provenance and expired
outcomes do not retain unselected history. Assert no `refs/legacy` class exists.

## 2. Concurrent GC barrier

At every mark/drain/closure/sweep/grace/final-delete failpoint concurrently:

- create/move/reset a head;
- create a checkpoint or MCTS frontier pin;
- prepare/commit a publication;
- activate/switch a materialization;
- renew/release a fenced lease;
- switch authority state in a simulated migration.

Visibility must occur only after durable seed registration. Any ambiguous generation
retains/restarts. No newly visible valid ref loses an object.

## 3. Disk-backed bounded marking

Use a live graph larger than the RSS budget. Assert:

- no resident all-live `HashSet`/map;
- external mark runs and typed direct-object seeds are complete;
- fixed run fan-in/buffers/FDs/tasks;
- bounded restart cursor/residue;
- corruption/missing run retains rather than deletes.

## 4. Pack and locator cases

- deterministic loose lookup without locator entry;
- pack mixed live/dead objects;
- crash before/after pack fsync, run fsync, and locator `CURRENT`;
- reader holds old locator generation through switch;
- fixed run-count/byte cap triggers consolidation/backpressure;
- missing/corrupt replacement leaves source usable;
- last locator never removed before verified selected replacement;
- legacy carrier evacuation preserves all retained checkpoints.

## 5. Grace/trash/resurrection

- create a checkpoint during grace and prove candidate bytes remain at normal lookup;
- crash before/after final recheck and trash rename;
- restore ambiguous trash before ref admission;
- resume a durable exact `deleting` batch;
- attempt a new ref to a graph already missing a deleted object and prove validation
  fails before visibility;
- lease expiry, wall-clock reversal, process pause, and restart do not alone authorize
  deletion.

## 6. Squash

Run manual, depth, fragmentation, evacuation, and repair squash. Assert:

- same `RootId`, exact logical tree, and checkpoint after restart;
- old-or-new complete `CURRENT` at every crash point;
- admitted old sessions remain valid;
- new sessions use replacement;
- old generation deletion waits for leases/grace/final recheck;
- no squash-specific durable state family.
- LayerStack GC never traverses or deletes `/eos/workspace`, `/eos/storage`, or
  `/eos/runtime`; WorkspaceManager cleanup remains independent.

## 7. Resource and space evidence

Record object/pack/locator/mark/trash/materialization bytes, duplicate peak and settled
residue, pack slack, locator lookup/read amplification, GC work/latency slices, RSS,
queues, tasks, workers, FDs, mappings, deletion batch, and source overlap. Verify warm
native request counters remain zero for all maintenance work.
