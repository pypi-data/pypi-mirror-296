from langgraph.constants import Send

from neurapolis_retriever.state.search_step import SearchStep
from neurapolis_retriever.state.state import State


def after_sub_planner_continue_to_sub_retrievers_edge(state: State) -> list[Send]:
    sends = []
    for x_search in state.searches:
        if x_search.step != SearchStep.PLANNED:
            continue
        sends.append(Send("sub_retriever", x_search))
    return sends
