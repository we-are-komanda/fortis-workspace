# FRC-10 independent acceptance plan

Status: preparation, not acceptance. Accepted entry commits: parent `b08d476`, frontend `667c447`, backend `4ff76c3`, knowledge-base `c596e6a`. FRC-06 SAVE-09 was explicitly staged N/A while reports were disabled; the actual dirty→report flow is mandatory here before enabling the capability.

Read [FRC-10](../../../fortis-release-specs/specs/FRC-10_versioned_report.md), [SAVE-09](../../../fortis-release-specs/specs/FRC-06_save_recovery.md), [ADR-0017](../../../../knowledge-base/03_Architecture/ADR-0017-enterprise-access-boundary.md) and the [autonomous contract](../../../../knowledge-base/01_Requirements/Release_2026_09_20_Autonomous_Run.md). Current approved decisions supersede the draft spec's viewer/viewCost proposal: enterprise membership authorizes reports; no new financial RBAC is introduced. Explicit hideCost still requires server-side omission.

## Contract and ownership

Issue through `GET /projects/report?id=P&projectVersion=V&hideCost=true|false&mapView=all|saved`; reopen through exclusive `GET /projects/report?reportId=R`. Versions and hideCost are parsed strictly. Contradictory/mixed modes are rejected rather than silently overriding one another. Report identity, immutable stored payload and issuance uniqueness include schema version, project revision, hideCost and mapView. Reopen reauthorizes current membership and returns the issued data without current catalog/budget/name enrichment or recalculation. Source deletion cascades to report unavailability/404. Missing historical enterprise name remains null with an honest label.

The unpriced response is an independently constructed allowlist: safe identity, text, quantities, geometry and display attributes only. It skips finance evaluation and cannot inherit raw project/catalog JSON, component pricing, budgets, financial warnings/provenance, arbitrary metadata, document references, private URLs or attachments. Safe inventory remains complete in both modes. Arbitrary user-entered free text can contain amounts; a separate manual-review warning is required and automatic free-text redaction is not claimed.

The approved viewer is a standalone `/reports/[reportId]` surface, keeping priced calculator content out of the unpriced report DOM and print document. Its map is an inline SVG built only from the frozen allowlist, explicitly labeled as a schematic view without an external basemap. No third-party image/export service, current Zustand map or mock/fallback ring is used. Map/font readiness gates printing; a malformed or failed render must not produce an apparently successful blank map.

Frontend owner: production DTO boundary, issuance/save intent, report route/view/map/print CSS and focused unit tests. Backend owner: DTO/domain/application/persistence/migration plus actual PostgreSQL tests. Independent reviewer: new `frontend/src/modules/defense-calculator/ui/report.browser.test.ts` once the DTO is agreed, and this plan/review. Coordinator: real Next→Go→PostgreSQL→report→PDF harness, seeded finance A7, 100 rows, empty/unknown/hidden modes, screenshots and extracted PDF evidence. No production edits by this reviewer.

## Server and immutable document probes

| ID | Probe | Required evidence |
|---|---|---|
| REP-01 | Priced finance fixture A7 | One payload identity A7 across map, objects, cost and budget; exact 47500000 minor and expected layer/type sums; saved name/time, report generation time/schema and source quality present. |
| REP-02 | Issue A7 while draft/current A8 changes | Document stays A7 through pending map rendering and after current project changes. No live store subscriptions or later catalog enrichment. |
| REP-03 | Issue and reopen hidden-cost report | Recursive JSON allowlist and report DOM/print HTML/PDF text/metadata contain no financial fields or test financial sentinel. No attached files or private URLs. No priced cost/cache call. |
| REP-04 | Place price-only sentinels in template, override, compound components, price provenance, document URLs and arbitrary metadata | None crosses the hidden-cost projection, including map and object subtrees; allowlisted descriptive sentinel does survive to demonstrate real data rather than an empty report. |
| REP-05 | Invalid version/mode/query; reportId plus override parameters | 400 with no partial payload; absent/zero/fractional versions never select mutable latest. Invalid hideCost never silently yields priced output. |
| REP-06 | Current membership removed, foreign/orphan/deleted source or unknown report | 404 without partial names, positions, geometry, prices or attachment links; cached/issued report reopening is also checked. |
| REP-07 | Concurrent issuance of the same selection; storage failure | One committed immutable identity/payload for the agreed unique selection; no partially issued artifact. Retry returns the stored winner. Transaction rollback proven in PostgreSQL. |
| REP-08 | Reopen reportId after source v8, catalog/source price changes or calculator implementation/binding change | Exact issued payload and report ID/digest/generatedAt remain unchanged. No new cost computation on reopen. Original source deletion still produces 404. |
| REP-09 | Same source revision with priced/unpriced and all/saved modes | Distinct issued selections; exclusive reportId reopening cannot convert one mode to another. |
| REP-10 | Historical enterprise name absent | Null survives boundary; UI says the historical name is unavailable, without borrowing the current enterprise name. |
| REP-11 | Unsupported financial calculator on source revision | Priced issuance fails honestly; hidden-cost issuance still succeeds without finance evaluation. Existing issued payload remains readable by authorized users. |

## Rendered browser and SAVE-09 probes

| ID | Probe | Required evidence |
|---|---|---|
| SAVE-09a | Dirty → request report → Cancel | No issue/open request, no save, edits/name/pinned intent remain intact. |
| SAVE-09b | Dirty → explicitly use last saved | Requests the saved positive revision, leaves unsaved business changes untouched and never mixes them into map or inventory. |
| SAVE-09c | Save before report: hold PUT | No report issuance or navigation before confirmed save. Then issue exactly the acknowledged revision; duplicate click does not create parallel save attempts. |
| SAVE-09d | Save 409/422/403/404/network/503 or ambiguous acknowledgement | Report is not presented as current. Inputs and frozen save attempt are preserved where appropriate; no automatic write retry or fabricated success. Verified ambiguous committed save follows existing save semantics. |
| SAVE-09e | User makes a newer business edit while PUT is pending | The newer edit remains dirty. Accepted strict `saveCurrentProject` semantics keep the report dialog pending until explicit last-saved choice; never label the newer draft as saved or weaken logout guards. |
| REP-12 | Issue/load pending, then change identity or report selection | Old result/error cannot publish or navigate in the new context. Existing private report disappears on identity invalidation. |
| REP-13 | Another request confirms selected project's denial while report is displayed or pending | Existing report clears, printing is unavailable, late success cannot publish. Denial of an unrelated active project does not suppress the authorized report. FRC-08's observed denial race is an explicit regression. |
| REP-14 | Malformed report ID/ref/version/schema/mode/digest/nested financial identity | Entire response rejected, no partially rendered official document or fallback. Renderer receives only a validated payload. |
| REP-15 | Priced→hidden selection with old priced response arriving late | Hidden viewer never receives or renders the previous priced payload, including print state and document title. |
| REP-16 | Manual free-text amount in hidden report | Text is not claimed sanitized; separate manual-review warning appears before print. Financial schema fields remain absent. |

## Frozen map and real PDF probes

| ID | Probe | Required evidence |
|---|---|---|
| MAP-01 | All-map default; saved filters hide a layer/object | Default includes every report position. `mapView=saved` visibly says selective view; recorded visibility identifies the selection. Full inventory/counts/priced estimate remain identical. |
| MAP-02 | Circle/ring, polygon/freeform, duplicate human layer codes, per-instance position and compound coverage geometry | SVG uses frozen stable IDs and actual allowlisted geometry; no fabricated default rings. Objects match inventory IDs. Changing the workbench does not change the map. |
| MAP-03 | SVG/font readiness delayed or map invalid | Print stays disabled until ready; errors give a retry/actionable explanation, with no blank-map success. Negative Chromium probe rejects actual `document.fonts.ready` before mount, without a production fault switch; positive strict-console checks stay separate. Invalid coordinates fail closed. No external map/export network request. |
| PDF-01 | Long multilingual/unbroken names, descriptions and 100 placed rows | Real Chromium PDF contains every row and expected totals once; repeated table headers and page numbers are readable. No clipped columns, truncated rows or overlapping footer. Inspect first/middle/last pages visually. |
| PDF-02 | PDF map and legend | Native SVG geometry/markers/legend remain visible in the actual PDF. A screenshot of an HTML map or a successful print call alone is insufficient. |
| PDF-03 | Hidden-cost sentinel report | Extract PDF text and inspect metadata/attachments/links plus source print HTML. No financial sentinel, financial columns, private link or priced document title/filename. Visual inspection confirms no blank map or hidden background calculator page. |
| PDF-04 | Empty configuration | Honest zero-position report; priced total zero, no reference/catalog recommendations; nonblank schematic/base-object state or explicit empty map explanation. |
| PDF-05 | Unknown prices, estimated/demo data, unperformed spatial checks | Prominent preliminary/incomplete reasons; unknown remains null/unavailable, not zero. No “no conflicts” claim without checks, no probability/effectiveness/coverage sufficiency claim. |

The PDF sentinel must be unique and absent from allowed coordinates/IDs/descriptions, so leakage checks test a financial source rather than accidentally matching valid geometry or free text. Use a separate allowed free-text sentinel for the manual-review case. Avoid naive “all numbers forbidden” assertions.

## Evidence and final gate

Record exact commands, exit status, fixture identity, tested source/dependency hashes, actual RED→GREEN and post-fix-only cases honestly. Root-owned real PDFs and rendered page images must be retained with extracted text and a short inspection record. The hidden-cost guarantee is demonstrated at server JSON, validated report DOM, print document and actual PDF layers; no single layer substitutes for the others.

Run relevant save/recovery, identity/access, cost/budget/comparison and document-provenance regressions. Compare full frontend failures with the six complete historical signatures; investigate every additional failure. Final type/lint/build and source manifests must include the last accepted report/map/print changes. Local code/report acceptance is separate from FRC-14 production artifact/TLS/storage/backup/retention gates.
