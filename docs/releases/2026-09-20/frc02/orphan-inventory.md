# FRC-02 — ownership inventory и production gate

## Policy

| Stored state | Ordinary authenticated user |
|---|---|
| Project `enterprise_id IS NULL` или отсутствующий enterprise | 404 |
| Private asset `enterprise_id IS NULL` или отсутствующий enterprise | 404 |
| Document с отсутствующим asset или orphan private parent | 404 |
| Public asset с NULL enterprise / его documents | Read allowed; mutation 403 |

В текущей schema есть nullable ownership. Существующие FK могут предотвратить missing references или каскадно удалить документы, но NULL ownership остаётся допустимым состоянием хранения. Application fail closed не зависит от будущей constraint migration.

## Команда

Из parent, с отдельно предоставленным доступом к **выбранной** БД:

```bash
psql "$FORTIS_INVENTORY_DSN" -v ON_ERROR_STOP=1 \
  -f docs/releases/2026-09-20/frc02/orphan-inventory.sql
```

[SQL](orphan-inventory.sql) выполняет только SELECT в READ ONLY transaction. Он выводит IDs и причину, не возвращает project JSON, document URL/storage key или персональные данные. Connection string не записывается в artifacts.

## Доказательства этой реализации

- Memory HTTP tests: orphan project; orphan private asset; document с private orphan parent; document после удаления parent; foreign/missing одинаковый public response.
- Local PostgreSQL: реальные migrations `000001…000010` в отдельной тестовой схеме; SQL выставляет NULL ownership project/private asset, после чего прежний owner получает 404; public NULL asset/document остаются читаемыми.
- Local browser использует отдельную synthetic schema с rollback. Это не inventory пользовательской БД.
- **Production inventory не выполнен.** Target deployment/database, реальные applied migrations и фактическое число legacy/orphan records неизвестны. Production acceptance остаётся blocked.

## До production

1. Выбрать deployment/DB и подтвердить applied migrations/backup policy.
2. Выполнить inventory уполномоченным оператором; сохранить результаты в контролируемом месте.
3. Для каждого finding установить законного владельца или решение об архивировании/удалении. Нельзя выбирать первого enterprise или текущего пользователя автоматически.
4. Выполнить только отдельно согласованный cleanup; повторить inventory и two-user isolation checks на candidate deployment.
5. Если требуется запрет NULL на уровне БД, спроектировать constraint после cleanup с учётом public assets. В FRC-02 новая migration не создавалась и не применялась.

## Provisioning

Ordinary JWT больше не создаёт enterprise и memberships и не изменяет public catalog. В checkout нет отдельного operator-role API. Доверенное provisioning через repository/DB остаётся административным процессом вне browser flow; до реального onboarding нужен назначенный оператор и согласованный порядок действий. Test fixtures не являются production admin API.
