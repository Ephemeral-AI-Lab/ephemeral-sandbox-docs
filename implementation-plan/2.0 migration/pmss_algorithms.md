---
title: PMSS Algorithm and Qualification Workbook
aliases:
  - Portable Merkle State Store Algorithms
  - PMSS Algorithms
tags:
  - ephemeral-sandbox
  - storage
  - pmss
  - algorithms
status: proposed-implementation-companion
authority: non-normative
production_qualification: open
version: 1
updated: 2026-08-02
related:
  - "[[implementation-plan/2.0 migration/system-design/index|Accepted PMSS system design]]"
  - "[[implementation-plan/2.0 migration/system-design/system_requirements|PMSS system requirements]]"
  - "[[implementation-plan/2.0 migration/system-design/architecture/mpla_demonstrations|PMSS demonstrations]]"
  - "[[implementation-plan/2.0 migration/phase 1/prompts/pmss-harsh-minimal-algorithm-architecture-review|Harsh minimal PMSS algorithm and architecture review prompt]]"
---

# PMSS Algorithm and Qualification Workbook

> [!important] Authority and scope
> This is a non-normative navigation, implementation, and qualification
> workbook for the accepted ten-document PMSS design. It introduces no
> architecture, format, lifecycle, resource, or accepted performance
> requirement. Each linked sole-authority document governs its definitions and
> gates; if this workbook differs, this workbook is wrong. Proposed
> implementation details and targets are labelled explicitly. This workbook
> authorizes no production-code change.

> [!warning] Exactness boundary
> The linked architecture is accepted; this derived workbook is not.
> Production qualification is open until every symbolic codec, FD,
> scratch-space, and HEAD constant named below is frozen and measured.
> It separates analytical bounds, project measurements, external measurements,
> targets, estimates, and hypotheses; it never upgrades an unmeasured number
> into a result.

## 1. Decision in one page

The storage system is named **Portable Merkle State Store**, abbreviated
**PMSS**.

PMSS stores complete immutable filesystem states. It does not store a logical
stack of layers:

- a publish builds or reuses one complete candidate StateId;
- unchanged canonical objects are shared by ObjectId;
- a checkpoint stores one immutable reference to a StateId;
- a fork starts a new sandbox head at a checkpoint StateId;
- rollback changes a sandbox head to a checkpoint StateId;
- materialization realizes one complete StateId into one private workspace;
- garbage collection retains objects reachable from explicit semantic roots;
- physical Full and Delta records are replaceable encodings below ObjectId.

Therefore the production design **drops LayerStack, logical layers, squash,
autosquash, squash-driven remount, and history-depth lookup**. An import
adapter may read legacy layers during migration, but PMSS canonicalizes their
result into one complete state. Legacy layer boundaries do not survive as PMSS
identity or version history.

> [!success] Direct answer
> Squash is removed, not deferred. Repack and S3 group normalization solve
> physical fragmentation; exact trace and semantic-root deletion solve
> retention. Neither operation changes StateId, and neither is a renamed
> squash.

The concise mental model is:

~~~mermaid
flowchart LR
  W["Private workspace"] -->|"publish"| NS["Complete new StateId"]
  OS["Complete origin StateId"] -. "share unchanged ObjectIds" .-> NS
  NS --> H["Sandbox head + HeadRevision"]
  NS --> CP["Optional named checkpoint"]
  NS --> O["Canonical objects"]
  O --> C["ObjectCatalog"]
  C --> P["Full or depth-one Delta records in packs"]
  H -->|"materialize"| NW["New private workspace"]
~~~

The conclusion is important: the logical arrow is always StateId to complete
state. Delta is only an ObjectCatalog locator codec. No reader reconstructs a
state by replaying versions or walking prior publications.

## 2. Minimal vocabulary

The implementation and documentation should use only these storage terms.

| Term | Exact meaning | Not this |
|---|---|---|
| PMSS | Portable Merkle State Store | A database, filesystem, or LayerStack |
| Canonical object | One typed, deterministic, content-addressed value | A mutable row or host file |
| ObjectId | BLAKE3-256 of one canonical typed object envelope | A pack offset or version |
| StateId | ObjectId of the complete canonical `FilesystemRoot` | A delta, layer, commit sequence, or workspace |
| HeadRevision | Per-sandbox ABA/conflict token | StoreSequence |
| Checkpoint | Immutable named retention root for one StateId | A copied state or operational history entry |
| Catalog | Closed fixed-purpose immutable CoW B+ index | A general key-value store |
| HEAD | Sole physical selector for one Catalog root | A sandbox head or dual-slot election |
| StoreSequence | Monotonic physical S2 selection sequence | Semantic version |
| ArenaId | Which immutable Catalog arena HEAD selects | State identity |
| PackSegment | Sealed immutable physical record container | A logical layer |
| Full / Delta locator | Physical encoding of one complete canonical object | A state edge or edit history |
| OwnerSlot | One of 16 static durable custody lanes: maintenance-only slot 0 or foreground-only slots 1..15; `Build` stores only `owner_nonce` | A pin table, lease, reservation ledger, dynamic owner pool, or unbounded staging registry |
| ReadSlot | One of 64 volatile, 30-second reader protections | A durable lease |

Avoid introducing synonyms such as generation chain, layer delta, snapshot
log, version edge, squash point, compaction level, or materialization history.
They imply mechanisms PMSS deliberately does not have.

## 3. Versioning and lifecycle meaning

PMSS separates four concepts that older LayerStack wording mixed together.

| Identifier | Owner | Changes when | Stable meaning |
|---|---|---|---|
| StateId | Canonical State | Canonical filesystem or attribution facts change | Content identity of one complete state |
| HeadRevision | Lifecycle | A sandbox head is actually published, rolled back, or updated by fork commit | Per-sandbox semantic concurrency token |
| StoreSequence | Durable Store | Any S2 commit selects a new Catalog root, including receipt-only commits | Physical atomic-selection order |
| ArenaId | Durable Store | A dense rebuild switches selected Catalog arena | Physical layout selection |

A workspace session captures the exact origin pair `(StateId, HeadRevision)`
and one immutable internal `ActorId[32]` from the authenticated principal of
the accepted create request. Capture, changed-metadata ownership and C3 use
only that stored actor; publish retries never consult an ambient caller.
Publication succeeds only if the sandbox still has the origin pair. This
closes the ABA case: publishing identical content still increments
HeadRevision even though StateId remains equal. Either Terminal transition
drops the origin, actor and reservation. `Session/Terminal` is exactly
`{status, allocation}`: `PUBLISHED` derives `Published`, `CONFLICTED` derives
`PublishConflict`, and the retained `Receipt`—not a duplicate result
field—holds the exact original publication response. A later semantic publish
call on `PUBLISHED` returns `AlreadyPublished`.

Lifecycle operations translate as follows:

| User concept | PMSS transition | Payload copied? |
|---|---|---:|
| Publish | Build/reuse a complete candidate StateId; strict-origin S2 CAS advances sandbox head and HeadRevision | Only missing canonical objects |
| Checkpoint | Insert checkpoint ID to current StateId | No |
| Fork | Create child sandbox at checkpoint StateId with immutable parent/checkpoint provenance and derived pin | No |
| Rollback | Replace sandbox StateId with checkpoint StateId and increment HeadRevision when different | No |
| Fork commit | Apply the ordered P/C/B decision and possibly change the parent head | No |
| Remove checkpoint | Delete only the named semantic root if no child pin uses it | No immediate storage credit |
| Destroy session | Select an `AdapterClose` owner intent, fence/drain and synchronously dispose the private allocation, then conditionally delete the exact session row and clear the intent through S2 | Workspace bytes only |
| Materialize | Stream one complete StateId into a private ordinary-file allocation | Yes, portable fallback is linear |
| Repack | Change physical locators for live objects | At most one 64-MiB complete output pack per bounded step; its frames total at most `64 MiB - 8 B` |
| Squash | **No PMSS operation** | Not applicable |

The authoritative version rules are in
[[implementation-plan/2.0 migration/system-design/components/lifecycle_engine#Version rules|Lifecycle version rules]].

## 4. Architecture and algorithm registry

PMSS keeps four domain responsibilities and one permit-only shared service.

~~~mermaid
flowchart TB
  L["Lifecycle<br/>heads, sessions, checkpoints, forks"] --> C["Canonical State<br/>facts, objects, StateId"]
  L --> S["Durable Store<br/>packs, Catalog, HEAD, GC"]
  L --> A["Backend Adapter<br/>private workspace, fence, capture"]
  A --> C
  S --> C
  L --> R["Resource Admission<br/>fixed permits only"]
  S --> R
  A --> R
~~~

There are exactly **six project-owned custom mechanisms**: C1, C2, C3, S1,
S2, and S3. S2 is the sole custom crash protocol; the other five are custom
algorithms. Ordinary codecs, library calls, lifecycle transitions, and
composed workflows must not be promoted into extra named mechanisms.

The Lifecycle-facing Store port has exactly three top-level capabilities:
`open_read`, `stage_objects`, and `commit`. Pack append/read, sparse and dense
Catalog construction, recovery, exact trace, closure, rewrite, and retirement
remain internal compositions of those capabilities; they are not additional
Lifecycle-facing methods or services.

| ID | Name | Classification | Primary optimization |
|---|---|---|---|
| C1 | Canonical compressed Patricia/Merkle directory | Custom algorithm | Stable logical directory identity and local path changes |
| C2 | ContentTree-v1 bounded content-defined Merkle sequence | Custom algorithm | Local file-metadata resynchronization |
| C3 | Deterministic C2-run attribution tiling | Custom algorithm | Exact current attribution without edit history |
| S1 | Fixed-purpose immutable CoW B+ Catalog | Custom algorithm | Bounded point reads, sparse updates, dense rebuild |
| S2 | Single-HEAD dependency-first commit/recovery | Custom crash protocol | One atomic visibility/durability authority |
| S3 | AlignedSpliceDelta-v1 | Custom algorithm | Small retained same-interval edit storage |

Authoritative registry:
[[implementation-plan/2.0 migration/system-design/index#Custom mechanism registry|custom mechanism registry]].

## 5. Symbols and claim labels

### 5.1 Complexity symbols

| Symbol | Meaning |
|---|---|
| B_scan | Non-hole source-payload occurrence bytes read during stable capture (`B_src` in some proofs) |
| B_realize | Non-hole logical occurrence bytes written while realizing one workspace |
| F | Filesystem fact count |
| A_fact | Attribution fact count |
| S_fact | Encoded filesystem/metadata/attribution input bytes |
| C_candidate | Sum of canonical byte lengths of distinct candidate objects, including metadata and attribution |
| C_reuse | Sum of canonical byte lengths of distinct candidate objects reused from the selected Store |
| P_reuse | Exact physical selected-Store bytes read to reconstruct and compare every reused object once |
| P_new | Exact physical bytes written for missing objects, including record and pack framing |
| D_dir | Total length-delimited directory-key bytes supplied to one C1 build |
| K_path | Encoded path bytes traversed by C1 |
| P_C1 | Frozen maximum encoded C1 node bytes; a qualification prerequisite |
| n_frame | Total framed C2 entry bytes |
| N_C2 | Number of C2 entries |
| c_old / c_new / c_match | C3 origin, candidate, and matched whole-C2-run counts |
| c_frag / c_out / s_old | C3 inherited owner-fragment count, output append bound, and verified origin owner-span count |
| N_C3_record_max | One authoritative cap for every C3 scratch/output count: `2,097,152` (`2^21`) |
| N | Selected Catalog records |
| K | Distinct candidate ObjectIds in one publication, `K=|U_candidate|<=N_object_max` |
| K_delta | Candidate Delta-locator count, `K_delta<=K` |
| K_s1 | Changed Catalog records in one S1 sparse update |
| H | Catalog height, frozen at H <= 8 |
| C_max | Configured full-occupancy byte capacity of one complete Catalog; never recomputed downward from current live rows |
| N_object | ObjectCatalog record count in one captured basis |
| N_reach | Unique logically live canonical objects |
| N_delta | Selected Delta-locator count |
| N_pack / N_pack_max | Installed sealed PackSegments / hard pack-directory inode/quota-derived cap |
| N_pack_record | `PackCensusV1` records: one for every selected ObjectCatalog row plus one installed-pack inventory record |
| N_pack_record_max | `N_object_max + N_pack_max` |
| p | Victim-pack count selected by one rewrite batch, `1 <= p <= 64` |
| N_roots | Semantic content-root count in the captured basis |
| R_scan | Lifecycle rows examined while finding semantic roots |
| E_reach | Typed outgoing edge occurrences from logically live objects |
| B_reach | Verified bytes of logically live objects |
| U_reach | Total unique canonical information reachable from retained semantic roots after ObjectId sharing |
| L_trace | Number of state/summary levels in the exact trace file |
| P_changed | Distinct Catalog pages written by one S1/S2 commit |
| V_alloc | Allocation-rounded bytes of the `p<=64` selected victim packs |
| X_live | Verified live frame bytes copied by a bounded repack step, `X_live <= 64 MiB - 8 B` |
| X_alloc | Allocation-rounded replacement pack bytes including the exact 8-B signature and exact record frames, `X_alloc <= P_pack_alloc_max` |
| Y_norm | Verified Full frame bytes written by one bounded S3-normalization-only step |
| Delta | Newly written canonical bytes, not a logical version delta |
| A_alloc(x) | Checked physical allocation-rounding function |
| D_aux_max | Maximum allocation-rounded bytes for one Auxiliary Catalog arena |
| D_closure_scratch_max | Peak allocation-rounded bytes for the two sequentially reused Delta-edge and pack-census sort workspaces |
| D_root_ctl / I_root_ctl | Separately protected byte/inode reserve for the largest complete semantic-root-removal control workflow; bulk maintenance cannot borrow it |
| Sort(n) | Bounded external-sort cost for n records |

### 5.2 Evidence labels

Every numeric claim uses one accepted primary label:

| Label | Meaning |
|---|---|
| **PROJECT MEASUREMENT** | Project-produced data from a named workload, platform, sample set, and timing boundary |
| **EXTERNAL MEASUREMENT** | Data produced outside this project, with a direct source and scope |
| **ANALYTICAL BOUND** | A derived asymptotic or arithmetic bound |
| **TARGET** | A future qualification threshold; not an achieved result |
| **ESTIMATE** | An approximate value whose assumptions are stated |
| **HYPOTHESIS** | A plausible result requiring measurement |

Stage 4.6 values are historical **project measurements of the MPLA POC**, not
PMSS measurements. A target is not a promise. An expected local case never
replaces a stated worst case.

## 6. C1 — canonical compressed Patricia/Merkle directory

Authoritative definition:
[[implementation-plan/2.0 migration/system-design/components/canonical_state#C1 — canonical compressed Patricia/Merkle directory|C1]].

### Purpose

C1 gives byte-for-byte deterministic identity to a directory while avoiding
rank-shift rewrites when an early lexical entry is inserted. The input is a
strictly sorted unique stream of raw basename bytes and typed EntryValue IDs.

### Pseudocode

~~~text
BUILD_DIRECTORY(sorted_entries):
    require complete C1 resource claim
    require entries are strictly increasing by raw basename bytes

    stack = bounded compressed-prefix stack
    previous_key = NONE

    for (name, value_id) in sorted_entries:
        require 1 <= length(name) <= 255
        verify typed value_id
        key = LENGTH_DELIMIT(name) || TERMINAL

        if previous_key exists:
            require previous_key < key

        shared = LONGEST_COMMON_PREFIX(previous_key, key)
        while stack extends below shared:
            node_id = CLOSE_CANONICAL_NODE(stack.pop())
            APPEND_CHILD_TO_PARENT(node_id)

        OPEN_CANONICAL_PREFIXES(stack, key, shared)
        APPEND_ORDERED_EDGE_OR_TERMINAL(stack, key, value_id)
        previous_key = key

    while stack is not empty:
        node_id = CLOSE_CANONICAL_NODE(stack.pop())
        APPEND_CHILD_TO_PARENT(node_id)

    return VERIFY_ROOT(node_id)

LOOKUP_DIRECTORY(root_id, raw_path):
    node_id = root_id
    for encoded byte or TERMINAL in LENGTH_DELIMIT_COMPONENTS(raw_path):
        node = READ_AND_VERIFY_TYPED_NODE(node_id)
        require compressed prefix matches
        node_id = SELECT_ORDERED_EDGE(node, next byte or TERMINAL)
    return verified EntryValue
~~~

### Bounds

| Property | Bound |
|---|---|
| Full build | Theta(D_dir) over directory key bytes |
| Lookup/update path | O(K_path) verified C1 nodes for encoded path bytes |
| Path-update encoded output | O(K_path × P_C1) |
| RAM | Bounded path/builder stack plus one node page; exact formula below |
| Temporary disk | One charged nested tail-stack scratch spool |
| FDs | Three for the composed build: sorted input, scratch spool, candidate-pack output |
| Failure | Duplicate, unsorted, over-cap, corrupt, or mistyped input fails before publication |

C1 is logical identity. It must not be merged with S1, whose keys are opaque
physical Catalog keys.

To avoid a vector of up to 257 child IDs in every open Patricia frame, the
proposed implementation keeps only prefix/count/spool offsets in memory.
Closed child descriptors append to the current parent's tail region in one
charged scratch file. Closing a node streams that bounded region, emits the
node, truncates the region, and appends one descriptor to its parent.

Freeze these codec constants before qualification:

~~~text
K1_max       = maximum encoded basename key including delimiter/terminal
P1_max       = maximum canonical DirectoryNode frame
C1_frame     = exact in-memory open-frame width
R1_edge      = exact scratch child-descriptor width
H1_spool     = exact scratch header/control bytes
C1_codec     = exact hash/encoder/control scratch
E1_max(D)    = proved maximum scratch edge descriptors for D encoded key bytes
~~~

Then the executable bounds are:

~~~text
M_C1 = ALIGN_64(P1_max
                + 2 × K1_max
                + K1_max × C1_frame
                + C1_codec)
D_C1_scratch(D_dir) = A_alloc(H1_spool + R1_edge × E1_max(D_dir))
I_C1_scratch = 1
FD_C1_composed = 3
~~~

The Patricia proof must establish `E1_max(D_dir) <= D_dir` or freeze the
corrected coefficient. Until `K1_max`, `P1_max`, the frame/edge codec widths,
and that proof exist, C1 has deterministic asymptotics but not an exact byte
resource proof.

## 7. C2 — ContentTree-v1 bounded content-defined Merkle sequence

Authoritative definition and frozen profile:
[[implementation-plan/2.0 migration/system-design/components/canonical_state#C2 — ContentTree-v1 bounded content-defined Merkle sequence|C2]].

### Purpose

C2 represents each regular file as one complete ordered sequence of coalesced
HOLE and DATA descriptors. Content-defined boundaries usually resynchronize
metadata pages after a local edit, while the deterministic adversarial bound
remains linear.

### Frozen limits

| Item | Value |
|---|---:|
| Payload FastCDC min/target/max | 8 / 16 / 32 KiB |
| C2 boundary input min/target/max | 4,096 / 8,192 / 16,384 B |
| Encoded entry | <= 64 B |
| Entries per node | <= 512 |
| Canonical node payload | <= 16,512 B |
| Root level | <= 7, eight levels total |
| Open builders | At most eight |

### Pseudocode

~~~text
BUILD_LEVEL(level, entry_stream):
    chunker.RESET(DOMAIN_PREFIX(level))
    node = empty bounded builder

    for entry in entry_stream:
        encoded = CANONICAL_ENCODE(entry)
        require length(encoded) <= 64
        frame = U16BE(length(encoded)) || encoded

        chunker.FEED(frame)
        node.APPEND_WHOLE_FRAME(frame)
        require node.entry_count <= 512

        if chunker selected a cut in or before this completed frame
           or node.entry_count == 512:
            emit VERIFY_AND_SEAL_NODE(level, node)
            chunker.RESET(DOMAIN_PREFIX(level))
            node.CLEAR()

    if node is nonempty:
        emit VERIFY_AND_SEAL_NODE(level, node)

BUILD_CONTENT_TREE(leaf_entries):
    require leaf_entries exactly tile the regular-file logical length
    require adjacent holes are already coalesced

    if leaf_entries is empty:
        return CANONICAL_EMPTY_LEVEL_ZERO_NODE

    entries = leaf_entries
    for level in 0 through 7:
        nodes = BUILD_LEVEL(level, entries)
        if nodes contains exactly one node:
            return COLLAPSE_SINGLE_CHILD_ROOT_CANONICALLY(nodes[0])
        entries = verified internal descriptors for nodes

    fail CanonicalLimitExceeded
~~~

### Bounds

| Property | Bound |
|---|---|
| Full build | Theta(n_frame) framed entry bytes |
| Expected local edit output | O(log N_C2) changed C2 pages after resynchronization |
| Deterministic adversarial edit | Theta(n_frame) |
| Named builder buffers | 8 × 16,512 B + 32,768 B chunk + 16,512 B scratch = 181,376 B |
| Proposed allocation-free worker slab | Exactly 262,144 B; control headroom is exactly 80,768 B |
| Logical storage | Complete tree; unchanged nodes and chunks deduplicate by ObjectId |

~~~text
M_C2_named = 8 × 16,512 + 32,768 + 16,512 = 181,376 B
M_C2_claim = 256 KiB = 262,144 B
remaining_worker_headroom = 80,768 B
D_C2_temporary = 0
I_C2_temporary = 0
FD_C2_algorithm = 0
~~~

The expected-local result is an optimization expectation, not a worst-case
guarantee. Adversarial boundaries, sparse-layout changes, or broad metadata
changes can re-ground the complete descriptor sequence. Qualification must
fit the chunker, hash state, codec, input/output windows, alignment, error
state, and bookkeeping inside the remaining 80,768 B. After the slab is
admitted, the C2 algorithm may perform no heap allocation. A streaming
eight-level cascade feeds every sealed level-j descriptor directly into
level j+1, so it needs no repository-sized vector or temporary disk. The
181,376 B payload shape alone is not a complete RAM proof; compile-time size
assertions must prove the remaining control layout.

## 8. C3 — deterministic whole-run attribution

Authoritative definition:
[[implementation-plan/2.0 migration/system-design/components/canonical_state#C3 — deterministic C2-run attribution tiling|C3]].

### Purpose

C3 preserves exact current ownership without retaining an edit log. It pairs
identical complete C2 runs deterministically by occurrence rank, inherits the
origin owner spans intersecting each paired run, and assigns every unmatched
candidate run to the session-bound actor. The caller supplies the immutable
`Session/Mutable.actor_id` captured at accepted session creation, never an
ambient publish principal. This is exact deterministic
**whole-C2-run attribution**; it does not claim byte-diff or edit-intent
precision.

### Pseudocode

~~~text
OccurrenceV1: exactly 50 bytes
    kind:u8                 # HOLE or DATA
    len:u64
    chunk_id_or_zero[32]    # zero for HOLE; complete DataChunk ID for DATA
    side:u8                 # 0 origin, 1 candidate
    start:u64

MatchV1: exactly 16 bytes
    origin_start:u64
    candidate_start:u64

OwnerFragmentV1: exactly 48 bytes
    candidate_start:u64
    len:u64
    actor_id[32]

ATTRIBUTE(origin_unit, candidate_unit, session_actor):
    verify complete origin C2 + ByteAttributionRoot
    verify complete candidate C2
    require checked C2 and attribution span sums agree
    require checked_add(c_old,c_new) <= N_C3_record_max

    for each origin C2 run in logical order:
        emit OccurrenceV1(complete identity, ORIGIN, run.start)
    for each candidate C2 run in logical order:
        emit OccurrenceV1(complete identity, CANDIDATE, run.start)

    occurrences = EXTERNAL_SORT(
        occurrences,
        key=(kind, len, chunk_id_or_zero, side, start))

    for each complete-identity group in the checked sorted stream:
        pair origin and candidate subranges by occurrence rank using two
            bounded sequential/pread cursors
        emit MatchV1 for every pair; ignore excess occurrences on either side

    matches = EXTERNAL_SORT(matches, key=origin_start)

    require checked_add(c_match, s_old) <= N_C3_record_max
    sequentially join matches, origin C2, and origin attribution:
        require each match names the next selected complete origin run
        for every positive owner-span intersection with that run:
            emit OwnerFragmentV1(
                candidate_start + intersection.start - origin_start,
                intersection.len,
                intersection.actor_id)
            check fragment counter <= N_C3_record_max

    fragments = EXTERNAL_SORT(fragments, key=candidate_start)

    require checked_add(c_frag, c_new-c_match)
        <= N_C3_record_max
    merge candidate C2 and fragments sequentially in candidate logical order:
        inherited fragments must exactly tile a matched complete run
        append session_actor for each unmatched complete run
        append to one bounded globally coalescing attribution builder

    require candidate C2 and fragment streams are exhausted exactly
    require positive, gap-free, non-overlapping, maximally coalesced output
    finish canonical bounded ByteAttributionRoot
    require output span sum equals candidate C2 span sum
    return ByteAttributionRoot
~~~

For a hardlink group, choose one origin ownership unit and run C3 exactly once:
among surviving aliases, use the lexicographically first origin whose
`ContentKey` equals the candidate; only if none is content-equal use the
lexicographically first surviving origin. Never blend multiple origin groups.
For the closed merge vector `a=X`, `b=Y`, candidate `Y`, alias `b` supplies
attribution even though `a` sorts first. Metadata ownership remains a separate
per-`EntryValue` calculation.

### Bounds

| Property | Bound |
|---|---|
| Complete-identity occurrence sort | `O(Sort(c_old+c_new))` over exact 50-B records |
| Origin-order match sort | `O(Sort(c_match))`, `c_match<=min(c_old,c_new)`, over exact 16-B records |
| Candidate-order fragment sort | `O(Sort(c_frag))` over exact 48-B records |
| Sequential joins and output | `Theta(c_old+c_new+c_match+s_old+c_frag+c_out)` |
| Single record cap | `c_old+c_new<=N_C3_record_max`; `c_frag<=c_match+s_old<=N_C3_record_max`; `c_out<=c_frag+(c_new-c_match)<=N_C3_record_max` |
| RAM | `<=2 MiB` heavy claim; 1-MiB run build or fan-in-8 windows plus bounded tile writer |
| Disk | `D_C3_max` below; exactly three reused scratch inodes |
| FDs | Proposed peak 7, pending the complete handle-by-handle inventory proof |
| History | None; only attribution reachable from retained complete states survives |

Changing only `ActorId` can create new attribution objects even when content
objects are reused. A one-byte edit may reattribute the complete affected DATA
run, and shifted FastCDC boundaries may reattribute neighboring unmatched
runs. That is the deliberately bounded whole-run contract, not history growth.

~~~text
n_occ = c_old + c_new
N_C3_record_max = 2,097,152
n_occ <= N_C3_record_max
c_match <= min(c_old, c_new)
c_frag <= c_match + s_old <= N_C3_record_max
c_out <= c_frag + (c_new-c_match) <= N_C3_record_max

D_C3_actual = 2 × max(G(50,n_occ), G(16,c_match), G(48,c_frag))
             + A_alloc(4096)
D_C3_max = 2 × max(G(50,N_C3_record_max),
                   G(16,N_C3_record_max),
                   G(48,N_C3_record_max)) + A_alloc(4096)
I_C3 = 3
q_run(50) = 20,971
q_run(16) = 65,536
q_run(48) = 21,845
~~~

The same two run containers and one 4-KiB checked control file are
retyped sequentially across all three sorts. The 50-byte record carries full
run identity, so there is no match hash or collision path. The 16-byte sort is
required for the sequential origin-C2/attribution join; the 48-byte sort is
required for the sequential candidate-order merge. Removing either sort
requires cardinality-scaled RAM, random identity-indexed rereads, or permits a
noncanonical result. These are three uses of the generic bounded sort
workflow, not extra project-owned mechanisms.
The one cap is the smallest power of two admitting the required million-run
origin plus million-run candidate adversary. It replaces three knobs because
the same run files are reused and the three streams need no independent
retention semantics. The full `D_C3_max` reservation is obtained before work;
the job may allocate only `D_C3_actual`.

## 9. S1 — fixed-purpose immutable CoW B+ Catalog

Authoritative definition:
[[implementation-plan/2.0 migration/system-design/components/durable_store#S1 — fixed-purpose immutable CoW B+ Catalog|S1]].

### Purpose

S1 stores a closed set of lifecycle rows and ObjectId locators with predictable
cache-disabled lookup, sparse copy-on-write updates, dense rebuild, and exact
basis-local record ranks for bounded GC.

### Pseudocode

~~~text
P = 16,384

DERIVED_CATALOG_ROOT(ArenaId, committed_arena_length):
    require committed_arena_length >= P
    require committed_arena_length mod P == 0
    return (ArenaId, committed_arena_length - P)

EMIT_PAGE_AT_CURSOR(arena, page, write_cursor):
    require write_cursor mod P == 0
    positional-write exactly P bytes of page to arena at write_cursor
    return checked_add(write_cursor, P)

SPARSE_PATH_COPY(selected_head, sorted_changes):
    require complete Catalog, FD, and disk permit
    require changes use the closed typed key/value schema
    require selected_head.committed_arena_length >= P and is P-aligned
    base_root = DERIVED_CATALOG_ROOT(
        selected_head.ArenaId, selected_head.committed_arena_length)

    # The selected length, not file size, is the only append authority.
    # Use positional writes beginning exactly there; never fstat or O_APPEND
    # to discover the candidate cursor. Unselected crash tail may be overwritten.
    write_cursor = selected_head.committed_arena_length

    walk base records and changes with one ordered bounded cursor
    reuse every untouched subtree by immutable page reference
    withhold at most one page candidate until it is known to be root or non-root

    for each touched leaf:
        verify key order, uniqueness, closed value type, and same-ID rules
        apply sorted changes
        for each balanced immutable replacement leaf known to be non-root:
            set leaf.subtree_record_count = exact unique record count
            write_cursor = EMIT_PAGE_AT_CURSOR(
                selected_head.ArenaId, leaf, write_cursor)
        require every non-root leaf is at least half full

    for each non-root parent level:
        stream changed child references upward
        set each count to CHECKED_SUM(child.subtree_record_count)
        for each balanced immutable replacement parent:
            write_cursor = EMIT_PAGE_AT_CURSOR(
                selected_head.ArenaId, parent, write_cursor)

    require height <= 8
    require arena and total <= 4C_max bounds
    build the fresh root from the final checked leaf-or-child stream
    write_cursor = EMIT_PAGE_AT_CURSOR(
        selected_head.ArenaId, one fresh immutable root, write_cursor)
    committed_arena_end = write_cursor
    require committed_arena_end >= P and is P-aligned
    require DERIVED_CATALOG_ROOT(
        selected_head.ArenaId, committed_arena_end) names that fresh root
    require no selected padding or trailer follows it
    return committed_arena_end

DENSE_BUILD_PREPARE(complete_sorted_records, basis, owner_slot):
    require basis is exactly
        {StoreSequence,ArenaId,committed_arena_length}
    create or truncate the owner-custodied Auxiliary to exactly zero bytes
    write_cursor = 0  # never discovered from file size or append mode
    withhold at most one page candidate until it is known to be root or non-root
    for each half-full-or-better leaf known to be non-root in complete order:
        write_cursor = EMIT_PAGE_AT_CURSOR(Auxiliary, leaf, write_cursor)
    for each streamed non-root parent page with checked subtree counts:
        write_cursor = EMIT_PAGE_AT_CURSOR(Auxiliary, parent, write_cursor)
    build the fresh root from the final checked leaf-or-child stream
    write_cursor = EMIT_PAGE_AT_CURSOR(
        Auxiliary, one fresh immutable root, write_cursor)
    committed_arena_end = write_cursor
    require committed_arena_end >= P and is P-aligned
    require DERIVED_CATALOG_ROOT(
        Auxiliary.ArenaId, committed_arena_end) names that fresh root
    require no selected padding or trailer follows it

    sync Auxiliary and every dependency
    return owner-custodied Auxiliary ArenaId, committed_arena_end, and basis

# S2 later acquires the dense-maintenance gate, performs its Theta(N_object)
# validation, and runs only the bounded final HEAD selector at the end.
~~~

### Dense rank

Each immutable internal child entry stores a checked u64
subtree_record_count. Preceding-sibling counts plus the leaf slot give a
global rank in one selected derived root. ObjectCatalog occupies one contiguous key
range, so subtracting its lower-bound rank gives a bijection to [0, No).

This field is not a refcount or live-set ledger. It is immutable S1
order-statistic metadata, recomputed on every sparse or dense build.

### Bounds

| Property | Bound |
|---|---|
| Point lookup | Theta(H), H <= 8 |
| Sparse update | `O(K_s1 H)` new pages worst case |
| Dense rebuild | Theta(N) ordered I/O |
| Page / arenas | 16 KiB / exactly two |
| One complete half-full-bounded arena | <= 2C_max |
| Selected plus Auxiliary physical space | <= 4C_max |
| RAM | Exactly one admitted subset of a global 128 x 16-KiB page-frame pool |
| Persistent cache | 0 B |

For reserve arithmetic, use an independent proved value
`D_aux_max <= A_alloc(2C_max)`. Using `A_alloc(C_max)` would underreserve an
Auxiliary arena at the admitted half-full worst case. `C_max` is a configured
capacity, not current live bytes; deletion cannot retroactively shrink the
bound while an old arena is still selected or reader-protected.

The proposed executable page schedule is:

| S1 operation | 16-KiB page frames | Complete S1 FD claim, excluding S2 control/directory handles |
|---|---:|---:|
| Point/rank lookup | 1 | 1 |
| Ordered cursor | 2 | 1 |
| Sparse path-copy | 3H + 2 = 26 | 2: selected arena + sorted change stream |
| Dense cascading builder | H + 2 = 10 | 2, or 3 with an independent sorted-input file |

~~~text
M_S1_page_pool = 128 × 16,384 = 2,097,152 B
~~~

No S1 operation may allocate a page-sized buffer outside those 128 frames.
Sparse path-copy performs a read-only packing preflight against the immutable
selected derived root and computes exact `p_new>=1`, including the mandatory
fresh final root page, before any positional write:

~~~text
D_S1_sparse =
    A_alloc(selected_committed_arena_length + 16,384 × p_new)
    - A_alloc(selected_committed_arena_length)
    + D_HEAD
~~~

Preflight must obtain the full permit, route to an already-reserved dense
build, or reject before mutation. Qualification must freeze page headers,
key/value/slot widths, subtree-count child widths, minimum leaf/internal
fanout, namespace row caps, and the exact HEAD/FD schedule, then prove height
`<= 8` and every frame-state transition. These remain format-freeze gates.

## 10. S2 — single-HEAD dependency-first commit and recovery

Authoritative definition:
[[implementation-plan/2.0 migration/system-design/components/durable_store#S2 — single-HEAD commit and recovery|S2]].

### Purpose

S2 is the sole custom crash protocol. It selects immutable packs, one Catalog
root, lifecycle effects, and an exact replay receipt through one mandatory
HEAD. There is no WAL, dual-selector election, fallback generation, or
database transaction engine.

`HEAD` serializes exactly the following closed record—there is no serialized
root offset or page identifier:

~~~text
HEAD = {
    type_tag,
    StoreSequence,
    ArenaId,
    committed_arena_length,
    checksum
}

VERIFY_MANDATORY_HEAD_AND_DERIVE_ROOT():
    head = read the one mandatory HEAD
    verify type_tag and checksum
    require head.committed_arena_length >= 16 KiB
    require head.committed_arena_length mod 16 KiB == 0
    root = DERIVED_CATALOG_ROOT(
        head.ArenaId, head.committed_arena_length)  # derived shorthand only
    return {head, verified selected arena, root}
~~~

Every selected S1 commit writes one fresh root as the last page, synchronizes
the committed arena prefix, and then selects only its new committed length.
The candidate write cursor starts at the selected committed length and is
never recovered from `fstat`, `O_APPEND`, padding, a trailer, or stale tail
bytes.

### Static custody, exact replay, and commit pseudocode

The Catalog still has exactly eight namespaces. `ReceiptControl` and
`ReceiptSlot` are closed key subtypes inside the existing `Receipt` namespace,
not a ninth namespace:

~~~text
OwnerSlot[0]     = Empty | Build{owner_nonce}                 # Maintenance only
OwnerSlot[1..15] = Empty | Build{owner_nonce} | AdapterClose  # foreground only

ReceiptControl(lane) -> next_sequence:u64                 # 16 rows, initially 0
ReceiptSlot(lane, sequence mod 64)
  -> {request_digest[32], bounded_exact_result}            # 1,024 rows

require complete canonical framed ReceiptSlot value <= 512 B
~~~

`Build` has no purpose field: its static lane supplies its meaning. Slot 0 and
its byte/inode reserve and quota are non-borrowable. Selecting its Build is the
sole global maintenance fence. Foreground lanes and their quotas are likewise
unavailable to maintenance.

~~~text
ACQUIRE_FOREGROUND_LANE(owner_value):
    require owner_value is Build{fresh_owner_nonce} or AdapterClose{...}
    under the serialized S2 admission gate:
        require OwnerSlot[0] is Empty, else return RetryLater
        select exactly one Empty OwnerSlot in [1,15], else return RetryLater
        # The 16th simultaneous foreground claimant is not admitted.
    return the selected static foreground lane

ACQUIRE_MAINTENANCE_LANE(fresh_owner_nonce):
    require the non-borrowable maintenance reserve/quota is intact
    under the serialized S2 admission gate:
        require OwnerSlot[0] is Empty, else return RetryLater
        select OwnerSlot[0] = Build{fresh_owner_nonce}
        # This selected row now fences every non-maintenance S2 mutation.
    return OwnerSlot[0]

REPLAY_DECISION(current_root, lane, sequence, request_digest):
    next = exact ReceiptControl(lane).next_sequence
    low = max(0, next - 64)

    if sequence < low:
        return ReplayExpired without executing
    if sequence < next:
        slot = one exact lookup of ReceiptSlot(lane, sequence mod 64)
        require slot.request_digest == request_digest, else typed transport reject
        return exact slot.bounded_exact_result without executing
    if sequence > next:
        return typed transport future-gap rejection without executing
    return NEW_SEQUENCE with exact slot key and expected next

PREPARE_PUBLISH_CUSTODY(owner_slot, candidate):
    require owner_slot is in [1,15]
    require exact Build{owner_nonce} is selected in that foreground lane
    require candidate has exactly one owner-staged sorted disk cursor
    require each cursor record is (ObjectId, REUSE | candidate locator)
    require every candidate locator names a verified record in this Build
    require all candidate frames are globally ObjectId-ordered and every
        SegmentId occupies one contiguous cursor interval
    seal, exact-EOF-verify and sync every candidate PackSegment, cursor and
        staging directory
    return a bounded cursor handle, never a locator or dependency vector

VALIDATE_CURRENT_CHOICE(current_root, object_id, choice, build):
    current_row = structural ObjectCatalog lookup by object_id, yielding
        ABSENT, INVALID, or VALID(row)
        # Trust the selected Catalog's structural/locator invariants.
        # Perform no pack/payload I/O in this final gate.

    require current_row is not INVALID

    if choice is REUSE:
        require current_row is VALID(row)
        selected = row
    else:
        require choice is a structurally valid staged locator owned by build
        selected = row if current_row is VALID(row) else choice
        # This preserves every existing encoding, especially Full over staged Delta.

    if selected is Delta:
        base_row = structural ObjectCatalog lookup of selected.base_id
        require base_row is structurally valid Full
    return selected

FOREGROUND_COMMIT(expected, accepted_request, typed_changes,
                  exact_result, optional_publish_candidate):
    acquire serialized foreground final gate
    require OwnerSlot[0] is Empty, else return RetryLater
    current = VERIFY_MANDATORY_HEAD_AND_DERIVE_ROOT()
    current_root = current.root

    replay = REPLAY_DECISION(current_root, accepted_request.lane,
        accepted_request.sequence, accepted_request.request_digest)
    if replay is retained, expired, digest-rejected, or future-gap:
        return replay

    require accepted_request.sequence == replay.expected_next
    replay-check only the bounded expected lifecycle/key facts
    publication_status = NONE
    if optional_publish_candidate exists:
        session = require exact Mutable/ACTIVE session
        build = require exact Build{owner_nonce} in one foreground lane
        current_sandbox = resolve Sandbox from the selected session key

        if (current_sandbox.StateId, current_sandbox.HeadRevision)
           != session.origin:
            # Conflict is decided before the cursor is opened.
            typed_changes = replace Mutable with Terminal {
                status=CONFLICTED, allocation=session.allocation
            }, dropping origin, actor_id and reservation
            exact_result = exact PublishConflict response
            select no candidate locator and retain exact Build{owner_nonce}
            publication_status = CONFLICTED
        else:
            # Pass V: complete structural revalidation; install nothing.
            for (object_id, choice) in the one sorted cursor exactly once:
                VALIDATE_CURRENT_CHOICE(current_root, object_id, choice, build)
            if the first REUSE row or required Full base is missing,
               structurally invalid, or incompatible:
                leave gate and return CANDIDATE_INVALIDATED

            # Pass S: same immutable root and cursor; O(1) state per segment.
            rewind cursor
            current_segment = NONE
            selected_count = 0
            for (object_id, choice) in the cursor exactly once:
                selected = VALIDATE_CURRENT_CHOICE(
                    current_root, object_id, choice, build)
                if choice is a staged locator:
                    if choice.segment_id != current_segment:
                        FINALIZE_PREVIOUS_CANDIDATE_SEGMENT(
                            current_segment, selected_count)
                        current_segment = choice.segment_id
                        selected_count = 0
                    if selected == choice:
                        selected_count = checked_increment(selected_count)
                typed_changes += choose selected for object_id
            FINALIZE_PREVIOUS_CANDIDATE_SEGMENT(
                current_segment, selected_count)

            # FINALIZE installs/syncs iff selected_count>0. For count 0 it
            # unlinks the staged late-dedup segment and syncs its directory.
            # An installed mixed segment leaves dead frames to exact maintenance.
            join cursor readers; delete/sync cursor and every non-pack scratch
                while exact Build{owner_nonce} remains selected
            typed_changes += head/revision update and replace Mutable with
                Terminal {status=PUBLISHED, allocation=session.allocation},
                dropping origin, actor_id and reservation
            exact_result = exact Published response
            typed_changes += exact Build-nonce clear
            publication_status = PUBLISHED

    require complete framed ReceiptSlot value for
        {accepted_request.request_digest, exact_result} <= 512 B
    typed_changes += replace ReceiptSlot(
        accepted_request.lane, accepted_request.sequence mod 64)
    typed_changes += set ReceiptControl(accepted_request.lane).next_sequence
        to checked(accepted_request.sequence + 1)

    new_committed_arena_length = SPARSE_PATH_COPY(
        current.head, sorted typed_changes containing the semantic effect
        or no-effect and receipt; no separate replay namespace exists)
    sync the exact selected Catalog arena prefix

    write complete checksummed HEAD.tmp containing exactly
        {type_tag, checked(current.head.StoreSequence+1), current.head.ArenaId,
         new committed_arena_length, checksum}
    sync HEAD.tmp
    same-filesystem rename HEAD.tmp to HEAD
    sync HEAD parent directory

    if publication_status != NONE:
        return selected publication status and exact ReceiptSlot result to the
            lifecycle owner without public acknowledgement
    acknowledge exact recorded result

FINALIZE_PREVIOUS_CANDIDATE_SEGMENT(segment, selected_count):
    if segment is NONE: return
    if selected_count == 0:
        unlink staged segment and sync its staging directory
        return
    derive SegmentId from the full exact staged file
    install and synchronize segment in packs/ before HEAD
    if an identical destination already existed:
        accept an existing destination only when full-file hash, fstat length,
            fixed header, every 34-B record header and exact EOF verify identically
        unlink duplicate staged source and sync its staging directory

INVALIDATE_AND_RECAPTURE_ONCE(owner_slot, build, active_session,
                              stable_private_workspace, accepted_request,
                              attempt):
    # Caller has left the final gate; Pass V installed no pack.
    require owner_slot is in [1,15] and holds exact build
    fence/join Build producers and close every cursor/FD
    while exact foreground Build{owner_nonce} remains selected:
        unlink the whole cursor, every staged pack and every scratch artifact
        sync the fixed Build staging directory
    require stable_private_workspace remains fenced
    if attempt == 0:
        return PREPARE_CANDIDATE(
            active_session, stable_private_workspace, owner_slot)
    ABORT_CANDIDATE_BUILD(build, installed_pack_may_exist=FALSE,
        accepted failure {request=accepted_request, result=RetryLater})
    return typed RetryLater

ABORT_CANDIDATE_BUILD(build, installed_pack_may_exist,
                      accepted_failure?):
    fence and join the producer; close every cursor/FD
    while exact foreground Build{owner_nonce} remains selected:
        if installed_pack_may_exist:
            run exact installed-pack census against the current selected Catalog
            unlink every zero-selected installed orphan and sync packs/
        delete every fixed-directory file and sync that directory
        exact-CAS-clear the nonce through S2, atomically storing the one
            ReceiptSlot and incremented ReceiptControl when accepted_failure exists
    release the live byte/inode charge and foreground permit

CLEAN_CONFLICT_AFTER_SELECTED_HEAD(build):
    # Terminal/CONFLICTED and its ReceiptSlot are selected; Build remains.
    ABORT_CANDIDATE_BUILD(build, installed_pack_may_exist=FALSE, NONE)
    acknowledge PublishConflict only after the final exact clear

VALIDATE_PREPARED_AUXILIARY(prepared_auxiliary):
    require OwnerSlot[0] holds exact Build{owner_nonce}
    stream and verify the complete basis/Auxiliary object relation
    classify every basis row exactly once as KEEP, DELETE, or REPLACE
    require every keep is identical
    require every deletion has trace/census proof for its exact old locator
    require every replacement names its exact old Full/Delta locator and one
        verified sealed new locator
    reject every extra or unclassified Auxiliary row
    require synchronized replacement packs and dependency summary
    require every non-ObjectCatalog row is byte-identical except deletion of
        exact OwnerSlot[0] Build{owner_nonce}; maintenance has no receipt
    return bounded summary binding basis, Auxiliary committed length, relation,
        owner_nonce and synchronized dependencies

MAINTENANCE_COMMIT(prepared_auxiliary, checked_summary):
    require OwnerSlot[0] still holds exact Build{owner_nonce}
    current = VERIFY_MANDATORY_HEAD_AND_DERIVE_ROOT()
    require exact (current.head.StoreSequence, current.head.ArenaId,
        current.head.committed_arena_length)
        == checked_summary.basis
    require checked_summary exactly binds checked_summary.basis, prepared Auxiliary
        committed length, row relation, and synchronized dependencies
    require prepared Auxiliary ends with its fresh root page and has no
        selected bytes after its committed_arena_length

    write/sync/rename/sync HEAD.tmp containing exactly
        {type_tag, checked(current.head.StoreSequence+1),
         prepared_auxiliary.ArenaId,
         prepared_auxiliary.committed_arena_length, checksum}; the selected
        Auxiliary omits exact OwnerSlot[0] Build{owner_nonce}, so selection
        and clear are atomic
    acknowledge the selected maintenance result
~~~

### Recovery pseudocode

~~~text
RECOVER():
    acquire exclusive Store ownership
    keep writable and readable readiness closed

    current = VERIFY_MANDATORY_HEAD_AND_DERIVE_ROOT()
    head = current.head
    verify the derived final page and selected Catalog framing
    verify selected pages, packs, Full bases, and closed namespace framing
    reconstruct selected session reservations, all selected Build charges, and
        all 16 static OwnerSlots
    fence stale adapters and every surviving Build producer
    clear expired volatile ReadSlots

    # Build rows and their reconstructed charges remain selected custody here.
    run the exact 72-byte pack census over the selected ObjectCatalog and every
        installed footerless exact-EOF PackSegment
    synchronously unlink every installed pack with zero selected rows
    if any pack was unlinked: sync packs/

    if selected data is missing, corrupt, or ambiguous:
        fail closed

    # Only the completed census proves which pre-HEAD installations are orphaned.
    for each selected Build row, in static lane order:
        fence/join any surviving producer and close every cursor/FD
        delete every file from its exact fixed directory and sync directory
    in one S2 commit, exact-CAS-clear the complete captured set of Build nonces
        and select one fresh root-last Catalog end
    only after that HEAD is durable, release every corresponding reconstructed
        byte/inode charge and permit
    require every unselected fixed staging directory is empty

    for each selected AdapterClose in OwnerSlot[1..15]:
        keep the session fenced and idempotently complete its exact close rule

    never elect Auxiliary or an older StoreSequence
    publish readiness
~~~

### Bounds

| Property | Bound |
|---|---|
| Candidate preparation | `Theta(P_new)` physical pack bytes plus one `Theta(K)` Build-owned disk cursor; packs, cursor and staging directory are synchronized before the final gate; at most the initial preparation plus one whole recapture |
| Origin-conflict gate | Bounded session/sandbox/receipt paths and fixed synchronization phases; origin is checked before opening the cursor, so there is no `K` scan |
| Origin-match gate | Per attempt `Theta(KH + K_delta + selected-candidate-pack install/sync work)`, with `K<=N_object_max`, `K_delta<=K`, `H<=8`; a complete validation pass precedes the selection/install pass, both are streaming, and one scalar count is retained per current segment; at most two attempts |
| Other sparse final gates | `O(K_s1 H)` Catalog build work plus bounded replay checks and fixed synchronization phases; `K_s1` is preflight-admitted |
| Static lane admission | Slot 0 accepts Maintenance only; slots 1..15 accept foreground Build/`AdapterClose` only. A busy applicable lane returns bounded `RetryLater`; the 16th simultaneous foreground claimant is not admitted. No class borrows another class's lane, reserve, or quota. |
| Dense maintenance write-side pause | `Theta(N_object+N_pack+X_live)` for trace, two sorts, rewrite, dense validation and selector while every other S2 mutation receives `RetryLater` |
| Dense final selector | `O(1)` in repository size after the fenced linear preparation |
| Recovery | Bounded HEAD/framing setup plus streamed exact pack census; every selected Build and charge remains in custody through orphan unlink and `packs/` directory synchronization, then staging cleanup, exact clear, and release |
| RAM | Bounded page, pack, HEAD, and one replay control/slot working set; all 1,024 retained ReceiptSlot rows remain cache-off on disk |
| Final-commit concurrency | Foreground final commits serialize across 15 foreground lanes; the admitted maximum origin-match pause is not `O(1)`. A selected Build in maintenance-only slot 0 globally fences all non-maintenance S2 mutations for its complete trace/sort/rewrite/dense workflow. |
| Crash visibility | Previous complete root or complete new root, never a mixture |
| Replay | One ReceiptControl lookup and at most one ReceiptSlot lookup; exact result within 16 lanes × 64 retained positions, with no resident receipt ring |

The minimal fenced maintenance design deliberately trades mutation
concurrency for fewer authorities: reads, materialization and private edits
continue, but publish/checkpoint/fork/rollback finalization receives bounded
`RetryLater`. Production must freeze and pass maximum pause and fairness at
`C_max` under 1/4/8/16/32/64 active sessions; failure blocks writable
production. The linearization and acknowledgement point is successful HEAD replacement
plus parent-directory synchronization. The protocol has a fixed number of
ordered synchronization phases, not necessarily a constant number of files or
system calls; those scale only within the admitted dependency caps. Production
qualification must freeze the HEAD codec, dependency-summary maximum,
`D_HEAD/I_HEAD`, final-gate buffers, and complete FD claim.

## 11. S3 — AlignedSpliceDelta-v1

Authoritative definition:
[[implementation-plan/2.0 migration/system-design/components/durable_store#S3 AlignedSpliceDelta-v1|S3]].

### Purpose

S3 reduces physical bytes for retained small edits to the same logical DATA
interval. It preserves a complete target ObjectId and has dependency depth
exactly one. It performs no global similarity search.

### Record

~~~text
DeltaRecord {
    # Locator kind chooses Full versus Delta; a Delta locator additionally
    # supplies only base_id. Neither locator stores codec or canonical_len.
    # The 34-B RecordHeader is the sole payload framing and supplies only
    # ObjectId and stored_len_minus_one.
    prefix_len,
    suffix_len,
    middle_bytes
}

target =
    base[0 : prefix_len]
    || middle_bytes
    || base[target_len - suffix_len : target_len]
~~~

### Pseudocode

~~~text
ENCODE_S3(origin_interval, target):
    acquire ReadSlot
    anchor = resolve origin interval through the captured Catalog root to its
             verified Full anchor, or resolve the origin Delta's base_id

    require target and base lengths are equal and <= 32 KiB
    prefix = longest common prefix
    suffix = longest non-overlapping common suffix
    candidate = FRAME_DELTA(prefix, suffix, target middle bytes)

    if candidate.framed_len <= floor(Full.framed_len / 4)
       and Full.framed_len - candidate.framed_len >= 1 KiB:
        stage candidate Delta under exact Build{owner_nonce} in OwnerSlot[1..15]
        release ReadSlot                       # no durable locator pin
        return staged candidate containing base_id only
    else:
        release ReadSlot
        return Full locator

DECODE_S3(delta, captured_catalog_root):
    base_locator = LOOKUP(delta.base_id, captured_catalog_root)
    require dependency depth exactly one
    require base_locator is Full
    verify base kind, length, and ObjectId
    require prefix_len + suffix_len <= target_len
    target = splice verified base and a borrowed slice of the target buffer
    verify target kind, exact length, canonical bytes, and BLAKE3 target_id
    return target
~~~

S3 has no separate selection algorithm. S2's complete current-root validation
pass chooses a structurally valid existing row when present; otherwise it
chooses the staged Delta only when `base_id` resolves structurally to current
Full. A failed base check invalidates the whole candidate and invokes the one
complete recapture rule. It never installs the Delta early or locally replaces
that one staged record with Full.

### Group normalization

~~~text
NORMALIZE_WITH_REWRITE_BATCH(captured_basis):
    while OwnerSlot[0] holds exact Build{owner_nonce} and fences S2 mutations:
        trace logical liveness and sort DeltaEdgeV1 by (base_id,target_rank)
        select dead-base singleton targets in key order while their verified
            Full frames fit the <=(64 MiB - 8 B) output-frame budget
        require at least one target entered physical-closure state 01
        choose only NORMALIZE; use no physical policy or victim set
        rescan captured ObjectCatalog in ObjectId order
        reconstruct exactly the state-01 Delta targets as verified Full records
        write at most one <=64-MiB ObjectId-ordered replacement pack, whose
            frames total <=64 MiB - 8 B
        rescan sealed replacement headers and merge derived locators
        require selected Delta count strictly decreases
        select dense Auxiliary committed length and clear exact owner_nonce atomically
    retire old packs only after old-epoch readers are canceled/joined and all
        cursors/FDs close; then unlink, dirsync and release charges
~~~

### Bounds and storage guarantee

| Property | Bound |
|---|---|
| Encode/decode | Theta(target length), target <= 32 KiB |
| Base candidate | O(1) from exact session-origin interval; final selection re-resolves one `base_id` in current S1 root |
| Reads | At most one Full base plus one Delta record |
| Proposed exact allocation-free slab | 32 KiB base + 32 KiB target + 16 KiB Delta window + 16 KiB hash/codec/control = 98,304 B |
| Dependency depth | Exactly one |
| Delta selection | Framed Delta <= 1/4 framed Full and saves >= 1 KiB |
| Selected per-object reduction | At least 4x versus that Full frame |
| Normalization progress | Selected Delta count strictly decreases; no physical-byte reduction is claimed, and old plus new allocation stays charged until exact later retirement |
| Pre-normalization singleton | Full anchor + selected Delta <= 1.25x Full in record-frame bytes; separately rounded packs may be larger |

~~~text
M_S3 = 98,304 B

FullFrame(x)  = 34 + x
DeltaFrame(d) = 34 + d       # d is the complete stored Delta payload
PackAlloc(frames) = A_alloc(8 + sum(exact frame bytes))
require frames is nonempty
require 8 + sum(exact frame bytes) <= 64 MiB
~~~

The middle is never copied into a third 32 KiB patch allocation: the encoder
borrows its slice from the target buffer and writes it through the 16 KiB
Delta window. The final codec must prove a selected framed Delta is `<=16 KiB`
and that all hash, header, offsets, buffered-I/O alignment, and error state fit the final
16 KiB control region. Encode, decode, and one-pack-at-a-time normalization
each claim exactly three FDs: Catalog, base/current input pack, and
candidate/replacement pack.

The 1.25x result is only a record-frame bound. Candidate append admission and
normalization use `PackAlloc`, including the exact 8-byte signature and
filesystem allocation rounding; they never infer physical bytes from frame ratios. A
`ReadSlot` protects only the captured base read/encode. The final gate is the
sole base-validity decision, so S3 needs no locator pin, pin cap, secondary
root wrapper, refcount, or background lease.

S3 can exceed 10x for a very small middle edit only when the measured framed
Delta is below 10% of Full. The design guarantees at least 4x for a selected
Delta, not a universal 10x.

## 12. Canonical codec and PackSegment workflows

These are required implementation workflows, not seventh and eighth custom
algorithms.

### Canonical encode and verify

~~~text
ENCODE_OBJECT(versioned_type_tag, typed_payload):
    validate closed kind and every format cap
    envelope = deterministic restricted-CBOR encoding of exactly
        [versioned_type_tag, typed_payload]
    require complete encoded envelope <= 65,536 B
    require direct typed canonical-object children <= 512
    object_id = BLAKE3_256(envelope)
    return object_id, envelope

VERIFY_OBJECT(expected_id, expected_kind, bytes):
    decode only definite-length fixed-order permitted values
    require exactly one supported versioned type tag and one exact payload
    require decoded type tag denotes expected_kind
    require CANONICAL_REENCODE(decoded) == bytes
    require BLAKE3_256(bytes) == expected_id
    return typed verified object
~~~

### Pack append and object read

~~~text
SegmentHeaderV1 = b"PMSSPK1\0"                            # exactly 8 B
RecordHeaderV1 = ObjectId[32] + stored_len_minus_one:u16  # exactly 34 B
PackSegmentV1 = SegmentHeaderV1
    + one or more (RecordHeaderV1 + payload)
    + exact EOF

Full = {segment_id, offset:u32, framed_len:u32}
Delta = {segment_id, offset:u32, framed_len:u32, base_id}

stored_len = checked_u16(stored_len_minus_one) + 1         # 1..65,536 B
frame_len = 34 + stored_len

APPEND_PACK_RECORD(owner_slot, object_id, canonical_bytes, optional_base_hint):
    verify object bytes and same-ID Catalog state
    choose a Full locator and canonical payload, or an eligible Delta locator
        and Delta payload whose locator alone additionally owns base_id
    require locator kind is the sole Full/Delta codec choice
    require neither locator stores codec or canonical_len
    require 1 <= stored payload length <= 65,536
    append the exact 34-B RecordHeaderV1 and payload with no padding
    require checked(8 + sum(frame_len)) <= 64 MiB
    when the complete-file limit is reached or the operation seals:
        require at least one frame and the final payload byte is exact EOF
        sequentially verify the exact 8-B SegmentHeaderV1 signature and every
            complete frame to EOF
        segment_id = BLAKE3_256(full exact file bytes)
        sync the complete footerless pack
    if Full:
        return unpublished Full {segment_id, offset:u32, framed_len:u32}
            owned by owner_slot
    return unpublished Delta {segment_id, offset:u32, framed_len:u32, base_id}
        owned by owner_slot

READ_OBJECT(object_id, read_slot):
    locator = S1_LOOKUP(read_slot.captured_root, ObjectCatalog, object_id)
    if locator is Full:
        read and verify exact canonical record
    else:
        read and verify Delta
        canonical = DECODE_S3(delta, read_slot.captured_root)
    verify object_id, kind, length, and canonical codec
    stream canonical bytes
~~~

`P_pack_committed_max=64 MiB` includes the exact 8-byte signature and all
frames, so output frames total at most `64 MiB - 8 B` and
`P_pack_alloc_max=A_alloc(64 MiB)<2^30`. `SegmentId` is a physical checksum
of the full exact file, never a canonical ID. A PackSegment has no footer,
trailer, padding, per-record codec/base field, or embedded record count; the
verified parse reaching exact EOF is its complete inventory. `RecordHeaderV1`
is the sole payload framing. The Catalog value's `Full`/`Delta` variant chooses
the decoder; a Delta target's canonical length comes only from its verified
Full base. No locator stores a `codec` or `canonical_len` field.

## 13. Materialization

Authoritative workflow:
[[implementation-plan/2.0 migration/system-design/components/workspace_engine#Materialize one complete state|materialization]].

~~~text
MATERIALIZE(origin_state_id, allocation_handle, admitted_claim):
    require claim covers buffers, worker, FDs, bytes, and inodes
    require private allocation is hidden and writer gate is closed
    create one hidden control directory descriptor-relatively inside the same
        filesystem allocation; keep it unreachable from the visible namespace

    logical_cursor = (origin_state_id, first canonical traversal key)
    while logical_cursor is not complete:
        acquire nonrenewable ReadSlot
        require origin_state_id is still a semantic root in this captured basis
        verify FilesystemRoot(origin_state_id)
        traverse filesystem/content objects from logical_cursor for one
            bounded physical batch; carry attribution ObjectIds opaquely

        for each materialization fact in this batch:
            if fact is not a HardlinkGroup member:
                adapter.APPLY_DESCRIPTOR_RELATIVE(allocation_handle, fact)
            else:
                group = verified HardlinkGroup named by fact
                anchor_name = lowercase_hex(group.ObjectId)
                    # Canonical State already verified the complete member set.
                open anchor_name below the hidden control-directory descriptor
                if absent:
                    create it with O_EXCL and no-follow containment
                    stream and verify the group's payload into that anchor once
                    apply the shared inode metadata
                    sync the completed anchor before publishing visible names
                require anchor is a regular file in this same private filesystem
                create this visible occurrence with descriptor-relative linkat
                verify its inode identity equals the anchor
            verify every fetched object

        advance logical_cursor only after the applied batch verifies
        before the 30-second deadline, end/cancel the batch
        join cancellation and close every captured-root cursor/FD
        release ReadSlot

        if origin_state_id is no longer rooted in the next basis:
            return SnapshotExpired or restart the public operation

    apply child contents before parent-directory metadata
    verify containment, exact fact profile, bytes, and inodes
    stream the hidden control directory with one bounded directory buffer:
        unlink every anchor name and sync the control directory
    remove and parent-directory-sync the empty hidden control directory
    require no anchor or control name remains and visible link topology verifies
    adapter.SYNC_ACTIVATION(allocation_handle)
    return verified private allocation handle
~~~

Portable materialization is Theta(B_realize + F) reads and writes and requires
adapter-specific Theta(B_realize + F) private-workspace bytes/inodes. Equal
non-hardlinked file occurrences count repeatedly in B_realize; a hardlink's
payload is realized once and its additional names count in F. A qualified
adapter must reserve one temporary link count per hardlink group so the hidden
anchor plus all canonical members fit its filesystem limit. The deterministic
ObjectId anchor name makes the private filesystem itself the bounded lookup
index: resident hardlink map, hardlink external sort, and hardlink scratch files
are all 0 B. On any failure the still-hidden allocation, including anchors, is
disposed through the existing allocation lifecycle. A qualified adapter may accelerate
physical realization, but correctness always has this streaming fallback.
No materializer decodes byte-attribution objects; `file_blame` does. No
materializer walks a version chain or requests squash. For Docker ordinary-file
allocation this portable path is the correctness fallback and cannot honestly
inherit the POC's mount-like activation ratios. An adapter-owned disposable
StateId projection or snapshotter/OverlayFS lower-reuse path is permitted only
after separate qualification proves complete private realization, no identity
authority, exact dependency/eviction accounting, current capability compliance
and portable fallback. Until then the 10x materialization target is unmet.

## 14. Portable two-pass publication

Authoritative workflow:
[[implementation-plan/2.0 migration/system-design/components/workspace_engine#Portable two-pass candidate preparation|candidate preparation]].

~~~text
PREPARE_CANDIDATE(active_session, stable_allocation, owner_slot):
    require durable Session/Mutable row is ACTIVE
    require active_session.actor_id is the immutable ActorId captured from the
        authenticated principal of the accepted create-session request
    require adapter holds an exact stability fence
    require owner_slot is one static foreground lane in [1,15]
    require exact Build{owner_nonce} is selected before file creation
    require its fixed staging directory is empty; live permit owns reservation

    PASS 1:
        stream complete stable facts
        read and hash at most B_scan source payload bytes
        build C1, C2, and C3 with bounded buffers and charged runs
        use only active_session.actor_id for changed metadata and every
            unmatched/changed C3 run
        emit a disk-backed sorted stream U_candidate of distinct object
            descriptors and one complete candidate StateId

    PASS 2:
        stream distinct descriptors in global ObjectId order; coalesce bounded
            source/Catalog locality only when it preserves that output order
        reread at most B_scan source payload bytes

        for every distinct same-ID object in U_reuse:
            reconstruct and exact-compare its selected typed canonical bytes
            exactly once; account the actual physical reads in P_reuse

        for every object in U_missing, exactly once:
            append Full or eligible depth-one S3 Delta
            account exact record and pack framing in P_new

    require candidate frames are globally ObjectId-ordered and each candidate
        SegmentId covers one contiguous ObjectId interval
    seal, exact-EOF-verify and sync candidate packs
    merge U_reuse and U_missing into the one Build-owned sorted disk cursor:
        emit (ObjectId, REUSE) for every U_reuse descriptor
        emit (ObjectId, candidate locator) for every U_missing descriptor
        synchronously delete the consumed input runs; retain no second list
    sync the cursor and staging directory
    require stability token is unchanged

    return candidate StateId, exact expected session/build facts, and a
        bounded handle to that one cursor

PUBLISH_WORKSPACE_SESSION(session_id, accepted_request):
    # accepted_request authenticates replay/admission; it never supplies C3 actor
    return exact retained receipt if present
    row = require session row
    if row is Terminal/PUBLISHED: return AlreadyPublished
    if row is Terminal/CONFLICTED: return PublishConflict
    session = require row is Mutable/ACTIVE
    owner = acquire transient session owner and one OwnerSlot[1..15]
    adapter.close writer gate, drain, and hold stability fence
    require OwnerSlot[0] is Empty when the foreground Build is selected
    require exact Build{owner.owner_nonce} remains in owner.slot

    candidate = PREPARE_CANDIDATE(
        session, session.allocation, owner.slot)
    result = FOREGROUND_COMMIT(
        exact session/origin/build facts,
        accepted_request,
        publication typed changes,
        exact publication result,
        candidate)

    if result == CANDIDATE_INVALIDATED:
        # Pass V installed nothing. Delete the whole first candidate, then
        # perform the sole permitted complete recapture under the same Build.
        candidate = INVALIDATE_AND_RECAPTURE_ONCE(
            owner.slot, exact Build{owner.owner_nonce}, session,
            session.allocation, accepted_request, attempt=0)
        result = FOREGROUND_COMMIT(
            exact session/origin/build facts,
            accepted_request,
            publication typed changes,
            exact publication result,
            candidate)

        if result == CANDIDATE_INVALIDATED:
            # This call performs complete cleanup, exact abort, and any
            # required accepted RetryLater receipt; there is no third attempt.
            return INVALIDATE_AND_RECAPTURE_ONCE(
                owner.slot, exact Build{owner.owner_nonce}, session,
                session.allocation, accepted_request, attempt=1)

    if result == PUBLISHED:
        transfer candidate charge to selected storage, release Build permit
        synchronously dispose and sync private allocation before acknowledgement
    else if result == CONFLICTED:
        # The conflict HEAD already selected the receipt but retained custody.
        ABORT_CANDIDATE_BUILD(exact Build{owner.owner_nonce},
            installed_pack_may_exist=FALSE, NONE)
        acknowledge PublishConflict only after that final clear
    else if a pre-HEAD failure occurred:
        ABORT_CANDIDATE_BUILD(exact Build{owner.owner_nonce},
            installed_pack_may_exist=(selection/install pass started),
            accepted failure {request=accepted_request, result=exact failure}
                if required, else NONE)
    return the exact publication response stored in ReceiptSlot
~~~

The adapter profile is qualified before support: every allocation that may be
retained after `PublishConflict` must already be self-contained and readable
without an origin-state edge. Unsupported adapters are rejected at profile
selection. Terminal therefore has no conditional content edge, per-conflict
proof branch or semantic-root role. Unrelated Store changes are folded into
the current Catalog root by bounded typed-row merge; strict origin still
compares the sandbox/session pair and never rebases workspace contents.

Let `K=|U_candidate|<=N_object_max`, `K_delta<=K`, and `H<=8`. Origin mismatch
is bounded session/sandbox/receipt work and never opens the cursor, so it has
no `K`-proportional scan. One origin-match attempt costs
`Theta(KH + K_delta + selected-candidate-pack install/sync work)`: complete
structural validation precedes the streaming selection/install pass, and both
retain only O(1) state for the current segment. The final gate performs no
payload I/O. There are at most two complete preparations and two finalization
attempts: initial plus one whole recapture. Admission freezes that combined
maximum before selection. A generic pre-HEAD failure keeps the session
`ACTIVE`, joins the producer, exact-censuses and unlinks any installed orphan,
deletes and directory-syncs every staged file while the exact Build nonce
remains selected, exact-clears that nonce with any required accepted failure
receipt, releases its charge/permit, and only then resumes safely or returns.

Portable byte bounds:

| I/O class | Bound |
|---|---:|
| Source payload reads | Per preparation `<=2B_scan`; bounded invalidation path with one whole recapture `<=4B_scan` total |
| Candidate sets | `U_candidate = U_reuse` disjoint-union `U_missing`; each distinct ObjectId is classified once through the disk-backed stream |
| Canonical comparison bytes | Per preparation exactly `C_reuse = sum(|canonical(o)|)` for `o in U_reuse`; at most the sum of two preparations after invalidation |
| Physical selected-Store comparison reads | Per preparation exactly measured `P_reuse`; a Delta locator includes the Delta frame and Full-anchor bytes its bounded reconstruction actually reads; at most two preparations |
| New canonical bytes | `Delta = C_candidate - C_reuse` |
| New physical writes | Per preparation `P_new`, including each exact 8-B signature and exact frame bytes; at most two preparations, with the first wholly deleted and directory-synchronized before recapture |
| Metadata, descriptor, C3, and sort bytes | Charged separately from encoded `S_fact`; fixed-record formulas apply after codec freeze |
| RAM | Fixed permits; no descriptor set proportional to repository size |

The path must not claim `C_reuse <= B_scan` or `P_reuse <= B_scan`. A tree of
empty files has `B_scan=0` but still has directory, metadata, attribution and
complete-root comparisons; reconstructing a depth-one Delta may also read its Full
anchor. A shared anchor read may be deducted only when the bounded operation
actually reuses that read—there is no persistent reconstruction cache.

~~~text
T_portable_publish =
    Theta(B_scan + S_fact + P_reuse + P_new)
    + T_candidate_sorts
    + T_C2
    + T_C3
    + T_sparse_catalog

T_publish_with_one_invalidation <=
    T_portable_publish(initial) + T_portable_publish(recapture)
    + bounded exact cleanup and finalization work for both attempts
~~~

A capability-qualified complete journal may replace discovery with
dirty-byte/fact closure. Any coverage gap, overflow, rename/link ambiguity, or
recovery uncertainty falls back to the portable full scan. The journal is an
adapter accelerator, not canonical state.

## 15. Checkpoint, fork, rollback, and fork commit

These are lifecycle transitions composed from S1 and S2. They are not custom
storage algorithms.

~~~text
CREATE_CHECKPOINT(sandbox_id, checkpoint_id, accepted_request):
    capture exact selected Sandbox row
    insert immutable (sandbox_id, checkpoint_id) -> StateId
    select exact receipt in the same S2 commit
    return checkpoint_id

ROLLBACK(sandbox_id, checkpoint_id, accepted_request):
    under sandbox gate, require Mutable prefix is empty
    current = exact Sandbox row
    target = exact owned Checkpoint row

    if current.StateId == target.StateId:
        S2 commit receipt-only AlreadyCurrent
    else:
        set current.StateId = target.StateId
        increment current.HeadRevision
        S2 commit RolledBack plus exact receipt

FORK(source_id, optional_checkpoint_id, child_id, accepted_request):
    under source gate, require Mutable prefix is empty

    if checkpoint_id supplied:
        cp = require source-owned checkpoint
    else:
        cp = atomically create checkpoint of source current StateId

    insert child Sandbox {
        StateId = cp.StateId,
        HeadRevision = 0,
        ForkOrigin = (source_id, cp.id)
    }
    insert derived CheckpointPin(cp.id, child_id)
    S2 commit all rows plus exact receipt
    return child_id, cp.id

COMMIT_FORK(child_id, child_checkpoint_id, accepted_request):
    hold child and parent gates in ascending sandbox-ID order
    require both Mutable prefixes are empty

    P = immediate parent current StateId
    C = explicit child-owned checkpoint StateId
    B = child immutable origin checkpoint StateId

    if P == C:
        result = AlreadyCurrent
    else if C == B:
        result = NoChanges
    else if P == B:
        parent.StateId = C
        increment parent.HeadRevision
        result = Committed
    else:
        result = ParentDiverged

    S2 commit parent change if any plus exact receipt
    return result
~~~

The authoritative behavior is the linked Lifecycle state table. The sequence
`P == C`, then `C == B`, then `P == B` below is the proposed verification order,
not a second normative owner.

## 16. Exact semantic retention and garbage collection

### 16.1 Semantic roots

The exact content-root set is:

~~~text
Rsem =
    every live Sandbox StateId
    union every Checkpoint StateId
    union every Session/Mutable origin StateId
~~~

Receipts, status-derived Terminal outcomes, allocation handles, provenance,
CheckpointPin, `Session/Terminal`, and HeadRevision are not content roots.
Physical custody is the selected Catalog plus exact `Build` staging custody
and old epochs protected by active ReadSlots; none is semantic history.

Deleting a root gives **zero speculative capacity credit**. Credit occurs only
after exact trace, any replacement, joined cancellation/drain of old-epoch
readers and their cursors/FDs, unlink, and parent-directory synchronization.

### 16.2 Dense-rank two-bit trace

Authoritative formulas:
[[implementation-plan/2.0 migration/system-design/components/durable_store#Exact GC and repack|exact GC and repack]].

~~~text
Ps = 4096
d  = 32
Pt = Ps - d = 4064

q0(n) = ceil(n / (4 × Pt))
q(j+1,n) = ceil(q(j,n) / (8 × Pt)) while q(j,n) > 1
Q(n) = sum of all q(j,n)
L_trace(n) = number of q levels, including q0

if n == 0:
    Q(n) = 0
    L_trace(n) = 0

D_trace(n) = A_alloc(Ps × (1 + Q(n)))
D_trace_max = D_trace(N_object_max)
I_trace_max = 1
~~~

The canonical header binds the trace format, exact `MaintenanceBasis`,
`N_object`, every level geometry/offset, allocated length and current phase.
Every state or summary block digest binds the format, exact basis,
`N_object`, phase, level/type, `block_index`, `valid_tail_len` and the complete
4,064-byte payload. A phase transition rewrites the header and **every** block
digest before any new state meaning is consumed; swapping a block, replaying
another basis or reading logical-phase bits as physical closure therefore
fails closed.

Level zero stores two bits per admitted ObjectCatalog rank:

| Bits | State |
|---|---|
| 00 | unseen |
| 01 | pending |
| 10 | done and logically live |
| 11 | invalid; valid ranks may never contain this at completion |

Higher levels store one summary bit per child block/subtree. A summary bit is
one exactly when its subtree contains a valid pending rank.

~~~text
TRACE_LOGICAL_LIVE(basis):
    require basis is exactly
        MaintenanceBasis{StoreSequence,ArenaId,committed_arena_length}
    root = DERIVED_CATALOG_ROOT(
        basis.ArenaId, basis.committed_arena_length)
    roots = STORE_SCAN_FIXED_SEMANTIC_ROOT_FIELDS(root)
    range = S1_EXACT_OBJECTCATALOG_RANGE_AND_COUNT(root)

    reserve D_trace_max before starting maintenance
    trace = CREATE_FULLY_ALLOCATED_CHECKED_TRACE_FILE(
        owner_slot,
        D_trace(range.N_object),
        valid state = 00,
        unused state tail = 11,
        summary and summary tails = 0)

    ENQUEUE(object_id, expected_kind):
        rank, locator = S1_EXACT_RANK_LOOKUP(
            root,
            object_id,
            expected_kind)
        state = trace.READ_STATE(rank)
        if state == 00:
            trace.WRITE_STATE(rank, 01)
            trace.RECOMPUTE_ANCESTOR_SUMMARIES(rank)
        else if state == 01 or state == 10:
            do nothing
        else:
            fail and discard trace

    for root in roots:
        ENQUEUE(root.id, root.expected_kind)

    while trace.ROOT_SUMMARY_HAS_PENDING:
        rank = trace.FOLLOW_SUMMARIES_TO_ONE_PENDING_RANK()
        require trace state(rank) == 01

        trace.WRITE_STATE(rank, 10)
        trace.RECOMPUTE_ANCESTOR_SUMMARIES(rank)

        id, locator = S1_SELECT_EXACT_OBJECTCATALOG_RANK(basis, rank)
        object = READ_VERIFY_CANONICAL_OBJECT(id, locator)
        for typed_child in CLOSED_TYPED_CHILDREN(object):
            increment checked edge counter
            require edge counter <= E_reach_max
            ENQUEUE(typed_child.id, typed_child.expected_kind)

    require every valid state is 00 or 10
    require no valid state is 01 or 11
    require unused state tail remains exactly 11
    require every summary and summary tail recomputes exactly to zero
    sync completed trace state needed by the next phase
    return trace
~~~

Setting 01 before expansion and allowing each rank to enter 01 only once makes
sharing, duplicate references, and corrupt cycles finite. A failure after a
rank becomes 10 is safe because the entire non-resumable trace is discarded.

The reserve remains the admitted maximum, but the trace file is physically
allocated only for the exact captured `N_object`. Initialization and final
full-file validation therefore scale with the captured Catalog, not the
deployment maximum. A deterministic bound is:

~~~text
Theta(D_trace(N_object)
      + R_scan
      + (N_roots + E_reach + N_reach) × H
      + N_reach × L_trace(N_object)
      + B_reach
      + N_object)
~~~

`R_scan` is the fixed-schema lifecycle-row scan, the `H` term includes root,
edge, and exact-rank Catalog work, `N_reach × L_trace` covers worst-case
state/summary updates, and `N_object` is the final ordered ObjectCatalog
sweep. RAM is one bounded set of state/summary windows, an `H <= 8` Catalog
path, a streaming decoder, and a bounded child batch within one `<= 2 MiB`
heavy claim. There is no mmap, heap queue, hash set, refcount table, or
object-count-sized resident structure.

### 16.3 Physical dependency closure

Logical reachability and physical retirement are separate. The completed trace
marks canonical objects reachable from the three semantic-root fields. A
one-way checked phase transition then marks a Full object needed only as the
depth-one base of a logically live Delta. `ReadSlot` protects a captured
Store epoch until cancellation is joined and all cursors/FDs close; it emits no
per-object liveness row. Staged Build files remain outside `packs/` and the
victim set until S2 installs and selects them.

For fixed record width `r`, maximum record count `n`, a 1-MiB initial-run
budget and checked allocation rounding `A_alloc`:

~~~text
q_run(r) = floor(1 MiB / r)
require q_run(r) >= 1
m(r,n) = ceil(n / q_run(r))
G(r,n) = A_alloc(r*n + 64*m(r,n))

DeltaEdgeV1 = {                                         # exactly 36 B
    base_id[32],
    target_rank:u32
}
PackCensusV1 = {                                         # exactly 72 B
    segment_id[32],
    offset_or_committed:u32,
    marked_len:u32,
    object_id[32]
}

KIND  = bits 31..30 of marked_len
VALUE = low 30 bits of marked_len

KIND_DEAD_CATALOG    = 00
KIND_LOGICAL_CATALOG = 01
KIND_ANCHOR_CATALOG  = 10
KIND_INVENTORY       = 11

P_pack_committed_max = 64 MiB < 2^30       # signature plus all frames
P_pack_alloc_max = A_alloc(64 MiB) < 2^30

N_pack_record = N_object + N_pack
N_pack_record_max = N_object_max + N_pack_max
require N_object < 2^32
require N_object_max < 2^32
require N_delta < 2^32
require N_delta_max < 2^32
D_closure_scratch_max =
    2*max(G(36,N_delta_max), G(72,N_pack_record_max))
    + A_alloc(4096)
I_closure_scratch = 3

q_run(36) = 29,127
q_run(72) = 14,563
passes_edge = ceil(log8(max(1,m(36,N_delta_max))))
passes_pack = ceil(log8(max(1,m(72,N_pack_record_max))))
~~~

The two sorts reuse exactly two run containers and one 4-KiB checked
control file. `PackCensusV1.object_id` is required: while merging in
physical order it verifies the selected Catalog key against the record header
without a random Catalog reread. The high two bits of `marked_len` are the
entire closed kind enum; its low 30 bits are the exact framed length or pack
allocation. `DEAD_CATALOG`, `LOGICAL_CATALOG`, and `ANCHOR_CATALOG` carry the
exact ObjectId; `INVENTORY` requires an all-zero ObjectId. The writer maps
physical states `00`, `01|10`, and `11` respectively to those three Catalog
kinds. Sort and merge decode `KIND` and mask `VALUE` before comparison or
arithmetic. With `segment=segment_id`, `offset=offset_or_committed`,
`value=VALUE`, `kind=KIND`, and `object=object_id`, the exact comparator is
`(segment, offset, value, kind, object)`.

The frozen writer, recovery path, and deployment profile reject unless
`P_pack_committed_max` and `P_pack_alloc_max` satisfy the strict `<2^30`
bounds. Every actual frame offset, pack committed length, framed length,
allocation and intermediate sum is computed with checked u64/u128 arithmetic;
only a proved `<2^30` value narrows to u32. This removes eight bytes per census
record without truncation or wraparound. Codec/source/reserved fields would
have no consumer. A second pack digest is redundant because `SegmentId`
authenticates the complete footerless exact-EOF file.

After logical success, the same two-bit rank state has this exact
`PhysicalClosure` meaning:

| Bits | Physical-closure state |
|---|---|
| `00` | Dead; omit from the new Catalog unless replaced by no operation, which is forbidden. |
| `01` | Logically live Delta target selected for deterministic normalization to Full. |
| `10` | Logically live row kept in its selected encoding unless the chosen physical policy relocates it. |
| `11` | Full anchor retained only for a live Delta; not logically live. |

~~~text
BUILD_PHYSICAL_CLOSURE(basis, completed_logical_trace, requested_policy):
    root = DERIVED_CATALOG_ROOT(
        basis.ArenaId, basis.committed_arena_length)
    sweep every selected ObjectCatalog row once in ObjectId/rank order:
        require current target_rank < 2^32
        for each logically-live selected Delta:
            emit DeltaEdgeV1(delta.base_id, checked_u32(target_rank))
    edges = EXTERNAL_SORT by (base_id, target_rank)
    reject duplicate target ranks, malformed groups and checked-count overflow

    planned_full_frames = 0
    for each base_id group in edges:
        base_rank, base_locator = exact key/rank lookup in root
        require base_locator is exact verified Full
        require trace[base_rank] is 00 or 10
        base_frame = read and verify the exact Full frame named by base_locator
        require base_frame.RecordHeaderV1.ObjectId == base_id
        base_target_len = checked(base_frame.stored_len_minus_one + 1)
        require base_locator.framed_len == checked(34 + base_target_len)

        sole_target_rank = NONE
        sole_target_full_frame = NONE
        target_count = 0
        for each target_rank in this group:
            target_object_id, target_locator = exact Catalog rank select in root
            require trace[target_rank] == 10
            require target_locator is the exact Delta naming base_id
            verify the frame header names target_object_id, bounded framing,
                valid splice fields, reconstruction to exactly base_target_len,
                canonical bytes and the target ObjectId
            count target; reject duplicates or overflow
            sole_target_rank = target_rank
            sole_target_full_frame = checked(34 + base_target_len)

        if requested_policy == NORMALIZE
           and trace[base_rank] == 00
           and target_count == 1
           and checked(planned_full_frames + sole_target_full_frame)
               <= 64 MiB - 8 B:
            trace[sole_target_rank] = 01
            planned_full_frames += sole_target_full_frame
            # The dead base remains 00; this removes the inefficient singleton.
        else if trace[base_rank] == 00:
            trace[base_rank] = 11
            # k>=2 always retains one Full anchor; a nonselected singleton does too.

    rewrite the header and EVERY block digest for PhysicalClosure
    sync, reopen, and verify exact basis, geometry, phase, states, zero
        summaries and all phase-bound digests before consuming the states

    for EVERY selected ObjectCatalog row, including dead state 00:
        emit PackCensusV1 with exact selected locator and ObjectId
        set KIND=DEAD_CATALOG for state 00, LOGICAL_CATALOG for state 01 or 10,
            or ANCHOR_CATALOG for state 11; store framed_len in VALUE
        checked-narrow offset and VALUE only after both are < 2^30

    stream the complete installed sealed-pack directory:
        verify containment, SegmentId filename, committed length, allocation,
            exact 8-B SegmentHeaderV1 signature, one-or-more exact frames,
            exact EOF,
            the frozen per-pack maxima and N_pack_max
        emit KIND=INVENTORY, committed length in offset_or_committed,
            allocation in VALUE and object_id = zero after checked narrowing

    census = EXTERNAL_SORT by decoded
        (segment, offset, value, kind, object)

    merge census sequentially by segment/frame:
        decode KIND and mask VALUE before comparison and arithmetic
        require every offset/value is the exact admitted field and < 2^30
        require Catalog kinds match the exact physical trace state and ObjectId
        require INVENTORY has object_id = zero and exact committed/allocation
        verify every selected ObjectId against its exact frame header
        reject missing inventory, conflicting duplicates, bad lengths,
            overlaps, unknown installed candidates or SegmentId mismatch
        count each unique selected frame once
        emit exact retained framed bytes and allocation per pack
        retain only the bounded victim candidates required by requested_policy
    return completed PhysicalClosure trace, exact pack totals, victim candidates
~~~

Dead rows are mandatory: omitting them can hide a wholly dead selected pack.
Installed inventory makes rowless physical artifacts visible without inventing
a `PackCatalog`. OwnerSlot staging is a separate fixed-directory custody
domain and contributes no census variant. An inventory-only pack is deleted
only after every old-epoch reader drains, then unlink and directory sync
complete. The dense keep-set is exactly every row whose physical trace state
is `01`, `10`, or `11`; `01` is a replacement with a verified Full locator,
while `10` and `11` are identical keeps unless the single physical policy
relocates them. Equivalently:

~~~text
CatalogKeep = rows_with_state(01 | 10 | 11)
~~~

Every captured ObjectCatalog row is classified exactly once as identical
`KEEP`, exact-locator `DELETE`, or exact-old-to-verified-new `REPLACE`.
All non-ObjectCatalog namespaces remain byte-identical except atomic deletion
of the exact selected Maintenance Build nonce.

### 16.4 One rewrite engine and retirement

There is one physical mutation algorithm, `REWRITE_BATCH`. Its four policies
select work; they are not four algorithms. One invocation carries exactly one
policy in the checked vector header/control; policy mixing is forbidden. The
payload keeps at most 64 source SegmentIds in one fixed 4-KiB phase-reused
vector:

~~~text
VictimV1 = {
    segment_id[32],
    allocated:u32,
    retained:u32
}                                                        # exactly 40 B
B_victim = 64
64*40 = 2,560 B; checked vector header/control keeps total <=4,096 B
~~~

Each per-victim `allocated` and framed-byte `retained` value is proved
`<2^30` under the frozen per-pack limits before checked narrowing. Cross-victim
`V_alloc`, `X_alloc`, retained-byte and policy totals remain checked u64 (or
u128 intermediates); no batch total narrows to u32.

~~~text
REWRITE_BATCH(requested_policy):
    require requested_policy is exactly one of
        DEAD_REPACK | EMERGENCY_REPACK | CONSOLIDATE | NORMALIZE
    store requested_policy once in the checked vector header/control
    owner_slot = ACQUIRE_MAINTENANCE_LANE(fresh_owner_nonce)
    require owner_slot == OwnerSlot[0]
    require exact Build{owner_nonce} is selected
        # global fence: every non-maintenance S2 mutation returns RetryLater
    selected = VERIFY_MANDATORY_HEAD_AND_DERIVE_ROOT()
    basis = exact MaintenanceBasis from only
        {selected.head.StoreSequence, selected.head.ArenaId,
         selected.head.committed_arena_length}

    trace = TRACE_LOGICAL_LIVE(basis)
    closure = BUILD_PHYSICAL_CLOSURE(basis, trace, requested_policy)
    if requested_policy == NORMALIZE:
        require at least one state-01 target and victim count == 0
    else:
        require no state-01 target
        choose <=64 eligible victims for requested_policy; ties use
            SegmentId order
        require at least one victim
    require admitted output frames <=64 MiB - 8 B

    rescan captured ObjectCatalog in ObjectId order:
        omit dead rows
        if requested_policy == NORMALIZE:
            reconstruct and verify exactly every state-01 Delta as Full
            append one ObjectId-ordered replacement record for each
        else:
            copy and verify exactly every state-10/state-11 row in a victim
            append one ObjectId-ordered replacement record for each
    seal, verify and sync at most one replacement PackSegment

    rescan replacement headers sequentially in ObjectId order
    derive {ObjectId,new_offset,framed_len} and merge with basis rows
        # no relocation record, stream, cap, or third external sort

    prepared = DENSE_BUILD_PREPARE(
        complete KEEP/DELETE/REPLACE merge plus every byte-identical
        non-ObjectCatalog row except exact nonce deletion, basis, owner_slot)
    checked_summary = VALIDATE_PREPARED_AUXILIARY(prepared)
    MAINTENANCE_COMMIT(prepared, checked_summary)

    after HEAD is durable:
        cancel expired old-epoch readers and join/drain them
        close every old cursor/FD
        unlink retired packs/arena and sync each parent directory
        only then release byte/inode charges and reopen S2 mutation admission
~~~

The write-side fence spans trace, both sorts, ObjectId-order rewrite, dense
build/validation and selector: `Theta(N_object+N_pack+X_live)`. Reads,
materialization and already-admitted private edits continue, but
publish/checkpoint/fork/rollback finalization returns bounded `RetryLater`.
There is no optimistic basis retry, change log, refcount, catch-up stream or
short-fence claim. Production must freeze and pass a maximum maintenance pause
and fairness threshold at `C_max` under 1/4/8/16/32/64 active sessions; a
failure blocks writable production.

Let `V_alloc` be actual allocation-rounded bytes of source packs fully
retired by this commit, `X_live<=64 MiB-8 B` verified output frame bytes, and
`X_alloc` the actual allocation-rounded sealed output:

| Policy | Eligibility and exact progress |
|---|---|
| `DEAD_REPACK` | Up to 64 partly/fully dead packs; require `2*X_alloc<=V_alloc`, hence `X_alloc/(V_alloc-X_alloc)<=1`. |
| `EMERGENCY_REPACK` | Only before retention failure when normal ratio is impossible; require `X_alloc<V_alloc`. |
| `CONSOLIDATE` | Up to 64 underfilled all-live packs; require `X_alloc<=V_alloc` and fewer selected pack inodes. |
| `NORMALIZE` | With zero victims, replace at least one selected dead-base singleton Delta with Full and strictly reduce Delta count. It claims no physical decrease; admission covers complete temporary growth. |

One invocation executes exactly one row of this table. It never normalizes and
repacks together; a later invocation captures a fresh basis for another
policy.

Only fully retired packs contribute to `V_alloc`. Physical batches converge
in at most `ceil(eligible_source_packs/64)`; normalization terminates by
strictly decreasing a finite selected-Delta count. One later batch always
captures a fresh basis. When no policy proves its stated progress, the selected
bytes are the irreducible live floor. No maintenance step deletes a semantic
root or borrows future reclaim credit.

Deleting a semantic root gives zero immediate quota credit. Old selected,
staged, orphan, replacement, scratch and retired bytes remain fully charged
until exact trace/census, selection or abort, joined readers, unlink and
directory synchronization complete. Reclaimable physical debt has per-store
soft/hard watermarks `128/256 MiB` and `32/64` inodes; those counters cover
only deterministically classified residue, not guessed garbage.

## 17. Repeated-edit and no-squash bad cases

### 17.1 Repeated edits to the same line

If an agent repeatedly changes the same line:

1. FastCDC may keep most payload chunks stable, but only the full-scan bound is
   guaranteed.
2. C2 may change only a short root-to-leaf region after resynchronization; its
   adversarial bound remains a full metadata rebuild.
3. S3 may encode an eligible changed `<=32 KiB` object as one depth-one Delta
   from a selected Full base. It never uses a Delta as another Delta's base,
   so a later edit may require a Full record instead of extending a chain.
4. A newly published head stops retaining the prior state unless a checkpoint
   or mutable-session origin still names it. Terminal sessions are not roots.
5. Exact GC deletes unrooted objects. In a `NORMALIZE` invocation it also
   rewrites a dead-base singleton Delta as Full; groups with `k>=2` live Delta
   targets keep one Full anchor because that is the smaller depth-one shape.

With no retained old roots, publication count is not a retention dimension.
Storage is the latest reachable state plus fully charged staged, unreachable,
and old-reader bytes until exact maintenance retires them. Debt watermarks,
the simultaneous reserve and write admission bound that temporary growth; a
successful publication does not claim speculative reclaim credit.

With a checkpoint after every edit, growth is intentional. Each checkpoint is
a semantic promise to preserve a distinct complete state. PMSS may deduplicate
unchanged objects and compact physical records, but it cannot delete the
unique changed bytes, changed C2/C1 path nodes, `FilesystemRoot`, or
attribution facts without breaking rollback.

A useful upper-shape model for v retained edits to one file is:

~~~text
retained unique bytes =
    original shared state
    + sum over v of:
        unique changed chunk or S3 middle bytes
        + changed C2 path objects
        + changed C1 ancestor objects
        + changed attribution objects
        + one small state/root envelope
~~~

This is not v full copies. It is also not constant if policy explicitly retains
v different truths.

### 17.2 Adversarial situations and controls

| Bad case | What could grow or slow | Elegant control without squash |
|---|---|---|
| Checkpoint every tiny edit | Unavoidable retained unique versions and roots | Hard root quota; explicit remove_checkpoint; optional external bounded TTL/last-N policy only for roots it owns |
| Many long-lived mutable sessions from old heads | Their explicit origins retain old complete states | Session/root quotas, explicit synchronous destroy, and an optional external policy only for sessions it created; never hide retention in GC |
| Same bytes, changing actor | New attribution objects | Content still deduplicates; retain attribution only through explicit roots |
| A/B/A/B content toggling | Repeated lifecycle revisions | Canonical A and B objects deduplicate; HeadRevision changes but is not content history |
| C2 adversarial boundary grounding | Theta(n) metadata rebuild | Admit worst-case buffers/runs; measure golden adversarial corpus; never claim expected locality as a bound |
| High-entropy or boundary-shifting tiny edits | Little content reuse and repeated Full records | Charge actual `P_new`; preserve the full-scan/Full-write bound; let exact GC reclaim unrooted predecessors |
| Large rename or directory churn | Many C1 ancestor objects and facts | Path-byte-bounded C1, external sort, exact fact quotas |
| Tiny objects and tiny packs | Header and inode fragmentation | Bounded candidate packing plus up-to-64-source all-live consolidation when it strictly reduces allocation/inodes |
| One live Delta retains one dead Full base | A singleton can exceed the corresponding Full-only frame shape | A `NORMALIZE` invocation selects the singleton, emits Full, then a later exact physical pass can retire old packs after readers drain |
| Many live Deltas share one dead Full base | One physical-only anchor remains | Keep the single anchor for `k>=2`; this is bounded depth-one sharing, not history or a chain |
| Delta chains | Unbounded reads and dependency retention | Forbidden; S3 depth exactly one and always points to Full |
| Many conflicted sessions | Self-contained private workspace allocations | Terminal-session/workspace quotas and explicit synchronous destroy; Terminal retains no canonical origin and is not a semantic root |
| Slow or abandoned readers | Delayed pack retirement | Exactly 64 ReadSlots, absolute nonrenewable 30-second lifetime, restart fence |
| Many in-flight candidates | Staging explosion or maintenance starvation | Static slot 0 and its quota/reserve are maintenance-only and non-borrowable; slots 1..15 are foreground-only; a 16th simultaneous foreground claim returns `RetryLater`, and a selected slot-0 Build fences every foreground final mutation |
| Edits arrive faster than maintenance | Fully charged unreachable and retired bytes approach debt limits | Watermarks trigger one fenced bounded policy per fresh basis; admission stops before reserve or hard quota is consumed |
| GC near full disk | No room to relocate | Non-borrowable simultaneous maintenance reserve; no speculative deletion credit |
| Mostly live packs | Ordinary <= 1/2-live policy finds nothing | One emergency high-live step when rounded space strictly decreases |
| All-live underfilled packs | Inode/signature growth | One `CONSOLIDATE` invocation selects up to 64 sources, emits one complete pack `<=64 MiB` whose frames total `<=64 MiB-8 B`, and must reduce pack inodes without increasing allocation |
| Root deletion races publication | Mixed root and locator basis | Store scans roots and locators from one MaintenanceBasis; final S2 exact-basis CAS |
| Crash during trace | A set bit might hide unprocessed work | Trace is non-resumable; delete and synchronize the whole scratch file |
| Multiple concurrent sessions | Memory or last-writer-wins growth | Immutable origin pairs, strict conflict, global all-or-none permits, idle sessions hold zero buffers/FDs |

### 17.3 Semantic retention policy

PMSS itself never silently expires a manual checkpoint. An optional external
policy may implement TTL or last-N only when it:

- tracks a finite set of checkpoint/session IDs it created;
- calls existing remove/destroy APIs;
- skips CheckpointInUse;
- never removes a manual checkpoint;
- behaves safely if its own bounded registry is lost.

This keeps retention policy out of the storage format and avoids a hidden
history database.

~~~text
RETENTION_SWEEP(policy_owned_ids, now, root_budget):
    read at most one bounded page of IDs from the policy's finite registry
    order eligible IDs by (expired first, oldest policy timestamp, opaque ID)

    for id in order while the policy's owned roots exceed root_budget:
        if id names a policy-created checkpoint:
            call remove_checkpoint(id)
            if CheckpointInUse: skip without retrying in this sweep
        else if id names a policy-created session:
            call destroy_workspace_session(id)
        remove id from the registry only after the lifecycle call's durable
            success or exact already-absent outcome

    stop at the bounded page/work limit; continue from a durable policy cursor
        on the next sweep
~~~

This is semantic-retention policy, not PMSS object GC. Only the lifecycle
method removes a root; only a later exact trace/census can reclaim and credit
its physical bytes.

## 18. Strict space and memory proof

### 18.1 Application-memory budget

| Partition | Hard sub-budget | Why it exists |
|---|---:|---|
| Catalog pages and cursors | 2 MiB = 128 x 16-KiB frames | H <= 8 point paths, S1 builders, ordered scans |
| Four worker slabs | 1 MiB total; exactly 256 KiB each | C1/C2 build, hashing, bounded streams |
| Coordinators, readers, replay, permits, queue | 1 MiB | Fixed owners, 64 readers, one bounded cache-off replay working set, 16 zero-payload scheduler descriptors |
| Chunk/hash/codec/trace/sort/merge scratch | 3 MiB | Full-vector admission; no assumed heavy-operation count |
| Accounting, recovery, allocator headroom | 1 MiB | Checked counters, error paths, fragmentation margin |
| **Global managed hard ceiling** | **8,388,608 B exactly** | All storage-owned live allocations |
| **Normal target** | **<= 4,194,304 B** | Future steady-operation qualification target |

Additional concurrency rules:

| Resource | Exact bound |
|---|---:|
| One sandbox’s concurrent managed attribution | <= 4 MiB ceiling; never a reservation |
| Sandboxes simultaneously at that maximum | <= 2 globally; partition limits may reduce this |
| One heavy operation | <= 2 MiB |
| Simultaneous heavy operations | No scalar promise; admit only when every partition and aggregate vector fits |
| Storage workers | 4 |
| Queued heavy descriptors | 16, aggregate <= 64 KiB, payload 0 |
| OwnerSlots | Exactly 16 static lanes: slot 0 is maintenance-only; slots 1..15 are foreground-only; no lane, quota, or reserve is borrowable |
| ReadSlots | 64, each <= 30 seconds absolute |
| Storage-owned FDs | 128 |
| Persistent application cache | 0 B |

Maintenance admission first obtains its complete non-borrowable resource
vector, then selects static OwnerSlot[0] or returns `RetryLater`. It never
waits for or drains a dynamic OwnerSlot pool. A selected slot-0 Build is the
only maintenance fence; no priority field, purpose field, or seventeenth lane
exists.

~~~text
M_managed =
    M_catalog_page_claims
  + M_worker_slab_claims
  + M_coordinator_and_table_claims
  + M_codec_sort_trace_claims
  + M_accounting_recovery_claims
  <= 8,388,608 B

M_one_sandbox <= 4,194,304 B
M_one_heavy   <= 2,097,152 B
count(sandbox with M_one_sandbox = 4,194,304 B) <= 2

for every partition p:
    sum(active_claim[p]) <= partition_cap[p]
~~~

The per-sandbox number is an attribution ceiling, not a preallocated slice.
Idle sandboxes reserve zero bytes, and any number of smaller claims may coexist
only while every shared partition and the global aggregate fit. Two nominally
heavy operations are concurrent only if their full vectors fit;
two 2-MiB claims against the 3-MiB scratch partition do not. C1/C2 charge the
worker partition, S1 page frames charge only the Catalog partition, and S3
charges codec scratch, so bytes are neither hidden nor double-counted.

FD admission uses the same rule:

~~~text
FD_peak = F_control_persistent
          + sum(FD_claim of every admitted active operation)
          <= 128
~~~

The implementation must freeze `F_control_persistent` and inventory every
open, duplicate, pack, arena, HEAD, and directory-sync handle. ReadSlots hold
locator/epoch facts, not FDs; 64 ReadSlots therefore do not authorize 64
simultaneous open streams.

Space is O(1) in repository bytes, file count, checkpoint count, sandbox count,
fork depth, and session count **for resident application memory**, because work
streams or spills to charged disk and admission stops additional work before
buffers, FDs, workers, or staging are acquired. Configured finite limits are
part of the deployment proof; raising them requires recomputing the bound.

Idle sandboxes, checkpoints, forks, and sessions retain no worker, buffer, FD,
ReadSlot, or volatile permit. Durable rows consume bounded Catalog space and
are admitted by record/root quotas.

Every volatile allocation has one acyclic owner. Claims are acquired
all-or-none before tasks start; children are joined before the owner returns;
buffers, frames, streams, FDs, slots, and permits are released on success,
error, timeout, and cancellation. This deterministic lifetime discipline—not
a best-effort language garbage collector—is the memory-reclamation proof.
Process death lets the kernel reclaim all volatile memory and handles;
restart reconstructs only durable OwnerSlots and synchronously disposes or
adopts their bounded artifacts before readiness. Concurrency tests must show a
repeatable post-operation plateau for managed bytes, RSS, cgroup current,
tasks, FDs, permits, ReadSlots, OwnerSlots, staging bytes, and inodes.

### 18.2 Cgroup envelope

One shared PMSS service owns storage work for all sandboxes and workspace
sessions. The controls below apply **once** to that service cgroup, including
every storage helper it starts; they are not multiplied into one 96-MiB budget
per sandbox or session.

| Control | Bound |
|---|---:|
| memory.high | 64 MiB |
| memory.max | 100,663,296 B, exactly 96 MiB |
| memory.swap.max | 0 B |

The exact deployment obligation is:

~~~text
M_service_current =
    baseline_RSS
  + resident_thread_stack_bound
  + allocator_arena_and_fragmentation_bound
  + storage_helper_process_bound
  + M_managed
  + charged_page_cache_writeback_bound
  + charged_dentry_inode_bound

M_service_current <= 64 MiB during every qualified workload
M_service_current < 96 MiB at every instant
~~~

The named terms are measured as non-overlapping cgroup-charged components for
the frozen binary, allocator, helper, filesystem and kernel profile. The
8-MiB permit ledger proves only `M_managed`; it does not prove the service
total. `memory.high` supplies pressure/throttling and a qualification ceiling,
not reclaim credit or a substitute for the inequality. Qualification must
also:

- prohibit mmap for repository-sized structures;
- use bounded aligned read/write windows;
- bound readahead and dirty/writeback behavior;
- drop scratch windows deterministically;
- cap threads and FDs;
- run cache-cold, cache-warm, million-entry, large-file, GC, recovery, and
  concurrent-session cgroup sweeps;
- fail if memory.events reports max, OOM, or OOM-kill.

The 96-MiB envelope is not derivable from the 8-MiB managed ledger alone.
Qualification must freeze the binary, allocator, thread count and stack size,
async-runtime baseline, I/O windows, filesystem, kernel, readahead/writeback
policy, helper set and cgroup configuration, then measure all coexisting
process and kernel-accounted bytes across the shared service. Stage 4.6 is
negative evidence: its campaign peak exceeded the new limit.

### 18.3 Disk reserve

The simultaneous non-borrowable reserve is:

~~~text
D_maintenance >=
    D_aux_max
    + D_trace_max
    + D_closure_scratch_max
    + P_pack_alloc_max
    + D_HEAD
    + D_root_ctl

D_aux_max <= A_alloc(2C_max)

I_maintenance >=
    I_aux_max
    + 1                 # trace
    + 3                 # reusable 36/72-byte closure-sort workspace
    + 1                 # replacement pack
    + I_HEAD
    + I_root_ctl
~~~

`P_pack_alloc_max=A_alloc(64 MiB)` covers one complete replacement pack,
including its exact 8-byte signature and all frames. Its inode counterpart
includes the Auxiliary Catalog, one trace file, two run containers plus one
control file reused across the Delta-edge and pack-census orderings,
one replacement pack, the maintenance HEAD temporary file, and the separately
non-borrowable root-control slice. `D_root_ctl/I_root_ctl` guarantees the
largest complete admitted checkpoint/session/sandbox root-removal workflow can
finish even at storage pressure; it earns no speculative reclaim credit and
bulk maintenance cannot consume it. A maximum-of-phases formula is invalid
across the listed coexisting or simultaneously reserved classes. Within the two
sequential closure orderings,
`D_closure_scratch_max` is valid because the same three files are reused and
each run container is sized to the largest sort bound.

### 18.4 Production-qualification closure ledger

Writable production readiness must remain closed until every row below is an
instantiated format/configuration constant or a passed measurement. A symbolic
formula is useful design evidence but not a deployment proof.

| Area | Must be frozen or measured | Closure test |
|---|---|---|
| C1 | `K1_max`, `P1_max`, frame/edge/header widths, `E1_max` proof, exact codec scratch | Compile-time layout assertions; adversarial deep/wide trie and spill accounting |
| C2 | Actual compiled controls within the 80,768-B slab remainder; allocation-free hot path | Size assertions, allocator-failure injection, eight-level adversaries |
| C3 | Exact 50/16/48-B scratch codecs, one `N_C3_record_max=2,097,152`, three-sort disk bound | Golden vectors with duplicates/moves/hardlink merges; checked occurrence/fragment/output caps and FD accounting |
| S1 | Page header, slot/key/value/child widths, fanout, `C_max`, `p_new` preflight, positional cursor, and root-last arena formula | State-machine page-frame proof; sparse/dense equivalence; full-capacity crash cuts |
| S2 | HEAD codec, `D_HEAD/I_HEAD`, dependency summary, sync/FD paths | Cut every barrier; previous-complete or complete-new result only |
| S3/pack | Exact Full/Delta locator variants with no stored codec or canonical length, exact 8-B signature, exact 34-B RecordHeaderV1, exact-EOF grammar, 64-MiB complete-file cap, and 98,304-B slab | Compile-time bounds; footerless golden files, group-layout and allocation-rounded comparisons |
| GC | `N_*_max`, actual-size trace formula, 36-B Delta edge, 72-B marked pack census, strict `<2^30` per-pack fields, `D_closure_scratch_max`, 40-B/64-entry victim vector with one header policy, checked wide totals, zero-live-pack visibility and allocation-rounded retirement | Maximum trace initialization/validation, writer/recovery overflow rejection, two sequential sorts, replacement-header rescan, each mutually exclusive rewrite policy |
| Managed RAM/FDs | Every operation vector, per-sandbox attribution and persistent handles | All combinations; exact shared `<=8 MiB`, per-sandbox `<=4 MiB` ceiling, at most two maximum sandbox claims, `<=128` FDs and deterministic cleanup plateau |
| Cgroup | Shared-service baseline, allocator, threads/stacks, helpers, page cache/writeback, filesystem/kernel profile | Cold/warm/concurrent sweeps; `M_service_current<=64 MiB` qualified and `<96 MiB` always; one cgroup with high 64 MiB, max 96 MiB, swap 0, no memory events |
| Performance | Matched P4 sparse, portable bytes/facts, journal completeness/fallback | Required percentiles and phase traces; targets remain unachieved until passed |

## 19. Time and space complexity analysis

This table is a derived implementation aid, not a new authority. Every row
states its claim class; `O(1)` RAM means independent of repository/state/root
cardinality under the fixed deployment caps, not literally zero bytes.

### 19.1 Operation complexity

| Operation | Time / byte-I/O | Managed RAM | Additional physical space | Claim class / qualification note |
|---|---|---|---|---|
| C1 directory build | `Theta(D_dir)` | `M_C1`, fixed after codec freeze | `D_C1_scratch(D_dir)` + missing canonical nodes | **ANALYTICAL BOUND**; exact bytes blocked on C1 constants |
| C1 lookup/update path | `O(K_path)` verified nodes; output `O(K_path x P_C1)` | Fixed frame/path claim | Missing changed path nodes | **ANALYTICAL BOUND** |
| C2 full build | `Theta(n_frame)` | Exactly one proposed 262,144-B slab | Missing C2 nodes/chunks; temporary disk 0 | **ANALYTICAL BOUND** plus proposed implementation constant |
| C2 local edit | Expected `O(log N_C2)` changed metadata after resynchronization; worst `Theta(n_frame)` | Same slab | Missing changed objects | Expected term is **HYPOTHESIS**; worst case is **ANALYTICAL BOUND** |
| C3 whole-run attribution | `O(Sort_50(c_old+c_new)+Sort_16(c_match)+Sort_48(c_frag)) + Theta(c_old+c_new+c_match+s_old+c_frag+c_out)` | Fixed run/merge/coalescing claims, heavy vector `<=2 MiB` | Actual `D_C3_actual`; admission reserves `D_C3_max` from the one `2^21` count cap, plus bounded attribution nodes | **ANALYTICAL BOUND**; all three sorts and checked occurrence/fragment/output bounds are mandatory |
| Complete canonical build | `Theta(B_scan) + O(Sort(F+A_fact))` | Fixed admitted claims | Charged fact runs + missing canonical objects | **ANALYTICAL BOUND** |
| Object read of `b` bytes | `Theta(H+b)`; S3 reads at most one Full base and one Delta | Page/stream/98,304-B S3 claims | 0 | **ANALYTICAL BOUND** |
| Portable materialization | `Theta(B_realize+F)` reads/writes | Fixed stream/cursor claims | `Theta(B_realize+F)` private ordinary workspace | **ANALYTICAL BOUND**; repeated non-hardlinked occurrences count each time |
| Portable publication | Per preparation `Theta(B_scan+S_fact+P_reuse+P_new)` plus C1/C2/C3 and external-sort work; source payload reads `<=2B_scan`; canonical comparison bytes `=C_reuse`; physical selected-Store reads `=P_reuse`; physical writes `=P_new`; the bounded invalidation path permits at most two whole preparations | One sandbox `<=4 MiB`, global vector-enforced | One preparation's `P_new` + charged runs + exact S1 preflight pages at a time; the first candidate is synchronously deleted before recapture | **ANALYTICAL BOUND**; neither comparison term is bounded by `B_scan`; total worst case is the sum of at most two preparations |
| Journal-qualified publication | Common work in complete dirty-byte/fact closure + affected Merkle closure; worst case is portable publication | Fixed claims | Missing affected objects + framing | Common case **HYPOTHESIS**; fallback bound is analytical |
| S1 point/rank lookup | `Theta(H)`, `H<=8` | 1 page frame + cursor | 0 | **ANALYTICAL BOUND** |
| S1 sparse commit | `O(K_s1 H)` build work; exact emitted pages `p_new` from preflight include one fresh root written last | Proposed 26 page frames at `H=8` | Exact `D_S1_sparse` + prepared packs; positional candidate cursor starts at selected committed end | **ANALYTICAL BOUND**; no `fstat`, `O_APPEND`, selected padding, trailer, or serialized root offset |
| S1 dense rebuild | `Theta(N)` ordered I/O; one fresh root is emitted last | Proposed 10 page frames at `H=8` + bounded input | `D_aux_max<=A_alloc(2C_max)`; total Catalog `<=4C_max` | **ANALYTICAL BOUND**; selected end is aligned, `>=16 KiB`, and alone derives the root |
| S2 candidate custody preparation | `Theta(P_new+K)` bytes to seal/sync missing-object packs and the one sorted Build-owned cursor | Bounded pack/hash/owner claims; no locator/dependency vector | Charged candidate packs + one charged cursor; consumed input runs are deleted/synced | **ANALYTICAL BOUND**; outside the foreground final gate |
| S2 origin-conflict final gate | Bounded session/sandbox/receipt paths plus fixed ordered durability phases; origin check precedes cursor open | Bounded Catalog/HEAD claims | `D_HEAD`; selected Build custody remains until synchronous abort | **ANALYTICAL BOUND**; no `K`-proportional scan and no candidate locator selection |
| S2 origin-match final gate | Per attempt `Theta(KH+K_delta+selected-candidate-pack install/sync work)`, `K<=N_object_max`, `K_delta<=K`, `H<=8`; one full structural-validation pass precedes one selection/install pass; at most two attempts | Bounded Catalog/HEAD/cursor windows and one scalar selected count per current segment; no resident candidate vector | `D_HEAD` + already durable candidate packs; cursor/non-pack scratch removed before selection | **ANALYTICAL BOUND**; no pack installs before complete validation; exact combined maximum and tail latency are admission gates |
| S2 other sparse final gates | `O(K_s1 H)` preflight-admitted Catalog build plus bounded replay checks and fixed durability phases | Bounded Catalog/HEAD claims | Exact `D_S1_sparse+D_HEAD` | **ANALYTICAL BOUND**; not a publication-candidate bound |
| S2 maintenance-lane admission | One static OwnerSlot[0] check/update after the complete non-borrowable maintenance vector is admitted; return `RetryLater` if unavailable | Bounded Catalog/HEAD claim; no dynamic waiter state | No foreground staging and no borrowed quota | **ANALYTICAL BOUND**; selecting slot 0 is the sole global maintenance fence |
| S2 fenced maintenance pause | `Theta(N_object+N_pack+X_live)` including trace, sorts, rewrite, dense build/validation and selector | One heavy vector plus bounded Catalog/HEAD claims | Prepared Auxiliary + replacement + `D_HEAD` | **ANALYTICAL BOUND**; all non-maintenance S2 mutations receive `RetryLater`; reads/private edits continue |
| S2 dense final selector | `O(1)` in repository size after the fenced preparation | Bounded Catalog/HEAD claim | Synchronized Auxiliary/replacement + `D_HEAD` | **ANALYTICAL BOUND**; exact MaintenanceBasis cannot become stale because the Build row is the global write fence |
| S2 critical recovery | Bounded HEAD/control setup + streamed selected dependency verification | Fixed recovery vector | 0 additional | **ANALYTICAL BOUND** after format caps freeze |
| S3 encode/decode | `Theta(target length)`, target `<=32 KiB` | Proposed exact 98,304-B slab | One Full or Delta frame | **ANALYTICAL BOUND** plus proposed slab constant |
| Checkpoint/fork/rollback/fork commit | `O(H)` per changed typed key | Exact admitted S1/S2 vector | Bounded rows only; payload copy 0 | **ANALYTICAL BOUND** |
| Exact logical trace | `Theta(D_trace(N_object) + R_scan + (N_roots+E_reach+N_reach)H + N_reach L_trace(N_object) + B_reach + N_object)` | One heavy vector `<=2 MiB` | Actual `D_trace(N_object)` allocation, with `D_trace_max` reserved; one inode | **ANALYTICAL BOUND**; initialization/validation scale with the captured Catalog |
| Physical closure and installed-pack census | `Theta(36N_delta(1+passes_edge)+72N_pack_record(1+passes_pack))` sort byte-I/O + `Theta(N_object+N_pack)` sequential census | Initial run `<=1 MiB`; merge `<1 MiB`; complete vector `<=2 MiB` | `D_closure_scratch_max`, exactly three reused scratch inodes | **ANALYTICAL BOUND**; `DeltaEdgeV1` stores only base ID plus target rank; every selected row, including dead, and every installed pack is represented; no pins, PackCatalog, relocation stream or third sort |
| One `REWRITE_BATCH` | Fenced trace/census + `Theta(N_object+N_pack+X_live)` rewrite/header rescan, `X_live<=64 MiB-8 B`, `p<=64` | Fixed trace/sort/S3 vector + 4-KiB victim vector | One output `X_alloc<=P_pack_alloc_max=A_alloc(64 MiB)` + Auxiliary/reserve; old bytes charged until retirement | **ANALYTICAL BOUND**; DEAD/EMERGENCY/CONSOLIDATE prove physical progress, NORMALIZE proves Delta-count progress separately |
| Export | `Theta(B_realize+F)` | Fixed stream/cursor vector | Selected sink output | **ANALYTICAL BOUND** |

No row has a term in logical layer depth because PMSS has no layer depth.

### 19.2 Persistent and peak-space complexity

| Space class | Bound | Why it cannot be smaller in general |
|---|---|---|
| Canonical objects reachable from retained roots | `Theta(U_reach)`, where `U_reach` is the unique reachable canonical information after ObjectId deduplication and chosen S3 encodings | Distinct retained information must exist somewhere; content addressing removes duplicates, not information |
| `v` deliberately retained complete states | Between one shared state and `Theta(sum of unique differences across v states)` | Checkpoints are semantic promises; an adversary can change every byte in every retained state |
| Repeated edits with no retained old root | Latest reachable state + temporarily charged unreachable objects until exact reclaim | Publication count itself is not a root; exact GC can reclaim every unrooted predecessor |
| Repeated edits with `v` retained checkpoints | Shared unchanged C1/C2 graph + S3 Full/Delta groups + every unique retained change | No correct GC may delete bytes needed by an explicit checkpoint or session origin |
| Catalog | Exactly two arenas, each `<=2C_max`, total `<=4C_max` | Old selected/reader-visible layout and Auxiliary replacement can coexist |
| Selected packs | Reachable selected encodings + pack framing/slack under hard byte/inode quotas | Immutable frames need placement; normalization/repack minimizes but cannot erase live bytes |
| Unselected/staged/retired bytes | Fully charged until durable adoption or synchronized deletion; root deletion gives zero early credit | Crash recovery and active readers may still require them |
| One active materialized session | `Theta(B_realize+F)` private allocation plus admitted growth | Portability requires private ordinary files; no reflink/FUSE/shared Store bytes |
| Checkpoint/fork metadata | `O(1)` bounded typed rows per operation, plus the objects their StateIds deliberately retain | Pointer creation copies no payload, but retention can keep unique content live |
| C1 scratch | `D_C1_scratch(D_dir)`, one inode | Resident child vectors would violate cardinality-independent RAM |
| C3/sort scratch | Allocation-rounded two-run-container formulas for admitted fixed-width records | Exact ordering without an object-count-sized RAM map requires spill |
| Exact GC scratch | Actual `D_trace(N_object)` plus `D_closure_scratch_max`, while the full maxima remain reserved; four inodes total | Exact state bits and two sequential required orderings cannot be inferred from approximate/refcount metadata; both sorts reuse the same three inodes |
| Simultaneous maintenance reserve | `D_aux_max + D_trace_max + D_closure_scratch_max + P_pack_alloc_max + D_HEAD + D_root_ctl` plus exact inode sum including `I_root_ctl` | Every listed class can coexist or must remain simultaneously reserved at a crash-safe cut; bulk work may not borrow root-removal capacity or future deletion credit |
| Managed storage RAM | One shared service is `O(1)` in repository cardinalities; hard `<=8,388,608 B`, per-sandbox attribution ceiling `<=4,194,304 B`, at most two simultaneous maximum sandbox claims | Larger inputs stream or spill; the sandbox ceiling is not a reservation, and admission rejects concurrency before allocation |
| Persistent cache | `0 B` | Correctness and baseline performance cannot depend on retained cache state |

The semantic lower bound matters: no squash, compactor, or compression scheme
can promise sublinear storage in the amount of distinct information that the
user explicitly asks PMSS to retain. The control is an explicit finite
retention policy, structural sharing, S3's depth-one encoding, exact tracing,
and bounded physical repack—not hidden history deletion.

## 20. Historical MPLA evidence and expected PMSS improvement

Stage 4.6 evidence comes from
[[implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/mpla_poc_benchmark_report|the sealed MPLA POC benchmark report]].
All values below are historical project measurements of MPLA, not PMSS
performance results. The sealed terminal decision was:

~~~text
POC_CORRECTNESS_PASS
POC_100X_NOT_SUPPORTED
POC_500X_NOT_SUPPORTED
AG_SQUASH_PASS
AG_STREAM_PASS
~~~

Small publication was the aggregate-multiplier blocker. The campaign used
`CLOCK_MONOTONIC`, not `CLOCK_MONOTONIC_RAW`, in a Linux/arm64 guest under
macOS Docker Desktop with 4 vCPU and 4 GiB. Most matched multiplier rows have
three candidate and three control observations; exact activation has five
candidate and three control observations. The sealed campaign supplies no p95
or p99 for those matched rows. F0, P0, and P6 are individual campaign
boundaries rather than percentile distributions.

Its 8-GiB S4 fixture was eight sparse logical allocations with zero allocated
payload bytes. Its P4 fixture added 1,048,576 logical sparse bytes across ten
files with zero allocated payload, 1,737 B of affected input, and 44 output
objects totaling 12,188 B. Neither fixture predicts dense ordinary-file work.

### 20.1 Historical evidence ledger

| Historical workload | MPLA project measurement | Historical decision/threshold | PMSS interpretation |
|---|---|---|---|
| Cold 8-GiB sparse construction | 1.228642917 s outer vs 133.683 s = 108.805412989x; 1.102406542 s service vs 129.932 s = 117.862145270x; complete process 3.99 s | Multiplier passed on the zero-payload sparse fixture | Useful sparse-work evidence only; not dense ingestion evidence and not a PMSS target |
| Warm attachment | 24.825208 ms service; 374.467417 ms complete in-service preparation; payload copied 0 | Historical source result | PMSS portable materialization still has `Theta(B_realize+F)` allocation; no transfer of a privileged/mount fast path |
| Exact activation | 21.375375 ms median vs 13,426.207298 ms = 628.115637644x | Preferred `<=19.975350676 ms` historical ceiling failed | Activation-boundary evidence only; it does not prove end-to-end private ordinary-file PMSS materialization |
| Historical MPLA “same-generation activation” | 21.155500 ms vs 11,310.809838 ms = 534.651028716x | Preferred `<=20 ms` historical ceiling failed | Source workload name only; PMSS has no generation identity |
| Fork | 7.706708 ms vs 13,277.046215 ms = 1,722.790874521x | Preferred `<=2 ms` historical ceiling failed | Supports metadata-pointer direction, but PMSS S1/S2/fsync latency remains unmeasured |
| Rollback | 16.487709 ms vs 13,158.580589 ms = 798.084232867x | Preferred `<=10 ms` historical ceiling failed | Supports StateId selection over reconstruction, but is not a PMSS latency result |
| Small sparse publication | Matched candidate median 58.136209 ms, matched max 62.567625 ms, all-five candidate max 65.937250 ms; control 36.444000 ms; score 0.626872660x, so candidate was 1.595220311x slower | `<=20 ms` and aggregate 100x/500x failed | This is the accepted PMSS optimization focus |
| Old P4 100x criterion | Control 36.444000 ms implied `<=0.364440 ms` | **Historical requirement**, neither measured nor achieved; not a PMSS target | The new 10x-over-candidate stretch does not satisfy the old 100x criterion |
| Durable 1-GiB stream | 1,073,741,824 B in 994.910334 ms including checksum = 1.005115703 GiB/s | 1-GiB/s floor passed; historical 5-GiB/s stretch missed | Useful implementation evidence, not a PMSS throughput result or accepted PMSS target |
| Historical squash | 6.504750 ms outer median; 0.831042 ms service median | Squash gate passed | PMSS deletes the operation; repack/normalization are physical maintenance, not renamed squash |
| Campaign memory | Peak cgroup 102,543,360 B; peak RSS 36,687,872 B; P7 cgroup 101,289,984 B | Old POC profile passed; new exact 96-MiB requirement was not the campaign gate | Negative evidence for PMSS: campaign and P7 both exceed the new cap |

The historical MPLA accelerator used an authorized OverlayFS/
`CAP_SYS_ADMIN` profile. PMSS may not add `CAP_SYS_ADMIN`, use reflink or FUSE,
or share Store/workspace bytes. A future runtime-internal accelerator must
still produce a complete private realization and prove that it affects no
canonical identity, correctness, retention, or portable fallback. Therefore
the warm/activation measurements cannot be copied into a PMSS expectation.

### 20.2 Expected performance-improvement and closure table

| PMSS path or resource | Evidence baseline | Expected algorithmic effect | Numeric bound/target | Current status |
|---|---|---|---|---|
| P4-compatible sparse publication | MPLA median 58.136209 ms; control 36.444000 ms | Remove layer/mount/squash/remount choreography; reuse C1/C2 objects; prepare one pack; sparse S1 update; one S2 selection; optionally use only a qualified complete journal | **TARGET:** `<=5.8136209 ms`, exactly 10.000x faster than MPLA candidate and 6.268726604x faster than the old control | Accepted stretch target, unmeasured and not an SLA |
| Portable publication | No comparable PMSS measurement | Missing-object-only writes and bounded same-ID verification | **ANALYTICAL BOUND:** source payload reads `<=2B_scan`; canonical comparisons `=C_reuse`; actual selected-Store reads `=P_reuse`; actual framed writes `=P_new` | Algorithmic accounting only; neither comparison term is bounded by source payload bytes and there is no universal millisecond promise |
| Journal-qualified small-dirty publication | Portable full scan is the correctness fallback | Replace discovery with complete dirty-byte/fact closure; retain the same canonical build and S2 result | **HYPOTHESIS:** may reach the P4 10x target when dirty closure is tiny; no accepted general multiplier | Disabled until loss, overflow, rename/link, restart, and fallback proofs pass |
| Checkpoint/fork/rollback | Historical MPLA shows 798x–1,723x against full-copy/reconstruction controls | `O(H)` typed metadata paths and zero payload copy | **ANALYTICAL BOUND:** payload-copy work 0; no proposed latency number | PMSS benchmark required with identical S2 durability boundary |
| Repeated retained same-line edit | No isolated POC ratio | C2 structural sharing + depth-one S3 splice + exact `PackAlloc` normalization | **ANALYTICAL BOUND:** selected Delta frame `<=1/4` Full; **HYPOTHESIS:** `>=10x` only when measured framed Delta `<=10%` of Full | Must report frame and allocation-rounded pack bytes separately |
| Exact `REWRITE_BATCH` | No comparable POC measurement | One trace/census executes exactly one policy: a physical policy can retire up to 64 sources, while `NORMALIZE` has zero victims and rewrites selected singleton Deltas; each copies in ObjectId order and rescans replacement headers | **ANALYTICAL BOUND:** `p<=64`, `X_live<=64 MiB-8 B`; DEAD requires `2X_alloc<=V_alloc`; physical convergence `<=ceil(eligible_packs/64)` batches; policies never mix | Unmeasured; stop-the-write-side pause at full `C_max` is an explicit production gate |
| Portable Docker materialization | Historical privileged activation is non-transferable | One complete state, no layer/attribution walk; bounded sequential filesystem/content read/verify/write | **ANALYTICAL BOUND:** `Theta(B_realize+F)` and private allocation of the same order | Correctness fallback only; 10x is not plausible for dense 1-GiB realization and is currently unmet |
| Adapter-owned disposable projection | No comparable PMSS measurement | A StateId-scoped runtime projection or snapshotter/OverlayFS lower-reuse may reduce realization only if it has no identity authority and exact dependency/eviction accounting | **HYPOTHESIS:** could accelerate warm Docker sessions; no accepted multiplier | Disabled until capability, isolation, complete-private-realization, eviction/recovery and portable-fallback qualification pass |
| Logical squash | Historical MPLA paid an explicit squash operation | Entire lifecycle operation and its remount choreography disappear | **ANALYTICAL BOUND:** squash-call count 0 and logical depth term 0 | Architectural result; no replacement latency target |
| Stream throughput | MPLA 1.005115703 GiB/s | Bounded streaming without version-chain reconstruction | Historical 5-GiB/s stretch would require 4.974551671x over that result, but it is **not an accepted PMSS target** | Benchmark on frozen PMSS format/hardware before setting a target |
| Managed memory | POC had an 8-MiB budget, not a measured PMSS allocation ledger | One shared service uses allocation-free slabs, 128 Catalog frames, disk spill, all-or-none concurrency vectors and cache 0 | **TARGET:** `<=4 MiB` normal shared aggregate; **REQUIRED:** `<=8 MiB` shared hard ceiling, per-sandbox attribution `<=4 MiB` as a ceiling rather than reservation | Unmeasured PMSS requirement |
| Parallel active workspace sessions, 1/4/8/16/32/64 | Stage 4.6 did not qualify this matrix | Separate idle session identity from admitted Store work; admit complete worker/owner/reader/FD/memory vectors before allocation; slots 1..15 bound foreground custody, while static slot 0 and its quota/reserve remain maintenance-only and non-borrowable | **REQUIRED:** at most 4 workers, 15 foreground OwnerSlots plus one maintenance OwnerSlot, 64 ReadSlots, 16 payload-free scheduler descriptors, 128 FDs and `<=8 MiB` managed aggregate; the 16th simultaneous foreground claimant returns `RetryLater`; at most two sandboxes can simultaneously hold the 4-MiB attribution maximum | Unmeasured; report throughput, admission rejection, p50/p95/p99/max, deterministic cleanup plateau, and the full `Theta(N_object+N_pack+X_live)` maintenance mutation pause at every load level |
| Idle workspace-session residual | No Stage 4.6 steady-state comparison | Keep a Mutable session's semantic origin only in its small Catalog row; Terminal drops origin and keeps only status/allocation; both release volatile Store execution resources | **REQUIRED:** 0 Store worker, buffer, FD, ReadSlot and resident cache per idle session | Must be verified after success, error, cancellation, conflict and restart; the applicable durable row and adapter-private allocation remain separately charged |
| Cgroup envelope | Campaign 102,543,360 B; P7 101,289,984 B | Apply one cgroup to the shared PMSS service and helpers; freeze allocator/stacks/I/O windows, bound cache/writeback and clean up deterministically | **REQUIRED:** `M_service_current<=64 MiB` in qualification and `<96 MiB` always; max 100,663,296 B, high 67,108,864 B, swap 0. Campaign needs 1.833433194% reduction; P7 needs 0.618706782% | Current evidence fails the new cap |

The P4 `5.8136209 ms` target is valid only when the logical fixture/edit shape,
visibility and durability boundary, correctness oracle, source/stored-byte
accounting, candidate/control allocation, and setup/teardown inclusion remain
matched. Qualification must report at least p50, p95, p99, maximum, and
phase-level traces with cache state explicit.

The portable full-scan path cannot promise 5.8 ms for arbitrary `B_scan` and
`F`: correctness has lower bound `Omega(B_non-hole+F)`. The only plausible
route to the 10x sparse target is a proven-complete journal closure plus C1/C2
locality, candidate-custody preparation outside the final gate, one sparse S1
update, and one short S2 selection. Until measured, that remains a target and
hypothesis—not a claimed optimization result.

## 21. Non-normative implementation order

Repository placement, crate names, facade names, and module boundaries are
deliberately deferred to a separate code-layout review. They are not storage
architecture and must not become additional authorities or runtime
components. The dependency order is:

Implementation order:

1. Freeze restricted canonical codec, object kinds, format caps, and golden
   vectors.
2. Implement C1, adopted payload FastCDC, C2, and C3 with adversarial vectors.
3. Implement PackSegment Full records and verified streaming object reads.
4. Implement S1 page codec, sparse path-copy, dense build, and checked rank.
5. Implement S2 commit/recovery and crash injection before exposing writes.
6. Implement S3 encode/decode, current-root Full-base revalidation, and
   normalization through the one rewrite engine; add no locator pin.
7. Compose Lifecycle checkpoint/fork/rollback/publication semantics.
8. Implement descriptor-safe adapter materialization and two-pass stable
   capture.
9. Implement exact trace, sequential 36/72-byte physical-closure sorts,
   64-source ObjectId-ordered `REWRITE_BATCH`, replacement-header rescan,
   retirement, maintenance mutation fence and simultaneous reserve.
10. Enforce admission and run performance/resource qualification with cache
    disabled first.

## 22. Proposed qualification checklist

### Correctness and format

- same supported facts always produce the same StateId across discovery order
  and backend;
- every object verifies kind, version, canonical bytes, length, references,
  caps, and BLAKE3;
- HEAD round-trips exactly `{type_tag, StoreSequence, ArenaId,
  committed_arena_length, checksum}`; every selected end is aligned and at
  least 16 KiB, its root is derived only as `end-16 KiB`, and the final page is
  fresh with no selected bytes after it;
- PackSegment golden files have the exact 8-byte `PMSSPK1\0` signature, at
  least one exact 34-byte-header frame, and exact EOF with no footer, padding,
  trailer, or embedded index; SegmentId verifies the complete file;
- C1 insertion/adversarial path, C2 boundary, C3 duplicate/move/actor, sparse,
  hardlink, and raw-name vectors pass;
- Full and S3 decode return byte-identical canonical objects;
- checkpoints, forks, rollback, strict-origin sibling publication, and ordered
  P/C/B fork commit pass exact state tables.

### Crash safety

- inject every pack, Catalog, HEAD temporary, rename, directory-sync,
  retirement, AdapterClose, Build abort, trace, and both closure-sort cuts;
- observe only previous complete or complete new selected state;
- never elect Auxiliary or an older StoreSequence;
- exact retained receipts replay;
- first candidate invalidation deletes and synchronizes the complete Build
  staging set before one whole recapture; second invalidation exact-aborts and
  returns `RetryLater`; no pack is installed before full revalidation;
- non-resumable trace scratch is always discarded after ambiguity.

### Resource safety

- 1 and 4 workers, static maintenance OwnerSlot[0], 15 foreground OwnerSlots,
  64 readers, 16 scheduler descriptors, and 128 FDs; the 16th simultaneous
  foreground claim returns `RetryLater` and no class borrows another's quota;
- shared-service 4 MiB target and 8 MiB hard managed-memory accounting,
  per-sandbox attribution `<=4 MiB` as a ceiling rather than reservation, and
  no more than two simultaneous maximum sandbox claims;
- one shared-service cgroup with exact 64/96 MiB controls, swap 0,
  `M_service_current<=64 MiB` in every qualified workload and `<96 MiB`
  always;
- million entries, huge directories/files, many roots, many sessions, repeated
  conflicts, full disk/inodes, GC churn, and recovery;
- deterministic return to a cleanup plateau for RAM, tasks, FDs, permits,
  staging, charged bytes, and inodes.
- at `C_max` and 1/4/8/16/32/64 active sessions, freeze and pass maximum
  maintenance mutation-pause, `RetryLater` fairness, recovery and cleanup
  thresholds; do not report the O(1) final selector as the whole pause;

### Performance

- measure P4-compat-sparse publication against the unmeasured
  `<=5.8136209 ms` 10x stretch target; this checklist does not promote it to an
  SLA or accepted gate;
- checkpoint/fork/rollback report comparable S2 durability boundaries and
  p50/p95/p99/max; no PMSS latency threshold is claimed before measurement;
- streaming reports comparable end-to-end checksum throughput; the historical
  1.005115703-GiB/s MPLA result is evidence, not a PMSS gate;
- portable publication reports `B_scan`, `F`, `A_fact`, `S_fact`, source reads,
  `C_reuse`, `P_reuse`, `P_new`, run bytes, synchronization time, and
  p50/p95/p99/max;
- journal fast path is enabled only after completeness/fallback tests and a
  repeatable material benefit;
- cache remains absent unless cache-disabled evidence proves a repeatable gain
  and cache loss cannot affect correctness.

## 23. Obsidian reference map

- [[implementation-plan/2.0 migration/system-design/index|Accepted PMSS design and mechanism registry]]
- [[implementation-plan/2.0 migration/system-design/system_requirements|Locked system requirements and resource profile]]
- [[implementation-plan/2.0 migration/system-design/architecture/overall_architecture|Minimal architecture and ownership]]
- [[implementation-plan/2.0 migration/system-design/architecture/mpla_demonstrations|Incremental state, no-squash, materialization, and retention demonstrations]]
- [[implementation-plan/2.0 migration/system-design/components/canonical_state|Canonical State, C1, C2, and C3]]
- [[implementation-plan/2.0 migration/system-design/components/durable_store|Durable Store, S1, S2, S3, GC, and admission]]
- [[implementation-plan/2.0 migration/system-design/components/workspace_engine|Materialization and publication workflows]]
- [[implementation-plan/2.0 migration/system-design/components/lifecycle_engine|Versioning, checkpoints, forks, rollback, and semantic roots]]
- [[implementation-plan/2.0 migration/system-design/components/backend_adapters|Stable capture, portability, and quota qualification]]
- [[implementation-plan/2.0 migration/system-design/api_methods|Locked public API semantics]]
- [[implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/mpla_poc_benchmark_report|Stage 4.6 sealed POC benchmark evidence]]
- [[implementation-plan/2.0 migration/system-design/refine/index|Six-phase refinement and acceptance audit]]
