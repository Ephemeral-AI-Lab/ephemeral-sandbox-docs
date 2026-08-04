# Hostile review, repair, and seal record

Status: **ARTIFACT-SYSTEM ROOT REVIEW COMPLETE; FRESH HOSTILE REVIEW PENDING; ACTIVE PHASE 0 PACKET `NOT_RUN`**

Date: 2026-08-04

This is a review-history record, not architecture, algorithm, requirement,
phase, or release authority. The substantive-package digest deliberately
excludes this file and `draft-manifest.md`, so review results can be appended
without changing the bytes under review. The manifest still hashes this file.

## Superseded pre-artifact-system seal

The values in this section identify the earlier design-only package. They
predate the execution contract, schemas, templates, validator, and active Phase
0 packet and therefore are not the current review candidate.

| Item | Exact value |
|---|---|
| package root | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/new_2.0_migration_implementation_plan` |
| Markdown population | 29 files |
| substantive Markdown population | 27 files; excludes only this record and `evidence/draft-manifest.md` |
| substantive aggregate SHA-256 | `074e68931d92037bb2505838cae95edf4db18187525b42172f5a04566e8ed221` |
| pinned implementation worktree | `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0` |
| pinned branch | `codex/new-2.0-storage-core` |
| pinned product `HEAD` | `e4974d1f9aac702b35e052629cb070c897989352` |
| local `origin/main` at closing audit | `e4974d1f9aac702b35e052629cb070c897989352` |
| remote `refs/heads/main` at closing audit | `e4974d1f9aac702b35e052629cb070c897989352` |
| reserved implementation worktree state | clean |
| product package population | 20 packages from `cargo metadata --no-deps --format-version 1` |

The manifest must be regenerated and verified after this record is written and
before review dispatch. A reviewer must reject the package without a passing
manifest and matching opening/closing substantive digest.

## Review severity and acceptance rule

| Severity | Meaning |
|---|---|
| `P0` | safety, integrity, destructive-cutover, security, or unrecoverable-correctness flaw |
| `P1` | architecture, algorithm, API, resource, phase-order, provenance, or evidence flaw that can invalidate implementation selection or release |
| `P2` | bounded clarity, completeness, or maintainability defect that does not independently invalidate the design |

Panel acceptance is `PASS` only when every reviewer reports `P0 = 0` and
`P1 = 0` against identical opening and closing substantive bytes. A `P2` is
recorded and repaired when it affects the handoff, but cannot be relabelled to
hide a `P1`. Any substantive repair creates a new digest and invalidates all
verdicts on earlier bytes.

## First sealed hostile panel

The first panel reviewed substantive digest
`621375a8390825d78bb19f3839f6ff1d2b37f51e10b96f32830177ef29957770`.
All three reviewers independently verified that digest and the then-current
manifest at both review open and close. Their verdicts applied only to those
bytes.

| Reviewer scope | Verdict | Findings |
|---|---|---|
| sealed architecture red team | `FAIL`; `P0 = 0`, `P1 = 4` | the draft treated absent historical `mpla-poc`/`layerstack-core` packages and edges as current; the purported topology universe omitted four nonbaseline set partitions of `A/S/N`; reflink/FUSE were both prohibited and permitted; migration code was preselected as a package and dependency-direction wording was inconsistent |
| sealed algorithm red team | `FAIL`; `P0 = 0`, `P1 = 1`, `P2 = 1` | reflink/FUSE policy contradicted itself; a physical lower bound for the acceleration-disabled copy-out path was overgeneralized to native overlay/snapshot realizations |
| sealed API/phase red team | `FAIL`; `P0 = 0`, `P1 = 1` | the source-backed current external inventory omitted eight observability operations and separately dispatched HTTP/control surfaces; the current public/tool operation-name lower bound is at least 27, not 19 |

The API/phase reviewer separately found no defeating counterexample to the
three-envelope, 11-gate ordering on the reviewed bytes. That was not an
acceptance because its inventory `P1` remained open and the global phase
minimum is deliberately `OPEN`.

## Repairs after the first panel

### Current-source and topology repair

- Rebased every current graph claim on the clean pinned e497 tree and exact
  20-package Cargo metadata. Historical `mpla-poc`, `layerstack-core`,
  EOS-LS3/V2/V3, generation-GC handoff, and helper material are evidence only;
  they create no current package, source, dependency, consumer, or target.
- Defined `G_scope` as the exact generated source, caller, direct-local-
  dependency, target, feature, DTO, writer/effect, resource, recovery, route,
  and control closure. Submitted destinations join that closure before the
  signed cutoff; they cannot appear later as uncounted helpers.
- Defined neutral `lawful`/`compatible` rules without assuming R0, a package,
  or separate owners. The generator must seal member IDs, count, exclusions,
  and executable exclusion proofs before results.
- Added every set partition of application decision `A`, selected state `S`,
  and native effect `N`: `A|S|N`, `A+S|N`, `A+N|S`, `S+N|A`, and `A+S+N`.
- Kept R0 as a zero-addition witness, not a winner or lower-bound proof. Exact
  component, package, module, trait, port, call-edge, authority, process,
  deployable, and method counts remain `OPEN` until joint selection.

### Acceleration and cost repair

- Prohibited reflink/clone ioctls and FUSE in every role, including optional or
  runtime-private acceleration. Qualification now checks source, generated
  source, enabled features, dependencies, binary/syscall traces, helpers,
  mounts, and devices for those paths.
- Limited eligible acceleration to qualified runtime-owner-private OverlayFS,
  native/VM snapshot, private storage-driver, or deduplication-hint paths. Each
  must have a fully equivalent all-acceleration-disabled profile.
- Separated enabled and disabled cost vectors. No accelerated result can
  conceal fallback cost, privilege, cleanup, durability, or unsupported
  behavior.
- Scoped the file/allocator/block lower-bound formulas to the explicit
  acceleration-disabled full copy-out realization. They are not universal
  physical lower bounds.
- Removed generic `2x` disk/memory and external-sort formulas. Scratch is the
  maximum over the actual live-allocation timeline; external-sort passes and
  I/O derive from the actual run manifest and merge DAG. A two-complete-run-set
  overlap is charged only when that exact overlap exists.

### Import and permanent-dependency repair

- Removed any mandatory importer package. Temporary migration code is the
  smallest actual-source translator chosen by the joint tournament.
- Made the only allowed temporary dependency graph explicit: migration code may
  call the inventoried read-only legacy adapter, accepted pure canonical
  functions/types, and the narrow selected-state import command. Permanent V2
  code never depends on migration code or the legacy adapter.
- Retirement removes temporary entry points and callers first, then deletes
  now-unreferenced migration code and adapters. Changed `H_RELEASE` is rebuilt,
  freshly qualified, fleet-rebound at a new release epoch, and live-attested.

### External-surface repair

- Separated the 18 manager/runtime operation names, eight observability names,
  and HTTP-only `file_list`: the source-proved public/tool operation-name lower
  bound is at least 27.
- Inventoried `GET /health`, `/forward/shared/...`,
  `/forward/isolated=...`, and private authenticated
  `sandbox_daemon_ready` separately as route/control surfaces, rather than
  inflating them into catalog rows or omitting them.
- Required a total disposition for every current surface, including caller,
  authorization, request/result/error, replay, revocation, generation,
  recovery, cancellation, resource, transport, and compatibility fields.
- Retained one `file_{verb}` namespace. `file_read` accepts optional
  `workspace_session_id`: omission captures one committed immutable revision;
  presence authorizes and reads the exact live workspace-session generation.
  No `workspace_file_{verb}` aliases are added.

### Architecture-minimality repair

- R0 now has zero mandatory added components, modules, packages, services,
  processes, deployables, traits, ports, facades, registries, plugins, RPCs,
  coordinators, governors, caches, workers, algorithm authorities, or physical
  fields.
- Canonicalization, hashing, codecs, and validation are pure functions beside
  a lawful caller unless a sealed necessity trigger proves a boundary.
- Resource charging is owner-local. No aggregate governor or admission ledger
  is assumed.
- MCTS/search policy remains outside storage. Storage supplies only any
  accepted bounded checkpoint/root/fork/OCC effects, with inactive roots
  retaining no mutable runtime allocation, worker, FD, permit, or cache.
- Future WASI and Firecracker work is a disposable conformance spike with
  `unsupported` as a valid result; it creates no plugin architecture. OCI is an
  import/export concern, not core identity or a hard-coded storage backend.

## Root closing review before the first fresh panel

The root reviewer reread the complete 29-file package after repair, checked the
owner attachment and pinned source/provenance, and challenged the architecture,
candidate-universe closure, all 21 audit families, cost laws, resource and
cache closure, zero-copy COW boundary, API inventory, MCTS isolation, crash
cuts, migration dependency direction, three-phase compression, release-byte
identity, and Stage 4.6 comparator status.

Root result for substantive digest
`f8647ddfa9fee5c7d0177acbf892a4b5093e96dccc0a0a994d59084ffc1f7d50`:

| Severity | Open count |
|---|---:|
| `P0` | 0 |
| `P1` | 0 |
| `P2` | 0 |

This root result authorizes only fresh hostile review. It does not accept a
production architecture, method, performance claim, migration, or release.

## Deterministic closing checks

| Check | Result |
|---|---|
| UTF-8, tabs, trailing whitespace, fenced blocks, YAML front matter | pass across all 29 Markdown files |
| local Markdown targets and anchors | pass; 0 missing targets/anchors |
| numbered phase files | exactly 3 |
| requirement registry | 63 unique definitions; every referenced ID defined |
| orthogonal qualification-gate registry | 12 unique definitions; every referenced ID defined |
| algorithm audit-family registry | 21 unique IDs; every referenced ID defined |
| decision registry | 18 unique definitions; every referenced ID defined |
| input/source manifest | 68 of 68 exact SHA-256 rows verified |
| historical P4 run-artifact manifest | 20 of 20 entries verified; this remains a run-artifact seal, not a causal source/build closure |
| reserved implementation worktree | clean; branch, `HEAD`, local `origin/main`, and remote main verified as recorded above |

The exact zero-copy COW invariant is a semantic selected-state boundary, not a
filesystem-clone claim: every same-`StateId` reference-only checkpoint, fork,
rollback-to-existing, `commit_fork` transfer, same-state publication, or root
move has whole-operation selected-state immutable payload reads, writes, and
copies equal to zero and creates zero root-private physical-closure bytes.
Bounded metadata I/O and any separately admitted runtime-private mutable
realization are counted separately in the complete cost vector.

Stage 4.6 remains `R_stage46 = INCOMPARABLE`. Its preserved receipts are useful
identity and historical context, but no current relative-speed or “guaranteed
improvement” claim may use them without a newly attested matched run or exact
causal source/build/execution reconstruction.

## First fresh-from-start hostile panel

Three isolated reviewers restarted from substantive digest
`f8647ddfa9fee5c7d0177acbf892a4b5093e96dccc0a0a994d59084ffc1f7d50`
without using the earlier panel as proof. Each read all 29 package files to EOF,
verified all 28 manifest payload rows and the substantive digest at both open
and close, independently checked the applicable pinned e497 source and sealed
receipts, and made no package edit.

| Reviewer scope | Verdict | Findings |
|---|---|---|
| architecture/source/minimality | `PASS_FOR_PHASE_0_OWNER_REVIEW`; end-state guarantee not proved | `P0 = 0`, `P1 = 0`, `P2 = 0`; the strongest live deletion challenger removes the current LayerStack package and may reduce the current 20-package graph to 19, but remains an uncompiled candidate rather than a minimum claim |
| algorithms/COW/cost/resources/performance | `PASS_FOR_PHASE_0_OWNER_REVIEW`; end-state guarantee not proved | `P0 = 0`, `P1 = 0`, `P2 = 2`; one noncanonical gate identifier and one additive encoded-byte expression that did not make shared-byte attribution explicit |
| API/source/phase/MCTS | `PASS_FOR_PHASE_0_OWNER_REVIEW`; global minimum open and end-state guarantee not proved | `P0 = 0`, `P1 = 0`, `P2 = 0`; confirmed the 27-name current operation subtotal plus separately classified HTTP/control surfaces, optional-session `file_read`, exact COW/fork obligations, three conservative envelopes, and the unresolved two-envelope challenger |

The panel accepted no architecture, physical method, algorithm, benchmark
guarantee, migration, release, or global phase minimum. It confirmed only that
the plan was eligible for Phase 0 owner review, subject to repairing the two
bounded P2 defects for a clean handoff.

## Post-panel P2 repairs and root reseal

- Replaced the undefined shorthand `QG-PERF` with the sole canonical gate ID
  `QG-PERF-001` and kept the sentence inside `REQ-PERF-002`.
- Replaced separate `E_transition` and `E_outcome` symbols with one
  profile-specific `E_tx`. It counts each actually written encoded byte once,
  including when a shared field or framing byte serves both semantics;
  allocation rounding and filesystem metadata remain in `M_tx`. The analytical
  statement no longer infers an additive lower bound from semantic separation.

Those substantive repairs produced digest
`074e68931d92037bb2505838cae95edf4db18187525b42172f5a04566e8ed221`.
The root reviewer then reread the changed contexts and their ownership/cost
cross-references and reran the package-wide deterministic audit:

| Check | Post-repair result |
|---|---|
| Markdown population and substantive population | 29 and 27 |
| UTF-8, tabs, trailing whitespace, fences, YAML, local targets and anchors | pass |
| registries | 63 requirements, 12 qualification gates, 21 audit families, 18 decisions; all checked gate references canonical |
| numbered phase files | exactly 3 |
| input/source manifest | 68 of 68 exact SHA-256 rows verified |
| historical P4 run manifest | 20 of 20 entries verified; manifest SHA-256 `ca38a57d6a93fd268e2f696a78e234bf73f3dccfdf64e1fd6883ae46438bfc96` |
| reserved implementation worktree | clean; branch `codex/new-2.0-storage-core`; `HEAD`, local `origin/main`, and remote main all `e4974d1f9aac702b35e052629cb070c897989352`; tree `5d04b31c26bf37e4f62435fe12febfda26ca9719`; 20 Cargo packages |
| root post-repair finding ledger | `P0 = 0`, `P1 = 0`, `P2 = 0` |

The repaired package still authorizes only Phase 0 owner review. All winner
counts remain zero, all implementation/minimum claims remain open, Stage 4.6
remains incomparable, and `NO_WINNER` remains a valid joint-tournament result.

## Final hostile-recheck dispatch

Because even a P2 repair changes substantive bytes, verdicts on the prior
digest cannot close this record. Three reviewers must restart from the repaired
digest without treating any earlier verdict as evidence. Each must verify the
manifest and digest at open and close, read all 29 files to EOF, inspect its
applicable pinned e497 source and receipts, and return a strict `P0/P1/P2`
ledger without editing the package. Final results remain absent until that
recheck closes against unchanged bytes.

## Final from-scratch hostile recheck

Three isolated reviewers restarted from substantive digest
`074e68931d92037bb2505838cae95edf4db18187525b42172f5a04566e8ed221`.
They did not treat the root review or either earlier panel as evidence. Each
read all 29 package files to EOF, verified all 28 manifest payload rows and the
27-file substantive digest at both open and close, inspected its applicable
pinned e497 source and sealed receipts, made no package edit, and returned the
following ledger against byte-identical substantive content:

| Reviewer scope | Verdict | Findings |
|---|---|---|
| architecture/source/minimality | `PASS_FOR_PHASE_0_OWNER_REVIEW`; end-state guarantee not proved | `P0 = 0`, `P1 = 0`, `P2 = 0`; all five `A/S/N` partitions and deletion/fusion generators remain required, all winner counts remain open, and the strongest live `20 -> 19` LayerStack-deletion challenger remains a generated but uncompiled candidate |
| algorithms/COW/cost/resources/performance | `PASS_FOR_PHASE_0_OWNER_REVIEW`; end-state guarantee not proved | `P0 = 0`, `P1 = 0`, `P2 = 0`; all 21 audit families remain unselected, `E_tx` counts shared encoded bytes once, exact same-`StateId` COW and last-root/resource/cache laws remain falsifiable, and Stage 4.6 remains incomparable |
| API/source/phase/MCTS | `PASS_FOR_PHASE_0_OWNER_REVIEW`; global minimum and end-state guarantee not proved | `P0 = 0`, `P1 = 0`, `P2 = 0`; the 27-name source-backed lower bound and separately classified controls, optional-session `file_read`, checkpoint-root MCTS boundary, 11 causal gates, 12 qualification dimensions, three conservative envelopes, and strongest two-envelope challenger remain consistent |

The reviewers independently reproduced the clean product identity at branch
`codex/new-2.0-storage-core`, commit
`e4974d1f9aac702b35e052629cb070c897989352`, and tree
`5d04b31c26bf37e4f62435fe12febfda26ca9719`; verified all 68 source-manifest
rows; and verified all 20 P4 run-manifest entries. The algorithm reviewer also
recomputed the preserved matched publication ratio as
`0.626872660375...x`. That historical ratio is not a current selector or a V2
performance qualification.

The strongest live architecture challenger is `S+N|A`: delete
`sandbox-runtime-layerstack` and move selected-state responsibility into
`sandbox-runtime-workspace`, potentially reducing the current package graph
from 20 to 19. The strongest phase challenger is `{Phase 0 + Phase 1 under
proved static noninterference, Phase 2}`. Neither is selected or disproved;
both remain mandatory Phase 0/1 evidence work. Preserving those challengers is
why this record can pass the plan without claiming an architecture or phase
minimum.

Final panel result: `P0 = 0`, `P1 = 0`, and `P2 = 0`. This closes the document
repair and review loop only. It authorizes Phase 0 owner review, not owner
acceptance, implementation selection, production implementation, benchmark
qualification, migration, cutover, retirement, or release. The joint
tournament is `NOT_RUN`; exact end-state counts and the global phase minimum
remain `OPEN`; zero physical methods are selected; and
`END_STATE_GUARANTEE = NOT_YET_PROVED`.

## Execution-artifact-system root review

The preceding panels reviewed the design-only package. They do not review or
authorize the execution-artifact system added afterward. The root reviewer
therefore restarted at the complete 56-file package, read the new execution
contract, five schemas, validator, nine-file reusable packet template, active
Phase 0 packet, and every integration change before dispatching any new
reviewer.

The root-reviewed substantive digest is
`0760e0d8e70db8d7796529897ded8ef73bac399c81ccb83db35553be7e90f006`.
It covers every regular package file except this append-only review record and
`evidence/draft-manifest.md`. The population at root-review close is:

| Item | Exact count or state |
|---|---:|
| regular package files | 56 |
| draft-manifest payload rows | 55 |
| Markdown files | 44 |
| machine-readable schemas | 5 |
| persistent reusable packet-template files | 9 |
| persistent active Phase 0 packet files | 9 |
| operational phases | 3 |
| strictly ordered causal gates | 11 |
| instantiated gates | 1 (`00-evidence-seal`) |
| instantiated Phase 1 or Phase 2 packets | 0 |
| accepted architecture or physical-method winners | 0 |
| produced product algorithms | 0 |

The active packet remains `DRAFT / NOT_RUN`. Its input-lock, result evidence,
producer seal, and independent acceptance are absent. Preparation does not
authorize Phase 0 result-bearing work, Phase 1 implementation, or any Phase 2
live mutation.

### Root deletion and simplification audit

The root reviewer challenged every stored projection against the rule that a
fact should have exactly one owner. The final system removes or avoids:

- catalog-level dependency-rule prose, stored predecessor-ID arrays, phase-
  entry flags, canonical paths, and transition effects; all derive from the
  one ordered gate catalog;
- mutable `active_gate_id`, completed-gate lists, mutable authority state, and
  record revision counters; the instantiated causal prefix derives from one
  integer and authority remains a separately sealed receipt;
- duplicate artifact state and redundant archive path/lineage fields;
  controlled bytes are identified by path, role, and digest, while archive
  location and lineage derive from the gate ID and content-addressed manifest;
- timestamp ordering as a concurrency or causality proof; UTC timestamps are
  audit labels, while exact digest edges, authenticated custody, and the
  serialized state-last publisher prove ordering; and
- precreated future-phase directories, placeholder evidence directories,
  caches, bytecode, temporary files, symlinks, and unmanifested packet files.

The remaining nine persistent packet files were retained because they divide
independently reviewed responsibilities: scope, decisions, algorithms,
experiments, benchmark evidence, verification, handoff, producer manifest,
and independent acceptance. On-demand evidence is a responsibility and
content-addressed byte closure, not a tenth placeholder file.

### Integrity and mutation results

The unmodified package passed `python3 execution/validate.py` with 1,067
checks. The first isolated mutation run rejected seven of nine attacks with
the intended diagnostic but exposed one validator robustness defect: missing
canonical packet bytes caused an uncaught `FileNotFoundError` in two cases.
The digest reader was then made fail-closed so an unreadable required byte
becomes a normal contract failure and cannot crash or bypass validation.

After that repair, a fresh isolated nine-case suite rejected all nine attacks
with their intended contract class:

1. future packet instantiated before eligibility;
2. state prefix advanced without its canonical packet;
3. catalog gate identity changed without the derived canonical packet;
4. redundant mutable active-gate projection restored;
5. final acceptance forged without an exact sealed manifest binding;
6. undeclared packet file added;
7. live verdict inserted into the inert template;
8. noncanonical path traversal inserted into an artifact row; and
9. packet output changed outside the catalog contract.

The repaired unmodified package again passed all 1,067 checks. Exact safe-path
schema adversaries, JSON parsing, and Python AST parsing also passed during the
root audit. No project cache, bytecode, temporary file, symlink, empty
directory, or future packet remains.

### Root finding ledger and source identity

| Severity | Open count |
|---|---:|
| `P0` | 0 |
| `P1` | 0 |
| `P2` | 0 |

The reserved product worktree remained clean and read-only on branch
`codex/new-2.0-storage-core`; `HEAD`, local `origin/main`, and remote
`refs/heads/main` were all
`e4974d1f9aac702b35e052629cb070c897989352`, with tree
`5d04b31c26bf37e4f62435fe12febfda26ca9719`. The documentation repository
remained on `layerstack_2_0` at
`dc9ae450107ec40087ac086950e7b38b2436c9cc`; the target package is untracked
and unrelated owner changes were not touched.

This root result authorizes only a new isolated hostile review of the exact
substantive digest above. It does not select or accept an architecture,
algorithm, storage method, comparator, performance claim, migration, cutover,
or release.

## First execution-artifact hostile panel and repair

The first execution-artifact hostile panel reviewed the exact substantive
digest
`0760e0d8e70db8d7796529897ded8ef73bac399c81ccb83db35553be7e90f006`
and full-tree digest
`b9ab6b9a774dadfc0d5742c9e341216534a8eecaf04e12806b7a83cbad6ffb2e`.
That snapshot contained 56 regular files, five schemas, a nine-file reusable
packet, and a nine-file active Phase 0 packet. Three isolated reviewers began
from the package rather than inheriting the root conclusions and returned the
following raw ledgers:

| Hostile lane | Raw ledger | Material challenge |
|---|---:|---|
| algorithms, exact COW, and complexity | `P0 = 1`, `P1 = 0`, `P2 = 0` | duplicate JSON object keys were accepted, so different consumers could assign different meanings to the same controlled bytes |
| lifecycle, invalidation, and cleanup | `P0 = 0`, `P1 = 1`, `P2 = 1` | the same duplicate-key semantic differential remained exploitable, and the filesystem inventory omitted non-regular entries such as FIFOs and sockets |
| architecture, authority, and minimality | `P0 = 0`, `P1 = 2`, `P2 = 2` | phase-entry authority could be represented by self-authored bytes; topology literals encoded the current three-phase/11-gate instance; the storage model duplicated too much owner text; and separate experiment and benchmark notes were not irreducible |

These findings invalidated that snapshot. The package was explicitly
**UNFROZEN**, and none of its earlier digests or PASS statements were carried
forward as approval. The repairs were:

1. one strict recursive JSON decoder now rejects duplicate keys at every
   nesting depth for every controlled JSON category;
2. package inventory now rejects symlinks, FIFOs, sockets, devices, and every
   other entry that is neither a directory nor a regular file;
3. phase entry now requires an attestation bound to the exact predecessor
   acceptance receipt, actor credentials and capabilities, authorization
   validity and revocation state, a trust root, and a pinned independently run
   verifier build; authorizer, actors, and verifier must have mutually distinct
   identities and credentials;
4. the validator and schemas derive the number of phases, gates, outcome sets,
   and canonical packet locations from the catalog rather than treating the
   current three phases and 11 gates as global constants;
5. `experiments.md` and `benchmarks.md` were fused into one ordered
   `evaluation.md`, reducing each persistent packet from nine files to eight
   without merging producer, verifier, or acceptor responsibilities; and
6. `design/storage-model.md` was reduced from 2,315 lines to a 473-line
   owner-linked contract and cost audit. It retains the exact zero-copy COW,
   memory-safety, cleanup, complexity, external-sort, checkpoint-fork, and
   runtime-neutrality obligations without becoming a second source of truth.

The root re-read then caught two additional drift defects before resealing: the
input-lock schema still encoded the deleted seven-note minimum, and the
authority check did not yet reject an authorizer identity or credential that
aliased an actor. Both were corrected, and internal authority tests now cover
actor, authorizer, and verifier identity and credential aliasing.

The repaired population is 55 regular files: 42 Markdown files, 12 JSON files,
one Python validator, six schemas, eight reusable packet files, and eight active
Phase 0 packet files. The active packet is still `DRAFT / NOT_RUN`; it contains
no input lock, phase-entry attestation, result evidence, producer seal, or
acceptance. The current catalog still happens to contain three operational
phases and 11 ordered gates, but those are catalog data, not validator
cardinality assumptions. Accepted architecture or physical-method winners
remain zero, produced product algorithms remain zero, and all 21 audit
families remain unresolved candidates. This section records repair history; it
does not authorize execution or claim that the repaired snapshot has passed
the required final hostile recheck.

## Repaired execution-artifact root seal

The root reviewer reread the repaired contracts, packet, schemas, validator,
phase/dependency rationale, architecture-selection rules, algorithm registry,
and compact storage model before freezing a second hostile-review input. The
substantive digest produced by the exact command published in `HANDOFF.md` is:

`515154893e339e288bb04b659e87192ef95a46410a33b9b3f300e5890897706c`

An interim calculation had stripped the leading `./` from each filename before
hashing the aggregate ledger and produced a different string. No file-byte
identity was wrong, the per-file manifest still verified, and that interim
aggregate was never dispatched to a reviewer. The manifest header was corrected
to the output of the published command; only that exact command is canonical.

The unmodified repaired package passed `python3 -B execution/validate.py` with
1,163 checks and independently verified every draft-manifest row. A 19-case
semantic mutation suite then established:

- same-value and conflicting duplicate JSON members fail at the top level and
  recursively;
- missing, reordered, and duplicated `evaluation.md` responsibility markers
  fail;
- valid two-phase/two-gate and four-phase/four-gate catalogs, including a gate
  with three legal PASS output alternatives, do not hit a hidden current-
  topology ceiling;
- backward phase movement and a gate/phase-ID mismatch fail;
- packet-authored attestation bytes cannot authorize dispatch without external
  verifier configuration, unpinned verifier bytes fail, and actor/authorizer/
  verifier aliasing fails;
- FIFOs, Unix sockets, and cache directories fail complete inventory; and
- the input-lock minimum equals the six controlled pre-result notes.

A separate full-CLI suite copied the package into isolated temporary roots and
confirmed fail-closed diagnostics for five integrated attacks: a duplicate
catalog key, reordered evaluation regions, a FIFO, a Unix socket, and an
undeclared ninth packet file. Every copy and special file was deleted after the
test. The original package passed all 1,163 checks again.

The root also reverified all 68 source-manifest rows and all 20 entries in the
sealed P4 run-artifact manifest. This preserves Stage 4.6 as verified historical
negative evidence but does not repair its missing causal source/build closure;
`R_stage46` remains `INCOMPARABLE`. The algorithm registry has exactly 21
unique `AF-001`–`AF-021` rows in both its disposition and cost crosswalks, while
selected, mandated-novel, proved-novel, architecture-winner, physical-method-
winner, and joint-profile-winner counts all remain zero.

The reserved product worktree was not modified. It remained clean on
`codex/new-2.0-storage-core`; `HEAD`, local `origin/main`, and remote
`refs/heads/main` were all
`e4974d1f9aac702b35e052629cb070c897989352`, and the tree remained
`5d04b31c26bf37e4f62435fe12febfda26ca9719`. The docs repository stayed on
`layerstack_2_0`; unrelated owner modifications and untracked files were not
touched.

Root finding ledger after repair: `P0 = 0`, `P1 = 0`, `P2 = 0`. This is a
structural/documentation result, not an end-state guarantee. Phase 0 remains
`DRAFT / NOT_RUN`; no architecture, method, algorithm, benchmark claim,
migration, cutover, retirement, or release is accepted. The only next permitted
review action is a fresh isolated hostile review of the exact substantive
digest above.

## Second execution-artifact hostile panel and authority/minimality repair

The next isolated hostile panel reviewed substantive digest
`515154893e339e288bb04b659e87192ef95a46410a33b9b3f300e5890897706c`
and full-tree digest
`ab842b352d092302b52fb2b9da2b8e8471d9b04d9a000b1ef84dedecdc79aa19`.
That 55-file snapshot had six schemas, eight persistent files in the reusable
packet and active Phase 0 packet, and six lock-controlled notes. The three
reviewers did not inherit the root verdict. Their raw ledgers were:

| Hostile lane | Raw ledger | Material challenge |
|---|---:|---|
| algorithms, exact COW, and complexity | `P0 = 0`, `P1 = 0`, `P2 = 0` | the algorithm inventory, same-`StateId` zero-copy COW law, complexity bounds, and `R_stage46 = INCOMPARABLE` classification survived attack |
| lifecycle, authority, and cleanup | `P0 = 2`, `P1 = 0`, `P2 = 0` | same-phase producer authority could be self-asserted, while acceptor independence compared only an identity string rather than authenticated principal, credential, and control-domain axes |
| architecture, verifier rotation, and packet minimality | `P0 = 1`, `P1 = 1`, `P2 = 0` | one global verifier build/trust-root tuple could not validate current and preserved historical artifacts after rotation; `spec.md` and `decisions.md` still shared every relevant lifecycle boundary and were not irreducible |

The `P0` findings invalidated that snapshot. The package was explicitly
**UNFROZEN**; its digest and PASS statement remain historical evidence only.
The repair deliberately removed authority duplication and one packet file
instead of adding an authority service, sidecar, daemon, or seventh schema:

1. one principal triple—`principal_id`, `credential_fingerprint`, and
   `control_domain_fingerprint`—now represents every security-relevant actor;
   authenticated actions add a bounded proof, and producer/acceptor,
   authorizer/actor, and verifier/action separation is checked on all three
   axes;
2. phase-entry actors carry only sorted exact `produce:<gate-id>` and
   `accept:<gate-id>` capabilities; wildcards, roles, free-text scope, and
   implicit same-phase authority were deleted;
3. `input-lock.producer` is the sole producer authority fact and
   `manifest.producer` was deleted; a later same-phase gate resolves its
   governing phase-entry actor set transitively through exact independently
   accepted predecessor bytes rather than copying authority pointers;
4. the three global verifier flags were replaced by one externally pinned,
   write-denied per-artifact policy. Each exact phase-entry attestation,
   input lock, and final acceptance selects its retained verifier build,
   trust root, and `CURRENT_AUTHORITY` or `HISTORICAL_VERIFY_ONLY` use. This
   makes verifier/root rotation compatible with exact historical replay;
5. `spec.md` and `decisions.md` were fused into marker-separated `plan.md`.
   The validator independently checks both ordered, nonempty responsibility
   regions and their headings, locks the whole file byte-for-byte, and rejects
   either obsolete filename; and
6. the persistent packet contract is now seven files, with five controlled
   Markdown notes and the unchanged acyclic producer-manifest/independent-
   acceptance boundary. Seven is a justified stopping point, not a claim that
   no more complex representation could use fewer inodes.

The repaired population is 53 regular files: 40 Markdown, 12 JSON, and one
Python validator. It contains six schemas, seven reusable packet files, seven
active Phase 0 packet files, and five lock-controlled notes. Phase 0 remains
`DRAFT / NOT_RUN`; phases 1 and 2 remain uninstantiated. No protected artifact
or result exists, so the checked-in draft still requires no external policy.
This section records why the preceding seal was rejected and how it was
repaired; it does not itself seal the repaired bytes or authorize Phase 0
execution.

## Root authority-lifecycle audit before the third hostile panel

The root did not immediately reseal the preceding repair. A full authority-
lifecycle trace found two additional fail-closed obligations that were stated
by the design but not yet represented precisely enough in executable checks:

1. a later same-phase descendant may be invalidated while the canonical phase-
   entry packet remains current. The descendant input lock and acceptance are
   historical artifacts, but the still-canonical entry attestation remains
   current authority. Verification use is now derived independently from the
   packet that owns each protected artifact; ordinary descendant invalidation
   does not invent a replacement phase grant, while a true attestation,
   verifier-build, or trust-root change still invalidates the entry lineage;
   and
2. phase entry fixes the complete maximum actor capability set for the phase.
   The union of exact actor grants must now equal both `produce:<gate-id>` and
   `accept:<gate-id>` for every gate in that phase, with no out-of-phase or
   malformed grant and no actor holding both sides of one gate. Later execution
   therefore cannot dead-end because entry silently omitted a gate, expand
   authority in a descendant packet, or collapse independent production and
   acceptance into one principal.

The validator's built-in authority regressions now cover a current phase entry
consumed by an archived descendant, a completed historical phase, an exhaustive
separated capability union, a missing capability, and a dual-side grant. The
whole-plan hostile prompt requires those exact attacks rather than treating the
prose as proof. This audit introduced no packet field, schema, component,
service, daemon, cache, or product edit. The contract remains seven persistent
packet files, five controlled Markdown notes, and six machine-readable formats.

At this point the validator reached 1,234 checks and failed only the three
expected draft-manifest rows changed by these repairs. That is a pre-seal
diagnostic, not a PASS. Phase 0 remains `DRAFT / NOT_RUN`, phases 1 and 2 remain
uninstantiated, and the package remains open until its manifest is regenerated
and a new isolated hostile panel reviews the resulting exact bytes.

## Third execution-artifact hostile panel and root repair

The root then regenerated the package inventory and sealed substantive digest
`39f06d15767b2fa9e32289ba9301187850ad6e3983589b5ca420fd93e81c72d0`
and full-tree digest
`3ee25892b4ab62cb0d07f52b441d70ebfb78f73d4380ed77d0cc27a62bf5e83e`.
The exact 53-file package passed `python3 -B execution/validate.py` with 1,234
checks before dispatch. Three new isolated reviewers started from those bytes,
read the source and Stage 4.6 evidence rather than inheriting the root verdict,
and attacked architecture/minimality, algorithms/performance, and
lifecycle/authority independently. Their material counterexamples invalidated
that seal:

1. the input lock authenticated only the pre-result producer action; a final
   `SEALED` manifest could still report results without a distinct
   domain-separated proof by the same authorized producer;
2. an external verifier could be hashed through one filesystem lookup and then
   executed through another pathname lookup, permitting a hash-to-exec object
   substitution;
3. lifecycle state did not yet give both ordinary `ADVANCE` and `INVALIDATE`
   one authenticated, serialized, externally committed transition chain with
   retained exact predecessor-state bytes; and
4. the candidate `StateId` discussion still leaned on impossible mathematical
   digest injectivity and did not make unequal-byte collision rejection a
   prerequisite to the accepted reference-only COW fast path.

The package was explicitly **UNFROZEN**. The repair reused the existing seven
packet files, six schemas/formats, external-policy boundary, and state file; it
added no product service, daemon, component, cache, strategy interface, or
selected algorithm:

- manifest schema version 3 makes `producer` null before `SEALED` and requires
  the authenticated final producer action afterward. The proof uses the
  domain `ephemeral-sandbox/v2/gate-producer-seal`, covers the complete RFC
  8785 manifest projection with only `producer.proof` omitted, must have the
  exact input-lock producer triple and capability, and is independently
  verified as `manifest -> exact input lock` before acceptance;
- external-policy version 2 opens policy and native ELF verifier objects once
  through no-follow component traversal, hashes and executes the same retained
  descriptor on Linux, rejects writable/nonregular/script/oversized objects,
  fixes environment and time/output bounds, and permits no pathname fallback;
- execution-state schema version 2 gives both `ADVANCE` and `INVALIDATE` one
  transition record. Each transition binds the exact raw predecessor state,
  complete prior packet prefix, exact replacement, publisher intent, genuine
  conditional-write or exclusive-lease identity, independent publication
  authority, and an externally authenticated one-shot commit result. Every
  predecessor raw state and exact packet identity must remain recursively
  available; a state visible without its commit evidence is unusable; and
- `StateId` is now explicitly a finite candidate digest. Equal facts imply
  identical canonical bytes and candidate ID, while accepted same-ID states
  must have identical complete canonical bytes. An occupied candidate is
  compared byte-for-byte: equal bytes coalesce; unequal bytes terminate as
  `T03_REJECTION / STATE_ID_COLLISION` before any alias, root, head, mapping,
  index, custody, revision, or capacity effect. Only an already accepted
  no-alias binding may take the zero-immutable-payload-I/O COW path. A forced
  collision seam is qualification-only and is neither a production interface
  nor a product algorithm.

The root reread found one further fail-closed sequencing defect before reseal:
the validator accumulated diagnostics, so a malformed policy or an earlier
local/package failure could still reach a later external-verifier launch.
Authority policy loading now treats every path, byte, digest, catalog, shape,
ordering, and identity error as an execution barrier. All non-executing
filesystem, schema, lineage, state, seal, text, and package-manifest checks run
before authority dispatch; any earlier error prevents every launch, and the
first authority failure prevents later verifier launches. The exact-FD
self-test returned:

```text
PASS authority exact-fd self-test: protected dispatch is fail-closed on this platform
```

Immediately before this reseal, the full validator reported only the 43
expected stale hashes caused by the repair: five active controlled-note rows
and 38 package-manifest rows. It reported no independent structural or semantic
error. The active packet remains `DRAFT / NOT_RUN`, has no input lock, protected
artifact, final producer seal, or acceptance, and therefore does not require a
live authority policy. Phases 1 and 2 remain uninstantiated. Accepted product
algorithms, architecture winners, physical-method winners, joint-profile
winners, and performance guarantees all remain zero. The current three phases,
11 gates, 21 audit families, and eight later tournament families are inventory
and evaluation structure, not selected product algorithms.

This section records a rejected seal and the repair made after it. It does not
authorize execution. A regenerated exact package must pass validation and a
new isolated hostile panel before the artifact-system handoff can be closed.

## Final hostile-review input seal

After all repairs above, the root regenerated the active packet hashes and the
complete 52-row draft manifest. The canonical substantive digest, excluding
only the generated draft manifest and this chronological review record, is:

`78593632efd99d71dd1e14ba3aed6cdb5510ff39bff06c22ac6b68ff4aec6dd5`

The candidate contains exactly 53 regular files: 40 Markdown, 12 JSON, and one
Python validator; six schemas/formats; seven reusable packet files; seven
active Phase 0 packet files; five controlled Markdown notes; three catalog
phases; and 11 catalog gates. There are no symlinks, special files, empty
directories, cache directories, or generated bytecode files. Before hostile
dispatch, all of the following passed against the same bytes:

```text
PASS execution artifact contract: 1243 checks
PASS authority exact-fd self-test: protected dispatch is fail-closed on this platform
PASS draft manifest: 52 rows
PASS source manifest: 68 exact files
PASS Stage 4.6 P4 run seal: 20 exact artifacts
```

The reserved implementation worktree remained clean on
`codex/new-2.0-storage-core`; `HEAD`, local `origin/main`, and remote main were
all `e4974d1f9aac702b35e052629cb070c897989352`, with tree
`5d04b31c26bf37e4f62435fe12febfda26ca9719`. It was not modified. The docs
repository remained on `layerstack_2_0`, and unrelated owner changes were not
touched.

This snapshot is frozen for a completely new isolated hostile panel. Reviewers
must begin from these exact bytes and may not inherit an earlier verdict. The
seal is a review input only: Phase 0 remains `DRAFT / NOT_RUN`, phases 1 and 2
remain uninstantiated, and accepted product algorithms, architecture winners,
physical-method winners, joint-profile winners, and performance guarantees all
remain zero.

## Hostile panel over the preceding seal and bounded repair

Three isolated reviewers reread the complete sealed corpus without editing it.
The algorithm/performance lane accepted the package with no P0, P1, or P2
finding. It independently reconstructed the exact external-sort I/O equation,
the max-over-time scratch equation, the whole-record packing counterexample,
the exact no-alias COW closure law, collision admission, memory/cache cleanup,
joint selection, MCTS neutrality, and the Stage 4.6 `INCOMPARABLE`
classification. It confirmed that selected, proved, mandated, and winning V2
product algorithms all remain zero.

The architecture lane found no correctness blocker. It retained the current
three-phase scope and proved all 11 causal gates locally irreducible under the
package's independent hash, acceptor, failure, time, invalidation, and
predecessor-reuse semantics. A two-phase static-authority envelope remains a
coherent Phase 0 challenger only if existing machinery can prove fixed actors,
fixed capabilities, holdout isolation, predecessor-conditioned dispatch, live
revocation, and no later grant. That proof does not exist yet. A one-phase
system is not equivalent. The reviewer also constructed an optional three-file
packet representation by fusing the five Markdown notes into one marker-
partitioned file. It removes inodes but not semantic responsibilities, makes
one file own five SRP concerns, and is not required for correctness. Because
the user requested the three-phase artifact system and the current seven-file
contract already disclaims a global minimum, neither challenger was promoted
or used to rewrite this handoff.

The lifecycle and architecture lanes did expose three bounded machine-contract
defects in the preceding seal:

1. `execution-state.schema.json` repeated the current catalog size with one
   `maximum: 11` and two `maxItems: 11` keywords even though executable state
   equations derive all three cardinalities from `gates.json`;
2. an invalidation receipt row could preserve arbitrary content-addressed bytes
   because the documented one-shot verifier contract authenticated state
   publication but did not require authenticated receipt causality; and
3. schema-file validation checked only root names and metadata, allowing a
   reject-all or permissive nested branch to survive after manifest
   regeneration.

The package was unfrozen and repaired without adding a packet file, schema,
service, component, daemon, cache, algorithm, or product edit:

- the three literal topology bounds were deleted; independent 64-transition
  history bounds remain, while catalog length and exact prefix/suffix equations
  own topology cardinality;
- `validate.py` now seals the complete non-annotation semantic projection of
  each of the six schemas and explicitly rejects topology cardinality keywords
  at the three former state paths. The Python validator is the sole package-
  acceptance authority and the schemas are reviewed interoperability
  projections, so a root `allOf`, nested permissive branch, weak digest rule,
  removed unknown-field guard, or other semantic drift cannot pass merely by
  regenerating the package manifest; and
- an `INVALIDATE` state dispatch now resolves exactly one content-addressed
  receipt from the canonical replacement lineage and passes its path, digest,
  and derived earliest owner to the existing `ONE_SHOT_STATE_COMMIT` verifier.
  `PASS` now requires that verifier to authenticate the exact receipt under its
  pinned trust root and bind the exact prior state, ordered prior frontier,
  replacement, explicit changed dependency or predicate, and earliest owner.
  The receipt remains an opaque external evidence format; no seventh schema was
  invented.

This is a repair record, not a seal or phase result. The active Phase 0 packet
remains `DRAFT / NOT_RUN`; phases 1 and 2 remain absent; the product worktree
remains out of scope and unchanged. The modified package must be regenerated,
validated, and reviewed from a new exact input seal before handoff can close.

## Fourth hostile panel, root adjudication, and aggressive reduction

The next frozen input had substantive digest
`2a31d85e6d1039b23b971c3a1a3fc654e0498b0e62b3f8e10f4a98465a39418c`,
full-tree digest
`d9ebc9f56703bca3504de77ec4c81cc8ba33b9e8a99c68ee2e9defe74dc3175d`,
53 regular files, a 52-row draft manifest, and a 1,253-check validator PASS.
Fresh isolated algorithm, architecture, and authority-lifecycle reviewers began
from that exact seal. They were told that every mechanism and phase boundary
was a hypothesis, not the intended answer. The package remained read-only
during their sampling. Each lane produced one material counterexample:

1. **Algorithm/performance P1 — collision/COW contradiction.** Several owning
   documents required exact canonical-byte comparison in “every reference fast
   path” while also requiring the complete accepted reference-only operation
   to perform exactly zero immutable-payload reads. Both cannot be true for an
   occupied digest. The corrected contract separates candidate-bearing
   admission from reference-only transition: admission compares complete
   canonical candidate bytes against an occupied binding; unequal bytes reject
   before effects. A reference-only transition consumes only a previously
   admitted, authorized no-alias binding and never receives, rereads, or
   compares immutable payload. Candidate-bearing input at a reference API is
   rejected or routed to admission before fast-path entry. The qualification
   collision seam covers that ingress without weakening the zero-I/O COW law.
2. **Architecture/minimality P2 — seven files were reducible.** Five persistent
   Markdown notes had distinct semantic responsibilities but did not require
   distinct inode authority. The countermodel fused them into one exact
   marker-delimited `packet.md`, leaving `manifest.json` as the producer seal
   and dependency owner and `acceptance.json` as the independent verdict. The
   root accepted the reduction. The validator still checks all five regions,
   their internal plan/evaluation partitions, ordered unique markers, required
   headings/anchors, nonempty responsibility bodies, input-lock identity, and
   whole-file manifest digest. A region digest is mechanically derivable from
   the documented domain-separated marker grammar; storing four additional
   digests or files would repeat authority without adding an independent fact.
3. **Authority-lifecycle P0 — executable hash did not close native loading.** A
   retained dynamic ELF could pass the old exact-descriptor hash and then load
   an unpinned interpreter and shared libraries. External verifier policy is
   now version 3. A strict bounded parser accepts ELF32/ELF64 in either byte
   order but rejects truncation, unsupported identification, malformed or
   out-of-bounds headers/program tables/segments, `PT_INTERP`, and
   `DT_NEEDED`. Protected dispatch therefore requires one self-contained static
   native object. The separately pinned verifier-build/trust contract forbids
   runtime delegation to unpinned helpers, plugins, interpreters, shared
   objects, or dynamically loaded code; no pathname, loader, library, helper,
   or plugin fallback exists. Negative fixtures exercise each rejected class
   before the existing exact-open-descriptor execution test.

The root independently retraced the three-file lifecycle before resealing.
Fusing `packet.md` with `manifest.json` creates a self-hash/projection problem;
fusing `acceptance.json` with the manifest mutates the producer-sealed object or
requires a more complex partial-object hash; and fusing acceptance with the
controlled packet mutates the exact pre-result input after lock. Thus the
remaining three files each own a non-fusible byte-lifecycle boundary even
though the five human responsibilities share one document. The root also
deleted a tautological `packet_section_sha256` helper that computed a digest
only to assert that SHA-256 output looked like a digest; the whole-file seal and
fixed markers already make exact region hashes derivable.

The mechanical reduction is exact:

- ten old note files—five template notes and five active notes—became two
  `packet.md` files, a net deletion of eight regular files;
- persistent files per packet fell from seven to three, a reduction of four
  files or 57.1%;
- controlled pre-result Markdown artifacts fell from five to one, a reduction
  of four artifacts or 80%, while all five semantic responsibilities remain;
- the package population fell from 53 to 45 regular files: 32 Markdown,
  12 JSON, and one Python validator;
- schemas remain six; phases remain three; causal gates remain 11; new product
  components/services/processes/deployables remain zero; and
- algorithms mandated, proved, selected, or produced remain `0 / 0 / 0 / 0`.

This bounded repair added no product edit, product dependency, packet schema,
service, daemon, cache, physical-method winner, architecture winner, or
performance guarantee. Phase 0 remains `DRAFT / NOT_RUN`; phases 1 and 2 remain
uninstantiated. The package is **UNFROZEN** until its 44-row manifest is
regenerated, all checks pass, and fresh closing reviewers accept the new exact
substantive seal.

## Fifth closing seal rejected and root-bounded repair

The next root seal contained 45 regular files and 44 manifest payload rows. Its
substantive digest was
`29d2f75e0a6f1226db6bacddc1d020e1acf7fefd077dee88cc767c9e43f27ce0` and
its full-tree digest was
`086870b043b47833a8e3944c73a8567a6835b6e4764bf73ffcc066e16627bfbe`.
The package validator passed 1,183 checks, the 68-row source manifest and
20-entry historical P4 seal were exact, the reserved product worktree remained
clean at the recorded e497 identity, and the platform authority self-test
failed closed on macOS. Those checks made the bytes reviewable; they did not
make them acceptable.

A new isolated algorithm/COW/performance reviewer read all 45 files and
recomputed both opening and closing digests. It rejected the seal with
`P0 = 0`, `P1 = 1`, and `P2 = 0`: one storage-model row required metadata work
independent of existing-root count even though `DEC-009` and `AF-018` leave an
exact bounded scan versus index/revalidation decision open. A scan may preserve
the four zero selected-payload/private-closure counters while taking
`Theta(R_root)` metadata work. The sentence therefore selected an index-like
complexity shape before the tournament.

The repair replaces that false bound with explicit population accounting.
Every candidate must name the semantic-root, pin/backup-hold, reader/read-view,
custody, and candidate-specific rows that it scans or indexes and give finite
exact best, expected, worst, and amortized metadata-I/O, update, memory,
synchronization, and contention bounds as functions of the applicable
cardinalities. Those bounds remain independent only of selected immutable
closure/payload bytes. No scan or index is selected; last-root races remain a
proof obligation. `design/storage-model.md`, `algorithms/registry.md`, and
`decisions/README.md` now state the same method-neutral rule.

The root reviewer independently found a digest-to-execution race in the
external authority-verifier path. Opening a write-denied source once and then
hashing and executing its descriptor did not prevent an actor with an already-
open writer from changing the same inode after the final stat check. The
validator now copies at most 64 MiB into one anonymous memfd, makes that
descriptor close-on-successful-exec, atomically applies
`F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL`, verifies the full
seal mask, closes the source, and only then hashes, parses, and executes the
same sealed clone. There is no unsealed-FD, pathname, interpreter, dynamic-
loader, helper, plugin, shared-library, or copy-to-disk fallback.

The same root pass found that a verifier could close stdout and stderr and then
hang, causing the prior code to leave the deadline loop and block in a plain
`waitpid`. The watchdog now polls the child until the same monotonic deadline
even after both pipes close, then kills/reaps the process group. One sequential
child receives `/dev/null` stdin, fixed `argv[0]` and environment, and limits of
256 MiB address space, one process, 32 descriptors, zero regular-file output,
no core dump, and bounded CPU and wall time. The clone, source, pipes, selector,
and child are never cached and are closed, killed, or reaped on every terminal
path.

The Linux self-test passed both executable-custody counterexamples: sealed
write/truncate attempts failed, the approved clone executed after in-place
source mutation and path replacement, and a child that closed both output
pipes could not bypass a 100-ms deadline. The pre-existing Lima VM used only
for that kernel-dependent test was returned to its prior `Stopped` state. The
macOS self-test still proves that protected dispatch has no non-Linux fallback.

These repairs add no product algorithm, architecture winner, physical-method
winner, package, schema, service, daemon, cache, or product-worktree edit. They
also do not retroactively repair the rejected seal. The package remains
**UNFROZEN** until its controlled packet digest and 44-row manifest are
regenerated, all deterministic checks pass, and a new from-start hostile panel
accepts one unchanged replacement seal.

## Sixth hostile panel rejected stale post-fusion schema cardinalities

The root resealed 45 regular files and 44 manifest payload rows with substantive
digest
`1bf2bc40f5ba806bfce2e22ce89356f5a363450aca09070317069314456ad71d` and
full-tree digest
`5ead192e01df970a6de1115352b4815bb1ca540b00c629752e8d6ebb49b4d0fe`.
Three new isolated hostile reviewers independently read all 45 files from byte
one through EOF, verified 44/44 manifest rows, recomputed matching opening and
closing digests, and made no edits. The algorithm/performance,
architecture/minimality, and execution-lifecycle lanes each returned the same
verdict: `REJECT`, with `P0 = 0`, one common-cause `P1`, and `P2 = 0`.

The common cause was residue from the earlier five-to-one controlled-artifact
fusion. `manifest.schema.json` still required at least five artifact rows even
though the canonical template, active Phase 0 manifest, controlled-file set,
and executable validator intentionally require the single fused `packet.md`.
`input-lock.schema.json` retained the same stale floor even though one
controlled packet snapshot is the format-level minimum; a phase-entry lock
adds its separately required authority receipt and attestation under the
executable context rule. Consequently a conforming Draft 2020-12 consumer had
to reject canonical bytes that the package validator accepted. The reviewed
semantic hashes preserved the contradiction instead of detecting it.

The bounded repair changes both format-level floors from five to one, updates
the two reviewed semantic-schema digests, and adds executable cross-contract
checks requiring both schema floors to equal the cardinality of
`CONTROLLED_PACKET_FILES`. Existing validator checks already require the
template and every instantiated manifest to name exactly that controlled set,
require every input lock to contain it, and add the two exact authority
snapshots at a phase boundary. Together these checks make another packet-file
fusion or split fail unless its schemas and executable rules change in the
same reviewed patch; no JSON Schema engine, dependency, duplicated packet
model, or seventh schema was added.

The panel found no additional architecture, phase-ordering, lifecycle,
resource-safety, COW-accounting, algorithm-neutrality, benchmark-provenance, or
future-runtime defect. In particular, the root-cardinality repair survived,
the phase count remains a conservative local stopping point rather than a
global-minimum claim, and algorithms mandated, proved, selected, or produced
remain `0 / 0 / 0 / 0`. This record is not a passing seal: Phase 0 remains
`DRAFT / NOT_RUN`, phases 1 and 2 remain uninstantiated, and the product
worktree remains untouched. The repaired package must be regenerated,
revalidated on its supported platform paths, and accepted by a new from-start
hostile panel against one unchanged replacement seal.

The root replacement seal then passed 1,185 executable-contract checks and all
44 manifest payload rows. The macOS protected path again rejected any unsealed
fallback. The Linux path accepted the static closure, rejected dynamic and
malformed ELF inputs, rejected writes and truncation after sealing, executed
the hashed clone despite source mutation and pathname replacement, and killed
and reaped the closed-output-pipe timeout fixture. The pre-existing Lima VM was
returned to its prior `Stopped` state. The replacement substantive digest is
`6a76df66c219e570fa253b4c2ba38c4838276c14d2d7da971944fac55cd7badc`.
These root checks establish a reviewable input, not acceptance; a new isolated
panel must recompute both opening and closing seals and return no unrebutted
P0/P1 before the package can be frozen for handoff.

## Seventh hostile panel rejected exceptional verifier cleanup

The next exact candidate contained 45 regular files and 44 manifest payload
rows. Its substantive digest was
`6a76df66c219e570fa253b4c2ba38c4838276c14d2d7da971944fac55cd7badc`
and its full-tree digest was
`18a603f047d50894a16ad328f241826f96469c11c1c70088217ba25019f36ac8`.
All three fresh reviewers read every regular file from byte one through EOF,
verified 44/44 manifest rows, recomputed identical opening and closing seals,
and made no edits. The architecture/minimality and
algorithm/COW/performance/evidence lanes returned `ACCEPT`, each with
`P0 = 0`, `P1 = 0`, and `P2 = 0`. The lifecycle/resource-safety lane returned
`REJECT`, with `P0 = 0`, `P1 = 1`, and `P2 = 0`.

The P1 was exact: the verifier child calls `setsid()`, and timeout or output
overflow killed that process group, but a parent-side `OSError` after `fork()`
entered a finalizer that killed only the leader PID. `RLIMIT_NPROC = 1` was not
a proof that no descendant existed because Linux exempts real UID zero and
processes with applicable resource or administrative capability. A privileged
verifier descendant could therefore retain execution and inherited resources
after the leader was killed and reaped.

Root reproduced the counterexample before changing production behavior. A
sealed `/bin/sh` fixture created one background descendant, transmitted the
leader and descendant IDs over an inherited pipe, retained a second lifetime
pipe, and then encountered an injected parent-side selector `EIO`. The old path
returned exit 127 while the descendant and process group remained live. The
isolated Linux container fixture killed that group before exiting. The same
case was then installed as a root-only Linux regression; against the old code
it failed exactly with `post-fork exception left a live verifier descendant`.

The bounded repair introduces one process-group termination primitive and one
interruption-safe direct-child reap primitive. The normal timeout/overflow path
and the unconditional post-fork finalizer now share them, and finalization
terminates/reaps before closing fallible selector and pipe resources. The
regression accepts only after the descendant-held lifetime pipe reaches EOF;
its own failure cleanup kills the fixture group.

The reproduction also disproved the prior unqualified “one process” wording.
Protected authority dispatch now fails closed unless real, effective, and
saved UIDs are all nonzero and the inherited, permitted, effective, and
ambient Linux capability sets are all empty. Missing or malformed procfs
capability state is ineligible. Only under that predicate does
`RLIMIT_NPROC = 1` establish the one-process execution bound. Process-group
termination remains necessary for pre-limit failures and defense in depth.
The privileged Linux regression now passes both the privilege-ineligibility
predicate and the injected exceptional-cleanup case.

This repair adds no product edit, schema, service, daemon, cache, architecture
winner, physical-method winner, selected algorithm, or performance guarantee.
The three phases, 11 causal gates, and three persistent files per packet remain
unchanged. Phase 0 remains `DRAFT / NOT_RUN`; phases 1 and 2 remain absent; the
product worktree remains untouched. This rejected seal cannot be accepted
retroactively. The package is **UNFROZEN** until its manifest and exact digests
are regenerated, all root checks pass on the replacement bytes, and a new
from-start hostile panel returns no unrebutted P0/P1.
