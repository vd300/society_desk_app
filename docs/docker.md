# Docker

This repo includes Dockerfiles for the backend and frontend, plus
`docker-compose.yml` for local full-stack runs.

## Run Everything

From the repository root:

```bash
docker compose up --build
```

Open:

```text
Frontend: http://localhost:3000/login
Backend:  http://localhost:8000/health
API docs: http://localhost:8000/docs
```

## Seed Data

In another terminal:

```bash
docker compose exec backend python scripts/seed.py
```

Seed password:

```text
password123
```

## Services

- `db`: PostgreSQL 16
- `backend`: FastAPI, Alembic migration on startup, Uvicorn
- `frontend`: Next.js production server

## Notes

The compose file uses local development credentials. Change
`JWT_SECRET_KEY`, database passwords, and CORS/API URLs before using these
images in production.
