from typing import List

from fastapi import APIRouter, FastAPI, Request, status
from pydantic import BaseModel

from service.log import app_logger
from service.modelService import ModelService

from .exception import Message, ModelNotFoundError, UserNotFoundError


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


router = APIRouter()


@router.get(path="/health", tags=["Health"], response_model=str)
async def health() -> str:
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": Message,
            "description": "Not found",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Message,
            "description": "Invalid token proveded",
        },
    },
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    service: ModelService = request.app.state.model_service

    if model_name == "popular":
        recomend = service.get_popular_prediction()
    elif model_name == "user_knn":
        recomend = service.get_user_knn_prediction(user_id)
    elif model_name == "rc_rcts_ann":
        recomend = service.get_rc_rcts_ann(user_id)
    else:
        raise ModelNotFoundError()

    return RecoResponse(user_id=user_id, items=recomend)


def add_views(app: FastAPI) -> None:
    app.include_router(router)
