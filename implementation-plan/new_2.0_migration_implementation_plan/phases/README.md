# Phase index

> **HISTORICAL PHASE INDEX — DO NOT USE FOR CURRENT V2 SCHEDULING.** The current
> program uses Phases 00–08, with current Phase 01 complete and R0 selected.
> Continue from current [Phase 02](../../../ephemeral-sandbox-v2/phases/02-state-identity/PRD.md)
> under the selected [architecture](../../../ephemeral-sandbox-v2/architecture_design.md).
> See the [archive compatibility map](../../README.md).

The migration has **three conservative top-level operational phases, numbered
0–2**. The 11 causal acceptance points remain independently hashed gates. They
are not top-level phases merely because one result must precede another.

**Current authorization: artifact-system and Phase 0 packet preparation only.**
No durable Phase 0 authority receipt or authenticated phase-entry authorization
attestation is sealed. Joint
topology × physical-profile selection is `NOT_RUN`; its accepted-winner count is zero.
Nothing in this index accepts a design, physical method, production artifact,
live migration, retirement, release, or deletion.

## Phase and gate are different things

A **phase** is a maximal externally authorized risk envelope with one fixed
actor/capability ceiling:

- Phase 0 may seal an independent judge but may not evaluate candidates;
- Phase 1 may evaluate, build, and qualify only non-live artifacts that can be
  discarded without changing live truth; and
- Phase 2 may mutate the live fleet and consume the one-way rollback boundary,
  but only after a new explicit owner authorization based on Phase 1's exact
  accepted output.

A **gate** is a content-addressed acceptance predicate over exact named inputs,
outputs, evidence scope, and invalidation rules. A gate can allow the next
ordered action already inside the phase's capability ceiling or permanently
narrow what remains legal. It cannot enlarge that ceiling, authorize the next
phase, promote evidence to different bytes, or weaken a stop condition.

This definition is operational rather than document-counting: hashes and
signatures preserve causality; phases isolate who may do what to which truth.

## Three envelopes, 11 causal gates

| Phase | Fixed risk/permission envelope | Ordered binding output |
|---:|---|---|
| [0](00-independent-judge-and-evidence-seal.md) | independent, candidate-blind facts and judge; no evaluation or production work | **(1)** content-addressed judge/evidence seal; no winner |
| [1](01-non-live-selection-implementation-and-qualification.md) | candidate evaluation plus reversible non-live implementation and qualification; no live V2 route or acknowledgment | **(2)** joint topology × method `H_PROFILE`/`NO_WINNER` → **(3)** `H_FMT` → **(4)** `Hstore` → **(5)** `Hpermanent` → **(6)** exact `H_PRECUTOVER` → **(7)** `Hqual` naming byte-identical `H_PRECUTOVER` |
| [2](02-irreversible-cutover-observation-retirement-and-release.md) | explicitly authorized live-fleet mutation, one-way activation, observation, compatibility retirement, changed-artifact release | **(8)** irreversible exact-`H_PRECUTOVER` cutover, complete fleet activation, and ingress opening → **(9)** bounded observation → **(10)** compatibility retirement/build `H_RELEASE` → **(11)** total exact-artifact qualification, fleet rebind, live attestation, and release of exact `H_RELEASE` |

The edge chain is strict. An accepted gate records every predecessor hash it
consumes; changed input invalidates that result and all transitive consumers.
`NO_WINNER` at gate 2 closes gates 3–11.

Optional destructive legacy-data deletion is a separately signed
**POST-RELEASE ACTION outside this DAG**. Phase 2 neither requires nor
implicitly authorizes it.

## Execution packet instantiation

The [execution artifact contract](../execution/README.md) maps all 11 gates to
predeclared packet paths; its separate
[`state.json`](../execution/state.json) records the instantiated canonical
prefix. Every edge requires exact manifest plus independent-acceptance hashes.
Only
[`phase-00/00-evidence-seal`](../execution/phase-00/00-evidence-seal/packet.md)
exists now, with state `DRAFT / NOT_RUN`. Phase 1 and 2 packet directories are
absent by design; copying a future template before predecessor acceptance,
separate phase authorization, and its independently verified entry attestation
is a contract failure, not preparation.

## Why three

Three is the smallest **conservative operational grouping currently
justified**, not a mathematical minimum and not a claim that every possible
administrative workflow needs three. The global minimum remains `OPEN`.

The two top-level boundaries pay for concrete capability changes:

| Boundary | Why a new phase is required |
|---|---|
| 0 → 1 | Candidate authors and implementers must not select or revise the facts, fixtures, holdout, oracle, thresholds, or rejection rules used to judge their work. Phase 0 therefore cannot grant candidate-evaluation capability. |
| 1 → 2 | A non-live envelope must not preauthorize fleet mutation or the irreversible activation before a winner exists and byte-identical `H_PRECUTOVER` passes rehearsal. Phase 2 requires a new owner decision over exact Phase 1 hashes. |

Two phases would have to fuse one of those boundaries. Fusing 1+2 is not
conservatively justified because it grants live/irreversible authority before
its qualifying artifact exists. A static-role 0+1 envelope is a genuine
unresolved challenger: it must prove candidate-blind holdout secrecy,
capability/ACL noninterference, immutable judge sealing before candidate work,
independent acceptance, and complete invalidation. The current package has not
proved those obligations, but it also does not claim that such fusion is
impossible. By contrast, the superseded extra phase boundaries subdivided work
inside one unchanged capability ceiling. Their signed evidence gates remain;
the redundant top-level promotions do not.

Within Phase 2, the activation gate can only narrow permissions: after exact
`V2Writable(g+2)` activation, writable-legacy abort disappears forever.
Observation completion can allow compatibility retirement only under the
already bounded Phase 2 live-change authorization, and changed
`H_RELEASE` bytes still require a total fresh gate disposition, exact-artifact
qualification, a new release epoch and receipt set, complete fleet rebinding,
old-process drain, and live attestation before release.

## Universal transition record

Every gate records:

- exact consumed and produced hashes, dirty state, artifact/configuration,
  actor, authority, and accepted capability scope;
- raw evidence, gate version, environment, resource deltas, crash cuts,
  deletions, and byte-identity attestation;
- status `NOT_RUN`, `PARTIAL(scope)`, `PASS`, `FAIL`, or `BLOCKED(reason)`;
- invalidation owner, reopening point, stop condition, and next allowed and
  forbidden actions; and
- an independent acceptor distinct from the gate's result-producing actor.

The reusable packet shape and machine-readable fields are defined only by the
execution contract. Qualification report status remains the five-value
vocabulary above; a separately recorded `INVALIDATED` lifecycle disposition
preserves the old report while blocking every transitive consumer.

The content-addressed static topology is in `execution/gates.json`; the
instantiated prefix and lifecycle invalidations are kept separately in
`execution/state.json`. Except for the exact one-packet bootstrap, each state
authenticates one `ADVANCE` or `INVALIDATE` transition from retained exact prior
state bytes and the complete prior packet prefix. State is published last and
is unusable unless an independent policy-selected verifier proves the external
conditional-write or fenced-lease provider committed the exact raw successor
against the exact prior token. The lifecycle publisher, commit provider, and
verifier are independent on principal, credential, and control-domain axes.
Phase authority exists only as a separately preserved receipt in the entering
packet's input lock, never as a mutable state assertion. This prevents a normal
phase transition from changing the catalog digest already named by an accepted
packet.

No exit self-authorizes its successor phase. Correctness, crash, capacity,
containment, migration, fleet-fence, or performance failures have no
production waiver. See
[`phase-isolation-and-ordering.md`](phase-isolation-and-ordering.md) for the
complete ordering, invalidation, permission, and compression proof.
