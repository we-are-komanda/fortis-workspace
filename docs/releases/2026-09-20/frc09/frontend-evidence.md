# FRC09 — frontend documents evidence

Date: 2026-09-20. Owner: independent frontend agent. No commits, server deployments, shared build/dev server, real external file storage or real scanner calls.

## Owned scope

- `frontend/src/modules/drone-defense/infra/asset-documents-api.ts`
- `frontend/src/modules/drone-defense/infra/asset-documents-api.test.ts`
- `frontend/src/modules/drone-defense/ui/asset-documents-panel.tsx`
- `frontend/src/modules/drone-defense/ui/asset-documents-panel.browser.test.ts`

Manager integration, provenance form, project/catalogue refresh store, shared API proxy and backend remain owned by root/other agents.

## Contract and behavior

`AssetDocumentsPanel({assetId, onSourceSelected?})` is mounted only for a known server card by its parent. Ready documents expose the optional `Использовать как источник` callback with their immutable ID, revision and checksum. UI never repoints older source references or applies catalogue values to a project.

Upload uses a real File in multipart `assetId`, `file`, `commercial` (true default), with browser-generated multipart Content-Type. No client storage key or external URL is sent. Client size/type checks reject empty, >10 MiB and non-PDF/PNG/JPEG/TXT inputs; server content validation/scanning remains authoritative.

List API validates consumed DTO fields, parent asset ID, statuses and ready integrity metadata; removes unconsumed storage/URL fields. It requests 50-row pages with totalItems. UI shows ready, quarantined, rejected and legacy_unavailable, revision, checksum and size. Upload/delete refresh the list; scan failure refreshes persisted quarantine/rejection while retaining the selected File. Success appears only after a valid server response. 503 honestly identifies scanner/storage unavailability; support request ID and 429 Retry-After are presented when supplied.

Download GET targets the fixed authenticated API path with document ID and asset ID, credentials same-origin and cache no-store. It consumes raw Blob bytes, validates MIME (allowing text charset parameters), metadata length and size cap, and checks session generation before/after reading. Only non-OK responses pass through readJson for the existing 401/403/404 boundary. No file bytes are parsed as JSON. A temporary object URL triggers attachment save and is revoked. Server-provided download URLs are neither retained nor rendered.

Selected asset/session changes remount scoped state and abort old operations. Delayed responses cannot repopulate a different card. A 403/404 document action closes stale metadata/actions pending an explicit verified refresh. Filename/checksum/error data render as React text. Controls have labels, feedback associations, loading/disabled states and wrapping layout using existing styles.

## TDD and verification

All commands run from `frontend/` with `rtk proxy`:

1. `node --import tsx --test src/modules/drone-defense/infra/asset-documents-api.test.ts`: initial RED 0/8 (legacy metadata POST, unvalidated lists and absent binary helper). First implementation GREEN 8/8. Added charset/MIME/length regression RED 8/9; fixed MIME media-type comparison; final **9/9 PASS**.
2. `env FRC09_BROWSER_TESTS=true node --import tsx --test src/modules/drone-defense/ui/asset-documents-panel.browser.test.ts`: initial RED missing panel; five rendered behavior scenarios GREEN. Added account-switch and revoked-download scenarios: account switch passed, revoked download RED because the stale source action remained. Fixed fail-closed panel state; final **7/7 PASS**.
3. `pnpm exec tsc --noEmit`: initial test fixture status widening corrected; final **exit 0**.
4. `pnpm exec eslint src/modules/drone-defense/infra/asset-documents-api.ts src/modules/drone-defense/infra/asset-documents-api.test.ts src/modules/drone-defense/ui/asset-documents-panel.tsx src/modules/drone-defense/ui/asset-documents-panel.browser.test.ts`: **exit 0**.

API tests exercise real helper behavior: actual multipart File, exact10 MiB boundary/four MIME types, invalid DTO/parent/checksum, URL stripping, fixed binary path, 401 invalidation, stale binary rejection on identity change, non-ready fail-closed, DELETE contract, executable MIME/length rejection and text charset compatibility.

Browser tests bundle actual React panel, actual API helper and actual session store with esbuild; only transport is intercepted using synthetic fixtures. Chromium runs at 375px viewport; CSS modules are empty-loaded, so these establish behavior/accessibility semantics, not final visual acceptance. Scenarios cover all statuses/escaping/ready source callback, scanner503 preserving file then real retry receipt, invalid-file feedback, real Blob attachment download and delete refresh, old-card response isolation, account-switch clearing, and revoked-download action closure.

Parent owns final actual Next/BFF/Go/storage browser integration and responsive visual review. No claim of real scanner availability or deployment acceptance is made here.
