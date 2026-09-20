# FRC-03 — research checkpoint, no implementation

Date: 2026-09-20. Status: **RESEARCH ONLY / STOPPED at user request**. FRC-06 acceptance and root GO have not been received. No FRC-03 application code, migration, test, dependency, role, or external operation was added. This records the investigation available at interruption, not an acceptance claim.

Spec: [FRC-03](../../../fortis-release-specs/specs/FRC-03_workspace.md). Authority: [ADR-0017](../../../../knowledge-base/03_Architecture/ADR-0017-enterprise-access-boundary.md) and ADR-0018 (immutable project revisions), read during the investigation.

## Existing flow and reuse

- `frontend/src/app/workspace/page.tsx` is already a thin module entry; retain it.
- Workspace implementation is `frontend/src/modules/workspace/ui/project-workspace-page.tsx`; reuse its enterprise, list, create and open UI. A whole workspace redesign is outside scope.
- `frontend/src/modules/drone-defense/infra/enterprise-api.ts` reads canonical `/api/v1/enterprises`; normalized results discard `totalItems`, and absent/invalid coordinates currently fall back to zero.
- `frontend/src/modules/drone-defense/infra/api-client.ts` exposes `listVariants()` without query arguments. The BFF GET `/api/defense/projects` already forwards query parameters unchanged to backend `/projects`.
- Backend `DefenseProjectService.ListProjects(actor, enterpriseId, limit, offset)` already checks membership for a supplied enterprise; repository rows and total use the same enterprise filter. Unscoped calls remain restricted to actor memberships. Limits are clamped to 100.
- Backend enterprise listing already joins `user_enterprises` before rows/count and supports limit/offset. Do not replace these authorization boundaries with client filtering.
- FRC-04 provides create idempotency and authoritative server project/version/enterprise context. FRC-06 is actively replacing save/recovery/navigation state; its final interfaces must be consumed after acceptance, not copied or independently rebuilt.

## Gap matrix from code inspection

These are inspected gaps; no new FRC-03 behavioural tests were run in this investigation.

| Scenario | Current evidence | Required next change |
|---|---|---|
| WS-01: E1 has projects; E2 empty | The previous `scoped.length ? scoped : variants` fallback is already removed. With no selection, `filteredVariants` still returns all variants. Listing is requested unscoped then filtered in the UI. | No selection returns `[]`; request the selected enterprise at the server boundary. Keep empty state separate from errors. |
| WS-02: no memberships | Empty enterprises disable create via missing selected enterprise, but there is no explicit administrator guidance. Enterprise selector fallback uses `enterprises[0]`, while selection is not reconciled against refreshed permissions. | Show “Нет доступных предприятий. Обратитесь к администратору”; no cached/demo enterprise; select only an actual authorized response item. |
| WS-03: new operator assignment | Enterprises load only in the mount effect. “Обновить” refreshes projects only. No trusted executable provisioning command was found; public enterprise creation and membership writes are intentionally 403. | Refresh enterprises too; add a documented trusted local provisioning operation using existing repository/transaction/config conventions. |
| WS-04: create 503 | Input is retained and navigation checks `state.error`, but `replaceProject(new draft)` happens before POST. The old current project can be replaced before successful creation. | Construct the proposed empty project without mutating current context; commit one replacement only after validated projectId/version. Reuse FRC-06 leave/save guard. |
| WS-05: late E1 reply | List store guards identity generation but has no enterprise/request generation. Enterprise change only changes local selection; compare selections/result are retained. | Key list results by enterprise and page; abort or generation-guard stale requests; clear selections/results/list state when context changes. |
| WS-06: 120+ projects | No project pagination controls; `listVariants()` uses backend default first page (50). Enterprise fetch uses limit 100 and drops total. | Forward enterpriseId/limit/offset; preserve totalItems; accessible page controls; test a later page and enterprise switch during an outstanding page request. |
| WS-07: missing/revoked project | Existing backend membership checks and FRC-02 access handling are reusable. Current workspace open action reads global activeVariantId after an async store action; FRC-06 changes may alter this contract. | Navigate only with that operation’s successful validated result; no old active project fallback. Pin final FRC-06 API before implementation. |
| WS-08: whitespace name | UI and current create handler turn blank trimmed name into “Новая конфигурация”. Backend checks only `name == ""`, not trimmed length 1…120. | Reject blank/>120 names before POST and at the backend create boundary; preserve input on failure. Define and test Unicode length consistently. |
| Ownership/orphans | Backend NULL-owned projects are inaccessible by ADR-0017. Current load store still contains enterprise fallback `project.enterpriseId ?? project.baseObject.id`. | Consume server enterpriseId only; missing enterprise is a protocol/orphan failure, not an implicit assignment. Recheck after FRC-06 finishes. |
| Comparison | Workspace uses all variants in compare selectors and keeps result across enterprise switches. It renders the legacy compare response. | Scope/reset selection now; do not implement FRC-08 comparison semantics during FRC-03. |

## Minimal implementation sequence after FRC-06 GO

- [ ] Confirm accepted FRC-06 interfaces for guarded navigation, successful create/open result, draft preservation and per-user storage. Coordinate exact ownership of `use-defense-variants-store.ts` and shared project store before editing.
- [ ] Add the small pure `workspace/domain/project-scope.ts` helper and test: `scopeProjects([{enterpriseId:'E1',projectId:'a'}], 'E2')` and a null enterprise both return `[]`; unrelated/null ownership is never adopted.
- [ ] Extend existing project list boundary to accept `{enterpriseId, limit, offset}` and retain `{items,totalItems}`. Keep the BFF thin. Add request-generation and pagination behaviour in the owning workspace/store layer without duplicating identity guards.
- [ ] Update existing workspace UI states and enterprise refresh. Persist selected enterprise under actual user identity only; revalidate persisted selection against authorized membership responses before using it. Changing enterprise resets comparison and pagination and uses the accepted FRC-06 guard.
- [ ] Make create atomic from the client’s perspective: trim/validate name, disable while pending, retain stable FRC-04 idempotency key for a repeated unchanged attempt, send empty workspace project with the chosen server enterprise/center, then replace context once using successful server projectId/version. A 503 must preserve old current project and form input.
- [ ] Add trusted enterprise provisioning described below; add no ordinary HTTP capability or role. Reuse existing membership-scoped APIs for the newly assigned user.
- [ ] Run synthetic integration and browser acceptance after implementation: E1 populated/E2 empty; no memberships; refresh after trusted assignment; create 503/blank; late E1 after E2; 120+ projects; revoke then open; dirty leave cancel/save/discard; missing enterprise rejected. Include first successful project through browser to actual Go/PostgreSQL.
- [ ] Record changed files, API examples, local evidence, rollback constraints and runtime limitations. No commit/push/deploy without the root release workflow.

## Operator provisioning boundary

ADR-0017 remains authoritative: membership does not grant enterprise creation, deletion or membership administration. There is no approved operator JWT role or admin HTTP API. FRC-03 should use a local trusted process requiring operating-system access and database credentials, as already used for the FRC-12 registry work mode.

Small proposed operation: validated name/address plus explicitly supplied finite latitude [-90,90], longitude [-180,180] and an existing member user UUID; construct `domain.NewEnterprise` with an explicit valid status and write enterprise+membership in one transaction using existing repositories. CLI input must distinguish omitted coordinates from a real zero. Missing user, invalid GIS input or membership write failure must leave no enterprise behind. Output identifiers only; do not print payloads/addresses/emails into general logs. Document invocation and verification through the normal user’s enterprise list; no developer SQL required. Shared main/config wiring remains root-owned and must be coordinated. Exact command/DTO is a proposed next implementation choice, not an already available command.

No new organization layer, RBAC, public-catalog administration, automatic geocoding, or orphan reassignment is planned. Membership/session audit remains deferred by ADR-0017; any additional audit scope needs an explicit release decision rather than an invented operator identity.

## Checkpoint and unresolved evidence

Backend authorization/list infrastructure appears reusable from inspected code and prior FRC-02 evidence. This investigation did not rerun those tests or perform onboarding. Production operator access, approved customer coordinates, deployed credentials, backup/retention and migration inventory are runtime concerns; local code cannot establish them. Stop here until the user resumes and root accepts FRC-06.
