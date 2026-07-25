# Stage 03 G01 approval and closure audit — 2026-07-25

Status: **PASS**

Closed at: `2026-07-24T21:58:21Z`

## Authority change

The owner resumed the Stage 03 goal and stated:

> proceed with my approval and you must not stop and auto approve if the blocker does
> not drift from stage 3 spec

That instruction supplies the missing authority to select and freeze exact values
only within the existing Stage 03 specification. It does not authorize a scope,
authority, dependency, resource, or later-stage drift.

The resulting approved amendment is:

- decision:
  [`contract_v3_owner_decision_g01_1.md`](contract_v3_owner_decision_g01_1.md);
- decision ID: `PRC-STAGE03-OWNER-DECISION-G01.1`;
- decision SHA-256:
  `27264ef96f97960757eeba0b51bb7d2560446466cbf8e6a11c99a881da834e16`;
- immutable fixture/benchmark manifest:
  [`stage03_v3_owner_corpus_v1.json`](stage03_v3_owner_corpus_v1.json);
- manifest SHA-256:
  `7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be`.

## Complete §5.2 audit

| Required decision row | Exact closure |
| --- | --- |
| `RootRecordV3` / `RootId` | Decision §§2–3 fixes version 3, kind/domain `0x10`, three identity fields, capability behavior, size, hashing, exclusions and v2 coexistence. |
| `TreePage` | §5 fixes kind/domain `0x20`, leaf/internal bytes, canonical raw ordering, deterministic page boundaries, fanout, encoded size, depth and dangling-edge validation. |
| `FileNode` | §§4 and 6 fix kind/domain `0x21`, metadata and per-kind option fields, xattr/symlink/device/FIFO rules, logical size, hardlink association and bounds. |
| `SegmentPage` | §7 fixes kind/domain `0x22`, descriptor bytes, sparse/hole/zero/chunk rules, contiguity, page formation, fanout/length/depth bounds. |
| `Chunk` | §8 fixes kind/domain `0x23`, exact raw payload framing, `1..32768` bound, ID and put-if-absent verification. |
| `AttributionRoot` | §9 fixes kind/domain `0x24`, capabilities, content-root association, page root, ID and bound. |
| `AttributionPage` / `ActorId` | §9 fixes kind/domain `0x25`, stable non-host actor bytes, node/range facts, order, fanout, page/query/output bounds and no-history-scan rule. |
| branch/publication/checkpoint/pin/lease IDs | §10 fixes syntax, byte lengths, canonical path spelling, branch scoping, collision and mismatch behavior. |
| head | §11 fixes kind `0x30`, fields, checksum, 256-byte bound, overflow behavior and atomic validation/install. |
| operation `STATE` | §12 fixes kind `0x31`, operation/phase enums, all atomic fields, checksum, 4096-byte bound, attempt/deadline/retention/ack/expiry behavior and exact outcomes. |
| locator/source lease | §13 fixes kinds `0x32`/`0x33`, fields, fence/checksum/size rules and last-location validation before ref visibility. |
| decoder errors | §14 fixes all mandatory hostile classes and stable terminal numeric codes. |
| approved maximum sizes | §15 fixes all record/page/count/depth/query/operation bounds at or below Preparation 04 limits. |
| v2 compatibility/import | §16 preserves every v2 byte/ID/decoder and defines typed streaming v2→v3 import without digest aliasing or public-authority change. |
| immutable corpus | §17 names the immutable manifest and its full SHA-256; the manifest contains 14 exact goldens, 16 hostile classes, all seven Preparation 04 corpus families and four Stage 03 focused corpus arms. |

## Non-drift audit

The amendment was checked against the full Stage 03 specification, Stage 03 E2E
plan, storage contract, Stage 02 D2.5 decision, Preparation 03 profile and Preparation
04 bounds.

It preserves:

- public `LegacyV1` sole authority and unchanged v1 identity;
- content/attribution separation;
- the approved scalar SeqCDC profile;
- bounded streaming, page sharing and changed-only mutation;
- branch-scoped idempotency, exact retry, semantic OCC and short commit lock;
- conditional last-v1-carrier protection only;
- zero new external dependencies/helpers/services/network;
- Stage 04–07 ownership and qualification deferrals.

No Stage 03 requirement was removed, weakened, converted to optional, or claimed as
implemented by this decision.

## Mechanical validation

The manifest parsed as JSON. Every golden hex string decoded to its declared byte
length and SHA-256. The manifest has:

- `14` exact contract goldens;
- `7` qualification corpus descriptors;
- `4` focused corpus descriptors;
- `16` hostile-vector classes.

The decision contains every §5.2 record/type name, v2 coexistence, immutable-corpus
authority, the mandatory hostile errors and all numeric bounds. Markdown fences are
balanced and `git diff --check` passed for both new authority files.

## Gate verdict

`S03-G01 = PASS`.

The previous three blocker audits remain retained history. Their conclusion was
correct for the authority state when they ran; this fourth record supersedes the
blocker only because the owner supplied new approval. Gated implementation may now
begin from the exact decision and manifest above. No implementation, E2E or benchmark
row passes merely because this authority gate closed.
