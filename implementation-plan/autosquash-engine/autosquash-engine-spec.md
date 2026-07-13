# Layerstack Autosquash Engine Specification

Status: Proposed

## 1. Purpose

Layerstacks can accumulate immutable layers faster than operators manually squash them. The autosquash engine evaluates configured policies after a layer is committed and schedules the existing squash action when a policy matches.

Autosquash is not a public operation. It has no operation request, response, dispatch registration, or API endpoint. It is an internal scheduler owned by the layerstack domain.

The first policy is `squash_at_n_layers`. More policies can be added later without introducing a policy framework before it is needed.

## 2. Goals

- Allow an operator to enable autosquash at a configurable active-layer count.
- Keep publishing and session finalization off the squash critical path.
- Reuse the same squash plan, flatten, commit, remount, cleanup, and safety logic as manual squash.
- Preserve the current manual `squash_layerstack` API and response contract.
- Coalesce bursts without losing the final evaluation.
- Recover safely after process restart or interruption.
- Make the scheduling decision and the reused squash action observable in one trace.

## 3. Non-goals

- A new public autosquash operation or endpoint.
- Time-, size-, disk-pressure-, or tenant-based policies in the first version.
- Dynamic configuration reload.
- A generic policy trait, registry, plug-in system, or policy expression language.
- Changing the lower-level layerstack storage format or squash algorithm.
- Retrying a failed squash in a tight loop.

## 4. Configuration

```yaml
runtime:
  layerstack:
    autosquash_policies:
      squash_at_n_layers: 100
```

The configuration model is equivalent to:

```rust
struct AutosquashPoliciesConfig {
    squash_at_n_layers: Option<usize>,
}
```

Rules:

- If `autosquash_policies` or `squash_at_n_layers` is absent, autosquash is disabled.
- The shipped product configuration enables the policy with a default threshold of `100` active layers.
- Operators can override `100` with another valid value or disable the policy by omitting it from a custom configuration.
- `squash_at_n_layers` must be at least `3`. A smaller value cannot represent a useful squashable stack of base plus at least two newer layers.
- Unknown fields are rejected by configuration deserialization.
- Configuration is fixed for the daemon lifetime. A change takes effect after restart.
- When future policies are added, matching uses OR semantics: one or more matching policies request one shared squash action.

## 5. Layer-count semantics

The policy uses the current active manifest count, consistent with the existing `layer_count` meaning.

- The base layer `B` counts.
- Ordinary immutable layers `L` count.
- A previously squashed layer `S` counts.
- Temporary staging data and inactive historical layers do not count.
- The policy matches when `active_layer_count >= squash_at_n_layers`.
- The worker always reads the current manifest. It does not trust a count captured by a producer.

Example for `squash_at_n_layers: 3`:

| Active manifest | Count | Decision |
|---|---:|---|
| `B` | 1 | Below threshold |
| `B + L1` | 2 | Below threshold |
| `B + L1 + L2` | 3 | Schedule squash |
| `B + S1 + L3` | 3 | Schedule squash if a squashable block exists |

Matching the numeric threshold does not guarantee that the current lease boundaries permit a block to be squashed. In that case evaluation records `no_squashable_blocks` and leaves the manifest unchanged.

## 6. Resulting source structure

```text
ephemeral-sandbox/crates/sandbox-runtime/operation/src/layerstack/
├── actions/
│   ├── mod.rs
│   └── squash.rs
├── autosquash_engine/
│   ├── mod.rs
│   ├── worker.rs
│   └── policies/
│       ├── mod.rs
│       └── squash_at_n_layers.rs
├── error.rs
├── mod.rs
├── service.rs
└── service/
    └── impls/
        └── squash.rs
```

The architecture name is `autosquash-engine`; the Rust module uses the conventional underscore form `autosquash_engine`.

Responsibilities:

- `actions/squash.rs`: shared domain action containing the current storage squash and live-remount orchestration.
- `autosquash_engine/mod.rs`: construction, notification interface, startup evaluation, and shutdown ownership.
- `autosquash_engine/worker.rs`: bounded notification channel, coalescing, serialized evaluation, and action invocation.
- `autosquash_engine/policies/squash_at_n_layers.rs`: the one configured comparison and its validation.
- `service/impls/squash.rs`: the existing manual operation adapter; it authorizes and maps the shared result to the unchanged operation response.

The lower-level crate at `sandbox-runtime/layerstack` remains policy-free.

## 7. Components and interfaces

### 7.1 Autosquash notifier

Layer-producing paths receive a cheap cloneable notifier. Its notification call must not await evaluation or squash.

Each accepted notification contains:

- the originating trace context;
- `trigger_reason`, initially `layer_committed` or `startup`;
- a monotonic enqueue timestamp.

The notification queue has effective capacity one. If an evaluation is already pending, another notification is coalesced and a counter is incremented. The newest manifest will still be evaluated, so no layer-count transition is lost.

Disabled configuration constructs a no-op notifier and does not start a worker.

### 7.2 Worker

There is one worker per layerstack service instance. For each pending signal it:

1. Restores or links the accepted trace context.
2. Reads the live active manifest.
3. Evaluates configured policies.
4. Stops with `below_threshold` when no policy matches.
5. Acquires the shared squash-action gate when a policy matches.
6. Re-reads the manifest and re-evaluates after acquiring the gate.
7. Executes the shared squash action if a squashable block remains.
8. Records completion or failure and waits for another notification.

The worker does not hot-retry `failed` or `no_squashable_blocks`. A later real layer commit or daemon restart supplies the next evaluation opportunity.

The runtime owns worker shutdown and joins or cancels it cleanly during teardown.

### 7.3 Shared squash action

The body currently owned by the manual layerstack squash implementation moves into `actions/squash.rs`. Both callers use it:

```rust
enum SquashCause {
    Manual,
    Autosquash {
        policy: &'static str,
        threshold: usize,
        observed_layers: usize,
        trigger_reason: AutosquashTriggerReason,
    },
}
```

The action returns structured data sufficient for both callers, including:

- active layer count before and after;
- planned and committed squash blocks;
- remount sweep outcome;
- whether no squashable block existed.

The manual adapter maps this result to its current JSON response without a contract change. The engine uses the same structured result for scheduling telemetry.

The shared action owns the existing:

- lease-aware planning;
- flattening and staging;
- atomic manifest commit;
- live remount sweep;
- fault cleanup and staging removal;
- low-level per-root single-flight protection.

### 7.4 Action serialization

Manual and automatic callers share one process-level action gate.

- Autosquash waits for the gate in its background worker, then rechecks the policy and manifest.
- Manual squash preserves its current in-flight behavior by attempting the gate without waiting and returning the existing in-flight error when occupied.
- The lower-level per-root single-flight guard remains the final correctness boundary.

This prevents duplicate planning work while preserving manual operation behavior.

## 8. Trigger points

### 8.1 Sessionless amend

After a successful sessionless file write or edit creates an immutable `L` layer and audit recording succeeds, the path sends a nonblocking `layer_committed` notification.

No notification is sent when the request produces no new layer.

### 8.2 Implicit-session finalization

Finalization retains the `PublishChangesResult.no_op` result. When a real layer was published, it attempts finalized-session destruction first and then sends the notification.

The notification is deliberately outside the publish storage primitive and after the destruction attempt. Autosquash therefore normally observes the released lease, while destruction failure remains safe because lease-aware planning excludes the active boundary.

A publish that is deduplicated or reports `no_op` sends no notification.

### 8.3 Startup catch-up

After boot reap and remount sweep complete, and after the layerstack/session services are ready, the engine sends one background `startup` evaluation. This catches a stack restored above the configured threshold or an autosquash interrupted by a previous process exit.

### 8.4 Non-triggering changes

- An `S` layer committed by the squash action must not notify the engine.
- Reads, observations, exports, and discarded sessions do not notify it.
- A below-threshold evaluation does not schedule another evaluation.

## 9. Concurrency and failure semantics

- A producer's successful layer publish is independent of later autosquash success.
- Queue saturation never blocks or fails the producer; the notification is coalesced.
- At least one pending notification remains until the worker performs a later live-manifest evaluation.
- The worker rechecks after waiting for the action gate, preventing a stale decision from causing redundant squash.
- Process interruption may leave inactive artifacts, but the active manifest must remain atomic and readable under the existing squash guarantees.
- Startup cleanup and evaluation recover from an interrupted attempt.
- Autosquash failure emits telemetry and a daemon warning but does not change an already successful publish/finalize response.
- A failure does not delete active source layers or leak active staging references.

## 10. Observability contract

Autosquash is represented as an internal scheduled action, not as an operation.

### 10.1 Trace shape

```text
layerstack.autosquash.evaluate
└── layerstack.squash
    ├── layerstack.squash.plan
    ├── layerstack.squash.flatten
    ├── layerstack.squash.commit
    └── layerstack.squash.remount_sweep
```

`layerstack.autosquash.evaluate` attributes:

| Attribute | Values |
|---|---|
| `trigger_reason` | `startup`, `layer_committed` |
| `policy` | `squash_at_n_layers` |
| `threshold` | configured integer |
| `observed_layers` | active count read by the worker |
| `decision` | `below_threshold`, `trigger`, `no_squashable_blocks` |
| `queue_delay_ms` | enqueue to evaluation start |
| `coalesced_notifications` | notifications merged into this evaluation |

The existing `layerstack.squash` span gains `cause=manual|autosquash`. For autosquash it also carries `policy`, `threshold`, and `observed_layers`. Existing phase names and measurements are reused rather than duplicated.

The layer-commit trace context is propagated to the accepted evaluation. Startup evaluation is a root internal trace or is linked to the boot trace, depending on the existing runtime trace convention.

### 10.2 Events

| Event | Emission rule | Required fields |
|---|---|---|
| `layerstack.autosquash.triggered` | Once after a policy matches and the gate recheck still requires action | policy, threshold, observed layers, trigger reason, queue delay, coalesced count |
| `layerstack.autosquash.completed` | Once after a successful shared action | policy, threshold, before/after counts, blocks committed, queue delay, squash duration, total convergence duration, coalesced count |
| `layerstack.autosquash.failed` | Once when evaluation/action fails | policy, threshold, observed layers, error, queue delay, elapsed duration |

Failure sets the active span status to error and also logs a warning. Disabled and below-threshold cases do not emit lifecycle events; the evaluation span is sufficient. Individual coalesced notifications do not emit events.

## 11. Acceptance criteria

1. The shipped product configuration enables autosquash at `100` active layers; omitting the policy disables it and leaves manual squash behavior unchanged.
2. Invalid thresholds below `3` and unknown policy keys fail configuration validation.
3. At exactly `N` active layers, a background evaluation eventually invokes the shared squash action.
4. Layer publish acknowledgement does not await autosquash evaluation, gate acquisition, flattening, commit, or remount.
5. Burst notifications are coalesced without losing the final above-threshold evaluation.
6. Manual and automatic squash produce equivalent storage results through the same action implementation.
7. Existing manual squash request, response, error, and observability behavior remains compatible, apart from the new `cause` attribute.
8. Active session leases remain authoritative, and remount/reclamation behavior is identical to manual squash.
9. A no-op publish and an autosquash-created `S` layer do not recursively trigger autosquash.
10. A failed autosquash cannot turn an already successful write/finalize request into a failure.
11. Startup evaluates and converges an already over-threshold stack.
12. Successful, skipped, coalesced, and failed decisions are distinguishable through the specified spans, events, attributes, and warnings.

## 12. Deferred extensions

When a second real policy is implemented, add its optional configuration and evaluation beside `squash_at_n_layers`. Introduce a trait or registry only if the implementations demonstrably need different dependencies or lifecycle behavior.
