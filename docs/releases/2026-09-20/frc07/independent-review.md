# FRC-07 independent review

Review completed for the tested frontend snapshot and final backend budget paths. **No remaining concrete findings.** This is independent review/verification evidence; the coordinator owns the real frontend → API → PostgreSQL acceptance gate and release decision.

The reviewer did not implement the production budget/save/recovery paths. Scope covered exact money and unknown prices, all persisted mutation entry points, the shared revision `Commit`, pinned budget reads, new/import/copy authority, complete candidate checks, local edit rejection, pending requests, recovery and identity changes. The approved persisted-baseline overage policy was used: saved550/limit500 → draft520 → draft540 is permitted; after saving540, that is the new ceiling.

| Finding | Observed defect | Closure |
|---|---|---|
| 1. Catalogue preview reported success after rejection | Saved template100/limit100, refresh101: actual store returned true and cleared preview while the shared budget gate retained old price100. | Independent Node probe first reproduced it. The same probe now verifies false plus retained project/preview, then successful explicit retry after unlimited applies101 and clears preview. Permanent owner regression added. |
| 2. Previous project preflight disabled the new project | Hold P check, open Q and load Q budget: Q check remained disabled by a component-wide pending flag. | Independent rendered testcase15 observed RED, then GREEN after pending state was scoped to context. Old completion cannot clear another context's pending state. |
| 3. Recovery displayed the wrong requested budget | Render saved500000.00, explicitly restore uncertain request600000.01: disabled input still displayed500000.00 while Retry would send600000.01. Initializer-only handling missed recovery after mount. | Testcase16 observed RED→GREEN. Testcase17 additionally verifies retention after verification followed by a concurrent PUT409; that branch was fixed before its first run, so it has post-fix GREEN evidence only. Final17 all pass. |

Raw RED/GREEN logs and commands are in [verification-logs](verification-logs/README.md). Browser executions used the coordinator's available approval path; the independent reviewer authored tests and inspected every result. There is no claim that case17 was observed RED.

## Final evidence

- Independent rendered budget suite: **17 passed, 0 failed, 0 skipped**. It covers exact equality/+1 minor, persisted overage undo, pending/pinned GET, lower-limit success, limited0, unlimited/unknown, GET failure/retry, form preservation, newer business edits during PUT, full-candidate read-only check, late project/version/identity responses, malformed pinned identity and recovery branches.
- Frozen frontend full suite: **314 tests, 232 passed, 6 failed, 76 skipped**, 89 files. All six complete failure signatures exactly match both the prior FRC-03 evidence and original FRC-02 historical text after replacing only the absolute frontend directory. No additional failures.
- Relevant release browser regressions: **56 passed, 0 failed, 0 skipped** (FRC-03/05/06/07); coordinator execution and raw log independently inspected. Production build completed with coordinator-observed **exit0**; raw completed build log copied.
- Frozen TypeScript and changed-file ESLint: **exit0**, ESLint covers21 changed source/test files. The420-file source manifest matched both working frontend and isolated copy before the later live-harness-only timeout adjustment; that harness has separate lint/hash evidence.
- Independent backend budget/project package tests: **exit0**, nine tested packages and one package without tests. Final source review found the final gate and writes under the shared row/member locks; pinned source copy has source/member protection; new/import remain unlimited; preflight writes nothing; legacy budget update cannot bypass required version. PostgreSQL/concurrency/rollback and full-backend evidence are maintained in the backend verification document.

Source review of the coordinator's narrow FRC-13 prerequisite confirms deck layer IDs now use `zone.layerId` consistently with selection and preview lookups, preventing repeated display codes from producing duplicate deck identities. The coordinator owns its actual browser RED→GREEN evidence.

The preliminary working-tree full run hit sandbox `listen EPERM` and is retained only as diagnostic evidence. It is superseded by the escalated frozen-copy full run. The earlier automatic approval-review usage failure was an execution limitation, not a product failure; it was not bypassed.

Future algorithm changes must interpret authoritative previous spend using its saved calculation binding, or fail closed before granting the overage exemption. The current release has only the existing v1 binding and no public path creates unsupported bindings; pinned unsupported reads already fail closed. This is a future rollout constraint, not an observed current-release defect.
