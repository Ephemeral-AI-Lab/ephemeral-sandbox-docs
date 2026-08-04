# Architecture verification matrix

**Status:** proof plan; executable V2 evidence is `NOT_RUN` unless linked below  
**Purpose:** trace every selected R0 claim to its implementation owner, proof
phase and reopening rule

## Evidence policy

- A design mechanism is not executable proof.
- `SOURCE-VERIFIED` e497 placement evidence proves current ownership/source
  availability, not future V2 correctness.
- Phase 02/03 algorithm descriptions remain `INFERRED` until their owning tests
  pass on a sealed implementation source.
- Historical Stage 4.6 is `INCOMPARABLE` and cannot pass/fail a V2 performance
  row.
- A later phase may strengthen proof but cannot waive a hard rule.
- Every result must identify source path, branch, HEAD, dirty state, command,
  fixture/artifact identity and raw evidence location where applicable.

Result labels in this file are `PLANNED`, `PASS`, `FAIL`, `BLOCKED`, or
`NOT_APPLICABLE` with a proof. No unchecked box implies success.

## Product hard rules 1–10

| Rule | Selected mechanism | Implementation owner | Required evidence | Current result | Failure action |
|---:|---|---|---|---|---|
| 1. Complete immutable Version | One Accepted Version at an occupied `VersionId` has one complete immutable payload closure; no parent/depth/layer reconstruction | Phase 02 identity + Phase 03 store | Phase 02 complete fact/golden-vector proof; Phase 03 read/restart/source audit; Phase 06 integration | `PLANNED` | Fix within R0 or reopen if complete identity/storage needs another family. |
| 2. Equal canonical Version → one payload | Admission converges exact-equal canonical bytes to one physical accepted closure | Phase 03 | Sequential/concurrent equal admission, restart and physical-count tests | `PLANNED` | Stop Phase 03; no duplicate-payload waiver. |
| 3. Accepted-reference payload I/O is zero | The single reference authority exposes exact Head create/replace/remove and fixed-Root create/remove; none can open/copy payload and no generic Root retarget exists | Phase 03; Phase 06 qualifies | Byte counters plus syscall/fixture evidence for all five operations across success, stale/absent/already-present, error, retry, `OUTCOME_UNKNOWN` read-back, and cleanup paths | `PLANNED` | Fix interface/implementation; reopen if storage family cannot satisfy it. |
| 4. Digest is not proof | Every occupied ID triggers full canonical-byte comparison; mismatch is typed collision before reference mutation | Phase 02 comparison seam + Phase 03 all-ingress enforcement | Forced-ID unequal/equal cases, concurrency, restart and source audit | `PLANNED` | Block publication; never weaken to digest-only lookup. |
| 5. One OCC head transition | Store rereads expected `(AcceptedBinding, HeadRevision)` under one transition gate; one atomic complete record replacement; stale has no merge/rebase | Phase 03 | Concurrent history tests and crash faults around the sole linearization point | `PLANNED` | Stop Phase 03; reopen if another authority is required. |
| 6. Accepted Version never edited | Writable Candidates/Workspaces stay at effect owners; accepted closures are immutable/read-only custody | Phases 03–04 | Mutation attempts, concurrent read/head move, product file-write/edit routing and source audit | `PLANNED` | Block wiring/cutover; direct Accepted-Version mutation is architecture-invalid. |
| 7. MCTS remains outside storage | LayerStack-0 exposes Version/reference primitives only; application owns search/rollout policy | Phases 03–04 | API/dependency/source audit and operation tests | `PLANNED` | Remove policy dependency or reopen ownership selection. |
| 8. Runtime-private facts stay private | Identity accepts only portable facts; forbids Docker/OCI/OverlayFS/mount/namespace/host paths | Phase 02 | Forbidden-field/type/dependency audit, golden vectors and rejection cases | `PLANNED` | Stop Phase 02 and reopen if complete identity requires runtime facts. |
| 9. No dual writable truth | Monotone generation fence; legacy read-only before V2 authoritative import/enablement; no dual-write rollback | Phases 05–08 | Complete writer inventory, fence-bypass/crash tests, rehearsal, live records, post-clean source audit | `PLANNED` | Stop migration/cutover; reopen if dual writes are required. |
| 10. Prefer R0 | Rewrite current LayerStack owner; zero new architectural boundaries by default | Phases 02–04 | Cargo/dependency/source graph and review of every addition against an exact R0 failure | `PLANNED` | Reject unnecessary boundary or reopen joint selection with necessity evidence. |

Any `FAIL`, or any architecture-changing `BLOCKED`, means the affected phase
cannot pass. Correctness and implementability precede performance.

## Phase 02 — identity proof

Cross-reference: Phase 02 [PRD](../phases/02-state-identity/PRD.md),
[PLAN](../phases/02-state-identity/PLAN.md), and
[test/perf](../phases/02-state-identity/test-perf.md).

| Claim | Required proof | Evidence location | Result |
|---|---|---|---|
| Complete portable fact set and explicit rejection set | Review plus fixtures covering every supported entry/fact and forbidden runtime-private field | To be recorded by Phase 02 | `PLANNED` |
| Deterministic versioned canonical bytes | Stable golden vectors, order permutation, encode/decode/compare tests | To be recorded | `PLANNED` |
| Typed `VersionId` and domain separation | Exact algorithm/width/domain decision plus cross-run vectors | To be recorded | `PLANNED` |
| Digest collision cannot alias | Forced collision yields exact equal or typed mismatch | To be recorded | `PLANNED` |
| Bounded validation/canonicalization | Boundary and over-limit cases; measured memory/scratch/FD behavior where required | To be recorded | `PLANNED` |
| Pure module/source placement | No store I/O, mounts, workspace, manager/provider/observability dependency or runtime brand | To be recorded | `PLANNED` |

Phase 02 reopens Phase 01 if complete bounded portable identity requires
runtime-private facts, layer reconstruction, another owner/storage family, or
cannot support exact occupied-ID comparison.

## Phase 03 — store proof

Cross-reference: Phase 03 [PRD](../phases/03-state-store/PRD.md),
[PLAN](../phases/03-state-store/PLAN.md), and
[test/perf](../phases/03-state-store/test-perf.md).

| Claim | Required proof | Evidence location | Result |
|---|---|---|---|
| Payload admission is immutable and idempotent | New/equal/concurrent admission, attempted mutation and restart tests | To be recorded by Phase 03 | `PLANNED` |
| Full occupied-ID comparison at every ingress | Candidate publish/import/direct admission source audit and forced collision tests | To be recorded | `PLANNED` |
| Payload precedes every durable reference | Faults at every stage/admission/root/head synchronization cut | To be recorded | `PLANNED` |
| One OCC transition; stale is clean | Concurrent expected-revision histories and no merge/rebase/source audit | To be recorded | `PLANNED` |
| Reference-only operations perform zero payload I/O | Per-operation counters plus independent syscall/fixture evidence on success/error/retry | To be recorded | `PLANNED` |
| Captured reads survive head moves | Reader/head and reader/retirement races; immutable handle tests | To be recorded | `PLANNED` |
| Recovery returns prior/new truth or fails closed | Supported-filesystem crash-prefix, corrupt, dangling, unknown-version and excessive-debt tests | To be recorded | `PLANNED` |
| Retirement closes last-root/custody race | Root/custody concurrency and bounded exact revalidation tests | To be recorded | `PLANNED` |
| All resource populations are finite | Boundary, ENOSPC, cancellation, restart and cleanup-plateau tests | To be recorded | `PLANNED` |
| Legacy truth is absent/hard-failed in V2 path | Source and runtime negative tests for parent/depth/squash/merge/whiteout fallback | To be recorded | `PLANNED` |

Phase 03 reopens Phase 01 if a supported filesystem cannot prove required
durability, exact comparison/zero-payload moves cannot be implemented, or
bounded retirement/recovery requires another owner, storage family or service.

## Phase 04 — product wiring proof

| Claim | Required proof | Evidence location | Result |
|---|---|---|---|
| Existing app owners retain auth/order/orchestration | Dependency/source audit and operation histories | To be recorded by Phase 04 | `PLANNED` |
| Live file writes/edits target Workspace only | Session/live routing tests and Accepted-Version mutation negatives | To be recorded | `PLANNED` |
| Committed reads resolve a captured Accepted Version | Sessionless/session read matrix and concurrent publish behavior | To be recorded | `PLANNED` |
| Workspace/overlay/namespace/exec remain effects | Dependency and forbidden-field audit | To be recorded | `PLANNED` |
| Observability is diagnostic-only | Read-only API/source audit and corruption/absence behavior | To be recorded | `PLANNED` |
| Open DECs remain isolated | Tests for implemented alternatives plus owner decision references; no silent closure | To be recorded | `PLANNED` |
| Autosquash/silent merge/depth policy leaves V2 path | Source and operation-negative audit | To be recorded | `PLANNED` |

Phase 04 cannot make a product-owner decision merely to finish wiring.

## Phase 05 — migration and fence proof

| Claim | Required proof | Evidence location | Result |
|---|---|---|---|
| Legacy mapping is total for declared in-scope roots | Deterministic mapping inventory and fixture comparison | To be recorded by Phase 05 | `PLANNED` |
| Import uses ordinary V2 admission/reference paths | Dependency/source audit, collision and physical-count tests | To be recorded | `PLANNED` |
| Progress and retry are restart-safe | Fault at every import/progress durability cut | To be recorded | `PLANNED` |
| Every writer is generation-fenced | Complete writer inventory, wrong/stale generation and bypass tests | To be recorded | `PLANNED` |
| Exactly one writable truth | Mode-transition histories and rehearsal | To be recorded | `PLANNED` |
| Temporary implementation is deletable | Named deletion manifest and permanent-code dependency audit | To be recorded | `PLANNED` |

Any incomplete writer inventory, silent partial import, fence bypass, dual-write
requirement, or permanent legacy dependency blocks Phase 05.

## Phase 06 — exact artifact qualification

| Claim | Required proof | Evidence location | Result |
|---|---|---|---|
| Phase 02–05 Must suites pass together | Frozen source/binary/config/fixture identity and raw results | To be recorded by Phase 06 | `PLANNED` |
| Crash/collision/OCC/resource laws hold end to end | Fault/load/recovery results on the same artifact | To be recorded | `PLANNED` |
| Reference-only zero-payload counters are credible | Cross-check instrumentation with independent syscall/fixture evidence | To be recorded | `PLANNED` |
| Rehearsal completes one-writer fence/import/cutover sequence | Rehearsal receipts and cleanup state | To be recorded | `PLANNED` |
| Performance is reported honestly | Matched protocol/provenance, raw samples and no Stage 4.6 winner claim | To be recorded | `PLANNED` |

Phase 06 qualifies one exact artifact. Changes after qualification require
proportional requalification and cannot inherit an old pass automatically.

## Phase 07 — live cutover and observation

| Claim | Required proof | Evidence location | Result |
|---|---|---|---|
| Exact qualified artifact/config deployed | Artifact identity and deployment receipt | To be recorded by Phase 07 | `PLANNED` |
| All writers fenced and legacy read-only | Live writer inventory, rejection checks and generation evidence | To be recorded | `PLANNED` |
| V2 is sole writable truth | Live readiness/write/read checks and incident ledger | To be recorded | `PLANNED` |
| Owner-selected observation completed | Explicit `DEC-011` decision plus observation log | To be recorded | `PLANNED` |
| No Must-class incident remains open | Incident and rollback/quarantine record | To be recorded | `PLANNED` |

This matrix does not authorize Phase 07. Live execution requires the separate
approval and prerequisites defined by that phase.

## Phase 08 — clean release proof

| Claim | Required proof | Evidence location | Result |
|---|---|---|---|
| Temporary migration code is absent | Deletion-manifest/source/dependency checks | To be recorded by Phase 08 | `PLANNED` |
| Permanent V2 code has no legacy import dependency | Build plus source/dependency audit | To be recorded | `PLANNED` |
| Clean artifact re-passes required proof | New artifact identity and rerun results | To be recorded | `PLANNED` |
| Production runs the clean artifact | Deployment/readiness/health receipt | To be recorded | `PLANNED` |
| Legacy data disposition is explicit | Retain-read-only record or separately authorized deletion evidence | To be recorded | `PLANNED` |

Deleting compatibility changes the binary, so the Phase 06 artifact proof
cannot simply be relabeled for the clean build.

## Source/dependency conformance checks

The owning phases must refine and run focused checks for:

- only `sandbox-runtime-layerstack` writes payload/root/head truth;
- identity has no store/effect/lifecycle/observability/runtime-brand dependency;
- store has no app auth/MCTS/workspace/mount/namespace/exec dependency;
- no new crate/service/database/coordinator/helper process without a reopened
  necessity decision;
- no V2 parent/depth/layer/squash/merge/rebase fallback;
- no raw digest accepted as an admitted binding;
- no temporary legacy import reference after Phase 08; and
- no owner DEC recorded as accepted without the owner's explicit decision.

The concrete command and result belong in the owning phase evidence; likely
tools include `cargo metadata`, `rg`, focused package tests, fault injection,
and phase-specific integration runners.

## Architecture reopening matrix

| New evidence | Local correction or reopen? |
|---|---|
| Codec/hash/record spelling or finite limit needs refinement inside fixed contracts | Local owning-phase decision and proof. |
| Safe fence sequence changes inside the same supported filesystem profile and failure model | Phase 03 decision and proof. |
| Need runtime-private facts or layer history in canonical identity | `REOPEN_PHASE_01`. |
| Need another selected-Version owner/writer or reversed dependency | `REOPEN_PHASE_01`. |
| Need database, object DAG/archive truth, service/helper process or persistent refcount authority for correctness | Present exact R0 failure and `REOPEN_PHASE_01`. |
| Cannot prove payload-before-reference, one OCC point, collision comparison, zero-payload moves or bounded recovery | Fix R0; if family/boundary must change, `REOPEN_PHASE_01`. |
| Owner DEC requires direct committed mutation, dual writes, canonical provenance or joint auth/store authority | `REOPEN_PHASE_01`. |
| Performance is disappointing but correctness holds | Do not weaken rules; profile and optimize inside R0, or reopen only with a complete necessary alternative. |

Related: [design index](README.md) · [algorithms](04-algorithms-and-call-flows.md)
· [reliability](05-concurrency-durability-recovery.md) ·
[performance](07-performance-and-optimization.md) ·
[source map](09-source-and-implementation-map.md)
