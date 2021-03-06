from datetime import timedelta, datetime
from typing import Union, Any
from jose import jwt
from pydantic import ValidationError
from api.exceptions import InvalidCredentialsException
from core.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


async def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.ENCRYPT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def decode_user_id_from_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.ENCRYPT_KEY, algorithms=[ALGORITHM])
    except(jwt.JWTError, ValidationError):
        raise InvalidCredentialsException(token=token)
    return int(payload['sub'])
