# Stage 4.6 evidence baseline

Status: **PINNED HISTORICAL EVIDENCE — NOT A V2 BASELINE OR WINNER**

V2 joint Phase 1A `H_PROFILE` selection execution status: **`NOT_RUN`**;
accepted architecture/physical-profile winner count: **0**

Historical matched-comparison classification: **`R_stage46 = INCOMPARABLE`**

## Receipt identity and provenance limits

| Role | Pinned receipt identity and recorded commitment | Permitted use |
|---|---|---|
| P4 publication source-identity receipt | run `mpla-final50-p4-20260731t100712z`; `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z/source.json` (receipt SHA-256 `1a00b32319f8c75979e3f0e98fc38f30f1279dcc2d32459d11b2f0fefe954999`); recorded commit `ac5c0686807ab40ee7e4ef3ff0f8488b66292221`; tree `918b4c0fad8ac37c5e2916d10b9b18d44cfeac55`; tracked-diff size `496,505 B`; claimed tracked-diff SHA-256 `1580ae28b40dee88177bfde575e16ffdf6daf2cff21d2007732b8aaaa2f4b132`; P4 `mpla_lifecycle.rs` SHA-256 `72d42529d54a77db6ebfd8df82b6c0a2bdbde7920495aa25da133d51d0996cf9` | Preserve what the receipt committed to. It does not contain the dirty patch bytes, untracked source bytes, a source archive/bundle, or the complete causal build/execution closure and therefore cannot reproduce or causally close the P4 run. |
| P4 publication resource receipt | `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z/resources.json` (receipt SHA-256 `341728d9709afe1258cc767509f79b620deba70a065059eb4e53335e91d2789b`); recorded `max_cgroup_memory_peak_bytes = 7,430,144 B` | Historical P4 publication observation only; it is not the campaign P1 activation value or a current qualification. |
| P1 activation identity/resource receipts | run `mpla-final34b-p1-20260731t014941z`; `source.json` receipt SHA-256 `0594c70819fde83f7f7de9e4c0c015bb8b33e49819365c1a777d551d5e33ee43`; `resources.json` receipt SHA-256 `2551a5e5a2a022a4f3e52038265aee2701b15977e4566981665d85a6aca67b78`; recorded commit `ac5c0686807ab40ee7e4ef3ff0f8488b66292221`; tree `918b4c0fad8ac37c5e2916d10b9b18d44cfeac55`; tracked-diff size `74,930 B`; claimed tracked-diff SHA-256 `2bfc4b64f730a6b956f17c1dbd74fa33ef5c7fc1ad5a9bd029a3d1e51913744f`; recorded `max_cgroup_memory_peak_bytes = 102,543,360 B` | Historical P1 activation observation and identity commitments only. The absent dirty/untracked source and executable mean this is not a reproducibility closure; never transfer its value or implied source to P4. |
| P4 sealed run-artifact manifest | `manifest.sha256` SHA-256 `ca38a57d6a93fd268e2f696a78e234bf73f3dccfdf64e1fd6883ae46438bfc96`; `manifest-verification.json` SHA-256 `3951cd5e032a98e8ade468053a0a4b54d74a528ceb0fe60ffdadf8528e49fab1`; independent `shasum -a 256 -c manifest.sha256` passed for all 20 entries on 2026-08-03 | Proves integrity of the named P4 run-artifact set, including raw result, summary, command ledger, source/resource receipts, and staged-artifact inventory. It does not recover dirty/untracked source or prove a complete causal executable/configuration closure. |
| Later historical P6/P7 code reference | `992906`-era `mpla_lifecycle.rs` SHA-256 `9735e17471edc6076cb218a99204ab7aa062f1eabd2e7fce8f605c94c3ce0f65` | Read-only later-lineage identity. It did not produce either receipt and cannot repair their missing provenance. |

A receipt hash proves only that the receipt bytes are unchanged. The embedded
dirty-diff hash is an identity commitment, not the dirty patch itself. The P4
seal does record individual staged executable digests for `mpla-poc-oracle`
(`42b5e24c...972a`), `mpla-speed-poc-v1` (`75f73566...653`),
`sandbox-catalog-export` (`cd25eef0...849`), and `sandbox-runtime-cli`
(`a2b65647...4a2`), plus the storage-helper digest `91ee6501...fd0` in the raw
result. Those narrow attestations are real. What remains absent is all exact
dirty/untracked source, the exact host publication-scorecard executable bytes,
and a complete transitive dependency, toolchain, build-configuration, helper,
and runtime-configuration closure. The P4 and P1 observations are associated
with distinct run IDs; they are neither interchangeable nor reproducible from
the tuples above. The shared commit/tree does not close either causal chain.

## Reported historical observations

| Fact | Receipt/report value | Allowed V2 interpretation |
|---|---:|---|
| Matched-first-three candidate median and ratio denominator | `58.136209 ms` | negative historical context over the three candidate samples paired with the three control samples; excluded from Phase 0 matched statistics and not the median of all five candidate samples |
| Matched-first-three control median and ratio numerator | `36.444 ms` | negative historical context; against the matched-first-three candidate denominator, the candidate/control ratio is about `1.595x` with the candidate slower |
| Historical matched-first-three report ratio | `0.626872660x` control/candidate | uses `36.444 / 58.136209`; context for why the old POC was not a winner, not a current sealed gate result |
| All-five candidate median | `62.567625 ms` | descriptive historical candidate statistic over all five candidate samples; it cannot be paired with only three controls and is excluded from Phase 0 matched statistics |
| All-five candidate maximum | `65.937250 ms` | descriptive historical candidate maximum over all five candidate samples; five observations provide no qualified tail bound |
| Sample scopes | five candidate samples, of which the first three have matched control samples | the matched-first-three and all-five statistics answer different questions and must never be relabeled or combined |
| P4 publication cgroup peak | `7,430,144 B` | P4 receipt only; not campaign maximum or current qualification |
| P1 activation cgroup peak/campaign maximum | `102,543,360 B` | numerically `1,880,064 B` above the proposed V2 `100,663,296 B` maximum, but the incomparable historical profile cannot pass or fail V2 qualification |
| Matched-first-three-candidate/10 stress value | `5.8136209 ms` | unmeasured derivation from the `58.136209 ms` ratio denominator, not a result, SLA, or hard gate |
| Control/100 stress value | `0.36444 ms` | unmeasured derivation, not a result, SLA, or hard gate |

The historical campaign used a different cgroup profile, including a `128 MiB`
maximum in its report. Its observations cannot pass or fail the V2 `96 MiB`
gate. The two derived speed values also cannot decide qualification. Neither
the matched-first-three median nor the all-five median/maximum supplies a tail
model. Only the single Phase 0-frozen `QG-PERF-001` contract, run against a newly attested
matched incumbent, may pass or fail performance. The historical medians, peaks,
and derived values remain negative context or stress hypotheses for newly
attested tests.

## What may be reused

- fixture ideas, and fixture bytes only after Phase 0 separately recovers,
  hashes, and verifies their exact content and semantic coverage;
- timing-boundary and setup/cleanup lessons, not the historical medians as a
  live comparator;
- independent semantic/oracle patterns;
- persisted durability-cut and negative-case ideas, only after Phase 0
  re-derives the complete cut set and keeps process crash, `SIGKILL`, host crash,
  and power loss distinct;
- public-CLI evidence discipline and receipt verification; and
- bottleneck traces as hypotheses for a complete candidate comparison.

## What may not be inferred

- No PMSS/V2 implementation was qualified.
- No physical profile was selected because the V2 tournament has not run.
  Stage 4.6 cannot manufacture either a winner or a formal `NO_WINNER` result.
- No Canonical Format, selected-state representation, index, selector,
  publication, maintenance, or recovery method won.
- The P4 or P1 tuple is not a source archive, causal closure, executable
  attestation, or reproducibility proof.
- Layer, squash, remount, runtime-specific storage, POC process, and module
  boundaries are not V2 architecture requirements.
- A value cannot be relabeled for another commit, workload, cache state, timing
  boundary, durability boundary, resource profile, or executable.
- Historical correctness rows cannot waive current correctness, provenance,
  performance, or resource gates.

## Phase 0 comparator eligibility

The default remains:

```text
R_stage46 = INCOMPARABLE
```

Stage 4.6 may become comparator-eligible only by one of these two routes:

1. Produce a newly attested incumbent comparator run under the accepted Phase 0
   protocol, with exact source, binary, build, fixture, command, environment,
   order/seed, and raw-result provenance.
2. Reconstruct the historical run from the exact clean base **and** exact dirty
   source, including every tracked patch and untracked/ignored build input;
   preserve it as a content-addressed source archive or Git bundle plus the
   dirty/untracked archive; and pin the dependency lock, compiler/toolchain,
   build configuration and command, executable digest, fixture bytes, run
   command, environment/cgroup/cache/timing boundaries, and raw samples.

Only a reconstruction that passes `QG-PROV-001` and the accepted matched
protocol may receive a new comparable classification. Until then, exclude the
historical values from paired samples, confidence calculations, baselines, and
acceptance decisions. Run current `origin/main` and every complete joint Phase
1A `H_PROFILE` candidate survivor on separately prepared equivalent inputs;
retain Stage 4.6 only
as negative historical context, never as the implementation base or cherry-pick
authority.
