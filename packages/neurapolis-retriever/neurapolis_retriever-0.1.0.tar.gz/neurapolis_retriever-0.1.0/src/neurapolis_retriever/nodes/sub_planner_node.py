from datetime import datetime
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field

from neurapolis_retriever.retriever_config import retriever_config
from neurapolis_retriever.state.hit import Hit
from neurapolis_retriever.state.hit_step import HitStep
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


def sub_planner_node(state: State):
    # TODO Beispiele
    prompt_template_string = """
    Generell:
    - Du bist Teil einer Retrieval Augmented Generation Anwendung. Diese besteht aus einem KI-Agenten, welcher aus mehreren LLM-Modulen besteht, welche zusammenarbeiten, um Nutzeranfragen zum Rats Informationssystem (RIS) zu beantworten.
    - Das RIS ist ein internes System für Politiker und städtische Mitarbeiter, das ihnen bei ihrer Arbeit hilft. Es ist eine Datenbank, welche Informationen einer bestimmten Stadt über Organisationen, Personen, Sitzungen, Dateien usw. enthält.
    - Ein menschlicher Mitarbeiter kommt zu dem KI-Agenten mit einer Nutzeranfrage/Frage, dessen Antworten sich in der Datenbank verstecken und ihr müsst die Frage so gut wie möglich beantworten.
    - Zur einfachen Durchsuchbarkeit wurden viele Daten durch ein Embeddingmodel als Vektoren embedded.

    Ablauf:
    - Du bist der "Sub-Planner"-Mitarbeiter in dem KI-Agenten.
    - Du bekommst vom "Retriever"-Mitarbeiter Treffer aus der Datenbank, welche vom "Relevance-Grader"-Mitarbeiter als relevant für die Nutzeranfrage gekennzeichnet wurden.
    - Deine Aufgabe ist es, aus diesen Treffern weitere Suchanfragen zu extrahieren, welche der "Retriever"-Mitarbeiter dann wieder in der Datenbank suchen kann.
    - Diese Suchanfragen können entweder Vektorsuchen sein oder Keywordsuchen.
        - Vektorsuchen
            - Diese sollten zwar spezifisch sein, aber trotzdem noch einen sehr guten Detailgrad haben und ganze Sätz sein. Sehr kurze oder allgemeine Sätze führen dazu, dass der "Retriever"-Mitarbeiter sehr viele allgemeine Treffer bekommt, wodurch die Antwort auf die Nutzeranfrage dann sehr schwammig wird, oder oft die gleiche ist, weil oft eher die allgemeinen Dokumente aus der Datenbank zurückgegeben werden.
            - Gebe mindestens eine Vektorsuche an und maximal {sub_vector_search_limit}.
        - Keywordsuchen
            - Diese sollten auf spezielle Keywords abzielen, diese Suchen sollten immer nur ein Wort sein. Keywords sollen aber auch auf keinen Fall sehr allgemeine, geläufige Wörter sein. Sondern eher bestimmte Aktenzeichen, Referenzen, Nummern, Namen, Orte, Straßennamen, Gebäudenamen, Firmennamen, etc.
            - Gebe mindestens eine Keywordsuche an und maximal {sub_keyword_search_limit}.
    - Deine Antwort geht an den "Retriever"-Mitarbeiter, welcher dann mit den Suchanfragen die Dokumente aus der Datenbank holt.

    Zum tieferen Verständnis:
    - Es geht hierbei um eine Art vertiefende Suche.
    - Im ersten Durchlauf wurden einige relevante Dokumente gefunden und jetzt geht es darum noch mehr Details zu diesen Dokumenten zu finden.
    - Das ganze ist so, als ob man bei Wikipedia eine, für seine Frage, relevante Seite gefunden hat und dann weitere Links auf dieser Seite öffnet, um mehr und tiefer über das Thema zu erfahren. Diese weiteren "Links" sollst du aus den relevanten Treffern extrahieren.

    Beispiele:
    - Nutzeranfrage 1: "Wie war die Verkehrssituation in der Innenstadt im letzten Jahr?"
    - Themenbereiche 1: "Verkehrsaufkommen in der Freiburger Innenstadt 2023\nStauprobleme und Lösungsansätze in Freiburg\nÖPNV-Nutzung und -Ausbau in der Freiburger Innenstadt"

    - Nutzeranfrage 2: "Wie hat sich der Wohnungsmarkt in Freiburg entwickelt?"
    - Themenbereiche 2: "Entwicklung der Mietpreise in Freiburg\nNeubaugebiete und Wohnungsbauprojekte in Freiburg\nSozialwohnungen und bezahlbarer Wohnraum in Freiburg"

    - Nutzeranfrage 3: "Was wurde über die Sanierung des Rathauses beschlossen?"
    - Themenbereiche 3: "Beschlüsse zur Rathaussanierung in Freiburg\nKosten und Finanzierung der Freiburger Rathaussanierung\nZeitplan und Phasen der Rathaussanierung\nEnergetische Maßnahmen bei der Rathaussanierung"

    
    Aktuelles Datum und Uhrzeit: {formatted_current_datetime}


    Metadaten:

    <Metadaten>
    {metadata}
    </Metadaten>


    Nutzeranfrage, welche du verarbeiten sollst:

    <Nutzeranfrage>
    {query}
    </Nutzeranfrage>


    Dokumente, welche du verarbeiten sollst:

    <Treffer>
    {hits_xml}
    </Treffer>
    """
    prompt_template = ChatPromptTemplate.from_template(prompt_template_string)
    llm = AzureChatOpenAI(azure_deployment="gpt-4o-mini", temperature=0.25)
    structured_llm = llm.with_structured_output(SearchPlannerLlmDataModel)
    chain = (
        {
            "sub_vector_search_limit": lambda x: retriever_config.sub_vector_search_limit,
            "sub_keyword_search_limit": lambda x: retriever_config.sub_keyword_search_limit,
            "formatted_current_datetime": lambda x: datetime.now().strftime(
                "%d.%m.%Y %H:%M"
            ),
            "metadata": lambda x: generate_llm_context_metadata(retriever_config),
            "query": itemgetter("query"),
            "hits_xml": itemgetter("hits")
            | RunnableLambda(Hit.format_hits_to_inner_xml),
        }
        | prompt_template
        | structured_llm
    )
    related_data_gathered_hits: list[Hit] = []
    for x_search in state.searches:
        if x_search.step != SearchStep.RELATED_DATA_GATHERED:
            continue
        for y_hit in x_search.hits:
            if y_hit.step != HitStep.RELATED_DATA_GATHERED:
                continue
            related_data_gathered_hits.append(y_hit)
    by_relevance_sorted_hits = sorted(
        related_data_gathered_hits,
        key=lambda hit: hit.grading.is_relevant,
        reverse=True,
    )
    top_relevant_hits = by_relevance_sorted_hits[
        : retriever_config.sub_planner_relevant_hits_limit
    ]
    response: SearchPlannerLlmDataModel = chain.invoke(
        {
            "query": state.query,
            "hits": top_relevant_hits,
        }
    )
    searches: list[Search] = []
    capped_vector_search_queries = response.vector_search_querires[
        : retriever_config.sub_vector_search_limit
    ]
    for x_vector_search_query in capped_vector_search_queries:
        search = Search(
            level=1,
            step=SearchStep.PLANNED,
            type=SearchType.VECTOR,
            query=x_vector_search_query,
        )
        searches.append(search)
    capped_keyword_search_queries = response.keyword_search_queries[
        : retriever_config.sub_keyword_search_limit
    ]
    for x_keyword_search_query in capped_keyword_search_queries:
        search = Search(
            level=1,
            step=SearchStep.PLANNED,
            type=SearchType.KEYWORD,
            query=x_keyword_search_query,
        )
        searches.append(search)
    return {"searches": searches}
