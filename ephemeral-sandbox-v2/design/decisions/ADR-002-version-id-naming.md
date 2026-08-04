# ADR-002 — `VersionId` is the LayerStack-0 content identity

Date: **2026-08-04**  
Status: **`ACCEPTED_PRODUCT_CONTRACT`**  
Scope: **V2 terminology, API types, storage-role examples, and migration maps**

## Decision

The typed identity derived from one complete canonical portable filesystem
value is named **`VersionId`** in LayerStack-0 V2 contracts.

The pre-implementation name `StateId` is superseded. Historical Phase 00,
Phase 01, and appendix documents may retain that spelling; when consumed by V2
implementation work, it maps semantically to `VersionId`.

## Type boundary

```text
Candidate
    -> validate and canonicalize
    -> derive VersionId
    -> LayerStack-0 admission
    -> AcceptedVersion
    -> AcceptedBinding
    -> Head or typed Root
```

`VersionId` may be derived before durable admission. It is a typed,
versioned, domain-separated content address, not proof that:

- an accepted Version exists;
- an occupied identifier contains equal bytes;
- a caller may create or move a durable reference; or
- the payload passed current-generation validation.

Only LayerStack-0 may create or revalidate `AcceptedVersion` and
`AcceptedBinding` evidence after normal admission. An occupied `VersionId`
requires comparison of the complete canonical bytes. Equal bytes reuse the
accepted payload; unequal bytes fail closed as a collision.

## Storage vocabulary

Conceptual layouts use:

```text
versions/<VersionId>/
    payload/
```

`versions/` is a logical role name and does not select CDC, Chunk
content-addressed storage, a manifest/object DAG, or a custom VersionView.
Under selected R0, each accepted entry is one complete filesystem-native
immutable payload closure. `payload/` makes the logical payload boundary
visible; exact root and directory spellings remain a Phase 03 choice.

## Architectural effect

This decision does **not** reopen Phase 01. It changes no selected-Version owner,
dependency direction, storage family, writer count, OCC point, crash behavior,
portable fact boundary, migration truth, or hard-rule mechanism. It only makes
the V2 product and API vocabulary consistent with LayerStack-0's accepted
immutable **Version** concept.

## Required propagation

- The product PRD and current architecture/design documents use `VersionId`.
- Phase 02 selects the exact digest and serialized representation under that
  type name.
- Phase 03 uses `VersionId` only through admission and accepted-binding APIs;
  it never treats a raw ID as admission evidence.
- Migration maps legacy selected views to `VersionId`, then uses ordinary
  LayerStack-0 admission to obtain an accepted binding.
- Heads and Roots store or resolve accepted bindings, not unchecked raw IDs.
- Historical evidence is annotated with the mapping instead of being silently
  rewritten.

## Rejected names

| Name | Reason |
|---|---|
| `StateId` | Technically neutral but inconsistent with the selected public Version model. |
| `WorkspaceId` | Conflicts with the mutable runtime Workspace identity. |
| `SnapshotId` | Collapses Version, Checkpoint, and filesystem-snapshot concepts. |
| `RootId` | Conflicts with typed durable Root identifiers. |
| `LayerId` | Reintroduces the legacy layer-chain model. |
| `ContentId` | Too generic and easily confused with proposed Chunk content addressing. |
| `CommitId` | Implies publication/history semantics that identity does not own. |

## Reopening condition

Reopen this decision if implementation evidence shows that the complete
canonical value needs more than one independent identity, or if product
semantics require a Version identity that is not content-derived. A different
digest algorithm, encoding, width, or display grammar remains Phase 02 work and
does not by itself reopen this naming decision.
