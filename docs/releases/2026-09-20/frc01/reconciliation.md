# FRC-01: baseline → current → target

Implementation approval: user attachment, 2026-09-20. Implement on current checkout; no reset/checkout/revert, commits or deployment.

Parent dbc2d05; frontend baseline 7ae4835, current 9feeb88; backend 7066656; knowledge-base eca5ee3.
Read-only origin check: parent/backend/knowledge-base refs match. Frontend current branch has no matching remote ref; no checkout change performed.

| Files (frontend unless prefixed) | Baseline | Current | Target |
|---|---|---|---|
| next.config.ts | broad rewrite, remote default | explicit rewrites, localhost default | API handler uses the same resolver as BFF; keep unrelated config |
| infra/backend-proxy.ts | aliases + remote default, JSON only | BACKEND_URL + unconditional localhost, JSON only | transparent streaming forwarding; separate JSON adaptation |
| shared/lib/api-client.ts | malformed success accepted as text | same | typed protocol error; preserve HTTP error semantics |
| app/api/auth/{login,register,me}/route.ts | JSON BFF | same | raw errors preserved; JSON only for token adaptation |
| app/api/defense/projects/**/route.ts | JSON BFF | same except sequential body read | raw statuses; validate successful project JSON |
| app/api/defense/{catalog,facilities}/route.ts | backend + fallback | static mock | explicit demo only, canonical workspace enterprises |
| app/api/defense/{layers,evaluate,recommend}/route.ts | mock | same | gate on server demo; unchanged algorithms |
| app/api/defense/assets/route.ts | BFF with fallback | absent | keep absent; reuse current canonical assets client |
| infra/{asset-library-api,enterprise-api,api-client,asset-documents-api}.ts | BFF assets, tolerant payloads | canonical assets/get supported, tolerant payloads | retain current endpoints and units; validate shapes |
| domain/use-defense-studio-store.ts | public env default local | same, retains scenario methods | explicit runtime mode; workspace does not initialize mock pack |
| shared/lib/use-defense-project-store.ts | clean project constructor, fallback catalog | default constructor, fallback persisted | no error/empty seeding; recovery separately unverified; keep current editing UI |
| domain/use-defense-variants-store.ts | autosave metadata + pending edits preserved | manual save only, no autosave | preserve manual save; no retry timer; preserve pending edits and failed load |
| ui/drone-defense-prototype.tsx | query demo, backend bootstrap + autosave | neither query demo nor autosave, restores local snapshot | keep absence; server mode; avoid overwriting open project; load requested project safely |
| ui/project-workspace-page.tsx | scoped-empty becomes all | same | honest empty; retain current project on navigation |
| ui/calculator-page.tsx | budget/cost/report fallback | cost/report fallback only | explicit server error/unverified state, no financial methodology change |
| app/layout.tsx | no runtime provider | same | expose only server-selected safe mode, visible demo indicator |
| backend/cmd/app/dependencies.go; internal/probe/* | empty probes | same | readiness DB ping; liveness independent |
| deploy/production/{docker-compose.yml,frontend.Dockerfile,README.md} | build-time URL/runtime, frontend health / | same + FRC-00 docs changes | server runtime config, private HTTP explicit, separate live/ready |
| knowledge-base ADR/index/roadmap | previous accepted fallback policy | same + FRC-00 notes | new ADR clarifies/supersedes conflicting clauses; preserve history |
| focused existing/new tests | fallback assertions | same where applicable | behavioural regressions, real localhost HTTP stub, binary path |

New files: server runtime resolver, API v1 handler, safe runtime endpoint/provider, live/ready handlers, regression tests and DB readiness check. None restored from baseline.

## Execution ledger

- Reconciliation complete before production edits. Current checkout has no autosave: do not introduce one merely to fix the baseline retry loop.
- Approved correction: network failure 502 (supersedes draft FRC-01 503); config 503; deadline 504. Upstream HTTP errors remain raw.
- HTTP on private container network explicitly permitted; external HTTPS remains deployment prerequisite, not verified here.

- Independent code review found three additional paths to the same defects: recovery normalizer expanded bundled assets; workspace creation used the demo factory; remount/pending load could erase edits. Regression tests reproduced each before fixes. Fixed shared normalization, reused a clean workspace factory and guarded/aborted loads. No unrelated review requests implemented.
- Final manual-save safety includes preserving edits made while save is pending, explicit error state and no retry scheduling. No autosave introduced.
- Removed only build-generated tsconfig formatting; no compiler contract change. Existing FRC-00 artifacts and user output files preserved.
