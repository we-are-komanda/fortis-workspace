# FRC-09 backend evidence — 2026-09-20

Status: implemented and verified locally with synthetic PostgreSQL and private temporary files. Root owns shared config/DI/server limits, frontend integration, independent review and acceptance. Real storage/scanner deployment is **not verified**. No production migration, customer file, scanner installation, external document fetch, commit or push was performed.

## Scope and behavior

Owning code: `backend/internal/modules/defense_asset/`; migration `1789916000_asset_documents_provenance`; `backend/cmd/app/frc09_backend_test.go`. Existing asset JSONB stores additive provenance and money fields; the document migration adds immutable identity, checksum, revision, status, commercial classification and soft deletion.

- `unitPriceMinor` preserves absence versus explicit `null`; explicit null remains unknown even when a legacy `pricePerUnitMln` exists. `pricingMode` and typed components are persisted without inferring prices from compound profiles. Minor prices are decimal integer strings in 0…10^15 and component quantities in 1…10^6. Existing legacy price fields remain.
- All 13 current frontend categories and 10 roles round-trip without coarse remapping. Existing category-specific weapon/detection/EW fields preserve their values and units. The existing compatibility groups accept the corresponding frontend category names; validation errors return 400.
- Legacy provenance remains null. Confirmed requires a source date and description, safe HTTP(S) source URL, or an accessible ready source document. The server supplies recordedAt/recordedBy/revision and resolves document revision/checksum. A client cannot forge these fields. Existing demo provenance cannot silently become confirmed. Frontend seed labeling and explicit refresh preview are owned by root; arbitrary old public database rows are not guessed to be demo or confirmed.
- Existing project snapshots already retain these fields through ADR-0018 raw document preservation. Catalog updates do not mutate historical project snapshots. Availability of a referenced source is checked at download; its saved ID/revision/checksum is never replaced by a similarly named upload.
- Each upload receives a new UUID and immutable revision `1`. The local private volume uses 0700 directories and 0600 files, generated UUID storage keys, exclusive creation, bounded reads and checksum verification. Storage paths are not returned in API responses. There is no static public mount.
- Files enter quarantine before scanning. Only a successful scanner result permits the separate authorized ready transaction. Scanner errors/timeouts leave quarantine and return 503; infected/rejected returns 422 and remains unavailable. Deactivated files return 404. Same filenames never overwrite an existing object. DB/audit failure during initial upload removes the newly staged file.
- Every file operation authorizes the persisted parent asset. Public catalog mutation remains 403; foreign private resources remain 404. Upload publication and deactivation recheck persisted membership in the same transaction as the document mutation and `audit.Append`. Audit contains identifiers and version/action only. Document repository SQL logging is suppressed to avoid filename/payload disclosure.
- ClamAV uses an absolute operator-configured executable via `exec.CommandContext`, fixed arguments, a 30-second deadline and discarded process output; no shell or user-provided command arguments. Missing configuration/executable fails closed. Limits/encrypted-content alerts are enabled so those results cannot silently become clean. Adapter semantics follow the [official ClamAV man page](https://raw.githubusercontent.com/Cisco-Talos/clamav/main/docs/man/clamscan.1.in). Tests use a fake scanner or synthetic exit-code executable, never claim antivirus validation.

## API contract

Existing routes are retained. `POST /api/v1/assets/documents` accepts multipart fields `assetId`, exactly one `file`, and optional `commercial` (default true). File limit is 10 MiB; transport overhead allowance is 64 KiB. PDF/PNG/JPEG/TXT MIME is checked against bytes; SVG/HTML/mismatches are rejected. Names are sanitized. No caller-supplied storage key or destination URL is accepted. Legacy JSON metadata writes perform parent authorization and then return 400 `document_upload_required`.

Document DTO adds `revision`, nullable `checksum`, `status` (`legacy_unavailable|quarantined|ready|rejected`) and `commercial`. `downloadUrl`, when ready, is only the authenticated relative backend route. Old external URLs are never emitted or fetched. List supports limit/offset/totalItems. Download requires `id`; optional `assetId` must match the persisted parent. It returns bytes with attachment disposition, correct MIME, `nosniff` and `Cache-Control: private, no-store`. No presigned/public URL is minted.

Errors: file too large 413; unsupported/mismatched MIME 415; scanner rejection 422; unavailable scanner/storage 503; unauthorized/private/not-ready source 404. The normal error envelope remains compatible with existing handlers.

## Verification

All Go checks used `GOCACHE=/private/tmp/fortis-frc12-gocache`. PostgreSQL checks used `FRC09_TEST_DSN=host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable`, root's isolated PostgreSQL 16 cluster. The existing shared helper creates a unique committed schema and applies actual migrations. No in-memory database substitutes for these checks.

| Check | Actual result |
|---|---|
| Domain provenance/minor validation | RED: negative price accepted; GREEN after validation |
| JSONB money/provenance round-trip | RED: explicit-null presence lost; GREEN after owning-layer mappings |
| Application server stamping/demo preservation | RED: metadata absent; GREEN after application handling |
| Private storage | RED: storage not ready; GREEN with real temporary filesystem permissions/read/immutable-key checks |
| PostgreSQL document pipeline | RED: unavailable stub/no quarantine row; GREEN after transactional persistence and orchestration |
| HTTP multipart/download | PASS: 201, 400, 403, 404, 413, 415, 422, 503; bytes/headers and no external URL |
| PostgreSQL typed-card matrix | RED: category/spec mismatch; GREEN for 13 frontend categories, 10 roles and compatible typed fields |
| Revocation during scanning | PASS: quarantine persists, ready event/write absent after membership removal |
| `go test -race -tags=unit ./internal/modules/defense_asset/... ./cmd/app -run 'Test(FRC09\|DefenseAsset\|Catalog\|PrivateDocumentStorage\|Scanner\|Document\|NewDefenseAsset)' -count=1 -timeout=120s` | PASS with FRC09 test DSN |
| `go build ./...` | Exit 0; sandbox warns about unavailable global module stat-cache write, compilation succeeds |
| `gofmt` and `git diff --check` | Completed / clean |

Eleven added top-level checks include five real-PostgreSQL scenarios plus category/subcase matrices. Existing document tests were updated for the intentionally closed metadata-only API; root adapted trusted FRC-02 fixture provisioning without bypassing browser authorization assertions. One new HTTP test initially omitted `RequestCtx.Init2`, causing a test-only fasthttp context panic and cleanup hang; bounded timeout identified it, initialization was corrected, and the identified old test process was stopped. This was not a production pipeline fix.

## Acceptance limits and runtime gates

DATA-01/02/03: backend nullable provenance, confirmed validation and demo preservation verified. DATA-04: immutable project storage is covered by FRC-04; actual frontend refresh preview/save is separate integration evidence. DATA-05/06/07/09: local filesystem + PostgreSQL + HTTP + synthetic scanner checks pass. DATA-08: backend transmits text/attachment data, while frontend text rendering requires frontend evidence. DATA-10: native categories/roles, typed-card fields and precise money round-trip pass; instance overrides remain in project snapshots, not catalog mutation.

Production remains disabled until the owner approves and verifies a persistent private volume/object lifecycle, backup/restore, replica sharing or single-writer deployment, scanner executable/signature freshness, real clean/infected/unavailable pipeline checks, monitoring and retention/deletion policy. Checksum is integrity metadata, **not antivirus**. Previously issued external URLs require owner-side storage ACL/revocation evidence; removing them from this API cannot revoke a third-party URL already known elsewhere.

Quarantined, rejected and deactivated files remain private until the owner's retention/cleanup policy is supplied. A process crash between file creation and the first DB commit can leave an unreachable private file; no public route discovers it. Soft deletion does not silently erase evidence or manufacture historical availability. This implementation does not claim atomicity between PostgreSQL and the filesystem. Do not run the down migration after real collection without an approved backup/data policy: it removes scan-state safeguards. Application rollback must remain fail closed or retain the new tables/columns and roll forward.

## Independent review and authorized corrections

The independent backend review traced upload quarantine/publication, current parent authorization, immutable file identity, source provenance, scanner execution and storage permissions. A temporary real-PostgreSQL overlay injected an audit failure specifically during publication: the file remained quarantined, download stayed closed and only the original upload event remained. This additional transition check passed.

One reproducible DATA-10 defect was found in the existing update path: a valid detection card with detectionSpec accepted a category change to kinetic, then failed to deserialize on subsequent reads. The parent authorized the reviewer to fix the shared root cause. Creation and update now call the same complete aggregate validation; update stages replaced fields on a value copy, so rejected changes cannot mutate a previously loaded aggregate. Permanent RED→GREEN tests cover in-memory aggregate preservation and HTTP 400 with the original PostgreSQL row unchanged for incompatible category, specification and invalid deployment type. No new category/domain inference was added.

FRC-09 OpenAPI annotations now use response bodies and request body wrappers, describe binary download, attach correct operation/query names and expose exact minor prices as strings. Current native category/role enum additions are reflected. The v0.36.6 scanner drops Required when placed on a swagger:file field; the multipart operation is therefore described with supported operation YAML next to UploadDocumentRequest in document_dto.go. The generated result has required assetId/file, optional commercial=true and actual error statuses. Source annotations were edited; generated Swagger was not hand-edited. The scoped nine-path assets/documents spec validates against Swagger 2.0.

Commands run from backend, with `GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache`:

```sh
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache FRC09_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' go test -race -tags=unit ./internal/modules/defense_asset/... ./cmd/app -run 'Test(FRC09|DefenseAsset|Catalog|PrivateDocumentStorage|Scanner|Document|NewDefenseAsset)' -count=1 -timeout=120s -json > /private/tmp/frc09-fixed-tests.jsonl
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache FRC09_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' FORTIS_FRC04_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' FRC02_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable' go test ./cmd/app -run 'TestFRC0(2Postgres|4|5|9)' -count=1 -json > /private/tmp/frc09-final-postgres.jsonl
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache /private/tmp/fortis-release-tools/swagger generate spec -o /private/tmp/frc09-swagger-review.json --scan-models
rtk proxy /private/tmp/fortis-release-tools/swagger validate /private/tmp/frc09-swagger-scoped.json
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go vet ./...
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go build -o /private/tmp/frc09-backend-app ./cmd/app
rtk proxy git diff --check
```

Results: race suite 55 top-level + 16 nested PASS across five packages; combined real-PG FRC-02/04/05/09 suite 27 top-level + 24 nested PASS; both original independent overlay checks GREEN after correction; vet/build/diff-check PASS. Build retains the nonfatal sandbox module-stat-cache warning. Scoped OpenAPI is derived by retaining `/api/v1/assets*` paths plus recursively referenced definitions/responses/parameters without modifying their content; parent owns generation of final repository/release artifacts. Other legacy modules still emit their pre-existing Swagger warnings. The bounded review has no remaining reproduced code finding; real scanner/storage and release runtime gates above remain open.
