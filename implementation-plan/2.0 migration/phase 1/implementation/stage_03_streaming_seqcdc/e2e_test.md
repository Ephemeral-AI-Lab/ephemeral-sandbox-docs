# Stage 03 E2E — Bounded scalar streaming SeqCDC

[Implementation overview](../index.md) · [Stage 03 specification](spec.md) · [Benchmark note](benchmark_note.md) · [Preparation 03](../../prep/03-seqcdc-cas-and-squash-decision.md) · [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Product root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
Test root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`
Normative POC image: `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`

## 1. Stage-local test objective

Stage 03 proves the scalar algorithm as a bounded, portable Rust primitive and proves that it is still dormant in the packaged runtime.

- Product tests are authoritative for author-oracle cuts, arbitrary `Read` fragmentation, exact byte coverage, bounded borrows, typed chunk IDs, source errors, and code/dependency boundaries.
- One focused live-Docker case publishes deterministic data through the existing public CLI and proves that legacy v1 remains the only route and the runtime SeqCDC/candidate counters remain zero.
- One ignored 30–60 second Rust loop reports diagnostic cut throughput/distribution and resource high-water values.

This is a **POC proof tier**, not the integrated SeqCDC-versus-StreamCDC selection campaign. No broad/full suite, nightly/release run, paper-throughput comparison, or favorable tiny result can satisfy the final ≥10% selection, storage, RSS-scale, or portability gates.

## 2. Existing assets to reuse

| Existing asset | Reuse in Stage 03 | Constraint |
| --- | --- | --- |
| Stage 02 core canonical codec/typed IDs | `ChunkProfileId`, `ObjectKind::ChunkPayload`, typed digest preimage | No backend/hash dependency may enter the core. |
| LayerStack existing `sha2` edge | Hash two borrowed slices synchronously | No new/moved external edge. |
| `e2e/harness/catalog/declarations.py` | Full immutable typed declaration | Exactly one terminal record per declared validation. |
| `e2e/harness/runner/reporter.py` | Durable JSONL result, phases, cleanup, surface proof, bounded artifacts | Missing data is explicit; logs do not substitute for a typed observation. |
| `e2e/harness/runner/resources.py` | Run-owned sampling and LIFO cleanup | Only exact run-owned identities; no global prune/kill. |
| Workspace-session public CLI helpers/cases | Create/write/publish/read and before/after v1 revision assertions | No private daemon route or direct product-storage inspection as SUT. |
| Stage 00 route/resource observations | Prove runtime SeqCDC scans and candidate resources are zero | Counters are bounded scalars with no per-path/chunk labels. |
| `e2e/test-report.md` | Append-only planned/run/good/defect/fix log | Append before each live command and after result. |
| Catalog collector | Discovery/validation without execution | Use explicit repository roots; optional output only under `.e2e-state/tmp`. |
| `benchmark/backend/benchmark_lab/planning.py`, `benchmark/backend/benchmark_lab/runner.py`, `benchmark/backend/benchmark_lab/artifacts.py`, `benchmark/backend/benchmark_lab/resource_sampling.py` | Existing sequential scheduler, paired raw samples, bounded resource evidence, and immutable bundles | Add only a bounded adapter/preset for the prebuilt SeqCDC probe; no separate scheduler or benchmark dependency. |

The harness’s `E2E_REBUILD_BINARY=1` requests a rebuilt packaged daemon on cold start; a responding gateway may be reused. Record whether rebuild or reuse occurred. An exact-node rerun with `=0` is allowed only after a recorded fix.

## 3. Resulting test tree

### Test/evidence tree

```text
ephemeral-sandbox/
└── crates/sandbox-runtime/
    ├── layerstack-core/
    │   └── tests/
    │       ├── seqcdc_author_oracle.rs          [add]
    │       ├── seqcdc_fragmentation.rs          [add]
    │       ├── seqcdc_boundaries.rs             [add]
    │       └── seqcdc_tiny_loop.rs              [add] — prebuilt probe
    └── layerstack/
        └── tests/
            ├── seqcdc_typed_ids.rs              [add]
            └── fixtures/cas/v2/seqcdc/
                ├── ORACLE.md                    [add]
                ├── cases.json                   [add]
                └── payloads.bin                 [add]

ephemeral-sandbox-test/
├── e2e/runtime/layerstack_phase1/
│   ├── helpers.py                              [reuse] — public-only helpers
│   └── test_seqcdc_dormant.py                  [add] — one POC live case
├── e2e/fixtures/layerstack_phase1/seqcdc-v1/
│   └── live-payload-manifest.json              [add] — deterministic seed/digest/size
├── e2e/tools/verify_external_dependency_delta.py [reuse] — stdlib dependency verifier
├── benchmark/backend/benchmark_lab/
│   ├── planning.py                              [modify] — register bounded SeqCDC probe
│   └── runner.py                                [modify] — schedule prebuilt probe
├── benchmark/presets/
│   └── layerstack-phase1-tiny-seqcdc.yml        [add] — paired sub-minute sentinel
├── .e2e-state/
│   ├── runs/<run_id>/                           [reuse] — run-owned durable bundle
│   └── tmp/<run_id>/                            [reuse] — run-owned temporary evidence
└── e2e/test-report.md                           [reuse] — append-only
```

### Complete expected `/eos` tree

The packaged case is deliberately feature-off. No candidate-format path may appear.

```text
/eos/                                                    [A0]
├── layer-stack/                                         [B0]
│   ├── .storage-writer.lock                             [B0a]
│   ├── manifest.json                                    [B1]
│   ├── workspace.json                                   [B0b]
│   ├── base/<base_id>/                                  [B2]
│   ├── layers/<layer_id>/                               [B3]
│   ├── staging/<layer_id>.staging/                      [B4]
│   └── .layer-metadata/
│       ├── <layer_id>.digest                            [B5]
│       └── <layer_id>.bytes                             [B6]
├── storage/
│   ├── file_auditability/                               [C1]
│   └── workspace_recovery/                              [C2]
├── workspace/
│   ├── manager.json                                     [D1]
│   ├── .export/<spool_id>                               [D1a]
│   └── <workspace_session_id>/                          [D2]
│       ├── upper/                                       [D3]
│       └── work/                                        [D4]
├── namespace_execution/                                 [E0]
│   └── <namespace_execution_id>/transcript.log          [E1]
└── runtime/daemon/
    ├── runtime.sock                                     [F1]
    └── runtime.pid                                      [F2]
```

This is the branch-independent Stage 00 scratch schema. If parallel Stage 01
has independently passed and its checkpoint is recorded, replace only `E1`
with this exact optional delta; Stage 03 does not require or produce it:

```text
/eos/workspace/<workspace_session_id>/executions/<command_session_id>/transcript.log [D5; Stage 01 replacement]
/eos/namespace_execution/<legacy_namespace_execution_id>/transcript.log              [E1; compatibility-only and may be absent]
```

| Code/path | State; class | Owner | Lifecycle, fsync, recovery, deletion | `RootId` | Rollout R/W | Bound; `T(t)` | Permission/exposure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `A0` | existing storage namespace | installation/daemon | provision → boot validate → installation removal only | none | daemon R/W | one; all terms | masked |
| `B0` | existing truth namespace | LayerStack | open → existing durability rules → legacy boot sweep | no v2 | legacy R/W | one; `L_hot+P_staging+M` | daemon-only |
| `B0a` | existing coordination lock | LayerStack | open/lock → kernel-held exclusivity → reacquire after restart → close | none | legacy coordination | one FD; `M` | daemon-only |
| `B1` | authoritative v1 truth | legacy publisher | temp/write/fsync → rename/parent fsync → validate → atomic supersede | v1 hash only; not v2 | sole R/W/publication | one; `M` | daemon-only |
| `B0b` | existing base-binding truth | base builder | bootstrap atomic write/fsync → boot validation → installation removal | physical v1 base reference only | legacy R/W | one; `M` | daemon-only |
| `B2` | native base carrier | base builder | verify/install/fsync → v1 reachability → approved remove | physical ref excluded | legacy R | one; `L_hot` | lower read-only/masked |
| `B3` | native layer carrier | legacy publisher | private stage/fsync/rename → v1 manifest commit → legacy squash/reap | physical ref excluded | legacy R/W | current `D`, final≤64; `L_hot` | lower read-only/masked |
| `B4` | legacy transaction staging | legacy publisher | allocate/write/fsync → rename or abort/boot reap | none | legacy W | admitted transaction; `P_staging` | `0700`, masked |
| `B5` | v1 digest metadata | legacy publisher | atomic post-carrier write → recompute → delete with carrier | not typed object ID | legacy R/W | one/carrier; `M` | daemon-only |
| `B6` | byte accounting metadata | legacy publisher | atomic write → recount → delete with carrier | none | legacy R/W | one/carrier; `M` | daemon-only |
| `C1` | audit truth | FileService | operation durability → boot recovery → retention | blame separate | service R/W | configured; `M` | authenticated only |
| `C2` | conditional recovery truth | recovery owner | exact-owner record/fsync → bounded retry → delete after reap | none | recovery R/W | failures only; `P_staging+M` | daemon-only |
| `D1` | workspace owner truth | WorkspaceManager | atomic update/fsync → boot reconcile → supersede | none | workspace R/W | one; `M` | daemon-only |
| `D1a` | transient export scratch | export owner | exact run-owned create/write → completion or failure recovery → exact owner cleanup | none | export R/W | bounded active exports; `P_staging` | absent at quiescence |
| `D2` | active session scratch | WorkspaceManager | create/admit → mount/action → publish/destroy → exact-id reap | none | workspace R/W | active sessions; `ΣU_active` | `0700` |
| `D3` | writable upper scratch | workspace/capture | create/write → whole-file legacy capture → teardown | only future input bytes; host path excluded | workspace R/W | unpublished bytes; `ΣU_active` | `/workspace` projection |
| `D4` | OverlayFS work scratch | overlay/kernel | mount → kernel use → unmount/reap | none | provider R/W | one/session; `ΣU_active` | masked |
| `D5` | optional Stage 01 replacement, absent from the Stage 00 branch-independent schema | command owner after Stage 01 | admit/append cap → close → Drop/session/boot cleanup | none | not touched by Stage 03 | transcript/terminal caps; `ΣU_active+M` | API-only |
| `E0` | Stage 00 command scratch; compatibility-only after Stage 01 | command owner or cleanup adapter, according to recorded layout epoch | active bounded writes/reap under Stage 00, or no new writes and exact legacy reap after Stage 01 | none | unchanged by Stage 03 | configured cap; converges only after Stage 01 | masked |
| `E1` | active Stage 00 transcript or legacy Stage 01 residue | recorded layout epoch owner | bounded append/close/reap; never inferred from directory presence alone | none | unchanged by Stage 03 | configured cap | `0700` |
| `F1` | ephemeral control socket | daemon | stale-owner check/bind → unlink shutdown/recovery | none | control R/W | one; `M` | `0600` |
| `F2` | ephemeral identity file | gateway/daemon | atomic boot write → identity recovery → remove | none | daemon R/W | one; `M` | daemon-only |

Forbidden candidate paths are `/eos/layer-stack/format-v2.json`, `roots/v2`, `manifests/v2`, `objects/v1/loose`, `packs/v1/open`, `packs/v1/sealed`, `indexes/v1/pages`, `indexes/v1/index.catalog`, `catalogs/v1/roots.catalog`, `catalogs/v1/locators.catalog`, `catalogs/v1/materializations.catalog`, `catalogs/v1/leases.catalog`, `catalogs/v1/retention.catalog`, `journals/v1/publication`, `journals/v1/hydration`, `journals/v1/squash`, `journals/v1/compaction`, `journals/v1/migration`, `staging/v2/publication`, `staging/v2/hydration`, `staging/v2/squash`, `staging/v2/compaction`, `staging/v2/migration`, `leases/v1`, `retention/v1`, `maintenance/v1`, `materializations/docker-overlayfs/v1`, `quarantine/v1`, and `trash/v1`.

## 4. Typed E2E case catalog

Run-now rows below use the stage-local pinned Ubuntu 24.04 target image and do
not qualify portability. Stage 11 must run required hosts/release runners and
the full Prep 04 Phase-1 image matrix: pinned Ubuntu/Debian glibc, Alpine
musl, minimal/distroless, shell-less, read-only, and non-root.

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `runtime.layerstack-phase1.seqcdc.runtime-dormant` | POC; `run-now-focused` | dormant scalar SeqCDC with legacy authority | pinned Ubuntu 24 image, legacy config, deterministic boundary payload | public write, publish, read | exact v1 bytes/revision and zero runtime SeqCDC/candidate work | diagnostic elapsed time | complete legacy allocation and zero candidate bytes | case owners/tasks/FDs/sessions quiesce | exact external delta zero and pinned Ubuntu 24 record | `60000` ms | typed JSONL and public/route/resource/storage/cleanup snapshots |
| `SCDC-R08` | POC; `run-now-tiny-bench` | scalar streaming primitive | one long-lived process and authors' oracle corpus | typed wrapper invokes the bounded primitive campaign | exact cuts and IDs for every feed schedule | raw paired diagnostic distribution | no durable artifact | ring, borrow, descriptor owners return every pair | std-only safe code and scalar golden proof | `60000` ms | raw JSON samples and summary |
| `runtime.layerstack-phase1.seqcdc.selection` | release; `planned-final` | selection, required-runner, and image-matrix qualification | frozen Stage 11 corpus, release runners, and full Prep 04 Phase-1 image matrix | packaged matched workload | full selection, locality, storage, lifecycle, image, and required-runner gates | normative matched metrics | complete physical envelope | full scale and repeated-lifecycle matrix | required-runner proof plus pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root | `300000` ms | Stage 11 qualification bundle |

Complete literal declaration metadata:

| Stable ID | Title | Description | Features | Validations | Validation features | Execution surface | Owner ID | Timeout (ms) | Pytest markers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `runtime.layerstack-phase1.seqcdc.runtime-dormant` | `SCDC-01 Scalar SeqCDC Is Deterministic And Runtime-Dormant` | `A packaged Ubuntu 24.04 sandbox publishes and reads a deterministic multi-boundary payload through public CLI operations while legacy v1 remains authoritative and runtime SeqCDC and candidate resource counters remain zero.` | `("runtime.workspace_session","runtime.layerstack-phase1.seqcdc")` | `{"assert-scdc-01-dormant-legacy-route":"Published bytes and the legacy revision are correct; read, write, and publication authorities remain legacy; runtime SeqCDC scans, bytes, chunks, candidate completions, mismatches, fallbacks, workers, queues, permits, transactions, roots, objects, packs, and durable bytes are zero; case-owned resources are reclaimed."}` | `{"assert-scdc-01-dormant-legacy-route":("runtime.workspace_session","runtime.layerstack-phase1.seqcdc")}` | `"cli"` | `"e2e-core"` | `60000` | `("smoke","phase1","config")` |
| `SCDC-R08` | `SCDC-R08 Scalar SeqCDC tiny diagnostic` | `Runs the frozen authors' oracle corpus through every fragmentation schedule in one long-lived scalar process and records bounded raw lifecycle evidence.` | `("runtime.layerstack-phase1.seqcdc","benchmark","observability.resource_efficiency")` | `{"terminal":"Every feed schedule produces the frozen cut offsets and object identifiers; terminal visitor failure stops reads; ring, borrow, descriptor, and logical owners release; raw samples validate."}` | `{"terminal":("runtime.layerstack-phase1.seqcdc","benchmark","observability.resource_efficiency")}` | `"cli"` | `"e2e-core"` | `60000` | `("benchmark","phase1")` |
| `runtime.layerstack-phase1.seqcdc.selection` | `SeqCDC final selection qualification` | `Executes the frozen Stage 11 Raw, StreamCDC, and SeqCDC matched campaigns plus required host/release-runner and Prep 04 Phase-1 image rows.` | `("runtime.layerstack-phase1.seqcdc","phase1.qualification","benchmark","portability")` | `{"terminal":"All final selection, distribution, locality, physical-space, lifecycle-memory, required-runner, and pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root gates execute from matched evidence and the selected algorithm is recorded."}` | `{"terminal":("runtime.layerstack-phase1.seqcdc","phase1.qualification","benchmark","portability")}` | `"cli"` | `"e2e-core"` | `300000` | `("release","benchmark","phase1","config")` |

Supporting checks below are not additional typed E2E declarations:

- `SCDC-01` is the `run-now-focused` live declaration above and proves public
  bytes/revision, legacy authority, zero runtime candidate work, and cleanup.
- `SCDC-R01` (`run-now-focused`) proves exact authors' oracle cumulative cuts.
- `SCDC-R02` (`run-now-focused`) proves empty, short, minimum, target, maximum,
  threshold, opposing, jump, wrap, and tail semantics.
- `SCDC-R03` (`run-now-focused`) proves identical cuts and IDs for
  byte-at-a-time, patterned, random, short-read, and `Interrupted` readers.
- `SCDC-R04` (`run-now-focused`) proves no seek, re-read, or read after a
  terminal visitor error.
- `SCDC-R05` (`run-now-focused`) proves the 32 KiB ring, at most two borrowed
  slices, and no retained payload or chunk list.
- `SCDC-R06` (`run-now-focused`) proves one- and two-slice hashing equals the
  contiguous payload and golden object ID.
- `SCDC-R07` (`run-now-focused`) proves the code-size, safe/std-only, and exact
  zero external-dependency boundaries.
- `SCDC-R08` is the `run-now-tiny-bench` typed wrapper declared above.
- Integrated StreamCDC comparison is `deferred-to-stage_11` and must use the
  equal-distribution final selection campaign.

The live case uses exactly one declaration validation and reports it once. It is not allowed to call a private chunker, read `/eos` as its SUT, scrape logs, or infer core correctness from a successful publish.

## 5. Correctness and failure matrix

| Scenario | Input/injection | Expected result | Resource/residue expectation | Disposition |
| --- | --- | --- | --- | --- |
| Empty | zero bytes | zero chunks, summary zero | ring dropped, no visitor calls | stage-gating |
| Sub-minimum | 1..8,191 bytes | one actual-length final chunk | ≤2 slices | stage-gating |
| Exact boundaries | around 8,192/16,384/32,768 | exact oracle cuts, no padded tail | all bytes once | stage-gating |
| Threshold | sequence counts around 4/5/6 | exact author behavior | no rescan | stage-gating |
| Opposing slope | 49/50/51 | exact author behavior | no overflow | stage-gating |
| Jump | candidate positions around 511/512/513 and end | jump never crosses available; exact tail | scan offset monotonic | stage-gating |
| Ring wrap | chunk spans end/start | two ordered slices, same contiguous ID | max slices=2 | stage-gating |
| Fragmentation | all small split points and seeded schedules | cuts/IDs byte-equal to whole-reader/oracle | fixed ring | stage-gating |
| `Interrupted` | injected between fragments | retry with no state/counter drift | no duplicate callback | stage-gating |
| Source error | non-Interrupted at every state | typed error, no later chunks | all memory dropped | stage-gating |
| Visitor/hash error | fail on selected callback | stop exactly there, no retry/later callback | no descriptor/payload retained | stage-gating |
| Huge logical offset | checked counter fixture | fail before integer wrap | no artifact | stage-gating |
| Nondeterministic fixture order | permuted case execution | each fixture output unchanged | no global state | stage-gating |
| Runtime publish | deterministic multi-boundary file | ordinary v1 content/revision correct | runtime SeqCDC counters=0, no candidate subtree | stage-gating |
| Runtime timeout/cancel | pytest deadline/interruption | terminal failed case, never implicit retry | exact-ID LIFO cleanup and retained evidence | stage-gating |
| Distribution/performance miss | tiny diagnostic outside target | report honestly; does not change oracle | no fallback or production decision | deferred |

Any oracle, byte-coverage, fragmentation, bounded-memory, dependency, v1 compatibility, or cleanup failure blocks Stage 04. A tiny throughput/distribution miss is retained but cannot select/reject production SeqCDC by itself.

## 6. Tiny correctness and benchmark loop

The existing benchmark laboratory owns the `layerstack-phase1-tiny-seqcdc` schedule, bounded sampling, raw JSON, and immutable bundle. A bounded Stage 03 adapter invokes the already-built `seqcdc_tiny_loop`; the Rust test remains the author-oracle primitive and is not a second scheduler.

| Dimension | Required setup |
| --- | --- |
| Wall duration | aggregate target 30–60 seconds; each operation hard-capped below 60 seconds |
| Corpora | pre-generated empty/no-op; pinned boundary literals; exact 9,000-byte `S03-OPPOSING-JUMP` generator from the benchmark note; 1 KiB localized edit in a deterministic 1 MiB file; deterministic 1 MiB incompressible bytes; 256 small files totaling about 1 MiB; source-like/mixed/repeated bytes; fragmentation schedules; overwrite histories 1, 8, and 32 |
| Pair | control feeds each byte string contiguously through the frozen author oracle; candidate feeds the same bytes through counterbalanced fragmented `Read` schedules and the streaming scalar scanner |
| Sampling | one warmup and at least five alternating control/candidate pairs; prefer three warmups and ten pairs only when the sub-minute cap holds |
| Fixed context | identical host, filesystem/cache treatment, seed, corpus, profile/configuration, one thread, prebuilt binary, and operation order |
| Iteration | scan → synchronous typed hash visitor → compare ordered-cut digest/chunk IDs → drop |
| Output | raw per-pair JSON; literal algorithm/mode/digest/domain/kind/format; oracle revision and source/config/fixture SHA-256 values; input/scanned bytes; chunks; absolute elapsed/throughput; candidate/control ratios; comparisons/jumps/wrapped chunks; ring/slice/descriptor high-water; errors |
| Hard POC gate | every output equals the oracle; each operation <60 s; aggregate cap holds; ring≤32 KiB; slices≤2; descriptor current≤1; payload queue bytes=0; no retained owner |
| Explicit non-claim | insufficient samples make p95 unavailable; no integrated capture, fsync, manifest/index, publication, StreamCDC advantage, final space/RSS/performance, or portability qualification |

Timing uses `std::time::Instant`. The lab consumes a prebuilt probe and adds no Criterion, profiler, allocator, C helper, Python package, or benchmark dependency.

## 7. Memory-stability and reclamation test

| Resource | Measurement | Hard POC bound | Quiescence | Failure |
| --- | --- | --- | --- | --- |
| SeqCDC ring | test high-water/capacity assertion | exactly one ≤32 KiB | dropped on success/error/cancel | growth or multiple rings |
| borrowed payload | visitor instrumentation | one chunk, ≤2 slices, total≤32 KiB | borrow ends at callback return | owned/retained payload |
| downstream payload | visitor instrumentation | 0 bytes | always 0 | any queued/copied payload |
| descriptor | current/high-water | one in Stage 03; future contract 16/≤64 KiB | zero after callback | retained list |
| hash state | adapter scope | one fixed SHA state | zero after callback | global/shared state |
| worker/task/thread/channel | public/test observation | 0 | always 0 | any introduced owner |
| runtime SeqCDC scans/bytes/chunks | public observation | 0 | always 0 | nonzero or missing |
| workspace/command IDs | tracker/public snapshot | exact current case | poll 100 ms, ≤5 s to absent | leak |
| process/cgroup RSS, FD, mappings | existing sampler | Stage 00 diagnostic noise band only | report logical release separately | missing=`unavailable`; no Stage 11 pass |

Do not restart the daemon/test loop, call `malloc_trim`, swap allocator, manually purge cache, or sleep arbitrarily to manufacture a settled result. Scanner logical release is immediate. Final 384 MiB/128 MiB RSS caps and scale-flatness proof remain Stage 11.

## 8. Dependency and portability proof

| Gate | Evidence | Pass |
| --- | --- | --- |
| core package | manifest + metadata | std-only; no dependency/dev/build/target table or build script |
| source boundary | deterministic import scan + review | no sha/serde/rayon/async/OS/libc/FFI/unsafe/SIMD/backend/runtime types |
| LayerStack hashing | manifest/source diff | uses already-present `sha2`; no edge added/moved |
| external packages | canonical metadata before/after per frozen invocation | exact `(name,version,source,checksum)` equality |
| features | canonical resolved features | exact external feature equality |
| direct edges | parsed manifests | exact product-wide external-edge multiset equality |
| non-Rust/system/image | manifest/process/image inventory | no Python/npm/package/tool/service/helper/network/download/FUSE/database/privilege delta |
| host semantics | oracle/fragmentation/endian-width goldens | identical scalar cuts/IDs on current executed host |
| required releases | frozen matrix | current Stage 03 row is contract evidence only; unexecuted required row remains unverified and blocks final production |

`usize`, native endian, filesystem enumeration, host paths, target CPU
features, and target-image userland do not affect boundaries or IDs. The Stage
11 matrix executes x86_64/AArch64, every required Docker
host/release-runner, and pinned Ubuntu/Debian glibc, Alpine musl,
minimal/distroless, shell-less, read-only, and non-root rows, recording each
resolved platform manifest. Stage 03's stage-local pinned Ubuntu evidence
does not overstate that qualification.

## 9. Focused and final-stage commands

Before every live command, append a Plan/Run entry with exact commits, command, image, node, and cleanup ownership to `e2e/test-report.md` via `apply_patch`. Append Good/Defect/Fix immediately afterward. Never erase a failed attempt or automatically rerun a failing broad selection.

### Focused Rust proof

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack --all-targets --all-features -- -D warnings
cargo test --locked -p sandbox-runtime-layerstack-core --test seqcdc_author_oracle
cargo test --locked -p sandbox-runtime-layerstack-core --test seqcdc_boundaries
cargo test --locked -p sandbox-runtime-layerstack-core --test seqcdc_fragmentation
cargo test --locked -p sandbox-runtime-layerstack --test seqcdc_typed_ids
cargo test --locked -p sandbox-runtime-layerstack-core --test seqcdc_tiny_loop -- --ignored --nocapture --test-threads=1
```

The line/source/dependency audit runs as a separate focused gate; no full workspace suite substitutes for it.

### Safe catalog collection

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
PYTHONPATH=e2e \
.venv/bin/python -m harness.catalog.collect \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

### Focused live POC

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_seqcdc_dormant.py::test_SCDC_01_scalar_seqcdc_is_runtime_dormant \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

After a recorded fix only, rerun this exact node with `E2E_REBUILD_BINARY=0`.

### Exact dependency comparison

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo metadata --locked --all-features --format-version 1 \
  > /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/tmp/<run_id>/metadata-after.json

cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.venv/bin/python e2e/tools/verify_external_dependency_delta.py \
  --baseline .e2e-state/baselines/layerstack-phase1/<invocation-id> \
  --candidate .e2e-state/tmp/<run_id>/metadata-after.json \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --require-stdlib-crate sandbox-runtime-layerstack-core \
  --require-exact-external-delta-zero
```

Resolve `<run_id>` and `<invocation-id>` to explicit validated run-owned paths. Repeat for each frozen target/feature invocation. No broad glob is a cleanup target.

### Tiny benchmark laboratory

The Stage 03 preset/adapter are implementation deliverables. They reuse the sequential lab, consume the prebuilt probe, target 30–60 seconds, and write run-owned output only beneath `.benchmark-state/{runs,results}/<run-id>/`; the CLI has no `--output`.

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
  --plan layerstack-phase1-tiny-seqcdc \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --plan layerstack-phase1-tiny-seqcdc \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
# Interruption-only; recover validates owned journals and has no --plan.
../.benchmark-state/test-venv/bin/sandbox-benchmark recover \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

### Artifact compatibility validation

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.benchmark-state/test-venv/bin/python -m pytest \
  benchmark/backend/tests/compatibility/test_artifacts.py
```

### DO NOT RUN in Stage 03 — Stage 11 affected regression

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1 \
  e2e/runtime/workspace_session \
  e2e/manager/management/squash \
  e2e/manager/management/export \
  e2e/observability/resource_isolation \
  e2e/observability/resource_efficiency \
  e2e/compound/stress \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

### DO NOT RUN in Stage 03 — Stage 11 host/image matrix

The command below is the pinned-Ubuntu representative and runs once per
required native host. The Stage 11 scheduler must additionally cover pinned
Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and
non-root rows; this Stage 03 command alone cannot qualify the matrix.

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_portability_matrix.py \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

### DO NOT RUN in Stage 03 — Stage 11 full Phase 1 qualification

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
for PHASE1_PLAN in \
  layerstack-phase1-selection \
  layerstack-phase1-rss \
  layerstack-phase1-space \
  layerstack-phase1-qualification
do
  E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
  ../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
    --plan "$PHASE1_PLAN" \
    --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
    --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
    --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
  E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
  ../.benchmark-state/test-venv/bin/sandbox-benchmark run \
    --plan "$PHASE1_PLAN" \
    --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
    --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
    --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
done
```

## 10. Metrics and evidence contract

The immutable Stage 03 evidence bundle contains:

- exact product/test commits, dirty state, mandated
  `upgrade-2.0-phase-1` and its recorded newest approved immutable base,
  command/node/timeout, and run/case IDs;
- host/arch, Rust target, Docker versions, guest kernel/filesystem, image tag and available pinned OCI index/platform digests;
- oracle source revision/digest/license/extraction method and fixture manifest digest;
- algorithm `seqcdc-scalar-author-v1`, mode `increasing`, typed SHA-256 domain
  `EOS-LS2\0`, object kind `3`, two-byte format version `2`, profile version,
  and every fixed parameter;
- input fixture/generator/seed/digest/bytes; fragmentation schedule ID;
- `S03-OPPOSING-JUMP` expected/actual 50-opposing trace, jump
  `8,242→8,754`, first cutpoint `8,758`, and typed-ID digest;
- ordered cut digest, expected/actual count and first bounded mismatch; min/mean/p10/p50/p90/max; final-short flag;
- bytes read/scanned/hashed, comparisons, jumps, wrap count, visitor calls, typed object-ID aggregate;
- ring allocation/high-water, max slices, payload queue bytes, current/high-water descriptors, worker/task/thread/channel/permit counts;
- production physical non-test line count and unsafe/source-boundary result;
- v1 public revision/content before/after, authorities/routes, runtime SeqCDC scans/bytes/chunks, all candidate counters/resources, teardown;
- exact dependency package/version/features/direct/internal edge deltas and non-Rust/system/image inventories;
- elapsed diagnostic distributions with sample count and explicit non-qualification label;
- reporter setup/call/teardown/validation/cleanup states and execution-surface proof;
- explicit reason for every unavailable metric, miss, timeout, or hard failure.

Artifacts are bounded and content-addressed through the existing run mechanism. Never retain raw unbounded payload, arbitrary path/chunk IDs, secrets, or full per-cut logs. Missing required fields fail schema validation; they do not become zero.

### Performance arrival checkpoint

The tiny run must materialize
`.benchmark-state/results/<run_id>/stage-03-perf-report.json` and
`stage-03-perf-report.md` according to
[the Stage 03 benchmark note](benchmark_note.md). The JSON schema version is
`phase1.stage03.perf-report.v1`; Markdown is a human-readable rendering of the
same values. Required groups are provenance; immutable run/raw artifact links;
raw oracle/control and candidate samples; frozen baseline actual; required
pass target/cap; separately predeclared optimization target; candidate actual;
delta, ratio, and headroom; complexity/work counters; logical memory and
sampled RSS; allocated physical-space and payload-zero fields; cleanup; and
`DIAGNOSTIC_PASS|FAIL|OPEN` verdict. The first Markdown table exposes those
comparison fields per stage-owned metric. Missing required values produce
`OPEN` or `FAIL`, never an inferred pass.

Before the live command, append Plan/Run to `e2e/test-report.md`. After report
validation, append Good/Defect there and append a new row to
`benchmark_note.md`; never rewrite an earlier result. The stage-exit check must
resolve both report links and verify that their run ID and provenance match the
raw bundle. Stage 03 reports remain **DIAGNOSTIC**, never final qualification.

## 11. Stage exit verdict

Return **POC PASS** only if:

- every product Stage 03 case and SCDC-01 passes on the first recorded attempt or one explicitly fixed/re-recorded exact-node attempt;
- cuts exactly match the pinned oracle for every boundary corpus;
- fragmentation, `Interrupted`, wrap, visitor failure, byte coverage, and tail properties pass;
- the core uses one 32 KiB ring, ≤2 callback-scoped slices, no payload ownership/collection, no worker/task/thread/channel, and ≤300 non-test lines;
- typed chunk IDs are exact through LayerStack’s existing SHA adapter;
- core remains safe/std-only and exact external dependency delta is zero;
- packaged public behavior is legacy-correct, runtime SeqCDC/candidate values are present and zero, forbidden candidate paths are absent, and case resources quiesce;
- each operation is <60 seconds and the 30–60 second loop is labeled diagnostic;
- both versioned performance-arrival reports validate, resolve their immutable raw/run links, and have matching append-only benchmark and E2E ledger entries;
- evidence schemas/report entries/cleanup records are complete and durable.

Planning creates no branch. Execution requires the exact implementation branch `upgrade-2.0-phase-1`, created from the newest approved immutable product revision, with immutable product/test/doc bases recorded before work begins. Return **POC FAIL / BLOCKED** for an oracle mismatch, hidden rescan, fragmentation difference, invalid borrow/ownership, over-bound memory, unsafe/external dependency, v1 regression, candidate artifact, missing observation, leak, timeout, branch/base noncompliance, or mandatory environment failure.

This verdict only permits Stage 04 to integrate the same scalar implementation into a shadow writer. It does not establish ≥10% selection advantage, ≤1.14× unique payload, locality, final RSS/space, required-release portability, broad CI, release readiness, or production authority.
