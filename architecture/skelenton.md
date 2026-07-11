# EphemeralOS Sandbox — Architecture Documentation Plan (Skeleton)

Synthesized from a 6-agent exploration of `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
(scopes: operations/adapters, web console, host management plane, daemon + runtime dispatch,
runtime isolation primitives, observability/config/infra). Date: 2026-07-11.
Revised the same day after a dedicated 8-topic deep-dive into cluster 01 (workspace
runtime & storage): that cluster is now 9 dependency-ordered pages with its own writing
spec at `01-workspace-runtime/SPEC.md`.

This file is the proposed structure for `ephemeral-sandbox-docs/architecture/`: 29 pages
organized into 8 clusters (each cluster = one subdirectory). Clusters are ordered by
importance; **Workspace runtime & storage is deliberately ranked second** — it is the
isolation core and the place where the deleted spec (§2.x, C1–C5) is recovered from git
history and reconstructed. Every page carries its own P0/P1/P2 priority, scope, source
components, and open questions.

## Directory layout at a glance

```text
architecture/
├── 00-foundations/                3 pages · P0 P0 P0
├── 01-workspace-runtime/          9 pages · P0 P0 P0 P0 P0 P0 P1 P0 P0 (dependency-ordered)
├── 02-security-model/             3 pages · P0 P0 P0
├── 03-management-plane/           2 pages · P0 P0
├── 04-daemon/                     3 pages · P0 P0 P0
├── 05-surfaces/                   3 pages · P0 P1 P1
├── 06-config-and-observability/   2 pages · P0 P1
└── 07-engineering/                4 pages · P1 P1 P2 P2
```

---

## Headline findings

1. **The deleted spec is recoverable — and partially recovered.** `docs/` contains only
   `.DS_Store` (last commit `0f7d02486` "chore: remove obsolete docs"), but the code cites
   the deleted spec constantly — §2.3/§2.5/§2.6 and F1/F5/F10 in workspace-session code,
   "C1–C5" rules across the live-remount path, "§4.9" in the Docker engine, "spec decision
   8" in telemetry. README links to `docs/daemon-http/README.md` and the obsidian migration
   spec dangle. The cluster-01 deep-dive found the squash/remount spec intact in git
   history — `git show '0f7d02486^:docs/obsidian/ephemeral-os/implementation_plan/squash/spec.md'`
   (1,420 lines: C1–C6, invariants, lock discipline) plus its 785-line test catalog and the
   remount-rework docs, all deleted by the same commit. Import these before writing
   (`01-workspace-runtime/SPEC.md` step 0) and hunt the remaining spec families (§2.x
   sessions, C3 file-auditability, observability) in the same deleted tree. The
   architecture pages remain the only *living* form of those invariants.
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

*The isolation core's mechanics — ranked second by importance. Restructured 2026-07-11
after a dedicated 8-topic deep-dive; the full writing spec (per-page outlines, must-state
invariants, file:line anchors, demo path) lives in `01-workspace-runtime/SPEC.md`. Nine
pages in **strict dependency order** — each page uses only concepts introduced by earlier
pages, so the cluster reads front-to-back as a demonstration: two independent roots (`01`
storage truth, `02` process substrate) meet in `03` (the overlay mount); `04` (sessions)
orchestrates them; `05`/`06` are the two mutation surfaces; `07` closes the write-back
loop into the store; `08` is the capstone that touches everything. Deep
namespace/holder/runner *mechanics* now live here (page `02`) — `02-security-model/01`
keeps the security analysis. Together these pages carry the recovered-and-reconstructed
§2.x/C1–C5 spec, the highest-decay-risk content in the plan.*

### `00-runtime-tour.md` — The runtime tour: one loop, eight mechanisms *(spine, half page)*
- **Priority:** P0
- **Scope:** the workspace lifecycle loop in one diagram (lease → holder → mount →
  execute/file-ops → capture → publish → squash → remount → destroy → GC); the unified
  `/eos` data-root map with per-subtree ownership; the cross-topic handoff-artifact table
  (12 edges, each a documented contract); the demonstration path (each step exercises
  exactly one page, in page order); reading order for newcomers.
- **Sources:** `01-workspace-runtime/SPEC.md` synthesis; `operation/src/services.rs`
  (composition root).
- **Open questions:** none.

### `01-layerstack-store.md` — LayerStack: store layout, hashes, leases, and GC
- **Priority:** P0 *(was `03-layerstack.md`)*
- **Scope:** on-disk layout (`manifest.json`, `layers/` with counter-based `B*`/`L*`/`S*`
  ids — **not** content hashes, `staging/`, `.layer-metadata/*.{digest,bytes}` sidecars,
  `.storage-writer.lock`, `workspace.json`); the **three distinct sha256 roles**
  (per-layer changeset digest = head-dedup only; manifest root hash = the OCC revision
  token; base root hash = shared-cache key) plus fingerprint/audit reuse; the newest-first
  manifest order — constructed at publish-prepend, never re-validated, consumed by every
  reader; the two-level writer lock (flock lifetime = open `LayerStack`; in-process
  reentrant RW) and the documented lock order; the RAM-only lease registry +
  release-time GC (the only GC besides the boot sweep); the fail-closed boot sweep (`B*`
  never deleted; manifest doubt ⇒ delete nothing); workspace-base seeding (private build
  vs shared-cache docker volume vs per-sandbox seed archive) and the `workspace.json`
  binding contract; the boot workspace-root **bind detach**; the three scratch roots
  (workspace, namespace-execution, gate-probe-in-staging).
- **Sources:** sandbox-runtime-layerstack (all), `operation/src/services.rs` boot steps,
  provider-docker archive/runtime (seeding).
- **Open questions:** `.bytes` sidecars advisory-only confirmation; release-time GC has
  no explicit `B*` guard (safety rests on the base always being in the active manifest) —
  add a defensive check?

### `02-namespace-processes.md` — Holder & runner: the namespace process substrate
- **Priority:** P0 *(new page — mechanics were previously split across
  `02-security-model/01` and `04-daemon/01`)*
- **Scope:** one static binary, four personalities, and why single-threaded subprocess
  bodies exist at all (`unshare`/`setns` with `CLONE_NEWUSER` require a single-threaded
  caller); the holder — `unshare(NEWUSER|NEWNS|NEWPID[+NEWNET])`, single-entry self
  uid/gid map, `mount_change("/", PRIVATE|REC)`, the pid-ns init fork trick and why
  `ns/pid_for_children` not `ns/pid`, the 3-token handshake (`ns-up` → daemon does
  ns-fd capture/veth/overlay-mount → `net-ready …` → in-ns network config → `ready`);
  ns-fd capture with **permanently cleared CLOEXEC** (raw fd integers as protocol
  values); the runner — the `current_exe` re-exec contract (`ForkRunnerLauncher` doesn't
  fork), the asymmetric-CLOEXEC pipe pair, the global spawn lock, EOF-framed JSON
  request/result, the four payload kinds (`--shell|--file-op|--mount-overlay|--remount-overlay`),
  setns join order (user first), the 8 MiB drain-while-waiting; the PDEATHSIG kill chain
  (daemon→holder SIGKILL; holder→pid-init SIGTERM; init death collapses the pid ns) as
  the foundation of boot reap; the holder exit-code contract (1/2); env plumbing
  (`SANDBOX_DAEMON_CONFIG_YAML` hard-required by runners; auth token env-only, never
  argv).
- **Sources:** sandbox-runtime-namespace-process, workspace `namespace/*`,
  namespace-execution `launcher.rs`, daemon main/holder/serve/runner.
- **Open questions:** holder spawn happens outside the spawn lock (benign asymmetry?);
  runner fd hygiene — CLOEXEC-cleared ns fds of *other* sessions are visible inside every
  runner; `SANDBOX_DAEMON_SANDBOX_ID` is set but read by nothing in-repo.

### `03-overlay-mount.md` — The overlay mount: lowerdir order, upper/work, who unmounts *(short)*
- **Priority:** P0 *(was `04-overlay-mounts.md`)*
- **Scope:** the raw fsopen → `lowerdir+`×N → `userxattr` → upperdir/workdir →
  fsconfig_create → fsmount → move_mount sequence (and why not mount(2)/mount(8));
  fd-pinned NOFOLLOW lowerdirs vs real-path upper/work (kernel restriction); the complete
  ordering-invariant chain across all eight hops (publish-prepend → manifest → lease →
  snapshot ref → entry → request JSON → `OverlayHandle` → first `lowerdir+` = highest
  priority); upper/work under the session run dir (same-fs by construction; per-remount
  fresh sibling workdir, **same upperdir forever**); the mount executes inside the
  holder's namespaces via the `--mount-overlay` runner and the RAII guard is deliberately
  leaked — namespace death is the production unmounter (`Drop`/peel is production-dead;
  `strict_unmount`/`move_mountpoint` exist for the remount protocol); `/eos` tmpfs masks
  applied post-mount by the same runner.
- **Sources:** sandbox-runtime-overlay, workspace `overlay/{dirs,tree}.rs`,
  namespace-process `setns/mount_overlay.rs`, daemon runner.
- **Open questions:** kernel floor — the boot 5.8 assert covers neither `lowerdir+`
  (≥ 6.8) nor `userxattr` (≥ 5.11); the first session mount is the de-facto probe.

### `04-workspace-sessions.md` — Workspace sessions: lifecycle, gates, finalize, network
- **Priority:** P0 *(was `01-workspace-sessions.md`)*
- **Scope:** the create sequence with every rollback edge (lease → overlay dirs → holder
  spawn → ns-fd capture → veth install → overlay mount → net-ready → persist) and destroy
  with lease + parked-lease release; the admission gate/ledger discipline and the lock
  order (gate → sessions map → storage writer); the `Active→Finalizing→FinalizeFailed`
  machine; `PublishThenDestroy` implicit sessions — the publish can be rejected *after*
  the command succeeded, surfaced only as `publish_rejected`; guarded vs faulty destroy
  (§2.5/§2.6) and recovery; **network modes** — shared = the *container's* netns (not the
  host), isolated = bridge + veth with **bridge-port isolation only** (the nft layer was
  removed in `d3c0538e1`; `rfc1918_egress: deny` is config-accepted but rejected at
  create; egress is environment-provided); `manager.json` persistence and the
  PDEATHSIG-backed boot reap; the composition-root service graph and boot order as
  orientation. This page replaces the missing §2.x spec.
- **Sources:** sandbox-runtime-workspace (session/lifecycle/service/isolated_network_setup),
  operation workspace_session, `operation/src/services.rs`.
- **Open questions:** finalize capture error = silent data loss (span attribute only) —
  accepted?; `latest_snapshot`/`ReadonlySnapshotHandle` has no production caller.

### `05-command-execution.md` — Command execution end-to-end
- **Priority:** P0 *(was `02-command-execution.md`)*
- **Scope:** `exec_command` from dispatch to terminal result — implicit session creation,
  admission-token RAII, the engine's reserve/spawn/watch registry, the runner spawn dance,
  PTY reality (no controlling terminal, no window size, no raw mode — echo lands in
  transcripts; stdin containing ETX/EOT cancels, a literal Ctrl-C byte is undeliverable),
  timestamped transcripts and their lifecycle (unbounded while running; deleted on
  512-entry terminal eviction, **not** on session destroy), windowed `read_command_lines`
  paging, the yield/poll model, exit codes 130/124/−signal, pgid-scoped wait, cgroup
  placement (later the quiesce discovery seed — forward ref to `08`), shell_security
  hardening hook anchors. Cross-reference the one-Observer-per-process and trace-handoff
  invariants from `06-config-and-observability/02`.
- **Sources:** operation command service, namespace-execution, namespace-process
  shell_exec/shell_security, daemon `runner/shell.rs`.
- **Open questions:** unbounded transcript growth — accepted?; no boot reaper found for
  orphaned `/eos/namespace_execution/*` dirs after a crash.

### `06-file-operations-and-blame.md` — File operations, attribution, and blame
- **Priority:** P1
- **Scope:** the dual-routing decision (presence of `workspace_session_id`; pre-gate
  resolve for path mapping, re-resolve under the gate); per-op mechanics — read windows,
  atomic runner-side writes, edit's exact-string conflict detection and the session-edit
  non-atomicity window (read and write are two separately-gated runner ops; the
  sessionless route is an atomic RMW under the exclusive writer lock), one-level list and
  its HTTP-only exposure; the owner grammar (`workspace_session:<id>` | `operation:<id>` |
  `original` | `unknown`) and the boundary law (layerstack emits owner-free `Origin`; the
  file domain mints owners); the NDJSON audit store and the `audit_gate` commit-order
  guarantee; blame as a pure store read over path-keyed line snapshots (survives squash
  by construction). Fix in passing: the stale module doc claiming read/write/edit "ship
  later".
- **Sources:** operation file service (incl. audit/store), workspace + operation
  `run_file_op`, layerstack read side.
- **Open questions:** none blocking.

### `07-capture-and-publish.md` — Capture & publish: from upperdir to layer
- **Priority:** P0 *(new page — previously smeared across old `01` and `03`)*
- **Scope:** the host-side upperdir scan (kernel whiteout/opaque **metadata only**; `.wh.`
  dirent names are user data, rejected fail-closed at publish; `WriteFile` captures are
  metadata-only references streamed at publish time); protected drops (special files
  tolerated, non-UTF-8 names fail the whole publish); content fingerprints (sha256,
  content-only — the executable bit is invisible to conflict detection) as the **real
  OCC** — the manifest recheck is practically unreachable; gitignore **routing, not
  filtering** (patterns read from the *base manifest*'s `.gitignore` files; ignored paths
  skip validation and get wholesale attribution); plan → resolve (three-way merge with
  8 MiB and Myers-diff caps) → route → layer write (kernel whiteout dual encoding) → the
  OCC commit (head-digest dedup no-op, staging → fsync → rename → digest sidecar →
  manifest prepend); the `publish_rejected` class taxonomy and the OnceLock surfacing
  chain onto the completing command's terminal output; `amend_path` (sessionless RMW —
  "the three-way merge never runs… nothing to retry"); audit-append ordering (G3/§13).
  Appendix: projection (`MergedView` consumers; full `project()` is test-only) and the
  export delta stream (logical `.wh.` encoding — the reverse translation).
- **Sources:** workspace `overlay/capture.rs` + `capture_changes.rs`, layerstack
  `stack/publish/**` + `stack/ops/publish.rs` + `stack/layer/write.rs` +
  `storage/whiteout.rs`, operation layerstack impls, operation finalize.
- **Open questions:** an empty capture with non-empty protected drops surfaces nowhere;
  merged-file executable-bit loss — bug or accepted?

### `08-squash-and-live-remount.md` — Squash & live remount (the C1–C5 protocol)
- **Priority:** P0 *(was `05-live-remount-and-squash.md`)* — **write against the
  recovered spec**
  (`git show '0f7d02486^:docs/obsidian/ephemeral-os/implementation_plan/squash/spec.md'`).
- **Scope:** why remount exists (lease-pinned layers cannot reclaim under live sessions);
  the boot kernel gate (G1+G2 — a miniature of the production protocol run in a scratch
  userns; unproven ⇒ commit-only squash forever); squash plan/build/commit (singleflight
  riding the outcome through the sweep, lease-newest boundaries, ≥2-layer non-`B*`
  blocks, flatten's newest-wins fold with whiteout collapse + opaque dual encoding, the
  single `syncfs` durability barrier, substitution recording, plan-lease release as the
  only GC); lease rewrite (oldest-generation-first contraction, pin-overlap, Identity
  degradation on any doubt); quiesce (holder-mountinfo check first, cgroup ∪ /proc
  discovery, SIGSTOP + freeze budget, C4 per-task pin inspection incl. the anon-inode
  allowlist); the 9-step staged switch (MaskGuard restore-before-move, point-of-no-return
  = first MS_MOVE success, strict-unmount EBUSY ⇒ park); C5 outcome classification
  (identity/migrated/parked/leased/faulty — faulty deliberately `mem::forget`s frozen
  tasks; a missing report is decided by the workspace-mount-id comparison); the
  bounded-width sweep, blocked-reason attribution, and batched handle persistence.
- **Sources:** layerstack squash/flatten/rewrite/cleanup, workspace
  `lifecycle/remount.rs`, namespace-execution `quiesce.rs`, namespace-process `gate.rs` +
  `setns/remount_overlay.rs`, operation squash impls; the recovered spec +
  `e2e/manager/management/squash/test_spec.md`.
- **Open questions:** vestigial `runner_pids` allowlist; sweep width vs blocking-pool
  coupling; PTY sessions always classify `pinned:cwd_pinned_workspace` ("physics, not
  policy" per spec C6) — needs an operator-facing note.

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
  Holder/runner and network-setup *mechanics* are documented in `01-workspace-runtime/02`
  and `/04`; this page owns the layered security *analysis* of those boundaries.
- **Sources:** sandbox-provider-docker, sandbox-runtime-namespace-process,
  sandbox-runtime-workspace, sandbox-daemon, sandbox-config.
- **Open questions:** peer isolation is now known to be bridge-port isolation only
  (rtnetlink `isolated(true)` + `mcast_flood(false)`; the nft layer was removed in
  `d3c0538e1` — the empty `netfilter/` dir is a leftover), so the remaining question is
  the egress story for 10.244.0.0/24 (no NAT/forwarding installed by this code);
  official kernel floor (5.8 assert vs `userxattr` ≥ 5.11 vs `lowerdir+` ≥ 6.8 vs gate
  probe as sole authority); support status of `privileged: true`.

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
  in argv. Holder/runner internals (handshake tokens, runner wire protocol, payload
  kinds, setns order) are deep-dived in `01-workspace-runtime/02-namespace-processes.md`;
  this page keeps the daemon-side process framing and cross-references.
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

1. **Deleted spec: partially FOUND.** The squash/remount spec (C1–C6), its test catalog,
   and the remount-rework docs are recoverable from git:
   `git show '0f7d02486^:docs/obsidian/ephemeral-os/implementation_plan/squash/spec.md'`
   (all deleted by `0f7d02486`). Action: import into this repo
   (`01-workspace-runtime/SPEC.md` step 0). Still missing: the §2.x workspace-session
   spec, the C3 file-auditability spec, the observability spec, `ab_driver.py` —
   enumerate the same deleted tree with `git log --diff-filter=D --name-only -- docs/`.
   Affects `00-foundations/03`, `01-workspace-runtime/04`, `01-workspace-runtime/08`,
   `06-config-and-observability/02`, `07-engineering/02`.
2. Streaming/auth-field framing: migrate into sandbox-protocol per the boundary law, or
   document co-ownership as intentional?
3. `LocalSandboxDaemonInstaller` + `manager.local_daemon` config: planned `--backend
   local` or dead scaffolding?
4. Auth-optional gateway (library) and non-loopback binds: supported deployments or
   dev-only? TLS roadmap?
5. Token rotation: is "restart console after gateway restart" permanent?
6. Isolated networking (answered in part by the cluster-01 deep-dive): peer isolation =
   bridge-port isolation set via rtnetlink (`isolated(true)`, `mcast_flood(false)`); nft
   was removed (`d3c0538e1`). Remaining: what provides egress for 10.244.0.0/24 (no
   NAT/forwarding exists in this code)?
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
15. Finalize failure surfacing: a capture error at finalize is recorded only as a span
    attribute (the session's changes are silently lost), and an empty capture with
    non-empty protected drops skips publish so the drops never surface — accepted
    contract or gap? (`01-workspace-runtime/04` and `/07`.)

## Suggested writing order

Cluster 00 first (prerequisites for everything), then cluster 01 in full **in its
internal page order (00 → 08)** — the pages are dependency-ordered so the cluster reads
sequentially; the highest-decay reconstructions are `04-workspace-sessions`,
`05-command-execution`, `07-capture-and-publish`, and `08-squash-and-live-remount`
(write 08 against the recovered spec). Then the remaining P0 pages by cluster order
(02 → 03 → 04 → 05/01 → 06/01), then P1, then P2.

## Source agent reports

The six per-scope exploration reports (with file:line anchors for every key abstraction)
were produced by session agents: ops/adapters `a97eb87037a1bf5b3`, console
`a0cdfa7d9edb12097`, host-mgmt `af79af236a13b1ab0`, daemon `a09d5820264b7b5a2`,
runtime-prims `aa18271ae6c950247`, obs/config/infra `a82389bbc91c60216`.

The cluster-01 restructure is grounded in a second, 8-topic deep-dive (2026-07-11):
layerstack/store `ab285c8232cb4c1b7`, sessions/network `a990922faed3870ce`,
holder/runner `ab090bba22f959521`, command/PTY `a5af6066852642fd4`, squash/remount
`a9d62ea872d7c4782` (found the recoverable spec in git history), file-ops/blame
`ae13e9ab6baa1ae49`, overlay `a822ce778471889bc`, capture/publish `a0e4d0230429e2b72`,
plus a boot/composition pass `a2de128d96c5f5d4a`. Their synthesis and the per-page
writing spec live in `01-workspace-runtime/SPEC.md`.
