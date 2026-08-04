<!-- packet:plan -->

# Gate execution plan

Status: **TEMPLATE — DO NOT EXECUTE OR TREAT AS A DECISION**

Replace every bracketed value before sealing. Copy this template only after the
gate is eligible under `execution/gates.json`. The copied packet starts
`DRAFT / NOT_RUN`; it must not inherit an acceptance or imply that a future
architecture, method, or implementation has been selected.

<!-- plan:spec -->

## Identity and authority

| Field | Value |
|---|---|
| phase / gate | `[phase-id] / [gate-id]` |
| immutable lineage | `[gate-id]-r[NNNN]` |
| packet maturity / producer report / independent disposition | `DRAFT / NOT_RUN / NOT_RUN` |
| producer | `[principal ID, credential fingerprint, and control-domain fingerprint; the pre-result proof lives in input-lock.json and the same triple signs the post-result manifest under the seal domain]` |
| independent acceptor | `[independent principal/credential/control-domain triple, or UNASSIGNED; proof lives in acceptance.json]` |
| capability ceiling | `[exact allowed effects]` |
| explicit prohibitions | `[effects this gate may not cause]` |
| authorization receipt | `[content-addressed receipt; a phase exit is insufficient]` |
| phase-entry authorization attestation | `[attestation logical path; the external authority policy chooses the exact verifier build and trust root]` |

The authenticated phase-entry attestation authorizes exact
`produce:<gate-id>` and `accept:<gate-id>` capabilities. Every result-bearing
action is verified through the externally pinned, write-denied authority
policy. Producer and acceptor principal ID, credential fingerprint, and control
domain must all differ. A sealed manifest is valid only when its producer
triple exactly equals the input-lock producer and its independently verified
post-result proof covers the finalized manifest.

## Exact consumed inputs

`manifest.json` is the single machine owner of both digests for the immediate
predecessor. Name the logical predecessor here and point to its manifest row;
do not copy digest literals into prose. Name every additional source, build,
configuration, requirement, corpus, and authority input by its logical path in
the input-lock index. At phase entry, include exactly the authorization-receipt
and phase-entry-attestation rows required by `execution/README.md`. The latter,
every producer input lock, every sealed manifest, every final acceptance, and
every non-bootstrap execution state must pass the external policy-selected
verifier before use. A branch, tag, directory, or `latest` label is not an
identity.

| Logical input | Machine-owned identity row | Purpose | Read-only verification |
|---|---|---|---|
| `[predecessor gate/lineage or NONE]` | `manifest.json#/predecessors/[index]` | `[why consumed]` | `[command]` |
| `[additional input]` | `evidence/input-lock.json#/entries/[logical_path]` | `[why consumed]` | `[command]` |

## Objective, non-goals, and success predicate

- Objective: `[one gate-sized outcome]`.
- Non-goals: `[explicitly excluded work]`.
- Success: `[all required QG/REQ predicates and exact output identity]`.
- Valid terminal alternatives: `[FAIL, BLOCKED, NO_WINNER when applicable]`.

## Scope and disposition

Name every in-scope source, generated file, surface, authority, configuration,
and evidence class. Assign each discovered item `KEEP`, `DELETE`, `MOVE`,
`NEUTRAL_DTO`, `NOT_APPLICABLE(reason)`, or another owning-contract disposition.
Unlisted work is out of scope and cannot enter a sealed run.

## Work DAG and safe parallelism

| Work item | Consumed sealed inputs | Produces | May run with | Must follow | Stop condition |
|---|---|---|---|---|---|
| `[id]` | `[digests]` | `[artifact/evidence]` | `[ids or NONE]` | `[ids or NONE]` | `[condition]` |

Parallel lanes share one immutable input lock. They may not edit the judge,
inspect another lane's holdout, rebuild the artifact they qualify, or broaden
the phase capability.

## Resource and safety envelope

For every buffer, allocation, mapping, file, inode, descriptor, task, worker,
queue, cache, scratch object, pin, and cleanup debt, record the owner, charge-
before-allocation rule, hard cap, overload behavior, and release/recovery path.

| Resource | Owner | Hard cap | Acquire-before-use rule | Overload | Every-terminal cleanup |
|---|---|---:|---|---|---|
| `[resource]` | `[owner]` | `[cap + unit]` | `[rule]` | `[fail/block]` | `[rule/evidence]` |

## Evidence protocols

The detailed method, experiment, benchmark, and verification contracts live in
the sibling algorithm, evaluation, and verification files. Before
result-bearing work, represent their exact pre-result bytes and every other
input under `evidence/input-lock/snapshots/`, then create the canonical
`evidence/input-lock.json` index defined by the input-lock schema. Store either
the exact bytes or a canonical immutable receipt that names the object's
digest, length, media type, durable content-addressed location, and
availability-verification command. The index and final result manifest are
distinct objects; neither hashes itself. The authenticated execution wrapper
supplies an absolute external authority-policy path plus the SHA-256 of its
exact bytes; packet bytes never choose their own verifier or trust root.
Policy and verifier-source locators are opened once with no-follow component
traversal; verifier bytes are copied into a close-on-successful-exec, fully
write/grow/shrink/seal-sealed memfd and hashed only after sealing; protected
verification has no source-path, unsealed-FD, or copy-to-disk execution
fallback and uses the contract's fixed child resource limits.

## Outputs and handoff

| Output | Exact format/identity | Acceptance predicate | Consumer |
|---|---|---|---|
| `[output]` | `[digest/receipt contract]` | `[predicate]` | `[next gate or terminal]` |

Passing this gate does not authorize a new phase. State the next allowed and
forbidden actions in the handoff region of this `packet.md`;
`acceptance.json` owns only the independent verdict over one exact manifest.

## Invalidation and reopening

List every trigger, its earliest owning gate, all transitive consumers, the
actor who blocks downstream work, and the exact archive path retained for the
obsolete lineage. `INVALIDATED` is recorded in `execution/state.json`, not by
editing the preserved gate verdict. Preserve exact prior-state bytes, bind the
complete authenticated prior packet prefix and full affected suffix, publish
state last through a genuine conditional write or exclusive lease/fence, and
require the independent one-shot commit receipt. Never refresh a digest
silently.

<!-- plan:decisions -->

## Consumed decisions

Requirements and cross-gate choices belong in the global decision ledger and
are referenced here by ID and accepted digest. An unanswered question is not a
decision.

| Decision ID | Accepted digest | Required consequence in this gate | Verified by |
|---|---|---|---|
| `[id or NONE]` | `[digest]` | `[consequence]` | `[command/reviewer]` |

## Local decision ledger

| Local ID | State | Question | Alternatives retained | Evidence required | Decision and rationale | Owner |
|---|---|---|---|---|---|---|
| `[gate]-D001` | `OPEN` | `[question]` | `[finite alternatives]` | `[evidence]` | `UNDECIDED` | `[owner]` |

Allowed states are `OPEN`, `ACCEPTED`, `REJECTED`, `SUPERSEDED`, and
`NOT_APPLICABLE(reason)`. An accepted row names the exact evidence and the
independent acceptor. Result-visible tuning creates a new lineage.

## Rejected assumptions

Record shortcuts explicitly rejected during preparation so they cannot return
as implicit implementation choices.

| Assumption | Why rejected | Reopening evidence |
|---|---|---|
| `[assumption]` | `[counterexample or owning rule]` | `[required evidence]` |

## Downstream impact

For each accepted or superseded decision, name every output and later gate it
affects. A changed accepted decision invalidates those consumers unless their
owning gate accepts a complete-closure non-impact proof.

<!-- plan:end -->

<!-- packet:algorithms -->

# Gate algorithm note

Status: **TEMPLATE — ZERO METHODS SELECTED**

An “algorithm” here means any nontrivial procedure whose correctness or cost
can affect the gate: standard-library use, protocol, traversal, indexing,
sorting, reclamation, concurrency control, recovery, hashing, encoding, or
measurement. Familiarity is not proof, and a custom method is not preferred.

## Inventory

| Method ID | Purpose | State | Standard/existing alternative | Why a distinct method is needed |
|---|---|---|---|---|
| `[gate]-ALG-001` | `[purpose]` | `UNSELECTED` | `[alternative]` | `[named failing execution, or NOT YET JUSTIFIED]` |

Use `UNSELECTED`, `USED_STANDARD`, `PROPOSED`, `PROVED`, `REJECTED`, or
`NOT_APPLICABLE(reason)`. Do not count audit questions as produced algorithms.

## Required proof card

Complete one card for every method that survives:

- exact input/output and pre/postconditions;
- invariant and linearization/commit point;
- concurrency, cancellation, duplicate/stale input, and every crash cut;
- recovery and progress/liveness rule;
- time complexity by operation and adversarial input;
- immutable-payload reads/writes/copies, metadata I/O, and synchronization;
- peak managed memory, persistent space, scratch, FDs, tasks, queues, pins, and
  cleanup debt, including simultaneous operations;
- overflow and capacity behavior before allocation;
- independent oracle, differential/metamorphic properties, and fault tests;
- standard-library/existing-crate comparison and deletion counterexample; and
- evidence digest and independent acceptor.

For checkpoint/fork/root operations, first distinguish candidate-bearing
admission from a reference-only transition over an already admitted,
authorized no-alias `StateId` binding. Candidate-bearing admission compares
exact canonical bytes when its digest is occupied: equal bytes coalesce;
unequal bytes terminate as `T03_REJECTION / STATE_ID_COLLISION` without any
alias/root/mapping/index/revision/custody/capacity fact. A candidate-bearing
attempt through a reference API must be rejected or routed to admission before
the zero-payload fast path. The qualification-only forced-collision seam covers
publish, import, recovery, index rebuild, reference-API ingress, and last-root
behavior; it must never make an accepted reference-only transition reread or
compare immutable payload bytes, and it is not a product API or algorithm.
After admission, measure whole-operation selected-state immutable payload
reads, writes, copies, and new root-private closure bytes. Do not hide work in
validation, warming, recovery, or cleanup; charge collision admission
separately from COW.

## Complexity table

| Operation | Time | Payload I/O | Metadata I/O | Peak memory | Persistent/scratch | Synchronization | Bound status |
|---|---|---|---|---|---|---|---|
| `[operation]` | `[formula]` | `[formula]` | `[formula]` | `[formula]` | `[formula]` | `[formula]` | `TARGET/DERIVED/MEASURED` |

State the domain of every symbol and distinguish a target, derivation, and
measurement. A historical benchmark or median is not a universal bound.

<!-- packet:evaluation -->

# Gate evaluation contract

Status: **TEMPLATE — NO EXPERIMENT OR BENCHMARK RUN**

This section keeps general experiment duties and benchmark/comparator duties
independently visible while sharing one packet writer, input lock, invalidation
boundary, and acceptance boundary. The validator requires both marked regions,
their order, and their responsibility-specific content.

<!-- evaluation:experiments -->

## General experiment contract

Protocols and results are separate immutable objects. Seal protocol bytes,
corpus partitions, thresholds, execution order, stopping rules, and custody
before any result is visible. Candidate authors may not access or alter
holdout custody.

### Protocol registry

| Experiment ID | Hypothesis | Protocol state | Selection corpus | Untouched holdout | Oracle | Raw-result path |
|---|---|---|---|---|---|---|
| `[gate]-EXP-001` | `[falsifiable statement]` | `UNSEALED` | `[identity]` | `[custodian/identity]` | `[independent oracle]` | `NOT_RUN` |

### Required preregistration

For each experiment record:

- exact artifact/source/build/configuration/environment identities;
- finite population, fixtures, seeds, randomization, warm/cold state, and run
  order;
- controls and admissibility/equivalence rules;
- sample count/power or exhaustive-enumeration argument;
- thresholds, uncertainty method, retry/outlier/stopping policy;
- fault schedule, crash cuts, concurrency, timeout/cancel, and recovery;
- authority/lifecycle mutations: input-lock/result-producer substitution,
  acceptor/verifier axis aliasing, policy/verifier symlink and pathname
  replacement, stale/reused publication tokens, forged or missing commit
  receipts, partial invalidation suffixes, and retained-state-chain tampering;
- resource attribution and containment boundaries;
- expected raw file names and checksum procedure; and
- invalidation triggers and the owner who blocks downstream use.

### General experiment results

Do not prefill Results. After a run, append immutable result objects and
classify each claim as `MEASURED`, `DERIVED`, `FALSIFIED`, or `UNKNOWN`.
Protocol changes after result access require a new experiment ID and input
lock; they never rewrite an old result.

<!-- evaluation:benchmarks -->

## Benchmark and comparator contract

The Benchmark region is mandatory even when performance is not a decision
gate. In that case record `NOT_APPLICABLE` with the owning rule and acceptor.
Historical numbers remain context unless exact artifact and measurement
comparability are proved.

### Frozen benchmark fields

| Field | Frozen value |
|---|---|
| decision supported | `[one decision or NOT_APPLICABLE]` |
| candidate artifact | `[exact digest]` |
| comparator artifact | `[exact digest and eligibility receipt]` |
| workload/corpus | `[content identity]` |
| environment | `[hardware/kernel/filesystem/toolchain/config identity]` |
| samples/power | `[predeclared rule]` |
| randomization/warmup/cache state | `[predeclared rule]` |
| statistics/uncertainty | `[predeclared rule]` |
| retry/outlier/stopping | `[predeclared rule]` |
| resource attribution | `[process tree/cgroup/storage scope]` |
| acceptance threshold | `[single owning gate rule]` |

### Operation cost matrix

| Operation/cell | Latency statistic | Payload I/O | Metadata I/O | Peak memory | Persistent/scratch | Cleanup plateau | Result state |
|---|---|---|---|---|---|---|---|
| `[operation × size × contention/fault]` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `UNKNOWN` |

Report exact observations and uncertainty. Never restate a desired speedup as
a guarantee, divide historical measurements into synthetic targets, join
results from different runs, or allow performance to rescue a correctness
failure.

<!-- evaluation:end -->

<!-- packet:verification -->

# Gate verification note

Status: **TEMPLATE — VERIFICATION `NOT_RUN`**

## Requirement and gate matrix

| Requirement/QG ID | Applicable predicate | Command/model/oracle | Expected evidence | Status | Evidence digest |
|---|---|---|---|---|---|
| `[ID]` | `[predicate]` | `[reproducible command]` | `[artifact]` | `NOT_RUN` | `NONE` |

Every referenced ID must exist in the owning registry. `PASS` requires exact
artifact, environment, raw evidence, and independent acceptance. A partial run
stays `PARTIAL`; absence is not success.

## Terminal and fault closure

| Operation | Terminal | Applicable fault/crash cut | Resource delta expected | Recovery expected | Status |
|---|---|---|---|---|---|
| `[operation]` | `[success/error/cancel/timeout/crash/restart]` | `[fault]` | `[all charged populations]` | `[rule]` | `NOT_RUN` |

Execute the normative `operation × terminal × applicable fault` product or
provide an independently checkable `UNREACHABLE` proof for each excluded cell.

## Structural and provenance checks

Record schema validation, packet validation, controlled hashes, source/build
identity, dirty state, input-lock identity, required tools, and exact commands.
If a command mutates external state, identify its authorization and rollback/
recovery behavior before running it. For a sealed packet, also prove exact
input-lock/manifest producer equality, the separate manifest-seal proof,
manifest-to-lock and acceptance-to-manifest bindings, one-open/no-follow policy,
post-copy immutable close-on-exec memfd seals, bounded child resources,
deadline enforcement after early pipe closure, sealed exact-fd verifier
dispatch, and every retained execution-state transition
plus its independent provider receipt. The manifest seal is mandatory during
the legal `SEALED / NOT_RUN` interval; an absent verdict does not defer producer
authentication. Missing policy custody or receipt evidence fails closed. No
verifier may launch after an earlier local/package/policy failure, and the
first authority failure stops all later dispatch in that validation run.

## Verdict

State `PASS`, `FAIL`, `BLOCKED(reason)`, `PARTIAL(scope)`, or `NOT_RUN` for
every applicable predicate. The packet gate status is the most conservative
result, never an average or majority vote.

<!-- packet:handoff -->

# Gate handoff note

Status: **TEMPLATE — NO HANDOFF AUTHORITY**

This section is a compact instruction set for the next executor. It is
controlled by `manifest.json`, so it deliberately does not embed the digest of
the manifest that hashes it. The external `acceptance.json` supplies the exact
verdict and manifest digest. This section cannot accept its own packet or
authorize another phase.

## Current disposition

```text
phase / gate:               [phase-id] / [gate-id]
lineage:                    [gate-id]-r[NNNN]
packet maturity:            DRAFT
producer-reported status:   NOT_RUN
independent disposition:    NOT_RUN
manifest SHA-256:           COMPUTE FROM manifest.json; DO NOT EMBED HERE
acceptance SHA-256:         COMPUTE FROM acceptance.json; DO NOT EMBED HERE
accepted output SHA-256:    NONE
input-lock SHA-256:         NONE
```

## Read and verify first

List the owning contract files, exact predecessor records, source/build
identities, and read-only verification commands. The executor computes the
manifest and acceptance digests externally and stops on any mismatch. For a
phase-entry packet, also name the two exact authority input-lock rows and the
externally pinned authority-policy path/digest supplied by the authenticated
wrapper. That version-3 policy maps exact attestation, input-lock,
sealed-manifest, acceptance, and execution-state/bound-byte digests to a
self-contained verifier executable, build, trust root, and derived use.
Neither packet bytes nor predecessor acceptance may choose or replace that
trust configuration; protected dispatch hashes only an immutable close-on-exec
sealed clone, applies the fixed process/address-space/descriptor/file-output/
CPU/wall bounds, and has no source-path, unsealed-FD, copy-to-disk, or dynamic-
loader fallback.

## Next allowed

- `[one or more actions already inside the current authorized capability]`.

## Next forbidden

- accepting one's own output;
- creating or executing a successor packet without exact predecessor seals;
- treating gate exit as successor-phase authorization;
- refreshing hashes after drift; and
- `[gate-specific prohibitions]`.

## Blockers and unknowns

List every blocker and unknown with an owner and reopening condition. Do not
turn missing evidence into an assumption.

## Invalidation response

Name the earliest gate to reopen, all transitive packets to invalidate, the
actor who blocks use, and the preserved
`history/<gate-id>--<manifest-sha256>/` lineage. Record invalidation in
`execution/state.json`; preserve the exact prior state, bind the complete prior
packet prefix and full archived suffix, and require the one-shot independent
commit receipt before use. Do not edit the archived verdict.

<!-- packet:end -->
