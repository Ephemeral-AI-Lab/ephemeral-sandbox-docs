Implement and fully verify the FlashCart demo in /Users/yifanxu/Ephemeral-AI-Lab. First read ephemeral-sandbox-docs/multiagent/IMPLEMENTATION_SPEC.md and DESIGN.md completely, then inspect every implementation/test they reference. The spec is normative. Do not stop at a plan, scaffolding, mocks, or a partial path. Preserve unrelated changes; do not commit or publish.

Deliver:

1. Add and test the sandbox-runtime-cli request-ID override for exact runtime trace correlation, preserving default UUID behavior.
2. Build ephemeral-sandbox-test/demo/multi-agent: deterministic generator/recipes, scenario, call budget, ten checked-in JSONL plans, payloads, tests, and a standard-library runner. Reuse current helpers; avoid a general workflow engine.
3. Generate 350–500 meaningful public CLI calls; prefer 450–500. Per-agent/category figures are recommendations only; derive and record the actual matrix. Each counted row starts one real CLI process and parses one response. Count engine/telemetry/control work separately. Reject padding, no-ops, sleeps, installs/downloads, and unchanged test reruns. Never pad counts.
4. Start ten gated automatic workspaces concurrently, with sequential work per lane and ten lanes in parallel. Build the offline storefront from the minimal bootstrap using Node/browser standard APIs. Publish all ten primary lanes; prove line-disjoint merge and ten raw blame owners, mapping owners to A01–A10 only as a labeled runner join.
5. Run a separate conflict wave from one head: A06 changes the seeded line via file_edit; A08 changes it via exec_command and creates unrelated files. Publish A06; require A08 publish_rejected=true/source_conflict; prove no revision advance or partial publish; retry A08 from a fresh head successfully.
6. Via trusted session control only, prove two Shared sessions collide on port 4173 and two isolated sessions both bind it. Stop before destroy; prove experiment files never reach shared content/blame.
7. Retain immutable, redacted timing, observability, blame, preview, assertion, and cleanup evidence. Never fabricate facts; keep process, publication, provenance, trusted control, runner mapping, and narrative distinct.
8. Make multiagent/index.html the light-theme control room with explicit sample/live/recorded modes, monotonic polling, scene checkpoints, nonblank failures, safe evidence, retained preview, accessibility, and recorded export. Live errors never fall back to sample.

Work through spec phases 0–5. Before entering the next phase, satisfy every acceptance checkbox with command, artifact, digest, and verdict evidence; invalidated evidence reopens that gate and all dependents. A10 runs final regression from a fresh post-merge workspace.

For every bug, preserve artifacts, reduce it in a fresh sandbox, classify it, patch the smallest script/runner/CLI/runtime layer, add a regression, rebuild, and restart fresh. Never weaken assertions or blindly retry mutations. Overall pass requires execution success and clean cleanup.

Use existing Playwright to verify both UIs, data/failure modes, hostile input, no blank states, commerce flows, preview/export, console, and accessibility.

Done means: all authored public CLI calls complete, with a validated total of 350–500; ten simultaneous workspaces; expected final-tree hashes and ten owners; atomic rejection plus retry; Shared collision plus two isolated servers; complete observability; all tests green; no success/interrupt leaks; three clean presentation-machine runs with frozen hashes; and a verified recorded package under ephemeral-sandbox-docs/multiagent/generated.

Continue autonomously while safe work remains. If blocked, give the exact command, artifact, diagnosis, and smallest needed decision. Finally report changed files, test outcomes, run/artifact IDs, call totals, acceptance evidence, cleanup, and only genuinely deferred non-required work.
