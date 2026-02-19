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
    # Return an AnalysisResponse (defined in app/models/responses.py).
    #
    # sentiment          — label ("positive"|"negative"|"neutral"|"mixed"), score (-1 to 1), confidence (0 to 1)
    # entities           — list of Entity: name, type, relationship to subject, sentiment_context
    # themes             — 3–5 high-level themes present in the article
    # reputation_signals — ReputationSignals with positive/negative/neutral lists of ReputationSignal:
    #                        each signal has: signal (str), evidence (direct quote or paraphrase)
    # significance_score — 0 to 1, how impactful this article is for the subject's reputation
    # reasoning          — plain-language explanation of the overall analysis
    #
    # === OPTIONAL EXTENSIONS ===
    # Use the optional fields on AnalysisResponse if you have time:
    #
    # sentiment_breakdown  — dict[str, float], e.g. {"governance": -0.6, "business_performance": 0.8}
    # mention_analysis     — dict, mention count, first mention context, patterns throughout article
    # contradictions       — list of Contradiction: type, description, evidence dict
    #                          e.g. {"positive_frame": "...", "negative_frame": "..."}
    # claims               — list of Claim: claim, evidence (quote), claim_type, significance
    # source_credibility   — dict, reliability and bias assessment of the publication

    raise NotImplementedError  # remove this line when you implement the function
