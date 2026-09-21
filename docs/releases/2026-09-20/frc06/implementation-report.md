# FRC-06 — завершение acceptance, 2026-09-21

**Status: PASS — локальная staged acceptance FRC-06.** SAVE-09 отключён до обязательной приёмки FRC-10; production gates остаются FRC-14.

Исходный опубликованный frontend `045db0d` сохранён. Работа продолжает frozen-save pipeline без переписывания истории. Итоговый статус и свежие проверки фиксируются в [test-evidence](test-evidence.md) и [полной матрице](acceptance-criteria.md).

## Изменённое поведение

- Business revision различает выбор в UI и изменения конфигурации. Visibility/lock входят в business content; UI-only операции и no-op не перезаписывают ещё не восстановленный локальный черновик.
- CREATE retry использует замороженные body/idempotency key. UPDATE после неоднозначного ответа сначала читает сервер; одинаковый номер версии разрешает retry только при совпадении с сохранённым baseline. Другая identity, enterprise или content дают конфликт. Никакого автоматического повторного write.
- Receipt не может менять enterprise проекта. Поздний verification не возвращает уже покинутый проект. Подтверждённое сохранение остаётся успешным при отдельной ошибке обновления списка.
- Recovery выключен по умолчанию в workspace, scoped по user/enterprise/project, требует явного Restore после fresh access check. Повторная проверка выполняется и при нажатии Restore. Revoked context не гидратируется; backend unavailable не превращает локальные данные в saved state.
- Project/variant switch, enterprise switch и logout предлагают Save / Stay / Discard. До подтверждения Save переход не происходит. Discard возвращает baseline и удаляет recovery, а при выключенном storage работает в памяти. Ошибка storage не теряет изменения.
- Auth revalidation скрывает защищённое дерево вместе с popup portals, сохраняя состояние диалога только для той же identity. Другая identity сбрасывает stores и весь boundary state, включая имя/намерение в диалоге logout. Поздний logout response не сбрасывает следующую identity. beforeunload централизован на protected boundary.
- Save-as-new обновляет URL проекта; hard reload открывает новую сохранённую identity/version. Same-project map↔calculator navigation сохраняет dirty context, в том числе после отказа доступа.

Побочная подтверждённая регрессия FRC-04 исправлена в общем provenance helper: отсутствующие optional поля остаются отсутствующими при lossless roundtrip. Demo provenance по-прежнему сохраняется. Старые тесты автоматической hydration заменены явным scoped recovery с сохранением isolation assertions.

## Границы

Backend API/schema/migrations в FRC-06 не менялись. CRDT, autosave и force overwrite не добавлялись. SAVE-09 сейчас **NOT APPLICABLE** для отключённой official-report capability: существующий saved-ref helper проверяет identity/version, действующий UI не выдаёт официальный отчёт. Реальный dirty → Save/last-saved report flow остаётся обязательной приёмкой FRC-10 перед включением capability. Это не PASS отчёта и не внешний runtime blocker.

Полный frontend suite остаётся красным из-за шести исторических исключений с проверенными полными signatures. Их наличие явно сохранено в evidence. Production deployment, TLS, storage/retention и остальные FRC-14 evidence этой локальной приёмкой не подтверждаются.

## Независимая проверка

[Review](independent-review.md) проверяет immutable snapshot, idempotency, verification, identity isolation, revoked access, navigation и прежние FRC-01/02 гарантии. Все найденные дефекты воспроизведены; исправления подтверждаются постоянными regressions и независимыми probes. Реальный browser → Next → Go → PostgreSQL сценарий отделён от браузерных тестов с управляемым транспортом.
