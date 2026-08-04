---
status: required-joint-profile-input
authority: source-and-direct-local-dependency-ledger
joint-profile-selection-execution-status: NOT_RUN
accepted-joint-profile-winner-count: 0
depends-on:
  - ARCH-BND-001
  - ARCH-BND-005
  - ARCH-BND-006
---

# Source-layout and dependency-ledger contract

## Status

No source layout is selected. This file turns the pinned workspace into a
mechanically checked input to the `H_PROFILE` tournament. It neither privileges
R0 nor treats a crate, directory, module, DTO, or call as an architecture
boundary. Exact counts remain open until one complete joint profile wins.

## Current anchors are non-exhaustive

These observed anchors are examples that the generated ledger must include;
they are not a hand-maintained complete inventory:

```text
crates/sandbox-runtime/
  operation/             application orchestration and storage-facing calls
  layerstack/            legacy V1 implementation; possible in-place owner
  workspace/             native workspace lifecycle and capture
  namespace-execution/   command/execution effects
  namespace-process/     process/namespace effects
  overlay/               Linux mount effects

crates/sandbox-manager/  manager application; shared-base builder caller
crates/sandbox-provider-docker/
                         provider archive; directly emits V1 seed bytes
crates/sandbox-observability/query/
                         observability DTOs typed to LayerStack
crates/sandbox-daemon/    composition root; LayerStack is currently a dev edge
```

Material source facts that prevent a rename-only design include:

- the Docker provider's `archive.rs` constructs a V1 manifest and workspace
  binding from LayerStack constants and `WorkspaceBinding`;
- the manager's `create_sandbox.rs` directly calls
  `build_shared_workspace_base`;
- workspace `CaptureChangesRequest`, `CapturedWorkspaceChanges`, snapshot, and
  lease DTOs embed LayerStack manifests, changes, and service types;
- observability query ports/responses embed `StackObservation`,
  `LayerDeltaDescription`, and LayerStack byte vocabulary;
- operation code is the largest normal semantic consumer and re-exports
  LayerStack types; and
- the LayerStack package has no direct local workspace dependency in the clean
  pinned tree. Its normal/build consumers are the Docker provider, manager,
  workspace, observability query, and operation packages; the daemon has a
  development-only edge.

The clean pinned e497 tree contains no `mpla-poc`, `layerstack-core`,
EOS-LS3/V2/V3 storage candidate, generation-GC handoff, or storage-helper
package. Historical experiment receipts that mention any such package or edge
are incomparable, non-current evidence. They may motivate a submitted candidate
or a fixture only if the candidate is reconstructed independently against the
pinned tree; they never create a current-source anchor, dependency row, control
edge, or mandatory constructor.

The provider V1 seed, manager base builder, workspace capture DTOs, and
observability DTOs are mandatory named ledger rows. Omitting them is an
incomplete candidate, even if a hand-drawn component diagram looks closed.

## Generated direct-local-dependency ledger

Phase 0 seals a script and invokes it against the pinned tree with locked Cargo
resolution, all frozen target triples, and every frozen feature set. Its input
includes `cargo metadata --locked --format-version 1`, manifest target tables,
and source-reference discovery. For each candidate realization it regenerates:

```text
(consumer package, target, dependency kind, cfg/features,
 provider package, referenced symbols/source sites)
```

for every direct local normal/build/development edge. Normal/build edges form
the scored production graph; development edges are retained separately so a
candidate cannot move production behavior into tests or use a dev-only edge to
claim closure.

The script also materializes the `G_scope` defined by the
[joint-selection contract](architecture-selection.md#finite-reproducible-candidate-universe):
the exact transitive source/caller/dependency/target/feature/DTO/writer/effect/
resource/recovery/route/control closure needed to disposition current behavior.
Any submitted destination or added edge extends that closure before the sealed
cutoff and receives normal generated rows. The sealed neutral admissibility
rules—not a hand-authored package list—define `lawful` and `compatible`; the
generator records every normalized member ID, exact count, and exclusion proof
before outcomes are visible.

Every generated normal/build row and every source reference must have exactly
one disposition:

- `KEEP`: preserve one direct edge; name its narrow contract, unique owner, and
  executable failure after deletion;
- `DELETE`: remove the edge and every source reference; compilation proves no
  forwarding facade or re-export remains;
- `MOVE`: name the exact destination owner and show the old edge, code, and
  authority disappear; or
- `NEUTRAL_DTO`: replace physical/storage/runtime-native types with bounded
  portable facts or an opaque identity owned by the consumer-facing contract;
  the old direct dependency disappears.

The verifier compares the generated row IDs with the disposition ledger in both
directions. A missing row, extra hand-authored row, unresolved destination,
source reference without an edge, edge without source/build justification, or
retained old-plus-new route makes the profile ineligible. The generated input,
script hash, stdout, normalized ledger, and before/after metadata are part of
`H_PROFILE`.

## Mandatory baseline dispositions

The baseline generator instantiates the following row-level dispositions. Each
cell contains exactly one disposition; words after the dash constrain that one
result and do not authorize a second action. A selectable submitted profile may
differ only by supplying a complete alternative ledger and passing the same
hard gates.

### Current normal/build dependency edges

| Generated current edge | `R_LEGACY_CONTROL` | `R0_IN_PLACE` |
|---|---|---|
| Docker provider → LayerStack | `KEEP` — pinned control edge | `NEUTRAL_DTO` — transport only opaque attested seed/install facts |
| manager → LayerStack | `KEEP` — pinned control edge | `KEEP` — one narrow V2 base-build call with a deletion falsifier |
| workspace → LayerStack | `KEEP` — pinned control edge | `NEUTRAL_DTO` — bounded capture facts and opaque generation only |
| observability query → LayerStack | `KEEP` — pinned control edge | `NEUTRAL_DTO` — bounded generic selected-state observations |
| operation → LayerStack | `KEEP` — pinned control edge | `KEEP` — one narrow selected-state owner call |

### Mandatory source responsibilities

| Generated current source row | `R_LEGACY_CONTROL` | `R0_IN_PLACE` |
|---|---|---|
| Docker provider V1 manifest/binding writer | `KEEP` — pinned control source | `DELETE` — provider emits only the neutral V2 seed/install contract |
| manager `build_shared_workspace_base` call site | `KEEP` — pinned control source | `KEEP` — invoke the in-place selected owner |
| workspace selected-state lifecycle orchestration | `KEEP` — pinned control source | `MOVE` — one application owner |
| workspace capture/snapshot/lease DTO definitions | `KEEP` — pinned control source | `NEUTRAL_DTO` — bounded portable facts or opaque identities |
| observability `StackObservation`/`LayerDeltaDescription` DTO definitions | `KEEP` — pinned control source | `NEUTRAL_DTO` — bounded generic observations |

The generator applies `KEEP` to every current control row, not only the anchors
shown above. Its invariant is exact comparator identity; the deletion falsifier
is a pinned-tree/build/output mismatch. The evidence judge owns that ledger.
`R_LEGACY_CONTROL` remains non-V2 and cannot become `H_PROFILE`; its accepted
measurements supply only preregistered comparator endpoints.

The deleted provider V1 writer is absent from `H_RELEASE`; any independently
required legacy decoder belongs to the temporary migration placement axis, not
to the provider. Neutral workspace DTOs
cannot retain a physical manifest, path, lease, selector, locator, or candidate-
generation type. Every generated edge and source row still has exactly one
disposition.

The remaining mandatory topology families are generated from those actual
rows, never from absent or historical package names:

- `R_ROLE_PARTITION[pi]` emits all five accountability partitions
  `A|S|N`, `A+S|N`, `A+N|S`, `S+N|A`, and `A+S+N`. For each partition the
  ledger names the exact owner, source, writer/effect, and dependency changes.
  Every generated partition × placement realization compiles or carries an
  independently checkable `INAPPLICABLE` proof against a Phase-0-frozen rule
  that does not assume separate owners.
- `R_PLACEMENT[o,q]` derives every extant lawful selected-state destination `o`
  and pure-function destination `q` from the generated source/package/call
  graph, including inline and fused placements. It emits an exact disposition
  for each affected row; no package or operation-private placement is
  privileged.
- `R_PACKAGE_DISPOSITION[d]` gives every generated in-scope current package
  exactly one `KEEP`, `DELETE`, or `MOVE` result and a destination where needed.
  It emits every one-package deletion and every compatible multi-package
  fusion/total-fusion set. Each result compiles or carries an independently
  checkable `INAPPLICABLE` proof; a package absent from the pinned tree cannot
  seed this family.
- `R1_ONE_BOUNDARY[s]` starts from every compatible smaller generated ledger,
  replaces only rows mechanically affected by sealed extraction site `s`, and
  emits one row for the new boundary plus its necessity falsifier.
- Each `R_NECESSITY_*` candidate emits rows for every added edge and the exact
  smaller-candidate counterexample that triggered it.

Every resulting cell has one disposition. A family name is never a wildcard
disposition, and no “other consumers” bucket is permitted.

## Dependency laws for every eligible profile

```text
public/composition entry -> declared accountability owner(s)
declared ordering transition -> exactly one selected-state transition
declared ordering transition -> applicable native-effect transition(s)
```

These are call/data transitions, not required package edges. The partition and
placement manifests declare whether their endpoints are distinct, co-located,
or one fused accountability owner. The selected-state transition remains unique
in every case. Migration dependencies are defined once, normatively, by
[the import dependency contract](migration-cutover.md#normative-import-dependency-direction);
this ledger verifies that graph but does not restate or reverse it.

Forbidden:

```text
selected-state transition -> mutable native runtime effect
native runtime-effect transition -> selected-state physical transition/writer
portable identity computation -> persistence, application, runtime, provider, or migration code
steady-state provider/runtime code -> legacy V1 schema writer
one resource owner -> another owner's claims, handles, census, or recovery debt
```

An operation-private or any other fused placement is a generated member, not a
privileged shape. It is eligible when the compiled transition graph preserves
the unique-writer, portable-data, native-effect, and resource laws; co-location
does not itself pass or fail it. No extant package is presumed to be a purity
boundary. A new boundary is eligible only through its frozen necessity
falsifier, and package count alone decides no candidate.

## Production source rules

- Compile exactly one physical implementation. No workload strategy menu,
  compatibility selector, forwarding facade, or duplicate selected-state
  writer survives.
- Add no generic transaction/KV/storage API, aggregate `WorkspaceBackend`,
  repository facade, plugin registry, runtime enum, grouping-directory facade,
  or package solely to host DTOs.
- Candidate algorithms, model checkers, fixtures, benchmarks, and fakes stay in
  tests, benches, or disposable labs, never production `src/`.
- Temporary migration code is a code unit, target, or artifact; a separate
  package exists only if the joint tournament selects it. It is read-only with
  respect to legacy truth, generation-fenced, follows the one normative import
  dependency graph, and is absent from the fully requalified `H_RELEASE`
  artifact after its no-reference proof.
- Native paths, mounts, namespaces, devices, snapshots, provider/runtime brands,
  VM/WASI handles, and physical locators never enter public/core identity.
- Semantic roles do not map to packages, modules, traits, ports, facades,
  registries, processes, or deployables. Algorithms, codecs, hashes,
  canonicalization, and validation are pure functions in the lawful caller
  unless a presealed executable necessity trigger proves exclusive state,
  lifecycle, synchronization, privilege, or resource custody needs an owner.
- `R0_IN_PLACE` has zero mandatory new components, traits, ports, facades,
  registries, packages, processes, or deployables. Any proposed addition is a
  separately generated necessity-triggered topology, not an implicit part of R0.
- Every retained/new source, edge, DTO, worker, package, process, durable fact,
  or authority names an invariant and executable deletion counterexample.

Linux is the first runtime. WASI and Firecracker are disposable conformance
spikes over portable facts, effects, containment, restart, and cleanup. They do
not create a core enum, trait, plugin, facade, package, or deployable without a
second accepted implementation and a necessity proof inside the joint
tournament.

## `H_PROFILE` handoff

Phase 1A compiles every complete pair, regenerates the dependency/disposition
ledger, rejects invalid topologies before measuring performance, and binds the
winning exact source/package/call/helper/process graph with its physical profile
as `H_PROFILE`. Only then may Phase 1B implement `H_FMT`, followed by 1C
`Hstore`, 1D `Hpermanent`, 1E `H_PRECUTOVER`, and 1F `Hqual`.
