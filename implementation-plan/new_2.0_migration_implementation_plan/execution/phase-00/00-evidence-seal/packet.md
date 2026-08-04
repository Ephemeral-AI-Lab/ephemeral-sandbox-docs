<!-- packet:plan -->

# Phase 0 gate plan — independent judge and evidence seal

Status: **DRAFT / `NOT_RUN` — PHASE 0 PREPARATION ONLY**

This packet operationalizes the authoritative
[Phase 0 contract](../../../phases/00-independent-judge-and-evidence-seal.md).
It does not replace that contract. It selects no architecture, physical
profile, product algorithm, component, schema, or implementation. Accepted
joint winners remain `0`; selected algorithms remain `0`.

<!-- plan:spec -->

## Identity and authority

| Field | Current value |
|---|---|
| phase / gate | `00 / 00-evidence-seal` (causal gate 1 of 11) |
| immutable lineage | `00-evidence-seal-r0001` |
| packet maturity / producer report / independent disposition | `DRAFT / NOT_RUN / NOT_RUN` |
| producer | current documentation agent; preparation only; result-bearing execution remains unassigned, and its exact authenticated input-lock triple must also sign the final manifest under the distinct result-seal domain |
| independent acceptor | `UNASSIGNED`; must be authenticated and independent from the producer on principal, credential, and control-domain axes |
| capability ceiling | candidate-blind fact, requirement, universe, fixture/oracle, holdout, threshold, comparator, and provenance construction |
| forbidden | candidate evaluation/tuning, holdout disclosure, production dependency/code/schema/API changes, V2 truth, Phase 1 execution, or self-acceptance |
| authorization | the current user request authorizes artifact-system preparation only; no authenticated phase-entry grant is sealed for result-bearing work, and no phase exit authorizes Phase 1 |

The current task authorizes creation of this execution-artifact system and
active packet. It substitutes for neither the authorization receipt nor the
phase-entry attestation required in the input lock before result-bearing work,
and it is not gate acceptance. The attestation must bind this exact catalog,
phase, gate, lineage, receipt digest, authenticated principals, exact
`produce:<gate-id>` and `accept:<gate-id>` capabilities, and validity and
revocation facts. The authenticated execution wrapper must supply an absolute,
write-denied external authority-policy path and the SHA-256 of its exact bytes.
That version-3 policy, never packet claims, binds exact attestation, input-lock,
sealed-manifest, acceptance, and non-bootstrap execution-state bytes to their
bound artifacts, derived uses, pinned verifier build, and trust root. The
sealed-manifest producer triple must equal the input-lock producer exactly, but
the pre-result and post-result proofs cover different bytes and domains.

`manifest.json` will be the sole machine owner of controlled-byte and
predecessor identities. Each later consumer must bind both the exact manifest
and independent acceptance; prose may name the logical relationship but may
not copy a mutable digest.

## Exact consumed inputs

Phase 0 has no predecessor gate. Before sealing, it must content-address all
actual inputs it uses, including:

| Input class | Current preparation identity | Required sealed form |
|---|---|---|
| plan package | docs repository branch `layerstack_2_0`, `HEAD dc9ae450107ec40087ac086950e7b38b2436c9cc`, package untracked amid unrelated owner changes | exact file manifest, Git identity, dirty/untracked declaration, and substantive digest |
| product base | clean reserved worktree `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0`, branch `codex/new-2.0-storage-core`, `HEAD e4974d1f9aac702b35e052629cb070c897989352`, matching local `origin/main` | reverified commit/tree/branch/worktree state plus source/dependency manifests |
| historical Stage 4.6 | [`stage-04-6-baseline.md`](../../../evidence/stage-04-6-baseline.md), classified `R_stage46 = INCOMPARABLE` | independently verified retained receipts; never a matched winner or implementation base |
| requirements/design/gates | owning package documents named by [`traceability.md`](../../../traceability.md) | exact accepted bytes and conflict-free authority map |
| owner authorization | artifact-system and packet preparation only | durable authorization receipt, authenticated phase-entry attestation, and external policy binding before any result-bearing procedure, including read-only evidence collection |

Any identity drift updates this draft before input lock. Drift after input lock
invalidates the run and requires a new lineage.

## Objective, non-goals, and success predicate

Objective: produce one content-addressed, candidate-independent judge/evidence
seal containing actual product facts, finite reproducible topology × physical-
profile closure, requirements and scope decisions, fixtures, independent
oracle, disjoint selection corpus and untouched holdout, comparator rules,
numeric thresholds, resource/fault protocols, and complete provenance.

Non-goals:

- selecting or ranking a topology, method, algorithm, or component;
- adding product code, schema, API, dependency, cache, worker, service, runtime
  seam, or future-runtime compatibility promise;
- running Phase 1 candidate/holdout evaluation;
- claiming a Stage 4.6 speedup or performance guarantee; and
- authorizing Phase 1, Phase 2, release, retirement, or deletion.

Success requires `QG-PROV-001 = PASS`; accepted Phase 0 contracts for
`QG-SEM-001` and the sole `QG-PERF-001`; every other applicable Phase 0 gate
contract sealed; an inaccessible untouched holdout; reproducible candidate
closure; and independent hostile acceptance that the judge encodes no favored
representation. Missing facts produce `BLOCKED`, never an assumption.

## Scope and disposition

The seal is incomplete until it closes the 11 work items and deliverables in
the owning Phase 0 contract, including:

- current manager/runtime and observability operations, HTTP routes, RPC
  controls, proposed/legacy rows, caller/auth/error/replay/revocation behavior;
- durable fields/roots/requests/outcomes, writers/readers, effects, allocations,
  resources, packages/edges, processes/deployables, and authorities;
- all five partitions of baseline `A/S/N`, generated actual-source transforms,
  signed submissions, `R_LEGACY_CONTROL`, R0 eligible to lose, and every
  compatible `T1`–`T8` physical profile;
- exact COW root-transfer/last-reference races and checkpoint-rooted bounded
  fan-out at `1/2/4/16/64/maximum` plus admitted active rollouts;
- normal/edge/corrupt/crash/concurrency/migration/capacity/security/aggregate
  fixtures and independent oracle;
- request-binding/authorization race, deterministic bounded `file_list`, and
  transport-aware total disposition;
- CPU/toolchain/kernel/filesystem/allocator/cgroup/storage/FD/task/queue/cache/
  scratch/cleanup scopes and the complete operation × terminal × applicable
  fault product; and
- disposable Linux/WASI/Firecracker contract falsifiers with `unsupported` as
  a valid result and no production plugin/runtime promise.

Every discovered source, surface, authority, configuration, and evidence class
receives an explicit owning disposition. Unlisted work remains out of scope and
cannot enter the sealed run.

## Work DAG and safe parallelism

| Lane | Produces | May run with | Must follow | Gate-local stop |
|---|---|---|---|---|
| `P0-W1 provenance/source` | Git/tree/dirty, Cargo/dependency/source-reference, build/tool/environment, and historical-evidence manifests | W2–W6 before common input lock | none | any input cannot be content-addressed or reproduced |
| `P0-W2 facts/scope` | total caller, surface, state/field/root, writer/reader, authority, effect, resource, process/deployable, and migration ledgers; closures for `DEC-001/011/017/018` | W1, W3–W6 | verified source anchors from W1 for final seal | an external surface, writer, authority, or durable fact remains unmatched |
| `P0-W3 candidate closure` | control, all five ownership partitions, actual-package deletion/placement/necessity transforms, signed cutoff, `T1`–`T8` product, equivalence/admissibility/dominance generator | W1–W2, W4–W6 | W1 source graph for final generation | open-ended universe, late eligible discovery, or missing realization/`INAPPLICABLE` proof |
| `P0-W4 semantics/oracle` | byte-exact fixtures, independent expected-result generator, total operation map, authorization/replay/MCTS/COW/crash cases | W1–W3, W5–W6 | W2 facts for final coverage | candidate-derived oracle, missing semantic class, or holdout leakage |
| `P0-W5 measurement/resources` | single benchmark/comparator/statistics contract, storage/process attribution, hard resource caps, terminal/fault cleanup matrix | W1–W4, W6 | W2/W4 operation and resource populations | unmatched comparator, unbounded population, or measurement unable to attribute owners |
| `P0-W6 custody/review` | corpus split, holdout ACL/capability proof, input lock, independent review/acceptance protocol, blocker ledger | W1–W5 before locking | all lane outputs before final seal | candidate access to holdout/judge state or producer/acceptor overlap |

Parallelism ends at the common input lock. No lane may observe candidate
results, alter another lane's sealed input, broaden Phase 0 capability, or
self-accept its output.

## Resource and safety envelope

No numeric cap is accepted merely because it appears in a design draft. Phase
0 must seal each cap's population, owner, charge-before-allocation rule,
overload behavior, process-tree attribution, terminal/restart cleanup, and
measurement procedure. Selected-state managed memory, storage qualification
containment, and each untrusted runtime remain distinct scopes. Secrets are
excluded from retained evidence; caches, scratch objects, pins, descriptors,
tasks, and process descendants require bounded ownership and every-terminal
cleanup evidence.

## Evidence protocols

Raw evidence is immutable and content-addressed. Before result-bearing work,
represent every pre-result input—including the exact authorization receipt and
phase-entry attestation—under `evidence/input-lock/snapshots/` as exact bytes or
a canonical immutable receipt naming digest, length, media type, durable
content-addressed location, and an availability-verification command. Generate
the canonical `evidence/input-lock.json` index. The external policy must bind
the exact attestation to its receipt, the exact input lock to the governing
phase-entry attestation, the exact sealed manifest to its input lock, any final
acceptance to its exact manifest, and every non-bootstrap execution state to
exact retained prior-state bytes. Each binding chooses an absolute verifier
locator, exact build digest, trust-root digest, and derived use. Policy and
verifier paths are opened once with no-follow component traversal; on Linux the
same regular, nonwritable, bounded, self-contained static native ELF32/ELF64
descriptor is hashed, strictly parsed, and executed under bounded time/output
and fixed environment. Malformed or out-of-bounds ELF structure, `PT_INTERP`,
and `DT_NEEDED` are rejected. The verifier contract forbids delegation to an
unpinned helper, plugin, interpreter, shared object, or dynamically loaded
code. There is no pathname, interpreter, dynamic-loader, shared-library,
helper, or plugin fallback.
The validator independently derives lookup keys from structurally valid bytes
and accepts only exit `0`, stdout exactly `PASS`, and empty stderr.

The final result manifest covers the input-lock index, its snapshots, and all
results without circular hashing. Protocol or corpus change after result
access creates a new run and new holdout. Before any final verdict, accepted
packets, invalidation events, and referenced evidence also require
authenticated versioned or write-denied custody with independent retention and
audit receipts. A passing local validator cannot prove past immutability,
external policy custody, or append-only history by itself.
For every frontier advance or invalidation, preserve exact prior-state bytes,
sign one general transition, and require the independent provider receipt to
prove the exact conditional/leased state commit before the successor is usable.

## Outputs and handoff

The sole gate output is a content-addressed candidate-independent judge/evidence
seal. Its accepted record must name every source/evidence manifest, generator,
ledger, corpus/holdout contract, oracle, comparator/statistical contract,
resource/fault protocol, decision closure, blocker, and independent acceptor.
It may report `BLOCKED`; it may not report an architecture/method winner.
The handoff region of this `packet.md` owns the next executor's allowed and
forbidden actions. Passing
Phase 0 does not itself authorize Phase 1.

## Invalidation and reopening

Any changed Phase 0 fact, requirement, candidate-set rule, source graph,
fixture, oracle, corpus/holdout, threshold, comparator, statistic,
authorization law, capability separation, or evidence identity invalidates
this seal and every consuming Phase 1/2 record. Preserve the old lineage,
archive it under the execution history contract, append the trigger and exact
transitive closure to `execution/state.json`, preserve the exact prior state and
complete prior packet prefix, and publish the replacement state last through a
genuine conditional write or exclusive lease/fence. The independent one-shot
verifier must prove its signed commit receipt before use. Block downstream
work, reseal Phase 0 as a new lineage, and create a new untouched holdout before
candidate evaluation resumes. Never refresh an accepted digest in place.

<!-- plan:decisions -->

## Consumed decisions

The authoritative ledger is [`decisions/README.md`](../../../decisions/README.md).
This packet neither duplicates nor accepts it. The global ledger contains no
accepted ADR and no accepted algorithm, topology, physical profile, component,
schema, or source-layout decision.

## Local decision ledger

Four Phase 0 decision closures remain open:

| Decision | State | Required Phase 0 evidence | Consequence while open |
|---|---|---|---|
| `DEC-001` exact `file_blame` retention | `OPEN` | pinned caller inventory, compatibility impact, owner decision | target public-operation set cannot seal |
| `DEC-011` observation/compatibility horizon | `OPEN` | longest retry/replay/restore/backup/audit/client-upgrade horizon and operational-risk decision | observation and retirement contracts cannot seal |
| `DEC-017` exact V2 operation/file-target/no-session write/edit behavior | `OPEN` | complete current/legacy/proposed/final transport-aware matrix plus owner approval | semantic oracle and API scope cannot seal |
| `DEC-018` authorization/revocation linearization | `OPEN` | bind/lookup/prepare/dispatch/terminal/response ordering and revoke-at-every-cut fixtures with security-owner approval | security oracle cannot seal |

`DEC-002`–`DEC-010` and `DEC-012`–`DEC-016` remain Phase 1A questions. Phase 0
may seal the finite evidence and judging rules they will consume; it must not
answer them.

| Local ID | State | Question | Alternatives retained | Evidence required | Decision and rationale | Owner |
|---|---|---|---|---|---|---|
| `P0-D001` | `OPEN` | Who has exclusive untouched-holdout/oracle custody and who independently accepts the seal? | principals with authenticated, non-overlapping candidate access and acceptance authority | credential/control-domain evidence, ACL/capability graph, process/filesystem/cache/log separation | `UNDECIDED` | Phase 0 authority owner |
| `P0-D002` | `OPEN` | What exact signed UTC submission cutoff and deterministic candidate-universe generator bytes are used? | any pre-result finite procedure satisfying the owning selection contract | source graph, generator digest, normalized output, completeness/admissibility/dominance receipts | `UNDECIDED` | candidate-closure owner |
| `P0-D003` | `OPEN` | What newly attested incumbent comparator is eligible under the single benchmark contract? | an exact current incumbent satisfying frozen equivalence/provenance, or `BLOCKED` | causal source/build/config/environment closure and matched-run eligibility receipt | `UNDECIDED` | benchmark owner |
| `P0-D004` | `OPEN` | What exact resource caps and containment/attribution procedures are accepted? | finite procedures independently bounding storage-side and untrusted-runtime trees | population proofs, admission/overload rules, process-tree attribution, fault and cleanup evidence | `UNDECIDED` | resource owner |

Allowed states are `OPEN`, `ACCEPTED`, `REJECTED`, `SUPERSEDED`, and
`NOT_APPLICABLE(reason)`. An accepted row names exact evidence and an
independent acceptor. Any execution-changing unresolved row prevents
`INPUT_LOCKED`; result-visible change after lock requires a new lineage.

## Rejected assumptions

| Assumption | Disposition |
|---|---|
| R0 or any `T1`–`T8` profile is the intended winner | rejected; all remain candidates and `NO_WINNER` is valid |
| three phases are a global minimum | rejected; three is the smallest conservative grouping currently justified and the two-envelope challenger remains open |
| Stage 4.6 proves the V2 baseline or a 100× guarantee | rejected; `R_stage46 = INCOMPARABLE` for matched selection |
| 21 audit families are new algorithms | rejected; current produced/proved/selected algorithm counts are all zero |
| a design target is an accepted hard cap or benchmark | rejected; Phase 0 must seal the procedure and independent acceptance |
| a phase exit authorizes its successor | rejected; separate exact capability authorization is mandatory |

## Downstream impact

Any changed accepted Phase 0 decision invalidates the Phase 0 seal and every
transitive Phase 1/2 consumer unless the owning gate accepts a complete-closure
non-impact proof. The obsolete lineage stays archived, its external verifier
binding stays historical-only, and hashes are never silently refreshed.

<!-- plan:end -->

<!-- packet:algorithms -->

# Phase 0 algorithm note

Status: **DRAFT — `0` PRODUCT ALGORITHMS PRODUCED, PROVED, OR SELECTED**

Phase 0 selects no storage algorithm. The 21 global audit families remain
questions, and `T1`–`T8` remain unselected physical-profile families. This
section identifies judge-construction procedures that must be frozen and proved
reproducible; it does not count them as V2 product algorithms or authorize
their implementation.

## Procedure inventory

| Procedure | State | Purpose | Default/simple alternative | Proof still required |
|---|---|---|---|---|
| source/dependency/reference inventory | `UNSELECTED` | derive complete current e497 graph and dispositions | pinned compiler/Cargo metadata plus direct deterministic source scan | exact closure, normalized rows, exclusions, repeatability, and independent reproduction |
| joint candidate-universe generator | `UNSELECTED` | enumerate finite topology × compatible physical-profile cards before results | deterministic finite Cartesian/transform generation with duplicate collapse | complete axes, signed cutoff, equivalence, admissibility, dominance, realizability/`INAPPLICABLE` receipts |
| fixture and expected-result generator | `UNSELECTED` | create representation-neutral semantic/fault cases | independently implemented deterministic oracle over portable facts | independence, full operation/terminal/fault coverage, golden vectors, mutation/falsification evidence |
| corpus partition and holdout custody | `UNSELECTED` | create disjoint selection and one-time untouched holdout | standard cryptographic RNG or deterministic keyed assignment under exclusive custody | seed/key custody, balance, no leakage, immutable assignment, late-discovery reopening |
| content and candidate-identity oracle | `USED_STANDARD` only after seal | identify exact packet/source/evidence/corpus/result bytes and judge candidate-to-accepted `StateId` admission | SHA-256 via standard system/library implementation plus exact canonical-byte comparison on occupied candidates | domain/path normalization, complete path set, independent rehash, no-alias admission, typed collision terminal, bounded cleanup, and qualification-only forced-collision coverage |
| statistical/comparator procedure | `UNSELECTED` | define the sole `QG-PERF-001` decision rule | standard preregistered matched analysis suitable for the measured distribution | hypotheses, power/sample, uncertainty, randomization, stopping/retry/outlier rules, comparator equivalence |
| resource/process attribution | `UNSELECTED` | charge memory/storage/FD/task/cache/scratch/cleanup to complete owners | kernel/cgroup/filesystem counters plus explicit ledger where applicable | descendants, hierarchy/escape, sampling error, shared-byte attribution, crash/restart cleanup |

## Proof obligations for every retained procedure

Before the Phase 0 seal, each procedure must expose exact inputs/outputs,
normalization, deterministic branches, completeness limits, failure behavior,
time/I/O/memory/persistent-space bounds, overflow/capacity handling, immutable
evidence, and an independent reproduction command. A custom implementation
requires a concrete failure of the standard/existing alternative; otherwise
use the simpler established mechanism.

For candidate product methods, Phase 0 freezes only the evidence-card schema
and finite universe. Correctness, complexity, physical resource behavior, and
performance are evaluated later in Phase 1A without changing the judge.

The identity oracle must not claim that a finite digest is mathematically
injective. Equal qualified facts must produce identical canonical bytes and the
same candidate ID; for accepted/published states, the same `StateId` must imply
identical canonical bytes and facts. Candidate-bearing admission at an
occupied digest compares exact bytes: equal coalesces, unequal terminates as
`T03_REJECTION / STATE_ID_COLLISION` without any alias, head, root, mapping,
index, revision, custody, or capacity change. Reference-only transitions may
consume only an already admitted, authorized no-alias binding and must perform
zero immutable-payload comparison or I/O. A candidate-bearing attempt at a
reference API is rejected or routed to admission before that fast path. The
forced-collision seam covers publish, import, recovery, index rebuild,
reference-API ingress, and last-root behavior, but adds no product interface,
physical method, or algorithm count.

## Current complexity status

| Procedure | Time | Peak memory | Persistent/scratch | Status |
|---|---|---|---|---|
| every procedure above | `UNSEALED` | `UNSEALED` | `UNSEALED` | `NOT_RUN`; no bound may be inferred from this draft |

The final Phase 0 seal must replace each `UNSEALED` entry with a derived or
mechanically enforced bound over a named finite population. Measurements alone
cannot stand in for worst-case bounds unless the owning schema explicitly
defines an empirical statistic.

<!-- packet:evaluation -->

# Phase 0 evaluation contract

Status: **DRAFT — ALL PROTOCOLS AND BENCHMARK TERMS UNSEALED; NOTHING RUN**

Phase 0 may reproduce facts and falsify judge construction after its input lock
and independently verified phase-entry authority exist. It may not run or tune
candidate profiles against the selection corpus or untouched holdout. The two
regions below share one producer, lock, invalidation boundary, and acceptance
boundary, but remain separately machine-checked responsibilities.

<!-- evaluation:experiments -->

## General experiment contract

Protocols below are preregistration candidates, not execution approval. Every
Raw-result path remains absent until the exact protocol and custody closure are
locked.

### Protocol registry

| ID | Falsifiable question | Protocol state | Required result/evidence | Raw-result path |
|---|---|---|---|---|
| `P0-EXP-001` | Does the source/dependency/surface generator reproduce the complete pinned e497 inventory? | `UNSEALED / NOT_RUN` | normalized manifests, two independent reproductions, discrepancy ledger, exact source/build identity | `NOT_RUN` |
| `P0-EXP-002` | Does the candidate generator enumerate every frozen eligible topology/profile exactly once or issue a checkable `INAPPLICABLE` receipt? | `UNSEALED / NOT_RUN` | generator/input/output digests, counts by family, duplicate/equivalence map, completeness/admissibility/dominance checks | `NOT_RUN` |
| `P0-EXP-003` | Does the independent oracle reject seeded semantic, COW, crash, authorization, replay, lifecycle-publication, and cleanup mutations without encoding a candidate representation? | `UNSEALED / NOT_RUN` | mutation/falsification corpus covering producer substitution, authority-axis aliasing, policy/verifier path replacement, forged/missing commit receipts, partial invalidation suffixes, retained-state tampering, minimized counterexamples, oracle provenance, and coverage matrix | `NOT_RUN` |
| `P0-EXP-004` | Can accepted-no-alias same-`StateId` root/reference transfers be judged with whole-operation zero immutable-payload I/O while candidate collisions and last-root races fail closed? | `UNSEALED / NOT_RUN` | instrumented protocol that separates candidate-bearing occupied-digest comparison from accepted reference-only paths, forces collisions at publication/import/recovery/index rebuild/reference-API ingress/last root, proves typed rejection before fast-path entry, preserves zero immutable-payload I/O for accepted references, and charges bounded cleanup plus admission/metadata separately across every terminal | `NOT_RUN` |
| `P0-EXP-005` | Can storage-side and untrusted-runtime resource populations be bounded and attributed through overload, descendant, supervisor/reaper, crash, and cleanup faults? | `UNSEALED / NOT_RUN` | process-tree/cgroup/storage protocol, admission and fault schedule, cleanup-plateau rule, attribution-error bound | `NOT_RUN` |
| `P0-EXP-006` | Is the newly attested incumbent eligible for a matched `QG-PERF-001` comparison? | `UNSEALED / NOT_RUN` | exact causal source/build/config/artifact/environment receipt and comparator-equivalence verdict | `NOT_RUN` |
| `P0-EXP-007` | Do disposable Linux/WASI/Firecracker spikes falsify any claimed semantic boundary without introducing a production plugin seam? | `UNSEALED / NOT_RUN` | isolated contract results; `unsupported` accepted; no production dependency or compatibility claim | `NOT_RUN` |
| `P0-EXP-008` | Does the proposed static-role two-envelope challenger preserve judge/candidate noninterference under every shared process/filesystem/cache/log/admin/timing path? | `UNSEALED / NOT_RUN` | capability/ACL model and adversarial leakage evidence; failure preserves the three-envelope conservative grouping | `NOT_RUN` |

### Mandatory preregistration

Each Protocol must freeze exact artifacts, inputs, environment, fixtures,
seeds, order/randomization, controls, oracle, sample/exhaustion rule,
thresholds, fault/crash schedule, retry/outlier/stopping policy, resource
attribution, raw paths, and invalidation rules before Results are visible.
Selection and holdout assignments are disjoint; holdout custody is inaccessible
to candidate authors. Authority/lifecycle mutation fixtures must include
input-lock/result-producer substitution, acceptor/verifier identity-axis
aliasing, policy/verifier symlink and pathname replacement, stale or reused
state tokens/operation IDs, forged or missing commit receipts, incomplete
invalidation suffixes, and retained-state-chain tampering.

### General experiment results

None. No raw result, pass, speedup, candidate score, compatibility claim, or
product method is recorded. Result access before input lock invalidates the
Protocol and requires a new ID and untouched holdout.

<!-- evaluation:benchmarks -->

## Benchmark and comparator contract

Phase 0 freezes the sole numeric/statistical performance contract. It produces
no V2 performance winner or guarantee. The authoritative historical evidence
is [`stage-04-6-baseline.md`](../../../evidence/stage-04-6-baseline.md).

### Current evidence disposition

| Evidence | Current classification | Allowed use |
|---|---|---|
| Stage 4.6 P4 timings and run-artifact receipts | measured historical context, `R_stage46 = INCOMPARABLE` for matched V2 decisions | fixture/measurement ideas and negative provenance evidence only |
| Stage 4.6 “100×” label or divided values | unmeasured hypothesis | never a gate, baseline, guarantee, or synthetic measurement |
| distinct P1 activation-memory receipt | separate run and scope | never join to P4 timing |
| newly attested incumbent | `NOT_RUN` | may become comparator only after exact causal identity and equivalence acceptance |
| any V2 joint candidate | `NOT_RUN`; no `H_PROFILE` exists | no candidate timing is authorized in Phase 0 |

### Contract fields still to seal

| Field | Current state |
|---|---|
| one decision and null hypothesis | `UNSEALED` |
| exact incumbent artifact and comparator eligibility receipt | `UNSEALED / NOT_RUN` |
| exact operation × payload × structure × concurrency × fault cells | `UNSEALED` |
| disjoint selection corpus and one-time untouched holdout | `UNSEALED` |
| hardware/CPU/kernel/filesystem/mount/toolchain/allocator/config/cache state | `UNSEALED` |
| sample/power/statistics/uncertainty/randomization/warmup/order | `UNSEALED` |
| retry/outlier/stopping policy | `UNSEALED` |
| latency, payload/metadata I/O, memory, disk/scratch, sync/contention, cleanup attribution | `UNSEALED` |
| hard rejection before cost/performance comparison | `UNSEALED` |
| single accepted improvement threshold and tie rule | `UNSEALED` |

### Operation cost matrix

No cell has run. The Phase 0 seal must define every applicable operation and
cost dimension, including best/expected/worst or amortized conditions where
valid, with symbol domains and whether each value is `TARGET`, `DERIVED`,
`MEASURED`, or `UNKNOWN`. Same-accepted-`StateId` root operations require
whole-operation zero selected-state immutable payload reads/writes/copies and
zero root-private closure bytes; bounded metadata is a separate measurement.
Candidate collision admission, exact-byte comparison, and cleanup are separate
charged cells and may never be hidden inside that COW fast path.

Correctness, security, durability, finite-resource rejection, and cleanup
precede performance. A faster invalid profile cannot win. If no eligible
matched comparator can be produced, the performance decision remains
`BLOCKED` rather than inheriting Stage 4.6.

<!-- evaluation:end -->

<!-- packet:verification -->

# Phase 0 verification note

Status: **DRAFT — ALL GATE EVIDENCE `NOT_RUN`**

The owning predicates are in
[`qualification/gates.md`](../../../qualification/gates.md). Phase 0 seals
facts, falsifiers, protocols, or judge contracts for every dimension. It does
not promote a model or protocol to a candidate result.

## Qualification matrix

| Gate ID | Phase 0 obligation | Status | Required evidence before Phase 0 acceptance |
|---|---|---|---|
| `QG-PROV-001` | seal all inputs, rules, commands, identities, path sets, raw-output custody, and independent reproduction | `NOT_RUN` | exact Git/tree/dirty/dependency/tool/build/environment/corpus/runner manifests and verified commands |
| `QG-DES-001` | seal outcome-neutral architecture comparison, deletion, authority, source-graph, and total-disposition rules | `NOT_RUN` | finite candidate closure and generator, deletion counterexample schema, current source/authority ledgers |
| `QG-SEM-001` | seal independent oracle, total operation/surface map, candidate-to-accepted no-alias identity admission, COW, request-binding, replay, authorization, and terminal/fault fixtures | `NOT_RUN` | byte-exact corpus, forced-collision seam, expected-result generator, mutation/falsification and coverage evidence |
| `QG-FMT-001` | seal fact corpus, portability/prohibited-fact laws, and finite limits | `NOT_RUN` | representation-neutral vectors and reject/limit fixtures; no format selected |
| `QG-CRASH-001` | seal process-death/host-power-loss cuts, custody and recovery predicates | `NOT_RUN` | executable crash matrix including root transfer, last-reference, effect, and cleanup cuts |
| `QG-RES-001` | seal populations, hard limits, admission/overload, attribution, containment, and cleanup measurement | `NOT_RUN` | complete resource ledger and operation × terminal × applicable fault protocol |
| `QG-SYS-001` | seal unsafe/FFI/syscall/ioctl/mmap/filesystem/helper/descendant inventory and falsifiers | `NOT_RUN` | pinned source/substrate inventory and enabled/disabled-path test plan |
| `QG-ADP-001` | seal runtime-effect conformance laws and disposable Linux/WASI/Firecracker spike scenarios | `NOT_RUN` | boundary-neutral scenarios; `unsupported` allowed; no production compatibility claim |
| `QG-MIG-001` | seal actual legacy source/writer graph, import dependency law, generation fence, fleet barrier, retirement, and destruction separation | `NOT_RUN` | source/fence model, every-writer inventory, crash cuts, no-reference and post-release deletion schemas |
| `QG-PERF-001` | seal the sole numeric/statistical/comparator/holdout decision contract | `NOT_RUN` | newly attested comparator plan, preregistered cells/statistics/thresholds, immutable corpus custody |
| `QG-OPS-001` | seal runbook, monitor, abort/restore/roll-forward, evidence, and cleanup contracts | `NOT_RUN` | reproducible operational scenarios and ownership/escalation matrix |
| `QG-RET-001` | seal compatibility target/horizon/policy and total-disposition schema | `NOT_RUN` | `DEC-011` closure, reference inventory rules, changed-artifact qualification and distinct destruction authority schema |

## Structural and provenance checks for this draft

These checks validate preparation structure only and do not pass Phase 0:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/new_2.0_migration_implementation_plan
python3 -B execution/validate.py
python3 -B execution/validate.py --self-test-authority-fd-exec
awk '/^```text$/{inside=1;next} inside && /^```$/{exit} inside{print}' \
  evidence/draft-manifest.md | shasum -a 256 -c -
```

Before result-bearing work, verification must also record the exact
`evidence/input-lock.json` digest, source/build identities, commands, exit
codes, raw outputs, environment, actor/capability scope, and cleanup receipts.
Before a final verdict, it must additionally prove exact input-lock/manifest
producer equality, the separate post-result manifest proof, manifest-to-lock
and acceptance-to-manifest bindings, one-open/no-follow policy, post-copy
immutable close-on-exec memfd seals, fixed child resource limits, deadline
enforcement after early pipe closure, and sealed exact-fd verifier dispatch,
authenticated versioned or write-denied custody for accepted
packet/evidence bytes, and every retained state transition plus its independent
signed provider commit receipt. Verify that no executable dispatch occurs
after any earlier local/package/policy error and that a first authority failure
suppresses all later verifier launches. The local validator alone is not that
proof. The post-result manifest proof is already mandatory in the legal
`SEALED / NOT_RUN` interval; the absence of an acceptor never defers producer-
seal authentication.

## Terminal/fault closure

The full operation × terminal × applicable fault registry is not yet
instantiated; status is `NOT_RUN`. Every exclusion requires an independently
checkable `UNREACHABLE` proof. Success-only sampling, process-local cleanup,
elapsed-time assumptions, or a missing raw receipt cannot pass.

## Verdict

`NOT_RUN`. No Phase 0 predicate, candidate, algorithm, performance claim,
future-runtime compatibility claim, or successor authorization is accepted by
this draft.

<!-- packet:handoff -->

# Phase 0 packet handoff

Status: **DRAFT / `NOT_RUN` — CONTINUE PHASE 0 PREPARATION ONLY**

This controlled section does not embed its containing manifest digest. Compute
the manifest and acceptance digests from their files and verify them before
use. `acceptance.json` is currently only a bootstrap `NOT_RUN` shell.

## Current disposition

```text
phase / gate:               00 / 00-evidence-seal
lineage:                    00-evidence-seal-r0001
causal position:            1 of 11
packet maturity:            DRAFT
producer-reported status:   NOT_RUN
independent disposition:    NOT_RUN
accepted output:            NONE
accepted profile winners:   0
selected algorithms:        0
Phase 1 authority:          NONE
manifest SHA-256:           compute externally from manifest.json
acceptance SHA-256:         compute externally from acceptance.json
input-lock SHA-256:         NONE
```

## Read and verify first

1. Read [`execution/README.md`](../../README.md),
   [`gates.json`](../../gates.json), this complete packet, and the owning
   [Phase 0 contract](../../../phases/00-independent-judge-and-evidence-seal.md).
2. Read the plan in the authority order from the package
   [`README.md`](../../../README.md) and stop on conflicts.
3. Reverify the docs and reserved product identities in `manifest.json` without
   modifying either worktree.
4. From the package root run `python3 -B execution/validate.py` and verify
   `evidence/draft-manifest.md`. A mismatch blocks work; never refresh a hash
   silently.

## Next allowed

- assign candidate-independent evidence/judge producers and a distinct
  independent acceptor;
- obtain the exact Phase 0 authorization receipt, produce the generic
  phase-entry attestation over actor principal/credential/control-domain
  triples, exact gate capabilities, validity, and revocation facts, then have
  the authenticated wrapper pin a version-3 external per-artifact verifier
  policy covering attestation, input lock, sealed manifest, acceptance, and any
  non-bootstrap execution state;
- close `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` with owning evidence and
  approval;
- finish and content-address the Phase 0 source/surface/state/authority/resource
  inventories and deterministic candidate-universe generator;
- preregister fixtures/oracle, holdout custody, comparator/statistics, resource,
  crash, and terminal/fault protocols; and
- snapshot `packet.md` and every other pre-result protocol/config/corpus/
  authority input as exact bytes or a canonical content-addressed-object
  receipt, including the two exact phase-entry authority rows required by
  `execution/README.md`, then seal the canonical `evidence/input-lock.json`
  index and obtain the required external policy-selected verifier `PASS` before
  any result-bearing procedure; do not copy or self-hash `manifest.json`;
- after work, require the exact input-lock producer triple to sign the finalized
  manifest under the distinct result-seal domain, independently verify that
  manifest-to-lock binding, and only then permit the distinct acceptor to bind
  acceptance to the manifest;
- establish authenticated versioned or write-denied custody and independent
  retention/audit receipts before any final verdict; and
- for any frontier advance or invalidation, preserve exact prior-state bytes,
  use the authenticated complete prior-packet prefix, publish state last through
  a genuine conditional write or exclusive lease/fence, and require the
  independent one-shot signed commit receipt before use.

## Next forbidden

- selecting, implementing, benchmarking, or tuning a candidate topology or
  physical profile;
- exposing the holdout to candidate authors;
- adding product code, schema, dependency, package, API, cache, worker, service,
  runtime plugin/seam, or writable V2 state;
- instantiating or executing a Phase 1/2 packet;
- self-acceptance or treating this artifact-system review as Phase 0 acceptance;
- claiming Stage 4.6 comparability, a 100× guarantee, or a selected algorithm;
  and
- staging, committing, merging, pushing, cutting over, retiring, or deleting
  anything without separate authority.

## Current blockers and unknowns

- independent Phase 0 producer/acceptor/holdout-custodian identities and
  isolation receipts are unassigned;
- the Phase 0 authorization receipt, phase-entry attestation, version-3 external
  policy, exact self-contained verifier/trust-root custody, and independent
  state commit provider do not exist;
- four Phase 0 decisions remain open;
- complete current source/surface/state/authority/resource inventories and
  candidate-universe generator outputs do not yet exist;
- oracle, corpus/holdout, comparator, statistics, resource/fault protocols, and
  their input lock are unsealed;
- accepted-packet/evidence custody, retained prior-state chain, and one-shot
  state publication receipts are unsealed; and
- all qualification evidence remains `NOT_RUN`.

## Invalidation response

A changed Phase 0 input, decision, rule, fixture, holdout, threshold,
comparator, environment, authorization law, or evidence byte reopens Phase 0
and invalidates every transitive consumer. Archive the complete obsolete
lineage under `execution/history/`, append the exact trigger/closure to
`execution/state.json`, preserve the exact prior state and complete
authenticated prior-packet prefix, and publish the replacement state last
under a genuine CAS or lease/fence receipt. Block downstream use until the
independent verifier proves that exact commit, create a new input lock and
untouched holdout, and obtain new independent acceptance. No exit record
authorizes Phase 1.

<!-- packet:end -->
