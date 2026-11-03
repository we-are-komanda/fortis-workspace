# FRC-10 backend verification

Status: local focused/full Go tests and build pass; actual PostgreSQL acceptance is pending execution by the parent task. The subagent's escalated PostgreSQL command was not executed because automatic approval review could not refresh the account token after an account change. This was an approval-system authentication failure, not a failed PostgreSQL test or unsafe-action determination.

## Runnable checks

From `backend/`, use existing installed Go with `GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache`.

```sh
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache go test ./internal/modules/report/... -count=1 -v
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache go test ./... -count=1
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache go build ./...
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache FORTIS_FRC04_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' go test ./cmd/app -run '^TestFRC10Postgres' -count=1 -v
```

The opt-in PostgreSQL helper creates a fresh uniquely named schema, runs migrations there, and drops only that schema. Port 55434 is the existing disposable cluster. User databases on port 5432 and services on 8090/3000 are outside scope.

## Evidence and cases

- Unit RED: `TestReportNeverInventsMalformedGeometry` failed because a null latitude was silently decoded as zero. A second RED caught missing polygon point arrays being turned into empty geometry. Required-coordinate/point-array decoding fixed both; explicit empty arrays remain preserved. The complete report package passes. The concise observed RED transcript is in `backend-verification-logs/mapper-red.log`.
- Application tests: hidden mode never calls finance; authorization precedes cache/finance; persisted priced reports bypass unavailable calculators; report-ID reopen bypasses project loading and propagates current-access denial.
- Transport/mapper tests: strict/mixed/duplicate query modes; separate hidden-cost allowlist; nested financial/URL/document sentinels absent; plain-text caveat preserved; polygon/freeform coordinates and zero positions retained; all/saved visibility keeps full inventory; malformed geometry and URL styles rejected; safe RGB styles and empty arrays preserved.
- PostgreSQL suite (pending actual run): immutable report reuse/reopen, pinned name/cost/budget identity, catalog/current-version independence, update trigger, cascade deletion; hidden unsupported calculator and sentinel exclusion; inserted report/audit rollback; ordinary foreign-user and revoked access; revocation between rendering and commit; eight concurrent requests produce one report/audit; reopen does not query revisions/cost cache; membership revocation waits behind issuance locks.

Final local focused/full Go test runs and build exited 0. Logs are retained as `backend-verification-logs/report-unit.log`, `go-test.log`, and `go-build.log`. Build may emit an existing nonfatal module stat-cache write warning under the sandbox. No database test is counted as passed solely because an opt-in test skipped.
