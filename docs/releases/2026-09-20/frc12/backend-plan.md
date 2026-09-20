# FRC-12 backend plan

Scope: durable public demo requests, PostgreSQL idempotency/rate limits/outbox, a bounded SMTP delivery worker, and a local operator registry. No existing mail, outbox or operator service was found. Reuse GORM/rdbms, UUID, existing HTTP error responses and the Go standard library; add no dependency.

1. Domain RED/GREEN: normalized/validated fields, consent allowlist, stable content hash, rolling-window limits and delivery schedule. No user content enters headers or ordinary logs.
2. Infrastructure RED/GREEN against disposable PostgreSQL: lead + outbox + receipt in one transaction; serialized idempotency/email limits; persisted IP attempts; atomic worker lease and stale completion protection. Tests create/drop a unique committed schema using `FRC12_TEST_DSN`.
3. Application: fail closed unless collection is explicitly enabled, approved consent versions and notification configuration are present. Worker uses injected notification port; real adapter uses mandatory STARTTLS. Test notifier sends nothing externally.
4. HTTP: POST only, 16 KiB, JSON/field errors, same-origin allowlist, trusted-proxy CIDRs, no user-configured recipients, 201/200/409/429/503 semantics. Registry has no HTTP route.
5. Local operator process: OS execution permission and existing DB credentials are the administrative boundary. Read-only paginated output is intentional operator output, never a general access log. No JWT member acquires an operator capability.
6. Root integrates module constructors, public POST whitelist, configuration, worker cancellation and CLI work mode. Root owns frontend and overall acceptance.

Acceptance uses synthetic consent `synthetic-test-v1`, reserved `.test` emails and loopback PostgreSQL only. No real email, provider call, customer data, deployment, commit or push. Collection remains disabled in production until owner-provided published policy/consent versions, retention, recipients and trusted ingress are supplied. Exhausted delivery is durable `failed` plus a content-free error event for monitoring; delivered operational alert is a production gate, not claimed by local tests.

Planned module API: `application.NewService(domain.Repository, application.Config, domain.Notifier)`; `infrastructure.NewRepository(rdbms.Executor)`; `infrastructure.NewSMTPNotifier(infrastructure.SMTPConfig)`; `ui.NewController(*application.Service, ui.TransportConfig)`; `Controller.Submit`; `Service.Run(context.Context)`; `Service.DeliverNext(context.Context,time.Time)`; `Service.ListForOperator(context.Context,limit,offset)` and `ui.WriteRegistry(...)` for the trusted CLI.
