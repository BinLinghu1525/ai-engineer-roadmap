def normalize_topic(topic: str) -> str:
    """Remove surrounding whitespace and convert to lowercase.

    Single responsibility: text normalization only.
    """
    return topic.strip().lower()
