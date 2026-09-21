# FRC-06 independent core review — 2026-09-21

Reviewed `045db0d` and the current working diff: save-state comparison, scoped storage, project/variants stores, API acknowledgement/replay, VariantsModal, IdentityBoundary, workspace transitions and map bootstrap. The reviewer did not implement this core. The reviewer's separate provenance helper/test repairs are reviewed by root.

## Findings and closure

| Priority | Finding | Status and verification |
|---|---|---|
| P1 | UI-only selection after loading server P persisted its baseline over an undiscovered scoped recovery draft. Recovery then disappeared without Restore/Discard. | **Closed.** Selection no longer persists; a no-op business update does not persist. Independent original probe now retains the unsaved draft and recovery candidate. Permanent regression: `UI selection after server load cannot overwrite an undiscovered recovery draft`. |
| P1 | 403/404 changed dirty to unverified, bypassing the variants transition guard. Same-project map bootstrap also reloaded and silently replaced unsaved memory after access returned. | **Closed.** VariantsModal includes unverified enterprise state; same-project bootstrap preserves changed business content. Independent original bootstrap probe now preserves the draft. Root reports the permanent browser regression `revoked dirty project still requires an explicit decision before another variant loads` passing in the 13-test browser run; this reviewer independently checked the source and store/bootstrap probe. |
| P2 | Discard accessed forbidden localStorage even when persistent drafts were disabled, blocking a memory-only transition/logout. | **Closed.** Removal honors draft policy; independent original SecurityError probe now discards successfully. Permanent regression: `memory-only discard works when persistent drafts are disabled and storage is forbidden`. |
| P2 | A malformed save acknowledgement with matching P/version but another enterprise rewrote immutable ownership and marked the project saved. | **Closed.** API boundary rejects enterprise mismatch as protocol failure and enters verification. Independent original probe retains enterprise E and dirty state. Permanent regression: `a malformed save acknowledgement cannot move a project to another enterprise`. This was a malformed-response test, not evidence of an actual backend authorization failure. |
| P2 | Creating a new workspace project after leaving a denied project retained the old resource access error and active variant, preventing POST in another authorized enterprise. | **Closed in explicit initialization.** Workspace clears the previous resource denial/variant before creating the new context. Independent probe executes the actual `createProject` function extracted and transpiled from the component: one POST, enterprise F, active new project, saved state, no access error. It does not bypass denial while editing the original project. |
| P2 | Successful PUT followed by list-refresh 503 left a shared error. Save-and-leave rejected the acknowledged save, and retry was a no-op because the project was already saved. Related error gates affected Save-and-open and workspace creation. | **Closed.** Original probe now returns true for first/repeated leave after confirmed version 8, saved state, no pending attempt and idle save status. Only one PUT and the failed list GET occur. List error stays visible; sibling modal/workspace transitions use confirmed save state. Permanent regression: `a confirmed save permits leaving even when subsequent project list refresh fails`. |
| P1 | Logout dialog state lived above the identity-keyed Fragment. After A opened the dialog and session verification switched to B, the old dialog and A's project name remained visible under B. | **Closed.** The whole session boundary is keyed to identity generation. Independent component probe follows keyed instances across verified A→B and now renders `oldOwnerNameVisible: false`, `logoutModalOpen: false`. Root's permanent browser test is `switching identity clears the previous user logout intent and name`. A generation check also rejects a late logout completion before clearing a newer identity; covered by the identity regression group. |

## Reproduction commands

Run from `frontend/`. Temporary probes exercise real production store/API functions with synthetic transport/storage. The workspace probe additionally executes the actual component initialization function; it is not a browser test.

```sh
rtk proxy node --import tsx /private/tmp/frc06-review-recovery-overwrite.ts
rtk proxy node --import tsx /private/tmp/frc06-review-unverified-reload.ts
rtk proxy node --import tsx /private/tmp/frc06-review-disabled-storage-discard.ts
rtk proxy node --import tsx /private/tmp/frc06-review-foreign-enterprise-summary.ts
rtk proxy node --import tsx /private/tmp/frc06-review-workspace-init.ts
rtk proxy node --import tsx /private/tmp/frc06-review-list-error-after-save.ts
rtk proxy node /private/tmp/frc06-review-url-sync.cjs
rtk proxy node /private/tmp/frc06-review-logout-identity.cjs
```

All eight checks now exit 0; exact outputs and commands are in `verification-logs/independent-review-closure.json`. The final probe models the actual wrapper's identity-keyed component lifecycle. Original probe `/private/tmp/frc06-review-new-project-after-denial.ts` demonstrated the missing initialization reset; it directly invokes `replaceProject`, which intentionally retains denial inside the old core context, so closure uses the real workspace initializer instead.

The additional URL-effect check executes the actual callback extracted from DefenseStudioShell: a changed active ID replaces projectId, removes the legacy project key, preserves other query values, and does not replace on unchanged/null/initial active IDs. Live reload verification remains root-owned.

No other distinct concrete defects were found in this pass. Frozen create body/key, single in-flight save, business edits versus selection, GET-first ambiguous update verification, identity/project/enterprise guards, explicit scoped recovery and no automatic hydration were inspected. Browser navigation, real API/PostgreSQL evidence and production gates remain separate; the review did not launch a browser, restart a server, mutate backend data or commit changes. The separate final verification includes an isolated production build; evidence is under `verification-logs/`. No open review findings remain.
