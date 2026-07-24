# Stage 06 — reversible candidate authority

Status: specification only.

Normative dependencies:

- [implementation index](../index.md)
- [minimal storage contract](../layerstack_storage_contract.md)
- Stages 03–05 complete
- [Preparation 04](../../prep/04-seqcdc-space-time-complexity-and-acceptance-criteria.md)

## 1. Outcome

Stage 06 makes one candidate branch head the public publication authority while
retaining a tested path back to legacy v1 read **and write** authority. There is never
more than one public writer.

A single atomic top-level `CONTROL` contains format version, authority mode/epoch,
rollback eligibility, and an optional active migration-operation ID. Migration
cursor, bounded v1↔v3 correspondence/coverage proof, and detailed recovery state remain
in that common operation's `STATE`/`work`. Existing v1 artifacts remain in their
current paths, and ordinary locator/source leases protect them when required. There is
no `refs/legacy`, new legacy directory, or continuous legacy-shadow control family.

The complete migration-time path layout is
[the canonical `/eos` tree](../layerstack_storage_contract.md#4-complete-eos-ownership-and-storage-tree).

## 2. Compatibility window

Until Stage 07 retirement:

- the v1 reader/writer and required v1 artifacts remain intact;
- candidate branch/checkpoint refs continue to retain their atomic
  `{RootId,AttributionRootId}` snapshots even while v1 is public;
- candidate publication accepts only logical capabilities that can be represented by
  the supported v1 rollback builder, or marks rollback ineligible and therefore cannot
  become/continue public while rollback is a non-negotiable gate;
- every legacy-only payload needed by retained candidate roots remains protected until
  independently evacuated;
- authority changes are fenced by `CONTROL.authority_epoch`;
- sessions admitted under an old epoch retain their immutable route/leases until
  completion; new admissions use the new epoch.

Provider/backend location never affects v3 identity.

## 3. Forward cutover

1. Enter a migration operation and quiesce/fence new v1 publication admissions.
2. Let admitted v1 publications reach terminal state.
3. Import the final v1 state through the ordinary Stage 03 v3 publication pipeline
   (`O(R+E)` first import is allowed), producing both content and attribution roots.
   Preserve attribution for paths unchanged from the retained candidate snapshot and
   apply the caller-supplied stable logical migration/publication `ActorId` to changed
   paths. Record exact v1-manifest↔candidate-snapshot correlation in bounded migration
   operation work.
4. Materialize the candidate root and verify exact logical parity through public APIs.
5. Prove every retained candidate root has a safe selected locator or
   source-protection lease, and persist the migration cursor/coverage proof in the
   migration operation `STATE`.
6. Under the writer/authority lock, participate in the GC barrier and atomically replace
   `CONTROL` with `{format_version,authority=candidate,new_epoch,
   rollback_allowed=true,active_migration_operation_id}`.
7. Resume publications through the candidate branch only.
8. Repair a lost response from the authority epoch and migration operation; never
   repeat the cutover as a new publication.
9. After the operation is terminal, atomically clear
   `CONTROL.active_migration_operation_id` if the same authority epoch still names
   that operation. This cleanup does not advance the authority epoch.

V1 remains unchanged and non-authoritative after the switch. It need not be continuously
updated.

## 4. Public candidate publication

The Stage 03 branch-head commit, which atomically advances content root, attribution
root, generation, and publication ID, is the only public publication linearization
point. Response recovery, OCC, checkpoints, reset/revert, and GC barrier rules are
unchanged. Authority code does not add another receipt, generation, head, or
transaction.

At admission, a request captures authority epoch. Before head commit it verifies the
same epoch and candidate authority. Epoch change yields a typed retry; work may remain
private and later be reaped.

Public checkout selects a branch/session; it does not change authority. Checkpoint and
MCTS refs remain private policy state unless an explicit head promotion CAS makes a
branch public.

## 5. Authority rollback to v1

Rollback may be cold `O(R+E)`; it is not required to be `O(1)`.

1. Create/open a stable rollback operation and acquire the authority fence.
2. Quiesce candidate admissions and drain admitted commits.
3. Snapshot expected
   `{candidate_root,candidate_attribution_root,candidate_generation,authority_epoch}`.
4. Verify the root is v1-representable and all logical objects/locators are available.
5. Reconstruct it into private v1 staging with bounded memory, using internal Rust
   filesystem operations only.
6. Verify exact parity and sync the complete v1 carrier/metadata/manifest candidate.
7. Publish the v1 manifest atomically while routing still names candidate authority.
8. Recheck the expected candidate head/epoch and persist the reverse-coverage proof in
   the rollback operation `STATE`. Under the writer/authority lock replace `CONTROL`
   with `{format_version,authority=legacy,new_epoch,rollback_allowed=true,
   active_migration_operation_id}`.
9. Persist the terminal rollback outcome, then atomically clear
   `CONTROL.active_migration_operation_id` if the same authority epoch still names
   that operation. This cleanup does not advance the authority epoch.
10. Resume v1 publication. The retained candidate snapshot and attribution graph remain
    protected; v1 reconstruction does not rewrite or delete them. Candidate private
    validation/import may continue only through the normal Stage 03 protocol.

A crash before step 8 leaves candidate authority and a recoverable prepared v1 result.
A crash after step 8 leaves v1 authority. No candidate commit can interleave between
the selected-root check and switch. Lost response reads `CONTROL` and the operation.

Forward cutover after rollback repeats §3; it never assumes stale candidate/v1 parity.
Any v1 writes since rollback are imported as changed paths with their caller-supplied
stable logical `ActorId`; unchanged paths structurally reuse the retained attribution
pages. V1 storage is not extended with a second attribution database merely to make
rollback possible.

## 6. Read rollback and sessions

An operator may request legacy read mode only as part of the authority rollback above
or a non-public diagnostic against a named verified v1 artifact. Merely routing reads
to stale v1 while candidate remains the writer is not authority rollback and must not
be reported as such.

Sessions use the immutable route captured at admission. Existing sessions finish with
their leases or are explicitly drained by rollout policy. A route switch never mutates
an active session's mount plan.

## 7. Failure and recovery

| Failure boundary | Authority after restart | Recovery |
| --- | --- | --- |
| forward import/materialization incomplete | legacy | resume/reap exact operation |
| candidate ready, before `CONTROL` | legacy | reverify parity/heads and retry |
| after candidate `CONTROL`, before response | candidate | return committed epoch |
| candidate publication during rollback quiesce | old complete head only | drain or typed fenced retry |
| v1 rollback build incomplete | candidate | resume/reap; no route change |
| v1 manifest published, before `CONTROL` | candidate | recheck head/epoch and finish or discard prepared v1 |
| legacy `CONTROL`, before response | legacy | return committed epoch |
| corrupt/missing coverage or locator | unchanged | fail closed; retain both stores |

No boot logic infers authority from newest mtime, directory contents, or which manifest
exists.

## 8. Complexity, space, and bounds

- forward first import or rollback reconstruction: streamed `O(R+E)`;
- authority switch: bounded atomic metadata under lock;
- normal candidate publication: unchanged Stage 03 incremental bound;
- authority rollback reconstructs content into v1 but retains the candidate
  attribution graph; re-cutover attribution work is included in the streamed import;
- warm execution: unchanged Stage 04 native route;
- rollback staging and legacy/candidate overlap count against Preparation 04 peak space;
- migration operations, correspondence runs, retry outcomes, sessions, workers,
  buffers, FDs, mappings, and quiesce duration are explicitly
  bounded/backpressured;
- no continuous reverse-copy queue, cursor history, or duplicate current tree is kept
  merely for fast rollback.

## 9. Exit criteria

- [E2E plan](e2e_test.md) passes forward cutover, candidate publication, genuine
  authority rollback, re-cutover, failpoints, and session fencing;
- [benchmark note](benchmark_note.md) records cutover/rollback/overlap/tail results;
- one and only one public writer exists at every epoch;
- all public roots remain v1-representable until retirement approval;
- lost-response retry returns the committed authority epoch/result;
- legacy artifacts remain complete and protected;
- attribution remains queryable from retained candidate refs across rollback and is
  correctly extended on re-cutover after intervening v1 writes;
- no new legacy directory or legacy ref class exists;
- no unsupported environment/dependency is introduced.
