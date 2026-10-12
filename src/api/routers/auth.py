from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...repositories import UserRepository
from ...schemas import Token, User, UserCreate
from ...services import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


def get_user_repo(
        db: Annotated[Session, Depends(get_db)]
    ) -> UserRepository:
    return UserRepository(db)

def get_auth_service(
        repo: Annotated[UserRepository, Depends(get_user_repo)]
    ) -> AuthService:
    return AuthService(repo)


@router.post('/register', status_code=201, response_model=User)
def register(
        service: Annotated[AuthService, Depends(get_auth_service)],
        payload: UserCreate
    ):
    return service.register(payload)

@router.post('/login', response_model=Token)
def login(
        service: Annotated[AuthService, Depends(get_auth_service)],
        payload: UserCreate
    ):
    return service.authenticate(payload.email, payload.password)
