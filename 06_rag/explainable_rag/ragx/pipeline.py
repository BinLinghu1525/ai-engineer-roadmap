"""End-to-end evidence-first RAG orchestration."""

import re
from pathlib import Path

from .chunking import chunk_documents
from .models import RAGAnswer, SearchHit
from .retrieval import hybrid_search
from .text import load_documents, tokenize


def _best_sentence(text: str, query: str) -> str:
    query_terms = set(tokenize(query))
    sentences = [part.strip() for part in re.split(r"(?<=[。！？.!?])\s*", text) if part.strip()]
    return max(
        sentences or [text],
        key=lambda sentence: len(query_terms.intersection(tokenize(sentence))),
    )


class ExplainableRAG:
    """A transparent baseline that separates retrieval from answer synthesis."""

    def __init__(self, corpus_dir: Path, max_chunk_tokens: int = 90) -> None:
        self.documents = load_documents(corpus_dir)
        self.chunks = chunk_documents(self.documents, max_tokens=max_chunk_tokens)
        if not self.chunks:
            raise ValueError(f"no supported documents found in {corpus_dir}")

    def retrieve(self, query: str, top_k: int = 3) -> list[SearchHit]:
        if not query.strip():
            raise ValueError("query cannot be empty")
        return hybrid_search(self.chunks, query, top_k=top_k)

    def answer(self, query: str, top_k: int = 3) -> RAGAnswer:
        """Build an extractive answer so every statement maps to evidence."""
        hits = self.retrieve(query, top_k=top_k)
        if not hits:
            return RAGAnswer(
                query=query,
                answer="Insufficient evidence in the indexed corpus.",
                hits=(),
            )
        evidence = [
            f"[{index}] {_best_sentence(hit.chunk.text, query)}"
            for index, hit in enumerate(hits, start=1)
        ]
        answer = "Evidence-first answer:\n" + "\n".join(evidence)
        return RAGAnswer(query=query, answer=answer, hits=tuple(hits))
