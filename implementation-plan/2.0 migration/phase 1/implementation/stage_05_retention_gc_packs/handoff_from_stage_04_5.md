# Stage 05 incoming handoff from Stage 04.5

Stage 04.5 verdict: **PASS WITH OWNER-APPROVED PERFORMANCE EXCEPTIONS**

The canonical, frozen handoff is:

- [Stage 04.5 implementation handoff](../stage_04_5_materialization_gc_alignment/implementation_handoff.md)

Read that handoff before changing Stage 05 product code, tests, benchmark
thresholds, or lifecycle behavior. It records the exact repository identities,
implemented boundary, passing evidence, retained raw benchmark artifact,
owner-approved performance disposition, custody, and optimization guardrails.

## Stage 05 entry conditions

- Stage 04.5 has no remaining blocker.
- Legacy v1 remains public read/write authority.
- The Stage 04.5 common publisher and four-state operation lifecycle are the
  input boundary; do not replace them.
- Stage 05 owns the first durable old-generation handoff, retention, GC,
  retirement, and exact-path deletion authority.
- Stage 06 still owns candidate public-authority switching, and Stage 07 owns
  broad qualification and irreversible v1 retirement.

## Performance disposition to preserve

- Approximately `48%` cold-read performance is owner-accepted.
- Activation, small-edit publication, and squash differences up to `10 ms` are
  owner-accepted.
- Ordinary `0–5%` throughput variation is owner-accepted.
- The strict raw formulas, samples, and `FAIL` cells remain immutable evidence;
  do not rewrite them to manufacture a pass.

Do not reopen Stage 04.5 or alter its architecture to chase these accepted
measurements. Optimize only after a regression is reproducible in matched runs,
exceeds the accepted envelope or a hard cap, and has a measured candidate-only
bottleneck. Correctness, deletion authority, crash durability, resource bounds,
and exact cleanup outrank microbenchmark score.

