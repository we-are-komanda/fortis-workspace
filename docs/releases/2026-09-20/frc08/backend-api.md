# FRC08 backend API

`GET /api/v1/projects/compare?projectIdA=A&projectVersionA=7&projectIdB=B&projectVersionB=3`

Both IDs and positive integer versions are required. Legacy `id1` and `id2` remain ID aliases only; versions remain mandatory. Conflicting aliases return 400 `validation_error`. Missing/invalid versions return 400 `version_required`; malformed UUIDs return 400.

```ts
type CompareResult = {
  enterpriseId: string;
  a: { identity: CalculationIdentity; name: string; updatedAt: string; cost: CostProjection; budget: BudgetProjection };
  b: { identity: CalculationIdentity; name: string; updatedAt: string; cost: CostProjection; budget: BudgetProjection };
  differenceMinor: string | null;
  differencePercent: string | null;
  warnings: Issue[];
};
```

`CalculationIdentity`, `CostProjection`, `BudgetProjection`, and `Issue` are the existing exact-money contracts. Each side's three identities agree. `name` is the saved configuration name, and `updatedAt` comes from that frozen project revision. Current names, budgets, and catalogue data do not replace historical values.

Both refs are authorized before financial calculation/cache materialization. Missing or inaccessible side, including revoked membership with the same JWT, returns 404 without partial comparison data. Two accessible enterprises or the identical project/version pair return 400 `incompatible_projects`. The same project at two distinct existing revisions is valid. Unsupported frozen calculator bindings return 503 `unsupported_calculation_version`, with no partial response.

Differences are B minus A in exact kopecks. If either total is unknown, both difference fields are null. Otherwise `differenceMinor` is signed decimal text. The percentage is `(B-A)*100/A`, rounded to two decimal places using exact rational arithmetic and nearest rounding with halves away from zero. A=0 yields null percentage. Rounded negative zero is normalized to `0.00`. For A 47500000/B 55000000, the result is `7500000` and `15.79`.

Cost lines and layer/type groups retain stable IDs, quantities, exact prices, selected price source, and frozen provenance. Matching never uses display names. There are no coverage, effectiveness, sufficiency, or optimization metrics in this response.

Top-level warning codes, all using the existing Issue shape:

| Code | Meaning |
|---|---|
| `incomplete_cost` | At least one side has unknown prices; affected object IDs are included. |
| `unmatched_layer_ids` | Layer ID sets differ; the client must keep distinct rows. |
| `unmatched_asset_ids` | Asset ID sets differ; matching names do not establish identity. |
| `price_provenance_missing` | At least one priced object has no recorded provenance. |
| `price_provenance_differs` | Matching assets have different sets of selected price source/provenance. |

Warning order is stable; object IDs are deduplicated and sorted. Layer/asset/provenance-set warnings use an empty objectIds list. Each side additionally retains its existing cost warnings. Provenance differences include the recorded source, date, quality, revision/checksum and recording metadata; they do not imply which source is better.

Access remains the ADR-0017 enterprise membership policy. No Viewer/viewCost role model or unpriced endpoint is introduced. The old mutable `projectA/projectB/diff` float response is replaced; clients must use the pinned contract.
