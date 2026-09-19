# DOC-QUERY-API

A FastAPI-based document ingestion and semantic search API built as the **Phase 2 — AI-Ready Backend** project in an AI Engineering roadmap.

The service allows users to:

- Upload PDF and DOCX documents
- Extract and clean their text
- Store document content and metadata in PostgreSQL
- Generate semantic embeddings using `sentence-transformers`
- Store embeddings with `pgvector`
- Search documents using vector cosine similarity
- Retrieve the most relevant documents for a natural-language query
- Run the API and PostgreSQL/pgvector stack through Docker Compose

> **Project repository:** https://github.com/Aditya01-crypto/DOC-QUERY-API

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Semantic Search](#semantic-search)
- [Document Processing](#document-processing)
- [Database Design](#database-design)
- [Docker Setup](#docker-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Project](#running-the-project)
- [Example Workflow](#example-workflow)
- [Phase 2 Learning Goals](#phase-2-learning-goals)
- [What This Project Demonstrates](#what-this-project-demonstrates)
- [Current Scope](#current-scope)

---

## Overview

**DOC-QUERY-API** is an AI-ready backend service that combines a REST API with vector search.

Instead of searching documents only through exact keyword matching, the project converts both documents and user queries into numerical embeddings. PostgreSQL with `pgvector` then compares those embeddings using cosine distance to retrieve the most semantically relevant documents.

The project focuses on building the backend infrastructure that AI applications can use for document retrieval.

### Core flow

```text
                ┌─────────────────┐
                │   PDF / DOCX    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  File Validation│
                │  & Text Extract │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   PostgreSQL    │
                │  Document Data  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Sentence        │
                │ Transformer     │
                │ Embedding Model │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   pgvector      │
                │ Vector Storage  │
                └─────────────────┘


User Query
    │
    ▼
Generate Query Embedding
    │
    ▼
Cosine Similarity Search
    │
    ▼
Most Relevant Documents
```

---

## Architecture

The application is organized into separate layers:

```text
Client
  │
  ▼
FastAPI
  │
  ├── Routers
  │     └── documents.py
  │
  ├── CRUD / Database Operations
  │     └── crud.py
  │
  ├── Document Extraction
  │     └── extract.py
  │
  ├── Embedding Generation
  │     └── embeddings.py
  │
  ├── SQLAlchemy Models
  │     └── models.py
  │
  └── Database Configuration
        └── database.py
                │
                ▼
        PostgreSQL + pgvector
```

FastAPI uses dependency injection to provide asynchronous SQLAlchemy database sessions to the endpoints.

---

## How It Works

### 1. Upload a document

The `/documents/upload` endpoint accepts a PDF or DOCX file.

The API:

1. Validates the file extension.
2. Reads the file to check its size.
3. Rejects files larger than 10 MB.
4. Saves the uploaded file to `uploaded_files/`.
5. Extracts the textual content.
6. Cleans the extracted text.
7. Calculates the document word count.
8. Stores the document in PostgreSQL.

Supported formats:

```text
.pdf
.docx
```

Maximum supported upload size:

```text
10 MB
```

---

### 2. Generate an embedding

After a document has been stored, its content can be embedded using:

```http
POST /documents/{id}/embed
```

The project uses:

```text
all-MiniLM-L6-v2
```

from `sentence-transformers`.

The resulting embedding contains **384 dimensions** and is stored in the PostgreSQL `vector` column.

---

### 3. Search documents semantically

A user can send a natural-language query to:

```http
POST /documents/search
```

The query is converted into an embedding using the same embedding model.

The API then compares the query embedding with stored document embeddings using **cosine distance**.

The results are ordered by cosine distance and the requested number of documents is returned.

---

## Features

### Document Management

- Upload PDF and DOCX documents
- Retrieve all stored documents
- Retrieve a document by ID
- Delete a document
- Pagination through `limit` and `skip`

### Document Processing

- PDF text extraction using `pypdf`
- DOCX text extraction using `python-docx`
- Text cleanup
- Word-count calculation
- File-size validation
- File-type validation

### Semantic Search

- Sentence-transformer embeddings
- 384-dimensional document vectors
- Query embedding generation
- Cosine-distance similarity search
- PostgreSQL `pgvector`
- HNSW vector index

### Backend Engineering

- FastAPI
- Async SQLAlchemy
- Async PostgreSQL driver
- Pydantic response models
- Dependency injection
- Docker
- Docker Compose
- Environment-based configuration

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12+ | Application language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| PostgreSQL | Primary database |
| pgvector | Vector storage and similarity search |
| SQLAlchemy 2 | Database ORM / async database access |
| asyncpg | Async PostgreSQL driver |
| Pydantic v2 | API response validation |
| Sentence Transformers | Text embedding generation |
| `all-MiniLM-L6-v2` | Embedding model |
| pypdf | PDF text extraction |
| python-docx | DOCX text extraction |
| Docker | Application containerization |
| Docker Compose | Multi-container development environment |
| uv | Python dependency and project management |

---

## Project Structure

```text
DOC-QUERY-API/
│
├── src/
│   └── doc_query_api/
│       ├── routers/
│       │   └── documents.py
│       │
│       ├── __init__.py
│       ├── crud.py
│       ├── database.py
│       ├── embeddings.py
│       ├── extract.py
│       ├── main.py
│       ├── models.py
│       └── schemas.py
│
├── tests/
│
├── uploaded_files/
│
├── .dockerignore
├── .gitignore
├── .env
├── Dockerfile
├── docker-compose.yml
├── meta.log
├── pyproject.toml
├── uv.lock
└── README.md
```

> `.env`, `meta.log`, and other local/generated files are intended to be excluded through `.gitignore` and `.dockerignore`.

---

## API Endpoints

The API exposes interactive documentation through:

```text
GET /docs
```

### Root

```http
GET /
```

Returns project information, version, stack, and the main API endpoints.

Example response:

```json
{
  "name": "DOC-QUERY-API",
  "version": "1.0.0",
  "description": "Upload documents, generate semantic embeddings, and retrieve the most relevant content using vector similarity search.",
  "phase": "Phase 2 — AI-Ready Backend"
}
```

---

### Get Documents

```http
GET /documents/
```

Query parameters:

```text
limit
skip
```

Default values:

```text
limit = 10
skip = 0
```

Returns a list of stored documents.

---

### Get Document

```http
GET /documents/{id}
```

Returns a single document by its ID.

---

### Upload Document

```http
POST /documents/upload
```

Request:

```text
multipart/form-data
file=<PDF or DOCX>
```

Validation:

- Only `.pdf` and `.docx` files are accepted.
- File size must be less than or equal to 10 MB according to the project's size validation.
- The extracted document must contain text.

---

### Generate Document Embedding

```http
POST /documents/{id}/embed
```

Generates an embedding from the stored document content and saves it to the document's vector column.

Example response:

```json
{
  "Status": "Document 1 successfully embedded"
}
```

---

### Semantic Search

```http
POST /documents/search
```

Query parameters:

```text
query
limit
```

Default:

```text
limit = 5
```

The query is embedded and compared against documents that already have an embedding.

---

### Delete Document

```http
DELETE /documents/{id}
```

Deletes a document by ID.

---

## Semantic Search

The semantic search pipeline is the core AI-related part of the project.

Given a query such as:

```text
"How does containerization help application deployment?"
```

the API first generates an embedding:

```text
Text
  │
  ▼
all-MiniLM-L6-v2
  │
  ▼
384-dimensional vector
```

The vector is then compared against document embeddings stored in PostgreSQL.

The database query uses cosine distance:

```text
cosine distance(query_embedding, document_embedding)
```

Documents are ordered by their distance, with the closest vectors returned first.

### Vector Index

The document embedding column uses a PostgreSQL HNSW index configured with:

```text
m = 16
ef_construction = 64
vector_cosine_ops
```

This provides an indexed structure for vector similarity search.

---

## Document Processing

The project separates file extraction from the API routing layer.

### PDF

PDF files are processed using:

```python
pypdf.PdfReader
```

Text is extracted page by page and combined into a single string.

### DOCX

DOCX files are processed using:

```python
python-docx
```

The application collects non-empty paragraphs and combines them into the document text.

### Text Cleaning

Extracted text is passed through a cleaning decorator that:

- Normalizes whitespace.
- Removes characters outside the supported ASCII range.

### Async Integration

The underlying PDF and DOCX extraction operations are synchronous, so the project executes them through the event loop's executor:

```text
FastAPI async endpoint
        │
        ▼
async extraction function
        │
        ▼
run_in_executor(...)
        │
        ▼
synchronous PDF/DOCX extraction
```

This keeps the blocking extraction work away from the main async execution path.

---

## Database Design

The project currently uses a `documents` table.

### Document fields

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `name` | String | Uploaded filename |
| `content` | Text | Extracted document text |
| `word_count` | Integer | Number of words |
| `uploaded_at` | DateTime | Upload timestamp |
| `embedding` | Vector(384) | Semantic document embedding |

The embedding column is nullable because documents can exist before their embeddings are generated.

The semantic search query only considers documents whose embeddings are not null.

---

## Docker Setup

The project uses two services:

```text
┌─────────────────────┐
│       API           │
│     FastAPI         │
│     Port 8000       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     PostgreSQL      │
│      pgvector       │
│       pg16          │
└─────────────────────┘
```

The database service uses:

```text
pgvector/pgvector:pg16
```

The API service is built from the project's `Dockerfile`.

Docker Compose also includes:

- A PostgreSQL health check
- Persistent database storage through the `doc_data` volume
- API-to-database service dependency
- Port `8000` exposed for the API

---

## Environment Configuration

The application reads the database connection through:

```text
DATABASE_URL
```

Docker Compose also loads environment configuration from:

```text
.env
```

The `.env` file is intentionally not part of the repository.

Configure the environment variables required by your local Docker/PostgreSQL setup before starting the services.

---

## Running the Project

### Prerequisites

You need:

- Docker
- Docker Compose
- A `.env` file containing the required database configuration

The project targets:

```text
Python >= 3.12
```

### Start the application

From the project root:

```bash
docker compose up --build
```

The API is exposed on:

```text
http://localhost:8000
```

Interactive FastAPI documentation:

```text
http://localhost:8000/docs
```

The Docker image uses `uv` for dependency installation and starts the application through the project's `dev` script.

---

## Example Workflow

A typical document retrieval workflow is:

### Step 1 — Upload

```http
POST /documents/upload
```

Upload a PDF or DOCX document.

The API extracts its text and stores the document.

### Step 2 — Generate the embedding

If the uploaded document receives ID `1`:

```http
POST /documents/1/embed
```

The document content is converted into a 384-dimensional embedding.

### Step 3 — Search

Send a natural-language query:

```http
POST /documents/search
```

For example:

```text
query = "What is discussed about database indexing?"
```

The query is embedded and compared with stored document vectors.

### Step 4 — Retrieve

The API returns the documents with the smallest cosine distance to the query embedding.

---

## Phase 2 Learning Goals

This project was built as the proof project for the **Backend for AI Engineers — Phase 2** roadmap.

The original roadmap focuses on:

- FastAPI
- REST APIs
- Dependency injection
- Background tasks
- Streaming responses
- Pydantic v2
- PostgreSQL + pgvector
- Vector similarity search
- Docker
- Docker Compose
- Async I/O
- Environment management
- Rate limiting basics

This implementation focuses on the parts directly required by the project's architecture.

Because this project generates embeddings locally using `sentence-transformers` rather than calling an external embedding API, it does not require an external API client such as `httpx` for embedding generation.

Likewise, streaming responses and API rate limiting are outside the implemented scope of this version.

---

## What This Project Demonstrates

This project demonstrates the backend foundations required by AI applications:

### API Layer

Building a REST API with FastAPI and organizing endpoints using routers.

### Async Backend

Using:

- `AsyncSession`
- `async_sessionmaker`
- async database operations
- async FastAPI endpoints
- executor-based handling for synchronous document extraction

### Database Layer

Using SQLAlchemy with PostgreSQL and managing database sessions through FastAPI dependency injection.

### Vector Database Capabilities

Using PostgreSQL + pgvector to:

- store embeddings
- create an HNSW vector index
- perform cosine-distance similarity search

### AI Integration

Using a local sentence-transformer model to transform text into embeddings.

### Containerization

Packaging the API and database infrastructure using Docker and Docker Compose.

---

## Current Scope

This project is primarily a **document storage + embedding + semantic retrieval API**.

It does not currently implement a complete generative RAG pipeline.

The implemented pipeline is:

```text
Document
   │
   ▼
Text Extraction
   │
   ▼
Embedding Generation
   │
   ▼
Vector Storage
   │
   ▼
Semantic Retrieval
```

A future RAG layer could build on top of this retrieval foundation by adding additional components for context construction and language-model response generation.

---

## Repository

GitHub:

https://github.com/Aditya01-crypto/DOC-QUERY-API

---

## Project Status

**Phase 2 — AI-Ready Backend**

The project establishes the backend and vector-search foundation for document-oriented AI applications.
