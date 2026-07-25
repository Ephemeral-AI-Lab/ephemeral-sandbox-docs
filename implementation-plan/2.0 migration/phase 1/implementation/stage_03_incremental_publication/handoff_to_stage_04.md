# Stage 03 handoff to Stage 04

Verdict: **POC PASS**  
Closed at: `2026-07-25T04:27:25Z`

## Authority and boundary

Stage 03 implemented and verified the authorized “corrected identity and
complete private publication” vertical slice under owner decision
`PRC-STAGE03-OWNER-DECISION-G01.1`.

- Decision:
  [`contract_v3_owner_decision_g01_1.md`](contract_v3_owner_decision_g01_1.md),
  SHA-256
  `27264ef96f97960757eeba0b51bb7d2560446466cbf8e6a11c99a881da834e16`.
- Approval mapping:
  [`gate_resolution_approval_20260725_04.md`](gate_resolution_approval_20260725_04.md),
  SHA-256
  `49ea0a740462ce2652d5a4c4f21f595a44a56af25c0b7222dff3149a63a5f849`.
- Frozen v3 corpus:
  [`stage03_v3_owner_corpus_v1.json`](stage03_v3_owner_corpus_v1.json),
  SHA-256
  `7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be`.

The public authority remains `legacy_v1`. Stage 03 did not authorize or
implement Stage 04 materialization/activation, Stage 05 packs/squash, Stage
06 cutover, or Stage 07 retirement/qualification. D2.5 remains immutable and
v2-only.

## Repository custody

All work remains uncommitted in the shared worktrees and must be preserved:

| Area | Branch | Baseline/upstream | Stage 03 custody |
| --- | --- | --- | --- |
| product | `upgrade-2.0-phase-1` | `cbe45de873cd24fbf48bb7b3a6c5f9f98980313c` | recorded modified/new Stage 03 source and tests; source-diff SHA-256 `d5323b27f1dd7b9e19cf53551162e5608624597b1a9b6aaa9f9dcf1d6b8c8823` |
| test + benchmark | `upgrade-2.0-phase-1` | `173191e8694515af43797128070dbdfd2d246040` | recorded modified/new runner, schema, fixture, E2E, and append-only report paths; final campaign source-diff SHA-256 `95adf9fddf75d715a464d095cc7e9192d240d3eaa00597b822795e5756c2ba38` |
| docs | `layerstack_2_0` | HEAD `901d6d2181d0795eaaf174a23636a38019aab9a1`; upstream `426b6be3284c26a59eb77d39ad6622997e8479c9` | Stage 03 decision, corpus, gate, entry, audit, guide, benchmark note, and this handoff; preserve all unrelated/pre-existing work |

Do not reset, stash, clean, restore, switch branches, or fold these paths into
another owner’s change without reconciling current custody.

## Implemented Stage 03 slice

The product delta provides:

- owner-approved bounded v3 codecs and typed identities alongside immutable v2
  read/import compatibility;
- deterministic scalar SeqCDC and typed loose-object put-if-absent;
- bounded raw-byte capture, external ordering/deduplication, persistent
  content/attribution pages, copy-on-write structural sharing, and
  diagnostic-only flat export;
- atomic private heads/checkpoints/pins and short publication commit sections;
- branch-scoped durable operation identity, exact retry/mismatch/expiry,
  F01–F09 recovery, and head/terminal repair;
- semantic changed-path OCC with typed conflict and bounded two-/three-writer
  disjoint progress;
- clean/dirty checkpoint, fork/pin, checkout, revert, reset, and ref deletion;
- conditional last-v1-carrier source protection;
- hidden candidate validation through the normal publication protocol while
  retaining v1 public bytes and authority;
- bounded observation/resource accounting; and
- terminal PTY output-drain synchronization so a successful command response
  cannot omit buffered terminal output.

The test/benchmark delta provides the complete 34-case typed Stage 03 catalog,
strict machine evidence, final-source identity capture, bounded runner-owned
ABBA execution, private probe evidence, exact cleanup accounting, and
positive/negative artifact validation.

## Verification

### Product

- `cargo fmt --all -- --check`: PASS.
- portable core: 15 non-ignored tests PASS; one benchmark remains ignored.
- Stage 03 `candidate_publication`: 28 non-ignored tests PASS.
- workspace unit suite: 34/34 PASS.
- `workspace_session_publish`: 18/18 PASS.
- publication security: 1/1 PASS.
- namespace-execution: 68 non-ignored tests PASS.
- all focused v3 codec, object store, SeqCDC/capture, tree, refs, recovery,
  OCC, source-hold, hidden-validation, PTY-drain, and compatibility
  regressions PASS.

A package-wide LayerStack unit invocation also executed unrelated Stage 05
squash/flatten tests on macOS: 86 tests passed and 26 reported the existing
explicit `"layer squash flattening is supported only on Linux"` guard. Those
Stage 05 platform cases are preserved as observed history; the Stage 03
candidate target in the same package passed 28/28 and Stage 03 did not modify
or weaken the later-stage guard.

### E2E and benchmark harness

- complete Stage 03 typed E2E module: 34/34 PASS in 77.56 seconds, covering
  I01–I05, P01–P05, R01–R06, O01–O03, F01–F09, S01–S02, and B01–B04;
- focused Stage 03 Python runner/compatibility/dispatch surface: 22/22 PASS;
- strict canonical plan validation: PASS;
- complete artifact compatibility module after the final campaign: 22/22
  PASS; and
- all 34 E2E cases destroyed their exact sandboxes and retired their
  case-owned runtime resources.

The authoritative chronological record, including every failed attempt and
fix, is
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`,
the Stage 03 append-only report through terminal closure.

## Final canonical campaign

| Field | Evidence |
| --- | --- |
| run | `019f977b-752d-7868-927d-170b8d46a078` |
| plan/cell | plan SHA-256 `5511812675ab2f6784b39b701a333200391e51d6e87e870906d0c454d308d8d6`; cell `sha256:e71292adeb408b5c8629e6ea9a32aa133cf1be8d427f9eb74dabd07e6b7ac371` |
| duration | 137.27 seconds runner elapsed; 136.568017333-second measured boundary; 180-second deadline PASS |
| state | completed; zero failures; zero warnings; report ready |
| verdict | overall `PASS`; correctness `PASS`; performance `NOT_RUN/INSUFFICIENT_SAMPLE` |
| strict evidence | `operation-evidence-e8d7426a22ae22680f0c1597d8dcbfd5d9814539e33aa85287efe23be44ff334.json`; SHA-256 `e8d7426a22ae22680f0c1597d8dcbfd5d9814539e33aa85287efe23be44ff334` |
| report/summary | report SHA-256 `fd919bddc80e50f5c45a26b5b22b476b14aea77e9346df9c76c27ffeffd2ae53`; summary SHA-256 `728d3c0d805ccfdc7146e9c3482838adad8b394c23e79702dc1d2c8009a7b464` |
| cleanup/result boundary | SHA-256 `7cf3607f4a9fb329651ef577393507130c74ba6103cb9a32aa8e1a26069d2059` / `f5657907f7c00f6bce6970a7c798c450c929866c31584b7ae13cb3623d86a7e5` |

The strict evidence reports zero public mismatches, route failures, fallback,
active owned resources after quiescence, detached tasks, strong cycles, and
unexplained residue. Both ABBA public pairs match. The private probe retains
16 valid samples and passes checkpoint, OCC, F01–F09 recovery, retry, and
cleanup assertions. All four arms report sandbox destruction, session
retirement, and gateway closure.

The complete result bundle is retained under
`.benchmark-state/results/019f977b-752d-7868-927d-170b8d46a078/` in the
test repository.

See [`benchmark_note.md`](benchmark_note.md), SHA-256
`8b775f3ed998132a72b451034b8d8e529fd427cfbfcd7bedd8a06bd84219778f`,
for samples, counters, unavailable fields, and the exact command.

## Dependency, portability, and layout

All six entry/earlier-exit/final dependency captures were byte-identical at
SHA-256
`1c77ccb2048f4c7383b0bbe6b45f5c999a88e79bcd2ef86ac2650d503e52be1d`:
16 invocations, 1,143 external packages, 2,179 feature pairs, 116 direct
edges, exact zero external delta, and a passing safe/std-only portable-core
audit.

The product/test source audit found no new production helper, service,
sidecar, network/download path, unsafe/FFI surface, or mutable image
resolution. The pinned local arm64 image remained
`ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`.

See
[`stage03_dependency_portability_audit_20260725.md`](stage03_dependency_portability_audit_20260725.md),
SHA-256
`a475ad7a23999ee4a231c08d40677186498bddcaf5b44d4e2fbf8683eaa386f7`.

The typed B02/B03/B04 evidence covers the complete Stage 03 `/eos`
allowed/conditional/forbidden map, public masking, normal capture exclusion,
failure/restart/ref-deletion boundaries, and settled teardown. Future-stage
directories remain absent until their owning stage uses them.

## Cleanup and retained history

Final exact cleanup removed only:

- `bin/sandbox-catalog-export`, SHA-256
  `da35db6e607efc3386af1452e3d647e189e6e994707af3c1e2586bab856a9c41`;
- `bin/sandbox-gateway`, SHA-256
  `cc341e827bf4a49651ebdf5c5ab544388e03cbe2a44e6a0f97400ab67cee7e22`;
- `dist/sandbox-daemon-linux-arm64`, SHA-256
  `eaa9b10d8044977ebb820051e88dff27ab78ec8501890c74b8ba9a17134113fd`;
  and
- the three exact temporary dependency comparator directories, after their
  identities were retained in the portability audit.

The immutable final result bundle, fixture, cleanup ledger, result boundary,
source changes, and ordinary Cargo target cache/private probe remain. No
Stage 03 container, benchmark runtime entry, process, or listener remains.
The three pre-existing unrelated PPID-1 gateways on ports 7878, 17878, and
17978 were not touched.

## Stage 04 entry

Stage 04 may consume the private v3 content/attribution roots and refs through
the approved interfaces, but must:

1. preserve all v2 and v3 identity bytes and typed domains;
2. preserve `legacy_v1` as sole public authority until Stage 06;
3. keep expensive materialization/activation work outside private publication
   commit sections;
4. neither reinterpret diagnostic flat exports nor scan complete
   trees/history as a normal publication input;
5. honor fenced source-protection leases and GC barriers;
6. add only Stage 04-owned `/eos` paths at their first actual use; and
7. retain its own direct dependency, resource, layout, restart, cleanup, and
   compatibility evidence.

Full performance selection, multi-host/filesystem qualification, later-stage
destructive-retention survival, and public cutover remain
`DEFERRED_STAGE_07`.

There is no open mandatory Stage 03 blocker.
