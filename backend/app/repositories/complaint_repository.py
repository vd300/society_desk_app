from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Complaint


def get_complaint(db: Session, complaint_id: str) -> Complaint | None:
    return db.get(Complaint, complaint_id)


def list_complaints(db: Session) -> list[Complaint]:
    return list(db.scalars(select(Complaint).order_by(Complaint.created_at.desc())))
