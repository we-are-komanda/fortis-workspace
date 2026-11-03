# FRC08 criterion decisions

Reviewer/coordinator: root, with independent reviewer; 2026-09-21. Status applies to the authorized membership contract (ADR-0017) and pinned comparison (ADR-0024).

| Criterion | Status | Evidence |
|---|---|---|
| CMP01 finance A7/B3 | PASS | Real API+ordinary workspace controls:47500000/55000000 minor;7500000 and15.79%, frozen side identities/budgets. |
| CMP02 current A8 preserves A7/B3 | PASS | Real current update and byte-equivalent pinned comparison; rendered list-refresh/save regression. |
| CMP03 A=0 | PASS | Real API, exact domain and response-boundary checks:delta present, percentage null. |
| CMP04 unknown B | PASS | Real API, PostgreSQL and rendered checks:unknown total/delta/percentage, known subtotal retained. |
| CMP05 foreign/revoked side | PASS | PostgreSQL both operand orders/current membership revocation; real foreign404; browser existing and late money cleared after known denial. No partial response. |
| CMP06 accessible different enterprises | PASS | Real PostgreSQL400 incompatible_projects before cost materialization. |
| CMP07 same name/different IDs | PASS | PostgreSQL identity fixture, pairing unit tests and rendered separate labeled rows. |
| CMP08 changed catalog | PASS | Persisted PostgreSQL snapshot unchanged; query counter current-catalog reads=0. |
| CMP09 viewer/viewCost | NOT APPLICABLE | Proposed roles deferred/superseded by accepted ADR-0017. Current resource membership is enforced; no claim that new financial RBAC exists. |
| Additional pinned versions/aliases | PASS | Required positive versions, alias conflicts400, identical refs400, same project distinct revisions allowed. |
| Dirty Save / explicit last-saved | PASS | Rendered confirmed/failure/ambiguous/newer-edit cases; historical A7/current8 saves9 asA7/A9. Shared logout strictness retained. |
| Async/enterprise/identity/access transitions | PASS | Independent20 browser cases; unrelated denied C control preserves authorizedA/B. |
| Composition/budget/provenance/limitations | PASS | Rendered groups/lines and actual screenshot; real frozen budget; unsupported calculation binding503. No efficacy inference. |

Logs and limits: [test-evidence.md](test-evidence.md). Synthetic browser fixtures complement actual PostgreSQL and real UI evidence; they do not substitute for them.
