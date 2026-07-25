# Stage 04 handoff to Stage 05

Verdict: **POC PASS — never release-qualified**

Closed at: 2026-07-26T04:56:00Z

## Scope and authority

Stage 04 candidate materialization, activation, strict command/file/PTY
routing, typed recovery, resource accounting, and the focused performance
campaign pass in the selected Linux/arm64 environment. Public authority
remains `legacy_v1`; candidate code has neither public nor fallback authority.
Stage 05 may consume the retained generation/lease evidence, but must not infer
release qualification or v1 retirement.

## Source and run identities

| Identity | Value |
| --- | --- |
| product repository | `ephemeral-sandbox`, commit `a400863b9` plus retained reviewed working-tree changes |
| test repository | `ephemeral-sandbox-test`, commit `152d37acf` plus append-only `e2e/test-report.md` |
| documentation repository | `ephemeral-sandbox-docs`, commit `6cacd62` plus this closure |
| canonical plan | SHA-256 `d95d9380e8b72a96746d4b6a6c0637efe05ed8a911f0eaf01dc6f83ccf02778b` |
| official campaign | `019f9aef-8059-7524-8cd8-d569c9c3d3d2` |
| selected image | `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` |
| candidate oracle | SHA-256 `8f41d104464733295bb6074e2cb9c12294fa1872b9340636a077d1ca86312d83` |
| workspace oracle | SHA-256 `5bbc4524a8d9e34ecc0263867172b28c291d038e8eeb63956ebb4ae6f3d4704f` |
| catalog exporter | SHA-256 `46fefcd77e08d008c6b076c43f2277be5af1dfa42dd0d11091427079ec75bdda` |

## Retained evidence

| Evidence | SHA-256 | Result |
| --- | --- | --- |
| strict official artifact `stage04-materialization-evidence-v1.json` | `9116f77b9f327b3d0e1aacf2d59b7286e21e00395c15347f178090d5cd625434` | every verdict `PASS` |
| official campaign command `BENCHMARK-STAGE04-OFFICIAL-D203.json` | `7d8a2cf6b46fe63f9e2b73aee4dd987d5ea2a744a4a0ab0d2635032bd2ff8c66` | `PASS` |
| independent acceptance `CMD-OFFICIAL-ACCEPTANCE-D204.json` | `171c2aa834af079e01c70066814e2779e8733ad693fd546559fabb66b6663d09` | `PASS` |
| final v1 regressions `CMD-P05-FINAL-V1-RETRY-D209.json` | `14c8a83f4b479560e485d3a29520b2240c0302cd157ece45ed5097f9460b411a` | `PASS` |
| final typed E2E `CMD-E03-FINAL-D210.json` | `05bae8e7b06c1a02559c65ed94a96c6400fe5ec2654b871d168ca1338a097de9` | 128/128 `PASS` |
| dependency/boundary `CMD-DEPENDENCY-BOUNDARY-AUDIT-D207.json` | `5041aa3298518ff6276b0ce32b4dc3947546149db65b20d3168c6397fd4d3ce3` | `PASS` |
| dependency delta | `a4fd0ed027f72bad8ae717d6fbf320122688d9fdb600ae385432dc88cf2b993b` | zero unexplained delta |
| boundary audit | `dd8ce7c5c44daa22bbac6924377d72b24b4dfa3df969a6086adf261384091baf` | portable core/ownership `PASS` |
| final v1 authority | `22eac843a5f44b6aeb8d5054089d7d2d16928c69eb0c78f1d13761158cac0073` | `legacy_v1`, `PASS` |
| Stage 07 deferral audit | `7f4173df64a8e37e427efcd26e2158707505af18a9eeac6c810d9e61b4fb0e6c` | explicit |
| cleanup ledger | `74e4638c8cc65a78ba8394369d745cbdb6fd451a66bf0287731ccfeb661b7908` | durable, quiescent, zero unexplained residue |

Evidence root:
`ephemeral-sandbox-test/.e2e-state/evidence/stage04-019f97c8-38c6-7352-9a4f-84f40f227588`.

## Performance disposition

All direct POC gates pass. Cold reconstruction ratio is `0.825583`; cold
activation p95 is `42.364291 ms`; warm `D=64` admission p50/p95 is
`17.093709/21.649333 ms`; no-op command p95 is `18.033167 ms`; file
read/write ratios are `5.968929/3.234837`; PTY create p50/p95 is
`6.643250/8.802708 ms`; PTY drain p50/p95 is `0.875500/1.354625 ms`.
See [`benchmark_note.md`](benchmark_note.md) for thresholds and the separate
sessionless `sandbox-runtime-cli exec_command` figure.

## Cleanup and retained state

The official cleanup ledger is durable, `quiescent=true`, and records zero
unexplained residue. Final E2E custody found zero suite-owned containers and
zero nonterminal candidate runtimes. Ordinary Cargo cache, the catalog
exporter, the official artifact tree, append-only report, and generated audit
summaries are intentionally retained. Pre-existing shared gateways/listeners
remain outside Stage 04 ownership.

## Stage 07 deferrals

| Deferred item | Status |
| --- | --- |
| release-wide Linux distribution/kernel/Docker/VM/filesystem qualification | `DEFERRED_STAGE_07` |
| universal amd64/arm64, glibc/musl, shell-less, minimal/distroless, read-only, and non-root claims | `DEFERRED_STAGE_07` |
| percentage-supported environment/image claims | `DEFERRED_STAGE_07` |
| soak, fleet/multi-host, upgrade/rollback, and destructive-retention campaigns | `DEFERRED_STAGE_07` |
| statistical performance qualification beyond the direct samples | `DEFERRED_STAGE_07` |
| authority cutover, v1 retirement/deletion, and destructive retirement | `DEFERRED_STAGE_07` |
| full Stage 05 pack/locator/GC/squash production-retention behavior | `DEFERRED_STAGE_07` |

The selected `docker-desktop-linux-vm-arm64-ubuntu-glibc` cell passed directly.
The six environment cells recorded `NOT_RUN` in the strict artifact remain
unrun; no generalized support claim is made. Stage 07 resources created by
Stage 04: zero.

## Stage 04.5 gate before Stage 05

Stage 05 must not treat this direct Stage 04 record as sufficient entry.
The mandatory alignment gate and incoming evidence are recorded in
[Stage 04.5 handoff](../stage_04_5_materialization_gc_alignment/handoff_from_stage_04.md).
Stage 04.5 must first remove the Stage 04 retirement/deletion path, align
publication/resource/recovery ownership, and pass its own direct exit evidence.

## Eventual Stage 05 entry

Stage 05 should consume exact generation/fence/lease identities, preserve
`legacy_v1` authority, maintain the retained cleanup/custody model, and start a
new append-only evidence run. It owns pack/locator/GC/squash and retirement
behavior only after its own entry gates; Stage 04 created no deletion or
authority-cutover permission.
