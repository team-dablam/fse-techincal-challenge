from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes.routes import router

app = FastAPI(
    title="Article Reputation Analyzer",
    description="FSE Technical Challenge — reputation analysis API",
    version="0.1.0",
)


@app.exception_handler(NotImplementedError)
async def not_implemented_handler(request: Request, exc: NotImplementedError) -> JSONResponse:
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "article-reputation-analyzer"}


app.include_router(router)
