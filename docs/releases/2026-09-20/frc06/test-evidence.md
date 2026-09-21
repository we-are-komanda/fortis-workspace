# FRC-06 — evidence, 2026-09-21

**Status: PASS — локальная staged acceptance FRC-06.** 30/30 пользовательских критериев PASS; SAVE-09 staged N/A до FRC-10. Production acceptance не заявляется.

Старт: parent `6bf246e26c1f792379ed6371ea669977294e7e38`, frontend `045db0db73d2595bf36c06d792bb79f4119ad97e`, backend `5ddc2ce58e5159a96069efabb2fa3250e02666cf`, knowledge-base `03b00208e4ff2b19cbee467db094aff6af328da6`. Все четыре `develop` были clean и origin-synchronized; оба опубликованных checkpoint commit входят в историю. История не переписана.

| Проверка | Результат | Evidence |
|---|---|---|
| FRC-06 state/storage/save regressions | 48/48 PASS | [log](verification-logs/focused-root-48.log) |
| Настоящий Chromium, rendered production components, controlled transport | 13/13 PASS | [log](verification-logs/browser-navigation-13.log), `frontend/src/modules/drone-defense/ui/project-recovery.browser.test.ts` |
| Browser → Next → Go → PostgreSQL | PASS: save v2, reload; map/calculator dirty preservation; explicit recovery save v3; concurrent v4/409; independent copy v1; hard reload same new ID/content | [result](browser-live/result.json), [environment and screenshots](browser-live/README.md) |
| Go suite / build / real PostgreSQL project/security regressions | PASS | `verification-logs/backend-live-*`, [environment](browser-live/README.md) |
| FRC-01/02/04 scoped frontend group | 38 PASS, 1 explicit PostgreSQL opt-in skip | [log](verification-logs/regression-stable.log); actual PostgreSQL path separately executed above |
| Финальная full frontend suite | 250 tests: 201 PASS, 6 historical FAIL, 43 opt-in SKIP; новых failures нет | [log](verification-logs/full-suite-stable.log), [signatures](verification-logs/baseline-signatures-final.json) |
| Typecheck / lint 21 changed JS/TS files / production build | PASS, exit 0; 454 source hashes test/build совпадают, workspace drift=[] | [verification log index](verification-logs/README.md) |
| Independent review | 7 defects closed independently; URL effect separately checked; 8/8 probes PASS | [review](independent-review.md) |

## Воспроизводимые команды

Из `frontend/`:

```sh
rtk proxy node --import tsx --test src/modules/drone-defense/domain/project-save.release.test.ts src/shared/lib/project-save-state.test.ts src/shared/lib/project-draft-storage.test.ts
rtk proxy env FRC06_BROWSER_TESTS=true node --import tsx --test src/modules/drone-defense/ui/project-recovery.browser.test.ts
rtk proxy env FRC06_BROWSER_BASE_URL=http://127.0.0.1:3111 FRC06_BROWSER_OUTPUT=/private/tmp/frc06-live node test/playwright/frc06-live.cjs
```

Точные команды full suite/build/backend, окружение и exit codes сохранены рядом с логами; live harness использует disposable fixture `/__fixture`, а не пользовательскую local DB. Next 16.2.11 фактически установлен, при manifest 16.2.5; согласованный exact pin и повторная проверка обязательны до FRC-13. Node 26.4.0, PostgreSQL 16, Go 1.26.0.

## Browser scope

13 component-browser cases покрывают Stay/Discard и Save с failure/retry для variant/enterprise/logout, pending save, frozen create key/body после позднего edit, conflict reload confirmation, revoked recovery/transition, reload explicit restore и session recheck без потери диалога. Accessible roles/names и scoped variant rows, без выбора по случайному DOM order. Управляемый transport нужен для воспроизводимых потерь ответа и задержек; real stack проверен отдельно.

Live save использует фокус и Enter: Next development overlay перекрывает нижнюю кнопку при прокрутке. Нет force-click/product UI обхода. Зафиксированы ожидаемый HTTP409 и runtime предупреждения; новых page errors/duplicate deck IDs в этом canonical сценарии нет. Отдельный известный synthetic duplicate layer-code дефект остаётся gate до FRC-13.

## Исторические failures и ограничения

Шесть исходных frontend assertions: catalog sidebar motion, map zoom controls, prototype 3D placeholder, retrospective navigation, GIS copy, recommendation/compatibility seed copy. Сравниваются полные exception/assertion/stack signatures с `frc02/pre-frc02-failure-signatures.txt`, нормализуется только абсолютный checkout root. Новые failures не приравниваются к baseline. Полный suite не называется green.

SAVE-09 official-report flow staged N/A, capability disabled до FRC-10; mandatory повторная проверка при включении. Production evidence отсутствует и остаётся FRC-14 gate.
