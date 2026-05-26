# SocietyDesk — Product Requirements Document

## 1. Product Summary

SocietyDesk is a web-based society maintenance management application for apartment societies that currently depend on WhatsApp groups, Excel sheets, manual registers, and informal follow-ups.

The MVP will help society admins, residents, and security guards manage maintenance dues, complaints, notices, and visitor entries from one centralized platform.

## 2. Problem

Apartment societies commonly manage operations through disconnected tools:

- Maintenance dues are tracked in spreadsheets.
- Payment confirmations are shared as screenshots on WhatsApp.
- Complaints get buried in group chats.
- Visitors are recorded manually in registers.
- Notices are sent repeatedly across WhatsApp groups.
- Committee members struggle to know what is pending, paid, resolved, or ignored.

This creates confusion, lack of accountability, missing records, delayed responses, and unnecessary manual work.

## 3. Target Users

### Admin / Committee Member

Responsible for society operations.

They need to:

- Add residents and flats.
- Generate monthly maintenance dues.
- Verify resident payments.
- Track pending dues.
- Manage complaints.
- Publish notices.
- View visitor logs.

### Resident

Lives in the society.

They need to:

- View maintenance dues.
- Upload payment proof.
- Raise complaints.
- Track complaint status.
- View notices.
- Add expected visitors.

### Security Guard

Handles entry gate operations.

They need to:

- See expected visitors.
- Add walk-in visitors.
- Mark visitor entry and exit.
- Search by flat number.

## 4. MVP Goal

Build a simple but usable society management platform with three dashboards:

1. Admin dashboard
2. Resident dashboard
3. Security dashboard

The MVP should solve four core problems:

1. Maintenance due tracking
2. Complaint management
3. Notice sharing
4. Visitor logging

## 5. MVP Features

## 5.1 Authentication and Role-Based Access

Users can log in with email and password.

Supported roles:

- ADMIN
- RESIDENT
- SECURITY

Each role gets access only to relevant features.

### Acceptance Criteria

- Admin can access all management screens.
- Resident can access only their own dues, complaints, notices, and visitor entries.
- Security can access visitor-related screens only.
- Unauthorized users cannot access restricted routes.

## 5.2 Society, Building, Flat, and Resident Setup

Admin can create and manage basic society structure.

### Entities

- Society
- Building / Wing
- Flat
- Resident

### Acceptance Criteria

- Admin can create buildings or wings.
- Admin can create flats under a building.
- Admin can assign residents to flats.
- Each resident is linked to one flat for MVP.
- Admin can view all flats and residents.

## 5.3 Maintenance Dues

Admin can generate monthly dues for all flats.

Residents can view dues and upload payment proof.

Admin can verify payment and mark dues as paid.

### Due Statuses

- UNPAID
- PAYMENT_SUBMITTED
- PAID
- REJECTED

### Acceptance Criteria

- Admin can generate dues for a selected month.
- Each flat gets one maintenance due record for that month.
- Resident can see current and past dues.
- Resident can upload payment proof.
- Admin can approve or reject submitted payment proof.
- Dashboard shows paid and unpaid counts.

## 5.4 Complaint Management

Residents can raise complaints.

Admins can view, update, and resolve complaints.

### Complaint Statuses

- OPEN
- IN_PROGRESS
- RESOLVED
- REJECTED

### Complaint Categories

- PLUMBING
- ELECTRICAL
- LIFT
- CLEANING
- PARKING
- SECURITY
- OTHER

### Acceptance Criteria

- Resident can create complaint with title, description, category, and optional image.
- Resident can view their own complaints.
- Admin can view all complaints.
- Admin can update complaint status.
- Admin can add internal/admin notes.
- Resident can see updated complaint status.

## 5.5 Notices

Admin can publish notices.

Residents and security can view notices.

### Acceptance Criteria

- Admin can create notice with title and body.
- Admin can optionally target all residents or a specific building.
- Residents can view active notices.
- Notices are sorted newest first.

## 5.6 Visitor Management

Residents can add expected visitors.

Security can add visitor entries and mark exit.

### Visitor Types

- Expected visitor
- Walk-in visitor

### Visitor Statuses

- EXPECTED
- CHECKED_IN
- CHECKED_OUT
- CANCELLED

### Acceptance Criteria

- Resident can add expected visitor with name, phone, purpose, and visit date.
- Security can view expected visitors for today.
- Security can create a walk-in visitor entry.
- Security can mark visitor as checked in.
- Security can mark visitor as checked out.
- Admin can view visitor logs.

## 6. Non-MVP Features

These should not be included in the first version:

- Real payment gateway
- WhatsApp integration
- Mobile app
- QR visitor pass
- Vendor login
- Advanced accounting
- Automated late fees
- Push notifications
- AI chatbot
- Multi-society SaaS billing
- Face recognition
- IoT gate integration

## 7. Success Metrics

The MVP is successful if:

- Admin can onboard a society structure.
- Monthly dues can be generated and tracked.
- Residents can submit payment proof.
- Admin can verify payments.
- Residents can raise and track complaints.
- Admin can publish notices.
- Security can maintain visitor logs.
- The app can be deployed and used by a small real society.

## 8. Product Vision

The long-term vision is to make SocietyDesk the central operating system for small and medium apartment societies.

It should replace scattered spreadsheets, WhatsApp messages, physical registers, and manual follow-ups with a transparent, trackable, role-based platform.
