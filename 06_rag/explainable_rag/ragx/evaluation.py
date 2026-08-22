"""Retrieval evaluation kept separate from answer generation."""

import json
from pathlib import Path
from typing import Any

from .pipeline import ExplainableRAG


def load_cases(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_retrieval(
    engine: ExplainableRAG, cases: list[dict[str, Any]], top_k: int = 3
) -> dict[str, Any]:
    rows = []
    reciprocal_ranks = []
    hits_at_k = []

    for case in cases:
        hits = engine.retrieve(case["query"], top_k=top_k)
        retrieved = [hit.chunk.document_id for hit in hits]
        relevant = set(case["relevant_documents"])
        first_rank = next(
            (rank for rank, document_id in enumerate(retrieved, start=1) if document_id in relevant),
            None,
        )
        reciprocal_rank = 1 / first_rank if first_rank else 0.0
        hit_at_k = first_rank is not None
        reciprocal_ranks.append(reciprocal_rank)
        hits_at_k.append(hit_at_k)
        rows.append(
            {
                "id": case["id"],
                "query": case["query"],
                "retrieved_documents": retrieved,
                "first_relevant_rank": first_rank,
                "hit_at_k": hit_at_k,
                "reciprocal_rank": round(reciprocal_rank, 4),
            }
        )

    count = len(cases) or 1
    return {
        "top_k": top_k,
        "case_count": len(cases),
        "hit_rate_at_k": round(sum(hits_at_k) / count, 4),
        "mrr": round(sum(reciprocal_ranks) / count, 4),
        "cases": rows,
    }
