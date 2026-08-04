# LayerStack-0 and EphCoW branding

Date: **2026-08-04**  
Status: **Working brand language; architecture-aligned, not a replacement for the architecture contract**

This folder contains the smallest useful branding package for the storage
architecture behind Ephemeral Sandbox V2. It focuses on the architectural
innovation rather than logos, launch campaigns, or a large messaging system.

The engineering source of truth remains the V2
[architecture design](../architecture_design.md). The branding language in this
folder must change if it conflicts with that contract, the product
[PRD](../PRD.md), or a later proved implementation result.

## Brand architecture

```text
Ephemeral Sandbox                 the multi-agent sandbox product
└── LayerStack-0                  its sandbox Version engine
    └── EphCoW                    its multi-agent copy-on-write architecture
```

Use the names as follows:

- **Ephemeral Sandbox** is the product.
- **LayerStack-0** is the short public name for the V2 sandbox Version engine.
- **EphCoW** means **Ephemeral Copy-on-Write** and names the architecture that
  combines immutable Versions, zero-payload reference forks, isolated writable
  agent work, immutable admission, and strict OCC publication.
- Use `layerstack-0` and `ephcow` only where a lowercase code, metric, file, or
  command identifier is required.

“LayerStack-0” does not mean a preliminary release. The zero expresses the V2
storage model: an accepted Version has **zero required layer-chain depth**. It
is complete and immutable, not an instruction to reconstruct a base plus layers.

## Canonical message

> **Ephemeral branches. Immutable outcomes.**

Technical subline:

> **Zero-payload forks. Isolated writes. Strict publication.**

One-sentence description:

> LayerStack-0 lets parallel agents branch from one accepted immutable sandbox
> Version without copying its payload, work in isolated writable namespaces,
> and publish a new complete Version through one strict OCC Head transition.

Short product paragraph:

> LayerStack-0 is the sandbox Version engine for Ephemeral Sandbox. Its EphCoW
> architecture separates durable immutable Versions from temporary writable
> agent work. Forking or moving a reference to an already accepted Version
> reads, writes, and copies zero payload bytes. Each agent works privately; a
> checkpoint admits a complete immutable candidate, and one optimistic-
> concurrency transition decides whether that candidate becomes the new Head.

## The architectural idea

```text
                     one accepted Version
                              |
                   zero-payload reference forks
                +-------------+-------------+
                |             |             |
             Agent A       Agent B       Agent C
             private       private       private
              writes        writes        writes
                |                           |
           candidate A                 candidate C
                +-------------+-------------+
                              |
                    strict OCC publication
                              |
                         one new Head
```

The full explanation, before/after comparison, algorithm story, and honest
comparison with reflink are in
[architecture-innovation.md](architecture-innovation.md). Canonical brand and
architecture vocabulary is defined in [terminology.md](terminology.md).

## Language boundaries

Use these claims:

- “zero-payload reference fork”;
- “complete immutable Version”;
- “isolated writable agent namespace”;
- “content-addressed complete Version”;
- “one strict OCC Head transition”;
- “no layer-chain reconstruction”; and
- “designed for high-fan-out multi-agent sandboxes.”

Do not currently claim:

- that all end-to-end fork or namespace setup performs zero I/O;
- that writes or checkpoints are zero-copy;
- that LayerStack-0 is universally faster than reflink or native filesystem
  snapshots;
- that the selected R0 store shares chunks across different Versions;
- that CDC, a chunk DAG, or a custom lazy COW filesystem is selected;
- that historical Stage 4.6 results prove V2 performance; or
- that storage chooses the winning rollout, performs MCTS, or silently merges
  stale agent results.

The selected design currently gives `EphCoW` the precise meaning documented
above: **reference-level copy-on-write over complete immutable Versions, paired
with runtime-owned isolated writable namespaces**. Cross-Version CAS+CDC and a
custom COW data plane remain a separate architecture proposal and require Phase
01 to be reopened before they can become LayerStack-0 product claims.
