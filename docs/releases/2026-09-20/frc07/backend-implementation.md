# FRC07 backend implementation

The shared project `Commit` transaction is the authoritative budget gate. It rechecks membership, locks the current project, checks the shared version, reads the current budget, evaluates the exact candidate, and only then writes the project, budget, immutable revision, audit event, and optional idempotency receipt. Failure rolls all of them back.

Budget domain values now retain exact minor-unit limits. Pure domain projection/check rules use the existing `CostProjection` and integer arithmetic. The document adapter reads legacy decimal millions without a float round trip and writes canonical string kopecks. Existing cost-v1 calculation validates selected prices and quantities before writes, including unlimited projects.

The application implements pinned projection reads, versioned configuration changes, and read-only full-candidate checks. HTTP controllers expose the approved shared schemas and reuse one financial error mapper. Budget PUT reuses the project response mapper so the frontend receives the canonical saved snapshot. Explicit copied budget provenance is carried through project creation and idempotency hashing; imports and embedded JSON cannot select a server budget.

Regression fixtures now seed canonical unlimited budgets directly where needed. Earlier rollback assertions expect the unchanged unlimited row instead of an absent row. The FRC05 invalid-price scenario now verifies rejection at project creation and no persisted project, because FRC07 moves that validation to the write boundary. Obsolete single-asset/float budget HTTP tests were replaced by actual PostgreSQL full-candidate, version, authorization, rollback, and clone tests; cost/compare controller tests remain.

No migration, public provisioning/admin API, new dependency, or unrelated data cleanup was introduced. Backend production source was frozen before the root-owned live browser run. Browser evidence is maintained separately by the parent task.

See [backend-api.md](backend-api.md) and [backend-verification.md](backend-verification.md).
