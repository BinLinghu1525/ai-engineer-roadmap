"""Command-line interface for querying and evaluating the baseline."""

import argparse
import json
from pathlib import Path

from .evaluation import evaluate_retrieval, load_cases
from .pipeline import ExplainableRAG


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = PROJECT_DIR / "fixtures" / "corpus"
DEFAULT_EVAL = PROJECT_DIR / "fixtures" / "eval_cases.json"


def _engine() -> ExplainableRAG:
    return ExplainableRAG(DEFAULT_CORPUS)


def query_command(query: str, top_k: int) -> None:
    answer = _engine().answer(query, top_k=top_k)
    print(answer.answer)
    print("\nRetrieval trace:")
    for hit in answer.hits:
        print(
            f"#{hit.rank} {hit.chunk.chunk_id} source={hit.chunk.source} "
            f"rrf={hit.rrf_score:.6f} bm25={hit.bm25_score:.4f} "
            f"tfidf={hit.vector_score:.4f} bm25_rank={hit.bm25_rank} "
            f"tfidf_rank={hit.vector_rank} terms={list(hit.matched_terms)}"
        )


def evaluate_command(top_k: int) -> None:
    report = evaluate_retrieval(_engine(), load_cases(DEFAULT_EVAL), top_k=top_k)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Explainable hybrid RAG baseline")
    subparsers = parser.add_subparsers(dest="command", required=True)
    query_parser = subparsers.add_parser("query", help="retrieve evidence and answer")
    query_parser.add_argument("query")
    query_parser.add_argument("--top-k", type=int, default=3)
    eval_parser = subparsers.add_parser("evaluate", help="run retrieval evaluation")
    eval_parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    if args.command == "query":
        query_command(args.query, args.top_k)
    else:
        evaluate_command(args.top_k)


if __name__ == "__main__":
    main()
