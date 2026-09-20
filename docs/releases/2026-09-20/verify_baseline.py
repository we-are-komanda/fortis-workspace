"""FRC-00 checks; source success does not imply runtime or release acceptance."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import subprocess


REPOS = ("parent", "frontend", "backend", "knowledge-base")
DEPLOYMENT_FIELDS = {
    "environment", "frontendDeploymentId", "frontendImageDigest", "backendImageDigest",
    "appliedMigrations", "runtimeMode", "nodeVersion", "pnpmVersion", "goVersion",
}
VERSION = r"v?\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?"


def matches(pattern, value):
    return isinstance(value, str) and re.fullmatch(pattern, value) is not None


def valid_migrations(value):
    return isinstance(value, list) and all(
        matches(r"\d+_[A-Za-z0-9_]+\.up\.sql", name) for name in value
    ) and len(value) == len(set(value))


def valid_deployment_field(key, value):
    if key == "appliedMigrations":
        return valid_migrations(value)
    if key.endswith("ImageDigest"):
        return matches(r"sha256:[0-9a-f]{64}", value)
    if key.endswith("Version"):
        return matches(VERSION, value)
    if key == "runtimeMode":
        return value == "workspace"
    return matches(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}", value)


def check_manifest(manifest):
    errors = []
    if not isinstance(manifest, dict):
        return ["BASE-03: manifest must be an object"]
    if set(manifest) != {"releaseId", "status", "specification", "repositories", "toolchain",
                         "migrationFiles", "requiredEnvNames", "deployment"}:
        errors.append("BASE-03: unexpected or missing manifest fields")
    repos = manifest.get("repositories", {})
    if not isinstance(repos, dict) or set(repos) != set(REPOS):
        return errors + ["BASE-01: four pinned repositories required"]
    for name in REPOS:
        repo = repos.get(name, {})
        if not isinstance(repo, dict):
            errors.append(f"BASE-01: {name} repository must be an object")
            continue
        if set(repo) != {"url", "branch", "sha"} or not matches(r"[0-9a-f]{40}", repo.get("sha")):
            errors.append(f"BASE-01: {name} requires a full commit SHA and repository fields")
        if not matches(r"[A-Za-z0-9][A-Za-z0-9._/-]*", repo.get("branch")):
            errors.append(f"BASE-03: {name} branch must be a ref name")
        if not matches(r"git@github\.com:[\w.-]+/[\w.-]+\.git", repo.get("url")):
            errors.append(f"BASE-03: {name} requires a credential-free GitHub SSH URL")
    if not isinstance(manifest.get("requiredEnvNames"), list) or not all(
        matches(r"[A-Z][A-Z0-9_]*", name) for name in manifest["requiredEnvNames"]
    ):
        errors.append("BASE-03: environment names only; values are forbidden")
    deployment = manifest.get("deployment", {})
    if not isinstance(deployment, dict) or set(deployment) != DEPLOYMENT_FIELDS:
        errors.append("BASE-03: unexpected or missing deployment fields")
    elif any(value is not None and not valid_deployment_field(key, value) for key, value in deployment.items()):
        errors.append("BASE-03: invalid deployment value types or formats")
    toolchain = manifest.get("toolchain", {})
    if not isinstance(toolchain, dict) or set(toolchain) != {
        "next", "react", "pnpm", "goDirective", "goToolchain", "frontendNodeImage",
        "backendGoImage", "openapiNodeImage", "swagger", "swagger2openapi",
    }:
        errors.append("BASE-03: unexpected or missing toolchain fields")
    else:
        for key, value in toolchain.items():
            pattern = VERSION
            if key.endswith("Image"):
                pattern = r"[\w./-]+:[\w.-]+(?:@sha256:[0-9a-f]{64})?"
            elif key == "goDirective":
                pattern = r"\d+\.\d+(?:\.\d+)?"
            elif key == "goToolchain":
                pattern = r"go\d+\.\d+\.\d+"
            if not (key == "swagger2openapi" and value is None) and not matches(pattern, value):
                errors.append(f"BASE-03: invalid toolchain value: {key}")
    spec = manifest.get("specification", {})
    if not isinstance(spec, dict) or set(spec) != {"path", "id", "sha256"}:
        errors.append("BASE-03: invalid specification fingerprint fields")
    elif (spec["path"] != "docs/fortis-release-specs" or spec["id"] != "FRC-00"
          or not isinstance(spec["sha256"], dict) or not spec["sha256"] or not all(
              matches(r"[A-Za-z0-9_][A-Za-z0-9_./-]*", name) and ".." not in name
              and matches(r"[0-9a-f]{64}", digest) for name, digest in spec["sha256"].items())):
        errors.append("BASE-03: invalid specification identity or fingerprints")
    if not valid_migrations(manifest.get("migrationFiles")):
        errors.append("BASE-03: invalid migration inventory")
    if not matches(r"\d{4}-\d{2}-\d{2}", manifest.get("releaseId")) or not matches(r"[a-z_]+", manifest.get("status")):
        errors.append("BASE-03: invalid release identity or status")
    return errors


def git(root, *args):
    return subprocess.check_output(
        ["git", "--no-optional-locks", "-C", str(root), *args], text=True,
        stderr=subprocess.DEVNULL,
    ).strip()


def check_source(manifest, root):
    errors = []
    for name in REPOS:
        repo = root if name == "parent" else root / name
        expected = manifest["repositories"][name]["sha"]
        try:
            if git(repo, "rev-parse", "HEAD") != expected:
                errors.append(f"BASE-01: {name} checkout SHA mismatch")
            if git(repo, "status", "--porcelain", "--untracked-files=normal"):
                errors.append(f"BASE-01: {name} worktree is not clean")
            if name != "parent":
                entry = git(root, "ls-tree", manifest["repositories"]["parent"]["sha"], name).split()
                if entry[:3] != ["160000", "commit", expected]:
                    errors.append(f"BASE-01: {name} parent gitlink mismatch")
        except subprocess.CalledProcessError:
            errors.append(f"BASE-01: {name} Git metadata unavailable")
    return errors


def check_runtime(manifest, runtime):
    errors = check_manifest(manifest)
    if errors:
        return errors
    if not isinstance(runtime, dict):
        return ["BASE-03: runtime evidence must be an object"]
    if set(runtime) != DEPLOYMENT_FIELDS | {"frontendSha", "backendSha", "observedAt"}:
        errors.append("BASE-03: unexpected or missing runtime fields; supply sanitized metadata only")
    if not matches(r"[0-9a-f]{40}", runtime.get("backendSha")):
        errors.append("BASE-05: backend SHA missing")
    for name in ("frontend", "backend"):
        if runtime.get(name + "Sha") != manifest["repositories"][name]["sha"]:
            errors.append(f"BASE-02: {name} runtime SHA mismatch")
        if not matches(r"sha256:[0-9a-f]{64}", runtime.get(name + "ImageDigest")):
            errors.append(f"BASE-02: {name} immutable image digest required")
    expected = manifest["deployment"]
    for key in sorted(DEPLOYMENT_FIELDS):
        if not valid_deployment_field(key, runtime.get(key)):
            errors.append(f"BASE-03: invalid runtime value type or format: {key}")
        if expected.get(key) is None or expected.get(key) == "":
            errors.append(f"BASE-02: manifest deployment field unresolved: {key}")
        elif runtime.get(key) != expected[key]:
            errors.append(f"BASE-02: deployment field mismatch: {key}")
    if runtime.get("runtimeMode") != "workspace":
        errors.append("BASE-02: workspace runtime required")
    migrations = runtime.get("appliedMigrations")
    if not isinstance(migrations, list) or any(m not in manifest["migrationFiles"] for m in migrations):
        errors.append("BASE-02: applied migration inventory invalid")
    try:
        if datetime.fromisoformat(runtime.get("observedAt", "").replace("Z", "+00:00")).tzinfo is None:
            raise ValueError
    except (ValueError, AttributeError):
        errors.append("BASE-02: timestamp with timezone required for runtime observation")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("source", "runtime"))
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("release-manifest.json"))
    parser.add_argument("--checkout", type=Path)
    parser.add_argument("--runtime", type=Path, help="Sanitized observation of running services, never .env or .deploy-info")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text())
        errors = check_manifest(manifest)
        if not errors and args.mode == "source":
            errors = check_source(manifest, args.checkout.resolve()) if args.checkout else ["BASE-01: --checkout required"]
        elif not errors:
            errors = check_runtime(manifest, json.loads(args.runtime.read_text())) if args.runtime else [
                "BASE-02: runtime evidence missing", "BASE-05: backend SHA missing",
            ]
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        errors = ["Invalid or unreadable input; values omitted from output"]
    for error in errors:
        print(error)
    if not errors:
        print(f"PASS {args.mode}: supplied evidence matches manifest; this is not release acceptance")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
