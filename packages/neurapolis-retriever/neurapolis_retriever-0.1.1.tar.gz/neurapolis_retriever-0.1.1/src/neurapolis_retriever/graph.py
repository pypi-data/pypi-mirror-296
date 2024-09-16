from langgraph.graph import END, StateGraph

from neurapolis_retriever.edges.after_cleaner_continute_to_relevance_graders_edge import (
    after_cleaner_continute_to_relevance_graders_edge,
)
from neurapolis_retriever.edges.after_planner_continue_to_retrievers_edge import (
    after_planner_continue_to_retrievers_edge,
)
from neurapolis_retriever.edges.after_sub_cleaner_continue_to_sub_relevance_graders_edge import (
    after_sub_cleaner_continue_to_sub_relevance_graders_edge,
)
from neurapolis_retriever.edges.after_sub_planner_continue_to_sub_retrievers_edge import (
    after_sub_planner_continue_to_sub_retrievers_edge,
)
from neurapolis_retriever.nodes.cleaner_node import cleaner_node
from neurapolis_retriever.nodes.planner_node import planner_node
from neurapolis_retriever.nodes.related_data_gatherer_node import (
    related_data_gatherer_node,
)
from neurapolis_retriever.nodes.relevance_grader_node import relevance_grader_node
from neurapolis_retriever.nodes.retriever_node import retriever_node
from neurapolis_retriever.nodes.sub_planner_node import sub_planner_node
from neurapolis_retriever.state.state import State

graph_builder = StateGraph(State)

graph_builder.add_node("planner", planner_node)
graph_builder.add_node("retriever", retriever_node)
graph_builder.add_node("cleaner", cleaner_node)
graph_builder.add_node("relevance_grader", relevance_grader_node)
# graph_builder.add_node("sub_planner", sub_planner_node)
# graph_builder.add_node("sub_retriever", retriever_node)
# graph_builder.add_node("sub_cleaner", cleaner_node)
# graph_builder.add_node("sub_relevance_grader", relevance_grader_node)
graph_builder.add_node("related_data_gatherer", related_data_gatherer_node)

graph_builder.set_entry_point("planner")
graph_builder.add_conditional_edges(
    "planner", after_planner_continue_to_retrievers_edge, ["retriever"]
)
graph_builder.add_edge("retriever", "cleaner")
graph_builder.add_conditional_edges(
    "cleaner",
    after_cleaner_continute_to_relevance_graders_edge,
    ["relevance_grader"],
)
graph_builder.add_edge("relevance_grader", "related_data_gatherer")
# graph_builder.add_conditional_edges(
#     "sub_planner", after_sub_planner_continue_to_sub_retrievers_edge, ["sub_retriever"]
# )
# graph_builder.add_edge("sub_retriever", "sub_cleaner")
# graph_builder.add_conditional_edges(
#     "sub_cleaner",
#     after_sub_cleaner_continue_to_sub_relevance_graders_edge,
#     ["sub_relevance_grader"],
# )
# graph_builder.add_edge("sub_relevance_grader", "related_data_gatherer")
graph_builder.add_edge("related_data_gatherer", END)

graph = graph_builder.compile()
