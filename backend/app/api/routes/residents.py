from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_resident
from app.core.database import get_db
from app.models import Complaint, MaintenanceDue, Notice, Resident, Visitor
from app.models.enums import NoticeTargetType
from app.schemas.common import ResidentDashboard

router = APIRouter(prefix="/resident", tags=["resident"])


@router.get("/dashboard", response_model=ResidentDashboard)
def resident_dashboard(
    resident: Resident = Depends(get_current_resident),
    db: Session = Depends(get_db),
) -> ResidentDashboard:
    today = date.today()
    current_due = db.scalar(
        select(MaintenanceDue)
        .where(
            MaintenanceDue.flat_id == resident.flat_id,
            MaintenanceDue.month == today.month,
            MaintenanceDue.year == today.year,
        )
        .order_by(MaintenanceDue.created_at.desc())
    )
    complaints = list(
        db.scalars(
            select(Complaint)
            .where(Complaint.resident_id == resident.id)
            .order_by(Complaint.created_at.desc())
            .limit(5)
        )
    )
    notices = list(
        db.scalars(
            select(Notice)
            .where(
                Notice.is_active.is_(True),
                (Notice.target_type == NoticeTargetType.ALL)
                | (
                    (Notice.target_type == NoticeTargetType.BUILDING)
                    & (Notice.building_id == resident.flat.building_id)
                ),
            )
            .order_by(Notice.created_at.desc())
            .limit(5)
        )
    )
    visitors = list(
        db.scalars(
            select(Visitor)
            .where(Visitor.resident_id == resident.id, Visitor.visit_date == today)
            .order_by(Visitor.created_at.desc())
        )
    )
    return ResidentDashboard(
        current_due=current_due,
        recent_complaints=complaints,
        recent_notices=notices,
        today_visitors=visitors,
    )
