# FRC-07 frontend changed files

Base: accepted frontend `e49253b`. Scope below is the frontend implementation owner's **17 files** (12 existing files modified, 5 new files), including its focused tests. Paths are relative to `frontend/`. No source is copied into the parent repository, no dependency was added by this implementation, and no commit is claimed by this checkpoint.

| File | Change |
|---|---|
| [src/shared/types/finance.ts](../../../../frontend/src/shared/types/finance.ts) | Exact `BudgetConfig`, `BudgetProjection`, and full-candidate `BudgetCheckResponse` contracts. |
| [src/shared/types/defense-project.ts](../../../../frontend/src/shared/types/defense-project.ts) | Layer deletion result can carry `budget-blocked` to the calling UI. |
| [src/shared/lib/budget-projection.ts](../../../../frontend/src/shared/lib/budget-projection.ts) — new | Reuses FRC-05 whole-project costing; exact amount parser/formatting, pinned receipt validation, local full-candidate and saved-overage decision. |
| [src/shared/lib/budget-projection.test.ts](../../../../frontend/src/shared/lib/budget-projection.test.ts) — new | Six exact-money, authority and response-boundary tests. |
| [src/shared/lib/project-save-state.ts](../../../../frontend/src/shared/lib/project-save-state.ts) | Adds the budget kind to the existing frozen save attempt. |
| [src/shared/lib/project-draft-storage.ts](../../../../frontend/src/shared/lib/project-draft-storage.ts) | Validates scoped budget replay/version/config and explicit source metadata, preserving the existing recovery envelope. |
| [src/shared/lib/project-draft-storage.test.ts](../../../../frontend/src/shared/lib/project-draft-storage.test.ts) | Adds frozen budget recovery and invalid-config/version checks to the accepted storage tests. |
| [src/shared/lib/use-defense-project-store.ts](../../../../frontend/src/shared/lib/use-defense-project-store.ts) | Matching authoritative projection state, common edit guard, historical read bypass, restoration verification, and truthful blocked result propagation through callers. |
| [src/modules/drone-defense/infra/api-client.ts](../../../../frontend/src/modules/drone-defense/infra/api-client.ts) | Frozen create source; budget PUT routing and canonical full-snapshot acknowledgement validation. |
| [src/modules/drone-defense/domain/use-defense-variants-store.ts](../../../../frontend/src/modules/drone-defense/domain/use-defense-variants-store.ts) | Budget update/retry in the accepted save pipeline; explicit verification after ambiguity; current context checks; source inheritance for copies; draft/input/error preservation. |
| [src/modules/drone-defense/domain/project-budget.release.test.ts](../../../../frontend/src/modules/drone-defense/domain/project-budget.release.test.ts) — new | Thirteen shared-store/recovery/copy/ambiguous-save behavior tests. |
| [src/modules/defense-calculator/infra/backend-project-api.ts](../../../../frontend/src/modules/defense-calculator/infra/backend-project-api.ts) | Replaces legacy float-budget helpers with pinned projection GET and full-candidate check contracts. |
| [src/modules/defense-calculator/domain/use-project-budget.ts](../../../../frontend/src/modules/defense-calculator/domain/use-project-budget.ts) — new | Scoped pinned read, explicit full-candidate check, stale-response suppression and context-owned pending state. |
| [src/modules/defense-calculator/ui/project-budget-panel.tsx](../../../../frontend/src/modules/defense-calculator/ui/project-budget-panel.tsx) — new | Shared calculator/GIS panel, exact editable input, explicit unlimited, candidate display, recovery intent and failed-input retention. |
| [src/modules/defense-calculator/ui/calculator-page.tsx](../../../../frontend/src/modules/defense-calculator/ui/calculator-page.tsx) | Mounts the shared budget panel for the authorized workspace context. |
| [src/modules/defense-calculator/ui/calculator-page.browser.test.ts](../../../../frontend/src/modules/defense-calculator/ui/calculator-page.browser.test.ts) | Scopes existing cost-total headings to “Смета размещённых объектов” after adding the budget heading; preserves the FRC-05 assertions. |
| [src/modules/drone-defense/ui/drone-defense-prototype.tsx](../../../../frontend/src/modules/drone-defense/ui/drone-defense-prototype.tsx) | Mounts the same compact budget panel in GIS and retains the object editor when the common guard rejects its save. |

## Separately owned files in the same working tree

These files are deliberately excluded from the 17-file implementation count:

| Owner / scope | Files |
|---|---|
| Independent FRC-07 rendered acceptance | [src/modules/defense-calculator/ui/budget-gate.browser.test.ts](../../../../frontend/src/modules/defense-calculator/ui/budget-gate.browser.test.ts), 17 tests; reviewer owns its scenarios and assertions. |
| Coordinator real FRC-07 gate | [test/playwright/frc07-live.cjs](../../../../frontend/test/playwright/frc07-live.cjs); real-backend execution and final acceptance remain coordinator-owned. |
| Coordinator pre-FRC-13 renderer prerequisite | [src/modules/drone-defense/ui/gis-board.tsx](../../../../frontend/src/modules/drone-defense/ui/gis-board.tsx) and [test/playwright/frc13-layer-identities.cjs](../../../../frontend/test/playwright/frc13-layer-identities.cjs): deck IDs use stable `zone.layerId`, with a separate repeated-display-code browser regression. |
| Coordinator toolchain pin | [package.json](../../../../frontend/package.json), [pnpm-lock.yaml](../../../../frontend/pnpm-lock.yaml): pin Next.js and matching eslint-config-next to the installed/tested 16.2.11. |
| Parent documentation | This file, [frontend-implementation.md](frontend-implementation.md), [frontend-evidence.md](frontend-evidence.md); backend/ADR/acceptance/review/integration evidence stays with its assigned owners. |

Validation and exact boundaries are recorded in [frontend-evidence.md](frontend-evidence.md). This manifest does not claim real-gate or whole-release acceptance.
