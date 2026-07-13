# Ephemeral Sandbox Multi-Agent Demo — Design

| Field | Value |
| --- | --- |
| Status | Proposed |
| Working title | **FlashCart: ten agents, one workspace** |
| Visual prototype | [Open the interactive light-theme control room](./index.html) |
| Implementation spec | [Build plan, contracts, tests, and acceptance gates](./IMPLEMENTATION_SPEC.md) |
| Implementation prompt | [Copy-ready full implementation and verification prompt](./IMPLEMENTATION_PROMPT.md) |
| Primary goal | Prove concurrent workspace isolation, merge-back, conflict handling, auditability, network isolation, and observability with real sandbox operations |
| Presentation rule | Agent personas and dialogue may be staged; CLI results, file changes, conflicts, blame, previews, and telemetry must be real |

## 1. Executive recommendation

Build a polished, test-backed, dependency-free e-commerce storefront from an
almost-empty workspace using ten deterministic agent lanes. Author each lane as
a granular transcript of real `sandbox-*cli` calls rather than one monolithic
shell payload. A qualified run contains **350–500** meaningful agent-attributed
CLI calls, excluding observability polling and trusted explicit-session
lifecycle control. Prefer 450–500 when every call remains useful; the
illustrative recommendation below is 477, not a fixed gate.

Hold one automatic `publish_then_destroy` workspace open for each active agent
with a gated anchor command. While that command is running, the lane performs
its reads, small writes/edits, builds, targeted tests, diagnostics, and fixes as
separate CLI calls against the returned workspace session ID. Releasing the
anchor after the lane is green triggers the real capture, three-way merge,
publish, blame attribution, and destroy lifecycle.

The demo should have one polished Control Room page, but it should keep three
data classes visibly separate:

1. **Evidence** — real CLI responses, files, blame, traces, events, cgroup
   samples, layerstack state, and forwarded previews.
2. **Narrative** — staged agent messages such as “I found a pricing conflict.”
3. **Presentation** — scene changes, camera focus, pauses, and explanatory
   annotations.

This separation makes the presentation entertaining without implying that the
product currently provides agent-to-agent messaging or native agent identity.

Use a pre-pulled Node image and only Node standard-library APIs. The storefront
uses plain HTML, CSS, and JavaScript, and the preview server uses `node:http`.
There is no package installation, external network dependency, or framework
build that can derail a live presentation.

## 2. What the repository supports today

| Claim | Current behavior | Demo treatment |
| --- | --- | --- |
| Independent execution workspace | `exec_command` without a workspace ID creates a fresh Shared-network workspace session | Real, through `sandbox-runtime-cli` |
| Merge results into shared state | Implicit session completion captures, resolves, publishes, then destroys | Real, through `sandbox-runtime-cli` |
| Concurrent non-overlapping edits | Text writes use publish-time three-way merge | Ten agents edit separate lines of one registry and all survive |
| Conflict detection | Overlapping edits reject with `publish_rejected: true` and class `source_conflict` | Two agents change the same pricing line from the same base |
| Rollback | A rejected capture publishes nothing; its implicit session is destroyed | Call this **atomic reject and discard**, not general undo |
| File blame | Published lines have opaque owners such as `workspace_session:<id>` | Map raw owners to demo agents in the runner; preserve raw IDs in detail |
| Same-port isolation | Explicit `isolated` sessions have separate network namespaces | Two variant servers both bind port 4173 and are forwarded independently |
| Ten parallel workers | Runtime defaults are well above ten active sessions/commands | Start ten gated commands before releasing any of them |
| Resource and lifecycle telemetry | Snapshot, cgroup, trace, events, and layerstack are public observability operations | Record and render real responses throughout the run |

### 2.1 Important product boundary

`create_workspace_session` and `destroy_workspace_session` are deliberately
internal operations. The public runtime CLI rejects them. Existing live E2E
tests reach only those two operations through the authenticated, allowlisted
`direct_daemon.py` adapter, then use the normal runtime CLI for commands and
file operations.

The demo should keep this boundary:

- use actual `sandbox-*cli` binaries for sandbox creation, commands, file
  reads, blame, and all observability queries;
- reuse the existing trusted direct-daemon adapter only for explicit session
  create/destroy;
- label those calls **Trusted session control**, not public CLI;
- use explicit sessions only for disposable experiments;
- never imply that destroying an explicit session merges its changes.

Do not expose the internal lifecycle operations publicly merely to simplify a
demo. If “every visible line must be a `sandbox-*cli` command” becomes a hard
marketing requirement, that is a separate product/API decision.

### 2.2 Precise rollback claim

There is no public arbitrary “undo a committed layer” operation. The demo can
honestly prove two rollback-like guarantees:

- **Atomic publish rejection:** a conflicting multi-file changeset publishes
  none of its files.
- **Experiment discard:** destroying an explicit `no_op` session removes its
  unpublished upperdir.

The UI may title the scene “Conflict rollback,” but the evidence label should
say “Rejected and discarded; shared head unchanged.”

## 3. Storefront decomposition

The run starts with an empty host workspace. A real bootstrap `exec_command`
creates only a ten-slot feature registry and minimal project metadata. The ten
agents create the application code from there.

The registry is the visual proof of multi-agent merging:

```js
export const features = {
  a01: null,
  a02: null,
  a03: null,
  a04: null,
  a05: null,
  a06: null,
  a07: null,
  a08: null,
  a09: null,
  a10: null,
};
```

Every agent creates files on disjoint paths and replaces exactly its assigned
registry line. All ten commands begin before any is released, so all ten
sessions share the same base. Publish order may vary, but line-disjoint
three-way merges should preserve all ten entries and give those lines ten
distinct blame owners.

| Agent | Role | Primary files | Shared-registry edit |
| --- | --- | --- | --- |
| A01 | Foundation | `index.html`, `src/app.js`, `scripts/serve.mjs` | `a01` |
| A02 | Theme | `styles/tokens.css`, `styles/layout.css` | `a02` |
| A03 | Product data | `src/data/products.js` | `a03` |
| A04 | Product grid | `src/features/catalog.js`, card styles | `a04` |
| A05 | Search and filters | `src/features/search.js` | `a05` |
| A06 | Cart and pricing | `src/features/cart.js`, `src/config/commerce.js` | `a06` |
| A07 | Wishlist | `src/features/wishlist.js` | `a07` |
| A08 | Checkout | `src/features/checkout.js` | `a08` |
| A09 | Accessibility | `src/features/accessibility.js`, accessibility CSS | `a09` |
| A10 | QA and diagnostics | `tests/storefront.test.mjs`, `src/features/status.js` | `a10` |

The final storefront should feel like a real product, not a feature collage. It
includes an application shell and router, responsive design system, typed
product fixtures and inventory rules, catalog/PDP/variant views, search and URL
facets, wishlist and recommendations, integer-money cart pricing, promotions,
tax and shipping, validated multi-step checkout, order receipt, keyboard and
screen-reader behavior, reduced motion, performance budgets, and full
integration regression coverage. The toolchain remains preloaded and offline;
“from scratch” refers to the application source, not downloading dependencies
during the presentation.

### 3.1 Recommended agent CLI-call allocation

Each recommended number below represents real CLI invocations with parsed
responses. Timeline animations, staged dialogue, barriers, sleeps, and
telemetry queries do not count.

| Agent | Workspace control | Inspect | Patch | Build/lint | Test/debug | Conflict/network/audit | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 Foundation | 2 | 8 | 14 | 6 | 11 | 2 | **43** |
| A02 Design system | 2 | 8 | 15 | 6 | 11 | 2 | **44** |
| A03 Product data | 2 | 9 | 14 | 6 | 12 | 2 | **45** |
| A04 Catalog and PDP | 2 | 9 | 15 | 6 | 10 | 8 | **50** |
| A05 Search and facets | 2 | 9 | 14 | 6 | 11 | 4 | **46** |
| A06 Cart and pricing | 2 | 9 | 15 | 6 | 11 | 7 | **50** |
| A07 Wishlist and recommendations | 2 | 8 | 13 | 5 | 11 | 3 | **42** |
| A08 Checkout | 2 | 10 | 16 | 6 | 12 | 8 | **54** |
| A09 Accessibility and performance | 2 | 9 | 14 | 5 | 12 | 12 | **54** |
| A10 Integration QA | 2 | 10 | 11 | 7 | 15 | 4 | **49** |
| **Recommended total** | **20** | **89** | **141** | **59** | **116** | **52** | **477** |

The two workspace-control calls per agent are the anchor `exec_command` and its
final `write_command_stdin`. The last column includes only actual public CLI
work such as port-server commands and probes, conflict attempts and retries,
command-log reads, blame queries, and final audit checks. Trusted explicit
session create/destroy calls used by the network scene are recorded separately.

Treat every row and category number as a recommendation only. Script repair and
tuning may move calls freely between agents and categories. Enforce the 350–500
total band, prefer 450–500, and enforce required proof cycles plus no-padding
rules instead of per-agent quotas. Record the generated totals in
call-budget.json and use them everywhere in the runner and UI. At 90–120
seconds, per-request trace lookups, 500 ms cgroup samples, and the remaining
lifecycle, event, snapshot, layer, and blame queries produce roughly 750–1,000
engine/lifecycle/observability interactions. A preferred run therefore produces
roughly 1,200–1,500 real interactions overall. These are capacity expectations,
not quotas.

## 4. Presentation story

Target a five-to-seven-minute guided presentation and a 90–120-second automatic
execution. Presenter controls can pause between scenes while the underlying
logical clock remains deterministic.

### Scene 0 — Reset and preflight

1. Create a unique run directory and empty workspace.
2. Create one sandbox with `sandbox-manager-cli create_sandbox`.
3. Verify runtime, blame, observability, trusted lifecycle control, port
   forwarding, and the configured autosquash threshold.
4. Run the bootstrap command and record the initial layerstack revision.

Audience message: **one empty project, one shared sandbox**.

### Scene 1 — Ten agents fan out

Start ten anchor commands with the existing stdin-gate pattern:

```text
sandbox-runtime-cli --sandbox-id <id> exec_command \
  --yield-time-ms 0 --timeout-ms 600000 \
  "printf 'READY\\n'; read publish"
```

Each response supplies a real `command_session_id` and
`workspace_session_id`. Do not release any command until all ten report
`status: running`. The engine then runs each agent's ordered JSONL lane;
workspace-scopable rows carry that workspace ID, command-control rows carry the
command ID, and post-publish checks are sessionless. Every file read, file
write/edit, search, build, unit test, failure diagnosis, patch, and rerun is a
separate real CLI process. One lane is sequential; up to ten lanes execute
concurrently.

The Control Room should now show:

- ten active agent lanes;
- ten active workspace sessions from the real snapshot;
- each workspace’s Shared network profile;
- live CPU, memory, I/O, and upperdir activity;
- the exact CLI command and elapsed time for the selected lane.

Audience message: **ten independent filesystem views exist at once**.

### Scene 2 — Merge and blame

After every lane has passed its targeted checks, release the ten anchors with
`write_command_stdin`, either together or with a small visual stagger. Every
implicit session then captures, resolves, publishes, and destroys.

Verify with real operations:

- all ten terminal responses have no publish rejection;
- all ten registry entries are present;
- blame on the registry contains ten distinct `workspace_session:` owners;
- the runner maps those raw IDs back to A01–A10;
- layerstack manifest revision advances once per non-no-op publish;
- the storefront smoke test passes.

The file viewer should color the ten registry lines by agent. Selecting a line
shows agent name, task, raw owner, command ID, workspace ID, request/trace ID
when available, start/end time, and the original CLI response.

Audience message: **independent work merged into one auditable result**.

### Scene 3 — Conflict, atomic discard, and retry

Start A06 and A08 from the same newly published base. Both wait on stdin.

- A06 changes `freeShippingCents` from `5000` to `6000`.
- A08 changes the same line from `5000` to `7500` and also creates
  `src/features/express-checkout.js`.

Release A06 and wait for its publish to complete. Then release A08. A08’s
process can still exit zero while its publish is rejected, so render two
separate facts:

```text
Process       exit 0
Publication   rejected · source_conflict
```

Prove atomic discard with four real checks:

1. `freeShippingCents` remains `6000`.
2. `express-checkout.js` is absent.
3. manifest/layer state did not advance for A08’s rejected publish.
4. blame on the contested line still resolves to A06.

The staged dialogue may say that A08 rebases onto A06’s decision. Label it
**Narrative simulation**. Then run A08 again in a fresh implicit workspace; its
retry preserves `6000`, creates the checkout integration, validates, and
publishes successfully.

The runtime terminal response provides the real rejection class, but not a
structured conflict path/fingerprint. The UI may say “scripted conflict target:
`src/config/commerce.js`”; it must not claim that the terminal API returned that
path. The raw finalize failure event may be shown separately.

Audience message: **the loser cannot partially corrupt shared state, and retry
starts from the new head**.

### Scene 4 — Shared-port collision, then isolated success

Use A04 and A09 as two preview experiments.

1. Create two explicit Shared-network sessions through trusted session control.
2. Start the first Node preview server on `0.0.0.0:4173`; it succeeds.
3. Start the second on the same address and port; it fails with address in use.
4. Stop commands and destroy both sessions.
5. Create two explicit `isolated` sessions.
6. Apply different in-session banner edits, one “dense catalog” and one
   “accessible catalog.”
7. Start both servers on `0.0.0.0:4173`; both succeed.
8. Show the two real forwarded previews side by side:
   `/s/<sandbox>/isolated=<workspace>/4173/`.
9. Stop and destroy both sessions, then prove the shared storefront and blame
   are unchanged.

Audience message: **network isolation turns a port collision into two safe,
disposable experiments**.

### Scene 5 — Final evidence

End on the real storefront preview, then zoom through four evidence views:

1. ten-agent blame on the shared registry;
2. the A08 conflict/finalize trace waterfall;
3. cgroup history around the ten-agent fan-out;
4. layerstack and event history, including publish failure and lease release.

Audience message: **the result, authorship, failure, cleanup, and cost are all
inspectable**.

## 5. Deterministic execution engine

### 5.1 Proposed files

Keep deterministic demo machinery with the E2E/benchmark repository and reuse
the existing session-control adapter:

```text
ephemeral-sandbox-test/demo/multi-agent/
├── README.md
├── run_demo.py
├── scenario.json                 # phases and cross-lane barriers
├── recipes.py
├── generate_scripts.py
├── update_oracle.py
├── call-budget.json              # generated actual advisory matrix
├── expected-final.json           # reviewed pre-run path/hash oracle
├── test-inventory.json           # exact test names and counts
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
│   └── ... A10/                  # file bodies and edit specs
└── runs/<run-id>/
    ├── manifest.json
    ├── run.json
    ├── events.ndjson
    ├── commands/
    ├── observability/
    └── blame/
```

Each JSONL record describes exactly one sandbox operation. Large HTML, CSS,
JavaScript, expected output, and structured edit lists live in payload files so
the plans stay reviewable and the runner never interpolates shell source.

```json
{"id":"A06.025","phase":"pricing","op":"file_write","args":{"path":"tests/cart-shipping.test.mjs","content_from":"payloads/A06/025.mjs"}}
{"id":"A06.026","phase":"pricing","op":"exec_command","args":{"command":"node --test tests/cart-shipping.test.mjs"},"expect":{"exit_code":1,"classification":"expected_red"}}
{"id":"A06.027","phase":"pricing","op":"file_edit","args":{"path":"src/features/cart.js","edits_from":"payloads/A06/027.json"}}
{"id":"A06.028","phase":"pricing","op":"exec_command","args":{"command":"node --test tests/cart-shipping.test.mjs"},"expect":{"exit_code":0}}
```

The runner injects the lane's live workspace session ID and invokes the actual
CLI for every row. The complexity belongs in these ten evidence-rich plans;
the engine itself remains a small `asyncio` scheduler.

### 5.2 Schedule format

Use JSON/JSONL so the Python standard library is sufficient. Ordering inside a
lane is implicit. A row may declare an earliest presentation time and explicit
cross-lane evidence dependencies:

```json
{
  "id": "a08-conflict-release",
  "at_ms": 24000,
  "after": ["a06-pricing-published"],
  "agent": "A08",
  "op": "write_command_stdin",
  "expect": {
    "process_exit": 0,
    "publish_reject_class": "source_conflict"
  }
}
```

Pure timestamp ordering is too fragile for merge and port demonstrations.
`at_ms` should mean “not before,” while `after` and runtime assertions determine
when a correctness-sensitive step may start. The engine uses a monotonic clock,
`asyncio`, and subprocess argument arrays.

Before execution, validate that there are exactly ten lanes and 350–500 counted
calls, warning below the preferred 450; every step ID is unique; dependency
edges are acyclic; referenced payloads exist; expected-red tests fail the exact
inventoried subtests for the expected reasons and have a later relevant mutation
and exact-inventory green rerun; and no write or edit is a no-op. Repeated tests
on an unchanged workspace revision are rejected unless explicitly classified as
conflict retry or A10 final regression coverage.

### 5.3 Runner responsibilities

The runner should do only the following:

- create and clean up the sandbox and all explicit sessions;
- schedule CLI subprocesses and stdin releases;
- capture argv, stdout, stderr, exit status, CLI elapsed time, and parsed JSON;
- retain the runtime’s `wall_time_seconds` and `command_total_time_seconds`;
- maintain agent, request, command-session, and workspace-session correlation;
- run real assertions before advancing dependent scenes;
- sample aggregate cgroup data every 500 ms during active scenes and selected
  workspace cgroups while those workspaces exist;
- checkpoint snapshot, events, trace, layerstack, file contents, and blame;
- append normalized events to `events.ndjson` and publish a current `run.json`;
- stop live commands and destroy explicit sessions on success, failure, or
  interrupt.

Do not build a general workflow engine, message bus, or agent protocol. A small
scenario scheduler and correlation ledger are enough.

### 5.4 Agent correlation

Each terminal command response exposes its workspace session ID, and published
blame uses that same ID. Store every mapping, including retries:

```text
workspace_session:<id>
  -> agent A08
  -> step a08-pricing-retry
  -> command_session_id
  -> request/trace id, if available
  -> start/end and raw result
```

`file_blame` itself has no agent name, timestamp, command, or history. The
agent-scoped rendering is a run-local presentation join, not a changed blame
contract. `original` and `unknown` remain unchanged and visible.

### 5.5 Trace correlation gap

The daemon trace ID is the operation request ID. The operation client supports
an explicit request ID, but the CLI currently generates a UUID internally and
does not print it. That prevents deterministic per-agent trace links during the
ten-command concurrent wave.

Strongly recommended small product change: add a global CLI request-ID override,
preferably `--request-id` with an environment-variable equivalent for scripts.
The runner can then use IDs such as `demo-<run>-A08-conflict` and link directly
to the trace. Without that patch, the MVP can still show aggregate telemetry
and use `trace --trace-id last` for sequential scenes, but should not guess the
trace-to-agent mapping.

### 5.6 Event model

Normalize runner events without replacing raw evidence:

```json
{
  "seq": 42,
  "at_ms": 8231,
  "kind": "command.terminal",
  "agent": "A08",
  "step": "a08-pricing-conflict",
  "workspace_session_id": "...",
  "evidence_path": "commands/a08-pricing-conflict.json"
}
```

Narrative events live in the same ordered stream with
`"kind": "narrative.message"` and `"simulated": true`. Raw CLI and telemetry
JSON remain in separate artifacts so the UI never needs to manufacture product
evidence.

## 6. Control Room presentation UI

Use the standalone light-theme `ephemeral-sandbox-docs/multiagent/index.html`
control room specified for this demo. Reuse the current observability data
shapes and visual language for resources, traces, events, layers, terminal
cards, preview, and blame, without adding a React build or another dashboard
service.

Suggested route:

```text
/multiagent/?mode=live&run=RUN_ID
```

Suggested desktop composition:

```text
┌──────────────────────────────────────────────────────────────────────┐
│ FlashCart Build · LIVE · Scene 2/5       Pause   Next   Reset        │
├────────────────────────────────────────────┬─────────────────────────┤
│ A01 Foundation   running  1.2s  ████████  │ Real storefront preview │
│ A02 Theme        publish  1.6s  ████████  │                         │
│ ... ten compact lanes ...                  │                         │
│ A10 QA           running  1.4s  ████████  │                         │
├────────────────────────────────────────────┼─────────────────────────┤
│ Evidence: CPU · memory · I/O · workspaces  │ Narrative simulation   │
├────────────────────────────────────────────┴─────────────────────────┤
│ CLI | Trace | Events | Layers | Blame      selected-agent detail    │
└──────────────────────────────────────────────────────────────────────┘
```

Design rules:

- preserve the console’s existing warm/light visual system;
- use one high-emphasis selected agent and compact rows for the other nine;
- label every card `Real CLI`, `Real telemetry`, or `Narrative simulation`;
- show process status and publish status separately;
- never render ten full charts at once—use lane sparklines/numbers and one
  selected workspace detail;
- show raw IDs and raw JSON behind disclosure, not in the primary story;
- provide pause, next-scene, reset, and keyboard controls;
- respect reduced motion and use an `aria-live` region for state changes;
- provide a data-table alternative for resource charts;
- keep the run alive across browser refresh by treating the runner artifacts as
  source of truth.

The smallest live transport is a local read-only HTTP/SSE endpoint owned by the
runner, or an equally small console proxy to the run artifacts. Do not add a
WebSocket system or new client state library. If SSE is inconvenient for the
first spike, polling `run.json` at 250–500 ms is sufficient.

## 7. Observability proof plan

| View | Real source | What the audience should learn |
| --- | --- | --- |
| Agent lanes | CLI lifecycle plus `snapshot` | Ten commands/workspaces are concurrently active |
| Resource chart | `cgroup` | CPU, memory, I/O, and workspace disk activity have measurable cost |
| Command time | `exec_command` response plus runner clock | Child runtime and end-to-end CLI time are distinct |
| Trace waterfall | `trace` | create → shell → capture → publish → destroy is one inspectable lifecycle |
| Event rail | `events` | leases, failed publication, cleanup, and autosquash events are auditable |
| Layers | `layerstack` | successful publishes advance shared state; rejection does not |
| File ownership | `file_blame` | final lines join back to the sessions that published them |

Repeated resource queries are important: aggregate cgroup sampling runs every
500 ms, while workspace-specific resource snapshots occur after selected
operations and queries. Capture samples during the live workspace lifetime; do
not expect destroyed workspaces to remain queryable.

## 8. Preflight and acceptance criteria

### 8.1 Preflight

- required CLI binaries resolve, and `help <required-operation>` succeeds for
  every operation used by the scenario;
- configured Node image exists locally; no image pull occurs during the talk;
- the trusted lifecycle adapter can create/destroy one isolated canary session;
- the runner’s constrained loopback proxy can forward one isolated port through
  the existing daemon_http route contract;
- snapshot, cgroup, trace, events, layerstack, and blame operations respond;
- project paths used for conflict proof are not ignored;
- autosquash is disabled or its threshold exceeds the maximum projected
  publication count; otherwise qualification is blocked;
- run workspace is unique and contains no user files;
- a throwaway two-command canary confirms the current build surfaces
  `publish_rejected` and `source_conflict` on the terminal response;
- cleanup is verified after an interrupted canary run.

### 8.2 Live acceptance criteria

1. Snapshot observes ten simultaneous active workspaces/commands.
2. Ten initial agent commands publish successfully from one common base.
3. The final registry contains all ten entries and blame maps them to ten agents.
4. A06/A08 produces exactly one accepted contested value and one
   `source_conflict` rejection.
5. The rejected changeset’s unrelated file is absent and shared revision does
   not advance for that rejection.
6. A08’s fresh retry publishes successfully.
7. Two Shared sessions demonstrate a real same-port collision.
8. Two isolated sessions bind the same port and both forwarded previews answer.
9. Destroying those sessions leaves shared files and blame unchanged.
10. Resource, trace, event, layerstack, command-time, and blame evidence is
    retained with the run.
11. Final storefront smoke tests pass and every resource is cleaned up.

## 9. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Timestamp races make the conflict flaky | Use stdin gates and evidence dependencies; timestamps are earliest-start cues only |
| Tiny commands produce weak charts | Give every agent real syntax/unit/accessibility validation lasting long enough to sample; do not add fake metrics |
| CLI request IDs cannot be correlated | Add the small request-ID override; otherwise restrict trace claims to sequential steps |
| Conflict UI overstates available detail | Mark the path as scenario metadata and show the raw terminal class/event separately |
| “Rollback” implies generic undo | Say atomic reject/discard and explicit experiment discard |
| Explicit experiment edits are mistaken for mergeable work | Use a distinct Experiment lane and prove shared state is unchanged after destroy |
| Blame is mistaken for native agent identity/history | Show the raw owner and label the agent mapping as run-local |
| Audit append can produce `unknown` | Render `unknown` honestly and fail preflight/rehearsal if the key blame proof is incomplete |
| Autosquash obscures layer deltas | Keep the run below the configured threshold or assert manifest revisions and content |
| Browser or projector disconnects | Runner persists state; UI reconnects; keep a clearly labeled replay of a previously recorded real run |
| Cleanup fails after interruption | Track every sandbox, explicit workspace, and command ID; cleanup in `finally` and signal handlers |

## 10. Implementation slices

These slices are refined into phases 0–5 in IMPLEMENTATION_SPEC.md. Every phase
has a normative evidence-backed checkbox list: all boxes in phase N must be
satisfied before phase N+1 begins, and an invalidated check reopens its phase and
dependent later gates.

### Slice A — Truth spike

- scale the existing five-command line-disjoint E2E pattern to ten;
- add one deterministic overlap/reject assertion;
- prove Shared collision and isolated same-port forwarding;
- capture blame and all five observability operations;
- decide whether the CLI request-ID override is included.

Exit condition: a terminal-only run produces every required fact and cleans up.

### Slice B — Scripts and runner

- implement the ten storefront scripts and scenario;
- add correlation, assertions, artifacts, sampling, interrupt cleanup, and replay;
- keep all scenario data deterministic and offline.

Exit condition: one command starts a reproducible 90–120-second run with a
passing evidence manifest.

### Slice C — Control Room

- add the single demo route;
- reuse existing preview, resources, traces, events, layers, terminal, and blame
  components;
- add only the ten-lane timeline, scene controls, evidence/narrative labels, and
  agent-owner join.

Exit condition: the whole story is understandable without reading terminal
JSON, while raw evidence remains one click away.

### Slice D — Rehearsal hardening

- run repeated live rehearsals on the presentation machine;
- verify p95 timings and increase scene slack rather than inserting blind sleeps;
- test refresh, pause, interrupt, restart, cleanup, and projector resolution;
- record one successful real run as a clearly labeled emergency replay.

## 11. Repository anchors

The design above is grounded in these existing implementations and tests:

- public runtime CLI projection:
  `ephemeral-sandbox/crates/sandbox-cli/src/projection/runtime.rs`;
- implicit workspace lifecycle:
  `ephemeral-sandbox/crates/sandbox-runtime/operation/src/command/service/exec_command.rs`;
- capture/publish/destroy and publish-failure event:
  `ephemeral-sandbox/crates/sandbox-runtime/operation/src/workspace_session/service/impls/finalize_session.rs`;
- all-or-reject publish resolution and text merge:
  `ephemeral-sandbox/crates/sandbox-runtime/layerstack/src/stack/publish/resolve.rs`;
- command response rejection fields:
  `ephemeral-sandbox/crates/sandbox-runtime/operation/src/operations/registry/command_operations.rs`;
- file operation/blame semantics:
  `architecture/01-workspace-runtime/06-file-operations-and-blame.md`;
- capture and merge semantics:
  `architecture/01-workspace-runtime/07-capture-and-publish.md`;
- existing concurrent line-disjoint merge proof:
  `ephemeral-sandbox-test/e2e/runtime/file/concurrent/test_concurrent_session.py`;
- existing gated-command pattern:
  `ephemeral-sandbox-test/e2e/runtime/command/test_git_policy_easy.py`;
- same-port isolated-session proof:
  `ephemeral-sandbox-test/e2e/runtime/network_isolation/test_network_isolation.py`;
- trusted lifecycle adapter:
  `ephemeral-sandbox-test/e2e/harness/runner/direct_daemon.py`;
- public observability CLI projection:
  `ephemeral-sandbox/crates/sandbox-cli/src/projection/observability.rs`;
- existing console observability and blame UI:
  `ephemeral-sandbox/web/console/src/pages/sandbox/observability/` and
  `ephemeral-sandbox/web/console/src/pages/sandbox/files/blame.ts`.
