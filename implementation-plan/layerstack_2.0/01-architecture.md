# LayerStack 2.0 architecture and invariants

Status: Proposed

Implementation: **BLOCKED BY THE EXPERIMENT**

## 1. Outcome

LayerStack 2.0 is a local, extent-sharing storage engine for Ephemeral Sandbox.
It preserves the ordinary filesystem interface seen by arbitrary container
images and by all agents sharing one workspace. The daemon neither chunks file
contents nor serves reads through a custom VFS. Normal reads and writes stay on
the Linux VFS, OverlayFS, and page cache.

The architectural change is deliberately broad:

- one storage domain replaces the current separate layer-stack and workspace
  volumes;
- immutable layer data and mutable session data are placed on the same
  filesystem;
- a clone-or-copy primitive replaces direct full-file copies;
- metadata moves from loosely coordinated JSON, NDJSON, and in-memory maps to
  one transactional on-disk control plane with bounded resident working set,
  queue, and WAL; and
- the file-blame event becomes part of the publish transaction instead of a
  best-effort append after the layer commit.

This is not a requirement to preserve the current internal storage format.
Compatibility is provided at the product boundary and by an explicit v1/v2
layout decision, not by retaining accidental implementation constraints.

## 2. Platform contract

“All operating systems” means the same contract Docker uses:

| Host | Runtime contract |
|---|---|
| Linux | Linux containers on the host kernel |
| macOS | Linux containers inside Docker Desktop's Linux VM |
| Windows | Linux containers inside Docker Desktop or WSL 2 |

OverlayFS itself is Linux-only. LayerStack 2.0 does not promise a native
macOS filesystem, native Windows containers, or a Windows filesystem filter.
It accepts arbitrary OCI image contents because no guest image library or
agent-side integration is required.

The runtime must select behavior by a probe on the exact production storage
domain, never by host OS name, Docker version, filesystem name, or a static
allowlist.

The cross-platform reflink claim is fail-closed: independent macOS, Windows,
and Linux platform gates must all prove the production storage path. A
correct copy fallback does not satisfy a reflink gate, and a successful result
on one host, architecture, filesystem, or Docker backend cannot qualify a
different cell.

## 3. Core design

### 3.1 One versioned storage domain

Every new v2 sandbox receives one Docker-managed storage domain mounted at a
single root such as `/eos/storage`:

```text
/eos/storage/
├── format                         # immutable layout marker: layerstack-v2
├── metadata/
│   ├── layerstack.db              # transactional control plane
│   ├── layerstack.db-wal
│   └── layerstack.db-shm
├── objects/
│   ├── B.../fs/                   # imported immutable base
│   ├── L.../fs/                   # published immutable layers
│   └── S.../fs/                   # compacted immutable layers
├── sessions/<session-id>/
│   ├── upper/
│   ├── work.<generation>/
│   ├── staging-root/
│   └── rollback-root/
├── staging/                       # uncommitted object builds
├── export/                        # bounded transient spools
└── lost+found/                    # quarantined crash artifacts
```

`objects`, `sessions`, and `staging` must report the same `st_dev`. OverlayFS
`upperdir` and each matching `workdir` remain siblings on that same
filesystem. The shared base is imported once into `objects`; it is not
re-copied per agent or per session.

The v2 format records a unique storage-domain ID and filesystem probe result.
Opening the same domain through two daemon writers remains forbidden. Payload
paths are opened fd-relative with no-follow rules, as in the current hardened
LayerStack code. The metadata directory is created beneath the already trusted
storage root, then ownership, mode, canonical parent, and absence of symlinks
are verified before SQLite opens its database and sidecars. V2 does not assume
a custom fd-based SQLite VFS.

### 3.2 Data plane: clone first, copy correctly

The data plane exposes one narrow operation:

```rust
trait ExtentTransfer {
    fn clone_or_copy(
        &self,
        source: BorrowedFd<'_>,
        destination: BorrowedFd<'_>,
        expected: &FileIdentity,
    ) -> Result<TransferReceipt, TransferError>;
}

struct TransferReceipt {
    method: TransferMethod,       // Reflink | CopyFileRange | BufferedCopy
    logical_bytes: u64,
    allocated_bytes_delta: u64,
}
```

Rules:

1. revalidate the opened source identity, not only its path and length;
2. try a whole-file clone (`FICLONE`/`vfs_clone_file_range`) only when the
   startup probe proved it on this storage domain;
3. on a classified unsupported result, fall back atomically to
   `copy_file_range` and then a bounded fixed-size buffered copy;
4. never expose a partial destination; and
5. fsync the completed object before its metadata transaction can reference
   it.

The daemon never holds file contents in a `Vec` proportional to file size.
Transfers use kernel cloning or a fixed-size buffer. Checksums, where required
for correctness, stream through a fixed-size buffer.

Linux OverlayFS's copy-up implementation attempts
`vfs_clone_file_range()` before its copy loop. Co-locating lower objects and
the session upperdir therefore creates an end-to-end extent-sharing path:

```text
immutable lower --kernel clone--> session upper --runtime clone--> L object
      ^                                                      |
      +---------------- squash winner clone -----------------+
```

This is a hypothesis until FIEMAP/shared-extent and allocated-block evidence
passes on the target kernel. If OverlayFS falls back to byte copy, LayerStack
publish may still clone the upper file, but the end-to-end storage claim has
failed and the implementation gate stays closed.

### 3.3 Metadata plane: one durable commit boundary

LayerStack 2.0 uses an embedded SQLite database compiled into the binary. It
is a local metadata engine, not a payload database. The schema owns:

- storage format and migration state;
- revisions and ordered manifest entries;
- immutable object state and physical/logical byte accounting;
- persistent leases and refcounts;
- squash substitutions and generations;
- publish identity, owner, and file-blame events/ranges; and
- crash-recovery work and parked remount state.

The runtime intentionally replaces the present “runtime never depends on
SQLite” dependency guard. This is an explicit architecture migration: a
transactional embedded store removes multiple ad-hoc logs and unbounded
in-memory indexes. `rusqlite` is already a bundled workspace dependency; no
user installation or service is introduced.

There is one metadata writer and a bounded request queue. Reads use a bounded
number of connections. Required database limits include a fixed page-cache
budget, bounded WAL size/checkpointing, file-backed temporary storage, and no
unbounded memory-mapped region. Values are configuration defaults with hard
upper bounds, not per-agent pools.

“Bounded” applies to daemon memory, queues, transient disk, and WAL—not to the
primary retained history. The database's durable rows grow with retained
revisions and provenance. A storage-domain quota and reserved recovery margin
make that growth finite; reaching the admission high-water mark rejects a new
publish before it becomes visible. Layer GC cannot silently discard blame.

### 3.4 Publish transaction, including blame

The current runtime commits a layer, then best-effort appends an audit event.
A crash or append failure can leave bytes published without their blame
record. V2 removes that dual-write gap:

```mermaid
sequenceDiagram
    participant C as capture/resolve
    participant F as filesystem data plane
    participant M as metadata transaction
    participant B as file_blame

    C->>F: build staged L object with clone_or_copy
    F->>F: fsync tree; rename to objects; fsync objects parent
    C->>M: stage invisible blame rows in bounded batches
    C->>M: BEGIN IMMEDIATE
    M->>M: validate expected revision
    M->>M: validate staged event digest/count
    M->>M: expose object + manifest + blame head together
    M->>M: COMMIT
    M-->>C: durable revision
    B->>M: indexed query by normalized path
```

The database commit is the logical publication boundary. Before it, a promoted
object and staged metadata rows are unreachable and boot cleanup may remove
them. After it, the fsynced object, manifest revision, and provenance are all
reachable. A publish cannot report success if any changed-path blame event
fails. No filesystem I/O, user wait, or range derivation occurs while the
short final write transaction is held.

Origin and ownership derivation is bound to `expected_revision` and
`blame_base_revision`. The final transaction checks both plus the before/after
content digests, changed/deleted path count, range count, and a digest of the
staged transition set.
If the head changed, the complete OCC resolve and blame derivation is discarded
and recomputed; stale ownership ranges are never rebased. A stable idempotency
key makes an uncertain post-commit retry query and return the already committed
revision instead of creating a second layer or event.

Every changed or deleted path has one transition record. An upsert transition
creates a new attribution event/range set and makes it the query-visible head.
A delete transition records the before digest, `after = NULL`, and the prior
head; it has no new ranges and leaves that prior attribution as the
query-visible head. If there was no prior audited head, deletion still records
the transition but `file_blame` remains `NotFound`. Delete transitions,
resulting heads, their counts/digest, the manifest, and the publish identity
become visible in the same transaction. Delete/recreate therefore cannot lose
or invent ownership across a crash.

Blame semantics remain product-compatible:

- attribution describes the latest **published** content, not unfinalized
  session bytes;
- owners and line ranges are identical to the existing OCC merge result;
- no-op publishes create neither a layer nor a blame event;
- deletion preserves the last published attribution, matching today's pure
  audit-store read; delete then recreate records the recreating publisher;
- an unaudited base-only or absent path remains `NotFound`, while today's
  non-text/ignored whole-file attribution remains one synthetic range;
- path normalization remains the existing `LayerPath` normalization; and
- squash and remount create no new publisher attribution.

Before code changes, characterization tests freeze current behavior for
rename/copy, empty files, binary files, trailing-newline changes, and very
large mixed-owner range sets. V2 must match those fixtures exactly unless a
separate public API change is approved.

Unlike the current eager `path -> latest event` `HashMap`, the storage-side
`file_blame` query reads indexed, bounded pages. The existing public
whole-array response remains exact and byte-compatible: the server streams
those internal pages into a quota-controlled file-backed response spool, then
serves it without assembling all ranges in heap. A public cursor API would be
additive and requires separate API approval; LayerStack 2.0 does not impose a
new lower response limit. Retained provenance consumes disk, not daemon heap.
Squash changes active storage structure but leaves the provenance head
unchanged. Provenance GC, if ever added, is a separate versioned retention
policy and cannot be implied by layer GC.

### 3.5 Squash

Squash keeps the existing correctness boundary and race behavior:

1. plan under a brief shared lock and acquire a plan lease;
2. build `S` objects without the storage lock;
3. clone regular-file winners, recreate symlinks, and preserve whiteouts,
   opaque directories, modes, xattrs, hardlink topology, and sparse layout;
4. under the exclusive metadata transaction, re-read the head and prove each
   source run is still contiguous;
5. atomically install the compact manifest and persistent substitution; and
6. release the plan lease only after commit.

Current squash hardlinks regular-file winners and is already almost
byte-neutral. V2 uses reflink across immutable objects to avoid shared inode
metadata while retaining shared data extents. Hardlinks that exist *within*
the guest tree must remain hardlinks within the emitted `S` object.

Storage commit remains independent of live remount. A skipped or failed
remount cannot roll back a committed squash.

### 3.6 Lease rewrite, quiesce, and staged remount

The replacement lease is committed before the old lease is released. The
persistent substitution graph makes rewrite available after daemon restart;
missing or invalid substitutions degrade to identity and never guess.

Leases are typed and epoch-owned. A live-session lease is reconstructed only
after the persisted session, holder, mount identity, and cgroup are proven; a
stale plan lease from a dead daemon epoch is released after its unreachable
build is classified; and a parked-remount lease remains pinned until the
rollback mount is strictly unmounted or the session is destroyed. Boot
recovery never treats “old epoch” alone as permission to release an object.

The existing live-remount proof remains mandatory:

1. verify the holder workspace is OverlayFS and has no child mounts;
2. discover holder-mount-namespace tasks union session-cgroup tasks;
3. `SIGSTOP` every observable task and prove every thread stopped, exited, or
   is safely traced;
4. rediscover; any new task blocks;
5. reject an unreadable or workspace-pinning mount namespace, cwd, root, fd,
   or memory map;
6. mount NEW with the same upperdir and a fresh workdir;
7. move OLD to rollback (point of no return), move NEW into place, and verify;
8. strictly unmount OLD—never lazy detach; and
9. resume only a proven healthy session, then release OLD, then install the
   NEW in-memory handle; on sanctioned `EBUSY`, resume on NEW and install its
   handle while retaining OLD and its parked lease.

Pre-PONR uncertainty releases NEW, keeps OLD, and resumes tasks. Post-PONR
uncertainty keeps tasks frozen and destroys the faulty session through the
ordinary lifecycle. `EBUSY` parks OLD with both leases until destroy.

The boot gate must run against the v2 storage domain and exercise production
mount options, same-upperdir coexistence, whiteouts, and opaque directories.
A failed gate allows commit-only squash but forbids live remount.

## 4. Memory and daemon-health contract

“Memory free” cannot literally mean zero bytes: operations need descriptors
and bounded control state, and Linux may retain reclaimable page cache. It
means **zero resident payload state and no unbounded daemon-owned growth**.

| Area | Required behavior |
|---|---|
| File transfer | Kernel clone or fixed-size streaming buffer; `O(1)` in file size |
| Hash/diff/origin | Exact bounded-memory processing; spill intermediate state to quota-controlled disk |
| Blame | Indexed, paged disk query; no eager all-path index or per-line expansion |
| Manifest | Bounded active chain; streaming/paged history queries |
| Leases/substitutions | Persisted and queried by key; no forever-growing process-global map |
| Work queue | Count- and byte-weighted admission with explicit backpressure |
| Metrics | Fixed-cardinality labels and bounded histograms |
| Export | File-backed spool with bounded page size and deterministic unlink |
| Page cache | Reclaimable kernel memory; reported separately from anonymous RSS |

The internal blame reader is cursor/paged for arbitrarily large range sets.
The existing public whole-array shape is preserved by a quota-controlled,
file-backed response spool; it is never assembled into one heap array. Huge
exact diffs remain exact by spilling compact origin runs to file-backed
temporary tables; “bounded memory” may not be implemented by truncating,
approximating ownership, or silently imposing a new API limit.

The daemon must expose current and peak anonymous RSS, file/page-cache usage,
metadata queue depth, SQLite cache/WAL bytes, open descriptors, live leases,
staged bytes, and parked remounts. Soak acceptance is based on steady-state
slope after warm-up, not only a final RSS snapshot.

## 5. Capability and security contract

The comparison unit is the exact current production container configuration,
not the phrase “has `SYS_ADMIN`.” Current production also uses networking
capabilities. The experiment records and diffs:

- `HostConfig.Privileged`;
- ordered `CapAdd`/`CapDrop` sets and effective capabilities;
- devices and device-cgroup rules;
- security options, seccomp, AppArmor/SELinux labels, and no-new-privileges;
- mounts, propagation, user namespace, and cgroup namespace; and
- helper containers, plugins, sockets, or host-installed components.

V2 passes only if that diff is empty except for the new storage volume layout.
Direct `FICLONE` needs no capability; mounting OverlayFS continues to use the
runtime's existing authority. A managed XFS/Btrfs loop device is unacceptable
if it requires a new device mapping, privileged mode, or host setup.

## 6. Capability modes

```yaml
runtime:
  layerstack:
    layout: v2
    extent_sharing: required # required | preferred | disabled
```

- `required`: boot fails before accepting work unless end-to-end reflink and
  every kernel gate passes.
- `preferred`: clone where proved; atomically fall back to copy on a classified
  unsupported path and emit a stable reason.
- `disabled`: v2 transactional metadata and unified layout, but force copy;
  this is the benchmark control and emergency rollback.

Production rollout cannot silently change `required` to `preferred`.
Per-operation fallback due to corruption, I/O errors, ENOSPC, or identity
mismatch is forbidden; those are hard failures, not capability misses.

## 7. Complexity

Let `F` be logical bytes copied up, `d` be blocks dirtied after clone, `X` be
the number of mapped extents the filesystem must reference, `E` be entries
visited, `L` active layers, `H` retained indexed blame heads, and `page` the
hard-bounded number of ranges returned by one internal blame query.

| Operation | Time | New physical payload | Daemon-owned memory |
|---|---:|---:|---:|
| Overlay first write, clone succeeds | `O(X + d)` filesystem work | `O(d)` payload + `O(X)` filesystem metadata | `O(1)` |
| Publish regular file, clone succeeds | `O(X)` clone metadata plus fsync | no copied payload + `O(X)` filesystem metadata | `O(1)` |
| Copy fallback | `O(F)` | `O(F)` | `O(1)` fixed buffer |
| Squash | `O(E log E)` winner selection | changed metadata + unique extents | bounded by configured batch; must stream |
| Manifest read | `O(L)` | 0 | `O(L)`, with a hard active-layer bound |
| File blame page | `O(log H + page)` indexed lookup | 0 | `O(page)` hard-bounded response |

Reflink's worst case remains `O(F)` new physical data when every block is
subsequently rewritten. Atomic-replace workloads may allocate a new file and
share nothing. These cases belong in the experiment and prevent a misleading
best-case-only claim.

## 8. Deliberate non-goals

- FastCDC, chunk CAS, Merkle traversal, or cross-sandbox global dedup on the
  live path;
- FUSE or a custom userspace filesystem;
- native macOS or Windows-container OverlayFS;
- remote storage, replication, or multi-host writers;
- retaining the v1 on-disk format internally; and
- claiming that filesystem type alone proves reflink behavior.
