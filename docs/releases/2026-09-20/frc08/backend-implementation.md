# FRC08 backend implementation

The existing compare route now accepts explicit A/B revision references and returns their frozen exact financial projections. The budget application service loads and authorizes each immutable project once, checks same-enterprise/distinct-reference compatibility, and then evaluates both sides. A private helper extracted from `ProjectCost` reuses the existing version/algorithm cache for the already-loaded project. Budget projections use the same exact cost object and the budget from that revision's snapshot.

A domain comparison value calculates signed minor-unit and percentage differences with `big.Int`/`big.Rat`. It preserves unknown totals and supplies deterministic warnings for unmatched IDs and missing/different provenance. The UI layer only maps the approved DTOs and errors. No catalogue lookup, current budget lookup, or inferred coverage result participates in comparison.

Obsolete comparison-only float diff models, mappers, and tests were removed. The report-shared structural profile builder, DTOs, and tests remain. FRC02 compare requests now pin versions; the in-memory port has no revision history, so its former identical-current-project success case is replaced by the actual PostgreSQL identical-reference rejection test. Foreign/revoked access regressions remain.

No schema migration, dependency, public operator/admin route, or RBAC change is included. Production source was frozen before the root-owned real browser run. Browser evidence and the final release acceptance are recorded separately by the parent task.

See [backend-api.md](backend-api.md), [backend-verification.md](backend-verification.md), and [backend-changed-files.md](backend-changed-files.md).
