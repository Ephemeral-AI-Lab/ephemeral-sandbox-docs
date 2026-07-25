# Portable Root Contract v3 — owner decision G01.1

Status: **approved**

Decision ID: `PRC-STAGE03-OWNER-DECISION-G01.1`

Owner response: `proceed with my approval and you must not stop and auto approve if
the blocker does not drift from stage 3 spec`

Approval recorded: `2026-07-25T05:58:21+0800`

Approval scope: the owner authorized the implementation agent to close the missing
numeric and wire-level choices only when they do not drift from the Stage 03
specification. This record makes those choices explicit. It does not relax, replace,
or defer a Stage 03 requirement.

This decision is the required Stage 03 amendment. It is additive to
`PRC-STAGE02-OWNER-DECISION-D2.5`; it does not alter any v2 byte, tag, ID, golden,
decoder, or diagnostic record.

## 1. Non-drift and authority decision

The approved v3 slice has these fixed authority boundaries:

1. `LegacyV1` remains the only public read, write, revision, and publication
   authority.
2. v3 is private, additive, and invoked only through the normal Stage 03 publication
   protocol or its bounded hidden-validation use.
3. v3 content identity excludes publication ID, branch, generation, parent, base,
   actor, attribution, timestamp of publication, backend, carrier, locator, and
   materialization.
4. attribution has a distinct Merkle identity associated with a content `RootId`.
5. the scalar SeqCDC profile is exactly Preparation 03:
   `min=8192`, `target=16384`, `max=32768`, `threshold=5`, `trigger=50`,
   `jump=512`, and a `32768`-byte ring/window.
6. no external dependency, helper executable, service, sidecar, target-image
   utility, network lookup, unsafe code, or materialization dependency is authorized.
7. packs, locator runs, pack leases, materializations, GC, squash, authority
   migration, public cutover, and retirement remain owned by later stages. Stage 03
   may create only the conditional loose locator and source-protection lease defined
   here for an existing v1 carrier.

## 2. Common canonical encoding and identity

All v3 integers are explicit-width big-endian. All lengths are byte lengths. Checked
arithmetic precedes allocation.

Every v3 record uses:

```text
"EOS-LS2\0"                     8 bytes
record_kind                     u8
format_version                  u16be = 3
payload_length                  u32be
payload                         exactly payload_length bytes
```

Except for the raw `Chunk` payload, record payload fields are TLVs:

```text
tag:u8 | value_length:u32be | value
```

Tags appear exactly once in strictly increasing numeric order. No unknown tag,
missing tag, duplicate tag, reordered tag, unread declared byte, or suffix byte is
accepted. An option value is `0x00` for `None` or `0x01 | canonical inner bytes` for
`Some`; other discriminants reject.

The magic remains `EOS-LS2\0` so the existing dispatcher can inspect kind and version
without a second magic family. Version `3`, not the magic spelling, distinguishes
the format. A v2 decoder still accepts only version `2`.

Immutable typed IDs are SHA-256 of the complete canonical framed record. The
`record_kind` and `format_version` bytes are the exact type/domain separation; no
second implicit prefix is added. Each digest is wrapped in a distinct nominal type
and cannot be substituted for another type without `WrongDomain`.

Mutable records are not content identities. Their last field is tag `255` containing:

```text
SHA-256(
  "EOS-LS3-MUTABLE\0" |
  record_kind:u8 |
  format_version:u16be |
  every preceding complete TLV byte
)
```

Their outer framing length includes the checksum TLV. The checksum is verified before
the record is acted upon.

### 2.1 Record kinds and digest domains

| Record | Kind/domain byte | ID type or role |
| --- | ---: | --- |
| `RootRecordV3` | `0x10` | `RootId` |
| v3 `NodeMetadata` | `0x13` | nested canonical value, not installed alone |
| `TreePage` | `0x20` | `TreePageId` |
| `FileNode` | `0x21` | `FileNodeId` |
| `SegmentPage` | `0x22` | `SegmentPageId` |
| `Chunk` | `0x23` | `ChunkId` |
| `AttributionRoot` | `0x24` | `AttributionRootId` |
| `AttributionPage` | `0x25` | `AttributionPageId` |
| `HardlinkGroup` | `0x26` | `HardlinkGroupIdV3` |
| head | `0x30` | mutable ref record |
| operation `STATE` | `0x31` | mutable operation record |
| locator | `0x32` | mutable physical-location record |
| source lease | `0x33` | mutable lifetime record |

`RootId` remains a 32-byte nominal SHA-256 wrapper. A root's version is learned by
reading its record, never by guessing from digest bytes.

## 3. `RootRecordV3`

`RootRecordV3` has exactly three TLVs:

| Tag | Value |
| ---: | --- |
| `1` | required capability bits, `u64be` |
| `2` | `ChunkProfileId`, `u16be`; only `SeqCdcV1 = 1` |
| `3` | root-directory `FileNodeId`, 32 bytes |

Known required content capability bits remain the v2 assignments:

| Capability | Bit |
| --- | ---: |
| xattrs | `0` |
| sparse holes | `1` |
| hardlinks | `2` |
| symlinks | `3` |
| devices | `4` |
| FIFO | `5` |

Bits `6..63` are unknown required capabilities and reject. The encoded set is the
minimal union required by the reachable logical tree. A mismatch between declared
and reachable capabilities is `NonCanonicalCapability`.

The root-directory `FileNode` must be kind `Directory`. Branch, publication,
generation, parent/base, attribution, author, operation, backend and physical
location are absent by construction.

Maximum encoded root bytes: `256`.

## 4. Portable metadata and node kinds

The v3 nested `NodeMetadata` record keeps the approved v2 field tags:

| Tag | Value |
| ---: | --- |
| `1` | mode, `u32be`, only bits `0o7777` |
| `2` | logical uid, `u32be` |
| `3` | logical gid, `u32be` |
| `4` | mtime seconds, `i64be` |
| `5` | mtime nanoseconds, `u32be`, less than `1_000_000_000` |
| `6` | canonical xattr sequence |

The xattr sequence is:

```text
count:u32be |
repeat count {
  key_length:u32be | key |
  value_length:u32be | value
}
```

Keys are non-empty raw bytes, at most `255` bytes, contain no NUL, and are strictly
increasing by unsigned-byte order. Metadata records are at most `65_536` encoded
bytes. The v2 maximum path (`4096`), component (`255`), symlink target (`4096`), and
metadata validation rules remain the v3 rules.

Node-kind values remain:

| Kind | Value |
| --- | ---: |
| directory | `1` |
| regular | `2` |
| symlink | `3` |
| device | `4` |
| FIFO | `5` |

Logical uid/gid are file metadata, not attribution actor identity. Linux whiteout and
opaque carrier markers are translated before this boundary.

## 5. `TreePage`

A directory child map is a canonical bounded copy-on-write B+ page set. Page payload
TLVs are:

| Tag | Value |
| ---: | --- |
| `1` | page kind: leaf `1`, internal `2` |
| `2` | depth from leaves, `u8`; leaf is `0` |
| `3` | entry count, `u16be` |
| `4` | packed entries |

A leaf entry is:

```text
name_length:u16be | raw component bytes | FileNodeId[32]
```

An internal entry is:

```text
inclusive_upper_name_length:u16be |
inclusive_upper_raw_component |
child TreePageId[32]
```

Names and upper bounds are strictly increasing by unsigned raw-byte order. Names obey
the canonical component rules and never contain `/` or NUL. Internal upper bounds
must equal the greatest reachable key in that child. Child depths are exactly one
less than the parent. Empty is represented only by one depth-zero leaf with zero
entries. A non-root internal page has at least two children.

Canonical page boundaries are selected from the sorted entry stream by the following
history-independent rule:

1. append an entry unless it would exceed `192` entries or `65_536` encoded bytes;
2. after an appended entry, close the page when the first 12 bits of
   `SHA-256("EOS-LS3-TREE-ANCHOR\0" | name_length:u16be | name)` are zero;
3. the final page closes at end of input;
4. apply the same rule at each internal level using the inclusive upper name as the
   anchor key.

The hard size/count rule takes precedence over the anchor. This makes page shape a
function of logical ordered entries rather than mutation history, while limiting a
localized boundary ripple to the next anchor or hard page boundary. Implementations
stream page construction and do not retain a complete directory or tree.

Bounds:

- maximum encoded page: `65_536` bytes;
- maximum entries: `192`;
- maximum page depth: `16`;
- maximum logical directory nesting: `64`;
- maximum page records visited for one point lookup: `17`.

Dangling child/file IDs, incorrect upper bounds, inconsistent depth, oversized pages,
and unsorted or duplicate keys reject.

## 6. `FileNode` and hardlinks

`FileNode` has all nine tags, using canonical `None` for inapplicable fields:

| Tag | Value |
| ---: | --- |
| `1` | node kind, `u8` |
| `2` | complete v3 `NodeMetadata` record |
| `3` | optional directory child-map `TreePageId` |
| `4` | optional regular logical length, `u64be` |
| `5` | optional regular `SegmentPageId` |
| `6` | optional symlink target raw bytes |
| `7` | optional device major, `u32be` |
| `8` | optional device minor, `u32be` |
| `9` | optional `HardlinkGroupIdV3`, 32 bytes |

Required combinations:

- directory: tag 3 present, tags 4–9 absent;
- regular: tags 4 and 5 present, tag 9 optional, tags 3, 6–8 absent;
- symlink: tag 6 present, tags 3–5 and 7–9 absent;
- device: tags 7 and 8 present, all other option tags absent; `(0,0)` rejects;
- FIFO: every option tag absent.

An empty regular file still references the canonical empty depth-zero
`SegmentPage`. Symlink targets contain no NUL and are at most `4096` bytes.

`HardlinkGroup` payload TLVs are:

| Tag | Value |
| ---: | --- |
| `1` | member count, `u16be` |
| `2` | repeated `path_length:u16be | canonical raw path` |

There are `2..1024` strictly sorted, unique members. The group ID is therefore stable
logical path membership, never inode/device identity. Every member refers to the same
group ID and has equal metadata, logical length, segment root, and sparse/zero layout.
A rename changes the affected group record and all group member references as one
conflict group.

Maximum encoded `FileNode`: `131_072` bytes. Maximum encoded hardlink group:
`262_144` bytes. A larger logical link set returns `HardlinkGroupLimit`.

## 7. `SegmentPage` and sparse/zero semantics

`SegmentPage` payload TLVs are:

| Tag | Value |
| ---: | --- |
| `1` | page kind: leaf `1`, internal `2` |
| `2` | depth from leaves, `u8`; leaf is `0` |
| `3` | descriptor/child count, `u16be` |
| `4` | logical covered length, `u64be` |
| `5` | packed descriptors or children |

Leaf descriptors are:

```text
kind:u8 | logical_offset:u64be | length:u64be |
if kind == Chunk { ChunkId[32] }
```

Descriptor kinds are chunk `1`, allocated zero range `2`, and sparse hole `3`.
Descriptors are non-empty, strictly contiguous from offset zero, checked for overflow,
and cover exactly the file logical length. Adjacent zero descriptors and adjacent
hole descriptors are noncanonical and must coalesce. A chunk descriptor length is
`1..32768`.

An allocated extent is fed to SeqCDC. A resulting chunk whose every byte is zero is
encoded as a zero descriptor; other chunks install a `Chunk`. Filesystem holes are
hole descriptors and are never read as payload. This rule distinguishes allocated
zeros from holes while remaining independent of read fragmentation.

An internal entry is:

```text
child_end_exclusive:u64be | child SegmentPageId[32]
```

Ends are strictly increasing, the first child starts at zero by implication, child
coverage is contiguous, and the final end equals tag 4.

Bounds:

- maximum encoded page: `65_536` bytes;
- maximum leaf descriptors or internal children: `1024`;
- maximum page depth: `16`;
- descriptor buffering: `16` descriptors and at most `65_536` serialized bytes.

Page grouping uses the same history-independent anchor algorithm as `TreePage`, with
the domain `EOS-LS3-SEGMENT-ANCHOR\0` and the descriptor ending offset as the anchor
key.

## 8. `Chunk`

The chunk payload is the exact logical payload bytes, with no TLV. Its canonical
framed bytes are:

```text
"EOS-LS2\0" | 0x23 | 0x0003 | payload_length:u32be | payload
```

Payload length is `1..32768`. `ChunkId` is SHA-256 of those complete bytes. Install
uses put-if-absent; an existing object is reopened and its length, framing, kind,
version, ID, and payload digest are verified before it is accepted. A mismatch is
`ObjectCollisionOrCorruption`; it is never overwritten.

## 9. Attribution

`ActorId` is exactly 32 nonzero opaque bytes issued by the authenticated logical
identity layer. It is stable across hosts and sessions. Host uid/gid, environment
variables, container identity, time, and filesystem ownership are forbidden sources.

Attribution required capability bits are:

| Capability | Bit |
| --- | ---: |
| node facts | `0` |
| byte-range facts | `1` |
| logical actor plus publication facts | `2` |

The only accepted Stage 03 attribution capability value is `0x7`; other or unknown
bits reject.

`AttributionRoot` has:

| Tag | Value |
| ---: | --- |
| `1` | attribution capability bits, `u64be` |
| `2` | associated content `RootId`, 32 bytes |
| `3` | root `AttributionPageId`, 32 bytes |

The direct content-root field is the association rule. Attribution changes never
change content IDs.

`AttributionPage` has the same tags 1–4, page-kind values, internal depth rules,
history-independent grouping, `65_536`-byte maximum, `16` maximum depth, and
`128` entry/child maximum as a tree page. Its anchor domain is
`EOS-LS3-ATTR-ANCHOR\0`.

A leaf fact is:

```text
path_length:u16be | canonical raw path |
scope:u8 |
offset:u64be | length:u64be |
ActorId[32] | PublicationId[16]
```

Empty path is accepted only for the root-directory node fact. Scope values are node
`0` and byte range `1`. A node fact has zero offset and length. A range fact has
nonzero length and checked end. Facts order strictly by
`(path bytes, scope, offset, length, actor bytes, publication bytes)`. Ranges for a
path do not overlap, adjacent ranges with the same actor/publication coalesce, and
the complete current logical byte range is attributable. Internal entries contain
the complete inclusive upper fact key followed by a child page ID.

A blame query accepts at most `1024` paths/ranges, visits at most `4096` pages, emits
at most `1024` facts and at most `262_144` encoded output bytes. Exceeding a bound is
`QueryLimit`; the implementation never scans retained operation history.

## 10. Logical identifiers

| Type | Canonical wire form and validation |
| --- | --- |
| `BranchId` | `1..128` ASCII bytes; first `[a-z0-9]`, remaining `[a-z0-9._-]`; `.` and `..` reject |
| checkpoint ID | same form and bound as `BranchId` |
| `PublicationId` | 16 bytes: `sequence:u64be | nonce:u64be`; sequence is nonzero; all-zero rejects |
| `PinId` | 16 nonzero bytes |
| `LeaseId` | 16 nonzero bytes |
| `ActorId` | 32 nonzero bytes |

Binary IDs used as path components are lowercase fixed-width hexadecimal and decode
back to the identical bytes; uppercase, short, long, or nonhex spellings reject.
Policy names are already canonical and are never Unicode-normalized.

`PublicationId` is scoped to one branch. Reuse on another branch is independent.
Within a branch, create/open compares the canonical request digest. Same ID and same
digest resumes or returns the retained exact outcome; same ID and another digest is
`IdempotencyMismatch`. Existing different bytes at a content ID are
`ObjectCollisionOrCorruption`. Existing different bytes at a policy-name ref are
`IdentifierCollision`; no record is replaced implicitly.

The common operation directory ID is:

```text
SHA-256(
  "EOS-LS3-OPERATION-ID\0" |
  operation_kind:u8 |
  branch_length:u16be | branch |
  PublicationId[16]
)
```

## 11. Head record

The head record has:

| Tag | Value |
| ---: | --- |
| `1` | content `RootId`, 32 bytes |
| `2` | `AttributionRootId`, 32 bytes |
| `3` | generation, `u64be` |
| `4` | `PublicationId`, 16 bytes |
| `255` | mutable checksum |

Maximum encoded head bytes: `256`. The attribution root must name the same content
root. Advancing generation uses checked `+1`; `u64::MAX` returns
`GenerationOverflow` before any visible write.

Atomic installation is: create same-directory unique temp with no-follow semantics,
write exact bytes, fsync file, rename over the head while holding
`.storage-writer.lock`, then fsync the parent directory. Readers accept only a complete
checksum-valid record. A generation decrease is invalid except through the explicit
new-generation reset operation; reset never rewinds the counter.

## 12. Operation `STATE`

Operation kinds are publish `1`, revert `2`, reset `3`, dirty checkpoint `4`, and
hidden validation `5`.

Phases are:

| Phase | Value | Terminal |
| --- | ---: | --- |
| preparing | `1` | no |
| prepared | `2` | no |
| committed | `3` | yes |
| conflicted | `4` | yes |
| failed | `5` | yes |
| acknowledged tombstone | `6` | yes |
| expired tombstone | `7` | yes |

The state record has:

| Tag | Value |
| ---: | --- |
| `1` | operation kind, `u8` |
| `2` | canonical branch bytes |
| `3` | `PublicationId`, 16 bytes |
| `4` | canonical request SHA-256, 32 bytes |
| `5` | optional base `RootId` |
| `6` | optional base `AttributionRootId` |
| `7` | base generation, `u64be` |
| `8` | phase, `u8` |
| `9` | optional prepared/result `RootId` |
| `10` | optional prepared/result `AttributionRootId` |
| `11` | optional changed-path run SHA-256 |
| `12` | rebase-attempt count, `u8` |
| `13` | terminal outcome |
| `14` | terminal expiry Unix seconds, `u64be`; zero before terminal |
| `15` | acknowledged flag, `u8` zero or one |
| `255` | mutable checksum |

Maximum encoded `STATE`: `4096` bytes. The changed-path run is external bounded work;
complete paths, trees, histories, and payload queues never enter `STATE`.

Terminal outcome begins with a discriminant: none `0`, success `1`, conflict `2`,
failure `3`, reset `4`. Success/reset append root, attribution root, generation and
publication ID. Conflict appends a `u16be` error code and a 32-byte conflict-key-set
digest. Failure appends one `u16be` error code. Terminal fields must agree with phase,
head and request digest.

Rebase/commit is limited to `8` attempts and `60` monotonic seconds, whichever occurs
first. A terminal full outcome is retained for `86_400` seconds. Acknowledgement or
expiry atomically replaces it with a checksum-valid tombstone retaining branch,
publication ID, request digest and outcome digest. Stage 03 never deletes tombstones;
later bounded retirement requires a separately versioned Stage 05 compaction index.
A tombstone retry returns `OutcomeExpired`, never starts new work.

Boot enumerates at most `1024` nonterminal states per recovery batch, with fixed
`4 MiB` owned metadata and `64 MiB` global storage-byte permits. Additional states are
processed in later batches. The head's publication ID is repaired to a terminal
outcome before that branch may advance.

## 13. Locator and source-protection lease

These records exist only when an otherwise reachable v3 object has its last payload
in an existing v1 carrier.

Locator fields:

| Tag | Value |
| ---: | --- |
| `1` | typed object record kind, `u8` |
| `2` | typed object digest, 32 bytes |
| `3` | locator generation, nonzero `u64be` |
| `4` | carrier kind; existing v1 carrier is `1` |
| `5` | stable v1 carrier ID, 32 bytes |
| `6` | offset, `u64be` |
| `7` | length, nonzero `u64be` |
| `8` | SHA-256 of exact located payload bytes |
| `255` | mutable checksum |

Source-lease fields:

| Tag | Value |
| ---: | --- |
| `1` | `LeaseId`, 16 bytes |
| `2` | protected holder content `RootId`, 32 bytes |
| `3` | v1 carrier ID, 32 bytes |
| `4` | locator generation, nonzero `u64be` |
| `5` | fence token, nonzero `u64be` |
| `6` | protected physical bytes, `u64be` |
| `255` | mutable checksum |

Maximum encoded locator and lease records: `512` bytes each. Offset+length is checked.
Before a dependent ref becomes visible, the implementation:

1. opens the existing carrier by stable catalog ID without following an untrusted
   path;
2. reads a checksum-valid locator and verifies kind, object ID, generation and range;
3. streams the located bytes and verifies both payload SHA-256 and typed object ID;
4. creates/fsyncs the lease with a fence at least the locator generation;
5. rereads the locator generation and carrier catalog generation;
6. fails closed on change, absence, corruption or a last-location mismatch; otherwise
   fsyncs the lease directory before head/ref visibility.

An all-loose root creates neither record. No `refs/legacy` mapping is authorized.

## 14. Typed errors and numeric outcome codes

Core errors remain allocation-free. Stage 03 adds the following exact error
classifications; terminal wire codes are stable:

| Code | Error |
| ---: | --- |
| `1` | `WrongKind` |
| `2` | `UnsupportedVersion` |
| `3` | `WrongDomain` |
| `4` | `TrailingBytes` |
| `5` | `NonCanonicalOrder` |
| `6` | `DuplicateEntry` |
| `7` | `CountLimit` |
| `8` | `LengthLimit` |
| `9` | `PageLimit` |
| `10` | `DepthLimit` |
| `11` | `DanglingEdge` |
| `12` | `SparseInvalid` |
| `13` | `UnknownRequiredCapability` |
| `14` | `ChecksumMismatch` |
| `15` | `CorruptRecord` |
| `16` | `ArithmeticOverflow` |
| `17` | `InvalidIdentifier` |
| `18` | `ObjectCollisionOrCorruption` |
| `19` | `IdentifierCollision` |
| `20` | `IdempotencyMismatch` |
| `21` | `OutcomeExpired` |
| `22` | `GenerationOverflow` |
| `23` | `Conflict` |
| `24` | `ContentionLimit` |
| `25` | `ResourceExhausted` |
| `26` | `QueryLimit` |
| `27` | `HardlinkGroupLimit` |
| `28` | `LastLocatorMissing` |
| `29` | `LastLocatorCorrupt` |
| `30` | `UnsupportedRequiredCapability` |
| `31` | `DigestCollision` |
| `32` | `RequestDeadline` |

The decoder distinguishes wrong kind, version and nominal digest domain. It proves
count/byte lower bounds before reserving, limits each nested record before reading
its body, and never preserves unknown required data.

## 15. Global bounds

| Bound | Approved value |
| --- | ---: |
| generic v3 record | `262_144` bytes |
| root/head | `256` bytes |
| tree/segment/attribution page | `65_536` bytes |
| file node | `131_072` bytes |
| metadata | `65_536` bytes |
| hardlink group | `262_144` bytes |
| chunk payload | `32_768` bytes |
| operation state | `4_096` bytes |
| locator/source lease | `512` bytes |
| tree page entries | `192` |
| segment descriptors/children | `1024` |
| attribution facts/children | `128` |
| tree/segment/attribution page depth | `16` |
| logical path bytes/component/depth | `4096 / 255 / 64` |
| xattr key | `255` bytes |
| symlink target | `4096` bytes |
| query input/output/pages/output bytes | `1024 / 1024 / 4096 / 262144` |
| external merge fan-in/read buffer | `8 / 65_536` bytes |
| encoder scratch/index cache | `262_144 / 16 MiB` |
| per-publication metadata/global owned bytes | `4 MiB / 64 MiB` |
| storage workers | `4` |
| rebase attempts/operation deadline | `8 / 60 seconds` |

The Preparation 04 limits remain stricter where they govern a runtime resource:
no payload queue; 16 descriptors/64 KiB metadata; 5% staging; 96 bytes/chunk,
64 bytes/segment, 256 bytes plus path per changed-path record; 384 MiB absolute RSS
and 128 MiB above idle.

## 16. v2 coexistence and import

1. All v2 kinds, tags, payload widths, values, golden bytes and typed IDs remain
   byte-for-byte unchanged.
2. Dispatch uses `(magic, kind, version)`. No v2 byte sequence is accepted as v3 and
   no v3 byte sequence is accepted as v2.
3. A v2 import decodes and validates the complete v2 record through the existing
   bounded v2 path, streams entries in canonical path order, and constructs new v3
   chunks/pages/nodes. It never aliases a v2 digest into a v3 nominal ID.
4. v2 parent, base, generation and publication identity are not imported into content
   identity. The private v3 operation records its own base/publication facts.
5. v2 sparse holes become v3 hole descriptors. Allocated all-zero chunks follow the
   v3 zero rule. v2 hardlink ranks are converted to the v3 sorted-path
   `HardlinkGroup`.
6. Any missing v2 object, corrupt reference, unsupported required capability, or
   unavailable last v1 location returns the typed error and exposes no v3 ref.
7. Public v1 routing and `Manifest::root_hash` remain unchanged throughout.

## 17. Immutable fixture and benchmark corpus

The owner-approved manifest is
[`stage03_v3_owner_corpus_v1.json`](stage03_v3_owner_corpus_v1.json).

Its full SHA-256 is:

```text
7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be
```

The manifest freezes:

- exact canonical bytes, lengths and SHA-256 IDs for root, metadata, tree page, file
  node, segment page, chunk, attribution page/root, head, operation state, locator
  and source lease;
- all mandatory hostile vector classes;
- a standard-library-reproducible deterministic corpus generator;
- the complete Preparation 04 qualification corpus descriptors; and
- the smaller deterministic Stage 03 focused 180-second corpus descriptors.

The manifest file is immutable. Generated fixture directories must carry this exact
manifest unchanged and verify its digest before producing or consuming data. A
semantic, numeric, generator, seed, or golden change requires a new decision ID,
manifest version, file name, and full owner approval.

## 18. Stage 03 specification conformance matrix

| Stage 03 requirement | Closed by |
| --- | --- |
| bounded Merkle identity and v2 read compatibility | §§2–8, 15–17 |
| attribution separate from content identity | §§3, 9 |
| deterministic streaming SeqCDC and typed chunks | §§1, 7–8, 15 |
| changed-path page updates and structural sharing | §§5–7 |
| private heads/checkpoints/pins and complete ref semantics | §§10–12 plus normative Stage 03 ref table, unchanged |
| durable branch-scoped idempotency and recovery | §§10–12 |
| semantic OCC and bounded disjoint rebase | §12 bounds plus normative Stage 03 conflict-key rules, unchanged |
| durable imported-v1 source protection | §13 |
| hidden normal-protocol validation, public v1 unchanged | §1 and §16 |
| exact formats/tags/domains/bounds/errors | §§2–15 |
| immutable corpus and full digest | §17 |
| no Stage 04–07 drift or new dependency | §1 |

All behavior not numerically specialized in this decision remains exactly as stated in
the Stage 03 specification, storage contract, Preparation 04, and canonical
implementation guide. This decision supplies missing wire authority; it does not
weaken their completion or evidence gates.
