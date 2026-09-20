# FRC06 — checkpoint перед остановкой

Дата: 2026-09-20. **FRC06 не завершён и не принят.** Пользователь попросил завершить ближайшую задачу и остановиться; root завершает только FRC09. Реализация FRC06 остановлена без отката. Коммиты, push, deployment не выполнялись. После инструкции остановки выполнены только read-only tsc/lint и запись этого checkpoint; production-код дополнительно не менялся.

## Точная область изменений этого агента

Все пути относительно workspace `/Users/rr/Documents/Fortis`:

- `docs/releases/2026-09-20/frc06/implementation-plan.md` — план, записанный до реализации.
- `docs/releases/2026-09-20/frc06/gap-matrix.md` — SAVE01–10 и восемь воспроизведённых исходных пробелов.
- `frontend/src/shared/lib/project-save-state.ts` — новый pure helper: SaveStatus, SaveAttempt, businessContent, savedProjectRef, classifySaveVerification.
- `frontend/src/shared/lib/project-save-state.test.ts` — 4 passing pure tests.
- `frontend/src/shared/lib/project-draft-storage.ts` — новый scoped storage helper: DraftScope/ProjectDraft, ключ user+enterprise+project, read/write/list/remove; ошибки storage/JSON возвращаются как typed result.
- `frontend/src/shared/lib/project-draft-storage.test.ts` — 3 passing pure tests.
- `frontend/src/shared/lib/use-defense-project-store.ts` — добавлены businessRevision, savedProject, saveAttempt, draftStorageError, localDraftSaved, localDraftsEnabled/setLocalDraftsEnabled, acceptServerProject, recordSavedProject, restoreVerifiedDraft. Business apply обновляет память до best-effort persistence; UI selection не увеличивает businessRevision. Persist использует новый scoped envelope и policy flag. `restoreProjectFromLocalStorage` теперь только отмечает hydration: автоматическая загрузка старых данных отключена, явный recovery UI **ещё не подключён**. Старый идентификатор projectStorageKey оставлен как legacy helper, новые writes его не используют. FRC09 preview/source изменения других агентов сохранены.
- `frontend/src/shared/lib/identity.ts` — единственная добавка: при reset stores сохраняется server delivery policy `localDraftsEnabled`, а не пользовательские данные.
- `frontend/src/modules/drone-defense/infra/api-client.ts` — добавлены prepareProjectSave (замороженный body/key/снимок) и sendProjectSaveAttempt; усилена проверка положительной целой версии summary. **Основной variants store ещё не вызывает эти helpers.** Существующие старые saveVariantAsNew/overwriteVariant сохранены.
- `frontend/src/modules/drone-defense/domain/use-defense-variants-store.ts` — пока только исправление authoritative GET: enterpriseId/version берутся из GET project, не cached list summary. Остальной save pipeline остаётся прежним.
- `frontend/src/modules/drone-defense/domain/project-save.release.test.ts` — новый permanent TDD suite, сейчас 7 тестов: **4 PASS / 3 ожидаемых RED**, перечислены ниже.

Никакая планировавшаяся перепись variants store не запускалась; прерванная перед остановкой работа находилась только в стадии рассуждения. Незавершённых tool sessions нет.

## Отдельные параллельные изменения root

Root уже реализовал server runtime policy: `FORTIS_LOCAL_DRAFTS_ENABLED`, additive `localDraftsEnabled` в `/api/runtime`, RuntimeProvider применяет setter и повторяет применение после смены session generation. Workspace default false, demo own namespace true по умолчанию; строгая boolean env validation. Эти файлы принадлежат root, не этому агенту. Root также менял `shared/lib/defense-project.ts` для FRC05 финансовых отображений; данный агент этот файл в FRC06 не редактировал.

## Что закончено и проверено

1. Cached list v7 больше не подменяет version/enterprise из GET v8. Permanent regression был RED `7 !== 8`, стал GREEN. FRC05 браузерная регрессия после этого исправления: **9/9 PASS**.
2. Pure comparison исключает UI/transport selection/mode/stamps, сохраняет бизнес-поля и unknown extensions; verification требует identity + совпадение отправленного содержимого, а не только более высокую version. **4/4 PASS**.
3. Scoped storage не читает legacy/other-user ключи, ловит getter/security/quota/corrupt JSON, default disabled не обращается к хранилищу. **3/3 PASS**.
4. Project memory edit переживает quota и показывает draftStorageError; business revision не меняется при selectAsset, изменяется при бизнес-edit, возврат к baseline даёт saved. Эти store tests PASS.

## Известные ожидаемые RED

Команда из `frontend/`:

`rtk proxy node --import tsx --test src/modules/drone-defense/domain/project-save.release.test.ts`

Последний результат: **4 PASS / 3 FAIL**.

- `pending save preserves UI selection as saved`: variants store всё ещё использует `latest !== project`, поэтому UI selection во время PUT даёт dirty вместо saved.
- `lost update response verifies current server identity before any second write`: после504 отсутствует GET verification.
- `create manual retry preserves exact body and idempotency key`: старый store вызывает старый API helper повторно; key и сериализованный updatedAt меняются.

Это TDD ожидания незавершённого FRC06, **не исторические baseline failures и не разрешение их игнорировать**. Не включать FRC06 capability/acceptance на основании чистого tsc.

## Последние проверки

Все команды запускались из `frontend/`:

| Команда | Результат |
|---|---|
| `rtk proxy node --import tsx --test src/shared/lib/project-save-state.test.ts src/shared/lib/project-draft-storage.test.ts` | 7/7 PASS |
| `rtk proxy node --import tsx --test src/modules/drone-defense/domain/project-save.release.test.ts src/shared/lib/project-save-state.test.ts src/shared/lib/project-draft-storage.test.ts` до добавления четырёх save lifecycle tests | 10/10 PASS |
| `rtk proxy node --import tsx --test src/modules/drone-defense/domain/project-save.release.test.ts` после добавления lifecycle tests | 4/7 PASS; 3 RED выше |
| `rtk proxy env FRC05_BROWSER_TESTS=true node --import tsx --test src/modules/defense-calculator/ui/calculator-page.browser.test.ts` после authoritative GET fix | 9/9 PASS; synthetic intercepted transport, Chromium |
| `rtk proxy pnpm exec tsc --noEmit` **после инструкции STOP** | exit 0 |
| `rtk proxy pnpm exec eslint src/shared/lib/project-save-state.ts src/shared/lib/project-save-state.test.ts src/shared/lib/project-draft-storage.ts src/shared/lib/project-draft-storage.test.ts src/shared/lib/use-defense-project-store.ts src/shared/lib/identity.ts src/modules/drone-defense/domain/use-defense-variants-store.ts src/modules/drone-defense/domain/project-save.release.test.ts src/modules/drone-defense/infra/api-client.ts` **после STOP** | exit 0 |

До реализации исходные identity/variants regressions: 11/11 node-reported tests PASS (включая один старый script с 7 inline scenarios). После смены recovery semantics эта старая группа **не перепроверена целиком**. Старый тест автоматического owner recovery потребуется заменить проверкой явного восстановления после fresh access, а не ослабить identity isolation.

## Необходимые следующие шаги — только после нового разрешения продолжить

1. Подключить frozen SaveAttempt helpers к variants store: single in-flight, captured identity/project/changeCounter; acknowledgement через recordSavedProject, GET load через acceptServerProject. Сохранить поздние edits, положительную server identity, scope/generation guards; сделать три RED зелёными.
2. Verification-first для ambiguous update: current GET, identity + business-content match; не считать N+1 достаточным доказательством. При ошибке GET никаких новых writes. Create replay — неизменные key/body; не создавать дубликат по новому key после потерянного ответа. Error/requestId/conflict должны оставаться доступны UI.
3. Завершить явное recovery: сначала действующая session и свежая авторизация server project либо enterprise для несохранённого local draft, затем предложение пользователю. Пока **новый storage пишет при включённой policy, но UI восстановления отсутствует**. Не показывать данные только из наличия ключа. Проверить сохранённые attempt metadata/body на соответствие scope перед replay; сейчас storage валидирует основную структуру, но это ещё не законченная trust boundary для replay.
4. Добавить guards save/stay/discard для смены проекта/предприятия/logout и beforeunload; обычный calculator↔map с тем же draft сохраняет контекст. Не переходить после save, если во время него появился новый edit.
5. Обновить variant selector/modal/workspace/shell: все SaveStatus, retry/requestId, 409 reload с явной потерей-confirmation, save-as-new; не закрывать modal/очищать имя при failure. Текущий UI и старые load/logout handlers пока не изменены.
6. Проверить clear/reset/new-project transitions на новые baseline/storage flags; завершить бизнес-vs-UI классификацию видимости/lock тестами. Отдельного autosave не добавлять.
7. FRC10 report остаётся gated. Подключить только reusable saved-ref/dirty intent, без fake report; actual report gate выполняется в FRC10.
8. Тесты SAVE01–10: pure/store concurrency + real rendered/browser controls; повторить FRC01/02, FRC05 и FRC09 preview regressions, changed lint/tsc. Root координирует полный build и реальный Next→Go→PG. Обновить evidence/матрицу/KB только после проверки.

Статус на остановке: изменения сохранены в рабочем дереве, код парсится и typechecks; FRC06 поведение частично интегрировано, три новых regression tests намеренно красные, production acceptance отсутствует.
