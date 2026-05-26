from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Resident(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "residents"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    society_id: Mapped[str] = mapped_column(ForeignKey("societies.id"), nullable=False)
    flat_id: Mapped[str] = mapped_column(ForeignKey("flats.id"), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    is_owner: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="resident_profile")
    flat = relationship("Flat", back_populates="residents")
