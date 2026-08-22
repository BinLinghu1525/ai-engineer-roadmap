from ragx.models import Chunk
from ragx.retrieval import hybrid_search


def _chunk(chunk_id: str, text: str) -> Chunk:
    return Chunk(chunk_id, chunk_id, f"{chunk_id}.md", text, 0, len(text.split()))


def test_hybrid_search_exposes_component_scores_and_ranks() -> None:
    chunks = [
        _chunk("bm25", "BM25 uses exact term frequency for retrieval"),
        _chunk("chunk", "Chunk boundaries preserve context"),
    ]

    hits = hybrid_search(chunks, "BM25 retrieval", top_k=1)

    assert hits[0].chunk.chunk_id == "bm25"
    assert hits[0].bm25_score > 0
    assert hits[0].vector_score > 0
    assert hits[0].bm25_rank == 1
    assert hits[0].vector_rank == 1
    assert set(hits[0].matched_terms) == {"bm25", "retrieval"}


def test_hybrid_search_is_deterministic_for_ties() -> None:
    chunks = [_chunk("b", "unrelated"), _chunk("a", "unrelated")]

    first = hybrid_search(chunks, "missing", top_k=2)
    second = hybrid_search(chunks, "missing", top_k=2)

    assert [hit.chunk.chunk_id for hit in first] == [hit.chunk.chunk_id for hit in second]
