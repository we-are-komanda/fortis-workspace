# SCN-01 — локальная поставка учебных сценариев

Дата: 2026-10-18. Scope: SCN-01, отдельно от FRC. Не опубликовано и не развёрнуто.

## Визуальное исправление по исходному макету

После прямого замечания пользователя первая упрощённая визуализация отклонена. Источник сравнения — `fortis-scenario-mockups.html`, а не интерпретация раннего implementation review. [Исходный вид](evidence/reference-original-1440.png), [исправленная подготовка](evidence/preparation-1440.png), [исправленное сравнение](evidence/comparison-1440.png).

Перестроен рендер сцены: непрерывная светло-зелёная земля с деформированной сеткой поверхности и изолиниями, нерегулярный лес из округлых крон, плавная сквозная река и оконтуренные дороги, увеличенное предприятие с шестью объёмными корпусами, отдельной кровлей с швами, четырьмя резервуарами, периметром и проездами. Исправлены цветовой tone mapping и порядок сброса/масштабирования камеры. Подготовка показывает одну активную и две приглушённые траектории; детали подготовки/событий плавают над картой, шкала расположена под ней. В сравнении сохранена отдельная правая колонка.

[PRODUCT](PRODUCT.md) фиксирует исходный визуальный ориентир. Независимый новый review признал детализацию предприятия соответствующей схематическому уровню макета и потребовал исправить замкнутую воду, регулярность леса и перекрытие контролов в fallback. Эти исправления применены; [verdict pass](evidence/visual-verdict-pass.md): **ship**, все четыре перечисленных finding resolved. Этот verdict оценивает исправления, а не повторяет полный аудит поверхности. Фотореализм и покадровое совпадение всей внешней оболочки не заявляются.

## Что реализовано

Demo URL `/prototype?view=scenario-modeling` открывает подготовку, просмотр и сравнение любых двух разных записей на одной синтетической площадке радиусом 10 км. `workspace` сохраняет серверный gate. `view=3d` сохраняет legacy drilldown.

Площадка `synthetic-campus@1` содержит шесть именованных корпусов с отдельными крышами, проезды, периметр/вход, возвышенности, лес, реку и дороги. Местные координаты в метрах; воспроизводимые параметры/seed. Three.js/R3F загружается лениво, 2D SVG использует те же данные и работает без WebGL. Положение маркеров — линейная интерполяция подготовленных отсчётов, не прогноз.

Три точные версионированные ссылки на записи по 240000 мс и упражнения. Валидатор блокирует повреждённые записи/ссылки, дубликаты, невалидное время/координаты/события и неизвестный manifest; подстановки latest нет. Монотонные часы, пауза, seek, 1×/2×/4×, конец/повтор, общая шкала пары и visibility-пауза. Слои/камера/AI-статус не меняют учебное время.

Ранее открытая обычная карта остаётся скрытой и смонтированной ради точного восстановления камеры, выделения и UI. Прямой сценарный вход её не создаёт. Сценарный UI не пишет в `DefenseProject`, revisions, budget, recovery или backend. Кнопки сохранения рабочего проекта скрыты только на сценарном URL. Учебные ресурсы освобождаются при выходе.

AI-панель — только информация о следующем этапе, без генерации, отправки и сетевых вызовов. События подписаны как план упражнения; действия сотрудников и оценка готовности отсутствуют.

## Изменённые файлы

Пути относительно владельца.

**frontend:**

- `src/modules/drone-defense/ui/drone-defense-prototype.tsx` — отдельная ветка, сохранение экземпляра обычной карты, ленивые учебный UI/legacy 3D.
- `src/modules/drone-defense/ui/defense-studio-shell.tsx` — вход не меняет обычный view; сохранение проекта скрыто в учебном режиме.
- `src/modules/drone-defense/domain/scenario-playback.ts` и `.test.ts` — единственные локальные типы/валидатор/часы/интерполяция и runnable проверки.
- `src/modules/drone-defense/domain/scenario-site.ts` — геометрия/фиксированный seed и цвета записей.
- `src/modules/drone-defense/infra/data/scenario/library-v1.json`, `site-v1.json` — версии, записи, события, происхождение, геометрия.
- `src/modules/drone-defense/ui/scenario/scenario-workspace.tsx`, `scenario-map-2d.tsx`, `scenario-map-3d.tsx`, `scenario.module.css` — UI и рендеры.
- `src/modules/drone-defense/domain/prototype-3d-placeholder-contract.test.mjs` — обновлён устаревший source contract: учебный режим отдельный, legacy drilldown сохранён.
- `test/playwright/scn01-live.cjs`, `scn01-gate.cjs`, `scn01-performance.cjs` — воспроизводимая browser acceptance; gate использует временный локальный HTTPS identity stub, без реального backend/учётных данных.

**knowledge-base:** ADR-0025, концепция сценарного режима, продуктовый план, `00_Index.md` — фактическая реализация, принятый renderer, изоляция и ограничения. Прежний незакоммиченный текст сохранён; обновлены только относящиеся к SCN статусы/дополнения.

**parent:** этот отчёт, `PRODUCT.md`, `DESIGN.md`, `.impeccable/design.json`, `evidence/` и ссылка на результат в README спецификации. Сама спецификация/референсы уже присутствовали до работы. Backend и FRC-файлы не изменялись. Коммиты и изменение submodule pointers не выполнялись.

## Проверки

- Все четыре origin получены безопасным fetch. На момент начала parent/frontend/backend/knowledge-base опережали origin на 4/5/3/4 коммита, отставания не было; fast-forward не требовался. Чужая незакоммиченная работа сохранена.
- `pnpm build` — PASS, включая TypeScript и production page generation. [Лог](evidence/build.log). Финальная сборка выполнена с существующим `FORTIS_NEXT_DIST_DIR=.next-visual-build`, чтобы изолировать dev-кэш. Затем готовая сборка перемещена в стандартную `.next`, прежний генерируемый кэш сохранён в `/private/tmp`; Next-изменения `tsconfig.json` возвращены к исходному содержимому. Текущий лог относится к завершённой финальной сборке.
- Отдельный `pnpm exec tsc --noEmit` блокируется существующим незакоммиченным FRC-тестом `src/modules/defense-calculator/domain/report-projection.test.ts:14` (`projectVersion` отсутствует в текущем типе options). Файл существовал до SCN-01 и не изменялся. Диагностик SCN нет. [Лог](evidence/typecheck.log).
- Scoped ESLint новых/затронутых файлов — PASS. [Лог](evidence/changed-lint.log).
- Общий ESLint — 19 исходных ошибок CommonJS require в старых `frc05/06/09/11/12-live.cjs`, 2 warnings. Generated dev-output исключён из этого замера; после очистки временных файлов выполнен штатный `pnpm lint`. [Лог](evidence/full-lint.log). Эти файлы не менялись SCN-01.
- 42 runnable unit/regression checks: сценарный валидатор/время, project-map adapter, variants store и project-save. [Лог](evidence/unit-checks.log).
- Source contracts: отдельный scenario URL + gate, legacy 3D, отсутствие eager GLB preload, проектное размещение — PASS. [Лог](evidence/source-contracts.log).
- Механический Impeccable detector визуальной редакции: `[]` ([лог](evidence/visual-detector.json)). Старый [finish review](evidence/finish-review.md) предшествует отклонению пользователем и не подтверждает текущую визуальную готовность. Новый [полный визуальный review](evidence/visual-finish-review.md) сравнивает исходный макет и все девять required captures; runtime/performance в его scope не входят.

## Triage замечаний Stop hook

После сдачи hook указал три замечания в неизменённом `drone-defense-prototype.module.css`. Два `side-tab` — нижнее подчёркивание настоящей активной вкладки в `topbar.tsx` для двух тем, а не акцент сбоку карточки. `layout-transition` — преднамеренное раскрытие каталога обычной карты с изменением занимаемого размера; это взаимодействие явно закреплено в существующем `catalog-sidebar-motion-contract.test.mjs`. CSS и поведение сохранены. Через `hook-admin.mjs ignore-value` добавлены только file-scoped исключения этих двух правил в parent `.impeccable/config.json`, с указанными основаниями; повторный detector для файла — `[]`. Непроверенных/оставленных замечаний этой тройки нет.

## Acceptance A01–A15

| ID | Результат и evidence |
|---|---|
| A01 | PASS: реальный server workspace gate для `scenario-modeling` и `3d`, query/localStorage не включают demo; отдельный demo server открывает сцену. [gate-result](evidence/gate-result.json), [снимок](evidence/workspace-gate-1280.png). |
| A02 | PASS: 10 циклов с несохранённым synthetic project; точное равенство project reference/данных, syncStatus, businessRevision, version, selectedObjectId, камеры и localStorage. Реальные данные пользователя не использовались. |
| A03 | PASS: одна synthetic-сцена, три записи по 04:00, слои, нет погоды. [Подготовка](evidence/preparation-1440.png). |
| A04 | PASS domain checks: точные/неизвестные версии, плохие отсчёты, NaN/Infinity, дубликаты и события блокируются; валидные две записи остаются доступны. Намеренное повреждение проверено на клонах библиотеки, без production debug-флагов. |
| A05 | PASS: пауза неподвижна, rate сохраняет время, положение определяется только записью/временем. |
| A06 | PASS: seek 0/105000/240000, ended/replay/reset, обратимые события без дописывания журнала. [Просмотр](evidence/playback-1440.png). |
| A07 | PASS: А+Б, А+В, Б+В, один canvas/clock, повтор записи disabled. [Сравнение](evidence/comparison-1440.png). |
| A08 | PASS: вкладки и участники пары ставят паузу; пара сохраняет время, одиночный выбор сбрасывает; 2D/3D и слои сохраняют время/данные. |
| A09 | PASS controlled browser integration: настоящий visibility handler с `document.hidden=true`, затем возврат; время стоит, автозапуска нет. Физическое сворачивание на всех ОС не проверялось. |
| A10 | PASS: реальный `WEBGL_lose_context`, пауза и сохранность времени/записи, переход в пригодный 2D. [Ошибка](evidence/fallback-1440.png). Полное отсутствие WebGL с первого открытия также переводит в 2D автоматически: [initial fallback](evidence/initial-webgl-fallback-1280.png). |
| A11 | PASS: исходные учебные события, явный статус AI без запросов, нет метрик готовности. [AI-статус](evidence/ai-status-1440.png). |
| A12 | PASS browser: 1440×900, 1280×720, 390×844, reduced-motion, keyboard Home/End на шкале, видимый фокус, отсутствие document horizontal overflow; панели скроллятся отдельно/под картой. [1280](evidence/comparison-1280.png), [390](evidence/comparison-390.png), [390 controls](evidence/comparison-390-controls.png). |
| A13 | PASS: десять циклов, учебная сессия/visibility listener удалены; контексты и rAF ограничены указанными ниже counters, постоянные ресурсы обычной карты сохранены. Подробные counters в browser-result. |
| A14 | PASS: browser request capture не обнаружил business-write или AI-запросов; локальные чанки и штатные demo reads разрешены. |
| A15 | Build/scoped checks PASS; общие lint failures исходные и перечислены выше; обе темы осмотрены. [Тёмная тема](evidence/comparison-dark.png). |

Числа и условия browser acceptance: [browser-result.json](evidence/browser-result.json).

## Загрузка и плавность

Chromium 148.0.7778.96, macOS arm64, Apple M4, 32 ГБ RAM, viewport 1440×900. Производственная сборка на localhost. Аппаратный renderer: `ANGLE (Apple, ANGLE Metal Renderer: Apple M4, Unspecified Version)`. Отдельный видимый browser без десяти циклов восстановления в performance-петле. Часы действительно продвинулись примерно на 60000 мс; до конца каждого замера сохранялись playing/3D и document.hidden=false.

| Режим | Стенное время | Кадры rAF | Медиана | p95 | Максимум | Интервалы >50 мс |
|---|---:|---:|---:|---:|---:|---:|
| playback | 60.005 с | 3601 | 16.7 мс | 17.7 мс | 17.8 мс | 0 |
| comparison | 60.008 с | 3601 | 16.7 мс | 17.6 мс | 17.8 мс | 0 |

Это rAF-интервалы страницы, а не аппаратные GPU timestamps или гарантия на любом устройстве. [Полные данные](evidence/hardware-performance.json), [runnable script](../../frontend/test/playwright/scn01-performance.cjs). Geometry/controls при замере относятся к финальной визуальной редакции: сквозная река, нерегулярный лес и сетка поверхности включены.

Открытие до доступной кнопки старта в новом headless browser context: 1704 мс на прогретом локальном production server. Начальные Next JS/CSS/fonts: 36 ресурсов, 1,155,771 байт transfer / 1,144,971 байт encoded body. Исходные локальные JSON ассеты суммарно 11,465 байт; включены в ленивый учебный JS chunk. Отдельных mesh/textures/downloads нет. Это измерение localhost, не оценка внешнего канала и не строго холодного дискового cache.

После десяти циклов в контрольном snapshot: 36 созданных / 34 получивших событие потери контекстов, разность 2, visibility listeners 0, pending rAF 1. Это счётчики создания/loss events, включая обычную карту, временные probes и отложенную очистку R3F; не GPU heap profiler. Автоматическая граница после десяти циклов — ≤3 для разности контекстов и pending rAF, отсутствие scenario DOM и visibility listener. Учебного playback вне режима нет.

Software SwiftShader headless прогон до итоговой визуальной редакции сохранён отдельно (исторический, не текущий performance result): [software-rendering-result.json](evidence/software-rendering-result.json). Финальный короткий headless acceptance также показывает существенно более медленную работу SwiftShader (см. browser-result). Software renderer значительно медленнее аппаратного renderer (включая длинные интервалы в сравнении); не используется как доказательство 60 FPS. Для слабого/недоступного WebGL предусмотрен 2D.


## Отклонения и ограничения

- 3D реализован существующим Three/R3F, 2D — SVG общей геометрии внутри нынешней оболочки. Новый MapLibre engine/универсальный simulator не создавался. Начальный fit показывает учебный радиус, zoom даёт детальный осмотр корпусов. Визуальная редакция воспроизводит материалы и детализацию исходной схемы; внешняя оболочка приложения использует текущий Fortis UI. Фоновые дороги/река продолжаются вне учебного радиуса; отсчёты дорожек остаются внутри 10 км. Габариты условно преувеличены для читаемости, физической достоверности нет.
- Обычная карта сохраняет свой экземпляр и постоянные ресурсы вместо сериализации/пересоздания камеры. Учебная сцена очищается; фиксированный расход обычной карты указан в counters.
- A09 автоматизирован через visibility event; проверка физических мобильных устройств и разных ОС остаётся отдельной аппаратной проверкой. Узкий экран проверен эмуляцией viewport в desktop Chromium.
- Повреждённая библиотека проверяется доменными fixtures; маршрута загрузки пользовательских библиотек в SCN-01 нет.
- Состояния не сохраняются между reload. Нет реальных предприятий/ландшафта, погоды, редактора маршрутов, расчёта исходов, вероятностей, NeuralDeep, backend routes или имитации server save.

## До SCN-02

Выбрать и проверить модель Starter; согласовать provider/data policy, JSON-контракты/ошибки, серверную валидацию точных версий, ручное утверждение AI-черновика, права и изоляцию, immutable упражнения/запуски, retry/cancel/timeout/cost и лимиты. Затем отдельно реализовать серверное хранение и реальный AI. Оценка готовности относится к SCN-03 после методики и фактических действий участников.

## Повторить локально

Из `frontend/`, с установленными зависимостями и Playwright Chromium:

```sh
rtk pnpm build
rtk proxy env FORTIS_RUNTIME_MODE=demo pnpm exec next start --hostname 127.0.0.1 --port 3128
# В другом терминале; сервер остаётся локальным.
rtk proxy env SCN01_PERF_SECONDS=1 node test/playwright/scn01-live.cjs
rtk proxy node test/playwright/scn01-gate.cjs
rtk proxy node test/playwright/scn01-performance.cjs
rtk proxy node --import tsx --test src/modules/drone-defense/domain/scenario-playback.test.ts
```

`scn01-live` по умолчанию также меряет 60 секунд в headless renderer; для acceptance без повторения аппаратного замера задана 1 секунда. `scn01-performance` отдельно меряет по 60 секунд в видимом Chromium и проверяет реальное продвижение времени в 3D. Gate script временно занимает localhost:3129/3131, создаёт и удаляет собственный локальный сертификат/identity stub. Все результаты пишутся только в evidence.

## Визуальная доработка 2026-10-19

Актуальные сцена и evidence: [отчёт](evidence/2026-10-19/visual-report.md). Прежние снимки и числовые размеры в этом документе отражают предыдущую итерацию.
