# R0 resources, security, and observability

**Status:** `LOCKED_PHASE_01` ownership and boundedness; exact limits are
`SELECT_IN_PHASE_02` or `SELECT_IN_PHASE_03`

**Selected architecture:** [R0](../architecture_design.md)

## Purpose

R0 is valid only if untrusted input, transient work, persistent populations,
and recovery debt remain finite. This document assigns accounting and proof
responsibility without inventing exact limits before measurement. It also fixes
the security boundary and ensures observability remains diagnostic rather than
a second selected-Version authority.

Product [hard rules](../PRD.md#hard-rules-must-never-break) and the root
[architecture design](../architecture_design.md) take precedence. Phase 00
resource values are [proposals](../phases/00-freeze-rules/SPEC.md#9-resource-envelope-proposals),
not V2 limits or pass/fail gates.

## Resource principles

1. Every attacker- or workload-controlled input and population has one
   accounting owner, a finite configured or coded limit, and a typed rejection.
2. Capacity is reserved or precharged before expensive or durable private work
   where feasible; a reference is never published on uncertain capacity.
3. Canonicalization and payload transfer are streaming/bounded; Version size does
   not imply holding all file bytes in memory.
4. Concurrency limits cover aggregate memory, scratch, descriptors, and workers,
   not only per-request input size.
5. Cancellation, timeout, collision, stale OCC, ENOSPC, I/O error, and crash all
   have deterministic idempotent cleanup.
6. A crash may leave only recognizable bounded private debt. Excessive or
   ambiguous debt fails readiness closed.
7. Caches, indexes, and counters are bounded aids, not selected-Version truth.
8. No exact finite value in this document is selected; Phase 02 and Phase 03
   must choose and test their respective constants.

## Accounting ownership matrix

| Resource/population | Accounting owner | Selection phase | Required admission/lifecycle behavior | Required evidence |
|---|---|---:|---|---|
| Candidate total canonical/payload bytes | Pure identity validation for semantic limit; store for physical reservation | 02 + 03 | Reject before publication; stream within aggregate budget | Limit−1/limit/limit+1 and oversized-stream tests |
| Entry count and entry-type count | Phase 02 identity module | 02 | Validate while decoding/enumerating; no unbounded collection | Boundary and malformed-count tests |
| Relative path bytes, component count, and depth | Phase 02 identity module | 02 | Normalize and validate before use as a store-relative target | Boundary, traversal, alias, and encoding tests |
| Symlink-target bytes | Phase 02 identity module | 02 | Record as bytes/facts only when accepted; never follow during identity/admission | Boundary and escape fixtures |
| Metadata per entry and total metadata | Phase 02 identity module | 02 | Explicit accepted grammar; reject unsupported/unbounded classes | Golden and over-limit vectors |
| Canonicalization working memory and buffers | Phase 02 identity module | 02 | Fixed/bounded buffers or a documented bounded ordering structure | Peak-memory measurement and adversarial ordering test |
| Simultaneous canonical streams/admissions | Store owner | 03 | Acquire aggregate permit/reservation before work; cancellation releases it | Saturation and cancellation tests |
| Staging transactions and staged disk bytes | Store owner | 03 | Precharge/reserve against a finite store budget; private names remain recognizable | ENOSPC, saturation, crash, and cleanup tests |
| Accepted payload population/physical disk | Store owner plus lifecycle capacity policy | 03 | Admit only under capacity policy; retirement is exact, bounded, and safe | Capacity rejection and reachability tests |
| Fixed-Root and Head count | Store owner | 03 | Typed namespace with a finite configured scope; atomic create and exact conditional remove for both record kinds, with exact conditional replacement only for Heads | Count boundary, lifecycle-policy, and restart tests |
| Active read custody | Store owner | 03 | Finite acquisition; release on normal, error, timeout, and cancellation paths | Saturation and last-root race tests |
| Open payload/control descriptors | Store owner | 03 | Bounded pool/request custody; close on every terminal path | FD snapshots before/after stress and injected failure |
| Worker/task count and queued work | Store owner | 03 | Fixed or explicitly bounded concurrency/queue; no detached untracked tasks | Saturation, cancellation, shutdown, and restart tests |
| Staging/orphan/retirement debt | Store owner | 03 | Recognizable, finite ceiling, idempotent bounded cleanup batches | Repeated crash and cleanup-plateau tests |
| Recovery work per startup/batch | Store/lifecycle owner | 03 | Readiness budget and debt ceiling; fail closed rather than scan forever | Maximum-population and excessive-debt startup tests |
| Diagnostic series/cardinality | Observability owner consuming bounded LayerStack-0 projections | 03–04 | No raw Version IDs, paths, Root IDs, or tenant-controlled strings as unbounded labels | Cardinality/source audit |
| Application request and live-workspace limits | Existing application/effect owners | 04 | Existing auth/order and workspace budgets remain outside store truth | Product integration/resource tests |
| Migration scratch/progress | Temporary importer and lifecycle owner | 05 | Uses normal V2 admission budgets; independently finite and deletable | Import retry/crash/resource tests |

LayerStack-0 is responsible for aggregate Version-storage budgets even when
the candidate is supplied by an application, workspace, or importer. Callers
cannot bypass store admission by claiming they already validated capacity.

## Reservation and cleanup lifecycle

The normal candidate path should follow this resource lifecycle:

```text
validate cheap structural limits
  -> acquire bounded admission/concurrency permit
  -> reserve scratch/disk and relevant memory/FD budget
  -> stream canonicalize/hash/build private staging
  -> exact occupied-ID comparison or new payload admission
  -> publish small reference under OCC, if requested
  -> release reservations and remove private temporaries
```

Required cleanup behavior by terminal path:

| Terminal path | Reference effect | Cleanup obligation |
|---|---|---|
| Invalid/unsupported candidate | None | Release all acquired permits/buffers/descriptors; no durable private state |
| Limit or capacity rejection | None | Release reservation; report typed finite-resource error |
| Digest collision | None | Remove private candidate material or record only bounded recognizable debt |
| Equal accepted payload reused | None unless a separate authorized publish succeeds | Remove unnecessary staging; decrement reservations |
| Stale OCC after admission | Head unchanged | Complete orphan may remain only as accounted bounded retirement debt |
| I/O error or ENOSPC | No success acknowledgement | Remove partial private state or leave recognizable bounded debt |
| Cancellation/timeout | No head mutation unless durable transition already linearized | Resolve outcome explicitly; release request-local resources; cleanup idempotently |
| Process crash | Prior or complete new truth | Startup classifies and cleans/quarantines bounded recognizable debt |
| Successful publication | One complete new head | Remove temporaries and release every transient reservation |
| Successful reference-only move | Small record only | Payload counters remain zero; release metadata resources |

Cleanup must converge under repeated interruption. A cleanup implementation may
use bounded batches, but it may not require an unbounded background worker,
cache, scanner, or persistent refcount as correctness authority.

## Security and untrusted-input rules

All candidate facts, selector/root names, legacy bytes, configuration paths,
and persistent bytes read during startup are untrusted until validated.

### Portable path and entry rules

- Canonical paths are normalized relative paths under one defined Phase 02
  grammar.
- Reject absolute paths, empty/ambiguous components where forbidden, `..`
  traversal, alternate separators, ambiguous encodings, duplicate canonical
  names, case/normalization aliases forbidden by the grammar, and paths beyond
  the selected byte/component/depth limits.
- A path is a portable fact, not permission to concatenate and access an
  arbitrary host path.
- Symlink targets may be represented only under the explicit portable grammar;
  identity and admission never follow them.
- Hard links, devices, sockets, FIFOs, sparse/extents, xattrs, ACLs, ownership,
  timestamps, modes, and other metadata classes must be explicitly included
  and canonicalized or explicitly rejected. Host enumeration must not
  accidentally decide the identity grammar.
- Runtime-private Docker/OCI identifiers, OverlayFS paths/whiteout operations,
  mount or namespace IDs, host absolute paths, workspace/session IDs, PIDs,
  FDs, leases, auth, audit, rollout, local payload paths, and legacy parent/depth
  facts are forbidden from portable identity.

### Filesystem access rules

- Phase 03 must select descriptor/path-resolution primitives that confine all
  access below the configured store or candidate root and resist symlink escape,
  path replacement, and time-of-check/time-of-use substitution.
- Store control names, head selectors, root kinds/IDs, transaction IDs, and
  encoded `VersionId`s are typed and validated; none is interpreted as an
  unchecked path fragment.
- Atomic operations that depend on one-filesystem topology must reject a
  cross-filesystem configuration rather than silently fall back to copying.
- Accepted payload custody is read-only through product/store APIs. A writable
  workspace is built and owned by runtime-effect code; it is never the accepted
  payload itself.
- Unknown versions, malformed lengths, checksum/integrity failures, digest/byte
  mismatch, dangling references, and ambiguous collision state fail closed.
- Cleanup may delete only recognized private/dead objects after exact
  reachability and custody checks. It must not infer liveness from age alone.

### Authority rules

- Application services own authorization, revocation ordering, and disclosure;
  the store does not become an auth policy engine.
- Only the store owner creates accepted bindings or mutates durable roots/heads.
- Observability cannot publish, repair, retire, or bless a Version.
- Raw digests supplied by callers are not accepted bindings.
- MCTS/search policy and runtime mount/namespace authority stay outside storage.
- Migration uses the ordinary V2 validation/admission/reference path and never
  gains a second write path into selected truth.

Open product decisions `DEC-001`, `DEC-011`, `DEC-017`, and `DEC-018` remain
open. Diagnostics may support their eventual choices, but metrics or logs do
not resolve them.

## Diagnostic-only observability

Observability reports projections of store behavior and health. It is never
consulted to decide accepted identity, current head, reachability, collision
equality, recovery truth, or retirement safety. Durable diagnostics, if any,
remain side data and cannot become an alternative recovery log.

### Minimum store test/operations seam

| Signal | Required shape/use | Cardinality rule |
|---|---|---|
| Selected payload bytes read/written/copied by operation class | Proves reference-only zeros and explains candidate-bearing work | Fixed operation/result labels only |
| Admission outcomes | New, reused-equal, invalid, limited, collision, I/O/durability | Fixed outcome labels |
| Accepted payload count and physical bytes | Capacity and one-payload checks | Aggregate/gauged; no `VersionId` label |
| Root/head counts and operations | Capacity and lifecycle | Aggregate by bounded root kind, not raw root ID |
| OCC outcomes | Success, stale, no-op if explicitly defined | Fixed outcome labels; no selector string |
| Staging/scratch reservation and active transaction counts | Saturation, leak, and cleanup detection | Aggregate buckets only |
| Orphan, retirement, and recovery debt | Bounded-debt/readiness monitoring | Aggregate counts/bytes and fixed reason |
| Active read custody | Retirement safety/resource accounting | Aggregate count only |
| Open descriptors, workers, queue depth, and memory reservations | Resource plateau and saturation | Aggregate per bounded component |
| Cleanup outcomes | Removed, deferred-active, quarantined, failed | Fixed outcome/reason labels |
| Recovery/readiness failures | Corrupt, dangling, unsupported version/profile, excessive debt | Fixed reason labels |
| Collision events | Security/correctness alert and test oracle | Count only; identifiers belong in access-controlled bounded logs if needed |
| Transition gate wait/hold duration | Contention diagnosis, not correctness | Aggregate histogram with controlled buckets |

Incomplete measurement is represented as unknown/unavailable, never false
zero. In particular, payload-I/O zeros used as a hard-rule oracle require the
instrumented operation boundary to be complete and auditable.

### Logs, traces, and sensitive values

- Do not place file contents, canonical bytes, symlink targets, host paths,
  tokens, or secrets in ordinary logs/metrics.
- Version/Root/Head identifiers, tenant data, and Candidate paths must not become
  unbounded metric labels. If needed for diagnosis, emit them only to a bounded,
  access-controlled event/audit sink with explicit retention.
- Recovery diagnostics identify record class and typed failure without dumping
  untrusted bytes.
- Trace sampling and diagnostic export have finite queues, output limits, and
  drop/backpressure behavior. They cannot block or change selected-Version
  correctness.
- Observability failure must not grant readiness or cause a state transition.

## Boundary and failure tests

Phase 02 and Phase 03 must test each selected constant at `limit - 1`, `limit`,
and `limit + 1` where meaningful, plus malformed declarations that attempt to
overflow accounting. Tests must cover aggregate concurrency, not only one
maximal request.

At minimum:

- nested/deep, wide, oversized, duplicate, ambiguous, and unsupported entries;
- arithmetic overflow and declared-size/actual-size mismatch;
- saturation of concurrent admission, scratch, custody, descriptors, workers,
  roots/heads, and recovery debt;
- cancellation and every injected I/O failure after reservations are acquired;
- repeated crash/recovery/cleanup until resource counts plateau;
- mutation attempts against committed payload custody;
- symlink/path replacement races during candidate traversal;
- diagnostic cardinality and sensitive-data source audit; and
- reference-only operations with complete payload-byte accounting equal to
  zero.

Phase 06 reruns all Must resource/crash/security tests selected by earlier
phases on one frozen artifact; it does not substitute an unsealed benchmark.

## Readiness and operating posture

| Condition | Required posture |
|---|---|
| Configuration exceeds validated bounds or uses unsupported filesystem profile | Fail configuration/readiness before accepting mutation |
| Corrupt or dangling selected truth | Fail readiness closed; typed diagnostic; no heuristic repair |
| Recognizable private debt within configured ceiling | Bounded idempotent cleanup/quarantine, then readiness only if truth is unambiguous |
| Debt exceeds startup/batch ceiling | Fail readiness or remain explicitly not-ready; no unbounded startup scan |
| Resource budget exhausted during operation | Typed rejection before reference publication |
| Diagnostic exporter unavailable | Preserve correctness; apply bounded drop/backpressure policy |
| Metrics unavailable/incomplete | Report unknown; never convert missing measurement into zero/pass |

## Reopening conditions

Reopen Phase 01 if finite limits and exact cleanup cannot be implemented without:

- changing the selected owner or dependency direction;
- introducing an unbounded authority/cache/scanner/worker population;
- using runtime-private facts in portable identity;
- adding a required service, database, coordinator, helper process, or persistent
  refcount truth;
- weakening exact collision comparison, zero-payload-I/O reference operations,
  immutable committed custody, or fail-closed recovery; or
- moving auth, runtime effects, search policy, or observability into store
  authority.

Changing a measured finite constant, bounded queue implementation, metric
backend, safe path primitive, or diagnostic record encoding within these
boundaries is a Phase 02/03 local decision, not an architecture reopening.

## References

- [Product PRD](../PRD.md)
- [Selected architecture](../architecture_design.md)
- [Phase 00 resource proposals](../phases/00-freeze-rules/SPEC.md#9-resource-envelope-proposals)
- [Phase 02 identity contract](../phases/02-state-identity/PRD.md) and
  [tests](../phases/02-state-identity/test-perf.md)
- [Phase 03 store contract](../phases/03-state-store/PRD.md) and
  [tests](../phases/03-state-store/test-perf.md)
- [Concurrency, durability, and recovery](05-concurrency-durability-recovery.md)
- [Phase 06 qualification](../phases/06-prove-offline/test-perf.md)
