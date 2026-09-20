# Fortis: отчёт для агента-архитектора

Дата: 20 сентября 2026 года. Workspace: `/Users/rr/Documents/Fortis`.

## 1. Текущее положение

Выполнена значительная часть локального release-hardening, но **релиз целиком не готов, первый пользовательский сценарий не завершён**. Пользователь может войти в локальный `/workspace`, однако без назначения предприятия не может создать конфигурацию.

Полный автономный run остановлен по просьбе пользователя после завершения кодовой приёмки FRC-09. Последующие отдельные обращения разрешали устранение локальных проблем входа и пустого workspace, а не возобновление всего release package. Текущий запрос — подготовить этот отчёт.

Все изменения остаются в рабочих деревьях. Коммитов, push, deploy и production migrations в этом run не было. Принятые локально изменения пересекаются в общих файлах с незавершённой FRC-06; весь checkout нельзя считать release candidate.

`CODE PASS / RUNTIME BLOCKED` ниже означает зафиксированную локальную кодовую приёмку соответствующего среза. Это не независимое утверждение архитектора, не полная приёмка исходной спецификации вне уточнённого scope и не доказательство production-ready состояния.

## 2. Статус спецификаций

| Спецификация | Фактический статус | Что сделано / что осталось |
| --- | --- | --- |
| FRC-00 | Реализация базового комплекта; runtime acceptance не закрыта | Зафиксирован baseline. Не доказана идентичность deployed artifacts, toolchain и migrations. |
| FRC-01 | Кодовая приёмка в принятом scope; runtime blocked | Один backend resolver, прозрачный proxy, явные workspace/demo, readiness/liveness, отсутствие молчаливого demo fallback. |
| FRC-02 | CODE PASS / RUNTIME BLOCKED в scope ADR-0017 | Membership-проверки ресурсов, scoped lists, identity isolation, защищённые страницы. Полный RBAC и другие deferred требования не реализованы. |
| FRC-03 | Исследована; отдельные UI-дефекты исправлены; **не принята** | Нет штатного операторского подключения пользователя к предприятию и проверенного первого проекта. После остановки добавлены empty-state guidance и повторная загрузка предприятий. |
| FRC-04 | CODE PASS / RUNTIME BLOCKED | Lossless snapshots, неизменяемые ревизии, optimistic locking, идемпотентность, атомарный audit. |
| FRC-05 | CODE PASS / RUNTIME BLOCKED | Единый точный расчёт стоимости, version-pinned server projection, отдельный draft projection, единые потребители карты/калькулятора. |
| FRC-06 | **Частичная реализация; не принята** | Базовые save-state/storage primitives есть, основной lifecycle и recovery UI не завершены; три regression-теста остаются RED. |
| FRC-07 | Исследование и backend plan; не реализована | Атомарный бюджетный контроль предстоит реализовать. |
| FRC-08 | Не начата | Сравнение фиксированных версий. Существующий legacy compare не означает выполнения FRC-08. |
| FRC-09 | CODE PASS / RUNTIME BLOCKED | Provenance, сохранение типизированных карточек, явный catalog refresh, приватные документы и quarantine/scanner pipeline. |
| FRC-10 | Не начата | Официальный отчёт из одной версии, включая server-side hideCost. |
| FRC-11 | CODE PASS / RUNTIME BLOCKED | Уточнены обещания и навигация, demo маркирован, ряд неготовых экранов закрыт capability notices. |
| FRC-12 | CODE PASS / RUNTIME BLOCKED | Durable demo request, receipts/idempotency, outbox/retry, SMTP transport constraints, локальный registry. Реальная доставка не подтверждена. |
| FRC-13 | Не начата | Итоговый CI и интегрированная сквозная приёмка. |
| FRC-14 | Не начата | Эксплуатация, восстановление, runtime gates и решение о выпуске. |

История: [autonomous-run.md](autonomous-run.md), [acceptance-matrix.md](acceptance-matrix.md). Эти документы содержат промежуточные записи и старые сведения о процессах. Для изменений после остановки см. разделы 5–6 этого отчёта и последнюю запись knowledge-base; старый статус «FRC-03 research only» уже не отражает небольшую последующую UI-правку.

## 3. Реализованные архитектурные изменения

### Runtime и доступ

- ADR-0016: `BACKEND_URL` — единый server-side источник backend; aliases только проверяются на совпадение. Public remote fallback отсутствует. Local HTTP разрешён явным development-флагом, production transport остаётся отдельной проверкой.
- ADR-0017: `user_enterprises` — граница доступа. Project/budget/cost/report/compare/private assets/documents проверяют сохранённую принадлежность enterprise. Недоступный и отсутствующий ресурс имеют одинаковый 404.
- Public catalog mutation, enterprise create/delete и membership administration закрыты ordinary JWT. Operator role/admin HTTP API не добавлялись. UI не должен обходить это ограничение автоматическим присвоением первого предприятия.
- Browser state изолирован по identity/generation; старые ответы не должны попадать в новую сессию. Local recovery не является подтверждением серверного доступа.

### Ревизии и стоимость

- ADR-0018: атомарная запись проекта, неизменяемого snapshot и минимального project audit; version conflict; create idempotency с ограниченным сроком; snapshot digest и сохранение неизвестных полей.
- ADR-0020: точные minor units на BigInt/big.Int. Ноль отличается от неизвестной цены; неизвестность сохраняется как null вместе с known subtotal. Скрытые/неактивные размещения учитываются; группировка по реальным layer IDs.
- Цена выбирается из override, явно заданных компонентов или шаблона; не вводились новые модели TCO/эффективности. Backend cache связан с project/version/calculationVersion, чтение повторно авторизуется.
- Для saved-проекта карта и калькулятор используют целиком закреплённую серверную projection; для dirty — целиком локальную draft projection. Ошибка server cost не подменяется локальным «успехом».

### Provenance и документы

- ADR-0021: native categories/roles и типизированные поля карточек сохраняются при round-trip; unknown/demo происхождение не превращается самопроизвольно в confirmed. Сервер задаёт author/time/revision; document source хранит ID/revision/checksum.
- Обновление библиотеки требует preview/apply. Замороженные ревизии и instance overrides сохраняются; неподходящие поздние preview не применяются.
- Реальные multipart bytes, лимит 10 MiB, PDF/PNG/JPEG/TXT, проверка MIME/signature/имени, private filesystem storage, quarantine → scanner → ready/rejected. Download повторно проверяет доступ к parent и целостность; публичные ссылки не выдаются. Delete деактивирует документ с audit.
- В локальном сквозном browser fixture использовался **test-only clean scanner**. Это не доказательство работы настоящего антивируса. `APP_DOCUMENTS_ENABLED` по умолчанию false.

### Заявки на демонстрацию

- ADR-0019: durable lead + receipt + outbox, повтор с тем же payload/key не создаёт второй lead после потерянного ответа, lease/retry и отказ от plaintext SMTP.
- Consent versions, разрешённые origins, proxy trust, recipient и delivery зависят от конфигурации. Реального письма адресату не отправляли; production consent/retention/owner не выдумывались.

## 4. Незавершённая FRC-06

Точный перечень файлов, состояний и команд: [frc06/recovery-checkpoint.md](frc06/recovery-checkpoint.md).

Есть `project-save-state`, scoped `project-draft-storage`, businessRevision/savedProject/saveAttempt в store и frozen request helpers. Исправлено чтение authoritative version из GET вместо cached list. Server runtime policy `FORTIS_LOCAL_DRAFTS_ENABLED` добавлена; persistent drafts в workspace по умолчанию выключены.

Основной variants store **ещё не подключён к новому save pipeline**. Три ожидаемых RED:

1. UI selection во время PUT ошибочно оставляет проект dirty.
2. После неоднозначного 503/504 отсутствует verification GET перед следующей записью.
3. Повтор create не сохраняет идентичные body и idempotency key.

Не завершены explicit recovery UI, проверка scope/access перед восстановлением и replay, save/stay/discard guards при смене проекта/enterprise/logout. Старое автоматическое восстановление уже отключено; включение новой storage policy само по себе ещё не даёт готового recovery flow.

## 5. Почему пользователь упёрся в workspace

Это требование **FRC-03**, а не дефект, исправляемый снятием authorization:

- §4.2 / WS-02: понятное состояние без memberships и disabled create.
- §4.3: оператор создаёт enterprise с явно заданными GIS-координатами и назначает участника; документированный процесс **без developer SQL**.
- WS-03: после назначения и обновления списка enterprise появляется и допускает первую конфигурацию.

Последняя проверка локальной базы: есть три пользователя, включая `root` и `root2`, два тестовых предприятия, **нет ни одного назначения `user_enterprises`**, проектов нет. В открытой пользовательской вкладке подтверждены пустой список и disabled create.

После обращения пользователя изменён только `frontend/src/modules/workspace/ui/project-workspace-page.tsx`:

- добавлено объяснение отсутствия назначений и следующего шага;
- «Обновить» перечитывает enterprises вместе с projects;
- выбранное предприятие сверяется со свежим списком;
- создание недоступно при loading/error; без доступного выбора проекты не показываются;
- добавлено accessible name поля конфигурации и уточнены пустые состояния.

Проверено в текущей in-app вкладке: объяснение появилось, Refresh выполнил два дополнительных scoped enterprise SQL-запроса, console errors/warnings отсутствовали. Scoped eslint, TypeScript и diff check прошли. Это локальная UI-проверка, **не приёмка WS-01…WS-08**.

Пользователю предложен выбор `root`/`root2` для назначения доступа к конкретному локальному тестовому предприятию. Ответ не получен, права не менялись. Ручное назначение может разблокировать локальный прогон, но не заменяет штатный operator provisioning и не закрывает FRC-03.

## 6. Локальная среда после остановки run

По отдельным сообщениям пользователя исправлены две последовательные проблемы:

1. `503 configuration_error` при login: у frontend отсутствовали backend settings. Создан игнорируемый `frontend/.env.development.local` с `BACKEND_URL=http://127.0.0.1:8090` и `FORTIS_LOCAL_DEVELOPMENT=true`; dev-сервер перечитал файл. README дополнен.
2. Позднейший `502 backend_unreachable`: прежний backend перестал слушать 8090. Причина завершения старого процесса не установлена. Найдена существующая локальная база `rr` на 127.0.0.1:5432, сделан и проверен backup, собран и запущен текущий backend.

Создан игнорируемый `backend/.env` с mode 0600, dev/webapp, параметрами существующей локальной базы и случайным JWT secret. Секрет не помещён в отчёты/Git; новая подпись требует повторного входа старых сессий. README описывает `make run-dev` и автоматические миграции при старте.

**Локальные миграции действительно применялись**: schema version 10 → 1789916000, dirty=false. Это произошло после остановки основного run при восстановлении local backend. Production не затрагивалась. Backup до запуска: `/private/tmp/fortis-local-backend-recovery-qpf_qe6c/before-start.dump` (0600); log: тот же каталог, `backend.log`. Бинарь: `/private/tmp/fortis-local-backend-app`.

Последние проверки: frontend ready=200, пустой login=400, случайный несуществующий аккаунт=401, пустая registration=400; затем пользователь самостоятельно вошёл в workspace. Backend оставлен запущенным, frontend localhost:3000 также работает по последней проверке. Перед продолжением проверить процессы заново. Отдельный старый синтетический PostgreSQL-кластер release tests на 55434 остановлен.

## 7. Проверки и ограничения доказательств

Ниже результаты ранее выполненных прогонов; при составлении отчёта они не запускались повторно. Свежо перепроверены Git HEAD/branch и прочитаны отчёты.

- FRC-04: real PostgreSQL revision/CAS/idempotency/audit и lossless frontend → backend → export → frontend, профильные build/vet/lint/types, независимый review; детали в [frc04](frc04/implementation-report.md).
- FRC-05/09: финальный объединённый Chromium run **23/23** = calculator 10 + documents 7 + manager 6. Не считать это 23 независимыми сценариями каждой спеки.
- FRC-05 live: Next → Go → PostgreSQL, точная сумма 47 500 000 minor units (475 000 ₽), две реальные группы, hidden object учтён, desktop/mobile. [Отчёт](frc05/implementation-report.md), [evidence](frc05/test-evidence.md).
- FRC-09 live: реальные bytes/private files/DB, invalid MIME 415, upload 201, checksum и byte equality, чужой доступ 404, deleted download 404, provenance round-trip. Backend race, combined PostgreSQL regressions, scoped OpenAPI и frontend production build прошли. [Отчёт](frc09/implementation-report.md), [evidence](frc09/test-evidence.md).
- FRC-11: direct-route gates, demo marker, шесть размеров экрана; [evidence](frc11/test-evidence.md).
- FRC-12: lost-response retry дал один lead, provider failure сохранил outbox, public endpoint не раскрывает registry; [evidence](frc12/test-evidence.md).
- FRC-06: pure state/storage GREEN; lifecycle suite **4/7 PASS, 3 FAIL**. Полная интеграция не проверена.

Остаются отдельные известные риски:

- Финальный полный regression после всех изменений не выполнен. Ранее полный frontend baseline был 84/90, с шестью зафиксированными историческими failures; это не разрешение игнорировать новые ошибки. Имена перечислены в autonomous-run.md.
- Синтетический сценарий с двумя custom layers одинакового кода обнаружил duplicate deck layer IDs и console assertions. Финансовая группировка по реальным IDs корректна; нельзя заявлять чистую консоль карты во всех сценариях.
- В package.json закреплён Next 16.2.5, фактически установлен 16.2.11. Требуется согласование toolchain в итоговом release gate.
- Проверен scoped OpenAPI изменённых модулей; whole-schema validation ранее выявляла legacy annotation errors.
- Не доказаны production TLS/artifact identity, migrations/rollback, storage/scanner/retention/backup, реальная SMTP-доставка и согласованные владельцы/политики.

## 8. Состояние Git и артефакты

Все четыре репозитория на `develop`. Последние fetch показали 0 ahead / 0 behind; при подготовке отчёта HEAD повторно сверены:

| Репозиторий | HEAD |
| --- | --- |
| parent | `b173183d85a02140b74189b4fde8875c46de4885` |
| frontend | `8a5480fcc803da818cf0feeb135884f5bdcc1e68` |
| backend | `b04696d87b5a5a085c9c5cc4eda1e7dacff8af12` |
| knowledge-base | `80c12da92bfd253e367bc09963fba9dea66857d1` |

HEAD не включает выполненные изменения. Source manifests внутри отчётов фиксируют принятые срезы на момент их создания и могут отличаться от текущих файлов после последующих правок. Перед любым staging/review прочитать реальный diff. Не делать reset/checkout поверх него; не считать submodule pointers обновлёнными.

Опорные документы:

- `docs/fortis-release-specs/specs/FRC-03_workspace.md` — обязательный первый пользовательский сценарий.
- `docs/releases/2026-09-20/frc03/research-checkpoint.md` — gap matrix и proposed provisioning.
- `docs/releases/2026-09-20/frc06/recovery-checkpoint.md` — точное состояние незавершённой реализации.
- `docs/releases/2026-09-20/frc07/backend-plan.md` — бюджетные контракты и открытые решения.
- `knowledge-base/03_Architecture/ADR-0016…ADR-0021` — принятые решения (реальные имена файлов см. KB index).
- `knowledge-base/01_Requirements/Release_2026_09_20_Autonomous_Run.md` — durable context, включая исправления после остановки.

## 9. Что требуется от архитектора

1. Проверить согласованность original FRC-02 с принятым ADR-0017 scope: bootstrap/admin/RBAC/session-membership audit нельзя объявлять выполненными только по label CODE PASS. Подтвердить deferred требования или вернуть их в отдельную обязательную работу.
2. Зафиксировать минимальный штатный operator provisioning для FRC-03: trusted local CLI/process с существующими OS/DB правами, атомарное создание enterprise + membership, валидные явные координаты, без публичного self-service обхода доступа и без ручного SQL в штатной инструкции.
3. Проверить незавершённый save/recovery контракт FRC-06 и закрыть три RED до полной приёмки зависимых потоков. Исследование и ограниченные независимые onboarding/UI-исправления могут идти раньше, полная FRC-03 acceptance — после зависимостей.
4. Приоритизировать реальный вертикальный сценарий: подключённый пользователь → доступное enterprise → create → карта → edit → save → reload с той же server identity/version. Наличие login/HTTP 200 не является его доказательством.
5. Согласовать budget/create/import/duplicate поведение FRC-07; не наследовать бюджет из недоверенного export без явного контракта.
6. Затем завершить FRC-08/10, интегрированный FRC-13 и эксплуатационный FRC-14. Перед выпуском сверить capability gates со всеми прямыми маршрутами и legacy workspace compare UI.
7. После разделения и проверки пересекающихся изменений оформить commits в дочерних репозиториях, затем parent gitlinks. Никакого production-ready утверждения до закрытия runtime evidence.

Это handoff для анализа, не поручение автоматически возобновлять полный run, менять memberships, выполнять deploy или публиковать изменения.

## Публикация checkpoint по запросу пользователя — 2026-09-20

После подготовки отчёта пользователь явно запросил коммит и push в develop всех репозиториев. Это разрешение на публикацию текущего промежуточного состояния, включая незавершённые FRC-03/06, а не приёмка релиза. Предпубликационная проверка: четыре origin/develop синхронизированы; backend go test ./... и frontend tsc --noEmit --incremental false прошли; FRC-06 повторно дал 4 PASS / 3 известных FAIL. Полный frontend suite и production evidence этим не заменяются. Локальные .env, JWT secret и backup базы исключены из Git. Предшествующие указания «коммитов/push не было» описывают состояние до этого запроса.
