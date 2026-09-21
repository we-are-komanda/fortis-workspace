# FRC-03 implementation report

Date: 2026-09-21. **PASS for local staged FRC-03 and its separate real vertical gate.** This is not whole-release or production acceptance. Entry baseline: accepted FRC-06, frontend `a56d128`, parent `0560b79`.

Authority: [FRC-03 specification](../../../fortis-release-specs/specs/FRC-03_workspace.md), [research checkpoint](research-checkpoint.md), [independent acceptance plan](acceptance-plan.md). The [criterion matrix](acceptance-criteria.md) separates tested behavior from the remaining integration gate; the [file inventory](changed-files.md) identifies each owning repository.

## Resulting behavior

The workspace requests projects with the selected authorized `enterpriseId`, `limit=50` and page offset, and displays the matching server total. E2 with no projects stays empty even when E1 has projects. A user without memberships receives administrator guidance and cannot create. Refresh reads the enterprise list again and reloads the authorized project scope. The enterprise reader consumes all pages rather than silently stopping at 100 items. A remembered choice is stored under the authenticated identity and admitted only after a fresh membership-scoped enterprise response.

Enterprise, page and session request generations prevent an obsolete list result from replacing the current list. Enterprise switching resets page and comparison state. Loading, authorized empty, transport failure and forbidden states have different rendered outcomes. The existing variants dialog also displays its independent list error instead of claiming that no saved variants exist.

Creation builds a proposed empty project without replacing the current project, saved baseline or active variant. The existing FRC-06 save preparation and transport functions freeze the proposal body and idempotency key. An unchanged manual retry reuses them. Only a valid server acknowledgement commits the new project context; failed or pending creation retains the old context and typed name. An identity or current-project change prevents a late acknowledgement or subsequent list refresh from authorizing navigation. Names are trimmed and validated as 1–120 Unicode code points in the workspace, save boundary, recovery metadata and backend write paths; 120 non-BMP characters remain intact.

Backend-loaded projects require explicit enterprise ownership and a positive integral revision. The save payload no longer infers ownership from `baseObject.id`. Existing orphan isolation remains in force. API loading still supplies the authoritative data needed by FRC-06 ambiguous-update verification; the store rejects a different requested project before installing it.

The real first-project exploration found that an empty map had no way to add its first layer because the layer panel required an existing selected layer. The existing map component now exposes the first-layer action in its empty state and reuses the existing layer creation flow. Root's real harness exercises that path, Save to revision 2 and reload; the final clean-start gate passed; see the final evidence addendum below.

## Trusted operator onboarding

The backend adds a local `enterprise-provision` command in the existing application. It accepts an existing user UUID, a stable enterprise UUID, name, address and explicitly supplied latitude/longitude. It validates finite GIS coordinates and distinguishes omitted coordinates from valid `(0,0)`. The application service and existing enterprise repository commit the enterprise and membership in one transaction.

Exact retries with the same normalized data and user return the same identifiers without duplicate writes. Changed details or recipient, an unrelated existing ID, or revoked membership fail without adopting or restoring access. The existing membership key is reused; no new schema, public administration endpoint, JWT role, tenant model or onboarding wizard is introduced. The command prints identifiers only and suppresses sensitive database error details. Operation and rollback guidance live in the [backend README](../../../../backend/README.md); [ADR-0022](../../../../knowledge-base/03_Architecture/ADR-0022-trusted-enterprise-provisioning.md) records the boundary.

## Evidence and verification boundary

| Check | Observed evidence | Current interpretation |
|---|---|---|
| Rendered FRC-03 workspace | [14/14 Chromium checks](browser-independent-14.log), [command](browser-independent-14.command.json) | PASS for real React UI with synthetic intercepted transport; not database evidence. |
| Focused workspace domain/API | [9/9 checks](verification-logs/focused-03.log) | PASS for scoped list, atomic creation, retry, identity/context races, ownership and GIS validation. |
| Operator CLI/application | [independent unit run](operator-independent-unit.log) | PASS; explicit coordinates, input boundaries and safe result/error behavior. |
| Real PostgreSQL operator/name tests | [independent database run](verification-logs/postgres-independent.log) | PASS for transaction rollback, eight concurrent exact retries, immutable retry behavior, changed-recipient conflict, revoked membership and configuration-name writes. |
| Actual operator executable | [9 CLI scenarios](backend-verification/actual-cli.log), [backend implementation/evidence](backend-implementation.md) | PASS with real disposable database row/coordinate assertions, including omitted coordinates, invalid values, missing user, explicit zero, exact retry and changed-data conflict. |
| Backend suite/build | [final suite](verification-logs/backend-tests-final.log), [final build](verification-logs/backend-build-final.log) and adjacent command JSON | PASS on recorded backend source manifest. Opt-in tests are separately evidenced above. |
| Combined FRC-03/FRC-06 browser run | [27/27, no skips](verification-logs/browser-03-06-final.log) | PASS after honest scoped-list fixture repair; 14 workspace and 13 accepted save/recovery cases. |
| Focused accepted regressions | [87 pass, 0 fail, 1 opt-in skip](verification-logs/regression-01-02-04-06-final.log) | PASS for executed checks; skipped real-export probe is not counted as a pass. |
| Malformed workspace CREATE acknowledgement | [5-case independent probe](verification-logs/malformed-create-probe.log), [runnable source](verification-logs/malformed-create-probe.ts) | PASS: empty ID, missing/zero/fractional version and wrong enterprise preserve prior context and frozen attempt. |
| Changed-file lint / TypeScript / production build | [lint command](verification-logs/changed-lint-final.command.json), [typecheck command](verification-logs/typecheck-final.command.json), [build command](verification-logs/build-final.command.json) | All exit 0. [Source consistency](verification-logs/source-consistency.json) confirms no production drift and identical FE build/test manifests; the separately amended live harness has its [own final lint](verification-logs/live-harness-final-lint.command.json). |
| Frontend full suite | [274 total: 211 pass, 6 fail, 57 skip](verification-logs/full-suite-final.log), [six exact baseline signatures](verification-logs/baseline-signatures.json) | No new failure signature. Exit remains 1; this is not a green whole suite and skips do not count as passes. |
| Clean-start Next → Go → PostgreSQL browser gate | Root owns [frc03-live.cjs](../../../../frontend/test/playwright/frc03-live.cjs); final durable result not yet supplied | **PENDING**. Must establish new user → no membership → trusted assignment → Refresh → create v1 → edit → Save v2 → reload, plus real scoped pagination. |

The RED/green history is retained in [initial corrected browser failures](browser-independent-red.log), [shared dialog list-error RED](shared-list-error-red.log), and [14-check green run](browser-independent-14.log). The initial selector failures are test-harness failures, not product defects. Independent review also reproduced a stale create navigation result after identity changed during list refresh; the permanent workspace unit test now expects no navigation result. Historical test fixtures were amended to declare explicit enterprise ownership and honor server list filters, retaining their behavioral assertions.

The six unchanged full-suite failures are `catalog-sidebar-motion-contract`, `map-zoom-controls-contract`, `prototype-3d-placeholder-contract`, `retrospective-analysis-navigation-contract`, `user-facing-copy-contract`, and `defense-project`. Exact assertion signatures are preserved in the linked comparison. Browser/PostgreSQL opt-in skips do not count as passes.

## Scope retained

No new dependency, model, schema migration, SQL provisioning workflow or duplicate save implementation was added. The proposed standalone `project-scope` helper was unnecessary: the existing UI filter and server query are covered directly by domain and rendered tests. Production deployment, operational ownership, TLS, backups and release gate FRC-14 remain outside this local stage.

SAVE-09 remains **NOT APPLICABLE to the currently gated official-report runtime**, with mandatory implementation and acceptance under FRC-10 after its prerequisites. FRC-03 does not claim an official-report pass or change the accepted FRC-06 record. Whole-release acceptance remains open.

## Final real gate and auth follow-up

[Real result](real-vertical/result.json) passed all7 checkpoints on disposable database `frc03_browser_90a2153f861046739ae3c40cc278a2d4`, Next3111 and Go8092. Project `1399fcab-3947-4422-9d80-526089ce2a95` progressed1→2 after the normal layer wizard and manual Save; reload and relogin preserve the entire canonical GET, hash `e1d571cff7f0c829a3cb79a1e9c365918d93fe111822ee28f5b0595dfc30b3c2`. Pagination reaches121 rows; empty second enterprise has none; user B receives no rows and404 for A's project. No endpoint mocks or store injection. Console errors and page errors are both empty;27 rendering/driver warnings are retained in the result.

The real gate found redundant auth/me401 calls after logout. IdentityBoundary now skips verification of a known invalid session. Successful login and registration use `beginSessionVerification()` to clear the prior identity and customer stores while marking the new cookie session unverified, allowing the normal authoritative auth/me check. Initial unauthenticated access still redirects on its first401. Two rendered RED→GREEN tests and an identity-store regression cover the distinction; root reviewed the follow-up after the independent agents reached their usage limit.

Final verification supersedes the earlier counts above:29/29 browser,277 full tests=212PASS/6 exact historicalFAIL/59opt-inSKIP, types/lint/isolated production buildPASS. See `verification-logs/*auth-final*`;304 source/test/toolchain hashes have zero drift. An initial parallel browser run had one3second locator timeout; the isolated affected scenario and full sequential29-test repeat pass without weakening the assertion. No new failures remain.

Local accepted child commits: frontend `e49253bc33d4e7c518b27fc55dbb92405d7c456e`, backend `5a4a6d5176d9602a1a8c548f9bd1b44a41f933c1`, knowledge-base `4cd6ff1335a85d78b959f5bb74488201fcb8244d`. Parent pointer/evidence commit follows; no push.
