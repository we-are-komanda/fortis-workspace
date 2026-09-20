# FRC-00: execution record

Plan: agreed in the task; specification: ../../fortis-release-specs/specs/FRC-00_release_baseline.md.

- Source baseline: parent dbc2d054798ec72fa7b607a64cae18319cfac3c3; frontend 7ae48358d10df796d6c5bc95e6b16791c9688ad9; backend 706665641894c966d2b0b83554554bc3d88b8f94; knowledge-base eca5ee3be1acbc543fa64706e654d6d631a2815c.
- Ruling: use separate local clones at pinned commits for verification; current worktree and submodule pointers stay untouched. Remote clone availability is a separate unverified check.
- Ruling: source baseline approval does not approve proposed product contracts (autosave/manual save, fallback, financial/access/revision changes). Record these as pending.
- Ruling: no commit, push or deployment; leave artifacts as working changes. Consequently artifact commit SHAs and final release acceptance remain pending.
- Pre-flight: manifest is consumed by verifier and acceptance matrix; local checkout metadata must not substitute for running-service evidence.

## Verification — 2026-09-20 09:46 UTC

Implementation workspace: `/private/tmp/fortis-frc00-3zsqdf42/workspace`.
Pristine source checkout: `/private/tmp/fortis-frc00-3zsqdf42/baseline`.
Both were cloned locally with `--no-hardlinks --no-checkout`, then detached at manifest SHAs.
No commits or user-checkout branch changes were made.

- RED: metadata test failed with `expected full knowledge-base SHA` before generator extension.
- RED: six verifier tests failed with `baseline verifier is not implemented` before verifier creation.
- RED: nested-sensitive-field test failed (empty error list) before nested-field allowlist.
- GREEN: `python3 -B -m unittest discover -s docs/releases/2026-09-20 -v` → 8 tests, OK, exit 0.
- `bash deploy/production/write-deploy-info.test.sh` → `ok - deploy info metadata contract`, exit 0.
- `bash deploy/production/deploy-with-notify.test.sh` → `ok - deploy Worker notification contract`, exit 0. This existing test replaces curl/compose with test doubles; it does not deploy or notify anyone. Simulated notification failure and healthcheck retry messages are expected.
- `bash -n deploy/production/write-deploy-info.sh deploy/production/write-deploy-info.test.sh` → exit 0.
- S1: `python3 -B docs/releases/2026-09-20/verify_baseline.py source --checkout /private/tmp/fortis-frc00-3zsqdf42/baseline` → `PASS source: supplied evidence matches manifest; this is not release acceptance`, exit 0.
- S3: `python3 -B docs/releases/2026-09-20/verify_baseline.py runtime` → `BASE-02: runtime evidence missing`, `BASE-05: backend SHA missing`, expected exit 1. Runtime acceptance is blocked.
- S4 (cwd: pristine baseline/backend): `GOTOOLCHAIN=local GOCACHE=/private/tmp/fortis-frc00-3zsqdf42/go-cache GOPROXY=off go test -count=1 -run '^TestUpdateProject' ./internal/modules/defense_project/application` → `ok github.com/fortis/backend/internal/modules/defense_project/application 0.445s`, exit 0. Existing application unit tests, no DB or customer data.

### Environment and external evidence

Actual local tools: Node v26.4.0; pnpm 10.28.2; Go go1.26.0 darwin/arm64.
These differ from build declarations; they are not presented as production versions.
Baseline frontend package.json: Next 16.2.11, React 19.2.4, pnpm 10.26.1.
Docker is unavailable locally. No production image build, frontend build, database
integration or browser acceptance was performed in this FRC-00 pass.

Read-only remote check (SSH BatchMode, strict host-key checking, no host-key updates):
`git ls-remote git@github.com:Ramilko37/fortis-back.git refs/heads/develop`
returned `706665641894c966d2b0b83554554bc3d88b8f94 refs/heads/develop`, exit 0.
This confirms the backend origin branch only, not a running backend image.
Read-only `docker ps` over SSH to the documented dev VM failed authentication:
`Permission denied (publickey)`, exit 255. No remote mutation occurred.

Ruling: `.gitmodules` backend URL corrected to verified current origin; parent source
SHA remains historical evidence, and the changed configuration awaits its own commit.
Cost if wrong: a later canonical host change requires updating this one URL; no history was moved.

### Tracker

Read current Linear descriptions/statuses. Mapping is in acceptance-matrix.md.
Queries: release baseline, deploy, заявк, лендинг, E2E. Unrelated retailer/cart issues
were excluded by content. No tracker mutation; absence of a matching search result
is not evidence that no task exists anywhere.

### Pending

No environment/deployment ID has been approved as runtime acceptance target.
No deployed frontend/backend SHA/digest or applied-migration inventory is known.
New contracts remain proposals; no changes to auth, save mode, API DTO or DB schema.
Artifacts and original untracked specification package require review before committing.
No final reviewer or acceptedAt is assigned for release acceptance.

## Final independent review and fix pass

Fresh-context reviewer inspected working diffs and untracked release artifacts.
No Critical or Minor findings. Two Important findings were reproduced and fixed:

1. Missing/uninitialized submodules inherited the parent Git SHA. Added a real local
   clone with uninitialized child directories: RED `uninitialized child must have unknown SHA`.
   Generator now checks the requested directory against Git's actual repository root;
   missing child identities and dirty states are `unknown`.
2. Object-valued fields bypassed scalar JSON contracts. RED showed nested environment,
   tool version and branch values accepted; explicit scalar/list formats now reject them.
   Synthetic sensitive values are never echoed in diagnostics.

After fixes: verifier suite 10 tests, OK; generator regression, existing notification
contract and bash syntax checks pass. Clean source verifier still passes. Parent and
knowledge-base `git diff --check` pass. No re-review claimed; fixes verified by regressions.

Review rulings:
- Runtime identity/provenance/migrations remain declined by reviewer: retain explicit blockers;
  cost of accepting without evidence would be testing or releasing the wrong artifacts.
- Reviewer did not re-query Linear or origin: executor's live read results are evidence,
  not independent remote verification; statuses remain timestamped, not permanent truth.
- Full frontend build/backend integration not reviewed: outside changed baseline tooling;
  no production-readiness or full FRT acceptance is claimed.
- Input specification package reviewed as supplied requirements: no modifications to it;
  proposed architecture still requires product approval.
- Copy preservation reviewed by executor separately: compare every existing destination
  against original HEAD and reject collisions before copying; no blanket directory replacement.

### Working artifact fingerprints (SHA-256)

These identify tested uncommitted files; they are not Git commit SHAs.
- `docs/releases/2026-09-20/release-manifest.json`: `cba0d4b945ba61197054769b0906389d242b5c4b59566d0d9686b92b4e64f4b3`
- `docs/releases/2026-09-20/verify_baseline.py`: `1b71357764dbd08fe167f788f47915a03272d29e79a205de8af86599607e3e02`
- `docs/releases/2026-09-20/test_verify_baseline.py`: `322248498588f00c00206c677fbf1473b8938faa9109d64071fdc9f3e917bcd8`
- `deploy/production/write-deploy-info.sh`: `e123427749b543c5d4063668c5ee38acaa03d40230ae01bd906233baae212ab4`
- `deploy/production/write-deploy-info.test.sh`: `ae5247cd7955e4c3c31cbb9e5fd8e63d5933a72c570bcbb675782f873ec0c700`

## Post-copy verification in user workspace

Copied exactly 13 changed/new FRC-00 files after checking all seven existing destinations
against their original HEAD contents and rejecting collisions at new paths. Hashes of
all original specification-package files and existing .deploy-info were unchanged.
All four current HEADs and branch selections were preserved; no index/commit/push operation.

Final checks from /Users/rr/Documents/Fortis:
- 10 verifier tests: OK (3.524s); generator regression including uninitialized children: PASS.
- Existing notification test: PASS; bash syntax and parent/knowledge-base diff whitespace checks: PASS.
- Clean separate baseline: source check exit 0.
- User working checkout: expected exit 1 (dirty parent/FE/KB and frontend SHA mismatch);
  the verifier does not silently accept the user's older frontend as the selected baseline.
- Missing runtime metadata: expected exit 1, BASE-02/BASE-05 explicitly blocked.
- All 13 copied file contents matched the reviewed/fixed implementation workspace before this log append.

No frontend/backend source edits, production migration, runtime deployment or external
notification occurred. Remaining runtime, build-environment and product-decision blockers
are retained in acceptance-matrix.md and the knowledge-base release index.
