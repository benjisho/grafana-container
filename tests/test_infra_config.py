from pathlib import Path


def test_grafana_admin_password_has_no_admin_fallback() -> None:
    compose = Path('docker-compose.yml').read_text()

    assert 'GF_SECURITY_ADMIN_PASSWORD' in compose
    assert 'GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD:?Set GRAFANA_ADMIN_PASSWORD in .env}' in compose
    password_line = next(
        line.strip()
        for line in compose.splitlines()
        if line.strip().startswith('GF_SECURITY_ADMIN_PASSWORD:')
    )

    assert ':-admin' not in password_line
