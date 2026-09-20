# FRC-04 scope/file inventory

Owning project module inventory includes existing files read as part of verification; actual diff determines edits. Shared FRC02 fixture successful update gains mandatory version; FRC12 provider/auth-list lines belong to FRC12. Middleware audit hook belongs to FRC04. Generated whole backend/swagger.json is ignored by the existing repository; scoped validated artifact is tracked in this report directory.

- `backend/cmd/app/frc04_access_test.go`
- `backend/cmd/app/frc04_postgres_test.go`
- `backend/cmd/app/testdata/frc04-project.json`
- `backend/internal/audit/event.go`
- `backend/internal/middleware/http_response.go`
- `backend/internal/middleware/request_id_test.go`
- `backend/internal/modules/defense_project/application/defense_project_service.go`
- `backend/internal/modules/defense_project/application/defense_project_service_test.go`
- `backend/internal/modules/defense_project/application/defense_project_service_update_test.go`
- `backend/internal/modules/defense_project/application/project_revisions.go`
- `backend/internal/modules/defense_project/document/json.go`
- `backend/internal/modules/defense_project/document/json_test.go`
- `backend/internal/modules/defense_project/domain/defense_project.go`
- `backend/internal/modules/defense_project/domain/defense_project_errors.go`
- `backend/internal/modules/defense_project/domain/defense_project_errors_test.go`
- `backend/internal/modules/defense_project/domain/defense_project_repository_interface.go`
- `backend/internal/modules/defense_project/domain/project_revision_repository_interface.go`
- `backend/internal/modules/defense_project/infrastructure/defense_project_repository.go`
- `backend/internal/modules/defense_project/infrastructure/defense_project_repository_test.go`
- `backend/internal/modules/defense_project/infrastructure/models.go`
- `backend/internal/modules/defense_project/infrastructure/project_revision_repository.go`
- `backend/internal/modules/defense_project/ui/controller.go`
- `backend/internal/modules/defense_project/ui/controller_test.go`
- `backend/internal/modules/defense_project/ui/dto.go`
- `backend/internal/modules/defense_project/ui/mapper.go`
- `backend/migrations/1789900000_project_revisions.down.sql`
- `backend/migrations/1789900000_project_revisions.up.sql`
- `backend/migrations/1789900001_audit_events.down.sql`
- `backend/migrations/1789900001_audit_events.up.sql`
- `frontend/src/app/api/defense/projects/[id]/route.ts`
- `frontend/src/modules/drone-defense/infra/api-client.ts`
- `frontend/src/modules/drone-defense/infra/backend-proxy.ts`
- `frontend/src/modules/drone-defense/infra/project-revisions.release.test.ts`
- `frontend/src/shared/lib/defense-project.ts`
- `frontend/src/shared/lib/project-roundtrip.release.test.ts`
- `frontend/test/fixtures/frc04-project.json`

Parent: frc04 artifacts, acceptance matrix/run ledger. Knowledge-base:ADR-0018 and index/run note.
