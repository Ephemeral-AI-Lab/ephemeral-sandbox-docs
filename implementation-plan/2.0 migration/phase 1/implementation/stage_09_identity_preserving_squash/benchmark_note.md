# Stage 09 benchmark note — identity-preserving squash

[Specification](spec.md) · [E2E plan](e2e_test.md) ·
[Overall Stage 03–11 scorecard](../stage_03_11_benchmark_note.md) ·
[Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

Status: **NOT_RUN**

Stage 09 owns the physical squash transaction and its boundedness. It is a POC
diagnostic stage: even a local pass cannot qualify the final latency, RSS, or
space gates owned by Stage 11.

| Required report field | Value frozen before the first candidate sample |
| --- | --- |
| frozen baseline | matched raw-v1 squash/remount control; revisions, corpus, host, cache, session count, and order fixed |
| required target/cap | exact identity/tree/policy/atomicity, bounded-resource and release rules, stage-owned complexity, and operation `≤60 s`; report the Prep remount/full-squash envelopes diagnostically |
| predeclared optimization target (recommended, non-normative) | frozen-remount median `≤raw` and full-squash median `≤raw×1.05+2 ms`; complete local bundle `≤100 s` |
| candidate actual | `NOT_RUN` |
| delta / ratio / headroom | `NOT_RUN`; derive only from preserved matched samples |

## Owned targets

| Area | Required local result |
| --- | --- |
| Identity | `RootId`, root-record bytes/digest, `PublicationId`, and publication/OCC generation are exactly unchanged; `MaterializationId` changes and materialization generation strictly increases |
| Correctness | Exact bytes, paths, supported metadata, reads, and exec behavior before/after remount and restart |
| Policy | Autosquash is enqueued at projected `D≥48`; compact or reject before `D>64`; routine benefit `≥8` carriers; a manual selected run contains at least 2 lowers and predicts lower depth; mount preflight checks both carrier count and the serialized OverlayFS `lowerdir=` byte limit; pack/locator pressure never triggers squash |
| Atomicity | One verified replacement target may overlap old leased sources; catalog CAS is atomic; old sources remain until lease/grace/recheck completion |
| Native hot path | Read, exec, file, PTY, and OverlayFS paths perform zero CDC/CAS/pack payload lookups |
| Complexity | Plan `O(D+A)`; build/verify `O(S+E_s)`; CAS `O(P)`; each live-remount frozen interval `O(D+tasks+verified FDs)` with no `U/R/K/S` work; all-session orchestration is the sum of bounded switches; recovery `O(A+P)` |
| Bounded resources | 4 workers, 256 KiB worker buffers, metadata queue 16 descriptors/64 KiB, encoder ≤256 KiB, shared cache ≤16 MiB, managed publication memory ≤4 MiB, storage semaphore ≤64 MiB |
| Local timing | Every operation/cell ≤60 s. Preserve raw samples and diagnostic median only; annotate the future remount `≤raw×1.05+2 ms` and full-squash `≤raw×1.10+5 ms` envelopes, but make no p95 claim before Stage 11 |

`D` is native carrier depth, `A` active sessions, `S` selected source bytes,
`E_s` selected entries, and `P` catalog/lease records.

## Concrete tiny evaluation matrix

The minimum counterbalanced schedule is `A,B,C,D,A`: one unscored global
warmup followed by five legacy-control/candidate-shadow pairs. The preferred
schedule repeats the coverage to ten pairs after 3–5 warmups only when the
whole developer loop still completes in 30–60 seconds. Policy cells E and F
are exact untimed calls and do not replace the five measured pairs.

| Cell | Frozen control and candidate | Warmups / measured | Raw metrics | Pass / fail |
| --- | --- | --- | --- | --- |
| A — normal squash | ~16 MiB mixed tree, `D=8`, 1 session, routine reduction 8; legacy control versus v2 squash | global 1 / 2 pairs in minimum schedule | phase times, identity/generations, depth, carriers, bytes, leases | exact identity/tree; new materialization generation; benefit 8 admitted |
| B — pre-trigger width | same corpus, `D=47`, 4 sessions, reduction 8 | global 1 / 1 pair | frozen interval, remount count, active/old/new leases, FDs | all 4 sessions switch atomically; no premature depth violation |
| C — trigger boundary | same corpus, `D=48`, 1 session, reduction 8 | global 1 / 1 pair | enqueue reason, plan counters, depth before/after | autosquash enqueued because projected `D≥48` |
| D — near cap/manual | same corpus, `D=63`, 4 sessions, manual selected run of exactly 2 lowers, replaced by one carrier | global 1 / 1 pair | admission, frozen work, exact carrier delta | two-lower manual run is accepted and lowers depth by 1; final depth ≤64 |
| E — insufficient/foreign pressure | `D=8`, routine benefit 7; manual selected run of exactly 1 lower; separately inject pack and locator pressure | 0 / 1 exact call per condition | decision enum and reason | no routine squash at benefit 7; one-lower manual request is rejected; pressure routes to Stage 08 maintenance |
| F — hard cap | synthetic policy states at projected `D=64` and `D=65` | 0 / 1 exact call each | admission/compact/reject decision | depth never becomes >64; projected 65 compacts first or rejects |
| G — release sentinel | one daemon; fixed publish, 4 sessions, squash/remount/destroy/grace | 3 / 20 cycles, plus equal-warmup control | 100 ms resource/RSS/space stream, first/last 5-cycle medians, slope, quiescence | logical owners release; unexplained bytes 0; no repeated growth outside frozen control noise |
| H — serialized lowerdir boundary | long absolute, colon-safe carrier paths with the same valid depth; serialized byte counts exactly `L_limit-1`, `L_limit`, and `L_limit+1` | 0 / 1 exact call per boundary | declared provider limit, actual serialized bytes, carrier count, preflight decision, mount syscall count | admit iff both `D≤64` and serialized bytes `≤L_limit`; over-limit compacts or returns `NeedCompaction` before any mount syscall or partial visibility |
| I — squash-build isolation | deterministic pending squash target; matched idle versus squash-builder-active command and PTY create/drain cells, with build kept outside the remount freeze | 3 warmups / frozen `N` before candidate data; minimum 5 interleaved pairs | command/PTY p50/p95 diagnostics, maintenance state, wait/lock/permit/CDC/CAS/manifest/pack route counters | exact command/PTY behavior; no squash-builder-owned wait, lock, permit, CDC/CAS/manifest/pack work enters either critical path; numeric qualification remains Stage 11 |

The deterministic corpus contains a localized edit, incompressible content, a
repeated object, 256 small files, and metadata-edge fixtures. Pre-generate it;
freeze seed, image, host allocation, filesystem, cache class, and operation
order. Each measured pair is:

```text
publish -> snapshot identities/generations -> create sessions/read/exec
-> squash -> exact oracle -> destroy -> quiesce
```

Poll quiescence every 100 ms for at most 5 s. A timeout, missing normative
source, leaked owner, or silent sample drop fails the cell.

### Required frozen-interval payload-independence sweep

Prebuild and verify replacement targets outside the timed freeze for selected
carrier sizes exactly **16 MiB, 64 MiB, and 256 MiB**. Hold `D=8`, four active
sessions, task schedule, verified-FD count, mount options, filesystem, and
cache class fixed. At each size run one excluded warmup and three measured
remount switches in counterbalanced size order.

Record lower descriptors visited, task transitions, verified-FD operations,
payload bytes read/hashed/copied, and frozen nanoseconds. The three structural
counter tuples must be identical for the fixed schedule, and frozen payload
read/hash/copy bytes must each be exactly zero. Elapsed time is retained as a
diagnostic; work growing with `S`, any payload operation inside the freeze, or
a missing counter is `FAIL`/`OPEN`. This is the Stage 09 structural proof of
`O(D+tasks+verified FDs)` and `S` independence; Stage 11 still owns the paired
p50/p95 remount gate.

### Planning wall-clock budget — ESTIMATED, not measured

| Work | Core tiny loop | 20-cycle sentinel | Full local bundle |
| --- | ---: | ---: | ---: |
| fixture/config/setup | 4–7 s | 4–7 s | 8–14 s |
| warmups | 5–10 s | 3–6 s | 8–16 s |
| measured cells/cycles | 15–30 s | 20–40 s | 35–70 s |
| quiescence/cleanup | 3–7 s | 5–13 s | 8–20 s |
| artifact/report write | 3–6 s | 3–6 s | 6–12 s |
| separate fixed-`D` 16/64/256 MiB frozen-size sweep | — | — | 12–24 s |
| serialized-lowerdir boundary + squash-builder isolation | — | — | 10–25 s |
| **Total** | **30–60 s** | **35–72 s** | **87–181 s** |

These are healthy-run scheduling estimates, not relaxed limits. Every
operation/cell remains ≤60 s and any final matched invocation remains ≤5 min.

## Raw evidence and arrival checkpoint

Keep every sample, including failures and exclusions. Record:

- plan/build/verify/fsync/CAS/frozen-remount/evacuation/end-to-end
  nanoseconds. Evacuation starts when the last old-carrier lease is released
  and relocation of its final live locator can begin, and ends when replacement
  locators are durable and the source is eligible for grace; record `0` with a
  closed reason when no evacuation is required;
- all IDs, generations, exact oracle digests, route counters, and decision
  reasons;
- logical and allocated source/target/grace, metadata, object, pack, staging,
  trash, quarantine, and unexplained bytes;
- bytes read/written, depth/carriers, sessions/remounts, leases, mappings/FDs,
  workers/tasks/queues/permits/cache, quiescence latency, and RSS source/scope;
- frozen lower-descriptor, task-transition, verified-FD, and payload
  read/hash/copy counters for every fixed-`D` size point;
- declared serialized-`lowerdir` limit, actual option bytes, depth, preflight
  result, and mount-syscall count for `L_limit-1/L_limit/L_limit+1`;
- idle-versus-squash-build command/PTY samples and maintenance-owned
  wait/lock/permit/CDC/CAS/manifest/pack critical-path counters;
- product/test/docs revisions and dirty state, binary/config digests, host,
  image/platform, filesystem/mount, corpus/seed/order/cache, and
  `measured|derived|estimated|unknown` provenance.

Stage 09 has not arrived until
`.benchmark-state/results/<run-id>/stage-09-perf-report.json` and
`stage-09-perf-report.md` exist with
`schema_version="phase1.stage09.perf-report.v1"` and contain the frozen
baseline actual, required pass target/cap, separately predeclared optimization
target, candidate actual, delta/ratio/headroom, complexity and work counters,
memory/RSS, complete physical-space terms, links between the reports and to
run/raw artifacts, provenance, and verdict. Allowed terminal verdicts are
`DIAGNOSTIC_PASS` or `FAIL`; never `QUALIFIED`.

The first Markdown table must show the frozen baseline actual, required pass
target/cap, separately predeclared optimization target, candidate actual,
delta/ratio, headroom, and verdict for every stage-owned metric.

## Append-only progress

Before each live command, append intent, exact command, expected evidence,
ownership, and cleanup to
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/e2e/test-report.md`.
Afterward append `Good` or `Defect`, artifact IDs, misses, and cleanup; append
later `Fix` and `Rerun` entries rather than rewriting history. Then update the
overall scorecard and append a row here.

| UTC | State | Run ID | Baseline → candidate actual | Required / optimization target | Delta / ratio / headroom | Report / raw artifacts | Cleanup / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | NOT_RUN | — | — | — | — | — | Freeze the first cell before execution |
