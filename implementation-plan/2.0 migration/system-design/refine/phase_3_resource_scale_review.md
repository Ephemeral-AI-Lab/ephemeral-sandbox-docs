# Phase 3 — Resource and scale review

> Owner: resource-safety reviewer  
> Prerequisite: Phase 2 PASS  
> Design-document writes: forbidden; this phase's Handoff record is writable  
> Output: Resource Safety Packet

## Objective

Prove that the candidate architecture survives large states, many sandboxes,
nested forks and concurrent workspace sessions without unbounded RAM, FDs,
workers, queues, disk, inodes or unreclaimable staging.

## Required scenarios

Evaluate at least:

- bases of 1 GiB and larger;
- one million filesystem entries;
- many sandboxes and checkpoints;
- many parallel and nested forks;
- multiple concurrent sessions on one sandbox;
- at least 1,000 idle sessions;
- slow, abandoned and expired readers;
- repeated publication and GC churn;
- byte, inode, staging, FD, worker, queue and RSS exhaustion;
- crash during capture, segment installation, catalog publication and GC;
- recovery when the storage pool is near full.

## Resource domains

Account separately for:

- application-owned memory;
- kernel page cache and filesystem metadata;
- workload runtime or container memory;
- catalog pages and cursors;
- payload and codec buffers;
- workspace bytes and inodes;
- temporary external-sort runs;
- candidate and unselected objects;
- orphan and obsolete generations;
- GC live-set and relocation space;
- reader and recovery leases;
- workers, coordinators, FDs and queue descriptors.

Large collections must stay disk-backed. No repository-sized map, set, vector,
memory mapping, queue or per-session index is allowed.

## Admission model

Require an all-or-none decision over one fixed resource vector:

    admit(request) only if every volatile claim and durable reservation fits

Separate:

- volatile claims: workers, coordinators, FDs, buffers and runtime memory;
- durable reservations: workspace bytes and inodes, staging, orphan, obsolete,
  recovery and GC space.

Do not acquire several resource semaphores independently. Do not maintain an
unbounded retry queue. Acquire permits before opening expensive resources.

Multiple sessions on one sandbox consume the sum of their reservations. Do not
credit shared bases, expected deduplication, page-cache sharing or likely
reclaim.

## Mandatory bounds

For every operation derive:

| Bound | Required statement |
|---|---|
| Application memory | Formula and configured maximum |
| Runtime memory | Backend-qualified reservation and enforcement |
| Open FDs | Global and per-operation maximum |
| Workers | Executing and queued maximum |
| Queue memory | Descriptor count and bytes |
| Workspace disk | Byte and inode reservation |
| Staging | Peak scratch and cleanup ownership |
| Catalog generations | Live, obsolete and recovery maximum |
| Reader leases | Count and maximum age |
| GC | Live-set, relocation and maintenance reserve |
| Orphans | Charged owner, cap and recovery policy |

Idle sessions may retain durable records and workspace allocation. They may not
retain dedicated workers, payload buffers, catalog copies or open file trees.

## Quota truthfulness

The review must not claim universal hard per-session byte and inode quotas on an
arbitrary ordinary bind-mounted directory.

Evaluate:

- PortableAccounting: admission, measurement and aggregate protection;
- EnforcedQuota: writable activation only when a backend proves byte and inode
  enforcement before session creation.

If a requested hard limit cannot be enforced, activation must fail. Monitoring
or post-write fencing is not a hard quota.

## Cache-off and batch qualification

Correctness and qualification run with no persistent cache. Evaluate bounded
batch lookup, ordered catalog traversal and coalesced payload reads as working
sets, not caches.

At 1 GiB/s with 16 KiB chunks, account for 65,536 chunk resolutions per second.
Reject a design that depends on one cold catalog descent per chunk without a
bounded page-aware batch path.

## Resource Safety Packet

Return:

1. resource-variable dictionary;
2. per-operation time, memory, FD, disk and inode formulas;
3. global admission vector and acquisition order;
4. overload and typed-failure matrix;
5. quota capability contract;
6. idle-session and concurrent-session proof;
7. GC and near-full-disk proof;
8. crash cleanup and reservation-reconstruction rules;
9. adversarial qualification plan;
10. unresolved blockers with owning phase;
11. task paths and session IDs.

## Pass gate

Phase 3 passes only when:

- every resource has a finite aggregate limit;
- no limit grows with repository size or inactive-session count in memory;
- every expensive operation reserves before allocation;
- orphan and obsolete bytes remain charged and reclaimable;
- recovery and GC retain maintenance headroom;
- quota language distinguishes accounting from enforcement;
- concurrent fanout reaches admission denial without host OOM;
- no cache is required for correctness;
- every overload path has a bounded typed outcome.

## Handoff record

> Mutable, append-only execution record. Complete this after gate evaluation.
> On a rerun, append Attempt 2 or later; do not overwrite an earlier attempt.

### Attempt 1

| Field | Value |
|---|---|
| Status | PASS |
| Gate | PASS — the selected architecture has one finite aggregate admission vector; fixed RAM, FD, worker, queue, reader, operation-owner and generation limits; pre-allocation byte/inode reservations; bounded GC and recovery headroom; typed overload; and no memory term proportional to repository or idle-session count. Measurements remain qualification work and are not represented as achieved. |
| Owner task path | `/root` |
| Owner session ID | `019fc04c-cc15-7bd0-9f32-15e944d54659` |
| Started | 2026-08-02T02:04:19Z |
| Completed | 2026-08-02T03:23:53Z |
| Next phase | Phase 4 — Review synthesis and writer handoff |
| Next phase may start | YES |

### Subagents

| Review scope | Task path | Session ID | Result |
|---|---|---|---|
| GC, catalog generations, crash cuts, reader retirement, near-full recovery and deterministic memory cleanup | `/root/phase3_gc_crash` | `019fc051-8e44-7fb1-a4c7-43ed71f9a3b9` | COMPLETE — selected the two-arena singleton catalog state machine, `4C` physical catalog bound, fixed reader deadlines, 8 MiB fallible pool, bounded victim GC, a physical maintenance reserve, reservation reconstruction and fail-closed crash outcomes. |
| Stage 4.6 provenance, publication/materialization lower bounds, sparse-fixture timing decomposition, qualified fast path and comparable benchmark contract | `/root/phase3_poc_optimization` | `019fc051-ce6b-71a1-8983-5bad4f76307e` | COMPLETE — proved the ordinary-directory `Omega(B_nonhole + F)` floor, separated portable and journal-qualified paths, corrected P4 attribution to the sealed build, removed layer/squash machinery, and found that campaign memory evidence exceeds the new 96 MiB limit. |
| Independent resource formulas, concurrent-session accounting and cgroup separation | `/root/phase3_resource_formulas` | `019fc051-1c65-7252-95c3-0f2ebd712900` | INTERRUPTED after preliminary review — separated storage-owned, cgroup and workload memory and independently found the sealed campaign incompatible with a 96 MiB hard limit. Its proposed 32 MiB global managed pool was rejected; the coordinator selected the stricter 8 MiB global bound below. |

### Scale synthesis

The architecture passes this design gate only with the constants and formulas in
this record made normative. The current authoritative documents do not yet
pass: they still contain dual-selector, renewable-reader, per-reader-buffer and
128 MiB language. Phase 5 must replace those statements; it must not merge old
and new resource models.

The scale result is intentionally simple:

- immutable state, checkpoints and nested forks consume catalog/disk records
  and unique reachable objects, never a resident heap graph;
- an idle session consumes one durable record plus its charged ordinary-file
  workspace, and zero storage RAM, FDs, workers, tasks, reader slots or queue
  payload;
- large capture, materialization, attribution, lookup and marking sets are
  fixed-width disk spools processed by bounded external merge;
- all work competes for one global all-or-none admission vector;
- exact disk and inode reservations are charged before allocation and remain
  charged through crash recovery until ownership transfers or synchronized
  deletion completes;
- one selected catalog arena plus one mutually exclusive auxiliary arena bounds
  sparse-update churn, abandoned readers and interrupted rebuilds;
- one physical maintenance reserve is unavailable to user work and makes one
  catalog rebuild plus one bounded relocation cycle possible near full disk.

This is an analytical design PASS, not an implementation or benchmark PASS.
FastCDC compatibility/throughput, B+ constants, 96 MiB execution, dense
capture/materialization and every crash barrier still require the Phase 6
qualification matrix before the documents may say `Accepted`.

#### Resource-variable dictionary

All arithmetic is checked for overflow before admission. `A(x)` rounds physical
bytes to the qualified filesystem allocation quantum. Logical file length is
never substituted for allocated bytes.

| Symbol | Meaning |
|---|---|
| `B` | Stable non-hole source bytes examined by capture or emitted by materialization. |
| `L` | Logical byte length, including holes; used for semantic limits, not physical-space credit. |
| `F` | Filesystem facts/entries visited, including directories, links and bounded metadata facts. |
| `K` | Canonical object/demand descriptors; `K <= ceil(B / 8 KiB) + c_meta * F`, with finite `c_meta` fixed by the canonical format. |
| `Delta` | Missing canonical payload bytes after exact catalog resolution; no deduplication credit is taken before that resolution. |
| `U` | Catalog records inserted, replaced or removed by one transaction. |
| `N_reach_max` | Deployment-fixed maximum reachable typed-object count, derived from catalog capacity. |
| `Qb`, `Qi` | One workspace's admitted physical-byte and inode reservations. Multiple sessions consume their sum. |
| `P` | Catalog page bytes: 16 KiB. |
| `alpha` | Minimum accepted non-root page fill: `1/2`. |
| `H_max` | Maximum B+ height: 8. |
| `C` | Configured maximum bytes in one self-contained live catalog arena, including page slack and every namespace. |
| `S_seg` | Maximum segment payload: 64 MiB. |
| `R_run` | External-sort/mark run memory: 1 MiB. |
| `F_merge` | External merge fan-in: 8. |
| `r_desc`, `r_demand`, `r_mark` | Publication descriptor, materialization demand and GC mark widths: at most 96, 56 and 40 bytes respectively. |
| `D_head` | Fixed `HEAD.tmp`, manifest/control framing and directory-allocation bound. |
| `h_seg`, `h_run` | Fixed segment framing/trailer bound and 64-byte run header/footer. |

Canonical keys are fixed binary fields, and catalog values are capped and refer
to large canonical objects by `ObjectId`. Let `k_max`, `v_max`, `h_page` and
`slot` be their frozen maxima. Format qualification computes:

```text
leaf_entries_min =
  floor((alpha * P - h_page) / (k_max + v_max + slot))

internal_fanout_min =
  floor((alpha * P - h_page) / (k_max + child_ref + slot))
```

It must prove `leaf_entries_min >= 2`, `internal_fanout_min >= 3`, and that the
configured record ceiling fits at `H_max <= 8`. A mutation exceeding a format,
arena, quota or height ceiling fails before page or segment allocation.

#### Selected finite aggregate limits

| Resource | Hard bound | Reason / ownership |
|---|---:|---|
| Storage-owned managed memory | 8 MiB globally per storage authority; 4 MiB qualification target | Shared by every sandbox/session; never multiplied by count. |
| One sandbox's concurrent managed claims | 4 MiB | At most two 2 MiB heavy-operation claims, still subordinate to the global pool. |
| One heavy operation | 2 MiB | Coordinator, borrowed worker buffer, catalog path and one sort/codec slice. |
| Storage-domain cgroup admission high-water | 64 MiB | Leaves 32 MiB for charged page cache, kernel memory, stacks and allocator variance. |
| Storage-domain cgroup hard maximum | exactly 100,663,296 bytes (96 MiB) | `memory.max`; `memory.swap.max = 0`. `memory.high` is not enforcement. |
| Executing data workers | 4 | Each borrows one 256 KiB buffer; no per-session worker. |
| Active durable operation owners/coordinators | 16 | Fixed staging slots `slot-00` through `slot-15`; recovery cannot discover a seventeenth owner. |
| Waiting heavy descriptors | 16, at most 64 KiB total | Descriptor-only no-wait queue; queued payload bytes are zero. |
| Storage-owned open FDs | 128 total, including fixed/control FDs | Light operation <=4, stream <=8, heavy/maintenance <=24. |
| Volatile readers | 64 | Slots contain only arena/root/deadline/fence fields. |
| Reader age | 30 seconds absolute, non-renewable | Long work resumes by immutable `StateId` plus traversal key. |
| Catalog arena files | 2 | One Selected plus one Auxiliary. |
| Catalog physical bytes | at most `4C` | Derived below; no third generation. |
| Relocating maintenance epochs | 1 | A second GC/rebuild waits for retirement and synchronized deletion. |
| Persistent application cache | 0 bytes | Cache-off is the baseline and qualification mode. |

The 8 MiB managed pool is a ceiling, not a target. Every byte has one class:

| Managed class | Hard bytes | Justification |
|---|---:|---|
| Catalog pages and bounded cursors | 2 MiB | Height-eight paths, ordered leaf batches, output page and bounded cursor state. |
| Four worker buffers | 1 MiB | Four times 256 KiB for capture, hashing, segment I/O, materialization or GC. |
| Coordinators, reader/replay/permit tables and queue | 1 MiB | Sixteen owners, sixteen waiting descriptors, 64 reader slots and fixed control state. |
| Chunk/hash/codec/sort/merge scratch | 3 MiB | FastCDC window <=32 KiB, BLAKE3 state and at most one admitted merge/codec working set. |
| Allocator/accounting/recovery headroom | 1 MiB | Fallible allocation metadata, checked error construction and recovery control. |
| **Total** | **8 MiB** | No class may borrow beyond the shared permit ledger. |

No large `Vec`, map, set, memory map, directory cache, locator cache, task
registry or session registry exists. Every variable allocation obtains a byte
permit before `try_reserve`, opening an FD, dispatching a worker or writing a
spool.

Kernel page cache, filesystem metadata, allocator arenas, helper processes and
thread stacks are not relabeled as application memory. They are observed in
`memory.current`/`memory.stat` and constrained by the 64 MiB writable-admission
high-water and 96 MiB hard cgroup. A backend whose idle baseline and worst
fixed claims cannot remain below the high-water is not writable-qualified.
There are no per-operation privileged storage helpers in the selected design.

#### Reusable finite functions

For `n` fixed-width records of `r` bytes:

```text
n_run(r,n) = ceil(r * n / R_run)

D_sort(r,n) <=
    2 * A(r * n + h_run * n_run(r,n))
  + A(F_merge * R_run)
  + A(D_sort_manifest)

I_sort(r,n) <=
    2 * n_run(r,n)
  + F_merge
  + I_sort_control
```

Inputs and outputs are consumed group-by-group, so another full repository-sized
copy is never added at a higher merge level. Ordered B+ resolution costs
`O(H_max + leaves_touched + results)`, not `O(K * H_max)` page reads.

A conservative sparse catalog transaction bound is:

```text
D_catalog(U) <= A(P * (1 + U * H_max)) + A(D_head)
I_catalog(U) <= 1                         # append in selected arena
```

Ordered/bulk construction normally shares paths and uses fewer pages; admission
uses the conservative bound or rejects in favor of the separately reserved
dense rebuild. Segment installation is bounded by:

```text
D_segment(Delta) <=
  A(Delta + h_seg * ceil(Delta / S_seg))

I_segment(Delta) <= ceil(Delta / S_seg)
```

#### Per-operation resource and complexity matrix

`M` values below are simultaneous managed claims, not retained allocations.
All queues are descriptor-only; all staging terms have one durable owner.

| Operation | Worst-case time and I/O | Managed memory / FDs / workers | Peak new disk and inodes | Failure and recovery |
|---|---|---|---|---|
| Point lifecycle read | `O(H_max)` pages | <=256 KiB, <=4 FDs, 0 workers, optional 1 reader | none | Typed integrity/read failure; no mutation. |
| Paginated list | `O(H_max + returned pages)` per bounded page | <=256 KiB, <=4 FDs, 0 workers, 1 reader | none | Cursor expires at 30 s and resumes from stable key. |
| File read / export | `Theta(B)` verified streaming plus ordered lookups | <=512 KiB, <=8 FDs, 1 worker, 1 reader | none unless the API owns a separately reserved output | Expiry resumes by `StateId` and byte/traversal key; corruption fails closed. |
| Create/materialize workspace | `Theta(B + F) + Sort(56,K)`; exactly one output write per non-hole byte | <=2 MiB, <=24 FDs, 1 worker | `Qb + D_sort(56,K) + D_materialize_control`; `Qi + I_sort(56,K) + I_control` | Incomplete target is private and owner-charged; old activation remains selected; exact cleanup/resume. |
| Portable publication | `Theta(B + F) + Sort(96,K) + ordered catalog lookup + Theta(Delta)`; source reads <=`B + Delta`; existing payload copies =0 | <=2 MiB, <=24 FDs, 1 worker | `D_meta(F) + D_sort(96,K) + D_segment(Delta) + D_catalog(U) + D_owner`; matching finite spool/segment/control inode formula | Early stale token writes nothing. Late conflict retains charged candidate until exact cleanup. One selected `HEAD` transaction records success/conflict receipt. |
| Journal-qualified publication | `Theta(dirty non-hole bytes + dirty facts + closure)` common case; same portable bound on any gap/overflow/restart/unsupported mutation | Same claims as portable path | Same admitted worst case; background prepared bytes remain owner-charged | Capability/epoch is in receipt. Any incomplete oracle proof falls back, never guesses. |
| Checkpoint | `O(H_max)` read plus bounded catalog mutation | <=256 KiB, <=4 FDs, 0 workers | `D_catalog(U_checkpoint)`; no payload copy | Names one complete committed `StateId`; active workspaces are never included. |
| Fork | Prefix-seek active-session proof plus `O(H_max)` checkpoint/ref transaction | <=256 KiB, <=4 FDs, 0 workers | `D_catalog(U_fork)`; no payload copy | Locked contract requires no source active session. Child head points to checkpoint state and then evolves independently. |
| Rollback / strict fork commit | Prefix-seek active-session proof plus `O(H_max)` validation/CAS | <=256 KiB, <=4 FDs, 0 workers | `D_catalog(U_head)`; no payload copy or inverse delta | Locked decision table applies; head revision changes prevent ABA; no merge/history log. |
| Destroy / workspace reclaim | `Theta(F + allocated extents)` streaming traversal | <=512 KiB, <=8 FDs, 1 worker | no positive user allocation; tiny fixed cleanup manifest already owner-reserved | Capacity remains charged until absence and parent-directory sync are proven. |
| Catalog rebuild | `Theta(C / P)` ordered stream/bulk build | <=2 MiB, <=24 FDs, up to 2 workers | one replacement arena <=`C`, one inode, from maintenance reserve | One auxiliary state; interrupted build is the sole RecoveryOrphan. |
| Exact GC/repack | `Theta(N_reach log N_reach + V)` external mark/merge plus victim copy | <=2 MiB, <=24 FDs, up to 2 workers | `D_mark_max + D_segment(X)` with `V<=128 MiB`, `X<=64 MiB`; formula below | Old root remains selected until dependencies and new catalog are durable; one retired epoch; idempotent cleanup. |
| Recovery/readiness | `Theta(committed catalog/reservation records + at most 16 owner manifests)` streaming | <=2 MiB, <=24 FDs, up to 2 workers | consumes only the pre-held recovery/maintenance allocation | No admission until sole `HEAD`, reservations, owners, reserve and fences reconcile. Unknown files or selected corruption fail read-only. |

`D_meta(F)` is the canonical encoder's finite path/metadata-spool bound derived
from `Qi`, maximum name/path/xattr facts and canonical record limits. Admission
rejects an infinite or uncomputable workspace contract. The portable algorithm
does one exact stable scan, writes no payload during that scan, externally sorts
descriptors by typed `ObjectId`, performs one page-aware catalog merge, then
rereads and writes only `Delta` in source order. A mutation journal may reduce
common-case work only after it proves complete coverage of namespace, data,
hardlink, xattr, truncate, allocation/hole and mmap changes with monotonic end
epochs and gap/overflow detection. Standard inotify/fanotify alone do not meet
that contract.

#### One all-or-none admission vector

Every request computes one overflow-checked vector:

```text
V = {
  managed_memory_bytes,
  cgroup_headroom_bytes,
  coordinators,
  workers,
  queue_descriptors,
  queue_bytes,
  fd_permits,
  reader_slots,
  durable_owner_slots,
  workspace_bytes,
  workspace_inodes,
  staging_bytes,
  staging_inodes,
  candidate_or_orphan_bytes,
  obsolete_or_retired_bytes,
  maintenance_epoch
}
```

Acquisition is not a chain of semaphores:

1. validate format, backend capabilities, quotas, root and request limits;
2. calculate `V` without opening an expensive FD or allocating a variable
   buffer;
3. under one Resource Admission ledger lock, either claim every volatile
   dimension and logical durable reservation or claim none;
4. when bytes may survive a crash, durably bind the reservation to one of the
   16 owner slots in the selected catalog/`HEAD` protocol before allocation;
5. allocate/open/dispatch only after that durable ownership point;
6. on completion/cancel, join workers, close FDs and return volatile permits;
   transfer selected bytes atomically or retain the owner charge until
   synchronized deletion.

The waiting queue accepts only a fully calculated <=4 KiB descriptor while a
queue slot and bytes fit; otherwise it returns typed pressure immediately.
There is no retry task or unbounded waiter registry.

#### Quota capability contract

`PortableAccounting` reserves and measures physical allocated bytes plus
inodes, protects aggregate pool capacity and fences a session that exceeds its
contract. It cannot claim hostile hard per-directory prevention on an arbitrary
ordinary bind mount. Deduplication, sparse logical length, expected reclaim and
shared bases give no admission credit.

`EnforcedQuota` is exposed only when the adapter proves, before workspace
creation, a platform-provisioned unique quota scope; hard byte and inode limits;
read-back verification; containment; and runtime/cgroup placement. If a caller
requires hard enforcement and any proof is absent, activation returns
`StorageCapabilityUnsupported` rather than silently downgrading. Future fixed
capacity block workspaces may qualify independently; snapshots never do.

#### Idle, concurrent-session, fork and publication proof

One thousand idle sessions add one catalog record and the sum of their
workspace byte/inode reservations. They add zero variable RAM, FDs, readers,
workers, queue payload or resident indexes. Session existence is found by a B+
prefix seek; no duplicated in-memory count is authoritative.

Each active session owns a private ordinary workspace and immutable origin
`(StateId, HeadRevision)`. Candidate construction may run concurrently under
the four worker/eight-MiB pool. Final `HEAD` publication is short and serialized:

- unrelated global catalog commits are rebased against the current root and do
  not create a sandbox conflict;
- two sessions from the same sandbox origin are ordered; the first valid CAS
  advances `HeadRevision`, and the other returns `PublishConflict` without a
  silent merge;
- independently validated sandboxes may share one fixed no-wait durability
  batch, but per-sandbox CAS decisions and receipts remain distinct;
- checkpoint observes only the complete committed head, never workspace data;
- fork, rollback and `commit_fork` perform a catalog prefix seek and obey the
  locked no-active-session rule;
- a fork/checkpoint is a reference to a complete `StateId`, so nested forks do
  not copy payload or create a layer-depth term.

Conflict workspaces remain read-only and disk/inode charged but retain no
service resources. Their aggregate count is bounded by admitted workspace
reservations and catalog capacity, not memory.

#### Catalog-generation and reader proof

There are exactly two arena slots:

```text
Selected
+ Auxiliary in { Empty, Building, RecoveryOrphan, Retired }
```

Thus `G_files <= 2` and `Building + RecoveryOrphan + Retired <= 1`. Sparse CoW
commits append to Selected. `HEAD` stores its arena ID, root page, committed
length, store sequence and checksum. A rebuild starts only from `Auxiliary =
Empty`; a third arena is an integrity breach.

With live-arena cap `C` and selected dead-page cap `C`:

```text
Selected <= 2C
Building or RecoveryOrphan <= C
Retired <= 2C
Catalog total <= 4C
```

Many readers can reference different root offsets in one arena but collectively
pin only that one physical arena. At selection, all old readers can pin the one
Retired arena and all new readers use Selected. Reader slots own no page,
buffer, FD or worker. Another rebuild/relocating GC waits for the 30-second
absolute deadline, adapter/process fencing and synchronized deletion. If dead
pages reach `C` first, mutation returns `CatalogGenerationLimit`; it never
creates a third generation.

#### GC, physical-space and near-full proof

Physical accounting is:

```text
D_used =
    live_segments
  + selected_catalog_live
  + selected_catalog_dead
  + canonical_metadata
  + allocated_workspaces
  + reserved_workspace_growth
  + staging_and_external_sort
  + unselected_segments
  + auxiliary_or_retired_catalog
  + retired_segments
  + operation_orphans
  + bounded_replay_receipts
  + adapter_projections
  + recovery_control
```

There is a parallel inode sum. Bytes/inodes remain charged until selected
ownership transfers in one `HEAD` transaction or the files are absent and all
affected parent directories are synchronized.

GC selects at most two 64 MiB segments and admits only a victim set whose live
ratio is at most one half:

```text
V <= 128 MiB
X <= V / 2 <= 64 MiB
copied / reclaimed = X / (V - X) <= 1
```

Victims above one-half live are skipped. With 40-byte mark records:

```text
n_mark_run = ceil(40 * N_reach_max / R_run)

D_mark_max =
    A(40 * N_reach_max)
  + A(h_run * n_mark_run)
  + A(F_merge * R_run)
  + A(D_mark_manifest)
```

The final mark merge streams into the catalog builder and liveness decision; it
does not create a second full mark set. The non-user-borrowable maintenance
reserve is physically allocated and synchronized:

```text
D_maintenance =
    A(C)
  + D_mark_max
  + A(64 MiB + h_seg)
  + A(D_head)

I_maintenance =
    1
  + n_mark_run
  + 1
  + I_head_control
```

Writable admission never loans this reserve. Maintenance may consume a named
portion, but readiness remains closed until cleanup restores and synchronizes
the complete reserve. If it is absent, the store permits validation/export and
administrative repair only and returns `MaintenanceReserveUnavailable` for
mutation. This proves progress for one catalog replacement plus one bounded GC
cycle at near-full disk without counting hoped-for reclaim.

#### Crash cleanup and memory-reclamation proof

Each heavy operation owns one fixed slot and checksummed committed-prefix
manifest. A crash leaves at most 16 owner groups. Restart accepts no mutation
until it validates the sole `HEAD`, streams reservation records, validates each
slot/manifest, charges every sealed-but-unselected file, truncates incomplete
tails, resumes or synchronously deletes exact owners, restores the maintenance
reserve and fences old adapters/readers. Repeated recovery crashes cannot create
another owner because admission remains closed. Unknown authority-root files,
selected corruption or accounting mismatch cause read-only `IntegrityFailure`;
recovery never elects an older root.

“Garbage collected” RAM means deterministic ownership, not a tracing collector:

- no detached tasks or unjoined workers;
- no strong reference cycle; children refer to parents by weak handle or ID;
- every buffer, FD, permit, slot and reservation has one acyclic RAII guard;
- variable working sets live in an operation arena and return to the fixed pool
  on terminal success, failure or cancellation;
- process death lets the OS reclaim volatile memory; only durable reservations
  are reconstructed.

At quiescence:

```text
active_workers = 0
active_reader_slots = 0
active_operation_fds = 0
queued_payload_bytes = 0
charged_variable_ram = 0
retained_ram <= fixed pool + measured process baseline
```

Qualification must show a plateau across repeated publish, materialize, GC,
conflict, cancel and crash cycles. Allocator retention is allowed only inside
the fixed reusable pool, never as operation/session growth.

#### Typed overload and failure matrix

| Exhausted or invalid dimension | Required bounded outcome |
|---|---|
| Managed memory / cgroup headroom | `MemoryBudgetExceeded` or `RetryLater{Memory}` before allocation |
| Worker / coordinator / queue | `WorkerLimitExceeded`, `QueueLimitExceeded` or bounded `RetryLater` |
| FD permits | `FdLimitExceeded` before opening an expensive FD |
| Reader slots / deadline | `ReaderSlotsExhausted`; `ReaderLeaseExpired{resume_key}` |
| Workspace/staging bytes | `InsufficientStorage{required, available, maintenance_protected}` |
| Inodes | `InodeCapacityExceeded{required, available}` |
| Requested hard quota unavailable/exceeded | `StorageCapabilityUnsupported` / `QuotaExceeded{Bytes|Inodes}` |
| Durable owner slots | `RetryLater{Maintenance|Queue}`; never an unowned staging file |
| Catalog dead bytes / auxiliary occupied | `CatalogGenerationLimit` or `RetryLater{CatalogGeneration, ReaderDrain}` |
| Retired bytes / maintenance reserve | `ObsoleteRetentionLimit` / `MaintenanceReserveUnavailable` |
| Reservation expansion/reconstruction | `ReservationExpansionFailed` / `ReservationReconciliationRequired` |
| Same-sandbox stale origin | `PublishConflict{expected, observed}` |
| Barrier I/O failure | `DurabilityFailure{barrier}`; old `HEAD` remains authority where applicable |
| Selected corruption / unknown file / accounting violation | `IntegrityFailure` and read-only fail-closed readiness |
| Replay outside retained window | `ReplayExpired`; never re-execute |

### Evidence and calculations

Stage 4.6 is evidence for stationary existing payloads and old-or-new replay,
not the selected physical protocol:

- sealed P4 matched median: `58.136209 ms`; the requested 10x hypothesis is
  `<= 5.8136209 ms`;
- the original formal 100x scorecard threshold was `<= 0.364440 ms`; 5.8 ms
  would not satisfy it;
- the exact fixture added 1,048,576 logical sparse bytes across ten files but
  zero allocated payload bytes; affected input was 1,737 bytes and immutable
  semantic output was 44 objects / 12,188 bytes;
- P4 itself used 7,430,144 cgroup bytes and 6,479,872 bytes process RSS, but the
  campaign-wide cgroup maximum was 102,543,360 bytes during activation —
  1,880,064 bytes above exact 96 MiB. P7 also reached 101,289,984 bytes, 626,688
  bytes above the new limit;
- the sealed source authority is commit
  `ac5c0686807ab40ee7e4ef3ff0f8488b66292221`; timing attribution from a later
  checkout is invalid;
- the matched-median service spent about 40.9% in privileged storage sequence,
  36.8% in parallel adoption/semantic/session-destroy wall time, 14.8% in ref
  commit, 5.7% pre-storage and 1.7% outcome persistence. The new architecture
  removes those duplicated authorities and mount choreography, but portable
  exact capture introduces its unavoidable scan.

Exact publication from an ordinary directory without a trusted complete
mutation oracle has worst-case `Omega(B_nonhole + F)`. Materializing an ordinary
writable directory has the same construction lower bound and `Omega(B_nonhole)`
output writes. Therefore 5.8136209 ms is retained only as a named median stretch
target for the exact comparable sparse metadata fixture on a qualified fast
filesystem. It is not a universal SLA or a dense 1/5/9 GiB claim.

Required benchmark families are separate: `P4-compat-sparse`,
`PortableFullScan`, and `JournalQualifiedDelta`. Every result reports p50/p95/
p99/max, queue delay, bytes and facts read, segment/catalog bytes written,
barrier count/time, disk/inode peak, memory.current/stat, managed live bytes,
RSS, FDs/tasks, fallback reason and cleanup convergence. Publication is timed
from admission through a durable selected root, exact receipt and terminal
session state. Cache-off correctness and cold lookup remain mandatory.

Primary sealed evidence:

- `phase 1/implementation/stage_04_6_ultra_optimization/poc/mpla_poc_benchmark_report.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z/cases/BG-PUBLISH-SMALL/raw-result.json`
- `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z/resources.json`
- `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final70-p7-20260801t082954z/cases/HV-07/raw-result.json`
- `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final70-p7-20260801t082954z/resources.json`

### Decisions and results

- Resource Safety Packet: produced in this Attempt 1.
- Aggregate admission vector: one fixed all-or-none vector selected; no
  independent semaphore acquisition and no unbounded waiter.
- Memory: 8 MiB global managed hard bound, 4 MiB target, 4 MiB per-sandbox
  concurrent claim, 2 MiB per heavy operation, 64 MiB cgroup admission
  high-water, exact 96 MiB `memory.max`, swap zero, cache zero.
- Concurrency: four workers, 16 owners/coordinators, 16 waiting descriptors /
  64 KiB / zero payload, 128 total FDs, 64 readers with 30-second absolute
  non-renewable deadlines.
- Catalog: 16 KiB pages, half-full non-root floor, height at most eight, two
  arenas and at most `4C`; no A/B selector, third generation or recovery
  election.
- Quota: `PortableAccounting` is aggregate reservation/measurement only;
  `EnforcedQuota` requires verified hard byte and inode scope before creation.
- GC: two 64 MiB victims, live ratio at most one half, relocation at most 64
  MiB and copied/reclaimed at most one; exact disk-backed mark and physical
  non-borrowable maintenance reserve.
- Publication: cache-off portable full scan is always correct; a qualified
  journal may optimize but never replace fallback. Existing payload remains
  stationary; each genuinely missing new byte is packed once.
- Logical layers and squash supply no resource or correctness role in the
  complete-`StateId` design. Physical repack is bounded GC, and materialization
  is a separate projection operation.
- Memory cleanup: acyclic RAII ownership, joined/cancelled work, fixed operation
  arenas and plateau evidence; no tracing-GC or allocator-release assumption.

### Adversarial qualification plan

1. Dense 1/5/9 GiB, one million entries, huge files, tiny files, maximum depth,
   all-hole and alternating data/hole extents, hardlinks, xattrs and maximum
   chunk counts.
2. One thousand idle sessions and many active sessions on one sandbox; prove
   zero per-idle-session RAM/FD/worker/task delta and first-writer-wins conflict.
3. Parallel and deeply nested forks/checkpoints; prove pointer-only creation,
   no layer-depth term and correct pinned-object accounting.
4. Fill 64 readers, rebuild once, attempt another rebuild, expire/fence readers,
   and prove two arenas/one retired epoch at every cut.
5. Repeated sparse commits with a pinned retired arena until `C` dead bytes;
   prove typed denial and no third arena.
6. GC at exactly 50% live and above 50%; prove copied/reclaimed <=1 or victim
   rejection, plus exact mark completeness under forced spill.
7. Byte and inode exhaustion at every workspace, spool, segment, catalog,
   `HEAD`, materialization, GC, unlink and directory-sync boundary.
8. Fill user capacity while preserving the physical reserve; crash repeatedly
   during near-full cleanup and prove owner count <=16 and writable admission
   stays closed until reconciliation.
9. Kill/corrupt at every capture frame, run manifest, segment body/footer/sync/
   rename/dir-sync, catalog append/sync, `HEAD.tmp` write/sync/rename/dir-sync,
   response, GC and materialization selection cut. No partial state or fallback.
10. Force 65,536/s representative and 131,072 hard-bound chunk resolutions;
    verify page-aware ordered lookup rather than one cold descent per chunk.
11. Run with exact 96 MiB hard cgroup, swap zero, cache off, low
    `RLIMIT_NOFILE`, allocator faults, worker/queue saturation and page-cache
    pressure; assert typed denial before partial acquisition and no host OOM.
12. Repeat publish/materialize/GC/conflict/cancel/recovery until managed live
    bytes, RSS/current, allocator arenas, tasks, FDs, readers and permit counters
    plateau.
13. Force every qualified-journal mutation class, overflow, gap, restart and
    unsupported event; all incomplete proofs take the portable full-scan path.
14. Run the three benchmark families independently with at least 30 interleaved
    samples and explicit durability/barrier attribution.

### Blockers and returned work

- No Phase 3 architecture/resource blocker remains. Phase 4 may synthesize the
  selected constraints.
- The existing implementation and measurements do **not** meet the new 96 MiB
  acceptance limit. Phase 6 owns empirical acceptance; until it passes, the
  documents must label the limits requirements/targets, not achievements.
- No journal or write-interposition backend is currently qualified. Phase 4
  must select portable full scan as the universal algorithm and describe the
  journal lane only as a fail-closed capability-qualified optimization, never a
  required or hidden fast path.
- The 5.8136209 ms number is a qualified sparse-fixture hypothesis, not a hard
  correctness gate. Phase 4 must reject any universal/dense latency claim.
- B+ codec capacity, FastCDC feed-invariance/throughput and exact filesystem
  barrier performance are unmeasured qualification obligations, not competing
  architecture choices.

### Files changed

- `refine/phase_3_resource_scale_review.md` — this Handoff record only. No
  authoritative design document, production source or other phase record was
  changed during Phase 3.

### Output for Phase 4

- Lock every finite constant, formula, admission rule, cleanup invariant,
  two-arena transition and overload type in this packet.
- Select portable exact capture/materialization as the universal baseline;
  qualify any journal path explicitly and retain unconditional fallback.
- Remove all LayerStack, logical squash/remount, dual-selector, renewable-reader,
  per-reader-buffer, per-session-service-resource and 128 MiB language.
- Distinguish `StateId`, per-sandbox `HeadRevision`, global physical
  `StoreSequence` and catalog `ArenaId`; do not overload “generation.”
- Keep one selected B+ catalog and sole fail-closed `HEAD`, stationary existing
  objects, packed missing bytes, two arenas and one retirement epoch.
- Hand the writer the three named benchmark contracts and evidence labels; do
  not turn targets or analytical lower bounds into measured claims.
- Packet reference: this Attempt 1 plus the three exact task/session records in
  the Subagents table.
