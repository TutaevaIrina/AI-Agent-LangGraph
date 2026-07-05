SEARCH_QUERY_PROMPT = """
Create 3 to 5 academic search queries for the user question.

Use Boolean search logic suitable for scientific databases.
Do not restrict the search to any predefined topic.
Prefer English academic keywords, even if the user question is in another language.
Include synonyms and related scholarly terms.

Research domain: {research_domain}
User question: {query}

Examples:
("large language models" OR "generative AI") AND ("scientific writing" OR "research support")
("digital transformation" OR "AI adoption") AND ("higher education" OR university)
("fake reviews" OR "review manipulation") AND ("impact" OR consequence OR effect)
"""
