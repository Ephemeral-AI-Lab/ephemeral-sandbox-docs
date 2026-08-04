# Phase 02 — Version identity — Test & performance

**Status:** authorized by Phase 01.5 `PASS`; not started  
**Closure trace:** `019fcd32-b832-7750-9eb5-5f544e39c533`

## Exit rule

```text
PASS if I1–I7 pass: deterministic bounded identity, exact-comparison support,
no runtime brands, and no acceptance authority.
```

## Functional checks

| ID | Check | Must? |
|----|-------|:-----:|
| I1 | Same facts → same canonical bytes → same `VersionId` | yes |
| I2 | Order-of-enumeration does not change `VersionId` (if applicable) | yes |
| I3 | Corrupt input rejected | yes |
| I4 | Over-limit input rejected | yes |
| I5 | Forced equal candidate ID + different full canonical bytes → inequality evidence for Phase 03 collision rejection | yes |
| I6 | No docker/overlay/host-path fields in identity | yes |
| I7 | Raw `VersionId` cannot construct `AcceptedVersion`/`AcceptedBinding` through identity APIs | yes |

## Crash / fault

Not required beyond pure function tests (no durable store yet).

## Not testing yet

- Disk commit  
- Multi-process recover  
- COW payload accounting (store phase)  

## Performance

| Question | Answer |
|----------|--------|
| Measure? | Optional microbench of encode/hash only |
| MUST gate? | No — correctness first |
| Bounds | Document decoder CPU/memory limits as code constants + tests |

## Pass / fail

- **Pass:** I1–I7 green.  
- **Fail:** flaky `VersionId`s, identity types carry runtime brands, or identity can assert durable acceptance.

---

[PRD.md](PRD.md) · [PLAN.md](PLAN.md)
