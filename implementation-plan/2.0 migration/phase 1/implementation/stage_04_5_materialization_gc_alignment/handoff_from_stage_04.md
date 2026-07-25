# Stage 04 handoff to Stage 04.5

Incoming verdict: **Stage 04 POC PASS; Stage 04.5 remains OPEN**

Handoff created: 2026-07-26T05:02:00Z

## What Stage 04 completed

Stage 04 completed candidate native reconstruction, immutable generation
publication, strict activation, exact session leases, per-session private
writable/execution state, command/file/PTY routing, typed recovery and
failpoints, resource accounting, and a focused performance campaign in the
selected Linux/arm64 environment. All 128 final typed E2E cases passed.
Public authority remains `legacy_v1`; candidate public and fallback authority
are false.

This is POC evidence, not release qualification. Stage 04.5 must run its own
E2E, crash/corruption, resource, space, and matched performance campaigns
before it can become `GO`.

## Frozen incoming identities

| Identity | Value |
| --- | --- |
| product base | `ephemeral-sandbox` commit `a400863b9` plus the retained Stage 04 working-tree changes |
| test base | `ephemeral-sandbox-test` commit `152d37acf` plus append-only Stage 04 reporting |
| Stage 04 official run | `019f9aef-8059-7524-8cd8-d569c9c3d3d2` |
| selected image | `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` |
| candidate oracle | SHA-256 `8f41d104464733295bb6074e2cb9c12294fa1872b9340636a077d1ca86312d83` |
| workspace oracle | SHA-256 `5bbc4524a8d9e34ecc0263867172b28c291d038e8eeb63956ebb4ae6f3d4704f` |
| catalog exporter | SHA-256 `46fefcd77e08d008c6b076c43f2277be5af1dfa42dd0d11091427079ec75bdda` |
| public authority | `legacy_v1` |

## Direct evidence to inherit

| Evidence | SHA-256 | Disposition |
| --- | --- | --- |
| strict official artifact `stage04-materialization-evidence-v1.json` | `9116f77b9f327b3d0e1aacf2d59b7286e21e00395c15347f178090d5cd625434` | every Stage 04 verdict `PASS` |
| final typed E2E `CMD-E03-FINAL-D210.json` | `05bae8e7b06c1a02559c65ed94a96c6400fe5ec2654b871d168ca1338a097de9` | 128/128 `PASS` |
| final v1 regressions `CMD-P05-FINAL-V1-RETRY-D209.json` | `14c8a83f4b479560e485d3a29520b2240c0302cd157ece45ed5097f9460b411a` | `PASS` |
| official acceptance `CMD-OFFICIAL-ACCEPTANCE-D204.json` | `171c2aa834af079e01c70066814e2779e8733ad693fd546559fabb66b6663d09` | `PASS` |
| dependency/boundary audit `CMD-DEPENDENCY-BOUNDARY-AUDIT-D207.json` | `5041aa3298518ff6276b0ce32b4dc3947546149db65b20d3168c6397fd4d3ce3` | `PASS` |
| final v1 authority `final-v1-authority.json` | `22eac843a5f44b6aeb8d5054089d7d2d16928c69eb0c78f1d13761158cac0073` | `legacy_v1`, `PASS` |
| Stage 07 deferral audit `stage07-deferral-audit.json` | `7f4173df64a8e37e427efcd26e2158707505af18a9eeac6c810d9e61b4fb0e6c` | explicit |
| cleanup ledger | `74e4638c8cc65a78ba8394369d745cbdb6fd451a66bf0287731ccfeb661b7908` | durable, quiescent, zero unexplained residue |

Stage 04 evidence root:
`ephemeral-sandbox-test/.e2e-state/evidence/stage04-019f97c8-38c6-7352-9a4f-84f40f227588`.

## Stage 04.5 required alignment work

The Stage 04.5 [specification](spec.md), [E2E plan](e2e_test.md), and
[benchmark note](benchmark_note.md) remain authoritative. In particular,
Stage 04.5 must:

- remove or make structurally unreachable the production retirement/deletion
  entry points currently rooted at
  `layerstack/src/stack/candidate/materialization.rs`:
  `begin_generation_retirement` and `finish_generation_retirement`, and
  `layerstack/src/stack/candidate/generation.rs`: `remove_generation`;
- separate private build from common publication and route every visibility
  change through the common four-state operation lifecycle:
  `Building → Ready → Published → Terminal`;
- provide the deterministic Stage 05 root-admission/old-generation handoff
  hook without implementing Stage 05 GC, unlink, locator, pack, or maintenance;
- move owners, waiters, workers, bytes, FDs, retries, holds, operations, and
  generations under the shared bounded storage governor and recovery
  dispatcher;
- prove there is no history-sized allocation/recovery/lease scan, heavy work
  under the writer lock, ownerless pool, memory mapping, or unreviewed unsafe
  expansion;
- preserve Stage 04 strict native activation, exact leases, immutable
  generations, per-session isolation, no silent fallback, and `legacy_v1`
  public authority.

## Performance and command baseline

The Stage 04 official campaign passed its direct POC thresholds. The public
sessionless `sandbox-runtime-cli exec_command`, including implicit
`create_workspace_session`, measured p50 `117.676 ms`, p95 `122.387 ms`, and
maximum `122.937 ms`. Existing-session `exec_command` measured p50
`43.379 ms`, p95 `45.671 ms`. Stage 04.5 must remeasure matched
materialization, squash, command, file, and PTY cells under its aligned
publication/resource model; these Stage 04 figures are baselines, not Stage
04.5 acceptance evidence.

## Custody and cleanup

The official Stage 04 ledger is durable and quiescent with zero unexplained
residue. Final E2E custody found no suite-owned container and no nonterminal
candidate oracle. Retain ordinary Cargo cache, the catalog exporter, the
official artifact tree, the append-only report, and audit summaries. Do not
clean unrelated shared gateways/listeners or any resource that lacks exact
Stage 04.5 ownership.

Start Stage 04.5 with a fresh ownership inventory, new run ID, new artifact
root, and append-only report pre-entry. Do not reuse Stage 04 PASS labels for
Stage 04.5-specific exit criteria.

## Explicit non-authority and deferrals

Stage 04.5 has no generation-deletion, GC, unlink, public-authority, or
retirement authority. Stage 05 owns GC admission and retirement only after
Stage 04.5 passes. Stage 06 owns candidate authority switching. Stage 07 owns
release-wide platform qualification, irreversible retirement, v1 deletion,
and production-default claims. The six unexecuted Stage 04 environment cells
remain `NOT_RUN`; generalized claims remain `DEFERRED_STAGE_07`.

Stage 04.5 entry status is `OPEN` until it records direct evidence for every
exit criterion in its specification.
