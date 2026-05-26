from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_resident, require_admin, require_security
from app.core.database import get_db
from app.models import Flat, Resident, User, Visitor
from app.models.enums import VisitorStatus
from app.schemas.common import (
    ExpectedVisitorCreate,
    FlatRead,
    SecurityDashboard,
    VisitorRead,
    WalkInVisitorCreate,
)
from app.services.visitor_service import (
    check_in,
    check_out,
    create_expected_visitor,
    create_walk_in_visitor,
)

router = APIRouter(prefix="/visitors", tags=["visitors"])


@router.post("/expected", response_model=VisitorRead, status_code=201)
def add_expected_visitor(
    payload: ExpectedVisitorCreate,
    resident: Resident = Depends(get_current_resident),
    db: Session = Depends(get_db),
) -> Visitor:
    return create_expected_visitor(db, resident, resident.user_id, payload)


@router.post("/walk-in", response_model=VisitorRead, status_code=201)
def add_walk_in_visitor(
    payload: WalkInVisitorCreate,
    current_user: User = Depends(require_security),
    db: Session = Depends(get_db),
) -> Visitor:
    return create_walk_in_visitor(db, current_user.id, payload)


@router.get("/today", response_model=list[VisitorRead])
def today_visitors(
    flat_number: str | None = Query(default=None),
    _: User = Depends(require_security),
    db: Session = Depends(get_db),
) -> list[Visitor]:
    query = select(Visitor).where(Visitor.visit_date == date.today()).order_by(Visitor.created_at.desc())
    if flat_number:
        query = query.join(Flat, Flat.id == Visitor.flat_id).where(Flat.flat_number.ilike(f"%{flat_number}%"))
    return list(db.scalars(query))


@router.get("/flats", response_model=list[FlatRead])
def search_flats(
    flat_number: str | None = Query(default=None),
    _: User = Depends(require_security),
    db: Session = Depends(get_db),
) -> list[Flat]:
    query = select(Flat).order_by(Flat.flat_number)
    if flat_number:
        query = query.where(Flat.flat_number.ilike(f"%{flat_number}%"))
    return list(db.scalars(query.limit(20)))


@router.get("/logs", response_model=list[VisitorRead])
def visitor_logs(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[Visitor]:
    return list(db.scalars(select(Visitor).order_by(Visitor.created_at.desc())))


@router.get("/security-dashboard", response_model=SecurityDashboard)
def security_dashboard(
    _: User = Depends(require_security),
    db: Session = Depends(get_db),
) -> SecurityDashboard:
    today = date.today()
    expected = list(
        db.scalars(
            select(Visitor)
            .where(Visitor.visit_date == today, Visitor.status == VisitorStatus.EXPECTED)
            .order_by(Visitor.created_at.desc())
        )
    )
    checked_in = list(
        db.scalars(
            select(Visitor)
            .where(Visitor.status == VisitorStatus.CHECKED_IN)
            .order_by(Visitor.entry_time.desc())
        )
    )
    return SecurityDashboard(expected_visitors_today=expected, checked_in_visitors=checked_in)


@router.post("/{visitor_id}/check-in", response_model=VisitorRead)
def mark_check_in(
    visitor_id: str,
    _: User = Depends(require_security),
    db: Session = Depends(get_db),
) -> Visitor:
    visitor = db.get(Visitor, visitor_id)
    if not visitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")
    return check_in(db, visitor)


@router.post("/{visitor_id}/check-out", response_model=VisitorRead)
def mark_check_out(
    visitor_id: str,
    _: User = Depends(require_security),
    db: Session = Depends(get_db),
) -> Visitor:
    visitor = db.get(Visitor, visitor_id)
    if not visitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")
    return check_out(db, visitor)
