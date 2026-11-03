# FRC-08 independent verification evidence

Final checks use the source after the scoped access-denial fix. Pre-access-fix full/type/lint/build and 73-test browser results are preserved separately under `round1/`.

| Evidence | Result and scope |
|---|---|
| `browser-initial-17-red.log` | 16 pass, one historical-side repinning failure; DOM shows erroneous A9/A9. |
| `browser-fixed-17-green.log` | 17 pass, no skips, after matching pre-save version in the repin predicate. |
| `browser-access-denial-red.log` | Both known-denial cases fail; unrelated denied active C control passes. |
| `browser-final-20-green.log` | All 20 pass, no skips, after matching denial clears visible/pending comparisons. |
| `browser-regressions.log` | Final combined 76 pass, zero failures/skips. Coordinator executed; full output independently inspected. |
| `frontend-full.log`, `frontend-full.command.json` | Final 92-file full suite: 341 tests, 239 pass, six historical failures, 96 opt-in skips, exit 1. |
| `baseline-signatures.json`, `baseline-1.log` through `baseline-6.log` | Independently rerun: all six exact signatures match prior FRC-07 and original FRC-02. No new failure. |
| `frontend-frozen-types.*` | Final TypeScript exit 0. |
| `frontend-frozen-changed-lint.*` | Final ESLint exit 0 across all 14 changed source/test files. |
| `production-build.log` | Coordinator production build exit 0; completed build output inspected. |
| `build-source-hashes.json`, `source-manifest-verification.json` | All 426 files match both the working tree and frozen build copy after final checks. |
| `independent-backend-packages.*` | Four budget packages pass, one has no tests. |
| `backend-manifest-verification.json` | All 14 backend owner manifest hashes match reviewed source. |

Rendered command from frontend:

```sh
rtk proxy env FRC08_BROWSER_TESTS=true node --import tsx --test src/modules/defense-calculator/ui/configuration-comparison.browser.test.ts
```

The access RED used the same command with `--test-name-pattern='known denial|confirms denial|unrelated active'`. Synthetic HTTP responses are deliberately held and reordered; the tests render actual comparison/store code. Backend authorization and immutable PostgreSQL data are checked separately in [backend-verification.md](../backend-verification.md), with ordinary-UI full-stack evidence supplied by the coordinator.

The final toolchain directory is `/private/var/folders/79/mmyd13f10px_4f6vb__s9b_w0000gn/T/frc06-build-final-0oobx55m`, using the coordinator-verified frozen install and exact Next/eslint-config-next 16.2.11 lock. Command JSON files record cwd, arguments, actual child exit status and explicit lint file list. Signature checks execute each failing test separately and normalize only the absolute frontend root before exact comparison with the prior FRC-07 JSON and original FRC-02 signature text.
