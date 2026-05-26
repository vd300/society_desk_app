from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_security
from app.api.routes.visitors import security_dashboard as visitor_security_dashboard
from app.core.database import get_db
from app.models import User
from app.schemas.common import SecurityDashboard

router = APIRouter(prefix="/security", tags=["security"])


@router.get("/dashboard", response_model=SecurityDashboard)
def dashboard(
    current_user: User = Depends(require_security),
    db: Session = Depends(get_db),
) -> SecurityDashboard:
    return visitor_security_dashboard(current_user, db)
