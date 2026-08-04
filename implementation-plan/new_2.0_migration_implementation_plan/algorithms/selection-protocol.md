---
status: required-before-profile-implementation
authority: joint-profile-selection-protocol
depends-on:
  - DEC-012
  - QG-PERF-001
---

# Joint topology and physical-profile selection protocol

## Purpose

Phase 1A selects one globally closed, compile-valid topology × physical profile
as `H_PROFILE`, or records `NO_WINNER`. It does not reward PMSS names, POC reuse,
isolated microbenchmark wins, novelty, package deletion, or added abstractions.
There is no architecture winner before this tournament: method-dependent
dependencies, helpers, processes, recovery, and resources are part of the same
candidate. This prevents either axis from excluding the best valid pair.

## Phase 0 freeze, before any candidate result

The evidence seal contains:

- accepted product semantics and a transport-aware total disposition separating
  the exact 18 manager/runtime catalog operation names, eight observability
  operation names, externally reachable HTTP-only `file_list`, HTTP health and
  forward route families, RPC readiness control, 26 legacy-proposed rows,
  proposed target ledger, every unmatched current surface, and final target;
- actual legacy schema/root/session/replay/migration facts;
- byte-exact normal, edge, corrupt, crash, capacity, concurrency, and aggregate
  corpora plus an independent semantic oracle;
- the finite topology and physical-method universes, signed submission cutoff,
  mandatory baseline constructors, graph-transform axes, equivalence,
  admissibility, structural-dominance, product-generation, and late-discovery
  invalidation rules, plus complete candidate sets for all eight tournaments
  and standard-primitive incumbents;
- compile-valid evidence-only `R_LEGACY_CONTROL`, current `origin/main`, and
  pinned Stage 4.6 historical identity/context receipts; Stage 4.6 supplies no
  objective endpoint while `R_stage46 = INCOMPARABLE`;
- exact correctness/durability/timing/setup/cleanup boundaries;
- cold/warm/cache profiles, randomization seed, sample size, power analysis,
  confidence statistic, multiplicity rule, stopping rule, variance rule,
  outlier/censor/retry policy, and invalid-run classes;
- numerical absolute and relative pass thresholds for every selected workload;
- hard capacity, memory, worker, queue, descriptor, reader, custody, recovery-
  reserve, and runtime-profile limits;
- the complete hard-eligibility predicate, including every required record,
  invalid-result disposition, and hard-gate outcome;
- the guardrail-constrained Pareto-then-lexicographic procedure below,
  instantiated with every objective's metric ID, workload and aggregation,
  statistic, unit, direction, confidence construction and compared endpoint,
  deterministic transformation/rounding, ordered priority, and exact tie or
  non-dominance disposition; and
- disjoint candidate-selection and untouched holdout partitions with access
  logging.

The current `5.8136209 ms` and `0.1x` sparse-publication values are proposals,
not defaults. Phase 0 must accept them as product thresholds or replace them
before any run. “Faster” or “statistically significant” without an effect-size
threshold is not an acceptance contract.

Phase 0 is not sealed until the result can be computed from the sealed evidence
without reviewer judgment. Changing a candidate set, fixture, comparator,
threshold, sample/analysis rule, objective unit/direction/order, confidence
endpoint, Pareto treatment, tie rule, or holdout after observing results
invalidates every affected comparison and returns it to Phase 0.

Phase 1A's effective input is only the unchanged Phase 0 seal. Its generator
forms the complete frozen selectable-topology × physical-profile product. Every
pair has a content-addressed realization or an independently checkable
`INAPPLICABLE` proof under a sealed rule; silence cannot remove a pair.
Candidate discovery after any result is observed invalidates the tournament,
returns to Phase 0, and requires a new uncontaminated holdout.

The universe first contains compile-valid evidence-only `R_LEGACY_CONTROL`,
which reproduces the pinned current/legacy tree unchanged. The selectable
baseline contains `R0_IN_PLACE`; the complete generated
`R_ROLE_PARTITION[pi]` family covering all five set partitions of baseline
ownership questions `A`, `S`, and `N`; every finite `R1_ONE_BOUNDARY[s]`;
every `R_PACKAGE_DISPOSITION[d]` and `R_PLACEMENT[o,q]` transform over
packages, normal/build edges, source sites, and consumers that actually exist
in clean e497; and every `R_NECESSITY_*` transform whose
presealed executable trigger fires. It also contains every complete signed
submission received before the cutoff. Each generated member must compile or
carry an independently checkable `INAPPLICABLE` proof; graph equivalence may
collapse duplicates only under the presealed rule. The exact constructors and
graph equivalence are normative in the
[joint architecture protocol](../design/architecture-selection.md#finite-reproducible-candidate-universe).
The physical side contains all frozen compatible `T1`–`T8` combinations, not
only methods expected to fit R0.

## Guardrail-constrained Pareto-then-lexicographic survivor rule

Before candidate eligibility, reproduce `R_LEGACY_CONTROL` under the sealed
current-comparator predicate and evaluate every named historical artifact under
its separate comparator-eligibility predicate. The control is not a V2
candidate, receives no physical-profile product, and never enters Pareto or
lexicographic selection. A historical artifact supplies identity/context only
unless a newly attested matched run or exact reconstruction independently makes
it comparator-eligible; in particular Stage 4.6 is unavailable while
`R_stage46 = INCOMPARABLE`. A failed or changed required comparator leaves each
dependent relative objective unresolved, so every candidate requiring that
objective is ineligible.

Unless a different complete total rule is owner-approved and preregistered in
Phase 0, Phase 1A applies this procedure exactly:

1. **Eligibility.** Reject an incomplete card, unrealized pair, invalid result,
   unresolved cost/fault cell, compile failure, topology hard-gate failure, or
   any later hard-gate failure. Generate and reconcile the complete direct-
   local-dependency/source-disposition ledger before performance. No later
   score can restore eligibility.
2. **Comparable endpoints.** For each objective, use only the Phase 0-sealed
   value. A minimized stochastic objective compares its frozen upper confidence
   endpoint; a maximized stochastic objective compares its frozen lower
   confidence endpoint. An exact deterministic objective compares its frozen
   scalar. The confidence level/method, unit, workload aggregation,
   transformation, numerical resolution, and direction are part of the seal.
   A missing, non-finite, or otherwise non-comparable required value is an
   eligibility failure; it is never imputed.
3. **Hard guardrails.** Apply every absolute and relative threshold as a
   pass/fail constraint. Improvement on one objective cannot compensate for a
   guardrail failure on another.
4. **Pareto treatment.** Over the complete frozen endpoint vector, eligible
   profile `A` dominates eligible profile `B` exactly when `A` is no worse in
   every objective after applying its sealed direction and strictly better in
   at least one. Remove dominated profiles. This Pareto pass is an elimination
   rule, not an unrecorded weighting rule.
5. **Lexicographic resolution.** Compare the remaining profiles by the exact
   Phase 0-sealed ordered objective list, stopping at the first unequal frozen
   value. Lower wins a minimized objective and higher wins a maximized
   objective. Units, transformations, numerical resolution, and confidence
   endpoints may not be changed after results are visible.
6. **Unique result or no result.** Zero eligible profiles yields `NO_WINNER`.
   One unique first profile after the frozen ordering is the provisional
   selection-partition result. Any tie, incomparability, or Pareto
   non-dominance that the preregistered ordering does not uniquely resolve also
   yields `NO_WINNER`; there is no coin flip, committee choice, or post-result
   tiebreaker.

A different lexicographic order or a product-utility rule is permitted only if
Phase 0 freezes it before candidate results. A product-utility rule must freeze
the complete formula, all weights, normalization bases, units, directions,
confidence endpoints, numerical resolution, and exact tie/non-dominance
outcome. An incomplete alternative is not a selection rule and therefore
yields `NO_WINNER`.

## Candidate card and proof bundle

Every selectable candidate publishes one immutable card **before execution**. A card is
ineligible unless it is I/O-complete and structurally complete. It first binds
the normalized topology and source realization: every authority/writer/effect,
package/process/deployable, call, privilege/helper, Cargo feature, and direct
local dependency; compile commands for every frozen target; and exactly one
`KEEP`, `DELETE`, `MOVE`, or `NEUTRAL_DTO` disposition for every generated
consumer/source row. It then contains all of the following:

1. the named standard primitive or prior-art basis, exact version, claimed
   adaptation, and the smaller incumbent that it must defeat;
2. exact typed inputs and outputs for every operation and branch, including
   error results, plus explicit preconditions and postconditions over durable
   state, volatile state, custody, resources, and externally visible effects;
3. exact bytes/grammar, persistent and volatile states, legal transitions,
   barriers, recovery election, and the sole owner of every state and
   transition; identity claims distinguish candidate digest from accepted
   no-alias `StateId`, require exact canonical-byte comparison for an occupied
   candidate, type unequal bytes as `T03_REJECTION / STATE_ID_COLLISION`, and
   specify bounded no-disclosure cleanup/replay/recovery behavior;
4. **I/O-complete pseudocode** for every operation and branch. It must name, in
   execution order, every lookup/list/stat/open/read/allocation/write/flush/
   sync/parent-sync/replace, lock and queue action, runtime-effect dispatch, retry,
   join/drain, cleanup, credit-visibility transition, and return. A helper is
   permitted only when its own complete contract is included or referenced by
   content hash; a phrase such as “persist,” “recover,” “validate,” or “clean
   up” cannot hide work or a crash cut;
5. one exact linearization or commit point for every success and non-success
   result, all safety invariants, and an inductive preservation argument for
   each pseudocode transition;
6. progress and fairness obligations: every blocking point, admission order,
   starvation bound, cancellation/deadline behavior, retry variant, finite
   retry bound, and typed result on exhaustion. An unbounded retry, a
   scheduler-dependent fairness claim, or “eventual” cleanup is ineligible;
7. a complete `COST_RECORD` schema from the storage model for every operation,
   semantic branch, payload class, target, and participating authority. Each
   record supplies best, expected, worst, and amortized envelopes for every
   applicable `C(op)` and `V(op)` dimension. The expected envelope freezes its
   probability/workload/contention/cache/fault distribution and assumptions;
   the amortized envelope names a finite sequence and potential/accounting
   proof. A pre-execution result slot may be `[OPEN:<owner>]` or
   `[TO_MEASURE:<metric>]` only under the resolution rule below;
8. the complete matrix `O × T × applicable F` from the
   [normative terminal and fault registry](../design/requirements.md#normative-terminal-and-fault-registry),
   including cleanup/reaper faults nested in every applicable cell. Each cell
   names the join/drain, synchronization, custody, cleanup, recovery, and
   capacity-visibility owners and numeric convergence horizon. Recovery and
   restart, stale revision and stale generation, and duplicates before/after
   every named boundary remain distinct cells. A pre-execution result slot may
   be open only under the resolution rule below. `UNREACHABLE` is allowed only
   with an executable falsifier that fails if the path becomes reachable;
9. every persisted crash cut before and after every durability, dispatch,
   custody, cleanup, and credit-visibility action; the exact bytes/state visible
   at that cut; and the authority that retains custody and converges it after
   recovery;
10. coupling to every other tournament and every prohibited combination;
11. semantic, corruption, crash, concurrency, migration, and runtime-neutrality
    falsifiers;
12. bounds and automatic cleanup for every authority-owned nondurable cache or
    scheduler hint, with zero idle per-sandbox/session residency unless a fixed
    shared baseline is separately justified and frozen;
13. a source-to-binary inventory of `unsafe`, FFI, syscalls/`ioctl`, `mmap`,
    direct I/O, filesystem assumptions, and helper processes;
14. max-over-time scratch accounting for streaming, reference-switch, in-place,
    and write-new-before-delete-old behavior; no generic `2x` factor and no
    selected external-sort assumption;
15. an executable verification plan and artifact schema covering a finite-state
    or model-checking model, property tests, differential tests, and fuzzing.
    The semantic oracle must be independently implemented from the candidate;
    every failure must preserve its seed, schedule/fault trace, raw input, and a
    mechanically minimized counterexample plus one-command reproduction;
16. deletion proof and why a smaller incumbent does not suffice; and
17. complete source/build/test/evidence provenance.

### Result-slot closure before eligibility

`OPEN` and `TO_MEASURE` exist only in the immutable pre-execution card. Each
such slot must already name one owner, the frozen proof or measurement command,
inputs, distribution, unit, statistic, sample/stopping rule, artifact schema,
and the condition that blocks eligibility. It is not a waiver or a scored
value.

Before hard-gate eligibility or scoring, every applicable cost field and every
`O × T × applicable F` cell must resolve to exactly one of:

1. a proved expression or mechanically enforced finite bound, with derivation
   and executable falsifier;
2. only where Phase 0 permits empirical expectation, the frozen expected-value
   statistic with raw receipt and all declared assumptions; or
3. `N/A` or `UNREACHABLE` with an accepted proof and executable falsifier.

Best-, worst-, and amortized-case envelopes require proof or enforcement. A
finite run, maximum observed sample, confidence endpoint, or absence of a
failure is not a worst-case or amortized bound. Expected measurements cannot be
substituted into those fields. Any unresolved, non-finite, assumption-drifted,
or misclassified slot makes the complete joint profile `INELIGIBLE`; if no
profile remains, the only result is `NO_WINNER`.

An accepted evidence bundle contains the sealed card and executable pseudocode,
candidate and independent-oracle source hashes, model/property/differential/
fuzz commands and raw results, coverage of every declared transition and
`O × T × applicable F` cell, minimized counterexamples for every observed
failure (including fixed failures), cost records with derivations and raw
measurements, a generated source/dependency/disposition ledger, successful
frozen-target compile receipts, and a machine-checkable card-to-artifact trace.
A prose proof, test-plan promise, happy-path test, or candidate-derived “oracle”
is not accepted evidence. Missing one required artifact rejects the card before
scoring; it cannot be waived by performance.

An unnamed “another method” is not an eligible candidate until its card is
sealed. Adding a candidate after seeing results triggers the invalidation rule.

## Hard-gate order

A joint profile is rejected at the first failure:

1. finite-universe membership, complete card, generated source/dependency/
   disposition closure, and successful frozen-target compilation;
2. topology admissibility: unique writers/effect/resource owners, lawful call
   and dependency direction, no duplicated truth or policy, and complete
   helper/privilege/process custody;
3. retained product semantics;
4. canonical identity, bounds, corruption rejection, and collision-safe
   admission: equal qualified facts produce identical canonical bytes and
   candidate IDs; an accepted ID denotes exactly one canonical byte string;
   occupied unequal bytes create no alias/root/mapping/index/revision/custody/
   capacity fact; forced-collision qualification covers publish, import,
   recovery, index rebuild, reference-API ingress, and last-root behavior; and
   accepted reference-only transitions consume only previously admitted
   authorized bindings with zero immutable-payload I/O;
5. selected-state-authority-local durable crash recovery and every cross-
   authority crash/effect cut under that candidate's own realized graph;
6. simultaneous resource/capacity feasibility;
7. the complete unsafe/FFI/syscall/filesystem/helper-process audit;
8. runtime-neutral dependency, static rejection before allocation, and bounded
   hidden-realization cleanup for data-dependent incompatibility;
9. actual-source migration and fleet fencing;
10. minimal state, surface, and operational ownership; then
11. matched performance and complete-system cost.

Performance never compensates for an earlier failure. A profile with a strong
microbenchmark but a missing crash state is rejected, not “conditionally
selected.”

## Joint tournaments

Run `T1` through `T8` as defined in the registry. Candidates are evaluated as
compatible complete profiles: directory/content grammar, digest, physical
representation, index/selector, publication, reachability/replacement,
retirement/recovery, replay/effect custody, and runtime realization must close
jointly. Replay candidates must prove authenticated namespace/key/semantic-
descriptor binding, conflict non-disclosure, pruning safety, and the accepted
authorization-revocation ordering. Do not select each fastest row and combine
incompatible winners.

`T5` must include a standard-first small-publication candidate whose sealed card
orders: freeze and attest; bounded in-process source capture; streaming
canonicalization, hashing, staging, and verification outside the final gate;
then a short origin-revalidation and selection gate. That final gate invokes no
subprocess, performs no unmount/remount, performs no immutable payload read,
write, or copy, and performs no runtime allocation, activation, capture,
disposal, or other lifecycle work. The candidate is timed and charged end to
end through durable response, cleanup, and capacity visibility; shortening the
gate cannot hide work moved before it. It remains merely eligible until the
complete profile passes the holdout and an ADR is accepted.

MCTS or any other rollout/search policy remains outside all eight storage
tournaments as scheduler policy. If an evaluation uses it, inactive rollouts
retain only one immutable root reference plus bounded metadata; active mutable
realizations are finite and admitted under the full vector; pruning cancels and
joins work, disposes or durably quarantines the exact realization, and releases
charges only after synchronized cleanup and capacity visibility. Phase 0 must
seal the exact product oracle before any implementation: immutable checkpoint
parent; sibling/parent write isolation; deterministic ancestry, policy, and
result identities; stale-parent behavior; winner, child, and sibling fate; no
merge/rebase; finite breadth/depth/concurrency with admission, fairness, and
typed overload; cancel/prune/timeout/crash/restart cleanup; purpose-independent
zero selected-state immutable payload I/O and last-root rules for `commit_fork`; and inactive
fan-out at 1/2/4/16/64/accepted maximum plus admitted active-rollout evidence.

The laboratory can use temporary code outside production packages. No
production crate depends on it. After 1A accepts `H_PROFILE`, the winner is
reimplemented through ordered Phase 1 non-live subgates: `1B H_FMT`, `1C
Hstore`, `1D Hpermanent`, `1E H_PRECUTOVER`, then `1F Hqual` over byte-identical
`H_PRECUTOVER`.
Laboratory source and raw evidence remain separately sealed.

## Standard-first novelty rule

For any claimed new algorithm, the candidate card must show:

1. a named standard primitive and version;
2. its implementation/model under the same fixtures and hard gates;
3. the exact failing requirement and counterexample;
4. the smallest adaptation attempted;
5. why composition with another selected standard primitive does not solve it;
6. added persistent/crash/resource states; and
7. independent review of novelty and necessity.

Without that record, the “novel” candidate is ineligible. The burden-of-proof
target is zero genuinely novel algorithms; a nonzero result is acceptable only
when the complete record above survives independent review.

## Selection, holdout, and no-winner result

Use the selection partition for elimination and parameter choice, then compute
the unique provisional result with the frozen survivor rule. If that result is
`NO_WINNER`, stop without opening the holdout. Otherwise run only the
provisional profile and the preregistered control/comparator measurements needed
by its acceptance predicate on the untouched holdout, once, according to the
sealed access rule. A holdout failure returns `NO_WINNER`; it is not a tuning
input, and no runner-up is promoted without a new Phase 0 seal and a new
uncontaminated holdout.

Phase 1A produces either:

- one accepted globally closed `H_PROFILE` binding topology, physical profile,
  compile-valid source, exact graphs/counts, control/comparator receipts, all
  losers/falsifiers, and owner-accepted ADRs; or
- `NO_WINNER`, leaving writable V2 closed and documenting which requirements or
  candidates need owner-approved reconsideration.

There is no obligation to select a profile. No runtime strategy menu, per-
workload format, or mutually incompatible “best parts” may escape the lab.

## Production-equivalence rule

Selection evidence authorizes implementation, not live qualification. Gates
1B–1F must demonstrate that production format/selected-state code, application/
current-Linux integration, source/dependency graph, and exact `H_PRECUTOVER`
have the same grammar, durability cuts, resource boundary, and complete-system
behavior. A mismatch reopens Phase 0 and the joint tournament; it is not waived
as an implementation detail. Only after `1F Hqual` names byte-identical
`H_PRECUTOVER` may Phase 2 begin: `2A` exact-artifact cutover, `2B` bounded
observation, `2C` compatibility retirement and `H_RELEASE` construction, then
`2D` fresh affected-scope requalification and release. Optional destructive
legacy deletion remains outside the phase DAG.

## Evidence record

Seal the exact repository/tree, dirty-state declaration, build/dependency
metadata, runner/environment, input and holdout hashes, commands, exit codes,
raw samples, phase traces, resource observations, invalid samples and reasons,
statistical calculations, candidate/decision versions, and review sign-off.
Reports link to artifacts; prose never substitutes for them.
