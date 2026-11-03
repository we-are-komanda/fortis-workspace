# FRC07 backend verification

Environment: Go 1.26.0, PostgreSQL 16.13 (Homebrew), disposable loopback port 55434. Test databases/schemas use only synthetic identities and project data. The existing `frc04Database` helper creates a unique `frc04_<uuid>` schema and drops it at cleanup; FRC02 has its own unique schema helper. User databases and services on 5432/8090/3000 were not used.

## Results

- TDD RED: new exact-budget domain APIs did not exist; initial real PostgreSQL tests failed against the old budget query/response contract. Logs retained.
- Pure exact-budget and legacy-document cases: GREEN (also included in full Go tests).
- `go test ./...`: PASS. Opt-in PostgreSQL tests skip without their DSNs; the separate run below actually executes them.
- Final budget controller subset after removing unused test mock methods: PASS.
- `go build ./...`: PASS, exit 0 (empty success log).
- Real PostgreSQL FRC02/03/04/05/07 regression: PASS, 26 top-level tests plus 20 subcases. Includes five new FRC07 top-level tests and three injected transactional failure subcases. No skipped tests in this selected run.

## Reproduction

From `backend/`:

```sh
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache go test ./...
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache go build ./...
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache FORTIS_FRC04_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' FRC02_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' go test ./cmd/app -run '^TestFRC0[23457]Postgres' -count=1 -v
```

Focused cases live in `backend/cmd/app/frc07_postgres_test.go`; use `-run '^TestFRC07Postgres'` for that subset. They assert exact equality and +1 kopeck overage, null unknown cost, zero limits, validation, read-only checks/no cache writes, stale versions, foreign membership isolation, authoritative clone/import behavior, idempotent replay/source identity, current and historical snapshots, same-version concurrent edits, and rollback of project/budget/revision/audit writes. Budget changes and composition updates contend for the same row/version; one succeeds and one returns version conflict.

Evidence: [backend-verification-logs/](backend-verification-logs/). No browser acceptance claim is made from these Go tests; the parent task records the real Next→Go→PostgreSQL run separately. Swagger generation was not run because the generator is not installed; affected source DTO/route comments and [backend-api.md](backend-api.md) document the actual contract.
