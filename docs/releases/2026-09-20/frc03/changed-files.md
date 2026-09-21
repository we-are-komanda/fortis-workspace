# FRC-03 changed files

Date: 2026-09-21. Working-tree inventory relative to accepted FRC-06 (`frontend a56d128`, parent `0560b79`). Final commit IDs and parent submodule pointers remain pending stage acceptance. This inventory describes changes; it is not a verification result.

## Frontend

| Files | Purpose |
|---|---|
| [project-workspace-page.tsx](../../../../frontend/src/modules/workspace/ui/project-workspace-page.tsx) | Scoped Refresh, all enterprise pages, identity-scoped remembered selection, 50-item project pagination, distinct states, Unicode name validation and atomic creation through the existing save pipeline. |
| [enterprise-api.ts](../../../../frontend/src/modules/drone-defense/infra/enterprise-api.ts) | Preserve enterprise totals; require explicit finite in-range coordinates while allowing zero. |
| [api-client.ts](../../../../frontend/src/modules/drone-defense/infra/api-client.ts) | Project list query/total validation, explicit loaded ownership/version, remove base-object ownership inference from save payloads. |
| [use-defense-variants-store.ts](../../../../frontend/src/modules/drone-defense/domain/use-defense-variants-store.ts) | Query-aware list generation and errors, staged workspace create attempt, frozen retry, authoritative commit and late-result guards. |
| [variants-modal.tsx](../../../../frontend/src/modules/drone-defense/ui/variants-modal.tsx) | Surface independent list failure without false empty success; use supported Ant Design Alert `title` prop. |
| [drone-defense-prototype.tsx](../../../../frontend/src/modules/drone-defense/ui/drone-defense-prototype.tsx) | Reachable first-layer action for an empty first project, reusing the existing layer workflow. |
| [project-draft-storage.ts](../../../../frontend/src/shared/lib/project-draft-storage.ts) | Match the Unicode code-point name boundary when validating recovery attempts. |
| [workspace-projects.test.ts](../../../../frontend/src/modules/workspace/domain/workspace-projects.test.ts), [project-workspace.browser.test.ts](../../../../frontend/src/modules/workspace/ui/project-workspace.browser.test.ts) | New focused contract and independent rendered acceptance tests, including atomic failure/retry, pagination, stale responses, identities and Unicode. |
| [project-draft-storage.test.ts](../../../../frontend/src/shared/lib/project-draft-storage.test.ts) | Persistent recovery name boundary regression. |
| [use-defense-variants-store.test.ts](../../../../frontend/src/modules/drone-defense/domain/use-defense-variants-store.test.ts), [project-revisions.release.test.ts](../../../../frontend/src/modules/drone-defense/infra/project-revisions.release.test.ts), [project-runtime.release.test.ts](../../../../frontend/src/shared/lib/project-runtime.release.test.ts), [project-recovery.browser.test.ts](../../../../frontend/src/modules/drone-defense/ui/project-recovery.browser.test.ts) | Honest authorized fixture ownership and scoped-list transport behavior; existing assertions retained. |
| [frc03-live.cjs](../../../../frontend/test/playwright/frc03-live.cjs) | Actual Next/Go/PostgreSQL browser acceptance harness with isolated synthetic users and data. |

## Backend

| Files | Purpose |
|---|---|
| [main.go](../../../../backend/cmd/app/main.go), [dependencies.go](../../../../backend/cmd/app/dependencies.go) | Dispatch and wire the local trusted provisioning command through existing application boundaries. |
| [commands.go](../../../../backend/internal/modules/enterprise/application/commands.go), [provision.go](../../../../backend/internal/modules/enterprise/application/provision.go) | Validated provisioning input and use case; safe result and failure messages. |
| [enterprise_provision_repository.go — domain](../../../../backend/internal/modules/enterprise/domain/enterprise_provision_repository.go), [enterprise_provision_repository.go — infrastructure](../../../../backend/internal/modules/enterprise/infrastructure/enterprise_provision_repository.go) | Existing enterprise/member transaction with exact-retry, concurrency and conflict behavior. |
| [provision.go — CLI](../../../../backend/internal/modules/enterprise/ui/provision.go), [enterprise DTO](../../../../backend/internal/modules/enterprise/ui/dto.go) | Explicit coordinate presence and identifier-only command output. |
| [project service](../../../../backend/internal/modules/defense_project/application/defense_project_service.go), [name value validation](../../../../backend/internal/modules/defense_project/domain/vo.go), [domain errors](../../../../backend/internal/modules/defense_project/domain/defense_project_errors.go), [controller](../../../../backend/internal/modules/defense_project/ui/controller.go), [project DTO](../../../../backend/internal/modules/defense_project/ui/dto.go) | Trimmed 1–120-code-point names at create/update/import write boundaries without changing historical read constructors. |
| [application provisioning tests](../../../../backend/internal/modules/enterprise/application/provision_test.go), [CLI tests](../../../../backend/internal/modules/enterprise/ui/provision_test.go), [name application tests](../../../../backend/internal/modules/defense_project/application/config_name_test.go), [domain error tests](../../../../backend/internal/modules/defense_project/domain/defense_project_errors_test.go) | Validation and error-boundary checks. |
| [frc03_access_test.go](../../../../backend/cmd/app/frc03_access_test.go), [frc03_postgres_test.go](../../../../backend/cmd/app/frc03_postgres_test.go), [frc03_browser_test.go](../../../../backend/cmd/app/frc03_browser_test.go) | HTTP name checks, real PostgreSQL rollback/retry/name evidence and isolated live browser server. |
| [README.md](../../../../backend/README.md) | Trusted operator command, retry and operational guidance. |

## Knowledge base and coordination

| Files | Purpose |
|---|---|
| [ADR-0022](../../../../knowledge-base/03_Architecture/ADR-0022-trusted-enterprise-provisioning.md), [KB index](../../../../knowledge-base/00_Index.md) | Durable operator boundary, coordinate rules and exact-retry contract. |
| [research checkpoint](research-checkpoint.md), [recovery checkpoint](recovery-checkpoint.md), [acceptance plan](acceptance-plan.md), [implementation report](implementation-report.md), [acceptance criteria](acceptance-criteria.md), this inventory | Stage rationale, file ownership, behavior and evidence limits. |
| Browser/operator logs and `verification-logs/` source manifests, commands and output | Reproducible independent verification; preliminary failures retained rather than rewritten as passes. |

[Backend implementation and evidence](backend-implementation.md), `backend-verification/`, and the independent runnable probes in `verification-logs/` complete the supporting inventory. Final real-browser artifacts remain pending root's clean-start run. Accepted FRC-06 documentation is unchanged. No migration file or dependency/lockfile change is part of this stage.

## Final real-gate follow-up

`frontend/src/shared/ui/identity-boundary.tsx` skips requests for an already invalid session. `frontend/src/shared/lib/session-state.ts` adds explicit session-verification reset, used by `frontend/src/modules/auth/ui/login-page.tsx` and `register-page.tsx` after successful authentication. `identity-isolation.release.test.ts` and the existing recovery browser fixture cover cleared prior identity, first401 and no redundant logout checks. The real harness now rejects all console errors. Final result/screenshots are in `real-vertical/`; final root test/build evidence in `verification-logs/*auth-final*`. These additions supersede the earlier pending statements.

Local accepted child commits: frontend `e49253bc33d4e7c518b27fc55dbb92405d7c456e`, backend `5a4a6d5176d9602a1a8c548f9bd1b44a41f933c1`, knowledge-base `4cd6ff1335a85d78b959f5bb74488201fcb8244d`. Parent pointer/evidence commit follows; no push.
