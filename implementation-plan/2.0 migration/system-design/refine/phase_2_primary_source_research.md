# Phase 2 — Primary-source research

> Owner: research lead  
> Prerequisite: Phase 1 PASS  
> Design-document writes: forbidden; this phase's Handoff record is writable  
> Output: Research Decision Packet

## Objective

Use primary evidence to select, reject or constrain every candidate that can
change the architecture. Research supports decisions; it does not expand the
system with speculative features.

## Research sources

Prefer, in order:

1. original papers and technical reports;
2. official OS, filesystem and runtime documentation;
3. official Rust crate documentation and repositories;
4. production-project design documents and formats.

Use secondary summaries only to locate a primary source.

Database projects may be studied only as rejected comparisons. They cannot be
selected, wrapped, embedded or copied into a general database surface.

## Required research tracks

### Physical catalog

Research immutable CoW B+, sorted tables, SST/LSM, radix/HAMT, extendible hash,
packed flat and FST-like structures.

Evaluate:

- cold point lookup;
- bounded sorted-batch lookup;
- sparse update amplification;
- dense rebuild and GC;
- ordered traversal;
- immutable snapshots;
- corruption behavior;
- mmap or cache dependence;
- FD behavior;
- implementation and maintenance effort.

Inspect relevant Rust projects, but reject engines that import database, WAL,
MVCC, cache, allocator, compaction or generic transaction machinery.

### Canonical identity and tree

Research:

- BLAKE3 specification and maintained Rust implementation;
- deterministic typed encoding;
- canonical compressed radix or Patricia structures;
- fixed-size chunking;
- FastCDC and maintained Rust implementations;
- attribution and external-merge techniques.

If FastCDC is retained, identify every parameter required for deterministic
golden vectors. Do not retain underspecified SeqCDC.

### Packed objects and durability

Research:

- sealed segment and trailer-index formats;
- bounded recovery metadata;
- file and directory synchronization;
- rename durability;
- crash-consistency studies;
- corruption and acknowledged-generation behavior.

The research must explicitly compare descriptor A/B policies and the
no-silent-rollback requirement.

### Portability and resource enforcement

Research official sources for:

- Docker bind mounts, storage-driver limits and rootless resource control;
- Linux byte and inode quotas;
- OCI descriptor and layer facts;
- WASI filesystem facts and durability;
- Firecracker block devices, snapshots and vsock;
- cgroup v2 memory and process accounting;
- descriptor-relative filesystem traversal.

State what is universally portable, capability-qualified, or impossible under
the prohibitions.

### Replay and idempotency

Separate:

- deterministic same-ID object equality;
- bounded API-operation idempotency receipts.

Research the information and storage requirements of both. Do not claim
forever replay with bounded receipt storage.

## Evidence record

For every retained or rejected mechanism record:

| Field | Required content |
|---|---|
| Mechanism | Exact candidate |
| Sources | Direct primary links |
| Status | Maintenance and latest relevant release |
| License | Compatibility and obligations |
| Platforms | Supported and excluded environments |
| Failure model | Crash, corruption and recovery assumptions |
| Resource model | Memory, FD, disk and queue behavior |
| Evidence | Tests, fuzzing, production use or paper results |
| Decision | Adopt, Wrap, Borrow design, Minimal custom, Reject |
| Reason | Hard gates and optimization evidence |

Clearly label:

- project measurement;
- external measurement;
- analytical bound;
- target;
- estimate;
- hypothesis.

## Research Decision Packet

Return:

1. completed research matrix;
2. direct source list grouped by final component;
3. physical-index recommendation;
4. canonical encoding and hash recommendation;
5. chunking recommendation or a decisive qualification gate;
6. durability and descriptor options with evidence;
7. quota and runtime-enforcement capability findings;
8. backend fact-profile findings;
9. dependency adoption and rejection list;
10. decisions that invalidate Phase 1 assumptions;
11. task paths and session IDs.

## Pass gate

Phase 2 passes only when:

- every Phase 1 research question is answered or proven unanswerable;
- every proposed custom mechanism has primary evidence;
- each dependency has a narrow justified role;
- database engines are rejected, not selected;
- portability and quota claims are technically honest;
- performance claims retain the correct evidence label;
- disagreements are explicit for Phase 3 or Phase 4 resolution.

## Handoff record

> Mutable, append-only execution record. Complete this after gate evaluation.
> On a rerun, append Attempt 2 or later; do not overwrite an earlier attempt.

### Attempt 1

| Field | Value |
|---|---|
| Status | PASS |
| Gate | PASS — all 12 Phase 1 questions have selecting answers; every retained custom mechanism has primary evidence; dependencies are narrow; no database engine remains selectable; portability, quota and performance claims are qualified |
| Owner task path | `/root` |
| Owner session ID | `019fbff4-d312-7e43-bde1-11a3a66fd36f` |
| Started | 2026-08-02T01:28:22Z |
| Completed | 2026-08-02T02:04:18Z |
| Next phase | Phase 3 — Resource and scale review |
| Next phase may start | YES |

### Subagents

| Research scope | Task path | Session ID | Result |
|---|---|---|---|
| Physical catalog, canonical encoding/hash/tree, chunking, attribution and migration | `/root/research_catalog_canonical` | `019fc01a-797a-7012-a9a0-953196e0fe59` | COMPLETE — recommended a fixed-purpose immutable CoW B+ catalog, strict RFC 8949 CBOR, official BLAKE3, canonical Patricia directories and one-shot ID-rewriting migration; recommended fixed chunks rather than FastCDC, with the disagreement resolved below. |
| Packed objects, single-`HEAD` durability, reader retirement and bounded replay | `/root/research_durability_replay` | `019fc01a-b70f-7a23-928d-339cb3c928d6` | COMPLETE — proved the A/B/no-rollback contradiction, specified dependency-first single-`HEAD` crash cuts, separated local segment validation from the global catalog, and derived fixed-window authenticated replay and volatile epoch retirement. |
| Docker, Linux, OCI, WASI and Firecracker capability and enforcement facts | `/root/algorithm_redesign` | `019fbff6-be63-7fe0-9421-31faca547d3d` | COMPLETE — separated portable accounting from verified enforcement, selected descriptor-relative Linux traversal, and defined fail-closed Docker-now and capability-qualified future adapter profiles. |

### Research synthesis

#### Selected evidence-backed design

Phase 1's four domain components plus one permit-only service remain selected.
The physical catalog changes from the leading radix candidate to a
**fixed-purpose immutable copy-on-write B+ tree**. It is not a database: it has
one closed typed key space and root, immutable fixed pages in append-only
arenas, checksummed pages, positioned reads, point/ordered-batch/range cursors,
sparse path-copy updates and a dense external-sort bulk builder. It has no WAL,
MVCC, generic transactions, query language, page cache, buffer manager, free
list, background compaction or user-extensible schema.

One catalog root contains the locator, lifecycle and bounded-replay namespaces.
The mandatory checksummed `HEAD` contains exactly one direct physical catalog
root reference plus format, generation and checksum. Root and child page
references are direct physical references so locator lookup is not circular.
Immutable segment dependencies and the catalog arena are synchronized first;
`HEAD.tmp` is then synchronized, renamed over `HEAD`, and the containing
directory is synchronized before acknowledgement. Recovery validates the one
selected descriptor/root and fails closed on its corruption. It never elects
an older valid generation.

Canonical bytes use a project-frozen restricted deterministic profile of
[RFC 8949](https://www.rfc-editor.org/rfc/rfc8949) CBOR through the low-level
`minicbor` API. The profile permits only the specifically enumerated typed
arrays, byte/text strings, unsigned integers and booleans; it forbids maps,
floats, tags, indefinite lengths, duplicate or alternative representations,
Serde and derive-generated wire schemas. Type and format tags are explicit.
`ObjectId` is the full 256-bit official BLAKE3 digest over a domain-separated,
typed, length-framed canonical payload. There is one definition of state
identity: `StateId = ObjectId(StateManifest)`.

Canonical directories retain a project-specific bytewise compressed
Patricia/radix Merkle construction. File data uses the maintained Rust
`fastcdc` crate rather than SeqCDC or a project CDC implementation. FastCDC is
adopted only through the following frozen compatibility profile:

| Frozen field | Required value |
|---|---|
| Format tag | `FastCDC-v2020-EPS1` |
| Implementation | `fastcdc` 4.0.1, `v2020` module |
| Minimum / target average / maximum | 8,192 / 16,384 / 32,768 bytes |
| Normalization | level 2 |
| Seed and tables | seed 0; the original v4.0.1 `v2020` gear and mask tables |
| Reset domain | Reset to offset zero for every canonical maximal non-hole data extent |
| Boundary procedure | Exact rolling, normalized-mask, skip, forced-maximum and EOF rules of the pinned v4.0.1 `v2020` source |
| Identity | Chunk content bytes are hashed as canonical objects; the rolling gear hash is never stored as identity |
| Streaming rule | Boundaries must be independent of caller buffer size and identical to the reference slice implementation |
| Compatibility gate | Golden vectors cover empty, minimum/average/maximum edges, repeated bytes, every byte value, pseudorandom bytes, extent resets, varied feed sizes and supported architectures; a changed boundary sequence requires a new canonical format version |

This is a format-level wrapper, not a fork or reimplementation. Phase 3 must
prove a buffer bounded by the 32 KiB maximum and preserve the 1 GiB/s project
target as an unmeasured target. Before format freeze, failure of deterministic
streaming vectors, maintenance review or the resource/throughput qualification
returns the design to fixed 16 KiB chunks as an explicit new decision; after
freeze, it requires a format migration.

Segments have a typed header, framed records, a local trailer directory and a
footer/full digest. The trailer is only for segment validation and victim
inspection. The selected B+ catalog is the sole global `ObjectId -> locator`
authority; recovery never rebuilds global truth by scanning every segment.

Lifecycle mutation replay is distinct from content equality. Each authenticated
client lane has a durable generation, low-water mark, high-water mark and a
fixed receipt ring. An accepted operation selects its semantic effect and exact
receipt/result reference together in the same catalog-root/`HEAD` commit. A
retained sequence returns that exact result; an older/evicted sequence returns
`ReplayExpired` without execution; reuse with a different request digest is an
error. This borrows RFC 4303/6479 bounded anti-replay windows and does not claim
forever replay. An already-present same `ObjectId` is instead verified by kind,
length and streaming byte equality.

Reader safety uses fixed process-local reader slots, absolute non-renewable
deadlines and fixed retirement epochs. Replacement is selected before new
leases to the old generation are stopped; deletion waits for drain or fences
the process/adapter. Restart fences all old processes and adapter allocations
before readiness. No durable reader registry or unlink-while-open assumption is
required.

Portability is a fact/capability contract, not a lowest-common-denominator
filesystem claim. The Store runs only on a qualified ordinary local filesystem.
Docker-now uses a private disk-backed bind workspace, a read-only digest-pinned
image root and no FUSE/OverlayFS correctness dependency. An arbitrary hostile
bind directory can supply only `PortableAccounting`; `EnforcedQuota` requires a
platform-provisioned, unique, verified project-quota scope with hard byte and
inode limits. If hostile hard quota is requested without that capability,
activation fails. WASI and Firecracker remain future capability-qualified
adapters: WASI exposes a reduced canonical fact profile and no generic `HEAD`
durability/quota claim; Firecracker uses a read-only boot/root, fixed-capacity
per-session block filesystem and authenticated guest agent over vsock.

#### Evidence labels

- **External measurement:** the FastCDC paper's reported throughput and
  deduplication results; they are motivation, not measurements of this project.
- **Analytical bounds:** B+ height/page reads, chunk-count bounds, replay-ring
  bytes, fixed reader slots, external-sort runs and dependency-first crash cuts.
- **Project targets:** at least 1 GiB/s chunk scanning, the documented memory
  budget and bounded recovery/readiness; none is marked achieved here.
- **Project measurement:** none was produced in Phase 2 for FastCDC, the new B+
  format or cache-off lookup.
- **Estimates/hypotheses:** implementation effort, likely cache hit rate and
  backend throughput remain non-normative until measured.

#### Completed research matrix — physical catalog and canonical data

| Mechanism | Sources | Status / license | Platforms and failure/resource model | Evidence | Decision and reason |
|---|---|---|---|---|---|
| Fixed-purpose immutable CoW B+ | [B-tree paper](https://doi.org/10.1007/BF00288683), [redb design](https://github.com/cberner/redb/blob/master/docs/design.md) | Foundational design; redb inspected only; project format has no third-party engine license | Positioned ordinary-file I/O; immutable checksummed fixed pages; `O(log_f N)` cold point pages, ordered cursor/batch reads, `O(log_f N)` sparse copied pages, linear dense build; fixed open arenas/generations | Original balanced-tree bounds plus production-project comparison; project constants/measurements pending Phase 3 | **Minimal custom.** Best joint fit for cold lookup, ordered batch/scan, sparse update and dense rebuild; closed typed format avoids database machinery. |
| Persistent Patricia/radix as physical catalog | [Patricia](https://dl.acm.org/doi/10.1145/321479.321481), [HAMT report](https://infoscience.epfl.ch/entities/publication/b892b2ce-7bf0-41d2-b68c-fb44a3c64a33) | Foundational algorithms; project implementation would be custom | Key-length-bounded path but digest keys have little prefix locality; immutable snapshots; more cold pointer/page steps and packing uncertainty | Analytical comparison; no project cache-off result | **Reject as physical catalog; retain for canonical directories.** Deterministic depth is attractive, but ordered batches and page density favor B+. |
| Packed flat / static sorted table | [Bigtable](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/), [Git pack format](https://git-scm.com/docs/pack-format) | Active formats; studies only | Excellent sequential dense build and scan; primary-root sparse update rewrites `Theta(N)`; generations add precedence | Production format precedent and analytical rewrite bound | **Borrow for dense-build leaves/runs; reject as sparse mutable root.** |
| SST/LSM | [LSM-tree paper](https://doi.org/10.1007/s002360050048), [Bigtable](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/) | Mature designs; not dependencies | Levels, filters, tombstones, precedence, caches and compaction create extra disk/write/recovery state | Original paper and production design | **Reject.** Recreates forbidden database/compaction machinery. |
| Extendible hash | [Original IBM paper](https://research.ibm.com/publications/extendible-hashinga-fast-access-method-for-dynamic-files) | Foundational design | Good expected point lookup; directory doubling/overflow; no natural ordered traversal or sorted batching | Original algorithm; analytical scan/rebuild comparison | **Reject.** Ordered operations and deterministic dense rebuild are hard gates. |
| FST-like static index | [Lucene FST package](https://lucene.apache.org/core/9_12_0/core/org/apache/lucene/util/fst/package-summary.html) | Maintained production implementation; study only, Apache-2.0 | Compact for shared prefixes; random digests share little; sparse locator changes imply broad rebuild | Production documentation; analytical key-distribution comparison | **Reject.** Compression premise and sparse-update cost do not fit digest locators. |
| Generic Rust engines (`redb`, `fjall`) | [redb](https://github.com/cberner/redb), [Fjall](https://github.com/fjall-rs/fjall) | Maintained; MIT/Apache-2.0 family as published by projects; inspected only | Import transactions, cache/allocator or LSM/WAL/compaction surfaces beyond the closed catalog | Production code/design comparison | **Reject as dependency or copied surface.** Useful only as comparison evidence. |
| Deterministic CBOR profile via `minicbor` | [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949), [`minicbor`](https://github.com/twittner/minicbor) | RFC current; `minicbor` 2.3.0 observed; BlueOak-1.0.0 | Pure Rust/no_std-capable library; caller streams under fixed buffers; project forbids ambiguous CBOR features and owns schema/profile evolution | Standards test vectors plus project golden/cross-version vectors required | **Wrap.** Reuse parsing/primitive encoding while freezing one smaller canonical language; no Serde/derive/maps/floats/tags. |
| BLAKE3-256 | [Specification](https://github.com/BLAKE3-team/BLAKE3-specs), [official Rust repository](https://github.com/BLAKE3-team/BLAKE3), [test vectors](https://github.com/BLAKE3-team/BLAKE3/blob/master/test_vectors/test_vectors.json) | `blake3` 1.8.5 observed; maintained; CC0-1.0 OR Apache-2.0 | Rust-supported targets with portable fallback; streaming constant working state; collision/corruption assumptions are cryptographic, not storage durability | Official spec/vectors and implementation tests | **Adopt.** Full 256-bit domain-separated typed hashes; same-ID equality still verifies kind, length and bytes. |
| Canonical directory Patricia/Merkle construction | [Patricia](https://dl.acm.org/doi/10.1145/321479.321481) | Foundational design; project code/license | Backend-neutral byte keys; immutable compressed paths; bounded by canonical path/key limits; malformed order/path/hash fails closed | Original algorithm plus required golden/adversarial tree vectors | **Minimal custom.** Canonical identity needs a deterministic typed Merkle layout not supplied by a general library. |
| External sort/merge and occurrence-rank attribution | [GNU sort manual](https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html), [Myers diff paper](https://doi.org/10.1007/BF01840446), [rsync report](https://rsync.samba.org/tech_report/) | Mature techniques; no engine selected | Spill files and run count are permit-bounded; exact duplicate chunks require deterministic occurrence ranks; adversarial repetition remains disk-backed | Algorithmic bounds and production tools; project attribution vectors pending | **Compose external sort; minimal custom occurrence tiling.** Existing tools supply primitives, not the exact canonical attribution rule. |
| Fixed 16 KiB chunks | Conventional deterministic operation | No dependency | One chunk buffer; 1 GiB implies 65,536 chunks, but an insertion shifts all following boundaries within an extent | Analytical bound only | **Qualified fallback, not selected.** Simpler, but materially weakens required structural sharing after insertions. |
| `fastcdc` v2020 frozen profile | [FastCDC paper](https://www.usenix.org/conference/atc20/presentation/xia), [`fastcdc-rs`](https://github.com/nlfiedler/fastcdc-rs) | Crate 4.0.1 observed; maintained; MIT | Pure Rust; 8/16/32 KiB bounds; one at-most-32-KiB streaming window; deterministic only under the frozen tables/rules/reset profile | Peer-reviewed external measurements; upstream/project vectors; project throughput is still an unmeasured target | **Wrap.** Provides resynchronizing content-defined boundaries and structural sharing without owning CDC code. |
| SeqCDC | No complete stable specification or maintained interoperable implementation was found | Underspecified/unqualified | Boundary sequence, tables, versions, memory and compatibility cannot be reconstructed | Evidence gap is itself a hard-gate failure | **Reject.** It cannot be part of canonical identity. |

#### Completed research matrix — durability, replay and portability

| Mechanism | Sources | Status / license | Platforms and failure/resource model | Evidence | Decision and reason |
|---|---|---|---|---|---|
| One mandatory atomically replaced `HEAD` | [POSIX `rename`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/rename.html), [POSIX `fsync`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fsync.html), [Linux `rename(2)`](https://man7.org/linux/man-pages/man2/rename.2.html), [Rust `File::sync_all`](https://doc.rust-lang.org/std/fs/struct.File.html#method.sync_all), [ALICE](https://www.usenix.org/conference/osdi14/technical-sessions/presentation/pillai), [CrashMonkey](https://www.usenix.org/conference/osdi18/presentation/mohan) | OS/Rust interfaces maintained; project protocol/license | Qualified same-filesystem ordinary local FS; dependencies synced first, then temp file, rename, directory sync; bounded selected-root validation; media/controller promises are qualification inputs | Official semantics plus crash-consistency studies; project fault injection required | **Minimal custom protocol borrowing OS primitives.** Exactly one selector can meet acknowledged-state/no-silent-rollback. |
| Alternating A/B descriptors, “highest valid” | Same durability sources | Common pattern, no dependency | After newest corruption, a valid old slot cannot reveal whether newest was an unacknowledged torn attempt or acknowledged state corrupted later | Indistinguishability proof over crash/corruption cuts | **Reject.** Silent rollback can violate acknowledged state; a durable selector added to fix it is `HEAD` again. |
| Sealed segment + local trailer | [Git pack format](https://git-scm.com/docs/pack-format), [OCI descriptor](https://github.com/opencontainers/image-spec/blob/main/descriptor.md) | Active formats; designs borrowed; Git GPL-2.0, OCI Apache-2.0 are not linked/copied code | Append framed records then trailer/footer/digest; partial packs unselected; bounded open-segment/FD count; local trailer is not global truth | Widely deployed content-addressed format precedents; project truncation/bit-flip tests required | **Borrow design / compose.** Simple validation and repack inspection without a second global index. |
| Volatile fixed reader epochs | [Linux RCU concepts](https://docs.kernel.org/RCU/whatisRCU.html), [Windows file deletion](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-deletefilea) | Maintained OS documentation; no library dependency | Fixed slots/deadlines/generations; publication before retirement; fence on timeout/restart; never depend on Unix unlink-open behavior | RCU grace-period precedent and cross-platform deletion facts | **Borrow design.** Bounded volatile leases preserve portability; reject durable reader logs and renewable unbounded leases. |
| Fixed authenticated replay windows | [RFC 4303](https://www.rfc-editor.org/rfc/rfc4303), [RFC 6479](https://www.rfc-editor.org/rfc/rfc6479) | Internet Standards; no code dependency | Fixed lanes and width; durable low/high water and exact ring receipt/result refs; same root commit as effect; finite bytes and deterministic expiry | Standards anti-replay information model plus crash-cut analysis | **Borrow design and compose with `HEAD`.** Exact retained replay is possible; forever replay with bounded storage is not. |
| Generic DB/WAL or atomic-write helper | Catalog/durability sources above | Varies | Hidden WAL/transactions/cache/recovery or incomplete directory-sync proof | Scope and crash-cut comparison | **Reject.** Neither a database nor a rename wrapper may replace the closed catalog and explicit proof. |
| Docker-now adapter | [Bind mounts](https://docs.docker.com/engine/storage/bind-mounts/), [resource constraints](https://docs.docker.com/engine/containers/resource_constraints/), [rootless mode](https://docs.docker.com/engine/security/rootless/), [OCI image spec](https://github.com/opencontainers/image-spec) | Docker 29.7.1 observed; OCI Image Spec 1.1.1; Apache-2.0 projects | Linux qualified host; private disk-backed workspace; digest-pinned read-only image root; rootless limits require delegated cgroup v2/systemd; no FUSE/storage-driver correctness claim | Official capability/limitation docs | **Adopt as current qualified adapter profile.** Activation verifies every requested capability and otherwise fails. |
| Descriptor-relative Linux traversal | [`openat2(2)`](https://man7.org/linux/man-pages/man2/openat2.2.html) | Linux ABI; project uses `std` plus existing `rustix` narrowly | `O_PATH` root plus `RESOLVE_BENEATH|RESOLVE_NO_MAGICLINKS|RESOLVE_NO_XDEV`, optionally `NO_SYMLINKS`; parent fd and validated basename; fail if unavailable | Official syscall semantics | **Borrow OS primitive.** Reject prefix/`realpath` checks and unsafe fallback. |
| Byte/inode enforced quota | [`quotactl(2)`](https://man7.org/linux/man-pages/man2/quotactl.2.html), [`xfs_quota(8)`](https://man7.org/linux/man-pages/man8/xfs_quota.8.html) | Maintained Linux/XFS interfaces | Requires platform-provisioned unique project scope, hard block+inode limits and verification; service receives no `CAP_SYS_ADMIN`; arbitrary bind dirs do not qualify | Official interfaces and privilege/scope requirements | **Capability-qualified.** Label verified scope `EnforcedQuota`; all other cases are `PortableAccounting`, never hostile hard enforcement. |
| cgroup v2 memory/process enforcement | [Kernel cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) | Maintained Linux interface | Verify controller delegation/placement; `memory.max` hard ceiling, `memory.high` throttle only, `memory.swap.max=0`; `pids.max` hierarchical task bound; counters include more than application buffers | Official kernel semantics | **Borrow OS primitive.** Enforce runtime ceilings where available while reporting application-pool and cgroup/RSS facts separately. |
| WASI future adapter | [WASI 0.3 announcement](https://wasi.dev/roadmap), [filesystem WIT](https://github.com/WebAssembly/wasi-filesystem) | WASI 0.3.0 observed 2026-06-11; W3C Community Contributor License Agreement | One writable preopen; reduced fact profile without Unix dev/inode/mode/uid/gid/xattr identity; Store remains a qualified host service; generic WASI supplies neither `HEAD` durability nor quota | Official WIT/API capability surface | **Future, capability-qualified.** Never claim a universal physical workspace or full POSIX facts. |
| Firecracker future adapter | [Firecracker repository/docs](https://github.com/firecracker-microvm/firecracker), [snapshot support](https://github.com/firecracker-microvm/firecracker/blob/main/docs/snapshotting/snapshot-support.md), [vsock](https://github.com/firecracker-microvm/firecracker/blob/main/docs/vsock.md) | 1.16.1 observed 2026-07-02; Apache-2.0 | Read-only boot/root, per-session fixed-capacity block FS, authenticated guest agent over vsock; snapshot is optimization only; restart resets vsock; host cgroup limits VMM, not exact guest process count | Official architecture/versioning/runtime docs | **Future, capability-qualified.** No snapshot/disk/runtime fact becomes canonical truth. |

No retained platform or storage mechanism depends on FUSE, OverlayFS behavior,
reflinks, privileged mounts, page-cache residency, unlink-while-open semantics or
backend snapshots for correctness.

### Primary sources

Grouped by the component whose decision they support:

- **Canonical State:** [RFC 8949 deterministic CBOR](https://www.rfc-editor.org/rfc/rfc8949), [official BLAKE3 specification](https://github.com/BLAKE3-team/BLAKE3-specs), [official BLAKE3 Rust implementation and vectors](https://github.com/BLAKE3-team/BLAKE3), [Patricia](https://dl.acm.org/doi/10.1145/321479.321481), [FastCDC](https://www.usenix.org/conference/atc20/presentation/xia), [`fastcdc-rs`](https://github.com/nlfiedler/fastcdc-rs), [Myers diff](https://doi.org/10.1007/BF01840446), [rsync technical report](https://rsync.samba.org/tech_report/) and [GNU external sort](https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html).
- **Durable Store:** [B-trees](https://doi.org/10.1007/BF00288683), [Patricia](https://dl.acm.org/doi/10.1145/321479.321481), [HAMT](https://infoscience.epfl.ch/entities/publication/b892b2ce-7bf0-41d2-b68c-fb44a3c64a33), [extendible hashing](https://research.ibm.com/publications/extendible-hashinga-fast-access-method-for-dynamic-files), [LSM trees](https://doi.org/10.1007/s002360050048), [Bigtable](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/), [Git pack format](https://git-scm.com/docs/pack-format), [OCI descriptors](https://github.com/opencontainers/image-spec/blob/main/descriptor.md), [POSIX rename](https://pubs.opengroup.org/onlinepubs/9799919799/functions/rename.html), [POSIX fsync](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fsync.html), [ALICE](https://www.usenix.org/conference/osdi14/technical-sessions/presentation/pillai), [CrashMonkey](https://www.usenix.org/conference/osdi18/presentation/mohan) and [Linux RCU](https://docs.kernel.org/RCU/whatisRCU.html).
- **Lifecycle:** [RFC 4303 anti-replay](https://www.rfc-editor.org/rfc/rfc4303) and [RFC 6479 extended sequence windows](https://www.rfc-editor.org/rfc/rfc6479).
- **Backend Adapters:** [Docker bind mounts](https://docs.docker.com/engine/storage/bind-mounts/), [Docker resource constraints](https://docs.docker.com/engine/containers/resource_constraints/), [Docker rootless mode](https://docs.docker.com/engine/security/rootless/), [OCI Image Spec](https://github.com/opencontainers/image-spec), [`openat2(2)`](https://man7.org/linux/man-pages/man2/openat2.2.html), [`quotactl(2)`](https://man7.org/linux/man-pages/man2/quotactl.2.html), [`xfs_quota(8)`](https://man7.org/linux/man-pages/man8/xfs_quota.8.html), [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), [WASI filesystem](https://github.com/WebAssembly/wasi-filesystem), [Firecracker](https://github.com/firecracker-microvm/firecracker), [Firecracker snapshot support](https://github.com/firecracker-microvm/firecracker/blob/main/docs/snapshotting/snapshot-support.md) and [Firecracker vsock](https://github.com/firecracker-microvm/firecracker/blob/main/docs/vsock.md).

### Decisions and results

- Research Decision Packet: produced in this Handoff record; all evidence
  claims carry source, failure/resource scope and evidence label.
- Final custom registry: exactly **four** mechanisms — (1) canonical Patricia
  Merkle-directory construction, (2) deterministic occurrence-rank attribution
  tiling, (3) fixed-purpose immutable CoW B+ update/bulk-build format and (4)
  the single-`HEAD` commit/recovery protocol, including atomic effect/receipt
  coupling. FastCDC, CBOR and BLAKE3 are reused; external sort, segments, GC,
  admission, traversal and replay windows are borrowed/composed operations.
- Adopt/wrap: official `blake3` 1.8.5; low-level `minicbor` 2.3.0 under a
  restricted profile; `fastcdc` 4.0.1 `v2020` under the frozen profile; existing
  `rustix` only for narrow descriptor-relative syscalls. No new general engine.
- Reject: SeqCDC, every database/LSM/WAL/MVCC engine, A/B descriptor election,
  durable reader registries, unbounded receipts, generic atomic-write wrappers
  as a durability proof, FUSE/reflink/snapshot/storage-driver correctness and
  unsafe path-resolution fallback.

#### Answers to all Phase 1 selecting questions

1. **Radix versus B+:** select the fixed-purpose immutable CoW B+ catalog for
   page density, ordered batches and sparse/dense dual behavior; keep Patricia
   only as the canonical directory structure.
2. **Single `HEAD` versus A/B:** select one mandatory atomically replaced and
   directory-synchronized `HEAD`. A/B election cannot distinguish pre-ack tear
   from later corruption and therefore can silently roll back acknowledged
   state.
3. **Deterministic typed encoding:** wrap `minicbor` primitives in a strict RFC
   8949 subset with project-owned explicit schema/profile and golden vectors;
   do not invent a primitive codec.
4. **Hash:** adopt official full BLAKE3-256 with domain, version, kind and length
   framing; stream under fixed memory and verify same-ID existing bytes exactly.
5. **Chunking:** reject SeqCDC and project CDC; wrap `fastcdc` 4.0.1 `v2020`
   using the complete frozen 8/16/32 KiB profile and compatibility vectors.
6. **Segments:** use sealed framed segments with a local trailer/footer/digest;
   the trailer validates a segment but the B+ catalog alone owns global
   locators and bounded selected-root recovery.
7. **Readers and GC:** use fixed volatile epoch slots with absolute deadlines,
   publication-before-retirement and process/adapter fencing; no durable reader
   log and no dependency on unlinking open files.
8. **Replay:** use authenticated fixed lanes/windows and exact bounded receipt
   rings committed atomically with effects. Expired IDs never execute and
   return `ReplayExpired`; content equality remains a separate byte-verification
   rule. Public API method signatures do not change; the replay key is a
   transport envelope.
9. **Backend facts:** only canonical facts and fail-closed capability semantics
   are universal. Docker-now is qualified as above; WASI has a reduced fact
   profile; Firecracker needs a block workspace and agent; no universal
   physical workspace is claimed.
10. **Quotas/cgroups:** arbitrary bind workspaces get `PortableAccounting`.
    Only a preprovisioned verified unique project-quota scope gets
    `EnforcedQuota`; cgroup v2 hard memory/process limits are separately
    verified and reported with their actual kernel meanings.
11. **Migration:** the new canonical profile and chunking generally change
    `StateId`. Perform a one-shot offline fact-equivalent rebuild and rewrite
    every ID/reference before an atomic routing switch; no dual writes,
    permanent ID map or legacy fast path.
12. **Dependencies/licenses:** only narrow hash/codec/chunker/syscall support is
    adopted under the licenses above. No database, cache, allocator, WAL, MVCC,
    compactor or hidden general transaction layer is selected.

#### Disagreements and Phase 1 assumptions invalidated

- The catalog research overturns Phase 1's leading physical radix: B+ wins the
  combined cold-read, ordered-batch, sparse-update and dense-rebuild comparison.
- The catalog/canonical reviewer preferred fixed 16 KiB chunks because the
  project had no FastCDC measurements. The coordinator instead selects the
  maintained frozen FastCDC wrapper: fixed chunks analytically shift every
  following boundary after an insertion in an extent, directly weakening the
  required Merkle structural sharing, whereas the original FastCDC work and a
  narrow maintained Rust implementation provide a qualification path. This is
  not a performance claim; Phase 3 retains deterministic, memory and throughput
  gates and fixed chunks as the pre-freeze fallback.
- Phase 1's provisional `HEAD` wording permitted a typed root plus auxiliary
  roots. The selected descriptor has exactly one direct physical catalog-root
  reference; lifecycle, locators and replay are namespaces under it.
- Fixed-size chunking is no longer the default, and canonical migration cannot
  preserve old IDs. The four-component/one-service authority graph, transient
  publication phase and fail-closed capability model are otherwise validated.

### Blockers and returned work

- None. Remaining numeric constants, adversarial resource bounds, golden-vector
  execution, cache-off lookup and chunk-throughput qualification are Phase 3
  proof obligations, not unresolved source-selection blockers.

### Files changed

- `refine/phase_2_primary_source_research.md` — this Handoff record only. No
  authoritative design document, production source or other phase record was
  changed during Phase 2.

### Output for Phase 3

- **Resource assumptions requiring proof:** choose page size, payload capacity,
  minimum occupancy, fanout and maximum height for the B+ catalog; bound direct
  page reads for point and sorted batches; bound arena generations/open FDs;
  reconcile application buffers, codec, hash, chunker, external-sort, catalog,
  reader/emergency and permit state within the documented memory budget; keep
  page cache, allocator/RSS and cgroup memory as separate ledgers.
- **Scale cases:** at least one 1 GiB extent (about 65,536 chunks at the 16 KiB
  target average, with hard count bounds derived from 8/32 KiB), one million
  tiny files, high directory fanout, all-hole and alternating hole/data extents,
  maximum path/name facts, duplicate/repeated content and adversarial sparse
  catalog updates.
- **Candidate bounds:** FastCDC uses at most one 32 KiB chunk window plus fixed
  state and must meet buffer-independent vectors; external sort has a fixed run
  buffer and bounded merge fan-in/FD permits; attribution remains disk-backed;
  GC admits one replacement generation plus selected/obsolete/orphan/workspace
  ledgers; replay selects fixed lane count `L`, window `W` and maximum receipt
  bytes; reader retirement selects a fixed slot count and absolute deadline.
- **Qualification gaps:** measure project FastCDC scalar/cache-off throughput
  against the at-least-1-GiB/s target; run golden vectors across feed sizes and
  supported architectures; measure B+ cold and ordered-batch I/O; fault-inject
  every dependency/`HEAD` sync cut and bit corruption; prove quota/cgroup
  activation checks and deterministic typed overload outcomes.
- **Packet reference:** this Attempt 1 and the three task/session reports in the
  Subagents table.
