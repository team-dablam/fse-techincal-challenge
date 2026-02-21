from fastapi import APIRouter

from app.models.responses import (
    AnalysisResponse,
    Sentiment,
    Entity,
    ReputationSignals,
    ReputationSignal,
)
from app.services.data_service import get_article_by_id, load_articles

import json
import re

from fastapi import HTTPException
from openai import OpenAI

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

    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="Missing OpenAI API key (OPENAI_API_KEY)")

    client = OpenAI(api_key=settings.openai_api_key)

    subject_name = article.get("subject_name", "")
    subject_type = article.get("subject_type", "")
    title = article.get("title", "")
    source = article.get("source", "")
    author = article.get("author", "")
    published_date = article.get("published_date", "")
    content = article.get("content", "")

    system_prompt = (
        "You are an expert reputation analyst. "
        "Return ONLY valid JSON that matches this exact schema:\n\n"
        "{\n"
        '  "sentiment": { "label": "positive|negative|neutral|mixed", "score": -1..1, "confidence": 0..1 },\n'
        '  "entities": [ { "name": string, "type": "person|company|organisation|location|other", '
        '"relationship": string, "sentiment_context": string } ],\n'
        '  "themes": [string, string, string],\n'
        '  "reputation_signals": {\n'
        '     "positive": [ { "signal": string, "evidence": string } ],\n'
        '     "negative": [ { "signal": string, "evidence": string } ],\n'
        '     "neutral":  [ { "signal": string, "evidence": string } ]\n'
        "  },\n"
        '  "significance_score": 0..1,\n'
        '  "reasoning": string,\n'
        '  "sentiment_breakdown": object|null,\n'
        '  "mention_analysis": object|null,\n'
        '  "contradictions": array|null,\n'
        '  "claims": array|null,\n'
        '  "source_credibility": object|null\n'
        "}\n\n"
        "Rules:\n"
        "- Output MUST be JSON only (no markdown, no code fences).\n"
        "- Evidence should be a short direct quote or faithful paraphrase from the article.\n"
        "- Provide 3–5 themes.\n"
    )

    user_prompt = (
        f"Subject: {subject_name} ({subject_type})\n"
        f"Title: {title}\n"
        f"Source: {source}\n"
        f"Author: {author}\n"
        f"Published: {published_date}\n\n"
        f"Article content:\n{content}\n"
    )

    def extract_json(text: str) -> dict:
        text = text.strip()
     
        if text.startswith("```"):
            text = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", text).strip()
        if not (text.startswith("{") and text.endswith("}")):
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if not m:
                raise ValueError("No JSON object found in model output")
            text = m.group(0)
        return json.loads(text)

    last_err: Exception | None = None

    for attempt in range(2):  
        try:
            resp = client.responses.create(
                model=settings.openai_model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )

            raw = (resp.output_text or "").strip()
            data = extract_json(raw)

            
            return AnalysisResponse.model_validate(data)

        except Exception as e:
            last_err = e

    raise HTTPException(status_code=502, detail=f"LLM analysis failed: {last_err}")