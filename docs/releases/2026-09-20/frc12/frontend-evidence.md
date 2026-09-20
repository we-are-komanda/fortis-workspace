# FRC-12 frontend form and independent boundary review

Date: 2026-09-20. Bounded ownership: landing integration, `modules/home/ui/demo-request-form.tsx`, its browser tests, and the rendered landing-copy test. Root owns public routes, proxy/client helpers and shared HTTP errors. No commit, deployment, production configuration or real lead/email submission.

## Form behavior

- GET configuration is required before personal-data fields mount. Disabled configuration shows an unavailable message; failed configuration remains closed and offers a manual retry with support requestId when available.
- Fields: name, organization, email, optional comment, required unchecked consent. The checkbox renders the server text as escaped plain text and submits its server version. No legal text or response-time promise was invented.
- Validation supplies associated field feedback, `aria-invalid`, required attributes, an announced summary and focus on the first invalid field. Pending submission disables inputs and the submit button; a synchronous ref also prevents two same-tick submit events.
- The normalized body and UUID Idempotency-Key stay together in component memory. Manual retry of unchanged input uses the identical body/key. Changed input or changed consent version creates a new key. Inputs remain unchanged on HTTP, protocol and network failures; no automatic retries or persistent browser storage of lead data were introduced.
- Success appears only after the existing helper validates a `received` receipt. Error messages do not echo raw server text/stack, and show field feedback, requestId and validated Retry-After seconds where available. A stale consent version requires loading the published text and explicit fresh consent before retry.
- Existing FRC-11 positioning, styles and limitations remain. Root's browser review also identified hidden floating actions still exposed to keyboard/assistive technology: the hidden CTA is now inert/aria-hidden and the hidden scroll-to-top button has tabindex -1/aria-hidden.

## Executed evidence

All commands below run from `frontend/` through `rtk proxy`.

```sh
rtk proxy env FRC12_BROWSER_TESTS=true node --import tsx --test src/modules/home/ui/demo-request-form.browser.test.ts
```

**RED → GREEN:** the empty form first failed all four original browser cases due to missing status/fields. Final expanded run: **6 tests, 6 pass, 0 fail**, repeated after root's public-request fix. Chromium runs an in-memory esbuild bundle of the actual component and actual API helper. Synthetic `https://fortis.test` requests are intercepted; no Next server or external request is required. Cases cover disabled collection, client validation/escaped server consent, configuration error/manual reload, consent-version refresh, double submission, 503→429 retry identity, modified body identity, valid receipt and malformed-success rejection. The initial sandbox attempt could not create Chromium's macOS Mach port; the approved retry executed the actual tests. Default all-source runs skip these six browser cases unless `FRC12_BROWSER_TESTS=true` is supplied.

```sh
rtk proxy node --import tsx --test src/modules/home/infra/demo-request.release.test.ts src/shared/lib/retry-after.release.test.ts
```

**7/7 PASS**, independently run against root-owned BFF/client code using its synthetic loopback fixture.

```sh
rtk proxy node --import tsx --test src/shared/lib/auth-boundary.release.test.ts src/shared/lib/identity-isolation.release.test.ts src/shared/lib/retry-after.release.test.ts
```

**15/15 PASS** after the public-request isolation fix; authenticated behavior remains guarded.

```sh
rtk proxy node --import tsx --test src/app/page-hero-copy.test.ts src/shared/ui/release-surface.test.tsx
rtk proxy node node_modules/eslint/bin/eslint.js src/app/page.tsx src/app/page-hero-copy.test.ts src/modules/home/ui/demo-request-form.tsx src/modules/home/ui/demo-request-form.browser.test.ts
rtk proxy node node_modules/typescript/bin/tsc --noEmit --incremental false
rtk proxy git diff --check
```

Rendered FRC-11 regression **4/4 PASS**; changed-file lint, non-incremental typecheck and diff-check **exit 0**.

## Independent root-owned boundary review

One concrete finding was reproduced and fixed by root: public `sendDemoRequest`/GET used auth-bound `readJson`, so a synthetic HTTP 401 changed a signed-in `synthetic-user` to null and navigated to `/login?next=%2F`, discarding the public form. Root added explicit `sessionBound:false` only to these public helpers; default authenticated calls retain identity-generation checks, 401 sign-out and resource-error events.

Independent post-fix probe invoked actual GET/send helpers with each of 401/403/404: identity stayed `synthetic-user`, no navigation occurred and no resource-error event fired. Form 6/6 and auth/identity 15/15 were repeated on the fix. No further concrete blocker found in the reviewed boundary: disabled-by-default publication config, exact Origin match, streamed body cap, validated trusted-edge IP forwarding, generic-proxy header isolation and durable receipt validation match the documented code boundary.

## Limits

These tests do not prove a DB commit or SMTP delivery; backend integration evidence owns those claims. Root coordinates actual Next browser/layout/responsive verification and complete release checks. Idempotency and field state are retained for the mounted form only; cross-reload recovery was not requested or claimed. Publication still requires owner-provided consent/version, verified trusted-edge header handling, backend notification configuration, accountable operator and retention policy. None were enabled for production by this work.
