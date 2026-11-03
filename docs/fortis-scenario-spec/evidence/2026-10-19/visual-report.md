# Карта и 3D: сверка с исходным макетом — 2026-10-19

Эталон: `fortis-scenario-mockups.html`, не упрощённая предыдущая сцена. Принятые правки: ортографическая архитектурная проекция, пять корпусов с исходными пропорциями/разной высотой, светлая кровля со швами и тонкими кромками, четыре резервуара, исходные двор и проезды, позиции лесных крон, контуры холмов, сквозные река и дороги. Данные общие для 2D и 3D; настоящие объёмы можно вращать. Заново проверены высоты трёх подготовленных записей над обновлённым рельефом и крышами.

Итоговый стартовый кадр: [1440×900](preparation-final-1440.png). Другие снимки в этой папке: просмотр, сравнение 1440/1280/390, тёмная тема, 2D fallback, AI-status. Это реализация в существующей оболочке Fortis, а не копия HTML-оболочки макета. Рабочая GIS-карта не подменяется сценарием; preview остаётся в demo.

## Проверки

- 6 unit-проверок библиотеки, времени, геометрии/просвета — PASS.
- ESLint renderer/domain — PASS; production build — PASS; design detector — без находок.
- Chromium 148, macOS arm64 / Apple M4 / 32 GiB; desktop 1440×900/1280, mobile viewport 390: проверены pair selection, seek/pause/speed/end, background pause event, context loss и initial fallback, восстановление карты и очистка listeners/frames. Ошибок страницы нет; business writes/AI requests нет. Подробности: `browser-result.json`.
- Холодное открытие dev-сборки: 1888 мс. Headless использовал SwiftShader: медиана кадра 33.4 мс / 17.6 мс, p95 около 300/283 мс; это программный renderer и не замер аппаратной плавности.
- Отдельный hardware run: ANGLE Metal / Apple M4, около 60 кадров/с; медиана 16.7 мс в обоих режимах, p95 17.5/17.3 мс, кадров дольше 50 мс нет. `hardware-performance.json`: по 15 секунд просмотра/сравнения. Не тест физического мобильного устройства.
- Полный standalone tsc имеет прежнюю ошибку пользовательского `report-projection.test.ts:14`; production build проходит. Старые global lint проблемы не менялись.

## Изменённые файлы этой доработки

- `frontend/src/modules/drone-defense/ui/scenario/scenario-map-3d.tsx`
- `frontend/src/modules/drone-defense/ui/scenario/scenario-map-2d.tsx`
- `frontend/src/modules/drone-defense/domain/scenario-site.ts`
- `frontend/src/modules/drone-defense/domain/scenario-playback.test.ts`
- `frontend/src/modules/drone-defense/infra/data/scenario/site-v1.json`
- `frontend/src/modules/drone-defense/infra/data/scenario/library-v1.json`
- `DESIGN.md`, данный evidence и `ADR-0025-synthetic-scenario-playback.md`.

AI-генерация, погода, физическая модель, реальные предприятия и готовность сотрудников не добавлялись. Публикации не было. Это дальнейшая визуальная редакция ещё не опубликованного v1; сохранённые рабочие проекты не изменялись.


## Основное приложение — последующее изменение 2026-10-19

По запросу пользователя учебная карта теперь доступна в workspace runtime: `/`, `/workspace`, `/prototype` без проекта открывают её напрямую. Прежние указания demo-only выше описывают состояние до этого запроса. Снимок: [основное приложение на 3000](main-app-3000.png).

Проверка `node test/playwright/scn01-gate.cjs` прошла на localhost:3000: четыре входа, видимый WebGL canvas, отсутствие выбора предприятия, отсутствие ошибок страницы и записей API. Девять unit/контрактных тестов и targeted ESLint прошли. Исправлена ошибка dev CSS: временный `.next-scn-visual/` добавлен в gitignore, чтобы Tailwind не сканировал сгенерированный preview.
