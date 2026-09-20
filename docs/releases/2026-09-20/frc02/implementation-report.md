# FRC-02 — implementation report

## 1. Статус

**Implemented / code-level verification passed / production runtime acceptance blocked.** Выполнено поверх текущего checkout. FRC-00: Implemented / Acceptance blocked by runtime evidence. FRC-01: Implemented / code-level acceptance passed / runtime acceptance blocked. К FRC-03 не переходили; commit, push, deployment и production migrations не выполнялись.

## 2. Устранённые vulnerabilities

Закрыты direct-ID cross-enterprise read/mutation, unscoped project/private asset lists и totals, financial/report/compare metadata leak, document URL disclosure до parent authorization, ordinary-JWT membership escalation и public catalog mutation. Private NULL/orphan ownership больше не считается доступным. Membership revocation проверяется без перевыпуска JWT. Account switch не переносит recovery, stores или поздние ответы A в B. Cookie presence заменена actual identity validation; production cookie hardened; external next rejected.

## 3. Backend architecture

`AuthRequired` проверяет JWT и существующую identity → controller извлекает actor → application service загружает stored resource/parent → существующий `EnterpriseService.CheckUserAccess` проверяет membership → domain operation → repository. Domain не зависит от auth/transport. Budget/cost/report наследуют project; compare проверяет оба operands до вычисления; document наследует asset. Lists используют membership-scoped SQL до pagination/count. 401 = identity, 404 = inaccessible/missing, 403 = closed operation, 500 = infrastructure failure. Normal project update не переносит ownership, version conflict остаётся 409.

## 4. Route-by-route matrix

Полная таблица 31 backend operation + frontend/BFF: [authorization-matrix.md](authorization-matrix.md).

## 5. Изменённые файлы

[changed-files.md](changed-files.md) содержит incremental FRC-02 inventory относительно snapshot перед реализацией; pre-existing FRC-00/01 изменения не приписаны FRC-02. SHA-256 финальных исходников — [source-manifest.json](source-manifest.json).

## 6. ADR-0017

[ADR-0017](../../../../knowledge-base/03_Architecture/ADR-0017-enterprise-access-boundary.md) фиксирует membership boundary, status semantics, application layer, immutable project ownership, public/private assets, document inheritance, orphans, revocation, frontend identity и operator-only actions. Full RBAC, RLS, fine-grained ACL, audit log и session revocation отложены. Обновлены KB index/release index и уточнено противоречащее правило public catalog в roadmap; старые ADR сохранены.

## 7. A–J

| Case | Result / evidence |
|---|---|
| A Enterprise isolation | PASS, A↔B list/get/update/delete/membership tests |
| B Project direct ID | PASS, own success / foreign get/export 404 |
| C Project mutations | PASS, foreign create/import/update/delete denied; ownership immutable |
| D Financial/report | PASS, parent access before budget/cost/check/report |
| E Compare | PASS, both operands checked; no partial result |
| F Private assets | PASS, scoped list/total and private CRUD |
| G Documents | PASS, parent policy; foreign metadata/download URL absent |
| H Account switch | PASS, state-level identity cases including five stale-error races + real browser A→B |
| I Revocation | PASS, memory + PostgreSQL + browser same-JWT/cookie |
| J Public assets | PASS, A/B authenticated reads; ordinary mutations 403 |

Memory suite calls real HTTP router/controllers/services with test repositories; PostgreSQL suite replaces repositories with production implementations. [Test evidence](test-evidence.md) lists commands and logs.

## 8. Orphans / anti-enumeration

PASS: NULL-owned project/private asset return 404; document with missing/private-orphan parent denied; public NULL-owned asset/document readable. PostgreSQL test creates actual SQL NULL rows. Missing UUID and existing foreign UUID have identical JSON status/body; access-storage error remains 500.

## 9. Account switch

PASS: deterministic `fortis-defense-project:user:<encoded identity>` key; generic legacy key is not read or migrated. Logout clears active stores; B cannot recover A. A snapshot may remain under A key for later unverified recovery. Generation guards discard in-flight A responses; keyed identity boundary remount clears component-local financial/report state. No active QueryClient cache exists in current product flow. Legacy configuration memory also resets.

## 10. Revocation / saving

PASS: revoke through trusted test fixture, reuse same JWT/cookie, subsequent project/enterprise/budget/report/private asset/document access fails 404. UI marks opened project inaccessible/unverified, blocks save and does not claim saved or inject demo data. Current product has manual save; no autosave subsystem or automatic retry introduced.

## 11. PostgreSQL

PASS on isolated local PostgreSQL cluster with synthetic A/B fixture. Real repositories, membership JOIN/count, project get/update, assets/documents, NULL ownership and revocation exercised. Tests apply existing migrations inside isolated schema/transaction and roll back. No production database connection or migration.

## 12. Browser E2E

PASS **3/3**, Chromium → Next.js → Go → PostgreSQL. H loads Project A and successful report, logs out, logs in B, checks absence of A and direct A request 404. I revokes membership and checks PUT 404, visible inaccessible alert, disabled save and unchanged cookie. Responsive workspace checked at 375/414/768/1024/1440 px with no horizontal overflow. Initial logout navigation defect was reproduced and fixed; a later test selector mismatch was corrected against actual accessible name.

## 13. Commands / verification

See [test-evidence.md](test-evidence.md) for executed commands, outcomes, failed intermediate attempts and preserved logs. Final Go normal/unit suites and build PASS; frontend typecheck/lint/build PASS; all new security and FRC-01 regressions PASS. Full frontend suite: **90 tests, 84 PASS, 6 known failures**.

## 14. Existing vs new failures

Six pre-FRC-01 frontend failures remain; exact normalized per-file failure signatures match pre-FRC-02 snapshot **6/6**. [Comparison](evidence/failure-signatures-after.json). Test bodies were not changed. No new failure remains in final suites. This is not a claim that the full frontend suite is green.

## 15. Runtime / storage blockers

Production deployment/image identity, actual environment/TLS/cookie behavior, production DB inventory, object-storage ACL/direct or presigned URL behavior and production restart/persistence remain unverified. Backend denies URL disclosure before authorization, but previously obtained direct storage URLs require independent storage controls. A local synthetic pass cannot establish production acceptance. Operator membership/catalog provisioning needs an explicit trusted operational process; no new operator API/UI was invented.

## 16. Cleanup / migrations

No new schema migration needed for this implementation. Before production, operator must run [read-only inventory](orphan-inventory.md), review findings, then explicitly decide repair/quarantine/delete. No automatic assignment of orphan resources. Constraint migration requires actual-data cleanup assessment first; none proposed or applied here.

## 17. Diff summary

- Backend: actor-aware application contracts/controllers, reused membership checker, scoped repositories, parent checks, authorization error mapping and tests.
- Frontend: session validation, identity-scoped recovery/reset and stale-response guards, access-error UI/save handling, cookie/next hardening and tests.
- Knowledge-base: ADR-0017, index/release links, access-policy clarification.
- Parent: acceptance addendum, FRC-02 report/matrix/evidence/inventory. **No FRC-02 deploy change**, submodule pointer update or commit; existing deploy modifications belong to earlier work.

## 18. Непроверенное

Production gates from §15, real storage permission/URL expiry, operational provisioning, production orphan inventory/cleanup and final deployed artifact acceptance. Full RBAC/session revocation/RLS/audit remain explicitly out of scope. Browser checks use a local synthetic fixture, not production accounts.

## Independent review

One P2 found: delayed project access failures could invalidate a different current project. Added five regression cases (load/overwrite/create/delete/list), observed all five fail, scoped invalidation to the affected project and checked stale-load generation first; all five now pass. Auth/identity suite 14/14; complete frontend suite 90 tests / 84 pass / same six known failures. Production build, lint, typecheck and browser 3/3 repeated successfully. No backend bypass found by reviewer. No deferred minor findings. Temporary backend, Next.js and PostgreSQL stopped; generated backend binary and task-specific tsconfig additions removed.

Final: fixed stale access-error invalidation — `late project access failures cannot invalidate another current project` RED→GREEN; final suite has zero new failures (six accepted baseline failures remain).

## Implementation ledger (preserved)

### Original plan

Status: implementation and verification completed; final review recorded above. Approved specification: user request 2026-09-20, enterprise isolation only. Current checkout retained; no commit/push/deployment/production migration.

## Plan

1. RED: persist two-user application/controller regression suite from investigation; prove existing cross-tenant paths fail expected 404/403.
2. Backend: reuse EnterpriseService.CheckUserAccess, bind actor at application boundary; immutable project ownership; authorize all derived and parent resources; scoped SQL lists; operator-only public/membership/destructive enterprise actions.
3. Backend: local PostgreSQL integration and orphan inventory. No schema changes unless demonstrated necessary.
4. RED → GREEN frontend: verified identity, scoped recovery, account reset/error boundary, cookie flags and safe next.
5. A–J, orphan/error mapping, FRC-01 regressions, Go tests/build, frontend tests/types/lint/build; browser A→B if local stack works.
6. ADR-0017, final matrix/evidence/changed-files/inventory; one independent whole-change review with a bounded fix pass. Stop before FRC-03.

## Rulings / shared boundaries

- Current checkout and no commits override executing-plans worktree/commit steps; this ledger tracks files and test evidence without inventing commits.
- Enterprise metadata update remains allowed to member (existing domain CRUD); creation, deletion and membership administration are operator-only for ordinary JWT. No operator role API added. Existing internal provisioning remains explicit; tests create fixture records below the user-facing boundary.
- API membership mutations return 403 to ordinary authenticated callers without checking target existence (closed operation, avoids enumeration). Enterprise delete first checks accessible context then returns 403; foreign target 404.
- Use existing schema. New projects require authorized non-empty enterprise. Orphan resources fail closed; no automatic data reassignment.
- Authentication principal must be established independently of user-supplied ownership. Access checker/storage failures retain 500; absence/denial maps consistently to 404.
- FRC-01 preservation on transient errors remains; identity changes must clear sensitive state, resource denial cannot schedule retries. Current checkout uses manual save; no autosave added.
- Session revocation is explicitly deferred by user; logout clears browser identity/caches/cookie, membership revocation rechecks storage each request using unchanged JWT.
- PostgreSQL executables are available locally; isolated test cluster will be attempted in tmp, not production. Docker absent.
