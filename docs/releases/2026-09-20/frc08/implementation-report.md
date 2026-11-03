# FRC08 implementation and local acceptance

Two explicit saved references now drive comparison end to end. Both operands are authorized before calculation; immutable names, timestamps, composition, exact cost, provenance and budget retain the same revision identity. Current catalog and project edits do not change an older comparison. No new schema or dependency was needed.

Frontend selection survives list refresh, pagination and later saves. Dirty projects require confirmed Save-and-compare or explicit saved-version comparison. A newer edit during saving remains dirty. Late responses, identity/enterprise changes and known selected-resource denial clear or invalidate financial results. Historical sides repin only when they match the pre-save active version. The existing strict logout save guard remains intact.

The result shows exact B−A and rounded percentage, completeness, quantities, stable-ID layer/type groups, line changes, frozen provenance and budget. Independently created IDs remain separate even when labels match. Unknown prices remain unknown; zero baseline has no percentage. Price is never described as effectiveness or sufficient protection.

Backend details: [implementation](backend-implementation.md), [API](backend-api.md). Frontend details: [implementation](frontend-implementation.md). Three observed review defects were corrected and verified in [independent review](independent-review.md). Criterion decisions are in [acceptance criteria](acceptance-criteria.md); full evidence in [test evidence](test-evidence.md).

The local FRC08 acceptance is separate from production/runtime readiness. CMP09's proposed viewCost roles remain deferred by ADR-0017. FRC10 remains required before reports/SAVE09 can be accepted.
