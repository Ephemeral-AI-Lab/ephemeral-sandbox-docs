# Stage 07 E2E — Durable candidate-private publication

Links: [implementation overview](../index.md) · [simplified storage contract](../layerstack_storage_contract.md) · [stage specification](spec.md) · [benchmark note](benchmark_note.md) · [quantitative contract](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Tier: **POC proof tier**. Mandatory now: one packaged OCC/idempotency/recovery case, one durable lease/restart case, and one sub-minute paired benchmark/memory sentinel. Public candidate authority and broad qualification remain later work.

## 1. Stage-local test objective

Implementation execution is blocked unless the product worktree is on the
exact fresh branch `upgrade-2.0-phase-1`, created from the newest approved
immutable product revision, with its base commit, upstream, clean scoped
worktrees, and responsible implementer recorded before any code edit. This
planning stage creates or switches no branch; any mismatch is a hard blocker.

Prove that the packaged product can publish a v2 root durably into a separately named candidate-validation branch while a normal public publish remains exclusively legacy. The focused tests target double authority, mutable capture reads, non-idempotent retries, stale-writer loss, broad serialization, transaction/ref disagreement, expired/stale lease reuse, crash residue, and unbounded publication resources.

> **Performance arrival checkpoint.** Stage 07 is not reached until its
> [benchmark note](benchmark_note.md) tracker has a new append-only row and the run emits
> versioned `.benchmark-state/results/<run-id>/stage-07-perf-report.json` and
> `stage-07-perf-report.md` with
> `schema_version="phase1.stage07.perf-report.v1"`. Each report contains the
> frozen raw baseline actual, required pass target/cap, separately predeclared
> optimization target, candidate actual, delta, ratio, and headroom,
> complexity/work counters, logical-resource high-water counters, memory/RSS,
> physical space, run/raw-artifact
> links, provenance, missing values, and a
> `DIAGNOSTIC_PASS|FAIL|OPEN` verdict. The first Markdown table exposes those
> comparison fields per stage-owned metric.
> Append the command and
> `Good`/`Defect`/`Fix` plus cleanup to `e2e/test-report.md`. These reports are
> diagnostic; only Stage 11 qualifies the Prep gates.

Invariants:

1. Public publish response/head/layer are legacy v1; candidate transaction can mutate only its validation-branch key.
2. The private transaction consumes the same command-fenced frozen change stream, not a later mutable upper.
3. Atomic replacement and directory `fsync` of the selected `refs/heads/<BranchId>.ref`, after root/object durability and `ready`, is the sole candidate linearization point.
4. Same request/intent retry returns exactly the same `RootId`, generation, and receipt; different intent under that request is rejected.
5. Disjoint concurrent changes rebase/commit; overlapping or stale incompatible changes conflict without lost update.
6. Recovery reconciles `intent`/`ready` with authoritative refs and fences; neither transaction fact alone proves commit. Pre-commit failure leaves the old head, and a post-commit lost response returns committed.
7. Root/carrier/transaction leases survive restart, reject stale fences, and release deterministically; no Stage 07 code deletes data.
8. Resources quiesce and publication physical peak/memory gates hold; `mismatch_count=0`.

The real packaged route is existing public workspace finalize/publish with generated `candidate_publish_private`; the candidate receipt is structured observation, not a new public storage API. The private branch can be strictly activated/materialized only for comparison. Retention/packs/GC, squash/remount, candidate public authority/default, legacy retirement, and full matrices are deferred.

## 2. Existing assets to reuse

| Asset | Exact path | Use |
| --- | --- | --- |
| Public workspace publication | `ephemeral-sandbox-test/e2e/runtime/workspace_session/test_publish_workspace_session.py` | legacy response/head, concurrent workspaces, tracked cleanup |
| Workspace command/finalize | `e2e/runtime/workspace_session/test_exec_finalize.py` | command fence/cancel/join before frozen capture |
| Workspace helpers | `e2e/runtime/workspace_session/helpers.py` | public file/tree/archive digest and session custody |
| Manager export helpers | `e2e/manager/management/export/` | deterministic streaming archive/tree evidence; `.export` remains separate |
| Typed declaration contract | `e2e/harness/catalog/declarations.py:17-48` | stable metadata and complete validation reporting |
| Gateway/rebuild custody | `e2e/harness/runner/config.py`; `e2e/harness/runner/gateway.py` | safe generated config and fresh/reuse mode |
| Resource samplers | `e2e/observability/resource_isolation/helpers.py`; `e2e/observability/resource_efficiency/helpers.py`; `e2e/observability/resource_efficiency/profile.py`; `e2e/observability/resource_efficiency/test_workspace_reclaim.py` | RSS/cgroup/FD/task/allocated-byte/quiescence |
| Benchmark CLI | `benchmark/backend/benchmark_lab/cli.py` | current `validate`, `run`, `compare`, `recover`, `cleanup` campaign owner |
| Publication presets | `benchmark/presets/publication.yml`; `benchmark/presets/payload-scaling.yml`; `benchmark/presets/workspace-size-count.yml`; `benchmark/presets/quick-smoke.yml` | workload/timing/physical-space vocabulary |
| Stage 03–06 artifacts | product core goldens, `.e2e-state/runs/<stage-run-id>/evidence/`, `.benchmark-state/results/<benchmark-run-id>/` | fixed identity, materialization comparison, strict route |
| Append-only report | `e2e/test-report.md` | planned command before execution, result after |

Failpoint control must use a bounded test-only configuration seam compiled/wired outside production `src` where possible; it cannot become an unguarded public API. Outside `/eos` inspection proves durable boundaries, while public CLI assertions prove public authority and behavior.

## 3. Resulting test tree

```text
ephemeral-sandbox/
├── crates/sandbox-runtime/layerstack-core/tests/
│   ├── publication_golden.rs                                     [add]
│   └── publication_properties.rs                                 [add]
├── crates/sandbox-runtime/layerstack/tests/
│   ├── publication_transaction.rs                                [add]
│   ├── publication_occ.rs                                        [add]
│   └── publication_recovery.rs                                   [add] — exhaustive failpoint matrix
└── crates/sandbox-runtime/operation/tests/candidate_private_publish.rs [add]

ephemeral-sandbox-test/
├── e2e/runtime/layerstack_phase1/
│   ├── publication_helpers.py                                    [add] — generated branch/config/failpoint and artifact custody
│   ├── test_candidate_private_publication.py                     [add]
│   └── test_spec.md                                              [modify] — typed Phase 1 catalog
├── benchmark/presets/candidate-publication-tiny.yml              [add]
├── benchmark/tests/fixtures/golden/layerstack_phase1/
│   ├── candidate-publication-tiny.json                           [add] — deterministic corpus manifest
│   └── publication_result_v1.json                               [add] — result validation fixture
├── .e2e-state/runs/<run-id>/evidence/                            [add] — emitted at run time
│   ├── declaration-results.json                                  [add] — emitted at run time
│   ├── publication-routes-receipts.jsonl                         [add] — emitted at run time
│   ├── occ-results.json                                          [add] — emitted at run time
│   ├── lease-results.json                                        [add] — emitted at run time
│   ├── eos-before.json                                           [add] — emitted at run time
│   ├── eos-prepared.json                                         [add] — emitted at run time
│   ├── eos-objects.json                                          [add] — emitted at run time
│   ├── eos-root.json                                             [add] — emitted at run time
│   ├── eos-commit-intent.json                                    [add] — emitted at run time
│   ├── eos-committed.json                                        [add] — emitted at run time
│   ├── eos-failure.json                                          [add] — emitted at run time
│   ├── eos-cleanup.json                                          [add] — emitted at run time
│   ├── recovery-actions.json                                     [add] — emitted at run time
│   ├── tree-digests.json                                         [add] — emitted at run time
│   ├── resource-summary.json                                     [add] — emitted at run time
│   ├── benchmark-raw.json                                        [add] — emitted at run time
│   ├── dependency-before.json                                    [add] — emitted at run time
│   └── dependency-after.json                                     [add] — emitted at run time
├── .benchmark-state/runs/<benchmark-run-id>/                     [add] — emitted at run time; lab-owned
└── .benchmark-state/results/<benchmark-run-id>/                  [add] — emitted at run time; lab-owned
```

### Full storage tree and boundary states

```text
/eos/layer-stack/
├── .storage-writer.lock
├── manifest.json                                                   legacy v1 sole public authority
├── format-v2.json
├── objects/
│   ├── loose/<prefix>/<ObjectId>.obj
│   └── locators/
│       ├── tables/<TableId>.sst
│       └── CURRENT
├── roots/<prefix>/<RootId>.root
├── refs/
│   ├── heads/<BranchId>.ref
│   ├── checkpoints/<CheckpointId>.ref
│   └── leases/<LeaseId>.ref
├── receipts/<prefix>/<PublicationId>.receipt
├── materializations/<BackendKey>/<RootId>/
│   ├── generations/<Generation>/
│   │   ├── manifest
│   │   └── carriers/
│   └── CURRENT
├── transactions/<TransactionId>/
│   ├── intent
│   ├── ready
│   └── work/
└── quarantine/
```

| Boundary / injected failure | Required durable and public state |
| --- | --- |
| Before | Known legacy head/private branch head/generation; no run transaction or lease; workspace commands still admitted until finalize fence. |
| `intent` | Fsynced transaction intent + transaction/base lease; no new object/root/head; public legacy state unchanged. Crash → fence/abort/release. |
| Objects durable | Verified immutable objects/locators may remain; no root/head visibility. Crash → reuse safe objects, clean transaction work. |
| Root durable | Immutable graph/root may exist but branch head remains old. Crash → request reconciliation may resume; no public/candidate head guess. |
| `ready` | Expected head/root/fence and verified outputs are durable; head still old until ref CAS. Stale/overlap → typed conflict, work cleanup, leases release. |
| Committed visibility | The branch ref atomically names the new root/generation/transaction after directory `fsync`. Response loss/restart → exact committed receipt. |
| After commit before receipt | The valid branch ref wins; recovery recreates the receipt idempotently and never rolls the head back. |
| Lease failpoints/restart | Lease ref generation chooses the valid token; a stale owner/fence cannot renew/release another lease; no deletion follows. |
| Success | Private materialization/tree equals expected candidate merge; public legacy response/head/layer remains authoritative; request retry exact. |
| Cleanup | No nonterminal transaction/work/transaction lease/frozen capture; committed roots/objects/receipt and active declared leases remain; tracked sessions/config restored. |

The Rust test injects every transaction `intent`/`ready` fsync, object/locator,
root, head-ref temp/rename/directory-fsync, receipt, lease
acquire/renew/release, cancellation, and restart boundary. The packaged cases
inject one pre-linearization and one post-linearization/lost-response boundary,
plus lease restart.

## 4. Typed E2E case catalog

The Stage 07 `run-now-*` rows use the pinned Ubuntu 24.04 diagnostic image
only. The `planned-final` row is not run or qualified here: Stage 11 owns the
full Prep 04 Phase-1 host/image matrix, including pinned Ubuntu/Debian glibc,
Alpine musl, minimal/distroless, shell-less, read-only, and non-root fixtures.

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `phase1.stage07.publication.occ-recovery` | POC; `run-now-focused` | legacy public plus `candidate_publish_private` | frozen base, two sessions, stable request IDs, disjoint/conflicting edits, commit failpoints | concurrent public finalize/publish and retry after restart | legacy public authority, exact private receipt, OCC correctness, `O(C log N)` indexed work plus bounded result output, atomic boundaries, mismatch zero | diagnostic capture/chunk/OCC/commit/recovery phases plus `C,N`, page-probe/comparison, touched-node and result-record/byte counters | complete capture/transaction-work/root/object allocation | transactions/workers/queues/permits/capture handles quiesce | scalar vectors and no target helper | `180000` ms | routes, receipts, OCC work/output counters, boundary trees, resources |
| `phase1.stage07.publication.lease-restart` | POC; `run-now-focused` | durable root, carrier, transaction leases | logical test clock plus packaged held strict session and candidate transaction | public strict session/publish, controlled restart, cleanup | valid lease protects, stale fence rejected, recovered transaction releases, no deletion, legacy public unaffected | diagnostic acquire/renew/recover/release phases | lease-ref/transaction residue | lease, guard, registry return to declared set | clock excluded from identity; helper-independent pinned Ubuntu 24.04 proof | `120000` ms | lease/recovery JSON |
| `phase1.stage07.publication.tiny` | POC; `run-now-tiny-bench` | legacy control versus private candidate | deterministic corpus, alternating requests, one daemon | benchmark lab publish, retry, conflict, cancel | exact roots/tree/receipt/authority and mismatch zero | two warmups and six raw pairs | complete envelope and bounded capture peak | twelve cycles with logical release | graph snapshots | `60000` ms | raw and summary JSON |
| `layerstack.phase1.retention-gc.retain-leased-root` | later; `deferred-to-stage_08` | retention and GC with held leases | Stage 08 retention policy, epochs, leases, cursors | publish, read, acquire/release lease, request bounded maintenance | every selected or leased root reconstructs and only unreachable unleased state reaches deletion | diagnostic maintenance phases | live/staging/trash allocation | GC owners and leases quiesce | same store and pinned public API evidence | `60000` ms | Stage 08 typed qualification bundle |
| `phase1.final.publication.qualification` | final; `planned-final` | candidate publication full matrix | frozen release/scale/corpus, required runners, and the full Prep 04 Phase-1 image matrix | Stage 11 full qualification | all atomicity, OCC, recovery, authority, performance, space, memory, required-runner, and portability gates | normative matched metrics | complete amplification envelope | full memory, history, soak matrix | pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root rows; every required row evidenced | `300000` ms per matched invocation | Stage 11 qualification bundle |

Complete declaration metadata:

| Stable ID | Title | Description | Features | Validations | Validation features | Execution surface | Owner ID | Timeout (ms) | Pytest markers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `phase1.stage07.publication.occ-recovery` | `Stage 07 candidate-private publication OCC and recovery` | `Drives disjoint and conflicting candidate-validation transactions from public legacy publishes and proves atomic head visibility, idempotent lost-response retry, and transaction/ref recovery.` | `("storage.publication_v2","storage.occ","storage.recovery","migration.candidate_publish_private")` | `{"legacy-public-authority":"Every public publication and read remains legacy-authoritative during Stage 07.","frozen-capture":"Each candidate transaction consumes one immutable captured base and edit set.","disjoint-committed":"Disjoint concurrent edits commit as the exact merged candidate root.","conflict-no-loss":"Conflicting stale edits fail with typed conflict and lose no committed update.","precommit-old-head":"Every failure before the candidate commit boundary leaves the prior head visible.","postcommit-exact-retry":"A lost response after commit returns the identical receipt and root on retry.","private-tree-equal":"The committed private candidate tree and metadata equal the oracle.","zero-mismatch":"Candidate comparison records no silent or counted mismatch.","cleanup-complete":"Transactions, workers, queues, permits, capture handles, transaction work, and file descriptors quiesce."}` | `{"legacy-public-authority":("migration.candidate_publish_private","storage.publication_v2"),"frozen-capture":("storage.publication_v2","storage.occ"),"disjoint-committed":("storage.publication_v2","storage.occ"),"conflict-no-loss":("storage.occ","storage.recovery"),"precommit-old-head":("storage.publication_v2","storage.recovery"),"postcommit-exact-retry":("storage.publication_v2","storage.recovery"),"private-tree-equal":("storage.publication_v2","migration.candidate_publish_private"),"zero-mismatch":("migration.candidate_publish_private",),"cleanup-complete":("storage.publication_v2","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `180000` | `("medium","phase1","config")` |
| `phase1.stage07.publication.lease-restart` | `Stage 07 durable lease fencing and restart` | `Holds root, carrier, and transaction leases across a controlled restart and proves authoritative generation fencing, safe release, and zero deletion.` | `("storage.leases","storage.recovery","storage.candidate_activation")` | `{"lease-durable":"A valid lease survives restart with its exact owner, target, generation, and expiry semantics.","stale-fence-rejected":"A stale generation cannot renew or release a newer lease.","active-carrier-protected":"The held strict session carrier remains selectable and readable throughout recovery.","transaction-lease-recovered":"Recovery resolves the in-flight transaction and releases its lease exactly once.","no-data-deleted":"Stage 07 performs no object, root, carrier, or publication deletion.","logical-release":"Lease registry, carrier guard, transaction, worker, and session owners return to the declared settled set."}` | `{"lease-durable":("storage.leases","storage.recovery"),"stale-fence-rejected":("storage.leases","storage.recovery"),"active-carrier-protected":("storage.leases","storage.candidate_activation"),"transaction-lease-recovered":("storage.leases","storage.recovery"),"no-data-deleted":("storage.leases","storage.publication_v2"),"logical-release":("storage.leases","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `120000` | `("medium","phase1","config")` |
| `phase1.stage07.publication.tiny` | `Stage 07 publication tiny sentinel` | `Alternates legacy and candidate-private publication over the frozen tiny corpus and records identity, receipt, OCC, time, physical space, and memory.` | `("benchmark.publication","observability.resource_efficiency","migration.candidate_publish_private")` | `{"paired-visible-tree-equal":"Every control and candidate-private pair produces the same visible legacy tree and exact private candidate tree.","receipt-idempotent":"Every retried request ID returns the identical candidate receipt and root.","all-ops-under-60s":"Every publish, retry, conflict, cancellation, and cleanup operation finishes within sixty seconds.","publication-peak-bounded":"Capture, transaction work, root, object, and carrier peak allocation satisfies the declared diagnostic bound.","logical-release":"Transactions, workers, queues, permits, capture handles, and file descriptors return to settled values.","memory-cap":"Physical memory remains within the declared diagnostic cap or is explicitly unavailable.","artifact-complete":"Raw pairs, receipts, OCC history, time, disk, memory, environment, and cleanup evidence validate."}` | `{"paired-visible-tree-equal":("benchmark.publication","migration.candidate_publish_private"),"receipt-idempotent":("benchmark.publication","storage.publication_v2"),"all-ops-under-60s":("benchmark.publication",),"publication-peak-bounded":("benchmark.publication","observability.resource_efficiency"),"logical-release":("storage.publication_v2","observability.resource_efficiency"),"memory-cap":("benchmark.publication","observability.resource_efficiency"),"artifact-complete":("benchmark.publication","observability.resource_efficiency")}` | `"cli"` | `"phase1-storage"` | `60000` | `("smoke","benchmark","phase1","config")` |
| `layerstack.phase1.retention-gc.retain-leased-root` | `Retention and GC preserve every selected or leased root` | `Publishes a deterministic candidate-shadow root graph, closes durable retention epochs, and proves that only unreachable unleased state passes trash, grace, and final recheck while legacy remains authoritative.` | `("workspace-session","layerstack","phase1-cas","retention","garbage-collection")` | `{"terminal":"All selected, pinned, leased, frontier, and in-flight roots reconstruct exactly; unreachable unleased state is deleted only after a complete durable grace epoch; cleanup and authority invariants hold."}` | `{"terminal":("layerstack","retention","resource-efficiency","observability")}` | `"cli"` | `"layerstack-phase1"` | `60000` | `("medium","config","phase1")` |
| `phase1.final.publication.qualification` | `Final durable publication qualification` | `Executes the frozen Stage 11 correctness, atomicity, OCC, recovery, authority, performance, space, memory, soak, rollback, required host/release-runner, and full Prep 04 Phase-1 image matrix.` | `("phase1.qualification","storage.publication_v2","storage.occ","storage.recovery","portability","linux-image-matrix")` | `{"terminal":"All final publication and required-runner gates pass with pinned evidence for Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root rows; no unverified required row remains."}` | `{"terminal":("phase1.qualification","storage.publication_v2","storage.occ","storage.recovery","observability.resource_efficiency","portability","linux-image-matrix")}` | `"cli"` | `"phase1-storage"` | `300000` | `("release","phase1","config")` |

Every declared checkpoint emits exactly one terminal `ValidationReporter`
record.

## 5. Correctness and failure matrix

| Scenario | Disposition | Required proof |
| --- | --- | --- |
| Empty/no-op, 8/16/32 KiB boundaries, arbitrary streaming splits | core/property + tiny now | deterministic root/object/chunk identity and exact retry |
| 1 KiB insert/delete/replace/rename in 1 MiB, 1 MiB no-dedup binary | tiny now | bytes scanned/new retained and exact tree |
| 100–1,000 metadata-rich small files | tiny/focused now | modes/symlink/whiteout/opaque/sparse canonical result, bounded queue |
| Repeated writes before one durable publication | now | may coalesce before linearization into one root |
| Repeated durable publications | now | each committed request remains distinct immutable root/receipt |
| Duplicate same request/same intent; same request/different intent | focused now | exact receipt; typed reuse error |
| Concurrent disjoint, overlapping conflict, stale expected generation | focused now | disjoint rebase; conflict/no lost update; generation CAS; OCC/root diff `O(C log N)` plus bounded result output, with no full-root/full-index scan |
| Failure/crash before/after every transaction/object/locator/root/head/receipt boundary | all Rust now; representative packaged | deterministic `intent`/`ready`/ref state table in §3 |
| Cancellation/timeout/disk full/panic | Rust now; cancellation tiny; packaged representative | commit token fenced; precommit abort/postcommit settling |
| Corrupt/missing/truncated/mismatched object/root/transaction/ref | Rust exhaustive; packaged ref/object representative if safe | typed fail closed/quarantine; public legacy unchanged |
| Root/carrier/transaction lease acquire/renew/release/restart/stale fence | focused now | no stale mutation/deletion; exact active set |
| Strict activation of committed private root | focused comparison now | fallback 0, exact candidate tree; not public head |
| Retention/pack/GC/compaction and held lease | deferred-to-stage_08 | no deletion now |
| Squash identity/remount/lease exchange | deferred-to-stage_09 | absent |
| Candidate public authority/mixed migration/default rollback | deferred-to-stage_10 | private only |
| Full required release/host and Prep 04 Phase-1 image matrix—pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless, shell-less, read-only, and non-root—plus scale/history/soak | planned-final | Stage 11 |

Success must show both authorities: the public legacy result and the distinct private branch ref/receipt. A legacy success without `commit_linearized`, request/branch/root/generation, OCC, and recovery evidence is not a Stage 07 pass.

## 6. Tiny correctness and benchmark loop

`candidate-publication-tiny.yml` uses seed `0x5A07`, pinned Ubuntu 24.04 OCI index/platform digest, same host/filesystem/cache/daemon/config except the candidate-private flag, and alternating control/candidate order. Corpus: empty/no-op; localized 1 KiB edit in deterministic 1 MiB; 1 MiB incompressible; 256 small metadata-rich files totaling ~1 MiB; history depths 1, 8, 32.

Run two warmup pairs and six measured pairs. Each candidate cycle uses a unique stable request, immediately retries it, and materializes/compares the committed private root. Fixed cycles include one disjoint two-writer pair, one conflicting writer, and one pre-commit cancellation. Preserve raw per-sample JSON and ratios; six samples do not support normative p95.

Hard caps: loop ≤60 s; every operation ≤60 s; identity/receipt/OCC/authority exact; first import `O(R+E)`; later publication `O(U+K+C+V_delta)+O(C log C)`; OCC/root diff `O(C log N)` plus bounded result output with `C,N,V_delta`, index-page probes/comparisons, result records, and result bytes recorded; no unchanged-tree scan/rewrite; SeqCDC chunk range exact; publication peak ≤`C_capture+5%`; ring 32 KiB; ≤4 borrowed chunks/workers; queue 16/64 KiB; external merge 8×64 KiB; encoder 256 KiB; cache 16 MiB; semaphore 64 MiB; managed ≤4 MiB/op excluding cache; RSS ≤384 MiB and idle +128 MiB; settled transaction-recovery bound `≤1 MiB+min(1% retained payload,64 MiB)`. Report small-edit `baseline+15%+5 ms` and disjoint throughput ≥90% as diagnostic POC lines; normative p95/sample corpus remains Stage 11.

## 7. Memory-stability and reclamation test

Stage 07 adds chunk/object/transaction encoders, external merge readers, queues, tasks/workers, permits, transaction/lease registries, frozen capture handles, and recovery ownership. Use one long-lived daemon with no restart between tiny measured iterations; restart evidence is a separate case.

Run 12 post-warmup candidate lifecycles: successful commits/retries, one disjoint pair, one conflict, one cancellation. Sample every 100 ms through a fixed ring and streamed JSONL:

```text
idle -> warmed idle -> capture/chunk/OCC/commit peak
-> receipt/materialize -> cleanup/quiescence -> settled -> repeated steady state
```

Quiescence poll ≤5 s requires no nonterminal txn, worker/task/queue/merge reader/borrowed view/permit/frozen capture/transaction lease/extra FD or transaction work; terminal receipts and explicitly active root/carrier leases are bounded durable state; cache is within cap. Freeze control noise before candidate as `max(8 MiB,4×control MAD)`.

Pass requires `bounded-and-released` ephemeral ownership and `bounded-retained-by-design` only for cache/terminal durable records; both RSS ceilings and no unexplained positive settled slope/delta beyond band. Attribute anonymous/file RSS/page cache. No restart, purge, `malloc_trim`, or allocator substitution can make it pass. Missing stage-gating data, suspected/confirmed leak, or growing live gauges blocks. Full size/history and sustained publication/lease churn belong to Stage 11.

## 8. Dependency and portability proof

Capture locked/all-feature Cargo metadata before/after and require identical external `(name,version,source,checksum)`, enabled feature set, and product-wide direct external edge multiset. Require zero additive manifest/lock/Python package/system-tool/runtime-service/target-helper delta; SQLite, sidecars, FUSE, reflink, shell, tar/cp, and target package manager are forbidden. List only internal core/adapter/orchestration edges and run cycle/forbidden-edge checks.

Run the scalar SeqCDC/root/object/publication golden corpus once; acceleration
is absent, so no scalar/accelerated differential applies. Run the Stage 07
diagnostic packaged publish/edit through the pinned Ubuntu OCI index
`sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`
using public file APIs and prove storage work invokes no target helper.
Read-only and non-root runtime variants use that same target identity.
Fixed-width transaction/ref/lease
goldens must be host-native-path independent. Current host/CPU proof qualifies
only its row; Stage 11 executes every required arm64/amd64
host/release-runner row using the same OCI index and records the resolved
platform manifest. Stage 11 separately runs the full Prep 04 Phase-1 image
matrix—pinned Ubuntu/Debian glibc, Alpine musl, minimal/distroless,
shell-less, read-only, and non-root—and leaves every unavailable required row
`unverified`, which blocks qualification and retirement.

## 9. Focused and final-stage commands

Follow the E2E skill’s append-only `e2e/test-report.md` discipline. First packaged gate rebuilds; reuse only after a passing unchanged build.

### Product formatting, lint, and focused unit/integration

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack -p sandbox-runtime --all-targets --all-features -- -D warnings
cargo test -p sandbox-runtime-layerstack-core publication -- --nocapture
cargo test -p sandbox-runtime-layerstack publication_occ -- --nocapture
cargo test -p sandbox-runtime-layerstack publication_recovery -- --nocapture
cargo test -p sandbox-runtime candidate_private_publish -- --nocapture
```

### Exact zero-external-dependency comparison

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo metadata --locked --all-features --format-version 1 \
  > /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/tmp/<run_id>/metadata-after.json

cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.venv/bin/python e2e/tools/verify_external_dependency_delta.py \
  --baseline .e2e-state/baselines/layerstack-phase1/<invocation_id> \
  --candidate .e2e-state/tmp/<run_id>/metadata-after.json \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --require-stdlib-crate sandbox-runtime-layerstack-core \
  --require-exact-external-delta-zero
```

### Focused E2E

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 E2E_REBUILD_BINARY=1 PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_candidate_private_publication.py::test_occ_idempotency_recovery \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox

E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 E2E_REBUILD_BINARY=0 PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_candidate_private_publication.py::test_durable_lease_restart_fencing \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

### Tiny benchmark validate/run

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin \
  --plan candidate-publication-tiny
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin \
  --plan candidate-publication-tiny
# Recover validates all owned transaction directories; its current CLI intentionally has no --plan.
../.benchmark-state/test-venv/bin/sandbox-benchmark recover \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

The new nodes/preset are stage deliverables. The CLI writes run-owned output beneath `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.benchmark-state/{runs,results}/<run-id>/`; it has no `--output` option. Current CLI options, workdirs, rebuild/reuse semantics, and existing package names (except stage-created core) are verified. Record build-lock waiting separately from execution wall time.

### Artifact compatibility validation

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.benchmark-state/test-venv/bin/python -m pytest \
  benchmark/backend/tests/compatibility/test_artifacts.py
```

### DO NOT RUN in Stage 07 — Stage 11 affected regression

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

### DO NOT RUN in Stage 07 — Stage 11 host/image matrix (Ubuntu row shown)

Stage 11 runs the matrix driver once per applicable required host and pinned
fixture: Ubuntu/Debian glibc, Alpine musl, minimal/distroless, and shell-less,
including read-only and non-root cases. The command below shows only the
pinned Ubuntu row; running it in Stage 07 does not qualify any matrix row.

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

### DO NOT RUN in Stage 07 — Stage 11 full Phase 1 qualification

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

| Field | Definition / scope/source | Sampling / aggregation | Baseline | Target / hard ceiling | Missing policy / artifact |
| --- | --- | --- | --- | --- | --- |
| `public_write_authority` / `candidate_branch` | route and separate namespace | structured result every publish | legacy control | public=`legacy_v1`; private branch non-public | blocker; routes JSONL |
| `publication_id`, `root_id`, `publication_generation`, `receipt_equal` | idempotency tuple/result | first attempt + retry | candidate first result | exact equality | blocker; receipts |
| `commit_linearized` | branch ref replacement and parent-directory `fsync` | result + ref snapshot | old head | one point only | blocker |
| `occ_outcome`, `lost_updates` | direct/rebase/conflict and tree verification | every concurrent pair | serialized control | expected class; lost 0 | blocker |
| `C`, `V_delta`, `N`, `occ_index_page_probes`, `occ_comparisons`, `occ_result_records`, `occ_result_bytes` | incremental graph and OCC/root-diff indexed work | every direct/rebase/conflict attempt | frozen fixture sizes | publication `O(U+K+C+V_delta)` plus changed-event ordering; OCC `O(C log N)`; no unchanged-tree/full-index scan | blocker; raw OCC work JSON |
| `publication_component_ns` | capture/chunk/hash/object/OCC/root/commit/settle | monotonic raw timers | paired legacy | each <60 s; diagnostics §6 | blocker |
| `bytes_scanned/hashed/reused/newly_retained` | transaction counters, bytes | each sample; totals/ratios | same corpus | exact reconciliation | blocker |
| `allocated_bytes.<category>` | full allocated filesystem blocks | before/peak/settled | paired control | peak `C_capture+≤5%`; full envelope | unknown blocks disk verdict |
| `live_owned_bytes/workers/queues/permits/readers/txns/leases/fds` | product gauges | 100 ms bounded ring + peaks/windows | warmed idle | exact caps; ephemeral zero at quiescence | blocker |
| `rss_total/anon/file`, `cgroup_current/peak` | daemon/cgroup scopes | 100 ms, peak/window/slope | equal warmup | ≤384 MiB; idle +128 MiB | required missing blocks |
| `quiescence_ms`, `settled_slope` | product poll / Theil–Sen | every cycle, n=12 | frozen control band | ≤5 s; not above band | blocker |
| `transaction_recovery_bytes`, `pending_transactions` | transaction/recovery residue | settled snapshot | none | bound in §6; pending 0 | blocker |
| `external_graph_delta` | canonical packages/features/direct edges | once | Stage 06 | empty | blocker; dependency JSON |

Every metric records units, numerator/denominator, source scope, and `measured|derived|estimated|unknown`. High-frequency raw samples stream to bounded artifacts; in-process state retains fixed windows only. Never combine daemon, cgroup, kernel/filesystem, and runner scopes unlabeled.

## 11. Stage exit verdict

Mandatory pass: three run-now cases; focused formatting/lint/unit/property/transaction/recovery tests; artifact/schema validation; exact external graph equality; current-host scalar/no-helper portability; and cleanup. Atomicity, authority separation, idempotency, OCC, transaction/ref recovery, lease fencing, private exact comparison, logical release, physical caps, and publication peak are hard gates.

Allow only attributed allocator/page-cache retention inside the frozen band or explicitly unavailable optional split counters. Disqualifiers include candidate mutation of public head/response, competing authority, mutable capture, duplicate/different retry error, lost update, treating `intent` or `ready` alone as commit, stale lease mutation, any deletion, partial visibility, mismatch, operation ≥60 s, resource/space cap breach, suspected/confirmed leak, missing gate data, dependency/runtime/helper delta, or incomplete artifacts/cleanup.

Cleanup is run-ID/request/branch scoped: restore config/gateway, destroy tracked sessions, recover/terminalize transactions, release test leases, remove only transaction-owned work, and preserve committed immutable candidate roots/objects/receipts plus all legacy state. Rebuild after product changes; otherwise rerun only the failed focused case after diagnosis. Disable the private trigger on failure. Stage 08 still owns retention/packs/GC, Stage 09 squash/remount, Stage 10 public candidate authority, and Stage 11 normative regression/performance/space/memory/portability/soak/rollback qualification.
