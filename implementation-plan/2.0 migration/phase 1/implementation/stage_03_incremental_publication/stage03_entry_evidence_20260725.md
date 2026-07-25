# Stage 03 entry evidence verification

- Gate: `S03-G02`
- Captured at (UTC): `2026-07-24T22:04:16Z`
- Verdict: `PASS`
- Product repository: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox`
- Test repository: `/Users/yifanxu/Ephemeral-AI-Lab/ephemeral-sandbox-test`

This record recomputes the complete retained identities required by Stage 03 §0.5.
No retained file was modified and no earlier result is promoted into a Stage 03
implementation result.

## Immutable v2 product fixtures

| Artifact | Bytes | Recomputed SHA-256 | Expected | Result |
| --- | ---: | --- | --- | --- |
| `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/contract-v2.bin` | 1,289 | `760236a658433c1d385adb7b96db1f1429d74d66b1023e6a6553f8696fb0505f` | same | `PASS` |
| `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/contract-v2.json` | 4,377 | `8e3cee4013021f236630c3c3182a3f40df0b1fc1ca02c210dca28a942a7bfda8` | same | `PASS` |
| `crates/sandbox-runtime/layerstack/tests/fixtures/cas/v2/portable-root-r08-v1.bin` | 61,289 | `dbdca20a50da366b037a9adeecc688bdce32cd4e0840630b31babb6018055c60` | same | `PASS` |

The immutable accepted v2 identities remain:

- tree: `sha256:4d95eff452b4c165ed5bdf5c5b4ef94b54022462570605ee118da011d5a41b5f`
- root: `sha256:601c290ff8e96cdbe4a6b64a2525e9a49dba3e6935b47a311f52fa6ef8c54c53`

## External v2 oracle and live proof

| Artifact | Recomputed SHA-256 | Expected | Result |
| --- | --- | --- | --- |
| `e2e/fixtures/layerstack_phase1/portable-root-v2/expected-contract.json` | `242f5a7f35579753015251a95f92fa22ea80cdbf4de9a4da2f08b83116949980` | same | `PASS` |
| `.e2e-state/observability/20260724T181645.820036Z-96797/runtime.layerstack-phase1.portable-root.feature-off/summary.json` | `c4646eb0b87f9d876077ebd1b11784c9456b6257cbeaaa44dde4638b2390c81d` | same | `PASS` |
| `.e2e-state/observability/20260724T181645.820036Z-96797/runtime.layerstack-phase1.portable-root.feature-off/cleanup.json` | `7494b60e4e20519a9fcc01479ed98a02217b71de98110365306a1175a80a9e1c` | same | `PASS` |

The retained PRC-01 summary still identifies case
`runtime.layerstack-phase1.portable-root.feature-off`, reports a passing pytest call,
records complete cleanup, and pins OCI index
`sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90`
with resolved `linux/arm64/v8` manifest
`sha256:7f622ca8766bccb22f04242ecb6f19f770b2f08827dc4b8c707de5e78a6da7ab`.

## Dependency evidence

| Artifact | Recomputed SHA-256 | Expected | Result |
| --- | --- | --- | --- |
| `.e2e-state/evidence/stage02-entry-20260724T214000+0800-61d7dbc6-f749-4215-b200-bec185c93ae5/dependency-entry-capture-a.json` | `3995bdabcc6f732883ee831189e690a60faa0cf58fe9e2a0be95870278a2b945` | same | `PASS` |
| `.e2e-state/evidence/stage02-entry-20260724T214000+0800-61d7dbc6-f749-4215-b200-bec185c93ae5/dependency-entry-capture-b.json` | `3995bdabcc6f732883ee831189e690a60faa0cf58fe9e2a0be95870278a2b945` | same | `PASS` |
| `.e2e-state/evidence/stage02-final-20260725T034500+0800-c996aa535/dependency-delta.json` | `1c77ccb2048f4c7383b0bbe6b45f5c999a88e79bcd2ef86ac2650d503e52be1d` | same | `PASS` |

Both retained entry captures are byte-identical and report `exact: true`, 16
invocations, 1,143 external packages, 2,179 external package-feature pairs, 116
direct external manifest edges, and zero differences. The final comparison reports
`external_delta_exact: true`, zero external differences, and a passing safe,
standard-library-only `layerstack-core` audit.

## Retained diagnostic benchmark

Successful run: `019f9583-82ff-717e-8247-c1162b0d536e`.

| Artifact | Recomputed SHA-256 | Expected | Result |
| --- | --- | --- | --- |
| `run-manifest.json` | `d9366bbefb84658e7a1b052bcf853523b2ab845debb051515a77f148f7b8526f` | same | `PASS` |
| `summary.json` | `1b7afbcf0cf7aa6b2d4548738633bd2babaaed3bf0192e866d63e5e0fc224a98` | same | `PASS` |
| `report.json` | `03cb754eb2e00282282e262a24a2ffad79d6582c168c40ef51833cf958f4092c` | same | `PASS` |
| `export.json` | `c9a708a6847b19b2fcbce669b2a98327e2a2b55f0c31e8824747e5d9ca95b274` | same | `PASS` |
| `events.ndjson` | `f039fe3bd2a707885503e76dcc73469a0b79dfe27b66ae20635cb010c6dba329` | same | `PASS` |
| `observations.ndjson` | `ba758de52c2621cb3f9979c07b1476c618f047df5e61e4d62de89269bf785eee` | same | `PASS` |

The retained summary still reports run state `completed` and correctness verdict
`pass`.

The earlier failed run `019f956a-3d46-77de-8115-98232c99d4bd` remains retained.
Its `summary.json` recomputes to
`30ac548e633d7ba7cfd6a9d816ab28fd1555cc9c2f21413ad2df0dd206c5aa25`,
matching the Stage 02 handoff.

## Gate conclusion

All mandatory Stage 00–02 artifacts named by Stage 03 §0.5 are present and match
their complete retained sizes and SHA-256 identities. `S03-G02 = PASS`. Fresh Stage
03 v1 regression, dependency captures, product evidence, E2E, and benchmark work
remain separate gates and are not claimed here.
