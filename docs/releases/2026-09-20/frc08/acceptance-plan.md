# FRC-08 independent acceptance plan

Status: checklist executed; results and limitations are in [independent-review.md](independent-review.md). Stage acceptance remains the coordinator's decision. Starting accepted FRC-07 commits: parent5008d25, frontend6838dd1, backend387572a, knowledge-base00c5aaa. The coordinator owns actual full-stack acceptance and final checks/build; implementation owners own production code. Independent verification owns a new rendered comparison test and this checklist/review.

## Contract used as the oracle

Read [FRC-08](../../../fortis-release-specs/specs/FRC-08_compare_revisions.md), [ADR-0017](../../../../knowledge-base/03_Architecture/ADR-0017-enterprise-access-boundary.md) and the autonomous-run contract. CMP-09's proposed viewer/viewCost role is deferred: current enterprise membership authorizes financial access, without inventing new RBAC. Missing/foreign/revoked resources remain404 without partial money disclosure.

GET compare receives explicit `projectIdA,projectVersionA,projectIdB,projectVersionB`. Legacy id1/id2 are ID aliases only; they do not select mutable latest versions or remove version requirements. Same project with different revisions is valid; identical refs are400. Both sides must belong to the same accessible enterprise. The result has `enterpriseId`, a/b `{identity,name,updatedAt,cost,budget}`, exact signed `differenceMinor`, `differencePercent` and warnings. Every side's cost and budget identity must match its selected immutable revision.

Selections remain pinned through background saves and list refresh/pagination. Explicit Save-and-compare may repin a selected side matching the pre-save active project ID and version only after confirmation; another historical side of that project remains pinned. Explicit last-saved comparison leaves unsaved edits in place. Newer edits during the save keep the dialog open until explicit saved-version comparison. Price or quantity alone cannot imply effective or sufficient protection.

## Acceptance probes

| ID | Probe | Required outcome |
|---|---|---|
| CMP-01 | Finance fixture A7=47500000 minor, B3=55000000 | Names, timestamps, identities, cost and budget shown; B−A=7500000; percent15.79. No float money. |
| CMP-02 | Background save A8 and list refresh after selecting A7/B3 | Selection, request and displayed identities remainA7/B3; historical sums/provenance remain unchanged. |
| CMP-03 | Complete A=0/B>0, both0 and negative/zero deltas | Exact signed absolute difference. A0 percentnull/Not calculated; no Infinity/NaN/negative zero. |
| CMP-04 | One selected price unknown in B | B total and both deltasnull; known subtotal and incomplete mark visible. Explicit zero remains complete. No cheaper/better assertion. |
| CMP-05 | Second operand missing/foreign/revoked, including malformed/expensive A | Both authorization checks precede financial calculation/response;404 contains no A money or partial result. UI removes prior successful result. |
| CMP-06 | Both resources accessible but different enterprises |400 incompatible_projects. UI selection offers only current enterprise; enterprise change clears selection/result/pending state. |
| CMP-07 | Same layer/asset name but distinct stable IDs | Rows stay separate and unmatched identity is explained. Stable matching IDs show quantity/price changes, not fuzzy name matches. |
| CMP-08 | Mutate current catalogue after both revisions saved | Compare remains pinned to saved exact amounts, sources, dates and quality; differing provenance yields comparability warning. |
| CMP-09 revised | Ordinary member vs unrelated user | Current membership contract applies. No invented viewer role, financial permission API or CSS hiding claim. |
| CMP-10 | Same project at7 and8; identical project7/7 | First allowed; identical pair rejected before display. Missing/zero/fractional/invalid versions rejected; conflicting canonical/legacy aliases400. |
| CMP-11 | Dirty selected active project: Cancel | No save/compare request; edits and selected refs remain intact. |
| CMP-12 | Dirty selected active project: explicit last saved | Compare selected saved refs; dirty current content stays dirty and unchanged, no PUT. |
| CMP-13 | Dirty selected active project: Save-and-compare pending/error/conflict | No compare before confirmed save; no navigation, lost input or automatic retry. After confirmed save, only matching selected side repins to acknowledged version; newer concurrent edits remain dirty. |
| CMP-14 | Change refs while an old compare is pending; old success/error arrives last | Old result/error cannot replace the current selection or current successful result. All rendered data belongs to one request pair. |
| CMP-15 | Change enterprise/identity while compare is pending | Old private result and selections disappear; stale response cannot reappear. New context is immediately usable without waiting for old response. |
| CMP-16 | Payload wrong enterprise/ref/version/digest or inconsistent per-side identity | Whole response rejected as protocol error; no partial price display, no local/demo fallback. |
| CMP-17 | Large exact money, one-minor difference and percent tie rounding | Exact string arithmetic, signed B−A; percent formatted to two decimal places using agreed server rounding. Unknown/zero denominator rules preserved. |
| CMP-18 | Both sides show layers/types, positions/units, budgets and sources | Each column derived only from that side's saved projections. No current catalogue enrichment or fabricated effectiveness/security claims. |
| CMP-19 | Another request confirms selected-project denial while comparison is visible or pending | Existing result clears and late success cannot publish prices. A denied unrelated active project does not hide the selected authorized pair. |

## Test ownership and completion evidence

Frontend owner: new comparison component/API boundary and focused pure/store tests. Independent verifier: `frontend/src/modules/defense-calculator/ui/configuration-comparison.browser.test.ts`, using real component/stores in Chromium with deterministic held/reordered HTTP responses. Backend owner: transport/application/pure comparison and actual PostgreSQL immutable-revision/access tests. Coordinator: real workspace→save→compare flow, final regression/type/lint/build and stage acceptance.

The rendered harness reuses the existing installed esbuild/tsx and Playwright pattern, with no dependency or production test seam. It does not claim to prove backend authorization, database immutability or atomic saves. Record command, exact tested source/dependency snapshot, raw output and exit status. Preserve actual RED→GREEN; label tests first run after a fix honestly. Compare any full frontend failures with the six exact historical signatures; new failures must be investigated. Root executes escalated browser checks if the independent agent's earlier approval-review usage limitation remains unavailable; no workaround bypass.
