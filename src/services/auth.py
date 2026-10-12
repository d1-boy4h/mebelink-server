from fastapi import HTTPException

from ..core import create_access_token, hash_password, verify_password
from ..models import UserORM
from ..repositories import UserRepository
from ..schemas import Token, UserCreate


class AuthService:
    '''Сервис регистрации и авторизации пользователей.'''

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def register(self, payload: UserCreate) -> UserORM:
        '''Регистрация.'''

        if self._user_repo.get_by_email(payload.email) is not None:
            raise HTTPException(
                status_code=409,
                detail='Эта почта уже зарегистрирована'
            )

        return self._user_repo.create(
            payload.email,
            hash_password(payload.password)
        )

    def authenticate(self, email: str, password: str) -> Token:
        '''Авторизация.'''

        user = self._user_repo.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail='Неверный логин или пароль'
            )

        return Token(
            access_token=create_access_token(user.uuid),
            token_type='bearer'
        )
