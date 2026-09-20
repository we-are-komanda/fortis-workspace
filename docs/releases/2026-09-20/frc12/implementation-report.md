# FRC-12 — durable demo request intake

Status: **CODE PASS / RUNTIME BLOCKED**, root acceptance 2026-09-20. ADR-0019 governs the contract. Collection remains disabled by default.

The public form validates owner-supplied consent and fields, keeps retry input/key in memory and acknowledges only a validated committed receipt. Browser → BFF → Go → PostgreSQL commits lead/outbox/idempotency atomically. Delivery retries survive request completion; SMTP requires STARTTLS. Persistent rate limits, exact Origin, trusted proxy handling, private operator registry and generic error/requestId boundaries are implemented. Public calls do not alter an authenticated workspace identity.

Independent review found a public401 logout defect: regression reproduced, root fixed the public helper scope and reviewer verified401/403/404 preserve identity. Separate backend review found no remaining issue; plaintext SMTP refusal, cancellation and worker lease recovery passed. Real browser testing deliberately lost a committed response, then retried the same key and got the same receipt with exactly one row.

See backend-evidence.md, frontend-evidence.md and test-evidence.md for executed checks. runtime-configuration.md records owner policy, consent/retention, SMTP recipient/delivery/alert, TLS/ingress and deployed worker gates. No real email, production configuration or migration was performed. Local PG schema cleanup completed. Local commits deferred because shared routing/landing/client hunks span accepted04/11/12; no push.
