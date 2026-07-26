# Stage 04.6 repository materialization baseline

Status: **RECORDED BASELINE — NOT AN ACCEPTANCE GATE**

This record fixes the 2026-07-27 near-1-GiB repository experiment as the
starting point for Stage 04.6 materialization optimization. It deliberately
separates candidate publication/CDC/CAS ingestion from native-carrier
materialization. The `107.024 s` publication result is not the materialization
time.

The reusable Linux integration test remains in the product tree at:

`ephemeral-sandbox/crates/sandbox-runtime/layerstack/tests/repository_materialization_benchmark.rs`

The input corpus, output carrier, machine-readable result, command evidence,
cleanup evidence, and a second copy of the test source remain preserved at:

`/Users/yifanxu/Ephemeral-AI-Lab/experiment/materialization-benchmark-20260727`

Nothing under that experiment directory should be removed or overwritten.
Every replay must use a new results directory.

## Baseline result

| Measured operation | Elapsed | Throughput | Result |
| --- | ---: | ---: | --- |
| Candidate publication / CDC / CAS ingestion | `107.024411507 s` | `8.5247 MB/s` / `8.1298 MiB/s` | matched |
| Cold complete native materialization | `9.987675338 s` | `91.3476 MB/s` / `87.1159 MiB/s` | `Built` |
| Explicit same-key materializer call | `6.361909169 s` | `143.4082 MB/s` / `136.7647 MiB/s` | `Reused` |
| Ordinary warm generation lookup, median of five | `0.035375 ms` | not byte-proportional | same generation |
| Post-measurement preservation copy | `2.046828709 s` | not scored | exact profile |

The optimization reference for complete cold materialization is therefore
`9.987675338 s` for `912,350,100` logical bytes, or `87.1159 MiB/s`. At this
measured rate, a 1-GiB tree would take approximately `11.75 s`. This is a
one-sample extrapolation.

The Stage 04.6 objective is to reduce the cold complete-materialization time
without weakening the existing architecture, authority boundaries, immutable
generation selection, bounded-memory hydration, or complete native-carrier
semantics. Publication, explicit same-key reuse, and ordinary warm lookup must
continue to be reported separately. A faster publication number must not be
presented as a faster materialization number, or vice versa.

This experiment does not establish a main-branch comparison, a native-copy
control, statistical confidence, or a release threshold. Optimization claims
must use repeated matched runs before and after the change. The preserved
single run is the historical starting point, not proof that a small delta is
real.

## Corpus

The copied input is
`ephemeral-sandbox-console/target/release`, preserved as
`experiment/materialization-benchmark-20260727/corpus/console-release`.

| Property | Value |
| --- | ---: |
| Directories | `694` |
| Regular files | `3,602` |
| Logical bytes | `912,350,100` |
| MiB | `870.084858` |
| GiB | `0.849692` |
| Files at least 1 MiB | `214` |

This corpus is mostly compiled Rust artifacts. It is useful for a
large-byte/many-file product-path baseline, but it is not representative of a
typical source checkout.

## Measurement boundaries

1. The test recursively converted the copied corpus into sorted
   `LayerChange` entries.
2. It published those entries through `HiddenValidationPublication`. The
   publication timer includes CDC, hashing, loose-object installation, tree
   construction, and source verification.
3. It started the cold timer immediately before
   `materialize_hidden_candidate`. The returned disposition had to be
   `Built`.
4. It called `materialize_hidden_candidate` a second time under a separate
   timer. The returned disposition had to be `Reused` and select the exact
   same generation.
5. It timed five calls to `lookup_hidden_candidate_generation`, sorted the
   samples, and reported the median.
6. Only after every product measurement did it copy the native carrier to the
   preserved results directory. That copy is not part of publication,
   materialization, or warm lookup timing.

The benchmark ran as one Linux integration test in a network-disabled Docker
container. Product state was created on the container's writable Linux
filesystem. The corpus and output directory were bind-mounted; the compiled
test executable and corpus mount were read-only.

## Correctness observations

- Cold materialization returned `Built`, generation `1`.
- The explicit same-key call returned `Reused`.
- Every warm lookup selected the identical generation.
- Maximum hydration buffer usage was `262,140` bytes.
- Source, live carrier, and preserved carrier profiles were identical:
  `694` directories, `3,602` files, and `912,350,100` logical bytes.
- The final recursive file comparison was byte-for-byte clean.
- Manifest SHA-256:
  `cfe8e5898f7a2185ba70a273554cb5255541b841d33de6b526b16e6f5029493b`.
- Native tree SHA-256:
  `e84c8a8cea89c9f65a3163a4947b753bc07c736af885d227db91732c181ea400`.
- The run-scoped Docker container was removed after the test.

These checks are required invariants for future optimization comparisons.

## Source and environment

The experiment was executed from:

- product branch: `upgrade-2.0-phase-1`;
- product HEAD: `68c6e2bdeb490c2e7a24f3791dba865c38d9e737`;
- worktree: dirty, containing the in-progress Stage 04.5 implementation;
- host: Apple M3 Max, arm64, 36 GiB RAM;
- host OS: macOS `26.4.1` (`25E253`);
- Docker client/server: `29.5.2`;
- Rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`;
- target: `aarch64-unknown-linux-musl`;
- image:
  `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`;
- Docker network: `none`.

Because the product worktree was dirty, the HEAD alone does not reconstruct
the tested implementation. The immutable command evidence, result JSON,
preserved carrier, test-source hash, and append-only Stage 04.5 test report are
the authoritative record for this run.

## Commands and evidence

The test executable was built with:

```bash
cargo zigbuild --locked \
  -p sandbox-runtime-layerstack \
  --target aarch64-unknown-linux-musl \
  --release \
  --test repository_materialization_benchmark
```

The exact historical `docker run` argv, timestamps, stdout, stderr, exit
status, and per-step elapsed times are stored in:

`experiment/materialization-benchmark-20260727/results/CMD-S045-492.json`

The recursive comparison and run-scoped cleanup record is:

`experiment/materialization-benchmark-20260727/results/CMD-S045-493.json`

The append-only narrative record is in
`ephemeral-sandbox-test/e2e/test-report.md`, Iterations 467 and 468.

Small-artifact SHA-256 values:

| Artifact | SHA-256 |
| --- | --- |
| Integration test source | `2fb799359a5f243e52ac680dd28fae1d0484dd5eb7d49bf4237874b9393f904d` |
| `benchmark.json` | `614a64e999b07f1a2565aa801cd95e4551f3cfad3af2076463dbdad5c650c908` |
| `CMD-S045-492.json` | `424c62b1a5cf7958699d5318c6dd872c52f796609c0b04cc20538cb23e74cea3` |
| `CMD-S045-493.json` | `f84618fc44e1aec971fa66ab8e664c031a1ad3813f413be467358cd44dc974b9` |

The structured values needed by automation are duplicated in
[`baseline.json`](baseline.json). Future runs should retain their raw output
beside the preserved experiment and add, rather than replace, comparison
records here.

## Expanded Stage 04.6 experiment plan

Status: **PLANNED — NOT YET MEASURED**

The recorded run above remains immutable. Stage 04.6 comparisons add new
run-scoped result directories and never rewrite `baseline.json` or the
preserved evidence. The optimization targets, formulas, and space gates are in
the [Stage 04.6 optimization plan](../plan.md).

Every comparison must time and report these boundaries separately:

1. fixture creation or mutation, excluded from product-path scores;
2. publication, including CDC, hashing, CAS installation, and tree creation;
3. native carrier construction or frozen-upper promotion;
4. carrier verification and immutable-generation publication;
5. workspace activation and first-command readiness;
6. exact-key reuse or reactivation;
7. logical squash and, when intentionally requested, physical flattening; and
8. untimed preservation and cleanup.

Network time is never included. A cold run means that no compatible native
carrier exists for the requested backend key. A warm run identifies whether it
is an exact catalog lookup, carrier-chain activation, or locality-pool hit.
Dropping the host page cache is a separate qualification cell, not an implicit
part of every cold run.

### Comparison protocol

- Compare the current complete-carrier implementation, a pinned
  legacy/main-branch raw-overlay materialization path, a direct native-copy
  control, and the Stage 04.6 candidate on identical copied fixtures. Record
  the exact commit and dirty-state evidence for every product control.
- Use an interleaved `ABBA` or `BAAB` order to reduce thermal and storage-order
  bias.
- Collect at least 20 matched samples for p50 and p95 claims. Report p99 only
  with at least 100 samples.
- Report logical and allocated bytes, bytes read, bytes written, bytes hashed,
  reconstructed bytes, newly retained CAS bytes, and native delta bytes.
- Report peak and final RSS, open-file high-water mark, queue depth, worker and
  byte-permit high-water marks, and every space-model term.
- Preserve raw per-sample output and machine-readable comparison results in a
  new append-only experiment directory.

### Corpus matrix

| ID | Corpus | Minimum shape | Purpose |
| --- | --- | --- | --- |
| `B0` | Preserved compiled-Rust corpus | `870.08 MiB`, `3,602` files | Historical matched reference |
| `B1` | Source tree / many-small | `≥512 MiB`, `≥20,000` files | Metadata, directory, and source-workload cost |
| `B2` | No-dedup binaries | `1 GiB` allocated | Worst-case payload and write throughput |
| `B3` | Mixed software repository | `1 GiB`; small, medium, and large files | Representative multi-language project |
| `B4` | Deduplication history | One base plus 64 retained small mutations | CAS uniqueness and retained-space behavior |
| `B5` | Localized large-file edit | At least one `100 MiB` file | One-byte, `4 KiB`, and `64 KiB` in-file edits |
| `B6-pip` | Offline Python environment | Target `≈250 MiB`, `≥12,000` entries | Install, upgrade, and uninstall churn |
| `B6-npm` | Offline Node environment | Target `≈350 MiB`, `≥25,000` entries | Nested tree, lockfile, bin-link, and removal churn |

All normal qualification corpora must fit the supported file representation.
An additional large-file boundary test must verify bounded rejection at the
current limit and bounded success after any hierarchical segment format is
introduced. The test must never obtain a result by simply removing a segment
or memory cap.

### Mutation and filesystem-operation matrix

Run applicable operations against `B1` through `B6`, preserving the exact root
and parent identity for every sample:

- no-op publication and exact-key reuse;
- one small-file edit of at most `64 KiB`;
- `1 MiB` of edits distributed across at most 100 files;
- one-byte, `4 KiB`, and `64 KiB` edits inside a `100 MiB` file;
- create, overwrite, append, truncate, unlink, rename, and cross-directory
  rename;
- file/directory/symlink type replacement;
- directory merge, recursive removal, whiteout, and opaque-directory behavior;
- executable-bit and ordinary mode changes;
- ownership, timestamp, and supported xattr changes;
- relative and absolute symlinks, hardlinks, and sparse files; and
- logical squash at several chain depths plus an intentionally requested
  physical flatten.

Correctness comparison includes bytes, entry type, mode, supported ownership
and timestamp fields, xattrs, symlink target, hardlink relationship where
promised by the backend, sparse allocation where promised, and absence of
deleted or opaque-hidden paths.

### Offline `pip` and `npm` workloads

The package-manager fixtures are deterministic local archives. Fixture
generation and archive acquisition occur before the timed window, and the
container remains network-disabled. The workloads emulate the filesystem
effects that matter to the product:

- archive extraction into a private upper;
- duplicate package payload shared across sibling branches;
- metadata and lockfile writes;
- temporary-file write followed by atomic rename;
- executable or `.bin` symlink creation;
- package upgrade with overwrite and deletion; and
- uninstall or removal of a subtree.

Record mutation application separately from seal, publish, materialize, and
activate. This makes the score about the CAS/native-carrier path, not Python,
Node, decompression, or network speed.

### Multi-agent and parallel-rollout matrix

The Stage 04.6 design is qualified as infrastructure for multi-agent software
development:

- Create 64 and 1,000 inactive forks from a `1 GiB` root. They retain immutable
  roots, references, and bounded metadata only; they must allocate zero native
  repository payload per inactive fork.
- Activate `1`, `4`, and `16` sibling attempts, or the configured lower pool
  cap. Each receives a private upper while sharing immutable lower carriers.
- Run 32 sibling tiny-edit publications, then reactivate a selected winner and
  measure both a locality hit and a cold worker.
- Interleave Python and Node package mutations with source edits across
  siblings and prove that no sibling can observe another sibling's upper.
- Saturate the materialization worker and byte-permit limits and verify bounded
  backpressure, cancellation, and recovery without deadlock.
- Checkpoint several depths, perform a logical squash, and prove that inactive
  nodes do not acquire permanent native materializations.

These experiments measure construction, selection, activation, and space.
They do not add Stage 5–7 deletion, packing, locator, eviction, or garbage
collection behavior.

### Required result record

Each row must include the implementation ID, backend key, corpus and mutation
ID, root and parent root, chain depth, cold/warm classification, sample count,
p50/p95 and optional p99 latency, logical and allocated bytes, throughput, and
correctness verdict. Space reporting must include:

```text
T(t) = L_hot(t) + H_cold(t) + sum(U_active(t)) + P_staging(t) + M(t)
D_ideal = C_current + H_unique
```

Also report settled amplification, avoidable duplicate payload, CAS unique
bytes, native delta bytes, lease-protected bytes, and unexplained bytes.
Performance results are invalid if a correctness, boundedness, or space gate
fails.
