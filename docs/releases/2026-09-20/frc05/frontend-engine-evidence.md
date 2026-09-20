# FRC-05 frontend exact cost engine — 2026-09-20

Scope: pure financial projection and focused verification after the root accepted the FRC-04 code gate. No store, API, route, UI, backend, catalog, migration or knowledge-base changes in this subtask. Root owns shared financial/project types, integration, the final source suite and release acceptance. No commit, push, deployment or external service call.

## Observed defect before implementation

Mapped the unchanged synthetic `finance-v1` fixture onto the actual `DefenseProject` shape and called the existing helpers with `rtk proxy node --import tsx -`:

- Variant A expected `47500000` minor; `calculateProjectTotalCost` returned `0.5` Mln, its layer totals were `0.3`/`0.2` Mln, and `estimateConfiguration` returned `0.6` Mln.
- Existing report lines returned `0.25`, `0.15000000000000002`, `0.075` Mln.
- A null template price became unit price `0` and total `0`.

The fixture copy at `frontend/test/fixtures/finance-v1.json` matches the release source byte-for-byte: SHA-256 `4d40df5ac6ed06b96e493876bac0de43cf9ba6d325bedd05c02670779a691920`.

## Owned files and public interface

- `frontend/src/shared/lib/cost-projection.ts`
- `frontend/src/shared/lib/cost-projection.test.ts`
- `frontend/src/modules/defense-calculator/ui/calculator-page.browser.test.ts` (later root delegation: real component/store integration tests only)

```ts
buildDraftCostProjection(project: DefenseProject): DraftCostProjection
legacyMlnToMinor(value: string | number): string
formatMinorRub(minor: string | null): string
getAssetUnitPriceMinor(asset: DefenseAsset): string | null
CostProjectionInputError // issues: {code, field, objectIds, message}[]
```

The engine belongs in shared because both GIS and calculator consumers need it, and shared compatibility helpers must not import a module. It uses native BigInt, no dependency or new store. Returned financial values are decimal strings. A draft has `kind: "draft"` and a server `basedOn` reference only for a backend project with a valid version; it never fabricates a calculation identity or snapshot digest.

Price precedence is explicit instance override (including zero or null), explicit asset `pricingMode: "components"`, then bundle/template price. Missing canonical minor fields allow legacy conversion; explicit null stops fallback. Components are only the typed accounting `asset.components` rows, never inferred from a descriptive compound profile, personnel or geometry. Empty/absent components and incomplete bundles remain unknown. Quantity is applied once after unit-price rounding. Every selected quantity is an integer 1–1,000,000; unit prices and component bundle unit totals are 0–10^15 minor units. Existing assets must use RUB even when an override is selected.

The engine includes every actual placement regardless of visibility/activity, groups by real layer IDs and category in first-placement order, and preserves missing-reference rows with warnings. A missing template with an explicit RUB override retains that known price and a `missing_asset` warning; without an override the price is unknown. Unknown lines produce null totals, separate known subtotals and object IDs. An empty project has no financial rows/groups and a complete zero total. Provenance follows the selected price field.

Frontend/backend implementations agreed on warning codes `legacy_price_converted`, `legacy_price_rounded`, `missing_asset`, `missing_layer`, `missing_components`, `missing_price`; errors include `invalid_price`, `invalid_quantity`, `invalid_currency`, `invalid_pricing_mode`. Field paths identify the placed object, asset or component index. Ignored price branches are not validated or added to the total.

## TDD and verification

Initial behavioral RED: 14 failures / 1 pass against a minimal empty-projection scaffold; the fixture specifically failed with `0 != 47500000`. GREEN followed exact projection implementation. One test expectation typo was corrected after reading fixture B: 3+2+1 is six units. A later malformed legacy `[1]` input reproduced an unwanted JavaScript string coercion (16 pass / 1 fail); rejecting non-string/non-number input made all 17 pass.

| Command (from frontend unless noted) | Actual result |
|---|---|
| `rtk proxy node --import tsx --test src/shared/lib/cost-projection.test.ts` | Final 19/19 PASS |
| `rtk proxy pnpm exec eslint src/shared/lib/cost-projection.ts src/shared/lib/cost-projection.test.ts` | Exit 0 |
| `rtk proxy python3 /private/tmp/frc05-decimal-review.py` | 507 deterministic cases matched independent Python Decimal `ROUND_HALF_UP`, including scientific notation, near-half boundaries and out-of-range values |
| `rtk proxy shasum -a 256 test/fixtures/finance-v1.json ../docs/fortis-release-specs/fixtures/finance-v1.json` | Identical SHA-256 above |
| `rtk proxy git diff --check` | Exit 0 at check time |
| `rtk proxy pnpm exec tsc --noEmit --incremental false` | Concurrent integration snapshot failed only in old consumers: calculator-page.tsx lines 106/110 (old cost call/state), backend-integration-contract.test.ts line 35 (old cost call). No engine/test type errors. Root is updating these consumers and owns final typecheck. |

Tests cover fixture A/B and components, exact row/group reconciliation, hidden/inactive/maintenance, custom/renamed/missing layers, zero/null override, incomplete/empty totals, missing templates, selected provenance, explicit pricing mode, invalid quantity/price/currency, half-up once per unit, large sums beyond Number.MAX_SAFE_INTEGER, exact formatting and input immutability.

## Limits and integration handoff

This verifies the pure engine, not the saved-versus-draft UI, response ordering, API transport or real-backend browser flow. Root must wire every financial consumer to one whole projection and remove legacy floats from the release UI. Compatibility outputs may be derived from this engine only. Capability publication remains gated by the relevant FRC acceptance.

An already-parsed legacy JavaScript number cannot recover the original JSON decimal lexeme. The adapter converts its available decimal spelling and emits `legacy_price_converted`; discarded nonzero fractional minor units also emit `legacy_price_rounded`. The exported string helper preserves an available original decimal spelling exactly. Canonical minor strings are authoritative for new financial inputs; no claim of recovered legacy precision is made.

## Integration review and browser evidence

The root later delegated independent consumer review and the browser test file above. Two concrete defects were reproduced and fixed by the root: the map object list still used a legacy catalogue alias/capex (canonical zero override produced a displayed 250,000 RUB), and the cost API validator accepted an object-valued provenance sourceLabel that React could not render. Permanent browser checks now verify canonical map zero/unknown amounts and malformed provenance rejection.

The saved map initially still displayed local calculations. An exact example (`4.999999999999999999999e-9` Mln) converts to zero from its original spelling but to one minor unit after JavaScript numeric parsing. Root extracted `domain/use-project-cost.ts` and reused it for calculator/map: saved amounts come from one pinned server projection; dirty amounts come from one complete local projection. Independent hook review checked the session-generation/project/version key, cancellation and current-result selection. Browser checks were rerun after extraction.

`rtk proxy env FRC05_BROWSER_TESTS=true node --import tsx --test src/modules/defense-calculator/ui/calculator-page.browser.test.ts`: **9/9 PASS**. The real CalculatorPage, RuntimeProvider, Zustand project store and financial engine are bundled with installed esbuild and run in Chromium; only Next Link, CSS and transport/runtime responses are test adaptations. Scenarios: late version and project responses; all-server rows/total switching to all-draft; unknown versus explicit zero; empty project; saved 503 without local fallback and manual retry; escaped names/source labels; malformed provenance; actual EchelonObjectsList canonical values. No Next dev/build server or external network is used. The initial sandbox Chromium Mach-port denial required an approved execution retry. The test-only CSS loader was corrected to include `.module.css`; that build-harness failure is not counted as a product regression.

Final scoped ESLint covering all three owned code/test files and full `tsc --noEmit --incremental false` returned exit 0 after root integration, superseding the intermediate consumer type failures above. Full application/source-suite acceptance remains owned by root.

## Independent backend parity

The backend agent emitted actual isolated-PostgreSQL/runtime artifacts `/private/tmp/frc05-project.json` and `/private/tmp/frc05-projection.json`. The frontend engine output deep-equals all server financial fields (identity versus draft metadata excluded): total `47500000`, three lines, two real layers, with matching groups, names and warnings.

A temporary Go overlay under `/private/tmp/frc05-parity-review` ran ten additional synthetic cases through the independently implemented backend document parser and DTO mapper. The frontend closed three reproduced differences using RED→GREEN tests: quoted legacy numeric fields now reject rather than coerce; blank optional object names fall back to the template; unknown empty-component prices retain their stated provenance. Final pure suite is 19/19. Two backend parser differences were handed to its owner with the exact corpus: null pricingMode was silently treated as bundle, and malformed ignored components were decoded before an overriding instance price. After that owner added RED→GREEN fixes, the independent overlay was rerun and fresh frontend expectations recomputed: **10/10 parity PASS**, including all amounts, lines, groups, provenance and validation code/field. Warning message wording was excluded from this secondary comparison; codes, severity and object IDs were compared. No remaining reproduced parity finding in this bounded corpus.
