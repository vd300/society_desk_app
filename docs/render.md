# Render Deployment

This repository is prepared for Render Blueprint deployment with `render.yaml`.

## Services

- `societydesk-api`: FastAPI backend
- `societydesk-web`: Next.js frontend
- `societydesk-db`: Render Postgres database

## Deploy

1. Push this repository to GitHub or GitLab.
2. In Render, create a new Blueprint from the repository.
3. Render uses the root `render.yaml` file automatically.
4. Provide `JWT_SECRET_KEY` when prompted.

Use a strong value for `JWT_SECRET_KEY`, for example a 32+ character random string.

## Backend

Render runs:

```text
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Health check:

```text
https://societydesk-api.onrender.com/health
```

If Render requires you to rename a service because the subdomain is already taken,
update these environment variables:

- Backend `CORS_ORIGINS`
- Frontend `NEXT_PUBLIC_API_BASE_URL`

## Seed Data

After the first backend deploy, run this one-off shell command from the backend
service shell:

```bash
python scripts/seed.py
```

Seed password: `password123`

## File Uploads

The blueprint stores uploads under `/tmp/societydesk-uploads`, which is suitable
for MVP testing but not persistent across restarts. For production file
persistence, add a Render disk on a paid service or switch uploads to Cloudinary
or Supabase Storage.
