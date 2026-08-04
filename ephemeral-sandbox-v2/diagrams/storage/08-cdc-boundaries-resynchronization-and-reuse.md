# CDC boundaries, resynchronization, and Chunk reuse

Date: **2026-08-04**

Design status: **`PROPOSED` CAS+CDC algorithm family — not selected by the
current Phase 01 decision**

This chapter supplies the CDC algorithm view that was missing from the storage
diagram set. It explains how changed regular-file bytes can become immutable
Chunks, how an edit can preserve an unchanged suffix, and where the algorithm
must fall back to a complete scan.

The design is backend-agnostic. CDC consumes and produces bounded byte streams;
Chunk admission uses the durable backend contract in
[proposed backend abstraction and runtime isolation](04-ephcow-runtime-view.md). No runtime
filesystem feature is part of the boundary algorithm.

FastCDC-style gear hashing is the leading research hypothesis, not a selected
algorithm or benchmark winner. Exact fingerprint family, masks, seed, and
minimum/target/maximum sizes remain versioned Phase 02/03 choices after the
joint CAS+CDC architecture is selected.

## Question answered

How can LayerStack-0 turn one changed file into stable content-derived Chunks,
reuse equal Chunks from earlier Versions, and remain correct when locality
hints or boundary resynchronization are unavailable?

```text
frozen complete file bytes
           |
           v
versioned CDC boundary detector
           |
           v
ordered candidate Chunk byte streams
           |
           v
typed ChunkId + occupied-ID full-byte comparison
           |
           +---- equal occupant ----> reuse accepted Chunk
           +---- vacant ------------> durably admit new immutable Chunk
           `---- unequal occupant --> collision; fail closed
           |
           v
complete ordered ChunkId sequence for this file
```

The output describes the complete file. It is never a parent-relative patch.

## Legend and variables

```text
[I]  immutable accepted Chunk or Version
[T]  private bounded candidate/staging bytes
[H]  optional trusted change hint
[P]  proposed algorithm family

====> file-content byte flow
----> metadata/control flow
....> optional optimization evidence
-X--> forbidden correctness dependency
```

```text
N = bytes in the frozen file
D = bytes directly edited
S = bytes scanned or re-scanned by CDC
K = unique new Chunk bytes durably written
C = number of output Chunks
W = fingerprint state size; constant for one ChunkerSpec
R = distance scanned before a verified reusable boundary/suffix
H = number of trusted disjoint change windows
```

Required parameter record:

```text
ChunkerSpec
  algorithm_id
  algorithm_version
  minimum_chunk_bytes
  target_chunk_bytes
  maximum_chunk_bytes
  fingerprint_seed/domain
  early_cut_rule
  late_cut_rule
```

The `ChunkerSpec` or its stable identifier must be part of the representation
needed to interpret a Version manifest. Two implementations must not silently
use different boundary grammars under one format version.

## 1. CDC is a file-content algorithm

CDC operates independently on each regular-file byte stream:

```text
complete Workspace Candidate
|
+-- README.md       ==== CDC independently ====> [C01, C02]
+-- app/main.py     ==== CDC independently ====> [C03, C04, C05]
+-- data/model.bin  ==== CDC independently ====> [C06 ... C42]
+-- empty.file      ---------------------------> [] + explicit zero length
+-- directory       ---------------------------> manifest entry; no Chunks
`-- symlink         ---------------------------> target in manifest; no Chunks
```

Chunk boundaries do not cross file boundaries. Paths, directories, entry
kinds, metadata, empty files, and symlink targets remain in the complete
Version manifest; Chunks store regular-file content bytes only.

## 2. Boundary selection

The generic normalized CDC family uses a small fingerprint state while scanning
between configured minimum and maximum sizes:

```text
one candidate Chunk

start                                                     forced end
  |                                                           |
  v                                                           v
  +----------+----------------------+-------------------------+
  0         min                   target                     max
             |                      |                          |
             | early region         | late region              |
             | lower cut chance     | higher cut chance        |
             +----------------------+--------------------------+
                        content-derived cut, or force at max
```

Conceptual pseudocode:

```text
function next_boundary(stream, spec):
    start = stream.position
    fp = spec.initial_fingerprint()

    while stream.position - start < spec.maximum_chunk_bytes:
        byte = stream.read_one()
        if byte == EOF:
            return stream.position

        fp = spec.update(fp, byte)
        size = stream.position - start

        if size < spec.minimum_chunk_bytes:
            continue

        if size < spec.target_chunk_bytes:
            if spec.early_cut_rule.matches(fp):
                return stream.position
        else:
            if spec.late_cut_rule.matches(fp):
                return stream.position

    return start + spec.maximum_chunk_bytes
```

This pseudocode fixes the required shape, not the exact fingerprint. The final
algorithm must define EOF behavior, arithmetic overflow behavior, seed/domain,
mask semantics, parameter bounds, and stable test vectors.

### Visual example

```text
file bytes

0                                                               N
|---------------------------------------------------------------|
         ^ scan fingerprint        ^ match       ^ force
         |                         |             |
         min                       cut           max

result

|---------- C01 ----------|------ C02 ------|--------- C03 -----|
0                         b1                b2                  N
```

The byte positions `b1` and `b2` follow from content plus the versioned
ChunkerSpec. They do not depend on a storage backend, inode, block size, path,
mount, or agent identity.

## 3. Why CDC can localize an insertion

Fixed-size blocks shift every later boundary after an insertion:

```text
before insertion

|---- F1 ----|---- F2 ----|---- F3 ----|---- F4 ----|

after inserting "xyz" near the start

|---- N1 ----|---- N2 ----|---- N3 ----|---- N4 ----|...
             most later block contents differ
```

Content-derived boundaries can eventually return to boundaries in unchanged
content:

```text
before edit

|------ C01 ------|------ C02 ------|------ C03 ------|------ C04 ------|
                   old edit region                         reusable suffix

after insertion

|------ C01 ------|-- N11 --|---- N12 ----|------ C03 ------|------ C04 ------|
                                           ^
                                           verified resynchronization point
```

This is an expected locality property, not a correctness or worst-case
guarantee. Adversarial or unlucky bytes can prevent an early match and force a
scan to EOF.

## 4. Safe localized rechunking

CDC boundary matching alone does not prove that the rest of a live file is
unchanged. Localized capture is valid only when a trusted frozen-Workspace
change source proves which byte ranges can differ.

```text
frozen file + prior complete Chunk map
                  |
                  v
trusted old/new edit windows available and complete?
          /                              \
        yes                               no
         |                                 |
         v                                 v
normalize and merge windows          scan complete file
         |
         v
restart at a safe prior Chunk boundary
         |
         v
rechunk through changed window and forward
         |
         v
candidate boundary aligns with proven unchanged old suffix?
          /                              \
        yes                               no
         |                                 |
         v                                 v
full-byte verify reused Chunks       continue, possibly to EOF
         |
         v
compose complete file Chunk sequence
```

Required safety conditions for stopping early:

1. The Workspace is frozen for the capture.
2. The change source is authoritative for all writes that could affect the
   file; a best-effort notification is not enough.
3. All edit windows are normalized, ordered, and expanded to safe prior Chunk
   boundaries.
4. No later dirty window remains beyond the proposed resynchronization point.
5. Reused Chunk occupants are read under valid custody and verified according
   to the accepted representation.
6. The final ordered Chunk sequence reconstructs exactly the frozen complete
   file bytes.

If any condition is unavailable, the algorithm scans the complete changed
file. Correctness must never depend on change hints.

## 5. Multiple edits and overlapping windows

```text
raw edit hints

       [h1----------]
          [h2-------------]
                                      [h3----]

normalize + merge + expand to safe boundaries

|---- reusable ----|====== window A ======|---- reusable ----|== window B ==|...
                   ^                       ^                   ^
             restart boundary       resync candidate     restart boundary
```

Conceptual workflow:

```text
function normalize_windows(hints, prior_chunk_map, limits):
    validate bounds and generation
    sort by new-file position
    merge overlaps and adjacent windows
    reject if count/metadata exceeds limits
    expand each start to a safe prior Chunk boundary
    return disjoint ordered windows
```

If the window count exceeds the configured limit, normalization metadata is
ambiguous, or edits cannot be mapped safely between old and new offsets, fall
back to scanning the complete file.

## 6. Reuse decision versus collision decision

A boundary produces candidate bytes, not an accepted Chunk:

```text
candidate Chunk bytes [T]
          |
          v
derive typed ChunkId
          |
          v
is identifier occupied?
      /             \
    no               yes
     |                 |
     v                 v
bounded staging    compare FULL occupant bytes
     |              /                     \
     v            equal                  unequal
durable admit       |                       |
     |               v                       v
     +------------> reuse                 COLLISION
                                             |
                                             v
                                      fail publication closed
```

Digest match, length match, a second digest, or “same boundary position” is not
full-byte equality. The durable backend profile must make concurrent equal
admission converge without exposing a partially durable occupant.

## 7. Complete file and Version construction

```text
old Version V1                       new frozen Workspace

main.py -> [C01,C02,C03]             main.py changed locally
data   -> [C10,C11]                  data unchanged and proven
                  \                    /
                   \                  /
                    v                v
                  capture each regular file
                    |
                    +-- main.py -> [C01,N20,N21,C03]
                    `-- data    -> [C10,C11]
                    |
                    v
             complete new Workspace manifest V2
                    |
                    v
        manifest + every transitively named Chunk
                    |
                    v
              complete Version admission
```

V2 never says “apply N20 and N21 to V1.” Its manifest directly names the full
ordered content of every regular file and all other accepted workspace facts.

## 8. Multi-agent reuse

```text
                         Accepted Version V1
                                  |
              +-------------------+-------------------+
              |                                       |
              v                                       v
       agent-a Workspace                        agent-b Workspace
       edits model.bin                          edits main.py
              |                                       |
              v                                       v
       CDC -> N30,N31                           CDC -> N40
              |                                       |
              v                                       v
       Version V2 manifest                     Version V3 manifest
       [C01,N30,N31,C04]                       [N40,C11,C12]

shared accepted Chunks remain immutable and may be named by V1, V2, and V3
```

Agent isolation belongs to the Workspace adapter. Chunk reuse happens only
after frozen content capture and collision-safe admission; live upperdirs do
not point directly into mutable Chunk objects.

## 9. Failure and fallback table

| Condition | Required behavior |
|---|---|
| No prior Version | Scan every regular file; build the first complete Chunk sequences. |
| File is known unchanged by trusted complete evidence | Reuse its prior complete entry/Chunk sequence after required validation. |
| Only changed-path hints are trusted | Scan each complete changed regular file. |
| Trusted byte-range edit log is complete | Localized rechunking may be attempted. |
| Hint generation does not match frozen Workspace | Reject hints and scan complete affected scope. |
| Windows overlap or are excessive | Normalize within limits or fall back to complete-file scan. |
| No boundary resynchronization before EOF | Complete scan result is valid; no locality guarantee. |
| Chunk identifier occupied by unequal bytes | Fail closed as collision. |
| Backend admission fails or is cancelled | Head remains unchanged; clean bounded private staging. |
| Crash after some Chunks are admitted but before Version admission | Chunks are immutable unreferenced occupants/debt handled by recovery and reclamation. |
| Stale OCC after complete Version admission | Version may remain unrooted; no merge/rebase; bounded retirement handles it. |

## 10. Complexity

### Full-file CDC

```text
time             O(N)
streaming memory O(W + maximum_chunk_bytes)
output metadata  O(C)
payload read     N
new payload write K, where 0 <= K <= N
```

The implementation may stream candidate Chunk bytes into bounded staging so it
does not retain the complete file in memory.

### Localized capture with trusted windows

```text
expected scan    O(sum(changed windows + resynchronization distance))
metadata         O(H + affected output Chunks)
streaming memory O(W + maximum_chunk_bytes + bounded window metadata)
worst-case scan  O(N)
new payload write K, bounded by bytes in newly admitted Chunks
```

`D` does not imply `S = D`. Boundary disturbance, missing evidence, fragmented
edits, or failure to resynchronize can make `S` approach `N`.

### Workspace capture

For total workspace payload `N_total`, entry count `E`, and changed-file scan
bytes `S_total`:

```text
canonical tree work          at least O(E)
content work with safe reuse O(S_total)
fallback content work        O(N_total)
new durable payload          K_total unique new Chunk bytes
```

No asymptotic or latency advantage is accepted until measured with matched
semantics and durability.

## 11. Benchmark and observability diagram

```text
fixture
  +-- append
  +-- overwrite middle
  +-- insert near start
  +-- delete range
  +-- truncate
  +-- multiple disjoint edits
  +-- repetitive/adversarial bytes
  +-- incompressible bytes
  `-- no-hint full fallback
          |
          v
record
  bytes_scanned
  bytes_chunked
  resynchronization_distance
  chunks_reused / chunks_admitted
  unique_chunk_bytes_written
  collision_full_compare_bytes
  peak_staging_bytes / peak_RSS
  CPU time and p50/p95/p99 elapsed
  backend operation counts
```

Every result must record ChunkerSpec, code revision, fixture bytes, backend
profile, durability mode, cache state, concurrency, machine, and raw samples.
Historical Stage 4.6 evidence remains `INCOMPARABLE` and is not a CDC target or
winner baseline.

## 12. Selected, proposed, and open

| Item | Status | Consequence |
|---|---|---|
| Complete immutable Version without parent reconstruction | `SELECTED R0` | Any Chunk manifest must describe a complete workspace. |
| Zero-payload accepted-reference operations | `SELECTED R0` | Fork/checkpoint/rollback do not invoke CDC. |
| CDC for regular-file content | `PROPOSED` | Requires joint CAS+CDC architecture selection. |
| FastCDC-style gear hashing | `LEADING HYPOTHESIS` | Must be compared against credible alternatives and fixed by versioned vectors. |
| Exact ChunkerSpec and compatibility policy | `OPEN` | Phase 02/03 may decide only after architecture selection. |
| Trusted byte-range edit evidence | `OPEN` | Optimization only; absence must not block correct full scanning. |
| Backend-independent byte-stream interface | `CANDIDATE CONSTRAINT` | No durable or runtime filesystem feature may define boundaries. |
| Chunk full-byte occupied-ID comparison | `REQUIRED IF ADMITTED` | Collision mismatch fails closed. |

## 13. Proof and reopening boundary

Before the CAS+CDC candidate can be selected, the reopened Phase 01 package
must show that:

1. CDC and Chunk admission live within the chosen LayerStack-0 ownership and
   backend dependency direction;
2. every Version manifest plus Chunk closure is complete and crash-recoverable;
3. missing hints and failed resynchronization have a correct bounded fallback;
4. memory, Chunk size/count, window count, staging, concurrency, and cleanup
   populations have finite configured limits;
5. collision handling compares full bytes and fails closed;
6. Chunker evolution cannot reinterpret an accepted Version silently;
7. runtime-private facts never influence boundary or Version identity; and
8. recovery and reclamation cannot expose missing Chunks or delete custodied
   content.

Until that joint decision is recorded, this file is candidate evidence rather
than implementation authorization.

## Related diagrams

- [Workspace Versions and Chunk content-addressed storage](02-workspace-versions-and-chunk-cas.md)
- [Branches, Checkpoints, and rollback](03-branches-checkpoints-and-rollback.md)
- [Proposed backend abstraction and runtime isolation](04-ephcow-runtime-view.md)
- [Publication, OCC, and recovery](05-publication-occ-and-recovery.md)
- [Retention and reclamation](06-retention-and-reclamation.md)
- [Data movement and complexity](07-data-movement-and-complexity.md)
- [Storage diagram index](README.md)
