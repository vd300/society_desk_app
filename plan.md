# SocietyDesk — MVP Plan

## 1. MVP Scope

The MVP will include:

1. Authentication and role-based access
2. Admin dashboard
3. Resident dashboard
4. Security dashboard
5. Society, building, flat, and resident setup
6. Maintenance due generation and payment proof verification
7. Complaint management
8. Notice publishing
9. Visitor management
10. Basic dashboard statistics

The goal is to build a deployable web application quickly without complex cloud infrastructure.

## 2. Recommended Tech Stack

## Backend

Use FastAPI.

Reasons:

- Simple and fast API development
- Strong typing with Pydantic
- Good for role-based systems
- Easy integration with PostgreSQL
- Easy deployment on Render, Railway, or Fly.io

## Frontend

Use Next.js with TypeScript.

Reasons:

- Good dashboard experience
- Easy deployment on Vercel
- Supports server-side and client-side rendering
- Strong ecosystem
- Works well with Tailwind CSS and shadcn/ui

## Database

Use PostgreSQL.

Reasons:

- Strong relational modeling
- Good for societies, flats, residents, dues, payments, complaints, and visitors
- Easy to host on Supabase, Neon, Railway, or Render

## ORM

Use SQLAlchemy or SQLModel.

Recommended for this project: SQLAlchemy 2.0.

Reasons:

- Mature
- Flexible
- Production-ready
- Works well with Alembic migrations

## Authentication

Use JWT-based authentication.

- Access token for API requests
- Password hashing using bcrypt
- Role stored on user table

## File Storage

For MVP:

- Use local storage during development.
- Use Cloudinary or Supabase Storage for deployment.

Files needed:

- Payment proof screenshots
- Complaint images

## Deployment

Simple deployment approach:

- Frontend: Vercel
- Backend: Render or Railway
- Database: Neon or Supabase Postgres
- File storage: Cloudinary or Supabase Storage

Avoid AWS for MVP.

## 3. High-Level Architecture

```text
User Browser
    |
    v
Next.js Frontend
    |
    v
FastAPI Backend
    |
    v
PostgreSQL Database

Optional:
FastAPI Backend -> Cloudinary/Supabase Storage for uploaded files
```

## 4. Main Roles

## Admin

Can manage:

- Society setup
- Buildings
- Flats
- Residents
- Maintenance dues
- Payment verification
- Complaints
- Notices
- Visitor logs

## Resident

Can manage:

- Own dues
- Own payment submissions
- Own complaints
- Own expected visitors
- View notices

## Security

Can manage:

- Expected visitors
- Walk-in visitors
- Visitor check-in
- Visitor check-out

## 5. Suggested Folder Structure

## Backend

```text
backend/
  app/
    main.py
    core/
      config.py
      security.py
      database.py
    models/
      user.py
      society.py
      building.py
      flat.py
      resident.py
      maintenance_due.py
      payment.py
      complaint.py
      notice.py
      visitor.py
    schemas/
      auth.py
      user.py
      society.py
      flat.py
      maintenance_due.py
      complaint.py
      notice.py
      visitor.py
    api/
      routes/
        auth.py
        admin.py
        residents.py
        dues.py
        complaints.py
        notices.py
        visitors.py
    services/
      auth_service.py
      due_service.py
      complaint_service.py
      visitor_service.py
    repositories/
      user_repository.py
      due_repository.py
      complaint_repository.py
    migrations/
  tests/
  pyproject.toml
  .env.example
```

## Frontend

```text
frontend/
  app/
    login/
    admin/
      dashboard/
      flats/
      residents/
      dues/
      complaints/
      notices/
      visitors/
    resident/
      dashboard/
      dues/
      complaints/
      notices/
      visitors/
    security/
      dashboard/
      visitors/
  components/
    ui/
    layout/
    forms/
    tables/
  lib/
    api.ts
    auth.ts
    types.ts
  .env.example
  package.json
```

## 6. Database Design

Core tables:

- users
- societies
- buildings
- flats
- residents
- maintenance_dues
- payments
- complaints
- notices
- visitors

Optional later tables:

- vendors
- parking_slots
- documents
- audit_logs
- notification_logs

## 7. API Design

## Auth APIs

```text
POST /auth/login
POST /auth/register
GET  /auth/me
```

## Admin APIs

```text
GET  /admin/dashboard
POST /admin/buildings
GET  /admin/buildings
POST /admin/flats
GET  /admin/flats
POST /admin/residents
GET  /admin/residents
```

## Maintenance APIs

```text
POST /dues/generate
GET  /dues
GET  /dues/my
POST /dues/{due_id}/submit-payment
POST /dues/{due_id}/approve
POST /dues/{due_id}/reject
```

## Complaint APIs

```text
POST /complaints
GET  /complaints
GET  /complaints/my
PATCH /complaints/{complaint_id}/status
```

## Notice APIs

```text
POST /notices
GET  /notices
GET  /notices/active
```

## Visitor APIs

```text
POST /visitors/expected
POST /visitors/walk-in
GET  /visitors/today
POST /visitors/{visitor_id}/check-in
POST /visitors/{visitor_id}/check-out
GET  /visitors/logs
```

## 8. Frontend Pages

## Public

```text
/login
```

## Admin

```text
/admin/dashboard
/admin/flats
/admin/residents
/admin/dues
/admin/complaints
/admin/notices
/admin/visitors
```

## Resident

```text
/resident/dashboard
/resident/dues
/resident/complaints
/resident/notices
/resident/visitors
```

## Security

```text
/security/dashboard
/security/visitors
```

## 9. Development Strategy

Build in this order:

1. Backend project setup
2. Database setup
3. User authentication
4. Role-based route protection
5. Society/building/flat/resident setup
6. Maintenance dues
7. Complaint management
8. Notices
9. Visitor management
10. Dashboards
11. Frontend integration
12. Deployment

## 10. Design Principle

Keep the MVP simple.

Do not build a massive product in version one.

The first goal is:

A small society committee should be able to use this app instead of Excel and WhatsApp for basic operations.
