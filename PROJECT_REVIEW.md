# Project Review: Grafana + Nginx Container Stack

## Aim of this repository
The repository provides a simple, reproducible setup to run Grafana behind an HTTPS-terminating Nginx reverse proxy using Docker Compose.

## What was already done
- Docker Compose orchestration for Grafana and Nginx.
- HTTPS proxying with self-signed certificate instructions.
- Basic health checks and persistent Grafana storage.

## What was improved in this update
- Added `.env.example` so operators can configure credentials and hostname consistently.
- Hardened `docker-compose.yml`:
  - Added explicit Grafana bootstrap credentials via environment variables.
  - Required `GRAFANA_ADMIN_PASSWORD` semantics (`:?`) to avoid weak fallback defaults.
  - Added Grafana root URL/domain alignment for reverse-proxy correctness.
  - Added `depends_on` health condition so Nginx starts after Grafana is healthy.
  - Added `no-new-privileges` to both services.
  - Added `read_only` root filesystem and `tmpfs` mounts for Nginx runtime directories.
  - Improved health checks for both services.
- Hardened `nginx.conf`:
  - Added HTTP/2 on TLS listener.
  - Added websocket upgrade handling required by Grafana live features.
  - Added forwarding headers (`X-Forwarded-*`, client IP).
  - Kept modern TLS protocols and session settings.
  - Added additional security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`).
- CI/CD hardening:
  - CI runs repository behavior tests (`python -m unittest ...`) before integration checks.
  - CI no longer masks failures in critical validation steps (`nginx -t` and endpoint probes).
  - CI readiness check waits for container health status instead of fixed sleep.
  - CI teardown always runs (`if: always()`) and failure paths include container log dump.
  - CI now sets `GRAFANA_ADMIN_PASSWORD` so `docker compose config` succeeds with required-variable interpolation.
- Added regression tests that validate stack behavior and security invariants to protect refactors.

## What is still recommended / TODO
- Replace self-signed certificates with CA-issued certificates (Let's Encrypt or enterprise PKI) for production.
- Move secrets to Docker secrets, Vault, or runtime secret managers (instead of plain `.env`) for stronger secret hygiene.
- Add dependency/security scanning (e.g., Trivy/Grype) for container images.
- Pin all third-party GitHub Actions by full commit SHA for supply-chain hardening.
- Add backup/restore guidance for `grafana-storage` volume.
- Consider Grafana provisioning (datasources/dashboards as code) for reproducible environments.

## Online best-practice validation references checked
- Docker Compose variable interpolation and required-variable behavior (`:?`):
  - https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/
- Docker Compose dependency and health behavior:
  - https://docs.docker.com/compose/compose-file/05-services/#depends_on
- Grafana reverse-proxy and `root_url` guidance:
  - https://grafana.com/tutorials/run-grafana-behind-a-proxy/
  - https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#root_url
- Nginx reverse-proxy and websocket guidance:
  - https://nginx.org/en/docs/http/ngx_http_proxy_module.html
  - https://nginx.org/en/docs/http/websocket.html
- Mozilla TLS baseline reference:
  - https://ssl-config.mozilla.org/

## Current assessment
The branch is directionally correct and aligns with mainstream best practices for a small self-managed deployment. Remaining items are production-operability and supply-chain hardening tasks, not blockers for local/dev usage.
