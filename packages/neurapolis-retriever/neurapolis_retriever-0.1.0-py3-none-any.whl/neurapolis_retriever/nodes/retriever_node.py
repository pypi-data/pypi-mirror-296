import re

from neurapolis_common.models.file_chunk import FileChunk
from neurapolis_common.services.db_session_builder import db_session_builder
from neurapolis_common.services.embeddings import embeddings

from neurapolis_retriever.retriever_config import retriever_config
from neurapolis_retriever.state.hit import Hit
from neurapolis_retriever.state.hit_step import HitStep
from neurapolis_retriever.state.search import Search
from neurapolis_retriever.state.search_step import SearchStep
from neurapolis_retriever.state.search_type import SearchType


def escape_lucene_special_chars(query):
    special_chars = r'[+\-&|!(){}[\]^"~*?:\\]'
    return re.sub(special_chars, r"\\\g<0>", query)


def create_fuzzy_lucene_query(query):
    escaped_query = escape_lucene_special_chars(query)
    words = escaped_query.split()
    fuzzy_words = [f'"{word}"~' if " " in word else f"{word}~" for word in words]
    return " AND ".join(fuzzy_words)


# Search step is guaranteed to be PLANNED
def retriever_node(search: Search):
    file_chunks: list[FileChunk] = []
    if search.type == SearchType.VECTOR:
        with db_session_builder.build() as db_session:
            db_query = """
            CALL db.index.vector.queryNodes('file_chunks', $limit, $query_embedding)
            YIELD node as file_chunk_node, score
            RETURN file_chunk_node, score
            """
            query_embedding = embeddings.embed_query(search.query)
            db_results = db_session.run(
                db_query,
                query_embedding=query_embedding,
                limit=retriever_config.vector_search_top_k,
            )
            for x_db_result in db_results:
                file_chunk = FileChunk.from_db_node_dict(x_db_result["file_chunk_node"])
                file_chunks.append(file_chunk)
    elif search.type == SearchType.KEYWORD:
        with db_session_builder.build() as db_session:
            db_query = """
            CALL db.index.fulltext.queryNodes("file_chunk_texts", $fuzzy_lucene_query) YIELD node as file_chunk_node, score
            RETURN file_chunk_node, score
            LIMIT toInteger($limit)
            """
            fuzzy_lucene_query = create_fuzzy_lucene_query(search.query)
            db_results = db_session.run(
                db_query,
                fuzzy_lucene_query=fuzzy_lucene_query,
                limit=retriever_config.keyword_search_top_k,
            )
            file_chunks: list[FileChunk] = []
            for x_db_result in db_results:
                file_chunk = FileChunk.from_db_node_dict(x_db_result["file_chunk_node"])
                file_chunks.append(file_chunk)
    else:
        raise ValueError(f"Invalid search type: {search.type}")
    for file_chunk in file_chunks:
        hit = Hit(
            step=HitStep.RETRIEVED,
            file_chunk=file_chunk,
        )
        search.hits.append(hit)
    search.step = SearchStep.RETRIEVED
    return {"searches": [search]}
