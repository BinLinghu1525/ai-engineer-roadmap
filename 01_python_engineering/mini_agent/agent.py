"""Stateful learning session built on top of the service layer."""

import service


class LearningSession:
    """Track successfully completed learning topics in memory."""

    def __init__(self) -> None:
        self.completed_topics: list[str] = []

    def complete_topic(self, topic: str) -> str:
        """Create a learning message and record the normalized topic."""
        message = service.create_learning_message(topic)
        normalized_topic = message.removeprefix("Today we learn: ")
        self.completed_topics.append(normalized_topic)
        return message
