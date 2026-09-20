#!/usr/bin/env python3
"""Check combined FE/BE publication configuration without printing any values.

Run in a protected release job with both servers' configuration available.
This is configuration evidence, not proof of SMTP delivery, policy approval or ingress trust.
"""
import ipaddress
import os
from urllib.parse import urlsplit


def check(env):
    frontend = env.get("FORTIS_DEMO_REQUESTS_ENABLED") == "true"
    backend = env.get("APP_DEMO_ENABLED") == "true"
    if not frontend and not backend:
        return []
    errors = []
    if not frontend or not backend:
        errors.append("intake must be enabled consistently on both servers")
    required = ["FORTIS_DEMO_FORM_ORIGIN", "FORTIS_DEMO_CONSENT_VERSION", "FORTIS_DEMO_CONSENT_TEXT",
                "FORTIS_TRUSTED_CLIENT_IP_HEADER", "APP_DEMO_ALLOWED_ORIGINS", "APP_DEMO_CONSENT_VERSIONS",
                "APP_DEMO_TRUSTED_PROXY_CIDRS", "APP_DEMO_SMTP_ADDRESS", "APP_DEMO_SMTP_FROM", "APP_DEMO_SMTP_TO"]
    for key in required:
        if not env.get(key, "").strip():
            errors.append("missing " + key)
    origin = env.get("FORTIS_DEMO_FORM_ORIGIN", "")
    try:
        parsed = urlsplit(origin)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password or origin != f"https://{parsed.netloc}":
            errors.append("production form origin must be an exact HTTPS origin")
    except ValueError:
        errors.append("invalid form origin")
    if origin not in env.get("APP_DEMO_ALLOWED_ORIGINS", "").split(","):
        errors.append("backend origin allowlist does not match the form")
    if env.get("FORTIS_DEMO_CONSENT_VERSION", "") not in env.get("APP_DEMO_CONSENT_VERSIONS", "").split(","):
        errors.append("backend consent allowlist does not match the form")
    try:
        for value in env.get("APP_DEMO_TRUSTED_PROXY_CIDRS", "").split(","):
            network = ipaddress.ip_network(value)
            if network.prefixlen == 0:
                errors.append("trusting all proxy peers is not an accepted ingress boundary")
    except ValueError:
        errors.append("invalid trusted proxy CIDR configuration")
    if bool(env.get("APP_DEMO_SMTP_USERNAME")) != bool(env.get("APP_DEMO_SMTP_PASSWORD")):
        errors.append("incomplete SMTP credential pair")
    return errors


if __name__ == "__main__":
    failures = check(os.environ)
    print("\n".join("BLOCKED: " + error for error in failures) if failures else "PASS: publication configuration gate (runtime/owner evidence still required)")
    raise SystemExit(bool(failures))
