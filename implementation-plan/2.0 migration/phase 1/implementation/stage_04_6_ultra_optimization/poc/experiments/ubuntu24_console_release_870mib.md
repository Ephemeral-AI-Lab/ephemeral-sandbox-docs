# Ubuntu 24.04 / console-release 870 MiB experiment

**Experiment ID:** `HV-08R`  
**Status:** bound PoC experiment; projected limits remain unmeasured  
**Matrix authority:** `../test_matrix.md`  
**Architecture authority:** `../../new_plan.md` and
`../../requirements_and_prohibitions.md`

---

## 1. Question

On the fixed Docker Desktop envelope, can MPLA publish a real 870.08 MiB
workspace by adopting one stationary upper allocation, activate the resulting
root, publish a later approximately 1 MiB delta from a fresh upper, reconstruct
the final tree exactly, and reconcile all bytes without:

- moving or copying the published upper;
- accepting an old workspace writer or deletion token;
- putting a physical locator into canonical identity;
- creating a hidden second corpus-sized publication allocation;
- exceeding the bounded memory policy; or
- relying on a helper inside the workload image?

For eligible post-setup operations, the experiment must additionally determine
whether MPLA demonstrates at least `100×` matched improvement and whether it
reaches the preferred `500×` result. A larger ratio is reported uncapped. Initial
full-corpus publication, cold construction and independent reconstruction are
physical-floor rows and never contribute a false multiplier.

This is a real-corpus throughput and lifecycle experiment. It does not replace
the synthetic large-file, high-cardinality or complete-semantic-oracle cases.

---

## 2. Immutable inputs

### 2.1 OCI image

| Field | Bound value |
|---|---|
| Convenience tag | `ubuntu:24.04` |
| Required local image identity | `sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` |
| OS / architecture | Linux / arm64 |
| Image version label | `24.04` |
| Observed Docker graph driver | `overlayfs` |

The runner resolves and records the image ID again before every campaign. A
different identity is a different environment receipt, not an automatic
equivalent run. The external projection/readiness probe performs the test; the
experiment does not invoke `/bin/sh`, `stat`, `find`, `diff`, or another helper
inside the image.

### 2.2 Corpus

Use exactly:

```text
/Users/yifanxu/Ephemeral-AI-Lab/experiment/materialization-benchmark-20260727/corpus/console-release
```

Preserved inventory:

| Property | Expected value |
|---|---:|
| Logical bytes | `912,350,100` |
| MiB / GiB | `870.0848579406738 MiB` / approximately `0.850 GiB` |
| Regular files | `3,602` |
| Directories | `694` |
| Symlinks | `0` |
| Files at least 1 MiB | `214` |

The runner verifies these values and emits a deterministic relative-path,
type, size, mode and content-digest manifest before use. A mismatch is
`FIXTURE_MISMATCH`, never a silently substituted corpus.

Do not use the parent `materialization-benchmark-20260727` directory as the
fixture. It is about 1.7 GiB because `results/materialized-carrier` is a second
preserved tree.

### 2.3 Historical comparison only

The preserved earlier experiment reported:

| Operation | Historical result |
|---|---:|
| Candidate publication / CDC / CAS ingestion | `107.024411507 s` |
| Cold complete native materialization | `9.987675338 s` |
| Explicit same-key materializer reuse | `6.361909169 s` |
| Ordinary warm generation lookup, median of five | `0.035375 ms` |

These are historical comparison points, not MPLA results or qualifying
percentile evidence. Their boundaries must not be pooled with the new
experiment unless they match.

For exact stored activation only, the preserved `9.987675338 s` cold
materialization gives an exact `100×`-equivalent ceiling of
`99.87675338 ms` and a `500×`-equivalent ceiling of `19.975350676 ms`.
Claiming either multiplier still requires the matched-current divisor in
Section 5. The historical `107.024411507 s` first-ingestion result is never a
denominator for the later 1 MiB publication.

---

## 3. Environment and time envelope

- Docker Desktop remains at 4 vCPU and 4 GiB.
- The storage application pool remains at or below 8 MiB.
- The full storage domain uses the matrix's 96 MiB soft and 128 MiB hard
  policy; no limit is raised to make the experiment pass.
- At most four data workers run.
- Current-control sources and outputs, the MPLA source/adopted allocation,
  projection/reconstruction outputs, delta, staging and metadata must remain
  below a measured `10 GiB` physical union throughout `HV-08R`; crossing it is
  `FIXTURE_ENVELOPE_FAILURE`.
- `HV-08R`, including its co-scheduled matched activation controls, has a
  projected 60-second target inside the heavy campaign.
- A visible performance miss may continue for diagnostics, but the
  `HV-08R` campaign is terminated at 120 seconds.
- Time beyond 60 seconds consumes the heavy suite's diagnostic margin; the
  complete heavy suite still stops before 600 seconds.

The target is a falsifiable hypothesis. The earlier 107-second publisher makes
a miss plausible; the result remains valuable if every physical span is
reported honestly. Exceeding the control budget makes the corresponding ratio
`UNKNOWN` and the booster verdict `POC_100X_NOT_SUPPORTED`; it never authorizes
dropping the control boundary or extending the 600-second suite hard stop.

---

## 4. Preparation outside the measured interval

1. Verify the exact corpus manifest and image identity.
2. Create one PoC-owned Linux Docker volume or allocation arena.
3. Copy only the source corpus from macOS into a newly allocated stationary
   upper in that Linux arena.
4. Using three fresh identical current-control source allocations, prepare
   three independently resolvable durable `I2` roots before the campaign.
   Record their setup cost separately. Do not prebuild a native carrier or
   projection and do not warm the activation/materializer lookup; root and CAS
   payload availability are the matched stored-input precondition, not timed
   source ingestion.
5. Record all host-to-VM transfers, logical bytes, allocated bytes, inodes and
   resulting fixture digest separately.
6. Before starting the campaign, account for the complete physical union of
   all prepared control sources plus the maximum simultaneously retained
   control/candidate outputs and prove that it is below `10 GiB`. Control pairs
   execute sequentially; a control output may be released only after its
   evidence and same-key sample are durable and no later assertion needs it.
7. Create the adjacent disposable OverlayFS workdir and the lightweight
   workspace lease record.
8. Flush fixture preparation before declaring the allocations ready.

The host-to-VM fixture copy is not a product operation and is outside the
measured campaign. The measured initial publication still includes admission,
quiescence, unmount, allocation flush/stability proof, scan, hash, Merkle and
locator construction, stationary adoption, ref durability and response.

No canonical root or ready projection may be prebuilt for the initial
publication measurement.

---

## 5. Measured sequence

The runner executes the following as one ordered campaign and emits a record
for every step. One physical sample may satisfy overlapping matrix assertions;
the same operation is not rerun only to populate another row.

| Step | Operation and timing boundary | Required observation |
|---|---|---|
| `R0-C01` | On each of three independently prepared durable roots, run current `I2` from before root/materializer selection and first cold carrier construction through external usable-session readiness | Complete materialization, carrier and readiness work remains inside each timer; stored root/CAS payload preparation is outside and reported exactly like MPLA's prior durable publication; record reset proof, cache class and all three raw samples |
| `R0-C02` | Immediately after each `R0-C01`, invoke the current `I2` same-key path through the identical external usable-session readiness boundary | Record three raw same-key samples; do not substitute catalog lookup for a usable session |
| `R0-01` | Start immediately before closing-publication admission; stop after durable paired ref and terminal response | Old session closes; the complete corpus is scanned/hashed; the original stationary allocation becomes `PayloadOwned`; no path move or payload copy |
| `R0-02` | Attempt stale write and stale deletion using the old lease/token | Both reject; owner epoch, bytes, inodes and canonical ref remain unchanged |
| `R0-03` | Start before projection selection; stop at external usable-session readiness | To qualify `BG-ACTIVATE-EXACT`, this first post-publication activation must select the stationary adopted allocation as an exact projection, construct/hydrate zero payload bytes and meet the applicable absolute ceiling; a build/miss remains reported evidence but makes the booster gate unsupported rather than warming it for `R0-04`; successor receives a fresh empty upper |
| `R0-04` | Repeat exact-key activation five times; use the first three as the candidate same-key block as well | Every run selects the same verified generation, reconstructs/hydrates zero payload bytes and ends after the external probe; report all raw samples, median and max, not p95 |
| `R0-05` | From the ready successor, mutate ten deterministic files for approximately 1 MiB total | Writes land only in the new upper; the adopted corpus allocation remains immutable |
| `R0-06` | Publish the small delta using the same boundary as `R0-01` | Successor upper is adopted at its stationary path; publication work is attributed to the new delta and metadata, not an 870-MiB payload twin; absolute `≤100 ms` is required and `≤20 ms` preferred, while the matched publication multiplier comes from `HV-01` |
| `R0-07` | Reconstruct the final root to an independent PoC-owned destination and compare through the external oracle | Every relative entry, byte and supported metadata field matches; reconstruction time and explicit cache/output bytes are reported separately |
| `R0-08` | Reconcile, close successor session and query final storage state | One owner epoch per allocation; all bytes/inodes classified; no live old lease; `X_unexplained=0` |

The real-corpus activation ratios are:

```text
R0_EXACT_ACTIVATION_POC_MEDIAN_RATIO =
  median(R0-C01 cold-to-usable samples) /
  median(R0-04 exact-hit samples)

R0_SAME_KEY_POC_MEDIAN_RATIO =
  median(R0-C02 same-key-to-usable samples) /
  median(first three R0-04 exact-hit samples)
```

The `BG-ACTIVATE-EXACT` `100×` gate additionally requires `R0-03` and every
`R0-04` sample to be at most `99.87675338 ms`; preferred `500×` requires each
of them to be at most `19.975350676 ms`. `R0-03` must be an exact zero-build
selection as specified above—construction there cannot be amortized away. The
`BG-ACTIVATE-SAME` gate requires every candidate sample to be at most `50 ms`,
preferably `20 ms`, in addition to the matched ratio. The report also emits the
uncapped historical-equivalent ratio, clearly separated from these matched
results.

For `R0-05`, select the first ten regular files of at least 1 MiB after
bytewise relative-path sorting. Overwrite a deterministic 100 KiB range in
each file with bytes derived from `(experiment id, relative path, offset)`.
This produces approximately 1,000 KiB of changed ranges without changing file
length. Record the exact selected paths and offsets.

---

## 6. Stationary-adoption proof

Immediately before `R0-01` and after its durable owner transition, capture:

- `AllocationId` and allocation generation;
- private backend-relative allocation locator;
- filesystem/device identity and upper-root inode where supported;
- owner state, workspace lease epoch and owner epoch;
- logical bytes, allocated bytes and inodes;
- mount table and writable holders;
- all PoC allocation-catalog entries;
- per-destination write telemetry and reconciliation categories.

The adoption assertion passes only if:

1. `AllocationId`, allocation generation and physical upper location are
   unchanged;
2. the owner advances exactly once from the expected `WorkspaceOwned` epoch to
   `PayloadOwned`;
3. the old lease and deletion token can no longer mutate or remove it;
4. no corpus-sized destination allocation, pack or staging object is written
   during publication;
5. publication peak is the existing upper plus canonical metadata and bounded
   scratch;
6. every physical byte and inode belongs to exactly one accounting category;
   and
7. the final ref becomes visible only after payload locator coverage is
   durable.

An unchanged pathname alone is insufficient evidence: the write telemetry,
allocation catalog, before/peak/after storage snapshots and final
reconciliation must also exclude a hidden twin.

Projection construction after publication may legitimately create a separate
explicit cache or reconstruction target. Its time and old-plus-new space
belong to `R0-03`, not to publication, and it cannot be relabeled as zero-copy
adoption.

---

## 7. Canonical-identity and correctness oracle

The root builder consumes normalized relative filesystem semantics. It must
not hash:

- `AllocationId`;
- absolute or backend-relative physical paths;
- inode or device numbers;
- owner/lease epochs;
- OverlayFS mount options; or
- projection generation identifiers.

For the same normalized record stream, the test substitutes a different
synthetic locator table and requires identical `RootId` and
`AttributionRootId`. It then verifies the real reconstructed tree against the
fixture-plus-delta oracle. The synthetic-locator comparison proves root
construction independence; the reconstruction comparison proves that the real
locators still resolve the required bytes.

Because this corpus contains no symlinks and is not a complete POSIX-semantic
shape, `S5-semantics` remains mandatory.

---

## 8. Memory, storage and timing evidence

Sample at least every 50 ms during long phases and at every durable phase
boundary:

- operation wall clock and phase spans;
- compared implementation/build, matched-pair id, reset proof, cache state,
  timing boundary digest and evidence class;
- application RSS and total storage-domain/cgroup memory;
- `memory.current`, `memory.events` and OOM events;
- attributable dentry/inode/slab memory where available;
- open FDs, mount count, worker count and queued descriptor bytes;
- bytes read, scanned, hashed, written, adopted and reconstructed;
- logical, allocated, unique, shared, staging, metadata, cache, retirement and
  unexplained bytes/inodes;
- owner journal/selector generation and ref generation;
- raw control/candidate samples, medians, maxima, matched
  `POC_MEDIAN_RATIO`, historical-equivalent ratio, exact gate expressions and
  verdicts.

Page cache and kernel metadata are real memory evidence; they are not omitted
because application heap is small. Any OOM, hard-memory breach, unbounded
task/FD growth or silent cardinality reduction fails the experiment.

---

## 9. Evidence artifacts

Store artifacts below one PoC-owned run directory:

```text
runs/<run-id>/HV-08R/
├── environment.json
├── fixture-manifest.json
├── fixture-transfer.json
├── R0-C01-01.json ... R0-C01-03.json
├── R0-C02-01.json ... R0-C02-03.json
├── R0-01.json ... R0-08.json
├── phases.jsonl
├── memory.jsonl
├── storage-before.json
├── storage-peak.json
├── storage-after.json
├── allocation-catalog-before.json
├── allocation-catalog-after.json
├── owner-journal-copy/
├── roots-and-locators.json
├── oracle.json
├── booster-scorecard.json
└── summary.json
```

Every projected value is labeled `PROJECTED` until replaced by a raw
artifact-backed measurement. Fixture transfer is never mixed into the
publication or activation result.

---

## 10. Pass, performance miss and falsification

`HV-08R` passes correctness only when:

- both stationary adoptions satisfy Section 6;
- stale writer and deleter attempts fail;
- the old session never resumes after durable `Sealing`;
- ref visibility is old-or-complete-new;
- activation uses a fresh upper;
- canonical identities exclude physical locators;
- reconstructed output matches the oracle;
- memory/storage limits hold without OOM; and
- reconciliation ends with `X_unexplained=0`.

It reports performance independently:

- `R0_100X_SUPPORTED` only when both exact activation and same-key usable
  session have valid matched controls, their PoC median ratios are at least
  `100`, the exact zero-build `R0-03` precondition holds, every candidate
  sample meets its required absolute ceiling, and correctness passes;
- `R0_500X_SUPPORTED` when both rows additionally reach matched median ratios
  of at least `500`, `R0-03` meets the preferred absolute ceiling, and every
  candidate sample meets the preferred absolute ceiling;
- `R0_500X_PARTIAL` when the `100×` result is supported and exactly one of the
  two activation rows reaches the preferred rule;
- `R0_500X_NOT_SUPPORTED` when the complete preferred rule is not met and
  `R0_500X_PARTIAL` does not apply; and
- `R0_100X_NOT_SUPPORTED` when a control is missing/incompatible, a ratio or
  absolute ceiling misses, or correctness fails.

`R0-01` and `R0-07` remain physical-floor evidence. `R0-06` reports its
absolute latency here, but it receives a multiplier verdict only from the
matched closing-publication block in matrix case `HV-01`; the 107-second
historical first ingestion is never used.

Taking more than 60 seconds with correctness intact is
`PASS_CORRECTNESS_PERFORMANCE_MISS`, not a full pass. Reaching 120 seconds is
`FAIL_DIAGNOSTIC_TIMEOUT`. A path move, hidden payload twin, stale-token
success, partial root, last-locator loss, OOM, unexplained storage or oracle
mismatch falsifies the current design regardless of speed.

---

## 11. Smoke derivative

The smoke derivative is generated offline from the same immutable corpus:

1. sort regular-file relative paths bytewise;
2. add complete files until cumulative logical bytes first reach or exceed
   128 MiB;
3. include their parent directories and normalized metadata;
4. persist and verify the subset manifest; and
5. report its actual bytes and path count.

It may provide a quick real-artifact repeat of activation and small-delta
publication, but it does not replace `S1-code` because this compiled corpus
lacks the required semantic diversity.
