from config import llm
from graph.state import AgentState
from models.schemas import ScientificRelevanceResult
from prompts.relevance import RELEVANCE_PROMPT


def relevance_agent(state: AgentState) -> AgentState:
    structured_llm = llm.with_structured_output(ScientificRelevanceResult)

    result = structured_llm.invoke(
        RELEVANCE_PROMPT.format(query=state["query"])
    )

    state["is_scientific"] = result.is_scientific
    state["relevance_reason"] = result.reason
    state["research_domain"] = result.research_domain

    return state
