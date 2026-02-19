from typing import Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Core models — required
# ---------------------------------------------------------------------------


class Sentiment(BaseModel):
    label: Literal["positive", "negative", "neutral", "mixed"]
    score: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Sentiment score from -1 (most negative) to 1 (most positive)",
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence in the sentiment label, 0 to 1"
    )


class Entity(BaseModel):
    name: str
    type: Literal["person", "company", "organisation", "location", "other"]
    relationship: str = Field(
        ...,
        description="Relationship to the article subject, e.g. 'competitor', 'regulator', 'employee'",
    )
    sentiment_context: str = Field(..., description="How this entity is framed in the article")


class ReputationSignal(BaseModel):
    signal: str = Field(..., description="The reputation signal, e.g. 'rigorous research approach'")
    evidence: str = Field(
        ..., description="Direct quote or paraphrase from the article that supports this signal"
    )


class ReputationSignals(BaseModel):
    positive: list[ReputationSignal] = Field(default_factory=list)
    negative: list[ReputationSignal] = Field(default_factory=list)
    neutral: list[ReputationSignal] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Optional extension models
# ---------------------------------------------------------------------------


class Contradiction(BaseModel):
    type: str = Field(
        ..., description="Category of contradiction, e.g. 'framing', 'factual', 'perspective'"
    )
    description: str = Field(..., description="Plain-language summary of the contradiction")
    evidence: dict = Field(
        ...,
        description="Two sides of the contradiction, e.g. {'positive_frame': '...', 'negative_frame': '...'}",
    )


class Claim(BaseModel):
    claim: str = Field(..., description="The specific factual claim made in the article")
    evidence: str = Field(
        ..., description="Direct quote or passage from the article supporting this claim"
    )
    claim_type: Literal["factual", "opinion", "projection"] = Field(default="factual")
    significance: Literal["low", "medium", "high"] = Field(default="medium")


# ---------------------------------------------------------------------------
# Top-level response
# ---------------------------------------------------------------------------


class AnalysisResponse(BaseModel):
    # --- Required ---
    sentiment: Sentiment
    entities: list[Entity] = Field(..., description="Key entities mentioned in the article")
    themes: list[str] = Field(
        ..., min_length=1, description="3–5 high-level themes present in the article"
    )
    reputation_signals: ReputationSignals
    significance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How significant this article is for the subject's reputation, 0 to 1",
    )
    reasoning: str = Field(..., description="Brief explanation of the overall analysis")

    # --- Optional extensions ---
    sentiment_breakdown: dict[str, float] | None = Field(
        default=None,
        description="Multi-dimensional sentiment scores, e.g. {'business_performance': 0.8, 'governance': -0.6}",
    )
    mention_analysis: dict | None = Field(
        default=None,
        description="Subject mention count, first mention context, mention patterns throughout the article",
    )
    contradictions: list[Contradiction] | None = Field(
        default=None,
        description="Competing perspectives or framing inconsistencies detected in the article",
    )
    claims: list[Claim] | None = Field(
        default=None,
        description="Specific factual claims made about the subject, with evidence and significance",
    )
    source_credibility: dict | None = Field(
        default=None,
        description="Assessment of the publication's credibility and potential bias",
    )
