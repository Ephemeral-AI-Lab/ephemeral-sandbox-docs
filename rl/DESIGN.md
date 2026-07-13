# RL Rollout Flexibility Demo — Design Draft

## Objective

Demonstrate one infrastructure capability, expressed through two rollout topologies:

> EphemeralOS stores the immutable base workspace once, while allowing RL workloads to choose the isolation and density model that fits each batch.

The `O(1)` claim applies only to the physical base payload as rollout count `N` increases. Per-rollout metadata and copy-on-write changes still grow with `N`.

## Audience takeaway

Within 30 seconds, a viewer should understand that:

1. Both modes reference one content-addressed immutable base.
2. Mode A launches `N` parallel sandboxes for stronger boundaries.
3. Mode B launches `N` workspace sessions for higher density.
4. Switching modes changes orchestration and private overhead, not the base-layout invariant.
5. A credible capacity claim must show measured physical bytes, rollout throughput, isolation, and reclamation.

## Storyboard

### 1. Hero: one invariant, two execution shapes

Show one base object at the bottom and a mode switch above it. The upper topology changes between sandbox containers and workspace sessions, while the base object remains visually fixed and labeled `1 physical copy`.

Primary statement: **One base layout. Two rollout modes.**

### 2. Flexibility switch

Provide two selectable modes:

| Mode | Topology | Shared state | Private state | Best fit |
| --- | --- | --- | --- | --- |
| A | `N` parallel sandboxes | Docker image layers and content-addressed workspace base | Container writable state, scratch volume, LayerStack metadata, COW delta | Untrusted, heterogeneous, or failure-sensitive rollouts |
| B | `N` sessions in one sandbox | One LayerStack and the same lower paths | Session upperdir, workdir, holder, lease, COW delta | Dense, homogeneous rollout batches |

Changing the selector must update the topology diagram, modeled overhead, formula, and recommendation without changing the base-copy counter.

### 3. Interactive storage model

Inputs:

- parallel rollout count `N`
- base payload size `B`
- mean private COW delta `Δ`
- rollout topology

Outputs:

- base copies: always `1`
- physical base bytes: always `B`
- modeled private bytes: topology overhead plus `N × Δ`
- naive full-copy comparison: `N × B`
- base payload avoided versus full copies

Display the scope explicitly:

```text
Mode A: S(N) = B_shared × 1 + ΣΔ_i + N × sandbox_metadata
Mode B: S(N) = B_shared × 1 + ΣΔ_i + N × session_metadata + one_sandbox
```

This is an explanatory model, not benchmark evidence.

### 4. RL rollout loop

Connect the storage layout to agent training:

```text
policy checkpoint + task
  → fork isolated environment
  → observe / act / execute tools
  → verify and reward
  → collect trajectory
  → update policy
```

Show that both topologies emit the same trajectory contract: observations, actions, tool traces, log probabilities, rewards, termination reason, base digest, and private-delta bytes.

### 5. Live proof plan

The production demo should run the same workload in both modes at `N = 1, 8, 32, 128, 256` and collect:

- physical allocated bytes for the base object
- total private bytes
- p50/p95 environment-ready latency
- completed trajectories per minute
- cross-rollout marker leakage
- bytes remaining after cleanup

Acceptance gates:

- base physical bytes remain within ±1% across `N`
- base digest and physical object identity remain unchanged
- deliberate writes appear only in the originating rollout
- private growth tracks writes and topology overhead, not `N × B`
- cleanup returns allocated private bytes within 1% of baseline

Run a read-only batch first, then a controlled-write batch. Report Mode A and Mode B side by side rather than presenting one as universally superior.

## Prototype structure

- `index.html` — interactive narrative and capacity model covering both modes
- no build step or external runtime dependencies
- responsive desktop/mobile layout
- reduced-motion support and semantic controls

## Accuracy guardrails

- Say `O(1) base payload storage`, not `O(1) total storage`.
- Separate modeled numbers from measurements.
- Note that overlay copy-up can make a private delta larger than the logical edit size.
- Do not imply the filesystem result also makes policy weights, inference memory, GPU memory, or trajectory storage constant.
