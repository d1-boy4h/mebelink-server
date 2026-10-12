from uuid import UUID

from sqlalchemy.orm import Session

from ..models import ProjectORM


class ProjectRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(self, owner_uuid: UUID,  title: str) -> ProjectORM:
        project = ProjectORM(title=title, owner_uuid=owner_uuid)

        self._db.add(project)
        self._db.commit()
        self._db.refresh(project)

        return project

    def get_by_uuid(
            self, project_id: UUID, owner_uuid: UUID
        ) -> ProjectORM | None:
        return (self._db.query(ProjectORM)
            .filter(
                ProjectORM.uuid == project_id,
                ProjectORM.owner_uuid == owner_uuid
            )
            .first()
        )

    def get_all(self, limit: int, owner_uuid: UUID) -> list[ProjectORM]:
            projects = self._db.query(ProjectORM).filter(
                ProjectORM.owner_uuid == owner_uuid
            )

            return projects.limit(limit).all()

    def save(self, project: ProjectORM) -> ProjectORM:
        self._db.commit()
        self._db.refresh(project)

        return project

    def delete(self, project: ProjectORM):
        self._db.delete(project)
        self._db.commit()
