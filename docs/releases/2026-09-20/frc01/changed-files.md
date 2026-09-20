# FRC-01: рабочие изменения

Полный список source-файлов; существующие output и FRC-00 артефакты исключены из frontend списка. В knowledge-base index/roadmap/release index содержат также ранее внесённые изменения FRC-00.

### frontend

- `frontend/next.config.ts`
- `frontend/src/app/api/auth/login/route.ts`
- `frontend/src/app/api/auth/me/route.ts`
- `frontend/src/app/api/auth/register/route.ts`
- `frontend/src/app/api/defense/catalog/route.ts`
- `frontend/src/app/api/defense/evaluate/route.ts`
- `frontend/src/app/api/defense/facilities/route.ts`
- `frontend/src/app/api/defense/layers/route.ts`
- `frontend/src/app/api/defense/projects/[id]/route.ts`
- `frontend/src/app/api/defense/projects/route.ts`
- `frontend/src/app/api/defense/recommend/route.ts`
- `frontend/src/app/api/health/live/route.ts`
- `frontend/src/app/api/health/ready/route.ts`
- `frontend/src/app/api/runtime/route.ts`
- `frontend/src/app/api/v1/[...path]/route.ts`
- `frontend/src/app/layout.tsx`
- `frontend/src/modules/defense-calculator/ui/calculator-page.tsx`
- `frontend/src/modules/drone-defense/domain/use-defense-studio-store.ts`
- `frontend/src/modules/drone-defense/domain/use-defense-variants-store.test.ts`
- `frontend/src/modules/drone-defense/domain/use-defense-variants-store.ts`
- `frontend/src/modules/drone-defense/infra/api-client.ts`
- `frontend/src/modules/drone-defense/infra/asset-api-proxy-contract.test.ts`
- `frontend/src/modules/drone-defense/infra/asset-documents-api.ts`
- `frontend/src/modules/drone-defense/infra/asset-library-api.ts`
- `frontend/src/modules/drone-defense/infra/backend-proxy.release.test.ts`
- `frontend/src/modules/drone-defense/infra/backend-proxy.ts`
- `frontend/src/modules/drone-defense/infra/enterprise-api.ts`
- `frontend/src/modules/drone-defense/infra/readiness.release.test.ts`
- `frontend/src/modules/drone-defense/ui/drone-defense-prototype.tsx`
- `frontend/src/modules/drone-defense/ui/variant-selector.tsx`
- `frontend/src/modules/workspace/ui/project-workspace-page.tsx`
- `frontend/src/shared/lib/api-client.ts`
- `frontend/src/shared/lib/defense-project.ts`
- `frontend/src/shared/lib/project-runtime.release.test.ts`
- `frontend/src/shared/lib/use-defense-project-store.test.ts`
- `frontend/src/shared/lib/use-defense-project-store.ts`
- `frontend/src/shared/server/runtime-config.ts`
- `frontend/src/shared/ui/runtime-provider.tsx`

### backend

- `backend/cmd/app/dependencies.go`
- `backend/internal/probe/database_check_service.go`
- `backend/internal/probe/database_check_service_test.go`

### knowledge-base

- `knowledge-base/"\320\237\321\200\320\276\320\264\321\203\320\272\321\202\320\276\320\262\321\213\320\271_\320\277\320\273\320\260\320\275_Fortis.md"`
- `knowledge-base/00_Index.md`
- `knowledge-base/01_Requirements/Release_2026_09_20_Index.md`
- `knowledge-base/03_Architecture/ADR-0016-runtime-backend-boundary.md`

### parent / deploy

- `deploy/production/docker-compose.yml`
- `deploy/production/frontend.Dockerfile`
- `deploy/production/README.md` (добавление FRC-01 после существующего FRC-00 текста)
- `docs/releases/2026-09-20/frc01/reconciliation.md`
- `docs/releases/2026-09-20/frc01/implementation-report.md`
- `docs/releases/2026-09-20/frc01/changed-files.md`
- `docs/releases/2026-09-20/acceptance-matrix.md` (только приложение FRC-01)

Parent `.gitmodules`, README, deploy-info scripts/metadata, release manifest и остальные FRC-00 файлы не входят в реализацию FRC-01; их рабочие изменения сохранены. Gitlinks не фиксировались.
