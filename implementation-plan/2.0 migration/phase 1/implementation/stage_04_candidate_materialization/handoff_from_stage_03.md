# Stage 04 incoming handoff from Stage 03

Status: **READY FOR STAGE 04 ENTRY**  
Upstream verdict: **Stage 03 POC PASS**  
Prepared: `2026-07-25`

This is the Stage 04-owned entry note. The immutable, evidence-complete outgoing
record remains
[`../stage_03_incremental_publication/handoff_to_stage_04.md`](../stage_03_incremental_publication/handoff_to_stage_04.md),
SHA-256
`471fc5b65a167755b5620f43429e6efc59794fb250f074789c19cf7ef4bf9954`.
If this note and that record disagree, stop and reconcile against the outgoing
record, the owner decision, and retained artifacts before changing product code.

## 1. What Stage 03 delivered

Stage 03 implemented and verified the private “corrected identity and complete
private publication” slice:

- owner-approved bounded v3 records, typed identities, immutable golden corpus,
  and hostile decoding while preserving v2 read/import compatibility;
- deterministic SeqCDC, typed loose objects, raw-byte capture, bounded external
  ordering, persistent content and attribution pages, and copy-on-write sharing;
- atomic private heads/checkpoints/pins, branch-scoped durable operations,
  exact retry/expiry, F01–F09 recovery, and short publication commit sections;
- semantic OCC with bounded rebase and typed conflict;
- checkpoint/fork/pin/checkout/revert/reset/delete behavior;
- conditional protection for a last v1 carrier;
- hidden candidate validation through the normal publication protocol while
  public authority and public bytes remain v1;
- bounded ownership/resource observations and terminal PTY output-drain
  synchronization; and
- a strict Stage 03 benchmark/E2E adapter with machine-verifiable evidence and
  exact cleanup accounting.

The main product seams Stage 04 inherits are:

| Seam | Current source |
| --- | --- |
| v3 typed record/identity contract | `crates/sandbox-runtime/layerstack-core/src/v3.rs` |
| private object, page, ref, operation, OCC, source-hold and publication implementation | `crates/sandbox-runtime/layerstack/src/stack/candidate/` |
| normal-protocol hidden publication integration | `crates/sandbox-runtime/operation/src/layerstack/service/hidden_validation.rs` and `impls/publish_changes.rs` |
| raw workspace capture boundary | `crates/sandbox-runtime/workspace/src/overlay/capture.rs` |
| terminal response/output ordering | `crates/sandbox-runtime/namespace-execution/src/pty.rs` |
| Stage 03 benchmark adapter | `benchmark/backend/benchmark_lab/stage03_publication.py` in the test repository |

These are shared-custody, uncommitted changes. They are not a clean upstream
baseline and must not be reset, stashed, restored, or silently rewritten.

## 2. Evidence inherited at entry

| Evidence | Result |
| --- | --- |
| Stage 03 typed E2E catalog | 34/34 PASS in 77.56 seconds |
| final canonical campaign | run `019f977b-752d-7868-927d-170b8d46a078`; overall/correctness PASS; zero failures and warnings |
| focused runner/compatibility/dispatch | 22/22 PASS |
| final artifact compatibility | 22/22 PASS |
| product candidate-publication suite | 28/28 non-ignored PASS |
| workspace publication/security | 18/18 and 1/1 PASS |
| namespace execution | 68 non-ignored PASS |
| dependency/portability closure | zero external dependency delta; safe/std-only portable core PASS |
| cleanup | no Stage 03-owned container, benchmark runtime, process, listener, or generated binary remains |

Authoritative details:

- [Stage 03 implementation guide](../stage_03_incremental_publication/implementation_instructions.md),
  external SHA-256
  `2ea6c4e64416cd1327d18656b811f135c90ce3144d77ffaba73caeb6d472f435`;
- [Stage 03 benchmark note](../stage_03_incremental_publication/benchmark_note.md),
  SHA-256
  `8b775f3ed998132a72b451034b8d8e529fd427cfbfcd7bedd8a06bd84219778f`;
- [dependency and portability audit](../stage_03_incremental_publication/stage03_dependency_portability_audit_20260725.md),
  SHA-256
  `a475ad7a23999ee4a231c08d40677186498bddcaf5b44d4e2fbf8683eaa386f7`;
- append-only test report
  `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`,
  external SHA-256
  `084873fd5d118e8edf69c34e743fba8bcab554a2701617a29d41604a1a5200a1`;
- product Stage 03 source-diff SHA-256
  `d5323b27f1dd7b9e19cf53551162e5608624597b1a9b6aaa9f9dcf1d6b8c8823`;
  and
- test/benchmark final-campaign source-diff SHA-256
  `95adf9fddf75d715a464d095cc7e9192d240d3eaa00597b822795e5756c2ba38`.

The final result bundle remains under
`.benchmark-state/results/019f977b-752d-7868-927d-170b8d46a078/` in the test
repository. The generated catalog export, gateway, and Linux daemon used by the
campaign were deliberately removed after evidence retention; Stage 04 must
rebuild its own exact revision rather than assuming those binaries still exist.

## 3. Repository custody

| Repository | Branch | Preserved baseline/custody |
| --- | --- | --- |
| product | `upgrade-2.0-phase-1` | baseline `cbe45de873cd24fbf48bb7b3a6c5f9f98980313c`; preserve all modified/new Stage 03 paths |
| test + benchmark | `upgrade-2.0-phase-1` | baseline `173191e8694515af43797128070dbdfd2d246040`; preserve runner, schema, fixture, E2E, and append-only report paths |
| docs | `layerstack_2_0` | shared Stage 02/03 decision, guide, evidence, benchmark, audit, and handoff history |

Before Stage 04 mutation, capture complete `git status`, branch/upstream, relevant
diff identities, ignored state needed for execution, live processes/listeners,
containers, and runtime directories. Reconcile any drift rather than cleaning it.

Three unrelated PPID-1 gateways were present at Stage 03 closure on ports 7878,
17878, and 17978. They were not Stage 03-owned and were not touched. Re-inventory
instead of assuming their continued presence or ownership.

## 4. Stage 04 watch-outs

1. **Authority does not move.** `legacy_v1` remains the sole public authority
   through Stage 04. Strict candidate activation is explicit and must never
   silently fall back to v1; Stage 06 owns authority cutover.
2. **Identity bytes are frozen.** Do not change v2/v3 framing, domains, record
   bounds, or golden vectors. Backend kind, format version, target profile,
   host paths, image tags, credentials, and materialization generations are
   physical selection inputs, never logical `RootId` inputs.
3. **Consume the typed graph.** Materialization must stream verified v3
   content/attribution objects. The diagnostic flat export is not an input and
   complete-tree/history collection is forbidden on normal publication or warm
   routes.
4. **Keep cold work outside visibility locks.** Reconstruction, native writes,
   sync, manifest creation, and verification occur as private operation work.
   The writer lock is only for the brief fenced GC registration and atomic
   `CURRENT` transition.
5. **Cold and warm paths remain distinct.** Missing/corrupt/unsupported
   materialization fails closed. A command/file/PTY request may not hide CDC,
   object traversal, hashing, locator merge, packing, GC, squash, or a cold
   build.
6. **Lease the exact generation.** An admitted session remains on its exact
   `{materialization-id,generation,fence}` despite later head or `CURRENT`
   changes. Shared immutable carriers never imply shared uppers, work dirs,
   executions, mount ownership, or unpublished writes.
7. **Preserve last-location safety.** Honor Stage 03 source holds, ref leases,
   and GC barriers. Do not delete a current, leased, pinned, or last verified
   native generation. Uncertainty retains data.
8. **Respect stage ownership.** Stage 04 may create only its actual
   `materializations/` and operation-work paths. General packs, locator
   compaction, GC, squash, destructive retention, authority cutover, and
   retirement remain owned by Stages 05–07.
9. **Preserve terminal semantics.** Do not regress the PTY drain handshake:
   terminal success must not become observable before buffered output reaches
   EOF/drain or an explicit completion error is returned.
10. **Prove Linux capabilities, not host folklore.** Native activation is a
    Linux backend claim. Record guest kernel, filesystem, mount/backend
    capabilities, architecture, and image digest. The observed macOS
    package-wide Stage 05 squash/flatten guard is not a Stage 04 regression and
    must not be weakened.
11. **Keep resource ownership explicit.** Every build worker, waiter, buffer,
    queue, FD, mapping, permit, session, lease, mount, upper, work dir, and
    temporary path needs a bounded owner and joined/recoverable teardown.
12. **Do not promote POC evidence into qualification.** Stage 03 performance is
    `NOT_RUN/INSUFFICIENT_SAMPLE`. The transferred Stage 07 matrix remains
    `OPEN`; see
    [`../stage_07_qualification_retirement/spec.md`](../stage_07_qualification_retirement/spec.md).

## 5. Stage 04 entry checklist

- [ ] Read this note, the Stage 03 outgoing handoff, owner decision/corpus,
  Stage 04 spec/E2E/benchmark note, storage contract, and Preparation 04
  completely.
- [ ] Re-capture shared-worktree custody and verify the Stage 03 diff identities
  or document exact drift before mutation.
- [ ] Add the Stage 04 plan to the append-only E2E report before each test,
  benchmark, or live diagnostic.
- [ ] Define Stage 04-owned tracker rows, artifact schemas, exact cleanup
  ownership, and failpoint/recovery cases before implementation.
- [ ] Rebuild only the exact required product binaries and pin every runtime
  image by immutable digest.
- [ ] Re-run the narrow inherited Stage 03 compatibility/public-authority
  regressions before and after Stage 04 integration.
- [ ] Implement and verify cold reconstruction before strict activation, then
  lifecycle/concurrency/recovery, then the complete Stage 04 E2E and benchmark
  matrix.
- [ ] Capture entry/exit dependency graphs and prove no unapproved helper,
  service, network, image, unsafe/FFI, or portable-core delta.
- [ ] Remove only Stage 04-owned generated/runtime resources after retaining
  immutable evidence.
- [ ] Produce a Stage 04 outgoing handoff that preserves every open Stage 07
  transfer item rather than marking it passed from design or Stage 03 POC
  evidence.

## 6. Entry verdict

Stage 04 is unblocked by Stage 03. Start only after the fresh custody capture and
entry checks above. No Stage 04 implementation or benchmark result is implied by
this note.
