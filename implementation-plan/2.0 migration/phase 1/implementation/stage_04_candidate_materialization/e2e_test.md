# Stage 04 E2E plan — materialization and activation

Status: `NOT_RUN`.

[Stage 04.5](../stage_04_5_materialization_gc_alignment/e2e_test.md)
supersedes this plan for common publication, bounded recovery/resource ownership,
and generation retirement. Stage 04 E2E must not exercise a direct generation
deletion path.

Entry evidence and inherited invariants are recorded in
[`handoff_from_stage_03.md`](handoff_from_stage_03.md). Stage 04 execution must
preserve the Stage 03 v2/v3 identities, public `legacy_v1` authority, exact
retry/recovery behavior, source holds, GC barriers, PTY drain ordering, and
shared-worktree custody named there.

## 1. Reconstruction matrix

Materialize roots covering empty/deep/wide trees, large/tiny/sparse files, raw byte
paths, xattrs, hardlinks, symlinks, metadata-only nodes, devices/FIFOs when supported,
and deleted/opaque/renamed paths. Compare through public file/workspace APIs with the
logical root and v1 reference result.

Verify:

- every typed object and final root is checked;
- unsupported required capability fails closed;
- a second request reuses the valid generation;
- concurrent same-key cold requests produce one fenced build/selected generation and
  bounded waiters; crash-race orphan bytes remain bounded and collectible;
- only active or explicitly pinned roots have materializations;
- a retained checkpoint alone does not force a native tree.

## 2. Strict route

In explicit candidate mode run command, file, PTY, workspace, restart, and concurrent
session cases. Authenticated counters must show:

- candidate plan selected;
- no legacy read fallback;
- no CDC, object traversal, hashing, locator merge, pack, GC, squash, or cold build in
  the request path;
- mount depth at most 64;
- missing/corrupt generation returns a typed error before workload mutation.

Shell-less/read-only targets use public file/workspace APIs instead of assuming a shell.

## 3. Failure injection

Crash/fail before carrier creation, during reconstruction, after native sync, after
manifest fsync, before/after `CURRENT`, during session admission, during unmount, and
after response loss. Restart must select exactly the old or complete new generation,
never partial output. Repeating the same materialization operation returns the selected
generation.

Delete/corrupt a non-current orphan and current/last carrier separately. The orphan is
recoverable; the current/last case fails closed and retains source/object data.

## 4. Lifecycle and concurrency

- multiple sessions share a read-only generation and own independent uppers;
- each session lease names the exact generation/fence and each session has a distinct
  `upper`, `work`, `executions`, and mount namespace;
- switching `CURRENT` does not invalidate an admitted session;
- publishing a new branch head does not remount or mutate admitted sessions; a new or
  explicitly checked-out session selects the new root;
- Stage 04 retains old generations and exposes exact lease/hold evidence for
  Stage 05; only Stage 05 tests deletion eligibility and unlink;
- cancellation, panic, timeout, daemon shutdown, and restart leave no detached task,
  permit, FD, mapping, mount, or temporary path;
- build admission, FD pressure, mapping pressure, and upper-space exhaustion apply
  bounded backpressure.
- current/pinned materialization and staging-byte quotas reject admission before disk
  use becomes unbounded; active leased generations are never quota-evicted.

## 5. Branch/MCTS cases

Create many inactive clean forks and assert metadata-only growth. Activate a bounded
subset and assert only those allocate private uppers/materializations. Publish
independent changes and prove native depth does not track logical ancestry.

## 6. Exit evidence

Run the Linux backend on Docker Engine/Linux and supported Docker Desktop Linux-VM
cells with qualified backing filesystems. Record the effective guest kernel and
filesystem. Treat bind mounts, translated APFS/NTFS, NFS/SMB, and other backing stores
as separate qualification cells, never as implied support. No “95% of images” or
universal compatibility result may be inferred.

Record route counters, cold bytes/entries/time, warm latency distribution, depth,
materialization/upper allocated bytes, duplicate peak, RSS, workers/tasks/FDs/mappings,
lease fences, failpoint recovery, image/backend/backing-filesystem matrix, commands,
revision, and artifacts in `benchmark_note.md`.
