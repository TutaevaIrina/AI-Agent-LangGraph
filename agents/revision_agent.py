from config import llm
from graph.state import AgentState
from prompts.revision import REVISION_PROMPT


def revision_agent(state: AgentState) -> AgentState:
    result = llm.invoke(
        REVISION_PROMPT.format(
            query=state["query"],
            answer=state["answer"],
            feedback=state["evaluation_feedback"],
        )
    )

    state["answer"] = result.content
    return state
