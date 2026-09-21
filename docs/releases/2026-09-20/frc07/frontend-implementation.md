# FRC-07 frontend implementation

Status on 2026-09-21: frontend implementation and focused verification complete; coordinator-owned real UI → API → PostgreSQL acceptance remains **pending**. This document does not accept FRC-07 or the whole release. Base frontend commit: `e49253b` (accepted FRC-03); these changes are uncommitted at this checkpoint.

The [active release agreement](../../../../knowledge-base/01_Requirements/Release_2026_09_20_Autonomous_Run.md) and [current acceptance plan](acceptance-plan.md) supply the budget rules. They supersede the old BUD-07 proposal that rejected lowering a limit below spend. The implemented [backend API](backend-api.md) is the explicit boundary.

## Visible behavior

One [ProjectBudgetPanel](../../../../frontend/src/modules/defense-calculator/ui/project-budget-panel.tsx) appears in the calculator and inside the GIS “Бюджет и расходы” section. It shows the pinned saved version's budget, the whole current draft's expense/remaining amount, incomplete prices, and existing overage. GIS also previews the selected placement candidate. Before an authorized matching projection arrives, the panel says the budget is unverified and the changes are a local draft.

The controls are “Режим бюджета”, “Лимит бюджета, ₽”, “Сохранить бюджет”, explicit “Снять ограничение бюджета”, and “Проверить текущий проект”. Recovery exposes “Повторить сохранение бюджета”; failed reads expose “Обновить бюджет”. A check explicitly says it neither saves nor reserves money. Limited zero is accepted as zero; unlimited uses null and is displayed as unlimited. Decimal input and money calculations use strings and `BigInt`, reusing FRC-05 cost calculation/formatting rather than converting through floating-point rubles.

Lowering the limit below saved spend succeeds through the server update and exposes the negative remainder. Existing overage allows a known candidate only when it does not exceed the authoritative saved total: saved 550 / limit 500 permits unsaved 520 → 540, but rejects 560. Once 540 is saved it becomes the new ceiling. Unknown totals under a limited budget fail the full-candidate guard; unlimited unknown totals remain incomplete instead of becoming zero.

## Shared candidate and persistence boundaries

[budget-projection.ts](../../../../frontend/src/shared/lib/budget-projection.ts) uses `buildDraftCostProjection` for the entire candidate. It validates pinned response identity/version, canonical string money, digest metadata and consistent budget status/remainder. The [budget hook](../../../../frontend/src/modules/defense-calculator/domain/use-project-budget.ts) fetches a positive saved project reference and suppresses late project, version, enterprise and session responses. Preflight sends the entire local project plus its pinned version, and only displays a result for unchanged business content. Pending preflight state belongs to that context, so P's unfinished check cannot disable Q's check or clear Q's pending state on completion.

The existing [shared project store](../../../../frontend/src/shared/lib/use-defense-project-store.ts) gates `applyProject` before mutation whenever an authoritative budget and saved project match the candidate's ID, version and enterprise. A rejection leaves the project unchanged and exposes its projected expense/remainder or missing-price error. Historical server acceptance and explicit authorized recovery read paths bypass this local edit guard, so historical exceeded/unknown snapshots remain readable. When the budget is unavailable, local changes do not become evidence of server acceptance; the persisted write still reaches the server's final gate.

The caller audit propagated the new boolean result through placement, movement/transfer, object editing, layer create/edit/delete, catalogue preview/removal and the legacy budget-selection success flag. The object editor closes only after a successful application. Catalogue previews remain pending when rejected; removal returns a budget failure instead of reporting a change that never happened. Visibility/activity is still part of the full project cost; it cannot remove placed objects from expense.

## Save, recovery and copy

Budget writes extend the accepted FRC-06 `SaveAttempt` with `kind: "budget"`; there is no second persistence model. [updateBudget](../../../../frontend/src/modules/drone-defense/domain/use-defense-variants-store.ts) freezes the version and exact requested configuration, uses the common busy state, and rejects replacement by a create attempt until the budget attempt is resolved or explicitly discarded. PUT uses the saved snapshot as its base. [The API boundary](../../../../frontend/src/modules/drone-defense/infra/api-client.ts) requires the expected new version, project/enterprise identity, unchanged canonical business content and the requested budget configuration before accepting its full snapshot.

A valid acknowledgement advances the saved baseline while retaining business edits made during the request; those edits remain dirty. HTTP 422 preserves the current project and user input without an automatic retry. An ambiguous response retains the frozen attempt. Explicit retry first reads the current server project and pinned budget: a matching committed result is accepted without a second write, an unchanged revision allows the explicit frozen retry, and divergent content/configuration produces a conflict. Session or project changes prevent late results from restoring previous context.

[Draft storage](../../../../frontend/src/shared/lib/project-draft-storage.ts) validates the budget body against its scoped project and exact version. Restoring any non-create attempt marks verification required even if the browser stopped before receiving its first response. The form synchronizes with a restored frozen request after it is already mounted; when a retry later fails and pending state clears, the requested values stay editable rather than reverting to the old saved limit.

“Save as New” includes a top-level `budgetSource: {projectId, projectVersion}` only from an explicit saved server reference. The source, request body and idempotency key remain frozen on retry. Workspace new projects omit that source even when another saved project is active. The server creates new/imported projects as unlimited and authorizes/copies an explicit source independently; embedded project JSON is not budget authority. Frontend tests prove request shape and retry behavior, while actual import/copy authorization and durable independence belong to backend and real integration evidence.

## Scope and verification

The owned implementation consists of 17 frontend files listed in [frontend-changed-files.md](frontend-changed-files.md). No dependency was added. The independent 17-case browser suite, coordinator's pre-FRC-13 deck layer ID repair, Next.js pin and integration harnesses are separately owned.

[frontend-evidence.md](frontend-evidence.md) records focused **61/61**, TypeScript and changed-file lint checks, the inspected independent browser **17/17** result, and coordinator-reported/inspected rendered regression **56/56** and isolated Next.js 16.2.11 build. Full-suite baseline adjudication and the real FRC-07 gate remain separate checkpoints. SAVE-09 official-report acceptance remains mandatory under FRC-10; this budget work does not accept reporting or the whole release.


Coordinator final addendum: real07 gate subsequently PASS (seven checkpoints,0 console/page errors); all six full-suite failures exactly match FRC02/FRC03 historical signatures. Root grants local07 PASS. See real-integration/result.json and test-evidence.md.
