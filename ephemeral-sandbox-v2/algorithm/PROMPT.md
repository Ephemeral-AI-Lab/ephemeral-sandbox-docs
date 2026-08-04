# Agent prompt — specify the selected LayerStack-0 algorithms

Use this prompt in a new agent session to write the algorithm documentation
for the **selected Phase 01 R0 architecture**. This is design documentation,
not product implementation.

The Phase 01 decision is already made:

```text
WINNER: R0 — LayerStack-0 rewrite-in-place filesystem-native complete-Version storage
```

Do not run another architecture tournament. Do not replace R0 with CAS+CDC,
a manifest/Chunk DAG, a layer chain, reflink-backed truth, a database, a new
service, or a backend-neutral storage framework. If source evidence shows that
R0 cannot satisfy a hard rule, report `REOPEN_PHASE_01` with the exact failure;
do not silently design a different system.

Write only under:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/algorithm
```

Do not edit V2 product code, the pinned product worktree, live state, migration
data, or files outside that folder.

## 1. Required first-screen result

The generated `algorithm/README.md` must begin with exactly one result:

```text
ALGORITHM_PACKAGE: ALIGNED_WITH_R0
```

or:

```text
ALGORITHM_PACKAGE: REOPEN_PHASE_01 — <specific architecture-changing failure>
```

`ALIGNED_WITH_R0` means the algorithms compose coherently within the selected
architecture. It does not mean implemented, benchmarked, or production-ready.

## 2. Authority and required reading

Read these documents in order before writing:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/README.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/PRD.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/PLAN.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/architecture_design.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/branding/terminology.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/README.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/01-ownership-and-boundaries.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/02-state-identity.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/03-state-store.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/04-algorithms-and-call-flows.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/05-concurrency-durability-recovery.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/06-resources-security-observability.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/07-performance-and-optimization.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/08-migration-and-cutover.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/09-source-and-implementation-map.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/design/10-verification-matrix.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/00-freeze-rules/SPEC.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/01-choose-design/SPEC.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/02-state-identity/PRD.md
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/ephemeral-sandbox-v2/phases/03-state-store/PRD.md
```

The product PRD and its hard rules outrank all later prose. Phase 00 is measured
e497 evidence. Phase 01 `SPEC.md` is the selection input; the root
`architecture_design.md` and accepted ADRs record the output. The
`implementation-plan/` tree is historical/evidence-only.

## 3. Product-source seal

The product tree is read-only:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
expected branch: codex/new-2.0-storage-core
recorded HEAD:   e4974d1f9aac702b35e052629cb070c897989352
```

Before any command there, read `AGENTS.md` and `CLAUDE.md`, then run the seal
commands required by Phase 01. Do not switch, edit, commit, reset, or clean the
tree. If it does not match the recorded clean base, mark source-placeability
claims `OPEN: BASE_DRIFT` and stop any conclusion that depends on another tree.

## 4. Locked naming contract

Use this authority chain everywhere:

```text
Candidate
  -> VersionId
  -> AcceptedVersion
  -> AcceptedBinding
  -> Head + HeadRevision or typed Root
```

Use the names precisely:

| Name | Meaning |
|---|---|
| **LayerStack-0** | V2 sandbox Version engine and sole selected-Version owner, implemented by rewriting `sandbox-runtime-layerstack`. |
| **EphCoW** | Reference-level copy-on-write over AcceptedBindings plus runtime-owned isolated writable Workspaces. |
| **Version** | One accepted complete immutable portable filesystem value. |
| `VersionId` | Typed content-derived Candidate identity; never equality, existence, admission, or reference authority by itself. |
| **AcceptedVersion** | LayerStack-0-verified durable admission of canonical bytes and one complete immutable payload closure. |
| **AcceptedBinding** | LayerStack-0-issued or revalidated reference capability naming an AcceptedVersion. |
| **Head** | Mutable selected reference containing an AcceptedBinding and monotone `HeadRevision`. |
| **Root** | Fixed typed durable reachability reference containing an AcceptedBinding. |
| **Branch** | Product exploration context: accepted starting binding, application context, and runtime-owned isolated Workspace. |
| **Checkpoint** | Product restore point represented by a typed Root. |
| **Workspace** | Mutable runtime-effect-owned filesystem view; never Version identity or selected truth. |

`StateId`, “state store,” “State Store,” “selected-state owner,” PMSS, and raw
digest references are historical vocabulary. Stable folder slugs such as
`02-state-identity` and `03-state-store` may remain in links, but new type, API,
metric, test, and prose names must use the Version model.

The product-owner decisions `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018`
remain open. Isolate them at existing application/API seams; never accept an
outcome on the owner's behalf.

## 5. Locked ownership and storage model

The algorithms must preserve this ownership map:

```text
application owners
  authorization, request ordering, expected Head capture,
  rollout/MCTS policy, scores, product orchestration
                    |
                    v direct calls
LayerStack-0: sandbox-runtime-layerstack
  canonical admission boundary, complete immutable payloads,
  AcceptedBindings, Roots, Heads, one OCC transition,
  recovery, retirement, bounded cleanup
                    |
                    v accepted Version / runtime request
existing runtime-effect owners
  Workspace, OverlayFS, mount, namespace, exec, manager/daemon lifecycle

observability -> diagnostic reader only
```

The selected conceptual physical family is:

```text
<LayerStack0Root>/
  versions/<VersionId>/payload/     complete immutable accepted closure
  heads/<selector>                  AcceptedBinding + HeadRevision
  roots/<kind>/<root-id>            typed reachability to AcceptedBinding
  staging/<transaction-id>/         bounded private Candidate work
  control/                          format/generation/recovery roles
```

Phase 03 chooses exact non-overlapping path spellings, record encodings,
checksums, durability fences, filesystem qualification, and bounded constants.
It does not choose a different storage family.

The following are not selected durable primitives:

- cross-Version Chunks or CDC;
- a manifest/Merkle/object DAG;
- a parent/layer/depth reconstruction chain;
- archive extraction as readable truth;
- reflink or filesystem snapshots as required correctness mechanisms;
- a database, new service, helper process, storage facade, or second writer;
- persistent refcount authority or tracing object-graph GC; or
- runtime OverlayFS, mount, namespace, Docker/OCI, or host paths in identity.

Any algorithm that requires one of these must return `REOPEN_PHASE_01` and
state the exact R0 failure it repairs, why the current owner/direct call cannot
repair it, and the dependency/crash/resource/operating costs introduced.

## 6. Required algorithm files

Create exactly these outputs in addition to this prompt:

```text
algorithm/
├── README.md
├── 01-canonical-version-identity.md
├── 02-complete-version-admission.md
├── 03-reference-ephcow.md
├── 04-occ-publication.md
├── 05-read-custody-and-runtime-handoff.md
├── 06-durability-and-recovery.md
├── 07-retirement-and-cleanup.md
├── 08-one-way-migration.md
└── 09-resources-complexity-and-observability.md
```

Do not create a Chunk/CDC algorithm package. Comparative notes belong in the
performance document and must remain non-selected hypotheses.

### `README.md` — composition and status

Include the package result, date, source seal, authority order, terminology,
ownership map, conceptual storage layout, file index, one end-to-end ASCII
flow, hard-rule crosswalk, cross-file invariants, evidence ledger, open
phase-owned choices, open owner decisions, and reopening conditions.

### `01-canonical-version-identity.md`

Specify the Phase 02 algorithm constraints without prematurely selecting its
codec/hash grammar: bounded portable-fact validation, deterministic canonical
bytes, domain/schema separation, typed `VersionId`, runtime-private exclusions,
and full canonical-byte equality. Make clear that a computed ID is a Candidate
identity only.

### `02-complete-version-admission.md`

Specify Candidate intake, reservation, bounded private staging, complete
filesystem-native payload construction, canonical-byte retention/comparison,
occupied-`VersionId` full-byte comparison, collision rejection, immutable
installation, `AcceptedVersion`, and issuance/revalidation of
`AcceptedBinding`. Equal canonical bytes must converge to one physical payload;
digest or length equality alone is insufficient.

### `03-reference-ephcow.md`

Specify Fork, Checkpoint-to-existing, rollback-to-existing, same-Version Head
move, and Root creation from an AcceptedBinding. Prove structurally that these
paths cannot open the payload and report:

```text
payload bytes read    = 0
payload bytes written = 0
payload bytes copied  = 0
```

Separate reference operations from Workspace activation, Candidate capture,
admission, and materialization, which may move bytes.

### `04-occ-publication.md`

Specify application authorization/ordering, Candidate admission, expected
AcceptedBinding plus `HeadRevision`, the single process/filesystem-exclusive
LayerStack-0 transition gate, one conditional Head-record replacement, stale
outcome, same-Version outcome, idempotent retry seam, and orphan accepted
payload handling. A stale writer loses cleanly and never silently merges,
rebases, or retries against a newly observed Head.

### `05-read-custody-and-runtime-handoff.md`

Specify capture/revalidation of an AcceptedBinding, bounded runtime-local read
custody, immutable Version access, and the handoff to existing Workspace,
OverlayFS, mount, namespace, and exec owners. Runtime activation and
materialization costs must be accounted separately from the zero-payload
reference claim. Accepted payloads may never become mutable lower/upper work.

### `06-durability-and-recovery.md`

Specify payload-before-reference ordering, recognizable staging states,
complete Head/Root record replacement, checksummed/generation-fenced control
records as Phase 03-selected details, crash-prefix classification, fail-closed
startup, quarantine, idempotent recovery, and bounded recovery work. Do not
claim one specific syscall sequence before Phase 03 qualifies it.

### `07-retirement-and-cleanup.md`

Specify exact Root/Head reachability plus read custody, final revalidation
under transition authority, retirement of complete payload closures, staging
cleanup, OCC-loser orphan cleanup, cancellation, restart behavior, and bounded
debt. Do not introduce a Chunk DAG or tracing-GC authority.

### `08-one-way-migration.md`

Specify fenced legacy reads, translation of portable complete-Version facts,
ordinary V2 Candidate validation/admission, one-writable-truth modes,
restartable progress, generation fencing, cutover, rollback-before-commit,
and deletion of temporary compatibility code. Legacy layer IDs, parent/depth,
whiteouts, mount paths, and host paths may not become V2 identity.

### `09-resources-complexity-and-observability.md`

Define variables and honest worst-case costs for canonicalization, full-byte
occupancy comparison, admission, reference transitions, publication, recovery,
retirement, migration, and runtime activation. Account for bytes, entries,
metadata operations, staging space, memory, FDs, workers, locks, custody, and
cleanup debt. Define counters that prove reference payload I/O `0/0/0`.
Observability consumes facts and may not become authority. Stage 4.6 remains
`INCOMPARABLE`; make no benchmark-winner or V2 performance-guarantee claim.

## 7. Per-file quality contract

Every algorithm file must include:

- purpose and owning phase;
- inputs, outputs, preconditions, and typed outcomes;
- concise pseudocode;
- normal, concurrent, retry, cancellation, crash, and cleanup behavior;
- the exact linearization or durable-visibility point where applicable;
- finite resource accounting and failure behavior;
- asymptotic time/space/I/O analysis with defined variables;
- security and path-validation obligations where untrusted input appears;
- observability/test seams;
- `SOURCE-VERIFIED`, `SPIKE-VERIFIED`, `INFERRED`, and `OPEN` evidence labels;
- details the owning phase may still select; and
- `REOPEN_PHASE_01` conditions.

Do not invent exact Rust signatures, codec bytes, digest algorithms, disk
filenames, fsync sequences, or numeric limits unless the owning phase has
selected and evidenced them. Conceptual APIs may show responsibility and type
flow but must label deferred spellings.

## 8. Required global invariants

The package must prove that its algorithms compose around these invariants:

1. One complete immutable Version is truth; no layer reconstruction.
2. Equal canonical bytes under one occupied `VersionId` map to one physical
   payload closure.
3. Occupancy equality uses full canonical-byte comparison; mismatch is a
   collision error.
4. Only LayerStack-0 admission creates/revalidates an `AcceptedBinding`.
5. Heads and Roots contain AcceptedBindings, never unchecked raw IDs.
6. Reference-only Fork/Checkpoint/rollback/same-Version moves perform payload
   bytes read/written/copied `0/0/0`.
7. Head publication has one OCC linearization point; stale loses without
   silent merge/rebase.
8. Accepted payloads cannot be modified by live Workspace writes.
9. MCTS/rollout policy and authorization remain outside LayerStack-0.
10. Portable identity excludes all runtime-private platform and host facts.
11. Migration has at most one writable selected-Version truth and its code is
    temporary and deletable.
12. Staging, memory, descriptors, workers, recovery, custody, and cleanup debt
    are bounded and fail closed.

Any unresolved item that changes ownership, storage family, dependency
direction, writer count, crash behavior, or hard-rule satisfiability requires
`REOPEN_PHASE_01`. Exact Phase 02 identity choices and Phase 03 filesystem
mechanics may remain `OPEN_WITHIN_R0` when the constraints above isolate them.

## 9. Final consistency check

Before reporting completion:

- verify all output links resolve;
- search new output for prohibited forward terms and classify every match;
- verify every file uses the same authority chain and one Head linearization
  point;
- verify CAS+CDC/Chunks/Merkle/reflink/layers appear only as rejected,
  comparative, or reopening material;
- verify the four owner DECs remain open;
- verify no benchmark result is claimed;
- verify no product source or live data changed; and
- list all files changed and checks run.

Return a concise result, paths written, source seal, remaining phase-owned
details, owner decisions still open, and any reopening condition.
