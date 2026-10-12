from uuid import UUID

from sqlalchemy.orm import Session

from ..models import UserORM


class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(self, email: str, password_hash: str) -> UserORM:
        user = UserORM(email=email, password_hash=password_hash)

        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)

        return user

    def get_by_uuid(self, uuid: UUID) -> UserORM | None:
        return self._db.get(UserORM, uuid)

    def get_by_email(self, email: str) -> UserORM | None:
        return self._db.query(UserORM).filter(UserORM.email == email).first()

    def get_all(self, limit: int) -> list[UserORM]:
        query = self._db.query(UserORM)
        return query.limit(limit).all()

    def save(self, user: UserORM) -> UserORM:
        self._db.commit()
        self._db.refresh(user)

        return user

    def delete(self, user: UserORM):
        self._db.delete(user)
        self._db.commit()
