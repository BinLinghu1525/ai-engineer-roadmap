import formatter


def create_learning_message(topic: str) -> str:
    """Create the final learning message for a given topic.

    Single responsibility: compose the output message using normalized topic.
    """
    if not isinstance(topic, str):
        raise TypeError("topic must be a string")

    if not topic.strip():
        raise ValueError("topic cannot be empty")

    normalized = formatter.normalize_topic(topic)
    return f"Today we learn: {normalized}"
