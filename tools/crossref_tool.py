import json
import re
import requests
from langchain_core.tools import tool


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "")


def extract_year(item: dict):
    year_parts = (
        item.get("published-print")
        or item.get("published-online")
        or item.get("published")
        or item.get("created")
    )
    if year_parts and "date-parts" in year_parts:
        return year_parts["date-parts"][0][0]
    return None


@tool
def search_crossref(query: str, max_results: int = 5) -> str:
    """
    Search publications using Crossref.
    Useful for DOI, title, journal, and publication year.
    """
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": max_results,
        "sort": "relevance",
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("message", {}).get("items", []):
        titles = item.get("title") or [""]
        containers = item.get("container-title") or [""]

        results.append({
            "title": titles[0],
            "year": extract_year(item),
            "doi": item.get("DOI"),
            "source": containers[0] if containers else "",
            "type": item.get("type"),
            "cited_by_count": item.get("is-referenced-by-count"),
            "abstract": strip_html(item.get("abstract", ""))[:1800],
            "url": item.get("URL"),
        })

    return json.dumps(results, ensure_ascii=False, indent=2)
