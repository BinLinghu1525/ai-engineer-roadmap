import formatter


def test_normalize_topic_trims_and_lowercases() -> None:
    assert formatter.normalize_topic("  PYTHON Agent  ") == "python agent"


def test_normalize_topic_preserves_unicode() -> None:
    assert formatter.normalize_topic("  Agent 状态  ") == "agent 状态"
