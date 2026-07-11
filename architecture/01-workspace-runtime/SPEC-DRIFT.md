# SPEC-DRIFT — deviations between `SPEC.md` and the code, plus net-new insights

> Ledger kept while authoring cluster 01 (2026-07-11). Format per entry:
> **spec claim → reality → anchor**. `SPEC.md` recorded one exploration of the
> code; where re-verification found the code saying otherwise, the code won and
> the pages follow the code. Net-new insights (things the spec missed entirely)
> are listed per page after the drift entries. Abbreviations as in SPEC.md
> (`LS/`, `WS/`, `OV/`, `NP/`, `NE/`, `OP/`, `SD/`).

## Step zero — recovered-spec hunt (SPEC §0)

- **Spec claim:** the §2.x workspace-session spec, the C3 file-auditability
  spec, and the observability spec might live somewhere in the deleted
  `docs/` tree → **Reality:** all three found. The "§2.x spec" is
  `implementation_plan/finalize-policy/spec.md` (§2.1–§2.7 + F-rules; §2.3
  admission/completion, §2.5 failure semantics, §2.6 uniformity — matches
  every `§2.x` code cite). The "C3 spec" is `docs/occ_merge_publish/c3_spec.md`
  (§7/§7.1 stores, §9 attribution, §10 event schema, §11/§11.1 blame, §13
  commit path — matches the file-domain cites verbatim). The observability
  spec generation lives under `docs/observability-rework/` (cluster 07's
  concern; enumerated, not imported). → **Anchor:** `recovered/README.md`;
  cites at `OP/file/service/store.rs:1`, `OP/file/audit.rs:1`,
  `OP/file/service/impls/blame.rs:1`,
  `OP/workspace_session/service/impls/admission.rs:17-21`.
- **Note:** `docs/daemon/workspace_migration/operation_service_workspace_session_SPEC.md`
  looks like the §2.x spec by title but is a *predecessor generation* — it
  contains none of the §2.x/F numbering. Imported as
  `recovered/predecessor-workspace-session-spec.md` for history only.
- SPEC §0's numbering-collision warning is confirmed and sharpened: "C3" in
  the file domain = phase C3 of the OCC-merge-publish plan
  (`docs/occ_merge_publish/c3_spec.md`), not remount step C3.

## Page 01 — LayerStack store

Drift (spec claim → reality → anchor):

1. **Layout constants** — spec: "Layout constants `LS/lib.rs:40-46`" (implying
   all of them) → reality: only `layers/`, `staging/`, `manifest.json`,
   `.layer-metadata/` live there; `workspace.json` is at
   `LS/workspace_base/binding.rs:11`, `.storage-writer.lock` at
   `LS/storage/lock.rs:12`, `base/` at `LS/workspace_base/layer.rs:17`
   (re-export `LS/lib.rs:34-38`).
2. **"Synthetic empty v0"** — spec: a missing manifest "reads as a synthetic
   empty v0" → reality: the synthetic manifest has *version counter* 0 but
   **schema_version 1**; no schema v0 exists or can be read
   (`LS/storage/fs.rs:190-192`, `:14-21` serde default, `:200-204` too-new
   reject; `LS/model/mod.rs:82-91`). Pages say "version 0", never "schema v0".
3. **"The three sha256 roles"** — spec counts three → reality: a fourth
   sha256 family exists, the per-path publish `content_fingerprint`
   (`LS/stack/publish/fingerprint.rs:10-28`); page 01 disambiguates and
   page 07 owns it. Also: the base layer's `.digest` sidecar stores the *base
   root hash*, not a changeset digest (`LS/workspace_base/build.rs:102`).
4. **Manifest schema range** — spec: `LS/model/mod.rs:75-97` → reality:
   struct + impl at `:74-97` (schema const at `:10`).
5. **Registry-inside-guard range** — spec: `LS/stack/mod.rs:91-113` →
   reality `:91-114`.
6. **Gate-probe scratch comment** — spec: `OP/services.rs:224-229` → reality:
   comment `:225-227`, scratch join `:228`.
7. **Docker import anchors** — spec: `runtime.rs:239-246,337-341` → reality
   today: volume bind at `:246` and `:339-341`; seed archive call `:256-263`;
   archive content `crates/sandbox-provider-docker/src/archive.rs:48-99`
   (manifest `:59-73`, binding `:75-86`, digest `:88-95`).
8. **Squash allocator anchor** — spec: `LS/stack/squash.rs:150` → reality the
   allocate call spans `:149-150`.
9. **Bind-detach range** — spec: `OP/services.rs:268-316` → reality: function
   `:268-302`, platform impls `:304-311` (linux) / `:313-316` (non-linux).
10. **`get_snapshot` location** — spec: "`LS/service/impls/get_snapshot.rs`"
    with a parenthetical suggesting it might be under `OP/` → reality: it is
    the LS path (`LS/service/impls/get_snapshot.rs:1-11`); `OP/layerstack/
    service/impls/` has no get_snapshot.
11. **Same-day repo drift after the spec's exploration:** commit `468ca8468`
    (2026-07-11 13:42) renamed the observability packages
    (`application→query`, `primitives→telemetry`). Layerstack impact is
    comment-level only, but any spec-era references to
    `sandbox-observability-primitives` are stale; the telemetry reader of the
    `.bytes` sidecar is now
    `crates/sandbox-observability/telemetry/src/collect/layerstack.rs`.
12. **Sweep-width et al. are config now, not constants** — commit `e8ee86607`
    (2026-07-10) introduced `LayerstackRuntimeConfig { remount_sweep_width: 4,
    export_chunk_bytes: 2 MiB, spool_zstd_level: 3 }` injected at
    `OP/services.rs:387-399`. SPEC page-08 phrasing "width default 4" is
    right but it is a *config default*, not a hardcoded constant.
13. **"staging/* wiped" is conditional, not unconditional** — spec: boot sweep
    "B* never deleted; `staging/*` wiped" → reality: all three skip branches
    (missing / unparsable / `version < 1`-or-empty manifest) return **before**
    the staging wipe; `staging/*` is cleared only on the healthy
    parsed-manifest path (`LS/stack/lease/cleanup.rs:85-94` early returns vs
    `:123-130` wipe). Caught by the page-01 adversarial review; the sweep
    doc's "deletes nothing" includes staging.

Net-new insights folded into page 01 (spec missed entirely):

- Layer-id counter is a process-wide `AtomicU64` from zero; cross-restart
  uniqueness rests on a 100-retry existence probe
  (`LS/storage/fs.rs:30-32,41-51,269`).
- Sweep candidates include orphaned **sidecar stems**, not just `layers/*`
  dirs (`LS/stack/lease/cleanup.rs:101-112`); sweep synthesizes `layers/{id}`
  paths, so absolute-path manifest entries are structurally beyond its reach
  (`:116-119`).
- `check_layer_path` validates every manifest read (relative, no `..`/NUL),
  while `resolve_layer_path` would honor an absolute path verbatim — the gate
  is validation, not resolution (`LS/storage/fs.rs:79-111`).
- fsync discipline: publish fsyncs the staging tree file-by-file + dir, then
  atomic-renames (`LS/stack/ops/publish.rs:74-88`); there is **no syncfs at
  publish** — the single `syncfs` barrier belongs to squash commit
  (`LS/storage/fs.rs:155-172`).
- Post-promote OCC recheck under the exclusive lock (defense-in-depth)
  rolls back the layer on manifest drift (`LS/stack/ops/publish.rs:95-103`).
- Head-dedup silently disables itself when the head layer has no `.digest`
  sidecar — which is exactly the S-layer case, pinned by "Test 21"
  (`LS/stack/ops/publish.rs:129-139`;
  `layerstack/tests/unit/squash.rs:1301-1330`).
- No shared→exclusive lock upgrade: a thread holding a shared guard that
  calls `exclusive()` self-deadlocks (`LS/storage/lock.rs:192`).
- `manager.json` persists each session's `lease_id`, but the lease registry
  is never rehydrated — the asymmetry that makes the boot sweep necessary
  (`WS/lifecycle/persistence.rs:23` vs `LS/stack/lease/registry.rs`).
- The file-auditability store deliberately lives *outside* the stack root at
  `<layer_stack_root>/../storage/file_auditability`
  (`OP/services.rs:326-332`).
- A publish failpoint ships in prod code behind
  `SANDBOX_LAYERSTACK_ENABLE_TEST_FAILPOINTS=1` + a consumed marker file
  (`LS/stack/ops/publish.rs:15-16,141-156`).
- `LayerPath::parse` trims whitespace and converts `\` → `/` before
  validating (`LS/model/mod.rs:31-54`).
- Glossary hazards discovered: "snapshot" has three meanings, "scratch root"
  four locations; page 01's Corrections and the tour glossary disambiguate.

## Page 02 — Namespace processes

Drift (spec claim → reality → anchor):

1. **"Why `ns/pid_for_children`, not `ns/pid`, on both sides (`:106`,
   `WS/namespace/mod.rs:45-55`)"** — the spec implies quotable rationale
   comments at both sites → reality: **no such comment exists anywhere**. The
   holder side has only the fork-trick SAFETY comment
   (`NP/holder/namespace.rs:162-165`, "materializes
   `/proc/self/ns/pid_for_children` for the parent holder to pin"); the
   daemon side is bare code (`WS/namespace/mod.rs:51`). The page states the
   mechanical reason itself and says the rationale is unwritten.
2. **"read-to-EOF `SD/runner/mod.rs:150-157`"** — spec presents this as the
   daemon reading the runner result → reality: that range is the **runner
   reading its request** (`read_payload_from_fd`). The daemon drains the
   result at `NE/launcher.rs:343-367` (`drain_result_fd`) / `:431-436`.
3. **"setns order user→mnt→pid→net, user first for capability grant
   (`NP/runner/setns/namespaces.rs:27-36`)"** — order confirmed and
   test-pinned, but the "capability grant" rationale is **not a comment in
   the code** — the range is bare construction. Logged so nobody hunts for a
   nonexistent quote.
4. **Handshake token detail** — `net-ready` is a **prefix** with no trailing
   newline; the rest of the line carries the veth config payload
   (`NP/holder/mod.rs:14-18`, `NP/holder/network.rs:19-35`). Spec's token
   list didn't distinguish.
5. **Exit-code contract quote location** — confirmed at `SD/main.rs:22-30`,
   but the actual holder exit mapping lives in `SD/holder.rs:15-28`
   (CONTROL_CLOSED→1, UNEXPECTED_TOKEN→2).
6. **Mount-mask body location** — spec (page-03 bullet) cites
   `SD/runner/mod.rs:52-93` → reality: `mask_model_shell_paths` lives at
   `NP/runner/mod.rs:53-93`; `SD/runner/mod.rs` only re-loads config and
   dispatches. (Carried forward to page 03's citations.)

Net-new insights folded into page 02:

- **Shared-net sessions' `ready` token is never read.** The daemon waits for
  `ready` only on the isolated path (`expect_line` callers:
  `WS/namespace/holder.rs:69`, `WS/namespace/setns_runner.rs:144`); shared
  holders write it into a pipe nobody reads.
- **PDEATHSIG-before-creds assumption.** PDEATHSIG is armed before unshare +
  uid/gid maps + setuid(0) and never re-armed; the kill tether survives only
  because the single-entry self-map keeps kernel creds unchanged. The pid-ns
  init *does* re-arm post-fork (`NP/holder/mod.rs:132` vs
  `NP/holder/namespace.rs:84-95,189`).
- **Runner exit-code truth**: payload failures ride the JSON
  (`RunResult{exit_code:1,…}` written, process exits 0); process exit 1 only
  for transport/decode/config errors; the daemon synthesizes a result from
  exit status when no valid JSON arrives (`NE/launcher.rs:438-452`).
- **Result fd opened after config load** in the runner — a missing
  `SANDBOX_DAEMON_CONFIG_YAML` kills the runner before any JSON exists
  (`SD/runner/mod.rs:22-26,44-49`).
- **pid-ns init zombie retention**: init's Drop reaps with WNOHANG only; a
  dead init stays zombie inside the pausing holder (`NP/holder/namespace.rs:38-49`).
- **gate-probe is a fourth personality with no pipes/protocol** — fresh
  unshare, exit code = verdict (`NP/gate.rs:25-91`, `SD/gate_probe.rs:13-23`).
- **"personality" is doc-coinage** — code vocabulary is "subcommand" /
  "subprocess bodies" (`SD/main.rs:14-16`, `NP/lib.rs:1-2`).
- **Holder argv/stdio contract**: `ns-holder <readiness_fd> <control_fd>
  <shared|isolated>`; stdout null, stderr piped, tokens go to the readiness
  fd (`SD/holder.rs:7-13`, `WS/namespace/holder.rs:55-64`).
- Same-day drift: `468ca8468` renamed observability imports inside NP/NE
  (`sandbox_observability` → `sandbox_observability_telemetry`).

## Page 03 — Overlay mount

Drift (spec claim → reality → anchor):

1. **"Syscall order with every fsconfig key … `userxattr` (`:132`)"** — the
   spec's phrasing groups userxattr with the SET_STRING keys → reality:
   `userxattr` is `fsconfig_set_flag` (FSCONFIG_SET_FLAG), set *between* the
   lowerdirs and upperdir (`OV/kernel_mount.rs:132`).
2. **"fd-pinned NOFOLLOW lowerdirs (TOCTOU close; `OV/kernel_mount.rs:242-331`)"**
   — reality: **all four roles** (lowerdirs, upperdir, workdir, mountpoint)
   are opened NOFOLLOW and held through `move_mount` (`:243-299,323-331`);
   the asymmetry is which *strings* the kernel receives (fd magic paths for
   lowerdirs vs real paths for the rest). Also no TOCTOU comment exists —
   the intent is carried by the test name only.
3. **Stale-doc anchor** — spec: `OV/kernel_mount.rs:66-69` → reality: the
   quotable stale text is `:67-69` (`:66` is a bare `///`).
4. **Error enum name** — the crate's error is `OverlayError`
   (`OV/lib.rs:31-59`), `#[non_exhaustive]`, four variants; there is no
   `OverlayMountError`.
5. **`allocate_overlay_writable_dirs` range** — spec `OV/lib.rs:71-93` →
   reality: struct `:71-77`, function `:85-93`. Still production-dead
   (only caller = its own test).
6. **Masks bullet (spec cites `SD/runner/mod.rs:52-93`)** — reality:
   `mask_model_shell_paths` lives at `NP/runner/mod.rs:53-93`, and the masks
   are **legacy-API `libc::mount` tmpfs mounts**, not new-API — the "raw new
   API" invariant covers the overlay object only. Config path
   `runner.mount_mask.hidden_paths`, prod `[/eos]` (`config/prd.yml:17-20`).
7. **`NamespaceRuntime::mount_overlay` location** — the method body is in
   `WS/namespace/setns_runner.rs:25-49`, not `WS/namespace/mod.rs`.

Net-new insights folded into page 03:

- **Kernel auto-appends options**: live mountinfo shows
  `redirect_dir=nofollow,uuid=on` added by the kernel, and permanently
  records the dead mounter's dangling `/proc/self/fd/N` strings (today's e2e
  witness `e2e/manager/management/squash/test-reports/squash-20260711-091741/MED-03/witness-mountinfo.txt`).
- Zero lowerdirs is rejected (`"layer_paths must not be empty"`,
  `OV/kernel_mount.rs:247-251`); **no code cap** on count — the kernel's
  ~500 stack limit surfaces as EINVAL, e2e-proven at exactly 500 ok / 501
  fail (`e2e/manager/management/squash/helpers.py:1732-1813`).
- The mountpoint is never created and must not be a symlink
  (`:260,303-320`); upper/work are `create_dir_all`'d (`:272-290`).
- Partial-mount leak is impossible: owned fds drop and the kernel discards a
  never-attached mount (`:126-151`).
- Drop vs `unmount()` asymmetry: Drop peels ≤64 with **no** MNT_DETACH;
  the zero-caller `unmount()` is the only lazy-detach path
  (`:95-103,339-368` vs `:76-81,349-352`).
- `fsmount` uses `MountAttrFlags::empty()` → the overlay is rw.
- Forbidden-char filter = exactly 7 substrings on all four roles, untested
  by unit tests (`:370-381`).
- `/workspace` originates as `DEFAULT_CONTAINER_WORKSPACE_ROOT`
  (`sandbox-config/src/configs/manager.rs:137`) → provider argv
  `--workspace-root` (`sandbox-provider-docker/src/launch.rs:29-30`).
- The magic-path formatter is implemented three times, no shared helper
  (`OV/kernel_mount.rs:334-336`, `NP/runner/setns/remount_overlay.rs:231-233`,
  `NP/gate.rs:176-179`).
- Overlay crate consumers are exactly three (mount runner, remount runner,
  gate probe); the workspace crate never links it.

## Page 04 — Workspace sessions

Drift (spec claim → reality → anchor):

1. **"Create sequence with every rollback edge R1–R6"** — spec assumes six
   edges → reality: **four** (R1 lease release on `open()` error; R2
   `rollback_partial` full teardown; R3 persist-failure un-insert + teardown;
   R4 operation-layer compensating destroy → `CreateRollbackFailed`), plus a
   netlink micro-rollback that frees the pool IP
   (`WS/service/impls/create_workspace.rs:30-36`,
   `WS/lifecycle/create.rs:50-52,109-119`,
   `OP/…/impls/create_workspace_session.rs:42-57`,
   `WS/isolated_network_setup/mod.rs:124-129`).
2. **Finalize machine enum** — spec: "Active→Finalizing→FinalizeFailed
   (`model.rs:53-58`)" → reality: enum is named **`FinalizationState`**
   (doc `:51-52`); there is no Destroyed state — success removes the map
   entry (`destroy_session.rs:61-63`).
3. **Who sets Finalizing** — spec implies finalize does → reality:
   `complete_under_gate` flips Active→Finalizing on the completion edge,
   *then* calls the runner (`admission.rs:214-226`).
4. **"destroy variants"** — the public `destroy_workspace_session` operation
   dispatches to **`guarded_destroy`**
   (`OP/operations/registry/workspace_session_operations.rs:60-68`);
   `destroy_session` is the gate-free low-level path with **no ledger
   check**; the ledger refusal lives only in guarded_destroy.
5. **Gates-map hygiene doc range** — spec `core.rs:74-99` → reality: doc
   `:74-78`, function body `:79-99`.
6. **Admission ranges** — spec `admission.rs:33-112` / `:114-144` → reality:
   token+slot `:15-65`, proof-of-lock doc `:68-76` fn `:77-112`,
   `with_gated_session` doc `:114-121` fn `:122-144`.
7. **NetworkProfile doc range** — spec `WS/model.rs:97-124` → reality: doc +
   enum `:97-114` (`:116-124` is `as_str`). The doc says "host network
   namespace"; "= the container's netns" is deployment inference, flagged as
   such in the page.
8. **rtnetlink bridge-port anchors** — spec `rtnl.rs:10-120` → reality:
   throwaway thread `:10-30`, move-into-ns `:80-93`, port isolation
   `:108-118` (the only fatal netlink step).
9. **Boot reap fn name** — the manager-side fn is `reap_persisted_handles`
   (`WS/lifecycle/persistence.rs:77`); `reap_persisted_sessions` is the
   service wrapper (`WS/service/impls/remount_workspace.rs:98-103`).
10. **No §2.7 citation exists in code** (nor §2.1/§2.2) — the spec's §2.7
    state-lock ceiling lives only in the recovered document.
11. **"exec_command sets KeepAlive when id present"-type readings are
    wrong** — with an id, no policy is touched; `FinalizePolicy` has exactly
    two variants and CLI creates are always `NoOp` (`model.rs:8-16`,
    `workspace_session_operations.rs:47`).

Net-new insights folded into page 04:

- The ledger is `active_commands: BTreeSet<NamespaceExecutionId>` — bare ids,
  in-memory, comment-only vocabulary (`model.rs:66`).
- The F5 silent-no-op trio in admission.rs (`:29-32`, `:146-149`,
  `:166-168`) and the exec-side §2.3 failure-path quote
  (`exec_command.rs:153-155`).
- `FinalizeOutcome` slot lives on `CommandExecValue`, minted per admission
  (`admission.rs:98`, `exec_value.rs:14-29`) — not on the session.
- Resurrected-gate hazard: `entry(id).or_default()` creates gates for dead
  ids; `discard_resurrected_gate` removes only on `Arc::ptr_eq` + absent
  session (`core.rs:58-99`; test `workspace_session.rs:511`).
- Session ids: 24-bit process counter + epoch-nanos hex
  (`WS/lifecycle/leases.rs:4-11`); `created_at`/`last_activity` use a
  process-relative monotonic clock; `last_activity` is write-only.
- manager.json persists the run dir under the key `scratch_dir`
  (`persistence.rs:28`).
- Isolated sessions are de-facto capped at 253 by the in-memory IP pool
  (`mod.rs:23-24,48-58`); no other session cap exists.
- No end-to-end create deadline — only `setup_timeout_s` on two phases.
- `rollback_partial` hardcodes 1.0 s holder grace vs `exit_grace_s` 0.25 s
  elsewhere (`create.rs:50-52`).
- Destroy failure retains the map entry and gate — retryable
  (`destroy_session.rs:72`).
- Cgroup leaf `workspace-<id>` create/remove is best-effort at OP layer
  (`core.rs:159-172`, `destroy_session.rs:65-67`).
- Test gaps: `CreateRollbackFailed` untested; parked-lease release on destroy
  unit-untested; rfc1918-deny rejection untested.

## Page 05 — Command execution & PTY

Drift (spec claim → reality → anchor):

1. **"`is_kill_input` … (write_command_stdin.rs:6-74)"** — the mechanism is
   confirmed but there is **no doc comment** on it; the page quotes the
   3-line function itself (`:72-74`). Nearest prose is the catalog
   description ("stays terminable through write_command_stdin (Ctrl-C or
   Ctrl-D)", `sandbox-operations/catalog/src/runtime/command.rs:35`).
2. **"512-entry terminal eviction (`NE/registry.rs:86-112`)"** — eviction
   logic confirmed, but 512 is a **caps/config default**
   (`max_terminal_entries`, `NE/caps.rs:28`,
   `sandbox-config/src/configs/runtime.rs:309-311`), not a registry
   constant; there is no `MAX_TERMINAL_ENTRIES` identifier.
3. **Exit-code table refinement** — the 128 fallback is **runner-side only**
   (`NP/runner/shell_exec/wait.rs:148`); the launcher's synthesis fallback is
   **1**, and exit-0-without-envelope is a `Completion` error
   (`NE/launcher.rs:438-452`).
4. **Status vocabulary** — terminal statuses are `ok/error/timed_out/
   cancelled` (+`running`), not completed/failed
   (`OP/command/service/dto.rs:27-46`, `NE/shell.rs:9-15`).
5. **"read_command_lines.rs:58-67 returns ok+empty"** — confirmed, and the
   fabrication is reached via `:17-22` (`unwrap_or_else(empty_terminal_output)`).
6. **`NamespaceExecutionError::Timeout` never constructed** — confirmed; the
   only `::Timeout` hits elsewhere are a different type
   (`SD/http/forward/proxy.rs`).
7. **"C6 PTY physics"** — the literals "C6" and "PTY physics" appear nowhere
   in command-path code; C-rule numbering in code is only C1/C3/C4/C5
   (quiesce/remount/file-audit). C6 lives in the recovered squash spec only.

Net-new insights folded into page 05:

- **Terminal yields never advance the streaming cursor** — idempotent
  re-reads; only running yields advance it (`yield.rs:54-56` vs `:78-95`).
- **Ctrl-D (EOT) is a cancel, not an EOF** — same containment test as ETX;
  kill-input against a finished command errors (`CommandAlreadyCompleted`).
- **`write_command_stdin` takes no session gate** (engine-value path only);
  its kill branch waits a hardcoded 1000 ms yield window.
- **No timeout ⇒ runs forever**: `timeout_ms` is request-only, no config
  default; the shell-mode `wait_completion` is an untimed `child.wait()`;
  `setup_timeout_s` applies only to mount/file-op/remount runners
  (`exec_command.rs:80`, `wait.rs:136-140`, `NE/launcher.rs:159,299-312`).
- **Watcher terminal order is load-bearing**: on_terminal (span) → finalize
  (token drop) → registry.complete → promise.resolve
  (`NE/engine.rs:248-273`); evicted values are dropped **outside** the
  registry lock because Drop does fs I/O (`registry.rs:92-112`).
- **Trace handoff is three spans**: sync `command.exec`; parked async
  `namespace.exec.run_shell` finished by the watcher's terminal hook; and
  `namespace.runner.spawn_child` written by the **runner child** itself via
  `observability_log_path` (`exec_command.rs:27,105-111`,
  `NE/engine.rs:325-353`, `NP/runner/shell_exec.rs:114-136`).
- **Transcript sink is fire-and-forget**: no fsync; a write error silently
  drops the sink (`NE/pty.rs:127-133`).
- **id == request_id** (`namespace_execution_{n}`; `NE/engine.rs:58-61,342`).
- **Backpressure error text**: "stdin_backpressure: consumer is not draining
  its stdin", 2 s deadline (`NE/pty.rs:78-106,207-212`; `NE/caps.rs:27`).
- **Caps became config on 2026-07-10** (`c02181c39`): `ExecutionCaps`
  injected from `runtime.{command,namespace_execution}`;
  `COMMAND_ENGINE_SETUP_TIMEOUT_S` deleted (now
  `runtime.workspace.setup_timeout_s`, `OP/services.rs:107`);
  `DEFAULT_FREEZE_BUDGET` deleted (now `ResourceCaps.freeze_budget_s`).
- **Cgroup e2e gap**: placement is unit-pinned only
  (`operation/tests/exec_command.rs:540`); no e2e exercises cgroup
  placement.

## Page 06 — File operations & blame

Drift (spec claim → reality → anchor):

1. **Handoff edge #7 anchor** — spec: "sessionless writes via `amend_path`
   (`LS/stack/projection/mod.rs:129-229`)" → reality: that range is
   `MergedView::{read_classified, list_dir}`; **`amend_path` lives at
   `LS/stack/file_read.rs:75-131`** (with the "nothing to retry" doc at
   `:1-7`). The OP-side owner-taking wrapper is
   `OP/layerstack/service/impls/amend.rs:21-51`.
2. **"session edit = two separately-gated runner ops"** — confirmed, and
   sharpened: `ReadFile` (≤ max_edit_bytes) → in-process `apply_edits` →
   `Write`, each via `with_gated_session` separately
   (`OP/file/service/impls/edit.rs:43-78`).
3. **run_file_op quote range** — spec `:13-14` → reality the doc is `:9-14`.
4. **"no-op commits record no blame (`LS/stack/file_read.rs:113-124`)"** —
   the behavior is real but that range has no literal comment; the quotable
   doc is `LS/stack/publish/model.rs:55-56` ("Empty when the publish was a
   no-op…").
5. **Limits refinement** — read limit is dispatch-hardcoded
   `READ_LIMIT_MAX = 2000` independent of config
   (`OP/operations/registry/file_operations.rs:18,153-154`); session write
   content has **no per-op cap** (transport-bounded only); sessionless
   overwrite uses classify-only read (`max_bytes 0`) so an over-4-MiB file
   can still be overwritten (`write.rs:74`).
6. **§15 exists** — the C3-spec § citations in code/tests also include §15
   (`operation/tests/file_blame.rs:1`), beyond the §7/§9/§10/§11/§13 set
   SPEC listed.

Net-new insights folded into page 06:

- **Deletes append no audit event** — blame survives `rm`
  (`LS/stack/publish/resolve.rs:52-77`; e2e
  `test_blame_survives_deletion`).
- **The audit store never rotates** — only `file_auditability_0.ndjson` is
  written; lexical segment sort is a latent multi-digit trap; eager boot
  replay panics the daemon on open failure (`store.rs:18,98-141,164`,
  `OP/services.rs:49-52`).
- **Events carry no timestamp/request-id/line content** — owners +
  `content_digest` only; ordering is append order under `audit_gate`.
- **`default_owner` is a compression artifact** (most-covering owner), not
  "the publisher" (`OP/file/audit.rs:118-149`).
- **`Origin::Active` is 0-based; audit lines are 1-based** — conversion at
  `audit.rs:67`.
- **A missing `content` arg silently writes an empty file** — catalog says
  required, dispatch uses `optional_string(...).unwrap_or_default()`
  (`file_operations.rs:167`).
- **Error-kind asymmetry**: blame path errors are `not_found`; read/write/
  edit path errors are `invalid_request` (`file_operations.rs:50-67`).
- **HTTP `files/list` is unauthenticated loopback** (`SD/http/server.rs:1-3`,
  `rpc/runtime.rs:30`); the manager RPC route refuses file_list
  (`sandbox-manager/src/router/dispatch.rs:27-32`).
- **Parity by copy**: window/normalize/split helpers duplicated verbatim in
  `OP/layerstack/service/impls/read.rs:119-162` and
  `NP/runner/setns/file_op.rs:405-448`.
- **Session write preserves mode** (`st_mode & 0o7777`, else 0644) via tmp +
  `fchmod` + rename + parent fsync (`NP/runner/setns/file_op.rs:165-209`).
- Test gaps: no dedicated audit-store unit suite (replay covered via blame
  fixtures); no LS-level `amend_path` unit test (covered via OP tests/e2e);
  no NP unit tests for the file-op runner body (NOFOLLOW pinned at e2e).

## Page 07 — Capture & publish

Drift (spec claim → reality → anchor):

1. **Entry-kind table range** — spec: `WS/overlay/capture.rs:190-222,332-349`
   → reality: file-entry classification `:190-222`; **OpaqueDir emission
   lives in the directory walk** (`:171-177,234-242`); whiteout/opaque
   detection `:332-349`.
2. **Resolve module doc range** — spec `resolve.rs:1-6` → reality `:1-5`
   (line 6 blank); all-resolved-or-one-reject at `:39` confirmed
   (doc `:37-39`).
3. **Capture-drop ranges** — spec `capture.rs:215-304` → reality drops split
   `:215-220` (special files) + `:267-304` (invalid layer paths); a
   non-UTF-8 **symlink target** is a hard `CaptureError`, not a drop
   (`:244-254,314-321`).
4. **`MERGE_MAX_BYTES` is duplicated** — `merge.rs:13` *and* `resolve.rs:24`
   (spec cited only merge.rs).
5. **"route" is two-valued** — `RouteKind { Source, Ignored }`
   (`route.rs:5-9`); "protected" is a reject, not a route — the spec's
   "capture→plan→resolve→route→write" figure phrasing folds route into plan.
6. **Base-revision checks are self-consistency, not freshness** — both the
   OP precheck (`publish_changes.rs:16-21`) and plan's
   `validate_base_revision` (`plan.rs:104-127`) compare the request against
   itself; head movement is adjudicated only by per-path fingerprints. The
   page states this plainly per the spec's "this, not the manifest recheck,
   is the OCC" instruction.
7. **Two `InvalidBaseRevision`s** — the OP-level error maps to wire class
   `publish_error`, not `invalid_base_revision` (`finalize_session.rs:150`).
8. **Export "spec decision 19" post-dates the code** — the token-gated HTTP
   export stream landed 2026-07-08 (`39f80668c`) and was **removed
   2026-07-10** (`2ee1b4240`: deleted `SD/http/export.rs`, stripped
   `stream_token`, deleted `EXPORT_STREAM_TOKEN_FIELD`); the tree is back to
   `read_export_chunk` paging with EOF-unlink. The recovered export spec
   records decision 19 as current — code wins.

Net-new insights folded into page 07:

- **Publish keeps net-nothing whiteouts** — a whiteout over an
  upperdir-only path fingerprints Absent-vs-Absent, passes resolve, and is
  persisted; net-effect folding is squash's job
  (`plan.rs:135-141`, `resolve.rs:108-111`, `write.rs:41-44`).
- **Clean writes still run the merge** (`three_way_merge(base, base,
  command)`) purely for diff-based origin (`resolve.rs:161-180`).
- **Myers budget** `MYERS_MAX_D = 200_000` degrades to whole-file
  delete+insert — attribution coarsens, no error (`merge.rs:252,307-322`).
- **Merge eligibility = ≤8 MiB ∧ no NUL ∧ valid UTF-8** (`merge.rs:162-164`).
- **created:false has exactly two causes** (empty resolved changeset;
  head-digest dedup), and both discard origin before audit — idempotent
  republish mints no blame (`ops/publish.rs:33-46,60-66`).
- **Modes are never captured** (`WriteFile` has no mode field); clean copies
  keep bits incidentally via `fs::copy`, merged files lose them via
  `fs::write` (`LS/model/mod.rs:176-180`, `write.rs:15-40`).
- **Capture walk has no entry cap** — the 50k limit belongs to
  `TreeResourceStats`, a different path (`WS/overlay/tree.rs:3`).
- **Gitignore sealed-by-parent rule** — negation cannot rescue descendants
  of an ignored dir (`gitignore.rs:75-87`); `.git` routes as ordinary
  source since `98b9a73a2`.
- **Export singleflight** per storage root via a process-global AtomicBool
  map; spool naming `exp-<pid>-<counter>.tar.zst`; registry is in-memory so
  spools orphan on restart until the boot wipe (`export.rs:256-298`,
  `OP/services.rs:147-161`).
- **WriteFile TOCTOU guard is untested** — the "spool payload changed before
  publish" string appears only in src (`write.rs:26-39`).
- The WS→LS boundary DTO carries **references, not bytes** — `WriteFile
  { source_path into the live upperdir }`; publish streams content at
  commit (`WS/model.rs:434-445`, `capture.rs:84-92,102-105`).

## Page 00 — Runtime tour

The tour introduces no independent runtime claims; it reconciles and links the
contracts owned by pages 01–08. One planning inconsistency was resolved while
writing it:

- **One page per demo step** — the page's done condition requires each demo
  step to name exactly one detail page, while the recovered sample grouped
  pages 02–04 and pages 06–07 into single steps. The written tour uses nine
  steps, one for each page in reading order.

## Page 08 — Squash & live remount

Drift (spec claim → reality → anchor):

1. **The runtime boot latch has two checks, not three bits** — the probe
   combines G1 (overlayfs) and G2 (writable cgroup v2); G3 is the separate
   boot-cleanup-before-serving invariant exercised by service order and E2E
   (`NP/gate.rs:1-15`, `OP/services.rs:163-240`).
2. **C5 persists after the sweep** — the recovered order says refresh/persist,
   resume, then release. The implementation resumes the task, releases OLD,
   updates the in-memory session, and performs one batched handle persist after
   every worker completes (`WS/lifecycle/remount.rs:115-194,276-294`,
   `OP/layerstack/service/impls/squash.rs:65-78`). This is ordering drift, but it preserves
   the safety rule that OLD is detached before deletion.
3. **Sweep width is configuration, not a fixed constant** —
   `runtime.layerstack.remount_sweep_width` supplies the bound; both the
   config and operation fallbacks default to 4
   (`sandbox-config/src/configs/runtime.rs:132-149`,
   `OP/services.rs:384-400`). The benchmark template's substituted `8` is a
   test arm, not the product default.
4. **`runner_pids` is a dormant hook** — production constructs remount inputs
   with an empty vector, so the pidfd runner-quiescence branch is not currently
   exercised by live squash (`WS/lifecycle/remount.rs:232-239`).
5. **Lease rewriting has two low-level outcomes** — the store returns
   `Identity` or `Replaced`; the parked state is produced later by C5 as
   `RemountOutcome::Leased` with `parked_lease_id`, not by a third rewrite
   variant (`LS/stack/lease/rewrite.rs:35-39`,
   `WS/lifecycle/remount.rs:313-379`).
6. **Gate and contract labels collide across domains** — boot G1–G3 and
   remount C3 are unrelated to the file-operation G1–G3/C3 labels used in
   page 06. Page 08 qualifies every label by domain.

Net-new insights folded into page 08:

- A helper report with `first_move=true` and `mount_verified=true` is still
  faulty if its detail is not the exact success token; both flags alone are
  insufficient (`WS/lifecycle/remount.rs:326-379`).
- A missing report is clean only when the workspace mount ID is readable and
  unchanged; a changed, absent, or unreadable mount ID is faulty.
- Strict rollback treats a non-`EBUSY` unmount result after verified success as
  an arbitrary detail, which C5 deliberately classifies as faulty.
- Replacement cleanup accepts `release_lease(OLD) == Ok(false)` as migrated;
  `released_old_lease` merely records whether a row was actually removed.
- Faulty sessions are destroyed only after all bounded workers finish, so the
  sweep has a global classification barrier before destructive cleanup.
