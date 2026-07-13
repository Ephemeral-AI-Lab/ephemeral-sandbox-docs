# FlashCart Multi-Agent Demo — Implementation Specification

| Field | Value |
| --- | --- |
| Status | Ready for implementation |
| Source design | [DESIGN.md](./DESIGN.md) |
| Visual baseline | [Light-theme control-room prototype](./index.html) |
| Primary implementation | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/demo/multi-agent |
| Presentation implementation | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/multiagent |
| Authored workload | 10 agent lanes, 350–500 counted public CLI calls; prefer 450–500 |
| Runtime target | 90–120 seconds, excluding presenter pauses |
| Dependency policy | Python and Node standard libraries; reuse existing repository helpers |

## 1. Purpose

This document turns DESIGN.md into an implementation and acceptance contract.
It covers four deliverables:

1. implement the deterministic multi-agent runner and the small product
   prerequisites required by the design;
2. generate ten complex, reviewable agent plans and their storefront payloads;
3. execute the plans against the real CLI, diagnose and fix runner, script, CLI,
   or runtime defects, then tune the scenario without weakening assertions;
4. produce the light-theme live and recorded demo HTML.

The finished demo starts from an almost-empty project, holds ten independent
workspaces open concurrently, performs 350–500 authored operations, publishes a
polished storefront, proves line-disjoint merge and blame, rejects one
cross-surface file conflict atomically, retries from a fresh head, proves
same-port network isolation, and retains real observability evidence.

Normative words such as **MUST**, **MUST NOT**, **SHOULD**, and **MAY** describe
implementation requirements.

## 2. Product truth and presentation truth

The implementation MUST preserve these boundaries:

| Data shown | Source | UI label |
| --- | --- | --- |
| Runtime, file, manager, and observability results | Parsed sandbox CLI output | Real CLI or Real telemetry |
| Explicit workspace create/destroy | Existing allowlisted direct-daemon helper | Trusted session control |
| Storefront iframe during a live run | Sandbox port-forwarding route | Live sandbox preview |
| Storefront from an exported successful run | Retained run artifact | Recorded real preview |
| Raw blame owner joined to A01–A10 | Runner correlation ledger | Real blame · Agent mapping by runner |
| Agent dialogue and conflict conversation | Authored presentation events | Staged narrative |
| Scene titles and annotations | Presentation projection | Presentation annotation |
| Data in the static design preview | Embedded fixture | Simulated sample |

The UI MUST keep raw owners, raw CLI responses, and provenance available in
evidence detail. It MUST NOT imply native agent identity, native agent-to-agent
messaging, general undo, or public workspace lifecycle APIs.

“Rollback” in the story means one of two precise outcomes:

- a conflicting changeset is rejected as a unit and publishes no files;
- an explicit no-op workspace is destroyed and its unpublished files disappear.

## 3. Implementation decisions

These decisions remove ambiguity before coding:

1. **Plans are JSONL, not shell scripts.** Each authored row represents one
   actual CLI process. Large contents and edit arrays live in payload files.
2. **Generation is deterministic.** Explicit Python recipes generate the ten
   checked-in plans and a checked-in call budget. The generator is not a
   general workflow language.
3. **The runner stays small.** One standard-library Python entry point performs
   validation, scheduling, evidence capture, serving, replay, and export.
   Modules are extracted only when tests show that the file has become hard to
   reason about.
4. **Existing harness code is reused.** CLI discovery/execution, authenticated
   direct-daemon calls, cleanup, and file assertions build on the current E2E
   helpers instead of duplicating transport or authentication logic.
5. **The first presentation target is standalone HTML.** The existing
   multiagent/index.html becomes the real artifact-driven control room. A
   React/Mantine console route is a later integration, not a dependency of this
   delivery.
6. **Live transport is polling.** The page reads an atomically replaced
   run.json every 400 ms. No WebSocket, client state framework, message bus, or
   separate event service is added.
7. **Presenter controls affect only the view.** Pause stops automatic scene
   following; it does not pause the runner or hold runtime leases.
8. **Exact request correlation is a prerequisite.** A small CLI request-ID
   override is required before the UI may claim per-step concurrent traces.
9. **Recorded delivery is a static package.** demo.html embeds its bounded
   projection, while curated evidence and the retained preview sit beside it.
   It needs a static file server but no demo runner or live sandbox.

## 4. System architecture

~~~mermaid
flowchart LR
    R["Explicit recipes.py"] --> G["generate_scripts.py"]
    P["Checked-in payloads"] --> G
    G --> L["10 JSONL plans"]
    G --> B["call-budget.json"]
    S["scenario.json"] --> V["Preflight validator"]
    L --> V
    B --> V
    P --> V
    V --> E["run_demo.py asyncio scheduler"]
    E --> M["sandbox-manager-cli"]
    E --> C["sandbox-runtime-cli"]
    E --> O["sandbox-observability-cli"]
    E --> D["Trusted direct-daemon lifecycle adapter"]
    M --> A["Raw immutable evidence"]
    C --> A
    O --> A
    D --> A
    A --> J["events.ndjson and bounded run.json projection"]
    J --> H["Light-theme index.html"]
    A --> X["Self-contained recorded demo.html"]
~~~

The plans contain scenario complexity. The runner provides only fixed operation
adapters, dependencies, barriers, expectations, evidence persistence, cleanup,
and projection.

## 5. Repository deliverables

### 5.1 Runtime and test repository

~~~text
ephemeral-sandbox-test/demo/multi-agent/
├── README.md
├── scenario.json
├── recipes.py
├── generate_scripts.py
├── update_oracle.py
├── run_demo.py
├── call-budget.json
├── expected-final.json
├── test-inventory.json
├── agents/
│   ├── A01-foundation.plan.jsonl
│   ├── A02-design-system.plan.jsonl
│   ├── A03-products.plan.jsonl
│   ├── A04-catalog.plan.jsonl
│   ├── A05-search.plan.jsonl
│   ├── A06-cart.plan.jsonl
│   ├── A07-wishlist.plan.jsonl
│   ├── A08-checkout.plan.jsonl
│   ├── A09-accessibility.plan.jsonl
│   └── A10-qa.plan.jsonl
├── payloads/
│   ├── A01/
│   ├── A02/
│   ├── A03/
│   ├── A04/
│   ├── A05/
│   ├── A06/
│   ├── A07/
│   ├── A08/
│   ├── A09/
│   └── A10/
├── tests/
│   ├── test_generation.py
│   └── test_run_demo.py
└── runs/
    ├── qualifications/
    │   └── QUALIFICATION_ID.json
    └── RUN_ID/
        ├── manifest.json
        ├── run.json
        ├── expected-final.json
        ├── events.ndjson
        ├── diagnoses.ndjson
        ├── triage-index.ndjson
        ├── scenario.compiled.json
        ├── commands/
        ├── defects/
        ├── observability/
        ├── blame/
        └── preview/
~~~

The runs directory is generated and ignored by version control except for a
small documented fixture if browser tests require it.

### 5.2 Product prerequisite

The runtime CLI currently creates request IDs internally. Add one global
request-ID override through the current input-building path:

- accept a global “--request-id VALUE” on sandbox-runtime-cli;
- accept only 1–128 ASCII letters, digits, period, underscore, colon, or dash;
- pass it to the existing request builder that accepts an explicit ID;
- retain the current UUID behavior when the option is omitted;
- add unit coverage for default, explicit, duplicate, and invalid values;
- add one live correlation test showing the supplied ID in trace/event output.

The runner uses IDs of the form:

~~~text
demo-RUN_ID-STEP_ID-ATTEMPT
~~~

The override applies to runtime CLI requests. Manager, trusted-session, and
observer interactions retain their native identifiers and appear only as
aggregate or lifecycle evidence unless their existing response exposes an
exact join. If the patch is unavailable, the runner MAY collect aggregate
telemetry, but the run cannot pass golden qualification. The HTML MUST NOT
guess an exact trace join.

### 5.3 Documentation and presentation repository

~~~text
ephemeral-sandbox-docs/multiagent/
├── DESIGN.md
├── IMPLEMENTATION_SPEC.md
├── index.html
└── generated/
    └── RUN_ID/
        ├── demo.html
        ├── manifest.json
        ├── export-manifest.json
        ├── artifacts/
        └── preview/
~~~

index.html is the source control room and static sample preview.
generated/RUN_ID is produced from a successful real run. demo.html embeds a
bounded recorded projection; the package remains viewable from any static HTTP
server without the runner, daemon, or sandbox.

## 6. CLI and runner contract

### 6.1 Host process rules

Extend e2e/harness/runner/cli.py with a structured cli_record sibling that
returns redacted argv, stdout, stderr, return code, parsed JSON, and monotonic
duration. Preserve compatibility by having the current cli helper delegate to
cli_record and return only its parsed response. Reuse the existing executable
routing, authentication environment, and JSON projection paths.

cli_record uses `subprocess.Popen`, registers the child in a run-owned process
registry as soon as it spawns, and accepts a `threading.Event` cancellation
token. The asyncio runner calls it through asyncio.to_thread. On cancellation it
sets the token, waits for cli_record to terminate then kill after a bounded
grace period, and does not finish cleanup until the registry is empty. Cancelling
the asyncio future alone is never treated as process cancellation. Add one
central argv/environment redactor before any log or artifact write; tests cover
split and equals-form secret flags, daemon credentials, URLs, stdout/stderr
credential patterns, and prove raw argv is never logged.

Every CLI invocation MUST:

- use a subprocess argument array with host-side shell execution disabled;
- capture the exact redacted argv, process return code, stdout, stderr,
  monotonic duration, and parsed JSON;
- require exactly one valid JSON response object when the CLI succeeds;
- distinguish CLI transport success from the child command exit code;
- distinguish child process completion from workspace publication;
- write its raw evidence before evaluating the expectation;
- never record daemon authentication credentials.

Invocation semantics are fixed:

| Condition | Host CLI exit | Parsed/runtime fields | Runner result |
| --- | ---: | --- | --- |
| Valid response, command succeeds | 0 | status success; child exit 0 when present | Evaluate operation expectation |
| Valid response, expected-red child | 0 | response status error; child exit 1 | EXPECTED_FAILURE only for the named cycle |
| Valid response, publish rejected | 0 | publish_rejected true and rejection class | Evaluate exact rejection expectation |
| Structured operation fault | 1 | Parsed error object with allowlisted `error.kind` | Evaluate only an expectation such as `not_found` that names that kind |
| Usage/schema error | 2 | No trusted result | FAILED |
| Transport/client error | 1 | No recognized structured operation fault; response retained if parseable | FAILED |
| Host timeout/cancel | nonterminal | Kill the local CLI process, record it, reconcile known command IDs; unknown mutation outcome fails | FAILED/CANCELLED |

Terminal command polling uses the current runtime status vocabulary discovered
by the live canary. An absent file_read or file_blame MUST return its documented
structured not-found error; empty content is not proof of absence.

Runtime command strings are static recipe data. Dynamic sandbox, workspace,
command, and request IDs are passed as CLI flags, never interpolated into a
shell program.

File-write bodies and file-edit arrays MUST be loaded from payload files and
passed as one argv value. Payloads MUST NOT contain NUL bytes. The initial
guardrail is 48 KiB per argv-backed payload; larger content must be split into
meaningful files or small patches.

### 6.2 Public operation allowlist

Agent plan rows may use only these public runtime operations:

- exec_command;
- write_command_stdin;
- read_command_lines;
- file_read;
- file_write;
- file_edit;
- file_blame.

The scenario engine may also invoke the public manager and observability CLIs.
Explicit create_workspace_session and destroy_workspace_session calls are
allowed only through the existing trusted adapter and are never counted as
public agent CLI calls.

### 6.3 Plan record schema

Each JSONL line has this shape:

~~~json
{
  "schema_version": 1,
  "id": "A06.026",
  "agent": "A06",
  "ordinal": 26,
  "scene": "fanout",
  "phase": "pricing-red-green",
  "category": "test_debug",
  "purpose": "Prove the free-shipping boundary initially fails",
  "op": "exec_command",
  "workspace_ref": "A06.primary.workspace",
  "args": {
    "command": "node --test tests/cart-shipping.test.mjs",
    "timeout_ms": 60000,
    "yield_time_ms": 30000
  },
  "expect": {
    "kind": "expected_red",
    "child_exit_code": 1,
    "failing_subtests": [{
      "id": "free shipping starts at 6000 cents",
      "reason_contains": "threshold should be 6000"
    }],
    "forbid_output_contains": [
      "SyntaxError", "ERR_MODULE_NOT_FOUND", "Could not find"
    ],
    "inventory_ref": "test-inventory.json#A06.shipping-boundary"
  },
  "test_cycle": "A06.shipping-boundary",
  "after": ["all-primary-workspaces-ready"],
  "at_ms": 12000
}
~~~

Required fields are schema_version, id, agent, ordinal, scene, phase, category,
purpose, op, args, and expect. Optional fields are attempt_ref, workspace_ref,
command_ref, bind, test_cycle, final_regression, after, at_ms, and effects. The generator derives
count_as=agent and provenance=public_cli for every authored plan row; neither
field is author-controlled. It also recomputes category from the named recipe
helper and rejects a serialized category that disagrees, preventing budget
gaming.

file_write and file_edit have a path effect derived from their arguments. An
exec_command that intentionally changes files MUST declare effects.paths; the
validator requires scoped relative paths and the runner records their
before/after digests. Test, build, read, server, and anchor commands declare no
file effect. Effects are evidence boundaries, not permission to ignore an
unexpected changed path. The runner snapshots the attempt immediately before
and after each mutating row and evaluates only that pre/post delta against the
row's effects. It separately compares the cumulative workspace diff with the
union of successful prior effects for that attempt. A path outside either
boundary fails the row; earlier legitimate edits do not.

Allowed category values are workspace_control, inspect, patch, build_lint,
test_debug, and conflict_network_audit. Allowed scene values are fanout, merge,
conflict, network, and evidence.

References are names, not runtime IDs. For example, the initial anchor binds:

~~~json
{
  "bind": {
    "workspace_session_id": "A06.primary.workspace",
    "command_session_id": "A06.primary.anchor"
  }
}
~~~

The engine resolves those names only after validating the producing response.
Retries bind new names and never overwrite the original mapping. Every automatic
lifecycle has a distinct immutable attempt_ref: `A01.primary` through
`A10.primary`, `A06.conflict`, `A08.conflict`, `A08.retry`, and `A10.final`.
An anchor binds `<attempt_ref>.workspace` and `<attempt_ref>.anchor` exactly
once. Workspace-scopable operations while the attempt is live must carry both
that attempt_ref and workspace_ref. write_command_stdin/read_command_lines use
only its command_ref; post-publication blame/read checks are sessionless and
depend on the publish barrier. Validation rejects ref reuse, mismatched refs,
use after release, or fallback from a later attempt to `*.primary.workspace`.

Payload-backed arguments include both the relative source and its generated
digest:

~~~json
{
  "args": {
    "path": "src/features/cart.js",
    "edits_from": "payloads/A06/027.json",
    "payload_sha256": "sha256"
  }
}
~~~

The runner verifies the digest immediately before spawning the CLI.

The expectation vocabulary is deliberately fixed:

- command_running;
- command_ok;
- expected_red;
- file_read;
- file_write;
- file_edit;
- publish_success;
- publish_noop;
- publish_reject;
- blame_owner;
- not_found.

test-inventory.json is a checked-in, generator-validated map from every test
cycle to its exact command, discovered subtest IDs and count, and allowed
skip/todo/cancelled set (empty unless the spec explicitly names an exception).
The runner parses TAP rather than accepting a generic exit code or “not ok.” An
expected_red row must observe exactly its declared failing subtest IDs and
reason fragments, see every other inventoried subtest, and contain none of the
frozen infrastructure-error signatures. A green row and A10's final regression
must exit zero, discover the exact frozen inventory, and report no unexpected
fail, skip, todo, or cancelled test. Zero discovered tests always fails.

There is no expression language, arbitrary JSONPath, embedded Python, or
templated shell evaluation in a plan.

### 6.4 Counting rules

One counted row equals one spawned public sandbox CLI process with one parsed
response. Authored agent rows always derive count_as=agent. The following
scenario control interactions derive count_as=engine and do not count toward
the authored total:

- manager sandbox create, inspect, or destroy;
- observability polling and checkpoints;
- trusted explicit-session create or destroy;
- automatic polling required to finish a running authored command;
- barriers, pacing, scene changes, and narrative;
- host-side HTTP fetches used to retain a preview.

An intentionally authored read_command_lines diagnostic is counted. An
automatic continuation poll is recorded as engine_control and is not counted.
Unplanned debugging calls are retained as diagnostic calls and never alter the
golden authored total.

The illustrative recommended allocation below is advisory, not a validator
contract:

| Agent | Workspace control | Inspect | Patch | Build/lint | Test/debug | Conflict/network/audit | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | 2 | 8 | 14 | 6 | 11 | 2 | 43 |
| A02 | 2 | 8 | 15 | 6 | 11 | 2 | 44 |
| A03 | 2 | 9 | 14 | 6 | 12 | 2 | 45 |
| A04 | 2 | 9 | 15 | 6 | 10 | 8 | 50 |
| A05 | 2 | 9 | 14 | 6 | 11 | 4 | 46 |
| A06 | 2 | 9 | 15 | 6 | 11 | 7 | 50 |
| A07 | 2 | 8 | 13 | 5 | 11 | 3 | 42 |
| A08 | 2 | 10 | 16 | 6 | 12 | 8 | 54 |
| A09 | 2 | 9 | 14 | 5 | 12 | 12 | 54 |
| A10 | 2 | 10 | 11 | 7 | 15 | 4 | 49 |
| **Recommended total** | **20** | **89** | **141** | **59** | **116** | **52** | **477** |

The two workspace-control rows are each agent’s primary anchor and release.
The separate A06/A08 conflict-wave anchors/releases, A08 retry lifecycle, and
A10 post-merge regression lifecycle are authored public calls categorized as
conflict_network_audit or test_debug. Every number in the table is advisory:
repair and tuning MAY move calls freely between agents and categories. A valid
generated plan has 350–500 calls total, preferably 450–500, all required proof
cycles, and no padding. There is no per-agent numeric acceptance gate;
call-budget.json records the actual matrix and its digest.

run.json and the HTML MUST report three separate totals:

- authored agent calls: completed / planned, where planned is derived from the
  validated generated plans;
- engine, lifecycle, and telemetry interactions;
- unexpected diagnostic calls.

A normal 90–120 second run is expected to add roughly 750–1,000 real engine,
lifecycle, and observability interactions: 450–500 per-request trace lookups,
180–240 aggregate cgroup samples, plus lifecycle, event, snapshot, layer,
blame, polling, and cleanup calls. That yields roughly 1,200–1,500 real
interactions in the preferred authored band. This is a capacity expectation,
not a padding target.

### 6.5 Persistent workspace lifecycle

The engine starts all ten primary automatic workspaces before allowing normal
lane work. Each is held open by one authored exec_command with no workspace ID:

~~~sh
set -eu
cd /workspace
printf '__DEMO_READY__\n'
IFS= read -r action
[ "$action" = publish ]
~~~

The response MUST be running and MUST supply both command_session_id and
workspace_session_id. Every subsequent primary lane operation carries that
workspace ID only when the operation accepts workspace scoping; command control
uses the bound command ID and post-publication inspection is sessionless.

The barrier “all-primary-workspaces-ready” opens only after snapshot evidence
also shows ten active workspaces. This proves concurrency rather than merely
starting commands quickly.

Before releasing an anchor, the runner MUST verify:

- every earlier authored row in the lane is terminal;
- no rider command remains running;
- required red/green cycles have reached the expected state;
- all mutations returned successfully;
- all release dependencies are satisfied.

The release sends “publish” plus a newline with write_command_stdin. If its
first response remains running, the engine polls to terminal as engine control.
The engine separately evaluates:

1. CLI process return code;
2. anchor child exit code;
3. publication success or rejection;
4. shared revision/content effect;
5. eventual automatic workspace destruction.

`publish_noop` is valid only for a deliberately unchanged attempt such as
`A10.final`. It requires CLI and child success, no publication rejection, shared
revision delta zero, identical shared-tree hash, and observed workspace
destruction. It is not a substitute for a primary or retry publish.

On a fatal lane failure, the runner MUST NOT release that lane’s anchor because
doing so could publish partial work. It stops the run and destroys the sandbox
as a whole.

### 6.6 State machines

Run state:

~~~text
NEW → VALIDATING → PREFLIGHT → PROVISIONING → RUNNING
    → VERIFYING → CLEANING → PASSED

any active state → FAILING → CLEANING → FAILED
any active state → CANCELLING → CLEANING → CANCELLED
~~~

Primary lane state:

~~~text
PENDING → ANCHOR_STARTING → ACTIVE → DRAINING → RELEASING → PUBLISHED
PUBLISHED → POST_PUBLISH → AUDITING → COMPLETE
~~~

Scenario publication-attempt state:

~~~text
PENDING → ANCHOR_STARTING → ACTIVE → RELEASING → PUBLISHED
                                           ↘ REJECTED → RETRY_PENDING
RETRY_PENDING → ANCHOR_STARTING → ACTIVE → RELEASING → PUBLISHED
~~~

Explicit experiment state:

~~~text
PENDING → SESSION_CREATING → ACTIVE → STOPPING → DESTROYING → DISCARDED
~~~

Step state:

~~~text
BLOCKED → READY → RUNNING → PASSED
                         ↘ EXPECTED_FAILURE
                         ↘ FAILED
~~~

run.json records execution_verdict and cleanup_verdict separately. The overall
run verdict is passed only when execution_verdict is passed and cleanup_verdict
is clean. A leak, unknown cleanup outcome, or intentionally preserved debug
resource makes the overall verdict failed and blocks successful export.

### 6.7 Scheduler

scenario.json owns only cross-lane configuration: plan paths and hashes,
barriers, scene gates, observer intervals, trusted experiment steps, narrative
events, and measured timeout values. It does not duplicate authored plan rows.
A representative shape is:

~~~json
{
  "schema_version": 1,
  "authored_call_budget": {"minimum": 350, "preferred_minimum": 450, "maximum": 500, "recommended": 477},
  "plans": [
    {
      "agent": "A01",
      "path": "agents/A01-foundation.plan.jsonl",
      "sha256": "sha256"
    }
  ],
  "observer": {
    "cgroup_interval_ms": 500,
    "projection_interval_ms": 400
  },
  "barriers": [],
  "control_steps": [
    {
      "id": "network.shared.a04.create",
      "kind": "trusted_create_workspace",
      "agent": "A04",
      "args": {"network_profile": "shared", "finalize_policy": "no_op"},
      "bind": {"workspace_session_id": "A04.shared.workspace"},
      "after": ["primary-merge-verified"],
      "provenance": "trusted_session_control",
      "count_as": "engine"
    }
  ],
  "narrative": [],
  "timeouts_ms": {}
}
~~~

control_steps is a validated DAG with only these fixed kinds:
manager_create_sandbox, manager_inspect_sandbox, manager_destroy_sandbox,
bootstrap, trusted_create_workspace, trusted_destroy_workspace,
host_http_probe, observability_checkpoint, assert_barrier, and preview_capture.
Each row has schema_version, id, kind, args, after, derived or fixed provenance,
and derived count_as=engine; producing rows may bind symbolic references.
Every control interaction gets immutable evidence. Public server starts,
write_command_stdin stops, and their intentional read_command_lines calls stay
in agent plans and count toward the generated authored total.

The image is resolved from an explicit “--image” option or the existing E2E
configuration; there is no network pull fallback. The UI root defaults to the
sibling ephemeral-sandbox-docs/multiagent directory derived from the repository
layout and can be overridden with “--ui-root”.

The runner uses one asyncio task per agent lane:

- strict sequential execution inside a lane;
- at most one authored operation in flight per lane;
- at most ten authored agent operations globally;
- one independent observer task that does not consume an agent slot;
- dependency events keyed by step ID or named barrier;
- at_ms as an earliest monotonic start time, never a correctness condition;
- append-only event sequencing under one lock;
- run.json writes through temporary file plus atomic rename.

Named barriers include:

- bootstrap-published;
- all-primary-workspaces-ready;
- all-primary-publications-complete;
- primary-merge-verified;
- conflict-workspaces-ready;
- conflict-winner-published;
- conflict-rejection-verified;
- conflict-retry-published;
- both-shared-network-probes-complete;
- both-isolated-servers-ready;
- all-feature-tests-green;
- final-regression-green.

Scene transitions are opened by barrier assertions, not wall-clock animation.

## 7. Workstream 1 — Implement DESIGN.md

### 7.1 Preflight

Before creating the presentation sandbox, run_demo.py validates:

- all three CLI binaries resolve to recorded realpaths and digests, and
  “help REQUIRED_OPERATION” succeeds for every operation the scenario uses;
- the configured Node image is already local;
- runs/RUN_ID/workspace is newly created, empty, inside the configured demo
  root, and is the only host workspace root passed to the manager;
- the direct-daemon adapter can create and destroy one isolated canary;
- snapshot, cgroup, events, trace, layerstack, file read, and blame respond;
- the request-ID override correlates to a trace;
- the preview route can forward a canary server;
- conflict proof paths are not ignored;
- autosquash is disabled or its threshold is greater than the maximum projected
  publication count for the complete demo; otherwise qualification is blocked;
- a two-workspace canary returns publish_rejected and source_conflict;
- interrupt cleanup leaves no canary sandbox or explicit session.

Preflight failure stops before the show run and produces a readable report.

### 7.2 Bootstrap

One non-agent bootstrap command creates only:

- package metadata with standard-library-only test and serve commands;
- an initial commerce configuration containing the contested value 5000;
- a ten-slot feature registry with null A01–A10 entries;
- minimal directories required for the agents to begin.

It MUST NOT pre-create the finished storefront or agent-owned feature files.
The bootstrap response, initial content hashes, blame, and layerstack revision
are retained.

### 7.3 Ten-agent merge proof

All ten primary workspaces fork from the bootstrap head. Each agent:

- creates files on agent-owned paths;
- replaces exactly its own registry line;
- performs meaningful reads, small edits, syntax/build checks, test failures,
  diagnosis, fixes, and green reruns;
- reaches a feature-specific green gate before release.

All ten primary changesets publish successfully. The runner freezes new
publish-capable steps while it records the post-merge revision, content,
snapshot, layerstack, and blame checkpoint.

At primary-merge-verified, the runner verifies:

- all ten registry values are present;
- all expected agent-owned files exist;
- registry blame contains ten distinct raw workspace owners;
- every raw owner maps to the correct run-local agent;
- the raw owner remains visible beside the display mapping.

A10’s primary lane authors and publishes the regression suite and status
surface. After the conflict retry and network experiment, A10 starts
`A10.final` from the final shared head and runs the complete syntax, unit,
integration, link, asset, accessibility, performance, and HTTP suite with
`final_regression: true`. In that same unchanged attempt it starts the
storefront server on 0.0.0.0:4173, binds `A10.final.preview`, and exposes it only
through the constrained `final-preview` route. After live preview capture it
stops and polls the server, then releases the anchor with `publish_noop`. That
post-merge lifecycle and its calls are included in the generated A10 authored
plan and budget. The final-regression-green barrier cannot open from A10’s
earlier primary results.

### 7.4 Cross-surface conflict and atomic discard

The conflict is a separate wave after primary-merge-verified and intentionally
crosses operation surfaces:

1. Start fresh A06 and A08 automatic anchors from the same final primary head;
   conflict-workspaces-ready opens only when both workspace IDs exist and their
   observed base revision is identical.
2. A06 uses file_edit to change the seeded commerce threshold from 5000 to
   6000.
3. A08 uses exec_command to run scripts/apply-commerce-threshold.mjs, which its
   successful primary lane checked in, changing 5000 to 7500. It also creates
   the otherwise absent src/features/express-checkout.js in that workspace.
4. Release A06 alone. After it publishes, freeze every other publish-capable
   step, record the exact revision/content/blame checkpoint, and open
   conflict-winner-published.
5. Only then release A08. Its anchor process exits zero, but publication MUST report
   publish_rejected true with class source_conflict.
6. Before allowing any later publication, the runner verifies that the manifest
   revision did not advance, the shared
   threshold remains 6000, every unrelated A08 file from the rejected
   changeset is absent, A06 blame remains, and the rejected workspace is gone.
   That atomic checkpoint opens conflict-rejection-verified.
7. A08 starts a fresh automatic workspace from the new head, applies the
   reconciled checkout behavior, reruns its tests, and publishes.

The UI shows child process status and publication status separately. It uses
the evidence wording “Rejected and discarded; shared head unchanged.”

Missing rejection fields, a partial A08 publish, or an undestroyed rejected
workspace is a product defect, not a script outcome to reinterpret.

### 7.5 Shared-port collision and isolated success

A04 and A09 run the disposable network experiment after their durable feature
work has published.

Shared phase:

1. Trusted control creates two explicit shared sessions with finalize_policy
   no_op.
2. A server in the first binds 0.0.0.0:4173 and emits a ready marker.
3. A server in the second attempts the same bind and MUST exit nonzero with an
   address-in-use signature.
4. Both process outcomes and command logs are retained.

Isolated phase:

1. Trusted control creates two explicit isolated sessions with finalize_policy
   no_op.
2. Both servers bind 0.0.0.0:4173 and reach ready markers.
3. The runner probes each workspace-specific forwarding URL and retains status,
   selected headers, body digest, and a bounded body preview.
4. It sends Ctrl-C to live servers, waits for terminal command state, destroys
   the explicit sessions, and verifies they are gone.
5. Sentinel files created in those sessions remain absent from published reads
   and blame.

An explicit session with a live command is never destroyed first. Stop, poll,
then destroy.

### 7.6 Observability collection

The observer runs independently of authored lanes:

| Signal | Collection rule | Required proof |
| --- | --- | --- |
| snapshot | Every major barrier and state change | Ten simultaneous active workspaces |
| cgroup sandbox | Every 500 ms during active scenes | CPU, memory, I/O, and workspace-disk series |
| cgroup workspace | At lane checkpoints while workspace exists | Selected-agent detail; degrade honestly if unsupported |
| events | Incrementally and at every barrier | Lifecycle, publication failure, cleanup |
| trace | Each authored request ID plus key lifecycle requests | Per-step waterfall and conflict finalization |
| layerstack | Bootstrap, every publication wave, before/after rejection | Revision advances only on accepted publish |
| file_blame | Only after successful publication | Registry and contested-line owners |

Resource sampling MUST occur while workspaces exist. A golden run has at least
floor(active_scene_duration_ms / 1000) successful aggregate samples, no gap
longer than two seconds, and CPU usage, memory current/peak, I/O bytes, and
workspace-disk fields whenever exposed by the operation contract. Workspace
cgroup may be labeled unsupported only when the preflight capability probe says
so; an unexpected failure is not a graceful degradation. Because events are
sandbox-scoped and expose inclusive `since_ms` rather than a stable cursor, the
initial watermark is the sandbox creation timestamp, recorded immediately after
create and before bootstrap or workspace creation. Each poll repeats the prior
maximum timestamp, pages to exhaustion, and de-duplicates by timestamp plus
canonical event identity/payload hash. It fails on truncation, timestamp
regression, an unexhausted page, or a missing expected barrier event. The final
daemon event checkpoint occurs after every workspace/command stop and
immediately before sandbox destruction; destroy and leak inspection are proved
by runner/manager evidence because sandbox event queries no longer exist.
Every authored runtime request has an exact trace join. Manager, trusted
control, and observers remain aggregate unless their native responses provide
exact IDs.

The evidence manifest contains a signal coverage matrix and checkpoint digests
for bootstrap, fan-out, all primary publishes, conflict winner, rejected loser,
retry, network phases, final regression, and cleanup. Physical layer count is
not used as a correctness assertion when autosquash is enabled; manifest
revision, content, and blame are authoritative.

### 7.7 Evidence persistence

Each invocation produces an immutable command artifact similar to:

~~~json
{
  "seq": 412,
  "run_id": "demo-20260714-001",
  "agent": "A06",
  "step": "A06.027",
  "scene": "conflict",
  "count_as": "agent",
  "started_at": "2026-07-14T10:12:01.422Z",
  "duration_ms": 184,
  "argv": ["sandbox-runtime-cli", "..."],
  "cli_exit": 0,
  "stdout": "{...}",
  "stderr": "",
  "parsed": {},
  "sandbox_id": "raw-sandbox-id",
  "workspace_session_id": "raw-workspace-id",
  "command_session_id": null,
  "request_id": "demo-20260714-001-A06.027-1",
  "expectation": {},
  "verdict": "passed"
}
~~~

Raw artifacts are never rewritten. manifest.json stores their SHA-256 digests,
scenario and generator hashes, the expected-final.json digest, counts,
assertions, execution verdict, cleanup verdict, and overall run verdict.

The checked-in root expected-final.json is the independent, pre-run content
oracle: a lexicographically sorted array of every expected shared path and
SHA-256. It explicitly excludes .git internals, caches, logs, command output,
run evidence, and other generated ephemera. Normal plan generation and every
live run treat it as read-only. Its reviewed digest is embedded in
scenario.compiled.json before sandbox provisioning and copied byte-for-byte
into run evidence; no actual run tree may create or update it. Final
verification fails on a missing, extra non-excluded, or different shared file.
The retained storefront and preview hashes are derived from this verified tree.

events.ndjson is the normalized append-only replay source. Its rows have a
monotonic sequence number and point to raw evidence; they never replace it. A
torn final line after interruption is ignored during replay and recorded as a
recovery warning.

### 7.8 Cleanup

The runner tracks every sandbox, explicit workspace, command session, and
forwarded preview. Normal completion, assertion failure, SIGINT, and SIGTERM
all enter bounded cleanup.

Cleanup order:

1. stop explicit-session servers;
2. poll their commands terminal;
3. destroy explicit no-op sessions;
4. destroy the presentation sandbox;
5. inspect for leaked resources;
6. atomically write the terminal projection and manifest.

Mutating operations are not automatically retried when their outcome is
unknown. For an unknown cleanup response, inspect the authoritative resource
list first. If the resource is still present, development mode permits one
recorded idempotent reissue; if absent, record reconciled success; if inspection
is inconclusive, cleanup is unknown. A qualification run that needs any reissue
fails qualification even if the second attempt succeeds. Cleanup errors record
leaked IDs and exact remediation commands. Unit/live fault tests cover failure
at every cleanup stage, repeated SIGINT, already-absent resources, unknown
responses, and inspection failure.

## 8. Workstream 2 — Generate the scripts

### 8.1 Source of truth

recipes.py contains explicit ordered Python data for A01–A10. It is concise
enough to review but does not hide calls behind a generic DSL. Each recipe
constructs plan records from named helpers such as read_file, write_payload,
edit_payload, run_check, expected_red, green_test, and release_anchor.

Payload files contain the actual HTML, CSS, JavaScript, test code, expected
fragments, and edit arrays. Generated JSONL plans and call-budget.json are
checked in so reviewers can inspect the complete operation set and actual
derived allocation without running Python.

generate_scripts.py supports:

~~~text
python3 generate_scripts.py --write
python3 generate_scripts.py --check
~~~

“--write” generates normalized JSON with fixed key order and one trailing
newline. “--check” regenerates in a temporary directory and byte-compares every
plan and budget file. Generation does not read clocks, UUIDs, environment
ordering, directory enumeration order, or network state.

Oracle updates use a separate, explicit review path:

~~~text
python3 update_oracle.py --from-tree OFFLINE_TREE --write
~~~

The command accepts only an offline materialization, prints the complete
path/hash diff, and requires the explicit write flag. It never reads runs/.
Plan generation cannot invoke it. Review and check in the oracle change
separately; the scenario compiler then pins its digest. test-inventory.json
follows the same frozen pre-run rule and may change only with an explicit
inventory update and review.

### 8.2 Storefront implementation

The generated workload builds a polished offline storefront with:

- semantic application shell and lightweight client-side routing;
- responsive tokens, layout, typography, focus, motion, and component styles;
- deterministic product, category, variant, inventory, and pricing fixtures;
- catalog grid, product detail, variant selection, sorting, and pagination;
- search, URL-backed facets, empty states, and result counts;
- wishlist and recommendations;
- integer-money cart, promotion, tax, shipping, and inventory rules;
- validated multi-step checkout and deterministic order receipt;
- keyboard and screen-reader behavior;
- reduced motion and performance checks;
- local node:http preview server;
- unit, integration, link, asset, accessibility, and HTTP smoke tests.

There is no package installation, image pull during the run, CDN, external
font, third-party request, or test that depends on the public internet.

### 8.3 Agent recipe responsibilities

| Agent | Durable output | Required proof cycle |
| --- | --- | --- |
| A01 Foundation | HTML shell, app entry, routes, local server | Broken route red → router patch → navigation and HTTP green |
| A02 Design system | Tokens, layout, responsive component styles | Missing token red → small CSS patches → viewport/style green |
| A03 Product data | Products, variants, inventory, money fixtures | Invalid fixture red → schema/data fixes → deterministic-data green |
| A04 Catalog/PDP | Grid, cards, PDP and variant interaction | Selection/render red → implementation → catalog green; network participant |
| A05 Search/facets | Search index, URL facets, sort and empty state | Facet edge-case red → patch → URL/state green |
| A06 Cart/pricing | Cart, promotion, tax, shipping, commerce config | Shipping boundary red → patch → pricing green; conflict winner |
| A07 Wishlist | Persistence and recommendations | Duplicate/persistence red → patch → wishlist green |
| A08 Checkout | Validation, steps, review, receipt | Validation red → patch → checkout green; rejected attempt and retry |
| A09 Accessibility | Keyboard, live regions, reduced motion, budgets | Accessibility/performance red → patch → audit green; network participant |
| A10 QA | Cross-feature status and full regression suite | Integration failures → targeted diagnostics → all-suite green |

Every lane MUST include genuine context reads, multiple small mutations,
syntax/build checks, a targeted red-patch-green cycle, and a final feature
test. Reads or reruns inserted solely to inflate the count are invalid.

### 8.4 Static plan validator

Validation fails before sandbox creation when any of these is true:

1. the lanes are not exactly A01 through A10;
2. the total is outside 350–500, the derived per-agent/category matrix differs
   from call-budget.json, or its digest is stale; 350–449 emits a visible
   quality warning but remains valid;
3. IDs are duplicated, ordinals are non-contiguous, a dependency is missing,
   or the dependency graph cycles;
4. an operation is outside the allowlist;
5. a payload is missing, stale by SHA-256, a symlink, outside the demo root,
   contains NUL, or exceeds the configured argv limit;
6. file_edit has empty old text, identical old/new text, or an ambiguous match
   without explicit replace_all intent;
7. an expected-red test has no exact inventoried failing subtest/reason, permits
   an infrastructure-error signature, or has no later relevant mutation and
   exact-inventory green rerun with the same test_cycle;
8. a test repeats on an unchanged lane revision unless `final_regression` is
   true on an A10.final exact-inventory test; any other use of that flag fails;
9. a payload repeats a state already established by earlier plan rows, a
   mutation effect is empty or contradictory, or a mutating exec lacks scoped
   effects.paths;
10. a counted command is sleep-only, true-only, echo-only, package install,
    network download, random, or wall-clock dependent; the anchor ready marker
    is the sole echo-like exception;
11. release can occur with an earlier lane row in flight;
12. blame is requested before the relevant publish;
13. host/runtime identifiers are interpolated into shell text;
14. purpose, scene, or expectation is absent, or a serialized count/provenance
    value disagrees with its generator-derived value.

At runtime, the runner compares live pre/post digests for every declared path,
checks the full workspace diff for undeclared changes, and associates the new
lane revision with later test rows. A successful mutation that changes nothing,
an unexpected path, or an unchanged non-final test rerun fails the scenario.

## 9. Workstream 3 — Test, repair, and fine-tune

### 9.1 Test ladder

Testing proceeds in this order. A later level does not start while an earlier
level has unexplained failures.

1. **Generator unit tests**
   - deterministic byte-for-byte generation;
   - 350–500 total, preferred-band warning, and derived category counts;
   - all validator rejection cases;
   - payload containment and hash checks.
2. **Runner unit tests with a fake subprocess adapter**
   - exact argv construction, multiline payloads, JSON parsing;
   - CLI versus child versus publication verdicts;
   - per-lane serialization and cross-lane concurrency;
   - running-to-terminal behavior;
   - cancellation and cleanup precedence;
   - event replay, torn-line recovery, and blame joins.
3. **Offline storefront materialization**
   - materialize the expected final tree outside a sandbox;
   - compare its sorted path/SHA-256 inventory to expected-final.json;
   - run node syntax checks and node --test;
   - use the existing Playwright installation at 375 and 1440 px to exercise
     routing, search/facets, product variants, wishlist, cart totals/promotions,
     checkout validation, order receipt, keyboard use, and reduced motion;
   - verify links/assets, local HTTP behavior, no body overflow, no unexpected
     console/network error, and no serious/critical accessibility finding;
   - prove there are no external or package-install dependencies.
4. **Existing focused live canaries**
   - rider command defers workspace finalization;
   - gated command lifecycle;
   - line-disjoint concurrent merge;
   - published file blame;
   - same-port network isolation;
   - observability snapshot and cleanup.
5. **New terminal truth spikes**
   - one anchor, scoped edit, publish, read, and blame;
   - ten anchors and ten disjoint registry edits;
   - A06/A08 atomic conflict and fresh retry;
   - shared collision and two isolated servers;
   - request-ID, snapshot, events, cgroup, trace, and layerstack correlation.
6. **Lane tests**
   - run A01 through A10 independently;
   - run the A06/A08 pair;
   - run the A04/A09 network pair;
   - run a ten-lane merge spike.
7. **Full golden run**
   - execute every validated authored row from a fresh sandbox;
   - verify all evidence and cleanup gates.
8. **Presentation qualification**
   - three consecutive clean golden runs on the presentation machine;
   - refresh, disconnect/reconnect, pause/view navigation, interrupt, and restart
     rehearsal;
   - desktop, projector, tablet, and mobile browser checks.

Existing E2E helpers and tests to reuse include:

- e2e/harness/runner/cli.py;
- e2e/harness/runner/direct_daemon.py;
- e2e/harness/runner/cleanup.py;
- e2e/runtime/file/helpers.py;
- e2e/runtime/command/test_git_policy_easy.py;
- e2e/runtime/file/concurrent/test_concurrent_session.py;
- e2e/runtime/file/blame/test_blame_session.py;
- e2e/runtime/network_isolation/test_network_isolation.py;
- e2e/runtime/workspace_session/test_exec_finalize.py.

### 9.2 Defect classification

Every failure writes one immutable defects/SEQ-STEP.json raw-evidence record.
It starts with `status: untriaged` and `classification: null` and is never
overwritten, so multiple failures survive. Each record contains:

- null classification pending triage;
- expected and actual values;
- redacted argv;
- CLI exit, stdout, stderr, and parsed response;
- sandbox, workspace, command, request, trace, and step IDs;
- surrounding event sequence and observability checkpoints;
- content and manifest hashes before and after;
- suggested smallest reproduction command.

Triage and repair append diagnoses.ndjson rows that reference the immutable
defect ID, one required classification from the enum below, root cause,
patch/test references, and disposition. Append-only triage-index.ndjson chains
each diagnosis digest to the preceding index digest. The terminal manifest
indexes raw defects and any triage rows present when it closes and is never
rewritten; later triage is discoverable through the chained index. A successful
rerun uses a new run directory and does not erase the original defect.

Use exactly these classifications:

- script_or_payload;
- runner_or_artifact;
- cli_projection_or_client;
- runtime_product;
- environment_or_stale_binary;
- transient_host_load.

### 9.3 Repair procedure

When a failure appears:

1. preserve raw evidence and the terminal manifest unchanged, appending only
   diagnoses.ndjson and triage-index.ndjson records;
2. reproduce the contract in the smallest fresh sandbox;
3. run the nearest focused existing E2E test;
4. inspect raw operation response, trace, events, content, and layer state;
5. patch the smallest responsible layer;
6. add a regression test at that layer;
7. rebuild/restart affected binaries or daemons;
8. rerun the focused test and failed lane from a fresh sandbox;
9. rerun paired and ten-lane gates when the fix affects concurrency;
10. perform a new full golden run after all focused failures are resolved.

Do not resume a partially completed scenario after changing product code. Do
not weaken an expectation, add a blind retry, or change the story to conceal a
product defect.

Likely early defects to test explicitly:

- wrong CLI argv ordering or malformed JSON projection;
- stale daemon binary missing publication-rejection fields;
- anchor finalizing before rider operations drain;
- file_edit old text missing or matching more than once;
- destroying an explicit session while its command is active;
- querying blame while changes are still live;
- absent conflict path in the public response;
- request ID not joining to trace/events;
- isolated image missing the required server runtime;
- preview server bound to the wrong interface or forwarding URL;
- autosquash invalidating physical-layer assumptions;
- payload exceeding the practical argv limit;
- browser fetching the wrong relative run.json and rendering a blank page.

### 9.4 Retry policy

Never automatically retry:

- file writes or edits;
- anchor release;
- explicit session create, or destroy except for the one inspected idempotent
  development cleanup reissue defined in section 7.8;
- unknown-outcome mutation;
- semantic test failure;
- conflict verdict;
- wrong content, blame, revision, or cleanup state.

Read-only observability transport calls MAY retry twice with bounded backoff.
During development only, one clearly recorded retry is allowed for a proven
host-load transient. A presentation qualification run must be clean without
semantic or hidden retries.

### 9.5 Fine-tuning

Tune from retained measurements, not guesses:

- keep one operation in flight per lane and ten lanes active;
- accumulate at least 20 successful development samples for each operation
  class: file/read, file/mutate, exec/test, publish/finalize, observability, and
  cleanup;
- set each timeout to clamp(3 × observed p95, class floor, class cap), using
  5–60 seconds for file/observability, 30–600 seconds for exec/publish, and
  10–120 seconds for cleanup; intentional anchors and servers use their named
  scenario lifetime plus the outer watchdog;
- use barriers for correctness and at_ms only for readable pacing;
- sample aggregate cgroup at 500 ms;
- shorten noisy command output at capture/render time without discarding raw
  artifacts;
- keep the audience-visible execution between 90 and 120 seconds;
- use real tests and application work rather than sleeps or synthetic CPU load;
- adjust script timing or payload granularity only if assertions, semantic
  coverage, and the 350–500 call band remain intact;
- show only selected-agent detail so ten-lane telemetry stays legible.

Every timing sample is keyed by the combined plan, payload, oracle, CLI binary,
image, and host fingerprint; stale or nonmatching samples cannot set a timeout.
Freeze scenario.compiled.json, plan/payload/oracle digests, timeout values, CLI
realpaths and SHA-256s, capability-help digests, image ID, and host fingerprint
before qualification. Then require three consecutive clean runs without
semantic, transport, or cleanup retry. The atomic
runs/qualifications/QUALIFICATION_ID.json indexes the three immutable run
manifests and records actual call matrices, audience-visible durations, samples,
retry counts, verdicts, cleanup, and the common frozen fingerprint.

The UI timer and qualification interval begin at `execution-start`, emitted
immediately before run-owned sandbox provisioning after static preflight. They
end at `execution-terminal`, emitted only after final regression, retained
preview capture, cleanup, and leak inspection. Each qualification run MUST be
within 90–120 seconds; an otherwise successful out-of-band run fails
qualification. The fingerprint-matched development sample pool, not only the
three runs, supplies p95.

## 10. Workstream 4 — Produce the demo HTML

### 10.1 Delivery modes

The same light-theme control room supports three explicit modes:

| Mode | Entry | Behavior |
| --- | --- | --- |
| Sample | index.html or ?mode=sample | Embedded simulated fixture; always labeled |
| Live | ?mode=live&run=RUN_ID | Polls that run’s projection; never falls back to sample |
| Recorded | generated/RUN_ID/demo.html | Embedded projection from a successful real run |

Mode resolution is deterministic:

1. a valid embedded recorded projection selects recorded mode;
2. “?mode=live&run=RUN_ID” selects live mode;
3. no mode or “?mode=sample” selects sample mode;
4. every other value shows a visible invalid-mode error.

The document shell renders before data loading. Live fetch failure shows a
visible retry panel and the last valid projection, if any. It MUST never become
blank and MUST never silently replace failed live data with simulated data.

### 10.2 Projection contract

run.json is a versioned, bounded UI projection:

~~~json
{
  "schema_version": "multiagent-demo/v1",
  "projection_seq": 404,
  "run": {
    "id": "demo-20260714-001",
    "status": "running",
    "title": "FlashCart: ten agents, one workspace",
    "started_at": "2026-07-14T10:10:53.302Z",
    "updated_at": "2026-07-14T10:12:01.422Z",
    "elapsed_ms": 68120,
    "sandbox_id": "raw-sandbox-id",
    "scenario_sha256": "sha256",
    "calls": {
      "completed": 404,
      "planned": 477,
      "failed": 0,
      "engine": 286,
      "diagnostic": 0
    },
    "shared_revision": 12
  },
  "presentation": {
    "active_scene": "conflict",
    "scenes": [
      {
        "id": "fanout",
        "ordinal": 1,
        "state": "completed",
        "title": "Ten agents fork from one immutable base.",
        "focus_agent": "A01",
        "entered_seq": 42,
        "completed_seq": 91,
        "checkpoint": {
          "summary": {},
          "agents": [],
          "evidence_refs": []
        },
        "narrative_ids": []
      }
    ]
  },
  "agents": [],
  "evidence": {},
  "narrative": [],
  "artifacts": {}
}
~~~

Each agent projection includes:

- stable ID, role, fixed color token, and planned/completed call counts;
- lane state and current operation purpose;
- primary and retry workspace attempts;
- raw workspace, command, and request IDs;
- CLI duration and child runtime;
- child process outcome and publication outcome as separate fields;
- evidence references and latest bounded resource sample.

The A08 rejected attempt must be representable as “process exited 0” and
“publication rejected: source_conflict” at the same time.

Projection bounds:

- latest 100 display events;
- up to 240 resource samples, covering 120 seconds at 500 ms;
- latest command per agent plus selected evidence commands;
- latest blame, trace, layerstack, and preview summaries;
- one immutable bounded checkpoint for every reached scene;
- relative links only to curated presentation-safe artifacts.

The runner captures each scene checkpoint after its gate passes. Scene rewind
and recorded playback render those checkpoints, never inferred current values
or hard-coded sample metrics.

Live polling permits one request in flight. It schedules the next request with
setTimeout only after the prior request finishes, uses cache “no-store” and a
bounded timeout, validates schema and the expected run ID, and accepts only a
projection_seq greater than the last accepted sequence. Duplicate or older
responses are ignored. HTTP, timeout, parse, schema, or sequence failure keeps
the last valid projection and changes the connection state. Polling refetches
when the tab becomes visible and stops when the run is terminal.

### 10.3 Provenance model

Artifact data may contain only these provenance enums:

- public_cli;
- telemetry;
- sandbox_preview;
- trusted_session_control;
- runner_join;
- simulated_narrative;
- presentation_annotation.

The HTML maps enums to fixed human labels. Artifact content cannot supply
arbitrary badge HTML or override provenance wording.

Recorded mode changes only the global mode badge and the sandbox_preview label
to “Recorded real preview.” Real CLI, Real telemetry, Trusted session control,
Runner mapping, and Staged narrative keep their original classification.

Raw evidence remains private to the run directory. The live server and exporter
expose only separately generated manifest entries shaped like:

~~~json
{
  "id": "command:A08.036",
  "kind": "public_cli",
  "path": "artifacts/A08.036.json",
  "sha256": "sha256",
  "content_type": "application/json",
  "byte_length": 3812,
  "safe_for_demo": true,
  "redacted": true
}
~~~

Only safe_for_demo entries may be served or packaged. Projection redaction does
not make an arbitrary raw stdout/stderr file safe for presentation.

### 10.4 Scene gates

The page contains five audience scenes, each unlocked only by evidence:

1. **Fan-out** — snapshot proves ten active primary workspaces.
2. **Merge and blame** — all ten non-conflicting primary changesets publish and
   line-disjoint registry edits retain ten mapped owners.
3. **Conflict and discard** — exact rejection class, unchanged revision,
   absent attempt-only loser files, retained winner content and blame, then a
   successful fresh retry integrates checkout against the new head.
4. **Port isolation** — real shared collision plus two successful isolated
   forwarding probes.
5. **Evidence and storefront** — final test suite, preview, artifacts, and
   cleanup all pass.

Automatic playback follows reached scenes. Previous/next can navigate only
scenes already reached. Pausing playback does not affect the run.

### 10.5 UI composition

Preserve the existing warm light theme and compact layout:

- run header with mode, scene, elapsed time, and presenter controls;
- six proof metrics including completed / actual planned calls;
- ten compact agent lanes with state, current purpose, calls, and duration;
- selected-agent command detail with process/publication separation;
- live or recorded storefront preview with a visible loading/error state;
- staged narrative panel with an explicit simulated label;
- tabbed evidence for CLI, blame, trace, events, layers, and resources;
- raw IDs and JSON behind disclosure;
- a permanent provenance footer.

Do not render ten large charts. Use compact lane values/sparklines and one
selected-agent resource panel.

### 10.6 Live server and recorded export

run_demo.py serves only loopback by default and provides:

~~~text
/multiagent/                 index.html
/multiagent/runs/RUN_ID/run.json
/multiagent/runs/RUN_ID/artifacts/...
/multiagent/runs/RUN_ID/preview/...
/multiagent/runs/RUN_ID/live-preview/WORKSPACE_REF/4173/...
~~~

“/multiagent” redirects to “/multiagent/”. The server disables directory
indexes, rejects path traversal and symlink escapes, uses correct MIME types,
adds X-Content-Type-Options “nosniff”, and sends Cache-Control “no-store” for
live HTML and projections. Digest-named recorded artifacts may use immutable
caching. Startup GETs the printed live URL and requires status 200, HTML content
type, and a visible shell marker before reporting ready.

The live-preview route is a constrained reverse proxy, not a second preview
backend. It resolves only a run-owned symbolic workspace and allowlisted port,
uses manager inspect/daemon_http metadata and the repository’s existing shared
or isolated forward-route helper, and preserves path, query, status, and safe
content headers while stripping hop-by-hop headers. It cannot proxy an
arbitrary origin. The browser never constructs daemon /s or /forward URLs and
never receives daemon credentials. Proxy integration tests cover shared and
isolated routes, query strings, 404/500 responses, content types, traversal,
unknown workspaces, stopped sessions, and cleanup transition to retained
preview.

`final-preview` is not user input: the runner binds it only to the live
`A10.final.workspace` after `A10.final.preview` reports its ready marker on
4173. The mapping is removed as soon as that command stops. The server is an
authored A10 command, its stop/poll is tracked, and failure cleanup terminates
it before sandbox destruction. No earlier lane or disposable network session
can become the storefront producer.

index.html resolves live URLs with the URL API and document.baseURI, never
string concatenation. It validates that the response run ID matches the query.
The runner prints the complete live URL including mode and run.

Before sandbox cleanup, the runner captures a final real storefront screenshot
and a content-hashed retained preview package. Live mode uses the forwarding
route while it is available and visibly switches to the retained preview after
cleanup; failure shows a status card rather than an empty iframe.

The export command reads a terminal successful manifest, verifies every source
digest, copies only presentation-safe artifacts and retained preview files,
embeds the bounded projection into a copy of index.html, and atomically replaces
the generated/RUN_ID directory. It then writes export-manifest.json with the
path, size, and SHA-256 of demo.html, the safe manifest, and every artifacts/
and preview/ output (excluding only export-manifest.json itself), re-reads the
installed directory, rejects unlisted files, and rehashes every entry. The
projection is base64-encoded UTF-8 JSON in
exactly one script element with type “application/octet-stream”, ID
“demo-data”, and data-encoding “base64”, so content such as “</script>” cannot
terminate the element. Decode or schema failure leaves the static error shell
visible. Failed or unclean runs cannot be exported as successful.

Recorded-mode Playwright qualification starts only after the runner process is
gone and the sandbox is confirmed absent. It serves generated/RUN_ID from a
plain static server, verifies export-manifest.json first, rejects every
unexpected browser request, and exercises the full recorded UI and retained
storefront without contacting a runner or sandbox endpoint.

### 10.7 Browser safety, accessibility, and responsiveness

The HTML MUST:

- contain a visible brand/header and role=status loading section in source HTML;
- contain a noscript role=alert message and disabled controls before boot;
- use a small independent watchdog that replaces loading with a visible error
  unless initialization sets data-demo-ready;
- catch top-level initialization and polling errors;
- never hide the body while JavaScript loads;
- use textContent for artifact and narrative strings;
- never inject raw command output with innerHTML;
- accept artifact URLs only when relative or expected loopback preview URLs;
- render retained HTML only inside the preview frame, never the parent DOM;
- give the iframe a title, forbid top navigation/popups, and use sandbox
  “allow-scripts allow-forms” without allow-same-origin; storefront payloads use
  bundled classic scripts, and tests reject an ES-module dependency;
- contain no external scripts, fonts, images, analytics, CDN, or build step;
- render a usable shell and explicit error for malformed data;
- keep the last valid projection if a later poll is malformed;
- redact likely credentials before projection and render;
- provide skip navigation, semantic landmarks, visible focus, and non-color
  status text;
- implement tablist/tab/tabpanel relationships, roving tabindex, and
  Left/Right/Home/End navigation for scene and evidence tabs;
- use role=status for loading/connection state and role=alert for fatal errors;
- announce only scene, connection, selected-agent terminal state, and run
  terminal state, never every metric poll;
- maintain 4.5:1 normal-text contrast, 44×44 px mobile targets, and 16 px mobile
  body text;
- label internal scroll regions and make wide event/trace tables focusable;
- provide a table alternative to charts;
- honor prefers-reduced-motion and disable autoplay when it is active;
- avoid body-level horizontal overflow at 375, 768, 1024, and 1440 px widths.

### 10.8 HTML tests

Use the repository’s existing Playwright installation rather than adding a
browser dependency. Tests cover:

- sample, live, recorded, loading, malformed, disconnected, failed, and passed
  modes;
- invalid mode, JavaScript disabled, missing script, HTTP 404, empty HTTP 200,
  truncated JSON, and unsupported schema;
- live failure never falling back to sample;
- delayed out-of-order projections never regressing the accepted sequence;
- ten agents, five gated scenes, and exact call counts;
- scene rewind using retained checkpoints rather than sample data;
- process success plus publication rejection rendered simultaneously;
- hostile event and export text, including a closing script tag and event
  handler markup, rendered as text and never executed;
- missing preview and degraded telemetry fallbacks;
- keyboard navigation, refresh, reduced motion, and responsive widths;
- no console error or unhandled promise rejection;
- screenshot baselines for conflict, network, and final evidence on desktop and
  mobile;
- no serious or critical automated accessibility findings;
- every displayed curated evidence link returning 200 with the manifest
  SHA-256, and no raw non-allowlisted path being served;
- a real successful run showing planned / planned within 350–500, ten owners,
  one atomic rejection, two isolated servers, final green tests, and clean
  cleanup.

## 11. Command-line interface

The implementation exposes these operator commands:

~~~sh
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/demo/multi-agent

python3 generate_scripts.py --write
python3 generate_scripts.py --check

python3 run_demo.py validate
python3 run_demo.py truth-spike
python3 run_demo.py run --serve --host 127.0.0.1 --port 8765
python3 run_demo.py qualify --runs 3
python3 run_demo.py replay runs/RUN_ID --serve --host 127.0.0.1 --port 8765
python3 run_demo.py export-html runs/RUN_ID \
  --output-dir /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/multiagent/generated/RUN_ID
~~~

run prints the run ID, demo URL, artifact directory, authored/engine call
counts, execution verdict, cleanup verdict, and overall verdict. There is no
keep-on-failure path in the demo runner; diagnosis uses immutable evidence and
fresh reduced reproductions so cleanup remains an invariant.

`qualify --runs 3` freezes one fingerprint before the first run, executes three
fresh runs serially, and rejects any fingerprint drift, nonconsecutive foreign
run, retry counter, non-passing execution/cleanup verdict, leak, duration outside
90–120 seconds, or manifest mismatch. It verifies recorded mode with the runner
and sandbox absent, then atomically writes the qualification record; interruption
or any failed child run leaves no passing qualification file.

## 12. Implementation sequence and gates

Every checkbox below is a hard phase gate, not an aspirational task list. Check
an item only after recording its command, immutable artifact path, digest, and
verdict in the implementation log. **No work in phase N+1 may begin until every
phase N box is checked.** If a later code/input change or failure invalidates
evidence, uncheck the affected item and every dependent later-phase gate before
continuing. Phase 5 must be fully checked before declaring implementation done.

### Phase 0 — Contract foundation

Implement and test the request-ID override, verify current public CLI output,
and complete the one-workspace truth spike.

Acceptance checklist:

- [ ] P0.1 Request-ID tests prove default UUID, explicit valid value, duplicate
  rejection, and every invalid-value boundary.
- [ ] P0.2 A fresh live canary joins one supplied request ID to its exact trace
  and event evidence.
- [ ] P0.3 Public CLI canaries freeze command, child, publication, structured
  error, blame, snapshot, cgroup, events, trace, and layerstack response shapes.
- [ ] P0.4 The one-workspace edit/publish/read/blame truth spike passes from a
  run-owned empty workspace.
- [ ] P0.5 Normal and interrupted canaries leave no sandbox, workspace, command,
  route, or local CLI process.

### Phase 1 — Deterministic generator

Create storefront payloads, recipes, validator, plans, and budget.

Acceptance checklist:

- [ ] P1.1 `generate_scripts.py --check` is byte-stable and matches all checked-in
  plans and call-budget.json.
- [ ] P1.2 The validator proves exactly A01–A10 and 350–500 authored public CLI
  calls, warns below preferred 450, and enforces no per-agent numeric quota.
- [ ] P1.3 Every payload, scoped effect, dependency, attempt ref, test cycle,
  category, provenance, and no-padding rule passes positive and rejection tests.
- [ ] P1.4 The exact frozen test inventory rejects wrong-red, infrastructure-error,
  zero-test, and unexpected skip/todo/cancelled cases.
- [ ] P1.5 Offline materialization matches the separately reviewed
  expected-final.json path/hash oracle with no missing, changed, or extra file.
- [ ] P1.6 Node and Playwright exercise all specified storefront flows, widths,
  accessibility, links/assets, and offline/no-install behavior successfully.
- [ ] P1.7 A reviewed pre-run artifact records the independently frozen oracle and
  inventory digests; generation and execution cannot mutate either, and negative
  tests prove `update_oracle.py` rejects `runs/`, non-offline or symlinked input,
  and any write lacking explicit authorization.

### Phase 2 — Runner and proof scenes

Implement scheduler, anchors, correlation, artifacts, observer, conflict,
network isolation, replay, and cleanup.

Acceptance checklist:

- [ ] P2.1 Runner unit tests prove cancellable Popen handling, centralized
  redaction, exact CLI classification, per-lane order, and cross-lane concurrency.
- [ ] P2.2 Snapshot proves ten gated automatic workspaces active simultaneously.
- [ ] P2.3 All ten primary publishes merge and registry blame retains ten distinct
  raw owners with explicit run-local A01–A10 mappings.
- [ ] P2.4 The A06/A08 spike proves one atomic source-conflict discard, no partial
  loser files or revision advance, then a successful fresh-head A08 retry.
- [ ] P2.5 Shared port collision and two isolated 4173 servers pass, and destroyed
  experiments change neither shared content nor blame.
- [ ] P2.6 Signal coverage proves exact request traces, inclusive event watermark
  handling, 500 ms cgroup series, checkpoints, layers, timing, and blame.
- [ ] P2.7 Replay/torn-line, SIGINT, timeout, cancellation, unknown-outcome, and
  every cleanup-stage fault test passes without a resource or process leak.
- [ ] P2.8 Parameterized tests make every preflight rejection branch fail before
  show-sandbox provisioning, including image/no-pull, empty-root, autosquash,
  ignored-path, CLI-help/digest, proxy, and cleanup checks; one fresh live
  preflight report proves the passing path.

### Phase 3 — Full script execution and repair

Run individual lanes, paired lanes, ten-lane spike, then the full workload.
Apply the defect procedure for any script, CLI, or runtime bug.

Acceptance checklist:

- [ ] P3.1 A01–A10 each pass independently, then A06/A08, A04/A09, and the
  ten-lane merge spike pass from fresh sandboxes.
- [ ] P3.2 One clean full run completes every validated authored row; the actual
  matrix matches call-budget.json and the authored total remains 350–500.
- [ ] P3.3 All primary merges, atomic conflict/retry, isolation, final A10 exact
  inventory, and expected-final.json tree/hash assertions pass together.
- [ ] P3.4 Every discovered script, runner, CLI, runtime, or environment defect has
  immutable evidence, a classification, smallest reproduction, and regression.
- [ ] P3.5 A fresh post-repair full run has passing execution and cleanup verdicts,
  complete evidence coverage, and zero leaked resources/processes.

### Phase 4 — Artifact-driven HTML

Wire index.html to the projection, add explicit modes and error states, implement
recorded export, and complete browser tests.

Acceptance checklist:

- [ ] P4.1 Sample, live, and recorded modes render correct provenance and every
  loading, malformed, disconnect, failure, cleanup, and recovery state nonblank.
- [ ] P4.2 Monotonic polling, scene gates, pause/rewind, selected-agent evidence,
  and live-to-retained preview transition match immutable run artifacts.
- [ ] P4.3 Desktop/mobile commerce flows, keyboard use, reduced motion,
  responsiveness, contrast, and automated accessibility checks pass.
- [ ] P4.4 Hostile projection/artifact text cannot execute; raw files, credentials,
  traversal, unsafe URLs, and unexpected browser requests are rejected.
- [ ] P4.5 Export rehashes every installed output; recorded Playwright passes from
  a plain static server with the runner and sandbox absent.
- [ ] P4.6 Required desktop/mobile screenshots have no blank panels, overflow,
  unexpected console errors, or unhandled rejections.
- [ ] P4.7 Export rejection tests cover failed, unclean, and nonterminal manifests,
  source-digest drift, unlisted or modified installed files, symlink/path escape,
  and interruption during atomic replacement; none produces a new passing export
  or damages the prior valid export.

### Phase 5 — Presentation qualification

Tune using measured p95 timings and rehearse failure/recovery.

Acceptance checklist:

- [ ] P5.1 Fingerprint-matched sample pools contain at least 20 successes per
  operation class and justify every frozen timeout from measured p95.
- [ ] P5.2 Scenario, plan, payload, oracle, inventory, CLI binaries/help, image,
  host, timeouts, runner/helpers, generator/updater, trusted adapter, control-room
  and export sources, browser tests, and Python/Node/Playwright/browser versions
  remain identical in timing-sample and qualification fingerprints.
- [ ] P5.3 Three consecutive fresh presentation-machine runs each complete in
  90–120 seconds with 350–500 authored calls and zero semantic, transport,
  cleanup, or hidden retry.
- [ ] P5.4 Each run independently proves ten workspaces/owners, atomic reject and
  retry, shared collision, two isolated servers, full observability, exact final
  tests/tree, and clean execution plus cleanup verdicts.
- [ ] P5.5 Refresh, disconnect/reconnect, pause/rewind, projector/mobile,
  SIGINT/restart, and retained-recording rehearsals pass.
- [ ] P5.6 The atomically written qualification record indexes all three immutable
  manifests, and its runner-independent recorded package passes final rehash and
  browser verification.
- [ ] P5.7 Fault injection proves fingerprint drift, foreign interleaving, any
  retry, failed verdict, leak, timing violation, manifest mismatch, and
  interruption cannot write a passing qualification record; the valid record
  binds exactly the three run-manifest digests and selected export manifest.

## 13. Definition of done

The implementation is complete only when all statements below are true:

- generation is deterministic and checked-in output exactly matches recipes;
- all generated authored public CLI calls run across A01–A10, with a validated
  total of 350–500 and a recorded warning when below the preferred 450;
- every authored call has a parsed real response and immutable evidence;
- snapshot proves ten automatic workspaces active concurrently;
- all durable storefront code is produced by the agent lanes from the bootstrap;
- all ten registry edits survive and blame maps to ten distinct raw owners;
- the A06 file_edit versus A08 exec_command overlap produces one real
  source_conflict rejection;
- rejection advances no shared revision and publishes none of A08’s files;
- A08 retries from a fresh head and publishes successfully;
- shared sessions collide on port 4173 while two isolated sessions both serve;
- destroyed experiment sessions leave shared content and blame unchanged;
- cgroup, time, events, traces, layerstack, snapshot, and blame evidence is
  retained and correctly labeled;
- final syntax, unit, integration, link, asset, HTTP, accessibility, and
  performance checks pass with the exact frozen inventory, no zero-test pass,
  and no unexpected fail, skip, todo, or cancellation;
- SIGINT and normal completion leave no sandbox, workspace, command, or preview
  leak;
- live HTML never silently substitutes sample data or renders blank;
- sample data, staged dialogue, trusted lifecycle, runner joins, and real
  evidence are visibly distinct;
- recorded demo export verifies its source manifest and works from a plain
  static HTTP server without the runner or sandbox, with every installed output
  covered by and reverified against export-manifest.json;
- three consecutive presentation-machine runs each complete from
  execution-start through cleanup and leak inspection in 90–120 seconds with no
  semantic, transport, or cleanup retry and one atomic qualification record.

Any failed item leaves the project in implementation or repair status; it must
not be represented as a successful demo.

## 14. Out of scope

This delivery does not add:

- a general agent protocol or real agent-to-agent messaging;
- a public create/destroy workspace-session CLI;
- arbitrary committed-layer undo;
- a general workflow engine, distributed scheduler, or message bus;
- a WebSocket service or new browser state framework;
- a React console migration;
- external package installation during the demo;
- fabricated telemetry, blame identity, conflict details, or execution results.
