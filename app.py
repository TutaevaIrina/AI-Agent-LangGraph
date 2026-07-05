import json
from graph.builder import build_graph
from graph.state import AgentState


def run_scientific_agent(query: str) -> dict:
    app = build_graph()

    initial_state: AgentState = {
        "query": query,
        "is_scientific": False,
        "relevance_reason": "",
        "research_domain": "",
        "search_queries": [],
        "papers": [],
        "ranked_papers": [],
        "selected_papers": [],
        "answer": "",
        "evaluation_passed": False,
        "evaluation_feedback": "",
    }

    result = app.invoke(initial_state)

    if not result["is_scientific"]:
        return {
            "status": "not_scientific",
            "reason": result["relevance_reason"],
        }

    return {
        "status": "success",
        "research_domain": result["research_domain"],
        "relevance_reason": result["relevance_reason"],
        "search_queries": result["search_queries"],
        "ranked_papers": result["ranked_papers"],
        "selected_papers": result["selected_papers"],
        "answer": result["answer"],
        "evaluation_passed": result["evaluation_passed"],
        "evaluation_feedback": result["evaluation_feedback"],
    }


if __name__ == "__main__":
    query = input("Scientific question: ").strip()
    result = run_scientific_agent(query)

    print("\n================ RESULT ================\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
