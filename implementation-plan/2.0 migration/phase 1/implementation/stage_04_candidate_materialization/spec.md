# Stage 04 — materialization and strict native activation

Status: specification only.

Normative dependencies:

- [implementation index](../index.md)
- [minimal storage contract](../layerstack_storage_contract.md)
- [Stage 03](../stage_03_incremental_publication/spec.md)
- [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

## 1. Outcome

Stage 04 reconstructs a private v3 root into a verified native generation and activates
it with one atomic `CURRENT` pointer. An explicit strict candidate mode runs
command/file/PTY/workspace operations only through that prebuilt native plan; absence
or corruption fails closed with no v1 fallback.

Public authority remains v1. Materializations are created only for active or explicitly
pinned roots.

## 2. Native generation model

`materialization-id` derives from
`(RootId, backend-kind, backend-format-version, target-profile)`. The canonical paths
and required manifest fields are in the storage contract.

`target-profile` is a versioned backend capability profile, not a host path,
environment variable, image tag, or logical identity input. Phase 1's concrete
backend is Linux native carrier directories activated with OverlayFS and mount
namespaces. The portable LayerStack core drives the materializer from CAS objects;
another OS or activation mechanism requires a separate qualified adapter.

A generation is immutable after verification. Its manifest names:

- the materialization tuple and generation fence;
- exact ordered carrier descriptors;
- reconstructed capability set;
- logical verification digest/root;
- entry and allocated-byte counts used for measurement, not identity.

Build output is private operation work until every logical object is verified, the
native tree is synced, and the manifest is durable. Only then may `CURRENT` change.
Old generations remain usable until all active reader/session leases release and
grace/final recheck permits deletion.

`materializations/` is a reconstructible managed native view, but it is not an
unprotected best-effort cache. A generation may be selected by `CURRENT`, leased by
sessions, explicitly pinned, or temporarily be the last verified native locator.
Those conditions prevent eviction. Only unreachable, unleased, non-current,
non-last-locator generations pass grace/final recheck deletion.

The complete relationship to `/eos/workspace` is defined by
[the full `/eos` tree](../layerstack_storage_contract.md#4-complete-eos-ownership-and-storage-tree):
immutable carriers are LayerStack-owned, while each session's `upper`, `work`, and
`executions` are WorkspaceManager-owned.

## 3. Cold reconstruction

Cold materialization:

1. derives the materialization key and joins or owns its one fenced common build
   operation; same-key callers do not intentionally build duplicate generations;
2. protects the root and every last physical locator needed for the build;
3. streams the logical tree in canonical order through fixed buffers;
4. resolves deterministic loose paths first and immutable locator runs otherwise;
5. verifies typed IDs and lengths before native writes;
6. recreates exact supported metadata, sparse layout, hardlinks, symlinks, devices,
   FIFOs, and xattrs or fails closed on unsupported required capability;
7. fsyncs/syncs the private native generation and durable manifest;
8. re-verifies the selected `RootId`;
9. under the brief writer lock registers the root with active GC, atomically selects
   the generation, and acquires/updates its durable fence;
10. releases build-only resources and, after the bounded retry/recovery window, removes
    terminal operation state; only active/pinned materialization state remains.

No full tree/file/all-live set is resident. Repeated requests for an already valid
generation are idempotent. If a builder dies, a later fenced owner resumes or abandons
its exact work conservatively. A complete losing generation from a crash race is
bounded orphan residue, never selected implicitly.

## 4. Activation

Activation resolves `CURRENT` before admitting a session and creates an immutable
bounded native execution plan with final depth `D≤64`. The session owns:

- one materialization-generation lease/fence;
- bounded carrier FDs/mappings required by the provider;
- its private writable upper/work state;
- all child command/file/PTY tasks.

The lease names the exact `{materialization-id,generation,fence}`. Multiple sessions
can share the same read-only carriers and page cache, but never `upper`, `work`,
execution scratch, mount ownership, or unpublished writes. Changing a branch head or
materialization `CURRENT` affects only later admissions. An admitted session stays on
its leased generation until explicit checkout/remount, session replacement, or
teardown.

The warm route performs only plan validation plus native provider I/O. It performs no
CDC, logical object traversal, chunk hash, locator merge, materialization, pack,
compaction, GC, or squash work. Cache miss, missing `CURRENT`, unsupported capability,
or corrupt carrier returns a typed strict error. It never silently invokes v1.

Checkout may select an already materialized root immediately. Otherwise it is an
explicit cold operation before activation; cold work is never hidden in a command,
file, or PTY request.

A publish advances the logical head but does not “sync” or mutate an existing native
generation. The publishing session continues to see its own private upper; a later
session resolves the new head and reuses or materializes that root.

## 5. MCTS and branching

Clean branch/MCTS fork remains the Stage 03 `O(1)` head/ref operation and allocates no
native tree. Only an admitted active fork receives a workspace upper/work pair and,
when needed, one selected shared materialization. Logical ancestry does not add native
mount layers. Squash/flattening later uses the same generation mechanism without
changing the root.

All task/permit/FD/mapping/lease ownership is rooted in a session or build operation.
Cancellation/shutdown joins tasks, closes handles, releases permits, unmounts exact
session paths, and then releases leases. No detached cleanup is allowed.

## 6. Recovery

| Crash point | Recovery |
| --- | --- |
| before verified manifest | old `CURRENT`; resume or reap exact private work |
| after manifest fsync, before `CURRENT` | old generation active; verify/finish or collect orphan |
| after `CURRENT`, before response | new generation active; return it idempotently |
| active session process loss | durable fence/lease and workspace recovery conservatively protect/reap exact state |
| corrupt/missing selected carrier | fail closed; keep evidence; rebuild only through explicit cold operation |

Recovery never chooses a generation by directory mtime or partial contents.

## 7. Complexity and bounds

- cold materialization: streamed `O(R+E+D)`, resident `O(B)`;
- warm activation: `O(D)`, `D≤64`;
- warm command/file/PTY: native provider cost only;
- clean fork: `O(1)` metadata, zero parent payload/native allocation;
- active native storage: only active or explicitly pinned roots;
- peak overlap: one bounded building generation plus protected active generations;
- build workers, buffers, queues, FDs, mappings, tasks, sessions, upper bytes, and
  leases have configured caps and backpressure;
- global/per-profile current-generation, pinned-generation, build-staging-byte, and
  per-session upper quotas reject/backpressure before unbounded allocation;
- same-key concurrent requests have one active fenced build and bounded waiters.

The 60-second Preparation 04 maintenance value is a scheduler slice/checkpoint bound
unless a benchmark cell declares a maximum root size; total cold work remains `O(R+E)`.

## 8. Exit criteria

- [E2E plan](e2e_test.md) passes for exact reconstruction, strict routing, failpoints,
  session lifecycle, and MCTS allocation;
- [benchmark note](benchmark_note.md) records measured cold/warm/space/resource results;
- strict-route gate assertions pass;
- zero candidate request silently falls back to v1;
- warm route counters show zero CDC/object/pack/GC/materialization work;
- source and materialization last-locator safety survives restart;
- concurrent sessions share immutable carriers while retaining isolated uppers and
  stable exact-generation leases;
- Linux/Docker/backend capability claims are limited to measured matrix cells; no
  universal or image-percentage claim is made;
- public authority remains v1.
