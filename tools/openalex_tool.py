import json
import requests
from langchain_core.tools import tool


def reconstruct_abstract(inverted_index: dict | None) -> str:
    if not inverted_index:
        return ""

    words = []
    for word, positions in inverted_index.items():
        for pos in positions:
            words.append((pos, word))

    return " ".join(word for _, word in sorted(words))


@tool
def search_openalex(query: str, max_results: int = 5) -> str:
    """
    Search scientific publications using OpenAlex.
    Returns title, abstract, year, DOI, source, citation count, and URL.
    """
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per-page": max_results,
        "sort": "relevance_score:desc",
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("results", []):
        primary_location = item.get("primary_location") or {}
        source_obj = primary_location.get("source") or {}

        results.append({
            "title": item.get("title"),
            "year": item.get("publication_year"),
            "doi": item.get("doi"),
            "source": source_obj.get("display_name"),
            "type": item.get("type"),
            "cited_by_count": item.get("cited_by_count"),
            "abstract": reconstruct_abstract(item.get("abstract_inverted_index"))[:1800],
            "url": item.get("id"),
        })

    return json.dumps(results, ensure_ascii=False, indent=2)
