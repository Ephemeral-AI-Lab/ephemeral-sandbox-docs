# Stage 04.5 E2E plan — materialization/GC lifecycle alignment

Status: `NOT_RUN`. No item in this document is a `PASS` without a raw artifact
and revision-linked result.

Normative sources:

- [Stage 04.5 specification](spec.md)
- [Stage 04 specification](../stage_04_candidate_materialization/spec.md)
- [Stage 05 specification](../stage_05_retention_gc_packs/spec.md)
- [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

## 1. Evidence rules

Each result records:

- exact command and test filter;
- source revision and whether the worktree was dirty;
- deterministic seed and corpus hash;
- machine, architecture, kernel, filesystem, mount options, container/runtime,
  and build profile;
- configuration and every resource cap;
- failpoint schedule and restart count;
- raw log/artifact path;
- expected and observed logical state;
- retained physical copies and their owners;
- live tasks, workers, permits, buffers, queues, FDs, mappings, leases, mounts,
  operations, and temporary paths;
- peak RAM and disk overlap; and
- `PASS`, `FAIL`, or `OPEN` with the exact reason.

Missing accounting is `OPEN`, not zero. A faster or smaller result cannot pass
if a correctness gate fails.

## 2. Static prerequisite checks

1. Search the production call graph for materialization generation unlink and
   recursive generation removal. Stage 04.5 code must expose no production
   deletion path.
2. Inventory every `unsafe` block and memory mapping reachable from materialize,
   verify, publish, recover, activate, session teardown, and squash. An empty
   inventory is recorded explicitly.
3. Assert that the materialization operation decoder exposes only the common
   authoritative phases `Building`, `Ready`, `Published`, and `Terminal`.
4. Assert the common recovery dispatcher recognizes materialization operations;
   no recognized kind may be skipped permanently.
5. Assert there is one shared storage worker/byte/FD governor and no
   materialization-owned permanent pool or detached thread.
6. Assert all directory enumeration used by recovery is paginated before
   allocation; forbid collect-then-truncate.
7. Assert no `CURRENT` repair path selects a generation by mtime, maximum
   directory number, or successful search of unreferenced directories.

## 3. Private build and visibility

For empty, deep, wide, many-small-file, large-file, sparse, hardlink, symlink,
xattr, metadata-only, device/FIFO where supported, and unsupported-capability
roots:

1. create the exact root/source holds;
2. build and verify a private generation;
3. stop at `Building` and `Ready` and prove `CURRENT` is unchanged;
4. compare the ready carrier with the logical root and v1 reference result;
5. prove the immutable manifest has bounded counts, digests, allocation
   accounting, capabilities, exact operation ID, generation, and fence;
6. publish and prove `CURRENT` changes once;
7. repeat the operation and prove idempotent reuse, not a second generation; and
8. inject an unsupported capability or corrupt object and prove fail-closed
   behavior with no visibility change.

For replacement, repair, and squash builds, disable Stage 05 handoff and prove
publication is rejected while the old selector remains usable. Enable the
deterministic handoff test double and prove publication reaches `Terminal` only
after the exact old subject is durably accepted.

## 4. GC-admission interleavings

Use a deterministic barrier model and, when Stage 05 exists, the real root log.
Explore at least:

1. GC absent before and after publication;
2. GC active before the publisher takes the writer lock;
3. GC installed after the publisher's first outside-lock check;
4. GC closure attempted while publication waits for the writer lock;
5. GC fence changes between checks;
6. root-log append succeeds and selector replacement fails;
7. root-log append response is lost;
8. selector replacement succeeds and `STATE` update fails; and
9. publication is cancelled or panics at every transition.

The linearization point is durable `CURRENT` replacement. Every new visible root
must appear in the active GC root log before closure can complete. Failure,
ambiguity, or a full root log aborts/retains the GC before admitting visibility.

## 5. Exact-reader and generation-switch tests

1. Admit sessions on generation `g`.
2. Build and publish `g+1`.
3. Assert existing sessions continue to use exact
   `{materialization-id,g,fence}` and new sessions use `g+1`.
4. Renew, expire, cancel, and recover leases in different orders. Clock movement
   alone must never delete or substitute `g`.
5. Repeat switches through numeric reuse/collision attempts and prove no
   ABA-style stale-generation acceptance.
6. Hold 1, 16, and 64 active/pinned generations; the 65th admission must
   backpressure then return `ResourceExhausted` without evicting an active
   generation.
7. Corrupt current and old manifests separately. Current corruption fails
   closed; old-session corruption is reported and never silently redirected.

## 6. Crash and persistence matrix

Crash or inject `EIO`, short write, torn/truncated metadata, response loss, and
`ENOSPC` before and after every write, fsync, rename, and parent-fsync boundary:

- common operation admission and root/source hold persistence;
- carrier file creation and native sync;
- ready-manifest write and fsync;
- private-generation installation;
- `Ready` state write;
- active-GC root-log append and fsync;
- `CURRENT` temporary write, rename, and parent fsync;
- `Published` state write;
- exact old-generation handoff; and
- terminal outcome/acknowledgement.

For every boundary record:

| Observation | Required result |
| --- | --- |
| before durable `CURRENT` | old complete selector visible; private target invisible |
| after durable `CURRENT` | new verified selector visible; old exact generation retained |
| corrupt/ambiguous operation state | no deletion or inferred selection; retain and report |
| response loss | retry returns the durable outcome idempotently |
| disk full | no authoritative or last usable source is removed to make room |

Run restart storms with several incomplete materialization, publication, and
ordinary common operations. Recovery must make progress in 64-record pages and
must not starve non-materialization kinds.

## 7. Concurrency and lock tests

Use deterministic concurrency tests or Loom models for:

- same-key join, owner completion, owner panic, cancellation, timeout, and
  waiter admission;
- per-key registry insert/remove racing with the last waiter;
- permit acquisition/release on every return and unwind;
- `Ready` publication racing with another publisher;
- session admission racing with `CURRENT` switch;
- GC installation/closure racing with publication; and
- shutdown racing with build completion and response delivery.

Instrumentation must prove the lock order:

```text
permits -> per-key ownership -> storage writer lock
```

Under the writer lock, counters for tree walk, carrier verification, directory
enumeration, permit wait, single-flight wait, task join, and payload-provider I/O
must remain zero.

Run:

- 17 same-key waiters: at most 16 wait; excess admission fails boundedly;
- 65 distinct owners: at most 64 enter common nonterminal state, at most four
  own private targets, and excess work remains in bounded admission;
- disjoint keys under `Q = 1, 4, 16, 64`;
- cancellation/panic for each owner/waiter position; and
- shutdown while all worker and queue slots are occupied.

## 8. Resource and malformed-input tests

Exercise each hard limit independently and in combination:

- `B = 64, 256, 1024 MiB`, with effective shared permits capped at
  `min(B,64 MiB)`;
- four global storage workers and a fifth request;
- four materialization `Building`/`Ready` targets, aggregate
  `W_mat=min(4 GiB,10% capacity)`, and a fifth target;
- 16 descriptors / 64 KiB metadata queue;
- 256-KiB hydration buffer;
- 16 FDs per operation / 64 global;
- zero Stage 04.5 mappings;
- 4,096 holds;
- 64 active/pinned generations;
- depth 64 and attempted depth 65;
- eight retries and a ninth failure;
- 256-KiB state/manifest boundary; and
- 64-record recovery pages over histories much larger than 64.

Fuzz object, manifest, `CURRENT`, lease, operation-state, carrier, and path
decoders with:

- zero, maximum, and maximum-plus-one lengths/counts;
- integer overflow in offsets, extents, allocation sums, and count × size;
- truncated/checksum-invalid/unknown-version records;
- duplicate/noncanonical IDs and path components;
- symlink and traversal attempts;
- deeply nested trees and segment counts at/above the cap; and
- metadata that requests excessive `Vec`, map, string, or buffer capacity.

The decoder must reject before excessive allocation or slicing. Run pure
decoder/state tests under Miri where supported and native integration under the
repository-supported address/thread/leak sanitizers. Unsupported tooling is
recorded `OPEN`, not silently omitted.

## 9. Command, PTY, and file fast-path correctness and space

Start from an already warm, admitted materialization and take component-level
allocated-byte snapshots before, at peak, after the operation, and after bounded
quiescence. Exercise:

- no-op `exec_command(["ls"])`, a sustained command batch, nonzero exit,
  stdout/stderr drain, timeout, cancellation, and response loss;
- PTY create, drain, supported `write_stdin`, control-C, control-D, cancellation,
  and the deterministic unsupported responses for resize, arbitrary signal, and
  literal EOF;
- sequential and 4-KiB random file reads and writes through the public
  workspace/file API;
- `stat`, `readdir`, create, rename, fsync, unlink, sparse-file, hardlink,
  symlink, xattr, and many-small-file operations where supported; and
- the same operations at `Q = 1, 4, 16, 64` during cold build, private squash,
  recovery, continuous publication, Stage 05 mark/sweep, and old-generation
  retirement when those Stage 05 paths exist.

For every case:

1. compare content, metadata, exit status, stdout/stderr, PTY stream, fsync
   durability, error, cancellation, and timeout behavior with the matched raw
   LayerStack baseline;
2. assert warm command/file/PTY admission performs no CAS payload read,
   materialization build, locator/history scan, root-log mutation, or maintenance
   worker admission unless the request explicitly publishes;
3. assert no-op, PTY-without-write, file-read, `stat`, and `readdir` cases leave
   zero new durable LayerStack operation, generation, root/object, pack/locator,
   or staging bytes after bounded quiescence;
4. attribute every mutating byte to the session upper/work filesystem or an
   explicit publication; command execution alone cannot create a hidden
   materialization generation;
5. after unlink and teardown, report filesystem slack against the matched raw
   baseline and require zero unexpected LayerStack-owned residue;
6. inject cancellation, panic, `EIO`, response loss, and `ENOSPC` and prove
   permits, buffers, FDs, mounts, tasks, and temporary paths reach bounded
   cleanup without changing `CURRENT`; and
7. keep an old exact-generation reader active while switching `CURRENT` and
   prove its command/file/PTY operations continue on that exact carrier.

Latency and throughput decisions are made by
[the benchmark note](benchmark_note.md). These E2E tests prove route, semantics,
ownership, cleanup, and component-level space attribution.

## 10. Exact cleanup and long-running stability

Run repeated cold build, replacement, squash, session admission, cancellation,
panic, timeout, injected failure, and restart cycles in one process. Do not
restart the process, trim the allocator, purge caches manually, or sleep an
arbitrary duration to manufacture quiescence.

After explicit bounded cleanup, poll until the product-defined deadline and
assert:

- in-flight owners and waiters are zero;
- permits are fully returned;
- queues are at warmed-idle bounds;
- workers are idle in the shared owned pool or joined at shutdown;
- FDs and mappings return to baseline;
- no session mount, lease, upper, or work owner is lost;
- terminal state is reaped or durably retained within its cap;
- private paths are either exactly reaped or named by a live operation; and
- every published old generation is explained as awaiting Stage 05 or held by an
  exact session/pin/authority owner.

Track settled RSS slope and first-to-last delta against Preparation 04's frozen
raw-control noise band and 16-MiB tolerance.

## 11. Cross-stage and authority tests

1. Stage 03 `RootId`, `AttributionRootId`, refs, checkpoints, and OCC remain
   byte-for-byte unchanged by build, repair, and squash.
2. Stage 04 strict candidate mode performs no v1 fallback and no cold work in a
   warm command/file/PTY request.
3. Stage 05's common publisher accepts the `Ready` output without translating
   it into a second materialization state machine.
4. Stage 05 GC/retirement is the only path that can retire a published old
   generation.
5. Stage 06 authority preparation uses ordinary root/source/generation holds and
   the same root-admission fence; Stage 04.5 cannot switch authority.
6. LayerStack never scans or deletes WorkspaceManager, storage-manager, runtime,
   or v1-authoritative paths.

## 12. Exit evidence table

| Suite | Required result | Status |
| --- | --- | --- |
| static deletion/unsafe/owner inventory | no Stage 04.5 deletion; documented unsafe inventory | `NOT_RUN` |
| private build/visibility | verified target invisible until common publish | `NOT_RUN` |
| GC admission interleavings | every visible root admitted or GC aborted/retained | `NOT_RUN` |
| exact-reader generation switch | old sessions retain exact generation | `NOT_RUN` |
| crash/response-loss/ENOSPC matrix | complete old or complete new; uncertainty retains | `NOT_RUN` |
| common recovery paging | bounded fair progress; no skipped operation kind | `NOT_RUN` |
| concurrency and lock instrumentation | caps and lock-order assertions pass | `NOT_RUN` |
| malformed-input fuzzing | no overflow, allocation bomb, or invalid access | `NOT_RUN` |
| Miri/Loom/sanitizers | scoped supported campaigns pass; unsupported cells explicit | `NOT_RUN` |
| command/file/PTY fast path | baseline semantics, no forbidden cold work, exact old-generation behavior | `NOT_RUN` |
| command/file space attribution | zero read-only durable growth; all mutation/cleanup bytes explained | `NOT_RUN` |
| long-running quiescence | resources return to caps; residue explained | `NOT_RUN` |
| Stage 03/04/05/06 compatibility | identities, strict route, lifecycle, authority preserved | `NOT_RUN` |

Stage 04.5 cannot pass on unit tests alone. Required raw performance and space
evidence is tracked separately in [benchmark_note.md](benchmark_note.md).
