import random
from typing import List

from fastapi import APIRouter, FastAPI, Request, status
from pydantic import BaseModel

from schemas.base import Error, Message
from service.api.exceptions import ModelNotFoundError, UserNotFoundError
from service.log import app_logger


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


router = APIRouter()


@router.get(
    path="/health",
    tags=["Health"],
)
@router.get(path="/health", tags=["Health"], response_model=RecoResponse)
async def health() -> str:
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": Error,
            "description": "Not enough privileges",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": Message,
            "description": "Model was not found",
        },
    },
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    if model_name == "top":
        recomend = list(range(10))
    elif model_name == "random":
        recomend = [random.randint(0, 100) for _ in range(10)]
    else:
        raise ModelNotFoundError()

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    return RecoResponse(user_id=user_id, items=recomend)


def add_views(app: FastAPI) -> None:
    app.include_router(router)
