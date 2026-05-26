from sqlalchemy.orm import Session

from app.models import Complaint, Resident
from app.schemas.common import ComplaintCreate


def create_complaint(db: Session, resident: Resident, payload: ComplaintCreate) -> Complaint:
    complaint = Complaint(
        society_id=resident.society_id,
        flat_id=resident.flat_id,
        resident_id=resident.id,
        title=payload.title,
        description=payload.description,
        category=payload.category,
        priority=payload.priority,
        image_url=payload.image_url,
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint
