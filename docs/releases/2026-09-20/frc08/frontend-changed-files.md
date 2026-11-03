# FRC-08 frontend changed files

Base frontend: accepted FRC-07 `6838dd1`. Frontend implementation owner: **12 files**, eight modified and four new. This checkpoint claims no commit or acceptance.

| File, relative to `frontend/` | Purpose |
|---|---|
| [src/shared/types/finance.ts](../../../../frontend/src/shared/types/finance.ts) | Adds shared CompareSide/CompareResult using existing cost/budget/identity types. |
| [src/modules/defense-calculator/infra/backend-project-api.ts](../../../../frontend/src/modules/defense-calculator/infra/backend-project-api.ts) | Reuses cost validation; sends pinned compare refs and validates full response authority, tenant and exact deltas/percentage. |
| [src/modules/defense-calculator/infra/compare-revisions.release.test.ts](../../../../frontend/src/modules/defense-calculator/infra/compare-revisions.release.test.ts) — new | Five behavioral API/financial-boundary tests. |
| [src/modules/defense-calculator/domain/configuration-comparison.ts](../../../../frontend/src/modules/defense-calculator/domain/configuration-comparison.ts) — new | Stable-ID pairing, pinned selection/request state, dirty choices and verified-save repinning. |
| [src/modules/defense-calculator/domain/configuration-comparison.test.ts](../../../../frontend/src/modules/defense-calculator/domain/configuration-comparison.test.ts) — new | Two stable-ID join checks, including equal display names. |
| [src/modules/defense-calculator/ui/configuration-comparison.tsx](../../../../frontend/src/modules/defense-calculator/ui/configuration-comparison.tsx) — new | Version selectors, responsive result/detail view, accessible dirty-choice modal and errors. |
| [src/modules/workspace/ui/project-workspace-page.tsx](../../../../frontend/src/modules/workspace/ui/project-workspace-page.tsx) | Replaces old mutable-ID comparison with the reusable component and removes pagination-driven selection reset. Existing enterprise/project/save flow stays in place. |
| [src/modules/defense-calculator/ui/calculator-page.tsx](../../../../frontend/src/modules/defense-calculator/ui/calculator-page.tsx) | Entry link to the same workspace comparison. |
| [src/shared/lib/identity.ts](../../../../frontend/src/shared/lib/identity.ts) | Neutral `saveCurrentProject` name for the existing save gate; `saveBeforeLogout` remains its strict compatibility alias. |
| [src/shared/config/product-capabilities.ts](../../../../frontend/src/shared/config/product-capabilities.ts) | Compare points to its implemented workspace entry; no other gate is promoted. |
| [src/shared/ui/release-surface.test.tsx](../../../../frontend/src/shared/ui/release-surface.test.tsx) | Compare available and report still gated; other release-surface assertions retained. |
| [src/modules/drone-defense/infra/backend-integration-contract.test.ts](../../../../frontend/src/modules/drone-defense/infra/backend-integration-contract.test.ts) | Valid pinned comparison response and exact four-parameter request assertion; prior boundary checks retained. |

Separately owned: reviewer [configuration-comparison.browser.test.ts](../../../../frontend/src/modules/defense-calculator/ui/configuration-comparison.browser.test.ts); coordinator [test/playwright/frc08-live.cjs](../../../../frontend/test/playwright/frc08-live.cjs), final build/regression/real evidence, ADR and acceptance decisions; backend source and backend-* documents. These do not inflate the twelve-file frontend implementation count. This owner also writes the three `frontend-*.md` parent documents, without moving frontend source across repository boundaries.

No dependencies, migrations, replacement project model or duplicated financial projection were added. Next.js remains the accepted pinned 16.2.11. Latest comparison20/20, combined browser76/76, real integration4/4 with zero console/page errors, and production build are verified. Full-suite239PASS/6FAIL/96SKIP is recorded with exact baseline and final independent type/lint/hash confirmation pending. See [frontend-implementation.md](frontend-implementation.md) and [frontend-evidence.md](frontend-evidence.md).
