from typing import Dict, Any
from jose import jwt, JWTError
from .config import settings


class InvalidTokenError(Exception):
    pass


def decode_jwt_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
        )
        return payload
    except JWTError as exc:
        raise InvalidTokenError(str(exc))
