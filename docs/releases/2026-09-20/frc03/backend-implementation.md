# FRC03 backend implementation and verification

Implemented on backend develop base `5ddc2ce58e5159a96069efabb2fa3250e02666cf`.
No new dependency, migration, public endpoint, admin role or manual SQL provisioning
procedure was added. No customer database or account was accessed.

## Operator contract

Run the existing application binary from the backend directory with
`ENVIRONMENT=dev`, `APP_WORK_MODE=enterprise-provision` and its ordinary `APP_DB_*`
configuration. Required flags:

```
--enterprise-id <stable UUID> --user-id <existing UUID>
--name <enterprise name> --address <address>
--latitude <explicit float> --longitude <explicit float>
```

Success is exit 0 with exactly `{ "enterpriseId": "…", "userId": "…" }` on
stdout. Failures have nonzero exit, no success JSON, and sanitized error text.
The repository suppresses SQL logging for this operation. The process emits its
ordinary environment/work-mode metadata to stderr. Full operator instructions,
including retry rules and configuration/migration behavior, are in
[`backend/README.md`](../../../../backend/README.md#первое-предприятие-доверенная-команда-оператора-frc03).

`application.ProvisionService` validates/canonicalizes IDs, trims the required
name/address and constructs an active domain Enterprise. Coordinate pointers
distinguish omission from explicit zero; domain bounds reject NaN/Infinity.
`EnterpriseProvisionRepository.Provision` creates the enterprise and initial
membership atomically, checks the existing user with a row lock, and relies on
the existing membership primary key. A membership insert failure rolls back the
enterprise. Stable enterprise IDs serialize concurrent attempts.

An existing ID returns success only when current enterprise values match and
that user's membership already exists. No existing row is updated and no absent
membership is adopted/restored. This is state-based safe replay, not a claim of
original operator-request provenance. A different UUID intentionally represents
a different enterprise; callers must retain the UUID across retries.

## Configuration-name boundary

One domain validator normalizes newly supplied configuration names by trimming
and counting Unicode code points, accepting 1–120. Application create/import/
rename paths use it; explicit empty HTTP rename is rejected. A schema-one import
without a separate `name` uses its existing `projectName` as the new configuration
label. Read constructors and historical snapshots are untouched. An unchanged
legacy label is retained during content save. Unknown project JSON fields remain
lossless; a wire-byte regression includes the integer `9007199254740993`.

## Verification

Run environment: macOS arm64, Go 1.26.0, PostgreSQL 16.13 (Homebrew). Go used
`GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache`.
Database checks exclusively used the owned disposable cluster
`127.0.0.1:55434`, role `fortis_test`. The user's services on 8090/3000 and
user databases were not touched.

| Evidence | Result |
| --- | --- |
| [Provisioning TDD red](backend-verification/tdd-red.log) | New checks fail because the operation did not exist |
| [Name-boundary TDD red](backend-verification/name-tdd-red.log) | Existing writes accepted blank/oversized names and empty rename |
| [Full Go tests](backend-verification/go-test.log) | `go test ./... -count=1`, exit 0 |
| [Go build](backend-verification/go-build.log) | `go build ./...`, exit 0 |
| [Operator binary build](backend-verification/operator-build.log) | `go build -o /private/tmp/frc03-backend-verification/fortis-operator ./cmd/app`, exit 0 |
| [Real PostgreSQL regression](backend-verification/postgres-regression.log) | 23 top-level tests PASS, no skips |
| [Actual binary invocation](backend-verification/actual-cli.log) | 9 CLI scenarios PASS with DB row/coordinate assertions |
| [Owned fixture cleanup](backend-verification/fixture-cleanup.log) | `/__stop` exits 0/PASS and removes only its generated database |

The build logs contain a nonfatal sandbox denial writing Go's module metadata
cache under `/Users/rr/go/pkg/mod/cache`; both build commands still exited 0 and
the produced executable was subsequently exercised.

PostgreSQL command:

```bash
FRC02_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' \
FORTIS_FRC04_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' \
go test ./cmd/app -run 'TestFRC0(2Postgres|3Postgres|4|5)' -count=1 -v -timeout=5m
```

FRC03 tests prove missing-user rollback; injected membership-write rollback;
eight concurrent retries yielding one enterprise/one membership; no-op retry
preserving persisted timestamps; no SQL input logging even with a verbose base
logger; changed payload/recipient conflict; retry cannot restore revoked access;
and configuration-name HTTP 400s without extra projects/revisions. Explicit zero
and boundary coordinates, NaN/Inf/range rejection, IDs, trimmed names/addresses
and sanitized failures also have unit coverage. Existing FRC02 ordinary-member
provisioning/membership denials and FRC04/05 revision/cost tests remain green.

The actual executable checks used only the first stopped disposable browser DB
before cleanup. Cases: both coordinates omitted, longitude omitted, NaN,
Infinity, out-of-range, missing user, explicit-zero creation, exact retry and
changed-data conflict. Success yielded enterprise
`bb4cb918-0de7-4cac-83cd-acfb2e4bd434`, user
`ea27db05-9047-4c5e-9673-3f209165924b`; one enterprise/one membership and `(0,0)`
were confirmed from that test database. Its exact database was then dropped and
absence verified. Logs contain synthetic identifiers only.

## Vertical fixture isolation

`cmd/app/frc03_browser_test.go` is an opt-in test-only 8092 server using the
production DI/getWepApp path. It creates `frc03_browser_<UUID>` as a separate
database on the disposable cluster, applies normal migrations/tracker, registers
two synthetic users and asserts zero enterprises/memberships/projects. The real
operator CLI uses the same ordinary database config via a temporary JSON env
file. Browser provisioning is performed through the executable; fixture routes
only expose synthetic metadata and stop the test.

The runtime migration driver can retain a leased database connection after the
application pool is closed. The final fixture therefore drops only its own
generated database with `WITH (FORCE)` after HTTP shutdown. Earlier attempts
were stopped and their exact disposable databases removed manually after process
exit; no generic name-pattern deletion was used. The active final browser run,
its screenshots and subsequent cleanup are recorded by the root acceptance run.

The existing runtime DSN builder does not quote an empty password; this makes
the next `dbname` token parse incorrectly. The test uses an explicit synthetic
password with the disposable trust-authenticated cluster. No runtime connection
configuration was changed for this feature.
