# 01.03 — Complete-Version content addressing and convergence

## 1. Purpose and owning phases

**Owners:** Phase 02 constrains canonical portable facts and typed `VersionId`
derivation. Phase 03 LayerStack-0 owns reservation, occupied-address equality,
complete payload installation, AcceptedVersion admission, and AcceptedBinding
issuance or revalidation.  
**Purpose:** Make the content-derived part of R0 explicit and demonstrate how
equal complete canonical Versions converge to one physical payload closure
without introducing a cross-Version object store.

This document is a focused composition of
[canonical Version identity](01-canonical-version-identity.md) and
[complete Version admission](02-complete-version-admission.md). It does not add
another identity, storage owner, or durable primitive.

```text
R0_CONTENT_ADDRESSING_SCOPE:
  one complete canonical Version value

NOT_SELECTED:
  cross-Version object CAS
  content-defined chunking (CDC)
  Chunk indexes or manifests
  Merkle/object DAGs
  object-graph reachability or GC
```

The abbreviation “CAS” may describe the content-derived lookup property of the
complete Version as a comparison aid. It does not name a selected CAS service,
object API, Chunk store, or second authority.

## 2. Evidence status

- `SOURCE-VERIFIED`: the sealed e497 base and Phase 00 evidence place the
  rewrite in `sandbox-runtime-layerstack` and preserve direct calls from
  application owners to existing runtime-effect owners.
- `SPIKE-VERIFIED`: none; no V2 canonical convergence, forced-collision, or
  resource-bound spike has run.
- `INFERRED`: complete-Version addressing, per-`VersionId` reservation,
  full-canonical-byte equality, collision rejection, and convergence on one
  complete payload are selected R0 design consequences.
- `OPEN`: Phase 02 selects canonical grammar, hash, domain/schema separation,
  and limits. Phase 03 selects path/record spellings, reservation mechanics,
  checksums, fences, supported filesystems, and finite bounds. These are
  `OPEN_WITHIN_R0`.

## 3. Authority and data model

```text
Candidate
  -> VersionId
  -> AcceptedVersion
  -> AcceptedBinding
  -> Head + HeadRevision or typed Root
```

This algorithm ends at `AcceptedBinding`. It cannot create a Head or Root.

The addressable durable unit is exactly:

```text
canonical bytes for one complete portable Version
  +
one complete immutable filesystem-native payload closure
```

Canonical bytes are retained or reproducibly available as Phase 03-qualified
comparison material. A digest, serialized `VersionId`, byte length, directory
existence, or payload-name match is never sufficient to declare equality.

## 4. Contract

Conceptual operation names below express responsibility and type flow. They are
not selected Rust signatures, codec bytes, hash algorithms, or disk names.

### Inputs

- A bounded Candidate containing only Phase 02-qualified portable facts.
- Canonical bytes produced deterministically for the complete Candidate.
- A typed, domain/schema-separated `VersionId` derived from every canonical
  byte.
- Finite entry, byte, path, metadata, memory, descriptor, worker, staging,
  reservation-wait, cleanup-debt, and deadline budgets.

### Preconditions

1. Candidate facts passed bounded portable validation; runtime-private facts,
   mount paths, host paths, namespaces, sessions, OverlayFS details, legacy
   layer identifiers, and process data are excluded.
2. Canonicalization is deterministic for the selected schema and consumes the
   entire logical Version value.
3. The caller has no authority to infer acceptance from a `VersionId`.
4. LayerStack-0 is ready on the active generation and can reserve enough private
   staging plus cleanup headroom.
5. The operation uses LayerStack-0's unique admission boundary; no database,
   service, facade, helper process, or second writer participates.

### Outputs and typed outcomes

| Outcome | Meaning |
|---|---|
| `AdmittedNew(AcceptedVersion, AcceptedBinding)` | One complete payload and its canonical comparison material became durably accepted, then admission issued a binding. |
| `ConvergedExisting(AcceptedVersion, AcceptedBinding)` | The occupied address contained byte-for-byte equal complete canonical bytes; no second accepted payload was installed, and admission revalidated/issued the binding. |
| `VersionIdCollision` | The occupied address had any canonical-byte mismatch or unequal exact end; the occupant remains authoritative and unchanged. |
| `InvalidCandidate(reason)` | Portable validation or canonicalization failed before acceptance. |
| `ResourceLimit(kind)` | A finite byte, entry, memory, FD, worker, staging, wait, disk-reserve, or debt bound prevented safe work. |
| `CancelledPrivate` | Cancellation occurred before accepted visibility; private staging is removed or charged as bounded cleanup debt. |
| `OutcomeUnknown` | A crash/lost acknowledgement may have crossed accepted visibility; recovery or ordinary idempotent re-admission must classify the slot. |
| `StoreNotReady` | Generation, recovery, filesystem qualification, corruption, or debt blocks admission. |

No outcome returns a raw `VersionId` as a reference capability.

## 5. Complete-Version addressing algorithm

```text
address_complete_candidate(candidate, budgets):
    reserve conservative bounded identity/admission resources
    validate every portable fact and checked aggregate limit
    canonical := deterministically emit complete canonical bytes
    version_id := derive typed domain/schema-separated identity(canonical)

    # Candidate identity only: no equality or existence conclusion yet.
    cancellation_checkpoint()
    acquire bounded LayerStack-0 reservation for version_id

    if accepted slot for version_id exists:
        occupant := validate complete accepted slot metadata
        comparison := compare full canonical byte streams to exact end
        if comparison is not EXACT_EQUAL:
            release reservation
            discard/charge private work
            return VersionIdCollision

        binding := LayerStack0Admission.revalidate_or_issue(occupant)
        release reservation
        return ConvergedExisting(occupant, binding)

    stage := allocate private bounded transaction
    retain canonical comparison material under the transaction
    construct one complete filesystem-native payload from candidate
    validate completeness, portable projection, and reserved totals
    cancellation_checkpoint()

    make complete comparison material and payload durable and immutable
        using the Phase 03-qualified ordering/fence contract
    install exactly one complete accepted slot for version_id

    accepted := validate accepted closure and canonical binding
    binding := LayerStack0Admission.issue(accepted)
    release reservation
    return AdmittedNew(accepted, binding)
```

The compare routine is length-sensitive but does not accept on length:

```text
compare_full_canonical(left, right):
    while either bounded stream has data:
        read next bounded buffer from each
        if buffer bytes differ: return MISMATCH
        if only one stream reached end: return MISMATCH
    return EXACT_EQUAL
```

An implementation may fail earlier on the first mismatch. Equal results require
reading both streams to exact end. Hash or length checks may reject cheaply,
but they may not accept cheaply.

## 6. Visibility and linearization

The durable visibility point for a new AcceptedVersion is the Phase
03-qualified installation of one complete accepted slot after canonical
comparison material and the complete immutable payload satisfy the selected
payload-before-reference fence. Exact syscall order is still open.

For an occupied equal address, there is no new payload visibility point. The
operation linearizes for admission at validation of the existing complete slot
and exact full-byte equality while its `VersionId` reservation excludes a
conflicting installer. Issuing/revalidating an AcceptedBinding remains an
admission-owned act.

Neither point is a Head transition. The only Head linearization point remains
the conditional complete Head-record replacement defined by
[OCC publication](../02-references-and-publication/02-occ-publication.md).

## 7. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal new Candidate | Validate, canonicalize, reserve, construct one complete closure, durably install it, and issue a binding. |
| Normal equal occupant | Compare every canonical byte to exact end, converge on the existing closure, and write/copy accepted payload bytes `0/0`. |
| Collision | Preserve the occupied closure, return `VersionIdCollision`, and never overwrite, alias, salt, or create a second occupant under the same ID. |
| Concurrent equal admissions | One reservation holder installs or confirms; followers perform full equality and converge on the same complete closure. |
| Concurrent unequal collision | At most one complete accepted occupant exists; every unequal contender fails collision after exact comparison. |
| Retry | Recompute/revalidate normally. Existing equal occupancy makes the retry idempotently converge; no unchecked “already exists” shortcut is allowed. |
| Cancellation | Before accepted visibility, remove or debt-charge staging. After possible visibility, return unknown and use recovery/re-admission; never remove a valid occupant speculatively. |
| Crash | Recovery classifies private, complete-but-uninstalled, installed-complete, ambiguous, and corrupt prefixes; incomplete/ambiguous slots do not yield bindings. |
| Cleanup | Remove bounded private staging and unreachable accepted orphans through whole-Version lifecycle rules; never trace a Chunk graph. |

## 8. Finite resources and complexity

Let:

- `E` be the complete portable entry count;
- `B` be complete canonical bytes;
- `P_path` be aggregate portable path bytes;
- `V` be logical complete-payload bytes;
- `Ops_fs` be filesystem construction and durability metadata operations;
- `M_order` be the Phase 02-bounded canonical ordering state;
- `w` and `b` be bounded workers and per-worker streaming buffer;
- `S_tx` be private transaction space, including canonical comparison material;
- `L_id` be bounded wait for the per-`VersionId` admission reservation.

| Path | Worst-case time | Byte I/O | Peak private resources |
|---|---:|---:|---:|
| Validate/canonicalize | `O(B + P_path + E log E)` for comparison sorting | Reads all Candidate facts; emits `B` canonical bytes | `O(M_order + w*b)`, selected strategy bounded |
| Derive `VersionId` | `O(B)` | Reads all `B` canonical bytes | fixed digest state plus bounded buffer |
| Occupied exact equality | `O(B)` worst case | Up to `2B` canonical bytes read; accepted payload writes/copies `0/0` | `O(b)` comparison buffers plus reservation |
| New complete admission | `O(B + V + E + Ops_fs + L_id)` plus ordering | Candidate/canonical reads and `O(B + V)` private/accepted writes | `O(M_order + w*b)`, `O(S_tx)`, bounded FDs/workers |
| Collision/retry after construction | New-attempt cost plus `O(B)` compare | Private writes may already be `O(B + V)`; occupant unchanged | bounded cleanup debt if immediate reclaim fails |

Every input and aggregate uses checked arithmetic. LayerStack-0 reserves staging
and cleanup headroom before growth. At memory, FD, worker, disk, wait, or debt
exhaustion it backpressures or fails closed without installing a partial
AcceptedVersion.

## 9. Security and path validation

- Treat every Candidate fact, path component, link target, metadata value,
  declared length, sparse extent, and content stream as untrusted.
- Reject absolute paths, traversal, NUL/invalid encoding under the selected
  portable grammar, duplicate/case-colliding aliases where the qualified
  profile forbids them, escapes through links, unsupported special files, and
  depth/entry/byte amplification.
- Resolve construction beneath a private capability-scoped staging root; never
  join caller text to `<LayerStack0Root>` directly and never follow ambient
  symlinks.
- Use checked lengths and exact-end comparison; timing or early mismatch
  behavior must not leak payload contents beyond the authorized admission
  boundary.
- Protect canonical comparison material with the same confidentiality and
  integrity policy as the payload. Diagnostic labels must not contain paths or
  contents.

## 10. Observability and demonstration seams

Required scoped facts include Candidate/canonical bytes, entries, path bytes,
ordering scratch, reservation wait, compare bytes per side, exact-end reached,
new/equal/collision outcome, staging high-water mark, accepted payload count,
private cleanup debt, FDs, workers, fence latency, cancellation side, and crash
classification.

Required tests include:

- deterministic golden/corrupt canonical vectors selected by Phase 02;
- equal Candidates produced through different traversal orders;
- same digest and length with an injected canonical-byte mismatch;
- mismatched exact end after an otherwise equal prefix;
- two and many concurrent equal admissions converging on one payload closure;
- unequal concurrent contenders never producing two occupants;
- retry and response loss around every durable prefix;
- input/path/size/FD/worker/disk/debt limit boundaries; and
- proof that equal occupied admission writes and copies accepted payload bytes
  `0/0`, while its canonical comparison reads remain nonzero and visible.

Observability is diagnostic only. A metric, index, cache, or dashboard cannot
declare existence/equality, install a payload, or issue a binding.

## 11. Details owning phases may still select

Phase 02 may select the exact portable schema, canonical grammar and ordering,
domain/schema bytes, digest algorithm/width/serialization, streaming strategy,
limits, and collision-test hook. Phase 03 may select non-overlapping paths,
records, checksums, generations, reservation/lock mechanics, supported
filesystem, durability fences, immutable enforcement, staging strategy,
budgets, and metric names.

Those choices may optimize one complete Version but may not introduce
cross-Version Chunks, a manifest/Merkle DAG, reconstruction parents/layers,
raw-ID reference authority, persistent object refcounts, or another writer.

## 12. `REOPEN_PHASE_01` conditions

Return `REOPEN_PHASE_01 — <specific architecture-changing failure>` if evidence
proves that:

- bounded deterministic portable canonicalization cannot represent a required
  complete Version;
- full occupied-ID canonical equality cannot be made finite and fail closed;
- equal complete canonical Versions cannot converge on one complete payload
  without violating a hard rule;
- a complete filesystem-native immutable payload cannot meet a hard product
  rule without object/Chunk reconstruction;
- admission-issued/revalidated bindings cannot remain solely inside
  LayerStack-0; or
- a selected and comparably measured hard target proves this complete-Version
  storage family cannot qualify.

The reopening report must identify the exact R0 failure, why the current direct
owner cannot repair it, and all dependency, crash, resource, migration, and
operating costs of the replacement. A generic claim that CAS+CDC might dedupe
better is not reopening evidence.
