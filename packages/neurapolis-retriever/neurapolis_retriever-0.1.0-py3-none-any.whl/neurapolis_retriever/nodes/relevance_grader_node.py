from datetime import datetime
from operator import itemgetter
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import AzureChatOpenAI

from neurapolis_retriever.retriever_config import retriever_config
from neurapolis_retriever.state.grading import Grading
from neurapolis_retriever.state.hit import Hit
from neurapolis_retriever.state.hit_step import HitStep
from neurapolis_retriever.state.search import Search
from neurapolis_retriever.state.search_step import SearchStep
from neurapolis_retriever.utilities.generate_grading_llm_data_model import (
    generate_grading_llm_data_model,
)
from neurapolis_retriever.utilities.generate_llm_context_metadata import (
    generate_llm_context_metadata,
)


# Search step is guaranteed to be UNDOUBLED
def relevance_grader_node(search: Search):
    unique_hits = list(
        filter(lambda x_hit: x_hit.step == HitStep.NOT_DOUBLED, search.hits)
    )
    if len(unique_hits) == 0:
        search.step = SearchStep.RELEVANCE_GRADED
        return {"searches": [search]}
    prompt_template_string = """ 
    Generell: ENSURE TO OUTPUT THE DATA MODEL FOR ALL HITS! THIS IS IMPORTANT!
    

    
    - Du bist Teil einer Retrieval Augmented Generation Anwendung. Diese besteht aus einem KI-Agenten, welcher aus mehreren LLM-Modulen besteht, welche zusammenarbeiten, um Nutzeranfragen zum Rats Informationssystem (RIS) zu beantworten.
    - Das RIS ist ein internes System für Politiker und städtische Mitarbeiter, das ihnen bei ihrer Arbeit hilft. Es ist eine Datenbank, welche Informationen einer bestimmten Stadt über Organisationen, Personen, Sitzungen, Dateien usw. enthält.
    - Ein menschlicher Mitarbeiter kommt zu dem KI-Agenten mit einer Nutzeranfrage/Frage, dessen Antworten sich in der Datenbank verstecken und ihr müsst die Frage so gut wie möglich beantworten.
    - Zur einfachen Durchsuchbarkeit wurden viele Daten durch ein Embeddingmodel als Vektoren embedded.
    
    Ablauf:
    - Du bist der "Relevance Grader"-Mitarbeiter in dem KI-Agenten.
    - Du bekommst vom "Retriever"-Mitarbeiter einen Treffer aus der Datenbank, welchen er relevant für die Nutzeranfrage hält.
    - Deine Aufgabe ist es, den Treffer zu bewerten, ob dieser relevant für die Beantwortung der Nutzeranfrage ist oder nicht.
    - Sei dabei nicht zu streng. Der Treffer kann auch nur teilweise relevant sein, oder entfernt über eine Verbindung relevant sein.
    - Wenn es also schon nur sehr sehr weit entfernt um das richtige Thema oder die richtigen Personen, Objekte, Gebäude, Orte, etc. geht, ist der Treffer relevant.
    - Treffer, welche du als irrelevant kennzeichnest, werden am Ende nicht zur Beantwortung der Nutzeranfrage zu Rate gezogen.
    Beispiele:
    
    - Nutzeranfrage 1: "Welche Projekte zur Stadtentwicklung wurden im letzten Quartal genehmigt?"
    - Treffer 1: "Beschlussvorlage zur Erweiterung des Stadtparks vom 10.09.2023..."
    - Antwort 1: 
      is_hit_relevant: True
      hit_feedback: "Relevant, da es sich um ein kürzlich genehmigtes Stadtentwicklungsprojekt handelt, das zur Beantwortung der Frage beitragen kann."

    - Nutzeranfrage 2: "Welche Maßnahmen wurden zur Verbesserung der Radwege beschlossen?"
    - Treffer 2: "Antrag zur Erhöhung der Hundesteuer..."
    - Antwort 2:
      is_hit_relevant: False
      hit_feedback: "Irrelevant, da dies ein Antrag zur Hundesteuer ist und nichts mit Radwegen zu tun hat."

    - Nutzeranfrage 3: "Wer ist der aktuelle Oberbürgermeister von Freiburg?"
    - Treffer 3: "Lebenslauf von Martin Horn, Oberbürgermeister der Stadt Freiburg..."
    - Antwort 3:
      is_hit_relevant: True
      hit_feedback: "Relevant, da es Informationen über den aktuellen Oberbürgermeister von Freiburg enthält."
    

    Aktuelles Datum und Uhrzeit: {formatted_current_datetime}


    Metadaten:

    <Metadaten>
    {metadata}
    </Metadaten>


    Nutzeranfrage, welche verarbeitet wird:

    <Nutzeranfrage>
    {query}
    </Nutzeranfrage>


    Treffer, welchen du verarbeiten sollst:

    <Treffer>
    {hit_xml}
    </Treffer>
    
    ENSURE TO OUTPUT THE DATA MODEL FOR THE HIT! THIS IS IMPORTANT! IF THERE ARE MISSING DATA MODEL FIELDS, YOU WILL BE PENALIZED!
    """
    prompt_template = ChatPromptTemplate.from_template(prompt_template_string)
    llm = AzureChatOpenAI(model="gpt-4o-mini", temperature=0.25)
    LlmDataModel = generate_grading_llm_data_model()
    structured_llm = llm.with_structured_output(LlmDataModel)
    chain = (
        {
            "formatted_current_datetime": lambda x: datetime.now().strftime(
                "%d.%m.%Y %H:%M"
            ),
            "metadata": lambda x: generate_llm_context_metadata(retriever_config),
            "query": itemgetter("query"),
            "hit_xml": itemgetter("hit") | RunnableLambda(Hit.format_hit_to_inner_xml),
        }
        | prompt_template
        | structured_llm
    )

    hit_id_to_grading_map: dict[str, Grading] = {}

    def process_hit(x_unique_hit):
        response = chain.invoke({"query": search.query, "hit": x_unique_hit})
        is_relevant = response.is_hit_relevant
        feedback = response.hit_feedback
        return x_unique_hit.id, Grading(is_relevant=is_relevant, feedback=feedback)

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_hit = {executor.submit(process_hit, hit): hit for hit in unique_hits}
        for future in as_completed(future_to_hit):
            hit_id, grading = future.result()
            hit_id_to_grading_map[hit_id] = grading

    for x_hit in search.hits:
        if x_hit.step != HitStep.NOT_DOUBLED:
            continue
        grading = hit_id_to_grading_map[x_hit.id]
        x_hit.grading = grading
        x_hit.step = HitStep.RELEVANCE_GRADED
    search.step = SearchStep.RELEVANCE_GRADED
    return {"searches": [search]}
