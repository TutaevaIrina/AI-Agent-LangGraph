import json
from langchain_core.messages import HumanMessage, SystemMessage

from config import llm
from graph.state import AgentState
from prompts.answer_generation import ANSWER_GENERATION_PROMPT


def answer_generation_agent(state: AgentState) -> AgentState:
    papers_text = json.dumps(
        state["selected_papers"],
        ensure_ascii=False,
        indent=2,
    )

    prompt = ANSWER_GENERATION_PROMPT.format(
        query=state["query"],
        papers=papers_text,
    )

    result = llm.invoke([
        SystemMessage(content="You write precise scientific answers in English."),
        HumanMessage(content=prompt),
    ])

    state["answer"] = result.content
    return state
