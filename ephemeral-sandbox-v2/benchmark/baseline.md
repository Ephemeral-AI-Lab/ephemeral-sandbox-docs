# Historical Stage 04.6 benchmark baseline

```text
DOCUMENT_ROLE: HISTORICAL_EVIDENCE_SUMMARY
ARCHITECTURE_UNDER_TEST: HISTORICAL_MPLA_POC
V2_ARCHITECTURE_AUTHORITY: NONE
EVIDENCE_LABEL: INCOMPARABLE
HISTORICAL_CORRECTNESS_RESULT: PASS
HISTORICAL_POC_100X: NOT_SUPPORTED
HISTORICAL_POC_500X: NOT_SUPPORTED
STAGE_4_6_COMPARISON: INCOMPARABLE
V2_OPTIMIZATION_TARGET: OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED
V2_FINAL_PERFORMANCE_VERDICT: TARGET_UNSELECTED
V2_ACCEPTANCE_EFFECT: NONE
```

This document summarizes reported observations from the historical Stage 04.6
MPLA Booster proof of concept. It is evidence about that campaign, not authority
for Ephemeral Sandbox V2. It does not qualify the selected R0 architecture, set
or satisfy a V2 optimization target, provide a V2 comparator, or transfer
MPLA's `RootId`, locator, or final-generation-reference model into V2.

V2 authority remains the accepted
`Candidate -> VersionId -> AcceptedVersion -> AcceptedBinding -> Head/fixed Root`
lifecycle, with one LayerStack-0 reference authority and one Head OCC point.

## 1. Sources and precedence

| Source | Role |
|---|---|
| [Phase 00 evidence policy](../phases/00-freeze-rules/SPEC.md#8-baseline-and-performance-policy) | Binding V2 disposition: `R_stage46 = INCOMPARABLE`; Stage 04.6 cannot pass or fail V2. |
| [Pinned Stage 04.6 evidence review](../../implementation-plan/new_2.0_migration_implementation_plan/evidence/stage-04-6-baseline.md) | Later integrity and provenance analysis; identifies the missing causal source closure and legal reuse. |
| [Historical POC benchmark report](<../../implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/mpla_poc_benchmark_report.md>) | Original report of fixtures, measurements, correctness results, and terminal campaign decision. |
| [Historical phase specification](<../../implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/mpla_booster_poc_phase_spec.md>) | Historical scoring rules; has no V2 product authority. |
| [Historical test matrix](<../../implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/test_matrix.md>) | Historical operation cases and sample expectations. |

Where the original report's terminal source presentation could imply a
campaign-wide reproducibility seal, the later pinned evidence review controls
this V2 summary: phase-specific receipts exist, but the exact dirty and
untracked source bytes and full transitive execution closure were not archived.

## 2. Historical terminal result

The campaign reported:

```text
POC_CORRECTNESS_PASS
POC_100X_NOT_SUPPORTED
POC_500X_NOT_SUPPORTED
AG_SQUASH_PASS
AG_STREAM_PASS
```

Four historical multiplier rows exceeded `100x`. Small publication did not.
Because the historical aggregate rule was conjunctive, the campaign did not
support the aggregate `100x` or `500x` claim. This is the historical campaign's
own result, not V2 `FAILED_TARGET`. V2 has no approved quantitative target and
has not run a qualifying campaign.

## 3. Fixture and environment receipt

| Field | Recorded historical value |
|---|---|
| Report evidence sealed / assembled | 2026-08-01 / 2026-08-01 |
| Platform | Linux/arm64 guest on macOS Docker Desktop |
| Docker Desktop allocation | 4 vCPU / 4 GiB |
| Container image | `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` |
| Storage | persistent ext4 with OverlayFS; not tmpfs |
| Workload `memory.high` / `memory.max` | 96 MiB / 128 MiB |
| Application pool ceiling | 8 MiB |
| Receipt clock label | `CLOCK_MONOTONIC` |
| R0 fixture | `console-release`; 912,350,100 logical bytes; 3,602 files; 694 directories |
| S4 fixture | `s4-chain-sparse-v1`; 8,589,934,592 logical bytes; eight logical allocations; depths 1/5/8 |

The historical phase specification required `CLOCK_MONOTONIC_RAW`, while the
receipts reported `CLOCK_MONOTONIC`. That mismatch is retained as an evidence
limitation. Docker setup contributed `2.198345375 s` to the recorded `3.99 s`
complete cold-process result and must not be hidden when interpreting that
boundary.

The historical sparse-fixture observation of zero allocated or copied payload
bytes is scoped to that exact fixture and operation. It is not universal
"zero-copy" evidence, a V2 accepted-reference measurement, or evidence of zero
metadata, coordination, fencing, or backend work.

## 4. Operation-level observations

The ratio orientation below is always `control median / candidate median`, as
defined by the historical report.

| Historical operation | Candidate samples (ms) | Candidate median / max (ms) | Control samples (ms) | Control median (ms) | Control/candidate | Historical gate |
|---|---|---:|---|---:|---:|---|
| Exact activation | 21.155500, 18.431042, 21.375375, 53.056750, 55.029542 | 21.375375 / 55.029542 | 13,925.473340, 13,426.207298, 13,034.438715 | 13,426.207298 | 628.115637644x | PASS |
| Same-generation activation | 21.155500, 18.431042, 21.375375 | 21.155500 / 21.375375 | 11,649.543256, 11,310.809838, 10,810.835838 | 11,310.809838 | 534.651028716x | PASS |
| Fork | 9.468417, 7.706708, 5.857166 | 7.706708 / 9.468417 | 13,277.046215, 13,353.248090, 13,023.158923 | 13,277.046215 | 1,722.790874521x | PASS |
| Rollback | 18.476208, 16.368959, 16.487709 | 16.487709 / 18.476208 | 13,158.580589, 13,313.166131, 12,943.071590 | 13,158.580589 | 798.084232867x | PASS |
| Small publication, matched first three | 58.136209, 57.915167, 62.567625 | 58.136209 / 62.567625 | 36.678333, 36.444000, 36.051083 | 36.444000 | 0.626872660x | FAIL |

The publication direction can also be stated as candidate/control:
`58.136209 / 36.444000`, approximately `1.595x`; the candidate median was about
1.6 times slower than the historical control median.

Publication had two additional candidate observations, `63.389209 ms` and
`65.937250 ms`. Across all five candidate samples, the median was
`62.567625 ms` and maximum was `65.937250 ms`. Those five candidate samples
cannot be paired with only three controls. Three matched observations also do
not establish p95 or a credible tail bound.

## 5. Other reported observations

| Scope | Recorded historical observation | Interpretation limit |
|---|---:|---|
| F0 cache-command outer path | 133.683 s before; 1.228642917 s after; reported 108.805412989x | Historical sparse-fixture cache construction only; not V2 publication or materialization. |
| F0 complete cold process | 3.99 s | Includes 2.198345375 s of separately reported Docker setup. |
| Warm attachment | 24.825208 ms service; 374.467417 ms complete preparation | Not the P0 phase wall and not a universal runtime-readiness result. |
| Logical squash | 6.504750 ms outer median; 9.196250 ms max; 0.831042 ms service median; 0.854958 ms max | Historical absolute gate, not an aggregate multiplier vote. |
| Durable stream | 1,073,741,824 B in 994.910334 ms; 1,079,234,768 B/s = 1.005115703 GiB/s | One result in two unit systems; passed historical 1 GiB/s narrowly and missed preferred 5 GiB/s. |
| Recovery | 46 registered interruption/recovery points passed | Historical POC coverage; not V2 recovery proof. |
| P4 publication cgroup peak | 7,430,144 B | P4 receipt only. |
| P1 activation cgroup peak / campaign maximum | 102,543,360 B | Must not be assigned to publication or compared to an unmatched V2 resource gate. |

The historical report also cites older, separately scoped observations:
`107.024411507 s` for first candidate/CDC/CAS work, `9.987675338 s` for cold
complete materialization, `6.361909169 s` for a same-key explicit materializer,
and `0.035375 ms` for ordinary warm-generation lookup median. They were not
substituted for the matched scorecard denominators and are not sealed V2
baselines.

## 6. Provenance and reproducibility limits

| Receipt | Recorded identity | What it proves and does not prove |
|---|---|---|
| P8 terminal sealing run | manifest SHA-256 `837578247484c38c95285b12c0e7710b66546e643c3132f3368aa3c87891638f`, 14 entries; commit `99290631750430cf267b5c9329f2ac5d281def05`; tree `ae1eac3747de54de749bd3290c7555f4988be8aa` | Authenticates the named terminal evidence set and sealing-process receipt. It is not the causal source identity for every scored phase. |
| P4 publication run `mpla-final50-p4-20260731t100712z` | manifest SHA-256 `ca38a57d6a93fd268e2f696a78e234bf73f3dccfdf64e1fd6883ae46438bfc96`, 20 entries; commit `ac5c0686807ab40ee7e4ef3ff0f8488b66292221`; tree `918b4c0fad8ac37c5e2916d10b9b18d44cfeac55`; tracked-diff size 496,505 B; claimed tracked-diff SHA-256 `1580ae28b40dee88177bfde575e16ffdf6daf2cff21d2007732b8aaaa2f4b132` | Authenticates the preserved P4 artifact set and identity commitments. The dirty patch bytes, untracked source, exact host scorecard executable, and complete transitive build/runtime closure are absent. |
| P1 activation run `mpla-final34b-p1-20260731t014941z` | commit `ac5c0686807ab40ee7e4ef3ff0f8488b66292221`; tree `918b4c0fad8ac37c5e2916d10b9b18d44cfeac55`; tracked-diff size 74,930 B; claimed tracked-diff SHA-256 `2bfc4b64f730a6b956f17c1dbd74fa33ef5c7fc1ad5a9bd029a3d1e51913744f` | A distinct phase receipt. It is not interchangeable with P4 and does not close the missing source state. |

A receipt hash proves that the receipt bytes are unchanged. An embedded dirty
diff hash is an identity commitment, not the dirty patch itself. Because the
exact dirty/untracked source and complete causal executable/configuration
closure are unavailable, no current reader can reproduce the historical
campaign from these tuples alone.

## 7. What V2 may reuse

- fixture concepts, after independently recovering, hashing, and verifying the
  exact fixture bytes and semantic coverage;
- timing-boundary and setup/cleanup lessons;
- independent semantic and correctness-oracle patterns;
- matched candidate/control sampling discipline;
- separate source, executable, environment, resource, command, raw-sample, and
  manifest receipts;
- crash-cut and recovery-case ideas, after re-deriving the V2 cut set; and
- publication and materialization as separate bottleneck hypotheses.

## 8. What V2 may not infer

- no V2 implementation, architecture winner, backend, storage profile, or
  performance claim was qualified;
- no historical latency, multiplier, throughput, or resource value is a V2
  target, SLA, gate, comparator denominator, or production guarantee;
- historical correctness cannot waive current V2 correctness, durability,
  identity, custody, recovery, or retirement gates;
- MPLA identity, locator, reference, layer, squash, mount, or module concepts do
  not become selected R0 contracts; and
- phase-wall time, operation latency, matched samples, candidate-only samples,
  and resource peaks from different phases may not be relabeled or combined.

## 9. Route to a comparable baseline

A future comparator needs either a new attested run under the selected V2
protocol or a full historical reconstruction. A reconstruction would have to
recover the exact clean base, tracked dirty patch bytes, untracked build inputs,
toolchain, dependencies, build configuration, executable bytes, fixture bytes,
commands, phase-specific source binding, environment/resource/cache state,
timing/durability boundaries, raw samples, and verified manifests.

Until one route is completed and passes the selected comparability gates:

```text
R_stage46 = INCOMPARABLE
STAGE_4_6_COMPARISON = INCOMPARABLE
V2_FINAL_PERFORMANCE_VERDICT = TARGET_UNSELECTED
V2_ACCEPTANCE_EFFECT = NONE
```

Stage 04.6 suggests dimensions worth measuring—especially publication,
materialization, runtime readiness, resources, and recovery—but does not select
their V2 targets. Those targets remain governed by [target.md](target.md).
