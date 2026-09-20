# FRC-01 — отчёт реализации, 2026-09-20

**Implemented; локальные проверки выполнены; runtime acceptance не подтверждена.**
FRC-00 сохраняет статус **Implemented / Acceptance blocked by runtime evidence**.
Работа выполнена поверх frontend `9feeb88`, backend `7066656`, parent `dbc2d05`, knowledge-base `eca5ee3` с сохранением предыдущих рабочих изменений. Коммитов, push, deployment и migrations нет. FRC-02 не начат.

## 1. Исправленные подтверждённые defects

- BFF и API rewrite выбирали backend независимо; теперь используют один server resolver без неявного remote/production localhost.
- JSON parsing в proxy терял HTML/empty upstream errors и повреждал download semantics. Raw forwarder сохраняет статус/тело; JSON adaptation выполняется отдельно.
- Malformed successful JSON и пустой project response могли становиться данными/200 null. Теперь это protocol error; валидный пустой список остаётся пустым.
- Mock facilities/catalog и bundled asset fallback проникали в workspace при ошибке или пустом результате. Введён server mode, canonical enterprises; query/localStorage не выбирают demo.
- Refresh и recovery normalizer добавляли bundled assets или заменяли импортированные значения. Общая нормализация сохраняет данные; чистый workspace constructor не содержит demo assets/layers.
- Ошибка загрузки, повторный mount и запоздавший ответ могли заменить открытый проект/правки. Загрузка учитывает отмену, поколение запроса и изменение проекта; recovery не перезаписывает открытое состояние.
- Ошибки сохранения и cost/report стали видимыми, без финансового local fallback. В текущем checkout save уже ручной: autosave не добавлен, retry timer отсутствует; новые правки во время save сохраняются.
- Backend readiness не проверял DB. Добавлен bounded PingContext; frontend live и ready разделены, Compose healthcheck frontend использует live.

Перед production edits выполнен [baseline → current → target reconciliation](reconciliation.md). После независимого review три дополнительных state defects воспроизведены regression tests и исправлены в общих точках.

## 2. Изменённые файлы

[Полный список по репозиториям](changed-files.md). Ключевые точки:

- Frontend: `shared/server/runtime-config.ts`, `infra/backend-proxy.ts`, `/api/v1/[...path]`, auth/project BFF, live/ready/runtime routes, API clients, runtime provider, project/variants/studio stores и их потребители.
- Backend: `cmd/app/dependencies.go`, DB probe и его tests.
- Knowledge-base: новый ADR-0016, индекс, roadmap, дополнение release index. ADR-0008/0010 сохранены.
- Deploy: Compose, frontend Dockerfile, README; parent release appendix и этот отчёт.

## 3. Принятые contracts

Полное решение: [ADR-0016](../../../../knowledge-base/03_Architecture/ADR-0016-runtime-backend-boundary.md).

| Случай | Контракт |
|---|---|
| Backend selection | Обязательный BACKEND_URL; aliases должны совпадать; один resolver для BFF и v1 |
| Public/private transport | HTTPS публично; private HTTP только явно разрешённый, с внешним HTTPS |
| Runtime | server workspace/demo; default workspace; query и localStorage режим не меняют |
| HTTP errors upstream | Исходные 401/403/404/409/500, body/content-type/request id сохранены |
| Boundary failures | Config 503; unreachable 502; deadline 504; generated requestId, retryable=false |
| JSON success | Parseable JSON + необходимая endpoint shape; malformed = protocol error |
| Empty | Legitimate empty list допустим; пустой project envelope ошибочен |
| Canonical enterprise | /api/v1/enterprises; facilities доступен только demo |
| Project state | Failed refresh/load не подмешивает demo и не уничтожает правки |
| Recovery | source сохранён, отдельный syncStatus=unverified; не server confirmation |
| Save | Текущий manual save; no scheduled retry, visible error, pending edits сохранены |
| Health | Live = process; ready = config/dependencies; DB readiness deadline 2 s |

Timeout API 10 s, documents 30 s; env overrides 1–120000 ms. Raw body streaming не буферизуется в JSON. После отправки headers raw timeout прерывает stream: изменить уже отправленный status на 504 невозможно. JSON adaptation читает body до собственного ответа, поэтому deadline body возвращает 504.

## 4. Добавленные tests

- `backend-proxy.release.test.ts`: один HTTP target BFF/v1, query/auth/method; JSON/HTML/empty errors, 403/404/409/500, missing/conflicting config, refused/timeout, malformed success, empty project, demo gate, binary 206 и byte equality. Отдельно deadline после получения headers, во время JSON body.
- `readiness.release.test.ts`: frontend live независимо от конфигурации/dependencies; ready healthy/outage/config.
- `project-runtime.release.test.ts`: no bundled fallback; empty enterprises; failed load/save, отсутствие retry после 409/500/502/504; recovery unverified; импорт сохраняет каталог и цены; чистый draft; remount dirty; pending edits и abort navigation.
- `database_check_service_test.go`: DB readiness healthy/failure/deadline, sanitized error; liveness не вызывает DB.
- Existing store/proxy tests адаптированы к явному demo fixture и настоящему Response. Assertions на неявный fallback заменены утверждениями согласованного workspace contract.

Первый прогон новых boundary tests был RED (11 failed/1 passed). После исправлений новые regression tests — 17/17 PASS. Review defects также сначала воспроизведены, затем исправлены. Эти тесты проверяют настоящий локальный HTTP stub; global fetch не заменяет upstream Response handcrafted объектом.

## 5. Реально выполненные проверки: команды и результаты

Команды ниже выполнялись из указанного cwd; `rtk proxy` сохраняет обычную семантику команды. Loopback listen блокируется sandbox (`EPERM`); повторный запуск с разрешением на локальные тесты выполнен успешно. Это ограничение среды, не PASS первого запуска.

### Frontend focused tests — PASS 17/17

Cwd `/Users/rr/Documents/Fortis/frontend`:

```bash
rtk proxy node --import tsx --test src/modules/drone-defense/infra/backend-proxy.release.test.ts src/modules/drone-defense/infra/readiness.release.test.ts src/shared/lib/project-runtime.release.test.ts
```

### Полный frontend suite и контроль до изменений — FAIL, одинаковые 6 падений

Полная реально выполненная команда (из parent):

```bash
rtk proxy python3 - <<'PYTEST'
import subprocess
from pathlib import Path
root=Path('/Users/rr/Documents/Fortis/frontend')
for cwd,log in [(root,'/private/tmp/frc01-all-tests-final.log'),(Path('/private/tmp/fortis-frc01-before'),'/private/tmp/frc01-before-tests-final.log')]:
    files=sorted(str(p.relative_to(cwd)) for p in (cwd/'src').rglob('*') if p.is_file() and p.name.endswith(('.test.ts','.test.tsx','.test.mjs')))
    result=subprocess.run(['node','--import','tsx','--test','--test-concurrency=2',*files],cwd=cwd,capture_output=True,text=True)
    Path(log).write_text(result.stdout+result.stderr)
    print(cwd, 'files',len(files),'exit',result.returncode)
    print('\n'.join(line for line in result.stdout.splitlines() if line.startswith('ℹ')))
PYTEST
```

Текущий: 59 files, 76 tests, **70 pass / 6 fail**, child exit 1. Контрольный неизменённый HEAD 9feeb88: 56 files, 59 tests, **53 pass / 6 fail**, child exit 1. Python wrapper exit 0 не означает PASS suite. Контроль экспортирован через git archive в tmp с теми же установленными dependencies; рабочий checkout не переключался.

Одинаковые падающие файлы до/после:

- `domain/catalog-sidebar-motion-contract.test.mjs`
- `domain/map-zoom-controls-contract.test.mjs`
- `domain/prototype-3d-placeholder-contract.test.mjs`
- `domain/retrospective-analysis-navigation-contract.test.mjs`
- `domain/user-facing-copy-contract.test.ts`
- `shared/lib/defense-project.test.ts`

Не исправлялись как unrelated scope; полный suite не зелёный.

### Typecheck — PASS

Cwd frontend:

```bash
rtk proxy pnpm exec next typegen
rtk proxy pnpm exec tsc --noEmit --incremental false
```

До regeneration мешали старые generated `.next` types; финальный tsc exit 0.

### Lint — changed PASS, full FAIL

Cwd frontend:

```bash
rtk proxy pnpm lint > /private/tmp/frc01-full-lint.log 2>&1
```

Exit 1: 45 errors в неизменённом `src/app/page.tsx`; 2 warnings в `postcss.config.mjs` и `defense-tool-icon.test.ts`. Файлы не менялись в FRC-01.

Полная команда проверки изменённых source files (из parent):

```bash
rtk proxy python3 - <<'PYLINT'
from pathlib import Path
import subprocess
root=Path('/Users/rr/Documents/Fortis/frontend')
files=subprocess.check_output(['git','diff','--name-only','--diff-filter=ACMR'],cwd=root,text=True).splitlines()+subprocess.check_output(['git','ls-files','--others','--exclude-standard','src'],cwd=root,text=True).splitlines()
files=sorted(set(f for f in files if f.endswith(('.ts','.tsx','.mjs'))))
r=subprocess.run(['pnpm','exec','eslint',*files],cwd=root,capture_output=True,text=True)
Path('/private/tmp/frc01-eslint-final.log').write_text(r.stdout+r.stderr)
print('changed eslint',r.returncode,'files',len(files));print(r.stdout+r.stderr)
PYLINT
```

Exit eslint 0, без findings.

### Build — PASS после разрешения network

Cwd frontend:

```bash
rtk proxy env FORTIS_NEXT_DIST_DIR=.next/frc01-build pnpm build > /private/tmp/frc01-build-final.log 2>&1
```

Первый sandbox build не смог скачать Google Fonts; повтор с network permission завершён exit 0. Установлен Next 16.2.11 при package текущего checkout 16.2.5; dependencies не обновлялись. Это local build evidence, не доказательство воспроизводимости release toolchain. Автоматические dist-dir additions/formatting tsconfig удалены после build.

### Running Next HTTP integration — PASS, 3 режимных прогона

```bash
rtk proxy node /private/tmp/frc01-http/next-http.mjs
```

Script запускает собранный Next на loopback и изолированный HTTPS stub с временным сертификатом. Проверены workspace BFF/v1 HTML 401, query/trailingSlash, empty project error, byte-exact binary download, live 200 при ready 503; отдельно missing config: landing/live 200, API/ready 503; отдельно demo: marked facilities 200, canonical API 404. Временные Next/stub процессы остановлены. Script/logs в tmp — диагностические артефакты текущей сессии, не portable E2E suite; приватный ключ не переносился в Git.

### Backend — PASS

Cwd `/Users/rr/Documents/Fortis/backend`:

```bash
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go test ./...
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache go build -o /private/tmp/fortis-frc01-backend ./cmd/app
```

Обе exit 0. Go предупреждал о недоступности записи module metadata в системный cache; это не изменило exit/result. Backend binary не запускался, startup migrations не выполнялись. Integration tests с отдельным DB build tag не запускались.

## 6. Что осталось непроверенным

- Реальный Go API + PostgreSQL, DB outage в контейнере, migration state; readiness dependency проверена fake Ping и HTTP stub, не живой DB.
- Production VM/container image, private network isolation, внешний TLS/certificates, nginx routing, deployment identity/digests/runtime SHA.
- Browser UX/visual/a11y walkthrough, реальные пользовательские сессии и документы большого размера; локальный HTTP smoke не покрывает всю UI навигацию.
- Multi-user recovery/identity partition, revision contracts FRC-04/06, FRC-07 и любые прочие FRC scope.
- Reproducible clean dependency install/build: использован уже установленный toolchain, расхождение Next package/runtime сохранено и раскрыто.

## 7. Новые или оставшиеся blockers

Новых blockers реализации FRC-01 не обнаружено в выполненных проверках. Остаются 6 прежних test failures, full lint 45 errors/2 warnings и runtime evidence blockers FRC-00. Они не скрыты статусом PASS focused tests. Runtime acceptance FRC-01 и release acceptance не заявляются. Недоступный ранее SSH runtime evidence не заменяется checkout metadata.

## 8. Diff summary по владельцам

- **Frontend:** единый transport/config, validated JSON clients, server mode, demo gating, project state safety, canonical enterprise flow, live/ready; точечные status/error UI и tests. Без новых dependencies и нового autosave.
- **Backend:** один DB check, подключение readiness, focused tests; liveness сохранён независимым. Schema/migrations не менялись.
- **Knowledge-base:** новый ADR и ссылки/запись статуса; прежние ADR сохранены, конфликтующие положения явно superseded/clarified.
- **Deploy/parent:** runtime env вместо build URL, frontend liveness healthcheck, эксплуатационная заметка, reconciliation и evidence report. Runtime deployment не выполнялся.

Существующие FRC-00 и пользовательские изменения сохранены. Задача остановлена на FRC-01.
