# SocietyDesk

SocietyDesk is a FastAPI + Next.js MVP for apartment society operations:
maintenance dues, complaints, notices, visitor logs, role-based dashboards, and
local seed data.

## Project Layout

```text
backend/   FastAPI API, SQLAlchemy models, Alembic migrations, tests
frontend/  Next.js app router frontend with Tailwind CSS
docs/      Documentation placeholder
```

## Backend

```powershell
cd backend
Copy-Item .env.example .env
python -m pip install -e .
alembic upgrade head
python scripts/seed.py
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Seed users:

```text
admin@societydesk.com
security@societydesk.com
resident1@societydesk.com
resident2@societydesk.com
resident3@societydesk.com
```

Password: `password123`

## Frontend

```powershell
cd frontend
Copy-Item .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000/login`.

## Verification

```powershell
cd backend
pytest
```

```powershell
cd frontend
npm run build
```

## Render Deployment

This repo includes a Render Blueprint at `render.yaml` for:

- FastAPI backend: `societydesk-api`
- Next.js frontend: `societydesk-web`
- Render Postgres: `societydesk-db`

Deploy from Render by creating a new Blueprint from this repository. Render will
prompt for `JWT_SECRET_KEY`.

More details are in `docs/render.md`.
