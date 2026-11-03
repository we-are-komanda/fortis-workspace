# FRC-07 frontend evidence

Checkpoint: 2026-09-21, working changes after accepted frontend `e49253b`. The checks below prove their stated boundaries. **The real FRC-07 UI → API → PostgreSQL gate is pending with the coordinator.** Synthetic fetch/browser fixtures do not prove a database transaction, source authorization or production behavior.

## Observed checks

| Check | Observed result | Evidence and limit |
|---|---|---|
| Focused pure/store/save/recovery | **61 passed, 0 failed, 0 skipped**, exit 0 | Frontend owner reran the exact command below after the final source changes and again during this documentation checkpoint. Six budget projection tests + thirteen budget store tests + thirty-four accepted FRC-06 save tests + eight recovery-storage tests. Output was inspected directly in the task tool result; no separate raw focused log is claimed. |
| TypeScript | **PASS**, exit 0 | Owner ran `rtk proxy npx tsc --noEmit` in `frontend/` after final production changes. Independent frozen-snapshot [command](verification-logs/frontend-frozen-types.command.json) and [log](verification-logs/frontend-frozen-types.log) are also available. |
| Owned changed-file ESLint | **PASS**, exit 0, no warnings | Owner ran `rtk proxy npx eslint` with the exact 17 paths in [frontend-changed-files.md](frontend-changed-files.md). Independent frozen-snapshot lint additionally covers 21 implementation/reviewer/coordinator paths: [command](verification-logs/frontend-frozen-changed-lint.command.json), [log](verification-logs/frontend-frozen-changed-lint.log). |
| Independent rendered FRC-07 | **17 passed, 0 failed, 0 skipped** | Coordinator executed the reviewer's actual rendered components/stores with synthetic transport; frontend owner inspected [final raw log](verification-logs/browser-final-17-green.log). It proves UI behavior, not PostgreSQL. |
| Combined rendered regressions | **56 passed, 0 failed, 0 skipped** | Coordinator execution, raw output inspected at [/private/tmp/frc07-browser-regressions.log](/private/tmp/frc07-browser-regressions.log). Includes all 17 budget cases and relevant prior release browser regressions. This temporary log is not presented as a durable repository artifact. |
| Isolated production build | **PASS**, coordinator-reported exit 0; successful output inspected | [/private/tmp/frc07-production-build.log](/private/tmp/frc07-production-build.log) identifies Next.js **16.2.11**, successful compilation, TypeScript and route generation. [Source hashes](verification-logs/build-source-hashes.json) identify the copied snapshot. The log contains Node's `module.register()` deprecation warning; it is not a warning-free claim. |
| Full frontend suite | **232 pass, 6 fail, 76 skip**, exit 1; baseline review pending | Inspected [log](verification-logs/frontend-full.log) and [exact 89-file command](verification-logs/frontend-full.command.json). Reviewer is comparing all six failures against the historical signatures. This row is deliberately not labeled full-suite PASS. |
| Real budget integration | **PENDING** | Coordinator owns ordinary authenticated UI → real API → disposable PostgreSQL execution and final evidence. No real-gate success is inferred from any synthetic test above. |

Focused command, from `frontend/`:

```sh
rtk proxy node --import tsx --test src/shared/lib/budget-projection.test.ts src/modules/drone-defense/domain/project-budget.release.test.ts src/modules/drone-defense/domain/project-save.release.test.ts src/shared/lib/project-draft-storage.test.ts
```

The current full-suite failures name `catalog-sidebar-motion-contract.test.mjs`, `map-zoom-controls-contract.test.mjs`, `prototype-3d-placeholder-contract.test.mjs`, `retrospective-analysis-navigation-contract.test.mjs`, `user-facing-copy-contract.test.ts`, and `defense-project.test.ts`. Matching filenames alone is insufficient for baseline attribution; the independent reviewer owns exact signature comparison. Skipped browser tests in that command are not counted as browser passes; the separate Chromium execution above supplies browser evidence.

## Focused behavior coverage

| Source | Checks |
|---|---|
| [budget-projection.test.ts](../../../../frontend/src/shared/lib/budget-projection.test.ts) — 6 | Equality versus one minor over; zero versus unlimited; unknown remains null; saved-baseline overage and stricter copy; exact large decimal input and signed remaining; malformed/stale pinned projection and check responses; unlimited remaining copy. |
| [project-budget.release.test.ts](../../../../frontend/src/modules/drone-defense/domain/project-budget.release.test.ts) — 13 | Shared mutation rejection preserves project; catalogue preview retained; catalogue removal failure propagated; canonical budget acknowledgement preserves concurrent edit; 422 makes one request and retains draft; ambiguous unchanged revision verifies before manual retry; lost committed receipt needs no second write; divergent verification conflicts; late identity reply ignored; source/body/key frozen on copy; new workspace request omits source; pending budget cannot be replaced by create; interrupted restored budget requires verification. |
| [project-save.release.test.ts](../../../../frontend/src/modules/drone-defense/domain/project-save.release.test.ts) — 34 | Previously accepted save/recovery identity, version, persistence and concurrent edit contracts remain green with budget integration. |
| [project-draft-storage.test.ts](../../../../frontend/src/shared/lib/project-draft-storage.test.ts) — 8 | Accepted scope/storage/create-body/Unicode rules plus exact budget body, pinned version and newer local draft recovery; invalid version, unlimited-zero combination and negative limit are rejected. |
| [budget-gate.browser.test.ts](../../../../frontend/src/modules/defense-calculator/ui/budget-gate.browser.test.ts) — 17, reviewer-owned | Actual calculator/shared store controls, full candidate check, lower-limit update, zero/unlimited/unknown states, failed and pending input retention, late project/version/session reads, invalid receipt, pending check context, frozen restored money, and retained requested money after a subsequent conflict. |

## Findings and closure evidence

| Finding | Evidence classification | Final behavior |
|---|---|---|
| Applying a catalogue preview returned true and cleared it after the shared guard rejected the candidate | Reviewer independently reproduced the defect; permanent store test passed after the fix. Reviewer also independently verified false + same preview/project, then success after unlimited. | Rejected preview remains available and is reported as rejected. |
| Removing an unused catalogue item under limited unknown cost reported success after rejection | Frontend owner observed focused **RED → GREEN** (`true !== false`). | Caller receives `budget-blocked`; current project is unchanged. |
| “Save as New” replaced an unresolved budget attempt | Frontend owner observed **RED → GREEN** (two writes instead of one). | Create is blocked until the budget attempt is completed or explicitly discarded; frozen attempt remains. |
| P's pending check disabled Q | Independent rendered **RED → GREEN**; [RED](verification-logs/browser-context-15-red.log), [final GREEN](verification-logs/browser-final-17-green.log). | Pending state is scoped by session/project/version; old completion cannot clear new pending state. |
| Restoring requested 600000.01 after a saved-500000.00 form mounted displayed the wrong frozen amount | Independent rendered **RED → GREEN**; [RED](verification-logs/browser-recovery-16-red.log), [final GREEN](verification-logs/browser-final-17-green.log). | Restored frozen configuration updates the displayed disabled controls even after mount. |
| A failed retry after recovery could revert requested input when the pending attempt cleared | Reviewer identified the case; code was fixed before the first execution. **Post-fix GREEN only** for browser case 17, not an observed RED claim. | Requested input remains editable after conflict while ordinary failed form input is also retained. |
| Unlimited preflight described null remaining as incomplete | Frontend owner observed pure-test **RED → GREEN**. | Unlimited remaining says “не ограничен”; an unknown spend still says incomplete. |

Budget restore-before-first-response, lost committed receipts, divergent verification, source freezing and late identity tests were added to protect implemented paths; this document does not invent prior failing executions for them. Final independent source review is maintained in [independent-review.md](independent-review.md).

These results are a frontend checkpoint. Backend durable checks live in [backend-verification.md](backend-verification.md). Real FRC-07 acceptance, the remaining ordered release stages, and SAVE-09/FRC-10 official reporting are not accepted here.


Coordinator final addendum: real07 gate subsequently PASS (seven checkpoints,0 console/page errors); all six full-suite failures exactly match FRC02/FRC03 historical signatures. Root grants local07 PASS. See real-integration/result.json and test-evidence.md.
