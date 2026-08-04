# Next-agent handoff

Status: **HISTORICAL HANDOFF — DO NOT EXECUTE**

> This handoff was superseded by the human V2 Phase 01
> [selected architecture](../../ephemeral-sandbox-v2/architecture_design.md).
> Phase 02 is now the next authorized design/implementation phase under the V2
> [PLAN](../../ephemeral-sandbox-v2/PLAN.md), subject to its prerequisites. Do
> not prepare this appendix's Phase 0 packet, rerun its tournament, or restore
> its historical `StateId`/storage terminology. See the
> [implementation-plan compatibility map](../README.md).

Original status: **DESIGN DRAFT — PREPARE, DO NOT EXECUTE, THE PHASE 0 PACKET**

## Do not mistake the challenger for a decision

```text
artifact-system preparation authorization      AUTHORIZED
durable Phase 0 authority + independent entry attestation  NOT_SEALED
Phase 0 execution packet / gate acceptance     DRAFT / NOT_RUN
Phase 1 joint topology × method selection     NOT_RUN
accepted joint H_PROFILE winners              0
algorithms mandated / proved / selected        0 / 0 / 0
exact responsibility/API/component counts      OPEN
Phase 2 live work                              UNAUTHORIZED
```

The zero-addition reference challenger is R0: repurpose the existing
`sandbox-runtime-layerstack` ownership home for complete immutable V2 state;
delete its LayerStack semantics; retain current application and runtime-effect
owners; add no mandatory package, module, component, service, process,
deployable, port, trait, facade, aggregate Backend, named canonical module, or
new coordinator. This is the first candidate to try to falsify, not an accepted
architecture or lower-bound theorem. Clean e497 contains the V1 LayerStack; it
does not contain the historical `mpla-poc` or `layerstack-core` packages or
their alleged local edges. R0 therefore means semantic replacement at one
plausible current dependency position, not a rename of finished code. Phase 0
must regenerate the source graph, all five set partitions of the three baseline
ownership questions, and every finite compile-valid deletion/placement
transform over actual packages/edges. Every generated candidate must compile
or have an independently checkable `INAPPLICABLE` proof. `NO_WINNER` is valid.

Do not turn diagram boxes into counts. Independently measure reasons to change,
call edges, writer/effect/decision/migration authorities, modules/packages,
components, processes, and deployables from the compiled candidate and runtime
graph.

## Non-negotiable behavior

For any number of roots naming one accepted `StateId` with identical accepted
canonical bytes, exactly one immutable physical dependency closure exists.
Every whole accepted no-alias checkpoint,
reference-only fork, rollback-to-existing, `commit_fork` winner transfer,
same-state no-op publication, root move, or ownership transfer—including every
failure, timeout/cancel, duplicate/stale input, crash, restart, recovery,
deletion, and last-root race—has:

```text
selected-state immutable payload bytes read    = 0
selected-state immutable payload bytes written = 0
total selected-state immutable payload bytes copied = 0
new root-private physical closure bytes         = 0
```

Only bounded, separately measured root/provenance/control metadata I/O is
allowed. Validation, warming, verification, prefetch, and recovery do not
create exceptions.

Never infer canonical equality from a finite digest alone. Candidate-bearing
admission compares the complete canonical candidate bytes against the admitted
bytes for an occupied digest. Unequal bytes are rejected as
`T03_REJECTION / STATE_ID_COLLISION` before creating any alias, head, root,
mapping, index entry, closure, revision, custody, or capacity claim. A
reference-only transition consumes only a previously admitted, authorized
no-alias binding and performs zero immutable-payload comparison or I/O; a
candidate-bearing attempt at a reference API is rejected or routed to
admission before fast-path entry. Phase 0 must seal a forced-collision
qualification seam across publication, import, recovery, index rebuild,
reference-API ingress, and last-root behavior without making the accepted
reference path reread payload. That seam adds no product algorithm, API,
field, service, or component.

MCTS/parallel-rollout selection, scoring, scheduling, backpropagation, and
pruning remain external. Storage exposes only accepted checkpoint/root/fork/OCC
behavior. Inactive roots retain no mutable runtime allocation, worker, FD,
queue, permit, or cache.

Reflink and FUSE are forbidden even as optional/private accelerators. Only a
qualified runtime-internal OverlayFS, native/VM snapshot, private
storage-driver acceleration, or dedup hint may accelerate a runtime-private
realization, and the complete contract must still pass with it disabled.

The public file namespace is `file_{verb}`. `file_read` behaves as follows:

- no `workspace_session_id`: capture one committed revision and read that
  immutable view;
- supplied `workspace_session_id`: authorize and read that exact live
  workspace-session generation through its current runtime-effect owner.

Writes and edits require a live workspace; they never mutate committed state.

## Workspace and evidence identity

```text
docs package
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/new_2.0_migration_implementation_plan
  repo branch: layerstack_2_0
  status: untracked package amid unrelated owner changes; preserve all

reserved implementation worktree
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0
  branch: codex/new-2.0-storage-core
  HEAD and origin/main: e4974d1f9aac702b35e052629cb070c897989352
  status: clean; no V2 product implementation changes
```

From the package root, verify the generated per-file manifest with this exact
read-only command:

```bash
awk '/^```text$/{inside=1;next} inside && /^```$/{exit} inside{print}' \
  evidence/draft-manifest.md | shasum -a 256 -c -
```

Then compute the separately sealed substantive digest across every regular
package file, including Markdown, JSON schemas/records, and the validator:

```bash
find . -type f \
  ! -path './evidence/draft-manifest.md' \
  ! -path './evidence/review-record.md' -print0 | \
  LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256
```

The first command covers every regular package file except the generated
manifest itself, including the generated review record, JSON contracts, and
validator. The second deliberately excludes both generated ledgers so
recording a verdict cannot change the bytes being judged. Also run:

```bash
python3 -B execution/validate.py
```

That no-argument form is valid only while no packet contains a protected
artifact. Before Phase 0 becomes `INPUT_LOCKED`, preserve the exact
authorization receipt and `phase-entry-attestation.schema.json` envelope in
the input lock, then run the validator with
`--authority-verifier-policy <absolute-path>` and
`--authority-verifier-policy-sha256 <exact-policy-digest>`. The authenticated
wrapper supplies an externally versioned, write-denied policy whose exact
per-artifact bindings select verifier executable/build and trust-root digests.
Packet bytes cannot choose their own verifier; historical bindings remain
independently verifiable after current-authority rotation.

The validator opens the policy and each self-contained static native
ELF32/ELF64 verifier source once through no-follow component traversal. It
copies at most 64 MiB into a close-on-successful-exec private anonymous
executable, removes write mode,
atomically applies `F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL`,
closes the source, and only then hashes, parses, and executes that same sealed
descriptor. Source mutation during copying fails the stat check or the
post-seal build digest; mutation after sealing cannot change executable bytes.
Policy version 3 rejects malformed or out-of-bounds ELF structure,
`PT_INTERP`, and `DT_NEEDED`; the verifier contract also forbids unpinned
helpers, plugins, interpreters, shared objects, and dynamically loaded code.
It has no source-path, interpreter, dynamic-loader, shared-library, helper, or
plugin execution fallback. Protected validation is Linux-only and fails closed
without memfd sealing plus exact-descriptor execution. Each sequential dispatch
owns at most one 64-MiB memfd, one transient 1-MiB copy buffer, and one child
capped at 256 MiB of address space, 32 descriptors, zero regular-file output
bytes, no core dump, and a bounded CPU/wall interval. Protected dispatch also
requires nonzero real/effective/saved UIDs plus empty inherited, permitted,
effective, and ambient Linux capability sets before treating
`RLIMIT_NPROC = 1` as an enforceable one-process bound; missing or malformed
capability state fails closed. Stdin is `/dev/null`; the watchdog remains active
even if the child closes both output pipes. Normal watchdog and exceptional
finalizer paths share process-group termination and interruption-safe direct-
child reaping. Every terminal path closes, kills, or reaps source, clone,
pipes, selector, process group, and child. Before depending on dispatch, run
`python3 -B execution/validate.py --self-test-authority-fd-exec`; the Linux
test proves sealed writes and truncation fail, that the approved clone still
executes after both in-place source mutation and pathname replacement, and that
closed output pipes cannot bypass the deadline. When run with privilege it also
proves privileged dispatch is ineligible and injects a parent-side post-fork
failure after a real descendant exists, accepting only after the descendant-
held lifetime pipe closes; a non-Linux host must prove protected dispatch is
unavailable.

At `SEALED`, the exact input-lock producer must authenticate the post-result
manifest under its separate seal domain; independent acceptance then binds
that exact manifest. Every non-bootstrap `state.json` advance or invalidation
must retain the exact prior state and complete prior packet prefix, authenticate
one state-last transition, and carry an externally verified one-shot
conditional-write or fenced-lease commit receipt for the exact raw successor
and prior token. Missing policy, retained history, exact-object verification,
or genuine commit receipt makes the frontier unusable.

Any manifest, digest, schema, dependency, packet-hash, source-identity, status,
or future-instantiation mismatch invalidates the review input; never refresh a
hash silently.

Stage 4.6 is read-only negative evidence. The P4 run-artifact manifest verifies
and several individual executable/helper digests are known, but exact
dirty/untracked source, the exact host publication-scorecard executable bytes,
and a complete causal build/configuration closure are missing. Set
`R_stage46 = INCOMPARABLE`. Do not join P4 timing to the distinct P1 memory
receipt and do not use the POC as an implementation base.

## Required read order

1. `README.md`, `traceability.md`, and `design/requirements.md`.
2. `design/architecture-selection.md`, `design/architecture.md`,
   `design/source-layout.md`, and `design/runtime-effects.md`.
3. `design/storage-model.md`, `design/public-api.md`,
   `design/migration-cutover.md`, and the remaining design contracts.
4. `algorithms/registry.md`, `algorithms/selection-protocol.md`, and
   `decisions/README.md`.
5. `phases/README.md`, `phases/phase-isolation-and-ordering.md`, all three
   numbered phase files, and `qualification/gates.md`.
6. `execution/README.md`, immutable `execution/gates.json`, mutable
   `execution/state.json`, all six schemas, the packet
   template, and the complete active `execution/phase-00/00-evidence-seal/`
   packet. Run `python3 -B execution/validate.py` from the package root.
7. Every evidence source required for the intended claim.
8. Product `AGENTS.md`, `CLAUDE.md`, and `docs/maintainer-architecture.md`
   before any product action.

## Active execution packet

Only `execution/phase-00/00-evidence-seal/` is instantiated, as declared by
`execution/state.json`. It contains the Phase 0 fused plan,
algorithm/evaluation/verification notes, handoff, evidence-custody rules,
controlled manifest, and independent-acceptance shell.
The evaluation note has separately validated experiment and benchmark regions.
Its state is `DRAFT / NOT_RUN`; the shell contains no
acceptor, accepted manifest, or output. Phase 1 and Phase 2 directories must
remain absent until exact predecessor acceptance and separate authority.

## First allowed deliverable: Phase 0 seal

Produce one content-addressed, candidate-independent package that freezes:

- exact product/docs/upstream Git and dirty identities; source and P4 run-seal
  hashes; retained versus missing provenance; and a newly attested matched
  incumbent plan;
- actual caller/auth/replay/error behavior and one transport-aware total
  disposition of all manager/runtime and observability operation names, HTTP
  routes, RPC control operations, legacy-proposed operations, and draft target
  operations; public/private/control classification is explicit rather than an
  excuse to omit a surface;
- all durable fields, roots, requests/outcomes, effect custody, allocations,
  writers/readers, packages/calls/processes/deployables, resource owners, and
  migration sources;
- exact architecture and physical-method candidate sets, with R0 eligible to
  lose and `NO_WINNER` required when all fail;
- representation-neutral fixtures, independent oracle, inaccessible holdout,
  numeric thresholds, statistical contract, execution order, retry/stopping/
  outlier rules, invalidation, and full source/build/run provenance;
- checkpoint/fork/rollback/commit/prune behavior at inactive fan-out
  `1/2/4/16/64/maximum` and all admitted active-rollout limits;
- exact managed-heap, cgroup, runtime-containment, storage/inode/FD/task/queue/
  cache/scratch/cleanup ceilings and acquisition/release rules; and
- the normative `operation × terminal × applicable fault` resource matrix,
  executing each cell or proving `UNREACHABLE` in the executable model.

Phase 0 selects and implements nothing. It adds no production path, schema,
package, API seam, field, cache, worker, index, V2 writer, or future-runtime
promise. Candidate authors do not see or tune the holdout.

## Complete causal chain

```text
Phase 0
  1. independent judge/evidence seal

Phase 1 — separately authorized, reversible, non-live
  2. joint topology x physical profile H_PROFILE or NO_WINNER
  3. H_FMT
  4. Hstore
  5. Hpermanent
  6. exact H_PRECUTOVER
  7. byte-identical Hqual

Phase 2 — separately authorized live-fleet envelope
  8. exact-H_PRECUTOVER irreversible cutover, fleet completion, and first
     possible public V2 operation acknowledgment
  9. bounded observation
  10. compatibility retirement and changed H_RELEASE build
  11. total QG disposition, exact-artifact qualification, new-release-epoch
      fleet rebind, old-process drain, live attestation, and release

post-release, outside DAG
  optional separately signed destructive legacy-byte deletion
```

Phase boundaries isolate capability changes: an independent judge cannot also
be candidate evaluation; a non-live authorization cannot preauthorize
irreversible live mutation. The 11 gates retain distinct hashes, producers,
acceptors, evidence scopes, invalidation, and stop rules. Three phases are the
smallest conservative operational grouping currently justified. A static-role
two-envelope challenger must still be evaluated; the global minimum remains
`OPEN`.

The fleet transition is monotone:

```text
LegacyWritable(g)
  -> QuiescedForImport(g+1)
  -> LegacyWritable(g+2)   # only before irreversible V2Writable transition

or

LegacyWritable(g)
  -> QuiescedForImport(g+1)
  -> distribute/install/sync/reconstruct/ack candidate g+2 while ingress closed
  -> V2Writable(g+2)
  -> activate local g+2, persist fleet completion, open generation-bound ingress
     # first possible public V2 operation acknowledgment; writable legacy never returns
```

## Stop rather than guess

Stop if the judge, source identity, authority/resource inventory, API semantics,
MCTS bounds, cleanup ownership, runtime containment, or comparator provenance
is incomplete; if a boundary/field/cache/worker/custom algorithm lacks a
deletion counterexample; if runtime-native values leak into portable identity;
if a method card omits exact I/O, linearization, crash/recovery, progress,
resource, or independent-oracle evidence; if results cause a holdout/threshold/
corpus/statistical change; if artifact hashes differ without requalification;
or if any post-activation path restores writable legacy.

## Repository rules

Preserve every dirty/untracked owner change. Do not reset, clean, stage, commit,
merge, push, or repurpose a worktree without explicit authorization. The
reserved worktree does not authorize implementation beyond Phase 0.

If runtime product code is later changed, run proportionate Rust checks and
`bin/start-sandbox-docker-gateway --rebuild-binary`. Manual sandbox operations
must use `sandbox-manager-cli`, `sandbox-runtime-cli`, and
`sandbox-observability-cli`. This design-only repair changed no product code,
so no gateway rebuild is due.
