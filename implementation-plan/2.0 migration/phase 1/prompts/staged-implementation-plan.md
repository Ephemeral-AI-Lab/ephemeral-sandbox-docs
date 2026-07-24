# Phase 1 — staged SeqCDC/CAS implementation-plan prompt

Use this prompt in a new Codex task to produce the implementation-ready Phase
1 plan. This task creates planning documents only. It does not create a Git
branch or change product, E2E, benchmark, or deployment code.

## Mission

Create an evidence-backed, stage-based implementation plan for the Phase 1
SeqCDC/CAS LayerStack migration.

Write the plan under:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/`

The result must contain one overview and one self-contained specification and
E2E test plan per stage:

```text
implementation/
├── index.md
├── stage_00_<short_slug>/
│   ├── spec.md
│   └── e2e_test.md
├── stage_01_<short_slug>/
│   ├── spec.md
│   └── e2e_test.md
└── stage_NN_<short_slug>/
    ├── spec.md
    └── e2e_test.md
```

Use zero-padded stage numbers and short lowercase snake-case slugs. `stage_00`
must freeze the current baseline and establish the correctness, routing,
resource, and benchmark evidence seams needed by later stages.

The plan must answer four questions for every stage:

1. What useful, independently verifiable capability exists when this stage
   ends?
2. How can that capability be tested before the complete migration exists?
3. Which memory resources can it retain, when are they reclaimed, and how is
   bounded steady-state behavior proven in one long-lived process?
4. How does it preserve an exact zero-new-external-dependency delta and keep
   the portable core independent of host OS, CPU features, and target-image
   userland?

Until the final stage, optimize for implementation progress and fast
falsification. Require only focused proof-of-concept correctness tests, one or
more narrow end-to-end proofs where a public path exists, and a tiny
correctness/performance benchmark. Do not require agents to make the entire
E2E suite pass after every intermediate stage. Reserve broad regression,
complete E2E convergence, and normative time/space qualification for the final
stage.

Do not implement the plan. Do not change files under either source repository.
Only create or update the requested planning documents.

## Authority order

When sources conflict, use this order:

1. the current user request and this prompt;
2. repository-local `AGENTS.md`, `CLAUDE.md`, and other applicable
   instructions;
3. the Phase 1 preparation documents, with later decisions superseding earlier
   proposals;
4. current product and test behavior demonstrated by source and tests;
5. the current external benchmark application and E2E harness; and
6. architecture prose and secondary descriptions.

Do not silently reconcile a contradiction. Record it, identify which authority
controls, state its implementation effect, and name the decision needed.

## Read before planning

Read all applicable instruction files completely before examining or changing
anything. At minimum, inspect:

### Migration authority

- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/index.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/index.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prep/01-cdc-cas-space-time-materialization-spec.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prep/02-storage-solution-examination-review.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prep/03-seqcdc-cas-and-squash-decision.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md`
- `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 3/index.md`

Treat preparation document 04 as the quantitative acceptance contract.
Document 03's identity-preserving squash decision supersedes older wording
that says squash creates a new logical root. If quantitative requirements
conflict, the stricter requirement governs.

SeqCDC is selected for gated implementation, not assumed production-ready.
StreamCDC is the fallback only for a demonstrated algorithm-specific failure.
A failure of the shared CAS, publication, materialization, recovery, retention,
or GC architecture cannot be hidden by changing chunkers.

### Product repository

Explore the actual source, tests, and current Git state under:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`

Start with:

- `AGENTS.md`
- `CLAUDE.md`
- `docs/maintainer-architecture.md`
- the workspace `Cargo.toml`
- `Cargo.lock`, workspace dependency declarations, build scripts, and enabled
  features;
- `config/prd.yml` and `config/bench.yml`
- `crates/sandbox-config/src/configs/runtime.rs`
- `crates/sandbox-runtime/layerstack/src/`
- `crates/sandbox-runtime/layerstack/tests/`
- `crates/sandbox-runtime/workspace/src/`
- `crates/sandbox-runtime/workspace/tests/`
- `crates/sandbox-runtime/overlay/src/`
- `crates/sandbox-runtime/operation/src/`
- `crates/sandbox-runtime/operation/tests/`
- `crates/sandbox-runtime/namespace-execution/src/`
- `crates/sandbox-runtime/namespace-process/src/`
- `bin/start-sandbox-docker-gateway`

Trace symbols and callers rather than inferring behavior from filenames.
Specifically inspect:

- manifest, layer, identity, filesystem-change, lease, and substitution types;
- whole-file publication and staging, fsync, rename, and manifest-commit
  boundaries;
- OCC behavior and idempotent retry behavior;
- upper-directory capture and its `WriteFile` source-path handoff;
- merged-view projection, export, hydration-equivalent paths, and squash;
- workspace create, publish, finalize, destroy, recovery, and live remount;
- autosquash policy and configuration;
- operation-service configuration and telemetry seams;
- command, file, PTY, stdin, signal, cancellation, and child-reaping paths;
- fixture compatibility and golden-root tests; and
- target-specific `cfg`, `target_feature`, SIMD, `unsafe`, FFI, host-path, and
  target-image command assumptions;
- any existing ignored benchmark or JSON result format.

At minimum, evaluate these existing seams before proposing new ones:

- `workspace/src/overlay/capture.rs::capture_upperdir` as a possible bounded
  streaming ingest boundary;
- LayerStack publication staging and manifest commit as the transaction
  boundary;
- `stack/projection` as a legacy materialization correctness oracle;
- `export_delta` and flattening tests as logical-tree oracles;
- `operation` service configuration as a possible rollout-control boundary;
  and
- `layerstack/tests/occ_merge_bench.rs` as a source of workloads and result
  conventions, while clearly distinguishing modeled data from measurements of
  a real backend.

Do not assume these are the final design. Confirm their current behavior and
ownership first.

### External E2E and benchmark repository

Explore the complete relevant surface under:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`

At minimum, inspect:

- `README.md`
- `e2e/pytest.ini`
- `e2e/conftest.py`
- `e2e/harness/catalog/declarations.py`
- `e2e/harness/runner/`
- `e2e/harness/runner/resources.py`
- `e2e/compound/configuration/config/`
- `e2e/runtime/workspace_session/`
- `e2e/manager/management/squash/`
- `e2e/manager/management/export/`
- `e2e/compound/stress/`
- `e2e/observability/resource_isolation/`
- `e2e/observability/resource_efficiency/`
- `benchmark/README.md`
- `benchmark/pyproject.toml`
- `benchmark/` runner, models, result schema, and presets; and
- `.e2e-state/` and `.benchmark-state/` artifact conventions.

Use the existing E2E control room and benchmark laboratory. Do not propose a
second competing scheduler or an unrelated benchmark framework unless a
specific, evidence-backed gap makes that unavoidable.

Verify commands from current source before placing them in the plan. The
expected focused live-E2E shape is:

```bash
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test
E2E_IMAGE=ubuntu:24.04 \
E2E_REBUILD_BINARY=1 \
PYTHONPATH=e2e \
.venv/bin/python -m pytest <node-or-folder> \
  --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test \
  --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

Confirm this against the current harness. Use rebuild mode for the first gate
after product changes and the supported reuse mode for focused reruns. Follow
the repository-specific E2E reporting and run-scoped cleanup rules when
implementation begins.

## Repository and branch preflight

Before designing stages, perform read-only preflight in both repositories:

- current branch, `HEAD`, remote tracking state, and worktrees;
- `git status --short`;
- applicable instruction files;
- toolchain and Docker availability; and
- existing user changes that must not be overwritten.

The eventual implementation is requested on a fresh branch based on the
newest approved source revision. However, at the time this prompt was written,
the product repository's `AGENTS.md` and `CLAUDE.md` required direct work on
`main` and prohibited side branches and worktrees.

Therefore:

1. do not create a branch during this planning task;
2. record the conflict prominently in `implementation/index.md`;
3. state the exact current branch and base commit observed during planning;
4. require an explicit repository-owner or user policy resolution before
   implementation starts;
5. after that resolution, require the implementation task to record the
   approved branch name and immutable base commit before editing code; and
6. never interpret “newer branch” silently as either a side branch or updated
   `main`.

This branch-policy issue blocks implementation, not completion of the planning
documents.

## Environment contract

Plan normative Phase 1 performance qualification for Docker Desktop running
the pinned `ubuntu:24.04` sandbox image. Do not use that single qualification
environment to claim Firecracker/KVM, WASM/WASI, native Linux, macOS, Windows,
or every-image qualification. Keep a separate portability contract and label
each platform or image `qualified`, `contract-tested`, `designed-compatible`,
or `unverified`.

Every benchmark and E2E plan must record enough environment data to make
results comparable:

- product and test repository commits and dirty state;
- Docker Desktop and Docker Engine versions;
- image digest, not only the `ubuntu:24.04` tag;
- host architecture, CPU allocation, memory allocation, and storage limit;
- guest kernel and filesystem/mount details;
- OverlayFS and `userxattr` behavior where relevant;
- Rust and Python versions;
- runtime configuration and rollout mode;
- cache state, warm/cold classification, seed, and corpus identity; and
- whether RSS came from cgroups, process sampling, `docker stats`, or another
  stated source.

Docker Desktop may not expose every in-container cgroup metric. The plan must
name an independent measurement fallback, such as Docker resource sampling
and `docker inspect --size`, without changing the public-CLI correctness
boundary.

## Zero-new-dependency and portability contract

The Phase 1 design has a zero-new-external-dependency budget. It must not add:

- a new resolved third-party Rust package/version, an additive direct external
  manifest edge, a Cargo feature activation, Python/npm dependency, vendored
  library, C/C++/FFI library, system package, command-line tool, runtime
  service, daemon, sidecar, or target-image helper;
- a new requirement for a shell, `tar`, coreutils, Python, package manager,
  libc flavor, or dynamically linked utility inside the sandbox image; or
- a build-time download, runtime download, or network service needed for
  publication, SeqCDC, CAS, materialization, squash, recovery, compaction, or
  GC.

Implement SeqCDC and the required streaming state in the product workspace
using Rust's standard library and third-party crates already present in the
approved baseline dependency graph. Reuse existing hashing, serialization,
async, checksum, compression, and test facilities only where their current
licenses, enabled features, and behavior satisfy the contract. Do not add a
`seqcdc`, `fastcdc`, database, allocator, heap-profiler, or benchmarking
library. A focused diagnostic tool may be used manually if it is already
available in the environment, but it cannot enter the build, test, image, or
runtime dependency graph.

Freeze and compare like-for-like dependency baselines for every supported
target and feature invocation. Do not compare different target-conditioned
graphs and call the difference a Phase 1 delta.

“Zero external delta” means all of the following:

- the product-wide set of resolved external package identities and versions is
  byte-for-byte unchanged;
- the product-wide enabled external feature set is unchanged;
- the count and multiset of direct external manifest edges do not grow;
- an existing direct external edge may be relocated between workspace crates
  only as part of a documented responsibility move, with the old edge removed,
  no package or feature change, and no increase in the product-wide edge
  multiset; and
- new workspace crates otherwise depend only on the standard library and
  internal workspace crates.

Thus a clean SRP split may add or rearrange internal workspace edges, but it
cannot expand the product's third-party attack, licensing, build, or runtime
surface. Prefer exposing an existing capability through a narrow internal
owner over duplicating its third-party edge. Do not add a wrapper solely to
game the dependency count.

Internal workspace modules and crate dependency edges may change when the
SRP/SOLID design requires it, but every new internal edge must point inward,
remain cycle-free, and be recorded. For every stage, capture before/after
evidence for:

- workspace manifests and lockfile package set;
- resolved Cargo package count and feature graph;
- non-Rust manifests and lockfiles;
- container image packages and helper binaries;
- external processes, sockets, and services used by the changed path; and
- licenses or notices affected.

The required external-dependency delta is exactly zero. A lockfile reorder or
version resolution change is not automatically harmless: explain and remove
it unless it is already caused by the approved baseline. Do not count Linux
container images used as compatibility fixtures as product dependencies, but
pin their immutable digests in evidence.

At planning time, define a finite, versioned release-triple matrix of
`host OS/version × host architecture × Docker Engine/Desktop version`. Include
every triple the release intends to support; do not use the moving phrase
“whatever Docker supports” as a test set. The architecture is still designed
to be host-independent beyond that matrix, but qualification and release
claims apply only to named rows with evidence.

Also define one versioned Linux-image capability profile. Compatibility is
claimed for images satisfying that profile, rather than for an unbounded list
of tags. The profile must state:

- valid Linux OCI/Docker configuration and root filesystem;
- matching architecture or explicitly configured Docker emulation;
- the current product's documented container-creation and provider-runtime
  prerequisites;
- required mount, namespace, filesystem, xattr, security-policy, and
  writable-storage semantics;
- no dependency on image-provided shell, libc, package manager, coreutils, or
  network; and
- how shell-less, distroless, scratch-style, read-only-base, and non-root
  images satisfy or fail each capability.

This is a design and compatibility requirement, not permission to make an
unmeasured “universal” claim. Explicitly define the boundary:

- required host rows may cover Linux, macOS, and Windows on the CPU
  architectures in the declared sandbox release matrix;
- the target is a Linux container image, including glibc, musl, distroless,
  and shell-less/scratch-style images satisfying the capability profile;
- foreign-architecture execution is required only when Docker provides the
  corresponding native support or configured emulation;
- the storage path cannot promise that an arbitrary user command exists
  inside an image; command execution may fail normally when the user-requested
  executable is absent; and
- Windows containers, unsupported Docker hosts, and image/kernel features the
  current sandbox explicitly does not support are outside this contract and
  must be listed rather than hidden.

Keep the portable LayerStack/SeqCDC/CAS core independent of:

- host path separators, drive letters, case-folding rules, endianness, word
  size, inode numbers, wall-clock formatting, locale, and host filesystem
  ordering;
- Docker Desktop VM paths and host filesystem implementation details;
- target-image shell, userland, package set, libc, entrypoint, working
  directory, and writable-root assumptions;
- x86-only instructions or compile-time CPU feature requirements; and
- provider-specific mount, OverlayFS, namespace, device, whiteout, or
  materialization locators in logical identities and portable manifests.

Use explicit-width, explicitly ordered serialization and deterministic byte
ordering. Treat container filesystem paths as validated Linux byte paths at
the provider boundary; do not round-trip them through host-native path
semantics. Preserve all currently supported Linux metadata and filesystem
behavior, including modes, ownership mapping, symlinks, hard links where
supported, sparse extents, whiteouts, opaque directories, and relevant xattrs,
without requiring utilities inside the target image.

SeqCDC must have a deterministic portable scalar implementation. Optional
SIMD acceleration may be selected only through safe runtime feature detection
inside a narrow optimization module. It must:

- never be required for correctness or startup;
- have scalar fallback on non-x86 and non-SIMD machines;
- produce byte-for-byte identical chunk boundaries and object identities on
  scalar, x86_64, and AArch64 paths;
- avoid unsafe code unless current-source evidence shows it is necessary and
  the stage adds a documented safety proof and scalar differential tests; and
- fall back safely when a feature is unavailable or misreported.

Linux/Docker-specific mount and namespace mechanics belong only in the Docker
provider adapter. The portable core and its persisted identities must remain
reusable by later Firecracker and WASM adapters without translation or a
second storage truth.

Trace every current target-image command or host-specific syscall assumption.
If the image-neutral contract cannot be met without a new external dependency
or helper, record a design blocker and redesign the provider boundary; do not
silently narrow the requirement or inject a utility into the image.

The final stage must include the frozen release-triple and image-capability
matrices with at least:

- the pinned normative Docker Desktop + `ubuntu:24.04` qualification run;
- contract tests for every host OS/architecture actually available in CI or
  the declared release matrix;
- representative Ubuntu/Debian glibc, Alpine musl, minimal/distroless, and
  shell-less image fixtures, using public file/workspace operations when the
  image has no executable;
- read-only base image and non-root user cases;
- scalar-forced versus each available accelerated SeqCDC path using the same
  golden corpus and arbitrary input segmentation;
- the OCI index digest and resolved platform-manifest digest for every
  multi-architecture fixture; and
- explicit `required-release` or `informational` scope plus `unverified` rows,
  owners, and required evidence for matrix entries that the planning
  environment cannot run.

No row becomes `qualified` without execution evidence. A platform may be
`designed-compatible` while its test infrastructure is pending, but the plan
must not call the solution universally qualified until the declared release
matrix passes. An `unverified` required-release row blocks the final
portability/production go/no-go gate, although the pinned Ubuntu performance
qualification may still be reported separately. An unverified informational
row blocks only a claim about that row.

## Architecture laws

Preserve current product behavior, filesystem semantics, data integrity, and
the useful direction of ownership. Do not treat the current crate, module,
type, or service structure as immutable. It is evidence about today's system,
not a constraint against a cleaner 2.0 architecture.

Use these current responsibilities as the starting point:

- LayerStack owns content identity, manifests, layers, storage, and leases.
- Workspace owns workspace lifecycle and upper-directory capture.
- Overlay owns low-level mount and unmount mechanics.
- Operation services orchestrate product workflows.
- Namespace crates retain execution and process semantics.
- Normal command, file, PTY, and stdin paths operate on native filesystems.
- CDC/CAS is not a hot-path execution VFS.
- CAS hydration must complete, verify, fsync, and become visible atomically
  before execution can use it.

The universal reusable item is the platform-neutral checkpoint-storage core:
logical roots and objects, SeqCDC chunking, typed hashes, manifests, packs,
indexes, publication/OCC, leases, retention, journals, recovery, and GC.
Docker/OverlayFS, Firecracker, and WASM require provider-specific
materialization and activation adapters. Provider locators, mount identifiers,
Linux whiteout encodings, and backend materialization generations must not
enter portable logical `RootId` identity.

Design this boundary now, but implement and qualify only the Docker/OverlayFS
adapter in Phase 1. The declared Docker host/image portability matrix remains
part of that adapter's Phase 1 qualification.

Preserve current deterministic unsupported PTY behavior for resize, arbitrary
signals, and literal EOF unless separately authorized. Do not claim new PTY
parity as part of storage migration.

## Software-design quality contract

Treat software design as an acceptance dimension, not a cosmetic review at
the end. The target must be cohesive, loosely coupled, testable, and open to
the already-planned Docker, Firecracker, and WASM provider evolution without
making Phase 1 implement those future providers.

Apply SRP and SOLID concretely:

- **Single responsibility:** every module and type has one primary
  responsibility and one principal reason to change. Do not combine chunk
  boundary selection, object persistence, publication coordination,
  materialization, provider activation, policy, and telemetry in one service.
- **Open/closed:** adding a materialization provider or a versioned storage
  format should primarily add an adapter or implementation, not rewrite the
  logical-root and transaction core.
- **Liskov substitution:** implementations behind a port must obey the same
  identity, atomicity, durability, error, cancellation, and resource-bound
  contract. Require shared contract tests; do not make callers branch on
  concrete implementation quirks.
- **Interface segregation:** use narrow capability-oriented ports. A chunker
  does not receive lease or mount methods; a materializer does not own root
  publication; an object reader is not forced to implement GC policy.
- **Dependency inversion:** orchestration and portable domain logic depend on
  stable contracts. Docker/OverlayFS, filesystem layout, clocks, and resource
  sampling implement or sit outside those contracts. Portable code must not
  import provider-specific identifiers or Linux mount concepts.

Loose coupling does not mean maximum abstraction. Prefer a small concrete type
when there is only one stable behavior. Introduce a trait or indirection only
at a demonstrated variation, test, ownership, or provider boundary. Record
the evidence for every new abstraction.

For each stage, require a design-quality table:

| Component/type | One responsibility | Dependencies | Dependents | Extension seam | Reason to change | Must not own |
| --- | --- | --- | --- | --- | --- | --- |

Also require:

- an inward-pointing dependency diagram;
- a check for dependency cycles and forbidden crate edges;
- constructor inputs that expose required dependencies rather than hidden
  globals;
- narrow error types with no provider leakage into portable APIs;
- immutable value types for identities and validated configuration;
- explicit ownership of transactions, buffers, workers, and cleanup;
- contract tests for every substitutable port;
- no “manager”, “service”, or context object that accumulates unrelated
  responsibilities; and
- a change-impact exercise showing the files expected to change when adding:
  1. a versioned chunker profile or approved StreamCDC fallback;
  2. a Firecracker materialization adapter; and
  3. a WASM/WASI materialization adapter.

A good extension design keeps logical root identity, object formats,
publication/OCC, leases, retention, and recovery stable while provider
materialization changes. If an extension requires edits across unrelated core
modules, identify and repair that coupling in the plan before implementation.

## Architecture-change mandate

Prefer the clean, internally consistent, future-proof target architecture over
the smallest diff. Substantial and disruptive internal changes to the existing
Ephemeral Sandbox are explicitly allowed and encouraged when they materially
improve:

- single responsibility and cohesion;
- dependency direction and loose coupling;
- one authoritative model for roots, transactions, leases, and recovery;
- crash consistency and data integrity;
- removal of physical-layout leakage from logical APIs;
- testability and deterministic failure injection;
- bounded-resource enforcement;
- Phase 2 durable graph, checkpoint, branch, rollback, merge, promotion, and
  MCTS compatibility; or
- Phase 3 Docker/OCI, Firecracker, and WASM/WASI adapter compatibility.

This authorization includes moving responsibilities, splitting or combining
modules, replacing leaky types, changing internal service composition,
introducing versioned formats, and retiring accidental abstractions. It does
not authorize changing public behavior without a migration contract, weakening
correctness, or expanding Phase 1 into Phase 2/3 feature implementation.

Do not preserve a poor boundary merely because current code uses it. Also do
not propose a big-bang rewrite. Every disruptive change must have:

1. a named architectural defect in the current design;
2. evidence from actual files, symbols, dependencies, or failure modes;
3. a target responsibility and dependency model;
4. a simpler alternative considered;
5. concrete Phase 1 integrity or Phase 2/3 compatibility benefit;
6. a staged compatibility bridge;
7. focused POC proof and a rollback point;
8. old/new format and mixed-version behavior;
9. a deletion point for transitional code; and
10. a complexity budget that prevents permanent dual architecture.

Use a strangler or additive transition where durable data and live work are at
risk, but allow a stage devoted to architectural realignment before feature
work if that produces a cleaner end state. Transitional adapters must have an
owner, purpose, removal gate, and latest-removal stage.

For Phase 2, prove the Phase 1 target exposes stable backend-neutral contracts
for immutable `RootId`, parent/child checkpoint publication, leases, OCC,
diff/blame/provenance, activation, retention, and rollback without requiring a
resident sandbox per node.

For Phase 3, prove the target separates:

- portable checkpoint storage and transaction truth;
- provider-local materialization;
- workspace-session-local writable state, which a future Phase 2
  `ExecutionAttempt` may own through an explicit identity mapping rather than
  through a Phase 1 filesystem name;
- execution/process/stream lifecycle; and
- capability reporting.

Show that OCI/Linux, Firecracker, and WASM can use the same root and
publication contracts without forking CAS, identity, leases, recovery, or GC.
The plan designs these seams in Phase 1 but implements only the Docker/OCI
path.

## Required `/eos` storage and runtime-scratch views

The plan must show how LayerStack data is stored under `/eos` today and after
every stage. Do not show only the repository source tree.

Confirm the current runtime layout from configuration and storage code. At
prompt-authoring time, the evidence indicates this starting shape:

```text
/eos/
├── layer-stack/
│   ├── .storage-writer.lock
│   ├── manifest.json
│   ├── workspace.json
│   ├── base/
│   │   └── B000001-base/
│   ├── layers/
│   │   └── <layer_id>/
│   ├── staging/                  # transient entries during storage operations
│   │   └── <layer_id>.staging/
│   └── .layer-metadata/
│       ├── <layer_id>.digest
│       └── <layer_id>.bytes
├── storage/
│   ├── file_auditability/
│   └── workspace_recovery/       # created only when failed cleanup preserves data
├── workspace/
│   ├── manager.json
│   └── <workspace_session_id>/
│       ├── upper/
│       └── work/
├── namespace_execution/
│   └── <namespace_execution_id>/
│       └── transcript.log
└── runtime/
    └── daemon/
```

Re-verify every path. Correct this tree if current source differs. Cite the
configuration field or storage symbol that creates or consumes each entry.
At minimum, trace:

- `runtime.workspace.scratch_root` and
  `WorkspaceManager::workspace_session_root`;
- `WorkspaceManager::persisted_handles_path` and the `manager.json`
  recovery/reaping flow;
- `runtime.namespace_execution.scratch_root`,
  `CommandOperationService::prepare_transcript_path`, and
  `CommandExecValue::drop`; and
- command admission ownership plus `WorkspaceCommandTeardown` ordering.

### Required runtime-scratch consolidation

Treat the two current scratch roots as a physical-layout defect, not as two
domain lifecycles. The current code admits each namespace execution to exactly
one `WorkspaceSessionId`, records that ownership, and drains active commands as
part of workspace teardown. The Phase 1 target must therefore consolidate
namespace-execution scratch beneath its owning workspace session:

```text
/eos/
├── workspace/
│   ├── manager.json
│   └── <workspace_session_id>/
│       ├── upper/
│       ├── work/
│       └── executions/
│           └── <namespace_execution_id>/
│               └── transcript.log
├── layer-stack/
├── storage/
└── runtime/
    └── daemon/
```

This is a normative target decision:

- do not introduce `/eos/attempts` in Phase 1;
- keep `ExecutionAttempt` as a future orchestration identity that can reference
  or own a `WorkspaceSessionId` without dictating the local path;
- preserve `manager.json` outside every deletable per-session subtree because
  it is the workspace crash-recovery catalog;
- keep logical ownership separate even though the paths share a parent:
  workspace lifecycle owns the session directory and OverlayFS `upper/` and
  `work/`, while command execution owns each `executions/<id>/` directory and
  transcript;
- expose the session-scoped execution path through a narrow, validated
  workspace-scratch locator or equivalent value object; do not let execution
  code reconstruct a sibling service's paths with unchecked string joins;
- retain namespace-execution limits under
  `runtime.namespace_execution`, but plan the compatible retirement of
  `runtime.namespace_execution.scratch_root` after the workspace-scoped
  locator becomes authoritative;
- support and safely reap stale legacy `/eos/namespace_execution` directories
  during the compatibility window; do not copy ephemeral transcripts into
  LayerStack or CAS;
- validate containment, identifier encoding, permissions, and symlink behavior
  before recursive cleanup;
- order teardown so active commands are rejected, cancelled, and joined,
  retained terminal entries and transcript owners are released, and only then
  is the enclosing workspace-session directory recursively removed; and
- prove that implicit and explicit workspace sessions, multiple concurrent
  commands, command-ID reuse after daemon restart, crash recovery, failed
  cleanup retry, and legacy-root cleanup cannot cross-delete or mix
  transcripts.

The physical consolidation must not merge the workspace and command
responsibilities into one manager/service, make command execution own
workspace teardown, or leak local scratch paths into portable LayerStack,
`RootId`, CAS, or provider-neutral APIs. A future OCI, Firecracker, or WASM
adapter may use a different provider-local locator behind the same lifecycle
contract.

For the target and every intermediate stage, provide an exact annotated tree
under `/eos`, with `/eos/layer-stack` fully expanded and the workspace-session
scratch delta shown. It must show the proposed placement of all applicable:

- legacy manifest and whole-file layers;
- portable logical roots and versioned manifests;
- content objects, open/sealed packs, and locators;
- bounded indexes and index pages;
- publication, hydration, squash, compaction, migration, and recovery
  journals;
- transaction staging and atomic promotion targets;
- leases, retention epochs, GC cursors, and quarantine;
- native hot carriers and rebuildable provider materializations;
- format/version markers;
- temporary files and crash residue cleanup; and
- observability metadata only when it is durable storage state.

Annotate every entry with:

- `[existing]`, `[add]`, `[migrate]`, `[compat]`, or `[remove-later]`;
- logical source of truth, rebuildable cache, transaction staging, or
  ephemeral scratch;
- owning module/type;
- creation, visibility, fsync, recovery, and deletion lifecycle;
- whether it participates in `RootId`;
- reader and writer in each rollout mode;
- maximum or complexity bound;
- physical-space accounting category; and
- permissions and reserved-path exposure.

Keep `/eos` runtime internals hidden from sandbox workloads as the current
mount-mask contract requires. The user-visible `/workspace` view and ordinary
native execution path must remain unchanged.

## Stage-decomposition laws

Derive the exact stages from current source. Do not copy a desired architecture
onto the repository without tracing its real integration seams, but do not let
the existing layout veto a better evidence-backed architecture.

Each stage must be:

- a smallest practical vertical slice;
- independently buildable, testable, reviewable, and rollbackable;
- compatible with all artifacts produced by earlier stages;
- explicit about which path is authoritative;
- measurable before a later stage exists; and
- complete enough that its exit gate is falsifiable.

“Testable” does not mean “run and repair the whole E2E suite” for an
intermediate stage. It means that the stage's newly introduced mechanism,
route, and most important invariant have a focused proof and a fast benchmark
sentinel.

Use additive migration. Keep the legacy path authoritative until the candidate
has produced enough evidence for a deliberate cutover. The plan should
evaluate a progression such as:

```text
legacy
  -> shadow_write
  -> dual_read_verify
  -> candidate_read_strict
  -> candidate_authoritative_with_legacy_shadow
  -> candidate_default
  -> legacy_retirement
```

These names are proposals, not existing facts. Confirm how typed runtime
configuration can represent the modes. No CDC/backend rollout switch exists
today, so configuration, validation, route telemetry, and comparison counters
are stage deliverables rather than assumed infrastructure.

For every migration mode, define:

- writer and publication authority;
- reader and materialization authority;
- whether fallback is permitted;
- which root format versions are accepted;
- what shadow work consumes;
- mismatch and corruption behavior;
- required route, fallback, and mismatch evidence; and
- rollback behavior.

One logical publication must have one authority. Shadow processing consumes an
already committed logical change/root or transaction input; it must not
publish a competing root. A candidate test that succeeds through a legacy
fallback is not a candidate-path pass.

Do not retire a compatibility reader or legacy path in the same stage that
first makes the candidate authoritative. Include a soak and rollback interval.

The stage sequence should consider, but must not blindly adopt:

1. frozen baseline, stable corpora, route/resource instrumentation, and
   benchmark seams;
2. versioned portable identity, schema, types, and golden compatibility;
3. bounded streaming SeqCDC plus its deterministic oracle and object writes;
4. shadow CAS ingest using legacy publication authority;
5. candidate materialization plus dual-read/tree comparison;
6. strict opt-in candidate activation with explicit no-fallback proof;
7. durable publication, leases, catalogs, recovery, retention, and bounded GC;
8. identity-preserving squash, native-carrier lifecycle, and live remount;
9. mixed-root migration and candidate authority;
10. default enablement, soak, rollback proof, and only then legacy retirement.

Reorder, split, or merge these only when current code dependencies and
stage-local testability justify it.

## Test-effort policy by stage

Use two explicit test tiers:

### Intermediate stages: POC proof tier

Every stage except the final stage requires only:

- compilation and the smallest relevant formatting or static check;
- focused Rust unit, golden, property, or integration tests for the changed
  primitive or transaction;
- the minimum live E2E node or nodes needed to prove that the packaged product
  took the intended route, when that route is externally reachable;
- one primary negative, restart, rollback, or cleanup proof appropriate to the
  stage;
- a deterministic tiny benchmark for correctness and gross time/space
  regression;
- a lightweight memory-lifecycle sentinel in the same long-lived process when
  the stage adds an allocation, cache, registry, queue, worker, mapping, or
  cleanup path; and
- machine-readable artifacts sufficient to compare the next stage.

Do not require at an intermediate stage:

- the complete E2E suite;
- every historical feature family;
- full release, nightly, stress, or long-duration matrices;
- the full corpus and sample count from preparation document 04;
- final p50/p95 qualification;
- unrelated flaky-test repair; or
- proof of behavior that cannot exist until a named later stage.

The plan may define future E2E cases early, but mark them `planned-final`,
`deferred-to-stage_NN`, or equivalent rather than making them intermediate
exit gates. A failure in a focused test that exercises changed behavior is a
real blocker. A pre-existing or unrelated broad-suite failure is recorded with
evidence and left outside the intermediate stage.

### Final stage: integration and qualification tier

The last stage owns:

- all focused proofs accumulated from earlier stages;
- mixed legacy/new-root and end-to-end migration coverage;
- the affected full E2E regression suite;
- release/qualification E2E required by the Phase 1 contract;
- full correctness, recovery, memory, physical-space, and performance
  matrices;
- normative baseline/candidate/StreamCDC comparison where required;
- Docker Desktop Ubuntu 24.04 environment evidence;
- zero-new-external-dependency evidence and the declared host/image
  portability matrix;
- soak, rollback, cleanup, and legacy-retirement proof; and
- triage of every failing required test to pass, accepted blocker, or explicit
  no-go.

Only this final stage may claim Phase 1 qualification or production
enablement.

## Required memory-lifecycle, leak, and reclamation contract

Treat memory stability as a correctness property, not merely a performance
number. Preparation document 04 remains normative for all buffer, queue,
worker, cache, semaphore, peak RSS, settled RSS, input-scaling, and
history-scaling ceilings. The staged plan must add lifecycle evidence without
weakening or replacing any of those gates.

Keep these two meanings of “GC” separate:

1. **Process-memory reclamation.** The product is Rust and has no
   tracing-language garbage collector. The relevant risks are retained
   allocations, strong `Arc` cycles, unbounded collections, caches,
   registries, channels, queued futures, detached tasks or threads, leaked
   mappings and file descriptors, allocator high-water retention, and
   incomplete cleanup on error or cancellation.
2. **LayerStack storage GC.** This is reachability and reclamation of durable
   CAS objects, packs, roots, journals, and rebuildable materializations on
   disk. Storage GC must itself use bounded application memory, but successful
   disk reclamation is not evidence that process memory was reclaimed.

For every stage that allocates, borrows, maps, caches, queues, or asynchronously
retains data, inventory at least:

- chunk, hash, manifest, journal, index, hydration, publication, squash, and
  GC buffers;
- borrowed chunk views and their maximum in-flight count;
- every `Arc`/`Weak` ownership graph, including the reason no strong reference
  cycle can survive completion;
- maps, registries, LRUs, index caches, terminal-command records, and their
  capacity, eviction, and teardown behavior;
- channels, queues, retry sets, pending futures, and both item and byte bounds;
- tasks, threads, blocking workers, cancellation tokens, join handles, and
  shutdown ownership;
- `mmap`, file-backed pages, page cache, file descriptors, and how their
  contribution is distinguished from anonymous heap RSS where the platform
  exposes it;
- FFI, SIMD-aligned, pinned, or allocator-specific buffers, if introduced;
  and
- permits, temporary files, staging state, and partially constructed values
  on success, error, timeout, cancellation, panic containment, retry, rollback,
  and daemon recovery paths.

Each applicable `spec.md` must include this table:

| Resource retained in memory | Owner | Acquire point | Hard item/byte bound and permit | Normal release | Error/cancel/panic release | Shutdown/restart behavior | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

The design must have one named owner and one bounded release path for every
row. Back-references use `Weak` or non-owning identifiers unless a documented
proof shows that a strong edge cannot form a cycle. Dropping the caller must
cancel or transfer ownership deliberately; it must not detach untracked work.
All spawned work must be bounded and either joined or owned by a bounded
long-lived supervisor with explicit shutdown.

Memory evidence must distinguish these states:

```text
idle baseline
  -> warmed idle
  -> active peak
  -> logical cleanup complete
  -> settled post-cleanup
  -> repeated steady state
```

“Settled” is reached by bounded polling of product-observable quiescence:
operation handles are complete, queues are drained, temporary ownership is
released, worker activity has returned to its expected idle cardinality, and
byte/item permits and live-resource gauges have returned to their declared
baseline. Define a deadline and missing-data behavior. Do not substitute an
arbitrary sleep, process/container restart, `malloc_trim`, allocator swap, or
manual cache purge for lifecycle proof.

Use a two-part verdict:

1. **Logical release:** live owned-byte, object, buffer, queue, task, permit,
   registry, lease, mapping, and file-descriptor counts return to their
   expected bounded idle values after quiescence. Terminal-retention and
   shared-cache entries may remain only within their explicit capacities and
   eviction rules.
2. **Physical stability:** peak and settled process RSS and cgroup memory stay
   within every gate classified `stage-gating`; the final stage applies all
   preparation-document-04 memory gates. Repeated post-warmup cycles show no
   unexplained positive settled-memory trend. Report first-window versus
   last-window deltas and a robust slope with its sample count and noise band.
   Freeze the noise band from an equal-warmup control run before judging the
   candidate; do not tune it after seeing candidate results.

RSS alone cannot prove a heap leak because allocators may retain freed arenas
and the kernel may retain file-backed pages. Conversely, allocator reuse
cannot excuse growing live ownership. Collect, where available, process RSS,
anonymous and file-backed RSS, cgroup current/peak memory, open file
descriptors and mappings, worker/task/queue counts, byte permits, cache and
registry cardinality, and component live-owned-byte gauges. Use a focused
heap profiler or allocator diagnostic only to investigate a failure; do not
make a different production allocator or privileged profiler a runtime
dependency.

Every applicable stage needs a small repeated-operation sentinel inside its
existing 30–60 second POC loop. Exercise the new happy path and at least the
most important applicable cancellation, timeout, or injected-error cleanup
path in one long-lived test process. Use the packaged daemon/container without
restart when a packaged route exists; an internal-only stage uses its
long-lived integration-test or benchmark process. The final stage additionally
owns:

- paired legacy/control and candidate runs after equal warmup;
- repeated create, execute, publish, materialize, squash, storage-GC, and
  destroy cycles applicable to the final architecture;
- the exact input-size and retained-history scaling matrix from preparation
  document 04;
- cold-cache and warm-cache attribution;
- long-lived workspace-session execution churn, including terminal-retained
  transcripts and workspace teardown;
- failure before and after each publication visibility boundary; and
- a declared repetition count and predeclared slope/noise acceptance rule
  sufficient to expose cumulative retention. Each matched scenario or
  `input size × retained-root count × candidate` point receives its own
  five-minute raw/candidate invocation and required repetitions exactly as
  preparation document 04 specifies; do not pack the matrix into one
  five-minute run. Declare a separate aggregate suite budget.

Do not create a heavyweight leak suite at every intermediate stage. Reuse the
tiny benchmark process and resource sampler, adding lifecycle gauges and a
short repetition loop. If a stage demonstrably changes no runtime allocation
or ownership path, its documents must identify that fact, reuse the nearest
memory sentinel, and defer only the full qualification matrix—not silently
omit memory evidence.

LayerStack storage GC, compaction, and squash must stream or externally merge
their live-set and relocation work within the same bounded-memory contract.
They must not load the complete object set, root history, manifest set, or
pack index into RAM. Their E2E evidence must separately report durable bytes
reclaimed, temporary disk used, peak process memory, logical-release gauges,
and settled-memory stability.

## Required output: `implementation/index.md`

The overview must be sufficient to navigate and audit the whole plan. Include:

1. **Status and decision summary**
   - purpose, scope, non-goals, selected SeqCDC status, and qualification
     environment;
   - observed facts versus proposed design versus unresolved decisions.
2. **Authority and evidence**
   - governing documents and repositories;
   - current Git branches, commits, dirty state, and the branch-policy blocker.
3. **Current state**
   - evidence-backed component and data flow;
   - existing format, publication, projection, workspace, squash, and test
     seams;
   - exact repository-relative paths and symbols for important claims.
4. **Target state**
   - portable checkpoint-storage core versus provider adapters;
   - logical identity versus backend materialization identity;
   - native hot path versus cold CDC/CAS history.
5. **Software architecture quality**
   - SRP/SOLID responsibility table;
   - dependency direction and forbidden edges;
   - zero-new-external-dependency proof and internal dependency-edge delta;
   - narrow ports and shared contract tests;
   - coupling and change-impact analysis for Docker, Firecracker, and WASM;
   - current architectural defects and justified disruptive changes;
   - transitional-adapter deletion ledger;
   - Phase 2 consumer contract and Phase 3 provider contract.
6. **`/eos` storage evolution**
   - verified current full `/eos` tree, including both existing scratch roots;
   - target tree;
   - stage-by-stage storage delta;
   - the migration from the global namespace-execution scratch root to
     workspace-session-scoped `executions/`;
   - authority, lifecycle, recovery, and physical-space category for every
     persistent or staging entry.
7. **Resulting plan tree**
   - the complete generated document tree;
   - the cumulative proposed source/test tree at Phase 1 completion.
8. **Stage table**
   - stage, objective, prerequisites, authoritative path, migration mode,
     deliverables, proof tier, focused E2E proof, benchmark proof, memory
     proof, dependency/portability proof, and rollback.
9. **Dependency graph**
   - a Mermaid DAG showing hard dependencies and safe parallel work.
10. **Rollout-mode and compatibility matrix**
   - legacy and new formats, read/write authority, fallback, mixed roots,
     restart behavior, and rollback for every stage.
11. **Global invariants**
   - correctness, durability, identity, leases, OCC, blame, atomic exposure,
     bounded memory, lifecycle reclamation, bounded queues, native execution,
     zero new external dependencies, and portability.
12. **Global time and space budgets**
    - notation and the exact normative gates inherited from preparation
      document 04;
    - baseline, warm, peak, logical-release, settled, and repeated-steady-state
      memory definitions;
    - no invented weakening of those gates.
13. **Memory lifecycle and reclamation**
    - ownership graph and resource-lifecycle inventory;
    - global cache, registry, queue, worker, permit, mapping, and descriptor
      bounds;
    - control/candidate warmup and quiescence rules;
    - stage-by-stage peak, settled, first/last-window, and slope evidence;
    - success, failure, timeout, cancellation, retry, teardown, and recovery
      release paths; and
    - separation of process-memory reclamation from LayerStack durable-object
      GC.
14. **Dependency and portability proof**
    - baseline and target resolved dependency graph with an external delta of
      exactly zero;
    - frozen host-OS/version, CPU-architecture, and Docker-version release
      triples;
    - versioned Linux-image capability profile and pinned
      index/platform-manifest digests;
    - qualified, contract-tested, designed-compatible, and unverified matrix;
    - scalar/SIMD determinism and fallback matrix;
    - target-image userland independence; and
    - provider-specific code isolation and Phase 2/3 reuse.
15. **Acceptance traceability**
    - map every requirement from preparation documents 01–04 to the first
      stage that measures it, the stage where it becomes gating, the final
      regression stage, and its evidence artifact.
16. **Evidence and artifact map**
    - fixtures, JSON schemas, reports, tree digests, resource samples,
      memory-lifecycle samples, dependency snapshots, portability matrices,
      benchmark results, and retention location.
17. **Implementation and commit strategy**
    - proposed implementation slices after branch policy is resolved;
    - no mixed refactor/behavior/benchmark commits without justification.
18. **Rollout, migration, and rollback**
    - activation sequence, mixed-root support, crash/restart, soak, rollback,
      and legacy retirement.
19. **Risks and open decisions**
    - owner, blocking effect, evidence needed, and deadline or decision stage.
20. **Final Phase 1 go/no-go gate**
    - all correctness gates before performance;
    - normative Docker Desktop + Ubuntu qualification statement;
    - honest cross-host and cross-image portability status.

Use this stage table shape:

| Stage | Objective | Prerequisites | Authority/mode | Proof tier | Deliverables | Focused E2E proof | Benchmark proof | Memory proof | Dependency/portability proof | Rollback |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Add a deferred-evidence ledger. `Deferred` means not yet tested; it must never
be presented as `passed`.

## Required output: every `stage_NN_<slug>/spec.md`

Every stage specification must use the following sections. Do not replace
concrete design with a prose milestone.

### 1. Stage contract

- status, dependencies, owners or affected crates;
- one-sentence objective;
- user-visible or system-visible outcome;
- explicit scope and non-goals;
- entry conditions;
- exit gate; and
- rollback point.

### 2. Current evidence

Identify the current files, symbols, tests, formats, and behavior this stage
changes or preserves. For every current-state claim, provide the repository,
repository-relative path, symbol, and stable line number where practical.

Mark statements as:

- `observed`;
- `proposed`;
- `inferred`; or
- `open`.

### 3. Resulting file and folder structure

Show the exact expected tree after the stage. Annotate every path as:

- `[add]`;
- `[modify]`;
- `[remove]`; or
- `[unchanged contract]`.

Separate product, configuration, Rust integration tests, E2E tests, benchmark
presets, fixtures, schemas, and documentation. Never place test support inside
production `src/` merely to make a stage testable.

Show a second, separate resulting runtime-storage tree rooted at `/eos`.
Include the full `/eos/layer-stack` state, the complete applicable
`/eos/workspace/<workspace_session_id>/` scratch state, the status of the
legacy `/eos/namespace_execution` root, and a concise delta from the preceding
stage. Apply every ownership, authority, lifecycle, durability, identity,
bound, and physical-space annotation required by the `/eos` storage-view
contract above.

### 4. SRP, SOLID, and coupling design

Provide:

- current architecture defects and integrity risks;
- target architecture and why a smaller change is insufficient;
- the required component responsibility table;
- portable-core, orchestration, persistence, and provider-adapter boundaries;
- dependency direction and forbidden dependencies;
- before/after direct, transitive, feature, system-tool, and runtime-service
  dependency graph, with an external delta of exactly zero;
- narrow trait/port signatures and shared contract-test ownership;
- construction and dependency-injection flow;
- error translation boundaries;
- which types remain concrete and why;
- the responsibility and evidence for each new abstraction;
- cycle and “god object” audit;
- the three required future-extension change-impact exercises; and
- Phase 2 branch/checkpoint/MCTS consumer compatibility;
- Phase 3 provider-adapter compatibility;
- host-OS, CPU-architecture, and Linux-image compatibility impact;
- target-image shell/userland/libc independence;
- transitional components and their removal stage; and
- a stage-local SOLID review checklist.

Demonstrate that storage layout details do not leak into logical domain types
and that Docker/OverlayFS details do not leak into portable checkpoint
identity or CAS rules.

Include a dependency-delta table:

| Manifest/graph | Baseline packages/features/edges | Resolved package/version delta | Feature delta | Direct external edge delta or relocation | System/runtime delta | Internal edge change | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

Every resolved-package, feature, additive-external-edge, and system/runtime
delta must be `none`; an edge relocation must identify the removed and added
manifest entries and preserve the product-wide edge count. Include a
portability impact table:

| Boundary | Host/image assumption before | Assumption after | Portable core or provider adapter | Evidence now | Deferred matrix evidence |
| --- | --- | --- | --- | --- | --- |

Do not call an unexecuted platform `qualified`.

### 5. Type, class, and field design

Rust does not use conventional classes, so “class and field” means the exact
struct, enum, trait, error, alias, and configuration design.

For every new or modified type, specify:

- status: `new`, `modified`, or `unchanged`;
- owning crate and module;
- visibility;
- responsibility and why the existing owner cannot already provide it;
- exact Rust field name and type;
- ownership and lifetime;
- allocation and reclamation owner, including `Arc`/`Weak` edge direction;
- default and validation;
- invariant;
- persisted, serialized, cached, or transient status;
- collection, cache, registry, queue, or buffer capacity and byte bound;
- normal, cancellation, error, retry, and shutdown release behavior;
- versioning and compatibility impact;
- error behavior; and
- thread-safety or concurrency assumptions.

Show important function and trait signatures, including input/output types and
errors. Distinguish public product APIs from internal interfaces. State which
existing types and interfaces deliberately remain unchanged.

Do not invent a trait, service, manager, registry, or wrapper until current
source proves the abstraction is needed.

### 6. Data and compatibility design

Specify:

- logical root and object schemas;
- domain-separated typed hashes;
- chunk and file descriptors;
- on-disk layout and locator rules;
- journals, transactions, fsync, and atomic rename/exposure;
- format versions and golden vectors;
- explicit integer widths, byte order, path-byte rules, canonical ordering,
  and host/CPU-independent encoding;
- legacy readers and mixed-root behavior;
- migration and downgrade behavior;
- provider-neutral identity fields;
- provider-specific locator/materialization fields;
- scalar versus accelerated implementation equivalence where applicable; and
- corruption detection and quarantine.

Do not mutate existing v1 fixtures or identities in place. Explain whether a
new logical `RootId` is introduced alongside the current physical
manifest-root hash.

### 7. Workflow and failure semantics

Describe the happy path and all relevant failure paths:

- publication and OCC;
- retry and idempotency;
- hydration/materialization;
- lease acquire/release;
- cancellation;
- daemon crash and restart;
- disk full;
- corrupt/truncated object or index;
- squash build, commit, and remount;
- retention, GC, and pack evacuation; and
- rollback to the prior stage.

Define concurrency bounds, worker ownership, queue limits, byte permits,
deadlines, and backpressure. No complete file, tree, history, or global index
may be required in application memory.

Include the required memory-resource lifecycle table. Define the exact
quiescence condition for the stage, who cancels and joins each worker, how
permits and registrations are released, how terminal-retained execution
records are bounded and evicted, and why no strong ownership cycle or detached
work can retain a workspace, publication, materialization, or GC transaction.

### 8. Complexity and performance contract

Provide a table for every operation introduced or affected:

| Operation | Inputs | Expected time | Worst-case time | Peak app memory | Temporary disk | Settled physical disk | I/O pattern |
| --- | --- | --- | --- | --- | --- | --- | --- |

Use the notation in preparation document 04. Explain all amortized claims and
worst cases. Include setup, cleanup, journals, indexes, slack, staging, native
carriers, and metadata in space accounting.

Physical space must be calculated as the complete applicable storage envelope,
not CAS payload alone:

```text
L_hot + H_cold + ΣU_active + P_staging + M
```

Copy all applicable numeric targets and hard ceilings exactly from preparation
document 04, including:

- fixed SeqCDC profile and boundary constraints;
- warm, cold, publication, command, file, PTY, and squash gates;
- RSS, buffer, queue, worker, cache, and byte-semaphore bounds;
- native-carrier depth and temporary-space limits;
- unique-history and total physical-space gates;
- pack, GC, compaction, lease, and recovery limits;
- no operation longer than 60 seconds; and
- no candidate/baseline qualification pair longer than five minutes.

Give every inherited gate one of exactly three states:

- `stage-gating`: measurable now and required for this stage to pass;
- `deferred-to-stage_NN` or `deferred-to-final`: applicable, but its
  capability, corpus, sample size, or qualification evidence belongs to the
  named later stage; or
- `not-applicable`: the operation is genuinely absent and unaffected, with a
  specific reason.

Never label a later-measurable gate `not-applicable`. Never describe a deferred
gate as passed.

For every affected operation, also state its memory working-set formula,
which terms are shared versus per-operation, what reaches the active peak,
what may remain at warmed idle, what must be released at quiescence, and how
concurrency multiplies the bound. Peak-memory compliance does not replace
settled-memory and repeated-cycle stability.

### 9. Diagrams

Include at least:

1. a Mermaid component/dependency diagram showing inward dependency direction
   and ports/adapters;
2. a Mermaid data-flow diagram showing logical and physical storage under
   `/eos`; and
3. a Mermaid sequence, state-machine, or crash-recovery diagram.

Use additional diagrams only when they make ownership, state, compatibility,
or concurrency materially clearer. Show the legacy/candidate authority and
the transaction visibility boundary.

### 10. Implementation sequence

Give a file-by-file, dependency-ordered implementation sequence. Each step
must state:

- files and symbols changed;
- behavior added;
- compatibility retained;
- focused Rust test or static check;
- E2E or benchmark evidence enabled; and
- safe checkpoint/rollback.

Separate refactoring required to expose an existing seam from behavior
changes. Architecture-driven refactoring is in scope when it has a documented
defect, dependency in this plan, compatibility bridge, proof, and removal
strategy. Avoid unrelated cleanup.

### 11. Observability

Define structured, bounded evidence needed to prove the intended route, such
as:

- storage mode;
- write authority and read source;
- fallback count and reason;
- shadow comparison count and mismatch count;
- bytes scanned, hashed, reused, newly retained, read, and written;
- live and high-water owned bytes, buffers, tasks, workers, queues, permits,
  mappings, file descriptors, caches, and registries;
- logical-cleanup completion and quiescence duration;
- hydration classification and reconstructed bytes;
- root/materialization generation;
- lease/GC decisions; and
- process RSS, anonymous/file-backed RSS where available, cgroup
  current/peak memory, first/last settled-window delta and slope, and
  allocated disk.

Counters and logs must not leak unbounded path or chunk cardinality. Avoid log
scraping as primary E2E proof when a structured result or inspection seam can
exist.

### 12. Completion checklist

List:

- implementation deliverables;
- SRP/SOLID and dependency-boundary review;
- `/eos` before/after layout and lifecycle verification;
- format and compatibility proof;
- focused correctness proof;
- the smallest stage-local E2E route proof, when externally reachable;
- tiny-benchmark proof;
- resource-bound proof;
- memory ownership, logical-release, and repeated-cycle stability proof;
- zero-new-external-dependency and host/image portability proof;
- failure/recovery proof;
- documentation and artifact links; and
- unresolved items explicitly deferred to later stages.

## Required output: every `stage_NN_<slug>/e2e_test.md`

Each E2E plan must be executable by an implementer without guessing. Include:

### 1. Stage-local test objective

- capability and risks under test;
- invariants;
- why the tests are runnable before later stages exist;
- authoritative and comparison paths;
- exact feature/configuration/observability seam;
- what remains deferred.

For every non-final stage, label the document `POC proof tier`. Limit its
required execution to the smallest focused set that can falsify the stage.
List broader regression and qualification cases as final-stage work, not as
current exit requirements.

If there is not yet a reachable packaged-product behavior, require:

1. focused Rust integration, golden, property, or transaction proof;
2. a tiny correctness/performance benchmark; and
3. a deferred public E2E case assigned to the exact later stage that creates
   the packaged route.

Do not introduce a premature production API, shadow path, or observability
route solely to satisfy E2E. If the current stage does introduce a reachable
packaged shadow or candidate route for architectural reasons, then require the
smallest structured-observability proof through that real route.

No stage may depend on a later stage merely to pass its own exit gate.

### 2. Existing assets to reuse

List existing tests, helpers, fixtures, digests, samplers, gateway custody
patterns, and benchmark presets with exact paths. Prefer:

- public CLIs and the Docker gateway for behavioral proof;
- typed E2E declarations with stable IDs;
- explicit validation checkpoints and structured evidence;
- temporary generated configuration and safe gateway restoration;
- existing export/tree/archive digests;
- existing squash timing breakdowns;
- existing stress storage measurements;
- existing resource samplers; and
- tracked-ID, run-scoped cleanup.

Docker inspection is acceptable for outside-observation facts such as
allocated container size where an existing approved seam uses it. It must not
replace public product behavior assertions.

### 3. Resulting test tree

Show exact `[add]`, `[modify]`, and `[reuse]` paths for:

- Rust integration and golden tests;
- external E2E cases and specifications;
- harness helpers;
- benchmark presets or corpus manifests;
- schemas and fixtures; and
- machine-readable evidence.

Also show the expected `/eos/layer-stack` tree before the test, at its
visibility boundary, after success, after each injected failure, and after
cleanup. For a stage that affects runtime scratch, show the corresponding
workspace-session tree and legacy namespace-execution root at the same
boundaries. State which paths may be inspected from outside as implementation
evidence and which behavior must be proven through public CLIs.

### 4. Typed E2E case catalog

Use a table:

| Stable ID | Tier | Capability/mode | Setup | Public action | Correctness assertions | Time metric | Disk metric | Memory-lifecycle metric | Dependency/portability evidence | Timeout | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

For each proposed test, specify the complete `@e2e_test` declaration metadata:
stable ID, title, description, features, validations, validation features,
execution surface, owner, timeout, and pytest markers.

Tag every case with one execution disposition:

- `run-now-focused`;
- `run-now-tiny-bench`;
- `planned-final`; or
- `deferred-to-stage_NN`.

Keep `run-now-focused` deliberately small for intermediate stages. The final
stage promotes all required `planned-final` cases into its executed
qualification set.

Distinguish:

- a test execution timeout;
- a diagnostic tiny-benchmark threshold; and
- a normative acceptance target.

They are not interchangeable.

### 5. Correctness and failure matrix

Cover the stage-applicable subset of:

- empty, short, boundary-sized, and large inputs;
- deterministic chunk boundaries and reconstruction;
- arbitrary streaming feed splits producing identical output;
- localized insert, delete, replace, rename, mode, symlink, whiteout, opaque
  directory, sparse file, and no-dedup binary behavior;
- duplicate object idempotency and typed-hash separation;
- legacy versus candidate tree/content/metadata equivalence;
- mixed pre- and post-migration roots;
- concurrent disjoint and conflicting publication;
- stale OCC writer;
- lease held during squash, compaction, and GC;
- fault before and after journal, object, locator, root, and manifest
  visibility boundaries;
- daemon restart, retry, cancellation, and disk full;
- corrupt, missing, truncated, or mismatched objects;
- fallback permitted versus strict no-fallback mode;
- zero silent shadow mismatch;
- cleanup of sandbox, session, lease, staging, journal, and orphan objects; and
- workspace-session transcript isolation for implicit, explicit, concurrent,
  terminal-retained, cancelled, and restarted command lifecycles;
- command-owner release before recursive workspace-session deletion;
- bounded, safe reaping of stale legacy `/eos/namespace_execution` entries
  without touching another session; and
- identity-preserving squash and rollback;
- logical resource release and settled-memory stability after repeated
  success, cancellation, timeout, and injected-failure cycles;
- scalar SeqCDC golden boundaries and, when acceleration exists,
  scalar-forced versus accelerated identity equivalence;
- storage behavior without a target-image shell, libc utility, package
  manager, or helper binary; and
- the stage-applicable host-OS, CPU-architecture, and Linux-image portability
  matrix.

A generic successful command is insufficient. Prove which storage route served
it. In strict candidate tests require `fallback_count = 0`.

### 6. Tiny correctness and benchmark loop

Create a tiny, deterministic, developer-feedback loop for every stage. Reuse
the existing benchmark laboratory and operation-timing artifacts. Do not
create an unrelated microbenchmark scheduler.

Even a schema-, type-, or compatibility-only stage must benchmark its smallest
relevant primitive, such as deterministic encode/decode/verify time, artifact
size, allocation/RSS behavior, fixture count, or bounded index access. Do not
use “no end-to-end route yet” to omit the tiny benchmark.

The tiny loop is a regression sentinel, not final qualification. It should
normally finish in 30–60 seconds and must declare an exact cap that respects
the 60-second per-operation limit.

Use the same host, filesystem, cache treatment, seed, corpus, and configuration
for control and candidate. Run them as paired, alternating or interleaved
samples. Use:

- pre-generated deterministic input;
- at least one warmup and at least five measured pairs for the smallest loop;
- preferably 3–5 warmups and at least 10 alternating repetitions when the
  sub-minute budget permits;
- raw per-sample JSON;
- absolute values and candidate/control ratios; and
- no p95 claim from an insufficient sample count.

The minimum applicable tiny corpus should include:

- empty/no-op behavior;
- a 1 KiB localized edit in a deterministic 1 MiB file;
- a deterministic 1 MiB incompressible file;
- 100–1,000 small files totaling about 1 MiB; and
- repeated overwrites at small history depths such as 1, 8, and 32.

As stages mature, reuse or extend the existing workload families for a larger
file, repeated churn, hundreds or thousands of small files, binary/minified
content, and varying native-layer depth.

Collect where applicable:

- end-to-end and component elapsed time;
- throughput, operations per second, p50, and p95 only with sufficient
  samples;
- bytes scanned, read, written, hashed, reused, and newly retained;
- unique CAS payload and logical/allocated physical bytes;
- chunk, object, file, layer, pack, journal, and staging counts;
- warm/cold materialization and reconstructed bytes;
- publish, hydrate, activate, mount, remount, squash, and cleanup latency;
- peak and final RSS, cgroup memory where available, and idle-adjusted RSS;
- live and high-water owned bytes, workers, tasks, queues, byte permits,
  mappings, descriptors, caches, and registries;
- exact tree/content/metadata digest and root identity; and
- all fallback and mismatch counters.

For `/eos`, record allocated bytes by relevant subtree rather than only one
aggregate. At minimum separate legacy native layers, portable
roots/objects/packs, indexes/metadata, staging/journals, rebuildable native
materializations, workspace OverlayFS scratch, execution transcripts, and
legacy namespace-execution residue when those categories exist in the stage.

Label every result `measured`, `derived`, `estimated`, or `unknown`.

Tiny thresholds must be coarse diagnostics derived from preparation document
04 and baseline noise. Label them non-normative. They may catch gross
regressions but may not weaken, replace, or claim to pass the full
qualification gates.

### 7. Memory-stability and reclamation test

Every stage must state whether it changes a runtime allocation, ownership,
cache, registry, queue, task, worker, mapping, descriptor, permit, or cleanup
path. When it does, extend the tiny loop with a focused leak/retention
sentinel. When it does not, identify the unchanged ownership boundary, reuse
the nearest applicable sentinel, and record the full matrix as deferred to
the final stage.

Run the sentinel against one long-lived test process. Use the packaged
daemon/container and do not restart it between measured iterations when a
packaged route exists. For an internal-only stage, use the long-lived Rust
integration-test or benchmark process without inventing a daemon route. Use
the same host, inputs, concurrency, cache treatment, warmup, sampling interval,
and operation order for control and candidate. Exercise the applicable subset
of:

- repeated successful operations;
- the stage's primary cancellation, timeout, or injected-error path;
- explicit cleanup and bounded polling to the declared quiescent state; and
- teardown of the affected primitive, sandbox, workspace session, publication,
  materialization, squash, or storage-GC owner.

Record the sequence:

```text
idle baseline -> warmed idle -> each active peak -> each settled sample
```

At minimum collect, where available:

- process RSS and its anonymous/file-backed split;
- cgroup current and peak memory;
- component live-owned bytes and high-water bytes;
- active and retained buffer, queue, task, worker, permit, mapping, file
  descriptor, cache, registry, lease, and transaction counts;
- quiescence latency;
- first and last settled-window medians, their delta, and a robust
  post-warmup slope with sample count and predeclared control noise band; and
- input size, retained-history depth, concurrency, result status, and
  cleanup-path label for every sample.

The stage-local POC sentinel must fit within the existing 30–60 second tiny
loop; do not add a broad stress campaign. Declare the repetition count and
noise rule before executing the candidate. The final stage must run the full
memory matrix and exact gates from preparation document 04 plus a sustained
repeated-lifecycle test. Give each matched scenario or scale-matrix point its
own five-minute raw/candidate invocation and required repetitions as
preparation document 04 specifies; declare the aggregate suite budget
separately.

An intermediate-stage POC pass requires:

1. logical ownership, permits, queues, tasks, mappings, descriptors, and
   bounded registries/caches for the changed path return to their expected
   quiescent values; and
2. the short physical-memory sentinel stays within its predeclared coarse
   control noise band and does not breach any memory ceiling already
   classified `stage-gating`.

That POC verdict is diagnostic and cannot claim the full normative memory
contract. The final-stage pass additionally requires every
preparation-document-04 peak, settled, scaling, repetition, and hard-cap gate,
with no unexplained positive settled-memory trend beyond the frozen control
noise band.

Do not infer “no leak” from RSS alone, and do not excuse growing live-resource
gauges because RSS is flat. Allocator arena retention or kernel page cache
must be attributed, not guessed. A process/container restart, manual cache
purge, `malloc_trim`, or alternate allocator cannot be used to make the test
pass. If a focused heap diagnostic is needed, keep it out of the production
runtime contract and preserve its bounded artifact.

The final report must distinguish:

- `bounded-and-released`;
- `bounded-retained-by-design`;
- `allocator-or-page-cache-retained`;
- `suspected-leak`;
- `confirmed-leak`; and
- `measurement-unavailable`.

`suspected-leak` and `confirmed-leak` are stage blockers when they touch the
changed path. `Measurement-unavailable` is a blocker for a `stage-gating`
metric and a no-go for any normative final-stage metric. An unavailable
optional source may use the declared independent fallback; a genuinely
later-stage metric is labeled deferred, not unavailable and not passed.

### 8. Dependency and portability proof

Every stage must record the resolved external dependency graph before and
after the change. The pass condition is an identical resolved external
package/version set, identical enabled external feature set, no growth in the
product-wide direct external edge multiset, and zero added system tools,
runtime services, or target-image helpers. Record an allowed relocation of an
existing external edge and all internal workspace-edge changes separately;
run the repository's existing cycle/forbidden-edge checks.

When a stage changes a portable format, chunker, storage path, or Docker
adapter, include the smallest applicable differential proof for:

- the scalar SeqCDC golden corpus and, only when an accelerated path exists,
  scalar-forced versus accelerated equivalence;
- deterministic output across available host CPU architectures;
- host-native path independence;
- glibc, musl, minimal/distroless, or shell-less image behavior reachable at
  that stage; and
- no invocation of a target-image shell or helper for storage operations.

Keep intermediate execution focused: one scalar golden proof, one
scalar/accelerated differential when acceleration exists, and one newly
affected image/adapter case are sufficient unless the stage risk requires
more. If acceleration is planned for a later named stage, mark its
differential `deferred-to-stage_NN`; if acceleration is explicitly excluded,
mark it `not-applicable` with that reason. Assign the complete frozen
release-triple and image-capability matrices to the final stage. Pin both the
OCI index digest and resolved platform-manifest digest for
multi-architecture fixtures. Label unavailable hosts/images `unverified`;
never convert missing evidence into a pass.

An `unverified` required-release row is a final portability/production no-go.
An unverified informational row blocks only a support claim for that row. The
pinned Ubuntu performance result may be reported independently, but it does
not satisfy the cross-host portability gate.

For a shell-less image, use existing public workspace/file APIs and exact
tree/metadata evidence. Do not add an executable to the image merely to make
the portability test possible.

### 9. Focused and final-stage commands

Provide verified commands for:

- focused Rust formatting, lint, unit, and integration checks;
- resolved dependency-graph and lockfile zero-delta check;
- the smallest focused E2E node;
- the tiny benchmark;
- artifact validation;
- final-stage affected regression;
- final-stage declared host/image portability matrix; and
- final-stage full Phase 1 qualification.

For intermediate stages, mark the final three command groups as `do not run in
this stage`. Do not require a cumulative or full-suite run merely because a
stage finishes. Run broader tests earlier only when a high-risk shared
boundary cannot be responsibly validated by a focused test, and document that
specific reason and expected time budget.

Do not invent a benchmark command before inspecting the current benchmark CLI.
State working directory, required environment variables, rebuild/reuse mode,
input preset, output path, and expected duration.

When implementation begins, follow the E2E repository's feature-by-feature,
append-only report discipline. Do not rerun already-passing broad suites
without a stated reason. Record build-lock wait separately from execution wall
time.

### 10. Metrics and evidence contract

For each metric, state:

- definition and unit;
- numerator and denominator;
- measurement source;
- sampling interval;
- warmup and sample count;
- aggregation;
- baseline/control;
- target and hard ceiling;
- missing-data policy;
- machine-readable field name; and
- artifact path.

Resource evidence must be bounded; use a ring, reservoir, or streamed
aggregation rather than retaining every high-frequency sample.

Memory evidence must preserve bounded raw or aggregated samples sufficient to
recompute peak, settled windows, first/last delta, and slope without retaining
an unbounded time series in the test process. State whether each value comes
from the daemon process, container cgroup, kernel page-cache accounting, or
test runner; never mix those scopes in one unlabeled series.

For total space, include active native state, retained unique history, active
uppers, staging, journals, indexes, pack slack, and other metadata. Do not
report “13.9% more unique payload” as “13.9% more disk.”

### 11. Stage exit verdict

Define:

- mandatory pass cases;
- allowable diagnostic warnings;
- disqualifying correctness, durability, memory, or route failures;
- logical-resource return, physical-memory cap, and repeated-cycle trend
  verdicts;
- zero-new-external-dependency and applicable portability verdicts;
- artifact completeness checks;
- cleanup proof;
- rerun policy;
- rollback trigger; and
- exact later-stage evidence that remains deferred.

For an intermediate stage, the mandatory cases are only its focused POC proof
set and tiny benchmark. For the final stage, the mandatory cases are the full
Phase 1 qualification set.

## How to prove stages before full migration

Every stage must use at least one real incremental proof mechanism:

- a pure internal primitive with golden/property Rust integration tests;
- legacy-authoritative shadow production;
- dual-write or shadow-write with read-only canonical comparison;
- a new reader over legacy-produced data;
- private candidate materialization followed by exact tree/metadata digest
  comparison;
- a compatibility adapter that preserves the previous stage;
- per-sandbox or per-root strict opt-in;
- candidate-authoritative operation with legacy shadow verification; or
- feature-off behavior proven equivalent to the frozen baseline.

Use real packaged daemon and CLI paths for stage completion wherever a public
behavior exists. Mocks can support a focused test but cannot be the only proof
of transaction, filesystem, restart, or resource behavior.

Instrument before relying on a new route. A stage that introduces shadow mode
must prove the shadow task ran and completed. A dual-read stage must prove both
trees were compared. A strict candidate stage must prove no fallback occurred.
A GC stage must prove a leased old root remains usable. A squash stage must
prove logical `RootId` and OCC publication generation remain unchanged while
materialization generation advances.

## Hard prohibitions

Reject or redesign any stage that requires:

- a full-file, full-tree, full-history, or global-index application buffer;
- unbounded mmap, queue, cache, worker set, artifact collection, or retry;
- accumulating emitted chunks before hashing/writing/dropping them;
- allocator behavior or eventual GC as the memory bound;
- claiming that Rust's lack of tracing GC proves the absence of memory
  retention;
- a strong `Arc` ownership cycle, unbounded terminal registry, detached
  worker, orphaned future, or cleanup path that relies on process exit;
- using daemon/container restart, `malloc_trim`, allocator replacement, an
  arbitrary sleep, or manual page-cache eviction to make a memory test pass;
- treating flat RSS as sufficient when live-resource ownership grows, or
  treating allocator/page-cache retention as a heap leak without attribution;
- conflating LayerStack durable-object GC with process-memory reclamation;
- any new resolved external package/version, external feature activation,
  additive direct external manifest edge, vendored library, system tool,
  runtime service, or target-image helper;
- requiring x86/SIMD support, a target-image shell, libc utility, package
  manager, or network access for correctness;
- host-native path rules, CPU word size, endianness, filesystem ordering, or
  provider locators in portable identity;
- calling a host OS, CPU architecture, or Linux image qualified without
  executed evidence;
- SQLite or another external database/service;
- a new resident daemon, sidecar, Docker plugin, target-image helper, FUSE,
  kernel module, capability, or privilege;
- required reflinks;
- CAS lookup or reconstruction in normal command/file/PTY/stdin hot paths;
- partial materialization visibility;
- one resident sandbox or native materialization per inactive future branch;
- blame derived from chunk ownership;
- provider locators or Linux encodings in logical root identity;
- a destructive bulk rewrite as the initial migration;
- silent candidate fallback in a passing candidate-path test;
- performance claims based on modeled or estimated data;
- a test-only production API placed in `src/`;
- a module or type with multiple unrelated reasons to change;
- a provider adapter that owns portable root, publication, lease, or GC
  policy;
- a Phase 1 `/eos/attempts` directory or another filesystem identity that
  prematurely makes the future `ExecutionAttempt` control-plane model the
  owner of current runtime scratch;
- a final target that retains an independently configured global
  `/eos/namespace_execution` scratch root;
- deletion of a workspace-session parent before its active commands are
  cancelled and joined and its retained transcript owners are released;
- a portable core type that imports Docker, OverlayFS, mount, or `/eos`
  locator details;
- a broad context/service interface that forces unrelated capabilities on
  callers;
- preservation of a known leaky or cyclic architecture solely to minimize the
  diff;
- a big-bang rewrite with no mixed-version bridge, focused proof, or rollback;
- a transitional adapter with no planned deletion stage;
- an unrelated refactor without a stage dependency;
- an unverified file, symbol, command, or numeric gate; or
- `TODO`, `TBD`, or placeholder stage content without a named decision owner,
  blocking effect, and evidence required.

Correctness, OCC, leases, recovery, namespace isolation, bounded memory, and
atomic visibility precede performance and storage scoring.

## Link and document conventions

- `implementation/index.md` links relatively to every stage's `spec.md` and
  `e2e_test.md`.
- Every stage document links back to `../index.md`.
- A stage's `spec.md` and `e2e_test.md` link to each other.
- Stage documents link to preparation sources through `../../prep/`.
- Use repository-relative source paths in prose, paired with the absolute
  repository root once per document.
- Use canonical absolute roots in executable E2E commands because the harness
  requires them.
- Ensure every local Markdown link resolves.
- Use Mermaid syntax supported by the documentation renderer.

## Required final validation

Before reporting completion:

1. verify only the requested planning-document paths changed;
2. preserve all pre-existing dirty work;
3. run Markdown and local-link checks available in the repository;
4. check every stage has both required files;
5. check stage numbers and dependencies are contiguous and acyclic;
6. verify every preparation 01–04 acceptance requirement appears in the
   traceability matrix;
7. verify every stage can pass its own exit gate without a later stage;
8. verify all proposed commands exist and use the correct working directory;
9. verify numeric gates exactly match preparation document 04;
10. verify no modeled benchmark result is described as measured;
11. verify every stage includes the SRP/SOLID responsibility and dependency
    audit;
12. verify current, per-stage, and target full `/eos` trees are shown and
    lifecycle-annotated, including the workspace-scoped execution-scratch
    migration and eventual absence of `/eos/attempts` and the global
    `/eos/namespace_execution` root;
13. verify every disruptive change names its defect, benefit, bridge,
    rollback, and transitional-code deletion stage;
14. verify the final architecture satisfies the Phase 2 consumer and Phase 3
    provider compatibility contracts without duplicating storage truth;
15. verify no intermediate stage requires a broad/full E2E pass;
16. verify the final stage owns cumulative E2E and normative qualification;
17. verify every allocating or asynchronously retaining stage contains a
    resource-lifecycle inventory, bounded ownership graph, quiescence
    definition, and focused repeated-cycle memory sentinel;
18. verify final memory evidence separates logical release from physical RSS
    and cgroup stability, covers success and failure cleanup without restart,
    and applies every normative preparation-document-04 gate;
19. verify LayerStack storage GC, squash, and compaction remain bounded in
    application memory and do not materialize a global live set;
20. verify identical resolved external package/version and enabled-feature
    sets, no growth in direct external edges, and zero new build, test,
    system-tool, service, or target-image dependencies;
21. verify scalar and all available accelerated SeqCDC paths produce identical
    boundaries and identities, with scalar fallback on unsupported CPUs;
22. verify the final frozen release-triple and image-capability matrices
    distinguish normative qualification from contract-tested,
    designed-compatible, and unverified rows, pin both OCI digests where
    applicable, and treat every unverified required-release row as a no-go;
23. verify no storage operation requires target-image userland and all
    provider-specific OS behavior remains behind the Docker adapter;
24. verify each selection or RSS scale-matrix point uses its own matched
    five-minute invocation and required repetitions, with a separate aggregate
    suite budget rather than one five-minute matrix budget;
25. verify the branch-policy conflict remains explicit; and
26. run `git diff --check` for the documentation repository.

## Completion report

Return:

- links to `implementation/index.md` and every stage directory;
- the number of stages and critical path;
- stages that may proceed in parallel;
- major architecture changes and why they are justified;
- transitional components and their removal stages;
- the resulting Phase 2 and Phase 3 compatibility seams;
- the first stage that writes candidate artifacts;
- the first strict no-fallback candidate stage;
- the stage that makes the candidate authoritative;
- the stage that first permits legacy retirement;
- memory-lifecycle gates, leak/retention verdicts, and any unavailable metric;
- proof that the external dependency delta is zero;
- qualified, contract-tested, designed-compatible, and unverified host/image
  matrix rows;
- the branch-policy decision still required;
- unresolved blockers and their owners;
- validation commands run and results; and
- confirmation that no product, E2E, benchmark, Git branch, commit, or remote
  state was changed.

The task is complete only when the plan is implementation-ready, every stage
is independently testable before the full migration, every acceptance
requirement is traceable to evidence, memory release and repeated-process
stability are explicit, the external dependency delta is zero, host/image
portability claims are evidence-scoped, and every local link resolves.
