# FRC-03 — test evidence, 2026-09-21

Entry: frontend `a56d128e715ed09387428ad3dd67434d18855dd5`, backend `5ddc2ce58e5159a96069efabb2fa3250e02666cf`, parent `0560b791d7971869cb7d708dc1fdc5e21715d2a3`. This is local candidate evidence; production is not deployed.

| Check | Result | Evidence |
|---|---|---|
| FRC03 store/API cases | 9 PASS | `verification-logs/focused-03*` |
| Independent rendered FRC03 + accepted FRC06 browser regressions | 27/27 PASS (14+13) | `verification-logs/browser-03-06*` |
| Frontend FRC01/02/04/06 regressions | 87 PASS, 1 explicit PostgreSQL skip | `verification-logs/regression-01-02-04-06*`; actual PostgreSQL separately below |
| Full frontend suite | 274 tests: 211 PASS, 6 historical FAIL, 57 opt-in SKIP | `verification-logs/full-suite*`; exact historical signature comparison is mandatory |
| Typecheck / changed-file lint / production build | PASS | `verification-logs/typecheck*`, `changed-lint*`, `build*`; source manifest consistency recorded by reviewer |
| Backend normal suite and build | PASS | `verification-logs/backend-tests-final*`, `backend-build-final*` |
| Real PostgreSQL regression group | 23 top-level PASS | `backend-verification/postgres-regression.log` |
| Independent provisioning PostgreSQL | 3 top-level + 6 nested PASS | `verification-logs/postgres-independent*` |
| Actual built operator CLI | PASS for validation/no writes, explicit zero, replay, conflict, identifier-only output | `backend-verification/actual-cli.log` |
| Independent core review | Stale create return after identity switch and hidden variants-list error fixed; empty first-layer CTA reviewed | Reviewer closure record; root actual browser below |
| Real Next→Go→PostgreSQL clean-start vertical gate | PASS | [7 checkpoints, zero console/page errors](real-vertical/result.json); all earlier interim attempts below retained as history |

## Real browser findings

The stack uses Next3111, Go test server8092 and a uniquely named disposable `frc03_browser_*` database on PostgreSQL16 loopback55434. The actual application DI/router/migrations and actual built local operator executable share that database. No project endpoint is mocked, no browser store is injected, and user's database5432/services8090/3000/root/root2 are untouched.

Initial run proved honest no-membership UI, actual CLI provisioning, Refresh and first creation through the normal UI with authoritative ID/version1. It found an actual blocker: empty `layers=[]` made the Add-layer button unreachable because its panel required `selectedLayer`. The root fix adds an empty-state button calling the existing layer wizard; a real follow-up run proved wizard edit → Save v2 → reload with the same layer/identity.

Two harness corrections are explicit: the visible new button includes its decorative icon in accessible name, so the stable role/name selector matches the `Добавить эшелон` suffix; Next development hydration exceeded Playwright expect's default5seconds once, and the screenshot already showed correct v2. The harness now uses30seconds for both actions and expectations. Neither correction bypasses UI or weakens identity/content assertions. Full clean-start evidence must still pass all checkpoints, including121 real project rows, empty E2 and B isolation.

## Honest regression fixture updates

Existing runtime retry fixture lacked explicit enterpriseId and now correctly failed closed before writing. Existing FRC06 browser list fixture ignored the new server enterprise filter and returned E rows for F. Fixtures now supply explicit ownership and apply server filtering/pagination; original behavior assertions are retained. These were investigated as new failures, not labelled historical.

Project-name boundary tests enforce writes at trim1…120 Unicode code points and preserve restoration of historical snapshots. The PostgreSQL raw-JSON assertion uses exact wire bytes instead of decoding an unknown integer extension through float64, which would round the test value. Six unrelated historical frontend assertion/exception/stack signatures are compared separately; full suite is not described as green.

## Reproduction

From frontend with the dedicated fixture running and its private synthetic environment JSON prepared:

```sh
rtk proxy env FRC03_BROWSER_TESTS=true FRC06_BROWSER_TESTS=true node --import tsx --test src/modules/workspace/ui/project-workspace.browser.test.ts src/modules/drone-defense/ui/project-recovery.browser.test.ts
rtk proxy env FRC03_OPERATOR_BINARY=/private/tmp/frc03-backend-verification/fortis-operator FRC03_OPERATOR_ENV_FILE=/private/tmp/frc03-backend-verification/operator-env.json node test/playwright/frc03-live.cjs
```

Exact full-suite, build and backend command arrays/exit codes are stored next to raw logs. Browser and database opt-in skips are never counted as passes. Production operator ownership/TLS/artifact/backup/rollback/storage and other FRC14 gates remain unproven.

## Accepted final evidence

Local FRC03 and separate vertical gate: **PASS**. [Real result and screenshots](real-vertical/result.json); [real log](verification-logs/real-vertical.log). Same project `1399fcab-3947-4422-9d80-526089ce2a95`, versions1→2; full saved content preserved after reload/relogin. Actual operator CLI,121 real rows, empty E2 and B isolation all passed.

A real logout request race was fixed in the common identity boundary. Successful login/register explicitly reset to an unverified session; known invalid sessions no longer refetch auth/me. [RED](verification-logs/logout-red.log), [29/29 final browser](verification-logs/browser-auth-final.log), [full277=212PASS/6FAIL/59SKIP](verification-logs/full-suite-auth-final.log), [exact6/6 historical signatures](verification-logs/baseline-signatures-auth-final.json). Types, lint and isolated production build exit0 (`*-auth-final.command.json`). [304 source/test/toolchain hashes match](verification-logs/auth-final-source-consistency.json). The final production changes were root-reviewed after independent agents became unavailable due to usage limits; earlier independent review remains valid for its recorded source.

The real gate preserves27 warnings from WebGL driver/map labels/style evaluation; none are console errors or application assertions. They are disclosed, not filtered into fake absence. The console gate now rejects every error message, with no broad404/deprecation exception.
