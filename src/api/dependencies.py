from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..core import decode_access_token
from ..database import get_db
from ..models import UserORM
from ..repositories import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)]
    ) -> UserORM:
    user_id = decode_access_token(token)
    repo = UserRepository(db)
    user = repo.get_by_uuid(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail='Невалидный токен')

    return user
