from datetime import UTC, datetime, timedelta
from uuid import UUID

import bcrypt
from fastapi import HTTPException
from jose import JWTError, jwt

from .config import settings


def hash_password(password: str) -> str:
    '''Хеширование пароля.'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hash: str) -> bool:
    '''Верификация пароля.'''
    return bcrypt.checkpw(password.encode(), hash.encode())

def create_access_token(user_uuid: UUID) -> str:
    '''Создание JWT-токена.'''

    expire = datetime.now(tz=UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {'sub': str(user_uuid), 'exp': expire}

    return jwt.encode(payload, settings.secret_key)

def decode_access_token(token: str) -> UUID:
    '''Проверка подписи токена.'''

    try:
        payload = jwt.decode(token, settings.secret_key)
        return UUID(payload['sub'])

    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail='Невалидный токен')
