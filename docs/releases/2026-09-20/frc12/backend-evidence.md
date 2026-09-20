# FRC-12 backend evidence — 2026-09-20

Status: module implemented and locally verified with synthetic PostgreSQL. Root owns shared config/DI/router, process lifecycle, trusted operator CLI wiring and integrated release acceptance. No commit, deployment, real email or external provider call was performed by this implementation.

## Ownership and result

- `backend/internal/modules/demo_request/`: domain validation/normalization, application orchestration, GORM persistence, SMTP port/adapter and HTTP/CLI presentation.
- `backend/migrations/1789913977_demo_requests.{up,down}.sql`: requests, delivery outbox, idempotency receipts and rolling rate windows.
- `backend/cmd/app/frc12_backend_test.go`: real DB/application/HTTP acceptance scenarios. Module-local tests cover domain, persistence races and safe email formatting.
- No edits to existing config/router/DI, existing modules or existing tests in this subtask. Shared integration is delegated to the root agent.

Normalized input is committed with an outbox event and operation-scoped 24-hour receipt in one transaction. Request and event IDs are UUIDs. The receipt row serializes retries; the normalized email rate row serializes competing accepted requests. IP attempts are separately committed before JSON/field validation, including malformed payload attempts. IP rate keys and email rate keys contain hashes, not original values. Actual lead fields exist only in the protected DB/explicit operator output and intended notification body.

Limits: 5 attempts per rolling 10 minutes per trusted IP; 3 accepted requests per rolling hour per normalized email. Replays do not count as another accepted request. Reusing an expired receipt permits a new request. Expired window timestamps are discarded on the next use; retention/maintenance of dormant control rows and lead data must be included in the owner's deployment policy.

Worker claims use `FOR UPDATE SKIP LOCKED`, a one-minute lease and a unique lease token. A stale worker cannot acknowledge a newer claim. Delivery deadlines are 30 seconds; failure retries are 1/5/30 minutes then hourly, capped at 24 hours. Exhaustion persists `failed` and emits an error with event/request ID and attempt count only. SMTP uses mandatory STARTTLS with certificate verification and bounded dialing; message headers use only configured sender/recipient, fixed subject and stable event ID. User text is a quoted-printable plain-text body. External delivery remains at least once; stable Message-ID does not promise exactly-once SMTP.

POST requires an exact allowlisted browser Origin. Only configured trusted proxy CIDRs may supply X-Forwarded-For; malformed/missing trusted proxy input fails closed. Direct peers cannot evade limits with forged forwarding headers. Config permits HTTP browser origin only on localhost/loopback. Body is capped at 16 KiB, must be one JSON object and cannot include unknown destination fields. Failures have the existing status/errors response plus additive error code/requestId/retryable/details; 429 includes Retry-After. GORM SQL logging is disabled for the module to avoid parameter/PII disclosure.

There is no registry HTTP route. `ui.WriteRegistry` is callable only from the local trusted process that the root wires. OS execution permission and DB administrative credentials are the operator boundary; ordinary JWT membership grants no access. The paginated JSON output deliberately contains requested lead data and is not an application log.

## TDD evidence

1. Domain RED: `request not normalized`; `rolling retry = 0s`. GREEN after normalization, consent validation and scheduling logic.
2. Repository RED on real PostgreSQL: expected one persisted row, got zero; expected eight serialized timestamps, got zero. GREEN after transactions and row locking. Tests also confirm rollback, a single concurrent worker claim, lease reclamation and stale-completion rejection.
3. Application RED: Ready false / demo requests unavailable. GREEN after transaction/idempotency/rate/outbox orchestration.
4. SMTP RED: valid configuration unexpectedly not ready. GREEN after strict configuration and message construction. No network send was exercised.
5. HTTP RED: valid request expected 201, got 503. GREEN after Origin/IP/body/JSON/field/error handling.

The first PostgreSQL invocation was blocked by the filesystem/network sandbox; the authorized retry accessed only the root's isolated loopback cluster. Initial cmd/app compilation briefly hit another agent's incomplete FRC-04 `saveProject` addition; isolated FRC-12 test-file execution passed, and the subsequent complete package suite passed after that work became compilable.

## Commands and actual results

All Go commands used `GOCACHE=/private/tmp/fortis-frc12-gocache`. DB commands used `FRC12_TEST_DSN='host=127.0.0.1 port=55434 user=fortis_test dbname=postgres sslmode=disable'`, the root-created disposable PostgreSQL 16 cluster. Each test uses a new committed random schema and drops it on cleanup, so independent DB connections and concurrent transactions are real.

| Command | Result |
|---|---|
| `go test ./internal/modules/demo_request/domain` | PASS |
| `go test ./internal/modules/demo_request/infrastructure` with test DSN | PASS |
| `go test ./internal/modules/demo_request/infrastructure -run TestSMTP -count=1` | PASS; no external send |
| `go test ./cmd/app/frc12_backend_test.go -count=1` with test DSN | PASS |
| `go test -race -tags=unit ./...` with FRC12 test DSN | PASS across backend packages; existing other opt-in DB/browser tests without their env remain skipped |
| `go build ./...` | Exit 0; sandbox warned that global module stat-cache writing was unavailable, without blocking compilation |
| `gofmt -w internal/modules/demo_request cmd/app/frc12_backend_test.go` | Completed |

Nine new top-level behavioral tests plus HTTP table subcases verify the module. These results cover the observed working tree, not a future committed/deployed SHA. Root records the final candidate SHA and repeats integration checks after shared wiring.

## Acceptance scope

| ID | Local evidence / remaining limit |
|---|---|
| LEAD-01 | Real DB row + outbox + 201 HTTP response; frontend evidence owned by root |
| LEAD-02 | Actual DB outbox constraint failure rolls back lead/receipt and returns unavailable |
| LEAD-03 | Injected provider failure leaves pending retries, eventually failed; real alert delivery unverified |
| LEAD-04/05 | Normalized replay and eight concurrent same-key submits yield one request; conflicting payload returns conflict |
| LEAD-06 | Domain and HTTP invalid consent/version/email/length reject; unknown fields/malformed body rejected |
| LEAD-07 | Persisted rolling IP limit and eight concurrent same-email submits produce exactly three accepted requests; HTTP 429/Retry-After |
| LEAD-08 | No module HTTP registry/get route; local operator output only; root verifies mounted routing |
| LEAD-09 | User newline/HTML content remains plain email body; no header injection, configured recipient only, no SQL payload logs |
| LEAD-10 | Module returns 503 unless enabled, consent versions and SMTP configuration are valid; root must also gate published policy text and trusted ingress |

## Runtime gates and rollback

Production remains disabled until the owner supplies the published consent/policy/version, retention and deletion policy, approved SMTP recipient/provider configuration, trusted ingress/header overwrite evidence, operator/support process and monitoring recipient. SMTP connectivity/TLS/delivery, exhausted-outbox alert delivery and actual deployed worker lifecycle were not verified with real credentials. A fake notifier is test-only and is never a production fallback.

Rollback before customer collection: disable collection/worker and revert module wiring. The down migration removes lead/outbox/control data; do not run it after real collection without the owner's backup/retention decision. Keep the tables and use a compatible application rollback/roll-forward once customer writes exist.
