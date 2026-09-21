# FRC-07 independent verification evidence

| Check | Result | Evidence |
|---|---|---|
| Frozen frontend full suite | 314 tests:232 pass,6 exact historical failures,76 skips;89 files | `frontend-full.log`, `frontend-full.command.json` |
| Full failure signatures | 6/6 exact matches to prior FRC-03 and original FRC-02 | `baseline-signatures.json`, `baseline-1.log` through `baseline-6.log` |
| TypeScript | Exit0 | `frontend-frozen-types.*` |
| ESLint all changed source/test files | Exit0,21 files | `frontend-frozen-changed-lint.*` |
| Rendered budget acceptance | 17 pass,0 fail,0 skips | `browser-final-17-green.log` |
| Preflight-context regression | Observed RED→GREEN | `browser-context-15-red.log`, `browser-current-16-green.log` |
| Recovery displayed amount regression | Observed RED→GREEN; follow-up conflict branch post-fix only | `browser-recovery-16-red.log`, `browser-final-17-green.log` |
| Relevant FRC-03/05/06/07 browser regression | 56 pass,0 fail,0 skips | `browser-regressions-56-green.log` |
| Production build | Coordinator-observed exit0, raw log inspected | `production-build.log` |
| Backend budget/project package checks | Exit0,9 tested packages,1 no-test package | `independent-backend-packages.*` |
| Frozen tested sources | 420 files; independently matched working/copy before later harness-only adjustment | `build-source-hashes.json` |
| Later live harness adjustment | Separate lint result and SHA256 | `live-harness-final-lint.*` |

The final frontend commands run in `/private/var/folders/79/mmyd13f10px_4f6vb__s9b_w0000gn/T/frc06-build-final-0oobx55m` with the coordinator-verified frozen dependencies and exact Next/eslint-config-next16.2.11 lock. Each command JSON records cwd, exit status and explicit file list when applicable. Production build and actual full-stack gate are executed by the coordinator separately.

Re-run the rendered suite from frontend with `rtk proxy env FRC07_BROWSER_TESTS=true node --import tsx --test src/modules/defense-calculator/ui/budget-gate.browser.test.ts`. Synthetic HTTP responses make these UI/store checks deterministic; they do not replace PostgreSQL atomicity checks. The initial14 and intermediate16 logs preserve the observed progression. No test assertions were weakened to obtain GREEN.

`frontend-working-preliminary.*` is diagnostic only: default sandbox blocked test HTTP listeners with `EPERM`. It is superseded by the final frozen escalated full run. Ordinary full-suite skips are opt-in browser/integration cases, not silently passed acceptance requirements. Six historical failures remain failures and are described precisely rather than calling the full suite green.

Backend full/PG/build commands and evidence are linked in `../backend-verification.md` and `../backend-verification-logs/`. The independent backend output is transcribed from the tool result with whitespace normalized; its command metadata explicitly states that scope.

`source-manifest-verification.json` records the independent comparison after final checks. The frozen copy remains an exact420-file match; any working-tree drift listed is the coordinator-owned live harness timeout adjustment. Production files remain equal.
