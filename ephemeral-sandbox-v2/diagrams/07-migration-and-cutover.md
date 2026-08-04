# Migration and cutover

**Status:** explanatory view of the selected R0 migration boundary

**Authority:** [V2 PRD](../PRD.md) -> Phase 01 [selection input contract](../phases/01-choose-design/SPEC.md) -> selected [architecture output](../architecture_design.md)

**Purpose:** show the one-way transfer of writer authority from legacy truth to
V2 truth, including the generation fence, normal V2 admission, pre-activation
abort boundary, irreversible activation, observation, and deletion of the
temporary compatibility unit.

This document does not authorize a live migration, cutover, deletion, or
legacy-data destruction. Phases 05 and 06 build and prove the path; Phase 07
requires separate live authorization. `DEC-011` (observation-window duration)
remains open. Historical Stage 4.6 evidence is `INCOMPARABLE` and is not a
cutover SLO or benchmark claim.

## Legend

```text
+----------------------+   permanent owner, component, or durable authority
[temporary compat]         Phase 05 migration-only unit; deleted in Phase 08
---->                      read, validation, or ordinary call
- - ->                     observation or non-authoritative comparison
===>                       durable writer-mode / authority transition
-X->                       forbidden transition

LW                          legacy writes permitted by current generation
LR                          legacy read-only
VW                          ordinary V2 product writes permitted
VI                          V2 writes allowed only through temporary importer
G<n>                        monotone durable generation/fence value
ACTIVATE V2                 irreversible writer-authority boundary
```

The whole authority transfer can be read as a single one-way sequence. The detailed
mode names below add restart and readiness precision without adding another
writer state machine.

```text
 LEGACY_ACTIVE
      ===> DRAIN_AND_FENCE
      ===> IMPORT
      ===> VERIFY
      ===> ACTIVATE_V2             <--- irreversible writer direction
      ===> OBSERVE                 <--- duration is open DEC-011
      ===> REMOVE_COMPATIBILITY

                    safe abort to legacy writer at a NEW generation
          IMPORT / VERIFY -----------------------------------------> LEGACY_ACTIVE
                              allowed only before ACTIVATE_V2

          ACTIVATE_V2 / later -X-> writable legacy
```

## Writer authority before, during, and after cutover

```text
  MODE                         LEGACY             IMPORTER              V2 PRODUCT
  ----                         ------             --------              -----------

  LEGACY_WRITABLE              LW                 off                   rejected
          |
          ===> install drain/fence generation; reject new ingress; drain in-flight
          v
  DRAINING_AND_FENCING         draining only      off                   rejected
          |
          ===> prove drained; install LEGACY_READ_ONLY generation
          v
  LEGACY_READ_ONLY             LR                 off                   rejected
          |
          ===> enable temporary importer only
          v
  IMPORTING_V2                 LR                 VI                    rejected
          |
          |    legacy read -> portable candidate -> ordinary V2 admission
          |    shadow verification; no dual writable selected truth
          v
  V2_VERIFIED                  LR                 stopped/limited       rejected
          |
          |  PRE-ACTIVATION SAFE-ABORT BOUNDARY
          |  (abort protocol must stop importer and prove no V2 product writer)
          |
          ===> ACTIVATE V2: install monotone V2-writer generation
          v
  V2_WRITABLE_                 LR                 off or repair-only    VW
  LEGACY_READ_ONLY
          |
          ===> open ingress only after required fleet/generation proof
          v
  OBSERVING                    LR                 retained compat only  VW
          |
          |  duration selected by owner DEC-011; Must incidents hold cleanup
          v
  COMPAT_REMOVABLE             LR / retained data off                  VW
          |
          ===> Phase 08 deletes compatibility code as one unit; rebuild/retest
          v
  CLEAN V2 ARTIFACT            no legacy writer   absent                VW

  After ACTIVATE V2:
      V2_WRITABLE_LEGACY_READ_ONLY -X-> LEGACY_WRITABLE
      incident response = stop/quarantine/repair V2 or deploy a qualified V2;
      it never re-enables writable legacy.
```

At every committed mode, at most one format has selected-Version writer
authority. During `IMPORTING_V2`, legacy is read-only and only the temporary
importer may call V2 mutation primitives; ordinary V2 product writers remain
fenced. Durable copies in two formats are not dual authority: the active
generation and writer mode identify the one writable truth.

## Generation fence on every mutation

The exact durable record format and fleet-barrier protocol are deferred, but
the decision law is selected.

```text
 mutation request
   carries/observes expected generation Gx and writer class
              |
              v
 +-----------------------------+
 | read and validate durable    |
 | generation + writer mode     |
 | under the owning gate        |
 +---------------+-------------+
                 |
       +---------+----------+----------------+
       |                    |                |
       v                    v                v
 current mode permits    stale Gx /       corrupt, missing,
 this writer class       wrong class      or ambiguous fence
       |                    |                |
       v                    v                v
 enter ordinary          reject before    FAIL CLOSED before
 mutation protocol       any mutation      any mutation/readiness

 Example:

   legacy writer holding G12 ---- after fence advances to G13 ----X-> mutation
   importer with G13 + VI ---------------------------------------> normal V2 API
   ordinary V2 writer -------- before ACTIVATE V2 ---------------X-> mutation
   legacy writer ------------ after ACTIVATE V2 -----------------X-> mutation
```

Every legacy and V2 mutation entry point must consult the same durable mode
law. A check performed only at process startup is insufficient: a process can
become stale while it is running. Exact leases, epochs, record checksums,
acknowledgement sets, and per-request validation placement belong to Phases 05
and 07, but they must prove rejection before mutation.

## One-way import through normal V2 admission

```text
 +---------------------------+
 | legacy durable truth      |
 | fenced read-only          |
 +-------------+-------------+
               |
               | read one in-scope legacy selected view
               v
 [temporary legacy decoder / compatibility adapter]     [DELETE IN PHASE 08]
               |
               | emit portable complete candidate facts
               | (no layer, Docker/OCI, mount, namespace, or host-path identity)
               v
 +-------------+-------------+
 | permanent V2 identity     |
 | validate + canonicalize   |
 | derive typed VersionId    |
 +-------------+-------------+
               |
               v
 +-------------+-------------+
 | permanent LayerStack-0    |
 | ordinary admission path   |
 | occupancy + full-byte     |
 | compare + immutable       |
 | durable payload           |
 +-------------+-------------+
               |
               | AcceptedVersion + AcceptedBinding
               v
 +-------------+--------------------------------------------+
 | ordinary V2 reference authority                         |
 | Branch/Head: CreateHeadIfAbsent(Expected::Absent, ...)  |
 | restore Root: CreateFixedRootIfAbsent(Expected::Absent, |
 |               root_kind, ...)                           |
 +-------------+--------------------------------------------+
               |
               +----> verify mapping and readable complete Version
               |
               - - -> [temporary migration progress record]
                       retry aid only; never Checkpoint/Root/selected truth

 PERMANENT V2 CORE -X-> legacy decoder/model/progress file
```

The importer is a store-local compatibility seam, not a second store or a
parallel publication algorithm. Re-import must be idempotent or have an
explicitly proven retry law. Corrupt or unrepresentable legacy input is
rejected without creating a partial authoritative V2 Head. An
`OUTCOME_UNKNOWN` result requires authoritative read-back of the exact typed
Head or fixed Root before retry or acknowledgement. Migration never retargets
a fixed Root; pre-activation cleanup uses `RemoveHead(Expected::Exact(...))`
or `RemoveFixedRoot(Expected::Exact(...))` and enters the ordinary retirement
protocol.

## Safe abort and the point of no return

```text
                       BEFORE ACTIVATE V2
                  (ordinary V2 writers never enabled)

 IMPORTING_V2 / V2_VERIFIED
          |
          | abort requested
          v
  1. fence and stop importer
  2. prove no in-flight/import or ordinary V2 writer can mutate
  3. verify legacy durable truth remains readable and unchanged
  4. use the rehearsed monotone-generation runbook to select legacy writer mode
  5. keep any imported V2 data non-authoritative; clean it only by safe protocol
          |
          ===> LEGACY_WRITABLE at a newer generation

 This path is "safe abort" only after Phase 06 proves it in isolation and a
 separately authorized live runbook executes it. It never creates a dual-write
 interval and never rewinds a generation.


                         ACTIVATE V2
                              |
                              ===> durable V2-writer generation installed
                              |
                              v
                         AFTER ACTIVATION

  legacy-writable rollback -X-> forbidden

  allowed incident actions:
    * stop ingress and V2 writers;
    * keep legacy read-only;
    * quarantine or repair V2 using a qualified V2 procedure;
    * deploy another already-qualified V2 artifact;
    * hold observation and compatibility deletion.
```

`ACTIVATE V2` is irreversible in writer direction, not a claim that operations
must continue through an incident. Fail closed and stop are always allowed.
What is forbidden is restoring legacy as writable selected truth after V2 has
accepted ordinary product writes, because V2-only writes may then be lost or
diverge.

## Observation and deletable compatibility unit

```text
 V2_WRITABLE_LEGACY_READ_ONLY
              |
              ===> OBSERVING
              |
              +---- ordinary traffic writes V2 only
              +---- legacy remains read-only
              +---- diagnostics compare/monitor - - -> no authority
              +---- Must incident ------------------> HOLD
              |
              | owner-selected DEC-011 duration completes with no open Must issue
              v
       COMPAT_REMOVABLE
              |
              v
 +-----------------------------------------------------------------------+
 | DELETE AS ONE COMPATIBILITY UNIT                                      |
 |                                                                       |
 | * temporary `legacy_import` module and legacy decoder/model           |
 | * migration-only config and writer-mode branches                      |
 | * importer callers, migration progress records, and migration deps    |
 | * compatibility-only tests and fixtures after their archival purpose  |
 +-----------------------------------------------------------------------+
              |
              | clean rebuild + store/wiring/fence/publish/recover retest
              ===> CLEAN V2 ARTIFACT

 KEEP PERMANENT:
   * V2 identity, admission, roots/heads, OCC, recovery, retirement;
   * monotone writer-generation/fence law needed by normal V2 operation;
   * evidence and retention record required by the approved runbook.

 NOT INCLUDED:
   * physical deletion of legacy durable data -- separately authorized work.
```

`DEC-011` is an open product-owner decision about how long observation must run
before Phase 08 may begin. The architecture supports any finite selected
duration and a hold extension; it does not guess the value. This open decision
does not permit dual writes or writable-legacy rollback.

## Walkthrough

1. Legacy is initially the only writable selected truth. General V2 product
   writes are rejected.
2. A monotone durable generation transition rejects new legacy work and drains
   admitted in-flight work before legacy becomes read-only.
3. The temporary importer is enabled as the only V2 writer class. It reads
   fenced legacy data, translates only portable complete-Version facts, and uses
   the permanent V2 identity, admission, root/head, and OCC paths.
4. Verification establishes the in-scope mapping and readable V2 result. Import
   progress may make retry efficient but cannot decide selected truth.
5. Before ordinary V2 product writers are enabled, the rehearsed abort path can
   stop the importer and select legacy writer mode at a newer generation,
   provided no V2 product writer ever ran and all barriers are proven.
6. `ACTIVATE V2` durably grants ordinary V2 writer authority while legacy stays
   read-only. This is the point after which writer direction never returns to
   legacy.
7. Ingress opens only after every required process/fleet member is consistent
   with the V2 generation. Observation monitors V2-only traffic and holds on a
   Must-class incident.
8. After the owner-selected `DEC-011` duration and all exit criteria pass,
   Phase 08 removes the temporary compatibility unit, creates a clean artifact,
   and reruns critical V2 and fence tests. Legacy data retention or destruction
   remains separately governed.

## Invariants

1. Exactly one format has selected-Version writer authority at every committed
   step; migration never dual-writes legacy and V2 truth.
2. Writer generation is monotone. A stale generation or wrong writer class is
   rejected before mutation.
3. During import, legacy is read-only and ordinary V2 product writers are
   disabled; only the temporary importer may invoke V2 mutations.
4. The importer uses normal V2 identity, admission, collision, root/head, OCC,
   recovery, and resource controls. It cannot create a second truth path.
5. Migration is one-way at the identity boundary: permanent V2 core code never
   depends on a legacy layer model, decoder, or progress record.
6. Before V2 activation, a safe abort requires a complete stop/barrier proof and
   a new monotone generation; it is not a casual mode toggle.
7. After V2 activation, legacy remains read-only forever. Incidents may stop or
   repair V2 but cannot re-enable legacy writes.
8. Import and recovery work are bounded in bytes, items, descriptors, workers,
   retries, and recognizable debt. Over-limit or ambiguous input fails closed.
9. Observation is diagnostic, never writer authority. `DEC-011` changes only
   the earliest allowed compatibility-removal time.
10. The compatibility unit is temporary and deletable as one unit. Physical
    legacy-data deletion is not implied by code removal.

## Selected architecture versus delegated details

| Topic | Status | Boundary |
|---|---|---|
| Single writable truth and no dual-write interval | **SELECTED R0** | Violation reopens Phase 01 and blocks cutover. |
| Store-local, temporary, one-way importer | **SELECTED R0** | No new permanent service/package/database or parallel store truth. |
| Import through ordinary V2 identity/admission/reference primitives | **SELECTED R0** | Migration cannot bypass collision, durability, OCC, or resource laws. |
| Monotone durable writer-generation fence | **SELECTED R0** | Exact record/lease/barrier mechanism is later work. |
| Pre-activation abort; post-activation no writable-legacy rollback | **SELECTED R0** | Phase 06 rehearses both isolated paths; Phase 07 executes only with authorization. |
| Observation before compatibility deletion | **SELECTED R0** | Completion duration is `DEC-011`, still open. |
| Canonical V2 grammar/hash | **DEFERRED PHASE 02** | Importer supplies the same portable facts as any other producer. |
| Migration progress cursor/record, batching, retry encoding | **DEFERRED PHASE 05** | Temporary and non-authoritative; never a Checkpoint; must have deletion notes. |
| Exact generation record, fleet acknowledgement, drain protocol | **DEFERRED PHASE 05/07** | Must prove all mutation entry points and restart behavior. |
| Live timestamps, fleet scope, incident owners, retention | **DEFERRED RUNBOOK/OWNER** | Required before separately authorized Phase 07. |
| Observation duration | **OPEN `DEC-011`, ARCHITECTURALLY ISOLATED** | Controls Phase 08 start only; cannot change writer law. |
| `DEC-017` operation semantics | `OWNER_DEC_OPEN`, isolated | Changes which product calls create candidates; normal V2 admission remains the only durable path. |
| `DEC-018` auth/revoke ordering | `OWNER_DEC_OPEN`, isolated | Application acceptance ordering may vary; it cannot bypass the generation fence or add a writer. |
| Physical legacy-data destruction | **OUT OF SCOPE / SEPARATE AUTHORIZATION** | Not part of Phase 08 compatibility-code deletion. |

## Verification mapping

| Diagram claim | Required later proof |
|---|---|
| Legacy-to-V2 mapping is total for in-scope roots | Phase 05 `M1` |
| Re-import is idempotent or has an explicit retry law | Phase 05 `M2` |
| Corrupt legacy cannot create partial authoritative V2 head | Phase 05 `M3` and `MC1` |
| Shadow comparison reports expected matches/known differences without authority | Phase 05 `M4` |
| Stale generation writer rejects before mutation and fence survives restart | Phase 05 `M5`, `MC2` |
| Compatibility unit has a concrete deletion boundary | Phase 05 `M6` |
| Abort-to-legacy and V2-forward paths work independently on one frozen artifact | Phase 06 `Q1`-`Q7`, especially `Q5` and `Q6` |
| Live cutover has all writers fenced and no dual writable step | Phase 07 `L1`-`L5` |
| Restart uses durable cutover facts; incident does not restore legacy writes | Phase 07 `LI1` and `LI2` |
| Observation completes or records an explicit hold | Phase 07 `L6` plus owner-selected `DEC-011` value |
| Clean artifact has no migrator path and preserves store/writer laws | Phase 08 `R1`-`R5` plus critical Phase 03 crash retest |
| Legacy data retention is explicit and not silently destroyed | Phase 08 `R6` and separate deletion authorization if ever requested |

Performance measurement in Phases 05-08 is capacity and regression evidence
under their specified protocols. Stage 4.6 remains `INCOMPARABLE` and cannot
authorize cutover, select a winner, or imply a numerical V2 guarantee.

## Reopening conditions

Reopen Phase 01 before proceeding if any of these becomes necessary:

- legacy and V2 must both accept selected-Version writes at any committed step;
- migration requires a permanent new service, database, registry, coordinator,
  or second store authority;
- importer output cannot enter through the normal V2 complete-Version identity,
  collision, admission, root/head, and OCC contracts;
- the generation fence cannot cover every legacy and V2 mutation entry point or
  cannot reject stale processes before mutation;
- activating V2 requires writable-legacy rollback as an incident strategy;
- permanent V2 code must depend on a legacy layer/history model, progress
  record, runtime-private identity fact, or reference-path payload copying; or
- the compatibility unit cannot be removed without redesigning selected-Version
  ownership or the V2 storage family.

A failed Phase 05/06/07 proof does not justify weakening an invariant. It
blocks the phase, records exact evidence, and reopens Phase 01 only if the
failure changes architecture rather than an implementation detail.

## Related documents

- [Architecture design](../architecture_design.md)
- [Migration and cutover design](../design/08-migration-and-cutover.md)
- [LayerStack-0 Version-storage design](../design/03-state-store.md)
- [Concurrency, durability, and recovery](../design/05-concurrency-durability-recovery.md)
- [Resources, security, and observability](../design/06-resources-security-observability.md)
- [Source and implementation map](../design/09-source-and-implementation-map.md)
- [Phase 01 selection input contract](../phases/01-choose-design/SPEC.md)
- [Phase 05 migrator checks](../phases/05-migrator/test-perf.md)
- [Phase 06 offline proof](../phases/06-prove-offline/test-perf.md)
- [Phase 07 go-live checks](../phases/07-go-live/test-perf.md)
- [Phase 08 clean-release checks](../phases/08-clean-release/test-perf.md)
