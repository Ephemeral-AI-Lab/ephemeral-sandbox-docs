# Migration and cutover

**Status:** `LOCKED_PHASE_01` architecture with Phase 05/07/08 details pending  
**Owners:** existing lifecycle owners plus a temporary store-local importer  
**Open owner decision:** `DEC-011` observation-window duration

## Purpose

Define the only permitted path from legacy LayerStack truth to LayerStack-0.
Migration is subordinate to normal V2 identity, admission, root/head,
and recovery contracts. It is not a second store design, dual-write bridge, or
permanent compatibility service.

Authority: product [hard rule 9](../PRD.md#hard-rules-must-never-break), the
selected [migration architecture](../architecture_design.md#10-migration-architecture),
and the Phase 05 [PRD](../phases/05-migrator/PRD.md).

## Non-negotiable invariants

1. Exactly one format is writable selected-Version truth at every point.
2. Legacy mutating ingress is drained and fenced before the importer creates
   authoritative V2 references.
3. The importer decodes legacy input into complete portable candidate facts and
   calls ordinary V2 validation, identity, admission, and reference APIs.
4. The importer never writes an alternate V2 layout or bypasses exact
   occupied-ID comparison.
5. V2 product writers start only under a monotone V2 generation in which legacy
   remains read-only.
6. There is no dual-write rollback after V2 becomes writable.
7. Permanent identity/store code does not depend on legacy types.
8. Migration-only code, config, tests, features/targets, progress records, and
   call sites form one named deletion unit for Phase 08.
9. Removing legacy data is a separately authorized operation, not implied by
   removing migration code.
10. Unknown/corrupt legacy facts or ambiguous progress fail closed without a
    partial authoritative V2 head.

## Authority and component placement

| Responsibility | Owner | Boundary |
|---|---|---|
| Fleet/process drain, readiness and generation installation | Existing manager/daemon lifecycle owners | May fence and invoke migration; may not write store paths directly. |
| Legacy decoding | Temporary `legacy_import` module/feature/target inside `crates/sandbox-runtime/layerstack` | Produces validated candidate input; cannot become a permanent store dependency. |
| Canonicalization and `VersionId` | Permanent internal identity module | Has no legacy types or migration modes. |
| Payload/root/head mutation | Permanent LayerStack-0 owner | Uses the same admission/OCC/durability path used after migration. |
| Product traffic enablement | Existing application/lifecycle owners | V2 writes remain disabled until the installed generation makes V2 sole writable truth. |
| Diagnostics | Existing observability readers | Report progress/failures without becoming fence or truth authority. |

The importer adds no service, process, RPC protocol, deployment unit, durable
authority, or independent resource pool. If a concrete privilege or process
invariant requires one, stop and reopen Phase 01 with the exact R0 failure and
costs.

## Migration modes and legal transitions

Names describe semantic modes; Phase 05 selects exact record names and encoding.

```text
LEGACY_WRITABLE
    -> DRAINING_AND_FENCING
    -> LEGACY_READ_ONLY
    -> IMPORTING_V2
    -> V2_VERIFIED
    -> V2_WRITABLE_LEGACY_READ_ONLY
    -> OBSERVING
    -> COMPAT_REMOVABLE
```

| Mode | Permitted selected-Version writers | Product traffic | Durable requirement |
|---|---|---|---|
| `LEGACY_WRITABLE` | Legacy only | Legacy traffic as currently authorized | Existing truth; no V2 authority implied. |
| `DRAINING_AND_FENCING` | No newly admitted writer after the cutoff; in-flight legacy work drains according to the chosen lifecycle protocol | Mutating ingress closed or rejected | Monotone target generation and complete writer inventory are established. |
| `LEGACY_READ_ONLY` | None | Reads/inspection needed for import only | Legacy cannot resume mutation under the new generation. |
| `IMPORTING_V2` | Temporary importer through permanent V2 APIs only | General V2 mutating traffic disabled | Progress is restart-safe; accepted payloads/references use normal V2 durability. |
| `V2_VERIFIED` | Importer only if bounded completion repair remains; otherwise none | Still not generally writable | Total in-scope root mapping and integrity/read checks pass. |
| `V2_WRITABLE_LEGACY_READ_ONLY` | Ordinary V2 store writer only | V2 traffic enabled on the frozen artifact | Installed generation rejects every legacy writer and stale V2 generation. |
| `OBSERVING` | Ordinary V2 store writer only | V2 live | Legacy remains read-only; migration compatibility remains available only as the approved runbook allows. |
| `COMPAT_REMOVABLE` | Ordinary V2 store writer only | V2 live | Owner has accepted the `DEC-011` observation result; Phase 08 may build a new clean artifact. |

No transition returns from `V2_WRITABLE_LEGACY_READ_ONLY` to a writable legacy
mode. Operational rollback after that point means stop/quarantine/repair V2 or
deploy another qualified V2 artifact—not restore dual truth.

## Generation fence contract

Phase 05 must select a monotone, integrity-checkable generation/mode record and
prove every inventoried writer consults it before mutation. The exact encoding
is `SELECT_IN_PHASE_05`; these semantics are fixed:

- every legacy and V2 selected-Version writer is inventoried;
- a writer binds its attempt to the installed generation;
- an outdated or wrong-mode writer fails before selected-Version mutation;
- generation comparison cannot be bypassed through a transport, internal
  operation, retry path, recovery path, or administrative command;
- fence installation and readiness ordering are crash-safe and restart-safe;
- ambiguous/corrupt generation state fails readiness closed;
- the fence remains permanent where needed to prevent legacy resurrection even
  after the temporary importer is removed.

Open `DEC-018` may change application authorization/revocation ordering, but it
does not permit a fence bypass or a second selected-Version writer.

## Legacy-to-Version mapping contract

The importer converts one selected legacy view, not one legacy layer, into one
complete Version candidate. The permanent result chain is:

```text
LegacySelectionKey
    -> CompletePortableCandidate
    -> VersionId
    -> AcceptedVersion
    -> AcceptedBinding
    -> target Head or Checkpoint Root
```

| Legacy artifact or fact | V2 disposition |
|---|---|
| Selected `manifest.json` view plus `layers/` and `base/` content | Decode into one complete portable candidate; admit one complete Version. |
| Layer IDs, parents, depth, changesets, squash/merge records, and whiteout-as-delta operations | Temporary decoder inputs only; never Version identity, permanent truth, or a Version relation. |
| Current selected branch/head | Map with `CreateHeadIfAbsent(head_identity, Expected::Absent, binding)` only when required by the product migration scope; an already-present nonidentical record is a conflict, not a retarget. |
| Explicit user restore point | Map with `CreateFixedRootIfAbsent(root_identity, Checkpoint, Expected::Absent, binding)`. A historical layer is not automatically a checkpoint, and a Checkpoint Root is never retargeted. |
| `/eos/workspace` sessions, mounts, upper/lower/work dirs, namespaces, and host paths | Runtime-private; exclude from Version identity. Live uncommitted work requires an explicit drain/resolve policy before import. |
| `/eos/storage/file_auditability` | Separate attribution side channel governed by open `DEC-001`; never infer file blame from Version storage. |
| `/eos/storage/workspace_recovery` | Recovery side channel, not portable identity or selected durable truth. |

Migration progress records use a dedicated name and type. They are retry
evidence for `LegacySelectionKey -> VersionId -> AcceptedVersion ->
AcceptedBinding -> TargetReference`; they are never called checkpoints and never create product
reachability.

The importer consumes the exact non-overlapping root/layout and public APIs
selected by Phase 03. It never constructs a V2 path or writes a payload,
reference, or control record directly. CDC, chunk stores, object DAGs, and
`VersionView` indirection are not selected migration mechanisms.

## Import algorithm contract

For each in-scope legacy root:

1. Resolve the legacy root under the fenced, read-only legacy generation.
2. Decode exactly one selected legacy view; do not treat historical parents,
   depth, mergeability, squash policy, runtime mounts, or host paths as V2
   identity.
3. Validate legacy facts and convert them to the complete portable candidate
   interface selected by Phase 02.
4. Invoke the normal identity stream and receive a typed candidate `VersionId`.
5. Invoke normal V2 admission. An occupied ID requires full canonical-byte
   comparison; equality reuses the accepted payload and inequality is a typed
   collision.
6. Receive the resulting `AcceptedVersion`/`AcceptedBinding`; a raw
   `VersionId` is not proof that the payload exists.
7. Record restart-safe progress only after the corresponding permanent V2
   admission/reference durability point.
8. Publish a mapped branch/head only with
   `CreateHeadIfAbsent(head_identity, Expected::Absent, binding)` and an
   explicit restore point only with `CreateFixedRootIfAbsent(root_identity,
   Checkpoint, Expected::Absent, binding)`. Never write a raw digest or direct
   filesystem reference, replace a Root, or bypass the single reference
   authority.
9. Re-read/validate the V2 result against the imported portable facts.
10. Continue within finite resource and cleanup limits.

The mapping output is deterministic for the same accepted legacy view and
identity domain. Retry converges through exact admission, exact create-if-absent
comparison, authoritative reference read-back after `OUTCOME_UNKNOWN`, and
explicit progress; it cannot silently skip a reference because a name or
digest is merely present.

## Progress, retry, and failure behavior

Phase 05 selects exact progress encoding, but must cover:

| Event | Required result |
|---|---|
| Crash before V2 admission | No authoritative V2 reference; private staging is normal bounded recovery debt. |
| Crash after payload admission but before root/head | Complete unreferenced payload is safe bounded debt; retry exact-admits/reuses it. |
| Crash after Root/Head durability but before progress acknowledgement | `OUTCOME_UNKNOWN`; retry authoritatively reads the complete record, accepts only an exact intended create-if-absent result, and records progress without duplicating payload. |
| Corrupt/unsupported legacy entry | Typed failure; no partial authoritative mapping for that root. |
| Occupied digest with unequal canonical bytes | Typed collision; no reference mutation. |
| Stale/wrong generation | Reject before mutation and report the installed generation diagnostically. |
| Resource exhaustion or ENOSPC | No reference publication; cleanup private state or leave bounded recognizable debt. |
| Incomplete writer inventory or fence bypass | Stop migration/cutover; do not compensate with dual writes. |
| Restart with ambiguous progress | Fail closed and require bounded diagnosis/repair; never guess completion. |

Migration progress is not a checkpoint, root, or second head and cannot
override store truth. The
permanent store must remain readable/recoverable if the progress record is
absent after compatibility deletion.

## Verification before V2 enablement

Phase 05 must produce, and Phase 06 must re-run on the exact ship candidate:

- total legacy-root inventory for the declared in-scope population;
- deterministic legacy-selection to `VersionId`, `AcceptedVersion`,
  `AcceptedBinding`, and target-reference mapping;
- semantic/read comparison against the Phase 00 fixture categories used;
- physical payload count for equal imported Versions;
- forced collision behavior;
- corrupt/unsupported input behavior;
- restart at every progress/durability cut;
- complete writer inventory and generation-fence bypass tests;
- proof that V2 product writes remain disabled during import;
- proof that the Phase 03 V2 namespace and all migration writes cannot alias
  legacy paths;
- bounded peak scratch, memory, FDs, workers, debt, and cleanup plateau;
- source/dependency proof that permanent identity/store code does not import
  temporary legacy types.

Phase 06 qualifies one exact artifact. A later code or configuration change
invalidates the corresponding proof until the changed artifact is requalified.

## Live cutover contract

Phase 07 requires separate live authorization. It must:

1. identify the exact Phase 06-qualified source, binary, configuration and
   evidence bundle;
2. confirm backups/runbooks and the complete writer inventory;
3. drain/close legacy mutation and install the V2 generation fence;
4. verify legacy rejection and V2 readiness before opening V2 traffic;
5. enable V2 writers while legacy remains read-only;
6. monitor store readiness, OCC/stale/collision failures, dangling/corrupt
   records, resource usage, cleanup debt and product error rates;
7. stop or quarantine on Must-class incidents rather than re-enable legacy
   writes; and
8. observe for the product-owner-selected `DEC-011` window.

This document neither authorizes live execution nor decides the observation
duration.

## Compatibility deletion boundary

After the owner accepts the observation window, Phase 08 deletes as one bounded
unit:

- the `legacy_import` module/feature/target;
- legacy decoder/model types used only by import;
- migration-only configuration and mode branches;
- importer CLI/manager/daemon/application call sites;
- migration-only progress handling;
- migration-only dependencies;
- compatibility-only tests and fixtures, except evidence fixtures deliberately
  retained for permanent regression coverage; and
- dead documentation/runbook paths that could imply import is still callable.

Phase 08 then builds and re-runs required proof on the clean artifact before
deployment. The permanent generation fence and V2 invariants remain. Legacy
data may remain read-only until a separately authorized deletion operation.

## Open decisions and stable seams

| Decision | Status | Effect that remains within R0 | Reopen trigger |
|---|---|---|---|
| `DEC-011` observation duration | `OWNER_DEC_OPEN` | Changes when Phase 08 may start. | Owner requires dual writes or writable legacy rollback. |
| `DEC-017` operation semantics | `OWNER_DEC_OPEN` | Changes which app calls produce Candidates; all publish through V2. | Requires direct Accepted-Version mutation. |
| `DEC-018` auth/revoke ordering | `OWNER_DEC_OPEN` | Application orders acceptance; generation and store OCC remain mandatory. | Requires joint auth/store durable authority or another writer. |
| Exact progress/fence record encoding | `SELECT_IN_PHASE_05` | Internal temporary/permanent lifecycle detail with fail-closed semantics. | Requires second truth, service, process or permanent legacy dependency. |

## Stop and reopen conditions

Stop cutover immediately if migration requires dual writes, legacy mutation
after V2 enablement, bypass of ordinary V2 admission, permanent legacy types in
identity/store, an unbounded import/recovery population, or a second selected
Version authority. Reopen Phase 01 if satisfying the requirement changes R0's
owner, storage family, process/dependency boundary, writer count, crash model,
or identity boundary.

Related: [Version identity](02-state-identity.md) · [LayerStack-0 storage](03-state-store.md)
· [algorithms](04-algorithms-and-call-flows.md) ·
[verification matrix](10-verification-matrix.md)
