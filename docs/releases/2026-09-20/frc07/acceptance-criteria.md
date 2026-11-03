# FRC07 acceptance criteria

The autonomous user contract and ADR-0023 override the old BUD-07 rejection of limit reduction and any embedded imported budget authority. All18 criteria PASS for this local stage. The coordinator's real UI integration additionally passed all seven checkpoints; see real-integration/result.json.

| Criterion | Result | Evidence |
|---|---|---|
| BUD-01 exact equality | PASS | AtomicBudgetGate PostgreSQL; independent rendered equality case; real UI/API checkpoint |
| BUD-02 one minor excess, no mutation | PASS | AtomicBudgetGate asserts persisted state; rendered shared gate; real direct PUT422 and unchanged full GET |
| BUD-03 shared mutation authority | PASS | Existing Commit covers all composition writes, copy/import, and full-candidate checks; owner and independent caller review; blocked preview and removal regressions |
| BUD-04 concurrent candidates | PASS | ConcurrentBudgetGate and RollbackAndBudgetRace: one CAS commit, one409; no double spend |
| BUD-05 unknown limited | PASS | UnknownZeroAndValidation:422 price_unknown, no durable mutation; rendered unknown guard |
| BUD-06 unknown unlimited | PASS | UnknownZeroAndValidation: null/incomplete, never zero; rendered unlimited case |
| BUD-07 revised overage | PASS | AtomicBudgetGate; rendered limit reduction and saved550→draft520→draft540; real limit500k→400k, flat/reduce accepted and increase rejected |
| BUD-08 common version and immutable budget | PASS | AtomicBudgetGate, pinned history; budget receipt exact identity/version and canonical snapshot checked by UI/parser |
| BUD-09 hidden/inactive costs retained | PASS | Exact cost regressions, AtomicBudgetGate; real visibility edit keeps50000000 minor |
| BUD-10 limited zero | PASS | UnknownZeroAndValidation; rendered literal0 request and one-minor rejection |
| BUD-11 malformed money distinct from unknown | PASS | Pure exact-money and UnknownZeroAndValidation, canonical strings and parser validation |
| BUD-12 check is not reservation | PASS | PG no cache/audit writes; final locked access/version check and budget-vs-composition race |
| BUD-13 rollback | PASS | Injected budget row, revision and audit failures roll back the shared transaction |
| BUD-14 copy authority/idempotency | PASS | CloneAuthorityAndReplay; ordinary UI Save as new passes explicit pinned source; later source budget leaves copy unchanged |
| BUD-15 late/error/protocol reads | PASS | Independent17 browser suite: pending,503/retry, wrong version, identity/project/version races |
| BUD-16 budget writes and dirty recovery | PASS | Focused save/recovery tests, independent pending/late/422/409 form cases; existing save pipeline retained |
| BUD-17 foreign/revoked access | PASS | CloneAuthorityAndReplay, FRC02 SQL regressions; no prices before authorization |
| BUD-18 local gate/unverified state | PASS | Independent shared guard tests; offline/unverified copy explicitly remains draft; read/historical restore bypasses editor gate |

Raw backend commands/results: [backend-verification](backend-verification.md). Independent findings and executed browser evidence: [independent-review](independent-review.md). Full-suite historical exceptions are explicitly retained, not converted to PASS.
