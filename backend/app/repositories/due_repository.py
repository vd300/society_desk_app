from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import MaintenanceDue


def get_due(db: Session, due_id: str) -> MaintenanceDue | None:
    return db.get(MaintenanceDue, due_id)


def list_dues(db: Session) -> list[MaintenanceDue]:
    return list(db.scalars(select(MaintenanceDue).order_by(MaintenanceDue.year.desc(), MaintenanceDue.month.desc())))
