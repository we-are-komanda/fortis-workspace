# FRC-04 implementation plan

**Goal:** Preserve a complete DefenseProject across save/load and freeze every accepted server version.
**Spec:** `docs/fortis-release-specs/specs/FRC-04_project_revisions.md`, shared contracts; access authority ADR-0017.
**Architecture:** Extend the existing project module and BFF. Keep DefenseProject canonical, authenticated membership checks and manual save. Preserve safe JSON extensions without using them as ownership or financial authority.
**Execution:** User authorized autonomous implementation on the current checkout. Backend is exclusively delegated; root owns frontend integration, ADR and acceptance. No push/deployment/production migration.

## Backend

Exact module-level plan and RED/GREEN commands are owned by the backend implementer in `backend-plan.md` / `backend-evidence.md`. Existing project domain/application/infrastructure/UI and a timestamp migration implement immutable snapshots, mandatory version, atomic CAS, idempotent creation and historical access. Future budget enforcement remains FRC-07.

Public contract agreed before parallel code:

- Existing POST/PUT summary retains `projectId`, `version`, names; adds `projectVersion` and `snapshotDigest`.
- GET get adds `snapshot: {project,budget,inputDataVersions}`; `projectVersion` selects a frozen revision.
- GET export remains raw DefenseProject, including server `version`; supports `projectVersion` and never falls back to current when missing.
- `Idempotency-Key` scopes create/import to actor and operation for 24 hours; same key/different payload is 409. Replay rechecks current authorization.
- Missing update version is 400 `version_required`; stale version is 409 `version_conflict`; absent revision is 404 `revision_not_found`.

## Frontend exact files and interfaces

- Modify `frontend/src/modules/drone-defense/infra/backend-proxy.ts`: forward `Idempotency-Key` through the existing allowlist; retain status/body/security behavior.
- Modify `frontend/src/app/api/defense/projects/[id]/route.ts`: forward only the additive `projectVersion` query to the existing export route, with path project ID authoritative.
- Modify `frontend/src/modules/drone-defense/infra/api-client.ts`: revision-aware load and caller-provided idempotency key, maintaining existing call compatibility. Save-attempt lifecycle belongs to FRC-06.
- Modify `frontend/src/shared/lib/defense-project.ts` only where a demonstrated normalization loses existing fields. Preserve geometry extensions and canonical field values; legacy additive defaults remain compatible.
- Add meaningful round-trip and real local HTTP boundary regression tests adjacent to the owning code. Fixtures are synthetic and use the existing workspace constructor, all layer forms, optional fields, instance values, visibility and safe extensions.
- Update `frontend/src/shared/types/defense-project.ts` only for fields exposed by the implemented API; avoid speculative types.

## Steps and acceptance

- [ ] Reproduce lost geometry fields, discarded revision query and dropped idempotency header as failing behavioral tests.
- [ ] Apply smallest shared fixes; verify focused tests green.
- [ ] Verify full FE→BE→PostgreSQL→BE→FE round-trip with synthetic fields, exact units, safe extensions and frozen earlier revision.
- [ ] Verify PostgreSQL race, revision-insert rollback, idempotency conflict/replay/revocation and current-version-only backfill.
- [ ] Re-run FRC-01/02 security/state regressions and relevant frontend types/lint, backend tests/build.
- [ ] Independent review, fix confirmed findings regression-first, then record evidence/ADR/acceptance.

## Review focus

- Unknown extensions must survive without overriding authoritative project/enterprise/version metadata.
- Replay after deletion/revocation must fail; concurrent same-key creates must not duplicate.
- Legacy JSON NULL/missing prices, custom IDs and geometry coordinates must not be silently normalized away.
- Failed revision persistence must not leave current state/version/budget partially changed.
- A request for an unavailable old version must never return the current project.
