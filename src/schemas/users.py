from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    uuid: UUID
    email: EmailStr