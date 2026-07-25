# Stage 03 entry environment and gate evidence

Timestamp: `2026-07-24T22:16:53Z`

Purpose: retain the direct entry evidence for `S03-G03` through `S03-G08` and
`S03-G10` before Stage 03 product implementation. The v3 owner decision/corpus
is retained separately by `S03-G01`; retained Stage 00–02 artifact verification
is retained separately in `stage03_entry_evidence_20260725.md`.

## S03-G03 — PASS: public v1 remains sole authority

The exact fresh Stage 03 entry regression was:

```text
E2E_IMAGE=ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90 E2E_REBUILD_BINARY=1 PYTHONPATH=e2e .venv/bin/python -m pytest e2e/runtime/layerstack_phase1/test_portable_root_contract.py::test_PRC_01_portable_root_contract_is_runtime_dormant --test-repository-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test --product-root /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
```

It passed 1/1 on the first Stage 03 entry attempt in 24.23 seconds. It proved
public-v1 no-op and changed publication/readback, all fifteen candidate gauges
zero, all fifteen forbidden candidate paths absent at every required boundary,
and exact run-owned teardown.

- Run: `20260724T221647.648307Z-52067`
- Stable ID: `runtime.layerstack-phase1.portable-root.feature-off`
- Evidence root:
  `.e2e-state/observability/20260724T221647.648307Z-52067/runtime.layerstack-phase1.portable-root.feature-off`
- Summary: 51,370 evidence bytes; SHA-256
  `de5fee5ea1d5f2a25ca324d48df45815cfe4fdbc9a7f2458f19ef7efde6447d6`
- Cleanup: `cleanup_complete=true`, no failures, registered and destroyed
  sandbox exactly `eos-26c6a566-4eb9-42b3-a6b5-1511d81dc8c0`; SHA-256
  `1a9511c34b5eef41f25ebb1f21dbc639d70d60bc435246d94b654401469abbdd`
- The seven sandboxes visible after the test predated this run; none was owned,
  modified, or removed by it.

## S03-G04 — PASS: shared-worktree custody

Fresh post-baseline custody:

| Repository | Branch | HEAD | Upstream | Task-owned state |
| --- | --- | --- | --- | --- |
| product | `upgrade-2.0-phase-1` | `cbe45de873cd24fbf48bb7b3a6c5f9f98980313c` | same | tracked worktree clean; rebuilt ignored binaries only |
| test | `upgrade-2.0-phase-1` | `173191e8694515af43797128070dbdfd2d246040` | same | only append-only `e2e/test-report.md`; ignored run-owned evidence |
| docs | `layerstack_2_0` | `901d6d2181d0795eaaf174a23636a38019aab9a1` | `426b6be3284c26a59eb77d39ad6622997e8479c9` | Stage 03 guide and gate/decision/evidence artifacts owned by this task |

There are no unclear overlapping edits. The earlier custody record remains
`gate_resolution_20260725.md`, SHA-256
`c4951f4599bb92383c877ec6b634b2b1f6f455f64ef89462f1faae062fa906c5`.

## S03-G05 — PASS: exact dependency entry

Two independent canonical 16-invocation captures are byte-identical:

- `.e2e-state/tmp/stage03-entry-20260725T061146+0800/dependency-delta-a.json`
- `.e2e-state/tmp/stage03-entry-20260725T061146+0800/dependency-delta-b.json`
- SHA-256 for each:
  `1c77ccb2048f4c7383b0bbe6b45f5c999a88e79bcd2ef86ac2650d503e52be1d`
- 16 invocations, 1,143 external packages, 2,179 external feature pairs,
  116 direct external edges, `external_delta_exact=true`, empty external
  differences, and a passing standard-library-only core audit.

`exact=false` is expected because the Stage 00 baseline predates the approved
internal Stage 02 manifest/member changes. External dependency identity is the
normative Stage 03 gate and is exact.

## S03-G06 — PASS: required tools and harnesses

- Rust `1.96.0` (`ac68faa20`), Cargo `1.96.0` (`30a34c682`), target
  `aarch64-apple-darwin`, LLVM `22.1.2`.
- `CARGO_NET_OFFLINE=true cargo metadata --locked --offline --no-deps
  --format-version 1` passed.
- Test `.venv`: Python `3.14.3`, pytest `9.1.1`.
- Benchmark venv: Python `3.14.3`; CLI exposes only the verified `serve`,
  `validate`, `run`, `compare`, `recover`, and `cleanup` surfaces.
- Safe catalog collection passed and collected 643 tests without launching any
  case.
- No dependency installation, network fetch, alternate harness, or product
  protocol was introduced.

## S03-G07 — PASS for implementation entry: pinned environment and identities

- Host: Darwin `25.4.0`, macOS `26.4.1` build `25E253`, arm64.
- Docker Desktop `4.76.0`; Engine `29.5.2`; Linux
  `6.12.76-linuxkit`, arm64; cgroup v2 with memory, swap, CPU and PID limits.
- Local pinned Ubuntu 24.04 OCI index:
  `sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`,
  arm64/v8. It was inspected locally; no pull occurred.
- Product source/config identity is the clean product commit above.
- Newly rebuilt public CLI SHA-256 identities:
  - manager:
    `cae893d1cc9c411a6d0319f307ef5122ad5406d027b1127deb426d41a1cee228`
  - runtime:
    `b3dcd0c44caf2f7e52dc5e94dfa70e98ccb0a6d1d776c0e23199f5f872f481a9`
  - observability:
    `d2b7948a79e3561367cbdec97745ad1f56fed235b598409ac8a98a8fb8872f55`

Every later measured run must rebuild when required and retain its own exact
binary/config identities. This entry PASS does not authorize reuse of a stale
binary for a measured claim.

One diagnostic `docker image inspect` transcribed a different non-local digest
and returned `No such image`; inspecting the canonical digest above succeeded.
The root cause was transcription, not a bad canonical pin or missing image. No
Docker state changed.

## S03-G08 — PASS for implementation entry: observable capacity

- Host physical memory: 38,654,705,664 bytes.
- Product filesystem: 463,411,544 KiB free and 4,634,115,440 free inodes.
- Allocated-byte baselines (`du -sk`):
  - product repository: 14,178,632 KiB
  - product `target`: 13,736,240 KiB
  - product `bin`: 76 KiB
  - test `.e2e-state`: 669,368 KiB
  - test `.benchmark-state`: 3,104,240 KiB
- Docker VM: 4 CPUs and 4,109,398,016 bytes total memory.
- Docker confirms cgroup-v2 memory-limit observability. The public standard
  resource profile used in the fresh baseline exposes
  `memory_high_bytes=402653184` (384 MiB),
  `memory_max_bytes=536870912`, and a separate workload cgroup.
- Docker storage baseline: images 25.26 GB, containers 101.1 MB, volumes
  2.798 GB, build cache 1.274 GB.

The required 384 MiB cap is therefore expressible and observable with more than
128 MiB of environment headroom. Immediately before the benchmark campaign,
the runner must still measure warmed idle and prove at least 128 MiB-over-idle
headroom; this is an explicit per-run recheck, not an open implementation gate.

## S03-G10 — PASS: append-only reporting and exact cleanup

`e2e/test-report.md` contains the planned entry before each live command, the
exact command, image/binary/config identity, expected good/defect/fix fields,
run-owned identities, cleanup oracle, result, and retained artifact digests.
The comparator owned only
`.e2e-state/tmp/stage03-entry-20260725T061146+0800`; the public-v1 regression
owned only its registered sandbox/workspace/command IDs and immutable evidence
root. Exact cleanup passed. Broad cleanup was not used.

## Entry conclusion

`S03-G02`, `S03-G03`, `S03-G04`, `S03-G05`, `S03-G06`, `S03-G07`,
`S03-G08`, and `S03-G10` are PASS. `S03-G09` intentionally remains
`NOT_STARTED` until the Stage 03 benchmark plan/verifier and strict fixtures
exist. Product implementation may begin at `S03-I01`; no measured benchmark
campaign may begin until `S03-G09` passes.
