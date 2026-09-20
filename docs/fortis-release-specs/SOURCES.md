# Основания пакета и ограничения проверки

Дата подготовки: **20 сентября 2026 года**.

## Как читать основания

- **Проверено в коде** — конкретный участок прочитан при подготовке пакета. Это не автоматически воспроизведённый runtime-баг.
- **Предыдущий аудит** — наблюдение из предыдущего ответа/приложенного журнала, требующее воспроизведения перед исправлением.
- **Принятый контракт** — действующий ADR или явно установленная граница roadmap.
- **Предложенная спецификация** — документ в базе знаний со статусом «предложена», а не доказательство реализации/приёмки.
- **Решение пакета** — конкретизация для кодеров, предложенная в этом документе. При расхождении с принятым ADR требуется зафиксировать изменение решения, а не молча переписать продукт.

## Источники проекта

[S1] Исходное «ТЗ_Картографическая_модель_защиты», разделы 1.1, II и III. Предоставлено в разговоре. Используются требования к GIS, стоимости, вариантам, документам и доступам. Разделы о ретроспективе и моделировании не включаются в текущий пакет.

[S2] Предоставленный `system-prompt.txt`. Используется как исторический контекст архитектуры и конвенций. Указанные там ветки, версии стека и статусы FRT не считаются актуальными без FRC-00.

[S3] Предоставленный `Исследование ТЗ и рынка.txt`. Дополнительный предложенный roadmap. Он не отменяет действующий scope и не означает, что все описанные задачи отсутствуют в коде.

[S4] Предыдущий ответ с аудитом и `verification_log_2026-09-10.md`. **В предыдущем ответе и журнале указано 10 сентября, тогда как текущая дата разговора — 20 сентября 2026 года. Дату 10 сентября не используем как надёжную метку свежей проверки.** HTTP-наблюдения, отличие на 104 коммита, данные плана хостинга и утверждение о форме заявки переносятся как основания для повторной проверки, а не как независимо подтверждённые сегодня результаты. Живое приложение, логин, deployment и тесты в этом ходе заново не проверялись.

[S5] Индекс knowledge-base/develop, прочитан при подготовке. Blob `f145a57f3498bcd0ece0fbeffd392aed7adafa6f`.
https://github.com/we-are-komanda/fortis-knowledge-base/blob/develop/00_Index.md

[S6] Roadmap knowledge-base/develop, прочитаны строки 1–190. В документе указаны актуализация 23 июля и последнее обновление 26 июля 2026 года. Подтверждены: GIS MVP; P2/P3 вне критического пути; история отката интерфейса; единый DefenseProject; часть уже выполненных работ.
https://github.com/we-are-komanda/fortis-knowledge-base/blob/develop/Продуктовый_план_Fortis.md

[S7] «Спецификация 00: базовый контракт и методики», **предложена** 13 июля. Blob `3649d20a30e2f1fe8717f24089b4aae56b40d8ab`. Версии расчётов, происхождение данных, отсутствие silent overwrite.
https://github.com/we-are-komanda/fortis-knowledge-base/blob/develop/01_Requirements/Спецификация_00_Базовый_контракт_и_методики.md

[S8] «Спецификация 03: сквозной GIS, бюджет и отчёт», **предложена** 13 июля. Blob `b06f1602f0eefdcc589c40b1ad5caff2d2b83441`. Server-backed workflow, состояния сохранения, единая версия отчёта.
https://github.com/we-are-komanda/fortis-knowledge-base/blob/develop/01_Requirements/Спецификация_03_Сквозной_GIS_бюджет_и_отчёт.md

[S9] ADR-0010, **Accepted**, 15 июня. Blob `2f94ebaea9302d3f2523a32fa110ea784d6e0e58`. Same-origin auth, HttpOnly cookie, защищённые страницы, единый store, optional version только у локальных drafts. Временное открытое demo-поведение не является production-решением.
https://github.com/we-are-komanda/fortis-knowledge-base/blob/develop/03_Architecture/ADR-0010-frontend-backend-auth-project-boundary.md

[S10] «Спецификация 01: каталог средств и ТТХ», **предложена** 13 июля. Blob `1901969e08b6c1067834ef214de5a3dfc474f0cd`. Источники данных, различие template/instance, документы, lossless round-trip.
https://github.com/we-are-komanda/fortis-knowledge-base/blob/develop/01_Requirements/Спецификация_01_Каталог_средств_и_ТТХ.md

## Код, повторно прочитанный при подготовке

GitHub вернул head frontend/develop `7ae48358d10df796d6c5bc95e6b16791c9688ad9`, commit от 30 июля 2026 года. Это подтверждает ветку, **но не подтверждает сегодняшний deployment**.

[C1] `project-workspace-page.tsx`, строки 42–115: `scoped.length > 0 ? scoped : variants`; создание и сравнение уже есть.
https://github.com/we-are-komanda/fortis-front/blob/7ae48358d10df796d6c5bc95e6b16791c9688ad9/src/modules/workspace/ui/project-workspace-page.tsx

[C2] `src/app/api/defense/facilities/route.ts`, прочитан полностью: mock fallback при пустом upstream и 401/404.
https://github.com/we-are-komanda/fortis-front/blob/7ae48358d10df796d6c5bc95e6b16791c9688ad9/src/app/api/defense/facilities/route.ts

[C3] `calculator-page.tsx`, строки 280–418: локальные objectLines/estimate, серверный backendCost, fallback для total; серверные запросы зависят от projectId/source/version. Это основание теста на mixed-version rendering, а не доказательство воспроизведённого runtime-сбоя.
https://github.com/we-are-komanda/fortis-front/blob/7ae48358d10df796d6c5bc95e6b16791c9688ad9/src/modules/defense-calculator/ui/calculator-page.tsx

Остальные исходные пути в спеках взяты из прошлого аудита и контекста. FRC-00 проверяет их существование и актуальность до кодирования. Новые имена файлов/эндпоинтов ниже — предложения пакета, не утверждения об уже существующих API.

## Внешние инженерные основания

[E1] Next.js, Authentication: Proxy не заменяет проверки доступа рядом с источником данных. Проверено через официальную документацию при подготовке.
https://nextjs.org/docs/app/guides/authentication

[E2] OWASP API1:2023 Broken Object Level Authorization: проверка разрешения на конкретный ресурс для каждого API, принимающего его ID.
https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/

Эти источники используются только для общих требований безопасности ПО. Они не являются подтверждением конкретной уязвимости Fortis.
