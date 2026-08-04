# Rewrite source manifest

Status: **CAPTURED INPUT PROVENANCE — 2026-08-03**

The legacy design folder and algorithm workbook were untracked in the owner's
docs worktree (`?? implementation-plan/2.0 migration/system-design/` and
`?? implementation-plan/2.0 migration/pmss_algorithms.md`). Therefore no docs
Git commit identifies their bytes. This manifest makes the rewrite input set
byte-traceable; the original files remain untouched. It does **not** make the
historical Stage 4.6 dirty source, executable, or experiment reproducible.

The captured set contains **68 files**: 18 legacy/design sources, 3 review
inputs, 4 raw Stage 4.6 identity/resource receipts, 2 P4 run-seal files, and 41
pinned-product external-surface sources.

All legacy relative paths below are under
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/`
in the owner's docs worktree.

## Primary rewrite inputs

| Legacy relative path | SHA-256 |
|---|---|
| `system-design/index.md` | `20b754c906bb1e86dbe77f537c284acf5eee4012a1ad0e5a24de18ba68eb79a1` |
| `system-design/system_requirements.md` | `3a51c50b11c134d49fca44d6d0f1c1d4a3c2e0551a42db1710ac35fafc21f598` |
| `system-design/api_methods.md` | `e0c9f10d0e0d340f14ee9789b5a3c0b2eabc019477ef7f37f69b769ef3ec0e9b` |
| `system-design/architecture/overall_architecture.md` | `eabfe6bba0ee4f0e09633df96ef2f35ce885f2abfe30af62f970fbcc4ec493fb` |
| `system-design/architecture/mpla_demonstrations.md` | `d7bbb1440696f7357d21df344c82c4676f2ced1aac87737d9a9ec151e72bc81a` |
| `system-design/components/backend_adapters.md` | `da0eafa31d70b3583d20891f5f4cd42e5164421fcb5bd9181d917ebe87537078` |
| `system-design/components/canonical_state.md` | `bc6fc6c06cd6e4fa4252b02f17124269bd8b0d67716bf32f1172d865aff7dd80` |
| `system-design/components/durable_store.md` | `b8d877d690f0d0b8e994568a70d5fd7cbded3d76fd9c21e0272624dd3590d526` |
| `system-design/components/lifecycle_engine.md` | `24990b987890641bcc33141c1ca98e726432bab6f48e53cf89668f2875e1d198` |
| `system-design/components/workspace_engine.md` | `1bff0e5c873db46eada649f3863dfe4c24b478b429e9fa2ecde8f1645816cab1` |
| `pmss_algorithms.md` | `2bafc7a17a5d3cdc5429ce22064dce8bec8b8217513c43e6fda0fafc395b7028` |

## Supporting legacy refinement records

These seven files were inside the requested `system-design/` folder and informed
the audit, but they do not override the primary legacy-design claims.

| Legacy relative path | SHA-256 |
|---|---|
| `system-design/refine/index.md` | `ccfe1b3f67623a8503d14602ecb27e4cb1099e21d465cb2c13748f2c74dab349` |
| `system-design/refine/phase_1_architecture_review.md` | `6a041fe05e706f8d6f51331bd6be63d609beab242f8e68377fd182bea1156cea` |
| `system-design/refine/phase_2_primary_source_research.md` | `e5c3d88adb3be4ae632d184874473c14e73f513cbe9cb47a9858bb7222e46576` |
| `system-design/refine/phase_3_resource_scale_review.md` | `7860c14a01948bd96a9b5955c77d6a53a67f4111397a00363150b81ec4e57141` |
| `system-design/refine/phase_4_review_handoff.md` | `153ab7eab61203daf6f3ae54f59d2db9cf99aae5c705b96934cc0f7603a11944` |
| `system-design/refine/phase_5_writer_finalization.md` | `f9c26aa2af7bdaf7b9f199d2ae9f727a01a1245de6d1d1d1a49c813441a86f0d` |
| `system-design/refine/phase_6_acceptance_audit.md` | `477353ad298961330aeff3961fc212c86569c05d4229b929f6ffb87df67111a3` |

## Review inputs

| Input absolute path | SHA-256 | Role |
|---|---|---|
| `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/2.0 migration/phase 1/implementation/stage_04_6_ultra_optimization/poc/mpla_poc_benchmark_report.md` | `402f771b47b810a483c3246e2ad7d99add9caf6031cecd988997fcbedf595e9a` | untracked Stage 4.6 benchmark report; its cited product commit does not identify the report bytes |
| `/Users/yifanxu/.codex/visualizations/2026/08/02/019fc2e8-af7b-7120-a9a0-05c9b95d1a82/pmss-harsh-minimal-audit.md` | `6451f10f7a9ea9c68ebe53669f0e76b94e4fe43f22646cb59c00bfc3d0dbdf68` | hostile reduction and evidence audit |
| `/Users/yifanxu/.codex/attachments/d08db571-b688-4b5e-b996-afca2acffb2b/pasted-text-1.txt` | `c7a1b61939e87d48fa30d4d245d0627049ddfc030d3993553a987533135e4d45` | owner task/acceptance context supplied to this drafting task |

## Stage 4.6 receipts and P4 run seal

The four receipts preserve their exact bytes and the identity commitments or
observations recorded inside them. The two P4 seal files preserve and verify a
20-file run-artifact manifest. On 2026-08-03,
`shasum -a 256 -c manifest.sha256` returned success for all 20 entries. This
closes the named run-artifact set, not either run's causal source/build closure.

The P4 source receipt records a tracked-diff size and digest but does not contain
the dirty patch bytes or untracked source bytes. Several individual staged
executables and the storage helper do have recorded digests; what remains absent
is the exact host publication-scorecard executable byte artifact and the
complete transitive source, dependency, toolchain, build-configuration, helper,
and runtime-configuration closure that causally produced the result. A digest
commitment without its committed bytes is not a reconstructible archive. The P1
receipt has the same dirty-source limitation; do not call it a reproducible
dirty-source closure. The shared commit/tree neither closes the missing
provenance nor permits transferring a value between runs.

| Input absolute path | Receipt SHA-256 | Embedded commitment or observation and limit |
|---|---|---|
| `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z/source.json` | `1a00b32319f8c75979e3f0e98fc38f30f1279dcc2d32459d11b2f0fefe954999` | P4 receipt commits to commit `ac5c0686807ab40ee7e4ef3ff0f8488b66292221`; tree `918b4c0fad8ac37c5e2916d10b9b18d44cfeac55`; tracked-diff size `496,505 B`; claimed tracked-diff SHA-256 `1580ae28b40dee88177bfde575e16ffdf6daf2cff21d2007732b8aaaa2f4b132`. Dirty patch bytes, untracked inputs, and a complete causal build/execution closure are absent. |
| `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z/resources.json` | `341728d9709afe1258cc767509f79b620deba70a065059eb4e53335e91d2789b` | P4 publication resource receipt: `max_cgroup_memory_peak_bytes = 7,430,144 B` |
| `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final34b-p1-20260731t014941z/source.json` | `0594c70819fde83f7f7de9e4c0c015bb8b33e49819365c1a777d551d5e33ee43` | P1 receipt commits to commit `ac5c0686807ab40ee7e4ef3ff0f8488b66292221`; tree `918b4c0fad8ac37c5e2916d10b9b18d44cfeac55`; tracked-diff size `74,930 B`; claimed tracked-diff SHA-256 `2bfc4b64f730a6b956f17c1dbd74fa33ef5c7fc1ad5a9bd029a3d1e51913744f`. The receipt does not archive the exact dirty/untracked source or executable and is not a P1 reproducibility closure. |
| `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final34b-p1-20260731t014941z/resources.json` | `2551a5e5a2a022a4f3e52038265aee2701b15977e4566981665d85a6aca67b78` | P1 activation-memory receipt and campaign maximum: `max_cgroup_memory_peak_bytes = 102,543,360 B`; never attribute this value to P4 |
| `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z/manifest.sha256` | `ca38a57d6a93fd268e2f696a78e234bf73f3dccfdf64e1fd6883ae46438bfc96` | P4 manifest naming and hashing 20 pre-seal run artifacts, including `raw-result.json` (`0eb2c221...161f`), `summary.json` (`e3942468...5e5`), `command-ledger.jsonl` (`95a8226d...228`), `source.json`, `resources.json`, and `staged-artifacts.json` (`b0e92575...1b4e`). It is a run-artifact seal, not a source/build archive. |
| `/Users/yifanxu/Ephemeral-AI-Lab/experiment/mpla-poc-20260727/evidence/runs/mpla-final50-p4-20260731t100712z/manifest-verification.json` | `3951cd5e032a98e8ade468053a0a4b54d74a528ceb0fe60ffdadf8528e49fab1` | Post-seal record says `verified: true` and commits to manifest SHA-256 `ca38a57d...fc96`; it is intentionally outside the self-referential manifest. Independent revalidation also passed on 2026-08-03. |

The sealed `staged-artifacts.json` records individual digests for
`mpla-poc-oracle` (`42b5e24c...972a`), `mpla-speed-poc-v1`
(`75f73566...653`), `sandbox-catalog-export` (`cd25eef0...849`), and
`sandbox-runtime-cli` (`a2b65647...4a2`). The sealed raw result records
`/usr/local/libexec/ephemeral-sandbox/mpla-storage-admin-v1` as
`91ee6501...fd0`. These narrow identities must not be described as absent, and
must not be inflated into the missing complete causal closure.

For Phase 0 matched-comparator purposes, the historical classification is
`R_stage46 = INCOMPARABLE`. Comparator eligibility requires either a newly
attested run or reconstruction of the exact dirty source including all
untracked bytes, preserved as a content-addressed source archive or Git bundle
plus dirty/untracked archive, together with dependency lock, toolchain/build
configuration, executable digest, exact fixture, command, environment, and raw
result artifacts.

## Pinned current-product API evidence

These files are from the clean reserved implementation worktree
`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-new-2.0` at branch
`codex/new-2.0-storage-core`. At capture time, `HEAD` and local `origin/main`
were both `e4974d1f9aac702b35e052629cb070c897989352`, and the worktree was clean. The
files below prove the current 8-manager + 10-runtime public catalogs, the
separate 8-name public observability catalog and daemon dispatch, CLI and MCP
projections, the catalog-external daemon `POST /files/list` dispatch, the
daemon HTTP health/forward router and path grammar, the private authenticated
readiness handshake and Docker caller, and the current host-loopback HTTP
exposure. They establish a source-backed minimum external-surface inventory;
they do not prove caller exhaustiveness, future retention, or V2 acceptance.

| Product-relative path | SHA-256 | Evidence note |
|---|---|---|
| `crates/sandbox-operations/catalog/src/manager.rs` | `ca8d526416af7b48a4cc165efa233160fbe4416a0574cbc1cd951a90503965c2` | assembles and routes the public manager catalog |
| `crates/sandbox-operations/catalog/src/manager/management.rs` | `bf747b811676882b4d57d4e2a3a800805bdcae925e029057bdfe6d9bc6d7362c` | declares the exact eight manager operation specs/names |
| `crates/sandbox-operations/catalog/src/runtime.rs` | `1601f93c2ab87947956e10cc56ca5f41fd1a254a681a06e7f26b1a23bba8a13b` | assembles and routes the public runtime catalog |
| `crates/sandbox-operations/catalog/src/runtime/command.rs` | `3ff7de2ccb8d433ed0aebeeedcf11413a7a2b6f5b9ccecf19b82c78f13a710b2` | declares the three public command operation specs/names |
| `crates/sandbox-operations/catalog/src/runtime/file.rs` | `2e5c06f60bc265525ec8f677757c823dbc05c44f4fbfdc5281a68a3f037182f3` | declares the four public file operation specs/names and optional session arguments |
| `crates/sandbox-operations/catalog/src/runtime/workspace_session.rs` | `4f585b3f009d21098490b47447da74e028d95eb37290dea2544fe6d8d18b21f6` | declares the three public workspace-session operation specs/names |
| `crates/sandbox-cli/src/projection/runtime.rs` | `f711843ce52d310b4e82d7c22ee52e71d381e24dc652b78464695f249976c7d8` | projects the runtime catalog into CLI names/arguments while leaving `file_list` outside it |
| `docs/maintainer-architecture.md` | `0694967cde1eb2930573eaa8fa8473263ac46ee03d7ea78ceb21f319d8c02cf8` | documents the current catalog/client/gateway/daemon ownership and transport background |
| `crates/sandbox-operations/catalog/src/internal/runtime.rs` | `ce45686f04739af56c35e06688fb8239dba1347f28a869a1eb0b12e9d68ce38c` | declares the catalog-external internal name `file_list` |
| `crates/sandbox-runtime/operation/src/operations/registry/file_operations.rs` | `0a0bf0e794e131c73f457cc567211efd77aec9b9aa0de2bfd69cfd8441fda726` | dispatches and shapes the internal bounded `file_list` runtime operation |
| `crates/sandbox-daemon/src/http/api.rs` | `1dafee427a440b53301c3bc833c6593e90a150e4953e29c35c155c76ee619f80` | maps daemon HTTP `POST /files/list` to internal `file_list` and defines request/result handling |
| `crates/sandbox-daemon/src/http/router.rs` | `7b0d649973167926b973727ab39a36c12def42dc9791370a2df82e23c54a628a` | routes exact `GET /health`, `/files/list`, and the `/forward/...` path prefix separately |
| `crates/sandbox-daemon/src/rpc/dispatch.rs` | `5f01f2b3f43da07eed05a6855f948b72a1a6961c4c0003f3430a5bbad50c6084` | proves daemon scope validation, private readiness dispatch, eight-operation observability dispatch, runtime fallback, TCP-token behavior, shutdown, admission, and cancellation responses |
| `crates/sandbox-observability/query/src/registry.rs` | `167378203430b06f33879985379f8063f848a8263c495175ba8bfe1011747f67` | registers and dispatches exactly eight sandbox-scoped observability handlers |
| `crates/sandbox-operations/catalog/src/observability.rs` | `f9cec411c5a6708ac03e128ac353ae81e7a58dc6117f543731490eabb91dee3b` | assembles the separate public observability catalog, families, specs, and routes |
| `crates/sandbox-operations/catalog/src/observability/snapshot.rs` | `368adb3b29fdbc8651b649ae3618bf0dd8b28cfc18af16b32668958200bb2697` | declares exact public name `snapshot`, arguments, scope, and routing |
| `crates/sandbox-operations/catalog/src/observability/trace.rs` | `37773deb8df6ccae79ed90910c5a468625be1424a5580beb10bdbe34e240cb92` | declares exact public name `trace`, arguments, scope, and routing |
| `crates/sandbox-operations/catalog/src/observability/events.rs` | `288d326ac87d57d44401c1085b0d643474fec2f33c6b8929b0b1bf6869c7e4fe` | declares exact public name `events`, arguments, scope, and routing |
| `crates/sandbox-operations/catalog/src/observability/cgroup.rs` | `e3e1151b943a804d13fba7d3aac49d9a12e9a3cd3292f9d37032a4087dbd0693` | declares exact public name `cgroup`, arguments, scope, and routing |
| `crates/sandbox-operations/catalog/src/observability/resources.rs` | `2b1a1af237159388291a280a907eabea39adc28cd9beaa6b4d7216ef86557976` | declares exact public name `resources`, arguments, scope, and routing |
| `crates/sandbox-operations/catalog/src/observability/topology.rs` | `f4a0ee9d502ab6f5327a5e51ab240b95ce533d2a37b344491c7bfe37a2770f1a` | declares exact public name `topology`, arguments, scope, and routing |
| `crates/sandbox-operations/catalog/src/observability/daemon.rs` | `942f4acf21ff1eab0d5c9f052ce1a9097e775337cb5e71f58c313b8707c887cf` | declares exact public name `daemon`, arguments, scope, and routing |
| `crates/sandbox-operations/catalog/src/observability/layerstack.rs` | `30e428837b9e9f5df710d315e844fb77d29fbe063fc961dc77d967ea37a20102` | declares exact public name `layerstack`, arguments, scope, and routing |
| `crates/sandbox-cli/src/projection/observability.rs` | `41a56be8147e9c40b59ddcd597668777cf76ffcc106782a1361286acd8e452e0` | projects all eight observability names and arguments into the public observability CLI |
| `crates/sandbox-cli/src/observability.rs` | `d57f7690363fd9b69a7ea69f649cb024f135eb4e318e3489a3841793b73ad7a9` | actual CLI caller loads the observability catalog/projection and sends through gateway endpoint/auth-token configuration |
| `crates/sandbox-mcp/src/config.rs` | `a2729d31d4686d13d054f7bf1915b1f4d2e953171d3c2b37c41252b04d93d79e` | makes `Observability` a selectable fixed MCP operation set and accepts gateway credentials |
| `crates/sandbox-mcp/src/catalog.rs` | `fb60fa1b626b99b8b192928faf5eb88fa1b24324bb53f3cf96c29219c4bb38a4` | selects the observability catalog for that MCP operation set |
| `crates/sandbox-mcp/src/schema.rs` | `8e476badec8874cd0c388b37812df062b2374cca61d1cd6183fb74b2c7a56c17` | projects selected catalog specs into MCP tool definitions and bounded schemas |
| `crates/sandbox-mcp/src/tools.rs` | `b0ef5476214c6cdef149470150fb09c00c49f3ffdec387b0f93f16da7d58d7b1` | validates public catalog routes, builds scoped requests, and dispatches MCP tool calls through the gateway client |
| `crates/sandbox-mcp/src/lib.rs` | `19e7f643e15c37d95a9155c6a61b64ac76a03cd4ecf90f5467b776201695acdb` | wires the fixed-set MCP stdio server to the selected catalog and gateway client |
| `crates/sandbox-mcp/src/server.rs` | `c2b563d5aceeed18da32d82e6f4f1fc869d2df523ada0297b43a87e58fd80ccb` | exposes projected catalog operations through MCP `list_tools` and `call_tool` |
| `crates/sandbox-daemon/src/http/mod.rs` | `306d58d230196f68fa8e895179fabd1e417b201040920310c1814225605e8454` | identifies health, forwarding, and `file_list` as a separate daemon HTTP transport from authenticated JSON-line RPC |
| `crates/sandbox-daemon/src/http/health.rs` | `4d1be2b7893be2e4b18ab6e8fd28c4d7198e03a42a3c17979be442c43d0d3799` | defines bounded `GET /health` liveness/telemetry output without runtime-state or event-storage access |
| `crates/sandbox-daemon/src/http/forward/mod.rs` | `ad21390b575dbcac31aaf147863c5c024fa5f4cefd1bd89efc97367c4c166e48` | parses, resolves, proxies, observes, and maps failures for shared/isolated forward requests |
| `crates/sandbox-daemon/src/http/forward/route.rs` | `dd574c0c6198413afea3dc0b353ff151161c960b1d7b9d82bec36856ee8276e1` | defines exact shared and isolated path-family grammar, target port, workspace selector, and forwarded tail/query |
| `crates/sandbox-daemon/src/http/forward/proxy.rs` | `3e69e6bb06d137f449c3536a7ed6a8886c6abdcd361a933c4dd2badc71d954d6` | defines the HTTP/WebSocket-style pass-through, timeouts, shutdown, and child-task behavior |
| `crates/sandbox-protocol/src/handshake.rs` | `b8ea8d714efac6a1cfc14cd22f269dbfa439f0de089c5dfa43aed2eaaaad72d1` | declares private control name `sandbox_daemon_ready` and encodes its authenticated sandbox-scoped request |
| `crates/sandbox-provider-docker/src/readiness.rs` | `7d3b2b7f9be1daed425031d5151646aaa8c8f783de69e67ddf7459a9667ae18b` | wraps readiness request encoding and validates the exact ready/sandbox-id response |
| `crates/sandbox-provider-docker/src/installer.rs` | `680cd5523f6dd7c984116a0b049b282601617fea90f44a47ffa6a8738ee359d0` | actual Docker caller polls the daemon with the authenticated readiness request and validates the response |
| `crates/sandbox-manager/src/model.rs` | `f6ab7aa376978c8ccbe8c0a7e538433b371c1ed97240620624ec4172fa17c9b1` | distinguishes authenticated daemon RPC endpoint from the published unauthenticated HTTP endpoint |
| `crates/sandbox-provider-docker/src/engine.rs` | `b02c3517a5e9e07a4841c055bf3e27702f28bc6e0a3bcc6508a187516469edc5` | publishes both daemon ports to random host `127.0.0.1` ports, establishing host-loopback reachability |

## Revalidation

Before relying on the rewrite, hash every legacy/review source in its named
worktree, every named receipt and seal file at its absolute path, and every
product source in the pinned implementation worktree. From the P4 run directory,
also run `shasum -a 256 -c manifest.sha256`. A match proves that the listed
input/receipt bytes and sealed run artifacts have not changed; it does not
supply the absent Stage 4.6 dirty patch, untracked source, exact host scorecard
artifact, or complete causal build/run closure. A mismatch means this draft is
no longer traceable to the same input set; review the delta explicitly rather
than updating this manifest silently.
