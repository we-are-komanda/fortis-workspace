# FRC08 backend verification

Environment: Go 1.26.0 and PostgreSQL 16.13 (Homebrew). Database tests use synthetic fixtures in automatically created/dropped unique schemas on the authorized disposable loopback cluster 127.0.0.1:55434. User databases and services on 5432/8090/3000 were not accessed.

Results:

- TDD RED: exact comparison domain constructors were absent; initial PostgreSQL A7/B3 failed against the old id1/id2 mutable query contract. Logs retained.
- Domain GREEN: exact positive/negative difference, unknown totals, A=0, ±0.005 percent rounding, negative-zero normalization, and a one-kopeck difference at total 10^21.
- `go test ./...`: PASS. This command skips opt-in database tests without DSNs; the explicit run below actually executes them.
- `go build ./...`: PASS (empty success log).
- PostgreSQL FRC02/03/04/05/07/08 regression: PASS, 29 top-level tests and 20 subcases, no selected skips. Three new FRC08 suites pass.
- `git diff --check`: PASS.

From `backend/`:

```sh
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache go test ./...
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache go build ./...
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc12-gocache FORTIS_FRC04_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' FRC02_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' go test ./cmd/app -run '^TestFRC0[234578]Postgres' -count=1 -v
```

Focused DB command uses `-run '^TestFRC08Postgres'`. Tests are in `cmd/app/frc08_postgres_test.go`:

| Test | Behavioral evidence |
|---|---|
| PinnedComparison | Real persisted A7/B3: 47500000/55000000, delta 7500000/15.79%; frozen names/budgets/identities; unchanged response after A8/catalog edit; same-ID distinct revisions; identical ref →400. Query counters prove one current authorization and one immutable revision read per side, no mutable budget/catalog lookup. |
| UnknownZeroAndAccess | A=0 and unknown null semantics; both foreign-side orders →404; no partial data/cache materialization before both authorized; accessible different enterprises →400; missing revision →404; aliases, required versions and malformed queries; same-JWT revocation →404. |
| IdentityAndProvenance | Same display names with different IDs remain separate; frozen source labels and provenance warnings; stable repeated response; unavailable calculator →503 without partial financial response. |

Evidence files: [backend-verification-logs/](backend-verification-logs/). The final large-total case was added after the full suite and rerun in the focused domain suite; production source was unchanged. API DTO/route annotations were updated; Swagger generation was not run because its generator is not installed. No browser acceptance claim is inferred from Go tests.
