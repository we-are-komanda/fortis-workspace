# FRC-02 — executed verification

All commands ran locally through `rtk proxy`; paths below are relative to their repository. Synthetic fixtures only. Go env: `GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache`. Browser ports: frontend 3102, backend 8092; local test PostgreSQL 54379. Logs retained under [evidence](evidence/).

## Final command results

| Repository / command | Result | Log |
|---|---|---|
| backend `go test -count=1 ./...` | PASS, exit 0 | [log](evidence/backend-final.log) |
| backend `go test -tags unit -count=1 ./...` | PASS, exit 0 | [log](evidence/backend-unit-final.log) |
| backend `go build -o /private/tmp/frc02-implementation/fortis-backend ./cmd/app` | PASS, exit 0 | [log](evidence/backend-build-final.log) |
| backend `go test ./cmd/app -run TestFRC02ProductionDependencyGraph -count=1 -v` | PASS; real dig graph DryRun | [log](evidence/backend-di.log) |
| backend `go test ./cmd/app -run TestFRC02 -count=1 -v` | Security tests PASS; optional PostgreSQL/browser tests skip without opt-in | [log](evidence/backend-access-extended.log) |
| backend `FRC02_TEST_DSN="host=127.0.0.1 port=54379 user=fortis_test dbname=postgres sslmode=disable" go test ./cmd/app -run TestFRC02Postgres -count=1 -v` | PASS, A/B real SQL | [log](evidence/postgres-final.log) |
| frontend `node --import tsx --test $(rg --files src | rg '\.test\.(ts|tsx|mjs)$')` | exit 1: 90 tests / 84 PASS / 6 known FAIL | [log](evidence/frontend-full-review.log) |
| frontend `node --import tsx --test src/shared/lib/auth-boundary.release.test.ts src/shared/lib/identity-isolation.release.test.ts` | PASS, 14/14 | [log](evidence/review-race-green.log) |
| frontend `node node_modules/typescript/bin/tsc --noEmit --incremental false` | PASS, exit 0 | [log](evidence/frontend-types-clean.log) |
| frontend `node node_modules/eslint/bin/eslint.js <23 changed TS/TSX files>` | PASS, exit 0; exact arguments below | [log](evidence/frontend-lint-review.log) |
| frontend `FORTIS_NEXT_DIST_DIR=.next/frc02-build pnpm build` | PASS, exit 0, Next 16.2.11 | [log](evidence/frontend-build-review.log) |
| frontend `node node_modules/@playwright/test/cli.js test --config test/playwright/frc02.config.ts` | PASS 3/3 (9.9s) | [log](evidence/browser-e2e-review.log) |

Full frontend command includes FRC-01 backend-boundary, readiness and project-runtime regressions; all pass. Default Go commands do not claim PostgreSQL coverage: the explicit DSN command above supplies it.

## Local stack commands

```sh
# backend repository; same Go environment as above
FRC02_BROWSER_SERVER=true FRC02_TEST_DSN="host=127.0.0.1 port=54379 user=fortis_test dbname=postgres sslmode=disable" go test ./cmd/app -run TestFRC02BrowserServer -count=1 -v -timeout 35m
# frontend repository
BACKEND_URL=http://127.0.0.1:8092 FORTIS_RUNTIME_MODE=workspace FORTIS_LOCAL_DEVELOPMENT=true FORTIS_AUTH_ENABLED=true FORTIS_NEXT_DIST_DIR=.next/frc02-e2e node node_modules/next/dist/bin/next dev --hostname 127.0.0.1 --port 3102
```

`__fixture/__revoke/__stop` only exist in `_test.go`. Restart fixture before rerun because revocation intentionally changes test membership. Database work rolls back; no production migration. Existing schema migrations applied in unique test transaction, not on application startup.

## RED → GREEN and intermediate attempts

- Backend `go test ./cmd/app -run 'TestFRC02(TenantIsolation|RevocationSameJWT|OrphansAndMissing)' -count=1`: original foreign resource 200/private-list leak/public mutation 201 and revocation/orphan access reproduced ([RED log](evidence/backend-red.log)); final same coverage PASS. Later invalid identity/500, own CRUD/pagination and DI coverage expanded.
- Frontend auth-boundary test reproduced missing Secure cookie, cookie-only protected page admission and unsafe next ([RED](evidence/frontend-auth-red.log)); all four final cases pass.
- Frontend identity isolation reproduced A recovery under B and incomplete resets ([RED recovery](evidence/frontend-identity-red.log), [RED switch](evidence/frontend-switch-red.log)); all four final cases pass.
- Focused `node --import tsx --test src/shared/lib/project-runtime.release.test.ts` and existing project-store test runs were used while integrating scoped recovery. Final all-source suite includes them.
- Earlier `go test ./...` / `go test -tags unit ./...` iterations exposed old mock/signature and expected-error assumptions; fixtures updated to explicit actor without weakening business assertions. Final both suites pass.
- PostgreSQL attempts: initial local connection restricted by sandbox; approved local-network retry exposed a test RequestCtx initialization defect, fixed in fixture. Actual final SQL suite passes.
- First production build failed fetching Google Fonts under network restriction; network-approved retry passes. Typecheck/lint were rerun on final code.
- Browser first attempt exposed logout navigation stuck after identity remount; full navigation after cookie clearing fixed it (subsequent 2/2 passed). Extended 3-case run initially used wrong exact accessible link name, fixed against browser snapshot; final 3/3 pass.
- Known-failure comparison runs each of six files using `node --import tsx <file>` in `/private/tmp/frc02-implementation/frontend-before` and current frontend; only root paths normalized. Full signatures identical 6/6 ([JSON](evidence/failure-signatures-after.json)). Pre-FRC-01 evidence remains in [original addendum](pre-frc02-failure-signatures.txt).

No React Doctor run was required for this request; no production browser/storage test, deployment or migration is claimed.

## Exact lint arguments

```text
src/app/api/auth/login/route.ts
src/app/api/auth/logout/route.ts
src/app/api/auth/register/route.ts
src/app/layout.tsx
src/modules/auth/ui/login-page.tsx
src/modules/auth/ui/register-page.tsx
src/modules/drone-defense/domain/use-defense-variants-store.ts
src/modules/drone-defense/infra/backend-integration-contract.test.ts
src/modules/drone-defense/ui/variant-selector.tsx
src/proxy.ts
src/shared/lib/api-client.ts
src/shared/lib/auth-boundary.release.test.ts
src/shared/lib/identity-isolation.release.test.ts
src/shared/lib/identity.ts
src/shared/lib/project-runtime.release.test.ts
src/shared/lib/safe-next.ts
src/shared/lib/session-state.ts
src/shared/lib/use-defense-project-store.test.ts
src/shared/lib/use-defense-project-store.ts
src/shared/server/auth-cookie.ts
src/shared/ui/identity-boundary.tsx
test/playwright/frc02.config.ts
test/playwright/frc02.spec.ts
```

## Final independent review / fix pass

One P2 stale-error finding. The new test `late project access failures cannot invalidate another current project` fails for all five operations on pre-fix code ([RED](evidence/review-race-red.log)); checking load generation/abort before error effects, targeting access invalidation to the affected project, and keeping list failures out of resource trust state resolves it ([GREEN](evidence/review-race-green.log)). Full frontend rerun: 90 tests / 84 pass / six identical baseline failures. All commands in final table point to the post-review output where affected. No second review or deferred minors.

After restoring task-generated tsconfig changes, explicit typecheck passed again. `gofmt -w cmd/app/frc02_access_test.go` formatted only the new test fixture; `go test -count=1 ./cmd/app` passed afterward ([log](evidence/backend-format-final.log)). Other pre-existing gofmt findings were not modified. Synthetic backend/Next/PostgreSQL stopped after testing. Test-specific generated backend binary removed.
