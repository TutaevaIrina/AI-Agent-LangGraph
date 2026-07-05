from graph.state import AgentState


def route_after_relevance(state: AgentState) -> str:
    if state["is_scientific"]:
        return "build_search_queries"
    return "end"


def route_after_evaluation(state: AgentState) -> str:
    if state["evaluation_passed"]:
        return "end"
    return "revision"
