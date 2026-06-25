import json
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import search_arxiv, evaluate_source

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)


class ResearchState(TypedDict):
    question: str
    intent: str
    plan: str
    search_query: str
    papers: List[dict]
    filtered_papers: List[dict]
    report: str


def planner_node(state: ResearchState):
    question = state["question"].strip()

    prompt = f"""
You are the planner of an academic research assistant.

Decide whether the user's question can be answered meaningfully by searching scientific literature. Be tolerant of spelling or grammar mistakes.

Classify the question into one of these intents:

1. "research"
Use this if the user asks about scientific knowledge, academic topics, methods, frameworks, models, systems, technologies, research trends, or literature reviews.

2. "general_knowledge"
Use this if the user asks for an explanation of a concept, technology, business system, software system, or academic topic that can still be supported by scientific literature.
Examples:
- What is ERP and how does it work?
- What is machine learning?
- How does blockchain work?
- What is supply chain management?

3. "out_of_scope"
Use this if the question is casual, personal, lifestyle-related, entertainment-related, weather-related, shopping-related, or cannot reasonably be answered using academic literature.

Return ONLY valid JSON with this structure:

{{
  "intent": "research",
  "search_query": "optimized academic search query",
  "reason": "short explanation"
}}

User question:
{question}
"""

    try:
        response = llm.invoke(prompt)
        content = response.content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        decision = json.loads(content)

        intent = decision.get("intent", "out_of_scope")

        if intent not in ["research", "general_knowledge", "out_of_scope"]:
            intent = "out_of_scope"

        return {
            "intent": intent,
            "search_query": decision.get("search_query", question),
            "plan": decision.get("reason", "")
        }

    except Exception as e:
      return {
          "intent": "research",
          "search_query": question,
          "plan": f"Planner fallback: treating the question as research because classification failed. Error: {e}"
      }


def out_of_scope_node(state: ResearchState):
    prompt = f"""
You are an academic research assistant.

The following user question is outside the scope of academic literature research:

{state["question"]}

Respond politely.
Explain briefly why this question is outside the system scope.
Suggest 3 example questions the system can answer.
"""

    try:
        response = llm.invoke(prompt)
        return {"report": response.content}
    except Exception:
        return {
            "report": f"""
# Out of Scope

Your question was:

{state["question"]}

This agent is designed for academic literature research.

Example questions:
- What is ERP and how does it work?
- How can AI agents support literature review in academic research?
- What are current methods for bias detection in large language models?
"""
        }


def search_node(state: ResearchState):
    papers = search_arxiv(state["search_query"], max_results=7)
    return {"papers": papers}


def source_evaluation_node(state: ResearchState):
    evaluated_papers = [
        evaluate_source(paper)
        for paper in state["papers"]
    ]

    return {"papers": evaluated_papers}


def ranking_node(state: ResearchState):
    question_words = set(state["search_query"].lower().split())
    ranked_papers = []

    for paper in state["papers"]:
        title = paper.get("title", "").lower()
        summary = paper.get("summary", "").lower()

        relevance_score = 0

        for word in question_words:
            if word in title:
                relevance_score += 3
            if word in summary:
                relevance_score += 1

        credibility_score = paper.get("credibility_score", 0)
        final_score = relevance_score + credibility_score / 10

        paper["relevance_score"] = relevance_score
        paper["final_score"] = final_score

        ranked_papers.append(paper)

    ranked_papers = sorted(
        ranked_papers,
        key=lambda p: p.get("final_score", 0),
        reverse=True
    )

    return {"filtered_papers": ranked_papers[:3]}


def fallback_report_node(state: ResearchState):
    report = f"""
# Research Report

## Question
{state["question"]}

## Intent
{state["intent"]}

## Search Plan
{state["plan"]}

## Search Query
{state["search_query"]}

## Selected Sources
"""

    for i, paper in enumerate(state["filtered_papers"], start=1):
        report += f"""
### Paper {i}: {paper.get("title", "Unknown title")}

**Authors:** {", ".join(paper.get("authors", []))}  
**Published:** {paper.get("published", "unknown")}  
**URL:** {paper.get("url", "unknown")}  
**DOI:** {paper.get("doi", "No DOI found")}  
**Source type:** {paper.get("source_type", "unknown")}  
**Peer-review status:** {paper.get("peer_review_status", "unknown")}  
**Publisher:** {paper.get("publisher", "unknown")}  
**Venue:** {paper.get("venue", "unknown")}  
**Credibility:** {paper.get("credibility", "unknown")} ({paper.get("credibility_score", 0)}/100)  
**Relevance score:** {paper.get("relevance_score", 0)}  
**Final ranking score:** {paper.get("final_score", 0)}

**Evaluation notes:**  
{", ".join(paper.get("evaluation_notes", []))}

**Abstract:**  
{paper.get("summary", "No summary available.")}

---
"""

    report += """
## Note
This report was generated with the fallback report generator because the LLM report generator was unavailable.
"""

    return {"report": report}


def report_node(state: ResearchState):
    papers_text = ""

    for i, paper in enumerate(state["filtered_papers"], start=1):
        papers_text += f"""
Paper {i}
Title: {paper.get("title", "Unknown title")}
Authors: {", ".join(paper.get("authors", []))}
Published: {paper.get("published", "unknown")}
URL: {paper.get("url", "unknown")}
DOI: {paper.get("doi", "No DOI found")}
Source type: {paper.get("source_type", "unknown")}
Peer-review status: {paper.get("peer_review_status", "unknown")}
Publisher: {paper.get("publisher", "unknown")}
Venue: {paper.get("venue", "unknown")}
Credibility: {paper.get("credibility", "unknown")} ({paper.get("credibility_score", 0)}/100)
Relevance score: {paper.get("relevance_score", 0)}
Final ranking score: {paper.get("final_score", 0)}
Evaluation notes: {", ".join(paper.get("evaluation_notes", []))}

Abstract:
{paper.get("summary", "No summary available.")}

---
"""

    prompt = f"""
You are an academic research assistant.

Create a structured academic report.

Original user question:
{state["question"]}

Intent:
{state["intent"]}

Search plan:
{state["plan"]}

Search query:
{state["search_query"]}

Use only the papers listed below:

{papers_text}

The report must include exactly these sections:
1. Research question or concept
2. Short overview
3. Summary of each paper
4. Source evaluation table
5. Comparison of the papers
6. Research gaps or limitations
7. Possible future work
8. Sources with URLs and DOI if available

For the source evaluation table, include:
Title | Source type | Peer-review status | DOI | Publisher | Venue | Credibility score | Evaluation notes

Write clearly in academic English.
"""

    try:
        response = llm.invoke(prompt)
        return {"report": response.content}
    except Exception:
        return fallback_report_node(state)


def route_after_planner(state: ResearchState):
    if state["intent"] in ["research", "general_knowledge"]:
        return "search"
    return "out_of_scope"


builder = StateGraph(ResearchState)

builder.add_node("planner", planner_node)
builder.add_node("out_of_scope", out_of_scope_node)
builder.add_node("search", search_node)
builder.add_node("source_evaluation", source_evaluation_node)
builder.add_node("ranking", ranking_node)
builder.add_node("report", report_node)

builder.add_edge(START, "planner")

builder.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "search": "search",
        "out_of_scope": "out_of_scope"
    }
)

builder.add_edge("out_of_scope", END)
builder.add_edge("search", "source_evaluation")
builder.add_edge("source_evaluation", "ranking")
builder.add_edge("ranking", "report")
builder.add_edge("report", END)

graph = builder.compile()