import jwt
import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from service.log import access_logger, app_logger
from service.models import Error
from service.response import server_error

from fastapi.requests import HTTPConnection
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthenticationBackend, AuthenticationError


from core.settings import settings


class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return None

        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            raise AuthenticationError("Not authentication")

        if scheme.lower() != "bearer":
            raise AuthenticationError("Invalid authentication scheme")

        try:
            jwt.decode(credentials, key=settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM],
                       options={"verify_signature": True})
        except Exception:
            raise AuthenticationError("Invalid JWT token")

class AccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        started_at = time.perf_counter()
        response = await call_next(request)
        request_time = time.perf_counter() - started_at

        status_code = response.status_code

        access_logger.info(
            msg="",
            extra={
                "request_time": round(request_time, 4),
                "status_code": status_code,
                "requested_url": request.url,
                "method": request.method,
            },
        )
        return response


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as e:  # pylint: disable=W0703,W1203
            app_logger.exception(msg=f"Caught unhandled {e.__class__} exception: {e}")
            error = Error(error_key="server_error", error_message="Internal Server Error")
            return server_error([error])


def add_middlewares(app: FastAPI) -> None:
    # do not change order
    app.add_middleware(ExceptionHandlerMiddleware)
    app.add_middleware(AccessMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
