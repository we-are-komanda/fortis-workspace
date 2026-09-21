# Exact tested Next toolchain pin — pre-FRC13

Manifest and repository lockfile had Next/eslint-config-next16.2.5 while installed packages and installed pnpm lock used16.2.11. Both top-level packages are now exact16.2.11, matching the already tested runtime. Local Next16.2.11 installation/upgrading docs read first; no routing/cache/runtime API changed.

pnpm install --lockfile-only --offline --ignore-scripts failed on stale cached Tailwind metadata; it changed no lock. The normal lock-only command succeeded without installing or executing package scripts. Diff retains all other direct versions; pnpm refreshed Next/SWC/env/eslintplugin peer keys and some existing transitive resolutions (hasown/tinyglobby/nanoid/optional sharp runtime), with registry integrity metadata.

A frozen offline install of this exact lock succeeded in the owned isolated build copy, with lifecycle scripts disabled. It reconciled two package links and restored the declared dayjs dependency there. Working frontend/node_modules and userdev server were not reinstalled. Commands/raw logs adjacent. This establishes lock resolvability; full tests/typecheck/productionbuild after pin are required at07/13 and not claimed here in advance.

FRC07 verification after pin: frozen full suite314=232PASS/6exacthistoricalFAIL/76SKIP; typecheck, changed-file lint and productionbuild PASS; rendered regressions56/56PASS. Raw evidence is in ../../frc07/verification-logs/. FRC13 full integrated chain remains pending.
