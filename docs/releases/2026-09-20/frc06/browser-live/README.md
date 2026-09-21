# FRC-06 real-backend browser evidence

Executed 2026-09-21, final browser run approximately 11:08–11:09 Europe/Moscow.
Result: **PASS, six checkpoints, process exit 0**. This is local integration evidence;
it does not establish production deployment acceptance or complete FRC-03.

Harness: `frontend/test/playwright/frc06-live.cjs`. Browser plugin was unavailable;
the run used the existing Playwright installation. Browser requests traversed
Next.js `127.0.0.1:3111` → Go test backend `127.0.0.1:8092` → actual PostgreSQL.
No project API response was mocked. Project creation and the competing write used
the authenticated API; edits, save, navigation, recovery and save-as-new used UI.

## Stack and isolation

| Component | Actual local version/configuration |
| --- | --- |
| Node | 26.4.0 |
| Next.js | 16.2.11, development mode, isolated output directory |
| React | 19.2.4 |
| Playwright | 1.60.0, headless Chromium, viewport 1440×960 |
| Go | 1.26.0 darwin/arm64, `GOTOOLCHAIN=local`, `GOPROXY=off` |
| PostgreSQL | 16.13 Homebrew, loopback port 55434 |
| Backend checkout | `5ddc2ce58e5159a96069efabb2fa3250e02666cf`, unchanged |
| Frontend | Current local FRC-06 worktree during this run |
| Runtime policy | `workspace`, explicit local development, `localDraftsEnabled=true` verified through `/api/runtime` |

The disposable cluster is recorded by `/private/tmp/fortis-release-run-location.json`:
data directory `/private/tmp/fortis-release-run-ghbq31gu/pgdata`, user `fortis_test`,
database `postgres`, port **55434**. The test runner does not source backend `.env`.
The user's database at port 5432 and root/root2 memberships were not used or changed.

`TestFRC02BrowserServer` calls `frc04Database`, which creates a random
`frc04_<uuid>` schema, applies actual migrations there, and sets `search_path` on
each connection. HTTP requests use committed independent transactions. Test cleanup
drops that schema. Its `/__fixture` and POST `/__stop` routes exist only in `_test.go`;
the server binds loopback and has a built-in 30-minute lifetime. Test fixture B uses
synthetic `example.test` data. No customer data, real credentials or production
services are part of this evidence.

## Verified milestones

| Step | Evidence |
| --- | --- |
| Create independent synthetic project | Original ID `c1ff624a-2415-415f-9cf8-6b636981a299`, enterprise `96604e7a-0f2a-4966-81f1-9f2de2bb2990`, version 1 |
| UI layer visibility edit, Save and reload | Same original ID, version 2, `frc06-layer-l1.isVisible=false`; actual GET confirmed content before and after saving |
| Dirty map → calculator → map | Same project and unsaved `isVisible=true`; server stayed version 2 with `false`; calculator visibly marked draft |
| Explicit recovery after reload | Reload initially showed server state; modal offered recovery; Restore changed only local state; Save committed version 3 |
| Concurrent write and conflict | Independent API writer committed original version 4 with layer name `Concurrent saved layer`; UI Save received real HTTP 409 and retained its local draft |
| Save as new and reload | New ID `6fb03735-6e05-4fbf-a81b-a71917be8767`, version 1, original local layer name and `isVisible=false`; URL and actual GET remained on the new ID after reload; original remained unchanged at version 4 |

[run.log](run.log) contains the concise checkpoint results.
[result.json](result.json) contains all checkpoints, console records and API response
statuses. Six numbered screenshots show saved reload, draft calculation, explicit
recovery, conflict, save-as-new and the new project's reload.

The initial diagnostic run exposed a stale-URL defect after save-as-new: the store
changed project but reload reopened the original ID. The final run above verifies
the root-owned URL synchronization fix against this previously failing scenario.

## Console and interaction observations

- No uncaught page errors or duplicate deck layer IDs occurred in the final run.
- One console resource error is the **expected 409 Conflict** deliberately produced
  by the concurrent writer; it is not an unexpected application failure.
- AntD emits the known `Alert.message` deprecation warning through `console.error`.
  It is retained separately in `knownWarnings`; the harness rejects other unexpected
  console errors. Deck missing-Cyrillic-glyph and Chromium ReadPixels performance
  warnings are also preserved in the raw result.
- The Next development indicator intercepts a pointer click on the bottom-left Save
  control after scrolling it into view. Its initial box was `x=8,y=961,w=59,h=48`
  in the 1440×960 viewport. The harness therefore focuses the actual enabled Save
  button and presses Enter. It does not force-click, hide the overlay or call the
  application store to save. Pointer accessibility/layout remains an observation
  for later UI verification.
- After hard reload the status label uses business `projectName` rather than the
  separately supplied save-as-new variant name. The harness records that label;
  acceptance here verifies actual project ID, immutable version and content.

Selectors use roles, labels, titles and visible controls. The layer selector scopes
the existing `data-selected` container by its exact visible layer title. There is
no `.first()`, `.nth()`, DOM-order selector or random-coordinate interaction.
Recovery inspection uses the actual scoped key
`fortis:draft:<encoded-userId>:<encoded-enterpriseId>:<encoded-projectId>` and never
injects browser state.

## Commands and backend checks

From `frontend/`, with the isolated stack already running:

```sh
rtk proxy env FRC06_BROWSER_OUTPUT=/private/tmp/frc06-live/final \
  node test/playwright/frc06-live.cjs
rtk proxy node --check test/playwright/frc06-live.cjs
```

Both exited 0. The browser stack requires explicit `BACKEND_URL=http://127.0.0.1:8092`,
`FORTIS_RUNTIME_MODE=workspace`, `FORTIS_LOCAL_DEVELOPMENT=true`,
`FORTIS_LOCAL_DRAFTS_ENABLED=true`; configured backend aliases must agree.

Backend checks used the existing cache `/private/tmp/fortis-frc12-gocache` and ran
before the browser fixture was started. From `backend/`:

```sh
rtk proxy env GOTOOLCHAIN=local GOPROXY=off \
  GOCACHE=/private/tmp/fortis-frc12-gocache go test ./... -count=1
rtk proxy env GOTOOLCHAIN=local GOPROXY=off \
  GOCACHE=/private/tmp/fortis-frc12-gocache go build ./...
rtk proxy env GOTOOLCHAIN=local GOPROXY=off \
  GOCACHE=/private/tmp/fortis-frc12-gocache \
  FRC02_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' \
  FORTIS_FRC04_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' \
  go test ./cmd/app -run 'TestFRC0(2Postgres|4|5)' -count=1 -v -timeout 5m
```

All three exited 0. The PostgreSQL run reports **21 top-level tests passed, zero
skips, zero failures**. Preserved logs, prefixed to avoid collision with reviewer logs:

- [Full backend tests](../verification-logs/backend-live-go-test.log).
- [Backend build](../verification-logs/backend-live-go-build.log): successful exit 0,
  with a non-fatal sandbox warning writing Go's module metadata cache under
  `/Users/rr/go/pkg/mod/cache`; no compilation failure.
- [Actual PostgreSQL regressions](../verification-logs/backend-live-postgres.log).

Initial sandbox attempts denied PostgreSQL shared memory and loopback connection.
Approved local-only retries started the same disposable cluster and produced the
passing PostgreSQL evidence above; denied attempts are not counted as test PASS.

## Fixture shutdown

After acceptance the owned browser backend was stopped through POST `/__stop`.
`TestFRC02BrowserServer` exited **0 / PASS** after 1690.13 seconds; port 8092 no
longer had a listener. [Shutdown log](../verification-logs/backend-live-browser-stop.log).
Read-only PostgreSQL namespace checks before/after confirmed that cleanup removed
only `frc04_2eebd44e3ae54e258c271763dcbae14c`; no schema was added. Four older
synthetic schemas were left unchanged. Disposable PostgreSQL 55434 and owned
Next 3111 remained running for the next stage; user services 8090/3000 were untouched.
