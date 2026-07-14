"""Pydantic schema definitions for structured agent outputs."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class ScientificRelevanceResult(BaseModel):
    """Structured output of the relevance agent."""

    is_scientific: bool = Field(..., description="Whether the query is scientific.")
    research_domain: str = Field(..., description="Detected research domain (e.g., Computer Science).")
    reason: str = Field(..., description="Explanation for the classification.")


class SearchQueries(BaseModel):
    """LLM output containing multiple search queries."""

    queries: List[str] = Field(..., description="List of academic search queries.")


class RankedPaperItem(BaseModel):
    """Scores assigned to a single paper."""

    title: str = Field(..., description="Title used for matching back to the paper list.")
    relevance_score: int = Field(..., ge=0, le=100)
    quality_score: int = Field(..., ge=0, le=100)
    recency_score: int = Field(..., ge=0, le=100)
    final_score: int = Field(..., ge=0, le=100)
    reason: str = Field(..., description="Short justification of the scores.")


class RankedPapers(BaseModel):
    """Container holding ranking information for all papers."""

    papers: List[RankedPaperItem]


class PaperDecision(BaseModel):
    """Structured decision on whether to include a paper."""

    include: bool
    reason: str


class EvaluationResult(BaseModel):
    """Answer evaluation outcome."""

    passed: bool = Field(..., description="Whether the answer satisfies all criteria.")
    feedback: str = Field(..., description="Review comments or improvement notes.")
