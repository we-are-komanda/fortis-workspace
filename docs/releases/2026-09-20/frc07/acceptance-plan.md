# FRC-07 independent acceptance plan

Status: planned; this checklist is not acceptance evidence. Prepared against accepted FRC-03 parent `7de854b`, frontend `e49253b`, backend `5a4a6d5`, followed by the FRC-07 working changes. The coordinator owns the real frontend → backend → disposable PostgreSQL gate and final acceptance. Independent verification owns separate rendered tests and review; production code belongs to its implementation owners.

## Authoritative contract

The [autonomous run contract](../../../../knowledge-base/01_Requirements/Release_2026_09_20_Autonomous_Run.md) overrides draft FRC-07 §4.6/BUD-07 and the older research proposal:

- Lowering a limit below current spend **succeeds**, creates a new revision and exposes the overage. Subsequent candidates compare against the current **saved** spend in both FE and BE: saved 550 / limit 500 → unsaved 520 → unsaved 540 remains allowed, including undo of an unsaved reduction; 560 is blocked. After saving 540 the new ceiling is 540. Cost-increasing saved candidates remain HTTP 422 `budget_exceeded` while over limit.
- A new project and an imported project start unlimited. A field inside project JSON never establishes budget authority. Copying a budget requires an explicit parameter naming an accessible, pinned server source; the copy is independent thereafter.
- Exact decimal minor-unit strings carry money. Limited zero is a real zero limit. Unknown spend stays null/incomplete and must not become zero.
- The shared project revision `Commit` transaction is final authority. A successful full-candidate check is read-only and does not reserve budget or waive the final authorization/version/budget checks.

The remaining draft scenarios in [FRC-07](../../../fortis-release-specs/specs/FRC-07_budget_gate.md) and shared release contracts apply. Old text rejecting limit reduction or permitting imported client budget authority is not used as an acceptance oracle.

## Behavioural gates

| ID | Probe | Required evidence |
|---|---|---|
| BUD-01 | Saved spend 47500000 minor, limit 50000000; candidate 50000000 | Full candidate preflight allowed; save succeeds; new pinned revision shows remaining 0. |
| BUD-02 | Candidate 50000001 | Preflight blocked; direct save HTTP 422 `budget_exceeded`; project JSON, version, budget, revision/audit and receipt counts unchanged. UI retains prior project and entered values. |
| BUD-03 | Change quantity, instance price, components/composition, duplicate and bulk candidate | Every persisted mutation enters the same final gate. New/import are unlimited; explicit clone uses only pinned source budget and enforces it. Raw embedded budget cannot bypass authority. |
| BUD-04 | Two candidates from N independently consume the same remaining amount | Exactly one reaches N+1; the stale writer receives 409. Re-reading and combining both edits fails 422; no lost update and no double spend. |
| BUD-05 | Limited and a valid unknown selected price | Preflight blocked and final save 422 `price_unknown`; no mutation. Error is associated with affected field/object and does not disclose foreign data. |
| BUD-06 | Unlimited and unknown selected price | Save allowed; spend/remaining null with an explicit incomplete warning. Known zero remains a complete zero. |
| BUD-07 revised | Lower 50000000 limit to 40000000 while spend is 47500000 | Limit save succeeds at N+1, remaining -7500000. Unchanged spend and reducing spend 45000000 succeed, including normal UI edits; edits/undo compare with the saved baseline, not the preceding draft. Increasing spend above that baseline while over the limit fails 422. A lower limit is not an implicit switch to unlimited. |
| BUD-08 | Change limit then read N and N+1 | One common revision per update, current full snapshot acknowledged. Old pinned projection retains prior config/digest; new revision has new config. Switching unlimited is explicit and audited. |
| BUD-09 | Toggle visibility or activity | Cost and remaining do not change; no exclusion of hidden/inactive objects from final gate. |
| BUD-10 | Limited zero | Empty and known-zero projects allowed; one minor blocked. UI sends exact zero rather than null/unlimited. |
| BUD-11 | Unknown versus malformed selected prices/quantity/currency | Unknown follows BUD-05/06; invalid input is rejected even under unlimited. Canonical exact strings survive large values and one-minor boundaries without float conversion. |
| BUD-12 | Check then mutate budget/project/membership before save | Check creates no writes/events/receipts/cache authority. Save rechecks current locked revision/access; stale or revoked operation fails without partial data. |
| BUD-13 | Inject failure after current/budget write but before revision/audit completes | PostgreSQL rollback leaves every durable entity and idempotency outcome consistent; retry is safe. |
| BUD-14 | Explicit copy from pinned source; mutate source later | Copied config reflects only specified accessible revision, remains independent; absent/foreign/revoked/missing revision fail safely. Changed source in an existing idempotency key conflicts; replay reauthorizes. |
| BUD-15 | Initial GET pending/503, malformed identity/version/config and late response from another project/version/identity | No fake zero, stale budget or wrong-context mutation; retry is explicit and response identity is validated before display. |
| BUD-16 | Budget PUT pending/failure/late acknowledgement with dirty project edits | Form values and existing unsaved project survive; no false saved state. Confirmed snapshot updates the saved baseline without silently overwriting newer business edits. |
| BUD-17 | Read/write/check as unrelated user or revoked member | Resource visibility semantics apply before money computation/details. No other user's amount, project state or budget appears in the response/UI. |
| BUD-18 | GIS add/edit while known over limit; unverified/offline candidate | Known prohibited candidate is not applied to active project. Offline/unverified state cannot masquerade as server acceptance. Error exposes projected expense/remaining and preserves independent edits. |

## Ownership and test seams

- Backend owner: pure gate, application/controller contracts and real PostgreSQL atomicity/concurrency/authorization tests; independent reviewer inspects final `Commit` call graph and all mutations.
- Frontend owner: exact types/parser/API, store transitions, shared candidate guard and budget UI. Focused pure/store tests remain with that owner.
- Independent verifier: new `frontend/src/modules/defense-calculator/ui/budget-gate.browser.test.ts`; real rendered components/stores, synthetic network only, controlled pending/late responses. Cover meaningful UI money boundaries, pending/error preservation, explicit unlimited/zero, no stale context, and candidate rejection. This harness does not prove PostgreSQL atomicity.
- Coordinator: actual authenticated ordinary UI → API → PostgreSQL flow, screenshots/console/network, clone/import and persisted revision evidence. No real customer data or production writes.

## Completion evidence

Record exact command, working snapshot/changed-file hashes, exit status and raw logs for each check. Distinguish observed RED→GREEN from tests added after implementation. Run final focused tests, rendered FRC-07 plus relevant prior release browser tests, backend full/PG tests, frontend full suite, TypeScript, changed-file ESLint and production build once source is stable. Compare every frontend failure against the six exact historical FRC-02 signatures; any additional failure is investigated rather than assigned to baseline.

At plan creation the independent agent's last escalated Chromium action was blocked because automatic approval review could not complete due to a usage limit. Default read/write work remains available. No execution is claimed for new FRC-07 browser tests until a fresh run has an observed result; the coordinator may execute them through its available approval path.
