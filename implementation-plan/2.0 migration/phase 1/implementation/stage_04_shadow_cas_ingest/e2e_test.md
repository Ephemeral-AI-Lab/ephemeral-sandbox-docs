# Stage 04 E2E — Shadow CAS ingest

[Implementation overview](../index.md) · [Stage 04 specification](spec.md) · [Preparation 03](../../prep/03-seqcdc-cas-and-squash-decision.md) · [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Product root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
Test root: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`
Normative POC image: `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`

## 1. Stage-local test objective

Stage 04 proves the first candidate-artifact writer without transferring any authority from legacy v1.

- A focused live-Docker case publishes changed bytes through the existing public CLI in a run-owned `shadow_write` configuration. It proves that v1 commits first and remains the sole read, write, OCC, revision, and publication authority while one correlated shadow transaction completes.
- A second focused live-Docker case proves that a public no-op publication creates no candidate root or transaction.
- Focused Rust integration tests prove canonical candidate artifacts, native-carrier locators, journal ordering, crash recovery, failure isolation, bounded memory, and exact empty reserved namespaces.
- One ignored 30–60 second Rust loop provides diagnostic incremental-work and resource evidence.

This is a **POC proof tier**. It does not add or test a candidate public reader, mount, `HEAD`, root selector, authoritative response field, hydration path, pack writer, compactor, garbage collector, retention authority, migration, squash, or SeqCDC-versus-StreamCDC selection. Broad/full, nightly, release, three-host portability, scale-RSS, and final benchmark gates remain deferred to their owning stages.

The live cases must first prove public v1 bytes and revision through the CLI. Candidate observations and host storage inventories are separately labeled evidence; neither may replace public behavior assertions or become a public candidate API.

## 2. Existing assets to reuse

| Existing asset | Stage 04 reuse | Constraint |
| --- | --- | --- |
| Stage 02 portable root contract | Canonical path/tree/object/root bytes, typed IDs, domain separation, bounded encoder ports | Core remains safe/std-only and contains no filesystem, hashing implementation, serde, config, or provider. |
| Stage 03 scalar SeqCDC | One-pass cuts over a committed immutable carrier | One 32 KiB ring/worker, at most two slices/chunk, no owned payload/chunk collection. |
| Existing `sandbox-runtime` LayerStack | v1 carrier/manifest publication, existing SHA-256/serde/filesystem duties | v1 commit remains the linearization point and sole authority. |
| Workspace capture | Freeze-consistent change discovery | Shadow mode replaces whole-publication metadata collections with bounded runs; payload bytes are never queued. |
| Stage 00 observations | Bounded route, checkpoint, candidate status, resource, and physical-accounting snapshots | Scalars/capped fields only; no arbitrary paths, payload, or per-chunk labels. |
| `e2e/harness/catalog/declarations.py` | Immutable full `@e2e_test` metadata | Exactly one terminal checkpoint record per declared validation. |
| `e2e/harness/runner/reporter.py` | Durable JSONL phases, validation, cleanup, execution-surface, logs, and artifacts | Flush+fsync each record; missing/unavailable differs from zero. |
| `e2e/harness/runner/resources.py` | Run-owned sampling and LIFO cleanup | Exact run-owned identities only; no broad kill, prune, or storage delete. |
| Public workspace-session CLI helpers | Create, write, publish, read, revision, and cleanup | No private daemon route, direct product-storage read, or log scrape as the SUT. |
| Configuration-family ownership | Serial gateway/config replacement and restoration | `shadow_write` is test-scoped; checked production/benchmark defaults remain `legacy`. |
| Catalog collector | Declaration/discovery validation without execution | Explicit roots; optional output only below `.e2e-state/tmp`. |
| `e2e/test-report.md` | Append-only planned/run/good/defect/fix ledger | Append before every live command and immediately after its outcome. |
| `benchmark/backend/benchmark_lab/planning.py`, `benchmark/backend/benchmark_lab/runner.py`, `benchmark/backend/benchmark_lab/artifacts.py`, `benchmark/backend/benchmark_lab/resource_sampling.py` | Existing sequential scheduling, paired raw samples, bounded resource sampling, and immutable bundles | Extend only the operation/config projection needed to alternate legacy and `shadow_write`; no second scheduler. |

`E2E_REBUILD_BINARY=1` requests a rebuilt packaged daemon on cold start, but a responding gateway may be reused. The evidence must say which occurred. `E2E_REBUILD_BINARY=0` is allowed only for an exact failed-node rerun after the defect and fix have been appended.

## 3. Resulting test tree

### Test and evidence tree

```text
ephemeral-sandbox/
└── crates/sandbox-runtime/
    ├── layerstack-core/tests/
    │   └── stage04_contract_regression.rs                    [add]
    └── layerstack/tests/
        ├── shadow_ingest.rs                                  [add]
        ├── shadow_failpoints.rs                              [add]
        ├── shadow_recovery.rs                                [add]
        ├── shadow_resources.rs                               [add]
        ├── shadow_tiny_loop.rs                               [add] — prebuilt focused probe
        └── fixtures/cas/v2/shadow-v1/
            ├── README.md                                     [add]
            ├── carrier.bin                                   [add]
            └── expected.json                                 [add]

ephemeral-sandbox-test/
├── e2e/runtime/layerstack_phase1/
│   ├── helpers.py                                            [reuse]
│   ├── shadow-write.yml                                      [add]
│   └── test_shadow_ingest.py                                 [add]
├── e2e/fixtures/layerstack_phase1/shadow-v1/
│   └── live-payload-manifest.json                            [add]
├── e2e/tools/verify_external_dependency_delta.py             [reuse] — Stage 00
├── benchmark/backend/benchmark_lab/
│   ├── planning.py                                          [modify] — register shadow/control mode
│   └── runner.py                                            [modify] — alternate modes under existing custody
├── benchmark/presets/layerstack-phase1-tiny-shadow-ingest.yml [add]
├── .e2e-state/
│   ├── runs/<run_id>/                                       [reuse] — run-owned
│   │   └── stage04-shadow-ingest/                           [add] — emitted at run time
│   └── tmp/<run_id>/                                        [reuse] — run-owned
└── e2e/test-report.md                                       [reuse] — append-only
```

`shadow-write.yml` is a complete checked test fixture, not a production default. The case owns exclusive configuration/gateway setup, records the prior state, and restores it in LIFO cleanup. The fixture must differ from the checked legacy configuration only by explicit test-safe settings and `rollout_mode: shadow_write`.

### Complete expected `/eos` tree

Tags below distinguish existing authority, active candidate evidence, fixed-but-empty candidate namespaces, scratch, quarantine, and remove-later compatibility state.

```text
/eos/                                                                  [E0]
├── layer-stack/                                                       [L0]
│   ├── .storage-writer.lock                                           [L0a]
│   ├── manifest.json                                                  [L1]
│   ├── workspace.json                                                 [L0b]
│   ├── base/<base_id>/                                                [L2]
│   ├── layers/<layer_id>/                                             [L3]
│   ├── staging/<layer_id>.staging/                                    [L4]
│   ├── .layer-metadata/
│   │   ├── <layer_id>.digest                                          [L5]
│   │   └── <layer_id>.bytes                                           [L6]
│   ├── format-v2.json                                                 [V0]
│   ├── roots/v2/<prefix>/<RootId>.root                               [V1]
│   ├── manifests/v2/<prefix>/<TreeManifestId>.manifest               [V2]
│   ├── objects/v1/loose/                                              [O0]
│   │   └── <prefix>/<object_id>.obj                                  [O1]
│   ├── packs/v1/
│   │   ├── open/<transaction_id>.pack                                [P1]
│   │   └── sealed/<pack_id>.pack                                     [P2]
│   ├── indexes/v1/
│   │   ├── pages/<page_id>.idx                                       [I1]
│   │   └── index.catalog                                              [I2]
│   ├── catalogs/v1/
│   │   ├── roots.catalog                                              [C1]
│   │   ├── locators.catalog                                           [C2]
│   │   ├── materializations.catalog                                   [C3]
│   │   ├── leases.catalog                                             [C4]
│   │   └── retention.catalog                                          [C5]
│   ├── journals/v1/
│   │   ├── publication/<transaction_id>.journal                       [J1]
│   │   ├── hydration/                                                 [J2]
│   │   ├── squash/                                                    [J3]
│   │   ├── compaction/                                                [J4]
│   │   └── migration/                                                 [J5]
│   ├── staging/v2/
│   │   ├── publication/<transaction_id>/                              [T1]
│   │   ├── hydration/                                                 [T2]
│   │   ├── squash/                                                    [T3]
│   │   ├── compaction/                                                [T4]
│   │   └── migration/                                                 [T5]
│   ├── leases/v1/                                                     [A1]
│   ├── retention/v1/                                                  [A2]
│   ├── maintenance/v1/                                                [A3]
│   ├── materializations/docker-overlayfs/v1/                          [M0]
│   ├── quarantine/v1/<transaction_id>/                                [Q1]
│   └── trash/v1/<durable_epoch>/<artifact_id>                          [X1]
├── storage/
│   ├── file_auditability/                                             [S1]
│   └── workspace_recovery/                                            [S2]
├── workspace/
│   ├── manager.json                                                   [W1]
│   ├── .export/<spool_id>                                             [W1a]
│   └── <workspace_session_id>/                                        [W2]
│       ├── upper/                                                     [W3]
│       └── work/                                                      [W4]
├── namespace_execution/                                               [N0]
│   └── <namespace_execution_id>/transcript.log                        [N1]
└── runtime/daemon/
    ├── runtime.sock                                                   [R1]
    └── runtime.pid                                                    [R2]
```

This is the branch-independent Stage 00 scratch schema required by Stage 04.
If parallel Stage 01 has independently passed and its checkpoint is present,
replace only `N1` with the following exact delta; Stage 04 neither requires nor
produces that delta:

```text
/eos/workspace/<workspace_session_id>/executions/<command_session_id>/transcript.log [W5; Stage 01 replacement]
/eos/namespace_execution/<legacy_namespace_execution_id>/transcript.log              [N1; compatibility-only and may be absent]
```

| Code/path | State/class and owner | Lifecycle, durability, recovery, deletion | Identity/authority and access | Bound/accounting/exposure |
| --- | --- | --- | --- | --- |
| `E0 /eos` | existing namespace; installation/daemon | provision → boot validation → installation removal only | no identity; daemon R/W | one; all `T(t)` terms; masked |
| `L0 layer-stack` | existing v1 authority plus candidate subtree; LayerStack | child-specific durability/recovery; never broad-delete for one transaction | v1 authority plus non-authoritative evidence | `L_hot+P_staging+M`; daemon-only |
| `L0a .storage-writer.lock` | existing coordination; LayerStack | open/lock → kernel-held exclusivity → reacquire after restart → close | no logical identity or public authority | one FD; `M`; daemon-only |
| `L1 manifest.json` | sole authoritative truth; legacy publisher | temp/write/fsync → rename/parent fsync → OCC/boot validate → supersede | only public read/write/revision/publication authority; not a v2 `RootId` | one; `M`; daemon-only |
| `L0b workspace.json` | existing base-binding truth; base builder | bootstrap atomic write/fsync → boot validation → installation removal | physical v1 base reference only | one; `M`; daemon-only |
| `L2 base/<id>` | authoritative immutable carrier; base builder | verify/install/fsync → v1 reachability → legacy-approved delete | candidate locator source; carrier/path excluded from IDs; shadow verified-read only | one base; `L_hot`; masked lower |
| `L3 layers/<id>` | authoritative immutable carrier; legacy publisher | legacy stage/fsync/rename → v1 commit → legacy deletion policy | candidate locator source only; shadow reads after commit | existing `D`, final≤64; `L_hot`; masked lower |
| `L4 staging` | legacy transaction staging; legacy publisher | private create/write/fsync → promote or exact abort/boot reap | no identity; candidate forbidden | admitted v1 transaction; `P_staging`; `0700` |
| `L5 digest` | v1 metadata; legacy publisher | atomic write/recompute/delete with carrier | comparison only; not typed v2 ID | one/carrier; `M`; daemon-only |
| `L6 bytes` | v1 accounting; legacy publisher | atomic write/recount/delete with carrier | no identity | one/carrier; `M`; daemon-only |
| `V0 format-v2.json` | candidate format truth; format initializer | create once via temp/fsync/rename/parent fsync → exact validation → candidate-only rollback | declares versions; no public authority | one≤64 KiB; `M`; daemon-only |
| `V1 roots/v2/<prefix>/<RootId>.root` | immutable candidate truth; shadow transaction | staged canonical bytes → ID verify/fsync/promote/dir fsync → validate → candidate retention/rollback only | bytes hash to filename `RootId`; no `HEAD`/public reader | one/completed checkpoint; ≤256 KiB root; `M` |
| `V2 manifests/v2/<prefix>/<TreeManifestId>.manifest` | immutable candidate reconstruction object; shadow transaction | staged stream → domain-typed ID verify/fsync/promote → recovery validate | strong root edge; no public authority | disk-backed bounded records; `M` |
| `O0 objects/v1/loose` | candidate namespace, reserved-empty; future writer | initialize/validate only | no Stage 04 child access | payload bytes=0; `H_cold=0`; daemon-only |
| `O1 loose object` | absent/reserved; future writer | any child is a format failure/quarantine trigger | forbidden | must remain zero |
| `P1 packs/open` | reserved-empty; Stage 08 | initialize and require empty | forbidden | payload/staging zero |
| `P2 packs/sealed` | reserved-empty; Stage 08 | initialize and require empty | forbidden | `H_cold=0` |
| `I1 index pages` | candidate index; shadow transaction | stage/checksum/fsync/promote → catalog install → keep/quarantine | physical locators excluded from IDs; candidate R/W | 4 KiB pages; cache≤4,096 pages=16 MiB |
| `I2 index.catalog` | candidate index-generation truth; shadow transaction | stage/fsync/atomic install/parent fsync → generation validation | selects only candidate index generation | one active + bounded recovery generation; `M` |
| `C1 roots.catalog` | candidate checkpoint correlation; shadow transaction | stage after root durable → atomic install/fsync → reconcile | `(v1 revision/hash)→RootId/status`; explicitly not `HEAD` | disk-backed; bounded cache; observation only |
| `C2 locators.catalog` | candidate physical-locator truth; shadow transaction | verify carrier ranges → stage/fsync/install → recovery revalidate | locator outside object/root identity | target≤96 B/chunk amortized; daemon-only |
| `C3 materializations.catalog` | reserved-empty; Stage 05 | initialize and validate one empty generation | no materialization identity or mount authority | fixed empty generation; `M` |
| `C4 leases.catalog` | reserved-empty authority catalog; future stage | initialize one empty generation only | no v2 lease may be granted | fixed empty; `M` |
| `C5 retention.catalog` | reserved-empty authority catalog; future stage | initialize one empty generation only | no retention selection | fixed empty; `M` |
| `J1 publication` | candidate recovery truth; shadow transaction/recovery | create/fsync before candidate writes → monotonic fsynced states → `Complete` → exact reap after durable catalogs | expected IDs/checkpoint only; no public authority | one/admitted txn; strict residue bound; `0600` |
| `J2 hydration` | reserved-empty; Stage 05 | initialize only | child writes forbidden | zero |
| `J3 squash` | reserved-empty; Stage 09 | initialize only | child writes forbidden | zero |
| `J4 compaction` | reserved-empty; Stage 08 | initialize only | child writes forbidden | zero |
| `J5 migration` | reserved-empty; Stage 10 | initialize only | child writes forbidden | zero |
| `T1 publication` | candidate metadata staging; shadow transaction | exact txn mkdir → runs/pages/records → fsync/promote or exact quarantine/reap | staged bytes have no identity until verified/promoted | payload=0; metadata only; `P_staging`; `0700` |
| `T2 hydration` | reserved-empty; Stage 05 | initialize only | forbidden | zero |
| `T3 squash` | reserved-empty; Stage 09 | initialize only | forbidden | zero |
| `T4 compaction` | reserved-empty; Stage 08 | initialize only | forbidden | zero |
| `T5 migration` | reserved-empty; Stage 10 | initialize only | forbidden | zero |
| `A1 leases/v1` | reserved-empty lease records; future stage | initialize only | no candidate lease authority | zero/fixed metadata |
| `A2 retention/v1` | reserved-empty policy; future stage | initialize only | no candidate retention authority | zero/fixed metadata |
| `A3 maintenance/v1` | reserved-empty cursors; Stage 08+ | initialize only | no background maintenance | zero |
| `M0 materializations/docker-overlayfs/v1` | reserved-empty; Stage 05 | initialize and require empty | no materialization identity or mount reader | zero carriers; `C_target=0`; daemon-only |
| `Q1 quarantine` | candidate failure evidence; recovery | move exact attributable txn/fsync → explicit candidate cleanup | never selected; v1 untouched | configured quota; counted; redacted daemon-only |
| `X1 trash` | reserved-empty deletion staging; future GC | initialize only | Stage 04 cannot trash authority/candidate root | zero |
| `S1 auditability` | existing audit truth; FileService | durable update → recovery → retention | separate from content identity | configured; `M`; authenticated |
| `S2 workspace_recovery` | conditional recovery truth; recovery owner | exact-owner fsync → bounded retry → delete after reap | no identity | failures only; `P_staging+M`; daemon-only |
| `W1 manager.json` | workspace ownership truth | atomic update/fsync → boot reconcile → supersede | no content identity | one; `M`; daemon-only |
| `W1a .export` | transient export scratch; export owner | exact run-owned create/write → completion or failure recovery → exact-owner cleanup | no content identity | bounded active exports; `P_staging`; absent at quiescence |
| `W2 session` | active scratch; WorkspaceManager | create/freeze/mount → publish/destroy → exact-ID cleanup | no content identity | active sessions; `ΣU_active`; `0700` |
| `W3 upper` | writable capture scratch | write → freeze → streamed capture → teardown | bytes influence v1/v2; host path excluded | `C_capture`; `/workspace` projection only |
| `W4 work` | OverlayFS scratch | mount → kernel use → unmount/reap | none | one/session; `ΣU_active`; masked |
| `W5 transcript` | consolidated command scratch | capped append → close → Drop/session/boot reap | none | capped; `ΣU_active+M`; API-only |
| `N0 namespace_execution` | compatibility root, remove-later | no new writes → exact pre-upgrade reap → remove after window | cleanup-only | converges zero; masked |
| `N1 legacy transcript` | old scratch, remove-later | close/reap only | cleanup-only | legacy cap; `0700` |
| `R1 runtime.sock` | ephemeral control; daemon | stale-owner validation/bind → unlink on shutdown/recovery | authenticated control only | one; `M`; `0600` |
| `R2 runtime.pid` | ephemeral identity; gateway/daemon | atomic boot write → recovery → shutdown remove | no content identity | one; `M`; daemon-only |

For a completed changed shadow publication, only `V0–V2`, `I1–I2`, `C1–C3`, `J1`, `T1`, and failure-only `Q1` may receive Stage 04 children. At clean settle, its `J1` and `T1` transaction children are absent. `M0`, `O0/O1`, `P1/P2`, `C4/C5`, `J2–J5`, `T2–T5`, `A1–A3`, and `X1` remain empty. Legacy mode creates no candidate subtree or work.

## 4. Typed E2E case catalog

Every row below uses only the Phase 1 pinned Ubuntu 24.04 target image.
Required host and release-runner coverage remains mandatory at each row's
listed disposition, while cross-image acceptance is deferred beyond Phase 1.

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `runtime.layerstack-phase1.shadow-ingest.changed` | POC; `run-now-focused` | post-v1-commit `shadow_write` | pinned Ubuntu 24.04 target image, serial owned config/gateway, deterministic edit | public write, publish, read | exact v1 sole authority, one correlated shadow completion, zero payload writes | diagnostic phase elapsed | complete subtree inventory and envelope | tasks, queues, permits, transactions, FDs settle | exact external delta zero and pinned-environment record | `60000` ms | typed JSONL plus public/shadow/resource/storage/cleanup snapshots |
| `runtime.layerstack-phase1.shadow-ingest.no-op` | POC; `run-now-focused` | no-op `shadow_write` | same owned config after changed-case cleanup | public no-op publish | unchanged v1, no candidate root or transaction, skipped counter increments | diagnostic elapsed | no journal/staging/root allocation delta | all owners settle and config/gateway restores | same dependency/image bundle | `60000` ms | typed JSONL plus before/after/cleanup snapshots |
| `SCI-R07` | POC; `run-now-tiny-bench` | incremental candidate ingest | long-lived process, private temporary storage root, deterministic corpus | typed wrapper invokes v1 commit and post-commit ingest campaign | exact roots, locators, counters, zero payload writes, bounded normal work | raw paired diagnostics | allocated bytes by subtree/class | logical owners settle every pair and RSS is classified | std-only core and exact external delta | `60000` ms | raw JSON, summary, dependency/layout inventories |
| `runtime.layerstack-phase1.shadow-ingest.qualification` | release; `planned-final` | final shadow-ingest qualification | frozen Stage 11 presets and required runners using one pinned Ubuntu 24.04 target image | packaged matched workloads | all final correctness, benchmark, storage, memory, and runner gates | normative matched metrics | complete physical envelope | full scale and repeated lifecycle | required runners, pinned Ubuntu 24.04 target; cross-image deferred beyond Phase 1 | `300000` ms | Stage 11 qualification bundle |

Complete literal declaration metadata:

| Stable ID | Title | Description | Features | Validations | Validation features | Execution surface | Owner ID | Timeout (ms) | Pytest markers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `runtime.layerstack-phase1.shadow-ingest.changed` | `SCI-01 Changed Publish Commits V1 Before Shadow Evidence` | `In a run-owned shadow_write Ubuntu 24.04 configuration, public CLI operations publish and read deterministic changed bytes while v1 stays the sole authority and one correlated metadata-only shadow ingest completes with zero duplicate payload writes.` | `("runtime.workspace_session","runtime.layerstack-phase1.shadow-ingest")` | `{"assert-sci-01-v1-authoritative-shadow-complete":"The public v1 revision advances exactly once and returns the exact published bytes; the response exposes no candidate root or status; bounded evidence correlates exactly one completed shadow root to that v1 checkpoint, reports zero candidate payload writes and no mismatch, and all case-owned resources and completed journal or staging children quiesce."}` | `{"assert-sci-01-v1-authoritative-shadow-complete":("runtime.workspace_session","runtime.layerstack-phase1.shadow-ingest")}` | `"cli"` | `"e2e-core"` | `60000` | `("smoke","phase1","config")` |
| `runtime.layerstack-phase1.shadow-ingest.no-op` | `SCI-02 No-op Publish Creates No Candidate Transaction` | `In the same run-owned shadow_write Ubuntu 24.04 configuration, a public publish with no changed state preserves the v1 revision and creates no candidate root, transaction, journal, or staging child.` | `("runtime.workspace_session","runtime.layerstack-phase1.shadow-ingest")` | `{"assert-sci-02-no-op-has-no-shadow-transaction":"Public bytes and revision are unchanged; candidate completion, root, and transaction counts do not increase; skipped_no_op_count increases exactly once; payload writes remain zero; resources quiesce and run-owned cleanup restores the prior gateway configuration."}` | `{"assert-sci-02-no-op-has-no-shadow-transaction":("runtime.workspace_session","runtime.layerstack-phase1.shadow-ingest")}` | `"cli"` | `"e2e-core"` | `60000` | `("smoke","phase1","config")` |
| `SCI-R07` | `SCI-R07 Incremental shadow ingest tiny diagnostic` | `Runs the deterministic changed-entry corpus through metadata-only post-commit ingest in one long-lived process and records exact identity, work, disk, and memory evidence.` | `("runtime.layerstack-phase1.shadow-ingest","benchmark","observability.resource_efficiency")` | `{"terminal":"Every iteration produces the frozen root and locator records, writes no duplicate payload, reports bounded normal work, releases transaction and worker owners, and emits schema-valid raw samples and inventories."}` | `{"terminal":("runtime.layerstack-phase1.shadow-ingest","benchmark","observability.resource_efficiency")}` | `"cli"` | `"e2e-core"` | `60000` | `("benchmark","phase1")` |
| `runtime.layerstack-phase1.shadow-ingest.qualification` | `Shadow ingest final qualification` | `Executes the frozen Stage 11 matched workloads, scale matrix, recovery faults, storage and memory gates, and required host/release-runner rows using the one pinned Ubuntu 24.04 target image; cross-image qualification is deferred beyond Phase 1.` | `("runtime.layerstack-phase1.shadow-ingest","phase1.qualification","benchmark","portability","ubuntu-24.04")` | `{"terminal":"All final shadow-ingest correctness, zero-duplicate-payload, recovery, time, storage, memory, and required-runner gates execute successfully against the pinned Ubuntu 24.04 target image with complete matched evidence; no cross-image acceptance is claimed."}` | `{"terminal":("runtime.layerstack-phase1.shadow-ingest","phase1.qualification","benchmark","portability","ubuntu-24.04")}` | `"cli"` | `"e2e-core"` | `300000` | `("release","benchmark","phase1","config")` |

Supporting checks below are not additional typed E2E declarations:

- `SCI-01` and `SCI-02` are the two `run-now-focused` live declarations above.
- `SCI-R01` (`run-now-focused`) proves exact canonical root, manifest, index,
  catalog bytes, and typed IDs.
- `SCI-R02` (`run-now-focused`) proves ordered non-overlapping locator ranges
  cover each chunk and resolve only into verified immutable v1 carriers.
- `SCI-R03` (`run-now-focused`) proves each
  write/fsync/rename/intent/install/comparison boundary preserves v1 and
  recovers idempotently.
- `SCI-R04` (`run-now-focused`) proves typed failure and quarantine with no v1
  mutation or leaked owner, permit, or file descriptor.
- `SCI-R05` (`run-now-focused`) proves the exact canonical subtree, empty
  reserved children, and absence of a candidate `HEAD`.
- `SCI-R06` (`run-now-focused`) proves normal work `O(U+E+K)` and separately
  labels the one-time bootstrap `O(C_current+E_current+K_current)`.
- `SCI-R07` is the `run-now-tiny-bench` typed wrapper declared above.
- The dependency/source/system/image inventory is `run-now-focused` and proves
  exact zero external delta and no new runtime, tool, or image requirement.
- Small-edit p95, scale RSS, and final selection/locality/space campaigns are
  `deferred-to-stage_11`.

Each declaration has exactly one terminal validation checkpoint and reports it exactly once. A missing observation is `unavailable`, never inferred as zero. Neither case reads `/eos`, invokes an internal LayerStack method, or scrapes logs as its SUT.

## 5. Correctness and failure matrix

| Scenario/boundary | Injection or setup | Expected candidate result | Required v1/public result | Cleanup/residue disposition |
| --- | --- | --- | --- | --- |
| Legacy mode | checked default config | no candidate format/path/task/counter movement | ordinary successful v1 publish/read | no candidate residue; stage-gating regression |
| Changed shadow publish | deterministic file set | one matching root/catalog observation after v1 commit | revision +1; exact public bytes; legacy authority | completed journal/staging reaped; stage-gating |
| Shadow no-op | unchanged session | no root/transaction; skipped count +1 | revision/bytes unchanged | no journal/staging child; stage-gating |
| First bootstrap | no prior candidate checkpoint | explicitly labeled full current-tree stream | v1 already committed/unchanged | excluded from normal timing; stage-gating correctness |
| Incremental edit | prior candidate exists; small `U/E/K` | only changed carrier/events plus bounded merge work | v1 already committed/unchanged | work counters match `O(U+E+K)`; stage-gating |
| Native carrier locator | chunks span SeqCDC/ring boundaries | exact carrier ID/path bytes/offset/length; all hashes verify | carrier remains v1-owned | no loose/pack payload; stage-gating |
| Candidate admission denied | 64 MiB semaphore or publication budget unavailable | `ResourceExhausted`, no partial catalog selection | committed v1 success unchanged | exact staging reaped or journal-owned; stage-gating |
| Descriptor queue saturation | 16 items or 64 KiB reached | producer backpressures to deadline then typed failure | v1 unchanged | queue drains/owner releases; stage-gating |
| Source read failure | each ingest phase | transaction fails/quarantines exact attributable evidence | v1 unchanged/readable | no callback after error; stage-gating |
| Manifest/object write failure | before/after write/fsync | journal state does not advance past durable fact | v1 unchanged | boot resumes or quarantines exact txn |
| Index page/catalog failure | page write/fsync/rename/catalog install boundaries | no catalog points to non-durable page | v1 unchanged | previous candidate generation remains valid |
| Root write failure | write/fsync/rename/dir-fsync boundaries | no roots catalog selects non-durable root | v1 unchanged | recover/quarantine exact txn |
| Catalog intent/install failure | every intent/fsync/rename/parent-fsync boundary | monotonic recovery chooses old or complete new generation | v1 unchanged | no split candidate selection |
| Comparison mismatch | candidate canonical/export digest differs | status mismatch; exact txn/root quarantined or retained unselected | successful v1 response is not rewritten | mismatch evidence durable/bounded; stage-gating defect |
| Client cancellation after v1 commit | cancel before shadow completion | journal/recovery owns candidate continuation; request callbacks fenced | v1 commit semantics unchanged | no orphan task/permit |
| Daemon crash/restart | states `Prepared`, `ManifestObjectsDurable`, `LocatorIndexDurable`, `RootDurable`, `CatalogIntentDurable`, `CatalogsInstalled`, `Compared`, `Complete` | replay is idempotent; complete or quarantine exact txn once | v1 opens and serves normally | no full-history scan; residue bound |
| Corrupt candidate journal | checksum/schema/ID corruption | safely attributable txn quarantined; otherwise candidate initialization disabled | legacy service opens | no broad delete/repair |
| Corrupt candidate catalog/page | checksum/generation corruption | previous valid candidate generation or disabled shadow route | v1 service opens | corrupt candidate bytes quarantined/accounted |
| Carrier disappeared by legitimate v1 policy | recovery references absent carrier | `missed_source`; candidate-only txn reaped/quarantined | no carrier resurrection or manifest change | terminal bounded evidence |
| Unexpected reserved child | object/pack/future journal/staging/lease/trash child | format violation; shadow disabled/quarantine | v1 service opens | no silent adoption |
| Panic in worker | panic at each owned resource | candidate txn terminal/journal-owned; worker failure visible | v1 unchanged | permit, borrow, queue/FD guards release; shutdown joins |
| Clean shutdown | admitted and queued work | stop admission, journal/drain within deadline, join four workers | normal legacy shutdown | zero active tasks/queue/permits/transactions |

A product-test failure in canonical bytes, locator coverage, authority ordering, crash recovery, resource release, dependency delta, or reserved layout blocks the live case. A live v1-content/revision/authority failure is a product defect even if candidate evidence looks correct.

## 6. Tiny correctness and benchmark loop

The existing benchmark laboratory owns `layerstack-phase1-tiny-shadow-ingest`: sequential custody, alternating mode order, bounded sampling, raw JSON, and immutable artifacts. The already-built `shadow_tiny_loop` remains a focused transaction/oracle probe consumed by the lab; it is not a second scheduler.

| Dimension | Required setup |
| --- | --- |
| Duration | aggregate target 30–60 seconds; every publication hard-capped below 60 seconds |
| Corpus | pre-generated empty/no-op; 1 KiB localized edit in deterministic 1 MiB; deterministic 1 MiB incompressible file; 256 small files totaling about 1 MiB; alternating 4 KiB edit/64 KiB append; histories 1, 8, and 32 |
| Pair | legacy control and `shadow_write` candidate use identical bytes/profile/config except rollout mode; candidate adds only post-v1-commit metadata ingest |
| Sampling | one bootstrap/warmup per mode and at least five counterbalanced alternating measured pairs; prefer three warmups and ten pairs only if the sub-minute cap holds |
| Fixed context | same host, filesystem, cache treatment, seed, corpus, prebuilt binary, gateway custody, and operation order |
| Iteration | v1 commit → optional bounded shadow ingest → exact v1/candidate digest/locator/counter checks → quiescence → exact run-owned cleanup |
| Outputs | raw per-pair JSON; absolute elapsed/throughput and ratios; `U/E/K`; source read/scanned/hashed bytes; metadata/index/fsync counters; candidate physical categories; resource high-waters |
| Hard POC gate | exact public v1 outputs/authority; exact candidate metadata; payload writes/loose/packs/`H_cold`=0; work proportional to `U+E+K`; configured bounds; no completed journal/staging residue |
| Diagnostic only | insufficient samples make p95 unavailable; no final selection, RSS, space, portability, or production qualification claim |

The loop uses run-owned state, no target-image helper/network/database/additional process, and no arbitrary sleep. It polls quiescence every 100 ms for at most 5 seconds and treats timeout, malformed artifacts, or cleanup residue as failure.

## 7. Memory-stability and reclamation test

| Resource | Hard Stage 04 bound | Measurement | Required terminal state |
| --- | --- | --- | --- |
| Worker pool | 4 globally | current/idle/high-water + joined-owner count | 4 idle during service; all 4 joined at shutdown |
| SeqCDC ring | 32 KiB/active worker | allocation/owner instrumentation | no active ring after task |
| Borrowed chunks | ≤1/worker, ≤4 global; ≤2 slices/chunk | current/high-water | zero |
| Payload queue | 0 bytes/items | explicit invariant counter | zero always |
| Descriptor queue | ≤16 items and ≤64 KiB serialized | current/high-water | zero |
| Capture/sort/publication metadata | ≤4 MiB/publication excluding shared page cache | charged byte permits and run-file accounting | zero managed allocation; exact files removed |
| Manifest/journal encoder | ≤256 KiB/admitted operation | encoder capacity high-water | zero |
| Merge readers | fan-in 8 ×64 KiB | open reader/current bytes high-water | zero |
| Index page cache | ≤4,096 ×4 KiB =16 MiB | logical pages/bytes plus diagnostic RSS | within bound; evictable, no publication owner |
| Global managed-memory semaphore | 64 MiB | permits in use/high-water | zero |
| Tasks/transactions | bounded by four admitted workers | registry current/high-water and journal correlation | zero or explicitly durable recovery-owned; clean settle zero |
| FDs/mappings | workers + 8 merge readers + current journal/catalog; no mmap required | `/proc`/runtime outside observation where available | return to baseline tolerance; mappings zero |
| Journals/staging | `≤1 MiB + min(1% retained bytes,64 MiB)` and no pending clean transaction | physical inventory | completed transaction children absent |

Focused tests run success, cancellation, each failpoint, panic, and restart in one long-lived test process. After each phase they poll the logical terminal state, then sample host RSS/FDs as diagnostic evidence. Logical leaks, monotonic task/permit growth, unbounded queue/cache growth, or unexplained physical residue fail Stage 04. Allocator-retained RSS alone is reported rather than called a leak; scale-RSS qualification remains deferred.

## 8. Dependency and portability proof

The before/after inventory is canonicalized and compared as a set, not reviewed manually.

| Surface | Required proof |
| --- | --- |
| Cargo packages | exact equality of external `(name,version,source,checksum)` tuples |
| Cargo features | exact equality of enabled external feature tuples |
| Direct edges | exact equality of external `(workspace package,dependency,features,kind,target)` multiset |
| New core | `sandbox-runtime-layerstack-core` resolves only `std` and workspace-internal code; no build script/unsafe/FFI |
| Existing runtime | hashing/persistence/provider adapters remain in existing `sandbox-runtime` code and reuse existing `sha2`/`serde`/OS edges |
| Source/tool inventory | no new Python/npm/system package, generator, sidecar, database, FUSE, C/C++, privilege, network, or download |
| Runtime image | sole Phase 1 target `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`; no code/userland executes inside the target image for ingest |
| Host determinism | golden root/object/chunk IDs match across debug/release and available architectures; canonical widths/order and raw Linux relative path bytes |
| Physical portability | carrier path/ID/offset, catalog generation, page placement, journal ID, and backend materialization are excluded from logical IDs |
| Backend boundary | future backend supplies capture/materialization/locator adapters; it cannot change root/object/canonical SeqCDC semantics |

The Stage 04 POC records one required-host row using the sole pinned Ubuntu OCI
index and the exact inventory. Stage 11 retains the final required
macOS/Linux/Windows host and release-runner gate, using that same OCI index on
every applicable host and recording the resolved platform manifest. Cross-image
portability is deferred beyond Phase 1 and is neither an acceptance nor a
retirement gate.

## 9. Focused and final-stage commands

Commands use absolute roots and the existing product package name. Before **each** live command, append its exact node, image, config, roots, timeout, and intended evidence to `e2e/test-report.md`. Append `Good`, `Defect`, and, after a repair, `Fix` immediately; never erase or overwrite a failure.

### Product gates

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack --all-targets --all-features -- -D warnings
cargo test --locked -p sandbox-runtime-layerstack-core --test stage04_contract_regression
cargo test --locked -p sandbox-runtime-layerstack --test shadow_ingest
cargo test --locked -p sandbox-runtime-layerstack --test shadow_failpoints
cargo test --locked -p sandbox-runtime-layerstack --test shadow_recovery
cargo test --locked -p sandbox-runtime-layerstack --test shadow_resources
cargo test --locked -p sandbox-runtime-layerstack --test shadow_tiny_loop -- --ignored --nocapture
```

Each filter/test target must first be confirmed by listing the matching `sandbox-runtime-layerstack-core` or `sandbox-runtime-layerstack` package; resolve a mismatch and record it rather than broadening to the workspace.

### External dependency gate

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo metadata --locked --all-features --format-version 1 \
  > /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/tmp/<run_id>/metadata-after.json

cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.venv/bin/python e2e/tools/verify_external_dependency_delta.py \
  --baseline /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/baselines/layerstack-phase1/<invocation_id> \
  --candidate /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/tmp/<run_id>/metadata-after.json \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --require-stdlib-crate sandbox-runtime-layerstack-core \
  --require-exact-external-delta-zero
```

`<run_id>` and `<invocation_id>` are execution-time values, not shell variables. Resolve them to explicit validated run-owned paths before running.

### Catalog validation

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
PYTHONPATH=e2e .venv/bin/python -m harness.catalog.collect \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

The optional catalog output, if requested, goes only below `.e2e-state/tmp/<run_id>`. Do not use the obsolete README `--ledger` form.

### Focused live POC

Run `SCI-01` first. After its terminal report and cleanup, append the next planned entry and run `SCI-02`.

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
SANDBOX_GATEWAY_CONFIG_YAML=/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/runtime/layerstack_phase1/shadow-write.yml \
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_shadow_ingest.py::test_SCI_01_changed_publish_commits_v1_before_shadow_evidence \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
SANDBOX_GATEWAY_CONFIG_YAML=/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/runtime/layerstack_phase1/shadow-write.yml \
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_shadow_ingest.py::test_SCI_02_no_op_publish_creates_no_candidate_transaction \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

If a recorded defect is fixed, rerun only its exact node with `E2E_REBUILD_BINARY=0`. Do not retry an unrelated/broad selector. On interruption, preserve the bundle, run only exact run-owned cleanup, and record whether gateway/config restoration completed.

### Tiny benchmark laboratory

The preset/config projection are Stage 04 deliverables. They reuse the existing sequential lab, alternate matched legacy and `shadow_write` trials, consume prebuilt binaries, target 30–60 seconds, and write only beneath `.benchmark-state/{runs,results}/<run-id>/`; there is no `--output`.

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
  --plan layerstack-phase1-tiny-shadow-ingest \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --plan layerstack-phase1-tiny-shadow-ingest \
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

### DO NOT RUN in Stage 04 — Stage 11 affected regression

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

### DO NOT RUN in Stage 04 — Stage 11 native-host/pinned-Ubuntu-24 matrix

Stage 11 runs this command once per required native host. Pinned Ubuntu 24 is
the only Phase 1 E2E image; cross-image portability is deferred beyond Phase 1
and is not an acceptance gate.

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

### DO NOT RUN in Stage 04 — Stage 11 full Phase 1 qualification

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

Each live case produces one run-owned, fsynced bundle with:

```text
.e2e-state/runs/<run_id>/stage04-shadow-ingest/
├── declaration.json
├── result.jsonl
├── environment.json
├── public-before.json
├── public-publish.json
├── public-after.json
├── shadow-before.json
├── shadow-after.json
├── resources.jsonl
├── storage-inventory-before.json
├── storage-inventory-after.json
├── dependency-delta.json
├── cleanup.json
└── artifacts.json
```

| Evidence family | Required fields/assertions |
| --- | --- |
| Identity/environment | run/case/invocation IDs, git SHA/dirty state, host/kernel/arch, image digest, gateway PID/epoch, rebuilt-or-reused, exact config digest, product/test roots |
| Public behavior | session ID, v1 revision/hash before/after, operation status, exact content digest/size, stable response schema, explicit absence of candidate root/status/authority |
| Shadow correlation | transaction ID, v1 revision/hash, candidate root correlation, mode, terminal status, journal terminal state, bootstrap/incremental/no-op label, mismatch/error kind |
| Logical work | `U`, `E`, `K`, paths/events, carrier bytes read, SeqCDC scanned/hashed bytes, chunks/descriptors, merge runs/passes/readers, index pages, fsync/rename counts |
| Payload invariant | candidate payload bytes staged/written=0, loose object count/bytes=0, open/sealed pack count/bytes=0, `H_cold=0` |
| Candidate physical | root/manifest/index/catalog/materialization bytes, journal/staging/quarantine bytes, unreachable/unexplained bytes, `L_hot`, `U_active`, `P_staging`, `M`, whole-filesystem used/free |
| Resources | active/idle workers, rings/borrows, queue items/bytes, encoder bytes, cache pages/bytes, publication bytes, semaphore permits, tasks/transactions, FDs/mappings, current/high-water |
| Layout | versioned inventory with every expected path code, active/reserved classification, reserved unexpected children, mode/permission/owner where available |
| Failure/recovery | injected boundary, durable journal state before/after, recovery action, replay count, quarantine reason/bytes, v1 before/after proof |
| Timing | monotonic operation/phase elapsed, quiescence wait, sampling cadence; POC diagnostic only |
| Cleanup | exact owned resources, LIFO action/outcome, config/gateway restoration, zero live case-owned session/container/temp path |

The reporter writes setup/call/teardown, the single declared validation checkpoint, cleanup, execution-surface proof, bounded stdout/stderr, and artifact references as durable JSONL. Candidate observations are sampled before and after and correlated by checkpoint/transaction, not inferred from logs. Host `/eos` inspection is outside evidence after public assertions; it must not be used to decide whether the publish itself succeeded.

All counters carry units, scope, source, timestamp/epoch, and availability. Saturation is explicit. Logs and artifacts redact arbitrary paths/content, xattrs, secrets, and unbounded IDs. Evidence must retain a candidate mismatch or cleanup failure even when the public v1 operation succeeded.

## 11. Stage exit verdict

Planning creates no branch. Implementation and execution require the exact branch `upgrade-2.0-phase-1`, created from the newest approved immutable product revision, with immutable product/test/doc bases recorded before work begins.

Stage 04 passes only when all of the following are true:

- Stages 02–03 remain green, the new core remains std-only, and the exact external dependency/feature/direct-edge/source/system/image delta is zero.
- Checked production and benchmark configs default explicitly to `legacy`; legacy mode creates no candidate path or work.
- `SCI-01` proves exact public v1 bytes/revision and legacy-only authority, then exactly one correlated shadow completion with no public candidate field.
- `SCI-02` proves a no-op creates no candidate root/transaction and increments only the bounded skipped counter.
- Candidate payload writes, loose objects, packs, and `H_cold` are exactly zero; locators reference verified immutable v1 carrier ranges and are excluded from logical identity.
- Canonical roots/manifests/index/catalogs/materialization records match goldens; no candidate `HEAD` or public resolver exists.
- Every journal/failure/cancel/panic/restart test preserves v1, recovers or quarantines only the exact candidate transaction, and never performs a full-history or broad delete.
- Normal incremental work is `O(U+E+K)` plus bounded external ordering. Any first full scan is labeled bootstrap and excluded from normal samples.
- Four workers, rings, borrows, queues, encoder, merge, cache, per-publication, semaphore, task, transaction, FD, mapping, and residue bounds hold; clean settle has zero active owners and no completed journal/staging child.
- The complete `/eos` inventory matches the active/reserved lifecycle table; every future namespace remains empty and all unexplained candidate residue is zero.
- Both focused live cases produce exactly one terminal validation checkpoint, durable complete evidence, exact run-owned cleanup, and restored gateway/config state.

Final small-edit latency, scale RSS, candidate-read correctness, hydration, pack/GC/compaction, squash, migration, multi-host portability, selection/locality, and release space gates remain explicitly deferred. No favorable POC result authorizes Stage 05 or changes v1 authority by itself.
