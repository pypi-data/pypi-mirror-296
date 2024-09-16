from typing import Annotated

from pydantic import BaseModel, Field

from .search import Search


def merge_searches(
    existing_searches: list[Search], new_searches: list[Search]
) -> list[Search]:
    merged_searches = {}
    for search in existing_searches:
        merged_searches[search.id] = search
    for new_search in new_searches:
        merged_searches[new_search.id] = new_search
    return list(merged_searches.values())


class State(BaseModel):
    query: str = Field()
    searches: Annotated[list[Search], merge_searches] = Field(default=[])
