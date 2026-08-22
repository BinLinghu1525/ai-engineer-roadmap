from pathlib import Path

from ragx.evaluation import evaluate_retrieval, load_cases
from ragx.pipeline import ExplainableRAG


PROJECT = Path(__file__).resolve().parents[1]


def test_sample_retrieval_baseline_is_measurable() -> None:
    engine = ExplainableRAG(PROJECT / "fixtures" / "corpus")
    cases = load_cases(PROJECT / "fixtures" / "eval_cases.json")

    report = evaluate_retrieval(engine, cases, top_k=3)

    assert report["case_count"] == 6
    assert 0 <= report["hit_rate_at_k"] <= 1
    assert 0 <= report["mrr"] <= 1
    assert len(report["cases"]) == 6
