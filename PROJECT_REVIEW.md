# Project Review: Grafana + Nginx Container Stack

## Aim of this repository
The repository provides a simple, reproducible setup to run Grafana behind an HTTPS-terminating Nginx reverse proxy using Docker Compose.

## What was already done
- Docker Compose orchestration for Grafana and Nginx.
- HTTPS proxying with self-signed certificate instructions.
- Basic health checks and persistent Grafana storage.

## What was improved in this branch (preserve)
- Added `.env.example` so operators can configure credentials and hostname consistently.
- Hardened `docker-compose.yml`:
  - Explicit Grafana bootstrap credentials via environment variables.
  - Required password semantics for `GRAFANA_ADMIN_PASSWORD` (no weak default fallback).
  - Grafana root URL/domain alignment for reverse-proxy correctness.
  - `depends_on` health condition so Nginx starts after Grafana is healthy.
  - `no-new-privileges` for both services.
  - `read_only` root filesystem and `tmpfs` mounts for Nginx runtime directories.
  - Health checks for both services.
- Hardened `nginx.conf`:
  - HTTP/2 on TLS listener and HTTP→HTTPS redirect.
  - WebSocket upgrade handling required by Grafana Live features.
  - Forwarding headers (`X-Forwarded-*`, client IP).
  - Modern TLS protocol and session settings.
  - Additional security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`).
- CI hardening:
  - Runs repository behavior tests (`python -m unittest ...`) before integration checks.
  - No masking of failures on critical validation/probe steps.
  - Readiness check waits for container health status (instead of fixed sleep).
  - Teardown always runs (`if: always()`), with logs available on failures.
- Added regression tests that validate stack behavior and security invariants to protect refactors.

## What still needs to be done / edited to fit long-term production use
- Replace self-signed certificates with CA-issued certificates (Let’s Encrypt or enterprise PKI).
- Move secrets to Docker secrets, Vault, or runtime secret managers (instead of plain `.env`).
- Add dependency/image scanning in CI (e.g., Trivy/Grype).
- Pin third-party GitHub Actions by full commit SHA for supply-chain hardening.
- Add backup/restore guidance for `grafana-storage` volume.
- Consider Grafana provisioning (datasources/dashboards as code) for reproducible environments.

## Online best-practice validation references checked
- Docker Compose variable interpolation and required-variable behavior (`:?`):
  - https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/
- Docker Compose dependency + health behavior:
  - https://docs.docker.com/compose/compose-file/05-services/#depends_on
- Grafana reverse proxy and `root_url` guidance:
  - https://grafana.com/tutorials/run-grafana-behind-a-proxy/
  - https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#root_url
- Nginx reverse proxy and websocket guidance:
  - https://nginx.org/en/docs/http/ngx_http_proxy_module.html
  - https://nginx.org/en/docs/http/websocket.html
- Mozilla TLS baseline reference:
  - https://ssl-config.mozilla.org/

## Current assessment
The branch is directionally correct and aligns with mainstream best practices for a small self-managed deployment. Remaining items are production-operability and supply-chain hardening tasks, not blockers for local/dev usage.
