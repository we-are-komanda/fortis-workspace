# FRC07 verification

**PASS — local staged FRC07.** [Actual integration](real-integration/result.json): seven checkpoints, v1→v11, independent copyv1, importv1, exact saved money/404 checks, consoleErrors=[]/pageErrors=[]. The acceptance includes this real UI→Next→Go→PostgreSQL evidence.

| Check | Observed result |
|---|---|
| Frontend focused budget/save/recovery | 61/61 PASS |
| Independent rendered budget | 17/17 PASS,0skip; cases15/16 observed RED→GREEN, case17 post-fix only |
| Rendered FRC03/05/06/07 regression | 56/56 PASS,0skip |
| Full frontend, frozen dependencies | 314 total:232PASS,6FAIL,76opt-inSKIP; exit1 |
| Exact historical failure comparison | All six complete signatures match both FRC03 and original FRC02; only absolute frontend path normalized |
| TypeScript and changed21-file ESLint | PASS in frozen source copy |
| Production build | PASS, exit0, Next16.2.11 in isolated copy |
| Source consistency | 420 files matched working and isolated copy before tests/build; later real-harness timeout-only adjustment tracked separately |
| Backend full Go tests/build | PASS |
| Real PostgreSQL FRC02/03/04/05/07 | 26 top-level and20 subcases PASS,0selectedskip |
| Independent backend packages | Nine tested packages PASS, one without tests |

Frontend full suite is intentionally reported as non-green. No new failure was classified as baseline. Preliminary unprivileged full run failed on sandbox loopback EPERM; the final authorized run above executed those tests and supersedes it.

The frozen isolated directory had an actual offline `pnpm install --frozen-lockfile --ignore-scripts` before source copy and verification. This proves manifest/lock/install consistency, rather than relying on the old working node_modules mismatch. Toolchain logs are in ../frc13/toolchain/.

Reproduction from the matching frontend source/dependencies:

```sh
rtk proxy env FRC06_BROWSER_TESTS=true FRC03_BROWSER_TESTS=true FRC05_BROWSER_TESTS=true FRC07_BROWSER_TESTS=true node --import tsx --test --test-concurrency=1 src/modules/drone-defense/ui/project-recovery.browser.test.ts src/modules/workspace/ui/project-workspace.browser.test.ts src/modules/defense-calculator/ui/calculator-page.browser.test.ts src/modules/defense-calculator/ui/budget-gate.browser.test.ts
rtk proxy pnpm build
```

The exact89-file full-suite command, type/lint commands, source hashes, six standalone baseline probes and raw logs are in [verification-logs](verification-logs/). Backend reproduction is in [backend-verification](backend-verification.md).
