# FRC-04 backend evidence — 2026-09-20

Backend baseline: `b04696d87b5a5a085c9c5cc4eda1e7dacff8af12`. Work is uncommitted in the shared workspace. No deployment, production migration, commit or push performed. Runtime used Go `go1.26.0 darwin/arm64`, existing module dependencies and the parent-owned disposable PostgreSQL 16 cluster at loopback port 55434. Tests create and remove unique synthetic schemas; concurrent calls commit independent transactions.

## Implemented boundary

- The existing project module retains validated raw JSON alongside typed domain values. Persistence/export overlays server project ID, enterprise ID, configuration name, version and updatedAt, preserving nested safe extensions, geometry, altitude, visibility/locked state, notes, null and zero prices, overrides, compound equipment, and weapon/detection/EW fields. Top-level requestId/generatedAt are excluded. Unsupported schemaVersion is still rejected; extensions never authorize a resource or enter typed calculations.
- One transaction performs a persisted membership check, expected-version check, current save, optional budget update, frozen `{project,budget,inputDataVersions}` revision and audit append. Returned version is assigned only after commit. The actual budget row is captured; missing budget is null. Input-data provenance is currently `{}`, not user-asserted provenance.
- GET/export accept projectVersion. A missing historical version returns revision_not_found; it cannot fall back to current. The get response adds snapshot metadata; export remains the raw DefenseProject document.
- Create/import Idempotency-Key scope is actor + operation, with 24-hour expiry and canonical payload conflict detection. Replays require current access and return the original revision without another write/event. Expired receipts are reset in place under lock, explicitly clearing the old project reference.
- The revision migration backfills only the stored current version. Historical actor UUIDs have no mutable user FK. Deleting a project removes ordinary revision access and leaves idempotency replay denied until expiry. The additive append-only audit table has no live project/user FKs and retains minimal identifier/version events.
- Shared audit.RequestIDKey is `fortis.request_id`; root-owned HTTP middleware generates the UUID and X-Request-ID. The service actor comes from authentication. Events contain no raw project, map, amount, email or credentials. Event insert failure rolls back current state, budget, revision and deletion.

The `name` server configuration/variant label and document `projectName` business title remain distinct. The frontend fixture intentionally submits configuration name `Frontend fixture`; original projectName survives. Metadata comparisons are separate from business-field equality.

## Acceptance evidence

| Scenario | Behavioral evidence | Result |
| --- | --- | --- |
| REV-01 | TestFRC04LosslessDocument and real-PG TestFRC04PostgresFrontendFixture compare actual frontend-constructor fixture business fields through current/revision/raw export | PASS |
| REV-02 | TestFRC04PostgresFreezesActualTemplateAndBudget changes the same referenced global template after save and changes the current budget after revision 2 | PASS; old export and budget remain frozen |
| REV-03 | TestFRC04PostgresCASAndRollback/two_writers_same_version | PASS; exactly one v2, one version conflict |
| REV-04 | Injected revision-insert failure after current and budget writes | PASS; current/budget/version/revision all roll back |
| REV-05 | Fresh-key 2-writer test, expired-key 8-writer test, original revision replay after later update | PASS; single committed result per key lifetime |
| REV-06 | Same key with changed normalized payload via actual router | PASS; HTTP 409 idempotency_conflict |
| REV-07 | TestFRC04PostgresLegacyBackfill seeds v7, migrates and queries v6 | PASS; only v7 exists, missing history returns revision_not_found |
| REV-08 | Revoked membership, deleted identity/project and orphaned ownership on historical reads/export/replay; persisted membership removed between app precheck and write | PASS; no tenant bypass or write after revoke |
| REV-09 | Minimal schemaVersion=1 backfill plus incomplete circle/ring fixtures | PASS; known defaults, no panic and no invented history |
| REV-10 | Fixture compares original geometry coordinates, radius fields and all business values after DB/raw export; parent independently imported emitted backend export into FE | PASS; no second unit conversion |
| Audit | TestFRC04PostgresAuditAtomicity checks authenticated actor, HTTP response request-ID equality despite spoofed input header, create/import/update/budget/delete action/version transitions, no replay event, audit failure rollback, retained history and rejected UPDATE/DELETE | PASS |

The backend fixture `cmd/app/testdata/frc04-project.json` is the same 5,504-byte fixture produced by the actual frontend constructor. Optional `FORTIS_FRC04_EXPORT_FILE` writes the resulting raw export. Parent reported its FE import comparison passed 3/3; this agent did not rerun frontend tests.

## RED → GREEN record

Persisted tests first reproduced loss of nested runtime fields, versionless update success, missing revision storage and duplicate retry results. Further regression REDs reproduced missing defaults in legacy migration load, user deletion failing against immutable revision FK updates, orphaned ownership replay returning 500, and missing audit storage. Each now passes.

Independent review supplied real-PG overlays for incomplete-circle panic and expired-key concurrency. Permanent TestFRC04PostgresLegacyGeometryDefaults and TestFRC04PostgresConcurrentExpiredIdempotency reproduced the failures before fixes. The expired-key RED returned `save project: record not found`; the in-place reset passes with eight callers, one new project, one revision and one audit event. Reviewer reran both independent overlay tests successfully and reported no open findings. Review overlays were outside the repository and are not required by the permanent tests.

## Exact verification commands and results

Run from `backend/`. The cache path belongs to this disposable local verification environment.

```sh
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache FORTIS_FRC04_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' FRC02_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' FORTIS_FRC04_EXPORT_FILE=/private/tmp/fortis-frc04-export.json go test ./cmd/app -run 'TestFRC0(2Postgres|4)' -count=1 -v
```

PASS: 15 top-level tests (14 FRC-04, one FRC-02) plus eight nested cases; no skips. Includes actual router/auth/controller requests and actual PostgreSQL CAS, rollback, audit, replay, migration and current-state checks. After adding stronger HTTP request-ID and exact audit transition assertions, reran `go test ./cmd/app -run '^TestFRC04PostgresAuditAtomicity$' -count=1 -v` with the same FORTIS_FRC04_TEST_DSN/cache settings: PASS. That fixture explicitly includes the actual HTTP response middleware; the reused FRC-02 helper otherwise wraps only authentication.

```sh
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go test ./... -count=1 -json > /private/tmp/frc04-backend-all-tests.jsonl
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go test -tags=unit ./... -count=1 -json > /private/tmp/frc04-backend-unit-tests.jsonl
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go vet ./...
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go build -o /private/tmp/frc04-backend-app ./cmd/app
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go test ./internal/modules/defense_project/ui ./internal/middleware -count=1
```

- Full default suite: 243 top-level + 84 nested PASS, 21 opt-in tests SKIP, zero FAIL; 27 tested packages pass. Skips are explicit PostgreSQL/browser opt-ins (including separately executed FRC-04/FRC-02 SQL), plus root-owned FRC-12 SQL/browser tests.
- Unit-tag suite: 275 top-level + 84 nested PASS, the same 21 SKIP, zero FAIL; 27 tested packages pass.
- `go vet`, build and final DTO/UI/middleware checks: PASS. Build emitted a denied optional module stat-cache warning but exited 0 and produced the temporary binary.
- Existing FRC-01 database-readiness/liveness and FRC-02 memory authorization tests are included in the full suite. The FRC-02 SQL regression also passed with all unauthorized assertions retained. Successful-update fixtures were adapted only to send mandatory expected version.

Root is generating the combined Swagger using the pinned v0.36.6 tool outside the repository; this agent changed owning DTO annotations and did not hand-edit generated swagger.json. golangci-lint is absent in this environment; `go vet` passed, but it is not represented as a golangci-lint run.

## Remaining release integration boundaries

- Root owns final acceptance/ADR, generated OpenAPI, deployment/runtime gate and frontend evidence. No production-ready claim follows from local SQL tests alone.
- UpdateBudget is the implemented common revision transaction hook. Wiring the existing budget API to it and financial invariants belongs to FRC-07; no FRC-07 financial gate was invented as an FRC-04 prerequisite. An accepted final release must not keep a direct independent budget write.
- Membership/session audit and roles remain deferred under ADR0017. This change adds scoped project/budget events only. Administrator-resistant audit storage and data retention are outside this task.
- Migration down removes the additive revision/idempotency stores and functions while retaining current project rows; the legacy-backfill test verifies this. Audit down removes only its additive table/function. No historical revisions are fabricated.
