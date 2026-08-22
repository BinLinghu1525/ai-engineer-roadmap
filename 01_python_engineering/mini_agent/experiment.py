"""Run a reproducible input-validation experiment from JSON data."""

import json
from pathlib import Path
from typing import Any

from agent import LearningSession


DATA_PATH = Path(__file__).parent / "fixtures" / "topic_cases.json"


def run_case(case: dict[str, Any]) -> dict[str, Any]:
    """Run one documented case and return structured evidence."""
    session = LearningSession()

    try:
        message = session.complete_topic(case["input"])
        return {
            "id": case["id"],
            "status": "success",
            "message": message,
            "completed_topics": session.completed_topics,
        }
    except (TypeError, ValueError) as error:
        return {
            "id": case["id"],
            "status": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "completed_topics": session.completed_topics,
        }


def main() -> None:
    """Load the dataset, run every case, and print JSON results."""
    cases = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    results = [run_case(case) for case in cases]
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
