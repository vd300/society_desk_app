from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Flat, MaintenanceDue, Payment, Resident
from app.models.enums import DueStatus, PaymentStatus


def generate_dues(
    db: Session,
    society_id: str,
    month: int,
    year: int,
    due_date,
) -> tuple[int, int]:
    flats = list(db.scalars(select(Flat).where(Flat.society_id == society_id)))
    created = 0
    skipped = 0
    for flat in flats:
        existing = db.scalar(
            select(MaintenanceDue).where(
                MaintenanceDue.flat_id == flat.id,
                MaintenanceDue.month == month,
                MaintenanceDue.year == year,
            )
        )
        if existing:
            skipped += 1
            continue
        db.add(
            MaintenanceDue(
                society_id=society_id,
                flat_id=flat.id,
                month=month,
                year=year,
                amount=flat.maintenance_amount,
                due_date=due_date,
            )
        )
        created += 1
    db.commit()
    return created, skipped


def submit_payment(
    db: Session,
    due: MaintenanceDue,
    resident: Resident,
    user_id: str,
    amount: Decimal,
    proof_url: str,
    transaction_reference: str | None,
) -> Payment:
    if due.flat_id != resident.flat_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Due is not for your flat")
    payment = Payment(
        maintenance_due_id=due.id,
        submitted_by_user_id=user_id,
        amount=amount,
        proof_url=proof_url,
        transaction_reference=transaction_reference,
    )
    due.status = DueStatus.PAYMENT_SUBMITTED
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def approve_latest_payment(db: Session, due: MaintenanceDue, admin_user_id: str, note: str | None) -> Payment:
    payment = _latest_payment(db, due.id)
    payment.status = PaymentStatus.APPROVED
    payment.admin_note = note
    payment.verified_by_user_id = admin_user_id
    payment.verified_at = datetime.now(timezone.utc)
    due.status = DueStatus.PAID
    db.commit()
    db.refresh(payment)
    return payment


def reject_latest_payment(db: Session, due: MaintenanceDue, admin_user_id: str, note: str | None) -> Payment:
    payment = _latest_payment(db, due.id)
    payment.status = PaymentStatus.REJECTED
    payment.admin_note = note
    payment.verified_by_user_id = admin_user_id
    payment.verified_at = datetime.now(timezone.utc)
    due.status = DueStatus.REJECTED
    db.commit()
    db.refresh(payment)
    return payment


def _latest_payment(db: Session, due_id: str) -> Payment:
    payment = db.scalar(
        select(Payment)
        .where(Payment.maintenance_due_id == due_id)
        .order_by(Payment.created_at.desc())
    )
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment
