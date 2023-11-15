import enum
import typing as tp
from typing import List

from pydantic import BaseModel


class Error(BaseModel):
    error_key: str
    error_message: str
    error_loc: tp.Optional[tp.Any] = None


class ModelNamesEnum(str, enum.Enum):
    TEST = "test"


class ModelRetrieveSchema(BaseModel):
    user_id: str
    items: List[int]
