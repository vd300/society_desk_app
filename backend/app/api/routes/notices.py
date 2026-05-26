from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_resident, require_admin, require_notice_viewer
from app.core.database import get_db
from app.models import Notice, User
from app.models.enums import NoticeTargetType, UserRole
from app.schemas.common import NoticeCreate, NoticeRead

router = APIRouter(prefix="/notices", tags=["notices"])


@router.post("", response_model=NoticeRead, status_code=201)
def create_notice(
    payload: NoticeCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Notice:
    notice = Notice(**payload.model_dump(), created_by=current_user.id)
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice


@router.get("", response_model=list[NoticeRead])
def list_notices(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[Notice]:
    return list(db.scalars(select(Notice).order_by(Notice.created_at.desc())))


@router.get("/active", response_model=list[NoticeRead])
def active_notices(
    current_user: User = Depends(require_notice_viewer),
    db: Session = Depends(get_db),
) -> list[Notice]:
    query = select(Notice).where(Notice.is_active.is_(True)).order_by(Notice.created_at.desc())
    if current_user.role == UserRole.RESIDENT and current_user.resident_profile:
        building_id = current_user.resident_profile.flat.building_id
        query = query.where(
            (Notice.target_type == NoticeTargetType.ALL)
            | ((Notice.target_type == NoticeTargetType.BUILDING) & (Notice.building_id == building_id))
        )
    else:
        query = query.where(Notice.target_type == NoticeTargetType.ALL)
    return list(db.scalars(query))
