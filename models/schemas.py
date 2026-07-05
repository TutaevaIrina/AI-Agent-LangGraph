from typing import List
from pydantic import BaseModel, Field


class ScientificRelevanceResult(BaseModel):
    is_scientific: bool = Field(
        description="True if the user asks an explicit scientific, academic, research, literature, theory, method, empirical, or scholarly question."
    )
    reason: str
    research_domain: str = Field(
        description="Short research domain, e.g. Information Systems, Psychology, Medicine, Computer Science, Education, Management, or Other."
    )


class SearchQueries(BaseModel):
    queries: List[str] = Field(description="3 to 5 academic search queries")


class PaperScore(BaseModel):
    title: str
    relevance_score: int = Field(description="Integer from 0 to 100")
    quality_score: int = Field(description="Integer from 0 to 100")
    recency_score: int = Field(description="Integer from 0 to 100")
    final_score: int = Field(description="Weighted final score from 0 to 100")
    reason: str


class RankedPapers(BaseModel):
    papers: List[PaperScore]


class PaperDecision(BaseModel):
    title: str
    include: bool
    reason: str


class EvaluationResult(BaseModel):
    passed: bool
    feedback: str
