from fastapi import APIRouter
from openai import OpenAI

from app.models.responses import AnalysisResponse
from app.services.data_service import get_article_by_id, load_articles
from app.config.config import settings

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

    client = OpenAI(api_key=settings.openai_api_key)

    try:
        response = client.responses.parse(
            model=settings.openai_model,
            temperature=0.2,
            input=[
                {
                    "role": "system",
                    "content": "You are an expert analyst. Return only JSON matching the provided schema exactly."
                },
                {
                    "role": "user",
                    "content": f"Analyze the following article and return an object matching the analysis_response schema exactly. Article: {article}"
                }
            ],
            text_format=AnalysisResponse
        )
        return response.output_parsed
    except Exception as e:
        print(f"An error occurred: {e}")

    
