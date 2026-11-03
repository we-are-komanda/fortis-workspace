# FRC-10 backend implementation

The old report assembled the current project twice, enriched it from mutable assets, inferred coverage, and hid prices by zeroing float fields. The replacement issues an immutable, render-ready payload from one explicitly pinned revision.

The report application authorizes/loads that revision, reuses an existing report before calculation, obtains its frozen exact cost only for priced mode, derives budget from the same snapshot/cost, and asks the UI serialization adapter to produce the explicit report DTO. A small renderer function port keeps transport serialization out of application/domain; the repository port and GORM model follow existing DDD conventions. No dependency was added.

Migration `1789950000_issued_reports` stores report UUID, project/version/enterprise identity, schema version, mode, map view, generation time, historical actor UUID, and payload JSONB. The unique key is `(project_id, project_version, report_schema_version, hide_cost, map_view)`; revision identity also pins immutable calculator/input bindings. An update-rejecting trigger protects issued rows. Project-revision deletion cascades to reports; historical actor identifiers have no live-user FK.

Issuance rechecks current enterprise membership inside the insert/audit transaction. It locks the project with KEY SHARE and membership with SHARE, matching project-first lock ordering. Revocation before the final lock rejects issuance; revocation after it waits until commit. Project deletion also cannot race the insert past its lock/FK boundary. Failed report insert or audit append rolls back the report and audit event together.

Concurrent identical issuances use INSERT ON CONFLICT DO NOTHING and return the persisted winner, including its report ID, generation time and payload. Only the winning insert appends `report.issue`; reuse/reopen emits no duplicate event. Initial issuance also rereads the stored JSONB representation so subsequent reopen returns the same serialization. Reopen by report ID authorizes current project membership and returns stored payload without loading historical content or invoking any calculator.

The report UI mapper deliberately reads a typed allowlist from the lossless frozen document. This preserves polygon coordinates/isClosed, freeform points, object visibility, optional altitude and frozen typed cards that older domain projections omit. It never queries live asset/enterprise catalogs. Hidden mode has its own response DTO, no financial objects, and can render a revision whose calculator binding is unsupported.

Scope ceilings: no PDF binary storage, background report queue, external map tiles, image proxy, catalog enrichment, inferred coverage/efficacy, report-list endpoint, RBAC additions, or revision cleanup. Persisted render-ready JSON is sufficient for exact reopens; frontend owns SVG/print capture from that payload. Historical enterprise name remains honestly null.
