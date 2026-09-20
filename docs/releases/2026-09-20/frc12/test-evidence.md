# FRC-12 acceptance evidence

Observed working tree on2026-09-20; source-manifest.tsv identifies files. All shell commands use rtk proxy. No production evidence is claimed.

| Requirement | Executed evidence | Result |
|---|---|---|
| LEAD01/02 | actual browser+BFF+Go+PG; DB constraint failure leaves no row and inputs unchanged; successful submit commits | PASS local |
| LEAD03 | fake delivery failure pending→retry→failed tests; cancellation/lease recovery probes | PASS code; actual SMTP and alert runtime blocked |
| LEAD04/05 | lost committed browser response then same-body/key retry returns same receipt/one row; eight concurrent DB submits serialize | PASS |
| LEAD06 | form six browser cases, backend invalid consent/email/length/unknown fields/malformed JSON | PASS |
| LEAD07 | rolling IP/email limits concurrent PG and HTTP429 Retry-After; client validates integer/date | PASS |
| LEAD08 | public GET405; unknown registry unauth401/auth404; local privileged CLI only | PASS |
| LEAD09 | escaped HTML/newlines in form and plain SMTP body; no user-controlled headers/recipient | PASS |
| LEAD10 | disabled/missing-config closes intake; check_publication.py + test_publication.py two tests | PASS code; owner/runtime gate open |

Agent commands and counts are in backend-evidence.md and frontend-evidence.md. Root additionally ran full Go default243 top-level+84 nested PASS21SKIP, unit275+84 PASS21SKIP, build/vet PASS (opt-in missing-env skips reported, not counted as integration success). Independent backend selection14 top-level+9 HTTP subcases PASS. Public-session regression tests preserve authenticated user on401/403/404. Changed frontend lint, non-incremental types and production build passed; latest build14.6s compile+4.8s types.

Actual chain: `FRC12_BROWSER_SERVER=true FRC12_TEST_DSN=... go test ./cmd/app -run TestFRC12BrowserServer -count=1 -v`, Next development3111 with synthetic consent and loopback8093 target; `node test/playwright/frc12-live.cjs` PASS. The test driver is opt-in, isolated synthetic schema, fake notifier and test-only mutation endpoints; these are not application routes. Screenshot `/private/tmp/fortis-frc12-browser/receipt.png`. Both owned servers stopped cleanly. Never expose these test fixtures publicly.

Standalone pinned Swagger0.36.6 generated all models; transitive scoped FRC12 paths saved in openapi.json and validated. Full API currently exposes unrelated malformed old response annotations, tracked for FRC13. API source remains UI annotations/DTO, not this derivative artifact.

No actual SMTP/TLS/alert delivery, deployed private operator access, production migrations, owner consent/retention or ingress-header overwrite acceptance was run. These are runtime gates, not PASS.
