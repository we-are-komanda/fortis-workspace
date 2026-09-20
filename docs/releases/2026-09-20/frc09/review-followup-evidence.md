# FRC-05 / FRC-09 independent review follow-up evidence

Date: 2026-09-20. Agent `spec_inventory`. Code changes below were individually authorized by root after independent reproductions. No commit, push, deployment, external notification or production scanner run. User requested finishing the nearest task then stopping; this file records checks already executed. No new checks were run to write this note.

## FRC-09 review fixes

Four independent temporary probes first failed, then permanent regressions were added:

1. Actual card-save callback (`upsertAssetInLibrary` then `selectAsset`) invalidated preview by changing the project reference. Selection-only updates now rebase the valid preview; business edits still invalidate it.
2. A second pending card save discarded the first. Valid pending preview assets are now accumulated.
3. Pre-provenance bundled seed lost demo classification after project import. Shared `preserveDemoAssetSources` is reused by project import and asset API normalization; exact bundled id/legacyItemId retains demo lineage, including supplied root/field source quality. Unrelated client cards remain unknown or preserve their explicit source. This does not infer demo from all public cards.
4. An unchanged source editor silently replaced distinct card provenance with price provenance. Unchanged metadata is preserved in full; explicit source-editor changes continue to update the labelled card/price source and remove old price provenance keys.

The document-selection callback now changes unknown quality to estimated, never confirmed, so selecting a ready document cannot silently discard its source reference.

Permanent tests are in `src/shared/lib/catalog-refresh.release.test.ts`, `src/modules/drone-defense/domain/asset-library-form.release.test.ts`, `src/modules/drone-defense/infra/catalog-provenance.release.test.ts`, and `src/modules/drone-defense/ui/asset-library-manager.browser.test.ts` (frontend). Four initial review probes plus a backend-seed-lineage probe live temporarily at `/private/tmp/fortis-frc09-fe-review.test.ts`.

Fresh run after these fixes: 14 permanent checks + 5 independent probes = **19/19 PASS**; targeted ESLint and full `tsc --noEmit` PASS. Document callback/browser suite independently run by `frc02_frontend_gate`: **5/5 PASS**, including expected `quality=estimated`.

## FRC-05 additional review

- Prior-session delayed cost response probe: PASS. A response from the prior identity does not replace the new identity’s projection.
- Draft source validation was missing despite strict saved API validation. A synthetic malformed `provenance.sourceLabel` object produced React error #31 and an empty calculator. Permanent regression was RED, then GREEN after validating the selected source using `readDataProvenance` and mapping invalid metadata to `CostProjectionInputError` with object IDs. Hook guidance now includes sources.
- An actual local Next map with an intercepted synthetic project containing quantity 0 crashed at unguarded layer-summary cost derivation. Root fixed the structural summary/projection integration. The exact independent probe `/private/tmp/fortis-frc05-map-review.cjs` then passed: `errors=[]`, map remains visible with a controlled unavailable-cost/retry message. No backend project was mutated by that probe.
- Invalid unused catalog prices also crashed rendering; malformed canonical strings threw `BigInt` while opening the editor. Root authorized a narrow follow-up: existing `assetPriceLabel` now yields “Некорректная цена” on typed price errors and is reused by catalog/manager preview. The form retains a price error and blocks unchanged invalid writes until the user explicitly corrects the price. No silent zero, unknown conversion or rounding is used.

Fresh commands/results:

```sh
# frontend; executed through rtk proxy
node --import tsx --test src/shared/lib/cost-projection.test.ts src/shared/lib/cost-consumers.release.test.ts src/modules/defense-calculator/infra/cost-projection.release.test.ts
# 24/24 PASS at draft-source fix checkpoint
FRC05_BROWSER_TESTS=true node --import tsx --test src/modules/defense-calculator/ui/calculator-page.browser.test.ts
# 10/10 PASS
node --import tsx --test src/shared/lib/cost-consumers.release.test.ts src/modules/drone-defense/domain/asset-library-form.release.test.ts
# 8/8 PASS after invalid-price presentation (includes root structural-summary test)
FRC09_BROWSER_TESTS=true node --import tsx --test src/modules/drone-defense/ui/asset-library-manager.browser.test.ts
# 6/6 PASS, including explicit correction before write
pnpm exec tsc --noEmit
# latest run PASS
```

Targeted ESLint and `git diff --check` PASS. One earlier broad run found the pre-existing `defense-project.test.ts:69` expectation for compatibility labels/status; it was reported to root, not silently omitted or modified by this agent. Local HTTP fixture tests initially needed sandbox escalation for loopback binding, then passed. A transient full TypeScript run failed on the concurrently unfinished FRC-06 draft-storage module; the later full run passed.

Browser tests used synthetic fixtures. Root owns the actual FRC-09 Next → Go → PostgreSQL/private-file pipeline run and final acceptance; this agent did not duplicate that active run. Synthetic scanner success is not real antivirus or production storage evidence. Runtime gates from FRC-09 backend evidence remain unchanged.
