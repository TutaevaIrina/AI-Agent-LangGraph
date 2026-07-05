from typing import List, Dict, Any


def deduplicate_papers(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result = []

    for paper in papers:
        title = paper.get("title") or ""
        doi = paper.get("doi") or ""
        key = doi.lower().strip() if doi else title.lower().strip()

        if not key:
            continue

        if key not in seen:
            seen.add(key)
            result.append(paper)

    return result
