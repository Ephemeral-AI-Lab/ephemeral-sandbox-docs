# Phase 2 — Irreversible cutover, observation, retirement, and release

## Objective

Under one explicitly authorized live-fleet change envelope:

1. cut over once using byte-identical `H_PRECUTOVER` and the qualified durable
   fleet barrier;
2. cross the exact global `V2Writable` transition while ingress remains closed,
   irreversibly ending writable-legacy rollback;
3. activate every exact `g+2` selector, durably record reconstructible fleet
   completion, and only then open ingress at the first-possible-public-V2-
   operation-acknowledgment boundary;
4. complete the accepted finite observation horizon while compatibility and
   legacy bytes remain recoverably read-only;
5. retire compatibility in dependency order—temporary entry points/callers
   first, then their now-unreferenced migration code and legacy adapters—and
   build changed `H_RELEASE`; and
6. freshly qualify, fleet-rebind, deploy, and live-attest byte-identical
   `H_RELEASE` while legacy data remains retained.

Optional destructive legacy-data deletion is outside this phase and outside
the mandatory DAG.

## Predecessor outputs consumed

- **Phase 0:** exact writer/authority/provenance inventory, semantic oracle,
  cutover and observation contracts, retention/no-reference rules, numeric
  signals, and independent evidence rules.
- **Phase 1 gates 1A–1F:** unchanged accepted joint `H_PROFILE`, `H_FMT`,
  `Hstore`, `Hpermanent`, exact `H_PRECUTOVER`, and `Hqual`; the qualified generation-
  token distribution/install/sync/ack/reconstruction protocol; exact writer
  set; runbooks, monitors, abort criteria, restore proof, capacity reserve,
  deletion manifest, and owner go/no-go inputs.

No partial, rebuilt, patched, reconfigured, or equivalent-looking artifact may
substitute for an exact predecessor.

## Entry authorization and capability ceiling

- Phase 0 and all Phase 1 gates are independently accepted and unchanged.
- Live binary, configuration, schemas, format, dependencies, and runbooks are
  byte-identical to `H_PRECUTOVER`.
- Every actual writer/selection/acknowledgment authority is in the sealed set
  and can durably participate in the qualified barrier.
- Required storage, recovery, observation, and incident reserves are
  precharged; monitoring and V2-only restore are ready.
- The owner explicitly authorizes the bounded Phase 2 live-change program,
  including the possibility of irreversible V2 activation and, only after its
  own observation gate, compatibility retirement and changed-artifact release.
  Phase 1 completion does not self-authorize this phase.
- The externally pinned per-artifact verifier policy authenticates the
  phase-entry attestation binding the exact live authorization receipt; actor
  principal/credential/control-domain triples; exact gate capabilities;
  validity/revocation fact; catalog; gate; and lineage.

| Actor | May | Must not |
|---|---|---|
| owner/change authority | authorize Phase 2 and accept or reject each internal promotion record | waive fleet completeness, reuse old evidence for changed bytes, or treat release approval as deletion authority |
| cutover/fleet operator | execute only the sealed monotone runbook against exact hashes | invent a writer, generation, artifact, timeout-based success, or post-activation legacy rollback |
| each writer/selection authority | durably install, reconstruct, and acknowledge exact generation state; select only when its local fence permits | select or acknowledge with a stale/unknown token; infer permission from another authority's state |
| independent gate authorities | attest artifact identity, barrier receipts, live evidence, observation, retirement diff, and fresh `H_RELEASE` results | produce and accept the same result; promote `H_PRECUTOVER` evidence to `H_RELEASE` |
| operations/incident owners | monitor, fail closed, restore or roll forward V2, and retain compatibility/legacy as required | make legacy writable after the global `V2Writable` transition or delete legacy under Phase 2 authority |

Phase 2 is one live-risk envelope. Its gates only narrow legal actions or allow
the next action already bounded by that authorization. They never weaken the
predecessor chain or make destructive data deletion legal.

## Four ordered gates

```text
2A exact-H_PRECUTOVER durable fleet cutover
  -> 2B accepted bounded observation
  -> 2C compatibility retirement and exact H_RELEASE build
  -> 2D total fresh qualification, fleet rebind, and live release of exact H_RELEASE
```

Every gate binds exact inputs, actor and authority set, raw evidence, process-
death and host-power-loss crash cuts where durability is claimed, resource
state, output hash, stop conditions, and invalidation owner. A
failure before the global `V2Writable` transition may use only the qualified
higher-generation abort. A failure at or after that transition stops promotion
but cannot restore writable legacy.

## 2A — Exact-artifact cutover with durable `g+2` fleet barrier

### Required semantic states

```text
LegacyWritable(g)
  -> QuiescedForImport(g+1)
       -> LegacyWritable(g+2)   # abort before global V2Writable transition only
       -> V2Writable(g+2, ingress=closed)  # irreversible rollback boundary
            -> V2Writable(g+2, ingress=open)  # only after durable fleet completion
```

Generations never decrease or repeat. Once any accepted generation is
`V2Writable`, no later generation may make legacy writable.

The selected Phase 1 protocol may encode and transport the following facts in
any proved smaller form, but it must provide their semantics without creating
a second selected-state truth:

- one exact authoritative fleet permission state whose semantics include
  `{generation, mode, ingress}`; a candidate may prove a smaller encoding but
  may not create a second conflicting permission truth;
- an exact sealed set of every authority capable of accepting, selecting, or
  acknowledging legacy or V2 work;
- a durable per-authority installation/acknowledgment fact bound to authority
  identity, `g+2`, target mode, exact `H_PRECUTOVER`, and the locally installed
  selection-fence state;
- a reconstructible fleet barrier proving the complete expected acknowledgment
  set, not a process-local counter, lease timeout, or best-effort broadcast;
  and
- one atomic global `V2Writable(g+2)` transition that irreversibly forbids
  writable legacy while ingress remains closed; and
- a reconstructible complete set of generation-bound selector-activation
  receipts plus a durable fleet-completion fact required before opening
  ingress. That opening is the first possible public V2 operation
  acknowledgment boundary. Installation and activation acknowledgments are
  control-plane receipts, not public operation acknowledgments.

An inert installation/readiness record does not authorize selection and is not
a fallback selector. The sole authoritative fleet activation plus each local
selector's atomic generation check determines permission.

### Ordered cutover

1. Recompute and attest exact `H_PRECUTOVER`, `Hqual`, current fleet token,
   writer/authority set, routes, capacity reserve, restore inputs, runbook, and
   monitor ownership. Any mismatch stops before mutation.
2. Atomically advance exact `LegacyWritable(g)` to
   `QuiescedForImport(g+1)`. Durably install and synchronize `g+1` at every
   inventoried authority; reject lower generations; drain admitted work through
   response or replay/effect custody; and durably record every exact
   generation-bound quiescence acknowledgment.
3. Reconstruct the expected set and received acknowledgments from durable
   authority/fleet facts. Unknown, duplicated with different contents,
   uninstalled, unsynchronized, stale, or non-acknowledging authority state
   blocks progress. A timeout is an incident signal, never completion.
4. Complete final import and verification using exact `H_PRECUTOVER`: total
   old-root mapping/provenance, semantic oracle, selected state, custody,
   allocation/capacity, backup/restore, and restart recovery. V2 remains
   non-routable and non-acknowledging.
5. For target `V2Writable(g+2)`, durably stage/install the qualified inert
   `g+2` activation material at every authority, synchronize it, and collect a
   durable acknowledgment bound to the exact authority, generation, mode,
   artifact, and local selector state. Before fleet activation, this material
   cannot admit, select, or acknowledge V2.
6. Close the preactivation fleet barrier only after the complete exact
   authority set has a valid durable `g+2` installation acknowledgment and a
   restart reconstructs the same complete barrier from authoritative storage.
   Crash/fault every distribution, local install, sync, acknowledgment, barrier
   update, duplicate, and reconstruction cut. Missing or ambiguous state fails
   closed at `QuiescedForImport(g+1)`.
7. **Abort branch, only before the global `V2Writable` transition:** atomically advance exact
   `QuiescedForImport(g+1)` to `LegacyWritable(g+2)`, durably distribute/install/
   synchronize it, collect the complete fleet acknowledgment set, and prove all
   staged V2 activation material is inert before resuming ingress. Never restore
   `g` or `g+1`. A later attempt starts from a newer generation.
8. **V2 branch:** after the complete preactivation barrier, atomically select
   exact `V2Writable(g+2)` at the protocol's single authoritative activation
   point under the barrier bound to exact `H_PRECUTOVER`. This durable global
   transition is the irreversible writable-legacy rollback boundary. Ingress
   remains closed, and this transition alone permits no public V2 operation
   acknowledgment. Installation or activation receipts are control-plane facts
   only.
9. Still with ingress closed, each authority atomically activates its exact
   durably installed `g+2` fence and emits a durable generation-bound control-
   plane receipt. An authority not yet converged to exact `g+2` fails closed; it
   never serves legacy or V2. Declare selector activation complete only after
   reconstructing the full activation-receipt set from durable facts.
10. Durably record fleet completion for exact `g+2`, then atomically open the
    generation-bound ingress permission. This opening is the first possible
    public V2 operation acknowledgment boundary. Every admitted operation must
    validate exact open ingress and the active local `g+2` fence; neither a
    control-plane receipt nor the earlier global mode transition is a public
    operation acknowledgment.
11. On restart, reconstruct the authoritative fleet permission state, exact expected
    authority set, local installed generation/mode/artifact, preactivation and
    post-activation receipts, custody, fleet-completion fact, ingress state, and
    barrier status before readiness. If the authoritative state remains
    `QuiescedForImport(g+1)`, no public V2 operation acknowledgment may occur and
    the runbook may resume or take only the higher-generation abort. If it is
    `V2Writable(g+2)`, writable legacy is permanently forbidden, ingress remains
    closed until the complete activation set is reconstructed and fleet
    completion durably recorded, and recovery reconciles forward. Only then may
    ingress open, which is the first possible public V2 operation acknowledgment
    boundary. If it is `LegacyWritable(g+2)`, the global V2 transition and local
    V2 activation are forbidden and any staged V2 material remains non-authoritative.

### 2A acceptance and stop

`QG-MIG-001`, `QG-SYS-001`, `QG-CRASH-001`, `QG-RES-001`, and every other
applicable live gate pass against byte-identical `H_PRECUTOVER`. The accepted
record binds the exact global `V2Writable` commit, installation and activation
receipt sets, durable fleet-completion and ingress-opening commits, restart
reconstructions, generation transitions, live artifact
attestation, capacity/resource state, and incident timeline.

Before the global `V2Writable` transition, stop or execute only the qualified
`LegacyWritable(g+2)` abort. At or after that transition, never restore writable
legacy; fail closed and use only accepted V2 recovery, restore, roll-forward,
and incident procedures. Until durable fleet completion and ingress opening,
no public V2 operation acknowledgment is legal.

## 2B — Bounded observation

Observe exact `H_PRECUTOVER` for the complete owner-accepted `DEC-011` horizon:
semantics, integrity, stale-writer exclusion, replay/effect custody, automatic
cache/resource cleanup, capacity, containment, latency/throughput, backup,
restore, recovery, fleet convergence, and operations signals. Include every
incident and failed plateau, not only successful samples.

Compatibility/importer code and legacy bytes remain retained recoverably
read-only for the whole horizon. A live failure blocks 2C but never permits
writable legacy rollback. Observation neither authorizes compatibility/data
deletion nor qualifies changed bytes.

Gate 2B accepts only when `QG-MIG-001`, `QG-SYS-001`, `QG-OPS-001`, and every
applicable live gate pass for the full horizon. Its content-addressed result
binds exact `H_PRECUTOVER`, raw signals, incidents, resource plateaus, start/end
conditions, and signed eligibility or ineligibility for 2C.

## 2C — Compatibility retirement and `H_RELEASE` build

Entry requires accepted unchanged 2A/2B evidence and proof that no caller,
writer, replay, reader, backup, restore, audit, client-upgrade, legal, or
operational obligation still requires compatibility. The exact code,
dependency, configuration, schema, runbook, and recovery targets are reviewed
before mutation.

Remove temporary migration entry points/callers first, then their
now-unreferenced migration code, legacy adapters/readers/writers, compatibility
branches, unreachable transitions, obsolete dependencies, laboratory code, and
temporary telemetry. Preserve canonical V2 bytes, generation binding,
stale-writer suppression, no-writable-legacy, accepted steady-state resource
bounds, every permanent authority/fence law, and legacy data itself. Build and
content-address changed source, binary, configuration, schemas, dependencies,
and runbooks as exact `H_RELEASE`.

Gate 2C binds the deletion diff, no-reference evidence available at build
time, exact build inputs/outputs, and a **total gate-impact disposition** with
one row for every `QG-*` ID. Each row is exactly one of:

- `RERUN(H_RELEASE, sealed procedure, required receipts)`; or
- `UNCHANGED_PROOF(H_RELEASE, proof hash, complete transitive
  source/build/configuration/runtime dependency closure, independent acceptor,
  executable falsifier)`.

A missing row, incomplete closure, or informal “unaffected” label fails closed.
Any binary, dependency, feature, linker, allocator, runtime-configuration, or
runbook change defaults every plausibly coupled row to `RERUN`; an independent
accepted proof is required to narrow that set. The disposition is content-
addressed and names exact `H_RELEASE`. Gate 2C does not qualify, install, or
release `H_RELEASE`, and no `H_PRECUTOVER` result transfers by omission.

## 2D — Fresh qualification, fleet rebind, and live release

“Release” here means **operational deployment to the complete live authority
set**, not merely publishing an artifact. It has two ordered barriers inside
this gate: exact-artifact qualification, then a content-addressed fleet
upgrade. Neither creates another top-level permission envelope.

### 2D.1 — Total exact-artifact qualification

1. Verify that the 2C disposition has exactly one accepted row for every
   frozen `QG-*` ID and is bound to byte-identical `H_RELEASE`.
2. Execute every `RERUN` against exact `H_RELEASE`. Accept an
   `UNCHANGED_PROOF` only after its independent acceptor runs the executable
   falsifier and verifies the complete transitive source, build,
   configuration, runtime, dependency, feature, linker, allocator, and runbook
   closure.
3. Prove that no live build, source, schema, configuration, runbook, backup,
   restore, recovery, or observability reference reaches removed machinery.
4. Fail on a missing row, stale hash, unresolved proof gap, or result produced
   for different bytes. Evidence from `H_PRECUTOVER`, Phase 1, or 2A/2B is
   historical input only unless the exact `UNCHANGED_PROOF` rule accepts it.

`QG-RET-001`, `QG-MIG-001`, `QG-SYS-001`, and every other row in the total
disposition must resolve successfully before any live selector can install or
activate `H_RELEASE`.

### 2D.2 — Content-addressed live fleet upgrade

The fleet upgrade uses a monotone **release epoch `r+1`** that is distinct from
the selected-state permission generation `g+2`. It never reuses or reinterprets
the `H_PRECUTOVER` installation, activation, or fleet-completion receipts.
Normal V2 state generations may continue to advance; release identity and
selected-state identity remain separate typed facts.

Execute in this order:

1. Seal the exact `H_RELEASE` artifact/configuration/runbook hash, current
   release epoch `r`, new epoch `r+1`, complete expected selector/acknowledgment
   authority set, live routes, capacity and recovery reserves, abort rule, and
   receipt schema. Unknown authorities or set drift stop before distribution.
2. Distribute and install exact `H_RELEASE` **inertly** at every expected
   authority. Synchronize required bytes and parent metadata, then record a
   durable per-authority installation receipt bound to authority identity,
   `H_RELEASE`, `r+1`, current V2 mode, and local selector state. Inert bytes
   cannot select or acknowledge work.
3. Reconstruct the complete installation set after restart. Fault every
   distribution, write, sync, receipt, duplicate, restart, and reconstruction
   cut, including distinct process-death and host-power-loss cuts at every
   claimed durability boundary. A timeout is an incident, not completion.
4. Quiesce public ingress, drain admitted work to a durable response or exact
   replay/effect-custody state, and attest that all selectors still run the
   qualified `H_PRECUTOVER` release epoch while the new bytes remain inert.
5. Atomically advance the authoritative release selector to
   `ReleaseServing(H_RELEASE, r+1, ingress=closed)`. Then each authority
   activates only its exact installed `H_RELEASE`, emits a durable activation
   receipt bound to `r+1`, and fails closed if local bytes, epoch, or selector
   state disagree.
6. Reconstruct the complete activation-receipt set, drain and terminate every
   old `H_PRECUTOVER` process, and prove that no route, executable mapping,
   supervisor restart target, backup/restore target, or recovery path can serve
   the compatibility-bearing artifact.
7. Run exact live attestation and the post-deployment `QG-MIG-001`,
   `QG-SYS-001`, `QG-OPS-001`, `QG-CRASH-001`, `QG-RES-001`, `QG-RET-001`, and
   any other live rows required by the total disposition. Bind raw receipts to
   exact `H_RELEASE`, `r+1`, and the complete authority set.
8. Only after all prior steps pass, durably record `ReleaseFleetComplete` for
   exact `H_RELEASE/r+1` and atomically reopen ingress. This is the first public
   acknowledgment permitted from `H_RELEASE`. Only now may the plan claim that
   compatibility code is operationally absent.

Before step 5, an abort may discard the inert `H_RELEASE` installation and
resume the already qualified `H_PRECUTOVER` fleet after reconstructing its
complete selector set; writable legacy remains forbidden. At or after step 5,
ingress stays closed on ambiguity and recovery reconciles forward to exact
`H_RELEASE/r+1`. It may not silently mix artifacts, reuse old receipts, or
restore writable legacy. A later rollback to any V2 artifact is a new release
epoch using this same complete qualification and fleet-rebinding protocol, not
an interpretation of old receipts.

On restart, readiness requires reconstruction of the authoritative release
selector, exact expected authority set, inert-install receipts, activation
receipts, old-process drain, fleet-completion record, ingress state, and every
unresolved custody item. A changed `H_RELEASE` byte, expected-set change, or
receipt schema change invalidates all of 2D and requires a new exact
qualification and deployment lineage.

## Invalidation, recovery direction, and stop rules

| Change or failure | Required action |
|---|---|
| any Phase 0/1 input changes before the 2A global `V2Writable` transition | stop; reopen its owning gate and invalidate every consumer; no drifted artifact may cut over |
| barrier/writer-set/generation/artifact ambiguity before the global transition | stay quiesced and reconstruct, or take only the qualified higher-generation legacy abort |
| global `V2Writable` transition has committed | writable-legacy rollback is permanently forbidden even if ingress is closed and no application response was observed; repair/restore/roll forward V2 |
| live failure or incomplete 2B horizon | block compatibility retirement; retain compatibility and legacy read-only; continue V2-only incident handling |
| compatibility target or `H_RELEASE` build byte changes | rebuild 2C output and total QG disposition; rerun all 2D qualification and fleet-rebinding work for a new release epoch |
| missing/invalid total QG row or non-impact proof | fail before installation; default the row to `RERUN` and obtain exact `H_RELEASE` evidence |
| `H_RELEASE` install/receipt/expected-set ambiguity before release-selector activation | keep new bytes inert; reconstruct or abort to the complete qualified `H_PRECUTOVER` V2 fleet; never make legacy writable |
| release selector names `H_RELEASE/r+1` but fleet completion is absent | keep ingress closed; reconstruct exact receipts, terminate old processes, and reconcile forward; never reuse `H_PRECUTOVER` receipts |
| permanent canonical/authority/fence law must change after the global transition | create a new explicitly authorized V2 evolution/migration lineage; never reinterpret Phase 1 hashes or resurrect legacy truth |
| optional deletion target/policy/command changes | obtain a new distinct post-release signature; Phase 2 approval never carries over |

Stop on unknown writer, incomplete durable acknowledgment set, hash drift,
unreconstructible barrier, stale selection/acknowledgment, dual writable truth,
generation reuse/decrease, failed hard gate, unbounded resource, containment or
cleanup failure, incomplete observation, remaining compatibility dependency,
unqualified `H_RELEASE`, incomplete total gate disposition, mixed release
epoch, missing old-process drain, no-reference gap, or restore uncertainty.
After either activation, stopping means fail-closed V2 incident handling, not
legacy rollback.

## Phase exit

The mandatory three-phase DAG ends only when exact `H_RELEASE` is independently
qualified, activated by every expected authority at its new release epoch,
live-attested, old `H_PRECUTOVER` processes are drained, durable release-fleet
completion is reconstructible, and ingress has reopened. V2 remains the sole
writable truth; the full cutover, observation, qualification, and release
evidence is retained; compatibility code is operationally absent; and legacy
bytes intentionally remain recoverably retained. Phase entry, elapsed time,
artifact publication, gate pass, or release approval never authorizes data
deletion.

## POST-RELEASE ACTION — Optional destructive legacy-data deletion

This action is outside Phase 2 and outside the mandatory DAG. Only after
`H_RELEASE` is accepted and released may the owner sign a distinct destructive
record naming exact targets and commands, retention/legal approvals, no-
reference proof, recovery consequences, required synchronization, and audit
evidence. Delete only resolved targets and record the post-deletion inventory
and recoverability result.

Do not begin on an unclear target, missing approval, changed artifact,
incomplete no-reference proof, or restore uncertainty. Refusing or withholding
deletion does not reopen Phase 2; legacy bytes remain retained.
