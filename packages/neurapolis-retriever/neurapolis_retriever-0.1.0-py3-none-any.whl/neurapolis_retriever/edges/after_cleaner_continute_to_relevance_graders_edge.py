from langgraph.constants import Send

from neurapolis_retriever.state.search_step import SearchStep
from neurapolis_retriever.state.state import State


def after_cleaner_continute_to_relevance_graders_edge(state: State) -> list[Send]:
    sends = []
    for x_search in state.searches:
        if x_search.step != SearchStep.UNDOUBLED:
            continue
        sends.append(Send("relevance_grader", x_search))
    return sends
