# FRC06 — минимальный план

2026-09-20. Исследование завершено; root принял FRC05 и разрешил реализацию FRC06. До GO исходники не изменялись. Существующие параллельные FRC04/05/09/11/12 изменения сохраняются. Без commits/push и отдельного dev server.

## Что переиспользуем

- Единственный `use-defense-project-store` на workspace/prototype/calculator. FRC05 `use-project-cost` уже разделяет целиком saved и draft.
- FRC01 `FortisApiError`/requestId, отказ от demo fallback, unverified recovery; FRC02 session generation, reset stores при смене аккаунта, 401 cleanup и resource403/404.
- Variants store уже сохраняет поздний бизнес-edit при успешном save и сохраняет draft при409; FRC04 backend обеспечивает expectedVersion, immutable GET revision и create Idempotency-Key.
- Каталог FRC09 preview/apply/cancel, provenance и document source callbacks не переписываем.

## Порядок и файлы

1. **Авторитетная GET identity.** `modules/drone-defense/domain/use-defense-variants-store.ts`: version/enterprise из результата GET, не cached list. Тест stale list v7 + GET v8; повторить FRC05 browser9. Поздний load/identity fences сохранить.
2. **Чистое состояние save.** Новые `shared/lib/project-save-state.ts` + test: стабильное бизнес-содержимое, saved ProjectRef/baseline, монотонный business-change counter и точный снимок попытки. Исключить только UI/transport: selected IDs, activeLayerId, mode, layer.isActive (selectLayer), updatedAt и серверные identity stamps из сравнения содержимого; все бизнес/unknown extension fields сохраняются. Theme/panels/filter уже вне project. Видимость и lock классифицировать явно тестами, не выдавать отдельный финансовый edit за выбор строки.
3. **Store integration.** `shared/lib/use-defense-project-store.ts`: бизнес-edit сначала обновляет память, затем best-effort local recovery; UI selection не меняет business counter. Saved baseline отдельно от current draft; успешный ответ повышает baseline/server version, но не затирает более новый draft. Повтор identical/no-op edit не создаёт ложную dirty revision. FRC05 `syncStatus` совместим, полный SaveStatus выводится из единого save-state.
4. **Локальный recovery.** Новые `shared/lib/project-draft-storage.ts` + test: `fortis:draft:<user>:<enterprise>:<project-or-localId>`, versioned envelope с baseline, draft и attempt metadata без токенов. Catch getter/getItem/setItem/parse/quota/security errors; typed result для честного предупреждения. Recovery выводить только после действующей identity и resource-access проверки; восстановление требует явного действия. Старый общий ключ не мигрировать автоматически. Старый user-only key тоже не делать авторитетным новым baseline. Политика shared-device должна отключать долговременное хранение; связать с безопасной server runtime настройкой, без client query override.
5. **Операции save.** `modules/drone-defense/domain/use-defense-variants-store.ts`, `infra/api-client.ts`: один in-flight attempt на scope identity+project, snapshot exact body/key/expectedVersion/changeCounter. Не генерировать JSON с новым updatedAt на retry. Один create attempt — один key и одинаковые bytes; новые данные — новая логическая попытка после разрешения предыдущей неоднозначности. Ответы проверять по ожидаемой identity и положительной версии. Ошибки сохраняют draft и requestId. 409 — явный conflict, без force overwrite.
6. **Неоднозначный update.** После network/5xx/timeout сначала read current GET, сохраняя draft. Сравнить resource identity + business payload с отправленным снимком; рост version сам по себе не доказывает сохранение нашего документа. Совпадение подтверждает baseline и оставляет последующий edit dirty. Тот же expectedVersion и несовпадающий draft разрешают только явный retry старой версии; новая несовпадающая revision — conflict. Ошибка verification блокирует повтор записи до проверки. Для create с неизвестным ID использовать авторизованный FRC04 replay неизменного key/body, а не list/name search или новый ключ. Истёкшая/непроверяемая попытка не получает ложный exactly-once статус.
7. **UI/переходы.** `variant-selector.tsx`, `variants-modal.tsx`, `defense-studio-shell.tsx`, owning workspace/prototype/logout entry points: явные SaveStatus, retry/requestId, конфликт с «Открыть серверную версию» после предупреждения и «Сохранить отдельным вариантом». Не закрывать модалку/очищать имя после неуспешной операции. Общий трёхвариантный guard «Сохранить / Остаться / Отказаться» на замену текущего проекта, смену предприятия и logout; обычный calculator↔map с тем же draft не блокируется. beforeunload только при dirty/незавершённом save; никаких обещаний обязательного browser диалога. Успешный save во время guard не выполняет переход, если появились новые edits.
8. **Report boundary.** FRC10 capability остаётся закрыта. Подготовить переиспользуемую проверку сохранённого ProjectRef/dirty intent без fake report или включения маршрута. Официальный report позже default-save либо явно last-saved; не current draft.

## Проверки

TDD на каждый выявленный defect. Pure save-state/storage, real store concurrency и real rendered controls; mock только transport/platform. SAVE01–10 сопоставляются в gap matrix. Перед сдачей focused suites, changed lint, tsc; FRC05 browser regression. Root координирует full build, реальный Next→Go→PG browser и итоговую приёмку.

## Границы решений

Не добавлять параллельный project store, server autosave, CRDT/merge, force overwrite, автоматическую миграцию чужих local keys или новый backend persistence. Изменения runtime public configuration, если необходимы shared-device policy, согласовать с root как явный контракт; сохранить workspace fail-closed. Report остаётся зависимостью FRC10, его HTTP200 не имитируется.
