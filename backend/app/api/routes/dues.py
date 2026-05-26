from decimal import Decimal

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_resident, require_admin
from app.core.database import get_db
from app.models import MaintenanceDue, Payment, Resident, User
from app.schemas.common import (
    GenerateDuesRequest,
    GenerateDuesResponse,
    MaintenanceDueRead,
    PaymentDecisionRequest,
    PaymentRead,
)
from app.services.due_service import (
    approve_latest_payment,
    generate_dues,
    reject_latest_payment,
    submit_payment,
)
from app.services.file_service import save_upload

router = APIRouter(prefix="/dues", tags=["dues"])


@router.post("/generate", response_model=GenerateDuesResponse)
def generate_monthly_dues(
    payload: GenerateDuesRequest,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> GenerateDuesResponse:
    created, skipped = generate_dues(db, payload.society_id, payload.month, payload.year, payload.due_date)
    return GenerateDuesResponse(created=created, skipped=skipped)


@router.get("", response_model=list[MaintenanceDueRead])
def list_all_dues(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[MaintenanceDue]:
    return list(db.scalars(select(MaintenanceDue).order_by(MaintenanceDue.year.desc(), MaintenanceDue.month.desc())))


@router.get("/my", response_model=list[MaintenanceDueRead])
def my_dues(
    resident: Resident = Depends(get_current_resident),
    db: Session = Depends(get_db),
) -> list[MaintenanceDue]:
    return list(
        db.scalars(
            select(MaintenanceDue)
            .where(MaintenanceDue.flat_id == resident.flat_id)
            .order_by(MaintenanceDue.year.desc(), MaintenanceDue.month.desc())
        )
    )


@router.post("/{due_id}/submit-payment", response_model=PaymentRead)
def submit_due_payment(
    due_id: str,
    amount: Decimal = Form(...),
    transaction_reference: str | None = Form(None),
    proof_file: UploadFile | None = File(None),
    proof_url: str | None = Form(None),
    resident: Resident = Depends(get_current_resident),
    db: Session = Depends(get_db),
) -> Payment:
    due = db.get(MaintenanceDue, due_id)
    if not due:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Due not found")
    final_proof_url = save_upload(proof_file, "payments") if proof_file else proof_url
    if not final_proof_url:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Payment proof is required")
    return submit_payment(db, due, resident, resident.user_id, amount, final_proof_url, transaction_reference)


@router.post("/{due_id}/approve", response_model=PaymentRead)
def approve_payment(
    due_id: str,
    payload: PaymentDecisionRequest | None = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Payment:
    due = db.get(MaintenanceDue, due_id)
    if not due:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Due not found")
    return approve_latest_payment(db, due, current_user.id, payload.admin_note if payload else None)


@router.post("/{due_id}/reject", response_model=PaymentRead)
def reject_payment(
    due_id: str,
    payload: PaymentDecisionRequest | None = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Payment:
    due = db.get(MaintenanceDue, due_id)
    if not due:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Due not found")
    return reject_latest_payment(db, due, current_user.id, payload.admin_note if payload else None)
