from config import llm
from graph.state import AgentState
from models.schemas import PaperDecision
from prompts.paper_selection import PAPER_SELECTION_PROMPT


def paper_selection_agent(state: AgentState) -> AgentState:
    structured_llm = llm.with_structured_output(PaperDecision)
    selected = []

    for paper in state["ranked_papers"]:
        if paper.get("final_score", 0) < 50:
            continue

        result = structured_llm.invoke(
            PAPER_SELECTION_PROMPT.format(
                query=state["query"],
                title=paper.get("title", ""),
                year=paper.get("year", ""),
                source=paper.get("source", ""),
                abstract=paper.get("abstract", ""),
                final_score=paper.get("final_score", 0),
                ranking_reason=paper.get("ranking_reason", ""),
            )
        )

        if result.include:
            paper["selection_reason"] = result.reason
            selected.append(paper)

        if len(selected) >= 8:
            break

    state["selected_papers"] = selected
    return state
