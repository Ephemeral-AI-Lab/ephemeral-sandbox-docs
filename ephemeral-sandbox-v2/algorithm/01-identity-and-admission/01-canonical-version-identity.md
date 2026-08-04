# 01.01 — Canonical Version identity

## 1. Purpose and owning phase

**Owner:** Phase 02 — Version identity.  
**Purpose:** Convert a bounded set of complete portable filesystem facts into
deterministic canonical bytes and a typed `VersionId`, while preserving the rule
that the result identifies only a Candidate.

This algorithm is pure with respect to LayerStack-0 durable storage. It does not
look up occupancy, accept a Version, issue an AcceptedBinding, create a Head or
Root, mount a filesystem, or infer existence from a digest.

Authority flows as defined by the package [README](../README.md):

```text
Candidate
  -> VersionId
  -> AcceptedVersion
  -> AcceptedBinding
  -> Head + HeadRevision or typed Root
```

This file defines only the first arrow. [Admission](02-complete-version-admission.md)
owns the remaining durable authority.

## 2. Evidence status

- `SOURCE-VERIFIED`: Phase 00 shows that portable identity must be separated
  from the current runtime-private layer, mount, and host machinery, and that
  the selected package boundary is source-placeable.
- `SPIKE-VERIFIED`: none; no identity spike or V2 executable proof has run.
- `INFERRED`: the validation, canonicalization, typed-ID, and exact-comparison
  contracts below follow from the product hard rules and selected R0 design.
- `OPEN`: Phase 02 must choose the exact fact profile, codec, ordering grammar,
  domain/schema separation, digest algorithm and width, limits, streaming
  representation, and golden vectors. These are `OPEN_WITHIN_R0`.

## 3. Contract

Names below are conceptual responsibility/type flows, not selected Rust
signatures or serialized spellings.

### Inputs

- `PortableFactSource`: a finite producer of complete filesystem facts for one
  Candidate, including qualified entry kind, portable relative path, portable
  metadata, link target where allowed, and file content.
- `ValidationBudget`: finite maxima selected by Phase 02 for aggregate bytes,
  entry count, path bytes and depth, individual and aggregate content,
  metadata/link populations, scratch, and elapsed/cancellation checkpoints.
- `SchemaContext`: the Phase 02-selected canonical format version and domain.
- Optional test-only forced-ID seam, unavailable in production authority paths.

The producer must present logical facts, not a path to be followed by the
identity algorithm. Capture from a Workspace or import source is a separate
owner's bounded operation.

### Preconditions

1. The caller has authority to read the source facts.
2. The source represents a complete Candidate, not a delta or parent-dependent
   reconstruction.
3. The budget is finite and no larger than the owning process/store admission
   budget.
4. The schema context is supported and unambiguous.

### Outputs

On success, `CanonicalCandidate` contains:

- the validated portable fact stream or bounded replay handle;
- the complete deterministic canonical-byte stream or bounded retained
  comparison source;
- a typed `VersionId` derived from all canonical bytes under explicit
  domain/schema separation; and
- bounded accounting totals needed by admission.

Neither this value nor its `VersionId` proves durable existence, equality with
an occupant, acceptance, reference authority, or selection.

### Typed outcomes

| Outcome | Meaning |
|---|---|
| `CanonicalCandidateReady` | All facts validated, canonical bytes completed, typed Candidate ID computed, and exact-comparison material is available. |
| `InvalidPortableFact` | A fact, path, metadata value, link, duplicate, conflict, or completeness rule is invalid. |
| `UnsupportedPortableFact` | The fact is well-formed but outside the selected portable profile. |
| `LimitExceeded` | A finite byte, entry, path, depth, metadata, scratch, or time budget would be exceeded. |
| `SourceChangedOrIncomplete` | The producer cannot prove one stable complete fact set. |
| `CanonicalizationFailed` | Canonical production or its bounded replay material failed without yielding an ID. |
| `Cancelled` | Cancellation was observed before successful completion. |

All non-success outcomes confer no durable authority and leave no partial
`VersionId` usable for admission.

## 4. Portable-fact boundary

The canonical domain may include only Phase 02-qualified facts necessary to
represent one complete portable filesystem value. At minimum, validation must
distinguish entry kinds, relative path components, portable metadata, link
targets where supported, file length, and every content byte. Phase 02 decides
the exact accepted subset.

The identity domain must exclude:

- Docker/OCI identifiers or archive representation details;
- OverlayFS lower/upper/work paths, whiteout encoding artifacts, mount IDs,
  namespaces, or mount options;
- host absolute paths, device/inode identities, filesystem allocation facts,
  reflink/snapshot facts, or host timestamps not explicitly selected as
  portable content semantics;
- process, PID, session, lease, worker, custody, authorization, or request
  facts;
- legacy layer IDs, parent/depth links, squash history, and merge history; and
- Head selectors, `HeadRevision`, Root IDs, scores, MCTS/rollout policy, or
  application orchestration.

If product semantics require an excluded runtime-private fact to determine
Version equality, this file cannot silently add it; that is a
`REOPEN_PHASE_01` condition.

## 5. Validation and canonicalization algorithm

The pseudocode deliberately leaves byte grammar, digest, and numeric constants
to Phase 02.

```text
canonicalize_candidate(source, budget, schema):
    require supported(schema)
    accounting := new_bounded_accounting(budget)
    ordered := new_bounded_canonical_orderer(budget)

    for fact in source:
        cancellation_checkpoint_or_return(Cancelled)
        accounting.charge_fact_before_allocation(fact)

        path := validate_portable_relative_path(fact.path, budget)
        reject absolute, empty-component, dot, dot-dot, prefix,
               separator-confusion, NUL, encoding ambiguity,
               duplicate, ancestor-kind conflict, or over-depth path

        portable := validate_and_normalize_selected_fact(fact, schema)
        reject runtime-private or unsupported fields
        charge content, metadata, link, path, and scratch bounds incrementally
        ordered.insert(path, portable) or return LimitExceeded

    require source reports one complete stable end
    require directory/child, entry-kind, duplicate, and completeness invariants

    encoder := begin_domain_and_schema_separated_stream(schema)
    comparator_source := begin_bounded_replay_or_retention(budget)
    id_state := begin_selected_typed_digest(schema)

    prefix := encoder.emit_domain_and_schema_prefix()
    charge emitted-byte and scratch bounds before growth
    write_exact(prefix, comparator_source)
    update(id_state, prefix)

    for portable in ordered.deterministic_order():
        bytes := encoder.emit_unambiguous_entry(portable)
        charge emitted-byte and scratch bounds before growth
        write_exact(bytes, comparator_source)
        update(id_state, bytes)

    suffix := encoder.finish_complete_stream()
    charge emitted-byte and scratch bounds before growth
    write_exact(suffix, comparator_source)
    update(id_state, suffix)

    require encoder reports one complete stream
    require comparator_source seals the exact prefix + entries + suffix bytes
    version_id := finish_typed_version_id(id_state, schema)

    return CanonicalCandidateReady(
        version_id,
        comparator_source,
        ordered.sealed_replayable_portable_facts,
        accounting.totals)
```

Canonical encodings must be unambiguous: entry and field boundaries, kinds,
lengths, ordering, absence/presence, and schema/domain must not rely on host
language, locale, traversal order, or filesystem enumeration order. Domain and
schema separation must prevent bytes from another format or product domain from
being interpreted as the same typed `VersionId` input.

### Full canonical-byte equality

```text
canonical_bytes_equal(left, right, budget):
    open bounded canonical replay streams
    while both streams have bytes:
        cancellation_checkpoint_or_fail_closed()
        read bounded blocks from both
        if block bytes differ: return NotEqual
    if one stream has remaining bytes: return NotEqual
    if both end exactly and integrity checks pass: return Equal
    return ComparisonFailed
```

Digest equality, canonical length equality, entry-count equality, payload-tree
shape, or a prefix match is insufficient. Only complete byte-for-byte equality
through simultaneous exact end-of-stream yields `Equal`.

## 6. Visibility and linearization

This pure algorithm has **no durable visibility point and no Head
linearization point**. Its local completion point is the return of a sealed
`CanonicalCandidateReady` after the complete stream and typed ID have finished.
Any partial ID state before that point is private scratch and unusable.

The exact occupancy/equality decision occurs later inside LayerStack-0
[admission](02-complete-version-admission.md), not here.

## 7. Behavior by execution condition

| Condition | Required behavior |
|---|---|
| Normal | Validate every fact, emit deterministic complete bytes, finish a typed Candidate ID, and retain/replay exact comparison material. |
| Concurrent | Independent canonicalizations have no shared authority. Equal qualified facts must yield identical canonical bytes and typed IDs regardless of input enumeration order. |
| Retry | Repeating over the same stable facts and schema yields exactly the same bytes and ID. Retry never upgrades a prior partial result. |
| Cancellation | Check before costly reads/allocations and between bounded units. Destroy or release private scratch; return no usable partial identity. |
| Crash | Only caller-owned ephemeral scratch may remain. No durable Version, binding, Head, or Root exists because this algorithm owns none. Caller or startup cleanup removes recognizable private scratch within its bound. |
| Cleanup | Close replay sources/descriptors and remove spill scratch on failure or after admission no longer needs them. Cleanup failure becomes bounded debt owned by the caller/admission path. |

A changing source must be rejected or captured by an owner that can provide one
stable complete capture. Retrying against silently changed facts is a new
Candidate, not continuation of the old one.

## 8. Finite resource accounting and complexity

Let:

- `E` = number of portable entries;
- `B` = total canonical bytes, including content;
- `P` = total portable path bytes;
- `D` = maximum portable path depth;
- `S_id` = Phase 02-bounded ordering/replay scratch; and
- `W_id` = bounded canonicalization worker count (normally one logical stream).

All are checked before or during consumption; there is no unbounded input
collection.

| Operation | Worst-case time | Data I/O | Space/resource bound |
|---|---:|---:|---:|
| Validation and canonicalization | `O(B + P + E log E)` with comparison sorting; a Phase 02-selected already-ordered or bounded external orderer may change the sort term, not the byte term | Reads `O(B + P)` source facts; emits or retains `O(B)` canonical bytes | `O(S_id)` scratch, finite memory, finite descriptors, `W_id` workers |
| Typed ID derivation | `O(B)` | Consumes every canonical byte | Digest state `O(1)` for the selected fixed algorithm plus bounded buffers |
| Full equality | `O(B)` worst case | Reads both complete canonical streams: up to `2B` for equal-size equal candidates | `O(1)` fixed-size compare buffers plus bounded replay handles |

If ordering, replay, or comparison cannot stay within configured memory,
scratch, descriptor, worker, or time limits, the algorithm returns
`LimitExceeded` or `ComparisonFailed`; it must not weaken equality or omit
facts. Staging/canonical scratch space is reserved before use and charged to the
Candidate admission budget described in
[resources, complexity, and observability](../06-resources-performance-and-evidence/01-resources-complexity-and-observability.md).

## 9. Security and path validation

All input is untrusted until validation completes.

- Accept only the selected portable relative-path grammar; reject traversal,
  absolute/prefixed paths, ambiguous separators or encodings, NUL, empty or
  special components, duplicate normalized names, and ancestor conflicts.
- Validate lengths and counts before allocation, concatenation, sorting, or
  content read. Charge decompressed/logical bytes, not just wire bytes.
- Treat link targets as data under a selected portable policy. Do not follow a
  symlink, hard link, mount, device, FIFO, or special node through a host path
  during pure canonicalization.
- Reject unsupported special entries and metadata; do not silently discard a
  field that affects portable semantics.
- Keep error messages bounded and avoid reflecting arbitrary content or host
  paths into logs.
- Keep the forced-ID seam test-only and incapable of issuing an
  AcceptedBinding outside explicit collision tests.

## 10. Observability and test seams

Diagnostic facts may include validation outcome, schema/domain version,
bounded totals, elapsed stages, rejection class, cancellation, and whether
full comparison reached exact end-of-stream. They must not include secret file
contents and cannot authorize admission.

Required Phase 02 tests include:

- golden vectors with independently checked canonical bytes and typed IDs;
- input-order permutation stability;
- path/metadata/content boundary and ambiguity cases;
- runtime-private-field rejection;
- corrupt, incomplete, over-limit, cancellation, and changing-source cases;
- full-byte equality with a difference at the first, middle, and final byte;
- equal digest/length through a forced-ID seam but unequal canonical bytes; and
- proof that a computed ID cannot be passed where an AcceptedBinding is
  required.

Metric and event spellings remain Phase 02/03 choices; new names must use the
Version vocabulary.

## 11. Details Phase 02 may still select

Phase 02 may select exact facts, canonical codec bytes, ordering grammar,
schema/domain tag, digest, typed encoding, finite numeric limits, replay/spill
mechanism, errors, and golden vectors. It may select an efficient streaming
implementation provided complete determinism and exact comparison remain
provable.

It may not select a raw digest as accepted authority, a host/runtime field as
identity, a layer/delta representation as complete truth, or a comparison that
stops at digest or length equality.

## 12. `REOPEN_PHASE_01` conditions

Reopen Phase 01 with the exact failed requirement if Phase 02 proves that:

- a complete Version cannot be represented by bounded deterministic portable
  facts;
- correct equality requires host, mount, namespace, OverlayFS, process,
  session, lease, legacy layer, or other runtime-private identity;
- full canonical-byte comparison cannot be implemented with finite fail-closed
  resources;
- a computed ID must become existence, admission, or reference authority for a
  required product behavior; or
- the product needs a second independent complete-value identity or a
  non-content-derived Version identity.

Codec, digest, ordering, limit, and scratch choices that satisfy this contract
remain `OPEN_WITHIN_R0` and do not reopen the architecture.
