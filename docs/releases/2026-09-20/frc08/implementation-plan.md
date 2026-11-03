# FRC08 active implementation plan

Begins after local accepted FRC07 parent5008d25b1c43d46598df355c2abb48570f78092f; FE6838dd1fc1931b0ae220f9ad6a76179876c5934b; BE387572a1310f11cc175f8db6ca1297e9e8264eef; KB00c5aaa47d503d393ddbee22cf99468b17736767. No08acceptance yet.

Approved API/semantics: ADR-0024 and updated shared CompareResult. The existing compare path rereads mutable current projects and converts exact costs to legacy floats; replace that path with pinned revisions and existing immutable cost/budget projections. Keep shared legacy report code unchanged until FRC10 unless a proven security regression requires repair.

1. Backend owner integration_research: test failing pinned/exact/access cases; implement controller/query/result and reusable frozen project projection; disposablePG regression and fullGo.
2. Frontend owner frc06_acceptance_tests: reuse workspace compare + calculator entry, strict response validation, pinned selection/date/version, exact cost/budget/line/group comparison and explicit dirty Save/last-saved. Minimal existing patterns; no new dependencies/model.
3. Independent frc06_verification: separate rendered test file, CMP criteria + additional race/dirty/error probes, source review. No production file overlap.
4. Root: contract/ADR, actual Next→Go→PG scenario, final full/regression/type/lint/isolatedbuild, source hashes and accepted-stage docs/commits. No final status inferred from mocks.

CMP01–08 required; CMP09's proposed RBAC is superseded/deferred under accepted ADR0017 membership contract. Exact money, stable IDs, no inferred protection, unchanged historical revision after current/catalog updates, and authorization before both prices remain mandatory. Unknown and zero cases cannot become cheaper/Infinity.

After accepted08 proceed10→13→14 without push/deployment/productionDBmutation. Existing user5432/root/root2 untouched. FRC07raw logs retain original whitespace; parent commit diff-check reported whitespace solely in raw Go/Playwright/build output, while product source checks passed. Do not rewrite raw evidence to manufacture a clean log diff.
