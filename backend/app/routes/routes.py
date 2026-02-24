import json

from fastapi import APIRouter, HTTPException
from openai import OpenAI

from app.config.config import settings
from app.models.responses import (
    AnalysisResponse,
    Claim,
    Contradiction,
    Entity,
    ReputationSignal,
    ReputationSignals,
    Sentiment,
)
from app.services.data_service import get_article_by_id, load_articles

router = APIRouter()

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an expert reputation analyst with deep experience in media analysis,
public relations risk, and corporate communications. Your role is to analyse news articles and
produce structured, evidence-based reputation reports.

Rules:
- Be precise and impartial. Do not editorialise beyond what the article supports.
- All evidence quotes must be verbatim or near-verbatim from the article content.
- All numeric scores must reflect the actual tone and weight of the article.
- Return ONLY a valid JSON object. No markdown fences, no commentary, no preamble."""


def build_user_prompt(article: dict) -> str:
    subject = article["subject_name"]
    return f"""Analyse this news article about {subject} (subject type: {article["subject_type"]}).

ARTICLE METADATA
Title:     {article["title"]}
Source:    {article["source"]}
Author:    {article.get("author", "Unknown")}
Published: {article.get("published_date", "Unknown")}

ARTICLE CONTENT
{article["content"]}

Return a JSON object with the following structure. Every REQUIRED field must be present.

REQUIRED
{{
  "sentiment": {{
    "label": "positive" | "negative" | "neutral" | "mixed",
    "score": <float -1.0 to 1.0>,
    "confidence": <float 0.0 to 1.0>
  }},
  "entities": [
    {{
      "name": "<entity name>",
      "type": "person" | "company" | "organisation" | "location" | "other",
      "relationship": "<relationship to {subject}, e.g. regulator, competitor, employee>",
      "sentiment_context": "<how this entity is framed in the article>"
    }}
  ],
  "themes": ["<theme1>", "<theme2>", "<theme3>"],
  "reputation_signals": {{
    "positive": [{{"signal": "<description>", "evidence": "<verbatim quote>"}}],
    "negative": [{{"signal": "<description>", "evidence": "<verbatim quote>"}}],
    "neutral":  [{{"signal": "<description>", "evidence": "<verbatim quote>"}}]
  }},
  "significance_score": <float 0.0 to 1.0>,
  "reasoning": "<2-4 sentence plain-language explanation of the overall reputation picture>"
}}

OPTIONAL
{{
  "sentiment_breakdown": {{
    "governance": <float -1.0 to 1.0>,
    "business_performance": <float -1.0 to 1.0>,
    "public_perception": <float -1.0 to 1.0>,
    "ethical_conduct": <float -1.0 to 1.0>,
    "leadership": <float -1.0 to 1.0>
  }},
  "mention_analysis": {{
    "mention_count": <integer>,
    "first_mention_context": "<how the subject is introduced>",
    "dominant_framing": "<predominant portrayal throughout>"
  }},
  "contradictions": [
    {{
      "type": "<framing | factual | perspective | tone>",
      "description": "<plain-language summary of the tension>",
      "evidence": {{
        "positive_frame": "<quote supporting positive reading>",
        "negative_frame": "<quote supporting negative reading>"
      }}
    }}
  ],
  "claims": [
    {{
      "claim": "<specific factual claim about {subject}>",
      "evidence": "<verbatim quote>",
      "claim_type": "factual" | "opinion" | "projection",
      "significance": "low" | "medium" | "high"
    }}
  ],
  "source_credibility": {{
    "reliability": "high" | "medium" | "low",
    "bias_assessment": "<detectable framing bias>",
    "notes": "<relevant context about this source>"
  }}
}}

Guidelines:
- Include 3-5 themes.
- Only include signals in buckets the article genuinely supports.
- Entities must be actually named in the article, not inferred.
- significance_score: breaking scandal = 0.9+, routine profile = 0.3.
"""


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_response(data: dict) -> AnalysisResponse:
    sentiment = Sentiment(**data["sentiment"])

    entities = [Entity(**e) for e in data.get("entities", [])]

    rs = data.get("reputation_signals", {})
    reputation_signals = ReputationSignals(
        positive=[ReputationSignal(**s) for s in rs.get("positive", [])],
        negative=[ReputationSignal(**s) for s in rs.get("negative", [])],
        neutral=[ReputationSignal(**s) for s in rs.get("neutral", [])],
    )

    return AnalysisResponse(
        sentiment=sentiment,
        entities=entities,
        themes=data["themes"],
        reputation_signals=reputation_signals,
        significance_score=data["significance_score"],
        reasoning=data["reasoning"],
        # optional
        sentiment_breakdown=data.get("sentiment_breakdown"),
        mention_analysis=data.get("mention_analysis"),
        claims=[Claim(**c) for c in data["claims"]] if data.get("claims") else None,
        contradictions=[Contradiction(**c) for c in data["contradictions"]] if data.get("contradictions") else None,
        source_credibility=data.get("source_credibility"),
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/articles")
async def list_articles() -> list[dict]:
    """Return all articles for the dropdown."""
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
    # 1. get the article
    article = get_article_by_id(article_id)

    # 2. check api key
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set in .env")

    # 3. create client
    client = OpenAI(api_key=settings.openai_api_key)

    # 4. call the llm
    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(article)},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {e}")

    # 5. parse json
    try:
        data = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON from LLM: {e}")

    # 6. build and return pydantic response
    try:
        return parse_response(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Response parsing failed: {e}")