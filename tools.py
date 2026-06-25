import arxiv
import requests


def search_arxiv(query: str, max_results: int = 5):
    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    for result in client.results(search):
        papers.append({
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary,
            "published": str(result.published.date()),
            "url": result.entry_id,
            "doi": result.doi
        })

    return papers


def check_crossref(title: str):
    """
    Checks whether a paper title appears in Crossref.
    If yes, the paper may have a DOI and publication metadata.
    """
    try:
        response = requests.get(
            "https://api.crossref.org/works",
            params={"query.title": title, "rows": 1},
            timeout=10
        )

        if response.status_code != 200:
            return None

        items = response.json().get("message", {}).get("items", [])

        if not items:
            return None

        item = items[0]

        return {
            "doi": item.get("DOI"),
            "publisher": item.get("publisher"),
            "container_title": item.get("container-title", ["Unknown"])[0],
            "type": item.get("type"),
            "published_print": item.get("published-print"),
            "published_online": item.get("published-online")
        }

    except Exception:
        return None


def evaluate_source(paper: dict) -> dict:
    url = paper.get("url", "").lower()
    title = paper.get("title", "")
    authors = paper.get("authors", [])
    summary = paper.get("summary", "")
    published = paper.get("published", "")
    doi = paper.get("doi")

    score = 0
    notes = []
    source_type = "unknown"
    peer_review_status = "unknown"

    crossref_data = check_crossref(title)

    if "arxiv.org" in url:
        score += 35
        source_type = "arXiv preprint"
        peer_review_status = "not peer-reviewed by arXiv"
        notes.append("The source is from arXiv, which is a scientific preprint repository.")
        notes.append("arXiv papers are moderated but not automatically peer-reviewed.")

    if doi:
        score += 20
        notes.append("The paper has a DOI in arXiv metadata.")

    elif crossref_data and crossref_data.get("doi"):
        doi = crossref_data.get("doi")
        score += 25
        notes.append("A DOI was found via Crossref, which indicates formal publication metadata.")

    else:
        notes.append("No DOI was found.")

    if crossref_data:
        score += 20
        peer_review_status = "possibly peer-reviewed"
        source_type = f"published academic work / {source_type}"
        notes.append("Crossref metadata was found.")
        notes.append(f"Publisher: {crossref_data.get('publisher', 'unknown')}")
        notes.append(f"Venue: {crossref_data.get('container_title', 'unknown')}")
    else:
        notes.append("No Crossref metadata was found.")

    if title:
        score += 5

    if authors:
        score += 10
    else:
        notes.append("Missing author information.")

    if summary:
        score += 10
    else:
        notes.append("Missing abstract or summary.")

    if published:
        score += 5
    else:
        notes.append("Missing publication date.")

    if "medium.com" in url or "blog" in url or "wordpress" in url:
        score -= 40
        source_type = "non-peer-reviewed web article"
        peer_review_status = "not peer-reviewed"
        notes.append("The source appears to be a blog or general website.")

    score = max(0, min(score, 100))

    if score >= 80:
        credibility = "high"
    elif score >= 55:
        credibility = "medium"
    else:
        credibility = "low"

    return {
        **paper,
        "doi": doi,
        "source_type": source_type,
        "peer_review_status": peer_review_status,
        "credibility_score": score,
        "credibility": credibility,
        "publisher": crossref_data.get("publisher") if crossref_data else None,
        "venue": crossref_data.get("container_title") if crossref_data else None,
        "evaluation_notes": notes
    }