# FRC-03 independent review — 2026-09-21

Reviewed the complete frontend/backend working changes from accepted FRC-06 (`frontend a56d128`, parent `0560b79`), including operator provisioning, project-name validation, workspace listing/pagination/creation, identity boundaries, shared save/list consumers and the empty-layer map CTA. The reviewer implemented the independent workspace browser tests and two honest regression fixture repairs, but did not implement production code. Root/implementers must review the test changes separately.

**No open concrete production findings remain.** Two defects discovered during implementation were reproduced and closed:

| Finding | Reproduction | Closure |
|---|---|---|
| P2: A successful create returned its navigation result after A→B while the subsequent list refresh awaited completion. | Actual store probe: POST acknowledgement → hold list GET → change identity → release GET; result originally contained A's created ID under B. | Final identity-generation and committed-project-reference check returns null. Original independent probe passes; permanent unit `create returns no navigation result after identity changes during its list refresh` passes. |
| P2: Moving list errors to `listError` left the existing VariantsModal reading only the shared save error; HTTP503 appeared as an empty successful list. | Independent Chromium rendered workspace error but dialog text “Пока нет сохранённых вариантов” with no failure. `shared-list-error-red.log` retains the failure. | Modal shows list failure and explicit retry; the list body does not show empty success on error. Permanent independent modal scenario passes within final 27/27 browser run. |

Additional root-discovered issue: an empty first project had no Add-layer entry because the existing button was inside selected-layer rendering. Independently inspected the narrow empty-layer CTA: it appears only with zero layers and no wizard, uses the existing quota-checked `createProjectLayer` path, and introduces no new save/domain logic. Root owns its real Next→Go→PostgreSQL browser evidence; this review does not manufacture a separate live-run result.

Operator review found no additional defect: existing-user lookup and lock, enterprise plus membership transaction, rollback on membership write failure, composite-key uniqueness, safe exact replay, refusal to restore revoked membership or adopt a different recipient, explicit GIS coordinates including valid zero, sanitized failures, identifier-only output, no HTTP/JWT privilege expansion. Independent PostgreSQL tests exercised rollback, eight concurrent exact retries, changed payload/user conflicts, privacy-preserving replay and revocation, not just mocked persistence. Existing identical entity+membership is a semantic safe replay; no original-provisioning provenance is claimed.

Frontend review checked server enterprise/page query and filtered totals, stale page/enterprise/identity rejection, authorized selection revalidation and user-scoped persistence, retained create input and immutable retry, old context unchanged until acknowledgement, authoritative ID/version and explicit ownership, no baseObject-based adoption, fresh explicit open, FRC-06 dirty choices and separated list failure. The 120-character rule uses Unicode code points consistently with Go; existing historical names may be preserved unchanged, while newly supplied names are validated. Loading/empty/error/forbidden and >100 enterprise reachability have code and targeted coverage.

Two failures in the first broad run were obsolete fixtures, not waived regressions. Runtime retry fixture lacked explicit enterprise ownership and therefore sent no PUT under the new fail-closed guard. FRC-06's browser fixture ignored enterprise/offset/limit and returned E rows for an F query, correctly rejected by the new boundary. Fixtures now model the real contract; all original assertions remain. Initial failing logs are retained. The live CJS harness lint directive addresses CommonJS requires only.

## Independent verification

| Check | Result |
|---|---|
| FRC-03 store/API focused | 9/9 PASS |
| FRC-01/02/04/06 regression group | 88 tests: 87 PASS, 0 FAIL, 1 opt-in PostgreSQL SKIP |
| Rendered Chromium FRC-03 plus FRC-06 | 27/27 PASS (14 workspace + 13 save/recovery) |
| Complete frontend tests | 274 tests: 211 PASS, 6 FAIL, 57 opt-in SKIP |
| Historical signatures | 6/6 exact exception/assertion/full-stack matches; only absolute root normalized |
| Typecheck and lint of all changed JS/TS files | PASS; 15 files linted |
| Isolated frontend production build | PASS |
| Whole backend tests/build | PASS; separate opt-in evidence below |
| Independent real PostgreSQL FRC-03 | 3 top-level tests and 6 provisioning subcases PASS, no skips |
| Malformed CREATE summary probe | 5/5 PASS: empty ID, missing/zero/fractional version, wrong enterprise preserve old project/baseline/active ID and frozen attempt |

Exact commands, raw logs and manifests: [verification logs](verification-logs/README.md). Durable extra probes: `verification-logs/late-create-identity-probe.ts`, `verification-logs/malformed-create-probe.ts`; run from frontend with `rtk proxy node --import tsx ../docs/releases/2026-09-20/frc03/verification-logs/<probe>.ts`.

Limits: synthetic browser checks use actual production components/stores/API adapters with intercepted transport; they do not prove DB commit. The independent PG run uses the disposable local cluster and isolated schema, not user/root/root2 or production data. Root owns the canonical CLI→Refresh→first-create→map-edit→save/reload→pagination/cross-user gate. Full frontend status remains FAIL because six historical failures are still present. No deployment, production database migration, push or commit was performed by this reviewer. Source hashes show no production drift; the final live-harness timeout adjustment is separately recorded and linted.
