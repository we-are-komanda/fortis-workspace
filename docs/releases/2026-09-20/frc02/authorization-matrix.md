# FRC-02 — route-by-route authorization

Все backend paths ниже имеют префикс `/api/v1`. Отсутствующая/invalid/expired identity: **401**. Foreign/missing private resource: одинаковый **404**. Storage/checker failure: **500**. `200/201` означает успешную операцию с валидным domain payload; существующие validation/version errors остаются 400/409.

| Method / route | Actor-aware application boundary | Own member / authenticated public | Foreign / orphan / forbidden |
|---|---|---|---|
| GET `/enterprises` без id | `EnterpriseService.ListByUser` → membership JOIN | Scoped list + total | Чужие отсутствуют |
| GET `/enterprises?id=E` | `Get` → `CheckUserAccess` | 200 | 404 |
| PUT `/enterprises?id=E` | `Update` → authorized `Get` | Metadata update 200 | 404 |
| POST `/enterprises` | `Create` → valid actor → closed operation | 403 | 403 без enumeration |
| DELETE `/enterprises?id=E` | `Delete` → access → operator policy | 403 | 404 |
| POST `/enterprises/members` | `AddUser` → valid actor → closed operation | 403 | 403; self-grant невозможен |
| DELETE `/enterprises/members` | `RemoveUser` → valid actor → closed operation | 403 | 403; удаление чужой связи невозможно |
| POST `/projects` | `CreateFromJSON` → authorized target enterprise | 200 | 404, ownership server-approved |
| GET `/projects?enterpriseId=E` | `ListProjects` → access → scoped repository | Scoped list + total | 404 |
| GET `/projects` без enterpriseId | `ListProjects` → `FindAllByUserID` | Все доступные enterprise, scoped pagination | Чужие/NULL отсутствуют |
| GET `/projects/get?id=P` | `GetProject` → stored enterprise → access | 200 | 404 |
| PUT `/projects/update?id=P` | Authorized `GetProject` → immutable ownership → version → update | 200; conflict 409 | Foreign 404; ownership change 400 |
| DELETE `/projects/delete?id=P` | `DeleteProject` → authorized `GetProject` | 200 | 404 |
| GET `/projects/export?id=P` | `Export` → authorized `GetProject` | 200 | 404 |
| POST `/projects/import` | `Import` → imported target enterprise authorization | 200, new project ID | 404; no implicit transfer |
| GET `/projects/budget?id=P` | `GetBudgetConfig` → authorized project before budget read | 200 | 404 |
| PUT `/projects/budget?id=P` | `UpdateBudgetConfig` → authorized project | 200 | 404 |
| GET `/projects/cost?id=P` | `CalculateCost` → authorized project | 200 | 404; no aggregate leak |
| POST `/projects/budget/check?id=P` | `CheckBudget` → authorized parent even for unlimited | 200 | 404 |
| GET `/projects/report?id=P` | `GetReport` → authorized parent; asset enrichment also scoped | 200 | 404; no metadata/URL leak |
| GET `/projects/compare?id1=P1&id2=P2` | `CompareConfigs` → authorize P1 and P2, then calculate | 200 when both accessible | 404 if either inaccessible; no partial result |
| GET `/assets` | `List` → actor-scoped SQL; optional enterprise checked | Own private + public, scoped total | Foreign private/NULL-private absent |
| GET `/assets/get?id=A` | `GetByID` → public or enterprise check | Own/private or public 200 | Private foreign/NULL 404 |
| POST `/assets` | `Create` → private target access; public closed | Private own 201 | Foreign/NULL 404; public 403 |
| PUT `/assets/update?id=A` | `GetForMutation` → stored parent/policy | Private own 200 | Private foreign/NULL 404; public/promotion 403 |
| DELETE `/assets/delete?id=A` | `GetForMutation` → stored parent/policy | Private own 200 | Private foreign/NULL 404; public 403 |
| GET `/assets/documents/list?assetId=A` | `ListByAssetID` → parent visibility first | Own private/public 200 | Foreign/orphan parent 404 |
| GET `/assets/documents/get?id=D` | `GetByID` → document → parent visibility | Own private/public 200 | Foreign/missing/orphan 404 |
| GET `/assets/documents/download?id=D` | `GetByID` → parent visibility before returning URL | Own private/public 200 | Foreign/missing/orphan 404, URL absent |
| POST `/assets/documents` | `Create` → parent `GetForMutation`, owner bound to actor | Own private 201 | Foreign/orphan 404; public 403 |
| DELETE `/assets/documents/delete?id=D` | `Delete` → document → parent mutation policy | Own private 200 | Foreign/orphan 404; public 403 |

## Frontend / BFF

| Route/flow | Boundary |
|---|---|
| `/workspace`, `/prototype`, `/calculator` (workspace) | Server `/auth/me` before page response + client `/api/auth/me` before mounting sensitive UI |
| `/api/defense/projects` and `/api/defense/projects/[id]` | Existing BFF → same backend authorization, preserved status and strict success JSON |
| `/api/v1/*` | Existing transparent forwarding; same target, cookie/Bearer, binary/error behavior |
| `/api/auth/login`, `/api/auth/register` | Backend identity flow; shared production cookie policy; no token returned to JS |
| `/api/auth/logout` | Cookie expiry with same flags; client clears active identity and navigates fully |
| Identity A → B | Per-user recovery, synchronous store reset, epoch guard, component remount |
| 401 / 403 / 404 after open | Identity invalidation / blocked action / unverified recovery; no demo or automatic save retries |

Auth register/login and token validation remain authentication operations, not tenant membership grants. `/_/*` probes retain FRC-01 semantics. No new role, admin UI, authorization database table or production route is introduced. The browser fixture's `__fixture/__revoke/__stop` endpoints exist only in `_test.go`, require explicit test-server opt-in and bind `127.0.0.1:8092`.
