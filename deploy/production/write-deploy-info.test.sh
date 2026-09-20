#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="${SCRIPT_DIR}/write-deploy-info.sh"

fail() {
  printf 'not ok - %s\n' "$1" >&2
  exit 1
}

output_file="$(mktemp)"
dirty_marker="$(mktemp "${SCRIPT_DIR}/.deploy-info-test.XXXXXX")"
uninitialized="$(mktemp -d)"
trap 'rm -f "${output_file}" "${dirty_marker}"; rm -rf "${uninitialized}"' EXIT

"${SCRIPT_PATH}" "${output_file}"

grep -q '^DEPLOY_REF=' "${output_file}" || fail "expected parent ref"
grep -q '^DEPLOY_COMMIT_SUBJECT=' "${output_file}" || fail "expected parent commit subject"
grep -q '^DEPLOY_BRANCH=' "${output_file}" || fail "expected parent branch"
grep -q '^DEPLOY_FRONTEND_REF=' "${output_file}" || fail "expected frontend ref"
grep -q '^DEPLOY_FRONTEND_COMMIT_SUBJECT=' "${output_file}" || fail "expected frontend commit subject"
grep -q '^DEPLOY_BACKEND_REF=' "${output_file}" || fail "expected backend ref"
grep -q '^DEPLOY_BACKEND_COMMIT_SUBJECT=' "${output_file}" || fail "expected backend commit subject"
grep -q '^DEPLOY_GENERATED_AT=' "${output_file}" || fail "expected generated timestamp"
grep -q '^DEPLOY_KNOWLEDGE_BASE_SHA=[0-9a-f]\{40\}$' "${output_file}" || fail "expected full knowledge-base SHA"
grep -q '^DEPLOY_DIRTY=true$' "${output_file}" || fail "expected dirty parent to be recorded"

set -a
# shellcheck source=/dev/null
source "${output_file}"
set +a

[[ -n "${DEPLOY_REF}" ]] || fail "expected sourced parent ref"
[[ -n "${DEPLOY_COMMIT_SUBJECT}" ]] || fail "expected sourced parent subject"
[[ -n "${DEPLOY_FRONTEND_REF}" ]] || fail "expected sourced frontend ref"
[[ -n "${DEPLOY_BACKEND_REF}" ]] || fail "expected sourced backend ref"
[[ "${DEPLOY_KNOWLEDGE_BASE_SHA}" == "$(git -C "${SCRIPT_DIR}/../../knowledge-base" rev-parse HEAD)" ]] || fail "knowledge-base SHA must describe actual checkout"

# An uninitialized submodule must never borrow its parent's Git identity.
git clone --quiet --no-hardlinks --no-checkout "${SCRIPT_DIR}/../.." "${uninitialized}/workspace"
git -C "${uninitialized}/workspace" checkout --quiet --detach HEAD
cp "${SCRIPT_PATH}" "${uninitialized}/workspace/deploy/production/write-deploy-info.sh"
bash "${uninitialized}/workspace/deploy/production/write-deploy-info.sh" "${uninitialized}/metadata"
for prefix in FRONTEND BACKEND KNOWLEDGE_BASE; do
  grep -q "^DEPLOY_${prefix}_SHA=unknown$" "${uninitialized}/metadata" || fail "uninitialized child must have unknown SHA"
  grep -q "^DEPLOY_${prefix}_DIRTY=unknown$" "${uninitialized}/metadata" || fail "uninitialized child must have unknown dirty state"
done

printf 'ok - deploy info metadata contract\n'
