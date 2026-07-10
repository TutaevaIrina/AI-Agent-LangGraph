import json
from typing import Any

from config import llm
from graph.state import AgentState
from models.schemas import RankedPapers
from prompts.ranking import RANKING_PROMPT


BATCH_SIZE = 5


def calculate_final_score(
    relevance_score: int,
    quality_score: int,
    recency_score: int,
) -> int:
    """
    Calculate the final score deterministically.

    Weighting:
    - Relevance: 60%
    - Quality: 25%
    - Recency: 15%
    """
    return round(
        relevance_score * 0.60
        + quality_score * 0.25
        + recency_score * 0.15
    )


def create_paper_id(index: int) -> str:
    return f"paper_{index + 1}"


def ranking_agent(state: AgentState) -> AgentState:
    structured_llm = llm.with_structured_output(RankedPapers)

    papers = state["papers"]

    # Assign stable IDs before sending papers to the LLM.
    for index, paper in enumerate(papers):
        paper["paper_id"] = create_paper_id(index)

    ranking_by_title: dict[str, dict[str, Any]] = {}

    for start in range(0, len(papers), BATCH_SIZE):
        batch = papers[start:start + BATCH_SIZE]

        papers_text = json.dumps(
            batch,
            ensure_ascii=False,
            indent=2,
        )

        result = structured_llm.invoke(
            RANKING_PROMPT.format(
                query=state["query"],
                paper_count=len(batch),
                papers=papers_text,
            )
        )

        print("========== RAW LLM OUTPUT ==========")
        print(result)
        print("====================================")

        for score in result.papers:
            normalized_title = score.title.strip().lower()

            ranking_by_title[normalized_title] = {
                "relevance_score": score.relevance_score,
                "quality_score": score.quality_score,
                "recency_score": score.recency_score,
                "reason": score.reason,
            }

    ranked_papers = []

    for paper in papers:
        title = (paper.get("title") or "").strip()
        normalized_title = title.lower()

        score = ranking_by_title.get(normalized_title)

        if score is None:
            paper["relevance_score"] = 0
            paper["quality_score"] = 0
            paper["recency_score"] = 0
            paper["final_score"] = 0
            paper["ranking_reason"] = (
                "No ranking returned by the model."
            )
        else:
            relevance = score["relevance_score"]
            quality = score["quality_score"]
            recency = score["recency_score"]

            paper["relevance_score"] = relevance
            paper["quality_score"] = quality
            paper["recency_score"] = recency

            # Python calculates the exact weighted score.
            paper["final_score"] = calculate_final_score(
                relevance_score=relevance,
                quality_score=quality,
                recency_score=recency,
            )

            paper["ranking_reason"] = score["reason"]

        ranked_papers.append(paper)

    ranked_papers.sort(
        key=lambda item: item.get("final_score", 0),
        reverse=True,
    )

    state["ranked_papers"] = ranked_papers
    return state