# L4 — Implementation

Use the `scaffolding-as-context` skill to consume the source scaffolds. Preserve the contractual schema in `src/rag/storage/schema.py`.

- CLI and MCP are adapters over shared operations.
- SQL belongs in `storage/`.
- Ollama calls in `models/`.
- extraction/chunking in `documents/`.
- Keep the existing `rag.__main__:main` entry point and connect it to the CLI during implementation.

- Use the CLI/MCP behaviour and test requirements in L3. Do not introduce new persistence systems, frameworks, or public commands without approval. - Flag conflicts rather than silently changing contractual anchors.

## VECTOR(n)

- `rag init` creates the baseline tables but does not select an embedding dimension.
- The first successful ingestion adds `chunks.embedding VECTOR(n) NOT NULL` and establishes the active profile in the same transaction.
- During re-embedding, add `next_embedding VECTOR(n)`, populate and validate it, then atomically promote it and the profile.
- The temporary column must not persist after successful migration.
