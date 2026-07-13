# FlashCart Multi-Agent Demo — Implementation Specification

| Field | Value |
| --- | --- |
| Status | Ready for implementation |
| Source design | [DESIGN.md](./DESIGN.md) |
| Visual baseline | [Light-theme control-room prototype](./index.html) |
| Primary implementation | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/demo/multi-agent |
| Presentation implementation | /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/multiagent |
| Authored workload | 10 agent lanes, exactly 389 counted public CLI calls |
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
workspaces open concurrently, performs 389 authored operations, publishes a
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
├── run_demo.py
├── call-budget.json
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
    └── RUN_ID/
        ├── manifest.json
        ├── run.json
        ├── events.ndjson
        ├── scenario.compiled.json
        ├── commands/
        ├── observability/
        ├── blame/
        ├── preview/
        └── defect.json
~~~

The runs directory is generated and ignored by version control except for a
small documented fixture if browser tests require it.

### 5.2 Product prerequisite

The runtime CLI currently creates request IDs internally. Add one global
request-ID override through the current input-building path:

- accept a global “--request-id VALUE” on sandbox-runtime-cli;
- validate that the value is non-empty and within the gateway’s existing
  request-ID limits;
- pass it to the existing request builder that accepts an explicit ID;
- retain the current UUID behavior when the option is omitted;
- add unit coverage for default, explicit, duplicate, and invalid values;
- add one live correlation test showing the supplied ID in trace/event output.

The runner uses IDs of the form:

~~~text
demo-RUN_ID-STEP_ID-ATTEMPT
~~~

If this patch is unavailable, the runner MAY still execute aggregate telemetry,
but the run cannot pass the “per-step trace correlation” acceptance item. The
HTML must label concurrent trace views as aggregate and MUST NOT guess.

### 5.3 Documentation and presentation repository

~~~text
ephemeral-sandbox-docs/multiagent/
├── DESIGN.md
├── IMPLEMENTATION_SPEC.md
├── index.html
└── generated/
    └── RUN_ID/
        └── demo.html
~~~

index.html is the source control room and static sample preview.
generated/RUN_ID/demo.html is produced from a successful real run and embeds a
bounded recorded projection so it remains viewable without the runner.

## 6. CLI and runner contract

### 6.1 Host process rules

Every CLI invocation MUST:

- use a subprocess argument array with host-side shell execution disabled;
- capture the exact redacted argv, process return code, stdout, stderr,
  monotonic duration, and parsed JSON;
- require exactly one valid JSON response object when the CLI succeeds;
- distinguish CLI transport success from the child command exit code;
- distinguish child process completion from workspace publication;
- write its raw evidence before evaluating the expectation;
- never record daemon authentication credentials.

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
    "output_contains": ["not ok"]
  },
  "test_cycle": "A06.shipping-boundary",
  "after": ["all-primary-workspaces-ready"],
  "at_ms": 12000,
  "count_as": "agent"
}
~~~

Required fields are schema_version, id, agent, ordinal, scene, phase, category,
purpose, op, args, expect, and count_as. Optional fields are workspace_ref,
command_ref, bind, test_cycle, after, and at_ms.

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
Retries bind new names and never overwrite the original mapping.

The expectation vocabulary is deliberately fixed:

- command_running;
- command_ok;
- expected_red;
- file_read;
- file_write;
- file_edit;
- publish_success;
- publish_reject;
- blame_owner;
- not_found;
- http_probe.

There is no expression language, arbitrary JSONPath, embedded Python, or
templated shell evaluation in a plan.

### 6.4 Counting rules

One counted row equals one spawned public sandbox CLI process with one parsed
response. The following do not count toward the 389:

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

The exact golden budget is:

| Agent | Workspace control | Inspect | Patch | Build/lint | Test/debug | Conflict/network/audit | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | 2 | 7 | 11 | 5 | 8 | 1 | 34 |
| A02 | 2 | 7 | 12 | 5 | 7 | 1 | 34 |
| A03 | 2 | 8 | 11 | 5 | 8 | 1 | 35 |
| A04 | 2 | 8 | 12 | 5 | 7 | 8 | 42 |
| A05 | 2 | 8 | 11 | 5 | 8 | 3 | 37 |
| A06 | 2 | 8 | 12 | 5 | 8 | 6 | 41 |
| A07 | 2 | 7 | 10 | 4 | 8 | 1 | 32 |
| A08 | 2 | 9 | 13 | 5 | 9 | 7 | 45 |
| A09 | 2 | 8 | 11 | 4 | 10 | 11 | 46 |
| A10 | 2 | 9 | 8 | 6 | 14 | 4 | 43 |
| **Total** | **20** | **79** | **111** | **49** | **87** | **43** | **389** |

The two ordinary workspace-control rows are each agent’s primary anchor and
release. A08’s fresh conflict retry anchor and release are scenario-specific
conflict/audit rows, preserving both the operation truth and the category
budget.

run.json and the HTML MUST report three separate totals:

- authored agent calls: completed / 389;
- engine, lifecycle, and telemetry interactions;
- unexpected diagnostic calls.

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
workspace ID.

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
                                                        ↘ REJECTED
REJECTED → RETRY_PENDING → ANCHOR_STARTING → ACTIVE → PUBLISHED
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

Cleanup failure adds cleanup_status “degraded” without replacing the original
run verdict.

### 6.7 Scheduler

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
- conflict-winner-published;
- nine-primary-publications-complete;
- conflict-retry-published;
- both-shared-network-probes-complete;
- both-isolated-servers-ready;
- all-feature-tests-green;
- final-regression-green.

Scene transitions are opened by barrier assertions, not wall-clock animation.

## 7. Workstream 1 — Implement DESIGN.md

### 7.1 Preflight

Before creating the presentation sandbox, run_demo.py validates:

- all three CLI binaries resolve and return compatible catalogs;
- the configured Node image is already local;
- the host workspace is new, empty, and inside the configured demo root;
- the direct-daemon adapter can create and destroy one isolated canary;
- snapshot, cgroup, events, trace, layerstack, file read, and blame respond;
- the request-ID override correlates to a trace;
- the preview route can forward a canary server;
- conflict proof paths are not ignored;
- manifest-revision assertions remain valid with the configured autosquash;
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

Nine primary changesets publish. A08’s first primary changeset is intentionally
rejected by the conflict proof, then a fresh A08 workspace reapplies the
checkout work against the new head and publishes.

After the retry, the runner verifies:

- all ten registry values are present;
- all expected agent-owned files exist;
- registry blame contains ten distinct raw workspace owners;
- every raw owner maps to the correct run-local agent;
- the raw owner remains visible beside the display mapping.

### 7.4 Cross-surface conflict and atomic discard

The conflict intentionally crosses operation surfaces:

1. A06 uses file_edit to change the seeded commerce threshold from 5000 to
   6000.
2. From the same base, A08 uses exec_command to run a checked-in local patch
   helper that changes 5000 to 7500. A08 also creates unrelated checkout files
   in the same workspace.
3. A06 publishes first.
4. A08’s anchor process exits zero, but publication MUST report
   publish_rejected true with class source_conflict.
5. The runner verifies that the manifest revision did not advance, the shared
   threshold remains 6000, every unrelated A08 file from the rejected
   changeset is absent, A06 blame remains, and the rejected workspace is gone.
6. A08 starts a fresh automatic workspace from the new head, applies the
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

Resource sampling MUST occur while workspaces exist. Workspace-scoped cgroup
failure marks that panel degraded; aggregate cgroup remains required. Physical
layer count is not used as a correctness assertion when autosquash is enabled;
manifest revision, content, and blame are authoritative.

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
scenario and generator hashes, final storefront hash, counts, assertions,
cleanup verdict, and run verdict.

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
unknown. Cleanup errors are recorded with leaked IDs and remediation commands.

## 8. Workstream 2 — Generate the scripts

### 8.1 Source of truth

recipes.py contains explicit ordered Python data for A01–A10. It is concise
enough to review but does not hide calls behind a generic DSL. Each recipe
constructs plan records from named helpers such as read_file, write_payload,
edit_payload, run_check, expected_red, green_test, and release_anchor.

Payload files contain the actual HTML, CSS, JavaScript, test code, expected
fragments, and edit arrays. Generated JSONL plans and call-budget.json are
checked in so reviewers can inspect the exact 389 operations without running
Python.

generate_scripts.py supports:

~~~text
python3 generate_scripts.py --write
python3 generate_scripts.py --check
~~~

“--write” generates normalized JSON with fixed key order and one trailing
newline. “--check” regenerates in a temporary directory and byte-compares every
plan and budget file. Generation does not read clocks, UUIDs, environment
ordering, directory enumeration order, or network state.

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
2. the total is not exactly 389 or the per-agent/category table differs;
3. IDs are duplicated, ordinals are non-contiguous, a dependency is missing,
   or the dependency graph cycles;
4. an operation is outside the allowlist;
5. a payload is missing, stale by SHA-256, a symlink, outside the demo root,
   contains NUL, or exceeds the configured argv limit;
6. file_edit has empty old text, identical old/new text, or an ambiguous match
   without explicit replace_all intent;
7. an expected-red test has no later relevant mutation and green rerun with the
   same test_cycle;
8. a test repeats on an unchanged lane revision unless marked final_regression;
9. a write matches existing payload state or an edit is a no-op;
10. a counted command is sleep-only, true-only, echo-only, package install,
    network download, random, or wall-clock dependent; the anchor ready marker
    is the sole echo-like exception;
11. release can occur with an earlier lane row in flight;
12. blame is requested before the relevant publish;
13. host/runtime identifiers are interpolated into shell text;
14. purpose, scene, expectation, or provenance is absent.

At runtime, the runner compares pre- and post-mutation content digests. A
reported successful mutation that changes nothing fails the scenario.

## 9. Workstream 3 — Test, repair, and fine-tune

### 9.1 Test ladder

Testing proceeds in this order. A later level does not start while an earlier
level has unexplained failures.

1. **Generator unit tests**
   - deterministic byte-for-byte generation;
   - exact budget and category counts;
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
   - run node syntax checks and node --test;
   - verify links/assets and local HTTP behavior;
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
   - execute all 389 authored rows from a fresh sandbox;
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

Every failed authored row writes defect.json with:

- classification;
- expected and actual values;
- redacted argv;
- CLI exit, stdout, stderr, and parsed response;
- sandbox, workspace, command, request, trace, and step IDs;
- surrounding event sequence and observability checkpoints;
- content and manifest hashes before and after;
- suggested smallest reproduction command.

Use exactly these classifications:

- script_or_payload;
- runner_or_artifact;
- cli_projection_or_client;
- runtime_product;
- environment_or_stale_binary;
- transient_host_load.

### 9.3 Repair procedure

When a failure appears:

1. preserve the failed run directory unchanged;
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
- explicit session create/destroy;
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
- set operation timeouts from observed p95 plus safety headroom;
- use barriers for correctness and at_ms only for readable pacing;
- sample aggregate cgroup at 500 ms;
- shorten noisy command output at capture/render time without discarding raw
  artifacts;
- keep the active run between 90 and 120 seconds;
- use real tests and application work rather than sleeps or synthetic CPU load;
- adjust script timing or payload granularity only if assertions and the exact
  389-call budget remain intact;
- show only selected-agent detail so ten-lane telemetry stays legible.

The accepted timing profile is the median and p95 from the three clean
qualification runs. Timeout values are committed with a short rationale in
scenario.json.

## 10. Workstream 4 — Produce the demo HTML

### 10.1 Delivery modes

The same light-theme control room supports three explicit modes:

| Mode | Entry | Behavior |
| --- | --- | --- |
| Sample | index.html or ?mode=sample | Embedded simulated fixture; always labeled |
| Live | ?mode=live | Polls the runner projection; never falls back to sample |
| Recorded | generated/RUN_ID/demo.html | Embedded projection from a successful real run |

The document shell renders before data loading. Live fetch failure shows a
visible retry panel and the last valid projection, if any. It MUST never become
blank and MUST never silently replace failed live data with simulated data.

### 10.2 Projection contract

run.json is a versioned, bounded UI projection:

~~~json
{
  "schema_version": "multiagent-demo/v1",
  "projection_seq": 327,
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
      "completed": 327,
      "planned": 389,
      "failed": 0,
      "engine": 286,
      "diagnostic": 0
    },
    "shared_revision": 12
  },
  "presentation": {
    "active_scene": "conflict",
    "reached_scenes": ["fanout", "merge", "conflict"]
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
- relative links to complete raw artifacts.

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

### 10.4 Scene gates

The page contains five audience scenes, each unlocked only by evidence:

1. **Fan-out** — snapshot proves ten active primary workspaces.
2. **Merge and blame** — the registry has ten values and ten mapped owners.
3. **Conflict and discard** — exact rejection class, unchanged revision,
   absent loser files, retained winner content and blame.
4. **Port isolation** — real shared collision plus two successful isolated
   forwarding probes.
5. **Evidence and storefront** — final test suite, preview, artifacts, and
   cleanup all pass.

Automatic playback follows reached scenes. Previous/next can navigate only
scenes already reached. Pausing playback does not affect the run.

### 10.5 UI composition

Preserve the existing warm light theme and compact layout:

- run header with mode, scene, elapsed time, and presenter controls;
- six proof metrics including completed / 389;
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
/multiagent/run.json         current atomic projection
/multiagent/artifacts/...    allowlisted files beneath the active run
/multiagent/preview/...      retained/forwarded preview target
~~~

The file server rejects path traversal and symlink escapes and sends no-store
headers for live projections.

The export command reads a terminal successful manifest, verifies every
artifact digest, embeds the bounded projection and retained preview into a copy
of index.html, changes all provenance labels to recorded-real equivalents, and
writes generated/RUN_ID/demo.html atomically. Failed or unclean runs cannot be
exported as a successful demo.

### 10.7 Browser safety, accessibility, and responsiveness

The HTML MUST:

- use textContent for artifact and narrative strings;
- never inject raw command output with innerHTML;
- accept artifact URLs only when relative or expected loopback preview URLs;
- sandbox the live preview iframe;
- contain no external scripts, fonts, images, analytics, CDN, or build step;
- render a usable shell and explicit error for malformed data;
- keep the last valid projection if a later poll is malformed;
- redact likely credentials before projection and render;
- provide skip navigation, semantic landmarks, visible focus, keyboard tabs,
  throttled aria-live status, and non-color status text;
- provide a table alternative to charts;
- honor prefers-reduced-motion;
- avoid body-level horizontal overflow at 375, 768, 1024, and 1440 px widths.

### 10.8 HTML tests

Use the repository’s existing Playwright installation rather than adding a
browser dependency. Tests cover:

- sample, live, recorded, loading, malformed, disconnected, failed, and passed
  modes;
- live failure never falling back to sample;
- ten agents, five gated scenes, and exact call counts;
- process success plus publication rejection rendered simultaneously;
- hostile event text rendered as text, never markup;
- missing preview and degraded telemetry fallbacks;
- keyboard navigation, refresh, reduced motion, and responsive widths;
- no console error or unhandled promise rejection;
- screenshot baselines for conflict, network, and final evidence on desktop and
  mobile;
- no serious or critical automated accessibility findings;
- every displayed evidence link returning 200 with the manifest SHA-256;
- a real successful run showing 389 / 389, ten owners, one atomic rejection,
  two isolated servers, final green tests, and clean cleanup.

## 11. Command-line interface

The implementation exposes these operator commands:

~~~sh
cd /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/demo/multi-agent

python3 generate_scripts.py --write
python3 generate_scripts.py --check

python3 run_demo.py validate
python3 run_demo.py truth-spike
python3 run_demo.py run --serve --host 127.0.0.1 --port 8765
python3 run_demo.py replay runs/RUN_ID --serve --host 127.0.0.1 --port 8765
python3 run_demo.py export-html runs/RUN_ID \
  --output /Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/multiagent/generated/RUN_ID/demo.html
~~~

run prints the run ID, demo URL, artifact directory, authored/engine call
counts, and terminal cleanup verdict. “--keep-on-failure” MAY preserve a failed
sandbox for interactive diagnosis in development, but is disabled for
qualification and presentation runs.

## 12. Implementation sequence and gates

### Phase 0 — Contract foundation

Implement and test the request-ID override, verify current public CLI output,
and complete the one-workspace truth spike.

**Gate:** exact request-to-trace join, publish fields, blame, observability, and
cleanup all work against a fresh sandbox.

### Phase 1 — Deterministic generator

Create storefront payloads, recipes, validator, plans, and budget.

**Gate:** generation is byte-stable; offline storefront tests pass; the
validator reports exactly ten lanes and 389 meaningful calls.

### Phase 2 — Runner and proof scenes

Implement scheduler, anchors, correlation, artifacts, observer, conflict,
network isolation, replay, and cleanup.

**Gate:** terminal-only truth spikes pass, including ten simultaneous
workspaces, atomic rejection, retry, isolation, and no leaked resources.

### Phase 3 — Full script execution and repair

Run individual lanes, paired lanes, ten-lane spike, then the full workload.
Apply the defect procedure for any script, CLI, or runtime bug.

**Gate:** one clean 389-call run produces the expected storefront and complete
evidence manifest.

### Phase 4 — Artifact-driven HTML

Wire index.html to the projection, add explicit modes and error states, implement
recorded export, and complete browser tests.

**Gate:** live, recorded, and sample modes pass functional, accessibility,
responsive, safety, and screenshot checks without blank states.

### Phase 5 — Presentation qualification

Tune using measured p95 timings and rehearse failure/recovery.

**Gate:** three consecutive clean end-to-end runs on the presentation machine,
plus a verified self-contained recorded demo.

## 13. Definition of done

The implementation is complete only when all statements below are true:

- generation is deterministic and checked-in output exactly matches recipes;
- exactly 389 authored public CLI calls run across A01–A10;
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
  performance checks pass;
- SIGINT and normal completion leave no sandbox, workspace, command, or preview
  leak;
- live HTML never silently substitutes sample data or renders blank;
- sample data, staged dialogue, trusted lifecycle, runner joins, and real
  evidence are visibly distinct;
- recorded demo export verifies its source manifest and opens without a runner;
- three consecutive presentation-machine runs pass with no semantic retry.

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

