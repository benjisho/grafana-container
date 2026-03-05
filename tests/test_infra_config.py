import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class TestComposeConfiguration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compose_text = (REPO_ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    def test_services_exist(self):
        self.assertIn("grafana:", self.compose_text)
        self.assertIn("nginx:", self.compose_text)

    def test_grafana_admin_password_has_required_variable_semantics(self):
        match = re.search(r"(?m)^\s+GF_SECURITY_ADMIN_PASSWORD:\s*(.+)$", self.compose_text)
        self.assertIsNotNone(match)
        expression = match.group(1)
        self.assertIn(":?", expression)
        self.assertNotIn(":-", expression)

    def test_grafana_healthcheck_uses_api_health(self):
        self.assertIn("/api/health", self.compose_text)

    def test_nginx_waits_for_grafana_health(self):
        self.assertRegex(
            self.compose_text,
            r"depends_on:\n\s+grafana:\n\s+condition:\s+service_healthy",
        )

    def test_no_new_privileges_for_services(self):
        occurrences = self.compose_text.count("no-new-privileges:true")
        self.assertGreaterEqual(occurrences, 2)

    def test_nginx_runtime_filesystem_hardening_present(self):
        self.assertIn("read_only: true", self.compose_text)
        self.assertIn("tmpfs:", self.compose_text)
        self.assertIn("/var/cache/nginx", self.compose_text)
        self.assertIn("/var/run", self.compose_text)


class TestNginxConfiguration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nginx_text = (REPO_ROOT / "nginx.conf").read_text(encoding="utf-8")

    def test_https_redirect_enabled(self):
        self.assertIn("return 301 https://$host$request_uri;", self.nginx_text)

    def test_secure_tls_versions_only(self):
        self.assertIn("ssl_protocols TLSv1.2 TLSv1.3;", self.nginx_text)

    def test_mozilla_intermediate_session_settings_present(self):
        self.assertIn("ssl_session_timeout 1d;", self.nginx_text)
        self.assertIn("ssl_session_cache shared:MozSSL:10m;", self.nginx_text)

    def test_http2_and_ipv6_listeners_configured(self):
        self.assertIn("listen [::]:443 ssl;", self.nginx_text)
        self.assertIn("http2 on;", self.nginx_text)

    def test_websocket_and_forwarding_proxy_headers_configured(self):
        self.assertIn("proxy_set_header Upgrade $http_upgrade;", self.nginx_text)
        self.assertIn("proxy_set_header Connection $connection_upgrade;", self.nginx_text)
        self.assertIn("proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;", self.nginx_text)
        self.assertIn("proxy_set_header X-Forwarded-Proto https;", self.nginx_text)

    def test_security_headers_present(self):
        required_headers = [
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Referrer-Policy",
        ]
        for header in required_headers:
            with self.subTest(header=header):
                self.assertIn(header, self.nginx_text)


class TestCiBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow_text = (
            REPO_ROOT / ".github/workflows/grafana-docker-compose-ci.yml"
        ).read_text(encoding="utf-8")

    def test_ci_uses_least_privilege_permissions(self):
        self.assertRegex(self.workflow_text, r"(?m)^permissions:\n\s+contents:\s+read$")

    def test_ci_runs_repository_behavior_tests(self):
        self.assertIn("python -m unittest discover -s tests -p 'test_*.py'", self.workflow_text)

    def test_ci_sets_required_compose_env_for_grafana_password(self):
        self.assertIn("GRAFANA_ADMIN_PASSWORD: ci-test-admin-password", self.workflow_text)

    def test_ci_does_not_soft_fail_critical_checks(self):
        self.assertNotIn("|| true", self.workflow_text)

    def test_ci_waits_for_service_health_without_fixed_sleep(self):
        self.assertIn("docker inspect --format=", self.workflow_text)

    def test_ci_has_always_cleanup(self):
        self.assertIn("if: always()", self.workflow_text)
        self.assertIn("docker compose down -v --remove-orphans", self.workflow_text)


if __name__ == "__main__":
    unittest.main()
