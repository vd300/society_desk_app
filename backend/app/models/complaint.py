from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ComplaintCategory, ComplaintPriority, ComplaintStatus


class Complaint(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "complaints"

    society_id: Mapped[str] = mapped_column(ForeignKey("societies.id"), nullable=False)
    flat_id: Mapped[str] = mapped_column(ForeignKey("flats.id"), nullable=False)
    resident_id: Mapped[str] = mapped_column(ForeignKey("residents.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[ComplaintCategory] = mapped_column(Enum(ComplaintCategory), nullable=False)
    status: Mapped[ComplaintStatus] = mapped_column(
        Enum(ComplaintStatus), default=ComplaintStatus.OPEN, nullable=False
    )
    priority: Mapped[ComplaintPriority] = mapped_column(
        Enum(ComplaintPriority), default=ComplaintPriority.MEDIUM, nullable=False
    )
    image_url: Mapped[str | None] = mapped_column(String(500))
    admin_note: Mapped[str | None] = mapped_column(Text)
