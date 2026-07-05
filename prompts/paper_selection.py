PAPER_SELECTION_PROMPT = """
You are a paper selection agent.

Decide whether this ranked paper should be used in the final answer.

Inclusion criteria:
- clearly relevant to the user question
- scholarly context
- sufficient metadata or abstract to support its use
- high or medium relevance score

Exclusion criteria:
- wrong topic
- too vague
- missing meaningful metadata and low score
- not useful for answering the user question

User question:
{query}

Paper:
Title: {title}
Year: {year}
Source: {source}
Abstract: {abstract}
Final score: {final_score}
Ranking reason: {ranking_reason}
"""
