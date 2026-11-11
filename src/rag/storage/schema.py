# Contractual: these table definitions are the initial PostgreSQL schema.
# The embedding column is added at first successful ingestion using the configured model's dimensions.

INITIAL_SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL CHECK (file_type IN ('txt', 'md', 'pdf', 'docx')),
    source_path TEXT NOT NULL UNIQUE,
    sha256 TEXT NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE chunks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_id BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL CHECK (chunk_index >= 0),
    content TEXT NOT NULL CHECK (length(btrim(content)) > 0),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (document_id, chunk_index)
);

CREATE TABLE knowledge_base_profile (
    id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    embedding_model TEXT NOT NULL,
    embedding_digest TEXT,
    embedding_dimensions INTEGER NOT NULL CHECK (embedding_dimensions > 0),
    document_prefix TEXT NOT NULL,
    query_prefix TEXT NOT NULL,
    chunk_size INTEGER NOT NULL CHECK (chunk_size > 0),
    chunk_overlap INTEGER NOT NULL CHECK (chunk_overlap >= 0),
    chunker_id TEXT NOT NULL,
    activated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (chunk_overlap < chunk_size)
);
"""
