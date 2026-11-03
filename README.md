# Fortis Workspace

Umbrella workspace for the Fortis ecosystem.

## Локальный запуск

Из корня workspace выполните одну команду:

```bash
make dev
```

Она запускает backend и frontend, проверяет готовность PostgreSQL через API
и запрос проектов через frontend, затем сообщает адрес `http://localhost:3000`.
Терминал нужно оставить открытым. Ctrl+C останавливает оба сервера и их дочерние
процессы. При завершении одного процесса supervisor делает до трёх попыток
перезапуска; при неисправимой ошибке останавливает весь комплект.

Предварительно нужны Python 3, Go, Node/npm, установленные зависимости frontend
(`cd frontend && pnpm install`), настроенный `backend/.env` и запущенная локальная
PostgreSQL с существующей схемой Fortis. Команда не создаёт БД, не устанавливает
зависимости и не запускает миграции отдельно. Обычный startup backend сохраняется.
Порты 3000 и 8090 должны быть свободны: старые серверы следует остановить перед
первым единым запуском. Чужие процессы скрипт не завершает.

Логи: `.fortis-dev/backend.log` и `.fortis-dev/frontend.log` (исключены из Git).
Проверка supervisor: `make test-dev`.

This repository stores workspace-level context for the Fortis ecosystem: how the Fortis repositories fit together, how agents should navigate them, and which repository owns each kind of change.

## Repositories

- `frontend/` - Fortis frontend application, tracked as a Git submodule from `Ramilko37/fortis-front`.
- `backend/` - Fortis backend/API repository, tracked as a Git submodule from `Ramilko37/fortis-back`.
- `knowledge-base/` - Obsidian-compatible project knowledge base, tracked as a Git submodule from `Ramilko37/fortis-knowledge-base`.
- `Fortis/` - legacy local Obsidian vault copy kept outside the parent Git history.

Frontend, backend, and knowledge base keep separate Git histories. The parent repository pins the selected commit for each submodule.

## Release baseline

The [2026-09-20 release manifest](docs/releases/2026-09-20/release-manifest.json)
pins the agreed FRC-00 source baseline. See the
[acceptance matrix and verification instructions](docs/releases/2026-09-20/acceptance-matrix.md)
for evidence and unresolved runtime blockers. Source verification is not release acceptance.

## Agent Workflow

Open this directory as the workspace when working across the Fortis ecosystem.

Before making durable product, architecture, UX, or domain decisions, read the knowledge base index and relevant notes. Record durable decisions back into the knowledge base.

Clone with submodules or initialize them after cloning:

```bash
git submodule update --init --recursive
```
