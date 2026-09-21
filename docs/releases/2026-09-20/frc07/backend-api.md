# FRC07 backend contract

Status: implemented; backend tests pass. The approved FRC07 amendment supersedes the older proposal that rejected lowering a limit below current spend.

All routes require the current authenticated user's enterprise membership. `projectId` is preferred; `id` is a compatible alias. Conflicting aliases return 400. Missing or inaccessible projects return 404 before financial details.

## Read a saved budget

`GET /api/v1/projects/budget?projectId=P&projectVersion=V`

Omitting `projectVersion` resolves the current immutable revision once. The response is:

```json
{"identity":{"projectId":"P","projectVersion":2,"calculationVersion":"cost-rub-v1","snapshotDigest":"sha256","inputDataVersions":{}},"config":{"budgetMode":"limited","budgetLimitMinor":"50000000"},"spentMinor":"47500000","remainingMinor":"2500000","status":"within_limit"}
```

Amounts are exact decimal strings in RUB kopecks, with `null` for unknown values. `status` is `within_limit`, `exceeded`, `unlimited`, or `indeterminate`. An incomplete cost is indeterminate even in unlimited mode; remaining is null. Known overage retains a negative remaining amount.

## Change configuration

`PUT /api/v1/projects/budget?projectId=P`

```json
{"version":2,"budgetMode":"limited","budgetLimitMinor":"50000000"}
```

For unlimited mode the limit must be explicitly `null`; for limited mode it must be a nonnegative integer string. Zero is valid. Omission, JSON numbers, negative/decimal/exponent/non-finite text are rejected. The total budget has no unit-price cap. Version is the shared positive project version.

The response contains the existing complete canonical `ProjectResponse` (`projectId`, `name`, `enterpriseId`, `projectName`, `version`, `projectVersion`, `snapshotDigest`, `snapshot`, `updatedAt`) plus `budget` with the projection above. Snapshot and projection identify the new committed version.

A configuration change may lower the limit below current spend or set a limit while current cost is incomplete. It leaves project composition unchanged, creates a revision and audit event, and uses the same transaction/version as project updates.

## Check a full candidate

`POST /api/v1/projects/budget/check?projectId=P`

```json
{"version":2,"projectJson":"<complete schemaVersion=1 candidate JSON>"}
```

```json
{"basedOn":{"projectId":"P","projectVersion":2},"status":"blocked","reasonCode":"budget_exceeded","projectedSpentMinor":"50000001","projectedRemainingMinor":"-1"}
```

Valid checks return 200 with `allowed` or `blocked`. Reasons are `within_budget`, `unlimited`, `non_increasing_overage`, `budget_exceeded`, and `price_unknown`. Checks do not write a projection cache, reserve money, change the project, or create a revision/audit event. Stale versions return 409.

All actual project writes independently evaluate the candidate after locking the current project and membership. Limited incomplete candidates return 422 `price_unknown`. Known candidates at or below the limit pass. When both current and candidate cost are known, a candidate no more expensive than current cost may remain over limit (`non_increasing_overage`). A known over-limit candidate against an unknown current cost returns 422 `budget_exceeded` because non-increase cannot be established. Unlimited mode allows incomplete prices but does not fabricate zero cost. Invalid selected financial data returns its existing 400 financial validation error.

Write refusals use the existing error envelope with exact details:

```json
{"error":{"code":"budget_exceeded","message":"Candidate does not satisfy the project budget","requestId":"request-uuid","retryable":false,"details":{"field":"budgetLimitMinor","objectIds":[],"budgetLimitMinor":"50000000","projectedSpentMinor":"50000001","projectedRemainingMinor":"-1","currentSpentMinor":"47500000"}}}
```

For unknown prices, the field is `placedObjects`, objectIds identifies the unknown objects, and unknown amounts are null. These details are available only after authorization.

## New, imported, and copied projects

New projects and imports always receive authoritative `{ "budgetMode":"unlimited", "budgetLimitMinor":null }`. Embedded budget fields remain untrusted document data and never configure the server budget. Import also ignores a top-level `budgetSource`.

Only `POST /api/v1/projects` accepts optional top-level `budgetSource: {projectId, projectVersion}`. It copies the budget from that exact accessible immutable source revision. The source must still exist and remain accessible, including during replay. The transaction locks the source project and membership, and the source reference participates in the create idempotency digest. Changing the reference under the same key returns 409. The new independent project has no existing-overage exemption: its candidate must fit the copied limit and have complete prices when limited.

## Persistence compatibility

No migration or dependency is added. The existing JSONB budget row and revision envelope hold canonical `budgetMode` and `budgetLimitMinor`. Historical null budgets mean unlimited. Historical `budgetAmountMln` is read from its JSON decimal using exact rational arithmetic and half-up conversion to kopecks; canonical field presence takes precedence, including explicit null. Successful subsequent writes store canonical values without rewriting historical revisions. The legacy decimal parser bounds input/exponent magnitude to 10,000 to prevent pathological allocations; this is not a financial amount cap.

The old unversioned application budget write fails closed with `version_required`. Public JWT roles, endpoint access, and enterprise provisioning are unchanged.

Future algorithm rollout prerequisite: the current release writes only `cost-rub-v1`. Before introducing another calculator binding, the overage baseline must dispatch the saved current revision’s binding or treat unsupported baseline cost as unknown; it must not grant an exemption using a different calculator. Pinned projection reads already reject unsupported bindings.
