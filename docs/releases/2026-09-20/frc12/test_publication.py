import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("publication", Path(__file__).with_name("check_publication.py"))
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)


class PublicationTests(unittest.TestCase):
    def test_disabled_and_partial_configuration(self):
        self.assertEqual(publication.check({}), [])
        errors = publication.check({"FORTIS_DEMO_REQUESTS_ENABLED": "true"})
        self.assertTrue(any("SMTP" in error for error in errors))
        self.assertTrue(any("CONSENT_TEXT" in error for error in errors))

    def test_configuration_consistency_and_no_value_disclosure(self):
        env = dict(FORTIS_DEMO_REQUESTS_ENABLED="true", APP_DEMO_ENABLED="true",
            FORTIS_DEMO_FORM_ORIGIN="https://workspace.example.test", APP_DEMO_ALLOWED_ORIGINS="https://workspace.example.test",
            FORTIS_DEMO_CONSENT_VERSION="synthetic-v1", APP_DEMO_CONSENT_VERSIONS="synthetic-v1",
            FORTIS_DEMO_CONSENT_TEXT="synthetic fixture only", FORTIS_TRUSTED_CLIENT_IP_HEADER="x-edge-client-ip",
            APP_DEMO_TRUSTED_PROXY_CIDRS="10.1.0.0/24", APP_DEMO_SMTP_ADDRESS="smtp.example.test:587",
            APP_DEMO_SMTP_FROM="test@example.test", APP_DEMO_SMTP_TO="operator@example.test")
        self.assertEqual(publication.check(env), [])
        env["APP_DEMO_CONSENT_VERSIONS"] = "other"
        env["APP_DEMO_SMTP_PASSWORD"] = "never-print-this"
        errors = publication.check(env)
        self.assertTrue(any("consent" in error for error in errors))
        self.assertTrue(any("credential" in error for error in errors))
        self.assertNotIn("never-print-this", str(errors))


if __name__ == "__main__":
    unittest.main()
