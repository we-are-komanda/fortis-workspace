# FRC-11 bounded frontend evidence

Date: 2026-09-20. Base frontend: `8a5480fcc803da818cf0feeb135884f5bdcc1e68`. Node `v26.4.0`, installed Next.js `16.2.11`, React `19.2.4`. This is local implementation evidence, not production acceptance.

## Implemented

- Landing uses the exact approved title, subtitle, CTA labels and calculation limitation. Removed unsupported detection/accuracy/SLA/savings/AI/brand-connector claims and operational mock preview. Existing colors, typography, responsive containers and radar decoration remain; GIS rendering was not redesigned.
- `product-capabilities.ts` is the presentation manifest. Workspace/map/own inputs/versions are `available`; operational dashboard, retrospective and scenarios are `demo`; calculation/comparison/report are `not_released` pending their individual acceptance. The manifest does not grant resource access.
- All eight dashboard routes (including arbitrary site ID), dashboard layout, retrospective route and both scenario query aliases are guarded by server runtime mode. Workspace returns a service notice before importing the mock module. The dashboard layout and retrospective route render per request; prototype awaits request-time search parameters. Invalid runtime configuration fails rather than exposing demo.
- Workspace studio navigation returns to `/workspace`, hides unavailable capabilities and removes the inert export button. Demo retains a fixed “Демонстрационные данные” marker; unprotected demo layouts also identify synthetic data in their initial server-rendered content.
- Demo-request destination remains visible, with a disabled submit and explicit statement that no request is created. Root will replace this block during FRC-12 integration.
- Public document metadata now describes configuration planning. Calculator implementation is owned by root; its copy/requestId changes were handed off and are not claimed here.

## Tests and results

Commands ran from `frontend/`, prefixed with `rtk proxy`.

1. RED: `node --import tsx --test src/app/page-hero-copy.test.ts` — **1 FAIL**, missing exact approved headline in the actual server-rendered landing. Replaced the obsolete source-string assertion with React rendering before changing production copy.
2. Final focused release surface: `node --import tsx --test src/app/page-hero-copy.test.ts src/shared/ui/release-surface.test.tsx` — **4/4 PASS**. Covers rendered copy/links/disabled form, capability decisions, visible notices/demo marker, and actual exports for every blocked direct route including arbitrary IDs and scenario aliases.
3. Focused regressions: `node --import tsx --test src/app/page-hero-copy.test.ts src/shared/ui/release-surface.test.tsx src/modules/drone-defense/domain/defense-studio-contract.test.ts src/modules/drone-defense/domain/prototype-workflow-contract.test.ts src/shared/lib/auth-boundary.release.test.ts src/shared/lib/identity-isolation.release.test.ts` — **20/20 PASS**.
4. Changed-file lint below — **PASS, exit 0**. Existing landing mounted-state effects were removed and intersection observer results destructured to satisfy React hook lint without disabling rules; visual behavior remains equivalent.
5. `node node_modules/typescript/bin/tsc --noEmit --incremental false` — two runs **PASS**. Latest run during root's FRC-12 RED phase exits 2 only for not-yet-created `@/app/api/public/demo-requests/route` imported from `src/modules/home/infra/demo-request.release.test.ts:42,55,64`. Root notified; final shared typecheck belongs to integration verification.
6. `git diff --check` — **PASS**.

Exact lint arguments:

```sh
rtk proxy node node_modules/eslint/bin/eslint.js src/app/page.tsx src/app/layout.tsx src/app/page-hero-copy.test.ts src/shared/config/product-capabilities.ts src/shared/ui/release-capability.tsx src/shared/ui/demo-marker.tsx src/shared/ui/release-surface.test.tsx src/shared/ui/runtime-provider.tsx src/modules/drone-defense/ui/defense-studio-shell.tsx src/modules/drone-defense/domain/retrospective-analysis-navigation-contract.test.mjs 'src/app/(dashboard)' 'src/app/(defense-studio)/prototype/page.tsx' 'src/app/(defense-studio)/retrospective-analysis/page.tsx'
```

## Historical tests and limits

An intermediate 22-test selection had two failures. `user-facing-copy-contract.test.ts` remains the known baseline failure at line 119. The retrospective navigation source test initially failed sooner because it required an unconditional module import; that obsolete assertion now expects the guarded dynamic import. Its existing unrelated compact-drawer assertion still fails with the original message and original line 21. No baseline test was suppressed or removed. The full suite was not rerun by this agent to avoid overlapping root integration work.

No shared build, browser/dev server, deployment, migration, commit or push was started. COPY-06 responsive screenshots at 375/414/768/1024/1280/1440 and deployed runtime checks remain root-coordinated. Existing FRC-02 browser tests assume a calculator navigation link; that link is deliberately hidden until calculation acceptance, so browser acceptance must use the current capability surface rather than the old unqualified link.

Local Next guides read: layout/page conventions, notFound, route-segment config, connection, and `caching-without-cache-components.md` (installed config does not enable Cache Components; request-time `force-dynamic` is supported).

Calculator handoff: replace technical “backend-контура”, “payload”, “backend-расчёт” and false local fallback copy; retain incompleteness/draft messaging and expose requestId for support; add the exact calculation limitation. Root owns this edit during financial work.
