Implement the EphemeralOS benchmark migration. First read the authority:

`/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-docs/implementation-plan/benchmark_test/python-benchmark-migration-spec.md`

Source: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox/benchmark`
Target: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test/benchmark`
Product: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`

Implement the migration completely. Inspect relevant code before each phase; do not line-port Rust. Preserve behavior, safety, artifacts, statistics, APIs, and web workflows.

Hard constraints:

1. Target code is Python backend plus TS/JS web only: no `.rs`, Cargo, FFI/PyO3, or benchmark-owned Rust binaries.
2. No benchmark command, test, or Node launcher may run Cargo/Rust tooling.
3. Python must not import product packages, add the product to `sys.path`, parse Rust source, or depend on product crates.
4. Product access uses explicit canonical roots, prebuilt binaries, `sandbox-catalog-export`, and authenticated gateway JSONL.
5. Time raw `asyncio` sockets with `time.monotonic_ns()`. Exclude startup, fixtures, verification, reports, and cleanup.
6. Use FastAPI, Uvicorn, Pydantic, and pytest. Pytest verifies the app; it is not the campaign scheduler.
7. Move the React/TypeScript web app. Keep Vitest, Playwright, `/api/v1`, SSE, nonce security, reports, artifacts, cancellation, and Quick Smoke.
8. All mutation stays under `<TEST_REPOSITORY_ROOT>/.benchmark-state`; source is read-only. Enforce exact ownership markers and safe deletion.
9. Read historical Rust-produced artifacts. Increment schemas for incompatible changes; never reuse an incompatible version.
10. Correctness, infrastructure, teardown, or cleanup failure prevents completion.
11. Preserve unrelated user changes; never restore, overwrite, or delete them.

Phases:

- Freeze sanitized golden fixtures for all public schemas, statistics, reports, comparison, and recovery.
- Create the Python project, roots, ownership/safety helpers, strict models, and a pytest guard rejecting Rust, Cargo, and product coupling.
- Implement compatibility readers, atomic artifacts, journals, recovery, statistics, reports, exports, and comparison against golden fixtures.
- Implement catalog consumption, isolated gateway lifecycle using prebuilt binaries, raw authenticated transport, resource tracking, redaction, and aggregated cleanup.
- Implement deterministic planning and one complete Quick Smoke slice. Add each operation individually, proving setup, timing, verification, teardown, artifacts, and reports.
- Implement FastAPI routes/SSE, move the web app, and replace Rust launch assumptions with Python.
- Run parity and live proof. Remove the product Cargo member and old benchmark tree only after the external implementation is committed and verified.

Testing:

- Run focused offline pytest after each Python change; run Vitest and fixture Playwright after web changes.
- Use fake processes/sockets for failures before Docker. Run live Docker tests feature-by-feature; avoid rerunning passing expensive suites until final proof.
- Cover cancellation, transport/gateway failure, cleanup, recovery, journal corruption, path escapes, secret redaction, SSE resume, and historical artifacts.
- Run the zero-Rust/no-Cargo/no-product-import guard every phase.

Do not add a database, queue, ORM, plugin framework, generated client, distributed runner, NumPy, or a second runner without measured need. CLI and API call one runner.

Maintain a checklist. After each phase report files changed, commands/results, gaps, and spec deviations. Do not claim completion with skipped tests, unproved cleanup, incompatible schemas, Rust-launching web code, or duplicate source. Stop before destructive cutover if parity or live proof fails; retain evidence and fix the root cause.
