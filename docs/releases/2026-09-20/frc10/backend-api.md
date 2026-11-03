# FRC-10 backend API

Implementation source of truth: `backend/internal/modules/report/ui/dto.go` and `controller.go`.

## Request modes

- Issue/reuse: `GET /api/v1/projects/report?id=<project UUID>&projectVersion=<positive integer>&hideCost=true|false&mapView=all|saved`.
- `hideCost` and `projectVersion` are required. `mapView` defaults to `all`.
- Reopen: `GET /api/v1/projects/report?reportId=<issued UUID>` only. Mixing this with any issuance parameter, duplicate parameters, and unknown parameters returns 400.
- No implicit current project version or boolean coercion. Access now follows ADR-0026 shared workspace without authentication; the earlier membership boundary is superseded.

Responses are direct JSON bodies. Missing version is 400 `version_required`; malformed input is 400 `validation_error`; unavailable revision/report/current membership is 404; unavailable pinned priced calculator is 503 `unsupported_calculation_version`; invalid saved map geometry is 422 `invalid_report_snapshot`.

## Immutable payload

Common fields: `reportId`, `reportSchemaVersion` (`report-v1`), existing `identity` (project/version/calculator/input-version bindings/snapshot digest), `generatedAt`, `title` (saved variant name), `enterprise: {id, name: null}`, `hideCost`, `mapSnapshotData`, `mapVisibility`, `objects`, `warnings`, `limitations`.

Enterprise name is null because existing revisions did not capture a trusted enterprise name. The saved base-object name remains separately available; neither it nor a mutable current enterprise name is relabeled as historical enterprise metadata.

Priced payload adds canonical exact `cost`, `budget`, and deduplicated frozen `sources`. Unknown prices remain null. A priced-only `preliminary_report` warning is emitted for incomplete prices, missing provenance, or provenance whose quality is not `confirmed`.

Unpriced payload uses a separate DTO without cost, budget, sources, financial line fields, financial provenance, financial warnings, asset libraries, raw metadata, document references, or structured URLs. It never invokes the financial calculator. Its identity still records the saved revision/calculator binding, including an unsupported historical calculator name.

## Safe map and inventory

`mapSnapshotData = {baseObject: {id,name,center}, layers: ReportLayer[], objects: ReportMapObject[]}`. Arrays always contain the full saved composition. `mapVisibility = {mode: "all"|"saved", layerIds: string[], objectIds: string[], showCoverage: false}` selects what the standalone renderer displays.

`all` includes every saved layer/object. `saved` uses saved layer visibility and object visibility (an absent visibility flag means visible); an object also needs a visible layer. Inventory and priced totals remain complete in both modes. Selective mode carries `selective_map` warning.

Layer allowlist: id, name, code, description (nullable text), order, color (nullable safe CSS color), opacity (nullable), isActive, isVisible, geometry. Geometry is circle (center/radiusM), ring (center/minRadiusM/maxRadiusM), polygon (coordinates/isClosed), or freeform (points). Legacy polygon points normalize to coordinates. Empty arrays and explicit zero coordinates/radii remain real zero/empty values. No center, radius, coverage or polygon points are invented. Missing/null coordinates, out-of-range coordinates, unsupported geometry, invalid radii and URL-style colors fail closed.

Map object allowlist: objectId, assetId, layerId, name, category, quantity, coordinates, rotation (nullable), scale (nullable), isVisibleOnMap. Coordinates contain lat/lng and optional altitude.

`objects` is the same full map-object inventory plus nullable description/notes, unitLabel, protectionType, and nullable typed card. Cards allow only compound (`kind`, `postType`, `personnelCount`, `accountability`, `armament`, `weaponUnits`, `sectorOrRange`, `azimuth`), weapon (`caliber`, `ammunitionType`, `operationMode`, `moduleCount`, `isManual`), detection (`frequencyRange`, `detectionMode`, `rotationSpeed`, `fieldOfView`, `hasThermalImager`), and EW (`frequencyRange`, `actionRange`, `azimuth`) properties. They come from the frozen document only.

Free text is intentionally preserved as text, including any human-entered amounts. `manual_text_review_required` asks the user to review it before sharing. UI must not interpret it as HTML, links, or image resources. Reports state that automatic checking was not performed and make no protection-effectiveness claims.
