# Decision ledger

Status: **DRAFT — NO ACCEPTED ALGORITHM DECISIONS**

## Open decisions

| ID | Question | Blocking phase | Required evidence |
|---|---|---:|---|
| `DEC-001` | Is exact `file_blame` a retained product requirement? | 0 | caller inventory, compatibility impact, product-owner decision |
| `DEC-002` | Does any mutable runtime-effect responsibility require a new ownership unit or deployable? | 1A | exact current-owner mapping plus privilege/threat/fault/scaling benefit large enough to pay for boundary/protocol/queue/retry/cgroup/latency/operations cost; otherwise keep direct in-process calls to existing owners |
| `DEC-003` | Which existing application/composition roots own management/runtime decisions, and what is the complete component/authority/process graph? | 1A | current call/dependency/deployment graph; durable writers, effect executors, semantic decision owners, migration-only authorities, cgroup scopes, and one-owner mapping |
| `DEC-004` | Where does the deletable temporary migration code unit/target/artifact live, and does it need a separate package? | 1A | actual legacy graph; generated source/package placement; compliance with the sole normative import dependency direction; executable deletion counterexample for any package; complete no-reference removal proof; fresh Phase 2D qualification; and separately signed post-release data-deletion scope |
| `DEC-005` | Which typed digest and domain-separation grammar wins? | 1A | standard-first security/portability evidence; independent golden vectors; exact candidate-digest admission with no-alias accepted identity; typed collision rejection; a qualification-only forced-collision seam covering publish, import, recovery, index rebuild, reference-API ingress, and last-root behavior; and proof that accepted reference-only transitions consume only previously admitted authorized bindings with zero immutable-payload I/O |
| `DEC-006` | Which complete directory/content/physical/index/selector profile wins? | 1A | all coupled joint-profile cards and global hard-gate/cost comparison |
| `DEC-007` | Which publication/finalization profile wins? | 1A | matched pass/I/O/fence/retry/crash/resource evidence |
| `DEC-008` | Which reachability/replacement/retirement/recovery profile and finite constants win? | 1A | capacity/debt/reader/crash/load/cgroup proof |
| `DEC-009` | Pin index or exact scan/revalidation? | 1A | Phase-0-bounded scale; the exact semantic-root, pin/backup-hold, reader/read-view, custody, and candidate-specific row populations touched; finite exact best, expected, worst, and amortized metadata-I/O, update, memory, synchronization, and contention bounds as functions of their applicable cardinalities; last-root race/model evidence; no presumption that work is independent of root count |
| `DEC-010` | What exact replay horizon/window/result profile satisfies the product contract? | 1A | caller retry horizon, concurrency, wrap, ambiguity, and resource proof |
| `DEC-011` | What observation and compatibility-retention horizon is sufficient before retirement/release? | 0 | longest retry/replay/restore/backup/audit/client-upgrade horizon plus operational risk decision, sealed before cutover |
| `DEC-012` | Which responsibility, component, authority, call-shape, package-direction, and deployment topology wins? | 1A | outcome-neutral joint tournament over the Phase-0-sealed finite universe: all five `A/S/N` accountability partitions; every compatible actual-source selected-state/pure-function placement; actual-package keep/delete/move, one-package deletion, multi-package fusion, and total-fusion families; R0 in-place witness; one-extracted-boundary and necessity-triggered families; legacy control; and every complete card submitted before the signed cutoff. Additions require deletion counterexamples; axes, equivalence, completeness, admissibility, dominance, cutoff, and tie-break are frozen before results |
| `DEC-013` | What local durability profile is actually supported? | 1A | filesystem/mount atomicity, synchronization, torn-write, ENOSPC, open-handle, backup, and topology evidence |
| `DEC-014` | What durable effect-custody and uncertainty model covers every mutable runtime operation? | 1A | operation-by-operation dispatch/dedup/retry/compensation/crash model |
| `DEC-015` | Where are finite selected-state and runtime-effect claims admitted and reconstructed before readiness? | 1A | begin with owner-local charges; compare any aggregate placement only from the actual acquisition graph; no standalone Governor unless every smaller shape fails a named invariant |
| `DEC-016` | Which atomic local token and fleet-control implementation proves the monotone generation fence? | 1A | every-writer inventory, atomic selection check, generation-bound acknowledgments, stale-writer tests |
| `DEC-017` | What exact V2 public-operation set, file-target contract, and no-session `file_write`/`file_edit` compatibility behavior wins? | 0 | pinned e497 catalog and caller inventory, legacy 26-row proposal mapping, exact request/result/error compatibility matrix, owner approval |
| `DEC-018` | Where does authorization linearize, and do later revocations affect already accepted bound requests before dispatch or disclosure? | 0 | one explicit snapshot or race-safe revocation-cutoff contract; ordering against bind/lookup/prepare/dispatch/terminalization/response; revoke-at-every-cut fixtures; security-owner approval |

Do not create an ADR merely to record an open question. Create one when a
complete cross-boundary, format, API, durability, migration, or irreversible
choice is ready for Proposed/Accepted/Rejected review.

## ADR index

No ADR exists yet. This is intentional. R0 proposes zero mandatory additions:
rewrite the existing LayerStack ownership home for complete immutable V2 and
reuse current application/runtime-effect owners. It adds no Store or aggregate
runtime seam, canonical module, coordinator, component, package, service,
process, deployable, port, trait, or facade by default. Every exact count,
admission placement, and physical method remains open. Production
implementation is blocked beyond Phase 0 until `DEC-012` is accepted.
R0 is not a package-count floor; a package-deleting fusion may be smaller and
must be evaluated under the identical Phase-0-frozen judge.

## ADR template

```markdown
# ADR-0001 — Decision title

Status: Proposed | Accepted | Rejected | Superseded

## Context

## Required invariants

Links to requirement/design IDs.

## Candidate choices

## Counterexamples and rejecting evidence

## Decision

Absent while Proposed.

## Why this choice wins

Hard gates first, then complete-system cost and simplicity.

## Consequences

## Migration and rollback effect

## Affected authorities

## Qualification evidence

## Supersedes / superseded by
```

Accepting an ADR requires updating the owning design document, algorithm
registry, traceability, phase gates, and migration/qualification impact in the
same commit. The ADR records why; the current design file remains the contract.
