# Stage 02 E2E — Portable root contract

[Implementation overview](../index.md) · [Stage 02 specification](spec.md) · [Preparation 03](../../prep/03-seqcdc-cas-and-squash-decision.md) · [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Product root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
Test root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`
Normative POC image: `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`

## 1. Stage-local test objective

This plan proves two deliberately separate claims:

1. pure Rust contract tests prove deterministic portable v2 bytes and typed IDs without a backend; and
2. one focused packaged live-Docker case proves that adding the dormant contract did not change legacy authority, public revision behavior, or resource cleanup.

This is a **POC proof tier**. It is not the Phase 1 performance, RSS-scale, storage-amplification, portability-matrix, recovery, release, or production-enablement gate. A broad test folder, full suite, nightly/release marker, or a favorable microbenchmark is not a Stage 02 exit.

Planning creates no branch. Implementation and execution require the exact
branch `upgrade-2.0-phase-1`, created from the newest approved immutable
product revision, with immutable product/test/doc bases recorded before work
begins. Stage 00 must pass; Stage 01 may proceed independently and is not an
entry condition. Docker must be healthy, and the test report must contain an
append-only planned-run entry. Every live resource is run-owned; cleanup uses
only exact sandbox, workspace, command, gateway-instance, and process-group
identities created by the run.

## 2. Existing assets to reuse

| Asset | Reuse | Limitation / required addition |
| --- | --- | --- |
| `e2e/harness/catalog/declarations.py` | Mandatory typed `@e2e_test`; one explicit declaration per live case | Every declared validation must receive exactly one terminal report. |
| `e2e/harness/runner/reporter.py` | Flush+fsync JSONL case result, setup/call/teardown, execution-surface proof, bounded logs/artifacts | Missing evidence is unavailable, never fabricated as zero. |
| `e2e/harness/runner/resources.py` and cleanup controller | Run-owned resource sampling and LIFO cleanup | No global Docker prune, gateway kill, process scan/kill, or other run’s workspace cleanup. |
| `e2e/runtime/workspace_session/test_publish_workspace_session.py` | Stable public CLI patterns and IDs such as `runtime.workspace-session.publish.changed` and `.no-op` | Existing cases remain compatibility references; Stage 02 does not relabel them as v2 proof. |
| `e2e/runtime/workspace_session/helpers.py` | `WorkspaceTracker`, public runtime/layerstack/snapshot helpers, monotonic polling, teardown evidence | Cleanup remains exact-ID and case-owned. No direct daemon/private route becomes the SUT. |
| Stage 00 bounded storage observations | Authority/route/resource counters through existing authenticated observability surface | Must expose explicit legacy authority and zero candidate owners; no per-path/object labels. |
| LayerStack v1 fixtures/tests | Current manifest, hash, copy, fsync, OCC behavior | Add immutable v2 binary/ID fixtures; do not regenerate v1 expectations. |
| `e2e/test-report.md` | Append-only Plan/Run/Good/Defect/Fix history | Append before each live command and after its result. Never erase a failed attempt. |
| E2E catalog collector | Safe collection without executing tests | Canonical command uses both explicit repository roots; README forms using stale `--ledger`/catalog paths are not used. |
| `benchmark/backend/benchmark_lab/planning.py`, `benchmark/backend/benchmark_lab/runner.py`, `benchmark/backend/benchmark_lab/artifacts.py`, `benchmark/backend/benchmark_lab/resource_sampling.py` | Existing sequential scheduling, paired raw samples, bounded resource evidence, and immutable run bundles | Add only the Stage 02 operation adapter/preset needed to schedule the prebuilt focused portable-root probe; do not add another scheduler. |

The live harness already reuses a responding gateway even with `E2E_REBUILD_BINARY=1`. The first focused run requests rebuild; an exact-node diagnostic rerun after a product fix may use `E2E_REBUILD_BINARY=0`, and that fact is recorded.

## 3. Resulting test tree

### Test/evidence tree

```text
ephemeral-sandbox/
└── crates/sandbox-runtime/
    ├── layerstack-core/tests/
    │   ├── canonical_contract.rs           [add] — exact bytes, ordering, rejection
    │   ├── host_independence.rs            [add] — raw bytes, width/endian vectors
    │   └── portable_root_tiny_loop.rs       [add] — ignored 30–60 s diagnostic
    └── layerstack/tests/
        ├── portable_root_golden.rs          [add] — existing-sha2 typed ID proof
        └── fixtures/cas/v2/
            ├── contract-v2.json             [add] — fixture metadata
            └── contract-v2.bin              [add] — immutable canonical bytes

ephemeral-sandbox-test/
├── e2e/runtime/layerstack_phase1/
│   ├── __init__.py                          [add]
│   ├── helpers.py                           [add] — public-only projections
│   └── test_portable_root_contract.py       [add] — one focused feature-off case
├── e2e/fixtures/layerstack_phase1/
│   └── portable-root-v2/
│       └── expected-contract.json           [add] — IDs/versions only, no product path
├── e2e/tools/
│   └── verify_external_dependency_delta.py  [reuse] — Stage 00 stdlib verifier
├── benchmark/backend/benchmark_lab/
│   ├── planning.py                          [modify] — register bounded portable-root probe
│   └── runner.py                            [modify] — schedule prebuilt probe inside existing custody
├── benchmark/presets/
│   └── layerstack-phase1-tiny-portable-root.yml [add] — paired sub-minute sentinel
├── .e2e-state/
│   ├── runs/<run_id>/                       [reuse] — run-owned immutable evidence
│   └── tmp/<run_id>/                        [reuse] — run-owned scratch; cleanup/recovery
└── e2e/test-report.md                       [reuse] — append-only
```

### Complete expected `/eos` tree

Stage 02 writes no v2 artifact. The live case may observe behavior only through public CLIs; an outside run-owned sampler may account for storage shape as independent evidence, not replace the public assertion.

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
with this exact optional delta; Stage 02 does not require or produce it:

```text
/eos/workspace/<workspace_session_id>/executions/<command_session_id>/transcript.log [D5; Stage 01 replacement]
/eos/namespace_execution/<legacy_namespace_execution_id>/transcript.log              [E1; compatibility-only and may be absent]
```

| Code/path | State; class | Owner | Create → durability → recovery → deletion | Root identity | Stage access | Bound; physical-space category | Permission/exposure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `A0 /eos` | existing namespace | installation/daemon | provisioned externally → mount durable → validate on boot → installation removal only | none | daemon R/W | one; contains all `T(t)` terms | masked from workload |
| `B0 layer-stack` | existing truth namespace | LayerStack | boot open → child fsync rules → legacy sweep → never transaction-recursive-delete | no v2 | legacy R/W | one; `L_hot+P_staging+M` | daemon-only, one filesystem |
| `B0a .storage-writer.lock` | existing coordination | LayerStack | open/lock → kernel-held exclusivity → reacquire after restart → close | none | legacy coordination | one FD; `M` | daemon-only |
| `B1 manifest.json` | authoritative truth | legacy publisher | temp/write/fsync → rename/parent fsync → validate/recover → supersede | v1 `root_hash`, expressly not `RootId` | sole legacy R/W/publication | one; `M` | daemon-only |
| `B0b workspace.json` | existing base-binding truth | base builder | bootstrap atomic write/fsync → boot validation → installation removal | physical v1 base reference only | legacy R/W | one; `M` | daemon-only |
| `B2 base/<id>` | native carrier truth | base builder | build/verify/fsync/rename → manifest reachability → approved installation cleanup | physical v1 ref only | legacy R | one current base; `L_hot` | lower read-only/masked |
| `B3 layers/<id>` | native carrier truth | legacy publisher | private staging → tree fsync/rename → manifest commit → legacy squash/reap | physical v1 ref only | legacy R/W | `O(D)`, final `D≤64`; `L_hot` | lower read-only/masked |
| `B4 staging/<id>` | transaction staging | legacy publisher | allocate private → write/fsync → rename or abort/boot reap | none | legacy W | admitted legacy transactions; `P_staging` | `0700`, masked |
| `B5 digest` | truth-adjacent v1 metadata | legacy publisher | post-carrier atomic write → recompute on recovery → carrier deletion | not a typed v2 object | legacy R/W | one/carrier; `M` | daemon-only |
| `B6 bytes` | accounting metadata | legacy publisher | atomic write → recount recovery → carrier deletion | none | legacy R/W | one/carrier; `M` | daemon-only |
| `C1 auditability` | existing audit truth | FileService | operation update/fsync → boot recovery → retention cleanup | blame remains separate from content | service R/W | configured bound; `M` | authenticated projection |
| `C2 recovery` | conditional recovery truth | workspace recovery | failed exact owner record/fsync → bounded boot retry → delete after reap | none | recovery R/W | failed sessions only; `P_staging+M` | daemon-only |
| `D1 manager.json` | active-owner truth | WorkspaceManager | atomic owner update/fsync → boot reconcile → supersede | none | workspace R/W | one; `M` | daemon-only |
| `D1a .export` | existing transient export scratch | export owner | exact run-owned create/write → public export completion or failure recovery → exact owner cleanup | none | export R/W | bounded active exports; `P_staging` | daemon-only, absent at quiescence |
| `D2 session` | active scratch | WorkspaceManager | create/admit → mount/use → publish/destroy → exact-id reap | none | workspace R/W | one per active session; `ΣU_active` | `0700` |
| `D3 upper` | writable scratch | workspace/capture | create → native writes → legacy capture → teardown/recovery delete | source bytes only; host path excluded | workspace R/W | unpublished allocation; `ΣU_active` | projected only as `/workspace` |
| `D4 work` | OverlayFS scratch | overlay/kernel | mount create → kernel state → unmount → session reap | none | provider R/W | one/session; `ΣU_active` | private |
| `D5 workspace/<session>/executions/<execution>/transcript.log` | optional Stage 01 replacement, absent from the Stage 00 branch-independent schema | command owner after Stage 01 | admit/append under cap → terminal close → Drop/session/boot cleanup | none | not touched by Stage 02 | transcript/terminal caps; `ΣU_active+M` | API-only, masked |
| `E0 namespace_execution` | Stage 00 command scratch; compatibility-only after Stage 01 | command owner or cleanup adapter, according to recorded layout epoch | admit/write/reap under Stage 00, or no new writes and exact legacy reap after Stage 01 | none | unchanged by Stage 02 | bounded transcript state; converges only after Stage 01 | masked |
| `E1 transcript` | active Stage 00 command scratch or legacy Stage 01 residue | recorded layout epoch owner | bounded append/close/reap; never inferred from directory presence alone | none | unchanged by Stage 02 | configured cap | `0700`, masked |
| `F1 runtime.sock` | ephemeral control | daemon | validate stale owner/bind → socket permissions → unlink shutdown/recovery | none | control R/W | one; `M` | `0600`, no image helper |
| `F2 runtime.pid` | ephemeral identity | gateway/daemon | atomic boot write → identity recovery → shutdown remove | none | daemon R/W | one; `M` | daemon-only |

Forbidden after setup, after the live action, and after teardown: `format-v2.json`, `roots/v2`, `manifests/v2`, `objects/v1`, `packs/v1`, `indexes/v1`, `catalogs/v1`, `journals/v1`, `staging/v2`, `leases/v1`, `retention/v1`, `maintenance/v1`, `materializations/docker-overlayfs/v1`, `quarantine/v1`, and `trash/v1`.

## 4. Typed E2E case catalog

Every row below uses only the Phase 1 pinned Ubuntu 24.04 target image.
Required host and release-runner coverage remains mandatory at each row's
listed disposition, while cross-image acceptance is deferred beyond Phase 1.

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `runtime.layerstack-phase1.portable-root.feature-off` | POC; `run-now-focused` | legacy authority with dormant portable contract | pinned Ubuntu 24 image, legacy config, deterministic changed/no-op inputs | public workspace write, publish, read | exact v1 bytes/revision, legacy routes, zero candidate work | diagnostic elapsed time | complete before/after allocation, zero candidate bytes | all case owners/tasks/FDs/sessions quiesce | exact external delta zero and pinned Ubuntu 24 record | `60000` ms | typed JSONL and public/route/resource/storage/cleanup snapshots |
| `PRC-R08` | POC; `run-now-tiny-bench` | canonical encode/decode/hash/drop | one long-lived process and deterministic paired corpus | typed wrapper invokes the bounded primitive campaign | exact canonical goldens on every iteration | raw pairs without normative p95 | encoded-byte series | owners and allocations release after every pair | std-only core and host-independent goldens | `60000` ms | raw JSON samples and summary |
| `runtime.layerstack-phase1.portable-root.release-matrix` | release; `planned-final` | required-runner portable-root qualification | required Stage 11 host/release runners using one pinned Ubuntu 24.04 target image | public qualification corpus | identical canonical IDs and compatible behavior on every required runner | normative Stage 11 metrics | complete physical envelope | full repeated-lifecycle matrix | required-runner evidence, pinned Ubuntu 24.04 target; cross-image deferred beyond Phase 1 | `300000` ms | Stage 11 qualification bundle |

Complete literal declaration metadata:

| Stable ID | Title | Description | Features | Validations | Validation features | Execution surface | Owner ID | Timeout (ms) | Pytest markers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `runtime.layerstack-phase1.portable-root.feature-off` | `PRC-01 Portable Root Contract Is Runtime-Dormant` | `A packaged Ubuntu 24.04 sandbox performs one public no-op and one changed workspace publication while legacy v1 remains the only read, write, and publication authority and every candidate resource gauge remains zero.` | `("runtime.workspace_session","runtime.layerstack-phase1.portable-root")` | `{"assert-prc-01-legacy-authority":"Public revision and content remain v1-compatible; configured, read, write, and publication routes are legacy; candidate completion, fallback, mismatch, worker, queue, permit, transaction, root, object, and durable-byte values are zero; case-owned resources are reclaimed."}` | `{"assert-prc-01-legacy-authority":("runtime.workspace_session","runtime.layerstack-phase1.portable-root")}` | `"cli"` | `"e2e-core"` | `60000` | `("smoke","phase1","config")` |
| `PRC-R08` | `PRC-R08 Portable root tiny canonical loop` | `Runs canonical encode, decode, hash, and drop over the deterministic portable-root corpus in one long-lived process and records bounded raw lifecycle evidence.` | `("runtime.layerstack-phase1.portable-root","benchmark","observability.resource_efficiency")` | `{"terminal":"Every repetition matches the frozen canonical bytes and identifiers, rejects no valid vector, retains no logical owner after drop, and emits schema-valid raw time, byte, and lifecycle samples."}` | `{"terminal":("runtime.layerstack-phase1.portable-root","benchmark","observability.resource_efficiency")}` | `"cli"` | `"e2e-core"` | `60000` | `("benchmark","phase1")` |
| `runtime.layerstack-phase1.portable-root.release-matrix` | `Portable root release matrix` | `Executes compatibility, memory, storage, and portable-identity qualification on every required host/release runner using the one pinned Ubuntu 24.04 target image; cross-image qualification is deferred beyond Phase 1.` | `("runtime.layerstack-phase1.portable-root","phase1.qualification","portability","ubuntu-24.04")` | `{"terminal":"Every required host/release-runner row produces the frozen canonical root identifiers and compatible public behavior against the pinned Ubuntu 24.04 target image with complete environment and lifecycle evidence; no cross-image acceptance is claimed."}` | `{"terminal":("runtime.layerstack-phase1.portable-root","phase1.qualification","portability","ubuntu-24.04")}` | `"cli"` | `"e2e-core"` | `300000` | `("release","phase1","config")` |

Supporting execution references below are not additional typed E2E declarations:

- `PRC-01` is the `run-now-focused` public CLI case declared above; it emits
  request/response, before/after revision, route/resource, cleanup, and
  execution-surface evidence.
- Existing `runtime.workspace-session.publish.no-op` is a
  `run-now-focused` compatibility reference when the fixture is required; it
  proves that no-op publication creates no v1 revision.
- Existing `runtime.workspace-session.publish.changed` is a
  `run-now-focused` compatibility reference when the changed-flow fixture is
  required; it proves one legacy revision and exact visible bytes.
- Cross-host root-ID acceptance executes in Stage 11 on every required runner
  using the pinned Ubuntu 24.04 target image. Cross-image acceptance is deferred
  beyond Phase 1 and is not an executable Phase 1 catalog row.

PRC-01 reports its one validation exactly once with the declaration-backed `validation(...)` context. Receiving a successful CLI response alone is insufficient: content, revision, authority, counters, and teardown all participate.

### Supporting product contract checks

These are Rust/product checks, not additional typed E2E declarations:

- `PRC-R01` (`run-now-focused`): exact bytes for
  empty/root/tree/metadata/reference records and exact decode round-trip.
- `PRC-R02` (`run-now-focused`): invalid UTF-8 accepted as bytes when otherwise
  valid; leading/trailing slash, NUL, empty, `.`, and `..` rejected; backslash
  unchanged.
- `PRC-R03` (`run-now-focused`): canonical result independent of input
  insertion and `Read` fragmentation.
- `PRC-R04` (`run-now-focused`): every identity-bearing field changes ID;
  backend, host, and materialization fields cannot enter the codec.
- `PRC-R05` (`run-now-focused`): hostile lengths, required bits,
  duplicate/unsorted keys, dangling references, and trailing bytes fail without
  panic or over-allocation.
- `PRC-R06` (`run-now-focused`): existing v1 bytes, hash, and publication tests
  remain unchanged.
- `PRC-R07` (`run-now-focused`): the core is std-only and the external
  dependency delta is exactly zero.
- `PRC-R08` is the `run-now-tiny-bench` typed wrapper declared above.

## 5. Correctness and failure matrix

| Scenario | Injection/input | Required correctness | Required residue/cleanup | Verdict |
| --- | --- | --- | --- | --- |
| Empty logical tree | canonical empty manifest/root | fixed bytes and IDs | pure values dropped | pass only exact golden |
| Raw non-UTF-8 path | valid relative byte sequence | byte-preserving encode/order/ID | none | pass |
| Host-looking separators | `a\\b` bytes | backslash remains data; no host normalization | none | pass |
| Traversal/ambiguous path | `/a`, `a/`, `a//b`, `.`, `..`, NUL | closed bounded error; no ID | no allocation retained | pass |
| Permuted entries/xattrs | every deterministic permutation | same canonical bytes/ID or explicit unsorted-input rejection followed by bounded sorter contract | no whole collection in production path | pass |
| Fragmented source/sink | all practical split points/short operations | same value and digest; injected I/O error yields no ID | scratch dropped | pass |
| Length/width overflow | `u32` length overflow, invalid nanos/extents | reject before allocation/arithmetic wrap | zero owner/permit | pass |
| Unknown version/capability | unknown required version/bit | reject, never downgrade | none | pass |
| Trailing/corrupt bytes | bit flips and suffixes | reject exact consumption/digest mismatch | none | pass |
| Physical-field mutation | host path, inode, carrier ID, locator changes in test adapter | impossible to encode into root; ID stays based only on logical record | none | pass |
| Identity-field mutation | tree ID/profile/publication/capability/parent changes | `RootId` changes | none | pass |
| Existing v1 no-op publish | public packaged CLI | no new v1 revision; no v2 route/artifact | exact workspace cleanup | pass |
| Existing v1 changed publish | public packaged CLI | exactly legacy revision/content contract | exact workspace cleanup | pass |
| Candidate observation missing | schema lacks required Stage 00 value | do not infer zero | retain failed artifact | fail |
| Unexpected v2 resource | nonzero candidate counter/byte/transaction or candidate namespace | legacy response cannot mask it | retain evidence, run-owned cleanup only | fail |
| Timeout/cancel | test deadline or process interruption | no fabricated pass; reporter terminal state | LIFO exact-ID cleanup/recovery record | fail |

Correctness precedes timing. A faster malformed decoder, changed v1 response, leaked session, or missing authority observation is a failure.

## 6. Tiny correctness and benchmark loop

The existing benchmark laboratory owns the `layerstack-phase1-tiny-portable-root` schedule, resource sampling, raw JSON, and immutable bundle. Its bounded Stage 02 adapter invokes the already-built `portable_root_tiny_loop` probe; the Rust test remains the focused primitive/oracle and does not become a second scheduler.

| Parameter | POC value |
| --- | --- |
| Duration | aggregate target 30–60 seconds; every operation hard-capped below 60 seconds |
| Inputs | pre-generated deterministic empty/no-op; 1 KiB localized edit in a 1 MiB file; deterministic 1 MiB incompressible file; 256 small files totaling about 1 MiB; raw-byte/mixed-metadata trees; overwrite histories 1, 8, and 32 |
| Pair | control decodes/verifies the frozen Stage 00 canonical fixture; candidate performs construct → validate → stream encode → existing LayerStack SHA-256 → compare typed ID → decode → drop over identical bytes |
| Sampling | one warmup and at least five counterbalanced alternating control/candidate pairs; prefer three warmups and ten pairs only when the sub-minute aggregate cap holds |
| Fixed context | same host, filesystem, cache treatment, seed, corpus, configuration, prebuilt binary identity, and operation order |
| Outputs | raw per-pair JSON; iterations; encoded bytes; absolute elapsed/throughput; candidate/control ratios; first/last ID; errors; peak codec scratch; run/environment identity |
| Gate | exact bytes/IDs and zero errors; every operation <60 s; aggregate within its declared cap; scratch ≤256 KiB; no logical owner after each pair |
| Non-claim | insufficient samples make p95 unavailable; no publication, fsync, CAS, SeqCDC selection, native execution, RSS-scale, final space/performance, or cross-host qualification claim |

The probe uses `std::time::Instant` and adds no Criterion, profiler, allocator, helper, or dependency. The benchmark lab consumes the prebuilt probe and writes only beneath its run-owned state; a malformed artifact, contract mismatch, or cap breach fails Stage 02.

## 7. Memory-stability and reclamation test

| Resource/source | POC observation | Bound | Settle rule | Failure |
| --- | --- | --- | --- | --- |
| core codec scratch | product test counter/returned high-water | ≤256 KiB/admitted operation | drop immediately after record | above cap or growth with entry history |
| live core values | test-scoped owner count | only current root/entry | zero between iterations | any retained owner |
| LayerStack SHA state | adapter operation scope | one fixed state | drop after finalize/error | retained/global state |
| daemon candidate workers/tasks | public bounded observation | 0 | always 0 | nonzero/missing |
| candidate queues/bytes/permits | public bounded observation | 0 | always 0 | nonzero/missing |
| candidate transactions/roots/objects/bytes | public bounded observation | 0 | always 0 | nonzero/missing |
| workspace/commands | public snapshot plus tracker | exact case IDs only | bounded poll every 100 ms, ≤5 s, to absent | leak/timeout |
| process/cgroup RSS | existing outside/public sampler | diagnostic raw baseline band only | report first/last/slope separately from logical release | missing source is `unavailable`; no Stage 11 pass |
| FD/mapping count | sampler when available | current Stage 00 band | settled after exact cleanup | unexplained positive trend |

No restart, `malloc_trim`, allocator swap, manual page-cache purge, or arbitrary settling sleep is allowed. Stage 02’s authoritative logical proof is that it adds no long-lived owner at all. Final RSS ≤384 MiB/≤128 MiB-above-idle and the 64/256/1024 MiB × 1/16/64-root matrix remain deferred to Stage 11.

## 8. Dependency and portability proof

The shared standard-library verifier compares canonical identities, not counts alone.

| Proof | Stage 02 pass condition |
| --- | --- |
| `cargo metadata --locked --all-features --format-version 1` per frozen invocation | external `(name,version,source,checksum)` set exactly equal |
| resolved features per package | external `(package,feature)` set exactly equal |
| parsed product manifests | direct external edge multiset exactly equal; no edge relocation |
| new core manifest | no dependencies, dev-dependencies, build-dependencies, target dependencies, build script, links, or proc macro |
| source import audit | no `serde`, `sha2`, OS/provider/runtime/OverlayFS/Docker/mount/namespace/guest/WASM import in core |
| graph audit | only LayerStack → core inward internal edge; cycle-free |
| non-Rust manifests/locks | byte-equal unless independently authorized; no Python/npm addition |
| host/system/image | no installed tool/package/service/helper/sidecar/FUSE/database/network/download/privilege delta |
| deterministic bytes | fixed raw-byte/endian/width goldens pass on current host |
| portability claim | `designed-compatible` only; no required-release row is called qualified until executed in Stage 11 |

LayerStack’s existing `sha2` and `serde` edges remain in place and perform outward implementation work. This is zero external edge delta, not a hidden dependency move.

## 9. Focused and final-stage commands

These forms were reconciled with the current workspace manifests, `e2e/conftest.py`, catalog collector, and gateway behavior. Before **each live command**, append its timestamp, commit(s), exact command, intended node, image, and ownership scope to `e2e/test-report.md` using an `apply_patch` append. After completion append `Good`, `Defect`, and `Fix/next action`; never rewrite earlier entries.

### Product focused tests

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack --all-targets --all-features -- -D warnings
cargo test --locked -p sandbox-runtime-layerstack-core --test canonical_contract
cargo test --locked -p sandbox-runtime-layerstack-core --test host_independence
cargo test --locked -p sandbox-runtime-layerstack --test portable_root_golden
cargo test --locked -p sandbox-runtime-layerstack-core --test portable_root_tiny_loop -- --ignored --nocapture --test-threads=1
```

Do not run all workspace tests as a Stage 02 exit substitute.

### Safe E2E catalog collection

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
PYTHONPATH=e2e \
.venv/bin/python -m harness.catalog.collect \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

Collector output, if retained, goes only below `.e2e-state/tmp/<run_id>/`. Do not use the stale README `--ledger` form.

### Focused live POC

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_portable_root_contract.py::test_PRC_01_portable_root_contract_is_runtime_dormant \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

Only after a recorded product/test fix, rerun the exact failed node with `E2E_REBUILD_BINARY=0`. Do not rerun a passing broad suite and do not silently retry a flaky/failing case.

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

`<run_id>` and `<invocation-id>` are resolved explicit run-owned values, never an unvalidated glob or broad cleanup target. Repeat for every frozen target/feature invocation.

### Tiny benchmark laboratory

The preset and bounded operation adapter are Stage 02 deliverables. They use the existing sequential laboratory and the prebuilt product/test artifact; they do not rebuild. Expected aggregate duration is 30–60 seconds, and output is run-owned beneath `.benchmark-state/{runs,results}/<run-id>/` because the CLI has no `--output` option.

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
  --plan layerstack-phase1-tiny-portable-root \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --plan layerstack-phase1-tiny-portable-root \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
# Interruption-only recovery validates all run-owned journals; recover has no --plan.
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

### DO NOT RUN in Stage 02 — Stage 11 affected regression

Stage 11 owns this cumulative selector; it is not a Stage 02 exit gate.

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

### DO NOT RUN in Stage 02 — Stage 11 native-host/pinned-Ubuntu-24 matrix

Stage 11 runs this command once per required native host and records the
resolved platform digest. Pinned Ubuntu 24 is the only Phase 1 E2E image;
cross-image portability is deferred beyond Phase 1 and is not an acceptance
gate.

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

### DO NOT RUN in Stage 02 — Stage 11 full Phase 1 qualification

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

Every retained POC bundle records:

- run/case ID; exact product/test commits and dirty state; mandated
  `upgrade-2.0-phase-1` and its recorded newest approved immutable base;
- host OS/architecture, Docker Desktop/Engine, guest kernel/filesystem, the sole pinned Ubuntu OCI index, and the verified resolved platform-manifest digest;
- Rust/Cargo/Python/pytest versions; config digest; gateway rebuild/reuse fact;
- declaration fields, exact pytest node, command, timeout, execution-surface proof;
- validation terminal record with expected/actual and bounded artifact references;
- v1 revision/layer count/hash before and after no-op/changed actions;
- configured/read/write/publication authority and candidate completion/fallback/mismatch counts;
- candidate live workers/tasks, queue items/bytes, permits, transactions, roots, objects, durable bytes;
- exact case-owned sandbox/workspace/command IDs and teardown snapshot;
- canonical fixture version/domain/type, byte count/digest, expected/actual typed ID, mutation/rejection class;
- codec scratch high-water and logical owner count; diagnostic RSS/cgroup/FD/mapping source or explicit unavailable;
- exact external package/version, feature, direct-edge, internal-edge, lockfile, source-boundary, system/image dependency deltas;
- `/eos` outside-accounting categories if collected, with candidate namespaces explicitly absent and no raw path exposed publicly;
- elapsed times labeled diagnostic, sample count, and exact reason for every miss.

Evidence values are bounded. Raw payload, arbitrary paths/xattrs, target-image secrets, unbounded logs, and object-cardinality labels are forbidden. Missing accounting fails the relevant gate rather than becoming zero. JSONL/result/artifact writes use the harness’s flush+fsync lifecycle; interrupted runs remain recoverable and visible.

## 11. Stage exit verdict

Return **POC PASS** only when:

- all eight focused product cases and PRC-01 pass without an unrecorded retry;
- canonical bytes/IDs are exact, hostile inputs fail closed, and v1 fixtures remain unchanged;
- the live case proves legacy-only read/write/publication authority and public behavior;
- every candidate gauge is present and zero, and the complete forbidden candidate subtree is absent from outside evidence;
- case-owned resources reach explicit quiescence and cleanup has no leaked ID;
- the core is std-only/safe/cycle-free and the exact external dependency delta is zero for every frozen invocation;
- each focused operation is under 60 seconds and the diagnostic loop is 30–60 seconds;
- all artifacts validate, missing sources are explicit, and `e2e/test-report.md` contains append-only Plan/Run/Good/Defect/Fix entries.

Return **POC FAIL / BLOCKED** for any mismatch, missing authority/resource evidence, v1 regression, candidate artifact, dependency delta, leak, timeout, malformed artifact, execution outside mandated `upgrade-2.0-phase-1` or without its recorded newest approved immutable base, or unavailable mandatory environment. Preserve the first failure and exact cleanup result.

This verdict does **not** authorize Stage 04 shadow writes, candidate reads,
migration, broad CI, release qualification, required-host portability claims,
final performance/memory/space claims, or production enablement. Stage 11 must
execute every required host/release-runner row using the same pinned Ubuntu OCI
index and record the resolved platform manifest. Cross-image portability is
deferred beyond Phase 1 and is neither an acceptance nor a retirement gate.
This verdict only unblocks the independently gated Stage 03 scalar SeqCDC
implementation.
