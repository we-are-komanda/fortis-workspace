# FRC-12 frontend boundary plan

Spec: FRC-12 and shared contracts. The root owns these files; FRC-11 owns landing until handoff. Preserve same backend resolver and transparent upstream errors.

- New `frontend/src/app/api/public/demo-requests/route.ts`: safe GET form configuration (no registry), POST with explicit enable/config, exact allowed Origin, JSON-only body capped while streaming at 16 KiB. No durable-commit acknowledgement is invented locally.
- Root-owned `frontend/src/modules/home/infra/demo-request-api.ts`: typed accepted response, caller-retained Idempotency-Key. UI remains idle/submitting/error until a real 200/201 payload contains requestId and received status.
- Existing `frontend/src/modules/drone-defense/infra/backend-proxy.ts`: only explicit server `init.headers` may add validated Origin and X-Forwarded-For. Raw incoming headers on generic `/api/v1/*` cannot bypass the form boundary.
- `FORTIS_DEMO_REQUESTS_ENABLED`, `FORTIS_DEMO_FORM_ORIGIN`, `FORTIS_DEMO_CONSENT_VERSION`, `FORTIS_DEMO_CONSENT_TEXT` default to disabled/unset. Text/version are owner-provided; no legal text is invented.
- `FORTIS_TRUSTED_CLIENT_IP_HEADER` names a header overwritten by a verified edge proxy. Missing/invalid configuration or IP fails closed. Local explicit development may use 127.0.0.1 for synthetic tests only. The Go peer must independently be in its configured trusted proxy CIDRs before honoring XFF.

Tests: default disabled; missing config; wrong/missing Origin; oversized streamed body; content type; forged/malformed client IP; exact key/body/Origin/IP forwarding; durable acknowledgement shape; upstream 400/409/429/503 and Retry-After preserved. Real DB+outbox behavior belongs to backend tests and integrated acceptance, not HTTP stub evidence.

Runtime gates: approved consent text/version, trusted edge header stripping, configured notification channel/recipient and accountable operator, approved retention. No enablement, production traffic or real message delivery occurs during this run.
