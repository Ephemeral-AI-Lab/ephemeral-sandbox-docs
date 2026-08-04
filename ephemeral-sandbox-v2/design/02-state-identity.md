# R0 Version identity design

Status: **PHASE 01 CONTRACT — exact Phase 02 selections pending**  
Owner: Phase 02, implemented as a pure internal module in
`crates/sandbox-runtime/layerstack`  
Authority: product [hard rules](../PRD.md#hard-rules-must-never-break) and the selected
[R0 architecture](../architecture_design.md)

## 1. Purpose and decision boundary

This document turns the selected R0 architecture into the implementation
contract for portable Version identity. It does not choose a second architecture,
an exact codec, or an exact digest. Phase 02 must fill the explicitly marked
local choices and prove them with the checks in the Phase 02
[test contract](../phases/02-state-identity/test-perf.md).

The status labels used here are normative:

| Label | Meaning |
|---|---|
| `LOCKED_PHASE_01` | Required by R0; Phase 02 may implement but may not weaken or replace it. |
| `SELECT_IN_PHASE_02` | Phase 02 must select and document the exact choice inside the R0 boundary. |
| `SELECT_IN_PHASE_03` | Store-owned detail; identity must expose the needed pure capability without selecting storage mechanics. |
| `OWNER_DEC_OPEN` | Product-owner choice remains open and cannot be silently accepted here. |
| `REOPEN_PHASE_01` | Evidence would invalidate the selected owner, storage family, or identity boundary. |

## 2. Fixed identity contract

| Subject | Required result | Status |
|---|---|---|
| Meaning | One `VersionId` is derived from one complete portable filesystem value, not a layer, parent chain, Workspace, or runtime instance. | `LOCKED_PHASE_01` |
| Canonical form | All accepted portable facts have one versioned, domain-separated, unambiguous deterministic byte representation. | `LOCKED_PHASE_01` |
| Enumeration order | Equivalent qualified facts produce identical canonical bytes regardless of input enumeration order. | `LOCKED_PHASE_01` |
| Identifier | `VersionId` is a typed digest of the entire canonical byte stream. It may be computed before admission and is neither equality proof nor durable-existence proof. | `LOCKED_PHASE_01` |
| Occupied ID | The store must compare full canonical bytes. Equal bytes reuse the payload; unequal bytes return a collision. | `LOCKED_PHASE_01` |
| Bounds | Validation, canonicalization, hashing, decoding, and exact comparison must operate within finite documented CPU, memory, entry, depth, and byte limits. | `LOCKED_PHASE_01` |
| Purity | Identity code performs no store I/O, mount operation, workspace policy, authorization, OCC, recovery, migration, or publication. | `LOCKED_PHASE_01` |
| Portability | Identity types and bytes exclude Docker, OCI, OverlayFS, mount, namespace, workspace, session, host-path, process, lease, and policy facts. | `LOCKED_PHASE_01` |
| Test seam | Tests can force two unequal canonical streams to occupy the same candidate ID without weakening production digest derivation. | `LOCKED_PHASE_01` |
| Source home | Pure internal module at `crates/sandbox-runtime/layerstack/src/identity.rs` or `src/identity/**`; no new crate or service. | `LOCKED_PHASE_01` |

## 3. Portable fact boundary

### 3.1 Required structure of accepted facts

A candidate represents one complete qualified portable filesystem value. For every entry class Phase
02 accepts, canonical facts must encode every semantic property needed to
distinguish two portable filesystem values. At minimum the fact model must have an explicit
answer for:

| Fact class | Contract | Exact Phase 02 work |
|---|---|---|
| Identity domain/schema | Included in canonicalization so incompatible meanings cannot alias. | Select version and domain separation. |
| Relative name | Canonical, store-independent relative path for every represented entry. | Select normalization, encoding, separator, component, and ordering grammar. |
| Entry kind | The kind is explicit; a file, directory, and link cannot share an encoding. | Select accepted kinds and stable tags. |
| Regular file | Exact content bytes and all explicitly portable semantics are represented. | Select streaming form and permitted metadata. |
| Directory | Existence and any accepted portable semantics are represented even when empty. | Select directory record and ordering rules. |
| Symbolic link | Encode the link target as portable data and never follow it during identity processing. | Select target encoding and validation rules. |
| Metadata | Every class is explicitly canonicalized or rejected; no host-walk default leaks into identity. | Decide modes, executable bit, ownership, timestamps, xattrs, ACLs, sparse/extents, and related classes one by one. |
| Completeness | Missing, duplicate, conflicting, or structurally impossible entries fail closed. | Select tree-validation rules and typed errors. |

“Complete” does not require accepting every Unix filesystem object. It requires
the accepted fact grammar to describe the entire qualified Version without an
implicit parent/layer and to reject unsupported facts explicitly. Phase 02 may
choose a narrower portable profile if normal product Versions can be represented
and unsupported inputs fail closed.

### 3.2 Facts forbidden from identity

The following must not appear in portable fact types, canonical bytes, or
`VersionId` derivation:

- Docker image, container, volume, or driver identifiers;
- OCI descriptors or runtime configuration;
- OverlayFS lower, upper, work, whiteout-as-delta, or mount details;
- mount identifiers, options, handles, or materialization locations;
- namespace, cgroup, process, thread, or file-descriptor identity;
- host absolute paths, store-root paths, payload paths, device/inode identity,
  or workspace/session paths and IDs;
- mutable workspace generation handles or runtime leases;
- application authorization, audit, request, tenant-policy, MCTS, rollout, or
  winner-selection data;
- legacy layer IDs, parents, changesets, merge/squash history, depth, or leases;
- nondeterministic host enumeration order, wall-clock time, random values, or
  locale-dependent representation.

A local reader handle, read-custody token, accepted binding, Root name, Head
selector, and `HeadRevision` are also not part of canonical Version facts. They
may refer to a Version but must not change its identity.

## 4. Conceptual types

Exact Rust names and representations are `SELECT_IN_PHASE_02`; the semantic
separation is `LOCKED_PHASE_01`.

```text
PortableEntry       validated portable facts for one qualified entry
PortableVersionFacts one complete bounded collection/stream of PortableEntry
CanonicalVersion    explicit identity schema/domain version
CanonicalBytes      deterministic complete byte stream (not necessarily held in memory)
VersionId           typed digest over CanonicalBytes; computable before admission
CanonicalSummary    VersionId plus bounded counts/lengths needed by the caller
IdentityLimits      finite validation/canonicalization limits
IdentityError       typed invalid/unsupported/limit/corrupt failure
```

These LayerStack-0 concepts are deliberately not identity types:

```text
AcceptedVersion     LayerStack-0-admitted complete payload; not an identity type
AcceptedBinding     LayerStack-0-issued capability naming an AcceptedVersion
HeadRevision        LayerStack-0-owned OCC version
RootRecord          LayerStack-0-owned durable reachability
HeadRecord          LayerStack-0-owned durable selected reference
ReadCustody         LayerStack-0-owned runtime protection
```

In particular, `VersionId -> AcceptedVersion` and `VersionId ->
AcceptedBinding` are never pure casts or public constructors. Only LayerStack-0
may admit a Version and issue or revalidate its binding after checking
occupancy and full canonical equality. The pure identity module can produce a
candidate `VersionId`; it cannot assert that the corresponding Version exists.

## 5. Conceptual pure interfaces

Phase 02 may refine the Rust shape, but it must preserve these capabilities and
must not add durable I/O:

```text
validate_complete(
    untrusted_facts,
    limits,
) -> Result<ValidatedPortableVersion, IdentityError>

write_canonical(
    validated_version,
    canonical_sink,
) -> Result<CanonicalSummary, IdentityError>

decode_and_validate_canonical(
    canonical_source,
    limits,
) -> Result<ValidatedCanonicalVersion, IdentityError>

compare_canonical(
    candidate_source,
    accepted_source,
    limits,
) -> Result<Equal | Unequal, IdentityError>
```

Required behavioral rules:

1. `validate_complete` rejects structural ambiguity before acceptance.
2. `write_canonical` emits deterministic bytes and derives a typed `VersionId`
   over exactly those bytes.
3. A Version need not be buffered as one allocation. Interfaces must permit
   streaming content and bounded metadata.
4. `compare_canonical` compares the complete canonical byte streams and cannot
   return equal merely because IDs, lengths, descriptors, or samples match.
5. Early return on the first unequal canonical byte is permitted, but the
   implementation must still validate enough input to fail safely and respect
   the selected corruption model.
6. The production digest implementation is not replaced by a weak test hash.
   Forced-ID behavior is injected only at the store/identity test seam.
7. Decode support is required only where the selected payload representation
   needs it for exact comparison or golden verification; Phase 02 must document
   whether comparison is encoder-to-encoder, encoder-to-canonical-record, or
   another bounded pure form.

## 6. Canonicalization properties

Phase 02 must select a grammar that demonstrates all of the following:

- unambiguous framing between fields and entries;
- explicit schema/domain versioning;
- stable integer, length, and enum encoding;
- stable path and string byte encoding;
- deterministic global or hierarchical entry ordering;
- an explicit duplicate canonical-path rejection rule;
- distinction among absent, empty, and zero-valued facts;
- complete inclusion of regular-file bytes;
- no locale, platform enumeration, host inode, or timestamp accident;
- no canonical alias between different accepted entry types or metadata;
- bounded parsing and encoding on adversarial input; and
- golden vectors that can be independently reproduced from the documented
  grammar.

Changing canonical bytes or Version meaning after release requires a new
identity domain/schema version and a one-way conversion through normal store
admission. Existing accepted payloads are never reinterpreted or modified in
place.

## 7. Equality, collision, and responsibility boundary

Identity and storage divide responsibility as follows:

| Step | Owner | Obligation |
|---|---|---|
| Validate portable candidate | Identity module | Reject malformed, unsupported, ambiguous, or over-limit facts. |
| Produce canonical bytes and candidate `VersionId` | Identity module | Deterministic complete encoding and typed digest. |
| Look up occupied ID | Store | Resolve the physical accepted payload slot under store authority. |
| Obtain accepted canonical bytes | Store | Provide immutable, integrity-checked canonical comparison input. |
| Compare complete canonical streams | Pure identity capability invoked by store | Return byte equality/inequality; no digest-only shortcut. |
| Classify mismatch | Store | Typed collision; no alias, binding, root, or head mutation. |
| Reuse equal occupant | Store | Return the one existing accepted binding; do not create a second payload. |
| Admit absent ID | Store | Durably admit one immutable payload before issuing a binding. |

Collision comparison can be linear in the canonical Version size and is a
mandatory correctness cost. Phase 02 may optimize streaming, buffering, and
early mismatch but may not replace full comparison with a probabilistic check,
secondary digest, length check, metadata sample, or “cryptographically
impossible” assumption.

## 8. Validation and resource contract

Phase 02 must select finite constants and test the boundary at limit minus one,
limit, and limit plus one where meaningful.

| Population/cost | Required Phase 02 decision |
|---|---|
| Total canonical/input bytes | Maximum and overflow-safe accounting rule |
| Entry count | Maximum represented entries |
| File content | Per-file and aggregate limits or a documented shared aggregate bound |
| Path | Maximum encoded length, component count, component length, and tree depth |
| Symbolic-link target | Maximum length if supported |
| Metadata | Maximum per-entry and aggregate metadata size/count |
| In-memory ordering workspace | Bounded strategy and upper bound |
| Streaming buffers | Fixed/finite buffer sizes and ownership |
| Decode nesting/work | Finite nesting and work accounting |
| Cancellation/deadline | Cooperative checkpoints where the current runtime contract permits them |

Arithmetic overflow, invalid lengths, truncated data, duplicate canonical
names, unsupported versions/types/metadata, and excess work all return typed
errors. They never truncate, normalize lossy data silently, partially identify
a Version, or panic on untrusted input.

## 9. Typed failure taxonomy

Exact Rust variants are `SELECT_IN_PHASE_02`, but callers must be able to
distinguish at least:

| Failure class | Meaning |
|---|---|
| Invalid fact | Malformed path, illegal tree relationship, invalid encoding, or inconsistent entry |
| Unsupported fact | Well-formed entry type or metadata outside the qualified portable profile |
| Duplicate/ambiguous name | Two inputs map to one canonical name or the path grammar is ambiguous |
| Limit exceeded | A named finite identity bound was exceeded |
| Unsupported identity version | Canonical domain/schema cannot be interpreted safely |
| Corrupt canonical data | Truncated, malformed, integrity-inconsistent, or impossible canonical input |
| Canonical I/O | A caller-provided bounded source/sink failed; this is not LayerStack-0 publication |

`DigestCollision` is a LayerStack-0 admission result, because only LayerStack-0
knows that an ID is occupied and can establish the accepted comparison source.
The identity module supplies byte inequality; LayerStack-0 classifies it as a
collision.

## 10. Phase 02 selections and deliverables

The following are intentionally not chosen by Phase 01:

| Exact choice | Status | Constraint |
|---|---|---|
| Accepted entry/metadata profile | `SELECT_IN_PHASE_02` | Complete for the qualified product Version; everything else explicitly rejected. |
| Canonical codec and grammar | `SELECT_IN_PHASE_02` | Deterministic, versioned, domain-separated, unambiguous, bounded. |
| Path normalization/ordering | `SELECT_IN_PHASE_02` | Portable, byte-defined, order-independent, ambiguity-rejecting. |
| Digest algorithm and width | `SELECT_IN_PHASE_02` | Typed, domain-separated derivation over the complete canonical stream. |
| Exact Rust types/signatures | `SELECT_IN_PHASE_02` | Preserve purity, streaming, full comparison, and binding separation. |
| Validation constants | `SELECT_IN_PHASE_02` | Finite, documented, and boundary-tested. |
| Canonical comparison representation | `SELECT_IN_PHASE_02` | Must permit full-byte equality without unbounded memory. |
| Golden vector format | `SELECT_IN_PHASE_02` | Stable and independently reproducible. |
| On-disk payload/root/head layout | `SELECT_IN_PHASE_03` | Not identity policy. |
| Store record checksums/versions | `SELECT_IN_PHASE_03` | Independent from identity domain/version. |
| `fsync`/rename/lock sequence | `SELECT_IN_PHASE_03` | Not selected here. |

Required Phase 02 outputs are:

- pure implementation under the existing LayerStack package;
- documented fact grammar, version/domain, digest, and limits;
- golden canonical-byte and `VersionId` vectors;
- corrupt, truncated, unsupported, duplicate, oversized, and deep-tree cases;
- order-independence checks;
- occupied-ID forced-collision support for Phase 03 tests;
- a forbidden-runtime-field/source audit; and
- a short store-caller contract matching this document.

## 11. Verification map

| Phase 02 check | Required evidence |
|---|---|
| I1 same facts → same bytes → same ID | Golden vectors and repeat runs |
| I2 enumeration order independence | Permuted equivalent fact inputs |
| I3 corrupt input rejected | Truncated, malformed, duplicate, and impossible inputs |
| I4 over-limit input rejected | Boundary tests for selected finite constants |
| I5 occupied ID + different bytes rejects | Forced-ID seam consumed by store-facing/unit tests; no alias |
| I6 no runtime brands | Type/source audit plus construction tests |
| I7 identity cannot assert durable acceptance | API/type proof that raw `VersionId` cannot construct `AcceptedVersion` or `AcceptedBinding` |

An encode/hash microbenchmark is optional sanity evidence. It cannot waive a
correctness check or become a V2 performance guarantee.

## 12. Open owner decisions and stable seams

`DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` remain open. None changes
canonical Version identity under its currently stated outcomes:

- blame/audit provenance remains an application-owned side channel;
- the observation window changes migration-code deletion timing only;
- sessionless mutation, if allowed, must construct a normal complete candidate;
- auth/revoke ordering determines whether the application may call the store,
  not what bytes identify a Version.

If any owner decision instead requires provenance, authorization, session,
runtime mount information, or mutable selected-Version history to enter canonical
identity, Phase 01 must be reopened.

## 13. Stop and reopening conditions

Stop Phase 02 and reopen Phase 01 if evidence shows any of the following:

- a complete qualified Version cannot be represented without layer history;
- stable identity requires a host path, mount, OverlayFS/OCI/Docker,
  namespace, process, lease, workspace, session, or policy fact;
- full occupied-ID canonical-byte comparison cannot be performed with bounded
  resources;
- the pure module must own durable I/O, OCC, runtime effects, or authorization;
- a new crate, service, process, registry, database, or facade is required for
  an identity invariant; or
- the identity contract forces a different payload/storage family or selected
  Version owner.

Do not reopen Phase 01 for ordinary choices of codec, digest, finite constants,
internal module names, or streaming implementation when they satisfy this
contract.

## References

- [Product PRD](../PRD.md)
- [Selected architecture](../architecture_design.md)
- [Phase 01 selection contract](../phases/01-choose-design/SPEC.md)
- [Phase 02 PRD](../phases/02-state-identity/PRD.md),
  [plan](../phases/02-state-identity/PLAN.md), and
  [tests](../phases/02-state-identity/test-perf.md)
- [R0 algorithms and call flows](04-algorithms-and-call-flows.md)
- [LayerStack-0 storage](03-state-store.md)
