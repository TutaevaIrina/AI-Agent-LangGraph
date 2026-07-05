from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    query: str
    is_scientific: bool
    relevance_reason: str
    research_domain: str
    search_queries: List[str]
    papers: List[Dict[str, Any]]
    ranked_papers: List[Dict[str, Any]]
    selected_papers: List[Dict[str, Any]]
    answer: str
    evaluation_passed: bool
    evaluation_feedback: str
