import uuid
from typing import Optional

from pydantic import BaseModel, Field

from .hit import Hit
from .search_step import SearchStep
from .search_type import SearchType


class Search(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    level: int = Field(default=0)
    step: SearchStep = Field()
    type: SearchType = Field()
    query: str = Field()
    hits: list[Hit] = Field(default=[])
