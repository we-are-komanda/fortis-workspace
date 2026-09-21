> Active autonomous run authority: the current user authorized FRC03–14 without per-spec approval. Historical statements below that stop after FRC00/01/02 describe earlier runs. Current decisions are in the **Autonomous FRC03–14 addenda** and [autonomous-run](autonomous-run.md). Code acceptance does not promote production/runtime acceptance.

# FRC-00 — исходный комплект и матрица приёмки

Дата: 2026-09-20. Исходный baseline согласован пользователем. Изменения FRC-00
не закоммичены. **FRC-00 не accepted: BASE-02 и фактический runtime backend SHA заблокированы.**
Следующие FRC автоматически не выполняются.

Источники: [спека](../../fortis-release-specs/specs/FRC-00_release_baseline.md),
[общие контракты](../../fortis-release-specs/00_SHARED_CONTRACTS.md),
[исходная матрица аудита](../../fortis-release-specs/ACCEPTANCE_MATRIX.md),
[manifest](release-manifest.json), [журнал доказательств](work-log.md).

## Правила статусов

- `not_verified`: доказательства отсутствуют; это не утверждение об отсутствии реализации.
- `failed`: выполненная проверка выявила несоответствие; приложены сценарий и результат.
- `implemented`: код или документ существует; полнота поведения ещё не доказана.
- `verified`: конкретный сценарий прошёл на указанном SHA/рабочем артефакте и окружении.
- `accepted`: явная приёмка результата с SHA, сценарием, результатом, reviewer и acceptedAt.

Reviewer и acceptedAt для релиза пока не назначены; `accepted` нет ни у одной строки.
Статус Linear фиксируется отдельно. Успех unit-теста не заменяет API/real-backend E2E.
SHA в manifest — исходный комплект; это не выдуманные commit SHA новых рабочих изменений.
Для рабочих скриптов журнал содержит SHA-256 файлов.

## BASE-01…05

| ID | Статус | Реализация / исходный SHA | Сценарий и результат | Оставшееся ограничение |
|---|---|---|---|---|
| BASE-01 | verified (локальный source checkout) | Четыре полных SHA из manifest | S1: чистые отдельные clones, HEAD и parent gitlinks совпадают; PASS. S2: dirty checkout и неверный pin отвергаются | Remote clone всего комплекта и точная сборка образов не проверены; branch не используется вместо SHA |
| BASE-02 | not_verified, BLOCKER | `verify_baseline.py`, рабочий артефакт | S2: сверка синтетических metadata и отказ при неверном digest/SHA/миграциях/mode — PASS. S3: реальных metadata нет, exit 1 | Нет выбранного deployment ID, digest образов, применённых миграций и версий runtime; SSH dev VM отклоняет ключ |
| BASE-03 | verified (текущие артефакты) | Manifest и рабочие скрипты | S2: extra/sensitive fields и env assignments отклонены без вывода значений; ручное чтение подготовленных артефактов | Это структурная проверка, не универсальный secret scanner; новые runtime evidence и артефакты перед публикацией проверяются заново |
| BASE-04 | verified (ограниченный unit-сценарий) | Backend `706665641894c966d2b0b83554554bc3d88b8f94`; FRT-56 Done | S4: существующие `TestUpdateProject*` — PASS: update, сохранение version, conflict, invalid JSON/schema, metadata-only | Реальная БД, cross-user доступ, полный lossless round-trip и browser flow не проверены; FRT-56 не переоткрывался и не принимался заново |
| BASE-05 | verified (обнаружение блокера), runtime BLOCKER | `verify_baseline.py`, рабочий артефакт | S2/S3: отсутствующий SHA выдаёт `BASE-05: backend SHA missing` и блокирует сверку | SHA работающего backend неизвестен; checkout SHA и `.deploy-info` не подставляются |

## Запуск проверок

Из parent с рабочими артефактами FRC-00:

```bash
# S1. Только чистый отдельный checkout; текущий checkout пользователя не менять.
python3 -B docs/releases/2026-09-20/verify_baseline.py source --checkout /path/to/pristine-baseline

# S2. Unit и локальные Git integration checks; только временные clones, без commits.
python3 -B -m unittest discover -s docs/releases/2026-09-20 -v
bash deploy/production/write-deploy-info.test.sh
bash deploy/production/deploy-with-notify.test.sh
bash -n deploy/production/write-deploy-info.sh deploy/production/write-deploy-info.test.sh

# S3. Без runtime-файла ожидается exit 1: сведения отсутствуют.
python3 -B docs/releases/2026-09-20/verify_baseline.py runtime

# После получения реальных очищенных metadata и фиксации ожидаемых значений в manifest:
python3 -B docs/releases/2026-09-20/verify_baseline.py runtime --runtime /path/to/runtime-observation.json
```

S4, из backend чистого baseline:

```bash
GOTOOLCHAIN=local GOPROXY=off go test -count=1 -run '^TestUpdateProject' ./internal/modules/defense_project/application
```

Для воспроизведения S1 создать **новый** каталог: clone каждого repository URL
из manifest с `--no-checkout`, затем `git -C <new-path> checkout --detach <full-sha>`.
Parent клонируется первым, дочерние — в его `frontend/`, `backend/`, `knowledge-base/`.
Не использовать `latest`, pull или текущую вершину ветки вместо SHA. Локальная проверка
использовала `git clone --no-hardlinks --no-checkout <existing-local-repo> <new-path>`;
доступность всех четырёх origin такой проверкой не доказывается.

Чистый source baseline не содержит ещё не закоммиченных release artifacts и пакета.
Проверяющий скрипт запускается из каталога рабочих артефактов, а `--checkout` указывает
на отдельный неизменённый baseline. После коммитов собрать новый candidate и повторить проверки.

## Формат runtime observation

Очищенный JSON содержит ровно поля `deployment` из manifest плюс `frontendSha`,
`backendSha`, `observedAt` (ISO-8601 с timezone). SHA — 40 hex; image digest —
`sha256:` и 64 hex; appliedMigrations — список имён применённых `.up.sql`.
Все ожидаемые deployment-поля manifest должны быть заполнены из проверенных данных.
Их исходные `null` — блокеры, а `runtimeMode: workspace` — требование, не наблюдение.

Снимать значения с реально работающих артефактов/контейнеров и migration state.
Не использовать .deploy-info как источник runtime SHA. Не передавать полный
`docker inspect`, `.env`, connection strings, cookie или customer data. В журнале
наблюдения отдельно указать источник, время и того, кто получил metadata.
Сверка JSON проверяет совпадение, но не удостоверяет происхождение файла: это обязанность reviewer.
Если бинарный артефакт не содержит SHA, требуется отдельная согласованная сборка с
внутренней build metadata; угадывание по ветке запрещено. Deployment сейчас не разрешён.

## Соответствие существующим задачам

Описание и статус перечисленных задач прочитаны через Linear 2026-09-20.
Ссылки — кандидаты на продолжение существующей работы, а не принятие нового scope.
Новые тикеты не создавались; статусы и relations не менялись.

| FRC | Existing ticket / состояние Linear | Статус требований пакета |
|---|---|---|
| FRC-00 | [FRT-9](https://linear.app/fortis-project/issue/FRT-9) Done — только прежний FE verification baseline; отдельный release manifest scope не покрыт | implemented, runtime blocked |
| FRC-01 | [FRT-55](https://linear.app/fortis-project/issue/FRT-55) Done — API client | not_verified |
| FRC-02 | [FRT-69](https://linear.app/fortis-project/issue/FRT-69), [FRT-70](https://linear.app/fortis-project/issue/FRT-70) Done — auth/access; новые роли не входят в прежний scope | not_verified |
| FRC-03 | [FRT-71](https://linear.app/fortis-project/issue/FRT-71), [FRT-72](https://linear.app/fortis-project/issue/FRT-72) Done — workspace/context | not_verified |
| FRC-04 | [FRT-56](https://linear.app/fortis-project/issue/FRT-56) Done — full update + version; immutable revisions — новый scope | not_verified; unit evidence только для существующего update |
| FRC-05 | [FRT-36](https://linear.app/fortis-project/issue/FRT-36) Done, [FRT-51](https://linear.app/fortis-project/issue/FRT-51) Todo — cost/budget | not_verified |
| FRC-06 | [FRT-18](https://linear.app/fortis-project/issue/FRT-18), [FRT-47](https://linear.app/fortis-project/issue/FRT-47) Done — variants/conflict | not_verified |
| FRC-07 | FRT-36 Done, FRT-51 Todo — прежний budget API; атомарный hard gate отдельно | not_verified |
| FRC-08 | [FRT-19](https://linear.app/fortis-project/issue/FRT-19) Todo; [FRT-37](https://linear.app/fortis-project/issue/FRT-37), [FRT-52](https://linear.app/fortis-project/issue/FRT-52) Done — compare | not_verified |
| FRC-09 | [FRT-35](https://linear.app/fortis-project/issue/FRT-35), [FRT-50](https://linear.app/fortis-project/issue/FRT-50) Done — documents; provenance/scanner отдельно | not_verified |
| FRC-10 | [FRT-28](https://linear.app/fortis-project/issue/FRT-28), [FRT-58](https://linear.app/fortis-project/issue/FRT-58) Todo; [FRT-38](https://linear.app/fortis-project/issue/FRT-38) Done — report | not_verified |
| FRC-11 | Подходящая задача не найдена поиском «лендинг»; это не полный аудит tracker | not_verified |
| FRC-12 | Подходящая задача не найдена поиском «заявк»; durable lead scope отдельно | not_verified |
| FRC-13 | [FRT-59](https://linear.app/fortis-project/issue/FRT-59) Todo; FRT-9 Done — E2E/verification | not_verified |
| FRC-14 | Подходящая эксплуатационная задача не найдена поиском «deploy», «release baseline» | not_verified |

Поиск также вернул нерелевантные задачи других продуктовых направлений; они не связаны
с Fortis GIS только на основании общего префикса FRT. Ни одна следующая FRC не реализована здесь.

## Production blockers и граница полного ТЗ

Блокеры комплекта: unknown deployment identity, runtime SHA/digests, applied migrations,
точный build toolchain, отсутствие real-backend приёмки и незакоммиченные candidate artifacts.
Доказательство доступа, бюджета, save recovery, сравнения и воспроизводимого отчёта
относится к следующим FRC; исторический Done не снимает release blockers.

Вне пакета: полноценные spatial/physical проверки ограничений, показатели реальной
эффективности, сценарии/ретроспектива, 3D, realtime collaboration и полнота исходного ТЗ.
Эти требования сохраняются отдельно в knowledge-base и не получают статус accepted.

## Решения и расхождения

- Source baseline с FE `7ae483…` согласован; текущий пользовательский FE `9feeb88…`
  не переключается. В baseline Next `16.2.11`; найденные ранее `16.2.5` относились к другому SHA.
- `.gitmodules` backend URL приведён к проверенному `Ramilko37/fortis-back`.
  Remote develop отвечает `70666564…`; исходный parent SHA сохраняет прежний URL в истории.
- Autosave/manual save, workspace fallback, bootstrap без projectId и все новые
  DTO/роли/денежные/ревизионные решения остаются открытыми. Подробности:
  [knowledge-base release index](../../../knowledge-base/01_Requirements/Release_2026_09_20_Index.md).
- Framework, API/UI, доступы, схема БД и deployment не менялись. Требование обновить
  runtime SHA при его отсутствии не выполняется выдуманными metadata или незапрошенной поставкой.

## Rollback и следующая фиксация

Изменения локальные: проверить diff и отменить только перечисленные рабочие изменения
FRC-00 при необходимости. Пользовательские untracked файлы и текущие SHA не удалять.
После отдельной команды на commit сначала фиксируется knowledge-base, затем parent
с согласованным pointer. Manifest этой исходной проверки сохраняется как baseline;
новые candidate SHA и evidence фиксируются отдельно. Сейчас коммиты и deployment запрещены.


## Subsequent FRC-01 implementation (2026-09-20)

This appendix records a later user-authorized task; preceding FRC-00 observations remain historical.
**FRC-00: Implemented / Acceptance blocked by runtime evidence**, unchanged.
FRC-01 is implemented over frontend `9feeb88`, with locally verified boundary/state/probe regressions and a local production Next server against an isolated stub. It is **not runtime accepted**. See [full commands, defects and limitations](frc01/implementation-report.md) and [ADR-0016](../../../knowledge-base/03_Architecture/ADR-0016-runtime-backend-boundary.md).
No deployment, migrations, commit, push or FRC-02 work performed.


# FRC-01: существующие frontend failures перед FRC-02

FRC-01: **Implemented / code-level acceptance passed / runtime acceptance blocked** — статус принят пользователем.
FRC-00: **Implemented / Acceptance blocked by runtime evidence** — без изменения.

Исходный pre-FRC-01: frontend HEAD 9feeb88, экспортированный во временный каталог; одинаковые установленные зависимости Node 26.4.0. 53/59 passed. После FRC-01: 70/76 passed. Сравнивались сохранённые логи финального прогона FRC-01, тесты заново в FRC-02 не запускались.

| Файл/assertion | Failure signature | Сравнение |
|---|---|---|
| `src/modules/drone-defense/domain/catalog-sidebar-motion-contract.test.mjs:22` | `Catalog sidebar must animate a fluid desktop width instead of unmounting` | Не изменилась |
| `src/modules/drone-defense/domain/map-zoom-controls-contract.test.mjs:6` | `GisBoard must expose clickable map zoom controls` | Не изменилась |
| `src/modules/drone-defense/domain/prototype-3d-placeholder-contract.test.mjs:16` | `Scenario modeling navigation must open a dedicated prototype state` | Не изменилась |
| `src/modules/drone-defense/domain/retrospective-analysis-navigation-contract.test.mjs:21` | `DefenseStudioShell must expose the new WIP route in desktop rail and compact navigation drawer` | Не изменилась |
| `src/modules/drone-defense/domain/user-facing-copy-contract.test.ts:119` | `GIS runtime must read workspace and compact-card copy from prototypeRu` | Не изменилась |
| `src/shared/lib/defense-project.test.ts:69` | `shared asset catalog must not expose user-facing recommendation or compatibility labels` | Не изменилась |

Все 6 исключений и полные stack traces совпали после замены только абсолютного checkout root на `<frontend>`. Для первых двух совпадают ERR_ASSERTION, actual=false, expected=true, operator=`==`. Лог нормализованных сигнатур: [полные сигнатуры](frc02/pre-frc02-failure-signatures.txt). Никаких исправлений этих тестов в FRC-02 нет.
# FRC-02 implementation addendum — 2026-09-20

Latest FRC-02 status: **Implemented / code-level verification passed / production runtime acceptance blocked**. This addendum does not upgrade historical FRC-00/01 runtime status. Full frontend suite remains non-green due to six unchanged pre-existing failures.

| Gate | Result |
|---|---|
| A Enterprise isolation / membership mutation | PASS, A↔B; ordinary JWT cannot self-grant |
| B–C Project IDs, CRUD/export/import/immutable enterprise | PASS |
| D–E Financial/report/compare parents | PASS; both operands authorized |
| F–G Private asset/document parents + no URL disclosure | PASS at API boundary |
| H Account switch / scoped recovery / stale responses | PASS state tests + real browser |
| I Revocation, unchanged JWT/cookie | PASS memory + PostgreSQL + browser |
| J Public reads / operator-only mutation | PASS |
| Orphans / foreign vs missing / access-storage 500 | PASS memory + SQL NULL cases |
| Go normal/unit suites + build | PASS |
| Frontend auth/identity | PASS 14/14 including five stale access-error cases found during review |
| FRC-01 regressions | PASS within full frontend/Go suites |
| Full frontend suite | 90 tests: 84 PASS, 6 pre-existing FAIL; normalized signatures identical 6/6 |
| Frontend types / changed-files lint / production build | PASS |
| Local PostgreSQL integration | PASS synthetic DB; no production connection |
| Browser E2E | PASS 3/3 after reviewed fix, five viewport widths |
| Production DB orphan inventory / cleanup decision | BLOCKED, production DB not inspected |
| Production storage ACL / URL expiry / previously issued URLs | BLOCKED, runtime evidence absent |
| Deployed artifact identity, production TLS/cookie and persistence | BLOCKED, no deployment/runtime evidence |

Evidence: [implementation report](frc02/implementation-report.md), [route matrix](frc02/authorization-matrix.md), [commands/logs](frc02/test-evidence.md), [incremental file inventory](frc02/changed-files.md), [orphan inventory](frc02/orphan-inventory.md). Independent review found one stale frontend error race; reproduced in five cases and fixed RED→GREEN. No backend authorization bypass found by that review; this is not a production security audit.

FRC-00 remains Implemented / Acceptance blocked by runtime evidence. FRC-01 remains Implemented / code-level acceptance passed / runtime acceptance blocked. No FRC-03, commit, push, deployment or production migrations.

# Autonomous FRC03–14 addenda

## FRC-11 — CODE PASS / RUNTIME BLOCKED

Reviewer root; code acceptance2026-09-20. COPY01/02/03/05/06/07 PASS within local checks; COPY04 local demo marker PASS, production origin/cookie/storage separation BLOCKED. FRC11 focused20/20 plus latest4/4, typecheck/lint/build PASS. Real Chromium:6 widths and11 blocked direct routes, actual synthetic PG-backed login, no console errors/overflow. Hidden offscreen CTA review defect fixed. Capability manifest keeps unaccepted financial/version functions not_released.

Evidence: [implementation](frc11/implementation-report.md), [tests](frc11/test-evidence.md), [files](frc11/changed-files.md), [working source hashes](frc11/source-manifest.json). No production deployment; source and UI are local candidates.

## FRC-04 — CODE PASS / RUNTIME BLOCKED

REV01–10 and scoped project audit PASS. PostgreSQL15 top-level+8 nested (includes FRC02); full Go243+84 and unit-tag275+84 PASS with21 explicit opt-in skips, separately run relevant SQL; build/vet PASS. FE round-trip3/3 including actual DB output, focused boundary regressions, types/lint/build PASS. Independent reviewer reproduced and closed geometry panic and expired receipt race; no open findings. Scoped generated OpenAPI validates; whole API legacy annotations outside04/12 tracked forFRC13. Production migration/deployed retention/runtime evidence remains blocked.

[Implementation](frc04/implementation-report.md) · [tests](frc04/test-evidence.md) · [files](frc04/changed-files.md) · [source hashes](frc04/source-manifest.json) · [OpenAPI](frc04/openapi.json). Root grants code acceptance and FRC05/09 implementation dependency is satisfied; FRC07 budget enforcement remains downstream.

## Autonomous FRC12 acceptance —2026-09-20

**CODE PASS / RUNTIME BLOCKED.** LEAD01–10 local evidence, independent review and actual browser→BFF→Go→PostgreSQL retry/receipt verified. See [implementation](frc12/implementation-report.md), [tests](frc12/test-evidence.md), [runtime gates](frc12/runtime-configuration.md). Publication remains disabled pending owner policy and actual SMTP/alert/TLS/ingress evidence.

## FRC05 root code acceptance — 2026-09-20

**CODE PASS / RUNTIME BLOCKED.** COST01–11: exactminor sharedgolden, FE/BEparity, immutablePGcache andauthorization, onepinnedsavedprojection/all-draft UI. Actualbrowser/BFF/Go/PG475000rub, hiddenrows andcustomlayers; Chromium9/9 late/error/zero/null regressions; types/lint/productionbuild/scopedSwaggerPASS. No newunexplained05failure. ProductionTLS/toolchain/migrations remainFRC13/14. [Implementation](frc05/implementation-report.md), [tests](frc05/test-evidence.md), [files](frc05/changed-files.md), [hashes](frc05/source-manifest.json). FRC06 code dependency satisfied. No push/deploy/productionmigration.

## FRC09 root code acceptance —2026-09-20

**CODE PASS / RUNTIME BLOCKED.** DATA01–10: provenance/typedcardroundtrip, explicitrefresh, immutableprivatedocuments, quarantine+auth+audit, actualbrowserfilebytes andforeign404. Rootchangedlint/build/scopedOpenAPI PASS; combinedChromium23/23, Node23/23, actualPG/racetests passed. [Report](frc09/implementation-report.md), [tests](frc09/test-evidence.md), [files](frc09/changed-files.md), [hashes](frc09/source-manifest.json). Real scanner/storage/retention/TLS/productionmigration remain FRC14. Userrequested stopafter09; FRC06partial, whole release notaccepted.


## FRC-06 — resumed acceptance, 2026-09-21

**PASS — local staged acceptance.** All 30 user criteria PASS; SAVE01–08/10 PASS. SAVE09 NOT APPLICABLE while official-report capability remains disabled; actual dirty Save/last-saved workflow mandatory in FRC10. No report or production PASS.

Focused48/48, rendered Chromium13/13, real Next→Go→PostgreSQL six checkpoints PASS. Original v1→2→3→4, independent copy v1 survives reload. Go tests/build + realPG21 top-level PASS. Frontend regressions38PASS/1explicitPGskip; full250=201PASS/6 historical FAIL/43opt-inSKIP, exact signatures6/6 unchanged. Types/lint21files/build PASS; test/build source manifests454files identical, drift=[]. Seven review defects fixed, eight independent probes PASS. Frontend `a56d128e715ed09387428ad3dd67434d18855dd5`.

[Implementation](frc06/implementation-report.md) · [30+SAVE criteria](frc06/acceptance-criteria.md) · [tests](frc06/test-evidence.md) · [review](frc06/independent-review.md) · [checkpoint](frc06/recovery-checkpoint.md). FRC03 may proceed; whole release remains unaccepted.
