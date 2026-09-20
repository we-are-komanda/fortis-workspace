# FRC-04 backend plan and investigation

Baseline: backend `b04696d87b5a5a085c9c5cc4eda1e7dacff8af12`; parent synchronized origins before entry. FRC-02 targeted gate passed; 37/37 backend manifest hashes match. No deployment or production migrations authorized.

## Investigation

- Existing service checks persisted enterprise membership; get/update/import/export reuse it. Preserve this boundary and recheck membership inside the database write transaction.
- Existing repository updates by `id/version` but revision and idempotency stores do not exist. Update version is optional. Typed import/export and infrastructure mappers silently drop unknown nested runtime fields; export also omits compoundProfile.
- Budget is currently a separate `budget_configs.config_data` JSONB row. Capture the actual row at each save; absent budget is explicit null, not an invented unlimited policy. Expose one transactional budget update method for the separately owned budget API integration.
- Existing module has rich typed domain values for business decisions. Retain the original validated document alongside them solely for lossless round-trip. Authoritative metadata is overlaid from persisted columns; unknown fields never grant access or alter typed calculations.

## Approved public contract

- Existing POST create/import accept optional `Idempotency-Key`; release client sends it. Scope actor + create/import operation; TTL 24h. Same normalized payload returns original project/version; changed payload 409 `idempotency_conflict`. Replays reauthorize current resource, even if previously successful.
- Existing PUT update requires positive expected `version`; missing/invalid 400 `version_required`, stale 409 `version_conflict`. Ownership/resource authorization precedes version error handling.
- GET get accepts optional positive `projectVersion`; metadata gains `projectVersion`, `snapshotDigest`, `snapshot: {project,budget,inputDataVersions}`. Missing historical version is 404 `revision_not_found`; current lookup remains default.
- Export remains raw DefenseProject JSON with authoritative version, and accepts `projectVersion`. No envelope or new geometry/units conversion.
- Create/import/update responses retain their fields and add revision metadata/snapshot. Unknown inputDataVersions are not asserted as server provenance; currently used external inputs are empty `{}`.
- `name` is the existing server configuration/variant name; `projectName` remains the document's business title. Identity/version/name/enterpriseId/updatedAt are reconciled from server metadata. Top-level transport requestId/generatedAt are excluded from persisted snapshots/digest.
- `DefenseProjectService.UpdateBudget(ctx,actor,id,expectedVersion,budgetJSON)` is the shared commit surface for budget API integration. Financial enforcement/methodology remains FRC-07 scope.

## Implementation order

1. Persist RED tests for runtime lossless fields and mandatory version, then real PostgreSQL revision/read/idempotency/CAS/rollback scenarios.
2. Add opaque document preservation and additive immutable revision metadata in owning domain; existing typed fields continue to govern business behavior.
3. Add migration for revisions and actor/operation idempotency with 24h expiry. Backfill exactly the stored current version, preserving known budget; never invent earlier history. Retain rows until explicit project deletion cascade; retention policy remains FRC-14.
4. Commit current state, budget snapshot and immutable revision in one GORM transaction using the existing rdbms Executor. CAS remains database-enforced. Unique revision and idempotency keys enforce concurrency. Attach returned version only after successful commit.
5. Extend service/controller DTOs and existing query routes without new DI components or external dependencies. Reauthorize history and replay through current resource access.
6. Run PostgreSQL REV-01..10 tests, all Go tests and build, then FRC-02/FRC-01 regressions. Adapt old successful-update fixtures only by supplying expected version; keep foreign/resource-denial assertions intact.
7. Append shared minimal audit events for project create/import/update/delete and the budget commit hook in the same transaction. Use the actor from the authenticated service call and the server request ID; replay does not append another event. Retain audit events after project/user deletion and reject event UPDATE/DELETE.

Synthetic PostgreSQL: `FORTIS_FRC04_TEST_DSN="host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable"`; root owns the disposable cluster. Tests create unique schemas and clean them up; concurrency uses committed rows and independent transactions. No real client data.

## Integration ownership

This agent owns defense_project module, its migration/tests, shared internal/audit helper and audit migration, and this backend evidence. Root owns frontend proxy, budget API wiring, request-ID middleware, combined Swagger generation and final ADR/acceptance. No commits/push/deploy. No DI change necessary for project revisions or the transaction-scoped audit helper.

Revision `created_by` is an immutable historical UUID, deliberately not a live user FK: an account deletion must not mutate history or fail because the revision update trigger rejects FK SET NULL. Resource and idempotency FKs remain explicit; project deletion cascades revisions, idempotency project reference becomes NULL so a retry remains denied until key expiry. Runtime access still requires the current identity and membership.

Independent review reproduced two additional defects and both received permanent regression coverage: incomplete legacy circle/ring geometry needed the same nil-safe defaults as the application mapper; expired idempotency records must be reset in place under their row lock because DELETE/INSERT can make waiting READ COMMITTED requests miss the replacement. The reset explicitly clears the previous project pointer. Neither fix changes preserved raw geometry or authoritative ownership.
