# Stage 04 benchmark note

Status: **POC PASS** (2026-07-25; not release qualification).

The official campaign is `019f9aef-8059-7524-8cd8-d569c9c3d3d2`. Its strict
artifact is
`ephemeral-sandbox-test/.benchmark-state/results/019f9aef-8059-7524-8cd8-d569c9c3d3d2/stage04/stage04-materialization-evidence-v1.json`
(SHA-256
`9116f77b9f327b3d0e1aacf2d59b7286e21e00395c15347f178090d5cd625434`).
The official runner command record is `BENCHMARK-STAGE04-OFFICIAL-D203.json`
(SHA-256
`7d8a2cf6b46fe63f9e2b73aee4dd987d5ea2a744a4a0ab0d2635032bd2ff8c66`);
the independent acceptance record is `CMD-OFFICIAL-ACCEPTANCE-D204.json`
(SHA-256
`171c2aa834af079e01c70066814e2779e8733ad693fd546559fabb66b6663d09`).

| Gate | Direct result | Threshold | Verdict |
| --- | --- | --- | --- |
| cold reconstruction | p95 candidate/control throughput ratio `0.825583` | `≥0.70` | `PASS` |
| cold activation | candidate p95 `42.364291 ms` | `≤45.206416 ms` copy-plus-warm limit | `PASS` |
| warm admission, `D=64` | p50/p95 `17.093709/21.649333 ms` | `≤19.701075/22.531218 ms` | `PASS` |
| no-op command | p95 `18.033167 ms`; throughput ratio `3.756245` | `≤70.269110 ms`; `≥0.97` | `PASS` |
| native file read/write | p95 throughput ratios `5.968929/3.234837` | each `≥0.97` | `PASS` |
| PTY create | p50/p95 `6.643250/8.802708 ms` | `≤60.389671/68.714689 ms` | `PASS` |
| PTY drain | p50/p95 `0.875500/1.354625 ms` | `≤1.148642/20.338873 ms` | `PASS` |
| deadline | maximum operation `532.579 ms`; one campaign clock | operation and campaign inside `150/180 s` boundaries | `PASS` |
| resources/space | workers, buffers, RSS, FDs, maps, and ten space boundaries reconcile | all caps/exact accounting | `PASS` |
| correctness/route | E01–E12 pass; public authority `legacy_v1`; allowed route positive; every forbidden warm delta zero | exact | `PASS` |
| sufficiency | 20 raw samples per inferential arm/cell | `≥20` | `PASS` |
| cleanup | durable ledger; quiescent; unexplained residue `0` | exact zero | `PASS` |

The command figure requested by the user is the sessionless public
`sandbox-runtime-cli exec_command` operation, including its implicit
`create_workspace_session`: p50 `117.676 ms`, p95 `122.387 ms`, maximum
`122.937 ms`. Existing-session `exec_command` was separately measured at p50
`43.379 ms`, p95 `45.671 ms`; the two figures must not be conflated.

The selected direct environment cell,
`docker-desktop-linux-vm-arm64-ubuntu-glibc`, passed against immutable image
`ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`.
Six amd64/musl/distroless/shell-less/read-only/non-root cells remain `NOT_RUN`.
Universal platform/image/filesystem claims, statistical release qualification,
soak/fleet campaigns, authority cutover, and v1 retirement remain
`DEFERRED_STAGE_07`.

The cleanup ledger SHA-256 is
`74e4638c8cc65a78ba8394369d745cbdb6fd451a66bf0287731ccfeb661b7908`.
The final authority summary is `final-v1-authority.json` (SHA-256
`22eac843a5f44b6aeb8d5054089d7d2d16928c69eb0c78f1d13761158cac0073`).

[Stage 04.5](../stage_04_5_materialization_gc_alignment/benchmark_note.md)
supersedes this POC for common publication, recovery/resource caps,
old-generation handoff, and peak-overlap qualification.
