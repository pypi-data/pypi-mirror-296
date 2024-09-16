from datetime import datetime
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field

from neurapolis_retriever.retriever_config import retriever_config
from neurapolis_retriever.state.search import Search
from neurapolis_retriever.state.search_step import SearchStep
from neurapolis_retriever.state.search_type import SearchType
from neurapolis_retriever.state.state import State
from neurapolis_retriever.utilities.generate_llm_context_metadata import (
    generate_llm_context_metadata,
)


class SearchPlannerLlmDataModel(BaseModel):
    vector_search_querires: list[str] = Field(
        description="Die Suchanfragen, die der Retriever an die Vektordatenbank stellen soll"
    )
    keyword_search_queries: list[str] = Field(
        description="Die Suchanfragen, die der Retriever an die Keyword-Datenbank stellen soll"
    )


def planner_node(state: State):
    # TODO Beispiele
    # Sparse retrieval dense retrieval multi vector retrieval
    # TODO Reflect on generated searches in a loop
    # Step back prompting
    # Enrich queries with memory, that was generated in the relevance grading step
    # Filter out bad data in ETL
    # query must be in german
    # Reranker: https://jina.ai/reranker
    # smart chunking: https://medium.com/@hajar.mousannif/exploring-the-frontiers-of-text-segmentation-for-better-rag-systems-1b9f9af49258
    # splitting should use markdown headings again
    # max distance relanvance marginak
    # Stop word removal
    # Synonyms
    # Expansion terms
    # Reranking with model
    # Reflect on planner
    # Create more indices
    # Create easy schema
    # Functions for getting this and that.
    # - [ ] Get meetings of organization
    #     - [ ] When multiple orgs, ask again which one
    # - [ ] Try to answer question, reflect if info is missing for good answer, retry
    # - [ ] Reflect on found documents, is there something worth to explore? Is there some info that could be important to other gradings, searches? Update memory
    # - [ ] Loops on normal retrieval
    # - [x] Config
    # - [ ] Only send in chunks for grading
    # Give the retriever memory. when he found important information use it for generating the next query
    # make keywords more forgivable. more edits allowed. leave out stop words or straße abbreviations etc.
    prompt_template_string = """
    Generell:
    - Du bist Teil einer Retrieval Augmented Generation Anwendung. Diese besteht aus einem KI-Agenten, welcher aus mehreren LLM-Modulen besteht, welche zusammenarbeiten, um Nutzeranfragen zum Rats Informationssystem (RIS) zu beantworten.
    - Das RIS ist ein internes System für Politiker und städtische Mitarbeiter, das ihnen bei ihrer Arbeit hilft. Es ist eine Datenbank, welche Informationen einer bestimmten Stadt über Organisationen, Personen, Sitzungen, Dateien usw. enthält.
    - Ein menschlicher Mitarbeiter kommt zu dem KI-Agenten mit einer Nutzeranfrage/Frage, dessen Antworten sich in der Datenbank verstecken und ihr müsst die Frage so gut wie möglich beantworten.
    - Zur einfachen Durchsuchbarkeit wurden viele Daten durch ein Embeddingmodel als Vektoren embedded.

    Aufgabe:
    - Du bist der "Planner"-Mitarbeiter in dem KI-Agenten.
    - Du bist der erste, der die Nutzeranfrage verarbeitet.
    - Eine Nutzeranfrage kann auf mehrere Themenbereiche abzielen und wenn der "Retriever"-Mitarbeiter eine Suche mit einem gemischten Themenbereich auf der Datenbank durchführt, bekommt er sehr gemischte Treffer, wodurch die Nutzeranfragen nicht gut beantwortet werden kann.
    - Deine Aufgabe ist es, die Nutzeranfrage in spezifischere, genauere, abzielendere Suchanfragen zu konvertieren.
    - Diese Suchanfragen können entweder Vektorsuchen sein oder Keywordsuchen.
        - Vektorsuchen
            - Diese sollten zwar spezifisch sein, aber trotzdem noch einen sehr guten Detailgrad haben und ganze Sätz sein. Sehr kurze oder allgemeine Sätze führen dazu, dass der "Retriever"-Mitarbeiter sehr viele allgemeine Treffer bekommt, wodurch die Antwort auf die Nutzeranfrage dann sehr schwammig wird, oder oft die gleiche ist, weil oft eher die allgemeinen Dokumente aus der Datenbank zurückgegeben werden.
            - Gebe mindestens eine Vektorsuche an und maximal {vector_search_limit}.
        - Keywordsuchen
            - Diese sollten auf spezielle Keywords abzielen, diese Suchen sollten immer nur ein Wort sein. Keywords sollen aber auch auf keinen Fall sehr allgemeine, geläufige Wörter sein. Sondern eher bestimmte Aktenzeichen, Referenzen, Nummern, Namen, Orte, Straßennamen, Gebäudenamen, Firmennamen, etc.
            - Gebe mindestens eine Keywordsuche an und maximal {keyword_search_limit}.
    - Deine Antwort geht an den "Retriever"-Mitarbeiter, welcher dann mit den Suchanfragen die Dokumente aus der Datenbank holt.

    
    Aktuelles Datum und Uhrzeit: {formatted_current_datetime}

    
    Metadaten:

    <Metadaten>
    {metadata}
    </Metadaten>


    Nutzeranfrage, welche verarbeitet wird:

    <Nutzeranfrage>
    {query}
    </Nutzeranfrage>
    """
    prompt_template = ChatPromptTemplate.from_template(prompt_template_string)
    llm = AzureChatOpenAI(azure_deployment="gpt-4o", temperature=0.25)
    structured_llm = llm.with_structured_output(SearchPlannerLlmDataModel)
    chain = (
        {
            "vector_search_limit": lambda x: retriever_config.vector_search_limit,
            "keyword_search_limit": lambda x: retriever_config.keyword_search_limit,
            "formatted_current_datetime": lambda x: datetime.now().strftime(
                "%d.%m.%Y %H:%M"
            ),
            "metadata": lambda x: generate_llm_context_metadata(retriever_config),
            "query": itemgetter("query"),
        }
        | prompt_template
        | structured_llm
    )
    response: SearchPlannerLlmDataModel = chain.invoke(
        {
            "query": state.query,
        }
    )
    searches: list[Search] = []
    query_search = Search(
        step=SearchStep.PLANNED,
        type=SearchType.VECTOR,
        query=state.query,
    )
    searches.append(query_search)
    capped_vector_search_queries = response.vector_search_querires[
        : retriever_config.vector_search_limit
    ]
    for x_vector_search_query in capped_vector_search_queries:
        search = Search(
            step=SearchStep.PLANNED,
            type=SearchType.VECTOR,
            query=x_vector_search_query,
        )
        searches.append(search)
    capped_keyword_search_queries = response.keyword_search_queries[
        : retriever_config.keyword_search_limit
    ]
    for x_keyword_search_query in capped_keyword_search_queries:
        search = Search(
            step=SearchStep.PLANNED,
            type=SearchType.KEYWORD,
            query=x_keyword_search_query,
        )
        searches.append(search)
    return {"searches": searches}
