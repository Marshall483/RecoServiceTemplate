import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, Dict

import uvloop
from fastapi import FastAPI
from settings import ServiceConfig

__all__ = ("create_app",)


def setup_asyncio(thread_name_prefix: str) -> None:
    uvloop.install()

    loop = asyncio.get_event_loop()

    executor = ThreadPoolExecutor(thread_name_prefix=thread_name_prefix)
    loop.set_default_executor(executor)

    def handler(_, context: Dict[str, Any]) -> None:
        message = "Caught asyncio exception: {message}".format_map(context)
        app_logger.warning(message)

    loop.set_exception_handler(handler)


def create_app(config: ServiceConfig) -> FastAPI:
    setup_asyncio(thread_name_prefix=config.service_name)

    app = FastAPI(debug=False)
    app.state.k_recs = config.k_recs

    return app
