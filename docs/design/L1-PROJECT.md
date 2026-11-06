# Local RAG Knowledge Base

## Purpose

- A standalone, locally operated document knowledge base that allows users and AI applications to retrieve information from their own collections of documents using natural-language queries.

- Provide a practical personal knowledge-retrieval system that can be used independently or through external AI applications.
- Demonstrate database engineering, applied AI integration, document processing and software engineering practices.

## Capabilities

Users should be able to:

- Import individual documents or entire directories.
- Maintain a collection of documents, including listing, updating and deleting entries.
- Search documents by semantic relevance rather than relying solely on exact keywords.
- View retrieved passages with references to their original sources.
- Ask natural-language questions and receive answers grounded in retrieved information.
- Make the knowledge base available to compatible external AI applications through MCP.

The initial document formats are PDF, TXT, Markdown and DOCX.

## Product Principles

- **Local-first:** Document storage, embedding and retrieval operate locally without requiring cloud services.
- **Reusable:** The knowledge base remains independent of any particular generative LLM or AI client.
- **Traceable:** Retrieved information should be attributable to its original document.
- **Maintainable:** Documents can be replaced, re-indexed or removed without rebuilding the entire collection.
- **Simple:** Prioritise a reliable, understandable implementation over unnecessary abstractions.

## Initial Scope

The product provides a command-line interface and an MCP interface. A graphical interface, hosted deployment, multi-user administration and autonomous agents are outside the initial scope.

## Success Criteria

The system can ingest a mixed collection of supported documents, retrieve relevant passages, answer questions using a local generative model and serve retrieval requests from an external MCP client.
