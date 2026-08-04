# Cluster 03 — Runtime access and materialization

## Purpose

This cluster defines how LayerStack-0 revalidates an AcceptedBinding, installs
bounded read custody, and hands immutable Version access to existing
runtime-effect owners. It separates zero-payload reference transitions from
activation and materialization paths that may move bytes.

## Reading order

1. [Read custody and runtime handoff](01-read-custody-and-runtime-handoff.md)
   closes the read/retirement race and preserves runtime ownership.
2. [Runtime materialization](02-runtime-materialization.md) defines protected
   immutable activation and bounded streaming construction of a runtime-private
   writable destination.

## Cluster invariants

- Accepted payloads are immutable and never become mutable upper/work storage.
- Mutable Workspace effects remain owned by existing runtime components.
- Every runtime use starts from an admission-issued or admission-revalidated
  AcceptedBinding and bounded custody.
- Activation and materialization payload I/O is accounted outside the
  reference `0/0/0` scope.
- Optional accelerators cannot become Version truth or required correctness
  mechanisms.

## Evidence and open choices

Existing runtime-effect ownership is `SOURCE-VERIFIED`; V2 custody,
materialization, and memory-bound algorithms are `INFERRED`; no V2 runtime
materialization result is `SPIKE-VERIFIED`. Phase 03 selects exact read handles,
custody, traversal, private-destination readiness, limits, and filesystem
qualification `OPEN_WITHIN_R0`.

## Backend evidence boundary

The portable seam is identical for every backend:

```text
AcceptedBinding -> admission revalidation -> immutable read custody
                -> direct accepted-Version handoff -> runtime-owned effects
```

| Runtime family | Backend status | Evidence label | Contract consequence |
|---|---|---|---|
| Current OCI/Docker/Linux path | current evidence only | `SOURCE-VERIFIED` | Proves current owner placement and motivates the adapter seam; it is not universal backend proof and contributes no portable identity field. |
| Firecracker | `OPEN_EVIDENCE` | `OPEN` | No implementation evidence was found; exact VM disk format, device model, adapter API, and materialization strategy remain unselected. |
| WASI/WASM | `OPEN_EVIDENCE` | `OPEN` | No implementation evidence was found; exact runtime, module/preopen mapping, adapter API, and materialization strategy remain unselected. |

Backend status is not an evidence label. OCI/Docker, VM, module, device,
snapshot, mount, namespace, and host-path identities remain below the
runtime-effect boundary. None may alter portable Version identity, Accepted
Version truth, direct AcceptedBinding handoff, ReferencePlane authority, or
Head OCC.

## API consumers

- [Runtime API](../../api/runtime.md)
- [Manager activation boundary](../../api/manager.md)
- [Shared API operation map](../../api/README.md#14-api-operation-to-algorithm-navigation)

Return `REOPEN_PHASE_01` if accepted-payload immutability, bounded custody, or
handoff to existing runtime owners cannot satisfy a hard rule without a new
writer, service, or storage representation.

[Back to package index](../README.md)
