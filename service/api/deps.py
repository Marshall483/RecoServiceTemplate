from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing_extensions import Annotated


async def auth_required(authorization: Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())]) -> None:
    """
    Добавляем авторизацию
    """
