import json

import pytest

from experiment import DATA_PATH, run_case


CASES = json.loads(DATA_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_documented_experiment_case(case: dict[str, object]) -> None:
    result = run_case(case)

    if "expected" in case:
        assert result["status"] == "success"
        assert result["message"] == case["expected"]
        assert result["completed_topics"]
    else:
        assert result["status"] == "error"
        assert result["error_type"] == case["expected_error"]
        assert result["completed_topics"] == []
