# Phase 05 — Migrator — Test & performance

## Exit rule

```text
PASS if import + fence Must checks pass in lab on fixtures.
```

## Functional checks

| ID | Check | Must? |
|----|-------|:-----:|
| M1 | Fixture legacy → V2 map is total for in-scope roots | yes |
| M2 | Re-import idempotent or explicitly documented | yes |
| M3 | Corrupt legacy rejected; no partial authoritative V2 head | yes |
| M4 | Shadow compare finds expected matches / known diffs | yes |
| M5 | Stale generation writer rejected | yes |
| M6 | Migrator code has clear deletion notes | yes |
| M7 | Equal complete legacy views converge to one Accepted Version/physical payload | yes |
| M8 | Layer IDs/parents/depth/whiteouts and runtime-private paths do not enter Version identity | yes |
| M9 | Importer uses LayerStack-0 APIs only; no direct V2 path writes or alternate format | yes |
| M10 | V2 namespace/layout cannot alias e497 legacy paths during coexistence | yes |
| M11 | Migration progress cannot be interpreted as a Checkpoint, Root, Head, or second truth | yes |

## Crash / fault

| ID | Check | Must? |
|----|-------|:-----:|
| MC1 | Kill mid-import → safe retry or clean fail | yes |
| MC2 | Fence available after restart in lab | yes |

## Not testing yet

- Real multi-node fleet barrier  
- Production observation  
- Stage 4.6 comparison; it is `INCOMPARABLE` and cannot be a ship gate  

## Performance

| Item | Stance |
|------|--------|
| Import time / disk | TARGET — record for capacity planning |
| Steady-state after import | not this phase’s ship gate |
| Separate accounting | import cost **≠** reference fork cost |
| Reference-only EphCoW | Phase 03/06 MUST show zero payload I/O; import measurements cannot substitute for it |

## Pass / fail

- **Pass:** M1–M11, MC1–MC2 green.  
- **Fail:** silent partial import or fence bypass.

---

[PRD.md](PRD.md) · [PLAN.md](PLAN.md)
