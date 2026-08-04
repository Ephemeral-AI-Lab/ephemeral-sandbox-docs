# Rollout and branch orchestration

**Status:** explanatory view of the selected R0 architecture

**Authority:** [V2 PRD](../PRD.md) -> Phase 01 [selection input contract](../phases/01-choose-design/SPEC.md) -> selected [architecture output](../architecture_design.md)

**Purpose:** show how a caller may compose generic LayerStack-0 and runtime
operations into MCTS or agent rollouts without moving policy, scoring, or
runtime effects into storage.

This is a conceptual workflow, not a new rollout API. Exact Phase 04 calls,
branch counts, scoring algorithms, retry policy, and scheduling remain caller
choices. Historical Stage 4.6 evidence is `INCOMPARABLE`; this view makes no
benchmark, speedup, or performance-guarantee claim.

## Legend

```text
+----------------------+   permanent owner, component, or authoritative object
[temporary/private]        workspace, execution, staging, or cleanup state
---->                      ordinary call or data flow
- - ->                     diagnostic or cleanup flow; never selected authority
===>                       authoritative reference transition
-X->                       forbidden ownership or dependency

binding                     LayerStack-0-issued/revalidated AcceptedBinding
P(read/write/copy)          complete-Version payload byte I/O for that operation
[OUTSIDE STORAGE]           policy decision owned by the application/caller
[SELECTED R0]               locked Phase 01 ownership or storage rule
[DEFERRED]                  exact later-phase implementation detail
```

## Selected rollout composition

```text
  +-----------------------------------------------------------------------+
  | application / rollout caller                         [OUTSIDE STORAGE] |
  |                                                                       |
  | choose base, budget, branching, prompts/actions, retry policy,         |
  | MCTS tree policy, scoring, pruning, and eventual winner               |
  +---------------------------+-------------------------------------------+
                              |
                              | capture expected selected-head record
                              | (base binding, head revision)
                              v
                   +-------------------------+
                   | LayerStack-0            |        [SELECTED R0]
                   | selected-Version owner  |
                   +------------+------------+
                                |
                for each branch | CreateHeadIfAbsent(branch identity,
                                | Expected::Absent, base binding)
                                | P(read/write/copy) = 0/0/0
                                v
                     +-----------------------+
                     | Branch Head           |
                     | -> accepted base      |
                     +-----------+-----------+
                                 |
             materialize/read    | complete accepted Version
             (payload I/O is      | allowed on this workspace path)
                                 v
                    [private writable workspace] <---- workspace/effect owner
                                 |
                                 | execute action/tool/agent step
                                 v
                    [namespace + exec + live files] <--- runtime owners
                                 |
                                 | candidate portable filesystem facts
                                 v
                   +-------------+-------------+
                   | LayerStack V2 admission   |
                   | canonicalize + VersionId    |
                   | occupancy + full compare  |
                   | durable immutable payload |
                   +-------------+-------------+
                                 |
                                 | accepted binding
                                 v
                   +-------------+-------------+
                   | ReplaceHead               |
                   | Expected::Exact(branch) ->|
                   | accepted candidate        |
                   +-------------+-------------+
                                 |
                                 | outcome facts / accepted binding
                                 v
  +------------------------------+----------------------------------------+
  | application / rollout caller                         [OUTSIDE STORAGE] |
  | score outcomes; update tree; continue, prune, or choose winner         |
  +------------------------------+----------------------------------------+
                                 |
                                 | winner binding + expected selected-head
                                 v
                   +-------------+-------------+
                   | one store transition gate |
                   | revalidate binding         |
                   | compare complete expected  |
                   | selected-head record       |
                   +-------------+-------------+
                                 |
               stale mismatch    | current record equals expected
               -> clean OCC loss |
               (no merge/rebase) v
                   +-------------+-------------+
                   | atomic complete head       |
                   | record replacement         |  <=== OCC linearization
                   +-------------+-------------+
                                 |
                                 v
                         selected winner

  loser Branch Heads/workspaces ----- cleanup by owning caller/runtime/store
                                      - - -> RemoveHead(Expected::Exact(head))
                                      - - -> eventual safe retirement
```

The diagram represents every Branch by a Head because Branch movement is
mutable and therefore must use the one Head OCC mechanism. LayerStack-0 need
not know that the Head participates in a rollout. A caller may score before
durable candidate admission or use a different number of Branch Heads,
provided the same ownership and publication laws hold. Phase 04 owns that
product-level composition.

For a rollout that creates `N` Branch Heads naming an already accepted base,
those `CreateHeadIfAbsent` operations perform aggregate selected-payload bytes read = `0`, written =
`0`, copied = `0`; the cost is bounded reference metadata, not `N` complete
payload operations. If execution produces `K` distinct complete canonical
outcomes that the caller chooses to admit, admission may create up to `K` new
complete immutable payloads. Equal outcomes converge on one physical payload
after exact occupied-ID byte comparison. R0 does not promise that arbitrary
distinct outcomes share blocks, chunks, or deltas.

## Walkthrough

1. The application captures the complete selected-head record before it starts
   work. The expected value contains both the accepted binding and the head
   revision; a digest alone is not an OCC token.
2. Each fork creates a new Branch Head with `CreateHeadIfAbsent(...,
   Expected::Absent, binding)`. A retry validates the already-present complete
   record; it never generically retargets a Root. The reference-only fork has
   complete-Version payload bytes read = 0, written = 0, copied = 0 and may
   perform bounded reference metadata, coordination, and durability-fence I/O.
3. The workspace owner materializes or otherwise exposes the accepted complete
   Version as a private writable runtime view. This path can read payload bytes;
   it is deliberately not the zero-payload reference path.
4. Namespace, mount, OverlayFS, exec, and live-file mutation remain with their
   current runtime-effect owners. Those facts do not enter portable Version
   identity.
5. A branch result enters the generic Candidate-admission path. LayerStack-0
   derives identity from the complete portable Version facts, performs occupancy and
   full-canonical-byte comparison, and makes a new payload durable and
   immutable before any reference can name it.
6. The application receives outcome facts and accepted bindings. It owns
   scoring, MCTS policy, branch expansion, pruning, retries, and winner choice.
7. Selecting an already admitted winner is `ReplaceHead(Expected::Exact(...),
   winner_binding)`. LayerStack-0 revalidates the accepted binding and performs
   one complete-record OCC replacement. A stale expected Head loses without
   merge or rebase; the accepted losing payload remains immutable truth and is
   accounted as a bounded accepted orphan until safe retirement.
8. The caller removes loser Branch Heads with
   `RemoveHead(Expected::Exact(...))` and releases runtime resources. Payload
   retirement is not immediate deletion: LayerStack-0 first proves that no
   durable Root/Head or bounded read custody still needs the payload.

## Why the separation matters

The left panel below is a **correctness-invalid hypothetical**. It is not a
claim about the current e497 implementation or any historical system.

```text
FORBIDDEN ALTERNATIVE -- NOT HISTORICAL

 +---------------------------------------------------------------+
 | rollout-aware Version engine                                |
 | owns MCTS tree + prompts/actions + scoring + winner choice    |
 | owns workspace/mount/exec lifecycle + retry policy            |
 | admits payload and publishes selected head                    |
 +---------------------------------------------------------------+
             |                      |
             +-- policy authority --+-- runtime-private effects
                        mixed with selected-Version truth

 Problems:
   * violates hard rule 7: MCTS/rollout policy is inside storage;
   * moves runtime-private facts toward portable identity/truth;
   * joins failure domains and privileges without a necessity case;
   * makes a storage retry capable of changing a policy decision;
   * obscures the single selected-Version transition point.


SELECTED R0 -- ARCHITECTURE DECISION

 +----------------------+      generic calls      +----------------------+
 | application caller   | ----------------------> | LayerStack-0          |
 | policy, score, winner | <---------------------- | identity, admission, |
 | expected-head capture|     results/bindings     | roots, heads, OCC     |
 +----------+-----------+                          +----------+-----------+
            |                                                 |
            | runtime work                                    | immutable
            v                                                 v
 +----------------------+                          +----------------------+
 | workspace/namespace/ |                          | accepted complete    |
 | exec effect owners   |                          | Version payloads     |
 +----------------------+                          +----------------------+

 LayerStack-0 can reject an invalid or stale transition, but it cannot score a
 branch, choose a winner, silently rebase, or run the rollout.
```

## Authority and failure ownership

| Concern | Owner | On failure |
|---|---|---|
| Branching/MCTS policy, scoring, winner choice | Application/rollout caller | Caller may stop, prune, or retry from a newly captured head; storage does not decide. |
| Auth and request ordering | Existing application owner | Reject or sequence before invoking the selected-Version transition. |
| Branch reference transition | LayerStack-0 | Clean OCC loss or fail closed; no silent merge/rebase. |
| Candidate identity and collision handling | Phase 02 pure identity under LayerStack-0 control | Reject noncanonical/over-limit input or occupied-ID byte mismatch. |
| Candidate admission and immutable payload | LayerStack-0 | No reference to incomplete payload; recognizable private debt is recoverable. |
| Workspace, OverlayFS, mount, namespace, exec | Existing runtime-effect owners | Tear down private effects; they are not portable selected truth. |
| Loser Branch-Head removal and retirement request | Caller initiates `RemoveHead(Expected::Exact(...))`; LayerStack-0 validates | Cleanup is retryable; retirement waits for all Heads, fixed Roots, and custody proof. |
| Diagnostics | Observability readers | Report outcomes and counters; never approve a transition or choose a winner. |

## Invariants

1. There is one selected-Version writer/transition point: LayerStack-0
   transition gate. Application policy may request a transition but cannot
   mutate accepted payload or head records directly.
2. An accepted payload is one complete immutable Version. No rollout reconstructs
   truth by following parent layers or a depth chain.
3. Creating a Branch Head from an accepted binding and selecting an already admitted
   winner are reference-only operations with payload bytes read = written =
   copied = 0.
4. Workspace mutation never changes a committed payload. A mutated workspace
   is a candidate for a different VersionId.
5. The application owns scoring and winner choice. Storage owns validation,
   admission, reference integrity, OCC, recovery, and retirement only.
6. Selected-head publication linearizes at exactly one atomic complete-record
   replacement after expected-head comparison under the transition gate.
7. A stale head loses cleanly. Neither storage nor application may convert that
   failure into an implicit merge or rebase.
8. Docker, OCI, OverlayFS, mount, namespace, host paths, worker IDs, and other
   runtime-placement facts are excluded from VersionId input.
9. Loser cleanup cannot retire a payload while any durable root/head or valid
   read custody still names it.
10. Resource admission is bounded before expensive work; a rollout fan-out does
    not authorize unbounded staging bytes, memory, descriptors, workers, or
    recovery debt.

## Selected architecture versus delegated details

| Topic | Status | Boundary |
|---|---|---|
| Policy remains outside storage | **SELECTED R0** | Required by hard rule 7; changing it reopens Phase 01. |
| Existing application and runtime-effect owners remain | **SELECTED R0** | No new rollout service, coordinator, or store-owned executor. |
| Complete immutable accepted payload and accepted binding | **SELECTED R0** | Generic storage contract used by every branch. |
| Reference-only Branch-Head creation/replacement with payload I/O `0/0/0` | **SELECTED R0** | Phase 03 must expose counters/test seams that prove it. |
| Single OCC selected-head transition | **SELECTED R0** | Exact synchronization and record encoding are Phase 03 details. |
| Canonical grammar and typed digest construction | **DEFERRED PHASE 02** | Must remain deterministic, portable, typed, bounded, and fully comparable. |
| On-disk names, durability sequence, lock implementation | **DEFERRED PHASE 03** | Must realize the selected atomicity and recovery outcomes. |
| Product rollout API and operation routing | **DEFERRED PHASE 04** | Must preserve current app/effect ownership and generic store boundary. |
| MCTS algorithm, scoring function, fan-out, pruning, retry policy | **CALLER POLICY** | Not a LayerStack-0 storage decision. |
| Exact resource ceilings and scheduling | **DEFERRED PHASE 02/03/04** | Limits must be finite, configured, enforced, and observable. |
| `DEC-017` operation semantics | `OWNER_DEC_OPEN`, isolated | May change which caller operations produce candidates; every admitted result still uses the same V2 path. |
| `DEC-018` auth/revoke race ordering | `OWNER_DEC_OPEN`, isolated | Application ordering may vary, but store OCC and generation/fence checks remain mandatory. |

## Verification mapping

| Claim in this view | Later proof owner |
|---|---|
| Complete-Version content identity and runtime-neutral canonical facts | Phase 02 identity vectors and forbidden-field tests |
| Equal accepted Versions reuse one physical payload; collision mismatches reject | Phase 03 functional/fault tests |
| `CreateHeadIfAbsent`, `ReplaceHead`, `RemoveHead`, `CreateFixedRootIfAbsent`, and `RemoveFixedRoot` have payload I/O `0/0/0` | Phase 03 operation counters, `F3`-`F7`, and the accepted-reference performance Must check |
| Candidate-bearing publication has one OCC linearization and stale loser | Phase 03 concurrency histories and crash matrix |
| Application owns policy; LayerStack-0 exposes only generic primitives | Phase 04 wiring and dependency tests |
| Workspace/exec facts do not enter identity | Phase 02 forbidden-field tests plus Phase 04 integration tests |
| Cleanup never races a live root or reader | Phase 03 retirement/custody histories and Phase 06 offline proof |
| End-to-end rollout behavior remains within resource ceilings | Phase 04 integration plus Phase 06 matched load/rehearsal |

Stage 4.6 results are not a verification row because they are
`INCOMPARABLE`. A matched protocol may later measure V2, but no result can
weaken the correctness invariants above.

## Reopening conditions

Reopen Phase 01 before implementation proceeds if any of the following becomes
necessary:

- storage must own scoring, branch expansion, MCTS policy, winner choice, or
  execution scheduling;
- a new service, package-level authority, registry, coordinator, database, or
  helper process is required for rollout correctness;
- a Fork or selection of an already accepted Version requires complete-Version
  payload copying or reading;
- portable identity must contain a workspace, OverlayFS, mount, namespace,
  Docker/OCI, host path, or rollout-policy fact;
- more than one selected-Version transition point or a silent merge/rebase is
  required; or
- the bounded-resource and cleanup contract cannot be realized by the existing
  application, runtime, and LayerStack ownership split.

## Related documents

- [Architecture design](../architecture_design.md)
- [Version identity](../design/02-state-identity.md)
- [LayerStack-0 Version-storage design](../design/03-state-store.md)
- [Algorithms and call flows](../design/04-algorithms-and-call-flows.md)
- [Concurrency, durability, and recovery](../design/05-concurrency-durability-recovery.md)
- [Resources, security, and observability](../design/06-resources-security-observability.md)
- [Performance and optimization](../design/07-performance-and-optimization.md)
- [Phase 01 selection input contract](../phases/01-choose-design/SPEC.md)
- [Fork/checkpoint/rollback diagram](03-fork-checkpoint-rollback-and-cow.md)
- [Publish/OCC diagram](04-publish-occ-and-head-cas.md)
