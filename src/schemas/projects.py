from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ..core import ProjectStatus


class ProjectCreate(BaseModel):
    title: str

class ProjectUpdate(BaseModel):
    title: str | None = None
    status: ProjectStatus | None = None
    is_improvements: bool | None = None
    created_date: datetime | None = None
    start_date: date | None = None
    end_date: date | None = None
    address: str | None = None
    phone: str | None = None

class Project(ProjectUpdate):
    uuid: UUID = Field(default_factory=uuid4)
