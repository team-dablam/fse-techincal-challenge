from fastapi import APIRouter

from app.models.responses import (
    AnalysisResponse,
    Sentiment,
    Entity,
    ReputationSignals,
    ReputationSignal,
)
from app.services.data_service import get_article_by_id, load_articles


router = APIRouter()


@router.get("/articles")
async def list_articles() -> list[dict]:
    """Return all subjects for the dropdown — id, subject_name, subject_type only."""
    return [
        {
            "id": a["id"],
            "subject_name": a["subject_name"],
            "subject_type": a["subject_type"],
        }
        for a in load_articles()
    ]


@router.get("/articles/{article_id}")
async def get_article(article_id: str) -> dict:
    """Return a single article by id."""
    return get_article_by_id(article_id)


@router.post("/analyse/{article_id}", response_model=AnalysisResponse)
async def analyse_article(article_id: str) -> AnalysisResponse:
    article = get_article_by_id(article_id)

    subject_name = article.get("subject_name", "Subject")
    subject_type = article.get("subject_type", "other")
    title = article.get("title", "")
    content = article.get("content", "")

    themes = ["public perception", "business performance", "media coverage"]

    neutral_signal = ReputationSignal(
        signal="General coverage / informational tone",
        evidence=(title or content[:160] or "No evidence available").strip(),
    )

    return AnalysisResponse(
        sentiment=Sentiment(label="neutral", score=0.0, confidence=0.55),
        entities=[
            Entity(
                name=subject_name,
                type=subject_type if subject_type in {"person", "company"} else "other",
                relationship="subject",
                sentiment_context="The article primarily describes the subject without strong sentiment.",
            )
        ],
        themes=themes,
        reputation_signals=ReputationSignals(
            positive=[],
            negative=[],
            neutral=[neutral_signal],
        ),
        significance_score=0.3,
        reasoning="Placeholder analysis so the UI can render. Next step will replace this with an LLM-powered analysis.",
    )

