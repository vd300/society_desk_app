from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_resident, require_admin
from app.core.database import get_db
from app.models import Complaint, Resident, User
from app.models.enums import ComplaintCategory, ComplaintStatus
from app.schemas.common import ComplaintCreate, ComplaintRead, ComplaintStatusUpdate
from app.services.complaint_service import create_complaint

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.post("", response_model=ComplaintRead, status_code=201)
def create_resident_complaint(
    payload: ComplaintCreate,
    resident: Resident = Depends(get_current_resident),
    db: Session = Depends(get_db),
) -> Complaint:
    return create_complaint(db, resident, payload)


@router.get("/my", response_model=list[ComplaintRead])
def my_complaints(
    resident: Resident = Depends(get_current_resident),
    db: Session = Depends(get_db),
) -> list[Complaint]:
    return list(
        db.scalars(
            select(Complaint)
            .where(Complaint.resident_id == resident.id)
            .order_by(Complaint.created_at.desc())
        )
    )


@router.get("", response_model=list[ComplaintRead])
def list_complaints(
    status_filter: ComplaintStatus | None = Query(default=None, alias="status"),
    category: ComplaintCategory | None = None,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> list[Complaint]:
    query = select(Complaint).order_by(Complaint.created_at.desc())
    if status_filter:
        query = query.where(Complaint.status == status_filter)
    if category:
        query = query.where(Complaint.category == category)
    return list(db.scalars(query))


@router.patch("/{complaint_id}/status", response_model=ComplaintRead)
def update_complaint_status(
    complaint_id: str,
    payload: ComplaintStatusUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Complaint:
    complaint = db.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    complaint.status = payload.status
    complaint.admin_note = payload.admin_note
    db.commit()
    db.refresh(complaint)
    return complaint
