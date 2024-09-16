from neurapolis_retriever.retriever_config import RetrieverConfig


def generate_llm_context_metadata(retriever_config: RetrieverConfig):
    return f"""
    - Deutsche Stadt: {retriever_config.metadata_city_name}
    - Name des Nutzers mit der Anfrage: {retriever_config.metadata_user_name}
    """
