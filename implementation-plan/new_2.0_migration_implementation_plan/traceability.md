# Traceability and document authority

Status: **DESIGN DRAFT — CONFLICTS BLOCK IMPLEMENTATION**

One concern has one owner. Summaries, phase notes, benchmarks, and review
records may link to a contract; they cannot redefine it, select a candidate,
promote a target, or broaden authorization.

## Authority map

| Concern | Owning document |
|---|---|
| product invariants, limits, terminal/fault registry, prohibitions | `design/requirements.md` |
| architecture candidates and comparison | `design/architecture-selection.md` |
| R0 boundary laws and cross-effect direction | `design/architecture.md` |
| integrated storage workflows, resources, and operation costs | `design/storage-model.md` |
| portable facts, identity, validation, bytes | `design/canonical-format.md` |
| selected-state behavior | `design/state-store.md` |
| application authorization/order/recovery routing | `design/application-coordination.md` |
| current mutable runtime-effect behavior | `design/runtime-effects.md` |
| observable operations and compatibility | `design/public-api.md` |
| import, fleet fence, cutover, retirement, release, destruction | `design/migration-cutover.md` |
| Rust source/dependency challenger | `design/source-layout.md` |
| physical-method status and candidate protocol | `algorithms/registry.md`, `algorithms/selection-protocol.md` |
| open decisions | `decisions/README.md` plus later accepted ADRs |
| permission/risk envelopes and causal order | `phases/README.md` plus the three numbered phase files |
| executable pass/fail predicates | `qualification/gates.md` |
| gate topology, mutable execution record, packet shape, content identity, independent verdict, and dependency/invalidation protocol | `execution/README.md`, `execution/gates.json`, `execution/state.json`, and `execution/schemas/` |
| active Phase 0 execution preparation | `execution/phase-00/00-evidence-seal/` |
| source and measurement provenance | `evidence/` |
| historical-claim disposition | `traceability/source-disposition.md` |
| hostile review procedure | `review-prompts/whole-plan-hostile-review.md` |

R0 adds no mandatory selected-state API/package/component, aggregate Backend,
named canonical module, coordinator, neutral port package, facade, service, or
deployable. Exact responsibility, call-edge, authority, module, package,
component, process, and method counts remain Phase 1 outputs. Pure computation
has no authority. R0 and the three baseline ownership questions are not lower
bounds: Phase 0 generates all five ownership-question partitions and finite
deletion/placement transforms over packages and edges that actually exist in
clean e497. Each generated candidate must compile or carry an independently
checkable `INAPPLICABLE` proof. Historical `layerstack-core` and MPLA material
is incomparable context, not a current package, edge, authority, or deletion
target. A larger boundary survives only with an executable deletion
counterexample and favorable before/after ledger.

## Required matrices

| Matrix | Completion rule |
|---|---|
| historical claim disposition | every legacy claim is retained, reframed, reopened, migration-only, removed, or evidence-only with a current owner |
| external-surface disposition | observed manager/runtime and observability operation names, HTTP routes, RPC control operations, legacy proposal, current draft, unmatched surfaces, and accepted target remain transport-aware and distinct |
| durable field/writer disposition | every field has exact byte source, writer/readers, commit/replay/recovery unit, migration mapping, and keep/fuse/derive/delete result |
| architecture deletion ledger | every retained boundary, call, state, authority, package, component, process, and deployable has an invariant, lifecycle owner, deletion failure, and before/after count |
| method disposition | six historical custom mechanisms remain zero-winner; 21 audit families remain questions, not algorithms |
| operation cost | every operation covers CPU, best/expected/worst and amortized conditions, byte I/O, peak-live disk, managed/cgroup memory, FDs/tasks/locks/syncs, contention, scratch, progress, crash/recovery, and cleanup |
| exact COW and collision admission | candidate-bearing admission compares complete canonical bytes for an occupied candidate `StateId`; unequal bytes fail `STATE_ID_COLLISION` before any durable/reference side effect. Each accepted reference-only transition consumes only a previously admitted authorized no-alias binding and proves one closure, zero selected-state immutable payload read/write/copy, zero root-private closure bytes, and separate metadata I/O on all terminal/fault paths; candidate-bearing reference requests are rejected or routed to admission before fast-path entry |
| MCTS/rollout | immutable checkpoint parent, isolation, deterministic IDs, stale/winner/sibling fate, no hidden merge/rebase, finite admission/fairness, cleanup, and required fan-out close |
| resource cleanup | normative `operation × terminal × applicable fault` cells execute or are proved `UNREACHABLE`; every cache/worker/queue/FD/buffer/debt converges |
| system boundary | every `unsafe`, FFI, syscall/ioctl, mmap/direct-I/O, filesystem primitive, helper/descendant, and containment assumption is inventoried and tested |
| benchmark provenance | P4 run seal is verified but incomplete causal source/build closure keeps `R_stage46=INCOMPARABLE` |

Documentation-only fields or operations are not product requirements. Missing
deployed facts block Phase 1.

## Requirement-to-gate trace

| Requirement family | Phase 0 judge | Phase 1 non-live proof | Phase 2 live/release proof |
|---|---|---|---|
| correctness, API, authorization, replay | facts, fixtures, oracle, terminal registry | gates 1A–1F: joint profile, local/cross-effect proof, exact-artifact rehearsal | gates 2A–2D: live truth, observation, changed-artifact reproof |
| portable identity and runtime neutrality | vectors and disposable runtime spikes | joint `H_PROFILE`, `H_FMT`, current-Linux proof | byte-identical cutover and total-disposition `H_RELEASE` proof |
| durability, crash recovery, effect custody | executable models and crash matrix | local then cross-effect then exact-artifact rehearsal | cutover/recovery evidence and changed-artifact proof |
| exact COW and rollout fan-out | purpose-independent fixtures and limits | inactive roots, active realizations, mixed load | live plateau and total-disposition reproof |
| bounded memory/cache/resources/cleanup | limits and full terminal/fault product | each scope plus side-by-side migration and exact-artifact matrix | live plateau, retirement cleanup, release reproof |
| small publication and all-operation performance | provenance and one preregistered comparator rule | candidate comparison and exact `H_PRECUTOVER` qualification | live signals and changed `H_RELEASE` proof |
| import and monotone fleet fence | actual writer/source inventory | temporary migration unit depends only on the read-only legacy adapter, accepted pure canonical functions/types, and narrow selected-state import command; permanent V2 code never depends on migration code; exact `g+2` installation; atomic global `V2Writable(g+2)` transition | every-selector activation plus reconstructible receipts; durable fleet completion; only then ingress opens for the first public V2 operation acknowledgment; observation and no-reference retirement proof |
| compatibility and destruction | horizon and target inventory | removal manifest and rehearsal | retirement/release; deletion still separately authorized outside DAG |

## Three-phase, 11-gate order

```text
Phase 0
  1 judge/evidence seal

Phase 1 — reversible and non-live
  2 joint H_PROFILE/NO_WINNER -> 3 H_FMT -> 4 Hstore
  -> 5 Hpermanent -> 6 H_PRECUTOVER -> 7 byte-identical Hqual

Phase 2 — separately authorized live-fleet work
  8 exact-H_PRECUTOVER cutover -> 9 bounded observation
  -> 10 compatibility retirement/H_RELEASE build
  -> 11 total QG disposition, exact-artifact qualification,
     new-release-epoch fleet rebind, old-process drain, and live release

outside DAG
  optional separately signed destructive legacy-byte deletion
```

The `0 -> 1` boundary isolates the judge from candidate authors. The `1 -> 2`
boundary prevents non-live authority from preauthorizing irreversible live
mutation. All intermediate hashes, independent acceptors, evidence scopes,
invalidation edges, and stop rules remain gates. Three is the smallest
conservative operational grouping currently justified; a static-role
two-envelope challenger remains mandatory and the global minimum is `OPEN`.

## Change propagation

A change is incomplete until its owner, decision, source mapping, phase/gate
scope, fixtures, migration impact, evidence seal, and handoff move together:

- fact, requirement, candidate set, fixture, holdout, threshold, statistic,
  rollout contract, or provenance change -> reseal Phase 0 and invalidate all
  consumers;
- architecture ownership/call/package/process or physical profile/protocol
  change -> rerun the joint Phase 1A tournament and all dependent gates;
- portable byte/identity change -> rerun `H_FMT` and every consumer;
- `H_PRECUTOVER` code/config/schema/runbook drift -> rebuild at 1E and rerun 1F;
- live bytes differing from qualified `H_PRECUTOVER` -> block 2A; and
- compatibility removal changing bytes -> build at 2C, produce a total QG
  disposition, freshly qualify exact `H_RELEASE`, and deploy/rebind the complete
  fleet at a distinct release epoch in 2D.

Every successor packet consumes both the predecessor manifest and independent-
acceptance SHA-256. Any changed consumed byte or decision invalidates the
owning record and all transitive packets; the obsolete lineage is retained and
the earliest owner is reopened. `execution/gates.json` owns immutable ordering;
`execution/state.json` owns the canonical instantiated prefix and exact
invalidation/archive records. Every non-bootstrap state transition retains the
exact prior state and prior packet prefix and is usable only with an
authenticated publisher plus an independently verified genuine external
conditional-write or fenced-lease commit receipt over the exact raw successor
and prior token. Future packet directories remain absent until
the accepted-predecessor condition in the catalog and the separate
authority-receipt condition in the entering packet's input-lock contract are
satisfied.

Evidence predating a changed input is invalid unless its dependency record
proves independence. Phase 2 release approval never authorizes destructive
legacy-data deletion.
