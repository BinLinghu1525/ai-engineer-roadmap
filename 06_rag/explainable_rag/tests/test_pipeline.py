from pathlib import Path

import pytest

from ragx.pipeline import ExplainableRAG


CORPUS = Path(__file__).resolve().parents[1] / "fixtures" / "corpus"


def test_answer_contains_ranked_evidence_and_sources() -> None:
    engine = ExplainableRAG(CORPUS)

    result = engine.answer("BM25 错误码 精确关键词", top_k=2)

    assert "Evidence-first answer:" in result.answer
    assert "[1]" in result.answer
    assert result.hits[0].chunk.document_id == "retrieval"
    assert all(hit.chunk.source.endswith(".md") for hit in result.hits)


def test_empty_query_is_rejected() -> None:
    engine = ExplainableRAG(CORPUS)

    with pytest.raises(ValueError, match="query cannot be empty"):
        engine.retrieve("   ")


def test_unknown_query_returns_insufficient_evidence() -> None:
    engine = ExplainableRAG(CORPUS)

    result = engine.answer("zzyyxx_nonexistent_term")

    assert result.answer == "Insufficient evidence in the indexed corpus."
    assert result.hits == ()
