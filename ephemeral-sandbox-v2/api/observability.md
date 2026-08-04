# Observability API — fleet, runtime, and LayerStack-0 diagnostics

Date: **2026-08-04**  
Status: **DESIGN DRAFT — proposed Phase 04 public surface**

The observability family exposes bounded, read-only diagnostic views of the
sandbox fleet, runtime effects, and LayerStack-0. It is a reader of selected
truth, never the owner of a Version, Root, Head, Checkpoint, Workspace, or
lifecycle transition.

This file is subordinate to the shared [API contract](README.md), the product
[hard rules](../PRD.md#hard-rules-must-never-break), and the selected
[architecture](../architecture_design.md).

## 1. Family boundary

```text
manager / runtime / LayerStack-0 / Linux-effect owners
        |
        | bounded events, counters, and read snapshots
        v
sandbox-observability
  - correlate diagnostics
  - redact private data
  - enforce time/cardinality/response bounds
  - report uncertainty and partial collection
        |
        v
CLI / MCP / diagnostic HTTP response

observability -X-> create or retarget a Root or Head
observability -X-> admit, repair, retire, or delete a Version
observability -X-> authorize a product mutation
diagnostic cache -X-> selected-state authority
```

The implementation may retain bounded diagnostic logs, caches, indexes, and
metric state. Those artifacts must be reconstructible or safely disposable;
they cannot be required to determine which Version is accepted or selected.

## 2. Operation index

| Operation | Evidence label | V2 disposition | Required arguments | Optional arguments | Diagnostic scope |
|---|---|---|---|---|---|
| `snapshot` | `SOURCE-VERIFIED` | rewrite result | — | `sandbox_id` | One bounded current diagnostic sample for a sandbox, or a fleet sample when omitted |
| `trace` | `SOURCE-VERIFIED` | retain | `sandbox_id` | `trace_id=last` | One bounded request/operation trace |
| `events` | `SOURCE-VERIFIED` | retain | `sandbox_id` | `name`, `since_ms`, `last_n` | Filtered bounded event history |
| `resources` | `SOURCE-VERIFIED` | retain | — | `sandbox_id`, `window_ms=60000` | Resource sample for one sandbox, or fleet summary when omitted |
| `daemon` | `SOURCE-VERIFIED` | retain | `sandbox_id` | — | Daemon/process health and routing diagnostics |
| `topology` | `SOURCE-VERIFIED` | rewrite terminology | `sandbox_id` | — | Runtime and ownership relationships without making them portable identity |
| `cgroup` | `SOURCE-VERIFIED` | retain current Linux-specific diagnostics below the runtime-effect boundary | `sandbox_id` | `scope=sandbox`, `window_ms=60000` | Bounded Linux cgroup/resource diagnostics |
| `layerstack` | `SOURCE-VERIFIED` | rewrite semantics | `sandbox_id` | `workspace_id`, `window_ms=60000` | LayerStack-0 Version, reference, OCC, recovery, and cleanup diagnostics |

The family retains the eight current operation names. The result schemas for
`snapshot`, `topology`, and especially `layerstack` must stop presenting a
legacy layer chain, depth, or squash state as V2 truth.

## 3. Shared observability conventions

### 3.1 CLI spelling

```text
sandbox-observability-cli <operation> [arguments]
```

Unlike the runtime CLI, `sandbox_id` is an ordinary per-operation argument:

```text
sandbox-observability-cli snapshot [--sandbox-id SANDBOX]

sandbox-observability-cli layerstack \
  --sandbox-id SANDBOX \
  [--workspace-id WORKSPACE] \
  [--window-ms 60000]
```

Catalog and MCP fields use snake case; CLI flags use kebab case. The catalog
remains the semantic source for requiredness, defaults, and maximum bounds.

### 3.2 Read-only law

Every operation in this family is semantically read-only:

- collection may read authoritative records through owner-provided reader
  interfaces or snapshots;
- collection may update a bounded, non-authoritative diagnostics cache as an
  implementation detail;
- collection must not acquire a writer role, repair a malformed store, replay
  recovery, remove an orphan, renew a Root, publish a Candidate, or move a
  Head;
- a diagnostic endpoint must not become a hidden administrative mutation API;
  and
- observing a race may report `partial` or a bounded consistency marker, but
  must not freeze product progress merely to fabricate a globally atomic view.

Repair, recovery, and retirement are internal LayerStack-0 responsibilities.
If a future administrative control plane is required, it needs separate
authorization and architecture review; it does not belong behind these names.

### 3.3 Diagnostic consistency

One response states its collection quality explicitly:

| Field | Meaning |
|---|---|
| `observed_at` | Timestamp assigned to the diagnostic response |
| `scope` | Fleet, sandbox, daemon, Workspace, command, or LayerStack-0 view |
| `consistency` | `coherent_owner_snapshot`, `correlated_samples`, or `partial` |
| `partial_reasons[]` | Bounded redacted explanations for unavailable/expired sources |
| `window_ms` | Requested/effective aggregation window where relevant |
| `request_id` | Diagnostic request correlation identifier |

`coherent_owner_snapshot` means one owner supplied a coherent bounded read; it
does not promise an atomic snapshot across manager, runtime, kernel, and
LayerStack-0. `correlated_samples` explicitly means that separately sampled
owners may have advanced between reads.

### 3.4 Bounds and disclosure

All operations apply finite configured limits to response bytes, collection
time, event/trace count, path count, label count, and time windows. When a
result is truncated it reports that fact and, where useful, an opaque cursor
or aggregate—not an unbounded continuation held in memory.

The following are never public diagnostic fields:

- auth tokens, credentials, environment secrets, stdin contents by default,
  or unredacted command output outside the existing authorized command API;
- LayerStack-0 host storage paths, temporary paths, lock-file contents, raw
  control-file bytes, or full canonical payload bytes;
- `AcceptedBinding`, `HeadRevision`, recovery tokens, collision comparison
  bytes, or a digest supplied as an authority capability;
- namespace handles, file descriptors, mount table details, cgroup paths, and
  host paths beyond the minimum redacted operational display; and
- arbitrary file paths, Checkpoint IDs, Version IDs, Workspace IDs, command
  IDs, or request IDs as unbounded metric labels.

Opaque IDs may appear in an authorized bounded diagnostic response for
correlation. Metrics use aggregated or hashed/bucketed dimensions so their
cardinality remains bounded.

## 4. General diagnostic operations

### 4.1 `snapshot`

Capture a bounded diagnostic sample. This operation's name is retained for
compatibility, but a diagnostic Snapshot is **not** a stored Version and is
**not** a Checkpoint.

```text
sandbox-observability-cli snapshot [--sandbox-id SANDBOX]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `sandbox_id` | no | opaque string | Sample one authorized sandbox; omit for an authorized fleet summary |

The sandbox form may correlate:

- manager lifecycle/readiness;
- daemon availability;
- selected accepted `VersionId` correlation and fixed-Checkpoint count;
- active Workspace and command counts;
- bounded CPU, memory, I/O, and process summaries; and
- LayerStack-0 readiness, recovery-debt, and cleanup summaries.

The fleet form aggregates counts and health categories. It must not expand
every sandbox, Version, Root, path, event, or process into one response.

Legacy fields such as current layer, layer count, layer depth, squash-needed,
or chain ancestry are removed or rewritten. V2 may report complete-Version
and reference counts, but no count is proof of payload equality or selected
authority.

### 4.2 `trace`

Read one bounded diagnostic trace for an authorized sandbox.

```text
sandbox-observability-cli trace \
  --sandbox-id SANDBOX \
  [--trace-id TRACE_ID]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox diagnostic scope |
| `trace_id` | no | opaque string, default `last` | Specific retained trace, or the most recent eligible trace when omitted |

`last` is a diagnostic convenience, not a mutation selector. The result is
bounded by retained span count and response bytes, preserves causal/parent
relationships where available, and marks missing or expired spans explicitly.

A publish trace should distinguish Candidate enumeration, admission,
occupied-ID verification, payload durability, internal OCC transition,
cleanup, and result mapping. It must not expose canonical bytes, the expected
Head token, or enough path/control data to bypass owner APIs.

### 4.3 `events`

Read a filtered bounded suffix of retained events.

```text
sandbox-observability-cli events \
  --sandbox-id SANDBOX \
  [--name EVENT_NAME] \
  [--since-ms DURATION_MS] \
  [--last-n COUNT]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox diagnostic scope |
| `name` | no | bounded event-name filter | Exact supported event family/name; no regex with unbounded evaluation |
| `since_ms` | no | non-negative bounded integer | Retention-relative lookback window |
| `last_n` | no | positive bounded integer | Maximum returned events after filters |

When both `since_ms` and `last_n` are present, both bounds apply. Omission uses
finite server defaults. Stable V2 event spellings remain
`OPEN_WITHIN_R0`; the semantic event families should cover:

| Family | Examples of facts—not frozen event names |
|---|---|
| Candidate | enumeration started/completed/rejected, validation failure |
| Admission | new payload accepted, occupied ID byte-verified, collision rejected |
| Publication | internal OCC succeeded, stale lost, same-Version transition |
| References | Fixed Checkpoint Root created/removed; sandbox/Branch Head created/replaced/removed |
| Recovery | incomplete operation found, replayed, quarantined, or left as debt |
| Retirement | Version became eligible, custody deferred it, retirement completed |
| Runtime | Workspace created/published/destroyed; command lifecycle |
| Lifecycle | sandbox/daemon readiness and shutdown transitions |

Events are diagnostic/audit inputs only. Replaying an event stream must not be
required to reconstruct authoritative Heads, Roots, or accepted payloads.

### 4.4 `resources`

Read bounded resource usage for one sandbox or an authorized fleet summary.

```text
sandbox-observability-cli resources \
  [--sandbox-id SANDBOX] \
  [--window-ms MS]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `sandbox_id` | no | opaque string | Sandbox scope; omit for fleet scope |
| `window_ms` | no | integer, default `60000`, maximum `600000` | Aggregation window for sandbox scope; current e497 fleet behavior ignores the field and V2 must either preserve that explicitly or normalize it in Phase 04 |

The result may include CPU, resident memory, I/O, process, Workspace scratch,
LayerStack-0 staging, and configured-capacity summaries. Logical payload bytes,
physical allocated bytes, temporary scratch bytes, and runtime Workspace bytes
must remain separate units; adding them as though they were interchangeable is
misleading.

### 4.5 `daemon`

```text
sandbox-observability-cli daemon --sandbox-id SANDBOX
```

| Argument | Required | Type | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox whose daemon/process view is requested |

The result may include daemon readiness, process state, start/uptime summary,
bounded restart/error counters, endpoint reachability, and current routing
generation. It does not expose credentials, raw sockets, host PID namespace
details, or direct storage mutation handles.

### 4.6 `topology`

```text
sandbox-observability-cli topology --sandbox-id SANDBOX
```

| Argument | Required | Type | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox whose ownership/runtime topology is requested |

The topology view explains current relationships while preserving the
portable-identity boundary:

```text
sandbox / Branch context
  |
  +-- manager lifecycle record
  +-- LayerStack-0 selected-Version reference
  +-- zero or more fixed Checkpoint Roots
  +-- runtime daemon
       +-- live Workspaces
       |    `-- mount/namespace effects
       `-- commands
            `-- exec/process effects
```

Docker/OCI identifiers, OverlayFS roles, mounts, namespaces, cgroups, daemon
endpoints, and host paths shown in this view are explicitly runtime-private
facts. Their diagnostic presence must never cause them to enter canonical
Version bytes or `VersionId`.

### 4.7 `cgroup`

```text
sandbox-observability-cli cgroup \
  --sandbox-id SANDBOX \
  [--scope SCOPE] \
  [--window-ms MS]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox routing scope |
| `scope` | no | string, default `sandbox` | `sandbox` or an authorized Workspace scope accepted by the current catalog |
| `window_ms` | no | integer, default `60000`, maximum `600000` | Bounded resource window |

The result may include CPU, memory, pressure, process, and I/O summaries
supported by the host. Kernel/cgroup absence or partial permission is reported
as unavailable/partial rather than fabricated as zero. A cgroup path or
namespace identity is never portable state.

## 5. `layerstack` — LayerStack-0 diagnostics

Read a bounded diagnostic view of the selected store owner and, optionally, a
correlated live Workspace.

```text
sandbox-observability-cli layerstack \
  --sandbox-id SANDBOX \
  [--workspace-id WORKSPACE] \
  [--window-ms MS]
```

| Argument | Required | Type/default | Contract |
|---|---:|---|---|
| `sandbox_id` | yes | opaque string | Sandbox/Branch context to correlate with LayerStack-0 |
| `workspace_id` | no | opaque runtime Workspace identifier | Optional live-Workspace correlation; this is the current observability spelling and Phase 04 must reconcile it with public `workspace_session_id` without silently accepting two identities |
| `window_ms` | no | integer, default `60000`, maximum `600000` | Window for rates/deltas; current-point records remain labeled as gauges |

The result is organized by selected architectural concerns rather than legacy
layer records.

### 5.1 Identity and admission

| Diagnostic | Meaning |
|---|---|
| `accepted_versions` | Count of accepted complete immutable Version bindings in the scoped store |
| `payloads_new` | Complete payload admissions that created physical payload occupancy during the window |
| `payloads_reused` | Admissions whose occupied `VersionId` was accepted only after full canonical-byte comparison |
| `collision_rejections` | Occupied-ID comparisons whose full bytes differed and were rejected |
| `candidate_rejections` | Candidates rejected for validation, bounds, instability, I/O, or canonicalization failure |
| `logical_payload_bytes` | Canonical logical bytes represented; kept distinct from allocated and transferred bytes |
| `physical_payload_bytes` | Store allocation attributable to committed complete payloads, measured with a documented filesystem method |

No counter proves that the canonical codec/hash grammar is correct. Phase 02
tests own that proof; diagnostics merely expose observed outcomes.

### 5.2 References and read custody

| Diagnostic | Meaning |
|---|---|
| `heads` | Count and bounded summary of mutable sandbox/Branch Head references |
| `checkpoint_roots` | Count of fixed Checkpoint Roots |
| `selected_version_id` | Optional opaque correlation value for the requested sandbox; never an authority token |
| `active_read_custodies` | Readers currently preventing retirement, reported as aggregate counts |
| `rootless_versions` | Complete accepted Versions currently without a durable Root/Head reference, classified as retirement/recovery debt |

Root/Head storage paths, revisions, raw AcceptedBindings, and reader handles do
not appear in the response.

### 5.3 Publication and internal OCC

| Diagnostic | Meaning |
|---|---|
| `head_transitions_published` | Conditional Head replacements that linearized successfully |
| `head_transitions_stale` | Requests that lost strict OCC and returned conflict |
| `head_transitions_same_version` | Reference transitions whose accepted target already equaled the selected Version |
| `publish_recovery_required` | Publish attempts that left durable work for bounded recovery |
| `silent_merge_or_rebase` | Must be structurally absent; if represented as a safety assertion, any non-zero/false-safe value is a correctness incident |

The expected Head record remains internal. Observability may report aggregated
stale rates, but cannot accept a public revision or retry a failed transition.

### 5.4 Payload-I/O accounting

Hard rule 3 requires a testable seam that distinguishes payload bytes from
metadata/reference I/O. At minimum, LayerStack-0 instrumentation records these
per logical operation class and exposes bounded aggregates:

| Counter | Unit | Required interpretation |
|---|---|---|
| `payload_bytes_read` | bytes | Complete/canonical payload bytes read by the operation; full-byte collision comparison is payload reading and must be counted |
| `payload_bytes_written` | bytes | Complete/canonical payload bytes written into committed or staging payload storage |
| `payload_bytes_copied` | bytes | Payload bytes copied between physical payload locations |
| `reference_bytes_read` | bytes | Root/Head/control metadata read; reported separately |
| `reference_bytes_written` | bytes | Root/Head/control metadata written; reported separately |
| `scratch_bytes_peak` | bytes | Peak bounded temporary scratch attributed to the operation |

For Checkpoint creation, same-store fork, rollback-to-existing, and same-
Version moves, tests must observe:

```text
payload_bytes_read    = 0
payload_bytes_written = 0
payload_bytes_copied  = 0

reference metadata I/O may be non-zero and is reported separately.
```

The zero-payload-I/O claim for `fork_sandbox` is conditional on the same-store
mapping in shared decision `API-D09`. Observability must label the store scope
used for the measurement without leaking host paths.

### 5.5 Recovery, capacity, and cleanup

| Diagnostic | Meaning |
|---|---|
| `staging_bytes` / `staging_items` | Bounded incomplete admission/publish staging work |
| `orphan_bytes` / `orphan_items` | Accepted payloads with no durable reference and no active custody, awaiting classified cleanup |
| `recovery_items` | Incomplete durable transitions classified for replay, quarantine, or cleanup |
| `quarantined_items` | Corrupt/ambiguous objects isolated from selection pending operator handling |
| `retirement_eligible` | Unreferenced, uncustodied accepted Versions eligible for retirement |
| `retirement_deferred` | Versions retained due to active custody, recovery ambiguity, or configured grace |
| `retirement_completed` | Completed bounded retirement work in the window |
| `scratch_bytes_peak` | Peak temporary work, distinct from durable committed payload allocation |
| `open_fds`, `active_workers`, `queued_work` | Aggregate resource use against configured finite caps |

These fields are diagnostic. A caller cannot request `retire_now`, `recover`,
`repair`, `force_publish`, `clear_quarantine`, or `delete_orphan` through this
family.

### 5.6 Optional Workspace correlation

When `workspace_id` is supplied, the response may correlate:

- the Workspace's captured base accepted `VersionId`;
- current runtime lifecycle state;
- logical upper/change estimates and bounded scratch consumption;
- active mount/namespace/command counts;
- publish attempts and their terminal outcome; and
- cleanup state after publish or destroy.

This view does not elevate upperdir/lowerdir, OverlayFS, mount, namespace,
container, or host-path facts into Version identity. The Workspace remains a
runtime effect and a Candidate source until a complete immutable Version is
admitted.

## 6. Legacy LayerStack diagnostics disposition

The e497 `layerstack` endpoint is useful as a transport and operator entry
point, but its V2 meaning changes.

| Legacy concept/behavior | V2 disposition |
|---|---|
| Layer inventory and individual layer truth | Remove; complete accepted Versions and reference summaries replace it |
| Current layer / top layer | Remove; selected accepted Version correlation replaces it |
| Layer depth / chain length | Remove; there is no layer-depth reconstruction metric in the V2 core path |
| Squash state, eligibility, or scheduling | Remove; no squash operation or background squash policy exists |
| Per-layer sizes | Remove; report complete payload logical/allocated bytes and bounded Workspace scratch separately |
| Lease/bookings as selected truth | Remove; bounded runtime custody and internal resource reservations may be diagnosed but do not select a Version |
| Lazy byte-count sidecar/cache | May remain only as bounded, reconstructible diagnostic cache; it is neither accepted payload evidence nor a publication prerequisite |
| Layer export/read chunks | Rewrite around complete Version export transport or remove; no legacy layer chain is reconstructed for diagnostics |

An old field must not be retained under a misleading V2 label solely for
dashboard compatibility. Compatibility adapters may return a declared
unsupported/deprecated field during a bounded transition, but cannot derive
fake layer depth from Version history.

## 7. Metrics and cardinality contract

Metrics complement bounded diagnostic responses; they do not replace typed
operation results.

| Dimension | Metric label policy | Detailed correlation location |
|---|---|---|
| Operation family/name | Allowed finite enumeration | Trace/event payload |
| Outcome/error class | Allowed finite enumeration | Typed response/error |
| Store generation/readiness state | Allowed finite enumeration or bounded generation gauge | LayerStack diagnostic response |
| Sandbox, Version, Checkpoint, Workspace, command, request IDs | Not raw metric labels | Authorized bounded response, trace, or event |
| File path, host path, image, command text | Not raw metric labels | Redacted trace/event only when policy allows |
| Collision/recovery reason | Bounded reason enum | Detailed redacted event |
| Provider, filesystem, kernel capability | Bounded configured enum only | Topology/resource response |

Histograms and counters use stable documented units. Byte counters distinguish
logical, allocated, read, written, copied, scratch, and metadata bytes. Time
histograms distinguish admission, full-byte verification, durability, OCC,
recovery, retirement, and runtime activation rather than reporting one
ambiguous “snapshot time.”

## 8. Errors and partial collection

The shared error envelope applies. Observability-specific cases include:

| Condition | Result |
|---|---|
| Requested sandbox/Workspace/trace is outside authorized scope | `not_found` or `forbidden` according to the product disclosure policy |
| Requested trace/event aged out | `not_found` with bounded retention metadata; never silently substitute a different record |
| Unsupported kernel metric | Successful partial result with explicit unavailable capability when useful |
| One correlated owner times out | Successful `partial` result if remaining data is useful; otherwise `unavailable` |
| Window, count, name, scope, or cursor invalid | `invalid_argument` |
| LayerStack-0 is recovering | Bounded readiness/recovery diagnostic if readable; no observer-initiated recovery |
| Response reaches configured cap | Successful truncated result with explicit truncation/cursor/aggregate |

Diagnostics must distinguish zero from unknown, unavailable, redacted, and
not-applicable. Absence of a sample is never reported as zero resource use or
zero recovery debt.

## 9. Open owner decisions and API seams

| Decision | Effect on this family | Isolation status |
|---|---|---|
| `DEC-001` — retain/replace/remove `file_blame` | Changes provenance/audit events and possibly operation-name correlation; must never move provenance into Version identity | Architecturally isolated |
| `DEC-011` — cutover observation window | Selects how long V1/V2 parity, recovery, and cleanup evidence must be retained and compared during rollout | Architecturally isolated if storage truth and rollback boundaries remain unchanged; rollout cannot declare completion before owner acceptance |
| `DEC-017` — `file_list`, no-session writes/edits, target forms | Changes file-operation counters, target labels, and automatic-Workspace traces | Architecturally isolated if all writes still use a Workspace Candidate and strict publish path |
| `DEC-018` — auth/revoke race ordering | Selects which authorization/order outcome diagnostics record; storage still receives one authorized internally expected transition | Architecturally isolated only while observability remains a reader and does not adjudicate the race |

Phase 04 may select exact field names, event names, redaction formats, cursor
encoding, and bounded defaults within R0. It may not add mutation controls,
turn metrics into authority, expose public OCC revisions, or restore legacy
layer-chain semantics.

## 10. Phase 04 implementation checklist

- [ ] Keep all eight operation names aligned with the operation catalog.
- [ ] Preserve the current required/optional argument shapes unless a recorded
      API decision changes them.
- [ ] Make `snapshot` unmistakably diagnostic, not a Version or Checkpoint.
- [ ] Rewrite `layerstack` around complete Versions, Roots/Heads, admission,
      strict OCC, recovery, retirement, and bounded resources.
- [ ] Delete layer-depth and squash truth from V2 result schemas.
- [ ] Instrument payload read/write/copy bytes separately from reference and
      metadata I/O.
- [ ] Test zero payload I/O for Checkpoint, same-store fork,
      rollback-to-existing, and same-Version reference transitions.
- [ ] Bound response bytes, list lengths, event/trace retention, windows,
      collection time, metric labels, scratch, workers, and file descriptors.
- [ ] Mark partial, unavailable, redacted, truncated, and unknown results
      explicitly.
- [ ] Prove observability cannot create, repair, move, retire, or delete
      selected-state records.
- [ ] Keep runtime-private topology facts out of canonical Version inputs.
- [ ] Preserve the four open owner decisions as explicit seams.

## 11. Evidence and first source anchors

Current signatures and operation names carry evidence label `SOURCE-VERIFIED`
from the sealed Phase 00 inventory and these first implementation anchors:

```text
crates/sandbox-operations/catalog/src/observability/
crates/sandbox-observability/
crates/sandbox-observability-cli/
```

See the Phase 00
[public-surface inventory](../phases/00-freeze-rules/inventory-surfaces.md) for
the measured current catalog/CLI/HTTP distinctions and the selected
[architecture design](../architecture_design.md) for V2 ownership and
storage-family decisions.

No V2 observability implementation, load test, or benchmark was executed for
this document. Counter names, result schemas, consistency markers, retention,
and exact metric instruments have evidence label `OPEN_WITHIN_R0`; proposed
schema disposition is not implementation evidence. Historical Stage 4.6 is
`INCOMPARABLE`, the final performance verdict is `TARGET_UNSELECTED`, and this
API makes no performance promise.

Reference lifecycle diagnostics report the canonical outcome names
`APPLIED`, `ALREADY_EXISTS`, `NOT_FOUND`, `CONFLICT`, `INVALID_BINDING`,
`CORRUPT`, `OUTCOME_UNKNOWN`, and `INTERNAL_FAILURE` from the
[Reference EphCoW algorithm](../algorithm/02-references-and-publication/01-reference-ephcow.md).
They never become read-back authority: exact Head/Root read-back remains a
LayerStack-0 operation invoked by an authorized application owner.
