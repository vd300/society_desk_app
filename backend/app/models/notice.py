from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import NoticeTargetType


class Notice(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "notices"

    society_id: Mapped[str] = mapped_column(ForeignKey("societies.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    target_type: Mapped[NoticeTargetType] = mapped_column(
        Enum(NoticeTargetType), default=NoticeTargetType.ALL, nullable=False
    )
    building_id: Mapped[str | None] = mapped_column(ForeignKey("buildings.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
