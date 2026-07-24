# Stage 02 completion summary and Stage 03 handoff

Prepared: 2026-07-25

Navigation: [implementation index](../index.md) | [Stage 02 specification](spec.md) | [Stage 02 E2E plan](e2e_test.md) | [D2.5 owner decision](contract_v2_owner_decision_d2_5.md) | [Stage 03 specification](../stage_03_incremental_publication/spec.md) | [Stage 03 E2E plan](../stage_03_incremental_publication/e2e_test.md)

Authoritative repositories:

- product: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
- test/E2E: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`
- documentation: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs`

## 1. Handoff status

Stage 02, Portable Root Contract, is **POC PASS**. All 15 mandatory Stage 02 completion-checklist items are checked, PRC-R01 through PRC-R08 passed, and PRC-01 passed on its first recorded attempt without a retry.

Stage 02 established a safe, standard-library-only portable identity and canonical-codec contract. It deliberately did **not** create durable v2 storage, activate a v2 root, or change publication authority. Legacy LayerStack v1 and `Manifest::root_hash` remain the sole runtime read, write, mount, revision, and publication authority.

This note transfers verified facts and reusable implementation assets. It is not an owner amendment and does not authorize Stage 03 to change the accepted v2 wire contract.

## 2. Stage 03 entry status

Stage 03 implementation remains **BLOCKED pending an owner decision**, even though Stage 02 itself is complete.

The required decision must define `RootRecordV3`, bounded `TreePage`, `FileNode`, `SegmentPage`, and `Chunk` records, including wire assignments, digest domains, field ordering, bounds, and compatibility rules. It must also freeze the Preparation 04 gates and benchmark corpus. The Stage 02 owner decision, `PRC-STAGE02-OWNER-DECISION-D2.5`, was approved at `2026-07-25T00:02:23+0800`; it freezes the v2 POC contract and a future two-slice `ChunkPayload` preimage, but it does not define or approve the v3 Merkle/page contract.

Do not freeze v3 goldens or begin canonical v3 implementation from an inferred schema. In particular, any requirement that v2 and v3 roots have identical IDs would conflict with versioned canonical identity and must return to the owner rather than being implemented silently.

## 3. Repository custody at handoff

No commit, push, stash, reset, branch switch, clean, or discard action was performed.

| Repository | Branch | HEAD | Upstream revision | Working-tree custody |
| --- | --- | --- | --- | --- |
| product | `upgrade-2.0-phase-1` | `c996aa535641a4523b164b372852bf5d2781ebbf` | `3a450d052b68daf45588328f723e50662808d266` | Unstaged inherited/concurrent edits to `AGENTS.md` and `CLAUDE.md`; run-owned generated `bin/sandbox-catalog-export` is absent with zero net change from the approved base; Stage 02 comment-only edits remain in `layerstack-core/src/tree.rs` and `layerstack/src/model/portable.rs`. No staged or untracked paths. |
| test/E2E | `upgrade-2.0-phase-1` | `6c4dbd6aec1ad053d6fdfc4c397983c513600e33` | `100d11c8f00b9774cbb7b509212d11742ae48bf5` | `e2e/test-report.md` is unstaged and contains the append-only Stage 02 command history through Iteration 147. No staged or untracked paths. |
| documentation | `layerstack_2_0` | `293434e22fb547b074d3be2831885786458c68ed` | `537938fe7c10a7607c408d2487199ac08a6dba44` | The working tree already contains an inherited/concurrent phase-plan rewrite, including modified Stage 00–02 documents, deletion of the former Stage 03–11 layout, and untracked replacement Stage 03–07 documents. This handoff note is the only new path created for this request. Preserve and merge with that dirty state; do not reconstruct dirty files from `HEAD`. |

The approved immutable Stage 02 product implementation base is:

`4d15cdfad3dd6c83e0ac51d56f932108a3a6db05`

The dependency/source-boundary comparison was frozen against that approved base, not against the upstream branch tip.

The retained Stage 02 commits are:

- product: `c996aa535641a4523b164b372852bf5d2781ebbf`
- test/E2E: `6c4dbd6aec1ad053d6fdfc4c397983c513600e33`
- documentation plan and closure: `f6e4bb628a05eb558c18c9a15fe5e139d91aa528` and `293434e22fb547b074d3be2831885786458c68ed`

## 4. What Stage 02 delivered

### 4.1 Portable core contract

The product now contains:

`crates/sandbox-runtime/layerstack-core`

The crate has `#![forbid(unsafe_code)]`, uses only the Rust standard library, and owns:

- nominal typed identities rather than interchangeable byte arrays;
- `FormatVersion`, capability bits, object kinds, entry kinds, publication identities, hardlink groups, and the frozen `SeqCdcV1` profile identifier;
- validated raw relative Linux path bytes through `CanonicalPath`;
- closed, bounded errors without arbitrary diagnostic strings;
- canonical framing, sinks, sources, and bounded decoding;
- portable metadata and logical tree-entry records;
- the `PendingTree` to `ValidatedTree` preparation boundary;
- `TreeManifestV2`, `RootRecordV2`, and object-record canonical codecs;
- typed identity preimages and digest-domain separation.

The core does not own SHA-256, serde, filesystem access, persistence, fsync, providers, Docker, mounts, namespaces, runtime operations, telemetry, async runtimes, services, FFI, or unsafe code.

### 4.2 Existing-LayerStack adapters

The existing LayerStack crate owns the host-facing adapters in:

`crates/sandbox-runtime/layerstack/src/model/portable.rs`

Those adapters provide:

- SHA-256 through `Sha256Digest`;
- compact, strict JSON diagnostics for accepted v2 roots and trees;
- preparation of backend observations into the core's sorted logical-entry contract;
- backend-only marker filtering;
- bounded diagnostic preparation statistics;
- the frozen two-slice `ChunkPayload` digest seam used by the Stage 02/Stage 03 boundary.

`prepare_tiny_portable_tree` is a Stage 02 test and diagnostic helper. It is useful as an executable example of the preparation contract, but its tiny entry bound and whole-result collection are not a Stage 03 production publication design.

### 4.3 Immutable v2 compatibility assets

The accepted Stage 02 fixtures are immutable compatibility evidence:

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/contract-v2.bin` | 1,289 bytes | `760236a658433c1d385adb7b96db1f1429d74d66b1023e6a6553f8696fb0505f` |
| `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/contract-v2.json` | 4,377 bytes | `8e3cee4013021f236630c3c3182a3f40df0b1fc1ca02c210dca28a942a7bfda8` |
| `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/portable-root-r08-v1.bin` | 61,289 bytes | `dbdca20a50da366b037a9adeecc688bdce32cd4e0840630b31babb6018055c60` |

The accepted fixture identities are:

- tree: `sha256:4d95eff452b4c165ed5bdf5c5b4ef94b54022462570605ee118da011d5a41b5f`
- root: `sha256:601c290ff8e96cdbe4a6b64a2525e9a49dba3e6935b47a311f52fa6ef8c54c53`

Stage 03 must rerun these v2 goldens unchanged. A semantic change requires a newly approved format/profile and new fixture; it must not rewrite these bytes or reinterpret their IDs.

The strict external contract projection is:

`e2e/fixtures/layerstack_phase1/portable-root-v2/expected-contract.json`

Its SHA-256 is:

`242f5a7f35579753015251a95f92fa22ea80cdbf4de9a4da2f08b83116949980`

### 4.4 Changed-path inventory

The Stage 02 product commit:

- added the workspace member, lockfile stanza, and `layerstack-core` crate;
- added LayerStack's internal dependency, portable model module, adapters, golden test, and three immutable fixtures;
- added the feature-off operation-catalog declaration and its catalog test;
- updated `docs/maintainer-architecture.md`;
- included the temporary `bin/sandbox-catalog-export` verification helper. That binary is deleted in the handed-off working tree and has zero net delta from the approved base; it is not a retained deliverable.

The Stage 02 test commit:

- added the PRC-01 external test, helpers, strict v1/v2 fixtures, and LayerStack Phase 1 package declarations;
- added the PRC-R08 adapter, preset, catalog operation, unit tests, and immutable benchmark oracle;
- extended the shared benchmark planner/runner/resource-accounting code needed by the diagnostic;
- extended the shared dependency comparator and its unit test;
- appended the complete Stage 02 execution history to `e2e/test-report.md`.

The Stage 02 documentation work updated the implementation index, Stage 02 spec and E2E plan, the D2.5 owner decision, the implementation guide, and architecture/storage-contract documentation. Current dirty Stage 03–07 planning work is concurrent custody, not part of this Stage 02 handoff edit.

## 5. Good findings and their Stage 03 value

| Verified finding | Evidence | What Stage 03 can rely on |
| --- | --- | --- |
| Canonical bytes and IDs are exact and round-trip clean. | PRC-R01 | The v2 implementation is a stable read-compatibility oracle and a concrete model for new versioned codecs. |
| Paths are raw validated Linux bytes, including invalid UTF-8, with explicit separator/component rules. | PRC-R02 | Stage 03 can preserve host-independent path identity without introducing host `Path` or Unicode normalization into the portable core. |
| Identity is stable across insertion order and fragmented reads. | PRC-R03 | Stage 03 can use streaming, sorted runs, and different read chunking without changing a logical record's identity, provided it emits the same canonical byte stream. |
| Logical mutations change identity while excluded physical/runtime details do not. | PRC-R04 | Stage 03 may evolve packing, offsets, compression, cache placement, mount state, and provider-local scratch without contaminating portable content identity. |
| Hostile lengths, tags, capabilities, ordering, and truncation fail closed without panic or unbounded allocation. | PRC-R05 | New page and chunk decoders should extend the same explicit-bound and closed-error pattern. |
| Legacy v1 bytes and public behavior remained exact while all candidate gauges stayed present and zero. | PRC-R06 and PRC-01 | Private Stage 03 construction can proceed behind the existing v1 authority boundary, with regression proof that dormant candidate code does not affect public behavior. |
| The core is safe and standard-library-only with zero external package, feature, or direct-edge delta. | PRC-R07 | Stage 03 can add portable record semantics without importing storage/runtime dependencies into the identity layer. |
| The tiny encode/decode/hash/drop loop used bounded scratch and retained zero owners. | PRC-R08 | The ports and adapter lifecycle are suitable for bounded diagnostic iteration. This is not a production performance, memory-scale, or concurrency qualification. |

The most useful architectural finding is that canonical identity and physical storage layout are now separated. Stage 03 can introduce bounded Merkle pages, chunks, private refs, and physical persistence without changing v2 logical identities or moving filesystem policy into the core.

## 6. Reusable product interfaces

### 6.1 Reuse directly

- `CanonicalPath` and its raw-byte validation rules.
- Nominal digest and publication identity types where the owner-approved v3 schema says their semantics are unchanged.
- `CanonicalSink::write_all`.
- `CanonicalSource::read_exact` and `CanonicalSource::ensure_exhausted`.
- `TypedDigest::digest(domain, version, payload_len, encode_payload)`.
- Digest-domain separation through `DigestDomain`.
- Closed bounded errors and the existing bounded decoder style.
- The dependency direction:

  `workspace/provider adapters -> layerstack -> layerstack-core`

- `Sha256Digest` in LayerStack. SHA-256 must not move into the core.
- `PendingTree`/`ValidatedTree` as the model for “prepared observations are not yet identity-bearing.”

### 6.2 Reuse as compatibility or design references

- `TreeManifestV2` and `RootRecordV2`: preserve for v2 decoding and immutable regression tests; do not expand them in place to carry Stage 03 state.
- The flat v2 `TreeManifestV2` is a compatibility and derived-export representation. Its whole-stream hash is not a proportional Stage 03 publication strategy; normal v3 publication must rewrite only bounded affected pages and ancestors.
- `ObjectRecord` and `ObjectKind::ChunkPayload`: the D2.5 decision freezes a two-slice preimage seam:

  `EOS-LS2\0 | 0x03 | 0x0002 | payload_len:u32be | first | second`

  This allows a Stage 03 chunker to hash two borrowed slices without first concatenating them. The v3 owner amendment must state whether the Stage 03 `Chunk` record reuses this exact seam or introduces a new versioned record.

- `prepare_tiny_portable_tree`: use as a behavioral example and test oracle only. Stage 03 needs bounded pages/cursors and external run/spool/fan-in handling rather than a production-wide flat collector.
- Canonical JSON adapters: diagnostic interchange only. Binary canonical bytes, not JSON, define identities.

### 6.3 Keep outside portable identity

- Stage 01 workspace transcripts and provider-local scratch.
- filesystem locations, pack offsets, compression, cache and materialization state;
- daemon/runtime counters and telemetry;
- mount, namespace, PTY, command, provider, Docker, and OverlayFS observations;
- leases and source holds unless an owner-approved record explicitly defines identity semantics for them.

## 7. Reusable test and evidence assets

### Product tests

- `crates/sandbox-runtime/layerstack-core/tests/canonical_contract.rs`
- `crates/sandbox-runtime/layerstack-core/tests/host_independence.rs`
- `crates/sandbox-runtime/layerstack-core/tests/portable_root_tiny_loop.rs`
- `crates/sandbox-runtime/layerstack/tests/portable_root_golden.rs`

These are the first regression tests to run after any Stage 03 core or adapter change.

### External proof and strict fixtures

- `e2e/runtime/layerstack_phase1/test_portable_root_contract.py`
- `e2e/fixtures/layerstack_phase1/portable-root-v2/expected-contract.json`
- `e2e/fixtures/layerstack_phase1/v1/tree.json`
- `e2e/fixtures/layerstack_phase1/v1/root.json`
- `e2e/fixtures/layerstack_phase1/v1/corpus.json`

PRC-01 stable ID:

`runtime.layerstack-phase1.portable-root.feature-off`

Successful run ID:

`20260724T181645.820036Z-96797`

The run passed 1/1 in 31.68 seconds on its first attempt. All 15 candidate gauges were present and zero, all 15 forbidden paths were observed absent at every required boundary, legacy no-op behavior stayed at count/version 1, a changed action advanced exactly to count/version 2, and the one run-owned sandbox was destroyed without cleanup failure.

Retained PRC-01 evidence:

- summary SHA-256: `c4646eb0b87f9d876077ebd1b11784c9456b6257cbeaaa44dde4638b2390c81d`
- cleanup SHA-256: `7494b60e4e20519a9fcc01479ed98a02217b71de98110365306a1175a80a9e1c`

Pinned OCI index:

`sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`

Resolved `linux/arm64/v8` manifest:

`sha256:7f622ca8766bccb22f04242ecb6f19f770b2f08827dc4b8c707de5e78a6da7ab`

Keep PRC-01 unchanged as the feature-off/v1 regression. Its Stage 02 boundary helper requires all Stage 02 candidate gauges to remain zero and checks the Stage 02 forbidden-path set. Stage 03 needs its own assertions for approved private v3 state; it must not weaken or repurpose PRC-01 to make active private publication pass.

### Dependency/source-boundary proof

- comparator: `e2e/tools/verify_external_dependency_delta.py`
- comparator unit test: `e2e/tools/test_verify_external_dependency_delta.py`
- final evidence: `.e2e-state/evidence/stage02-final-20260725T034500+0800-c996aa535/dependency-delta.json`
- evidence SHA-256: `1c77ccb2048f4c7383b0bbe6b45f5c999a88e79bcd2ef86ac2650d503e52be1d`
- frozen entry captures:
  - `.e2e-state/evidence/stage02-entry-20260724T214000+0800-61d7dbc6-f749-4215-b200-bec185c93ae5/dependency-entry-capture-a.json`
  - `.e2e-state/evidence/stage02-entry-20260724T214000+0800-61d7dbc6-f749-4215-b200-bec185c93ae5/dependency-entry-capture-b.json`
- both entry captures SHA-256: `3995bdabcc6f732883ee831189e690a60faa0cf58fe9e2a0be95870278a2b945`

The comparison covered all 16 frozen invocations. Before and after counts were 1,143 external packages, 2,179 package-feature pairs, and 116 direct external edges. Every external difference set was empty, and the standard-library/source-boundary audit passed.

This is Stage 02 provenance, not Stage 03 exit proof. Stage 03 must freeze two agreeing captures from its actual entry base, extend the comparator's frozen invocation list when it adds focused invocations, and compare its own exit. It should not replace the shared comparator with an ad hoc dependency check.

### Diagnostic benchmark

- adapter: `benchmark/backend/benchmark_lab/portable_root.py`
- preset: `benchmark/presets/layerstack-phase1-tiny-portable-root.yml`
- catalog operation: `portable_root_tiny_loop`
- oracle: `benchmark/tests/fixtures/golden/layerstack_phase1/portable_root_v1.json`
- unit tests: `benchmark/backend/tests/unit/test_portable_root.py` and `test_portable_root_golden.py`

Successful run ID:

`019f9583-82ff-717e-8247-c1162b0d536e`

The aggregate ran for 35.609327582 seconds, completed 2,292 iterations and 140,474,388 bytes, used 31,496 peak scratch bytes, and reported zero errors and zero retained owners.

One earlier attempt, `019f956a-3d46-77de-8115-98232c99d4bd`, failed during pretrial gateway preparation. Its evidence is preserved. The successful run used the documented offline correction; no interruption or interruption-recovery claim was made.

Retained successful-run SHA-256 values:

- manifest: `d9366bbefb84658e7a1b052bcf853523b2ab845debb051515a77f148f7b8526f`
- summary: `1b7afbcf0cf7aa6b2d4548738633bd2babaaed3bf0192e866d63e5e0fc224a98`
- report: `03cb754eb2e00282282e262a24a2ffad79d6582c168c40ef51833cf958f4092c`
- export: `c9a708a6847b19b2fcbce669b2a98327e2a2b55f0c31e8824747e5d9ca95b274`
- events: `f039fe3bd2a707885503e76dcc73469a0b79dfe27b66ae20635cb010c6dba329`
- observations: `ba758de52c2621cb3f9979c07b1476c618f047df5e61e4d62de89269bf785eee`

The failed attempt remains retained with summary SHA-256 `30ac548e633d7ba7cfd6a9d816ab28fd1555cc9c2f21413ad2df0dd206c5aa25`. Both run IDs are absent from their exact transient `.benchmark-state/runs`, `.benchmark-state/runtime`, and `.benchmark-state/tmp` ownership locations; immutable result bundles remain retained.

## 8. Stage 03 integration guardrails

Stage 03 should:

1. obtain and record the owner-approved v3 amendment before freezing any new canonical golden;
2. add v3 records side-by-side with v2 decoding and immutable v2 goldens;
3. keep canonical values/codecs in `layerstack-core` and storage, hashing, serde, fsync, failpoints, and runtime authority in LayerStack;
4. use bounded pages, cursors, spools, and fan-in rather than loading an unbounded tree or file into core memory;
5. keep new refs and publication state private while v1 remains the public authority;
6. preserve the raw Linux path contract and keep workspace transcripts outside portable identity;
7. add exact v3 root/tree/file/segment/chunk goldens, cross-host identity checks, hostile decoder cases, and publication/recovery/OCC/source-hold evidence required by the Stage 03 E2E plan;
8. rerun all accepted v2 compatibility tests and the shared dependency/source audit.

Under the current specification, Stage 03 may create only `.storage-writer.lock`, top-level `CONTROL`, deterministic loose logical objects, private heads/checkpoints/pins, publication operations with bounded work, and migration/source leases only when an imported payload location actually requires them. It must not precreate empty future pack, locator-run, materialization, GC, or authority-migration structures.

Stage 03 must not:

- mutate v2 tags, field ordering, numeric assignments, bytes, fixtures, or identity meanings;
- make `RootRecordV2` carry v3 page, chunk, ref, lease, or publication state;
- call tiny-loop or benchmark helpers from production runtime paths;
- treat diagnostic JSON as the canonical identity format;
- introduce SHA, serde, filesystem persistence, async runtimes, services, FFI, or unsafe code into `layerstack-core`;
- make Stage 01 scratch or transcripts part of portable identity;
- activate candidate roots, alter `Manifest::root_hash`, or weaken v1 publication authority before the stage that explicitly owns that transition;
- scan or hash a complete flat manifest during normal proportional publication;
- create speculative empty storage directories merely to reserve names.

## 9. Recommended Stage 03 start sequence

1. Freeze product, test, and documentation custody from the exact dirty trees. Preserve this note, the append-only report, and the concurrent documentation rewrite.
2. Reconcile the current Stage 03 spec with an owner-approved v3 amendment covering record kinds, format/profile versions, field ordering, bounds, identity preimages, decoder compatibility, and private storage/ref names.
3. Rerun the four focused Stage 02 product suites and verify the three immutable artifact digests before editing shared codecs or adapters.
4. Add v3 nominal values and bounded codecs beside the v2 code. Do not alter accepted v2 encoders or decoders.
5. Implement streaming SeqCDC and the two-slice hash path in LayerStack, using core only for approved portable values and canonical bytes.
6. Add bounded tree, file, and segment pages and private persistence with exact durability and recovery ordering from the Stage 03 decision.
7. Add private idempotent publication, OCC/rebase, source holds, and failpoint recovery while retaining v1 public authority.
8. Run the Stage 03 focused E2E and benchmark gates, then rerun v2 goldens and the dependency/source-boundary comparator.
9. Record every live command and failed attempt append-only, validate retained artifacts, clean only exact run-owned resources, and hand off the final custody state.

## 10. Stage 02 evidence summary

| Requirement | Result |
| --- | --- |
| PRC-R01 canonical bytes and round trip | PASS |
| PRC-R02 raw portable paths | PASS |
| PRC-R03 ordering/read-fragmentation determinism | PASS |
| PRC-R04 mutation and exclusion matrix | PASS |
| PRC-R05 hostile bounded decoding | PASS |
| PRC-R06 unchanged v1 behavior | PASS |
| PRC-R07 safe std-only core and zero external delta | PASS |
| PRC-R08 bounded tiny diagnostic | PASS |
| PRC-01 feature-off live proof | PASS, first recorded attempt |
| artifact compatibility | PASS, 11/11 |
| safe E2E catalog collection | PASS, 643 cases |
| focused operation duration | PASS, every focused operation under 60 seconds |
| benchmark aggregate duration | PASS, within the required 30–60 second window |
| completion checklist | PASS, 15/15 mandatory items checked |

The focused final product results were:

- `cargo fmt --all -- --check`: 1.552 seconds;
- exact core and LayerStack all-target/all-feature clippy: 3.716 seconds;
- `canonical_contract`: 7 passed in 2.746 seconds;
- `host_independence`: 2 passed in 0.933 seconds;
- `portable_root_golden`: 2 passed and 1 intentionally ignored in 2.407 seconds;
- ignored `portable_root_tiny_loop`: 1 passed in 0.972 seconds, 256 iterations, 329,984 bytes, 1,334 peak scratch bytes, zero retained owners.

The complete append-only execution history, including failed attempts and corrections, is in:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`

## 11. Non-authority, cleanup, and deferred qualification

Stage 02 wrote no durable v2 candidate bytes and added no v2 storage directory. At entry, setup, after public actions, teardown/quiescence, and final outside accounting, all 15 forbidden candidate paths were absent.

The exact Stage 02 forbidden paths were:

- `/eos/layer-stack/format-v2.json`
- `/eos/layer-stack/roots/v2`
- `/eos/layer-stack/manifests/v2`
- `/eos/layer-stack/objects/v1`
- `/eos/layer-stack/packs/v1`
- `/eos/layer-stack/indexes/v1`
- `/eos/layer-stack/catalogs/v1`
- `/eos/layer-stack/journals/v1`
- `/eos/layer-stack/staging/v2`
- `/eos/layer-stack/leases/v1`
- `/eos/layer-stack/retention/v1`
- `/eos/layer-stack/maintenance/v1`
- `/eos/layer-stack/materializations/docker-overlayfs/v1`
- `/eos/layer-stack/quarantine/v1`
- `/eos/layer-stack/trash/v1`

Cleanup is complete: the PRC-01 run-owned sandbox was destroyed with no cleanup failure, both benchmark run IDs are absent from every exact transient ownership directory, immutable evidence remains retained, and the temporary product exporter is absent.

The resulting runtime storage structure is therefore still the legacy v1 structure. “Legacy” means the currently authoritative, compatibility-preserved LayerStack format—not abandoned data and not a directory that Stage 03 may delete. Stage 03 may add an owner-approved private storage structure for its candidate pipeline, but it must coexist with v1 and remain non-authoritative until a later stage explicitly changes authority.

This separation is what makes Stage 02 a useful foundation: the canonical logical contract is frozen and independently testable, while physical storage, chunking, packing, leases, recovery, and concurrent publication remain free to evolve behind a versioned boundary. Stage 02 did not claim to prove Stage 03 concurrency, durability, recovery, memory scale, or production performance; those remain Stage 03 and later-stage evidence obligations.

Stage 02 did not run or claim the broad portability matrix, RSS/space/performance suites, soak, migration, release matrix, or production qualification. The original plan called that future qualification “Stage 11”; the active condensed plan renumbers the final qualification/default/retirement gate as Stage 07. That planning rename does not alter any Stage 02 result, and neither form of the future qualification gate is claimed here.
