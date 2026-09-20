# FRC-02 — changed files

Incremental content comparison against pre-implementation snapshot (SHA-256), not HEAD diff: current checkout already contained FRC-00/01 and user changes. Existing files retain those changes. No commit, branch change or submodule pointer update. Generated temporary binary/Next configuration changes are removed.

## parent — 32 files

- `modified` `docs/releases/2026-09-20/acceptance-matrix.md`
- `added` `docs/releases/2026-09-20/frc02/authorization-matrix.md`
- `added` `docs/releases/2026-09-20/frc02/evidence/backend-access-extended.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/backend-build-final.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/backend-di.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/backend-final.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/backend-format-final.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/backend-red.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/backend-unit-final.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/browser-e2e-final2.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/browser-e2e-review.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/failure-signatures-after.json`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-auth-red.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-build-2.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-build-review.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-full-final.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-full-review.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-identity-red.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-lint-final.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-lint-review.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-security-extended.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-switch-red.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-types-clean.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/frontend-types-final.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/postgres-final.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/review-race-green.log`
- `added` `docs/releases/2026-09-20/frc02/evidence/review-race-red.log`
- `added` `docs/releases/2026-09-20/frc02/implementation-report.md`
- `added` `docs/releases/2026-09-20/frc02/orphan-inventory.md`
- `added` `docs/releases/2026-09-20/frc02/orphan-inventory.sql`
- `added` `docs/releases/2026-09-20/frc02/pre-frc02-failure-signatures.txt`
- `added` `docs/releases/2026-09-20/frc02/test-evidence.md`

## frontend — 23 files

- `modified` `src/app/api/auth/login/route.ts`
- `modified` `src/app/api/auth/logout/route.ts`
- `modified` `src/app/api/auth/register/route.ts`
- `modified` `src/app/layout.tsx`
- `modified` `src/modules/auth/ui/login-page.tsx`
- `modified` `src/modules/auth/ui/register-page.tsx`
- `modified` `src/modules/drone-defense/domain/use-defense-variants-store.ts`
- `modified` `src/modules/drone-defense/infra/backend-integration-contract.test.ts`
- `modified` `src/modules/drone-defense/ui/variant-selector.tsx`
- `modified` `src/proxy.ts`
- `modified` `src/shared/lib/api-client.ts`
- `added` `src/shared/lib/auth-boundary.release.test.ts`
- `added` `src/shared/lib/identity-isolation.release.test.ts`
- `added` `src/shared/lib/identity.ts`
- `modified` `src/shared/lib/project-runtime.release.test.ts`
- `added` `src/shared/lib/safe-next.ts`
- `added` `src/shared/lib/session-state.ts`
- `modified` `src/shared/lib/use-defense-project-store.test.ts`
- `modified` `src/shared/lib/use-defense-project-store.ts`
- `added` `src/shared/server/auth-cookie.ts`
- `added` `src/shared/ui/identity-boundary.tsx`
- `added` `test/playwright/frc02.config.ts`
- `added` `test/playwright/frc02.spec.ts`

## backend — 37 files

- `modified` `cmd/app/dependencies.go`
- `added` `cmd/app/frc02_access_test.go`
- `added` `cmd/app/frc02_postgres_test.go`
- `added` `internal/auth/access.go`
- `modified` `internal/middleware/auth.go`
- `modified` `internal/modules/budget/application/budget_service.go`
- `modified` `internal/modules/budget/application/budget_service_test.go`
- `modified` `internal/modules/budget/ui/controller.go`
- `modified` `internal/modules/budget/ui/controller_test.go`
- `modified` `internal/modules/defense_asset/application/defense_asset_service.go`
- `modified` `internal/modules/defense_asset/application/defense_asset_service_test.go`
- `modified` `internal/modules/defense_asset/application/document_service.go`
- `modified` `internal/modules/defense_asset/application/document_service_test.go`
- `modified` `internal/modules/defense_asset/domain/defense_asset_repository_interface.go`
- `modified` `internal/modules/defense_asset/infrastructure/defense_asset_repository.go`
- `modified` `internal/modules/defense_asset/ui/controller.go`
- `modified` `internal/modules/defense_asset/ui/controller_test.go`
- `modified` `internal/modules/defense_asset/ui/document_controller.go`
- `modified` `internal/modules/defense_asset/ui/document_controller_test.go`
- `modified` `internal/modules/defense_project/application/defense_project_service.go`
- `modified` `internal/modules/defense_project/application/defense_project_service_test.go`
- `modified` `internal/modules/defense_project/application/defense_project_service_update_test.go`
- `modified` `internal/modules/defense_project/domain/defense_project_errors.go`
- `modified` `internal/modules/defense_project/domain/defense_project_repository_interface.go`
- `modified` `internal/modules/defense_project/infrastructure/defense_project_repository.go`
- `modified` `internal/modules/defense_project/ui/controller.go`
- `modified` `internal/modules/defense_project/ui/controller_test.go`
- `modified` `internal/modules/defense_project/ui/dto.go`
- `modified` `internal/modules/enterprise/application/enterprise_service.go`
- `modified` `internal/modules/enterprise/application/enterprise_service_test.go`
- `modified` `internal/modules/enterprise/ui/controller.go`
- `modified` `internal/modules/enterprise/ui/controller_test.go`
- `modified` `internal/modules/report/application/report_service.go`
- `modified` `internal/modules/report/application/report_service_test.go`
- `modified` `internal/modules/report/ui/controller.go`
- `modified` `internal/modules/report/ui/controller_test.go`
- `added` `pkg/handlers/authorization.go`

## knowledge-base — 4 files

- `modified` `00_Index.md`
- `modified` `01_Requirements/Release_2026_09_20_Index.md`
- `added` `03_Architecture/ADR-0017-enterprise-access-boundary.md`
- `modified` `Продуктовый_план_Fortis.md`

Inventory artifacts `changed-files.md` and `source-manifest.json` themselves are also added; excluded from their own hash list to avoid recursion. Parent evidence logs are documentation, not product source. No FRC-02 deploy edits or new dependencies/migrations.
