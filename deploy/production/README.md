# Fortis production deploy

Release provenance: see [FRC-00](../../docs/releases/2026-09-20/acceptance-matrix.md).
`write-deploy-info.sh` records the actual checkout SHA and dirty flag for parent,
frontend, backend and knowledge-base. It does not inspect running containers or
prove their image digest, deployment ID or applied migrations. Do not use
`.deploy-info` as runtime evidence or include `.env` values in release artifacts.

Target VM for the first dev deployment:

- public IP: `85.208.87.187`
- SSH user: `user1`
- OS: Ubuntu 24.04
- local SSH alias: `fortis-dev-vm`

Make sure the cloud firewall/security group allows inbound TCP `80` and `443`
from the internet. The VM can serve the app on its private interface, but the
public IP will time out while the provider-level rule is closed.

## What runs

- `postgres`: PostgreSQL 17 with persistent Docker volume.
- `backend`: Go API on internal `:8090`, migrations run on app startup.
- `frontend`: Next.js on loopback `${FRONTEND_HOST_PORT:-3000}`, proxying API calls to `backend`.
- `nginx`: host reverse proxy on public `80` and `443`, forwarding to `127.0.0.1:3000`.

## First server setup

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl git nginx openssl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"
```

Log out and SSH back in after adding the user to the `docker` group.

## Deploy from this workspace

Copy the repository to the server:

```bash
ssh user1@85.208.87.187 'mkdir -p ~/fortis'
rsync -az --delete --exclude '.git/' --exclude 'vendor/' backend/ user1@85.208.87.187:~/fortis/backend/
rsync -az --delete --exclude '.git/' --exclude 'node_modules/' --exclude '.next/' --exclude 'test-results/' --exclude 'output/' frontend/ user1@85.208.87.187:~/fortis/frontend/
rsync -az --delete --exclude 'production/.env' deploy/ user1@85.208.87.187:~/fortis/deploy/
```

If the local SSH alias is configured, `ssh fortis-dev-vm` can be used instead
of `ssh user1@85.208.87.187`.

Then on the server:

```bash
cd ~/fortis/deploy/production
cp .env.example .env
```

Edit `.env` and set real values for `POSTGRES_PASSWORD` and `APP_AUTH_JWTSECRET`.
For Telegram build notifications, also set `DEPLOY_NOTIFY_WEBHOOK_URL`. This URL
points to the Cloudflare Worker proxy because the dev VM cannot call Telegram
API directly from the Russian network:

```env
DEPLOY_NOTIFY_WEBHOOK_URL=https://fortis-build-telegram.galyamdin.workers.dev/deploy/<secret>
```

```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
  -keyout /etc/nginx/ssl/fortis-selfsigned.key \
  -out /etc/nginx/ssl/fortis-selfsigned.crt \
  -subj "/CN=85.208.87.187" \
  -addext "subjectAltName=IP:85.208.87.187"
sudo install -m 0644 nginx.conf /etc/nginx/sites-available/default
sudo nginx -t
sudo systemctl enable --now nginx
./deploy-with-notify.sh
docker compose --env-file .env ps
docker compose --env-file .env exec backend wget -qO- http://127.0.0.1:8090/_/liveness
```

`deploy-with-notify.sh` sends deploy events to the Worker when deploy starts,
succeeds, or fails. Success is sent only after Docker Compose finishes and both
backend and frontend healthchecks respond inside the Compose network.

Public frontend URL:

```text
http://85.208.87.187/
```

HTTPS on the raw IP uses the self-signed certificate above until a real domain
and certificate are attached.


## FRC-01 runtime configuration and probes

The frontend reads configuration at process runtime. Build arguments no longer choose
backend or demo mode. Set `FORTIS_RUNTIME_MODE=workspace`, `BACKEND_URL=http://backend:8090`
and `FORTIS_BACKEND_PRIVATE_HTTP=true` in the private Compose network. Optional URL
aliases must normalize to the same target; missing/conflicting workspace configuration
returns 503, without a remote fallback. External traffic must use HTTPS. This code
change does not verify the VM certificate or network isolation.

`FORTIS_API_TIMEOUT_MS` defaults to 10000, `FORTIS_DOCUMENT_TIMEOUT_MS` to 30000
(valid range 1–120000). Explicit local development may use
`FORTIS_LOCAL_DEVELOPMENT=true` with `NODE_ENV=development` for localhost fallback.
Do not use that fallback for production. `FORTIS_RUNTIME_MODE=demo` explicitly enables
marked demo routes and disables canonical backend operations; URL queries cannot do so.

- Backend `/_/liveness`: process only; `/_/readiness`: database ping, deadline 2 seconds.
- Frontend `/api/health/live`: process only; `/api/health/ready`: runtime config and backend readiness in workspace.
- Frontend Compose healthcheck uses **live**, so a backend outage does not mark the frontend process dead. Backend healthcheck and startup dependency use backend readiness.
- A successful Compose/deploy healthcheck alone is no longer proof of frontend dependency readiness. Check `/api/health/ready` separately for traffic admission; do not wire it to frontend restart policy.

Deployment was not executed for FRC-01. See [implementation evidence](../../docs/releases/2026-09-20/frc01/implementation-report.md) and [ADR-0016](../../knowledge-base/03_Architecture/ADR-0016-runtime-backend-boundary.md).
