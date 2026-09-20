# FRC06 — investigation / gap matrix

2026-09-20. Эта таблица фиксирует исходный код до реализации FRC06, не PASS приёмку.

| Scenario | Уже есть | Конкретный пробел / минимальное действие |
|---|---|---|
| SAVE01 | Общий Zustand; shouldLoadBackendProject не перезагружает тот же dirty project | Проверить real navigation и expose одинаковый draft/status; убрать автоматическую неподтверждённую recovery hydration |
| SAVE02 | Поздний edit сохраняется по `latest !== project` | Ref equality путает UI selection с business edit; добавить counter/baseline и request identity |
| SAVE03 | Backend immutable revisions и create idempotency | После503 только PUT, GET отсутствует; повторcreate новыйkey; даже одинаковыйkey сериализует новый updatedAt. Freeze attempt и verification-first |
| SAVE04 |409 оставляет draft, conflictState | Reload button вызывает load без потери-confirmation; cached list может заменить server version; requestId теряется в stringerror |
| SAVE05 | Save-as-new существует | Удержать key/body ручногоretry; не закрывать/очищатьUI наerror; не менять старый serverproject |
| SAVE06 | Corrupt JSON catch возвращаетnull | getItem/SecurityError иsetItem/quota не catch; persist вызывается ДОset, поэтому edit теряется. Отдельный typed storage result +memoryfirst |
| SAVE07 | Selection напрямую не ставитdirty; тема/panel внеproject | Во время save selectAsset меняет reference→ложныйdirty; бизнесcounter обязателен |
| SAVE08 | user-only scoped key; identity reset; старый общий key не читаетсяworkspace | Нужен user+enterprise+project namespace, explicit/access-verified recovery, shared-device disablepolicy |
| SAVE09 | FRC05 whole saved/draft projections; report capability gated | Дать reusable saved-ref intent/guard, actualreport остаётся FRC10 |
| SAVE10 |401 reset;403/404 accessError блокируетповторsave; staleidentityresponses dropped | Сохранить этиграницы приrecovery/transition; не доверятьlocalStorage владению; не выводить recovery доaccesscheck |

## Reproduction evidence (read-only source)

Temporary probe `/private/tmp/frc06-investigation.ts`, command fromfrontend:

`rtk proxy node --import tsx /private/tmp/frc06-investigation.ts`

Eight observed outcomes:

1. QuotaExceededError on replaceProject: throws=true, name remains `before`, attempted `edited` is not installed in memory.
2. Ambiguous update503: only `PUT:/api/defense/projects/P`; no verification GET.
3. UI-only selectAsset during pending PUT: responsev8, syncStatus=`dirty`.
4. Cached listv7 + currentGET `{name:server-v8,version:8}`: resultingname=`server-v8`, version=`7`.
5. Two manual same-body create retries: two different idempotency keys.
6. Caller-supplied samekey/sameproject twice: body differs due fresh export updatedAt.
7. localStorage.getItem SecurityError escapes restore.
8. Corrupt JSON restore marks hydrated=true, exposes no recoveryerror.

Source points: project store `projectStorageKey:131`, `persist:138`, `readProject:144`, `applyProject:208`, selection411/437/445, restore587; variants store pending100/129 and cachedversion165; API `projectUpdatePayload:88`; export timestamp `defense-project.ts:1313`; variants modal directreload59 and `.then(onClose)`74; workspace create64/open83; identity boundary logout66.

Existing reuse regression:

`rtk proxy node --import tsx --test src/shared/lib/identity-isolation.release.test.ts src/modules/drone-defense/domain/use-defense-variants-store.test.ts`

**11/11 reported node tests PASS**, including five late-access subcases and one variants script with seven inline scenarios. This establishes existing identity/409 behavior only; it does not prove missing FRC06 criteria.

Read: FRC06 spec, shared contracts/types, KB index/current roadmap and ADR0010/0017/0018; owning save/storage/session/workspace/variant UI/current cost flow. Parent synchronised all repos before distributed work. Concurrent working tree intentionally not reset.
