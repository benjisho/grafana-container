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
  - Added Grafana root URL/domain alignment for reverse-proxy correctness.
  - Updated Nginx image to a maintained modern release (`1.27.5-alpine`).
  - Added `depends_on` health condition so Nginx starts after Grafana is healthy.
  - Added `no-new-privileges` to both services.
  - Added `read_only` root filesystem and `tmpfs` mounts for Nginx runtime directories.
  - Improved health checks for both services.
- Hardened `nginx.conf`:
  - Added HTTP/2 on TLS listener.
  - Added websocket upgrade handling required by Grafana live features.
  - Added forwarding headers (`X-Forwarded-*`, client IP).
  - Kept modern TLS protocols and reduced cipher list to modern AEAD suites.
  - Added additional security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`).
- Added tests that validate stack behavior and security invariants to protect refactors.

## What is still recommended / TODO
- Replace self-signed certificates with CA-issued certificates (Let's Encrypt or enterprise PKI) for production.
- Move secrets to Docker secrets, Vault, or runtime secret managers (instead of plain `.env`) for stronger secret hygiene.
- Add CI pipeline running:
  - `python -m unittest discover -s tests -p 'test_*.py'`
  - `docker compose config`
  - optional containerized `nginx -t` check against mounted config.
- Consider Grafana provisioning (datasources/dashboards as code) for reproducible environments.
- Add backup/restore guidance for `grafana-storage` volume.

## Online best-practice validation references checked
- Docker Compose specification and health/dependency behavior.
- Grafana Docker deployment and reverse proxy guidance.
- Nginx TLS and reverse proxy header recommendations.

(These references were used to guide the config hardening choices above.)
