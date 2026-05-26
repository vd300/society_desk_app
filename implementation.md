# SocietyDesk — Implementation Notes

## 1. Product Name

Working name: SocietyDesk

## 2. MVP Boundary

The MVP should be intentionally simple.

Included:

- Role-based login
- Admin dashboard
- Resident dashboard
- Security dashboard
- Society/building/flat/resident setup
- Maintenance dues
- Payment proof upload
- Admin payment verification
- Complaint tracking
- Notices
- Visitor logs

Excluded:

- Real payment gateway
- WhatsApp integration
- Mobile app
- QR visitor pass
- Vendor login
- AI features
- Multi-society billing
- Complex accounting

## 3. Main Data Model

## User

Represents anyone who can log in.

Fields:

```text
id
name
email
password_hash
role
is_active
created_at
updated_at
```

Roles:

```text
ADMIN
RESIDENT
SECURITY
```

## Society

Represents one apartment society.

Fields:

```text
id
name
address
created_at
updated_at
```

For MVP, you can support only one society. Keep `society_id` in tables so the app can become multi-society later.

## Building

Represents wing/building/tower.

Fields:

```text
id
society_id
name
created_at
updated_at
```

## Flat

Represents one flat/unit.

Fields:

```text
id
society_id
building_id
flat_number
floor_number
maintenance_amount
created_at
updated_at
```

## Resident

Links a user to a flat.

Fields:

```text
id
user_id
society_id
flat_id
phone
is_owner
created_at
updated_at
```

## MaintenanceDue

Represents monthly maintenance due for a flat.

Fields:

```text
id
society_id
flat_id
month
year
amount
status
due_date
created_at
updated_at
```

Status enum:

```text
UNPAID
PAYMENT_SUBMITTED
PAID
REJECTED
```

Unique constraint:

```text
flat_id + month + year
```

## Payment

Represents payment proof submitted by resident.

Fields:

```text
id
maintenance_due_id
submitted_by_user_id
amount
proof_url
transaction_reference
status
admin_note
verified_by_user_id
verified_at
created_at
updated_at
```

Status enum:

```text
SUBMITTED
APPROVED
REJECTED
```

## Complaint

Represents resident complaint.

Fields:

```text
id
society_id
flat_id
resident_id
title
description
category
status
priority
image_url
admin_note
created_at
updated_at
```

Category enum:

```text
PLUMBING
ELECTRICAL
LIFT
CLEANING
PARKING
SECURITY
OTHER
```

Status enum:

```text
OPEN
IN_PROGRESS
RESOLVED
REJECTED
```

Priority enum:

```text
LOW
MEDIUM
HIGH
```

## Notice

Represents society notice.

Fields:

```text
id
society_id
title
body
target_type
building_id
is_active
created_by
created_at
updated_at
```

Target type enum:

```text
ALL
BUILDING
```

## Visitor

Represents expected or walk-in visitor.

Fields:

```text
id
society_id
flat_id
resident_id
visitor_name
visitor_phone
purpose
vehicle_number
visit_date
entry_time
exit_time
status
created_by_user_id
created_at
updated_at
```

Status enum:

```text
EXPECTED
CHECKED_IN
CHECKED_OUT
CANCELLED
```

## 4. Backend Implementation Details

## 4.1 FastAPI App Structure

Use routers by domain:

```text
auth
admin
dues
complaints
notices
visitors
```

Keep business logic in services.

Avoid putting too much logic directly inside route functions.

## 4.2 Auth Flow

Login request:

```json
{
  "email": "admin@societydesk.com",
  "password": "password"
}
```

Login response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "name": "Admin User",
    "email": "admin@societydesk.com",
    "role": "ADMIN"
  }
}
```

Use JWT payload:

```json
{
  "sub": "user_id",
  "role": "ADMIN"
}
```

## 4.3 Role Guards

Create dependencies:

```text
get_current_user()
require_admin()
require_resident()
require_security()
```

Use them in routes.

Example:

```python
@router.post("/dues/generate")
def generate_dues(
    payload: GenerateDuesRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    ...
```

## 4.4 File Uploads

For local development:

```text
backend/uploads/
  payments/
  complaints/
```

For deployed app, use Cloudinary or Supabase Storage.

Store only the file URL/path in database.

## 5. Frontend Implementation Details

## 5.1 Layouts

Create separate layouts:

```text
AdminLayout
ResidentLayout
SecurityLayout
```

Each layout should have role-specific navigation.

## 5.2 Auth Storage

For MVP, store token in localStorage.

Later, move to httpOnly cookies for better security.

## 5.3 API Client

Create a shared API client:

```text
frontend/lib/api.ts
```

It should:

- Attach JWT token to requests
- Handle 401 responses
- Use environment variable for backend URL

## 5.4 UI Components

Reusable components:

```text
StatCard
DataTable
StatusBadge
PageHeader
ConfirmDialog
FormInput
FileUpload
```

## 6. Dashboard Stats

## Admin Dashboard

Query should return:

```json
{
  "total_flats": 100,
  "total_residents": 240,
  "current_month_paid_dues": 72,
  "current_month_unpaid_dues": 28,
  "open_complaints": 13,
  "visitors_today": 18
}
```

## Resident Dashboard

Query should return:

```json
{
  "current_due": {
    "amount": 3000,
    "status": "UNPAID",
    "month": 5,
    "year": 2026
  },
  "recent_complaints": [],
  "recent_notices": [],
  "today_visitors": []
}
```

## Security Dashboard

Query should return:

```json
{
  "expected_visitors_today": [],
  "checked_in_visitors": []
}
```

## 7. Important Business Rules

## Maintenance Dues

- Admin should not generate duplicate dues for same flat/month/year.
- Resident should not submit payment proof for another flat.
- Payment approval should update both payment and due status.
- Payment rejection should allow resident to submit again.

## Complaints

- Residents can only view their own complaints.
- Admin can view all complaints.
- Only admin can change complaint status.
- Complaint status should start as OPEN.

## Notices

- Admin creates notices.
- Residents see notices targeted to all or their building.
- Security can see general notices.

## Visitors

- Residents can create expected visitors only for their own flat.
- Security can create walk-in visitor logs.
- Check-in should set entry time.
- Check-out should set exit time.
- Checked-out visitors should not be checked out again.

## 8. Seed Data

Create seed data for local development:

```text
Society: Green Heights
Buildings: A Wing, B Wing
Flats: A-101 to A-105, B-101 to B-105

Users:
admin@societydesk.com
security@societydesk.com
resident1@societydesk.com
resident2@societydesk.com
resident3@societydesk.com
```

Use password:

```text
password123
```

Only for local development.

## 9. Environment Variables

Backend `.env.example`:

```text
DATABASE_URL=postgresql://user:password@localhost:5432/societydesk
JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=uploads
CORS_ORIGINS=http://localhost:3000
```

Frontend `.env.example`:

```text
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## 10. Deployment Notes

## Backend

Deploy to Render or Railway.

Production command example:

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Frontend

Deploy to Vercel.

Set:

```text
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url
```

## Database

Use Neon or Supabase Postgres.

Run migrations after deployment.

## 11. MVP Completion Checklist

The MVP is complete when:

- Admin can log in.
- Resident can log in.
- Security can log in.
- Admin can create society structure.
- Admin can generate monthly dues.
- Resident can upload payment proof.
- Admin can approve/reject payment.
- Resident can raise complaint.
- Admin can update complaint status.
- Admin can create notice.
- Resident can view notice.
- Resident can add expected visitor.
- Security can check visitor in and out.
- App is deployed and usable from public URL.
