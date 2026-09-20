# FRC-05 backend evidence — 2026-09-20

Scope: canonical RUB cost from immutable project revisions. Parent authorized this slice after FRC-04 CODE PASS / RUNTIME BLOCKED. Backend baseline remains `b04696d87b5a5a085c9c5cc4eda1e7dacff8af12`; changes are uncommitted. No deployment, production migration, dependency addition, commit or push.

## Accepted interface and implementation

GET `/api/v1/projects/cost?projectId=P&projectVersion=V` returns the shared CostProjection directly. Existing `id` is an explicit alias; conflicting aliases return 400. A compatibility request without version resolves the current authorized revision once. Specific missing history returns 404 revision_not_found. Invalid selected money/quantity/currency/mode returns 400 with code, field and objectIds. Unavailable frozen algorithm returns 503 unsupported_calculation_version; there is no current-engine fallback. The release client supplies projectVersion.

The response has `identity`, RUB currency, lines, byLayer/byType, knownSubtotalMinor, nullable totalMinor, isComplete, unknownPriceObjectIds and warnings. Identity comes from the actual server revision: projectId/version, stored calculationVersion, snapshotDigest and snapshot inputDataVersions. FinancialLineDTO carries the typed shared provenance object or null, including optional FRC-09 sourceDocumentRevision/sourceDocumentChecksum. [api-example.json](api-example.json) is an actual synthetic PostgreSQL endpoint response: total `47500000` minor, groups `25000000` and `22500000`, three lines, six units, matching finance-v1 A.

Additive input fields: asset unitPriceMinor, pricingMode bundle/components, explicit components `{id?,name,quantity,unitPriceMinor}`, and object customPriceMinor. Absent canonical price uses the corresponding legacy decimal; present null remains unknown and zero remains known. Override wins over components, which replace bundle price. Only selected branches are validated. Existing asset currency must be RUB even with override. Missing asset remains a warning/line and an explicit RUB override can still price it. No cost is inferred from compoundProfile, geometry, visibility, maintenance/inactive status or catalogue recommendations.

`budget/domain/cost_projection.go` supplies exact integer arithmetic and immutable result values; `budget/document/cost.go` adapts preserved raw JSON. Legacy decimal digits are shifted and half-up rounded once per unit before quantity multiplication. Canonical prices are digit strings, canonicalized after validation; unit cap is 10^15 minor, quantity 1..1,000,000, totals use big.Int/NUMERIC and decimal strings. Empty placement lists return complete zero. Unknown prices return nullable line/group/overall totals and separate known subtotal. Old internal CalculateCost output is derived from the same projection; incompleteness is an explicit error for consumers that cannot represent null.

Migration `1789914500_cost_projections` adds immutable per-revision `cost_calculation_version=cost-rub-v1` and cached result rows keyed by project/version/calculation version, with JSONB plus exact NUMERIC totals. Existing real revisions are bound without inventing issued calculations/history. First calculation inserts with ON CONFLICT DO NOTHING and reads the committed result in one transaction. Reads reauthorize the current project even for an existing cache. Projection UPDATE is rejected; project deletion cascades cache access/storage. The v1 dispatch remains explicit for older/unread revisions. Down removes only cost additions and preserves prior revision snapshot/digest.

Root owns shared DI, Swagger generation, frontend consumers and final release acceptance. This slice does not alter defense_asset storage or implement FRC-07 budget enforcement. Financial validation at project save, budget write integration and report/compare adaptations remain their owning stages. No runtime/production acceptance follows from these local checks.

## Acceptance map

| Scenario | Evidence |
| --- | --- |
| COST-01/02/03/11 | Shared fixture A/B, hidden/inactive/maintenance lines, custom layer IDs and stable group names; actual PG A response matches independent FE projection |
| COST-04 | Canonical zero override remains known zero and suppresses template/components/legacy values |
| COST-05 | The unchanged shared component fixture totals 10000000 minor, without adding its bundle price |
| COST-06 | Pure and PG null-price cases return incomplete total=null, known subtotal separately, persisted NUMERIC null |
| COST-07 | Empty placement list has no lines/groups, complete zero |
| COST-08 | 0.125 million converts exactly; half-up happens per unit before multiplication; scientific/decimal integer quantities accepted, fractional quantities rejected exactly |
| COST-09 | API identity is pinned to requested revision; root/FE owns stale-response application tests |
| COST-10 | Structured invalid_price/invalid_quantity/invalid_currency/invalid_pricing_mode errors, canonical cap and exact total beyond JSON safe integer; PG stores 1000000000000000000000 minor losslessly |
| History/access | PG cached old result unchanged after current save; unread v1 remains v1 after a simulated future binding; unsupported binding has no cache/current-engine fallback; tenant denial, membership revoke and project deletion deny reads |
| Concurrency/migration | Eight requests materialize one cache row; current/backfilled revision only receives v1 binding, no invented calculations; immutable trigger and down preservation checked |

## RED/GREEN and independent verification

Initial golden tests failed because Calculate/CalculationIdentity were absent. Real PostgreSQL API test reproduced old endpoint rejection of projectId/version request (400). Further permanent REDs covered missing-asset override and mathematically integer decimal/scientific quantities. The independent FE agent reproduced eager decoding of ignored malformed components and silent acceptance of null pricingMode; both permanent tests failed before fixes and now pass.

Final FRC-09 integration exposed loss of its additive document revision/checksum in cost provenance. The permanent real-PG test failed on the first HTTP response before the narrow whitelist/DTO fix. It now checks the complete provenance in first and cached HTTP responses plus persisted JSONB. No asset-module code was changed for this fix.

Independent actual PG project → FE engine comparison passed for all financial fields, excluding only server identity/draft bookkeeping. A separate ten-case Go-overlay/FE corpus passed amounts, lines, groups, provenance, warning codes/severity/object IDs and validation code+field after fixes. Warning prose is not byte-identical. Review overlays and synthetic probe data live outside the repo; permanent backend tests require no overlay. The FE agent reported no remaining reproduced engine parity finding in that bounded corpus.

## Commands and results

Run from backend with Go `go1.26.0 darwin/arm64`. PostgreSQL is root's disposable local PG16 cluster; tests create/drop synthetic schemas, use committed independent connections and never touch client data.

```sh
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go test ./internal/modules/budget/... -count=1
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache FORTIS_FRC04_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' go test ./cmd/app -run '^TestFRC0(4PostgresLegacyBackfill|5)' -count=1 -v
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go test ./... -count=1 -json > /private/tmp/frc05-backend-tests.jsonl
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go test -tags=unit ./... -count=1 -json > /private/tmp/frc05-backend-unit-tests.jsonl
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go vet ./...
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go build -o /private/tmp/frc05-backend-app ./cmd/app
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache FORTIS_FRC04_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' go test ./cmd/app -run '^TestFRC0(4|5)' -count=1 -json > /private/tmp/frc05-focused-postgres.jsonl
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache FORTIS_FRC04_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' FRC02_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' go test ./cmd/app -run 'TestFRC0(2Postgres|4|5)' -count=1 -json > /private/tmp/frc05-final-postgres.jsonl
```

- Budget modules PASS; pure financial package has five top-level + 27 nested PASS.
- Final FRC-05 PostgreSQL has six top-level + three nested PASS, including source provenance. Combined FRC-04/05 command: 20 top-level + nine nested PASS, exit 0.
- Full default suite: 254 top-level + 114 nested PASS, 30 explicit opt-in SKIP, zero FAIL; 29 tested packages PASS.
- Unit-tag suite: 286 top-level + 114 nested PASS, 29 opt-in SKIP, zero FAIL; 29 tested packages PASS. One FRC-09 opt-in test was added by its owner between these runs, so skip counts differ.
- Go vet/build rerun after the final provenance fix: PASS. Build emits a denied optional module stat-cache warning but exits zero and produces the temporary binary. golangci-lint is not installed and is not claimed as run.
- Final combined FRC-02 PostgreSQL + FRC-04/05 command: 21 top-level + 11 nested PASS, exit 0. Earlier combined runs identified outdated document fixture expectations (metadata-only downloads and an incorrect metadata GET route); their owner corrected those without removing tenant authorization assertions. The final green run supersedes those transient failures. The earlier full-suite counts above predate the additive final provenance test; focused suites and vet/build were rerun after it.

To re-emit actual endpoint artifacts, set `FORTIS_FRC05_PROJECT_FILE=/private/tmp/frc05-project.json` and `FORTIS_FRC05_PROJECTION_FILE=/private/tmp/frc05-projection.json` on TestFRC05PostgresFrozenProjection. Root owns generated OpenAPI, frontend/live integration and final release acceptance.
