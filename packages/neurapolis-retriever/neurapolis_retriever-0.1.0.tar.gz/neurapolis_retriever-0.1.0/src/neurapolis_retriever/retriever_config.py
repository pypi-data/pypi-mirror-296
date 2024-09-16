from pydantic import BaseModel


class RetrieverConfig(BaseModel):
    metadata_city_name: str
    metadata_user_name: str
    vector_search_limit: int
    keyword_search_limit: int
    vector_search_top_k: int
    keyword_search_top_k: int
    sub_vector_search_limit: int
    sub_keyword_search_limit: int
    sub_planner_relevant_hits_limit: int


retriever_config = RetrieverConfig(
    metadata_city_name="Freiburg",
    metadata_user_name="Julius Huck",
    vector_search_limit=5,
    keyword_search_limit=3,
    vector_search_top_k=15,
    keyword_search_top_k=8,
    sub_vector_search_limit=5,
    sub_keyword_search_limit=3,
    sub_planner_relevant_hits_limit=10,
)
