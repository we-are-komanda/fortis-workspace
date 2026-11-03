# FRC-03 independent acceptance plan

Date: 2026-09-21. **Plan, not acceptance.** Entry: FRC-06 accepted at frontend `a56d128`, knowledge-base `7cd0de1`, parent `0560b79`; all three worktrees clean at independent inspection. Root owns synchronization, stage decision and real vertical harness. This reviewer owns this plan, a separate workspace browser test, and later independent implementation review. Frontend/backend implementers own production files.

Authority: [FRC-03 specification](../../../fortis-release-specs/specs/FRC-03_workspace.md), [research checkpoint](research-checkpoint.md), [approved operator contract](../../../../knowledge-base/01_Requirements/Release_2026_09_20_Autonomous_Run.md), [ADR-0017](../../../../knowledge-base/03_Architecture/ADR-0017-enterprise-access-boundary.md). FRC-06 save/recovery contracts remain mandatory. Ordinary JWT users gain no enterprise/membership administration capability.

## Acceptance probes

| ID | Setup/action | Observable pass condition and evidence layer |
|---|---|---|
| OP-01 | Trusted CLI with existing synthetic user, name/address and explicit valid GIS center | Exactly one enterprise and one membership commit; identifier-only result; normal user enterprise GET sees it. Real disposable PostgreSQL plus root vertical browser. |
| OP-02 | Omit either latitude or longitude; supply NaN, Infinity, malformed number, latitude outside ±90 or longitude outside ±180 | Nonzero command exit and zero enterprise/membership delta. Explicit `(0,0)` and boundary values remain valid. CLI/domain checks plus PG. |
| OP-03 | Well-formed but nonexistent user UUID | Nonzero exit; no enterprise or membership remains. Distinct from invalid UUID input. Application/PG probe. |
| OP-04 | Force membership write failure after enterprise insert within the transaction | Command/use case fails; enterprise and membership counts unchanged in a separate committed connection. Fake-only transaction tests do not prove rollback. Disposable PG failure injection. |
| OP-05 | Attempt same user/enterprise association twice (including concurrent contention if supported) | At most one membership row; no partial enterprise left on failure. Reuse composite PK; no schema workaround or duplicated memberships. PG/repository probe. |
| OP-06 | Ordinary user calls existing enterprise-create/delete/membership routes | Existing authorization remains closed; no new public operator endpoint or JWT role. Existing FRC-02 HTTP regression plus route diff review. |
| WS-01 | E1 has projects; E2 empty; select E2 | Zero E1 rows/options, explicit empty state; network query contains E2, correct limit/offset. Browser plus store/API tests. |
| WS-02 | User has zero memberships and stale cached selection | Administrator guidance; create disabled; no selected demo/old enterprise, no unscoped project fallback. Browser. |
| WS-03 | Assign E2 through trusted CLI, then Refresh | Fresh authorized enterprise list admits E2 and enables first project. Synthetic browser assignment transition plus real CLI→normal API→browser gate. |
| WS-04 | Existing saved P; fill new name; CREATE pending, then 503 | Old P/project baseline/active ID survive; name remains; no success navigation; create cannot double-submit. Retry with unchanged input reuses frozen body/key and navigates only after confirmed server identity/version. Browser plus store tests. |
| WS-05 | Hold E1 page response, select E2, then release E1; repeat with obsolete E1 page | E2 rows/total/page/comparison remain unchanged; stale success and stale error both ignored. Browser plus request-generation store test. |
| WS-06 | E1 has 121 projects and E2 has none | Pages 50/50/21, filtered total121, correct offsets0/50/100, no first-page-only filtering; switching enterprise resets page. Last page then Previous works. API/PG counts plus browser. |
| WS-07 | Open missing project or revoke membership before GET | Clear unavailable state; no navigation using old active ID, no replacement with old current/demo state. Actual current context stays available only as allowed local state. Browser and real API authorization. |
| WS-08 | Whitespace name; name length121 code points | No POST and actionable validation; input retained. Trimmed length1…120 accepted consistently on FE and backend, including non-BMP characters. Browser/API/application checks. |
| WS-09 | Successful creation from selected E2 while old P belongs to E1 | Request uses explicit E2 and E2 center. Before response old context intact; after valid acknowledgement exactly one project-context replacement uses server projectId/version/enterprise. No geometry/name-derived ownership. Store subscription and browser. |
| WS-10 | Loaded project has missing/wrong enterprise; save acknowledgement contradicts explicit enterprise or has missing/invalid version or empty projectId | Protocol failure; no false saved state/navigation or ownership reassignment. Keep frozen attempt available for safe explicit resolution. Boundary/store tests. |
| WS-11 | A selects E2, remounts; B then signs in; E2 later revoked from A | A's valid choice survives remount; B cannot inherit A selection; refreshed permissions invalidate revoked choice before request/create. User-scoped storage is not authorization. Browser. |
| WS-12 | Dirty P; switch enterprise/open/create | FRC-06 Stay retains P, Save proceeds only after confirmation, Discard removes discarded recovery before transition. Existing FRC-06 browser suite plus focused workspace flow. |
| WS-13 | Enterprise/list read: loading, empty200, 403/404, 503, malformed response | Distinct loading/empty/error/forbidden states; no stale rows or false empty success. Refresh retries explicitly; no automatic retry loop. Browser/API tests. |
| WS-14 | More than100 authorized enterprises, selected item beyond initial page | User can reach it; enterprise total/pagination cannot silently drop it. Paginated API/FE selection check. |
| WS-15 | Load/list project lacking enterprise ownership | Reject/quarantine at backend; FE cannot adopt baseObject.id, selected enterprise or first enterprise as owner. FRC-02 orphan check and FE boundary test. |
| WS-16 | Create pending while identity/context changes | Late response cannot replace another identity/project; no success navigation by cancelled operation. Same pending request is single-flight. Store test and browser where needed. |

## Contract decisions to keep explicit

- Name length means Unicode code points (Go rune count and JavaScript `Array.from(name).length`), after trim. HTML `maxLength` alone counts UTF-16 units and cannot establish this contract.
- Create atomicity is a client-visible context guarantee in addition to the backend transaction. FRC-06's current-project save machinery cannot temporarily install a proposed project before POST and then call that atomic. Retain the old context until a confirmed server result; preserve the proposed immutable body/key separately while pending or ambiguous.
- No-membership is an empty authorized list, not an authorization bypass. A persisted selected ID must be checked against a fresh authorized response before requests or creation.
- Explicit `(0,0)` is valid GIS input. Missing/invalid coordinates must not silently become zero. Domain range checks and CLI omission checks have different purposes.
- Root approved a required stable `--enterprise-id` for safe operator retries, using the existing enterprise identity and composite membership key without a new receipt/schema. Exact same normalized payload plus same user may replay without duplicate writes; changed payload/user and preexisting unrelated enterprise IDs must fail without mutation or access adoption. The CLI remains a trusted local process, not a public admin endpoint.
- Ordinary project create/import must use explicit immutable server enterprise ownership. Existing `baseObject.id` fallback in request construction/load normalization is a known entry gap to remove, not an accepted compatibility fallback.
- Server project pagination exists and is membership-scoped; consume it. Do not replace authorization with browser filtering or silently suppress a list transport failure as an empty enterprise.

## Evidence and execution

Independent rendered checks live in `frontend/src/modules/workspace/ui/project-workspace.browser.test.ts`, use the existing Chromium/esbuild pattern and synthetic `https://fortis.test` transport. They do not prove database commit or deployment routing. Root's disposable Next→Go→PostgreSQL gate must establish the actual initial-user path after trusted provisioning. No real local root/root2 or user database mutations are authorized for fixtures.

Planned commands (exact final files/flags and exit results will be recorded after implementation):

```sh
rtk proxy env FRC03_BROWSER_TESTS=true node --import tsx --test src/modules/workspace/ui/project-workspace.browser.test.ts
rtk proxy go test ./internal/modules/enterprise/... ./cmd/app/...
rtk proxy pnpm exec tsc --noEmit --incremental false
```

Final verification also includes focused FRC-03 store/API/domain tests, accepted FRC-01/02/04/06 regressions, whole backend tests, frontend full-suite comparison against the six exact historical signatures, changed-file lint and isolated frontend production build. Browser/PostgreSQL opt-in skips are not passes. Independent review must inspect both complete diffs, report reproducible findings with file/line, and recheck closures before stage acceptance. Production deployment, TLS, operator ownership, migrations/backup/rollback remain later runtime gates and must not be inferred from local fixture success.
