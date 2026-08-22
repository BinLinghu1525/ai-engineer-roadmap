"""Paragraph-aware chunking with visible boundaries."""

import re

from .models import Chunk, Document
from .text import tokenize


def _paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def chunk_document(document: Document, max_tokens: int = 90) -> list[Chunk]:
    """Group adjacent paragraphs without silently splitting provenance."""
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")

    groups: list[list[str]] = []
    current: list[str] = []
    current_tokens = 0

    for paragraph in _paragraphs(document.text):
        paragraph_tokens = len(tokenize(paragraph))
        if current and current_tokens + paragraph_tokens > max_tokens:
            groups.append(current)
            current = []
            current_tokens = 0
        current.append(paragraph)
        current_tokens += paragraph_tokens

    if current:
        groups.append(current)

    return [
        Chunk(
            chunk_id=f"{document.document_id}::c{position:03d}",
            document_id=document.document_id,
            source=document.source,
            text="\n\n".join(group),
            position=position,
            token_count=len(tokenize("\n\n".join(group))),
        )
        for position, group in enumerate(groups)
    ]


def chunk_documents(documents: list[Document], max_tokens: int = 90) -> list[Chunk]:
    """Chunk every document while preserving stable IDs."""
    return [chunk for document in documents for chunk in chunk_document(document, max_tokens)]
