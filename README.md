# Local RAG Knowledge Base

A standalone, locally operated document knowledge base for semantic retrieval and question answering using your own documents.

## Features

- Import and maintain documents (PDF, TXT, Markdown, DOCX)
- Semantic search with source references
- Natural-language Q&A grounded in retrieved content
- Read-only MCP server for external AI applications
- Local-first: PostgreSQL/pgvector + Ollama, no cloud services required

## Quick Start

```bash
# Install dependencies
uv sync --locked

# Configure environment (see .env.example)
cp .env.example .env

# Initialise database
rag init

# Import documents
rag ingest /path/to/documents

# Search
rag search "your query"

# Ask questions
rag ask "your question"
```

## Requirements

- Python 3.14+
- PostgreSQL with pgvector extension
- Ollama (with embedding and generation models)

## Development

Run `./check.sh` for linting, formatting, type checking, and tests.

## Documentation

See `docs/design/` for detailed design and component specifications.
