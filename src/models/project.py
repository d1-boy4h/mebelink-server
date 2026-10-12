from datetime import UTC, date, datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from ..core import ProjectStatus
from ..database import Base


class ProjectORM(Base):
    __tablename__ = 'projects'

    uuid: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    owner_uuid: Mapped[UUID] = mapped_column(
        ForeignKey('users.uuid'), nullable=False
    )

    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[ProjectStatus] = mapped_column(
        String(16),
        nullable=False,
        default=ProjectStatus.NOT_IN_PROGRESS
    )
    is_improvements: Mapped[bool] = mapped_column(
        nullable=False,
        default=False
    )
    created_date: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(tz=UTC)
    )
    start_date: Mapped[date] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(tz=UTC).date()
    )
    end_date: Mapped[date | None]
    address: Mapped[str | None]
    phone: Mapped[str | None]

    @validates('title')
    def validate_title(self, _, value):
        if not value or not value.strip():
            return 'Без названия'

        return value
