# EphemeralOS E2E Control Room — UI Design

| Field | Value |
| --- | --- |
| Status | Rewritten; interaction implementation not started |
| System contract | [e2e-test-system-spec.md](e2e-test-system-spec.md) |
| Technical contract | [e2e-test-design.md](e2e-test-design.md) |
| Visual target | [e2e-test-ui-layout-theme.md](e2e-test-ui-layout-theme.md) |
| Migration specification | [e2e-test-ui-migration-spec.md](e2e-test-ui-migration-spec.md) |
| Prototype migration | Move `<PRODUCT_ROOT>/e2e/ui-prototype` to `<E2E_SOURCE_ROOT>/web/prototype`; visual reference only, never production UI |

The Control Room is a catalog and run-comprehension tool. It is not a generic
pytest console, infrastructure dashboard, or domain portal. The interface must
help an engineer answer four questions quickly:

1. What behavior does this case intend to prove?
2. What exactly will run and through which product boundary?
3. What is happening now, including cleanup?
4. Why did it finish this way, and what evidence is still trustworthy?

## 1. UX verdict and cuts

The migrated static prototype establishes useful visual direction: warm neutral
surfaces, dense operational rows, status chips, a selection tray, and a
catalog-first hierarchy. It does not prove routing, state, APIs, selection,
keyboard behavior, accessibility, or responsive execution.

The previous UI draft mirrored too much backend vocabulary. This rewrite removes:

- recovery-session management controls and compatibility overlays;
- separate feature and case resources;
- domain pages and fixed taxonomy cards;
- simultaneous chip clusters for direct/effective features, proof, policy,
  lifecycle, and availability in every row;
- virtualized tables before server pagination is shown insufficient;
- speculative charting and high-rate telemetry surfaces;
- UI controls for roots, paths, surfaces, drivers, endpoints, or commands.

The safety and accessibility requirements remain.

## 2. Information architecture

Four top-level destinations exist:

| Route | Job |
| --- | --- |
| `/e2e/catalog` | find, understand, select, and review cases |
| `/e2e/runs` | find current and historical runs |
| `/e2e/runs/:run_id` | understand one live or historical run |
| `/e2e/workspaces` | see template, active attempts, quarantine, capacity, and safe purge eligibility |

Runner health is a persistent drawer opened from the app header, not a fifth
page. It shows catalog freshness, lane, store, product-boundary capabilities,
and root safety. Its “Run harness diagnostics” action opens the ordinary catalog
with `kind=harness&runnable=true`.

Test detail is a catalog route state:

```text
/e2e/catalog?test_id=<id>&case_id=<id>
```

Feature discovery is also catalog state:

```text
/e2e/catalog?feature_id=<id>
```

Domain/family and Harness diagnostic navigation use the same route state:

```text
/e2e/catalog?domain_id=observability&family_id=cgroup
/e2e/catalog?domain_id=runtime&family_id=shell_security
/e2e/catalog?kind=harness&family_id=runner
```

Back, forward, refresh, and copied URLs preserve server-backed filters. Selection
is revision-qualified browser session state and is not encoded into an
unbounded URL.

### 2.1 Prototype route mapping

The static implementation served at `http://127.0.0.1:4173/*` is a visual
reference, not the route contract. Its nine hash sections map as follows:

| Prototype section | Production route/state |
| --- | --- |
| `#catalog` | `/e2e/catalog` |
| `#manager` | `/e2e/catalog?domain_id=manager` |
| `#runtime` | `/e2e/catalog?domain_id=runtime` |
| `#observability` | `/e2e/catalog?domain_id=observability` |
| `#compound` | `/e2e/catalog?domain_id=compound` |
| `#test-detail` | `/e2e/catalog?test_id=<id>&case_id=<id>` |
| `#live-run` | `/e2e/runs/:run_id` |
| `#runs` | `/e2e/runs` |
| `#workspaces` | `/e2e/workspaces` |

The production IA therefore has four route patterns rather than nine bespoke
pages. It adds the Health drawer and a subordinate Harness Diagnostics catalog
entry, while preserving the prototype's useful visual flows. No prototype
section requires a parallel Runtime-internal hierarchy.

## 3. Visual system

### 3.1 Hierarchy

Use four surface levels only:

1. page background;
2. primary working surface;
3. inset detail/evidence surface;
4. popover/dialog surface.

Status uses text and icon in addition to color. Color meanings:

| Meaning | Treatment |
| --- | --- |
| neutral/queued | gray-blue |
| active/checking | blue with restrained motion |
| passed/ready | green |
| warning/degraded/stale | amber |
| failed | red |
| error/incompatible/recovery blocked | magenta-red |
| cancelled/not run/skipped | gray with distinct icon and label |

Domain and family colors are optional metadata hints, never semantic status.
Unknown hints use one neutral fallback.

### 3.2 Typography and density

- 16 px minimum mobile body text; 14 px minimum desktop dense rows;
- tabular numerals for time, counts, sequences, and byte values;
- monospace only for stable IDs, digests, and short evidence excerpts;
- row height at least 44 px and pointer targets at least 44 by 44 CSS pixels;
- labels state their unit: “3 cases”, “7 validations”, “2 failures.”

Do not display raw full digests in primary flow. Show a short prefix with Copy
and a disclosure for full identity.

### 3.3 Component stack

Use React, TypeScript, Mantine, React Router, TanStack Query, and native
EventSource. Server pagination keeps tables bounded, so v1 uses native semantic
tables/lists and CSS layout. Evidence begins with summaries and accessible
tables. No chart, table, virtualization, state-machine, or second client-store
dependency is required.

The app owns one `/api/v1/events` EventSource. A run route supplies `run_id` and
the last applied sequence; other routes receive only unnumbered
`catalog.revision` and `stream.heartbeat` notifications. A catalog revision
invalidates the one catalog query. There is no polling and no parallel stream.

### 3.4 Label grammar

Different facts must not collapse into interchangeable chips:

| Concept | Presentation |
| --- | --- |
| Domain / family / group / scenario | One breadcrumb with plain-language labels |
| Test / expanded case | Title first; parameters second; stable ID in disclosure |
| Feature | Searchable link-style tag; detail says `Direct` or `Inherited` in text |
| Validation | Named row with `Required` or `Optional`, phase, and mapped feature |
| Execution surface | Boundary icon plus explicit label such as `CLI boundary` |
| Compound scenario | `Compound · {complexity}` text plus component-domain map in detail |
| Execution label | Prefix by category: `Risk: privileged`, `Cost: slow`, or `Schedule: exclusive` |
| Status / verdict | High-emphasis status badge with icon and text |
| Evidence health | Separate `Evidence: Complete/Degraded/Unavailable` badge |

Feature tags identify covered capabilities; the Purpose annotation is the test
description; named Validations are the assertion checkpoints. A checkpoint
always exposes its stable name, requiredness, phase, mapped feature, state, and
evidence link when evidence exists. These three concepts never share one chip.

These fields come only from the mandatory
`@e2e_test(id, title, description, features, validations)` declaration and its
`validation(...)` reports. The UI never infers a feature from a pytest mark or
an assertion from a test name. An undecorated test is a catalog-health error,
not a case card with guessed tags or checkpoints.

Rows show at most one status, one boundary, and one exceptional execution label.
The rest belongs in detail or Review. Color never carries a category alone, and
tooltips only supplement visible text.

## 4. Catalog journey

Catalog navigation has four primary domain cards generated from the combined
catalog: Manager, Runtime, Observability, and Compound. A separate Harness
Diagnostics card is visually subordinate because it tests the E2E control
system rather than a product domain. Selecting a card reveals families, then
cases.

Runtime initially reveals `Command`, `File`, `Daemon HTTP`, `Network
Isolation`, `Reserved Paths`, `Shell Security`, and `Workspace Session`, with
exact IDs `command`, `file`, `daemon_http`, `network_isolation`,
`reserved_paths`, `shell_security`, and `workspace_session`.
Observability initially reveals `Snapshot`, `Trace`, `Events`, `Cgroup`, and
`Layerstack`, with exact IDs `snapshot`, `trace`, `events`, `cgroup`, and
`layerstack`. Harness Diagnostics reveals `Catalog`, `Runner`, `Reducer`,
`Storage`, `API`, and `UI`, with exact IDs `catalog`, `runner`, `reducer`,
`storage`, `api`, and `ui`. The frontend contains no domain/family allowlist and
no Runtime-, Observability-, or Harness-specific page component.

### 4.1 Desktop layout

```text
┌────────────────────────────────────────────────────────────────────┐
│ E2E Control Room    Catalog  Runs  Workspaces   Health ●           │
├───────────────┬────────────────────────────────────────────────────┤
│ Search        │  214 matching cases            3 selected         │
│ Domains       │ Manager · Runtime · Observability · Compound      │
│ Diagnostics   │ Harness Diagnostics                               │
│ Filters       │ ┌────────────────────────────────────────────────┐ │
│ - Feature     │ │ □ Runtime · File read                         │ │
│ - Family      │ │ Purpose: reads through the real runtime CLI   │ │
│ - Owner       │ │ 2 validations · CLI boundary · Ready metadata │ │
│ - Surface     │ └────────────────────────────────────────────────┘ │
│ - Complexity  │                                                    │
│ - Exec label  │ ...                                                │
│ - Kind        │                                                    │
├───────────────┴────────────────────────────────────────────────────┤
│ Selection: 3 cases · 1 query · 1 exclusion          Review run → │
└────────────────────────────────────────────────────────────────────┘
```

The row scan order is:

1. case selection and title;
2. purpose;
3. compact topology path;
4. validation count and boundary claim;
5. metadata/runnable problem only when one exists.

Do not show all inherited/direct features in the row. A single “3 features” link
opens the detail section. Do not show latest result as declaration coverage;
when present, it is a secondary line labeled with run ID, time, and source
revision.

### 4.2 Mobile layout

At 375/390 px the page is one column. Search remains in the page header. Filters
open a full-screen drawer. Rows become cards but preserve semantic heading and
checkbox order. The selection tray is a bottom bar with count and “Review.”
Nothing important is reachable only by hover.

### 4.3 Search and filters

Search placeholder:

> Search behavior, purpose, feature, validation, owner, or ID

Applied filters are removable chips above results. The browser issues one
debounced catalog request and cancels obsolete reads. Empty search is distinct
from invalid/stale catalog.

Aggregate selection labels must be explicit:

- “Select all 18 cases in this group”;
- “Select all 214 matching cases”;
- “18 selected; 2 excluded.”

The checkbox state derives from the selection expression, including off-page
cases.

The page has no folder/test registry. On `catalog.revision`, its normal catalog
refetch renders any newly discovered valid `e2e/**` test or folder using the
same topology, tags, and checkpoint rows. No UI release is required for a new
test family that is represented by catalog data.

## 5. Test detail

The detail surface answers intent before machinery. Sections appear in this
order:

1. **Purpose** — plain-language behavior and stable identity;
2. **Validations** — named checks, requiredness, phase, and mapped features;
3. **Product coverage** — direct and inherited feature provenance for product
   cases only;
4. **Compound context** when present — complexity, subject domains, ordered
   component roles, shared workspace, and teardown contract;
5. **Execution boundary** — immutable expected surface, what it proves, access
   class, and why another surface cannot satisfy it;
6. **Run policy** — execution labels, workspace, timeout, evidence, cleanup,
   and resource claims;
7. **History** — recent frozen results labeled with run and source revision;
8. **Source** — path and pytest selector as contributor diagnostics.

Harness cases omit product coverage. A no-surface case shows:

> Harness diagnostic — no product boundary claimed

It never shows “Surface unavailable.”

Declared validations use “Not run” before execution. They never use a passed
check icon in catalog/detail.

## 6. Review and admission

Clicking Review sends one preview request and opens a full-height dialog on
desktop or a full-screen route-like surface on mobile.


### 6.1 Review content

```text
Review run

Scope
  3 cases · 7 required validations · exact catalog revision a81c…
  [expand ordered case list]

Boundaries
  2 CLI · 1 daemon HTTP

Execution
  Serial lane · Fail-fast off · 3 fresh attempts
  Risk: privileged · Cost: ordinary

Evidence and cleanup
  Bounded logs + structured validation evidence
  Mandatory cleanup; uncertain attempts quarantine

Inputs
  E2E source 42d9… · product build b116… · template 0a3c…

Preflight
  ✓ Store safety   ✓ Product binaries   ✓ Disk reserve
  ✓ CLI boundary  ✓ Daemon endpoint

[Cancel]                                      [Start run]
```

Primary details are human-readable. Exact digests and full checks are in
disclosures. No raw path is editable.

### 6.2 Start rule

Start is enabled only in `ready`. While checking it reads “Checking…” and is
disabled. In every disabled state, adjacent text provides the exact reason; a
tooltip alone is insufficient.

One click issues one admission request. The UI does not retry it automatically.
On success it navigates to the returned run. On `active_run_conflict`, it links
the active run and preserves the review if still valid.

## 7. Live and historical run

The same `RunPage` renders live and history from `RunProjection`. Live behavior
adds stream freshness and Cancel; historical behavior does not use a separate
data model.

### 7.1 Page anatomy

```text
┌────────────────────────────────────────────────────────────────────┐
│ Failed · Run 01J…       1 passed · 1 failed · 3 not run           │
│ Started 14:32:10 · 28.4 s · Stream live at seq 284      [Cancel] │
├────────────────────────────────────────────────────────────────────┤
│ First failure                                                     │
│ Runtime file write · validation “content persisted”               │
│ Assertion failed at 14:32:24                       [Open evidence] │
│ Primary error: teardown cleanup failed              [Open cleanup]│
├────────────────────────────────────────────────────────────────────┤
│ Cases                                                             │
│ ✓ 1  File read                         Passed       4.1 s          │
│ ✕ 2  File write                        Error       17.8 s          │
│   ├ Validation: command accepted        Passed       1.0 s        │
│   ├ Validation: content persisted       Failed       0.4 s        │
│   └ Cleanup: destroy sandbox            Error        5.0 s        │
│ ⊘ 3  File edit                         Not run · fail-fast         │
│ ⊘ 4  File blame                        Not run · fail-fast         │
│ ⊘ 5  File list                         Not run · fail-fast         │
├────────────────────────────────────────────────────────────────────┤
│ Evidence health: Degraded · logs truncated after 5 MiB            │
│ [Retry failed] [Retry not run] [Retry failed + not run]            │
└────────────────────────────────────────────────────────────────────┘
```

### 7.2 Header

Always show:

- status, run ID, parent link when applicable;
- exact counts by case state;
- start/completion/duration with timing quality;
- stream state and applied sequence for nonterminal runs;
- source, catalog, controller, runner, and product identities in a disclosure;
- fail-fast, evidence, workspace, and boundary summary;
- Cancel only when the server projection says it is allowed.

Do not show a nonterminal persisted state as live unless the current controller
overlay proves ownership and the event stream is fresh.

### 7.3 First and primary failure

The first-failure panel appears before cases and logs. It contains causal entity,
failure kind, concise message, time, and evidence link. When primary differs, a
second sentence explains why the terminal severity is higher.

The prototype's count-only mid-flight failure state is insufficient. As soon as
a failed or errored case exists, the live page pins the first-failure panel even
while another case is running or cleanup is active. The operator can see the
case and validation state, phase, boundary-proof state, cleanup state, stream
freshness, bounded logs, evidence health, and the causal link for every not-run
case without waiting for the run to become terminal.

Failure labels are concrete: Assertion, Setup, Fixture, Infrastructure, Timeout,
Teardown, Cancellation, Recorder, Contract, or Controller restart. “Something
went wrong” is prohibited.

The first failure is announced once through a polite live region. Reconnect and
duplicate events cannot reannounce it.

### 7.4 Case rows

Each row shows ordinal, title, state, duration, and boundary proof state. Expand
to see phases, validations, cleanup, failures, and evidence summaries. Not-run
always includes a reason and causal link. Skipped, cancelled, and not-run are
visually and textually distinct.

Cleanup remains visible while active. A case that failed product validation but
is cleaning up is labeled “Failed · cleaning up,” not terminal. Run verdict
remains “Finishing cleanup” until mandatory cleanup is complete.

### 7.5 Evidence

The evidence drawer opens from a validation, surface, failure, cleanup action, or
case. It starts with structured summary, availability, coverage/cap facts, and
correlation. Bounded raw logs are secondary.

Availability messages:

- `available`: “Evidence complete”;
- `partial`: “Evidence partial — {reason}. {retained}/{expected}.”;
- `unsupported`: “Evidence unsupported on this provider.”;
- `unavailable`: “Evidence unavailable — {reason}.”;
- `invalid`: “Evidence rejected — integrity or redaction check failed.”;
- purged overlay: “Evidence was purged on {date}. Verdict and summaries remain.”

Missing values display an em dash plus reason, never zero. Truncated logs show
retained head/tail and omitted lines/bytes. Artifact links use one on-demand
request and never embed active content.

### 7.6 Recovery rendering

`RunProjection.recovery_bundle_match` is exactly `exact_match` or `mismatch`.
No frontend compatibility translation exists.

Exact-bundle recovery uses one message:

> Recovering interrupted run — verifying process ownership and cleaning scoped resources.

Show the current action and completed/total action count. Do not offer Resume.

Bundle mismatch uses:

> Recovery blocked — controller bundle changed.

Supporting text:

> This page shows the last verified state at sequence {N}. No process was signalled and no cleanup was attempted. Restart the admitted controller bundle or follow the manual recovery procedure.

Cancel, Retry, Start, and generic “Try again” mutations are disabled while the
blocker owns the single lane. Refresh is a read-only action.

Recovery history appears in an “Interruption and recovery” disclosure derived
from run events. The UI does not present or manage recovery sessions.

## 8. Runs history

The Runs page has a current-run callout followed by server-paginated history.
Filters are result, date, parent run, domain, feature, surface, evidence health,
and retention state. Result filters do not appear in Catalog.

Each row shows run ID, frozen title/selection summary, result, created/completed
time, duration, counts, source revision, evidence health, and retention state.

If one corrupt run header is excluded, the page shows:

> History is partial — 1 run record could not be read. Open Runner health for details.

A directory scan failure shows:

> Run history is unavailable — the store could not be read safely.

It never renders “No runs” in either case. A known run deep link remains
independent of history listing.

## 9. Workspaces

The Workspaces page is monitoring plus narrow safe action, not a file browser.

Sections:

1. **Capacity** — free bytes, reserved finalization bytes, admission readiness;
2. **Template** — identity, verified time, size, state, Prepare action only when
   no valid template exists;
3. **Active attempts** — run/case, age, state, cleanup progress; no purge;
4. **Quarantine** — reason, ownership, size, verification state, linked run;
5. **Recent purges** — semantic target, time, result, survivor summary.

Only a server-projected inactive owned leaf may show Purge. The confirmation
names the semantic workspace ID and retained lineage. It never displays an
editable path or asks the user to type a filesystem value.

Root identities and full paths live in Runner health, are read-only, and use
wrapping monospace text. The page does not provide settings or pickers.

## 10. Runner health drawer

Health groups facts by operator decision:

- **Can I browse?** catalog ready/stale/unavailable, current revision and
  diagnostics;
- **Can I start?** active lane, disk reserve, template, source/product identity;
- **Which boundaries work?** one row per surface with ready/blocked reason;
- **Is storage safe?** configured/derived roots, ownership markers, separation;
- **What needs attention?** recovery blocker, partial history, quarantine.

The drawer does not contain low-level services merely because they exist. It
does not offer shell commands, arbitrary retry, root mutation, or surface
override. Each action is named and scoped: “Refresh catalog,” “Open active run,”
“Review runnable harness diagnostics,” or “Open manual recovery procedure.”

## 11. Exact async and failure-state matrix

| State | Exact headline | Supporting explanation | Freshness | Safe action | Forbidden claim |
| --- | --- | --- | --- | --- | --- |
| Catalog loading, no data | “Loading test catalog…” | “Reading the current published revision.” | No catalog shown | None | Empty catalog |
| Catalog refreshing | “Updating test catalog — inputs changed.” | “Recollecting now; revision {R} remains the last verified catalog.” | Old rows labeled “Last verified {time}” | Continue browsing | Refreshed or current |
| Catalog filtered empty | “No cases match these filters.” | “Clear a filter or change the search.” | Current revision shown | Clear filters | Catalog empty |
| Catalog known empty group | “This group has no runnable cases.” | “The group exists in revision {R}, but no runnable case is registered.” | Current revision shown | Back to catalog | Loading or failure |
| Catalog invalid with last-good | “Catalog update failed — showing the last good revision.” | “{diagnostic}. Admission is blocked until a valid refresh succeeds.” | Attempt time and last-good revision/time shown | View diagnostics / Refresh catalog | Ready to start |
| Catalog unavailable | “Test catalog is unavailable.” | “No valid published revision exists. {first diagnostic}.” | Failed attempt time shown | View diagnostics / Refresh catalog | Empty catalog or ready |
| Catalog incompatible | “Catalog schema is not supported by this UI.” | “This UI did not interpret the published data.” | Revision shown, contents hidden | Reload after compatible upgrade | Empty, valid, or runnable |
| Preview checking | “Checking {check name}…” | “Start is unavailable while {reason for check} is verified.” | Observation time updates per check | Cancel review | Ready or blocked before result |
| Preview ready | “Ready to start {N} exact cases.” | “Scope is frozen at revision {R} until {expiry}; Start creates one run.” | Preview creation and expiry shown | Start run | Scope will be recomputed |
| Preview blocked | “Run blocked — {blocker label}.” | “{affected scope}. {safe recovery instruction}.” | Blocker observation time shown | Named scoped action / Cancel | Start available |
| Preview stale | “Review is out of date.” | “{catalog/source/preflight fact} changed; the old scope was not submitted.” | Old and current revision/time shown | Review again | Automatically updated scope |
| Preview error | “Readiness check failed.” | “{typed reason}. Request {request ID}; nothing was submitted.” | Failure time shown | Retry only if `retryable=true` | Blocked by product or started |
| Admission pending | “Starting one run…” | “The reviewed {N} cases are being admitted; duplicate Start is disabled.” | Request start time shown | Wait / Cancel request only if supported | A run exists before response |
| Active-run conflict | “Another run owns the execution lane.” | “Run {ID} is {state}; your reviewed scope was not started.” | Conflict response time shown | Open active run / return to review | Queued behind it |
| Admission nonce expired | “This tab is no longer authorized to start runs.” | “Reload before trying again. Nothing was submitted.” | Response time shown | Reload | Started or retrying automatically |
| Run queued | “Run queued.” | “Run {ID} is waiting for its controller-owned serial lane.” | Snapshot sequence/time shown | Cancel if allowed | Actively executing a case |
| Preparing | “Preparing workspace for {case title}…” | “Creating fresh attempt {ID}; product execution has not started.” | Live sequence/time shown | Cancel if allowed | Case or validation running |
| Case running | “Running {case title} — {phase label}.” | “{validation or action}; elapsed {duration}; evidence current as of {time}.” | Live sequence and stream age shown | Cancel | Terminal or complete evidence |
| Failure detected | “Failure detected — finalization continues.” | “First failure: {message}. Teardown, cleanup, and evidence may still change the primary verdict.” | Failure sequence/time shown | Open failure evidence | Final verdict complete |
| Fail-fast applied | “Fail-fast stopped new cases.” | “Failure {ID} caused {N} remaining cases to become Not run; active cleanup continues.” | Causal sequence/time shown | Inspect affected cases | Skipped or cancelled cases |
| Cleaning up | “Cleaning up {resource or attempt}…” | “Mandatory cleanup is still running; the run cannot finish yet.” | Live action and sequence/time shown | Wait / inspect action | Terminal passed/failed |
| Evidence finalizing | “Finalizing evidence…” | “Product work ended; integrity, redaction, caps, and availability are still being recorded.” | Live sequence/time shown | Wait | Evidence complete or terminal final |
| Cancelling | “Cancelling — cleanup continues.” | “Stopping product work at {stage}; mandatory cleanup continues until {deadline}.” | Live sequence/time shown | Wait | Cancelled terminal before cleanup |
| Reconnecting | “Reconnecting to live updates…” | “Showing verified state through sequence {N} at {time}; missing events will replay or trigger one snapshot refresh.” | Last verified sequence/time shown | Wait / Refresh snapshot | Live current state |
| Stream stale | “Live updates delayed.” | “No event arrived for {duration}; showing state as of sequence {N} at {time}. Timers are paused.” | Explicit stale badge and as-of time | Refresh snapshot | Live or advancing timers |
| Disconnected | “Disconnected — showing last verified state.” | “Controller state is unknown after sequence {N} at {time}.” | Explicit offline badge | Reconnect / Refresh snapshot | Run failed or terminal |
| Recovering | “Recovering interrupted run.” | “{action label}, {completed}/{total}; only scoped resources are being reconciled.” | Recovery sequence/time shown | Wait | Resumed product execution |
| Recovery blocked | “Recovery blocked — controller bundle changed.” | “State is verified through sequence {N}. No process was signalled and no cleanup was attempted.” | Blocker observation and both digests shown | Manual procedure / Refresh | Cancel, cleanup, purge, retry, or resume |
| Run incompatible | “Run data uses an unsupported schema.” | “Unknown state was not mapped to success.” | Run revision shown | Safe raw diagnostic download | Passed, failed, or live interpretation |
| Terminal passed | “Passed.” | “Required checks and cleanup passed. Evidence health: {health}.” | Completion time and terminal sequence shown | Inspect / explicit retry subset if any | Evidence complete when degraded |
| Terminal failed | “Failed.” | “First failure: {first}. Primary cause: {primary}. Cleanup: {state}. Evidence: {health}.” | Completion time and terminal sequence shown | Retry failed / Not run subsets | Cleanup/evidence implied healthy |
| Terminal error | “Error.” | “{infrastructure, cleanup, contract, or recovery cause}. Product assertions are shown separately.” | Completion time and terminal sequence shown | Retry explicit eligible subset after resolution | Ordinary assertion failure only |
| Evidence degraded | “Product checks passed; evidence is degraded.” | “{missing/truncated reason}; retained {amount}.” | Evidence finalization time shown | Inspect evidence | Evidence complete |
| Evidence unavailable | “Evidence unavailable.” | “Verdict source remains; {availability reason}.” | Availability observation shown | Named provider action if one exists | No issues or zero samples |
| Evidence purged | “Evidence was purged.” | “Verdict, validations, lineage, and purge time remain.” | Purge time shown | None | Never collected or lost unexpectedly |
| History true empty | “No runs yet.” | “Start from Catalog to create the first run.” | Successful scan time shown | Open Catalog | History unavailable |
| History partial | “History is partial.” | “{N} run records could not be read; visible rows remain verified.” | Scan time shown | Open Health | Complete history |
| History unavailable | “Run history is unavailable.” | “The store could not be read safely.” | Failure time shown | Refresh / Open Health | No runs |
| Workspace purge partial | “Purge incomplete.” | “Removed {N}, retained {N}, failed {N}; lineage remains.” | Last purge attempt shown | Retry when `retryable=true` | Fully purged |
| Demo fixture | “Demo data — no runner connected.” | “Actions here do not start or cancel a real run.” | Persistent demo banner | Explore only | Live, ready, or safe runtime claim |

Messages are product copy, not examples. Tests assert them or stable accessible
equivalents.

## 12. Responsive behavior

| Width | Layout |
| ---: | --- |
| 375/390 | one column; full-screen filters, detail, preview, evidence; sticky bottom selection/action bar |
| 768 | one column with side sheets; cases use stacked rows |
| 1024 | catalog filter rail plus results; run summary plus case list |
| 1440 | catalog rail/results/detail; run list plus evidence drawer without hiding first failure |

At all widths and 200% zoom:

- no page-level horizontal overflow;
- long IDs/paths wrap or scroll inside their own noncritical disclosure;
- status, first failure, cleanup, stream freshness, Start, Cancel, and retry remain
  reachable;
- dialogs trap and return focus; route transitions move focus to the page
  heading;
- sticky surfaces never cover focused controls or the final row;
- safe-area insets are respected on mobile.

## 13. Keyboard, screen reader, and motion

A keyboard-only user can search, filter, select off-page scope, open detail,
review, start, inspect first failure/evidence, cancel, retry, and review
workspaces. Custom row click targets do not replace native links, buttons, and
checkboxes.

Live announcements:

- first failure once, polite;
- run terminal state once, polite;
- recovery blocker once, assertive;
- progress summaries at most every ten seconds and only when meaningfully
  changed;
- never announce individual log chunks, timers, samples, heartbeats, or every
  event.

Animation respects `prefers-reduced-motion`. A spinner is accompanied by text.
No essential state relies on pulsing or color.

## 14. Genericity and fixtures

The UI renders records, not known domains. The default fixture proves the four
primary domains, seven initial Runtime families, five initial Observability
families, and subordinate Harness Diagnostics area without a frontend registry.
Also add fixture data for:

- a fifth domain, new family, group, scenario, feature, owner, and validation;
- unknown display hints and additive schema fields;
- product, Compound, and no-surface Harness cases;
- all six execution surfaces and proof failures;
- every row in the async-state matrix;
- first failure differing from primary error;
- 1 passed, 1 failed/error, 3 fail-fast not-run;
- partial logs, unavailable evidence, and purged evidence;
- reconnect duplicate/gap, exact recovery, and recovery mismatch;
- 10,000 catalog cases through server pages and a 1,000-case admitted run;
- long translated-like strings, IDs, paths, and 200% zoom.

A fixture for new taxonomy data must require no component, route, icon, style,
or API change. Unknown schema major must fail visibly.

## 15. Interaction acceptance criteria

1. Feature search to three mixed cases to exact Review to Start uses one catalog
   request per page, one preview request, and one admission request.
2. All enabled controls perform an asserted request or navigation; all disabled
   controls expose adjacent reasons.
3. Selection remains exact across paging, filtering, background refresh, and
   exclusions; revision changes require review rather than silent scope change.
4. Run refresh and SSE replay produce the same rendered projection; duplicate
   events do not duplicate counts, rows, or announcements.
5. A failed validation followed by cleanup error preserves first and primary
   causes and never displays a terminal pass while cleanup runs.
6. Console-down fixtures block only console surfaces.
7. No-surface harness uses ordinary catalog/preview/run/history components and
   never displays product coverage or a surface error.
8. Evidence gaps, truncation, unsupported state, unavailability, invalidity, and
   purge use exact truthful messages and no fabricated zero.
9. Recovery mismatch exposes no Start, Cancel, Resume, generic Retry, shell, or
   mutation request.
10. The complete primary and failure journeys pass with pointer and keyboard at
    all five widths and 200% zoom, with no applicable WCAG 2.2 AA violation.
11. First failure and terminal state are announced once; logs/events do not
    flood assistive technology or steal focus.
12. Demo data remains persistently labeled and cannot produce a live or safe
    readiness claim.

## 16. Implementation handoff

Build the UI only after catalog, preview, manifest, event, projection, and error
fixtures are frozen. The smallest UI order is:

1. shell, tokens, semantic status, and fixture gallery;
2. catalog query, filters, rows, detail, and revision-qualified selection;
3. review dialog and all checking/ready/blocked/stale states;
4. run page from static projections, first/primary failure, cleanup, evidence;
5. SSE reconciliation and stale/disconnected/recovery states;
6. history and workspaces;
7. responsive, keyboard, screen-reader, zoom, and high-volume fixture proof.

Do not treat the existing static prototype DOM as an implementation constraint.
Preserve only the parts that survive data, interaction, and accessibility proof.
