from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Flat(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "flats"
    __table_args__ = (
        UniqueConstraint("building_id", "flat_number", name="uq_flat_building_number"),
    )

    society_id: Mapped[str] = mapped_column(ForeignKey("societies.id"), nullable=False)
    building_id: Mapped[str] = mapped_column(ForeignKey("buildings.id"), nullable=False)
    flat_number: Mapped[str] = mapped_column(String(40), nullable=False)
    floor_number: Mapped[int] = mapped_column(nullable=False)
    maintenance_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    society = relationship("Society", back_populates="flats")
    building = relationship("Building", back_populates="flats")
    residents = relationship("Resident", back_populates="flat")
    dues = relationship("MaintenanceDue", back_populates="flat")
