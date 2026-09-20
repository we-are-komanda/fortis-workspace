# FRC-09 backend plan

Authority: FRC-09/shared contracts and ADR-0017/0018. Root approved implementation after FRC-04 code acceptance; production storage/scanner remains a runtime gate.

1. Add validated provenance and optional exact money fields to the existing asset aggregate and all DTO/JSONB mappings. Preserve absent versus explicit-null minor prices, legacy prices, typed cards and demo quality. Server supplies provenance author/time/revision and resolves authorized source-document revision/checksum.
2. Add immutable document revision/checksum/status/commercial/deletion metadata. Existing external URLs become unavailable metadata and are never emitted or fetched.
3. Add a private local store and bounded configured ClamAV executable adapter using the standard library. Quarantine files until MIME validation and a successful scan; unavailable scanning never publishes a document. No scanner installation or external service.
4. Preserve routes, replacing metadata-only creation with one multipart file (10 MiB maximum). Download checks persisted parent access on every request and optional supplied parent identity, returning attachment bytes only for ready documents. Document writes/deactivation and audit are atomic; authorization is rechecked inside that transaction.
5. TDD: domain invariants, actual PostgreSQL round-trip/permissions/audit rollback, private filesystem/checksum, fake-scanner clean/infected/unavailable, MIME/body boundaries and same-name immutable uploads. Existing FRC-02 fixture expectations are coordinated with root.

Root owns frontend, shared DI/config/router/server body limit. No real data, production writes, real scanner claim, deployment, commits or pushes in this subtask.
