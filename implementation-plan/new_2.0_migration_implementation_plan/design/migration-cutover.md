---
status: proposed
authority: migration-cutover
depends-on:
  - REQ-MIG-001
  - REQ-MIG-003
  - REQ-MIG-005
---

# Migration, cutover, and retirement

## Responsibility

This document owns legacy inventory, import, identity mapping, fleet fencing,
rollback boundary, compatibility retirement/release, and the separately signed
post-release destructive legacy-deletion contract.

## Source inventory before importer design

Phase 0 records the actual deployed authorities and bytes, including:

- sandbox heads, checkpoints, fork origins, revisions, and authorization;
- LayerStack manifests/layers, leases, mounts, mutable workspaces, and
  autosquash/squash state;
- any records actually discovered with MPLA-era ownership/custody, allocation,
  replay/session, or recovery semantics; historical MPLA experiment receipts
  alone are incomparable and establish neither deployed truth nor a current
  source/package row;
- runtime-owner-private allocations and active effects;
- in-flight requests, exact replay sources, readers, builders, and sessions;
- backup, restore, export, and disaster-recovery dependencies; and
- every caller that reads or writes legacy truth.

An importer designed from prose rather than this inventory fails the entry gate.

## Normative import dependency direction

Arrows below mean source, build, or call dependency from left to right. This is
the sole normative import direction; source-layout and candidate ledgers verify
it without inventing an opposite “inward” or “outward” convention.

```text
temporary migration code unit/target/artifact -> read-only inventoried-legacy-schema adapter
temporary migration code unit/target/artifact -> accepted pure canonical function/type set
temporary migration code unit/target/artifact -> exactly one bounded selected-state import command/effect
```

Forbidden reverse or steady-state dependencies are:

```text
permanent V2 canonical/selected/application/runtime/provider code -> temporary migration code or legacy adapter
legacy adapter -> permanent selected-state writer internals
```

The selected-state import command is a narrow effect invoked by the temporary
code; its implementation never imports or calls back into migration code. The
same graph applies if the temporary code is a module or one-shot target inside
an extant package. A separate migration package is generated and retained only
if the joint topology tournament selects it after its deletion counterexample.

## Import contract

- **MIG-IMP-001.** Every import source/build/call edge obeys the normative graph
  above: temporary migration code may read through the legacy adapter, invoke
  the accepted pure functions, and invoke the one bounded import effect; none
  of those permanent dependencies points back to migration code.
- **MIG-IMP-002.** Every complete legacy root is materialized as complete
  portable facts, including root metadata, then canonicalized through the
  selected V2 pure canonical function set. Migration-source provenance is recorded beside the
  old-to-new mapping; it enters canonical identity only if the independently
  accepted product fact contract requires that provenance.
- **MIG-IMP-003.** Import first derives a candidate V2 `StateId`; an occupied
  candidate is admitted only after exact canonical-byte equality. Equal bytes
  coalesce. Unequal bytes terminate as
  `T03_REJECTION / STATE_ID_COLLISION` with bounded cleanup and no alias, root,
  mapping, index, revision, custody, or capacity fact. Only an accepted
  no-alias binding may be recorded in the total old-root-to-V2 mapping, which
  an independent oracle verifies before selection. Import and recovery fail
  readiness closed if uniqueness cannot be established.
- **MIG-IMP-004.** Mutable/in-flight sessions are drained, expired, or mapped by
  an explicit rule; they are never silently treated as complete roots.
- **MIG-IMP-005.** Import is all-or-none under exact side-by-side capacity,
  recovery, and retirement-debt charges for every selected profile dimension,
  including bytes and inodes for the current Linux storage profile.
- **MIG-IMP-006.** The temporary migration code unit/target/artifact is
  deletable. A separate package exists only if selected by `H_PROFILE`; V2
  steady state contains no migration target, layer/squash reader, legacy
  adapter, or legacy fallback.

## Fleet cutover fence

The fleet configuration authority established by Phase 0 must expose one
atomic logical fence value:

```text
FleetFence {
    cutover_generation,
    mode: LegacyWritable | QuiescedForImport | V2Writable
}
```

This tuple is a semantic state, not a prescribed record encoding, database, or
RPC. `cutover_generation` increases on every mode transition. Mode is not
globally forward-only before V2: the only legal branches from a writable
legacy generation are:

```text
LegacyWritable(g)
  -> QuiescedForImport(g+1)
  -> LegacyWritable(g+2)       // pre-V2 abort

or

LegacyWritable(g)
  -> QuiescedForImport(g+1)
  -> V2Writable(g+2)           // irreversible
```

A generation is never restored, reused, or decremented. Once any generation is
`V2Writable`, no later generation may be `LegacyWritable`.

This is a migration fence, not a third V2 storage component or a second
selected-state selector. A client-side read immediately before a write is
insufficient: a paused writer could resume after quiescence. Every legacy and
V2 durable-selection authority must therefore atomically condition selection
on the exact locally installed generation token. Installing a newer generation
durably prevents all lower-generation selections before that authority can
contribute to cutover completion. The selected fleet-fence protocol may declare
completion only after it proves that every inventoried writer authority is
generation-bound and quiescent and that every accepted request has drained
through response or replay custody. This invariant does not preselect a central
controller, broadcast fan-out, lease topology, or one network acknowledgment
per process.

Every process that could accept, durably select, or acknowledge work must:

1. obtain the full exact generation/mode token before accepting work;
2. have its local durable-selection authority validate that token atomically
   with selection rather than through a time-of-check/time-of-use reread;
3. bind the resulting durable receipt to that generation;
4. validate generation/mode before acknowledgment and suppress a stale
   acknowledgment according to the sealed replay/roll-forward rule; and
5. fail closed when the fence is stale, unavailable, ambiguous, or cannot be
   enforced by the local selector.

Joint Phase 1A profile selection must select and prove the concrete fleet-to-local installation and
acknowledgment protocol as part of its realized topology. The design may not assume a linearizable remote read
can be atomically combined with unrelated storage by timing alone.

A selected-state selector cannot substitute for this fleet authority because it
cannot fence independent legacy writers.

## Controlled sequence

1. Freeze a Phase 1F-qualified `H_PRECUTOVER` binary, configuration, evidence manifest, restore
   plan, and exact capacity reservation.
2. Atomically advance the exact expected `LegacyWritable(g)` value to
   `QuiescedForImport(g+1)` and stop new write ingress.
3. Durably install generation `g+1` at every inventoried legacy/V2 selection
   authority; drain active requests, sessions, readers, builders, and responses;
   and collect every exact generation-bound quiescence acknowledgment.
4. Precharge the complete side-by-side import and recovery reserve.
5. Import complete facts using the selected pure canonical function set and write source provenance
   to the separate old-to-new mapping ledger.
6. Build the selected-state representation without making V2 writable.
7. Verify semantic oracle parity, mappings/provenance, custody, allocation, and
   recovery.
8. While ingress remains closed, distribute the exact candidate
   `V2Writable(g+2)` token to every inventoried selector, durably install and
   sync it in an **inactive** slot, prove restart reconstruction, and collect
   generation-bound installation acknowledgments. An inactive slot cannot
   select or acknowledge work.
9. Atomically advance the exact expected global
   `QuiescedForImport(g+1)` value to `V2Writable(g+2)`. This is the irreversible
   fleet-fence boundary; it does not by itself open ingress or authorize a
   local acknowledgment.
10. Still with ingress closed, atomically activate the already durable `g+2`
    slot at every selector, inject crashes immediately before/after local
    install, sync, activation, acknowledgment, and recovery reconstruction,
    and collect every exact `g+2` activation acknowledgment. A missing,
    ambiguous, or restarted selector fails closed.
11. Durably record fleet completion for exact `g+2` and only then open the
    generation-bound ingress gate. This opening is the
    **first-possible-public-V2-operation-acknowledgment boundary**. Every V2 selection and
    acknowledgment atomically validates the active local `g+2` token; every
    lower token remains fenced.
12. Observe, recover forward when necessary, and retain legacy read-only data
    until every retirement gate passes.

## Rollback boundary

- **MIG-CUT-001.** Before the transition to `V2Writable`, a failed attempt may
  atomically advance the exact expected `QuiescedForImport(g+1)` value to
  `LegacyWritable(g+2)` after proving no V2 selection or acknowledgment was
  possible. It never restores an earlier generation.
- **MIG-CUT-002.** At or after the global transition to `V2Writable(g+2)`,
  writable legacy rollback is forbidden even while ingress remains closed.
  After the fleet-completion ingress opening, V2 recovery/roll-forward is the
  only data path visible to new work.
- **MIG-CUT-003.** There is no dual-write reconciliation protocol and no client
  chooses a format.
- **MIG-CUT-004.** The global transition to `V2Writable` is the irreversible
  rollback boundary. The later fleet-completion ingress opening is the first
  possible public V2 operation acknowledgment. Neither boundary is inferred from observation
  of an application response.

## Compatibility and retirement

Compatibility endpoints remain translations into V2, never a second truth.
Each has telemetry and an explicit deletion condition. Phase 0 records the
longest retry, replay, restore, backup, audit, client-upgrade, and operational
observation horizons; Phase 0 freezes a proposed retention window that covers them, and
the owner accepts it before cutover. This draft does not invent a release count
or number of days without that evidence (`DEC-011`).

Retirement changes executable/configuration bytes, so it produces exact
`H_RELEASE`; it cannot inherit `H_PRECUTOVER` qualification or fleet receipts.
Before operational release, the retirement build supplies a total disposition
for every frozen `QG-*` gate: either an exact-`H_RELEASE` rerun or an
independently accepted executable non-impact proof over the complete transitive
source/build/configuration/runtime dependency closure. Missing rows fail and
binary/dependency/feature/linker/allocator/configuration changes default to
rerun.

After that total qualification passes, live deployment uses a release epoch
separate from `cutover_generation`: seal the complete expected authority set;
install exact `H_RELEASE` inertly; sync and reconstruct per-authority install
receipts; quiesce ingress and drain work; activate a new release epoch; collect
and reconstruct new activation receipts; drain/terminate all compatibility-
bearing processes; run exact live attestation; durably record complete-fleet
release; then reopen ingress. The `g+2/H_PRECUTOVER` receipts are never reused.
Before release-selector activation an inert-install failure may abort to the
already qualified V2 `H_PRECUTOVER` fleet. At or after activation, ambiguity
keeps ingress closed and recovery reconciles forward; it never restores
writable legacy. Only complete live `H_RELEASE` fleet evidence makes
compatibility operationally absent.

Legacy code/data deletion is not part of the three-envelope DAG. It is a
separately signed post-release action after accepted Phase 2 release and only after:

- no direct or compatibility caller remains;
- no semantic root, reader, receipt, replay horizon, backup, restore, or audit
  depends on legacy bytes;
- V2 restore and post-ack recovery have been rehearsed;
- exact reclaimable bytes/inodes are proved and synchronized; and
- the owner explicitly approves the named deletion targets.

## Stage 4.6 use

The sealed evidence commit and later hardening tip remain detached read-only
identity/context sources and are currently `INCOMPARABLE`. They may identify
historical fixtures, OCI/OverlayFS observations, crash hypotheses, and
measurement-boundary definitions, but supply no causal performance endpoint,
current-source anchor, topology constructor, or migration target. Their
layer/squash architecture, module graph, and unqualified thresholds are never
wholesale cherry-picked.
