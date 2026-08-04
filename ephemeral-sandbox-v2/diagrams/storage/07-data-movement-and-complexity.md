# Data movement and complexity

> Status boundary: zero-payload reference transitions over accepted complete
> Versions are **SELECTED R0**. Cross-Version CAS+CDC reuse plus the
> backend-agnostic durable/runtime contracts are **PROPOSED**. No benchmark
> result in this document selects or amends the architecture.

This document makes byte movement explicit. It separates the operation's
reference metadata from workspace payload, runtime materialization, and live
upperdir writes so that “zero-copy” has one testable meaning.

Authoritative context:

- [V2 product hard rules](../../PRD.md)
- [Selected architecture](../../architecture_design.md)
- [Normative terminology](../../branding/terminology.md)
- [Phase 01 performance protocol](../../phases/01-choose-design/test-perf.md)

## Byte classes

```text
R = reference bytes
    Head, HeadRevision, typed Root, AcceptedBinding

M = description bytes
    selected: canonical complete-Version identity representation
    proposed: complete workspace manifest

P = immutable payload bytes
    selected: one complete payload closure
    proposed: immutable chunks transitively named by a manifest

B = runtime WorkspaceBase bytes
    bytes read or written to prepare a runtime-readable immutable base

U = live writable bytes
    upperdir writes, workdir metadata, process output
```

The hard zero-payload condition measures `P`, not all machine activity. A
reference transition may read and write bounded `R`; runtime activation or
materialization may separately touch `B`; a running agent may write `U`.

## The selected fast path

Forking from, checkpointing, rolling back to, or moving to an already accepted
Version is a reference operation. Its payload path is structurally absent.

```text
caller
  |
  | expected Head + AcceptedBinding
  v
+--------------------------+
| reference transition API |
|                          |
| read/write bounded R     |
| never open payload       |
+-------------+------------+
              |
              v
      OCC Head replacement

P bytes read    = 0
P bytes written = 0
P bytes copied  = 0
```

“Checkpoint” needs one qualification:

```text
checkpoint accepted V1              capture new live workspace as V2
----------------------              --------------------------------
add typed Root -> V1                scan/canonicalize candidate
P read/write/copy = 0               admit complete immutable V2
                                    then add Root -> V2
                                    payload I/O is required for admission
```

EphCoW's selected innovation is reference-level copy-on-write: many isolated
agent workspaces begin from the same immutable accepted Version; only their
live upperdirs diverge. It does not currently claim chunk-level CoW between
different accepted Versions.

## Selected publish path

Publishing a genuinely new Version is not a zero-payload operation. Candidate
bytes must be validated, canonicalized, compared on occupied identity, and
made durably immutable before the one Head OCC transition.

```text
live workspace candidate
          |
          | read candidate bytes
          v
canonical identity + validation
          |
          v
stage complete immutable payload closure
          |
          | occupied VersionId?
          +---------- yes ----------> full canonical-byte comparison
          |                              | equal       | mismatch
          |                              v             v
          |                           reuse exact    collision error
          |                           payload
          v
make accepted payload durable
          |
          v
one conditional OCC Head transition
          |
          +---- stale ----> Head unchanged; accepted orphan is cleanup debt
```

Phase 03 may optimize how bytes flow through staging, but it cannot report
admission as a zero-payload reference operation or mutate a committed payload.

## Proposed CAS plus CDC publish path

The following data flow demonstrates the proposed cross-Version optimization.
It is **not selected R0**.

```text
PROPOSED ONLY

complete workspace folder
          |
          v
walk paths in canonical order
          |
          +---- unchanged file metadata/content ----> reuse prior chunk IDs
          |
          v
changed regular file bytes
          |
          v
content-defined chunking (CDC)
          |
          v
hash chunk -> verify occupied digest by full bytes
          |
          +---- exact chunk exists ----> write 0 new chunk bytes
          |
          +---- new chunk ------------> durable immutable chunk write
          |
          v
build complete workspace manifest
          |
          v
durably publish manifest, then conditional OCC Branch/Head transition
```

The manifest must describe the full workspace, even though its chunks can be
shared. A directory delta or a chain of partial manifests would violate the
complete-Version requirement by making reconstruction depth part of truth.

This proposal can reduce bytes written for localized edits, but it also adds
manifest/chunk atomicity, transitive reachability, graph recovery, and shared
chunk retirement. Those costs require a reopened Phase 01 decision.

## Backend-neutral runtime activation boundary

Reference reuse and runtime usability are separate. Moving a Head to an
accepted Version can be zero-payload even when later opening a live Workspace
has nonzero cost.

```text
accepted Version reference
          |
          | zero-payload Head/Root operation ends here
          v
Workspace activation request
          |
          v
backend-neutral Workspace adapter
          |
          +---- ordinary-I/O profile ----> materialize immutable WorkspaceBase
          |
          +---- current Linux profile ----> WorkspaceBase as lowerdir
          |                                 + private upperdir/workdir
          |
          v
agent namespace and exec
```

The correctness-first ordinary-I/O profile may read and write the complete
Version during cold materialization. A warm validated base may avoid that work.
Neither result changes the `0/0/0` reference path. The candidate does not
require a custom filesystem or storage-specific clone feature; optional
acceleration must remain behind the same conformance contract.

## Operation matrix

Symbols: `O(1)` means independent of workspace payload size, not literally one
CPU instruction. `N` is complete candidate payload bytes, `C` changed bytes
read by the proposal, `K` new unique chunk bytes, `L` number of exact live
references/custody entries, and `G` manifest/chunk graph edges.

| Operation | Selected R0 payload movement | Complexity target | Status / qualification |
|---|---:|---:|---|
| Create Branch binding at accepted Version | `P read=0, write=0, copy=0` | `O(1)` reference metadata | **SELECTED**; runtime workspace preparation is separate |
| Add Checkpoint Root to accepted Version | `P read=0, write=0, copy=0` | `O(1)` reference metadata | **SELECTED** |
| Roll back Head to accepted Version | `P read=0, write=0, copy=0` | `O(1)` reference metadata plus OCC serialization | **SELECTED** |
| Same-Version Head move/no-op | `P read=0, write=0, copy=0` | `O(1)` reference metadata | **SELECTED** |
| Capture and publish new workspace Version | candidate/payload I/O allowed and expected | `O(N)` worst-case scan/admission | **SELECTED family**; exact implementation is Phase 03 work |
| Occupied complete-Version identity | full canonical bytes compared | `O(N)` worst case | **SELECTED correctness rule**; digest alone is insufficient |
| Read/materialize immutable Version | outside reference-only claim | payload/view dependent | **SELECTED boundary**; mechanism-specific cost remains to prove |
| Retire complete payload closure | no live payload reader; metadata scan plus unlink | bounded `O(L)` exact revalidation plus filesystem work | **SELECTED family** |
| CDC publish of localized edit | proposed reads approximately `C`, writes `K` plus manifest | best case proportional to changed/rechunked region; worst case `O(N)` | **PROPOSED**; no guarantee |
| Reclaim shared chunks | graph traversal and deletion | at least bounded work over relevant `G` | **PROPOSED**; architecture not selected |
| Cold ordinary-I/O WorkspaceBase materialization | reads/writes up to complete accepted payload | `O(N + entries + chunks)` | **PROPOSED PROFILE**; separate from reference COW |
| Warm Workspace activation | validated-base and adapter dependent | bounded by selected cache/adapter profile | **PROPOSED PROFILE**; must fall back correctly if cache is absent |

## Before and after byte movement

The useful comparison is by operation and byte class, not a universal “faster
than filesystem X” claim.

```text
accepted-Version fork / rollback

legacy layer-history intuition          selected LayerStack-0 / EphCoW
------------------------------          -----------------------------
inspect/reconstruct ancestry?           update bounded reference R
possibly copy/squash payload?            payload P is never opened
cost may follow history depth            cost independent of payload size

new-Version publish

selected complete payload               proposed CAS+CDC extension
-------------------------               --------------------------
scan/admit complete candidate            full logical manifest
store complete closure                   CDC changed file content
exact same-Version reuse only            reuse exact chunks across Versions
simple closure retirement                graph reachability/reclamation
```

The right-hand publish proposal trades lower expected write amplification on
localized changes for more metadata, random I/O, CPU hashing/chunking,
recovery states, cache behavior, and reclamation work. Workload measurements,
not the word “CAS,” determine whether that trade wins.

## Complexity and space model

### Selected R0

```text
reference operation time     O(1) in payload size, plus bounded serialization
reference operation space    O(1) reference record
new Version admission time   O(N) worst case
new Version stored space     up to O(N), except exact accepted-Version reuse
retirement decision          bounded exact scan of Heads/Roots/custody
history reconstruction       none; every accepted Version is complete
```

### Proposed CAS plus CDC

```text
reference operation time     O(1) in payload size
changed publish time         best case O(C), worst case O(N)
new unique payload space     O(K), plus complete manifest and indexes
Version stream/read time     O(chunks accessed) plus backend operation costs
ordinary materialization    O(N + entries + chunks)
reclamation                  bounded graph/reverse-index work over G
metadata space               manifests + chunk IDs + recovery/lease records
```

`C` can approach `N`: inserting bytes can shift content-defined boundaries,
metadata changes can force rescans, and a workload can replace every file.
CDC therefore provides an optimization opportunity, not a new asymptotic
correctness guarantee.

## Counters and benchmark contract

The selected hard rule needs byte counters at the reference API boundary:

```text
selected required counters
  reference_payload_bytes_read
  reference_payload_bytes_written
  reference_payload_bytes_copied

required value for Head create/replace/remove and fixed-Root create/remove
  0 / 0 / 0
```

Additional counters help explain, but cannot redefine, that proof:

```text
candidate_bytes_scanned
payload_bytes_staged
payload_bytes_deduplicated_at_complete_state_boundary
view_bytes_read_or_materialized
upperdir_bytes_written
staging_bytes_current / peak
orphan_bytes_current / peak
retirement_debt_bytes_current / peak

PROPOSED CAS+CDC counters
  cdc_bytes_scanned
  chunk_bytes_reused
  chunk_bytes_written
  manifest_bytes_written
  chunk_collision_full_compare_bytes
  chunk_reclamation_edges_scanned
```

Measure at least empty, metadata-heavy, many-small-file, large-file, localized
edit, rename, and whole-tree replacement workloads. Report cold and warm view
costs separately, concurrency, filesystem, cache state, durability mode, and
percentiles. Never fold materialization or upperdir writes into the reference
counter, and never hide them when reporting end-to-end latency.

Historical Stage 4.6 measurements are `INCOMPARABLE`: they used legacy
semantics and cannot establish a V2 baseline, winner, regression budget, or
guarantee. The CAS+CDC proposal needs its own like-for-like evidence after its
architecture is explicitly selected; platform-specific acceleration is never
the correctness baseline.

## Optimization order

Correctness gates optimization:

```text
1. complete immutable Version and canonical identity
2. full-byte occupied-ID comparison
3. payload durability before one conditional OCC Head transition
4. structural 0/0/0 reference path
5. bounded read custody, recovery, retirement, and cleanup
6. only then: reduce scan, write, materialization, and reclamation costs
```

An optimization is invalid if it introduces layer-depth reconstruction,
silently merges stale work, puts runtime-private facts in portable identity,
edits accepted bytes, or creates an unbounded resource path.

## Proof and reopening boundary

Phase 03 owns executable proof of the selected reference counters, collision
comparison, OCC linearization, crash prefixes, custody, and bounded cleanup.
Phase 06 owns offline integration and performance qualification. Neither phase
may turn historical Stage 4.6 numbers into a V2 promise.

Reopen Phase 01 before treating Chunk-level CDC reuse, a manifest/object DAG,
or the backend-neutral durable/runtime contracts as selected. The reopened
decision must choose that storage family jointly with its owner, recovery
model, retirement model, resource limits, and Workspace-adapter boundary.

See [CDC boundaries, resynchronization, and reuse](08-cdc-boundaries-resynchronization-and-reuse.md)
for the detailed `C`, `K`, and worst-case `N` path.
