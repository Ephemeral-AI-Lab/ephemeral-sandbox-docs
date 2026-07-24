# Phase 1 — LayerStack 2.0 storage

> Overview for the first phase of the
> [Ephemeral Sandbox 2.0 migration](../index.md).

| Field | Decision |
| --- | --- |
| Status | Proposed; evidence-gated |
| Goal | Replace LayerStack historical storage without replacing native execution |
| Product implementation | Rust |
| Benchmark verification | Python |
| Initial environment | Pinned Ubuntu 24.04 Docker image |
| Phase 2 handoff | Stable immutable roots, leases, publication, recovery, and native materialization |

## 1. Purpose

Phase 1 makes LayerStack an efficient and dependable checkpoint foundation for
the later branch and MCTS system.

The current runtime already provides fast native workspace execution through
LayerStack and OverlayFS. Phase 1 keeps that execution model and changes how
immutable history is identified, retained, reconstructed, and reclaimed.

The intended result is:

- native files for active execution;
- CDC/CAS for portable, reusable historical content;
- immutable and versioned checkpoint roots;
- old roots protected by durable leases;
- transactional publication and recovery;
- blame and provenance independent of chunk identity; and
- bounded memory and disk-backed maintenance state.

## 2. Architecture boundary

```mermaid
flowchart LR
    W["Native writable workspace"] --> P["Checkpoint publication"]
    P --> R["Immutable LayerStack root"]
    R --> H["Hot native materialization"]
    R --> C["Portable CDC/CAS history"]
    H --> O["OverlayFS workspace"]
    O --> X["Command, file, PTY, and stdin execution"]
    C --> M["Cold-root materialization"]
    M --> H
```

CDC/CAS is not a replacement for OverlayFS. It participates in checkpoint
publication, retained history, verification, hydration, squash, and garbage
collection. Ordinary command and PTY execution continues to use the native
filesystem.

## 3. Phase 1 abstractions

| Abstraction | Purpose |
| --- | --- |
| Immutable root | Stable identity of one published workspace state |
| Logical manifest | Portable description of the root’s filesystem content |
| Native materialization | Mount-ready representation used by OCI/Linux execution |
| CDC/CAS history | Compact retained content shared across root versions |
| Publication transaction | Creates a complete new root or no visible root |
| Lease | Protects old and active roots from reclamation |
| OCC generation | Prevents stale publication from overwriting newer work |
| Blame transition | Records authorship separately from deduplication |
| Recovery journal | Makes interrupted state changes resumable or safely abortable |
| Retention and GC | Reclaims only unreachable and unleased state |

## 4. What Phase 1 changes

Phase 1 changes:

- the identity and format of immutable LayerStack roots;
- how changed file content is retained across revisions;
- how old roots are materialized when they are no longer hot;
- how publication, leases, blame, recovery, and garbage collection are made
  durable; and
- how existing LayerStack roots migrate to the new format.

Phase 1 does not change:

- the ordinary `/workspace` filesystem seen by sandboxed commands;
- command, PTY, stdin, signal, cancellation, or child-reaping semantics;
- namespace isolation;
- the private writable upper owned by each active execution; or
- the requirement that target images need no LayerStack utility.

## 5. Work order

| Order | Milestone | Outcome |
| ---: | --- | --- |
| 1.0 | Freeze the current baseline | Existing correctness, speed, and total-space behavior are reproducible |
| 1.1 | Define the portable root contract | New roots are immutable, versioned, deterministic, and migration-safe |
| 1.2 | Introduce CDC/CAS in shadow mode | New metadata is produced beside the current authoritative LayerStack |
| 1.3 | Prove materialization and storage lifecycle | Hot roots remain native and cold roots can be reconstructed safely |
| 1.4 | Make new publication authoritative | OCC, leases, blame, recovery, squash, and GC operate on the new roots |
| 1.5 | Complete compatibility migration | Existing roots remain readable and rollback remains possible |
| 1.6 | Hand off to Phase 2 | SandboxGraph can depend on stable root and transaction semantics |

The migration must be additive. Existing roots remain readable while the new
format is introduced, compared, and qualified. A bulk destructive rewrite is
not part of the initial migration.

## 6. Parallel work

Three lanes can proceed in parallel after the contracts are frozen:

| Lane | Responsibility |
| --- | --- |
| Baseline and benchmark | Unified baseline runner, measurements, and Python verification |
| Storage implementation | Rust implementation of roots, CDC/CAS, publication, materialization, and retention |
| Compatibility and correctness | Old-root reading, migration comparison, fault injection, and recovery evidence |

Phase 2 graph schemas may be explored during this work, but the Phase 2 runtime
must wait for the Phase 1 exit gate.

If an implementation finishes before the shared benchmark is ready, its
evaluation clock begins only after the baseline and verifier are available.

## 7. Evaluation priorities

Phase 1 is judged in this order:

1. exact filesystem correctness;
2. OCC, lease, blame, recovery, and GC correctness;
3. materialization, mount/remount, squash, command, and PTY performance;
4. total physical storage, including active native state and staging;
5. bounded memory and operational simplicity; and
6. future portability.

A correctness or memory failure cannot be offset by better speed or storage.

No CDC algorithm is selected by this overview. Candidate algorithms and storage
layouts must use the same contract and baseline. The selected implementation
must be based on measured evidence rather than research scores alone.

## 8. Phase 1 exit gate

Phase 1 is complete only when:

- existing and new roots remain readable;
- published and materialized workspaces preserve exact filesystem behavior;
- old leased roots remain usable while newer roots, squash, and GC exist;
- stale publishers cannot silently overwrite newer work;
- blame survives edits, renames, merges, materialization, squash, and GC;
- crashes cannot expose a partial or corrupt root;
- command and PTY execution remain on the native filesystem path;
- warm materialization and mount performance remain competitive with the
  current LayerStack baseline;
- total physical storage is measured honestly rather than reporting CAS bytes
  alone;
- memory, queues, workers, and maintenance operations are bounded;
- no target-image helper, FUSE path, external database service, SQLite
  dependency, or required reflink is introduced; and
- the Ubuntu 24.04 Docker qualification suite passes.

Passing this gate does not prove Windows, macOS, native Linux, or WASI
qualification. It proves the pinned initial Docker environment only.

## 9. Explicit non-goals

- SandboxGraph product APIs;
- MCTS scheduling, evaluation, or backpropagation;
- nested workspace sessions;
- exact process-memory rollback or CRIU;
- one sandbox per retained checkpoint;
- distributed or remote CAS;
- FUSE, JuiceFS, or a CAS-backed execution VFS;
- a required reflink path;
- production WASI execution; and
- broad Docker image or host matrices.

These belong to Phase 2 or later portability work.

## 10. Documents to prepare under Phase 1

This index is only the overview. Phase 1 should later add separate documents
for:

1. root and compatibility contract;
2. [CDC/CAS space, time, and native materialization
   specification](01-cdc-cas-space-time-materialization-spec.md);
3. native storage-lifecycle and on-disk format specification;
4. publication, OCC, leases, blame, and recovery specification;
5. benchmark and acceptance contract;
6. implementation order and work-lane prompts; and
7. migration, rollout, and rollback plan.

Implementation should not begin from this index alone.

The current read-only storage-selection prompt is
[prompts/storage-solution-examination-review.md](prompts/storage-solution-examination-review.md).
