# Final storage-design refinement

> Status: Execution specification  
> Scope: sequential review and documentation finalization; no code implementation

This packet turns the final-review prompt into six gated phases. Each phase
consumes the previous phase's approved output. A later phase may return work to
an earlier phase, but it may not bypass a failed gate.

## Read first

1. Goal objective:
   /Users/yifanxu/.codex/attachments/2fdad60a-7bc9-415d-90cb-19f22186dca0/goal-objective.md
2. System-design draft:
   /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/system-design
3. Proof-of-concept code, for evidence only:
   /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox
4. Repository instructions:
   /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/AGENTS.md
   /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/CLAUDE.md

## Operating rules

- Architecture and documentation only. Do not implement production code.
- Phases 1 through 4 are read-only for the ten authoritative design documents.
- Phase 5 edits only the ten authoritative design documents and its own Handoff
  record.
- Phase 6 audits the design and may change only status, provenance and its own
  Handoff record.
- Each phase owner may update only the Handoff record in that phase's
  specification. Those records are process notes, not design authority.
- Preserve unrelated user changes.
- Subagents are allowed. Give each one a bounded scope and require source or
  file evidence. The lead agent reconciles all disagreements.
- No phase may convert an estimate, target, or external result into an achieved
  project measurement.
- If a hard requirement is impossible, report the incompatibility and choose a
  fail-closed capability contract. Do not silently weaken it.

## Absolute prohibitions

- No database of any kind.
- No SQLite, redb, RocksDB, LevelDB, LMDB, sled, Fjall, SQL service, KV engine,
  or embedded database.
- No recreated database surface: WAL, MVCC, arbitrary KV operations, generic
  transactions, mutable page allocation, buffer pools, or compaction levels.
- No reflink use, including optional fast paths.
- No FUSE.
- No additional administrative or storage capability, including CAP_SYS_ADMIN.
- No correctness dependency on OverlayFS, snapshots, one host filesystem,
  memory-backed workspaces, or a persistent cache.

A retained catalog must be a fixed-purpose immutable typed index file. It is
not a database and must not expose a general database or KV interface.

## Locked semantic baseline

- Docker OCI works now; WASI and Firecracker remain replaceable future adapters.
- Canonical identity is independent of backend locations and runtime state.
- A checkpoint pins the sandbox's committed full state, never session changes.
- Multiple workspace sessions may run concurrently on one sandbox.
- Publication uses the session's exact origin StateId and monotonic head token.
- Fork is checkpoint-bound, quiescent, nested, and operationally detached.
- The parent remains writable; there is no freeze mode.
- Rollback, fork commit, and destroy require the documented quiescence.
- Fork and rollback history are not public storage state.
- An acknowledged root may not silently roll back during recovery.
- Resources are admitted before use and have finite aggregate bounds.
- Cache-off operation is the baseline.

The existing system requirements and API methods are nearly locked. Change
them only to repair a demonstrated contradiction.

## Sequential phases

| Phase | Specification | Owner | Required output |
|---:|---|---|---|
| 1 | [Read-only architecture review](phase_1_architecture_review.md) | Lead reviewer | Architecture Review Packet |
| 2 | [Primary-source research](phase_2_primary_source_research.md) | Research lead | Research Decision Packet |
| 3 | [Resource and scale review](phase_3_resource_scale_review.md) | Resource reviewer | Resource Safety Packet |
| 4 | [Review handoff](phase_4_review_handoff.md) | Lead reviewer | Writer Handoff |
| 5 | [Writer finalization](phase_5_writer_finalization.md) | Separate writer | Writer Completion Packet |
| 6 | [Final acceptance audit](phase_6_acceptance_audit.md) | Independent auditor | Acceptance Report |

At most one phase is authoritative at a time:

    NOT_STARTED -> IN_PROGRESS -> PASS
                               -> BLOCKED
                               -> RETURN_TO_PHASE_N

Phase 5 cannot start until Phase 4 passes. Phase 6 cannot mark the design
Accepted while any blocker remains.

## Handoff-record protocol

Every phase specification ends with an append-only Handoff record. The phase
owner completes it after evaluating the phase gate.

Each attempt records:

- owner task path, session ID and timing;
- subagent task paths, session IDs and contributions;
- synthesis;
- research and evidence used;
- decisions and results;
- blockers or returned work;
- files changed;
- output packet for the next phase;
- gate result and whether the next phase may start.

On a rerun, append a new Attempt section. Do not overwrite an earlier attempt.
The record must contain enough information for the next agent to continue
without repeating the phase. Large evidence matrices may remain in the
referenced task transcript, but the decisions, blockers and source locations
must be summarized in the record.

A next phase may start only when the preceding record says:

    Status: PASS
    Next phase may start: YES

## Authoritative design documents

The writer may edit exactly these ten files:

| Document | Authority |
|---|---|
| ../index.md | Navigation, selected design, counts, evidence and provenance |
| ../system_requirements.md | Hard gates, prohibitions and resource bounds |
| ../api_methods.md | Public API and lifecycle contracts |
| ../architecture/overall_architecture.md | Selected architecture and tournament |
| ../architecture/mpla_demonstrations.md | Visual and comparative proof |
| ../components/canonical_state.md | Canonical identity, facts and attribution |
| ../components/durable_store.md | Objects, physical index, commit, recovery and GC |
| ../components/workspace_engine.md | Projection, capture and candidate construction |
| ../components/lifecycle_engine.md | Sessions, checkpoints, rollback and forks |
| ../components/backend_adapters.md | Docker, WASI and Firecracker boundaries |

This refine packet adds seven process specifications. Therefore final file-count
acceptance is:

- exactly ten authoritative design documents;
- exactly seven refine specifications;
- no other new system-design documents.

## Required final classifications

Every named item must be classified as exactly one of:

- self-implemented algorithm;
- self-implemented crash or durability protocol;
- lifecycle transition;
- composed workflow;
- adopted standard or library operation;
- qualification or test procedure.

Only the first two categories belong in the custom-mechanism count.

Every retained custom mechanism must state:

- owner and replacement interface;
- invariant;
- inputs and outputs;
- pseudocode when non-trivial;
- linearization or durability point;
- crash and replay behavior;
- worst-case time, memory, disk and FD bounds;
- primary optimization target;
- adoption-versus-custom decision;
- evidence and rejection of simpler alternatives.

## Leading candidates, not locked decisions

The prior review found these candidates worthy of final adjudication:

- five domain ownership boundaries plus one permit-only Resource Governor;
- one Lifecycle authority for public mutations;
- a fixed canonical typed envelope and StateId equal to ObjectId(StateManifest);
- a canonical compressed Merkle Patricia directory;
- one shared bounded external-merge facility;
- fixed-size chunks versus a frozen FastCDC profile;
- an adaptive immutable CoW B+ catalog with sparse path-copy and dense rebuild;
- bounded batch lookup and segment-offset coalescing;
- sealed immutable payload segments with checksummed trailer directories;
- exact disk-backed GC with maintenance headroom;
- explicit portable and Linux filesystem-fact profiles;
- capability-qualified quotas and runtime resource enforcement.

The reviewer must accept, replace, or reject each candidate. The writer must
not receive unresolved alternatives.

## Task provenance

| Role | Task path | Session ID |
|---|---|---|
| Parent coordinator | /root | 019fbe4c-0a9c-75a2-b767-07cd3f8f653f |
| Contract review | /root/contract_invariant_review | 019fbfba-f9d1-7303-9b99-de33bb149a60 |
| Algorithm/resource research | /root/algorithm_resource_review | 019fbfba-ce89-7c22-bf1c-04444acc0b3f |
| Physical-index research | /root/index_primary_research | 019fbfca-2ede-7882-8438-c46b32ce1864 |
| Portability review | /root/portability_simplicity_review | Runtime exposed no numeric session ID |

The Phase 6 auditor appends all new reviewer, subagent, writer and auditor task
paths and session IDs to the authoritative ../index.md.
