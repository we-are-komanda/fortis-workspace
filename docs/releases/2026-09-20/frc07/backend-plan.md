# FRC-07 backend implementation plan and recovery checkpoint

## Active execution agreement — 2026-09-21

FRC03 and real vertical gate accepted at parent7de854b, frontend e49253b, backend5a4a6d5, KB4cd6ff1. FRC07 implementation is now authorized. User continuation supersedes the historical STOP and undecided proposals below. Read ADR-0023 before using this plan: new/importunlimited; explicit accessible pinned budgetSource only for create/clone; reducedlimit overage allowed followed by non-increasing/reducing writes; reasonCode non_increasing_overage. No migration expected, no new dependency. Existing Commit remains one atomic authority.

Ownership: backend implementation/tests — integration_research; frontend production/focusedtests — frc06_acceptance_tests; independent plans/renderedtests/review — frc06_verification; root — ADR, shared agreement, actual integration and acceptance. Root handles approved Chromium/PG runs if an agent approval call is unavailable by account limit. Child commits only after accepted stage, then parent pointers; no push/deploy.

Execution checklist:
- [ ] RED→GREEN pure budget rules: exact equality/onekopeck/zero, unknown, loweredlimit nonincrease.
- [ ] Shared Commit authority and explicit clone source digest/access; atomic rollback/concurrentCAS PG evidence.
- [ ] Pinned budget read, readonly candidatecheck and canonical budgetPUT with currentversion receipt.
- [ ] Existing FE save pipeline supports budget update/retry/recovery, reusable UI and honest projected/full costs.
- [ ] Independent browser/API tests, real Next→Go→PG budget scenario, full regressions/types/lint/build.
- [ ] Final review, criteria/docs/KB, childcommits thenparent.

The remainder records the original research state, including superseded alternatives; it is not current authority.

> Research only, 2026-09-20. Implementation NOT STARTED. Parent authorized investigation only pending FRC-06 acceptance; the user subsequently instructed the team to finish its nearest task and STOP. No FRC-07 code, tests, migration or runtime changes were made. Resume only on new authorization.
>
> For agentic workers: use the approved native implementation/review workflow and TDD after GO. No commits, pushes or deployment are authorized by this plan.

**Goal:** Every accepted project or budget mutation obeys its exact RUB limit within the same transaction as current state, revision and audit.

**Architecture:** Reuse FRC-04 `ProjectRevisionRepository.Commit`, its project-row lock, membership lock, CAS, immutable snapshot and audit. Reuse FRC-05 raw-document cost calculation and exact integer arithmetic. Budget rules belong in the existing budget domain; the transaction delegates to the same pure rule used by read-only preflight.

**Stack:** Existing Go/PostgreSQL/GORM; no additional dependency or parallel financial model.

**Sources read:** `docs/fortis-release-specs/specs/FRC-07_budget_gate.md`, shared contracts §5–8/12, `contracts/release-contracts.ts`, KB index/roadmap and ADR-0018/0020. FRC-04/05 code is accepted locally; that does not accept FRC-07 or production runtime.

## Observed current flow

| Evidence | Current behavior | FRC-07 consequence |
| --- | --- | --- |
| `backend/cmd/app/router.go:56` | GET/PUT `/projects/budget`, POST `/projects/budget/check`; no backend PATCH route | Extend existing routes, retain explicit `id` compatibility alias where appropriate |
| `budget/ui/controller.go:100` and `budget/application/budget_service.go:43` | PUT accepts `budgetAmountMln` float and calls repository Save directly | Bypasses expected version, cost validation, project revision and budget audit |
| `budget/domain/budget_config.go:25` | Limited amount must be strictly positive; remaining uses float and clamps negative values | Limited zero unsupported; exact overage and historical negative remaining unavailable |
| `budget/application/budget_service.go:75` | Check evaluates only one asset/quantity; unlimited returns synthetic zero | Does not validate full candidate, overrides, components or unknown prices |
| `defense_project/application/project_revisions.go:82` | Existing UpdateBudget accepts expected version and JSON budget, then calls saveProject | Reuse this hook; it deliberately does not yet enforce monetary rules |
| `defense_project/infrastructure/project_revision_repository.go:52` | Existing write locks current project FOR UPDATE, locks membership FOR SHARE, compares expected version | Correct serialization boundary already exists |
| Same file `:76–127` | Serializes/writes candidate, optionally upserts budget, rereads JSONB, inserts immutable snapshot | Add authoritative budget read and candidate validation before first write; keep all writes in this transaction |
| Same file `:137` | Budget operation records budget.update with prior/new project versions | Reuse audit; old/new mode remains recoverable from the two immutable snapshots |
| `budget/document/cost.go:49` | Pure Calculate validates selected money/quantity/currency/mode and uses exact FRC-05 arithmetic | Reuse for save validation and full-candidate preflight; do not duplicate arithmetic |
| `budget/application/project_cost.go:14` | Version-pinned cost reads authorize current project, then use frozen calculator/cache | Reuse for historical GET BudgetProjection; preflight must use pure calculation because cache materialization would be a write |
| `defense_project/application/defense_project_service.go:208,293,323,417,492` | Create/import/typed create/metadata update/content update all converge on saveProject/Commit | Put enforcement at shared Commit boundary, including internal Save path; no per-button gate |
| `defense_project/application/project_revisions.go:24` | Create/import idempotency digest currently includes name, enterprise, project document only | Any added budget input/source reference must join the request digest |
| `budget/infrastructure/models.go:23` and migration `000008_budget_configs` | Current budget is JSONB with legacy float serialization; old revisions preserve its raw snapshot | Exact string fields fit existing storage; avoid a schema migration unless implementation proves it necessary |

File references above are relative to `backend/internal/modules/` unless an explicit workspace path is shown. They describe the state inspected during planning, not a verified FRC-07 implementation.

## Proposed public interface — not yet frozen

Use the shared `BudgetConfig`, `BudgetProjection`, `BudgetCheckRequest/Response` types without renaming monetary fields:

```ts
type BudgetConfig =
  | { budgetMode: "unlimited"; budgetLimitMinor: null }
  | { budgetMode: "limited"; budgetLimitMinor: string };

// GET /api/v1/projects/budget?projectId=P&projectVersion=V
type BudgetProjection = {
  identity: CalculationIdentity;
  config: BudgetConfig;
  spentMinor: string | null;
  remainingMinor: string | null;
  status: "within_limit" | "exceeded" | "unlimited" | "indeterminate";
};

// PUT /api/v1/projects/budget?projectId=P
type BudgetUpdateRequest = BudgetConfig & { version: number };

// POST /api/v1/projects/budget/check?projectId=P
type BudgetCheckRequest = { version: number; projectJson: string };
type BudgetCheckResponse = {
  basedOn: { projectId: string; projectVersion: number };
  status: "allowed" | "blocked";
  reasonCode: "within_budget" | "unlimited" | "budget_exceeded" | "price_unknown";
  projectedSpentMinor: string | null;
  projectedRemainingMinor: string | null;
};
```

GET reads budget from the requested immutable revision, never the current budget table for an older version. Explicit nonexistent version stays 404 revision_not_found. Compatibility omission may resolve current once, as FRC-05 does; release consumers supply the version. `projectId` is preferred, `id` an explicit alias, conflicting aliases are rejected.

PUT requires positive expected version. Proposed response: existing FRC-04 project summary/snapshot fields plus `budget: BudgetProjection`, all describing the committed new version. This lets FE advance its saved baseline from the actual acknowledgement. The FRC-06 owner reported `recordSavedProject(sentProject, serverProject)` as its planned acknowledgement helper; budget integration should feed that helper and preserve any newer local draft, rather than replace it with an older returned project.

Preflight is read-only and does not reserve remaining budget. Authorize current resource, compare expected version and use that immutable revision's budget with the submitted full candidate. Return 200 allowed/blocked for a valid preflight; return 400 for malformed inputs, 409 for stale version. Final save reruns the same rule while holding the write lock. Actual prohibited writes return 422 budget_exceeded or price_unknown with requestId and authorized field/object details. Errors do not expose foreign prices or mutate project/budget/revision/audit/cache.

Malformed selected price, quantity, currency or pricing mode must return the same structured 400 codes on save/import as on FRC-05 calculation, including unlimited mode. Unknown price is a valid incomplete calculation; limited blocks it with 422, unlimited allows it with explicit incomplete projection/warnings. Unlimited + incomplete has status indeterminate, not a fabricated zero.

## Outstanding contract decision — root owns resolution

Create/import currently accept raw project JSON without an authoritative BudgetConfig, and FRC-04 raw export intentionally has no snapshot envelope. Supplied projectId/version are not authority. A new variant's initial budget therefore cannot safely be inferred from those fields.

Proposed minimal addition is explicit `budget: BudgetConfig` on create/import, persisted and checked in the initial transaction. The release duplicate/save-as-variant flow should carry the source snapshot budget. Omitted budget for a genuinely new legacy-compatible project could default to explicit unlimited, but **this is not accepted yet**. If duplication must enforce inheritance independently of client-supplied config, an explicit authenticated source reference `{projectId,projectVersion}` must be introduced and checked by the server. Existing in-project object duplication already follows ordinary project PUT and will be gated there.

The root agent is reading authority and will decide new-project defaults, import/variant inheritance and whether a source reference is required. Do not silently implement unlimited fallback for duplication, trust imported ownership/version, or invent an endpoint while this remains unresolved. Include whichever explicit inputs are approved in idempotency payload comparison.

Also do not copy the 10^15 **unit-price** cap onto the total budget: no budget-limit cap is specified. Proposed budget representation is an exact nonnegative integer string with limited zero accepted. If a separate input digit bound is needed, document it as an explicit contract choice rather than silently rejecting a valid aggregate limit.

## Minimal implementation approach after GO

- [ ] Add exact budget configuration/projection/rule in existing budget domain. Keep legacy million fields only as an adapter for remaining consumers; remove float arithmetic from authoritative budget decisions. Domain comparison is total ≤ limit, using big.Int; historical remaining may be negative.
- [ ] Add a pure raw-budget adapter next to `budget/document/cost.go`. Parse canonical string/null fields first; only absent canonical fields may fall back to legacy JSON decimal `budgetAmountMln`. Never decode legacy money to float before conversion. A missing old budget can be treated as unconfigured/unlimited only after the root's contract decision; malformed limited data must not silently become zero/unlimited.
- [ ] Reuse Calculate plus the domain rule for a single candidate evaluator. Its inputs are serialized candidate project and the effective authoritative budget; output includes cost, normalized BudgetConfig and allowed/blocked result. No cache or DB writes occur inside this evaluator.
- [ ] In Commit, after current project/membership locks and CAS, serialize the candidate and read its current budget while the project lock is held. Use explicit authorized budget input only for budget mutation/create/import as agreed. Delegate validation to the pure evaluator before writing. Persist canonical budget JSON, current project, new revision and audit atomically. Do not leave an unvalidated trusted/internal Save bypass.
- [ ] Route HTTP budget PUT through DefenseProjectService.UpdateBudget and the same Commit. Retire direct browser-accessible budgetRepo.Save. There must be no alternative write path that changes the budget without the project lock/version increment. No new lock manager or reservation table is necessary.
- [ ] Implement pinned GET BudgetProjection and full-candidate preflight in BudgetService. Keep each read tied to one revision. Budget change uses current project content; an unsaved FE draft remains a separate pending candidate unless an explicit combined-save contract is agreed.
- [ ] Normalize canonical budget on new successful writes; retain all historical snapshot JSON/digests. Existing JSONB is sufficient, so no schema migration is presently planned. Old exceeded snapshots remain readable as exceeded/legacy-invalid and cannot produce a new accepted invalid state. Do not rewrite history to manufacture compliance.
- [ ] Map gate errors in all project create/import/update controllers and budget controller. Update only owning DTO annotations; generate OpenAPI normally. Preserve authorization precedence, version errors, replay behavior and FRC-04 requestId/audit.

Suggested owning files: budget domain config/projection tests; budget document budget adapter/tests; budget application service/projection methods; budget UI dto/mapper/controller/tests; defense_project Commit and create/import input plumbing; `cmd/app/frc07_postgres_test.go` using the existing isolated-schema helper (or the spec's `tests/integration/budget_revision_gate_test.go` if that helper is reused cleanly). Root coordinates shared DI/router and FE integration; no new dependency is expected.

## Acceptance gap matrix and RED cases to add after GO

| Case | Current evidence/gap | Required permanent check |
| --- | --- | --- |
| BUD-01 | Exact cost exists, gate absent | A=47500000; limit=50000000; full candidate=50000000 succeeds, remaining=0 |
| BUD-02 | Current PUT ignores cost | Candidate=50000001 rejects422; current raw project, version, budget, revision count and audit count identical before/after |
| BUD-03 | All saves converge, none enforce | Same overage via raw PUT, import/create with approved limited config, object duplicate, quantity/override/component/bulk change rejects |
| BUD-04 | Project CAS already serializes writes | Two independent committed connections start from N with separate 2000000 additions; one N+1 succeeds, other409; recombined fresh candidate then422; no double spend |
| BUD-05 | Cost knows unknown; budget single-item checker loses it | Limited unknown rejects422 price_unknown and exposes only authorized object IDs |
| BUD-06 | Unlimited checker currently returns synthetic zero | Unlimited unknown saves preliminary; cost/budget spent null and status indeterminate |
| BUD-07 | Direct budget Save accepts lowering | Limit40000000 at spend47500000 rejects with no state/event/revision mutation |
| BUD-08 | FRC-04 budget hook exists but HTTP bypasses it | Limit50000000→60000000 creates N+1; N still returns50000000 and unchanged digest; audit links old/new versions |
| BUD-09 | FRC-05 cost includes hidden/inactive/maintenance | Toggle visibility/status; spent and remaining unchanged |
| BUD-10 | Old constructor rejects limited zero | Empty/zero-cost limited0 succeeds; one-minor paid candidate rejects; unlimited remains explicitly null |
| Save price validation | Invalid money currently fails only on cost read | All shared save paths reject selected negative/fractional/over-cap price, invalid quantity/currency/mode before any write; overrides still ignore unused price branches as FRC-05 specifies |
| Transaction failures | Revision/audit rollback already covered in04 | Inject budget write, revision and audit failures; project/budget/revision/idempotency/cache remain consistent |
| Budget vs project race | Separate budget writes currently evade lock | Race limit reduction and project increase from N; one commit wins, stale second gets409; re-evaluation cannot exceed accepted limit |
| Preflight semantics | Existing check has wrong input | Full candidate checked; no writes/caches/events/reservations; later conflicting save is still rejected |
| Historical data | Immutable snapshots already available | Old exceeded/unknown/legacy budgets readable honestly; no fake backfill or mutated digest; malformed config requires explicit repair |
| Access/replay | FRC02/04 existing tests green | Foreign/revoked project404 before money details, no audit on denied operation, replay reauthorizes and altered budget payload conflicts |

Tests use only root's existing isolated local PostgreSQL16 cluster (`127.0.0.1:55434`, fortis_test/postgres) with unique synthetic schemas. Use existing `FORTIS_FRC04_TEST_DSN` fixture contract unless the executor defines an FRC07 alias. Concurrent checks must use actual committed connections, not an in-memory repository. No new FRC-07 tests were written or run during this planning checkpoint.

Expected verification after implementation: focused domain/document tests; actual PostgreSQL BUD matrix including CAS/audit rollback; FRC02/04/05 regressions; go vet/build; generated scoped OpenAPI validation; independent review and frontend real-backend acceptance. Exact commands/counts belong in backend-evidence.md after execution, not as guessed results here.

## Resume handoff

1. Confirm new user authorization and root FRC-06 acceptance/GO; preserve all current uncommitted work.
2. Read the root's resolution of initial/duplicated/imported budget semantics and response acknowledgement shape.
3. Recheck the touched files for concurrent FRC06/09 changes; update this plan's interface agreement before writing code.
4. Implement the bounded steps with RED→GREEN and independent review. Root owns final acceptance/ADR/status artifacts.

This file is the final FRC-07 research checkpoint for the stop request. It does not authorize implementation or imply budget enforcement is delivered.
