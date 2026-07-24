# Stage 03 benchmark note

Status: **NOT_RUN**. This specification records gates, not results.

Normative thresholds are in
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md).

## Required cells

| Cell | Required evidence | Result |
| --- | --- | --- |
| first import | time, bytes read/written, entries, peak RSS; `O(R+E)` trend | `NOT_RUN` |
| 4 KiB middle edit in growing tree | changed bytes/chunks/pages, unchanged-tree reads, elapsed scaling | `NOT_RUN` |
| append/truncate/metadata/delete/rename | per-operation input and touched-page counters | `NOT_RUN` |
| no-op | capture evidence and zero new payload | `NOT_RUN` |
| clean checkpoint/fork | metadata bytes; exactly zero copied payload/native tree | `NOT_RUN` |
| dirty checkpoint | delta equal to publication plus one ref | `NOT_RUN` |
| same-path conflict | stable conflict and bounded work | `NOT_RUN` |
| 2/3+ disjoint writers | throughput, lock wait, retries, progress ratio | `NOT_RUN` |
| lost response/failpoint matrix | exact retry result after restart | `NOT_RUN` |
| v1 source hold | restart/delete attempt and last-locator survival | `NOT_RUN` |
| memory/FD/tasks | every Preparation 04 cap and zero detached tasks | `NOT_RUN` |
| settled/peak space | objects, metadata, operations, source holds, unreachable residue | `NOT_RUN` |
| host/architecture determinism | identical chunk/page/root IDs | `NOT_RUN` |

## Required report fields

- exact command, revision, profile, corpus/fixture digest, host and target;
- median/tail samples and raw artifact path;
- `R,E,U,E_changed,K,P,N,Q` for the cell;
- object/page read/write counts and bytes;
- complete-tree/history scan counters;
- peak/settled logical, physical, staging, and metadata bytes;
- RSS, worker/task, queue, FD, mapping, and lock-wait peaks;
- threshold, measured result, `PASS`/`FAIL`, and variance explanation.

Do not report `PASS` because the implementation is expected to be incremental.
