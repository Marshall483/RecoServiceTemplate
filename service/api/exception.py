import typing as tp
from http import HTTPStatus
from typing import Awaitable, Callable

from fastapi.requests import Request
from pydantic import BaseModel


class Message(BaseModel):
    message: str


class Error(BaseModel):
    detail: str


class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        error_key: str,
        error_message: str = "",
        error_loc: tp.Optional[tp.Sequence[str]] = None,
    ) -> None:
        self.error_key = error_key
        self.error_message = error_message
        self.error_loc = error_loc
        self.status_code = status_code
        super().__init__()


class UserNotFoundError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.NOT_FOUND,
        error_key: str = "user_not_found",
        error_message: str = "User is unknown",
        error_loc: tp.Optional[tp.Sequence[str]] = None,
    ):
        super().__init__(status_code, error_key, error_message, error_loc)


class ModelNotFoundError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.NOT_FOUND,
        error_key: str = "model_not_found",
        error_message: str = "Model is unknown",
        error_loc: tp.Optional[tp.Sequence[str]] = None,
    ):
        super().__init__(status_code, error_key, error_message, error_loc)


class UnauthorizedError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.UNAUTHORIZED,
        error_key: str = "user_not_found",
        error_message: str = "User is unauthorized",
        error_loc: tp.Optional[tp.Sequence[str]] = None,
    ):
        super().__init__(status_code, error_key, error_message, error_loc)


async def json_exceptions_wrapper_middleware(request: Request, call_next: Callable[[Request], Awaitable]):
    """
    JSONResponse exception wrapping
    """
