# Stage 04.6 native-delta materialization optimization plan

Status: **PROPOSED — TARGETS NOT YET MEASURED**

This plan optimizes the existing CAS/SeqCDC and native-materialization design.
It does not replace CAS, require reflink or FUSE, weaken immutable root
identity, or move Stage 5–7 packing, locator, retention, deletion, or garbage
collection work into Stage 04.6.

The central change is to stop rebuilding a complete native repository when a
new root differs from a verified parent by a small set of paths. The Linux
adapter should construct or promote a small immutable native delta and mount
it over existing immutable carriers. CAS remains the durable, deduplicated,
backend-neutral truth.

## Inputs and current evidence

The expanded workload and measurement protocol are defined in the
[baseline experiment README](baseline-experiment/README.md).

| Observed path | Current evidence | Interpretation |
| --- | ---: | --- |
| Publication / CDC / CAS ingestion | `107.024 s`, `8.13 MiB/s` for `870.08 MiB` | Full publication pipeline; not materialization |
| Cold complete native materialization | `9.988 s`, `87.12 MiB/s` | Current Stage 04.6 optimization reference |
| Explicit same-key materializer call | `6.362 s` | Returns `Reused`, but still performs byte-proportional work |
| Ordinary warm generation lookup | `0.035375 ms` median | Catalog lookup is already fast |
| Prior complete native-copy control | approximately `303–357 MB/s` | Diagnostic upper reference, not a correctness-equivalent product path |
| Raw SeqCDC scan | no local `5 GB/s` result | Must not be conflated with the full CAS pipeline |
| Logical squash control path | approximately `6 ms` in prior Stage 04.5 evidence | Already within the accepted `10 ms` tolerance |

The historical result is a one-sample baseline. Every target below is a
proposed Stage 04.6 gate or stretch target and becomes an acceptance threshold
only after the expanded matched baseline is recorded.

## Goals

1. Make a small repository change cost proportional to the changed native
   files and changed Merkle nodes, not total repository size.
2. Reuse already-written sandbox upper bytes when a sealed upper is eligible
   to become an immutable native delta.
3. Make exact reuse and ordinary activation metadata-bound.
4. Improve the complete cold path without making it the normal path for every
   new root.
5. Preserve or improve the established physical-space budget.
6. Keep inactive multi-agent rollout nodes as roots and references, with no
   per-node native repository copy.
7. Keep root identity and storage backend-neutral so Linux OverlayFS,
   Firecracker, and WASI can use different materializations of the same root.

## Non-goals

- No RootId or AttributionRootId semantic change.
- No required reflink, block CoW, FUSE, network filesystem, or new external
  dependency.
- No cross-authority transaction that merges CAS publication and native
  carrier publication into a second source of truth.
- No Stage 5–7 pack, locator, eviction, pruning, retention, deletion, or
  garbage-collection authority.
- No unbounded file-segment list, task fan-out, memory buffer, lower chain, or
  retry loop.
- No claim that a one-byte edit inside a large file is byte-range native CoW.
  OverlayFS replaces complete changed files.

## Cost model

Let:

- `U_pub` be unpublished upper payload bytes read by publication;
- `R` be the allocated bytes in a complete native target;
- `E` be the number of target entries;
- `K` be the number of chunks referenced or installed by publication;
- `F_changed` be a complete lower-only file copied up or republished after an
  in-file edit;
- `C` be the chunks read or verified;
- `P` be an explicit verified parent root and carrier generation;
- `Q` be the changed Merkle nodes and paths between `P` and the new root;
- `H` be the allocated bytes of complete changed files that must be hydrated;
- `X` be changed metadata, whiteout, opaque-directory, and type-replacement
  operations;
- `U` be a quiesced, validated private upper eligible for promotion; and
- `D` be the native carrier-chain depth.

The current complete-carrier path is approximately:

```text
T_full =
    T_admit
  + T_walk(E)
  + T_load(C)
  + T_write(R)
  + T_sync
  + T_verify_cas(C)
  + T_verify_native(R)
  + T_publish_generation
```

It is `O(R + E + C)` even when the logical change is tiny. A second full-tree
verification can reread CAS and native bytes after they were just written.

The durable CAS publication cost remains:

```text
T_cas_publish = O(U_pub + E + K)
```

If a one-byte modification forces a complete lower-only file into the captured
upper or publication stream, that operation still includes `O(F_changed)`
reading and CDC. Native-delta construction removes the unrelated
repository-wide rewrite; it does not make this scan disappear.

For a CAS-only root with an explicit verified parent, the proposed path is:

```text
T_delta =
    T_admit
  + T_merkle_diff(Q)
  + T_hydrate_complete_changed_files(H)
  + T_apply_metadata(X)
  + T_sync(delta)
  + T_verify_delta(Q + H + X)
  + T_publish_generation
```

For a sandbox-generated root whose upper is safe to adopt:

```text
T_promote =
    T_quiesce
  + T_validate_upper(U entries)
  + T_sync(U)
  + T_publish_generation
```

Activation becomes selection and mounting of an already verified carrier
vector:

```text
T_activate = T_lookup + T_lease(D) + T_mount(D)
```

The end-to-end path must always report the two large stages independently:

```text
T_new_root =
    T_cas_publish
  + (T_promote if eligible, otherwise T_delta)
  + T_activate

T_logical_squash = T_root_metadata + T_generation_selection

T_physical_flatten =
    T_full_for_selected_root
  + T_publish_generation
```

The main gain is `H << R` for ordinary source edits. Promotion is better:
native payload was already written by the workload and is renamed or adopted,
not copied through CAS and written again. CAS publication remains separately
durable and may still scan every byte in a modified lower-only file. A one-byte
edit inside a `100 MiB` file therefore does not receive the same improvement
as a `4 KiB` source-file edit until a future native byte-range or block-image
adapter exists.

## Expected performance improvement

These are end-to-end product-path targets, not isolated paper numbers. Warm
paths may regress by at most 5% within the noise allowance already accepted for
Stage 04.5. Latency below `10 ms` is not a reason to add architectural risk.

| Scenario | Current reference | Stage 04.6 target | Stretch target | Expected improvement |
| --- | ---: | ---: | ---: | ---: |
| First publication / CDC / CAS, `870.08 MiB` | `107.024 s` | `≤30 s` diagnostic | `≤10 s` | `≥3.6×`; `≥10.7×` stretch |
| Cold complete native materialization, `870.08 MiB` | `9.988 s` | `≤5.0 s` | `2–3 s` | `≥2.0×`; `3.3–5.0×` stretch |
| Explicit exact-key materializer reuse | `6.362 s` | `≤100 ms` p95 | `≤25 ms` p95 | `≥64×`; `≥254×` stretch |
| Ordinary warm generation lookup | `0.035375 ms` median | `≤0.1 ms` median | preserve baseline | No meaningful regression |
| Existing warm workspace activation | `18.54 ms` p95 reference | `≤21.5 ms` p95 | `≤18.54 ms` | Within accepted 5% plus `2 ms` noise |
| Logical squash / control-plane selection | approximately `6 ms` | `≤10 ms` p95 | preserve baseline | No risky optimization required |
| Deliberate physical flatten, `870.08 MiB` | cold complete path is the `9.988 s` proxy | `≤5.0 s` | `2–3 s` | Same expected gain as complete cold construction |
| CAS-only `≤64 KiB` edit in a `1 GiB` root | approximately `11.75 s` if rebuilt completely | `≤100 ms` p95 | `10–50 ms` p95 | `≥117×`; `235–1,175×` stretch |
| Eligible frozen-upper promotion after tiny edit | no promotion path | `≤25 ms` carrier publication p95 | `1–10 ms` typical | Avoids the full native rewrite |
| `1 MiB` changed across at most 100 files | complete-root rebuild | `≤200 ms` p95 | `20–100 ms` p95 | Expected `50–500×`, corpus-dependent |
| One-byte edit in a `100 MiB` file, CAS-only root | complete changed file plus current full-root path | `≤1.0 s` p95 | `0.2–0.5 s` p95 | Limited by complete-file reconstruction |
| Offline `pip` install delta, `≈250 MiB` / `≥12k` entries | to be measured | `≤3 s` p95 | `1–2 s` p95 | Establish after matched baseline |
| Offline `npm` install delta, `≈350 MiB` / `≥25k` entries | to be measured | `≤5 s` p95 | `2–3 s` p95 | Establish after matched baseline |
| Four concurrent sibling tiny-delta builds | to be measured | `≤250 ms` per-root p95 | `≤150 ms` per-root p95 | Bounded parallel scaling |
| 64 or 1,000 inactive forks | no qualified result | `O(1)` fork; zero native payload per fork | same | Repository bytes independent of node count |
| Raw SeqCDC scan microbenchmark | not measured locally | `≥5 GB/s` stretch diagnostic | none | Not a full publication gate |

The first-publication target is intentionally diagnostic. Stage 04.6 is not
complete merely because an isolated CDC scan reaches `5 GB/s`, and it is not
blocked if full publication misses that stretch number while native-delta
materialization, correctness, boundedness, and space gates pass. No special
work is justified solely to reduce an already-safe `1–10 ms` operation.

## Space model and gates

The optimization must reduce byte movement without retaining a complete native
carrier for every root. Measure allocated physical bytes:

```text
T(t) =
    L_hot(t)
  + H_cold(t)
  + sum(U_active(t))
  + P_staging(t)
  + M(t)

D_ideal = C_current + H_unique
settled_amplification = T_settled / D_ideal
```

Under the delta design:

```text
L_hot =
    shared immutable base carriers
  + retained immutable native deltas needed by current carrier vectors

S_peak_cas_delta <=
    S_before
  + delta_build_allocated
  + bounded metadata and at most 5% payload staging

S_peak_upper_promotion <=
    S_before
  + bounded metadata and at most 5% staging

S_peak_physical_flatten <=
    S_before
  + one replacement carrier
  + bounded metadata and at most 5% payload staging
```

Adopting a frozen upper must not create a second native payload copy.
Its payload moves from `sum(U_active)` to `L_hot` in the accounting; it is not
added to both.
CAS-only delta construction allocates complete changed files because normal
OverlayFS is path-level CoW, but it must not allocate an unchanged complete
repository. Inactive roots add CAS references and bounded metadata only.

Existing space gates remain release gates:

| Space scenario | Target | Hard failure |
| --- | ---: | ---: |
| Mixed or no-dedup settled amplification | `≤1.08 × D_ideal` | `>1.15 × D_ideal` |
| Many-small settled amplification | `≤1.15 × D_ideal` | `>1.25 × D_ideal` |
| Avoidable duplicate payload | `≤1%` of `C_current + H_unique` | `>3%` |
| Unexplained unreachable or unleased payload | `0 bytes` | Any persistent bytes |
| Cold complete hydration staging | one target plus `≤5%` | More than the gate |
| Frozen-upper promotion staging | adopted upper plus `≤5%` metadata/staging | A second native payload copy |
| CAS-only native delta | changed complete-file allocation plus required filesystem and metadata blocks, all charged to the global amplification gate | Complete unchanged carrier retained for the root |
| `1 GiB` base plus 32 independent `1 MiB` native deltas | one shared base plus `≤32 MiB` changed payload and bounded metadata | Approximately 32 complete `1 GiB` carriers |
| 1,000 inactive forks | zero additional native payload | Any per-fork native repository copy |
| 16 active sibling attempts | one shared lower vector plus the sum of private upper allocations | Any complete shared lower copied per sibling |
| Native carrier depth | operational target `≤16`, preemptively below 64 | Exceeds 64 |

The expected payload-space effect is:

| Example topology | Complete-copy shape to avoid | Expected Stage 04.6 shape | Expected payload reduction |
| --- | ---: | ---: | ---: |
| `1 GiB` base plus 32 independent roots with `1 MiB` changed files | up to `33 GiB` of native carriers | approximately `1 GiB + 32 MiB` native payload plus metadata | approximately `32×` versus complete per-root copies |
| 16 active siblings over a `1 GiB` base | up to `16 GiB` of duplicated lowers plus uppers | one `1 GiB` shared lower vector plus private uppers | up to `16×` for lower payload |
| 1,000 inactive forks of a `1 GiB` root | up to `1 TiB` if materialized per node | zero additional native payload; references and metadata only | payload cost independent of fork count |
| Eligible `250 MiB` frozen package upper | frozen upper plus another `250 MiB` native reconstruction | adopt the original `250 MiB` upper | avoids one complete native copy |
| CAS-only one-byte edit inside a `100 MiB` file | complete-root reconstruction | one new complete `100 MiB` changed file in the delta | no byte-range native-space claim |

These are topology calculations, not measured results. Allocated-byte
qualification and the `D_ideal` amplification gates override the illustration
if filesystem metadata, sparse allocation, or retained leases make the real
footprint larger.

All lease-protected, quarantined, grace-period, and staging bytes remain in the
accounting. Stage 04.6 may construct and select a bounded replacement carrier,
but it may not delete old generations. If retained authorities make the
settled-space gate impossible without Stage 5–7 work, the result is reported
as such; it is not hidden by excluding bytes.

## Design

### 1. Versioned backend materialization key

Introduce a new Linux overlay materialization format under:

```text
(RootId, backend_kind, backend_format_version, target_profile)
```

The immutable manifest records an ordered carrier vector, dependency
generations, manifest digests, parent root used for construction, and
whiteout/opaque encoding version. Parent lineage and backend paths are not
inputs to RootId. A v1 complete carrier and a v2 carrier vector can represent
the same logical root.

### 2. Explicit parent and dependency chain

The caller supplies the verified parent root and selected carrier generation;
the builder never searches arbitrary history for a convenient ancestor. A
lease or pin covers the entire carrier dependency vector, including generation
and manifest digest, before activation. Publication keeps the existing
`Building -> Ready -> Published -> Terminal` lifecycle, `STATE` authority,
immutable `MANIFEST`, and `CURRENT` selector.

### 3. Merkle-diff operation stream

Compare the new root with the explicit parent and skip equal subtrees. Emit a
sorted, canonical, bounded stream containing:

- complete changed regular files;
- created directories and directory metadata;
- symlinks and supported special metadata;
- removals as whiteouts;
- opaque directories;
- file/directory/symlink type replacements; and
- supported xattr, ownership, mode, and timestamp changes.

Directory rename may initially normalize to bounded create/delete operations.
No semantic operation may be silently treated as an ordinary file write.

### 4. Frozen-upper promotion

For sandbox-generated roots:

1. quiesce the attempt and prevent further writes;
2. complete normal CAS publication and obtain the immutable root;
3. validate the frozen upper against its published change set;
4. sync it and publish it as a native delta generation using the existing
   materialization operation; and
5. rotate to a new private upper before any continued execution.

CAS remains authoritative. A crash after CAS publication but before native
generation publication falls back to Merkle-diff construction. There is no
new atomic journal spanning two authorities. If quiescence, ownership,
filesystem, or validation conditions fail, do not promote.

### 5. CAS-only delta construction

When there is no eligible frozen upper, stream the Merkle diff from CAS into a
staging delta:

- hydrate only changed complete files;
- apply metadata, whiteouts, opaque markers, and type replacements;
- use fixed worker and byte-permit limits;
- sync, verify, and atomically publish the immutable generation; and
- abandon cleanly on cancellation, `ENOSPC`, or a stale dependency fence.

Large-file handling remains bounded. Before expanding the current segment
limit, introduce a hierarchical or streaming file-segment representation with
fixed memory and queue limits. Never fix the large-file case by deleting the
cap.

### 6. Compositional verification

Trust a dependency only after validating its immutable state, generation,
manifest digest, and backend-format key. Then verify:

```text
verified parent carrier
+ Merkle equality for skipped subtrees
+ verified changed delta entries
= verified requested root
```

This removes the mandatory second full-root read from the normal delta path.
A complete merged-tree audit remains in qualification and recovery testing.
It is not repeated on every safe reuse.

### 7. Bounded carrier depth and squash

Use logical squash—publishing a content root independent of its physical
history—as the normal operation. Target at most 16 native lower carriers for
activation latency and act before the existing hard limit of 64. Before
admitting a chain that would exceed the operational cap, construct and verify
a bounded rebased or complete carrier outside the writer lock, then publish it
through the normal generation lifecycle.

Physical flattening is a deliberate, separately timed fallback. Stage 04.6
does not delete the old dependency chain; later retention authority decides
when it can be reclaimed.

### 8. Complete cold-path improvements

The complete carrier remains necessary for first hydration, incompatible
backend versions, recovery, and deliberate rebase. Improve it without changing
authority:

- combine streaming write-time verification with final metadata checks;
- avoid rereading immutable chunks and native bytes already verified in the
  same fenced operation;
- coalesce adjacent chunk reads;
- parallelize independent files under fixed worker and byte budgets; and
- stream hierarchical segment lists with bounded memory.

These improvements are secondary to avoiding the complete path for small
changes.

## Implementation sequence

1. **Record expanded baselines.** Add the corpus, mutation, package-manager,
   multi-agent, correctness, and physical-space measurements before changing
   the default format.
2. **Add observability.** Attribute time and bytes to diff, CAS read, write,
   metadata, sync, verification, generation publication, activation, and
   staging.
3. **Add the versioned carrier-vector manifest.** Keep the v1 complete-carrier
   read path and make v2 feature-gated.
4. **Implement dependency leases and activation.** Prove sibling isolation,
   recovery, and exact reuse before optimizing writes.
5. **Implement bounded Merkle diff and CAS-only delta construction.**
6. **Implement compositional verification** and retain full-audit tests.
7. **Implement frozen-upper promotion** behind explicit eligibility checks.
8. **Add depth control and deliberate rebase/flatten fallback.**
9. **Optimize the complete cold path** only where profiles show material cost.
10. **Run matched qualification.** Make v2 default only if performance,
    correctness, boundedness, recovery, and space gates all pass.

Each slice is independently feature-gated and must leave v1 readable. Large IO
occurs outside the writer lock. Lock-held work validates fences and publishes
small immutable metadata only.

## Correctness and failure qualification

The test matrix must cover:

- process death before and after every generation lifecycle transition;
- stale parent generation, manifest digest, and dependency fence;
- cancellation and retry at diff, hydration, sync, verification, and publish;
- `ENOSPC` before visibility without deleting an authoritative source;
- upper promotion rejection and CAS-only fallback;
- corrupt or missing dependency carrier;
- concurrent same-key builders selecting one valid generation;
- whiteout, opaque-directory, type-replacement, rename, metadata, symlink,
  hardlink, and sparse-file behavior;
- activation lease acquisition and release for the whole carrier vector;
- depth-cap admission and physical-flatten fallback; and
- restart reconciliation without guessing from directory presence.

Performance is not accepted if any case weakens content equality, attribution,
immutability, crash recovery, sibling isolation, or bounded resource use.

## Phase 2: parallel MCTS rollout compatibility

Phase 2 keeps a durable graph of immutable `SandboxNode` roots and creates
temporary `ExecutionAttempt`s only for bounded active rollouts. This plan
supports that model directly:

- fork is an `O(1)` root/reference operation, not a payload or native clone;
- inactive nodes own no upper and no permanent native carrier;
- active siblings lease the same immutable carrier vector and receive isolated
  private uppers;
- a fixed-size, prewarmed execution pool may retain backend-keyed carriers for
  locality without making them part of node identity;
- winner reactivation selects a verified carrier or reconstructs a delta from
  CAS;
- OCC promotion, idempotent evaluation, and backpropagation continue to use
  immutable root identity; and
- materialization workers, byte permits, and active attempts remain bounded
  independently of the number of MCTS nodes.

The plan deliberately does not make carrier residency authoritative. A pool
miss affects latency, not correctness.

## Phase 3: WASM/WASI and Firecracker compatibility

Root identity, CAS objects, references, OCC, leases, publication, and recovery
remain shared. Only the adapter-specific materialization changes:

- **Linux/OCI:** an ordered directory-carrier vector with Linux
  whiteout/opaque encoding;
- **Firecracker:** a microVM-local workspace or block-image carrier. A VM or
  block snapshot is a cache of a root, never the authoritative root; and
- **WASM/WASI:** a capability-scoped filesystem projection for the WASM
  runtime that explicitly represents or rejects metadata the backend cannot
  preserve.

Every backend uses the versioned materialization key. Backend paths, inode
numbers, Linux carrier markers, VM snapshot IDs, and WASI handles never enter
RootId. The same logical root may therefore have independent Linux,
Firecracker, and WASI materializations without changing CAS or the durable
graph.

Ordinary reads use a prepared native/backend projection and must not
reconstruct CAS objects per syscall. Optional reflink or block CoW can later
accelerate a backend adapter, but the Stage 04.6 correctness path does not
depend on either.

## Completion rule

Stage 04.6 is ready only when:

1. the expanded baseline is recorded with immutable evidence;
2. delta construction and eligible upper promotion pass correctness and crash
   qualification;
3. tiny-edit materialization demonstrates at least the target improvement over
   matched complete rebuilding;
4. warm paths stay within the accepted 5% and `10 ms` tolerance;
5. all settled and peak space gates pass, including inactive-fork zero-copy;
6. lower depth and all memory, worker, queue, and file limits remain bounded;
7. v1 recovery and rollback remain tested; and
8. the Linux design preserves the backend-neutral contracts required by Phase
   2 and Phase 3.

Missing a stretch target is not by itself a failure. An obvious throughput
defect, correctness regression, unbounded path, unexplained retained byte, or
architecture-breaking shortcut is.
