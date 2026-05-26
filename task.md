# SocietyDesk — MVP Task Breakdown

## Phase 1 — Project Setup

## Task 1.1 — Create Repository Structure

Create the project structure:

```text
societydesk/
  backend/
  frontend/
  docs/
```

Acceptance Criteria:

- Backend folder exists.
- Frontend folder exists.
- Docs folder exists.
- README file exists.

## Task 1.2 — Setup Backend

Set up FastAPI backend.

Acceptance Criteria:

- FastAPI app starts successfully.
- Health check endpoint works.
- Environment variables are loaded from `.env`.

Suggested endpoint:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

## Task 1.3 — Setup Frontend

Set up Next.js frontend.

Acceptance Criteria:

- Next.js app starts successfully.
- Tailwind CSS is configured.
- Basic landing/login page exists.

## Phase 2 — Database and Auth

## Task 2.1 — Setup PostgreSQL Connection

Acceptance Criteria:

- Backend connects to PostgreSQL.
- Database session dependency is available.
- `.env.example` contains database configuration.

## Task 2.2 — Setup Alembic Migrations

Acceptance Criteria:

- Alembic is installed and configured.
- Initial migration can be generated.
- Migration can be applied successfully.

## Task 2.3 — Create User Model

Fields:

- id
- name
- email
- password_hash
- role
- is_active
- created_at
- updated_at

Roles:

- ADMIN
- RESIDENT
- SECURITY

Acceptance Criteria:

- User table exists.
- Email is unique.
- Role is required.

## Task 2.4 — Implement Password Hashing

Acceptance Criteria:

- Passwords are hashed before storage.
- Plain text passwords are never stored.
- Login verifies password correctly.

## Task 2.5 — Implement JWT Login

Endpoints:

```text
POST /auth/login
GET /auth/me
```

Acceptance Criteria:

- User can log in with email and password.
- API returns JWT access token.
- `/auth/me` returns current user details.

## Task 2.6 — Implement Role-Based Access

Acceptance Criteria:

- Admin-only routes reject residents and security users.
- Resident routes reject unauthorized users.
- Security routes reject unauthorized users.

## Phase 3 — Society Setup

## Task 3.1 — Create Society Model

Fields:

- id
- name
- address
- created_at
- updated_at

Acceptance Criteria:

- Society table exists.
- Admin can create society.
- Admin can view society details.

## Task 3.2 — Create Building Model

Fields:

- id
- society_id
- name
- created_at
- updated_at

Acceptance Criteria:

- Building belongs to society.
- Admin can create building.
- Admin can list buildings.

## Task 3.3 — Create Flat Model

Fields:

- id
- society_id
- building_id
- flat_number
- floor_number
- maintenance_amount
- created_at
- updated_at

Acceptance Criteria:

- Flat belongs to building and society.
- Flat number is unique within a building.
- Admin can create and list flats.

## Task 3.4 — Create Resident Model

Fields:

- id
- user_id
- society_id
- flat_id
- phone
- is_owner
- created_at
- updated_at

Acceptance Criteria:

- Resident is linked to a user.
- Resident is linked to a flat.
- Admin can assign resident to flat.

## Phase 4 — Maintenance Dues

## Task 4.1 — Create Maintenance Due Model

Fields:

- id
- society_id
- flat_id
- month
- year
- amount
- status
- due_date
- created_at
- updated_at

Statuses:

- UNPAID
- PAYMENT_SUBMITTED
- PAID
- REJECTED

Acceptance Criteria:

- Maintenance due table exists.
- Each flat can have only one due per month/year.

## Task 4.2 — Generate Monthly Dues

Endpoint:

```text
POST /dues/generate
```

Acceptance Criteria:

- Admin can generate dues for selected month/year.
- System creates due records for all flats.
- Duplicate due records are not created.

## Task 4.3 — Resident Views Own Dues

Endpoint:

```text
GET /dues/my
```

Acceptance Criteria:

- Resident can see only their flat dues.
- Dues are sorted by latest month/year.

## Task 4.4 — Submit Payment Proof

Endpoint:

```text
POST /dues/{due_id}/submit-payment
```

Acceptance Criteria:

- Resident can upload payment proof.
- Due status becomes PAYMENT_SUBMITTED.
- Payment record is created.

## Task 4.5 — Approve or Reject Payment

Endpoints:

```text
POST /dues/{due_id}/approve
POST /dues/{due_id}/reject
```

Acceptance Criteria:

- Admin can approve payment.
- Approved due status becomes PAID.
- Rejected due status becomes REJECTED.
- Admin can add rejection reason.

## Phase 5 — Complaint Management

## Task 5.1 — Create Complaint Model

Fields:

- id
- society_id
- flat_id
- resident_id
- title
- description
- category
- status
- priority
- image_url
- admin_note
- created_at
- updated_at

Statuses:

- OPEN
- IN_PROGRESS
- RESOLVED
- REJECTED

Categories:

- PLUMBING
- ELECTRICAL
- LIFT
- CLEANING
- PARKING
- SECURITY
- OTHER

Acceptance Criteria:

- Complaint table exists.
- Complaint is linked to resident and flat.

## Task 5.2 — Resident Creates Complaint

Endpoint:

```text
POST /complaints
```

Acceptance Criteria:

- Resident can create complaint.
- Complaint starts with OPEN status.
- Optional image can be uploaded.

## Task 5.3 — Resident Views Own Complaints

Endpoint:

```text
GET /complaints/my
```

Acceptance Criteria:

- Resident sees only their complaints.
- Complaints are sorted newest first.

## Task 5.4 — Admin Views All Complaints

Endpoint:

```text
GET /complaints
```

Acceptance Criteria:

- Admin can view all complaints.
- Admin can filter by status and category.

## Task 5.5 — Admin Updates Complaint Status

Endpoint:

```text
PATCH /complaints/{complaint_id}/status
```

Acceptance Criteria:

- Admin can update status.
- Admin can add note.
- Resident can see updated status.

## Phase 6 — Notices

## Task 6.1 — Create Notice Model

Fields:

- id
- society_id
- title
- body
- target_type
- building_id
- is_active
- created_by
- created_at
- updated_at

Target types:

- ALL
- BUILDING

Acceptance Criteria:

- Notice table exists.
- Notice can target all residents or one building.

## Task 6.2 — Admin Creates Notice

Endpoint:

```text
POST /notices
```

Acceptance Criteria:

- Admin can create notice.
- Notice is active by default.

## Task 6.3 — Users View Active Notices

Endpoint:

```text
GET /notices/active
```

Acceptance Criteria:

- Residents can view active notices.
- Security can view active notices.
- Notices are sorted newest first.

## Phase 7 — Visitor Management

## Task 7.1 — Create Visitor Model

Fields:

- id
- society_id
- flat_id
- resident_id
- visitor_name
- visitor_phone
- purpose
- vehicle_number
- visit_date
- entry_time
- exit_time
- status
- created_by_user_id
- created_at
- updated_at

Statuses:

- EXPECTED
- CHECKED_IN
- CHECKED_OUT
- CANCELLED

Acceptance Criteria:

- Visitor table exists.
- Visitor is linked to flat.
- Visitor can be expected or walk-in.

## Task 7.2 — Resident Adds Expected Visitor

Endpoint:

```text
POST /visitors/expected
```

Acceptance Criteria:

- Resident can add expected visitor.
- Visitor status starts as EXPECTED.

## Task 7.3 — Security Views Today’s Visitors

Endpoint:

```text
GET /visitors/today
```

Acceptance Criteria:

- Security can view expected visitors for today.
- Security can search by flat number.

## Task 7.4 — Security Adds Walk-In Visitor

Endpoint:

```text
POST /visitors/walk-in
```

Acceptance Criteria:

- Security can create visitor entry.
- Visitor can be linked to flat.
- Status becomes CHECKED_IN.

## Task 7.5 — Security Marks Check-In and Check-Out

Endpoints:

```text
POST /visitors/{visitor_id}/check-in
POST /visitors/{visitor_id}/check-out
```

Acceptance Criteria:

- Check-in sets entry time.
- Check-out sets exit time.
- Status updates correctly.

## Phase 8 — Dashboards

## Task 8.1 — Admin Dashboard

Show:

- Total flats
- Total residents
- Current month paid dues
- Current month unpaid dues
- Open complaints
- Visitors today

Acceptance Criteria:

- Admin dashboard loads summary data.
- Data is accurate for current month.

## Task 8.2 — Resident Dashboard

Show:

- Current due status
- Recent complaints
- Recent notices
- Today’s expected visitors

Acceptance Criteria:

- Resident sees only own data.
- Dashboard is simple and mobile-friendly.

## Task 8.3 — Security Dashboard

Show:

- Expected visitors today
- Checked-in visitors
- Quick visitor entry form

Acceptance Criteria:

- Security dashboard is optimized for quick entry.
- Search by flat number works.

## Phase 9 — Deployment

## Task 9.1 — Prepare Backend Deployment

Acceptance Criteria:

- Backend has production start command.
- CORS is configured.
- Environment variables are documented.
- Database URL is configurable.

## Task 9.2 — Prepare Frontend Deployment

Acceptance Criteria:

- Frontend has production build command.
- API base URL is configurable.
- Authentication token storage works.

## Task 9.3 — Deploy MVP

Suggested deployment:

- Frontend: Vercel
- Backend: Render or Railway
- Database: Neon or Supabase

Acceptance Criteria:

- App is publicly accessible.
- Login works.
- Admin, resident, and security flows work end-to-end.

## Phase 10 — Final Testing

## Task 10.1 — Seed Test Data

Create:

- One society
- Two buildings
- Ten flats
- One admin
- Three residents
- One security user

Acceptance Criteria:

- Seed command creates usable test data.

## Task 10.2 — End-to-End MVP Test

Test:

- Admin creates flats and residents.
- Admin generates dues.
- Resident uploads payment proof.
- Admin approves payment.
- Resident raises complaint.
- Admin updates complaint.
- Admin creates notice.
- Resident adds expected visitor.
- Security checks in visitor.

Acceptance Criteria:

- All core flows work without manual database changes.
