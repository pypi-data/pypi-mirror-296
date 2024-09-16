from typing import Optional

from pydantic import BaseModel, Field

from .grading import Grading


class RelatedDataState(BaseModel):
    text: str = Field()
    node_datas: list[dict] = Field()
    grading: Optional[Grading] = Field(default=None)
