# System Architecture

## Overview

The system consists of one Python application and two local services:

1. **Python application:** Document processing, ingestion, retrieval, answer generation and external interfaces.
2. **PostgreSQL with pgvector:** Persistent storage of documents, text chunks, embeddings and metadata.
3. **Ollama:** Local inference service providing independently configurable embedding and generative models.

PostgreSQL runs in Docker Compose. Ollama and the Python application initially run on the host.

## Application Structure

The Python application separates its core functionality from its interfaces.

### Core Responsibilities

- **Document loading:** Extract text and source information from supported formats.
- **Ingestion:** Split text into overlapping chunks, generate embeddings and persist the results.
- **Document management:** Identify documents using SHA-256 hashes and support listing, replacement and deletion.
- **Retrieval:** Embed search queries, perform vector similarity searches and return matching passages with source references.
- **Answer generation:** Supply retrieved passages to a generative LLM and return its response.

### Interfaces

- **CLI:** Supports document management, semantic search and question answering. Results are displayed through standard output.
- **MCP server:** Exposes read-only document search and retrieval tools to compatible AI clients, such as Codex.

Both interfaces reuse the same application logic.

## Data Architecture

PostgreSQL maintains separate logical records for documents and their associated text chunks.

Document records contain source information, file hashes and metadata. Chunk records contain text, embeddings, ordering information and optional source locations such as PDF pages, text-file line ranges or DOCX paragraph references.

Retrieval initially uses exact cosine similarity search.

## Model Integration

Embedding and generative models are separate, configurable dependencies.

The initial models are:

- Embedding: `nomic-embed-text:v1.5`
- Generation: `qwen3:4b-instruct`

Model identifiers and service configuration are externalised through environment variables. The public repository provides `.env.example`; local overrides are provided in an ignored `.env`.

The database records the embedding model identifier, vector dimensions and relevant embedding configuration used to generate its stored vectors.

Before ingestion or retrieval, the application validates that the configured embedding model matches the database's recorded configuration. If they differ, the operation fails with a clear message indicating that re-indexing is required.

Model migration is a separate operation and must not leave incompatible embeddings mixed in the active collection.

## Boundaries

- No application-specific agent or orchestration framework is required.
- MCP clients remain responsible for their own reasoning and tool invocation.
- Document ingestion and database modification are not exposed through the initial read-only MCP interface.

## Implementation Constraints

Use Python with `uv` for project management and `pytest` for testing. Keep document processing, persistence, model integration and external interfaces independently testable.
