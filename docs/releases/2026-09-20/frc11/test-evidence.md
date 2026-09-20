# FRC-11 verification

Baseline frontend8a5480fcc803da818cf0feeb135884f5bdcc1e68; Node26.4.0, installed Next16.2.11, React19.2.4. Package manifest currently names Next16.2.5; final release dependency identity is an FRC13/14 gate, not silently changed.

- Agent RED→GREEN/rendered20/20 and changed lint: [agent-evidence](agent-evidence.md).
- Root rendered surface4/4 passed after last capability update: `rtk proxy node --import tsx --test src/app/page-hero-copy.test.ts src/shared/ui/release-surface.test.tsx`.
- Root typecheck PASS: `rtk proxy node node_modules/typescript/bin/tsc --noEmit --incremental false`.
- Production build PASS twice; latest after hidden CTA/public-session fix compiled14.6s, TypeScript4.8s, all routes emitted. Initial sandbox build failed Google Fonts network; approved retry passed. Command `rtk proxy env FORTIS_RUNTIME_MODE=workspace FORTIS_LOCAL_DEVELOPMENT=true BACKEND_URL=http://127.0.0.1:8092 node node_modules/next/dist/bin/next build`. Build success does not assert production loopback backend is allowed; FRC01 correctly forbids that at runtime.
- Browser plugin absent; installed Playwright Chromium used. `rtk proxy node test/playwright/frc11-live.cjs` with frontend development localhost3111, existing FRC02 browser fixture8092 backed by isolated PG16. Target: landing CTA → form unavailable/workspace login;11 direct operational routes → notice. **PASS**, six widths including exact1280×720/1440×960; meaningful content, correct title/URL, no framework error overlay, no console errors, no horizontal overflow. Full-page screenshots wait for existing reveal animations; root inspected desktop/mobile.
- Separate local compiled demo server3112: `/dashboard`, permanent marker remains visible after scroll, screenshot PASS. It does not prove production origin/cookie isolation.
- Screenshot directory `/private/tmp/fortis-frc11-browser`: landing widths, workspace-notice.png, demo-marker.png. Synthetic UI only. Full screenshot paths remain local artifacts.
- Root calculator/client changed lint exit0. Final full-source regressions remain FRC13 coordination; six existing failures are not silently waived for changed code.

Browser fixture startup: backend `FRC02_TEST_DSN=<disposable local DSN> FRC02_BROWSER_SERVER=true go test ./cmd/app -run '^TestFRC02BrowserServer$' -count=1 -v -timeout35m`; frontend dev with explicit local development, backend8092, port3111. Avoid live services. The retained browser script uses fixed loopback ports only.
