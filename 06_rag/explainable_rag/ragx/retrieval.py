"""Inspectible BM25, TF-IDF cosine, and reciprocal-rank fusion."""

import math
from collections import Counter
from dataclasses import replace

from .models import Chunk, SearchHit
from .text import tokenize


class BM25Retriever:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75) -> None:
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.tokens = [tokenize(chunk.text) for chunk in chunks]
        self.term_counts = [Counter(tokens) for tokens in self.tokens]
        self.average_length = sum(map(len, self.tokens)) / max(len(self.tokens), 1)
        document_frequency: Counter[str] = Counter()
        for tokens in self.tokens:
            document_frequency.update(set(tokens))
        size = len(chunks)
        self.idf = {
            term: math.log(1 + (size - frequency + 0.5) / (frequency + 0.5))
            for term, frequency in document_frequency.items()
        }

    def scores(self, query: str) -> list[float]:
        query_terms = tokenize(query)
        scores: list[float] = []
        for tokens, counts in zip(self.tokens, self.term_counts):
            length_ratio = len(tokens) / max(self.average_length, 1.0)
            score = 0.0
            for term in query_terms:
                frequency = counts[term]
                if not frequency:
                    continue
                numerator = frequency * (self.k1 + 1)
                denominator = frequency + self.k1 * (1 - self.b + self.b * length_ratio)
                score += self.idf.get(term, 0.0) * numerator / denominator
            scores.append(score)
        return scores


class TfidfCosineRetriever:
    """A deterministic vector baseline whose dimensions remain explainable."""

    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.tokens = [tokenize(chunk.text) for chunk in chunks]
        frequency: Counter[str] = Counter()
        for tokens in self.tokens:
            frequency.update(set(tokens))
        size = len(chunks)
        self.idf = {
            term: math.log((size + 1) / (count + 1)) + 1
            for term, count in frequency.items()
        }
        self.vectors = [self._vector(tokens) for tokens in self.tokens]

    def _vector(self, tokens: list[str]) -> dict[str, float]:
        counts = Counter(tokens)
        weighted = {term: count * self.idf.get(term, 0.0) for term, count in counts.items()}
        norm = math.sqrt(sum(value * value for value in weighted.values())) or 1.0
        return {term: value / norm for term, value in weighted.items()}

    def scores(self, query: str) -> list[float]:
        query_vector = self._vector(tokenize(query))
        return [
            sum(query_vector.get(term, 0.0) * value for term, value in vector.items())
            for vector in self.vectors
        ]


def _rank(scores: list[float]) -> dict[int, int]:
    ordered = sorted(range(len(scores)), key=lambda index: (-scores[index], index))
    return {index: rank for rank, index in enumerate(ordered, start=1)}


def hybrid_search(
    chunks: list[Chunk], query: str, top_k: int = 5, rrf_k: int = 60
) -> list[SearchHit]:
    """Fuse BM25 and TF-IDF rankings and expose every component score."""
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    bm25_scores = BM25Retriever(chunks).scores(query)
    vector_scores = TfidfCosineRetriever(chunks).scores(query)
    bm25_ranks = _rank(bm25_scores)
    vector_ranks = _rank(vector_scores)
    query_terms = set(tokenize(query))

    hits = []
    for index, chunk in enumerate(chunks):
        if bm25_scores[index] <= 0 and vector_scores[index] <= 0:
            continue
        fused = 1 / (rrf_k + bm25_ranks[index]) + 1 / (rrf_k + vector_ranks[index])
        matched = tuple(sorted(query_terms.intersection(tokenize(chunk.text))))
        hits.append(
            SearchHit(
                chunk=chunk,
                rank=0,
                rrf_score=fused,
                bm25_score=bm25_scores[index],
                vector_score=vector_scores[index],
                bm25_rank=bm25_ranks[index],
                vector_rank=vector_ranks[index],
                matched_terms=matched,
            )
        )

    ordered = sorted(hits, key=lambda hit: (-hit.rrf_score, hit.chunk.chunk_id))[:top_k]
    return [replace(hit, rank=rank) for rank, hit in enumerate(ordered, start=1)]
