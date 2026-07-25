# Stage 03 dependency and portability closure audit

Date: 2026-07-25  
Verdict: **PASS** for `S03-D01` and `S03-V46`

## Scope and authority

This audit covers only the authorized Stage 03 private-publication delta. It
does not approve a new public authority, Stage 04 materialization, Stage 05
packs/squash, Stage 06 cutover, or Stage 07 release qualification.

The product baseline is
`cbe45de873cd24fbf48bb7b3a6c5f9f98980313c`; the test/benchmark baseline is
`173191e8694515af43797128070dbdfd2d246040`. The approved v3 corpus identity is
`sha256:7090f6646e67e7b8f4cca1dcf87cd9d7f4fed99ae33d87ec44c4436757b704be`.

## Exact dependency comparator result

The Stage 00 baseline comparator was executed twice at Stage 03 entry, once
twice at the earlier exit boundary, and twice again after the final canonical
campaign:

| Boundary | Retained captures |
| --- | --- |
| Entry | `.e2e-state/tmp/stage03-entry-20260725T061146+0800/dependency-delta-{a,b}.json` |
| Earlier exit | `.e2e-state/tmp/stage03-exit-20260725T120000+0800-019f9765/dependency-delta-{a,b}.json` |
| Final | `.e2e-state/tmp/stage03-final-20260725T122000+0800-019f977b/dependency-delta-{a,b}.json` |

All six files were byte-identical with SHA-256
`1c77ccb2048f4c7383b0bbe6b45f5c999a88e79bcd2ef86ac2650d503e52be1d`.
Each records:

- 16 of 16 frozen Cargo invocations;
- 1,143 external package/version identities;
- 2,179 external feature pairs;
- 116 direct external manifest edges;
- exact zero external dependency delta; and
- a passing safe/std-only audit for `sandbox-runtime-layerstack-core`.

The comparator's overall `exact: false` is solely the approved internal
Stage 00 product-contract manifest/lock delta. No external package/version,
feature-pair, or direct-edge delta was introduced by Stage 03.

## Product source and helper audit

`git diff --check` passes for the complete product delta. The Stage 03 product
changes introduce:

- no new Cargo dependency or manifest surface;
- no production process launcher;
- no socket client or listener;
- no HTTP client, registry access, runtime download, or package installation;
- no system helper, service, daemon, or sidecar;
- no unsafe or FFI surface; and
- no mutable image selection.

The only newly added `Command::new("mkfifo")` occurrence is in
`crates/sandbox-runtime/workspace/tests/unit/overlay_capture.rs`. It is a
test-only raw-file-kind fixture and reuses a helper pattern already present in
that module. The portable core and candidate implementation contain only
`std::process::id()` calls used to derive owned temporary identities; they do
not launch processes.

## Test and benchmark harness audit

`git diff --check` passes for the complete test/benchmark delta. Bounded
subprocess use is restricted to:

- resolving and executing the prebuilt private candidate-publication probe;
- the existing runner-owned `docker cp` and `docker exec chmod` fixture
  injection seams; and
- bounded Git commands that capture source identity.

No Stage 03 test path performs `docker pull` or `docker build`, contacts a
registry, downloads a package, starts a system service, or adds a network
client/listener.

The local image resolved exactly as:

```text
ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
architecture: arm64
```

## Live quiescence

After the final campaign, independent inspection found:

- no Docker container;
- no Stage 03 benchmark runtime entry;
- no Stage 03-owned benchmark, gateway, or daemon process;
- no Stage 03-owned TCP listener; and
- zero active owned resources and zero unexplained residue in the strict
  campaign artifact.

Three PPID-1 gateways already present before Stage 03 remained untouched:
PID 14966 on port 17878, PID 23296 on port 7878, and PID 53713 on port 17978.
They are explicitly outside Stage 03 custody.

## Closure

`S03-D01` and `S03-V46` pass. Stage 03 remains std-only in its portable core
and adds no external dependency, helper, service, image, or network surface.
Full multi-host/filesystem release qualification remains
`DEFERRED_STAGE_07`.
