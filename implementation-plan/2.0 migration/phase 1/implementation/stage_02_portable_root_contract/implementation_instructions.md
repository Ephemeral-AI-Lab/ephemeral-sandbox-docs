# Stage 02 Implementation Instructions

> **Status:** Instructional document only. Stage 02 is still proposed. Nothing
> in this document claims that Stage 02 code, tests, E2E evidence, benchmark
> evidence, dependency comparison, or completion criteria have passed.
>
> **Authority:** For implementation behavior and evidence, the existing
> [Stage 02 specification](spec.md) and [Stage 02 E2E plan](e2e_test.md) remain
> authoritative. If this guide differs from either source, stop and reconcile
> the guide; do not weaken or reinterpret the source.

## 1. Purpose and expected outcome

Stage 02 introduces a deterministic, versioned, backend-neutral contract for
portable logical roots. It does so by adding a standard-library-only internal
crate, canonical binary records, validated Linux path bytes, nominal
identities, logical tree/root values, and narrow byte/digest ports.

The expected outcome is deliberately offline:

- canonical v2 values can be constructed, encoded, decoded, and hashed
  deterministically in focused Rust and golden tests;
- the same logical input produces the same canonical bytes and typed
  identities regardless of insertion order used to prepare canonical input,
  `Read` fragmentation, host path conventions, native word size, or byte
  order;
- malformed input fails closed without panic, repair, fallback, excessive
  allocation, or side effects; and
- the new core can be removed with its single internal dependency edge because
  no v2 durable state exists.

The runtime invariants are more important than the new types:

- legacy LayerStack v1 remains the **sole runtime read, write, and publication
  authority**;
- `Manifest::root_hash` remains the only runtime/public revision identity and
  is never reinterpreted as a v2 `RootId`;
- public command, file, PTY, mount, publication, and revision behavior remain
  v1-compatible;
- no candidate root, object, manifest, catalog, journal, materialization, or
  other v2 path is written under `/eos`; and
- Stage 01 workspace-scoped execution transcripts remain provider-local
  scratch. Their paths, session IDs, execution IDs, contents, and lifecycle
  state never participate in portable identity.

`RootId` at Stage 02 is a nominal value plus a deterministic computation. It
is not an active root, a published revision, a migration mapping, a storage
locator, or a rollout selector.

## 2. Prerequisites and required reading

Stage 00 is the only formal prerequisite. Stage 01 has completed at the POC
tier and its behavior must be preserved, but the Stage 01 layout is not a
Stage 02 prerequisite and must not become an identity input.

Read the following sources completely before editing:

| Source | What it contributes |
| --- | --- |
| [`../index.md`](../index.md) | Phase 1 authority, global invariants, dependency direction, stage DAG, physical-state model, pinned image, and the boundary between Stage 02 POC evidence and Stage 11 qualification. |
| [`../stage_00_baseline_evidence/spec.md`](../stage_00_baseline_evidence/spec.md) | The completed legacy behavior, bounded observability, v1 fixture, dependency, environment, compatibility, and logical-release contracts inherited by Stage 02. |
| [`../stage_00_baseline_evidence/e2e_test.md`](../stage_00_baseline_evidence/e2e_test.md) | The immutable baseline artifacts, exact dependency comparator contract, public legacy-route evidence conventions, run-owned cleanup, and Stage 11 “do not run” boundaries. |
| [`../stage_01_workspace_scratch/spec.md`](../stage_01_workspace_scratch/spec.md) | Completed workspace-scoped transcript ownership, containment, release-before-delete, bounded legacy reaping, and provider-local behavior that Stage 02 must preserve. |
| [`../stage_01_workspace_scratch/e2e_test.md`](../stage_01_workspace_scratch/e2e_test.md) | The passed Stage 01 stable IDs, benchmark/catalog additions, public behavior, cleanup contracts, and evidence that must not be renamed or absorbed. |
| [`handoff_from_stage_01.md`](handoff_from_stage_01.md) | Actual handoff custody, preserved tracked and untracked changes, immutable Stage 00 comparison bases, overlapping dirty files/catalogs, passed Stage 01 evidence, and warnings about prior unrelated failures. |
| [`spec.md`](spec.md) | Authoritative Stage 02 scope, architecture, types, canonical rules, runtime invariants, forbidden paths, implementation order, and completion checklist. |
| [`e2e_test.md`](e2e_test.md) | Authoritative Stage 02 focused commands, PRC-R01–PRC-R08 evidence, PRC-01 live proof, benchmark contract, artifact rules, and POC verdict. |

Repository-local instructions must also be read from the product, test, and
documentation repositories before work begins. Resolve their scope by
directory ancestry. A repository-local instruction cannot silently override
the owner-mandated Phase 1 branch or authorize destructive custody changes;
record and escalate any conflict.

Inherited status must be described precisely:

- Stage 00 is completed and is the formal prerequisite. Reuse its immutable
  evidence and exact comparator; do not rerun passing live Stage 00 cases just
  to recreate evidence.
- Stage 01 is completed and must be preserved. Its workspace scratch locator,
  execution leases, terminal ownership, teardown ordering, legacy reaper,
  bounded observations, stable E2E declarations, and benchmark catalog entry
  are existing work.
- Stage 02, PRC-01, PRC-R01–PRC-R08, and the portable-root tiny benchmark are
  future work. Do not describe any of them as implemented or passed until the
  required evidence exists.

### Inherited evidence and compatibility contracts

Do not rename, absorb, or casually rerun the inherited declarations:

| Stage | Stable ID | Status and Stage 02 use |
| --- | --- | --- |
| 00 | `layerstack.phase1.baseline.legacy-route` | Completed focused legacy-route, content, resource, and cleanup evidence. Reuse its v1 oracle and public observation contract. |
| 00 | `layerstack.phase1.baseline.restart-cleanup` | Completed focused legacy recovery evidence. Preserve its visibility and deterministic cleanup contract. |
| 00 | `layerstack.phase1.baseline.tiny` | Completed raw legacy-control baseline. Reuse the frozen control; it is not a candidate benchmark result. |
| 00 | `layerstack.phase1.qualification.all` | `planned-final`; owned by Stage 11. Do not execute or claim it in Stage 02. |
| 01 | `phase1.stage01.workspace-scratch.lifecycle` | Completed. Preserve workspace containment, transcript isolation, owner-release-before-delete, no-new-global-write, and cleanup behavior. |
| 01 | `phase1.stage01.workspace-scratch.restart-reap` | Completed. Preserve restart isolation and the bounded containment-safe legacy reaper. |
| 01 | `phase1.stage01.workspace-scratch.tiny` | Completed tiny benchmark sentinel. Preserve its catalog operation and strict fixtures. |
| 01 | `phase1.final.workspace-scratch.qualification` | `planned-final`; owned by Stage 11. Do not execute or claim it in Stage 02. |
| Existing public compatibility | `runtime.workspace-session.publish.no-op` and `runtime.workspace-session.publish.changed` | Supporting public v1 references only. Do not relabel them as v2 proof or add duplicate declarations. |

Stage 00's exact runtime seam is
`runtime.layerstack.rollout_mode: legacy`, observed through the existing
`sandbox-observability-cli snapshot/layerstack` projection and bounded
`LayerStackRouteSnapshot` / `LayerStackResourceSnapshot` fields. Preserve the
`StorageRouteObservationV1` / `StorageResourceObservationV1` artifact
contract: configured mode is `legacy`, read/write/publication authority is
`legacy_v1`, candidate activity is explicitly zero, and a missing mandatory
field is unavailable/failing evidence rather than an inferred zero. Keep the
exact v1 fixture, `manifest.json` bytes, `Manifest::root_hash`, atomic
visibility, fsync/OCC behavior, public CLI responses, and run-owned artifact
schemas unchanged.

The Stage 01 handoff records concrete evidence that may be referenced rather
than recreated:

- lifecycle verdict:
  `.e2e-state/reports/workspace-session/workspace-session-20260724-202348/phase1.stage01.workspace-scratch.lifecycle/verdict.json`,
  `sha256:76e29502f281c42282769cb918bd2ba60f4cf4128a07f6c60d079f45c7262d74`;
- restart/reap verdict:
  `.e2e-state/reports/workspace-session/workspace-session-20260724-202453/phase1.stage01.workspace-scratch.restart-reap/verdict.json`,
  `sha256:96c0a717b43d41b7a86d802ba913f9c39b1c62efff35197b0f421921f47dc772`;
- final tiny benchmark run:
  `019f9430-f031-748b-a29a-42f9542c1ac8`; and
- exact Stage 01 dependency comparison:
  `.e2e-state/evidence/stage01-offline/dependency-delta.json`,
  `sha256:3995bdabcc6f732883ee831189e690a60faa0cf58fe9e2a0be95870278a2b945`.

These paths are relative to the test repository. Verify that retained
artifacts still match their recorded digests before relying on them; do not
rewrite an inherited artifact to make it match.

## 3. Repository custody and pre-edit procedure

### Recorded Stage 01 handoff

The handoff is a working-tree handoff, not a commit handoff:

| Repository | Recorded branch | Recorded HEAD and upstream | Recorded handoff state |
| --- | --- | --- | --- |
| Product: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox` | `upgrade-2.0-phase-1` | `3a450d052b68daf45588328f723e50662808d266`; `origin/upgrade-2.0-phase-1` at the same revision | Dirty Stage 00 plus Stage 01 implementation. Tracked and untracked files are intentional. |
| Test: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test` | `upgrade-2.0-phase-1` | `100d11c8f00b9774cbb7b509212d11742ae48bf5`; `origin/upgrade-2.0-phase-1` at the same revision | Dirty Stage 00 plus Stage 01 harness/evidence. Tracked and untracked files are intentional. |
| Documentation: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs` | `layerstack_2_0` | `537938fe7c10a7607c408d2487199ac08a6dba44`; `origin/layerstack_2_0` at the same revision | Existing Phase 1 planning edits, completed Stage 01 checklist, and the Stage 01 handoff. |

The immutable Stage 00 comparison bases are:

- product: `7e8f4562f9079f27dcb5b514f6e4546b87e5aa04`;
- test: `d594f0c72083c39f95334fac685399bca20193f0`.

These values describe the recorded handoff, not a promise that the repositories
will still have those HEADs when implementation starts. The recorded product
and test HEADs did not contain the dirty Stage 01 implementation. Never infer
that implementation from `git log`, and never restore dirty files from those
HEADs.

### Mandatory pre-edit record

Before the first Stage 02 edit, record for all three repositories:

- repository absolute path;
- current branch;
- exact `HEAD`;
- upstream name and upstream revision, or the explicit absence of an
  upstream;
- complete tracked, staged, unstaged, ignored-as-relevant, and untracked
  worktree status;
- immutable implementation base and the source of owner approval;
- responsible implementer;
- the preserved Stage 00/01 status inventory; and
- two agreeing Stage 02 entry dependency captures for every frozen
  target/feature invocation.

Use read-only Git inspection. `git status --short --untracked-files=all` is
the minimum worktree inventory; also inspect staged and unstaged diffs and
list untracked files explicitly. If the live state differs from the handoff,
first determine whether the preserved work was committed, moved, or changed
by another owner. A clean status at a newer HEAD is not by itself proof that
the inherited Stage 00/01 work is present.

### Dirty-tree custody rules

- Preserve every inherited Stage 00/01 tracked and untracked change.
- Isolate the Stage 02 diff by path and responsibility. Keep an explicit
  inventory of files created or changed only for Stage 02.
- Inspect a dirty file as it exists in the worktree. Merge into it; do not
  replace it with the version from `HEAD`.
- Do not commit, push, stash, reset, switch branches, clean, discard, move, or
  otherwise change custody without explicit owner authorization.
- Do not use broad cleanup, Docker prune, global gateway termination, process
  scans/kills, or cleanup by unresolved glob.
- If unrelated mutation continues while implementing, stop at a safe boundary,
  recapture status, identify ownership, and obtain a custody decision.

The handoff identifies these overlaps:

| Area | Preserved state and required handling |
| --- | --- |
| Product LayerStack | `crates/sandbox-runtime/layerstack/src/stack/ops/publish.rs` and `crates/sandbox-runtime/layerstack/src/storage/whiteout.rs` were already dirty. Stage 02 should not need to rewrite them; if a compatibility test forces an edit, use merge-style editing and preserve all Stage 00/01 changes. |
| Workspace and operation | Preserve the workspace scratch locator, move-only execution leases, terminal ownership, release-before-delete ordering, restart recovery, and bounded legacy reaper. The portable core must not import or own them. |
| Operation catalog | Preserve the hidden same-revision legacy-control adapter and the public/hidden partition. Stage 02 evidence must not expose benchmark-only operations as public runtime operations. |
| Daemon observability | Preserve all bounded Stage 00/01 route, ownership, teardown, and reaper fields. Any dormant Stage 02 fields are additive, closed, bounded, and explicitly zero. |
| Benchmark definitions | The handoff catalog contains nine operations and a passing exact-count API contract. Extend the existing catalog deliberately and update strict fixtures coherently; do not replace the scheduler or silently change count expectations. |
| E2E catalog | Preserve both Stage 01 declarations, IDs, markers, and validation contracts. Add the Stage 02 declaration without renaming or absorbing Stage 01 cases. |
| Dependency comparator | Reuse `e2e/tools/verify_external_dependency_delta.py` and the immutable Stage 00 baselines. Do not fork a second comparator. |
| `/eos` state | Accept `workspace/<session>/executions` as the already-completed Stage 01 delta. It remains unrelated to portable identity. No Stage 02 v2 path may appear. |

### Custody inconsistency and reconciliation

The Stage 02 entry text asks for clean scoped worktrees, while the owner
handoff explicitly preserves dirty Stage 00/01 tracked and untracked work.
Do not silently choose one description.

Reconcile it as follows:

1. capture the full live state and the historical handoff values;
2. ask the repository owner whether direct work on the preserved dirty tree
   is authorized;
3. do not create cleanliness by committing, stashing, resetting, switching,
   cleaning, or discarding unless the owner explicitly authorizes that exact
   custody action;
4. if direct dirty-tree work is authorized, record the decision as the
   reconciliation of the entry condition and maintain a path-by-path Stage 02
   diff inventory; and
5. if authorization is withheld, return `POC BLOCKED` before editing.

## 4. Stage 02 scope

Stage 02 must implement all of the following and nothing from a later storage
stage:

1. **A std-only core crate.** Add the internal package
   `sandbox-runtime-layerstack-core`, forbid unsafe code, and give it no
   external, dev, build, target, proc-macro, or system dependency.
2. **A canonical codec and bounded decoder.** Handwrite deterministic
   streaming encode/decode over narrow sinks/sources, with explicit
   domain/kind/version, fixed byte order, checked lengths, exact consumption,
   and bounded errors.
3. **Typed identities.** Add nominal `Digest32`, `RootId`,
   `TreeManifestId`, `ObjectId`, `ObjectKind`, `PublicationId`,
   `PublicationIdentity`, `FormatVersion`, and `ChunkProfileId` values so
   unrelated domains cannot be interchanged.
4. **Portable Linux path bytes.** Add `CanonicalPath` for validated relative
   Linux byte paths, including byte-preserving non-UTF-8 names and ordinary
   backslashes.
5. **Capabilities.** Add a closed, version-aware `CapabilitySet` whose unknown
   required bits fail closed.
6. **Logical tree and root records.** Add canonical final-tree entries,
   portable node metadata, xattrs, sparse extents, segment references,
   hardlink-group identity, `RootRecordV2`, and publication identity.
7. **Narrow variation points.** Add only canonical sink, canonical source,
   and typed-digest ports. Do not add repositories, factories, managers, async
   runtimes, or context bags.
8. **LayerStack-owned adapters.** In the existing LayerStack crate, use its
   existing `sha2` edge for typed/domain-separated SHA-256 and its existing
   `serde` edge for outward diagnostic/compatibility envelopes.
9. **Immutable goldens and focused product tests.** Freeze exact canonical
   bytes, typed IDs, host-independence vectors, malformed vectors, mutation
   matrices, fragmentation behavior, and unchanged v1 fixtures.
10. **Feature-off public proof.** Add and run only the focused packaged case
    `runtime.layerstack-phase1.portable-root.feature-off` / PRC-01 to prove
    v1 authority and zero candidate activity.
11. **Tiny diagnostic adapter and preset.** Extend the existing benchmark
    laboratory with the bounded portable-root probe and
    `layerstack-phase1-tiny-portable-root`; do not add another scheduler.
12. **Dependency and source-boundary proof.** Compare exact external
    identities/features/edges for every frozen invocation, audit the core
    manifest and imports, and record the permitted internal edge.
13. **Closure documentation.** Append every live plan/result to
    `e2e/test-report.md`, update the Stage 02 completion checklist only after
    evidence actually passes, update `docs/maintainer-architecture.md`, and
    produce a custody-aware final handoff.

## 5. Explicit non-goals

Do not include any of the following:

- SeqCDC or the `seqcdc-scalar-author-v1` implementation;
- payload chunking or a CDC stream;
- CAS payload persistence;
- objects, loose-object payloads, packs, indexes, catalogs, journals, format
  markers, leases, retention, maintenance, quarantine, trash, or v2 staging
  directories;
- candidate writes, shadow writes, or candidate publication;
- candidate reads, hydration, or materialization;
- migration or v1→v2 mappings;
- shadow ingest;
- strict candidate activation or any mount of a candidate carrier;
- changes to public, read, write, or publication authority;
- GC, retention, compaction, or squash;
- mixed-root authority, fallback, or rollout behavior;
- SIMD, acceleration, unsafe code, C/C++, FFI, vendored code, or runtime CPU
  dispatch;
- a service, daemon, sidecar, database, FUSE layer, helper, shell dependency,
  target-image utility, network requirement, runtime download, or privilege
  change;
- production rollout, release enablement, or legacy retirement; and
- Stage 11 affected regression, required-host qualification, selection
  campaigns, RSS-scale matrix, space campaigns, soak, or final go/no-go.

Whiteout devices and opaque-directory xattrs are not complete-tree root values
in Stage 02. Backend-neutral future transition operations named in the spec
(`RemoveEntry` and `ReplaceSubtree`) do not authorize implementing transition
records now.

## 6. Architecture and dependency boundaries

The required direction is:

```text
workspace/provider adapters → layerstack → layerstack-core
```

The single Stage 02 product edge points inward from
`sandbox-runtime-layerstack` to `sandbox-runtime-layerstack-core`. Provider,
workspace, operation, daemon, E2E, and benchmark code do not become core
dependencies.

| Owner | Owns in Stage 02 | Must not own |
| --- | --- | --- |
| `layerstack-core` | Validated portable values, canonical byte transforms, closed contract errors, and narrow sink/source/digest interfaces. | SHA implementation, serde, JSON, host paths, persistence, clocks, filesystem operations, fsync, publication locks, leases, `/eos`, Docker, OverlayFS, mounts, namespaces, telemetry, async tasks, or rollout. |
| Existing LayerStack crate | Existing `sha2` and `serde` adapters, host/provider paths, v1 compatibility, atomic files, fsync, storage root, publication, leases, and future persistence/materialization adapters. | Changes to the logical v2 identity policy outside the core contract. |
| Workspace/provider adapters | Capture/provider-local translation and, in later stages, conversion of Linux upper state to core-facing values. | Root hashing, root persistence, publication policy, or portable identity. |
| External E2E/benchmark | Public packaged proof, bounded scheduling, outside accounting, artifact validation, and exact run-owned cleanup. | Product authority, private backdoors, a second scheduler, or cleanup outside the run. |

The core remains standard-library-only so that:

- portable identity does not inherit a backend, serialization framework, hash
  implementation, runtime, or provider dependency;
- future Docker, Firecracker, and WASM materializers can consume the same
  logical contract without reversing dependency direction;
- canonical bytes are controlled by one explicit versioned codec rather than
  a library’s host- or version-sensitive defaults; and
- the Stage 00 external dependency set, features, and direct-edge multiset can
  remain exactly unchanged.

### Forbidden imports and edges

The core must not import or depend on:

- `serde`, `sha2`, or another digest/serialization crate;
- `Path`, `PathBuf`, host canonicalization, filesystem persistence, or fsync;
- `/eos` layout constants;
- Docker, OverlayFS, mount, namespace, guest-agent, WASM-runtime, provider, or
  materialization types;
- runtime operation, configuration, observability transport, telemetry, E2E,
  benchmark, or test-support types;
- async runtimes, workers, queues, global registries, services, databases,
  FUSE, C/C++, or FFI.

Also forbid LayerStack → operation/E2E/benchmark, workspace → object/catalog
implementation, provider → root/publication/lease/GC policy, product → test
support, reverse core → LayerStack edges, and dependency cycles.

### Permitted manifest and lockfile delta

Only these changes are permitted:

- add one workspace member for `sandbox-runtime-layerstack-core`;
- add one internal dependency from `sandbox-runtime-layerstack` to that core;
- add the local core package stanza to `Cargo.lock`.

The new core manifest has package metadata and lints only. It has no
`[dependencies]`, `[dev-dependencies]`, `[build-dependencies]`, target
dependency, build script, `links`, or proc-macro behavior. Existing `sha2` and
`serde` edges stay in LayerStack; they are not relocated. External packages,
versions, sources, checksums, enabled features, and direct manifest edges have
an exact delta of zero.

## 7. Types and canonical contract

### Required value types

| Type | Required semantics |
| --- | --- |
| `Digest32([u8; 32])` | Exact 32-byte digest value. It does not select or implement SHA in the core. |
| `RootId(Digest32)` | Nominal, domain-separated identity of the exact canonical `RootRecordV2`. It is not a v1 `root_hash`, physical layer hash, active revision, or locator. |
| `TreeManifestId(Digest32)` | Nominal, domain-separated identity of the complete canonical tree-manifest byte stream. It is not interchangeable with `ObjectId`. |
| `ObjectId { kind, digest }` | Typed identity of canonical object bytes. The `ObjectKind` is part of the domain. |
| `ObjectKind` | Exact declared discriminants: `FileSegments = 2`, `ChunkPayload = 3`, `Transition = 4`. Stage 02 does not persist any of them. |
| `PublicationId([u8; 16])` | Caller-stable, nonzero idempotency value. It is supplied by future publication and is not generated from host randomness in the core. |
| `PublicationIdentity { generation: u64, id: PublicationId }` | Identity-bearing publication generation and request identity. |
| `FormatVersion` | Explicit version value. `ROOT_FORMAT_V2` is `FormatVersion::new_const(2)`. |
| `ChunkProfileId` | Nominal identity-bearing profile value. Stage 02 defines its portable representation but does not implement SeqCDC. |
| `CapabilitySet` | Version-aware capability bits. Unknown required bits reject; unsupported required metadata never degrades silently. |
| `CanonicalPath(Vec<u8>)` | Non-empty relative Linux path components encoded as raw bytes and separated by `/`. Validation is constructor-enforced. |
| `TypedDigest` | Narrow typed-digest port. It accepts a digest domain plus bytes and returns `Result<Digest32, Error>`; the core defines the contract but no SHA implementation. |
| `CanonicalSink` | Narrow streaming output port with `write_all` semantics. Partial writes are either completed by the contract or become a bounded error; no valid partial record is exposed. |
| `CanonicalSource` | Narrow bounded streaming input port used for fragmented reads and exact-consumption checks. The sources require the port but do not specify a copy-ready trait signature. |

### Root and tree values

`RootRecordV2` contains exactly these identity-bearing logical fields:

- `format: FormatVersion`;
- `required_capabilities: CapabilitySet`;
- `chunk_profile: ChunkProfileId`;
- `tree_manifest: TreeManifestId`;
- `parent: Option<RootId>`;
- `base: Option<RootId>`; and
- `publication: PublicationIdentity`.

`parent` and `base` are provenance and future weak GC edges. They become
retention edges only when an independent pin, lease, active branch, retention
window, frontier, or pending transaction selects them.

The complete tree manifest is the reconstruction graph. It contains
canonically ordered entries:

- `Directory { path, meta }`;
- `RegularFile { path, meta, logical_len: u64, sparse_extents, segments:
  ObjectId, hardlink_group: Option<[u8; 16]> }`;
- `Symlink { path, meta, target: Vec<u8> }`;
- `Device { path, meta, major: u32, minor: u32 }`; and
- `Fifo { path, meta }`.

Portable `NodeMetadata` contains:

- `mode: u32`;
- `uid: u32`;
- `gid: u32`;
- `mtime_seconds: i64`;
- `mtime_nanoseconds: u32`; and
- canonically ordered, unique raw-byte xattrs.

Sparse extents, xattrs, symlink targets, and per-entry data are bounded before
allocation. Serialized per-entry metadata is bounded to **≤64 KiB** for the
future queue, and codec/root scratch is bounded to **≤256 KiB** per admitted
operation. `Vec` in the design represents bounded per-entry data, never a
whole-tree resident collection.

### Identity inclusion and exclusion

| Participates in identity | Explicitly excluded |
| --- | --- |
| Root format, required capabilities, chunk-profile ID, complete tree-manifest ID, parent, base, publication generation, and publication ID. | Host path, `PathBuf`, physical layer/carrier ID, v1 `LayerRef`, inode number, enumeration order, mount handle, provider locator, materialization ID/generation, backend kind/format/target profile, capture timestamp, compression, blame, telemetry, and Stage 01 transcript state. |
| Complete logical path bytes, entry kind, portable metadata, symlink target bytes, sparse layout, typed segment reference, and hardlink group. | Docker whiteout encoding, opaque-directory adapter xattr, workspace upper/work paths, execution/session IDs, filesystem canonical keys, and `/eos` paths. |
| Object domain, object kind, format/version, declared length, and canonical object bytes. | Object storage location, loose/pack/index position, hydration state, cache state, and publication/mount state. |

A future `MaterializationKey` is
`(RootId, backend_kind, backend_format_version, target_profile)`. That tuple,
its locator, and materialization generation live outside `RootId`.

### Canonical wire rules

| Element | Rule |
| --- | --- |
| Record prefix | Fixed ASCII bytes `EOS-LS2\0`. |
| Record kind | One byte. The kind participates in the domain-separated record. |
| Format version | Two bytes; v2 is numeric value `2`. |
| Field lengths | Explicit, checked before arithmetic or allocation, and included in the canonical record. Oversized or inconsistent lengths reject. |
| Integer widths | Use the explicit type widths in the contract: IDs are fixed byte arrays; `u32`/`i64`/`u64` fields retain those widths; version is two bytes; record kind is one byte. No native `usize`, host word, or variable host representation is persisted. |
| Byte order | Big-endian for explicit-width signed and unsigned integers. |
| Paths and xattrs | Lexicographic unsigned-byte ordering. Paths and xattr keys are unique. No locale, Unicode normalization, case folding, or host separator normalization. |
| Tree streaming | Encode one already-canonical entry at a time to the supplied sink. Do not require a complete tree map or serialized tree in memory. |
| Digest preimage | Typed and domain-separated by domain/type/version/length. Hash the exact canonical bytes; never repair or reserialize first. |
| Decode completion | Consume the declared record exactly. Short input, inconsistent length, extra suffix/trailing bytes, or unread declared content rejects. |

`CanonicalPath` accepts invalid UTF-8 when all byte-path rules pass. It rejects
an empty path, leading `/`, trailing `/`, `//` empty components, NUL, `.`, and
`..`. Byte `\` is ordinary data and remains unchanged.

### Contract gaps that require owner reconciliation

The authoritative sources state the framing rules but do not assign every
numeric wire value needed to freeze a binary format. In particular, they do
not give:

- numeric record-kind values for root/tree/metadata/reference records beyond
  the listed `ObjectKind` discriminants;
- a complete field-tag table;
- the width of every variable-length prefix;
- concrete capability-bit assignments and optional-bit preservation rules; or
- the concrete canonical encoding/value for `ChunkProfileId`; or
- one final API name/signature for the digest/source ports: the architecture
  prose calls the digest variation point `DigestPort`, the required-shape
  example names `TypedDigest`, and no copy-ready `CanonicalSource` signature
  is shown.

Do not let the first implementation or generated golden silently become the
specification. Before freezing `contract-v2.bin`, prepare a closed wire-schema
table covering every record kind, field tag/order, length-prefix width, limit,
capability bit, and profile value. Obtain owner approval and add it to the
authoritative Stage 02 contract or an explicitly referenced versioned contract
record. Resolve the port spelling/signatures in that same approved API record;
do not add multiple synonymous ports. Until that happens, canonical goldens
and POC completion are blocked.

There is also a source tension around ordering:

- the spec requires canonical input, one-entry streaming, and decoder rejection
  of duplicate or unsorted records;
- PRC-R03 requires the canonical result to be independent of insertion order;
  and
- the E2E matrix allows either canonical equality or explicit unsorted-input
  rejection followed by a bounded sorter contract.

Reconcile this without an unbounded production sorter. Test that arbitrary
insertion order, when passed through the approved bounded/canonical preparation
seam, yields the same ordered record stream; separately test that the decoder
rejects unsorted bytes. If the owner instead requires the Stage 02 codec itself
to reorder input, stop and obtain an explicit bounded-memory design amendment
before implementation.

## 8. Validation and failure behavior

Every malformed input below must return a bounded typed error. It must produce
no ID, panic, repair, downgrade, legacy/untyped fallback, excessive allocation,
durable artifact, filesystem mutation, or other side effect.

### Path and byte validation

- [ ] Empty whole path.
- [ ] Leading `/`.
- [ ] Trailing `/`.
- [ ] Empty component such as `a//b`.
- [ ] Component `.`.
- [ ] Component `..`.
- [ ] Any NUL byte.
- [ ] Path or component over the approved bound.

Acceptance controls that must **not** be treated as malformed:

- [ ] Invalid UTF-8 that otherwise satisfies every path rule is accepted and
  preserved byte-for-byte.
- [ ] Backslash is accepted and preserved as ordinary data.

### Header, version, capability, and length validation

- [ ] Wrong or truncated `EOS-LS2\0` prefix.
- [ ] Unknown/invalid record kind.
- [ ] Unknown required format version.
- [ ] Unknown required capability bit.
- [ ] Unknown optional capability bit without an approved versioned
  preservation rule.
- [ ] Truncated kind/version/field header.
- [ ] Oversized field or record length.
- [ ] Declared length inconsistent with available bytes.
- [ ] Addition, multiplication, conversion, or offset overflow.
- [ ] Length that would allocate beyond the per-record or ≤256 KiB operation
  budget.
- [ ] Trailing bytes after an otherwise complete record.

### Ordering, uniqueness, metadata, and reference validation

- [ ] Duplicate path records.
- [ ] Unsorted path records.
- [ ] Duplicate xattr keys.
- [ ] Unsorted xattr keys.
- [ ] Invalid metadata width/value, including invalid nanoseconds.
- [ ] Sparse extent start/length overflow.
- [ ] Sparse extent beyond `logical_len`.
- [ ] Overlapping, backward, duplicate, or otherwise impossible sparse ranges.
- [ ] Dangling or wrong-kind segment/object reference.
- [ ] Inconsistent hardlink-group metadata or content reference.
- [ ] Invalid symlink, device, FIFO, or regular-file record shape.
- [ ] Identity field omitted, duplicated, reordered, or encoded at the wrong
  width.

### Source, sink, digest, and injected failure validation

- [ ] Fragmented reads at practical split points produce the same value.
- [ ] A short read before the declared end fails.
- [ ] A short write or a sink that accepts only a prefix is completed only
  through the `write_all` contract; an injected failure aborts.
- [ ] Injected source/sink I/O failure yields no partially valid value or ID.
- [ ] Digest adapter failure yields no legacy or untyped fallback digest.
- [ ] Bit flips and digest mismatches fail.
- [ ] Repeated valid and invalid operations release all test-scoped values and
  codec scratch immediately.

Error detail is a closed error kind plus format version, field class, and
bounded ordinal/index. Never include arbitrary path, xattr, payload, host path,
or unbounded error text.

## 9. File-by-file implementation map

### Product workspace and architecture

| Path | Change | Responsibility | Custody note |
| --- | --- | --- | --- |
| `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/Cargo.toml` | Modify | Add one workspace member and internal workspace dependency declaration only. | Preserve all existing Stage 00/01 edits. |
| `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/Cargo.lock` | Modify | Add the local core package stanza only. | Any external source/checksum/package change is a blocker. Merge; do not regenerate without reviewing the exact delta. |
| `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/docs/maintainer-architecture.md` | Modify | Document LayerStack → portable-core ownership, allowed ports, and forbidden reverse/provider edges. | Documentation closure; do not claim runtime authority changed. |

### New core crate

| Path | Change | Responsibility |
| --- | --- | --- |
| `crates/sandbox-runtime/layerstack-core/Cargo.toml` | Add | Package metadata/lints; no dependency tables, build script, `links`, or proc macro. |
| `crates/sandbox-runtime/layerstack-core/src/lib.rs` | Add | `#![forbid(unsafe_code)]`, cohesive public modules/re-exports; no provider façade. |
| `crates/sandbox-runtime/layerstack-core/src/error.rs` | Add | Closed bounded contract errors with no raw payload/path detail. |
| `crates/sandbox-runtime/layerstack-core/src/identity.rs` | Add | `Digest32`, nominal IDs, versions, `ObjectKind`, capabilities, and profile IDs as assigned by the approved wire table. |
| `crates/sandbox-runtime/layerstack-core/src/path.rs` | Add | Raw relative Linux byte-path validation and unsigned-byte ordering. |
| `crates/sandbox-runtime/layerstack-core/src/codec.rs` | Add | Canonical framing, source/sink, explicit widths/order, checked lengths, and exact consumption. |
| `crates/sandbox-runtime/layerstack-core/src/tree.rs` | Add | One-entry streaming logical tree, portable metadata, xattrs, sparse ranges, hardlink and typed segment references. |
| `crates/sandbox-runtime/layerstack-core/src/root.rs` | Add | `RootRecordV2`, publication identity, parent/base provenance, canonical root encoding. |
| `crates/sandbox-runtime/layerstack-core/src/port.rs` | Add | Minimal typed digest and canonical sink/source ports only. |

### Existing LayerStack adapter and product tests

| Path | Change | Responsibility | Custody note |
| --- | --- | --- | --- |
| `crates/sandbox-runtime/layerstack/Cargo.toml` | Modify | Add only the internal core dependency; retain existing `sha2` and `serde` edges. | Review direct external-edge multiset before and after. |
| `crates/sandbox-runtime/layerstack/src/model/portable.rs` | Add | LayerStack-owned typed SHA-256 adapter and serde diagnostic/v1-v2 compatibility envelope. | No v2 persistence call and no schema policy duplication. |
| `crates/sandbox-runtime/layerstack/tests/portable_root_golden.rs` | Add | Exact typed-hash goldens plus unchanged v1 compatibility checks. | Tests remain outside production `src/`. |
| `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/contract-v2.json` | Add | Human-readable immutable fixture inventory, version/domain/input/provenance/rejection metadata. | Append-only by version; never rewrite an accepted ID. |
| `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/contract-v2.bin` | Add | Exact canonical bytes after the missing wire assignments are approved. | Do not generate until the closed wire table exists. |
| `crates/sandbox-runtime/layerstack/src/stack/ops/publish.rs` | Avoid; merge only if unavoidable | Existing v1 publication compatibility. | Recorded dirty overlap. Never replace from `HEAD`; Stage 02 must not change authority. |
| `crates/sandbox-runtime/layerstack/src/storage/whiteout.rs` | Avoid; merge only if unavoidable | Existing adapter-local whiteout behavior. | Recorded dirty overlap. Whiteout encoding remains outside complete-tree identity. |

### Core product tests

| Path | Change | Responsibility |
| --- | --- | --- |
| `crates/sandbox-runtime/layerstack-core/tests/canonical_contract.rs` | Add | PRC-R01, R02, R03, R05: exact bytes, paths, ordering, round-trip, malformed input, short I/O, and exact consumption. |
| `crates/sandbox-runtime/layerstack-core/tests/host_independence.rs` | Add | Width/endian/raw-byte vectors and identity inclusion/exclusion mutation matrix. |
| `crates/sandbox-runtime/layerstack-core/tests/portable_root_tiny_loop.rs` | Add | Ignored bounded primitive/oracle used by the existing benchmark laboratory adapter. |

### External E2E harness

| Path | Change | Responsibility | Custody note |
| --- | --- | --- | --- |
| `e2e/runtime/layerstack_phase1/__init__.py` | Add if absent | Package marker. | Do not disturb existing Stage 01 marker registration. |
| `e2e/runtime/layerstack_phase1/helpers.py` | Add | Public-only revision, route, resource, storage-shape, and cleanup projections. | No private daemon route becomes the SUT. |
| `e2e/runtime/layerstack_phase1/test_portable_root_contract.py` | Add | The one typed feature-off case `runtime.layerstack-phase1.portable-root.feature-off` / PRC-01. | Preserve all existing declarations and exactly-once validation. |
| `e2e/fixtures/layerstack_phase1/portable-root-v2/expected-contract.json` | Add | Version and expected IDs for external contract evidence; no product-local path as identity. | Must match approved immutable goldens. |
| `e2e/tools/verify_external_dependency_delta.py` | Reuse | Exact external package/feature/direct-edge and std-only core verification. | Do not fork or replace the Stage 00 comparator. |
| `e2e/test-report.md` | Append only during implementation/evidence | Plan/Run/Good/Defect/Fix entries and exact cleanup custody. | Never reorder, truncate, rewrite, or erase failed attempts. |

### Benchmark

| Path | Change | Responsibility | Custody note |
| --- | --- | --- | --- |
| `benchmark/backend/benchmark_lab/planning.py` | Modify | Register the bounded portable-root operation/preset in the existing catalog. | Merge with the nine-operation Stage 01 catalog and update strict count fixtures deliberately. |
| `benchmark/backend/benchmark_lab/runner.py` | Modify | Schedule the prebuilt probe within existing sequential custody. | Do not rebuild or create another scheduler. |
| `benchmark/backend/benchmark_lab/artifacts.py` | Reuse; modify only if the authoritative Stage 02 artifact fields cannot be represented | Existing run-manifest v2, observation v5, report/export v4, evidence v1, flush/fsync, and immutable bundle contract. | Prefer existing extension points; preserve compatibility fixtures and do not fork the artifact lifecycle. |
| `benchmark/backend/benchmark_lab/resource_sampling.py` | Reuse | Existing bounded logical/physical sampling and explicit-unavailable representation. | Do not add a profiler, allocator, helper, or target-image dependency. |
| `benchmark/presets/layerstack-phase1-tiny-portable-root.yml` | Add | One warmup and ≥5 counterbalanced pairs, 30–60 s diagnostic cap, exact byte/ID/lifecycle outputs. | Run-owned output remains under `.benchmark-state`. |
| `benchmark/tests/fixtures/golden/layerstack_phase1/workspace_scratch_v1.json` and other exact-count/golden fixtures discovered by status/tests | Modify only as required | Reflect the deliberate catalog addition and artifact schema without weakening strict checks. | Merge-style editing; preserve Stage 01 `workspace_scratch`, `workspace-scratch-tiny.yml`, seed `0x5A01`, two warm-up pairs, six measured pairs, and one cancellation. |

### Documentation closure

| Path | Change | Responsibility |
| --- | --- | --- |
| `stage_02_portable_root_contract/spec.md` | Change checklist status only after evidence passes and only with authorized closure edits. | Do not mark an item complete from design intent or missing evidence. |
| `stage_02_portable_root_contract/e2e_test.md` | Normally unchanged; amend only to resolve an approved authoritative contract inconsistency. | Never rewrite evidence history through the plan. |
| `stage_02_portable_root_contract/handoff_from_stage_01.md` | Unchanged historical input. | Do not rewrite the Stage 01 handoff. |
| Stage 00/01 specifications, E2E plans, and records | Unchanged. | Reference completed work; do not reinterpret or rerun it. |

## 10. Ordered implementation sequence

Every step below has a local rollback boundary. Do not proceed on a failed
invariant, unexplained custody change, missing mandatory evidence, or
unresolved wire-format decision.

| Step | Files/components | Behavior introduced | Invariants that remain true | Smallest focused verification | Rollback boundary | Proceed only when |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Freeze custody | All three repositories; no source change | A complete branch/HEAD/upstream/status/base/owner record and Stage 02 path inventory. | No Git or runtime custody is changed; inherited Stage 00/01 work remains byte-for-byte present. | Read-only Git/status review against the handoff and repository instructions. | No edit exists. | Dirty-tree/clean-entry conflict is owner-reconciled and no unexplained mutation remains. |
| 2. Freeze dependency entry evidence | Stage 00 baselines and run-owned evidence only | Two agreeing entry captures for every frozen target/feature invocation. | Existing package/feature/edge/system inventory is untouched. | Run the existing comparator on the two entry captures; do not use counts alone. | Remove only exact run-owned temporary capture after retention rules permit. | Captures agree and every invocation ID is explicit. |
| 3. Add an empty core crate | Root `Cargo.toml`, `Cargo.lock`, core `Cargo.toml`, `lib.rs`, LayerStack manifest | One local package/member and LayerStack → core edge; unsafe forbidden. | Core has no dependencies; external graph is unchanged; no runtime code calls it. | Manifest/metadata/source audit for local stanza, zero dependency entries, acyclic direction, and no external delta. | Remove core/member/internal edge/local lock stanza. | The empty crate is demonstrably std-only and every external comparison is exact. |
| 4. Add closed errors and value primitives | `error.rs`, `identity.rs` | Fixed-size digest/nominal IDs, format version 2, object-kind discriminants, publication identity, capabilities/profile values after owner-approved wire assignments. | No SHA, serde, persistence, provider, or host type enters core. | Constructor/unit vectors for size, nonzero `PublicationId`, unknown required bits, and nominal non-interchangeability. | Revert value/error modules only. | The wire-schema table is approved for all values being encoded. |
| 5. Add portable paths | `path.rs`, `canonical_contract.rs`, `host_independence.rs` | Raw Linux byte validation and unsigned-byte ordering. | Invalid UTF-8 is preserved; backslash is data; Stage 01 filesystem paths remain separate. | PRC-R02 path matrix plus ordering vectors. | Revert path module/tests. | All valid/invalid vectors pass without panic or host normalization. |
| 6. Add canonical source/sink and bounded decoder | `codec.rs`, `port.rs`, tests | Prefix/kind/version framing, explicit widths/BE order, checked lengths, fragmented I/O, exact consumption, bounded errors. | No whole-record repair, untyped fallback, >256 KiB scratch, global owner, or side effect. | PRC-R01/R03/R05 codec-only vectors including every practical split, short read/write, overflow, trailing bytes. | Revert codec/port changes while retaining validated values. | Hostile cases fail before allocation and valid fragmentation is byte-identical. |
| 7. Add logical tree records | `tree.rs`, tests | Canonical one-entry tree encoding, metadata, xattrs, sparse extents, hardlink groups, typed segment refs. | Input is canonical/streaming; duplicates/unsorted bytes reject; no complete-tree production collection. | Entry-by-entry exact bytes, permutation-through-approved-preparation, duplicate/order, sparse, hardlink, dangling-reference vectors. | Revert tree module/vectors. | Ordering ambiguity is explicitly reconciled and all per-entry bounds are enforced. |
| 8. Add root records and identity preimages | `root.rs`, `identity.rs`, ports/tests | `RootRecordV2`, `TreeManifestId`, parent/base provenance, publication identity, identity mutation/exclusion contract. | Physical/provider/runtime fields are unrepresentable in the codec; no root is published. | PRC-R04 mutation/exclusion matrix and exact root round-trip. | Revert root additions while retaining lower-level codec if still independently valid. | Every identity field changes the expected ID input and every excluded field is absent by type. |
| 9. Add LayerStack adapters | `layerstack/src/model/portable.rs`, LayerStack manifest | Typed/domain-separated SHA-256 and serde diagnostic/v1 compatibility envelopes using existing edges. | v1 `root_hash`, publication, fsync, mount, command, and PTY behavior remain unchanged; core stays hash/serde-free. | Adapter tests with injected digest failure plus v1 fixture non-regression. | Remove adapter/module/internal use; core remains offline. | No edge relocation or runtime call writes/reads v2 state. |
| 10. Freeze immutable goldens | Core/LayerStack tests and `fixtures/cas/v2` | Approved canonical bytes, IDs, provenance, rejections, cross-width/endian/raw-byte vectors. | Accepted v1 fixtures are unchanged; v2 fixtures are append-only by format. | PRC-R01–R06 focused product tests. | Remove only the not-yet-accepted v2 fixtures and associated tests. | Exact bytes/IDs pass and the closed wire table matches every fixture byte. |
| 11. Add external feature-off proof | `e2e/runtime/layerstack_phase1`, fixture, catalog/markers as needed | One typed PRC-01 case using public APIs and outside run-owned storage accounting. | Legacy v1 is sole authority; Stage 01 declarations/layout remain intact; all candidate gauges are present and zero. | Safe catalog collection, then exact PRC-01 node with fresh-binary request. | Remove Stage 02 E2E declaration/helper/fixture only; no runtime data migration. | Catalog is coherent and no candidate path/gauge appears at setup, action, or teardown. |
| 12. Add the tiny benchmark adapter | Benchmark `planning.py`, `runner.py`, strict fixtures, preset; ignored Rust probe | Existing laboratory schedules construct/validate/encode/hash/decode/drop pairs over deterministic inputs. | One scheduler, prebuilt binary, run-owned output, ≤256 KiB scratch, no publication/CAS/SeqCDC claim. | Preset validation, then PRC-R08 run; interruption-only recovery only when applicable. | Remove Stage 02 adapter/preset and restore exact catalog count while preserving Stage 01 operation. | Strict benchmark/artifact tests pass and every pair has exact bytes/IDs and zero owners. |
| 13. Close focused evidence | All Stage 02 product/E2E/benchmark/dependency artifacts | A complete POC record and append-only execution history. | No broad/Stage 11 qualification or runtime authority claim; failed attempts remain visible. | Commands in §11, dependency comparison for every invocation, forbidden-path inspection, artifact compatibility. | Source rollback is core/edge/adapters/tests only; exact run-owned cleanup follows harness custody. | Every mandatory POC item passes; otherwise report FAIL/BLOCKED. |
| 14. Documentation and handoff | Maintainer architecture, Stage 02 checklist, append-only test report, final handoff | Accurate ownership/dependency documentation and POC verdict. | Checklist remains unchecked for missing evidence; current Git custody is explicit. | Cross-check artifacts, run IDs, SHA/digests, cleanup, and status against source and report. | Revert only unsupported closure claims, never execution history. | No mandatory evidence is absent and no contradiction is hidden. |

## 11. Test and evidence instructions

These commands are instructions for the future implementation agent. **Do not
run them during a documentation-only task.**

Before every live command, append to
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`:

- timestamp;
- product/test commits and complete dirty state;
- exact command and intended node/operation;
- image identity;
- run-owned sandbox/workspace/command/gateway/process-group scope; and
- cleanup plan.

Afterward append `Run`, `Good`, `Defect`, and `Fix/next action`, including run
ID, binary/config identity, artifacts, elapsed time, and exact cleanup result.
Never erase or rewrite a failed attempt. Every cleanup target must be an exact
ID created by that run.

### Formatting and clippy

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo fmt --all -- --check
cargo clippy --locked -p sandbox-runtime-layerstack-core -p sandbox-runtime-layerstack --all-targets --all-features -- -D warnings
```

### Core contract and LayerStack golden tests

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo test --locked -p sandbox-runtime-layerstack-core --test canonical_contract
cargo test --locked -p sandbox-runtime-layerstack-core --test host_independence
cargo test --locked -p sandbox-runtime-layerstack --test portable_root_golden
cargo test --locked -p sandbox-runtime-layerstack-core --test portable_root_tiny_loop -- --ignored --nocapture --test-threads=1
```

Do not substitute all-workspace tests for a missing focused filter.

### Stable product evidence IDs

| ID | Required evidence |
| --- | --- |
| `PRC-R01` | Exact bytes for empty/root/tree/metadata/reference records and exact decode round-trip. |
| `PRC-R02` | Valid non-UTF-8 paths are byte-preserving; leading/trailing slash, NUL, empty components, `.`, and `..` reject; backslash is unchanged. |
| `PRC-R03` | Canonical result is independent of insertion order through the approved bounded preparation seam and independent of `Read` fragmentation; unsorted decoder input rejects as specified. |
| `PRC-R04` | Every identity-bearing mutation changes the typed identity; backend, host, inode, carrier, locator, and materialization values cannot enter the codec. |
| `PRC-R05` | Hostile lengths, required bits, duplicates, unsorted keys, sparse errors, dangling references, hardlink inconsistency, and trailing bytes fail without panic or over-allocation. |
| `PRC-R06` | Existing v1 manifest bytes, `root_hash`, publication, mount, public file/command/PTY behavior, and fixtures remain unchanged. |
| `PRC-R07` | Core manifest/import/graph audit proves std-only safe Rust and exact zero external dependency delta. |
| `PRC-R08` | The typed tiny benchmark wrapper records exact encode/decode/hash/drop goldens, bounded raw samples, ≤256 KiB scratch, and zero live owners after every pair. |

PRC-01 is separate from PRC-R01–R08. PRC-01 is the packaged runtime-dormancy
proof; PRC-R01–R07 are focused product/source checks, and PRC-R08 is the typed
benchmark wrapper.

### Safe E2E catalog collection

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
PYTHONPATH=e2e \
.venv/bin/python -m harness.catalog.collect \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

If retained, collector output belongs only below
`.e2e-state/tmp/<run_id>/`. Do not use the stale README `--ledger` form.

### PRC-01 live feature-off case

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest \
  e2e/runtime/layerstack_phase1/test_portable_root_contract.py::test_PRC_01_portable_root_contract_is_runtime_dormant \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

The stable catalog ID is
`runtime.layerstack-phase1.portable-root.feature-off`, title
`PRC-01 Portable Root Contract Is Runtime-Dormant`, with exactly-once
validation `assert-prc-01-legacy-authority`.

The first focused run requests a rebuild, but a responding gateway may still
be reused; record actual gateway/binary/config custody. Use
`E2E_REBUILD_BINARY=0` only for the exact failed node after a recorded
product/test fix. Do not silently retry or rerun a passing broad suite.

PRC-01 must prove:

- one public no-op publication creates no new v1 revision;
- one public changed publication creates exactly the expected legacy v1
  revision and visible bytes;
- configured/read/write/publication authority is legacy;
- candidate completion, fallback, mismatch, workers, tasks, queues, bytes,
  permits, transactions, roots, objects, and durable bytes are present and
  zero;
- every forbidden candidate path is absent at setup, after action, and after
  teardown; and
- exact run-owned sandbox/workspace/command resources quiesce within bounded
  polling and are cleaned.

### Exact dependency comparison

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
cargo metadata --locked --all-features --format-version 1 \
  > /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/.e2e-state/tmp/<run_id>/metadata-after.json

cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.venv/bin/python e2e/tools/verify_external_dependency_delta.py \
  --baseline .e2e-state/baselines/layerstack-phase1/<invocation-id> \
  --candidate .e2e-state/tmp/<run_id>/metadata-after.json \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --require-stdlib-crate sandbox-runtime-layerstack-core \
  --require-exact-external-delta-zero
```

Resolve `<run_id>` and `<invocation-id>` to explicit run-owned values. Repeat
for every frozen target/feature invocation; never use an unvalidated glob.

### Tiny portable-root benchmark

The existing laboratory consumes a prebuilt probe and owns scheduling and
run-state paths. The expected aggregate is 30–60 seconds; every operation is
hard-capped below 60 seconds.

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark validate \
  --plan layerstack-phase1-tiny-portable-root \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
../.benchmark-state/test-venv/bin/sandbox-benchmark run \
  --plan layerstack-phase1-tiny-portable-root \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

Run recovery only after interruption; it has no `--plan`:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark
../.benchmark-state/test-venv/bin/sandbox-benchmark recover \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox \
  --product-bin-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/bin
```

The campaign uses one warmup and at least five counterbalanced alternating
control/candidate pairs. Prefer three warmups and ten pairs only if the
sub-minute aggregate cap still holds. The control verifies the frozen Stage 00
fixture; the candidate constructs, validates, stream-encodes, hashes through
the existing LayerStack SHA-256 adapter, compares the typed ID, decodes, and
drops identical logical input.

No p95, publication, fsync, CAS, SeqCDC selection, native-execution,
RSS-scale, final-space/performance, required-host, or production claim may be
made from this diagnostic.

### Artifact compatibility validation

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
.benchmark-state/test-venv/bin/python -m pytest \
  benchmark/backend/tests/compatibility/test_artifacts.py
```

### Stage 02 “do not run” boundary

Do **not** run these as Stage 02 exit evidence:

- the broad affected selector covering
  `e2e/runtime/layerstack_phase1`,
  `e2e/runtime/workspace_session`,
  `e2e/manager/management/squash`,
  `e2e/manager/management/export`,
  `e2e/observability/resource_isolation`,
  `e2e/observability/resource_efficiency`, and `e2e/compound/stress`;
- `e2e/runtime/layerstack_phase1/test_portability_matrix.py`; or
- benchmark plans `layerstack-phase1-selection`, `layerstack-phase1-rss`,
  `layerstack-phase1-space`, and `layerstack-phase1-qualification`.

Stage 11 owns those selectors and all required native-host rows. A broad pass
cannot replace a missing Stage 02 focused result.
The corresponding portable-root typed row
`runtime.layerstack-phase1.portable-root.release-matrix` is also
`planned-final` and must not execute or be reported as passed during Stage 02.

## 12. Runtime invariants and forbidden artifacts

Stage 02 writes no v2 durable state. The runtime remains legacy-only before,
during, and after PRC-01. The only permitted changes under `/eos` are normal
legacy v1 changes intentionally caused by the no-op/changed compatibility
actions and exact run-owned workspace/command scratch.

The following paths must be absent:

- `/eos/layer-stack/format-v2.json`;
- `/eos/layer-stack/roots/v2`;
- `/eos/layer-stack/manifests/v2`;
- `/eos/layer-stack/objects/v1`;
- `/eos/layer-stack/packs/v1`;
- `/eos/layer-stack/indexes/v1`;
- `/eos/layer-stack/catalogs/v1`;
- `/eos/layer-stack/journals/v1`;
- `/eos/layer-stack/staging/v2`;
- `/eos/layer-stack/leases/v1`;
- `/eos/layer-stack/retention/v1`;
- `/eos/layer-stack/maintenance/v1`;
- `/eos/layer-stack/materializations/docker-overlayfs/v1`;
- `/eos/layer-stack/quarantine/v1`; and
- `/eos/layer-stack/trash/v1`.

Check absence:

1. at Stage 02 entry, before a live case;
2. after live setup;
3. after the no-op and changed public actions;
4. after teardown/quiescence; and
5. in the final outside storage/accounting artifact.

Missing observation is not proof of absence. Use the approved outside
run-owned sampler while keeping `/eos` masked from the workload. If a forbidden
path appears, retain the evidence and report a hard failure. Do not broadly
delete it or let a successful legacy response mask it.

Because Stage 01 has completed,
`/eos/workspace/<session>/executions/<execution>/transcript.log` may exist
while its command/session owner is active, and
`/eos/namespace_execution` may contain compatibility-only residue. Those paths
are ephemeral provider-local scratch. They are not candidate artifacts and
must not influence canonical bytes or IDs.

Other runtime invariants:

- configured mode, read authority, write authority, and publication authority
  are legacy;
- candidate/shadow completion, fallback, and mismatch counts are zero;
- candidate workers, tasks, queues, bytes, permits, transactions, roots,
  objects, and durable bytes are explicitly present and zero;
- v1 no-op and changed publication semantics remain exact;
- there is no new worker, thread, task, queue, semaphore, FD, mmap, cache,
  `Arc`, global registry, service, or process owner;
- pure core values and codec scratch release immediately after the call; and
- case-owned workspace/command resources poll every 100 ms for at most 5
  seconds to explicit quiescence.

## 13. Dependency and portability proof

Use the immutable Stage 00 baselines and the shared standard-library verifier.
Counts are diagnostics only; equality is over canonical sets and multisets.

### Exact before/after comparisons

| Dimension | Required comparison and result |
| --- | --- |
| External packages | Exact sorted `(source,name,version,checksum)` set for every frozen target/feature invocation; before and after must be byte-equal. |
| External features | Exact external `(package,feature)` set; byte-equal. |
| Direct external edges | Product-wide multiset `(from,to,req,features,optional,default_features,target)`; no addition, removal, or relocation. |
| Workspace manifests | Review exact bytes/semantic delta. Only member/internal core edge changes are allowed. |
| `Cargo.lock` | Only the local core package stanza may change; no external package, checksum, version, or source stanza may change. |
| Internal graph | Record workspace membership and the single LayerStack → core edge; graph must be acyclic with no reverse/outward core edge. |
| Core manifest | No dependencies, dev-dependencies, build-dependencies, target dependencies, build script, `links`, or proc macro. |
| Non-Rust manifests/locks | Python/npm and other manifests/locks remain byte-equal unless independently authorized; Stage 02 adds none. |
| System/runtime surface | No system package/tool/command, process, socket, service, daemon, sidecar, database, FUSE component, helper, target-image package, runtime download, network, or privilege delta. |
| Source boundary | No core import/reference to `serde`, `sha2`, filesystem/provider/runtime/OverlayFS/Docker/mount/namespace/guest/WASM/operation/telemetry/test support; no unsafe code. |
| License/notice | No new external/vendored source or license/notice obligation. |

Existing LayerStack `sha2` and `serde` use is allowed only in the adapter crate
and must not be relocated into the core.

### Pinned image and portability claim

The sole Phase 1 target is:

| Fixture | OCI index | linux/amd64 manifest | linux/arm64 manifest |
| --- | --- | --- | --- |
| Ubuntu 24.04 | `sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` | `sha256:52df9b1ee71626e0088f7d400d5c6b5f7bb916f8f0c82b474289a4ece6cf3faf` | `sha256:7f622ca8766bccb22f04242ecb6f19f770b2f08827dc4b8c707de5e78a6da7ab` |

Record and verify the OCI index plus the resolved platform manifest; tag-only
evidence does not count. Stage 02 proves only:

- pure/source-contract host independence through raw-byte, width, endian,
  fragmentation, ordering, and excluded-field goldens;
- no target-image userland, helper, shell, package, network, or privilege
  dependency; and
- dormant feature-off compatibility on the selected POC environment.

The Stage 02 result is at most `designed-compatible`/POC contract evidence.
It does not qualify the macOS arm64, Ubuntu amd64, or Windows amd64 release
rows. Stage 11 runs the required-host matrix using the same pinned Ubuntu OCI
index. Cross-image portability is after Phase 1 and is not a Stage 02 or
Stage 11 acceptance/retirement gate.

## 14. Completion criteria

Do not mark the existing Stage 02 checklist complete until the matching
mandatory evidence exists.

### Mandatory POC evidence

- [ ] Custody is reconciled and implementation ran on
  `upgrade-2.0-phase-1` from the recorded newest approved immutable base.
- [ ] Stage 00 focused evidence and baselines are intact and referenced.
- [ ] Completed Stage 01 behavior and declarations are preserved but absent
  from portable identity.
- [ ] The missing wire assignments are owner-approved and versioned before
  goldens are frozen.
- [ ] PRC-R01 through PRC-R08 all pass.
- [ ] PRC-01 passes once without an unrecorded retry.
- [ ] Canonical bytes and typed IDs match immutable goldens.
- [ ] All hostile/malformed cases fail closed without panic, over-allocation,
  fallback, or side effect.
- [ ] V1 bytes, `root_hash`, publication, mount, file, command, PTY, and public
  revision behavior remain compatible.
- [ ] Every candidate gauge is present and zero.
- [ ] Every forbidden v2 path is absent at all required boundaries.
- [ ] Core values/scratch release immediately; live case resources reach
  explicit quiescence and exact cleanup.
- [ ] Core is safe, std-only, cycle-free, and source-boundary clean.
- [ ] External package/feature/direct-edge delta is exactly zero for every
  frozen invocation; system/runtime/image/helper delta is zero.
- [ ] Every focused operation is under 60 seconds and the diagnostic loop is
  within its declared 30–60 second aggregate.
- [ ] All retained artifacts and schemas validate.
- [ ] Append-only Plan/Run/Good/Defect/Fix entries include run IDs, binary
  identity, artifacts, failures, and cleanup.

### Optional unavailable measurements

Only non-gating diagnostic sources may be unavailable, and the artifact must
say `unavailable` with reason and scope. Examples include an optional
anonymous/file-backed RSS split or a diagnostic mapping/FD source on a host
that cannot provide it. Unavailable diagnostics do not become zero and do not
support a portability, memory, or performance claim.

Authority fields, candidate gauges, tree/revision assertions, forbidden-path
evidence, dependency/source audits, exact IDs/bytes, cleanup, and required
environment identity are mandatory. Their absence is a blocker.

### Hard blockers

Return `POC FAIL / BLOCKED` for any:

- wrong branch, unapproved base, unresolved custody, or unexplained mutation;
- unresolved canonical wire assignment needed by a golden;
- canonical mismatch, malformed input panic, repair, downgrade, allocation
  escape, or partial ID;
- v1 behavior/revision regression;
- candidate route, activity, durable byte, or forbidden path;
- missing authority/resource/absence evidence;
- leaked run-owned resource or cleanup outside the run;
- external dependency/feature/edge, system, service, helper, image, network,
  FFI, or runtime delta;
- unsafe/forbidden core import or dependency cycle;
- timeout, diagnostic cap breach, malformed/incomplete artifact, or unrecorded
  retry; or
- unavailable mandatory environment or evidence.

Preserve the first failure and exact cleanup result. Do not relabel a blocker
as a warning or continue to later-stage work.

### Explicitly deferred to Stage 11

Stage 02 does not claim:

- broad affected regression;
- required macOS/Ubuntu/Windows host qualification;
- `runtime.layerstack-phase1.portable-root.release-matrix`;
- cross-host required-release status;
- normative p50/p95 or throughput;
- no-op/PTY/native-I/O performance qualification;
- SeqCDC selection or StreamCDC comparison;
- full 64/256/1024 MiB × roots 1/16/64 ×3 RSS matrix;
- final physical-space/amplification/locality/pack/GC/squash gates;
- long soak, migration, rollback/forward-restore, retirement, release, or
  production status.

Missing any mandatory Stage 02 POC evidence prevents completion. Favorable
diagnostic timing or a broad test pass cannot substitute for it.

## 15. Final handoff format

The future implementation agent must provide a self-contained handoff with
this structure:

```text
Stage 02 verdict: POC PASS | POC FAIL / BLOCKED

Implementation summary
- Contract/version implemented:
- Runtime behavior intentionally unchanged:
- Reconciled source/custody decisions:

Files changed
- Product:
- Test/E2E:
- Benchmark:
- Documentation:
- Pre-existing dirty files merged without replacement:

Focused product results
- PRC-R01:
- PRC-R02:
- PRC-R03:
- PRC-R04:
- PRC-R05:
- PRC-R06:
- PRC-R07:
- Formatting/clippy:

Live and benchmark evidence
- PRC-01 stable ID and run ID:
- PRC-01 result, elapsed time, binary/config/image identity:
- PRC-R08 benchmark run ID:
- Preset validation/run/recovery result:
- Artifact compatibility result:

Dependency and portability
- Frozen invocation IDs compared:
- External package delta:
- External feature delta:
- Direct external-edge delta:
- Lockfile/internal-edge delta:
- Core manifest/import audit:
- System/runtime/service/helper/image/network delta:
- OCI index and resolved platform manifest:
- Claim limited to POC/source-contract compatibility:

Artifacts
- Golden JSON/bin paths and digests:
- E2E verdict/evidence paths and digests:
- Benchmark summary/report/export/raw paths and digests:
- Dependency comparison path and digest:
- Append-only test-report entry references:

Runtime and cleanup
- Legacy read/write/publication authority confirmed:
- V1 revision/content behavior confirmed:
- Candidate gauges present and zero:
- All forbidden v2 paths absent at setup/action/teardown:
- Stage 01 workspace-scoped transcripts preserved and excluded from identity:
- Exact run-owned cleanup result:
- Failed attempts retained:

Current Git custody
- Product branch/HEAD/upstream/status:
- Test branch/HEAD/upstream/status:
- Documentation branch/HEAD/upstream/status:
- Commit/push/stash/reset/switch/cleanup actions, if explicitly authorized:

Skipped and deferred
- Optional unavailable diagnostics:
- Checks not run and why:
- Stage 11 deferred work:
- Remaining blockers or unresolved contradictions:
```

The handoff must state legacy authority and forbidden-path absence directly;
do not infer them from a successful CLI response. It must distinguish POC
evidence from Stage 11 work and must not claim Stage 02 complete while a
mandatory row is missing.
