# EphemeralOS Sandbox — Architecture Documentation Plan (Skeleton)

Synthesized from a 6-agent exploration of `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
(scopes: operations/adapters, web console, host management plane, daemon + runtime dispatch,
runtime isolation primitives, observability/config/infra). Date: 2026-07-11.

This file is the proposed structure for `ephemeral-sandbox-docs/architecture/`: 26 pages
organized into 8 clusters (each cluster = one subdirectory). Clusters are ordered by
importance; **Workspace runtime & storage is deliberately ranked second** — it is the
isolation core and the place where the deleted spec (§2.x, C1–C5) must be reconstructed.
Every page carries its own P0/P1/P2 priority, scope, source components, and open questions.

## Directory layout at a glance

```text
architecture/
├── 00-foundations/                3 pages · P0 P0 P0
├── 01-workspace-runtime/          6 pages · P0 P0 P0 P0 P0 P1
├── 02-security-model/             3 pages · P0 P0 P0
├── 03-management-plane/           2 pages · P0 P0
├── 04-daemon/                     3 pages · P0 P0 P0
├── 05-surfaces/                   3 pages · P0 P1 P1
├── 06-config-and-observability/   2 pages · P0 P1
└── 07-engineering/                4 pages · P1 P1 P2 P2
```

---

## Headline findings

1. **The docs must reconstruct a spec that no longer exists.** `docs/` contains only
   `.DS_Store` (last commit: "chore: remove obsolete docs"), but the code cites the deleted
   spec constantly — §2.3/§2.5/§2.6 and F1/F5/F10 in workspace-session code, "C1–C5" rules
   across the live-remount path, "§4.9" in the Docker engine, "spec decision 8" in telemetry.
   README links to `docs/daemon-http/README.md` and the obsidian migration spec dangle.
   These architecture pages will be the only written form of invariants that currently live
   in code comments.
2. **Existing coverage is near-zero.** Real docs exist only for the console crate (its own
   README), `config/README.md`, and `e2e/README.md`/`RUNNING.md`. Everything else has at
   most one line in the root README's component table.
3. **Three agents independently flagged the same boundary-law violation**: the
   `_stream_logs` / `cli_log(...)` progress-streaming dialect and auth-field injection are
   wire framing implemented in the client, gateway, daemon, and even parsed back out of
   Docker logs — despite the README stating wire framing lives only in `sandbox-protocol`.
   The wire-protocol page must document reality, and a maintainer should rule on intent.
4. **Repo-health issues found in passing** (not doc work, but worth acting on): the docs
   deletion likely broke `cargo run -p xtask -- operation-architecture-check` and
   `cargo test -p xtask` (the stale-reference checker requires git-tracked files under the
   deleted `docs/obsidian/` tree); `rusqlite`/`prost*` are declared workspace deps consumed
   by zero crates; e2e runs recreate a fragment of the deleted docs tree via its default
   metrics dir; and there is no CI — local `cargo test -p xtask` is the only
   boundary-law gate.

## Cross-cutting threads → dedicated pages

Deduplicated from per-agent findings into standalone pages: **Isolation model** (Docker
hardening + namespaces + seccomp + network, reported by 3 agents), **Wire protocol &
request lifecycle** (absorbs the error-taxonomy thread: envelope kinds, CLI exit codes
0/1/2, HTTP status mappings), **Tokens & trust boundaries** (gateway token + per-sandbox
daemon tokens + unauthenticated surfaces, 4 agents), **Ephemerality & crash recovery**
(host-side label recovery + in-sandbox PDEATHSIG/reap/sweep), **Operation catalog** (the
"one declaration, many surfaces" thread from CLI/MCP/console/manager/daemon), and
**Observability** (span-to-snapshot vertical). Protocol *versioning* gets no page of its
own because there is none — the versioning-by-absence story (stale-daemon `unknown_op`
translation, Phase 0 CLI freeze fixture) is covered inside the wire-protocol and catalog
pages.

## Priority conflicts resolved

- **Configuration**: P0 for the delivery model (the two-lane story changes what lands
  inside every container), P1 for the knob-by-knob reference — one page with a reference
  appendix.
- **Observability**: telemetry was rated P0 by its scope agent, P1 by the daemon agent.
  Resolved **P1** overall — you can break observability without breaking isolation — but
  its two P0-grade invariants (one Observer per process, cross-process trace handoff) are
  cross-referenced from the command-execution P0 page.
- **CLI/MCP**: P1 as pages, with their P0-grade invariants (projection lockstep validation,
  Phase 0 compatibility freeze, per-binary authority isolation) hoisted into the P0 catalog
  page.
- **Overlay crate**: kept **P0** despite its size — the newest-first lowerdir ordering and
  deliberate guard-leaking are silent-corruption-grade invariants.
- **e2e**: P2 for mechanics (well covered by its own READMEs); its Lane A/B config-delivery
  model is promoted into the P0 configuration page because it documents production
  behavior.

---

# Cluster 00 — Foundations (`00-foundations/`)

*The prerequisites for every other page: how the system is shaped and how the parts talk.
Read first.*

### `01-system-overview.md` — System overview: planes, crates, and the boundary law
- **Priority:** P0
- **Scope:** the operator→adapter→catalog→client→gateway→manager→daemon→runtime layering;
  the component table distilled into prose; the three grouping-only namespaces; which crate
  owns which vocabulary; enforcement via xtask.
- **Sources:** root README + all crates.
- **Open questions:** where the authoritative allowed-edge table will live now that the
  spec link dangles.

### `02-wire-protocol.md` — Wire protocol & request lifecycle
- **Priority:** P0
- **Scope:** end-to-end sequence diagram adapter→client→gateway→manager→daemon→runtime and
  back; the JSON-line envelope (`op`/`request_id`/`scope`/`args`); one-request-per-
  connection + half-close semantics; both auth fields and where each is checked; 16 MiB/
  30 s limits and the gateway-hardcoded vs daemon-configurable asymmetry; the
  `_stream_logs`/`cli_log` streaming dialect and its ownership drift outside
  sandbox-protocol; the full error taxonomy (transport kinds vs contract kinds, CLI exit
  codes, console HTTP-200-with-error-body mapping); versioning-by-absence and the
  stale-daemon `unknown_op`→"recreate sandbox" translation.
- **Sources:** sandbox-protocol, sandbox-operation-client, gateway connection handling,
  manager router, daemon rpc.
- **Open questions:** UDS intent (`gateway_socket_path: PathBuf` holds a TCP address);
  should streaming/auth framing migrate into sandbox-protocol; versioning plans.

### `03-operation-catalog.md` — The operation catalog: one declaration, many surfaces
- **Priority:** P0
- **Scope:** the contract/catalog/client three-way split; `RoutedOperation` const
  expansion; scope policy + visibility as access-control metadata enforced at three
  independent choke points (client builder, manager router, daemon dispatch);
  public/internal/http-only tiers; the `file_list` HTTP-only exception; why `sandbox_id`
  travels in scope, never in args; startup lockstep validations (CLI projection mirror,
  MCP schema generation with injected `sandbox_id`, console `public_routes()` check); the
  Phase 0 compatibility freeze fixture as the hidden public-surface contract; how to add
  an operation end-to-end.
- **Sources:** sandbox-operations/*, sandbox-cli projection, sandbox-mcp, sandbox-console
  rpc, manager dispatch, daemon registry.
- **Open questions:** governance of the Phase 0 fixture (additive-only forever?);
  manager-vs-management naming drift.

# Cluster 01 — Workspace runtime & storage (`01-workspace-runtime/`)

*The isolation core's mechanics — ranked second by importance. These six pages constantly
reference each other's invariants (leases, gates, newest-first ordering) and together
reconstruct the deleted §2.x/C1–C5 spec, making them the highest-decay-risk content in the
plan. Deep namespace/seccomp mechanics are detailed in `02-security-model/01`; read
alongside if unfamiliar.*

### `01-workspace-sessions.md` — Workspace sessions: lifecycle, gates, and finalize
- **Priority:** P0
- **Scope:** create → lease → holder spawn → ns-fd capture → veth → overlay mount →
  execute → capture → destroy, with every rollback edge; the admission gate/ledger
  discipline and lock ordering (gate → sessions → storage writer); the
  `Active→Finalizing→FinalizeFailed` finalize state machine; `PublishThenDestroy` implicit
  sessions (one-shot `exec_command` auto-publishes — and the publish can be rejected
  *after* the command succeeded, surfaced only as `publish_rejected`); guarded vs faulty
  destroy and recovery from `FinalizeFailed`. This page replaces the missing §2.x spec.
- **Sources:** sandbox-runtime operation workspace_session, sandbox-runtime-workspace.
- **Open questions:** location of the original spec.

### `02-command-execution.md` — Command execution end-to-end
- **Priority:** P0
- **Scope:** `exec_command` from dispatch to terminal result — implicit session creation,
  admission-token RAII, the engine's reserve/spawn/watch registry, the runner spawn dance
  (asymmetric CLOEXEC pipes, 8 MiB drain-while-waiting), PTY data flow into timestamped
  transcripts, windowed `read_command_lines` paging, the yield/poll model, stdin +
  Ctrl-C/Ctrl-D cancel (exit 130, timeout 124), pgid-scoped wait, cgroup placement.
  Cross-reference the one-Observer-per-process and trace-handoff invariants from
  `06-config-and-observability/02`.
- **Sources:** operation command service, namespace-execution, namespace-process
  shell_exec/shell_security.
- **Open questions:** unbounded transcript growth until session destroy — accepted?

### `03-layerstack.md` — LayerStack: manifests, leases, and garbage collection
- **Priority:** P0
- **Scope:** the content-addressed store; manifest schema v1 and the **newest-first** layer
  order; the publish OCC transaction (staging fsync → rename → digest sidecar → conflict
  recheck); the two-level storage writer lock (flock + in-process); the in-memory lease
  registry and release-time GC; the fail-closed boot sweep (never touches `B*` base
  layers, deletes nothing on manifest doubt); workspace-base seeding; the dual whiteout
  encoding (logical `.wh.` markers vs kernel char-dev/xattr) and the reserved-name publish
  rejection.
- **Sources:** sandbox-runtime-layerstack, operation layerstack service.
- **Open questions:** `.bytes` sidecars advisory-only confirmation; same-filesystem
  assumptions for rename/staging.

### `04-overlay-mounts.md` — Overlay mounts & the newest-first invariant *(short page)*
- **Priority:** P0
- **Scope:** the raw fsopen→fsconfig→fsmount→move_mount sequence (never mount(8));
  `userxattr` for rootless whiteouts; fd-pinned NOFOLLOW lowerdirs; the ordering invariant
  end-to-end (manifest → lease → OverlayHandle → first `lowerdir+` = highest priority);
  strict vs peel unmount and who *really* unmounts in production (namespace death — the
  RAII Drop path is production-dead by design).
- **Sources:** sandbox-runtime-overlay, namespace-process mount helpers.
- **Open questions:** none beyond kernel floor.

### `05-live-remount-and-squash.md` — Live remount & squash (reconstructing the C1–C5 protocol)
- **Priority:** P0
- **Scope:** the boot kernel gate (fail-safe: unproven ⇒ commit-only squash forever);
  squash's plan/build/commit with singleflight and lease-block boundaries; the in-memory
  substitution map; quiesce (cgroup ∪ /proc discovery, SIGSTOP freeze budget, per-task pin
  inspection); the 9-step staged MS_MOVE switch with MaskGuard (masks restored before any
  move); outcome classification (identity/migrated/parked/leased/faulty — faulty
  deliberately `mem::forget`s frozen tasks); the bounded-width remount sweep and
  blocked-reason attribution.
- **Sources:** workspace remount, namespace-execution quiesce, namespace-process
  remount_overlay + gate, operation squash impls.
- **Open questions:** the original C1–C5 spec; vestigial `runner_pids` allowlist; sweep
  width vs blocking-pool coupling.

### `06-file-operations-and-blame.md` — File operations, attribution, and blame
- **Priority:** P1
- **Scope:** dual routing (live session via ns-runner vs sessionless against the published
  stack); owner-string minting rules; audit-gate ordering (blame events land in commit
  order); the blame pipeline. Note the stale module doc claiming read/write/edit "ship
  later" — they're implemented.
- **Sources:** operation file service, layerstack audit.
- **Open questions:** none blocking.

# Cluster 02 — Security model & guarantees (`02-security-model/`)

*The product promise in one place — what isolates, what authenticates, what is guaranteed
to disappear. All three are cross-cutting pages deduplicated from multiple scopes.*

### `01-isolation-model.md` — Isolation model (layered)
- **Priority:** P0
- **Scope:** the four boundaries in order — Docker container hardening (de-privileged
  default: `SYS_ADMIN`+`NET_ADMIN` only, no-new-privileges, default seccomp, private
  cgroupns, loopback-only random host-port publish, memory/CPU caps, three-mount layout,
  `privileged: true` legacy escape hatch); per-workspace namespaces (user/mnt/pid[/net] via
  holder, single-entry uid map, pid-ns init child, `ns/pid_for_children` not `ns/pid`);
  the command sandbox (seccomp deny table, `clone3→ENOSYS` downgrade, x32 kill guard,
  12-cap bounding set, no_new_privs, `/eos` mount masks); network profiles (shared vs
  isolated bridge/veth/IP pool, what peer isolation does and doesn't provide,
  `rfc1918_egress: deny` accepted by config but rejected at runtime). Must include the
  topology nuance: the daemon binds `0.0.0.0` inside the container — loopback confinement
  happens only at Docker's host-port publish, and the HTTP listener is unauthenticated.
- **Sources:** sandbox-provider-docker, sandbox-runtime-namespace-process,
  sandbox-runtime-workspace, sandbox-daemon, sandbox-config.
- **Open questions:** exact peer-isolation mechanism and egress story for 10.244.0.0/24;
  official kernel floor (5.8 assert vs 5.11 feature needs vs gate probe as sole authority);
  support status of `privileged: true`.

### `02-tokens-and-trust-boundaries.md` — Tokens & trust boundaries
- **Priority:** P0
- **Scope:** gateway token lifecycle (mandatory in the binary, **optional in the library**
  — `None` accepts everything; flag/env only, never YAML; `/tmp/eos-gateway.token`
  handshake with the wrapper scripts); per-sandbox daemon tokens (uuid4 minting, exposure
  via Docker labels + container argv + plaintext-but-0600 registry JSON, never returned in
  responses); the unauthenticated `daemon_http` endpoint and 0600 unix socket; console
  credential confinement (four-field whitelist reconstruction of browser requests); the
  overall "loopback + same-origin + Docker-socket-equals-host" trust model; no
  TLS/CORS/origin checks anywhere.
- **Sources:** gateway, provider-docker, manager store, console, operation-client,
  bin scripts.
- **Open questions:** is non-loopback bind ever intended (TLS story); browser authn
  roadmap; token rotation contract (console must restart after gateway restart —
  script-encoded only); constant-time token comparison.

### `03-ephemerality-and-crash-recovery.md` — Ephemerality & crash recovery guarantees
- **Priority:** P0
- **Scope:** the system-wide "what survives what" matrix — gateway restart (label recovery,
  registry reconcile), daemon crash (PDEATHSIG makes every holder/runner provably dead;
  boot reap deletes run dirs; fail-closed sweep GCs layers; spools purged), what is
  RAM-only by design (leases, squash substitution maps, parked leases, export spools,
  endpoint caches) and what persists where (registry JSON, `manager.json` handles,
  layerstack manifests, audit store, transcripts).
- **Sources:** manager store, provider recovery, workspace persistence, layerstack cleanup,
  daemon boot.
- **Open questions:** none new — this page consolidates; cross-reference
  `03-management-plane/01` and `04-daemon/02`.

# Cluster 03 — Host management plane (`03-management-plane/`)

*Everything the gateway/manager/provider do on the host side of the trust boundary.
Deliberately thin — tokens, recovery, and packaging live in clusters 02 and 07.*

### `01-sandbox-lifecycle.md` — Sandbox lifecycle: create, readiness, destroy, recovery
- **Priority:** P0
- **Scope:** the `Creating→Ready→Stopping→Stopped/Failed` state machine with every
  transition trigger; the create sequence (shared-base build → container create-stopped →
  asset upload → start → authenticated readiness handshake → Ready) with per-step rollback
  and batch all-or-nothing semantics; why forwarding gates on Ready; destroy
  retry-from-Failed; registry persistence (atomic 0600 JSON snapshot); label-driven Docker
  recovery + `reconcile` (orphans→Failed); the gap: recovery marks containers Ready without
  re-running the handshake; the `sandbox_daemon_ready` handshake and why a TCP connect
  isn't a readiness signal.
- **Sources:** sandbox-manager, sandbox-provider-docker, gateway composition root,
  sandbox-protocol handshake.
- **Open questions:** Failed-record and shared-base-volume GC (never collected today);
  multi-gateway-per-host support (`gateway_instance_id` labels vs uninstanced shared-base
  volume names); stability of the log-prefix failure classification.

### `02-export-pipeline.md` — The export pipeline & host-side apply hardening
- **Priority:** P0
- **Scope:** the two-op export (daemon spools tar.zst, manager pages chunks with per-chunk
  integrity checks); destination deny-list (registry file, `/`, `$HOME`, `.export`
  components) checked lexically *and* post-canonicalization; the compromised-daemon threat
  model of `export_apply` — validate-before-mutate two-pass, O_NOFOLLOW fd-walk, O_EXCL
  creation, zstd-bomb/entry caps, atomic nonce renders, three-pass whiteout ordering.
- **Sources:** manager export_changes + export_apply, operation layerstack export.
- **Open questions:** spool non-persistence (restart drops it — re-run) as a stated
  contract.

# Cluster 04 — Daemon internals (`04-daemon/`)

*The in-container server as a process: its personalities, lifecycle, and network surfaces.*

### `01-process-model.md` — One binary, four processes: the daemon process model
- **Priority:** P0
- **Scope:** serve / ns-holder / ns-runner / gate-probe personalities; the `current_exe`
  re-exec contract (any embedding binary must implement the subcommands —
  `ForkRunnerLauncher` doesn't fork); fd-inheritance + the global spawn lock; the holder's
  3-token pipe handshake (`ns-up`/`net-ready`/`ready`); the PDEATHSIG kill chain; the
  exit-code contract (holder 1/2); env-var plumbing (`SANDBOX_DAEMON_*`), auth token never
  in argv.
- **Sources:** sandbox-daemon main/serve/holder/runner/gate_probe, namespace-process,
  namespace-execution launcher.
- **Open questions:** is `serve --spawn` production or e2e-only; intended AF_UNIX RPC
  clients.

### `02-daemon-lifecycle.md` — Daemon lifecycle: startup, boot recovery, shutdown
- **Priority:** P0
- **Scope:** config load → cgroup self-vacation → the eight-step storage boot sequence
  (base ensure, provisioning-bind detach, kernel-floor assert, live-remount gate probe +
  latch, spool purge, session reap, fail-closed storage sweep) → listener bind order →
  readiness; the ordered shutdown drain (cancel → stop listeners → drain in-flight →
  pid/socket cleanup); connection semaphore/backpressure.
- **Sources:** sandbox-daemon rpc/lifecycle, sandbox-runtime `services.rs`.
- **Open questions:** kernel floor authority (ties to `02-security-model/01`).

### `03-http-surface.md` — Daemon HTTP surface: the allowlist and app forwarding
- **Priority:** P0
- **Scope:** the exact four-route allowlist and deliberate 404s (`/files/read` etc.);
  `file_list` as the sole HTTP operation (and its two-channel error mapping — transport
  400 vs dispatch errors in HTTP **200**); shared vs isolated forward resolution through
  the session registry; reverse-proxy mechanics (hop-by-hop stripping, X-Forwarded-*,
  WebSocket upgrade tunnels — unbounded after 101); why this surface is safe without auth
  (host loopback publish topology).
- **Sources:** sandbox-daemon http/, provider port publishing.
- **Open questions:** HTTP-200 dispatch errors — contract or accident; upgrade-tunnel idle
  timeout.

# Cluster 05 — User surfaces (`05-surfaces/`)

*The adapters. Thin projections over the catalog — readable with only Foundations as
prerequisite.*

### `01-web-console.md` — Web console: one origin, two planes
- **Priority:** P0
- **Scope:** browser → console `/api/rpc` → authenticated gateway RPC (field-whitelist
  reconstruction, public-route validation, SSE streaming variant) vs browser → console →
  per-sandbox `daemon_http` (health, files/list, `/s/` preview prefix-swap with 3s
  endpoint cache); credential confinement as the defining job; status-code mapping; the
  deliberate v0 security posture (loopback + same-origin only) and its unstated residual
  risks (DNS rebinding, CSRF-shaped posts).
- **Sources:** sandbox-console, operation-client, catalog.
- **Open questions:** post-v0 browser auth; `file_edit`/`export_changes` validated but
  unused by the SPA — CLI-only UX or unbuilt UI?

### `02-cli-and-mcp.md` — Adapters: the three CLIs and sandbox-mcp
- **Priority:** P1
- **Scope:** authority isolation and its two different proofs (CLI compile-time
  `required-features` vs MCP runtime `--set`); scope-selector resolution matrix per
  binary; the agent output contract (stdout/stderr JSON, exit 0/1/2, `--progress`);
  wrapper scripts and the token-file pickup (plus the stale-`target/debug` footgun); MCP
  schema generation and `is_error` mapping.
- **Sources:** sandbox-cli, sandbox-mcp, bin wrappers.
- **Open questions:** why MCP compiles all three catalogs.

### `03-spa-data-flow.md` — SPA data flow: polling, ledger, transcripts
- **Priority:** P1
- **Scope:** `usePoll` cadence/idle-decay engine; the localStorage command ledger
  reconciled against observability snapshots; transcript offset paging; the file-edit
  conflict-detection protocol; SSE for lifecycle ops; hand-mirrored TypeScript wire types
  (drift risk).
- **Sources:** web/console.
- **Open questions:** codegen plans.

# Cluster 06 — Configuration & observability (`06-config-and-observability/`)

*The two cross-cutting verticals that every component participates in but none owns.*

### `01-configuration.md` — Configuration: one YAML, two lanes
- **Priority:** P0
- **Scope:** `ConfigDocument` load→merge→validate→typed-inject; the `yaml.rs` parser fence;
  `deny_unknown_fields` + `validate()` pattern; **Lane A** (installer re-reads and uploads
  the YAML on *every* create — rewrites govern the next sandbox, never running ones; bad
  values = structured create error + rollback) vs **Lane B** (gateway/manager sections load
  at gateway start — bad values = fails to serve); section-by-section prd.yml walk
  including sections that exist only as Rust defaults (observability, gateway, console);
  the host/container config-agreement invariant; known softness (malformed `observability`
  section silently defaults; unknown top-level sections ignored). Appendix (P1): knob
  reference with defaults and blast radius across
  gateway/manager/daemon/runtime/runner/observability.
- **Sources:** sandbox-config, config/, gateway main, provider installer, e2e config
  family.
- **Open questions:** observability silent-default — bug or contract; stale "eos-sandbox"
  naming; compile-time `CARGO_MANIFEST_DIR` baking in `ConfigPath::prd()`.

### `02-observability.md` — Observability: from span to snapshot
- **Priority:** P1
- **Scope:** Observer/SpanGuard/SpanRegistry emit model; one-Observer-per-process;
  `d-*`/`np-*` cross-process trace handoff via log-path + parent context; NDJSON record
  grammar and naming vocabulary; sink truncation/rotation; Reader folds (span forest,
  counter deltas); the query port and five operations; the sandbox-scoped vs
  manager-aggregate `snapshot` split (same op name, two applications, keyed by scope).
  Corrections the doc must state: **sampling is request-triggered, not periodic** (idle
  sandboxes emit nothing), and **storage is NDJSON — the sqlite/protobuf workspace deps
  are unused**.
- **Sources:** sandbox-observability-telemetry, sandbox-observability-query, daemon
  observability composition, manager aggregate snapshot.
- **Open questions:** rusqlite/prost intent; sampling cadence deliberate or placeholder.

# Cluster 07 — Engineering & operations (`07-engineering/`)

*About developing and operating the repo rather than the product's runtime architecture.*

### `01-packaging-pipeline.md` — Packaging pipeline: source → musl daemon → container
- **Priority:** P1
- **Scope:** setup-musl-cross; xtask builder selection (zigbuild→cross→error; escape
  hatches) and profiles; the dist/ artifact set (binaries, manifests, SHA256SUMS,
  minisign, git toolchains, console SPA); the launcher's mtime staleness heuristic
  (hand-maintained crate list; also re-parses YAML with `sed`); per-create upload
  sequence. Flag: provenance artifacts are produced but **never verified** at install
  time; `dist/git` tars have no in-repo build recipe.
- **Sources:** xtask, dist/, bin scripts, provider installer.
- **Open questions:** provenance verification as gap-or-roadmap; who builds
  `dist/git/*.tar`.

### `02-boundary-law-enforcement.md` — Boundary-law enforcement (xtask checks)
- **Priority:** P1
- **Scope:** what `operation-architecture-check` and the check-* policies enforce;
  `cargo test -p xtask` runs them against the live repo; **there is no CI** — local runs
  are the gate; current broken state of the stale-reference checker after the docs
  deletion.
- **Sources:** xtask operation_architecture + policy tests.
- **Open questions:** intended post-docs-removal state of the stale checker.

### `03-e2e-suite.md` — E2E suite architecture *(thin — defer mechanics to e2e/README+RUNNING)*
- **Priority:** P2
- **Scope:** family/fixture layout, gateway custody model, the structured-JSON-only
  verification law and its two sanctioned exceptions (daemon-HTTP boundary tests, two
  allowlisted direct-daemon internal ops). Note: README claims e2e covers the console; the
  suite explicitly disclaims it — console coverage lives in crate integration tests.
- **Sources:** e2e/.
- **Open questions:** whose job is console E2E.

### `04-local-dev.md` — Local development bring-up
- **Priority:** P2
- **Scope:** `start-sandbox-docker-gateway` / `start-sandbox-console-stack` phases; the
  env/file contract (`/tmp/eos-gateway.token`, pid/log files, ports 7878/7880); failure
  modes (stale token after gateway restart, stale debug binaries, unbuilt SPA
  placeholder).
- **Sources:** bin/, crate READMEs.
- **Open questions:** none blocking.

---

## Consolidated open questions for maintainers (blocking doc authorship)

1. **Where is the deleted spec?** (obsidian vault: operation-migration spec, C1–C5 remount
   rules, §2.x workspace-session invariants, observability spec, `ab_driver.py`). Can it
   be imported into ephemeral-sandbox-docs? Affects `00-foundations/03`,
   `01-workspace-runtime/01`, `01-workspace-runtime/05`, `06-config-and-observability/02`,
   `07-engineering/02`.
2. Streaming/auth-field framing: migrate into sandbox-protocol per the boundary law, or
   document co-ownership as intentional?
3. `LocalSandboxDaemonInstaller` + `manager.local_daemon` config: planned `--backend
   local` or dead scaffolding?
4. Auth-optional gateway (library) and non-loopback binds: supported deployments or
   dev-only? TLS roadmap?
5. Token rotation: is "restart console after gateway restart" permanent?
6. Isolated networking: where is peer isolation actually enforced, and what's the egress
   story?
7. Official kernel floor (5.8 assert vs 5.11 features vs gate-probe-as-authority)?
8. `rusqlite`/`prost*` workspace deps: planned storage engine or deletable?
9. Malformed `observability` config section silently defaulting: bug or contract?
10. Post-docs-removal state of the xtask stale checker — is `cargo test -p xtask` expected
    red right now?
11. Phase 0 CLI compatibility fixture: what's the change policy?
12. Artifact provenance: should install-time sha256/minisign verification be documented as
    a known gap or added? Who builds `dist/git/*.tar`?
13. Failed-record and shared-base-volume GC: sanctioned cleanup path?
14. `/files/list` returning HTTP 200 for dispatch errors: contract or accident?

## Suggested writing order

Cluster 00 first (prerequisites for everything), then cluster 01 in full — it is ranked
second by importance and holds the missing-spec reconstructions with the highest decay
risk (`01-workspace-sessions`, `02-command-execution`, `05-live-remount-and-squash`).
Then the remaining P0 pages by cluster order (02 → 03 → 04 → 05/01 → 06/01), then P1,
then P2.

## Source agent reports

The six per-scope exploration reports (with file:line anchors for every key abstraction)
were produced by session agents: ops/adapters `a97eb87037a1bf5b3`, console
`a0cdfa7d9edb12097`, host-mgmt `af79af236a13b1ab0`, daemon `a09d5820264b7b5a2`,
runtime-prims `aa18271ae6c950247`, obs/config/infra `a82389bbc91c60216`.
