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
| attribution update/query | changed attribution pages, stable content IDs, blame query work, no operation-history scan | `NOT_RUN` |
| clean checkpoint/fork | metadata bytes; exactly zero copied payload/native tree | `NOT_RUN` |
| dirty checkpoint | delta equal to publication plus one ref | `NOT_RUN` |
| same-path conflict | stable conflict and bounded work | `NOT_RUN` |
| 2/3+ disjoint writers | throughput, lock wait, retries, progress ratio | `NOT_RUN` |
| lost response/failpoint matrix | exact retry result after restart | `NOT_RUN` |
| v1 source-protection lease | restart/delete attempt and last-locator survival | `NOT_RUN` |
| memory/FD/tasks | every Preparation 04 cap and zero detached tasks | `NOT_RUN` |
| settled/peak space | content/attribution objects, metadata, operations, source-protection leases, unreachable residue | `NOT_RUN` |
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

## Final Stage 03 POC result — 2026-07-25

The initial `NOT_RUN` specification above is retained as history. The final
runner-owned campaign now has this bounded result:

- **overall:** `PASS`;
- **correctness:** `PASS`;
- **performance:** `NOT_RUN/INSUFFICIENT_SAMPLE`;
- **resource locality:** `NOT_RUN/UNAVAILABLE_COMPONENTS`; and
- **full release qualification:** `DEFERRED_STAGE_07`.

This is a Stage 03 correctness and bounded-resource POC pass. It is not a
performance-selection or release-qualification claim.

### Identity and execution

| Field | Final value |
| --- | --- |
| run | `019f977b-752d-7868-927d-170b8d46a078` |
| cell | `sha256:e71292adeb408b5c8629e6ea9a32aa133cf1be8d427f9eb74dabd07e6b7ac371` |
| plan | `layerstack-phase1-stage03-publication`; SHA-256 `5511812675ab2f6784b39b701a333200391e51d6e87e870906d0c454d308d8d6` |
| trial | `trial-4dabd07e6b7ac371-measured-000000` |
| product | baseline commit `cbe45de873cd24fbf48bb7b3a6c5f9f98980313c`; dirty source-diff SHA-256 `d5323b27f1dd7b9e19cf53551162e5608624597b1a9b6aaa9f9dcf1d6b8c8823` |
| test/benchmark | baseline commit `173191e8694515af43797128070dbdfd2d246040`; dirty source-diff SHA-256 `95adf9fddf75d715a464d095cc7e9192d240d3eaa00597b822795e5756c2ba38` |
| profile/seed | `stage03-focused-56mib-v1` / `1392705537` |
| host/target | `Yifans-MacBook-Pro-10.local`; Darwin `25.4.0`; `arm64`; `macOS-26.4.1-arm64-arm-64bit-Mach-O` |
| image | `ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` |
| fixture | 60,323,840-byte archive; SHA-256 `fa624dceba41bcc7fda2be3703a650a8d7ab05819bef9e38f4c36e51183b7a2d` |
| owner corpus | SHA-256 `7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be` |
| private probe | 4,383,592 bytes; SHA-256 `6133d70bcd8e87efd454e2f768f8efff6773bc9331f7d5a934d6fd01ccf012c1` |

The exact command retained by the evidence artifact is:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.benchmark-state/test-venv/bin/python ../.benchmark-state/test-venv/bin/sandbox-benchmark run --plan layerstack-phase1-stage03-publication --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

The runner completed in 137.27 seconds; its measured monotonic campaign
boundary was 136.568017333 seconds, below the 180-second deadline. Exactly one
trial batch and one product request completed without automatic retry.

### Samples and bounded verdicts

The ABBA public-arm order was baseline, candidate, candidate, baseline. Both
public tree pairs were byte-identical; public content mismatches, route
failures, and fallbacks were zero. `legacy_v1` remained the public route
authority.

| Cell | Baseline valid samples / p50 | Candidate valid samples / p50 | Disposition |
| --- | --- | --- | --- |
| first import | 2 / 1.876209834 s | 2 / 2.830067416 s | correctness retained; p95 unavailable |
| no-op | 5 / 117.466917 ms | 5 / 109.831916 ms | correctness retained; p95 unavailable |
| 4 KiB edit, 8 MiB input | 10 / 306.509834 ms | 10 / 341.934500 ms | p95 gate `NOT_RUN/INSUFFICIENT_SAMPLE` |
| 4 KiB edit, 32 MiB input | 10 / 709.438250 ms | 10 / 1.228577083 s | p95 gate `NOT_RUN/INSUFFICIENT_SAMPLE` |

The private probe retained 16 valid samples: three each for clean
checkpoint/fork, dirty checkpoint, two-writer disjoint OCC, three-writer
disjoint OCC, and typed OCC conflict, plus one aggregate F01–F09 recovery
sample. All private minimums passed. Clean checkpoint created zero payload
objects/bytes, dirty checkpoint had the required publication-plus-ref
generation delta, disjoint writers remained visible, three-writer progress
was terminal, conflict was typed/stable, and recovery returned the old or one
complete result.

Complexity variables were retained as `R=1024`, `E=2048`,
`E_changed=1`, `K=4096`, `N=68`, and `Q=2`; `U` and private page count `P`
were explicitly unavailable. The bounded public route does not expose enough
per-edit counters for the full locality formula, so no stronger claim is made.

Candidate high-water evidence retained one active publication/task/worker,
two buffers, one queued item, 33,554,432 queued bytes, and 67,108,864 byte
permits. The strict caps remained encoded as four workers, a 32 KiB ring
window, fan-in eight, 64 KiB readers, 256 KiB encoders, 16 MiB cache, 64
lower layers, 4 MiB publication ownership, 64 MiB global permits, and 384 MiB
RSS. At quiescence the artifact reports zero active owned resources, detached
tasks, strong cycles, route failures, and unexplained residue.

### Artifacts and cleanup

- strict operation evidence:
  `.benchmark-state/results/019f977b-752d-7868-927d-170b8d46a078/cells/sha256:e71292adeb408b5c8629e6ea9a32aa133cf1be8d427f9eb74dabd07e6b7ac371/trials/trial-4dabd07e6b7ac371-measured-000000/bounded-evidence/operation-evidence-e8d7426a22ae22680f0c1597d8dcbfd5d9814539e33aa85287efe23be44ff334.json`;
  SHA-256 `e8d7426a22ae22680f0c1597d8dcbfd5d9814539e33aa85287efe23be44ff334`;
- final report: `.benchmark-state/results/019f977b-752d-7868-927d-170b8d46a078/report.json`;
  SHA-256 `fd919bddc80e50f5c45a26b5b22b476b14aea77e9346df9c76c27ffeffd2ae53`;
- summary: `.benchmark-state/results/019f977b-752d-7868-927d-170b8d46a078/summary.json`;
  SHA-256 `728d3c0d805ccfdc7146e9c3482838adad8b394c23e79702dc1d2c8009a7b464`;
- cleanup ledger SHA-256
  `7cf3607f4a9fb329651ef577393507130c74ba6103cb9a32aa8e1a26069d2059`;
  and
- complete result-boundary SHA-256
  `f5657907f7c00f6bce6970a7c798c450c929866c31584b7ae13cb3623d86a7e5`.

All four arms report sandbox destruction, session retirement, and gateway
closure. Independent inspection found no campaign-owned container, process,
listener, or benchmark runtime entry.
