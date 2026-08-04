# Phase 03 — LayerStack-0 durable storage — Test & performance

## Exit rule

```text
PASS if Must functional + crash checks are green.
Perf items marked TARGET do not block ship of this phase unless marked MUST.
```

## Functional checks

| ID | Check | Must? |
|----|-------|:-----:|
| F1 | Publish then read back the same `VersionId` and complete facts | yes |
| F2 | Stale OCC publish conflicts cleanly | yes |
| F3 | `CreateHeadIfAbsent(Expected::Absent)`: exact create/retry/conflict behavior and payload bytes read = written = copied = 0 | yes |
| F4 | `ReplaceHead(Expected::Exact(expected_head))`: exact stale behavior, Branch move/rollback mapping, and payload bytes read = written = copied = 0 | yes |
| F5 | `RemoveHead(Expected::Exact(expected_head))`: exact absent/stale behavior and payload bytes read = written = copied = 0 | yes |
| F6 | `CreateFixedRootIfAbsent(root_kind, Expected::Absent)`: Checkpoint creation is fixed, rejects generic retarget, and has payload bytes read = written = copied = 0 | yes |
| F7 | `RemoveFixedRoot(Expected::Exact(expected_root))`: exact absent/stale behavior and payload bytes read = written = copied = 0 | yes |
| F8 | Every accepted-reference operation distinguishes `APPLIED`, `ALREADY_EXISTS`, `NOT_FOUND`, `CONFLICT`, `INVALID_BINDING`, `CORRUPT`, `OUTCOME_UNKNOWN`, and `INTERNAL_FAILURE`; lost responses use authoritative read-back | yes |
| F9 | N Heads/fixed Roots → one physical payload for the same Accepted Version | yes |
| F10 | Collision unequal bytes → reject, no alias | yes |
| F11 | Layer-depth reconstruction not used as truth | yes |
| F12 | Selected V2 physical namespace/layout cannot alias any legacy e497 path during coexistence | yes |

## Crash / fault checks

| ID | Check | Must? |
|----|-------|:-----:|
| C1 | Kill mid-publish → prior or complete new; never mixed | yes |
| C2 | Restart recovers durable Head | yes |
| C3 | Exact Head/fixed-Root removal and last-reference retirement races retain reachable or custodied payload and bound cleanup debt | yes |
| C4 | Cancel/timeout and lost-response paths free scratch/FDs or leave bounded recognizable debt; authoritative read-back resolves `OUTCOME_UNKNOWN` | yes |

## Not testing yet

- Full `file_edit` through HTTP/CLI  
- Live multi-machine fence  
- Matched fleet observation  

## Performance

| Item | Stance |
|------|--------|
| Quantitative optimization target | `OPEN: OPTIMIZATION_TARGET_NOT_QUANTIFIED`; final performance verdict is `TARGET_UNSELECTED` until owner-approved workload, statistic, threshold, and comparison exist |
| Accepted-reference cost | **MUST correctness property:** selected payload bytes read = written = copied = 0 for all five operations; measure metadata, coordination, fence, and any separately invoked backend materialization work without converting it into a benchmark win |
| Compare to Stage 4.6 | `INCOMPARABLE`; record separately if useful, never use as a winner or pass baseline |
| Complexity notes | Document as implemented: publish, lookup, recover (best/expected/worst when known) |
| Memory | Stay within proposed envelopes from phase 00 or document variance |

### What to record when measuring

- Cold vs warm  
- Fixture size class  
- Raw samples path  
- Machine/OS note  

## Pass / fail

- **Pass:** all Must F* and C* green.  
- **Fail:** hidden payload I/O on a reference-only path, or mixed Version/reference truth after crash.

---

[PRD.md](PRD.md) · [PLAN.md](PLAN.md)
