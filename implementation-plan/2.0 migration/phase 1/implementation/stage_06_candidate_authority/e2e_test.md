# Stage 06 E2E plan — reversible authority

Status: `NOT_RUN`.

## 1. Forward cutover

- quiesce with in-flight v1 publications at each phase;
- import final v1 state, correlate exact manifest/root, materialize, and compare;
- assert correlation/cursor/proof stays inside the bounded migration operation and no
  `refs/legacy` or new legacy directory appears;
- attempt cutover with missing locator, unsupported capability, mismatch, corrupt state,
  or active GC barrier failure; authority remains legacy;
- successful switch yields exactly one new authority epoch and candidate writer;
- retry after response loss returns that epoch.

## 2. Candidate authority

Run publication, checkpoint, reset, revert, checkout, branch promotion, command, file,
PTY, restart, concurrent writer, and GC/materialization cases. Assert the candidate
head is the only publication linearization point, strict native route has no v1
fallback, and every request observes one immutable authority epoch.

Attempt a mutation not v1-representable during the rollback-required window. It must
fail before public visibility rather than silently invalidate rollback.

## 3. Authority rollback

For varied root sizes and all supported logical node types:

- quiesce/drain candidate writers;
- build private v1 state from selected candidate root;
- verify parity before publishing v1;
- inject crash before/after each build sync, v1 manifest commit, final head/epoch
  recheck, `CONTROL` switch, and response;
- assert public authority is complete candidate or complete v1, never two writers;
- after rollback, publish through v1 and prove the public result;
- re-cut over using a fresh import/parity proof.

A diagnostic legacy read of stale v1 must never be labeled authority rollback.

## 4. Concurrency and sessions

- race cutover/rollback with publication admissions, head reset, checkpoint creation,
  GC closure, materialization switch, and session admission;
- epoch fencing yields commit or typed retry, never mixed authority;
- admitted sessions finish on their captured route/leases;
- sessions admitted before a head/authority/materialization switch keep their exact
  leased generation and private upper; later sessions use the new epoch/root;
- quiesce timeout is bounded and leaves authority unchanged;
- shutdown/cancel releases every task, permit, FD, mapping, lease, staging path, and
  authority fence.

## 5. Environment and exposure

Run glibc, musl, minimal/distroless, shell-less, read-only-root, non-root, amd64, and
arm64 target cells on the qualified Linux native backend. Record the effective
kernel/backing filesystem for Linux Engine and Docker Desktop Linux-VM cells. Use
public file/workspace APIs where commands are unavailable. Assert no target helper,
shell, libc/coreutils, package manager, FUSE, reflink, tar, or `cp`, and make no
universal/image-percentage compatibility claim.

## 6. Evidence

Record authority epochs, expected/actual heads, operation IDs, quiesce duration,
import/rollback bytes/time, peak overlap, request tails, route counters, failpoint
outcomes, image digests, commands, revision, and artifact paths.
