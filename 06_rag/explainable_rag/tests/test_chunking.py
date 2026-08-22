from ragx.chunking import chunk_document
from ragx.models import Document


def test_chunk_preserves_provenance_and_stable_id() -> None:
    document = Document("guide", "guide.md", "First paragraph.\n\nSecond paragraph.")
    chunks = chunk_document(document, max_tokens=3)

    assert [chunk.chunk_id for chunk in chunks] == ["guide::c000", "guide::c001"]
    assert all(chunk.source == "guide.md" for chunk in chunks)


def test_chunk_size_must_be_positive() -> None:
    document = Document("guide", "guide.md", "text")

    try:
        chunk_document(document, max_tokens=0)
    except ValueError as error:
        assert str(error) == "max_tokens must be positive"
    else:
        raise AssertionError("expected ValueError")
