Perfect — this final **Part 4: Documentation** is where you pull together everything you built so far (local setup, Docker, CI/CD, etc.) into a clean, professional **`README.md`** for the assignment repo.

Below is a **ready-to-use full documentation template**, customized for your project `dummy-branch-app-om` (Branch Loan API).
You can copy this directly into your repo root as `README.md`.

---

# 🏦 Branch Loan API — DevOps Take-Home Assignment

This project is a containerized **loan API service** with a fully automated **CI/CD pipeline** using GitHub Actions and GitHub Container Registry (GHCR).
It demonstrates **local development with Docker Compose**, **Alembic migrations**, and **automated build + scan + deploy** workflow.

---

## 🚀 Part 1: Run Application Locally

### 🧩 Prerequisites

| Tool           | Version | Notes                                  |
| -------------- | ------- | -------------------------------------- |
| Docker Desktop | ≥ 4.30  | Ensure Linux container mode            |
| Docker Compose | v2.x    | Comes with Docker Desktop              |
| Git            | Latest  | For cloning repo                       |
| Python         | ≥ 3.11  | (optional) for running scripts locally |

---

### 📂 1️⃣ Clone Repository

```bash
git clone https://github.com/omsre/dummy-branch-app-om.git
cd dummy-branch-app-om
```

---

### ⚙️ 2️⃣ Environment Setup

Copy the sample `.env` file:

```bash
cp .env.dev.example .env.dev
```

or if the repo already includes `.env.dev`, review and edit:

```bash
POSTGRES_USER=branch_user
POSTGRES_PASSWORD=branch_pass
POSTGRES_DB=branch_loans
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

**Never commit `.env.*` files.**
They are ignored by `.gitignore` via:

```
.env.*
infra/certs/
```

---

### 🐳 3️⃣ Start Containers

```bash
docker compose --env-file .env.dev up -d --build
```

This starts:

* `db` → PostgreSQL database
* `api` → FastAPI backend
* `nginx` → HTTPS reverse proxy with self-signed certificate

Check container status:

```bash
docker compose ps
```

---

### 🧰 4️⃣ Database Migrations & Seed

```bash
# Apply Alembic migrations
docker compose --env-file .env.dev exec api alembic upgrade head

# Seed database (idempotent)
docker compose --env-file .env.dev exec api python scripts/seed.py
```

---

### 🔒 5️⃣ Verify HTTPS

#### Browser

Visit:

```
https://branchloans.com
```

You’ll see a warning (self-signed cert). Accept and continue.

#### CLI

On Windows PowerShell:

```bash
curl.exe -k https://branchloans.com/health
```

Expected output:

```
{"status":"ok"}
```

---

## 🌐 Switching Environments

You can maintain multiple `.env` files:

```
.env.dev
.env.staging
.env.prod
```

Run Compose with any environment:

```bash
docker compose --env-file .env.staging up -d
```

---

## 🔧 Environment Variables Explained

| Variable            | Description                     | Example                    |
| ------------------- | ------------------------------- | -------------------------- |
| `POSTGRES_USER`     | DB username                     | `branch_user`              |
| `POSTGRES_PASSWORD` | DB password                     | `branch_pass`              |
| `POSTGRES_DB`       | Database name                   | `branch_loans`             |
| `POSTGRES_HOST`     | Hostname (container name of DB) | `db`                       |
| `POSTGRES_PORT`     | Port of PostgreSQL              | `5432`                     |
| `APP_ENV`           | Current environment             | `dev` / `staging` / `prod` |
| `SECRET_KEY`        | JWT or app secret               | *not committed*            |
| `NGINX_HOST`        | Domain used for HTTPS proxy     | `branchloans.com`          |

---

## ⚙️ CI/CD Pipeline (GitHub Actions)

### 📁 Workflow File

`.github/workflows/ci-cd.yml`

### 🧱 Stages

| Stage     | Purpose                                | Key Action                  |
| --------- | -------------------------------------- | --------------------------- |
| **Test**  | Detect & run Python tests if present   | `pytest`                    |
| **Build** | Build Docker image tagged with Git SHA | `docker build`              |
| **Scan**  | Run Trivy vulnerability scan           | `aquasecurity/trivy-action` |
| **Push**  | Push image to GHCR (main branch only)  | `docker push ghcr.io/...`   |

---

### ⚡ Trigger Conditions

* On **push** to `main`
* On **pull request** → runs tests + build + scan but **no push**

---

### 🧩 Secrets and Permissions

| Secret                                     | Description                                        |
| ------------------------------------------ | -------------------------------------------------- |
| `GITHUB_TOKEN`                             | Default GitHub-provided token (used for GHCR push) |
| `DOCKER_HUB_USERNAME` / `DOCKER_HUB_TOKEN` | *(optional)* if using Docker Hub                   |
| `.env.*`                                   | Local env config (ignored by git)                  |

---

## 🏗️ Architecture Diagram

```
                        ┌────────────────────────────┐
                        │     Developer Machine      │
                        │  (Docker Compose + VSCode) │
                        └──────────────┬─────────────┘
                                       │
                    docker compose build/run
                                       │
        ┌──────────────────────────────────────────────────┐
        │                Docker Network                    │
        │                                                  │
        │  ┌──────────────┐     ┌──────────────┐           │
        │  │   nginx      │ ◀──▶│     api      │           │
        │  │ (TLS Proxy)  │     │ (FastAPI)    │           │
        │  └──────────────┘     └──────────────┘           │
        │                        │                         │
        │                        ▼                         │
        │                 ┌──────────────┐                 │
        │                 │     db       │ (Postgres)      │
        │                 └──────────────┘                 │
        └──────────────────────────────────────────────────┘

                CI/CD → GitHub Actions → Build → Scan → Push → GHCR
```

---

## 🧠 Design Decisions

### ✅ Why Docker Compose

* Simplifies multi-service orchestration (API + DB + Nginx)
* Same config runs on all machines

### ✅ Why GHCR

* Native to GitHub → uses `GITHUB_TOKEN`
* Simplifies auth and permissions
* Free private image hosting

### ✅ Why Trivy

* Lightweight open-source image scanner
* Easy to integrate in GitHub Actions

---

### ⚖️ Trade-Offs

| Choice                                | Trade-Off                                              |
| ------------------------------------- | ------------------------------------------------------ |
| **Self-signed cert**                  | Browser warning in dev, but no cost                    |
| **Single environment Docker Compose** | Simple but not scalable for multi-cluster prod         |
| **Manual DB seed**                    | Simpler for test data, but not suitable for prod scale |

---

### 🚀 Future Improvements

* Add deployment stage → deploy image to AWS ECS or Kubernetes
* Automate SSL using Let’s Encrypt in staging/prod
* Add automated Alembic migrations in CI pipeline
* Add unit tests for routes and DB models

---

## 🧩 Troubleshooting

| Problem                                        | Possible Cause               | Solution                                                                          |
| ---------------------------------------------- | ---------------------------- | --------------------------------------------------------------------------------- |
| `unauthorized: incorrect username or password` | Docker not logged in         | `docker login` before compose                                                     |
| DNS error like `no such host`                  | Corporate/ISP DNS blocking   | Add `"dns": ["8.8.8.8", "1.1.1.1"]` to `C:\ProgramData\Docker\config\daemon.json` |
| `ModuleNotFoundError: No module named 'app'`   | Python path missing          | Add `WORKDIR /app` and `ENV PYTHONPATH=/app` to Dockerfile                        |
| HTTPS 404                                      | Nginx routing not configured | Check `nginx.conf` → `proxy_pass http://api:8000;`                                |
| CI build fails to push                         | Missing checkout before push | Ensure `actions/checkout@v4` in push job                                          |
| Trivy scan fails                               | DB too large / slow          | Add `--scanners vuln` or increase timeout                                         |

---

## 🧾 Health Check

To confirm services:

```bash
docker compose ps
curl.exe -k https://branchloans.com/health
```

Expected:

```
{"status": "ok"}
```

Check logs:

```bash
docker compose logs -f api
```

---

## 📚 References

* [Docker Docs](https://docs.docker.com/)
* [GitHub Actions](https://docs.github.com/en/actions)
* [Trivy Docs](https://aquasecurity.github.io/trivy)
* [Alembic Docs](https://alembic.sqlalchemy.org/)
* [FastAPI Docs](https://fastapi.tiangolo.com/)

---

### 🏁 Summary

✅ Local Docker Compose setup
✅ HTTPS via Nginx (self-signed)
✅ Database migrations + seed
✅ CI/CD: Test → Build → Scan → Push
✅ Documentation with troubleshooting and design notes

---

Would you like me to include a **diagram image (.png)** version of the ASCII architecture (which you can add under `docs/architecture.png` and reference in README)? I can generate that next for you.
