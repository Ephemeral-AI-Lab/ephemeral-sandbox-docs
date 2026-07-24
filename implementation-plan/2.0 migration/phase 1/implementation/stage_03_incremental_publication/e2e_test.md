# Stage 03 E2E plan — private incremental publication

Status: `NOT_RUN`.

Use public workspace/file APIs for workload mutation and authenticated observations for
bounded counters. Tests must not inspect private implementation files as a substitute
for public behavior; dedicated crash harnesses may inspect exact recovery state.

## 1. Identity and codec cases

1. Re-run all immutable v2 golden vectors unchanged.
2. Verify v3 root/tree/file/segment/chunk and attribution root/page golden bytes and
   typed IDs.
3. Prove identical v3 IDs across amd64/arm64 and supported host filesystems.
4. Reject wrong object kind, trailing bytes, unsorted/duplicate entries, oversized
   pages/lengths, dangling edges, invalid sparse ranges, and unknown required
   capabilities without oversized allocation.
5. Stream a v3 root as a flat manifest and reconstruct the same logical tree; prove the
   flat stream is never used to compute the root.

## 2. Publication correctness

Cover empty tree; nested directories; large and tiny files; sparse/zero regions; raw
Linux byte paths; xattrs; hardlinks; symlinks; devices/FIFOs where supported; deletion;
opaque directory; rename; truncate; append; and metadata-only change.

For each:

- publish to a private head;
- independently reconstruct/compare the exact final logical tree;
- verify unchanged chunk/page IDs are shared;
- verify only changed paths and ancestors are read/rewritten;
- restart and repeat the comparison.

For attribution, prove that unchanged paths/ranges share attribution pages, changed
paths receive the stable logical actor/publication attribution, identical content from
different actors keeps the same content IDs but different attribution IDs, and blame
lookup never scans retained operation history.

## 3. Ref semantics

- clean checkpoint and clean branch/MCTS fork allocate one content/attribution
  ref/head, zero payload, and no complete native tree;
- dirty checkpoint has the same object/page delta as ordinary publication plus one ref;
- checkout changes session selection but no head;
- revert advances generation through a publication event, may reuse the historical
  content root, and attributes reverted paths to the reverting actor;
- reset moves the head to an existing historical content/attribution pair with no new
  logical or attribution objects;
- checkpoint content and attribution survive later reset, compaction, squash, GC, and
  restart;
- deleting a checkpoint does not synchronously delete payload.

## 4. OCC and progress

Run two and at least three writers:

- identical path and directory metadata changes conflict;
- ancestor removal versus descendant change conflicts;
- rename source/destination overlap conflicts;
- opaque subtree versus descendant change conflicts;
- hardlink-group overlap conflicts;
- truly disjoint paths rebase and both become visible;
- retries are bounded and typed contention is returned rather than starvation/hang;
- measured disjoint throughput meets Preparation 04.

No test may implement OCC by collecting the complete path set in memory.

## 5. Idempotency and failpoints

Inject process death or I/O failure:

1. before operation state;
2. during changed-path spill;
3. during chunk/page install;
4. after objects/root are durable;
5. after prepared state;
6. during GC-barrier registration when active is simulated;
7. before head rename;
8. after head rename and before terminal outcome;
9. after terminal outcome and before response.

After restart, the head is old or the one complete result. Retrying the same
`PublicationId` returns the exact result/conflict. Different input under the same ID is
rejected. A branch cannot advance past a missing terminal outcome for its current
`head.publication_id`. Expired/acknowledged IDs return `OutcomeExpired`, never publish.

## 6. Existing v1 source safety and validation mode

- import a root whose last payload location is a v1 carrier;
- prove an ordinary fenced locator/source lease exists before candidate ref visibility;
- crash/restart and attempt legacy squash/delete; candidate reconstruction remains
  possible;
- prove no `refs/legacy` directory or mapping record is created;
- turn optional validation on/off repeatedly without new storage schemas;
- correlate candidate and v1 results and report bounded mismatches;
- prove validation never changes public authority or delays v1 beyond its declared
  admission/backpressure contract.

## 7. Boundedness and exposure

- run the largest Preparation 04 corpus under RSS/FD/task/queue instrumentation;
- assert all configured maxima and zero detached tasks/strong cycles;
- assert no resident total-tree/history/all-live set;
- assert `/eos` candidate paths remain masked from workloads;
- assert publication reads only the admitted session's `upper` as changed input and
  does not ingest `work`, `executions`, `/eos/storage`, or `/eos/runtime`;
- verify shell-less/read-only/non-root cases through public APIs;
- verify no new dependency or target helper is invoked.

## 8. Exit evidence

Record commands, git revision, host/target matrix, fixture hashes, failpoint IDs,
observed content/attribution object and page reads/writes, lock wait/retry counts,
memory/FD/task peaks, source-protection-lease evidence, and artifact paths in
`benchmark_note.md`. Architecture inspection alone cannot pass a case.
