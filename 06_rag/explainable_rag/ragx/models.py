"""Shared data contracts for the RAG pipeline."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Document:
    document_id: str
    source: str
    text: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    source: str
    text: str
    position: int
    token_count: int


@dataclass(frozen=True)
class SearchHit:
    chunk: Chunk
    rank: int
    rrf_score: float
    bm25_score: float = 0.0
    vector_score: float = 0.0
    bm25_rank: int | None = None
    vector_rank: int | None = None
    matched_terms: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RAGAnswer:
    query: str
    answer: str
    hits: tuple[SearchHit, ...]
