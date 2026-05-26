from datetime import date, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import VisitorStatus


class Visitor(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "visitors"

    society_id: Mapped[str] = mapped_column(ForeignKey("societies.id"), nullable=False)
    flat_id: Mapped[str] = mapped_column(ForeignKey("flats.id"), nullable=False)
    resident_id: Mapped[str | None] = mapped_column(ForeignKey("residents.id"))
    visitor_name: Mapped[str] = mapped_column(String(120), nullable=False)
    visitor_phone: Mapped[str] = mapped_column(String(30), nullable=False)
    purpose: Mapped[str] = mapped_column(String(200), nullable=False)
    vehicle_number: Mapped[str | None] = mapped_column(String(40))
    visit_date: Mapped[date] = mapped_column(nullable=False)
    entry_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    exit_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[VisitorStatus] = mapped_column(
        Enum(VisitorStatus), default=VisitorStatus.EXPECTED, nullable=False
    )
    created_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
