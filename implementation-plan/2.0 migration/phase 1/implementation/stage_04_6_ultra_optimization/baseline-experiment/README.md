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

At the time of recording, the immediate objective was to reduce cold complete
carrier construction. The subsequent architecture review broadens that goal:
avoid complete construction on normal post-setup operations while preserving
authority, identity, boundedness, and a qualified OCI directory fallback.
Publication, explicit same-key reuse, ordinary warm lookup, projection-ready,
and deferred access costs continue to be reported separately. A faster
publication number must not be presented as faster materialization, or vice
versa.

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
preserved evidence. The selected architecture, target formulas, decision
record, and hard falsifiers are in the
[Stage 04.6 implementation plan](../new_plan.md). The older `plan.md`,
`review.md`, and `portable_split_cow.md` are historical design inputs. The
normative lifecycle authority is ratified
[`SD-04.6-001`](../requirements_and_prohibitions.md#31-ratified-specification-decision-sd-046-001):
candidate canonical publication uses a closing seal-and-publish boundary, with
post-commit successor restart measured separately when requested. Same-upper
non-closing rows are pinned `I0`/`I2` compatibility controls only, not `I3`
acceptance gates or release blockers.

The absolute reference ceilings remain reported for first ingestion,
publication, and activation. First ingestion is scored against both
`1.070 s` / `214 ms` and its measured one-pass physical floor. Normal
incremental publication and stored-projection activation must meet the
applicable 100x gate. Setup may be excluded only when no product operation
performs it.

The historical timers are retained as exact inner-span controls, but their
boundaries are incomplete for a new product claim: source walk, `stat`,
ordering, and `LayerChange` creation preceded the `107.024 s` timer, while
carrier profiling and actual activation followed the `9.988 s` timer. New
campaigns record both matched inner spans and outer operation-to-readiness
clocks.

Every comparison must time and report these boundaries separately:

1. fixture preparation and network acquisition, separately reported and
   excluded only because the product does not perform them;
2. very first source-open/walk through durable resolvable root;
3. historical prepared-`LayerChange` publication span;
4. legacy/control-only non-closing post-setup logical checkpoint/add-layer on
   `I0`/`I2`, from before admission and tracker enumeration through durable
   root/ref, recorder-epoch advance in the same upper, and next-command
   readiness, with receipt hit and miss separated; this row is never an `I3`
   candidate gate or speedup denominator;
5. candidate closing `seal_publish` from before admission through the durable
   `PublicationCommitted` timestamp/acknowledgement, session close, upper
   ownership adoption, and durable ref. That is the publication
   constituent. A coupled request additionally records successor-workspace
   readiness and the final combined response as distinct post-commit clocks;
6. raw-upper normalization from before freeze/first enumeration through a
   durable normalized delta and semantic receipt;
7. exact frozen-recipe handoff from before lookup through compatible
   receipt/generation selection, dependency pinning, and readiness probe;
8. projection miss/build from before root resolution/build decision through a
   durable immutable projection receipt, with activation separate;
9. workspace-ready activation plus an adapter-owned, image-independent
   namespace/read probe over a known fixture path;
10. first open/byte, first selected-file read, metadata walk, byte-reading full
   scan, deterministic random reads, and first write/fsync/copy-up;
11. exact-key reuse from immediately before lookup through generation
    selection, dependency pinning, and readiness probe;
12. winner reactivation from before selected-root resolution/placement through
    a usable probed target, split into warm-local, cold-local, and remote/cold;
13. public `squash_layerstacks` logical ancestry prune and, as a separate
    requested maintenance operation, physical flatten;
14. rollback through target-root readiness;
15. public response and asynchronous settle/reclamation latency, distinguishing
    physical deletion from transfer to inventoried `PayloadStore` ownership;
    and
16. untimed artifact preservation after every product and cleanup check.

Record every publication/ref, successor activation, and combined outer outcome
as separate fields and denominators, each with attempts, successes, failures,
and success rate. `CommittedActivationFailed` counts as publication success and
activation/combined-lifecycle failure; it remains in every applicable
denominator and MUST NOT be discarded or retried until it looks successful. A
same-`PublicationId` retry must prove that no second ref update occurs. Inject
crashes after ref commit and before activation start, activation terminal
persistence, and combined response delivery. Success-only latency percentiles
are diagnostic; any `ActivationFailed` fails a success-required activation or
combined cell.

For `I1`, the direct native-copy clock starts before source open/walk and ends
only after the complete destination namespace, semantic oracle, durability
sync, and the same adapter-owned readiness probe pass. It does not use
durable-root publication as a substitute end boundary.

`I0` is a pinned, reproducible control rather than an already-warm workspace.
Freeze the exact main commit and dirty-state evidence, OCI index/platform
digest, Docker/kernel/storage-driver/backing-filesystem tuple, OverlayFS
options, and capability receipt. The once-only sandbox/base-workspace setup
may occur outside a post-setup sample, but every sample gets a fresh private
upper/work pair and no receipt or projection artifact from `I2`/`I3`. Run the
same product mutation and readiness probe through pinned main. A non-closing
publication clock starts before admission/tracker enumeration and ends only
when the root/ref are durable and the same upper passes the next-command
probe; it is `I0`/`I2` control evidence only. An `I3` closing-session
publication constituent instead ends at its durable `PublicationCommitted`
timestamp/acknowledgement, session close, stationary ownership adoption of the
same upper allocation, and durable ref. It never deletes that allocation. A
coupled final response belongs to the combined clock.
Activation starts before root/projection selection and ends after the adapter
probe. Record
raw-OverlayFS mutation/copy-up, pinned-main publication, sync, response, and
settlement subspans. Product-required network work stays inside the outer
timer and is also a named subspan.

External fixture/archive/image acquisition is separately reported and excluded
only when the product does not perform it. Every product-required network
action—including an image pull triggered by create, remote checkpoint/object
fetch, and lazy remote read—remains inside the outer operation clock and is
also reported as a network subspan.

Package execution/decompression can be a separate span; the combined
write-plus-publish clock is still mandatory. A cold run records projection
presence, worker placement, page-cache state, and remote/local payload state.
Dropping the host page cache is a separate qualification cell, not an
unreported assumption.

Every cold deferred-cost metric uses a fresh identical activation and declared
worker/cache/remote state. A full scan must not precede a supposedly cold
random read, first-file read, or first write. If cache reset cannot be proved,
label the cell `cache state unknown`, not cold. Random reads use a versioned
seed, declared read count, offsets/alignment, file-size strata, touched-byte
count, checksum, p50/p95/p99, and throughput. A qualified random-read row has
at least 100 measured samples; an `n=20` p50/p95-only row is explicitly
unqualified diagnostic evidence. Full scans compute and verify a checksum
inside the timer.

No expensive required work may move before the relevant outer timer. When
`AttemptSealer` overlaps hashing or durability with an idle epoch, report
checkpoint-call latency **and** mutation-to-durable-root latency, dirty bytes,
sync method/count, and `syncfs` interference.

### Comparison protocol

- Compare four explicit implementations on identical copied fixtures:
  `I0` pinned main/raw-overlay, `I1` direct native-copy,
  `I2` current CAS complete-carrier, and `I3` the Stage 04.6 candidate with
  its projection/accelerator mode in the sample key. Record the exact commit
  and dirty-state evidence for every product control.
- Qualify the portable no-accelerator `I3` path independently. Accelerator
  modes use separate sample keys and MUST NOT rescue or be pooled with a miss
  on the required portable path.
- Split publication controls into explicit, unpooled modes. The retired
  `legacy_nonclosing_compatibility` mode exists only on pinned `I0`/`I2`. A
  publication speedup denominator must instead be a
  `matched_closing_publication_control` on pinned `I0` or `I2`: the harness
  uses the same request shape, fences and drains admission, makes the old
  session terminal, includes its implementation's durable root/ref work, and
  stops only when the old session is closed and the publication constituent is
  durable. Any requested successor activation uses a fresh upper and a
  separate clock. If a pinned control cannot expose this closing semantic and
  timing boundary, record the comparator `BLOCKED` and the publication ratio
  `UNKNOWN`; never substitute the non-closing compatibility row.
- Use a predeclared balanced four-treatment Williams crossover in complete
  blocks: `I0 I1 I3 I2`, `I1 I2 I0 I3`, `I2 I3 I1 I0`, and
  `I3 I0 I2 I1`, with a fresh matched fixture copy per run. If complete
  four-way blocks are impossible, run separately reported pairwise
  `I3`-versus-control ABBA/BAAB blocks; never pool the designs silently.
- Collect at least 100 matched measured samples after declared warmup for every
  qualified row and report mandatory p50, p95, and p99. An `n=20` p50/p95 row
  may be retained only as explicitly unqualified diagnostic evidence.
- The preserved `baseline.json` has `n=1` for publication, materialization,
  and reuse and `n=5` for warm lookup. Its thresholds are absolute ceilings,
  not percentile evidence. Any 100x label requires candidate p95 no greater
  than both the applicable historical ceiling and
  `matched_current_p95 / 100`; any 500x label requires both its historical
  ceiling and `matched_current_p95 / 500`. Matched distributions use identical
  outer boundaries/cache/placement. Any sub-millisecond claim requires at
  least 100 matched samples.
- Report receipt-hit rate per workload. The primary small-edit campaign also
  forces an immediate-post-command receipt miss and times mutation,
  invalidation, scan/hash, dirty writeback, sync, durable root, and requested
  readiness in one combined cell.
- Freeze and compare the exact dependency contract from
  [prep §11.1](../../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md#111-zero-new-external-dependency-contract):
  lockfile package/version identities, enabled external features, the
  product-wide multiset of direct external manifest edges,
  system/helper/target-image commands, and build/runtime downloads. Any
  unexplained delta is a release failure.
- Report logical and allocated bytes, bytes discovered, read, written, hashed,
  hash-reused, reconstructed, adopted, packed, deferred, and evacuated.
- Report peak and final RSS, open-file high-water mark, queue depth, worker and
  byte-permit high-water marks, mounts, inodes, leases, sync/fsync calls,
  dirty-byte writeback, page/dentry cache where attributable, and every
  space-model term.
- Preserve raw per-sample output and machine-readable comparison results in a
  new append-only experiment directory.

### Corpus matrix

| ID | Corpus | Minimum shape | Purpose |
| --- | --- | --- | --- |
| `B0` | Preserved compiled-Rust corpus | `870.08 MiB`, `3,602` files | Historical matched reference |
| `B1` | Mixed software repository | recorded `1 GiB`; small, medium, large, sparse, and linked files | Representative multi-language project |
| `B2a` | Many-small qualification | `≥20,000` regular small files; record directories/symlinks separately | Lower metadata scale |
| `B2b` | Many-small qualification | `≥100,000` regular small files; record directories/symlinks separately | Required metadata and package scale |
| `B2c` | Many-small stress | `1,000,000` entries | Bounded streaming, inode, and recovery stress |
| `B3a` | Localized large file | one `100 MiB` file | Whole-file versus range behavior |
| `B3b` | Localized large file | one `1 GiB` file | Required one-byte large-file challenge |
| `B3c` | Adversarial SeqCDC large file | one `1 GiB` deterministic near-min-cut stream, plus a synthetic 131,072-range owner-manifest boundary case | Prove reverse-manifest sharding and forbid a 100,000-range owner rejection |
| `B4` | No-dedup and retained history | `1 GiB` allocated; base plus 64 mutations | Worst-case payload, uniqueness, and retention |
| `B5-pip` | Deterministic offline/fake Python environment | normal, `≥100k`, and stress-only `1M` entry shapes | Install, upgrade, uninstall, cancellation |
| `B5-npm` | Deterministic offline/fake Node environment | normal, `≥100k`, and stress-only `1M` entry shapes | Install, update, removal, cancellation |

All normal qualification corpora must fit the current canonical v3 file
representation. The recommended `I3` path must successfully ingest,
reconstruct, activate, edit deterministic beginning/middle/end offsets,
publish, roll back, and reactivate `B3b` and `B3c` while preserving golden IDs and every
declared RSS/working-set limit. `I3` rejection, truncation, or a weakened
fixture is a hard falsifier. A legacy control may explicitly reject only when
that is its real pinned behavior; rejection is recorded as a control
limitation, never a candidate pass. Build and reconstruction use bounded
streaming cursors. The test must never obtain a result by removing a segment
or memory cap. Record `B3c`'s actual SeqCDC count; regardless of how closely
the byte generator approaches the theoretical maximum, the synthetic
owner-manifest case must atomically select and traverse all 131,072 ranges in
two or fewer 100,000-entry shards.

### Mutation and filesystem-operation matrix

Run applicable operations against every corpus ID above, with every omission
explicitly marked and the exact root and parent identity preserved:

- no-op publication and exact-key reuse;
- one small-file edit of at most `64 KiB`;
- `1 MiB` of edits distributed across at most 100 files;
- one-byte, `4 KiB`, and `64 KiB` edits at deterministic beginning, middle,
  and end offsets inside both `100 MiB` and `1 GiB` files;
- create, overwrite, append, truncate, unlink, rename, and cross-directory
  rename;
- file/directory/symlink type replacement;
- directory merge, recursive removal, whiteout, and opaque-directory behavior;
- executable-bit and ordinary mode changes;
- ownership, timestamp, and supported xattr changes;
- relative and absolute symlinks, hardlinks, and sparse files; and
- public `squash_layerstacks` logical ancestry prune at several history
  depths plus a separately requested physical flatten.

Correctness comparison preserves the existing canonical v3 contract: raw path
bytes; regular/directory/symlink/FIFO/device entries represented by v3; exact
bytes and hole extents; full mode bits; canonical `u32` UID/GID and mtime;
relative and absolute symlink targets; exact xattr bytes including encoded
ACLs/capabilities; hardlink identity, mutation behavior, and observable
`st_nlink`; rename/delete; and sparse files. A placement that lacks authority
or filesystem support must return the expected capability-placement error,
not publish or accept a weakened root. Physical sparseness and allocated
extents are separately measured space properties. Deleted and opaque-hidden
paths must be absent.

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

Record package execution/decompression separately from seal, publish,
materialize, and activate. Also record the combined execution-through-ready
clock. This prevents package runtime from obscuring storage cost without
allowing storage work to escape the product boundary.

### Multi-agent and parallel-rollout matrix

The Stage 04.6 design is qualified as infrastructure for multi-agent software
development:

- Create 64 and 1,000 inactive forks from a `1 GiB` root. No per-node/private
  native repository projection or payload may be caused by the fork; shared
  payload-store allocations and unique logical-history payload are counted
  once.
- Always submit `1`, `4`, and `16` sibling attempts. Each admitted attempt
  receives a private upper while sharing immutable lower projections. If the
  configured cap is below 16, report admitted, queued/backpressured/rejected,
  first-ready, last-ready, and total completion rather than skipping the cell.
- Run 32 sibling tiny-edit publications, then reactivate a selected winner and
  measure three distinct placements: warm-local; cold page cache with a local
  stored projection; and a genuinely empty worker with neither projection nor
  payload. The empty-worker acquisition/build remains inside its timer and is
  scored against the direct transfer/native-copy floor, not mislabeled as a
  100x stored-projection activation.
- Interleave Python and Node package mutations with source edits across
  siblings and prove that no sibling can observe another sibling's upper.
- Saturate the materialization worker and byte-permit limits and verify bounded
  backpressure, cancellation, and recovery without deadlock.
- When legacy compatibility evidence is reported, run 64- and 1,000-operation
  non-closing logical-layer campaigns on pinned `I0` and `I2` only. Every
  sample starts before
  admission/queue/backpressure and ends only after the root/ref are durable
  and the same upper accepts and passes a next-command probe. All forced
  synchronous work and any delay induced by earlier maintenance remain timed.
  Report the former `<=1.070 s p95`/max and preferred `<=214 ms p95` thresholds
  as compatibility-control comparisons, not candidate gates. Do not run,
  synthesize, or mark an `I3` non-closing row as required qualification, and
  never pool these samples with closing publication.
- Separately run 64- and 1,000-operation tiny-edit
  publish-then-`freeze_for_branch`/fork/activate campaigns. These traverse
  every depth-compaction/debt trigger, report publication and activation
  independently plus outer p50/p95/max and aggregate compaction, require
  `<=1.070 s` publication, `<=99.9 ms` locally stored activation, and
  `<=1.170 s` outer maximum without rejection/deferred readiness, stay at
  `D_proj <=8`, and reach zero maintenance debt within `D_settle`. The
  preferred constituent p95 gates are `<=214 ms` and `<=20 ms`; the reported
  `<=234 ms p95` outer target is never a combined speedup claim.
- Checkpoint several history depths, perform public logical
  `squash_layerstacks`, and prove that inactive nodes do not acquire permanent native
  materializations.
- Here, candidate `D_proj` means incremental LayerStack delta/carrier lowers
  above one mandatory base:
  `total_overlay_lowers = 1 + D_proj`. Run candidate `D_proj` `0`, `1`,
  `4`, and `8` (respectively 1, 2, 5, and 9 total lowers). On a pinned host whose
  capability receipt supports the new mount API, separately run legacy/control
  depth `32`, `64`, `128`, `499`, and `500`, then verify capability rejection
  at 501 total workspace lowers. Upstream OverlayFS permits 500 total
  lower-directory entries, normally 499 incremental LayerStack carriers when
  one mandatory base consumes a slot; the candidate's depth-8 rejection is a
  performance design bound, not the kernel maximum. On other hosts, run the
  correct legacy mount API through candidate `D_proj=8` and record its
  serialized `lowerdir=` byte/path ceiling. Record Docker Engine `overlay2`'s
  image-layer limit as a different constraint. Keep public logical ancestry
  prune separate from physical flatten.
- Roll back to an old winner and reactivate it on both a warm and a cold
  worker.

These experiments measure construction, selection, activation, and space.
They include the locator evacuation and cleanup required to declare a result
settled; unrelated long-term retention policy remains separately owned.

### Real CLI/runtime lifecycle phase

After publication and materialization cells are sound, run an additional
campaign over the real product command surface. Discover it for every build:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo run --quiet -p sandbox-cli \
  --features manager,runtime,observability \
  --bin sandbox-catalog-export
```

The currently discovered manager surface is:

- `create_sandbox`, `list_docker_images`, `list_workspace_directories`,
  `destroy_sandbox`, `list_sandboxes`, `inspect_sandbox`,
  `squash_layerstacks`, and `export_changes`.

The currently discovered runtime surface is:

- `exec_command`, `write_command_stdin`, `read_command_lines`, `file_read`,
  `file_write`, `file_edit`, `file_blame`, `create_workspace_session`,
  `publish_workspace_session`, and `destroy_workspace_session`.

The currently discovered observability surface is:

- `snapshot`, `trace`, `events`, `resources`, `daemon`, `topology`, `cgroup`,
  and `layerstack`.

Cover every listed operation, all export formats, explicit and implicit
execution, stdin/line lifecycle, read/write/edit/blame, success, error,
cancel, and teardown. Observability commands are non-scored integrity/overhead
cells rather than performance wins; exercise both system and sandbox routes
for `snapshot` and `resources`.

`fork`, committed `checkpoint`, historical-root
`materialize`/`reactivate`, and committed `rollback` are not public commands
today. Benchmark their real component APIs and mark the public cells
**blocked** until catalog export exposes them. Do not invent command names,
and do not substitute `create_sandbox --count` for fork.

The current `squash_layerstacks` behavior is the physical-flatten legacy
control. Stage 04.6 changes its public contract to metadata-only logical
ancestry pruning while preserving the exact root pair; physical flatten
becomes a separately timed internal maintenance cell. Stage 04.6 completion
also requires ProductAccess rollback exposure and a generated catalog entry.

The outer CLI clock wraps the caller before CLI or `ProductAccess` invocation
and includes process spawn, serialization, connection/auth, IPC, response, and
the operation-specific readiness probe. Inner service spans diagnose but do
not replace it. In particular, `TimedGatewayResponse.latency_ns` starts after
TCP connection and is never the product score. Coverage validation fails if a
newly catalogued public operation-and-route tuple is unclassified.

Operation-specific boundaries are:

| Operation | Readiness boundary and required split |
| --- | --- |
| `create_sandbox` | before CLI spawn through every returned record `Ready` plus direct daemon/workspace probe; split shared-base built/reused and image present/pull, and report first/last ready for count |
| list/inspect operations | complete schema-validated response with expected membership/cardinality |
| `destroy_sandbox` | record, daemon/container, mounts, and owned storage absent; report response and settle separately |
| `squash_layerstacks` after the contract switch | identical root pair, new ancestry selection durably visible, and public response complete; require `<=20 ms p95` outer and `<=1 ms p95` service |
| internal physical flatten / legacy squash control | new projection durable, required sessions switched/probed, and old generation reclaimable; report all copy/allocation and settle work separately |
| catalogued committed rollback after ProductAccess exposure | target root selected, usable, and probed; hot cached-projection path requires `<=20 ms p95` outer and `<=1 ms p95` service, while cold projection/acquisition is a separate physical-floor cell |
| legacy/control-only non-closing logical checkpoint/add-layer on `I0`/`I2` | root/ref durable, recorder epoch advanced in the same upper, and next-command probe accepted; no session close, upper rotation, lower addition, or remount; report as compatibility evidence only |
| matched closing publication control on pinned `I0`/`I2` | same request shape as `I3`; admission fenced/drained, old session terminal and closed, implementation-specific root/ref durable; successor activation, if requested, uses a fresh upper and separate clock. This is the only `I0`/`I2` publication mode eligible as a candidate speedup denominator; absent support makes the ratio `UNKNOWN` |
| candidate closing `seal_publish`, and public route only after catalog exposure | publication constituent stops at the durable `PublicationCommitted` timestamp/acknowledgement with old session closed and upper transferred to immutable PayloadStore ownership or deleted when unretained; successor activation has a distinct `ActivationOperationId` and post-commit row; the combined clock stops at its final response without reclassifying publication |
| `export_changes` | complete verified destination; separate directory, tar, and `tar-zst` rows |
| `create_workspace_session` | response plus probe in that exact explicit session; split shared/isolated network profiles |
| explicit `exec_command` | terminal command result/output; initial still-running response does not stop the timer |
| implicit `exec_command` | terminal command, automatic publication durable, automatic session destruction, and session-upper ownership transfer/deletion; label as a combined closing lifecycle. Time successor-workspace readiness separately only if the exported contract promises it; do not assume a new private upper |
| stdin/read-lines | accepted write/yield and validated stable-offset read; include complete running-command interaction |
| `file_read` | verified returned bytes; separate snapshot and explicit-session variants |
| `file_write` / `file_edit` with session ID | mutation visible in that live session |
| `file_write` / `file_edit` without session ID | automatically published layer durable and read back; a distinct score row |
| `file_blame` | complete correct published-file tiling |
| `publish_workspace_session` | root durable, session closed, and session upper transferred to immutable payload ownership when adopted or deleted when unretained; report response and settle separately. Add successor-workspace readiness only if catalog/schema semantics require it |
| `destroy_workspace_session` | session absent and unretained upper deleted; adopted payload remains under inventoried `PayloadStore` ownership; active-command rejection is an error-path cell |
| every observability operation and route | complete schema-validated, bounded response; record cardinality and response bytes, and verify no lifecycle, checkpoint, projection, or payload-store mutation |

### Required result record

Each row must include implementation/source/build/host/filesystem identity,
capability probes, backend/projection key, corpus/mutation, root,
attribution root, parent, depth, placement/cache classification, concurrency,
active/inactive count, sample count, every named span, mandatory p50/p95/p99
for qualified rows, throughput, receipt status/hit rate, semantic verdict, and
recovery verdict. It also includes exact `PublicationId` and
`PublicationOperationId`/ref-operation identity, optional
`ActivationOperationId`, separate durable outcomes, composed response,
attempt/success/failure counts and success rate for every publication/ref,
activation, and combined denominator, retry count, and ref-update count. The
campaign artifact also includes the baseline/candidate
package/version/feature/direct-edge and helper/command/download inventories.
Space reporting must include:

```text
T(t) = L_hot(t) + H_cold(t) + sum(U_active(t)) + P_staging(t) + M(t)
D_ideal = C_current + H_unique
```

Also report settled amplification, avoidable duplicate payload, pack/CAS
unique bytes, native delta, staging, metadata, quarantined,
lease-protected, and unexplained bytes. Record current/peak RSS, index/mmap
residency, FDs, mounts, workers, queues, permits, inodes, leases, dirty bytes,
sync activity, and cleanup inventory.

The settled gates remain `<=1.08 D_ideal` for mixed/no-dedup,
`<=1.15 D_ideal` for many-small, `<=1%` avoidable duplicate payload, and zero
persistent unexplained bytes; settled pack dead/slack allocation is `<=2%`.
Incremental publication permits at most
five-percent additional **payload** staging relative to captured allocation
and zero payload staging for metadata-only edits; hydrate-and-adopt permits one
native target plus at most five-percent additional payload staging. Each
transaction may separately own at most a `256 KiB` journal and its share of
the declared `4 MiB` managed budget, charged to `M`.

“Settled” means `MaintenanceSettled`: locator evacuation and retirement are
complete, `P_staging` is zero, the duplicate-payload gate passes, and no lease
blocks retirement. An accounted `Retiring` generation is explicitly not a
settled result. Maintenance settlement is deterministic. Before candidate
runs, controls freeze
`R_bytes` and `R_entries` as conservative lower 95% confidence bounds for
durable evacuation bytes/s and reverse-manifest entries/s:

```text
D_calc = 2 s + 1.25 * max(B_remaining / R_bytes, E_remaining / R_entries)
D_settle = min(D_calc, 60 s)
```

If `D_calc > 60 s`, admission must split/pre-evacuate or reject the operation.
On a quiescent qualification cell, eligibility begins at publication. In
general it begins at the durably observed release of the last blocking lease;
the persisted eligibility time and derived absolute deadline survive restart,
and an ambiguous clock after eligibility counts as expired. Missing the
deadline, retaining retirement debt, or failing to return `P_staging` to zero
after success, failure, or cancellation fails the cell.

Performance results are invalid if a correctness, boundedness, portability, or
space gate fails. If the legacy `I0`/`I2` non-closing controls are run,
omitting, pooling, or mislabeling their evidence invalidates those
compatibility-control rows only; it does not pass or fail `I3` and cannot block
candidate release qualification.

The candidate is specifically falsified by:

- candidate closing small post-setup publication or the combined
  immediate-receipt-miss
  mutation-to-durable-root cell above `1.070 s p95`;
- any 100x/500x label that misses the lesser of its historical ceiling and
  `matched_current_p95 / 100` or `/ 500`;
- stored-local-projection readiness above `99.9 ms p95`; missing the preferred
  `20 ms p95` target is a 500x-target miss and forbids a 500x
  workspace-ready claim, but does not by itself fail the minimum 100x gate;
- first ingestion above `1.25x` its matched one-pass physical floor, an
  avoidable second complete source-payload pass, or `I3` rejection,
  truncation, or weakening of the required 1 GiB canonical challenge;
- public logical squash or hot cached-projection rollback above `20 ms p95`
  outer or `1 ms p95` service, or either scaling with root size/history depth;
- either of the separate candidate closing branch-projection sequences
  exceeding a `1.070 s` publication constituent, a `99.9 ms` locally stored
  activation constituent, a `1.170 s` outer maximum, or `D_proj>8`,
  rejecting/deferring readiness, hiding compaction or maintenance-induced
  later delay, or retaining debt past `D_settle`;
- a missing deferred read/scan/random-read/first-write cost, warm-lookup
  regression, space-gate failure, persistent unexplained bytes, or failure to
  return `P_staging` and cancellation inventory;
- an exceeded resource cap or correctness path that secretly depends on an
  undeclared device, filesystem, kernel minor, privileged helper, page cache,
  or RAM-resident repository; or
- any unexplained external package/version/feature/direct-edge,
  helper/target-image-command, or build/runtime-download delta.

For every closing publication campaign, `CommittedActivationFailed` remains a
successful publication sample and a failed activation/combined sample. The
harness must preserve both operation identities, prove same-`PublicationId`
retry does not update the ref again, and retain the crash-injection cases around
activation intent, start, terminal persistence, and response delivery. It must
report attempt/success/failure counts and success rate; success-only latency
percentiles are diagnostics, and any failure fails a success-required
activation or combined cell.
