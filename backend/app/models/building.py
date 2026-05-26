from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Building(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "buildings"
    __table_args__ = (UniqueConstraint("society_id", "name", name="uq_building_society_name"),)

    society_id: Mapped[str] = mapped_column(ForeignKey("societies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    society = relationship("Society", back_populates="buildings")
    flats = relationship("Flat", back_populates="building")
