import pytest

import service


def test_create_learning_message() -> None:
    assert (
        service.create_learning_message("  PYTHON Agent  ")
        == "Today we learn: python agent"
    )


def test_rejects_blank_topic() -> None:
    with pytest.raises(ValueError, match="topic cannot be empty"):
        service.create_learning_message("   ")


def test_rejects_non_string_topic() -> None:
    with pytest.raises(TypeError, match="topic must be a string"):
        service.create_learning_message(123)  # type: ignore[arg-type]
