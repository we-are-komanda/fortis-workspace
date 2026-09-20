# FRC-05 backend plan and implementation decisions

Coordinator granted GO after FRC-04 CODE PASS / RUNTIME BLOCKED. The bounded backend slice below is implemented and independently reviewable; final release acceptance remains with root. Runtime/production acceptance is not inferred from local tests.

## Investigation

The existing budget service iterates actual placed objects and actual layer IDs, so that loop/grouping can be retained. However, it computes float64 values in millions, rounds to two decimal places in millions, omits zero/unknown-price lines, and replaces invalid quantities with one. Existing frontend costing also has independent arithmetic. Actual runtime data has `asset.pricePerUnitMln`, optional `object.customPricePerUnitMln` and descriptive compoundProfile equipment/weapon fields. It has no explicit component-price contract yet. The finance-v1 fixture is intentionally a normalized accounting fixture, not a complete DefenseProject.

The FRC-04 authoritative source is `DefenseProjectService.GetRevision`: it reauthorizes the current project and returns the exact immutable raw project, revision envelope and digest. Cost must read this source, never the mutable global asset catalogue and never the typed float64 reconstruction when parsing money.

## Agreed additive money inputs

The coordinator agreed these names with the frontend owner:

```ts
type PriceComponent = {
  id?: string;
  name: string;
  quantity: number;
  unitPriceMinor: string | null;
};
type AssetPriceFields = {
  unitPriceMinor?: string | null;
  pricingMode?: "bundle" | "components";
  components?: PriceComponent[];
};
type ObjectPriceFields = { customPriceMinor?: string | null };
```

`assetLibrary[]` owns AssetPriceFields; `placedObjects[]` owns ObjectPriceFields. Currency remains the existing RUB field. Absent minor field falls back to its corresponding legacy `*Mln` field. A present null explicitly means an unknown price and must not silently pick a legacy value. Presence checks must distinguish absent, null and zero. Instance override takes precedence over explicit components mode; components replace bundle price, not add to it. CompoundProfile equipment/personnel/coverage data alone never implies a price, recurrence or component line. The FRC-09 owner handles global asset persistence/DTO fields; FRC-05 consumes the raw frozen project fields only and will not edit defense_asset.

The pure domain engine uses integer minor units (`math/big.Int`) and a normalized input, not float64. The raw JSON adapter uses RawMessage so the original legacy decimal spelling is retained. The implemented parser shifts decimal digits by eight and rounds half-up once per unit, avoiding a huge exponent allocation; exact rational parsing is used for integer quantity validation. Quantity is an integer 1..1,000,000. Each resolved unit price is 0..10^15 minor; totals are arbitrary-precision integers, persisted NUMERIC and exposed as decimal strings. Selected legacy prices emit a conversion warning and rounded values a separate rounding warning. Invalid values produce a field error, never a partial numeric success.

Unknown referenced assets emit a warning and retain a line; an explicit instance override can still price the line because the minor-unit contract is RUB. Without that override, missing asset/price/component data produces explicit incompleteness. A missing layer retains its actual layer ID and emits an issue. Hidden/inactive/maintenance objects stay included. Empty placedObjects produces empty arrays and complete zero totals. Component mode without components produces unknown, not a free bundle. These edge cases are aligned with frontend tests. PricingMode/components are parsed only in the selected branch, so malformed ignored component data cannot defeat an override; a selected null mode is invalid.

## Public API proposal

Keep GET `/api/v1/projects/cost`. Add canonical query `projectId` and positive `projectVersion`; retain existing `id` as an explicit compatibility alias, rejecting conflicting aliases. The release client supplies version. Compatibility requests without version may resolve the current authorized revision once and return its exact identity; they may never combine a current summary with historical lines.

The response is the exact shared CostProjection shape, with identity at the top-level field `identity`:

```ts
type CalculationIdentity = {
  projectId: string;
  projectVersion: number;
  calculationVersion: string;
  inputDataVersions: Record<string, string>;
  snapshotDigest: string;
};
type FinancialLine = {
  objectId: string; assetId: string; layerId: string;
  category: string; name: string; quantity: number;
  unitPriceMinor: string | null; lineTotalMinor: string | null;
  priceSource: "instance_override" | "components" | "template" | "unknown";
  provenance: DataProvenance | null;
};
type CostGroup = {
  id: string; name: string; objectCount: number; unitCount: number;
  knownSubtotalMinor: string; totalMinor: string | null;
};
type CostProjection = {
  identity: CalculationIdentity; currency: "RUB";
  lines: FinancialLine[]; byLayer: CostGroup[]; byType: CostGroup[];
  knownSubtotalMinor: string; totalMinor: string | null;
  isComplete: boolean; unknownPriceObjectIds: string[]; warnings: Issue[];
};
```

Issue and DataProvenance use the existing shared contract. No provenance is fabricated for old data. Object/layer order is stable (placed-object order and first encountered group order), grouping uses real layerId/category. Known subtotal sums known lines. Any unknown line makes its group and overall total null; zero remains a known price. The HTTP endpoint returns CostProjection only. Existing internal CalculateCost callers receive compatibility values derived from this same projection; the old independent float calculator/grouping was deleted. Internal callers that cannot represent an incomplete total receive ErrIncompleteCost until their owning report/budget adaptation.

Proposed new application entrypoint:

`BudgetService.ProjectCost(ctx, actorID, projectID string, projectVersion *int) (*domain.CostProjection, error)`

It authorizes via GetRevision before both cache reads and calculation. Domain errors map to existing authorization codes, 404 revision_not_found, 400 invalid_price/invalid_quantity with field information, and explicit unsupported_calculation_version if no frozen calculator is available. Never use a newer algorithm as fallback. Root owns cross-module API/DI coordination; an added cost repository port must be registered through the existing budget repository/DI pattern, with the exact constructor change sent before editing shared dependencies.

## Smallest correct historical persistence

Propose two small owning storage additions, without changing project snapshot contents/digests:

1. Add a `cost_calculation_version` binding to each immutable project revision, initially `cost-rub-v1`. A migration assigns the known first algorithm to existing current/backfilled revisions without inventing earlier calculations. New revisions persist the binding explicitly. The revision UPDATE guard protects this field too. Future algorithm changes keep the v1 function available for old bindings and bind v2 only to new or explicitly recalculated versions.
2. Add append-only `project_cost_projections` keyed by `(project_id, project_version, calculation_version)`, referencing the actual revision. Store projection JSONB and exact known/nullable total NUMERIC columns. Materialize on first cost request with ON CONFLICT DO NOTHING then read the committed winner. This stores the authoritative issued result and handles duplicate concurrent reads without recomputing it later. Delete follows project/revision cascade and current access is always required.

This avoids invoking a budget application service from inside project infrastructure. A mutable global calculationVersion constant by itself is insufficient: an old revision that has not been read yet would silently select a newer algorithm. A cache alone keyed only by the currently deployed calculationVersion has the same flaw. Frozen per-revision binding plus immutable result storage covers both previously issued and as-yet uncalculated historical revisions. FRC-07 can use the same pure calculator for preflight/save validation and optionally materialize the result in the save transaction; that later financial gate is not implemented here.

## Planned RED/GREEN evidence

1. Copy finance-v1 bytes into owning backend testdata; parse it into normalized input and independently assert both variants, groups, compound fixture, zero override, missing price, decimal conversion and half-up.
2. Add runtime-document tests using actual DefenseProject shape, custom IDs, null vs zero vs absent, descriptive compoundProfile, hidden/inactive/maintenance objects, missing asset/layer references and invalid price/quantity/currency.
3. Add real-PG API test: create revision, request cost, mutate global catalogue/current project, request old version, verify exact identity and unchanged persisted projection. Query a pre-migration version and revoked/deleted project. Verify concurrent cost requests commit one projection and tampering UPDATE fails.
4. Simulate a newer default calculator while an older revision remains bound to v1; prove both cached and previously uncalculated old revisions still use v1. Unknown binding must fail explicitly.
5. Verify compatibility totals are derived from minor units, then run focused budget/domain/UI tests, FRC-04/FRC-02 regression, Go suite/vet/build. Root coordinates the same golden fixture against the frontend and checks stale-response handling (COST-09).

No new dependency, no changes to scoring/placement/coverage methodology, and no FRC-07 budget enforcement or report redesign in this slice. No commit/push/deploy. Root registered the existing BudgetConfigRepository under both budget and projection ports for the approved NewBudgetService third constructor argument. The exact API example is captured from the actual PostgreSQL endpoint in api-example.json.
