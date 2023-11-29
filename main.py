import os
import uvicorn
from functools import partial

from fastapi.middleware.cors import CORSMiddleware

from service.settings import settings
from service.api.middlewares import JWTAuthBackend, JWTAuthenticationMiddleware
from service.api.exception import json_exceptions_wrapper_middleware
from service.api.app import create_app
from service.settings import get_config

config = get_config()
app = create_app(config)


if __name__ == "__main__":

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8080"))

    uvicorn.run(app, host=host, port=port)

    # MIDDLEWARES
    app.add_middleware(JWTAuthenticationMiddleware, backend=JWTAuthBackend())
    app.middleware("http")(partial(json_exceptions_wrapper_middleware))
    app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
