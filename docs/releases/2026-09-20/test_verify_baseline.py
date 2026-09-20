"""Run with python3 -B -m unittest discover -s docs/releases/2026-09-20."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


HERE = Path(__file__).parent


class BaselineChecks(unittest.TestCase):
    def setUp(self):
        path = HERE / "verify_baseline.py"
        self.assertTrue(path.exists(), "baseline verifier is not implemented")
        spec = importlib.util.spec_from_file_location("verify_baseline", path)
        self.verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.verifier)
        self.manifest = json.loads((HERE / "release-manifest.json").read_text())

    def runtime(self):
        deployment = dict(
            environment="synthetic-test", frontendDeploymentId="build-7",
            frontendImageDigest="sha256:" + "a" * 64,
            backendImageDigest="sha256:" + "b" * 64,
            appliedMigrations=self.manifest["migrationFiles"], runtimeMode="workspace",
            nodeVersion="22.1.0", pnpmVersion="10.26.1", goVersion="1.24.3",
        )
        self.manifest["deployment"] = copy.deepcopy(deployment)
        return dict(deployment, frontendSha=self.manifest["repositories"]["frontend"]["sha"],
                    backendSha=self.manifest["repositories"]["backend"]["sha"],
                    observedAt="2026-09-20T12:00:00Z")

    def test_matching_runtime_passes_and_wrong_image_fails(self):
        runtime = self.runtime()
        self.assertEqual(self.verifier.check_runtime(self.manifest, runtime), [])
        runtime["backendImageDigest"] = "sha256:" + "c" * 64
        self.assertTrue(self.verifier.check_runtime(self.manifest, runtime))

    def test_unknown_backend_sha_is_explicit_blocker(self):
        runtime = self.runtime()
        runtime["backendSha"] = None
        self.assertIn("BASE-05: backend SHA missing", self.verifier.check_runtime(self.manifest, runtime))

    def test_runtime_cannot_pass_with_unknown_manifest_target(self):
        runtime = self.runtime()
        self.manifest["deployment"]["environment"] = None
        self.assertTrue(self.verifier.check_runtime(self.manifest, runtime))

    def test_wrong_revision_migrations_and_demo_are_rejected(self):
        runtime = self.runtime()
        for key, value in [("frontendSha", "0" * 40), ("appliedMigrations", []), ("runtimeMode", "demo")]:
            with self.subTest(key=key):
                self.assertTrue(self.verifier.check_runtime(self.manifest, dict(runtime, **{key: value})))

    def test_secret_fields_are_rejected_without_echoing_values(self):
        runtime = self.runtime()
        runtime["cookie"] = "synthetic-sensitive-value"
        errors = self.verifier.check_runtime(self.manifest, runtime)
        self.assertTrue(errors)
        self.assertNotIn("synthetic-sensitive-value", str(errors))

    def test_manifest_requires_exact_sha_and_env_names_only(self):
        self.assertEqual(self.verifier.check_manifest(self.manifest), [])
        self.manifest["repositories"]["frontend"]["sha"] = "develop"
        self.manifest["requiredEnvNames"].append("PASSWORD=synthetic-sensitive-value")
        errors = self.verifier.check_manifest(self.manifest)
        self.assertTrue(errors)
        self.assertNotIn("synthetic-sensitive-value", str(errors))

    def test_manifest_rejects_sensitive_fields_in_nested_objects(self):
        self.manifest["toolchain"]["accessToken"] = "synthetic-sensitive-value"
        errors = self.verifier.check_manifest(self.manifest)
        self.assertTrue(errors)
        self.assertNotIn("synthetic-sensitive-value", str(errors))

    def test_nested_deployment_value_cannot_pass_when_both_inputs_match(self):
        runtime = self.runtime()
        nested = {"accessToken": "synthetic-sensitive-value"}
        self.manifest["deployment"]["environment"] = nested
        runtime["environment"] = nested
        self.assertTrue(self.verifier.check_manifest(self.manifest))
        errors = self.verifier.check_runtime(self.manifest, runtime)
        self.assertTrue(errors)
        self.assertNotIn("synthetic-sensitive-value", str(errors))

    def test_scalar_schema_rejects_nested_branch_and_tool_versions(self):
        for section, key in [("toolchain", "pnpm"), ("deployment", "nodeVersion")]:
            with self.subTest(section=section):
                changed = copy.deepcopy(self.manifest)
                changed[section][key] = {"token": "synthetic-sensitive-value"}
                self.assertTrue(self.verifier.check_manifest(changed))
        self.manifest["repositories"]["frontend"]["branch"] = {"token": "synthetic-sensitive-value"}
        self.assertTrue(self.verifier.check_manifest(self.manifest))

    def test_source_rejects_dirty_checkout_and_wrong_pin(self):
        source = HERE.resolve().parents[2]
        with tempfile.TemporaryDirectory(prefix="fortis-baseline-test-") as directory:
            root = Path(directory) / "workspace"
            for name, repo in self.manifest["repositories"].items():
                relative = "." if name == "parent" else name
                subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", "--no-checkout",
                                str(source / relative), str(root / relative)], check=True)
                subprocess.run(["git", "-C", str(root / relative), "checkout", "--quiet",
                                "--detach", repo["sha"]], check=True)
            self.assertEqual(self.verifier.check_source(self.manifest, root), [])
            marker = root / "frontend" / "frc00-synthetic-change"
            marker.write_text("synthetic\n")
            self.assertIn("BASE-01: frontend worktree is not clean", self.verifier.check_source(self.manifest, root))
            marker.unlink()
            self.manifest["repositories"]["frontend"]["sha"] = "0" * 40
            errors = self.verifier.check_source(self.manifest, root)
            self.assertIn("BASE-01: frontend checkout SHA mismatch", errors)
            self.assertIn("BASE-01: frontend parent gitlink mismatch", errors)


if __name__ == "__main__":
    unittest.main()
