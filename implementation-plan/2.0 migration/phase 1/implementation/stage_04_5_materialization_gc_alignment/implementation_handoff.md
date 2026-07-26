# Stage 04.5 handoff to Stage 05

Verdict: **PASS WITH OWNER-APPROVED PERFORMANCE EXCEPTIONS**

Created: 2026-07-27T04:12:00+08:00

The raw strict benchmark verdict remains `FAIL`. This handoff does not rewrite
that result: it records the owner's explicit acceptance of the retained
performance measurements. Every correctness, authority, resource, space,
integrity, cleanup, and quiescence gate passed.

## Frozen identities

- Product: branch `upgrade-2.0-phase-1`, base
  `68c6e2bdeb490c2e7a24f3791dba865c38d9e737`, dirty diff SHA-256
  `3a6ef338234bedece22354673287504cb3f25973a0ae536fcfba46199aad1a69`.
- Tests: branch `upgrade-2.0-phase-1`, base
  `47d634d88db005f81b3e2c1ed66a8b4a4bc3d80b`, pre-handoff dirty diff
  SHA-256 `ec4f4ebe26c01e6668c48f0b3191aa3f8ce5a22721fc055df426fba3d8198231`.
- Documentation: branch `layerstack_2_0`, base
  `98949dee6b20ff290f98f5d06f87008ce6bc4362`.
- Product profile: Rust debug and release Linux/arm64 musl oracles; final
  candidate-materialization oracle SHA-256
  `86a398977e00b23334424573f48bb00c106c33e689ed463d42421e7849d84b74`.
- Host: Apple M3 Max arm64, 36 GiB RAM, macOS 26.4.1/Darwin 25.4.0.
- Runtime: Docker 29.5.2 Linux/arm64.
- Pinned image:
  `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`.
- Stage 04.5 evidence owner:
  `6ee1e379-86cf-4275-bcbe-b7ac3da251e8`.
- Catalog SHA-256:
  `64f0bb62004304c7af860e1f042259d9e9a86f130c0fddd8d68f55d750b86db3`.
- Public authority: `legacy_v1`; candidate public and fallback authority remain
  disabled.

## What Stage 04.5 delivered

- Private materialization and squash build complete and verify before
  visibility.
- The lifecycle is exactly `Building → Ready → Published → Terminal`; `STATE`
  remains operation/recovery truth, `CURRENT` remains the selector, and
  `MANIFEST` is immutable after Ready.
- Materialization, repair, and squash use the bounded common publisher and the
  Stage 05 root-admission/exact-old-subject handoff seam.
- `RootId`, `AttributionRootId`, generation fences, old-reader pinning, and
  new-reader selector behavior are preserved.
- The supervisor owns the four-worker pool, operations, waiters, queues, build
  bytes, FDs, holds, recovery pages/retries, shutdown, and exact private-work
  cleanup.
- Production generation deletion, retirement, GC, packing, locator
  publication, and public-authority changes are unreachable. Stage 04.5 cleans
  only exact operation-owned private work.
- Product integration covers candidate generation/materialization/squash
  publication, the storage supervisor and resource accounting, operation and
  workspace/session/command/PTY bridges, and the supported gateway path.
- Test infrastructure covers 77 typed Stage 04.5 E2E cases, the retained Stage
  04 suite, benchmark planning and verification, crash/recovery paths, and
  immutable benchmark evidence.

## Direct evidence

| Gate | Status | Evidence | Exact reason |
| --- | --- | --- | --- |
| Static authority and architecture | PASS | `CMD-S045-394` | Seven positive/negative architecture-policy fixtures passed. |
| Formatting and linting | PASS | `CMD-S045-395`, `CMD-S045-396`, later focused format/build commands | Formatting and warnings-denied policy checks passed. |
| Full product regression | PASS | `CMD-S045-397` | `cargo test --workspace --all-features` passed. |
| Catalog | PASS | `CMD-S045-400`, `CMD-S045-401` | All 882 repository items accepted; exactly 77 Stage 04.5 cases collected. |
| Stage 04.5 typed E2E | PASS | `CMD-S045-406` | Exactly 77/77 passed, no skips/xfails or retained owned containers. |
| Stage 04 regression | PASS | `CMD-S045-409` | All 128/128 retained strict typed cases passed. |
| Benchmark verifier/planning/integration | PASS | `CMD-S045-483`, `CMD-S045-411`, `CMD-S045-414`, `CMD-S045-415` | 13 verifier, 23 planning, and 41 integration/compatibility tests passed; frozen plan validated. |
| Gateway rebuild | PASS | `CMD-S045-452` | Supported gateway rebuilt and reloaded the current product. |
| Functional/resource/space/cleanup campaign gates | PASS | `CMD-S045-484` | All non-performance gates passed; zero forbidden work and unexplained bytes. |
| Performance release disposition | PASS WITH EXCEPTIONS | `CMD-S045-480`, `CMD-S045-484` | Raw measurements retained; explicit owner tolerances applied below. |

All command JSON is under
`ephemeral-sandbox-test/.e2e-state/evidence/stage04_5-6ee1e379-86cf-4275-bcbe-b7ac3da251e8/`.
The append-only narrative ledger is
`ephemeral-sandbox-test/e2e/test-report.md`.

## Official benchmark artifact

- Command: the exact `CMD-S045-484` `sandbox-benchmark run --plan
  layerstack-phase1-stage04-5-materialization-gc-alignment` invocation recorded
  in the test report.
- Run: `019fa006-36da-7f9f-ae82-3b3af89f2bab`.
- Artifact:
  `ephemeral-sandbox-test/.benchmark-state/results/019fa006-36da-7f9f-ae82-3b3af89f2bab/stage04_5/stage04_5-materialization-gc-alignment-v1.json`.
- Whole-artifact SHA-256:
  `85b3db42ea391ec4b4f22f385e607613cc18c11da55598da45d81a9d326cb689`.
- Manifest/verdict/raw-sample component SHA-256:
  `6776b2ee69cd34830e660bdedac98bd4a669e86ce7635f46feddee1d458ef9e0`,
  `aa8e163461f797cf6216d41fe608ef7771718d185b5244b96ab75ac74ced1907`,
  and `fd53085e5c022aaea968290a263adca8dbbdff91a747751fca8765e169d68409`.
- Clock: `179.796 s` runner elapsed; artifact completed `1.986 s` before its
  strict deadline, stopped admission before settlement, ran zero retries, and
  had no operation over `60 s`.
- Samples: every p50/p95 arm has 20 matched samples; p99 is honestly
  `INSUFFICIENT_SAMPLE` at `n=20`.
- Resources: all configured caps passed; four-times-history adjusted RSS growth
  was `12,288 B`; mapping peak was zero.
- Space: all 13 buckets reconciled; unexplained allocated bytes were zero.

## Owner-approved performance exceptions

The strict formulas and raw `FAIL` cells remain unchanged:

- Cold hydration aggregate throughput is `145,411,063.594 B/s` versus
  `302,624,797.003 B/s`, ratio `0.480499`. The owner explicitly accepts this
  approximately `48%` cold-read result.
- In the retained unchanged-product run `CMD-S045-480`, cold activation missed
  its formula by `6.363 ms`, inside the owner's `10 ms` acceptance.
- One-megabyte sequential read measured ratio `0.942917` in `CMD-S045-484`,
  `0.7083` percentage point beyond the ordinary 5% tolerance; the immediately
  preceding unchanged-product run passed its inherited p95 throughput gate at
  `0.999790`. This is dispositioned as run variance, not an architecture defect.
- Small-edit publication missed by `2.175 ms`, within the `10 ms` acceptance.
- Full and frozen squash passed in `CMD-S045-484`; earlier low-single-digit
  squash misses remain retained in the append-only ledger and are accepted.

No product threshold, correctness assertion, resource cap, or raw sample was
weakened or rewritten.

## Optimization guardrails

Stage 04.5 is complete. Treat the owner-approved measurements above as frozen
release policy, not as open performance bugs. In particular, do not change the
architecture merely to turn the strict raw benchmark artifact green:

- Cold-read performance at approximately `48%` of the baseline is accepted.
- Activation, small-edit publication, and squash differences up to `10 ms` are
  accepted.
- Ordinary `0–5%` throughput variation is accepted.
- A single marginal or contradictory run is noise unless it reproduces in
  matched runs and exposes a concrete defect.

Correctness and ownership outrank microbenchmark improvements. Preserve:

- `Building → Ready → Published → Terminal`, immutable Ready `MANIFEST`,
  durable `STATE`, and atomic `CURRENT` publication.
- The bounded common publisher, writer-lock discipline, exact generation
  fences and reader pins, root admission, fsync/verification, resource caps,
  and exact private-work cleanup.
- Zero hidden fallback, hidden cache/pool, forbidden work, unexplained space,
  or Stage 04.5 production-deletion authority.

Do not remove durability work, move expensive work into the writer lock, bypass
the common publisher, add speculative caching or batching, special-case the
benchmark path, or loosen thresholds/raw evidence to claim a pass. Do not add
retirement, deletion, or GC as a Stage 04.5 performance shortcut; that authority
belongs to Stage 05.

Only optimize when all of the following are true:

1. The regression repeats in at least two matched runs using the same build,
   image, topology, and arm order.
2. It exceeds the accepted tolerances, violates a hard resource/deadline cap,
   or reveals a correctness/lifecycle problem.
3. Measurement or profiling identifies specific candidate-only work rather
   than general host or control-arm variance.
4. The change can remain narrow and preserves every authority, durability, and
   cleanup invariant.

Use this workflow for any justified optimization:

1. Reproduce the focused cell and retain the unmodified raw samples.
2. Measure the suspected stage outside the writer lock and identify the actual
   bottleneck.
3. Make the smallest local change; avoid new abstractions unless the evidence
   requires them.
4. Rerun the focused functional, failure/recovery, resource, and benchmark
   checks.
5. Run the full campaign only after the focused result shows stable,
   meaningful headroom.
6. Drop the optimization if the gain is run noise, depends on test-only
   behavior, or increases architectural complexity without robust benefit.

The priority order for follow-on work is: authority and correctness, recovery
and durability, bounded resources and cleanup, stable performance, then
microbenchmark score.

## Custody and cleanup

- The final artifact proves every run-owned container absent, runtime owner
  removed, quiescence true, unexplained residue `0 B`, and unrelated resource
  changes `0`.
- Only exact operation/run-owned private state was cleaned. Shared caches,
  unrelated containers, user work, and retained evidence were preserved.
- The working trees remain intentionally dirty with the Stage 04/04.5
  implementation and evidence; no branch switch or history rewrite occurred.

## Remaining authority boundary

- Stage 04.5 introduces no public capability and leaves v1 read/write
  authoritative.
- Stage 05 owns the first retention, GC, retirement, and deletion authority.
- Stage 06 owns candidate public-authority switching.
- Stage 07 owns broad platform qualification and irreversible v1 retirement.

## Exact blockers or next action

No Stage 04.5 blocker remains. Stage 05 may begin from this frozen handoff while
preserving the owner-approved performance exceptions and all raw evidence.
