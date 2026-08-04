---
status: required-before-implementation
authority: joint-profile-selection-protocol
joint-profile-selection-execution-status: NOT_RUN
accepted-joint-profile-winner-count: 0
accepted-architecture-winner-count: 0
accepted-physical-method-winner-count: 0
depends-on:
  - REQ-COR-004
  - REQ-PORT-002
  - REQ-RES-003
produces:
  - DEC-012
---

# Joint architecture and physical-profile selection

## Current result

`DEC-012` has not run. No topology, source layout, call graph, package graph,
process graph, helper placement, physical method, or implementation count is
accepted. The result must be one exact jointly realized `H_PROFILE` or
`NO_WINNER`; all three accepted winner counts remain zero until then.

The old two-step rule—freeze an architecture and then fit a physical method
inside it—is deleted. Representation, recovery, helper custody, process
placement, resource ownership, and dependency direction can change whether a
topology is valid and how much it costs. Conversely, topology can make a
physical method impossible. Selecting either axis first could exclude the best
valid pair.

## Finite, reproducible candidate universe

Phase 0 first seals `G_scope`: the exact generated source, caller, direct-local-
dependency, target, feature, DTO, writer/effect, resource, recovery, route, and
control closure needed to disposition current LayerStack behavior and every
current public/tool operation or separately dispatched surface. The closure is
derived from the pinned tree, not from package names in this draft. Every
submitted destination or added edge is inserted into `G_scope` before the
cutoff and therefore receives the same generated rows and dispositions; it may
not appear later as an uncounted helper.

Here, `lawful` means only that a placement passes the Phase-0-sealed neutral
compile, target/feature, cycle, unique-writer/effect, portable-data, privilege,
authority, and finite-resource rules. Those rules may not assume separate
owners, a new boundary, an existing package, or R0. Before any correctness or
performance result is visible, the generator emits the normalized member IDs,
exact count, exclusions, and independently checkable exclusion proofs. Thus
“in scope,” “lawful,” and “compatible” cannot be changed after seeing results.

Phase 0 seals all of the following before any result is visible:

1. the pinned source/evidence trees, a signed UTC submission cutoff, the hash of
   the candidate-discovery generator, and the digest of every complete signed
   submission received by that cutoff;
2. the actual current package/target/dependency/source graph generated from the
   clean pinned e497 tree, followed by the finite topology transforms:
   all five `A/S/N` accountability partitions, selected-state-authority
   placement, pure-computation placement, package/file keep/delete/move,
   DTO direction, migration-code placement, helper/privilege custody, call
   direction, and process/deployable placement;
3. normalized graph equivalence, admissibility, structural-dominance, and
   duplicate-collapse rules;
4. the finite `T1`–`T8` physical candidate sets, standard-library/standard-
   primitive incumbents, parameters, and compatibility constraints; and
5. the exact generator for the topology × physical-profile product.

The mandatory universe baseline is not optional:

| ID | Role | Mechanically constructed realization |
|---|---|---|
| `R_LEGACY_CONTROL` | evidence-only, non-V2 control | Generate the exact current graph from e497, then compile and run that tree unchanged with locked dependencies, frozen targets/features, and its current physical stack. Every generated source/dependency row is `KEEP`; any source/build/configuration/graph change invalidates the control. |
| `R0_IN_PLACE` | selectable named V2 witness | Rewrite the existing LayerStack ownership home for V2 selected state, retain the actual current package positions initially, use inline/existing pure functions, and keep application and native effects with their current owners. Its incremental component/package/boundary count is zero. |
| `R_ROLE_PARTITION[pi]` | selectable mandatory five-member family | Emit exactly `A|S|N`, `A+S|N`, `A+N|S`, `S+N|A`, and `A+S+N`. A plus sign means one accountability/reason-to-change owner, not mere co-location. Every member is realized or has an independently checkable `INAPPLICABLE` proof against a frozen rule that does not assume the three-role split. |
| `R_PLACEMENT[o,q]` | selectable actual-source placement family | Derive every extant lawful selected-state destination `o` and pure-function destination `q` from the generated package/source/call graph, including inline/fused placement. Emit every compatible pair; a new boundary is not an implicit destination. Operation-private placement is one generated member, not a privileged special case. |
| `R_PACKAGE_DISPOSITION[d]` | selectable actual-source deletion/fusion family | For every generated in-scope current package, `d` supplies exactly one `KEEP`, `DELETE`, or `MOVE` result and destination. Include each one-package deletion and every compatible multi-package fusion/total-fusion set; each emitted graph must compile or carry an independently checkable `INAPPLICABLE` proof. No historical/non-current package may seed this family. |
| `R1_ONE_BOUNDARY[s]` | selectable finite V2 family | From every Phase-0-enumerated eligible extraction site `s`, apply exactly one boundary to each compatible smaller generated realization. The new edge and its necessity falsifier are explicit; this is not an unnamed design. |
| `R_NECESSITY_*` | selectable triggered V2 family | Generate every larger topology whose sealed executable trigger proves every compatible smaller shape cannot preserve a named invariant; the transform and added edge are fixed before execution. |

The selectable topology generator takes the compatible product of the partition,
placement, package-disposition, boundary, DTO, migration, helper/privilege,
call-direction, and process/deployable axes. It then takes the product with the
compatible `T1`–`T8` physical profiles. `R0_IN_PLACE` is a named zero-addition
witness inside that product, not a sequentially selected architecture. Exact
graph duplicates may be collapsed only by the sealed equivalence rule.

`R_LEGACY_CONTROL` is not a V2 candidate and cannot become `H_PROFILE`. It
supplies preregistered current-product comparator endpoints and a corpus/runner
drift check. It is compiled and measured before candidate scoring; it is never a
Pareto or lexicographic member. Failure of its frozen comparator-eligibility
predicate leaves every control-relative candidate field unresolved and therefore
ineligible. The separately pinned Stage 4.6 receipts are identity/context-only
and currently `INCOMPARABLE`: absent a complete causal source/build/execution
closure, they supply no performance endpoint, calibration value, topology
constructor, or selection result. Any future comparison requires separately
sealed evidence that passes the frozen comparator-eligibility predicate; it
cannot reinterpret the current receipts.

The selectable universe also includes every complete, compile-targeted, signed
joint-profile submission received before the cutoff. A name or sketch is not a
submission. For every selectable frozen topology and physical profile, the
generator emits one pair. Each pair must either provide a complete realization
or an independently checkable `INAPPLICABLE` proof tied to a frozen
admissibility rule. Silence does not remove a pair.

Two topology manifests are equivalent only when their normalized authority,
writer/effect, direct-local-dependency, package/process/deployable, privilege/
helper-custody, DTO, call, and source-disposition graphs are identical. A
structural-dominance rule may remove only a graph that is identical on all
those facts and adds a pure forwarding edge/boundary with no deletion
counterexample. Performance expectations never establish dominance.

Discovery after the cutoff of an otherwise eligible topology, method, transform
axis, consumer, or pair invalidates `H_PROFILE`, returns to Phase 0, and requires
a new uncontaminated holdout. It is never appended to a visible tournament.

## Source-grounded reference shape

R0 is the first selectable challenger because it adds no boundary by default and
the current LayerStack package occupies a plausible dependency position. It is
not a rename plan or a winner. Its mandatory incremental count is exactly zero
new components, traits, ports, facades, registries, packages, processes, or
deployables. The clean pinned e497 graph contains 20 workspace packages,
including the legacy V1 LayerStack package; normal/build consumers from the
Docker provider, manager, workspace, observability query, and operation
packages; and a daemon development edge. The
provider emits V1 seed bytes, the manager calls the shared-base builder, and
workspace/observability DTOs carry LayerStack vocabulary. LayerStack itself has
no local workspace dependency. The pinned tree contains no current
`layerstack-core`, `mpla-poc`, EOS-LS3/V2/V3 storage candidate, generation-GC
handoff, or storage-helper package. Historical experiment material mentioning
those names is incomparable evidence and cannot construct a current candidate.

Any R0 realization therefore has to replace LayerStack semantics, choose one
format, integrate recovery and reclamation, and disposition every actual current
consumer. A generated package-deleting, operation-private, two-role, or one-role
fusion can win. A larger shape can win only through the same complete
tournament.

## What the joint card must prove

Every topology × physical-profile pair supplies one content-addressed card with:

1. compile-valid source for the frozen workspace targets, features, tests, and
   helper binaries; before/after `cargo metadata` and resolved feature graphs;
2. actual call, direct-local-dependency, durable-state, writer, authorization,
   effect, resource, recovery, component, package, process, deployment,
   privilege, and helper-custody graphs;
3. exactly one owner for every decision, selected-state write, native effect,
   recovery debt, resource claim, and fleet-fence transition;
4. one `KEEP`, `DELETE`, `MOVE`, or `NEUTRAL_DTO` disposition for every current
   direct consumer and every retained/new source, edge, DTO, worker, durable
   fact, package, process, and deployable, with an executable deletion
   counterexample for every `KEEP`;
5. complete I/O/state/crash/resource cards and a resolved `COST_RECORD` for every
   applicable operation, branch, terminal, fault, target, and authority under
   the [selection protocol](../algorithms/selection-protocol.md);
6. exact accepted-no-alias same-`StateId` whole-operation zero-selected-state-
   immutable-payload-I/O and zero-root-private-closure proof for checkpoint,
   fork, rollback-to-existing, `commit_fork`, and every same-state reference
   move; plus a qualification-only forced-collision seam proving exact-byte
   occupied-digest admission, typed terminal rejection, bounded cleanup, and
   fail-closed publish/import/recovery/index-rebuild/reference-fast-path/
   last-root behavior without adding a product interface or algorithm family;
   and
7. Linux conformance plus disposable WASI and Firecracker contract spikes,
   where `unsupported` is valid and creates no plugin architecture.

Reasons to change, call edges, source modules/packages, implementation
components, authorities, and processes/deployables are counted independently.
No diagram box implies an API or authority. Exact counts come from the compiled
winner, not a design sketch.

A semantic label is only candidate behavior or an accountability row; it is never
by itself a package, component, module, type, trait, port, facade, registry,
process, or deployable. Algorithms, codecs, hashes, canonicalization, and
validation remain stateless pure functions beside their lawful caller. The five
mandatory partitions test whether accountability owners may be fused. A new
owner or boundary beyond a generated fusion/placement is eligible only when a
presealed executable necessity trigger proves that every smaller compatible
owner arrangement plus direct calls cannot preserve a named state, effect,
lifecycle, synchronization, privilege, or resource invariant.

## Rejection and scoring order

A pair is rejected before any performance score if it is incomplete, does not
compile, omits a frozen consumer/product result, violates graph admissibility,
creates a duplicate writer/effect path or contradicts its declared partition,
reverses a forbidden
dependency, leaks native facts into portable identity, leaves unbounded work or
recovery debt, or fails crash, migration, containment, or resource safety.

Only complete compile-valid pairs that pass every non-performance hard gate may
enter the frozen cost/Pareto/lexicographic rule. `R_LEGACY_CONTROL` supplies only
sealed comparator endpoints and is never in that pool. “Zero additions,” fewer
boxes, or a fast physical microbenchmark is never a correctness waiver. A
larger boundary must still bind its necessity-trigger counterexample and show
through the complete ledger that it removes more total state, calls, failure
branches, or resource cost than it adds.

## Deliberately unselected

No representation, digest, graph/index, selector, replay encoding,
publication/reclamation/recovery method, synchronization primitive, admission
mechanic, package split, helper, process, deployable, method count, or API-edge
count is selected. OCI, WASI, and Firecracker are edge/profile concerns, not
core enums or Store plugins. MCTS and parallel rollout remain external policy
over accepted checkpoint/fork/root/OCC operations.

## `H_PROFILE` acceptance

Phase 1A records exactly one accepted `H_PROFILE` or `NO_WINNER`. `H_PROFILE`
binds the winning topology and physical profile together: source/build hashes,
all normalized graphs and exact counts, source/consumer dispositions, frozen
parameters, complete cost and hard-gate evidence, control/comparator receipts,
rejected candidates, holdout receipt, ADRs, and reopening conditions. It
authorizes only the later non-live implementation gates.

Any later topology, method, source consumer, dependency, DTO, writer, helper,
process, deployable, parameter, or candidate-universe change reopens Phase 0 and
invalidates `H_PROFILE` and all transitive artifacts.
