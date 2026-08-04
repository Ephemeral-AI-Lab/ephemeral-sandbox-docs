# MPLA proof-of-concept benchmark report

| Report metadata | Value |
|---|---|
| Evidence sealed | 2026-08-01 |
| Report assembled | 2026-08-01 |
| Platform | Linux/arm64 guest on macOS Docker Desktop, fixed at 4 vCPU and 4 GiB |

```text
POC_CORRECTNESS_PASS
POC_100X_NOT_SUPPORTED
POC_500X_NOT_SUPPORTED
AG_SQUASH_PASS
AG_STREAM_PASS
```

## Executive summary

The Merkle-Promoted Locator Architecture (MPLA) POC passed its correctness,
integrity, isolation, recovery, squash, and streaming acceptance gates. It also
made the genuine first-time construction of the sealed 8-GiB publication
fixture cache 108.81x faster on the measured outer cache-command path: from
133.683 s to 1.228642917 s. The complete cold launcher process took 3.99 s,
including 2.198345375 s of separately identified Docker setup, so the cold
builder met the less-than-5.0-second acceptance target without reclassifying a
warm attachment as a cold build.

Normal read-only attachment remained a separate fast path. Its measured cache
attachment service time was 24.825208 ms, complete in-service preparation was
374.467417 ms, and no fixture payload bytes were copied. Earlier warm repeats
measured 19.368500-23.010084 ms service and 490.085667-529.899292 ms complete
preparation.

Four of the five conjunctive aggregate Booster gates exceeded 100x against
their matched controls:

- exact activation: 628.12x;
- same-generation activation: 534.65x;
- fork: 1,722.79x;
- rollback: 798.08x.

Small publication passed correctness and its absolute 100 ms ceiling, but its
matched ratio was only 0.6269x: the 58.136209 ms candidate median was about
1.60x slower than the 36.444000 ms control median. Because the aggregate rule
is a conjunction, not an average, the POC does not support an aggregate 100x or
500x claim. The defensible result is therefore: correctness passed; several
core metadata operations achieved large, independently measured speedups; the
aggregate multiplier claim remains blocked by publication.

## Algorithm under test

MPLA separates durable logical identity from physical placement. A generation
is named by its Merkle `RootId` and `AttributionRootId`; mutable allocation
paths, mount points, and storage locations are kept out of those content IDs.
Publication then promotes a durable locator and ownership receipt instead of
copying the payload into a newly named physical tree.

```text
                 immutable logical identity
             RootId + AttributionRootId
                         |
                         v
              canonical object records
                         |
                         v
            durable locator / owner receipt
                         |
        +----------------+----------------+
        |                                 |
        v                                 v
  stable allocation                 final generation ref
  (payload stays put)               (replaced last)
        |                                 |
        +---------------+-----------------+
                        v
              read-only activation view

  publish: quiesce -> strict unmount -> adopt upper -> write durable
           objects/locator/owner receipt -> replace final ref -> retire lease

  fork:     metadata lineage update; no inactive payload copy
  rollback: select prior Merkle root + exact activation
  squash:   select a ready exact generation; physical flattening is separate
```

The intended complexity bounds are scoped, not universal:

- exact activation is O(1) in payload bytes and file count because it does not
  eagerly copy lower layers;
- fork is O(log R) metadata work with zero inactive-payload copying;
- rollback is O(log R) metadata selection plus exact activation;
- a valid pre-seal checkpoint finalization is
  O(delta-payload x Merkle-depth + changed-metadata), while a general
  incremental checkpoint still includes its required scan term;
- logical squash is metadata-only selection of an already ready exact
  generation. It does not pretend that physical flattening is free.

The publication linearization point is the last durable replacement of the
final generation reference. Canonical objects, locators, and ownership receipts
must already be durable when that replacement occurs.

## Scope and benchmark method

The campaign followed the current [test matrix](test_matrix.md),
[phase specification](mpla_booster_poc_phase_spec.md), and
[execution record](booster_scorecard_execution_spec.md), subject to the
[POC requirements and prohibitions](../requirements_and_prohibitions.md). It
used independent phase limits. There is no 480 s or 600 s aggregate campaign
cap, no budget carryover, and no borrowing between phases.

F0 is the one-time or recovery fixture-cache construction qualifier. P0 is the
normal warm read-only attachment qualifier. Neither casts an aggregate
multiplier vote. P1-P4 contain the five conjunctive multiplier gates. P5 and P6
are independent absolute gates. P7 validates interruption and recovery safety,
and P8 seals the evidence set and terminal decision.

For multiplier gates, the reported formula is:

```text
median ratio = median(matched control elapsed time)
             / median(candidate elapsed time)
```

Each scored timing set reports its raw observations, median, and maximum. With
only three matched samples in most gates, this report does not call the maximum
a p95. Required gates combine timing, exact semantic/oracle checks, durability,
resource conformance, and zero-copy or allocation proof as specified.

## Fixture and environment

| Property | Measured or sealed value |
|---|---:|
| R0 fixture | `console-release` |
| R0 logical bytes | 912,350,100 B (870.084858 MiB) |
| R0 files / directories | 3,602 / 694 |
| S4 cache format | `s4-chain-sparse-v1` |
| S4 logical size | 8,589,934,592 B (8 GiB) |
| S4 logical allocations | exactly 8 |
| S4 allocated payload bytes | 0 B |
| Cache-build payload bytes read / copied | 0 B / 0 B |
| Qualified branch depths | 1 / 5 / 8 |
| Host cache budget | less than 10 GiB |
| Guest platform | Linux/arm64 |
| Image | `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` |
| Gateway | `127.0.0.1:7903` |
| Storage | persistent ext4 with real OverlayFS; no tmpfs |
| Docker Desktop allocation | 4 vCPU / 4 GiB |
| Workload `memory.high` / `memory.max` | 96 MiB / 128 MiB |
| Application pool budget | at most 8 MiB |
| Receipt clock label | `CLOCK_MONOTONIC` |

The authorized storage process used the observed
`mpla-storage-admin-overlayfs-dac-override-qualification-v1` profile and the
required `mpla-storage-admin-v1` contract, with CAP_SYS_ADMIN present only in
the authorized process. Ordinary workload mount attempts and capability use
were denied. Wrong namespace and wrong profile selections also failed closed.

## Historical baseline and cold-cache redesign

The V13 cold-cache baseline took 133.683 s wall time and 129.932 s service time.
It constructed eight dense lifecycle publications, writing, syncing, and
hashing each layer, then repeatedly walked the accumulated semantic and oracle
trees. The result was approximately 48 GiB of cumulative scans plus roughly
9 GiB of explicit payload hashing to describe an 8-GiB logical fixture.

The permanent F0 design constructs eight exact, hole-only,
content-addressed sparse allocations. It performs bounded receipt validation
per allocation, then one final inventory, extent, and manifest validation and
one filesystem sync. This removes repeated dense layer construction, repeated
tree walks, per-layer syncs, and unnecessary payload hashing while retaining
the exact sealed identity and recovery contract.

| Cold-build component | Final measurement |
|---|---:|
| Builder service | 1.102406542 s |
| Cache-command outer path | 1.228642917 s |
| Orchestration overhead | 0.126236375 s |
| Docker setup, measured separately | 2.198345375 s |
| Staging | 0.043895500 s |
| Launcher through pre-cleanup | 3.471067 s |
| Complete cold process | 3.99 s |
| Outer improvement over 133.683 s | 108.805412989x |
| Service improvement over 129.932 s | 117.862145270x |

F0 passed both its less-than-5.0-second cold-build acceptance target and its
independent 30 s phase cap. The 2.198 s Docker setup is platform orchestration
overhead, not hidden payload work, and is shown separately rather than removed
from the complete-process result.

For historical context only, the
[original R0 measurements](../baseline-experiment/README.md) were
107.024411507 s for candidate publication/CDC/CAS ingestion, 9.987675338 s for
cold complete materialization, 6.361909169 s for the same-key explicit
materializer, and 0.035375 ms for the ordinary warm generation lookup median.
These values are not substituted for the matched denominators defined by the
current scorecard.

## Phase results

| Phase | Purpose | Wall time | Independent cap | Result |
|---|---|---:|---:|---|
| F0 | Genuine first/recovery 8-GiB cache construction | 1.228642917 s outer; 3.99 s complete | 30 s | PASS |
| P0 | Warm cache attachment/materialization qualification | 2.120485208 s phase | 60 s | PASS |
| P1 | Exact and same-generation activation | 85.129972292 s | 120 s | PASS |
| P2 | Fork and rollout-node scaling at 1/64/1000 | 52.723843000 s | 60 s | PASS |
| P3 | Rollback | 51.757623833 s | 60 s | PASS |
| P4 | Small publication | 22.881794000 s | 70 s | FAIL: matched ratio only |
| P5 | Logical squash | 29.591311167 s | 60 s | PASS |
| P6 | 1-GiB durable stream | 8.363238417 s | 40 s | PASS |
| P7 | Crash/recovery matrix | 21.349401583 s | 120 s | PASS |
| P8 | Artifact verification and terminal decision | 0.396731209 s receipt; 0.57 s process | 30 s | PASS |

P0's phase wall includes qualification orchestration. The normal consumer fast
path itself measured 24.825208 ms attachment service and 374.467417 ms complete
in-service preparation, with zero payload bytes copied. It therefore met the
separate less-than-50 ms service and less-than-1 s preparation targets.

### Aggregate multiplier gates

| Gate | Candidate raw times (ms) | Candidate median / max (ms) | Control raw times (ms) | Control median (ms) | Ratio | Required result |
|---|---|---:|---|---:|---:|---|
| Exact activation | 21.155500, 18.431042, 21.375375, 53.056750, 55.029542 | 21.375375 / 55.029542 | 13,925.473340, 13,426.207298, 13,034.438715 | 13,426.207298 | 628.115637644x | PASS |
| Same-generation activation | 21.155500, 18.431042, 21.375375 | 21.155500 / 21.375375 | 11,649.543256, 11,310.809838, 10,810.835838 | 11,310.809838 | 534.651028716x | PASS |
| Fork | 9.468417, 7.706708, 5.857166 | 7.706708 / 9.468417 | 13,277.046215, 13,353.248090, 13,023.158923 | 13,277.046215 | 1,722.790874521x | PASS |
| Rollback | 18.476208, 16.368959, 16.487709 | 16.487709 / 18.476208 | 13,158.580589, 13,313.166131, 12,943.071590 | 13,158.580589 | 798.084232867x | PASS |
| Small publication, matched first three | 58.136209, 57.915167, 62.567625 | 58.136209 / 62.567625 | 36.678333, 36.444000, 36.051083 | 36.444000 | 0.626872660x | FAIL |

The publication candidate had two additional depth observations, 63.389209 ms
and 65.937250 ms. Across all five samples its median was 62.567625 ms and its
maximum was 65.937250 ms, so every sample passed the required absolute ceiling
of 100 ms. It still failed the required matched ratio of at least 100x. The
preferred ceilings also did not pass: exact activation was not always at most
19.975350676 ms, same-generation activation was not always at most 20 ms, fork
was not at most 2 ms, rollback was not at most 10 ms, and publication was not at
most 20 ms.

The matched candidate and control rows used the same logical fixture and
operation intent, required the same logical availability and durability at the
timing boundary, used independently allocated storage, and passed their exact
oracle and cleanup checks. No historical R0 number was used as a replacement
denominator.

### Squash, stream, and recovery

P5 logical squash recorded outer times of 9.196250, 6.504750, and 6.170000 ms
(median 6.504750 ms; maximum 9.196250 ms) and service times of 0.854958,
0.463042, and 0.831042 ms (median 0.831042 ms; maximum 0.854958 ms). It passed
the required 10 ms outer and 1 ms service ceilings. Identity and attribution
stayed stable, public outcomes were exact, and reference progression matched
the oracle. This is an absolute gate, not a multiplier vote.

P6 durably streamed exactly 1,073,741,824 B in 994.910334 ms, including its
checksum inside the timed boundary. Floor throughput was 1,079,234,768 B/s,
or 1.005115703 GiB/s. It passed the required 1 GiB/s floor narrowly and did not
meet the preferred 5 GiB/s target. The 994.910334 ms comprised 514.471042 ms of
semantic build and 480.439292 ms of storage-stable callback work. Durability,
the exact oracle, zero immutable-payload reads, and no second payload allocation
all passed.

P7 passed all 46 registered interruption and recovery points. It performed one
semantic build followed by 45 identical-input reuses, exercised real SIGKILL,
verified old-or-complete-new visibility and same-ID replay, and found no
residue. Its internal campaign took 15.867793590 s, the registered sweep took
14.438988090 s, and the complete phase took 21.349401583 s.

## CLI and polling overhead

The evidence includes the following supported-CLI command-ledger counts. A
ledger entry is one recorded CLI round trip; poll and scorecard-read counts are
shown so orchestration is not confused with operation service time. F0 used a
dedicated construction receipt rather than this command-ledger format.

| Phase | CLI ledger entries | Coordinator polls | Scorecard reads |
|---|---:|---:|---:|
| P0 | 28 | 2 | 14 |
| P1 | 38 | 20 | 6 |
| P2 | 45 | 16 | 17 |
| P3 | 33 | 16 | 5 |
| P4 | 90 | 10 | 61 |
| P5 | 20 | 5 | 4 |
| P6 | 29 | 3 | 15 |
| P7 | 56 | 4 | 41 |
| P8 | 4 | 0 | 0 |

## Correctness, integrity, and isolation proof

The performance results were accepted only with the following properties:

- Candidate activation, fork, rollback, publication, squash, stream, and
  recovery outcomes matched their exact semantic oracles.
- Candidate metadata operations did not copy inactive immutable payload.
  Publication recorded zero immutable-payload reads and no second payload
  allocation; stream recorded the same conditions over exactly 1 GiB.
- The S4 fixture remained exactly eight logical allocations and 8 GiB at branch
  depths 1, 5, and 8 while consuming zero allocated payload bytes.
- Normal consumers attach the sealed cache read-only. They cannot select the
  builder path, mutate the cache, or invoke recovery.
- Cold recovery is fail closed: corrupt, partial, stale, and unknown sealed
  states are rejected. Only exact known unsealed roots are eligible for bounded
  recovery.
- The final reference is replaced only after canonical objects, locator,
  ownership receipt, and required durability checks have completed.
- Authorized storage capability is isolated from ordinary workloads. Wrong
  profile and wrong namespace choices fail closed.
- All workload resource checks passed, with no OOM event. Final manager and
  observability inventories were empty and staging paths were removed.

The largest recorded cgroup memory peak was 102,543,360 B during activation,
below the 128 MiB `memory.max`. The largest recorded process RSS was
36,687,872 B during squash. These are distinct measurements; neither is
misreported as the at-most-8-MiB application-pool accounting metric.

## Evidence seal and reproducibility

P8 sealed a 14-entry manifest. Its SHA-256 is:

```text
837578247484c38c95285b12c0e7710b66546e643c3132f3368aa3c87891638f
```

All 14 entries were independently rehashed, and
`manifest-verification.json` records `verified: true`. The source identity was:

```text
commit:                 99290631750430cf267b5c9329f2ac5d281def05
tree:                   ae1eac3747de54de749bd3290c7555f4988be8aa
tracked diff SHA-256:   390906e0a19da1389c2695b8ac1a15e16e88405c803ee56735177b1844190c85
porcelain SHA-256:      08b26860499fe3533e0e281c6229c292e1a891d90bfa7663c7da3fc5bdf659ef
configuration:          config/mpla-poc-m3-phase-profile-sparse-v1.yml
```

Sealed evidence roots:

```text
F0  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final43-f0-v3-20260731t072650z
P0  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final34-p0-20260731t014411z
P1  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final34b-p1-20260731t014941z
P2  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final34-p2-20260731t015423z
P3  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final40-p3-20260731t045422z
P4  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z
P5  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final54-p5-20260731t111116z
P6  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final61-p6-20260731t132300z
P7  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final70-p7-20260801t082954z
P8  /Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final73-p8-20260801t085647z
```

## Limitations and next improvements

1. **Publication is the aggregate blocker.** The candidate is already below
   the 100 ms absolute ceiling, but it must eliminate enough locator,
   durability, mount/unmount, receipt, or orchestration work to beat a 36.444 ms
   matched control by at least 100x. The current data does not justify that
   claim.
2. **Rollout coverage is logical, not a production traffic cutover.** P2 proves
   fork and rollout-node behavior at 1, 64, and 1,000 nodes. The selected
   profile still records `rollout_mode: legacy`, so a production rollout or
   traffic-switch benchmark must be specified and sealed separately before
   making a production-cutover performance claim.
3. **Clock labeling differs from the specification wording.** The
   sealed phase receipts label their clock `CLOCK_MONOTONIC`, not
   `CLOCK_MONOTONIC_RAW`. P8 accepted the internally consistent sealed
   nanosecond boundaries, but future cross-host comparison campaigns should
   use and record the requested raw clock explicitly.
4. **Some historical raw-result schemas have indirect binding.** P2 fork, P3
   rollback, P5 squash, and P7 recovery have explicit raw phase/runner binding.
   P0 qualification, P1 activation, P4 publication, and P6 stream are narrowed
   by result kind plus their sealed phase and runner receipts because their
   historical raw-result schema omitted the complete explicit pair. This is a
   provenance limitation, not a retroactive upgrade of those raw files.
5. **Docker Desktop contributes visible cold overhead.** The measured 2.198 s
   setup component is already compatible with the less-than-5 s complete cold
   target, but native Linux measurement would distinguish the algorithmic floor
   from desktop virtualization and daemon orchestration more cleanly.

The next optimization priority is therefore P4 publication, followed by a
native-Linux confirmation run using an explicitly recorded
`CLOCK_MONOTONIC_RAW` boundary and a separately specified production rollout
cutover benchmark. F0, P0, P1, P2, and P3 should use their sealed fast-path
evidence rather than being rerun merely to revisit already passed phases.

## Conclusion

The POC demonstrates that content-addressed identity, stationary allocation
adoption, read-only zero-copy activation, metadata-only fork/rollback/squash,
bounded crash recovery, and a sparse sealed 8-GiB fixture can coexist with
strong fail-closed behavior. The cold-cache defect was removed with a genuine
108.81x outer-path improvement, normal warm attachment remained a tens-of-
milliseconds service operation, and four multiplier gates exceeded 100x.

It does not yet demonstrate an aggregate 100x MPLA Booster because the small
publication ratio failed. That distinction is the main result of the benchmark:
the architecture and its correctness proof are viable, the cold construction
algorithm is fixed, and publication is now the precise measured optimization
frontier.
