from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Society(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "societies"

    name: Mapped[str] = mapped_column(String(160), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)

    buildings = relationship("Building", back_populates="society")
    flats = relationship("Flat", back_populates="society")
