from fastapi import FastAPI,Depends,HTTPException
import uvicorn
from contextlib import asynccontextmanager
from doc_query_api.database import Base,engine
from sqlalchemy import text
from pathlib import Path
from doc_query_api.routers.documents import router
import os
from doc_query_api.limiter import limiter

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    yield 
    await engine.dispose()

app=FastAPI(lifespan=lifespan)
app.include_router(router)
app.state.limiter=limiter
def start():
    host=os.getenv("HOST","0.0.0.0")
    port=int(os.getenv("PORT",8000))
    uvicorn.run("doc_query_api.main:app", host=host, port=port, reload=False)

@app.get("/")
def index():
    return {
        "name": "DOC-QUERY-API",
        "version": "1.0.0",
        "description": "Upload documents, generate semantic embeddings, and retrieve the most relevant content using vector similarity search.",
        "phase": "Phase 2 — AI-Ready Backend",
        "stack": ["FastAPI", "PostgreSQL", "pgvector", "sentence-transformers", "Docker"],
        "endpoints": {
            "docs": "/docs",
            "upload": "POST /documents/upload",
            "embed": "POST /documents/{id}/embed",
            "search": "POST /documents/search",
            "documents": "GET /documents",
            "delete": "DELETE /documents"
        }
    }


