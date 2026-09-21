# FRC-06 — поэлементная приёмка сохранения и восстановления

Дата проверки: 2026-09-21. Область: текущий FRC-06 candidate поверх frontend `045db0d`, итоговый commit `a56d128e715ed09387428ad3dd67434d18855dd5` и независимый review. Основание: [спецификация FRC-06](../../../fortis-release-specs/specs/FRC-06_save_recovery.md), [общие контракты, §§5 и 9](../../../fortis-release-specs/00_SHARED_CONTRACTS.md), 30 дополнительных критериев из пользовательского задания от 2026-09-21.

**Все 30 дополнительных критериев: PASS.** Это поэлементная приёмка локального save/recovery-контура, не окончательная приёмка всего релиза. SAVE-09 ниже имеет **NOT APPLICABLE** только для текущего runtime с закрытой capability официального отчёта; его полная приёмка обязательна в FRC-10. Наличие `savedProjectRef` само по себе не означает готовность отчёта.

Финальная verification завершена: focused48/48, browser13/13, regressions38 PASS/1 explicit PG skip, full250=201 PASS/6 historical FAIL/43 opt-in SKIP. Types/lint/build PASS; 454 source hashes test/build совпали без workspace drift. Семь findings закрыты, восемь independent probes PASS. Root grants **PASS для локального FRC-06 stage**; это не зелёная полная suite и не production/report acceptance. См. [verification logs](verification-logs/README.md) и [independent review](independent-review.md).

## Доказательства и границы

Тесты выполняют production store/API/UI. В unit/store-тестах транспорт и localStorage синтетические. Browser harness использует настоящий Chromium и production-компоненты с перехваченным HTTP; он не доказывает PostgreSQL. Отдельный live run использует Next → Go → disposable PostgreSQL и реальные сохранённые версии. Production runtime этим этапом не принят.

| Код | Источник |
|---|---|
| F1 | [project-save.release.test.ts](../../../../frontend/src/modules/drone-defense/domain/project-save.release.test.ts): save concurrency, verification, recovery, access, discard и late-response regressions. |
| F2 | [project-save-state.test.ts](../../../../frontend/src/shared/lib/project-save-state.test.ts): business content, server identity/version, baseline verification и saved ref. |
| F3 | [project-draft-storage.test.ts](../../../../frontend/src/shared/lib/project-draft-storage.test.ts): scoped storage, corrupt/quota/security, frozen replay после reload. |
| F4 | [project-runtime.release.test.ts](../../../../frontend/src/shared/lib/project-runtime.release.test.ts): workspace без fallback/автореставрации, отсутствие автоматических retry и failed verification без второй записи. |
| F5 | [identity-isolation.release.test.ts](../../../../frontend/src/shared/lib/identity-isolation.release.test.ts): 11/11 PASS, включая `late logout completion cannot clear the next authenticated identity`; смена аккаунта, logout, stale async responses и explicit owner recovery. |
| F6 | [local-draft-policy.release.test.ts](../../../../frontend/src/shared/server/local-draft-policy.release.test.ts): server policy для persistent drafts. |
| B | [project-recovery.browser.test.ts](../../../../frontend/src/modules/drone-defense/ui/project-recovery.browser.test.ts): [13/13 PASS log](verification-logs/browser-navigation-13.log); перечень B1–B13 ниже. |
| F | F1 + F2 + F3: [48/48 PASS log](verification-logs/focused-root-48.log). |
| L | Live run: [6/6 checkpoints PASS](browser-live/result.json), [окружение и ограничения](browser-live/README.md); перечень L1–L6 ниже. Проверены значения проекта, версия и восстановление после reload, а не только HTTP 200. |
| A | [FRC-02 access tests](../../../../backend/cmd/app/frc02_access_test.go), [FRC-02 PostgreSQL tests](../../../../backend/cmd/app/frc02_postgres_test.go), [FRC-04 revision/idempotency tests](../../../../backend/cmd/app/frc04_postgres_test.go). Повторные backend проверки и Go build приведены в общем test evidence. |

Browser log обновлён до 13 passing cases после седьмого security finding. Исходные результаты `/private/tmp/frc06-final-focused.log` и `/private/tmp/frc06-live/final/result.json` сохранены в durable evidence по ссылкам выше. В live console присутствуют deck font/GPU warnings, antd deprecation и ожидаемый 409 отрицательного сценария; этот файл не заявляет полностью пустую консоль.

Browser checkpoints:

| ID | Точное имя passing browser-теста |
|---|---|
| B1 | `variant Stay preserves edit; Discard opens target and deletes discarded recovery` |
| B2 | `conflict reload asks before replacing the active project` |
| B3 | `enterprise switch while dirty offers Stay and Discard` |
| B4 | `logout while dirty offers Stay and Discard before ending session` |
| B5 | `failed or pending Save cannot navigate; explicit retry confirms before opening target` |
| B6 | `failed create retains the name and explicit retry replays the frozen body/key` |
| B7 | `recovery rechecks access when Restore is clicked, after the offer was displayed` |
| B8 | `revoked dirty project still requires an explicit decision before another variant loads` |
| B9 | `reload keeps saved state until explicit scoped recovery` |
| B10 | `session recheck hides all protected dialogs and preserves same-user transition state` |
| B11 | `logout Save stays on failed save, then leaves only after confirmed retry` |
| B12 | `enterprise Save keeps selection after failure and switches after confirmed retry` |
| B13 | `switching identity clears the previous user logout intent and name` |

Live checkpoints:

| ID | Фактически проверено |
|---|---|
| L1 | Synthetic server project создан в disposable контуре, version 1. |
| L2 | Реальное изменение видимости через UI сохранено; тот же projectId/version 2 и `visible=false` после reload. |
| L3 | Map → calculator → map сохраняет unsaved visibility, projectId и последнюю server version 2. |
| L4 | После reload recovery только явное; восстановление само не пишет на сервер; отдельный Save даёт version 3. |
| L5 | Конкурирующая server version 4 приводит к 409, draft остаётся; Save as new создаёт другой projectId/version 1, исходная версия остаётся 4. |
| L6 | Новый server projectId/version 1 сохраняются после reload; selector показывает сохранённый вариант. |

## Все 30 пользовательских критериев

| № | Критерий | Статус | Конкретное доказательство |
|---|---|---|---|
| 1 | UI-only selection во время PUT не делает проект dirty | PASS | F1 `pending save preserves UI selection as saved`; F2 `selection and transport changes are not business changes`. |
| 2 | Business change во время save остаётся dirty | PASS | F1 `pending save preserves business edit as dirty`; отдельные passing tests для layer visibility и lock во время PUT. |
| 3 | Successful save без новых business changes → saved | PASS | F1 UI-selection save и `lost update response verifies current server identity before any second write`; L2/L6. |
| 4 | Frozen request не меняется при retry | PASS | F1 `unchanged server revision permits only an explicit retry of the frozen update after another verification`; create retry с более новым draft; B6. |
| 5 | Repeated CREATE отправляет identical body | PASS | F1 `create manual retry preserves exact body and idempotency key` и retry после нового edit; B6 сравнивает фактические POST bodies. |
| 6 | Repeated CREATE использует identical idempotency key | PASS | Те же F1/B6 проверки; F3 `reload preserves the exact frozen create body and key alongside a newer draft`. |
| 7 | Ambiguous UPDATE сначала выполняет GET verification | PASS | F1 потерянный ответ и controlled retry проверяют последовательность PUT → GET → явный retry → GET → PUT. F4 запрещает PUT после failed verification. |
| 8 | Committed-state verification принимает authoritative ID/version | PASS | F1 потерянный ответ принимает version 8; `authoritative GET version cannot be replaced by an older cached list summary`; неправильная identity отвергается, L2/L6 сохраняют ID после reload. |
| 9 | Unchanged server state допускает controlled retry | PASS | F1 explicit frozen UPDATE retry; F2 `unchanged version permits retry only when the server still matches the saved baseline`. |
| 10 | Divergent verification → conflict | PASS | Три F1 cases для отличающихся content/project/enterprise; F2 отдельно проверяет same-version content, lower/invalid version. Повторной записи нет. |
| 11 | 409 не выполняет silent overwrite | PASS | F1 `409 preserves the local draft and a new variant never writes the conflicted project`; B2 требует подтверждение reload; L5 подтверждает исходную server version и отдельный новый ID. |
| 12 | 401/403/404 не запускают automatic retry | PASS | F1 три отдельных dirty-save tests: только один PUT, без GET/retry; 401 очищает identity, 403/404 блокируют overwrite и copy. F5/F4 — регрессии. |
| 13 | 5xx/timeout не запускают uncontrolled save loop | PASS | F1 frozen retry и ambiguous verification; F4 no-auto-retry/failed-verification; B5 показывает явную повторную кнопку после ошибки. |
| 14 | Workspace default не auto-restores persistent draft | PASS | F1 `workspace startup and authorized recovery discovery leave the server project active until explicit restore`; B9/L4. F6 отдельно проверяет default policy. |
| 15 | Recovery выполняется только explicit user action | PASS | Discovery в F1 не меняет project; B9/L4 восстанавливают только после Restore и не делают server write. |
| 16 | Draft scoped по authenticated identity | PASS | F3 namespace/envelope validation; F1 `the next identity cannot discover or apply the previous identity recovery candidate`; F5 account switch; B13 дополнительно проверяет очистку локального logout intent/name при смене пользователя. |
| 17 | Draft scoped по enterprise/project | PASS | F3 delimiter-character scope isolation; F1 stale recovery не заменяет другой current project/enterprise. |
| 18 | Доступ проверяется перед restore | PASS | F1 fresh authorized GET; B7 повторно проверяет доступ при клике Restore после первоначального предложения; workspace restore делает fresh `getEnterprise` в [workspace UI](../../../../frontend/src/modules/workspace/ui/project-workspace-page.tsx). |
| 19 | Revoked/inaccessible draft не становится active project | PASS | F1 fresh 403/404 и позднее revoked access; B7/B8; [restore guard](../../../../frontend/src/shared/lib/use-defense-project-store.ts) не очищает denial из stale candidate. |
| 20 | Backend-unavailable draft не называется authoritative server state | PASS | F1 fresh 503 оставляет server-loaded active project и скрывает draft candidate; F4 запрещает fallback; восстановленный draft имеет dirty, а не saved. L4 требует отдельный Save. |
| 21 | Dirty project/variant switch → Save / Stay / Discard | PASS | B1/B5; [VariantsModal](../../../../frontend/src/modules/drone-defense/ui/variants-modal.tsx) и workspace open guard. |
| 22 | Dirty enterprise switch → Save / Stay / Discard | PASS | B3 и B12: Stay/Discard, failed Save сохраняет выбор, подтверждённый retry разрешает switch. |
| 23 | Dirty logout → Save / Stay / Discard | PASS | B4/B11: до решения logout POST отсутствует; после failed Save остаются session/draft. B13 сбрасывает intent/name предыдущего пользователя; F5 не позволяет позднему logout response очистить следующую identity. |
| 24 | Save не разрешает navigation до confirmed resolution | PASS | B5 удерживает PUT до ответа; B11/B12 разрешают переход только после успешного retry; F1 list-refresh regression отличает подтверждённый save от вторичной list error. |
| 25 | Failed/ambiguous save не выполняет navigation автоматически | PASS | B5/B11/B12; после 503 выполняется verification, текущее место и draft сохраняются до явного решения. |
| 26 | Discard удаляет unsaved changes/recovery | PASS | B1/B3/B4 проверяют удаление scoped keys и переход; F1 `memory-only discard works when persistent drafts are disabled and storage is forbidden`; F3 scope-safe removal. |
| 27 | UI-only state не вызывает лишний dirty guard | PASS | F1 businessRevision/selection tests и `UI selection after server load cannot overwrite an undiscovered recovery draft`; F2 классификация. Guards читают dirty/pending-attempt/in-flight/unverified enterprise в [workspace](../../../../frontend/src/modules/workspace/ui/project-workspace-page.tsx), [modal](../../../../frontend/src/modules/drone-defense/ui/variants-modal.tsx), [identity boundary](../../../../frontend/src/shared/ui/identity-boundary.tsx); selection не добавляет ни одного из этих условий. Это store test + проверка guard, отдельный theme-switch browser case не заявляется. |
| 28 | Reload допускает только scoped recovery flow | PASS | B9/L4; F3 frozen attempt roundtrip; F1 startup/discovery не гидратируют draft. |
| 29 | Другой пользователь не получает draft первого | PASS | F1 cross-identity discovery/restore, F3 scopes, F5 logout→другая identity и late response; B10 скрывает protected UI при повторной auth-проверке. B13 воспроизводит прежнюю утечку имени из открытого logout dialog A после смены на B и подтверждает исправление: весь SessionIdentityBoundary keyed по generation, его локальные intent/name/error сбрасываются вместе с subtree. |
| 30 | Project identity/version корректны после save/reload | PASS | L2 и L6; F1 authoritative GET против stale list; late ambiguous verification не заменяет identity другого current project; malformed acknowledgement не меняет enterprise. |

## SAVE-01…SAVE-10 спецификации

| ID | Статус | Доказательство и предел |
|---|---|---|
| SAVE-01 | PASS | L3: реальная навигация map → calculator → map сохраняет одну unsaved конфигурацию, projectId и server version. Общий Zustand store читают оба маршрута; отдельная конфигурация не создаётся. |
| SAVE-02 | PASS | F1 оба pending-save cases; edit 2 остаётся, baseline получает server version, dirty сохраняется. Visibility/lock проверены отдельно как business fields. |
| SAVE-03 | PASS | F1 lost-response GET принимает committed state без второго PUT; unchanged/divergent verification и frozen CREATE retry. Backend idempotency — A. |
| SAVE-04 | PASS | F1 409 сохраняет draft; B2 подтверждает выбор перед server reload; L5 воспроизводит conflict на реальном server project. |
| SAVE-05 | PASS | F1 409→copy отправляет POST, не второй PUT исходного проекта; B6 frozen retry; L5/L6 дают независимый новый ID/version 1 и сохранённый исходный version 4. |
| SAVE-06 | PASS | F3 corrupt JSON/cross-scope/security/quota возвращают typed error без исключения; F1 quota сохраняет edit в памяти и показывает draftStorageError. Server load отделён от локального storage; F1 startup/recovery tests и live reload. |
| SAVE-07 | PASS | F2 selection/mode/transport excluded, F1 pending selection saved и бизнес-counter; тема/panels не входят в DefenseProject. Visibility/lock, напротив, сохраняются и увеличивают business revision. |
| SAVE-08 | PASS | F1/F3/F5: identity scope, никакой автоматической migration общего ключа, явное восстановление только владельцу после fresh access. B13 проверяет также logout dialog/name; F5 проверяет, что поздний logout A не очищает identity B. |
| SAVE-09 | NOT APPLICABLE | Для текущего FRC-06 runtime official-report capability закрыта (`report: not_released` в [product-capabilities](../../../../frontend/src/shared/config/product-capabilities.ts)); active [CalculatorPage](../../../../frontend/src/modules/defense-calculator/ui/calculator-page.tsx) показывает только целиком saved projection или маркированный draft. `CalculatorReport` не имеет callers в текущем UI. F2 проверяет `savedProjectRef` только для положительной integral backend version; [release-surface tests](../../../../frontend/src/shared/ui/release-surface.test.tsx) проверяют закрытые capability/routes. **Сам workflow «dirty → официальный отчёт → Save/last-saved» здесь не реализован и не принят.** Его обязательная активация и полноценная приёмка остаются FRC-10 согласно исходному [gap matrix](gap-matrix.md) и dependency chain. Это не внешний runtime blocker и не report PASS. |
| SAVE-10 | PASS | F1/F5 и B7/B8: revoked access блокирует recovery и новые writes, 401 очищает identity. Backend membership проверяется для каждого read/write/export: A, включая `TestFRC02RevocationSameJWT` и PostgreSQL revocation cases. Это membership policy ADR-0017, не отложенный полный RBAC/viewCost. |

## Остальные обязательные пункты спецификации

| Требование | Статус | Доказательство |
|---|---|---|
| §3: sent revision + business-change counter сохранены для in-flight attempt | PASS | [prepareProjectSave](../../../../frontend/src/modules/drone-defense/infra/api-client.ts) создаёт отдельный сериализованный snapshot/body/key; F1/F3 проверяют replay и новый edit; F2 отделяет business content от UI. |
| §4.1: один current context для workspace/map/calculator | PASS | Общий [project store](../../../../frontend/src/shared/lib/use-defense-project-store.ts); L3 и SAVE-01. |
| §4.2: сохранено/dirty/saving/local draft/conflict/error различимы | PASS | [VariantSelector](../../../../frontend/src/modules/drone-defense/ui/variant-selector.tsx) выводит явные статусы; B2/B5/B6 и L6 проверяют соответствующие пользовательские состояния. LocalStorage success не вызывает `recordSavedProject`; F1 quota/restore cases сохраняют dirty. |
| §4.3: explicit server save, local preview, без autosave/merge | PASS | F4 no-auto-retry, F1 recovery discovery, B9/L4; CalculatorPage маркирует draft. Сервер меняется только по явному Save/Save as new. |
| §4.5: error/retry/requestId после timeout/5xx | PASS | F1 unchanged verification сохраняет `lost-update` requestId; B5 показывает `fixture-request` и сохраняет проект до явного retry. |
| §4.6: конфликт разрешается reload с подтверждением или отдельным вариантом | PASS | B2 и L5; SAVE-04/05. Нет автоматического объединения. |
| §4.7: legacy storage не мигрирует автоматически; quota/security не теряют память | PASS | F3 legacy/other-user keys и malformed replay; F1 quota, UI selection не перезаписывает ещё не восстановленный draft. |
| §4.8: browser beforeunload для dirty state | PASS | [IdentityBoundary](../../../../frontend/src/shared/ui/identity-boundary.tsx) содержит единый handler для protected routes. B9 явно обрабатывает browser beforeunload при reload. Нельзя гарантировать, что любой браузер всегда покажет диалог. |
| §4.9: повторная auth-проверка и смена identity не показывают старые данные | PASS | B10 скрывает protected subtree и contextual dialogs во время revalidation и сохраняет state при том же пользователе. B13 проверяет generation-keyed remount всего SessionIdentityBoundary, включая local logout state. F5 сбрасывает stores/отвергает stale responses и позднее завершение logout предыдущей identity. |
| §4.10: официальный отчёт для dirty | NOT APPLICABLE | Точная staged граница и обязательство FRC-10 приведены в SAVE-09; отсутствие report acceptance не скрывается. |
| Shared-device: persistent drafts отключаются server policy | PASS | F6; F1 memory-only discard не требует запрещённый localStorage. JWT/credentials в ProjectDraft не добавляются. |
| Новый проект после явного выхода из denied старого контекста | PASS | [workspace createProject](../../../../frontend/src/modules/workspace/ui/project-workspace-page.tsx) очищает denial/active variant только при explicit new context; [independent review](independent-review.md) фиксирует реальный initializer probe с POST в authorized enterprise F. Это не permission bypass для редактирования старого проекта. |
| Late verification / malformed acknowledgement не меняют чужой current scope | PASS | F1 late ambiguous verification и malformed enterprise acknowledgement; независимый review. |
| Ошибка обновления списка после confirmed save не блокирует выход | PASS | F1 `a confirmed save permits leaving even when the subsequent project list refresh fails`: version 8, saved, no pending attempt, no повторный PUT. |
| Полная финальная verification + release bookkeeping | PASS | Финальные результаты и совпадающие source manifests зафиксированы в test-evidence/verification-logs; review без открытых findings. Frontend commit `a56d128e715ed09387428ad3dd67434d18855dd5`. |

Предыдущие FRC-01/02/04/05 guarantees сохраняются; их регрессии и полная suite учитываются отдельно. Не вводятся CRDT, autosave replay, общий неподтверждённый draft, новая доменная модель, роли или production deployment. Операционная готовность и актуальный deployed artifact требуют самостоятельной FRC-14 runtime acceptance.
