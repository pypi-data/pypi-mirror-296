import uuid
from typing import List

from langchain_core.documents import Document

from neurapolis_retriever.graph import graph
from neurapolis_retriever.quality_config import QualityConfig
from neurapolis_retriever.state.article import check_are_articles_equal
from neurapolis_retriever.state.topic_state import TopicState


class ArchiveRetriever:
    def __init__(self, quality_config: QualityConfig):
        self._quality_config = quality_config

    def retrieve(self, query: str) -> List[Document]:
        result = graph.invoke(
            {
                "quality_config": vars(self._quality_config),
                "query": query,
                "topics": [
                    {
                        "id": str(uuid.uuid4()),
                        "state": TopicState.INITIAL,
                        "title": query,
                        "is_relevant": True,
                        "feedback": "Dies ist die rohe Nutzeranfrage",
                    }
                ],
                "stories": [],
            },
            config={
                "recursion_limit": 100,
            },
        )
        articles = []
        for source in result["topics"] + result["stories"]:
            for article in source["articles"]:
                is_duplicate = False
                for existing_article in articles:
                    if check_are_articles_equal(article, existing_article):
                        is_duplicate = True
                        break
                if not article["is_relevant"] or article["is_doubled"] or is_duplicate:
                    continue
                articles.append(article)
        documents = []
        for article in articles:
            document = Document(
                page_content=article["text"], metadata=article["document"].metadata
            )
            documents.append(document)
        return documents
