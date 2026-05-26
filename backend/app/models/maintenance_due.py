from datetime import date
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import DueStatus


class MaintenanceDue(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "maintenance_dues"
    __table_args__ = (
        UniqueConstraint("flat_id", "month", "year", name="uq_due_flat_month_year"),
    )

    society_id: Mapped[str] = mapped_column(ForeignKey("societies.id"), nullable=False)
    flat_id: Mapped[str] = mapped_column(ForeignKey("flats.id"), nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[DueStatus] = mapped_column(
        Enum(DueStatus), default=DueStatus.UNPAID, nullable=False
    )
    due_date: Mapped[date] = mapped_column(nullable=False)

    flat = relationship("Flat", back_populates="dues")
    payments = relationship("Payment", back_populates="maintenance_due")
