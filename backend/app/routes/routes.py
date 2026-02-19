from fastapi import APIRouter

from app.models.responses import AnalysisResponse
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

    # TODO: implement your analysis here
    #
    # `article` is a dict with:
    #   id, subject_name, subject_type, title, source, author, published_date, content
    #
    # Use settings from app/config/config.py:
    #   settings.openai_api_key
    #   settings.openai_model  (default: "gpt-4o-mini")
    #
    # === REQUIRED ===
    # Return an AnalysisResponse (defined in app/models/responses.py):
    #   - sentiment:          label, score (-1 to 1), confidence
    #   - entities:           name, type, relationship, sentiment_context
    #   - themes:             3–5 relevant themes
    #   - reputation_signals: positive / negative / neutral signal lists
    #   - significance_score: 0–1 importance rating
    #   - reasoning:          brief explanation of the overall analysis
    #
    # === OPTIONAL EXTENSIONS ===
    # Use the optional fields on AnalysisResponse if you have time:
    #   - sentiment_breakdown  (e.g. {"business_performance": 0.8, "governance": -0.6})
    #   - mention_analysis     (mention count, first mention context, patterns)
    #   - contradictions       (competing perspectives or framing inconsistencies)
    #   - claims               (specific factual claims made about the subject)
    #   - source_credibility   (reliability and bias assessment of the publication)
    #
    # Document your choices in IMPLEMENTATION.md.

    raise NotImplementedError
