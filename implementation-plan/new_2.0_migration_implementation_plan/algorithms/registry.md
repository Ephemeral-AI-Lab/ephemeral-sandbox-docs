---
status: draft-planning-inventory
authority: method-decision-registry
selected-physical-method-count: 0
mandated-novel-algorithm-count: 0
proven-novel-algorithm-count: 0
joint-profile-selection-execution-status: NOT_RUN
accepted-joint-profile-winner-count: 0
accepted-architecture-winner-count: 0
accepted-physical-method-winner-count: 0
historical-workbook-declared-custom-mechanism-count: 6
historical-workbook-declared-custom-algorithm-count: 5
historical-workbook-declared-custom-crash-protocol-count: 1
owner-prompt-audited-functional-family-count: 21
actual-open-decision-count: not-yet-bounded
---

# Method decision and result registry

## The count that matters

This plan currently produces **zero new algorithms**:

- mandated genuinely novel algorithms: **0**;
- proven genuinely novel algorithms: **0**;
- selected physical method winners: **0**;
- historical-workbook-declared custom mechanisms reopened: **6**—five
  algorithms and one crash protocol; and
- owner-prompted audited functional families retained for omission checking:
  **21**.

The source distinction is exact. `pmss_algorithms.md:172-190` historically
labels six project-owned mechanisms: `C1`, `C2`, `C3`, `S1`, and `S3` as
algorithms, with `S2` as the sole custom crash protocol. Those names are
evidence/index labels only: this plan mandates none, proves none novel, and
selects none. The 21-family census instead originates
in the owner-supplied hostile-review prompt at `pasted-text-1.txt:488-494`; the
harsh audit calls it “the prompt's 21-item census” and expands it at
`pmss-harsh-minimal-audit.md:935-959`. The registry IDs below disposition those
21 audited families so none is lost. They are not 21 workbook rows, inventions,
selected methods, or a proven complete count of open decisions. They mix
product results, standard data-structure choices, conditional physical work,
and lifecycle transition proofs.

The current Phase 1A joint-profile tournament status is **`NOT_RUN`**, and the
accepted joint, architecture, and physical-method winner counts are **0**.
`NO_WINNER` is a valid formal result only after the sealed Phase 1A tournament
runs and no complete profile passes; it must not be used to make an unexecuted
selection look conclusive. Nothing in the historical POC or an open registry
row supplies a winner.

The audit also found cross-cutting choices—digest grammar, selector topology,
effect custody, runtime-effect binding, allocation/capture routing, and fleet
fencing—outside the 21-family prompt census. Phase 0 must bound the actual
decision inventory before Phase 1A selection; this draft does not manufacture
a false exact number.

The target novelty count is zero. A novel method is eligible only after its
owner records which standard primitive was implemented or modelled, which hard
requirement it failed, the smallest adaptation considered, and why the new
mechanism reduces total state/failure surface. Novelty earns no score.

`R_LEGACY_CONTROL` is a compile-valid evidence-only current/legacy control, not
a candidate, method winner, or algorithm. Its sealed measurements supply only
preregistered baseline endpoints and runner/corpus drift detection. It is never
counted among the zero selected winners or placed in the Pareto pool.

## Disposition of the 21 owner-prompted audited functional families

`AF` means **audit family**, not algorithm. The prefix is intentionally distinct
from the zero-count set of selected or novel algorithms.

| ID | Required result or product effect | Classification now | Selection/proof path | Deletion or standard-method question |
|---|---|---|---|---|
| `AF-001` | Canonical directory construction and lookup | open method decision | `T1` | Can a standard immutable ordered/trie representation meet byte, depth, lookup, churn, and scratch bounds? |
| `AF-002` | Canonical regular-content/extent sequence | open method decision | `T2` | Compare whole-file, fixed-unit, rolling-boundary, or jointly grouped standard forms; no FastCDC assumption. |
| `AF-003` | Exact attribution, only if retained | conditional product/method decision | `DEC-001`, then `T3` | Delete with approved API removal, or prove an exact bounded standard method. |
| `AF-004` | Sparse physical lookup/index update | open method decision | `T4` | Does a standard immutable ordered structure meet cache-off I/O and crash bounds? |
| `AF-005` | Dense lookup/index construction | conditional method decision | `T4` | Delete if one bounded sparse method dominates; otherwise prove the crossover and temporary capacity. |
| `AF-006` | Complete publication under OCC | open method decision | `T5` | Include the small-publication candidate: freeze/attest; bounded in-process capture; stream/canonicalize/hash/stage/verify outside the final gate; then short origin revalidation/selection. The final gate has no subprocess, unmount/remount, selected-state immutable payload I/O, or runtime lifecycle work. Compare complete end-to-end cost, not gate time alone. |
| `AF-007` | Canonical/physical object representation | open method decision | `T2` | Prefer the smallest closed grammar; any dependency edge must repay closure/recovery cost. |
| `AF-008` | Portable materialization | open method decision | `T8` | Evaluate direct verified streaming as the minimum-surface candidate; any acceleration must beat it while remaining disposable and exact. |
| `AF-009` | Exact semantic reachability | open method decision | `T6` | Use bounded scans/merge/traversal before inventing persistent refcounts or live caches. |
| `AF-010` | Physical dependency closure | conditional method decision | `T6` | Delete for an edge-free representation; otherwise prove a finite standard closure pass. |
| `AF-011` | Dependency-eliminating conversion | conditional fused work | `T6` | Delete for edge-free storage; otherwise keep inside the single replacement workflow. |
| `AF-012` | Replacement victim choice | policy inside one workflow | `T6` | Start with the smallest deterministic bounded ordering; no independent service or policy menu. |
| `AF-013` | Immutable replacement workflow | open method decision | `T6` | One owner must cover trace, rewrite, selection, retirement, debt, and recovery. |
| `AF-014` | Safe old read-view retirement | open method decision | `T6` | Compare bounded volatile read-view tokens/join proof with any other finite candidate; wall-clock expiry is not custody proof. |
| `AF-015` | Exact finite request replay, semantic request binding, and anti-replay | open method decision | `T7` | Select a bounded standard authenticated sequence/window/freshness structure from the real product horizon. It must bind namespace/key to one immutable normalized descriptor, reject mismatches without prior-state disclosure, and prevent pruning from making an expired identity fresh; no fixed lane count is assumed. |
| `AF-016` | Fail-closed startup recovery | open method decision | `T6` | Prove a bounded no-ready-before-census procedure with exact reserve; encoding follows the selected state representation. |
| `AF-017` | Named checkpoint | required semantic transition, not a new algorithm | API/model proof | Reuse one metadata/root transition naming an accepted no-alias immutable closure; for the whole operation, total selected-state immutable payload bytes read, written, and copied and new root-private closure bytes are all zero. An occupied candidate digest first requires exact-byte admission; unequal bytes take the typed collision terminal and never enter this fast path. |
| `AF-018` | Fork and `commit_fork` | required semantic transition with one open pin decision | API/model proof plus `DEC-009` | Reference-only fork and same-accepted-`StateId` winner transfer have total selected-state immutable payload bytes read, written, and copied equal to zero and zero root-private closure bytes; compare a bounded exact scan/revalidation with an index without preselecting either. Each candidate names every semantic-root, pin/backup-hold, reader/read-view, custody, and candidate-specific row population it scans or indexes and gives finite exact best, expected, worst, and amortized metadata-I/O, update, memory, synchronization, and contention bounds as functions of the applicable cardinalities; `N/A` requires a reachability proof. No generic transaction API. Forced-collision testing is a qualification seam, not an audit family, API, or algorithm. |
| `AF-019` | Rollback | required semantic transition, not a new algorithm | API/model proof | Reuse an authorized OCC head transition; rollback-to-existing accepted state has total selected-state immutable payload bytes read, written, and copied equal to zero and no replay/history mechanism. Candidate-digest collision admission remains outside this COW path. |
| `AF-020` | Session close | required cross-authority transition | API/effect model plus `T7`/`T8` | Derive minimum durable custody from every disposal crash cut; do not freeze four fields or two commits by assertion. |
| `AF-021` | Semantic root deletion | required semantic transition, not a new algorithm | API/model proof plus `T6` | Remove semantic ownership only; exact shared reclamation happens later and grants no speculative credit. |

`REQUIRED` means the public result survives unless an accepted product change
removes it. It never implies a bespoke implementation or separately owned
workflow.

## Proof-complete selection requirement

No audit-family row can become `SELECTED` from prose, partial pseudocode, a
benchmark, or a happy-path implementation. Its complete candidate card and
accepted evidence bundle must satisfy the
[method-selection proof contract](selection-protocol.md#candidate-card-and-proof-bundle):
exact inputs/outputs/preconditions/postconditions; I/O-complete pseudocode;
linearization and commit points; invariants; finite progress, fairness, and
retry rules; every persisted crash cut and custody owner; and executable
model/property/differential/fuzz evidence against an independent oracle with
mechanically minimized counterexamples. These artifacts describe a proof
obligation, not a new algorithm family, so the count remains **0 / 0 / 0**.

## Exhaustive cost-record crosswalk

The functional census and resource proof ledger are one-to-one. Each ID below
must have separate `COST_RECORD` instances for every operation, target,
semantic branch, payload class, participating authority, terminal path, and
applicable injected fault under the schema in
[Storage model](../design/storage-model.md#common-cost-record).
Terminal paths and fault cuts are not recopied here: the sole enumeration is
the [normative terminal and fault registry](../design/requirements.md#normative-terminal-and-fault-registry),
and evidence covers `O × T × applicable F`. Before eligibility, best, worst,
and amortized envelopes require proved or mechanically enforced bounds; only an
expected field may use a Phase-0-permitted empirical statistic under its frozen
distribution/procedure and raw receipt. `N/A` requires proof. `NOT_RUN` means
the pre-execution result slot is unresolved and therefore ineligible for
scoring; it does not license a blank field, observed maximum as a bound, or an
`OPEN` value in an accepted bundle.

| Audit family | Required cost-record subject | Current evidence |
|---|---|---|
| `AF-001` | `COST-AF-001` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-002` | `COST-AF-002` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-003` | `COST-AF-003` if retained; otherwise deletion proof | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-004` | `COST-AF-004` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-005` | `COST-AF-005` if eligible; otherwise deletion proof | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-006` | `COST-AF-006` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-007` | `COST-AF-007` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-008` | `COST-AF-008` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-009` | `COST-AF-009` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-010` | `COST-AF-010` if representation has dependency edges; otherwise `N/A` proof | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-011` | `COST-AF-011` if conversion exists; otherwise `N/A` proof | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-012` | `COST-AF-012` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-013` | `COST-AF-013` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-014` | `COST-AF-014` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-015` | `COST-AF-015` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-016` | `COST-AF-016` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-017` | `COST-AF-017` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-018` | `COST-AF-018` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-019` | `COST-AF-019` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-020` | `COST-AF-020` | `NOT_RUN`; unresolved pre-execution slots, ineligible |
| `AF-021` | `COST-AF-021` | `NOT_RUN`; unresolved pre-execution slots, ineligible |

## Tournament crosswalk

| Tournament | Coupled questions | Why they cannot be selected independently |
|---|---|---|
| `T1 — canonical directory` | `AF-001`, identity grammar, decoder limits | byte shape fixes lookup depth, changed-object churn, and validation cost |
| `T2 — content and representation` | `AF-002`, `AF-007`, digest/domain separation | chunk boundaries, object edges, physical reuse, recovery, and identity cost move together |
| `T3 — attribution` | `AF-003` if `DEC-001` retains blame | duplicate/move semantics and storage/pass cost must be judged with the product result |
| `T4 — physical lookup and selection` | `AF-004`, `AF-005`, selector topology | update/build costs and crash recovery share the physical commit profile |
| `T5 — publication` | `AF-006`, capture stability, OCC, selected representation/index | a fast pass count is meaningless without source stability, final selection, and conflict behavior |
| `T6 — reachability, replacement, retirement, recovery` | `AF-009`–`AF-014`, `AF-016` | representation edges, reader custody, reserve, debt, and startup convergence form one resource/crash system |
| `T7 — replay and effect custody` | `AF-015`, request outcomes, ambiguous runtime effects | replay windows and deduplication determine whether recovery can safely repeat or only report uncertainty |
| `T8 — realization and runtime-effect binding` | `AF-008`, allocation/activation/capture/disposal routing | portable facts, opaque binding generations, runtime crash cuts, and cleanup must form one runtime-neutral contract |

The semantic transitions in `AF-017`–`AF-021` are verified through the public
API and state-machine gates. They use tournament winners but are not themselves
scored as algorithms.

## Cross-cutting decisions outside the 21-family review census

Phase 0 must add explicit decision records or prove fusion for at least:

- typed digest and domain-separation grammar (`DEC-005`);
- authoritative-revision/selector physical topology;
- aggregate encoding and transaction boundary;
- authenticated semantic request binding, conflict non-disclosure, pruning
  safety, and authorization linearization/revocation (`DEC-018`);
- separate durable request-outcome and effect-custody lifetimes, plus ambiguity
  and quarantine representation;
- opaque runtime-allocation binding and restart routing;
- terminal and fault closure for the complete normative
  `O × T × applicable F` registry, including cleanup/reaper failure nested in
  every applicable terminal cell and executable `UNREACHABLE` falsifiers;
- resource-claim/reconstruction policy, bounded authority-owned nondurable cache
  policy, and measurable cleanup plateau;
- MCTS/search policy as an external scheduler: inactive rollouts retain only one
  immutable root plus bounded metadata, active mutable realizations are finite
  and admitted, and prune cleanup is exact;
- source-to-binary inventory of `unsafe`, FFI, syscalls/`ioctl`, `mmap`, direct
  I/O, filesystem assumptions, and helper processes;
- max-over-time scratch accounting, with `2x` accepted only for a proved
  write-new-before-delete-old overlap and external sort still unselected; and
- migration generation/fleet-writer fence implementation.

This list demonstrates why treating the review prompt as “21 open algorithms”
or a complete decision inventory would be unsound; it is not declared complete.

## Selection transition and final accounting

A method becomes `SELECTED` only as part of the one jointly accepted
`H_PROFILE`: the finite selectable-topology × physical universe and complete
decision rule are frozen; the evidence-only control and named comparators pass
their own sealed eligibility predicates wherever a relative endpoint depends on
them; each applicable result slot resolves; every eligible
compile-valid pair runs under the sealed protocol; every hard gate passes; the
untouched holdout is used exactly as declared; raw evidence is sealed; and the
topology and method ADRs are accepted together. Candidate code, pseudocode,
Stage 4.6 code, and benchmark prose are non-authoritative before then.
Stage 4.6 is currently `INCOMPARABLE`: its receipts supply identity/context but
no selection endpoint. Any relative cell that depends on it remains unresolved
unless a separately sealed attested rerun or exact reconstruction passes the
frozen eligibility predicate.

Phase 1A reports, without overlap:

1. required product/result rows retained;
2. physical method decisions selected;
3. standard primitives reused unchanged;
4. standard primitives narrowly adapted;
5. genuinely novel algorithms, if any, with failed-standard evidence; and
6. rows and candidate code deleted.

Until that process runs and produces one uniquely selected and accepted
`H_PROFILE`, the registry remains `NOT_RUN` with 0 selected, 0 mandated novel,
and 0 proved novel. After execution, the formal result is exactly one accepted
joint profile or `NO_WINNER`.

No branch-dependent `18/17` or `21/19` function/workflow count is retained:
those numbers assumed unselected representations and ownership boundaries.
