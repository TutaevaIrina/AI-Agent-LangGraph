from config import llm
from graph.state import AgentState
from models.schemas import SearchQueries
from prompts.search_query import SEARCH_QUERY_PROMPT


def build_search_queries_agent(state: AgentState) -> AgentState:
    structured_llm = llm.with_structured_output(SearchQueries)

    result = structured_llm.invoke(
        SEARCH_QUERY_PROMPT.format(
            research_domain=state["research_domain"],
            query=state["query"],
        )
    )

    state["search_queries"] = result.queries
    return state
