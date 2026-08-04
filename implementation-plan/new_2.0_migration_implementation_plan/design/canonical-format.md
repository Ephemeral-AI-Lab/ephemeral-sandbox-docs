---
status: proposed-behavior
authority: canonical-fact-and-identity-laws
depends-on:
  - REQ-COR-001
  - REQ-COR-002
  - REQ-COR-003
  - REQ-PORT-001
---

# Canonical fact and identity laws

## Behavior, not an architectural module

V2 requires pure deterministic behavior for portable filesystem facts,
canonical bytes, `StateId`, bounded decoding, validation, and test vectors. It
does **not** require a named canonical module, package, component, service,
deployable, trait, port, facade, or independent authority.

The clean pinned e497 tree has no `sandbox-runtime-layerstack-core` package.
R0 first tries the minimum pure functions in lawful extant source or inline in
their caller. The generated `R_PLACEMENT[o,q]` family tries every compatible
actual-source and fused destination `q`; a new pure-code boundary is eligible
only after its sealed deletion/necessity falsifier. Historical experiment
references to a core package are incomparable, non-current evidence and do not
construct a candidate. Pure computation writes no durable truth and owns no
admission or runtime effect.

The organization decision is independent of these required laws.

## Scope

In scope:

- a distinct candidate/accepted `StateId` type and version/domain-separated identity law;
- the closed product-visible filesystem fact vocabulary, including complete
  root facts;
- one byte-exact deterministic grammar after physical-method selection;
- canonical ordering, uniqueness, normalization, and finite limits;
- bounded streaming encode/decode and fail-closed validation; and
- golden, corrupt, oversized, cross-implementation, and migration vectors.

Out of scope:

- heads, revisions, selectors, persistent records, locators, packs, indexes,
  sessions, outcomes, custody, admission, GC, recovery, backup, or replay;
- source enumeration/fencing/capture, destination realization/activation,
  command/file effects, and disposal; and
- native paths, mounts, namespaces, devices, snapshots, runtime/provider
  brands, wall clocks, deployment values, WASI/VM handles, OCI values, and
  selected physical locators.

Object kinds, edges, trees, manifests, chunkers, digests, and containers exist
only if the coupled physical candidate selects them. No wrapper or object graph
is presumed.

## Complete root identity

```text
state_identity(format_version, complete_canonical_root_facts) -> CandidateStateId
```

- **FMT-ID-001.** Complete root facts include the root node and every accepted
  product-visible root fact, including root metadata. Attribution participates
  only if `DEC-001` retains it.
- **FMT-ID-002.** Equal qualified facts produce identical canonical bytes and
  the same candidate `StateId`; source order, batching, allocation, runtime,
  capture, and physical placement do not. For accepted/published states, the
  same ID implies identical complete canonical bytes/facts because admission
  checks the bytes, not because a finite digest is assumed injective.
- **FMT-ID-003.** Legacy and V2 IDs are not interchangeable. Migration records
  deterministic old-to-new mapping and required provenance.
- **FMT-ID-004.** The domain-separated digest is a candidate commitment and
  lookup key, not a sufficient equality witness. If objects exist, their kinds
  are also bound.
- **FMT-ID-005.** If a candidate digest is already bound, admission compares the
  complete canonical bytes with bounded streaming equality. Equal bytes reuse
  the accepted binding; unequal bytes return
  `T03_REJECTION / STATE_ID_COLLISION` before any published identity, alias,
  mapping, head, root, index, closure, revision, custody, or capacity effect.
  Recovery/import fail readiness closed on unequal durable candidates and never
  choose one arbitrarily.

Whether root facts occupy a distinct object or another closed representation is
open. No digest primitive, root wrapper, manifest, or tree shape is accepted by
this file.

## Canonicality and safety

- **FMT-CAN-001.** One semantic fact set has exactly one accepted byte sequence.
- **FMT-CAN-002.** Source enumeration, batching, resume boundaries, allocation,
  and qualified runtime do not change bytes.
- **FMT-CAN-003.** Duplicate keys, ambiguous/nonminimal encodings, invalid
  order/type/edge, prohibited cycles, over-limit values, and trailing bytes fail
  closed.
- **FMT-CAN-004.** Decoders validate every field, record, collection, nesting,
  depth, and total-byte limit before allocation.
- **FMT-CAN-005.** If canonical bytes contain child edges, those authenticated
  bytes are the sole identity source; no duplicate durable edge truth exists.
  Edge-free candidates remain eligible.
- **FMT-CAN-006.** Attribution exists only if `DEC-001` retains exact
  `file_blame`; deletion adds no actor/history substitute.
- **FMT-CAN-007.** Repeated same-line or same-unit edits have a finite decode
  bound independent of prior-version depth.

## Portability

- **FMT-PORT-001.** Facts describe observable filesystem semantics, never a
  capture, storage, or realization mechanism.
- **FMT-PORT-002.** A source that cannot produce every required fact rejects
  before publication and never fabricates a default.
- **FMT-PORT-003.** A destination rejects statically knowable unsupported facts
  before allocation. Data-dependent incompatibility may fail only in bounded
  hidden realization followed by synchronized cleanup before activation.
- **FMT-PORT-004.** Independent implementations encoding equal facts produce
  identical bytes and the same candidate `StateId`, plus identical object IDs only when the
  selected representation defines objects.

OCI is an edge format. WASI and Firecracker are runtime-private conformance
subjects; they do not enter canonical values or justify a plugin architecture.

## Resource law

Encoding, decoding, and occupied-ID exact comparison use bounded streams and bounded caller-provided scratch
charged before allocation. They require no repository-sized set, full-tree
buffer, unbounded recursion, resident/global index, per-session cache,
background worker, hidden allocation, or unbounded queue. Exact field, record,
nesting, scratch, and byte caps become versioned constants only when a complete
physical candidate wins.

Temporary collision candidates remain under existing admitted temporary custody
until synchronous deletion or bounded cleanup/quarantine convergence. Durable
request replay terminalizes and replays the exact rejection; it never retries as
a new publication attempt or discloses incumbent bytes.

Any optimization cache is optional, bounded, reconstructible, non-authoritative,
charged, and automatically cleared at its finite idle/expiry/error/restart
boundary.

## Open coupled decisions

- canonical directory/root representation and any object/edge topology;
- content grouping and the repeated-edit bound;
- attribution or its approved product deletion;
- canonical/physical representation interaction;
- digest and domain-separation grammar; and
- collision-witness comparison cost and the qualification-only forced-collision
  seam, which must be absent from production builds and request configuration;
- exact stream/scratch limits and migration vectors.

No writable V2 state is accepted until these form one closed, independently
vectored winner. The winner must not manufacture another authority or require a
new organizational boundary without its own deletion counterexample.
