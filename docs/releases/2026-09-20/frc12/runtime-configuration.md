# FRC-12 configuration and publication boundary

Intake is **disabled by default**. No production form, SMTP recipient or policy was enabled during this run. Synthetic fixtures are not legal text.

## Backend server-only environment

The existing envconfig parser accepts `APP_DEMO_ENABLED`, `APP_DEMO_CONSENT_VERSIONS` (comma separated allowlist), `APP_DEMO_ALLOWED_ORIGINS` (exact HTTPS origins), `APP_DEMO_TRUSTED_PROXY_CIDRS` (only the actual BFF/ingress peers), `APP_DEMO_SMTP_ADDRESS` (host:port), `APP_DEMO_SMTP_USERNAME`, `APP_DEMO_SMTP_PASSWORD`, `APP_DEMO_SMTP_FROM`, `APP_DEMO_SMTP_TO`. No recipient or credentials are read from the browser. SMTP STARTTLS and certificate validation are mandatory. Password is environment-only, excluded from YAML.

The existing `webapp` work mode runs the outbox worker. Shutdown cancels pending sends and waits for worker exit. Lead acknowledgement follows DB commit; delivery failure is visible as pending/retries or failed after the 24-hour delivery horizon. External email is at-least-once: stable event/Message-ID assists deduplication, but exactly-once delivery is not promised.

Trusted operators may run the binary locally with `APP_WORK_MODE=demo-request-registry ./app --limit 100 --offset 0`. It requires process OS/database credentials and produces paginated sensitive JSON; it is not an HTTP endpoint and is not granted to ordinary members. Keep output in access-controlled storage. The generic application database constructor currently applies migrations at startup; review the release migration plan before invoking any process against staging/production. No such invocation was made in this run.

## Frontend server-only environment

`FORTIS_DEMO_REQUESTS_ENABLED=true`, `FORTIS_DEMO_FORM_ORIGIN`, `FORTIS_DEMO_CONSENT_VERSION`, `FORTIS_DEMO_CONSENT_TEXT`, `FORTIS_TRUSTED_CLIENT_IP_HEADER` and the existing validated backend target are required. Public GET exposes only enabled state and owner-supplied consent text/version. It cannot list submitted records. Browser POST must have the configured exact Origin and JSON body no larger than16KiB. The edge must overwrite the configured client-IP header; a single valid IP is forwarded to the backend. The generic API proxy strips browser-supplied Origin/IP headers. The backend must trust only that authenticated network path, otherwise it uses its direct socket peer for rate limiting.

Local HTTP is allowed only through the existing explicit development setting; no production bypass is introduced. Production ingress/TLS/header overwrite and private backend access must be evidenced before publication.

## Required owner/runtime evidence

- Approved published consent text/version and privacy/retention policy; named responsible operator and access process.
- Configured real notification channel/recipient; controlled delivery acceptance and failed-delivery alert routed to the responsible person (logs alone do not prove an alert).
- Deployment check that both sides enable the same consent version and correct origin, and backend notification configuration is complete. Missing config must keep publication disabled.
- Retention/cleanup of leads, outbox, expired idempotency and inactive rate rows, without deleting unknown production data.
- Tested persistent PostgreSQL and worker restart/recovery in the deployed artifact.

The FRC12 code tests use synthetic emails under example.test and fake notifier implementations. No actual external email was sent. Local PostgreSQL tests use isolated temporary schemas.
