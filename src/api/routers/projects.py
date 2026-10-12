from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...models import UserORM
from ...repositories import ProjectRepository
from ...schemas import Project, ProjectCreate, ProjectUpdate
from ...services import ProjectService
from ..dependencies import get_current_user

router = APIRouter(prefix='/projects', tags=['projects'])


def get_project_repo(
        db: Annotated[Session, Depends(get_db)]
    ) -> ProjectRepository:
    return ProjectRepository(db)

def get_project_service(
        repo: Annotated[ProjectRepository, Depends(get_project_repo)]
    ) -> ProjectService:
    return ProjectService(repo)


@router.get('/{id}', response_model=Project)
def get_project(
        uuid: UUID,
        service: Annotated[ProjectService, Depends(get_project_service)],
        current_user: Annotated[UserORM, Depends(get_current_user)]
    ):
    return service.get_by_uuid(uuid, current_user.uuid)

@router.get('', response_model=list[Project])
def get_all_projects(
        service: Annotated[ProjectService, Depends(get_project_service)],
        current_user: Annotated[UserORM, Depends(get_current_user)],
        limit: int = 10
    ):
    return service.get_all(limit, current_user.uuid)

@router.post('', status_code=201, response_model=Project)
def create_project(
        service: Annotated[ProjectService, Depends(get_project_service)],
        current_user: Annotated[UserORM, Depends(get_current_user)],
        payload: ProjectCreate
    ):
    return service.create(payload, current_user.uuid)

@router.patch('/{id}', response_model=Project)
def update_project(
        service: Annotated[ProjectService, Depends(get_project_service)],
        current_user: Annotated[UserORM, Depends(get_current_user)],
        id: UUID,
        payload: ProjectUpdate
    ):
    return service.update(id, payload, current_user.uuid)

@router.delete('/{id}', status_code=204)
def delete_project(
        service: Annotated[ProjectService, Depends(get_project_service)],
        current_user: Annotated[UserORM, Depends(get_current_user)],
        id: UUID,
    ):
    service.delete(id, current_user.uuid)
