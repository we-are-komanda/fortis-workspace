# FRC-03 independent verification logs

Date: 2026-09-21. Every `.command.json` records the exact prefixed command, working directory and child exit code. Raw output is retained without substituting a parent wrapper exit status. `*-final` files are authoritative after fixture repairs.

| Evidence | Result |
|---|---|
| `focused-03-final.log` | 9 PASS |
| `regression-01-02-04-06-final.log` | 88 tests: 87 PASS, 0 FAIL, 1 PostgreSQL opt-in SKIP |
| `browser-03-06-final.log` | 27 PASS, no skips (FRC-03 14 + FRC-06 13) |
| `full-suite-final.log` | 86 files, 274 tests: 211 PASS, 6 FAIL, 57 opt-in SKIP |
| `baseline-signatures.json` | Six exact historical exception/assertion/full-stack signatures match `../../frc02/pre-frc02-failure-signatures.txt`; only absolute frontend root normalized |
| `typecheck-final.log`, `changed-lint-final.log` | Exit0; lint includes all15 changed TS/JS/CJS files |
| `build-final.log` | Exit0, isolated copied source/dependencies; active dev server/working `.next` untouched |
| `backend-tests-final.log`, `backend-build-final.log` | Exit0 after final test-fixture cleanup change |
| `postgres-independent.log` | Three top-level FRC-03 tests plus six provisioning subcases PASS against disposable local PG, no skips |
| `malformed-create-probe.log` | Five malformed acknowledgements preserve old current context and immutable retry; 5PASS |
| `late-create-identity-probe.log` | Changed identity returns null navigation result; PASS |

`frontend-final-source-manifest.json` and `build-final-source-manifest.json` match exactly (457 files). `backend-final-source-manifest.json` captures241 files. `source-consistency.json` compares these to the later current manifests. The final documentation refresh changes only backend `README.md`; frontend changed only `test/playwright/frc03-live.cjs` for the root-owned real-browser timeout configuration. Production drift is zero; the updated harness separately passes `live-harness-final-lint.log`. Do not rewrite the tested manifests to imply the later harness was part of the earlier build.

Initial broad logs without `-final` are deliberately retained: one runtime fixture omitted explicit enterpriseId, one FRC-06 browser fixture returned unscoped rows for enterprise queries, and the CommonJS live harness needed a narrow lint directive. Repairs preserved every behavioral assertion. The first full run was210 PASS/7FAIL/57SKIP, becoming211 PASS/6 historicalFAIL/57SKIP. Initial browser was26 PASS/1FAIL, then27 PASS. No additional failure was dismissed as baseline.

Earlier independent browser RED/GREEN development logs are one directory above: `browser-independent-initial.log` included selector mistakes (not product findings); `browser-independent-red.log` is the corrected2PASS/9FAIL baseline; `browser-independent-current.log` was11PASS/known-modalFAIL; `browser-independent-green.log`12PASS; `browser-independent-14.log`14PASS. `shared-list-error-red.log` preserves the actual dialog regression. `operator-independent-unit.log` records four top-level provisioning validation/CLI tests; the restricted-cache attempt is retained separately and was not treated as an application failure.

This evidence does not claim global frontend green, production readiness or the root-owned real browser gate. Skips remain skips. See [independent review](../independent-review.md) and [acceptance plan](../acceptance-plan.md).
