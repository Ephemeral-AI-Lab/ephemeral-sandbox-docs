# Portable Root Contract v2 — owner decision D2.5

Status: **approved**

Decision ID: `PRC-STAGE02-OWNER-DECISION-D2.5`

Owner response: `approved`

Approval recorded: `2026-07-25T00:02:23+0800`

This record closes the Stage 02 custody, preparation, numeric wire-assignment,
and port-signature gaps identified by
[`implementation_instructions.md`](implementation_instructions.md). It is the
versioned contract record referenced by the authoritative Stage 02
specification. Where the earlier required-shape pseudocode is less specific or
uses a different illustrative spelling, this approved record controls.

Approval freezes a POC/source contract. It does not activate a v2 root, change
publication authority, authorize durable v2 state, or qualify Stage 11 release
behavior.

## 1. Custody and authority reconciliation

Implementation is authorized directly on the preserved dirty worktrees
recorded in the Stage 01 handoff and Stage 02 entry capture. The recorded
product, test, and documentation branches and immutable HEADs remain the
implementation bases. Inherited tracked and untracked Stage 00/01 work must be
merged around and preserved.

The approval does not authorize a commit, push, stash, reset, branch switch,
clean, discard, or replacement of a dirty file from `HEAD`.

Legacy LayerStack v1 remains the sole runtime read, write, revision, and
publication authority. `Manifest::root_hash` remains the sole public/runtime
revision identity. Stage 01 workspace execution transcripts are provider-local
scratch and never participate in portable identity. Stage 02 writes no v2
durable byte.

## 2. Ownership and dependency direction

The dependency direction is:

```text
workspace/provider adapters -> layerstack -> layerstack-core
```

`sandbox-runtime-layerstack-core` owns only:

- safe, standard-library-only portable values;
- constructor-enforced validation;
- canonical payload encoding and bounded exact decoding;
- logical entry, tree, and root records;
- `PendingTree` to `ValidatedTree` validation state; and
- the single canonical sink, canonical source, and typed-digest ports below.

LayerStack owns:

- capture preparation and backend-marker filtering;
- external run generation, coalescing, and bounded fan-in ordering;
- SHA-256;
- serde diagnostic envelopes;
- filesystem and persistence concerns; and
- every current or future runtime-authority decision.

The core has no dependency, dev-dependency, build-dependency, target
dependency, build script, `links` value, proc macro, FFI, or unsafe code. It
does not import or own SHA, serde, filesystem persistence, fsync, providers,
Docker, OverlayFS, mounts, namespaces, runtime operations, telemetry, E2E or
benchmark support, async runtimes, services, or helpers.

## 3. Closed public port signatures

These are the only variation-point ports:

```rust
pub trait CanonicalSink {
    fn write_all(&mut self, bytes: &[u8]) -> Result<(), Error>;
}

pub trait CanonicalSource {
    fn read_exact(&mut self, bytes: &mut [u8]) -> Result<(), Error>;
    fn ensure_exhausted(&mut self) -> Result<(), Error>;
}

pub enum DigestDomain {
    RootRecord,
    TreeManifest,
    Object(ObjectKind),
}

pub trait TypedDigest {
    fn digest(
        &mut self,
        domain: DigestDomain,
        version: FormatVersion,
        payload_len: u64,
        encode_payload: &mut dyn FnMut(
            &mut dyn CanonicalSink,
        ) -> Result<(), Error>,
    ) -> Result<Digest32, Error>;
}
```

The digest implementation emits the one canonical preimage header, invokes
`encode_payload` exactly once, and requires the callback to emit exactly
`payload_len` bytes. A short, long, repeated, or failed callback yields no ID.
The core does not buffer a complete digest preimage.

`Error` is a closed, allocation-free value containing only an error kind,
format version, field class, and bounded ordinal. It never retains arbitrary
path, xattr, payload, or host error text.

## 4. Nominal values and numeric assignments

| Value | Approved representation or assignment |
| --- | --- |
| `FormatVersion` | nominal `u16`; v2 is numeric `2` |
| `Digest32` | exactly 32 bytes |
| `RootId` | nominal wrapper around `Digest32` |
| `TreeManifestId` | distinct nominal wrapper around `Digest32` |
| `ObjectId` | `ObjectKind` plus `Digest32` |
| `PublicationId` | exactly 16 bytes; all-zero is invalid |
| `PublicationIdentity` | `generation: u64` plus `PublicationId` |
| `HardlinkGroupId` | nonzero `u128`, encoded big-endian; canonical one-based equivalence-class rank |
| `ChunkProfileId` | nominal `u16`; `SeqCdcV1 = 1` is the only accepted Stage 02 value |

Object-kind values are frozen:

| Object kind | Value |
| --- | ---: |
| `FileSegments` | `2` |
| `ChunkPayload` | `3` |
| `Transition` | `4` |

Entry-kind values are frozen:

| Entry kind | Value |
| --- | ---: |
| `Directory` | `1` |
| `Regular` | `2` |
| `Symlink` | `3` |
| `Device` | `4` |
| `Fifo` | `5` |

Capability bits are frozen:

| Required capability | Bit |
| --- | ---: |
| xattrs | `0` |
| sparse holes | `1` |
| hardlinks | `2` |
| symlinks | `3` |
| devices | `4` |
| FIFO | `5` |

Bits 6 through 63 are unknown required bits and reject. The encoded capability
set is the exact minimal union implied by the complete tree. Unknown required
capabilities are never preserved as optional data or silently degraded.

## 5. Canonical path and metadata rules

`CanonicalPath` is a non-empty relative Linux path represented by raw bytes:

- total length is 1 through 4,096 bytes;
- every component is 1 through 255 bytes;
- `/` is the only separator;
- leading `/`, trailing `/`, empty components, NUL, `.`, and `..` reject;
- invalid UTF-8 is valid when the byte rules pass; and
- `\` is ordinary data and remains unchanged.

Portable metadata uses exact-width values:

- `mode: u32` contains only `0o7777`; file-type bits and every higher bit
  reject;
- `uid` and `gid` are unrestricted `u32` values;
- `mtime_seconds` is `i64`;
- `mtime_nanoseconds` is `u32` in `0..1_000_000_000`;
- xattr keys are non-empty raw byte strings of at most 255 bytes, contain no
  NUL, and are strictly increasing by unsigned byte order;
- duplicate or unsorted xattr keys reject; and
- xattr values are raw bytes bounded by the complete metadata-record limit.

Symlink targets are raw bytes of at most 4,096 bytes and contain no NUL.
Sparse extents are `(offset: u64, length: u64)` pairs with nonzero length,
checked `offset + length`, increasing non-overlapping order, and an end no
greater than the regular file's logical length.

A regular entry references exactly an `ObjectKind::FileSegments` object.
Hardlink groups use contiguous one-based ranks, contain at least two entries,
and require equal portable metadata, logical length, sparse layout, and
segment reference within the group.

LayerStack filters Linux whiteout and opaque-directory carrier markers before
the portable boundary. A surviving device `(0, 0)` rejects. The core remains
backend-neutral and does not encode Docker or OverlayFS marker names.

## 6. Canonical framing

Every record begins with the eight bytes `EOS-LS2\0`, followed by one record
kind byte and the two-byte big-endian format version.

| Record | Kind | Payload-length width | Header bytes |
| --- | ---: | ---: | ---: |
| `FileSegments` object | `0x02` | `u32` big-endian | 15 |
| `ChunkPayload` object | `0x03` | `u32` big-endian | 15 |
| `Transition` object | `0x04` | `u32` big-endian | 15 |
| root | `0x10` | `u32` big-endian | 15 |
| tree | `0x11` | `u64` big-endian | 19 |
| entry | `0x12` | `u32` big-endian | 15 |
| metadata | `0x13` | `u32` big-endian | 15 |
| object reference | `0x14` | `u32` big-endian | 15 |

Fields are TLVs in strictly increasing fixed schema order:

```text
tag: u8 | value_length: u32be | value bytes
```

An option TLV value is one discriminant byte: `0` for `None`, or `1` followed
by the canonical inner bytes for `Some`. No other discriminant is valid.

Xattrs encode:

```text
count: u32be |
repeat count times {
  key_length: u32be | key |
  value_length: u32be | value
}
```

Sparse holes encode:

```text
count: u32be |
repeat count times { offset: u64be | length: u64be }
```

Decoding consumes exactly the declared record. Short input, extra suffix
bytes, unread declared bytes, unknown kinds, unknown versions, inconsistent
lengths, overflow, or noncanonical field values reject without repair.

## 7. Field tables

Root payload TLVs are:

| Tag | Value |
| ---: | --- |
| `1` | required-capability bits, `u64be` |
| `2` | chunk-profile ID, `u16be` |
| `3` | tree-manifest digest, 32 bytes |
| `4` | optional parent root digest |
| `5` | optional base root digest |
| `6` | publication generation, `u64be` |
| `7` | publication ID, 16 bytes |

Tree payload is:

```text
entry_count: u64be |
entries_bytes: u64be |
exactly entry_count complete Entry records occupying entries_bytes
```

Entry payload TLVs are:

| Tag | Value |
| ---: | --- |
| `1` | entry kind, one byte |
| `2` | canonical raw path bytes |
| `3` | complete metadata record |
| `4` | optional symlink target |
| `5` | optional device major, `u32be` |
| `6` | optional device minor, `u32be` |
| `7` | optional logical length, `u64be` |
| `8` | optional sparse-hole sequence |
| `9` | optional hardlink-group rank, `u128be` |
| `10` | optional complete object-reference record |

The entry kind determines exactly which option fields must be present. A
missing required option or a present inapplicable option rejects.

Metadata payload TLVs are:

| Tag | Value |
| ---: | --- |
| `1` | mode, `u32be` |
| `2` | uid, `u32be` |
| `3` | gid, `u32be` |
| `4` | mtime seconds, `i64be` |
| `5` | mtime nanoseconds, `u32be` |
| `6` | canonical xattr sequence |

Object-reference payload TLVs are:

| Tag | Value |
| ---: | --- |
| `1` | object kind, one byte |
| `2` | object digest, 32 bytes |

## 8. Bounds and preparation

`MAX_RECORD_BYTES` is 262,144. Bounded Stage 02 tiny helpers accept at most
256 entries/identities and a complete tree record of at most 262,144 bytes.
These are POC/test bounds, not a production whole-tree collector.

Serialized per-entry metadata plus regular-entry sparse/hardlink data is at
most 65,536 bytes. The fixed regular baseline is 88 bytes. The approved
maximum empty-key-free dense single-xattr value is 65,439 bytes, and the
maximum sparse-hole count under the same bound is 4,090.

Before decoding entries, a tree checks:

```text
entry_count * 147 <= entries_bytes
```

using checked arithmetic. Decoders do not reserve from an attacker-controlled
count before the corresponding byte lower bound is proved.

The core receives entries already in strict canonical path order and rejects
duplicates or unsorted input. LayerStack owns bounded preparation from
arbitrary insertion order: run generation/coalescing, whiteout filtering,
disk-backed sorting/spooling, and an eight-way bounded merge. The core neither
imports the filesystem nor retains the complete tree.

Tree validation is two-phase:

```rust
stage_tree_candidate(
    tree_source,
    hardlink_claim_sink,
    reference_claim_sink,
    digest,
) -> Result<PendingTree, Error>

validate_tree_candidate(
    pending,
    sorted_hardlink_claim_source,
    sorted_reference_claim_source,
    sorted_known_file_segments_source,
) -> Result<ValidatedTree, Error>
```

The concrete arguments use the approved canonical source/sink/digest trait
objects. `PendingTree` internals are private. Only `ValidatedTree` can produce
a `RootRecordV2`.

## 9. Identity preimages

Root, tree, and object IDs are SHA-256 of their complete canonical framed
bytes. The record kind and version make each preimage typed and domain
separated.

The LayerStack adapter, not the core, owns SHA-256 and emits the single header
selected by `DigestDomain`. The core callback emits only the payload and must
be invoked exactly once for exactly the declared byte count.

For the future Stage 03 two-slice chunk seam, the frozen `ChunkPayload`
preimage is:

```text
EOS-LS2\0 |
0x03 |
0x0002 |
payload_len: u32be |
first slice |
second slice
```

The two slices are written directly to the sink. Stage 02 does not implement
SeqCDC or chunk persistence.

## 10. Diagnostic JSON and immutable fixtures

JSON is diagnostic only. LayerStack uses compact `serde_json` with fixed
struct field order, denies unknown fields, and accepts a diagnostic record
only when parse followed by re-encode is byte-identical to the input.
Root-record and tree-manifest schemas remain distinct.

`contract-v2.bin` contains exactly one complete canonical Tree record followed
by one complete canonical Root record. `contract-v2.json` is the ordered
inventory for schema/version, provenance, canonical logical input, binary
length/digest, expected typed identities, and required rejection vectors.
Accepted v2 fixtures are immutable; a semantic change requires a new
format/profile and a new fixture.

The mandatory core tiny-loop command remains std-only. The benchmark's
one-process candidate probe is an ignored test in the already-built
LayerStack golden-test executable so it can exercise the real existing
LayerStack SHA-256 adapter without a forbidden reverse dependency or a new
runtime/public binary. The core oracle and LayerStack golden must agree on
the same exact canonical bytes and typed IDs.

## 11. Dormant-runtime evidence

No daemon metric is added for Stage 02. PRC-01 derives its test-local
publication-authority projection only when the existing configured,
read-authority, and write-authority fields all report legacy v1 and the
observed public publication has exact v1 `Manifest::root_hash` semantics.

Candidate root count, object count, and durable bytes are explicit numeric
zeros only after a complete outside `lstat` observation proves every forbidden
path absent at every required boundary. Missing, errored, duplicate, or
disagreeing observations fail; absence is never inferred.

This decision introduces no runtime call from LayerStack to the portable
module and no `/eos` path. Stage 11 host, release, performance, memory, space,
soak, migration, and production qualification remain deferred.
