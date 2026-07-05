import json

from graph.state import AgentState
from tools.openalex_tool import search_openalex
from tools.crossref_tool import search_crossref
from tools.arxiv_tool import search_arxiv
from tools.utils import deduplicate_papers

SEARCH_TOOLS = [
    search_openalex,
    search_crossref,
    search_arxiv,
]


def search_agent(state: AgentState) -> AgentState:
    all_papers = []

    for query in state["search_queries"]:
        for tool_fn in SEARCH_TOOLS:
            try:
                raw = tool_fn.invoke({
                    "query": query,
                    "max_results": 5,
                })
                papers = json.loads(raw)

                for paper in papers:
                    paper["search_query"] = query
                    paper["tool"] = tool_fn.name
                    all_papers.append(paper)

            except Exception as exc:
                all_papers.append({
                    "title": "TOOL_ERROR",
                    "error": str(exc),
                    "search_query": query,
                    "tool": tool_fn.name,
                })

    valid_papers = [
        paper for paper in all_papers
        if paper.get("title") and paper.get("title") != "TOOL_ERROR"
    ]

    state["papers"] = deduplicate_papers(valid_papers)[:25]
    return state
