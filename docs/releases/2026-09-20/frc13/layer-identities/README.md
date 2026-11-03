# Stable runtime layer identity — pre-FRC13 gate

Actual Next→Go→disposable PostgreSQL browser regression created two layers with distinct canonical IDs and code SAME. Before: duplicate echelon-same-zone/slots/slot-labels and child deck layers produced five initialization assertions (red/failure.json). After the one-line zone.layerId identity change in gis-board.tsx: green/result.json PASS, consoleErrors/pageErrors empty; both layers remain independently selectable with preserved stored IDs and codes. Screenshot green/map.png.

Runnable regression: frontend/test/playwright/frc13-layer-identities.cjs. It requires the owned FRC03fixture on8092/PG55434 and FRC13_SEED_PROJECT; creates synthetic data only. Root verified the database prefix/loopback before writing. User DB5432 is never used.

An initial GREEN attempt hit a30second dev-navigation/hydration timeout; its screenshot already showed the expected map and no assertions. The unchanged harness then passed after compilation. This is not a production performance measurement. Scoped renderer/harness ESLint passes. Full tests/typecheck/build are repeated at the owning07/13 gates; this narrow regression alone does not accept FRC13.
