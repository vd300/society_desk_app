from datetime import date, datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Flat, Resident, Visitor
from app.models.enums import VisitorStatus
from app.schemas.common import ExpectedVisitorCreate, WalkInVisitorCreate


def create_expected_visitor(
    db: Session, resident: Resident, user_id: str, payload: ExpectedVisitorCreate
) -> Visitor:
    visitor = Visitor(
        society_id=resident.society_id,
        flat_id=resident.flat_id,
        resident_id=resident.id,
        visitor_name=payload.visitor_name,
        visitor_phone=payload.visitor_phone,
        purpose=payload.purpose,
        vehicle_number=payload.vehicle_number,
        visit_date=payload.visit_date,
        status=VisitorStatus.EXPECTED,
        created_by_user_id=user_id,
    )
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return visitor


def create_walk_in_visitor(
    db: Session, user_id: str, payload: WalkInVisitorCreate
) -> Visitor:
    flat = db.get(Flat, payload.flat_id)
    if not flat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flat not found")
    visitor = Visitor(
        society_id=flat.society_id,
        flat_id=flat.id,
        visitor_name=payload.visitor_name,
        visitor_phone=payload.visitor_phone,
        purpose=payload.purpose,
        vehicle_number=payload.vehicle_number,
        visit_date=payload.visit_date or date.today(),
        entry_time=datetime.now(timezone.utc),
        status=VisitorStatus.CHECKED_IN,
        created_by_user_id=user_id,
    )
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return visitor


def check_in(db: Session, visitor: Visitor) -> Visitor:
    visitor.entry_time = datetime.now(timezone.utc)
    visitor.status = VisitorStatus.CHECKED_IN
    db.commit()
    db.refresh(visitor)
    return visitor


def check_out(db: Session, visitor: Visitor) -> Visitor:
    if visitor.status == VisitorStatus.CHECKED_OUT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Visitor already checked out")
    visitor.exit_time = datetime.now(timezone.utc)
    visitor.status = VisitorStatus.CHECKED_OUT
    db.commit()
    db.refresh(visitor)
    return visitor
