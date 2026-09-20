# FRC-11 implementation plan

Approved scope: honest release copy and capability-based presentation. Preserve the current GIS design and server identity boundary. No operational feature development, deployment, commits or production changes.

1. Replace the existing landing copy with the exact FRC-11 title, subtitle, CTA labels and calculation limitation. Remove unsupported SLA, accuracy, savings, detection-time, AI and integration claims. Retain existing visual classes and responsive layout. Keep the demo request destination visible without claiming submission until FRC-12 is integrated.
2. Add one `product-capabilities.ts` manifest with `available`, `demo`, `not_released`. Workspace/map/own input/version storage remain reachable; budget/report/compare are not promoted until their individual acceptance. Operational dashboard, retrospective analysis and scenario mock surfaces are demo-only.
3. Apply server runtime checks to direct operational page routes as well as their layout. An unavailable route returns a plain notice without customer-like mock data. Hide unreleased studio navigation in workspace and return to `/workspace`, preserving the current map layout. Demo surfaces retain a permanent “Демонстрационные данные” marker.
4. Replace the obsolete landing source-string test with rendered assertions. Run it RED before implementation. Add behavior/rendered tests for capability decisions, unavailable direct routes, demo marker and no false demo-request success.
5. Run focused node tests, changed-file lint and a non-incremental typecheck. Root coordinates shared build/browser/responsive verification and updates final matrix/report/KB. Report calculator copy changes to root rather than editing its concurrently owned calculator implementation.

Owned files: landing `src/app/page.tsx`, landing tests; `src/shared/config/product-capabilities.ts`; presentation gate/notice and demo marker; dashboard route files/layout; retrospective/prototype route presentation gate; studio navigation; `docs/releases/2026-09-20/frc11/implementation-plan.md` and `agent-evidence.md`. Shared auth, project/variant stores, API project routes, backend and KB are excluded.

Next.js local guides read before route changes: `01-app/03-api-reference/03-file-conventions/{layout,page}.md` and `01-app/03-api-reference/04-functions/not-found.md`. Async route props and request-time search parameters follow the installed version.
