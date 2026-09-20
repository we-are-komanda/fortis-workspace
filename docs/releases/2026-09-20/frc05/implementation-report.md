# FRC-05 — CODE PASS / RUNTIME BLOCKED

Root acceptance: 2026-09-20. FRC-00/04 code gates satisfied; COST-01…11 covered. Exact canonical cost replaces the mounted calculator mixed local/server total and map aliases. Saved map and calculator use one pinned server CostProjection; dirty state uses one whole explicitly marked draft. Unknown stays null with a known subtotal, zero stays zero, hidden/inactive positions remain included, real layer IDs group all placements. Legacy display outputs derive from exact amounts. Existing unrelated selection/scoring helpers remain unmounted and unchanged.

Backend binds cost-rub-v1 to immutable revision, caches a reconciled result by project/version/algorithm, and reauthorizes every read. Snapshot/document provenance follows the selected price. No invented future TCO/effectiveness calculation, no new dependency. [[ADR-0020-canonical-versioned-cost]] records the cross-repository decision in knowledge-base.

Independent review caught and fixed map zero override, malformed provenance accepted into React, ignored-component parsing, FE/BE legacy coercion/parity, saved-map use of draft totals and lost source document revision/checksum. Live custom layer order0 withoutcolor crashed an existing fallback array index; one-line clamp plus failing-then-passing map regression preserves custom layers. No unresolved reproduced finding in this bounded slice.

Runtime gates: actual release toolchain image, deployed PostgreSQL migration/rollback and cache behavior, ingress/TLS and production access evidence remain FRC13/14. Local Next production build passes; running that bundle with loopback HTTP correctly rejects the backend configuration under FRC01 and is not counted as production E2E. Dev-mode local browser uses explicit permitted local HTTP to actual Go/PostgreSQL. No remote deployment or real client data.

No local commit yet: shared project/schema/DI/store and catalog provenance hunks overlap evolving FRC09/06. Source manifest makes accepted code reviewable; parent pointers unchanged. FRC06 implementation dependency is now satisfied; budget enforcement remains FRC07 and official report/compare remain FRC08/10.
