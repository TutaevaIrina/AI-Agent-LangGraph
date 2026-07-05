import json
import xml.etree.ElementTree as ET
from datetime import datetime

import requests
from langchain_core.tools import tool


ARXIV_API_URL = "http://export.arxiv.org/api/query"


def _clean_text(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.replace("\n", " ").split())


def _extract_year(date_text: str | None):
    if not date_text:
        return None

    try:
        return datetime.fromisoformat(date_text.replace("Z", "+00:00")).year
    except ValueError:
        return None


@tool
def search_arxiv(query: str, max_results: int = 5) -> str:
    """
    Search scientific preprints using the arXiv API.
    Returns title, abstract, year, authors, arXiv URL, PDF URL, source, type, and categories.
    """
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    response = requests.get(ARXIV_API_URL, params=params, timeout=20)
    response.raise_for_status()

    root = ET.fromstring(response.text)

    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }

    results = []

    for entry in root.findall("atom:entry", ns):
        title = _clean_text(entry.findtext("atom:title", default="", namespaces=ns))
        abstract = _clean_text(entry.findtext("atom:summary", default="", namespaces=ns))
        published = entry.findtext("atom:published", default="", namespaces=ns)
        updated = entry.findtext("atom:updated", default="", namespaces=ns)
        arxiv_url = entry.findtext("atom:id", default="", namespaces=ns)

        authors = [
            _clean_text(author.findtext("atom:name", default="", namespaces=ns))
            for author in entry.findall("atom:author", ns)
        ]

        categories = [
            category.attrib.get("term", "")
            for category in entry.findall("atom:category", ns)
            if category.attrib.get("term")
        ]

        pdf_url = ""
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("title") == "pdf":
                pdf_url = link.attrib.get("href", "")
                break

        doi = entry.findtext("arxiv:doi", default="", namespaces=ns) or None

        results.append(
            {
                "title": title,
                "year": _extract_year(published),
                "doi": doi,
                "source": "arXiv",
                "type": "preprint",
                "cited_by_count": None,
                "authors": authors,
                "categories": categories,
                "abstract": abstract[:1800],
                "url": arxiv_url,
                "pdf_url": pdf_url,
                "published": published,
                "updated": updated,
            }
        )

    return json.dumps(results, ensure_ascii=False, indent=2)