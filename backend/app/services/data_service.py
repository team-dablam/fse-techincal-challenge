import json
from pathlib import Path

from fastapi import HTTPException

DATA_PATH = Path(__file__).parent.parent.parent / "data" / "articles.json"


def load_articles() -> list[dict]:
    with open(DATA_PATH) as f:
        return json.load(f)


def get_article_by_id(article_id: str) -> dict:
    article = next((a for a in load_articles() if a["id"] == article_id), None)
    if not article:
        raise HTTPException(status_code=404, detail=f"Article '{article_id}' not found")
    return article
