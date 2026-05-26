from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.core.database import get_db
from app.models import Building, Complaint, Flat, MaintenanceDue, Resident, Society, User, Visitor
from app.models.enums import ComplaintStatus, DueStatus
from app.schemas.common import (
    AdminDashboard,
    BuildingCreate,
    BuildingRead,
    FlatCreate,
    FlatRead,
    ResidentCreate,
    ResidentRead,
    SocietyCreate,
    SocietyRead,
    UserRead,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard", response_model=AdminDashboard)
def admin_dashboard(
    _: User = Depends(require_admin), db: Session = Depends(get_db)
) -> AdminDashboard:
    today = date.today()
    total_flats = db.scalar(select(func.count()).select_from(Flat)) or 0
    total_residents = db.scalar(select(func.count()).select_from(Resident)) or 0
    paid_dues = db.scalar(
        select(func.count()).where(
            MaintenanceDue.month == today.month,
            MaintenanceDue.year == today.year,
            MaintenanceDue.status == DueStatus.PAID,
        )
    ) or 0
    unpaid_dues = db.scalar(
        select(func.count()).where(
            MaintenanceDue.month == today.month,
            MaintenanceDue.year == today.year,
            MaintenanceDue.status != DueStatus.PAID,
        )
    ) or 0
    open_complaints = db.scalar(
        select(func.count()).where(Complaint.status == ComplaintStatus.OPEN)
    ) or 0
    visitors_today = db.scalar(select(func.count()).where(Visitor.visit_date == today)) or 0
    return AdminDashboard(
        total_flats=total_flats,
        total_residents=total_residents,
        current_month_paid_dues=paid_dues,
        current_month_unpaid_dues=unpaid_dues,
        open_complaints=open_complaints,
        visitors_today=visitors_today,
    )


@router.post("/societies", response_model=SocietyRead, status_code=201)
def create_society(
    payload: SocietyCreate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Society:
    society = Society(name=payload.name, address=payload.address)
    db.add(society)
    db.commit()
    db.refresh(society)
    return society


@router.get("/societies", response_model=list[SocietyRead])
def list_societies(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[Society]:
    return list(db.scalars(select(Society).order_by(Society.created_at.desc())))


@router.get("/users", response_model=list[UserRead])
def list_users(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[User]:
    return list(db.scalars(select(User).order_by(User.name)))


@router.get("/societies/{society_id}", response_model=SocietyRead)
def get_society(
    society_id: str, _: User = Depends(require_admin), db: Session = Depends(get_db)
) -> Society:
    society = db.get(Society, society_id)
    if not society:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Society not found")
    return society


@router.post("/buildings", response_model=BuildingRead, status_code=201)
def create_building(
    payload: BuildingCreate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Building:
    if not db.get(Society, payload.society_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Society not found")
    building = Building(society_id=payload.society_id, name=payload.name)
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


@router.get("/buildings", response_model=list[BuildingRead])
def list_buildings(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[Building]:
    return list(db.scalars(select(Building).order_by(Building.name)))


@router.post("/flats", response_model=FlatRead, status_code=201)
def create_flat(
    payload: FlatCreate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Flat:
    if not db.get(Society, payload.society_id) or not db.get(Building, payload.building_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Society or building not found")
    flat = Flat(**payload.model_dump())
    db.add(flat)
    db.commit()
    db.refresh(flat)
    return flat


@router.get("/flats", response_model=list[FlatRead])
def list_flats(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[Flat]:
    return list(db.scalars(select(Flat).order_by(Flat.flat_number)))


@router.post("/residents", response_model=ResidentRead, status_code=201)
def create_resident(
    payload: ResidentCreate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Resident:
    user = db.get(User, payload.user_id)
    flat = db.get(Flat, payload.flat_id)
    if not user or not flat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or flat not found")
    resident = Resident(**payload.model_dump())
    db.add(resident)
    db.commit()
    db.refresh(resident)
    return resident


@router.get("/residents", response_model=list[ResidentRead])
def list_residents(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[Resident]:
    return list(db.scalars(select(Resident).order_by(Resident.created_at.desc())))
