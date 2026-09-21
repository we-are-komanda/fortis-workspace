# FRC-06 verification — 2026-09-21

Initial frontend: `045db0d` (clean `develop`). Parent reported all four origins synchronized before delegation. No commits, deployment, database mutation, browser execution or dev-server restart by this verification agent.

Every `.command.json` stores exact command, working directory and exit code. `.log` files retain raw output. Commands use `rtk proxy`; test runner is `node --import tsx --test`.

| Check | Result | Evidence |
|---|---|---|
| Initial FRC-06 focused tests | 20 PASS | `focused-initial.log` |
| Initial full frontend suite, 83 files | 208 tests: 163 PASS, 15 FAIL, 30 SKIP | `full-suite-initial.log` |
| Initial FRC-01/02/04 regression group with loopback fixtures | 38 tests: 29 PASS, 8 FAIL, 1 SKIP | `regression-loopback-initial.log` |
| Initial typecheck / lint of FRC-06 commit files | Both exit 0 | `typecheck-initial.log`, `changed-lint-initial.log` |
| Repaired FRC-06 focused tests | 43 PASS | `focused-repaired.log` |
| Repaired FRC-01/02/04 regression group | 38 tests: 37 PASS, 0 FAIL, 1 SKIP | `regression-current.log` |
| Repaired identity/runtime/store/roundtrip/catalog group | 32 tests: 31 PASS, 0 FAIL, 1 SKIP | `regression-repaired-final.log` |
| Repaired full frontend suite | 237 tests: 195 PASS, 6 FAIL, 36 SKIP | `full-suite-repaired.log` |
| Lint of six verification-owned changed files / workspace typecheck | Both exit 0 | `repaired-lint.log`, `repaired-typecheck.log` |
| Isolated production build of initial commit | Exit 0 after allowing build-time font network | `build-network-initial.log` |
| Isolated production build of updated source snapshot | Exit 0 | `build-current.log`, `build-current-source-manifest.json` |

Initial restricted regression run hit `listen EPERM`; it is preserved as `regression-initial.log`, but the subsequent loopback-enabled run is authoritative. Initial restricted build failed only downloading four Google Fonts; `build-initial.log` retains that outcome. Build copies tracked/nonignored sources into a temporary directory and reuses unchanged installed dependencies; workspace `.next`, environment files and dev server are not modified. The updated build source manifest is authoritative: concurrent edits after capture require another final build. At handoff the later changes were `src/shared/lib/identity.ts`, `src/shared/ui/identity-boundary.tsx`, and `src/modules/drone-defense/ui/project-recovery.browser.test.ts`.

## Final stable verification

The authoritative final run is `*-stable`, captured after all seven independent review findings were closed. All eight independent probes (seven defects and URL synchronization) pass; `../independent-review.md` records scope and closure. The `*-final` run immediately before identity isolation found one additional obsolete runtime fixture, retained below as evidence; it is not the acceptance snapshot.

| Check | Final result | Evidence |
|---|---|---|
| FRC-06 focused | 48 PASS, no skips | `focused-stable.log` |
| FRC-01/02/04 regressions | 39 tests: 38 PASS, 0 FAIL, 1 PostgreSQL SKIP | `regression-stable.log` |
| Full frontend suite, 84 files | 250 tests: 201 PASS, 6 FAIL, 43 SKIP | `full-suite-stable.log` |
| Historical failure comparison | Exact exception/assertion/full-stack matches 6/6; only absolute root normalized | `baseline-signatures-stable.json` |
| Typecheck | Exit 0 | `typecheck-stable.log` |
| Lint all changed JS/TS files since pre-FRC-06 `653e109`, including untracked tests | 21 files, exit 0 | `changed-lint-stable.log` |
| Isolated production build | Exit 0 | `build-stable.log`, `build-stable.command.json` |
| Source consistency after all checks | Test/build SHA-256 manifests identical; zero workspace drift | `stable-source-consistency.json`, `stable-source-manifest.json` |

The pre-identity `full-suite-final.log` had 248 tests (199 PASS, 7 FAIL, 42 SKIP). The additional failure was `project-runtime.release.test.ts:114`: it reused a previous saved baseline and expected unverified dirty business content to auto-reload. The deterministic repaired fixture now proves both branches: changed content stays in memory after lost access; clean unverified content may reload. Its isolated rerun passes 7/7 (`runtime-final-fixture-repair.log`). Final full/regression runs include the repair and the later identity logout regression/browser registration.

The 43 full-suite skips are opt-in browser/PostgreSQL checks; browser and live API evidence are owned by root and the integration agent. The six remaining failures are still failures, with no new failure signature in the stable run. This verification does not imply global release or production acceptance.

## Additional failures resolved

The initial 15 failures contained six historical failures and eight additional failing cases, plus the parent node of one nested failed test. The additional cases were not dismissed as baseline.

- `use-defense-variants-store.test.ts`: obsolete conflict text assertion; retained structured conflict identity and checked both available recovery choices.
- `identity-isolation.release.test.ts`, 401/403/404 and late overwrite: fixtures incorrectly requested an overwrite of a saved project; fixed to use a dirty, versioned enterprise project so requests reach the existing security boundary. Existing isolation/no-retry assertions retained.
- Owner recovery after logout and runtime recovery: replaced legacy automatic owner-key hydration expectations with enabled scoped storage, fresh authorized reads and explicit restoration. Verified another authorized collaborator cannot recover the owner's data, denied access cannot expose recovery, and discovery alone leaves the loaded project unchanged.
- `project-runtime.release.test.ts`, no automatic retry: independent failure fixtures now exercise every status; added explicit proof that ambiguous retry performs GET and sends no second PUT when verification fails.
- `use-defense-project-store.test.ts`: updated enterprise/policy fixture and scoped envelope expectations; hydration must not restore automatically, explicit restoration keeps dirty state.
- `project-roundtrip.release.test.ts`: strict complete-object equality exposed manufactured `provenance: null` and `fieldProvenance: undefined` for source records without those keys. Fixed the shared `preserveDemoAssetSources` helper to retain absent optional fields. The roundtrip assertion was unchanged. Existing demo provenance stamping remains covered. The related catalog assertion now requires an absent source field for an unrelated legacy card.

The revised owner-recovery test also caught recovery being offered after restored server access while the new store guard still saw stale `accessError`. Root fixed the successful fresh authorization transition; the test subsequently passed.

## Remaining historical failures

`baseline-signatures-stable.json` compares full exception/assertion/stack signatures against `../../frc02/pre-frc02-failure-signatures.txt`. Only the absolute frontend root is normalized. All six are identical:

1. `catalog-sidebar-motion-contract.test.mjs`: catalog sidebar fluid-width animation assertion.
2. `map-zoom-controls-contract.test.mjs`: clickable zoom controls assertion.
3. `prototype-3d-placeholder-contract.test.mjs`: scenario-modeling navigation assertion.
4. `retrospective-analysis-navigation-contract.test.mjs`: WIP navigation assertion.
5. `user-facing-copy-contract.test.ts`: `prototypeRu` copy assertion.
6. `defense-project.test.ts`: recommendation/compatibility catalog-label assertion.

Full-suite status remains FAIL; historical classification is not acceptance of these checks. Skipped tests require explicit browser or real PostgreSQL opt-in. This agent's evidence does not establish browser/runtime acceptance, report acceptance or production readiness.
