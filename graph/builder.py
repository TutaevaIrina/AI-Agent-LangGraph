from langgraph.graph import StateGraph, END

from graph.state import AgentState
from graph.router import route_after_relevance, route_after_evaluation

from agents.relevance_agent import relevance_agent
from agents.search_query_agent import build_search_queries_agent
from agents.search_agent import search_agent
from agents.ranking_agent import ranking_agent
from agents.paper_selection_agent import paper_selection_agent
from agents.answer_generation_agent import answer_generation_agent
from agents.answer_evaluation_agent import answer_evaluation_agent
from agents.revision_agent import revision_agent


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("relevance", relevance_agent)
    graph.add_node("build_search_queries", build_search_queries_agent)
    graph.add_node("search", search_agent)
    graph.add_node("ranking", ranking_agent)
    graph.add_node("paper_selection", paper_selection_agent)
    graph.add_node("answer_generation", answer_generation_agent)
    graph.add_node("answer_evaluation", answer_evaluation_agent)
    graph.add_node("revision", revision_agent)

    graph.set_entry_point("relevance")

    graph.add_conditional_edges(
        "relevance",
        route_after_relevance,
        {
            "build_search_queries": "build_search_queries",
            "end": END,
        },
    )

    graph.add_edge("build_search_queries", "search")
    graph.add_edge("search", "ranking")
    graph.add_edge("ranking", "paper_selection")
    graph.add_edge("paper_selection", "answer_generation")
    graph.add_edge("answer_generation", "answer_evaluation")

    graph.add_conditional_edges(
        "answer_evaluation",
        route_after_evaluation,
        {
            "revision": "revision",
            "end": END,
        },
    )

    graph.add_edge("revision", END)

    return graph.compile()
