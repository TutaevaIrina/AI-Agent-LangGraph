import json

from config import llm
from graph.state import AgentState
from models.schemas import RankedPapers
from prompts.ranking import RANKING_PROMPT


def ranking_agent(state: AgentState) -> AgentState:
    structured_llm = llm.with_structured_output(RankedPapers)

    papers_text = json.dumps(
        state["papers"],
        ensure_ascii=False,
        indent=2,
    )

    result = structured_llm.invoke(
        RANKING_PROMPT.format(
            query=state["query"],
            papers=papers_text,
        )
    )

    score_by_title = {
        item.title.lower().strip(): item.model_dump()
        for item in result.papers
    }

    ranked = []
    for paper in state["papers"]:
        key = (paper.get("title") or "").lower().strip()
        score = score_by_title.get(key)

        if not score:
            paper["relevance_score"] = 0
            paper["quality_score"] = 0
            paper["recency_score"] = 0
            paper["final_score"] = 0
            paper["ranking_reason"] = "No ranking returned by the model."
        else:
            paper["relevance_score"] = score["relevance_score"]
            paper["quality_score"] = score["quality_score"]
            paper["recency_score"] = score["recency_score"]
            paper["final_score"] = score["final_score"]
            paper["ranking_reason"] = score["reason"]

        ranked.append(paper)

    ranked.sort(key=lambda item: item.get("final_score", 0), reverse=True)

    state["ranked_papers"] = ranked
    return state
