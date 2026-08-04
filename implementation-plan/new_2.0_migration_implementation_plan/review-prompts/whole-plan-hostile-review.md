# State Storage V2 whole-plan hostile review prompt

Status: **EXECUTABLE REVIEW PROMPT — NOT DESIGN OR SELECTION AUTHORITY**

Use this prompt in a fresh task. It is intentionally adversarial: none of the
five requested conclusions is a premise. A reviewer passes a conclusion only
after trying to falsify it and producing reproducible evidence. This prompt may
block the plan; it may not lower a gate, invent missing evidence, or edit the
reviewed corpus into compliance while reviewing it.

---

/goal Perform a read-only, from-scratch hostile review of the complete State
Storage V2 migration implementation-plan package. Determine whether every
requested architectural, algorithmic, performance, memory/resource, checkpoint
fork/rollout, and phase-minimality claim is actually proved. Do not confirm the
author's preferred conclusions. Try to delete, fuse, replace, or falsify them.

## 1. Reviewed package and repositories

Review this package:

```text
/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/new_2.0_migration_implementation_plan
```

Use these read-only implementation/evidence locations when a claim depends on
deployed code or historical measurements:

```text
current implementation base/worktree
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0

reserved branch
  codex/new-2.0-storage-core

recorded clean origin/main base
  e4974d1f9aac702b35e052629cb070c897989352

later Stage 4.6 report/package identity; it does not establish the P4 run's
measured-code identity
  99290631750430cf267b5c9329f2ac5d281def05

later Stage 4.6 code-reference cutoff, not a sealed benchmark identity
  c70855d98588dc1739394c408aba395baa0ead54

raw P4 run provenance that must be independently verified
  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z/source.json
  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z/resources.json
  commit ac5c0686807ab40ee7e4ef3ff0f8488b66292221
  tree   918b4c0fad8ac37c5e2916d10b9b18d44cfeac55
  tracked diff 496505 bytes
  tracked diff SHA-256
    1580ae28b40dee88177bfde575e16ffdf6daf2cff21d2007732b8aaaa2f4b132
  measured mpla_lifecycle.rs SHA-256
    72d42529d54a77db6ebfd8df82b6c0a2bdbde7920495aa25da133d51d0996cf9
  later 992906-era mpla_lifecycle.rs SHA-256
    9735e17471edc6076cb218a99204ab7aa062f1eabd2e7fce8f605c94c3ce0f65
  P4 resource receipt memory peak 7,430,144 bytes

separate P1 activation-memory provenance; never attribute this peak to P4
  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final34b-p1-20260731t014941z/source.json
  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final34b-p1-20260731t014941z/resources.json
  commit ac5c0686807ab40ee7e4ef3ff0f8488b66292221
  tree   918b4c0fad8ac37c5e2916d10b9b18d44cfeac55
  tracked diff 74930 bytes
  tracked diff SHA-256
    2bfc4b64f730a6b956f17c1dbd74fa33ef5c7fc1ad5a9bd029a3d1e51913744f
  P1 activation resource receipt memory peak 102,543,360 bytes

sealed historical benchmark report
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/mpla_poc_benchmark_report.md

historical harsh-review prompt
  /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/prompts/pmss-harsh-minimal-algorithm-architecture-review.md
```

The recorded identities are review inputs, not facts to trust blindly. Resolve
the actual Git identities and dirty state at review start. Do not switch
branches, merge, reset, clean, stage, commit, or modify either repository.
Follow every applicable `AGENTS.md` and `CLAUDE.md` instruction for read-only
inspection. Do not run a mutating live sandbox benchmark unless the owner
separately authorizes that action; missing empirical evidence produces an
`OPEN` or `BLOCKED` finding, never an inferred pass.

## 2. Five claims to prove or reject

Treat each statement below as a contested hypothesis:

1. **Irreducible clean architecture.** R0 is the plan's zero-addition in-place
   reuse reference—not a winner, proved minimum, or lower bound—and the review
   must actively construct package-deleting fusion and any other complete
   smaller challenger. The selection procedure can delete any component,
   responsibility, call edge, deployable, package, abstraction, method, record,
   or field that lacks a named failing execution.
2. **Correct and dominating methods.** The joint topology × method selection
   and qualification
   procedure can prove every eventual winner correct under concurrency and
   every crash cut, with explicit time, I/O, memory, persistent-space,
   synchronization, contention, and cleanup bounds, and can test the exact V2
   artifact under the sole exact performance rule frozen by `QG-PERF-001` in
   Phase 0. Stage 4.6 and legacy ratios are reported only where artifacts and
   cells are comparable; the historical 100x label is not an implicit second
   gate. If no method/artifact/comparator is selected, this end-state claim is
   not yet proved.
3. **Memory and resource safety.** Trusted storage and every untrusted runtime
   have independent finite containment; every cache, buffer, index, pin,
   scratch object, mapping, descriptor, background task, and temporary artifact
   has bounded ownership and deterministic cleanup across every terminal path.
4. **Checkpoint-rooted fan-out.** Fork, MCTS expansion, and parallel rollout
   begin from an immutable named checkpoint/`StateId`, share the checkpoint's
   configured immutable closure exactly once, isolate all divergent mutable
   state, and retire all rollout resources safely.
5. **Phase-boundary minimality.** The current three operational envelopes—
   Phase 0 independent judge/evidence seal, Phase 1 non-live selection/
   implementation/qualification, and Phase 2 irreversible cutover/observation/
   retirement/release—preserve the required authorization and artifact
   boundaries through ordered subgates. Three is a conservative current
   grouping, not a demonstrated or global minimum; the minimum remains `OPEN`.

Do not assume these are already the method, architecture, or phase answers.
`PROPOSED`, `OPEN`, `TBD`, `NOT_RUN`, a worked example, an interface sketch, or
an analytical estimate is not proof. If architecture or physical methods are
still unselected, say explicitly which minimality, correctness, and performance
claims are therefore not yet provable.

## 3. Required review conduct

### 3.1 Freeze the input before interpreting it

From the package root:

1. enumerate every regular package file, including Markdown, JSON schemas and
   instances, the validator, this prompt, the generated draft manifest, and the
   historical review record;
2. verify the fenced payload in `evidence/draft-manifest.md` with the exact
   command in `HANDOFF.md`;
3. run `python3 -B execution/validate.py` and preserve its complete result;
4. compute a separate aggregate digest of every substantive regular file,
   excluding only `evidence/draft-manifest.md` and
   `evidence/review-record.md`;
5. compute a second full-tree aggregate digest including both ledgers;
6. record the docs and product Git HEAD/tree/branch/worktree/dirty state;
7. repeat the validator, manifest check, file inventory, and both digests at
   review end; and
8. return `BLOCKED_INPUT_CHANGED` if any reviewed byte changes.

Use this exact package-root command for the substantive digest so path prefixes
cannot produce superficially different seals:

```bash
find . -type f \
  ! -path './evidence/draft-manifest.md' \
  ! -path './evidence/review-record.md' -print0 | \
  LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256
```

Use the same pipeline without either `! -path` exclusion for the full-tree
digest. The review lead must not edit even the excluded ledgers while reviewers
are running.

Manifest identity proves which bytes were read. It does not prove the bytes are
correct or that a historical hostile verdict applies to the current digest.

### 3.2 Read the complete corpus, not selected summaries

Read every regular package file from byte 1 to EOF. Inspect JSON and Python as
executable contracts, not as attachments whose Markdown summaries may be
trusted. At minimum, explicitly cover this order:

1. `README.md`, `HANDOFF.md`, `traceability.md`, and
   `traceability/source-disposition.md`;
2. `design/requirements.md`, `design/architecture-selection.md`,
   `design/architecture.md`, and `design/source-layout.md`;
3. `design/storage-model.md`, `design/canonical-format.md`,
   `design/state-store.md`, `design/application-coordination.md`,
   `design/runtime-effects.md`, `design/public-api.md`, and
   `design/migration-cutover.md`;
4. `algorithms/registry.md` and `algorithms/selection-protocol.md`;
5. `phases/README.md`, `phases/phase-isolation-and-ordering.md`, and all three
   numbered phase files;
6. `execution/README.md`, `execution/gates.json`, `execution/state.json`, all
   six files in `execution/schemas/`, every file in
   `execution/packet-template/`, the complete active packet at
   `execution/phase-00/00-evidence-seal/`, and `execution/validate.py`;
7. `qualification/gates.md`, every decision/evidence document, the draft
   manifest, and the historical review record; and
8. the pinned Stage 4.6 report, source inputs, and current code for every claim
   whose proof depends on them.

Use exact `path:line` citations. A summary that does not cite the owner of the
claim is not a finding.

### 3.3 Lead review first, then an independent hostile round

The lead reviewer must complete and freeze its own full finding ledger before
launching subagents. After that self-review, launch the maximum useful number
of independent hostile subagents that the environment permits, with at least
these three non-overlapping primary lanes:

1. architecture deletion/SRP/SOLID/authority and field-method minimality;
2. algorithm correctness, complexity, benchmark provenance, performance
   dominance, schema/hash-chain correctness, and circularity attacks; and
3. memory/resource/cache cleanup, checkpoint-fork/MCTS fan-out, phase
   compression/order, validator bypasses, and execution-lifecycle drift.

Each subagent must:

- restart at the frozen package digest and read the complete current package;
- be told the five claims are hypotheses, not intended conclusions;
- remain read-only and avoid relying on the lead's verdict;
- report counterexamples and dissent even if another reviewer passed; and
- return its opening and closing digest plus exact files read.

The lead then reconciles findings against evidence. Do not accept a claim by
majority vote. One unrebutted counterexample or one missing hard-gate proof
blocks that claim. Preserve minority objections in the final report.

### 3.4 Attack the execution-artifact system itself

Do not confuse a validator pass with a phase-gate pass. Reconstruct the packet
state machine and try to produce a false authorization, an unverifiable
handoff, or mutable history. At minimum, determine whether:

- the three persistent packet files are irreducible: `packet.md` holds five
  exact marker-delimited, independently validated semantic regions,
  `manifest.json` seals controlled bytes and dependency identity, and
  `acceptance.json` records the independent verdict over one exact manifest.
  Reattempt both three-to-two fusion directions and try deriving either JSON
  authority from packet prose. Confirm that exact region hashes are derivable
  from the whole-file digest and fixed marker grammar rather than stored as
  four redundant persistent files. Try omitting a required historical file,
  adding an undeclared packet-root file, reordering/duplicating/removing a
  marker, and restoring the deleted derivable artifact-state field;
- content-addressed static topology in `gates.json` and mutable progress in `state.json` are
  the smallest coherent split, and advancing progress never changes the
  catalog digest embedded in already accepted packets;
- `gates.json` is the sole exact machine owner of concrete phase/gate IDs,
  their ordered phase assignments, and allowed output sets; predecessor edges,
  phase-entry locations, canonical paths, and transition effects must be
  derived and must not be stored or repeated: search schemas and `validate.py`
  for a second hard-coded topology,
  then mutate one catalog gate ID/phase boundary/allowed output in an
  isolated copy and verify that all derived paths and checks follow the one
  catalog or fail consistently rather than consulting a stale second table;
- the state record does not need stored `active_gate_id` or `stop_state`
  fields: try to find two valid meanings for the final instantiated packet and
  its acceptance disposition, or a lifecycle state that the derived frontier
  cannot express without mutating historical bytes; also attack whether the
  single `instantiated_gate_count` loses information compared with copying the
  catalog prefix IDs;
- the state contains no self-asserted phase authorization projection, a draft
  or input-locked manifest has no result producer, a sealed manifest has
  exactly one authenticated post-result producer whose principal triple is
  byte-for-byte equal to the input-lock producer, and every phase-entry input
  lock contains both a distinct exact authority
  receipt and a generic authorization attestation binding
  catalog/phase-entry-gate/lineage, authenticated
  principal/credential/control-domain triples, exact
  `produce:<gate-id>`/`accept:<gate-id>` capabilities, and
  validity/revocation; attempt arbitrary receipt bytes, shared values on each
  of the three independence axes, wildcard/role/scope authority,
  a phase capability omitted from the actor-set union, one actor granted both
  sides of the same gate,
  packet-selected trust material, predecessor acceptance alone, and a state
  edit;
- later same-phase input locks contain no repeated authority pointer and can
  resolve their governing phase entry only by following exact accepted
  predecessor bytes transitively; try a skipped gate, unresolved historical
  edge, cyclic edge, non-PASS predecessor, phase-crossing edge, and a later
  packet that injects replacement authority;
- the authenticated wrapper pins the exact raw bytes of one external,
  write-denied per-artifact policy; its sorted unique lookup key binds kind,
  phase, gate, lineage, artifact digest, and bound digest to an exact verifier
  build/trust root and current, historical, or one-shot-state-commit use; try
  packet-selected
  policy bytes, a global verifier tuple, build rotation, stale trust material,
  one key used as both current and historical, aliased verifier principals,
  missing historical binaries, a policy/executable symlink, parent-directory
  replacement, a wrong policy digest or malformed/unsorted binding that still
  attempts to launch its executable, any earlier schema/lineage/filesystem/
  package-manifest failure followed by verifier launch, a second verifier
  launch after the first authority failure, verifier-path replacement, source-
  inode mutation both during and after cloning, mutation through an already
  open source writer, a missing or partial memfd seal set, write/truncate/grow/
  shrink attempts against the sealed clone, build hashing before rather than
  after sealing, non-ELF executable, writable verifier source, truncated or
  malformed ELF32/ELF64, unsupported byte order, out-of-bounds headers/tables/
  segments, `PT_INTERP`, `DT_NEEDED`, runtime loading, unpinned interpreter/
  shared object/helper/plugin delegation, oversize output, a child that closes
  both output pipes and then hangs, timeout, fork/process growth, address-space
  growth, regular-file output, core dumps, inherited stdin, descriptor leakage,
  environment or `argv[0]` dependence, and any source-path, interpreter, loader,
  library, helper,
  plugin, unsealed-FD, or copy-to-disk execution fallback; require policy
  version 3, a post-copy hashed self-contained executable closure, all four
  irreversible seals on a close-on-successful-exec descriptor, exact sealed-
  descriptor execution, the fixed one-clone/one-child resource caps, watchdog
  enforcement even after pipe closure, and cleanup on every terminal path;
  require every protected
  attestation, input lock, sealed manifest, final acceptance, and non-bootstrap
  execution state to fail closed before use unless the exact policy-selected
  sealed clone authenticates its proof and derives the claimed control domain
  from trust evidence; mutate every field covered by the four packet
  action proof projections and the state-publisher projection, attempt to omit
  any field besides the one named `proof` member, and require rejection;
- archive a later same-phase descendant while leaving its canonical
  phase-entry packet current; the descendant lock/acceptance must become
  historical without relabeling the still-current phase-entry attestation or
  demanding a fabricated new phase grant, while a real change to the
  attestation/verifier/trust root must invalidate the phase-entry lineage;
- every JSON source rejects duplicate object members recursively before
  semantic validation; try same-value and conflicting-value duplicates at the
  top level and in nested schema, catalog, state, manifest, acceptance,
  input-lock, and phase-entry-attestation objects;
- the file inventory rejects symlinks and every non-regular entry, including a
  FIFO or socket that `find -type f` would omit; an unsealed special entry may
  not disappear from both the manifest and review digest;
- a producer's sealed `reported_status` remains distinct from the independent
  acceptor's `disposition`, so rejection or downgrade never requires producer
  mutation, every final verdict including `PASS` carries nonempty independent
  rationale, and only an independent `PASS` promotes exact produced outputs;
  require the legal intermediate pair `SEALED / NOT_RUN` to authenticate the
  result manifest immediately even though no acceptor exists yet, and try to
  bypass manifest verification by leaving the acceptance at `NOT_RUN`;
  attack a result written by a different producer, a copied input-lock proof,
  a null/unsigned manifest producer, a producer triple changed on any one axis,
  a post-seal field change, and an acceptor that authenticates only the input
  lock rather than the distinct result-seal domain;
- schemas, examples, prose, and `validate.py` define the same exact states,
  fields, paths, hashes, predecessor laws, and pass conditions, with no
  permissive branch or circular self-digest; verify that `validate.py` is the
  one package-acceptance authority and that the six interoperability schemas'
  complete non-annotation semantic projections are independently sealed;
  mutate an isolated copy with root `allOf: [{"not": {}}]`, a nested permissive
  `anyOf`, removal of `additionalProperties: false`, a weakened digest pattern,
  and each of the three former literal-11 state-cardinality bounds, and require
  every mutation to fail without regenerating a second topology table;
- every successor consumes both the exact predecessor manifest digest and the
  independently written acceptance digest, and transitive invalidation removes
  every now-unauthorized canonical consumer;
- accepted packet bytes remain immutable while invalidation is represented as
  separate lifecycle history, with a content-addressed archive and a monotonic
  replacement lineage rather than mutation of the old verdict;
- the flat `history/<gate-id>--<manifest-sha256>/` path preserves canonical
  relative schema/link depth, every invalidation's ordered affected rows form
  the complete first-through-last causal range, each gate's revisions are exactly contiguous
  from `r0001`, and `trigger_sha256` resolves in the lifecycle-later
  exact-next lineage of the first affected row's gate rather than in a later
  repair, unrelated packet, or free-floating digest; require that the receipt
  bind the immediately prior authenticated state digest and derived frontier
  so the final affected row is checked against historical proof rather than
  treated as a current-snapshot assertion; require the one-shot verifier to
  authenticate the exact receipt bytes under its pinned trust root and bind the
  exact prior state, ordered manifest/acceptance frontier, replacement, explicit
  changed dependency or predicate, and derived earliest owner; try arbitrary
  `x\n` bytes, a signed receipt for the wrong prior state, frontier, replacement,
  trigger basis, or later owner, and a valid receipt in an unrelated lineage;
  try restoring redundant first/last,
  archive-path, or archive-lineage fields and prove whether any adds information;
- revoking a previously instantiated phase-entry authority can reopen only the
  exact-next lineage as a receipt-only `DRAFT`, while an initial phase entry
  still requires an authority-bearing input lock and no `DRAFT` can
  perform result-bearing work;
- successor publication stages and verifies a complete same-filesystem packet,
  renames it into an absent canonical path, preserves exact prior state bytes,
  and commits `state.json` last under both an authenticated lifecycle publisher
  and a genuine external conditional write or fenced lease against the exact
  prior token; require the independently selected verifier to retrieve the
  signed provider receipt by operation ID and prove `COMMITTED`, exact raw
  successor digest, prior token/digest, object identity, and lease/fence values;
  reject a plain rename, local lock, self-authored receipt, missing receipt,
  forged provider, reused operation ID, partial invalidation suffix, omitted
  prior packet, a changed packet identity in a non-current retained transition,
  altered retained state, historical-chain cycle, or publisher/provider/
  verifier sharing any identity axis; distinguish the authenticated raw prior-
  state digest from the provider's opaque prior token and require one genuine
  receipt to bind both to the same successor/object; crash after every boundary
  and verify that orphan directories, stale state, or directory presence cannot
  grant authority;
- authenticated versioned or write-denied custody, rather than a local hash
  check alone, actually proves accepted-byte immutability and append-only state
  history; absent custody is a blocking Phase 0 fact, not an inferred property;
- timestamps are canonical audit labels only: attempt clock skew, equal wall
  times, and backdating, and require digest edges, the serialized state-last
  transition, and authenticated custody sequence—never wall-clock comparison—to
  prove causality and concurrency;
- `NO_WINNER` closes gates 1B through 2D, Phase exit never authorizes the next
  phase, and Phase 1 or Phase 2 cannot be instantiated before the causal
  prefix permits it;
- the active Phase 0 packet contains no completed run, accepted output,
  selected method, selected/new algorithm, implementation authority, or Phase
  1/2 authorization, and its `NOT_RUN` acceptance cannot be mistaken for an
  independent verdict;
- future lifecycle progression is expressible without changing historical
  packet bytes or weakening current source-identity requirements; and
- no cache, bytecode, temporary file, undeclared directory, symlink, or other
  artifact escapes the package inventory and package manifest.

Report the smallest concrete counterexample for every failed property. A
structural pass only proves that the declared packet shape is internally
consistent; it does not prove any experiment, benchmark, algorithm, design
choice, or gate disposition.

## 4. Claim labels and burden of proof

Label every important assertion with exactly one state:

- `MEASURED`: produced by a named command against a content-addressed artifact
  and accompanied by raw output and environment identity;
- `DERIVED`: follows from stated premises, with the derivation shown;
- `TARGET`: desired future threshold, not yet evidence;
- `HYPOTHESIS`: falsifiable proposed explanation or design;
- `UNSELECTED`: alternatives remain eligible;
- `FALSIFIED`: a reproducible counterexample exists; or
- `UNKNOWN`: the necessary evidence is absent or incomparable.

Do not promote a target to a guarantee. A benchmark proves observations inside
its declared envelope, not universal future latency. A real guarantee needs an
enforced bound/admission policy and a proof or qualified worst-case envelope.
For statistical claims, require predeclared samples, workloads, confidence or
uncertainty method, randomization, stopping rule, outlier policy, retry policy,
hardware/software identity, and untouched holdout. Three samples can establish
a historical median observation; they do not establish p95/p99 or a universal
guarantee.

## 5. Architecture deletion and cleanliness attack

Do not award cleanliness for more interfaces, familiar patterns, or a diagram.
First construct a clean-sheet minimum that satisfies the frozen requirements.
Architecture and physical method must be one joint card because a method can
change writers, packages, helpers, unsafe code, synchronization, recovery, and
resource ownership. Reject an architecture-first result followed by projection
of a later method onto it. Compare every joint card in the finite Phase-0-frozen
universe: the pinned evidence-only legacy control; R0; all five set partitions
of the three baseline ownership questions; every frozen one-boundary,
actual-package deletion, placement, and necessity-triggered transform generated
from clean e497; and every complete submission received before the signed
cutoff. Every generated candidate must compile or carry an independently
checkable `INAPPLICABLE` proof. Larger cards enter only under the frozen
added-boundary trigger. Verify that transform axes, equivalence, completeness,
admissibility, pre-result dominance, cutoff, and tie-breaking make the universe
reproducible; “every smaller candidate” or an open-ended generator is not
reproducible.
Direct concrete calls are eligible. A new Rust trait, port, facade, aggregate
runtime API, component, package, service, or process may survive only when the
exact compile graph, a frozen repository law, independent consumer contracts,
substitution/testing, or accepted conformance work supplies an executable
deletion counterexample. `NO_WINNER` must remain possible.

In particular, try to defeat R0's provisional zero-addition challenger: rewrite
the existing LayerStack ownership home for complete immutable V2 selected
state; retain application ordering and runtime-native effects in their existing
owners; and add no crate, package, component, trait, port, facade, coordinator,
service, deployable, process, registry, plugin, RPC, aggregate runtime API, or
predetermined call surface. R0 is neither a winner nor a proved lower bound.
First inspect whether the present package can actually carry that
responsibility. Reconstruct the clean e497 workspace/package, dependency,
writer, DTO, dispatch, helper, and process graph from hashed source. Confirm
that its V1 LayerStack is not a finished immutable V2 store. Explicitly reject
historical `mpla-poc`, `layerstack-core`, hidden-candidate, helper, or GC claims
as current facts unless independently pinned source proves them; those items
must never manufacture current edges or deletion candidates.

Then construct the complete smaller-shape challenge from actual source. For
baseline ownership questions `A` (application decisions), `S` (selected-state
truth), and `N` (applicable native effects), require `A|S|N`, `A+S|N`,
`A+N|S`, `S+N|A`, and `A+S+N`. Generate package-deletion and placement
transforms only over packages/edges actually present in e497. A transform may
fail security or ownership laws, but it remains an explicit candidate with a
checkable `INAPPLICABLE` proof rather than disappearing by assumption. Charge
lost purity, privilege, migration, and compatibility costs; do not award a
candidate merely for deleting package names.
Inventory the actual compiled call/writer graph and separately census reasons
to change, durable writers, effect executors, semantic decision owners,
migration-only authorities, components, packages, methods, and processes; do
not infer any count from the diagrams or semantic categories. Keep existing
application authorization, ordering, recovery, and admission decisions visible.
Treat admission placement as open: compare statically partitioned
authority-local permits, a process-scoped limiter hosted by an existing
composition root, and enforcement colocated with an accepted authority. Reject
a new global ledger or standalone Governor unless every smaller existing
placement fails a named invariant under executable evidence.

### 5.1 Count all architecture dimensions separately

Report exact counts for:

- semantic responsibilities;
- durable authorities and independent writers;
- volatile authorities;
- failure/commit domains;
- logical components;
- deployables/processes;
- Rust packages/modules;
- port/trait families;
- public operations;
- internal operations/methods;
- persistent records/rows;
- persistent fields;
- in-memory cache/index structures; and
- background workers/queues.

Never use one count as a substitute for another. “Four components” says
nothing about deployables, authorities, packages, or method/field minimality.

### 5.2 Produce a deletion ledger

For every proposed or selected component, responsibility, governor, port,
method, record, and field, assign one verdict:

- `KEEP_PROVED`;
- `DELETE`;
- `FUSE`;
- `DERIVE_INSTEAD_OF_STORE`;
- `MOVE_TO_CALLER`;
- `MOVE_TO_BACKEND`;
- `OPEN_UNSELECTED`; or
- `MISSING_REQUIRED`.

Every `KEEP_PROVED` row must state all of:

1. the exact invariant or user-visible semantic it owns;
2. its independent reason to change;
3. its unique writer/authority and readers;
4. its failure/commit boundary;
5. the concrete valid execution that fails after deletion or fusion;
6. why a standard library, existing crate, caller-local value, derived value,
   or runtime-owner-private implementation cannot replace it;
7. its measurable coupling/cycle impact; and
8. its lifecycle and cleanup owner.

If the reviewer cannot produce the failing execution, delete or reopen the
element. Reject speculative WASI/Firecracker abstractions, generic plugin
systems, generic transaction/merge engines, repositories wrapping repositories,
and fields stored only “for future use.” Runtime neutrality must come from
stable semantics and runtime-owner-private profiles, not from encoding OCI, WASI,
Firecracker, mounts, paths, snapshots, handles, devices, or native locators in
canonical/storage identity.

### 5.3 Check SRP and SOLID as falsifiable properties

- SRP: list the independent actors/reasons that can force each component to
  change. More than one unrelated actor is a split/fusion warning, not an
  automatic conclusion.
- OCP/DIP: prove that future runtime implementations change only private realization
  plus conformance composition; reject a selected-state core that imports
  runtime implementations or a runtime-effect owner that writes selected-state
  truth.
- LSP: give the common conformance corpus and show that a replacement runtime implementation
  preserves observable semantics without leaking a weaker durability/resource
  contract.
- ISP: map every trait method to callers; delete methods unused by a real
  consumer or split clients forced to depend on unrelated behavior.

Patterns are eligible only when they remove a demonstrated dependency or
failure ambiguity. Name the pattern, its cost, its deletion test, and why a
plain function or data type is insufficient.

## 6. Algorithm and protocol correctness attack

No historical PMSS name is a winner. Start with standard primitives and the
smallest adaptation. For every selected or proposed physical method/protocol,
produce a method card containing:

1. exact typed inputs, outputs, error results, preconditions, and postconditions
   for every operation and semantic branch;
2. exact persistent/volatile state machine, legal transitions, and the sole
   owner of each state and transition;
3. I/O-complete pseudocode in execution order, naming every lookup/list/stat/
   open/read/allocation/write/flush/sync/parent-sync/replace, lock/queue action,
   runtime-effect dispatch, retry, join/drain, cleanup, credit-visibility transition,
   and return; no opaque helper or verb may hide work;
4. one exact linearization or commit point for every success and non-success
   result, every invariant, and an inductive preservation argument for every
   pseudocode transition;
5. progress and fairness assumptions, every blocking point, starvation bound,
   cancellation/deadline behavior, finite retry variant and bound, and typed
   exhaustion result;
6. all concurrency interleavings with the same root, different roots, last-root
   retirement, cancellation, retry, duplicate identity at every boundary, and
   process death;
7. every persisted process-death cut and every distinct host/power-loss cut,
   exact visible synchronized bytes/state before and after it, exact recovered
   state, and the authority retaining custody to convergence; same-host
   `SIGKILL` evidence never substitutes for real-substrate durability evidence;
8. corruption/torn-write detection and exact error result;
9. authoritative owner of request outcome, effect custody, reader pins,
   capacity debt, runtime allocation, cleanup, and capacity visibility;
10. standard-library/crate alternatives and why the selected method wins; and
11. an executable model-check/property/fuzz/differential-test plan with an
    independently implemented oracle, preserved seed/schedule/fault/input, and
    mechanically minimized one-command counterexample output.

The accepted evidence bundle contains the immutable card, pseudocode and source
hashes, independent-oracle hash, executable commands and raw results, complete
transition and `O × T × applicable F` coverage, minimized counterexamples for
every observed failure, full cost-record derivations/measurements, and a
machine-checkable card-to-artifact trace. A prose plan or candidate-derived
oracle is not accepted evidence.

Before scoring, require a machine-checked closure predicate over every required
operation, branch, payload bucket, target, authority, terminal, fault, and cost
cell. Each cell must end as a proved analytical/mechanically enforced bound, an
empirical statistic only where the frozen schema explicitly permits it and
binds raw receipts, or proved `N/A` with an executable reachability/deletion
falsifier. Any `OPEN`, `TO_MEASURE`, blank, or finite measurement offered as a
worst-case or amortized bound makes the whole joint profile ineligible.

Reject correctness arguments based only on Rust ownership, happy-path unit
tests, filesystem folklore, a single process, or eventual best-effort cleanup.
Audit every `unsafe` block and foreign/system call boundary. If no physical
method is selected, report `UNSELECTED`; do not review a placeholder as if it
were an implementation.

### 6.1 Mandatory complexity and cost table

Define symbols before using them—for example total logical bytes, files,
directories, chunks/objects, changed bytes, roots, generations, dependency
edges, concurrent readers/writers, rollouts, replay entries, and runtime
realizations. Do not hide work in an undefined `O(1)` metadata operation.

For every public operation and every internal maintenance/recovery/migration
operation, and separately for every semantic branch, payload class, target,
participating authority, terminal path, and applicable fault cut, report:

- distinct best, expected, worst, and amortized CPU time, I/O, memory,
  persistent-space, synchronization, contention, cleanup, and custody envelopes;
- reachable preconditions for best case;
- the frozen distribution and workload/payload/cache/contention/fault/arrival/
  dependence assumptions for expected case;
- admitted domain and adversary for worst case;
- finite sequence plus potential/accounting proof for amortized case;
- logical bytes read/written;
- allocated physical bytes and peak live persistent bytes;
- peak managed heap and total cgroup memory;
- syscall, open-file, mapping, thread/task, lock, and fsync/dirsync counts;
- index/scan/replay work;
- contention scope and queue bound;
- temporary/scratch lifetime and cleanup point; and
- which bound is proved, measured, targeted, or unknown; an inapplicable field
  is `N/A` only with proof.

Expected and amortized are not aliases. Omission of an operation, branch,
payload, authority, terminal/fault cell, envelope, or cost dimension fails the
method card.

For checkpoint creation, reference-only fork, rollback-to-existing-state,
`commit_fork`, same-state no-op publication, and every future accepted no-alias
reference transition, the complete operation must perform exactly zero total
selected-state immutable payload reads, writes, and copies and create zero
root-private immutable closure bytes. An asymptotic `O(1)` label is
insufficient because it could hide a nonzero constant payload access. State
the real metadata bound rather than calling metadata constant when it is not.
Any sort/compaction formula must be derived from simultaneously live run sets
and crash policy; reject a generic “2x disk” or “2x memory” statement.
Streaming is the first candidate, and disk scratch never masquerades as RAM.
For variable-width external sort, reconstruct whole-record run packing from the
ordered encoded-record-size sequence. Treat `ceil(total_bytes / memory_limit)`
only as a lower bound unless a packing theorem proves equality; require an
oversized-record rule and derive merge passes, run/inode/FD counts, I/O, syncs,
recovery, and cleanup from the actual run manifest and merge graph.

## 7. Performance dominance and the “100x booster” trap

The historical label is not evidence. The later packaged Stage 4.6 report
states:

```text
POC_CORRECTNESS_PASS
POC_100X_NOT_SUPPORTED
POC_500X_NOT_SUPPORTED
AG_SQUASH_PASS
AG_STREAM_PASS
```

It reports only three samples for key medians. The P4 run's raw `source.json`
identifies dirty commit `ac5c068...`, tree `918b4c0...`, a tracked-diff length
and hash, and measured `mpla_lifecycle.rs` hash `72d425...`; it does **not**
retain the dirty patch bytes, complete tracked/untracked source archive, build
closure, or executable. Later P6/P7 packaging has a different `9735e1...`
source hash. The receipt is an identity commitment, not a reconstructible
causal closure. Therefore the P4 measurements cannot be causally attributed to
`992906...`, and they cannot serve as a matched Phase 0 comparator unless the
exact source/executable is reconstructed or the comparator is rerun. Four of five named
booster operations exceeded 100x against their matched controls, but small
publication did not: its matched-first-three candidate median and ratio
denominator was `58.136209 ms`, its all-five candidate median was
`62.567625 ms`, its all-five maximum was `65.937250 ms`, and its control median
was `36.444 ms`; the matched-subset comparison was approximately `0.6269x` as
fast or `1.595x` slower. Therefore:

- never call Stage 4.6 an aggregate “successful 100x booster”;
- never attribute the P4 measurements to `992906...`, `c70855...`, or a clean
  tree unless exact measured artifacts and raw provenance prove that identity;
- never compare numbers from unmatched machines, corpora, operation semantics,
  cache states, setup boundaries, durability modes, or concurrency levels; and
- never hide a regressing operation in a geometric mean or aggregate score.

For each comparable operation define, report, and retain both ratios:

```text
R_stage46 = T_exact_stage46_candidate / T_exact_v2_candidate
R_legacy  = T_matched_legacy_control / T_exact_v2_candidate
```

Because the retained evidence lacks the exact P4 executable/source closure,
the historical status is `R_stage46 = INCOMPARABLE`. A future reviewer may
change that status only after either (a) reconstructing exact tracked and
untracked source in a content-addressed archive/bundle plus toolchain/build
configuration, executable digest, fixtures, command, and environment or (b)
rerunning a newly attested comparator. A report file's later Git identity is
not the benchmark binary's identity.

There is exactly one prospective hard gate: the complete `QG-PERF-001` rule
frozen in Phase 0 before candidate results. It names the exact operation cells,
artifacts, comparators, correctness/resource prerequisites, absolute and
relative endpoints, statistics, confidence, workloads, cache states,
concurrency, restart/recovery scopes, cgroups, and holdout rule. A reviewer may
not add, relax, or replace a conjunct after results.

`R_stage46` and `R_legacy` remain mandatory diagnostic fields where comparable,
but they become pass/fail terms only if the Phase-0 seal says so. The historical
legacy-control 100x claim and its derived `0.36444 ms` value are nonbinding
stress falsifiers: they can falsify an assertion that V2 achieved that
historical target, but cannot independently pass or fail V2. No copied prompt,
historical label, or derived value creates a second gate.

### 7.1 Small publication is a red-alert stress workload

Treat small publication as the primary performance falsifier, not as one row
that an aggregate can hide. The historical evidence is an observed regression,
so any plan that lacks a dedicated small-publication critical path, candidate
tournament, benchmark cell, and stop condition receives
`SMALL_PUBLICATION_NOT_CLOSED`.

On the historical numbers alone, a 100x stress hypothesis would imply:

```text
historical legacy-control threshold = 36.444 ms / 100
                                    = 0.36444 ms

historical matched-first-three
Stage 4.6 dominance                 = T_v2 < 58.136209 ms

derived historical stress value    = T_v2 <= 0.36444 ms
```

`0.36444 ms` is a **nonbinding derived historical stress value**, not an SLA,
portable measurement, or independent hard gate. Phase 0 may adopt a
preregistered matched-control threshold on the qualification host, but only the
value sealed there before results decides `QG-PERF-001`. If durability-
equivalent device calibration, scheduler noise, or an unavoidable sync lower
bound makes the historical stress value infeasible, report that finding; do not
win by omitting required durability, delaying work, or renaming the operation.

Reconstruct the exact historical small-publication semantics and corpus from
the sealed command/raw artifacts before comparison. Then require a
nanosecond-resolution critical-path trace, with CPU and off-CPU time, for at
least these stages when applicable:

1. request decode, authorization, target normalization, and revision binding;
2. base checkpoint/root pin and conflict validation;
3. dirty-set discovery and delta validation;
4. content hashing/encoding and immutable-object existence checks;
5. new immutable-byte creation;
6. canonical-state/root construction;
7. index/catalog/root/outcome preparation;
8. durable publication, file/data sync, atomic selector transition, and
   directory sync;
9. visibility/linearization acknowledgement; and
10. pin, buffer, temporary-file, descriptor, and deferred-debt cleanup.

The minimum candidate to falsify separates preparation from the final
linearization gate: freeze and attest the origin; perform only bounded
in-process capture; stream/canonicalize/hash/stage and verify before the gate;
then briefly revalidate the origin and select the prepared root. The final gate
may not start a subprocess, unmount/remount, read or write immutable payload,
or manage a runtime-effect lifecycle. This is a latency hypothesis, not permission to
move work outside the benchmark: preparation, conflicts, retries, cleanup,
recovery, and the gate are all charged end to end and also reported separately.

Every stage must report call count, bytes, allocations, syscalls, locks,
context switches, page faults, sync waits, and percentage of end-to-end time.
The critical path must have one accountable owner. “Serialization,” “storage,”
or “filesystem overhead” is not a diagnosis.

The small-publication candidate tournament starts from existing, standard
primitives. It must attempt to eliminate whole-workspace scans, whole-base
rehashing, sorting, materialization, duplicated encoding, repeated path walks,
per-object sync, redundant directory sync, lock convoying, process startup,
and synchronous cleanup that is not necessary for visibility—without weakening
the operation's semantics. A specialized fast path is eligible only if:

- its predicate is closed and checked before mutation;
- it is correct for new, changed, deleted, and renamed small entries;
- cost is a function of the bounded change set and required publication
  metadata rather than total checkpoint/workspace size;
- it uses the same canonical identity, durability, authorization, replay,
  outcome, and crash contract as the general path;
- its fallback is semantically identical and independently tested;
- no unselected/unaccounted persistent cache, unbounded dirty journal, hidden
  resident index, or precomputed artifact moves publication work outside the
  measurement; any eligible durable index has explicit authority,
  reconstructibility, byte/lifecycle cost, invalidation, and cleanup; and
- its extra code/method/field survives the architecture deletion ledger with
  measured benefit on untouched holdout data.

At minimum, cross these small-publication workload factors:

- no-op/empty delta and one new, modified, deleted, and renamed entry;
- 1 byte, 4 KiB, and 64 KiB changed payloads, plus the exact historical cell;
- small and very large immutable bases with the same small change, to expose
  accidental `O(total base)` work;
- cold process/cold cache, warm process/cold data, and fully warm states;
- already-present content and wholly new content;
- clean start, restart/recovery, and immediately-after-checkpoint states;
- one publisher and the frozen admitted concurrent-reader/publisher levels;
- every applicable normative terminal and nested fault cell at each publication
  cut; and
- constrained service memory/cgroup plus normal and stressed storage latency.

Report p50/p95/p99/max, throughput, CPU, off-CPU, logical/physical I/O, fsync
and dirsync latency/count, peak heap/cgroup memory, peak temporary/persistent
bytes, descriptors, tasks, cleanup tail, and correctness for every required
cell. Use enough randomized matched trials to support the declared tails and
confidence interval. Pair run order, preserve raw samples, and use an untouched
holdout; do not tune the cutoff, batch size, or fast-path predicate on the
holdout.

Require two separate conclusions:

1. `SMALL_PUBLICATION_CAUSE_IDENTIFIED`: each Stage 4.6 regression term is
   attributed to a measured critical-path stage and reproduced or explicitly
   shown absent on the matched artifact; and
2. `SMALL_PUBLICATION_GATE_PASS`: V2 passes every small-publication term in the
   sole Phase-0-frozen `QG-PERF-001` rule plus all prerequisite semantic, crash,
   durability, and resource gates. Report Stage 4.6 and legacy ratios separately
   where comparable; the historical 100x stress value is not silently added.

Until `SMALL_PUBLICATION_GATE_PASS` is supported by content-addressed
production-artifact evidence, the end-state performance guarantee remains
blocked. `SMALL_PUBLICATION_CAUSE_IDENTIFIED` is a required diagnostic verdict,
not a second numerical gate unless Phase 0 explicitly makes it one. Optimizing
the median while regressing a frozen tail, crash-recovery, memory, cleanup,
larger-base, or concurrent-publication term is not a pass.

If the plan means a different scope by “improve,” require it to name the exact
operation set and margin before measuring. Do not accept “same asymptotic
complexity,” one faster construction path, or four of five operations as the
requested guarantee.

Detect work shifted outside the timer: preprocessing, import, checkpoint
creation, digesting, materialization, cache warming, lazy cleanup, recovery,
compaction, and deferred fsync must be charged. Report setup, cold, warm,
steady-state, amortized, and end-to-end costs separately. If existing evidence
cannot prove the hard gate, the honest result is `PERFORMANCE_NOT_PROVED` with
the exact missing experiment—not a predicted pass.

## 8. Memory, resource, and cache-cleanup attack

Audit language memory safety and finite resource ownership separately. Rust's
type system does not bound heap growth, page cache, kernel slab, mappings,
descriptors, queues, child processes, disk scratch, or leaked durable pins.

### 8.1 Required inventory

Inventory every cache-like or retained object, including:

- maps/sets/LRUs, memoization, decoded metadata, directory/content indexes;
- request/result/idempotency/replay state and effect-custody records;
- buffers, arenas, mmap regions, page-cache reliance, read-ahead, and batches;
- reader pins, checkpoint/root references, leases, sessions, rollout records;
- temporary files, partial objects, sort/compaction/import/recovery scratch;
- open files, directory handles, sockets, subprocesses, threads/tasks, queues;
- runtime workspaces, mounts, runtime-private overlays/snapshots, VM/WASI
  instances, and helper descendants; and
- backup/restore holds, migration generations, retirement debt, tombstones, and
  deferred deletion work.

For each item state owner, key, authority, maximum entries and bytes, admission
rule, accounting boundary, eviction policy, expiry trigger, reaper/cleanup
owner, reaper failure and restart behavior, cleanup linearization point,
crash/restart reconstruction, observability, and overload result. “The OS
cleans it,” “eventually,” “background GC,” or an unbounded TTL is a blocker.

### 8.2 Terminal-path cleanup matrix

Do not reproduce or abbreviate terminal/fault names in the report. Use the sole
[normative terminal and fault registry](../design/requirements.md#normative-terminal-and-fault-registry)
and require the full `O × T × applicable F` evidence matrix. Every applicable
terminal cell nests cleanup-worker and reaper faults. Recovery is a distinct
case from restart, stale revision is distinct from stale generation, and a
duplicate identity is injected before and after every named outcome/effect/
durability/cleanup boundary. An `UNREACHABLE` cell is valid only with an
invariant and executable falsifier that fails if the path becomes reachable.

Every cell names exact join/drain, synchronization, custody, cleanup, reaper,
startup/recovery, and capacity-visibility owners, plus durable debt, numeric
convergence horizon, and expected plateau. Cleanup must be idempotent and
recoverable. Detached best-effort tasks cannot be the only owner.

Capacity credit appears only after the relevant readers/pins/owners/backup
holds drain, unlink/release is complete, required directory synchronization is
durable, and the release is visible to admission accounting. Test a repeated
create/use/cancel/delete workload until memory, descriptors, tasks, inodes,
allocated bytes, and debt converge to a stated plateau.

### 8.3 Independent containment scopes

Verify both:

1. the trusted storage-managed aggregate across the actual selected
   process/cgroup topology, including the documented 8 MiB managed cap, normal
   4 MiB target, disjoint local admission shares plus shared recovery reserve,
   `memory.high = 64 MiB`, `memory.max = 96 MiB`, and zero swap; do not infer a
   new service or global admission authority from the budget; and
2. a separate finite enforced parent cgroup or proved runtime-equivalent
   boundary for every untrusted sandbox runtime/process tree, including all
   descendants/helpers, reparent/escape attempts, restart continuity, OOM
   behavior, and cleanup.

Passing one scope does not pass the other. Keep the run provenance separate:
P4 publication's resource receipt is `7,430,144 B`; P1 activation recorded
`102,543,360 B`, which is `1,880,064 B` over exact 96 MiB. Reconcile the P1
failure without falsely attaching it to P4 or rounding it into a pass.

## 9. Checkpoint, fork, MCTS, and parallel-rollout attack

Do not allow an active mutable workspace to be the semantic parent of a fork.
Require an immutable named checkpoint/`StateId` captured under a defined
revision and authorization decision. The storage layer supplies checkpoint,
fork-root, pin, compare/select/commit, and retirement primitives; MCTS policy
(selection, expansion, simulation, scoring, and backpropagation) belongs above
storage unless a proved invariant requires otherwise.

For one checkpoint with `N` forks/rollouts, prove all of:

- exactly one physical configured immutable dependency closure for an accepted
  shared checkpoint whose canonical bytes are identical, for every `N >= 1`;
- purpose-independent zero **total** selected-state immutable payload read,
  write, and copy plus zero root-private closure creation for accepted no-alias
  checkpoint,
  reference-only fork, rollback-to-existing, `commit_fork` winner transfer,
  same-state no-op publication/reference moves, and every future same-state
  reference transition;
- only bounded per-rollout root, provenance, lease/pin, outcome, and scheduling
  metadata before realization;
- an inactive rollout owns no payload copy, mutable workspace, mount, VM/WASI
  instance, open descriptor, or permanent cache entry;
- each active rollout receives a separately authorized and contained mutable
  runtime realization, with no sibling or parent write visibility;
- deterministic ancestry: checkpoint, parent root, child root, request, policy
  version, and result identity cannot be confused or rebound;
- a defined compare/select/`commit_fork` linearization rule, stale-parent
  behavior, winner publication, sibling fate, and no accidental generic
  merge/rebase semantics;
- breadth/depth/concurrency/admission/fairness bounds and typed overload;
- cancellation/pruning/timeout/crash/restart cleanup with idempotent pin and
  allocation release; and
- safety under every accepted no-alias root transition—checkpoint creation,
  reference-only fork, rollback, `commit_fork` winner transfer, rollout prune,
  checkpoint removal, child/parent deletion, and retirement—racing removal of
  the target state's last other root. Require an authority-atomic root transfer
  or durable transfer custody held until the new root is durable, recoverable,
  and capacity-visible.

Do not treat a finite `StateId` digest as injective. Force unequal canonical
bytes to the same candidate digest and attack candidate-bearing publication,
import, recovery, index rebuild, reference-API ingress, last-root reclamation,
restart, and replay. Candidate-bearing admission must compare exact canonical
bytes against the occupied binding and return
`T03_REJECTION / STATE_ID_COLLISION` before any alias, head, root, mapping,
index entry, closure, revision, custody, or capacity claim. Separately prove
that an accepted reference-only transition consumes only a previously admitted,
authorized no-alias binding and never rereads or compares immutable payload;
candidate-bearing input at that API must be rejected or routed to admission
before fast-path entry. Require bounded cleanup/quarantine, terminal replay,
fail-closed readiness, no disclosure of the prior state, and no digest-alias
table, fallback identity, second store, persistent collision index, or
payload-I/O escape in the normal zero-copy path. The collision injector is
qualification-only and must not be counted as a product algorithm or interface.

Instrument at the selected immutable-payload storage boundary. Apply the exact
zero totals to every applicable normative `O × T × F` cell. Separately measured
bounded metadata I/O is allowed; a candidate may not call a full payload scan
validation, verification, warming, or prefetch to evade the law.

Require tests at 1, 2, 4, 16, 64, and maximum inactive roots plus admitted
parallel active rollouts. Include thousands of inactive fan-out roots if that
is a claimed MCTS use case. Measure closure bytes, root metadata, heap, total
cgroup memory, inodes, FDs, tasks, runtime allocations, cleanup time, and
post-cleanup plateau separately.

If the plan contains only a generic fork sketch, return
`MISSING_MCTS_CHECKPOINT_CONTRACT`. Do not infer the contract. MCTS policy and
scheduling must remain outside storage. Even when the policy is out of scope,
require a closed checkpoint/fork/select/prune contract without embedding
selection, simulation, scoring, or backpropagation in the selected-state
implementation.

## 10. Three-envelope compression and ordering tournament

Do not accept three because the files are numbered 0–2. Reconstruct the DAG
from artifact identity, evidence validity, authorization transitions, rollback
points, and irreversibility. For every edge `A -> B`, give the concrete bad
execution or invalid evidence result caused by B running first. Remove every
edge justified only by convenience, team ownership, document order, or an
unselected architecture.

The current conservative operational grouping and ordered gate chain are:

```text
Phase 0 — Independent judge and evidence seal
  1. Phase-0 judge seal

Phase 1 — Non-live selection, implementation, and qualification
  2. 1A joint topology x physical profile H_PROFILE or NO_WINNER
  3. 1B H_FMT
  4. 1C Hstore
  5. 1D Hpermanent
  6. 1E exact H_PRECUTOVER
  7. 1F Hqual naming byte-identical H_PRECUTOVER

Phase 2 — Irreversible cutover, observation, retirement, and release
  8.  2A exact-artifact cutover plus durable fleet barrier
  9.  2B bounded observation
  10. 2C compatibility retirement and H_RELEASE build
  11. 2D total QG disposition, exact-artifact qualification,
      new-release-epoch fleet rebind, old-process drain, and live release
```

Optional destructive legacy-data removal is outside the DAG and requires a
later target-specific signature.

Within `2A`, verify two distinct boundaries and do not collapse their receipt
types. With ingress closed, every selector durably installs exact `g+2` in an
inactive slot and proves restart reconstruction. The global atomic FleetFence
transition from `QuiescedForImport(g+1)` to `V2Writable(g+2)` is the
irreversible writable-legacy rollback boundary, but does not open ingress or
permit a public V2 operation acknowledgment. Still with ingress closed, every
selector activates exact `g+2`; the complete generation-bound activation-ack
set must be persisted and reconstructible, and exact-`g+2` fleet completion
must be durable. Installation and activation acknowledgments are control-plane
receipts. Only the later opening of generation-bound ingress is the
first-possible-public-V2-operation-acknowledgment boundary. Inject crash,
restart, missing-selector, stale-generation, incomplete-ack-set, and duplicate
receipt faults before and after every step; fail closed unless the exact active
generation and complete fleet state are reconstructible.

### 10.1 Attack every adjacent fusion and internal boundary

Individually attempt both top-level fusions:

```text
0+1  1+2
```

Also try to fuse, reorder, parallelize, or delete every adjacent pair in the
eleven-node chain, especially 1A/1B, 1E/1F, 2A/2B, and 2C/2D. For each attempt,
provide the smallest complete fused form, then test:

- holdout/judge contamination and self-acceptance;
- production work before a winner or after `NO_WINNER`;
- content-addressed inputs/outputs and evidence-scope promotion;
- authority, failure-domain, call-direction, and rollback separation;
- public V2 operation acknowledgment before byte-identical `H_PRECUTOVER`
  qualification, or before exact-`g+2` fleet completion is durable and
  generation-bound ingress opens;
- compatibility removal before bounded observation;
- inherited `H_PRECUTOVER` evidence falsely qualifying changed `H_RELEASE`, an
  omitted QG disposition, or a release declared before exact changed bytes are
  installed and activated at a distinct release epoch across the expected
  fleet and every old process is drained;
- destructive action separation; and
- whether the proposed boundary is independently authorized or only scheduled.

### 10.2 Construct smaller complete plans

Produce at least:

1. the strongest complete two-envelope plan;
2. the strongest complete one-envelope plan, using a clean-sheet repartition
   rather than deleting labels; and
3. a clean-sheet minimum gate DAG unconstrained by current filenames.

Test whether any envelope hides another independently authorized or
irreversible artifact and needs a split. The current three-envelope grouping is
only a conservative operational organization. The global minimum remains
`OPEN` unless every smaller complete construction has a concrete judge,
selection, irreversibility, observation, or artifact-identity failure. “Clearer,”
“easier to manage,” and “a prior reviewer accepted it” are not proofs.

## 11. Contradiction and completeness checks

Cross-check all repeated counts, statuses, identities, names, limits, and
permissions. At minimum verify:

- three operational envelopes means exactly phases 0–2 everywhere, with the
  eleven ordered nodes above retaining independent hashes, owners, evidence
  scopes, stop conditions, and invalidation edges rather than becoming hidden
  top-level phases;
- zero mandated novel algorithms, zero proven novel algorithms, and zero
  selected physical methods are not contradicted by prose that names a
  historical custom winner;
- candidate architecture counts are not reported as accepted counts;
- current, legacy-proposed, V2-proposed, and finally selected external-surface
  populations remain distinct; clean e497 must account for all 18 manager/
  runtime names, eight observability names, HTTP `file_list`, health and forward
  routes, and RPC readiness control without inflating routes into operation-name
  rows or omitting them because they are private/control;
- `file_read` committed/workspace branches have one closed target-normalization
  rule and cannot leak conflict existence;
- exact one-closure checkpoint COW is not weakened to “near 1x,” dedup hints,
  snapshot, overlay, or mutable hard-link correctness; reflink/clone ioctls and
  FUSE remain prohibited even as optional/private accelerators;
- runtime-native identifiers remain outside canonical/storage identity;
- no cache, DB, WAL, refcount, queue, worker, process, plugin, field, or generic
  protocol appears outside the component/method/resource ledgers;
- no Phase 0 or joint-1A open decision is silently implemented by a later phase;
- each public result and external effect has one durable custody owner; and
- migration generations, stale-writer suppression, rollback, retirement, and
  destructive authorization remain coherent after the compatibility code is
  removed; the global `V2Writable(g+2)` transition remains the irreversible
  rollback boundary while the later fleet-completion ingress opening remains
  the first possible public V2 operation acknowledgment; and
- installation/activation acknowledgments remain control-plane receipts and
  cannot substitute for the complete persisted/reconstructible activation-ack
  set, durable fleet-completion record, or a public operation acknowledgment.

Run link, identifier, manifest, and source-hash checks. Mechanical consistency
is necessary but never sufficient for a pass.

## 12. Required final report

Lead with two independent verdicts:

```text
PLAN_REVIEW =
  PASS_FOR_PHASE_0_OWNER_REVIEW | BLOCKED_DESIGN |
  BLOCKED_INPUT_CHANGED | NO_DECISION

END_STATE_GUARANTEE =
  PROVED | NOT_YET_PROVED | FALSIFIED | NOT_TESTABLE
```

The first verdict asks whether the draft honestly defines sufficient frozen
work, evidence, ownership, and stop conditions for its currently authorized
phase. The second asks whether the implemented end state already proves all
five requested claims. Do not make one stand in for the other. Before a
selected production artifact and matched qualification run exist, the normal
honest end-state verdict is `NOT_YET_PROVED`, even if the Phase 0 plan is sound.

Then provide these sections in order.

### A. Seal and scope

- opening/closing package digest and manifest result;
- docs/product Git identities and dirty-state declaration;
- exact files and external artifacts read;
- commands executed and mutations explicitly avoided; and
- each lead/subagent scope, opening/closing digest, and verdict.

### B. Five-claim verdict matrix

For each contested claim report `PROVED`, `FALSIFIED`, `OPEN`, or
`NOT_TESTABLE`, with its strongest evidence, strongest counterexample, and
minimal missing proof. Do not average claims together.

### C. Ranked findings

Use:

- `P0`: could corrupt identity/data, violate isolation/authorization, make
  rollback/destruction unsafe, or render a claimed guarantee false;
- `P1`: blocks architecture/method selection, reproducible performance proof,
  bounded-resource proof, or phase acceptance; and
- `P2`: nonblocking clarity/maintainability defect with a concrete consequence.

Every finding must contain claim, exact citation, counterexample execution,
impact, violated invariant/gate, and smallest acceptable correction. Omit style
opinions and praise.

### D. Architecture deletion ledger

Include the clean-sheet alternative, all dimensional counts, every
component/port/method/record/field disposition, and before/after deletion/fusion
counts. State what was removed, simplified, moved, or added and why.

### E. Algorithm and complexity ledger

Include every public and internal operation, selected/unselected method status,
correctness state, linearization/crash/concurrency result, exact complexity and
resource vector, standard alternative, and required falsification test.
Conclude with exact counts of selected standard methods, adapted standard
methods, genuinely novel algorithms, custom crash protocols, open decisions,
and rejected historical mechanisms.

### F. Performance dominance report

For each operation show Stage 4.6 provenance, legacy control, exact V2 artifact,
semantic comparability, cold/warm/setup boundaries, raw measurement source,
`R_stage46`, `R_legacy`, absolute ceiling, statistics, resource regressions, and
gate verdict. Preserve `POC_100X_NOT_SUPPORTED` unless new matched evidence
actually changes the V2 result; never rewrite the historical verdict.

Give small publication its own red-alert subsection with the reconstructed
semantic cell, historical threshold derivation, critical-path flame/timeline
breakdown, cause attribution, candidate tournament, full factor matrix,
`SMALL_PUBLICATION_CAUSE_IDENTIFIED` status, and
`SMALL_PUBLICATION_GATE_PASS` status. No aggregate score may override either.

### G. Memory/cache/resource report

Provide the full inventory, bounds, owner/cleanup matrix, two containment-scope
verdicts, peak/plateau evidence, unsafe/syscall audit, last-reference races, and
all unbounded or best-effort cleanup blockers.

### H. Checkpoint/fork/MCTS report

Show the semantic workflow and ownership graph, one-closure proof, fan-out cost
equation, active/inactive rollout resource model, commit/prune/cancel/crash
state machines, exact purpose-independent payload-I/O measurements, concurrency
tests, and missing API/phase decisions.

### I. Phase compression report

Show the minimal dependency DAG, both top-level adjacent-fusion verdicts, every
adjacent-node reorder/fusion verdict across the eleven-node chain, strongest
two-envelope and one-envelope plans, any required split, allowed parallelism,
and the exact counterexample for every retained ordering edge and phase
boundary.

### J. Minimal correction and evidence plan

List only changes required to discharge P0/P1 findings, in dependency order.
Name the owning document/decision, artifact, command/test, acceptance threshold,
and invalidation rule. Do not implement those changes during this review.

### K. Final numeric answer

End with exact current and minimum-justified counts for phases, responsibilities,
components, authorities, deployables, packages, ports, public operations,
internal methods, persistent records/fields, caches/workers, selected physical
methods, and genuinely new algorithms. Use `OPEN` instead of inventing a
number.

## 13. Terminal pass rule

Return `PLAN_REVIEW = PASS_FOR_PHASE_0_OWNER_REVIEW` only when:

1. the complete stable corpus and all claim-critical sources were read;
2. each unproved end-state claim is explicitly `OPEN`/`NOT_YET_PROVED`, has one
   future phase/evidence owner and an immutable falsifiable hard gate, and is
   not described anywhere as a present result;
3. there are zero P0 and zero P1 **plan defects**; the honest absence of a later
   artifact is not itself a plan defect, but a missing/weak/waivable evidence
   gate, false present-tense guarantee, or unfunded critical experiment is;
4. every retained component/method/field survived an actual deletion/fusion
   attempt, every retained phase edge has a concrete ordering counterexample,
   and the report distinguishes the current three-envelope conservative
   operational grouping from the still-`OPEN` global minimum;
5. algorithm, crash, concurrency, resource, cache cleanup, and checkpoint-fan-
   out contracts are closed enough to create falsifiable evidence;
6. every performance statement retains its correct `MEASURED`/`TARGET`/
   `UNKNOWN` label, and no unsupported 100x or universal guarantee remains;
7. all reviewer dissents are either accepted as blockers or rebutted with exact
   evidence; and
8. the report states clearly that a design-review pass is not owner acceptance,
   algorithm selection, benchmark qualification, cutover authorization, or
   permission to implement beyond the package's current phase gate.

Set `END_STATE_GUARANTEE = PROVED` only if all five contested claims are
individually `PROVED`, including content-addressed matched evidence for small
publication and every other performance cell. Any `OPEN`, `UNKNOWN`,
`UNSELECTED`, missing production artifact, or missing holdout result makes the
end-state verdict `NOT_YET_PROVED`; a counterexample makes it `FALSIFIED`.

If desired V2-over-Stage-4.6 or historical 100x claims lack matched
production-artifact evidence—as is expected before implementation—do not
pretend they passed. Preserve `R_stage46 = INCOMPARABLE` where required and
report the historical 100x/`0.36444 ms` result only as a nonbinding stress
falsifier. The sole prospective hard-gate verdict comes from the exact
Phase-0-frozen `QG-PERF-001` contract; state which later artifact and experiment
can prove or falsify each of its terms.
