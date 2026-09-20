# FRC-04 implementation report

Status: **CODE PASS / RUNTIME BLOCKED**. Code acceptance2026-09-20 by root after independent review by spec_inventory. REV01–10 and scoped project audit pass on local PostgreSQL16; no open review defect. Production migration/deployed artifact/retention evidence remain unavailable.

Minimal owning-module changes preserve the complete validated DefenseProject document without promoting extensions into authority. Immutable revisions, mandatory expected version, actual budget snapshot, scoped24h idempotency and same-transaction audit extend the existing repository/service. Historical reads and retries reauthorize current ownership/membership. Current-known-version-only backfill preserves old schema1 defaults and does not invent older history.

Frontend preserves circle/polygon extensions, forwards explicit projectVersion and Idempotency-Key, exposes version-pinned load and caller-retained creation keys. Complete synthetic frontend fixture round-trips through real Go/PostgreSQL/export/frontend parsing with all original business fields unchanged; authoritative metadata and separate configuration name are checked separately.

Independent review found two defects during implementation: nil legacy geometry panic and concurrent expired-receipt replacement race. Both were reproduced in permanent tests, fixed minimally, and independently retested on PG. Audit insertion failure rolls back mutation; deleted/revoked resources cannot be recovered through receipt replay. No remaining known tenant/data-loss regression.

See [backend-evidence](backend-evidence.md) for REV01–10, transaction/audit tests and exact commands; [test-evidence](test-evidence.md) for integrated frontend/build/API proof. Contract decision: knowledge-base ADR-0018. Existing direct budget API integration is intentionally FRC07, not a reversed dependency; final release must replace its independent write.

Generated scoped OpenAPI validates. Whole pre-existing API annotations outside project/demo modules still produce invalid response-header schemas and are recorded for FRC13; no whole-API validation PASS claimed. Local commits deferred while shared DI/fixtures/swagger/client hunks overlap independently accepted FRC12; file hashes retain reviewable scope.
