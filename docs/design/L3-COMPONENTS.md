# L3 — Component Design

## Summary

The Local RAG Knowledge Base is a single-user Python application with (all local):

- PostgreSQL/pgvector
- Ollama

It supports (all local):

- document ingestion
- maintenance
- semantic retrieval
- question answering
- read-only MCP access.

The following defines component responsibilities, interfaces, data contracts, and observable behaviour.

---

## Components

### CLI Layer

The CLI layer is the administrative and interactive interface. It takes:

- document paths
- questions
- invokes shared application operations
- writes successful results to stdout
- reports errors to stderr with nonzero exit status

### MCP server

A local stdio MCP server exposes bounded, READ-ONLY document access to compatible clients. It uses the same retrieval and persistence operations as the CLI.

It does NOT expose:

- ingestion
- deletion
- re-embedding
- arbitrary file access
- SQL execution

### Document loader and chunker

- Supported inputs: UTF-8 TXT, Markdown, text-extractable PDF, and DOCX.
- Extract text in original order, together with source locations when available.
- Split text into ordered, overlapping chunks, preferring paragraph and sentence boundaries.
- Initial target: 500 tokens per chunk with 75 tokens of overlap. These are configurable, not fixed assumptions about every document.
- Record source-file SHA-256 values for change detection.
- Report unsupported, unreadable, or image-only documents without creating incomplete records. OCR is outside the initial scope.

### Embedding adapter

The embedding adapter invokes the configured Ollama embedding model for both stored chunks and search queries. It applies the configured document/query prefixes and supplies the resulting vectors to the persistence or retrieval components.

Initial profile:

- `nomic-embed-text:v1.5`
- 768 dimensions
- `search_document:` for document inputs
- `search_query:` for queries

### Persistence

PostgreSQL with pgvector stores document metadata, source text chunks, embeddings, and active configuration metadata. It owns document creation, replacement, deletion, vector searches, and database-consistent embedding migrations. No separate vector database service is required.

### Retrieval

The retrieval component validates embedding compatibility, embeds the query, performs a vector similarity search, and returns ranked text passages with source references. It is independent of answer generation.

Defaults:

- exact cosine-distance search
- five results
- no HNSW or IVFFlat index
- `top-k` can be overridden per query

### Answer generator

The answer generator retrieves passages, provides the question and retrieved evidence to the configured Ollama generative model, and returns an answer with available source references. It treats retrieved content as source material rather than instructions and does not invent citations. If retrieval offers insufficient evidence, the answer should say so.

Initial model: `qwen3:4b-instruct`. Questions are independent; persistent conversation history is not part of the initial interface.

---

## Data contracts

### Documents

A document record contains:

- stable ID
- filename
- file type
- original source path
- SHA-256 of the source file
- created/updated timestamps
- optional metadata

Note:

- Source paths distinguish separate imported files; matching hashes identify unchanged content.
- Two files with identical bytes at different paths may be stored separately.
- Chunk text remains stored for retrieval and subsequent re-embedding, but the original source documents are not retained.

### Chunks

Each chunk has:

- stable ID
- parent document ID
- zero-based chunk order
- extracted text
- embedding
- optional location metadata

Note:

- Deleting a document deletes its chunks. Soft deletion and recovery operations are not provided.
- Updating a document replaces its chunk set only after the new set is prepared successfully.
- Re-chunking requires access to the original source documents.
- The active embedding column normally has an explicit dimension constraint, initially `embedding VECTOR(768)`.

### Source references

References identify the document and, where reliably available, a source location:

| Format         | Preferred location       |
| -------------- | ------------------------ |
| PDF            | Page or page range       |
| TXT / Markdown | Line range               |
| DOCX           | Paragraph index or range |

Return the document ID, filename, and chunk index when an exact location is unavailable. Displayed page and line numbers are one-based. Do not infer a page or line number that was not captured.

### Active profiles

The database records the active embedding profile:

- model identifier
- resolved model identity/digest when available
- vector dimensions
- document/query preprocessing
- relevant model settings

Note:

- One embedding profile is active for the knowledge base at a time.
- The chunking profile (target size, overlap, and relevant splitting configuration) is recorded separately.
- Re-embedding preserves stored chunks and does not alter this profile.
- Environment settings express the desired runtime configuration.
- Database metadata describes the configuration that actually produced stored embeddings.
- Vector compatibility is checked before operations that generate or search embeddings.

---

## CLI contract

| Command                                      | Behaviour                                                                       |
| -------------------------------------------- | ------------------------------------------------------------------------------- |
| `rag init`                                   | Initialise database structures and configuration storage.                       |
| `rag ingest <path>`                          | Import or update one supported file or a directory recursively.                 |
| `rag list`                                   | List document IDs, filenames, and status information.                           |
| `rag search <query> [--top-k N]`             | Return ranked passages with source references.                                  |
| `rag ask <question>`                         | Retrieve passages and generate a grounded answer.                               |
| `rag delete <document-id>`                   | Delete a document and its stored chunks.                                        |
| `rag reindex --embedding-model <model-name>` | Regenerate embeddings from stored chunks and activate the replacement profile.  |
| `rag status`                                 | Show service availability, database status, active profiles, and compatibility. |
| `rag mcp`                                    | Run the local read-only MCP server.                                             |

### Ingest

For each file, identify the document by:

- source path
- SHA-256 hash
- skip it if the stored hash matches

Otherwise:

- extract and chunk the text
- generate embeddings
- replace the corresponding stored record and chunks as one successful document update
- A failed file does not partially replace its previous version

Note:

- Recursive directory imports report imported, updated, skipped, and failed files separately. Unsupported files are skipped with a reason.
- The default embedding model produces 768-dimensional vectors.
- On a fresh database, the first ingestion determines the embedding dimensions from the configured model and establishes the corresponding database schema.

### Search

Validate the active embedding profile, embed the query with the query-specific preprocessing, run exact cosine-distance retrieval, and return at most the requested number of matching chunks. Results include text, source reference, document ID, chunk index, and distance/similarity information where useful. A similarity score is not presented as a calibrated probability.

### Ask

Use the same retrieval path as `rag search`, then send retrieved passages to the generative model with the question. Return the answer and source references to stdout. Model failures do not modify stored documents or embeddings.

### List, delete, and status

List and delete use stable document IDs to avoid ambiguous filenames. Deletion does not remove original files from the filesystem. Status remains available even when the configured embedding model differs from the database's active profile.

---

## MCP interface

### `search_documents`

Accept a natural-language query and optional result count. Return bounded ranked chunks with their text, document ID, filename, chunk index, available source location, and relevance information. Use the same compatibility checks as CLI search.

### `get_document`

Accept a document ID and optional chunk range or pagination information. Return document metadata and a bounded portion of stored chunk text with source references. Reject unknown IDs and invalid ranges.

The MCP transport is stdio. Protocol output must not be mixed with human-readable logging on stdout. MCP clients decide when to call tools and how to use returned passages.

---

## Embedding configuration and compatibility

The public repository includes `.env.example`; `.env` is local and excluded from version control. Initial settings include:

| Setting             | Initial value                       |
| ------------------- | ----------------------------------- |
| Ollama endpoint     | `http://localhost:11434`            |
| Embedding model     | `nomic-embed-text:v1.5`             |
| Generative model    | `qwen3:4b-instruct`                 |
| Document prefix     | `search_document:`                  |
| Query prefix        | `search_query:`                     |
| Chunk target        | 500 tokens                          |
| Chunk overlap       | 75 tokens                           |
| Search result count | 5                                   |
| Database            | Local PostgreSQL via Docker Compose |

Model names and endpoints are configuration values, not application constants. Embedding profiles are identified by the model and preprocessing configuration actually used, not by vector dimensions alone.

When a nonempty collection is accessed for ingestion or retrieval, compare the configured embedding profile with the database's active profile. A mismatch produces an actionable error identifying the conflicting settings and the `rag reindex` command. For a new, empty collection, establish the active profile when first populating it.

Before ingestion, also compare the configured chunking profile with the stored chunking profile. Reject a change that would silently mix chunking strategies. Existing retrieval and embedding migration continue to use the stored chunks.

Changing the configured generative model does not invalidate embeddings.

---

## Embedding migration

### Command contract

`rag reindex --embedding-model <model-name>` recomputes vectors from the **existing stored chunk text** using the requested embedding model. It keeps document IDs, chunk IDs, text, ordering, source references, and chunk boundaries unchanged. Original PDF, DOCX, TXT, and Markdown files are not needed.

Re-embedding changes only the embedding profile and vector data; it does not re-chunk documents.

### Temporary staging column

During normal operation, the chunks table contains one active, dimension-constrained embedding column, initially `embedding VECTOR(768)`.

When migration starts, the application determines the target model's vector length and temporarily adds a **`next_embedding VECTOR(n)`** column using that length. The application populates this column for all existing chunks while retaining the active embeddings.

`next_embedding` is absent from the initial schema and absent again after a successful migration. The target dimension is determined at runtime rather than hardcoded.

### Promotion and failure behaviour

1. Verify the target model and its embedding/preprocessing configuration.
2. Prevent concurrent normal operations for the duration of the migration.
3. Add the temporary `next_embedding` column and populate it from existing chunk text.
4. Verify that every stored chunk has a valid new vector of the expected dimension.
5. In one database transaction, replace the active embedding column with the completed replacement, update the active embedding profile, and remove the obsolete column.
6. Release the migration restriction and report the outcome.

If embedding or validation fails before promotion, preserve the original active column and profile. Staging data may be discarded or safely cleaned up before another attempt. A failed migration must not make a mixture of model representations available to retrieval.

Migration is synchronous in the initial release. Status inspection and recovery information remain available during or after failure. After a successful migration, inform the user that they must align `.env` with the newly active model and preprocessing configuration before ordinary search or ingestion resumes.

### Chunking changes

- Chunk target and overlap are independently configurable.
- Re-embedding does not apply new chunking settings to existing text.

Changing the chunking profile requires re-extracting and re-chunking the source documents, followed by new embeddings. That process requires accessible source files or separately preserved full extracted text; the stored chunks alone are not assumed to reproduce the original document faithfully. Re-chunking is NOT part of `rag reindex`.

---

## Failures and operational behaviour

Operations report actionable failures for unavailable PostgreSQL or Ollama services, missing models, unsupported or unreadable documents, empty PDF text extraction, invalid document identifiers, incompatible embedding profiles, invalid queries, and incomplete migrations.

Per-file ingestion failures do not corrupt previously stored documents. Answer generation failure does not modify the knowledge base. A migration failure before promotion preserves the previous active embedding state.

---

## Testing and verification

### Component tests

- Document extraction and source-location handling by format.
- Chunk ordering, overlap, and boundaries.
- SHA-256 skipping and modified-file replacement.
- Vector search ranking and `top-k` limits.
- Embedding and chunking configuration drift detection, including same-dimension model changes.
- Answer generation using supplied passages.
- CLI and MCP input/output contracts.

### Integration tests

#### Success scenarios

- Ingest, list, search, update, and delete against PostgreSQL.
- Retrieve the same stored evidence through CLI and MCP.
- Re-embed from stored chunks without accessing the original files.
- Migrate to a model with different vector dimensions.
- Confirm that `next_embedding` exists only during migration and the normal schema is restored afterward.

#### Failure scenarios

- Confirm preserving previous records after ingestion fails.
- Simulate migration failure and verify that the original active embeddings and profile remain usable.
- Confirm expected behavior:
  - Use invalid document identifiers, unsupported or unreadable documents, empty text extraction, invalid queries, and incompatible embedding profiles.

### Retrieval evaluation

Use a small synthetic document collection with known answers and expected source passages.

- Check whether the expected passages appear in the top results.
- Confirm expected behavior when fewer than `top-k` passages are available.
- Separately evaluate answer quality and retrieval quality. Expanded evaluation tooling is not required for initial operation.

---

## Completion criteria

The initial release is complete when the CLI can manage supported documents, retrieve evidence with source references, and answer questions through a local generative model; an external MCP client can access read-only search and document retrieval; configuration mismatches are detected; and re-embedding can safely replace active vectors, including when the new model uses a different dimension count.
