# FRC07 authoritative project budget

Status: **PASS — local staged acceptance**,2026-09-21, coordinator root. Actual Next→Go→PostgreSQL seven-checkpoint gate PASS with0 console/page errors. Production acceptance is not claimed.

The server owns the budget in the existing immutable project revision. All composition commits share the project lock, access check, expected version and exact full-candidate gate. A read-only preflight cannot reserve money or bypass the final transaction. New/imported projects are unlimited; an explicit accessible pinned source can establish an independent copy budget. Unknown prices remain unknown.

The calculator and GIS budget panel read a pinned server projection. Budget changes reuse frozen SaveAttempt/recovery handling, update the common saved baseline, and retain newer dirty edits. Reducing a limit below saved cost is allowed; later candidates compare against that saved cost until the next successful save. No new reservation table, dependency or public privilege mechanism was added.

Independent review reproduced and closed preview false success, project-switch preflight blocking, and restored form/request disagreement. Additional regressions preserve recovered input after a409 and prevent a pending budget attempt from being replaced by Save as new. See [review](independent-review.md), [criteria](acceptance-criteria.md), backend and frontend owner reports.

Pre-FRC13 prerequisites were checked alongside this stage: deck IDs use stable layer.id and Next/eslint-config-next are pinned16.2.11 in manifest and lock. Their separate evidence is in ../frc13/. These do not by themselves accept FRC13.

Remaining release chain after FRC07 acceptance: FRC08→FRC10→FRC13→FRC14. No push, deployment, production database mutation, or assignment to root/root2.
