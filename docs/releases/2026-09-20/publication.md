# Фиксация FRC-00/01/02 в develop — 2026-09-20

Пользователь отдельно разрешил commit и push всей выполненной работы в develop четырёх репозиториев. Deployment и production migrations не выполнялись; runtime acceptance не повышается. Исторические baseline SHA и отчёты оставлены как свидетельства состояния на момент проверки.

## Дочерние репозитории

| Repository | Pushed develop SHA |
|---|---|
| frontend | `8a5480fcc803da818cf0feeb135884f5bdcc1e68` |
| backend | `b04696d87b5a5a085c9c5cc4eda1e7dacff8af12` |
| knowledge-base | `80c12da92bfd253e367bc09963fba9dea66857d1` |

## Frontend integration

User-approved choice: сохранить текущий проверенный checkout, поскольку remote develop содержал 14 более поздних коммитов с изменениями 110 файлов. Commit `0cdb577` фиксирует выполненную работу; merge `8a5480f` добавляет историю `origin/develop` с сохранением дерева `0cdb577` (равенство подтверждено `git diff --exit-code`). Затем локальный develop обновлён fast-forward; обычный push выполнен без force. Исходные remote-коммиты остаются в истории, их изменения не заменяют утверждённую версию файлов.

## Повторные проверки перед фиксацией

- Backend `go test -count=1 ./...`: PASS.
- Frontend полный source suite: 90 tests, 84 PASS, те же 6 известных FAIL.
- Parent `python3 -B -m unittest discover -s docs/releases/2026-09-20`: 10/10 PASS.
- `bash deploy/production/write-deploy-info.test.sh`: PASS.
- Staged source/document diff checks: PASS; raw evidence logs retain test-runner whitespace.

Типизация, lint, production build, PostgreSQL и browser E2E evidence — [FRC-02](frc02/test-evidence.md). Генерируемые `frontend/output/` и `deploy/production/.deploy-info` остаются локальными и исключены через .gitignore. Parent фиксирует исходники координации, спеки, отчёты и точные новые gitlinks.
