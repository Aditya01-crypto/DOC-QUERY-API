from fastapi import FastAPI
import uvicorn

app=FastAPI()

def start():
    uvicorn.run("doc_query_api.main:app", host="127.0.0.1", port=8000, reload=True)

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
            "documents": "GET /documents"
        }
    }

