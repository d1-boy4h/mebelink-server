from uuid import UUID

from fastapi import HTTPException

from ..models import ProjectORM
from ..repositories import ProjectRepository
from ..schemas import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self._project_repo = project_repo

    def create(self, payload: ProjectCreate, owner_uuid: UUID) -> ProjectORM:
        return self._project_repo.create(owner_uuid, payload.title)

    def get_by_uuid(self, uuid: UUID, owner_uuid: UUID) -> ProjectORM:
        project = self._project_repo.get_by_uuid(uuid, owner_uuid)
        if project is None:
            raise HTTPException(status_code=404, detail='Проект не найден')

        return project

    def get_all(self, limit: int, owner_uuid: UUID) -> list[ProjectORM]:
        return self._project_repo.get_all(limit, owner_uuid)

    def update(
            self, uuid: UUID, payload: ProjectUpdate, owner_uuid: UUID
        ) -> ProjectORM:
        project = self.get_by_uuid(uuid, owner_uuid)
        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(project, field):
                setattr(project, field, value)

        return self._project_repo.save(project)

    def delete(self, uuid: UUID, owner_uuid: UUID):
        project = self.get_by_uuid(uuid, owner_uuid)
        self._project_repo.delete(project)
