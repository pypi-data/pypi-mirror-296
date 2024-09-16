from langgraph.constants import Send

from neurapolis_retriever.state.search_step import SearchStep
from neurapolis_retriever.state.state import State


def after_sub_cleaner_continue_to_sub_relevance_graders_edge(
    state: State,
) -> list[Send]:
    sends = []
    for x_search in state.searches:
        if x_search.step != SearchStep.UNDOUBLED:
            continue
        sends.append(Send("sub_relevance_grader", x_search))
    return sends
