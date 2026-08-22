import pytest

from agent import LearningSession


def test_completed_topics_are_isolated_between_sessions() -> None:
    first = LearningSession()
    second = LearningSession()

    first.complete_topic("Python")

    assert first.completed_topics == ["python"]
    assert second.completed_topics == []


def test_failed_topic_does_not_change_state() -> None:
    session = LearningSession()

    with pytest.raises(ValueError):
        session.complete_topic("   ")

    assert session.completed_topics == []
