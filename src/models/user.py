from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database.database import Base


class UserORM(Base):
    __tablename__ = 'users'

    uuid: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    email: Mapped[str | None] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
